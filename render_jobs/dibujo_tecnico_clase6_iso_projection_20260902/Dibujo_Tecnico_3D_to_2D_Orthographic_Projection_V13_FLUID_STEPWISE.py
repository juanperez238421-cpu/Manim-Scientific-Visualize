#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V13 FLUID STEPWISE.

Pacing/director revision built on the validated V12 full-total scene.

V13 intentionally keeps V12's geometry, orthographic-projection logic,
ALZADO/PLANTA/PERFIL construction, PH 90° fold, alignment guides, 2D studio,
final sheet, safe-area composition and publication-safe visual language.

The revision addresses classroom readability rather than changing content:

* longer semantic pauses after each explanatory beat;
* slightly longer motion durations so camera moves and object transfers read
  as continuous actions instead of quick jumps;
* a short automatic "breath" after substantial animations;
* smooth interpolation is used as the default scene-level play rate function;
* the existing explicit 1/3 → 2/3 → 3/3 construction remains unchanged;
* all pacing controls are exposed through environment variables for easy QA.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh final.
"""
from __future__ import annotations

import os
from manim import smooth

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V12_FIXED_FULL_TOTAL import (
    Projection3Dto2DV12FixedFullTotal,
)


# ---------------------------------------------------------------------------
# Director controls
# ---------------------------------------------------------------------------
# V12 already applies its classroom timing wrapper T().  These factors are a
# second, deliberately modest director pass focused on fluidity and breathing
# room.  They can be overridden by CI for fast preview renders.
ANIMATION_FACTOR = float(os.getenv("V13_ANIMATION_FACTOR", "1.12"))
PAUSE_FACTOR = float(os.getenv("V13_PAUSE_FACTOR", "1.35"))
MICRO_BREATH = float(os.getenv("V13_MICRO_BREATH", "0.18"))
BREATH_THRESHOLD = float(os.getenv("V13_BREATH_THRESHOLD", "0.60"))


class Projection3Dto2DV13FluidStepwise(Projection3Dto2DV12FixedFullTotal):
    """Validated V12 lesson with slower motion and stronger stepwise pauses."""

    def play(self, *animations, **kwargs):
        """Make substantial motions more fluid and add a brief reading beat.

        V12 already specifies explicit run times for nearly every meaningful
        action.  We preserve their relative timing and only scale the duration.
        A scene-level smooth rate function is supplied when the call does not
        already define one.
        """
        requested = kwargs.get("run_time")
        if requested is not None:
            kwargs["run_time"] = float(requested) * ANIMATION_FACTOR

        kwargs.setdefault("rate_func", smooth)
        result = super().play(*animations, **kwargs)

        # Add a tiny neutral hold after substantial visual actions.  Call the
        # parent wait directly so the micro-breath is not multiplied again by
        # PAUSE_FACTOR.
        effective = kwargs.get("run_time")
        if effective is not None and float(effective) >= BREATH_THRESHOLD and MICRO_BREATH > 0:
            super().wait(MICRO_BREATH)
        return result

    def wait(self, duration=1, stop_condition=None, frozen_frame=None):
        """Increase deliberate classroom pauses without altering scene logic."""
        return super().wait(
            float(duration) * PAUSE_FACTOR,
            stop_condition=stop_condition,
            frozen_frame=frozen_frame,
        )


__all__ = ["Projection3Dto2DV13FluidStepwise"]
