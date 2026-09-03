#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V8 Senior Layout Safe.

Direct rendered-frame QA successor to V7 OVERLAP FREE.  V8 keeps the complete
V7 curriculum and mathematics while applying a stronger spatial-layout layer to
all worked examples and the specific figure / derivation scenes that still had
visible text collisions in the delivered PQH video.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V7_OVERLAP_FREE import (
    Geometry8Areas2DFigureByFigureV7OverlapFree,
)
from geometry8_area_senior_layout_safe_v8 import Geometry8AreaSeniorLayoutSafeV8Mixin


class Geometry8Areas2DFigureByFigureV8SeniorLayoutSafe(
    Geometry8AreaSeniorLayoutSafeV8Mixin,
    Geometry8Areas2DFigureByFigureV7OverlapFree,
):
    """Full V7 lesson with V8 rendered-frame text / geometry safe zones."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT_SAFE.py Geometry8Areas2DFigureByFigureV8SeniorLayoutSafe --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V8_SENIOR_LAYOUT_SAFE.py Geometry8Areas2DFigureByFigureV8SeniorLayoutSafe --disable_caching
