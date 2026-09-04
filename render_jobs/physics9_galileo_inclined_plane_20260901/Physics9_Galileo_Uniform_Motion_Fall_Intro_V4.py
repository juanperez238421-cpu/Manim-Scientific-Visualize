#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior visual-QA refinement of the focused Physics 9 uniform-motion lesson.

V4 keeps the validated V3 pedagogical sequence and corrects the four issues
found in the distributed contact-sheet audit: overly long headers, an overly
steep starter ramp, insufficiently visible equal-time snapshots in the lab,
and falling snapshots that did not exactly follow the displayed square-time
pattern.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_Galileo_Uniform_Motion_Fall_Intro_V3 import (
    Physics9GalileoUniformMotionFallIntroV3,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    RUN,
    RUN_FAST,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)


class Physics9GalileoUniformMotionFallIntroV4(Physics9GalileoUniformMotionFallIntroV3):
    """Final senior-QA scene focused on deriving x = x_i + vt experimentally."""

    def uniform_motion_apparatus(self):
        self.set_header(
            2,
            "GALILEO-INSPIRED LAB: RAMP -> HORIZONTAL TRACK",
            "The ramp starts the ball; the idealized low-friction horizontal zone is where equal-time positions are measured.",
        )

        # Shallow starter ramp, visually closer to the historical classroom idea.
        ramp_top = np.array([-5.65, 0.85, 0.0])
        join = np.array([-3.00, -1.15, 0.0])
        track_end = np.array([6.15, -1.15, 0.0])
        ramp = Line(ramp_top, join, color=BLACK, stroke_width=5)
        track = Line(join, track_end, color=BLACK, stroke_width=5)
        floor = Line(LEFT * 6.4 + DOWN * 1.65, RIGHT * 6.4 + DOWN * 1.65,
                     color=LIGHT_GRAY, stroke_width=1.5)

        ball = Circle(radius=0.18, stroke_color=BLACK, stroke_width=2,
                      fill_color=WHITE, fill_opacity=1).move_to(ramp_top + UP * 0.18)
        label_ramp = self.txt("STARTER RAMP", 20, BOLD).move_to(LEFT * 4.75 + UP * 1.45)
        label_measure = self.txt("HORIZONTAL MEASUREMENT ZONE", 20, BOLD).move_to(RIGHT * 1.55 + UP * 1.05)

        # Five equal-time measurement positions, separated by equal distances.
        mark_xs = [-2.50, -1.00, 0.50, 2.00, 3.50]
        marks = VGroup()
        labels = VGroup()
        for i, x in enumerate(mark_xs):
            marks.add(Line([x, -1.42, 0], [x, -0.88, 0], color=MID_GRAY, stroke_width=1.6))
            labels.add(self.txt(f"t={i} s", 17, color=DARK_GRAY).move_to([x, -1.78, 0]))

        stopwatch = self.panel(2.55, 1.45, fill=WHITE).move_to(RIGHT * 5.05 + UP * 2.35)
        stopwatch_title = self.txt("EQUAL TIMES", 20, BOLD).next_to(stopwatch.get_top(), DOWN, buff=0.20)
        stopwatch_eq = self.math(r"\Delta t=1\ \mathrm{s}", 30).move_to(stopwatch).shift(DOWN * 0.18)
        clock = VGroup(stopwatch, stopwatch_title, stopwatch_eq)

        reminder = self.note_panel(
            "MEASUREMENT RULE",
            [
                "The ramp is only the launcher.",
                "Build the model from the horizontal snapshots.",
            ],
            width=5.8,
            title_size=21,
            body_size=18,
        ).move_to(LEFT * 2.4 + DOWN * 2.70)

        self.play(Create(ramp), Create(track), Create(floor), run_time=RUN)
        self.play(FadeIn(label_ramp), FadeIn(label_measure), FadeIn(clock), run_time=RUN)
        self.play(FadeIn(marks), FadeIn(labels), FadeIn(ball), FadeIn(reminder), run_time=RUN)
        self.wait(PAUSE_READ)

        # Stage 1: ramp creates the motion.
        self.play(
            MoveAlongPath(ball, Line(ramp_top + UP * 0.18, join + UP * 0.20)),
            run_time=1.55,
            rate_func=rate_functions.ease_in_quad,
        )

        # Stage 2: move into the measurement zone and leave a visible strobe
        # snapshot after each equal time interval. This makes the deduction
        # visually explicit instead of only stating it later in a table.
        y_ball = -0.95
        self.play(ball.animate.move_to([mark_xs[0], y_ball, 0]), run_time=0.35, rate_func=linear)
        ghosts = VGroup()
        first = Circle(radius=0.16, stroke_color=MID_GRAY, stroke_width=1.8,
                       fill_color=PAPER_GRAY, fill_opacity=0.65).move_to([mark_xs[0], y_ball, 0])
        ghosts.add(first)
        self.play(FadeIn(first), run_time=RUN_FAST)

        equal_arrows = VGroup()
        for i in range(1, len(mark_xs)):
            target = np.array([mark_xs[i], y_ball, 0.0])
            self.play(ball.animate.move_to(target), run_time=0.78, rate_func=linear)
            ghost = Circle(radius=0.16, stroke_color=MID_GRAY, stroke_width=1.8,
                           fill_color=PAPER_GRAY, fill_opacity=0.65).move_to(target)
            ghosts.add(ghost)
            self.play(FadeIn(ghost), run_time=0.18)
            arrow = DoubleArrow(
                [mark_xs[i-1] + 0.20, -0.35, 0],
                [mark_xs[i] - 0.20, -0.35, 0],
                color=MID_GRAY,
                stroke_width=1.5,
                buff=0,
            )
            equal_arrows.add(arrow)
            self.play(Create(arrow), run_time=0.20)

        result = self.formula_panel(
            r"\Delta t\ \text{equal}\quad\Longrightarrow\quad\Delta x\ \text{equal}",
            width=7.0,
            height=0.85,
            size=31,
        ).move_to(RIGHT * 2.15 + DOWN * 2.75)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def interpret_and_predict(self):
        # Use the V3 content but shorten the header so it remains inside the
        # safe title width on every 16:9 frame.
        self.set_header(
            5,
            "INTERPRET x = x_i + vt: START + TRAVELED DISTANCE",
            "The formula is a position statement, not just an algebra rule.",
        )

        equation = self.formula_panel(r"x=x_i+vt", width=5.6, height=1.0, size=48)
        equation.shift(UP * 2.25)
        parts = VGroup(
            self.note_panel("x_i", ["where the object starts"], width=3.6, title_size=25, body_size=18),
            self.note_panel("v t", ["distance added during time t"], width=4.2, title_size=25, body_size=18),
            self.note_panel("x", ["predicted final position"], width=3.6, title_size=25, body_size=18),
        ).arrange(RIGHT, buff=0.35).shift(UP * 0.65)
        values = self.formula_panel(
            r"x_i=2.0\,\mathrm{m},\quad v=1.2\,\mathrm{m/s},\quad t=4.0\,\mathrm{s}",
            width=9.6, height=0.92, size=31,
        ).shift(DOWN * 0.75)
        calc = self.math(r"x=2.0+(1.2)(4.0)=\boxed{6.8\,\mathrm{m}}", 42).shift(DOWN * 1.75)
        numberline = NumberLine(x_range=[0, 8, 1], length=10.5, include_numbers=True,
                                color=BLACK, font_size=20).shift(DOWN * 3.0)
        start_dot = Dot(numberline.n2p(2.0), radius=0.08, color=BLACK)
        end_dot = Dot(numberline.n2p(6.8), radius=0.10, color=BLACK)
        start_lab = self.txt("start", 17, BOLD).next_to(start_dot, UP, buff=0.08)
        end_lab = self.txt("prediction", 17, BOLD).next_to(end_dot, UP, buff=0.08)
        travel = Arrow(numberline.n2p(2.0) + UP * 0.35,
                       numberline.n2p(6.8) + UP * 0.35,
                       color=MID_GRAY, stroke_width=2.2, buff=0.05)

        self.play(FadeIn(equation), FadeIn(parts), run_time=RUN)
        self.play(FadeIn(values), run_time=RUN)
        self.play(Write(calc), run_time=RUN)
        self.play(Create(numberline), FadeIn(start_dot), FadeIn(start_lab), run_time=RUN)
        self.play(GrowArrow(travel), FadeIn(end_dot), FadeIn(end_lab), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def position_time_graph(self):
        self.set_header(
            6,
            "x(t) IS A STRAIGHT LINE FOR UNIFORM MOTION",
            "The intercept is x_i and the slope is v: experiment, algebra, and graph tell the same story.",
        )

        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 9, 1], x_length=7.1, y_length=4.8,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        ).shift(LEFT * 3.2 + DOWN * 0.45)
        labels = VGroup(
            self.txt("time t (s)", 18).next_to(axes.x_axis, DOWN, buff=0.18),
            self.txt("position x (m)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.20),
        )
        line = axes.plot(lambda t: 1.0 + 1.5 * t, x_range=[0, 5], color=BLACK, stroke_width=4)
        intercept = Dot(axes.c2p(0, 1.0), radius=0.08, color=BLACK)
        ilab = self.math(r"x_i", 26).next_to(intercept, LEFT, buff=0.12)
        p1 = axes.c2p(1, 2.5)
        p3 = axes.c2p(3, 5.5)
        run = DashedLine(p1, [p3[0], p1[1], 0], color=MID_GRAY)
        rise = DashedLine([p3[0], p1[1], 0], p3, color=MID_GRAY)
        slope = self.math(r"v=\frac{\Delta x}{\Delta t}", 34).shift(RIGHT * 4.1 + UP * 1.3)
        linear = self.formula_panel(r"x=x_i+vt", width=5.2, height=1.0, size=44).shift(RIGHT * 4.1 + DOWN * 0.15)
        mapnote = self.note_panel(
            "GRAPH ↔ EQUATION",
            ["vertical intercept  ->  x_i", "slope               ->  v", "straight line       ->  constant v"],
            width=5.2, title_size=22, body_size=19,
        ).shift(RIGHT * 4.1 + DOWN * 2.0)

        self.play(Create(axes), FadeIn(labels), run_time=RUN)
        self.play(Create(line), FadeIn(intercept), FadeIn(ilab), run_time=RUN)
        self.play(Create(run), Create(rise), FadeIn(slope), run_time=RUN)
        self.play(FadeIn(linear), FadeIn(mapnote), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_motion_transition(self):
        self.set_header(
            7,
            "COMPARE: UNIFORM MOTION VS FALLING MOTION",
            "Repeat the equal-time snapshot idea: falling positions spread farther apart as time passes.",
        )

        left_box = self.panel(6.6, 4.9, fill=WHITE).shift(LEFT * 3.6 + DOWN * 0.35)
        lt = self.txt("UNIFORM MOTION", 23, BOLD).next_to(left_box.get_top(), DOWN, buff=0.25)
        hline = Line(LEFT * 6.0 + DOWN * 0.55, LEFT * 1.2 + DOWN * 0.55, color=BLACK, stroke_width=3)
        hxs = [-5.7, -4.55, -3.4, -2.25, -1.1]
        hdots = VGroup(*[Dot([x, -0.37, 0], radius=0.075, color=BLACK) for x in hxs])
        htext = self.txt("equal time -> equal spacing", 19, BOLD).next_to(hline, DOWN, buff=0.55)

        right_box = self.panel(6.6, 4.9, fill=WHITE).shift(RIGHT * 3.6 + DOWN * 0.35)
        rt = self.txt("FALLING MOTION", 23, BOLD).next_to(right_box.get_top(), DOWN, buff=0.25)
        fall_line = Line(RIGHT * 3.6 + UP * 1.35, RIGHT * 3.6 + DOWN * 2.05, color=LIGHT_GRAY, stroke_width=2)
        # Exact square-time snapshots: y = y0 - k t^2.
        ys = [1.30 - 0.22 * (i ** 2) for i in range(4)]
        fdots = VGroup(*[Dot([3.6, y, 0], radius=0.08, color=BLACK) for y in ys])
        flabels = VGroup(*[self.txt(f"t={i}s", 16).next_to(fdots[i], RIGHT, buff=0.12) for i in range(4)])
        ftext = self.txt("equal time -> growing spacing", 19, BOLD).next_to(fall_line, DOWN, buff=0.28)

        question = self.formula_panel(
            r"\text{A single constant }v\text{ cannot model the whole fall.}",
            width=9.2, height=0.9, size=30,
        ).to_edge(DOWN, buff=0.25)

        self.play(FadeIn(left_box), FadeIn(right_box), FadeIn(lt), FadeIn(rt), run_time=RUN)
        self.play(Create(hline), FadeIn(hdots), FadeIn(htext), run_time=RUN)
        self.play(Create(fall_line), run_time=RUN_FAST)
        for i in range(4):
            self.play(FadeIn(fdots[i]), FadeIn(flabels[i]), run_time=0.35)
        self.play(FadeIn(ftext), FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def summary_refocused(self):
        self.set_header(
            9,
            "SUMMARY: FROM MEASUREMENTS TO x = x_i + vt",
            "Today's target is uniform motion; falling motion is only the bridge to the next lesson.",
        )
        flow = VGroup(
            self.note_panel("1  OBSERVE", ["equal times -> equal distances"], width=3.2, title_size=21, body_size=17),
            self.note_panel("2  DEFINE", [r"v = Δx / Δt"], width=3.2, title_size=21, body_size=17),
            self.note_panel("3  REWRITE", [r"v = (x - x_i) / t"], width=3.2, title_size=21, body_size=17),
            self.note_panel("4  SOLVE", [r"x = x_i + vt"], width=3.2, title_size=21, body_size=17),
        ).arrange(RIGHT, buff=0.30).shift(UP * 1.5)
        target = self.formula_panel(r"\boxed{x=x_i+vt}", width=6.0, height=1.2, size=54).shift(DOWN * 0.20)
        next_box = self.note_panel(
            "NEXT CLASS",
            [
                "Why do falling positions spread farther apart?",
                "What does the symbol g tell us physically?",
                "How does the square-time law change our model?",
            ],
            width=8.7, title_size=24, body_size=20,
        ).shift(DOWN * 2.25)
        self.play(FadeIn(flow), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.play(FadeIn(next_box), run_time=RUN)
        self.wait(4.0)


# Preview:
# manim -pql Physics9_Galileo_Uniform_Motion_Fall_Intro_V4.py Physics9GalileoUniformMotionFallIntroV4 --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Uniform_Motion_Fall_Intro_V4.py Physics9GalileoUniformMotionFallIntroV4 --disable_caching
