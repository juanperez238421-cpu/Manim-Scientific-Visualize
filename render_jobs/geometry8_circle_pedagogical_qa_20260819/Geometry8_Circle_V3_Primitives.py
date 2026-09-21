#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 circle lesson V3 — modular cinematic animation layer.

Target: Manim Community Edition 0.20.1.
Visual contract: JP Classroom monochrome, projector-safe 16:9.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *


class CircleV3PrimitivesMixin:
    """Animation mixin used by the Geometry 8 V3 circle lesson."""

    def _object_disc(self, center, radius, label, *, rings=2):
        outer = Circle(radius=radius, stroke_color=BLACK_LINE, stroke_width=4)
        outer.move_to(center)
        inner = VGroup()
        for j in range(rings):
            rr = radius * (0.72 - j * 0.18)
            ring = Circle(radius=rr, stroke_color=LIGHT_GRAY, stroke_width=1.7)
            ring.move_to(center)
            inner.add(ring)
        dot = Dot(center, radius=0.045, color=BLACK_LINE)
        title = self.text(label, 22, BOLD).next_to(outer, UP, buff=0.15)
        return VGroup(outer, inner, dot, title)

    def _diameter_gauge(self, circle: Circle, text: str):
        y = circle.get_center()[1]
        left = np.array([circle.get_left()[0], y, 0])
        right = np.array([circle.get_right()[0], y, 0])
        line = DoubleArrow(
            left, right, buff=0.02, tip_length=0.12,
            color=BLACK_LINE, stroke_width=2.4,
        )
        label = self.math(text, 29).next_to(line, DOWN, buff=0.10)
        return VGroup(line, label)

    def _circumference_trace(self, circle: Circle):
        start = circle.point_at_angle(0)
        dot = Dot(start, radius=0.07, color=BLACK_LINE)
        path = Circle(
            radius=circle.radius,
            stroke_color=BLACK_LINE,
            stroke_width=7,
        ).move_to(circle.get_center())
        return path, dot

    def _unit_badge(self, text_value: str, position):
        box = RoundedRectangle(
            width=2.0,
            height=0.76,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=PAPER_GRAY,
            fill_opacity=1.0,
        ).move_to(position)
        value = self.math(text_value, 31).move_to(box)
        return VGroup(box, value)

    def _mini_square_grid(self, center, cols=5, rows=5, size=0.23):
        squares = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=size,
                    stroke_color=LIGHT_GRAY,
                    stroke_width=1.0,
                    fill_color=VERY_LIGHT_GRAY,
                    fill_opacity=0.75,
                )
                sq.move_to(
                    center
                    + RIGHT * (c - (cols - 1) / 2) * size
                    + UP * ((rows - 1) / 2 - r) * size
                )
                squares.add(sq)
        return squares

    def _solution_line(self, expression: str, size=40, pos=ORIGIN):
        mob = self.math(expression, size).move_to(pos)
        self.fit(mob, 6.3, 0.85)
        return mob
