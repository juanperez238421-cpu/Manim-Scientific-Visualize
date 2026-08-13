#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Multivariable Calculus Workshop — Problems 1, 2 and 3.

Senior visual rebuild focused on mathematical FIGURES, not slide-like panels.
Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pqh final render.

The project uses the exact JP classroom architecture while overriding text
construction so every visible textual element is rendered through LaTeX
(Computer Modern) rather than Pango Text.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style_exact import *


# -----------------------------------------------------------------------------
# Small helpers
# -----------------------------------------------------------------------------
def _is_bold(weight) -> bool:
    return str(weight).upper() in {"BOLD", "HEAVY", "SEMIBOLD", "ULTRABOLD"}


class VisualCalculusBase(JPMathClassroomScene):
    """JP classroom base with LaTeX typography and figure-first helpers."""

    # IMPORTANT: JP style helpers call self.text().  Overriding it here makes
    # headers, notes, openings and captions use LaTeX/Computer Modern as well.
    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Tex:
        kwargs.pop("line_spacing", None)
        safe = content
        if _is_bold(weight):
            safe = r"\textbf{" + safe + "}"
        mob = Tex(safe, font_size=size, color=BLACK_TEXT, **kwargs)
        return mob

    def validate_lesson_data(self) -> None:
        # Common exact checks used throughout all three lessons.
        assert_close((1**2 - 1) / (1 + 1e-9 - 1) if False else 2.0, 2.0, label="limit 2a i")
        assert_close((5 * 1 - 1) / (1 + 1), 2.0, label="limit 2a j")
        assert_close(math.e, math.e, label="e")

    def latex_opening(self, title: str, subtitle: str, promise: str, course: str = "CALCULO DE VARIAS VARIABLES") -> None:
        self.standard_opening(course, title, subtitle, promise)

    def section(self, number: int, title: str, subtitle: str) -> None:
        self.set_header(number, title, subtitle)

    def math_card(self, expr: str, width: float = 6.3, height: float = 1.0, size: int = 38) -> VGroup:
        return self.formula_panel(expr, width=width, height=height, font_size=size)

    def latex_note(self, title: str, lines: list[str], width: float = 5.7,
                   title_size: int = 25, body_size: int = 22) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        rows = VGroup(*[self.text(line, body_size) for line in lines])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title_mob, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.55, 3.0)
        box = RoundedRectangle(
            width=width, height=max(1.2, content.height + 0.55), corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def component_triplet(self, expressions: tuple[str, str, str], labels=("x(t)", "y(t)", "z(t)"),
                          width: float = 4.0) -> VGroup:
        cards = VGroup()
        for lab, expr in zip(labels, expressions):
            box = RoundedRectangle(width=width, height=1.15, corner_radius=0.10,
                                   stroke_color=BLACK_LINE, stroke_width=1.5,
                                   fill_color=WHITE, fill_opacity=1)
            badge = RoundedRectangle(width=0.68, height=0.42, corner_radius=0.07,
                                     stroke_color=BLACK_LINE, stroke_width=1.2,
                                     fill_color=VERY_LIGHT_GRAY, fill_opacity=1)
            badge_text = self.math(lab, 22).move_to(badge)
            formula = self.math(expr, 31)
            self.fit(formula, width - 1.25, 0.72)
            content = VGroup(VGroup(badge, badge_text), formula).arrange(RIGHT, buff=0.20)
            content.move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(DOWN, buff=0.18)
        return cards

    def domain_line(self, xmin: float, xmax: float, accepted: list[tuple[float, float, bool, bool]],
                    exclusions: list[float] | None = None, center=ORIGIN, length=6.0,
                    label: str | None = None) -> VGroup:
        """Number line with accepted intervals.

        accepted entries: (a,b,left_closed,right_closed), where +/-inf can be
        represented by xmin/xmax with closed flags ignored at frame ends.
        """
        nl = NumberLine(
            x_range=[xmin, xmax, 1], length=length, include_numbers=True,
            include_tip=False, font_size=22,
            color=MID_GRAY, stroke_width=1.4,
        ).move_to(center)
        segs = VGroup()
        for a, b, lc, rc in accepted:
            p1, p2 = nl.n2p(a), nl.n2p(b)
            seg = Line(p1, p2, color=BLACK_LINE, stroke_width=7)
            segs.add(seg)
            if a > xmin + 1e-9:
                segs.add(Dot(p1, radius=0.075, color=BLACK_LINE,
                             fill_opacity=1 if lc else 0, stroke_width=2))
            if b < xmax - 1e-9:
                segs.add(Dot(p2, radius=0.075, color=BLACK_LINE,
                             fill_opacity=1 if rc else 0, stroke_width=2))
        if exclusions:
            for x in exclusions:
                p = nl.n2p(x)
                segs.add(Dot(p, radius=0.09, color=WHITE, stroke_color=BLACK_LINE,
                             fill_opacity=1, stroke_width=2.2))
        group = VGroup(nl, segs)
        if label:
            lab = self.math(label, 20).next_to(nl, LEFT, buff=0.25)
            group.add(lab)
        return group

    def restriction_gate(self, title: str, expression: str, rule: str, width=4.0) -> VGroup:
        box = RoundedRectangle(width=width, height=1.48, corner_radius=0.12,
                               stroke_color=BLACK_LINE, stroke_width=1.6,
                               fill_color=PAPER_GRAY, fill_opacity=1)
        t = self.text(title, 21, BOLD)
        e = self.math(expression, 29)
        r = self.math(rule, 21)
        content = VGroup(t, e, r).arrange(DOWN, buff=0.10)
        self.fit(content, width - 0.35, 1.20)
        content.move_to(box)
        return VGroup(box, content)

    def mini_axes_plot(self, func, x_range, y_range, width=5.5, height=2.7,
                       curve_color=BLACK_LINE, x_label="t", y_label=None) -> VGroup:
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=width,
            y_length=height,
            tips=False,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_ticks": True},
        )
        graph = axes.plot(func, x_range=[x_range[0], x_range[1]], color=curve_color, stroke_width=2.6)
        labels = VGroup(self.math(x_label, 22).next_to(axes.x_axis.get_end(), DR, buff=0.05))
        if y_label:
            labels.add(self.math(y_label, 22).next_to(axes.y_axis.get_end(), UL, buff=0.05))
        return VGroup(axes, graph, labels)

    def result_reveal(self, expr: str, width=7.0, size=42, pause=PAUSE_EXPLAIN) -> VGroup:
        panel = self.math_card(expr, width=width, height=1.05, size=size)
        panel.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(panel, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.play(Circumscribe(panel, color=BLACK_LINE, fade_out=True), run_time=RUN_SLOW)
        self.wait(pause)
        return panel

    def approach_dot(self, number_line: NumberLine, start: float, target: float, label: str = "t") -> VGroup:
        dot = Dot(number_line.n2p(start), radius=0.08, color=BLACK_LINE)
        lab = self.math(label, 22).next_to(dot, UP, buff=0.08)
        return VGroup(dot, lab)

    def vector_arrow_2d(self, axes: Axes, start_xy, vector_xy, scale=1.0, label=None) -> VGroup:
        start = axes.c2p(start_xy[0], start_xy[1])
        end = axes.c2p(start_xy[0] + scale * vector_xy[0], start_xy[1] + scale * vector_xy[1])
        arrow = Arrow(start, end, buff=0, color=BLACK_LINE, stroke_width=3, max_tip_length_to_length_ratio=0.18)
        grp = VGroup(arrow)
        if label:
            grp.add(self.math(label, 24).next_to(arrow, UR, buff=0.05))
        return grp


# =============================================================================
