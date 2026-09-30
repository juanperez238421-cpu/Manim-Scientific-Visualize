#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle foundations + vertical halves + two-row area derivation V7.

Pedagogical sequence requested for the classroom master render:
1. Identify perimeter/circumference, diameter and radius.
2. Use pi = P/d, then d = 2r, to derive P = pi d = 2 pi r.
3. Cut the circle with a vertical diameter into two semicircles.
4. Make explicit that EACH curved semicircle arc is P/2 = pi r.
5. Divide EACH half into equal sectors while preserving the half ownership.
6. Transform the right-half pieces into ROW 1 and the left-half pieces into ROW 2.
7. Measure each row separately: radial height r and curved-edge total P/2 = pi r.
8. Interlock the two rows with essentially vertical motion into one almost-rectangle.
9. Reuse the audited V6 shared-height/base/limit scenes to conclude A = pi r^2.

This file intentionally subclasses the audited V6 English master so the established
projector-safe typography, margin checks, animation helpers and final limit argument
remain unchanged. Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps,
H.264/yuv420p using the literal -pqh render path.
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
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V7Master(
    Geometry8CircleAreaTwoRowsEnglish20260827V6Master
):
    """Full English classroom master: circle parts -> pi -> halves -> rows -> area."""

    # ------------------------------------------------------------------
    # Geometry helpers dedicated to the vertical-half ownership narrative
    # ------------------------------------------------------------------
    def vertical_half_sectors(
        self,
        n_total: int,
        r: float,
        center: np.ndarray,
    ) -> tuple[VGroup, VGroup, VGroup]:
        """Return all sectors plus right/left semicircle groups.

        The first boundary is the downward vertical radius (-pi/2). Therefore the
        first n/2 sectors sweep the RIGHT semicircle and the second n/2 sectors
        sweep the LEFT semicircle. This makes the vertical diameter the exact
        ownership boundary used later for ROW 1 and ROW 2.
        """
        assert n_total % 2 == 0
        delta = TAU / n_total
        all_sectors = VGroup()
        right = VGroup()
        left = VGroup()
        for i in range(n_total):
            is_right = i < n_total // 2
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=-PI / 2 + i * delta,
                stroke_color=BLACK,
                stroke_width=1.35,
                fill_color=VERY_LIGHT_GRAY if is_right else WHITE,
                fill_opacity=1,
            )
            sec.shift(center)
            all_sectors.add(sec)
            (right if is_right else left).add(sec)
        return all_sectors, right, left

    def half_row_targets(
        self,
        n_total: int,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
        center_x: float = 0.0,
    ) -> tuple[VGroup, VGroup]:
        """Create two separate rows while preserving semicircle ownership.

        Right-half pieces occupy the final EVEN x-locations and point upward.
        Left-half pieces occupy the final ODD x-locations and point downward.
        Therefore the later interlock is a controlled vertical motion rather than
        a crossing fan.
        """
        assert n_total % 2 == 0
        m = n_total // 2
        delta = TAU / n_total
        dx = PI * r / n_total
        row1 = VGroup()
        row2 = VGroup()
        for j in range(m):
            i_even = 2 * j
            i_odd = 2 * j + 1
            x1 = center_x + (i_even - (n_total - 1) / 2) * dx
            x2 = center_x + (i_odd - (n_total - 1) / 2) * dx

            top = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=PI / 2 - delta / 2,
                stroke_color=BLACK,
                stroke_width=1.35,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1,
            ).shift([x1, top_pivot_y, 0])

            bottom = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=-PI / 2 - delta / 2,
                stroke_color=BLACK,
                stroke_width=1.35,
                fill_color=WHITE,
                fill_opacity=1,
            ).shift([x2, bottom_pivot_y, 0])

            row1.add(top)
            row2.add(bottom)
        return row1, row2

    def half_row_arc_overlays(
        self,
        n_total: int,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
        center_x: float = 0.0,
    ) -> tuple[VGroup, VGroup]:
        """Highlight the curved edges whose sums are P/2 for the two half-rows."""
        m = n_total // 2
        delta = TAU / n_total
        dx = PI * r / n_total
        top_arcs = VGroup()
        bottom_arcs = VGroup()
        for j in range(m):
            i_even = 2 * j
            i_odd = 2 * j + 1
            x1 = center_x + (i_even - (n_total - 1) / 2) * dx
            x2 = center_x + (i_odd - (n_total - 1) / 2) * dx
            top_arcs.add(
                Arc(
                    radius=r,
                    start_angle=PI / 2 - delta / 2,
                    angle=delta,
                    color=BLACK,
                    stroke_width=6,
                ).move_arc_center_to([x1, top_pivot_y, 0])
            )
            bottom_arcs.add(
                Arc(
                    radius=r,
                    start_angle=-PI / 2 - delta / 2,
                    angle=delta,
                    color=MID_GRAY,
                    stroke_width=6,
                ).move_arc_center_to([x2, bottom_pivot_y, 0])
            )
        return top_arcs, bottom_arcs

    def row_measurements_from_halves(
        self,
        row1: VGroup,
        row2: VGroup,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
    ) -> VGroup:
        """Large row-by-row measurements for the separate semicircle rows."""
        x0 = min(row1.get_left()[0], row2.get_left()[0])
        x1 = max(row1.get_right()[0], row2.get_right()[0])
        top_y = top_pivot_y + r
        bottom_y = bottom_pivot_y - r

        top_base = DoubleArrow(
            [x0, top_y + 0.28, 0], [x1, top_y + 0.28, 0],
            color=BLACK, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        top_base_lab = self.math(r"\frac{P}{2}=\pi r", 42).next_to(top_base, UP, buff=0.07)

        bottom_base = DoubleArrow(
            [x0, bottom_y - 0.28, 0], [x1, bottom_y - 0.28, 0],
            color=MID_GRAY, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        bottom_base_lab = self.math(r"\frac{P}{2}=\pi r", 42).next_to(bottom_base, DOWN, buff=0.07)

        xh = x1 + 0.58
        top_h = DoubleArrow(
            [xh, top_pivot_y, 0], [xh, top_y, 0],
            color=BLACK, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        top_h_lab = self.math("r", 44).next_to(top_h, RIGHT, buff=0.12)

        bottom_h = DoubleArrow(
            [xh, bottom_y, 0], [xh, bottom_pivot_y, 0],
            color=MID_GRAY, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        bottom_h_lab = self.math("r", 44).next_to(bottom_h, RIGHT, buff=0.12)

        return VGroup(
            top_base, top_base_lab,
            bottom_base, bottom_base_lab,
            top_h, top_h_lab,
            bottom_h, bottom_h_lab,
        )

    # ------------------------------------------------------------------
    # Full V7 timeline
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening_v7()
        self.step_1_circle_parts_and_pi()
        self.step_2_vertical_halves()
        self.step_3_divide_each_half()
        self.step_4_two_separate_rows_from_halves()
        self.step_5_interlock_halves_pair_first()
        self.step_6_shared_height_english()
        self.step_7_base_english()
        self.step_8_limit_english()
        self.closing_v7()

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening_v7(self) -> None:
        title = self.text("CIRCLE: FROM PERIMETER TO AREA", 54, BOLD)
        subtitle = self.text("Parts → π → two semicircles → two rows → one area formula", 31)
        flow = self.text("MEASURE  →  SPLIT  →  DIVIDE  →  SEPARATE  →  INTERLOCK", 27, BOLD)
        formula = self.big_formula(r"P=2\pi r\qquad\Longrightarrow\qquad A=\pi r^2", 9.0, 54)
        group = VGroup(title, subtitle, flow, formula).arrange(DOWN, buff=0.38)
        self.assert_safe(group, "v7 opening")

        self.play(Write(title), run_time=1.30)
        self.play(FadeIn(subtitle, shift=UP * 0.08), run_time=0.85)
        self.play(FadeIn(flow, shift=UP * 0.08), run_time=0.90)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.90)
        self.wait(3.8)
        self.clear_stage(group)

    # ------------------------------------------------------------------
    # 01 — Circle parts and circumference formula from pi
    # ------------------------------------------------------------------
    def step_1_circle_parts_and_pi(self) -> None:
        h = self.header(
            1,
            "CIRCLE PARTS: PERIMETER, DIAMETER AND RADIUS",
            "The constant ratio perimeter ÷ diameter is π. From that ratio we obtain the circumference formula.",
        )
        self.add(h)

        center = np.array([-3.45, -0.20, 0.0])
        r = 2.28
        circle = Circle(radius=r, color=BLACK, stroke_width=4.4).move_to(center)
        dot = Dot(center, radius=0.075, color=BLACK)
        center_lab = self.text("CENTER", 22, BOLD).next_to(dot, DOWN + LEFT, buff=0.12)

        diameter = DoubleArrow(
            center + LEFT * r,
            center + RIGHT * r,
            color=BLACK,
            buff=0.03,
            tip_length=0.16,
            stroke_width=3.1,
        )
        d_lab = self.math("d", 44).next_to(diameter, DOWN, buff=0.13)

        theta = 42 * DEGREES
        r_end = center + r * np.array([np.cos(theta), np.sin(theta), 0.0])
        radius = Arrow(center, r_end, buff=0.0, color=MID_GRAY, stroke_width=3.4, tip_length=0.17)
        r_lab = self.math("r", 44).next_to(radius.get_center(), UP + LEFT, buff=0.08)

        perimeter_lab = self.text("PERIMETER  P", 28, BOLD).move_to([-3.55, 2.62, 0])
        perimeter_arrow = Arrow(
            [-3.55, 2.34, 0], center + UP * r * 0.98,
            color=MID_GRAY, stroke_width=2.5, tip_length=0.14,
        )

        ratio_title = self.text("THE DEFINITION OF π", 29, BOLD)
        ratio = self.big_formula(r"\pi=\frac{P}{d}", 4.6, 52)
        rearranged = self.big_formula(r"P=\pi d", 4.6, 52)
        relation = self.big_formula(r"d=2r", 4.6, 52)
        conclusion = self.big_formula(r"P=\pi(2r)=2\pi r", 5.5, 50)
        formulas = VGroup(ratio_title, ratio, rearranged, relation, conclusion).arrange(DOWN, buff=0.18)
        formulas.move_to([3.75, -0.05, 0])

        g = VGroup(
            h, circle, dot, center_lab, diameter, d_lab, radius, r_lab,
            perimeter_lab, perimeter_arrow, formulas,
        )
        self.assert_safe(g, "v7 step1 circle parts and pi")

        self.play(Create(circle), FadeIn(dot), run_time=1.00)
        self.play(FadeIn(perimeter_lab), GrowArrow(perimeter_arrow), run_time=0.80)
        self.wait(0.8)
        self.play(GrowFromCenter(diameter), Write(d_lab), run_time=0.95)
        self.play(GrowArrow(radius), Write(r_lab), FadeIn(center_lab), run_time=0.90)
        self.wait(1.2)

        self.play(FadeIn(ratio_title, shift=UP * 0.05), FadeIn(ratio, shift=LEFT * 0.08), run_time=0.90)
        self.wait(1.3)
        self.play(FadeIn(rearranged, shift=LEFT * 0.08), run_time=0.80)
        self.wait(1.0)
        self.play(FadeIn(relation, shift=LEFT * 0.08), run_time=0.80)
        self.wait(1.0)
        self.play(FadeIn(conclusion, shift=LEFT * 0.08), run_time=0.90)
        self.play(Indicate(conclusion[1], color=MID_GRAY, scale_factor=1.04), run_time=1.00)
        self.wait(4.4)
        self.clear_stage(g)

    # ------------------------------------------------------------------
    # 02 — Cut by the vertical diameter: each curved half is P/2
    # ------------------------------------------------------------------
    def step_2_vertical_halves(self) -> None:
        h = self.header(
            2,
            "CUT THE CIRCLE WITH A VERTICAL DIAMETER",
            "The cut creates two semicircles. Each CURVED semicircle arc is exactly half of the original perimeter.",
        )
        self.add(h)

        center = np.array([0.0, -0.15, 0.0])
        r = 2.30
        right = AnnularSector(
            inner_radius=0, outer_radius=r, angle=PI, start_angle=-PI / 2,
            stroke_color=BLACK, stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        ).shift(center)
        left = AnnularSector(
            inner_radius=0, outer_radius=r, angle=PI, start_angle=PI / 2,
            stroke_color=BLACK, stroke_width=2.0,
            fill_color=WHITE, fill_opacity=1,
        ).shift(center)
        outline = Circle(radius=r, color=BLACK, stroke_width=3.8).move_to(center)
        cut = Line(center + DOWN * r, center + UP * r, color=BLACK, stroke_width=3.4)
        cut_lab = self.text("VERTICAL DIAMETER", 26, BOLD).next_to(cut, RIGHT, buff=0.18).shift(UP * 0.15)

        right_arc = Arc(radius=r, start_angle=-PI / 2, angle=PI, color=BLACK, stroke_width=7).move_arc_center_to(center)
        left_arc = Arc(radius=r, start_angle=PI / 2, angle=PI, color=MID_GRAY, stroke_width=7).move_arc_center_to(center)

        formula = self.big_formula(r"P=2\pi r\qquad\Rightarrow\qquad\frac{P}{2}=\pi r", 7.8, 48).move_to([0.0, -3.15, 0])
        note = self.text("Important: P/2 refers to the curved arc, not arc + diameter.", 28, BOLD).move_to([0.0, 2.63, 0])

        self.assert_safe(VGroup(h, right, left, outline, cut, cut_lab, right_arc, left_arc, formula, note), "v7 step2 vertical halves")

        self.play(FadeIn(right), FadeIn(left), Create(outline), run_time=1.00)
        self.play(Create(cut), FadeIn(cut_lab, shift=LEFT * 0.06), run_time=0.85)
        self.wait(1.0)
        self.play(FadeIn(note, shift=UP * 0.06), run_time=0.70)
        self.play(Create(right_arc), run_time=0.90)
        right_lab = self.math(r"\frac{P}{2}=\pi r", 42).move_to([3.45, 0.55, 0])
        self.play(FadeIn(right_lab, shift=LEFT * 0.08), run_time=0.70)
        self.wait(1.0)
        self.play(Create(left_arc), run_time=0.90)
        left_lab = self.math(r"\frac{P}{2}=\pi r", 42).move_to([-3.45, 0.55, 0])
        self.play(FadeIn(left_lab, shift=RIGHT * 0.08), run_time=0.70)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.80)
        self.wait(4.6)

        # Separate the two halves slightly so ownership is visually unmistakable.
        self.play(
            right.animate.shift(RIGHT * 0.48), right_arc.animate.shift(RIGHT * 0.48), right_lab.animate.shift(RIGHT * 0.30),
            left.animate.shift(LEFT * 0.48), left_arc.animate.shift(LEFT * 0.48), left_lab.animate.shift(LEFT * 0.30),
            FadeOut(outline), FadeOut(cut), FadeOut(cut_lab),
            run_time=1.15,
            rate_func=smooth,
        )
        self.wait(2.8)
        self.clear_stage(VGroup(h, right, left, right_arc, left_arc, right_lab, left_lab, formula, note))

    # ------------------------------------------------------------------
    # 03 — Divide EACH semicircle into equal sectors
    # ------------------------------------------------------------------
    def step_3_divide_each_half(self) -> None:
        h = self.header(
            3,
            "DIVIDE EACH SEMICIRCLE INTO THE SAME NUMBER OF PIECES",
            "We keep the two halves distinct: 12 sectors come from the right half and 12 sectors come from the left half.",
        )
        self.add(h)

        n_total, r = 24, 2.22
        center = np.array([0.0, -0.22, 0.0])
        _, right, left = self.vertical_half_sectors(n_total, r, center)
        right.shift(RIGHT * 0.42)
        left.shift(LEFT * 0.42)

        right_outline = Arc(radius=r, start_angle=-PI / 2, angle=PI, color=BLACK, stroke_width=4).move_arc_center_to(center + RIGHT * 0.42)
        left_outline = Arc(radius=r, start_angle=PI / 2, angle=PI, color=MID_GRAY, stroke_width=4).move_arc_center_to(center + LEFT * 0.42)

        right_title = self.text("RIGHT HALF", 30, BOLD).move_to([4.10, 1.55, 0])
        left_title = self.text("LEFT HALF", 30, BOLD).move_to([-4.10, 1.55, 0])
        right_count = self.big_formula(r"12\ \text{equal sectors}", 4.4, 39).move_to([4.25, 0.45, 0])
        left_count = self.big_formula(r"12\ \text{equal sectors}", 4.4, 39).move_to([-4.25, 0.45, 0])
        right_arc_sum = self.math(r"\text{arc sum}=\frac{P}{2}=\pi r", 36).move_to([4.15, -1.10, 0])
        left_arc_sum = self.math(r"\text{arc sum}=\frac{P}{2}=\pi r", 36).move_to([-4.15, -1.10, 0])

        radial_note = self.text("Every sector still reaches a radial distance r from its own vertex.", 28, BOLD).move_to([0.0, -3.18, 0])

        self.assert_safe(VGroup(h, right, left, right_outline, left_outline, right_title, left_title, right_count, left_count, right_arc_sum, left_arc_sum, radial_note), "v7 step3 divide halves")

        self.play(Create(right_outline), Create(left_outline), run_time=0.70)
        self.play(
            LaggedStart(*[FadeIn(s) for s in right], lag_ratio=0.035),
            FadeIn(right_title), FadeIn(right_count, shift=LEFT * 0.08),
            run_time=1.55,
        )
        self.play(FadeIn(right_arc_sum, shift=UP * 0.06), run_time=0.70)
        self.wait(1.2)
        self.play(
            LaggedStart(*[FadeIn(s) for s in left], lag_ratio=0.035),
            FadeIn(left_title), FadeIn(left_count, shift=RIGHT * 0.08),
            run_time=1.55,
        )
        self.play(FadeIn(left_arc_sum, shift=UP * 0.06), run_time=0.70)
        self.play(FadeIn(radial_note, shift=UP * 0.06), run_time=0.70)
        self.wait(4.5)
        self.clear_stage(VGroup(h, right, left, right_outline, left_outline, right_title, left_title, right_count, left_count, right_arc_sum, left_arc_sum, radial_note))

    # ------------------------------------------------------------------
    # 04 — Transform the two semicircles into TWO SEPARATE rows
    # ------------------------------------------------------------------
    def step_4_two_separate_rows_from_halves(self) -> None:
        h = self.header(
            4,
            "FORM TWO SEPARATE ROWS — ONE ROW FROM EACH HALF",
            "Do not combine them yet. ROW 1 keeps all right-half pieces; ROW 2 keeps all left-half pieces.",
        )
        self.add(h)

        n_total = 24
        source_r = 1.55
        source_center = np.array([0.0, -0.18, 0.0])
        _, right_source, left_source = self.vertical_half_sectors(n_total, source_r, source_center)
        right_source.shift(RIGHT * 0.28)
        left_source.shift(LEFT * 0.28)

        row_r = 1.63
        top_y, bottom_y = 0.58, -0.58
        row1, row2 = self.half_row_targets(n_total, row_r, top_y, bottom_y)
        top_arcs, bottom_arcs = self.half_row_arc_overlays(n_total, row_r, top_y, bottom_y)
        measures = self.row_measurements_from_halves(row1, row2, row_r, top_y, bottom_y)

        source_r_lab = self.text("RIGHT HALF", 27, BOLD).move_to([2.75, 1.82, 0])
        source_l_lab = self.text("LEFT HALF", 27, BOLD).move_to([-2.75, 1.82, 0])
        row1_lab = self.text("ROW 1  ←  right semicircle", 31, BOLD).move_to([-4.85, 1.35, 0])
        row2_lab = self.text("ROW 2  ←  left semicircle", 31, BOLD).move_to([-4.85, -1.35, 0])

        keep_separate = self.text("CHECKPOINT: TWO ROWS ARE STILL SEPARATE.", 29, BOLD).move_to([0.0, -3.48, 0])

        self.assert_safe(VGroup(h, right_source, left_source, source_r_lab, source_l_lab, row1, row2, top_arcs, bottom_arcs, measures, row1_lab, row2_lab, keep_separate), "v7 step4 two separate rows")

        self.play(FadeIn(right_source), FadeIn(left_source), FadeIn(source_r_lab), FadeIn(source_l_lab), run_time=0.90)
        self.wait(1.0)
        self.play(FadeOut(source_r_lab), FadeOut(source_l_lab), run_time=0.35)

        self.play(
            AnimationGroup(*[Transform(right_source[j], row1[j]) for j in range(n_total // 2)], lag_ratio=0.035),
            FadeIn(row1_lab, shift=RIGHT * 0.08),
            run_time=2.05,
            rate_func=smooth,
        )
        self.wait(0.8)
        self.play(
            AnimationGroup(*[Transform(left_source[j], row2[j]) for j in range(n_total // 2)], lag_ratio=0.035),
            FadeIn(row2_lab, shift=RIGHT * 0.08),
            run_time=2.05,
            rate_func=smooth,
        )
        self.play(FadeIn(keep_separate, shift=UP * 0.06), run_time=0.70)
        self.wait(1.0)

        # Measure ROW 1 first.
        self.play(LaggedStart(*[Create(a) for a in top_arcs], lag_ratio=0.045), run_time=1.10)
        self.play(
            GrowFromCenter(measures[0]), Write(measures[1]),
            GrowFromCenter(measures[4]), Write(measures[5]),
            run_time=1.15,
        )
        self.wait(2.5)

        # Then ROW 2 with the exact same logic.
        self.play(LaggedStart(*[Create(a) for a in bottom_arcs], lag_ratio=0.045), run_time=1.10)
        self.play(
            GrowFromCenter(measures[2]), Write(measures[3]),
            GrowFromCenter(measures[6]), Write(measures[7]),
            run_time=1.15,
        )
        self.wait(4.4)

        self.clear_stage(VGroup(h, right_source, left_source, top_arcs, bottom_arcs, measures, row1_lab, row2_lab, keep_separate))

    # ------------------------------------------------------------------
    # 05 — Interlock while preserving half ownership
    # ------------------------------------------------------------------
    def step_5_interlock_halves_pair_first(self) -> None:
        h = self.header(
            5,
            "INTERLOCK ROW 1 AND ROW 2",
            "ROW 1 moves down and ROW 2 moves up. Because their x-positions are pre-aligned, the motion stays clean and readable.",
        )
        self.add(h)

        n_total, r = 24, 2.00
        top_y, bottom_y = 0.78, -0.78
        row1, row2 = self.half_row_targets(n_total, r, top_y, bottom_y)
        target = self.strip_targets(n_total, r, center=np.array([0.0, -0.10, 0.0]))
        row1_lab = self.text("ROW 1 / RIGHT HALF   ↓", 32, BOLD).move_to([-5.35, 1.55, 0])
        row2_lab = self.text("ROW 2 / LEFT HALF    ↑", 32, BOLD).move_to([-5.35, -1.55, 0])
        cue = self.text("FIRST: ONE MATCHED PAIR", 29, BOLD).move_to([0.0, -3.08, 0])

        self.assert_safe(VGroup(h, row1, row2, target, row1_lab, row2_lab, cue), "v7 step5 interlock halves")
        self.play(FadeIn(row1), FadeIn(row2), FadeIn(row1_lab), FadeIn(row2_lab), run_time=0.90)
        self.play(FadeIn(cue, shift=UP * 0.06), run_time=0.60)

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

        all_cue = self.text("NOW REPEAT THE SAME VERTICAL MOTION WITH EVERY PAIR", 28, BOLD).move_to(cue)
        self.play(Transform(cue, all_cue), run_time=0.55)

        order = sorted([k for k in range(n_total // 2) if k != j], key=lambda k: abs(k - j))
        animations = []
        for k in order:
            animations.append(Transform(row1[k], target[2 * k]))
            animations.append(Transform(row2[k], target[2 * k + 1]))
        self.play(
            LaggedStart(*animations, lag_ratio=0.035),
            FadeOut(row1_lab), FadeOut(row2_lab),
            run_time=3.20,
            rate_func=smooth,
        )
        self.play(FadeOut(cue), run_time=0.35)

        top_line = DashedLine([-3.75, 0.90, 0], [3.75, 0.90, 0], color=LIGHT_GRAY, dash_length=0.10)
        bottom_line = DashedLine([-3.75, -1.10, 0], [3.75, -1.10, 0], color=LIGHT_GRAY, dash_length=0.10)
        conserved = self.text("SAME 24 PIECES  →  SAME TOTAL AREA", 32, BOLD).move_to([0.0, -3.08, 0])
        self.play(Create(top_line), Create(bottom_line), FadeIn(conserved, shift=UP * 0.06), run_time=0.80)
        self.wait(4.2)
        self.clear_stage(VGroup(h, row1, row2, top_line, bottom_line, conserved))

    # ------------------------------------------------------------------
    # Closing notebook checkpoint
    # ------------------------------------------------------------------
    def closing_v7(self) -> None:
        title = self.text("CIRCLE DERIVATION — NOTEBOOK SUMMARY", 41, BOLD)
        lines = VGroup(
            self.text("1. π is the constant ratio  P/d, so  P = πd.", 30),
            self.text("2. Since  d = 2r, the circle perimeter is  P = 2πr.", 30),
            self.text("3. A vertical diameter creates two curved arcs; each arc is  P/2 = πr.", 30),
            self.text("4. Divide each semicircle and keep its pieces in a separate row.", 30),
            self.text("5. Interlock the rows: shared height = r and one long base = P/2 = πr.", 30),
            self.text("6. Rearranging changes position, not area.", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        formula = self.big_formula(r"A=(\pi r)(r)=\pi r^2", 7.0, 56)
        group = VGroup(title, lines, formula).arrange(DOWN, buff=0.34)
        if group.height > 7.6:
            group.scale_to_fit_height(7.6)
        self.assert_safe(group, "v7 closing")

        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.80)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.08) for line in lines], lag_ratio=0.16), run_time=2.35)
        self.wait(2.0)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.90)
        self.wait(6.0)


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_MASTER.py Geometry8CircleFoundationsHalvesTwoRows20260829V7Master --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_MASTER.py Geometry8CircleFoundationsHalvesTwoRows20260829V7Master --disable_caching
