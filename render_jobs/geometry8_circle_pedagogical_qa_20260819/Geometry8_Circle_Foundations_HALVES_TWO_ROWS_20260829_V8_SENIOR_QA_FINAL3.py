#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V8 SENIOR QA — FINAL3 human-visual-QA correction.

The FINAL2 pipeline passed compile, PQL, PQH, full decode, edge safety and the
60-frame extraction.  Human inspection of that contact sheet then identified a
semantic scene-boundary defect: the `P = πd` target created by
TransformMatchingTex in Step 01 has a different object identity than the source
MathTex stored in the original cleanup VGroup, so the target remained visible
through later stages.

FINAL3 explicitly verifies and clears any Step-01 residual mobjects at the
section boundary.  This is deliberately a surgical lifecycle correction; all
V8 geometry, large typography, pacing, safe-margin and Step-04 corrections are
preserved unchanged.
"""

from __future__ import annotations

from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL2 import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal2,
)


class Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal3(
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal2
):
    """FINAL3: no visual object is allowed to leak across the Step-01 boundary."""

    def step_1_circle_parts_and_pi(self) -> None:
        super().step_1_circle_parts_and_pi()

        # Human QA root-cause correction:
        # TransformMatchingTex may replace the source object in the scene with
        # a target object that is not the same Python object stored in the
        # cleanup VGroup.  At this exact boundary the stage must be empty.
        residuals = list(self.mobjects)
        if residuals:
            self.play(
                *[FadeOut(mob) for mob in residuals],
                run_time=0.55,
                rate_func=smooth,
            )

        if self.mobjects:
            raise ValueError(
                f"Step 01 lifecycle QA failed: {len(self.mobjects)} residual mobject(s) remain"
            )


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL3.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal3 --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL3.py Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal3 --disable_caching
