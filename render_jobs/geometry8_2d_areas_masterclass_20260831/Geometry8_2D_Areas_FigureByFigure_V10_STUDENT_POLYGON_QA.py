#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V10 STUDENT POLYGON QA.

Full-total lesson based on V9. The V9 collision-free circle derivation is kept,
while the polygon chapter is replaced by the cleaner V10 familiar-pentagon
lesson followed by the retained regular-hexagon apothem shortcut.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V9_POLYGON_CIRCLE_QA import Geometry8Areas2DFigureByFigureV9PolygonCircleQA
from geometry8_area_polygon_v10 import Geometry8AreaPolygonV10Mixin


class Geometry8Areas2DFigureByFigureV10StudentPolygonQA(
    Geometry8AreaPolygonV10Mixin,
    Geometry8Areas2DFigureByFigureV9PolygonCircleQA,
):
    """Complete V9 curriculum with the final overlap-free V10 polygon chapter."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V10_STUDENT_POLYGON_QA.py Geometry8Areas2DFigureByFigureV10StudentPolygonQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V10_STUDENT_POLYGON_QA.py Geometry8Areas2DFigureByFigureV10StudentPolygonQA --disable_caching
