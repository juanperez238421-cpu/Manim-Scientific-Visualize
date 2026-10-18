"""Canal worker -> API: lease, heartbeat, entrega verificada, fallos, cancelación, almacenamiento local firmado."""
from __future__ import annotations

import hashlib
import time

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.routers.worker import video_keys
from app.storage import LocalFsStore
from tests.conftest import WORKER_TOKEN, FakeStore
from tests.helpers import assert_job_accounting, job as db_job

H = {"Authorization": f"Bearer {WORKER_TOKEN}"}
BASE = "/internal/worker/v1"
VIDEO = b"\x00\x00\x00\x18ftypmp42" + b"x" * 5000
OK_DELIVERY = {"delivery_ready": True, "verification": "verified", "stages": {"render": "pass", "qa": "pass"}}


def claim(client, worker="w-local-1"):
    r = client.post(f"{BASE}/claim", headers=H, json={"worker_id": worker})
    assert r.status_code == 200, r.text
    return r.json()["job"]


def put_video(store, actor_id, job_id, data=VIDEO):
    vkey, skey = video_keys(actor_id, job_id)
    store.objects[vkey] = data
    store.objects[skey] = data[:2000]
    return vkey, skey


def complete_body(worker="w-local-1", data=VIDEO, delivery=None, duration=30.0):
    return {"worker_id": worker, "delivery": delivery or OK_DELIVERY, "qa": {"pass": True},
            "video": {"duration_seconds": duration, "width": 1280, "height": 720, "fps": 30, "size_bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(), "share_size_bytes": 2000}}


@pytest.fixture
def queued(alice, make_job):
    alice.grant(500)
    j, est = make_job(alice, resolution="720p")
    return j


# ---------------------------------------------------------------- autenticación del canal
def test_channel_disabled_without_token(pool, store, rsa_key):
    from app.auth import JwtVerifier
    app = create_app(Settings(), pool=pool, store=store, verifier=JwtVerifier(lambda t: rsa_key.public_key(), "x"))
    with TestClient(app) as c:
        assert c.post(f"{BASE}/claim", json={"worker_id": "abc"}).status_code == 503


def test_wrong_or_missing_worker_token_is_401(client, queued):
    assert client.post(f"{BASE}/claim", json={"worker_id": "abc"}).status_code == 401
    assert client.post(f"{BASE}/claim", headers={"Authorization": "Bearer nope"}, json={"worker_id": "abc"}).status_code == 401
    # un JWT de usuario NO sirve como token de worker
    assert client.post(f"{BASE}/claim", headers={"Authorization": "Bearer " + "u" * 40}, json={"worker_id": "abc"}).status_code == 401


def test_internal_routes_not_in_public_openapi(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert not any(p.startswith("/internal") or p.startswith("/blob") for p in paths)


# ---------------------------------------------------------------- reclamo / lease
def test_claim_empty_then_claim_once(client, alice, queued):
    j = claim(client)
    assert j["id"] == queued["id"] and j["kind"] == "solution_video" and j["attempt"] == 1
    assert j["pdf"]["url"].startswith("https://store.test/users/") and len(j["pdf"]["sha256"]) == 64
    assert "email" not in str(j) and alice.sub not in str(j)                  # el worker no recibe identidad
    assert client.post(f"{BASE}/claim", headers=H, json={"worker_id": "w-local-2"}).json()["job"] is None
    assert client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["status"] == "running"


def test_expired_lease_is_reclaimed_and_old_worker_is_fenced(client, alice, queued, pool, store):
    claim(client, "w-old")
    with pool.connection() as c:
        c.execute("UPDATE jobs SET lease_expires_at = now() - interval '1 second' WHERE id=%s", (queued["id"],))
    j2 = claim(client, "w-new")
    assert j2["id"] == queued["id"] and j2["attempt"] == 2
    r = client.post(f"{BASE}/jobs/{queued['id']}/heartbeat", headers=H, json={"worker_id": "w-old"})
    assert r.status_code == 409 and r.json()["code"] == "lease_lost"
    put_video(store, alice.id, queued["id"])
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body("w-old"))
    assert r.status_code == 409 and r.json()["code"] == "lease_lost"
    assert client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body("w-new")).status_code == 200


def test_too_many_lost_workers_refunds_everything(client, alice, queued, pool):
    for i in range(3):
        claim(client, f"w-lost-{i}")
        with pool.connection() as c:
            c.execute("UPDATE jobs SET lease_expires_at = now() - interval '1 second' WHERE id=%s", (queued["id"],))
    assert client.post(f"{BASE}/claim", headers=H, json={"worker_id": "w-last-9"}).json()["job"] is None
    j = db_job(pool, queued["id"])
    assert j["status"] == "failed" and j["error_code"] == "worker_lost" and j["final_credits"] == 0
    assert alice.balance() == {"available": 500, "held": 0, "total": 500}
    assert_job_accounting(pool, queued["id"])


# ---------------------------------------------------------------- éxito / fallo
def test_complete_registers_video_settles_and_user_can_download(client, alice, queued, pool, store):
    claim(client)
    r = client.post(f"{BASE}/jobs/{queued['id']}/stage", headers=H,
                    json={"worker_id": "w-local-1", "stage": "script", "status": "succeeded", "progress_pct": 40})
    assert r.status_code == 200 and r.json()["status"] == "ok"
    assert client.post(f"{BASE}/jobs/{queued['id']}/heartbeat", headers=H, json={"worker_id": "w-local-1"}).json() == {"status": "ok"}
    put_video(store, alice.id, queued["id"])
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body())
    assert r.status_code == 200, r.text
    final = r.json()["final_credits"]
    assert 0 < final <= queued["reserved_credits"]
    jj = client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()
    assert jj["status"] == "succeeded" and jj["progress_pct"] == 100 and jj["final_credits"] == final
    assert jj["video"]["height"] == 720 and jj["video"]["fps"] == 30
    assert {s["stage"]: s["status"] for s in jj["stages"]}["script"] == "succeeded"
    a = client.get(f"/v1/jobs/{queued['id']}/assets", headers=alice.headers)
    assert a.status_code == 200 and "video.mp4" in a.json()["video_url"] or a.json()["video_url"]
    assert alice.balance()["held"] == 0 and alice.balance()["available"] == 500 - final
    assert_job_accounting(pool, queued["id"])
    # idempotente
    assert client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body()).json()["final_credits"] == final


