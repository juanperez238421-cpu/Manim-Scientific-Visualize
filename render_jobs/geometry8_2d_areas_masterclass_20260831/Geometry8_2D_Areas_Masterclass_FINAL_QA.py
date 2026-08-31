#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior visual-QA layer for Geometry 8 2D Areas Masterclass.

Corrections after inspecting the actual PQH timeline:
- ManimCE 0.20.1-compatible Sector constructors;
- exact parallelogram cut-and-translate geometry that closes into a rectangle;
- exact two-congruent-triangle construction that closes into a parallelogram.
"""
from __future__ import annotations

from Geometry8_2D_Areas_Masterclass_FINAL import *


class Geometry8Areas2DMasterclassFinalQA(Geometry8Areas2DMasterclassFinal):
    """Release class: compatibility + geometry-first senior frame corrections."""

    def parallelogram(self):
        h = self.header(
            6,
            "PARALLELOGRAM — CUT AND TRANSLATE",
            "Cut one triangular piece and slide it without rotating; the same pieces close into a rectangle.",
        )
        self.add(h)

        # Exact construction.  The left triangle translates +4.4 units and
        # becomes exactly the missing right-hand triangle of the rectangle.
        A = np.array([-5.6, -1.40, 0.0])
        E = np.array([-4.6, -1.40, 0.0])
        B = np.array([-1.2, -1.40, 0.0])
        F = np.array([-0.2, -1.40, 0.0])
        C = np.array([-0.2,  1.40, 0.0])
        D = np.array([-4.6,  1.40, 0.0])

        full = Polygon(
            A, B, C, D,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.62,
        )
        cut = DashedLine(D, E, color=MID, stroke_width=3)
        cut_label = self.txt("CUT", 26, True).next_to(cut, LEFT, buff=.13)

        left_piece = Polygon(
            A, E, D,
            stroke_color=INK,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        remaining = Polygon(
            E, B, C, D,
            stroke_color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.62,
        )

        rect_outline = Polygon(
            E, F, C, D,
            stroke_color=INK,
            stroke_width=5,
            fill_opacity=0,
        )
        base_line = DoubleArrow(E + DOWN * .38, F + DOWN * .38, buff=0, color=INK, stroke_width=2.2)
        height_line = DoubleArrow(E + LEFT * .38, D + LEFT * .38, buff=0, color=INK, stroke_width=2.2)
        base_lab = self.eq("b", 40).next_to(base_line, DOWN, buff=.06)
        height_lab = self.eq("h", 40).next_to(height_line, LEFT, buff=.06)

        message = self.txt("Same pieces → same area", 32, True).move_to(RIGHT * 3.55 + UP * 1.20)
        relation = self.eq(r"A_{\text{parallelogram}}=A_{\text{rectangle}}", 42).move_to(RIGHT * 3.55 + UP * .30)
        formula = self.box(r"A=b\,h", 5.4, 64).move_to(RIGHT * 3.55 + DOWN * .85)

        self.play(Create(full), run_time=.85)
        self.play(Create(cut), FadeIn(cut_label, shift=RIGHT * .04), run_time=.65)
        self.wait(.85)
        self.play(
            FadeOut(full),
            FadeOut(cut_label),
            FadeIn(remaining),
            FadeIn(left_piece),
            run_time=.55,
        )
        self.play(Indicate(left_piece, scale_factor=1.025, color=GRAY), run_time=.70)
        self.wait(.55)
        self.play(left_piece.animate.shift(RIGHT * 4.4), run_time=1.25, rate_func=smooth)
        self.wait(.70)
        self.play(Create(rect_outline), FadeOut(cut), run_time=.70)
        self.play(
            GrowFromCenter(base_line),
            GrowFromCenter(height_line),
            FadeIn(base_lab),
            FadeIn(height_lab),
            run_time=.75,
        )
        self.play(FadeIn(message, shift=UP * .05), run_time=.55)
        self.play(FadeIn(relation), run_time=.55)
        self.play(FadeIn(formula, shift=UP * .05), run_time=.60)
        self.play(Circumscribe(formula[1], color=GRAY), run_time=.90)
        self.wait(2.9)
        self.wipe()

    def triangle(self):
        h = self.header(
            7,
            "TRIANGLE — HALF OF A PARALLELOGRAM",
            "Copy one triangle and place the congruent copy across the shared diagonal: together they form one parallelogram.",
        )
        self.add(h)

        A = np.array([-5.6, -1.35, 0.0])
        B = np.array([-2.0, -1.35, 0.0])
        C = np.array([-4.55, 1.35, 0.0])
        D = B + C - A  # exact fourth vertex of the parallelogram

        tri1 = Polygon(
            A, B, C,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.70,
        )
        tri2 = Polygon(
            B, D, C,
            stroke_color=INK,
            stroke_width=5,
            fill_color=PAPER,
            fill_opacity=.90,
        )
        para_outline = Polygon(
            A, B, D, C,
            stroke_color=INK,
            stroke_width=5,
            fill_opacity=0,
        )
        diagonal = Line(B, C, color=MID, stroke_width=2.8)

        base_line = DoubleArrow(A + DOWN * .38, B + DOWN * .38, buff=0, color=INK, stroke_width=2.2)
        height_line = DoubleArrow(A + LEFT * .38, A + LEFT * .38 + UP * 2.70, buff=0, color=INK, stroke_width=2.2)
        base_lab = self.eq("b", 40).next_to(base_line, DOWN, buff=.06)
        height_lab = self.eq("h", 40).next_to(height_line, LEFT, buff=.06)

        rhs = VGroup(
            self.txt("2 congruent triangles = 1 parallelogram", 31, True),
            self.eq(r"2A_{\triangle}=b\,h", 48),
            self.box(r"A_{\triangle}=\frac12b\,h", 6.0, 58),
        ).arrange(DOWN, buff=.35).move_to(RIGHT * 3.55 + DOWN * .05)

        self.play(Create(tri1), run_time=.80)
        self.play(
            GrowFromCenter(base_line),
            GrowFromCenter(height_line),
            FadeIn(base_lab),
            FadeIn(height_lab),
            run_time=.70,
        )
        self.wait(.75)
        self.play(TransformFromCopy(tri1, tri2), run_time=1.20, rate_func=smooth)
        self.play(Create(para_outline), Create(diagonal), run_time=.70)
        self.wait(.65)
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.58)
            self.wait(.70)
        self.play(Circumscribe(rhs[-1][1], color=GRAY), run_time=.90)
        self.wait(2.8)
        self.wipe()

    def circle_parts(self):
        h = self.header(
            10,
            "CIRCLE PARTS — FRACTIONS OF THE FULL AREA",
            "Semicircles and quadrants use a fraction of A = πr².",
        )
        self.add(h)
        s = Sector(
            radius=1.75,
            angle=PI,
            start_angle=0,
            color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.75,
        ).shift(LEFT * 4 + DOWN * .1)
        q = Sector(
            radius=1.75,
            angle=PI / 2,
            start_angle=0,
            color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.75,
        ).shift(RIGHT * 2.9 + DOWN * .1)
        e1 = self.box(r"A_{semi}=\frac12\pi r^2", 5.1, 48).next_to(s, DOWN, buff=.25)
        e2 = self.box(r"A_{quad}=\frac14\pi r^2", 5.1, 48).next_to(q, DOWN, buff=.25)
        self.play(Create(s), run_time=.7)
        self.play(FadeIn(e1), run_time=.55)
        self.play(Create(q), run_time=.7)
        self.play(FadeIn(e2), run_time=.55)
        self.wait(2.8)
        self.wipe()

    def shaded_complex(self):
        h = self.header(
            14,
            "COMPLEX SHADED AREA — SIMPLIFY FIRST",
            "Recognize repeated pieces before calculating.",
        )
        self.add(h)
        sq = Square(
            4.7,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.72,
        ).shift(LEFT * 3.2 + DOWN * .05)
        corners = [sq.get_corner(DL), sq.get_corner(DR), sq.get_corner(UR), sq.get_corner(UL)]
        starts = [0, PI / 2, PI, 3 * PI / 2]
        sectors = VGroup(*[
            Sector(
                arc_center=c,
                radius=2.35,
                angle=PI / 2,
                start_angle=a,
                stroke_color=INK,
                stroke_width=3,
                fill_color=WHITE,
                fill_opacity=1,
            )
            for c, a in zip(corners, starts)
        ])
        rhs = VGroup(
            self.txt("4 quadrants = 1 full circle", 30, True),
            self.eq(r"A_s=12^2-\pi(6)^2", 44),
            self.box(r"A_s=144-36\pi\approx30.90", 6.1, 48),
        ).arrange(DOWN, buff=.34).move_to(RIGHT * 3.45 + DOWN * .05)
        self.play(
            Create(sq),
            LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=.1),
            run_time=1.1,
        )
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.58)
            self.wait(.65)
        self.wait(2.5)
        self.wipe()


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
