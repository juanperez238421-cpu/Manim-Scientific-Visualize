#!/usr/bin/env python3
"""Static acceptance checks for the ITM CAD Manim scene."""

from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCENE = ROOT / "house_extrusion_itm.py"
LOGO = ROOT / "assets" / "itm_logo.png"

EXPECTED_SCENES = {
    "HouseExtrusion3D",
    "HouseExtrusionITM_SEDTCAD22",
    "HouseExtrusionITM_DTR43",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not SCENE.is_file():
        fail(f"missing scene: {SCENE}")
    if not LOGO.is_file() or LOGO.stat().st_size < 1024:
        fail(f"missing or empty ITM logo: {LOGO}")

    source = SCENE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SCENE))
    class_names = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
    missing = EXPECTED_SCENES - class_names
    if missing:
        fail(f"missing scene classes: {sorted(missing)}")

    if re.search(r"(?<![A-Za-z])Text\s*\(", source):
        fail("Text(...) found; visible text must use Tex/MathTex")
    if "return Tex(" not in source:
        fail("LaTeX typography helper is missing")
    if source.count("Write(") < 10:
        fail("insufficient Write(...) calls for the textual narrative")
    if "closed_wall_profile" not in source or "wall_trace" not in source:
        fail("closed-wall croquis protocol is missing")
    if "enter_plan_croquis" not in source or "enter_front_face_croquis" not in source:
        fail("face-normal croquis camera states are missing")
    if "front_after_door" not in source or "front_final" not in source:
        fail("subtractive wall replacement states are missing")
    if "SEDTCAD22" not in source or "DTR43" not in source:
        fail("both ITM group codes must be present")

    forbidden = (r"[A-Za-z]:\\", "/Users/", "/home/")
    for marker in forbidden:
        if marker in source:
            fail(f"non-portable path marker found: {marker}")

    print("PASS: syntax, scenes, logo, LaTeX/Write, CAD grammar and portability")


if __name__ == "__main__":
    main()

