#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle V9 PROJECTOR MAX.

Targeted legibility refinement of V8 FINAL4 after inspecting the full rendered
241 s timeline. This pass avoids a global scene scale and instead enlarges the
persistent classroom labels, measurement math, checkpoints, opening/closing
typography, and header copy while preserving FINAL4 geometry.

Target: ManimCE 0.20.1, literal -pqh, 1920x1080, 30 fps.
"""

from __future__ import annotations

from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260829_V8_SENIOR_QA_FINAL4 import (
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal4,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (
    LIGHT_GRAY,
    PAPER,
)


class Geometry8CircleFoundationsHalvesTwoRows20260830V9ProjectorMax(
    Geometry8CircleFoundationsHalvesTwoRows20260829V8SeniorQAFinal4
):
    """Projector-first V9: larger secondary copy with FINAL4 geometry preserved."""

    # V9 intentionally allows the larger audited labels to use more horizontal
    # canvas. SAFE_X=7.78 still leaves ~26 px at 1920 width, while the final
    # decoded-frame QA rejects any visible content entering the outer 18 px.
    SAFE_X = 7.78
    PAUSE_SCALE = 1.32

    _TEXT_TARGETS = {
        "CIRCLE: FROM PERIMETER TO AREA": 64,
        "Measure the boundary → split the circle → rearrange the same area": 36,
        "PERIMETER   →   DIAMETER   →   π   →   TWO HALVES   →   TWO ROWS": 34,
        "PERIMETER  P": 36,
        "CENTER": 30,
        "THE DEFINITION OF π": 36,
        "RIGHT HALF": 33,
        "LEFT HALF": 33,
        "ROW 1 — RIGHT HALF": 35,
        "ROW 2 — LEFT HALF": 35,
        "ROW 1 pieces": 34,
        "ROW 2 pieces": 34,
        "ROW 1 boundary = P/2": 34,
        "ROW 2 boundary = P/2": 34,
        "8 sectors — visible scallops": 38,
        "24 sectors — edges look straighter": 38,
        "64 sectors — almost a rectangle": 38,
        "AREA OF A CIRCLE": 54,
        "CIRCLE DERIVATION — NOTEBOOK SUMMARY": 50,
        "1.  π = P/d  →  P = πd; because d = 2r,  P = 2πr.": 36,
        "2.  A vertical diameter creates two curved semicircle arcs.": 36,
        "3.  Each curved semicircle arc has length  P/2 = πr.": 36,
        "4.  Keep the two rows separate, then interlock the same pieces.": 36,
        "5.  Shared height = r; one long base = πr; area = πr².": 36,
    }

    def text(self, content, size, *args, **kwargs):
        target = max(float(size), float(self._TEXT_TARGETS.get(content, size)))
        return super().text(content, target, *args, **kwargs)

    def math(self, latex, size, *args, **kwargs):
        target = float(size)
        if latex == "d" and target >= 50:
            target = max(target, 54)
        elif latex == "r":
            if target >= 58:
                target = max(target, 62)
            elif target >= 50:
                target = max(target, 54)
            elif target >= 44:
                target = max(target, 48)
        elif latex == r"\frac{P}{2}=\pi r" and target <= 46:
            target = 46
        elif latex == r"\text{base}=\frac{P}{2}=\pi r" and target <= 54:
            target = 54
        elif latex == r"\pi r" and target <= 54:
            target = 54
        elif latex == r"\pi=\frac{P}{d}" and target >= 62:
            target = max(target, 66)
        return super().math(latex, target, *args, **kwargs)

    def big_formula(self, latex: str, width: float = 7.0, size: int = 50) -> VGroup:
        target = float(size)
        boosts = {
            r"P=2\pi r\qquad\Longrightarrow\qquad A=\pi r^2": 64,
            r"d=2r": 60,
            r"P=\pi(2r)=2\pi r": 60,
            r"\text{TWO SEPARATE ROWS}\qquad\frac{P}{2}=\pi r\quad\text{for each row}": 47,
            r"\text{shared height}=r\qquad\text{NOT}\qquad 2r": 58,
            r"\text{ONE base}=\frac{P}{2}=\pi r": 54,
            r"A=(\pi r)(r)=\pi r^2": 66,
        }
        target = max(target, float(boosts.get(latex, target)))
        box = RoundedRectangle(
            width=width, height=1.32, corner_radius=0.14,
            stroke_color=BLACK, stroke_width=2.25,
            fill_color=PAPER, fill_opacity=1,
        )
        eq = self.math(latex, target)
        if eq.width > width - 0.48:
            eq.scale_to_fit_width(width - 0.48)
        eq.move_to(box)
        return VGroup(box, eq)

    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        badge = RoundedRectangle(
            width=0.88, height=0.60, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=2.35,
            fill_color=WHITE, fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 27, BOLD).move_to(badge)
        title_mob = self.text(title, 42, BOLD)
        if title_mob.width > 13.00:
            title_mob.scale_to_fit_width(13.00)
        row = VGroup(VGroup(badge, badge_text), title_mob).arrange(RIGHT, buff=0.27)
        row.to_edge(UP, buff=0.14).to_edge(LEFT, buff=0.46)

        rule_y = row.get_bottom()[1] - 0.10
        rule = Line([-7.52, rule_y, 0], [7.52, rule_y, 0], color=LIGHT_GRAY, stroke_width=2.2)

        subtitle_mob = self.text(subtitle, 30)
        if subtitle_mob.width > 14.45:
            subtitle_mob.scale_to_fit_width(14.45)
        subtitle_mob.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)

        group = VGroup(row, rule, subtitle_mob)
        self.projector_safe(group, f"v9 header {number:02d}")
        return group

    def opening_v8(self) -> None:
        """Maximize each opening element independently before final arrangement."""
        title = self.text("CIRCLE: FROM PERIMETER TO AREA", 64, BOLD)
        subtitle = self.text(
            "Measure the boundary → split the circle → rearrange the same area", 36
        )
        flow = self.text(
            "PERIMETER   →   DIAMETER   →   π   →   TWO HALVES   →   TWO ROWS", 34, BOLD
        )
        for mob in (title, subtitle, flow):
            if mob.width > 14.65:
                mob.scale_to_fit_width(14.65)

        formula = self.big_formula(
            r"P=2\pi r\qquad\Longrightarrow\qquad A=\pi r^2", 10.2, 64
        )
        group = VGroup(title, subtitle, flow, formula).arrange(DOWN, buff=0.44)
        self.projector_safe(group, "v9 opening")

        self.play(Write(title), run_time=1.55, rate_func=smooth)
        self.wait(0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.10), run_time=0.95)
        self.wait(0.7)
        self.play(FadeIn(flow, shift=UP * 0.08), run_time=1.00)
        self.wait(0.8)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=1.00)
        self.wait(4.8)
        self.clear_stage(group)

    def closing_v8(self) -> None:
        """Large notebook summary with independent title/line fit; no whole-group shrink."""
        title = self.text("CIRCLE DERIVATION — NOTEBOOK SUMMARY", 50, BOLD)
        if title.width > 14.65:
            title.scale_to_fit_width(14.65)

        lines = VGroup(
            self.text("1.  π = P/d  →  P = πd; because d = 2r,  P = 2πr.", 36),
            self.text("2.  A vertical diameter creates two curved semicircle arcs.", 36),
            self.text("3.  Each curved semicircle arc has length  P/2 = πr.", 36),
            self.text("4.  Keep the two rows separate, then interlock the same pieces.", 36),
            self.text("5.  Shared height = r; one long base = πr; area = πr².", 36),
        )
        for line in lines:
            if line.width > 14.35:
                line.scale_to_fit_width(14.35)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        formula = self.big_formula(r"A=(\pi r)(r)=\pi r^2", 8.4, 66)
        group = VGroup(title, lines, formula).arrange(DOWN, buff=0.38)
        self.projector_safe(group, "v9 closing")

        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.95)
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 0.08) for line in lines],
                lag_ratio=0.20,
            ),
            run_time=3.05,
        )
        self.wait(3.0)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=1.00)
        self.play(Circumscribe(formula[1], color=GRAY, time_width=0.9), run_time=1.25)
        self.wait(8.2)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V9_PROJECTOR_MAX.py Geometry8CircleFoundationsHalvesTwoRows20260830V9ProjectorMax --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V9_PROJECTOR_MAX.py Geometry8CircleFoundationsHalvesTwoRows20260830V9ProjectorMax --disable_caching
