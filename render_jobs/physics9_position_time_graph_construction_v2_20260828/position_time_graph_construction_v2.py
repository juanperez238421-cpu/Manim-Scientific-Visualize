#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9: professional position-vs-time graph construction.

Uses the audited JP classroom style from the existing position-time workshop
lineage and the project PQH protocol.
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
    BLACK_TEXT,
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


class Physics9PositionTimeGraphConstructionV2(JPClassroomScene):
    """Construct, animate, calculate, and interpret one position-time graph."""

    POINTS = [(0, 2), (3, 8), (5, 8), (7, 4)]
    VELOCITIES = [2, 0, -2]

    def validate_lesson_data(self) -> None:
        slopes = [
            (self.POINTS[i + 1][1] - self.POINTS[i][1]) /
            (self.POINTS[i + 1][0] - self.POINTS[i][0])
            for i in range(3)
        ]
        assert slopes == self.VELOCITIES
        assert self.position_at(0) == 2
        assert self.position_at(3) == 8
        assert self.position_at(5) == 8
        assert self.position_at(7) == 4

    def construct(self) -> None:
        self.opening()
        self.motion_to_data()
        self.axes_and_points()
        self.synchronized_motion()
        self.slope_velocity()
        self.meaning_and_mistakes()
        self.final_method()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(self, title, lines, width=5.4, height=1.7, title_size=24, body_size=20):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        self.fit(content, width - 0.42, height - 0.28)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.21)
        return VGroup(box, content)

    def formula_chip(self, expression, width=5.8, size=33):
        box = RoundedRectangle(
            width=width, height=0.90, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.35, 0.62)
        eq.move_to(box)
        return VGroup(box, eq)

    def position_at(self, t):
        t = max(0.0, min(7.0, float(t)))
        if t <= 3:
            return 2 + 2 * t
        if t <= 5:
            return 8.0
        return 8 - 2 * (t - 5)

    def axes(self, center=DOWN * 0.55, x_length=10.4, y_length=5.0, small=False):
        fs = 17 if small else 20
        return Axes(
            x_range=[0, 7, 1], y_range=[0, 10, 2],
            x_length=x_length, y_length=y_length, tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2},
            x_axis_config={"include_numbers": True, "font_size": fs},
            y_axis_config={"include_numbers": True, "font_size": fs},
        ).move_to(center)

    def axis_labels(self, axes, size=24):
        tx = self.math(r"\text{time }t\;(\mathrm{s})", size)
        tx.next_to(axes.x_axis, DOWN, buff=0.27).shift(RIGHT * 3.05)
        px = self.math(r"\text{position }x\;(\mathrm{m})", size)
        px.next_to(axes.y_axis, UP, buff=0.10).shift(RIGHT * 0.70)
        return VGroup(tx, px)

    def grid(self, axes):
        lines = VGroup()
        for t in range(1, 8):
            lines.add(Line(axes.c2p(t, 0), axes.c2p(t, 10), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.62))
        for x in range(2, 11, 2):
            lines.add(Line(axes.c2p(0, x), axes.c2p(7, x), color=LIGHT_GRAY, stroke_width=1.0).set_stroke(opacity=0.62))
        return lines

    def segments(self, axes, color=BLACK_LINE, width=3.3):
        return VGroup(*[
            Line(axes.c2p(*self.POINTS[i]), axes.c2p(*self.POINTS[i + 1]), color=color, stroke_width=width)
            for i in range(3)
        ])

    def dots(self, axes):
        return VGroup(*[Dot(axes.c2p(*p), radius=0.085, color=BLACK_LINE) for p in self.POINTS])

    def guides(self, axes, point):
        t, x = point
        return VGroup(
            DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY, dash_length=0.08, stroke_width=1.7),
            DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY, dash_length=0.08, stroke_width=1.7),
        )

    def data_table(self, scale=1.0):
        data = [[r"t\;(\mathrm{s})", r"x\;(\mathrm{m})"], ["0", "2"], ["3", "8"], ["5", "8"], ["7", "4"]]
        rows = []
        for r, row in enumerate(data):
            cells = VGroup()
            for entry in row:
                rect = Rectangle(
                    width=2.15, height=0.60,
                    stroke_color=BLACK_LINE, stroke_width=1.5,
                    fill_color=PAPER_GRAY if r == 0 else WHITE, fill_opacity=1,
                )
                label = self.math(entry, 25 if r == 0 else 27).move_to(rect)
                cells.add(VGroup(rect, label))
            cells.arrange(RIGHT, buff=0)
            rows.append(cells)
        return VGroup(*rows).arrange(DOWN, buff=0).scale(scale), rows

    def track(self, width=10.8, y=0.7):
        x0, x1 = -width / 2, width / 2
        line = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.5)
        ticks, nums = VGroup(), VGroup()
        for value in range(0, 11, 2):
            x = x0 + value / 10 * width
            ticks.add(Line([x, y - 0.09, 0], [x, y + 0.09, 0], color=BLACK_LINE, stroke_width=1.7))
            nums.add(self.math(str(value), 20).move_to([x, y - 0.28, 0]))
        label = self.math(r"x\;(\mathrm{m})", 24).next_to(line, RIGHT, buff=0.12)
        return VGroup(line, ticks, nums, label)

    def track_x(self, position, width=10.8):
        return -width / 2 + float(position) / 10 * width

    def walker(self, scale=1.0):
        head = Circle(radius=0.13, stroke_color=BLACK_LINE, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        body = RoundedRectangle(
            width=0.24, height=0.44, corner_radius=0.07,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        ).next_to(head, DOWN, buff=0.03)
        shoulder, hip = body.get_top() + DOWN * 0.08, body.get_bottom() + UP * 0.05
        limbs = VGroup(
            Line(shoulder + LEFT * 0.07, shoulder + LEFT * 0.24 + DOWN * 0.18, color=BLACK_LINE, stroke_width=3),
            Line(shoulder + RIGHT * 0.07, shoulder + RIGHT * 0.23 + DOWN * 0.16, color=BLACK_LINE, stroke_width=3),
            Line(hip + LEFT * 0.05, hip + LEFT * 0.17 + DOWN * 0.27, color=BLACK_LINE, stroke_width=3),
            Line(hip + RIGHT * 0.05, hip + RIGHT * 0.19 + DOWN * 0.27, color=BLACK_LINE, stroke_width=3),
        )
        return VGroup(head, body, limbs).scale(scale)

    # ------------------------------------------------------------------
    # Lesson sections
    # ------------------------------------------------------------------
    def opening(self):
        self.standard_opening(
            "PHYSICS 9 | KINEMATICS",
            "POSITION vs TIME GRAPH",
            "Construct the graph from motion data and read velocity from its slope",
            "Position is the vertical value. Time is the horizontal value. Slope tells the motion.",
        )

    def motion_to_data(self):
        self.set_header(
            1, "START WITH THE MOTION, NOT WITH THE GRAPH",
            "A position-time graph records where the object is at each instant. First identify the events and write each one as an ordered pair (t, x).",
        )
        track = self.track(width=10.8, y=0.75)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_SLOW)
        events = [
            (0, 2, "START", "t = 0 s", "x = 2 m"),
            (3, 8, "MOVE RIGHT", "t = 3 s", "x = 8 m"),
            (5, 8, "WAIT", "t = 5 s", "x = 8 m"),
            (7, 4, "RETURN LEFT", "t = 7 s", "x = 4 m"),
        ]
        cards = VGroup(*[
            self.card(title, [t_text, x_text], width=3.10, height=1.42, title_size=21, body_size=19)
            for _, _, title, t_text, x_text in events
        ]).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.85)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.10), run_time=RUN_SLOW)

        person = self.walker(1.02).move_to([self.track_x(2), 1.40, 0])
        self.play(FadeIn(person), run_time=RUN_NORMAL)
        active = SurroundingRectangle(cards[0], buff=0.05, color=BLACK_LINE, stroke_width=2.3)
        self.play(Create(active), run_time=RUN_QUICK)
        for i, (_, x, _, _, _) in enumerate(events[1:], start=1):
            next_box = SurroundingRectangle(cards[i], buff=0.05, color=BLACK_LINE, stroke_width=2.3)
            self.play(
                person.animate.move_to([self.track_x(x), 1.40, 0]),
                ReplacementTransform(active, next_box),
                run_time=1.45 if i != 2 else 0.85,
                rate_func=smooth,
            )
            active = next_box
            self.wait(PAUSE_SHORT)
        pair = self.formula_chip(r"(t,x):\;(0,2)\rightarrow(3,8)\rightarrow(5,8)\rightarrow(7,4)", width=8.7, size=30)
        pair.next_to(cards, DOWN, buff=0.28)
        self.play(FadeIn(pair), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def axes_and_points(self):
        self.set_header(
            2, "CONSTRUCT THE GRAPH STEP BY STEP",
            "Put time on the horizontal axis and position on the vertical axis, choose a readable scale, then plot every data row as (t, x) before connecting points.",
        )
        table, rows = self.data_table(0.93)
        table.move_to(LEFT * 4.75 + DOWN * 0.25)
        table_title = self.text("MOTION DATA", 26, BOLD).next_to(table, UP, buff=0.20)
        axes = self.axes(center=RIGHT * 2.20 + DOWN * 0.55, x_length=8.45, y_length=4.9, small=True)
        labels, grid = self.axis_labels(axes, 22), self.grid(axes)

        self.play(FadeIn(table_title), FadeIn(table), run_time=RUN_SLOW)
        self.play(Create(axes.x_axis), Write(labels[0]), run_time=RUN_NORMAL)
        x_note = self.card("HORIZONTAL", ["time t", "seconds (s)"], width=3.35, height=1.28, title_size=20, body_size=18)
        x_note.move_to(RIGHT * 5.40 + DOWN * 2.45)
        self.play(FadeIn(x_note), run_time=RUN_NORMAL)
        self.play(Create(axes.y_axis), Write(labels[1]), run_time=RUN_NORMAL)
        y_note = self.card("VERTICAL", ["position x", "meters (m)"], width=3.35, height=1.28, title_size=20, body_size=18)
        y_note.move_to(RIGHT * 5.40 + UP * 1.65)
        self.play(FadeIn(y_note), Create(grid), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        directions = [DR, UL, DL, UL]
        guides_group, dots_group, labels_group = VGroup(), VGroup(), VGroup()
        current = None
        for i, point in enumerate(self.POINTS, start=1):
            row_box = SurroundingRectangle(rows[i], buff=0.04, color=BLACK_LINE, stroke_width=2.2)
            if current is None:
                self.play(Create(row_box), run_time=RUN_QUICK)
            else:
                self.play(ReplacementTransform(current, row_box), run_time=RUN_QUICK)
            current = row_box
            guides = self.guides(axes, point)
            dot = Dot(axes.c2p(*point), radius=0.09, color=BLACK_LINE)
            label = self.math(rf"({point[0]},{point[1]})", 19).next_to(axes.c2p(*point), directions[i - 1], buff=0.07)
            guides_group.add(guides); dots_group.add(dot); labels_group.add(label)
            self.play(Create(guides), FadeIn(dot, scale=1.3), Write(label), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.55)
        self.play(FadeOut(current), FadeOut(guides_group), run_time=RUN_NORMAL)
        segs = self.segments(axes)
        self.play(LaggedStart(*[Create(seg) for seg in segs], lag_ratio=0.22), run_time=RUN_SLOW * 1.3)
        rule = self.card("CONNECT IN TIME ORDER", ["0 s -> 3 s -> 5 s -> 7 s", "One segment = one motion interval."], width=5.0, height=1.45, title_size=20, body_size=18)
        rule.move_to(LEFT * 4.65 + DOWN * 2.55)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def synchronized_motion(self):
        self.set_header(
            3, "SAME MOTION, TWO REPRESENTATIONS",
            "The object moves on a physical line while one point moves through (time, position) space. This is why the graph is a record of motion, not a map of the path.",
        )
        track = self.track(width=10.9, y=1.45)
        graph = self.axes(center=DOWN * 1.62, x_length=8.8, y_length=3.15, small=True)
        graph_labels, graph_grid = self.axis_labels(graph, 20), self.grid(graph)
        pale = self.segments(graph, color=LIGHT_GRAY, width=3.1)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_NORMAL)
        self.add(graph_grid)
        self.play(Create(graph), Write(graph_labels), FadeIn(pale), FadeIn(self.dots(graph)), run_time=RUN_SLOW)

        t = ValueTracker(0.0)
        person = always_redraw(lambda: self.walker(0.82).move_to([self.track_x(self.position_at(t.get_value()), 10.9), 2.00, 0]))
        point = always_redraw(lambda: Dot(graph.c2p(t.get_value(), self.position_at(t.get_value())), radius=0.085, color=BLACK_LINE))
        guide = always_redraw(lambda: DashedLine(graph.c2p(t.get_value(), 0), graph.c2p(t.get_value(), self.position_at(t.get_value())), color=MID_GRAY, dash_length=0.07, stroke_width=1.6))
        trace = TracedPath(point.get_center, stroke_color=BLACK_LINE, stroke_width=4)
        self.add(trace, guide, person, point)

        state = self.card("INTERVAL 1", ["moving right", "slope > 0"], width=3.35, height=1.22, title_size=20, body_size=18).move_to(LEFT * 4.90 + UP * 2.05)
        self.play(FadeIn(state), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(3), run_time=3.0, rate_func=linear)
        self.wait(PAUSE_SHORT)
        state2 = self.card("INTERVAL 2", ["at rest", "slope = 0"], width=3.35, height=1.22, title_size=20, body_size=18).move_to(state)
        self.play(ReplacementTransform(state, state2), run_time=RUN_QUICK)
        state = state2
        self.play(t.animate.set_value(5), run_time=2.0, rate_func=linear)
        self.wait(PAUSE_SHORT)
        state3 = self.card("INTERVAL 3", ["moving left", "slope < 0"], width=3.35, height=1.22, title_size=20, body_size=18).move_to(state)
        self.play(ReplacementTransform(state, state3), run_time=RUN_QUICK)
        self.play(t.animate.set_value(7), run_time=2.0, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def slope_velocity(self):
        self.set_header(
            4, "SLOPE IS VELOCITY",
            "For each straight segment, velocity is change in position divided by change in time. Positive, zero, and negative slopes have direct physical meanings.",
        )
        axes = self.axes(center=LEFT * 3.15 + DOWN * 0.55, x_length=7.3, y_length=4.85, small=True)
        self.add(self.grid(axes))
        labels = self.axis_labels(axes, 21)
        base = self.segments(axes, color=LIGHT_GRAY, width=3.0)
        self.play(Create(axes), Write(labels), FadeIn(base), FadeIn(self.dots(axes)), run_time=RUN_SLOW)

        cases = [
            (0, r"\Delta x=8-2=+6\,\mathrm{m}", r"\Delta t=3-0=3\,\mathrm{s}", r"v=\frac{+6}{3}=+2\,\mathrm{m/s}", "POSITIVE SLOPE", ["position increases", "motion toward +x"]),
            (1, r"\Delta x=8-8=0\,\mathrm{m}", r"\Delta t=5-3=2\,\mathrm{s}", r"v=\frac{0}{2}=0\,\mathrm{m/s}", "ZERO SLOPE", ["position is constant", "object is at rest"]),
            (2, r"\Delta x=4-8=-4\,\mathrm{m}", r"\Delta t=7-5=2\,\mathrm{s}", r"v=\frac{-4}{2}=-2\,\mathrm{m/s}", "NEGATIVE SLOPE", ["position decreases", "motion toward -x"]),
        ]
        active = rhs = None
        for index, dx, dt, answer, title, meaning in cases:
            new_active = base[index].copy().set_color(BLACK_LINE).set_stroke(width=5)
            eqs = VGroup(self.math(dx, 29), self.math(dt, 29), self.math(answer, 37)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = SurroundingRectangle(eqs[-1], buff=0.13, color=BLACK_LINE, stroke_width=2)
            meaning_card = self.card(title, meaning, width=5.45, height=1.55, title_size=21, body_size=18)
            new_rhs = VGroup(eqs, box, meaning_card).arrange(DOWN, buff=0.28).move_to(RIGHT * 4.30 + DOWN * 0.42)
            if active is None:
                self.play(Create(new_active), FadeIn(new_rhs, shift=LEFT * 0.08), run_time=RUN_SLOW)
            else:
                self.play(ReplacementTransform(active, new_active), ReplacementTransform(rhs, new_rhs), run_time=RUN_SLOW)
            active, rhs = new_active, new_rhs
            self.wait(PAUSE_WORK)
        formula = self.formula_chip(r"v=\text{slope}=\frac{\Delta x}{\Delta t}", width=5.4, size=34).move_to(RIGHT * 4.30 + UP * 2.15)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def meaning_and_mistakes(self):
        self.set_header(
            5, "READ THE GRAPH CORRECTLY",
            "The vertical coordinate gives position; the slope gives velocity. The shape of the line is not the physical road traveled by the object.",
        )
        cards = VGroup(
            self.card("HEIGHT = POSITION", ["Read x from the vertical axis.", "A larger height means a larger position."], width=6.25, height=1.55, title_size=22, body_size=18),
            self.card("SLOPE = VELOCITY", ["Rising: v > 0", "Horizontal: v = 0", "Falling: v < 0"], width=6.25, height=1.55, title_size=22, body_size=18),
            self.card("NOT A MAP OF THE PATH", ["The line lives in (time, position) space.", "It is a data representation of the motion."], width=6.25, height=1.55, title_size=22, body_size=18),
            self.card("POSITION AND VELOCITY ARE DIFFERENT", ["The object can have x > 0 and v < 0.", "Returning from 8 m to 4 m proves it."], width=6.25, height=1.55, title_size=22, body_size=18),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.42, 0.40)).move_to(DOWN * 0.42)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.12), run_time=RUN_SLOW * 1.35)
        check = self.formula_chip(r"x>0\;\text{can coexist with}\;v<0", width=6.4, size=31).to_edge(DOWN, buff=0.27)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def final_method(self):
        self.set_header(
            6, "THE SIX-STEP POSITION-TIME METHOD",
            "Use the same sequence for a table, an experiment, or a written description of motion.",
        )
        info = [
            ("1", "RECORD DATA", "Write each event as (t, x)."),
            ("2", "TIME HORIZONTAL", "Label t and seconds."),
            ("3", "POSITION VERTICAL", "Label x and meters."),
            ("4", "CHOOSE SCALE", "Use equal readable intervals."),
            ("5", "PLOT + CONNECT", "Follow chronological order."),
            ("6", "READ SLOPE", "v = Delta x / Delta t."),
        ]
        cards = VGroup()
        for number, title, body in info:
            badge = RoundedRectangle(width=0.58, height=0.48, corner_radius=0.09, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=PAPER_GRAY, fill_opacity=1)
            num = self.text(number, 22, BOLD).move_to(badge)
            text_group = VGroup(self.text(title, 21, BOLD), self.text(body, 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            row = VGroup(VGroup(badge, num), text_group).arrange(RIGHT, buff=0.18)
            box = RoundedRectangle(width=5.95, height=1.18, corner_radius=0.11, stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
            row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.24)
            cards.add(VGroup(box, row))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.42, 0.28)).move_to(DOWN * 0.38)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.07) for c in cards], lag_ratio=0.10), run_time=RUN_SLOW * 1.45)
        self.wait(PAUSE_WORK)
        exit_q = self.card(
            "EXIT QUESTION",
            ["A graph rises from (1 s, 3 m) to (4 s, 12 m).", "What is the velocity? Explain its sign from the graph."],
            width=9.0, height=1.40, title_size=21, body_size=18,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(exit_q), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Construct carefully. Read position from height. Read velocity from slope.")
