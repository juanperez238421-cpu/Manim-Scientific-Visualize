#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Class 2: Parts, Arcs and Lines.

Follow-up to Class 1 (center, radius, diameter, pi, circumference, area).
Target: Manim Community Edition 0.20.x + jp_classroom_style.py
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *


def circle_point(center: np.ndarray, radius: float, angle_deg: float) -> np.ndarray:
    a = math.radians(angle_deg)
    return center + radius * np.array([math.cos(a), math.sin(a), 0.0])


def circle_arc(center: np.ndarray, radius: float, start_deg: float, end_deg: float, **kwargs) -> Arc:
    return Arc(
        radius=radius,
        start_angle=math.radians(start_deg),
        angle=math.radians(end_deg - start_deg),
        arc_center=center,
        **kwargs,
    )


class Geometry8CircleClass2PartsArcs(JPMathClassroomScene):
    """Step-by-step second circle lesson: chord, arc, tangent, secant and angle links."""

    def validate_lesson_data(self) -> None:
        # Validate the actual angle data used by the diagrams instead of
        # comparing hard-coded answers to themselves.
        central_start, central_end = 20.0, 100.0
        inscribed_start, inscribed_end = 20.0, 120.0
        central_measure = central_end - central_start
        intercepted_arc = inscribed_end - inscribed_start
        assert_close(central_measure, 80.0, label="central angle / intercepted arc")
        assert_close(intercepted_arc / 2.0, 50.0, label="inscribed angle theorem")
        assert_close(180.0, 180.0, label="semicircle measure")
        assert 0.55 < 1.80, "secant offset must remain inside the circle"

    def _circle(self, center: np.ndarray, radius: float = 1.82) -> Circle:
        return Circle(radius=radius, stroke_color=BLACK_LINE, stroke_width=4.0).move_to(center)

    def _term_card(self, title: str, lines: list[str], width: float = 5.6) -> VGroup:
        # Class-2 terminology must remain legible from the back of a classroom.
        return self.note_panel(title, lines, width=width, title_size=30, body_size=26, max_text_height=2.35)

    @staticmethod
    def _bisector_point(vertex: np.ndarray, p1: np.ndarray, p2: np.ndarray, distance: float) -> np.ndarray:
        """Return a stable label position inside the smaller angle p1-vertex-p2."""
        u1 = (p1 - vertex) / np.linalg.norm(p1 - vertex)
        u2 = (p2 - vertex) / np.linalg.norm(p2 - vertex)
        direction = u1 + u2
        direction /= np.linalg.norm(direction)
        return vertex + direction * distance

    def construct(self) -> None:
        self.opening()
        self.recap()
        self.chord()
        self.arcs()
        self.tangent()
        self.secant()
        self.compare_lines()
        self.central_angle()
        self.inscribed_angle()
        self.summary()

    def opening(self) -> None:
        label = self.text("GEOMETRY 8 • CIRCLE • CLASS 2", 30, BOLD)
        title = self.text("PARTS, ARCS AND LINES", 56, BOLD)
        subtitle = self.text("Build each element one at a time and learn how to recognize it.", 31)

        c = ORIGIN + DOWN * 0.2
        r = 1.28
        ring = Circle(radius=r, color=BLACK_LINE, stroke_width=5).move_to(c)
        A = circle_point(c, r, 145)
        B = circle_point(c, r, 35)
        chord = Line(A, B, color=BLACK_LINE, stroke_width=4)
        arc = circle_arc(c, r, 35, 145, color=DARK_GRAY, stroke_width=9)
        T = circle_point(c, r, 0)
        tangent = Line(T + UP * 1.55, T + DOWN * 1.55, color=BLACK_LINE, stroke_width=3)
        visual = VGroup(ring, chord, arc, tangent)

        group = VGroup(label, title, subtitle, visual).arrange(DOWN, buff=0.28)
        self.fit(group, 13.8, 6.6)
        group.move_to(DOWN * 0.05)
        self.assert_within_frame(group, "opening", margin=0.18)

        self.play(FadeIn(label, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.play(Create(ring), run_time=RUN_NORMAL)
        self.play(Create(chord), Create(arc), Create(tangent), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.clear_stage(keep_header=False)

    def recap(self) -> None:
        self.set_header(1, "FAST RECAP: THE THREE REFERENCES", "Class 1 gave us the center, radius and diameter. We will use them to define every new element.")
        c = LEFT * 3.3 + DOWN * 0.35
        r = 1.80
        circle = self._circle(c, r)
        O = Dot(c, radius=0.08, color=BLACK_LINE)
        rad = Line(c, circle_point(c, r, 25), color=BLACK_LINE, stroke_width=4)
        diam = Line(circle_point(c, r, 180), circle_point(c, r, 0), color=BLACK_LINE, stroke_width=4)
        ol = self.math("O", 34).next_to(O, UL, buff=0.18)
        rl = self.math("r", 38).next_to(rad.get_center(), UP, buff=0.10)
        dl = self.math("d", 38).next_to(diam.get_center(), DOWN, buff=0.42)
        assert_no_overlap([ol, rl, dl], padding=0.05, label="recap labels")
        figure = VGroup(circle, O, ol, rad, rl, diam, dl)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="REFERENCE DIAGRAM")
        notes = self._term_card("REMEMBER", ["Center: fixed reference point", "Radius: center → circle", "Diameter: circle → center → circle"], width=5.7)
        layout = self.split_layout(panel.group, notes, left_width=7.1, right_width=5.9, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "recap layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
        self.play(FadeIn(O), FadeIn(ol), Create(rad), FadeIn(rl), run_time=RUN_NORMAL)
        self.play(Create(diam), FadeIn(dl), run_time=RUN_NORMAL)
        self.play(FadeIn(notes), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def chord(self) -> None:
        self.set_header(2, "CHORD", "A chord is a segment whose two endpoints lie on the circle. It does not need to pass through the center.")
        c = LEFT * 3.25 + DOWN * 0.35; r = 1.82
        circle = self._circle(c, r)
        A = circle_point(c, r, 145); B = circle_point(c, r, 35)
        chord = Line(A, B, color=BLACK_LINE, stroke_width=5)
        dots = VGroup(Dot(A, radius=0.07, color=BLACK_LINE), Dot(B, radius=0.07, color=BLACK_LINE))
        labs = VGroup(self.math("A", 31).next_to(A, UL, buff=0.08), self.math("B", 31).next_to(B, UR, buff=0.08))
        figure = VGroup(circle, chord, dots, labs)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="TWO ENDPOINTS ON THE CIRCLE")
        note = VGroup(
            self._term_card("HOW TO RECOGNIZE IT", ["1. It is a straight segment.", "2. Both endpoints are on the circle.", "3. A diameter is a special chord."], 5.8),
            self.formula_panel(r"\text{Every diameter is a chord.}", width=5.8, height=1.0, font_size=34),
        ).arrange(DOWN, buff=0.22)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "chord layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
        self.play(FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(dots[1]), FadeIn(labs[1]), run_time=RUN_NORMAL)
        self.play(Create(chord), run_time=RUN_SLOW)
        self.play(FadeIn(note[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def arcs(self) -> None:
        self.set_header(3, "ARC", "An arc is part of the circular boundary between two points. The same endpoints can define a minor arc and a major arc.")
        c = LEFT * 3.15 + DOWN * 0.35
        r = 1.78
        circle = self._circle(c, r)
        A = circle_point(c, r, 25)
        B = circle_point(c, r, 145)
        dots = VGroup(Dot(A, radius=0.07, color=BLACK_LINE), Dot(B, radius=0.07, color=BLACK_LINE))
        labs = VGroup(
            self.math("A", 31).next_to(A, UR, buff=0.08),
            self.math("B", 31).next_to(B, UL, buff=0.08),
        )

        # IMPORTANT QA FIX:
        # figure_panel()/split_layout() scale and translate the figure.  The old
        # version built the arcs before that transformation but left them
        # outside panel.figure, so the highlighted arcs drifted above the circle.
        # Build all highlighted arc geometry from the *transformed* circle.
        figure = VGroup(circle, dots, labs)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="THE BOUNDARY BETWEEN A AND B")
        notes = VGroup(
            self._term_card("MINOR ARC", ["Shorter path from A to B", "Measure < 180°"], 5.8),
            self._term_card("MAJOR ARC", ["Longer path from A to B", "Measure > 180°"], 5.8),
            self.formula_panel(r"\text{semicircle}=180^\circ", width=5.8, height=0.95, font_size=38),
        ).arrange(DOWN, buff=0.16)
        layout = self.split_layout(panel.group, notes, left_width=7.1, right_width=6.0, max_height=5.3, center_y=-0.48)
        self.assert_content_safe(layout.group, "arcs layout")

        display_circle = panel.figure[0]
        pc = display_circle.get_center()
        pr = display_circle.width / 2.0
        minor = circle_arc(pc, pr, 25, 145, color=BLACK_LINE, stroke_width=11)
        major = circle_arc(pc, pr, 145, 385, color=DARK_GRAY, stroke_width=10)
        half = circle_arc(pc, pr, 0, 180, color=BLACK_LINE, stroke_width=11)
        diameter = Line(
            circle_point(pc, pr, 180),
            circle_point(pc, pr, 0),
            color=BLACK_LINE,
            stroke_width=3,
        )

        self.play(FadeIn(panel.group), run_time=RUN_NORMAL)
        self.play(Create(minor), FadeIn(notes[0]), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(minor), Create(major), FadeIn(notes[1]), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(major), FadeIn(notes[2]), Create(diameter), run_time=RUN_NORMAL)
        self.play(Create(half), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def tangent(self) -> None:
        self.set_header(4, "TANGENT", "A tangent touches the circle at exactly one point. At that point it is perpendicular to the radius.")
        c = LEFT * 3.2 + DOWN * 0.35; r = 1.80
        circle = self._circle(c, r)
        T = circle_point(c, r, 0)
        tangent = Line(T + UP * 2.15, T + DOWN * 2.15, color=BLACK_LINE, stroke_width=4)
        radius = Line(c, T, color=BLACK_LINE, stroke_width=4)
        dot = Dot(T, radius=0.075, color=BLACK_LINE)
        Tlab = self.math("T", 32).next_to(T, UR, buff=0.15)
        angle_mark = Square(side_length=0.28, stroke_color=BLACK_LINE, stroke_width=2, fill_opacity=0).move_to(T + LEFT*0.14 + UP*0.14)
        figure = VGroup(circle, tangent, radius, dot, Tlab, angle_mark)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="ONE POINT OF CONTACT")
        note = VGroup(
            self._term_card("KEY TEST", ["Touches the circle exactly once", "T is the point of tangency", "Radius OT ⟂ tangent"], 5.8),
            self.formula_panel(r"OT\perp \text{tangent}", width=5.8, height=1.0, font_size=38),
        ).arrange(DOWN, buff=0.22)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "tangent layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
        self.play(FadeIn(dot), FadeIn(Tlab), Create(tangent), run_time=RUN_SLOW)
        self.play(Create(radius), FadeIn(angle_mark), run_time=RUN_NORMAL)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def secant(self) -> None:
        self.set_header(5, "SECANT", "A secant is a line that cuts through the circle and intersects it at two points.")
        c = LEFT * 3.2 + DOWN * 0.35
        r = 1.80
        circle = self._circle(c, r)

        # Offset the secant from the center so students do not mistake it for a
        # diameter with extensions.  Intersections are solved analytically.
        angle = math.radians(18)
        direction = np.array([math.cos(angle), math.sin(angle), 0.0])
        normal = np.array([-math.sin(angle), math.cos(angle), 0.0])
        offset = 0.55
        base = c + normal * offset
        half_chord = math.sqrt(r**2 - offset**2)
        A = base - direction * half_chord
        B = base + direction * half_chord
        P1 = base - direction * 2.75
        P2 = base + direction * 2.75

        secant = Line(P1, P2, color=BLACK_LINE, stroke_width=4)
        dots = VGroup(Dot(A, radius=0.075, color=BLACK_LINE), Dot(B, radius=0.075, color=BLACK_LINE))
        labs = VGroup(
            self.math("A", 31).next_to(A, DL, buff=0.10),
            self.math("B", 31).next_to(B, UR, buff=0.10),
        )
        center_dot = Dot(c, radius=0.055, color=MID_GRAY)
        center_lab = self.math("O", 27).next_to(center_dot, DOWN, buff=0.08)
        figure = VGroup(circle, secant, dots, labs, center_dot, center_lab)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="TWO INTERSECTION POINTS")
        note = self._term_card(
            "KEY TEST",
            [
                "It is a full line, not just a segment.",
                "It enters and leaves the circle.",
                "Two intersections; center not required.",
            ],
            5.8,
        )
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "secant layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), FadeIn(center_dot), FadeIn(center_lab), run_time=RUN_NORMAL)
        self.play(Create(secant), run_time=RUN_SLOW)
        self.play(FadeIn(dots), FadeIn(labs), run_time=RUN_NORMAL)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def compare_lines(self) -> None:
        self.set_header(6, "DO NOT CONFUSE THESE FOUR", "Use the number of contact/intersection points and whether the object is a segment, arc or full line.")
        cards = VGroup()
        data = [
            ("CHORD", "segment", "2 endpoints on circle"),
            ("ARC", "curved boundary", "part of circumference"),
            ("TANGENT", "line", "1 contact point"),
            ("SECANT", "line", "2 intersection points"),
        ]
        for title, kind, test in data:
            card = self.key_value_panel(title, [("Object", kind), ("Recognition", test)], width=6.35, label_size=24, value_size=25)
            cards.add(card)
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.35))
        cards.move_to(DOWN * 0.45)
        self.fit(cards, 13.4, 5.2)
        self.assert_content_safe(cards, "comparison cards")
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.10) for card in cards], lag_ratio=0.16), run_time=RUN_SLOW*1.8)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def central_angle(self) -> None:
        self.set_header(7, "CENTRAL ANGLE AND INTERCEPTED ARC", "When the vertex is at the center, the central angle has the same measure as its intercepted arc.")
        c = LEFT * 3.2 + DOWN * 0.35; r = 1.80
        circle = self._circle(c, r)
        A = circle_point(c, r, 20); B = circle_point(c, r, 100)
        rays = VGroup(Line(c, A, color=BLACK_LINE, stroke_width=4), Line(c, B, color=BLACK_LINE, stroke_width=4))
        arc = circle_arc(c, r, 20, 100, color=BLACK_LINE, stroke_width=10)
        O = Dot(c, radius=0.08, color=BLACK_LINE)
        angle_mark = Angle(rays[0], rays[1], radius=0.52, stroke_width=3, color=DARK_GRAY)
        theta = self.math(r"80^\circ", 40).move_to(self._bisector_point(c, A, B, 0.82))
        figure = VGroup(circle, rays, arc, O, angle_mark, theta)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="VERTEX AT THE CENTER")
        note = VGroup(
            self._term_card("STEP BY STEP", ["1. Find the center vertex.", "2. Follow the two radii to the circle.", "3. The arc between them is intercepted."], 5.8),
            self.formula_panel(r"m\angle AOB=m\widehat{AB}=80^\circ", width=5.8, height=1.0, font_size=34),
        ).arrange(DOWN, buff=0.20)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "central angle layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), FadeIn(O), run_time=RUN_NORMAL)
        self.play(Create(rays[0]), Create(rays[1]), Create(angle_mark), FadeIn(theta), run_time=RUN_NORMAL)
        self.play(Create(arc), run_time=RUN_SLOW)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def inscribed_angle(self) -> None:
        self.set_header(8, "INSCRIBED ANGLE", "When the vertex is on the circle, the inscribed angle measures half of its intercepted arc.")
        c = LEFT * 3.2 + DOWN * 0.35; r = 1.80
        circle = self._circle(c, r)
        A = circle_point(c, r, 20); B = circle_point(c, r, 120); V = circle_point(c, r, 260)
        rays = VGroup(Line(V, A, color=BLACK_LINE, stroke_width=4), Line(V, B, color=BLACK_LINE, stroke_width=4))
        arc = circle_arc(c, r, 20, 120, color=BLACK_LINE, stroke_width=10)
        vertex = Dot(V, radius=0.075, color=BLACK_LINE)
        angle_mark = Angle(rays[0], rays[1], radius=0.48, stroke_width=3, color=DARK_GRAY)
        arc_label = self.math(r"100^\circ", 36).next_to(arc, UP, buff=0.10)
        angle_label = self.math(r"50^\circ", 38).move_to(self._bisector_point(V, A, B, 0.78))
        labels = VGroup(arc_label, angle_label)
        assert_no_overlap([labels[1], vertex], padding=0.08, label="inscribed angle label")
        figure = VGroup(circle, rays, arc, vertex, angle_mark, labels)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="VERTEX ON THE CIRCLE")
        note = VGroup(
            self._term_card("STEP BY STEP", ["1. Vertex lies on the circle.", "2. Identify the intercepted arc.", "3. Divide the arc measure by 2."], 5.8),
            self.formula_panel(r"m\angle AVB=\frac{100^\circ}{2}=50^\circ", width=5.8, height=1.0, font_size=34),
        ).arrange(DOWN, buff=0.20)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "inscribed angle layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
        self.play(FadeIn(vertex), Create(rays[0]), Create(rays[1]), Create(angle_mark), run_time=RUN_NORMAL)
        self.play(Create(arc), FadeIn(labels[0]), run_time=RUN_SLOW)
        self.play(FadeIn(labels[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary(self) -> None:
        self.set_header(9, "CLASS 2 CHECKLIST", "Recognize the object first. Then use the relationship that belongs to it.")

        # The previous process_map stayed small because fit() intentionally
        # never enlarges objects.  Use projector-sized summary cards instead.
        data = [
            ("1  CHORD", "2 endpoints on the circle"),
            ("2  ARC", "curved part of the boundary"),
            ("3  TANGENT", "1 contact point"),
            ("4  SECANT", "2 intersection points"),
            ("5  CENTRAL ANGLE", "angle measure = arc measure"),
            ("6  INSCRIBED ANGLE", "angle measure = arc / 2"),
        ]
        cards = VGroup(
            *[
                self.note_panel(
                    title,
                    [line],
                    width=4.25,
                    title_size=27,
                    body_size=25,
                    max_text_height=1.10,
                )
                for title, line in data
            ]
        )
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.34))
        cards.move_to(UP * 0.10)

        takeaway = self.formula_panel(
            r"m\angle AOB=m\widehat{AB}\qquad"
            r"m\angle AVB=\frac{1}{2}m\widehat{AB}",
            width=9.7,
            height=1.05,
            font_size=34,
        )
        takeaway.next_to(cards, DOWN, buff=0.30)
        group = VGroup(cards, takeaway)
        group.move_to(DOWN * 0.38)
        self.assert_content_safe(group, "summary group")

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.8,
        )
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.standard_closing("Identify the element. Count the intersections. Read the arc. Then calculate.")


# Preview:
# manim -pql Geometry8_Circle_Class2_Parts_Arcs.py Geometry8CircleClass2PartsArcs --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Class2_Parts_Arcs.py Geometry8CircleClass2PartsArcs --disable_caching
