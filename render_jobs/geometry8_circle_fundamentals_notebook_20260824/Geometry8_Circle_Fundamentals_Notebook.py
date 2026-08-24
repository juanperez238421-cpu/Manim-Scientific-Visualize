#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 - Circle fundamentals, large projector notebook-copy edition V2.

Focus: center, radius, diameter, chord and arc.
Target: Manim Community Edition 0.20.1 + JP Classroom style.
Revision objective: materially larger figures/text while preserving strict separation
between the diagram and notebook-copy zones.
"""
from __future__ import annotations

import numpy as np
from manim import *
from jp_classroom_style import *

R = 2.25
COPY_PAUSE = 9.0
THINK_PAUSE = 5.0


class Geometry8CircleFundamentalsNotebook(JPMathClassroomScene):
    def validate_lesson_data(self) -> None:
        assert_close(2 * R, 4.5, label="diameter from radius")
        assert 0 < 100 < 180
        assert 180 < 260 < 360

    def construct(self) -> None:
        self.opening()
        self.circle_and_center()
        self.radius()
        self.diameter()
        self.chord()
        self.arc()
        self.compare_all()
        self.notebook_check()

    def base_circle(self, center=np.array([-3.80, -0.50, 0.0]), radius=R):
        return Circle(
            radius=radius,
            stroke_color=BLACK_LINE,
            stroke_width=5.4,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(center)

    def point_with_label(self, point, label, direction=UR):
        dot = Dot(point, radius=0.105, color=BLACK_LINE)
        text = self.math(label, 40).next_to(dot, direction, buff=0.12)
        return VGroup(dot, text)

    def copy_card(self, term: str, lines: list[str], formula: str | None = None):
        """Large notebook card with short wrapped lines to prevent fit-driven shrinking."""
        box = RoundedRectangle(
            width=6.45,
            height=4.95,
            corner_radius=0.16,
            stroke_color=BLACK_LINE,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1.0,
        )

        title = self.text("COPY TO NOTEBOOK", 31, BOLD)
        term_m = self.text(term, 44, BOLD)
        body = VGroup(*[self.text(line, 32) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.13)

        pieces = [title, term_m, body]
        if formula is not None:
            pieces.append(self.math(formula, 50))

        content = VGroup(*pieces).arrange(DOWN, aligned_edge=LEFT, buff=0.23)
        self.fit(content, 5.90, 4.32)
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, content)

    def layout_pair(self, diagram: Mobject, copy: Mobject):
        diagram.move_to(LEFT * 3.82 + DOWN * 0.48)
        copy.move_to(RIGHT * 3.58 + DOWN * 0.48)
        group = VGroup(diagram, copy)
        self.assert_content_safe(group, "circle notebook V2 separated two-column layout")
        return group

    def section_header(self, number: int, title: str, subtitle: str) -> None:
        """Fade between section headers instead of morphing letters into each other."""
        old = [mob for mob in (self.header_group, self.subtitle_group) if mob is not None]
        if old:
            self.play(*[FadeOut(mob) for mob in old], run_time=RUN_QUICK)
            self.remove(*old)
            self.header_group = None
            self.subtitle_group = None
        JPMathClassroomScene.set_header(self, number, title, subtitle)

    def opening(self) -> None:
        self.standard_opening(
            "GEOMETRY 8",
            "CIRCLE FUNDAMENTALS",
            "Center, radius, diameter, chords and arcs",
            "Watch the large figure, copy the definition, then connect the ideas.",
        )

    def circle_and_center(self) -> None:
        self.section_header(
            1,
            "THE CIRCLE AND ITS CENTER",
            "Start from the fixed point that organizes every other element.",
        )
        c = self.base_circle()
        O = c.get_center()
        center = self.point_with_label(O, "O", UR)
        radii = VGroup(
            Line(O, c.point_at_angle(20 * DEGREES), color=MID_GRAY, stroke_width=2.8),
            Line(O, c.point_at_angle(145 * DEGREES), color=MID_GRAY, stroke_width=2.8),
            Line(O, c.point_at_angle(255 * DEGREES), color=MID_GRAY, stroke_width=2.8),
        )
        diagram = VGroup(c, radii, center)
        card = self.copy_card(
            "CENTER (O)",
            [
                "The center is a fixed point inside the circle.",
                "Every point on the circumference",
                "is the same distance from O.",
            ],
        )
        self.layout_pair(diagram, card)
        self.play(Create(c), run_time=RUN_SLOW)
        self.play(FadeIn(center), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Create(r) for r in radii], lag_ratio=0.16), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY_PAUSE)
        self.clear_stage()

    def radius(self) -> None:
        self.section_header(
            2,
            "RADIUS",
            "A radius starts at the center and ends on the circumference.",
        )
        c = self.base_circle()
        O = c.get_center()
        A = c.point_at_angle(30 * DEGREES)
        seg = Line(O, A, color=BLACK_LINE, stroke_width=7.0)
        labels = VGroup(
            self.point_with_label(O, "O", DL),
            self.point_with_label(A, "A", UR),
            self.math("r", 48).next_to(seg, UP, buff=0.16),
        )
        diagram = VGroup(c, seg, labels)
        card = self.copy_card(
            "RADIUS (r)",
            [
                "A radius is a segment from the center",
                "to a point on the circumference.",
                "All radii in the same circle are equal.",
            ],
            formula=r"OA=r",
        )
        self.layout_pair(diagram, card)
        self.play(Create(c), run_time=RUN_NORMAL)
        self.play(Create(seg), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY_PAUSE)
        self.clear_stage()

    def diameter(self) -> None:
        self.section_header(
            3,
            "DIAMETER",
            "A diameter is the longest chord because it passes through the center.",
        )
        c = self.base_circle()
        O = c.get_center()
        A = c.point_at_angle(180 * DEGREES)
        B = c.point_at_angle(0 * DEGREES)
        diam = Line(A, B, color=BLACK_LINE, stroke_width=7.0)
        labels = VGroup(
            self.point_with_label(A, "A", UL),
            self.point_with_label(O, "O", DOWN),
            self.point_with_label(B, "B", UR),
            self.math("d", 50).next_to(diam, UP, buff=0.18),
        )
        diagram = VGroup(c, diam, labels)
        card = self.copy_card(
            "DIAMETER (d)",
            [
                "A diameter joins two points on the circumference.",
                "It passes through the center O.",
                "One diameter is equal to two radii.",
            ],
            formula=r"d=2r\qquad r=\frac{d}{2}",
        )
        self.layout_pair(diagram, card)
        self.play(Create(c), run_time=RUN_NORMAL)
        self.play(Create(diam), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY_PAUSE + 2.0)
        self.clear_stage()

    def chord(self) -> None:
        self.section_header(
            4,
            "CHORD",
            "A chord connects two points on the circumference; it does not have to pass through the center.",
        )
        c = self.base_circle()
        O = c.get_center()
        A = c.point_at_angle(142 * DEGREES)
        B = c.point_at_angle(34 * DEGREES)
        chord = Line(A, B, color=BLACK_LINE, stroke_width=7.0)
        diameter = Line(c.point_at_angle(180 * DEGREES), c.point_at_angle(0), color=MID_GRAY, stroke_width=2.8)
        labels = VGroup(
            self.point_with_label(A, "A", UL),
            self.point_with_label(B, "B", UR),
            self.point_with_label(O, "O", DOWN),
            self.text("chord", 31, BOLD).next_to(chord, UP, buff=0.13),
        )
        diagram = VGroup(c, diameter, chord, labels)
        card = self.copy_card(
            "CHORD",
            [
                "A chord joins two points on the circumference.",
                "It may or may not pass through the center.",
                "Every diameter is a chord.",
                "Not every chord is a diameter.",
            ],
        )
        self.layout_pair(diagram, card)
        self.play(Create(c), run_time=RUN_NORMAL)
        self.play(Create(diameter), run_time=RUN_QUICK)
        self.play(Create(chord), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY_PAUSE + 2.0)
        self.clear_stage()

    def arc(self) -> None:
        self.section_header(
            5,
            "ARC",
            "An arc is a curved part of the circumference between two points.",
        )
        center = np.array([-3.80, -0.50, 0.0])
        c = Circle(radius=R, stroke_color=MID_GRAY, stroke_width=3.0).move_to(center)
        start = 25 * DEGREES
        minor_angle = 100 * DEGREES
        A = c.point_at_angle(start)
        B = c.point_at_angle(start + minor_angle)
        minor = Arc(radius=R, start_angle=start, angle=minor_angle, arc_center=center, color=BLACK_LINE, stroke_width=10.0)
        major = Arc(radius=R, start_angle=start + minor_angle, angle=TAU - minor_angle, arc_center=center, color=BLACK_LINE, stroke_width=4.0)
        labels = VGroup(
            self.point_with_label(A, "A", UR),
            self.point_with_label(B, "B", UL),
            self.text("minor arc", 31, BOLD).next_to(minor.point_from_proportion(0.48), UP, buff=0.18),
            self.text("major arc", 29).next_to(major.point_from_proportion(0.55), DOWN, buff=0.18),
        )
        diagram = VGroup(c, major, minor, labels)
        card = self.copy_card(
            "ARC",
            [
                "An arc is a curved part of the circumference.",
                "A minor arc measures less than 180 degrees.",
                "A major arc measures more than 180 degrees.",
            ],
        )
        self.layout_pair(diagram, card)
        self.play(Create(c), run_time=RUN_NORMAL)
        self.play(Create(minor), FadeIn(labels[0:3]), run_time=RUN_SLOW)
        self.wait(THINK_PAUSE)
        self.play(Create(major), FadeIn(labels[3]), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY_PAUSE + 2.0)
        self.clear_stage()

    def summary_row(self, number: str, text: str):
        badge = RoundedRectangle(
            width=0.62,
            height=0.52,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        n = self.text(number, 28, BOLD).move_to(badge)
        label = self.text(text, 29, BOLD)
        row = VGroup(VGroup(badge, n), label).arrange(RIGHT, buff=0.20, aligned_edge=ORIGIN)
        return row

    def compare_all(self) -> None:
        self.section_header(
            6,
            "PUT THE FIVE ELEMENTS TOGETHER",
            "Use the numbered marks to identify each element without overlapping labels.",
        )
        center = np.array([-3.85, -0.50, 0.0])
        rr = 2.17
        c = Circle(radius=rr, stroke_color=BLACK_LINE, stroke_width=5.0).move_to(center)
        O = center
        Rpt = c.point_at_angle(45 * DEGREES)
        D1, D2 = c.point_at_angle(180 * DEGREES), c.point_at_angle(0)
        C1, C2 = c.point_at_angle(135 * DEGREES), c.point_at_angle(45 * DEGREES)
        rad = Line(O, Rpt, color=BLACK_LINE, stroke_width=6.0)
        diam = Line(D1, D2, color=BLACK_LINE, stroke_width=4.0)
        chord = Line(C1, C2, color=BLACK_LINE, stroke_width=7.0)
        arc = Arc(radius=rr, start_angle=210 * DEGREES, angle=82 * DEGREES, arc_center=center, color=BLACK_LINE, stroke_width=10.0)

        tag1 = self.text("1", 31, BOLD).move_to(O + RIGHT * 0.42 + DOWN * 0.36)
        tag2 = self.text("2", 31, BOLD).move_to(rad.get_center() + UL * 0.28)
        tag3 = self.text("3", 31, BOLD).move_to(diam.get_center() + LEFT * 1.05 + DOWN * 0.30)
        tag4 = self.text("4", 31, BOLD).next_to(chord, UP, buff=0.14)
        tag5 = self.text("5", 31, BOLD).next_to(arc.point_from_proportion(0.50), DOWN, buff=0.17)
        Olabel = self.math("O", 40).next_to(O, UL, buff=0.10)
        diagram = VGroup(c, diam, chord, rad, arc, Olabel, tag1, tag2, tag3, tag4, tag5)

        rows = VGroup(
            self.summary_row("1", "CENTER: fixed point O"),
            self.summary_row("2", "RADIUS: center to circle"),
            self.summary_row("3", "DIAMETER: through O"),
            self.summary_row("4", "CHORD: two endpoints"),
            self.summary_row("5", "ARC: curved boundary"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(rows, 6.15, 4.45)
        self.layout_pair(diagram, rows)

        self.play(Create(c), run_time=RUN_NORMAL)
        self.play(LaggedStart(Create(rad), Create(diam), Create(chord), Create(arc), lag_ratio=0.18), run_time=RUN_SLOW * 1.5)
        self.play(FadeIn(VGroup(Olabel, tag1, tag2, tag3, tag4, tag5)), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in rows], lag_ratio=0.12), run_time=RUN_SLOW * 1.4)
        self.wait(COPY_PAUSE)
        self.clear_stage()

    def notebook_check(self) -> None:
        self.section_header(
            7,
            "NOTEBOOK CHECK",
            "Read each clue and say the element before the answer appears.",
        )
        questions = [
            ("Starts at O and ends on the circumference.", "RADIUS"),
            ("Joins two points and passes through O.", "DIAMETER"),
            ("Joins two points but may miss O.", "CHORD"),
            ("Curved part of the circumference.", "ARC"),
            ("Fixed point equally distant from the circumference.", "CENTER"),
        ]
        holder = RoundedRectangle(
            width=12.55,
            height=4.70,
            corner_radius=0.16,
            stroke_color=BLACK_LINE,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(DOWN * 0.45)
        self.play(FadeIn(holder), run_time=RUN_NORMAL)
        current = None
        for i, (q, a) in enumerate(questions, start=1):
            idx = self.text(f"CHECK {i} / 5", 34, BOLD).next_to(holder.get_top(), DOWN, buff=0.30)
            prompt = self.text(q, 44, BOLD)
            self.fit(prompt, 11.35, 1.00)
            prompt.move_to(holder).shift(UP * 0.28)
            answer = self.text(a, 58, BOLD).next_to(prompt, DOWN, buff=0.52)
            state = VGroup(idx, prompt)
            if current is None:
                self.play(FadeIn(state), run_time=RUN_NORMAL)
            else:
                self.play(ReplacementTransform(current, state), run_time=RUN_NORMAL)
            self.wait(THINK_PAUSE)
            self.play(FadeIn(answer), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
            self.play(FadeOut(answer), run_time=RUN_QUICK)
            current = state
        self.wait(PAUSE_FINAL)
        self.remove(*list(self.mobjects))
        self.header_group = None
        self.subtitle_group = None
        closing = self.text(
            "Center  ->  radius  ->  diameter  ->  chord  ->  arc",
            52,
            BOLD,
        )
        self.fit(closing, 13.45, 1.25)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)


# Preview QA:
# LESSON_TIME_SCALE=0.08 manim -pql Geometry8_Circle_Fundamentals_Notebook.py Geometry8CircleFundamentalsNotebook --fps 15 --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Circle_Fundamentals_Notebook.py Geometry8CircleFundamentalsNotebook --fps 30 --disable_caching
