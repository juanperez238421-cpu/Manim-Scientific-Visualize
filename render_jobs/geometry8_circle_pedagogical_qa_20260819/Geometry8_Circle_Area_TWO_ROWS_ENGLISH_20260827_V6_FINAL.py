#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Area V6 FINAL ENGLISH.

Final safe-layout refinement of the V6 English masterclass. The only override
is Step 07, whose right-side explanatory copy is pulled inward after the PQL
safe-frame gate correctly detected a horizontal overflow in the master draft.
All enlarged figures, improved pauses, English copy and animation timing from
V6 Master are preserved.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_TWO_ROWS_ENGLISH_20260827_V6_MASTER import (  # noqa: E402
    Geometry8CircleAreaTwoRowsEnglish20260827V6Master,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import MID_GRAY  # noqa: E402


class Geometry8CircleAreaTwoRowsEnglish20260827V6Final(Geometry8CircleAreaTwoRowsEnglish20260827V6Master):
    """Audited V6 English lesson with safe Step-07 composition."""

    def step_7_base_english(self) -> None:
        h = self.header(
            7,
            "THE BASE IS HALF THE PERIMETER",
            "ROW 1 forms one long boundary and ROW 2 forms the opposite boundary; one base uses only one of them.",
        )
        self.add(h)

        n, r = 32, 1.90
        center_x = -1.55
        strip = self.strip_targets(n, r, center=np.array([center_x, -0.08, 0.0]))
        arcs_top, arcs_bottom = self.final_row_arc_overlays(n, r, center_y=-0.08)
        arcs_top.shift(RIGHT * center_x)
        arcs_bottom.shift(RIGHT * center_x)

        x0, x1 = strip.get_left()[0], strip.get_right()[0]
        base = DoubleArrow(
            [x0, -1.45, 0], [x1, -1.45, 0],
            color=BLACK, buff=0.02, tip_length=0.14, stroke_width=3.0,
        )
        base_lab = self.math(r"\text{base}=\frac{P}{2}=\pi r", 45).next_to(base, DOWN, buff=0.10)

        row1 = self.text("ROW 1 boundary = P/2", 25, BOLD).move_to([4.30, 0.72, 0])
        row2 = self.text("ROW 2 boundary = P/2", 25, BOLD).move_to([4.30, -0.12, 0])
        notsum = self.text(
            "Choose ONE boundary for the base — do not add them.",
            24,
            BOLD,
        ).move_to([2.75, -2.58, 0])

        group = VGroup(strip, arcs_top, arcs_bottom, base, base_lab, row1, row2, notsum, h)
        self.assert_safe(group, "v6 final step7")

        self.play(FadeIn(strip), run_time=0.85)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.035),
            FadeIn(row1, shift=LEFT * 0.08),
            run_time=1.20,
        )
        self.wait(1.2)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.035),
            FadeIn(row2, shift=LEFT * 0.08),
            run_time=1.20,
        )
        self.wait(1.3)
        self.play(GrowFromCenter(base), Write(base_lab), run_time=1.15)
        self.play(FadeIn(notsum, shift=UP * 0.06), run_time=0.75)
        self.wait(5.2)
        self.clear_stage(group)


# Preview:
#   LESSON_TIME_SCALE=0.08 manim -pql Geometry8_Circle_Area_TWO_ROWS_ENGLISH_20260827_V6_FINAL.py Geometry8CircleAreaTwoRowsEnglish20260827V6Final --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_TWO_ROWS_ENGLISH_20260827_V6_FINAL.py Geometry8CircleAreaTwoRowsEnglish20260827V6Final --disable_caching
