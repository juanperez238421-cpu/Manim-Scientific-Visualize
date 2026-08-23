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

from Geometry8_Circle_Measurement_To_Area_20260823 import (
    SAMPLE_DATA,
    SAMPLE_MEAN,
    SAMPLE_RATIOS,
)


class CircleV3MeasurementMixin:
    """Animation mixin used by the Geometry 8 V3 circle lesson."""

    def opening_measurement_bridge_v3(self) -> None:
        course = self.text("GEOMETRY 8", 27, BOLD)
        title = self.text("CIRCLES — MEASURE, DISCOVER, EXPLAIN", 48, BOLD)
        subtitle = self.text(
            "Your three objects become the evidence for circumference, pi, radius, diameter, and area.",
            25,
        )
        self.fit(subtitle, 13.2, 0.75)

        circles = VGroup()
        for x, r in [(-2.2, 0.48), (0.0, 0.68), (2.3, 0.88)]:
            c = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=3)
            c.move_to([x, -1.0, 0])
            circles.add(c)
        baseline = Line(LEFT * 3.7, RIGHT * 3.7, color=LIGHT_GRAY, stroke_width=2)
        baseline.move_to(DOWN * 2.15)
        question = self.math(r"\frac{C}{d}\;=?", 48).move_to(DOWN * 3.05)

        top = VGroup(course, title, subtitle).arrange(DOWN, buff=0.25).move_to(UP * 1.65)
        group = VGroup(top, circles, baseline, question)
        self.fit(group, 14.2, 7.7)
        self.assert_within_frame(group, "V3 opening", margin=0.2)

        self.play(FadeIn(course, shift=UP * 0.14), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.play(Create(baseline), run_time=RUN_QUICK)
        self.play(
            LaggedStart(*[Create(c) for c in circles], lag_ratio=0.20),
            run_time=RUN_SLOW * 1.35,
        )
        self.play(Write(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def measure_three_objects_v3(self) -> None:
        self.set_header(
            1,
            "THREE OBJECTS — MEASURE THE SAME TWO LENGTHS",
            "The sample values are illustrative. Repeat the exact process with the three circular objects you measured.",
        )

        rows = VGroup()
        y_positions = [1.15, -0.35, -1.85]
        object_radii = [0.58, 0.68, 0.52]
        labels = ["OBJECT A", "OBJECT B", "OBJECT C"]

        for idx, ((_, d, c), y, rr, label) in enumerate(
            zip(SAMPLE_DATA, y_positions, object_radii, labels)
        ):
            center = np.array([-5.65, y, 0.0])
            disc = self._object_disc(center, rr, label, rings=1 if idx == 2 else 2)
            outer = disc[0]
            gauge = self._diameter_gauge(outer, rf"d={d:.1f}\text{{ cm}}")
            trace, tracer = self._circumference_trace(outer)
            c_label = self.math(rf"C={c:.1f}\text{{ cm}}", 29).move_to([0.1, y, 0])
            ratio = self.math(rf"C/d={c/d:.3f}", 30).move_to([4.4, y, 0])
            arrow1 = Arrow(
                [-3.80, y, 0], [-1.10, y, 0],
                color=MID_GRAY, stroke_width=2.0, buff=0.05, tip_length=0.12,
            )
            arrow2 = Arrow(
                [1.25, y, 0], [3.20, y, 0],
                color=MID_GRAY, stroke_width=2.0, buff=0.05, tip_length=0.12,
            )
            row = VGroup(disc, gauge, trace, tracer, c_label, ratio, arrow1, arrow2)
            self.assert_content_safe(row, f"V3 measured object {idx+1}")

            self.play(FadeIn(disc[3]), Create(outer), FadeIn(disc[1:3]), run_time=RUN_NORMAL)
            self.play(GrowFromCenter(gauge[0]), Write(gauge[1]), run_time=RUN_NORMAL)
            self.play(Create(trace), MoveAlongPath(tracer, trace), run_time=RUN_SLOW * 1.45)
            self.play(FadeIn(c_label), GrowArrow(arrow1), run_time=RUN_NORMAL)
            self.play(GrowArrow(arrow2), Write(ratio), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)

            compact = VGroup(
                self.text(label, 22, BOLD),
                self.math(rf"d={d:.1f}", 28),
                self.math(rf"C={c:.1f}", 28),
                self.math(rf"C/d={c/d:.3f}", 29),
            ).arrange(RIGHT, buff=0.62)
            compact.move_to([1.15, y, 0])
            self.fit(compact, 10.9, 0.66)
            self.play(
                FadeOut(VGroup(disc, gauge, trace, tracer, c_label, ratio, arrow1, arrow2)),
                FadeIn(compact, shift=LEFT * 0.12),
                run_time=RUN_NORMAL,
            )
            rows.add(compact)

        frame = SurroundingRectangle(
            rows,
            buff=0.30,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            corner_radius=0.12,
        )
        label = self.text("EXAMPLE EVIDENCE — COMPARE WITH YOUR OWN DATA", 22, BOLD)
        label.next_to(frame, DOWN, buff=0.18)
        self.assert_content_safe(VGroup(frame, label), "V3 measurement evidence")
        self.play(Create(frame), FadeIn(label), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def discover_pi_v3(self) -> None:
        self.set_header(
            2,
            "THREE DIFFERENT CIRCLES — ONE STABLE RATIO",
            "The circles change size, but C / d remains close to 3.14; measurement error explains the small differences.",
        )

        ratio_mobs = VGroup()
        xs = [-4.7, -1.4, 1.9]
        for x, ratio, letter in zip(xs, SAMPLE_RATIOS, "ABC"):
            value = self.math(rf"{ratio:.3f}", 44)
            badge = RoundedRectangle(
                width=2.35,
                height=1.20,
                corner_radius=0.14,
                stroke_color=BLACK_LINE,
                stroke_width=2,
                fill_color=PAPER_GRAY,
                fill_opacity=1,
            )
            caption = self.text(f"C / d — OBJECT {letter}", 18, BOLD).next_to(badge, UP, buff=0.10)
            value.move_to(badge)
            grp = VGroup(badge, value, caption).move_to([x, 0.75, 0])
            ratio_mobs.add(grp)

        pi_target = self.math(r"\pi=3.14159\ldots", 52).move_to([4.75, 0.75, 0])
        arrows = VGroup(*[
            Arrow(g.get_right() + RIGHT * 0.10, pi_target.get_left() + LEFT * 0.20,
                  color=LIGHT_GRAY, stroke_width=1.8, tip_length=0.10, buff=0.12)
            for g in ratio_mobs
        ])

        mean = self.math(rf"\text{{mean}}\left(\frac{{C}}{{d}}\right)\approx {SAMPLE_MEAN:.3f}", 40)
        mean.move_to(DOWN * 1.05)
        relation = self.math(r"\boxed{\frac{C}{d}=\pi}", 50).move_to(DOWN * 2.25)
        sentence = self.text("Circumference is about 3.14 diameters long.", 27, BOLD)
        sentence.move_to(DOWN * 3.20)
        group = VGroup(ratio_mobs, pi_target, arrows, mean, relation, sentence)
        self.assert_content_safe(group, "V3 pi discovery")

        for grp in ratio_mobs:
            self.play(FadeIn(grp[0], scale=0.95), Write(grp[1]), FadeIn(grp[2]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=RUN_NORMAL)
        self.play(Write(pi_target), run_time=RUN_NORMAL)
        self.play(Write(mean), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(TransformMatchingTex(mean.copy(), relation), run_time=RUN_SLOW)
        self.play(FadeIn(sentence, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def elements_radius_diameter_v3(self) -> None:
        self.set_header(
            3,
            "BUILD THE CIRCLE FROM ITS CENTER",
            "A radius reaches the boundary; two opposite radii create the diameter; the boundary itself is the circumference.",
        )

        center = np.array([-2.6, -0.45, 0.0])
        r = 1.75
        o = Dot(center, radius=0.075, color=BLACK_LINE)
        o_label = self.math("O", 30).next_to(o, UL, buff=0.10)
        radius = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=4)
        r_label = self.math("r", 38).next_to(radius, UP, buff=0.10)
        opposite = Line(center, center + LEFT * r, color=MID_GRAY, stroke_width=4)
        diameter = Line(center + LEFT * r, center + RIGHT * r, color=BLACK_LINE, stroke_width=5)
        d_label = self.math("d", 38).next_to(diameter, DOWN, buff=0.14)
        circle = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=5).move_to(center)
        tracer = Dot(circle.point_at_angle(0), radius=0.07, color=BLACK_LINE)
        circumference_label = self.text("CIRCUMFERENCE", 23, BOLD).next_to(circle, LEFT, buff=0.20)

        eq_pos = np.array([4.0, 0.35, 0.0])
        eq1 = self.math(r"r", 55).move_to(eq_pos)
        eq2 = self.math(r"r+r=d", 50).move_to(eq_pos)
        eq3 = self.math(r"d=2r", 54).move_to(eq_pos)
        relation = self.formula_panel(r"C=\pi d=2\pi r", width=5.8, height=1.15, font_size=45)
        relation.move_to([4.0, -1.55, 0])
        units = self.text("r, d, and C are lengths → linear units", 24, BOLD).move_to([4.0, -2.65, 0])

        group = VGroup(o, o_label, radius, r_label, opposite, diameter, d_label, circle,
                       circumference_label, relation, units)
        self.assert_content_safe(group, "V3 circle elements")

        self.play(FadeIn(o, scale=0.6), Write(o_label), run_time=RUN_QUICK)
        self.play(GrowFromPoint(radius, center), Write(r_label), run_time=RUN_NORMAL)
        self.play(Write(eq1), run_time=RUN_QUICK)
        self.play(GrowFromPoint(opposite, center), run_time=RUN_NORMAL)
        self.play(ReplacementTransform(VGroup(radius.copy(), opposite.copy()), diameter), run_time=RUN_SLOW)
        self.play(Write(d_label), TransformMatchingTex(eq1, eq2), run_time=RUN_NORMAL)
        eq1.become(eq2)
        self.play(TransformMatchingTex(eq1, eq3), run_time=RUN_NORMAL)
        eq1.become(eq3)
        self.play(Create(circle), MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.45)
        self.play(FadeOut(tracer), FadeIn(circumference_label), run_time=RUN_QUICK)
        self.play(FadeIn(relation, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.play(FadeIn(units), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def unwrap_circumference_v3(self) -> None:
        self.set_header(
            4,
            "UNWRAP THE BORDER — CIRCUMFERENCE IS A LENGTH",
            "The experimental statement C / d = pi can be rearranged into the two circumference formulas.",
        )

        c_center = np.array([-4.25, 0.15, 0.0])
        circle = Circle(radius=1.35, stroke_color=BLACK_LINE, stroke_width=7).move_to(c_center)
        diameter = DoubleArrow(
            circle.get_left(), circle.get_right(), buff=0.02, tip_length=0.13,
            color=BLACK_LINE, stroke_width=2.5,
        )
        d_label = self.math("d", 38).next_to(diameter, DOWN, buff=0.10)
        tracer = Dot(circle.point_at_angle(0), radius=0.075, color=BLACK_LINE)

        line_y = 0.15
        unwrapped = Line([0.0, line_y, 0], [5.6, line_y, 0], color=BLACK_LINE, stroke_width=7)
        brace = Brace(unwrapped, DOWN, buff=0.12, color=BLACK_LINE)
        c_label = self.math("C", 38).next_to(brace, DOWN, buff=0.10)
        arrow = Arrow([-1.95, 0.15, 0], [-0.45, 0.15, 0], color=MID_GRAY, stroke_width=2.5, tip_length=0.13)

        chain_pos = np.array([0.7, -2.05, 0.0])
        e1 = self.math(r"\frac{C}{d}=\pi", 48).move_to(chain_pos)
        e2 = self.math(r"C=\pi d", 52).move_to(chain_pos)
        e3 = self.math(r"C=2\pi r", 52).move_to(chain_pos)
        note = self.text("PERIMETER OF A CIRCLE = CIRCUMFERENCE", 25, BOLD).move_to(DOWN * 3.15)

        group = VGroup(circle, diameter, d_label, arrow, unwrapped, brace, c_label, e1, note)
        self.assert_content_safe(group, "V3 circumference unwrap")

        self.play(Create(circle), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(diameter), Write(d_label), run_time=RUN_NORMAL)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.55)
        self.play(FadeOut(tracer), GrowArrow(arrow), run_time=RUN_QUICK)
        border_copy = circle.copy()
        self.add(border_copy)
        self.play(Transform(border_copy, unwrapped), run_time=RUN_SLOW * 1.4)
        self.play(GrowFromCenter(brace), Write(c_label), run_time=RUN_NORMAL)
        self.play(Write(e1), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(TransformMatchingTex(e1, e2), run_time=RUN_SLOW)
        e1.become(e2)
        self.wait(PAUSE_READ)
        self.play(TransformMatchingTex(e1, e3), run_time=RUN_SLOW)
        e1.become(e3)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
