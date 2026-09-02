#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Composite Figures + Simple Shaded Areas — Senior V2.

Frame-by-frame QA revision of V1.  The mathematics is preserved while the
geometry, labels, typography, and projection readability are corrected.
Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Composite_Simple_Shaded_Areas_V1_SENIOR import (
    Geometry8CompositeSimpleShadedAreasV1Senior,
)
from Geometry8_2D_Areas_Masterclass_FINAL_QA import INK, MID, LIGHT, PAPER, FILL


class Geometry8CompositeSimpleShadedAreasV2Senior(
    Geometry8CompositeSimpleShadedAreasV1Senior
):
    """Projector-first Senior QA revision of the composite-area lesson."""

    # ------------------------------------------------------------------
    # Shared visual upgrades
    # ------------------------------------------------------------------

    def process_strip(self, active=0):
        labels = ["SEE", "DECOMPOSE", "OPERATE", "CALCULATE", "CHECK"]
        strip = VGroup()
        for i, label in enumerate(labels):
            box = RoundedRectangle(
                width=1.90,
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

    def set_process(self, strip, active):
        anims = []
        for i, item in enumerate(strip):
            box, text = item
            anims.extend([
                box.animate.set_stroke(
                    INK if i == active else LIGHT,
                    width=3.2 if i == active else 1.4,
                ).set_fill(PAPER if i == active else WHITE, opacity=1),
                text.animate.set_opacity(1 if i == active else .38),
            ])
        self.play(*anims, run_time=.30)

    def mini_formula_card(self, name, formula):
        card = RoundedRectangle(
            width=2.52,
            height=1.58,
            corner_radius=.10,
            stroke_color=INK,
            stroke_width=1.9,
            fill_color=PAPER,
            fill_opacity=1,
        )
        name_m = self.txt(name, 22, True)
        formula_m = self.eq(formula, 33)
        self.fit(name_m, 2.18, .38)
        self.fit(formula_m, 2.18, .52)
        VGroup(name_m, formula_m).arrange(DOWN, buff=.15).move_to(card)
        return VGroup(card, name_m, formula_m)

    def solution_panel(
        self,
        title,
        lines,
        result,
        *,
        x=3.72,
        y=-.18,
        width=6.55,
        height=4.82,
    ):
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=.14,
            stroke_color=INK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        title_m = self.txt(title, 31, True)
        self.fit(title_m, width-.62, .48)

        body = VGroup()
        for line in lines:
            m = self.eq(line, 40)
            self.fit(m, width-.78, .58)
            body.add(m)
        body.arrange(DOWN, aligned_edge=LEFT, buff=.16)

        result_box = self.box(result, width-.55, 49)
        self.fit(result_box, width-.42, .88)
        check = self.txt("CHECK → area uses square units", 26, True)
        self.fit(check, width-.72, .42)

        content = VGroup(title_m, body, result_box, check).arrange(
            DOWN, aligned_edge=LEFT, buff=.19
        )
        self.fit(content, width-.58, height-.52)
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*.30)
        return VGroup(panel, content).move_to(RIGHT*x + UP*y)

    def _concave_l(self, x0, y0, sx, sy, W, H, cut_w, cut_h, opacity=.72):
        """Stable concave L: independent fill rectangles + unfilled outer outline."""
        left_w = W-cut_w
        lower_h = H-cut_h
        fill_left = Rectangle(
            width=left_w*sx,
            height=H*sy,
            stroke_width=0,
            fill_color=FILL,
            fill_opacity=opacity,
        ).move_to([x0+left_w*sx/2, y0+H*sy/2, 0])
        fill_right = Rectangle(
            width=cut_w*sx,
            height=lower_h*sy,
            stroke_width=0,
            fill_color=FILL,
            fill_opacity=opacity,
        ).move_to([x0+(left_w+cut_w/2)*sx, y0+lower_h*sy/2, 0])
        pts = [
            [x0, y0, 0],
            [x0+W*sx, y0, 0],
            [x0+W*sx, y0+lower_h*sy, 0],
            [x0+left_w*sx, y0+lower_h*sy, 0],
            [x0+left_w*sx, y0+H*sy, 0],
            [x0, y0+H*sy, 0],
        ]
        outline = Polygon(*pts, color=INK, stroke_width=5, fill_opacity=0)
        return VGroup(fill_left, fill_right), outline

    # ------------------------------------------------------------------
    # L-shape: remove concave-fill artifacts and label both decompositions
    # ------------------------------------------------------------------

    def l_shape_two_methods(self):
        h = self.header(
            3,
            "COMPOSITE FIGURE · ONE REGION, TWO VALID METHODS",
            "Different correct decompositions must produce the same target area.",
        )
        self.add(h)
        strip = self.process_strip(0)
        self.add(strip)

        x0, y0, sx, sy = -6.0, -2.0, .55, .55
        fill, outline = self._concave_l(x0, y0, sx, sy, 9, 7, 4, 3)
        dims = VGroup(
            self.dimension_line([x0,y0-.28,0],[x0+9*sx,y0-.28,0],r"9",DOWN),
            self.dimension_line([x0-.28,y0,0],[x0-.28,y0+7*sy,0],r"7",LEFT),
            self.dimension_line([x0+5*sx,y0+7*sy+.22,0],[x0+9*sx,y0+7*sy+.22,0],r"4",UP),
            self.dimension_line([x0+9*sx+.22,y0+4*sy,0],[x0+9*sx+.22,y0+7*sy,0],r"3",RIGHT),
        )
        self.play(FadeIn(fill), Create(outline), run_time=.9)
        self.play(FadeIn(dims), run_time=.8)
        self.wait(1.0)

        self.set_process(strip, 1)
        missing = Rectangle(
            width=4*sx, height=3*sy,
            color=INK, stroke_width=4,
            fill_color=PAPER, fill_opacity=1,
        ).move_to([x0+7*sx, y0+5.5*sy, 0])
        miss_lab = self.txt("MISSING 4 × 3", 24, True).move_to(missing)
        self.fit(miss_lab, 1.8, .55)
        self.play(FadeIn(missing), FadeIn(miss_lab), run_time=.6)
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
            [x0+5*sx,y0,0], [x0+5*sx,y0+4*sy,0],
            color=MID, stroke_width=3,
        )
        labels = VGroup(
            self.txt("5 × 7", 26, True).move_to([x0+2.5*sx,y0+3.4*sy,0]),
            self.txt("4 × 4", 26, True).move_to([x0+7*sx,y0+2.0*sy,0]),
        )
        self.play(
            FadeOut(VGroup(missing, miss_lab, method_a)),
            Create(split), FadeIn(labels), run_time=.7,
        )
        alt = VGroup(
            self.eq(r"A_1=5(7)=35", 39),
            self.eq(r"A_2=4(4)=16", 39),
            self.box(r"A_T=35+16=51\ \mathrm{cm}^2", 5.55, 45),
        ).arrange(DOWN, buff=.20).move_to(RIGHT*3.75+DOWN*.78)
        self.play(FadeIn(alt), run_time=.65)
        self.wait(2.0)

        self.set_process(strip, 4)
        check = self.txt("METHOD A = METHOD B = 51 cm²", 31, True)
        check.move_to(RIGHT*3.65+UP*1.35)
        self.play(FadeIn(check), run_time=.5)
        self.wait(3.0)
        self.wipe()

    # ------------------------------------------------------------------
    # Square minus quadrant: make removed region and target unambiguous
    # ------------------------------------------------------------------

    def square_minus_quadrant(self):
        h = self.header(
            5,
            "SIMPLE SHADED AREA · SQUARE MINUS QUADRANT",
            "The white region is one quarter of a circle. The gray corner is the target area that remains.",
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
        rline = Line(corner, sq.get_corner(DR), color=INK, stroke_width=3)
        rlab = self.eq(r"r=8\ \mathrm{cm}", 30).next_to(rline, UP, buff=.10).shift(LEFT*.45)

        self.play(Create(sq), run_time=.8)
        self.play(FadeIn(sector), FadeIn(VGroup(side_dim, rline, rlab)), run_time=.8)
        self.wait(.8)

        self.set_process(strip, 1)
        removed = self.txt("REMOVED QUADRANT", 25, True)
        removed.move_to(corner+RIGHT*1.55+UP*1.05)
        self.fit(removed, 2.8, .48)
        target = self.txt("TARGET SHADED", 25, True).move_to(LEFT*.45+UP*1.28)
        target_arrow = Arrow(
            target.get_left()+LEFT*.10,
            sq.get_corner(UR)+LEFT*.35+DOWN*.35,
            buff=.08,
            color=INK,
            stroke_width=2.5,
        )
        relation = self.txt("radius = square side = 8 cm", 25, True)
        relation.move_to(RIGHT*3.65+UP*1.62)
        self.fit(relation, 5.9, .5)
        self.play(
            FadeIn(removed), FadeIn(target), GrowArrow(target_arrow), FadeIn(relation),
            run_time=.7,
        )

        self.set_process(strip, 2)
        rule = self.box(
            r"A_s=A_{\square}-A_{\mathrm{quadrant}}",
            6.05, 45,
        ).move_to(RIGHT*3.65+UP*.84)
        self.play(FadeIn(rule), run_time=.6)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "SQUARE − QUADRANT",
            [
                r"A_{\square}=8^2=64",
                r"A_Q=\frac{\pi(8)^2}{4}=16\pi",
                r"A_s=64-16\pi",
            ],
            r"A_s\approx13.73\ \mathrm{cm}^2",
        ).shift(DOWN*.72)
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.9)

        self.set_process(strip, 4)
        note = self.txt("8 cm is the RADIUS here, not the diameter.", 28, True)
        note.move_to(RIGHT*3.65+DOWN*2.72)
        self.fit(note, 6.1, .55)
        self.play(FadeIn(note), run_time=.5)
        self.wait(2.6)
        self.wipe()

    # ------------------------------------------------------------------
    # Rectangle + semicircle: correct 10:6 proportions and radius reasoning
    # ------------------------------------------------------------------

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
            r"d=10\ \Rightarrow\ r=\frac{10}{2}=5\ \mathrm{cm}",
            5.8, 42,
        ).move_to(RIGHT*3.55+UP*1.35)
        self.play(Create(diameter), Create(radius), FadeIn(radius_step), run_time=.7)

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_{\mathrm{rectangle}}+A_{\mathrm{semicircle}}",
            6.15, 42,
        ).move_to(RIGHT*3.55+UP*.45)
        self.play(FadeIn(structure), run_time=.55)

        self.set_process(strip, 3)
        panel = self.solution_panel(
            "ADD BOTH TARGET PIECES",
            [
                r"A_R=10(6)=60",
                r"A_S=\frac{\pi(5)^2}{2}=\frac{25\pi}{2}",
                r"A_T=60+\frac{25\pi}{2}",
            ],
            r"A_T\approx99.27\ \mathrm{cm}^2",
        ).shift(DOWN*.62)
        self.play(FadeIn(panel), run_time=.7)
        self.wait(2.8)

        self.set_process(strip, 4)
        note = self.txt(
            "The shared diameter is an INTERNAL boundary; do not subtract it.",
            26, True,
        ).move_to(RIGHT*3.62+DOWN*2.72)
        self.fit(note, 6.1, .55)
        self.play(FadeIn(note), run_time=.5)
        self.wait(2.5)
        self.wipe()

    # ------------------------------------------------------------------
    # Hidden dimensions: attach the unknowns to the actual missing segments
    # ------------------------------------------------------------------

    def hidden_dimensions(self):
        h = self.header(
            7,
            "BEFORE CALCULATING · COMPLETE THE MISSING DIMENSIONS",
            "Subtract corresponding outer segments before you calculate any area.",
        )
        self.add(h)

        x0, y0, sx, sy = -5.9, -1.9, .44, .44
        fill, outline = self._concave_l(x0, y0, sx, sy, 12, 8, 4, 3, opacity=.70)
        self.play(FadeIn(fill), Create(outline), run_time=.8)

        known = VGroup(
            self.dimension_line([x0,y0-.25,0],[x0+12*sx,y0-.25,0],r"12",DOWN,29),
            self.dimension_line([x0-.25,y0,0],[x0-.25,y0+8*sy,0],r"8",LEFT,29),
            self.dimension_line([x0+8*sx,y0+8*sy+.22,0],[x0+12*sx,y0+8*sy+.22,0],r"4",UP,29),
            self.dimension_line([x0+12*sx+.22,y0+5*sy,0],[x0+12*sx+.22,y0+8*sy,0],r"3",RIGHT,29),
        )
        self.play(FadeIn(known), run_time=.7)

        unknown_top = self.dimension_line(
            [x0,y0+8*sy+.52,0], [x0+8*sx,y0+8*sy+.52,0], r"?", UP, 31,
        )
        unknown_right = self.dimension_line(
            [x0+12*sx+.55,y0,0], [x0+12*sx+.55,y0+5*sy,0], r"?", RIGHT, 31,
        )
        question = self.txt("Find these two missing lengths first.", 31, True)
        question.move_to(RIGHT*3.55+UP*1.48)
        self.play(FadeIn(VGroup(unknown_top, unknown_right, question)), run_time=.65)
        self.wait(2.2)

        calc = VGroup(
            self.eq(r"12-4=8\quad\text{(top segment)}", 42),
            self.eq(r"8-3=5\quad\text{(right segment)}", 42),
        ).arrange(DOWN, buff=.32).move_to(RIGHT*3.55+DOWN*.02)
        self.play(FadeIn(calc[0]), run_time=.55)
        self.wait(.7)
        self.play(FadeIn(calc[1]), run_time=.55)
        self.wait(.8)

        solved_top = self.dimension_line(
            [x0,y0+8*sy+.52,0], [x0+8*sx,y0+8*sy+.52,0], r"8", UP, 31,
        )
        solved_right = self.dimension_line(
            [x0+12*sx+.55,y0,0], [x0+12*sx+.55,y0+5*sy,0], r"5", RIGHT, 31,
        )
        self.play(
            Transform(unknown_top, solved_top),
            Transform(unknown_right, solved_right),
            run_time=.7,
        )

        rule = self.box(
            r"\text{Complete dimensions first}\;\longrightarrow\;\text{area second}",
            7.25, 42,
        ).move_to(RIGHT*3.55+DOWN*1.82)
        self.play(FadeIn(rule), run_time=.6)
        self.wait(3.1)
        self.wipe()

    # ------------------------------------------------------------------
    # Guided challenge: real roof altitude, real radius, no overlapping labels
    # ------------------------------------------------------------------

    def guided_challenge(self):
        h = self.header(
            9,
            "GUIDED CHALLENGE · HOUSE WITH A CIRCULAR WINDOW",
            "Add the rectangle and roof, then subtract the circular window. Pause before the reveal.",
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
        h_lab = self.eq(r"h_{\triangle}=3\ \mathrm{cm}", 28).next_to(altitude, LEFT, buff=.12)
        radius_line = Line(window.get_center(), window.get_right(), color=INK, stroke_width=3)
        r_lab = self.eq(r"r=1\ \mathrm{cm}", 27).next_to(radius_line, UP, buff=.08)

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
        rect_lab = self.txt("+ RECTANGLE", 24, True).move_to(rect.get_center()+DOWN*.83)
        tri_lab = self.txt("+ TRIANGLE", 24, True).move_to(roof.get_center()+UP*.15)
        circ_lab = self.txt("− CIRCLE", 24, True).next_to(window, RIGHT, buff=.35)
        leader = Arrow(
            circ_lab.get_left(), window.get_right(),
            buff=.08, color=INK, stroke_width=2.4,
        )
        self.play(
            FadeIn(rect_lab), FadeIn(tri_lab), FadeIn(circ_lab), GrowArrow(leader),
            run_time=.65,
        )

        self.set_process(strip, 2)
        structure = self.box(
            r"A_T=A_R+A_{\triangle}-A_C",
            6.15, 47,
        ).move_to(RIGHT*3.55+UP*1.30)
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
            height=5.02,
        ).shift(DOWN*.48)
        self.play(FadeIn(panel), run_time=.7)
        self.wait(3.1)

        self.set_process(strip, 4)
        self.play(Circumscribe(panel[1][-2], color=GRAY), run_time=.8)
        self.wait(2.4)
        self.wipe()

    # ------------------------------------------------------------------
    # Larger summary cards for projector readability
    # ------------------------------------------------------------------

    def common_errors(self):
        h = self.header(
            10,
            "COMMON ERRORS · CHECK THE GEOMETRY BEFORE THE ARITHMETIC",
            "Correct region choice and correct dimensions matter more than fast calculation.",
        )
        self.add(h)
        items = [
            ("ERROR 1 · WRONG REGION", "Subtract the HOLE, not the shaded target."),
            ("ERROR 2 · RADIUS / DIAMETER", "Circle area uses r. Convert d to r first."),
            ("ERROR 3 · HIDDEN LENGTHS", "Complete missing segments before area."),
            ("ERROR 4 · UNITS", "Area answers must use cm², m², ..."),
        ]
        cards = VGroup()
        for title, text in items:
            box = RoundedRectangle(
                width=6.50,
                height=1.78,
                corner_radius=.12,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            title_m = self.txt(title, 27, True)
            text_m = self.txt(text, 27)
            self.fit(title_m, 5.9, .42)
            self.fit(text_m, 5.85, .54)
            VGroup(title_m, text_m).arrange(DOWN, buff=.14).move_to(box)
            cards.add(VGroup(box, title_m, text_m))
        cards.arrange_in_grid(rows=2, cols=2, buff=(.32, .34)).shift(DOWN*.22)
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
                width=4.35,
                height=1.48,
                corner_radius=.11,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            text_m = self.txt(text, 28, True)
            self.fit(text_m, 3.92, .74)
            text_m.move_to(box)
            cards.add(VGroup(box, text_m))
        cards.arrange_in_grid(rows=2, cols=3, buff=(.30, .30)).shift(UP*.46)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*.05) for c in cards], lag_ratio=.08),
            run_time=1.4,
        )
        self.wait(2.8)
        general = self.box(
            r"A_{\mathrm{target}}=\sum A_+-\sum A_-",
            7.45, 55,
        ).shift(DOWN*1.72)
        self.play(FadeIn(general), run_time=.6)
        self.wait(2.0)
        preview = self.txt(
            "NEXT → COMPLEX SHADED AREAS: repeated pieces · several holes · symmetry · multiple strategies",
            29, True,
        ).to_edge(DOWN, buff=.28)
        self.fit(preview, 14.0, .70)
        self.play(FadeIn(preview), run_time=.6)
        self.wait(3.6)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Composite_Simple_Shaded_Areas_V2_SENIOR.py Geometry8CompositeSimpleShadedAreasV2Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Composite_Simple_Shaded_Areas_V2_SENIOR.py Geometry8CompositeSimpleShadedAreasV2Senior --disable_caching
