"""Reserva, liquidación, cancelación y estados: PostgreSQL real, múltiples conexiones concurrentes."""
import threading
from concurrent.futures import ThreadPoolExecutor

import psycopg
import pytest

from app import lifecycle
from tests.helpers import (assert_job_accounting, available, held, job, ledger_for, new_estimate, new_user,
                           queue_job)


def err(exc: Exception) -> str:
    return getattr(getattr(exc, "diag", None), "message_primary", None) or str(exc)


# ------------------------------------------------------------------ reserva
def test_audit_scenario_settle_cannot_make_balance_negative(pool):
    """Escenario del auditor: saldo 100; A reserva 40, B reserva 60; A 'liquida 50' => antes -10."""
    u = new_user(pool, 100)
    a, b = queue_job(pool, u, 40), queue_job(pool, u, 60)
    assert available(pool, u) == 0
    lifecycle.mark_running(pool, a)
    charged = lifecycle.complete_job(pool, a, 50)           # real 50 > reservado 40
    assert charged == 40 and available(pool, u) == 0       # tope = reserva; sin saldo negativo
    assert_job_accounting(pool, a)


def test_reserve_is_max_authorized_and_settle_only_releases(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    assert [r["entry_type"] for r in ledger_for(pool, j)] == ["reserve"]
    lifecycle.mark_running(pool, j)
    assert lifecycle.complete_job(pool, j, 25) == 25
    assert [(r["entry_type"], r["delta"]) for r in ledger_for(pool, j)] == [("reserve", -40), ("release", 15)]
    assert available(pool, u) == 75 and held(pool, u) == 0
    assert all(r["entry_type"] != "consume" for r in ledger_for(pool, j))


def test_concurrent_jobs_same_balance_no_overspend(pool):
    u = new_user(pool, 100)
    eids = [new_estimate(pool, u, 40) for _ in range(10)]
    barrier = threading.Barrier(10)

    def go(eid):
        barrier.wait()
        try:
            with pool.connection() as c:
                return c.execute("SELECT create_queued_job(%s,%s,%s,40,'t',1000) AS id",
                                 (u, eid, "e" * 64)).fetchone()["id"]
        except psycopg.errors.RaiseException as e:
            return err(e)
    with ThreadPoolExecutor(10) as ex:
        out = list(ex.map(go, eids))
    ok = [o for o in out if not isinstance(o, str)]
    assert len(ok) == 2 and out.count("insufficient_credits") == 8
    assert available(pool, u) == 20 and held(pool, u) == 80
    with pool.connection() as c:
        assert c.execute("SELECT count(*) AS n FROM credit_ledger WHERE entry_type='reserve'").fetchone()["n"] == 2
        assert c.execute("SELECT count(*) AS n FROM jobs WHERE status<>'queued'").fetchone()["n"] == 0  # sin drafts huérfanos


def test_same_estimate_concurrently_creates_exactly_one_job(pool):
    u = new_user(pool, 1000)
    eid = new_estimate(pool, u, 40)
    barrier = threading.Barrier(8)

    def go(_):
        barrier.wait()
        try:
            with pool.connection() as c:
                return c.execute("SELECT create_queued_job(%s,%s,%s,40,'t') AS id", (u, eid, "e" * 64)).fetchone()["id"]
        except (psycopg.errors.RaiseException, psycopg.errors.UniqueViolation) as e:
            return err(e)
    with ThreadPoolExecutor(8) as ex:
        out = list(ex.map(go, range(8)))
    assert len([o for o in out if not isinstance(o, str)]) == 1
    assert available(pool, u) == 960


def test_concurrent_settle_is_idempotent(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    lifecycle.mark_running(pool, j)
    barrier = threading.Barrier(10)

    def go(_):
        barrier.wait()
        return lifecycle.complete_job(pool, j, 10)
    with ThreadPoolExecutor(10) as ex:
        assert set(ex.map(go, range(10))) == {10}
    assert available(pool, u) == 90
    assert [r["entry_type"] for r in ledger_for(pool, j)] == ["reserve", "release"]


def test_no_deadlock_under_mixed_reserve_settle_cancel_stress(pool):
    """Orden de bloqueo job->usuario en todas las rutas. 30 hilos mezclan crear/completar/cancelar."""
    u = new_user(pool, 400)
    running = [queue_job(pool, u, 10) for _ in range(12)]
    for r in running[:8]:
        lifecycle.mark_running(pool, r)
    pending_est = [new_estimate(pool, u, 10) for _ in range(10)]
    errors: list[str] = []
    start = threading.Barrier(24)

    def create(eid):
        start.wait()
        try:
            with pool.connection() as c:
                c.execute("SELECT create_queued_job(%s,%s,%s,10,'t') ", (u, eid, "e" * 64))
        except psycopg.errors.RaiseException as e:
            if err(e) != "insufficient_credits":
                errors.append(err(e))

    def complete(jid):
        start.wait()
        try:
            lifecycle.complete_job(pool, jid, 7)
        except Exception as e:
            errors.append(err(e))

    def cancel(jid):
        start.wait()
        try:
            with pool.connection() as c:
                c.execute("SELECT request_cancel(%s,%s)", (jid, u))
        except Exception as e:
            errors.append(err(e))

    with ThreadPoolExecutor(24) as ex:
        fs = [ex.submit(create, e) for e in pending_est]
        fs += [ex.submit(complete, j) for j in running[:8]]
        fs += [ex.submit(cancel, j) for j in running[8:]]          # queued: cancelación inmediata
        fs += [ex.submit(cancel, j) for j in running[:2]]          # carrera cancel vs complete (running)
        for f in fs:
            f.result(timeout=60)                                    # un deadlock revienta aquí
    assert not [e for e in errors if "deadlock" in e.lower()], errors
    assert available(pool, u) >= 0
    for j in running:
        assert_job_accounting(pool, j)


def test_ledger_trigger_blocks_negative_balance(pool):
    u = new_user(pool, 5)
    with pytest.raises(psycopg.errors.RaiseException, match="insufficient_credits"):
        with pool.connection() as c:
            c.execute("INSERT INTO credit_ledger(user_id, entry_type, delta) VALUES (%s,'adjustment',-6)", (u,))
    assert available(pool, u) == 5


def test_ledger_is_append_only(pool):
    u = new_user(pool, 5)
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"):
        with pool.connection() as c:
            c.execute("UPDATE credit_ledger SET delta = 999 WHERE user_id=%s", (u,))
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"):
        with pool.connection() as c:
            c.execute("DELETE FROM credit_ledger WHERE user_id=%s", (u,))


# ------------------------------------------------------------------ holds / settle
def test_holds_exclude_settled_jobs(pool):
    u = new_user(pool, 100)
    a, b = queue_job(pool, u, 30), queue_job(pool, u, 20)
    assert held(pool, u) == 50 and available(pool, u) == 50
    lifecycle.mark_running(pool, a)
    lifecycle.complete_job(pool, a, 30)                     # consumido por completo: ya no es 'retenido'
    assert held(pool, u) == 20 and available(pool, u) == 50
    with pool.connection() as c:                            # total = available + held, sin doble descuento
        assert c.execute("SELECT COALESCE(SUM(delta),0)::int AS v FROM credit_ledger WHERE user_id=%s",
                         (u,)).fetchone()["v"] + held(pool, u) == 70


def test_platform_failure_refunds_everything_non_platform_charges_consumed(pool):
    u = new_user(pool, 100)
    a, b = queue_job(pool, u, 40), queue_job(pool, u, 40)
    lifecycle.mark_running(pool, a)
    lifecycle.mark_running(pool, b)
    assert lifecycle.fail_job(pool, a, "worker_crash", "boom", platform_fault=True, consumed=33) == 0
    assert lifecycle.fail_job(pool, b, "bad_pdf", "ilegible", platform_fault=False, consumed=12) == 12
    assert available(pool, u) == 100 - 12
    # idempotente
    assert lifecycle.fail_job(pool, a, "worker_crash", "boom", platform_fault=True, consumed=33) == 0
    assert available(pool, u) == 88
    for j in (a, b):
        assert_job_accounting(pool, j)


def test_invalid_transitions_rejected(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 10)
    with pytest.raises(psycopg.errors.RaiseException, match="invalid_transition"):
        lifecycle.complete_job(pool, j, 5)                  # queued -> succeeded no existe
    lifecycle.mark_running(pool, j)
    lifecycle.complete_job(pool, j, 5)
    with pytest.raises(psycopg.errors.RaiseException, match="invalid_transition"):
        with pool.connection() as c:
            c.execute("UPDATE jobs SET status='running' WHERE id=%s", (j,))
    with pytest.raises(psycopg.errors.RaiseException, match="invalid_transition"):
        lifecycle.fail_job(pool, j, "x", "y", platform_fault=True)
    assert lifecycle.mark_running(pool, j) == "terminal"


def test_terminal_job_without_settlement_cannot_commit(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 10)
    lifecycle.mark_running(pool, j)
    with pytest.raises(psycopg.errors.RaiseException, match="not settled"):
        with pool.connection() as c:
            c.execute("UPDATE jobs SET status='succeeded', finished_at=now() WHERE id=%s", (j,))


def test_ownership_enforced_by_composite_foreign_keys(pool):
    a, b = new_user(pool, 100), new_user(pool, 100)
    eid_a = new_estimate(pool, a, 10)
    # b intenta crear un job con la estimación de a
    with pytest.raises(psycopg.errors.RaiseException, match="estimate_not_found"):
        with pool.connection() as c:
            c.execute("SELECT create_queued_job(%s,%s,%s,10,'t')", (b, eid_a, "e" * 64))
    # y sin pasar por la función: la FK compuesta lo impide
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with pool.connection() as c:
            pdf_a = c.execute("SELECT pdf_file_id FROM job_estimates WHERE id=%s", (eid_a,)).fetchone()["pdf_file_id"]
            c.execute("INSERT INTO jobs(user_id, pdf_file_id, kind, pipeline_version) VALUES (%s,%s,'solution_video','t')",
                      (b, pdf_a))


def test_solution_video_cannot_have_prologue(pool):
    u = new_user(pool, 10)
    with pytest.raises(psycopg.errors.CheckViolation):
        with pool.connection() as c:
            pdf = c.execute("INSERT INTO pdf_files(user_id,original_name,storage_key,size_bytes,declared_sha256) "
                            "VALUES (%s,'a.pdf','k/x',1,%s) RETURNING id", (u, "a" * 64)).fetchone()["id"]
            c.execute("INSERT INTO jobs(user_id,pdf_file_id,kind,pipeline_version,include_prologue) "
                      "VALUES (%s,%s,'solution_video','t',true)", (u, pdf))


# ------------------------------------------------------------------ cancelación
def test_cancel_queued_is_immediate_full_refund_and_idempotent(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    with pool.connection() as c:
        assert c.execute("SELECT request_cancel(%s,%s) AS s", (j, u)).fetchone()["s"] == "cancelled"
        assert c.execute("SELECT request_cancel(%s,%s) AS s", (j, u)).fetchone()["s"] == "cancelled"
    assert available(pool, u) == 100 and held(pool, u) == 0
    assert job(pool, j)["final_credits"] == 0
    assert [r["entry_type"] for r in ledger_for(pool, j)] == ["reserve", "release"]
    assert lifecycle.mark_running(pool, j) == "cancelled"           # el worker que llega tarde se retira
    with pool.connection() as c:
        assert c.execute("SELECT status FROM outbox WHERE job_id=%s", (j,)).fetchone()["status"] == "cancelled"


def test_cancel_running_is_cooperative_no_early_release(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    lifecycle.mark_running(pool, j)
    with pool.connection() as c:
        assert c.execute("SELECT request_cancel(%s,%s) AS s", (j, u)).fetchone()["s"] == "cancelling"
    assert available(pool, u) == 60 and held(pool, u) == 40        # NADA liberado mientras siga procesando
    assert job(pool, j)["status"] == "running"
    assert lifecycle.confirm_cancel(pool, j, 15) == 15              # el worker confirma que se detuvo
    assert job(pool, j)["status"] == "cancelled" and available(pool, u) == 85 and held(pool, u) == 0
    assert lifecycle.confirm_cancel(pool, j, 15) == 15              # idempotente
    assert available(pool, u) == 85
    assert_job_accounting(pool, j)


def test_confirm_cancel_requires_request_and_caps_to_reserve(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    lifecycle.mark_running(pool, j)
    with pytest.raises(psycopg.errors.RaiseException, match="cancel_not_requested"):
        lifecycle.confirm_cancel(pool, j, 1)
    with pool.connection() as c:
        c.execute("SELECT request_cancel(%s,%s)", (j, u))
    assert lifecycle.confirm_cancel(pool, j, 999) == 40             # tope = reserva
    assert available(pool, u) == 60


def test_cancel_finished_job_is_rejected(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 10)
    lifecycle.mark_running(pool, j)
    lifecycle.complete_job(pool, j, 10)
    with pytest.raises(psycopg.errors.RaiseException, match="job_not_cancellable"):
        with pool.connection() as c:
            c.execute("SELECT request_cancel(%s,%s)", (j, u))


def test_cancel_vs_worker_start_race_is_always_consistent(pool):
    for _ in range(20):
        u = new_user(pool, 100)
        j = queue_job(pool, u, 40)
        barrier = threading.Barrier(2)

        def cancel():
            barrier.wait()
            with pool.connection() as c:
                return c.execute("SELECT request_cancel(%s,%s) AS s", (j, u)).fetchone()["s"]

        def start():
            barrier.wait()
            return lifecycle.mark_running(pool, j)
        with ThreadPoolExecutor(2) as ex:
            f1, f2 = ex.submit(cancel), ex.submit(start)
            c_res, s_res = f1.result(timeout=30), f2.result(timeout=30)
        jb = job(pool, j)
        if c_res == "cancelled":                      # cancel ganó: el worker no arranca, reembolso total
            assert s_res == "cancelled" and jb["status"] == "cancelled" and available(pool, u) == 100
        else:                                         # worker ganó: cancelación cooperativa pendiente
            assert (c_res, s_res) == ("cancelling", "started") and jb["status"] == "running"
            assert available(pool, u) == 60
            lifecycle.confirm_cancel(pool, j, 0)
            assert available(pool, u) == 100
        assert_job_accounting(pool, j)


def test_api_cancel_endpoint_idempotent_and_refunds(alice, make_job, client):
    alice.grant(200)
    job_, est = make_job(alice)
    h = alice.h(**{"Idempotency-Key": "cancel-key-1"})
    r1 = client.post(f"/v1/jobs/{job_['id']}/cancel", headers=h)
    r2 = client.post(f"/v1/jobs/{job_['id']}/cancel", headers=h)
    assert r1.status_code == r2.status_code == 200 and r1.json()["status"] == "cancelled"
    assert r2.headers["Idempotent-Replayed"] == "true"
    r3 = client.post(f"/v1/jobs/{job_['id']}/cancel", headers=alice.h(**{"Idempotency-Key": "cancel-key-2"}))
    assert r3.status_code == 200                                    # otra clave: igualmente idempotente
    assert alice.balance() == {"available": 200, "held": 0, "total": 200}
    assert client.post(f"/v1/jobs/{job_['id']}/cancel", headers=alice.headers).status_code == 422  # sin clave


def test_api_cancel_running_then_worker_confirms(alice, make_job, client, pool):
    alice.grant(200)
    job_, est = make_job(alice)
    lifecycle.mark_running(pool, job_["id"])
    r = client.post(f"/v1/jobs/{job_['id']}/cancel", headers=alice.h(**{"Idempotency-Key": "cancel-run-1"}))
    assert r.status_code == 200 and r.json()["status"] == "running" and r.json()["cancel_requested"] is True
    assert alice.balance()["held"] == est["max_credits"]
    lifecycle.confirm_cancel(pool, job_["id"], 5)
    j = client.get(f"/v1/jobs/{job_['id']}", headers=alice.headers).json()
    assert j["status"] == "cancelled" and j["final_credits"] == 5
    assert alice.balance() == {"available": 195, "held": 0, "total": 195}


def test_api_cancel_finished_is_409(alice, make_job, client, pool):
    alice.grant(200)
    job_, _ = make_job(alice)
    lifecycle.mark_running(pool, job_["id"])
    lifecycle.complete_job(pool, job_["id"], 3)
    r = client.post(f"/v1/jobs/{job_['id']}/cancel", headers=alice.h(**{"Idempotency-Key": "cancel-done-1"}))
    assert r.status_code == 409 and r.json()["code"] == "job_not_cancellable"


# ------------------------------------------------------------------ concurrencia vía API
def test_api_concurrent_same_idempotency_key_creates_one_job(alice, pdf_for, estimate_for, client, pool):
    from tests.conftest import create_job
    alice.grant(500)
    est = estimate_for(alice, pdf_for(alice))
    barrier = threading.Barrier(8)

    def go(_):
        barrier.wait()
        r = create_job(alice, est, key="same-key-12345")
        return r.status_code, r.json().get("id")
    with ThreadPoolExecutor(8) as ex:
        out = list(ex.map(go, range(8)))
    assert {s for s, _ in out} == {201} and len({i for _, i in out}) == 1
    with pool.connection() as c:
        assert c.execute("SELECT count(*) AS n FROM credit_ledger WHERE entry_type='reserve'").fetchone()["n"] == 1
    assert alice.balance()["held"] == est["max_credits"]


def test_api_concurrent_creates_never_overspend(bob, pdf_for, estimate_for, client, pool):
    from tests.conftest import create_job
    bob.set_plan("pro")
    with pool.connection() as c:                                     # el límite de concurrencia no debe ser el vinculante
        c.execute("UPDATE plans SET max_concurrent_jobs = 10 WHERE code='pro'")
    pid = pdf_for(bob)
    ests = [estimate_for(bob, pid) for _ in range(6)]
    cost = ests[0]["max_credits"]
    bob.grant(cost * 3 + cost // 2)                                  # alcanza para 3
    barrier = threading.Barrier(6)

    def go(e):
        barrier.wait()
        return create_job(bob, e).status_code
    with ThreadPoolExecutor(6) as ex:
        codes = list(ex.map(go, ests))
    assert sorted(codes) == [201] * 3 + [402] * 3
    b = bob.balance()
    assert b["available"] == cost // 2 and b["held"] == cost * 3


def test_api_concurrency_limit_race_never_exceeds_plan(bob, pdf_for, estimate_for, client):
    """El límite de jobs simultáneos del plan (pro=3) se respeta aunque lleguen 6 peticiones a la vez."""
    from tests.conftest import create_job
    bob.set_plan("pro")
    pid = pdf_for(bob)
    ests = [estimate_for(bob, pid) for _ in range(6)]
    bob.grant(10_000)
    barrier = threading.Barrier(6)

    def go(e):
        barrier.wait()
        return create_job(bob, e).status_code
    with ThreadPoolExecutor(6) as ex:
        codes = list(ex.map(go, ests))
    assert sorted(codes) == [201] * 3 + [409] * 3
