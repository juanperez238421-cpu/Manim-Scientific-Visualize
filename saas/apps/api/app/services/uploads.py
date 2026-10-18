from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from ..auth import CurrentUser
from ..errors import ApiError
from ..pdf import InvalidPdf, analyze_pdf


def init_upload(conn, store, user: CurrentUser, filename: str, size: int, sha256: str, ttl: int) -> dict:
    if not filename.lower().endswith(".pdf"):
        raise ApiError(422, "invalid_pdf", "Solo se aceptan archivos .pdf.", {"reason": "bad_extension"})
    if size > user.plan.max_pdf_bytes:
        raise ApiError(422, "invalid_pdf", "El archivo excede el tamaño de tu plan.",
                       {"reason": "too_large", "max_bytes": user.plan.max_pdf_bytes})
    file_id = uuid4()
    key = f"users/{user.id}/pdfs/{file_id}.pdf"           # la clave NO contiene el nombre del cliente
    safe_name = re.sub(r"[^\w.\- ]", "_", filename)[:255]
    expires = datetime.now(timezone.utc) + timedelta(seconds=ttl)
    conn.execute(
        """INSERT INTO pdf_files(id, user_id, original_name, storage_key, size_bytes, declared_sha256,
                                 upload_expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (file_id, user.id, safe_name, key, size, sha256.lower(), expires))
    url, headers = store.presign_put(key, "application/pdf", ttl)
    return {"file_id": file_id, "upload_url": url, "method": "PUT", "headers": headers, "expires_at": expires}


def complete_upload(conn, store, user: CurrentUser, file_id) -> dict:
    row = conn.execute("SELECT * FROM pdf_files WHERE id=%s AND user_id=%s AND deleted_at IS NULL FOR UPDATE",
                       (file_id, user.id)).fetchone()
    if row is None:
        raise ApiError(404, "not_found", "PDF no encontrado.")
    if row["status"] == "analyzed":                        # idempotente
        return _resp(row)
    if row["status"] == "rejected":
        raise ApiError(422, "invalid_pdf", "El PDF fue rechazado.", {"reason": row["reject_reason"]})
    if row["upload_expires_at"] and row["upload_expires_at"] < datetime.now(timezone.utc):
        raise ApiError(409, "upload_expired", "La URL de subida expiró; inicia de nuevo.")
    size = store.head(row["storage_key"])
    if size is None:
        raise ApiError(409, "upload_incomplete", "Aún no se subió el archivo.")
    if size > user.plan.max_pdf_bytes:
        return _reject(conn, store, row, "too_large")
    data = store.get_bytes(row["storage_key"], user.plan.max_pdf_bytes)
    try:
        a = analyze_pdf(data, declared_size=row["size_bytes"], declared_sha256=row["declared_sha256"],
                        max_pages=user.plan.max_pdf_pages)
    except InvalidPdf as e:
        return _reject(conn, store, row, e.reason)
    row = conn.execute(
        """UPDATE pdf_files SET status='analyzed', sha256=%s, page_count=%s, has_text_layer=%s,
                  ocr_required=%s, analysis=%s WHERE id=%s RETURNING *""",
        (a.sha256, a.page_count, a.has_text_layer, not a.has_text_layer,
         psycopg_json({"pages": a.page_count, "has_text_layer": a.has_text_layer}), file_id)).fetchone()
    return _resp(row)


def psycopg_json(v):
    from psycopg.types.json import Jsonb
    return Jsonb(v)


def _reject(conn, store, row, reason: str):
    conn.execute("UPDATE pdf_files SET status='rejected', reject_reason=%s WHERE id=%s", (reason, row["id"]))
    try:
        store.delete(row["storage_key"])
    except Exception:
        pass
    # el rechazo debe persistir aunque respondamos 422: se confirma antes de lanzar
    conn.commit()
    raise ApiError(422, "invalid_pdf", "El documento fue rechazado.", {"reason": reason})


def _resp(row) -> dict:
    return {"file_id": row["id"], "status": "analyzed", "page_count": row["page_count"],
            "has_text_layer": bool(row["has_text_layer"]), "ocr_required": row["ocr_required"],
            "sha256": row["sha256"]}
