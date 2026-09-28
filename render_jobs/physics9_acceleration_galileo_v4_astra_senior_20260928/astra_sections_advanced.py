#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
from manim import *

from astra_visual_mixin import *  # noqa: F401,F403


class AstraAdvancedSections:
    """Sections 05–09 for the V4 ASTRA lesson."""

    def section_5_read_full_acceleration_graph(self) -> None:
        self.astra_header(
            5,
            "READ a(t)",
            "Replay the trip once more: acceleration is the rate at which the velocity value is changing.",
        )

        road = Line([-6.45, 1.78, 0], [2.60, 1.78, 0], color=MID_GRAY, stroke_width=2.2)
        axes, labels, segs = self.acceleration_axes_astra(x_length=9.25, y_length=3.05)
        graph = VGroup(axes, labels, *segs).move_to([-2.25, -1.05, 0])

        tracker = ValueTracker(0.0)
        total_d = self.total_distance_km()
        base_car = self.make_vehicle(0.64)
        moving_car = always_redraw(
            lambda: base_car.copy().move_to(
                road.point_from_proportion(self.distance_km_at(tracker.get_value()) / total_d) + UP * 0.28
            )
        )
        adot = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), self.acceleration_at(tracker.get_value())),
                radius=0.085,
                color=BLACK_LINE,
            )
        )
        hud = self.big_hud(tracker, x=5.20, y=-0.35)

        self.assert_content_safe(VGroup(road, graph), "V4 section 5 static")
        self.play(FadeIn(road), FadeIn(graph), FadeIn(moving_car), FadeIn(adot), FadeIn(hud), run_time=0.75)
        self.wait(0.7)

        for t1, _ in PROFILE[1:]:
            self.play(tracker.animate.set_value(t1), run_time=0.40, rate_func=linear)
            self.wait(0.13)

        strongest_pos = max(ACCEL_INTERVALS, key=lambda d: d["a"])
        strongest_neg = min(ACCEL_INTERVALS, key=lambda d: d["a"])
        self.play(FadeOut(hud), run_time=0.25)

        cards = [
            self.focus_panel(
                "LARGEST POSITIVE a",
                [f"{strongest_pos['t0']:.0f}–{strongest_pos['t1']:.0f} min",
                 f"a = {strongest_pos['a']:+.3f} m/s²"],
                meaning="FASTEST VELOCITY INCREASE",
                width=4.20, height=3.45,
            ).move_to([5.20, -0.35, 0]),
            self.focus_panel(
                "LARGEST NEGATIVE a",
                [f"{strongest_neg['t0']:.0f}–{strongest_neg['t1']:.0f} min",
                 f"a = {strongest_neg['a']:+.3f} m/s²"],
                meaning="STRONGEST BRAKING",
                width=4.20, height=3.45,
            ).move_to([5.20, -0.35, 0]),
            self.focus_panel(
                "ZERO ACCELERATION",
                ["a = 0", "velocity can still be nonzero"],
                meaning="CONSTANT v ≠ REST",
                width=4.20, height=3.45,
            ).move_to([5.20, -0.35, 0]),
        ]
        current = cards[0]
        self.play(FadeIn(current), run_time=0.40)
        self.wait(1.1)
        for new in cards[1:]:
            self.play(ReplacementTransform(current, new), run_time=0.40)
            current = new
            self.wait(1.1)
        self.clear_stage()

    def section_6_constant_acceleration_equations(self) -> None:
        self.astra_header(
            6,
            "DERIVE  v = v₀ + at",
            "Constant acceleration means constant slope on v(t). The algebra must preserve that geometric meaning.",
        )

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 8, 2],
            x_length=6.3, y_length=3.75,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )
        v0, t1, v1 = 2.0, 5.0, 7.0
        line = Line(axes.c2p(0, v0), axes.c2p(t1, v1), color=BLACK_LINE, stroke_width=4.5)
        run = Line(axes.c2p(0, v0), axes.c2p(t1, v0), color=MID_GRAY, stroke_width=2.2)
        rise = Line(axes.c2p(t1, v0), axes.c2p(t1, v1), color=MID_GRAY, stroke_width=2.2)
        dt = self.math(r"\Delta t", 32).next_to(run, DOWN, buff=0.12)
        dv = self.math(r"\Delta v", 32).next_to(rise, RIGHT, buff=0.12)
        slope = self.text("slope = acceleration", 28, BOLD).next_to(axes, DOWN, buff=0.55)
        graph = VGroup(axes, line, run, rise, dt, dv, slope).move_to([-3.95, -0.55, 0])
        self.assert_content_safe(graph, "V4 section 6 graph")

        self.play(FadeIn(graph), run_time=0.75)
        self.wait(0.9)

        chain = [
            r"a=\frac{\Delta v}{\Delta t}",
            r"a=\frac{v-v_0}{t}",
            r"at=v-v_0",
            r"v_0+at=v",
            r"\boxed{v=v_0+at}",
        ]
        current = MathTex(chain[0], font_size=52, color=BLACK_TEXT).move_to([3.45, 0.25, 0])
        self.play(Write(current), run_time=0.75)
        self.wait(1.15)
        for expression in chain[1:]:
            target = MathTex(expression, font_size=52, color=BLACK_TEXT).move_to([3.45, 0.25, 0])
            self.play(
                TransformMatchingTex(current, target, transform_mismatches=True),
                run_time=0.80,
            )
            current = target
            self.wait(1.15)

        interpretation = self.text(
            "intercept = v₀     slope = a     elapsed change = at",
            28, BOLD,
        ).move_to([3.45, -1.65, 0])
        self.play(FadeIn(interpretation), run_time=0.45)
        self.wait(1.7)
        self.clear_stage()

    def section_7_position_equation_from_area(self) -> None:
        self.astra_header(
            7,
            "AREA → POSITION",
            "Displacement is the area under v(t): rectangle + triangle becomes the constant-acceleration position equation.",
        )

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 8, 2],
            x_length=7.0, y_length=4.05,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )
        t1, v0, v1 = 5.0, 2.0, 7.0
        line = Line(axes.c2p(0, v0), axes.c2p(t1, v1), color=BLACK_LINE, stroke_width=4.5)
        rect = Polygon(
            axes.c2p(0, 0), axes.c2p(t1, 0), axes.c2p(t1, v0), axes.c2p(0, v0),
            stroke_color=MID_GRAY, stroke_width=1.5,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=0.80,
        )
        tri = Polygon(
            axes.c2p(0, v0), axes.c2p(t1, v0), axes.c2p(t1, v1),
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=LIGHT_GRAY, fill_opacity=0.60,
        )
        labels = VGroup(
            self.text("time", 24, BOLD).next_to(axes.x_axis, DOWN, buff=0.30),
            self.text("velocity", 24, BOLD).rotate(PI / 2).next_to(
                axes.y_axis, LEFT, buff=0.35
            ),
        )
        graph = VGroup(axes, rect, tri, line, labels).move_to([-3.75, -0.55, 0])

        eq1 = MathTex(r"A_{\rm rect}=v_0t", font_size=44, color=BLACK_TEXT)
        eq2 = MathTex(r"A_{\triangle}=\frac12(at)t=\frac12at^2", font_size=41, color=BLACK_TEXT)
        eq3 = MathTex(r"\Delta x=v_0t+\frac12at^2", font_size=44, color=BLACK_TEXT)
        eq4 = MathTex(r"\boxed{x=x_0+v_0t+\frac12at^2}", font_size=46, color=BLACK_TEXT)
        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.50).move_to([3.60, -0.45, 0])

        self.assert_content_safe(VGroup(graph, eqs), "V4 section 7")
        self.play(FadeIn(VGroup(axes, labels, line)), run_time=0.65)
        self.play(FadeIn(rect), run_time=0.55)
        self.play(TransformFromCopy(rect, eq1), run_time=0.65)
        self.wait(0.85)
        self.play(FadeIn(tri), run_time=0.55)
        self.play(TransformFromCopy(tri, eq2), run_time=0.65)
        self.wait(0.95)
        self.play(FadeIn(eq3), run_time=0.50)
        self.wait(1.10)
        self.play(FadeIn(eq4), run_time=0.55)
        self.wait(1.8)
        self.clear_stage()

    def section_8_why_galileo_inclined_plane(self) -> None:
        self.astra_header(
            8,
            "WHY GALILEO USED A RAMP",
            "The ramp makes the timing easier to resolve while preserving a constant-acceleration experiment.",
        )

        question = self.text(
            "How can we measure accelerated motion with a coarse clock?",
            34, BOLD,
        ).move_to([0, 1.95, 0])

        fall_top = np.array([-2.70, 1.20, 0])
        fall_bottom = np.array([-2.70, -2.40, 0])
        fall_track = Line(fall_top, fall_bottom, color=BLACK_LINE, stroke_width=4.0)
        floor = Line([-3.50, -2.40, 0], [-1.90, -2.40, 0], color=MID_GRAY, stroke_width=2.0)
        ball = Circle(
            radius=0.22, stroke_color=BLACK_LINE, stroke_width=2.2,
            fill_color=WHITE_FILL, fill_opacity=1.0,
        ).move_to(fall_top)
        free_label = self.text("FREE FALL", 31, BOLD).move_to([-2.70, 1.75, 0])
        free_eq = MathTex(r"a=g", font_size=44, color=BLACK_TEXT).move_to([3.05, 0.65, 0])
        short = self.text("SHORT TIMING WINDOW", 34, BOLD).move_to([3.05, -0.25, 0])
        short_note = self.text(
            "small timing errors become a large fraction of Δt",
            26,
        ).move_to([3.05, -0.85, 0])

        free_group = VGroup(question, fall_track, floor, ball, free_label, free_eq, short, short_note)
        self.assert_content_safe(free_group, "V4 section 8 free fall")

        self.play(FadeIn(free_group), run_time=0.75)
        self.wait(0.8)
        self.play(ball.animate.move_to(fall_bottom), run_time=0.62, rate_func=rate_functions.ease_in_quad)
        self.wait(1.0)

        ramp_start = np.array([-5.35, -2.25, 0])
        ramp_end = np.array([0.35, 1.20, 0])
        ramp = Line(ramp_start, ramp_end, color=BLACK_LINE, stroke_width=4.0)
        ramp_floor = Line([-5.65, -2.25, 0], [0.85, -2.25, 0], color=MID_GRAY, stroke_width=2.0)
        ramp_ball = ball.copy().move_to(ramp_end)
        ramp_label = self.text("INCLINED PLANE", 31, BOLD).move_to([-2.55, 1.78, 0])
        longer = self.text("LONGER MEASURABLE Δt", 34, BOLD).move_to([3.55, 0.45, 0])
        model = self.text(
            "For a rolling ball, the exact a depends on rotational inertia.",
            25,
        ).move_to([3.55, -0.28, 0])
        invariant = self.text(
            "Experimental target: a ≈ constant",
            29, BOLD,
        ).move_to([3.55, -1.05, 0])
        ramp_group = VGroup(question, ramp, ramp_floor, ramp_ball, ramp_label, longer, model, invariant)
        self.assert_content_safe(ramp_group, "V4 section 8 ramp")

        self.play(
            FadeOut(VGroup(fall_track, floor, ball, free_label, free_eq, short, short_note)),
            run_time=0.45,
        )
        self.play(
            FadeIn(VGroup(ramp, ramp_floor, ramp_ball, ramp_label, longer, model, invariant)),
            run_time=0.65,
        )
        self.wait(0.8)
        self.play(
            ramp_ball.animate.move_to(ramp_start),
            run_time=2.20,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(1.2)

        conclusion = self.focus_panel(
            "WHY THE RAMP HELPS",
            [
                "longer observable motion",
                "smaller relative timing error",
                "constant-a model remains testable",
            ],
            meaning="SLOWER TO MEASURE, SAME KINEMATIC STRUCTURE",
            width=8.20, height=3.10,
        ).move_to([0, -0.40, 0])
        self.play(FadeOut(ramp_group), run_time=0.45)
        self.play(FadeIn(conclusion), run_time=0.55)
        self.wait(2.0)
        self.clear_stage()

    def section_9_galileo_measurement_prediction(self) -> None:
        self.astra_header(
            9,
            "TEST  x ∝ t²",
            "Start from rest. Measure position at equal times. Then test whether displacement is proportional to t².",
        )

        ramp_start = np.array([-6.20, -2.60, 0])
        ramp_end = np.array([0.25, 1.55, 0])
        ramp = Line(ramp_start, ramp_end, color=BLACK_LINE, stroke_width=4.0)
        floor = Line([-6.50, -2.60, 0], [0.80, -2.60, 0], color=LIGHT_GRAY, stroke_width=1.8)
        ball = Circle(
            radius=0.22, stroke_color=BLACK_LINE, stroke_width=2.2,
            fill_color=WHITE_FILL, fill_opacity=1.0,
        ).move_to(ramp_end)
        release = self.text("RELEASE", 24, BOLD).next_to(ramp_end, UP, buff=0.15)

        table_box = RoundedRectangle(
            width=5.05, height=4.25, corner_radius=0.13,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE_FILL, fill_opacity=1.0,
        ).move_to([4.80, -0.45, 0])
        table_title = self.text("EQUAL-TIME MEASUREMENTS", 25, BOLD).next_to(
            table_box.get_top(), DOWN, buff=0.22
        )
        rows = [
            self.text("t = 1   →   x / x₁ = 1", 29, BOLD),
            self.text("t = 2   →   x / x₁ = 4", 29, BOLD),
            self.text("t = 3   →   x / x₁ = 9", 29, BOLD),
            self.text("t = 4   →   x / x₁ = 16", 29, BOLD),
        ]
        row_group = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.33).next_to(
            table_title, DOWN, buff=0.40
        )
        row_group.align_to(table_box, LEFT).shift(RIGHT * 0.38)
        rule = self.math(r"x-x_0=\frac12at^2", 40).next_to(row_group, DOWN, buff=0.40)
        rule.align_to(row_group, LEFT)

        static = VGroup(ramp, floor, ball, release, table_box, table_title)
        self.assert_content_safe(static, "V4 section 9 measurement")

        qs = [1, 4, 9, 16]
        points = [ramp.point_from_proportion(1.0 - q / 16.0) for q in qs]
        marks = VGroup()
        for p in points:
            tick = Line(DOWN * 0.15, UP * 0.15, color=BLACK_LINE, stroke_width=2.2)
            tick.rotate(ramp.get_angle() + PI / 2)
            tick.move_to(p)
            marks.add(tick)

        self.play(FadeIn(static), FadeIn(marks), run_time=0.75)
        self.wait(0.8)
        for i, p in enumerate(points):
            pulse = self.text(f"t = {i + 1}", 30, BOLD).move_to([2.35, 1.65, 0])
            self.play(
                FadeIn(pulse), ball.animate.move_to(p), FadeIn(rows[i]),
                run_time=0.85, rate_func=linear,
            )
            self.wait(0.65)
            self.play(FadeOut(pulse), run_time=0.20)

        self.play(FadeIn(rule), run_time=0.50)
        self.wait(1.4)

        measurement_group = VGroup(
            ramp, floor, ball, release, marks, table_box, table_title, row_group, rule
        )
        self.play(FadeOut(measurement_group), run_time=0.55)

        data_axes = Axes(
            x_range=[0, 16, 4], y_range=[0, 16, 4],
            x_length=8.2, y_length=4.80,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        ).move_to([-2.35, -0.65, 0])
        xlab = self.text("t²", 27, BOLD).next_to(data_axes.x_axis, DOWN, buff=0.25)
        ylab = self.text("displacement", 27, BOLD).rotate(PI / 2).next_to(
            data_axes.y_axis, LEFT, buff=0.30
        )
        tick_labels = VGroup()
        for q in (0, 4, 8, 12, 16):
            tick_labels.add(self.text(str(q), 20).next_to(data_axes.c2p(q, 0), DOWN, buff=0.08))
            tick_labels.add(self.text(str(q), 20).next_to(data_axes.c2p(0, q), LEFT, buff=0.08))

        line = Line(data_axes.c2p(0, 0), data_axes.c2p(16, 16), color=LIGHT_GRAY, stroke_width=3.0)
        dots = VGroup(*[
            Dot(data_axes.c2p(q, q), radius=0.09, color=BLACK_LINE)
            for q in qs
        ])
        equation = self.focus_panel(
            "LINEAR TEST",
            ["plot x against t²"],
            equation=r"x-x_0=\left(\frac a2\right)t^2",
            meaning="SLOPE = a / 2",
            width=4.45, height=3.60,
        ).move_to([5.05, -0.45, 0])

        plot_group = VGroup(data_axes, xlab, ylab, tick_labels, line, dots)
        self.assert_content_safe(VGroup(plot_group, equation), "V4 section 9 plot")

        self.play(
            FadeIn(VGroup(data_axes, xlab, ylab, tick_labels)),
            FadeIn(equation),
            run_time=0.75,
        )
        self.play(Create(line), run_time=0.70)
        for dot in dots:
            self.play(FadeIn(dot, scale=0.6), run_time=0.22)
        self.wait(1.0)

        final = self.focus_panel(
            "EXPERIMENTAL SIGNATURE",
            [
                "equal time steps → unequal distances",
                "x - x₀ ∝ t²",
                "x versus t² → straight line",
            ],
            meaning="CONSTANT ACCELERATION CONFIRMED",
            width=7.70, height=3.25,
        ).move_to([0, -0.35, 0])
        self.play(FadeOut(VGroup(plot_group, equation)), run_time=0.45)
        self.play(FadeIn(final), run_time=0.55)
        self.wait(2.2)
        self.clear_stage()
