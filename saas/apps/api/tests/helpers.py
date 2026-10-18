"""Helpers a nivel SQL para tests financieros (sin pasar por HTTP)."""
from __future__ import annotations

import uuid

from psycopg.types.json import Jsonb


def new_user(pool, balance=0):
    with pool.connection() as c:
        uid = c.execute("INSERT INTO users(email, provider_subject) VALUES (%s,%s) RETURNING id",
                        (f"{uuid.uuid4()}@t.co", f"sub_{uuid.uuid4()}")).fetchone()["id"]
        if balance:
            c.execute("INSERT INTO credit_ledger(user_id, entry_type, delta) VALUES (%s,'grant',%s)", (uid, balance))
    return uid


def new_estimate(pool, uid, credits=40, max_credits=None, kind="solution_video", pdf_id=None):
    with pool.connection() as c:
        if pdf_id is None:
            pdf_id = c.execute(
                """INSERT INTO pdf_files(user_id, original_name, storage_key, size_bytes, declared_sha256, sha256,
                   status, page_count) VALUES (%s,'a.pdf',%s,10,%s,%s,'analyzed',1) RETURNING id""",
                (uid, f"k/{uuid.uuid4()}", "a" * 64, "a" * 64)).fetchone()["id"]
        eid = c.execute(
            """INSERT INTO job_estimates(user_id, pdf_file_id, kind, config, estimated_seconds, estimated_credits,
               max_credits, breakdown, pricing_version, config_hash, expires_at)
               VALUES (%s,%s,%s,%s,30,%s,%s,%s,'draft-0.1',%s, now() + interval '1 hour') RETURNING id""",
            (uid, pdf_id, kind, Jsonb({"include_prologue": False}), credits, max_credits or credits, Jsonb({}),
             "e" * 64)).fetchone()["id"]
    return eid


def queue_job(pool, uid, credits=40, concurrent=1000):
    eid = new_estimate(pool, uid, credits)
    with pool.connection() as c:
        return c.execute("SELECT create_queued_job(%s,%s,%s,%s,'t',%s) AS id",
                         (uid, eid, "e" * 64, credits, concurrent)).fetchone()["id"]


def available(pool, uid):
    with pool.connection() as c:
        return c.execute("SELECT COALESCE(SUM(delta),0)::int AS v FROM credit_ledger WHERE user_id=%s",
                         (uid,)).fetchone()["v"]


def held(pool, uid):
    with pool.connection() as c:
        r = c.execute("SELECT held FROM credit_holds WHERE user_id=%s", (uid,)).fetchone()
        return r["held"] if r else 0


def job(pool, jid):
    with pool.connection() as c:
        return c.execute("SELECT * FROM jobs WHERE id=%s", (jid,)).fetchone()


def ledger_for(pool, jid):
    with pool.connection() as c:
        return c.execute("SELECT entry_type, delta FROM credit_ledger WHERE job_id=%s ORDER BY id", (jid,)).fetchall()


def assert_job_accounting(pool, jid):
    """Invariante: neto del ledger del job == -final_credits cuando está liquidado."""
    j = job(pool, jid)
    net = sum(r["delta"] for r in ledger_for(pool, jid))
    if j["final_credits"] is not None:
        assert net == -j["final_credits"], (net, j["final_credits"])
    else:
        assert net == -j["reserved_credits"]
