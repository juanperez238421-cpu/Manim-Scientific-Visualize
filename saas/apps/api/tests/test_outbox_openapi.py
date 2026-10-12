import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openapi_spec_validator import validate

from app import lifecycle
from app.main import create_app
from app.outbox import relay_once
from tests.helpers import available, held, job, new_user, queue_job


class Pub:
    def __init__(self, fail=False):
        self.fail, self.sent = fail, []
        self.lock = threading.Lock()

    def publish(self, topic, payload, task_id):
        if self.fail:
            raise ConnectionError("redis down")
        with self.lock:
            self.sent.append((topic, payload["job_id"], task_id))


def outbox_row(pool, jid):
    with pool.connection() as c:
        return c.execute("SELECT * FROM outbox WHERE job_id=%s", (jid,)).fetchone()


def test_outbox_written_with_reservation_and_publish_failure_is_recoverable(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    assert outbox_row(pool, j)["status"] == "pending"                 # misma transacción que la reserva
    # Redis caído: el relay falla, nada se pierde, el job sigue encolado y con créditos reservados
    assert relay_once(pool, Pub(fail=True)) == {"published": 0, "failed": 1}
    row = outbox_row(pool, j)
    assert row["status"] == "pending" and row["attempts"] == 1 and "redis down" in row["last_error"]
    assert job(pool, j)["status"] == "queued" and held(pool, u) == 40
    assert relay_once(pool, Pub()) == {"published": 0, "failed": 0}   # backoff: aún no toca reintentar
    with pool.connection() as c:
        c.execute("UPDATE outbox SET available_at = now() WHERE job_id=%s", (j,))
    pub = Pub()
    assert relay_once(pool, pub) == {"published": 1, "failed": 0}
    assert pub.sent == [("job.run", str(j), str(j))]                  # task_id = job_id (idempotente)
    assert relay_once(pool, pub) == {"published": 0, "failed": 0} and len(pub.sent) == 1


def test_concurrent_relays_publish_each_job_once(pool):
    u = new_user(pool, 10_000)
    jobs = [queue_job(pool, u, 10) for _ in range(20)]
    pub = Pub()
    barrier = threading.Barrier(4)

    def go(_):
        barrier.wait()
        return relay_once(pool, pub, batch=50)["published"]
    with ThreadPoolExecutor(4) as ex:
        assert sum(ex.map(go, range(4))) == 20
    assert sorted(x[1] for x in pub.sent) == sorted(str(j) for j in jobs)


def test_cancelled_job_is_never_published(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    with pool.connection() as c:
        c.execute("SELECT request_cancel(%s,%s)", (j, u))
    pub = Pub()
    assert relay_once(pool, pub) == {"published": 0, "failed": 0} and pub.sent == []
    assert available(pool, u) == 100


def test_duplicate_delivery_after_publish_is_harmless(pool):
    """At-least-once: si la tarea llega dos veces, la segunda no ejecuta ni cobra de nuevo."""
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    assert lifecycle.mark_running(pool, j) == "started"
    assert lifecycle.mark_running(pool, j) == "resumed"               # re-entrega tras caída de worker
    lifecycle.complete_job(pool, j, 20)
    assert lifecycle.mark_running(pool, j) == "terminal"
    assert available(pool, u) == 80


def test_worker_crash_failure_releases_everything(pool):
    u = new_user(pool, 100)
    j = queue_job(pool, u, 40)
    lifecycle.mark_running(pool, j)
    lifecycle.fail_job(pool, j, "worker_lost", "OOM", platform_fault=True, consumed=40)
    assert available(pool, u) == 100 and held(pool, u) == 0


# ---------------------------------------------------------------- OpenAPI real
EXPECTED_OPS = {"getMe", "getRenderOptions", "initiateUpload", "completeUpload", "estimateJob", "createJob",
                "listJobs", "getJob", "cancelJob", "getJobAssets", "getCreditsBalance", "getCreditsLedger"}


def test_generated_openapi_is_valid_complete_and_committed(client):
    spec = client.get("/openapi.json").json()
    validate(spec)
    assert spec["openapi"].startswith("3.1")
    ops = {op["operationId"] for p in spec["paths"].values() for op in p.values()}
    assert ops == EXPECTED_OPS
    create = spec["paths"]["/v1/jobs"]["post"]
    assert any(p["name"] == "Idempotency-Key" and p["required"] for p in create["parameters"])
    cancel = spec["paths"]["/v1/jobs/{job_id}/cancel"]["post"]
    assert any(p["name"] == "Idempotency-Key" and p["required"] for p in cancel["parameters"])
    for code in ("401", "402", "409", "422"):
        assert code in create["responses"]
    err = spec["components"]["schemas"]["ApiErrorBody"]
    assert set(err["required"]) == {"code", "message", "request_id"}
    status_enum = spec["components"]["schemas"]["Job"]["properties"]["status"]["enum"]
    assert status_enum == ["draft", "queued", "running", "succeeded", "failed", "cancelled"]
    committed = json.loads((Path(__file__).resolve().parents[1] / "openapi.json").read_text())
    assert committed == spec, "openapi.json desactualizado: ejecuta scripts/export_openapi.py"


def test_enums_match_sql(pool):
    from app.schemas import JobKind, JobStatus, StageName
    from typing import get_args
    with pool.connection() as c:
        def labels(t):
            return [r["enumlabel"] for r in c.execute(
                "SELECT enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname=%s "
                "ORDER BY enumsortorder", (t,)).fetchall()]
        assert labels("job_status") == list(get_args(JobStatus))
        assert labels("job_kind") == list(get_args(JobKind))
        assert labels("stage_name") == list(get_args(StageName))
