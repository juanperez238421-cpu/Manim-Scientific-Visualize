#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Acceleration graph construction + Galileo bridge V2.

This scene is the direct continuation of the latest variable-velocity lesson.
It preserves the same trip profile and builds the acceleration-time graph
interval by interval from the slope of the velocity-time graph.

Pedagogical sequence:
    recall v(t) -> define acceleration as slope -> construct a(t) ->
    interpret sign and magnitude -> derive constant-acceleration equations ->
    connect to Galileo's inclined-plane experiment.

Target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from jp_classroom_style import *  # noqa: F401,F403,E402


# =============================================================================
# SAME VELOCITY PROFILE AS THE PREVIOUS LESSON
# time: min, velocity: km/h
# =============================================================================
PROFILE = [
    (0.0, 0.0),
    (10.0, 70.0),
    (35.0, 70.0),
    (40.0, 0.0),
    (55.0, 0.0),
    (60.0, 65.0),
    (75.0, 65.0),
    (82.0, 25.0),
    (92.0, 25.0),
    (100.0, 10.0),
    (108.0, 10.0),
    (115.0, 55.0),
    (120.0, 55.0),
]


def acceleration_ms2(t0_min: float, v0_kmh: float, t1_min: float, v1_kmh: float) -> float:
    """Average acceleration for a linear v(t) interval, in m/s^2."""
    dv_ms = (v1_kmh - v0_kmh) / 3.6
    dt_s = (t1_min - t0_min) * 60.0
    return dv_ms / dt_s


ACCEL_INTERVALS = []
for i, ((t0, v0), (t1, v1)) in enumerate(zip(PROFILE[:-1], PROFILE[1:]), start=1):
    a = acceleration_ms2(t0, v0, t1, v1)
    if abs(a) < 1e-12:
        meaning = "constant velocity"
    elif a > 0:
        meaning = "speeding up"
    else:
        meaning = "slowing down"
    ACCEL_INTERVALS.append(
        {
            "n": i,
            "t0": t0,
            "t1": t1,
            "v0": v0,
            "v1": v1,
            "dv": v1 - v0,
            "dt": t1 - t0,
            "a": a,
            "meaning": meaning,
        }
    )


