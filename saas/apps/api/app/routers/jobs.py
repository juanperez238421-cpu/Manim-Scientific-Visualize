import uuid

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import JSONResponse

from ..auth import CurrentUser, get_current_user
from ..errors import ERROR_RESPONSES, ApiError
from ..idempotency import request_hash, run_idempotent
from ..schemas import CreateJobRequest, EstimateRequest, Job, JobAssets, JobEstimate, JobPage
from ..services import jobs as svc

router = APIRouter(prefix="/v1/jobs", tags=["jobs"],
                   responses={k: ERROR_RESPONSES[k] for k in (401, 404, 409, 422)})

IdemKey = Header(alias="Idempotency-Key", min_length=8, max_length=128,
                 description="Obligatoria. Misma clave + mismo cuerpo = misma respuesta.")


def _uuid(value: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except ValueError:
        raise ApiError(404, "not_found", "Job no encontrado.")


def _reply(status: int, body: dict, replayed: bool) -> JSONResponse:
    from fastapi.encoders import jsonable_encoder
    return JSONResponse(jsonable_encoder(body), status_code=status,
                        headers={"Idempotent-Replayed": "true"} if replayed else None)


@router.post("/estimate", response_model=JobEstimate, operation_id="estimateJob")
def estimate(body: EstimateRequest, request: Request, user: CurrentUser = Depends(get_current_user)):
    s = request.app.state
    with s.pool.connection() as conn:
        return svc.create_estimate(conn, user, body, s.settings.estimate_ttl_seconds)


@router.post("", response_model=Job, status_code=201, operation_id="createJob",
             responses={402: ERROR_RESPONSES[402]})
def create(body: CreateJobRequest, request: Request, idem_key: str = IdemKey,
           user: CurrentUser = Depends(get_current_user)):
    s = request.app.state
    h = request_hash(body.model_dump(mode="json"))
    with s.pool.connection() as conn:
        status, out, replayed = run_idempotent(
            conn, user.id, "job.create", idem_key, h,
            lambda: (201, _json(svc.create_job(conn, user, body.estimate_id, body.estimate_hash,
                                               body.max_authorized_credits, s.settings.pipeline_version))))
    return _reply(status, out, replayed)


@router.get("", response_model=JobPage, operation_id="listJobs")
def list_(request: Request, limit: int = Query(20, ge=1, le=100), cursor: str | None = None,
          user: CurrentUser = Depends(get_current_user)):
    with request.app.state.pool.connection() as conn:
        return svc.list_jobs(conn, user.id, limit, cursor)


@router.get("/{job_id}", response_model=Job, operation_id="getJob")
def get(job_id: str, request: Request, user: CurrentUser = Depends(get_current_user)):
    with request.app.state.pool.connection() as conn:
        return svc.load_job(conn, _uuid(job_id), user.id)


@router.post("/{job_id}/cancel", response_model=Job, operation_id="cancelJob")
def cancel(job_id: str, request: Request, idem_key: str = IdemKey,
           user: CurrentUser = Depends(get_current_user)):
    jid = _uuid(job_id)
    with request.app.state.pool.connection() as conn:
        status, out, replayed = run_idempotent(
            conn, user.id, f"job.cancel:{jid}", idem_key, request_hash({}, job_id=str(jid)),
            lambda: (200, _json(svc.cancel_job(conn, user, jid))))
    return _reply(status, out, replayed)


@router.get("/{job_id}/assets", response_model=JobAssets, operation_id="getJobAssets")
def assets(job_id: str, request: Request, user: CurrentUser = Depends(get_current_user)):
    s = request.app.state
    with s.pool.connection() as conn:
        return svc.job_assets(conn, s.store, _uuid(job_id), user.id, s.settings.signed_url_ttl_seconds)


def _json(model: dict) -> dict:
    from fastapi.encoders import jsonable_encoder
    return jsonable_encoder(model)
