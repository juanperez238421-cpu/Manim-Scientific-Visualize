from fastapi import APIRouter, Depends, Query, Request

from ..auth import CurrentUser, get_current_user
from ..errors import ERROR_RESPONSES
from ..schemas import CreditsBalance, LedgerPage
from ..services import credits as svc

router = APIRouter(prefix="/v1/credits", tags=["credits"], responses={401: ERROR_RESPONSES[401], 422: ERROR_RESPONSES[422]})


@router.get("/balance", response_model=CreditsBalance, operation_id="getCreditsBalance")
def balance(request: Request, user: CurrentUser = Depends(get_current_user)):
    with request.app.state.pool.connection() as conn:
        return svc.balance(conn, user.id)


@router.get("/ledger", response_model=LedgerPage, operation_id="getCreditsLedger")
def ledger(request: Request, limit: int = Query(20, ge=1, le=100), cursor: str | None = None,
           user: CurrentUser = Depends(get_current_user)):
    with request.app.state.pool.connection() as conn:
        return svc.ledger(conn, user.id, limit, cursor)
