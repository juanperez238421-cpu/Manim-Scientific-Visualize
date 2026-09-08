#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · V5.4 · final residual frame-QA corrections.

V5.3 was rendered and manually inspected at one-second resolution. Three residual
defects remained: Galileo apparatus label collisions, square-time deduction
cross-panel overlap, and cramped t=0/t=1 labels in the falling preview.
V5.4 changes only these scenes and inherits every other V5.3 correction.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_3_TOTAL_QA import (
    Physics9UniformMotionGalileoV53TotalQA,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)


class Physics9UniformMotionGalileoV54FinalFrameQA(Physics9UniformMotionGalileoV53TotalQA):
    """Final frame-safe correction after inspecting the V5.3 PQH render."""

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S INCLINED-PLANE EXPERIMENT",
            "Historical reconstruction: same release point, water-clock timing, and repeated position measurements along a shallow ramp.",
        )

        ramp_panel = self.panel(9.45, 5.25, fill=WHITE).move_to(LEFT * 2.55 + DOWN * 0.12)
        instr_panel = self.panel(4.25, 5.25, fill=WHITE).move_to(RIGHT * 5.05 + DOWN * 0.12)

        start = np.array([-6.15, -1.35, 0.0])
        end = np.array([1.15, 1.25, 0.0])
        ramp = Line(start, end, color=BLACK, stroke_width=5)
        floor = Line([-6.45, -1.35, 0], [1.55, -1.35, 0], color=BLACK, stroke_width=2)
        support = Line(end, [1.15, -1.35, 0], color=MID_GRAY, stroke_width=2)
        ball = Circle(radius=0.18, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(end)

        release = self.txt("same release point", 19, BOLD).move_to([-0.50, 1.92, 0])
        leader = Arrow(release.get_bottom() + RIGHT * 0.55, ball.get_top(), buff=0.12, color=MID_GRAY, stroke_width=1.6, max_tip_length_to_length_ratio=0.12)

        us = [0.0, 1 / 16, 4 / 16, 9 / 16, 1.0]
        points = [end + u * (start - end) for u in us]
        markers = VGroup(*[Dot(p, radius=0.055, color=BLACK) for p in points])
        label_positions = [
            np.array([1.72, 1.05, 0.0]),
            np.array([0.30, 0.62, 0.0]),
            np.array([-0.45, -0.10, 0.0]),
            np.array([-3.05, -0.15, 0.0]),
            np.array([-5.95, -1.72, 0.0]),
        ]
        labels = VGroup(*[self.txt(f"t={i}", 19, BOLD, color=DARK_GRAY).move_to(pos) for i, pos in enumerate(label_positions)])

        ramp_caption = self.formula_panel(r"\text{record the ball position at equal time intervals}", width=7.65, height=0.88, size=29).move_to(ramp_panel.get_center() + DOWN * 2.00)

        ptitle = self.txt("HOW TIME WAS MEASURED", 22, BOLD).next_to(instr_panel.get_top(), DOWN, buff=0.22)
        steps = VGroup(
            self.txt("1  Release without pushing", 18, BOLD),
            self.txt("2  Collect water while ball moves", 18),
            self.txt("3  Compare equal water amounts", 18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.fit(steps, 3.55, 1.25)
        steps.next_to(ptitle, DOWN, buff=0.20).align_to(instr_panel, LEFT).shift(RIGHT * 0.34)

        divider = Line(instr_panel.get_left() + RIGHT * 0.30, instr_panel.get_right() + LEFT * 0.30, color=LIGHT_GRAY, stroke_width=1.5)
        divider.move_to(instr_panel.get_center() + DOWN * 0.02)

        ctitle = self.txt("WATER CLOCK", 21, BOLD).next_to(divider, DOWN, buff=0.14)
        tank = RoundedRectangle(width=1.15, height=0.82, corner_radius=0.08, stroke_color=BLACK, stroke_width=1.8, fill_color=WHITE, fill_opacity=1).next_to(ctitle, DOWN, buff=0.10)
        water = Rectangle(width=0.97, height=0.34, stroke_width=0, fill_color=LIGHT_GRAY, fill_opacity=1)
        water.move_to(tank).align_to(tank, DOWN).shift(UP * 0.055)
        nozzle = Line(tank.get_bottom(), tank.get_bottom() + DOWN * 0.15, color=BLACK, stroke_width=1.8)
        drop = Dot(nozzle.get_end() + DOWN * 0.08, radius=0.032, color=BLACK)
        collector = RoundedRectangle(width=1.10, height=0.30, corner_radius=0.05, stroke_color=BLACK, stroke_width=1.6, fill_color=WHITE, fill_opacity=1).next_to(drop, DOWN, buff=0.05)
        cnote = self.txt("equal water amount = equal time", 16, BOLD, color=DARK_GRAY)
        self.fit(cnote, 3.35, 0.32)
        cnote.move_to(instr_panel.get_bottom() + UP * 0.30)
        clock = VGroup(ctitle, tank, water, nozzle, drop, collector)
        if clock.get_bottom()[1] < cnote.get_top()[1] + 0.10:
            clock.shift(UP * (cnote.get_top()[1] + 0.14 - clock.get_bottom()[1]))

        self.play(FadeIn(ramp_panel), FadeIn(instr_panel), run_time=RUN)
        self.play(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(release), GrowArrow(leader), FadeIn(markers), FadeIn(labels), run_time=RUN)
        self.play(FadeIn(ramp_caption), run_time=RUN)
        self.play(FadeIn(ptitle), FadeIn(steps), Create(divider), run_time=RUN)
        self.play(FadeIn(clock), FadeIn(cnote), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(MoveAlongPath(ball, Line(end, start)), run_time=2.8, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_deduction_v5(self):
        self.set_header(7, "FROM THE DATA TO THE SQUARE-TIME LAW", "The position values are square numbers, so the position-time graph is curved rather than linear.")
        left = self.panel(4.70, 4.55, fill=WHITE).move_to(LEFT * 4.90 + UP * 0.05)
        right = self.panel(7.30, 4.55, fill=WHITE).move_to(RIGHT * 3.65 + UP * 0.05)
        lt = self.txt("LOOK AT THE NUMBERS", 23, BOLD).next_to(left.get_top(), DOWN, buff=0.23)
        squares = VGroup(self.math(r"1=1^2", 40), self.math(r"4=2^2", 40), self.math(r"9=3^2", 40), self.math(r"16=4^2", 40)).arrange(DOWN, buff=0.32).move_to(left.get_center() + DOWN * 0.18)
        rt = self.txt("POSITION vs TIME", 23, BOLD).next_to(right.get_top(), DOWN, buff=0.20)
        law = self.formula_panel(r"x\propto t^2", width=3.70, height=0.88, size=44).move_to(right.get_center() + UP * 1.25)
        axes = Axes(x_range=[0, 4.4, 1], y_range=[0, 17, 4], x_length=5.45, y_length=2.55, axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False}).move_to(right.get_center() + DOWN * 0.58)
        curve = axes.plot(lambda t: t ** 2, x_range=[0, 4], color=BLACK, stroke_width=4)
        ax_labs = VGroup(self.txt("t", 18).next_to(axes.x_axis, DOWN, buff=0.07), self.txt("x", 18).next_to(axes.y_axis, LEFT, buff=0.09))
        steep = self.txt("curve gets steeper as time increases", 18, BOLD, color=DARK_GRAY).move_to(right.get_bottom() + UP * 0.30)
        contrast = self.formula_panel(r"\text{uniform motion: straight line}\qquad\text{Galileo ramp: curve}", width=9.3, height=0.90, size=29).to_edge(DOWN, buff=0.27)
        self.play(FadeIn(left), FadeIn(lt), run_time=RUN)
        self.play(Write(squares), run_time=RUN)
        self.play(FadeIn(right), FadeIn(rt), FadeIn(law), run_time=RUN)
        self.play(Create(axes), FadeIn(ax_labs), Create(curve), FadeIn(steep), run_time=RUN)
        self.play(FadeIn(contrast), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(8, "INTRODUCTION TO FALLING MOTION", "The inclined plane slows the motion; vertical fall shows the same growing-distance pattern much faster.")
        left = self.panel(5.70, 5.00, fill=WHITE).move_to(LEFT * 4.15 + DOWN * 0.10)
        lt = self.txt("EQUAL TIMES -> BIGGER GAPS", 23, BOLD).next_to(left.get_top(), DOWN, buff=0.23)
        line_x = -4.95
        y0 = 1.35
        k = 0.36
        ys = [y0 - k * (i ** 2) for i in range(4)]
        line = Line([line_x, y0 + 0.18, 0], [line_x, ys[-1] - 0.18, 0], color=BLACK, stroke_width=3)
        balls = VGroup(); labs = VGroup()
        label_offsets = [UP * 0.08, DOWN * 0.10, ORIGIN, ORIGIN]
        for i, (y, off) in enumerate(zip(ys, label_offsets)):
            b = Circle(radius=0.16, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to([line_x, y, 0])
            balls.add(b)
            lab = self.txt(f"t={i}", 19, BOLD, color=DARK_GRAY).next_to(b, RIGHT, buff=0.28)
            lab.shift(off)
            labs.add(lab)
        gap_x = -5.70
        gap_labels = VGroup(self.txt("1", 19, BOLD).move_to([gap_x, (ys[0] + ys[1]) / 2, 0]), self.txt("3", 19, BOLD).move_to([gap_x, (ys[1] + ys[2]) / 2, 0]), self.txt("5", 19, BOLD).move_to([gap_x, (ys[2] + ys[3]) / 2, 0]))
        left_note = self.txt("successive gaps grow 1 : 3 : 5", 21, BOLD, color=DARK_GRAY).move_to(left.get_bottom() + UP * 0.40)
        eq1 = self.formula_panel(r"y=y_i-\frac12gt^2", width=6.1, height=1.12, size=44).move_to(RIGHT * 3.55 + UP * 1.65)
        release = self.txt("release from rest", 21, BOLD, color=DARK_GRAY).next_to(eq1, UP, buff=0.14)
        eq2 = self.formula_panel(r"y=y_i+v_it-\frac12gt^2", width=6.3, height=1.12, size=41).next_to(eq1, DOWN, buff=0.34)
        preview = self.note_panel("PREVIEW ONLY", ["The important feature today is the t² term.", "The meaning of g and changing velocity comes next."], width=6.35, title_size=24, body_size=20).move_to(RIGHT * 3.55 + DOWN * 1.80)
        self.play(FadeIn(left), FadeIn(lt), Create(line), run_time=RUN)
        for b, lab in zip(balls, labs): self.play(FadeIn(b), FadeIn(lab), run_time=0.34)
        self.play(FadeIn(gap_labels), FadeIn(left_note), run_time=RUN)
        self.play(FadeIn(release), FadeIn(eq1), FadeIn(eq2), run_time=RUN)
        self.play(FadeIn(preview), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview:
# manim -pql Physics9_UniformMotion_Galileo_V5_4_FINAL_FRAME_QA.py Physics9UniformMotionGalileoV54FinalFrameQA --disable_caching
# Final:
# manim -pqh Physics9_UniformMotion_Galileo_V5_4_FINAL_FRAME_QA.py Physics9UniformMotionGalileoV54FinalFrameQA --disable_caching
