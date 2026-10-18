"""Validación y análisis de PDFs subidos (datos NO confiables)."""
from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass

from pypdf import PdfReader


class InvalidPdf(Exception):
    def __init__(self, reason: str):
        self.reason = reason


@dataclass(frozen=True)
class PdfAnalysis:
    sha256: str
    page_count: int
    has_text_layer: bool


def analyze_pdf(data: bytes, *, declared_size: int, declared_sha256: str, max_pages: int) -> PdfAnalysis:
    if len(data) != declared_size:
        raise InvalidPdf("size_mismatch")
    if not data.startswith(b"%PDF-"):
        raise InvalidPdf("not_a_pdf")
    digest = hashlib.sha256(data).hexdigest()
    if digest != declared_sha256.lower():
        raise InvalidPdf("sha256_mismatch")
    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            raise InvalidPdf("encrypted")
        pages = len(reader.pages)
        if pages < 1:
            raise InvalidPdf("empty")
        if pages > max_pages:
            raise InvalidPdf("too_many_pages")
        has_text = any((reader.pages[i].extract_text() or "").strip() for i in range(min(pages, 5)))
    except InvalidPdf:
        raise
    except Exception:
        raise InvalidPdf("corrupt")
    return PdfAnalysis(digest, pages, has_text)
