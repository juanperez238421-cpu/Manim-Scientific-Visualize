#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V9 classroom simplification + circle spacing QA.

V9 keeps the complete validated V8 lesson and changes only two chapters:
1) CIRCLE: fewer visual sectors, larger vertical air-gaps, and a dedicated proof
   panel so no proof text can collide with the rearranged-sector strip.
2) POLYGONS: begin with a familiar house-shaped pentagon decomposed into a
   rectangle + triangle, then keep the regular-hexagon/apothem shortcut as the
   advanced continuation of the same chapter.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaPolygonCircleV9Mixin:
    """Student-first polygon chapter and collision-free circle derivation."""

    # ------------------------------------------------------------------
    # Circle: simplified sector count + four non-intersecting vertical bands.
    # ------------------------------------------------------------------
    def circle_explicit(self):
        h = self.header(
            10,
            "7 · CIRCLE",
            "Rearrange equal sectors to see why the circle behaves like a rectangle.",
        )
        strip = self.stage_strip()
        self.add(h, strip)

        center = np.array([-4.15, -.35, 0])
        radius = 1.55
        circle = Circle(
            radius,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.18,
        ).move_to(center)
        sweep = Line(center, center + RIGHT * radius, color=INK, stroke_width=4)
        dot = Dot(center, radius=.07, color=INK)

        self.mark_stage(strip, 0)
        self.play(FadeIn(dot), Create(sweep), run_time=.42)
        self.play(
            Create(circle),
            Rotate(sweep, angle=TAU, about_point=center),
            run_time=1.10,
            rate_func=linear,
        )
        construct_note = self.txt("A radius sweeps one complete circle.", 26, True)
        construct_note.move_to(RIGHT * 3.45 + UP * .80)
        self.play(FadeIn(construct_note), run_time=.34)
        self.wait(.55)
        self.play(FadeOut(construct_note), run_time=.24)

        self.mark_stage(strip, 1)
        diameter = DashedLine(
            center + LEFT * radius,
            center + RIGHT * radius,
            color=MID,
            stroke_width=2.8,
        )
        rlab = self.eq("r", 38).next_to(Line(center, center + RIGHT * radius), UP, buff=.08)
        dlab = self.eq("d=2r", 35).next_to(diameter, DOWN, buff=.18)
        self.play(Create(diameter), FadeIn(rlab), FadeIn(dlab), run_time=.58)
        parts_note = self.txt("Radius = r   ·   Diameter = 2r", 27, True)
        parts_note.move_to(RIGHT * 3.45 + UP * .80)
        self.play(FadeIn(parts_note), run_time=.34)
        self.wait(.70)
        self.play(FadeOut(parts_note), run_time=.24)

        self.mark_stage(strip, 2)

        # Fewer sectors than V8: enough to show the idea without creating a
        # visually dense comb of lines for Grade 8 students.
        n = 12
        theta = TAU / n
        sectors = VGroup()
        for k in range(n):
            sectors.add(
                Sector(
                    arc_center=center,
                    radius=radius,
                    start_angle=k * theta,
                    angle=theta,
                    stroke_color=INK,
                    stroke_width=1.45,
                    fill_color=FILL if k % 2 == 0 else PAPER,
                    fill_opacity=.76 if k % 2 == 0 else .94,
                )
            )

        source_outline = Circle(
            radius,
            color=LIGHT,
            stroke_width=2.0,
            fill_opacity=0,
        ).move_to(center)
        self.play(FadeOut(circle), FadeIn(source_outline), FadeIn(sectors), run_time=.52)

        cut_note = self.txt("STEP 1 · Cut the circle into equal sectors", 25, True)
        cut_note.move_to(RIGHT * 3.45 + UP * 1.20)
        self.play(FadeIn(cut_note), run_time=.32)
        self.wait(.55)

        step = (math.pi * radius) / n
        x0 = .95
        sector_y = -.70
        targets = VGroup()
        for i in range(n):
            x = x0 + i * step
            if i % 2 == 0:
                apex = np.array([x, -radius / 2 + sector_y, 0])
                start = PI / 2 - theta / 2
            else:
                apex = np.array([x, radius / 2 + sector_y, 0])
                start = 3 * PI / 2 - theta / 2
            targets.add(
                Sector(
                    arc_center=apex,
                    radius=radius,
                    start_angle=start,
                    angle=theta,
                    stroke_color=INK,
                    stroke_width=1.35,
                    fill_color=FILL if i % 2 == 0 else PAPER,
                    fill_opacity=.76 if i % 2 == 0 else .94,
                )
            )

        rearrange_note = self.txt("STEP 2 · Alternate the sectors up and down", 25, True)
        rearrange_note.move_to(cut_note)
        self.play(
            LaggedStart(
                *[Transform(sectors[i], targets[i]) for i in range(n)],
                lag_ratio=.035,
            ),
            ReplacementTransform(cut_note, rearrange_note),
            run_time=1.55,
            rate_func=smooth,
        )
        self.wait(.50)
        self.play(FadeOut(rearrange_note), run_time=.24)

        # TOP BAND: proof only. The panel bottom stays well above the sectors.
        proof_panel = self._safe_panel(
            5.95,
            1.02,
            RIGHT * 3.50 + UP * 1.30,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.997,
        )
        proof_title = self.txt("STEP 3 · Read the new dimensions", 23, True)
        proof_eq = self.eq(r"\text{base}=\frac{C}{2}=\pi r", 35)
        proof_text = VGroup(proof_title, proof_eq).arrange(DOWN, buff=.10)
        self.fit(proof_text, 5.35, .74)
        proof_text.move_to(proof_panel)
        proof = VGroup(proof_panel, proof_text)
        self.play(FadeIn(proof_panel), FadeIn(proof_text), run_time=.46)

        left_x = x0 - .10
        right_x = x0 + (n - 1) * step + .18

        # MIDDLE BAND: sector strip. BOTTOM DIMENSION BAND is separated below.
        base_y = -1.82
        base = self.dimension(
            [left_x, base_y, 0],
            [right_x, base_y, 0],
            r"\pi r",
            DOWN,
            31,
        )
        height = self.dimension(
            [right_x + .38, -radius / 2 + sector_y, 0],
            [right_x + .38, radius / 2 + sector_y, 0],
            "r",
            RIGHT,
            32,
        )
        self.play(
            GrowFromCenter(base[0]),
            FadeIn(base[1]),
            GrowFromCenter(height[0]),
            FadeIn(height[1]),
            run_time=.58,
        )
        self.wait(.55)

        # RESULT BAND: isolated below the dimension arrows.
        formula = self.box(r"A=(\pi r)(r)=\pi r^2", 5.45, 50)
        formula.move_to(RIGHT * 3.45 + DOWN * 2.88)
        self.play(FadeIn(formula), run_time=.44)
        self.wait(1.15)

        self.mark_stage(strip, 3)
        self.play(
            FadeOut(sectors),
            FadeOut(base),
            FadeOut(height),
            FadeOut(proof),
            FadeOut(formula),
            run_time=.36,
        )
        self.play(source_outline.animate.set_stroke(INK, width=4), run_time=.25)
        ex = self.example_stack(
            "Given: r = 4 cm",
            r"A=\pi r^2",
            r"A=\pi(4)^2=16\pi",
            r"A\approx50.27\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80)
        self.wipe()

    # ------------------------------------------------------------------
    # Polygons: familiar decomposition first; regular-polygon shortcut second.
    # ------------------------------------------------------------------
    def regular_polygon_explicit(self):
        h = self.header(
            11,
            "8 · POLYGONS",
            "Start with familiar shapes; then use the apothem shortcut for regular polygons.",
        )
        strip = self.stage_strip()
        self.add(h, strip)

        # Familiar house-shaped pentagon: rectangle + triangle.
        A = np.array([-5.85, -1.65, 0])
        B = np.array([-2.45, -1.65, 0])
        C = np.array([-2.45, .35, 0])
        D = np.array([-4.15, 1.75, 0])
        E = np.array([-5.85, .35, 0])
        house = Polygon(
            A, B, C, D, E,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.62,
        )

        self.mark_stage(strip, 0)
        self.play(Create(house), run_time=.78)
        familiar = self.txt("FAMILIAR PENTAGON", 26, True).next_to(house, DOWN, buff=.24)
        self.play(FadeIn(familiar), run_time=.32)
        self.wait(.55)

        self.mark_stage(strip, 1)
        split = DashedLine(E, C, color=INK, stroke_width=2.7)
        roof_alt = DashedLine(D, np.array([D[0], C[1], 0]), color=MID, stroke_width=2.4)
        right = self.right_mark(np.array([D[0], C[1], 0]), RIGHT, UP, .23)

        base_dim = self.dimension(A + DOWN * .30, B + DOWN * .30, "6\,\mathrm{cm}", DOWN, 28)
        rect_h = self.dimension(A + LEFT * .34, E + LEFT * .34, "4\,\mathrm{cm}", LEFT, 28)
        roof_h = self.dimension(
            np.array([D[0], C[1], 0]) + RIGHT * .30,
            D + RIGHT * .30,
            "3\,\mathrm{cm}",
            RIGHT,
            28,
        )

        rect_label = self.txt("RECTANGLE", 22, True).move_to([-4.15, -.70, 0])
        tri_label = self.txt("TRIANGLE", 22, True).move_to([-4.15, .82, 0])
        self.play(
            Create(split),
            Create(roof_alt),
            FadeIn(right),
            GrowFromCenter(base_dim[0]),
            FadeIn(base_dim[1]),
            GrowFromCenter(rect_h[0]),
            FadeIn(rect_h[1]),
            GrowFromCenter(roof_h[0]),
            FadeIn(roof_h[1]),
            FadeIn(rect_label),
            FadeIn(tri_label),
            run_time=.82,
        )

        simple_panel = self._safe_panel(5.75, 3.20, RIGHT * 3.55 + DOWN * .15)
        simple_body = VGroup(
            self.txt("DECOMPOSE INTO SHAPES YOU KNOW", 25, True),
            self.eq(r"A_{rect}=6(4)=24", 37),
            self.eq(r"A_{tri}=\frac{6(3)}{2}=9", 37),
            self.box(r"A_{total}=24+9=33\ \mathrm{cm}^2", 5.10, 45),
        ).arrange(DOWN, buff=.22)
        self.fit(simple_body, 5.20, 2.65)
        simple_body.move_to(simple_panel)
        simple = VGroup(simple_panel, simple_body)
        self.play(FadeIn(simple_panel), run_time=.28)
        for item in simple_body:
            self.play(FadeIn(item, shift=UP * .025), run_time=.36)
            self.wait(.30)
        self.wait(1.00)

        # Keep the regular polygon lesson, but clearly mark it as a shortcut.
        self.play(
            FadeOut(house),
            FadeOut(familiar),
            FadeOut(split),
            FadeOut(roof_alt),
            FadeOut(right),
            FadeOut(base_dim),
            FadeOut(rect_h),
            FadeOut(roof_h),
            FadeOut(rect_label),
            FadeOut(tri_label),
            FadeOut(simple),
            run_time=.45,
        )

        center = np.array([-4.05, -.25, 0])
        R = 1.72
        vertices = [
            center + R * np.array([
                math.cos(PI / 6 + k * TAU / 6),
                math.sin(PI / 6 + k * TAU / 6),
                0,
            ])
            for k in range(6)
        ]
        poly = Polygon(
            *vertices,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.56,
        )
        shortcut = self.txt("REGULAR HEXAGON · shortcut", 25, True)
        shortcut.move_to(RIGHT * 3.45 + UP * 1.18)
        self.play(Create(poly), FadeIn(Dot(center, radius=.07, color=INK)), FadeIn(shortcut), run_time=.72)
        self.wait(.45)

        self.mark_stage(strip, 2)
        spokes = VGroup(*[Line(center, v, color=LIGHT, stroke_width=1.9) for v in vertices])
        side_mid = (vertices[0] + vertices[1]) / 2
        ap = DashedLine(center, side_mid, color=INK, stroke_width=2.8)
        alab = self.eq("a", 34).next_to(ap, RIGHT, buff=.07)
        side = Line(vertices[0], vertices[1], color=INK, stroke_width=4)
        slab = self.eq("s", 32).next_to(side, UR, buff=.05)
        ap_dir = (side_mid - center) / np.linalg.norm(side_mid - center)
        side_dir = (vertices[1] - vertices[0]) / np.linalg.norm(vertices[1] - vertices[0])
        rmark = self.right_mark(side_mid, -ap_dir, side_dir, .20)
        one = Polygon(
            center,
            vertices[0],
            vertices[1],
            stroke_color=INK,
            stroke_width=3,
            fill_color=WHITE,
            fill_opacity=.82,
        )
        self.play(
            LaggedStart(*[Create(s) for s in spokes], lag_ratio=.05),
            Create(ap),
            Create(side),
            FadeIn(alab),
            FadeIn(slab),
            FadeIn(rmark),
            FadeIn(one),
            run_time=.85,
        )

        deriv = self._derivation_panel(
            [
                self.txt("All center triangles share height a", 25, True),
                self.eq(r"A=\frac12(s_1+s_2+\cdots+s_n)a", 36),
                self.eq(r"P=s_1+s_2+\cdots+s_n", 35),
                self.box(r"A=\frac{P\,a}{2}", 4.95, 52),
            ],
            center=RIGHT * 3.55 + DOWN * .28,
            width=5.90,
            height=3.45,
        )
        self.play(FadeIn(deriv[0]), run_time=.28)
        for item in deriv[1]:
            self.play(FadeIn(item, shift=UP * .025), run_time=.37)
            self.wait(.28)
        self.wait(.85)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), FadeOut(one), FadeOut(shortcut), run_time=.34)
        ex = self.example_stack(
            "Given: P = 30 cm, a = 4 cm",
            r"A=\frac{P\,a}{2}",
            r"A=\frac{(30)(4)}{2}",
            r"A=60\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80)
        self.wipe()
