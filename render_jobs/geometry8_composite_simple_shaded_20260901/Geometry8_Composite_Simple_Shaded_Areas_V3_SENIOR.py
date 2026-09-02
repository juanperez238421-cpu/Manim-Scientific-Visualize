#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V3.

Final visual-QA correction pass after inspecting the V2 PQH contact sheet at
full resolution.  This pass removes residual annotation/panel collisions and
separates geometric dimensions from operation labels in the guided challenge.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V2_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV2Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, FILL


class Geometry8CompositeSimpleShadedAreasV3Senior(
    Geometry8CompositeSimpleShadedAreasV2Senior
):
    """Final projector-safe revision after full-resolution V2 visual QA."""

    def square_minus_quadrant(self):
        h = self.header(
            5,
            "SIMPLE SHADED AREA · SQUARE MINUS QUADRANT",
            "The white quadrant is removed. The small gray corner is the target area that remains.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        side = 4.30
        sq = Square(
            side_length=side,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.82,
        ).move_to(LEFT*3.70+DOWN*.18)
        corner = sq.get_corner(DL)
        sector = Sector(
            radius=side,
            angle=PI/2,
            start_angle=0,
            arc_center=corner,
            stroke_color=INK,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        side_dim = self.dimension_line(
            sq.get_corner(DL)+DOWN*.24,
            sq.get_corner(DR)+DOWN*.24,
            r"8\ \mathrm{cm}", DOWN, 30,
        )
        radius = Line(corner, sq.get_corner(DR), color=INK, stroke_width=3)
        rlab = self.eq(r"r=8\ \mathrm{cm}", 30).next_to(radius, UP, buff=.10).shift(LEFT*.48)

        self.play(Create(sq), run_time=.8)
        self.play(FadeIn(sector), FadeIn(VGroup(side_dim, radius, rlab)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        removed = self.txt("REMOVED QUADRANT", 24, True)
        removed.move_to(corner+RIGHT*1.55+UP*1.05)
        self.fit(removed, 2.75, .45)
        target = self.txt("TARGET", 22, True)
        target.move_to(sq.get_corner(UR)+LEFT*.60+DOWN*.30)
        relation = self.txt("radius = square side = 8 cm", 26, True)
        relation.move_to(RIGHT*3.62+UP*1.45)
        self.fit(relation, 5.85, .46)
        self.play(FadeIn(removed), FadeIn(target), FadeIn(relation), run_time=.7)
        self.wait(.6)

        self.set_process(strip, 2)
        rule = self.box(
            r"A_s=A_{\square}-A_{\mathrm{quadrant}}",
            6.05, 45,
        ).move_to(RIGHT*3.62+UP*.62)
        radius_note = self.txt("Here 8 cm is a radius, not a diameter.", 25, True)
        radius_note.move_to(RIGHT*3.62+DOWN*.15)
        self.fit(radius_note, 5.9, .45)
        self.play(FadeIn(rule), FadeIn(radius_note), run_time=.6)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(relation, rule, radius_note)), run_time=.35)
        panel = self.solution_panel(
            "SQUARE − QUADRANT",
            [
                r"A_{\square}=8^2=64",
                r"A_Q=\frac{\pi(8)^2}{4}=16\pi",
                r"A_s=64-16\pi",
            ],
            r"A_s\approx13.73\ \mathrm{cm}^2",
            y=-.30,
            height=4.55,
        )
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.7)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.7)
        self.wipe()

    def rectangle_plus_semicircle(self):
        h = self.header(
            6,
            "COMPOSITE ADDITION · RECTANGLE PLUS SEMICIRCLE",
            "Both pieces belong to the target, so their areas are added.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        rect_w, rect_h = 5.0, 3.0  # exact visual ratio 10:6
        center = np.array([-3.65, -1.05, 0.0])
        rect = Rectangle(
            width=rect_w, height=rect_h,
            color=INK, stroke_width=5,
            fill_color=FILL, fill_opacity=.72,
        ).move_to(center)
        top_mid = rect.get_top()
        semi = Sector(
            radius=rect_w/2,
            angle=PI,
            start_angle=0,
            arc_center=top_mid,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.72,
        )
        dims = VGroup(
            self.dimension_line(rect.get_corner(DL)+DOWN*.22,rect.get_corner(DR)+DOWN*.22,r"10\ \mathrm{cm}",DOWN,29),
            self.dimension_line(rect.get_corner(DL)+LEFT*.22,rect.get_corner(UL)+LEFT*.22,r"6\ \mathrm{cm}",LEFT,29),
        )
        self.play(Create(rect), FadeIn(dims), run_time=.8)
        self.play(Create(semi), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        diameter = Line(
            top_mid+LEFT*(rect_w/2), top_mid+RIGHT*(rect_w/2),
            color=MID, stroke_width=3,
        )
        radius = Line(top_mid, top_mid+RIGHT*(rect_w/2), color=INK, stroke_width=3)
        radius_step = self.box(
            r"d=10\ \Rightarrow\ r=\frac{10}{2}=5\ \mathrm{cm}",
            5.8, 42,
        ).move_to(RIGHT*3.58+UP*1.35)
        self.play(Create(diameter), Create(radius), FadeIn(radius_step), run_time=.7)
        self.wait(.8)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_{\mathrm{rectangle}}+A_{\mathrm{semicircle}}",
            6.15, 42,
        ).move_to(RIGHT*3.58+UP*.42)
        internal_note = self.txt("The shared diameter is internal; it is not removed.", 24, True)
        internal_note.move_to(RIGHT*3.58+DOWN*.30)
        self.fit(internal_note, 5.95, .43)
        self.play(FadeIn(structure), FadeIn(internal_note), run_time=.55)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(radius_step, structure, internal_note)), run_time=.35)
        panel = self.solution_panel(
            "ADD BOTH TARGET PIECES",
            [
                r"A_R=10(6)=60",
                r"A_S=\frac{\pi(5)^2}{2}=\frac{25\pi}{2}",
                r"A_T=60+\frac{25\pi}{2}",
            ],
            r"A_T\approx99.27\ \mathrm{cm}^2",
            y=-.30,
            height=4.55,
        )
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.8)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.6)
        self.wipe()

    def guided_challenge(self):
        h = self.header(
            9,
            "GUIDED CHALLENGE · HOUSE WITH A CIRCULAR WINDOW",
            "Add the rectangle and triangular roof, then subtract the circular window.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        rect_w, rect_h = 4.65, 2.90
        base_center = np.array([-3.75, -1.05, 0.0])
        rect = Rectangle(
            width=rect_w, height=rect_h,
            color=INK, stroke_width=5,
            fill_color=FILL, fill_opacity=.74,
        ).move_to(base_center)
        apex = rect.get_top()+UP*1.75
        roof = Polygon(
            rect.get_corner(UL), rect.get_corner(UR), apex,
            color=INK, stroke_width=5,
            fill_color=FILL, fill_opacity=.74,
        )
        window = Circle(
            radius=.55,
            color=INK, stroke_width=4,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(rect.get_center()+UP*.22)

        base_dim = self.dimension_line(
            rect.get_corner(DL)+DOWN*.22,
            rect.get_corner(DR)+DOWN*.22,
            r"8\ \mathrm{cm}", DOWN, 29,
        )
        wall_dim = self.dimension_line(
            rect.get_corner(DL)+LEFT*.22,
            rect.get_corner(UL)+LEFT*.22,
            r"5\ \mathrm{cm}", LEFT, 29,
        )
        altitude = DashedLine(rect.get_top(), apex, color=MID, stroke_width=3)
        h_lab = self.eq(r"h_{\triangle}=3\ \mathrm{cm}", 26)
        h_lab.move_to(altitude.get_center()+LEFT*.78)

        # Draw the radius to the LEFT so it cannot collide with the subtraction label.
        radius_line = Line(window.get_center(), window.get_left(), color=INK, stroke_width=3)
        r_lab = self.eq(r"r=1\ \mathrm{cm}", 25).next_to(radius_line, UP, buff=.06).shift(LEFT*.08)

        self.play(Create(rect), Create(roof), Create(window), run_time=1.0)
        self.play(
            FadeIn(VGroup(base_dim, wall_dim)),
            Create(altitude), FadeIn(h_lab),
            Create(radius_line), FadeIn(r_lab),
            run_time=.8,
        )

        prompt = VGroup(
            self.txt("YOUR TURN", 34, True),
            self.txt("Write the area expression before calculating.", 29),
            self.eq(r"A_T=\ ?", 50),
        ).arrange(DOWN, buff=.24).move_to(RIGHT*3.55+DOWN*.05)
        self.fit(prompt, 6.0, 2.4)
        self.play(FadeIn(prompt), run_time=.6)
        self.wait(5.5)

        self.set_process(strip, 1)
        rect_lab = self.txt("+ RECTANGLE", 23, True).move_to(rect.get_center()+DOWN*.88)
        tri_lab = self.txt("+ TRIANGLE", 22, True).move_to(roof.get_center()+RIGHT*.82+DOWN*.12)
        circ_lab = self.txt("− CIRCLE", 22, True).next_to(window, RIGHT, buff=.58)
        leader = Arrow(
            circ_lab.get_left()+LEFT*.04,
            window.get_right(),
            buff=.08, color=INK, stroke_width=2.4,
        )
        self.play(
            FadeIn(rect_lab), FadeIn(tri_lab), FadeIn(circ_lab), GrowArrow(leader),
            run_time=.65,
        )
        self.wait(.9)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_R+A_{\triangle}-A_C",
            6.15, 47,
        ).move_to(RIGHT*3.55+UP*1.25)
        self.play(FadeOut(prompt), FadeIn(structure), run_time=.6)
        self.wait(.8)

        self.set_process(strip, 3)
        self.play(FadeOut(structure), run_time=.30)
        panel = self.solution_panel(
            "ADD + SUBTRACT",
            [
                r"A_R=8(5)=40",
                r"A_{\triangle}=\frac{8(3)}{2}=12",
                r"A_C=\pi(1)^2=\pi",
                r"A_T=40+12-\pi",
            ],
            r"A_T\approx48.86\ \mathrm{cm}^2",
            y=-.25,
            height=4.82,
        )
        self.play(FadeIn(panel), run_time=.7)
        self.wait(3.0)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.5)
        self.wipe()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V3_SENIOR.py Geometry8CompositeSimpleShadedAreasV3Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V3_SENIOR.py Geometry8CompositeSimpleShadedAreasV3Senior --disable_caching
