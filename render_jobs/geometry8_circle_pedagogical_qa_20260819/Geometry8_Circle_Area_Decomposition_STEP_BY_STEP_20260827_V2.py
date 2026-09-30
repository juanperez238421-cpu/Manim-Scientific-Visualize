#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 safe-header patch for the dedicated circle-area decomposition lesson.

The pedagogical/geometry timeline remains exactly the V1 scene.  This subclass
only corrects the persistent header rule so its 14.9-unit line stays centered
on the frame rather than inheriting the left-shifted title-row center.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    Geometry8CircleAreaDecomposition20260827,
    LIGHT_GRAY,
)


class Geometry8CircleAreaDecomposition20260827V2(Geometry8CircleAreaDecomposition20260827):
    """Same lesson, with a frame-safe centered persistent header."""

    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        badge = RoundedRectangle(
            width=0.78,
            height=0.54,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 23, BOLD).move_to(badge)
        title_mob = self.text(title, 34, BOLD)
        if title_mob.width > 12.8:
            title_mob.scale_to_fit_width(12.8)

        badge_group = VGroup(badge, badge_text)
        row = VGroup(badge_group, title_mob).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

        # Critical V2 fix: keep the full-width rule centered at x=0.
        rule_y = row.get_bottom()[1] - 0.10
        rule = Line(
            [-7.45, rule_y, 0],
            [7.45, rule_y, 0],
            color=LIGHT_GRAY,
            stroke_width=2,
        )

        sub = self.text(subtitle, 21)
        if sub.width > 14.0:
            sub.scale_to_fit_width(14.0)
        sub.next_to(rule, DOWN, buff=0.08)
        sub.align_to(row, LEFT)

        return VGroup(row, rule, sub)


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827_V2.py Geometry8CircleAreaDecomposition20260827V2 --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827_V2.py Geometry8CircleAreaDecomposition20260827V2 --disable_caching
