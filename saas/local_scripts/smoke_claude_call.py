"""Prueba minima y reproducible de Claude API a traves del AIBudgetGuard. No imprime credenciales.

1) Carga .env; 2) valida limites (presupuesto acumulado y tope por solicitud);
3) comprueba que el modelo existe (GET /v1/models/{id}); 4) UNA llamada de ~20 tokens de salida,
solo si el coste maximo estimado cabe; 5) concilia y muestra tokens, coste, HTTP y presupuesto restante.
Uso:  python scripts/smoke_claude_call.py [--dry-run]
"""
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "packages" / "scianim_adapter"))

from api.app.config import get_settings, key_is_configured  # noqa: E402
from scianim_adapter import AIBudgetGuard, BudgetExceeded  # noqa: E402

dry = "--dry-run" in sys.argv
s = get_settings()
print("clave configurada:", key_is_configured(), "| modelo:", s.model)
assert key_is_configured(), "ANTHROPIC_API_KEY ausente o placeholder"
guard = AIBudgetGuard(s.storage / "budget.sqlite3", budget_usd=s.budget_usd, price_in_per_mtok=s.price_in,
                      price_out_per_mtok=s.price_out, max_request_usd=s.max_request_usd, journal_mode=s.budget_journal)
st = guard.status()
print(f"presupuesto acumulado: {st['budget_usd']:.2f} USD | tope por solicitud: {s.max_request_usd} USD | "
      f"gastado {st['spent_usd']:.6f} | reservado {st['held_usd']:.6f} | restante {st['remaining_usd']:.6f}")

PROMPT = "Responde exactamente con la palabra: OK"
MAX_OUT = 20
est_in = guard.estimate_input_tokens(len(PROMPT))
maxc = guard.max_cost_micro(est_in, MAX_OUT) / 1e6
print(f"coste maximo estimado de la llamada: {maxc:.6f} USD (entrada~{est_in} tok, salida<= {MAX_OUT} tok)")
assert maxc <= 0.25, "coste maximo estimado supera 0.25 USD"
if dry:
    print("dry-run: no se llama a la API"); sys.exit(0)

import anthropic  # noqa: E402

client = anthropic.Anthropic(max_retries=0, timeout=60)   # lee ANTHROPIC_API_KEY del entorno
try:
    m = client.models.with_raw_response.retrieve(s.model)
    print("modelo disponible: HTTP", m.status_code, "| id:", m.parse().id)
except anthropic.APIStatusError as e:
    ct = e.response.headers.get("content-type", "") if getattr(e, "response", None) is not None else ""
    if e.status_code == 401 and "json" not in ct.lower():
        # Anthropic siempre responde JSON ({"type":"error",...}); un 401 text/plain lo genera un intermediario.
        print("HTTP 401 text/plain: NO proviene de Anthropic sino de un proxy/pasarela de salida que intercepta "
              "x-api-key. Ejecuta este script desde Windows nativo (sin proxy corporativo).")
    else:
        print("modelo NO disponible: HTTP", e.status_code)
    sys.exit(2)

rid = uuid.uuid4().hex
try:
    guard.reserve(rid, s.model, est_in, MAX_OUT)
except BudgetExceeded as e:
    print("bloqueado por presupuesto:", e); sys.exit(3)
try:
    raw = client.messages.with_raw_response.create(model=s.model, max_tokens=MAX_OUT,
                                                   messages=[{"role": "user", "content": PROMPT}])
except anthropic.APIStatusError as e:
    (guard.release if 400 <= e.status_code < 500 and e.status_code not in (408, 409) else guard.mark_unknown)(rid, f"HTTP {e.status_code}")
    print("llamada fallida: HTTP", e.status_code); sys.exit(4)
except Exception as e:  # noqa: BLE001
    guard.mark_unknown(rid, type(e).__name__)
    print("llamada incierta (reserva mantenida):", type(e).__name__); sys.exit(5)
msg = raw.parse()
u = msg.usage
actual = guard.settle(rid, u.input_tokens, u.output_tokens,
                      cache_write_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
                      cache_read_tokens=getattr(u, "cache_read_input_tokens", 0) or 0) / 1e6
st = guard.status()
print("HTTP:", raw.status_code, "| request-id:", raw.headers.get("request-id"))
print("respuesta:", "".join(b.text for b in msg.content if b.type == "text").strip()[:60])
print(f"tokens entrada={u.input_tokens} salida={u.output_tokens} | coste real={actual:.6f} USD")
print(f"presupuesto: gastado {st['spent_usd']:.6f} | restante {st['remaining_usd']:.6f} de {st['budget_usd']:.2f} USD")
