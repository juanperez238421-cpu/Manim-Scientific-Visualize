#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V12 POLYGON DERIVATION QA.

Full-total lesson based on V11. All validated V11 chapters are preserved.
Only the regular-polygon derivation panel is replaced by the V12 fixed-zone,
runtime-guarded overlap-free layout.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V11_EXPLICIT_POLYGON_QA import Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA
from geometry8_area_polygon_v12 import Geometry8AreaPolygonV12Mixin


class Geometry8Areas2DFigureByFigureV12PolygonDerivationQA(
    Geometry8AreaPolygonV12Mixin,
    Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA,
):
    """Complete V11 curriculum with the corrected V12 polygon derivation."""

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V12_POLYGON_DERIVATION_QA.py Geometry8Areas2DFigureByFigureV12PolygonDerivationQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V12_POLYGON_DERIVATION_QA.py Geometry8Areas2DFigureByFigureV12PolygonDerivationQA --disable_caching
