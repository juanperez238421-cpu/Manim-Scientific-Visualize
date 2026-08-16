#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Position–Time Graph — Senior ManimCE lesson.

Pedagogical sequence:
physical motion -> sampled data -> axes -> points -> connected graph ->
coordinate reading -> positive/zero/negative slope -> speed magnitude ->
graph-to-motion reconstruction -> curved graph preview -> reproducible method.

Target: ManimCE 0.20.1 + exact JP classroom style.
"""
from __future__ import annotations

import numpy as np
from manim import *

from jp_classroom_style import *


TIMES = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
POSITIONS = np.array([0, 1, 2, 3, 3, 3, 2, 1, 0], dtype=float)


def position_at(t: float) -> float:
    if t <= 3:
        return t
    if t <= 5:
        return 3.0
    return 8.0 - t


class PositionTimeGraphSenior(JPMathClassroomScene):
    """Complete senior lesson on how to construct and interpret an x-t graph."""

    def validate_lesson_data(self) -> None:
        assert len(TIMES) == len(POSITIONS)
        for t, x in zip(TIMES, POSITIONS):
            assert_close(position_at(float(t)), float(x), label=f"x({t})")
        assert_close((POSITIONS[3] - POSITIONS[0]) / (TIMES[3] - TIMES[0]), 1.0, label="segment A velocity")
        assert_close((POSITIONS[5] - POSITIONS[3]) / (TIMES[5] - TIMES[3]), 0.0, label="segment B velocity")
        assert_close((POSITIONS[8] - POSITIONS[5]) / (TIMES[8] - TIMES[5]), -1.0, label="segment C velocity")

    def construct(self) -> None:
        self.opening()
        self.scene_01_motion_story()
        self.scene_02_sample_data()
        self.scene_03_build_axes()
        self.scene_04_plot_points()
        self.scene_05_connect_points()
        self.scene_06_read_coordinates()
        self.scene_07_positive_slope()
        self.scene_08_zero_slope()
        self.scene_09_negative_slope()
        self.scene_10_compare_slopes()
        self.scene_11_graph_reconstructs_motion()
        self.scene_12_curved_graph_preview()
        self.scene_13_summary()

    # ------------------------------------------------------------------
    # Reusable lesson helpers
    # ------------------------------------------------------------------
    def raw_axes(self, *, x_length: float = 10.5, y_length: float = 5.1) -> Axes:
        return Axes(
            x_range=[0, 8.6, 1],
            y_range=[0, 3.7, 1],
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_ticks": True, "tick_size": 0.08},
            tips=True,
        )

    def graph_labels(self, axes: Axes) -> VGroup:
        x_label = VGroup(self.text("time", 22, BOLD), self.math("t", 27), self.text("(s)", 20)).arrange(RIGHT, buff=0.09)
        y_label = VGroup(self.text("position", 22, BOLD), self.math("x", 27), self.text("(m)", 20)).arrange(RIGHT, buff=0.09)
        x_label.next_to(axes.x_axis, DOWN, buff=0.26)
        y_label.rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.26)
        return VGroup(x_label, y_label)

    def make_data_graph(self, axes: Axes) -> VGroup:
        points = [axes.c2p(t, x) for t, x in zip(TIMES, POSITIONS)]
        segments = VGroup(*[
            Line(points[i], points[i + 1], color=BLACK_LINE, stroke_width=3.2)
            for i in range(len(points) - 1)
        ])
        dots = VGroup(*[Dot(point, radius=0.075, color=BLACK_LINE) for point in points])
        return VGroup(segments, dots)

    def dataset_table(self, compact: bool = False) -> TableDiagram:
        rows = [[f"{int(t)}", f"{int(x)}"] for t, x in zip(TIMES, POSITIONS)]
        return self.build_table(
            headers=("Time t (s)", "Position x (m)"),
            body_rows=rows,
            column_widths=(2.7, 3.0) if not compact else (2.15, 2.35),
            math_columns=(),
            row_height=0.46 if not compact else 0.39,
            header_height=0.62 if not compact else 0.52,
            body_font_size=21 if not compact else 18,
            header_font_size=21 if not compact else 18,
        )

    def state_tag(self, text_value: str, center: np.ndarray, width: float | None = None) -> VGroup:
        txt = self.text(text_value, 22, BOLD)
        w = width or max(2.15, txt.width + 0.45)
        box = RoundedRectangle(width=w, height=0.68, corner_radius=0.09, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1)
        self.fit(txt, w - 0.30, 0.43)
        txt.move_to(box)
        return VGroup(box, txt).move_to(center)

    def motion_track(self) -> VGroup:
        line = NumberLine(
            x_range=[0, 3.2, 1],
            length=10.8,
            color=BLACK_LINE,
            stroke_width=2.3,
            include_ticks=True,
            include_numbers=False,
            include_tip=True,
        )
        labels = VGroup(*[
            self.math(str(x), 25).next_to(line.n2p(x), DOWN, buff=0.17)
            for x in range(4)
        ])
        origin = self.text("origin", 19, BOLD).next_to(line.n2p(0), UP, buff=0.13)
        xlabel = VGroup(self.text("position", 20, BOLD), self.math("x", 25), self.text("(m)", 19)).arrange(RIGHT, buff=0.08)
        xlabel.next_to(line, DOWN, buff=0.62)
        return VGroup(line, labels, origin, xlabel)

    def slope_triangle(self, axes: Axes, t0: float, x0: float, t1: float, x1: float) -> VGroup:
        run = DashedLine(axes.c2p(t0, x0), axes.c2p(t1, x0), color=MID_GRAY, stroke_width=2.0)
        rise = DashedLine(axes.c2p(t1, x0), axes.c2p(t1, x1), color=MID_GRAY, stroke_width=2.0)
        run_lab = self.math(rf"\Delta t={int(t1-t0)}\,\mathrm{{s}}", 25).next_to(run, DOWN, buff=0.11)
        dx = x1 - x0
        sign = "+" if dx > 0 else ""
        rise_lab = self.math(rf"\Delta x={sign}{int(dx)}\,\mathrm{{m}}", 25).next_to(rise, RIGHT, buff=0.11)
        return VGroup(run, rise, run_lab, rise_lab)

    def mini_note(self, title: str, lines: list[str], center: np.ndarray, width: float = 5.2) -> VGroup:
        note = self.note_panel(title, lines, width=width, title_size=24, body_size=21)
        return note.move_to(center)

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "MOTION • POSITION–TIME GRAPHS",
            "HOW TO BUILD AND READ AN x–t GRAPH",
            "From a moving object to a data table, then from the table to the graph.",
            "Visualize first. Plot carefully. Read the slope as motion.",
        )

    # ------------------------------------------------------------------
    # 01 — Physical motion before graphing
    # ------------------------------------------------------------------
    def scene_01_motion_story(self) -> None:
        self.set_header(
            1,
            "START WITH THE PHYSICAL MOTION",
            "Before drawing a graph, watch the object move along a one-dimensional position axis.",
        )

        track = self.motion_track()
        track.move_to(DOWN * 0.65)
        number_line = track[0]
        walker = Dot(number_line.n2p(0), radius=0.16, color=BLACK_LINE)
        walker_label = self.text("object", 22, BOLD).next_to(walker, UP, buff=0.18)

        time_label = self.text("time", 19, BOLD)
        time_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color=BLACK)
        time_unit = self.text("s", 20, BOLD)
        time_readout = VGroup(time_label, time_num, time_unit).arrange(RIGHT, buff=0.12)
        time_box = RoundedRectangle(width=3.2, height=0.90, corner_radius=0.10, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1)
        time_readout.move_to(time_box)
        clock = VGroup(time_box, time_readout).move_to(LEFT * 4.9 + UP * 1.65)

        pos_label = self.text("position", 19, BOLD)
        pos_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color=BLACK)
        pos_unit = self.text("m", 20, BOLD)
        pos_readout = VGroup(pos_label, pos_num, pos_unit).arrange(RIGHT, buff=0.12)
        pos_box = RoundedRectangle(width=3.2, height=0.90, corner_radius=0.10, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1)
        pos_readout.move_to(pos_box)
        position_card = VGroup(pos_box, pos_readout).move_to(RIGHT * 4.9 + UP * 1.65)

        question = self.note_panel(
            "WATCH THE STORY",
            [
                "0–3 s: move away from the origin",
                "3–5 s: stay at the same position",
                "5–8 s: return toward the origin",
            ],
            width=7.2,
            title_size=25,
            body_size=22,
        )
        question.move_to(UP * 1.03)

        stage = VGroup(track, walker, walker_label, clock, position_card, question)
        self.assert_content_safe(stage, "motion story")

        self.play(FadeIn(question), Create(number_line), FadeIn(track[1:]), FadeIn(clock), FadeIn(position_card), run_time=RUN_NORMAL)
        self.play(FadeIn(walker), FadeIn(walker_label), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        for t, x in zip(TIMES[1:], POSITIONS[1:]):
            target = number_line.n2p(x)
            self.play(
                walker.animate.move_to(target),
                walker_label.animate.next_to(target, UP, buff=0.18),
                ChangeDecimalToValue(time_num, t),
                ChangeDecimalToValue(pos_num, x),
                run_time=0.85,
                rate_func=smooth,
            )
            self.wait(PAUSE_SHORT * 0.40)

        idea = self.formula_panel(r"x=x(t)", width=4.2, height=1.0, font_size=40)
        idea.move_to(DOWN * 2.55)
        self.play(FadeIn(idea), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 — Sample data
    # ------------------------------------------------------------------
    def scene_02_sample_data(self) -> None:
        self.set_header(
            2,
            "TURN THE MOTION INTO DATA",
            "At equal time intervals, record the object's position. Each measurement becomes one ordered pair (t, x).",
        )

        table = self.dataset_table(compact=False)
        table.group.move_to(LEFT * 3.55 + DOWN * 0.50)

        explanation = self.note_panel(
            "HOW TO READ ONE ROW",
            [
                "At t = 2 s, the object is at x = 2 m.",
                "The ordered pair is (2, 2).",
                "Later, that pair becomes one point on the graph.",
            ],
            width=6.2,
            title_size=26,
            body_size=23,
        )
        explanation.move_to(RIGHT * 3.60 + UP * 0.15)

        pair = self.formula_panel(r"(t,x)=(2,2)", width=5.0, height=1.05, font_size=40)
        pair.move_to(RIGHT * 3.60 + DOWN * 2.15)
        group = VGroup(table.group, explanation, pair)
        self.assert_content_safe(group, "data table layout")

        self.animate_table_rows(table, include_header=True, pause=0.35)
        self.play(self.shade_cells(table, [(3, 0), (3, 1)]), run_time=RUN_QUICK)
        self.play(FadeIn(explanation), FadeIn(pair), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — Build axes
    # ------------------------------------------------------------------
    def scene_03_build_axes(self) -> None:
        self.set_header(
            3,
            "BUILD THE COORDINATE SYSTEM",
            "Time is the independent variable, so it goes on the horizontal axis. Position goes on the vertical axis.",
        )

        axes = self.raw_axes().move_to(DOWN * 0.55)
        x_label, y_label = self.graph_labels(axes)
        horizontal = self.state_tag("HORIZONTAL → TIME", LEFT * 4.6 + UP * 1.75, 3.7)
        vertical = self.state_tag("VERTICAL → POSITION", RIGHT * 4.6 + UP * 1.75, 4.3)
        origin_label = self.text("origin  (0,0)", 22, BOLD).next_to(axes.c2p(0, 0), UR, buff=0.12)

        self.play(Create(axes.x_axis), FadeIn(horizontal), run_time=RUN_NORMAL)
        self.play(FadeIn(x_label), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        self.play(Create(axes.y_axis), FadeIn(vertical), run_time=RUN_NORMAL)
        self.play(FadeIn(y_label), FadeIn(origin_label), run_time=RUN_QUICK)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — Plot ordered pairs one by one
    # ------------------------------------------------------------------
    def scene_04_plot_points(self) -> None:
        self.set_header(
            4,
            "PLOT EACH ORDERED PAIR",
            "Use the table as a checklist. For every measurement, move across to the time and up to the position.",
        )

        table = self.dataset_table(compact=True)
        table.group.move_to(LEFT * 5.0 + DOWN * 0.60)
        axes = self.raw_axes(x_length=8.0, y_length=4.85).move_to(RIGHT * 2.15 + DOWN * 0.55)
        labels = self.graph_labels(axes)
        self.play(FadeIn(table.group), Create(axes), FadeIn(labels), run_time=RUN_NORMAL)

        plotted = VGroup()
        for i, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            row_index = i + 1
            self.play(
                table.rectangles[row_index][0].animate.set_fill(LIGHT_GRAY, opacity=1),
                table.rectangles[row_index][1].animate.set_fill(LIGHT_GRAY, opacity=1),
                run_time=0.25,
            )
            guide_v = DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.6)
            guide_h = DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.6)
            dot = Dot(axes.c2p(t, x), radius=0.095, color=BLACK)
            coordinate = self.math(rf"({int(t)},{int(x)})", 25).next_to(dot, UR, buff=0.10)
            self.play(Create(guide_v), Create(guide_h), FadeIn(dot), FadeIn(coordinate), run_time=0.45)
            self.wait(0.18)
            self.play(FadeOut(VGroup(guide_v, guide_h, coordinate)), run_time=0.20)
            plotted.add(dot)
            self.play(
                table.rectangles[row_index][0].animate.set_fill(WHITE, opacity=1),
                table.rectangles[row_index][1].animate.set_fill(WHITE, opacity=1),
                run_time=0.14,
            )

        final_note = self.note_panel(
            "CHECK BEFORE CONNECTING",
            ["Every row in the table now has exactly one point on the graph."],
            width=8.2,
            title_size=24,
            body_size=22,
        ).move_to(RIGHT * 2.0 + DOWN * 3.10)
        self.play(FadeIn(final_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — Connect points and trace motion
    # ------------------------------------------------------------------
    def scene_05_connect_points(self) -> None:
        self.set_header(
            5,
            "CONNECT THE POINTS — THE GRAPH BECOMES A STORY",
            "The line shows how position changes continuously while time moves from left to right.",
        )

        axes = self.raw_axes(x_length=10.4, y_length=5.15).move_to(DOWN * 0.45)
        labels = self.graph_labels(axes)
        dots = VGroup(*[Dot(axes.c2p(t, x), radius=0.08, color=BLACK) for t, x in zip(TIMES, POSITIONS)])
        self.play(Create(axes), FadeIn(labels), FadeIn(dots), run_time=RUN_NORMAL)

        cursor = Dot(axes.c2p(TIMES[0], POSITIONS[0]), radius=0.12, color=BLACK)
        t_num = DecimalNumber(0, num_decimal_places=0, color=BLACK, font_size=30)
        x_num = DecimalNumber(0, num_decimal_places=0, color=BLACK, font_size=30)
        readout = VGroup(
            self.text("t =", 21, BOLD), t_num, self.text("s", 19, BOLD),
            self.text("   x =", 21, BOLD), x_num, self.text("m", 19, BOLD),
        ).arrange(RIGHT, buff=0.08).move_to(UP * 1.90)
        self.play(FadeIn(cursor), FadeIn(readout), run_time=RUN_QUICK)

        segments = VGroup()
        for i in range(len(TIMES) - 1):
            segment = Line(
                axes.c2p(TIMES[i], POSITIONS[i]),
                axes.c2p(TIMES[i + 1], POSITIONS[i + 1]),
                color=BLACK_LINE,
                stroke_width=3.3,
            )
            segments.add(segment)
            self.play(
                Create(segment),
                cursor.animate.move_to(axes.c2p(TIMES[i + 1], POSITIONS[i + 1])),
                ChangeDecimalToValue(t_num, TIMES[i + 1]),
                ChangeDecimalToValue(x_num, POSITIONS[i + 1]),
                run_time=0.75,
                rate_func=linear,
            )
            self.wait(0.18)

        conclusion = self.formula_panel(r"\text{graph}=\text{position as a function of time}", width=9.4, height=1.0, font_size=32)
        conclusion.move_to(UP * 1.88)
        self.play(FadeOut(readout), FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — Read coordinates
    # ------------------------------------------------------------------
    def scene_06_read_coordinates(self) -> None:
        self.set_header(
            6,
            "READ A POINT FROM THE GRAPH",
            "To answer 'Where is the object at a certain time?', start at the time axis and project to the graph.",
        )

        axes = self.raw_axes(x_length=10.3, y_length=5.1).move_to(DOWN * 0.45)
        labels = self.graph_labels(axes)
        graph = self.make_data_graph(axes)
        self.play(Create(axes), FadeIn(labels), Create(graph[0]), FadeIn(graph[1]), run_time=RUN_NORMAL)

        t = 6.0
        x = 2.0
        vertical = DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY, stroke_width=2.0)
        horizontal = DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY, stroke_width=2.0)
        point = Dot(axes.c2p(t, x), radius=0.14, color=BLACK)
        t_tag = self.state_tag("1. FIND t = 6 s", LEFT * 4.55 + UP * 1.75)
        x_tag = self.state_tag("2. READ x = 2 m", RIGHT * 4.55 + UP * 1.75)

        self.play(FadeIn(t_tag), Create(vertical), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(point), Create(horizontal), FadeIn(x_tag), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        answer = self.formula_panel(r"x(6\,\mathrm{s})=2\,\mathrm{m}", width=6.6, height=1.05, font_size=40)
        answer.move_to(UP * 1.72)
        self.play(FadeOut(VGroup(t_tag, x_tag)), FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — Positive slope
    # ------------------------------------------------------------------
    def scene_07_positive_slope(self) -> None:
        self.set_header(7, "POSITIVE SLOPE → POSITIVE VELOCITY", "From 0 s to 3 s the object moves away from the origin at a constant rate.")
        axes = self.raw_axes(x_length=9.0, y_length=4.55).move_to(LEFT * 2.65 + DOWN * 0.55)
        labels = self.graph_labels(axes); graph = self.make_data_graph(axes)
        self.play(Create(axes), FadeIn(labels), Create(graph[0]), FadeIn(graph[1]), run_time=RUN_NORMAL)
        triangle = self.slope_triangle(axes, 0, 0, 3, 3)
        self.play(Create(triangle[0]), Create(triangle[1]), FadeIn(triangle[2:]), run_time=RUN_NORMAL)
        formula = self.formula_panel(r"v_{\mathrm{avg}}=\frac{\Delta x}{\Delta t}", width=4.8, height=1.0, font_size=36).move_to(RIGHT * 4.7 + UP * 0.75)
        result = self.formula_panel(r"v=\frac{3-0}{3-0}=+1\,\mathrm{m/s}", width=5.4, height=1.0, font_size=34).move_to(RIGHT * 4.7 + DOWN * 0.45)
        note = self.mini_note("INTERPRETATION", ["Position increases as time increases.", "The object moves in the +x direction."], RIGHT * 4.7 + DOWN * 2.10, 5.4)
        self.play(FadeIn(formula), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(result), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — Zero slope
    # ------------------------------------------------------------------
    def scene_08_zero_slope(self) -> None:
        self.set_header(8, "ZERO SLOPE → THE OBJECT IS AT REST", "From 3 s to 5 s time continues, but position stays at 3 m.")
        axes = self.raw_axes(x_length=9.0, y_length=4.55).move_to(LEFT * 2.65 + DOWN * 0.55)
        labels = self.graph_labels(axes); graph = self.make_data_graph(axes)
        self.play(Create(axes), FadeIn(labels), Create(graph[0]), FadeIn(graph[1]), run_time=RUN_NORMAL)
        run = DashedLine(axes.c2p(3, 3), axes.c2p(5, 3), color=MID_GRAY, stroke_width=2)
        dt = self.math(r"\Delta t=2\,\mathrm{s}", 26).next_to(run, DOWN, buff=0.20)
        dx = self.math(r"\Delta x=0", 28).next_to(run, UP, buff=0.16)
        self.play(Create(run), FadeIn(dt), FadeIn(dx), run_time=RUN_NORMAL)
        result = self.formula_panel(r"v=\frac{3-3}{5-3}=0\,\mathrm{m/s}", width=5.4, height=1.0, font_size=34).move_to(RIGHT * 4.7 + UP * 0.35)
        note = self.mini_note("INTERPRETATION", ["Same position for several seconds.", "A horizontal x–t line means no motion."], RIGHT * 4.7 + DOWN * 1.60, 5.4)
        self.play(FadeIn(result), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — Negative slope
    # ------------------------------------------------------------------
    def scene_09_negative_slope(self) -> None:
        self.set_header(9, "NEGATIVE SLOPE → NEGATIVE VELOCITY", "From 5 s to 8 s the position decreases, so the object moves back toward the origin.")
        axes = self.raw_axes(x_length=9.0, y_length=4.55).move_to(LEFT * 2.65 + DOWN * 0.55)
        labels = self.graph_labels(axes); graph = self.make_data_graph(axes)
        self.play(Create(axes), FadeIn(labels), Create(graph[0]), FadeIn(graph[1]), run_time=RUN_NORMAL)
        triangle = self.slope_triangle(axes, 5, 3, 8, 0)
        self.play(Create(triangle[0]), Create(triangle[1]), FadeIn(triangle[2:]), run_time=RUN_NORMAL)
        result = self.formula_panel(r"v=\frac{0-3}{8-5}=-1\,\mathrm{m/s}", width=5.4, height=1.0, font_size=34).move_to(RIGHT * 4.7 + UP * 0.35)
        note = self.mini_note("INTERPRETATION", ["Position decreases as time increases.", "The minus sign tells us the direction."], RIGHT * 4.7 + DOWN * 1.60, 5.4)
        self.play(FadeIn(result), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 — Compare steepness and speed
    # ------------------------------------------------------------------
    def scene_10_compare_slopes(self) -> None:
        self.set_header(10, "STEEPER SLOPE → LARGER SPEED", "The sign tells direction. The magnitude of the slope tells how fast position changes.")
        axes = Axes(x_range=[0, 4.5, 1], y_range=[0, 8.5, 2], x_length=7.2, y_length=5.0, axis_config={"color": BLACK_LINE, "stroke_width": 2}, tips=True).move_to(LEFT * 3.0 + DOWN * 0.45)
        labels = VGroup(self.text("time (s)", 21, BOLD).next_to(axes.x_axis, DOWN, buff=0.22), self.text("position (m)", 21, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.22))
        g1 = axes.plot(lambda t: t, x_range=[0, 4], color=MID_GRAY, stroke_width=3)
        g2 = axes.plot(lambda t: 2*t, x_range=[0, 4], color=BLACK_LINE, stroke_width=4)
        l1 = self.text("1 m/s", 22, BOLD).next_to(g1.get_end(), RIGHT, buff=0.15)
        l2 = self.text("2 m/s", 22, BOLD).next_to(g2.get_end(), RIGHT, buff=0.15)
        note = self.mini_note("COMPARE THE LINES", ["Both slopes are positive → both move in +x.", "The 2 m/s line rises twice as much in the same time.", "Therefore it is steeper and represents faster motion."], RIGHT * 4.25 + UP * 0.45, 6.0)
        relation = self.formula_panel(r"|\mathrm{slope}|\uparrow\quad\Rightarrow\quad \mathrm{speed}\uparrow", width=6.0, height=1.05, font_size=34).move_to(RIGHT * 4.25 + DOWN * 2.15)
        self.play(Create(axes), FadeIn(labels), run_time=RUN_NORMAL)
        self.play(Create(g1), FadeIn(l1), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(Create(g2), FadeIn(l2), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(note), FadeIn(relation), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 11 — Graph reconstructs physical motion
    # ------------------------------------------------------------------
    def scene_11_graph_reconstructs_motion(self) -> None:
        self.set_header(11, "MAKE THE GRAPH MOVE AGAIN", "A good x–t graph should let you reconstruct the physical motion without seeing the original experiment.")
        number_line = NumberLine(x_range=[0, 3.2, 1], length=6.0, color=BLACK_LINE, stroke_width=2.0, include_ticks=True, include_numbers=False, include_tip=True).move_to(LEFT * 4.25 + DOWN * 0.65)
        track_lab = self.text("physical position", 21, BOLD).next_to(number_line, DOWN, buff=0.40)
        walker = Dot(number_line.n2p(0), radius=0.14, color=BLACK); walker_lab = self.text("object", 19, BOLD).next_to(walker, UP, buff=0.14)
        axes = self.raw_axes(x_length=7.3, y_length=4.15).move_to(RIGHT * 3.15 + DOWN * 0.65)
        labels = self.graph_labels(axes); graph = self.make_data_graph(axes)
        cursor = Dot(axes.c2p(0, 0), radius=0.12, color=BLACK)
        vertical = always_redraw(lambda: DashedLine(axes.c2p(self._story_t.get_value(), 0), axes.c2p(self._story_t.get_value(), position_at(self._story_t.get_value())), color=MID_GRAY, stroke_width=1.6))
        self._story_t = ValueTracker(0)
        tnum = DecimalNumber(0, num_decimal_places=1, font_size=27, color=BLACK); tnum.add_updater(lambda m: m.set_value(self._story_t.get_value()))
        tag = VGroup(self.text("t =", 20, BOLD), tnum, self.text("s", 18, BOLD)).arrange(RIGHT, buff=0.08).move_to(RIGHT * 3.15 + UP * 1.72)
        phase = self.state_tag("MOVE AWAY", LEFT * 4.25 + UP * 1.72, 2.8)
        self.play(Create(number_line), FadeIn(track_lab), FadeIn(walker), FadeIn(walker_lab), Create(axes), FadeIn(labels), Create(graph[0]), FadeIn(graph[1]), FadeIn(cursor), FadeIn(tag), FadeIn(phase), run_time=RUN_NORMAL)
        self.add(vertical)
        checkpoints = [(3, "MOVE AWAY"), (5, "REST"), (8, "RETURN")]
        previous = 0.0
        for target_t, text_value in checkpoints:
            target_phase = self.state_tag(text_value, LEFT * 4.25 + UP * 1.72, 2.8)
            self.play(Transform(phase, target_phase), run_time=RUN_QUICK)
            steps = 20
            for j in range(1, steps + 1):
                tt = previous + (target_t - previous) * j / steps
                xx = position_at(tt)
                self._story_t.set_value(tt)
                walker.move_to(number_line.n2p(xx)); walker_lab.next_to(walker, UP, buff=0.14); cursor.move_to(axes.c2p(tt, xx))
                self.wait((target_t - previous) / steps * 0.22)
            previous = float(target_t)
        bridge = self.formula_panel(r"x\!-\!t\ \mathrm{graph}\quad\Longleftrightarrow\quad\mathrm{motion\ story}", width=7.8, height=1.0, font_size=34).move_to(DOWN * 3.10)
        self.play(FadeIn(bridge), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 12 — Curved graph preview
    # ------------------------------------------------------------------
    def scene_12_curved_graph_preview(self) -> None:
        self.set_header(12, "WHAT IF THE POSITION–TIME GRAPH IS CURVED?", "A changing slope means the velocity is changing. The tangent line gives the slope at one instant.")
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 10, 2], x_length=9.2, y_length=5.2, axis_config={"color": BLACK_LINE, "stroke_width": 2}, tips=True).move_to(LEFT * 2.15 + DOWN * 0.50)
        labels = VGroup(self.text("time (s)", 21, BOLD).next_to(axes.x_axis, DOWN, buff=0.22), self.text("position (m)", 21, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.22))
        curve = axes.plot(lambda t: 0.25*t*t, x_range=[0, 6], color=BLACK_LINE, stroke_width=3.3)
        t0=3.5; x0=0.25*t0*t0; slope=0.5*t0
        tangent=Line(axes.c2p(t0-1.5, x0-slope*1.5), axes.c2p(t0+1.5, x0+slope*1.5), color=MID_GRAY, stroke_width=2.8)
        point=Dot(axes.c2p(t0,x0), radius=0.13, color=BLACK)
        note=self.mini_note("PREVIEW", ["Straight segment → constant slope → constant velocity.", "Curved segment → changing slope → changing velocity.", "At one instant, use the tangent slope."], RIGHT * 4.65 + UP * 0.45, 5.8)
        formula=self.formula_panel(r"v\ \approx\ \mathrm{slope\ of\ the\ tangent}", width=5.8, height=1.05, font_size=31).move_to(RIGHT * 4.65 + DOWN * 2.10)
        self.play(Create(axes), FadeIn(labels), run_time=RUN_NORMAL); self.play(Create(curve), run_time=RUN_SLOW); self.wait(PAUSE_READ)
        self.play(FadeIn(point), Create(tangent), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note), FadeIn(formula), run_time=RUN_NORMAL); self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 13 — Summary method map
    # ------------------------------------------------------------------
    def scene_13_summary(self) -> None:
        self.set_header(13, "A REPRODUCIBLE METHOD FOR ANY POSITION–TIME GRAPH", "Use the same sequence every time: identify variables, plot carefully, then interpret position and slope.")
        route = self.process_map([
            ("1", "WATCH / READ MOTION"), ("2", "RECORD (t, x) DATA"), ("3", "DRAW AXES + UNITS"),
            ("4", "PLOT EACH POINT"), ("5", "CONNECT / TRACE"), ("6", "READ COORDINATES"),
            ("7", "FIND SLOPE"), ("8", "INTERPRET VELOCITY"), ("9", "TELL THE MOTION STORY"),
        ], card_width=4.45, card_height=1.0, columns=3)
        route.move_to(UP * 0.05)
        self.fit(route, 14.1, 4.55)
        formula = self.formula_panel(r"\text{slope of an }x\!-\!t\text{ graph}=\frac{\Delta x}{\Delta t}=\text{average velocity}", width=10.7, height=1.05, font_size=31).move_to(DOWN * 3.00)
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.08) for card in route], lag_ratio=0.08), run_time=RUN_SLOW*2.1)
        self.wait(PAUSE_WORK); self.play(FadeIn(formula), run_time=RUN_NORMAL); self.wait(PAUSE_FINAL)
        self.standard_closing("Position tells where. Slope tells how the position is changing.")


# Preview:
#   LESSON_TIME_SCALE=0.35 manim -pql position_time_graph_senior.py PositionTimeGraphSenior --fps 15 --disable_caching
# Final:
#   manim -pqh position_time_graph_senior.py PositionTimeGraphSenior --fps 30 --disable_caching