def test_complete_requires_verified_and_qa_and_uploaded_bytes(client, alice, queued, store):
    claim(client)
    bad = {"delivery_ready": False, "verification": "requires_review"}
    put_video(store, alice.id, queued["id"])
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body(delivery=bad))
    assert r.status_code == 409 and r.json()["code"] == "not_deliverable"
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H,
                    json=complete_body(delivery={"delivery_ready": True, "verification": "partially_verified"}))
    assert r.status_code == 409
    store.objects.pop(video_keys(alice.id, queued["id"])[0])
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body())
    assert r.status_code == 409 and r.json()["code"] == "upload_incomplete"
    assert client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["status"] == "running"


def test_platform_failure_refunds_all(client, alice, queued, pool):
    claim(client)
    r = client.post(f"{BASE}/jobs/{queued['id']}/fail", headers=H,
                    json={"worker_id": "w-local-1", "code": "render_failed", "message": "manim crashed", "platform_fault": True,
                          "delivery": {"delivery_ready": False, "verification": "verified"}})
    assert r.status_code == 200 and r.json()["final_credits"] == 0
    jj = client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()
    assert jj["status"] == "failed" and jj["error_code"] == "render_failed"
    assert alice.balance() == {"available": 500, "held": 0, "total": 500}
    assert_job_accounting(pool, queued["id"])


# ---------------------------------------------------------------- cancelación cooperativa
def test_cancel_running_job_via_heartbeat_then_confirm(client, alice, queued, pool, store):
    claim(client)
    r = client.post(f"/v1/jobs/{queued['id']}/cancel", headers=alice.h(**{"Idempotency-Key": "cancel-key-1"}))
    assert r.status_code == 200 and r.json()["cancel_requested"] is True and r.json()["status"] == "running"
    assert alice.balance()["held"] == queued["reserved_credits"]               # sigue retenido hasta confirmar
    hb = client.post(f"{BASE}/jobs/{queued['id']}/heartbeat", headers=H, json={"worker_id": "w-local-1"})
    assert hb.json() == {"status": "cancel_requested"}
    put_video(store, alice.id, queued["id"])
    r = client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body())
    assert r.status_code == 409 and r.json()["code"] == "cancel_requested"
    r = client.post(f"{BASE}/jobs/{queued['id']}/confirm-cancel", headers=H, json={"worker_id": "w-local-1", "consumed_credits": 0})
    assert r.status_code == 200 and r.json()["final_credits"] == 0
    assert client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["status"] == "cancelled"
    assert alice.balance() == {"available": 500, "held": 0, "total": 500}
    assert_job_accounting(pool, queued["id"])


def test_cancel_queued_job_is_never_claimed(client, alice, queued):
    client.post(f"/v1/jobs/{queued['id']}/cancel", headers=alice.h(**{"Idempotency-Key": "cancel-key-2"}))
    assert client.post(f"{BASE}/claim", headers=H, json={"worker_id": "w-local-1"}).json()["job"] is None


def test_worker_cannot_touch_unknown_job(client):
    r = client.post(f"{BASE}/jobs/00000000-0000-0000-0000-000000000000/heartbeat", headers=H, json={"worker_id": "w-local-1"})
    assert r.status_code == 404
    assert client.post(f"{BASE}/jobs/not-a-uuid/heartbeat", headers=H, json={"worker_id": "w-local-1"}).status_code == 404


