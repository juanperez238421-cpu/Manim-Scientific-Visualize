#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V11 EXPLICIT POLYGON QA.

Full-total lesson based on V10.  All previously validated chapters, including
the V9 circle-spacing correction, are preserved.  Only the polygon chapter is
replaced by the V11 single-story regular-hexagon derivation.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V10_STUDENT_POLYGON_QA import Geometry8Areas2DFigureByFigureV10StudentPolygonQA
from geometry8_area_polygon_v11 import Geometry8AreaPolygonV11Mixin


class Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA(
    Geometry8AreaPolygonV11Mixin,
    Geometry8Areas2DFigureByFigureV10StudentPolygonQA,
):
    """Complete V10 curriculum with the rebuilt explicit V11 polygon chapter."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V11_EXPLICIT_POLYGON_QA.py Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V11_EXPLICIT_POLYGON_QA.py Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA --disable_caching
