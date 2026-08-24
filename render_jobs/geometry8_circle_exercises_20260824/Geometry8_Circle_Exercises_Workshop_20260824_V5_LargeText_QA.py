#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle Exercises Workshop V5 — Large Text QA fixes."""
from __future__ import annotations

from manim import *
from jp_classroom_style import *
from Geometry8_Circle_Exercises_Workshop_20260824_V4_LargeText import (
    Geometry8CircleExercisesWorkshop20260824V4LargeText,
)


class Geometry8CircleExercisesWorkshop20260824V5LargeTextQA(
    Geometry8CircleExercisesWorkshop20260824V4LargeText
):
    """Large-text projector edition with safe lower answer bands."""

    # Inherited protocol markers:
    # exercise_09_sector
    # self._v4_zoom
    # assert_content_safe

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()

    def _answer_check(self, text: str, *, y: float = -2.58, width: float = 9.8) -> VGroup:
        """Large, compact verification band placed safely above the lower margin."""
        title = self.text("COMPROBACIÓN", 40, BOLD)
        body = self.text(text, 40)
        self.fit(body, width - 1.0, 0.70)
        content = VGroup(title, body).arrange(DOWN, buff=0.16)
        panel = self._v4_panel(
            content,
            width=width,
            height=1.62,
            fill_color=PAPER_GRAY,
        ).move_to([0, max(y, -2.70), 0])
        self.assert_content_safe(panel, "V5 large answer check")
        return panel
