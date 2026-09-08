#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V8 FULL TOTAL DOWNLOAD SAFE.

Purpose
-------
Re-render the complete V7 senior orthographic-projection lesson after a fresh
frame review, while making a small legibility pass and hardening publication so
that the final MP4 can be downloaded and played as a real H.264 file directly
from GitHub.

The geometric construction, dimensional model, PV/PH fold and pedagogical
sequence remain the validated V7 implementation.  V8 deliberately changes only
presentation details that are safe after the V7 frame audit:

- stronger fixed-orientation plane/direction labels with a white backing;
- slightly heavier final 2D-view strokes;
- slightly stronger final view panels and method bars;
- a new literal -pqh render and independent full-video QA;
- publication under both a descriptive filename and a short ASCII alias.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh final.
"""
from __future__ import annotations

from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA import (
    Projection3Dto2DSeniorV7,
    INK,
    GRID,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

LABEL_BG = "#FFFFFF"


class Projection3Dto2DFullTotalV8(Projection3Dto2DSeniorV7):
    """V7 geometry + V8 legibility and publication-safe final render."""

    # ------------------------------------------------------------------
    # Legibility polish verified to preserve V7 geometry and timing
    # ------------------------------------------------------------------
    def _fixed_backed_label(self, text: str, pos, color, font_size: int):
        label = Text(text, font_size=font_size, color=color, weight=BOLD)
        label.move_to(pos)
        bg = SurroundingRectangle(
            label,
            buff=0.07,
            corner_radius=0.04,
            stroke_width=0,
            fill_color=LABEL_BG,
            fill_opacity=0.82,
        )
        group = VGroup(bg, label)
        self.add_fixed_orientation_mobjects(group)
        return group

    def plane_label_3d(self, text, pos, color):
        # V7 labels were correct but low-contrast over translucent planes.
        return self._fixed_backed_label(text, pos, color, font_size=26)

    def direction_label_3d(self, text, pos, color):
        # Keep the observer directions readable during the initial orbit.
        return self._fixed_backed_label(text, pos, color, font_size=25)

    def front_view_2d(self, scale=1.0):
        view = super().front_view_2d(scale)
        view.set_stroke(width=5.1)
        return view

    def top_view_2d(self, scale=1.0):
        view = super().top_view_2d(scale)
        view.set_stroke(width=4.8)
        return view

    def right_view_2d(self, scale=1.0):
        view = super().right_view_2d(scale)
        view.set_stroke(width=5.1)
        return view

    def view_panel(self, view, label, color, width, height):
        panel = super().view_panel(view, label, color, width, height)
        panel[0].set_stroke(color=GRID, width=1.8)
        panel[2].scale(1.05)
        return panel

    def method_bar(self, number, title, detail):
        bar = super().method_bar(number, title, detail)
        bar[0].set_stroke(color=GRID, width=1.65)
        bar[1].set_stroke(color=INK, width=2.0)
        return bar


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_FULL_TOTAL_DOWNLOAD_SAFE.py Projection3Dto2DFullTotalV8 --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_FULL_TOTAL_DOWNLOAD_SAFE.py Projection3Dto2DFullTotalV8 --disable_caching
