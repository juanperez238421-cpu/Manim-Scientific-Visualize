"""Canal INTERNO worker -> API (no aparece en el OpenAPI público).

El worker local se conecta SALIENTE (sin puertos entrantes), se autentica con un token de servicio, reclama jobs con
lease, envía latidos y entrega resultados. No recibe credenciales de BD, ni el email/identidad del usuario, ni la clave
de Anthropic de la API. Los créditos se calculan AQUÍ a partir de la duración medida del video, no los dicta el worker.
"""
from __future__ import annotations

import hmac
import math
import re
from typing import Any

import psycopg
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from .. import pricing
from ..errors import ApiError, translate_db_error

router = APIRouter(prefix="/internal/worker/v1", include_in_schema=False)

STAGES = {"extract", "script", "render_manim", "render_prologue", "render_svg", "compose", "upload"}
STEP = {"running", "succeeded", "failed", "skipped"}
_WORKER_ID = re.compile(r"^[A-Za-z0-9_.:-]{3,64}$")
_SHA = re.compile(r"^[0-9a-f]{64}$")


def require_worker(request: Request) -> None:
    token = request.app.state.settings.worker_token
    if len(token) < 24:
        raise ApiError(503, "worker_channel_disabled", "Canal de workers deshabilitado (WORKER_TOKEN no configurado).")
    got = request.headers.get("authorization", "")
    if not got.startswith("Bearer ") or not hmac.compare_digest(got[7:].encode(), token.encode()):
        raise ApiError(401, "unauthorized", "Token de worker inválido.")


class Claim(BaseModel):
    worker_id: str


class Beat(BaseModel):
    worker_id: str


class StageIn(BaseModel):
    worker_id: str
    stage: str
    status: str
    progress_pct: int = Field(0, ge=0, le=100)


class VideoIn(BaseModel):
    duration_seconds: float = Field(gt=0, le=3600)
    width: int = Field(gt=0, le=7680)
    height: int = Field(gt=0, le=4320)
    fps: int = Field(gt=0, le=240)
    size_bytes: int = Field(gt=0)
    sha256: str
    share_size_bytes: int | None = None


class CompleteIn(BaseModel):
    worker_id: str
    video: VideoIn
    delivery: dict[str, Any]
    qa: dict[str, Any] = {}


class FailIn(BaseModel):
    worker_id: str
    code: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9_]+$")
    message: str = Field(max_length=1000)
    platform_fault: bool = True
    delivery: dict[str, Any] = {}


class CancelIn(BaseModel):
    worker_id: str
    consumed_credits: int = Field(0, ge=0)


def _wid(w: str) -> str:
    if not _WORKER_ID.match(w):
        raise ApiError(422, "validation_error", "worker_id inválido.")
    return w


def _call(conn, sql: str, params: tuple):
    try:
        return conn.execute(sql, params).fetchone()
    except psycopg.errors.RaiseException as exc:
        err = translate_db_error(exc)
        raise ApiError(err.status, err.code, err.message)


def _job_id(job_id: str):
    import uuid
    try:
        return uuid.UUID(job_id)
    except ValueError:
        raise ApiError(404, "not_found", "Job no encontrado.")


def video_keys(user_id, job_id) -> tuple[str, str]:
    return f"users/{user_id}/videos/{job_id}/video.mp4", f"users/{user_id}/videos/{job_id}/share.mp4"


@router.post("/claim", dependencies=[Depends(require_worker)])
def claim(body: Claim, request: Request):
    s = request.app.state
    wid = _wid(body.worker_id)
    with s.pool.connection() as conn:
        jid = _call(conn, "SELECT claim_job(%s,%s::int) AS id", (wid, s.settings.lease_seconds))["id"]
        if jid is None:
            return {"job": None}
        j = conn.execute("""SELECT j.id, j.kind, j.config, j.user_id, j.attempts, p.storage_key AS pdf_key,
                                   p.sha256 AS pdf_sha, p.size_bytes, p.page_count
                            FROM jobs j JOIN pdf_files p ON p.id = j.pdf_file_id WHERE j.id = %s""", (jid,)).fetchone()
    vkey, skey = video_keys(j["user_id"], j["id"])
    ttl = max(s.settings.signed_url_ttl_seconds, 3600)
    put_v, _ = s.store.presign_put(vkey, "video/mp4", ttl)
    put_s, _ = s.store.presign_put(skey, "video/mp4", ttl)
    return {"job": {
        "id": str(j["id"]), "kind": j["kind"], "config": j["config"], "attempt": j["attempts"],
        "lease_seconds": s.settings.lease_seconds,
        "pdf": {"url": s.store.presign_get(j["pdf_key"], ttl), "sha256": j["pdf_sha"],
                "size_bytes": j["size_bytes"], "pages": j["page_count"]},
        "outputs": {"video_put_url": put_v, "share_put_url": put_s},
    }}


