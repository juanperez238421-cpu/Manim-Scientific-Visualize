#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V10 TOTAL QA.

Human-frame-driven refinement of V9 PROJECTOR MAX.  The principal V9 defect was
Step 04: source-half labels, ownership labels and moving sectors could occupy the
same visual corridor during the half-to-row transformation.  V10 treats that as
an animation-lifecycle problem rather than shrinking the typography.

V10 goals
---------
* preserve the large projector-first V9 typography;
* remove Step-04 label/sector overlap at every animation phase;
* separate ownership labels from the sector rows with an explicit safety gap;
* measure one row at a time instead of stacking measurement graphics;
* use deliberate classroom holds between conceptual checkpoints;
* keep all V8/V9 lifecycle, projector-edge and mathematical QA protections.

Target: ManimCE 0.20.1, literal -pqh, 1920x1080, 30 fps.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V9_PROJECTOR_MAX import (
    Geometry8CircleFoundationsHalvesTwoRows20260830V9ProjectorMax,
)


class Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA(
    Geometry8CircleFoundationsHalvesTwoRows20260830V9ProjectorMax
):
    """V10: clean staged ownership, larger readable labels, professional holds."""

    # A modest global pause increase keeps the whole lesson copy-friendly while
    # the Step-04 override below uses purpose-built checkpoint waits.
    PAUSE_SCALE = 1.40

    def _row_owner_tag(self, row_name: str, owner: str, center) -> VGroup:
        """Compact two-line ownership tag that never intrudes into row geometry."""
        box = RoundedRectangle(
            width=2.78,
            height=1.02,
            corner_radius=0.13,
            stroke_color=BLACK,
            stroke_width=2.20,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        top = self.text(row_name, 34, BOLD)
        bottom = self.text(owner, 26, BOLD)
        copy = VGroup(top, bottom).arrange(DOWN, buff=0.035)
        if copy.width > 2.32:
            copy.scale_to_fit_width(2.32)
        copy.move_to(box)
        return VGroup(box, copy).move_to(center)

    @staticmethod
    def _horizontal_gap(left_mob: Mobject, right_mob: Mobject) -> float:
        return float(right_mob.get_left()[0] - left_mob.get_right()[0])

    def step_4_two_separate_rows_from_halves(self) -> None:
        """Rebuild Step 04 so labels and moving sectors never share a corridor."""
        h = self.header(
            4,
            "FORM TWO SEPARATE ROWS — ONE ROW FROM EACH HALF",
            "Build one row at a time. Keep each ownership label outside the moving sectors, then measure each row separately.",
        )
        self.add(h)

        n_total = 24

        # -------------------- A. clean source-halves stage --------------------
        source_r = 1.48
        source_center = np.array([0.0, -0.34, 0.0])
        _, right_source, left_source = self.vertical_half_sectors(
            n_total, source_r, source_center
        )
        right_source.shift(RIGHT * 0.46)
        left_source.shift(LEFT * 0.46)

        source_r_lab = self.text("RIGHT HALF", 30, BOLD).move_to([2.55, 1.36, 0])
        source_l_lab = self.text("LEFT HALF", 30, BOLD).move_to([-2.55, 1.36, 0])

        # -------------------- B. final row targets ----------------------------
        row_r = 1.62
        top_y, bottom_y = 0.66, -0.66
        row1, row2 = self.half_row_targets(n_total, row_r, top_y, bottom_y)
        top_arcs, bottom_arcs = self.half_row_arc_overlays(
            n_total, row_r, top_y, bottom_y
        )
        measures = self.row_measurements_from_halves(
            row1, row2, row_r, top_y, bottom_y
        )

        # V10 uses canvas whitespace instead of shrinking text.  Moving the
        # complete row system right creates a stable label-to-geometry corridor.
        VGroup(row1, row2, top_arcs, bottom_arcs, measures).shift(RIGHT * 0.95)

        row1_tag = self._row_owner_tag("ROW 1", "RIGHT HALF", [-5.48, 0.78, 0])
        row2_tag = self._row_owner_tag("ROW 2", "LEFT HALF", [-5.48, -0.78, 0])

        gap1 = self._horizontal_gap(row1_tag, row1)
        gap2 = self._horizontal_gap(row2_tag, row2)
        if gap1 < 0.62 or gap2 < 0.62:
            raise ValueError(
                f"V10 Step04 ownership corridor too small: gap1={gap1:.3f}, gap2={gap2:.3f}"
            )

        group = VGroup(
            h,
            right_source,
            left_source,
            source_r_lab,
            source_l_lab,
            row1_tag,
            row2_tag,
            top_arcs,
            bottom_arcs,
            measures,
        )
        self.projector_safe(group, "v10 step04 staged layout")

        # -------------------- C. source inspection ----------------------------
        self.play(
            FadeIn(right_source),
            FadeIn(left_source),
            FadeIn(source_r_lab, shift=UP * 0.06),
            FadeIn(source_l_lab, shift=UP * 0.06),
            run_time=1.10,
        )
        self.wait(1.70)

        # Focus right half.  Crucially, BOTH source labels are removed before
        # any sector starts moving.  This eliminates the V9 transition overlap.
        self.play(
            Indicate(right_source, scale_factor=1.025, color=GRAY),
            left_source.animate.set_opacity(0.22),
            run_time=0.90,
        )
        self.wait(0.75)
        self.play(FadeOut(source_r_lab), FadeOut(source_l_lab), run_time=0.55)
        self.wait(0.45)

        # -------------------- D. right half -> row 1 --------------------------
        self.play(
            AnimationGroup(
                *[
                    Transform(right_source[j], row1[j])
                    for j in range(n_total // 2)
                ],
                lag_ratio=0.052,
            ),
            run_time=2.70,
            rate_func=smooth,
        )
        self.wait(1.15)
        self.play(FadeIn(row1_tag, shift=RIGHT * 0.08), run_time=0.72)
        self.wait(2.05)

        # -------------------- E. left half -> row 2 ---------------------------
        self.play(left_source.animate.set_opacity(1.0), run_time=0.55)
        self.play(
            Indicate(left_source, scale_factor=1.025, color=GRAY),
            run_time=0.80,
        )
        self.wait(0.70)
        self.play(
            AnimationGroup(
                *[
                    Transform(left_source[j], row2[j])
                    for j in range(n_total // 2)
                ],
                lag_ratio=0.052,
            ),
            run_time=2.70,
            rate_func=smooth,
        )
        self.wait(1.15)
        self.play(FadeIn(row2_tag, shift=RIGHT * 0.08), run_time=0.72)
        self.wait(2.35)

        # -------------------- F. measure ROW 1 only ---------------------------
        self.play(
            LaggedStart(*[Create(a) for a in top_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[0]),
            Write(measures[1]),
            GrowFromCenter(measures[4]),
            Write(measures[5]),
            run_time=1.20,
        )
        self.wait(2.45)
        self.play(
            FadeOut(top_arcs),
            FadeOut(measures[0]), FadeOut(measures[1]),
            FadeOut(measures[4]), FadeOut(measures[5]),
            run_time=0.70,
        )
        self.wait(0.65)

        # -------------------- G. measure ROW 2 only ---------------------------
        self.play(
            LaggedStart(*[Create(a) for a in bottom_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[2]),
            Write(measures[3]),
            GrowFromCenter(measures[6]),
            Write(measures[7]),
            run_time=1.20,
        )
        self.wait(2.55)
        self.play(
            FadeOut(bottom_arcs),
            FadeOut(measures[2]), FadeOut(measures[3]),
            FadeOut(measures[6]), FadeOut(measures[7]),
            run_time=0.70,
        )
        self.wait(0.75)

        # -------------------- H. clean mathematical checkpoint ----------------
        checkpoint = self.big_formula(
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}",
            10.55,
            47,
        ).move_to([0.55, -3.03, 0])
        self.projector_safe(checkpoint, "v10 step04 final checkpoint")
        self.play(FadeIn(checkpoint, shift=UP * 0.07), run_time=0.95)
        self.play(Circumscribe(checkpoint[1], color=GRAY, time_width=0.90), run_time=1.20)
        self.wait(5.10)

        self.clear_stage(
            VGroup(h, right_source, left_source, row1_tag, row2_tag, checkpoint)
        )

        if self.mobjects:
            residuals = list(self.mobjects)
            self.play(*[FadeOut(m) for m in residuals], run_time=0.35)
        if self.mobjects:
            raise ValueError("V10 Step04 lifecycle boundary is not empty")


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V10_TOTAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V10_TOTAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA --disable_caching
