from fastapi import APIRouter, Depends, Request

from ..auth import CurrentUser, get_current_user
from ..errors import ERROR_RESPONSES
from ..schemas import UploadCompleteResponse, UploadInitRequest, UploadInitResponse
from ..services import uploads as svc

router = APIRouter(prefix="/v1/uploads", tags=["uploads"],
                   responses={k: ERROR_RESPONSES[k] for k in (401, 404, 409, 422)})


@router.post("/init", response_model=UploadInitResponse, operation_id="initiateUpload")
def init(body: UploadInitRequest, request: Request, user: CurrentUser = Depends(get_current_user)):
    s = request.app.state
    with s.pool.connection() as conn:
        return svc.init_upload(conn, s.store, user, body.filename, body.size_bytes, body.sha256,
                               s.settings.upload_url_ttl_seconds)


@router.post("/{file_id}/complete", response_model=UploadCompleteResponse, operation_id="completeUpload")
def complete(file_id: str, request: Request, user: CurrentUser = Depends(get_current_user)):
    import uuid
    from ..errors import ApiError
    try:
        fid = uuid.UUID(file_id)
    except ValueError:
        raise ApiError(404, "not_found", "PDF no encontrado.")
    s = request.app.state
    with s.pool.connection() as conn:
        return svc.complete_upload(conn, s.store, user, fid)
