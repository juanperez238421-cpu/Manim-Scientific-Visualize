#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V9 POLYGON + CIRCLE QA.

Full-total lesson based on V8. It preserves every validated chapter and layout,
while overriding the circle derivation and polygon chapter for simpler Grade-8
visual logic and additional anti-overlap spacing.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT import Geometry8Areas2DFigureByFigureV8SeniorLayout
from geometry8_area_polygon_circle_v9 import Geometry8AreaPolygonCircleV9Mixin


class Geometry8Areas2DFigureByFigureV9PolygonCircleQA(
    Geometry8AreaPolygonCircleV9Mixin,
    Geometry8Areas2DFigureByFigureV8SeniorLayout,
):
    """Complete V8 curriculum with V9 student-first polygon/circle overrides."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V9_POLYGON_CIRCLE_QA.py Geometry8Areas2DFigureByFigureV9PolygonCircleQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V9_POLYGON_CIRCLE_QA.py Geometry8Areas2DFigureByFigureV9PolygonCircleQA --disable_caching
