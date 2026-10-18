"""Estimador de créditos. TARIFAS BORRADOR (no aprobadas): se calibrarán con el benchmark."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any

PRICING_VERSION = "draft-0.1"
WEIGHTS = {"svg": 0.5, "manim": 1.0, "threejs": 2.5}          # créditos por segundo
RESOLUTION_MULT = {"480p": 0.5, "720p": 0.75, "1080p": 1.0}
OCR_CREDITS_PER_PAGE = 1.0
PROLOGUE_SECONDS = 30
MAX_HEADROOM = 1.25                                            # max_credits = ceil(estimado * 1.25)


def split_seconds(kind: str, target: int, include_prologue: bool) -> dict[str, float]:
    if kind == "solution_video":           # página -> solución -> página: Manim + anotaciones SVG
        return {"manim": 0.7 * target, "svg": 0.3 * target}
    pro = min(PROLOGUE_SECONDS, 0.5 * target) if include_prologue else 0
    rest = target - pro
    out = {"manim": 0.75 * rest, "svg": 0.25 * rest}
    if pro:
        out["threejs"] = pro
    return out


def estimate(kind: str, target_seconds: int, include_prologue: bool, resolution: str,
             ocr_pages: int) -> dict[str, Any]:
    seconds = split_seconds(kind, target_seconds, include_prologue)
    mult = RESOLUTION_MULT[resolution]
    engines = {e: round(s * WEIGHTS[e] * mult, 4) for e, s in seconds.items()}
    ocr = ocr_pages * OCR_CREDITS_PER_PAGE
    total = math.ceil(sum(engines.values()) + ocr - 1e-9)
    total = max(total, 1)
    return {
        "estimated_credits": total,
        "max_credits": math.ceil(total * MAX_HEADROOM),
        "estimated_seconds": target_seconds,
        "breakdown": {"seconds": seconds, "credits_by_engine": engines, "ocr_credits": ocr,
                      "resolution_multiplier": mult, "weights": WEIGHTS},
    }


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def sha256_hex(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def estimate_hash(pdf_id: str, kind: str, config: dict, est: dict, pricing_version: str) -> str:
    return sha256_hex({"pdf": pdf_id, "kind": kind, "config": config,
                       "estimated": est["estimated_credits"], "max": est["max_credits"],
                       "pricing": pricing_version})
