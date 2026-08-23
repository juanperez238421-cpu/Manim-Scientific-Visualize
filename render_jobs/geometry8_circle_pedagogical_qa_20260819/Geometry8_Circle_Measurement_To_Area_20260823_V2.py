#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior visual-QA patch for the measurement-to-area lesson.

V2 preserves the complete pedagogical sequence from
Geometry8CircleMeasurementArea20260823 and applies projector/safe-frame QA:
- all area sectors share one geometric center;
- lower note/formula panels stay inside the JP content-safe zone.
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

    def boundary_vs_surface(self) -> None:
        self.set_header(
            5,
            "THE NEXT QUESTION: AROUND OR INSIDE?",
            "Circumference measures the boundary; area measures the region covered by the circle.",
        )

        left_circle = Circle(radius=1.45, stroke_color=BLACK_LINE, stroke_width=7)
        left_title = self.text("BOUNDARY LENGTH", 29, BOLD)
        left_unit = self.math(r"C\;\rightarrow\;\text{cm, m, ...}", 34)
        left = VGroup(left_title, left_circle, left_unit).arrange(DOWN, buff=0.26)

        right_circle = Circle(
            radius=1.45,
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.72,
        )
        right_title = self.text("COVERED REGION", 29, BOLD)
        right_unit = self.math(r"A\;\rightarrow\;\text{cm}^2,\text{ m}^2, ...", 34)
        right = VGroup(right_title, right_circle, right_unit).arrange(DOWN, buff=0.26)

        comparison = VGroup(left, right).arrange(RIGHT, buff=2.20).move_to(DOWN * 0.30)
        question = self.note_panel(
            "BEFORE CALCULATING",
            ["Ask: am I measuring the edge, or covering the inside?"],
            width=9.2,
            title_size=27,
            body_size=25,
            max_text_height=1.12,
        ).to_edge(DOWN, buff=0.58)

        group = VGroup(comparison, question)
        self.assert_content_safe(group, "boundary versus surface V2")
        self.play(FadeIn(left), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(right), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

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
        ).to_edge(DOWN, buff=0.58)

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

    def lesson_summary(self) -> None:
        self.set_header(
            9,
            "METHOD MAP — FROM A REAL OBJECT TO AREA",
            "Use this route with any of the three objects you measured at home.",
        )

        route = self.process_map(
            [
                ("1", "MEASURE d AND C"),
                ("2", "CALCULATE C / d"),
                ("3", "RECOGNIZE pi"),
                ("4", "FIND r = d / 2"),
                ("5", "CHOOSE C OR A"),
                ("6", "CHECK THE UNITS"),
            ],
            columns=3,
        )
        self.fit(route, 13.2, 3.25)
        route.move_to(UP * 0.22)

        extension = self.note_panel(
            "USE YOUR OWN DATA",
            [
                "Pick one of your three objects.",
                "Use its measured diameter to predict C and calculate A.",
                "Compare predicted C with the circumference you actually measured.",
            ],
            width=10.8,
            title_size=28,
            body_size=25,
            max_text_height=1.90,
        ).to_edge(DOWN, buff=0.58)

        group = VGroup(route, extension)
        self.assert_content_safe(group, "lesson summary V2")
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.8,
        )
        self.wait(PAUSE_WORK)
        self.play(FadeIn(extension), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing(
            "Measure the circle. Discover pi. Decide: boundary or surface. Then calculate."
        )


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
