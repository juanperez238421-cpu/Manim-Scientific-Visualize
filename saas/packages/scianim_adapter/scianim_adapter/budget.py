"""AIBudgetGuard: control de gasto de la API comercial, persistente y a prueba de fallos (fail-closed).

- Estado en SQLite (modo WAL) y escrituras con BEGIN IMMEDIATE: las reservas son atomicas entre hilos Y procesos.
- Todo en micro-USD enteros (1 token a 1 USD/MTok = 1 micro-USD): sin errores de coma flotante.
- reserve(): coste MAXIMO posible de la solicitud (tokens de entrada estimados con margen + max_tokens de salida).
  Se rechaza si gasto_conciliado + reservas_vivas + este maximo > presupuesto, o si supera el tope por solicitud.
- settle(): concilia con el uso real que informa la API. Si el real supera lo reservado se registra igual (overrun).
- release(): solo cuando se SABE que no hubo cargo (p. ej. 4xx de validacion antes de ejecutar).
- mark_unknown(): resultado incierto (timeout/red tras enviar): la reserva completa se mantiene hasta reconcile().
- Cualquier error del propio control (BD ilegible, bloqueada, esquema roto) => BudgetGuardError => NO se llama a la API.
- El presupuesto acumulado NO se reinicia al reiniciar el proceso. Para cambiarlo hay que editar la configuracion.
"""
from __future__ import annotations

import math
import sqlite3
import time
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .providers import BudgetExceeded, ProviderError


class BudgetGuardError(ProviderError):
    """El control financiero no esta disponible o es inconsistente: bloqueo por defecto."""


def usd_to_micro(x) -> int:
    return int((Decimal(str(x)) * 1_000_000).to_integral_value(rounding="ROUND_CEILING"))


def micro_to_usd(m: int) -> float:
    return m / 1_000_000


def token_cost_micro(tokens: int, price_per_mtok) -> int:
    # USD/MTok * tokens / 1e6 USD = tokens * price micro-USD
    return int(math.ceil(Decimal(tokens) * Decimal(str(price_per_mtok))))


@dataclass
class Reservation:
    request_id: str
    reserved_micro: int
    est_input_tokens: int
    max_output_tokens: int


_SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger(
  request_id TEXT PRIMARY KEY,
  state TEXT NOT NULL CHECK(state IN ('reserved','settled','released','unknown')),
  model TEXT NOT NULL,
  reserved_micro INTEGER NOT NULL CHECK(reserved_micro >= 0),
  actual_micro INTEGER,
  input_tokens INTEGER, output_tokens INTEGER,
  note TEXT,
  created REAL NOT NULL, updated REAL NOT NULL);
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT NOT NULL);
"""


class AIBudgetGuard:
    def __init__(self, db_path, *, budget_usd, price_in_per_mtok, price_out_per_mtok,
                 max_request_usd=None, input_safety=1.25, chars_per_token=3.0, busy_timeout_s=10.0,
                 journal_mode="WAL"):
        if budget_usd is None or price_in_per_mtok is None or price_out_per_mtok is None:
            raise BudgetGuardError("budget_usd y los dos precios son obligatorios (fail-closed)")
        if float(budget_usd) <= 0:
            raise BudgetGuardError("budget_usd debe ser > 0")
        self.path = Path(db_path)
        self.budget = usd_to_micro(budget_usd)
        self.p_in, self.p_out = price_in_per_mtok, price_out_per_mtok
        self.max_request = usd_to_micro(max_request_usd) if max_request_usd is not None else self.budget
        self.input_safety, self.cpt, self.busy = input_safety, chars_per_token, busy_timeout_s
        self.journal = str(journal_mode).upper()
        if self.journal not in ("WAL", "TRUNCATE", "PERSIST"):
            # DELETE/OFF/MEMORY quedan excluidos: borran el diario o no protegen ante cortes de energia
            raise BudgetGuardError("journal_mode debe ser WAL, TRUNCATE o PERSIST")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            c = self._conn()
            try:
                c.executescript(_SCHEMA)
                c.commit()
            finally:
                c.close()
            self._check_integrity()
        except BudgetGuardError:
            raise
        except Exception as e:  # noqa: BLE001
            raise BudgetGuardError(f"no se pudo abrir el libro de presupuesto: {e}") from e

    # ---- infraestructura
    def _conn(self):
        c = sqlite3.connect(self.path, timeout=self.busy, isolation_level=None)
        mode = c.execute(f"PRAGMA journal_mode={self.journal}").fetchone()[0]
        if str(mode).upper() != self.journal:
            c.close()
            raise BudgetGuardError(f"el sistema de archivos no admite journal_mode={self.journal} (obtenido {mode})")
        c.execute("PRAGMA synchronous=FULL")
        c.row_factory = sqlite3.Row
        return c

    def _tx(self):
        guard = self

        class _T:
            def __enter__(s):
                s.c = guard._conn()
                s.c.execute("BEGIN IMMEDIATE")
                return s.c

            def __exit__(s, et, ev, tb):
                try:
                    s.c.execute("ROLLBACK" if et else "COMMIT")
                finally:
                    s.c.close()
                return False
        return _T()

    def _check_integrity(self):
        c = self._conn()
        try:
            if c.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise BudgetGuardError("libro de presupuesto corrupto")
        finally:
            c.close()

    # ---- estimacion
    def estimate_input_tokens(self, text_chars: int) -> int:
        return int(math.ceil(text_chars / self.cpt * self.input_safety))

    def max_cost_micro(self, est_input_tokens: int, max_output_tokens: int) -> int:
        return token_cost_micro(est_input_tokens, self.p_in) + token_cost_micro(max_output_tokens, self.p_out)

    # ---- operaciones
    def _spent_and_held(self, c):
        r = c.execute("""SELECT
            COALESCE(SUM(CASE WHEN state='settled' THEN actual_micro END),0) AS spent,
            COALESCE(SUM(CASE WHEN state IN ('reserved','unknown') THEN reserved_micro END),0) AS held
            FROM ledger""").fetchone()
        return int(r["spent"]), int(r["held"])

    def reserve(self, request_id: str, model: str, est_input_tokens: int, max_output_tokens: int) -> Reservation:
        try:
            need = self.max_cost_micro(est_input_tokens, max_output_tokens)
            if need > self.max_request:
                raise BudgetExceeded(f"coste maximo de la solicitud {micro_to_usd(need):.4f} USD supera el tope "
                                     f"por solicitud {micro_to_usd(self.max_request):.4f} USD")
            with self._tx() as c:
                spent, held = self._spent_and_held(c)
                if spent + held + need > self.budget:
                    raise BudgetExceeded(
                        f"presupuesto insuficiente: gastado {micro_to_usd(spent):.4f} + reservado {micro_to_usd(held):.4f} "
                        f"+ maximo de esta solicitud {micro_to_usd(need):.4f} > {micro_to_usd(self.budget):.4f} USD")
                now = time.time()
                c.execute("INSERT INTO ledger(request_id,state,model,reserved_micro,created,updated) VALUES(?,?,?,?,?,?)",
                          (request_id, "reserved", model, need, now, now))
            return Reservation(request_id, need, est_input_tokens, max_output_tokens)
        except BudgetExceeded:
            raise
        except Exception as e:  # noqa: BLE001 - fail-closed
            raise BudgetGuardError(f"control de presupuesto no disponible: {e}") from e

    def _finish(self, request_id, from_states, state, **cols):
        try:
            with self._tx() as c:
                row = c.execute("SELECT state FROM ledger WHERE request_id=?", (request_id,)).fetchone()
                if row is None or row["state"] not in from_states:
                    raise BudgetGuardError(f"transicion invalida para {request_id}: {row['state'] if row else 'inexistente'} -> {state}")
                sets = ", ".join(f"{k}=?" for k in cols)
                c.execute(f"UPDATE ledger SET state=?, updated=?{', ' + sets if sets else ''} WHERE request_id=?",
                          (state, time.time(), *cols.values(), request_id))
        except BudgetGuardError:
            raise
        except Exception as e:  # noqa: BLE001
            raise BudgetGuardError(f"no se pudo registrar {state}: {e}") from e

    def settle(self, request_id: str, input_tokens: int, output_tokens: int, *, cache_write_tokens=0,
               cache_read_tokens=0) -> int:
        """Concilia con el uso real. Los tokens de cache se cobran como entrada (cota superior prudente)."""
        total_in = int(input_tokens) + int(cache_write_tokens) + int(cache_read_tokens)
        actual = token_cost_micro(total_in, self.p_in) + token_cost_micro(int(output_tokens), self.p_out)
        self._finish(request_id, ("reserved", "unknown"), "settled", actual_micro=actual,
                     input_tokens=total_in, output_tokens=int(output_tokens))
        return actual

    def release(self, request_id: str, note: str = "") -> None:
        self._finish(request_id, ("reserved",), "released", actual_micro=0, note=note)

    def mark_unknown(self, request_id: str, note: str = "") -> None:
        self._finish(request_id, ("reserved",), "unknown", note=note)

    def reconcile(self, request_id: str, actual_usd) -> None:
        """Conciliacion manual de una solicitud incierta con el gasto visto en la consola de Anthropic."""
        self._finish(request_id, ("unknown",), "settled", actual_micro=usd_to_micro(actual_usd))

    def status(self) -> dict:
        try:
            c = self._conn()
            try:
                spent, held = self._spent_and_held(c)
                n = c.execute("SELECT COUNT(*) FROM ledger").fetchone()[0]
            finally:
                c.close()
        except Exception as e:  # noqa: BLE001
            raise BudgetGuardError(f"no se pudo leer el libro: {e}") from e
        return {"budget_usd": micro_to_usd(self.budget), "spent_usd": micro_to_usd(spent), "held_usd": micro_to_usd(held),
                "remaining_usd": micro_to_usd(self.budget - spent - held), "requests": n}
