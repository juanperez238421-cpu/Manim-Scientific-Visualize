#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas Masterclass — Senior visual QA V2.

This release keeps the accepted FINAL presentation as the base and only replaces
scenes where frame-by-frame review found avoidable visual or pedagogical defects.

QA V2 corrections:
- clearer perimeter-vs-area highlighting;
- larger, row-aware unit-square and rectangle animations;
- parallelogram cut-and-translate with an explicit translation cue and no fill flash;
- triangle duplication as a rigid 180° rotation (no polygon-morph/fan artifact);
- stable trapezoid/rhombus entrances plus explicit geometric dimensions;
- composite figure rebuilt to match the stated 6×6 and 3×2 decomposition exactly;
- scaling shown as a true similarity enlargement by k=2;
- applied floor problem separates interior-area and boundary-perimeter animations;
- ManimCE 0.20.1-compatible Sector constructors retained.
"""
from __future__ import annotations

from Geometry8_2D_Areas_Masterclass_FINAL import *


class Geometry8Areas2DMasterclassFinalQA(Geometry8Areas2DMasterclassFinal):
    """Release class: geometry-first, motion-safe, classroom-readable QA layer."""

    def area_vs_perimeter(self):
        h = self.header(
            2,
            "AREA VS PERIMETER",
            "Perimeter measures the boundary; area measures the region inside it.",
        )
        self.add(h)

        outline = Rectangle(
            width=5.55,
            height=3.35,
            color=INK,
            stroke_width=6,
            fill_opacity=0,
        ).shift(LEFT * 3.35 + DOWN * .30)
        interior = outline.copy().set_stroke(opacity=0).set_fill(FILL, opacity=.90)
        border_flash = outline.copy().set_fill(opacity=0).set_stroke(INK, width=11)

        p_label = self.txt("PERIMETER = boundary length", 31, True).next_to(outline, DOWN, buff=.27)
        a_label = self.txt("AREA = covered region", 31, True).next_to(outline, DOWN, buff=.27)
        n = self.note(
            "UNITS",
            ["Perimeter: cm, m, km", "Area: cm², m², km²", "Area uses square units."],
            5.7,
        ).move_to(RIGHT * 3.55 + DOWN * .25)

        self.play(FadeIn(outline), run_time=.55)
        self.play(ShowPassingFlash(border_flash, time_width=.45), FadeIn(p_label), run_time=1.05)
        self.wait(.85)
        self.play(FadeOut(p_label), FadeIn(interior), FadeIn(a_label), run_time=.70)
        self.play(FadeIn(n, shift=LEFT * .05), run_time=.65)
        self.wait(2.65)
        self.wipe()

    def unit_squares(self):
        h = self.header(
            3,
            "SQUARE UNITS",
            "Area counts how many 1×1 squares cover a region without gaps or overlaps.",
        )
        self.add(h)

        g = self.grid(5, 3, .88).shift(LEFT * 2.85 + DOWN * .22)
        rows = [VGroup(*g[j * 5:(j + 1) * 5]) for j in range(3)]
        row_caption = self.txt("3 rows · 5 unit squares in each row", 29, True).move_to(RIGHT * 3.55 + UP * .90)
        count = self.eq(r"5\times3=15\ \text{unit squares}", 46).move_to(RIGHT * 3.55 + UP * .20)
        ans = self.box(r"A=15\ \text{units}^2", 5.8, 58).move_to(RIGHT * 3.55 + DOWN * .95)

        for row in rows:
            self.play(LaggedStart(*[FadeIn(x, scale=.88) for x in row], lag_ratio=.06), run_time=.58)
        self.play(FadeIn(row_caption, shift=UP * .04), run_time=.55)
        self.play(Write(count), run_time=.65)
        self.play(FadeIn(ans), run_time=.65)
        self.wait(2.45)
        self.wipe()

    def rectangle(self):
        h = self.header(4, "RECTANGLE — THE BASE MODEL", "Rows × columns becomes base × height.")
        self.add(h)

        g = self.grid(5, 3, .80).shift(LEFT * 3.25 + DOWN * .16)
        out = Rectangle(width=4.0, height=2.40, color=INK, stroke_width=5).move_to(g)
        base = DoubleArrow(out.get_corner(DL) + DOWN * .34, out.get_corner(DR) + DOWN * .34, buff=0, color=INK, stroke_width=2.2)
        height = DoubleArrow(out.get_corner(DL) + LEFT * .34, out.get_corner(UL) + LEFT * .34, buff=0, color=INK, stroke_width=2.2)
        b_lab = self.eq("b", 38).next_to(base, DOWN, buff=.05)
        h_lab = self.eq("h", 38).next_to(height, LEFT, buff=.05)

        rhs = VGroup(
            self.txt("5 squares per row", 30, True),
            self.txt("3 equal rows", 30),
            self.eq(r"5+5+5=3\cdot5", 43),
            self.box(r"A=b\,h", 5.2, 64),
        ).arrange(DOWN, buff=.29).move_to(RIGHT * 3.55 + DOWN * .02)

        row_groups = [VGroup(*g[j * 5:(j + 1) * 5]) for j in range(3)]
        for row in row_groups:
            self.play(LaggedStart(*[FadeIn(x) for x in row], lag_ratio=.04), run_time=.47)
        self.play(Create(out), run_time=.55)
        self.play(GrowFromCenter(base), GrowFromCenter(height), FadeIn(b_lab), FadeIn(h_lab), run_time=.65)
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.52)
            self.wait(.48)
        self.wait(2.15)
        self.wipe()

    def parallelogram(self):
        h = self.header(
            6,
            "PARALLELOGRAM — CUT AND TRANSLATE",
            "Cut one triangular piece and slide it without rotating; the same pieces close into a rectangle.",
        )
        self.add(h)

        # Exact construction: the left triangle translates +4.4 units and
        # becomes exactly the missing right-hand triangle of the rectangle.
        A = np.array([-5.6, -1.40, 0.0])
        E = np.array([-4.6, -1.40, 0.0])
        B = np.array([-1.2, -1.40, 0.0])
        F = np.array([-0.2, -1.40, 0.0])
        C = np.array([-0.2,  1.40, 0.0])
        D = np.array([-4.6,  1.40, 0.0])

        full = Polygon(A, B, C, D, stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.62)
        cut = DashedLine(D, E, color=MID, stroke_width=3)
        cut_label = self.txt("CUT", 25, True).move_to(D + LEFT * .42 + DOWN * .24)

        left_piece = Polygon(A, E, D, stroke_color=INK, stroke_width=4, fill_color=WHITE, fill_opacity=1)
        remaining = Polygon(E, B, C, D, stroke_color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.62)
        rect_outline = Polygon(E, F, C, D, stroke_color=INK, stroke_width=5, fill_opacity=0)

        move_arrow = Arrow(
            left_piece.get_center() + UP * 1.90,
            left_piece.get_center() + UP * 1.90 + RIGHT * 4.15,
            buff=.05,
            color=MID,
            stroke_width=3,
            max_tip_length_to_length_ratio=.09,
        )
        move_label = self.txt("translate — no rotation", 25, True).next_to(move_arrow, UP, buff=.05)

        base_line = DoubleArrow(E + DOWN * .38, F + DOWN * .38, buff=0, color=INK, stroke_width=2.2)
        height_line = DoubleArrow(E + LEFT * .38, D + LEFT * .38, buff=0, color=INK, stroke_width=2.2)
        base_lab = self.eq("b", 40).next_to(base_line, DOWN, buff=.06)
        height_lab = self.eq("h", 40).next_to(height_line, LEFT, buff=.06)

        message = self.txt("Same pieces → same area", 32, True).move_to(RIGHT * 3.55 + UP * 1.20)
        relation = self.eq(r"A_{\text{parallelogram}}=A_{\text{rectangle}}", 42).move_to(RIGHT * 3.55 + UP * .30)
        formula = self.box(r"A=b\,h", 5.4, 64).move_to(RIGHT * 3.55 + DOWN * .85)

        self.play(FadeIn(full), run_time=.55)
        self.play(Create(cut), FadeIn(cut_label), run_time=.60)
        self.wait(.60)
        self.play(FadeOut(full), FadeIn(remaining), FadeIn(left_piece), run_time=.50)
        self.play(Circumscribe(left_piece, color=GRAY, buff=.05), run_time=.70)
        self.play(GrowArrow(move_arrow), FadeIn(move_label), run_time=.55)
        self.play(left_piece.animate.shift(RIGHT * 4.4), run_time=1.35, rate_func=smooth)
        self.play(FadeOut(move_arrow), FadeOut(move_label), FadeOut(cut_label), run_time=.35)
        self.play(Create(rect_outline), FadeOut(cut), run_time=.60)
        self.play(GrowFromCenter(base_line), GrowFromCenter(height_line), FadeIn(base_lab), FadeIn(height_lab), run_time=.68)
        self.play(FadeIn(message, shift=UP * .04), run_time=.50)
        self.play(FadeIn(relation), run_time=.50)
        self.play(FadeIn(formula, shift=UP * .04), run_time=.55)
        self.play(Circumscribe(formula[1], color=GRAY), run_time=.80)
        self.wait(2.55)
        self.wipe()

    def triangle(self):
        h = self.header(
            7,
            "TRIANGLE — HALF OF A PARALLELOGRAM",
            "Copy one triangle and move the congruent copy rigidly; together they form one parallelogram.",
        )
        self.add(h)

        A = np.array([-5.6, -1.35, 0.0])
        B = np.array([-2.0, -1.35, 0.0])
        C = np.array([-4.55, 1.35, 0.0])
        D = B + C - A  # exact fourth vertex of the parallelogram
        midpoint = (B + C) / 2

        tri1 = Polygon(A, B, C, stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.70)
        moving_copy = tri1.copy().set_fill(PAPER, opacity=.92).set_stroke(MID, width=4)
        para_outline = Polygon(A, B, D, C, stroke_color=INK, stroke_width=5, fill_opacity=0)
        diagonal = Line(B, C, color=MID, stroke_width=2.8)
        pivot = Dot(midpoint, radius=.065, color=INK)
        pivot_label = self.txt("rigid 180° turn", 24, True).next_to(pivot, UP, buff=.16)

        base_line = DoubleArrow(A + DOWN * .38, B + DOWN * .38, buff=0, color=INK, stroke_width=2.2)
        height_line = DoubleArrow(A + LEFT * .38, A + LEFT * .38 + UP * 2.70, buff=0, color=INK, stroke_width=2.2)
        base_lab = self.eq("b", 40).next_to(base_line, DOWN, buff=.06)
        height_lab = self.eq("h", 40).next_to(height_line, LEFT, buff=.06)

        rhs = VGroup(
            self.txt("2 congruent triangles = 1 parallelogram", 31, True),
            self.eq(r"2A_{\triangle}=b\,h", 48),
            self.box(r"A_{\triangle}=\frac12b\,h", 6.0, 58),
        ).arrange(DOWN, buff=.35).move_to(RIGHT * 3.55 + DOWN * .05)

        self.play(FadeIn(tri1), run_time=.55)
        self.play(GrowFromCenter(base_line), GrowFromCenter(height_line), FadeIn(base_lab), FadeIn(height_lab), run_time=.65)
        self.wait(.55)
        self.add(moving_copy)
        self.play(FadeIn(pivot), FadeIn(pivot_label), run_time=.40)
        # Rigid motion instead of TransformFromCopy: every intermediate frame remains a triangle.
        self.play(Rotate(moving_copy, angle=PI, about_point=midpoint), run_time=1.35, rate_func=smooth)
        self.play(FadeOut(pivot), FadeOut(pivot_label), run_time=.30)
        self.play(
            tri1.animate.set_stroke(opacity=0),
            moving_copy.animate.set_stroke(opacity=0),
            Create(para_outline),
            Create(diagonal),
            run_time=.62,
        )
        self.wait(.45)
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.55)
            self.wait(.58)
        self.play(Circumscribe(rhs[-1][1], color=GRAY), run_time=.82)
        self.wait(2.55)
        self.wipe()

    def extended_toolkit(self):
        h = self.header(
            8,
            "EXTENDED 2D AREA TOOLKIT",
            "The same decomposition idea extends to trapezoids and rhombi.",
        )
        self.add(h)

        # Trapezoid: show both parallel bases and the perpendicular height.
        t = Polygon(
            [-6.25, -1.05, 0], [-2.35, -1.05, 0], [-3.15, 1.15, 0], [-5.40, 1.15, 0],
            stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.62,
        )
        t_alt = DashedLine([-5.40, -1.05, 0], [-5.40, 1.15, 0], color=MID, stroke_width=2.6)
        t_b1 = DoubleArrow([-5.40, 1.48, 0], [-3.15, 1.48, 0], buff=0, color=INK, stroke_width=2)
        t_b2 = DoubleArrow([-6.25, -1.40, 0], [-2.35, -1.40, 0], buff=0, color=INK, stroke_width=2)
        t_h = DoubleArrow([-6.58, -1.05, 0], [-6.58, 1.15, 0], buff=0, color=INK, stroke_width=2)
        t_labs = VGroup(
            self.eq("b_1", 34).next_to(t_b1, UP, buff=.03),
            self.eq("b_2", 34).next_to(t_b2, DOWN, buff=.03),
            self.eq("h", 34).next_to(t_h, LEFT, buff=.04),
        )
        te = self.box(r"A=\frac{(b_1+b_2)h}{2}", 6.15, 50).move_to([-4.30, -2.47, 0])

        # Rhombus: diagonals explicitly partition the region into four triangles.
        R = np.array([5.85, 0.0, 0.0])
        L = np.array([2.05, 0.0, 0.0])
        T = np.array([3.95, 1.52, 0.0])
        Bm = np.array([3.95, -1.52, 0.0])
        rh = Polygon(L, T, R, Bm, stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.62)
        d1 = DashedLine(L, R, color=INK, stroke_width=2.7)
        d2 = DashedLine(Bm, T, color=INK, stroke_width=2.7)
        d1_lab = self.eq("d_1", 34).next_to(d1, UP, buff=.08)
        d2_lab = self.eq("d_2", 34).next_to(d2, RIGHT, buff=.08)
        re = self.box(r"A=\frac{d_1d_2}{2}", 5.05, 54).move_to([3.95, -2.47, 0])

        self.play(FadeIn(t, scale=.97), run_time=.55)
        self.play(Create(t_alt), GrowFromCenter(t_b1), GrowFromCenter(t_b2), GrowFromCenter(t_h), FadeIn(t_labs), run_time=.80)
        self.play(FadeIn(te), run_time=.55)
        self.play(FadeIn(rh, scale=.97), run_time=.55)
        self.play(Create(d1), Create(d2), FadeIn(d1_lab), FadeIn(d2_lab), run_time=.72)
        self.play(FadeIn(re), run_time=.55)
        self.wait(2.75)
        self.wipe()

    def circle_parts(self):
        h = self.header(
            10,
            "CIRCLE PARTS — FRACTIONS OF THE FULL AREA",
            "Semicircles and quadrants use a fraction of A = πr².",
        )
        self.add(h)
        s = Sector(radius=1.75, angle=PI, start_angle=0, color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.75).shift(LEFT * 4 + DOWN * .1)
        q = Sector(radius=1.75, angle=PI / 2, start_angle=0, color=INK, stroke_width=4, fill_color=FILL, fill_opacity=.75).shift(RIGHT * 2.9 + DOWN * .1)
        e1 = self.box(r"A_{semi}=\frac12\pi r^2", 5.1, 48).next_to(s, DOWN, buff=.25)
        e2 = self.box(r"A_{quad}=\frac14\pi r^2", 5.1, 48).next_to(q, DOWN, buff=.25)
        self.play(FadeIn(s, scale=.96), run_time=.55)
        self.play(FadeIn(e1), run_time=.50)
        self.play(FadeIn(q, scale=.96), run_time=.55)
        self.play(FadeIn(e2), run_time=.50)
        self.wait(2.65)
        self.wipe()

    def composite(self):
        h = self.header(
            12,
            "COMPOSITE FIGURES — ADD KNOWN AREAS",
            "Break one unfamiliar figure into familiar pieces, then add.",
        )
        self.add(h)

        # Exact classroom geometry: 6×6 rectangle + 3×2 rectangle.
        u = .48
        x0, xs, xr = -6.20, -6.20 + 6 * u, -6.20 + 9 * u
        y0, yt, yr = -1.65, -1.65 + 6 * u, -1.65 + 2 * u
        Lshape = Polygon(
            [x0, y0, 0], [xr, y0, 0], [xr, yr, 0], [xs, yr, 0], [xs, yt, 0], [x0, yt, 0],
            stroke_color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.62,
        )
        split = DashedLine([xs, y0, 0], [xs, yr, 0], color=MID, stroke_width=3)
        left_ref = Rectangle(width=6 * u, height=6 * u, color=MID, stroke_width=2.2).move_to([(x0 + xs) / 2, (y0 + yt) / 2, 0])
        right_ref = Rectangle(width=3 * u, height=2 * u, color=MID, stroke_width=2.2).move_to([(xs + xr) / 2, (y0 + yr) / 2, 0])

        dim6v = DoubleArrow([x0 - .34, y0, 0], [x0 - .34, yt, 0], buff=0, color=INK, stroke_width=2)
        dim6h = DoubleArrow([x0, yt + .34, 0], [xs, yt + .34, 0], buff=0, color=INK, stroke_width=2)
        dim3 = DoubleArrow([xs, y0 - .34, 0], [xr, y0 - .34, 0], buff=0, color=INK, stroke_width=2)
        dim2 = DoubleArrow([xr + .34, y0, 0], [xr + .34, yr, 0], buff=0, color=INK, stroke_width=2)
        dims = VGroup(
            dim6v, dim6h, dim3, dim2,
            self.eq("6", 32).next_to(dim6v, LEFT, buff=.04),
            self.eq("6", 32).next_to(dim6h, UP, buff=.04),
            self.eq("3", 32).next_to(dim3, DOWN, buff=.04),
            self.eq("2", 32).next_to(dim2, RIGHT, buff=.04),
        )

        title = self.txt("Decompose into 2 rectangles", 31, True).move_to(RIGHT * 3.55 + UP * 1.45)
        e1 = self.eq(r"A_1=6\cdot6=36", 42).move_to(RIGHT * 3.55 + UP * .55)
        e2 = self.eq(r"A_2=3\cdot2=6", 42).move_to(RIGHT * 3.55 + DOWN * .15)
        total = self.box(r"A_{total}=36+6=42", 6.0, 52).move_to(RIGHT * 3.55 + DOWN * 1.20)

        self.play(FadeIn(Lshape, scale=.97), Create(split), run_time=.70)
        self.play(LaggedStart(*[FadeIn(x) for x in dims], lag_ratio=.06), run_time=.85)
        self.play(FadeIn(title), run_time=.45)
        self.play(Circumscribe(left_ref, color=GRAY, buff=.03), FadeIn(e1), run_time=.78)
        self.play(Circumscribe(right_ref, color=GRAY, buff=.03), FadeIn(e2), run_time=.78)
        self.play(FadeIn(total), run_time=.55)
        self.wait(2.55)
        self.wipe()

    def shaded_complex(self):
        h = self.header(
            14,
            "COMPLEX SHADED AREA — SIMPLIFY FIRST",
            "Recognize repeated pieces before calculating.",
        )
        self.add(h)
        sq = Square(4.7, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.72).shift(LEFT * 3.2 + DOWN * .05)
        corners = [sq.get_corner(DL), sq.get_corner(DR), sq.get_corner(UR), sq.get_corner(UL)]
        starts = [0, PI / 2, PI, 3 * PI / 2]
        sectors = VGroup(*[
            Sector(arc_center=c, radius=2.35, angle=PI / 2, start_angle=a, stroke_color=INK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
            for c, a in zip(corners, starts)
        ])
        rhs = VGroup(
            self.txt("4 quadrants = 1 full circle", 30, True),
            self.eq(r"A_s=12^2-\pi(6)^2", 44),
            self.box(r"A_s=144-36\pi\approx30.90", 6.1, 48),
        ).arrange(DOWN, buff=.34).move_to(RIGHT * 3.45 + DOWN * .05)
        self.play(FadeIn(sq, scale=.98), run_time=.50)
        self.play(LaggedStart(*[FadeIn(s, scale=.96) for s in sectors], lag_ratio=.10), run_time=1.00)
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.55)
            self.wait(.58)
        self.wait(2.35)
        self.wipe()

    def scaling(self):
        h = self.header(
            15,
            "SCALING — PERIMETER × k, AREA × k²",
            "Doubling every length doubles perimeter but quadruples area.",
        )
        self.add(h)

        small = Rectangle(width=2.20, height=1.65, color=INK, stroke_width=5, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 5.0 + DOWN * .15)
        large_center = np.array([-1.55, -.15, 0.0])
        moving = small.copy().set_fill(FILL, opacity=.65)
        la = self.txt("4×3  →  P=14, A=12", 27, True).next_to(small, DOWN, buff=.16)
        lb = self.txt("8×6  →  P=28, A=48", 27, True).next_to(moving.copy().scale(2).move_to(large_center), DOWN, buff=.16)
        k2 = self.box(r"k=2", 2.55, 47).move_to([-3.25, 2.05, 0])
        rule = VGroup(self.box(r"P'=kP", 4.5, 52), self.box(r"A'=k^2A", 4.5, 52)).arrange(DOWN, buff=.30).move_to(RIGHT * 4.75 + DOWN * .10)

        self.play(FadeIn(small), FadeIn(la), run_time=.60)
        self.add(moving)
        self.play(FadeIn(k2), run_time=.40)
        self.play(moving.animate.scale(2).move_to(large_center), run_time=1.35, rate_func=smooth)
        self.play(FadeIn(lb), run_time=.45)
        self.play(FadeIn(rule, shift=LEFT * .04), run_time=.65)
        self.play(Circumscribe(rule[1][1], color=GRAY), run_time=.75)
        self.wait(2.65)
        self.wipe()

    def applied(self):
        h = self.header(
            16,
            "APPLIED 2D PROBLEM — FLOOR AND BORDER",
            "Decide whether the question asks for surface, boundary, or both.",
        )
        self.add(h)

        floor = Rectangle(width=5.30, height=3.30, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.18).shift(LEFT * 3.30 + DOWN * .10)
        labs = VGroup(
            self.txt("6 m", 30, True).next_to(floor, DOWN, buff=.16),
            self.txt("4 m", 30, True).next_to(floor, LEFT, buff=.16).rotate(PI / 2),
        )
        border_flash = floor.copy().set_fill(opacity=0).set_stroke(INK, width=10)

        area_title = self.txt("Tiles cover inside → AREA", 30, True).move_to(RIGHT * 3.45 + UP * 1.10)
        area_eq = self.eq(r"A=6\cdot4=24\ \mathrm{m}^2", 43).move_to(RIGHT * 3.45 + UP * .35)
        per_title = self.txt("Trim follows edge → PERIMETER", 30, True).move_to(RIGHT * 3.45 + DOWN * .50)
        per_eq = self.eq(r"P=2(6+4)=20\ \mathrm{m}", 43).move_to(RIGHT * 3.45 + DOWN * 1.25)

        self.play(FadeIn(floor), FadeIn(labs), run_time=.65)
        self.play(floor.animate.set_fill(FILL, opacity=.72), FadeIn(area_title), run_time=.70)
        self.play(FadeIn(area_eq), run_time=.52)
        self.wait(.65)
        self.play(ShowPassingFlash(border_flash, time_width=.45), FadeIn(per_title), run_time=1.05)
        self.play(FadeIn(per_eq), run_time=.52)
        self.wait(2.55)
        self.wipe()


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
