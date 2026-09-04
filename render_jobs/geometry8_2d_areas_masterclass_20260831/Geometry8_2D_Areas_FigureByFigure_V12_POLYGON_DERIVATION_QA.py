#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V12 POLYGON DERIVATION QA.

Full-total lesson based on V11. All validated V11 chapters are preserved.
Only the regular-polygon derivation panel is replaced by the V12 fixed-zone,
runtime-guarded overlap-free layout.

V12.1 runtime fix:
The first GitHub PQL gate correctly detected that the heading
"AREA OF ONE TRIANGLE" consumed the protected horizontal gutter between the
isolated triangle and the upper-right formula zone.  Keep the geometric QA
assertion intact and cap only that heading's rendered width.  This preserves
readability while guaranteeing a real visual gutter instead of weakening QA.
"""
from __future__ import annotations

from Geometry8_2D_Areas_FigureByFigure_V11_EXPLICIT_POLYGON_QA import Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA
from geometry8_area_polygon_v12 import Geometry8AreaPolygonV12Mixin


class Geometry8Areas2DFigureByFigureV12PolygonDerivationQA(
    Geometry8AreaPolygonV12Mixin,
    Geometry8Areas2DFigureByFigureV11ExplicitPolygonQA,
):
    """Complete V11 curriculum with the corrected V12 polygon derivation."""

    def txt(self, s, size=34, bold=False):
        """Preserve the classroom style while enforcing the V12 derivation gutter.

        The geometry panel places the extracted triangle at x≈2.1 and the
        one-triangle formula at x≈4.7.  The long heading is the only object that
        exceeded its lane in the first V12 runtime QA.  Limiting its width to
        2.80 scene units keeps the font visually large and leaves >0.16 units of
        protected whitespace before the formula lane, as required by the
        unchanged bounding-box assertion in geometry8_area_polygon_v12.py.
        """
        mob = super().txt(s, size, bold)
        if s == "AREA OF ONE TRIANGLE" and size == 18 and mob.width > 2.80:
            mob.scale_to_fit_width(2.80)
        return mob

    def construct(self):
        super().construct()


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V12_POLYGON_DERIVATION_QA.py Geometry8Areas2DFigureByFigureV12PolygonDerivationQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V12_POLYGON_DERIVATION_QA.py Geometry8Areas2DFigureByFigureV12PolygonDerivationQA --disable_caching
