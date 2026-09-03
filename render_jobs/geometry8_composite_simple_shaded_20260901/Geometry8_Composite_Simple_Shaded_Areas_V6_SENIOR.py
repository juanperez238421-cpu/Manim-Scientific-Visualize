#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V6.

Senior micro-QA pass based on direct inspection of the delivered V5 MP4.
This revision targets residual projector-readability issues: small labels,
callout crowding, dimension-label spacing, and overlap risk in the square,
semicircle, hidden-dimension, decision-rule, house, error-summary and final
method scenes. Mathematics and instructional sequence remain unchanged.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V5_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV5Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, LIGHT, PAPER, FILL


class Geometry8CompositeSimpleShadedAreasV6Senior(
    Geometry8CompositeSimpleShadedAreasV5Senior
):
    """Projector-readability and micro-overlap precision pass."""

    def process_strip(self, active=0):
        labels = ["SEE", "DECOMPOSE", "+ / −", "CALCULATE", "CHECK"]
        strip = VGroup()
        for i, label in enumerate(labels):
            box = RoundedRectangle(
                width=1.93,
                height=.62,
                corner_radius=.08,
                stroke_color=INK if i == active else LIGHT,
                stroke_width=3.2 if i == active else 1.4,
                fill_color=PAPER if i == active else WHITE,
                fill_opacity=1,
            )
            text = self.txt(label, 23, True).move_to(box)
            if i != active:
                text.set_opacity(.38)
            strip.add(VGroup(box, text))
        strip.arrange(RIGHT, buff=.075)
        strip.to_edge(RIGHT, buff=.30).shift(UP * 2.48)
        return strip

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
        name_m = self.txt(name, 24, True)
        formula_m = self.eq(formula, 35)
        self.fit(name_m, 2.22, .42)
        self.fit(formula_m, 2.22, .56)
        VGroup(name_m, formula_m).arrange(DOWN, buff=.15).move_to(card)
        return VGroup(card, name_m, formula_m)

    def square_minus_quadrant(self):
        h = self.header(
            5,
            "SIMPLE SHADED AREA · SQUARE MINUS QUADRANT",
            "The white quadrant is removed. The gray corner outside the arc is the target area that remains.",
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
            r"8\ \mathrm{cm}", DOWN, 32,
        )
        radius = Line(corner, sq.get_corner(DR), color=INK, stroke_width=3)
        radius_label = self.eq(r"r=8\ \mathrm{cm}", 32).next_to(radius, UP, buff=.11).shift(LEFT*.44)

        self.play(Create(sq), run_time=.8)
        self.play(FadeIn(sector), FadeIn(VGroup(side_dim, radius, radius_label)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        removed = self.txt("REMOVED QUADRANT", 27, True)
        removed.move_to(corner+RIGHT*1.60+UP*.82)
        self.fit(removed, 3.00, .50)

        target_point = sq.get_corner(UR)+LEFT*.25+DOWN*.25
        target_panel = RoundedRectangle(
            width=3.45, height=.72, corner_radius=.10,
            stroke_color=INK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT*3.55+UP*1.30)
        target_text = self.txt("TARGET = GRAY CORNER", 27, True).move_to(target_panel)
        self.fit(target_text, 3.10, .48)
        target_arrow = Arrow(
            target_panel.get_left()+LEFT*.03,
            target_point,
            buff=.10,
            color=INK,
            stroke_width=2.6,
        )
        relation = self.txt("radius = square side = 8 cm", 28, True)
        relation.move_to(RIGHT*3.55+UP*.48)
        self.fit(relation, 5.9, .50)
        decomp = VGroup(target_panel, target_text, target_arrow, relation)
        self.play(FadeIn(removed), FadeIn(VGroup(target_panel, target_text)), GrowArrow(target_arrow), FadeIn(relation), run_time=.7)
        self.wait(.9)

        self.set_process(strip, 2)
        self.play(FadeOut(decomp), run_time=.30)
        rule = self.box(
            r"A_s=A_{\mathrm{square}}-A_{\mathrm{quadrant}}",
            6.18,
            45,
        ).move_to(RIGHT*3.62+UP*.78)
        radius_note = self.txt("8 cm is the radius here — not the diameter.", 28, True)
        radius_note.move_to(RIGHT*3.62+DOWN*.12)
        self.fit(radius_note, 5.95, .50)
        self.play(FadeIn(rule), FadeIn(radius_note), run_time=.6)
        self.wait(1.0)

        self.set_process(strip, 3)
        self.play(FadeOut(VGroup(rule, radius_note)), run_time=.30)
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
            self.dimension_line(rect.get_corner(DL)+DOWN*.22,rect.get_corner(DR)+DOWN*.22,r"10\ \mathrm{cm}",DOWN,31),
            self.dimension_line(rect.get_corner(DL)+LEFT*.22,rect.get_corner(UL)+LEFT*.22,r"6\ \mathrm{cm}",LEFT,31),
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
            r"d=10\ \mathrm{cm}\quad\Rightarrow\quad r=5\ \mathrm{cm}",
            6.05,
            43,
        ).move_to(RIGHT*3.58+UP*.92)
        self.play(Create(diameter), Create(radius), FadeIn(radius_step), run_time=.7)
        self.wait(1.1)

        self.set_process(strip, 2)
        self.play(FadeOut(radius_step), run_time=.28)
        structure = self.box(
            r"A_T=A_{\mathrm{rect}}+A_{\mathrm{semi}}",
            6.05,
            45,
        ).move_to(RIGHT*3.58+UP*.88)
        note_box = RoundedRectangle(
            width=6.05, height=1.02, corner_radius=.10,
            stroke_color=INK, stroke_width=1.7,
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

        x0, y0, sx, sy = -6.35, -1.85, .40, .40
        fill, outline = self._concave_l(x0, y0, sx, sy, 12, 8, 4, 3, opacity=.70)
        self.play(FadeIn(fill), Create(outline), run_time=.8)

        known = VGroup(
            self.dimension_line([x0,y0-.26,0],[x0+12*sx,y0-.26,0],r"12",DOWN,31),
            self.dimension_line([x0-.27,y0,0],[x0-.27,y0+8*sy,0],r"8",LEFT,31),
            self.dimension_line([x0+8*sx,y0+8*sy+.22,0],[x0+12*sx,y0+8*sy+.22,0],r"4",UP,31),
            self.dimension_line([x0+12*sx+.24,y0+5*sy,0],[x0+12*sx+.24,y0+8*sy,0],r"3",RIGHT,31),
        )
        self.play(FadeIn(known), run_time=.7)

        unknown_top = self.dimension_line(
            [x0,y0+8*sy+.58,0], [x0+8*sx,y0+8*sy+.58,0], r"x", UP, 34,
        )
        unknown_right = self.dimension_line(
            [x0+12*sx+.72,y0,0], [x0+12*sx+.72,y0+5*sy,0], r"y", RIGHT, 34,
        )
        question = VGroup(
            self.txt("STEP 1 · WRITE THE SEGMENT EQUATIONS", 30, True),
            self.txt("Total length = known piece + missing piece", 27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.11).move_to(RIGHT*3.50+UP*1.36)
        self.fit(question, 6.20, 1.02)
        self.play(FadeIn(VGroup(unknown_top, unknown_right, question)), run_time=.65)
        self.wait(1.5)

        equations = VGroup(
            self.eq(r"12=x+4", 44),
            self.eq(r"x=12-4=8", 44),
            self.eq(r"8=3+y", 44),
            self.eq(r"y=8-3=5", 44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.19).move_to(RIGHT*3.45+DOWN*.10)

        self.play(FadeIn(equations[0]), run_time=.5)
        self.wait(.55)
        self.play(FadeIn(equations[1]), run_time=.5)
        self.wait(.65)
        solved_top = self.dimension_line(
            [x0,y0+8*sy+.58,0], [x0+8*sx,y0+8*sy+.58,0], r"8", UP, 34,
        )
        self.play(Transform(unknown_top, solved_top), run_time=.55)
        self.wait(.55)

        self.play(FadeIn(equations[2]), run_time=.5)
        self.wait(.55)
        self.play(FadeIn(equations[3]), run_time=.5)
        self.wait(.65)
        solved_right = self.dimension_line(
            [x0+12*sx+.72,y0,0], [x0+12*sx+.72,y0+5*sy,0], r"5", RIGHT, 34,
        )
        self.play(Transform(unknown_right, solved_right), run_time=.55)

        rule = self.box(
            r"\text{Complete dimensions first}\;\longrightarrow\;\text{area second}",
            6.75,
            40,
        ).move_to(RIGHT*3.45+DOWN*2.12)
        self.play(FadeIn(rule), run_time=.6)
        self.wait(3.0)
        self.wipe()

    def decision_rule(self):
        h = self.header(
            8,
            "DECISION RULE · WHICH OPERATION SHOULD I USE?",
            "The drawing tells you whether to add, subtract, or do both.",
        )
        self.add(h)

        q = self.box(
            r"\text{What exactly is the target region?}",
            7.9,
            50,
        ).shift(UP * 1.82)
        self.play(FadeIn(q), run_time=.6)

        cards = VGroup()
        data = [
            ("ALL PIECES BELONG", "+", r"A_T=A_1+A_2+\cdots", "ADD"),
            ("A HOLE IS REMOVED", "-", r"A_T=A_{\mathrm{whole}}-A_{\mathrm{hole}}", "SUBTRACT"),
            ("PIECES + HOLES", r"+/-", r"A_T=\sum A_+-\sum A_-", "COMBINE"),
        ]
        for title, symbol, formula, action in data:
            box = RoundedRectangle(
                width=4.32,
                height=3.48,
                corner_radius=.13,
                stroke_color=INK,
                stroke_width=2,
                fill_color=WHITE,
                fill_opacity=1,
            )
            sy = self.eq(symbol, 47)
            t = self.txt(title, 27, True)
            f = self.eq(formula, 32)
            a = self.txt(action, 29, True)
            c = VGroup(t, sy, f, a).arrange(DOWN, buff=.21).move_to(box)
            self.fit(c, 3.90, 2.95)
            cards.add(VGroup(box, c))
        cards.arrange(RIGHT, buff=.28).shift(DOWN * .65)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.16),
            run_time=1.5,
        )
        self.wait(4.2)
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
            r"8\ \mathrm{cm}", DOWN, 31,
        )
        wall_dim = self.dimension_line(
            rect.get_corner(DL)+LEFT*.22,
            rect.get_corner(UL)+LEFT*.22,
            r"5\ \mathrm{cm}", LEFT, 31,
        )
        altitude = DashedLine(rect.get_top(), apex, color=MID, stroke_width=3)
        h_chip = RoundedRectangle(
            width=1.95, height=.58, corner_radius=.08,
            stroke_color=INK, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=.96,
        ).move_to(altitude.get_center()+RIGHT*.72)
        h_text = self.eq(r"h=3\ \mathrm{cm}", 28).move_to(h_chip)
        radius_line = Line(window.get_center(), window.get_left(), color=INK, stroke_width=3)
        r_text = self.eq(r"r=1\ \mathrm{cm}", 28).next_to(window, DOWN, buff=.12)

        self.play(Create(rect), Create(roof), Create(window), run_time=1.0)
        self.play(
            FadeIn(VGroup(base_dim, wall_dim)),
            Create(altitude), FadeIn(VGroup(h_chip, h_text)),
            Create(radius_line), FadeIn(r_text),
            run_time=.8,
        )

        prompt = VGroup(
            self.txt("YOUR TURN", 36, True),
            self.txt("Write the area expression before calculating.", 30),
            self.eq(r"A_T=\ ?", 52),
        ).arrange(DOWN, buff=.24).move_to(RIGHT*3.55+DOWN*.05)
        self.fit(prompt, 6.0, 2.45)
        self.play(FadeIn(prompt), run_time=.6)
        self.wait(5.0)

        self.set_process(strip, 1)
        self.play(FadeOut(prompt), run_time=.25)
        operation_panel = RoundedRectangle(
            width=5.75, height=2.75, corner_radius=.13,
            stroke_color=INK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT*3.55+DOWN*.18)
        op_title = self.txt("DECOMPOSE THE TARGET", 30, True)
        op_rows = VGroup(
            self.txt("1.  +  RECTANGLE", 29, True),
            self.txt("2.  +  TRIANGLE", 29, True),
            self.txt("3.  −  CIRCLE", 29, True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.19)
        op_content = VGroup(op_title, op_rows).arrange(DOWN, aligned_edge=LEFT, buff=.24).move_to(operation_panel)
        self.fit(op_content, 5.25, 2.25)
        self.play(FadeIn(VGroup(operation_panel, op_content)), run_time=.6)
        self.play(Circumscribe(rect, color=GRAY), run_time=.45)
        self.play(Circumscribe(roof, color=GRAY), run_time=.45)
        self.play(Circumscribe(window, color=GRAY), run_time=.45)
        self.wait(.7)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_{\mathrm{rect}}+A_{\triangle}-A_{\mathrm{circle}}",
            6.18,
            43,
        ).move_to(RIGHT*3.55+UP*.82)
        self.play(FadeOut(VGroup(operation_panel, op_content)), FadeIn(structure), run_time=.6)
        self.wait(.9)

        self.set_process(strip, 3)
        self.play(FadeOut(structure), run_time=.30)
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

    def common_errors(self):
        h = self.header(
            10,
            "COMMON ERRORS · CHECK THE GEOMETRY BEFORE THE ARITHMETIC",
            "Correct region choice and correct dimensions matter more than fast calculation.",
        )
        self.add(h)
        items = [
            ("ERROR 1 · WRONG REGION", "Subtract the HOLE — not the target."),
            ("ERROR 2 · RADIUS / DIAMETER", "Convert diameter to radius first."),
            ("ERROR 3 · HIDDEN LENGTHS", "Complete missing segments before area."),
            ("ERROR 4 · UNITS", "Area uses square units: cm², m², ..."),
        ]
        cards = VGroup()
        for title, text in items:
            box = RoundedRectangle(
                width=6.62,
                height=1.92,
                corner_radius=.12,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            title_m = self.txt(title, 29, True)
            text_m = self.txt(text, 29)
            self.fit(title_m, 6.00, .46)
            self.fit(text_m, 5.95, .60)
            VGroup(title_m, text_m).arrange(DOWN, buff=.16).move_to(box)
            cards.add(VGroup(box, title_m, text_m))
        cards.arrange_in_grid(rows=2, cols=2, buff=(.34, .34)).shift(DOWN*.20)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.12),
            run_time=1.5,
        )
        self.wait(4.8)
        self.wipe()

    def final_method_and_preview(self):
        h = self.header(
            11,
            "FINAL METHOD · SIMPLE COMPOSITE AND SHADED AREAS",
            "First decide the target region. Then use formulas to calculate its pieces.",
        )
        self.add(h)
        steps = [
            "1 · SEE THE TARGET",
            "2 · DECOMPOSE FIGURES",
            "3 · FIND MISSING LENGTHS",
            "4 · CHOOSE + OR −",
            "5 · WRITE ONE EXPRESSION",
            "6 · CALCULATE + CHECK cm²",
        ]
        cards = VGroup()
        for text in steps:
            box = RoundedRectangle(
                width=4.42,
                height=1.56,
                corner_radius=.11,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            text_m = self.txt(text, 29, True)
            self.fit(text_m, 4.00, .78)
            text_m.move_to(box)
            cards.add(VGroup(box, text_m))
        cards.arrange_in_grid(rows=2, cols=3, buff=(.30, .31)).shift(UP*.48)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.08),
            run_time=1.4,
        )
        self.wait(2.8)
        general = self.box(
            r"A_{\mathrm{target}}=\sum A_+-\sum A_-",
            7.55, 57,
        ).shift(DOWN*1.72)
        self.play(FadeIn(general), run_time=.6)
        self.wait(2.0)

        preview_box = RoundedRectangle(
            width=13.85, height=.82, corner_radius=.10,
            stroke_color=INK, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        ).to_edge(DOWN, buff=.16)
        preview = self.txt(
            "NEXT → COMPLEX SHADED AREAS · repeated pieces · several holes · symmetry · multiple strategies",
            30, True,
        ).move_to(preview_box)
        self.fit(preview, 13.30, .52)
        self.play(FadeIn(VGroup(preview_box, preview)), run_time=.6)
        self.wait(3.6)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V6_SENIOR.py Geometry8CompositeSimpleShadedAreasV6Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V6_SENIOR.py Geometry8CompositeSimpleShadedAreasV6Senior --disable_caching
