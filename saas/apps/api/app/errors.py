"""Errores tipados: todos devuelven {code, message, request_id, details?}."""
from __future__ import annotations

import logging
import uuid
from typing import Any

import psycopg
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


log = logging.getLogger("animotion.api")


class ApiErrorBody(BaseModel):
    code: str
    message: str
    request_id: str
    details: dict[str, Any] | None = None


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details: dict | None = None):
        self.status, self.code, self.message, self.details = status, code, message, details


# código de negocio (mensaje de RAISE EXCEPTION en PostgreSQL) -> (HTTP, mensaje)
DB_ERRORS: dict[str, tuple[int, str]] = {
    "insufficient_credits": (402, "Créditos insuficientes para reservar el máximo autorizado."),
    "estimate_not_found": (404, "Estimación no encontrada."),
    "estimate_expired": (409, "La estimación venció; solicita una nueva."),
    "estimate_mismatch": (409, "La estimación no coincide con la mostrada (hash alterado)."),
    "estimate_already_used": (409, "Esta estimación ya generó un job."),
    "invalid_authorization": (422, "max_authorized_credits debe estar entre el estimado y el máximo."),
    "pdf_not_ready": (409, "El PDF no está analizado o fue eliminado."),
    "concurrency_limit": (409, "Alcanzaste el máximo de jobs simultáneos de tu plan."),
    "job_not_found": (404, "Job no encontrado."),
    "lease_lost": (409, "El worker perdió el lease de este job."),
    "cancel_requested": (409, "El usuario solicitó cancelar este job."),
    "cancel_not_requested": (409, "No hay cancelación solicitada."),
    "job_not_cancellable": (409, "El job ya terminó y no se puede cancelar."),
}


def translate_db_error(exc: psycopg.errors.RaiseException) -> ApiError:
    code = (exc.diag.message_primary or "").strip()
    status, msg = DB_ERRORS.get(code, (500, "Error interno."))
    if code not in DB_ERRORS:
        code = "internal_error"
    return ApiError(status, code, msg)


def _rid(request: Request) -> str:
    return getattr(request.state, "request_id", "-")


def install(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_id_mw(request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response

    def body(request, status, code, message, details=None, headers=None):
        payload = ApiErrorBody(code=code, message=message, request_id=_rid(request), details=details)
        return JSONResponse(payload.model_dump(exclude_none=True), status_code=status, headers=headers)

    @app.exception_handler(ApiError)
    async def _api(request: Request, exc: ApiError):
        return body(request, exc.status, exc.code, exc.message, exc.details,
                    {"WWW-Authenticate": "Bearer"} if exc.status == 401 else None)

    @app.exception_handler(RequestValidationError)
    async def _val(request: Request, exc: RequestValidationError):
        errs = [{"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
        return body(request, 422, "validation_error", "Solicitud inválida.", {"errors": errs})

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        code = {404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
        return body(request, exc.status_code, code, str(exc.detail))

    @app.exception_handler(psycopg.errors.RaiseException)
    async def _pg(request: Request, exc: psycopg.errors.RaiseException):
        e = translate_db_error(exc)
        return body(request, e.status, e.code, e.message)

    @app.exception_handler(Exception)
    async def _any(request: Request, exc: Exception):  # no filtrar detalles internos al cliente
        log.exception("unhandled error request_id=%s", _rid(request), exc_info=exc)
        return body(request, 500, "internal_error", "Error interno.")


ERROR_RESPONSES = {
    code: {"model": ApiErrorBody, "description": desc}
    for code, desc in {
        401: "Token ausente o inválido", 402: "Créditos insuficientes", 404: "No encontrado (o ajeno)",
        409: "Conflicto de estado o idempotencia", 422: "Validación",
    }.items()
}
