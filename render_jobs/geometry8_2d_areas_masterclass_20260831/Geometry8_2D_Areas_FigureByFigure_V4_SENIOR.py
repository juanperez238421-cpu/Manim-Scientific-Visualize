#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — Senior V4.

Senior QA revision of the complete V3 atlas. The lesson data, formulas, examples,
and chapter order are preserved; presentation hierarchy and geometric clarity are
refined, especially for circle-sector rearrangement and circle fractions.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V3 import Geometry8Areas2DFigureByFigureV3
from geometry8_area_atlas_senior_v4 import Geometry8AreaSeniorV4Mixin


class Geometry8Areas2DFigureByFigureV4Senior(
    Geometry8AreaSeniorV4Mixin,
    Geometry8Areas2DFigureByFigureV3,
):
    """Full V3 curriculum with senior visual/geometry refinements."""

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
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V4_SENIOR.py Geometry8Areas2DFigureByFigureV4Senior --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V4_SENIOR.py Geometry8Areas2DFigureByFigureV4Senior --disable_caching
