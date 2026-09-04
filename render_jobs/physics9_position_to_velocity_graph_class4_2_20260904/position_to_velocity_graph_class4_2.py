#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Class 4-2: construct v(t) from the Class 4-1 position graph.

Exact source data retained from the audited Position-Time Graph lesson:
    (t, x) = (0,2) -> (3,8) -> (5,8) -> (7,4)
therefore the three constant interval velocities are:
    +2 m/s, 0 m/s, -2 m/s.

Pedagogical goal
----------------
Students do not receive the velocity graph immediately. The scene first rebuilds
and reads the original x-t graph, calculates each slope explicitly, gives a
student construction pause, and only then maps each slope to the corresponding
horizontal level on a v-t graph.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps, literal -pqh.
"""
from __future__ import annotations

from pathlib import Path
import sys
from manim import *

STYLE_DIR = Path(__file__).resolve().parents[1] / "physics9_position_time_velocity_workshop_20260824"
if str(STYLE_DIR) not in sys.path:
    sys.path.insert(0, str(STYLE_DIR))

from jp_classroom_style import (  # noqa: E402
    JPClassroomScene,
    BLACK_LINE,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER_GRAY,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
    PAUSE_FINAL,
)


class Physics9PositionToVelocityGraphClass42(JPClassroomScene):
    """Convert the exact Class 4-1 position-time graph into a velocity-time graph."""

    POINTS = [(0, 2), (3, 8), (5, 8), (7, 4)]
    INTERVALS = [(0, 3), (3, 5), (5, 7)]
    VELOCITIES = [2, 0, -2]

    def validate_lesson_data(self) -> None:
        slopes = [
            (self.POINTS[i + 1][1] - self.POINTS[i][1]) /
            (self.POINTS[i + 1][0] - self.POINTS[i][0])
            for i in range(3)
        ]
        assert slopes == self.VELOCITIES
        assert (8 - 2) == 6 and (3 - 0) == 3
        assert (8 - 8) == 0 and (5 - 3) == 2
        assert (4 - 8) == -4 and (7 - 5) == 2
        assert (self.POINTS[-1][1] - self.POINTS[0][1]) / 7 == 2 / 7

    def construct(self) -> None:
        self.opening()
        self.recall_position_graph()
        self.slope_to_velocity_table()
        self.student_construction_pause()
        self.build_velocity_graph()
        self.compare_both_graphs()
        self.interpret_and_check()
        self.final_method()

    # ------------------------------------------------------------------
    # Reusable visual helpers
    # ------------------------------------------------------------------
    def card(self, title, lines, width=5.2, height=1.65, title_size=24, body_size=20):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        )
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.fit(content, width - 0.42, height - 0.28)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.21)
        return VGroup(box, content)

    def formula_chip(self, expression, width=5.8, size=32):
        box = RoundedRectangle(
            width=width,
            height=0.88,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.34, 0.60)
        eq.move_to(box)
        return VGroup(box, eq)

    def xt_axes(self, center=LEFT * 3.35 + DOWN * 0.42, x_length=7.0, y_length=4.55):
        return Axes(
            x_range=[0, 7, 1],
            y_range=[0, 10, 2],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2, "include_numbers": False},
        ).move_to(center)

    def vt_axes(self, center=RIGHT * 3.55 + DOWN * 0.42, x_length=6.7, y_length=4.55):
        return Axes(
            x_range=[0, 7, 1],
            y_range=[-3, 3, 1],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2, "include_numbers": False},
        ).move_to(center)

    def axis_numbers(self, axes, x_values, y_values, size=17):
        x_nums = VGroup()
        for x in x_values:
            lab = self.math(str(x), size)
            lab.next_to(axes.c2p(x, 0), DOWN, buff=0.10)
            x_nums.add(lab)
        y_nums = VGroup()
        for y in y_values:
            lab = self.math(str(y), size)
            lab.next_to(axes.c2p(0, y), LEFT, buff=0.10)
            y_nums.add(lab)
        return VGroup(x_nums, y_nums)

    def xt_labels(self, axes, size=21):
        t = self.math(r"t\;(\mathrm{s})", size).next_to(axes.x_axis, RIGHT, buff=0.10)
        x = self.math(r"x\;(\mathrm{m})", size).next_to(axes.y_axis, UP, buff=0.08)
        return VGroup(t, x)

    def vt_labels(self, axes, size=21):
        t = self.math(r"t\;(\mathrm{s})", size).next_to(axes.x_axis, RIGHT, buff=0.10)
        v = self.math(r"v\;(\mathrm{m/s})", size).next_to(axes.y_axis, UP, buff=0.08)
        return VGroup(t, v)

    def grid(self, axes, x_values, y_values):
        lines = VGroup()
        for x in x_values:
            if x == 0:
                continue
            lines.add(
                Line(axes.c2p(x, min(y_values)), axes.c2p(x, max(y_values)), color=LIGHT_GRAY, stroke_width=1.0)
                .set_stroke(opacity=0.55)
            )
        for y in y_values:
            if y == 0:
                continue
            lines.add(
                Line(axes.c2p(0, y), axes.c2p(7, y), color=LIGHT_GRAY, stroke_width=1.0)
                .set_stroke(opacity=0.55)
            )
        return lines

    def xt_segments(self, axes, width=3.4):
        return VGroup(*[
            Line(axes.c2p(*self.POINTS[i]), axes.c2p(*self.POINTS[i + 1]), color=BLACK_LINE, stroke_width=width)
            for i in range(3)
        ])

    def xt_dots(self, axes):
        return VGroup(*[Dot(axes.c2p(*p), radius=0.08, color=BLACK_LINE) for p in self.POINTS])

    def boundary_guides(self, axes, y_min, y_max):
        return VGroup(*[
            DashedLine(
                axes.c2p(t, y_min), axes.c2p(t, y_max),
                color=MID_GRAY, dash_length=0.08, stroke_width=1.6,
            )
            for t in (3, 5)
        ])

    def interval_calc(self, index):
        p1, p2 = self.POINTS[index], self.POINTS[index + 1]
        t1, x1 = p1
        t2, x2 = p2
        dx = x2 - x1
        dt = t2 - t1
        v = self.VELOCITIES[index]
        return VGroup(
            self.math(rf"\Delta x={x2}-{x1}={dx:+d}\,\mathrm{{m}}", 29),
            self.math(rf"\Delta t={t2}-{t1}={dt}\,\mathrm{{s}}", 29),
            self.math(rf"v=\frac{{\Delta x}}{{\Delta t}}=\frac{{{dx:+d}}}{{{dt}}}={v:+d}\,\mathrm{{m/s}}", 34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.21)

    def slope_triangle(self, axes, p1, p2, dx_text, dt_text):
        t1, x1 = p1
        t2, x2 = p2
        horizontal = Line(axes.c2p(t1, x1), axes.c2p(t2, x1), color=MID_GRAY, stroke_width=2.1)
        dt = self.math(dt_text, 19).next_to(horizontal, DOWN if x2 >= x1 else UP, buff=0.05)
        if x2 == x1:
            return VGroup(horizontal, dt)
        vertical = Line(axes.c2p(t2, x1), axes.c2p(t2, x2), color=MID_GRAY, stroke_width=2.1)
        dx = self.math(dx_text, 19).next_to(vertical, RIGHT, buff=0.06)
        return VGroup(horizontal, vertical, dt, dx)

    def velocity_segments(self, axes, width=5.0):
        return VGroup(
            Line(axes.c2p(0, 2), axes.c2p(3, 2), color=BLACK_LINE, stroke_width=width),
            Line(axes.c2p(3, 0), axes.c2p(5, 0), color=BLACK_LINE, stroke_width=width),
            Line(axes.c2p(5, -2), axes.c2p(7, -2), color=BLACK_LINE, stroke_width=width),
        )

    # ------------------------------------------------------------------
    # Lesson sections
    # ------------------------------------------------------------------
    def opening(self):
        self.standard_opening(
            "PHYSICS 9 | KINEMATICS",
            "FROM POSITION GRAPH TO VELOCITY GRAPH",
            "Use the exact Class 4-1 motion to construct the matching velocity-time graph",
            "Slope on x-t becomes height on v-t.",
        )

    def recall_position_graph(self):
        self.set_header(
            1,
            "START FROM THE SAME POSITION-TIME GRAPH",
            "Do not invent new motion data. Reuse the exact four events from Class 4-1 and identify the three straight motion intervals.",
        )
        axes = self.xt_axes(center=LEFT * 2.95 + DOWN * 0.42, x_length=8.0, y_length=4.55)
        grid = self.grid(axes, range(0, 8), range(0, 11, 2))
        nums = self.axis_numbers(axes, range(0, 8), range(0, 11, 2), 17)
        labels = self.xt_labels(axes)
        graph = self.xt_segments(axes)
        dots = self.xt_dots(axes)
        coords = VGroup(
            self.math(r"(0,2)", 20).next_to(axes.c2p(0, 2), UR, buff=0.07),
            self.math(r"(3,8)", 20).next_to(axes.c2p(3, 8), UL, buff=0.07),
            self.math(r"(5,8)", 20).next_to(axes.c2p(5, 8), UR, buff=0.07),
            self.math(r"(7,4)", 20).next_to(axes.c2p(7, 4), UL, buff=0.07),
        )
        data_card = self.card(
            "EXACT MOTION DATA",
            ["(0 s, 2 m) -> (3 s, 8 m)", "-> (5 s, 8 m) -> (7 s, 4 m)"],
            width=5.35,
            height=1.65,
            title_size=24,
            body_size=20,
        ).move_to(RIGHT * 4.45 + UP * 0.80)
        interval_card = self.card(
            "THREE INTERVALS",
            ["0 to 3 s: rising", "3 to 5 s: horizontal", "5 to 7 s: falling"],
            width=5.35,
            height=2.05,
            title_size=24,
            body_size=20,
        ).move_to(RIGHT * 4.45 + DOWN * 1.25)

        self.play(Create(grid), Create(axes), Write(nums), Write(labels), run_time=RUN_SLOW)
        self.play(Create(graph), FadeIn(dots), Write(coords), run_time=RUN_SLOW)
        self.play(FadeIn(data_card, shift=LEFT * 0.10), FadeIn(interval_card, shift=LEFT * 0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def slope_to_velocity_table(self):
        self.set_header(
            2,
            "CALCULATE ONE SLOPE FOR EACH STRAIGHT SEGMENT",
            "Velocity is not read from graph height. It is the slope: change in position divided by change in time.",
        )
        formula = self.formula_chip(r"v=\text{slope}=\frac{\Delta x}{\Delta t}", width=6.3, size=35)
        formula.to_edge(UP, buff=1.28)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)

        axes = self.xt_axes(center=LEFT * 3.55 + DOWN * 0.75, x_length=7.0, y_length=4.25)
        grid = self.grid(axes, range(0, 8), range(0, 11, 2))
        nums = self.axis_numbers(axes, range(0, 8), range(0, 11, 2), 16)
        labels = self.xt_labels(axes, 20)
        base_graph = self.xt_segments(axes, width=2.0).set_stroke(opacity=0.22)
        dots = self.xt_dots(axes)
        self.play(Create(grid), Create(axes), Write(nums), Write(labels), Create(base_graph), FadeIn(dots), run_time=RUN_SLOW)

        data = [
            (0, r"\Delta x=+6\,\mathrm{m}", r"\Delta t=3\,\mathrm{s}", "+2 m/s"),
            (1, r"\Delta x=0\,\mathrm{m}", r"\Delta t=2\,\mathrm{s}", "0 m/s"),
            (2, r"\Delta x=-4\,\mathrm{m}", r"\Delta t=2\,\mathrm{s}", "-2 m/s"),
        ]
        right_center = RIGHT * 4.05 + DOWN * 0.65
        active_segment = None
        active_geom = None
        active_calc = None
        active_result = None

        for index, dx_text, dt_text, result_text in data:
            seg = Line(
                axes.c2p(*self.POINTS[index]),
                axes.c2p(*self.POINTS[index + 1]),
                color=BLACK_LINE,
                stroke_width=5.2,
            )
            geom = self.slope_triangle(axes, self.POINTS[index], self.POINTS[index + 1], dx_text, dt_text)
            calc = self.interval_calc(index).move_to(right_center + UP * 0.35)
            interval = self.math(
                rf"{self.INTERVALS[index][0]}\le t<{self.INTERVALS[index][1]}\,\mathrm{{s}}" if index < 2 else r"5\le t\le7\,\mathrm{s}",
                27,
            ).next_to(calc, UP, buff=0.28)
            result = self.card(
                f"VELOCITY LEVEL: {result_text}",
                ["This will become one horizontal", "segment on the velocity-time graph."],
                width=5.35,
                height=1.55,
                title_size=22,
                body_size=19,
            ).next_to(calc, DOWN, buff=0.35)
            group_calc = VGroup(interval, calc)

            if active_segment is not None:
                self.play(
                    FadeOut(active_segment), FadeOut(active_geom), FadeOut(active_calc), FadeOut(active_result),
                    run_time=RUN_QUICK,
                )
            self.play(Create(seg), Create(geom), FadeIn(group_calc, shift=LEFT * 0.08), run_time=RUN_SLOW)
            self.wait(PAUSE_READ)
            self.play(FadeIn(result), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN)
            active_segment, active_geom, active_calc, active_result = seg, geom, group_calc, result

        self.wait(PAUSE_WORK)
        self.clear_stage()

    def student_construction_pause(self):
        self.set_header(
            3,
            "YOUR TURN: CONSTRUCT THE VELOCITY-TIME GRAPH",
            "Before the answer appears, use the three velocities you calculated and place each one over its correct time interval.",
        )
        axes = self.vt_axes(center=DOWN * 0.40, x_length=10.8, y_length=4.70)
        grid = self.grid(axes, range(0, 8), range(-3, 4))
        nums = self.axis_numbers(axes, range(0, 8), range(-3, 4), 18)
        labels = self.vt_labels(axes, 23)
        guides = self.boundary_guides(axes, -3, 3)
        challenge = VGroup(
            self.card("INTERVAL 1", ["0 to 3 s", "v = +2 m/s"], width=3.35, height=1.35, title_size=21, body_size=19),
            self.card("INTERVAL 2", ["3 to 5 s", "v = 0 m/s"], width=3.35, height=1.35, title_size=21, body_size=19),
            self.card("INTERVAL 3", ["5 to 7 s", "v = -2 m/s"], width=3.35, height=1.35, title_size=21, body_size=19),
        ).arrange(RIGHT, buff=0.30).to_edge(DOWN, buff=0.24)
        prompt = self.text("PAUSE AND DRAW THE THREE HORIZONTAL SEGMENTS", 28, BOLD).to_edge(UP, buff=1.35)

        self.play(Create(grid), Create(axes), Write(nums), Write(labels), Create(guides), run_time=RUN_SLOW)
        self.play(FadeIn(challenge, shift=UP * 0.10), Write(prompt), run_time=RUN_SLOW)
        self.wait(6.0)
        self.clear_stage()

    def build_velocity_graph(self):
        self.set_header(
            4,
            "BUILD THE VELOCITY GRAPH ONE INTERVAL AT A TIME",
            "Each constant slope on the position graph becomes a constant height on the velocity graph over the same time interval.",
        )
        axes = self.vt_axes(center=LEFT * 2.65 + DOWN * 0.50, x_length=8.2, y_length=4.65)
        grid = self.grid(axes, range(0, 8), range(-3, 4))
        nums = self.axis_numbers(axes, range(0, 8), range(-3, 4), 17)
        labels = self.vt_labels(axes, 21)
        guides = self.boundary_guides(axes, -3, 3)
        segments = self.velocity_segments(axes)
        self.play(Create(grid), Create(axes), Write(nums), Write(labels), Create(guides), run_time=RUN_SLOW)

        cards = [
            self.card("STEP 1", ["0 to 3 s", "plot v = +2 m/s"], width=4.45, height=1.48, title_size=22, body_size=19),
            self.card("STEP 2", ["3 to 5 s", "plot v = 0 m/s"], width=4.45, height=1.48, title_size=22, body_size=19),
            self.card("STEP 3", ["5 to 7 s", "plot v = -2 m/s"], width=4.45, height=1.48, title_size=22, body_size=19),
        ]
        card_pos = RIGHT * 4.75 + DOWN * 0.15
        current = None
        for i, (segment, card) in enumerate(zip(segments, cards)):
            card.move_to(card_pos)
            if current is not None:
                self.play(FadeOut(current), run_time=RUN_QUICK)
            self.play(FadeIn(card, shift=LEFT * 0.08), Create(segment), run_time=RUN_SLOW)
            value = self.math(rf"v={self.VELOCITIES[i]:+d}\,\mathrm{{m/s}}", 30)
            value.next_to(segment, UP if self.VELOCITIES[i] >= 0 else DOWN, buff=0.10)
            self.play(Write(value), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN)
            current = VGroup(card, value)

        if current is not None:
            self.play(FadeOut(current), run_time=RUN_QUICK)
        jump_note = self.card(
            "AT t = 3 s AND t = 5 s",
            ["The idealized velocity changes instantly.", "Do not draw a vertical motion segment."],
            width=4.85,
            height=1.65,
            title_size=22,
            body_size=19,
        ).move_to(RIGHT * 4.75 + DOWN * 0.20)
        final_formula = self.formula_chip(
            r"v(t)=\begin{cases}2,&0\le t<3\\0,&3\le t<5\\-2,&5\le t\le7\end{cases}\;\mathrm{m/s}",
            width=5.15,
            size=26,
        ).next_to(jump_note, DOWN, buff=0.30)
        self.play(FadeIn(jump_note), FadeIn(final_formula), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def compare_both_graphs(self):
        self.set_header(
            5,
            "COMPARE THE TWO REPRESENTATIONS",
            "Look vertically at the same time interval: slope on x-t and height on v-t must describe the same motion.",
        )
        xt = self.xt_axes(center=LEFT * 3.65 + DOWN * 0.55, x_length=6.55, y_length=4.35)
        vt = self.vt_axes(center=RIGHT * 3.75 + DOWN * 0.55, x_length=6.35, y_length=4.35)
        xt_grid = self.grid(xt, range(0, 8), range(0, 11, 2))
        vt_grid = self.grid(vt, range(0, 8), range(-3, 4))
        xt_nums = self.axis_numbers(xt, range(0, 8), range(0, 11, 2), 15)
        vt_nums = self.axis_numbers(vt, range(0, 8), range(-3, 4), 15)
        xt_labels = self.xt_labels(xt, 19)
        vt_labels = self.vt_labels(vt, 19)
        xt_graph = self.xt_segments(xt, 3.2)
        xt_dots = self.xt_dots(xt)
        vt_segments = self.velocity_segments(vt, 4.4)
        xt_bounds = self.boundary_guides(xt, 0, 10)
        vt_bounds = self.boundary_guides(vt, -3, 3)
        title_xt = self.text("POSITION-TIME", 25, BOLD).next_to(xt, UP, buff=0.18)
        title_vt = self.text("VELOCITY-TIME", 25, BOLD).next_to(vt, UP, buff=0.18)

        self.play(
            Create(xt_grid), Create(vt_grid), Create(xt), Create(vt),
            Write(xt_nums), Write(vt_nums), Write(xt_labels), Write(vt_labels),
            Write(title_xt), Write(title_vt),
            run_time=RUN_SLOW,
        )
        self.play(Create(xt_graph), FadeIn(xt_dots), Create(vt_segments), Create(xt_bounds), Create(vt_bounds), run_time=RUN_SLOW)

        pairs = [
            (0, "RISING x-t", "v = +2 m/s"),
            (1, "HORIZONTAL x-t", "v = 0 m/s"),
            (2, "FALLING x-t", "v = -2 m/s"),
        ]
        active = None
        for i, left_text, right_text in pairs:
            xt_hi = Line(xt_graph[i].get_start(), xt_graph[i].get_end(), color=BLACK_LINE, stroke_width=6.2)
            vt_hi = Line(vt_segments[i].get_start(), vt_segments[i].get_end(), color=BLACK_LINE, stroke_width=7.0)
            bridge = self.card(
                left_text,
                ["same time interval", right_text],
                width=4.75,
                height=1.48,
                title_size=21,
                body_size=19,
            ).to_edge(DOWN, buff=0.22)
            group = VGroup(xt_hi, vt_hi, bridge)
            if active is not None:
                self.play(FadeOut(active), run_time=RUN_QUICK)
            self.play(Create(xt_hi), Create(vt_hi), FadeIn(bridge), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN)
            active = group
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def interpret_and_check(self):
        self.set_header(
            6,
            "CHECK THE PHYSICS, NOT ONLY THE DRAWING",
            "A correct velocity graph must reproduce direction, rest, and the net displacement of the original motion.",
        )
        cards = VGroup(
            self.card("0-3 s | MOVE RIGHT", ["x increases by 6 m", "v = +2 m/s"], width=4.15, height=1.58, title_size=21, body_size=19),
            self.card("3-5 s | WAIT", ["x stays at 8 m", "v = 0 m/s"], width=4.15, height=1.58, title_size=21, body_size=19),
            self.card("5-7 s | RETURN LEFT", ["x decreases by 4 m", "v = -2 m/s"], width=4.15, height=1.58, title_size=21, body_size=19),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in cards], lag_ratio=0.12), run_time=RUN_SLOW)

        check = VGroup(
            self.math(r"\Delta x=(+2)(3)+(0)(2)+(-2)(2)", 31),
            self.math(r"\Delta x=6+0-4=+2\,\mathrm{m}", 34),
            self.math(r"x_f=x_i+\Delta x=2+2=4\,\mathrm{m}", 34),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.55)
        for eq in check:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        box = SurroundingRectangle(check[-1], buff=0.14, color=BLACK_LINE, stroke_width=2.2)
        self.play(Create(box), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def final_method(self):
        self.set_header(
            7,
            "THE FIVE-STEP x-t TO v-t METHOD",
            "Use this exact sequence whenever a piecewise position-time graph is made of straight segments.",
        )
        steps = VGroup(
            self.card("1 | SPLIT", ["Mark every straight", "time interval"], width=2.65, height=1.55, title_size=21, body_size=18),
            self.card("2 | SLOPE", ["Compute", "Delta x / Delta t"], width=2.65, height=1.55, title_size=21, body_size=18),
            self.card("3 | SIGN", ["Rising +", "flat 0, falling -"], width=2.65, height=1.55, title_size=21, body_size=18),
            self.card("4 | HEIGHT", ["Plot that v level", "on the same interval"], width=2.65, height=1.55, title_size=21, body_size=18),
            self.card("5 | CHECK", ["Area under v-t", "must match Delta x"], width=2.65, height=1.55, title_size=21, body_size=18),
        ).arrange(RIGHT, buff=0.18).move_to(UP * 0.45)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in steps], lag_ratio=0.10), run_time=RUN_SLOW * 1.5)

        exact = self.formula_chip(
            r"(0,2)\rightarrow(3,8)\rightarrow(5,8)\rightarrow(7,4)\quad\Longrightarrow\quad v=+2,\;0,\;-2\;\mathrm{m/s}",
            width=11.2,
            size=30,
        ).move_to(DOWN * 1.45)
        takeaway = self.text("SLOPE ON x-t  =  HEIGHT ON v-t", 31, BOLD).next_to(exact, DOWN, buff=0.42)
        self.play(FadeIn(exact), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(Write(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Construct. Calculate. Match the interval. Verify the motion.")


# Preview:
#   manim -pql position_to_velocity_graph_class4_2.py Physics9PositionToVelocityGraphClass42 --disable_caching
# Final:
#   manim -pqh position_to_velocity_graph_class4_2.py Physics9PositionToVelocityGraphClass42 --disable_caching
