#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final lower-margin fixes for Geometry 8 Circle V4 senior QA."""
from __future__ import annotations
import numpy as np
from manim import *
from jp_classroom_style import *
from Geometry8_Circle_V4_Senior_QA import V4_EXPLAIN, V4_THINK, V4_FINAL, V4_SUMMARY


class CircleV4SeniorQAFixesMixin:
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
        radius = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=4)
        r_label = self.math("r", 46).next_to(radius, UP, buff=0.12)
        cut_note = self._v4_text_panel("STEP 1 — CUT", ["Same circle. Same area. 20 sectors."],
            width=7.2, title_size=32, body_size=29, fill_color=PAPER_GRAY).move_to(DOWN * 2.82)
        self.assert_content_safe(VGroup(outline, radius, r_label, sectors, cut_note), "V4 area cut final margin")
        self.play(Create(outline), GrowFromPoint(radius, center), Write(r_label), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.028), run_time=RUN_SLOW * 1.60)
        self.play(FadeIn(cut_note), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(outline, sectors, radius, r_label), width=6.7, pause=V4_THINK)
        self.play(FadeOut(outline), FadeOut(radius), FadeOut(r_label), FadeOut(cut_note), run_time=RUN_QUICK)
        spacing = PI * r / n; targets = VGroup()
        for i in range(n):
            x = (i - (n - 1) / 2) * spacing
            if i % 2 == 0:
                start = PI / 2 - delta / 2; pivot = np.array([x, -0.05 - r / 2, 0.0])
            else:
                start = -PI / 2 - delta / 2; pivot = np.array([x, -0.05 + r / 2, 0.0])
            targets.add(AnnularSector(inner_radius=0, outer_radius=r, angle=delta, start_angle=start,
                stroke_color=BLACK_LINE, stroke_width=1.35,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE, fill_opacity=1).shift(pivot))
        self.play(LaggedStart(*[Transform(s, t) for s, t in zip(sectors, targets)], lag_ratio=0.030),
                  run_time=RUN_SLOW * 2.90)
        self._v4_zoom(sectors, width=9.0, pause=V4_THINK)
        base = Line([-3.35, -2.35, 0], [3.35, -2.35, 0], color=BLACK_LINE, stroke_width=3.2)
        base_brace = Brace(base, DOWN, buff=0.11, color=BLACK_LINE)
        base_label = self.math(r"\frac{C}{2}=\pi r", 46).next_to(base_brace, DOWN, buff=0.09)
        height = DoubleArrow([3.80, -1.12, 0], [3.80, 1.08, 0], color=BLACK_LINE,
                             stroke_width=2.8, buff=0.03, tip_length=0.14)
        height_label = self.math("r", 46).next_to(height, RIGHT, buff=0.12)
        self.play(Create(base), GrowFromCenter(base_brace), Write(base_label), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(height), Write(height_label), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(sectors, base, base_brace, base_label, height, height_label), width=10.2, pause=V4_EXPLAIN)
        geometry = VGroup(sectors, base, base_brace, base_label, height, height_label)
        self.play(geometry.animate.shift(UP * 0.55), run_time=RUN_NORMAL)
        f1 = self._v4_formula_panel(r"A\approx(\pi r)(r)", width=7.0, height=1.45, size=58).move_to(DOWN * 3.12)
        f2 = self._v4_formula_panel(r"\boxed{A=\pi r^2}", width=7.0, height=1.45, size=66).move_to(f1)
        self.assert_content_safe(f1, "V4 area formula final margin")
        self.play(FadeIn(f1, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(V4_EXPLAIN)
        self.play(Transform(f1, f2), run_time=RUN_SLOW * 1.10)
        self._v4_zoom(f1, width=7.6, pause=V4_FINAL)
        self.clear_stage()

    def exercise_radius_area_v4(self) -> None:
        self._v4_header(8, "EXERCISE 2 — RADIUS GIVEN",
            "A circular sticker has radius 5 cm. Find its area and explain why the result uses square centimeters.")
        center = np.array([0.0, -0.15, 0.0])
        circle = Circle(radius=2.30, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        radius = Line(center, center + RIGHT * 2.30, color=BLACK_LINE, stroke_width=5)
        r_label = self.math(r"r=5\text{ cm}", 50).next_to(radius, UP, buff=0.14)
        ask = self._v4_text_panel("THINK FIRST", ["Which formula uses r directly?", "What unit should area use?"],
            width=6.3, title_size=34, body_size=30, fill_color=PAPER_GRAY).move_to([4.55, -0.30, 0])
        self.assert_content_safe(VGroup(circle, radius, r_label, ask), "V4 exercise 2 prompt final")
        self.play(Create(circle), GrowFromPoint(radius, center), Write(r_label), FadeIn(ask), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(circle, radius, r_label), width=6.8, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(ask), VGroup(circle, radius, r_label).animate.shift(LEFT * 3.25), run_time=RUN_NORMAL)
        p1 = self._v4_formula_panel(r"A=\pi r^2", width=5.8, height=1.45, size=62).move_to([3.85, 1.05, 0])
        p2 = self._v4_formula_panel(r"A=\pi(5)^2=25\pi", width=6.5, height=1.45, size=56).move_to([3.85, -0.65, 0])
        p3 = self._v4_formula_panel(r"A\approx78.5\text{ cm}^2", width=6.5, height=1.45, size=58).move_to([3.85, -2.35, 0])
        self.play(FadeIn(p1), run_time=RUN_NORMAL); self._v4_zoom(p1, width=6.5, pause=V4_EXPLAIN)
        fill = circle.copy().set_fill(LIGHT_GRAY, opacity=0.65).set_stroke(BLACK_LINE, width=5)
        self.play(Transform(circle, fill), FadeIn(p2), run_time=RUN_NORMAL); self._v4_zoom(p2, width=7.0, pause=V4_EXPLAIN)
        self.play(FadeIn(p3), run_time=RUN_NORMAL); self._v4_zoom(p3, width=7.0, pause=V4_THINK)
        unit = self._v4_text_panel("UNIT CHECK", ["Area covers a surface → use square units."],
            width=8.2, title_size=32, body_size=30, fill_color=PAPER_GRAY).move_to(DOWN * 2.92)
        self.assert_content_safe(unit, "V4 unit check final margin")
        self.play(FadeOut(p1), FadeOut(p2), VGroup(circle, radius, r_label).animate.shift(UP * 0.35),
                  p3.animate.move_to([2.2, -0.75, 0]), run_time=RUN_NORMAL)
        self.play(FadeIn(unit), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(p3, unit), width=9.0, pause=V4_SUMMARY)
        self.clear_stage()
