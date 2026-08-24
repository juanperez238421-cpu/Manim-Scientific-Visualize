#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle Exercises Workshop V2 — safe opening correction."""
from __future__ import annotations

import numpy as np
from manim import *
from jp_classroom_style import *
from Geometry8_Circle_V4_Senior_QA import V4_READ, V4_EXPLAIN, V4_SUMMARY
from Geometry8_Circle_Exercises_Workshop_20260824 import Geometry8CircleExercisesWorkshop20260824


class Geometry8CircleExercisesWorkshop20260824V2(Geometry8CircleExercisesWorkshop20260824):
    """Same full workshop with an audited safe-frame opening."""

    # QA markers inherited from the parent implementation:
    # exercise_09_sector
    # assert_content_safe

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()

    def opening_workshop(self) -> None:
        course = self.text("GEOMETRÍA 8", 34, BOLD)
        title = self.text("TALLER ANIMADO — CÍRCULO Y REGIONES", 54, BOLD)
        subtitle = self.text(
            "Radio, diámetro, perímetro, área completa y regiones del círculo — ejercicio por ejercicio.",
            32,
        )
        # Critical V2 correction: constrain both title and subtitle before grouping.
        self.fit(title, 13.70, 0.82)
        self.fit(subtitle, 13.55, 0.76)

        center = np.array([-3.70, -0.65, 0.0])
        circle = Circle(radius=1.85, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        center_dot = Dot(center, radius=0.075, color=BLACK_LINE)
        radius = Line(center, center + RIGHT * 1.85, color=BLACK_LINE, stroke_width=5)
        diameter = Line(center + LEFT * 1.85, center + RIGHT * 1.85, color=LIGHT_GRAY, stroke_width=3)

        cards = VGroup(
            self._v4_formula_panel(r"d=2r", width=4.1, height=1.18, size=58),
            self._v4_formula_panel(r"C=\pi d=2\pi r", width=5.5, height=1.18, size=50),
            self._v4_formula_panel(r"A=\pi r^2", width=4.8, height=1.18, size=58),
        ).arrange(DOWN, buff=0.30).move_to([3.45, -0.55, 0])

        top = VGroup(course, title, subtitle).arrange(DOWN, buff=0.25).move_to(UP * 2.15)
        group = VGroup(top, circle, center_dot, radius, diameter, cards)
        self.assert_within_frame(group, "workshop V2 opening", margin=0.16)

        self.play(FadeIn(course, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW * 1.25)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.wait(V4_READ)
        self.play(Create(circle), FadeIn(center_dot), run_time=RUN_NORMAL)
        self.play(GrowFromPoint(radius, center), Create(diameter), run_time=RUN_NORMAL)
        for card in cards:
            self.play(Create(card[0]), Write(card[1]), run_time=RUN_NORMAL)
            self.wait(V4_READ)
        self._v4_zoom(VGroup(circle, radius, diameter), width=6.4, pause=V4_EXPLAIN)
        self.wait(V4_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)
