#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9: Position-Time Graph Construction V3 — senior QA revision.

This revision preserves the accepted V2 classroom architecture while fixing
visual defects found in a frame-by-frame senior QA pass:
- explicit numeric scale labels on both axes;
- no callout overlap with plotted data;
- clean cross-fades instead of glyph-morphing state cards;
- no detached/blank answer rectangles;
- slope formula introduced before the worked cases;
- visible rise/run geometry for each velocity calculation.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
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


class Physics9PositionTimeGraphConstructionV3(JPClassroomScene):
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
        assert [self.position_at(t) for t in (0, 3, 5, 7)] == [2, 8, 8, 4]

    def construct(self) -> None:
        self.opening()
        self.motion_to_data()
        self.axes_and_points()
        self.synchronized_motion()
        self.slope_velocity()
        self.meaning_and_mistakes()
        self.final_method()

    # ------------------------------------------------------------------
    # Reusable visual helpers
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

    def axes(self, center=DOWN * 0.55, x_length=10.4, y_length=5.0):
        return Axes(
            x_range=[0, 7, 1], y_range=[0, 10, 2],
            x_length=x_length, y_length=y_length, tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2, "include_numbers": False},
        ).move_to(center)

    def axis_labels(self, axes, size=24):
        tx = self.math(r"\text{time }t\;(\mathrm{s})", size)
        tx.next_to(axes.x_axis, DOWN, buff=0.28).align_to(axes.x_axis, RIGHT).shift(LEFT * 0.10)
        px = self.math(r"\text{position }x\;(\mathrm{m})", size)
        px.next_to(axes.y_axis, UP, buff=0.11).align_to(axes.y_axis, LEFT).shift(RIGHT * 0.08)
        return VGroup(tx, px)

    def axis_numbers(self, axes, size=18):
        """Explicit labels; avoids relying on NumberLine internal number rendering."""
        x_nums = VGroup()
        for t in range(0, 8):
            lab = self.math(str(t), size)
            lab.next_to(axes.c2p(t, 0), DOWN, buff=0.10)
            x_nums.add(lab)
        y_nums = VGroup()
        for x in range(0, 11, 2):
            lab = self.math(str(x), size)
            lab.next_to(axes.c2p(0, x), LEFT, buff=0.11)
            y_nums.add(lab)
        return VGroup(x_nums, y_nums)

    def grid(self, axes):
        lines = VGroup()
        for t in range(1, 8):
            lines.add(
                Line(axes.c2p(t, 0), axes.c2p(t, 10), color=LIGHT_GRAY, stroke_width=1.0)
                .set_stroke(opacity=0.58)
            )
        for x in range(2, 11, 2):
            lines.add(
                Line(axes.c2p(0, x), axes.c2p(7, x), color=LIGHT_GRAY, stroke_width=1.0)
                .set_stroke(opacity=0.58)
            )
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
        data = [
            [r"t\;(\mathrm{s})", r"x\;(\mathrm{m})"],
            ["0", "2"], ["3", "8"], ["5", "8"], ["7", "4"],
        ]
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
        table = VGroup(*rows).arrange(DOWN, buff=0).scale(scale)
        return table, rows

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
        shoulder = body.get_top() + DOWN * 0.08
        hip = body.get_bottom() + UP * 0.05
        limbs = VGroup(
            Line(shoulder + LEFT * 0.07, shoulder + LEFT * 0.24 + DOWN * 0.18, color=BLACK_LINE, stroke_width=3),
            Line(shoulder + RIGHT * 0.07, shoulder + RIGHT * 0.23 + DOWN * 0.16, color=BLACK_LINE, stroke_width=3),
            Line(hip + LEFT * 0.05, hip + LEFT * 0.17 + DOWN * 0.27, color=BLACK_LINE, stroke_width=3),
            Line(hip + RIGHT * 0.05, hip + RIGHT * 0.19 + DOWN * 0.27, color=BLACK_LINE, stroke_width=3),
        )
        return VGroup(head, body, limbs).scale(scale)

    def slope_triangle(self, axes, p1, p2, dx_text, dt_text):
        """Rise/run geometry for one straight x-t segment."""
        t1, x1 = p1
        t2, x2 = p2
        horizontal = Line(axes.c2p(t1, x1), axes.c2p(t2, x1), color=MID_GRAY, stroke_width=2.2)
        dt = self.math(dt_text, 20).next_to(horizontal, DOWN if x2 >= x1 else UP, buff=0.06)
        if x2 == x1:
            return VGroup(horizontal, dt)
        vertical = Line(axes.c2p(t2, x1), axes.c2p(t2, x2), color=MID_GRAY, stroke_width=2.2)
        dx = self.math(dx_text, 20).next_to(vertical, RIGHT, buff=0.07)
        return VGroup(horizontal, vertical, dt, dx)

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
            self.play(person.animate.move_to([self.track_x(x), 1.40, 0]), run_time=1.40 if i != 2 else 0.85, rate_func=smooth)
            self.play(FadeOut(active), FadeIn(next_box), run_time=RUN_QUICK)
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
        axes = self.axes(center=RIGHT * 2.05 + DOWN * 0.52, x_length=8.05, y_length=4.65)
        labels = self.axis_labels(axes, 21)
        numbers = self.axis_numbers(axes, 17)
        grid = self.grid(axes)

        self.play(FadeIn(table_title), FadeIn(table), run_time=RUN_SLOW)
        self.play(Create(axes.x_axis), Write(numbers[0]), Write(labels[0]), run_time=RUN_NORMAL)
        x_note = self.card("HORIZONTAL AXIS", ["time t", "seconds (s)"], width=3.15, height=1.23, title_size=19, body_size=17)
        x_note.move_to(RIGHT * 5.62 + DOWN * 2.62)
        self.play(FadeIn(x_note), run_time=RUN_NORMAL)
        self.play(Create(axes.y_axis), Write(numbers[1]), Write(labels[1]), run_time=RUN_NORMAL)
        y_note = self.card("VERTICAL AXIS", ["position x", "meters (m)"], width=3.15, height=1.23, title_size=19, body_size=17)
        y_note.move_to(RIGHT * 5.62 + UP * 1.72)
        self.play(FadeIn(y_note), Create(grid), run_time=RUN_SLOW)
        scale_note = self.card("SCALE", ["equal spacing", "1 s horizontally", "2 m vertically"], width=3.15, height=1.35, title_size=19, body_size=16)
        scale_note.move_to(LEFT * 4.75 + DOWN * 2.47)
        self.play(FadeIn(scale_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        # Keep the plotting area clean before data points appear.
        self.play(FadeOut(x_note), FadeOut(y_note), run_time=RUN_NORMAL)

        directions = [DR, UL, DL, UL]
        guides_group, dots_group, labels_group = VGroup(), VGroup(), VGroup()
        current = None
        for i, point in enumerate(self.POINTS, start=1):
            row_box = SurroundingRectangle(rows[i], buff=0.04, color=BLACK_LINE, stroke_width=2.2)
            if current is not None:
                self.play(FadeOut(current), run_time=RUN_QUICK * 0.55)
            self.play(Create(row_box), run_time=RUN_QUICK * 0.65)
            current = row_box
            guides = self.guides(axes, point)
            dot = Dot(axes.c2p(*point), radius=0.09, color=BLACK_LINE)
            label = self.math(rf"({point[0]},{point[1]})", 19).next_to(axes.c2p(*point), directions[i - 1], buff=0.07)
            guides_group.add(guides)
            dots_group.add(dot)
            labels_group.add(label)
            self.play(Create(guides), FadeIn(dot, scale=1.3), Write(label), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.55)
        self.play(FadeOut(current), FadeOut(guides_group), run_time=RUN_NORMAL)
        segs = self.segments(axes)
        self.play(LaggedStart(*[Create(seg) for seg in segs], lag_ratio=0.22), run_time=RUN_SLOW * 1.3)
        rule = self.card(
            "CONNECT ONLY AFTER PLOTTING",
            ["chronological order: 0 -> 3 -> 5 -> 7 s", "one segment = one motion interval"],
            width=5.05, height=1.52, title_size=19, body_size=17,
        )
        rule.move_to(LEFT * 4.65 + DOWN * 2.46)
        self.play(ReplacementTransform(scale_note, rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def synchronized_motion(self):
        self.set_header(
            3, "SAME MOTION, TWO REPRESENTATIONS",
            "The object moves on a physical line while one point moves through (time, position) space. The graph records motion; it is not a map of the path.",
        )
        track = self.track(width=10.9, y=1.42)
        graph = self.axes(center=DOWN * 1.58, x_length=8.55, y_length=3.02)
        graph_labels = self.axis_labels(graph, 19)
        graph_numbers = self.axis_numbers(graph, 15)
        graph_grid = self.grid(graph)
        pale = self.segments(graph, color=LIGHT_GRAY, width=3.0)
        self.play(Create(track[0]), FadeIn(track[1]), Write(track[2]), Write(track[3]), run_time=RUN_NORMAL)
        self.add(graph_grid)
        self.play(Create(graph), Write(graph_numbers), Write(graph_labels), FadeIn(pale), FadeIn(self.dots(graph)), run_time=RUN_SLOW)

        t = ValueTracker(0.0)
        person = always_redraw(lambda: self.walker(0.82).move_to([self.track_x(self.position_at(t.get_value()), 10.9), 1.97, 0]))
        point = always_redraw(lambda: Dot(graph.c2p(t.get_value(), self.position_at(t.get_value())), radius=0.085, color=BLACK_LINE))
        guide = always_redraw(lambda: DashedLine(graph.c2p(t.get_value(), 0), graph.c2p(t.get_value(), self.position_at(t.get_value())), color=MID_GRAY, dash_length=0.07, stroke_width=1.6))
        trace = TracedPath(point.get_center, stroke_color=BLACK_LINE, stroke_width=4)
        clock = always_redraw(lambda: self.math(rf"t={t.get_value():.1f}\,\mathrm{{s}}", 22).move_to(RIGHT * 5.85 + UP * 2.18))
        self.add(trace, guide, person, point, clock)

        state = self.card("INTERVAL 1", ["moving right", "positive slope"], width=3.25, height=1.18, title_size=19, body_size=17).move_to(LEFT * 5.05 + UP * 2.10)
        self.play(FadeIn(state), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(3), run_time=3.0, rate_func=linear)
        self.wait(PAUSE_SHORT)
        state2 = self.card("INTERVAL 2", ["at rest", "zero slope"], width=3.25, height=1.18, title_size=19, body_size=17).move_to(state)
        self.play(FadeOut(state), FadeIn(state2), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(5), run_time=2.0, rate_func=linear)
        self.wait(PAUSE_SHORT)
        state3 = self.card("INTERVAL 3", ["moving left", "negative slope"], width=3.25, height=1.18, title_size=19, body_size=17).move_to(state2)
        self.play(FadeOut(state2), FadeIn(state3), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(7), run_time=2.0, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def slope_velocity(self):
        self.set_header(
            4, "SLOPE IS VELOCITY",
            "For each straight segment, velocity is change in position divided by change in time. Positive, zero, and negative slopes have direct physical meanings.",
        )
        axes = self.axes(center=LEFT * 3.15 + DOWN * 0.55, x_length=7.25, y_length=4.75)
        labels = self.axis_labels(axes, 20)
        numbers = self.axis_numbers(axes, 16)
        self.add(self.grid(axes))
        base = self.segments(axes, color=LIGHT_GRAY, width=3.0)
        self.play(Create(axes), Write(numbers), Write(labels), FadeIn(base), FadeIn(self.dots(axes)), run_time=RUN_SLOW)

        formula = self.formula_chip(r"v=\text{slope}=\frac{\Delta x}{\Delta t}", width=5.35, size=34)
        formula.move_to(RIGHT * 4.35 + UP * 2.18)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)

        cases = [
            (0, r"\Delta x=8-2=+6\,\mathrm{m}", r"\Delta t=3-0=3\,\mathrm{s}", r"v=\frac{+6}{3}=+2\,\mathrm{m/s}", "POSITIVE SLOPE", ["position increases", "motion toward +x"], r"\Delta x=+6", r"\Delta t=3"),
            (1, r"\Delta x=8-8=0\,\mathrm{m}", r"\Delta t=5-3=2\,\mathrm{s}", r"v=\frac{0}{2}=0\,\mathrm{m/s}", "ZERO SLOPE", ["position is constant", "object is at rest"], r"\Delta x=0", r"\Delta t=2"),
            (2, r"\Delta x=4-8=-4\,\mathrm{m}", r"\Delta t=7-5=2\,\mathrm{s}", r"v=\frac{-4}{2}=-2\,\mathrm{m/s}", "NEGATIVE SLOPE", ["position decreases", "motion toward -x"], r"\Delta x=-4", r"\Delta t=2"),
        ]

        active_line = active_rhs = active_triangle = None
        for index, dx, dt, answer, title, meaning, dx_short, dt_short in cases:
            p1, p2 = self.POINTS[index], self.POINTS[index + 1]
            new_line = base[index].copy().set_color(BLACK_LINE).set_stroke(width=5)
            tri = self.slope_triangle(axes, p1, p2, dx_short, dt_short)

            eqs = VGroup(self.math(dx, 28), self.math(dt, 28), self.math(answer, 36))
            eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.20)
            eqs.move_to(RIGHT * 4.35 + UP * 0.40)
            meaning_card = self.card(title, meaning, width=5.35, height=1.45, title_size=21, body_size=18)
            meaning_card.move_to(RIGHT * 4.35 + DOWN * 1.85)
            answer_box = SurroundingRectangle(eqs[-1], buff=0.14, color=BLACK_LINE, stroke_width=2)
            new_rhs = VGroup(eqs, answer_box, meaning_card)

            if active_line is not None:
                self.play(FadeOut(active_line), FadeOut(active_rhs), FadeOut(active_triangle), run_time=RUN_NORMAL)
            self.play(Create(new_line), Create(tri), FadeIn(new_rhs, shift=LEFT * 0.08), run_time=RUN_SLOW)
            active_line, active_rhs, active_triangle = new_line, new_rhs, tri
            self.wait(PAUSE_WORK)

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
            ("6", "READ SLOPE", "v = Δx / Δt."),
        ]
        cards = VGroup()
        for number, title, body in info:
            badge = RoundedRectangle(
                width=0.58, height=0.48, corner_radius=0.09,
                stroke_color=BLACK_LINE, stroke_width=1.8,
                fill_color=PAPER_GRAY, fill_opacity=1,
            )
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
