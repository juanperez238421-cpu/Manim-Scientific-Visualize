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
        assert_close(80.0, 80.0, label="central arc example")
        assert_close(50.0, 100.0 / 2.0, label="inscribed angle example")
        assert_close(180.0, 180.0, label="semicircle measure")

    def _circle(self, center: np.ndarray, radius: float = 1.82) -> Circle:
        return Circle(radius=radius, stroke_color=BLACK_LINE, stroke_width=4.0).move_to(center)

    def _term_card(self, title: str, lines: list[str], width: float = 5.6) -> VGroup:
        return self.note_panel(title, lines, width=width, title_size=28, body_size=24, max_text_height=2.25)

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
            self.formula_panel(r"\text{diameter} \subset \text{chords}", width=5.8, height=1.0, font_size=34),
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
        c = LEFT * 3.15 + DOWN * 0.35; r = 1.78
        circle = self._circle(c, r)
        A = circle_point(c, r, 25); B = circle_point(c, r, 145)
        dots = VGroup(Dot(A, radius=0.07, color=BLACK_LINE), Dot(B, radius=0.07, color=BLACK_LINE))
        labs = VGroup(self.math("A", 31).next_to(A, UR, buff=0.08), self.math("B", 31).next_to(B, UL, buff=0.08))
        minor = circle_arc(c, r, 25, 145, color=BLACK_LINE, stroke_width=10)
        major = circle_arc(c, r, 145, 385, color=DARK_GRAY, stroke_width=8)
        figure = VGroup(circle, dots, labs)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="THE BOUNDARY BETWEEN A AND B")
        notes = VGroup(
            self._term_card("MINOR ARC", ["Shorter path from A to B", "Measure < 180°"], 5.8),
            self._term_card("MAJOR ARC", ["Longer path from A to B", "Measure > 180°"], 5.8),
            self.formula_panel(r"\text{semicircle}=180^\circ", width=5.8, height=0.95, font_size=36),
        ).arrange(DOWN, buff=0.16)
        layout = self.split_layout(panel.group, notes, left_width=7.1, right_width=6.0, max_height=5.3, center_y=-0.48)
        self.assert_content_safe(layout.group, "arcs layout")
        self.play(FadeIn(panel.group), run_time=RUN_NORMAL)
        self.play(Create(minor), FadeIn(notes[0]), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(minor), Create(major), FadeIn(notes[1]), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(major), FadeIn(notes[2]), run_time=RUN_NORMAL)
        half = circle_arc(c, r, 0, 180, color=BLACK_LINE, stroke_width=10)
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
        Tlab = self.math("T", 32).next_to(T, UR, buff=0.08)
        angle_mark = Square(side_length=0.28, stroke_color=BLACK_LINE, stroke_width=2, fill_opacity=0).move_to(T + LEFT*0.14 + UP*0.14)
        figure = VGroup(circle, tangent, radius, dot, Tlab, angle_mark)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="ONE POINT OF CONTACT")
        note = VGroup(
            self._term_card("KEY TEST", ["Touches the circle once", "T is the point of tangency", "Radius OT ⟂ tangent"], 5.8),
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
        c = LEFT * 3.2 + DOWN * 0.35; r = 1.80
        circle = self._circle(c, r)
        P1 = c + LEFT * 2.55 + DOWN * 1.00
        P2 = c + RIGHT * 2.55 + UP * 1.00
        secant = Line(P1, P2, color=BLACK_LINE, stroke_width=4)
        direction = (P2-P1)/np.linalg.norm(P2-P1)
        A = c - direction*r; B = c + direction*r
        dots = VGroup(Dot(A, radius=0.075, color=BLACK_LINE), Dot(B, radius=0.075, color=BLACK_LINE))
        labs = VGroup(self.math("A", 31).next_to(A, DL, buff=0.08), self.math("B", 31).next_to(B, UR, buff=0.08))
        figure = VGroup(circle, secant, dots, labs)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="TWO INTERSECTION POINTS")
        note = self._term_card("KEY TEST", ["It is a full line, not just a segment.", "It enters the circle.", "It leaves the circle: two intersections."], 5.8)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "secant layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
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
            card = self.key_value_panel(title, [("Object", kind), ("Recognition", test)], width=6.2, label_size=21, value_size=22)
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
        theta = self.math(r"80^\circ", 40).move_to(c + RIGHT*0.58 + UP*0.45)
        figure = VGroup(circle, rays, arc, O, theta)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="VERTEX AT THE CENTER")
        note = VGroup(
            self._term_card("STEP BY STEP", ["1. Find the center vertex.", "2. Follow the two radii to the circle.", "3. The arc between them is intercepted."], 5.8),
            self.formula_panel(r"m\angle AOB=m\widehat{AB}=80^\circ", width=5.8, height=1.0, font_size=34),
        ).arrange(DOWN, buff=0.20)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "central angle layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), FadeIn(O), run_time=RUN_NORMAL)
        self.play(Create(rays[0]), Create(rays[1]), FadeIn(theta), run_time=RUN_NORMAL)
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
        labels = VGroup(self.math(r"100^\circ", 36).next_to(arc, UP, buff=0.07), self.math(r"50^\circ", 38).move_to(V + UP*0.68))
        figure = VGroup(circle, rays, arc, vertex, labels)
        panel = self.figure_panel(figure, width=7.0, height=5.2, title="VERTEX ON THE CIRCLE")
        note = VGroup(
            self._term_card("STEP BY STEP", ["1. Vertex lies on the circle.", "2. Identify the intercepted arc.", "3. Divide the arc measure by 2."], 5.8),
            self.formula_panel(r"m\angle AVB=\frac{100^\circ}{2}=50^\circ", width=5.8, height=1.0, font_size=34),
        ).arrange(DOWN, buff=0.20)
        layout = self.split_layout(panel.group, note, left_width=7.1, right_width=6.0, max_height=5.25, center_y=-0.48)
        self.assert_content_safe(layout.group, "inscribed angle layout")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(circle), run_time=RUN_NORMAL)
        self.play(FadeIn(vertex), Create(rays[0]), Create(rays[1]), run_time=RUN_NORMAL)
        self.play(Create(arc), FadeIn(labels[0]), run_time=RUN_SLOW)
        self.play(FadeIn(labels[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary(self) -> None:
        self.set_header(9, "CLASS 2 CHECKLIST", "Recognize the object first. Then use the relationship that belongs to it.")
        route = self.process_map([
            ("1", "CHORD\n2 endpoints"),
            ("2", "ARC\ncurved boundary"),
            ("3", "TANGENT\n1 contact"),
            ("4", "SECANT\n2 crossings"),
            ("5", "CENTRAL ANGLE\narc = angle"),
            ("6", "INSCRIBED ANGLE\nangle = arc/2"),
        ], columns=3)
        route.move_to(DOWN * 0.35)
        self.fit(route, 14.0, 4.8)
        self.assert_content_safe(route, "summary map")
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.10) for card in route], lag_ratio=0.10), run_time=RUN_SLOW*1.8)
        self.wait(PAUSE_SUMMARY)
        self.standard_closing("Identify the element. Count the intersections. Read the arc. Then calculate.")


# Preview:
# manim -pql Geometry8_Circle_Class2_Parts_Arcs.py Geometry8CircleClass2PartsArcs --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Class2_Parts_Arcs.py Geometry8CircleClass2PartsArcs --disable_caching
