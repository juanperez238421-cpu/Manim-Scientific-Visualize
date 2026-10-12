from __future__ import annotations

from .jobs import decode_cursor, encode_cursor


def balance(conn, user_id) -> dict:
    a = conn.execute("SELECT COALESCE(SUM(delta),0)::int AS v FROM credit_ledger WHERE user_id=%s",
                     (user_id,)).fetchone()["v"]
    h = conn.execute("SELECT held FROM credit_holds WHERE user_id=%s", (user_id,)).fetchone()
    held = h["held"] if h else 0
    return {"available": a, "held": held, "total": a + held}


def ledger(conn, user_id, limit: int, cursor: str | None) -> dict:
    params = [user_id]
    where = ""
    if cursor:
        (last,) = decode_cursor(cursor, 1)
        where, params = "AND id < %s", [user_id, int(last)]
    rows = conn.execute(
        f"SELECT id, entry_type, delta, job_id, reason, created_at FROM credit_ledger WHERE user_id=%s {where} "
        "ORDER BY id DESC LIMIT %s", params + [limit + 1]).fetchall()
    page, more = rows[:limit], len(rows) > limit
    return {"items": page, "next_cursor": encode_cursor(page[-1]["id"]) if more else None}
