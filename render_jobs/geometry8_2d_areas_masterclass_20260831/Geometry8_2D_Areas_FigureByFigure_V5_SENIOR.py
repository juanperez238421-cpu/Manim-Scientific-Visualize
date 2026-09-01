#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — Senior V5.

V5 preserves the complete accepted V4 lesson and applies one precision correction
to the parallelogram cut-and-translate construction so the translated triangular
piece fits the final rectangle exactly in both geometry and rendered linework.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V3 import Geometry8Areas2DFigureByFigureV3
from geometry8_area_atlas_senior_v4 import Geometry8AreaSeniorV4Mixin
from geometry8_area_parallelogram_precision_v5 import Geometry8ParallelogramPrecisionV5Mixin


class Geometry8Areas2DFigureByFigureV5Senior(
    Geometry8ParallelogramPrecisionV5Mixin,
    Geometry8AreaSeniorV4Mixin,
    Geometry8Areas2DFigureByFigureV3,
):
    """Full V4 senior curriculum plus the exact parallelogram V5 correction."""

    def construct(self):
        self.atlas_opening()
        self.area_vs_perimeter()
        self.unit_squares()
        self.square_explicit()
        self.rectangle_explicit()
        self.triangle_explicit()
        self.parallelogram_explicit()
        self.trapezoid_explicit()
        self.rhombus_explicit()
        self.circle_explicit()
        self.regular_polygon_explicit()
        self.semicircle_explicit()
        self.quarter_circle_explicit()
        self.formula_atlas()
        self.final_method()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V5_SENIOR.py Geometry8Areas2DFigureByFigureV5Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V5_SENIOR.py Geometry8Areas2DFigureByFigureV5Senior --disable_caching
