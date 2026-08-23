#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior visual-QA patch for the measurement-to-area lesson.

V2 preserves the complete pedagogical sequence from
Geometry8CircleMeasurementArea20260823 and corrects the sector construction in
the area derivation: every sector is translated from the same geometric origin,
so all wedges share one circle center.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Measurement_To_Area_20260823 import (
    Geometry8CircleMeasurementArea20260823,
)
from jp_classroom_style import *


class Geometry8CircleMeasurementArea20260823V2(
    Geometry8CircleMeasurementArea20260823
):
    """Final visual-QA revision of the measurement-to-area lesson."""

    def derive_area_visually(self) -> None:
        self.set_header(
            6,
            "WHY DOES THE AREA FORMULA CONTAIN pi?",
            "Slice the circle into many thin sectors and rearrange them into an almost-rectangle.",
        )

        r = 1.65
        center = np.array([-3.85, -0.35, 0.0])
        sectors = VGroup()
        n = 16
        for i in range(n):
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=TAU / n,
                start_angle=i * TAU / n,
                stroke_color=BLACK_LINE,
                stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1.0,
            ).shift(center)
            sectors.add(sector)

        radius_line = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=3)
        radius_label = self.math("r", 34).next_to(radius_line, UP, buff=0.08)
        sliced = VGroup(sectors, radius_line, radius_label)

        arrow = Arrow(LEFT * 0.2, RIGHT * 1.2, color=BLACK_LINE, stroke_width=3, buff=0)
        arrow.move_to([0.0, -0.25, 0])

        almost_rect = Polygon(
            [-2.65, -1.10, 0],
            [2.45, -1.10, 0],
            [2.75, 1.10, 0],
            [-2.35, 1.10, 0],
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.85,
        ).scale(0.84).move_to([3.75, -0.25, 0])

        teeth = VGroup()
        top_y = almost_rect.get_top()[1]
        bottom_y = almost_rect.get_bottom()[1]
        x0 = almost_rect.get_left()[0] + 0.35
        x1 = almost_rect.get_right()[0] - 0.35
        xs = np.linspace(x0, x1, 10)
        for x in xs:
            teeth.add(
                Line(
                    [x, bottom_y, 0],
                    [x + 0.18, top_y, 0],
                    color=LIGHT_GRAY,
                    stroke_width=1.5,
                )
            )

        base_label = self.math(r"\text{base}\approx\pi r", 32).next_to(
            almost_rect, DOWN, buff=0.16
        )
        height_line = DoubleArrow(
            almost_rect.get_right() + RIGHT * 0.22 + DOWN * 0.78,
            almost_rect.get_right() + RIGHT * 0.22 + UP * 0.78,
            color=BLACK_LINE,
            stroke_width=2.2,
            buff=0.0,
            tip_length=0.12,
        )
        height_label = self.math("r", 32).next_to(height_line, RIGHT, buff=0.10)
        rearranged = VGroup(almost_rect, teeth, base_label, height_line, height_label)

        formula = self.formula_panel(
            r"A\approx (\pi r)(r)\quad\Longrightarrow\quad A=\pi r^2",
            width=9.3,
            height=1.12,
            font_size=40,
        ).to_edge(DOWN, buff=0.42)

        group = VGroup(sliced, arrow, rearranged, formula)
        self.assert_content_safe(group, "area derivation V2")
        self.play(FadeIn(sliced), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(GrowArrow(arrow), run_time=RUN_NORMAL)
        self.play(FadeIn(rearranged), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()


# Preview QA:
# LESSON_TIME_SCALE=0.08 manim -pql \
#   Geometry8_Circle_Measurement_To_Area_20260823_V2.py \
#   Geometry8CircleMeasurementArea20260823V2 \
#   --fps 15 --disable_caching
#
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh \
#   Geometry8_Circle_Measurement_To_Area_20260823_V2.py \
#   Geometry8CircleMeasurementArea20260823V2 \
#   --fps 30 --disable_caching