class Physics9AccelerationGraphGalileoV2StepByStep(JPMathClassroomScene):
    """Slower, explicit step-by-step acceleration graph and Galileo experiment bridge."""

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        assert len(PROFILE) == 13
        assert len(ACCEL_INTERVALS) == 12

        expected = [
            +0.0324074,
            0.0,
            -0.0648148,
            0.0,
            +0.0601852,
            0.0,
            -0.0264550,
            0.0,
            -0.00868056,
            0.0,
            +0.0297619,
            0.0,
        ]
        for actual, target in zip((d["a"] for d in ACCEL_INTERVALS), expected):
            assert abs(actual - target) < 2e-5

        assert abs((70 / 3.6) / 600 - 0.0324074) < 1e-5
        assert abs((-70 / 3.6) / 300 + 0.0648148) < 1e-5
        assert abs((65 / 3.6) / 300 - 0.0601852) < 1e-5

    # -------------------------------------------------------------------------
    # Deliberate classroom pacing
    # -------------------------------------------------------------------------
    def paced_play(self, *animations, pause: float = 0.85, **kwargs):
        """Run one animation beat, then leave a visible thinking pause."""
        super().play(*animations, **kwargs)
        self.wait(pause)

    # -------------------------------------------------------------------------
    # Main flow
    # -------------------------------------------------------------------------
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
            "Next: use the inclined plane to measure x and t, then test whether x divided by t squared is approximately constant."
        )

    # -------------------------------------------------------------------------
    # Shared scientific header
    # -------------------------------------------------------------------------
    def lecture_header(self, number: int, title: str, subtitle: str) -> None:
        kicker = self.text("PHYSICS 9  |  ACCELERATION", 19, BOLD)
        badge = RoundedRectangle(
            width=0.62,
            height=0.42,
            corner_radius=0.07,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 17, BOLD).move_to(badge)
        title_mob = self.text(title, 30, BOLD)
        title_row = VGroup(VGroup(badge, badge_text), title_mob).arrange(RIGHT, buff=0.20)
        self.fit(title_row, 14.2, 0.50)

        subtitle_mob = self.text(subtitle, 18)
        self.fit(subtitle_mob, 14.0, 0.44)

        rule = Line(LEFT * 7.2, RIGHT * 7.2, color=LIGHT_GRAY, stroke_width=1.8)
        kicker.to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.48)
        title_row.next_to(kicker, DOWN, buff=0.08).align_to(kicker, LEFT)
        rule.next_to(title_row, DOWN, buff=0.07)
        subtitle_mob.next_to(rule, DOWN, buff=0.07).align_to(kicker, LEFT)

        new_header = VGroup(kicker, title_row, rule)
        old_header = self.header_group
        old_subtitle = self.subtitle_group
        self.header_group = new_header
        self.subtitle_group = subtitle_mob

        if old_header is not None:
            fades = [FadeOut(old_header)]
            if old_subtitle is not None:
                fades.append(FadeOut(old_subtitle))
            self.paced_play(*fades, run_time=0.30, pause=0.45)

        self.paced_play(FadeIn(new_header), FadeIn(subtitle_mob), run_time=0.36, pause=0.90)

    # -------------------------------------------------------------------------
    # Graph helpers
    # -------------------------------------------------------------------------
    def velocity_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 10],
            x_length=8.1,
            y_length=3.65,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.7, "include_ticks": True},
            tips=False,
        )

    def acceleration_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 20],
            y_range=[-0.08, 0.08, 0.02],
            x_length=8.1,
            y_length=3.85,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.7, "include_ticks": True},
            tips=False,
        )

    def velocity_axis_labels(self, axes: Axes) -> VGroup:
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(self.text(str(x), 13).next_to(axes.c2p(x, 0), DOWN, buff=0.07))
        for y in range(20, 81, 20):
            labels.add(self.text(str(y), 13).next_to(axes.c2p(0, y), LEFT, buff=0.07))
        labels.add(self.text("time (min)", 17).next_to(axes.x_axis, DOWN, buff=0.29))
        labels.add(
            self.text("velocity (km/h)", 17)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.35)
        )
        return labels

    def acceleration_axis_labels(self, axes: Axes) -> VGroup:
        labels = VGroup()
        for x in range(0, 121, 20):
            labels.add(self.text(str(x), 13).next_to(axes.c2p(x, 0), DOWN, buff=0.07))
        for value in (-0.06, -0.04, -0.02, 0.02, 0.04, 0.06):
            text_value = f"{value:.2f}"
            labels.add(
                self.text(text_value, 12)
                .next_to(axes.c2p(0, value), LEFT, buff=0.06)
            )
        labels.add(self.text("time (min)", 17).next_to(axes.x_axis, DOWN, buff=0.29))
        labels.add(
            self.text("acceleration (m/s²)", 17)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.35)
        )
        return labels

    def velocity_segments(self, axes: Axes) -> list[Line]:
        pts = [axes.c2p(t, v) for t, v in PROFILE]
        return [
            Line(pts[i], pts[i + 1], color=BLACK_LINE, stroke_width=4.0)
            for i in range(12)
        ]

    def acceleration_segments(self, axes: Axes) -> list[Line]:
        segs = []
        for d in ACCEL_INTERVALS:
            y = d["a"]
            segs.append(
                Line(
                    axes.c2p(d["t0"], y),
                    axes.c2p(d["t1"], y),
                    color=BLACK_LINE,
                    stroke_width=5.0,
                )
            )
        return segs

    def interval_card(self, d: dict, *, width: float = 4.75) -> VGroup:
        title = self.text(f"STEP {d['n']:02d} / 12", 20, BOLD)
        interval = self.text(f"{d['t0']:.0f}–{d['t1']:.0f} min", 20)
        delta_v = self.text(f"Δv = {d['dv']:+.0f} km/h", 22, BOLD)
        delta_t = self.text(f"Δt = {d['dt']:.0f} min", 19)
        a_value = self.text(f"a = {d['a']:+.3f} m/s²", 23, BOLD)
        meaning = self.text(d["meaning"], 19)
        content = VGroup(
            title,
            interval,
            delta_v,
            delta_t,
            a_value,
            meaning,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        self.fit(content, width - 0.45, 2.22)

        box = RoundedRectangle(
            width=width,
            height=2.52,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.25)
        return VGroup(box, content)

    def slope_formula_card(self, d: dict, *, width: float = 4.75) -> VGroup:
        dv_ms = d["dv"] / 3.6
        dt_s = d["dt"] * 60
        formula = MathTex(
            rf"a=\frac{{\Delta v}}{{\Delta t}}"
            rf"=\frac{{{dv_ms:+.2f}\ \mathrm{{m/s}}}}{{{dt_s:.0f}\ \mathrm{{s}}}}"
            rf"\approx {d['a']:+.3f}\ \mathrm{{m/s^2}}",
            font_size=31,
            color=BLACK_TEXT,
        )
        self.fit(formula, width - 0.35, 0.90)
        box = RoundedRectangle(
            width=width,
            height=1.20,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        formula.move_to(box)
        return VGroup(box, formula)

    # -------------------------------------------------------------------------
    # Opening
    # -------------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9  |  KINEMATICS",
            "FROM VELOCITY TO ACCELERATION",
            "Build the acceleration-time graph from the velocity-time graph, one interval at a time.",
            "Then derive the constant-acceleration motion equation that leads directly to Galileo's inclined plane.",
        )

    # -------------------------------------------------------------------------
    # 01 — recall previous v(t)
    # -------------------------------------------------------------------------
    def section_1_recall_velocity_graph(self) -> None:
        self.lecture_header(
            1,
            "RECALL THE VELOCITY-TIME GRAPH FROM THE LAST LESSON",
            "Every line segment already contains information about acceleration.",
        )

        axes = self.velocity_axes()
        labels = self.velocity_axis_labels(axes)
        segments = self.velocity_segments(axes)
        graph = VGroup(axes, labels, *segments)

        panel = self.figure_panel(
            graph,
            width=10.0,
            height=5.35,
            title="The same 120-minute trip",
            caption="Rising, horizontal, and falling segments will become positive, zero, and negative acceleration.",
        )
        panel.group.move_to([-2.05, -0.45, 0])

        rule = self.note_panel(
            "NEW QUESTION",
            [
                "How fast is velocity changing?",
                "We answer by measuring the slope of v(t).",
            ],
            width=4.45,
            body_size=21,
        )
        rule.move_to([5.30, 0.65, 0])

        formula = self.formula_panel(
            r"a_{\mathrm{avg}}=\frac{\Delta v}{\Delta t}",
            width=4.45,
            height=1.10,
            font_size=38,
        )
        formula.move_to([5.30, -1.40, 0])

        stage = VGroup(panel.group, rule, formula)
        self.assert_content_safe(stage, "section 1")
        self.paced_play(FadeIn(panel.group), FadeIn(rule), FadeIn(formula))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 02 — meaning of acceleration
    # -------------------------------------------------------------------------
    def section_2_meaning_of_acceleration(self) -> None:
        self.lecture_header(
            2,
            "ACCELERATION IS THE SLOPE OF THE VELOCITY-TIME GRAPH",
            "The sign tells the direction of velocity change; the magnitude tells how quickly the change occurs.",
        )

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5.6,
            y_length=3.2,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.6, "include_ticks": True},
            tips=False,
        )
        p0 = axes.c2p(1, 2)
        p1 = axes.c2p(8, 8)
        line = Line(p0, p1, color=BLACK_LINE, stroke_width=4.0)
        xlab = self.text("time", 16).next_to(axes.x_axis, DOWN, buff=0.16)
        ylab = self.text("velocity", 16).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.16)
        slope_fig = VGroup(axes, line, xlab, ylab)

        left = self.figure_panel(
            slope_fig,
            width=7.7,
            height=4.85,
            title="Slope means velocity change per unit time",
            caption="a = rise / run = Δv / Δt",
        )

        positive = self.note_panel(
            "POSITIVE a",
            ["v increases", "v(t) slopes upward", "object speeds up in this trip"],
            width=5.4,
            body_size=20,
        )
        zero = self.note_panel(
            "ZERO a",
            ["v is constant", "v(t) is horizontal", "speed does not change"],
            width=5.4,
            body_size=20,
        )
        negative = self.note_panel(
            "NEGATIVE a",
            ["v decreases", "v(t) slopes downward", "object slows down in this trip"],
            width=5.4,
            body_size=20,
        )
        right = VGroup(positive, zero, negative).arrange(DOWN, buff=0.18)

        layout = self.split_layout(
            left.group,
            right,
            left_width=7.8,
            right_width=5.5,
            max_height=5.10,
            gap=0.60,
            center_y=-0.45,
        )
        self.assert_content_safe(layout.group, "section 2")

        # Generate the slope triangle only after the final layout transform.
        run = Line(axes.c2p(1, 2), axes.c2p(8, 2), color=MID_GRAY, stroke_width=2)
        rise = Line(axes.c2p(8, 2), axes.c2p(8, 8), color=MID_GRAY, stroke_width=2)
        dv = self.text("Δv", 19, BOLD).next_to(rise, RIGHT, buff=0.08)
        dt = self.text("Δt", 19, BOLD).next_to(run, DOWN, buff=0.08)

        self.paced_play(FadeIn(left.group), FadeIn(right))
        self.paced_play(Create(run), Create(rise), FadeIn(dv), FadeIn(dt), run_time=0.9)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 03 — a(t), first half
    # -------------------------------------------------------------------------
    def section_3_build_acceleration_graph_first_half(self) -> None:
        self.lecture_header(
            3,
            "BUILD THE ACCELERATION GRAPH — INTERVALS 01 TO 06",
            "For every interval we will pause after each decision: read time, find Δv, find Δt, calculate a, interpret it, then draw the level.",
        )

        axes = self.acceleration_axes()
        labels = self.acceleration_axis_labels(axes)
        base = VGroup(axes, labels)

        panel = self.figure_panel(
            base,
            width=9.65,
            height=5.45,
            title="Acceleration-time graph",
            caption="Each linear v(t) interval gives one constant acceleration level.",
        )
        panel.group.move_to([-2.25, -0.45, 0])
        a_segments = self.acceleration_segments(axes)

        method = self.note_panel(
            "THE SIX-BEAT METHOD",
            [
                "1. Read the time interval.",
                "2. Compute Δv.",
                "3. Compute Δt.",
                "4. Calculate a = Δv/Δt.",
                "5. Read the physical meaning.",
                "6. Draw the horizontal level on a(t).",
            ],
            width=4.50,
            body_size=17,
        ).move_to([5.25, -0.20, 0])

        stage = VGroup(panel.group, method)
        self.assert_content_safe(stage, "section 3 method")
        self.paced_play(FadeIn(panel.group), pause=0.90)
        self.paced_play(FadeIn(method), pause=1.60)
        self.paced_play(FadeOut(method), pause=0.65)

        for i, d in enumerate(ACCEL_INTERVALS[:6]):
            card = self.interval_card(d, width=4.50).move_to([5.25, 0.65, 0])
            formula = self.slope_formula_card(d, width=4.50).move_to([5.25, -2.00, 0])
            box = card[0]
            lines = card[1]

            guide0 = DashedLine(
                axes.c2p(d["t0"], -0.078),
                axes.c2p(d["t0"], 0.078),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )
            guide1 = DashedLine(
                axes.c2p(d["t1"], -0.078),
                axes.c2p(d["t1"], 0.078),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )

            # Beat 1 — identify the exact time interval.
            self.paced_play(
                FadeIn(box), FadeIn(lines[0]), FadeIn(lines[1]),
                FadeIn(guide0), FadeIn(guide1),
                run_time=0.55, pause=1.15,
            )

            # Beat 2 — velocity change.
            self.paced_play(FadeIn(lines[2]), run_time=0.35, pause=1.15)

            # Beat 3 — elapsed time.
            self.paced_play(FadeIn(lines[3]), run_time=0.35, pause=1.15)

            # Beat 4 — convert to SI and calculate acceleration.
            self.paced_play(FadeIn(formula[0]), run_time=0.30, pause=0.35)
            self.paced_play(Write(formula[1]), run_time=0.72, pause=1.35)

            # Beat 5 — display numerical acceleration and its meaning.
            self.paced_play(FadeIn(lines[4]), run_time=0.35, pause=0.85)
            self.paced_play(FadeIn(lines[5]), run_time=0.35, pause=1.20)

            # Beat 6 — transfer the calculation to the acceleration graph.
            self.paced_play(Create(a_segments[i]), run_time=0.80, pause=1.45)

            self.paced_play(
                FadeOut(guide0), FadeOut(guide1),
                FadeOut(card), FadeOut(formula),
                run_time=0.35, pause=0.65,
            )

        summary = self.note_panel(
            "FIRST HALF PATTERN",
            [
                "positive → zero → negative → zero → positive → zero",
                "Every horizontal level came from one slope calculation on v(t).",
            ],
            width=4.50,
            body_size=18,
        ).move_to([5.25, -0.35, 0])

        self.paced_play(FadeIn(summary), pause=2.00)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 04 — a(t), second half
    # -------------------------------------------------------------------------
    def section_4_build_acceleration_graph_second_half(self) -> None:
        self.lecture_header(
            4,
            "COMPLETE THE ACCELERATION GRAPH — INTERVALS 07 TO 12",
            "Use the same six-beat method again. The procedure must not change just because the road event changes.",
        )

        axes = self.acceleration_axes()
        labels = self.acceleration_axis_labels(axes)
        base = VGroup(axes, labels)

        panel = self.figure_panel(
            base,
            width=9.65,
            height=5.45,
            title="Acceleration-time graph",
            caption="The first six levels are prior knowledge. Now complete the second half.",
        )
        panel.group.move_to([-2.25, -0.45, 0])

        a_segments = self.acceleration_segments(axes)
        known_levels = VGroup(*a_segments[:6])

        stage = VGroup(panel.group, known_levels)
        self.assert_content_safe(stage, "section 4 known graph")
        self.paced_play(FadeIn(panel.group), pause=0.85)
        self.paced_play(FadeIn(known_levels), pause=1.30)

        for global_i, d in enumerate(ACCEL_INTERVALS[6:], start=6):
            card = self.interval_card(d, width=4.50).move_to([5.25, 0.65, 0])
            formula = self.slope_formula_card(d, width=4.50).move_to([5.25, -2.00, 0])
            box = card[0]
            lines = card[1]

            guide0 = DashedLine(
                axes.c2p(d["t0"], -0.078),
                axes.c2p(d["t0"], 0.078),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )
            guide1 = DashedLine(
                axes.c2p(d["t1"], -0.078),
                axes.c2p(d["t1"], 0.078),
                dash_length=0.05,
                color=LIGHT_GRAY,
                stroke_width=1.0,
            )

            self.paced_play(
                FadeIn(box), FadeIn(lines[0]), FadeIn(lines[1]),
                FadeIn(guide0), FadeIn(guide1),
                run_time=0.55, pause=1.15,
            )
            self.paced_play(FadeIn(lines[2]), run_time=0.35, pause=1.15)
            self.paced_play(FadeIn(lines[3]), run_time=0.35, pause=1.15)
            self.paced_play(FadeIn(formula[0]), run_time=0.30, pause=0.35)
            self.paced_play(Write(formula[1]), run_time=0.72, pause=1.35)
            self.paced_play(FadeIn(lines[4]), run_time=0.35, pause=0.85)
            self.paced_play(FadeIn(lines[5]), run_time=0.35, pause=1.20)
            self.paced_play(Create(a_segments[global_i]), run_time=0.80, pause=1.45)
            self.paced_play(
                FadeOut(guide0), FadeOut(guide1),
                FadeOut(card), FadeOut(formula),
                run_time=0.35, pause=0.65,
            )

        completed = self.note_panel(
            "CONSTRUCTION COMPLETE",
            [
                "12 velocity intervals → 12 acceleration levels.",
                "Now interpret the sign, magnitude, and zero-acceleration intervals.",
            ],
            width=4.50,
            body_size=18,
        ).move_to([5.25, -0.35, 0])
        self.paced_play(FadeIn(completed), pause=2.00)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 05 — meaning of full graph
    # -------------------------------------------------------------------------
    def section_5_read_full_acceleration_graph(self) -> None:
        self.lecture_header(
            5,
            "READ THE COMPLETE ACCELERATION-TIME GRAPH",
            "The vertical position of each level tells both the sign and the strength of the velocity change.",
        )

        axes = self.acceleration_axes()
        labels = self.acceleration_axis_labels(axes)
        segs = self.acceleration_segments(axes)
        graph = VGroup(axes, labels, *segs)

        panel = self.figure_panel(
            graph,
            width=9.9,
            height=5.45,
            title="The full acceleration history",
            caption="Above zero: speeding up | on zero: constant velocity | below zero: slowing down",
        )
        panel.group.move_to([-2.15, -0.68, 0])

        strongest_pos = max(ACCEL_INTERVALS, key=lambda d: d["a"])
        strongest_neg = min(ACCEL_INTERVALS, key=lambda d: d["a"])

        notes = VGroup(
            self.note_panel(
                "LARGEST POSITIVE a",
                [
                    f"{strongest_pos['t0']:.0f}–{strongest_pos['t1']:.0f} min",
                    f"a ≈ {strongest_pos['a']:+.3f} m/s²",
                    "fastest increase of velocity",
                ],
                width=4.45,
                body_size=18,
            ),
            self.note_panel(
                "LARGEST NEGATIVE a",
                [
                    f"{strongest_neg['t0']:.0f}–{strongest_neg['t1']:.0f} min",
                    f"a ≈ {strongest_neg['a']:+.3f} m/s²",
                    "strongest braking",
                ],
                width=4.45,
                body_size=18,
            ),
            self.note_panel(
                "ZERO a",
                [
                    "horizontal v(t) intervals",
                    "velocity remains constant",
                    "zero acceleration does not mean zero velocity",
                ],
                width=4.45,
                body_size=18,
            ),
        ).arrange(DOWN, buff=0.18)
        notes.move_to([5.25, -0.68, 0])

        stage = VGroup(panel.group, notes)
        self.assert_content_safe(stage, "section 5")
        self.paced_play(FadeIn(panel.group), FadeIn(notes))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 06 — derive v = v0 + at
    # -------------------------------------------------------------------------
    def section_6_constant_acceleration_equations(self) -> None:
        self.lecture_header(
            6,
            "IF ACCELERATION IS CONSTANT, VELOCITY CHANGES LINEARLY",
            "Do not memorize the equation yet. Build it from the definition of acceleration one algebraic step at a time.",
        )

        step1 = self.formula_panel(
            r"a=\frac{\Delta v}{\Delta t}",
            width=4.4, height=1.00, font_size=39,
        )
        step2 = self.formula_panel(
            r"a=\frac{v-v_0}{t}",
            width=4.4, height=1.00, font_size=39,
        )
        step3 = self.formula_panel(
            r"at=v-v_0",
            width=4.4, height=1.00, font_size=39,
        )
        step4 = self.formula_panel(
            r"v_0+at=v",
            width=4.4, height=1.00, font_size=39,
        )
        final = self.formula_panel(
            r"\boxed{v=v_0+at}",
            width=5.4, height=1.18, font_size=43,
        )

        row1 = VGroup(step1, step2).arrange(RIGHT, buff=0.35)
        row2 = VGroup(step3, step4).arrange(RIGHT, buff=0.35)
        derivation = VGroup(row1, row2, final).arrange(DOWN, buff=0.22)
        derivation.move_to([0, 0.80, 0])

        meaning = self.note_panel(
            "READ THE SYMBOLS",
            [
                "v₀ = velocity at the start of the interval",
                "a = constant acceleration",
                "t = elapsed time",
                "v = velocity after time t",
            ],
            width=6.4,
            body_size=20,
        ).move_to([-3.65, -2.15, 0])

        graph_note = self.note_panel(
            "CONNECT IT TO THE GRAPH",
            [
                "constant a → constant slope on v(t)",
                "a > 0 → v rises linearly",
                "a = 0 → v stays constant",
                "a < 0 → v falls linearly",
            ],
            width=6.4,
            body_size=20,
        ).move_to([3.65, -2.15, 0])

        stage = VGroup(derivation, meaning, graph_note)
        self.assert_content_safe(stage, "section 6")

        self.paced_play(FadeIn(step1), pause=1.60)
        self.paced_play(FadeIn(step2, shift=RIGHT * 0.05), pause=1.60)
        self.paced_play(FadeIn(step3, shift=DOWN * 0.05), pause=1.60)
        self.paced_play(FadeIn(step4, shift=RIGHT * 0.05), pause=1.60)
        self.paced_play(FadeIn(final), pause=2.10)
        self.paced_play(FadeIn(meaning), pause=1.45)
        self.paced_play(FadeIn(graph_note), pause=1.80)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 07 — derive position equation from v-t area
    # -------------------------------------------------------------------------
    def section_7_position_equation_from_area(self) -> None:
        self.lecture_header(
            7,
            "FROM VELOCITY TO POSITION: AREA UNDER v(t)",
            "For constant acceleration, displacement is the area under the straight velocity-time graph.",
        )

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 8, 2],
            x_length=6.2,
            y_length=3.65,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.6, "include_ticks": True},
            tips=False,
        )
        t_end = 5.0
        v0 = 2.0
        v_end = 7.0
        line = Line(axes.c2p(0, v0), axes.c2p(t_end, v_end), color=BLACK_LINE, stroke_width=4.0)
        xlab = self.text("time", 16).next_to(axes.x_axis, DOWN, buff=0.17)
        ylab = self.text("velocity", 16).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.17)
        fig = VGroup(axes, line, xlab, ylab)

        left = self.figure_panel(
            fig,
            width=7.8,
            height=5.10,
            title="Displacement = area under the velocity graph",
            caption="Split the area into a rectangle and a triangle.",
        )

        area1 = self.formula_panel(
            r"A_{\mathrm{rect}}=v_0t",
            width=5.3, height=0.92, font_size=35,
        )
        area2a = self.formula_panel(
            r"A_{\triangle}=\frac12(\mathrm{base})(\mathrm{height})",
            width=5.3, height=0.92, font_size=31,
        )
        area2b = self.formula_panel(
            r"A_{\triangle}=\frac12(t)(at)=\frac12at^2",
            width=5.3, height=0.92, font_size=31,
        )
        combine = self.formula_panel(
            r"\Delta x=v_0t+\frac12at^2",
            width=5.3, height=1.00, font_size=36,
        )
        final_eq = self.formula_panel(
            r"\boxed{x=x_0+v_0t+\frac12at^2}",
            width=5.5, height=1.15, font_size=38,
        )
        right = VGroup(area1, area2a, area2b, combine, final_eq).arrange(DOWN, buff=0.14)

        layout = self.split_layout(
            left.group,
            right,
            left_width=7.9,
            right_width=5.6,
            max_height=5.25,
            gap=0.55,
            center_y=-0.45,
        )
        self.assert_content_safe(layout.group, "section 7")

        rect = Polygon(
            axes.c2p(0, 0),
            axes.c2p(t_end, 0),
            axes.c2p(t_end, v0),
            axes.c2p(0, v0),
            stroke_color=MID_GRAY,
            stroke_width=1.5,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.65,
        )
        tri = Polygon(
            axes.c2p(0, v0),
            axes.c2p(t_end, v0),
            axes.c2p(t_end, v_end),
            stroke_color=BLACK_LINE,
            stroke_width=1.4,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.55,
        )

        self.paced_play(FadeIn(left.group), pause=1.30)
        self.paced_play(FadeIn(rect), pause=1.00)
        self.paced_play(FadeIn(area1), pause=1.45)
        self.paced_play(FadeIn(tri), pause=1.00)
        self.paced_play(FadeIn(area2a), pause=1.35)
        self.paced_play(FadeIn(area2b), pause=1.55)
        self.paced_play(FadeIn(combine), pause=1.70)
        self.paced_play(FadeIn(final_eq), pause=2.20)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 08 — Galileo bridge
    # -------------------------------------------------------------------------
    def section_8_why_galileo_inclined_plane(self) -> None:
        self.lecture_header(
            8,
            "WHY USE AN INCLINED PLANE?",
            "The goal is not to change the idea of accelerated motion. The goal is to slow it down enough to measure it carefully.",
        )

        # LEFT — free fall: short distance covered very quickly.
        fall_track = Line([0, 1.55, 0], [0, -1.55, 0], color=BLACK_LINE, stroke_width=3.0)
        fall_ball = Circle(
            radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to(fall_track.get_start())
        fall_label = self.text("FREE FALL", 20, BOLD).next_to(fall_track, UP, buff=0.20)
        fall_note = self.text("motion is very fast", 17).next_to(fall_track, DOWN, buff=0.20)
        fall_fig = VGroup(fall_track, fall_ball, fall_label, fall_note)
        fall_panel = self.figure_panel(
            fall_fig,
            width=5.65,
            height=4.20,
            title="Problem: difficult timing",
            caption="A short fall happens quickly, so small timing errors matter a lot.",
        )

        # RIGHT — inclined plane: longer path and slower motion.
        ramp = Line([-2.20, -1.35, 0], [2.05, 1.20, 0], color=BLACK_LINE, stroke_width=3.5)
        floor = Line([-2.45, -1.35, 0], [2.45, -1.35, 0], color=LIGHT_GRAY, stroke_width=1.8)
        ramp_ball = Circle(
            radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to(ramp.get_end())
        ramp_label = self.text("INCLINED PLANE", 20, BOLD).next_to(ramp, UP, buff=0.30)
        ramp_note = self.text("same acceleration idea, easier to observe", 16).next_to(floor, DOWN, buff=0.16)
        ramp_fig = VGroup(ramp, floor, ramp_ball, ramp_label, ramp_note)
        ramp_panel = self.figure_panel(
            ramp_fig,
            width=7.25,
            height=4.20,
            title="Galileo's strategy",
            caption="Use a gentler path so the change of motion unfolds over more measurable time.",
        )

        comparison = self.split_layout(
            fall_panel.group,
            ramp_panel.group,
            left_width=5.8,
            right_width=7.4,
            max_height=4.35,
            gap=0.60,
            center_y=0.05,
        )

        idea = self.note_panel(
            "WHAT STAYS THE SAME?",
            [
                "Gravity still makes the velocity change.",
                "For a fixed slope, the acceleration along the track is approximately constant.",
                "That is exactly the condition behind our constant-acceleration equations.",
            ],
            width=12.8,
            body_size=20,
        ).move_to([0, -2.95, 0])

        stage = VGroup(comparison.group, idea)
        self.assert_content_safe(stage, "section 8")

        # Re-anchor moving balls after layout transformations.
        fall_ball.move_to(fall_track.get_start())
        ramp_ball.move_to(ramp.get_end())

        self.paced_play(FadeIn(fall_panel.group), pause=1.20)
        self.paced_play(
            fall_ball.animate.move_to(fall_track.get_end()),
            run_time=0.55,
            rate_func=rate_functions.ease_in_quad,
            pause=1.60,
        )
        fall_ball.move_to(fall_track.get_start())

        self.paced_play(FadeIn(ramp_panel.group), pause=1.30)
        self.paced_play(
            ramp_ball.animate.move_to(ramp.get_start()),
            run_time=2.20,
            rate_func=rate_functions.ease_in_quad,
            pause=1.80,
        )
        self.paced_play(FadeIn(idea), pause=2.20)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 09 — Galileo's actual measurement logic
    # -------------------------------------------------------------------------
    def section_9_galileo_measurement_prediction(self) -> None:
        self.lecture_header(
            9,
            "GALILEO'S TEST: DOES DISTANCE GROW LIKE t²?",
            "Start from rest, mark equal time intervals, measure distance, and compare the data with the prediction from constant acceleration.",
        )

        ramp = Line([-3.75, -2.20, 0], [2.30, 1.45, 0], color=BLACK_LINE, stroke_width=4.0)
        floor = Line([-4.00, -2.20, 0], [3.00, -2.20, 0], color=LIGHT_GRAY, stroke_width=1.8)
        ball = Circle(
            radius=0.20,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )

        ramp_fig = VGroup(ramp, floor, ball)
        left = self.figure_panel(
            ramp_fig,
            width=8.15,
            height=5.10,
            title="Equal-time measurements along the ramp",
            caption="Equal time steps do not produce equal distances when the ball accelerates.",
        )

        eq0 = self.formula_panel(r"v_0=0", width=5.25, height=0.82, font_size=32)
        eq1 = self.formula_panel(
            r"x=x_0+v_0t+\frac12at^2",
            width=5.25, height=0.95, font_size=32,
        )
        eq2 = self.formula_panel(
            r"x-x_0=\frac12at^2",
            width=5.25, height=0.95, font_size=34,
        )
        eq3 = self.formula_panel(
            r"\boxed{\frac{x-x_0}{t^2}=\frac12a=\mathrm{constant}}",
            width=5.25, height=1.05, font_size=31,
        )
        prediction = self.note_panel(
            "SQUARE-TIME PATTERN",
            [
                "t:     1    2    3    4",
                "t²:    1    4    9   16",
                "If a is constant, distance follows the same ratio.",
            ],
            width=5.25,
            body_size=19,
        )
        right = VGroup(eq0, eq1, eq2, eq3, prediction).arrange(DOWN, buff=0.13)

        layout = self.split_layout(
            left.group,
            right,
            left_width=8.25,
            right_width=5.35,
            max_height=5.25,
            gap=0.55,
            center_y=-0.45,
        )
        self.assert_content_safe(layout.group, "section 9")

        release = ramp.get_end()
        ball.move_to(release)

        time_values = [1, 2, 3, 4]
        square_values = [1, 4, 9, 16]
        marker_fracs = [1 - q / 16 for q in square_values]
        marker_points = [ramp.point_from_proportion(max(0.0, frac)) for frac in marker_fracs]

        marks = VGroup()
        mark_labels = VGroup()
        for t_value, point in zip(time_values, marker_points):
            mark = Line(DOWN * 0.12, UP * 0.12, color=BLACK_LINE, stroke_width=2.0)
            mark.rotate(ramp.get_angle() + PI / 2)
            mark.move_to(point)
            label = self.text(f"t={t_value}", 15, BOLD).next_to(point, DOWN, buff=0.18)
            marks.add(mark)
            mark_labels.add(label)

        test_note = self.note_panel(
            "WHAT STUDENTS WILL TEST NEXT",
            [
                "1. Measure t.",
                "2. Measure x - x₀.",
                "3. Calculate (x - x₀)/t².",
                "4. Ask whether the value stays approximately constant.",
            ],
            width=7.4,
            body_size=18,
        ).move_to([-0.20, -3.18, 0])

        self.paced_play(FadeIn(left.group), pause=1.10)
        self.paced_play(FadeIn(eq0), pause=1.15)
        self.paced_play(FadeIn(eq1), pause=1.45)
        self.paced_play(FadeIn(eq2), pause=1.60)
        self.paced_play(FadeIn(eq3), pause=1.90)
        self.paced_play(FadeIn(prediction), pause=1.80)

        self.paced_play(FadeIn(marks), FadeIn(mark_labels), pause=1.50)

        previous = release
        for point in marker_points:
            travel = Line(previous, point, color=LIGHT_GRAY, stroke_width=4.5)
            self.paced_play(
                FadeIn(travel),
                ball.animate.move_to(point),
                run_time=1.00,
                rate_func=linear,
                pause=1.20,
            )
            previous = point

        self.paced_play(FadeIn(test_note), pause=2.40)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
