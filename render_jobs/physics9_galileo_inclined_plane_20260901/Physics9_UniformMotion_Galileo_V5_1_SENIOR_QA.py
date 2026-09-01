#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Uniform Motion + Galileo V5.1 · Senior visual-QA correction.

This scene inherits the validated V5 pedagogical sequence and corrects every
layout defect found by a 1-second full-timeline visual review of the PQH render:
- long section headers clipped at the right edge,
- x-t slope panel colliding with the v-t title/axes,
- Galileo comparison captions merging across the center gutter,
- water-clock and measurement-cycle panels overlapping,
- Galileo t^2 graph and explanatory note competing for the same area,
- several small explanatory elements that were readable only on desktop.

No formal acceleration lesson is added. The scope stays:
uniform-motion graphs -> x=x_i+vt -> Galileo experiment -> x proportional t^2
-> falling-motion equation preview.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5 import (
    Physics9UniformMotionGalileoV5,
    BLACK_TEXT,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    RUN_FAST,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
)


class Physics9UniformMotionGalileoV5SeniorQAFixed(Physics9UniformMotionGalileoV5):
    """V5.1: geometry-safe, larger, non-overlapping classroom render."""

    def set_header(self, number, title, subtitle):
        """Fit every header inside the 16:9 safe area before placing subtitle."""
        if self.header_group is not None:
            self.remove(self.header_group)

        num_box = RoundedRectangle(
            width=0.70,
            height=0.50,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 21, BOLD).move_to(num_box)

        title_m = self.txt(title, 26, BOLD)
        self.fit(title_m, 12.95, 0.46)
        row = VGroup(VGroup(num_box, num), title_m).arrange(RIGHT, buff=0.20)
        self.fit(row, 14.45, 0.54)
        row.to_edge(UP, buff=0.16).align_to(LEFT * 7.25, LEFT)

        subtitle_m = self.txt(subtitle, 18, color=DARK_GRAY)
        self.fit(subtitle_m, 13.85, 0.47)
        subtitle_m.next_to(row, DOWN, buff=0.08).align_to(row, LEFT)

        rule = Line(LEFT * 7.30, RIGHT * 7.30, color=LIGHT_GRAY, stroke_width=1.5)
        rule.next_to(subtitle_m, DOWN, buff=0.08)

        self.header_group = VGroup(row, subtitle_m, rule)
        self.add(self.header_group)

    def uniform_motion_two_graphs(self):
        self.set_header(
            1,
            "ONE UNIFORM MOTION, TWO GRAPHS",
            "A straight position-time line and a horizontal velocity-time line describe the same constant-velocity motion.",
        )

        left_panel = self.panel(5.35, 4.55, fill=WHITE).move_to(LEFT * 4.15 + UP * 0.15)
        left_title = self.txt("PHYSICAL MOTION", 22, BOLD).next_to(left_panel.get_top(), DOWN, buff=0.22)
        track = Line(LEFT * 6.15 + DOWN * 0.25, LEFT * 2.20 + DOWN * 0.25, color=BLACK, stroke_width=4)
        ticks = VGroup(*[
            Line([-5.75 + i * 0.82, -0.42, 0], [-5.75 + i * 0.82, -0.08, 0], color=MID_GRAY, stroke_width=1.4)
            for i in range(5)
        ])
        cart = RoundedRectangle(
            width=0.88, height=0.46, corner_radius=0.08,
            stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1,
        ).move_to(LEFT * 5.70 + UP * 0.10)
        wheel1 = Circle(radius=0.075, color=BLACK).move_to(cart.get_bottom() + DOWN * 0.02 + LEFT * 0.22)
        wheel2 = Circle(radius=0.075, color=BLACK).move_to(cart.get_bottom() + DOWN * 0.02 + RIGHT * 0.22)
        cartg = VGroup(cart, wheel1, wheel2)
        equal_note = self.txt("equal distance every second", 19, BOLD, color=DARK_GRAY).next_to(track, DOWN, buff=0.18)

        read = VGroup(
            self.txt("READ BOTH GRAPHS", 21, BOLD),
            self.txt("x-t: straight line -> constant slope", 18),
            self.txt("v-t: horizontal line -> constant velocity", 18),
            self.txt("Both represent the SAME motion.", 18, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        read.move_to(left_panel.get_center() + DOWN * 1.33).align_to(left_panel, LEFT).shift(RIGHT * 0.34)

        slope = self.formula_panel(
            r"v=\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",
            width=4.45, height=0.80, size=29,
        ).move_to(left_panel.get_center() + UP * 1.30)

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
        slope_label = self.math(r"\text{slope}=v", 24).next_to(xaxes, DOWN, buff=0.12)

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
        self.play(Create(xgraph), FadeIn(p0), FadeIn(p1), Create(dtx), Create(dxx), FadeIn(slope_label), run_time=RUN)
        self.play(Create(vaxes), FadeIn(vtitle), FadeIn(vlabs), run_time=RUN)
        self.play(Create(vgraph), FadeIn(vlabel), run_time=RUN)
        self.play(FadeIn(read), run_time=RUN)
        self.play(cartg.animate.shift(RIGHT * 3.0), run_time=2.3, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def derive_position_equation(self):
        self.set_header(
            2,
            "BUILD x = x_i + vt FROM THE DEFINITION OF VELOCITY",
            "Use the measured position change, substitute x - x_i, then isolate the final position one operation at a time.",
        )

        measured = self.note_panel(
            "MEASURED QUANTITIES",
            [
                "initial position: x_i",
                "final position: x",
                "elapsed time: t",
                "constant velocity: v",
            ],
            width=4.6, title_size=23, body_size=20,
        ).move_to(LEFT * 4.7 + UP * 0.15)

        eq1 = self.math(r"v=\frac{\Delta x}{\Delta t}", 50)
        eq2 = self.math(r"v=\frac{x-x_i}{t}", 50)
        eq3 = self.math(r"vt=x-x_i", 50)
        eq4 = self.math(r"\boxed{x=x_i+vt}", 56)
        VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.42).move_to(RIGHT * 2.35 + UP * 0.18)

        labels = VGroup(
            self.txt("1 · definition", 18, BOLD, color=DARK_GRAY).next_to(eq1, LEFT, buff=0.42),
            self.txt("2 · substitute Δx", 18, BOLD, color=DARK_GRAY).next_to(eq2, LEFT, buff=0.42),
            self.txt("3 · multiply by t", 18, BOLD, color=DARK_GRAY).next_to(eq3, LEFT, buff=0.42),
            self.txt("4 · isolate x", 18, BOLD, color=DARK_GRAY).next_to(eq4, LEFT, buff=0.42),
        )

        meaning = self.formula_panel(
            r"\text{final position}=\text{initial position}+\text{distance added}",
            width=9.6, height=0.88, size=28,
        ).to_edge(DOWN, buff=0.34)

        self.play(FadeIn(measured), run_time=RUN)
        self.play(Write(eq1), FadeIn(labels[0]), run_time=RUN)
        self.play(TransformMatchingTex(eq1.copy(), eq2), FadeIn(labels[1]), run_time=RUN)
        self.play(TransformMatchingTex(eq2.copy(), eq3), FadeIn(labels[2]), run_time=RUN)
        self.play(TransformMatchingTex(eq3.copy(), eq4), FadeIn(labels[3]), run_time=RUN)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def galileo_question_v5(self):
        self.set_header(
            4,
            "GALILEO'S QUESTION: WHAT IF EQUAL TIMES DO NOT GIVE EQUAL DISTANCES?",
            "Free fall changes too quickly for easy measurement; a shallow incline makes the changing-motion pattern observable.",
        )

        left = self.panel(6.05, 4.35, fill=WHITE).move_to(LEFT * 3.65 + DOWN * 0.20)
        right = self.panel(6.05, 4.35, fill=WHITE).move_to(RIGHT * 3.65 + DOWN * 0.20)
        ltitle = self.txt("VERTICAL FALL", 24, BOLD).next_to(left.get_top(), DOWN, buff=0.25)
        rtitle = self.txt("GALILEO'S INCLINED PLANE", 23, BOLD).next_to(right.get_top(), DOWN, buff=0.25)

        fall_line = Line(LEFT * 4.75 + UP * 0.95, LEFT * 4.75 + DOWN * 0.95, color=BLACK, stroke_width=3)
        ball1 = Circle(radius=0.17, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(fall_line.get_start())
        lnote = self.txt("too fast for precise position records", 18, BOLD, color=DARK_GRAY)
        lnote.move_to(left.get_bottom() + UP * 0.55)

        ramp = Line(RIGHT * 2.05 + DOWN * 0.75, RIGHT * 5.05 + UP * 0.85, color=BLACK, stroke_width=4)
        floor = Line(RIGHT * 1.70 + DOWN * 0.75, RIGHT * 5.45 + DOWN * 0.75, color=BLACK, stroke_width=2)
        ball2 = Circle(radius=0.17, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(ramp.get_end() + UP * 0.17)
        rnote = self.txt("slower motion -> measurable positions", 18, BOLD, color=DARK_GRAY)
        rnote.move_to(right.get_bottom() + UP * 0.55)

        q = self.formula_panel(
            r"\text{At equal times, how do the traveled distances change?}",
            width=9.4, height=0.90, size=31,
        ).to_edge(DOWN, buff=0.32)

        self.play(FadeIn(left), FadeIn(ltitle), Create(fall_line), FadeIn(ball1), FadeIn(lnote), run_time=RUN)
        self.play(FadeIn(right), FadeIn(rtitle), Create(ramp), Create(floor), FadeIn(ball2), FadeIn(rnote), run_time=RUN)
        self.play(FadeIn(q), run_time=RUN)
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
            label = self.txt(f"t={i}", 18, color=DARK_GRAY)
            label.move_to(p - normal * 0.34 + direction * 0.04)
            labels.add(label)

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
        divider.move_to(panel.get_center() + DOWN * 0.15)

        ctitle = self.txt("WATER CLOCK", 20, BOLD).next_to(divider, DOWN, buff=0.17)
        tank = RoundedRectangle(
            width=1.05, height=0.95, corner_radius=0.08,
            stroke_color=BLACK, stroke_width=1.7, fill_color=WHITE, fill_opacity=1,
        ).next_to(ctitle, DOWN, buff=0.14)
        water = Rectangle(width=0.88, height=0.40, stroke_width=0, fill_color=LIGHT_GRAY, fill_opacity=1)
        water.move_to(tank).align_to(tank, DOWN).shift(UP * 0.06)
        nozzle = Line(tank.get_bottom(), tank.get_bottom() + DOWN * 0.19, color=BLACK, stroke_width=1.7)
        drop = Dot(nozzle.get_end() + DOWN * 0.11, radius=0.035, color=BLACK)
        collector = RoundedRectangle(
            width=1.0, height=0.32, corner_radius=0.05,
            stroke_color=BLACK, stroke_width=1.5, fill_color=WHITE, fill_opacity=1,
        ).next_to(drop, DOWN, buff=0.08)
        cnote = self.txt("equal water volume = equal time", 16, BOLD, color=DARK_GRAY)
        cnote.next_to(collector, DOWN, buff=0.12)
        instrument = VGroup(panel, ptitle, steps, divider, ctitle, tank, water, nozzle, drop, collector, cnote)

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

        table = Table(
            [["0", "0"], ["1", "1"], ["2", "4"], ["3", "9"], ["4", "16"]],
            col_labels=[self.txt("time", 19, BOLD), self.txt("position", 19, BOLD)],
            include_outer_lines=True,
            line_config={"stroke_width": 1.25, "color": MID_GRAY},
            element_to_mobject_config={"font_size": 19, "color": BLACK},
        ).scale(0.90).move_to(LEFT * 4.85 + UP * 1.75)

        p1 = self.formula_panel(r"\text{positions: }0,1,4,9,16", width=5.55, height=0.88, size=30)
        p1.move_to(RIGHT * 3.25 + UP * 2.05)
        p2 = self.formula_panel(r"\text{intervals: }1,3,5,7", width=4.75, height=0.88, size=31)
        p2.next_to(p1, DOWN, buff=0.18)

        baseline = Line(LEFT * 5.45 + DOWN * 0.45, RIGHT * 5.35 + DOWN * 0.45, color=BLACK, stroke_width=4)
        xs = [-5.05, -4.40, -2.50, 0.60, 4.90]
        balls = VGroup()
        tlabs = VGroup()
        arrows = VGroup()
        ilabs = VGroup()
        vals = [1, 3, 5, 7]
        for i, x in enumerate(xs):
            balls.add(Circle(radius=0.15, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to([x, -0.20, 0]))
            tlabs.add(self.txt(f"t={i}", 18).move_to([x, -0.88, 0]))
            if i < 4:
                arr = DoubleArrow([xs[i] + 0.18, 0.18, 0], [xs[i + 1] - 0.18, 0.18, 0], color=MID_GRAY, stroke_width=1.7, buff=0)
                arrows.add(arr)
                ilabs.add(self.math(fr"{vals[i]}", 28).next_to(arr, UP, buff=0.04))

        compare = VGroup(
            self.txt("COMPARE THE TWO PATTERNS", 21, BOLD),
            self.txt("Uniform motion: equal times -> equal distances", 18),
            self.txt("Galileo ramp: equal times -> increasing distances", 18),
            self.txt("Therefore x = x_i + vt does NOT describe the ramp motion.", 18, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        compare_box = self.panel(7.5, 1.72, fill=WHITE).move_to(RIGHT * 2.15 + DOWN * 2.55)
        compare.move_to(compare_box).align_to(compare_box, LEFT).shift(RIGHT * 0.28)

        self.play(FadeIn(table), FadeIn(p1), FadeIn(p2), run_time=RUN)
        self.play(Create(baseline), run_time=RUN_FAST)
        for i in range(5):
            self.play(FadeIn(balls[i]), FadeIn(tlabs[i]), run_time=0.33)
            if i < 4:
                self.play(Create(arrows[i]), FadeIn(ilabs[i]), run_time=0.33)
        self.play(FadeIn(compare_box), FadeIn(compare), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_deduction_v5(self):
        self.set_header(
            7,
            "DEDUCE THE NEW PATTERN: POSITION IS PROPORTIONAL TO TIME SQUARED",
            "The recorded positions are perfect squares, so the position-time relation is curved rather than linear.",
        )

        squares = VGroup(
            self.math(r"0=0^2", 38),
            self.math(r"1=1^2", 38),
            self.math(r"4=2^2", 38),
            self.math(r"9=3^2", 38),
            self.math(r"16=4^2", 38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).move_to(LEFT * 5.1 + DOWN * 0.10)

        law = self.formula_panel(r"\boxed{x\propto t^2}", width=4.1, height=0.96, size=45)
        law.move_to(LEFT * 0.45 + UP * 2.25)

        axes = Axes(
            x_range=[0, 4.4, 1], y_range=[0, 17, 4],
            x_length=4.75, y_length=3.15,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        ).move_to(LEFT * 0.35 + DOWN * 0.85)
        curve = axes.plot(lambda t: t ** 2, x_range=[0, 4], color=BLACK, stroke_width=4)
        title = self.txt("POSITION vs TIME: curved", 20, BOLD).next_to(axes, UP, buff=0.12)
        ax_labs = VGroup(
            self.txt("t", 16).next_to(axes.x_axis, DOWN, buff=0.08),
            self.txt("x", 16).next_to(axes.y_axis, LEFT, buff=0.10),
        )

        contrast = self.note_panel(
            "LINEAR vs QUADRATIC",
            [
                "uniform: equal position changes -> straight line",
                "Galileo: increasing position changes -> curve",
                "the measurements reveal the t² pattern",
            ],
            width=4.65, title_size=21, body_size=18,
        ).move_to(RIGHT * 4.85 + DOWN * 0.20)

        self.play(Write(squares), run_time=RUN)
        self.play(FadeIn(law), run_time=RUN)
        self.play(Create(axes), FadeIn(title), FadeIn(ax_labs), Create(curve), run_time=RUN)
        self.play(FadeIn(contrast), run_time=RUN)
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
        observation.next_to(left_panel.get_top(), DOWN, buff=0.25)
        line = Line(LEFT * 4.95 + UP * 1.25, LEFT * 4.95 + DOWN * 1.65, color=BLACK, stroke_width=3)
        ys = [1.25, 0.78, -0.12, -1.62]
        balls = VGroup()
        labs = VGroup()
        for i, y in enumerate(ys):
            b = Circle(radius=0.15, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 4.95 + UP * y)
            balls.add(b)
            labs.add(self.txt(f"t={i}", 18, color=DARK_GRAY).next_to(b, RIGHT, buff=0.22))

        eq1 = self.formula_panel(r"\boxed{y=y_i-\frac12gt^2}", width=5.8, height=1.05, size=42)
        eq1.move_to(RIGHT * 3.55 + UP * 1.45)
        eq2 = self.formula_panel(r"y=y_i+v_it-\frac12gt^2", width=6.0, height=1.05, size=39)
        eq2.next_to(eq1, DOWN, buff=0.28)
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
# manim -pql Physics9_UniformMotion_Galileo_V5_1_SENIOR_QA.py Physics9UniformMotionGalileoV5SeniorQAFixed --disable_caching
# Final:
# manim -pqh Physics9_UniformMotion_Galileo_V5_1_SENIOR_QA.py Physics9UniformMotionGalileoV5SeniorQAFixed --disable_caching
