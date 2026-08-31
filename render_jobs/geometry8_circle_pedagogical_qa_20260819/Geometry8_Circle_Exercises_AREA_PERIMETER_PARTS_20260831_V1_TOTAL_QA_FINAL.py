#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL projector-fit patch for Geometry 8 Circle Exercises V1."""

from __future__ import annotations

from manim import *

from Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA import (
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQA,
)


class Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal(
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQA
):
    """Preserve V10/V1 animation logic while enforcing opening safe-width margins."""

    def opening_workshop(self) -> None:
        title = self.text("CIRCLE WORKSHOP", 66, BOLD)
        subtitle = self.text(
            "AREA • PERIMETER • RADIUS • DIAMETER • FRACTIONAL REGIONS", 36, BOLD
        )
        note = self.text(
            "No arc length — focus on formulas, inverse reasoning and circle parts", 32
        )
        for mob in (title, subtitle, note):
            if mob.width > 14.55:
                mob.scale_to_fit_width(14.55)

        formula = self.big_formula(
            r"A=\pi r^2\qquad P=2\pi r=\pi d", 10.4, 62
        )
        group = VGroup(title, subtitle, note, formula).arrange(DOWN, buff=0.45)
        self.projector_safe(group, "circle exercises opening final")

        self.play(Write(title), run_time=1.35)
        self.wait(0.70)
        self.play(FadeIn(subtitle, shift=UP * 0.08), run_time=0.85)
        self.wait(0.65)
        self.play(FadeIn(note, shift=UP * 0.06), run_time=0.80)
        self.wait(0.70)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.90)
        self.wait(4.8)
        self.clear_stage(group)


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal --disable_caching
