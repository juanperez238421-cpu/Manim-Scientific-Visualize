#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5.9 — post-render text-collision cleanup.

V5.8 corrected the mathematical notation, ramp normal, equal-time motion, and
fall spacing. Manual inspection of its rendered frames found two redundant
captions crossing other text. This file removes only those captions while
retaining every V5.8 geometry/animation correction.
"""
from manim import ORIGIN, VectorizedPoint

from Physics9_UniformMotion_Galileo_V5_8_FINAL_VISUAL_QA import (
    Physics9UniformMotionGalileoV58FinalVisualQA,
)


class Physics9UniformMotionGalileoV59PostRenderQA(Physics9UniformMotionGalileoV58FinalVisualQA):
    """Final post-render cleanup after manual inspection of V5.8 frames."""

    def _run_with_hidden_caption(self, exact_caption, scene_method):
        original_txt = self.txt

        def filtered_txt(text, *args, **kwargs):
            if text == exact_caption:
                # Preserve the parent animation sequence without displaying the
                # redundant caption. VectorizedPoint is movable and invisible.
                return VectorizedPoint(ORIGIN)
            return original_txt(text, *args, **kwargs)

        self.txt = filtered_txt
        try:
            return scene_method()
        finally:
            self.txt = original_txt

    def galileo_real_apparatus_v5(self):
        return self._run_with_hidden_caption(
            "position marker after each equal time step",
            super().galileo_real_apparatus_v5,
        )

    def falling_equation_preview_v5(self):
        return self._run_with_hidden_caption(
            "successive distances",
            super().falling_equation_preview_v5,
        )


# Preview: manim -pql Physics9_UniformMotion_Galileo_V5_9_POST_RENDER_QA.py Physics9UniformMotionGalileoV59PostRenderQA --disable_caching
# Final:   manim -pqh Physics9_UniformMotion_Galileo_V5_9_POST_RENDER_QA.py Physics9UniformMotionGalileoV59PostRenderQA --disable_caching
