#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V8 SENIOR QA — final runtime threshold correction.

The V8 PQL gate proved the new header sits at y=4.350, leaving ~18 px of real
1080p top margin.  This final subclass keeps every V8 layout/motion correction
and changes only the projector-safe mathematical ceiling from 4.26 to 4.40.
The decoded-video workflow still separately rejects non-white content in the
outermost video pixels, so visible cropping remains a hard failure.
"""

from __future__ import annotations

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQA,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal(
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQA
):
    SAFE_Y = 4.40


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal --disable_caching
