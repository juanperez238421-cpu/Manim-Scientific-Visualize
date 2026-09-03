#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V8 TEXT-SAFE Senior QA FINAL.

V8 inherits the complete validated V7 lesson and applies a final text-collision
QA layer. Geometry, formulas, numerical examples and V5 parallelogram precision
remain unchanged.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V7_OVERLAP_FREE import Geometry8Areas2DFigureByFigureV7OverlapFree
from geometry8_area_text_safe_v8 import Geometry8AreaTextSafeV8Mixin


class Geometry8Areas2DFigureByFigureV8TextSafe(
    Geometry8AreaTextSafeV8Mixin,
    Geometry8Areas2DFigureByFigureV7OverlapFree,
):
    """Full Geometry 8 atlas with V8 text-safe Senior QA overrides."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V8_TEXT_SAFE.py Geometry8Areas2DFigureByFigureV8TextSafe --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V8_TEXT_SAFE.py Geometry8Areas2DFigureByFigureV8TextSafe --disable_caching
