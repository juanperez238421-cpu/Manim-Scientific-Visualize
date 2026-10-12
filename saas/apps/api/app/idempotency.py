"""Idempotency-Key + hash canónico del request. Todo ocurre en la MISMA transacción que la operación:
si la operación falla (402, 409...) se hace rollback también de la clave, y un reintento la re-evalúa."""
from __future__ import annotations

from typing import Any, Callable

from psycopg.types.json import Jsonb

from .errors import ApiError
from .pricing import sha256_hex


def request_hash(body: Any, **path_params: str) -> str:
    return sha256_hex({"body": body, "path": path_params})


def run_idempotent(conn, user_id: str, scope: str, key: str, req_hash: str,
                   op: Callable[[], tuple[int, dict]]) -> tuple[int, dict, bool]:
    row = conn.execute(
        """INSERT INTO idempotency_keys(user_id, scope, key, request_hash) VALUES (%s,%s,%s,%s)
           ON CONFLICT (user_id, scope, key) DO NOTHING RETURNING id""",
        (user_id, scope, key, req_hash)).fetchone()
    if row is not None:                       # primera vez (o la transacción previa hizo rollback)
        status, body = op()
        conn.execute("UPDATE idempotency_keys SET response_status=%s, response_body=%s WHERE id=%s",
                     (status, Jsonb(body), row["id"]))
        return status, body, False
    ex = conn.execute(
        "SELECT request_hash, response_status, response_body FROM idempotency_keys "
        "WHERE user_id=%s AND scope=%s AND key=%s", (user_id, scope, key)).fetchone()
    if ex["request_hash"] != req_hash:
        raise ApiError(409, "idempotency_conflict", "La Idempotency-Key ya se usó con otro cuerpo.")
    return ex["response_status"], ex["response_body"], True
