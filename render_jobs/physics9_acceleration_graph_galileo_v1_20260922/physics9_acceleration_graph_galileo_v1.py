#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Acceleration graph construction + Galileo bridge.

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


class Physics9AccelerationGraphGalileoV1(JPMathClassroomScene):
    """Step-by-step acceleration graph and constant-acceleration equations."""

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
        self.section_8_galileo_bridge()
        self.standard_closing(
            "Next: use an inclined plane to test the prediction x proportional to t squared."
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
            self.play(*fades, run_time=0.30)

        self.play(FadeIn(new_header), FadeIn(subtitle_mob), run_time=0.36)

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
        self.play(FadeIn(panel.group), FadeIn(rule), FadeIn(formula))
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

        self.play(FadeIn(left.group), FadeIn(right))
        self.play(Create(run), Create(rise), FadeIn(dv), FadeIn(dt), run_time=0.9)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 03 — a(t), first half
    # -------------------------------------------------------------------------
    def section_3_build_acceleration_graph_first_half(self) -> None:
        self.lecture_header(
            3,
            "BUILD THE ACCELERATION GRAPH — INTERVALS 01 TO 06",
            "For each interval: read Δv, read Δt, calculate a, then draw a horizontal level on a(t).",
        )

        axes = self.acceleration_axes()
        labels = self.acceleration_axis_labels(axes)
        base = VGroup(axes, labels)

        panel = self.figure_panel(
            base,
            width=9.65,
            height=5.45,
            title="Acceleration-time graph",
            caption="Because each v(t) segment is linear, acceleration is constant inside each interval.",
        )
        panel.group.move_to([-2.25, -0.45, 0])

        # Generate graph levels after the axes reach their final coordinates.
        a_segments = self.acceleration_segments(axes)

        current_card = self.interval_card(ACCEL_INTERVALS[0], width=4.50).move_to([5.25, 0.65, 0])
        current_formula = self.slope_formula_card(ACCEL_INTERVALS[0], width=4.50).move_to([5.25, -2.00, 0])

        stage = VGroup(panel.group, current_card, current_formula)
        self.assert_content_safe(stage, "section 3")
        self.play(FadeIn(panel.group), FadeIn(current_card), FadeIn(current_formula))

        for i, d in enumerate(ACCEL_INTERVALS[:6]):
            target_card = self.interval_card(d, width=4.50).move_to(current_card)
            target_formula = self.slope_formula_card(d, width=4.50).move_to(current_formula)

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

            if i > 0:
                self.play(FadeOut(current_card), FadeOut(current_formula), run_time=0.18)
                self.play(FadeIn(target_card), FadeIn(target_formula), run_time=0.22)

            self.play(
                FadeIn(guide0),
                FadeIn(guide1),
                Create(a_segments[i]),
                run_time=0.76,
            )
            self.wait(PAUSE_READ * 0.30)
            self.play(FadeOut(guide0), FadeOut(guide1), run_time=0.16)
            current_card = target_card
            current_formula = target_formula

        summary = self.note_panel(
            "FIRST HALF PATTERN",
            [
                "positive → zero → negative → zero → positive → zero",
                "The graph alternates whenever the road conditions change.",
            ],
            width=4.50,
            body_size=18,
        ).move_to([5.25, -0.35, 0])

        self.play(FadeOut(current_card), FadeOut(current_formula), FadeIn(summary))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 04 — a(t), second half
    # -------------------------------------------------------------------------
    def section_4_build_acceleration_graph_second_half(self) -> None:
        self.lecture_header(
            4,
            "COMPLETE THE ACCELERATION GRAPH — INTERVALS 07 TO 12",
            "Continue exactly the same construction rule for the accident zone, traffic, recovery, and final cruise.",
        )

        axes = self.acceleration_axes()
        labels = self.acceleration_axis_labels(axes)
        base = VGroup(axes, labels)

        panel = self.figure_panel(
            base,
            width=9.65,
            height=5.45,
            title="Acceleration-time graph",
            caption="The first six levels are already known. Now complete the second half.",
        )
        panel.group.move_to([-2.25, -0.45, 0])

        # Build levels only after panel placement; first six are prior knowledge.
        a_segments = self.acceleration_segments(axes)
        known_levels = VGroup(*a_segments[:6])

        current_card = self.interval_card(ACCEL_INTERVALS[6], width=4.50).move_to([5.25, 0.65, 0])
        current_formula = self.slope_formula_card(ACCEL_INTERVALS[6], width=4.50).move_to([5.25, -2.00, 0])

        stage = VGroup(panel.group, current_card, current_formula)
        self.assert_content_safe(stage, "section 4")
        self.play(FadeIn(panel.group), FadeIn(known_levels), FadeIn(current_card), FadeIn(current_formula))

        for local_i, d in enumerate(ACCEL_INTERVALS[6:]):
            global_i = local_i + 6
            target_card = self.interval_card(d, width=4.50).move_to(current_card)
            target_formula = self.slope_formula_card(d, width=4.50).move_to(current_formula)

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

            if local_i > 0:
                self.play(FadeOut(current_card), FadeOut(current_formula), run_time=0.18)
                self.play(FadeIn(target_card), FadeIn(target_formula), run_time=0.22)

            self.play(
                FadeIn(guide0),
                FadeIn(guide1),
                Create(a_segments[global_i]),
                run_time=0.76,
            )
            self.wait(PAUSE_READ * 0.30)
            self.play(FadeOut(guide0), FadeOut(guide1), run_time=0.16)
            current_card = target_card
            current_formula = target_formula

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
        self.play(FadeIn(panel.group), FadeIn(notes))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 06 — derive v = v0 + at
    # -------------------------------------------------------------------------
    def section_6_constant_acceleration_equations(self) -> None:
        self.lecture_header(
            6,
            "IF ACCELERATION IS CONSTANT, VELOCITY CHANGES LINEARLY",
            "This is the key model we will use for Galileo's inclined-plane motion.",
        )

        step1 = self.formula_panel(
            r"a=\frac{\Delta v}{\Delta t}",
            width=4.2,
            height=1.00,
            font_size=39,
        )
        step2 = self.formula_panel(
            r"a=\frac{v-v_0}{t}",
            width=4.2,
            height=1.00,
            font_size=39,
        )
        step3 = self.formula_panel(
            r"at=v-v_0",
            width=4.2,
            height=1.00,
            font_size=39,
        )
        step4 = self.formula_panel(
            r"\boxed{v=v_0+at}",
            width=4.8,
            height=1.15,
            font_size=42,
        )
        row1 = VGroup(step1, step2).arrange(RIGHT, buff=0.28)
        row2 = VGroup(step3, step4).arrange(RIGHT, buff=0.28)
        derivation = VGroup(row1, row2).arrange(DOWN, buff=0.20)
        derivation.move_to([0, 1.00, 0])

        meaning = self.note_panel(
            "WHAT THE EQUATION SAYS",
            [
                "v₀ = initial velocity",
                "a = constant acceleration",
                "t = elapsed time",
                "v = velocity after time t",
            ],
            width=6.4,
            body_size=21,
        )
        meaning.move_to([-3.65, -1.65, 0])

        graph_note = self.note_panel(
            "GRAPH MEANING",
            [
                "constant a → straight line on v(t)",
                "slope of v(t) = a",
                "positive slope: v increases",
                "negative slope: v decreases",
            ],
            width=6.4,
            body_size=21,
        )
        graph_note.move_to([3.65, -1.65, 0])

        stage = VGroup(derivation, meaning, graph_note)
        self.assert_content_safe(stage, "section 6")
        self.play(FadeIn(step1))
        for box in (step2, step3, step4):
            self.play(FadeIn(box, shift=RIGHT * 0.05), run_time=0.45)
        self.play(FadeIn(meaning), FadeIn(graph_note))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 07 — derive position equation from v-t area
    # -------------------------------------------------------------------------
    def section_7_position_equation_from_area(self) -> None:
        self.lecture_header(
            7,
            "THE AREA UNDER v(t) GIVES DISPLACEMENT",
            "For constant acceleration, the area is a rectangle plus a triangle.",
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
        p0 = axes.c2p(0, v0)
        p1 = axes.c2p(t_end, v_end)
        line = Line(p0, p1, color=BLACK_LINE, stroke_width=4.0)
        xlab = self.text("time", 16).next_to(axes.x_axis, DOWN, buff=0.17)
        ylab = self.text("velocity", 16).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.17)
        fig = VGroup(axes, line, xlab, ylab)

        left = self.figure_panel(
            fig,
            width=7.8,
            height=5.10,
            title="Displacement = area under the velocity graph",
            caption="rectangle + triangle",
        )

        area1 = self.formula_panel(
            r"A_{\mathrm{rect}}=v_0t",
            width=5.3,
            height=0.92,
            font_size=35,
        )
        area2 = self.formula_panel(
            r"A_{\triangle}=\frac12(at)t=\frac12at^2",
            width=5.3,
            height=0.92,
            font_size=34,
        )
        combine = self.formula_panel(
            r"\Delta x=v_0t+\frac12at^2",
            width=5.3,
            height=1.00,
            font_size=36,
        )
        final_eq = self.formula_panel(
            r"\boxed{x=x_0+v_0t+\frac12at^2}",
            width=5.5,
            height=1.15,
            font_size=38,
        )
        right = VGroup(area1, area2, combine, final_eq).arrange(DOWN, buff=0.22)

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

        # Create the geometric areas after the axes have been placed by layout.
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

        self.play(FadeIn(left.group))
        self.play(FadeIn(rect), FadeIn(area1), run_time=0.55)
        self.play(FadeIn(tri), FadeIn(area2), run_time=0.55)
        self.play(FadeIn(combine), run_time=0.50)
        self.play(FadeIn(final_eq), run_time=0.55)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 08 — Galileo bridge
    # -------------------------------------------------------------------------
    def section_8_galileo_bridge(self) -> None:
        self.lecture_header(
            8,
            "NEXT: GALILEO'S INCLINED PLANE",
            "The inclined plane slows the motion enough to measure how distance grows with time.",
        )

        ramp = Line([-3.9, -2.1, 0], [2.2, 1.45, 0], color=BLACK_LINE, stroke_width=4.0)
        floor = Line([-4.2, -2.1, 0], [3.1, -2.1, 0], color=LIGHT_GRAY, stroke_width=2.0)
        ball = Circle(
            radius=0.22,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to([1.65, 1.12, 0])
        arrow = Arrow(
            [1.25, 0.90, 0],
            [-0.20, 0.05, 0],
            buff=0.05,
            color=BLACK_LINE,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12,
        )
        motion_label = self.text("motion down the ramp", 18, BOLD).next_to(arrow, UP, buff=0.08)

        theta_arc = Arc(
            radius=0.65,
            start_angle=0,
            angle=np.arctan2(3.55, 6.10),
            color=MID_GRAY,
            stroke_width=1.6,
        ).move_arc_center_to([-3.9, -2.1, 0])
        theta = MathTex(r"\theta", font_size=28, color=BLACK_TEXT).next_to(theta_arc, RIGHT, buff=0.03)

        ramp_fig = VGroup(ramp, floor, ball, arrow, motion_label, theta_arc, theta)
        left = self.figure_panel(
            ramp_fig,
            width=7.9,
            height=4.85,
            title="Galileo's measurement idea",
            caption="Use a gentler slope so the accelerated motion is easier to time and measure.",
        )

        start_from_rest = self.formula_panel(
            r"v_0=0",
            width=4.8,
            height=0.86,
            font_size=34,
        )
        general = self.formula_panel(
            r"x=x_0+v_0t+\frac12at^2",
            width=5.5,
            height=1.00,
            font_size=34,
        )
        simplify = self.formula_panel(
            r"\boxed{x-x_0=\frac12at^2}",
            width=5.5,
            height=1.10,
            font_size=38,
        )
        prediction = self.note_panel(
            "EXPERIMENTAL PREDICTION",
            [
                "if a is constant and the ball starts from rest:",
                "distance is proportional to t²",
                "1² : 2² : 3² : 4² = 1 : 4 : 9 : 16",
            ],
            width=5.5,
            body_size=19,
        )
        right = VGroup(start_from_rest, general, simplify, prediction).arrange(DOWN, buff=0.18)

        layout = self.split_layout(
            left.group,
            right,
            left_width=8.0,
            right_width=5.6,
            max_height=5.10,
            gap=0.55,
            center_y=-0.45,
        )
        self.assert_content_safe(layout.group, "section 8")

        # Re-anchor the ball to the transformed ramp before animation.
        ball.move_to(ramp.point_from_proportion(0.88))
        target = ramp.point_from_proportion(0.18)

        self.play(FadeIn(left.group), FadeIn(start_from_rest))
        self.play(FadeIn(general), run_time=0.45)
        self.play(FadeIn(simplify), run_time=0.45)
        self.play(FadeIn(prediction), run_time=0.55)

        self.play(ball.animate.move_to(target), run_time=1.20, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
