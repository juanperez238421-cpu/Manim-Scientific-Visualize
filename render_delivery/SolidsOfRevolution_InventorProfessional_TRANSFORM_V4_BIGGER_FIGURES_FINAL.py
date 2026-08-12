#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior V4 — Solids of Revolution for Autodesk Inventor Professional.

Calculus-free college-level ManimCE lesson. The central model is always:
PROFILE -> AXIS -> ANGLE -> OPERATION -> SOLID.

V4 keeps the dedicated geometric sweep engine and enlarges the visual geometry: the *actual 2D generating area*
rotates in 3D, selected points leave circular trajectories, and those traces
resolve into the final revolved surface. This preserves the causal connection
between sketch and solid instead of cutting from one object to the other.

Designed for Manim Community Edition 0.20.x and the JP classroom visual system.
"""
from __future__ import annotations

import math
import os
from typing import Sequence

import numpy as np
from manim import *

from jp_classroom_style import (
    JPThreeDClassroomScene,
    BLACK_TEXT, BLACK_LINE, DARK_GRAY, MID_GRAY, LIGHT_GRAY,
    VERY_LIGHT_GRAY, PAPER_GRAY, WHITE_FILL,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

# Senior V4 visual enlargement: preserve all lesson logic and proportions while
# increasing the effective size of every 2D generator and 3D revolved body.
GEOMETRY_SCALE = 1.22


# -----------------------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------------------
def profile_interp(points: Sequence[tuple[float, float]], t: float) -> tuple[float, float]:
    pts = np.array(points, dtype=float)
    seg = np.diff(pts, axis=0)
    lengths = np.sqrt(np.sum(seg * seg, axis=1))
    total = float(np.sum(lengths))
    if total <= 1e-12:
        return float(pts[0, 0]), float(pts[0, 1])
    s = np.clip(t, 0.0, 1.0) * total
    acc = 0.0
    for i, length in enumerate(lengths):
        if s <= acc + length or i == len(lengths) - 1:
            q = 0.0 if length <= 1e-12 else (s - acc) / length
            p = pts[i] + q * seg[i]
            return float(p[0]), float(p[1])
        acc += length
    return float(pts[-1, 0]), float(pts[-1, 1])


def revolution_surface(profile, angle=TAU, opacity=0.50, resolution=(28, 16), color=GRAY_C):
    def f(u, v):
        r, y = profile_interp(profile, v)
        return np.array([GEOMETRY_SCALE * r * math.cos(u), GEOMETRY_SCALE * y, GEOMETRY_SCALE * r * math.sin(u)])
    return Surface(
        f, u_range=[0, angle], v_range=[0, 1], resolution=resolution,
        fill_color=color, fill_opacity=opacity,
        stroke_color=GRAY_B, stroke_width=0.65,
    )


def revolution_cap(y, radius, angle=TAU, opacity=0.28):
    def f(u, v):
        rr = GEOMETRY_SCALE * radius * v
        return np.array([rr * math.cos(u), GEOMETRY_SCALE * y, rr * math.sin(u)])
    return Surface(
        f, u_range=[0, angle], v_range=[0, 1], resolution=(24, 5),
        fill_color=GRAY_D, fill_opacity=opacity,
        stroke_color=GRAY_B, stroke_width=0.50,
    )


def sphere_surface(radius=1.25):
    def f(u, v):
        return np.array([
            GEOMETRY_SCALE * radius * math.sin(v) * math.cos(u),
            GEOMETRY_SCALE * radius * math.cos(v),
            GEOMETRY_SCALE * radius * math.sin(v) * math.sin(u),
        ])
    return Surface(
        f, u_range=[0, TAU], v_range=[0, PI], resolution=(30, 16),
        fill_color=GRAY_C, fill_opacity=0.50,
        stroke_color=GRAY_B, stroke_width=0.60,
    )


def closed_profile_polygon(profile, opacity=0.50, axis_radius=0.0):
    pts = [np.array([GEOMETRY_SCALE * axis_radius, GEOMETRY_SCALE * profile[0][1], 0.0])]
    pts.extend(np.array([GEOMETRY_SCALE * r, GEOMETRY_SCALE * y, 0.0]) for r, y in profile)
    pts.append(np.array([GEOMETRY_SCALE * axis_radius, GEOMETRY_SCALE * profile[-1][1], 0.0]))
    return Polygon(
        *pts, stroke_color=BLACK_LINE, stroke_width=2.5,
        fill_color=LIGHT_GRAY, fill_opacity=opacity,
    )


def closed_ring_profile(outer_profile, inner_radius, opacity=0.45):
    outer = [np.array([GEOMETRY_SCALE * r, GEOMETRY_SCALE * y, 0]) for r, y in outer_profile]
    inner = [np.array([GEOMETRY_SCALE * inner_radius, GEOMETRY_SCALE * y, 0]) for _, y in reversed(outer_profile)]
    return Polygon(
        *(outer + inner), stroke_color=BLACK_LINE, stroke_width=2.4,
        fill_color=LIGHT_GRAY, fill_opacity=opacity,
    )


def axis_line(y0=-2.5, y1=2.5):
    return DashedLine(
        np.array([0, GEOMETRY_SCALE * y0, 0]), np.array([0, GEOMETRY_SCALE * y1, 0]),
        color=BLACK_LINE, stroke_width=2.7, dash_length=0.12,
    )


def arrow_between(a, b):
    return Arrow(a, b, buff=0.10, color=BLACK_LINE, stroke_width=2.4, max_tip_length_to_length_ratio=0.16)


# -----------------------------------------------------------------------------
# SPECIALIZED GEOMETRIC SWEEP ENGINE
# -----------------------------------------------------------------------------
def profile_curve(profile, color=BLACK_LINE, stroke_width=3.0, opacity=1.0):
    """Outer generating curve r(y) drawn in the sketch plane z=0."""
    curve = VMobject(color=color, stroke_width=stroke_width)
    curve.set_points_as_corners([np.array([GEOMETRY_SCALE * r, GEOMETRY_SCALE * y, 0.0]) for r, y in profile])
    curve.set_stroke(opacity=opacity)
    return curve


def orbit_curve(radius, y, start_angle=0.0, end_angle=TAU, color=MID_GRAY, opacity=0.42):
    """Exact circular trajectory of one profile point around the Y axis."""
    if radius <= 1e-6:
        # A point on the axis has no orbit. Return a tiny invisible placeholder.
        return ParametricFunction(
            lambda t: np.array([0.0, GEOMETRY_SCALE * y, 0.0]),
            t_range=[0.0, 1.0], color=color, stroke_opacity=0.0,
        )
    return ParametricFunction(
        lambda a: np.array([GEOMETRY_SCALE * radius * math.cos(a), GEOMETRY_SCALE * y, GEOMETRY_SCALE * radius * math.sin(a)]),
        t_range=[start_angle, end_angle],
        color=color, stroke_width=1.65, stroke_opacity=opacity,
    )


def annular_cap(y, inner_radius, outer_radius, angle=TAU, opacity=0.26, color=GRAY_D):
    """Flat annulus used to close hollow revolved bodies or rectangular cut volumes."""
    def f(u, v):
        rr = GEOMETRY_SCALE * (inner_radius + (outer_radius - inner_radius) * v)
        return np.array([rr * math.cos(u), GEOMETRY_SCALE * y, rr * math.sin(u)])
    return Surface(
        f, u_range=[0, angle], v_range=[0, 1], resolution=(28, 5),
        fill_color=color, fill_opacity=opacity,
        stroke_color=GRAY_B, stroke_width=0.45,
    )


class RevolveSweepEngine:
    """Reusable animation system for a true profile -> sweep -> solid transition.

    The engine deliberately shows the geometric mechanism rather than using a
    simple cross-fade. A translucent 2D region is rotated about the selected
    axis while sample points on its generating boundary draw their exact
    circular trajectories. Only after the sweep is visually established does
    the wire/sweep evidence resolve into a continuous surface.
    """

    def __init__(self, scene):
        self.scene = scene

    @staticmethod
    def sample_points(profile, count=7):
        # Include the vertices (important for shoulders) plus evenly spaced
        # path samples. Deduplicate to keep the wireframe readable.
        raw = list(profile)
        raw.extend(profile_interp(profile, t) for t in np.linspace(0.08, 0.92, max(0, count)))
        out = []
        for r, y in raw:
            key = (round(float(r), 3), round(float(y), 3))
            if key not in {(round(a, 3), round(b, 3)) for a, b in out}:
                out.append((float(r), float(y)))
        # Limit clutter while prioritizing true profile corners.
        if len(out) > 12:
            vertices = list(profile)
            extras = [p for p in out if p not in vertices]
            step = max(1, len(extras) // max(1, 12 - len(vertices)))
            out = vertices + extras[::step][:max(0, 12 - len(vertices))]
        return out

    def traces(self, profile, start_angle=0.0, end_angle=TAU, count=7, opacity=0.40):
        return VGroup(*[
            orbit_curve(r, y, start_angle, end_angle, opacity=opacity)
            for r, y in self.sample_points(profile, count=count)
            if r > 1e-5
        ])

    def final_solid(self, profile, angle=TAU, opacity=0.53, caps=True, resolution=(32, 18), color=GRAY_C):
        pieces = [revolution_surface(profile, angle, opacity, resolution=resolution, color=color)]
        if caps:
            r0, y0 = profile[0]
            r1, y1 = profile[-1]
            if r0 > 1e-5:
                pieces.append(revolution_cap(y0, r0, angle, 0.24))
            if r1 > 1e-5:
                pieces.append(revolution_cap(y1, r1, angle, 0.24))
        return VGroup(*pieces)

    def hollow_solid(self, outer_profile, inner_profile, opacity=0.48, resolution=(32, 18)):
        y0 = outer_profile[0][1]
        y1 = outer_profile[-1][1]
        rin0 = inner_profile[0][0]
        rout0 = outer_profile[0][0]
        rin1 = inner_profile[-1][0]
        rout1 = outer_profile[-1][0]
        return VGroup(
            revolution_surface(outer_profile, TAU, opacity, resolution=resolution, color=GRAY_C),
            revolution_surface(inner_profile, TAU, 0.24, resolution=resolution, color=GRAY_D),
            annular_cap(y0, rin0, rout0, opacity=0.24),
            annular_cap(y1, rin1, rout1, opacity=0.24),
        )

    def animate_full_revolve(
        self,
        region,
        profile,
        *,
        angle=TAU,
        duration=4.0,
        trace_count=7,
        final_solid=None,
        surface_opacity=0.53,
        caps=True,
        keep_axis=None,
        completion_pause=0.55,
    ):
        """Rotate the *visible* 2D region and simultaneously draw its sweep."""
        scene = self.scene
        traces = self.traces(profile, 0.0, angle, count=trace_count, opacity=0.44)
        generating_curve = profile_curve(profile, stroke_width=3.5)
        scene.add(generating_curve)

        # Rotate both the filled area and its outer generator. Every orbit is
        # drawn over the same time interval, so the geometry is temporally linked.
        scene.play(
            Rotate(region, angle, axis=UP, about_point=ORIGIN),
            Rotate(generating_curve, angle, axis=UP, about_point=ORIGIN),
            AnimationGroup(*[Create(t) for t in traces], lag_ratio=0.0),
            run_time=duration,
            rate_func=linear,
        )
        scene.wait(completion_pause)

        solid = final_solid or self.final_solid(
            profile, angle=angle, opacity=surface_opacity, caps=caps,
        )
        # Resolve the construction evidence into the CAD-like skin.
        scene.play(
            FadeIn(solid),
            region.animate.set_opacity(0.08),
            generating_curve.animate.set_stroke(opacity=0.20),
            traces.animate.set_stroke(opacity=0.12),
            run_time=1.05,
        )
        scene.play(FadeOut(region), FadeOut(generating_curve), FadeOut(traces), run_time=0.55)
        if keep_axis is not None:
            scene.bring_to_front(keep_axis)
        return solid

    def animate_angle_progression(self, region, profile, labels, durations=(1.5, 1.6, 2.1)):
        """Continue one physical generator through 90°, 180°, then 360°."""
        scene = self.scene
        targets = (PI / 2, PI, TAU)
        current = 0.0
        surface = None
        generating_curve = profile_curve(profile, stroke_width=3.3)
        scene.add(generating_curve)
        for i, (target, lab, runtime) in enumerate(zip(targets, labels, durations)):
            delta = target - current
            segment_traces = self.traces(profile, current, target, count=6, opacity=0.42)
            scene.add_fixed_in_frame_mobjects(lab)
            if i == 0:
                scene.play(FadeIn(lab), run_time=0.45)
            else:
                scene.play(ReplacementTransform(labels[i - 1], lab), run_time=0.45)
            scene.play(
                Rotate(region, delta, axis=UP, about_point=ORIGIN),
                Rotate(generating_curve, delta, axis=UP, about_point=ORIGIN),
                AnimationGroup(*[Create(t) for t in segment_traces], lag_ratio=0.0),
                run_time=runtime,
                rate_func=linear,
            )
            new_surface = self.final_solid(profile, angle=target, opacity=0.48, caps=(target >= TAU - 1e-6))
            if surface is None:
                surface = new_surface
                scene.play(FadeIn(surface), segment_traces.animate.set_stroke(opacity=0.10), run_time=0.65)
            else:
                scene.play(Transform(surface, new_surface), segment_traces.animate.set_stroke(opacity=0.10), run_time=0.70)
            scene.play(FadeOut(segment_traces), run_time=0.30)
            scene.wait(0.70)
            current = target
        scene.play(FadeOut(region), FadeOut(generating_curve), run_time=0.45)
        return surface

    def animate_cut_revolve(self, cut_region, cut_profile_outer, cut_profile_inner, shaft_before, shaft_after, duration=3.2):
        """Sweep a rectangular cut region and then apply the exact subtraction."""
        scene = self.scene
        all_trace_profile = [
            cut_profile_outer[0], cut_profile_outer[-1],
            cut_profile_inner[0], cut_profile_inner[-1],
        ]
        traces = VGroup(*[
            orbit_curve(r, y, 0.0, TAU, opacity=0.46)
            for r, y in all_trace_profile
        ])
        cut_volume = VGroup(
            revolution_surface(cut_profile_outer, TAU, 0.20, resolution=(28, 14), color=GRAY_B),
            revolution_surface(cut_profile_inner, TAU, 0.15, resolution=(28, 14), color=GRAY_D),
            annular_cap(cut_profile_outer[0][1], cut_profile_inner[0][0], cut_profile_outer[0][0], opacity=0.18),
            annular_cap(cut_profile_outer[-1][1], cut_profile_inner[-1][0], cut_profile_outer[-1][0], opacity=0.18),
        )
        scene.play(
            Rotate(cut_region, TAU, axis=UP, about_point=ORIGIN),
            AnimationGroup(*[Create(t) for t in traces], lag_ratio=0.0),
            run_time=duration,
            rate_func=linear,
        )
        scene.play(FadeIn(cut_volume), cut_region.animate.set_opacity(0.06), traces.animate.set_opacity(0.14), run_time=0.85)
        scene.wait(0.65)
        scene.play(
            Transform(shaft_before, shaft_after),
            FadeOut(cut_volume), FadeOut(cut_region), FadeOut(traces),
            run_time=1.25,
        )
        return shaft_before


class SolidsOfRevolutionInventorSeniorV3(JPThreeDClassroomScene):
    def validate_lesson_data(self):
        assert abs(TAU - 2 * PI) < 1e-12
        assert 0 < PI / 2 < PI < TAU

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def fixed(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)

    def fit(self, mob, max_w=14.5, max_h=7.5):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def section_header(self, n, title, subtitle):
        badge = RoundedRectangle(
            width=0.72, height=0.52, corner_radius=0.09,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        num = self.text(f"{n:02d}", 22, BOLD).move_to(badge)
        head = self.text(title, 31, BOLD)
        self.fit(head, 13.1, 0.58)
        row = VGroup(VGroup(badge, num), head).arrange(RIGHT, buff=0.22)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, color=LIGHT_GRAY, stroke_width=1.8)
        rule.next_to(row, DOWN, buff=0.06)
        sub = self.text(subtitle, 20)
        self.fit(sub, 14.2, 0.55)
        sub.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def pill(self, text, size=22, width=None):
        t = self.text(text, size, BOLD)
        w = max(t.width + 0.45, width or 0)
        box = RoundedRectangle(
            width=w, height=0.58, corner_radius=0.18,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        t.move_to(box)
        return VGroup(box, t)

    def note(self, title, lines, width=5.6, body_size=21):
        h = self.text(title, 24, BOLD)
        body = VGroup(*[self.text(x, body_size) for x in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(h, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.55, 3.1)
        box = RoundedRectangle(
            width=width, height=max(1.35, content.height + 0.54),
            corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=0.97,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def cad_parameter_row(self, label, value, width=5.6):
        lab = self.text(label, 20, BOLD)
        val = self.text(value, 20)
        field = RoundedRectangle(
            width=3.20, height=0.55, corner_radius=0.06,
            stroke_color=MID_GRAY, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=1,
        )
        val.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.17)
        row = VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.24)
        row.scale_to_fit_width(width)
        return row

    def cad_panel(self):
        title = VGroup(self.text("REVOLVE", 25, BOLD), self.text("Inventor mental model", 18)).arrange(DOWN, buff=0.04)
        rows = VGroup(
            self.cad_parameter_row("Profile", "Closed sketch region"),
            self.cad_parameter_row("Axis", "Centerline"),
            self.cad_parameter_row("Extent", "Full"),
            self.cad_parameter_row("Angle", "360 deg"),
            self.cad_parameter_row("Operation", "New Solid"),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        ok = self.pill("OK", 20, width=1.05)
        cancel = self.pill("Cancel", 18, width=1.35)
        buttons = VGroup(ok, cancel).arrange(RIGHT, buff=0.18)
        content = VGroup(title, rows, buttons).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        box = RoundedRectangle(
            width=6.35, height=4.55, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color="#FAFAFA", fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.32)
        return VGroup(box, content)

    def clear_scene(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.65)
        for m in mobs:
            self.remove(m)

    def profile_panel_2d(self, profile, title, caption, scale=0.85, x=-4.6, y=-0.30, ring_inner=None):
        if ring_inner is None:
            region = closed_profile_polygon(profile, 0.52)
        else:
            region = closed_ring_profile(profile, ring_inner, 0.50)
        ax = axis_line(min(y for _, y in profile) - 0.35, max(y for _, y in profile) + 0.35)
        g = VGroup(ax, region).scale(scale).move_to(np.array([x, y, 0]))
        lab = VGroup(self.text(title, 22, BOLD), self.text(caption, 18)).arrange(DOWN, buff=0.05)
        lab.move_to(np.array([x, -3.00, 0]))
        self.fixed(lab)
        return g, lab

    # ------------------------------------------------------------------
    # Lesson
    # ------------------------------------------------------------------
    def construct(self):
        self.sweep = RevolveSweepEngine(self)
        self.opening()
        self.core_idea()
        self.angle_logic()
        self.profile_to_solid_library()
        self.inventor_workflow()
        self.stepped_shaft_example()
        self.revolved_cut_example()
        self.no_calculus_check()
        self.final_design_challenge()
        self.closing()

    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        title = self.text("SOLIDS OF REVOLUTION", 52, BOLD)
        line = Line(LEFT * 5.7, RIGHT * 5.7, color=BLACK_LINE, stroke_width=2)
        sub = self.text("Inventor Professional · from a 2D profile to an axisymmetric 3D part", 26)
        promise = self.text("No integral calculus: learn the geometry and the CAD decision process first.", 25, MEDIUM)
        route = VGroup(
            self.pill("PROFILE", 22), self.pill("AXIS", 22), self.pill("ANGLE", 22),
            self.pill("OPERATION", 22), self.pill("SOLID", 22),
        ).arrange(RIGHT, buff=0.20)
        arrows = VGroup(*[
            arrow_between(route[i].get_right(), route[i+1].get_left()) for i in range(len(route)-1)
        ])
        path = VGroup(route, arrows)
        group = VGroup(title, line, sub, promise, path).arrange(DOWN, buff=0.34)
        self.fixed(group)
        self.play(FadeIn(title, shift=UP * 0.12), Create(line), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(promise), run_time=0.8)
        self.wait(1.8)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.08) for p in route], lag_ratio=0.12), Create(arrows), run_time=1.9)
        self.wait(3.0)
        self.clear_scene()

    def core_idea(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        h = self.section_header(
            1,
            "THE 2D AREA PHYSICALLY SWEEPS THE 3D SPACE",
            "Watch the same profile rotate: its points draw circles, those circles form a skin, and the skin becomes the solid.",
        )
        self.fixed(h); self.play(FadeIn(h), run_time=0.7)

        profile = [(1.55, -1.35), (1.55, 1.35)]
        origin_shift = LEFT * 3.35
        region = closed_profile_polygon(profile, 0.58).shift(origin_shift)
        ax = axis_line(-1.85, 1.85).shift(origin_shift)
        radius = Line(LEFT * 3.35, LEFT * 3.35 + RIGHT * (1.55 * GEOMETRY_SCALE), color=BLACK_LINE, stroke_width=2.4).shift(DOWN * 0.62)
        rlab = MathTex("r", color=BLACK_TEXT, font_size=38).next_to(radius, UP, buff=0.05)
        profile_lab = self.pill("GENERATING AREA", 20).move_to(LEFT * 3.35 + DOWN * 2.70)
        axis_lab = self.pill("AXIS", 20).move_to(LEFT * 0.60 + DOWN * 2.70)
        self.fixed(rlab, profile_lab, axis_lab)

        self.play(Create(ax), FadeIn(region), run_time=1.1)
        self.play(Create(radius), FadeIn(rlab), FadeIn(profile_lab), FadeIn(axis_lab), run_time=0.9)
        self.wait(2.0)

        explanation = self.note(
            "THE MOTION TO LOOK FOR",
            ["1. The area stays rigid.", "2. It rotates about the centerline.", "3. Every boundary point traces a circle."],
            width=5.6,
        ).move_to(RIGHT * 3.7 + DOWN * 0.15)
        self.fixed(explanation); self.play(FadeIn(explanation), run_time=0.7); self.wait(2.3)
        self.play(FadeOut(explanation), FadeOut(profile_lab), FadeOut(axis_lab), FadeOut(radius), FadeOut(rlab), run_time=0.5)

        # One continuous transition: camera tilts while the exact sketch moves onto the 3D axis.
        self.move_camera(
            phi=66 * DEGREES, theta=-48 * DEGREES, zoom=1.00,
            added_anims=[region.animate.shift(-origin_shift), ax.animate.shift(-origin_shift)],
            run_time=1.6,
        )
        self.wait(0.5)
        solid = self.sweep.animate_full_revolve(
            region, profile, duration=4.2, trace_count=8, keep_axis=ax,
        )
        takeaway = self.text(
            "This is Revolve: the 3D surface is the history of the moving 2D generator.", 27, BOLD
        ).to_edge(DOWN, buff=0.32)
        self.fit(takeaway, 14.0, 0.58); self.fixed(takeaway)
        self.play(FadeIn(takeaway), run_time=0.75); self.wait(3.1)
        self.clear_scene()

    def angle_logic(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        h = self.section_header(
            2,
            "ONE GENERATOR CONTINUES FROM 90° TO 180° TO 360°",
            "Do not imagine three different solids: it is the same 2D area continuing farther around the same axis.",
        )
        self.fixed(h); self.play(FadeIn(h), run_time=0.7)
        profile = [(1.45, -1.25), (1.45, 1.25)]
        shift = LEFT * 3.0
        region = closed_profile_polygon(profile, 0.52).shift(shift)
        ax = axis_line(-1.75, 1.75).shift(shift)
        intro = self.note("ANGLE = TRAVEL", ["90° = quarter turn", "180° = half turn", "360° = complete turn"], width=5.4).move_to(RIGHT*3.7+DOWN*0.2)
        self.fixed(intro)
        self.play(Create(ax), FadeIn(region), FadeIn(intro), run_time=1.0); self.wait(2.4)
        self.play(FadeOut(intro), run_time=0.45)
        self.move_camera(
            phi=64*DEGREES, theta=-50*DEGREES, zoom=1.00,
            added_anims=[region.animate.shift(-shift), ax.animate.shift(-shift)],
            run_time=1.5,
        )
        labels = []
        for deg, caption in [(90, "quarter sweep"), (180, "half sweep"), (360, "full sweep")]:
            lab = VGroup(self.text(f"{deg}°", 34, BOLD), self.text(caption, 21)).arrange(DOWN, buff=0.05).to_corner(DL, buff=0.55)
            labels.append(lab)
        surface = self.sweep.animate_angle_progression(region, profile, labels)
        rule = self.note(
            "IN INVENTOR",
            ["Full / 360° closes the axisymmetric part.", "A partial angle is a deliberate design choice, not a different command."],
            width=6.0,
        ).to_corner(DR, buff=0.45)
        self.fixed(rule); self.play(FadeIn(rule), run_time=0.75); self.wait(3.4)
        self.clear_scene()

    def profile_to_solid_library(self):
        # Each example is now animated independently so the student watches
        # the generating profile produce its own solid instead of seeing a static pair.
        examples = [
            ([(1.15, -1.35), (1.15, 1.35)], "RECTANGLE", "CYLINDER", True),
            ([(1.28, -1.35), (0.0, 1.35)], "TRIANGLE", "CONE", True),
            ([(1.25 * math.sin(t), 1.25 * math.cos(t)) for t in np.linspace(PI, 0, 18)], "SEMICIRCLE", "SPHERE", False),
        ]
        for index, (profile, ptitle, stitle, caps) in enumerate(examples, start=3):
            self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1)
            h = self.section_header(
                index,
                f"{ptitle} PROFILE → {stitle}",
                "The silhouette of the final 3D object is already encoded in the side profile before the Revolve command is used.",
            )
            self.fixed(h); self.play(FadeIn(h), run_time=0.65)
            shift = LEFT * 3.4
            region = closed_profile_polygon(profile, 0.54).shift(shift)
            ax = axis_line(min(y for _, y in profile)-0.35, max(y for _, y in profile)+0.35).shift(shift)
            label = VGroup(
                self.pill("2D CLOSED REGION", 19),
                self.text(f"Rotate it 360° → {stitle.lower()}", 24, BOLD),
            ).arrange(DOWN, buff=0.20).move_to(RIGHT*3.4+DOWN*0.2)
            self.fixed(label)
            self.play(Create(ax), FadeIn(region), FadeIn(label), run_time=1.0); self.wait(2.2)
            self.play(FadeOut(label), run_time=0.4)
            self.move_camera(
                phi=64*DEGREES, theta=-48*DEGREES, zoom=1.00,
                added_anims=[region.animate.shift(-shift), ax.animate.shift(-shift)],
                run_time=1.45,
            )
            solid = self.sweep.animate_full_revolve(
                region, profile, duration=3.5 if stitle != "SPHERE" else 4.0,
                trace_count=7, caps=caps, keep_axis=ax,
                surface_opacity=0.52,
            )
            final_lab = self.text(f"{ptitle}  →  360° REVOLVE  →  {stitle}", 28, BOLD).to_edge(DOWN, buff=0.30)
            self.fit(final_lab, 13.5, 0.58); self.fixed(final_lab)
            self.play(FadeIn(final_lab), run_time=0.65); self.wait(2.6)
            self.clear_scene()

        # Hollow-body example: both the outer and inner boundaries are swept.
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1)
        h = self.section_header(
            6,
            "OFFSET PROFILE → HOLLOW REVOLVED BODY",
            "When the closed area stays away from the axis, its inner boundary also sweeps a surface and creates the bore.",
        )
        self.fixed(h); self.play(FadeIn(h), run_time=0.65)
        outer = [(1.55, -1.25), (1.55, 1.25)]
        inner = [(0.82, -1.25), (0.82, 1.25)]
        shift = LEFT * 3.2
        ring = closed_ring_profile(outer, 0.82, 0.52).shift(shift)
        ax = axis_line(-1.7, 1.7).shift(shift)
        gap = DoubleArrow(LEFT*3.2, LEFT*3.2 + RIGHT*(0.82*GEOMETRY_SCALE), buff=0, color=BLACK_LINE, stroke_width=2.0)
        gaplab = self.text("inner radius", 21, BOLD).next_to(gap, DOWN, buff=0.10)
        self.fixed(gaplab)
        self.play(Create(ax), FadeIn(ring), Create(gap), FadeIn(gaplab), run_time=1.05); self.wait(2.3)
        self.play(FadeOut(gap), FadeOut(gaplab), run_time=0.4)
        self.move_camera(
            phi=66*DEGREES, theta=-48*DEGREES, zoom=1.00,
            added_anims=[ring.animate.shift(-shift), ax.animate.shift(-shift)],
            run_time=1.45,
        )
        hollow = self.sweep.hollow_solid(outer, inner)
        # Draw trajectories from both the outer and inner profile simultaneously.
        traces = VGroup(self.sweep.traces(outer, count=5), self.sweep.traces(inner, count=5, opacity=0.34))
        self.play(
            Rotate(ring, TAU, axis=UP, about_point=ORIGIN),
            AnimationGroup(*[Create(t) for group in traces for t in group], lag_ratio=0.0),
            run_time=4.0, rate_func=linear,
        )
        self.play(FadeIn(hollow), ring.animate.set_opacity(0.07), traces.animate.set_opacity(0.10), run_time=1.0)
        self.play(FadeOut(ring), FadeOut(traces), run_time=0.5)
        note = self.note(
            "ENGINEERING READING",
            ["Outer radius → outside diameter", "Inner radius → bore", "One annular sketch can define both."],
            width=5.9,
        ).to_corner(DR, buff=0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.7); self.wait(3.2)
        self.clear_scene()

    def inventor_workflow(self):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=self.section_header(7,"INVENTOR WORKFLOW: THE COMMAND ONLY EXECUTES THE GEOMETRY",
                              "Profile, axis, extent and operation are geometric decisions first; the dialog simply records those decisions.")
        self.fixed(h);self.play(FadeIn(h),run_time=0.7)
        panel=self.cad_panel().move_to(RIGHT*3.55+DOWN*0.35)
        self.fixed(panel)
        profile=[(1.25,-1.45),(1.25,-0.25),(0.85,-0.25),(0.85,1.35)]
        sketch=closed_profile_polygon(profile,0.53).scale(1.14).move_to(LEFT*3.45+DOWN*0.30)
        ax=axis_line(-2.0,2.0).scale(1.14).move_to(LEFT*3.45+DOWN*0.30)
        p_lab=self.pill("PROFILE",20).move_to(LEFT*5.1+DOWN*2.9)
        a_lab=self.pill("AXIS",20).move_to(LEFT*2.0+DOWN*2.9)
        self.fixed(p_lab,a_lab)
        self.play(Create(ax),FadeIn(sketch),FadeIn(p_lab),FadeIn(a_lab),run_time=1.2)
        self.play(FadeIn(panel),run_time=1.0);self.wait(1.8)
        rows=panel[1][1]
        for i,label in enumerate(["Select closed region","Choose centerline","Choose 360° / Full","Choose Join / Cut"]):
            idx=[0,1,3,4][i]
            box=SurroundingRectangle(rows[idx],color=BLACK_LINE,buff=0.07,stroke_width=2.2)
            tag=self.text(label,20,BOLD).to_edge(DOWN,buff=0.30)
            self.fixed(box,tag)
            self.play(Create(box),FadeIn(tag),run_time=0.50);self.wait(1.10)
            self.play(FadeOut(box),FadeOut(tag),run_time=0.35)
        summary=self.text("The animation you just saw is what Inventor computes after these inputs are selected.",25,BOLD).to_edge(DOWN,buff=0.28)
        self.fit(summary,13.8,0.58);self.fixed(summary);self.play(FadeIn(summary),run_time=0.75);self.wait(3.0)
        self.clear_scene()

    def stepped_shaft_example(self):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=self.section_header(8,"STEPPED SHAFT: WATCH EVERY SHOULDER SWEEP INTO A DIAMETER CHANGE",
                              "This is the key professional case: one side profile can generate a complex lathe-like part with multiple diameters.")
        self.fixed(h);self.play(FadeIn(h),run_time=0.7)
        prof=[(0.68,-2.0),(0.68,-1.35),(1.12,-1.35),(1.12,-0.40),(0.86,-0.40),(0.86,0.45),(1.36,0.45),(1.36,1.20),(0.76,1.20),(0.76,2.0)]
        shift=LEFT*3.55
        sketch=closed_profile_polygon(prof,0.55).shift(shift)
        ax=axis_line(-2.3,2.3).shift(shift)
        labels=VGroup(
            self.text("radius 1",18).move_to(LEFT*1.25+UP*1.62),
            self.text("shoulder",18,BOLD).move_to(LEFT*1.05+UP*0.78),
            self.text("radius 2",18).move_to(LEFT*1.15+DOWN*0.15),
        );self.fixed(labels)
        insight=self.note("READ THE SKETCH",["Vertical segments set axial lengths.","Horizontal steps change radius.","After Revolve, each radius becomes a diameter."],width=5.6).move_to(RIGHT*3.75+DOWN*0.25)
        self.fixed(insight)
        self.play(Create(ax),FadeIn(sketch),FadeIn(labels),FadeIn(insight),run_time=1.1);self.wait(3.1)
        self.play(FadeOut(labels),FadeOut(insight),run_time=0.45)
        self.move_camera(
            phi=65*DEGREES,theta=-48*DEGREES,zoom=0.98,
            added_anims=[sketch.animate.shift(-shift),ax.animate.shift(-shift)],
            run_time=1.55,
        )
        shaft=self.sweep.animate_full_revolve(
            sketch,prof,duration=4.7,trace_count=9,keep_axis=ax,
            final_solid=self.sweep.final_solid(prof,opacity=0.55,caps=True,resolution=(36,24)),
        )
        note=self.note("WHAT THE SWEEP PROVES",["Each shoulder leaves a circular edge.","Each constant radius leaves a cylindrical band.","The 3D part is a direct record of the 2D profile."],width=6.1).to_corner(DR,buff=0.45)
        self.fixed(note);self.play(FadeIn(note),run_time=0.75);self.wait(3.5)
        self.clear_scene()

    def revolved_cut_example(self):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=self.section_header(9,"REVOLVED CUT: WATCH THE CUT PROFILE SWEEP THE MATERIAL AWAY",
                              "The subtractive profile uses the same rotation mechanism; only the operation changes from adding material to removing it.")
        self.fixed(h);self.play(FadeIn(h),run_time=0.7)
        plain=[(1.42,-1.70),(1.42,1.70)]
        grooved=[(1.42,-1.70),(1.42,-0.35),(1.08,-0.35),(1.08,0.35),(1.42,0.35),(1.42,1.70)]
        # Start with the plain shaft as the existing Inventor body.
        shaft_before=VGroup(revolution_surface(plain,TAU,0.43),revolution_cap(-1.70,1.42),revolution_cap(1.70,1.42))
        shaft_after=VGroup(revolution_surface(grooved,TAU,0.53),revolution_cap(-1.70,1.42),revolution_cap(1.70,1.42))
        # Exact rectangular cut region: inner/outer radii and two axial limits.
        rin,rout,y0,y1=1.08,1.42,-0.35,0.35
        cut_region=Polygon(
            np.array([GEOMETRY_SCALE*rin,GEOMETRY_SCALE*y0,0]),np.array([GEOMETRY_SCALE*rout,GEOMETRY_SCALE*y0,0]),np.array([GEOMETRY_SCALE*rout,GEOMETRY_SCALE*y1,0]),np.array([GEOMETRY_SCALE*rin,GEOMETRY_SCALE*y1,0]),
            stroke_color=BLACK_LINE,stroke_width=2.7,fill_color=GRAY_B,fill_opacity=0.40,
        )
        cut_outer=[(rout,y0),(rout,y1)]
        cut_inner=[(rin,y0),(rin,y1)]
        # First show front-view causality: existing body + 2D cut rectangle.
        body_icon=shaft_before.copy().scale(0.72).move_to(RIGHT*3.4+DOWN*0.25)
        cut2d=cut_region.copy().shift(LEFT*3.3)
        ax2d=axis_line(-1.8,1.8).shift(LEFT*3.3)
        labels=VGroup(self.pill("EXISTING BODY",19).move_to(RIGHT*3.4+DOWN*2.75),self.pill("CUT PROFILE",19).move_to(LEFT*3.3+DOWN*2.75))
        self.fixed(labels)
        self.play(FadeIn(body_icon),Create(ax2d),FadeIn(cut2d),FadeIn(labels),run_time=1.1);self.wait(2.7)
        self.play(FadeOut(body_icon),FadeOut(labels),run_time=0.45)
        # Center the exact cut profile while moving into 3D; bring in the existing shaft at the same center.
        self.move_camera(
            phi=65*DEGREES,theta=-48*DEGREES,zoom=0.99,
            added_anims=[cut2d.animate.shift(RIGHT*3.3),ax2d.animate.shift(RIGHT*3.3)],
            run_time=1.5,
        )
        self.play(FadeIn(shaft_before),run_time=0.8)
        self.bring_to_front(cut2d)
        result=self.sweep.animate_cut_revolve(cut2d,cut_outer,cut_inner,shaft_before,shaft_after,duration=3.6)
        operation=self.note("BOOLEAN MEANING",["Join: swept volume becomes material.","Cut: swept volume is subtracted from the existing body."],width=5.8).to_corner(DR,buff=0.45)
        self.fixed(operation);self.play(FadeIn(operation),run_time=0.75);self.wait(3.4)
        self.clear_scene()

    def no_calculus_check(self):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=self.section_header(10,"A SIMPLE GEOMETRY CHECK — WITHOUT INTEGRAL CALCULUS",
                              "Use familiar formulas only as a model check. The Revolve concept itself is geometric and visual.")
        self.fixed(h);self.play(FadeIn(h),run_time=0.7)
        circle=Circle(radius=1.42,color=BLACK_LINE,stroke_width=2.5,fill_color=LIGHT_GRAY,fill_opacity=0.50).move_to(LEFT*4.25+DOWN*0.20)
        rad=Line(circle.get_center(),circle.get_right(),color=BLACK_LINE,stroke_width=2.3)
        rlab=MathTex("r",color=BLACK_TEXT,font_size=36).next_to(rad,UP,buff=0.05)
        title=self.text("CIRCULAR BASE AREA",24,BOLD).next_to(circle,UP,buff=0.35)
        area=MathTex(r"A=\pi r^2",color=BLACK_TEXT,font_size=48).next_to(circle,DOWN,buff=0.32)
        self.fixed(circle,rad,rlab,title,area)
        self.play(FadeIn(circle),Create(rad),FadeIn(rlab),FadeIn(title),run_time=1.0);self.play(Write(area),run_time=0.9);self.wait(2.4)
        bridge=VGroup(self.pill("same base",20),self.pill("length L",20),self.pill("cylinder volume",20)).arrange(DOWN,buff=0.22).move_to(ORIGIN+DOWN*0.20)
        self.fixed(bridge);self.play(LaggedStart(*[FadeIn(x) for x in bridge],lag_ratio=0.15),run_time=1.2);self.wait(1.8)
        formula=MathTex(r"V=A\,L=\pi r^2L",color=BLACK_TEXT,font_size=52).move_to(RIGHT*4.25+DOWN*0.25)
        ftitle=self.text("CYLINDER CHECK",24,BOLD).next_to(formula,UP,buff=0.35)
        self.fixed(formula,ftitle);self.play(FadeIn(ftitle),Write(formula),run_time=1.2);self.wait(2.8)
        footer=self.text("For tomorrow's class: understand profile + axis + operation first; calculus can be added later.",25,BOLD).to_edge(DOWN,buff=0.30)
        self.fit(footer,14.0,0.60)
        self.fixed(footer);self.play(FadeIn(footer),run_time=0.8);self.wait(3.3)
        self.clear_scene()

    def final_design_challenge(self):
        self.set_camera_orientation(phi=64*DEGREES,theta=-48*DEGREES,zoom=0.99)
        h=self.section_header(11,"FINAL DESIGN CHALLENGE: REVERSE THE MOTION IN YOUR HEAD",
                              "A professional CAD habit is to look at the 3D part and recover the 2D generator that must have swept around its axis.")
        self.fixed(h);self.play(FadeIn(h),run_time=0.7)
        prof=[(0.64,-2.0),(0.64,-1.35),(1.12,-1.35),(1.12,-0.40),(0.86,-0.40),(0.86,0.45),(1.35,0.45),(1.35,1.20),(0.78,1.20),(0.78,2.0)]
        solid=self.sweep.final_solid(prof,opacity=0.54,caps=True,resolution=(34,22)).shift(RIGHT*2.8)
        self.play(FadeIn(solid),run_time=1.1)
        q=self.note("ASK IN THIS ORDER",["1. Where is the symmetry axis?","2. Where do diameters change?","3. Which radii create those bands?","4. Which closed profile would sweep them?"],width=5.9).to_corner(DL,buff=0.50).shift(UP*0.65)
        self.fixed(q);self.play(FadeIn(q),run_time=0.75);self.wait(4.0)
        self.play(FadeOut(q),run_time=0.4)
        # Rather than merely fading in the answer, visually collapse the 3D logic back to its generator.
        self.move_camera(phi=0,theta=-90*DEGREES,zoom=1.0,run_time=1.4)
        sketch=closed_profile_polygon(prof,0.54).shift(LEFT*3.5)
        ax=axis_line(-2.3,2.3).shift(LEFT*3.5)
        reveal=self.text("REVERSE ENGINEERING: the shaft can be encoded by this one side profile.",25,BOLD).to_edge(DOWN,buff=0.30)
        self.fit(reveal,13.7,0.58);self.fixed(reveal)
        self.play(solid.animate.set_opacity(0.16),Create(ax),FadeIn(sketch),FadeIn(reveal),run_time=1.3)
        self.wait(3.2)
        # Finish by replaying a short sweep so the answer is verified, not merely asserted.
        self.play(FadeOut(solid),FadeOut(reveal),run_time=0.45)
        self.move_camera(
            phi=62*DEGREES,theta=-48*DEGREES,zoom=1.00,
            added_anims=[sketch.animate.shift(RIGHT*3.5),ax.animate.shift(RIGHT*3.5)],
            run_time=1.35,
        )
        verified=self.sweep.animate_full_revolve(sketch,prof,duration=3.2,trace_count=8,keep_axis=ax,final_solid=self.sweep.final_solid(prof,opacity=0.54,caps=True,resolution=(34,22)))
        verify_lab=self.text("Verified: the recovered 2D profile regenerates the same 3D shaft.",26,BOLD).to_edge(DOWN,buff=0.30)
        self.fit(verify_lab,13.6,0.58);self.fixed(verify_lab);self.play(FadeIn(verify_lab),run_time=0.7);self.wait(3.1)
        self.clear_scene()

    def closing(self):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        title=self.text("PROFILE  →  SWEEP  →  SURFACE  →  SOLID",40,BOLD); self.fit(title, 14.20, 0.82)
        sub=self.text("In Inventor, Revolve is not a magic 3D command: it is the recorded motion of a 2D generator around an axis.",26); self.fit(sub, 13.65, 0.64)
        checklist=VGroup(
            self.pill("closed area",19),self.pill("axis",19),self.pill("angle",19),self.pill("join / cut",19),
        ).arrange(RIGHT,buff=0.20)
        group=VGroup(title,sub,checklist).arrange(DOWN,buff=0.34)
        self.fixed(group)
        self.play(FadeIn(title),run_time=0.9);self.wait(1.3)
        self.play(FadeIn(sub),run_time=0.8);self.wait(1.7)
        self.play(LaggedStart(*[FadeIn(x) for x in checklist],lag_ratio=0.13),run_time=1.2);self.wait(4.0)
        self.play(FadeOut(group),run_time=0.8)

# Preview:
# manim -pql SolidsOfRevolution_InventorProfessional_TRANSFORM_V3.py SolidsOfRevolutionInventorSeniorV3 --format=mp4 --disable_caching
# Final:
# manim -pqh SolidsOfRevolution_InventorProfessional_TRANSFORM_V3.py SolidsOfRevolutionInventorSeniorV3 --format=mp4 --disable_caching
