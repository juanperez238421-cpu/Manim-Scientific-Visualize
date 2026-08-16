#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""History of Velocity — Senior V6 review update.

This file is a review-focused continuation of the audited V5 reconstruction.
Goal of V6:
- preserve the improved V5 layouts;
- give more reading time between sections;
- add a calmer reflection beat during stage clears;
- remain fully compatible with the same JP classroom style stack.

Render target:
    LESSON_TIME_SCALE=1.85 manim -pqh history_of_velocity_FINAL_V6.py HistoryOfVelocityV6 --fps 30 --disable_caching
"""
from __future__ import annotations

from manim import *
from jp_classroom_style import *
from history_of_velocity_FINAL_V5 import HistoryOfVelocityV5


class HistoryOfVelocityV6(HistoryOfVelocityV5):
    """Senior review version with more deliberate pacing.

    V6 intentionally focuses on pacing polish rather than changing the
    mathematical storyline again.  The objective is to preserve the improved
    compositions from V5 while leaving noticeably more time for students to
    read, connect and discuss each section.
    """

    def clear_stage(self, keep_header: bool = True) -> None:
        """Longer reflection beat before clearing the stage.

        This replaces the faster V5 transition with a calmer cue so the viewer
        has a genuine reading pause before the next historical block begins.
        """
        if keep_header and self.mobjects:
            y = 2.10
            track = Line(
                LEFT * 5.45 + UP * y,
                RIGHT * 5.45 + UP * y,
                color=LIGHT_GRAY,
                stroke_width=1.5,
            )
            pulse = Dot(track.get_start(), radius=0.060, color=BLACK)
            label = self.text("REFLECT • CONNECT • PREPARE FOR THE NEXT IDEA", 14, BOLD)
            label.next_to(track, UP, buff=0.06, aligned_edge=LEFT)
            self.play(FadeIn(label), Create(track), FadeIn(pulse), run_time=0.35)
            self.play(pulse.animate.move_to(track.get_end()), run_time=2.65, rate_func=linear)
            self.wait(0.25)
            self.play(FadeOut(VGroup(label, track, pulse)), run_time=0.30)
        super().clear_stage(keep_header=keep_header)

    def construct(self) -> None:
        """Run the full lesson with the V5 scene stack and a gentler cadence."""
        super().construct()
