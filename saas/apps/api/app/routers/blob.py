"""Bytes del almacenamiento LOCAL de desarrollo, protegidos por URL firmada (HMAC, método+clave+expiración).
No aparece en el OpenAPI público. En nube lo reemplaza R2/S3 con URLs prefirmadas equivalentes."""
from __future__ import annotations

import os
import uuid

from fastapi import APIRouter, Query, Request
from fastapi.responses import FileResponse, Response

from ..errors import ApiError
from ..storage import BadKey, LocalFsStore

router = APIRouter(prefix="/blob", include_in_schema=False)


def _store(request: Request) -> LocalFsStore:
    st = request.app.state.store
    if not isinstance(st, LocalFsStore):
        raise ApiError(404, "not_found", "No encontrado.")
    return st


def _check(st: LocalFsStore, method: str, key: str, exp: int, sig: str, fn: str | None = None):
    try:
        st.path(key)
    except BadKey:
        raise ApiError(404, "not_found", "No encontrado.")
    ok = st.verify(method, key, exp, sig, fn or "")
    if not ok and method == "HEAD":
        ok = st.verify("GET", key, exp, sig, fn or "")
    if not ok:
        raise ApiError(403, "forbidden", "URL firmada inválida o vencida.")


@router.put("/{key:path}")
async def put_blob(key: str, request: Request, exp: int = Query(...), sig: str = Query(...)):
    st = _store(request)
    _check(st, "PUT", key, exp, sig)
    declared = request.headers.get("content-length")
    if declared and int(declared) > st.max_object_bytes:
        raise ApiError(413, "too_large", "Objeto demasiado grande.")
    dest = st.path(key)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.name}.{uuid.uuid4().hex}.part")
    total = 0
    try:
        with tmp.open("wb") as f:
            async for chunk in request.stream():
                total += len(chunk)
                if total > st.max_object_bytes:
                    raise ApiError(413, "too_large", "Objeto demasiado grande.")
                f.write(chunk)
        os.replace(tmp, dest)                # publicación atómica: nunca se ve un objeto a medias
    finally:
        tmp.unlink(missing_ok=True)
    return Response(status_code=200)


@router.api_route("/{key:path}", methods=["GET", "HEAD"])
def get_blob(key: str, request: Request, exp: int = Query(...), sig: str = Query(...), fn: str | None = None):
    st = _store(request)
    _check(st, request.method, key, exp, sig, fn)
    p = st.path(key)
    if not p.is_file():
        raise ApiError(404, "not_found", "No encontrado.")
    ctype = "video/mp4" if key.endswith(".mp4") else "application/pdf" if key.endswith(".pdf") else "application/octet-stream"
    headers = {"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"}
    safe = "".join(c for c in (fn or "") if c.isalnum() or c in "._- ")
    if safe:
        headers["Content-Disposition"] = f'attachment; filename="{safe}"'
    return FileResponse(p, media_type=ctype, headers=headers)      # soporta Range => reproducción/seek en <video>
