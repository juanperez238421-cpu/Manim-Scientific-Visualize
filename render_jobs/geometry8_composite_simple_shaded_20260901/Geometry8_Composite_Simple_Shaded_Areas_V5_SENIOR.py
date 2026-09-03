#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V5.

Final manual-frame QA pass on top of V4.  V4 fixed the mathematical notation,
sequencing and decomposition logic, but full-resolution inspection still found
residual annotation crowding in the rectangle-hole and guided-house scenes.
V5 keeps all approved mathematics and removes those last collisions.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V4_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV4Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, FILL


class Geometry8CompositeSimpleShadedAreasV5Senior(
    Geometry8CompositeSimpleShadedAreasV4Senior
):
    """Final high-resolution annotation-spacing correction pass."""

    def rectangle_minus_circle(self):
        h = self.header(
            4,
            "SIMPLE SHADED AREA · RECTANGLE MINUS CIRCULAR HOLE",
            "Keep the whole rectangle visible and identify the circular hole as the one region to subtract.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        rect = Rectangle(
            width=5.10,
            height=4.05,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.78,
        ).move_to(LEFT * 3.70 + DOWN * .18)
        circle = Circle(
            radius=1.23,
            color=INK,
            stroke_width=5,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(rect)

        width_dim = self.dimension_line(
            rect.get_corner(DL) + DOWN*.25,
            rect.get_corner(DR) + DOWN*.25,
            r"12\ \mathrm{cm}", DOWN, 30,
        )
        height_dim = self.dimension_line(
            rect.get_corner(DL) + LEFT*.25,
            rect.get_corner(UL) + LEFT*.25,
            r"10\ \mathrm{cm}", LEFT, 30,
        )
        radius = Line(circle.get_center(), circle.get_right(), color=INK, stroke_width=3)
        radius_label = self.eq(r"r=3\ \mathrm{cm}", 30).next_to(radius, UP, buff=.08)

        self.play(Create(rect), run_time=.8)
        self.play(Create(circle), FadeIn(VGroup(width_dim, height_dim, radius, radius_label)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        # Keep both semantic labels INSIDE their own regions so they cannot
        # collide with dimensions, panel borders or one another.
        whole_label = self.txt("WHOLE", 23, True)
        whole_label.move_to(rect.get_corner(UL)+RIGHT*1.18+DOWN*.40)
        hole_label = self.txt("HOLE", 23, True)
        hole_label.move_to(circle.get_center()+DOWN*.62)
        self.play(FadeIn(whole_label), FadeIn(hole_label), run_time=.55)
        self.wait(.9)

        self.set_process(strip, 2)
        relation = self.box(
            r"A_s=A_{\mathrm{rectangle}}-A_{\mathrm{circle}}",
            6.15,
            44,
        ).move_to(RIGHT*3.62+UP*.90)
        cue = self.txt("Subtract the hole. Keep the original geometry fixed.", 24, True)
        cue.move_to(RIGHT*3.62+DOWN*.02)
        self.fit(cue, 5.90, .48)
        self.play(FadeIn(relation), FadeIn(cue), run_time=.6)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(
            FadeOut(VGroup(whole_label, hole_label, relation, cue)),
            run_time=.35,
        )
        panel = self.solution_panel(
            "WHOLE − HOLE",
            [
                r"A_{\mathrm{rect}}=12(10)=120",
                r"A_{\mathrm{circle}}=\pi(3)^2=9\pi",
                r"A_s=120-9\pi",
            ],
            r"A_s\approx91.73\ \mathrm{cm}^2",
            y=-.24,
            height=4.62,
        )
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.6)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.3)
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
        h_lab.move_to(altitude.get_center()+LEFT*.80)
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
        self.wait(5.0)

        self.set_process(strip, 1)
        # All operation labels stay inside their regions.  This preserves the
        # geometry-first explanation and leaves the right column completely
        # clear for the symbolic area expression.
        rect_lab = self.txt("+ RECTANGLE", 22, True)
        rect_lab.move_to(rect.get_center()+DOWN*.90)

        tri_lab = self.txt("+ TRIANGLE", 20, True)
        self.fit(tri_lab, 1.82, .40)
        tri_lab.move_to(roof.get_center()+RIGHT*.72+DOWN*.12)

        circ_lab = self.txt("− CIRCLE", 20, True)
        self.fit(circ_lab, 1.35, .40)
        circ_lab.next_to(window, RIGHT, buff=.22)

        callouts = VGroup(rect_lab, tri_lab, circ_lab)
        self.play(FadeIn(callouts), run_time=.60)
        self.wait(1.0)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_{\mathrm{rect}}+A_{\triangle}-A_{\mathrm{circle}}",
            6.18,
            42,
        ).move_to(RIGHT*3.55+UP*.95)
        self.play(FadeOut(prompt), FadeIn(structure), run_time=.6)
        self.wait(.9)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(structure, callouts)), run_time=.35)
        panel = self.solution_panel(
            "ADD + SUBTRACT",
            [
                r"A_{\mathrm{rect}}=8(5)=40",
                r"A_{\triangle}=\frac{8(3)}{2}=12",
                r"A_{\mathrm{circle}}=\pi(1)^2=\pi",
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
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V5_SENIOR.py Geometry8CompositeSimpleShadedAreasV5Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V5_SENIOR.py Geometry8CompositeSimpleShadedAreasV5Senior --disable_caching
