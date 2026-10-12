"""Transactional outbox: la tarea a Celery se escribe en la MISMA transacción que la reserva.
El relay la publica después (at-least-once). Si Redis falla, la fila sigue 'pending' y se reintenta
con backoff. La tarea debe ser idempotente: task_id = job_id y mark_running() descarta duplicados."""
from __future__ import annotations

from typing import Protocol


class Publisher(Protocol):
    def publish(self, topic: str, payload: dict, task_id: str) -> None: ...


def relay_once(pool, publisher: Publisher, batch: int = 50) -> dict[str, int]:
    published = failed = 0
    with pool.connection() as conn:
        rows = conn.execute(
            """SELECT id, job_id, topic, payload, attempts FROM outbox
               WHERE status = 'pending' AND available_at <= now()
               ORDER BY id LIMIT %s FOR UPDATE SKIP LOCKED""", (batch,)).fetchall()
        for r in rows:
            try:
                publisher.publish(r["topic"], r["payload"], task_id=str(r["job_id"]))
            except Exception as exc:
                failed += 1
                conn.execute(
                    """UPDATE outbox SET attempts = attempts + 1, last_error = %s,
                       available_at = now() + make_interval(secs => LEAST(power(2, attempts + 1), 300))
                       WHERE id = %s""", (str(exc)[:500], r["id"]))
            else:
                published += 1
                conn.execute("UPDATE outbox SET status='published', published_at=now(), attempts=attempts+1 "
                             "WHERE id=%s", (r["id"],))
    return {"published": published, "failed": failed}
