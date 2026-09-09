#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V15 PRESENTATION QA.

Targeted presentation QA on top of the real V14 choreography rebuild.

Why this exists:
- V14 successfully replaced the V13 timing-only revision with a real visual rebuild.
- Frame audit then found three tail-section defects:
  1) the ISO A / ISO E title exceeded the horizontal safe area;
  2) the already-folded physical projections remained visible behind the ISO comparison;
  3) the final five-step cards were added as children of one fixed group and did not
     render reliably as independent teaching beats.

V15 keeps the complete V14 point-first, vertex-ray, landing-point, traced-contour,
PH/PL rigid-fold choreography and fixes only those presentation defects.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh.
"""
from __future__ import annotations

from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V14_REBUILT_CHOREOGRAPHY import (
    Projection3Dto2DV14RebuiltChoreography,
    T,
)


class Projection3Dto2DV15PresentationQA(Projection3Dto2DV14RebuiltChoreography):
    """V14 with tail-section visual QA fixes."""

    @staticmethod
    def _text_strings(mob):
        texts = []
        txt = getattr(mob, "text", None)
        if isinstance(txt, str):
            texts.append(txt)
        for sub in getattr(mob, "submobjects", []):
            texts.extend(Projection3Dto2DV15PresentationQA._text_strings(sub))
        return texts

    @classmethod
    def _contains_text(cls, mob, phrase: str) -> bool:
        return any(phrase in t for t in cls._text_strings(mob))

    def add_fixed_in_frame_mobjects(self, *mobjects):
        # Keep any fixed title inside the 16:9 safe width.  This specifically
        # corrects the long ISO A/E comparison heading found in the V14 audit,
        # while remaining harmless for already-safe banners.
        for mob in mobjects:
            try:
                if mob.width > 14.15:
                    mob.scale_to_fit_width(14.15)
            except Exception:
                pass

        # When the ISO A/E comparison begins, the pedagogical 3D construction
        # has already completed its job.  V14 left the three folded projection
        # drawings behind the new comparison, which visually stacked two
        # different explanations.  Clean the scene with a short fade before
        # introducing the A/E diagram.
        if any(self._contains_text(m, "LAS VISTAS SON LAS MISMAS") for m in mobjects):
            current = list(self.mobjects)
            if current:
                self.play(*[FadeOut(m) for m in current], run_time=T(0.55), rate_func=smooth)
                self.remove(*current)

        # The V14 final mental-model group contains title + cards + note.
        # Register its visible pieces independently so each numbered card can
        # FadeIn as an actual separate teaching beat.
        for mob in mobjects:
            if self._contains_text(mob, "DE UN OBJETO 3D A UNA HOJA 2D") and len(getattr(mob, "submobjects", [])) == 3:
                title, cards, note = mob.submobjects
                pieces = [title, *list(cards.submobjects), note]
                return super().add_fixed_in_frame_mobjects(*pieces)

        return super().add_fixed_in_frame_mobjects(*mobjects)

    def remove_fixed_in_frame_mobjects(self, *mobjects):
        for mob in mobjects:
            if self._contains_text(mob, "DE UN OBJETO 3D A UNA HOJA 2D") and len(getattr(mob, "submobjects", [])) == 3:
                title, cards, note = mob.submobjects
                pieces = [title, *list(cards.submobjects), note]
                return super().remove_fixed_in_frame_mobjects(*pieces)
        return super().remove_fixed_in_frame_mobjects(*mobjects)


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V15_PRESENTATION_QA.py Projection3Dto2DV15PresentationQA --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V15_PRESENTATION_QA.py Projection3Dto2DV15PresentationQA --disable_caching
