"""API interna para los workers (NO expuesta por HTTP). Cada llamada es una transacción atómica."""
from __future__ import annotations


def mark_running(pool, job_id) -> str:
    with pool.connection() as c:
        return c.execute("SELECT mark_running(%s) AS r", (job_id,)).fetchone()["r"]


def complete_job(pool, job_id, actual_credits: int) -> int:
    with pool.connection() as c:
        return c.execute("SELECT complete_job(%s,%s) AS r", (job_id, actual_credits)).fetchone()["r"]


def fail_job(pool, job_id, code: str, message: str, *, platform_fault: bool, consumed: int = 0) -> int:
    with pool.connection() as c:
        return c.execute("SELECT fail_job(%s,%s,%s,%s,%s) AS r",
                         (job_id, code, message, platform_fault, consumed)).fetchone()["r"]


def confirm_cancel(pool, job_id, consumed: int) -> int:
    with pool.connection() as c:
        return c.execute("SELECT confirm_cancel(%s,%s) AS r", (job_id, consumed)).fetchone()["r"]
