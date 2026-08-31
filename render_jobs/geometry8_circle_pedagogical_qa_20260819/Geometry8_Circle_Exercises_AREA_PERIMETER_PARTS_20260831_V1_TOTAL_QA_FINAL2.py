#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL2 compatibility patch for Geometry 8 Circle Exercises V1.

Fixes fractional-region construction for ManimCE 0.20.1 while preserving the
projector-fit opening and the complete V10-derived workshop timeline.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL import (
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import LIGHT_GRAY


class Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal2(
    Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal
):
    """ManimCE-0.20.1-safe fractional circles with geometric-center alignment."""

    def circle_metrics_diagram(
        self,
        radius: float = 1.55,
        center: np.ndarray = np.array([-3.9, -0.35, 0.0]),
        show_radius: bool = True,
        show_diameter: bool = False,
        shade_fraction: float | None = None,
    ) -> VGroup:
        center = np.array(center, dtype=float)
        circle = Circle(radius=radius, color=BLACK, stroke_width=3.0).move_to(center)
        dot = Dot(center, radius=0.055, color=BLACK)
        items = [circle, dot]

        if shade_fraction is not None:
            if not (0.0 < float(shade_fraction) <= 1.0):
                raise ValueError(f"shade_fraction must be in (0, 1], got {shade_fraction}")
            angle = TAU * float(shade_fraction)
            # ManimCE 0.20.1 Sector takes `radius`; passing outer_radius causes
            # a duplicate AnnularSector keyword.  Build at ORIGIN and shift so
            # the sector's true arc center stays exactly concentric with circle.
            sector = Sector(
                radius=radius,
                angle=angle,
                start_angle=0,
                fill_color=LIGHT_GRAY,
                fill_opacity=0.48,
                stroke_color=BLACK,
                stroke_width=2.0,
            ).shift(center)
            items.insert(0, sector)

        if show_radius:
            rline = Line(center, center + RIGHT * radius, color=BLACK, stroke_width=3.2)
            rlab = self.math("r", 50).next_to(rline, UP, buff=0.08)
            items.extend([rline, rlab])

        if show_diameter:
            dline = Line(
                center + LEFT * radius,
                center + RIGHT * radius,
                color=BLACK,
                stroke_width=3.2,
            )
            dlab = self.math("d", 50).next_to(dline, DOWN, buff=0.12)
            items.extend([dline, dlab])

        group = VGroup(*items)
        # Geometry-only guard: each diagram must remain compact enough to share
        # the slide with worked equations without pushing content to the edges.
        if group.width > 4.35 or group.height > 4.25:
            raise ValueError(
                f"FINAL2 circle diagram unexpectedly large: width={group.width:.3f}, height={group.height:.3f}"
            )
        return group


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL2.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal2 --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA_FINAL2.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQAFinal2 --disable_caching
