#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V8 SENIOR QA — FINAL2.

Runtime correction discovered by the strict V8 PQL gate:
Step 04 row labels were large enough to reach x=-7.970.  This version keeps the
31 pt projector typography but moves the labels inward so the true safe margin
is respected.  Every other V8 senior-QA correction remains unchanged.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal2(
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal
):
    """Final V8 scene with Step 04 horizontal-safe large labels."""

    def step_4_two_separate_rows_from_halves(self) -> None:
        h = self.header(
            4,
            "FORM TWO SEPARATE ROWS — ONE ROW FROM EACH HALF",
            "Do not combine them yet. Build the two rows independently, then measure each row without overlapping labels.",
        )
        self.add(h)

        n_total = 24
        source_r = 1.60
        source_center = np.array([0.0, -0.20, 0.0])
        _, right_source, left_source = self.vertical_half_sectors(
            n_total, source_r, source_center
        )
        right_source.shift(RIGHT * 0.34)
        left_source.shift(LEFT * 0.34)

        source_r_lab = self.text("RIGHT HALF", 29, BOLD).move_to([2.90, 1.72, 0])
        source_l_lab = self.text("LEFT HALF", 29, BOLD).move_to([-2.90, 1.72, 0])

        row_r = 1.70
        top_y, bottom_y = 0.48, -0.48
        row1, row2 = self.half_row_targets(n_total, row_r, top_y, bottom_y)
        top_arcs, bottom_arcs = self.half_row_arc_overlays(
            n_total, row_r, top_y, bottom_y
        )
        measures = self.row_measurements_from_halves(
            row1, row2, row_r, top_y, bottom_y
        )

        # V8 FINAL2 correction: preserve the requested 31 pt size but move the
        # ownership labels inward. The previous center x=-5.55 produced a
        # measured left edge at -7.970 under ManimCE 0.20.1.
        row1_lab = self.text("ROW 1 — RIGHT HALF", 31, BOLD).move_to([-5.00, 1.02, 0])
        row2_lab = self.text("ROW 2 — LEFT HALF", 31, BOLD).move_to([-5.00, -1.02, 0])

        group = VGroup(
            h, right_source, left_source, source_r_lab, source_l_lab,
            row1, row2, top_arcs, bottom_arcs, measures, row1_lab, row2_lab,
        )
        self.projector_safe(group, "v8 final2 step4")

        self.play(
            FadeIn(right_source), FadeIn(left_source),
            FadeIn(source_r_lab), FadeIn(source_l_lab),
            run_time=1.00,
        )
        self.wait(1.5)

        self.play(
            AnimationGroup(
                *[Transform(right_source[j], row1[j]) for j in range(n_total // 2)],
                lag_ratio=0.050,
            ),
            FadeOut(source_r_lab),
            FadeIn(row1_lab, shift=RIGHT * 0.08),
            run_time=2.45,
            rate_func=smooth,
        )
        self.wait(1.7)

        self.play(
            AnimationGroup(
                *[Transform(left_source[j], row2[j]) for j in range(n_total // 2)],
                lag_ratio=0.050,
            ),
            FadeOut(source_l_lab),
            FadeIn(row2_lab, shift=RIGHT * 0.08),
            run_time=2.45,
            rate_func=smooth,
        )
        self.wait(2.0)

        self.play(
            LaggedStart(*[Create(a) for a in top_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[0]), Write(measures[1]),
            GrowFromCenter(measures[4]), Write(measures[5]),
            run_time=1.25,
        )
        self.wait(2.8)

        self.play(
            LaggedStart(*[Create(a) for a in bottom_arcs], lag_ratio=0.055),
            run_time=1.30,
        )
        self.play(
            GrowFromCenter(measures[2]), Write(measures[3]),
            GrowFromCenter(measures[6]), Write(measures[7]),
            run_time=1.25,
        )
        self.wait(3.6)

        # Remove the measurement layer before the checkpoint. This is an
        # intentional temporal-layout fix: the old V7 frame visually merged the
        # lower P/2 marker with the checkpoint copy.
        self.play(
            FadeOut(top_arcs), FadeOut(bottom_arcs), FadeOut(measures),
            run_time=0.80,
        )
        checkpoint = self.big_formula(
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}",
            10.5,
            43,
        ).move_to([0.0, -3.04, 0])
        self.projector_safe(checkpoint, "v8 final2 step4 checkpoint")
        self.play(FadeIn(checkpoint, shift=UP * 0.08), run_time=0.95)
        self.wait(4.6)

        self.clear_stage(
            VGroup(h, right_source, left_source, row1_lab, row2_lab, checkpoint)
        )


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL2.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal2 --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL2.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal2 --disable_caching
