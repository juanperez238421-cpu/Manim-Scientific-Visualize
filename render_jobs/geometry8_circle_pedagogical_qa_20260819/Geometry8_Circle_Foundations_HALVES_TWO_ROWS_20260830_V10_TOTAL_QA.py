#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V10 TOTAL QA.

Human-frame-driven refinement of V9 PROJECTOR MAX. The principal V9 defect was
Step 04: source-half labels, ownership labels and moving sectors could occupy the
same visual corridor during the half-to-row transformation. V10 treats that as
an animation-lifecycle problem rather than shrinking the typography.

The final V10 pass also removes transient sector pileups and lowers the complete
row/measurement system so the top P/2 = pi r annotation never enters the header
subtitle band.

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
    """V10: clean staged ownership, large readable labels, professional holds."""

    PAUSE_SCALE = 1.40

    def _row_owner_tag(self, row_name: str, owner: str, center) -> VGroup:
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
        """Step 04 with isolated source phases, clean lanes and header-safe measures."""
        h = self.header(
            4,
            "FORM TWO SEPARATE ROWS — ONE ROW FROM EACH HALF",
            "Build one row at a time. Keep ownership labels outside the sector lanes, then measure each row separately.",
        )
        self.add(h)

        n_total = 24

        # A. Source halves are shown only during ownership identification.
        source_r = 1.48
        source_center = np.array([0.0, -0.34, 0.0])
        _, right_source, left_source = self.vertical_half_sectors(
            n_total, source_r, source_center
        )
        right_source.shift(RIGHT * 0.46)
        left_source.shift(LEFT * 0.46)
        source_r_lab = self.text("RIGHT HALF", 30, BOLD).move_to([2.55, 1.36, 0])
        source_l_lab = self.text("LEFT HALF", 30, BOLD).move_to([-2.55, 1.36, 0])

        # B. Final row system. First move right for a wide ownership corridor,
        # then lower the entire system 0.42 units to keep the top measurement
        # formula completely below the subtitle band.
        row_r = 1.62
        top_y, bottom_y = 0.66, -0.66
        row1, row2 = self.half_row_targets(n_total, row_r, top_y, bottom_y)
        top_arcs, bottom_arcs = self.half_row_arc_overlays(
            n_total, row_r, top_y, bottom_y
        )
        measures = self.row_measurements_from_halves(
            row1, row2, row_r, top_y, bottom_y
        )
        row_system = VGroup(row1, row2, top_arcs, bottom_arcs, measures)
        row_system.shift(RIGHT * 0.95)
        row_system.shift(DOWN * 0.42)

        row1_tag = self._row_owner_tag("ROW 1", "RIGHT HALF", [-5.48, 0.78, 0])
        row2_tag = self._row_owner_tag("ROW 2", "LEFT HALF", [-5.48, -0.78, 0])
        VGroup(row1_tag, row2_tag).shift(DOWN * 0.42)

        gap1 = self._horizontal_gap(row1_tag, row1)
        gap2 = self._horizontal_gap(row2_tag, row2)
        if gap1 < 0.62 or gap2 < 0.62:
            raise ValueError(
                f"V10 Step04 ownership corridor too small: gap1={gap1:.3f}, gap2={gap2:.3f}"
            )

        left_stage = left_source.copy().scale(0.82).move_to([0.55, -2.12, 0])
        left_stage_lab = self.text("LEFT HALF", 27, BOLD).next_to(
            left_stage, DOWN, buff=0.12
        )

        preflight = VGroup(
            h,
            right_source,
            left_source,
            source_r_lab,
            source_l_lab,
            row1,
            row2,
            row1_tag,
            row2_tag,
            top_arcs,
            bottom_arcs,
            measures,
            left_stage,
            left_stage_lab,
        )
        self.projector_safe(preflight, "v10 final step04 staged layout")

        # C. Identify both halves.
        self.play(
            FadeIn(right_source),
            FadeIn(left_source),
            FadeIn(source_r_lab, shift=UP * 0.06),
            FadeIn(source_l_lab, shift=UP * 0.06),
            run_time=1.10,
        )
        self.wait(1.80)

        # D. Focus RIGHT HALF, then clear all source geometry before row 1 appears.
        self.play(
            Indicate(right_source, scale_factor=1.025, color=GRAY),
            left_source.animate.set_opacity(0.22),
            run_time=0.90,
        )
        self.wait(0.80)
        self.play(
            FadeOut(source_r_lab),
            FadeOut(source_l_lab),
            FadeOut(left_source),
            run_time=0.62,
        )
        self.play(FadeOut(right_source, shift=UP * 0.10), run_time=0.72)
        self.wait(0.55)

        # E. Reveal ROW 1 directly in its final lane.
        self.play(
            LaggedStart(
                *[FadeIn(row1[j], shift=DOWN * 0.14) for j in range(n_total // 2)],
                lag_ratio=0.055,
            ),
            run_time=1.95,
        )
        self.play(FadeIn(row1_tag, shift=RIGHT * 0.08), run_time=0.72)
        self.wait(2.30)

        # F. Re-establish LEFT HALF in an isolated lower stage.
        self.play(
            FadeIn(left_stage, shift=UP * 0.06),
            FadeIn(left_stage_lab, shift=UP * 0.04),
            run_time=0.90,
        )
        self.wait(1.20)
        self.play(Indicate(left_stage, scale_factor=1.025, color=GRAY), run_time=0.82)
        self.wait(0.72)
        self.play(
            FadeOut(left_stage_lab),
            FadeOut(left_stage, shift=DOWN * 0.10),
            run_time=0.68,
        )
        self.wait(0.55)

        # G. Reveal ROW 2 directly in its final lane.
        self.play(
            LaggedStart(
                *[FadeIn(row2[j], shift=UP * 0.14) for j in range(n_total // 2)],
                lag_ratio=0.055,
            ),
            run_time=1.95,
        )
        self.play(FadeIn(row2_tag, shift=RIGHT * 0.08), run_time=0.72)
        self.wait(2.45)

        # H. Measure ROW 1 only.
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
        self.wait(2.55)
        self.play(
            FadeOut(top_arcs),
            FadeOut(measures[0]), FadeOut(measures[1]),
            FadeOut(measures[4]), FadeOut(measures[5]),
            run_time=0.70,
        )
        self.wait(0.70)

        # I. Measure ROW 2 only.
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
        self.wait(2.65)
        self.play(
            FadeOut(bottom_arcs),
            FadeOut(measures[2]), FadeOut(measures[3]),
            FadeOut(measures[6]), FadeOut(measures[7]),
            run_time=0.70,
        )
        self.wait(0.80)

        # J. Final clean checkpoint.
        checkpoint = self.big_formula(
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}",
            10.55,
            47,
        ).move_to([0.55, -3.03, 0])
        self.projector_safe(checkpoint, "v10 step04 final checkpoint")
        self.play(FadeIn(checkpoint, shift=UP * 0.07), run_time=0.95)
        self.play(Circumscribe(checkpoint[1], color=GRAY, time_width=0.90), run_time=1.20)
        self.wait(5.20)

        self.clear_stage(VGroup(h, row1, row2, row1_tag, row2_tag, checkpoint))

        if self.mobjects:
            residuals = list(self.mobjects)
            self.play(*[FadeOut(m) for m in residuals], run_time=0.35)
        if self.mobjects:
            raise ValueError("V10 Step04 lifecycle boundary is not empty")


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V10_TOTAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V10_TOTAL_QA.py Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA --disable_caching
