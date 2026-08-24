#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 position-time velocity workshop.

Rendered with the JP classroom style and the full ManimCE PQH package protocol.
"""
from __future__ import annotations

from manim import *

from jp_classroom_style import (
    JPClassroomScene,
    BLACK_TEXT,
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


class Physics9PositionTimeVelocityWorkshop(JPClassroomScene):
    """Examples and workshop for velocity from position-time graphs."""

    PIECEWISE_POINTS = [(0, 0), (2, 8), (5, 8), (7, 2)]
    PIECEWISE_V = [4, 0, -3]

    def validate_lesson_data(self) -> None:
        assert (14 - 2) / (5 - 1) == 3
        assert (6 - 6) / (4 - 0) == 0
        assert (4 - 12) / (5 - 1) == -2
        assert 10 / 2 == 5 and 6 / 2 == 3
        pts = self.PIECEWISE_POINTS
        slopes = [(pts[i + 1][1] - pts[i][1]) / (pts[i + 1][0] - pts[i][0]) for i in range(3)]
        assert slopes == self.PIECEWISE_V
        assert (2 - 0) / (7 - 0) == 2 / 7

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def result_chip(self, expression: str, width=4.8, size=33) -> VGroup:
        box = RoundedRectangle(
            width=width, height=0.84, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.34, 0.56)
        eq.move_to(box)
        return VGroup(box, eq)

    def card(self, title: str, lines: list[str], width=5.3, height=1.75) -> VGroup:
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1,
        )
        title_mob = self.text(title, 25, BOLD)
        body = VGroup(*[self.text(line, 21) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.45, height - 0.35)
        content.move_to(box)
        return VGroup(box, content)

    def position_axes(
        self,
        x_max=7,
        y_min=0,
        y_max=14,
        position=LEFT * 2.9 + DOWN * 0.55,
        x_length=7.7,
        y_length=4.8,
    ) -> Axes:
        y_step = 2 if y_max - y_min >= 8 else 1
        return Axes(
            x_range=[0, x_max, 1],
            y_range=[y_min, y_max, y_step],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2},
            x_axis_config={"include_numbers": True, "font_size": 20},
            y_axis_config={"include_numbers": True, "font_size": 20},
        ).move_to(position)

    def velocity_axes(
        self,
        x_max=7,
        y_min=-4,
        y_max=5,
        position=RIGHT * 3.6 + DOWN * 0.55,
        x_length=6.4,
        y_length=4.55,
    ) -> Axes:
        return Axes(
            x_range=[0, x_max, 1],
            y_range=[y_min, y_max, 1],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.1},
            x_axis_config={"include_numbers": True, "font_size": 18},
            y_axis_config={"include_numbers": True, "font_size": 18},
        ).move_to(position)

    def axis_labels(self, axes: Axes, vertical: str) -> VGroup:
        tx = self.math(r"t\;(\mathrm{s})", 25).next_to(axes.x_axis, RIGHT, buff=0.10)
        vy = self.math(vertical, 25).next_to(axes.y_axis, UP, buff=0.08)
        return VGroup(tx, vy)

    def polyline(self, axes: Axes, points, color=BLACK_LINE, width=3.2) -> VGroup:
        return VGroup(*[
            Line(axes.c2p(*points[i]), axes.c2p(*points[i + 1]), color=color, stroke_width=width)
            for i in range(len(points) - 1)
        ])

    def dots(self, axes: Axes, points) -> VGroup:
        return VGroup(*[Dot(axes.c2p(*p), radius=0.09, color=BLACK_LINE) for p in points])

    def coordinate_label(self, axes: Axes, point, text_value: str, direction=UR) -> Mobject:
        label = self.math(text_value, 22)
        label.next_to(axes.c2p(*point), direction, buff=0.08)
        return label

    def interval_guides(self, axes: Axes, boundaries, y_min, y_max) -> VGroup:
        return VGroup(*[
            DashedLine(axes.c2p(t, y_min), axes.c2p(t, y_max), color=LIGHT_GRAY, dash_length=0.08)
            for t in boundaries
        ])

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9 • POSITION AND VELOCITY",
            "READ SLOPE, CALCULATE VELOCITY",
            "Examples and position-time graph workshop",
            "One straight x–t segment gives one constant velocity.",
        )

    def workshop_map(self) -> None:
        self.set_header(1, "WORKSHOP MAP", "We will calculate velocity from slope and then build the matching velocity-time graph.")
        cards = VGroup(
            self.card("1  CHOOSE", ["Two points", "on one segment"], width=3.25, height=1.65),
            self.card("2  CHANGE", ["Calculate Dx", "and Dt"], width=3.25, height=1.65),
            self.card("3  DIVIDE", ["v = Dx / Dt", "keep the sign"], width=3.25, height=1.65),
            self.card("4  GRAPH", ["One v level", "per interval"], width=3.25, height=1.65),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.14), run_time=RUN_SLOW)
        bridge = self.math(r"x\!\! -\!\! t\;\mathrm{slope}\;\longrightarrow\;v\;\longrightarrow\;v\!\! -\!\! t\;\mathrm{height}", 38)
        bridge.next_to(cards, DOWN, buff=0.50)
        self.play(Write(bridge), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def slope_recipe(self) -> None:
        self.set_header(2, "THE SLOPE RECIPE", "Choose two points on the same straight segment. Slope is change in position divided by change in time.")
        axes = self.position_axes(x_max=4, y_max=12, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        p1, p2 = (1, 2), (4, 11)
        line = self.polyline(axes, [p1, p2])
        points = self.dots(axes, [p1, p2])
        p1_label = self.coordinate_label(axes, p1, r"P_1(t_1,x_1)", DL)
        p2_label = self.coordinate_label(axes, p2, r"P_2(t_2,x_2)", UR)
        run = Line(axes.c2p(*p1), axes.c2p(p2[0], p1[1]), color=MID_GRAY, stroke_width=2.4)
        rise = Line(axes.c2p(p2[0], p1[1]), axes.c2p(*p2), color=MID_GRAY, stroke_width=2.4)
        dt = self.math(r"\Delta t", 24).next_to(run, DOWN, buff=0.08)
        dx = self.math(r"\Delta x", 24).next_to(rise, RIGHT, buff=0.08)
        formula = self.result_chip(r"v_{\mathrm{avg}}=\frac{x_2-x_1}{t_2-t_1}=\frac{\Delta x}{\Delta t}", 6.0, 31)
        formula.move_to(RIGHT * 4.35 + UP * 1.18)
        recipe = self.card("WRITE BEFORE SUBSTITUTING", ["P1=(t1,x1)", "P2=(t2,x2)", "units: m/s"], width=5.5, height=2.10)
        recipe.move_to(RIGHT * 4.35 + DOWN * 1.20)
        unit = self.result_chip(r"\frac{\mathrm{m}}{\mathrm{s}}=\mathrm{m/s}", 3.6, 31).next_to(recipe, DOWN, buff=0.34)
        self.play(Create(axes), Write(labels), run_time=RUN_NORMAL)
        self.play(Create(line), FadeIn(points), Write(p1_label), Write(p2_label), run_time=RUN_SLOW)
        self.play(Create(run), Create(rise), Write(dt), Write(dx), run_time=RUN_NORMAL)
        self.play(Write(formula), FadeIn(recipe, shift=LEFT * 0.10), run_time=RUN_SLOW)
        self.play(FadeIn(unit), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def positive_example(self) -> None:
        self.set_header(3, "EXAMPLE A: POSITIVE VELOCITY", "The object moves from 2 m at 1 s to 14 m at 5 s. Calculate and interpret the slope.")
        axes = self.position_axes(x_max=5, y_max=16, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        pts = [(1, 2), (5, 14)]
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        coord = VGroup(
            self.coordinate_label(axes, pts[0], r"(1,2)", DR),
            self.coordinate_label(axes, pts[1], r"(5,14)", UL),
        )
        eqs = VGroup(
            self.math(r"\Delta x=14-2=12\,\mathrm{m}", 31),
            self.math(r"\Delta t=5-1=4\,\mathrm{s}", 31),
            self.math(r"v=\frac{12}{4}=+3\,\mathrm{m/s}", 36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 4.35 + DOWN * 0.45)
        interpretation = self.card("INTERPRET", ["rising line", "positive direction", "constant velocity"], width=5.25, height=1.75)
        interpretation.next_to(eqs, DOWN, buff=0.34)
        self.play(Create(axes), Write(labels), Create(graph), FadeIn(dots), Write(coord), run_time=RUN_SLOW)
        for eq in eqs:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.55)
        box = SurroundingRectangle(eqs[-1], buff=0.16, color=BLACK_LINE, stroke_width=2)
        self.play(Create(box), FadeIn(interpretation), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def rest_example(self) -> None:
        self.set_header(4, "EXAMPLE B: REST", "A horizontal position-time line does not mean x=0. It means position does not change.")
        axes = self.position_axes(x_max=4, y_max=10, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        pts = [(0, 6), (4, 6)]
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        pos_label = self.math(r"x=6\,\mathrm{m}", 25).next_to(graph, UP, buff=0.12)
        eqs = VGroup(
            self.math(r"\Delta x=6-6=0\,\mathrm{m}", 33),
            self.math(r"v=\frac{0}{4}=0\,\mathrm{m/s}", 38),
        ).arrange(DOWN, buff=0.34).move_to(RIGHT * 4.30 + UP * 0.40)
        compare = VGroup(
            self.card("ZERO VELOCITY", ["position is constant", "the object is at rest"], width=5.5, height=1.65),
            self.card("NOT ZERO POSITION", ["the object remains", "at x=6 m"], width=5.5, height=1.65),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.30 + DOWN * 1.85)
        self.play(Create(axes), Write(labels), Create(graph), FadeIn(dots), Write(pos_label), run_time=RUN_SLOW)
        self.play(Write(eqs[0]), Write(eqs[1]), run_time=RUN_SLOW)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.08) for c in compare], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def negative_example(self) -> None:
        self.set_header(5, "EXAMPLE C: NEGATIVE VELOCITY", "When position decreases as time increases, the slope and velocity are negative.")
        axes = self.position_axes(x_max=5, y_max=14, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        pts = [(1, 12), (5, 4)]
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        coords = VGroup(
            self.coordinate_label(axes, pts[0], r"(1,12)", UR),
            self.coordinate_label(axes, pts[1], r"(5,4)", UL),
        )
        eqs = VGroup(
            self.math(r"\Delta x=4-12=-8\,\mathrm{m}", 31),
            self.math(r"\Delta t=5-1=4\,\mathrm{s}", 31),
            self.math(r"v=\frac{-8}{4}=-2\,\mathrm{m/s}", 36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 4.30 + DOWN * 0.45)
        note = self.card("THE SIGN MATTERS", ["falling line", "negative direction", "speed = 2 m/s"], width=5.25, height=1.75)
        note.next_to(eqs, DOWN, buff=0.34)
        self.play(Create(axes), Write(labels), Create(graph), FadeIn(dots), Write(coords), run_time=RUN_SLOW)
        for eq in eqs:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.55)
        self.play(Create(SurroundingRectangle(eqs[-1], buff=0.16, color=BLACK_LINE)), FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def compare_speeds(self) -> None:
        self.set_header(6, "COMPARE SPEEDS BY STEEPNESS", "On the same axes and time scale, the steeper position-time line has greater speed.")
        axes = self.position_axes(x_max=2, y_max=12, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        a_line = self.polyline(axes, [(0, 0), (2, 10)], BLACK_LINE, 3.5)
        b_line = self.polyline(axes, [(0, 0), (2, 6)], DARK_GRAY, 3.2)
        a_tag = self.text("A", 23, BOLD).next_to(axes.c2p(1.55, 7.75), UL, buff=0.05)
        b_tag = self.text("B", 23, BOLD).next_to(axes.c2p(1.55, 4.65), DL, buff=0.05)
        calculations = VGroup(
            self.result_chip(r"v_A=\frac{10}{2}=5\,\mathrm{m/s}", 5.2, 32),
            self.result_chip(r"v_B=\frac{6}{2}=3\,\mathrm{m/s}", 5.2, 32),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 4.35 + UP * 0.55)
        conclusion = self.card("CONCLUSION", ["A is steeper", "A has greater speed", "5 m/s > 3 m/s"], width=5.25, height=1.90)
        conclusion.move_to(RIGHT * 4.35 + DOWN * 1.85)
        self.play(Create(axes), Write(labels), Create(a_line), Write(a_tag), run_time=RUN_SLOW)
        self.play(Create(b_line), Write(b_tag), run_time=RUN_SLOW)
        self.play(FadeIn(calculations[0]), FadeIn(calculations[1]), run_time=RUN_NORMAL)
        highlight = SurroundingRectangle(VGroup(a_line, a_tag), buff=0.12, color=MID_GRAY, stroke_width=2)
        self.play(Create(highlight), FadeIn(conclusion, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def piecewise_calculation(self) -> None:
        self.set_header(7, "PIECEWISE POSITION GRAPH", "Calculate one slope for each straight segment. A change in slope means a change in velocity.")
        pts = self.PIECEWISE_POINTS
        axes = self.position_axes(x_max=7, y_max=10, position=LEFT * 3.35 + DOWN * 0.50, x_length=7.0)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        seg_labels = VGroup(
            self.text("I", 21, BOLD).move_to(axes.c2p(1.0, 4.5)),
            self.text("II", 21, BOLD).move_to(axes.c2p(3.5, 8.55)),
            self.text("III", 21, BOLD).move_to(axes.c2p(6.0, 5.4)),
        )
        table = self.build_table(
            ["segment", r"\Delta t", r"\Delta x", r"v=\Delta x/\Delta t"],
            [["I", r"2\,s", r"+8\,m", r"+4\,m/s"],
             ["II", r"3\,s", r"0\,m", r"0\,m/s"],
             ["III", r"2\,s", r"-6\,m", r"-3\,m/s"]],
            [1.25, 1.45, 1.55, 2.35], math_columns=(1, 2, 3),
            row_height=0.72, header_height=0.78, body_font_size=25, header_font_size=21,
        )
        table.group.move_to(RIGHT * 4.05 + DOWN * 0.20)
        self.play(Create(axes), Write(labels), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Create(s) for s in graph], lag_ratio=0.20), FadeIn(dots), Write(seg_labels), run_time=RUN_SLOW)
        self.play(FadeIn(table.header), run_time=RUN_NORMAL)
        for row in table.rows[1:]:
            self.play(FadeIn(row, shift=LEFT * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        takeaway = self.result_chip(r"+4\;\longrightarrow\;0\;\longrightarrow\;-3\;\mathrm{m/s}", 6.0, 32)
        takeaway.next_to(table.group, DOWN, buff=0.35)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def matching_velocity_graph(self) -> None:
        self.set_header(8, "BUILD THE MATCHING v–t GRAPH", "Each x-t segment becomes one horizontal velocity level over the same time interval.")
        pts = self.PIECEWISE_POINTS
        x_axes = self.position_axes(x_max=7, y_max=10, position=LEFT * 3.65 + DOWN * 0.55, x_length=6.4, y_length=4.45)
        x_labels = self.axis_labels(x_axes, r"x\;(\mathrm{m})")
        x_graph = self.polyline(x_axes, pts)
        v_axes = self.velocity_axes(position=RIGHT * 3.65 + DOWN * 0.55)
        v_labels = self.axis_labels(v_axes, r"v\;(\mathrm{m/s})")
        guides = self.interval_guides(v_axes, [2, 5], -4, 5)
        v_lines = VGroup(
            Line(v_axes.c2p(0, 4), v_axes.c2p(2, 4), color=BLACK_LINE, stroke_width=3.4),
            Line(v_axes.c2p(2, 0), v_axes.c2p(5, 0), color=BLACK_LINE, stroke_width=3.4),
            Line(v_axes.c2p(5, -3), v_axes.c2p(7, -3), color=BLACK_LINE, stroke_width=3.4),
        )
        v_tags = VGroup(
            self.math(r"+4", 24).next_to(v_lines[0], UP, buff=0.08),
            self.math(r"0", 24).next_to(v_lines[1], UP, buff=0.08),
            self.math(r"-3", 24).next_to(v_lines[2], DOWN, buff=0.08),
        )
        arrow = Arrow(LEFT * 0.55, RIGHT * 0.55, color=MID_GRAY, stroke_width=2.2)
        arrow_label = self.text("SLOPE → HEIGHT", 17, BOLD).next_to(arrow, UP, buff=0.08)
        self.play(Create(x_axes), Write(x_labels), Create(x_graph), run_time=RUN_SLOW)
        self.play(GrowArrow(arrow), Write(arrow_label), Create(v_axes), Write(v_labels), Create(guides), run_time=RUN_SLOW)
        for line, tag in zip(v_lines, v_tags):
            self.play(Create(line), Write(tag), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def workshop_problem_one(self) -> None:
        self.set_header(9, "WORKSHOP PROBLEM 1", "The graph connects (0 s, 1 m) and (3 s, 10 m). Calculate velocity and interpret its sign.")
        axes = self.position_axes(x_max=3, y_max=12, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        pts = [(0, 1), (3, 10)]
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        prompt = self.card("YOUR TURN", ["write coordinates", "calculate Dx and Dt", "divide and keep sign"], width=5.5, height=2.0)
        prompt.move_to(RIGHT * 4.30 + UP * 0.85)
        self.play(Create(axes), Write(labels), Create(graph), FadeIn(dots), FadeIn(prompt), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK * 1.55)
        solution = VGroup(
            self.math(r"\Delta x=10-1=9\,\mathrm{m}", 31),
            self.math(r"\Delta t=3-0=3\,\mathrm{s}", 31),
            self.result_chip(r"v=\frac{9}{3}=+3\,\mathrm{m/s}", 5.3, 34),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.30 + DOWN * 1.35)
        for item in solution:
            self.play(Write(item) if isinstance(item, MathTex) else FadeIn(item), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.45)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def workshop_problem_two(self) -> None:
        self.set_header(10, "WORKSHOP PROBLEM 2", "Calculate the three segment velocities, identify rest and backward motion, then build v-t.")
        pts = [(0, 2), (2, 8), (4, 8), (6, 0)]
        x_axes = self.position_axes(x_max=6, y_max=10, position=LEFT * 3.65 + DOWN * 0.55, x_length=6.4, y_length=4.45)
        x_labels = self.axis_labels(x_axes, r"x\;(\mathrm{m})")
        x_graph = self.polyline(x_axes, pts)
        x_dots = self.dots(x_axes, pts)
        v_axes = self.velocity_axes(x_max=6, y_min=-5, y_max=4, position=RIGHT * 3.65 + DOWN * 0.55, x_length=6.3)
        v_labels = self.axis_labels(v_axes, r"v\;(\mathrm{m/s})")
        question = self.card("PAUSE AND SOLVE", ["segment I", "segment II", "segment III"], width=4.6, height=1.55)
        question.move_to(RIGHT * 3.65 + UP * 1.85)
        self.play(Create(x_axes), Write(x_labels), Create(x_graph), FadeIn(x_dots), run_time=RUN_SLOW)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK * 1.60)
        calculations = VGroup(
            self.math(r"v_1=\frac{8-2}{2-0}=+3", 24),
            self.math(r"v_2=\frac{8-8}{4-2}=0", 24),
            self.math(r"v_3=\frac{0-8}{6-4}=-4", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.65 + UP * 0.95)
        self.play(FadeOut(question), Write(calculations), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(calculations), Create(v_axes), Write(v_labels), run_time=RUN_SLOW)
        guides = self.interval_guides(v_axes, [2, 4], -5, 4)
        v_lines = VGroup(
            Line(v_axes.c2p(0, 3), v_axes.c2p(2, 3), color=BLACK_LINE, stroke_width=3.3),
            Line(v_axes.c2p(2, 0), v_axes.c2p(4, 0), color=BLACK_LINE, stroke_width=3.3),
            Line(v_axes.c2p(4, -4), v_axes.c2p(6, -4), color=BLACK_LINE, stroke_width=3.3),
        )
        self.play(Create(guides), run_time=RUN_QUICK)
        for line in v_lines:
            self.play(Create(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def whole_trip_average(self) -> None:
        self.set_header(11, "WHOLE-TRIP AVERAGE VELOCITY", "For the complete trip, use total displacement divided by total time, not an unweighted mean of slopes.")
        pts = self.PIECEWISE_POINTS
        axes = self.position_axes(x_max=7, y_max=10, position=LEFT * 3.0 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        graph = self.polyline(axes, pts)
        dots = self.dots(axes, pts)
        first = self.coordinate_label(axes, pts[0], r"(0,0)", UR)
        last = self.coordinate_label(axes, pts[-1], r"(7,2)", DR)
        solution = VGroup(
            self.text("USE ONLY THE FIRST AND FINAL POINTS", 23, BOLD),
            self.math(r"\Delta x_{\mathrm{total}}=2-0=2\,\mathrm{m}", 30),
            self.math(r"\Delta t_{\mathrm{total}}=7-0=7\,\mathrm{s}", 30),
            self.result_chip(r"v_{\mathrm{avg}}=\frac{2}{7}\,\mathrm{m/s}\approx0.286\,\mathrm{m/s}", 6.2, 29),
        ).arrange(DOWN, buff=0.27).move_to(RIGHT * 4.30 + DOWN * 0.50)
        note = self.card("WHY NOT (4+0-3)/3?", ["segments have different durations", "whole-trip average uses totals"], width=5.8, height=1.65)
        note.next_to(solution, DOWN, buff=0.32)
        self.play(Create(axes), Write(labels), Create(graph), FadeIn(dots), Write(first), Write(last), run_time=RUN_SLOW)
        for item in solution:
            self.play(Write(item) if isinstance(item, (Text, MathTex)) else FadeIn(item), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.50)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def final_recipe(self) -> None:
        self.set_header(12, "FINAL RECIPE", "Repeat the same method on every straight position-time segment.")
        recipe = self.process_map(
            [("1", "Choose two points"), ("2", "Calculate Dx"), ("3", "Calculate Dt"),
             ("4", "Divide and keep sign"), ("5", "Draw the v-t level")],
            card_width=4.15, card_height=1.16, columns=3,
        ).move_to(UP * 0.40)
        sign_map = VGroup(
            self.card("RISING", ["positive slope", "positive velocity"], width=4.25, height=1.55),
            self.card("HORIZONTAL", ["zero slope", "zero velocity"], width=4.25, height=1.55),
            self.card("FALLING", ["negative slope", "negative velocity"], width=4.25, height=1.55),
        ).arrange(RIGHT, buff=0.30).move_to(DOWN * 2.15)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in recipe], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in sign_map], lag_ratio=0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)

    def construct(self) -> None:
        self.opening()
        self.workshop_map()
        self.slope_recipe()
        self.positive_example()
        self.rest_example()
        self.negative_example()
        self.compare_speeds()
        self.piecewise_calculation()
        self.matching_velocity_graph()
        self.workshop_problem_one()
        self.workshop_problem_two()
        self.whole_trip_average()
        self.final_recipe()
        self.standard_closing("On an x–t graph, velocity is the slope - not the height.")
