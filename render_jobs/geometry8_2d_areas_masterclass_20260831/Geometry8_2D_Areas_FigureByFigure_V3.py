#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — Figure-by-Figure Atlas V3.

Each figure follows the same student-facing sequence:
CONSTRUCT -> PARTS -> DERIVE -> EXAMPLE -> CHECK SQUARE UNITS.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
from manim import *

from Geometry8_2D_Areas_Masterclass_FINAL_QA import Geometry8Areas2DMasterclassFinalQA
from geometry8_area_atlas_helpers_v3 import Geometry8AreaAtlasHelpersMixin
from geometry8_area_atlas_basic_v3 import Geometry8AreaBasicFiguresMixin
from geometry8_area_atlas_quads_v3 import Geometry8AreaQuadrilateralFiguresMixin
from geometry8_area_atlas_circle_polygon_v3 import Geometry8AreaCirclePolygonMixin
from geometry8_area_atlas_circle_parts_v3 import Geometry8AreaCirclePartsMixin


class Geometry8Areas2DFigureByFigureV3(
    Geometry8AreaAtlasHelpersMixin,
    Geometry8AreaBasicFiguresMixin,
    Geometry8AreaQuadrilateralFiguresMixin,
    Geometry8AreaCirclePolygonMixin,
    Geometry8AreaCirclePartsMixin,
    Geometry8Areas2DMasterclassFinalQA,
):
    """Explicit construction, parts, derivation and worked example for all ten figures."""

    def validate_lesson_data(self):
        super().validate_lesson_data()
        assert 5**2 == 25
        assert 8 * 3 == 24
        assert 0.5 * 10 * 6 == 30
        assert 7 * 4 == 28
        assert ((10 + 6) * 4) / 2 == 32
        assert (12 * 8) / 2 == 48
        assert abs(math.pi * 4**2 - 50.2654824574) < 1e-8
        assert (30 * 4) / 2 == 60
        assert abs((math.pi * 6**2) / 2 - 56.5486677646) < 1e-8
        assert abs((math.pi * 8**2) / 4 - 50.2654824574) < 1e-8

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
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V3.py Geometry8Areas2DFigureByFigureV3 --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V3.py Geometry8Areas2DFigureByFigureV3 --disable_caching
