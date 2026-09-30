#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Uniform Motion + Galileo V5.2 · final visual-QA pass.

This pass is based on manual inspection of every 1-second audit frame from V5.1.
It fixes the residual issues that remained after the first QA correction:
1) physical-motion text still touching the track caption,
2) x-t slope label touching the x-axis time label,
3) water-clock note touching the instrument-panel border,
4) the Galileo data table occupying the header/number-line area,
5) the falling-motion observation extending outside its panel.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_1_SENIOR_QA import (
    Physics9UniformMotionGalileoV5SeniorQAFixed,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    RUN_FAST,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)


class Physics9UniformMotionGalileoV52FinalQA(Physics9UniformMotionGalileoV5SeniorQAFixed):
    """Residual-overlap correction after manual one-second frame audit."""

    def uniform_motion_two_graphs(self):
        self.set_header(
            1,
            "ONE UNIFORM MOTION, TWO GRAPHS",
            "A straight position-time line and a horizontal velocity-time line describe the same constant-velocity motion.",
        )

        left_panel = self.panel(5.35, 4.55, fill=WHITE).move_to(LEFT * 4.15 + UP * 0.15)
        left_title = self.txt("PHYSICAL MOTION", 22, BOLD).next_to(left_panel.get_top(), DOWN, buff=0.22)
        slope = self.formula_panel(
            r"v=\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",
            width=4.45, height=0.80, size=29,
        ).move_to(left_panel.get_center() + UP * 1.30)

        track_y = 0.28
        track = Line([-6.15, track_y, 0], [-2.20, track_y, 0], color=BLACK, stroke_width=4)
        ticks = VGroup(*[
            Line([-5.75 + i * 0.82, track_y - 0.17, 0], [-5.75 + i * 0.82, track_y + 0.17, 0], color=MID_GRAY, stroke_width=1.4)
            for i in range(5)
        ])
        cart = RoundedRectangle(
            width=0.88, height=0.46, corner_radius=0.08,
            stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1,
        ).move_to([-5.70, track_y + 0.36, 0])
        wheel1 = Circle(radius=0.075, color=BLACK).move_to(cart.get_bottom() + DOWN * 0.02 + LEFT * 0.22)
        wheel2 = Circle(radius=0.075, color=BLACK).move_to(cart.get_bottom() + DOWN * 0.02 + RIGHT * 0.22)
        cartg = VGroup(cart, wheel1, wheel2)
        equal_note = self.txt("equal distance every second", 18, BOLD, color=DARK_GRAY)
        equal_note.next_to(track, DOWN, buff=0.16)

        read = VGroup(
            self.txt("READ BOTH GRAPHS", 20, BOLD),
            self.txt("x-t: straight line -> constant slope", 17),
            self.txt("v-t: horizontal line -> constant velocity", 17),
            self.txt("Both represent the SAME motion.", 17, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        read.move_to(left_panel.get_center() + DOWN * 1.42).align_to(left_panel, LEFT).shift(RIGHT * 0.34)

        xaxes = Axes(
            x_range=[0, 4.4, 1], y_range=[0, 7.8, 1],
            x_length=5.55, y_length=2.55,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        ).move_to(RIGHT * 3.45 + UP * 1.35)
        xgraph = xaxes.plot(lambda t: 1 + 1.5 * t, x_range=[0, 4], color=BLACK, stroke_width=4)
        xtitle = self.txt("POSITION vs TIME", 21, BOLD).next_to(xaxes, UP, buff=0.11)
        xlabs = VGroup(
            self.txt("t (s)", 16).next_to(xaxes.x_axis, DOWN, buff=0.08),
            self.txt("x (m)", 16).rotate(PI / 2).next_to(xaxes.y_axis, LEFT, buff=0.12),
        )
        p0 = Dot(xaxes.c2p(0, 1), radius=0.06, color=BLACK)
        p1 = Dot(xaxes.c2p(4, 7), radius=0.06, color=BLACK)
        dtx = DashedLine(xaxes.c2p(0, 1), xaxes.c2p(4, 1), color=MID_GRAY)
        dxx = DashedLine(xaxes.c2p(4, 1), xaxes.c2p(4, 7), color=MID_GRAY)

        vaxes = Axes(
            x_range=[0, 4.4, 1], y_range=[0, 2.2, 0.5],
            x_length=5.55, y_length=1.82,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        ).move_to(RIGHT * 3.45 + DOWN * 2.10)
        vgraph = vaxes.plot(lambda t: 1.5, x_range=[0, 4], color=BLACK, stroke_width=4)
        vtitle = self.txt("VELOCITY vs TIME", 21, BOLD).next_to(vaxes, UP, buff=0.10)
        vlabs = VGroup(
            self.txt("t (s)", 16).next_to(vaxes.x_axis, DOWN, buff=0.08),
            self.txt("v (m/s)", 16).rotate(PI / 2).next_to(vaxes.y_axis, LEFT, buff=0.12),
        )
        vlabel = self.math(r"v=1.5\,\mathrm{m/s}", 24).next_to(vaxes.c2p(2.5, 1.5), UP, buff=0.06)

        self.play(FadeIn(left_panel), FadeIn(left_title), FadeIn(slope), run_time=RUN)
        self.play(Create(track), FadeIn(ticks), FadeIn(cartg), FadeIn(equal_note), run_time=RUN)
        self.play(Create(xaxes), FadeIn(xtitle), FadeIn(xlabs), run_time=RUN)
        self.play(Create(xgraph), FadeIn(p0), FadeIn(p1), Create(dtx), Create(dxx), run_time=RUN)
        self.play(Create(vaxes), FadeIn(vtitle), FadeIn(vlabs), run_time=RUN)
        self.play(Create(vgraph), FadeIn(vlabel), run_time=RUN)
        self.play(FadeIn(read), run_time=RUN)
        self.play(cartg.animate.shift(RIGHT * 3.0), run_time=2.3, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S EXPERIMENT: INCLINED RAMP, WATER CLOCK, AND POSITION MARKS",
            "Release from the same point, compare equal time intervals, and record the ball's position along the ramp.",
        )

        start = np.array([-6.05, -1.75, 0.0])
        end = np.array([1.45, 1.18, 0.0])
        ramp = Line(start, end, color=BLACK, stroke_width=5)
        floor = Line(np.array([-6.45, -1.75, 0.0]), np.array([1.90, -1.75, 0.0]), color=BLACK, stroke_width=2)
        support = Line(end, np.array([1.45, -1.75, 0.0]), color=MID_GRAY, stroke_width=2)
        ref = DashedLine(start, start + RIGHT * 2.0, color=LIGHT_GRAY, stroke_width=1.4)
        theta = Angle(ref, ramp, radius=0.48, color=BLACK, stroke_width=1.8)
        tlab = self.math(r"\theta", 26).next_to(theta, UR, buff=0.03)
        ball = Circle(radius=0.18, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(end)
        release = self.txt("same release point", 18, BOLD).next_to(ball, UP + LEFT, buff=0.16)

        direction = (start - end) / np.linalg.norm(start - end)
        normal = np.array([-direction[1], direction[0], 0.0])
        us = [0.0, 1 / 16, 4 / 16, 9 / 16, 1.0]
        points = [end + u * (start - end) for u in us]
        marks = VGroup()
        labels = VGroup()
        for i, p in enumerate(points):
            marks.add(Line(p - normal * 0.10, p + normal * 0.10, color=MID_GRAY, stroke_width=1.6))
            lab = self.txt(f"t={i}", 18, color=DARK_GRAY)
            lab.move_to(p - normal * 0.34 + direction * 0.04)
            labels.add(lab)

        panel = self.panel(3.55, 5.20, fill=WHITE).move_to(RIGHT * 5.05 + DOWN * 0.25)
        ptitle = self.txt("MEASUREMENT CYCLE", 21, BOLD).next_to(panel.get_top(), DOWN, buff=0.22)
        steps = VGroup(
            self.txt("1. same starting point", 17),
            self.txt("2. release — do not push", 17),
            self.txt("3. compare equal times", 17),
            self.txt("4. mark each position", 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        steps.next_to(ptitle, DOWN, buff=0.17).align_to(ptitle, LEFT)
        divider = Line(panel.get_left() + RIGHT * 0.28, panel.get_right() + LEFT * 0.28, color=LIGHT_GRAY, stroke_width=1.4)
        divider.move_to(panel.get_center() + DOWN * 0.12)

        ctitle = self.txt("WATER CLOCK", 20, BOLD).next_to(divider, DOWN, buff=0.14)
        tank = RoundedRectangle(
            width=1.05, height=0.90, corner_radius=0.08,
            stroke_color=BLACK, stroke_width=1.7, fill_color=WHITE, fill_opacity=1,
        ).next_to(ctitle, DOWN, buff=0.10)
        water = Rectangle(width=0.88, height=0.37, stroke_width=0, fill_color=LIGHT_GRAY, fill_opacity=1)
        water.move_to(tank).align_to(tank, DOWN).shift(UP * 0.06)
        nozzle = Line(tank.get_bottom(), tank.get_bottom() + DOWN * 0.16, color=BLACK, stroke_width=1.7)
        drop = Dot(nozzle.get_end() + DOWN * 0.09, radius=0.032, color=BLACK)
        collector = RoundedRectangle(
            width=1.0, height=0.30, corner_radius=0.05,
            stroke_color=BLACK, stroke_width=1.5, fill_color=WHITE, fill_opacity=1,
        ).next_to(drop, DOWN, buff=0.06)
        cnote = self.txt("equal water volume = equal time", 14, BOLD, color=DARK_GRAY)
        cnote.move_to(panel.get_bottom() + UP * 0.27)
        clock_body = VGroup(ctitle, tank, water, nozzle, drop, collector)
        clock_body.shift(UP * 0.13)
        instrument = VGroup(panel, ptitle, steps, divider, clock_body, cnote)

        ramp_note = self.formula_panel(
            r"\text{compare positions at }t=0,1,2,3,4",
            width=6.7, height=0.78, size=27,
        ).move_to(LEFT * 2.15 + DOWN * 3.00)

        self.play(Create(ramp), Create(floor), Create(support), run_time=RUN)
        self.play(Create(ref), Create(theta), FadeIn(tlab), run_time=RUN_FAST)
        self.play(FadeIn(ball), FadeIn(release), FadeIn(marks), FadeIn(labels), run_time=RUN)
        self.play(FadeIn(instrument), FadeIn(ramp_note), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(MoveAlongPath(ball, Line(end, start)), run_time=2.8, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_equal_time_pattern_v5(self):
        self.set_header(
            6,
            "EQUAL TIMES, BUT THE DISTANCES GET LARGER",
            "Positions 0, 1, 4, 9, 16 produce successive interval distances 1, 3, 5, 7.",
        )

        data = self.note_panel(
            "RECORDED POSITIONS",
            [
                "time t:       0    1    2    3    4",
                "position x:  0    1    4    9   16",
            ],
            width=5.7, title_size=22, body_size=19,
        ).move_to(LEFT * 4.15 + UP * 1.75)
        intervals = self.formula_panel(
            r"\text{successive intervals: }1,3,5,7",
            width=5.8, height=0.90, size=30,
        ).move_to(RIGHT * 3.35 + UP * 1.75)

        baseline_y = -0.25
        xs = [-5.40, -4.72, -2.68, 0.72, 5.40]
        baseline = Line([xs[0] - 0.25, baseline_y, 0], [xs[-1] + 0.25, baseline_y, 0], color=BLACK, stroke_width=4)
        balls = VGroup()
        tlabs = VGroup()
        segments = VGroup()
        ilabs = VGroup()
        vals = [1, 3, 5, 7]
        for i, x in enumerate(xs):
            balls.add(Circle(radius=0.15, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to([x, baseline_y + 0.23, 0]))
            tlabs.add(self.txt(f"t={i}", 18).move_to([x, baseline_y - 0.50, 0]))
            if i < 4:
                seg = Line([xs[i] + 0.18, baseline_y + 0.58, 0], [xs[i + 1] - 0.18, baseline_y + 0.58, 0], color=MID_GRAY, stroke_width=2.0)
                segments.add(seg)
                ilabs.add(self.math(fr"{vals[i]}", 27).next_to(seg, UP, buff=0.04))

        compare_box = self.panel(8.4, 1.60, fill=WHITE).move_to(RIGHT * 1.65 + DOWN * 2.55)
        compare = VGroup(
            self.txt("COMPARE THE TWO PATTERNS", 20, BOLD),
            self.txt("Uniform motion: equal times -> equal distances", 17),
            self.txt("Galileo ramp: equal times -> increasing distances", 17),
            self.txt("Therefore x = x_i + vt does NOT describe the ramp motion.", 17, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        compare.move_to(compare_box).align_to(compare_box, LEFT).shift(RIGHT * 0.28)

        self.play(FadeIn(data), FadeIn(intervals), run_time=RUN)
        self.play(Create(baseline), run_time=RUN_FAST)
        for i in range(5):
            self.play(FadeIn(balls[i]), FadeIn(tlabs[i]), run_time=0.32)
            if i < 4:
                self.play(Create(segments[i]), FadeIn(ilabs[i]), run_time=0.32)
        self.play(FadeIn(compare_box), FadeIn(compare), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(
            8,
            "INTRODUCTION TO FALLING MOTION",
            "The inclined plane makes the square-time pattern measurable; vertical fall shows the same qualitative behavior much faster.",
        )

        left_panel = self.panel(5.15, 4.70, fill=WHITE).move_to(LEFT * 4.20 + DOWN * 0.10)
        observation = self.txt("equal times -> increasingly larger distances", 19, BOLD)
        self.fit(observation, 4.45, 0.38)
        observation.move_to(left_panel.get_top() + DOWN * 0.38)
        line = Line(LEFT * 4.95 + UP * 1.10, LEFT * 4.95 + DOWN * 1.60, color=BLACK, stroke_width=3)
        ys = [1.10, 0.62, -0.25, -1.57]
        balls = VGroup()
        labs = VGroup()
        for i, y in enumerate(ys):
            b = Circle(radius=0.15, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 4.95 + UP * y)
            balls.add(b)
            labs.add(self.txt(f"t={i}", 18, color=DARK_GRAY).next_to(b, RIGHT, buff=0.22))

        eq1 = self.formula_panel(r"\boxed{y=y_i-\frac12gt^2}", width=5.8, height=1.05, size=42).move_to(RIGHT * 3.55 + UP * 1.45)
        eq2 = self.formula_panel(r"y=y_i+v_it-\frac12gt^2", width=6.0, height=1.05, size=39).next_to(eq1, DOWN, buff=0.28)
        note = self.note_panel(
            "TODAY'S LIMIT",
            [
                "We introduce the equation, but do not derive g yet.",
                "For now, focus on the t² position pattern.",
                "Changing velocity is developed in the next lesson.",
            ],
            width=6.1, title_size=22, body_size=19,
        ).move_to(RIGHT * 3.55 + DOWN * 2.00)

        self.play(FadeIn(left_panel), Create(line), FadeIn(observation), run_time=RUN)
        for b, lab in zip(balls, labs):
            self.play(FadeIn(b), FadeIn(lab), run_time=0.38)
        self.play(FadeIn(eq1), FadeIn(eq2), run_time=RUN)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview:
# manim -pql Physics9_UniformMotion_Galileo_V5_2_FINAL_QA.py Physics9UniformMotionGalileoV52FinalQA --disable_caching
# Final:
# manim -pqh Physics9_UniformMotion_Galileo_V5_2_FINAL_QA.py Physics9UniformMotionGalileoV52FinalQA --disable_caching
