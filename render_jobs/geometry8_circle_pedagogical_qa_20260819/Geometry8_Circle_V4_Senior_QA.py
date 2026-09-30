#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 circle lesson V4 — senior projector/readability QA layer.

Purpose
-------
Rebuild the V3 choreography for real classroom projection:
- one focal idea at a time;
- substantially larger geometry and typography;
- no dense text spilling outside panels;
- deliberate think/read pauses;
- visible camera zooms around the geometric action;
- full-size sector rearrangement and worked examples.

Target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *

from Geometry8_Circle_Measurement_To_Area_20260823 import (
    SAMPLE_DATA,
    SAMPLE_MEAN,
    SAMPLE_RATIOS,
)

V4_READ = 2.60
V4_EXPLAIN = 3.60
V4_THINK = 5.20
V4_SUMMARY = 5.80
V4_FINAL = 7.00


class CircleV4SeniorQAMixin:
    """Projector-first redesign layered on top of the audited V3 primitives."""

    def _v4_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(width=0.90, height=0.62, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
        number_text = self.text(f"{number:02d}", 28, BOLD).move_to(number_box)
        title_mob = self.text(title, 44, BOLD)
        self.fit(title_mob, 13.55, 0.72)
        title_row = VGroup(VGroup(number_box, number_text), title_mob).arrange(RIGHT, buff=0.28)
        title_row.to_edge(UP, buff=0.14).to_edge(LEFT, buff=0.46)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2.2)
        rule.next_to(title_row, DOWN, buff=0.08)
        words = subtitle.split()
        if len(subtitle) > 86:
            half = len(words) // 2
            best = min(range(max(1, half - 6), min(len(words), half + 7)),
                key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
            lines = [" ".join(words[:best]), " ".join(words[best:])]
        else:
            lines = [subtitle]
        subtitle_mob = VGroup(*[self.text(line, 27) for line in lines])
        subtitle_mob.arrange(DOWN, aligned_edge=LEFT, buff=0.045)
        self.fit(subtitle_mob, 14.15, 0.86)
        subtitle_mob.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)
        new_header = VGroup(title_row, rule)
        if self.header_group is None:
            self.header_group = new_header
            self.add(new_header)
        else:
            old = self.header_group
            self.header_group = new_header
            self.play(ReplacementTransform(old, new_header), run_time=RUN_QUICK)
        if self.subtitle_group is None:
            self.subtitle_group = subtitle_mob
            self.add(subtitle_mob)
        else:
            old = self.subtitle_group
            self.subtitle_group = subtitle_mob
            self.play(ReplacementTransform(old, subtitle_mob), run_time=RUN_QUICK)

    def _v4_panel(self, content: Mobject, *, width: float, height: float,
                  fill_color=WHITE, padding: float = 0.44, stroke_width: float = 2.2) -> VGroup:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.15,
            stroke_color=BLACK_LINE, stroke_width=stroke_width,
            fill_color=fill_color, fill_opacity=1)
        self.fit(content, width - 2 * padding, height - 2 * padding)
        content.move_to(box)
        panel = VGroup(box, content)
        if content.get_left()[0] < box.get_left()[0] + 0.12:
            raise ValueError("V4 panel content exceeds left padding")
        if content.get_right()[0] > box.get_right()[0] - 0.12:
            raise ValueError("V4 panel content exceeds right padding")
        if content.get_top()[1] > box.get_top()[1] - 0.10:
            raise ValueError("V4 panel content exceeds top padding")
        if content.get_bottom()[1] < box.get_bottom()[1] + 0.10:
            raise ValueError("V4 panel content exceeds bottom padding")
        return panel

    def _v4_text_panel(self, title: str, lines: list[str], *, width: float = 10.6,
                       title_size: int = 34, body_size: int = 30, fill_color=WHITE) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        height = max(1.55, content.height + 0.82)
        return self._v4_panel(content, width=width, height=height, fill_color=fill_color)

    def _v4_formula_panel(self, expression: str, *, width=7.6, height=1.45, size=56) -> VGroup:
        return self._v4_panel(self.math(expression, size), width=width, height=height, fill_color=PAPER_GRAY)

    def _v4_zoom(self, mob: Mobject, *, width: float = 8.0, pause: float = V4_READ) -> None:
        persistent = [m for m in (self.header_group, self.subtitle_group) if m is not None]
        if persistent:
            self.play(*[FadeOut(m) for m in persistent], run_time=RUN_QUICK)
        self.camera.frame.save_state()
        required_width = max(width, mob.width + 0.85, (mob.height + 0.75) * FRAME_WIDTH / FRAME_HEIGHT)
        required_width = min(required_width, FRAME_WIDTH)
        self.play(self.camera.frame.animate.set(width=required_width).move_to(mob),
                  run_time=RUN_CAMERA * 1.35)
        self.wait(pause)
        self.play(Restore(self.camera.frame), run_time=RUN_CAMERA * 1.20)
        if persistent:
            self.play(*[FadeIn(m) for m in persistent], run_time=RUN_QUICK)

    def opening_measurement_bridge_v4(self) -> None:
        course = self.text("GEOMETRY 8", 32, BOLD)
        title = self.text("CIRCLES — MEASURE, DISCOVER, EXPLAIN", 58, BOLD)
        subtitle = self.text("Use your three measured objects to discover pi, circumference, diameter, radius, and area.", 31)
        self.fit(subtitle, 13.6, 0.75)
        circles = VGroup()
        for x, r in [(-2.65, 0.86), (0.0, 1.12), (2.95, 1.40)]:
            circles.add(Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=4).move_to([x, -0.80, 0]))
        baseline = Line(LEFT * 4.55, RIGHT * 4.55, color=LIGHT_GRAY, stroke_width=2.5).move_to(DOWN * 2.48)
        question = self._v4_formula_panel(r"\frac{C}{d}\;=?", width=4.2, height=1.30, size=64).move_to(DOWN * 3.25)
        top = VGroup(course, title, subtitle).arrange(DOWN, buff=0.27).move_to(UP * 1.75)
        group = VGroup(top, circles, baseline, question)
        self.fit(group, 14.6, 8.35)
        self.assert_within_frame(group, "V4 opening", margin=0.18)
        self.play(FadeIn(course, shift=UP * 0.14), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW * 1.20)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.wait(V4_READ)
        self.play(Create(baseline), run_time=RUN_QUICK)
        self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.20), run_time=RUN_SLOW * 1.60)
        self.play(FadeIn(question, shift=UP * 0.12), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circles, question), width=10.2, pause=V4_EXPLAIN)
        self.wait(V4_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def measure_three_objects_v4(self) -> None:
        self._v4_header(1, "MEASURE ONE OBJECT AT A TIME",
            "For every circular object: measure diameter d, trace circumference C, then calculate C / d.")
        results = []
        radii = [1.95, 2.10, 1.82]
        for idx, ((_, d, c), rr) in enumerate(zip(SAMPLE_DATA, radii)):
            letter = "ABC"[idx]
            center = np.array([-3.55, -0.45, 0.0])
            outer = Circle(radius=rr, stroke_color=BLACK_LINE, stroke_width=5).move_to(center)
            inner1 = Circle(radius=rr * 0.72, stroke_color=LIGHT_GRAY, stroke_width=2).move_to(center)
            inner2 = Circle(radius=rr * 0.49, stroke_color=LIGHT_GRAY, stroke_width=1.6).move_to(center)
            name = self.text(f"OBJECT {letter}", 36, BOLD).next_to(outer, UP, buff=0.20)
            diameter = DoubleArrow(outer.get_left(), outer.get_right(), buff=0.03, tip_length=0.16,
                color=BLACK_LINE, stroke_width=3.2)
            d_label = self.math(rf"d={d:.1f}\text{{ cm}}", 46).next_to(diameter, DOWN, buff=0.15)
            trace = Circle(radius=rr, stroke_color=BLACK_LINE, stroke_width=9).move_to(center)
            tracer = Dot(trace.point_at_angle(0), radius=0.095, color=BLACK_LINE)
            measurement = VGroup(self.text("MEASURED", 30, BOLD),
                self.math(rf"d={d:.1f}\text{{ cm}}", 46), self.math(rf"C={c:.1f}\text{{ cm}}", 46)).arrange(DOWN, buff=0.23)
            measured_panel = self._v4_panel(measurement, width=5.5, height=2.85).move_to([4.05, 0.15, 0])
            ratio_formula = self.math(rf"\frac{{C}}{{d}}=\frac{{{c:.1f}}}{{{d:.1f}}}\approx {c/d:.3f}", 54)
            ratio_panel = self._v4_panel(ratio_formula, width=6.0, height=1.65, fill_color=PAPER_GRAY).move_to([4.05, -2.15, 0])
            all_content = VGroup(outer, inner1, inner2, name, diameter, d_label, measured_panel, ratio_panel)
            self.assert_content_safe(all_content, f"V4 object {letter}")
            self.play(Create(outer), FadeIn(inner1), FadeIn(inner2), FadeIn(name), run_time=RUN_NORMAL)
            self._v4_zoom(VGroup(outer, name), width=6.8, pause=V4_READ)
            self.play(GrowFromCenter(diameter), Write(d_label), run_time=RUN_NORMAL * 1.15)
            self._v4_zoom(VGroup(outer, diameter, d_label), width=7.3, pause=V4_EXPLAIN)
            self.play(Create(trace), MoveAlongPath(tracer, trace), run_time=RUN_SLOW * 2.05)
            self.play(FadeOut(tracer), FadeIn(measured_panel, shift=LEFT * 0.12), run_time=RUN_NORMAL)
            self.wait(V4_READ)
            self.play(FadeIn(ratio_panel, shift=UP * 0.10), run_time=RUN_NORMAL)
            self._v4_zoom(ratio_panel, width=7.2, pause=V4_THINK)
            results.append((letter, d, c, c / d))
            self.clear_stage()
        self._v4_header(1, "COMPARE THE THREE RESULTS",
            "Different-sized objects give nearly the same C / d value. Compare these illustrative values with your own data.")
        rows = VGroup()
        for letter, d, c, ratio in results:
            row = VGroup(self.text(f"OBJECT {letter}", 31, BOLD), self.math(rf"d={d:.1f}\text{{ cm}}", 38),
                self.math(rf"C={c:.1f}\text{{ cm}}", 38), self.math(rf"C/d={ratio:.3f}", 40)).arrange(RIGHT, buff=0.75)
            self.fit(row, 12.7, 0.72)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        board = self._v4_panel(rows, width=13.7, height=3.65).move_to(DOWN * 0.25)
        caption = self._v4_text_panel("WHAT SHOULD YOU NOTICE?",
            ["The three ratios cluster near the same number: about 3.14."], width=11.2,
            title_size=32, body_size=30, fill_color=PAPER_GRAY).move_to(DOWN * 2.75)
        self.assert_content_safe(VGroup(board, caption), "V4 measurement board")
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in rows], lag_ratio=0.18), run_time=RUN_SLOW * 1.45)
        self.wait(V4_EXPLAIN)
        self.play(FadeIn(caption), run_time=RUN_NORMAL)
        self._v4_zoom(board, width=13.0, pause=V4_THINK)
        self.clear_stage()

    def discover_pi_v4(self) -> None:
        self._v4_header(2, "THE STABLE RATIO IS PI",
            "Measurement error changes the last decimals, but C / d stays close to 3.14 for every circle.")
        badges = VGroup()
        for x, ratio, letter in zip([-4.4, 0.0, 4.4], SAMPLE_RATIOS, "ABC"):
            content = VGroup(self.text(f"OBJECT {letter}", 28, BOLD), self.math(rf"{ratio:.3f}", 62)).arrange(DOWN, buff=0.18)
            badges.add(self._v4_panel(content, width=3.55, height=2.05, fill_color=PAPER_GRAY).move_to([x, 0.30, 0]))
        mean = self._v4_formula_panel(rf"\text{{mean}}\left(\frac{{C}}{{d}}\right)\approx {SAMPLE_MEAN:.3f}",
            width=8.3, height=1.55, size=52).move_to(DOWN * 1.55)
        pi_formula = self._v4_formula_panel(r"\boxed{\frac{C}{d}=\pi}", width=6.4, height=1.65, size=66).move_to(DOWN * 2.95)
        self.assert_content_safe(VGroup(badges, mean, pi_formula), "V4 pi")
        self.play(LaggedStart(*[FadeIn(b, scale=0.94) for b in badges], lag_ratio=0.20), run_time=RUN_SLOW * 1.35)
        self.wait(V4_EXPLAIN)
        self.play(FadeIn(mean, shift=UP * 0.10), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(badges, mean), width=12.8, pause=V4_THINK)
        self.play(FadeIn(pi_formula, shift=UP * 0.10), run_time=RUN_SLOW)
        self._v4_zoom(pi_formula, width=7.0, pause=V4_SUMMARY)
        self.clear_stage()

    def elements_radius_diameter_v4(self) -> None:
        self._v4_header(3, "BUILD THE CIRCLE FROM THE CENTER",
            "First radius, then diameter, then circumference. Each element is shown separately at projector scale.")
        center = np.array([-2.55, -0.35, 0.0]); r = 2.25
        o = Dot(center, radius=0.10, color=BLACK_LINE); o_label = self.math("O", 40).next_to(o, UL, buff=0.12)
        radius = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=5); r_label = self.math("r", 52).next_to(radius, UP, buff=0.14)
        opposite = Line(center, center + LEFT * r, color=MID_GRAY, stroke_width=5)
        diameter = Line(center + LEFT * r, center + RIGHT * r, color=BLACK_LINE, stroke_width=6); d_label = self.math("d", 52).next_to(diameter, DOWN, buff=0.16)
        circle = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=7).move_to(center); tracer = Dot(circle.point_at_angle(0), radius=0.10, color=BLACK_LINE)
        formula = self._v4_formula_panel(r"d=2r", width=4.8, height=1.50, size=64).move_to([4.35, 0.75, 0])
        c_formula = self._v4_formula_panel(r"C=\pi d=2\pi r", width=6.1, height=1.55, size=58).move_to([4.35, -1.10, 0])
        unit_panel = self._v4_text_panel("LINEAR MEASUREMENTS", ["r, d, and C use units such as cm or m."],
            width=6.3, title_size=30, body_size=27).move_to([4.35, -2.70, 0])
        self.assert_content_safe(VGroup(o, o_label, radius, r_label, opposite, diameter, d_label, circle, formula, c_formula, unit_panel), "V4 elements")
        self.play(FadeIn(o), Write(o_label), run_time=RUN_QUICK)
        self.play(GrowFromPoint(radius, center), Write(r_label), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(o, o_label, radius, r_label), width=6.5, pause=V4_EXPLAIN)
        self.play(GrowFromPoint(opposite, center), run_time=RUN_NORMAL)
        self.play(ReplacementTransform(VGroup(radius.copy(), opposite.copy()), diameter), Write(d_label), run_time=RUN_SLOW)
        self.play(FadeIn(formula, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(diameter, d_label, formula), width=9.0, pause=V4_THINK)
        self.play(Create(circle), MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.90)
        self.play(FadeOut(tracer), FadeIn(c_formula), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, c_formula), width=10.5, pause=V4_EXPLAIN)
        self.play(FadeIn(unit_panel), run_time=RUN_NORMAL)
        self.wait(V4_SUMMARY)
        self.clear_stage()

    def unwrap_circumference_v4(self) -> None:
        self._v4_header(4, "UNWRAP THE BORDER",
            "Circumference is a length. Watch the circular border become one straight segment of the same length.")
        center = np.array([-3.7, -0.20, 0.0])
        circle = Circle(radius=2.00, stroke_color=BLACK_LINE, stroke_width=9).move_to(center)
        diameter = DoubleArrow(circle.get_left(), circle.get_right(), buff=0.03, tip_length=0.16, color=BLACK_LINE, stroke_width=3.0)
        d_label = self.math("d", 48).next_to(diameter, DOWN, buff=0.14); tracer = Dot(circle.point_at_angle(0), radius=0.10, color=BLACK_LINE)
        unwrapped = Line([-0.35, -0.20, 0], [6.45, -0.20, 0], color=BLACK_LINE, stroke_width=9)
        brace = Brace(unwrapped, DOWN, buff=0.15, color=BLACK_LINE); c_label = self.math("C", 48).next_to(brace, DOWN, buff=0.12)
        arrow = Arrow([-1.25, -0.20, 0], [-0.52, -0.20, 0], color=MID_GRAY, stroke_width=3, tip_length=0.14)
        equation = self._v4_formula_panel(r"\frac{C}{d}=\pi", width=5.2, height=1.45, size=60).move_to([2.95, -2.55, 0])
        eq2 = self._v4_formula_panel(r"C=\pi d", width=5.2, height=1.45, size=64).move_to(equation)
        eq3 = self._v4_formula_panel(r"C=2\pi r", width=5.2, height=1.45, size=64).move_to(equation)
        self.assert_content_safe(VGroup(circle, diameter, d_label, unwrapped, brace, c_label, arrow, equation), "V4 unwrap")
        self.play(Create(circle), GrowFromCenter(diameter), Write(d_label), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, diameter, d_label), width=6.6, pause=V4_READ)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 2.05)
        self.play(FadeOut(tracer), GrowArrow(arrow), run_time=RUN_QUICK)
        border_copy = circle.copy(); self.add(border_copy)
        self.play(Transform(border_copy, unwrapped), run_time=RUN_SLOW * 1.75)
        self.play(GrowFromCenter(brace), Write(c_label), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(border_copy, brace, c_label), width=9.2, pause=V4_EXPLAIN)
        self.play(FadeIn(equation), run_time=RUN_NORMAL); self._v4_zoom(equation, width=6.0, pause=V4_THINK)
        self.play(Transform(equation, eq2), run_time=RUN_SLOW); self.wait(V4_EXPLAIN)
        self.play(Transform(equation, eq3), run_time=RUN_SLOW); self._v4_zoom(equation, width=6.0, pause=V4_SUMMARY)
        self.clear_stage()

    def boundary_to_surface_v4(self) -> None:
        self._v4_header(5, "AROUND OR INSIDE?",
            "The same circle answers two different questions: boundary length C or covered surface A.")
        center = np.array([-2.65, -0.30, 0.0]); r = 2.20
        circle = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=9).move_to(center); tracer = Dot(circle.point_at_angle(0), radius=0.10, color=BLACK_LINE)
        around = self.text("AROUND", 40, BOLD).next_to(circle, UP, buff=0.18)
        linear = self._v4_text_panel("BOUNDARY LENGTH", ["Use C", "Units: cm, m, ..."], width=5.3, title_size=32, body_size=31).move_to([4.20, 0.55, 0])
        filled = circle.copy().set_fill(LIGHT_GRAY, opacity=0.70).set_stroke(BLACK_LINE, width=5)
        inside = self.text("INSIDE", 40, BOLD).next_to(filled, UP, buff=0.18)
        square = self._v4_text_panel("COVERED SURFACE", ["Use A", "Units: cm², m², ..."], width=5.3, title_size=32, body_size=31, fill_color=PAPER_GRAY).move_to([4.20, -1.70, 0])
        decision = self._v4_formula_panel(r"\text{around}\Rightarrow C\qquad\text{inside}\Rightarrow A", width=10.2, height=1.40, size=50).move_to(DOWN * 3.20)
        self.assert_content_safe(VGroup(circle, around, linear, square, decision), "V4 boundary surface")
        self.play(Create(circle), FadeIn(around), run_time=RUN_NORMAL)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.85)
        self.play(FadeOut(tracer), FadeIn(linear, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, around, linear), width=10.5, pause=V4_THINK)
        self.play(Transform(circle, filled), Transform(around, inside), run_time=RUN_SLOW)
        self.play(FadeIn(square, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, around, square), width=10.5, pause=V4_THINK)
        self.play(FadeIn(decision), run_time=RUN_NORMAL); self._v4_zoom(decision, width=10.8, pause=V4_SUMMARY)
        self.clear_stage()

    def derive_area_sectors_v4(self) -> None:
        self._v4_header(6, "CUT THE CIRCLE — THEN REARRANGE IT",
            "Twenty thin sectors alternate up and down. Their total area does not change when we rearrange them.")
        n = 20; r = 2.20; delta = TAU / n; center = np.array([0.0, -0.35, 0.0])
        sectors = VGroup()
        for i in range(n):
            sectors.add(AnnularSector(inner_radius=0, outer_radius=r, angle=delta, start_angle=i * delta,
                stroke_color=BLACK_LINE, stroke_width=1.35,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE, fill_opacity=1).shift(center))
        outline = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=5).move_to(center)
        radius = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=4); r_label = self.math("r", 46).next_to(radius, UP, buff=0.12)
        cut_note = self._v4_text_panel("STEP 1 — CUT", ["Same circle. Same area. 20 sectors."], width=7.2, title_size=32, body_size=29, fill_color=PAPER_GRAY).move_to(DOWN * 3.10)
        self.assert_content_safe(VGroup(outline, radius, r_label, sectors, cut_note), "V4 area cut")
        self.play(Create(outline), GrowFromPoint(radius, center), Write(r_label), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.028), run_time=RUN_SLOW * 1.60)
        self.play(FadeIn(cut_note), run_time=RUN_NORMAL); self._v4_zoom(VGroup(outline, sectors, radius, r_label), width=6.7, pause=V4_THINK)
        self.play(FadeOut(outline), FadeOut(radius), FadeOut(r_label), FadeOut(cut_note), run_time=RUN_QUICK)
        target_center_x = 0.0; target_center_y = -0.05; spacing = PI * r / n; targets = VGroup()
        for i in range(n):
            x = target_center_x + (i - (n - 1) / 2) * spacing
            if i % 2 == 0:
                start = PI / 2 - delta / 2; pivot = np.array([x, target_center_y - r / 2, 0.0])
            else:
                start = -PI / 2 - delta / 2; pivot = np.array([x, target_center_y + r / 2, 0.0])
            targets.add(AnnularSector(inner_radius=0, outer_radius=r, angle=delta, start_angle=start,
                stroke_color=BLACK_LINE, stroke_width=1.35,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE, fill_opacity=1).shift(pivot))
        self.play(LaggedStart(*[Transform(s, t) for s, t in zip(sectors, targets)], lag_ratio=0.030), run_time=RUN_SLOW * 2.90)
        self._v4_zoom(sectors, width=9.0, pause=V4_THINK)
        base = Line([-3.35, -2.35, 0], [3.35, -2.35, 0], color=BLACK_LINE, stroke_width=3.2)
        base_brace = Brace(base, DOWN, buff=0.11, color=BLACK_LINE); base_label = self.math(r"\frac{C}{2}=\pi r", 46).next_to(base_brace, DOWN, buff=0.09)
        height = DoubleArrow([3.80, -1.12, 0], [3.80, 1.08, 0], color=BLACK_LINE, stroke_width=2.8, buff=0.03, tip_length=0.14)
        height_label = self.math("r", 46).next_to(height, RIGHT, buff=0.12)
        self.play(Create(base), GrowFromCenter(base_brace), Write(base_label), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(height), Write(height_label), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(sectors, base, base_brace, base_label, height, height_label), width=10.2, pause=V4_EXPLAIN)
        geometry = VGroup(sectors, base, base_brace, base_label, height, height_label)
        self.play(geometry.animate.shift(UP * 0.55), run_time=RUN_NORMAL)
        f1 = self._v4_formula_panel(r"A\approx(\pi r)(r)", width=7.0, height=1.45, size=58).move_to(DOWN * 3.12)
        f2 = self._v4_formula_panel(r"\boxed{A=\pi r^2}", width=7.0, height=1.45, size=66).move_to(f1)
        self.play(FadeIn(f1, shift=UP * 0.10), run_time=RUN_NORMAL); self.wait(V4_EXPLAIN)
        self.play(Transform(f1, f2), run_time=RUN_SLOW * 1.10); self._v4_zoom(f1, width=7.6, pause=V4_FINAL)
        self.clear_stage()

    def exercise_diameter_v4(self) -> None:
        self._v4_header(7, "EXERCISE 1 — DIAMETER GIVEN",
            "A circular lid has diameter 14 cm. Find radius, circumference, and area. Check the units.")
        center = np.array([0.0, -0.20, 0.0]); circle = Circle(radius=2.25, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        diameter = DoubleArrow(circle.get_left(), circle.get_right(), buff=0.03, tip_length=0.16, color=BLACK_LINE, stroke_width=3.2)
        d_label = self.math(r"d=14\text{ cm}", 50).next_to(diameter, DOWN, buff=0.15)
        ask = self._v4_text_panel("YOUR TURN", ["1. Find r", "2. Find C", "3. Find A"], width=5.0, title_size=34, body_size=31, fill_color=PAPER_GRAY).move_to([5.10, -0.15, 0])
        self.assert_content_safe(VGroup(circle, diameter, d_label, ask), "V4 exercise 1 prompt")
        self.play(Create(circle), GrowFromCenter(diameter), Write(d_label), FadeIn(ask), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, diameter, d_label), width=6.8, pause=V4_THINK); self.wait(V4_THINK)
        self.play(FadeOut(ask), circle.animate.shift(LEFT * 3.20), diameter.animate.shift(LEFT * 3.20), d_label.animate.shift(LEFT * 3.20), run_time=RUN_NORMAL)
        half = Line(circle.get_center(), circle.get_center() + RIGHT * 2.25, color=MID_GRAY, stroke_width=5); r_label = self.math(r"r=7\text{ cm}", 44).next_to(half, UP, buff=0.12)
        step1 = self._v4_formula_panel(r"r=\frac{d}{2}=7\text{ cm}", width=6.6, height=1.45, size=54).move_to([3.75, 0.95, 0])
        step2 = self._v4_formula_panel(r"C=\pi d=14\pi\approx44.0\text{ cm}", width=7.5, height=1.45, size=48).move_to([3.75, -0.75, 0])
        step3 = self._v4_formula_panel(r"A=\pi r^2=49\pi\approx153.9\text{ cm}^2", width=7.5, height=1.45, size=45).move_to([3.75, -2.45, 0])
        self.assert_content_safe(VGroup(circle, diameter, d_label, half, r_label, step1, step2, step3), "V4 exercise 1 solution")
        self.play(TransformFromCopy(diameter, half), Write(r_label), FadeIn(step1), run_time=RUN_NORMAL); self._v4_zoom(step1, width=7.0, pause=V4_EXPLAIN)
        tracer = Dot(circle.point_at_angle(0), radius=0.095, color=BLACK_LINE); self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.70)
        self.play(FadeOut(tracer), FadeIn(step2), run_time=RUN_NORMAL); self._v4_zoom(step2, width=8.0, pause=V4_EXPLAIN)
        fill = circle.copy().set_fill(LIGHT_GRAY, opacity=0.68).set_stroke(BLACK_LINE, width=5)
        self.play(Transform(circle, fill), FadeIn(step3), run_time=RUN_NORMAL); self._v4_zoom(step3, width=8.0, pause=V4_THINK)
        self.wait(V4_SUMMARY); self.clear_stage()

    def exercise_radius_area_v4(self) -> None:
        self._v4_header(8, "EXERCISE 2 — RADIUS GIVEN",
            "A circular sticker has radius 5 cm. Find its area and explain why the result uses square centimeters.")
        center = np.array([0.0, -0.15, 0.0]); circle = Circle(radius=2.30, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        radius = Line(center, center + RIGHT * 2.30, color=BLACK_LINE, stroke_width=5); r_label = self.math(r"r=5\text{ cm}", 50).next_to(radius, UP, buff=0.14)
        ask = self._v4_text_panel("THINK FIRST", ["Which formula uses r directly?", "What unit should area use?"], width=6.3, title_size=34, body_size=30, fill_color=PAPER_GRAY).move_to([4.55, -0.30, 0])
        self.assert_content_safe(VGroup(circle, radius, r_label, ask), "V4 exercise 2 prompt")
        self.play(Create(circle), GrowFromPoint(radius, center), Write(r_label), FadeIn(ask), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, radius, r_label), width=6.8, pause=V4_THINK); self.wait(V4_THINK)
        self.play(FadeOut(ask), VGroup(circle, radius, r_label).animate.shift(LEFT * 3.25), run_time=RUN_NORMAL)
        p1 = self._v4_formula_panel(r"A=\pi r^2", width=5.8, height=1.45, size=62).move_to([3.85, 1.05, 0])
        p2 = self._v4_formula_panel(r"A=\pi(5)^2=25\pi", width=6.5, height=1.45, size=56).move_to([3.85, -0.65, 0])
        p3 = self._v4_formula_panel(r"A\approx78.5\text{ cm}^2", width=6.5, height=1.45, size=58).move_to([3.85, -2.35, 0])
        self.play(FadeIn(p1), run_time=RUN_NORMAL); self._v4_zoom(p1, width=6.5, pause=V4_EXPLAIN)
        fill = circle.copy().set_fill(LIGHT_GRAY, opacity=0.65).set_stroke(BLACK_LINE, width=5)
        self.play(Transform(circle, fill), FadeIn(p2), run_time=RUN_NORMAL); self._v4_zoom(p2, width=7.0, pause=V4_EXPLAIN)
        self.play(FadeIn(p3), run_time=RUN_NORMAL); self._v4_zoom(p3, width=7.0, pause=V4_THINK)
        unit = self._v4_text_panel("UNIT CHECK", ["Area covers a surface → use square units."], width=8.2, title_size=32, body_size=30, fill_color=PAPER_GRAY).move_to(DOWN * 3.20)
        self.play(FadeOut(p1), FadeOut(p2), VGroup(circle, radius, r_label).animate.shift(UP * 0.35), p3.animate.move_to([2.2, -0.75, 0]), run_time=RUN_NORMAL)
        self.play(FadeIn(unit), run_time=RUN_NORMAL); self._v4_zoom(VGroup(p3, unit), width=9.0, pause=V4_SUMMARY)
        self.clear_stage()

    def exercise_inverse_and_context_v4(self) -> None:
        self._v4_header(9, "EXERCISE 3 — WORK BACKWARD",
            "A round table has circumference 31.4 cm. Estimate diameter and radius, then choose boundary or area by context.")
        center = np.array([0.0, -0.15, 0.0]); circle = Circle(radius=2.25, stroke_color=BLACK_LINE, stroke_width=8).move_to(center)
        c_label = self.math(r"C=31.4\text{ cm}", 50).next_to(circle, DOWN, buff=0.20)
        ask = self._v4_text_panel("WORK BACKWARD", ["1. Find d from C = pi d", "2. Find r = d / 2"], width=6.7, title_size=34, body_size=30, fill_color=PAPER_GRAY).move_to([4.55, -0.10, 0])
        self.play(Create(circle), Write(c_label), FadeIn(ask), run_time=RUN_NORMAL)
        tracer = Dot(circle.point_at_angle(0), radius=0.095, color=BLACK_LINE); self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.70)
        self.play(FadeOut(tracer), run_time=RUN_QUICK); self._v4_zoom(VGroup(circle, c_label), width=6.8, pause=V4_THINK); self.wait(V4_THINK)
        self.play(FadeOut(ask), VGroup(circle, c_label).animate.shift(LEFT * 3.25), run_time=RUN_NORMAL)
        diameter = DoubleArrow(circle.get_left(), circle.get_right(), buff=0.03, tip_length=0.14, color=MID_GRAY, stroke_width=3)
        radius = Line(circle.get_center(), circle.get_center() + RIGHT * 2.25, color=BLACK_LINE, stroke_width=4)
        s1 = self._v4_formula_panel(r"d=\frac{C}{\pi}\approx\frac{31.4}{3.14}=10\text{ cm}", width=7.6, height=1.50, size=48).move_to([3.85, 0.95, 0])
        s2 = self._v4_formula_panel(r"r=\frac{d}{2}=5\text{ cm}", width=6.6, height=1.45, size=54).move_to([3.85, -0.85, 0])
        self.play(GrowFromCenter(diameter), FadeIn(s1), run_time=RUN_NORMAL); self._v4_zoom(s1, width=8.0, pause=V4_EXPLAIN)
        self.play(GrowFromPoint(radius, circle.get_center()), FadeIn(s2), run_time=RUN_NORMAL); self._v4_zoom(s2, width=7.0, pause=V4_EXPLAIN)
        self.play(FadeOut(VGroup(diameter, radius, s1, s2, circle, c_label)), run_time=RUN_NORMAL)
        context_title = self.text("WHICH MEASUREMENT DOES THE CONTEXT REQUIRE?", 40, BOLD).move_to(UP * 1.85)
        border = self._v4_text_panel("BORDER STRIP", ["Goes around the edge", "→ circumference C"], width=6.0, title_size=36, body_size=31).move_to([-3.35, -0.25, 0])
        cover = self._v4_text_panel("SURFACE COVER", ["Covers the inside", "→ area A"], width=6.0, title_size=36, body_size=31, fill_color=PAPER_GRAY).move_to([3.35, -0.25, 0])
        self.assert_content_safe(VGroup(context_title, border, cover), "V4 exercise 3 context")
        self.play(Write(context_title), run_time=RUN_NORMAL); self.play(FadeIn(border, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self._v4_zoom(border, width=6.8, pause=V4_THINK); self.play(FadeIn(cover, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self._v4_zoom(cover, width=6.8, pause=V4_THINK); self.wait(V4_SUMMARY); self.clear_stage()

    def lesson_summary_v4(self) -> None:
        self._v4_header(10, "RETURN TO YOUR THREE REAL OBJECTS",
            "Use the same six-step method on one object you actually measured in the previous class.")
        labels = [("1", "MEASURE d"), ("2", "MEASURE C"), ("3", "CALCULATE C / d"),
                  ("4", "PREDICT C = pi d"), ("5", "FIND r = d / 2"), ("6", "CALCULATE A = pi r²")]
        cards = VGroup()
        for num, label in labels:
            content = VGroup(self.text(num, 29, BOLD), self.text(label, 29, BOLD)).arrange(RIGHT, buff=0.25)
            cards.add(self._v4_panel(content, width=4.35, height=1.25, fill_color=PAPER_GRAY))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.45)); cards.move_to([0, 0.25, 0])
        self.assert_content_safe(cards, "V4 summary cards")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.09) for c in cards], lag_ratio=0.14), run_time=RUN_SLOW * 1.65)
        self._v4_zoom(cards[:3], width=13.4, pause=V4_EXPLAIN); self._v4_zoom(cards[3:], width=13.4, pause=V4_EXPLAIN)
        self.wait(V4_THINK); self.play(FadeOut(cards), run_time=RUN_NORMAL)
        challenge = self._v4_text_panel("FINAL CHALLENGE", ["Choose one of your three measured objects.",
            "Compare measured C with predicted C = pi d.", "Then calculate its area and report the correct square unit."],
            width=12.2, title_size=40, body_size=34, fill_color=PAPER_GRAY).move_to(DOWN * 0.25)
        self.assert_content_safe(challenge, "V4 final challenge")
        self.play(FadeIn(challenge, shift=UP * 0.12), run_time=RUN_SLOW); self._v4_zoom(challenge, width=12.8, pause=V4_FINAL)
        self.wait(V4_FINAL); self.standard_closing("Measure. Discover pi. Choose C or A. Explain the unit.")