# ---------------------------------------------------------------- almacenamiento local firmado
@pytest.fixture
def local_client(tmp_path, pool, rsa_key):
    from app.auth import JwtVerifier
    st = LocalFsStore(tmp_path / "blobs", "s" * 32, "http://testserver")
    app = create_app(Settings(worker_token=WORKER_TOKEN), pool=pool, store=st,
                     verifier=JwtVerifier(lambda t: rsa_key.public_key(), "x"))
    with TestClient(app) as c:
        yield c, st


def _rel(url):
    return url.replace("http://testserver", "")


def test_local_store_put_get_range_head(local_client):
    c, st = local_client
    put, _ = st.presign_put("users/u1/videos/j1/video.mp4", "video/mp4", 60)
    assert c.put(_rel(put), content=VIDEO).status_code == 200
    get = _rel(st.presign_get("users/u1/videos/j1/video.mp4", 60, "mi video.mp4"))
    r = c.get(get)
    assert r.status_code == 200 and r.content == VIDEO and r.headers["content-type"] == "video/mp4"
    assert 'filename="mi video.mp4"' in r.headers["content-disposition"]
    r = c.get(get, headers={"Range": "bytes=0-9"})
    assert r.status_code == 206 and r.content == VIDEO[:10] and r.headers["content-range"].startswith("bytes 0-9/")
    assert c.head(get).status_code == 200


def test_local_store_rejects_tamper_expiry_method_and_traversal(local_client):
    c, st = local_client
    key = "users/u1/pdfs/a.pdf"
    put, _ = st.presign_put(key, "application/pdf", 60)
    assert c.put(_rel(put) + "0", content=b"x").status_code == 403                    # firma alterada
    assert c.put(_rel(put).replace("a.pdf", "b.pdf"), content=b"x").status_code == 403   # otra clave
    assert c.get(_rel(put)).status_code == 403                                           # URL de PUT no sirve para GET
    old = LocalFsStore(st.root, "s" * 32, "http://testserver")
    exp = int(time.time()) - 5
    assert c.put(f"/blob/{key}?exp={exp}&sig={old.sign('PUT', key, exp)}", content=b"x").status_code == 403
    for bad in ("../x.pdf", "users/../../etc/passwd", "/abs.pdf", "a//b.pdf"):
        with pytest.raises(Exception):
            st.presign_get(bad, 60)
    exp = int(time.time()) + 60
    assert c.get(f"/blob/users%2F..%2F..%2Fx?exp={exp}&sig=00").status_code in (403, 404)


def test_local_store_atomic_and_secret_length(tmp_path):
    with pytest.raises(ValueError):
        LocalFsStore(tmp_path, "short", "http://x")


def test_local_store_enforces_size_limit(tmp_path, pool, rsa_key):
    from app.auth import JwtVerifier
    st = LocalFsStore(tmp_path / "b", "s" * 32, "http://testserver", max_object_bytes=100)
    app = create_app(Settings(worker_token=WORKER_TOKEN), pool=pool, store=st,
                     verifier=JwtVerifier(lambda t: rsa_key.public_key(), "x"))
    with TestClient(app) as c:
        put, _ = st.presign_put("users/u/a.bin", "application/octet-stream", 60)
        assert c.put(_rel(put), content=b"x" * 500).status_code == 413
        assert not list((tmp_path / "b").rglob("*.part")) and st.head("users/u/a.bin") is None


def test_job_exposes_separate_verification_verdicts(client, alice, queued, store):
    claim(client)
    assert client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["verification"] is None
    put_video(store, alice.id, queued["id"])
    d = {**OK_DELIVERY, "profile": "dev720", "mock": True, "problems": [{"id": "1", "pass": True}, {"id": "2", "pass": True}],
         "stages": {"render": "PASS", "qa": "PASS"}}
    assert client.post(f"{BASE}/jobs/{queued['id']}/complete", headers=H, json=complete_body(delivery=d)).status_code == 200
    v = client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["verification"]
    assert v == {"status": "verified", "problems_total": 2, "problems_verified": 2, "render": "pass", "qa": "pass",
                 "profile": "dev720", "delivery_ready": True, "simulated": True}


def test_failed_job_verification_shows_not_ready(client, alice, queued):
    claim(client)
    client.post(f"{BASE}/jobs/{queued['id']}/fail", headers=H,
                json={"worker_id": "w-local-1", "code": "verification_failed", "message": "x", "platform_fault": True,
                      "delivery": {"delivery_ready": False, "verification": "requires_review", "problems": [{"id": "1", "pass": False}]}})
    v = client.get(f"/v1/jobs/{queued['id']}", headers=alice.headers).json()["verification"]
    assert v["status"] == "requires_review" and v["delivery_ready"] is False and v["problems_verified"] == 0
