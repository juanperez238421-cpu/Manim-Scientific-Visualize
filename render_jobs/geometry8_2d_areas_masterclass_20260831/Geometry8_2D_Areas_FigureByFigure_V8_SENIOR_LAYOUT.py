#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V8 SENIOR LAYOUT QA.

V8 inherits the complete V7 lesson, keeps the validated fixed-grid worked
examples, and replaces only the remaining collision-prone layouts identified
through frame-by-frame visual QA.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V7_OVERLAP_FREE import Geometry8Areas2DFigureByFigureV7OverlapFree
from geometry8_area_senior_layout_v8 import Geometry8AreaSeniorLayoutV8Mixin


class Geometry8Areas2DFigureByFigureV8SeniorLayout(
    Geometry8AreaSeniorLayoutV8Mixin,
    Geometry8Areas2DFigureByFigureV7OverlapFree,
):
    """Full V7 curriculum with V8 senior collision-free layout overrides."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT.py Geometry8Areas2DFigureByFigureV8SeniorLayout --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT.py Geometry8Areas2DFigureByFigureV8SeniorLayout --disable_caching
