#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 circle lesson V3 — modular cinematic animation layer.

Target: Manim Community Edition 0.20.1.
Visual contract: JP Classroom monochrome, projector-safe 16:9.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *


class CircleV3AreaMixin:
    """Animation mixin used by the Geometry 8 V3 circle lesson."""

    def boundary_to_surface_v3(self) -> None:
        self.set_header(
            5,
            "SAME CIRCLE — TWO DIFFERENT QUESTIONS",
            "A fence follows one-dimensional boundary length; covering the inside requires two-dimensional area.",
        )

        center = np.array([-3.4, -0.35, 0.0])
        circle = Circle(radius=1.65, stroke_color=BLACK_LINE, stroke_width=7).move_to(center)
        tracer = Dot(circle.point_at_angle(0), radius=0.075, color=BLACK_LINE)
        boundary_label = self.text("AROUND", 27, BOLD).next_to(circle, UP, buff=0.18)
        length_badge = self._unit_badge(r"\text{cm}", [2.5, 0.75, 0])
        area_badge = self._unit_badge(r"\text{cm}^2", [5.0, 0.75, 0])
        arrow_units = Arrow(
            length_badge.get_right() + RIGHT * 0.05,
            area_badge.get_left() + LEFT * 0.05,
            color=MID_GRAY, stroke_width=2.0, tip_length=0.12, buff=0.10,
        )
        q1 = self.text("boundary length", 23, BOLD).next_to(length_badge, DOWN, buff=0.15)
        q2 = self.text("covered surface", 23, BOLD).next_to(area_badge, DOWN, buff=0.15)

        filled = Circle(
            radius=1.65,
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.72,
        ).move_to(center)
        radial_lines = VGroup(*[
            Line(center, filled.point_at_angle(a), color=VERY_LIGHT_GRAY, stroke_width=1.2)
            for a in np.linspace(0, TAU, 28, endpoint=False)
        ])
        inside_label = self.text("INSIDE", 27, BOLD).next_to(filled, UP, buff=0.18)

        decision = self.formula_panel(
            r"\text{around}\Rightarrow C\qquad\text{inside}\Rightarrow A",
            width=8.3, height=1.05, font_size=39,
        ).move_to(DOWN * 2.75)
        group = VGroup(circle, boundary_label, length_badge, area_badge, arrow_units, q1, q2, decision)
        self.assert_content_safe(group, "V3 boundary surface")

        self.play(Create(circle), FadeIn(boundary_label), run_time=RUN_NORMAL)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.35)
        self.play(FadeIn(length_badge), FadeIn(q1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Transform(circle, filled), FadeOut(boundary_label), FadeIn(inside_label), run_time=RUN_SLOW)
        self.play(LaggedStart(*[Create(line) for line in radial_lines], lag_ratio=0.02), run_time=RUN_SLOW)
        self.play(GrowArrow(arrow_units), FadeIn(area_badge), FadeIn(q2), run_time=RUN_NORMAL)
        self.play(FadeIn(decision, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def derive_area_sectors_v3(self) -> None:
        self.set_header(
            6,
            "CUT AND REARRANGE — SEE WHY A = pi r²",
            "Alternating thin sectors make an almost-rectangle: its height is r and its base approaches half the circumference.",
        )

        n = 20
        r = 1.52
        delta = TAU / n
        source_center = np.array([-4.45, 0.20, 0.0])
        source = VGroup()
        for i in range(n):
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=i * delta,
                stroke_color=BLACK_LINE,
                stroke_width=1.0,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1.0,
            )
            sec.shift(source_center)
            source.add(sec)

        outline = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=3).move_to(source_center)
        radius = Line(source_center, source_center + RIGHT * r, color=BLACK_LINE, stroke_width=3)
        r_label = self.math("r", 32).next_to(radius, UP, buff=0.08)
        slice_note = self.text("20 thin sectors", 22, BOLD).next_to(outline, DOWN, buff=0.16)

        target_center_x = 3.05
        target_center_y = 0.15
        # Two alternating sectors form one visual "tooth". Half the outer
        # arc length per sector gives a compact row whose width approaches pi*r.
        spacing = PI * r / n
        targets = VGroup()
        for i in range(n):
            x = target_center_x + (i - (n - 1) / 2) * spacing
            if i % 2 == 0:
                start = PI / 2 - delta / 2
                pivot = np.array([x, target_center_y - r / 2, 0.0])
            else:
                start = -PI / 2 - delta / 2
                pivot = np.array([x, target_center_y + r / 2, 0.0])
            tgt = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=start,
                stroke_color=BLACK_LINE,
                stroke_width=1.0,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1.0,
            )
            tgt.shift(pivot)
            targets.add(tgt)

        base = Line([0.72, -1.45, 0], [5.38, -1.45, 0], color=BLACK_LINE, stroke_width=2.5)
        base_brace = Brace(base, DOWN, buff=0.10, color=BLACK_LINE)
        base_label = self.math(r"\frac{C}{2}=\pi r", 34).next_to(base_brace, DOWN, buff=0.08)
        height = DoubleArrow(
            [5.72, -0.61, 0], [5.72, 0.91, 0],
            color=BLACK_LINE, stroke_width=2.2, buff=0.03, tip_length=0.11,
        )
        height_label = self.math("r", 34).next_to(height, RIGHT, buff=0.10)

        e1 = self.math(r"A\approx (\pi r)(r)", 44).move_to([0.15, -2.72, 0])
        e2 = self.math(r"\boxed{A=\pi r^2}", 50).move_to([0.15, -2.72, 0])
        group = VGroup(source, outline, radius, r_label, slice_note, targets, base,
                       base_brace, base_label, height, height_label, e2)
        self.assert_content_safe(group, "V3 area sectors")

        self.play(Create(outline), GrowFromPoint(radius, source_center), Write(r_label), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(s) for s in source], lag_ratio=0.025), run_time=RUN_SLOW * 1.35)
        self.play(FadeIn(slice_note), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        self.play(FadeOut(outline), FadeOut(radius), FadeOut(r_label), FadeOut(slice_note), run_time=RUN_QUICK)
        self.play(
            LaggedStart(*[Transform(s, t) for s, t in zip(source, targets)], lag_ratio=0.025),
            run_time=RUN_SLOW * 2.4,
        )
        self.play(Create(base), GrowFromCenter(base_brace), Write(base_label), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(height), Write(height_label), run_time=RUN_NORMAL)
        self.play(Write(e1), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(Transform(e1, e2), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
