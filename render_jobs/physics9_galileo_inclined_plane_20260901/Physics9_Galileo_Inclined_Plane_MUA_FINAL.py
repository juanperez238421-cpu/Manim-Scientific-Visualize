#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Galileo's Inclined Plane · Constant Acceleration Equations.

Full classroom presentation designed for Manim Community Edition 0.20.1.
The scene follows the JP classroom visual system: 16:9 Full HD, white
background, black/gray visual hierarchy, large readable typography,
stepwise derivations, animated physical model, synchronized graphs,
and a final student challenge.

Pedagogical sequence
--------------------
1. Bridge from position-time slope to velocity.
2. Reconstruct Galileo's inclined-plane experiment.
3. Observe equal-time positions and the 1:3:5:7 distance pattern.
4. Infer x ∝ t² for motion from rest under constant acceleration.
5. Introduce constant acceleration on a velocity-time graph.
6. Derive v = v0 + at from slope.
7. Derive Δx = v0 t + 1/2 a t² from area under v-t.
8. Derive v² = v0² + 2aΔx by eliminating time.
9. Verify all three equations on a laboratory-style example.
10. Connect x-t, v-t and a-t graphs.
11. Finish with a reproducible method map and student challenge.

Historical note
---------------
The animation represents the standard classroom reconstruction of Galileo's
inclined-plane investigations: a shallow ramp slows the motion enough to make
regular measurements practical. The kinematic conclusion used here is the
constant-acceleration pattern, not a claim that a rolling sphere has a = g sinθ.
"""

from __future__ import annotations

import os
import math
import numpy as np
from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE


# =============================================================================
# VISUAL SYSTEM
# =============================================================================
BLACK_TEXT = BLACK
DARK_GRAY = "#333333"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D8D8D8"
PAPER_GRAY = "#F4F4F4"
VERY_LIGHT_GRAY = "#FAFAFA"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_FAST = 0.65
RUN = 1.0
RUN_SLOW = 1.35
PAUSE_SHORT = 0.8
PAUSE_READ = 1.7
PAUSE_EXPLAIN = 2.5
PAUSE_WORK = 3.2
PAUSE_FINAL = 4.2

SAFE_W = 14.6
SAFE_H = 7.55


# =============================================================================
# REUSABLE CLASSROOM BASE
# =============================================================================
class Physics9GalileoInclinedPlaneFinal(MovingCameraScene):
    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header_group = None
        self.validate_lesson_data()

    def validate_lesson_data(self):
        # Equal-time Galileo pattern: cumulative distances proportional to t².
        times = np.array([0, 1, 2, 3, 4], dtype=float)
        positions = times**2
        increments = np.diff(positions)
        assert np.allclose(increments, [1, 3, 5, 7])

        # Worked example.
        a = 0.80
        t = 3.0
        v0 = 0.0
        dx = v0 * t + 0.5 * a * t**2
        v = v0 + a * t
        assert abs(dx - 3.6) < 1e-12
        assert abs(v - 2.4) < 1e-12
        assert abs(v**2 - (v0**2 + 2 * a * dx)) < 1e-12

    # Timing wrappers ---------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # Typography -------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=BLACK_TEXT, **kwargs):
        return Text(
            content,
            font_size=size,
            weight=weight,
            color=color,
            line_spacing=0.92,
            **kwargs,
        )

    def math(self, expr, size=40, color=BLACK_TEXT, **kwargs):
        return MathTex(expr, font_size=size, color=color, **kwargs)

    def fit(self, mob, max_w=SAFE_W, max_h=SAFE_H):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    # Layout -----------------------------------------------------------------
    def set_header(self, number, title, subtitle):
        if self.header_group is not None:
            self.remove(self.header_group)

        num_box = RoundedRectangle(
            width=0.74,
            height=0.53,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 22, BOLD).move_to(num_box)
        title_m = self.txt(title, 29, BOLD)
        top = VGroup(VGroup(num_box, num), title_m).arrange(RIGHT, buff=0.22)
        top.to_edge(UP, buff=0.18).align_to(LEFT * 7.3, LEFT)

        subtitle_m = self.txt(subtitle, 19, NORMAL, color=DARK_GRAY)
        self.fit(subtitle_m, 13.9, 0.55)
        subtitle_m.next_to(top, DOWN, buff=0.10).align_to(top, LEFT)

        rule = Line(LEFT * 7.3, RIGHT * 7.3, color=LIGHT_GRAY, stroke_width=1.6)
        rule.next_to(subtitle_m, DOWN, buff=0.10)

        self.header_group = VGroup(top, subtitle_m, rule)
        self.add(self.header_group)

    def panel(self, width, height, fill=PAPER_GRAY, stroke=BLACK, radius=0.12):
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=radius,
            stroke_color=stroke,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1,
        )

    def formula_panel(self, expr, width=6.6, height=1.15, size=42):
        box = self.panel(width, height)
        eq = self.math(expr, size)
        self.fit(eq, width - 0.45, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(self, title, lines, width=5.8, title_size=24, body_size=21):
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.55, 3.9)
        box = self.panel(width, max(1.2, content.height + 0.55), fill=WHITE)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def clear_stage(self):
        keep = set(self.header_group.submobjects if self.header_group is not None else [])
        if self.header_group is not None:
            keep.add(self.header_group)
        targets = [m for m in self.mobjects if m not in keep and m is not self.header_group]
        if targets:
            self.play(*[FadeOut(m) for m in targets], run_time=RUN_FAST)

    # Small helpers ----------------------------------------------------------
    def make_person(self, scale=1.0):
        head = Circle(radius=0.14, stroke_color=BLACK, stroke_width=2)
        body = Line(ORIGIN, DOWN * 0.48, color=BLACK, stroke_width=2)
        arms = VGroup(
            Line(ORIGIN + DOWN * 0.16, LEFT * 0.22 + DOWN * 0.32, color=BLACK, stroke_width=2),
            Line(ORIGIN + DOWN * 0.16, RIGHT * 0.22 + DOWN * 0.32, color=BLACK, stroke_width=2),
        )
        legs = VGroup(
            Line(DOWN * 0.48, LEFT * 0.18 + DOWN * 0.78, color=BLACK, stroke_width=2),
            Line(DOWN * 0.48, RIGHT * 0.18 + DOWN * 0.78, color=BLACK, stroke_width=2),
        )
        body_group = VGroup(head, body, arms, legs)
        body_group.scale(scale)
        return body_group

    def make_ramp(self, start=np.array([-5.7, -2.4, 0]), end=np.array([3.9, 1.7, 0])):
        ramp = Line(start, end, color=BLACK, stroke_width=5)
        floor = Line(np.array([-6.4, -2.4, 0]), np.array([5.4, -2.4, 0]), color=BLACK, stroke_width=2)
        support = Line(end, np.array([3.9, -2.4, 0]), color=MID_GRAY, stroke_width=2)
        return VGroup(ramp, floor, support), ramp

    def ramp_point(self, start, end, u):
        return start + u * (end - start)

    # Main orchestration -----------------------------------------------------
    def construct(self):
        self.opening()
        self.bridge_from_previous_class()
        self.galileo_question()
        self.galileo_apparatus()
        self.equal_time_pattern()
        self.square_time_law()
        self.velocity_time_meaning()
        self.derive_first_equation()
        self.derive_second_equation()
        self.derive_third_equation()
        self.worked_lab_example()
        self.three_graphs_one_motion()
        self.student_challenge()
        self.summary()

    # ------------------------------------------------------------------
    # 00 Opening
    # ------------------------------------------------------------------
    def opening(self):
        title = self.txt("PHYSICS 9 | KINEMATICS", 28, BOLD)
        main = self.txt("GALILEO'S INCLINED PLANE", 50, BOLD)
        sub = self.txt("From experiment to the equations of constant acceleration", 28)
        eq = self.formula_panel(
            r"v=v_0+at\qquad \Delta x=v_0t+\frac12at^2\qquad v^2=v_0^2+2a\Delta x",
            width=12.3,
            height=1.25,
            size=39,
        )
        promise = self.txt(
            "Observe the motion. Find the pattern. Build the equations.",
            24,
            weight=BOLD,
            color=DARK_GRAY,
        )
        group = VGroup(title, main, sub, eq, promise).arrange(DOWN, buff=0.34)
        group.move_to(ORIGIN)
        self.fit(group, 14.2, 7.2)

        self.play(FadeIn(title, shift=UP * 0.12), run_time=RUN)
        self.play(Write(main), run_time=RUN_SLOW)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(eq), run_time=RUN)
        self.play(FadeIn(promise), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    # ------------------------------------------------------------------
    # 01 Bridge
    # ------------------------------------------------------------------
    def bridge_from_previous_class(self):
        self.set_header(
            1,
            "BRIDGE: THE SLOPE OF POSITION-TIME IS VELOCITY",
            "The previous graph gives us the next question: what happens when velocity itself changes with time?",
        )

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=6.0,
            y_length=4.0,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        )
        axes.shift(LEFT * 3.55 + DOWN * 0.55)
        labels = VGroup(
            self.txt("time t (s)", 18).next_to(axes.x_axis, DOWN, buff=0.18),
            self.txt("position x (m)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.20),
        )
        line = axes.plot(lambda t: 1 + 1.6 * t, x_range=[0, 5], color=BLACK, stroke_width=4)
        p0 = Dot(axes.c2p(0, 1), radius=0.07, color=BLACK)
        p1 = Dot(axes.c2p(4, 7.4), radius=0.07, color=BLACK)
        dx_line = DashedLine(axes.c2p(0, 1), axes.c2p(4, 1), color=MID_GRAY)
        dy_line = DashedLine(axes.c2p(4, 1), axes.c2p(4, 7.4), color=MID_GRAY)
        graph_group = VGroup(axes, labels, line, p0, p1, dx_line, dy_line)

        slope = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}", width=5.5, height=1.15, size=48)
        slope.shift(RIGHT * 4.1 + UP * 1.0)
        question = self.note_panel(
            "NEW QUESTION",
            [
                "What if the slope is not constant?",
                "How can we describe changing velocity?",
                "Galileo's experiment gives the bridge.",
            ],
            width=5.5,
            title_size=25,
            body_size=22,
        )
        question.next_to(slope, DOWN, buff=0.28)

        self.play(Create(axes), FadeIn(labels), run_time=RUN)
        self.play(Create(line), FadeIn(p0), FadeIn(p1), run_time=RUN)
        self.play(Create(dx_line), Create(dy_line), run_time=RUN_FAST)
        self.play(FadeIn(slope), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 Galileo question
    # ------------------------------------------------------------------
    def galileo_question(self):
        self.set_header(
            2,
            "GALILEO'S PROBLEM: FALLING MOTION IS TOO FAST TO MEASURE EASILY",
            "A shallow inclined plane slows the evolution of motion while preserving a repeatable acceleration pattern.",
        )

        left_box = self.panel(6.6, 4.8, fill=WHITE)
        left_box.shift(LEFT * 3.65 + DOWN * 0.45)
        fall_title = self.txt("VERTICAL FALL", 25, BOLD).next_to(left_box.get_top(), DOWN, buff=0.30)
        fall_line = Line(LEFT * 4.9 + UP * 1.15, LEFT * 4.9 + DOWN * 1.65, color=BLACK, stroke_width=3)
        ball = Circle(radius=0.18, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(fall_line.get_start())
        fast = self.txt("Motion changes very quickly", 21).next_to(fall_line, RIGHT, buff=0.45)

        right_box = self.panel(6.6, 4.8, fill=WHITE)
        right_box.shift(RIGHT * 3.65 + DOWN * 0.45)
        ramp_title = self.txt("INCLINED PLANE", 25, BOLD).next_to(right_box.get_top(), DOWN, buff=0.30)
        rs = RIGHT * 1.4 + DOWN * 1.55
        re = RIGHT * 5.8 + UP * 0.95
        ramp = Line(rs, re, color=BLACK, stroke_width=4)
        sphere = Circle(radius=0.18, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(re)
        slow = self.txt("Longer time to observe the pattern", 21)
        slow.next_to(ramp, DOWN, buff=0.42)

        arrow = Arrow(LEFT * 0.55, RIGHT * 0.55, buff=0, color=BLACK, stroke_width=3)
        arrow.shift(DOWN * 0.35)
        purpose = self.txt("slow the experiment", 18, BOLD).next_to(arrow, UP, buff=0.12)

        self.play(FadeIn(left_box), FadeIn(fall_title), Create(fall_line), FadeIn(fast), run_time=RUN)
        self.play(MoveAlongPath(ball, fall_line), run_time=1.0 * TIME_SCALE, rate_func=rate_functions.ease_in_quad)
        self.play(FadeIn(right_box), FadeIn(ramp_title), Create(ramp), FadeIn(slow), run_time=RUN)
        self.play(FadeIn(arrow), FadeIn(purpose), run_time=RUN_FAST)
        self.play(MoveAlongPath(sphere, ramp.copy().reverse_points()), run_time=2.0 * TIME_SCALE, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 Apparatus reconstruction
    # ------------------------------------------------------------------
    def galileo_apparatus(self):
        self.set_header(
            3,
            "LAB RECONSTRUCTION: RAMP + BALL + DISTANCE MARKS + WATER CLOCK",
            "Repeat the release from rest and compare the distance traveled after equal intervals of time.",
        )

        start = np.array([-5.8, -2.0, 0])
        end = np.array([2.9, 1.55, 0])
        apparatus, ramp = self.make_ramp(start, end)
        apparatus.shift(LEFT * 0.65 + UP * 0.05)
        start2 = start + LEFT * 0.65 + UP * 0.05
        end2 = end + LEFT * 0.65 + UP * 0.05

        ball = Circle(radius=0.19, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(end2)
        release = self.txt("release from rest", 20, BOLD).next_to(ball, UP + RIGHT, buff=0.18)

        # Water clock on the right.
        jar = RoundedRectangle(
            width=1.55,
            height=2.25,
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        ).shift(RIGHT * 5.2 + DOWN * 0.45)
        water = Rectangle(
            width=1.30,
            height=1.15,
            stroke_width=0,
            fill_color=LIGHT_GRAY,
            fill_opacity=1,
        ).align_to(jar, DOWN).shift(UP * 0.12)
        outlet = Line(jar.get_bottom(), jar.get_bottom() + DOWN * 0.35, color=BLACK, stroke_width=2)
        drop = Dot(outlet.get_end() + DOWN * 0.12, radius=0.06, color=BLACK)
        clock_label = self.txt("water clock", 20, BOLD).next_to(jar, UP, buff=0.16)
        clock_note = self.txt("equal collected water → equal time", 18).next_to(jar, DOWN, buff=0.24)

        ruler = Line(start2, end2, color=MID_GRAY, stroke_width=1.2).shift(DOWN * 0.25)
        marks = VGroup()
        for u in np.linspace(0, 1, 9):
            p = self.ramp_point(start2, end2, u) + DOWN * 0.25
            marks.add(Dot(p, radius=0.035, color=MID_GRAY))

        procedure = self.note_panel(
            "PROCEDURE",
            [
                "1. Use the same starting point.",
                "2. Release without an initial push.",
                "3. Measure position after equal times.",
                "4. Repeat to check the pattern.",
            ],
            width=4.25,
            title_size=23,
            body_size=19,
        )
        procedure.shift(RIGHT * 4.85 + UP * 1.95)

        self.play(Create(apparatus), FadeIn(ruler), FadeIn(marks), run_time=RUN)
        self.play(FadeIn(ball), FadeIn(release), run_time=RUN_FAST)
        self.play(FadeIn(jar), FadeIn(water), Create(outlet), FadeIn(drop), FadeIn(clock_label), FadeIn(clock_note), run_time=RUN)
        self.play(FadeIn(procedure), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(MoveAlongPath(ball, Line(end2, start2)), run_time=2.6 * TIME_SCALE, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 Equal-time pattern
    # ------------------------------------------------------------------
    def equal_time_pattern(self):
        self.set_header(
            4,
            "EQUAL TIMES DO NOT PRODUCE EQUAL DISTANCES",
            "For motion from rest with constant acceleration, cumulative distance follows 1, 4, 9, 16 while interval distances follow 1, 3, 5, 7.",
        )

        start = np.array([-5.7, -1.95, 0])
        end = np.array([3.8, 1.35, 0])
        ramp = Line(start, end, color=BLACK, stroke_width=5)
        base = Line(LEFT * 6.4 + DOWN * 1.95, RIGHT * 4.6 + DOWN * 1.95, color=BLACK, stroke_width=2)

        times = [0, 1, 2, 3, 4]
        positions = [0, 1, 4, 9, 16]
        dots = VGroup()
        labels = VGroup()
        for t, s in zip(times, positions):
            u = s / 16
            p = self.ramp_point(end, start, u)
            dots.add(Dot(p, radius=0.075, color=BLACK))
            labels.add(self.txt(f"t={t}T   s={s}", 18, BOLD).next_to(p, UP + RIGHT, buff=0.10))

        interval_data = VGroup(
            self.txt("distance during each equal time interval", 21, BOLD),
            self.math(r"1\quad 3\quad 5\quad 7", 44),
            self.txt("the object covers more distance every second", 20),
        ).arrange(DOWN, buff=0.17)
        box = self.panel(5.2, 2.2, fill=WHITE)
        interval_data.move_to(box)
        interval_panel = VGroup(box, interval_data).shift(RIGHT * 4.55 + DOWN * 0.75)

        self.play(Create(base), Create(ramp), run_time=RUN)
        for i in range(len(dots)):
            self.play(FadeIn(dots[i], scale=0.5), FadeIn(labels[i]), run_time=RUN_FAST)
        self.wait(PAUSE_READ)
        self.play(FadeIn(interval_panel), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        # Highlight differences as 1,3,5,7 with braces on a simplified number line.
        number_line = NumberLine(x_range=[0, 16, 1], length=9.2, include_numbers=False, color=BLACK)
        number_line.shift(DOWN * 2.85 + LEFT * 1.05)
        marks = VGroup()
        for x in [0, 1, 4, 9, 16]:
            marks.add(Dot(number_line.n2p(x), radius=0.06, color=BLACK))
        inc_labels = VGroup()
        vals = [(0, 1, "1"), (1, 4, "3"), (4, 9, "5"), (9, 16, "7")]
        for a, b, val in vals:
            brace = BraceBetweenPoints(number_line.n2p(a), number_line.n2p(b), direction=UP, color=MID_GRAY)
            lab = self.math(val, 26).next_to(brace, UP, buff=0.05)
            inc_labels.add(VGroup(brace, lab))
        self.play(FadeIn(number_line), FadeIn(marks), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(g) for g in inc_labels], lag_ratio=0.16), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 x proportional to t²
    # ------------------------------------------------------------------
    def square_time_law(self):
        self.set_header(
            5,
            "THE EXPERIMENTAL PATTERN: POSITION GROWS WITH THE SQUARE OF TIME",
            "The 1, 4, 9, 16 sequence is the fingerprint of a quadratic position-time relation.",
        )

        # Table
        table_box = self.panel(5.0, 4.7, fill=WHITE).shift(LEFT * 4.55 + DOWN * 0.35)
        title = self.txt("EQUAL-TIME DATA", 24, BOLD).next_to(table_box.get_top(), DOWN, buff=0.28)
        rows = VGroup()
        header = VGroup(self.txt("t / T", 21, BOLD), self.txt("s / unit", 21, BOLD), self.txt("t²", 21, BOLD))
        header.arrange(RIGHT, buff=0.78)
        rows.add(header)
        for t in range(5):
            row = VGroup(self.math(str(t), 28), self.math(str(t*t), 28), self.math(str(t*t), 28))
            row.arrange(RIGHT, buff=1.00)
            rows.add(row)
        rows.arrange(DOWN, buff=0.24)
        rows.move_to(table_box).shift(DOWN * 0.18)

        # Graph
        axes = Axes(
            x_range=[0, 4.2, 1],
            y_range=[0, 17, 4],
            x_length=6.6,
            y_length=4.4,
            axis_config={"color": BLACK, "include_tip": False, "stroke_width": 2},
        ).shift(RIGHT * 2.9 + DOWN * 0.35)
        curve = axes.plot(lambda t: t**2, x_range=[0, 4], color=BLACK, stroke_width=4)
        points = VGroup(*[Dot(axes.c2p(t, t*t), radius=0.07, color=BLACK) for t in range(5)])
        graph_labels = VGroup(
            self.txt("time", 18).next_to(axes.x_axis, DOWN, buff=0.15),
            self.txt("position", 18).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.18),
        )

        formula = self.formula_panel(r"\Delta x\propto t^2", width=4.6, height=1.0, size=44)
        formula.next_to(axes, UP, buff=0.22)

        self.play(FadeIn(table_box), FadeIn(title), FadeIn(rows), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(Create(axes), FadeIn(graph_labels), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.12), run_time=RUN)
        self.play(Create(curve), run_time=RUN_SLOW)
        self.play(FadeIn(formula), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        conclusion = self.note_panel(
            "KINEMATIC INTERPRETATION",
            [
                "The velocity is changing.",
                "The change in velocity is regular.",
                "That regular change is constant acceleration.",
            ],
            width=5.1,
            title_size=22,
            body_size=20,
        ).shift(RIGHT * 4.55 + DOWN * 2.20)
        self.play(FadeIn(conclusion), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 Velocity-time meaning
    # ------------------------------------------------------------------
    def velocity_time_meaning(self):
        self.set_header(
            6,
            "CONSTANT ACCELERATION MEANS A STRAIGHT LINE ON A VELOCITY-TIME GRAPH",
            "Acceleration is the slope of velocity versus time: the velocity changes by the same amount each second.",
        )

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=7.0,
            y_length=4.5,
            axis_config={"color": BLACK, "include_tip": False, "stroke_width": 2},
        ).shift(LEFT * 2.9 + DOWN * 0.35)
        line = axes.plot(lambda t: 1 + t, x_range=[0, 5], color=BLACK, stroke_width=4)
        p0 = Dot(axes.c2p(0, 1), radius=0.07, color=BLACK)
        p1 = Dot(axes.c2p(4, 5), radius=0.07, color=BLACK)
        dash_h = DashedLine(axes.c2p(0, 1), axes.c2p(4, 1), color=MID_GRAY)
        dash_v = DashedLine(axes.c2p(4, 1), axes.c2p(4, 5), color=MID_GRAY)
        graph_labels = VGroup(
            self.txt("time t", 18).next_to(axes.x_axis, DOWN, buff=0.15),
            self.txt("velocity v", 18).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.20),
        )

        formula = self.formula_panel(r"a=\frac{\Delta v}{\Delta t}", width=5.2, height=1.15, size=46)
        formula.shift(RIGHT * 4.35 + UP * 0.95)
        note = self.note_panel(
            "READ THE SLOPE",
            [
                "positive slope → positive acceleration",
                "zero slope → constant velocity",
                "negative slope → negative acceleration",
            ],
            width=5.2,
            title_size=23,
            body_size=20,
        ).next_to(formula, DOWN, buff=0.25)

        self.play(Create(axes), FadeIn(graph_labels), run_time=RUN)
        self.play(Create(line), FadeIn(p0), FadeIn(p1), run_time=RUN)
        self.play(Create(dash_h), Create(dash_v), run_time=RUN_FAST)
        self.play(FadeIn(formula), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 First equation
    # ------------------------------------------------------------------
    def derive_first_equation(self):
        self.set_header(
            7,
            "DERIVE EQUATION 1 FROM THE SLOPE OF THE v-t GRAPH",
            "Start with the definition of acceleration and isolate the final velocity.",
        )

        steps = VGroup(
            self.math(r"a=\frac{\Delta v}{\Delta t}", 44),
            self.math(r"a=\frac{v-v_0}{t}", 44),
            self.math(r"at=v-v_0", 44),
            self.math(r"\boxed{v=v_0+at}", 50),
        )
        steps.arrange(DOWN, buff=0.37, aligned_edge=LEFT)
        steps.shift(LEFT * 3.3 + DOWN * 0.25)

        meaning = self.note_panel(
            "WHAT IT PREDICTS",
            [
                "Given v₀, a and t, find v.",
                "Velocity changes linearly with time.",
                "The sign of a controls the direction of change.",
            ],
            width=5.7,
            title_size=24,
            body_size=21,
        ).shift(RIGHT * 4.0 + DOWN * 0.05)

        for i, eq in enumerate(steps):
            self.play(FadeIn(eq, shift=UP * 0.08), run_time=RUN)
            if i < len(steps) - 1:
                self.wait(PAUSE_SHORT)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 Second equation via area
    # ------------------------------------------------------------------
    def derive_second_equation(self):
        self.set_header(
            8,
            "DERIVE EQUATION 2 FROM THE AREA UNDER THE v-t GRAPH",
            "Displacement is the accumulated velocity: rectangle area + triangle area.",
        )

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=7.0,
            y_length=4.8,
            axis_config={"color": BLACK, "include_tip": False, "stroke_width": 2},
        ).shift(LEFT * 3.05 + DOWN * 0.45)
        v0 = 1.3
        a = 0.8
        t_end = 4.2
        line = axes.plot(lambda t: v0 + a * t, x_range=[0, t_end], color=BLACK, stroke_width=4)
        base_line = Line(axes.c2p(0, 0), axes.c2p(t_end, 0), color=BLACK, stroke_width=2)
        v0_line = DashedLine(axes.c2p(0, v0), axes.c2p(t_end, v0), color=MID_GRAY)

        rect = Polygon(
            axes.c2p(0, 0), axes.c2p(t_end, 0), axes.c2p(t_end, v0), axes.c2p(0, v0),
            stroke_color=MID_GRAY, stroke_width=1.5, fill_color=LIGHT_GRAY, fill_opacity=0.45,
        )
        tri = Polygon(
            axes.c2p(0, v0), axes.c2p(t_end, v0), axes.c2p(t_end, v0 + a*t_end),
            stroke_color=BLACK, stroke_width=1.5, fill_color=PAPER_GRAY, fill_opacity=0.85,
        )
        labels = VGroup(
            self.txt("time t", 18).next_to(axes.x_axis, DOWN, buff=0.15),
            self.txt("velocity v", 18).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.20),
            self.math(r"v_0", 27).next_to(axes.c2p(0, v0), LEFT, buff=0.08),
            self.math(r"at", 27).next_to(axes.c2p(t_end, v0 + a*t_end/2), RIGHT, buff=0.08),
        )

        derivation = VGroup(
            self.txt("AREA = DISPLACEMENT", 24, BOLD),
            self.math(r"\Delta x=A_{rectangle}+A_{triangle}", 36),
            self.math(r"\Delta x=v_0t+\frac12(t)(at)", 36),
            self.math(r"\boxed{\Delta x=v_0t+\frac12at^2}", 42),
        ).arrange(DOWN, buff=0.34)
        self.fit(derivation, 6.0, 4.6)
        derivation.shift(RIGHT * 4.35 + DOWN * 0.20)

        self.play(Create(axes), Create(base_line), FadeIn(labels), run_time=RUN)
        self.play(Create(line), Create(v0_line), run_time=RUN)
        self.play(FadeIn(rect), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(tri), run_time=RUN)
        self.wait(PAUSE_READ)
        for mob in derivation:
            self.play(FadeIn(mob), run_time=RUN_FAST)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 Third equation
    # ------------------------------------------------------------------
    def derive_third_equation(self):
        self.set_header(
            9,
            "DERIVE EQUATION 3 BY ELIMINATING TIME",
            "For constant acceleration, average velocity is the midpoint between the initial and final velocities.",
        )

        left = VGroup(
            self.math(r"v_{avg}=\frac{v_0+v}{2}", 39),
            self.math(r"\Delta x=v_{avg}t", 39),
            self.math(r"t=\frac{v-v_0}{a}", 39),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        left_box = self.panel(6.0, 4.0, fill=WHITE)
        left.move_to(left_box)
        left_group = VGroup(left_box, left).shift(LEFT * 4.0 + DOWN * 0.35)

        right = VGroup(
            self.math(r"\Delta x=\frac{v_0+v}{2}\left(\frac{v-v_0}{a}\right)", 34),
            self.math(r"2a\Delta x=(v_0+v)(v-v_0)", 34),
            self.math(r"2a\Delta x=v^2-v_0^2", 36),
            self.math(r"\boxed{v^2=v_0^2+2a\Delta x}", 43),
        ).arrange(DOWN, buff=0.34)
        right_box = self.panel(7.2, 4.4, fill=PAPER_GRAY)
        right.move_to(right_box)
        right_group = VGroup(right_box, right).shift(RIGHT * 3.55 + DOWN * 0.35)

        arrow = Arrow(LEFT * 0.65, RIGHT * 0.65, color=BLACK, stroke_width=3).shift(DOWN * 0.35)

        self.play(FadeIn(left_group), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(arrow), run_time=RUN_FAST)
        for eq in right:
            self.play(FadeIn(eq, shift=UP * 0.05), run_time=RUN)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(right_box), run_time=RUN_FAST)
        self.bring_to_front(right)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 Worked lab example
    # ------------------------------------------------------------------
    def worked_lab_example(self):
        self.set_header(
            10,
            "WORKED LAB PREDICTION: A CART STARTS FROM REST ON A SHALLOW RAMP",
            "Use the equations to predict the velocity and displacement after 3.0 s, then cross-check the result.",
        )

        # Physical sketch
        rs = np.array([-6.0, -1.55, 0])
        re = np.array([-1.0, 1.25, 0])
        ramp = Line(rs, re, color=BLACK, stroke_width=5)
        floor = Line(LEFT * 6.5 + DOWN * 1.55, RIGHT * 0.0 + DOWN * 1.55, color=BLACK, stroke_width=2)
        cart = RoundedRectangle(width=0.72, height=0.42, corner_radius=0.08, stroke_color=BLACK, fill_color=WHITE, fill_opacity=1)
        cart.move_to(re + LEFT * 0.12 + DOWN * 0.05)
        sketch = VGroup(ramp, floor, cart)

        givens = self.note_panel(
            "MEASURED / GIVEN",
            [
                "v₀ = 0 m/s",
                "a = 0.80 m/s²",
                "t = 3.0 s",
            ],
            width=3.8,
            title_size=22,
            body_size=21,
        ).shift(LEFT * 3.9 + UP * 2.0)

        equations = VGroup(
            self.math(r"v=v_0+at", 34),
            self.math(r"v=0+(0.80)(3.0)=2.4\ \mathrm{m/s}", 32),
            self.math(r"\Delta x=v_0t+\frac12at^2", 34),
            self.math(r"\Delta x=\frac12(0.80)(3.0)^2=3.6\ \mathrm{m}", 32),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        eq_box = self.panel(7.4, 4.1, fill=PAPER_GRAY)
        equations.move_to(eq_box)
        eq_group = VGroup(eq_box, equations).shift(RIGHT * 3.75 + DOWN * 0.15)

        check = self.formula_panel(r"v^2=2a\Delta x\;\Rightarrow\;(2.4)^2=2(0.80)(3.6)=5.76", width=7.3, height=1.05, size=31)
        check.shift(RIGHT * 3.75 + DOWN * 2.85)

        self.play(Create(ramp), Create(floor), FadeIn(cart), FadeIn(givens), run_time=RUN)
        self.wait(PAUSE_READ)
        for eq in equations:
            self.play(FadeIn(eq), run_time=RUN_FAST)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(eq_box), run_time=RUN_FAST)
        self.bring_to_front(equations)
        self.play(MoveAlongPath(cart, Line(re, rs + RIGHT * 1.4)), run_time=2.0 * TIME_SCALE, rate_func=rate_functions.ease_in_quad)
        self.play(FadeIn(check), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 11 Three graphs
    # ------------------------------------------------------------------
    def three_graphs_one_motion(self):
        self.set_header(
            11,
            "ONE MOTION, THREE GRAPHS",
            "Position curves upward, velocity rises linearly, and acceleration stays constant.",
        )

        a = 0.8
        tmax = 4.0
        configs = [
            (LEFT * 5.0, "POSITION vs TIME", r"x(t)=\frac12at^2", lambda t: 0.5*a*t*t, [0, 4.5, 1]),
            (ORIGIN, "VELOCITY vs TIME", r"v(t)=at", lambda t: a*t, [0, 3.5, 1]),
            (RIGHT * 5.0, "ACCELERATION vs TIME", r"a(t)=a", lambda t: a, [0, 1.2, 0.4]),
        ]

        groups = VGroup()
        for center, title_text, formula_text, func, yrange in configs:
            axes = Axes(
                x_range=[0, tmax, 1],
                y_range=yrange,
                x_length=4.0,
                y_length=3.2,
                axis_config={"color": BLACK, "include_tip": False, "stroke_width": 1.8},
            ).move_to(center + DOWN * 0.35)
            graph = axes.plot(func, x_range=[0, tmax], color=BLACK, stroke_width=3.5)
            title = self.txt(title_text, 20, BOLD).next_to(axes, UP, buff=0.16)
            formula = self.math(formula_text, 28).next_to(axes, DOWN, buff=0.18)
            groups.add(VGroup(axes, graph, title, formula))

        connectors = VGroup(
            self.txt("slope → v", 18, BOLD).move_to(LEFT * 2.5 + UP * 2.35),
            self.txt("slope → a", 18, BOLD).move_to(RIGHT * 2.5 + UP * 2.35),
            Arrow(LEFT * 3.2 + UP * 2.05, LEFT * 1.8 + UP * 2.05, buff=0, color=BLACK, stroke_width=2.5),
            Arrow(RIGHT * 1.8 + UP * 2.05, RIGHT * 3.2 + UP * 2.05, buff=0, color=BLACK, stroke_width=2.5),
        )

        for grp in groups:
            self.play(Create(grp[0]), FadeIn(grp[2]), run_time=RUN)
            self.play(Create(grp[1]), FadeIn(grp[3]), run_time=RUN)
        self.play(FadeIn(connectors), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        area_note = self.note_panel(
            "AREA LINKS",
            [
                "area under v-t → displacement Δx",
                "area under a-t → change in velocity Δv",
            ],
            width=6.2,
            title_size=22,
            body_size=20,
        ).shift(DOWN * 3.05)
        self.play(FadeIn(area_note), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 12 Student challenge
    # ------------------------------------------------------------------
    def student_challenge(self):
        self.set_header(
            12,
            "STUDENT CHALLENGE: RECONSTRUCT THE MOTION FROM DATA",
            "Decide whether the motion is uniformly accelerated, then predict the next position without being given the answer.",
        )

        table_box = self.panel(6.6, 4.7, fill=WHITE).shift(LEFT * 3.7 + DOWN * 0.25)
        headings = VGroup(
            self.txt("t (s)", 22, BOLD),
            self.txt("x (m)", 22, BOLD),
            self.txt("Δx each second", 22, BOLD),
        ).arrange(RIGHT, buff=0.78)
        rows = VGroup(headings)
        data = [
            (0, 0.0, "—"),
            (1, 0.5, "0.5"),
            (2, 2.0, "1.5"),
            (3, 4.5, "2.5"),
            (4, 8.0, "3.5"),
            (5, "?", "?"),
        ]
        for t, x, dx in data:
            x_text = str(x) if isinstance(x, str) else f"{x:.1f}"
            row = VGroup(self.txt(str(t), 21), self.txt(x_text, 21), self.txt(str(dx), 21))
            row.arrange(RIGHT, buff=1.28)
            rows.add(row)
        rows.arrange(DOWN, buff=0.21)
        self.fit(rows, 5.9, 4.1)
        rows.move_to(table_box)

        tasks = self.note_panel(
            "YOUR TASK",
            [
                "1. Find the next interval distance.",
                "2. Predict x at t = 5 s.",
                "3. Identify the acceleration.",
                "4. Draw the v-t graph.",
                "5. Verify using one MUA equation.",
            ],
            width=5.8,
            title_size=24,
            body_size=21,
        ).shift(RIGHT * 4.15 + UP * 0.30)

        clue = self.formula_panel(r"\Delta x_{interval}:\;0.5,\;1.5,\;2.5,\;3.5,\;\ldots", width=6.1, height=1.0, size=31)
        clue.shift(RIGHT * 4.15 + DOWN * 2.55)

        self.play(FadeIn(table_box), FadeIn(rows), run_time=RUN)
        self.play(FadeIn(tasks), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(clue), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 13 Summary
    # ------------------------------------------------------------------
    def summary(self):
        self.set_header(
            13,
            "SUMMARY: FROM GALILEO'S MEASUREMENTS TO A REUSABLE METHOD",
            "Use the physical situation first, then select the equation that matches the known and unknown quantities.",
        )

        equations = VGroup(
            self.formula_panel(r"v=v_0+at", width=4.5, height=1.0, size=40),
            self.formula_panel(r"\Delta x=v_0t+\frac12at^2", width=5.2, height=1.0, size=36),
            self.formula_panel(r"v^2=v_0^2+2a\Delta x", width=5.0, height=1.0, size=36),
        ).arrange(RIGHT, buff=0.28)
        equations.shift(UP * 1.55)

        route = VGroup()
        labels = [
            ("1", "DEFINE + DIRECTION"),
            ("2", "LIST KNOWN VALUES"),
            ("3", "IDENTIFY THE UNKNOWN"),
            ("4", "SELECT THE EQUATION"),
            ("5", "SUBSTITUTE WITH UNITS"),
            ("6", "CHECK SIGN + GRAPH"),
        ]
        for number, text in labels:
            card = self.panel(4.2, 1.0, fill=WHITE)
            n = self.txt(number, 24, BOLD)
            label = self.txt(text, 19, BOLD)
            content = VGroup(n, label).arrange(RIGHT, buff=0.22).move_to(card)
            route.add(VGroup(card, content))
        route.arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.30))
        route.shift(DOWN * 0.35)

        takeaway = self.txt(
            "Galileo's key idea: measure a regular pattern carefully enough, and an equation emerges from the data.",
            23,
            BOLD,
            color=DARK_GRAY,
        )
        self.fit(takeaway, 13.4, 0.7)
        takeaway.to_edge(DOWN, buff=0.42)

        self.play(LaggedStart(*[FadeIn(eq, shift=UP * 0.06) for eq in equations], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.05) for card in route], lag_ratio=0.09), run_time=RUN_SLOW)
        self.play(FadeIn(takeaway), run_time=RUN)
        self.wait(PAUSE_FINAL)

        # Closing title.
        closing = VGroup(
            self.txt("PHYSICS 9", 26, BOLD),
            self.txt("OBSERVE → MODEL → CALCULATE → VERIFY", 36, BOLD),
            self.txt("Next: velocity-time and acceleration-time problem solving", 23),
        ).arrange(DOWN, buff=0.28)
        closing_box = self.panel(10.8, 3.0, fill=WHITE)
        closing.move_to(closing_box)
        final_group = VGroup(closing_box, closing)
        self.play(FadeOut(equations), FadeOut(route), FadeOut(takeaway), run_time=RUN)
        if self.header_group is not None:
            self.play(FadeOut(self.header_group), run_time=RUN_FAST)
        self.play(FadeIn(final_group, scale=0.98), run_time=RUN)
        self.wait(PAUSE_FINAL)


# Preview:
# manim -pql Physics9_Galileo_Inclined_Plane_MUA_FINAL.py Physics9GalileoInclinedPlaneFinal --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Inclined_Plane_MUA_FINAL.py Physics9GalileoInclinedPlaneFinal --disable_caching
