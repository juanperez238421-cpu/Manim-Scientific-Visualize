#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Construct velocity-time graphs from the two-object x-t exercise.

Direct continuation of the approved Physics 9 two-object position-time meeting
lesson. The numerical model is intentionally unchanged:

Object A: x0 = 1 m,  v = +2 m/s,  xA = 1 + 2t
Object B: x0 = 13 m, v = -1 m/s,  xB = 13 - t
Times:    0, 1, 2, 3, 4, 5 s

Students read slope from each position-time graph and then construct the
corresponding velocity-time graph. The lesson emphasizes that a constant
slope becomes a horizontal line on a v-t graph and that meeting at the same
position does not imply equal velocity.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

from pathlib import Path
import sys
from manim import *

RENDER_ROOT = Path(__file__).resolve().parents[1]
BASE_V2_DIR = RENDER_ROOT / "physics9_two_object_meeting_xt_v2_20260831"
BASE_V1_DIR = RENDER_ROOT / "physics9_two_object_meeting_xt_20260831"
STYLE_DIR = RENDER_ROOT / "physics9_position_time_velocity_workshop_20260824"
for p in (BASE_V2_DIR, BASE_V1_DIR, STYLE_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from two_object_meeting_xt_v2 import Physics9TwoObjectMeetingXTV2  # noqa: E402
from jp_classroom_style import (  # noqa: E402
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
    PAUSE_FINAL,
)


class Physics9TwoObjectVelocityGraph(Physics9TwoObjectMeetingXTV2):
    """Build v-t graphs for the exact Object A and Object B motions."""

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()
        a = [self.position_a(t) for t in self.TIMES]
        b = [self.position_b(t) for t in self.TIMES]
        assert a == [1, 3, 5, 7, 9, 11]
        assert b == [13, 12, 11, 10, 9, 8]
        assert (a[4] - a[1]) / (self.TIMES[4] - self.TIMES[1]) == 2
        assert (b[4] - b[1]) / (self.TIMES[4] - self.TIMES[1]) == -1
        assert all(a[i + 1] - a[i] == 2 for i in range(len(a) - 1))
        assert all(b[i + 1] - b[i] == -1 for i in range(len(b) - 1))

    def construct(self) -> None:
        self.opening_velocity()
        self.recap_position_graphs()
        self.velocity_is_slope()
        self.construct_object_a_velocity()
        self.analyze_object_b_slope()
        self.construct_object_b_velocity()
        self.compare_velocity_graphs()
        self.synchronized_velocity_view()
        self.notebook_method()

    def velocity_axes(self, center=RIGHT * 2.00 + DOWN * 0.45, x_length=8.1, y_length=4.75):
        return Axes(
            x_range=[0, 5, 1], y_range=[-2, 3, 1],
            x_length=x_length, y_length=y_length, tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2, "include_numbers": False},
        ).move_to(center)

    def velocity_axis_labels(self, axes, size=22):
        tx = self.math(r"\text{time }t\;(\mathrm{s})", size)
        tx.next_to(axes.x_axis, DOWN, buff=0.23).align_to(axes.x_axis, RIGHT).shift(LEFT * 0.04)
        vv = self.math(r"\text{velocity }v\;(\mathrm{m/s})", size)
        vv.next_to(axes.y_axis, UP, buff=0.10).align_to(axes.y_axis, LEFT).shift(RIGHT * 0.06)
        return VGroup(tx, vv)

    def velocity_axis_numbers(self, axes, size=17):
        x_nums = VGroup(*[
            self.math(str(t), size).next_to(axes.c2p(t, 0), DOWN, buff=0.09)
            for t in range(0, 6)
        ])
        y_nums = VGroup(*[
            self.math(str(v), size).next_to(axes.c2p(0, v), LEFT, buff=0.10)
            for v in (-2, -1, 1, 2, 3)
        ])
        zero = self.math("0", size).next_to(axes.c2p(0, 0), DL, buff=0.08)
        return VGroup(x_nums, y_nums, zero)

    def velocity_grid(self, axes):
        lines = VGroup()
        for t in range(1, 6):
            lines.add(Line(axes.c2p(t, -2), axes.c2p(t, 3), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.58))
        for v in (-2, -1, 1, 2, 3):
            lines.add(Line(axes.c2p(0, v), axes.c2p(5, v), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.58))
        return lines

    def velocity_line_a(self, axes, width=3.8):
        return Line(axes.c2p(0, self.V_A), axes.c2p(5, self.V_A), color=BLACK_LINE, stroke_width=width)

    def velocity_line_b(self, axes, width=3.4):
        return DashedLine(
            axes.c2p(0, self.V_B), axes.c2p(5, self.V_B),
            color=DARK_GRAY, stroke_width=width, dash_length=0.12,
        )

    def velocity_dots(self, axes, which: str):
        v = self.V_A if which == "A" else self.V_B
        if which == "A":
            return VGroup(*[Dot(axes.c2p(t, v), radius=0.074, color=BLACK_LINE) for t in self.TIMES])
        return VGroup(*[
            Circle(radius=0.084, stroke_color=DARK_GRAY, stroke_width=2.2,
                   fill_color=WHITE, fill_opacity=1).move_to(axes.c2p(t, v))
            for t in self.TIMES
        ])

    def velocity_key(self):
        a_line = Line(ORIGIN, RIGHT * 0.60, color=BLACK_LINE, stroke_width=3.5)
        a = VGroup(a_line, self.text("Object A  +2 m/s", 18, BOLD)).arrange(RIGHT, buff=0.12)
        b_line = DashedLine(ORIGIN, RIGHT * 0.60, color=DARK_GRAY, stroke_width=3.2, dash_length=0.11)
        b = VGroup(b_line, self.text("Object B  -1 m/s", 18, BOLD)).arrange(RIGHT, buff=0.12)
        return VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

    def slope_triangle(self, axes, p0, p1, rise_text, run_text):
        corner = (p1[0], p0[1])
        run = Line(axes.c2p(*p0), axes.c2p(*corner), color=MID_GRAY, stroke_width=3.0)
        rise = Line(axes.c2p(*corner), axes.c2p(*p1), color=MID_GRAY, stroke_width=3.0)
        run_label = self.math(run_text, 24).next_to(run, DOWN, buff=0.10)
        rise_label = self.math(rise_text, 24).next_to(rise, RIGHT, buff=0.10)
        return VGroup(run, rise, run_label, rise_label)

    def opening_velocity(self):
        self.standard_opening(
            "PHYSICS 9 | KINEMATICS",
            "FROM POSITION GRAPH TO VELOCITY GRAPH",
            "Use the exact same two-object motion and construct v-t for each object",
            "The slope of x-t becomes the height of v-t.",
        )

    def recap_position_graphs(self):
        self.set_header(
            1, "READ THE SAME POSITION-TIME GRAPHS AGAIN",
            "Keep every value from the previous exercise. Before drawing v-t, identify what each x-t line is telling you about velocity.",
        )
        axes = self.meeting_axes(center=LEFT * 1.70 + DOWN * 0.48, x_length=9.10, y_length=4.75)
        labels = self.meeting_axis_labels(axes, 20)
        numbers = self.meeting_axis_numbers(axes, 16)
        grid = self.meeting_grid(axes)
        self.add(grid)
        self.play(Create(axes), Write(numbers), Write(labels), run_time=RUN_NORMAL)
        self.play(
            FadeIn(self.graph_line_a(axes, width=3.4)), FadeIn(self.graph_line_b(axes, width=3.1)),
            FadeIn(self.graph_dots(axes, "A")), FadeIn(self.graph_dots(axes, "B")), run_time=RUN_SLOW,
        )
        values = VGroup(
            self.card("OBJECT A", ["x: 1, 3, 5, 7, 9, 11 m", "every 1 s: +2 m"], width=4.45, height=1.45, title_size=20, body_size=16),
            self.card("OBJECT B", ["x: 13, 12, 11, 10, 9, 8 m", "every 1 s: -1 m"], width=4.45, height=1.45, title_size=20, body_size=16),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 5.10 + DOWN * 0.50)
        self.play(FadeIn(values[0]), FadeIn(values[1]), run_time=RUN_NORMAL)
        question = self.formula_chip(
            r"\text{What does the slope of each line become on a }v\!\text{-}t\text{ graph?}",
            width=9.0, size=27,
        ).move_to(DOWN * 3.35)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK + 1.0)
        self.clear_stage()

    def velocity_is_slope(self):
        self.set_header(
            2, "VELOCITY IS THE SLOPE OF A POSITION-TIME GRAPH",
            "Choose two points on the same straight x-t line. The ratio of vertical change to horizontal change is the constant velocity.",
        )
        formula = self.formula_chip(r"v=\text{slope}=\frac{\Delta x}{\Delta t}", width=5.4, size=39).move_to(UP * 1.82)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        axes = self.meeting_axes(center=LEFT * 3.55 + DOWN * 0.85, x_length=6.55, y_length=3.75)
        grid = self.meeting_grid(axes)
        numbers = self.meeting_axis_numbers(axes, 13)
        labels = self.meeting_axis_labels(axes, 16)
        self.add(grid)
        self.play(Create(axes), Write(numbers), Write(labels), FadeIn(self.graph_line_a(axes, width=3.3)), FadeIn(self.graph_dots(axes, "A")), run_time=RUN_SLOW)
        tri = self.slope_triangle(axes, (1, 3), (4, 9), r"\Delta x=+6\,\mathrm{m}", r"\Delta t=3\,\mathrm{s}")
        self.play(Create(tri[0]), Create(tri[1]), Write(tri[2]), Write(tri[3]), run_time=RUN_SLOW)
        calc = VGroup(
            self.math(r"v_A=\frac{9-3}{4-1}", 35),
            self.math(r"v_A=\frac{+6\,\mathrm{m}}{3\,\mathrm{s}}=+2\,\mathrm{m/s}", 35),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.95 + DOWN * 0.62)
        self.play(Write(calc[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(calc[1]), run_time=RUN_NORMAL)
        self.play(Create(SurroundingRectangle(calc[1], buff=0.14, color=BLACK_LINE, stroke_width=2.0)), run_time=RUN_QUICK)
        note = self.card(
            "INTERPRET THE SIGN", ["positive slope", "motion to the right", "constant +2 m/s"],
            width=4.6, height=1.55, title_size=20, body_size=17,
        ).move_to(RIGHT * 3.95 + DOWN * 2.33)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def construct_object_a_velocity(self):
        self.set_header(
            3, "CONSTRUCT OBJECT A'S VELOCITY-TIME GRAPH",
            "Object A has the same slope on every x-t interval. On v-t, plot that velocity value at every time and then connect the points.",
        )
        axes = self.velocity_axes(center=RIGHT * 1.95 + DOWN * 0.48, x_length=8.2, y_length=4.75)
        labels = self.velocity_axis_labels(axes)
        numbers = self.velocity_axis_numbers(axes)
        self.add(self.velocity_grid(axes))
        self.play(Create(axes), Write(numbers), Write(labels), run_time=RUN_SLOW)
        prompt = self.card(
            "YOUR TURN — DRAW FIRST", ["A: v = +2 m/s", "What shape should v(t) have?", "Pause and sketch it in your notebook."],
            width=4.45, height=2.00, title_size=21, body_size=17,
        ).move_to(LEFT * 4.70 + DOWN * 0.15)
        rule = self.formula_chip(r"v_A=+2\,\mathrm{m/s}\quad\text{for }0\le t\le5\,\mathrm{s}", width=5.2, size=28).move_to(LEFT * 4.70 + DOWN * 2.05)
        self.play(FadeIn(prompt), FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK + 2.0)
        dots = self.velocity_dots(axes, "A")
        for dot in dots:
            self.play(FadeIn(dot, scale=0.3), run_time=RUN_QUICK * 0.65)
        self.play(Create(self.velocity_line_a(axes)), run_time=RUN_SLOW)
        reveal = self.card(
            "OBJECT A", ["horizontal line", "above v = 0", "height = +2 m/s"],
            width=4.45, height=1.55, title_size=21, body_size=17,
        ).move_to(LEFT * 4.70 + UP * 1.35)
        self.play(FadeOut(prompt), FadeIn(reveal), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def analyze_object_b_slope(self):
        self.set_header(
            4, "ANALYZE OBJECT B'S SLOPE BEFORE DRAWING v-t",
            "A falling x-t line has negative slope. Use the same two times as before so the sign comes only from the position change.",
        )
        axes = self.meeting_axes(center=LEFT * 3.55 + DOWN * 0.80, x_length=6.55, y_length=3.75)
        self.add(self.meeting_grid(axes))
        self.play(Create(axes), Write(self.meeting_axis_numbers(axes, 13)), Write(self.meeting_axis_labels(axes, 16)), FadeIn(self.graph_line_b(axes, width=3.2)), FadeIn(self.graph_dots(axes, "B")), run_time=RUN_SLOW)
        tri = self.slope_triangle(axes, (1, 12), (4, 9), r"\Delta x=-3\,\mathrm{m}", r"\Delta t=3\,\mathrm{s}")
        self.play(Create(tri[0]), Create(tri[1]), Write(tri[2]), Write(tri[3]), run_time=RUN_SLOW)
        calc = VGroup(
            self.math(r"v_B=\frac{9-12}{4-1}", 35),
            self.math(r"v_B=\frac{-3\,\mathrm{m}}{3\,\mathrm{s}}=-1\,\mathrm{m/s}", 35),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.95 + DOWN * 0.50)
        self.play(Write(calc[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(calc[1]), run_time=RUN_NORMAL)
        self.play(Create(SurroundingRectangle(calc[1], buff=0.14, color=DARK_GRAY, stroke_width=2.0)), run_time=RUN_QUICK)
        note = self.card(
            "INTERPRET THE SIGN", ["negative slope", "motion to the left", "constant -1 m/s"],
            width=4.6, height=1.55, title_size=20, body_size=17,
        ).move_to(RIGHT * 3.95 + DOWN * 2.18)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def construct_object_b_velocity(self):
        self.set_header(
            5, "CONSTRUCT OBJECT B'S VELOCITY-TIME GRAPH",
            "The slope is -1 m/s on every interval. Plot the constant value below v = 0 and use the same dashed/hollow encoding as Object B.",
        )
        axes = self.velocity_axes(center=RIGHT * 1.95 + DOWN * 0.48, x_length=8.2, y_length=4.75)
        labels = self.velocity_axis_labels(axes)
        numbers = self.velocity_axis_numbers(axes)
        self.add(self.velocity_grid(axes))
        self.play(Create(axes), Write(numbers), Write(labels), run_time=RUN_SLOW)
        prompt = self.card(
            "YOUR TURN — DRAW FIRST", ["B: v = -1 m/s", "Which side of v = 0?", "Pause and sketch the graph."],
            width=4.45, height=2.00, title_size=21, body_size=17,
        ).move_to(LEFT * 4.70 + DOWN * 0.15)
        rule = self.formula_chip(r"v_B=-1\,\mathrm{m/s}\quad\text{for }0\le t\le5\,\mathrm{s}", width=5.2, size=28).move_to(LEFT * 4.70 + DOWN * 2.05)
        self.play(FadeIn(prompt), FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK + 2.0)
        dots = self.velocity_dots(axes, "B")
        for dot in dots:
            self.play(FadeIn(dot, scale=0.3), run_time=RUN_QUICK * 0.65)
        self.play(Create(self.velocity_line_b(axes)), run_time=RUN_SLOW)
        reveal = self.card(
            "OBJECT B", ["horizontal dashed line", "below v = 0", "height = -1 m/s"],
            width=4.45, height=1.55, title_size=21, body_size=17,
        ).move_to(LEFT * 4.70 + UP * 1.35)
        self.play(FadeOut(prompt), FadeIn(reveal), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def compare_velocity_graphs(self):
        self.set_header(
            6, "COMPARE BOTH VELOCITY GRAPHS ON THE SAME AXES",
            "The objects meet at t = 4 s and x = 9 m, but their velocities are still different. Same position does not mean same velocity.",
        )
        axes = self.velocity_axes(center=LEFT * 1.35 + DOWN * 0.45, x_length=9.5, y_length=4.75)
        self.add(self.velocity_grid(axes))
        self.play(Create(axes), Write(self.velocity_axis_numbers(axes, 16)), Write(self.velocity_axis_labels(axes, 20)), run_time=RUN_NORMAL)
        self.play(FadeIn(self.velocity_dots(axes, "A")), Create(self.velocity_line_a(axes)), run_time=RUN_SLOW)
        self.play(FadeIn(self.velocity_dots(axes, "B")), Create(self.velocity_line_b(axes)), run_time=RUN_SLOW)
        meet_t = DashedLine(axes.c2p(self.T_MEET, -2), axes.c2p(self.T_MEET, 3), color=MID_GRAY, dash_length=0.08, stroke_width=2.0)
        meet_label = self.math(r"t_{meet}=4\,\mathrm{s}", 25).next_to(meet_t, UP, buff=0.10)
        self.play(Create(meet_t), Write(meet_label), run_time=RUN_NORMAL)
        key = self.velocity_key().move_to(RIGHT * 5.25 + UP * 1.45)
        warning = self.card(
            "IMPORTANT", ["At 4 s: same position = 9 m", "but vA = +2 m/s", "and vB = -1 m/s"],
            width=4.20, height=1.85, title_size=20, body_size=17,
        ).move_to(RIGHT * 5.05 + DOWN * 0.85)
        self.play(FadeIn(key), FadeIn(warning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def synchronized_velocity_view(self):
        self.set_header(
            7, "WATCH POSITION CHANGE WHILE VELOCITY STAYS CONSTANT",
            "As time advances, the physical objects move and the v-t markers slide horizontally. Their vertical levels never change because both velocities are constant.",
        )
        track = self.track14(width=11.7, y=1.55)
        vaxes = self.velocity_axes(center=DOWN * 1.35, x_length=9.6, y_length=3.45)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_NORMAL)
        self.add(self.velocity_grid(vaxes))
        self.play(Create(vaxes), Write(self.velocity_axis_numbers(vaxes, 13)), Write(self.velocity_axis_labels(vaxes, 17)), FadeIn(self.velocity_line_a(vaxes, width=2.5).set_opacity(0.35)), FadeIn(self.velocity_line_b(vaxes, width=2.4).set_opacity(0.40)), run_time=RUN_SLOW)
        t = ValueTracker(0.0)
        a = always_redraw(lambda: self.walker(0.76).move_to([self.track14_x(self.position_a(t.get_value()), 11.7), 2.08, 0]))
        b = always_redraw(lambda: self.walker(0.76).flip(UP).move_to([self.track14_x(self.position_b(t.get_value()), 11.7), 2.08, 0]))
        pa = always_redraw(lambda: Dot(vaxes.c2p(t.get_value(), self.V_A), radius=0.080, color=BLACK_LINE))
        pb = always_redraw(lambda: Circle(radius=0.088, stroke_color=DARK_GRAY, stroke_width=2.1, fill_color=WHITE, fill_opacity=1).move_to(vaxes.c2p(t.get_value(), self.V_B)))
        clock = always_redraw(lambda: self.formula_chip(rf"t={t.get_value():.1f}\,\mathrm{{s}}", width=2.7, size=24).move_to(UP * 2.28))
        self.add(a, b, pa, pb, clock)
        self.play(t.animate.set_value(5.0), run_time=5.0, rate_func=linear)
        statement = self.formula_chip(
            r"x_A\text{ and }x_B\text{ change}\qquad v_A=+2\,\mathrm{m/s},\;v_B=-1\,\mathrm{m/s}\text{ do not}",
            width=9.6, size=25,
        ).move_to(DOWN * 3.47)
        self.play(FadeIn(statement), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def notebook_method(self):
        self.set_header(
            8, "NOTEBOOK METHOD: CONVERT x-t INTO v-t",
            "Use the same sequence for any straight segment of a position-time graph. Repeat it for every interval if the slope changes.",
        )
        cards = VGroup(
            self.card("1  CHOOSE", ["select two x-t points", "on one straight segment"], width=4.15, height=1.35, title_size=20, body_size=16),
            self.card("2  FIND Δx", ["final position - initial", "keep the sign"], width=4.15, height=1.35, title_size=20, body_size=16),
            self.card("3  FIND Δt", ["final time - initial", "Δt must be positive"], width=4.15, height=1.35, title_size=20, body_size=16),
            self.card("4  CALCULATE", ["v = Δx / Δt", "include m/s"], width=4.15, height=1.35, title_size=20, body_size=16),
            self.card("5  PLOT v", ["time on horizontal axis", "velocity on vertical axis"], width=4.15, height=1.35, title_size=20, body_size=16),
            self.card("6  REPEAT", ["new slope = new velocity", "constant slope = horizontal v"], width=4.15, height=1.35, title_size=20, body_size=16),
        )
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.32, 0.34)).move_to(UP * 0.05)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.10), run_time=RUN_SLOW * 1.7)
        final = VGroup(
            self.formula_chip(r"A:\;v_A=+2\,\mathrm{m/s}", width=4.8, size=30),
            self.formula_chip(r"B:\;v_B=-1\,\mathrm{m/s}", width=4.8, size=30),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.45)
        self.play(FadeIn(final[0]), FadeIn(final[1]), run_time=RUN_NORMAL)
        takeaway = self.formula_chip(
            r"\boxed{\text{slope of }x\!\text{-}t\;\longrightarrow\;\text{height of }v\!\text{-}t}",
            width=8.8, size=30,
        ).move_to(DOWN * 3.45)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Read the slope. Keep the sign. Build the velocity graph.")


# Preview gate:
# manim -pql physics9_two_object_velocity_graph.py Physics9TwoObjectVelocityGraph --disable_caching
# Final render:
# manim -pqh physics9_two_object_velocity_graph.py Physics9TwoObjectVelocityGraph --disable_caching
