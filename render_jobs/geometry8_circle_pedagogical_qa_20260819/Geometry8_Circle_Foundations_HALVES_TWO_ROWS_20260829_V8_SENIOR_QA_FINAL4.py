#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V8 SENIOR QA — FINAL4.

Final human contact-sheet micro-layout pass after FINAL3:
1) separate CENTER and diameter label d in Step 01;
2) increase horizontal clearance between Step-04 ownership labels and sectors;
3) separate the Step-07 base equation from the ONE-base conclusion panel.

No typography is reduced.  The fixes use spatial redistribution only.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL3 import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal3,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (
    MID_GRAY, PAPER,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal4(
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal3
):
    """Final projector-first scene after frame-level human QA."""

    def step_1_circle_parts_and_pi(self) -> None:
        h = self.header(
            1,
            "CIRCLE PARTS: PERIMETER, DIAMETER AND RADIUS",
            "Identify the geometry first. Then use the constant ratio P ÷ d = π to derive the circumference formula.",
        )
        self.add(h)

        center = np.array([-3.55, -0.22, 0.0])
        r = 2.48
        circle = Circle(radius=r, color=BLACK, stroke_width=4.8).move_to(center)
        dot = Dot(center, radius=0.085, color=BLACK)

        perimeter_lab = self.text("PERIMETER  P", 32, BOLD).move_to([-3.55, 2.56, 0])
        perimeter_arrow = Arrow(
            [-3.55, 2.30, 0], center + UP * r * 0.99,
            color=MID_GRAY, stroke_width=2.8, tip_length=0.15,
        )

        diameter = DoubleArrow(
            center + LEFT * r, center + RIGHT * r,
            color=BLACK, buff=0.03, tip_length=0.17, stroke_width=3.3,
        )
        # FINAL4: move d slightly right/down and CENTER further left/down.
        # This keeps both labels large while creating an explicit visual gap.
        d_lab = self.math("d", 50).move_to(center + np.array([0.52, -0.58, 0]))

        theta = 42 * DEGREES
        r_end = center + r * np.array([np.cos(theta), np.sin(theta), 0.0])
        radius = Arrow(
            center, r_end, buff=0.0,
            color=MID_GRAY, stroke_width=3.5, tip_length=0.18,
        )
        r_lab = self.math("r", 50).move_to(center + np.array([1.18, 1.35, 0]))
        center_lab = self.text("CENTER", 24, BOLD).move_to(
            center + np.array([-0.88, -0.42, 0])
        )

        definition = self.text("THE DEFINITION OF π", 32, BOLD).move_to([3.72, 2.24, 0])
        eq_box = RoundedRectangle(
            width=5.55, height=1.42, corner_radius=0.14,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=PAPER, fill_opacity=1,
        ).move_to([3.72, 1.08, 0])
        eq = self.math(r"\pi=\frac{P}{d}", 62).move_to(eq_box)

        relation = self.big_formula(r"d=2r", 4.35, 56).move_to([3.72, -0.68, 0])
        conclusion = self.big_formula(
            r"P=\pi(2r)=2\pi r", 5.95, 56
        ).move_to([3.72, -2.42, 0])

        group = VGroup(
            h, circle, dot, perimeter_lab, perimeter_arrow,
            diameter, d_lab, radius, r_lab, center_lab,
            definition, eq_box, eq, relation, conclusion,
        )
        self.projector_safe(group, "v8 final4 step1")

        self.play(Create(circle), FadeIn(dot), run_time=1.15)
        self.play(
            ShowPassingFlash(circle.copy().set_stroke(MID_GRAY, width=8), time_width=0.8),
            FadeIn(perimeter_lab, shift=UP * 0.06),
            GrowArrow(perimeter_arrow),
            run_time=1.45,
        )
        self.wait(1.3)
        self.play(GrowFromCenter(diameter), Write(d_lab), run_time=1.05)
        self.wait(1.1)
        self.play(
            GrowArrow(radius), Write(r_lab), FadeIn(center_lab, shift=RIGHT * 0.05),
            run_time=1.05,
        )
        self.wait(1.9)

        self.play(FadeIn(definition), FadeIn(eq_box), Write(eq), run_time=1.15)
        self.wait(2.0)
        eq2 = self.math(r"P=\pi d", 62).move_to(eq_box)
        # Use Transform on the same source object so cleanup retains identity.
        self.play(Transform(eq, eq2), run_time=1.10)
        self.wait(1.9)
        self.play(FadeIn(relation, shift=LEFT * 0.08), run_time=0.95)
        self.wait(1.8)
        self.play(FadeIn(conclusion, shift=LEFT * 0.08), run_time=1.05)
        self.play(Circumscribe(conclusion[1], color=MID_GRAY, time_width=0.8), run_time=1.20)
        self.wait(4.8)
        self.clear_stage(group)

        if self.mobjects:
            residuals = list(self.mobjects)
            self.play(*[FadeOut(m) for m in residuals], run_time=0.40)
        if self.mobjects:
            raise ValueError("FINAL4 Step 01 lifecycle boundary is not empty")

    def step_4_two_separate_rows_from_halves(self) -> None:
        h = self.header(
            4,
            "FORM TWO SEPARATE ROWS — ONE ROW FROM EACH HALF",
            "Do not combine them yet. Build the two rows independently, then measure each row without overlapping labels.",
        )
        self.add(h)

        n_total = 24
        source_r = 1.60
        source_center = np.array([0.0, -0.20, 0.0])
        _, right_source, left_source = self.vertical_half_sectors(
            n_total, source_r, source_center
        )
        right_source.shift(RIGHT * 0.34)
        left_source.shift(LEFT * 0.34)

        source_r_lab = self.text("RIGHT HALF", 29, BOLD).move_to([2.90, 1.72, 0])
        source_l_lab = self.text("LEFT HALF", 29, BOLD).move_to([-2.90, 1.72, 0])

        row_r = 1.70
        top_y, bottom_y = 0.48, -0.48
        row1, row2 = self.half_row_targets(n_total, row_r, top_y, bottom_y)
        top_arcs, bottom_arcs = self.half_row_arc_overlays(
            n_total, row_r, top_y, bottom_y
        )
        measures = self.row_measurements_from_halves(
            row1, row2, row_r, top_y, bottom_y
        )

        # FINAL4: translate the complete row/measurement system right by 0.42.
        # This creates projector-visible air between the 31 pt labels and the
        # first sector without shrinking either element.
        VGroup(row1, row2, top_arcs, bottom_arcs, measures).shift(RIGHT * 0.42)

        row1_lab = self.text("ROW 1 — RIGHT HALF", 31, BOLD).move_to([-5.00, 1.02, 0])
        row2_lab = self.text("ROW 2 — LEFT HALF", 31, BOLD).move_to([-5.00, -1.02, 0])

        group = VGroup(
            h, right_source, left_source, source_r_lab, source_l_lab,
            row1, row2, top_arcs, bottom_arcs, measures, row1_lab, row2_lab,
        )
        self.projector_safe(group, "v8 final4 step4")

        self.play(
            FadeIn(right_source), FadeIn(left_source),
            FadeIn(source_r_lab), FadeIn(source_l_lab),
            run_time=1.00,
        )
        self.wait(1.5)
        self.play(
            AnimationGroup(
                *[Transform(right_source[j], row1[j]) for j in range(n_total // 2)],
                lag_ratio=0.050,
            ),
            FadeOut(source_r_lab), FadeIn(row1_lab, shift=RIGHT * 0.08),
            run_time=2.45, rate_func=smooth,
        )
        self.wait(1.7)
        self.play(
            AnimationGroup(
                *[Transform(left_source[j], row2[j]) for j in range(n_total // 2)],
                lag_ratio=0.050,
            ),
            FadeOut(source_l_lab), FadeIn(row2_lab, shift=RIGHT * 0.08),
            run_time=2.45, rate_func=smooth,
        )
        self.wait(2.0)
        self.play(
            LaggedStart(*[Create(a) for a in top_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[0]), Write(measures[1]),
            GrowFromCenter(measures[4]), Write(measures[5]),
            run_time=1.25,
        )
        self.wait(2.8)
        self.play(
            LaggedStart(*[Create(a) for a in bottom_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[2]), Write(measures[3]),
            GrowFromCenter(measures[6]), Write(measures[7]),
            run_time=1.25,
        )
        self.wait(3.6)
        self.play(
            FadeOut(top_arcs), FadeOut(bottom_arcs), FadeOut(measures),
            run_time=0.80,
        )
        checkpoint = self.big_formula(
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}",
            10.5, 43,
        ).move_to([0.0, -3.04, 0])
        self.projector_safe(checkpoint, "v8 final4 step4 checkpoint")
        self.play(FadeIn(checkpoint, shift=UP * 0.08), run_time=0.95)
        self.wait(4.6)
        self.clear_stage(VGroup(h, right_source, left_source, row1_lab, row2_lab, checkpoint))

    def step_7_base_english(self) -> None:
        h = self.header(
            7,
            "THE BASE IS HALF THE PERIMETER",
            "The top and bottom boundaries each come from one semicircle. A rectangle base uses only one of them.",
        )
        self.add(h)

        n, r = 36, 2.24
        center = np.array([-0.70, 0.00, 0.0])
        strip = self.strip_targets(n, r, center=center)
        arcs_top, arcs_bottom = self.final_row_arc_overlays(n, r, center_y=center[1])
        arcs_top.shift(LEFT * 0.70)
        arcs_bottom.shift(LEFT * 0.70)

        x0, x1 = strip.get_left()[0], strip.get_right()[0]
        base = DoubleArrow(
            [x0, -1.56, 0], [x1, -1.56, 0],
            color=BLACK, buff=0.02, tip_length=0.15, stroke_width=3.2,
        )
        base_lab = self.math(
            r"\text{base}=\frac{P}{2}=\pi r", 50
        ).next_to(base, DOWN, buff=0.09)

        row1 = self.text("ROW 1 boundary = P/2", 29, BOLD).move_to([5.25, 0.70, 0])
        row2 = self.text("ROW 2 boundary = P/2", 29, BOLD).move_to([5.25, -0.10, 0])
        # FINAL4: shift the conclusion panel right.  Its left edge is now >1.2,
        # leaving clear air after the base equation while the right edge remains
        # inside the projector-safe zone.
        choose = self.big_formula(
            r"\text{ONE base}=\frac{P}{2}=\pi r", 6.4, 50
        ).move_to([4.45, -2.96, 0])

        group = VGroup(
            h, strip, arcs_top, arcs_bottom,
            base, base_lab, row1, row2, choose,
        )
        self.projector_safe(group, "v8 final4 step7")

        self.play(FadeIn(strip), run_time=1.00)
        self.wait(1.2)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.042),
            FadeIn(row1, shift=LEFT * 0.08),
            run_time=1.40,
        )
        self.wait(2.0)
        self.play(
            LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.042),
            FadeIn(row2, shift=LEFT * 0.08),
            run_time=1.40,
        )
        self.wait(2.1)
        self.play(GrowFromCenter(base), Write(base_lab), run_time=1.25)
        self.wait(1.8)
        self.play(FadeIn(choose, shift=UP * 0.06), run_time=0.95)
        self.play(Circumscribe(base_lab, color=MID_GRAY, time_width=0.8), run_time=1.15)
        self.wait(5.2)
        self.clear_stage(group)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL4.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal4 --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL4.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal4 --disable_caching
