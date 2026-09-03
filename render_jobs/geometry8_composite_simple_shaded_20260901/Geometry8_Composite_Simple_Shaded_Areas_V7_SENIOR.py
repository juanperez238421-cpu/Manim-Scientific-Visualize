#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V7.

Targeted senior QA revision based on direct frame inspection of the V6 PQH
binary.  V7 preserves all accepted mathematics and pedagogy while enforcing a
clear vertical safe zone below the process strip and widening the separation
between parallel dimension annotations.

Verified V6 residual issues corrected here:
  1) L-shape top 4-unit dimension touched the process strip.
  2) Semicircle arc crossed the SEE/DECOMPOSE process strip.
  3) Hidden-dimension right-side 3 and y/5 annotations remained crowded.
  4) House roof apex sat too close to the process strip.
  5) Formula-toolbox labels receive a modest projector-legibility increase.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V6_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV6Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, PAPER, FILL


class Geometry8CompositeSimpleShadedAreasV7Senior(
    Geometry8CompositeSimpleShadedAreasV6Senior
):
    """Targeted safe-zone and micro-spacing correction pass."""

    def mini_formula_card(self, name, formula):
        card = RoundedRectangle(
            width=2.58,
            height=1.66,
            corner_radius=.10,
            stroke_color=INK,
            stroke_width=1.9,
            fill_color=PAPER,
            fill_opacity=1,
        )
        name_m = self.txt(name, 25, True)
        formula_m = self.eq(formula, 37)
        self.fit(name_m, 2.22, .44)
        self.fit(formula_m, 2.22, .60)
        VGroup(name_m, formula_m).arrange(DOWN, buff=.14).move_to(card)
        return VGroup(card, name_m, formula_m)

    def l_shape_two_methods(self):
        h = self.header(
            3,
            "COMPOSITE FIGURE · ONE REGION, TWO VALID METHODS",
            "Different correct decompositions must produce the same target area.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        x0, y0 = -6.0, -2.28
        sx, sy = .55, .55
        pts = [
            [x0, y0, 0],
            [x0 + 9*sx, y0, 0],
            [x0 + 9*sx, y0 + 4*sy, 0],
            [x0 + 5*sx, y0 + 4*sy, 0],
            [x0 + 5*sx, y0 + 7*sy, 0],
            [x0, y0 + 7*sy, 0],
        ]
        L = Polygon(*pts, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.72)

        total_w = self.dimension_line(
            [x0, y0 - .24, 0], [x0 + 9*sx, y0 - .24, 0], r"9", DOWN, 31,
        )
        total_h = self.dimension_line(
            [x0 - .26, y0, 0], [x0 - .26, y0 + 7*sy, 0], r"7", LEFT, 31,
        )
        notch_w = self.dimension_line(
            [x0 + 5*sx, y0 + 7*sy + .10, 0],
            [x0 + 9*sx, y0 + 7*sy + .10, 0],
            r"4", UP, 31,
        )
        notch_h = self.dimension_line(
            [x0 + 9*sx + .20, y0 + 4*sy, 0],
            [x0 + 9*sx + .20, y0 + 7*sy, 0],
            r"3", RIGHT, 31,
        )

        self.play(Create(L), run_time=.9)
        self.play(FadeIn(VGroup(total_w, total_h, notch_w, notch_h)), run_time=.8)
        self.wait(1.0)

        self.set_process(strip, 1)
        missing = Rectangle(
            width=4*sx, height=3*sy, color=INK, stroke_width=4,
            fill_color=WHITE, fill_opacity=1,
        )
        missing.move_to([x0 + 7*sx, y0 + 5.5*sy, 0])
        missing_label = self.txt("MISSING 4 × 3", 23, True).move_to(missing)
        self.fit(missing_label, 1.85, .38)
        self.play(FadeIn(missing), FadeIn(missing_label), run_time=.6)
        self.wait(.8)

        self.set_process(strip, 2)
        method_a = self.solution_panel(
            "METHOD A · WHOLE − MISSING",
            [r"A_{\mathrm{whole}}=9(7)=63", r"A_{\mathrm{missing}}=4(3)=12", r"A_T=63-12"],
            r"A_T=51\ \mathrm{cm}^2",
        )
        self.play(FadeIn(method_a), run_time=.7)
        self.wait(2.0)

        self.set_process(strip, 3)
        split = DashedLine(
            [x0 + 5*sx, y0, 0], [x0 + 5*sx, y0 + 4*sy, 0],
            color=MID, stroke_width=3,
        )
        self.play(FadeOut(VGroup(missing, missing_label)), Create(split), run_time=.6)
        area_labs = VGroup(
            self.txt("5 × 7", 25, True).move_to([x0+2.5*sx, y0+3.45*sy, 0]),
            self.txt("4 × 4", 25, True).move_to([x0+7*sx, y0+2.0*sy, 0]),
        )
        alt = VGroup(
            self.eq(r"A_1=5(7)=35", 37),
            self.eq(r"A_2=4(4)=16", 37),
            self.box(r"A_T=35+16=51\ \mathrm{cm}^2", 5.25, 42),
        ).arrange(DOWN, buff=.18).move_to(RIGHT * 3.75 + DOWN * 1.20)
        self.play(FadeOut(method_a), FadeIn(area_labs), FadeIn(alt), run_time=.65)
        self.wait(2.0)

        self.set_process(strip, 4)
        check = self.txt("METHOD A = METHOD B = 51 cm²", 31, True).move_to(RIGHT * 3.62 + UP * 1.55)
        self.fit(check, 6.15, .62)
        self.play(FadeIn(check), run_time=.5)
        self.wait(3.0)
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
        center = np.array([-3.65, -2.00, 0.0])
        rect = Rectangle(
            width=rect_w, height=rect_h, color=INK, stroke_width=5,
            fill_color=FILL, fill_opacity=.72,
        ).move_to(center)
        top_mid = rect.get_top()
        semi = Sector(
            radius=rect_w/2, angle=PI, start_angle=0, arc_center=top_mid,
            stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.72,
        )
        dims = VGroup(
            self.dimension_line(rect.get_corner(DL)+DOWN*.10, rect.get_corner(DR)+DOWN*.10, r"10\ \mathrm{cm}", DOWN, 30),
            self.dimension_line(rect.get_corner(DL)+LEFT*.20, rect.get_corner(UL)+LEFT*.20, r"6\ \mathrm{cm}", LEFT, 30),
        )
        self.play(Create(rect), FadeIn(dims), run_time=.8)
        self.play(Create(semi), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        diameter = Line(top_mid+LEFT*(rect_w/2), top_mid+RIGHT*(rect_w/2), color=MID, stroke_width=3)
        radius = Line(top_mid, top_mid+RIGHT*(rect_w/2), color=INK, stroke_width=3)
        radius_step = self.box(r"d=10\ \mathrm{cm}\quad\Rightarrow\quad r=5\ \mathrm{cm}", 6.05, 43).move_to(RIGHT*3.58+UP*.92)
        self.play(Create(diameter), Create(radius), FadeIn(radius_step), run_time=.7)
        self.wait(1.1)

        self.set_process(strip, 2)
        self.play(FadeOut(radius_step), run_time=.28)
        structure = self.box(r"A_T=A_{\mathrm{rect}}+A_{\mathrm{semi}}", 6.05, 45).move_to(RIGHT*3.58+UP*.88)
        note_box = RoundedRectangle(
            width=6.05, height=1.02, corner_radius=.10, stroke_color=INK, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT*3.58+DOWN*.26)
        note = VGroup(
            self.txt("SHARED DIAMETER = INTERNAL BOUNDARY", 26, True),
            self.txt("It is not removed from the area.", 27),
        ).arrange(DOWN, buff=.08).move_to(note_box)
        self.fit(note, 5.65, .72)
        self.play(FadeIn(structure), FadeIn(VGroup(note_box, note)), run_time=.55)
        self.wait(1.2)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(structure, note_box, note)), run_time=.30)
        panel = self.solution_panel(
            "ADD BOTH TARGET PIECES",
            [r"A_{\mathrm{rect}}=10(6)=60", r"A_{\mathrm{semi}}=\frac{\pi(5)^2}{2}=\frac{25\pi}{2}", r"A_T=60+\frac{25\pi}{2}"],
            r"A_T\approx99.27\ \mathrm{cm}^2", y=-.30, height=4.55,
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
        x0, y0, sx, sy = -6.40, -1.85, .40, .40
        fill, outline = self._concave_l(x0, y0, sx, sy, 12, 8, 4, 3, opacity=.70)
        self.play(FadeIn(fill), Create(outline), run_time=.8)
        known_right_x = x0 + 12*sx + .18
        unknown_right_x = x0 + 12*sx + .90
        known = VGroup(
            self.dimension_line([x0,y0-.26,0],[x0+12*sx,y0-.26,0],r"12",DOWN,31),
            self.dimension_line([x0-.27,y0,0],[x0-.27,y0+8*sy,0],r"8",LEFT,31),
            self.dimension_line([x0+8*sx,y0+8*sy+.22,0],[x0+12*sx,y0+8*sy+.22,0],r"4",UP,31),
            self.dimension_line([known_right_x,y0+5*sy,0],[known_right_x,y0+8*sy,0],r"3",RIGHT,31),
        )
        self.play(FadeIn(known), run_time=.7)
        unknown_top = self.dimension_line([x0,y0+8*sy+.58,0], [x0+8*sx,y0+8*sy+.58,0], r"x", UP, 34)
        unknown_right = self.dimension_line([unknown_right_x,y0,0], [unknown_right_x,y0+5*sy,0], r"y", RIGHT, 34)
        question = VGroup(
            self.txt("STEP 1 · WRITE THE SEGMENT EQUATIONS", 30, True),
            self.txt("Total length = known piece + missing piece", 27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.11).move_to(RIGHT*3.50+UP*1.36)
        self.fit(question, 6.20, 1.02)
        self.play(FadeIn(VGroup(unknown_top, unknown_right, question)), run_time=.65)
        self.wait(1.5)
        equations = VGroup(
            self.eq(r"12=x+4", 44), self.eq(r"x=12-4=8", 44),
            self.eq(r"8=3+y", 44), self.eq(r"y=8-3=5", 44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.19).move_to(RIGHT*3.45+DOWN*.10)
        self.play(FadeIn(equations[0]), run_time=.5); self.wait(.55)
        self.play(FadeIn(equations[1]), run_time=.5); self.wait(.65)
        solved_top = self.dimension_line([x0,y0+8*sy+.58,0], [x0+8*sx,y0+8*sy+.58,0], r"8", UP, 34)
        self.play(Transform(unknown_top, solved_top), run_time=.55); self.wait(.55)
        self.play(FadeIn(equations[2]), run_time=.5); self.wait(.55)
        self.play(FadeIn(equations[3]), run_time=.5); self.wait(.65)
        solved_right = self.dimension_line([unknown_right_x,y0,0], [unknown_right_x,y0+5*sy,0], r"5", RIGHT, 34)
        self.play(Transform(unknown_right, solved_right), run_time=.55)
        rule = self.box(r"\text{Complete dimensions first}\;\longrightarrow\;\text{area second}", 6.75, 40).move_to(RIGHT*3.45+DOWN*2.12)
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
        base_center = np.array([-3.75, -1.28, 0.0])
        rect = Rectangle(width=rect_w, height=rect_h, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.74).move_to(base_center)
        apex = rect.get_top()+UP*1.75
        roof = Polygon(rect.get_corner(UL), rect.get_corner(UR), apex, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.74)
        window = Circle(radius=.55, color=INK, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to(rect.get_center()+UP*.22)
        base_dim = self.dimension_line(rect.get_corner(DL)+DOWN*.18, rect.get_corner(DR)+DOWN*.18, r"8\ \mathrm{cm}", DOWN, 31)
        wall_dim = self.dimension_line(rect.get_corner(DL)+LEFT*.22, rect.get_corner(UL)+LEFT*.22, r"5\ \mathrm{cm}", LEFT, 31)
        altitude = DashedLine(rect.get_top(), apex, color=MID, stroke_width=3)
        h_chip = RoundedRectangle(width=2.10, height=.62, corner_radius=.08, stroke_color=INK, stroke_width=1.5, fill_color=WHITE, fill_opacity=.97).move_to(altitude.get_center()+RIGHT*.78)
        h_text = self.eq(r"h=3\ \mathrm{cm}", 30).move_to(h_chip)
        radius_line = Line(window.get_center(), window.get_left(), color=INK, stroke_width=3)
        r_text = self.eq(r"r=1\ \mathrm{cm}", 30).next_to(window, DOWN, buff=.13)
        self.play(Create(rect), Create(roof), Create(window), run_time=1.0)
        self.play(FadeIn(VGroup(base_dim, wall_dim)), Create(altitude), FadeIn(VGroup(h_chip, h_text)), Create(radius_line), FadeIn(r_text), run_time=.8)
        prompt = VGroup(self.txt("YOUR TURN", 36, True), self.txt("Write the area expression before calculating.", 30), self.eq(r"A_T=\ ?", 52)).arrange(DOWN, buff=.24).move_to(RIGHT*3.55+DOWN*.05)
        self.fit(prompt, 6.0, 2.45)
        self.play(FadeIn(prompt), run_time=.6)
        self.wait(5.0)
        self.set_process(strip, 1)
        self.play(FadeOut(prompt), run_time=.25)
        operation_panel = RoundedRectangle(width=5.75, height=2.75, corner_radius=.13, stroke_color=INK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(RIGHT*3.55+DOWN*.18)
        op_title = self.txt("DECOMPOSE THE TARGET", 30, True)
        op_rows = VGroup(self.txt("1.  +  RECTANGLE", 29, True), self.txt("2.  +  TRIANGLE", 29, True), self.txt("3.  −  CIRCLE", 29, True)).arrange(DOWN, aligned_edge=LEFT, buff=.19)
        op_content = VGroup(op_title, op_rows).arrange(DOWN, aligned_edge=LEFT, buff=.24).move_to(operation_panel)
        self.fit(op_content, 5.25, 2.25)
        self.play(FadeIn(VGroup(operation_panel, op_content)), run_time=.6)
        self.play(Circumscribe(rect, color=GRAY), run_time=.45)
        self.play(Circumscribe(roof, color=GRAY), run_time=.45)
        self.play(Circumscribe(window, color=GRAY), run_time=.45)
        self.wait(.7)
        self.set_process(strip, 2)
        structure = self.box(r"A_T=A_{\mathrm{rect}}+A_{\triangle}-A_{\mathrm{circle}}", 6.18, 43).move_to(RIGHT*3.55+UP*.82)
        self.play(FadeOut(VGroup(operation_panel, op_content)), FadeIn(structure), run_time=.6)
        self.wait(.9)
        self.set_process(strip, 3)
        self.play(FadeOut(structure), run_time=.30)
        panel = self.solution_panel(
            "ADD + SUBTRACT",
            [r"A_{\mathrm{rect}}=8(5)=40", r"A_{\triangle}=\frac{8(3)}{2}=12", r"A_{\mathrm{circle}}=\pi(1)^2=\pi", r"A_T=40+12-\pi"],
            r"A_T\approx48.86\ \mathrm{cm}^2", y=-.25, height=4.82,
        )
        self.play(FadeIn(panel), run_time=.7)
        self.wait(3.0)
        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.5)
        self.wipe()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V7_SENIOR.py Geometry8CompositeSimpleShadedAreasV7Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V7_SENIOR.py Geometry8CompositeSimpleShadedAreasV7Senior --disable_caching
