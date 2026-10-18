import uuid

import pytest
from psycopg.types.json import Jsonb

from tests.conftest import create_job, make_pdf, upload_pdf


def test_create_job_reserves_max_authorized(alice, make_job):
    alice.grant(200)
    job, est = make_job(alice)
    assert job["status"] == "queued" and job["reserved_credits"] == est["max_credits"]
    assert job["max_authorized_credits"] == est["max_credits"] and job["final_credits"] is None
    b = alice.balance()
    assert b == {"available": 200 - est["max_credits"], "held": est["max_credits"], "total": 200}
    stages = {s["stage"]: s["status"] for s in job["stages"]}
    assert list(stages) == ["extract", "script", "render_manim", "render_prologue", "render_svg", "compose", "upload"]
    assert stages["render_prologue"] == "skipped" and stages["extract"] == "pending"


def test_hybrid_with_prologue_has_active_prologue_stage(bob, pdf_for, estimate_for):
    bob.set_plan("pro")
    bob.grant(1000)
    est = estimate_for(bob, pdf_for(bob), kind="hybrid_lesson", include_prologue=True, target_seconds=90)
    assert est["breakdown"]["seconds"]["threejs"] == 30
    job = create_job(bob, est).json()
    stages = {s["stage"]: s["status"] for s in job["stages"]}
    assert job["include_prologue"] is True and stages["render_prologue"] == "pending"


def test_402_insufficient_credits_and_nothing_persists(alice, pdf_for, estimate_for, pool):
    alice.grant(1)
    est = estimate_for(alice, pdf_for(alice))
    r = create_job(alice, est)
    assert r.status_code == 402 and r.json()["code"] == "insufficient_credits"
    with pool.connection() as c:
        assert c.execute("SELECT count(*) AS n FROM jobs").fetchone()["n"] == 0
        assert c.execute("SELECT count(*) AS n FROM outbox").fetchone()["n"] == 0
    assert alice.balance()["available"] == 1


def test_idempotent_create_same_body_replays(alice, pdf_for, estimate_for, pool):
    alice.grant(200)
    est = estimate_for(alice, pdf_for(alice))
    r1 = create_job(alice, est, key="key-12345678")
    r2 = create_job(alice, est, key="key-12345678")
    assert r1.status_code == r2.status_code == 201
    assert r1.json()["id"] == r2.json()["id"] and r2.headers["Idempotent-Replayed"] == "true"
    with pool.connection() as c:
        assert c.execute("SELECT count(*) AS n FROM credit_ledger WHERE entry_type='reserve'").fetchone()["n"] == 1
    assert alice.balance()["held"] == est["max_credits"]


def test_409_idempotency_conflict_same_key_different_body(alice, pdf_for, estimate_for):
    alice.grant(500)
    pid = pdf_for(alice)
    e1, e2 = estimate_for(alice, pid), estimate_for(alice, pid, target_seconds=20)
    assert create_job(alice, e1, key="key-abcdefgh").status_code == 201
    r = create_job(alice, e2, key="key-abcdefgh")
    assert r.status_code == 409 and r.json()["code"] == "idempotency_conflict"


def test_idempotency_key_required_and_scoped_per_user(alice, bob, pdf_for, estimate_for, client):
    alice.grant(200)
    est = estimate_for(alice, pdf_for(alice))
    r = client.post("/v1/jobs", headers=alice.headers,
                    json={"estimate_id": est["estimate_id"], "estimate_hash": est["estimate_hash"],
                          "max_authorized_credits": est["max_credits"]})
    assert r.status_code == 422
    # la misma clave en otro usuario no interfiere
    bob.grant(200)
    e_b = estimate_for(bob, pdf_for(bob))
    assert create_job(alice, est, key="shared-key-1").status_code == 201
    assert create_job(bob, e_b, key="shared-key-1").status_code == 201


def test_failed_attempt_does_not_cache_error_retry_works(alice, pdf_for, estimate_for):
    est = estimate_for(alice, pdf_for(alice))
    assert create_job(alice, est, key="retry-key-1").status_code == 402
    alice.grant(200)
    assert create_job(alice, est, key="retry-key-1").status_code == 201


def test_estimate_second_use_is_409(alice, pdf_for, estimate_for):
    alice.grant(500)
    est = estimate_for(alice, pdf_for(alice))
    assert create_job(alice, est).status_code == 201
    r = create_job(alice, est)
    assert r.status_code == 409 and r.json()["code"] == "estimate_already_used"


def test_estimate_expired_is_409(alice, pdf_for, estimate_for, pool):
    alice.grant(200)
    est = estimate_for(alice, pdf_for(alice))
    with pool.connection() as c:
        c.execute("UPDATE job_estimates SET expires_at = now() - interval '1 second'")
    r = create_job(alice, est)
    assert r.status_code == 409 and r.json()["code"] == "estimate_expired"


def test_estimate_tampered_hash_or_credits(alice, pdf_for, estimate_for, client):
    alice.grant(500)
    est = estimate_for(alice, pdf_for(alice))
    bad = {**est, "estimate_hash": "0" * 64}
    r = create_job(alice, bad)
    assert r.status_code == 409 and r.json()["code"] == "estimate_mismatch"
    # autorizar menos que el estimado o más que el máximo
    assert create_job(alice, est, max_auth=est["estimated_credits"] - 1).status_code == 422
    assert create_job(alice, est, max_auth=est["max_credits"] + 1).status_code == 422
    # autorizar exactamente el estimado es válido y reserva solo eso
    r = create_job(alice, est, max_auth=est["estimated_credits"])
    assert r.status_code == 201 and r.json()["reserved_credits"] == est["estimated_credits"]


