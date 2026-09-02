#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5.7 — typography + equal-time interval visual QA.

Focus of this revision:
1. Never show LaTeX source syntax such as ``x_i`` inside normal Text objects.
   Initial-value symbols are rendered as MathTex with a true subscript:
   x_{\mathrm{i}}, y_{\mathrm{i}}, v_{\mathrm{i}}.
2. Replace the crowded Galileo/fall time labels with an explicit equal-Δt
   timeline synchronized to the moving ball.
3. Preserve the established white/black classroom style and the V5.6 content.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_6_FINAL_AUDIT import (
    Physics9UniformMotionGalileoV56FinalAudit,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)
from Physics9_UniformMotion_Galileo_V5_1_SENIOR_QA import PAUSE_WORK


class Physics9UniformMotionGalileoV57LatexIntervalQA(Physics9UniformMotionGalileoV56FinalAudit):
    """V5.7: proper mathematical subscripts and clearer equal-time motion."""

    def opening_v5(self):
        kicker = self.txt("PHYSICS 9 | KINEMATICS", 29, BOLD)
        main = self.txt("FROM MOTION GRAPHS TO GALILEO'S EXPERIMENT", 43, BOLD)
        sub = self.txt("Observe -> graph -> deduce -> test a new kind of motion", 27)
        target = self.formula_panel(
            r"x=x_{\mathrm{i}}+vt", width=5.4, height=1.18, size=55
        )
        question = self.txt(
            "Will the same rule describe a ball rolling down an inclined plane?",
            24,
            BOLD,
            color=DARK_GRAY,
        )
        group = VGroup(kicker, main, sub, target, question).arrange(DOWN, buff=0.38)
        group.move_to(ORIGIN)
        self.fit(group, 14.0, 6.7)
        self.play(FadeIn(kicker, shift=UP * 0.10), run_time=RUN)
        self.play(Write(main), run_time=RUN)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.play(FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    def derive_position_equation(self):
        self.set_header(
            2,
            "DEDUCE THE UNIFORM-MOTION POSITION EQUATION",
            "Start from velocity, replace displacement, then isolate the final position.",
        )

        measured_box = self.panel(4.45, 4.75, fill=WHITE).move_to(LEFT * 4.95 + DOWN * 0.10)
        measured_title = self.txt("WHAT WE MEASURE", 24, BOLD).next_to(
            measured_box.get_top(), DOWN, buff=0.24
        )

        symbol_specs = [
            (r"x_{\mathrm{i}}", "initial position"),
            (r"x", "final position"),
            (r"t", "elapsed time"),
            (r"v", "constant velocity"),
        ]
        symbol_rows = VGroup()
        for symbol, meaning in symbol_specs:
            sm = self.math(symbol, 32)
            desc = self.txt(meaning, 20)
            row = VGroup(sm, desc).arrange(RIGHT, buff=0.34, aligned_edge=DOWN)
            symbol_rows.add(row)
        symbol_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        symbol_rows.next_to(measured_title, DOWN, buff=0.37).align_to(measured_box, LEFT).shift(RIGHT * 0.44)

        row_y = [1.72, 0.58, -0.56, -1.70]
        labels = VGroup(
            self.txt("1  Start with velocity", 21, BOLD, color=DARK_GRAY).move_to([-1.00, row_y[0], 0]),
            self.txt("2  Replace displacement", 21, BOLD, color=DARK_GRAY).move_to([-1.00, row_y[1], 0]),
            self.txt("3  Multiply by time", 21, BOLD, color=DARK_GRAY).move_to([-1.00, row_y[2], 0]),
            self.txt("4  Isolate final position", 21, BOLD, color=DARK_GRAY).move_to([-1.00, row_y[3], 0]),
        )
        eqs = VGroup(
            self.math(r"v=\frac{\Delta x}{\Delta t}", 50).move_to([3.25, row_y[0], 0]),
            self.math(r"v=\frac{x-x_{\mathrm{i}}}{t}", 50).move_to([3.25, row_y[1], 0]),
            self.math(r"vt=x-x_{\mathrm{i}}", 50).move_to([3.25, row_y[2], 0]),
            self.math(r"x=x_{\mathrm{i}}+vt", 58).move_to([3.25, row_y[3], 0]),
        )
        arrows = VGroup(
            *[
                Arrow(
                    [3.25, row_y[i] - 0.34, 0],
                    [3.25, row_y[i + 1] + 0.34, 0],
                    buff=0.08,
                    color=MID_GRAY,
                    stroke_width=1.8,
                )
                for i in range(3)
            ]
        )
        meaning = self.formula_panel(
            r"\text{final position}=\text{initial position}+\text{distance traveled}",
            width=10.4,
            height=0.95,
            size=31,
        ).to_edge(DOWN, buff=0.30).shift(RIGHT * 0.85)

        self.play(FadeIn(measured_box), FadeIn(measured_title), FadeIn(symbol_rows), run_time=RUN)
        self.play(FadeIn(labels[0]), Write(eqs[0]), run_time=RUN)
        for i in range(1, 4):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(labels[i]), Write(eqs[i]), run_time=RUN)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def graph_equation_connection(self):
        self.set_header(
            3,
            "READ THE POSITION EQUATION FROM THE GRAPH",
            "The vertical intercept is the initial position; the slope is the constant velocity.",
        )
        box = self.panel(8.30, 5.35, fill=WHITE).move_to(LEFT * 3.30 + DOWN * 0.15)
        ax = Axes(
            x_range=[0, 4.5, 1],
            y_range=[0, 7.8, 1],
            x_length=6.55,
            y_length=3.65,
            axis_config={"color": BLACK, "stroke_width": 2, "include_tip": False},
        ).move_to(box.get_center() + DOWN * 0.20)
        gr = ax.plot(lambda t: 1 + 1.5 * t, x_range=[0, 4], color=BLACK, stroke_width=4)
        title = self.txt("POSITION vs TIME", 23, BOLD).next_to(box.get_top(), DOWN, buff=0.18)
        labs = VGroup(
            self.txt("t (s)", 18).next_to(ax.x_axis, DOWN, buff=0.10),
            self.txt("x (m)", 18).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.14),
        )
        p = Dot(ax.c2p(0, 1), radius=0.075, color=BLACK)
        ilab = self.formula_panel(
            r"x_{\mathrm{i}}=1\,\mathrm{m}", width=2.45, height=0.74, size=31
        )
        ilab.move_to(box.get_left() + RIGHT * 1.72 + UP * 1.35)
        leader = Arrow(
            ilab.get_bottom() + LEFT * 0.42,
            p.get_center() + UP * 0.05,
            buff=0.08,
            color=MID_GRAY,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.10,
        )
        tri = Polygon(
            ax.c2p(1, 2.5),
            ax.c2p(3, 2.5),
            ax.c2p(3, 5.5),
            color=MID_GRAY,
            stroke_width=2,
            fill_opacity=0,
        )
        dt = self.math(r"\Delta t=2\,\mathrm{s}", 25).move_to(ax.c2p(2, 2.12))
        dx = self.math(r"\Delta x=3\,\mathrm{m}", 25).move_to(ax.c2p(3.58, 4.0))
        slope = self.formula_panel(
            r"v=\frac{\Delta x}{\Delta t}=\frac32=1.5\,\mathrm{m/s}",
            width=5.45,
            height=1.05,
            size=31,
        ).move_to(RIGHT * 4.55 + UP * 1.85)

        map_box = self.panel(5.35, 2.55, fill=WHITE).move_to(RIGHT * 4.55 + DOWN * 0.35)
        map_title = self.txt("EQUATION MAP", 24, BOLD).next_to(map_box.get_top(), DOWN, buff=0.20)
        map_specs = [
            (r"x_{\mathrm{i}}", "vertical intercept"),
            (r"v", "slope of the line"),
            (r"t", "horizontal coordinate"),
            (r"x", "predicted position"),
        ]
        map_rows = VGroup()
        for symbol, desc_text in map_specs:
            symbol_m = self.math(symbol, 27)
            arrow_m = self.math(r"\longrightarrow", 24)
            desc_m = self.txt(desc_text, 18)
            row = VGroup(symbol_m, arrow_m, desc_m).arrange(RIGHT, buff=0.18)
            map_rows.add(row)
        map_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        map_rows.next_to(map_title, DOWN, buff=0.18).align_to(map_box, LEFT).shift(RIGHT * 0.38)

        quick = self.formula_panel(
            r"x=2+(1.2)(4)=6.8\,\mathrm{m}", width=5.35, height=0.95, size=31
        ).move_to(RIGHT * 4.55 + DOWN * 2.70)

        self.play(FadeIn(box), FadeIn(title), Create(ax), FadeIn(labs), run_time=RUN)
        self.play(Create(gr), FadeIn(p), FadeIn(ilab), GrowArrow(leader), run_time=RUN)
        self.play(Create(tri), FadeIn(dt), FadeIn(dx), run_time=RUN)
        self.play(FadeIn(slope), FadeIn(map_box), FadeIn(map_title), FadeIn(map_rows), FadeIn(quick), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def _equal_time_strip(self, center, width, y, intervals=4):
        """Horizontal timeline with equal-width Δt cells and checkpoint ticks."""
        x0 = center[0] - width / 2
        cell_w = width / intervals
        cells = VGroup()
        labels = VGroup()
        ticks = VGroup()
        tick_labels = VGroup()
        for i in range(intervals):
            rect = Rectangle(
                width=cell_w,
                height=0.48,
                stroke_color=MID_GRAY,
                stroke_width=1.4,
                fill_color=WHITE,
                fill_opacity=1,
            ).move_to([x0 + (i + 0.5) * cell_w, y, 0])
            cells.add(rect)
            labels.add(self.math(r"\Delta t", 22).move_to(rect))
        for i in range(intervals + 1):
            x = x0 + i * cell_w
            ticks.add(Line([x, y - 0.30, 0], [x, y + 0.30, 0], color=BLACK, stroke_width=1.5))
            if i == 0:
                tick_tex = r"0"
            elif i == 1:
                tick_tex = r"\Delta t"
            else:
                tick_tex = rf"{i}\Delta t"
            tick_labels.add(self.math(tick_tex, 18).move_to([x, y + 0.58, 0]))
        tracker = Dot([x0, y + 0.36, 0], radius=0.06, color=BLACK)
        return VGroup(cells, labels, ticks, tick_labels), tracker, [x0 + i * cell_w for i in range(intervals + 1)]

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S INCLINED-PLANE EXPERIMENT",
            "Historical reconstruction: equal time intervals reveal increasing distances along the shallow ramp.",
        )
        rp = self.panel(9.85, 5.25, fill=WHITE).move_to(LEFT * 2.35 + DOWN * 0.12)
        ip = self.panel(3.85, 5.25, fill=WHITE).move_to(RIGHT * 5.05 + DOWN * 0.12)

        lower = np.array([-6.25, -0.75, 0.0])
        release_p = np.array([1.18, 1.63, 0.0])
        ramp = Line(lower, release_p, color=BLACK, stroke_width=5)
        floor = Line([-6.55, -0.75, 0], [1.55, -0.75, 0], color=BLACK, stroke_width=2)
        support = Line(release_p, [release_p[0], -0.75, 0], color=MID_GRAY, stroke_width=2)

        direction = (lower - release_p) / np.linalg.norm(lower - release_p)
        normal = np.array([-direction[1], direction[0], 0.0])
        pts_u = [0.0, 1 / 16, 4 / 16, 9 / 16, 1.0]
        pts = [release_p + u * (lower - release_p) + normal * 0.17 for u in pts_u]
        ball = Circle(
            radius=0.17,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(pts[0])

        release_label = self.txt("same release point", 19, BOLD).move_to([-0.25, 2.03, 0])
        release_leader = Arrow(
            release_label.get_bottom() + RIGHT * 0.40,
            ball.get_top(),
            buff=0.10,
            color=MID_GRAY,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.10,
        )

        ghost_markers = VGroup()
        checkpoint_labels = VGroup()
        for i, p in enumerate(pts):
            ghost_markers.add(Dot(p, radius=0.045, color=MID_GRAY))
            checkpoint_labels.add(self.math(str(i), 18).move_to(p + normal * 0.31))

        strip, tracker, strip_x = self._equal_time_strip(rp.get_center(), 7.25, -1.84, intervals=4)
        distance_note = self.math(
            r"\text{equal }\Delta t\;\Longrightarrow\;\Delta x_1:\Delta x_2:\Delta x_3:\Delta x_4=1:3:5:7",
            24,
        ).move_to([rp.get_center()[0], -2.42, 0])

        right_title = self.txt("HISTORICAL TIMEKEEPING", 20, BOLD).next_to(ip.get_top(), DOWN, buff=0.22)
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
        nozzle = Line(clock_box.get_bottom(), clock_box.get_bottom() + DOWN * 0.25, color=BLACK, stroke_width=1.8)
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
        self.play(FadeIn(strip), FadeIn(tracker), run_time=RUN)
        self.play(FadeIn(right_title), FadeIn(clock), FadeIn(equal_water), FadeIn(procedure), run_time=RUN)

        self.add(ghost_markers[0], checkpoint_labels[0])
        for i in range(1, 5):
            self.play(
                ball.animate.move_to(pts[i]),
                tracker.animate.move_to([strip_x[i], -1.48, 0]),
                run_time=0.85,
                rate_func=linear,
            )
            self.play(FadeIn(ghost_markers[i]), FadeIn(checkpoint_labels[i]), run_time=0.16)
        self.play(FadeIn(distance_note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(
            8,
            "INTRODUCTION TO FALLING MOTION",
            "Use one moving ball and equal time intervals to see why successive vertical gaps grow.",
        )
        L = self.panel(6.15, 5.05, fill=WHITE).move_to(LEFT * 4.00 + DOWN * 0.10)
        lt = self.txt("ONE BALL | EQUAL TIME STEPS", 22, BOLD).next_to(L.get_top(), DOWN, buff=0.22)

        x = -4.80
        y0 = 1.48
        u = 0.27
        ys = [y0, y0 - u, y0 - 4 * u, y0 - 9 * u]
        fall_line = Line([x, y0 + 0.20, 0], [x, ys[-1] - 0.18, 0], color=BLACK, stroke_width=2.6)
        ball = Circle(
            radius=0.095,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to([x, ys[0], 0])

        ghosts = VGroup(*[Dot([x, y, 0], radius=0.043, color=MID_GRAY) for y in ys])
        checkpoint_nums = VGroup(
            *[
                self.math(str(i), 18).move_to([x + 0.42, y, 0])
                for i, y in enumerate(ys)
            ]
        )

        gap_arrows = VGroup()
        gap_labels = VGroup()
        for j, label in enumerate(["1", "3", "5"]):
            mid_y = (ys[j] + ys[j + 1]) / 2
            arr = DoubleArrow(
                [-5.62, ys[j] - 0.04, 0],
                [-5.62, ys[j + 1] + 0.04, 0],
                buff=0.02,
                color=MID_GRAY,
                stroke_width=1.4,
                max_tip_length_to_length_ratio=0.12,
            )
            gap_arrows.add(arr)
            gap_labels.add(self.math(label, 20).move_to([-5.93, mid_y, 0]))

        strip, tracker, strip_x = self._equal_time_strip(L.get_center(), 4.45, -1.84, intervals=3)
        gap_note = self.math(
            r"\Delta y_1:\Delta y_2:\Delta y_3=1:3:5",
            25,
        ).move_to([L.get_center()[0], -2.39, 0])

        eq1 = self.formula_panel(
            r"y=y_{\mathrm{i}}-\frac12gt^2", width=6.10, height=1.12, size=44
        ).move_to(RIGHT * 3.55 + UP * 1.65)
        rel = self.txt("release from rest", 21, BOLD, color=DARK_GRAY).next_to(eq1, UP, buff=0.14)
        eq2 = self.formula_panel(
            r"y=y_{\mathrm{i}}+v_{\mathrm{i}}t-\frac12gt^2", width=6.35, height=1.12, size=40
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

        self.play(FadeIn(L), FadeIn(lt), Create(fall_line), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(strip), FadeIn(tracker), run_time=RUN)
        self.add(ghosts[0], checkpoint_nums[0])
        for i in range(1, 4):
            self.play(
                ball.animate.move_to([x, ys[i], 0]),
                tracker.animate.move_to([strip_x[i], -1.48, 0]),
                run_time=0.78,
                rate_func=linear,
            )
            self.play(FadeIn(ghosts[i]), FadeIn(checkpoint_nums[i]), run_time=0.16)
        self.play(FadeIn(gap_arrows), FadeIn(gap_labels), FadeIn(gap_note), run_time=RUN)
        self.play(FadeIn(rel), FadeIn(eq1), FadeIn(eq2), run_time=RUN)
        self.play(FadeIn(prev), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview: manim -pql Physics9_UniformMotion_Galileo_V5_7_LATEX_INTERVAL_QA.py Physics9UniformMotionGalileoV57LatexIntervalQA --disable_caching
# Final:   manim -pqh Physics9_UniformMotion_Galileo_V5_7_LATEX_INTERVAL_QA.py Physics9UniformMotionGalileoV57LatexIntervalQA --disable_caching
