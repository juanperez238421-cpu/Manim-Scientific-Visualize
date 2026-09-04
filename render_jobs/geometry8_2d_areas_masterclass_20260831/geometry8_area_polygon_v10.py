#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V10 common-polygon classroom QA.

V10 keeps the validated V9 circle correction and rebuilds only the polygon
chapter. The chapter now begins with a familiar house-shaped pentagon, uses a
clean rectangle + triangle decomposition, and keeps the regular-hexagon apothem
method afterward as an explicit shortcut for regular polygons.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaPolygonV10Mixin:
    """Overlap-free, student-first polygon chapter."""

    def regular_polygon_explicit(self):
        h = self.header(
            11,
            "8 · POLYGONS",
            "First decompose a familiar polygon; then learn the regular-polygon shortcut.",
        )
        strip = self.stage_strip()
        self.add(h, strip)

        # --------------------------------------------------------------
        # PART A — familiar pentagon (house shape)
        # --------------------------------------------------------------
        A = np.array([-5.85, -1.45, 0])
        B = np.array([-2.45, -1.45, 0])
        C = np.array([-2.45, .45, 0])
        D = np.array([-4.15, 1.78, 0])
        E = np.array([-5.85, .45, 0])
        house = Polygon(
            A, B, C, D, E,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.62,
        )

        self.mark_stage(strip, 0)
        self.play(Create(house), run_time=.78)
        familiar = self.txt("COMMON PENTAGON · 5 SIDES", 25, True)
        familiar.next_to(house, DOWN, buff=.24)
        self.play(FadeIn(familiar), run_time=.32)
        self.wait(.70)

        # The construction label disappears before dimensions are added.
        # This prevents the bottom dimension line from ever crossing text.
        self.mark_stage(strip, 1)
        self.play(FadeOut(familiar), run_time=.24)

        split = DashedLine(E, C, color=INK, stroke_width=2.7)
        roof_alt = DashedLine(D, np.array([D[0], C[1], 0]), color=MID, stroke_width=2.5)
        right = self.right_mark(np.array([D[0], C[1], 0]), RIGHT, UP, .23)

        base_dim = self.dimension(
            A + DOWN * .38,
            B + DOWN * .38,
            "6\,\mathrm{cm}",
            DOWN,
            28,
        )
        rect_h = self.dimension(
            A + LEFT * .36,
            E + LEFT * .36,
            "4\,\mathrm{cm}",
            LEFT,
            28,
        )

        # Keep the numeric height beside the central altitude. The triangle
        # name is placed above the roof, so no annotation shares the same zone.
        roof_h_label = self.eq("3\,\mathrm{cm}", 27)
        roof_h_label.next_to(roof_alt, RIGHT, buff=.15)
        roof_h_label.shift(DOWN * .06)

        rect_label = self.txt("RECTANGLE", 21, True).set_opacity(.66)
        rect_label.move_to([-4.15, -.58, 0])
        tri_label = self.txt("TRIANGLE", 20, True).set_opacity(.72)
        tri_label.next_to(D, UP, buff=.10)

        self.play(
            Create(split),
            Create(roof_alt),
            FadeIn(right),
            GrowFromCenter(base_dim[0]),
            FadeIn(base_dim[1]),
            GrowFromCenter(rect_h[0]),
            FadeIn(rect_h[1]),
            FadeIn(roof_h_label),
            FadeIn(rect_label),
            FadeIn(tri_label),
            run_time=.86,
        )
        self.wait(.55)

        simple_panel = self._safe_panel(5.80, 3.28, RIGHT * 3.55 + DOWN * .18)
        simple_body = VGroup(
            self.txt("DECOMPOSE INTO SHAPES YOU KNOW", 25, True),
            self.eq(r"A_{rectangle}=6(4)=24", 36),
            self.eq(r"A_{triangle}=\frac{6(3)}{2}=9", 36),
            self.box(r"A_{total}=24+9=33\ \mathrm{cm}^2", 5.14, 44),
        ).arrange(DOWN, buff=.22)
        self.fit(simple_body, 5.24, 2.70)
        simple_body.move_to(simple_panel)
        simple = VGroup(simple_panel, simple_body)

        self.play(FadeIn(simple_panel), run_time=.28)
        for item in simple_body:
            self.play(FadeIn(item, shift=UP * .025), run_time=.38)
            self.wait(.34)
        self.wait(1.10)

        # --------------------------------------------------------------
        # PART B — keep the regular-polygon method as a second idea.
        # --------------------------------------------------------------
        self.play(
            FadeOut(house),
            FadeOut(split),
            FadeOut(roof_alt),
            FadeOut(right),
            FadeOut(base_dim),
            FadeOut(rect_h),
            FadeOut(roof_h_label),
            FadeOut(rect_label),
            FadeOut(tri_label),
            FadeOut(simple),
            run_time=.46,
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
        center_dot = Dot(center, radius=.07, color=INK)
        shortcut = self.txt("REGULAR HEXAGON · APOTHEM SHORTCUT", 24, True)
        shortcut.move_to(RIGHT * 3.45 + UP * 1.18)

        self.play(Create(poly), FadeIn(center_dot), FadeIn(shortcut), run_time=.74)
        self.wait(.50)

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
            run_time=.86,
        )
        self.wait(.35)

        # Clear the shortcut heading before the derivation panel occupies the
        # same right-side teaching zone.
        self.play(FadeOut(shortcut), run_time=.25)

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
        self.wait(.90)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), FadeOut(one), run_time=.34)
        ex = self.example_stack(
            "Given: P = 30 cm, a = 4 cm",
            r"A=\frac{P\,a}{2}",
            r"A=\frac{(30)(4)}{2}",
            r"A=60\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80)
        self.wipe()
