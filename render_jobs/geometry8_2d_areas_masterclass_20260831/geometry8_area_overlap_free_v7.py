#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V7 Senior QA overlap correction.

This layer preserves every validated V6 figure, derivation, number, formula and
animation while rebuilding the worked-example panel with fixed vertical rows and
non-intersecting horizontal zones for step headings and mathematical content.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaOverlapFreeV7Mixin:
    """Senior-QA layout overrides for all ten worked examples."""

    def _example_step_row(self, number, label, value, panel, y_offset):
        """Build one fixed-height row with guaranteed left/right safety zones."""
        badge = RoundedRectangle(
            width=.64,
            height=.36,
            corner_radius=.07,
            stroke_color=INK,
            stroke_width=1.35,
            fill_color=PAPER,
            fill_opacity=1,
        )
        num = self.txt(number, 16, True).move_to(badge)
        lab = self.txt(label, 17, True).set_opacity(.72)
        heading = VGroup(VGroup(badge, num), lab).arrange(RIGHT, buff=.10)

        # LEFT ZONE: x in approximately [-2.85, -1.00].
        # RIGHT ZONE: x in approximately [-0.52, +2.72].
        # The divider and a >=0.20 scene-unit gutter prevent touching/overlap,
        # even for the longest GIVEN strings used by the ten examples.
        self.fit(heading, 1.82, .42)
        heading.move_to(panel.get_center() + LEFT*1.93 + UP*y_offset)

        self.fit(value, 3.16, .52)
        value.move_to(panel.get_center() + RIGHT*1.10 + UP*y_offset)

        divider = Line(
            panel.get_center() + LEFT*.72 + UP*(y_offset-.30),
            panel.get_center() + LEFT*.72 + UP*(y_offset+.30),
            color=LIGHT,
            stroke_width=1.25,
        )
        return VGroup(heading, divider, value)

    def example_stack(self, given, formula, substitution, result, width=6.15):
        """Rebuild the worked example as a fixed-grid notebook panel."""
        width = max(width, 6.20)
        panel = RoundedRectangle(
            width=width,
            height=4.92,
            corner_radius=.14,
            stroke_color=LIGHT,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=.985,
        )

        title = self.txt("WORKED EXAMPLE", 31, True)
        title.move_to(panel.get_center() + UP*2.06)

        guide = self.txt("READ  →  FORMULA  →  SUBSTITUTE  →  ANSWER", 18, True).set_opacity(.58)
        self.fit(guide, width-.62, .30)
        guide.move_to(panel.get_center() + UP*1.70)

        top_rule = Line(
            panel.get_left()+RIGHT*.24+UP*1.47,
            panel.get_right()+LEFT*.24+UP*1.47,
            color=LIGHT,
            stroke_width=1.25,
        )

        given_m = self.txt(given, 26)
        formula_m = self.eq(formula, 40)
        sub_m = self.eq(substitution, 38)
        answer_m = self.box(result, 3.05, 42)

        row1 = self._example_step_row("01", "READ GIVEN", given_m, panel, 1.08)
        row2 = self._example_step_row("02", "CHOOSE FORMULA", formula_m, panel, .30)
        row3 = self._example_step_row("03", "SUBSTITUTE", sub_m, panel, -.48)
        row4 = self._example_step_row("04", "CALCULATE", answer_m, panel, -1.28)

        check = self.txt("✓ Answer written in square units", 19, True).set_opacity(.74)
        self.fit(check, width-.74, .34)
        check.move_to(panel.get_center() + DOWN*2.08)

        content = VGroup(title, guide, top_rule, row1, row2, row3, row4, check)
        return VGroup(panel, content)

    def show_example(self, stack, right_x=3.55):
        """Reveal the fixed-grid example one numbered row at a time."""
        stack.move_to(RIGHT*right_x + DOWN*.40)
        panel, content = stack

        self.play(FadeIn(panel, shift=UP*.03), run_time=.38)
        self.play(FadeIn(content[0], shift=UP*.02), run_time=.34)
        self.play(FadeIn(content[1]), Create(content[2]), run_time=.36)
        self.wait(.55)

        pauses = (.90, 1.00, 1.05, 1.30)
        for row, pause in zip(content[3:7], pauses):
            self.play(FadeIn(row, shift=UP*.025), run_time=.44)
            self.wait(pause)

        self.play(FadeIn(content[7], shift=UP*.02), run_time=.34)
        self.wait(2.00)
