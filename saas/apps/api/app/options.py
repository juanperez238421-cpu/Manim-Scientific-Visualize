"""Fuente ÚNICA de opciones válidas: /v1/render-options las publica y la validación las usa."""
from __future__ import annotations

from .auth import Plan

LANGUAGES = ["es"]                                   # i18n futura: "en"
KINDS = ["solution_video", "hybrid_lesson"]
DETAIL_LEVELS = ["brief", "standard", "detailed"]
RESOLUTIONS = ["480p", "720p", "1080p"]              # orden ascendente
MIN_TARGET_SECONDS = 10


def allowed_resolutions(plan: Plan) -> list[str]:
    return RESOLUTIONS[: RESOLUTIONS.index(plan.max_resolution) + 1]


def render_options(plan: Plan) -> dict:
    return {
        "languages": LANGUAGES,
        "kinds": [
            {"kind": "solution_video", "prologue_allowed": False},
            {"kind": "hybrid_lesson", "prologue_allowed": plan.allows_prologue},
        ],
        "detail_levels": DETAIL_LEVELS,
        "resolutions": allowed_resolutions(plan),
        "target_seconds": {"min": MIN_TARGET_SECONDS, "max": plan.max_video_seconds},
        "limits": {"max_pdf_pages": plan.max_pdf_pages, "max_pdf_bytes": plan.max_pdf_bytes,
                   "max_concurrent_jobs": plan.max_concurrent_jobs},
        "voices": [],                                # sin narración disponible todavía: no suponer voces
    }
