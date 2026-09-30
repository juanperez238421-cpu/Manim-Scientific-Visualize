#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5.8 — final visual QA for Galileo timing and LaTeX typography.

This revision inherits V5.7's proper MathTex initial-value notation and fixes
residual frame-level issues found after rendering V5.7:
- the animated ball is now on the physically correct (upper) side of the ramp;
- ramp checkpoint-number/timeline collisions are removed;
- elapsed equal-time cells highlight while the ball moves;
- the falling-motion first physical interval has more visual separation;
- physical fall markers are intentionally unlabeled because the timeline already
  carries the time labels, avoiding duplicate and cramped 0/1 labels.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_7_LATEX_INTERVAL_QA import (
    Physics9UniformMotionGalileoV57LatexIntervalQA,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    PAUSE_EXPLAIN,
)


class Physics9UniformMotionGalileoV58FinalVisualQA(Physics9UniformMotionGalileoV57LatexIntervalQA):
    """V5.8 frame-level fixes after inspecting the V5.7 PQH render."""

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S INCLINED-PLANE EXPERIMENT",
            "Historical reconstruction: equal time intervals reveal increasing distances along the shallow ramp.",
        )

        rp = self.panel(9.85, 5.25, fill=WHITE).move_to(LEFT * 2.35 + DOWN * 0.12)
        ip = self.panel(3.85, 5.25, fill=WHITE).move_to(RIGHT * 5.05 + DOWN * 0.12)

        # Ramp geometry.  The ball must sit on the upper side of the ramp.
        lower = np.array([-6.25, -0.75, 0.0])
        release_p = np.array([1.18, 1.63, 0.0])
        ramp = Line(lower, release_p, color=BLACK, stroke_width=5)
        floor = Line([-6.55, -0.75, 0], [1.55, -0.75, 0], color=BLACK, stroke_width=2)
        support = Line(release_p, [release_p[0], -0.75, 0], color=MID_GRAY, stroke_width=2)

        direction = (lower - release_p) / np.linalg.norm(lower - release_p)
        # For a down-left ramp direction, this 90-degree rotation points up-left.
        normal_up = np.array([direction[1], -direction[0], 0.0])

        # x ~ t^2 => cumulative positions 0,1,4,9,16 at equal time steps.
        pts_u = [0.0, 1 / 16, 4 / 16, 9 / 16, 1.0]
        pts = [release_p + u * (lower - release_p) + normal_up * 0.18 for u in pts_u]

        ball = Circle(
            radius=0.17,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(pts[0])

        release_label = self.txt("same release point", 19, BOLD).move_to([-0.45, 2.06, 0])
        release_leader = Arrow(
            release_label.get_bottom() + RIGHT * 0.45,
            ball.get_top(),
            buff=0.10,
            color=MID_GRAY,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.10,
        )

        # Ghost positions intentionally carry no numeric labels: the synchronized
        # timeline below already encodes 0, Δt, 2Δt, 3Δt and 4Δt.
        ghost_markers = VGroup(*[Dot(p, radius=0.050, color=MID_GRAY) for p in pts])
        marker_note = self.txt(
            "position marker after each equal time step",
            17,
            color=DARK_GRAY,
        ).move_to([-2.78, -1.19, 0])

        strip, tracker, strip_x = self._equal_time_strip(rp.get_center(), 7.25, -1.84, intervals=4)
        distance_note = self.math(
            r"\text{equal }\Delta t\;\Longrightarrow\;\Delta x_1:\Delta x_2:\Delta x_3:\Delta x_4=1:3:5:7",
            24,
        ).move_to([rp.get_center()[0], -2.42, 0])

        right_title = self.txt("HISTORICAL TIMEKEEPING", 18, BOLD).next_to(
            ip.get_top(), DOWN, buff=0.24
        )
        self.fit(right_title, 3.35, 0.40)
        clock_box = RoundedRectangle(
            width=1.35,
            height=1.00,
            corner_radius=0.08,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(ip.get_center() + UP * 0.78)
        water = Rectangle(
            width=1.15,
            height=0.40,
            stroke_width=0,
            fill_color=LIGHT_GRAY,
            fill_opacity=1,
        ).move_to(clock_box).align_to(clock_box, DOWN).shift(UP * 0.06)
        nozzle = Line(
            clock_box.get_bottom(),
            clock_box.get_bottom() + DOWN * 0.25,
            color=BLACK,
            stroke_width=1.8,
        )
        drop = Dot(nozzle.get_end() + DOWN * 0.10, radius=0.035, color=BLACK)
        cup = RoundedRectangle(
            width=1.25,
            height=0.36,
            corner_radius=0.05,
            stroke_color=BLACK,
            stroke_width=1.6,
            fill_color=WHITE,
            fill_opacity=1,
        ).next_to(drop, DOWN, buff=0.08)
        clock = VGroup(clock_box, water, nozzle, drop, cup)
        equal_water = self.formula_panel(
            r"\text{same collected water}\;\Longrightarrow\;\text{same }\Delta t",
            width=3.25,
            height=0.86,
            size=22,
        ).move_to(ip.get_center() + DOWN * 1.10)
        procedure = VGroup(
            self.txt("Release without pushing", 17, BOLD),
            self.txt("Mark position each interval", 17),
            self.txt("Repeat and compare", 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(ip.get_center() + DOWN * 2.00)
        self.fit(procedure, 3.2, 0.9)

        self.play(FadeIn(rp), FadeIn(ip), run_time=RUN)
        self.play(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(release_label), GrowArrow(release_leader), run_time=RUN)
        self.play(FadeIn(strip), FadeIn(tracker), FadeIn(marker_note), run_time=RUN)
        self.play(
            FadeIn(right_title),
            FadeIn(clock),
            FadeIn(equal_water),
            FadeIn(procedure),
            run_time=RUN,
        )

        self.add(ghost_markers[0])
        cells = strip[0]
        tracker_y = -1.48
        for i in range(1, 5):
            self.play(
                ball.animate.move_to(pts[i]),
                tracker.animate.move_to([strip_x[i], tracker_y, 0]),
                cells[i - 1].animate.set_fill(LIGHT_GRAY, opacity=0.72),
                run_time=0.92,
                rate_func=linear,
            )
            self.play(FadeIn(ghost_markers[i]), run_time=0.14)

        self.play(FadeIn(distance_note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(
            8,
            "INTRODUCTION TO FALLING MOTION",
            "One moving ball and equal time intervals: the clock steps are equal while the vertical distances grow.",
        )

        L = self.panel(6.15, 5.05, fill=WHITE).move_to(LEFT * 4.00 + DOWN * 0.10)
        lt = self.txt("ONE BALL | EQUAL TIME STEPS", 22, BOLD).next_to(
            L.get_top(), DOWN, buff=0.22
        )

        x = -4.80
        y0 = 1.55
        # Larger display scale than V5.7 so the first 1-unit gap is visually legible.
        # The exact 1:3:5 successive-distance ratio is preserved.
        u = 0.30
        ys = [y0, y0 - u, y0 - 4 * u, y0 - 9 * u]

        fall_line = Line(
            [x, y0 + 0.18, 0],
            [x, ys[-1] - 0.18, 0],
            color=BLACK,
            stroke_width=2.6,
        )
        ball = Circle(
            radius=0.095,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to([x, ys[0], 0])
        ghosts = VGroup(*[Dot([x, y, 0], radius=0.045, color=MID_GRAY) for y in ys])

        # Distances are labeled on the opposite side of the fall path; physical
        # markers are not redundantly labeled by time because the timeline does it.
        gap_arrows = VGroup()
        gap_labels = VGroup()
        for j, label in enumerate(["1", "3", "5"]):
            mid_y = (ys[j] + ys[j + 1]) / 2
            arr = DoubleArrow(
                [-5.62, ys[j] - 0.045, 0],
                [-5.62, ys[j + 1] + 0.045, 0],
                buff=0.015,
                color=MID_GRAY,
                stroke_width=1.4,
                max_tip_length_to_length_ratio=0.12,
            )
            gap_arrows.add(arr)
            gap_labels.add(self.math(label, 20).move_to([-5.93, mid_y, 0]))

        distance_caption = self.txt("successive distances", 16, color=DARK_GRAY).move_to(
            [-5.60, 1.93, 0]
        )

        strip, tracker, strip_x = self._equal_time_strip(L.get_center(), 4.45, -2.00, intervals=3)
        gap_note = self.math(
            r"\Delta y_1:\Delta y_2:\Delta y_3=1:3:5",
            24,
        ).move_to([L.get_center()[0], -2.46, 0])

        eq1 = self.formula_panel(
            r"y=y_{\mathrm{i}}-\frac12gt^2", width=6.10, height=1.12, size=44
        ).move_to(RIGHT * 3.55 + UP * 1.65)
        rel = self.txt("release from rest", 21, BOLD, color=DARK_GRAY).next_to(
            eq1, UP, buff=0.14
        )
        eq2 = self.formula_panel(
            r"y=y_{\mathrm{i}}+v_{\mathrm{i}}t-\frac12gt^2",
            width=6.35,
            height=1.12,
            size=40,
        ).next_to(eq1, DOWN, buff=0.34)
        prev = self.note_panel(
            "PREVIEW ONLY",
            [
                "Focus on the square-time pattern today.",
                "The meaning of g and changing velocity comes next.",
            ],
            width=6.35,
            title_size=24,
            body_size=20,
        ).move_to(RIGHT * 3.55 + DOWN * 1.80)

        self.play(
            FadeIn(L),
            FadeIn(lt),
            Create(fall_line),
            FadeIn(ball),
            FadeIn(distance_caption),
            run_time=RUN,
        )
        self.play(FadeIn(strip), FadeIn(tracker), run_time=RUN)
        self.add(ghosts[0])

        cells = strip[0]
        tracker_y = -1.64
        for i in range(1, 4):
            self.play(
                ball.animate.move_to([x, ys[i], 0]),
                tracker.animate.move_to([strip_x[i], tracker_y, 0]),
                cells[i - 1].animate.set_fill(LIGHT_GRAY, opacity=0.72),
                run_time=0.88,
                rate_func=linear,
            )
            self.play(FadeIn(ghosts[i]), run_time=0.14)

        self.play(FadeIn(gap_arrows), FadeIn(gap_labels), FadeIn(gap_note), run_time=RUN)
        self.play(FadeIn(rel), FadeIn(eq1), FadeIn(eq2), run_time=RUN)
        self.play(FadeIn(prev), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview: manim -pql Physics9_UniformMotion_Galileo_V5_8_FINAL_VISUAL_QA.py Physics9UniformMotionGalileoV58FinalVisualQA --disable_caching
# Final:   manim -pqh Physics9_UniformMotion_Galileo_V5_8_FINAL_VISUAL_QA.py Physics9UniformMotionGalileoV58FinalVisualQA --disable_caching
