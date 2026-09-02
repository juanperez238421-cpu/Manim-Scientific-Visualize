#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V1.

Direct continuation of the accepted Figure-by-Figure V5 area atlas.

Pedagogical shift:
    individual area formulas -> combine known regions -> target area

Sequence:
    SEE -> DECOMPOSE -> CHOOSE + / - -> CALCULATE -> CHECK

Target:
    Manim Community Edition 0.20.1
    1920x1080, 30 fps, white-background JP classroom language
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from Geometry8_2D_Areas_FigureByFigure_V5_SENIOR import (
    Geometry8Areas2DFigureByFigureV5Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import (
    INK, MID, LIGHT, PAPER, FILL,
)


class Geometry8CompositeSimpleShadedAreasV1Senior(
    Geometry8Areas2DFigureByFigureV5Senior
):
    """Apply the V5 formula atlas to composite and simple shaded regions."""

    def validate_lesson_data(self):
        super().validate_lesson_data()
        assert 9 * 7 - 4 * 3 == 51
        assert 5 * 7 + 4 * 4 == 51
        rect_circle = 12 * 10 - math.pi * 3**2
        assert abs(rect_circle - 91.7256661177) < 1e-8
        square_quadrant = 8**2 - math.pi * 8**2 / 4
        assert abs(square_quadrant - 13.7345175426) < 1e-8
        door = 10 * 6 + 0.5 * math.pi * 5**2
        assert abs(door - 99.2699081699) < 1e-8
        house = 8 * 5 + 0.5 * 8 * 3 - math.pi
        assert abs(house - 48.8584073464) < 1e-8

    # ------------------------------------------------------------------
    # Shared lesson helpers
    # ------------------------------------------------------------------

    def process_strip(self, active=0):
        labels = ["SEE", "DECOMPOSE", "OPERATE", "CALCULATE", "CHECK"]
        strip = VGroup()
        for i, label in enumerate(labels):
            box = RoundedRectangle(
                width=1.75,
                height=.52,
                corner_radius=.08,
                stroke_color=INK if i == active else LIGHT,
                stroke_width=3 if i == active else 1.5,
                fill_color=PAPER if i == active else WHITE,
                fill_opacity=1,
            )
            text = self.txt(label, 19, True).move_to(box)
            if i != active:
                text.set_opacity(.45)
            strip.add(VGroup(box, text))
        strip.arrange(RIGHT, buff=.09)
        strip.to_edge(RIGHT, buff=.45).shift(UP * 2.56)
        return strip

    def set_process(self, strip, active):
        anims = []
        for i, item in enumerate(strip):
            box, text = item
            anims.append(
                box.animate
                .set_stroke(INK if i == active else LIGHT, width=3 if i == active else 1.5)
                .set_fill(PAPER if i == active else WHITE, opacity=1)
            )
            anims.append(text.animate.set_opacity(1 if i == active else .45))
        self.play(*anims, run_time=.28)

    def dimension_line(self, start, end, label, direction=DOWN, size=32):
        arr = DoubleArrow(
            start,
            end,
            buff=0,
            color=INK,
            stroke_width=2.0,
            tip_length=.16,
        )
        lab = self.eq(label, size).next_to(arr, direction, buff=.06)
        return VGroup(arr, lab)

    def solution_panel(
        self,
        title,
        lines,
        result,
        *,
        x=3.75,
        y=-.12,
        width=6.55,
        height=4.65,
    ):
        title_m = self.txt(title, 30, True)
        body = VGroup(*[self.eq(line, 37) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=.20
        )
        result_box = self.box(result, width - .40, 47)
        check = self.txt("CHECK → square units", 24, True)
        content = VGroup(title_m, body, result_box, check).arrange(
            DOWN, aligned_edge=LEFT, buff=.22
        )
        self.fit(content, width - .55, height - .55)
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=.14,
            stroke_color=INK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * .30)
        return VGroup(panel, content).move_to(RIGHT * x + UP * y)

    def operation_badge(self, symbol, word):
        circle = Circle(
            radius=.48,
            stroke_color=INK,
            stroke_width=3,
            fill_color=PAPER,
            fill_opacity=1,
        )
        sym = self.eq(symbol, 42).move_to(circle)
        label = self.txt(word, 24, True).next_to(circle, DOWN, buff=.10)
        return VGroup(circle, sym, label)

    def mini_formula_card(self, name, formula):
        r = RoundedRectangle(
            width=2.25,
            height=1.45,
            corner_radius=.10,
            stroke_color=INK,
            stroke_width=1.8,
            fill_color=PAPER,
            fill_opacity=1,
        )
        n = self.txt(name, 20, True)
        f = self.eq(formula, 30)
        c = VGroup(n, f).arrange(DOWN, buff=.13).move_to(r)
        return VGroup(r, c)

    # ------------------------------------------------------------------
    # Master timeline
    # ------------------------------------------------------------------

    def construct(self):
        self.opening()
        self.bridge_from_v5()
        self.add_subtract_language()
        self.l_shape_two_methods()
        self.rectangle_minus_circle()
        self.square_minus_quadrant()
        self.rectangle_plus_semicircle()
        self.hidden_dimensions()
        self.decision_rule()
        self.guided_challenge()
        self.common_errors()
        self.final_method_and_preview()

    # ------------------------------------------------------------------
    # 00 — Opening
    # ------------------------------------------------------------------

    def opening(self):
        title = VGroup(
            self.txt("GEOMETRY 8 · AREA OF 2D FIGURES", 46, True),
            self.txt("COMPOSITE FIGURES + SIMPLE SHADED AREAS", 56, True),
            self.txt(
                "Use the formulas you already derived to build the area you actually need.",
                30,
            ),
        ).arrange(DOWN, buff=.18).shift(UP * 1.62)
        self.fit(title, 14.5, 2.0)

        left = VGroup(
            Square(1.05, color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.75),
            Circle(.52, color=INK, stroke_width=4, fill_color=WHITE, fill_opacity=1),
        )
        left[1].move_to(left[0])

        plus = self.operation_badge("+", "ADD PIECES")
        minus = self.operation_badge("-", "REMOVE HOLES")
        arrow = Arrow(LEFT * 1.0, RIGHT * 1.0, color=INK, stroke_width=3)

        target = VGroup(
            Rectangle(
                width=2.05,
                height=1.35,
                color=INK,
                stroke_width=4,
                fill_color=FILL,
                fill_opacity=.75,
            ),
            Circle(
                .38,
                color=INK,
                stroke_width=4,
                fill_color=WHITE,
                fill_opacity=1,
            ),
        )
        target[1].move_to(target[0])

        row = VGroup(left, plus, minus, arrow, target).arrange(RIGHT, buff=.48)
        row.shift(DOWN * .45)

        motto = self.txt(
            "SEE → DECOMPOSE → CHOOSE + / − → CALCULATE → CHECK",
            35,
            True,
        ).shift(DOWN * 2.30)
        self.fit(motto, 14.2, .7)

        self.play(Write(title[0]), run_time=.7)
        self.play(Write(title[1]), FadeIn(title[2]), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * .05) for x in row], lag_ratio=.10), run_time=1.4)
        self.play(FadeIn(motto), run_time=.6)
        self.wait(3.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 01 — Bridge from the accepted V5 atlas
    # ------------------------------------------------------------------

    def bridge_from_v5(self):
        h = self.header(
            1,
            "FROM INDIVIDUAL FIGURES TO TARGET REGIONS",
            "The formulas from the V5 atlas are now tools. The new skill is deciding how the regions combine.",
        )
        self.add(h)

        cards = VGroup(
            self.mini_formula_card("RECTANGLE", r"A=bh"),
            self.mini_formula_card("TRIANGLE", r"A=\frac{bh}{2}"),
            self.mini_formula_card("CIRCLE", r"A=\pi r^2"),
            self.mini_formula_card("SEMICIRCLE", r"A=\frac{\pi r^2}{2}"),
            self.mini_formula_card("QUADRANT", r"A=\frac{\pi r^2}{4}"),
        ).arrange(RIGHT, buff=.18).shift(UP * .45)

        add = self.operation_badge("+", "COMBINE")
        sub = self.operation_badge("-", "REMOVE")
        ops = VGroup(add, sub).arrange(RIGHT, buff=1.0).shift(DOWN * 1.45)

        eq = self.box(
            r"A_{\mathrm{target}}=\sum A_{\mathrm{added}}-\sum A_{\mathrm{removed}}",
            10.3,
            52,
        ).shift(DOWN * 2.75)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * .05) for c in cards], lag_ratio=.08),
            run_time=1.3,
        )
        self.wait(1.2)
        self.play(FadeIn(ops), run_time=.7)
        self.wait(1.2)
        self.play(FadeIn(eq), run_time=.7)
        self.wait(3.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 02 — Visual language of addition and subtraction
    # ------------------------------------------------------------------

    def add_subtract_language(self):
        h = self.header(
            2,
            "THE THREE REGION OPERATIONS",
            "Name the target region before touching the calculator.",
        )
        self.add(h)

        r1 = Rectangle(
            width=2.2, height=1.5, color=INK, stroke_width=4,
            fill_color=FILL, fill_opacity=.68,
        )
        t1 = Polygon(
            [-1.1, .75, 0], [1.1, .75, 0], [0, 1.85, 0],
            color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.68,
        )
        add_shape = VGroup(r1, t1).scale(.78)
        add_formula = self.eq(r"A_T=A_1+A_2", 38)

        r2 = Rectangle(
            width=2.2, height=1.7, color=INK, stroke_width=4,
            fill_color=FILL, fill_opacity=.68,
        )
        hole = Circle(.48, color=INK, stroke_width=4, fill_color=WHITE, fill_opacity=1)
        sub_shape = VGroup(r2, hole).scale(.78)
        sub_formula = self.eq(r"A_T=A_{\mathrm{whole}}-A_{\mathrm{hole}}", 32)

        r3 = Rectangle(
            width=2.2, height=1.45, color=INK, stroke_width=4,
            fill_color=FILL, fill_opacity=.68,
        )
        roof = Polygon(
            [-1.1, .72, 0], [1.1, .72, 0], [0, 1.75, 0],
            color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.68,
        )
        win = Circle(.34, color=INK, stroke_width=4, fill_color=WHITE, fill_opacity=1).shift(UP * .25)
        mixed_shape = VGroup(r3, roof, win).scale(.78)
        mixed_formula = self.eq(r"A_T=(A_1+A_2)-A_3", 34)

        groups = []
        for title, shape, formula in [
            ("ADD", add_shape, add_formula),
            ("SUBTRACT", sub_shape, sub_formula),
            ("ADD + SUBTRACT", mixed_shape, mixed_formula),
        ]:
            box = RoundedRectangle(
                width=4.35,
                height=4.45,
                corner_radius=.14,
                stroke_color=INK,
                stroke_width=2,
                fill_color=WHITE,
                fill_opacity=1,
            )
            ti = self.txt(title, 30, True)
            content = VGroup(ti, shape, formula).arrange(DOWN, buff=.32).move_to(box)
            self.fit(content, 3.85, 3.85)
            groups.append(VGroup(box, content))
        cards = VGroup(*groups).arrange(RIGHT, buff=.28).shift(DOWN * .33)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * .05) for c in cards], lag_ratio=.16),
            run_time=1.6,
        )
        self.wait(4.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 03 — L shape: one region, two valid decompositions
    # ------------------------------------------------------------------

    def l_shape_two_methods(self):
        h = self.header(
            3,
            "COMPOSITE FIGURE · ONE REGION, TWO VALID METHODS",
            "A correct decomposition preserves the same target area.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        x0, y0 = -6.0, -2.0
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
            [x0, y0 - .28, 0],
            [x0 + 9*sx, y0 - .28, 0],
            r"9",
            DOWN,
        )
        total_h = self.dimension_line(
            [x0 - .28, y0, 0],
            [x0 - .28, y0 + 7*sy, 0],
            r"7",
            LEFT,
        )
        notch_w = self.dimension_line(
            [x0 + 5*sx, y0 + 7*sy + .22, 0],
            [x0 + 9*sx, y0 + 7*sy + .22, 0],
            r"4",
            UP,
        )
        notch_h = self.dimension_line(
            [x0 + 9*sx + .22, y0 + 4*sy, 0],
            [x0 + 9*sx + .22, y0 + 7*sy, 0],
            r"3",
            RIGHT,
        )

        self.play(Create(L), run_time=.9)
        self.play(FadeIn(VGroup(total_w, total_h, notch_w, notch_h)), run_time=.8)
        self.wait(1.0)

        self.set_process(strip, 1)
        missing = Rectangle(
            width=4*sx,
            height=3*sy,
            color=INK,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        missing.move_to([x0 + 7*sx, y0 + 5.5*sy, 0])
        self.play(FadeIn(missing), run_time=.6)
        self.wait(.8)

        self.set_process(strip, 2)
        method_a = self.solution_panel(
            "METHOD A · WHOLE − MISSING",
            [
                r"A_{\mathrm{whole}}=9(7)=63",
                r"A_{\mathrm{missing}}=4(3)=12",
                r"A_T=63-12",
            ],
            r"A_T=51\ \mathrm{cm}^2",
        )
        self.play(FadeIn(method_a), run_time=.7)
        self.wait(2.0)

        self.set_process(strip, 3)
        split = DashedLine(
            [x0 + 5*sx, y0, 0],
            [x0 + 5*sx, y0 + 4*sy, 0],
            color=MID,
            stroke_width=3,
        )
        self.play(FadeOut(missing), Create(split), run_time=.6)
        alt = VGroup(
            self.eq(r"A_1=5(7)=35", 35),
            self.eq(r"A_2=4(4)=16", 35),
            self.box(r"35+16=51", 4.7, 42),
        ).arrange(DOWN, buff=.17).move_to(RIGHT * 3.8 + DOWN * 1.28)
        self.play(FadeOut(method_a), FadeIn(alt), run_time=.65)
        self.wait(2.0)

        self.set_process(strip, 4)
        check = self.txt(
            "Two decompositions → same area → geometry is consistent.",
            29,
            True,
        ).move_to(RIGHT * 3.6 + UP * 1.60)
        self.fit(check, 6.3, .65)
        self.play(FadeIn(check), run_time=.5)
        self.wait(3.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 04 — Rectangle minus circle
    # ------------------------------------------------------------------

    def rectangle_minus_circle(self):
        h = self.header(
            4,
            "SIMPLE SHADED AREA · RECTANGLE MINUS CIRCULAR HOLE",
            "Keep the whole region visible, then remove exactly the part you do not want.",
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

        w = self.dimension_line(
            rect.get_corner(DL) + DOWN*.25,
            rect.get_corner(DR) + DOWN*.25,
            r"12\ \mathrm{cm}",
            DOWN,
            30,
        )
        hh = self.dimension_line(
            rect.get_corner(DL) + LEFT*.25,
            rect.get_corner(UL) + LEFT*.25,
            r"10\ \mathrm{cm}",
            LEFT,
            30,
        )
        rad = Line(circle.get_center(), circle.get_right(), color=INK, stroke_width=3)
        rlab = self.eq(r"r=3\ \mathrm{cm}", 30).next_to(rad, UP, buff=.08)

        self.play(Create(rect), run_time=.8)
        self.play(Create(circle), FadeIn(VGroup(w, hh, rad, rlab)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        ghost = circle.copy().set_fill(PAPER, opacity=1)
        self.play(TransformFromCopy(circle, ghost), run_time=.5)
        self.play(ghost.animate.shift(RIGHT * 2.0 + UP * .15), run_time=.65)

        self.set_process(strip, 2)
        minus = self.eq("-", 56).next_to(ghost, LEFT, buff=.22)
        self.play(FadeIn(minus), run_time=.4)
        self.wait(.7)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "WHOLE − HOLE",
            [
                r"A_R=12(10)=120",
                r"A_C=\pi(3)^2=9\pi",
                r"A_s=120-9\pi",
            ],
            r"A_s\approx91.73\ \mathrm{cm}^2",
        )
        self.play(FadeOut(VGroup(ghost, minus)), FadeIn(panel), run_time=.7)
        self.wait(2.7)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.2)
        self.wipe()

    # ------------------------------------------------------------------
    # 05 — Square minus quadrant
    # ------------------------------------------------------------------

    def square_minus_quadrant(self):
        h = self.header(
            5,
            "SIMPLE SHADED AREA · SQUARE MINUS QUADRANT",
            "A quadrant is one fourth of a full circle, not one fourth of the square.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        side = 4.45
        sq = Square(
            side_length=side,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.80,
        ).move_to(LEFT * 3.70 + DOWN * .12)
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

        base = self.dimension_line(
            sq.get_corner(DL) + DOWN*.22,
            sq.get_corner(DR) + DOWN*.22,
            r"8\ \mathrm{cm}",
            DOWN,
            30,
        )
        radius = Line(corner, sq.get_corner(DR), color=INK, stroke_width=3)
        rlab = self.eq(r"r=8\ \mathrm{cm}", 30).next_to(radius, UP, buff=.08)

        self.play(Create(sq), run_time=.8)
        self.play(FadeIn(sector), FadeIn(VGroup(base, radius, rlab)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        label = self.txt(
            "WHITE = 1/4 of a circle",
            28,
            True,
        ).move_to(LEFT * 3.75 + UP * 2.0)
        self.play(FadeIn(label), run_time=.5)

        self.set_process(strip, 2)
        eq_rule = self.box(
            r"A_s=A_{\square}-A_{\mathrm{quadrant}}",
            6.0,
            43,
        ).move_to(RIGHT * 3.75 + UP * 1.70)
        self.play(FadeIn(eq_rule), run_time=.6)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "SQUARE − QUADRANT",
            [
                r"A_{\square}=8^2=64",
                r"A_Q=\frac{\pi(8)^2}{4}=16\pi",
                r"A_s=64-16\pi",
            ],
            r"A_s\approx13.73\ \mathrm{cm}^2",
        )
        panel.shift(DOWN * .42)
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.8)

        self.set_process(strip, 4)
        wrong = self.txt(
            "Do not use 8 as a diameter: here 8 cm is the radius.",
            25,
            True,
        ).move_to(RIGHT * 3.7 + DOWN * 2.63)
        self.fit(wrong, 6.2, .6)
        self.play(FadeIn(wrong), run_time=.5)
        self.wait(2.6)
        self.wipe()

    # ------------------------------------------------------------------
    # 06 — Rectangle plus semicircle
    # ------------------------------------------------------------------

    def rectangle_plus_semicircle(self):
        h = self.header(
            6,
            "COMPOSITE ADDITION · RECTANGLE PLUS SEMICIRCLE",
            "When all pieces belong to the target, add their areas.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        rect_w, rect_h = 5.0, 2.75
        center = np.array([-3.65, -1.05, 0.0])
        rect = Rectangle(
            width=rect_w,
            height=rect_h,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.72,
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

        w = self.dimension_line(
            rect.get_corner(DL)+DOWN*.22,
            rect.get_corner(DR)+DOWN*.22,
            r"10\ \mathrm{cm}",
            DOWN,
            29,
        )
        hh = self.dimension_line(
            rect.get_corner(DL)+LEFT*.22,
            rect.get_corner(UL)+LEFT*.22,
            r"6\ \mathrm{cm}",
            LEFT,
            29,
        )

        self.play(Create(rect), FadeIn(VGroup(w, hh)), run_time=.8)
        self.play(Create(semi), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        diam = Line(
            top_mid + LEFT*(rect_w/2),
            top_mid + RIGHT*(rect_w/2),
            color=MID,
            stroke_width=3,
        )
        rline = Line(top_mid, top_mid + RIGHT*(rect_w/2), color=INK, stroke_width=3)
        rlab = self.eq(r"r=\frac{10}{2}=5", 32).next_to(rline, UP, buff=.07)
        self.play(Create(diam), Create(rline), FadeIn(rlab), run_time=.7)

        self.set_process(strip, 2)
        plus = self.eq("+", 56).move_to(RIGHT * .15 + DOWN * .10)
        parts = VGroup(
            self.txt("rectangle", 26, True),
            self.txt("semicircle", 26, True),
        ).arrange(DOWN, buff=.15).move_to(RIGHT * 1.05 + DOWN * .10)
        self.play(FadeIn(plus), FadeIn(parts), run_time=.5)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "ADD BOTH TARGET PIECES",
            [
                r"A_R=10(6)=60",
                r"A_S=\frac{\pi(5)^2}{2}=\frac{25\pi}{2}",
                r"A_T=60+\frac{25\pi}{2}",
            ],
            r"A_T\approx99.27\ \mathrm{cm}^2",
        )
        self.play(FadeOut(VGroup(plus, parts)), FadeIn(panel), run_time=.7)
        self.wait(2.8)

        self.set_process(strip, 4)
        note = self.txt(
            "The shared diameter is inside the composite figure; it is not removed.",
            25,
            True,
        ).move_to(RIGHT * 3.75 + DOWN * 2.62)
        self.fit(note, 6.15, .6)
        self.play(FadeIn(note), run_time=.5)
        self.wait(2.5)
        self.wipe()

    # ------------------------------------------------------------------
    # 07 — Hidden dimensions before arithmetic
    # ------------------------------------------------------------------

    def hidden_dimensions(self):
        h = self.header(
            7,
            "BEFORE CALCULATING · COMPLETE THE MISSING DIMENSIONS",
            "Composite figures often hide lengths that must be deduced from the outer dimensions.",
        )
        self.add(h)

        x0, y0 = -5.9, -1.9
        sx, sy = .44, .44
        pts = [
            [x0, y0, 0],
            [x0+12*sx, y0, 0],
            [x0+12*sx, y0+5*sy, 0],
            [x0+8*sx, y0+5*sy, 0],
            [x0+8*sx, y0+8*sy, 0],
            [x0, y0+8*sy, 0],
        ]
        L = Polygon(*pts, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.70)
        self.play(Create(L), run_time=.8)

        dims = VGroup(
            self.dimension_line([x0, y0-.25,0],[x0+12*sx,y0-.25,0],r"12",DOWN,29),
            self.dimension_line([x0-.25,y0,0],[x0-.25,y0+8*sy,0],r"8",LEFT,29),
            self.dimension_line([x0+8*sx,y0+8*sy+.20,0],[x0+12*sx,y0+8*sy+.20,0],r"4",UP,29),
            self.dimension_line([x0+12*sx+.20,y0+5*sy,0],[x0+12*sx+.20,y0+8*sy,0],r"3",RIGHT,29),
        )
        self.play(FadeIn(dims), run_time=.7)

        q = self.txt(
            "What are the two hidden lengths?",
            31,
            True,
        ).move_to(RIGHT * 3.60 + UP * 1.45)
        self.play(FadeIn(q), run_time=.5)
        self.wait(2.2)

        calc = VGroup(
            self.eq(r"12-4=8", 46),
            self.eq(r"8-3=5", 46),
        ).arrange(DOWN, buff=.35).move_to(RIGHT * 3.60 + DOWN * .05)
        self.play(FadeIn(calc[0]), run_time=.55)
        self.wait(.7)
        self.play(FadeIn(calc[1]), run_time=.55)
        self.wait(.8)

        labels = VGroup(
            self.eq(r"8", 34).move_to([x0+4*sx, y0+5*sy+.10,0]),
            self.eq(r"5", 34).move_to([x0+8*sx+.15, y0+2.5*sy,0]),
        )
        self.play(FadeIn(labels), run_time=.6)

        rule = self.box(
            r"\text{Complete dimensions first}\;\rightarrow\;\text{area second}",
            7.1,
            40,
        ).move_to(RIGHT * 3.60 + DOWN * 1.80)
        self.play(FadeIn(rule), run_time=.6)
        self.wait(3.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 08 — Decision rule / algorithm
    # ------------------------------------------------------------------

    def decision_rule(self):
        h = self.header(
            8,
            "DECISION RULE · WHICH OPERATION SHOULD I USE?",
            "The drawing tells you whether to add, subtract, or do both.",
        )
        self.add(h)

        q = self.box(
            r"\text{What exactly is the target region?}",
            7.8,
            48,
        ).shift(UP * 1.80)
        self.play(FadeIn(q), run_time=.6)

        cards = VGroup()
        data = [
            (
                "ALL PIECES BELONG",
                "+",
                r"A_T=A_1+A_2+\cdots",
                "ADD",
            ),
            (
                "A HOLE IS REMOVED",
                "-",
                r"A_T=A_{\mathrm{whole}}-A_{\mathrm{hole}}",
                "SUBTRACT",
            ),
            (
                "PIECES + HOLES",
                r"+/-",
                r"A_T=\sum A_+-\sum A_-",
                "COMBINE",
            ),
        ]
        for title, symbol, formula, action in data:
            r = RoundedRectangle(
                width=4.25,
                height=3.35,
                corner_radius=.13,
                stroke_color=INK,
                stroke_width=2,
                fill_color=WHITE,
                fill_opacity=1,
            )
            sy = self.eq(symbol, 44)
            t = self.txt(title, 25, True)
            f = self.eq(formula, 29)
            a = self.txt(action, 27, True)
            c = VGroup(t, sy, f, a).arrange(DOWN, buff=.20).move_to(r)
            self.fit(c, 3.75, 2.80)
            cards.add(VGroup(r, c))
        cards.arrange(RIGHT, buff=.30).shift(DOWN * .65)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.16),
            run_time=1.5,
        )
        self.wait(4.0)
        self.wipe()

    # ------------------------------------------------------------------
    # 09 — Guided challenge: add + subtract
    # ------------------------------------------------------------------

    def guided_challenge(self):
        h = self.header(
            9,
            "GUIDED CHALLENGE · HOUSE WITH A CIRCULAR WINDOW",
            "Build the total first, then remove the window. Pause before the reveal.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        rect_w, rect_h = 4.65, 2.90
        base_center = np.array([-3.75, -1.05, 0.0])
        rect = Rectangle(
            width=rect_w,
            height=rect_h,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.74,
        ).move_to(base_center)
        roof = Polygon(
            rect.get_corner(UL),
            rect.get_corner(UR),
            rect.get_top() + UP * 1.75,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.74,
        )
        window = Circle(
            radius=.55,
            color=INK,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(rect.get_center() + UP * .25)

        dims = VGroup(
            self.dimension_line(
                rect.get_corner(DL)+DOWN*.22,
                rect.get_corner(DR)+DOWN*.22,
                r"8\ \mathrm{cm}",
                DOWN,
                29,
            ),
            self.dimension_line(
                rect.get_corner(DL)+LEFT*.22,
                rect.get_corner(UL)+LEFT*.22,
                r"5\ \mathrm{cm}",
                LEFT,
                29,
            ),
            self.eq(r"h_{\triangle}=3\ \mathrm{cm}", 28).next_to(roof, LEFT, buff=.18),
            self.eq(r"r_w=1\ \mathrm{cm}", 28).next_to(window, RIGHT, buff=.15),
        )

        self.play(Create(rect), Create(roof), Create(window), run_time=1.0)
        self.play(FadeIn(dims), run_time=.7)

        prompt = VGroup(
            self.txt("YOUR TURN", 32, True),
            self.txt("Write the area expression before calculating.", 28),
            self.eq(r"A_T=\ ? ", 48),
        ).arrange(DOWN, buff=.22).move_to(RIGHT * 3.55 + DOWN * .10)
        self.fit(prompt, 6.0, 2.3)
        self.play(FadeIn(prompt), run_time=.6)
        self.wait(5.5)

        self.set_process(strip, 1)
        labels = VGroup(
            self.txt("RECTANGLE", 23, True).move_to(rect.get_center()+DOWN*.70),
            self.txt("TRIANGLE", 23, True).move_to(roof.get_center()+UP*.12),
            self.txt("REMOVE", 21, True).next_to(window, DOWN, buff=.08),
        )
        self.play(FadeIn(labels), run_time=.6)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_R+A_{\triangle}-A_C",
            6.1,
            46,
        ).move_to(RIGHT * 3.55 + UP * 1.30)
        self.play(FadeOut(prompt), FadeIn(structure), run_time=.6)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "ADD + SUBTRACT",
            [
                r"A_R=8(5)=40",
                r"A_{\triangle}=\frac{8(3)}{2}=12",
                r"A_C=\pi(1)^2=\pi",
                r"A_T=40+12-\pi",
            ],
            r"A_T\approx48.86\ \mathrm{cm}^2",
            height=4.90,
        )
        panel.shift(DOWN * .45)
        self.play(FadeIn(panel), run_time=.7)
        self.wait(3.0)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.4)
        self.wipe()

    # ------------------------------------------------------------------
    # 10 — Common errors
    # ------------------------------------------------------------------

    def common_errors(self):
        h = self.header(
            10,
            "COMMON ERRORS · CHECK THE GEOMETRY BEFORE THE ARITHMETIC",
            "Most shaded-area mistakes come from choosing the wrong region or dimension.",
        )
        self.add(h)

        items = [
            ("ERROR 1", "Subtracting the shaded region instead of the missing region."),
            ("ERROR 2", "Using diameter where the circle formula needs radius."),
            ("ERROR 3", "Calculating before completing hidden dimensions."),
            ("ERROR 4", "Reporting cm or m instead of cm² or m²."),
        ]
        cards = VGroup()
        for n, text in items:
            r = RoundedRectangle(
                width=6.45,
                height=1.55,
                corner_radius=.12,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            a = self.txt(n, 24, True)
            b = self.txt(text, 25)
            self.fit(b, 5.65, .72)
            c = VGroup(a, b).arrange(DOWN, buff=.10).move_to(r)
            cards.add(VGroup(r, c))
        cards.arrange_in_grid(rows=2, cols=2, buff=(.30, .30)).shift(DOWN * .20)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.12),
            run_time=1.5,
        )
        self.wait(4.5)
        self.wipe()

    # ------------------------------------------------------------------
    # 11 — Final method + preview of the next lesson
    # ------------------------------------------------------------------

    def final_method_and_preview(self):
        h = self.header(
            11,
            "FINAL METHOD · SIMPLE COMPOSITE AND SHADED AREAS",
            "The target region determines the operation. The formulas only calculate the pieces.",
        )
        self.add(h)

        steps = [
            "1 · SEE THE TARGET REGION",
            "2 · DECOMPOSE INTO KNOWN FIGURES",
            "3 · COMPLETE MISSING DIMENSIONS",
            "4 · CHOOSE + OR −",
            "5 · WRITE THE FULL EXPRESSION",
            "6 · CALCULATE + CHECK SQUARE UNITS",
        ]
        cards = VGroup()
        for text in steps:
            r = RoundedRectangle(
                width=4.25,
                height=1.28,
                corner_radius=.11,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            t = self.txt(text, 25, True)
            self.fit(t, 3.82, .72)
            t.move_to(r)
            cards.add(VGroup(r, t))
        cards.arrange_in_grid(rows=2, cols=3, buff=(.30, .28)).shift(UP * .35)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.08),
            run_time=1.4,
        )
        self.wait(2.7)

        general = self.box(
            r"A_{\mathrm{target}}=\sum A_+-\sum A_-",
            7.1,
            52,
        ).shift(DOWN * 1.75)
        self.play(FadeIn(general), run_time=.6)
        self.wait(2.0)

        preview = self.txt(
            "NEXT → COMPLEX SHADED AREAS: repeated pieces, several holes, symmetry, and multiple strategies.",
            28,
            True,
        ).to_edge(DOWN, buff=.28)
        self.fit(preview, 14.2, .72)
        self.play(FadeIn(preview), run_time=.6)
        self.wait(3.5)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V1_SENIOR.py Geometry8CompositeSimpleShadedAreasV1Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V1_SENIOR.py Geometry8CompositeSimpleShadedAreasV1Senior --disable_caching
