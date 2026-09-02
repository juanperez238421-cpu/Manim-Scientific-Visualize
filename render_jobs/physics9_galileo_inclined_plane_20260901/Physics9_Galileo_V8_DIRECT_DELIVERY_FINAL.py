#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V8 Direct Delivery Final.

V8 is the delivery-focused polish requested after the V6.2 screenshots and the
V7/V7.1 review. It keeps the complete V7 redesign and V7.1 safe header while
making the presentation feel less rushed and more fluid:

- V7 large-format figures, equations, axes, labels and numerical examples;
- explicit 0.00/0.50/1.00/1.50/2.00 s Galileo timing;
- 0.00/0.10/0.40/0.90/1.60 m positions and 1:3:5:7 interval pattern;
- V7.1 safe top margin and larger header hierarchy;
- slower staged transformations and physical-motion animations;
- longer reading/explanation pauses;
- smoother section exits with a short visual breathing pause.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pql -> -pqh.
"""
from manim import *

import Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL as v7mod
import Physics9_Galileo_V7_1_SENIOR_POLISH_FINAL as v71mod
from Physics9_Galileo_V7_1_SENIOR_POLISH_FINAL import (
    Physics9GalileoV71SeniorPolishFinal,
)


class Physics9GalileoV8DirectDeliveryFinal(Physics9GalileoV71SeniorPolishFinal):
    """V7.1 content with senior pacing and smoother scene transitions."""

    def construct(self):
        v7mod.RUN = 1.30
        v7mod.RUN_FAST = 0.95
        v7mod.RUN_SLOW = 1.85
        v7mod.PAUSE_SHORT = 1.55
        v7mod.PAUSE_READ = 2.90
        v7mod.PAUSE_EXPLAIN = 4.10
        v7mod.PAUSE_WORK = 5.20
        v71mod.RUN = 1.30
        super().construct()

    def clear_stage(self):
        """Use a smooth full-stage fade instead of an abrupt scene reset."""
        if self.mobjects:
            stage = Group(*self.mobjects)
            self.play(
                FadeOut(stage, shift=DOWN * 0.025),
                run_time=0.95,
                rate_func=smooth,
            )
        self.clear()
        self.wait(0.22)