def test_estimate_pricing_version_change_is_409(alice, pdf_for, estimate_for, pool):
    alice.grant(200)
    est = estimate_for(alice, pdf_for(alice))
    with pool.connection() as c:
        c.execute("UPDATE job_estimates SET pricing_version='old'")
    r = create_job(alice, est)
    assert r.status_code == 409 and r.json()["code"] == "pricing_changed"


def test_isolation_between_users(alice, bob, make_job, pdf_for, estimate_for, client):
    alice.grant(300)
    bob.grant(300)
    job, est = make_job(alice)
    jid = job["id"]
    # bob no ve, no cancela, no descarga, no usa estimación ni PDF de alice
    assert client.get(f"/v1/jobs/{jid}", headers=bob.headers).status_code == 404
    assert client.get(f"/v1/jobs/{jid}/assets", headers=bob.headers).status_code == 404
    assert client.post(f"/v1/jobs/{jid}/cancel", headers=bob.h(**{"Idempotency-Key": "k-bob-12345"})).status_code == 404
    r = create_job(bob, est)
    assert r.status_code == 404                                    # estimación ajena
    pid_alice = pdf_for(alice)
    r = client.post("/v1/jobs/estimate", headers=bob.headers,
                    json={"pdf_file_id": pid_alice, "kind": "solution_video", "config": {"target_seconds": 30}})
    assert r.status_code == 404                                    # PDF ajeno
    assert client.get("/v1/jobs", headers=bob.headers).json()["items"] == []
    assert client.get("/v1/credits/ledger", headers=bob.headers).json()["items"][0]["entry_type"] == "grant"
    assert bob.balance()["available"] == 300 and bob.balance()["held"] == 0


def test_job_not_ready_assets_then_ready(alice, make_job, client, pool):
    alice.grant(200)
    job, _ = make_job(alice)
    r = client.get(f"/v1/jobs/{job['id']}/assets", headers=alice.headers)
    assert r.status_code == 409 and r.json()["code"] == "job_not_ready"
    from app import lifecycle
    lifecycle.mark_running(pool, job["id"])
    lifecycle.complete_job(pool, job["id"], 10)
    assert client.get(f"/v1/jobs/{job['id']}/assets", headers=alice.headers).status_code == 409  # sin video aún
    with pool.connection() as c:
        c.execute("""INSERT INTO videos(job_id,user_id,storage_key,share_key,duration_seconds,width,height,fps,
                     size_bytes,sha256) VALUES (%s,%s,'v/k.mp4','v/s.mp4',30,1280,720,30,1000,%s)""",
                  (job["id"], alice.id, "c" * 64))
    r = client.get(f"/v1/jobs/{job['id']}/assets", headers=alice.headers)
    assert r.status_code == 200 and "sig=get" in r.json()["video_url"] and r.json()["share_url"]
    j = client.get(f"/v1/jobs/{job['id']}", headers=alice.headers).json()
    assert j["status"] == "succeeded" and j["video"]["fps"] == 30 and j["final_credits"] == 10


def test_stage_and_scene_progress_in_job(alice, make_job, client, pool):
    alice.grant(200)
    job, _ = make_job(alice)
    with pool.connection() as c:
        for i, (lab, eng, st) in enumerate([("01", "manim", "running"), ("02", "manim", "running"),
                                            ("A1", "svg", "succeeded")]):
            c.execute("""INSERT INTO job_scenes(job_id,position,label,engine,spec,spec_hash,planned_seconds,status)
                         VALUES (%s,%s,%s,%s,%s,%s,5,%s)""", (job["id"], i, lab, eng, Jsonb({}), "d" * 64, st))
        c.execute("UPDATE job_stages SET status='running' WHERE job_id=%s AND stage IN ('render_manim','render_svg')",
                  (job["id"],))
    j = client.get(f"/v1/jobs/{job['id']}", headers=alice.headers).json()
    assert j["scenes"]["total"] == 3 and j["scenes"]["by_status"] == {"running": 2, "succeeded": 1}
    st = {s["stage"]: s["status"] for s in j["stages"]}
    assert st["render_manim"] == st["render_svg"] == "running"      # etapas paralelas simultáneas


def test_concurrent_job_limit_per_plan(alice, pdf_for, estimate_for):
    alice.grant(500)
    pid = pdf_for(alice)
    assert create_job(alice, estimate_for(alice, pid)).status_code == 201
    r = create_job(alice, estimate_for(alice, pid))
    assert r.status_code == 409 and r.json()["code"] == "concurrency_limit"      # free = 1


def test_pagination_cursor(bob, pdf_for, estimate_for, client):
    bob.set_plan("pro")
    bob.grant(2000)
    pid = pdf_for(bob)
    ids = [create_job(bob, estimate_for(bob, pid)).json()["id"] for _ in range(3)]
    p1 = client.get("/v1/jobs?limit=2", headers=bob.headers).json()
    assert len(p1["items"]) == 2 and p1["next_cursor"]
    p2 = client.get(f"/v1/jobs?limit=2&cursor={p1['next_cursor']}", headers=bob.headers).json()
    assert len(p2["items"]) == 1 and p2["next_cursor"] is None
    assert [j["id"] for j in p1["items"] + p2["items"]] == ids[::-1]
    assert client.get("/v1/jobs?cursor=garbage", headers=bob.headers).status_code == 422
