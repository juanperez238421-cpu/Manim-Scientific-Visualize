"""Reusable visual primitives for the first month of Multivariable Calculus.

Target: Manim Community Edition 0.20.1.
The module intentionally avoids external assets and absolute paths.
"""
from __future__ import annotations

from manim import *
import numpy as np

# 16:9 / 1080p30 when rendered with -pqh.
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#F7F8FA"

BG = "#F7F8FA"
INK = "#111827"
MUTED = "#64748B"
BLUE = "#2563EB"
CYAN = "#0891B2"
GREEN = "#059669"
ORANGE = "#EA580C"
RED = "#DC2626"
PURPLE = "#7C3AED"
YELLOW = "#CA8A04"
GRID = "#CBD5E1"


def prepare_scene(scene: Scene) -> None:
    scene.camera.background_color = BG


def title_group(kicker: str, title: str, subtitle: str | None = None) -> VGroup:
    """Compact title block that stays inside the 16:9 safe area."""
    k = Text(kicker.upper(), font_size=22, color=BLUE, weight=BOLD)
    t = Text(title, font_size=38, color=INK, weight=BOLD)
    items = [k, t]
    if subtitle:
        items.append(Text(subtitle, font_size=22, color=MUTED))
    group = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    group.to_corner(UL, buff=0.38)
    return group


def footer(label: str = "Cálculo de varias variables · Mes 1") -> Text:
    return Text(label, font_size=18, color=MUTED).to_corner(DR, buff=0.28)


def equation_card(*lines: Mobject, width: float = 6.0) -> VGroup:
    content = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    bg = RoundedRectangle(
        corner_radius=0.18,
        width=max(width, content.width + 0.6),
        height=content.height + 0.45,
        stroke_color=GRID,
        stroke_width=1.4,
        fill_color=WHITE,
        fill_opacity=0.94,
    )
    return VGroup(bg, content)


def section_badge(text: str, color: str = BLUE) -> VGroup:
    txt = Text(text, font_size=20, color=WHITE, weight=BOLD)
    box = RoundedRectangle(
        corner_radius=0.15,
        width=txt.width + 0.42,
        height=txt.height + 0.25,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    )
    txt.move_to(box)
    return VGroup(box, txt)


def clean_number_plane(x_range=(-5, 6, 1), y_range=(-4, 5, 1), size=0.82) -> NumberPlane:
    plane = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        background_line_style={"stroke_color": GRID, "stroke_opacity": 0.55, "stroke_width": 1},
        axis_config={"color": INK, "stroke_width": 2},
    )
    return plane.scale(size)


def component_guides(plane: NumberPlane, end: np.ndarray, color: str = BLUE) -> VGroup:
    x, y = float(end[0]), float(end[1])
    vertical = DashedLine(plane.c2p(x, 0), plane.c2p(x, y), color=MUTED, dash_length=0.12)
    horizontal = DashedLine(plane.c2p(0, y), plane.c2p(x, y), color=MUTED, dash_length=0.12)
    x_label = MathTex(fr"{x:g}", color=color).scale(0.58).next_to(plane.c2p(x, 0), DOWN, buff=0.12)
    y_label = MathTex(fr"{y:g}", color=color).scale(0.58).next_to(plane.c2p(0, y), LEFT, buff=0.12)
    return VGroup(vertical, horizontal, x_label, y_label)


def vector2d(plane: NumberPlane, end: np.ndarray, color: str = BLUE, buff: float = 0.0) -> Arrow:
    return Arrow(plane.c2p(0, 0), plane.c2p(end[0], end[1]), buff=buff, color=color, stroke_width=7)


def standard_3d_axes(length: float = 5.2) -> ThreeDAxes:
    axes = ThreeDAxes(
        x_range=[-3, 3, 1],
        y_range=[-3, 3, 1],
        z_range=[-2, 4, 1],
        x_length=length,
        y_length=length,
        z_length=4.4,
        axis_config={"color": INK, "stroke_width": 2},
    )
    return axes


def line3d_from_origin(axes: ThreeDAxes, coords: tuple[float, float, float], color: str = BLUE) -> Line3D:
    return Line3D(
        start=axes.c2p(0, 0, 0),
        end=axes.c2p(*coords),
        color=color,
        thickness=0.035,
    )


def fixed_overlay(scene: ThreeDScene, *mobjects: Mobject) -> None:
    scene.add_fixed_in_frame_mobjects(*mobjects)


def fade_scene(scene: Scene, run_time: float = 0.8) -> None:
    if scene.mobjects:
        scene.play(*[FadeOut(mob) for mob in list(scene.mobjects)], run_time=run_time)
