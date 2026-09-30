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


class CircleV3ExercisesMixin:
    """Animation mixin used by the Geometry 8 V3 circle lesson."""

    def exercise_diameter_v3(self) -> None:
        self.set_header(
            7,
            "EXERCISE 1 — DIAMETER GIVEN",
            "A circular lid has diameter 14 cm. Find the radius, circumference, and area — then check each unit.",
        )

        center = np.array([-3.9, -0.35, 0.0])
        circle = Circle(radius=1.60, stroke_color=BLACK_LINE, stroke_width=4).move_to(center)
        diameter = DoubleArrow(circle.get_left(), circle.get_right(), buff=0.02, tip_length=0.13,
                               color=BLACK_LINE, stroke_width=2.5)
        d_label = self.math(r"d=14\text{ cm}", 34).next_to(diameter, DOWN, buff=0.10)
        half = Line(center, center + RIGHT * 1.60, color=MID_GRAY, stroke_width=4)
        r_label = self.math(r"r=7\text{ cm}", 32).next_to(half, UP, buff=0.10)
        tracer = Dot(circle.point_at_angle(0), radius=0.07, color=BLACK_LINE)

        x = 3.5
        y0 = 1.10
        lines = [
            self._solution_line(r"r=\frac{d}{2}=7\text{ cm}", 38, [x, y0, 0]),
            self._solution_line(r"C=\pi d=14\pi\approx44.0\text{ cm}", 37, [x, y0-1.05, 0]),
            self._solution_line(r"A=\pi r^2=49\pi\approx153.9\text{ cm}^2", 35, [x, y0-2.10, 0]),
        ]
        unit_check = self.text("C → cm     |     A → cm²", 25, BOLD).move_to([3.5, -2.55, 0])
        group = VGroup(circle, diameter, d_label, half, r_label, *lines, unit_check)
        self.assert_content_safe(group, "V3 diameter exercise")

        self.play(Create(circle), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(diameter), Write(d_label), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(diameter, half), Write(r_label), run_time=RUN_NORMAL)
        self.play(Write(lines[0]), run_time=RUN_NORMAL)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.25)
        self.play(FadeOut(tracer), Write(lines[1]), run_time=RUN_NORMAL)
        fill = circle.copy().set_fill(LIGHT_GRAY, opacity=0.65).set_stroke(BLACK_LINE, width=3)
        self.play(Transform(circle, fill), run_time=RUN_NORMAL)
        self.play(Write(lines[2]), run_time=RUN_NORMAL)
        self.play(FadeIn(unit_check, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def exercise_radius_area_v3(self) -> None:
        self.set_header(
            8,
            "EXERCISE 2 — RADIUS GIVEN: BUILD THE AREA",
            "A circular sticker has radius 5 cm. Find its area and explain why the answer is measured in square centimeters.",
        )

        center = np.array([-3.85, -0.35, 0.0])
        circle = Circle(radius=1.60, stroke_color=BLACK_LINE, stroke_width=4).move_to(center)
        radius = Line(center, center + RIGHT * 1.60, color=BLACK_LINE, stroke_width=4)
        r_label = self.math(r"r=5\text{ cm}", 34).next_to(radius, UP, buff=0.10)
        grid = self._mini_square_grid(center, cols=11, rows=11, size=0.25)
        grid.set_opacity(0.42)

        eq_pos = [3.6, 0.75, 0]
        e1 = self.math(r"A=\pi r^2", 48).move_to(eq_pos)
        e2 = self.math(r"A=\pi(5)^2", 48).move_to(eq_pos)
        e3 = self.math(r"A=25\pi\text{ cm}^2", 46).move_to(eq_pos)
        e4 = self.math(r"A\approx78.5\text{ cm}^2", 48).move_to(eq_pos)
        squares_note = self.text("Area counts surface → square units", 25, BOLD).move_to([3.6, -1.05, 0])
        unit_visual = VGroup(
            Square(side_length=0.62, stroke_color=BLACK_LINE, stroke_width=2, fill_color=VERY_LIGHT_GRAY, fill_opacity=1),
            self.math(r"1\text{ cm}^2", 26),
        ).arrange(RIGHT, buff=0.18).move_to([3.6, -2.05, 0])
        group = VGroup(circle, radius, r_label, e4, squares_note, unit_visual)
        self.assert_content_safe(group, "V3 radius area exercise")

        self.play(Create(circle), GrowFromPoint(radius, center), Write(r_label), run_time=RUN_NORMAL)
        self.play(Write(e1), run_time=RUN_NORMAL)
        self.play(Transform(e1, e2), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.006), run_time=RUN_SLOW)
        fill = circle.copy().set_fill(LIGHT_GRAY, opacity=0.60).set_stroke(BLACK_LINE, width=3)
        self.play(Transform(circle, fill), run_time=RUN_NORMAL)
        self.play(Transform(e1, e3), run_time=RUN_NORMAL)
        self.play(FadeIn(unit_visual), FadeIn(squares_note), run_time=RUN_NORMAL)
        self.play(Transform(e1, e4), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def exercise_inverse_and_context_v3(self) -> None:
        self.set_header(
            9,
            "EXERCISE 3 — WORK BACKWARD, THEN CHOOSE THE MEASUREMENT",
            "A round table has C = 31.4 cm. Estimate d and r; then decide what a border strip and a surface cover would require.",
        )

        center = np.array([-4.25, -0.20, 0.0])
        circle = Circle(radius=1.52, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        tracer = Dot(circle.point_at_angle(0), radius=0.07, color=BLACK_LINE)
        c_label = self.math(r"C=31.4\text{ cm}", 34).next_to(circle, DOWN, buff=0.20)
        diameter = DoubleArrow(circle.get_left(), circle.get_right(), buff=0.02, tip_length=0.12,
                               color=MID_GRAY, stroke_width=2.3)
        radius = Line(center, center + RIGHT * 1.52, color=BLACK_LINE, stroke_width=3.2)

        pos = np.array([3.4, 1.15, 0.0])
        e1 = self.math(r"C=\pi d", 45).move_to(pos)
        e2 = self.math(r"d=\frac{C}{\pi}", 45).move_to(pos)
        e3 = self.math(r"d\approx\frac{31.4}{3.14}=10\text{ cm}", 39).move_to(pos)
        e4 = self.math(r"r=\frac{d}{2}=5\text{ cm}", 40).move_to([3.4, 0.00, 0])

        fence = RoundedRectangle(width=4.5, height=1.05, corner_radius=0.12,
                                 stroke_color=BLACK_LINE, stroke_width=1.7,
                                 fill_color=WHITE, fill_opacity=1).move_to([3.4, -1.35, 0])
        fence_text = self.text("BORDER STRIP → circumference", 23, BOLD).move_to(fence)
        cover = RoundedRectangle(width=4.5, height=1.05, corner_radius=0.12,
                                 stroke_color=BLACK_LINE, stroke_width=1.7,
                                 fill_color=PAPER_GRAY, fill_opacity=1).move_to([3.4, -2.65, 0])
        cover_text = self.text("SURFACE COVER → area", 23, BOLD).move_to(cover)
        group = VGroup(circle, c_label, diameter, radius, e3, e4, fence, fence_text, cover, cover_text)
        self.assert_content_safe(group, "V3 inverse context exercise")

        self.play(Create(circle), Write(c_label), run_time=RUN_NORMAL)
        self.play(MoveAlongPath(tracer, circle), run_time=RUN_SLOW * 1.25)
        self.play(FadeOut(tracer), Write(e1), run_time=RUN_NORMAL)
        self.play(Transform(e1, e2), run_time=RUN_NORMAL)
        self.play(Transform(e1, e3), GrowFromCenter(diameter), run_time=RUN_SLOW)
        self.play(GrowFromPoint(radius, center), Write(e4), run_time=RUN_NORMAL)
        self.play(FadeIn(fence), FadeIn(fence_text), run_time=RUN_NORMAL)
        self.play(FadeIn(cover), FadeIn(cover_text), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def lesson_summary_v3(self) -> None:
        self.set_header(
            10,
            "RETURN TO YOUR THREE OBJECTS — COMPLETE THE EXPERIMENT",
            "For one real object, connect the measurement you made to a prediction, a comparison, and a new area calculation.",
        )

        steps = [
            ("1", "MEASURE d"),
            ("2", "MEASURE C"),
            ("3", "CALCULATE C / d"),
            ("4", "PREDICT C = pi d"),
            ("5", "FIND r = d / 2"),
            ("6", "CALCULATE A = pi r²"),
        ]
        cards = self.process_map(steps, card_width=4.15, card_height=1.02, columns=3)
        self.fit(cards, 13.1, 2.4)
        cards.move_to(UP * 0.55)

        object_circle = Circle(radius=0.78, stroke_color=BLACK_LINE, stroke_width=4).move_to([-4.65, -2.10, 0])
        d = DoubleArrow(object_circle.get_left(), object_circle.get_right(), buff=0.02,
                        tip_length=0.10, color=BLACK_LINE, stroke_width=2)
        unknown = self.math(r"d=?\qquad C=?\qquad A=?", 35).move_to([-1.4, -2.10, 0])
        challenge = self.note_panel(
            "FINAL CHALLENGE",
            [
                "Choose one of your three measured objects.",
                "Compare measured C with predicted C = pi d.",
                "Then calculate the area and report the correct square unit.",
            ],
            width=6.15,
            title_size=26,
            body_size=23,
            max_text_height=1.65,
        ).move_to([3.85, -2.05, 0])
        group = VGroup(cards, object_circle, d, unknown, challenge)
        self.assert_content_safe(group, "V3 summary")

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.7,
        )
        self.play(Create(object_circle), GrowFromCenter(d), run_time=RUN_NORMAL)
        self.play(Write(unknown), run_time=RUN_NORMAL)
        self.play(FadeIn(challenge, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing(
            "Measure. Discover pi. Distinguish boundary from surface. Explain every unit."
        )
