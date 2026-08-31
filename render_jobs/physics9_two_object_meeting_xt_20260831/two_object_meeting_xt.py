#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Two objects meeting on a position-time graph.

Senior classroom continuation of Physics9PositionTimeGraphConstructionV3.
The scene preserves the accepted JP white/black visual contract and the V3
construction logic, but now two objects move in opposite directions. Students
locate the meeting graphically and verify the same event with x = x0 + vt.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

from pathlib import Path
import sys
from manim import *

RENDER_ROOT = Path(__file__).resolve().parents[1]
V3_DIR = RENDER_ROOT / "physics9_position_time_graph_construction_v3_20260828"
STYLE_DIR = RENDER_ROOT / "physics9_position_time_velocity_workshop_20260824"
for p in (V3_DIR, STYLE_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from position_time_graph_construction_v3 import Physics9PositionTimeGraphConstructionV3  # noqa: E402
from jp_classroom_style import (  # noqa: E402
    BLACK_LINE,
    DARK_GRAY,
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


class Physics9TwoObjectMeetingXT(Physics9PositionTimeGraphConstructionV3):
    """Construct two x-t graphs, find their intersection, and verify algebraically."""

    TIMES = [0, 1, 2, 3, 4, 5]
    X0_A = 1
    V_A = 2
    X0_B = 13
    V_B = -1
    T_MEET = 4
    X_MEET = 9

    def validate_lesson_data(self) -> None:
        a = [self.position_a(t) for t in self.TIMES]
        b = [self.position_b(t) for t in self.TIMES]
        assert a == [1, 3, 5, 7, 9, 11]
        assert b == [13, 12, 11, 10, 9, 8]
        assert self.X0_A + self.V_A * self.T_MEET == self.X_MEET
        assert self.X0_B + self.V_B * self.T_MEET == self.X_MEET
        assert (self.X0_B - self.X0_A) / (self.V_A - self.V_B) == self.T_MEET

    def construct(self) -> None:
        self.opening()
        self.initial_motion()
        self.build_data()
        self.plot_object_a()
        self.plot_object_b()
        self.graphical_meeting()
        self.synchronized_meeting()
        self.equation_solution()
        self.compare_methods()
        self.final_method()

    # ------------------------------------------------------------------
    # Model + visual helpers
    # ------------------------------------------------------------------
    def position_a(self, t: float) -> float:
        return self.X0_A + self.V_A * float(t)

    def position_b(self, t: float) -> float:
        return self.X0_B + self.V_B * float(t)

    def track14(self, width=11.6, y=0.75):
        x0, x1 = -width / 2, width / 2
        line = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.5)
        ticks, nums = VGroup(), VGroup()
        for value in range(0, 15, 2):
            x = x0 + value / 14 * width
            ticks.add(Line([x, y - 0.09, 0], [x, y + 0.09, 0], color=BLACK_LINE, stroke_width=1.7))
            nums.add(self.math(str(value), 19).move_to([x, y - 0.28, 0]))
        label = self.math(r"x\;(\mathrm{m})", 23).next_to(line, RIGHT, buff=0.10)
        return VGroup(line, ticks, nums, label)

    def track14_x(self, position, width=11.6):
        return -width / 2 + float(position) / 14 * width

    def meeting_axes(self, center=RIGHT * 2.05 + DOWN * 0.52, x_length=8.1, y_length=4.75):
        return Axes(
            x_range=[0, 5, 1], y_range=[0, 14, 2],
            x_length=x_length, y_length=y_length, tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2, "include_numbers": False},
        ).move_to(center)

    def meeting_axis_labels(self, axes, size=22):
        tx = self.math(r"\text{time }t\;(\mathrm{s})", size)
        tx.next_to(axes.x_axis, DOWN, buff=0.27).align_to(axes.x_axis, RIGHT).shift(LEFT * 0.08)
        px = self.math(r"\text{position }x\;(\mathrm{m})", size)
        px.next_to(axes.y_axis, UP, buff=0.10).align_to(axes.y_axis, LEFT).shift(RIGHT * 0.08)
        return VGroup(tx, px)

    def meeting_axis_numbers(self, axes, size=17):
        x_nums = VGroup(*[
            self.math(str(t), size).next_to(axes.c2p(t, 0), DOWN, buff=0.10)
            for t in range(0, 6)
        ])
        y_nums = VGroup(*[
            self.math(str(x), size).next_to(axes.c2p(0, x), LEFT, buff=0.11)
            for x in range(0, 15, 2)
        ])
        return VGroup(x_nums, y_nums)

    def meeting_grid(self, axes):
        lines = VGroup()
        for t in range(1, 6):
            lines.add(Line(axes.c2p(t, 0), axes.c2p(t, 14), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.58))
        for x in range(2, 15, 2):
            lines.add(Line(axes.c2p(0, x), axes.c2p(5, x), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.58))
        return lines

    def object_points(self, which: str):
        values = [self.position_a(t) if which == "A" else self.position_b(t) for t in self.TIMES]
        return list(zip(self.TIMES, values))

    def object_table(self, which: str, scale=1.0):
        values = [self.position_a(t) if which == "A" else self.position_b(t) for t in self.TIMES]
        data = [[r"t\;(\mathrm{s})", rf"x_{which}\;(\mathrm{{m}})"]] + [[str(t), str(int(x))] for t, x in zip(self.TIMES, values)]
        rows = []
        for r, row in enumerate(data):
            cells = VGroup()
            for entry in row:
                rect = Rectangle(
                    width=1.75, height=0.49,
                    stroke_color=BLACK_LINE, stroke_width=1.4,
                    fill_color=PAPER_GRAY if r == 0 else WHITE, fill_opacity=1,
                )
                label = self.math(entry, 21 if r == 0 else 23).move_to(rect)
                cells.add(VGroup(rect, label))
            cells.arrange(RIGHT, buff=0)
            rows.append(cells)
        table = VGroup(*rows).arrange(DOWN, buff=0).scale(scale)
        return table, rows

    def graph_line_a(self, axes, width=3.6):
        pts = self.object_points("A")
        return VGroup(*[
            Line(axes.c2p(*pts[i]), axes.c2p(*pts[i + 1]), color=BLACK_LINE, stroke_width=width)
            for i in range(len(pts) - 1)
        ])

    def graph_line_b(self, axes, width=3.3):
        pts = self.object_points("B")
        return VGroup(*[
            DashedLine(
                axes.c2p(*pts[i]), axes.c2p(*pts[i + 1]),
                color=DARK_GRAY, stroke_width=width, dash_length=0.12,
            )
            for i in range(len(pts) - 1)
        ])

    def graph_dots(self, axes, which: str):
        pts = self.object_points(which)
        if which == "A":
            return VGroup(*[Dot(axes.c2p(*p), radius=0.078, color=BLACK_LINE) for p in pts])
        return VGroup(*[
            Circle(radius=0.088, stroke_color=DARK_GRAY, stroke_width=2.2, fill_color=WHITE, fill_opacity=1).move_to(axes.c2p(*p))
            for p in pts
        ])

    def object_key(self):
        a_line = Line(ORIGIN, RIGHT * 0.62, color=BLACK_LINE, stroke_width=3.5)
        a_txt = self.text("Object A", 19, BOLD)
        a = VGroup(a_line, a_txt).arrange(RIGHT, buff=0.14)
        b_line = DashedLine(ORIGIN, RIGHT * 0.62, color=DARK_GRAY, stroke_width=3.2, dash_length=0.11)
        b_txt = self.text("Object B", 19, BOLD)
        b = VGroup(b_line, b_txt).arrange(RIGHT, buff=0.14)
        return VGroup(a, b).arrange(RIGHT, buff=0.35)

    # ------------------------------------------------------------------
    # Lesson sections
    # ------------------------------------------------------------------
    def opening(self):
        self.standard_opening(
            "PHYSICS 9 | KINEMATICS",
            "WHERE DO TWO OBJECTS MEET?",
            "Construct two position-time graphs, find their intersection, then verify with x = x0 + vt",
            "Same time + same position means the objects are at the same place.",
        )

    def initial_motion(self):
        self.set_header(
            1, "READ THE PHYSICAL SITUATION",
            "Two objects start at different positions and move toward each other. Use one positive direction to assign the signs of their velocities.",
        )
        track = self.track14(width=11.6, y=0.72)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_SLOW)

        a = self.walker(1.04).move_to([self.track14_x(self.X0_A), 1.42, 0])
        b = self.walker(1.04).flip(UP).move_to([self.track14_x(self.X0_B), 1.42, 0])
        a_tag = self.text("A", 25, BOLD).next_to(a, UP, buff=0.09)
        b_tag = self.text("B", 25, BOLD).next_to(b, UP, buff=0.09)
        self.play(FadeIn(a), FadeIn(b), Write(a_tag), Write(b_tag), run_time=RUN_NORMAL)

        arrow_a = Arrow(a.get_center() + UP * 0.73, a.get_center() + RIGHT * 1.2 + UP * 0.73, buff=0.05, color=BLACK_LINE, stroke_width=3)
        arrow_b = Arrow(b.get_center() + UP * 0.73, b.get_center() + LEFT * 1.2 + UP * 0.73, buff=0.05, color=DARK_GRAY, stroke_width=3)
        self.play(GrowArrow(arrow_a), GrowArrow(arrow_b), run_time=RUN_NORMAL)

        cards = VGroup(
            self.card("OBJECT A", ["x0 = 1 m", "v = +2 m/s", "moves right"], width=4.35, height=1.72, title_size=22, body_size=18),
            self.card("OBJECT B", ["x0 = 13 m", "v = -1 m/s", "moves left"], width=4.35, height=1.72, title_size=22, body_size=18),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.62)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.16), run_time=RUN_SLOW)
        sign = self.formula_chip(r"+x\;\text{to the right}\quad\Rightarrow\quad v_A>0,\;v_B<0", width=8.4, size=28)
        sign.next_to(cards, DOWN, buff=0.30)
        self.play(FadeIn(sign), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def build_data(self):
        self.set_header(
            2, "RECORD BOTH MOTIONS AS DATA",
            "At each clock reading, record the position of A and B. These ordered pairs will become the points of the two position-time graphs.",
        )
        track = self.track14(width=11.5, y=1.45)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_NORMAL)
        table_a, rows_a = self.object_table("A", 0.94)
        table_b, rows_b = self.object_table("B", 0.94)
        table_a.move_to(LEFT * 4.55 + DOWN * 1.10)
        table_b.move_to(RIGHT * 4.55 + DOWN * 1.10)
        ta = self.text("OBJECT A DATA", 23, BOLD).next_to(table_a, UP, buff=0.16)
        tb = self.text("OBJECT B DATA", 23, BOLD).next_to(table_b, UP, buff=0.16)
        self.play(FadeIn(table_a), FadeIn(table_b), FadeIn(ta), FadeIn(tb), run_time=RUN_SLOW)

        t = ValueTracker(0)
        a = always_redraw(lambda: self.walker(0.77).move_to([self.track14_x(self.position_a(t.get_value()), 11.5), 1.96, 0]))
        b = always_redraw(lambda: self.walker(0.77).flip(UP).move_to([self.track14_x(self.position_b(t.get_value()), 11.5), 1.96, 0]))
        clock = always_redraw(lambda: self.formula_chip(rf"t={t.get_value():.0f}\,\mathrm{{s}}", width=2.5, size=25).move_to(DOWN * 1.05))
        self.add(a, b, clock)

        previous_a = previous_b = None
        for idx, time_value in enumerate(self.TIMES):
            if idx > 0:
                self.play(t.animate.set_value(time_value), run_time=0.85, rate_func=linear)
            ha = SurroundingRectangle(rows_a[idx + 1], buff=0.025, color=BLACK_LINE, stroke_width=1.8)
            hb = SurroundingRectangle(rows_b[idx + 1], buff=0.025, color=DARK_GRAY, stroke_width=1.8)
            anims = [FadeIn(ha), FadeIn(hb)]
            if previous_a is not None:
                anims += [FadeOut(previous_a), FadeOut(previous_b)]
            self.play(*anims, run_time=RUN_QUICK)
            previous_a, previous_b = ha, hb
            self.wait(PAUSE_SHORT * 0.42)

        pair = self.formula_chip(r"A:(t,x_A)\qquad B:(t,x_B)", width=5.2, size=28).move_to(DOWN * 2.87)
        self.play(FadeIn(pair), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def plot_object_a(self):
        self.set_header(
            3, "CONSTRUCT THE FIRST POSITION-TIME GRAPH",
            "Use time on the horizontal axis and position on the vertical axis. Plot every Object A row before connecting the points.",
        )
        table, rows = self.object_table("A", 0.96)
        table.move_to(LEFT * 4.92 + DOWN * 0.28)
        title = self.text("OBJECT A", 25, BOLD).next_to(table, UP, buff=0.17)
        axes = self.meeting_axes()
        labels = self.meeting_axis_labels(axes)
        numbers = self.meeting_axis_numbers(axes)
        grid = self.meeting_grid(axes)
        self.play(FadeIn(table), FadeIn(title), run_time=RUN_NORMAL)
        self.play(Create(axes.x_axis), Write(numbers[0]), Write(labels[0]), run_time=RUN_NORMAL)
        x_note = self.card("HORIZONTAL AXIS", ["time t", "seconds (s)"], width=3.0, height=1.18, title_size=18, body_size=16).move_to(RIGHT * 5.75 + DOWN * 2.60)
        self.play(FadeIn(x_note), run_time=RUN_QUICK)
        self.play(Create(axes.y_axis), Write(numbers[1]), Write(labels[1]), Create(grid), run_time=RUN_NORMAL)
        y_note = self.card("VERTICAL AXIS", ["position x", "meters (m)"], width=3.0, height=1.18, title_size=18, body_size=16).move_to(RIGHT * 5.75 + UP * 1.70)
        scale = self.card("SCALE", ["1 s horizontally", "2 m vertically"], width=3.25, height=1.22, title_size=18, body_size=16).move_to(LEFT * 4.92 + DOWN * 2.75)
        self.play(FadeIn(y_note), FadeIn(scale), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeOut(x_note), FadeOut(y_note), run_time=RUN_NORMAL)

        dots = VGroup()
        for idx, p in enumerate(self.object_points("A")):
            h = SurroundingRectangle(rows[idx + 1], buff=0.025, color=BLACK_LINE, stroke_width=1.8)
            guides = self.guides(axes, p)
            dot = Dot(axes.c2p(*p), radius=0.082, color=BLACK_LINE)
            self.play(FadeIn(h), Create(guides), run_time=RUN_QUICK)
            self.play(FadeIn(dot, scale=0.3), run_time=RUN_QUICK)
            dots.add(dot)
            self.play(FadeOut(guides), FadeOut(h), run_time=RUN_QUICK)
        self.play(LaggedStart(*[Create(seg) for seg in self.graph_line_a(axes)], lag_ratio=0.10), run_time=RUN_SLOW)
        rule = self.card("OBJECT A", ["rising line", "positive velocity", "solid graph"], width=3.55, height=1.45, title_size=19, body_size=16).move_to(LEFT * 4.85 + DOWN * 2.66)
        self.play(ReplacementTransform(scale, rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def plot_object_b(self):
        self.set_header(
            4, "ADD THE SECOND POSITION-TIME GRAPH",
            "Keep the same axes and scale. Plot Object B on the same coordinate plane so the two motions can be compared directly.",
        )
        axes = self.meeting_axes()
        labels = self.meeting_axis_labels(axes)
        numbers = self.meeting_axis_numbers(axes)
        grid = self.meeting_grid(axes)
        line_a = self.graph_line_a(axes)
        dots_a = self.graph_dots(axes, "A")
        table, rows = self.object_table("B", 0.96)
        table.move_to(LEFT * 4.92 + DOWN * 0.28)
        title = self.text("OBJECT B", 25, BOLD).next_to(table, UP, buff=0.17)
        self.add(grid)
        self.play(Create(axes), Write(numbers), Write(labels), FadeIn(line_a), FadeIn(dots_a), FadeIn(table), FadeIn(title), run_time=RUN_SLOW)

        dots_b = VGroup()
        for idx, p in enumerate(self.object_points("B")):
            h = SurroundingRectangle(rows[idx + 1], buff=0.025, color=DARK_GRAY, stroke_width=1.8)
            guides = self.guides(axes, p)
            dot = Circle(radius=0.090, stroke_color=DARK_GRAY, stroke_width=2.2, fill_color=WHITE, fill_opacity=1).move_to(axes.c2p(*p))
            self.play(FadeIn(h), Create(guides), run_time=RUN_QUICK)
            self.play(FadeIn(dot, scale=0.3), run_time=RUN_QUICK)
            dots_b.add(dot)
            self.play(FadeOut(guides), FadeOut(h), run_time=RUN_QUICK)
        self.play(LaggedStart(*[Create(seg) for seg in self.graph_line_b(axes)], lag_ratio=0.10), run_time=RUN_SLOW)
        key = self.object_key().move_to(LEFT * 4.90 + DOWN * 2.70)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def graphical_meeting(self):
        self.set_header(
            5, "FIND THE MEETING GRAPHICALLY",
            "The objects meet when both graphs have the same time and the same position. On one x-t plane, that event is the intersection point.",
        )
        axes = self.meeting_axes(center=LEFT * 1.55 + DOWN * 0.48, x_length=9.25, y_length=4.85)
        labels = self.meeting_axis_labels(axes, 21)
        numbers = self.meeting_axis_numbers(axes, 17)
        grid = self.meeting_grid(axes)
        a_line = self.graph_line_a(axes)
        b_line = self.graph_line_b(axes)
        a_dots = self.graph_dots(axes, "A")
        b_dots = self.graph_dots(axes, "B")
        self.add(grid)
        self.play(Create(axes), Write(numbers), Write(labels), FadeIn(a_line), FadeIn(b_line), FadeIn(a_dots), FadeIn(b_dots), run_time=RUN_SLOW)
        key = self.object_key().move_to(RIGHT * 5.15 + UP * 1.70)
        prompt = self.card("STUDENT CHECK", ["Where do the lines cross?", "Read time first.", "Then read position."], width=4.05, height=1.78, title_size=21, body_size=17).move_to(RIGHT * 5.05 + DOWN * 0.45)
        self.play(FadeIn(key), FadeIn(prompt), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK + 1.2)

        meet = axes.c2p(self.T_MEET, self.X_MEET)
        dot = Dot(meet, radius=0.115, color=BLACK_LINE)
        vline = DashedLine(axes.c2p(self.T_MEET, 0), meet, color=MID_GRAY, dash_length=0.08, stroke_width=2)
        hline = DashedLine(axes.c2p(0, self.X_MEET), meet, color=MID_GRAY, dash_length=0.08, stroke_width=2)
        meet_label = self.math(r"(4\,\mathrm{s},\,9\,\mathrm{m})", 27).next_to(dot, UR, buff=0.10)
        self.play(FadeOut(prompt), FadeIn(dot, scale=0.3), Create(vline), Create(hline), Write(meet_label), run_time=RUN_SLOW)
        result = self.formula_chip(r"t_{meet}=4\,\mathrm{s}\qquad x_{meet}=9\,\mathrm{m}", width=4.85, size=28).move_to(RIGHT * 5.05 + DOWN * 0.55)
        self.play(FadeIn(result), run_time=RUN_NORMAL)
        self.focus_on(VGroup(dot, meet_label, vline, hline), width=5.0, pause=PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def synchronized_meeting(self):
        self.set_header(
            6, "SAME MEETING, TWO REPRESENTATIONS",
            "Watch the physical objects approach while their graph points move at the same time. At the meeting, both physical positions and both graph points coincide.",
        )
        track = self.track14(width=11.7, y=1.55)
        graph = self.meeting_axes(center=DOWN * 1.37, x_length=9.45, y_length=3.35)
        labels = self.meeting_axis_labels(graph, 18)
        numbers = self.meeting_axis_numbers(graph, 14)
        grid = self.meeting_grid(graph)
        pale_a = self.graph_line_a(graph, width=2.4).set_opacity(0.30)
        pale_b = self.graph_line_b(graph, width=2.3).set_opacity(0.35)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_NORMAL)
        self.add(grid)
        self.play(Create(graph), Write(numbers), Write(labels), FadeIn(pale_a), FadeIn(pale_b), run_time=RUN_SLOW)

        t = ValueTracker(0.0)
        a = always_redraw(lambda: self.walker(0.76).move_to([self.track14_x(self.position_a(t.get_value()), 11.7), 2.08, 0]))
        b = always_redraw(lambda: self.walker(0.76).flip(UP).move_to([self.track14_x(self.position_b(t.get_value()), 11.7), 2.08, 0]))
        pa = always_redraw(lambda: Dot(graph.c2p(t.get_value(), self.position_a(t.get_value())), radius=0.075, color=BLACK_LINE))
        pb = always_redraw(lambda: Circle(radius=0.085, stroke_color=DARK_GRAY, stroke_width=2.0, fill_color=WHITE, fill_opacity=1).move_to(graph.c2p(t.get_value(), self.position_b(t.get_value()))))
        trace_a = TracedPath(pa.get_center, stroke_color=BLACK_LINE, stroke_width=3.2)
        trace_b = TracedPath(pb.get_center, stroke_color=DARK_GRAY, stroke_width=3.0)
        clock = always_redraw(lambda: self.formula_chip(rf"t={t.get_value():.1f}\,\mathrm{{s}}", width=2.7, size=24).move_to(UP * 2.25))
        self.add(trace_a, trace_b, a, b, pa, pb, clock)
        self.play(t.animate.set_value(self.T_MEET), run_time=4.0, rate_func=linear)
        self.wait(PAUSE_SHORT)
        meet_track = DashedLine([self.track14_x(self.X_MEET, 11.7), 1.05, 0], [self.track14_x(self.X_MEET, 11.7), 2.62, 0], color=MID_GRAY, dash_length=0.07)
        meet_graph = Dot(graph.c2p(self.T_MEET, self.X_MEET), radius=0.12, color=BLACK_LINE)
        call = self.formula_chip(r"\text{same }t=4\,\mathrm{s}\quad+\quad\text{same }x=9\,\mathrm{m}", width=6.6, size=26).move_to(DOWN * 3.45)
        self.play(Create(meet_track), FadeIn(meet_graph), FadeIn(call), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def equation_solution(self):
        self.set_header(
            7, "VERIFY WITH THE MOTION EQUATION",
            "For constant velocity, write x = x0 + vt for each object. At the meeting, both equations must produce the same position at the same time.",
        )
        formula = self.formula_chip(r"x=x_0+vt", width=4.0, size=38).move_to(UP * 1.80)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        a_card = self.card("OBJECT A", ["x0 = 1 m", "v = +2 m/s"], width=4.6, height=1.55, title_size=22, body_size=18).move_to(LEFT * 4.35 + UP * 0.22)
        b_card = self.card("OBJECT B", ["x0 = 13 m", "v = -1 m/s"], width=4.6, height=1.55, title_size=22, body_size=18).move_to(RIGHT * 4.35 + UP * 0.22)
        eq_a = self.formula_chip(r"x_A=1+2t", width=4.0, size=32).next_to(a_card, DOWN, buff=0.22)
        eq_b = self.formula_chip(r"x_B=13-t", width=4.0, size=32).next_to(b_card, DOWN, buff=0.22)
        self.play(FadeIn(a_card), FadeIn(b_card), run_time=RUN_NORMAL)
        self.play(FadeIn(eq_a), FadeIn(eq_b), run_time=RUN_NORMAL)

        same = self.text("AT THE MEETING:  xA = xB", 25, BOLD).move_to(DOWN * 1.74)
        algebra = VGroup(
            self.math(r"1+2t=13-t", 34),
            self.math(r"3t=12", 34),
            self.math(r"t=4\,\mathrm{s}", 38),
        ).arrange(RIGHT, buff=0.48).next_to(same, DOWN, buff=0.25)
        self.play(FadeIn(same), run_time=RUN_NORMAL)
        for eq in algebra:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.45)
        box_t = SurroundingRectangle(algebra[-1], buff=0.12, color=BLACK_LINE, stroke_width=2.1)
        self.play(Create(box_t), run_time=RUN_QUICK)

        substitution = VGroup(
            self.math(r"x_A=1+2(4)=9\,\mathrm{m}", 29),
            self.math(r"x_B=13-4=9\,\mathrm{m}", 29),
        ).arrange(RIGHT, buff=0.75).move_to(DOWN * 3.23)
        self.play(Write(substitution[0]), Write(substitution[1]), run_time=RUN_SLOW)
        result = SurroundingRectangle(substitution, buff=0.15, color=BLACK_LINE, stroke_width=2.0)
        self.play(Create(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def compare_methods(self):
        self.set_header(
            8, "GRAPHICAL AND ALGEBRAIC ANSWERS MUST AGREE",
            "The graph intersection and the equation solution describe the same physical event, so both methods must return the same meeting time and position.",
        )
        axes = self.meeting_axes(center=LEFT * 3.30 + DOWN * 0.55, x_length=7.15, y_length=4.35)
        labels = self.meeting_axis_labels(axes, 18)
        numbers = self.meeting_axis_numbers(axes, 14)
        grid = self.meeting_grid(axes)
        self.add(grid)
        a_line = self.graph_line_a(axes, width=3.0)
        b_line = self.graph_line_b(axes, width=2.8)
        meet = Dot(axes.c2p(self.T_MEET, self.X_MEET), radius=0.10, color=BLACK_LINE)
        guides = VGroup(
            DashedLine(axes.c2p(self.T_MEET, 0), axes.c2p(self.T_MEET, self.X_MEET), color=MID_GRAY, dash_length=0.07),
            DashedLine(axes.c2p(0, self.X_MEET), axes.c2p(self.T_MEET, self.X_MEET), color=MID_GRAY, dash_length=0.07),
        )
        self.play(Create(axes), Write(numbers), Write(labels), FadeIn(a_line), FadeIn(b_line), FadeIn(meet), Create(guides), run_time=RUN_SLOW)

        graphical = self.card("GRAPHICAL METHOD", ["intersection", "t = 4 s", "x = 9 m"], width=4.9, height=1.95, title_size=22, body_size=19).move_to(RIGHT * 4.45 + UP * 1.00)
        algebraic = self.card("EQUATION METHOD", ["1 + 2t = 13 - t", "t = 4 s", "x = 9 m"], width=4.9, height=1.95, title_size=22, body_size=18).move_to(RIGHT * 4.45 + DOWN * 1.20)
        self.play(FadeIn(graphical, shift=LEFT * 0.10), FadeIn(algebraic, shift=LEFT * 0.10), run_time=RUN_SLOW)
        agree = self.formula_chip(r"\boxed{(t_{meet},x_{meet})=(4\,\mathrm{s},9\,\mathrm{m})}", width=6.1, size=29).move_to(DOWN * 3.30)
        self.play(FadeIn(agree), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def final_method(self):
        self.set_header(
            9, "NOTEBOOK METHOD: TWO OBJECTS MEETING",
            "Use this sequence whenever two constant-velocity objects share the same one-dimensional path.",
        )
        cards = VGroup(
            self.card("1  CHOOSE +x", ["define one positive direction", "assign velocity signs"], width=4.15, height=1.48, title_size=19, body_size=16),
            self.card("2  RECORD", ["make (t,x) data", "for both objects"], width=4.15, height=1.48, title_size=19, body_size=16),
            self.card("3  GRAPH", ["same axes + same scale", "plot both motions"], width=4.15, height=1.48, title_size=19, body_size=16),
            self.card("4  INTERSECT", ["read meeting time", "read meeting position"], width=4.15, height=1.48, title_size=19, body_size=16),
            self.card("5  WRITE", ["xA = x0A + vAt", "xB = x0B + vBt"], width=4.15, height=1.48, title_size=19, body_size=16),
            self.card("6  VERIFY", ["set xA = xB", "substitute t to find x"], width=4.15, height=1.48, title_size=19, body_size=16),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.30)).move_to(DOWN * 0.52)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.09), run_time=RUN_SLOW * 1.25)
        key = self.formula_chip(r"\text{meeting}\quad\Longleftrightarrow\quad\text{same }t\;\text{and same }x", width=7.2, size=31).next_to(cards, DOWN, buff=0.34)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Two lines intersect because two motions share one time and one position.")
