#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle Exercises Workshop V3 — regions safe-frame correction."""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *
from Geometry8_Circle_V4_Senior_QA import V4_READ, V4_EXPLAIN, V4_SUMMARY
from Geometry8_Circle_Exercises_Workshop_20260824_V2 import Geometry8CircleExercisesWorkshop20260824V2


class Geometry8CircleExercisesWorkshop20260824V3(Geometry8CircleExercisesWorkshop20260824V2):
    """Full workshop with V2 opening + compact regions reference band."""

    # Protocol/static-QA markers inherited from the complete parent scene:
    # exercise_09_sector
    # self._v4_zoom
    # assert_content_safe

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()

    def circle_regions_reference(self) -> None:
        self._v4_header(
            8,
            "REGIONES DEL CÍRCULO",
            "La circunferencia es solamente el borde; semicírculos, cuadrantes, sectores y segmentos son regiones del círculo.",
        )
        centers = [
            np.array([-5.25, 0.55, 0]),
            np.array([-1.75, 0.55, 0]),
            np.array([1.75, 0.55, 0]),
            np.array([5.25, 0.55, 0]),
        ]
        r = 1.20

        semi = AnnularSector(
            inner_radius=0,
            outer_radius=r,
            angle=PI,
            start_angle=0,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).shift(centers[0])
        semi_label = self.text("SEMICÍRCULO", 29, BOLD).next_to(semi, DOWN, buff=0.22)

        quad = AnnularSector(
            inner_radius=0,
            outer_radius=r,
            angle=PI / 2,
            start_angle=0,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).shift(centers[1])
        quad_label = self.text("CUADRANTE", 29, BOLD).next_to(quad, DOWN, buff=0.22)

        sec = AnnularSector(
            inner_radius=0,
            outer_radius=r,
            angle=PI / 3,
            start_angle=0,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).shift(centers[2])
        sec_label = self.text("SECTOR", 29, BOLD).next_to(sec, DOWN, buff=0.22)

        seg_circle = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=4).move_to(centers[3])
        a1, a2 = 35 * DEGREES, 145 * DEGREES
        p1 = centers[3] + r * np.array([math.cos(a1), math.sin(a1), 0])
        p2 = centers[3] + r * np.array([math.cos(a2), math.sin(a2), 0])
        chord = Line(p1, p2, color=BLACK_LINE, stroke_width=4)
        seg_label = self.text("SEGMENTO", 29, BOLD).next_to(seg_circle, DOWN, buff=0.22)

        figures = VGroup(
            VGroup(semi, semi_label),
            VGroup(quad, quad_label),
            VGroup(sec, sec_label),
            VGroup(seg_circle, chord, seg_label),
        )

        # V3 correction: fixed-height summary band instead of the tall note panel.
        band_title = self.text("FRACCIÓN DEL CÍRCULO", 31, BOLD)
        band_formula = VGroup(
            self.math(r"\text{Semicírculo}=\frac12", 38),
            self.math(r"\text{Cuadrante}=\frac14", 38),
            self.math(r"\text{Sector}=\frac{\theta}{360^\circ}", 38),
        ).arrange(RIGHT, buff=0.75)
        band_content = VGroup(band_title, band_formula).arrange(DOWN, buff=0.16)
        self.fit(band_content, 11.8, 1.18)
        note = self._v4_panel(
            band_content,
            width=12.7,
            height=1.55,
            fill_color=PAPER_GRAY,
        ).move_to([0, -2.85, 0])

        self.assert_content_safe(VGroup(figures, note), "circle regions reference V3")

        for item in figures:
            animations = [Create(item[0])]
            if len(item) == 3:
                animations.append(Create(item[1]))
            animations.append(Write(item[-1]))
            self.play(*animations, run_time=RUN_NORMAL)
            self._v4_zoom(item, width=4.6, pause=V4_READ)

        self.play(Create(note[0]), FadeIn(note[1], shift=UP * 0.08), run_time=RUN_NORMAL)
        self._v4_zoom(note, width=13.1, pause=V4_EXPLAIN)
        self.wait(V4_SUMMARY)
        self.clear_stage()
