#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Acceleration graph + Galileo V3 OPUS VISUAL.

This is a visual-first rebuild of the verified V2 render.
It keeps the same physical data and JP Classroom architecture while replacing
static-card dominance with synchronized motion, aligned v(t)/a(t) graphs,
graph-to-graph transformations, morphing equations, and a more rigorous
Galileo measurement sequence.

Target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from physics9_acceleration_graph_galileo_v2_base import *  # noqa: F401,F403,E402


class Physics9AccelerationGraphGalileoV3OpusVisual(
    Physics9AccelerationGraphGalileoV2StepByStep
):
    """Visual-first V3: synchronized motion, graph causality, and experiment."""

    def construct(self) -> None:
        self.opening()
        self.section_1_recall_velocity_graph()
        self.section_2_meaning_of_acceleration()
        self.section_3_build_acceleration_graph_first_half()
        self.section_4_build_acceleration_graph_second_half()
        self.section_5_read_full_acceleration_graph()
        self.section_6_constant_acceleration_equations()
        self.section_7_position_equation_from_area()
        self.section_8_why_galileo_inclined_plane()
        self.section_9_galileo_measurement_prediction()
        self.standard_closing(
            "Acceleration is visible twice: as the slope of v(t), and through the t squared growth of displacement."
        )

    # =========================================================================
    # Motion / graph helpers
    # =========================================================================
    @staticmethod
    def velocity_kmh_at(t_min: float) -> float:
        t = float(np.clip(t_min, PROFILE[0][0], PROFILE[-1][0]))
        for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:]):
            if t <= t1 + 1e-12:
                if abs(t1 - t0) < 1e-12:
                    return float(v1)
                f = (t - t0) / (t1 - t0)
                return float(v0 + f * (v1 - v0))
        return float(PROFILE[-1][1])

    @classmethod
    def distance_km_at(cls, t_min: float) -> float:
        """Integrate the piecewise-linear velocity profile exactly."""
        t = float(np.clip(t_min, PROFILE[0][0], PROFILE[-1][0]))
        distance = 0.0
        for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:]):
            if t <= t0:
                break
            stop = min(t, t1)
            dt_h = (stop - t0) / 60.0
            if dt_h > 0:
                frac = (stop - t0) / (t1 - t0)
                vend = v0 + frac * (v1 - v0)
                distance += 0.5 * (v0 + vend) * dt_h
            if t <= t1:
                break
        return distance

    @classmethod
    def total_distance_km(cls) -> float:
        return cls.distance_km_at(PROFILE[-1][0])

    def make_vehicle(self, scale: float = 1.0) -> VGroup:
        """Simple vector-built car: no external asset dependency."""
        body = RoundedRectangle(
            width=1.05,
            height=0.40,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        roof = Polygon(
            [-0.30, 0.20, 0],
            [-0.12, 0.43, 0],
            [0.27, 0.43, 0],
            [0.43, 0.20, 0],
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        wheel_l = Circle(
            radius=0.105,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to([-0.31, -0.22, 0])
        wheel_r = wheel_l.copy().move_to([0.31, -0.22, 0])
        axle_l = Dot(wheel_l.get_center(), radius=0.025, color=BLACK_LINE)
        axle_r = Dot(wheel_r.get_center(), radius=0.025, color=BLACK_LINE)
        return VGroup(body, roof, wheel_l, wheel_r, axle_l, axle_r).scale(scale)

    def time_chip(self, tracker: ValueTracker) -> Mobject:
        return always_redraw(
            lambda: self.text(
                f"t = {tracker.get_value():5.1f} min", 17, BOLD
            ).move_to([5.75, 1.95, 0])
        )

    def velocity_graph_compact(
        self, *, x_length: float = 8.7, y_length: float = 2.25
    ) -> tuple[Axes, VGroup, list[Line]]:
        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 20],
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.5,
                "include_ticks": True,
            },
            tips=False,
        )
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(
                self.text(str(x), 11).next_to(
                    axes.c2p(x, 0), DOWN, buff=0.05
                )
            )
        for y in (20, 40, 60, 80):
            labels.add(
                self.text(str(y), 11).next_to(
                    axes.c2p(0, y), LEFT, buff=0.05
                )
            )
        labels.add(
            self.text("t (min)", 14).next_to(
                axes.x_axis, DOWN, buff=0.22
            )
        )
        labels.add(
            self.text("v (km/h)", 14)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.27)
        )
        segments = self.velocity_segments(axes)
        return axes, labels, segments

    def acceleration_graph_compact(
        self, *, x_length: float = 8.7, y_length: float = 2.25
    ) -> tuple[Axes, VGroup, list[Line]]:
        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[-0.08, 0.08, 0.04],
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.5,
                "include_ticks": True,
            },
            tips=False,
        )
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(
                self.text(str(x), 11).next_to(
                    axes.c2p(x, 0), DOWN, buff=0.05
                )
            )
        for y in (-0.08, -0.04, 0.04, 0.08):
            labels.add(
                self.text(f"{y:+.2f}", 10).next_to(
                    axes.c2p(0, y), LEFT, buff=0.04
                )
            )
        labels.add(
            self.text("t (min)", 14).next_to(
                axes.x_axis, DOWN, buff=0.22
            )
        )
        labels.add(
            self.text("a (m/s²)", 14)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.27)
        )
        segments = self.acceleration_segments(axes)
        return axes, labels, segments

    def reasoning_rail(self) -> tuple[VGroup, list[VGroup]]:
        labels = ["interval", "Δv", "Δt", "calculate", "interpret", "draw"]
        chips: list[VGroup] = []
        for i, label in enumerate(labels, start=1):
            box = RoundedRectangle(
                width=3.75,
                height=0.47,
                corner_radius=0.08,
                stroke_color=LIGHT_GRAY,
                stroke_width=1.2,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            )
            n = self.text(f"{i}", 15, BOLD).move_to(
                box.get_left() + RIGHT * 0.25
            )
            txt = self.text(label, 15, BOLD).move_to(box).shift(
                RIGHT * 0.22
            )
            chips.append(VGroup(box, n, txt))
        rail = VGroup(*chips).arrange(DOWN, buff=0.08)
        return rail, chips

    def transform_equation_chain(
        self,
        expressions: list[str],
        *,
        size: int = 40,
        position: np.ndarray = ORIGIN,
        pause: float = 1.0,
    ) -> MathTex:
        """Morph one equation into the next while preserving matching symbols."""
        current = MathTex(
            expressions[0],
            font_size=size,
            color=BLACK_TEXT,
        ).move_to(position)
        self.play(Write(current), run_time=0.75)
        self.wait(pause)
        for expression in expressions[1:]:
            target = MathTex(
                expression,
                font_size=size,
                color=BLACK_TEXT,
            ).move_to(position)
            self.play(
                TransformMatchingTex(
                    current,
                    target,
                    transform_mismatches=True,
                ),
                run_time=0.85,
            )
            current = target
            self.wait(pause)
        return current

    def activate_reasoning_chip(
        self, chips: list[VGroup], index: int
    ) -> None:
        animations = []
        for i, chip in enumerate(chips):
            fill = VERY_LIGHT_GRAY if i == index else WHITE_FILL
            stroke = BLACK_LINE if i == index else LIGHT_GRAY
            animations.append(
                chip[0]
                .animate.set_fill(fill, opacity=1)
                .set_stroke(
                    stroke, width=1.6 if i == index else 1.2
                )
            )
        self.play(*animations, run_time=0.22)

    # =========================================================================
    # Opening — visual thesis first
    # =========================================================================
    def opening(self) -> None:
        label = self.text(
            "PHYSICS 9  |  KINEMATICS", 25, BOLD
        ).move_to([0, 3.15, 0])
        title = self.text(
            "FROM VELOCITY TO ACCELERATION", 48, BOLD
        ).move_to([0, 2.42, 0])
        rule = Line(
            LEFT * 5.7,
            RIGHT * 5.7,
            color=BLACK_LINE,
            stroke_width=2.2,
        ).move_to([0, 1.96, 0])
        thesis = self.text(
            "See the motion. Measure the slope. Build the acceleration graph.",
            25,
            MEDIUM,
        ).move_to([0, 1.52, 0])

        road = Line(
            LEFT * 5.6,
            RIGHT * 5.6,
            color=MID_GRAY,
            stroke_width=2.0,
        ).move_to([0, 0.42, 0])
        car = self.make_vehicle(0.72).move_to(
            road.get_start() + RIGHT * 0.35 + UP * 0.26
        )
        velocity_arrow = Arrow(
            car.get_center() + UP * 0.55,
            car.get_center() + RIGHT * 1.65 + UP * 0.55,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.16,
            color=BLACK_LINE,
        )
        v_label = self.math("v", 28).next_to(
            velocity_arrow, UP, buff=0.05
        )

        mini_v = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=3.1,
            y_length=1.35,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.2,
            },
            tips=False,
        ).move_to([-2.65, -1.85, 0])
        vline = Line(
            mini_v.c2p(0, 0.8),
            mini_v.c2p(4, 3.4),
            color=BLACK_LINE,
            stroke_width=3.0,
        )
        vtag = self.text("v(t)", 18, BOLD).next_to(
            mini_v, UP, buff=0.08
        )

        mini_a = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 1, 1],
            x_length=3.1,
            y_length=1.35,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.2,
            },
            tips=False,
        ).move_to([2.65, -1.85, 0])
        aline = Line(
            mini_a.c2p(0, 0.55),
            mini_a.c2p(4, 0.55),
            color=BLACK_LINE,
            stroke_width=4.0,
        )
        atag = self.text("a(t)", 18, BOLD).next_to(
            mini_a, UP, buff=0.08
        )

        connector = Arrow(
            [-0.65, -1.83, 0],
            [0.65, -1.83, 0],
            buff=0.12,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.14,
            color=MID_GRAY,
        )
        slope_word = self.text(
            "slope", 15, BOLD
        ).next_to(connector, UP, buff=0.05)

        group = VGroup(
            label,
            title,
            rule,
            thesis,
            road,
            car,
            velocity_arrow,
            v_label,
            mini_v,
            vline,
            vtag,
            mini_a,
            aline,
            atag,
            connector,
            slope_word,
        )
        self.assert_within_frame(group, "V3 opening", margin=0.15)

        self.play(
            FadeIn(label, shift=UP * 0.12),
            Write(title),
            Create(rule),
            run_time=1.3,
        )
        self.play(FadeIn(thesis), run_time=0.7)
        self.wait(0.9)
        self.play(
            Create(road),
            FadeIn(car),
            GrowArrow(velocity_arrow),
            FadeIn(v_label),
            run_time=0.8,
        )
        self.play(
            car.animate.shift(RIGHT * 4.2),
            velocity_arrow.animate.shift(RIGHT * 4.2),
            v_label.animate.shift(RIGHT * 4.2),
            run_time=1.4,
            rate_func=rate_functions.ease_in_quad,
        )
        self.play(
            FadeIn(VGroup(mini_v, vtag)),
            Create(vline),
            run_time=0.8,
        )
        self.play(
            GrowArrow(connector),
            FadeIn(slope_word),
            FadeIn(VGroup(mini_a, atag)),
            TransformFromCopy(vline, aline),
            run_time=1.0,
        )
        self.wait(1.7)
        self.play(FadeOut(group), run_time=0.8)

    # =========================================================================
    # 01 — real trip replay synchronized to v(t)
    # =========================================================================
    def section_1_recall_velocity_graph(self) -> None:
        self.lecture_header(
            1,
            "REPLAY THE TRIP: MOTION AND v(t) MUST TELL THE SAME STORY",
            "The graph is not decoration. Every point on v(t) is synchronized with the vehicle's motion.",
        )

        road = Line(
            [-6.55, 1.55, 0],
            [2.25, 1.55, 0],
            color=MID_GRAY,
            stroke_width=2.2,
        )
        start = self.text(
            "start", 14
        ).next_to(road.get_start(), DOWN, buff=0.10)
        finish = self.text(
            "trip progress", 14
        ).next_to(road.get_end(), DOWN, buff=0.10)

        axes, labels, segments = self.velocity_graph_compact(
            x_length=8.8, y_length=2.35
        )
        graph = VGroup(
            axes, labels, *segments
        ).move_to([-2.10, -1.10, 0])

        tracker = ValueTracker(0.0)
        total_d = self.total_distance_km()
        car = self.make_vehicle(0.60)

        moving_car = always_redraw(
            lambda: car.copy().move_to(
                road.point_from_proportion(
                    self.distance_km_at(tracker.get_value()) / total_d
                )
                + UP * 0.26
            )
        )
        vdot = always_redraw(
            lambda: Dot(
                axes.c2p(
                    tracker.get_value(),
                    self.velocity_kmh_at(tracker.get_value()),
                ),
                radius=0.07,
                color=BLACK_LINE,
            )
        )
        guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), 0),
                axes.c2p(
                    tracker.get_value(),
                    self.velocity_kmh_at(tracker.get_value()),
                ),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.1,
            )
        )
        arrow = always_redraw(
            lambda: Arrow(
                moving_car.get_center() + UP * 0.55,
                moving_car.get_center()
                + UP * 0.55
                + RIGHT
                * max(
                    0.02,
                    0.020
                    * self.velocity_kmh_at(tracker.get_value()),
                ),
                buff=0,
                stroke_width=3.2,
                max_tip_length_to_length_ratio=0.18,
                color=BLACK_LINE,
            )
        )
        speed = always_redraw(
            lambda: self.text(
                f"v = {self.velocity_kmh_at(tracker.get_value()):4.0f} km/h",
                16,
                BOLD,
            ).move_to([4.95, 1.70, 0])
        )
        clock = self.time_chip(tracker)

        question = self.note_panel(
            "WATCH FOR THREE SHAPES",
            [
                "rising v(t): velocity changes upward",
                "flat v(t): velocity is constant",
                "falling v(t): velocity changes downward",
            ],
            width=4.25,
            body_size=17,
        ).move_to([5.25, -0.95, 0])

        stage = VGroup(
            road, start, finish, graph, question
        )
        self.assert_content_safe(stage, "V3 section 1")

        self.play(
            FadeIn(VGroup(road, start, finish, graph, question)),
            FadeIn(moving_car),
            FadeIn(vdot),
            FadeIn(guide),
            FadeIn(arrow),
            FadeIn(speed),
            FadeIn(clock),
            run_time=0.9,
        )
        self.wait(1.0)

        previous = 0.0
        for t1, _ in PROFILE[1:]:
            interval = t1 - previous
            self.play(
                tracker.animate.set_value(t1),
                run_time=max(0.55, 0.055 * interval),
                rate_func=linear,
            )
            self.wait(0.25)
            previous = t1

        self.wait(1.2)
        self.clear_stage()

    # =========================================================================
    # 02 — slope morphs into acceleration level
    # =========================================================================
    def section_2_meaning_of_acceleration(self) -> None:
        self.lecture_header(
            2,
            "ACCELERATION IS WHAT THE SLOPE OF v(t) LOOKS LIKE AS A NEW GRAPH",
            "Read one velocity segment locally, then transfer its slope to one horizontal level on a(t).",
        )

        v_axes, v_labels, v_segments = self.velocity_graph_compact(
            x_length=8.7, y_length=2.20
        )
        a_axes, a_labels, _ = self.acceleration_graph_compact(
            x_length=8.7, y_length=2.20
        )
        VGroup(
            v_axes, v_labels, *v_segments
        ).move_to([-2.10, 0.75, 0])
        VGroup(
            a_axes, a_labels
        ).move_to([-2.10, -2.00, 0])

        right_title = self.text(
            "ONE SEGMENT → ONE LEVEL", 19, BOLD
        ).move_to([5.15, 1.25, 0])
        formula = self.formula_panel(
            r"a=\frac{\Delta v}{\Delta t}",
            width=4.3,
            height=0.90,
            font_size=34,
        ).move_to([5.15, 0.55, 0])
        cases = self.note_panel(
            "READ THE SIGN",
            [
                "slope > 0  →  a > 0",
                "slope = 0  →  a = 0",
                "slope < 0  →  a < 0",
                "Sign of a is not direction of motion.",
            ],
            width=4.3,
            body_size=18,
        ).move_to([5.15, -1.05, 0])

        stage = VGroup(
            v_axes,
            v_labels,
            *v_segments,
            a_axes,
            a_labels,
            right_title,
            formula,
            cases,
        )
        self.assert_content_safe(stage, "V3 section 2")
        self.play(FadeIn(stage), run_time=0.9)
        self.wait(1.0)

        retained = VGroup()
        for idx in (0, 1, 2):
            d = ACCEL_INTERVALS[idx]
            seg = v_segments[idx]
            highlight = seg.copy().set_stroke(width=7)
            g0 = DashedLine(
                v_axes.c2p(d["t0"], 0),
                a_axes.c2p(d["t0"], d["a"]),
                color=LIGHT_GRAY,
                stroke_width=1.1,
            )
            g1 = DashedLine(
                v_axes.c2p(d["t1"], 0),
                a_axes.c2p(d["t1"], d["a"]),
                color=LIGHT_GRAY,
                stroke_width=1.1,
            )
            level = Line(
                a_axes.c2p(d["t0"], d["a"]),
                a_axes.c2p(d["t1"], d["a"]),
                color=BLACK_LINE,
                stroke_width=5,
            )
            delta = self.text(
                f"Δv = {d['dv']:+.0f} km/h", 18, BOLD
            ).move_to([5.15, -2.65, 0])

            self.play(
                FadeIn(highlight),
                FadeIn(g0),
                FadeIn(g1),
                FadeIn(delta),
                run_time=0.45,
            )
            self.wait(0.8)
            self.play(
                TransformFromCopy(highlight, level),
                run_time=0.9,
            )
            self.wait(1.0)
            retained.add(level)
            self.play(
                FadeOut(highlight),
                FadeOut(g0),
                FadeOut(g1),
                FadeOut(delta),
                run_time=0.35,
            )

        self.wait(1.5)
        self.clear_stage()

    # =========================================================================
    # Shared interval-construction engine
    # =========================================================================
    def build_acceleration_intervals_visual(
        self,
        start_index: int,
        end_index: int,
        number: int,
        title: str,
    ) -> None:
        self.lecture_header(
            number,
            title,
            "The same six reasoning beats are attached directly to the two aligned graphs.",
        )

        v_axes, v_labels, v_segments = self.velocity_graph_compact(
            x_length=8.65, y_length=1.95
        )
        a_axes, a_labels, a_segments = self.acceleration_graph_compact(
            x_length=8.65, y_length=1.95
        )
        v_group = VGroup(
            v_axes, v_labels, *v_segments
        ).move_to([-2.25, 0.85, 0])
        a_group = VGroup(
            a_axes, a_labels
        ).move_to([-2.25, -1.80, 0])

        rail, chips = self.reasoning_rail()
        rail.move_to([5.25, 0.70, 0])
        formula_box = RoundedRectangle(
            width=4.05,
            height=1.35,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to([5.25, -2.05, 0])
        formula_title = self.text(
            "CURRENT INTERVAL", 15, BOLD
        ).next_to(
            formula_box.get_top(), DOWN, buff=0.12
        )

        retained = VGroup(
            *[a_segments[i] for i in range(start_index)]
        )
        stage = VGroup(
            v_group,
            a_group,
            rail,
            formula_box,
            formula_title,
            retained,
        )
        self.assert_content_safe(
            stage, f"V3 section {number}"
        )

        self.play(
            FadeIn(
                VGroup(
                    v_group,
                    a_group,
                    rail,
                    formula_box,
                    formula_title,
                )
            ),
            run_time=0.8,
        )
        if start_index > 0:
            self.play(FadeIn(retained), run_time=0.5)
        self.wait(0.8)

        for idx in range(start_index, end_index):
            d = ACCEL_INTERVALS[idx]
            current_texts = VGroup(
                self.text(
                    f"{d['t0']:.0f}–{d['t1']:.0f} min",
                    17,
                    BOLD,
                ),
                self.text(
                    f"Δv = {d['dv']:+.0f} km/h", 17
                ),
                self.text(
                    f"Δt = {d['dt']:.0f} min = {d['dt']*60:.0f} s",
                    16,
                ),
                self.text(
                    f"a = {d['a']:+.3f} m/s²", 18, BOLD
                ),
                self.text(
                    d["meaning"], 16, BOLD
                ),
            ).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05
            )
            self.fit(current_texts, 3.55, 1.00)
            current_texts.next_to(
                formula_title, DOWN, buff=0.08
            )

            vseg = v_segments[idx]
            hi = vseg.copy().set_stroke(width=7)
            t0x = d["t0"]
            t1x = d["t1"]
            guide0 = DashedLine(
                v_axes.c2p(t0x, 0),
                a_axes.c2p(t0x, d["a"]),
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )
            guide1 = DashedLine(
                v_axes.c2p(t1x, 0),
                a_axes.c2p(t1x, d["a"]),
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )
            dt_brace = BraceBetweenPoints(
                v_axes.c2p(t0x, 0),
                v_axes.c2p(t1x, 0),
                direction=DOWN,
                color=MID_GRAY,
            )

            if abs(d["dv"]) < 1e-12:
                dv_anchor = v_axes.c2p(
                    t1x, d["v0"]
                )
                dv_line = VGroup(
                    Dot(
                        dv_anchor,
                        radius=0.055,
                        color=MID_GRAY,
                    ),
                    self.text(
                        "Δv = 0", 13, BOLD
                    ).next_to(
                        dv_anchor, UP, buff=0.08
                    ),
                )
            else:
                dv_line = DoubleArrow(
                    v_axes.c2p(t1x, d["v0"]),
                    v_axes.c2p(t1x, d["v1"]),
                    buff=0.02,
                    stroke_width=2.0,
                    tip_length=0.12,
                    color=MID_GRAY,
                )

            level = a_segments[idx]

            self.activate_reasoning_chip(chips, 0)
            self.play(
                FadeIn(hi),
                FadeIn(guide0),
                FadeIn(guide1),
                FadeIn(current_texts[0]),
                run_time=0.42,
            )
            self.wait(0.65)

            self.activate_reasoning_chip(chips, 1)
            self.play(
                FadeIn(dv_line),
                FadeIn(current_texts[1]),
                run_time=0.38,
            )
            self.wait(0.65)

            self.activate_reasoning_chip(chips, 2)
            self.play(
                GrowFromCenter(dt_brace),
                FadeIn(current_texts[2]),
                run_time=0.38,
            )
            self.wait(0.65)

            self.activate_reasoning_chip(chips, 3)
            calc = MathTex(
                rf"a=\frac{{{d['dv']/3.6:+.2f}\ \mathrm{{m/s}}}}{{{d['dt']*60:.0f}\ \mathrm{{s}}}}={d['a']:+.3f}\ \mathrm{{m/s^2}}",
                font_size=24,
                color=BLACK_TEXT,
            )
            self.fit(calc, 3.65, 0.40)
            calc.next_to(
                formula_box.get_bottom(), UP, buff=0.12
            )
            self.play(
                Write(calc),
                FadeIn(current_texts[3]),
                run_time=0.62,
            )
            self.wait(0.85)

            self.activate_reasoning_chip(chips, 4)
            self.play(
                FadeIn(current_texts[4]),
                run_time=0.28,
            )
            self.wait(0.72)

            self.activate_reasoning_chip(chips, 5)
            self.play(
                TransformFromCopy(hi, level),
                run_time=0.78,
            )
            self.wait(0.90)

            self.play(
                FadeOut(
                    VGroup(
                        hi,
                        guide0,
                        guide1,
                        dt_brace,
                        dv_line,
                        current_texts,
                        calc,
                    )
                ),
                run_time=0.32,
            )
            retained.add(level)

        self.wait(1.3)
        self.clear_stage()

    def section_3_build_acceleration_graph_first_half(
        self,
    ) -> None:
        self.build_acceleration_intervals_visual(
            0,
            6,
            3,
            "BUILD a(t) — INTERVALS 01 TO 06",
        )

    def section_4_build_acceleration_graph_second_half(
        self,
    ) -> None:
        self.build_acceleration_intervals_visual(
            6,
            12,
            4,
            "COMPLETE a(t) — INTERVALS 07 TO 12",
        )

    # =========================================================================
    # 05 — replay complete a(t) with the moving vehicle
    # =========================================================================
    def section_5_read_full_acceleration_graph(self) -> None:
        self.lecture_header(
            5,
            "READ a(t) WITH THE VEHICLE: SIGN, MAGNITUDE, AND ZERO",
            "Because this trip never has negative velocity, a < 0 means slowing down here — not moving backward.",
        )

        road = Line(
            [-6.45, 1.62, 0],
            [2.10, 1.62, 0],
            color=MID_GRAY,
            stroke_width=2.0,
        )
        tracker = ValueTracker(0.0)
        total_d = self.total_distance_km()
        base_car = self.make_vehicle(0.55)

        moving_car = always_redraw(
            lambda: base_car.copy().move_to(
                road.point_from_proportion(
                    self.distance_km_at(
                        tracker.get_value()
                    )
                    / total_d
                )
                + UP * 0.24
            )
        )

        axes, labels, segs = self.acceleration_graph_compact(
            x_length=8.8, y_length=2.65
        )
        graph = VGroup(
            axes, labels, *segs
        ).move_to([-2.05, -1.22, 0])

        def current_accel() -> float:
            t = tracker.get_value()
            for d in ACCEL_INTERVALS:
                if d["t0"] <= t <= d["t1"] + 1e-9:
                    return d["a"]
            return 0.0

        adot = always_redraw(
            lambda: Dot(
                axes.c2p(
                    tracker.get_value(),
                    current_accel(),
                ),
                radius=0.07,
                color=BLACK_LINE,
            )
        )
        guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(
                    tracker.get_value(), -0.079
                ),
                axes.c2p(
                    tracker.get_value(), 0.079
                ),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )
        )
        speed = always_redraw(
            lambda: self.text(
                f"v = {self.velocity_kmh_at(tracker.get_value()):4.0f} km/h",
                16,
                BOLD,
            ).move_to([5.20, 1.75, 0])
        )
        accel = always_redraw(
            lambda: self.text(
                f"a = {current_accel():+.3f} m/s²",
                16,
                BOLD,
            ).move_to([5.20, 1.30, 0])
        )

        note = self.note_panel(
            "PHYSICS CHECK",
            [
                "a and v same sign → speed increases",
                "a and v opposite signs → speed decreases",
                "a = 0 → velocity stays constant",
            ],
            width=4.25,
            body_size=17,
        ).move_to([5.20, -0.80, 0])

        stage = VGroup(road, graph, note)
        self.assert_content_safe(
            stage, "V3 section 5"
        )

        self.play(
            FadeIn(VGroup(road, graph, note)),
            FadeIn(moving_car),
            FadeIn(adot),
            FadeIn(guide),
            FadeIn(speed),
            FadeIn(accel),
            run_time=0.8,
        )
        self.wait(0.8)

        for t1, _ in PROFILE[1:]:
            self.play(
                tracker.animate.set_value(t1),
                run_time=0.42,
                rate_func=linear,
            )
            self.wait(0.18)

        self.wait(1.3)
        self.clear_stage()

    # =========================================================================
    # 06 — single morphing derivation
    # =========================================================================
    def section_6_constant_acceleration_equations(
        self,
    ) -> None:
        self.lecture_header(
            6,
            "CONSTANT a MEANS A STRAIGHT v(t): DERIVE v = v₀ + at",
            "Keep the slope triangle visible while the algebra transforms in place.",
        )

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 8, 2],
            x_length=5.6,
            y_length=3.6,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.6,
                "include_ticks": True,
            },
            tips=False,
        )
        v0, t1, v1 = 2.0, 5.0, 7.0
        line = Line(
            axes.c2p(0, v0),
            axes.c2p(t1, v1),
            color=BLACK_LINE,
            stroke_width=4.0,
        )
        run = Line(
            axes.c2p(0, v0),
            axes.c2p(t1, v0),
            color=MID_GRAY,
            stroke_width=2.0,
        )
        rise = Line(
            axes.c2p(t1, v0),
            axes.c2p(t1, v1),
            color=MID_GRAY,
            stroke_width=2.0,
        )
        dt = self.math(
            r"\Delta t", 25
        ).next_to(run, DOWN, buff=0.08)
        dv = self.math(
            r"\Delta v", 25
        ).next_to(rise, RIGHT, buff=0.08)
        fig = VGroup(
            axes, line, run, rise, dt, dv
        )
        panel = self.figure_panel(
            fig,
            width=6.6,
            height=4.85,
            title="Slope of the velocity graph",
            caption="Constant slope = constant acceleration",
        )
        panel.group.move_to([-4.15, -0.55, 0])

        chain = [
            r"a=\frac{\Delta v}{\Delta t}",
            r"a=\frac{v-v_0}{t}",
            r"at=v-v_0",
            r"v_0+at=v",
            r"\boxed{v=v_0+at}",
        ]

        self.assert_content_safe(
            panel.group, "V3 section 6 graph"
        )
        self.play(FadeIn(panel.group), run_time=0.8)
        self.wait(1.0)

        self.transform_equation_chain(
            chain,
            size=43,
            position=np.array([3.45, 0.35, 0]),
            pause=1.25,
        )

        meaning = self.note_panel(
            "THE GRAPH AND EQUATION AGREE",
            [
                "v₀ = intercept",
                "a = slope",
                "at = accumulated velocity change",
            ],
            width=6.0,
            body_size=19,
        ).move_to([3.45, -2.05, 0])
        self.play(FadeIn(meaning), run_time=0.6)
        self.wait(2.0)
        self.clear_stage()

    # =========================================================================
    # 07 — area geometry becomes algebra
    # =========================================================================
    def section_7_position_equation_from_area(
        self,
    ) -> None:
        self.lecture_header(
            7,
            "AREA UNDER v(t) BECOMES DISPLACEMENT",
            "Build the rectangle and triangle first; only then translate each area into algebra.",
        )

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 8, 2],
            x_length=7.0,
            y_length=3.6,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.6,
                "include_ticks": True,
            },
            tips=False,
        )
        t1, v0, v1 = 5.0, 2.0, 7.0
        line = Line(
            axes.c2p(0, v0),
            axes.c2p(t1, v1),
            color=BLACK_LINE,
            stroke_width=4.0,
        )
        rect = Polygon(
            axes.c2p(0, 0),
            axes.c2p(t1, 0),
            axes.c2p(t1, v0),
            axes.c2p(0, v0),
            stroke_color=MID_GRAY,
            stroke_width=1.3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.75,
        )
        tri = Polygon(
            axes.c2p(0, v0),
            axes.c2p(t1, v0),
            axes.c2p(t1, v1),
            stroke_color=BLACK_LINE,
            stroke_width=1.4,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.60,
        )
        fig = VGroup(axes, line, rect, tri)
        panel = self.figure_panel(
            fig,
            width=8.0,
            height=5.05,
            title="Displacement is area under v(t)",
            caption="rectangle + triangle",
        )
        panel.group.move_to([-3.55, -0.55, 0])

        eq_rect = self.formula_panel(
            r"A_{\rm rect}=v_0t",
            width=5.5,
            height=0.92,
            font_size=34,
        ).move_to([4.55, 1.25, 0])
        eq_tri = self.formula_panel(
            r"A_{\triangle}=\frac12(at)t=\frac12at^2",
            width=5.5,
            height=0.92,
            font_size=31,
        ).move_to([4.55, 0.10, 0])
        eq_sum = self.formula_panel(
            r"\Delta x=v_0t+\frac12at^2",
            width=5.5,
            height=1.02,
            font_size=35,
        ).move_to([4.55, -1.10, 0])
        eq_final = self.formula_panel(
            r"\boxed{x=x_0+v_0t+\frac12at^2}",
            width=5.5,
            height=1.12,
            font_size=36,
        ).move_to([4.55, -2.40, 0])

        stage = VGroup(
            panel.group,
            eq_rect,
            eq_tri,
            eq_sum,
            eq_final,
        )
        self.assert_content_safe(
            stage, "V3 section 7"
        )

        self.play(FadeIn(panel.group), run_time=0.8)
        self.wait(1.0)
        self.play(
            TransformFromCopy(rect, eq_rect),
            run_time=0.8,
        )
        self.wait(0.9)
        self.play(
            TransformFromCopy(tri, eq_tri),
            run_time=0.8,
        )
        self.wait(1.0)
        self.play(FadeIn(eq_sum), run_time=0.6)
        self.wait(1.1)
        self.play(FadeIn(eq_final), run_time=0.7)
        self.wait(1.8)
        self.clear_stage()

    # =========================================================================
    # 08 — Galileo: timing problem vs measurable ramp
    # =========================================================================
    def section_8_why_galileo_inclined_plane(
        self,
    ) -> None:
        self.lecture_header(
            8,
            "GALILEO'S MEASUREMENT TRICK: SLOW THE MOTION WITHOUT LOSING CONSTANT a",
            "Free fall is too fast for coarse timing. A gentle ramp spreads the same t² pattern over a longer observable path.",
        )

        fall_top = np.array([-4.9, 1.45, 0])
        fall_bottom = np.array([-4.9, -2.25, 0])
        fall_track = Line(
            fall_top,
            fall_bottom,
            color=BLACK_LINE,
            stroke_width=3.0,
        )
        floor_l = Line(
            [-5.65, -2.25, 0],
            [-4.15, -2.25, 0],
            color=MID_GRAY,
            stroke_width=1.8,
        )
        fall_ball = Circle(
            radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to(fall_top)
        fall_clock = self.text(
            "same clock", 16, BOLD
        ).move_to([-4.9, 1.95, 0])

        ramp_start = np.array([1.10, -2.25, 0])
        ramp_end = np.array([5.75, 1.25, 0])
        ramp = Line(
            ramp_start,
            ramp_end,
            color=BLACK_LINE,
            stroke_width=3.5,
        )
        floor_r = Line(
            [0.55, -2.25, 0],
            [6.10, -2.25, 0],
            color=MID_GRAY,
            stroke_width=1.8,
        )
        ramp_ball = Circle(
            radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to(ramp_end)
        ramp_clock = self.text(
            "same clock", 16, BOLD
        ).move_to([3.65, 1.95, 0])

        left_title = self.text(
            "FREE FALL", 20, BOLD
        ).move_to([-4.9, 2.30, 0])
        right_title = self.text(
            "INCLINED PLANE", 20, BOLD
        ).move_to([3.65, 2.30, 0])
        left_note = self.text(
            "a = g", 19, BOLD
        ).move_to([-4.9, -2.72, 0])
        right_note = self.text(
            "a_ramp is constant and smaller than g",
            18,
            BOLD,
        ).move_to([3.65, -2.72, 0])
        model_note = self.text(
            "Exact magnitude depends on sliding/rolling model; the t² law does not.",
            17,
        ).move_to([0.45, -3.42, 0])

        divider = Line(
            [0, 2.45, 0],
            [0, -3.15, 0],
            color=LIGHT_GRAY,
            stroke_width=1.5,
        )

        stage = VGroup(
            fall_track,
            floor_l,
            fall_ball,
            fall_clock,
            ramp,
            floor_r,
            ramp_ball,
            ramp_clock,
            left_title,
            right_title,
            left_note,
            right_note,
            model_note,
            divider,
        )
        self.assert_content_safe(
            stage, "V3 section 8"
        )
        self.play(FadeIn(stage), run_time=0.8)
        self.wait(0.8)

        self.play(
            fall_ball.animate.move_to(fall_bottom),
            run_time=0.65,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.8)
        fall_ball.move_to(fall_top)

        self.play(
            ramp_ball.animate.move_to(ramp_start),
            run_time=2.3,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(1.2)

        conclusion = self.note_panel(
            "EXPERIMENTAL ADVANTAGE",
            [
                "more time between measurable positions",
                "smaller relative timing error",
                "constant acceleration remains testable",
            ],
            width=7.0,
            body_size=19,
        ).move_to([0, -0.55, 0])

        self.play(FadeOut(stage), run_time=0.45)
        self.play(FadeIn(conclusion), run_time=0.6)
        self.wait(2.1)
        self.clear_stage()

    # =========================================================================
    # 09 — equal-time pulses + 1:4:9:16 + x versus t²
    # =========================================================================
    def section_9_galileo_measurement_prediction(
        self,
    ) -> None:
        self.lecture_header(
            9,
            "GALILEO'S TEST: EQUAL TIMES PRODUCE A 1 : 4 : 9 : 16 DISTANCE PATTERN",
            "Measure positions at equal time pulses, then plot displacement against t². Constant acceleration becomes a straight line.",
        )

        ramp_start = np.array([-6.25, -2.55, 0])
        ramp_end = np.array([-0.75, 1.65, 0])
        ramp = Line(
            ramp_start,
            ramp_end,
            color=BLACK_LINE,
            stroke_width=4.0,
        )
        floor = Line(
            [-6.55, -2.55, 0],
            [-0.15, -2.55, 0],
            color=LIGHT_GRAY,
            stroke_width=1.7,
        )
        ball = Circle(
            radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to(ramp_end)
        release = self.text(
            "release", 15, BOLD
        ).next_to(ramp_end, UP, buff=0.12)

        qs = [1, 4, 9, 16]
        points = [
            ramp.point_from_proportion(1 - q / 16)
            for q in qs
        ]
        marks = VGroup()
        labels = VGroup()
        for t, q, p in zip(
            (1, 2, 3, 4), qs, points
        ):
            tick = Line(
                DOWN * 0.13,
                UP * 0.13,
                color=BLACK_LINE,
                stroke_width=2.1,
            )
            tick.rotate(ramp.get_angle() + PI / 2)
            tick.move_to(p)
            lab = self.text(
                f"t={t}   x∝{q}", 14, BOLD
            ).next_to(p, DOWN, buff=0.14)
            marks.add(tick)
            labels.add(lab)

        data_axes = Axes(
            x_range=[0, 16, 4],
            y_range=[0, 16, 4],
            x_length=4.8,
            y_length=3.45,
            axis_config={
                "color": BLACK_LINE,
                "stroke_width": 1.5,
                "include_ticks": True,
            },
            tips=False,
        ).move_to([4.20, -0.35, 0])
        data_x = self.text(
            "t²", 16, BOLD
        ).next_to(data_axes.x_axis, DOWN, buff=0.14)
        data_y = self.text(
            "displacement", 15, BOLD
        ).rotate(PI / 2).next_to(
            data_axes.y_axis, LEFT, buff=0.18
        )
        line = Line(
            data_axes.c2p(0, 0),
            data_axes.c2p(16, 16),
            color=LIGHT_GRAY,
            stroke_width=2.0,
        )
        data_dots = VGroup(
            *[
                Dot(
                    data_axes.c2p(q, q),
                    radius=0.065,
                    color=BLACK_LINE,
                )
                for q in qs
            ]
        )
        graph_title = self.text(
            "x versus t²", 20, BOLD
        ).move_to([4.20, 1.78, 0])

        formula = self.formula_panel(
            r"x-x_0=\frac12at^2",
            width=4.7,
            height=0.88,
            font_size=32,
        ).move_to([4.20, -2.60, 0])

        stage = VGroup(
            ramp,
            floor,
            ball,
            release,
            marks,
            labels,
            data_axes,
            data_x,
            data_y,
            line,
            graph_title,
            formula,
        )
        self.assert_content_safe(
            stage, "V3 section 9"
        )

        self.play(
            FadeIn(
                VGroup(
                    ramp,
                    floor,
                    ball,
                    release,
                    data_axes,
                    data_x,
                    data_y,
                    graph_title,
                )
            ),
            run_time=0.8,
        )
        self.wait(0.7)
        self.play(FadeIn(marks), run_time=0.5)

        for i, point in enumerate(points):
            pulse = Circle(
                radius=0.18,
                stroke_color=MID_GRAY,
                stroke_width=2.0,
            ).move_to([-0.05, 2.00, 0])
            clock_txt = self.text(
                f"t = {i+1}", 15, BOLD
            ).move_to(pulse)

            self.play(
                FadeIn(pulse),
                FadeIn(clock_txt),
                ball.animate.move_to(point),
                FadeIn(labels[i]),
                run_time=0.85,
                rate_func=linear,
            )
            self.play(
                FadeOut(pulse),
                FadeOut(clock_txt),
                run_time=0.18,
            )
            self.wait(0.45)

        self.play(FadeIn(formula), run_time=0.55)
        self.wait(0.8)
        self.play(Create(line), run_time=0.8)
        for dot in data_dots:
            self.play(
                FadeIn(dot, scale=0.6),
                run_time=0.25,
            )
        self.wait(1.4)

        result = self.note_panel(
            "EXPERIMENTAL SIGNATURE OF CONSTANT ACCELERATION",
            [
                "equal Δt does not give equal Δx",
                "x ∝ t²",
                "therefore x versus t² is linear",
                "free fall is the constant-acceleration case a = g",
            ],
            width=7.2,
            body_size=18,
        ).move_to([0.30, -0.60, 0])

        self.play(
            FadeOut(stage),
            FadeOut(data_dots),
            run_time=0.45,
        )
        self.play(FadeIn(result), run_time=0.6)
        self.wait(2.3)
        self.clear_stage()
