from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from typing import Any

import psycopg

from .. import options, pricing
from ..auth import CurrentUser
from ..errors import ApiError, translate_db_error
from ..schemas import EstimateRequest

STAGE_ORDER = ["extract", "script", "render_manim", "render_prologue", "render_svg", "compose", "upload"]


def _not_found(what: str = "Recurso") -> ApiError:
    return ApiError(404, "not_found", f"{what} no encontrado.")


def encode_cursor(*parts: Any) -> str:
    return base64.urlsafe_b64encode("|".join(str(p) for p in parts).encode()).decode()


def decode_cursor(cursor: str, n: int) -> list[str]:
    try:
        parts = base64.urlsafe_b64decode(cursor.encode()).decode().split("|")
        if len(parts) != n:
            raise ValueError
        return parts
    except Exception:
        raise ApiError(422, "validation_error", "Cursor inválido.")


# ---------------------------------------------------------------- estimación
def create_estimate(conn, user: CurrentUser, req: EstimateRequest, ttl_seconds: int) -> dict:
    pdf = conn.execute("SELECT id, status, page_count, ocr_required FROM pdf_files "
                       "WHERE id=%s AND user_id=%s AND deleted_at IS NULL", (req.pdf_file_id, user.id)).fetchone()
    if pdf is None:
        raise _not_found("PDF")
    if pdf["status"] != "analyzed":
        raise ApiError(409, "pdf_not_ready", "El PDF aún no está analizado.")
    cfg = req.config
    problems = []
    if cfg.language not in options.LANGUAGES:
        problems.append({"field": "language", "allowed": options.LANGUAGES})
    if cfg.detail_level not in options.DETAIL_LEVELS:
        problems.append({"field": "detail_level", "allowed": options.DETAIL_LEVELS})
    allowed_res = options.allowed_resolutions(user.plan)
    if cfg.resolution not in allowed_res:
        problems.append({"field": "resolution", "allowed": allowed_res})
    if not options.MIN_TARGET_SECONDS <= cfg.target_seconds <= user.plan.max_video_seconds:
        problems.append({"field": "target_seconds",
                         "allowed": [options.MIN_TARGET_SECONDS, user.plan.max_video_seconds]})
    if cfg.include_prologue and (req.kind != "hybrid_lesson" or not user.plan.allows_prologue):
        problems.append({"field": "include_prologue",
                         "reason": "solo hybrid_lesson y planes que lo incluyen"})
    if pdf["page_count"] > user.plan.max_pdf_pages:
        problems.append({"field": "pdf_file_id", "reason": "excede las páginas del plan"})
    if problems:
        raise ApiError(422, "invalid_config", "Configuración fuera de las opciones publicadas.",
                       {"problems": problems})

    est = pricing.estimate(req.kind, cfg.target_seconds, cfg.include_prologue, cfg.resolution,
                           pdf["page_count"] if pdf["ocr_required"] else 0)
    config = cfg.model_dump()
    h = pricing.estimate_hash(str(req.pdf_file_id), req.kind, config, est, pricing.PRICING_VERSION)
    expires = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    row = conn.execute(
        """INSERT INTO job_estimates(user_id, pdf_file_id, kind, config, estimated_seconds, estimated_credits,
                                     max_credits, breakdown, pricing_version, config_hash, expires_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (user.id, req.pdf_file_id, req.kind, psycopg.types.json.Jsonb(config), est["estimated_seconds"],
         est["estimated_credits"], est["max_credits"], psycopg.types.json.Jsonb(est["breakdown"]),
         pricing.PRICING_VERSION, h, expires)).fetchone()
    available = conn.execute("SELECT COALESCE(SUM(delta),0)::int AS a FROM credit_ledger WHERE user_id=%s",
                             (user.id,)).fetchone()["a"]
    return {"estimate_id": row["id"], "estimate_hash": h, "kind": req.kind,
            "estimated_credits": est["estimated_credits"], "max_credits": est["max_credits"],
            "estimated_seconds": est["estimated_seconds"], "breakdown": est["breakdown"],
            "pricing_version": pricing.PRICING_VERSION, "expires_at": expires,
            "available_credits": available, "sufficient_credits": available >= est["max_credits"]}


# ---------------------------------------------------------------- crear / cancelar
def create_job(conn, user: CurrentUser, estimate_id, estimate_hash: str, max_auth: int,
               pipeline_version: str) -> dict:
    est = conn.execute("SELECT pricing_version FROM job_estimates WHERE id=%s AND user_id=%s",
                       (estimate_id, user.id)).fetchone()
    if est is None:
        raise _not_found("Estimación")
    if est["pricing_version"] != pricing.PRICING_VERSION:
        raise ApiError(409, "pricing_changed", "Las tarifas cambiaron; solicita una nueva estimación.")
    try:
        job_id = conn.execute("SELECT create_queued_job(%s,%s,%s,%s,%s,%s) AS id",
                              (user.id, estimate_id, estimate_hash, max_auth, pipeline_version,
                               user.plan.max_concurrent_jobs)).fetchone()["id"]
    except psycopg.errors.RaiseException as exc:
        err = translate_db_error(exc)
        details = {"required": max_auth} if err.code == "insufficient_credits" else None
        raise ApiError(err.status, err.code, err.message, details)
    return load_job(conn, job_id, user.id)


def cancel_job(conn, user: CurrentUser, job_id) -> dict:
    try:
        conn.execute("SELECT request_cancel(%s,%s)", (job_id, user.id))
    except psycopg.errors.RaiseException as exc:
        err = translate_db_error(exc)
        raise ApiError(err.status, err.code, err.message)
    return load_job(conn, job_id, user.id)


# ---------------------------------------------------------------- lectura
def _verification(delivery) -> dict | None:
    if not isinstance(delivery, dict):
        return None
    probs = delivery.get("problems") if isinstance(delivery.get("problems"), list) else None
    st = delivery.get("stages") if isinstance(delivery.get("stages"), dict) else {}
    ver = delivery.get("verification")
    return {
        "status": ver if ver in ("verified", "partially_verified", "requires_review", "unsupported") else None,
        "problems_total": len(probs) if probs is not None else None,
        "problems_verified": sum(1 for p in probs if p.get("pass")) if probs is not None else None,
        "render": str(st["render"]).lower() if st.get("render") else None,
        "qa": str(st["qa"]).lower() if st.get("qa") else None,
        "profile": delivery.get("profile") if isinstance(delivery.get("profile"), str) else None,
        "delivery_ready": delivery.get("delivery_ready") is True,
        "simulated": delivery.get("mock") is True,
    }


def _hydrate(conn, rows: list[dict]) -> list[dict]:
    if not rows:
        return []
    ids = [r["id"] for r in rows]
    stages = conn.execute("""SELECT job_id, stage, status, attempt, started_at, finished_at FROM job_stages
                             WHERE job_id = ANY(%s) ORDER BY attempt""", (ids,)).fetchall()
    scenes = conn.execute("""SELECT job_id, label, engine, status, planned_seconds::float AS planned_seconds
                             FROM job_scenes WHERE job_id = ANY(%s) ORDER BY position""", (ids,)).fetchall()
    videos = conn.execute("""SELECT job_id, duration_seconds::float AS duration_seconds, width, height, fps,
                             size_bytes FROM videos WHERE job_id = ANY(%s) AND deleted_at IS NULL""",
                          (ids,)).fetchall()
    out = []
    for r in rows:
        st: dict[str, dict] = {}
        for s in (x for x in stages if x["job_id"] == r["id"]):
            st[s["stage"]] = {k: s[k] for k in ("stage", "status", "attempt", "started_at", "finished_at")}
        stage_list = [st.get(n) or {"stage": n, "status": "pending", "attempt": 1} for n in STAGE_ORDER]
        sc = [x for x in scenes if x["job_id"] == r["id"]]
        by: dict[str, int] = {}
        for x in sc:
            by[x["status"]] = by.get(x["status"], 0) + 1
        vid = next((x for x in videos if x["job_id"] == r["id"]), None)
        out.append({
            "id": r["id"], "kind": r["kind"], "status": r["status"], "current_stage": r["current_stage"],
            "progress_pct": r["progress_pct"], "include_prologue": r["include_prologue"], "config": r["config"],
            "estimated_credits": r["estimated_credits"], "max_authorized_credits": r["max_authorized_credits"],
            "reserved_credits": r["reserved_credits"], "final_credits": r["final_credits"],
            "cancel_requested": r["cancel_requested_at"] is not None,
            "error_code": r["error_code"], "error_message": r["error_message"],
            "created_at": r["created_at"], "queued_at": r["queued_at"], "started_at": r["started_at"],
            "finished_at": r["finished_at"], "stages": stage_list,
            "scenes": {"total": len(sc), "by_status": by,
                       "items": [{k: x[k] for k in ("label", "engine", "status", "planned_seconds")} for x in sc]},
            "video": ({k: vid[k] for k in ("duration_seconds", "width", "height", "fps", "size_bytes")}
                      if vid and r["status"] == "succeeded" else None),
            "verification": _verification(r.get("delivery")),
        })
    return out


def load_job(conn, job_id, user_id) -> dict:
    row = conn.execute("SELECT * FROM jobs WHERE id=%s AND user_id=%s", (job_id, user_id)).fetchone()
    if row is None:
        raise _not_found("Job")
    return _hydrate(conn, [row])[0]


def list_jobs(conn, user_id, limit: int, cursor: str | None) -> dict:
    params: list[Any] = [user_id]
    where = ""
    if cursor:
        ts, jid = decode_cursor(cursor, 2)
        where = "AND (created_at, id) < (%s::timestamptz, %s::uuid)"
        params += [ts, jid]
    rows = conn.execute(f"SELECT * FROM jobs WHERE user_id=%s {where} ORDER BY created_at DESC, id DESC LIMIT %s",
                        params + [limit + 1]).fetchall()
    page, more = rows[:limit], len(rows) > limit
    nxt = encode_cursor(page[-1]["created_at"].isoformat(), page[-1]["id"]) if more else None
    return {"items": _hydrate(conn, page), "next_cursor": nxt}


def job_assets(conn, store, job_id, user_id, ttl: int) -> dict:
    j = conn.execute("SELECT id, status FROM jobs WHERE id=%s AND user_id=%s", (job_id, user_id)).fetchone()
    if j is None:
        raise _not_found("Job")
    v = conn.execute("SELECT storage_key, share_key FROM videos WHERE job_id=%s AND deleted_at IS NULL "
                     "AND (expires_at IS NULL OR expires_at > now())", (job_id,)).fetchone()
    if j["status"] != "succeeded" or v is None:
        raise ApiError(409, "job_not_ready", "El video todavía no está disponible.")
    return {"video_url": store.presign_get(v["storage_key"], ttl, "video.mp4"),
            "share_url": store.presign_get(v["share_key"], ttl, "video-share.mp4") if v["share_key"] else None,
            "expires_in_seconds": ttl}
