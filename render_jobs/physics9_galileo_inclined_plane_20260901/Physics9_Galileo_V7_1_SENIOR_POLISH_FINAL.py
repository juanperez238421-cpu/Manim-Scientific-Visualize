#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V7.1 Senior Polish Final.

This scene intentionally reuses the complete V7 pedagogical redesign and
applies the final presentation-level correction requested after reviewing the
V6.2 render: larger header hierarchy, materially larger subtitle text, a safe
top margin, and more breathing room between the persistent header and the
animated lesson content.

The inherited V7 scenes already implement the substantive redesign:
- explicit 0.00 / 0.50 / 1.00 / 1.50 / 2.00 s timing;
- 0.00 / 0.10 / 0.40 / 0.90 / 1.60 m ramp positions;
- 0.10 / 0.30 / 0.50 / 0.70 m interval distances = 1:3:5:7;
- larger figures/equations than V6.2;
- staged transforms, physical cart/ball motion, progressive data reveals;
- longer reading/explanation pauses;
- enlarged Pisa mass-independence and air-resistance sections.

The override below fixes the remaining systematic top-edge/clipping problem
without shrinking the educational content back down.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pql -> -pqh.
"""
from manim import *

from Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL import (
    Physics9GalileoV7VisualRedesignSeniorFinal,
    BLACK_TEXT,
    DARK_GRAY,
    LIGHT_GRAY,
    RUN,
)


class Physics9GalileoV71SeniorPolishFinal(Physics9GalileoV7VisualRedesignSeniorFinal):
    """V7 content with a larger, safer persistent section header."""

    def header_v7(self, number: int, title: str, subtitle: str):
        # A larger badge/title improves projector readability, while the 0.34
        # top buffer prevents ascenders and antialiasing pixels from touching
        # the 1920x1080 frame boundary.
        badge = RoundedRectangle(
            width=0.62,
            height=0.40,
            corner_radius=0.08,
            stroke_color=BLACK_TEXT,
            stroke_width=1.9,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 22, BOLD).move_to(badge)
        title_m = self.txt(title, 34, BOLD)
        title_m.next_to(badge, RIGHT, buff=0.18)

        header = VGroup(badge, num, title_m)
        # Preserve a substantial font size. Only fit unusually long titles,
        # and fit them inside a deliberate horizontal safe region.
        self.fit(header, 13.00, 0.66)
        header.to_edge(UP, buff=0.34).to_edge(LEFT, buff=0.40)

        subtitle_m = self.txt(subtitle, 24, color=DARK_GRAY)
        self.fit(subtitle_m, 12.95, 0.53)
        subtitle_m.next_to(header, DOWN, aligned_edge=LEFT, buff=0.11)

        line = Line(
            LEFT * 6.48,
            RIGHT * 6.48,
            color=LIGHT_GRAY,
            stroke_width=1.35,
        )
        line.next_to(subtitle_m, DOWN, buff=0.10)

        self.play(
            FadeIn(header, shift=RIGHT * 0.10),
            FadeIn(subtitle_m, shift=DOWN * 0.04),
            Create(line),
            run_time=RUN,
            rate_func=smooth,
        )
        # A short settle pause is deliberate: students can read the new
        # section before the next moving diagram enters.
        self.wait(0.55)
        return VGroup(header, subtitle_m, line)
