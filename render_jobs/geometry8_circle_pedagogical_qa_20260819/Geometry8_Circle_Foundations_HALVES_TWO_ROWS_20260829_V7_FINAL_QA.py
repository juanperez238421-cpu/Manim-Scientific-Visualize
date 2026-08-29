#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Foundations V7 FINAL QA.

This is a surgical projector-safe correction over the V7 master. The complete
pedagogical timeline, mathematical derivation, semicircle ownership and sector
motion are inherited unchanged. Only Step 05 is rebuilt so the two ownership
labels remain comfortably inside the 16:9 safe frame before the rows interlock.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps, literal -pqh.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_MASTER import (  # noqa: E402
    Geometry8CircleFoundationsHalvesTwoRows20260829V7Master,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    MID_GRAY,
    LIGHT_GRAY,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA(
    Geometry8CircleFoundationsHalvesTwoRows20260829V7Master
):
    """V7 master with final safe-frame correction for the interlock labels."""

    def step_5_interlock_halves_pair_first(self) -> None:
        h = self.header(
            5,
            "INTERLOCK ROW 1 AND ROW 2",
            "ROW 1 moves down and ROW 2 moves up. Their pre-aligned x-positions keep the motion clean and readable.",
        )
        self.add(h)

        n_total, r = 24, 2.00
        top_y, bottom_y = 0.78, -0.78
        row1, row2 = self.half_row_targets(n_total, r, top_y, bottom_y)
        target = self.strip_targets(n_total, r, center=np.array([0.0, -0.10, 0.0]))

        # FINAL QA: shorter ownership labels + a safer center position.
        # The ownership relationship was already established in Step 04, so these
        # compact labels reinforce it without competing with the sector geometry.
        row1_lab = self.text("ROW 1 · RIGHT HALF  ↓", 27, BOLD).move_to([-4.55, 1.55, 0])
        row2_lab = self.text("ROW 2 · LEFT HALF   ↑", 27, BOLD).move_to([-4.55, -1.55, 0])
        cue = self.text("FIRST: ONE MATCHED PAIR", 29, BOLD).move_to([0.0, -3.08, 0])

        self.assert_safe(
            VGroup(h, row1, row2, target, row1_lab, row2_lab, cue),
            "v7 final qa step5 interlock halves",
        )
        self.play(FadeIn(row1), FadeIn(row2), FadeIn(row1_lab), FadeIn(row2_lab), run_time=0.90)
        self.play(FadeIn(cue, shift=UP * 0.06), run_time=0.60)

        # Show one representative pair before repeating the mechanism globally.
        j = 5
        self.play(
            Indicate(row1[j], color=MID_GRAY, scale_factor=1.10),
            Indicate(row2[j], color=MID_GRAY, scale_factor=1.10),
            run_time=1.00,
        )
        self.wait(0.6)
        self.play(
            Transform(row1[j], target[2 * j]),
            Transform(row2[j], target[2 * j + 1]),
            run_time=1.65,
            rate_func=smooth,
        )
        self.wait(0.9)

        all_cue = self.text(
            "NOW REPEAT THE SAME VERTICAL MOTION WITH EVERY PAIR",
            28,
            BOLD,
        ).move_to(cue)
        self.play(Transform(cue, all_cue), run_time=0.55)

        order = sorted(
            [k for k in range(n_total // 2) if k != j],
            key=lambda k: abs(k - j),
        )
        animations = []
        for k in order:
            animations.append(Transform(row1[k], target[2 * k]))
            animations.append(Transform(row2[k], target[2 * k + 1]))

        self.play(
            LaggedStart(*animations, lag_ratio=0.035),
            FadeOut(row1_lab),
            FadeOut(row2_lab),
            run_time=3.20,
            rate_func=smooth,
        )
        self.play(FadeOut(cue), run_time=0.35)

        top_line = DashedLine(
            [-3.75, 0.90, 0], [3.75, 0.90, 0],
            color=LIGHT_GRAY, dash_length=0.10,
        )
        bottom_line = DashedLine(
            [-3.75, -1.10, 0], [3.75, -1.10, 0],
            color=LIGHT_GRAY, dash_length=0.10,
        )
        conserved = self.text(
            "SAME 24 PIECES  →  SAME TOTAL AREA",
            32,
            BOLD,
        ).move_to([0.0, -3.08, 0])
        self.play(
            Create(top_line),
            Create(bottom_line),
            FadeIn(conserved, shift=UP * 0.06),
            run_time=0.80,
        )
        self.wait(4.2)
        self.clear_stage(VGroup(h, row1, row2, top_line, bottom_line, conserved))


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_FINAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_FINAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA --disable_caching
