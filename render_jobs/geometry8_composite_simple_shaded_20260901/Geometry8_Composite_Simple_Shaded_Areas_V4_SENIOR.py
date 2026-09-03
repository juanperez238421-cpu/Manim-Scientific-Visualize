#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V4.

Full frame-by-frame QA revision of V3 after review of the delivered PQH MP4.
This pass fixes the remaining visual/math notation defects found in the actual
rendered timeline, not only in source inspection.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V3_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV3Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, LIGHT, PAPER, FILL


class Geometry8CompositeSimpleShadedAreasV4Senior(
    Geometry8CompositeSimpleShadedAreasV3Senior
):
    """Full-timeline correction pass based on the rendered V3 video."""

    def process_strip(self, active=0):
        labels = ["SEE", "DECOMPOSE", "+ / −", "CALCULATE", "CHECK"]
        strip = VGroup()
        for i, label in enumerate(labels):
            box = RoundedRectangle(
                width=1.86,
                height=.56,
                corner_radius=.08,
                stroke_color=INK if i == active else LIGHT,
                stroke_width=3.2 if i == active else 1.4,
                fill_color=PAPER if i == active else WHITE,
                fill_opacity=1,
            )
            text = self.txt(label, 21, True).move_to(box)
            if i != active:
                text.set_opacity(.38)
            strip.add(VGroup(box, text))
        strip.arrange(RIGHT, buff=.075)
        strip.to_edge(RIGHT, buff=.38).shift(UP * 2.53)
        return strip

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
        whole_label = self.txt("WHOLE RECTANGLE", 24, True).move_to(rect.get_corner(UL)+RIGHT*1.20+DOWN*.35)
        hole_label = self.txt("CIRCULAR HOLE", 23, True).next_to(circle, RIGHT, buff=.34).shift(UP*.42)
        leader = Arrow(
            hole_label.get_left()+LEFT*.04,
            circle.get_right()+UP*.32,
            buff=.08,
            color=INK,
            stroke_width=2.4,
        )
        self.play(FadeIn(whole_label), FadeIn(hole_label), GrowArrow(leader), run_time=.65)
        self.wait(.8)

        self.set_process(strip, 2)
        relation = self.box(
            r"A_s=A_{\mathrm{rectangle}}-A_{\mathrm{circle}}",
            6.15,
            44,
        ).move_to(RIGHT*3.62+UP*.90)
        cue = self.txt("Subtract the hole — do not move or duplicate the geometry.", 24, True)
        cue.move_to(RIGHT*3.62+UP*.05)
        self.fit(cue, 5.95, .48)
        self.play(FadeIn(relation), FadeIn(cue), run_time=.6)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(whole_label, hole_label, leader, relation, cue)), run_time=.35)
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

    def square_minus_quadrant(self):
        h = self.header(
            5,
            "SIMPLE SHADED AREA · SQUARE MINUS QUADRANT",
            "The white quadrant is removed. The small gray corner outside the arc is the target area that remains.",
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
        radius_label = self.eq(r"r=8\ \mathrm{cm}", 30).next_to(radius, UP, buff=.10).shift(LEFT*.48)

        self.play(Create(sq), run_time=.8)
        self.play(FadeIn(sector), FadeIn(VGroup(side_dim, radius, radius_label)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        removed = self.txt("REMOVED QUADRANT", 24, True)
        removed.move_to(corner+RIGHT*1.55+UP*1.05)
        self.fit(removed, 2.75, .45)

        target_point = sq.get_corner(UR)+LEFT*.30+DOWN*.30
        target_label = self.txt("TARGET", 23, True).move_to(LEFT*.55+UP*.95)
        target_arrow = Arrow(
            target_label.get_left()+LEFT*.08,
            target_point,
            buff=.10,
            color=INK,
            stroke_width=2.5,
        )
        relation = self.txt("radius = square side = 8 cm", 26, True)
        relation.move_to(RIGHT*3.62+UP*1.45)
        self.fit(relation, 5.85, .46)
        self.play(
            FadeIn(removed), FadeIn(target_label), GrowArrow(target_arrow), FadeIn(relation),
            run_time=.7,
        )
        self.wait(.7)

        self.set_process(strip, 2)
        self.play(FadeOut(relation), run_time=.25)
        rule = self.box(
            r"A_s=A_{\mathrm{square}}-A_{\mathrm{quadrant}}",
            6.12,
            43,
        ).move_to(RIGHT*3.62+UP*.82)
        radius_note = self.txt("Here 8 cm is a radius, not a diameter.", 25, True)
        radius_note.move_to(RIGHT*3.62+DOWN*.02)
        self.fit(radius_note, 5.9, .45)
        self.play(FadeIn(rule), FadeIn(radius_note), run_time=.6)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(
            FadeOut(VGroup(rule, radius_note, target_label, target_arrow)),
            run_time=.35,
        )
        panel = self.solution_panel(
            "SQUARE − QUADRANT",
            [
                r"A_{\mathrm{square}}=8^2=64",
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

        rect_w, rect_h = 5.0, 3.0
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
            r"d=10\ \mathrm{cm}\quad\Rightarrow\quad r=\frac{10}{2}=5\ \mathrm{cm}",
            6.05,
            40,
        ).move_to(RIGHT*3.58+UP*.92)
        self.play(Create(diameter), Create(radius), FadeIn(radius_step), run_time=.7)
        self.wait(1.1)

        self.set_process(strip, 2)
        self.play(FadeOut(radius_step), run_time=.28)
        structure = self.box(
            r"A_T=A_{\mathrm{rect}}+A_{\mathrm{semi}}",
            6.05,
            43,
        ).move_to(RIGHT*3.58+UP*.78)
        internal_note = self.txt("The shared diameter is an internal boundary — do not subtract it.", 24, True)
        internal_note.move_to(RIGHT*3.58+DOWN*.18)
        self.fit(internal_note, 5.95, .46)
        self.play(FadeIn(structure), FadeIn(internal_note), run_time=.55)
        self.wait(1.1)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(structure, internal_note)), run_time=.30)
        panel = self.solution_panel(
            "ADD BOTH TARGET PIECES",
            [
                r"A_{\mathrm{rect}}=10(6)=60",
                r"A_{\mathrm{semi}}=\frac{\pi(5)^2}{2}=\frac{25\pi}{2}",
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

    def hidden_dimensions(self):
        h = self.header(
            7,
            "BEFORE CALCULATING · COMPLETE THE MISSING DIMENSIONS",
            "Match horizontal pieces with the total width and vertical pieces with the total height.",
        )
        self.add(h)

        x0, y0, sx, sy = -6.25, -1.85, .40, .40
        fill, outline = self._concave_l(x0, y0, sx, sy, 12, 8, 4, 3, opacity=.70)
        self.play(FadeIn(fill), Create(outline), run_time=.8)

        known = VGroup(
            self.dimension_line([x0,y0-.24,0],[x0+12*sx,y0-.24,0],r"12",DOWN,29),
            self.dimension_line([x0-.24,y0,0],[x0-.24,y0+8*sy,0],r"8",LEFT,29),
            self.dimension_line([x0+8*sx,y0+8*sy+.20,0],[x0+12*sx,y0+8*sy+.20,0],r"4",UP,29),
            self.dimension_line([x0+12*sx+.20,y0+5*sy,0],[x0+12*sx+.20,y0+8*sy,0],r"3",RIGHT,29),
        )
        self.play(FadeIn(known), run_time=.7)

        unknown_top = self.dimension_line(
            [x0,y0+8*sy+.50,0], [x0+8*sx,y0+8*sy+.50,0], r"x", UP, 31,
        )
        unknown_right = self.dimension_line(
            [x0+12*sx+.52,y0,0], [x0+12*sx+.52,y0+5*sy,0], r"y", RIGHT, 31,
        )
        question = VGroup(
            self.txt("STEP 1 · WRITE THE SEGMENT EQUATIONS", 28, True),
            self.txt("Total = one piece + the missing piece", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.10).move_to(RIGHT*3.55+UP*1.35)
        self.fit(question, 6.15, .95)
        self.play(FadeIn(VGroup(unknown_top, unknown_right, question)), run_time=.65)
        self.wait(1.5)

        equations = VGroup(
            self.eq(r"12=x+4", 42),
            self.eq(r"x=12-4=8", 42),
            self.eq(r"8=3+y", 42),
            self.eq(r"y=8-3=5", 42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.20).move_to(RIGHT*3.45+DOWN*.20)

        self.play(FadeIn(equations[0]), run_time=.5)
        self.wait(.55)
        self.play(FadeIn(equations[1]), run_time=.5)
        self.wait(.65)

        solved_top = self.dimension_line(
            [x0,y0+8*sy+.50,0], [x0+8*sx,y0+8*sy+.50,0], r"8", UP, 31,
        )
        self.play(Transform(unknown_top, solved_top), run_time=.55)
        self.wait(.55)

        self.play(FadeIn(equations[2]), run_time=.5)
        self.wait(.55)
        self.play(FadeIn(equations[3]), run_time=.5)
        self.wait(.65)

        solved_right = self.dimension_line(
            [x0+12*sx+.52,y0,0], [x0+12*sx+.52,y0+5*sy,0], r"5", RIGHT, 31,
        )
        self.play(Transform(unknown_right, solved_right), run_time=.55)

        rule = self.box(
            r"\text{Complete dimensions first}\;\longrightarrow\;\text{area second}",
            6.85,
            39,
        ).move_to(RIGHT*3.45+DOWN*2.22)
        self.play(FadeIn(rule), run_time=.6)
        self.wait(3.0)
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
        rect_lab = self.txt("+ RECTANGLE", 22, True).move_to(rect.get_center()+DOWN*.90)
        tri_lab = self.txt("+ TRIANGLE", 22, True).move_to(LEFT*.45+UP*.85)
        tri_arrow = Arrow(
            tri_lab.get_left()+LEFT*.05,
            roof.get_center()+RIGHT*.42,
            buff=.10,
            color=INK,
            stroke_width=2.3,
        )
        circ_lab = self.txt("− CIRCLE", 22, True).next_to(window, RIGHT, buff=.52)
        circ_arrow = Arrow(
            circ_lab.get_left()+LEFT*.04,
            window.get_right(),
            buff=.08,
            color=INK,
            stroke_width=2.4,
        )
        callouts = VGroup(rect_lab, tri_lab, tri_arrow, circ_lab, circ_arrow)
        self.play(
            FadeIn(rect_lab), FadeIn(tri_lab), GrowArrow(tri_arrow),
            FadeIn(circ_lab), GrowArrow(circ_arrow),
            run_time=.65,
        )
        self.wait(.9)

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
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V4_SENIOR.py Geometry8CompositeSimpleShadedAreasV4Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V4_SENIOR.py Geometry8CompositeSimpleShadedAreasV4Senior --disable_caching
