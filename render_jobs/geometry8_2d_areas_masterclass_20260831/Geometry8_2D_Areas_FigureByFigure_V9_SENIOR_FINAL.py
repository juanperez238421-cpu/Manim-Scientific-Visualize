#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V9 SENIOR FINAL.

Full V8 layout-safe curriculum plus the final rendered-frame corrections for the
circle derivation and the two-page formula guide.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT_SAFE import (
    Geometry8Areas2DFigureByFigureV8SeniorLayoutSafe,
)
from geometry8_area_senior_final_v9 import Geometry8AreaSeniorFinalV9Mixin


class Geometry8Areas2DFigureByFigureV9SeniorFinal(
    Geometry8AreaSeniorFinalV9Mixin,
    Geometry8Areas2DFigureByFigureV8SeniorLayoutSafe,
):
    """Complete lesson with senior spatial QA through V9."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V9_SENIOR_FINAL.py Geometry8Areas2DFigureByFigureV9SeniorFinal --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V9_SENIOR_FINAL.py Geometry8Areas2DFigureByFigureV9SeniorFinal --disable_caching
