import multiprocessing as mp
import sqlite3
import threading
from types import SimpleNamespace

import pytest

from scianim_adapter import AIBudgetGuard, AnthropicProvider, BudgetExceeded, BudgetGuardError


def G(path, budget=1.0, **kw):
    return AIBudgetGuard(path, budget_usd=budget, price_in_per_mtok=2.0, price_out_per_mtok=10.0, **kw)


def test_max_cost_uses_official_prices(tmp_path):
    g = G(tmp_path / "b.db")
    # 10.000 tok entrada a 2 USD/MTok = 0.02 ; 8.000 salida a 10 USD/MTok = 0.08
    assert g.max_cost_micro(10_000, 8_000) == 20_000 + 80_000


def test_reserve_settle_and_status(tmp_path):
    g = G(tmp_path / "b.db")
    r = g.reserve("a", "m", 10_000, 8_000)
    assert r.reserved_micro == 100_000
    assert g.status()["held_usd"] == pytest.approx(0.10)
    actual = g.settle("a", 4_000, 1_000)           # 0.008 + 0.010
    assert actual == 18_000
    s = g.status()
    assert s["spent_usd"] == pytest.approx(0.018) and s["held_usd"] == 0


def test_rejects_when_max_does_not_fit_and_leaves_no_trace(tmp_path):
    g = G(tmp_path / "b.db", budget=0.05)
    with pytest.raises(BudgetExceeded):
        g.reserve("a", "m", 10_000, 8_000)         # max 0.10 > 0.05
    assert g.status()["requests"] == 0


def test_per_request_cap(tmp_path):
    g = G(tmp_path / "b.db", max_request_usd=0.05)
    with pytest.raises(BudgetExceeded, match="tope"):
        g.reserve("a", "m", 10_000, 8_000)


def test_persists_across_restart(tmp_path):
    p = tmp_path / "b.db"
    g1 = G(p); g1.reserve("a", "m", 1000, 1000); g1.settle("a", 1000, 1000)
    g1.reserve("held", "m", 1000, 1000)
    g2 = G(p)                                       # "reinicio" de FastAPI
    s = g2.status()
    assert s["spent_usd"] == pytest.approx(0.012) and s["held_usd"] == pytest.approx(0.012)


def test_release_frees_budget_and_unknown_keeps_it(tmp_path):
    g = G(tmp_path / "b.db")
    g.reserve("a", "m", 1000, 1000); g.release("a", "400")
    assert g.status()["held_usd"] == 0
    g.reserve("b", "m", 1000, 1000); g.mark_unknown("b", "Timeout")
    assert g.status()["held_usd"] == pytest.approx(0.012)
    g.reconcile("b", 0.003)
    s = g.status()
    assert s["held_usd"] == 0 and s["spent_usd"] == pytest.approx(0.003)


def test_invalid_transitions_are_blocked(tmp_path):
    g = G(tmp_path / "b.db")
    g.reserve("a", "m", 100, 100); g.settle("a", 1, 1)
    with pytest.raises(BudgetGuardError):
        g.settle("a", 1, 1)                         # doble conciliacion
    with pytest.raises(BudgetGuardError):
        g.release("nope")


def test_overrun_is_recorded_not_hidden(tmp_path):
    g = G(tmp_path / "b.db")
    g.reserve("a", "m", 100, 100)                   # reservado 0.0012
    g.settle("a", 10_000, 10_000)                   # real 0.12
    assert g.status()["spent_usd"] == pytest.approx(0.12)


