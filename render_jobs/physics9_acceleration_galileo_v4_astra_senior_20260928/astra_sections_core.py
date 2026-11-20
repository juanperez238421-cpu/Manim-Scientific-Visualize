#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
from manim import *

from astra_visual_mixin import *  # noqa: F401,F403


class AstraCoreSections:
    """Opening and sections 01–04 for the V4 ASTRA lesson."""

    def opening(self) -> None:
        title = self.text("FROM VELOCITY TO ACCELERATION", 54, BOLD).move_to([0, 2.42, 0])
        subtitle = self.text("Motion → slope → acceleration → Galileo", 30, BOLD).move_to([0, 1.72, 0])
        rule = Line(LEFT * 5.7, RIGHT * 5.7, color=BLACK_LINE, stroke_width=2.2).move_to([0, 1.30, 0])
        road = Line([-5.8, 0.10, 0], [5.8, 0.10, 0], color=MID_GRAY, stroke_width=2.4)
        car = self.make_vehicle(0.82).move_to(road.get_start() + RIGHT * 0.5 + UP * 0.30)
        words = VGroup(
            self.text("MOTION", 33, BOLD),
            self.text("SLOPE", 33, BOLD),
            self.text("ACCELERATION", 33, BOLD),
        ).arrange(RIGHT, buff=1.35).move_to([0, -1.55, 0])
        arrows = VGroup(
            Arrow(words[0].get_right() + RIGHT * 0.08, words[1].get_left() + LEFT * 0.08,
                  buff=0, color=BLACK_LINE, stroke_width=3),
            Arrow(words[1].get_right() + RIGHT * 0.08, words[2].get_left() + LEFT * 0.08,
                  buff=0, color=BLACK_LINE, stroke_width=3),
        )
        group = VGroup(title, subtitle, rule, road, car, words, arrows)
        self.assert_within_frame(group, "V4 opening", margin=0.15)

        self.play(Write(title), FadeIn(subtitle), Create(rule), run_time=1.05)
        self.play(Create(road), FadeIn(car), run_time=0.55)
        self.play(
            car.animate.move_to(road.get_end() + LEFT * 0.5 + UP * 0.30),
            run_time=1.55,
            rate_func=rate_functions.ease_in_quad,
        )
        self.play(FadeIn(words), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=0.80)
        self.wait(1.5)
        self.play(FadeOut(group), run_time=0.65)

    def section_1_recall_velocity_graph(self) -> None:
        self.astra_header(
            1,
            "MOTION ↔ v(t)",
            "The vehicle and the graph are synchronized: every point on v(t) describes the same instant of the trip.",
        )
        road = Line([-6.55, 1.78, 0], [2.55, 1.78, 0], color=MID_GRAY, stroke_width=2.2)
        start = self.text("START", 22, BOLD).next_to(road.get_start(), DOWN, buff=0.12)
        end = self.text("TRIP PROGRESS", 22, BOLD).next_to(road.get_end(), DOWN, buff=0.12)

        axes, labels, segments = self.velocity_axes_astra(x_length=9.25, y_length=3.10)
        graph = VGroup(axes, labels, *segments).move_to([-2.25, -1.05, 0])

        tracker = ValueTracker(0.0)
        total_d = self.total_distance_km()
        base_car = self.make_vehicle(0.66)
        moving_car = always_redraw(
            lambda: base_car.copy().move_to(
                road.point_from_proportion(self.distance_km_at(tracker.get_value()) / total_d) + UP * 0.29
            )
        )
        graph_dot = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), self.velocity_kmh_at(tracker.get_value())),
                radius=0.085,
                color=BLACK_LINE,
            )
        )
        graph_guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), 0),
                axes.c2p(tracker.get_value(), self.velocity_kmh_at(tracker.get_value())),
                dash_length=0.06,
                color=LIGHT_GRAY,
                stroke_width=1.3,
            )
        )
        hud = self.big_hud(tracker, x=5.20, y=-0.35)

        stage = VGroup(road, start, end, graph)
        self.assert_content_safe(stage, "V4 section 1 static")
        self.play(FadeIn(stage), FadeIn(moving_car), FadeIn(graph_dot), FadeIn(graph_guide), FadeIn(hud), run_time=0.80)
        self.wait(0.8)

        previous = 0.0
        for t1, _ in PROFILE[1:]:
            dt = t1 - previous
            self.play(
                tracker.animate.set_value(t1),
                run_time=float(np.clip(0.065 * dt, 0.55, 1.25)),
                rate_func=linear,
            )
            self.wait(0.20)
            previous = t1
        self.wait(1.3)
        self.clear_stage()

    def section_2_meaning_of_acceleration(self) -> None:
        self.astra_header(
            2,
            "SLOPE ↔ ACCELERATION",
            "For one interval: read the slope on v(t), calculate Δv/Δt, then place one horizontal level on a(t).",
        )
        v_axes, v_labels, v_segments = self.velocity_axes_astra(x_length=9.15, y_length=2.30)
        a_axes, a_labels, _ = self.acceleration_axes_astra(x_length=9.15, y_length=2.05)
        v_graph = VGroup(v_axes, v_labels, *v_segments).move_to([-2.30, 0.90, 0])
        a_graph = VGroup(a_axes, a_labels).move_to([-2.30, -2.05, 0])
        focus = self.focus_panel(
            "CORE DEFINITION",
            ["change in velocity", "divided by elapsed time"],
            equation=r"a=\frac{\Delta v}{\Delta t}",
            width=4.20,
            height=3.50,
        ).move_to([5.20, -0.30, 0])

        self.assert_content_safe(VGroup(v_graph, a_graph, focus), "V4 section 2")
        self.play(FadeIn(v_graph), FadeIn(a_graph), FadeIn(focus), run_time=0.80)
        self.wait(1.0)

        for idx in (0, 1, 2):
            d = ACCEL_INTERVALS[idx]
            hi = v_segments[idx].copy().set_stroke(width=8)
            guide0 = DashedLine(
                v_axes.c2p(d["t0"], -2), a_axes.c2p(d["t0"], d["a"]),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.2,
            )
            guide1 = DashedLine(
                v_axes.c2p(d["t1"], -2), a_axes.c2p(d["t1"], d["a"]),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.2,
            )
            level = Line(
                a_axes.c2p(d["t0"], d["a"]), a_axes.c2p(d["t1"], d["a"]),
                color=BLACK_LINE, stroke_width=6.0,
            )
            new_focus = self.focus_panel(
                f"EXAMPLE {idx + 1}",
                [
                    f"{d['t0']:.0f}–{d['t1']:.0f} min",
                    f"Δv = {d['dv']:+.0f} km/h",
                    f"a = {d['a']:+.3f} m/s²",
                ],
                meaning=d["meaning"].upper(),
                width=4.20,
                height=3.50,
            ).move_to(focus)
            self.play(
                ReplacementTransform(focus, new_focus),
                FadeIn(hi), FadeIn(guide0), FadeIn(guide1),
                run_time=0.48,
            )
            focus = new_focus
            self.wait(1.05)
            self.play(TransformFromCopy(hi, level), run_time=0.72)
            self.wait(0.90)
            self.play(FadeOut(hi), FadeOut(guide0), FadeOut(guide1), run_time=0.28)

        final_focus = self.focus_panel(
            "READ THE SIGN",
            [
                "a > 0 → velocity increases",
                "a = 0 → velocity is constant",
                "a < 0 → velocity decreases",
            ],
            meaning="a SIGN ≠ MOTION DIRECTION",
            width=4.20,
            height=3.55,
        ).move_to(focus)
        self.play(ReplacementTransform(focus, final_focus), run_time=0.45)
        self.wait(1.8)
        self.clear_stage()

    def build_intervals_astra(
        self,
        start_index: int,
        end_index: int,
        *,
        section_number: int,
        title: str,
    ) -> None:
        self.astra_header(
            section_number,
            title,
            "Six decisions per interval, but only one focus state on screen at a time.",
        )
        v_axes, v_labels, v_segments = self.velocity_axes_astra(x_length=9.25, y_length=2.20)
        a_axes, a_labels, a_segments = self.acceleration_axes_astra(x_length=9.25, y_length=2.00)
        v_graph = VGroup(v_axes, v_labels, *v_segments).move_to([-2.30, 0.95, 0])
        a_graph = VGroup(a_axes, a_labels).move_to([-2.30, -2.00, 0])
        retained = VGroup(*[a_segments[i] for i in range(start_index)])

        focus = self.focus_panel(
            "METHOD",
            ["1 interval", "2 Δv", "3 Δt", "4 calculate", "5 interpret", "6 draw"],
            width=4.20,
            height=4.00,
        ).move_to([5.20, -0.40, 0])
        self.assert_content_safe(VGroup(v_graph, a_graph, retained, focus), f"V4 section {section_number}")

        self.play(FadeIn(v_graph), FadeIn(a_graph), FadeIn(focus), run_time=0.75)
        if start_index > 0:
            self.play(FadeIn(retained), run_time=0.35)
        self.wait(0.9)

        for idx in range(start_index, end_index):
            d = ACCEL_INTERVALS[idx]
            hi = v_segments[idx].copy().set_stroke(width=8.0)
            guide0 = DashedLine(
                v_axes.c2p(d["t0"], -2), a_axes.c2p(d["t0"], d["a"]),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.1,
            )
            guide1 = DashedLine(
                v_axes.c2p(d["t1"], -2), a_axes.c2p(d["t1"], d["a"]),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.1,
            )

            p1 = self.focus_panel(
                f"1 / 6  INTERVAL {idx + 1:02d}",
                [f"{d['t0']:.0f} → {d['t1']:.0f} min"],
                meaning="READ THE TIME WINDOW",
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(
                ReplacementTransform(focus, p1),
                FadeIn(hi), FadeIn(guide0), FadeIn(guide1),
                run_time=0.42,
            )
            focus = p1
            self.wait(0.65)

            if abs(d["dv"]) > 1e-12:
                dv_mark = DoubleArrow(
                    v_axes.c2p(d["t1"], d["v0"]),
                    v_axes.c2p(d["t1"], d["v1"]),
                    buff=0.02, stroke_width=2.5, tip_length=0.13, color=MID_GRAY,
                )
            else:
                dv_mark = Circle(
                    radius=0.11, stroke_color=MID_GRAY, stroke_width=2.0,
                ).move_to(v_axes.c2p(d["t1"], d["v1"]))

            p2 = self.focus_panel(
                "2 / 6  VELOCITY CHANGE",
                [
                    f"v₀ = {d['v0']:.0f} km/h",
                    f"v₁ = {d['v1']:.0f} km/h",
                    f"Δv = {d['dv']:+.0f} km/h",
                ],
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(ReplacementTransform(focus, p2), FadeIn(dv_mark), run_time=0.38)
            focus = p2
            self.wait(0.75)

            p3 = self.focus_panel(
                "3 / 6  ELAPSED TIME",
                [f"Δt = {d['dt']:.0f} min", f"Δt = {d['dt'] * 60:.0f} s"],
                meaning="CONVERT TO SI",
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(ReplacementTransform(focus, p3), run_time=0.36)
            focus = p3
            self.wait(0.75)

            dv_ms = d["dv"] / 3.6
            dt_s = d["dt"] * 60.0
            p4 = self.focus_panel(
                "4 / 6  CALCULATE",
                [
                    f"Δv = {dv_ms:+.2f} m/s",
                    f"Δt = {dt_s:.0f} s",
                ],
                equation=rf"a=\frac{{{dv_ms:+.2f}}}{{{dt_s:.0f}}}",
                meaning=f"a = {d['a']:+.3f} m/s²",
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(ReplacementTransform(focus, p4), run_time=0.40)
            focus = p4
            self.wait(1.20)

            meaning = (
                "SPEEDING UP" if d["a"] > 1e-9
                else "SLOWING DOWN" if d["a"] < -1e-9
                else "CONSTANT VELOCITY"
            )
            p5 = self.focus_panel(
                "5 / 6  INTERPRET",
                [f"a = {d['a']:+.3f} m/s²"],
                meaning=meaning,
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(ReplacementTransform(focus, p5), run_time=0.38)
            focus = p5
            self.wait(0.80)

            p6 = self.focus_panel(
                "6 / 6  TRANSFER TO a(t)",
                [f"{d['t0']:.0f}–{d['t1']:.0f} min"],
                equation=rf"a={d['a']:+.3f}\ \mathrm{{m/s^2}}",
                width=4.20,
                height=3.55,
            ).move_to(focus)
            self.play(ReplacementTransform(focus, p6), run_time=0.38)
            focus = p6
            self.play(TransformFromCopy(hi, a_segments[idx]), run_time=0.72)
            self.wait(0.80)

            self.play(
                FadeOut(hi), FadeOut(guide0), FadeOut(guide1), FadeOut(dv_mark),
                run_time=0.25,
            )

        summary = self.focus_panel(
            "SECTION COMPLETE",
            [f"intervals {start_index + 1:02d}–{end_index:02d}", "slope on v(t) → level on a(t)"],
            meaning="SAME PHYSICS, SAME METHOD",
            width=4.20,
            height=3.55,
        ).move_to(focus)
        self.play(ReplacementTransform(focus, summary), run_time=0.42)
        self.wait(1.4)
        self.clear_stage()

    def section_3_build_acceleration_graph_first_half(self) -> None:
        self.build_intervals_astra(0, 6, section_number=3, title="BUILD a(t): 0–60 min")

    def section_4_build_acceleration_graph_second_half(self) -> None:
        self.build_intervals_astra(6, 12, section_number=4, title="BUILD a(t): 60–120 min")
