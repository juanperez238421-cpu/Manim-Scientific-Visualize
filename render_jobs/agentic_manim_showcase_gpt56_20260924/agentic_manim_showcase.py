#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agentic Manim Showcase — long-horizon animation benchmark.

A self-contained ManimCE 0.20.x scene designed to stress the same capabilities
that matter in modern agentic visual coding: decomposition, reusable visual
primitives, live state, synchronized motion, 3D, visual feedback, and
QA-friendly deterministic rendering.

No external assets are required.
"""

from __future__ import annotations

import math
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#070A12"

BG = "#070A12"
PANEL = "#111827"
PANEL_2 = "#0E1628"
INK = "#F8FAFC"
MUTED = "#94A3B8"
CYAN = "#38BDF8"
BLUE = "#60A5FA"
VIOLET = "#A78BFA"
MAGENTA = "#F472B6"
GREEN = "#34D399"
AMBER = "#FBBF24"
RED = "#FB7185"
GRID = "#22304A"


def clamp_text(mob: Mobject, max_w: float, max_h: float) -> Mobject:
    """Scale down only, preserving hierarchy."""
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    if mob.height > max_h:
        mob.scale_to_fit_height(max_h)
    return mob


def glow_dot(point=ORIGIN, color=CYAN, radius=0.085, layers=5) -> VGroup:
    """Cheap deterministic pseudo-glow that works with Cairo."""
    rings = VGroup()
    for i in range(layers, 0, -1):
        r = radius * (1.0 + i * 0.72)
        c = Circle(
            radius=r,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.045 + 0.012 * i,
        ).move_to(point)
        rings.add(c)
    core = Dot(point, radius=radius, color=color)
    return VGroup(rings, core)


def glass_card(width: float, height: float, title: str, subtitle: str, accent=CYAN) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=accent,
        stroke_width=1.7,
        fill_color=PANEL,
        fill_opacity=0.96,
    )
    accent_bar = RoundedRectangle(
        width=0.085,
        height=height - 0.32,
        corner_radius=0.04,
        stroke_width=0,
        fill_color=accent,
        fill_opacity=1,
    ).align_to(box, LEFT).shift(RIGHT * 0.18)
    title_mob = Text(title, font_size=25, weight=BOLD, color=INK)
    subtitle_mob = Text(subtitle, font_size=16, color=MUTED, line_spacing=0.9)
    clamp_text(title_mob, width - 0.75, 0.42)
    clamp_text(subtitle_mob, width - 0.75, height - 0.88)
    text_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
    text_group.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.45)
    return VGroup(box, accent_bar, text_group)


def section_tag(index: str, title: str, accent=CYAN) -> VGroup:
    badge = RoundedRectangle(
        width=0.62,
        height=0.42,
        corner_radius=0.09,
        stroke_color=accent,
        stroke_width=1.5,
        fill_color=PANEL_2,
        fill_opacity=1,
    )
    number = Text(index, font_size=18, weight=BOLD, color=accent).move_to(badge)
    label = Text(title, font_size=27, weight=BOLD, color=INK)
    return VGroup(VGroup(badge, number), label).arrange(RIGHT, buff=0.18)


def make_grid(width=15.2, height=8.0, dx=0.5, dy=0.5) -> VGroup:
    lines = VGroup()
    for x in np.arange(-width / 2, width / 2 + 1e-6, dx):
        opacity = 0.16 if abs(x) < 1e-6 else 0.055
        lines.add(Line(
            [x, -height / 2, 0], [x, height / 2, 0],
            color=GRID, stroke_width=1, stroke_opacity=opacity,
        ))
    for y in np.arange(-height / 2, height / 2 + 1e-6, dy):
        opacity = 0.16 if abs(y) < 1e-6 else 0.055
        lines.add(Line(
            [-width / 2, y, 0], [width / 2, y, 0],
            color=GRID, stroke_width=1, stroke_opacity=opacity,
        ))
    return lines


class AgenticManimShowcase(ThreeDScene):
    """Single-scene visual benchmark: orchestration -> live motion -> 3D -> QA."""

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.agent_orchestration()
        self.live_state_motion()
        self.three_d_projection()
        self.visual_qa_loop()
        self.final_synthesis()

    def opening(self):
        grid = make_grid()
        self.add(grid)

        kicker = Text("AGENTIC MANIM BENCHMARK", font_size=20, weight=BOLD, color=CYAN)
        title = Text("ONE PROMPT → A LIVING SYSTEM", font_size=54, weight=BOLD, color=INK)
        sub = Text(
            "Planning, code, motion, 3D, verification — all synchronized in one deterministic render.",
            font_size=22,
            color=MUTED,
        )
        clamp_text(sub, 12.8, 0.65)
        stack = VGroup(kicker, title, sub).arrange(DOWN, buff=0.18).move_to(UP * 0.55)

        scan = Line(LEFT * 6.4, RIGHT * 6.4, color=CYAN, stroke_width=2.0, stroke_opacity=0.55)
        scan.move_to(DOWN * 1.10)

        pts = []
        for i in range(22):
            x = -6.8 + i * 0.64
            y = -2.2 + 0.22 * math.sin(i * 0.9)
            pts.append(glow_dot(
                [x, y, 0],
                color=[CYAN, VIOLET, MAGENTA][i % 3],
                radius=0.035,
                layers=3,
            ))
        stars = VGroup(*pts)

        self.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in stack], lag_ratio=0.12),
            run_time=1.5,
        )
        self.play(
            Create(scan),
            LaggedStart(*[FadeIn(p, scale=0.3) for p in stars], lag_ratio=0.035),
            run_time=1.3,
        )
        self.play(
            ShowPassingFlash(scan.copy().set_stroke(width=7, opacity=0.75), time_width=0.35),
            run_time=1.2,
        )
        self.wait(0.8)
        self.play(FadeOut(stack), FadeOut(scan), FadeOut(stars), run_time=0.85)

    def agent_orchestration(self):
        tag = section_tag("01", "ORCHESTRATE THE WORK", CYAN).to_corner(UL, buff=0.48)
        subtitle = Text(
            "Complex output becomes tractable when the job is decomposed into verifiable stages.",
            font_size=18,
            color=MUTED,
        ).next_to(tag, DOWN, aligned_edge=LEFT, buff=0.09)
        clamp_text(subtitle, 13.8, 0.42)
        self.play(FadeIn(tag), FadeIn(subtitle), run_time=0.6)

        labels = [
            ("PLAN", "scene graph\n+ timing", CYAN),
            ("BUILD", "Manim objects\n+ state", BLUE),
            ("RENDER", "Cairo / ffmpeg\nexecution", VIOLET),
            ("SEE", "frame audit\n+ visual QA", MAGENTA),
            ("FIX", "iterate from\nmeasured errors", GREEN),
        ]
        xs = [-5.8, -2.9, 0.0, 2.9, 5.8]
        cards = VGroup(*[
            glass_card(2.35, 1.65, a, b, c).move_to([x, -0.10, 0])
            for x, (a, b, c) in zip(xs, labels)
        ])
        edges = VGroup(*[
            Arrow(
                cards[i].get_right() + RIGHT * 0.08,
                cards[i + 1].get_left() + LEFT * 0.08,
                buff=0.10,
                stroke_width=2.0,
                max_tip_length_to_length_ratio=0.13,
                color=GRID,
            )
            for i in range(4)
        ])
        return_edge = CurvedArrow(
            cards[-1].get_bottom() + DOWN * 0.10,
            cards[0].get_bottom() + DOWN * 0.10,
            angle=-TAU / 7,
            color=GRID,
            stroke_width=2,
        )
        return_label = Text("feedback loop", font_size=15, color=MUTED).next_to(return_edge, DOWN, buff=0.06)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.18) for c in cards], lag_ratio=0.11), run_time=1.35)
        self.play(Create(edges), Create(return_edge), FadeIn(return_label), run_time=1.0)

        colors = [CYAN, BLUE, VIOLET, MAGENTA, GREEN]
        for i in range(4):
            self.play(
                ShowPassingFlash(edges[i].copy().set_color(colors[i]).set_stroke(width=6), time_width=0.28),
                run_time=0.42,
            )
        self.play(
            ShowPassingFlash(return_edge.copy().set_color(GREEN).set_stroke(width=6), time_width=0.35),
            run_time=0.8,
        )

        metric = glass_card(
            5.4, 1.15,
            "KEY IDEA",
            "The model is only one layer; the loop makes the animation reliable.",
            AMBER,
        ).move_to([0, -2.65, 0])
        self.play(FadeIn(metric, shift=UP * 0.15), run_time=0.65)
        self.wait(1.1)
        self.play(
            FadeOut(VGroup(tag, subtitle, cards, edges, return_edge, return_label, metric)),
            run_time=0.85,
        )

    def live_state_motion(self):
        tag = section_tag("02", "ONE STATE, MANY SYNCHRONIZED VIEWS", BLUE).to_corner(UL, buff=0.48)
        subtitle = Text(
            "A single ValueTracker can coordinate geometry, trails, vectors, labels and graphs frame by frame.",
            font_size=18,
            color=MUTED,
        ).next_to(tag, DOWN, aligned_edge=LEFT, buff=0.09)
        clamp_text(subtitle, 13.8, 0.42)
        self.play(FadeIn(tag), FadeIn(subtitle), run_time=0.55)

        left_box = RoundedRectangle(
            width=8.8, height=5.6, corner_radius=0.18,
            stroke_color=BLUE, stroke_width=1.5,
            fill_color=PANEL_2, fill_opacity=0.82,
        ).move_to(LEFT * 3.15 + DOWN * 0.45)
        right_box = RoundedRectangle(
            width=5.6, height=5.6, corner_radius=0.18,
            stroke_color=VIOLET, stroke_width=1.5,
            fill_color=PANEL_2, fill_opacity=0.82,
        ).move_to(RIGHT * 4.25 + DOWN * 0.45)
        self.play(FadeIn(left_box), FadeIn(right_box), run_time=0.55)

        path = ParametricFunction(
            lambda u: np.array([
                -6.3 + 6.25 * u,
                -0.85 + 1.05 * math.sin(TAU * u) + 0.38 * math.sin(3 * TAU * u),
                0,
            ]),
            t_range=[0, 1],
            color=GRID,
            stroke_width=2.2,
        )
        self.play(Create(path), run_time=0.75)

        progress = ValueTracker(0.0)
        mover = always_redraw(lambda: glow_dot(path.point_from_proportion(progress.get_value()), CYAN, 0.06, 4))
        trail = TracedPath(lambda: mover[-1].get_center(), stroke_color=CYAN, stroke_width=4.0, dissipating_time=1.5)
        tangent = always_redraw(lambda: self._tangent_arrow(path, progress.get_value()))
        live_label = always_redraw(
            lambda: self._motion_label(progress.get_value()).move_to([-2.65, -2.45, 0])
        )

        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-1.4, 1.4, 0.5],
            x_length=4.6,
            y_length=3.5,
            axis_config={"color": GRID, "stroke_width": 1.4, "include_ticks": True},
            tips=False,
        ).move_to([4.35, -0.20, 0])
        xlab = Text("state", font_size=15, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.12)
        ylab = Text("response", font_size=15, color=MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.12)
        graph = always_redraw(lambda: axes.plot(
            lambda x: math.sin(TAU * x) + 0.35 * math.sin(3 * TAU * x),
            x_range=[0, max(0.001, progress.get_value())],
            color=VIOLET,
            stroke_width=3.3,
        ))
        graph_dot = always_redraw(lambda: glow_dot(
            axes.c2p(
                progress.get_value(),
                math.sin(TAU * progress.get_value()) + 0.35 * math.sin(3 * TAU * progress.get_value()),
            ),
            MAGENTA, 0.05, 3,
        ))

        self.add(trail, mover, tangent, graph, graph_dot)
        self.play(FadeIn(VGroup(axes, xlab, ylab)), FadeIn(live_label), run_time=0.65)
        self.play(progress.animate.set_value(1.0), run_time=5.4, rate_func=linear)
        self.wait(0.75)

        sync_card = glass_card(
            5.0, 1.08,
            "SYNCHRONIZED",
            "path + vector + trail + graph + label",
            GREEN,
        ).move_to([4.3, -2.65, 0])
        self.play(FadeIn(sync_card, shift=UP * 0.10), run_time=0.55)
        self.wait(0.8)

        all_live = VGroup(tag, subtitle, left_box, right_box, path, axes, xlab, ylab, sync_card)
        self.play(
            FadeOut(all_live),
            FadeOut(mover),
            FadeOut(tangent),
            FadeOut(graph),
            FadeOut(graph_dot),
            FadeOut(live_label),
            run_time=0.85,
        )
        self.remove(trail)

    def _tangent_arrow(self, path: VMobject, alpha: float) -> Arrow:
        a = min(max(alpha, 0.001), 0.999)
        p = path.point_from_proportion(a)
        p0 = path.point_from_proportion(max(0.0, a - 0.012))
        p1 = path.point_from_proportion(min(1.0, a + 0.012))
        direction = p1 - p0
        norm = np.linalg.norm(direction)
        direction = RIGHT if norm < 1e-9 else direction / norm
        return Arrow(
            p, p + 0.9 * direction,
            buff=0,
            color=AMBER,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )

    def _motion_label(self, alpha: float) -> VGroup:
        pct = int(round(alpha * 100))
        title = Text("LIVE STATE", font_size=17, weight=BOLD, color=CYAN)
        value = Text(f"{pct:03d}%", font_size=34, weight=BOLD, color=INK)
        return VGroup(title, value).arrange(DOWN, buff=0.06)

    def three_d_projection(self):
        tag = section_tag("03", "3D GEOMETRY CAN BECOME A CAMERA CHOREOGRAPHY", VIOLET).to_corner(UL, buff=0.48)
        subtitle = Text(
            "The scene does not need to be a slideshow: the camera itself can carry the explanation.",
            font_size=18,
            color=MUTED,
        ).next_to(tag, DOWN, aligned_edge=LEFT, buff=0.09)
        clamp_text(subtitle, 13.8, 0.42)
        self.add_fixed_in_frame_mobjects(tag, subtitle)
        self.play(FadeIn(tag), FadeIn(subtitle), run_time=0.55)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.95)
        axes3d = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6.0,
            y_length=6.0,
            z_length=4.5,
            axis_config={"color": GRID, "stroke_width": 1.3},
        )
        cube = Cube(
            side_length=2.4,
            fill_color=VIOLET,
            fill_opacity=0.24,
            stroke_color=VIOLET,
            stroke_width=2.0,
        )
        cube.rotate(18 * DEGREES, axis=UP).rotate(12 * DEGREES, axis=RIGHT)
        inner = Cube(
            side_length=1.25,
            fill_color=CYAN,
            fill_opacity=0.18,
            stroke_color=CYAN,
            stroke_width=1.6,
        )
        diagonal = Line3D(
            start=[-1.2, -1.2, -1.2],
            end=[1.2, 1.2, 1.2],
            color=AMBER,
            thickness=0.018,
        )
        model = VGroup(axes3d, cube, inner, diagonal)

        self.play(Create(axes3d), FadeIn(cube), FadeIn(inner), Create(diagonal), run_time=1.4)
        self.begin_ambient_camera_rotation(rate=0.20)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=72 * DEGREES, theta=35 * DEGREES, zoom=1.08, run_time=2.0)
        self.wait(0.6)
        self.play(FadeOut(model), run_time=0.65)

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=1.35)

        cards = VGroup()
        view_data = [
            ("FRONT", VIOLET, [Square(1.45, color=VIOLET), Line(LEFT * 0.72, RIGHT * 0.72, color=CYAN)]),
            ("TOP", CYAN, [Square(1.45, color=CYAN), Line(DOWN * 0.72, UP * 0.72, color=VIOLET)]),
            ("SIDE", MAGENTA, [Square(1.45, color=MAGENTA), Line(DL * 0.52, UR * 0.52, color=AMBER)]),
        ]
        for i, (name, accent, pieces) in enumerate(view_data):
            box = RoundedRectangle(
                width=3.5, height=3.35, corner_radius=0.18,
                stroke_color=accent, stroke_width=1.6,
                fill_color=PANEL, fill_opacity=0.96,
            )
            figure = VGroup(*pieces).move_to(box).shift(UP * 0.18)
            label = Text(name, font_size=21, weight=BOLD, color=accent).next_to(figure, DOWN, buff=0.28)
            cards.add(VGroup(box, figure, label).move_to([-4.15 + i * 4.15, -0.45, 0]))

        self.add_fixed_in_frame_mobjects(cards)
        for card in cards:
            self.play(
                FadeIn(card[0]),
                Create(card[1][0]),
                Create(card[1][1]),
                FadeIn(card[2]),
                run_time=0.65,
            )
        method = Text(
            "camera motion → spatial understanding → clean 2D views",
            font_size=22,
            color=INK,
        ).to_edge(DOWN, buff=0.50)
        self.add_fixed_in_frame_mobjects(method)
        self.play(FadeIn(method, shift=UP * 0.10), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(cards), FadeOut(method), FadeOut(tag), FadeOut(subtitle), run_time=0.8)
        self.remove_fixed_in_frame_mobjects(cards, method, tag, subtitle)

    def visual_qa_loop(self):
        tag = section_tag("04", "RENDER → SEE → MEASURE → REPAIR", MAGENTA).to_corner(UL, buff=0.48)
        subtitle = Text(
            "A strong coding model improves when the environment returns objective visual evidence, not just compiler success.",
            font_size=18,
            color=MUTED,
        ).next_to(tag, DOWN, aligned_edge=LEFT, buff=0.09)
        clamp_text(subtitle, 13.8, 0.42)
        self.play(FadeIn(tag), FadeIn(subtitle), run_time=0.55)

        frame = RoundedRectangle(
            width=10.2, height=5.55, corner_radius=0.18,
            stroke_color=INK, stroke_width=1.8,
            fill_color=PANEL_2, fill_opacity=0.9,
        ).move_to(LEFT * 1.75 + DOWN * 0.45)
        target = RoundedRectangle(
            width=3.6, height=1.35, corner_radius=0.15,
            stroke_color=CYAN, stroke_width=2.0,
            fill_color=PANEL, fill_opacity=1,
        ).move_to(frame).shift(UP * 0.25)
        txt = Text("important content", font_size=24, weight=BOLD, color=INK).move_to(target)
        defect = Text("overlap", font_size=20, weight=BOLD, color=RED).move_to(target).shift(UP * 0.50 + RIGHT * 1.20)
        bad_box = SurroundingRectangle(defect, color=RED, buff=0.10, stroke_width=2.0)

        panel = glass_card(
            4.35, 3.7,
            "VISUAL EVALUATOR",
            "1. detect overlap\n2. measure bounds\n3. propose correction\n4. rerender\n5. verify again",
            MAGENTA,
        ).move_to([5.25, -0.45, 0])

        self.play(
            FadeIn(frame), FadeIn(target), FadeIn(txt), FadeIn(defect),
            Create(bad_box), FadeIn(panel), run_time=0.85,
        )
        self.play(
            ShowPassingFlash(bad_box.copy().set_stroke(width=7, color=RED), time_width=0.35),
            run_time=0.8,
        )

        dx_arrow = Arrow(
            defect.get_center(),
            defect.get_center() + DOWN * 1.1 + LEFT * 0.55,
            buff=0.12,
            color=AMBER,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.16,
        )
        measure = Text("measured repair", font_size=16, color=AMBER).next_to(dx_arrow, RIGHT, buff=0.08)
        self.play(Create(dx_arrow), FadeIn(measure), run_time=0.6)
        self.play(
            defect.animate.shift(DOWN * 1.1 + LEFT * 0.55).set_color(GREEN),
            bad_box.animate.shift(DOWN * 1.1 + LEFT * 0.55).set_color(GREEN),
            run_time=0.75,
        )
        ok = Text("PASS", font_size=28, weight=BOLD, color=GREEN).move_to(frame).shift(DOWN * 1.85 + RIGHT * 3.65)
        self.play(FadeIn(ok, scale=0.8), FadeOut(dx_arrow), FadeOut(measure), run_time=0.5)
        self.wait(1.0)
        self.play(
            FadeOut(VGroup(tag, subtitle, frame, target, txt, defect, bad_box, panel, ok)),
            run_time=0.8,
        )

    def final_synthesis(self):
        headline = Text("COMPLEX ANIMATION IS A SYSTEMS PROBLEM", font_size=44, weight=BOLD, color=INK)
        sub = Text(
            "model intelligence × context × tools × execution × visual verification",
            font_size=24,
            color=MUTED,
        )
        clamp_text(sub, 13.5, 0.62)
        stack = VGroup(headline, sub).arrange(DOWN, buff=0.18).move_to(UP * 1.55)

        formula = MathTex(
            r"\text{quality}\;\propto\;\text{reasoning}\times\text{feedback loops}",
            font_size=46,
            color=INK,
        ).move_to(UP * 0.15)
        formula.set_color_by_tex("reasoning", CYAN)
        formula.set_color_by_tex("feedback", MAGENTA)

        chips = VGroup(
            self._chip("PLAN", CYAN),
            self._chip("CODE", BLUE),
            self._chip("RENDER", VIOLET),
            self._chip("SEE", MAGENTA),
            self._chip("VERIFY", GREEN),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.45)

        self.play(FadeIn(stack, shift=UP * 0.12), Write(formula), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.08),
            run_time=0.9,
        )
        for c in chips:
            self.play(
                ShowPassingFlash(c[0].copy().set_stroke(width=6), time_width=0.35),
                run_time=0.24,
            )

        line = Line(LEFT * 6.4, RIGHT * 6.4, color=GRID, stroke_width=1.5).move_to(DOWN * 2.45)
        closing = Text(
            "The target is not prettier code. The target is a verified visual experience.",
            font_size=20,
            color=INK,
        ).next_to(line, DOWN, buff=0.28)
        self.play(Create(line), FadeIn(closing), run_time=0.65)
        self.wait(2.2)

    def _chip(self, label: str, color) -> VGroup:
        box = RoundedRectangle(
            width=2.15, height=0.72, corner_radius=0.22,
            stroke_color=color, stroke_width=1.6,
            fill_color=PANEL, fill_opacity=1,
        )
        txt = Text(label, font_size=19, weight=BOLD, color=color).move_to(box)
        return VGroup(box, txt)