@router.post("/jobs/{job_id}/heartbeat", dependencies=[Depends(require_worker)])
def heartbeat(job_id: str, body: Beat, request: Request):
    s = request.app.state
    with s.pool.connection() as conn:
        r = _call(conn, "SELECT worker_heartbeat(%s::uuid,%s,%s::int) AS r", (_job_id(job_id), _wid(body.worker_id),
                                                                   s.settings.lease_seconds))
    return {"status": r["r"]}


@router.post("/jobs/{job_id}/stage", dependencies=[Depends(require_worker)])
def stage(job_id: str, body: StageIn, request: Request):
    if body.stage not in STAGES or body.status not in STEP:
        raise ApiError(422, "validation_error", "Etapa o estado inválido.")
    s = request.app.state
    with s.pool.connection() as conn:
        r = _call(conn, "SELECT worker_set_stage(%s::uuid,%s,%s::stage_name,%s::step_status,%s::int,%s::int) AS r",
                  (_job_id(job_id), _wid(body.worker_id), body.stage, body.status, body.progress_pct,
                   s.settings.lease_seconds))
    return {"status": r["r"]}


@router.post("/jobs/{job_id}/complete", dependencies=[Depends(require_worker)])
def complete(job_id: str, body: CompleteIn, request: Request):
    s = request.app.state
    jid, wid, v = _job_id(job_id), _wid(body.worker_id), body.video
    if not _SHA.match(v.sha256):
        raise ApiError(422, "validation_error", "sha256 inválido.")
    d = body.delivery
    if d.get("delivery_ready") is not True or d.get("verification") != "verified":
        raise ApiError(409, "not_deliverable", "Solo se completa un job verificado y con QA aprobado; usa /fail.")
    with s.pool.connection() as conn:
        j = conn.execute("SELECT id, user_id, kind, include_prologue, config FROM jobs WHERE id=%s", (jid,)).fetchone()
        if j is None:
            raise ApiError(404, "not_found", "Job no encontrado.")
        vkey, skey = video_keys(j["user_id"], jid)
        size = s.store.head(vkey)
        if size is None or size != v.size_bytes:
            raise ApiError(409, "upload_incomplete", "El video no está subido o su tamaño no coincide.")
        has_share = v.share_size_bytes is not None and s.store.head(skey) == v.share_size_bytes
        cfg = j["config"]
        # créditos por duración REAL entregada, con las mismas tarifas de la estimación; se acotan a la reserva en SQL
        credits = pricing.estimate(j["kind"], max(1, math.ceil(v.duration_seconds)), j["include_prologue"],
                                   cfg.get("resolution", "1080p"), 0)["estimated_credits"]
        from psycopg.types.json import Jsonb
        charged = _call(conn, "SELECT worker_complete(%s::uuid,%s,%s::int,%s,%s,%s,%s::numeric,%s::int,%s::int,%s::int,%s::bigint,%s,%s) AS r",
                        (jid, wid, credits, Jsonb(d), vkey, skey if has_share else None, v.duration_seconds,
                         v.width, v.height, v.fps, v.size_bytes, v.sha256, Jsonb(body.qa)))["r"]
    return {"status": "succeeded", "final_credits": charged}


@router.post("/jobs/{job_id}/fail", dependencies=[Depends(require_worker)])
def fail(job_id: str, body: FailIn, request: Request):
    from psycopg.types.json import Jsonb
    s = request.app.state
    with s.pool.connection() as conn:
        charged = _call(conn, "SELECT worker_fail(%s::uuid,%s,%s,%s,%s,%s::int,%s) AS r",
                        (_job_id(job_id), _wid(body.worker_id), body.code, body.message[:1000], body.platform_fault,
                         0, Jsonb(body.delivery)))["r"]
    return {"status": "failed", "final_credits": charged}


@router.post("/jobs/{job_id}/confirm-cancel", dependencies=[Depends(require_worker)])
def confirm_cancel(job_id: str, body: CancelIn, request: Request):
    s = request.app.state
    with s.pool.connection() as conn:
        charged = _call(conn, "SELECT worker_confirm_cancel(%s::uuid,%s,%s::int) AS r",
                        (_job_id(job_id), _wid(body.worker_id), body.consumed_credits))["r"]
    return {"status": "cancelled", "final_credits": charged}
