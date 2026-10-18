from fastapi import APIRouter, Depends

from .. import options
from ..auth import CurrentUser, get_current_user
from ..errors import ERROR_RESPONSES
from ..schemas import RenderOptions, User

router = APIRouter(prefix="/v1", tags=["meta"], responses={401: ERROR_RESPONSES[401]})


@router.get("/me", response_model=User, operation_id="getMe")
def get_me(user: CurrentUser = Depends(get_current_user)):
    p = user.plan
    return {"id": user.id, "email": user.email, "plan": p.code,
            "limits": {"max_pdf_pages": p.max_pdf_pages, "max_pdf_bytes": p.max_pdf_bytes,
                       "max_video_seconds": p.max_video_seconds, "max_concurrent_jobs": p.max_concurrent_jobs,
                       "max_resolution": p.max_resolution, "monthly_credits": p.monthly_credits}}


@router.get("/render-options", response_model=RenderOptions, operation_id="getRenderOptions")
def get_render_options(user: CurrentUser = Depends(get_current_user)):
    return options.render_options(user.plan)
