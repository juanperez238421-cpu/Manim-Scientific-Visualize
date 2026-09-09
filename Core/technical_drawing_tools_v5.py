#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 presentation helpers for engineering-graphics Manim lessons.

Extends the stable technical_drawing_tools module with larger orthographic
view surfaces and explicit safe-layout primitives.  The goal is to separate
narrative UI from geometry so titles/callouts never compete with the figures.
Compatible with ManimCE 0.20.x.
"""
from __future__ import annotations
from manim import *
from Core.technical_drawing_tools import *

SAFE_TOP_Y = 2.55
SAFE_BOTTOM_Y = -3.25
CONTENT_TOP_Y = 2.20
CONTENT_BOTTOM_Y = -2.95


def large_view_card(key: str, width: float = 6.4, height: float = 4.25,
                    scale: float = 0.82, dimensions: bool = False,
                    title_size: int = 23) -> VGroup:
    """Large technical view intended for one-view-at-a-time explanation."""
    spec = VIEW_SPECS[key]
    panel = RoundedRectangle(
        width=width, height=height, corner_radius=0.15,
        stroke_color=LIGHT, stroke_width=1.45,
        fill_color=PAPER, fill_opacity=1,
    )
    accent = Line(
        panel.get_corner(UL) + RIGHT * 0.22,
        panel.get_corner(UR) + LEFT * 0.22,
        stroke_color=spec.accent, stroke_width=5,
    )
    title = safe_text(spec.label, title_size, spec.accent, BOLD, width - 0.55)
    title.next_to(panel.get_top(), DOWN, buff=0.22)
    view = orthographic_view(key, scale, dimensions)
    if view.width > width - 0.55:
        view.scale_to_fit_width(width - 0.55)
    if view.height > height - 1.05:
        view.scale_to_fit_height(height - 1.05)
    view.move_to(panel).shift(DOWN * 0.12)
    return VGroup(panel, accent, title, view)


def safe_bottom_callout(text: str, color: str = BLUE, width: float = 6.4,
                        size: int = 21) -> VGroup:
    c = callout(text, color, width, size)
    c.move_to([0, -3.52, 0])
    return c


def safe_top_tag(text: str, color: str = BLUE, width: float = 4.6,
                 size: int = 20) -> VGroup:
    c = callout(text, color, width, size)
    c.move_to([0, 2.42, 0])
    return c


def floating_view_label(text: str, color: str = BLUE) -> VGroup:
    """Small fixed-frame perspective label, deliberately away from headers."""
    b = badge(text, color, 18)
    b.to_corner(DL, buff=0.48).shift(UP * 0.22)
    return b


def view_reveal_frame(key: str, accent: str | None = None,
                      width: float = 8.0, height: float = 5.15,
                      dimensions: bool = False) -> VGroup:
    """Presentation board for a full-size orthographic reveal."""
    accent = accent or VIEW_SPECS[key].accent
    board = RoundedRectangle(
        width=width, height=height, corner_radius=0.18,
        stroke_color=accent, stroke_width=1.8,
        fill_color=PAPER, fill_opacity=0.985,
    )
    view = large_view_card(key, width - 0.38, height - 0.38, 0.92, dimensions, 25)
    view.move_to(board)
    return VGroup(board, view)


def observer_sequence_strip(first_angle: bool = True, color: str = ORANGE) -> VGroup:
    """Observer/plane/object schematic with equal spacing and no text collision."""
    eye = observer_icon(color, 0.72)
    plane = RoundedRectangle(width=0.14, height=2.9, corner_radius=0.04,
                             stroke_color=BLUE, stroke_width=1.7,
                             fill_color=PALE_BLUE, fill_opacity=0.55)
    obj = orthographic_view("front", 0.35)
    if first_angle:
        elems = [eye, obj, plane]
        labels = ["OBSERVADOR", "OBJETO", "PLANO"]
    else:
        elems = [eye, plane, obj]
        labels = ["OBSERVADOR", "PLANO", "OBJETO"]
    groups = VGroup()
    for e, label in zip(elems, labels):
        tag = badge(label, color if label != "PLANO" else BLUE, 15)
        groups.add(VGroup(e, tag).arrange(DOWN, buff=0.22))
    groups.arrange(RIGHT, buff=1.65)
    arrows = VGroup()
    for a, b in zip(groups[:-1], groups[1:]):
        arrows.add(Arrow(a.get_right() + RIGHT * 0.18,
                         b.get_left() + LEFT * 0.18,
                         buff=0.05, stroke_width=2.2,
                         max_tip_length_to_length_ratio=0.13,
                         color=color))
    return VGroup(groups, arrows)


def split_comparison_panel() -> tuple[VGroup, VGroup, Line]:
    left = RoundedRectangle(width=7.2, height=5.7, corner_radius=0.16,
                            stroke_color=ORANGE, stroke_width=1.45,
                            fill_color=PAPER, fill_opacity=1)
    right = RoundedRectangle(width=7.2, height=5.7, corner_radius=0.16,
                             stroke_color=TEAL, stroke_width=1.45,
                             fill_color=PAPER, fill_opacity=1)
    left.move_to([-3.75, -0.25, 0]); right.move_to([3.75, -0.25, 0])
    div = Line([0, 2.65, 0], [0, -3.25, 0], color=LIGHT, stroke_width=1.5)
    return VGroup(left), VGroup(right), div


def progress_dots(count: int = 6, active: int = 0) -> VGroup:
    dots = VGroup(*[
        Dot(radius=0.07, color=BLUE if i == active else LIGHT)
        for i in range(count)
    ]).arrange(RIGHT, buff=0.12)
    dots.move_to([0, -3.78, 0])
    return dots
