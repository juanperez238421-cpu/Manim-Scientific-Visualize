#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL3 human-QA patch for Geometry 8 Circle Exercises.

FINAL2 passed the automated protocol, but dense human frame inspection exposed
formula collisions in the semicircle and quarter-circle deduction scenes.
FINAL3 rebuilds those two scenes with explicit equation panels, isolated reveals
and projector-safe gaps.  All other validated exercise scenes remain unchanged.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL2 import (
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal2,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import PAPER, MID_GRAY


class Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal3(
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal2
):
    """Human-QA final: collision-free fractional-area deduction scenes."""

    def _formula_stack_panel(
        self,
        formulas: list[Mobject],
        center,
        width: float = 5.7,
        height: float = 2.75,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=PAPER,
            fill_opacity=1.0,
        ).move_to(center)
        stack = VGroup(*formulas).arrange(DOWN, buff=0.42)
        if stack.width > width - 0.50:
            stack.scale_to_fit_width(width - 0.50)
        if stack.height > height - 0.42:
            stack.scale_to_fit_height(height - 0.42)
        stack.move_to(box)
        return VGroup(box, stack)

    def derive_semicircle_area(self) -> None:
        h = self.workshop_header(
            6,
            "DEDUCE THE AREA OF A SEMICIRCLE",
            "A semicircle is exactly one half of the full circular region.",
        )
        self.add(h)

        full = self.circle_metrics_diagram(
            radius=1.47,
            center=np.array([-4.75, -0.30, 0]),
            show_radius=True,
        )
        half = self.circle_metrics_diagram(
            radius=1.47,
            center=np.array([-1.25, -0.30, 0]),
            show_radius=True,
            shade_fraction=0.5,
        )
        full_lab = self.text("FULL CIRCLE", 30, BOLD).next_to(full, DOWN, buff=0.18)
        half_lab = self.text("ONE HALF", 30, BOLD).next_to(half, DOWN, buff=0.18)

        arrow = Arrow(
            [0.45, -0.30, 0], [1.35, -0.30, 0],
            buff=0.0, color=BLACK, stroke_width=3.0,
        )
        question = self.math(r"A_{1/2}=?", 56).move_to([3.05, -0.30, 0])

        source_group = VGroup(h, full, half, full_lab, half_lab, arrow, question)
        self.projector_safe(source_group, "FINAL3 semicircle source layout")

        self.play(FadeIn(full), FadeIn(full_lab), run_time=0.90)
        self.wait(1.15)
        self.play(FadeIn(half), FadeIn(half_lab), run_time=0.90)
        self.wait(1.05)
        self.play(GrowArrow(arrow), Write(question), run_time=0.85)
        self.think_pause(4.9)

        self.play(FadeOut(question), FadeOut(arrow), run_time=0.55)
        self.wait(0.45)

        eq1 = self.math(r"A_{1/2}=\frac{1}{2}A_{\text{circle}}", 47)
        eq2 = self.math(r"A_{1/2}=\frac{1}{2}\pi r^2", 56)
        panel = self._formula_stack_panel(
            [eq1, eq2], center=[4.25, -0.35, 0], width=5.65, height=2.90
        )
        self.projector_safe(panel, "FINAL3 semicircle formula panel")

        self.play(FadeIn(panel[0], shift=LEFT * 0.06), run_time=0.65)
        self.play(FadeIn(eq1, shift=RIGHT * 0.06), run_time=0.78)
        self.wait(1.35)
        self.play(FadeIn(eq2, shift=RIGHT * 0.06), run_time=0.82)
        self.play(Circumscribe(eq2, color=MID_GRAY, time_width=0.85), run_time=1.10)
        self.wait(5.2)
        self.clear_stage(VGroup(h, full, half, full_lab, half_lab, panel))

    def derive_quarter_circle_area(self) -> None:
        h = self.workshop_header(
            8,
            "DEDUCE THE AREA OF A QUARTER CIRCLE",
            "Four equal quarters reconstruct one complete circle.",
        )
        self.add(h)

        full = self.circle_metrics_diagram(
            radius=1.43,
            center=np.array([-4.75, -0.15, 0]),
            show_radius=True,
        )
        quarter = self.circle_metrics_diagram(
            radius=1.43,
            center=np.array([-1.30, -0.15, 0]),
            show_radius=True,
            shade_fraction=0.25,
        )
        full_lab = self.text("FULL CIRCLE", 29, BOLD).next_to(full, DOWN, buff=0.17)
        quarter_lab = self.text("ONE OF FOUR", 29, BOLD).next_to(quarter, DOWN, buff=0.17)
        four_note = self.text("4 equal quarters = 1 full circle", 29, BOLD).move_to([-3.0, -2.72, 0])

        visual_group = VGroup(h, full, quarter, full_lab, quarter_lab, four_note)
        self.projector_safe(visual_group, "FINAL3 quarter visual layout")

        self.play(FadeIn(full), FadeIn(full_lab), run_time=0.85)
        self.wait(1.05)
        self.play(FadeIn(quarter), FadeIn(quarter_lab), run_time=0.90)
        self.play(FadeIn(four_note, shift=UP * 0.05), run_time=0.70)
        self.think_pause(4.8)

        eq1 = self.math(r"A_{1/4}=\frac{1}{4}A_{\text{circle}}", 46)
        eq2 = self.math(r"A_{1/4}=\frac{1}{4}\pi r^2", 55)
        panel = self._formula_stack_panel(
            [eq1, eq2], center=[4.22, 0.10, 0], width=5.70, height=2.70
        )

        example_box = RoundedRectangle(
            width=6.05,
            height=1.15,
            corner_radius=0.13,
            stroke_color=BLACK,
            stroke_width=2.0,
            fill_color=PAPER,
            fill_opacity=1.0,
        ).move_to([4.22, -2.38, 0])
        example = self.math(
            r"r=12\Rightarrow A_{1/4}=\frac14\pi(12)^2=36\pi", 43
        )
        if example.width > 5.62:
            example.scale_to_fit_width(5.62)
        example.move_to(example_box)
        example_group = VGroup(example_box, example)

        self.projector_safe(panel, "FINAL3 quarter formula panel")
        self.projector_safe(example_group, "FINAL3 quarter example panel")
        vertical_gap = panel.get_bottom()[1] - example_group.get_top()[1]
        if vertical_gap < 0.20:
            raise ValueError(f"FINAL3 quarter panels too close: gap={vertical_gap:.3f}")

        self.play(FadeIn(panel[0], shift=LEFT * 0.06), run_time=0.65)
        self.play(FadeIn(eq1, shift=RIGHT * 0.06), run_time=0.78)
        self.wait(1.25)
        self.play(FadeIn(eq2, shift=RIGHT * 0.06), run_time=0.82)
        self.play(Circumscribe(eq2, color=MID_GRAY, time_width=0.85), run_time=1.10)
        self.wait(1.55)
        self.play(FadeIn(example_group, shift=UP * 0.06), run_time=0.82)
        self.wait(5.2)
        self.clear_stage(VGroup(h, full, quarter, full_lab, quarter_lab, four_note, panel, example_group))


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL3.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal3 --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL3.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal3 --disable_caching
