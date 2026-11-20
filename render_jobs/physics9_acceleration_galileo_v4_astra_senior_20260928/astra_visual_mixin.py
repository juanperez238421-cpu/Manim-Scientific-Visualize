#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
from manim import *

from physics9_acceleration_graph_galileo_v3_opusvisual import *  # noqa: F401,F403


class AstraVisualMixin:
    """Legibility, layout, graph and focus-card helpers for V4."""

    def astra_header(self, number: int, title: str, subtitle: str) -> None:
        self.set_header(number, title, subtitle)

    def acceleration_at(self, t_min: float) -> float:
        t = float(np.clip(t_min, 0.0, 120.0))
        if t >= 120.0:
            return float(ACCEL_INTERVALS[-1]["a"])
        for d in ACCEL_INTERVALS:
            if d["t0"] <= t < d["t1"]:
                return float(d["a"])
        return 0.0

    def motion_state(self, t_min: float) -> str:
        a = self.acceleration_at(t_min)
        if a > 1e-9:
            return "ACCELERATING"
        if a < -1e-9:
            return "BRAKING"
        return "CRUISING"

    def assert_clearance(self, left: Mobject, right: Mobject, label: str, gap: float = 0.08) -> None:
        lx0, lx1 = left.get_left()[0], left.get_right()[0]
        ly0, ly1 = left.get_bottom()[1], left.get_top()[1]
        rx0, rx1 = right.get_left()[0], right.get_right()[0]
        ry0, ry1 = right.get_bottom()[1], right.get_top()[1]
        separated = (
            lx1 + gap <= rx0 or rx1 + gap <= lx0 or
            ly1 + gap <= ry0 or ry1 + gap <= ly0
        )
        if not separated:
            raise ValueError(f"{label}: static layout overlap")

    def velocity_axes_astra(self, *, x_length: float = 9.35, y_length: float = 2.35):
        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 20],
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(self.text(str(x), 18).next_to(axes.c2p(x, 0), DOWN, buff=0.08))
        for y in (0, 40, 80):
            labels.add(self.text(str(y), 18).next_to(axes.c2p(0, y), LEFT, buff=0.08))
        labels.add(self.text("time (min)", 22, BOLD).next_to(axes.x_axis, DOWN, buff=0.36))
        labels.add(
            self.text("velocity (km/h)", 22, BOLD)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.42)
        )
        segments = [
            Line(axes.c2p(t0, v0), axes.c2p(t1, v1), color=BLACK_LINE, stroke_width=4.5)
            for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:])
        ]
        return axes, labels, segments

    def acceleration_axes_astra(self, *, x_length: float = 9.35, y_length: float = 2.15):
        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[-0.08, 0.08, 0.04],
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(self.text(str(x), 18).next_to(axes.c2p(x, 0), DOWN, buff=0.08))
        for y in (-0.08, -0.04, 0.0, 0.04, 0.08):
            labels.add(self.text(f"{y:+.2f}", 18).next_to(axes.c2p(0, y), LEFT, buff=0.08))
        labels.add(self.text("time (min)", 22, BOLD).next_to(axes.x_axis, DOWN, buff=0.36))
        labels.add(
            self.text("acceleration (m/s²)", 22, BOLD)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.42)
        )
        segments = [
            Line(
                axes.c2p(d["t0"], d["a"]),
                axes.c2p(d["t1"], d["a"]),
                color=BLACK_LINE,
                stroke_width=5.5,
            )
            for d in ACCEL_INTERVALS
        ]
        return axes, labels, segments

    def focus_panel(
        self,
        phase: str,
        lines: list[str],
        *,
        equation: str | None = None,
        meaning: str | None = None,
        width: float = 4.25,
        height: float = 3.70,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.13,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE_FILL, fill_opacity=1.0,
        )
        phase_mob = self.text(phase, 24, BOLD)
        rule = Line(
            LEFT * (width - 0.62) / 2,
            RIGHT * (width - 0.62) / 2,
            color=LIGHT_GRAY, stroke_width=1.5,
        )
        body = VGroup(*[
            self.text(line, 27, BOLD if i == 0 else NORMAL)
            for i, line in enumerate(lines)
        ])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        parts = [phase_mob, rule, body]
        if equation is not None:
            eq = MathTex(equation, font_size=36, color=BLACK_TEXT)
            if eq.width > width - 0.55:
                eq.scale_to_fit_width(width - 0.55)
            parts.append(eq)
        if meaning is not None:
            parts.append(self.text(meaning, 30, BOLD))
        content = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        if content.height > height - 0.48:
            content.scale_to_fit_height(height - 0.48)
        if content.width > width - 0.50:
            content.scale_to_fit_width(width - 0.50)
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def big_hud(self, tracker: ValueTracker, *, x: float = 5.25, y: float = -0.15) -> Mobject:
        return always_redraw(
            lambda: self.focus_panel(
                "LIVE MOTION",
                [
                    f"t = {tracker.get_value():.0f} min",
                    f"v = {self.velocity_kmh_at(tracker.get_value()):.0f} km/h",
                    f"a = {self.acceleration_at(tracker.get_value()):+.3f} m/s²",
                ],
                meaning=self.motion_state(tracker.get_value()),
                width=4.20,
                height=3.65,
            ).move_to([x, y, 0])
        )
