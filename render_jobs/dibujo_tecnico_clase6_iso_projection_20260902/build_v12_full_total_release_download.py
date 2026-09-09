#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the full V12 scene from the V11 stepwise-view director version.

V12 is deliberately conservative in geometry: the validated V11 projection
construction is retained, while pacing is tightened slightly and delivery is
moved to a GitHub Release asset that CI re-downloads byte-for-byte.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
V11_BUILDER = ROOT / "build_v11_stepwise_views.py"
V11_SRC = ROOT / "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V11_STEPWISE_VIEWS_DIRECTOR_QA.py"
V12_SRC = ROOT / "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V12_FULL_TOTAL_RELEASE_DOWNLOAD.py"

# Rebuild V11 deterministically from its validated V9/V10 lineage first.
runpy.run_path(str(V11_BUILDER), run_name="__main__")
assert V11_SRC.exists() and V11_SRC.stat().st_size > 10000
s = V11_SRC.read_text(encoding="utf-8")

# Promote all internal V11 labels/constants to V12.
s = s.replace("V11", "V12")

# Give the class a delivery-oriented V12 identity while retaining the same
# pedagogical geometry and the sequential front/top/right construction.
s = s.replace(
    "class Projection3Dto2DV12StepwiseViewsDirectorQA",
    "class Projection3Dto2DV12FullTotalReleaseDownload",
)
s = s.replace(
    "Projection3Dto2DV12StepwiseViewsDirectorQA",
    "Projection3Dto2DV12FullTotalReleaseDownload",
)

# V11 used a 1.25 classroom multiplier. V12 keeps the deliberate pauses but
# trims dead time slightly so the flow remains readable without feeling static.
s = s.replace("V12_GLOBAL_PACE = 1.25", "V12_GLOBAL_PACE = 1.20")

# Make the new construction studio visually/version-identifiable. This also
# guarantees the V12 video is a true fresh render rather than a renamed V11.
s = s.replace(
    'Text("CONSTRUCCIÓN 2D · UNA VISTA A LA VEZ", font_size=36, color=INK, weight=BOLD)',
    'Text("CONSTRUCCIÓN 2D · UNA VISTA A LA VEZ · V12", font_size=35, color=INK, weight=BOLD)',
)

# Update generated header language if present.
s = s.replace(
    "V12 goals:",
    "V12 full-total goals:",
)

required = [
    "class Projection3Dto2DV12FullTotalReleaseDownload",
    "V12_GLOBAL_PACE = 1.20",
    "FOLD_EXTRA_UPSHIFT = 1.20",
    "CONSTRUCCIÓN 2D · UNA VISTA A LA VEZ · V12",
    "ALZADO · PASO 1/3",
    "PLANTA · PASO 3/3",
    "PERFIL · PASO 3/3",
    "front_card.animate.scale(0.50).move_to",
    "top_card.animate.scale(0.50).move_to",
    "right_card.animate.scale(0.50).move_to",
    "UN OBJETO · TRES DESCRIPCIONES 2D",
]
missing = [x for x in required if x not in s]
assert not missing, f"V12 required markers missing: {missing}"
assert "Projection3Dto2DV11StepwiseViewsDirectorQA" not in s

V12_SRC.write_text(s, encoding="utf-8")
print(f"WROTE {V12_SRC}")
print(f"BYTES {V12_SRC.stat().st_size}")
print("V12_BUILDER_STATIC_QA=PASS")
