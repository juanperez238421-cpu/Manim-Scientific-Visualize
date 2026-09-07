#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Foundations V8 SENIOR QA.

Frame-by-frame refinement of the rendered V7 FINAL_QA.
Keeps the validated mathematics/ownership model while fixing visible clipping,
local collisions, scale, pacing and motion continuity.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pqh.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V7_FINAL_QA import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (
    MID_GRAY, LIGHT_GRAY, PAPER,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQA(
    Geometry8CircleFoundationsHalvesTwoRows20260829V7FinalQA
):
    """Projector-first senior QA master."""

    SAFE_X = 7.70
    SAFE_Y = 4.26
    MOTION_SCALE = 1.12
    PAUSE_SCALE = 1.28

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= self.MOTION_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * self.PAUSE_SCALE, *args, **kwargs)

    def projector_safe(self, mob: Mobject, label: str) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -self.SAFE_X or right > self.SAFE_X:
            raise ValueError(
                f"{label}: projector horizontal overflow "
                f"(left={left:.3f}, right={right:.3f})"
            )
        if bottom < -self.SAFE_Y or top > self.SAFE_Y:
            raise ValueError(
                f"{label}: projector vertical overflow "
                f"(bottom={bottom:.3f}, top={top:.3f})"
            )

    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        """Safe replacement for the V6/V7 header that visibly cropped long titles."""
        badge = RoundedRectangle(
            width=0.86, height=0.58, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=2.3,
            fill_color=WHITE, fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 25, BOLD).move_to(badge)
        title_mob = self.text(title, 40, BOLD)
        if title_mob.width > 12.95:
            title_mob.scale_to_fit_width(12.95)

        row = VGroup(VGroup(badge, badge_text), title_mob).arrange(RIGHT, buff=0.27)
        row.to_edge(UP, buff=0.15).to_edge(LEFT, buff=0.48)

        rule_y = row.get_bottom()[1] - 0.10
        rule = Line(
            [-7.52, rule_y, 0], [7.52, rule_y, 0],
            color=LIGHT_GRAY, stroke_width=2.2,
        )

        subtitle_mob = self.text(subtitle, 27)
        if subtitle_mob.width > 14.45:
            subtitle_mob.scale_to_fit_width(14.45)
        subtitle_mob.next_to(rule, DOWN, buff=0.09).align_to(row, LEFT)

        group = VGroup(row, rule, subtitle_mob)
        self.projector_safe(group, f"header {number:02d}")
        return group

    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening_v8()
        self.step_1_circle_parts_and_pi()
        self.step_2_vertical_halves()
        self.step_3_divide_each_half()
        self.step_4_two_separate_rows_from_halves()
        self.step_5_interlock_halves_pair_first()
        self.step_6_shared_height_english()
        self.step_7_base_english()
        self.step_8_limit_english()
        self.closing_v8()

    def opening_v8(self) -> None:
        title = self.text("CIRCLE: FROM PERIMETER TO AREA", 60, BOLD)
        subtitle = self.text(
            "Measure the boundary → split the circle → rearrange the same area", 34
        )
        flow = self.text(
            "PERIMETER   →   DIAMETER   →   π   →   TWO HALVES   →   TWO ROWS",
            30, BOLD,
        )
        formula = self.big_formula(
            r"P=2\pi r\qquad\Longrightarrow\qquad A=\pi r^2", 10.2, 60
        )
        group = VGroup(title, subtitle, flow, formula).arrange(DOWN, buff=0.44)
        self.projector_safe(group, "v8 opening")

        self.play(Write(title), run_time=1.55, rate_func=smooth)
        self.wait(0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.10), run_time=0.95)
        self.wait(0.6)
        self.play(FadeIn(flow, shift=UP * 0.08), run_time=1.00)
        self.wait(0.7)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=1.00)
        self.wait(4.5)
        self.clear_stage(group)

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
        d_lab = self.math("d", 50).move_to(center + DOWN * 0.54)

        theta = 42 * DEGREES
        r_end = center + r * np.array([np.cos(theta), np.sin(theta), 0.0])
        radius = Arrow(
            center, r_end, buff=0.0,
            color=MID_GRAY, stroke_width=3.5, tip_length=0.18,
        )
        r_lab = self.math("r", 50).move_to(center + np.array([1.18, 1.35, 0]))
        center_lab = self.text("CENTER", 24, BOLD).move_to(
            center + np.array([-0.68, -0.34, 0])
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
        self.projector_safe(group, "v8 step1")

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
        self.play(TransformMatchingTex(eq, eq2), run_time=1.10)
        self.wait(1.9)
        self.play(FadeIn(relation, shift=LEFT * 0.08), run_time=0.95)
        self.wait(1.8)
        self.play(FadeIn(conclusion, shift=LEFT * 0.08), run_time=1.05)
        self.play(Circumscribe(conclusion[1], color=MID_GRAY, time_width=0.8), run_time=1.20)
        self.wait(4.8)
        self.clear_stage(group)

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

        row1_lab = self.text("ROW 1 — RIGHT HALF", 31, BOLD).move_to([-5.55, 1.02, 0])
        row2_lab = self.text("ROW 2 — LEFT HALF", 31, BOLD).move_to([-5.55, -1.02, 0])

        group = VGroup(
            h, right_source, left_source, source_r_lab, source_l_lab,
            row1, row2, top_arcs, bottom_arcs, measures, row1_lab, row2_lab,
        )
        self.projector_safe(group, "v8 step4")

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
            FadeOut(source_r_lab),
            FadeIn(row1_lab, shift=RIGHT * 0.08),
            run_time=2.45, rate_func=smooth,
        )
        self.wait(1.7)

        self.play(
            AnimationGroup(
                *[Transform(left_source[j], row2[j]) for j in range(n_total // 2)],
                lag_ratio=0.050,
            ),
            FadeOut(source_l_lab),
            FadeIn(row2_lab, shift=RIGHT * 0.08),
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

        self.play(FadeOut(top_arcs), FadeOut(bottom_arcs), FadeOut(measures), run_time=0.80)
        checkpoint = self.big_formula(
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}",
            10.5, 43,
        ).move_to([0.0, -3.04, 0])
        self.projector_safe(checkpoint, "v8 step4 checkpoint")
        self.play(FadeIn(checkpoint, shift=UP * 0.08), run_time=0.95)
        self.wait(4.6)

        self.clear_stage(VGroup(
            h, right_source, left_source, row1_lab, row2_lab, checkpoint
        ))

    def step_6_shared_height_english(self) -> None:
        h = self.header(
            6,
            "THE TWO ROWS SHARE ONE HEIGHT:  r",
            "After interlocking, both ownership groups occupy the same vertical band. Their heights are not added.",
        )
        self.add(h)

        n, r = 36, 2.28
        center = np.array([-0.20, -0.10, 0.0])
        strip = self.strip_targets(n, r, center=center)

        top_y = center[1] + r / 2
        bottom_y = center[1] - r / 2
        top = DashedLine(
            [-4.25, top_y, 0], [4.05, top_y, 0],
            color=MID_GRAY, dash_length=0.10,
        )
        bottom = DashedLine(
            [-4.25, bottom_y, 0], [4.05, bottom_y, 0],
            color=MID_GRAY, dash_length=0.10,
        )
        height = DoubleArrow(
            [4.45, bottom_y, 0], [4.45, top_y, 0],
            color=BLACK, buff=0.02, tip_length=0.15, stroke_width=3.2,
        )
        h_lab = self.math("r", 58).next_to(height, RIGHT, buff=0.15)

        row1_tag = self.text("ROW 1 pieces", 30, BOLD).move_to([-5.45, 0.68, 0])
        row2_tag = self.text("ROW 2 pieces", 30, BOLD).move_to([-5.45, -0.90, 0])
        arrow1 = Arrow(
            [-4.55, 0.60, 0], strip[12].get_center(),
            color=MID_GRAY, stroke_width=2.2, tip_length=0.12,
        )
        arrow2 = Arrow(
            [-4.55, -0.82, 0], strip[13].get_center(),
            color=MID_GRAY, stroke_width=2.2, tip_length=0.12,
        )
        key = self.big_formula(
            r"\text{shared height}=r\qquad\text{NOT}\qquad 2r",
            8.8, 54,
        ).move_to([0.0, -3.12, 0])

        group = VGroup(
            h, strip, top, bottom, height, h_lab,
            row1_tag, row2_tag, arrow1, arrow2, key,
        )
        self.projector_safe(group, "v8 step6")

        self.play(FadeIn(strip), run_time=1.00)
        self.wait(1.1)
        self.play(Create(top), Create(bottom), run_time=0.80)
        self.play(
            FadeIn(row1_tag), FadeIn(row2_tag),
            GrowArrow(arrow1), GrowArrow(arrow2),
            run_time=1.05,
        )
        self.wait(2.1)
        self.play(
            Indicate(strip[12], color=MID_GRAY, scale_factor=1.08),
            Indicate(strip[13], color=MID_GRAY, scale_factor=1.08),
            run_time=1.20,
        )
        self.wait(1.0)
        self.play(
            FadeOut(arrow1), FadeOut(arrow2),
            GrowFromCenter(height), Write(h_lab),
            run_time=1.10,
        )
        self.wait(1.8)
        self.play(FadeIn(key, shift=UP * 0.08), run_time=0.95)
        self.wait(5.2)
        self.clear_stage(group)

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
        choose = self.big_formula(
            r"\text{ONE base}=\frac{P}{2}=\pi r", 6.4, 50
        ).move_to([3.85, -2.96, 0])

        group = VGroup(
            h, strip, arcs_top, arcs_bottom,
            base, base_lab, row1, row2, choose,
        )
        self.projector_safe(group, "v8 step7")

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

    def step_8_limit_english(self) -> None:
        h = self.header(
            8,
            "MORE SECTORS → STRAIGHTER EDGES → EXACT AREA",
            "As sectors become thinner, the scalloped edges approach straight lines while the area remains unchanged.",
        )
        self.add(h)

        r = 2.40
        center = np.array([0.0, -0.10, 0.0])
        coarse = self.strip_targets(8, r, center=center)
        medium = self.strip_targets(24, r, center=center)
        fine = self.strip_targets(64, r, center=center)
        label = self.text("8 sectors — visible scallops", 34, BOLD).move_to([0.0, 2.15, 0])

        self.projector_safe(VGroup(h, coarse, medium, fine, label), "v8 step8 start")
        self.play(FadeIn(coarse), FadeIn(label), run_time=0.95)
        self.wait(2.1)

        l24 = self.text("24 sectors — edges look straighter", 34, BOLD).move_to(label)
        self.play(
            Transform(coarse, medium), Transform(label, l24),
            run_time=1.70, rate_func=smooth,
        )
        self.wait(2.3)

        l64 = self.text("64 sectors — almost a rectangle", 34, BOLD).move_to(label)
        self.play(
            Transform(coarse, fine), Transform(label, l64),
            run_time=1.90, rate_func=smooth,
        )
        self.wait(2.6)

        rect = Rectangle(
            width=PI * r, height=r,
            color=MID_GRAY, stroke_width=3.0,
        ).move_to(center)

        base_y = center[1] - r / 2 - 0.40
        base = DoubleArrow(
            [-PI * r / 2, base_y, 0], [PI * r / 2, base_y, 0],
            color=BLACK, buff=0.02, tip_length=0.14, stroke_width=3.0,
        )
        base_lab = self.math(r"\pi r", 50).next_to(base, DOWN, buff=0.08)

        hx = PI * r / 2 + 0.40
        height = DoubleArrow(
            [hx, center[1] - r / 2, 0], [hx, center[1] + r / 2, 0],
            color=BLACK, buff=0.02, tip_length=0.14, stroke_width=3.0,
        )
        height_lab = self.math("r", 50).next_to(height, RIGHT, buff=0.12)

        self.projector_safe(
            VGroup(rect, base, base_lab, height, height_lab),
            "v8 step8 rectangle",
        )
        self.play(
            Create(rect), GrowFromCenter(base), Write(base_lab),
            GrowFromCenter(height), Write(height_lab),
            run_time=1.30,
        )
        self.wait(2.6)

        equation = self.big_formula(
            r"A=(\pi r)(r)=\pi r^2", 8.4, 62
        ).move_to([0.0, -3.16, 0])
        self.projector_safe(equation, "v8 step8 equation")
        self.play(FadeIn(equation, shift=UP * 0.10), run_time=1.00)
        self.wait(4.7)

        self.play(
            FadeOut(coarse), FadeOut(label), FadeOut(rect),
            FadeOut(base), FadeOut(base_lab),
            FadeOut(height), FadeOut(height_lab), FadeOut(h),
            equation.animate.move_to([0.0, -0.15, 0]).scale(1.16),
            run_time=1.30, rate_func=smooth,
        )
        final_title = self.text("AREA OF A CIRCLE", 48, BOLD).move_to([0.0, 1.45, 0])
        self.projector_safe(VGroup(equation, final_title), "v8 final area")
        self.play(FadeIn(final_title, shift=UP * 0.08), run_time=0.90)
        self.play(Circumscribe(equation[1], color=MID_GRAY, time_width=0.9), run_time=1.30)
        self.wait(6.0)
        self.clear_stage(VGroup(equation, final_title))

    def closing_v8(self) -> None:
        title = self.text("CIRCLE DERIVATION — NOTEBOOK SUMMARY", 46, BOLD)
        lines = VGroup(
            self.text("1.  π = P/d  →  P = πd; because d = 2r,  P = 2πr.", 34),
            self.text("2.  A vertical diameter creates two curved semicircle arcs.", 34),
            self.text("3.  Each curved semicircle arc has length  P/2 = πr.", 34),
            self.text("4.  Keep the two rows separate, then interlock the same pieces.", 34),
            self.text("5.  Shared height = r; one long base = πr; area = πr².", 34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        formula = self.big_formula(r"A=(\pi r)(r)=\pi r^2", 8.2, 62)
        group = VGroup(title, lines, formula).arrange(DOWN, buff=0.42)
        if group.height > 7.85:
            group.scale_to_fit_height(7.85)
        self.projector_safe(group, "v8 closing")

        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.95)
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 0.08) for line in lines],
                lag_ratio=0.19,
            ),
            run_time=2.90,
        )
        self.wait(2.6)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=1.00)
        self.play(Circumscribe(formula[1], color=MID_GRAY, time_width=0.9), run_time=1.20)
        self.wait(7.2)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQA --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQA --disable_caching