def test_threads_never_exceed_budget(tmp_path):
    g = G(tmp_path / "b.db", budget=1.0)            # cada una max 0.10 -> caben 10
    ok, ko = [], []

    def w(i):
        try:
            g.reserve(f"r{i}", "m", 10_000, 8_000); ok.append(i)
        except BudgetExceeded:
            ko.append(i)
    ts = [threading.Thread(target=w, args=(i,)) for i in range(40)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert len(ok) == 10 and len(ko) == 30 and g.status()["held_usd"] == pytest.approx(1.0)


def _proc(args):
    path, i = args
    try:
        G(path).reserve(f"p{i}", "m", 10_000, 8_000)
        return 1
    except BudgetExceeded:
        return 0


def test_processes_never_exceed_budget(tmp_path):
    p = str(tmp_path / "b.db"); G(p)
    with mp.get_context("spawn").Pool(4) as pool:
        got = sum(pool.map(_proc, [(p, i) for i in range(24)]))
    assert got == 10


def test_fail_closed_when_ledger_unusable(tmp_path):
    p = tmp_path / "b.db"
    g = G(p)
    p.write_bytes(b"esto no es sqlite" * 100)
    for ext in ("-wal", "-shm"):
        (tmp_path / f"b.db{ext}").unlink(missing_ok=True)
    with pytest.raises(BudgetGuardError):
        g.reserve("a", "m", 100, 100)
    with pytest.raises(BudgetGuardError):
        G(p)


def test_requires_budget_and_prices(tmp_path):
    with pytest.raises(BudgetGuardError):
        AIBudgetGuard(tmp_path / "b.db", budget_usd=None, price_in_per_mtok=2, price_out_per_mtok=10)
    with pytest.raises(BudgetGuardError):
        AIBudgetGuard(tmp_path / "b.db", budget_usd=1, price_in_per_mtok=None, price_out_per_mtok=10)


# ---- integracion con el proveedor (cliente simulado: NO es una llamada real)
class FakeClient:
    def __init__(self, text='{"problems": []}', inp=1000, out=500, exc=None):
        self.calls, self.exc = 0, exc
        self.messages = self
        self._r = SimpleNamespace(content=[SimpleNamespace(type="text", text=text)],
                                  usage=SimpleNamespace(input_tokens=inp, output_tokens=out))

    def create(self, **kw):
        self.calls += 1
        if self.exc:
            raise self.exc
        return self._r


def prov(tmp_path, client, guard, **kw):
    pf = tmp_path / "p.md"; pf.write_text("system", encoding="utf-8")
    return AnthropicProvider(model="m", prompt_path=pf, client=client, guard=guard, max_output_tokens=8000,
                             price_in_per_mtok=2.0, price_out_per_mtok=10.0, **kw)


def test_provider_reserves_and_settles(tmp_path):
    g = G(tmp_path / "b.db"); c = FakeClient()
    prov(tmp_path, c, g).author_spec("x" * 3000)
    s = g.status()
    assert c.calls == 1 and s["held_usd"] == 0 and s["spent_usd"] == pytest.approx(0.002 + 0.005)


def test_provider_never_calls_api_when_budget_blocks(tmp_path):
    g = G(tmp_path / "b.db", budget=0.05); c = FakeClient()
    with pytest.raises(BudgetExceeded):
        prov(tmp_path, c, g).author_spec("x" * 3000)
    assert c.calls == 0


def test_provider_never_calls_api_when_guard_broken(tmp_path):
    p = tmp_path / "b.db"; g = G(p); c = FakeClient()
    p.write_bytes(b"garbage" * 200)
    for ext in ("-wal", "-shm"):
        (tmp_path / f"b.db{ext}").unlink(missing_ok=True)
    with pytest.raises(BudgetGuardError):
        prov(tmp_path, c, g).author_spec("x")
    assert c.calls == 0


def test_provider_4xx_releases_and_timeout_holds(tmp_path):
    g = G(tmp_path / "b.db")
    e400 = type("E", (Exception,), {"status_code": 400})()
    with pytest.raises(Exception):
        prov(tmp_path, FakeClient(exc=e400), g).author_spec("x")
    assert g.status()["held_usd"] == 0
    with pytest.raises(TimeoutError):
        prov(tmp_path, FakeClient(exc=TimeoutError()), g).author_spec("x")
    assert g.status()["held_usd"] > 0


@pytest.mark.parametrize("mode", ["TRUNCATE", "PERSIST", "WAL"])
def test_journal_modes_work(tmp_path, mode):
    g = G(tmp_path / "b.db", journal_mode=mode)
    g.reserve("a", "m", 100, 100); g.settle("a", 10, 10)
    assert G(tmp_path / "b.db", journal_mode=mode).status()["requests"] == 1


def test_unsafe_journal_modes_rejected(tmp_path):
    for bad in ("DELETE", "OFF", "MEMORY"):
        with pytest.raises(BudgetGuardError):
            G(tmp_path / "b.db", journal_mode=bad)
