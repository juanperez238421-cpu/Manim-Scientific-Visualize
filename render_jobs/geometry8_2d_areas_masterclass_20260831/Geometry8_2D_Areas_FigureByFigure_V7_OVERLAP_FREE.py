#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V7 OVERLAP-FREE Senior QA.

V7 preserves the complete V6 lesson and replaces only the worked-example layout
with a fixed-row composition validated for 1920x1080 projector output.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V6_EXPLICIT_GUIDE import Geometry8Areas2DFigureByFigureV6ExplicitGuide
from geometry8_area_overlap_free_v7 import Geometry8AreaOverlapFreeV7Mixin


class Geometry8Areas2DFigureByFigureV7OverlapFree(
    Geometry8AreaOverlapFreeV7Mixin,
    Geometry8Areas2DFigureByFigureV6ExplicitGuide,
):
    """Full V6 curriculum with Senior-QA overlap-free worked examples."""

    def construct(self):
        # Keep the validated V6 chapter sequence exactly intact.
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V7_OVERLAP_FREE.py Geometry8Areas2DFigureByFigureV7OverlapFree --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V7_OVERLAP_FREE.py Geometry8Areas2DFigureByFigureV7OverlapFree --disable_caching
