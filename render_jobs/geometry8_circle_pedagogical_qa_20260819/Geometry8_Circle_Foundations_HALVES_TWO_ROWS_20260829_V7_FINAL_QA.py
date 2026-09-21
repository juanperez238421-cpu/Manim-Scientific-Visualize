#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Foundations V7 FINAL QA.

Projector-safe corrections over the V7 master. The complete pedagogical timeline,
mathematical derivation, semicircle ownership and sector motion are inherited
unchanged. This QA subclass only rebuilds the interlock-label panel (Step 05)
and the base-measurement panel (Step 07) to keep every element inside the 16:9
safe frame while preserving the exact mathematics.

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
    """V7 master with final projector-safe corrections."""

    # ------------------------------------------------------------------
    # 05 — Interlock labels: compact ownership reinforcement
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # 07 — Base P/2, not P: compact projector-safe panel
    # ------------------------------------------------------------------
    def step_7_base_english(self) -> None:
        h = self.header(
            7,
            "THE BASE IS HALF THE PERIMETER",
            "Each row creates one opposite curved boundary of length P/2. A single base uses only ONE of those boundaries.",
        )
        self.add(h)

        n, r = 32, 2.05
        center = np.array([-1.15, -0.08, 0.0])
        strip = self.strip_targets(n, r, center=center)
        arcs_top, arcs_bottom = self.final_row_arc_overlays(n, r, center_y=-0.08)
        arcs_top.shift(LEFT * 1.15)
        arcs_bottom.shift(LEFT * 1.15)

        x0, x1 = strip.get_left()[0], strip.get_right()[0]
        base = DoubleArrow(
            [x0, -1.52, 0],
            [x1, -1.52, 0],
            color=BLACK,
            buff=0.02,
            tip_length=0.14,
            stroke_width=3.0,
        )
        base_lab = self.math(r"\text{base}=\frac{P}{2}=\pi r", 43).next_to(base, DOWN, buff=0.10)

        # Shorter labels preserve the exact statement while leaving generous
        # projector margins on the right-hand explanation column.
        row1 = self.text("ROW 1  =  P/2", 27, BOLD).move_to([4.65, 0.70, 0])
        row2 = self.text("ROW 2  =  P/2", 27, BOLD).move_to([4.65, -0.05, 0])
        choose = self.text("BASE = ONE boundary", 26, BOLD).move_to([4.55, -1.05, 0])
        notsum = self.text("Do not add both.", 24, BOLD).move_to([4.55, -1.48, 0])

        group = VGroup(
            strip,
            arcs_top,
            arcs_bottom,
            base,
            base_lab,
            row1,
            row2,
            choose,
            notsum,
            h,
        )
        self.assert_safe(group, "v7 final qa step7 base")

        self.play(FadeIn(strip), run_time=0.80)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.035),
            FadeIn(row1, shift=LEFT * 0.08),
            run_time=1.15,
        )
        self.wait(1.0)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.035),
            FadeIn(row2, shift=LEFT * 0.08),
            run_time=1.15,
        )
        self.wait(1.1)
        self.play(GrowFromCenter(base), Write(base_lab), run_time=1.10)
        self.play(
            FadeIn(choose, shift=UP * 0.05),
            FadeIn(notsum, shift=UP * 0.05),
            run_time=0.75,
        )
        self.play(Indicate(base_lab, color=MID_GRAY, scale_factor=1.03), run_time=0.90)
        self.wait(4.8)
        self.clear_stage(group)


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_FINAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_FINAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA --disable_caching
