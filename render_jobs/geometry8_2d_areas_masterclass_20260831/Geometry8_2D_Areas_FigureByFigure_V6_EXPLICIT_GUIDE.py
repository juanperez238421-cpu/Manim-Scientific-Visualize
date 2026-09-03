#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V6 Explicit Guide Senior.

Preserves the validated V5 lesson and adds explicit numbering, slower worked
examples, a two-screen visual formula guide, and a numbered final method.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V5_SENIOR import Geometry8Areas2DFigureByFigureV5Senior
from geometry8_area_explicit_steps_v6 import Geometry8AreaExplicitGuideV6Mixin


class Geometry8Areas2DFigureByFigureV6ExplicitGuide(
    Geometry8AreaExplicitGuideV6Mixin,
    Geometry8Areas2DFigureByFigureV5Senior,
):
    """Full V5 curriculum with explicit Grade-8 step sequencing and guide."""

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
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V6_EXPLICIT_GUIDE.py Geometry8Areas2DFigureByFigureV6ExplicitGuide --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V6_EXPLICIT_GUIDE.py Geometry8Areas2DFigureByFigureV6ExplicitGuide --disable_caching
