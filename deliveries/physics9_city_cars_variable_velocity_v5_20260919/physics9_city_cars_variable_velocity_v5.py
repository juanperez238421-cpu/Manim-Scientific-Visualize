#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — From Constant Velocity to Realistic Motion.

Direct continuation of the audited city-to-city two-car lesson.

Pedagogical focus
-----------------
1. Recall the ideal MRU model: both cars have constant velocity.
2. Disturb reality: lunch stop, accident stop, and heavy traffic.
3. Track Car A with a piecewise velocity model while Car B remains at -40 km/h.
4. Rebuild the velocity-time and position-time graphs.
5. Compare ideal and realistic meeting events.
6. Distinguish average velocity from the actual velocity at each interval.
7. Explain why real motion involves repeated/continuous velocity changes and therefore acceleration.
8. Close with the modeling idea: MRU is useful locally, but real motion is generally v(t).

Target: Manim Community Edition 0.20.1
Final render command:
    manim -pqh physics9_city_cars_variable_velocity_v5.py Physics9CityCarsVariableVelocityV5 \
        --format=mp4 --disable_caching
"""

from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *


# =============================================================================
# LESSON DATA — exact values used in every displayed calculation.
# =============================================================================
CITY_DISTANCE_KM = 240.0
X_A0_KM = 0.0
X_B0_KM = 240.0
V_B_KMH = -40.0

# Car A: start time, end time, velocity, event label.
A_SEGMENTS = (
    (0.00, 0.75, 80.0, "OPEN ROAD"),
    (0.75, 1.25, 0.0, "LUNCH STOP"),
    (1.25, 1.75, 60.0, "TRAFFIC BUILDS"),
    (1.75, 2.00, 0.0, "ACCIDENT AHEAD"),
    (2.00, 3.00, 30.0, "HEAVY TRAFFIC"),
)

A_BREAKS = (0.00, 0.75, 1.25, 1.75, 2.00, 3.00)
A_POSITIONS = (0.0, 60.0, 60.0, 90.0, 90.0, 120.0)
REAL_MEETING_TIME_H = 3.0
REAL_MEETING_X_KM = 120.0
AVERAGE_V_A_KMH = 40.0

# Previous ideal MRU result from the city-car lesson.
IDEAL_MEETING_TIME_H = 2.0
IDEAL_MEETING_X_KM = 160.0
IDEAL_V_A_KMH = 80.0

# Braking micro-example used to show that a real speed change is not instantaneous.
BRAKE_VI_KMH = 80.0
BRAKE_VI_MS = BRAKE_VI_KMH / 3.6
BRAKE_VF_MS = 0.0
BRAKE_DT_S = 8.0
BRAKE_A_MS2 = (BRAKE_VF_MS - BRAKE_VI_MS) / BRAKE_DT_S


def car_a_position(t: float) -> float:
    """Piecewise position of Car A in km for 0 <= t <= 3 h."""
    t = float(np.clip(t, A_BREAKS[0], A_BREAKS[-1]))
    x = X_A0_KM
    for t0, t1, v, _ in A_SEGMENTS:
        if t <= t0:
            break
        dt = min(t, t1) - t0
        if dt > 0:
            x += v * dt
        if t <= t1:
            break
    return x


def car_a_velocity(t: float) -> float:
    """Velocity of Car A in km/h for the active modeled interval."""
    t = float(np.clip(t, A_BREAKS[0], A_BREAKS[-1]))
    for idx, (t0, t1, v, _) in enumerate(A_SEGMENTS):
        if t0 <= t < t1:
            return v
        if idx == len(A_SEGMENTS) - 1 and math.isclose(t, t1):
            return v
    return A_SEGMENTS[-1][2]


def car_b_position(t: float) -> float:
    return X_B0_KM + V_B_KMH * t


def validate_variable_motion_data() -> None:
    # Cumulative position at every breakpoint.
    for t, expected in zip(A_BREAKS, A_POSITIONS):
        assert_close(car_a_position(t), expected, label=f"Car A x({t})")

    # New meeting event.
    assert_close(car_a_position(REAL_MEETING_TIME_H), REAL_MEETING_X_KM, label="Car A real meeting x")
    assert_close(car_b_position(REAL_MEETING_TIME_H), REAL_MEETING_X_KM, label="Car B real meeting x")
    assert_close(REAL_MEETING_X_KM / REAL_MEETING_TIME_H, AVERAGE_V_A_KMH, label="Car A average velocity")

    # Ideal comparison.
    ideal_t = CITY_DISTANCE_KM / (IDEAL_V_A_KMH + abs(V_B_KMH))
    ideal_x = IDEAL_V_A_KMH * ideal_t
    assert_close(ideal_t, IDEAL_MEETING_TIME_H, label="ideal meeting time")
    assert_close(ideal_x, IDEAL_MEETING_X_KM, label="ideal meeting x")

    # Braking micro-example.
    assert_close(BRAKE_VI_MS, 22.2222222222, tol=1e-8, label="80 km/h in m/s")
    assert_close(BRAKE_A_MS2, -2.7777777778, tol=1e-8, label="braking acceleration")


# =============================================================================
# MONOCHROME VISUAL PRIMITIVES — consistent with the JP classroom system.
# =============================================================================
def city_icon(label: str, variant: int = 0) -> VGroup:
    heights = (0.72, 1.12, 0.84) if variant == 0 else (0.92, 0.72, 1.18)
    widths = (0.48, 0.42, 0.56)
    blocks = VGroup()
    for width, height in zip(widths, heights):
        blocks.add(
            Rectangle(
                width=width,
                height=height,
                stroke_color=BLACK_LINE,
                stroke_width=2,
                fill_color=VERY_LIGHT_GRAY if variant else WHITE_FILL,
                fill_opacity=1,
            )
        )
    blocks.arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
    ground = Line(LEFT * 0.95, RIGHT * 0.95, color=BLACK_LINE, stroke_width=2.4)
    blocks.next_to(ground, UP, buff=0.0)
    roof = Triangle(stroke_color=BLACK_LINE, stroke_width=1.7, fill_opacity=0).scale(0.16)
    roof.next_to(blocks[1 if variant == 0 else 2], UP, buff=0.02)
    text = Text(label, font_size=21, color=BLACK_TEXT, weight=BOLD)
    text.next_to(ground, DOWN, buff=0.10)
    return VGroup(ground, blocks, roof, text)


def classroom_car(label: str, facing: int = 1, variant: int = 0, scale: float = 1.0) -> VGroup:
    """Directional car with an asymmetric nose; no color is required to show direction."""
    s = 1 if facing >= 0 else -1
    pts = [
        np.array([-1.28 * s, -0.17, 0]),
        np.array([-1.12 * s, 0.25, 0]),
        np.array([-0.45 * s, 0.42, 0]),
        np.array([0.18 * s, 0.41, 0]),
        np.array([0.68 * s, 0.24, 0]),
        np.array([1.22 * s, 0.13, 0]),
        np.array([1.36 * s, -0.17, 0]),
    ]
    body = Polygon(
        *pts,
        stroke_color=BLACK_LINE,
        stroke_width=2.5,
        fill_color=VERY_LIGHT_GRAY if variant else WHITE_FILL,
        fill_opacity=1,
    )
    cabin_pts = [
        np.array([-0.43 * s, 0.42, 0]),
        np.array([-0.05 * s, 0.80, 0]),
        np.array([0.51 * s, 0.75, 0]),
        np.array([0.76 * s, 0.25, 0]),
    ]
    cabin = Polygon(
        *cabin_pts,
        stroke_color=BLACK_LINE,
        stroke_width=2.0,
        fill_color=WHITE_FILL,
        fill_opacity=1,
    )
    windshield = Line(
        np.array([0.50 * s, 0.73, 0]),
        np.array([0.74 * s, 0.28, 0]),
        color=BLACK_LINE,
        stroke_width=2.3,
    )
    wheels = VGroup(
        *[
            Circle(
                radius=0.22,
                stroke_color=BLACK_LINE,
                stroke_width=2.4,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            ).move_to(np.array([x * s, -0.22, 0]))
            for x in (-0.80, 0.84)
        ]
    )
    hubs = VGroup(*[Dot(w.get_center(), radius=0.045, color=BLACK_LINE) for w in wheels])
    headlight = Dot(np.array([1.27 * s, 0.01, 0]), radius=0.055, color=BLACK_LINE)
    direction = Arrow(
        np.array([-0.62 * s, 1.04, 0]),
        np.array([0.62 * s, 1.04, 0]),
        buff=0,
        color=BLACK_LINE,
        stroke_width=4.0,
        max_tip_length_to_length_ratio=0.20,
    )
    car_label = Text(label, font_size=20, color=BLACK_TEXT, weight=BOLD)
    car_label.next_to(VGroup(body, cabin, wheels), DOWN, buff=0.10)
    return VGroup(body, cabin, windshield, wheels, hubs, headlight, direction, car_label).scale(scale)


def restaurant_icon() -> VGroup:
    plate = Circle(radius=0.34, stroke_color=BLACK_LINE, stroke_width=2.0, fill_opacity=0)
    fork = VGroup(
        Line([-0.48, -0.34, 0], [-0.48, 0.32, 0], color=BLACK_LINE, stroke_width=2.0),
        *[
            Line([-0.58 + i * 0.07, 0.18, 0], [-0.58 + i * 0.07, 0.34, 0], color=BLACK_LINE, stroke_width=1.4)
            for i in range(4)
        ],
    )
    knife = Line([0.50, -0.34, 0], [0.50, 0.34, 0], color=BLACK_LINE, stroke_width=2.0)
    label = Text("LUNCH", font_size=18, color=BLACK_TEXT, weight=BOLD).next_to(plate, DOWN, buff=0.10)
    return VGroup(plate, fork, knife, label)


def accident_icon() -> VGroup:
    tri = Triangle(stroke_color=BLACK_LINE, stroke_width=2.5, fill_color=WHITE_FILL, fill_opacity=1).scale(0.52)
    bang = Text("!", font_size=28, color=BLACK_TEXT, weight=BOLD).move_to(tri).shift(DOWN * 0.03)
    label = Text("ACCIDENT", font_size=18, color=BLACK_TEXT, weight=BOLD).next_to(tri, DOWN, buff=0.08)
    return VGroup(tri, bang, label)


def traffic_icon() -> VGroup:
    cars = VGroup()
    for i in range(3):
        shell = RoundedRectangle(
            width=0.74, height=0.34, corner_radius=0.08,
            stroke_color=BLACK_LINE, stroke_width=1.7,
            fill_color=VERY_LIGHT_GRAY if i % 2 else WHITE_FILL,
            fill_opacity=1,
        )
        wheels = VGroup(
            Circle(radius=0.07, stroke_color=BLACK_LINE, fill_color=WHITE_FILL, fill_opacity=1),
            Circle(radius=0.07, stroke_color=BLACK_LINE, fill_color=WHITE_FILL, fill_opacity=1),
        )
        wheels[0].move_to(shell.get_center() + LEFT * 0.23 + DOWN * 0.20)
        wheels[1].move_to(shell.get_center() + RIGHT * 0.23 + DOWN * 0.20)
        car = VGroup(shell, wheels).shift(RIGHT * (i - 1) * 0.88)
        cars.add(car)
    label = Text("HEAVY TRAFFIC", font_size=18, color=BLACK_TEXT, weight=BOLD).next_to(cars, DOWN, buff=0.12)
    return VGroup(cars, label)


def road_model(*, y: float = -0.15, left: float = -5.70, right: float = 5.70, show_events: bool = False):
    road = RoundedRectangle(
        width=(right - left) + 0.60,
        height=1.25,
        corner_radius=0.14,
        stroke_color=BLACK_LINE,
        stroke_width=1.8,
        fill_color=PAPER_GRAY,
        fill_opacity=1,
    ).move_to([(left + right) / 2, y, 0])
    center = DashedLine(
        [left + 0.12, y, 0], [right - 0.12, y, 0],
        dash_length=0.26, dashed_ratio=0.52,
        color=MID_GRAY, stroke_width=2.0,
    )
    top = Line([left, y + 0.47, 0], [right, y + 0.47, 0], color=BLACK_LINE, stroke_width=1.4)
    bottom = Line([left, y - 0.47, 0], [right, y - 0.47, 0], color=BLACK_LINE, stroke_width=1.4)

    city_a = city_icon("CITY A", 0).scale(0.78).move_to([left, y + 1.52, 0])
    city_b = city_icon("CITY B", 1).scale(0.78).move_to([right, y + 1.52, 0])
    zero = MathTex(r"0\ \mathrm{km}", font_size=25, color=BLACK_TEXT).move_to([left, y - 1.05, 0])
    twoforty = MathTex(r"240\ \mathrm{km}", font_size=25, color=BLACK_TEXT).move_to([right, y - 1.05, 0])

    def x_from_km(km: float) -> float:
        return left + (right - left) * (km / CITY_DISTANCE_KM)

    group = VGroup(road, center, top, bottom, city_a, city_b, zero, twoforty)
    event_group = VGroup()
    if show_events:
        lunch = restaurant_icon().scale(0.66).move_to([x_from_km(60), y + 1.42, 0])
        accident = accident_icon().scale(0.68).move_to([x_from_km(90), y + 1.42, 0])
        traffic = traffic_icon().scale(0.67).move_to([x_from_km(135), y - 1.25, 0])
        event_group.add(lunch, accident, traffic)
        group.add(event_group)
    return group, x_from_km, event_group


# =============================================================================
# MAIN LESSON
# =============================================================================
class Physics9CityCarsVariableVelocityV5(JPMathClassroomScene):
    """Professional Grade 9 bridge from MRU to changing velocity and acceleration."""

    def validate_lesson_data(self) -> None:
        validate_variable_motion_data()

    def construct(self) -> None:
        self.opening()
        self.scene_01_recall_ideal_model()
        self.scene_02_reality_interrupts()
        self.scene_03_piecewise_schedule()
        self.scene_04_live_two_car_motion()
        self.scene_05_velocity_time_graph()
        self.scene_06_position_time_graph()
        self.scene_07_compare_meeting_results()
        self.scene_08_average_vs_actual_velocity()
        self.scene_09_real_changes_need_acceleration()
        self.scene_10_modeling_summary()
        self.standard_closing(
            "Real motion is usually not one constant velocity: velocity changes with time, and acceleration describes that change."
        )

    # ------------------------------------------------------------------
    # 00 — OPENING
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9 / MOTION",
            "WHEN VELOCITY STOPS BEING CONSTANT",
            "The same two-city trip becomes more realistic when stops and traffic appear.",
            "MRU is a useful model — but real motion usually contains many velocity changes.",
        )

    # ------------------------------------------------------------------
    # 01 — RECALL IDEAL MODEL
    # ------------------------------------------------------------------
    def scene_01_recall_ideal_model(self) -> None:
        self.set_header(
            1,
            "START WITH THE IDEAL MODEL WE ALREADY KNOW",
            "In the previous city-car problem, both velocities were constant from start to meeting.",
        )
        road, _, _ = road_model(y=0.25, show_events=False)
        car_a = classroom_car("A", +1, 0, 0.50).move_to([-4.3, 0.53, 0])
        car_b = classroom_car("B", -1, 1, 0.50).move_to([4.3, -0.03, 0])
        eqs = VGroup(
            self.formula_panel(r"x_A=80t", width=4.5, height=1.00, font_size=39),
            self.formula_panel(r"x_B=240-40t", width=4.5, height=1.00, font_size=39),
            self.formula_panel(r"\boxed{t=2\ \mathrm{h},\ x=160\ \mathrm{km}}", width=5.7, height=1.00, font_size=37),
        ).arrange(RIGHT, buff=0.24).scale(0.88).move_to([0, -2.65, 0])
        question = self.note_panel(
            "THE HIDDEN ASSUMPTION",
            ["Each car keeps exactly the same velocity for the whole trip."],
            width=8.4, title_size=24, body_size=23,
        ).move_to([0, 2.00, 0])
        stage = VGroup(road, car_a, car_b, eqs, question)
        self.assert_content_safe(stage, "scene 01 ideal model")

        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.play(FadeIn(road), FadeIn(car_a), FadeIn(car_b), run_time=RUN_NORMAL)
        self.play(FadeIn(eqs[0]), FadeIn(eqs[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eqs[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 — REALITY INTERRUPTS
    # ------------------------------------------------------------------
    def scene_02_reality_interrupts(self) -> None:
        self.set_header(
            2,
            "NOW LET REAL LIFE ENTER THE MODEL",
            "A meal stop, an accident, and heavy traffic make Car A's velocity change several times.",
        )
        road, x_from_km, events = road_model(y=-0.35, show_events=True)
        car_a = classroom_car("A", +1, 0, 0.52).move_to([x_from_km(25), -0.08, 0])
        car_b = classroom_car("B", -1, 1, 0.52).move_to([x_from_km(215), -0.62, 0])
        data = self.key_value_panel(
            "NEW SITUATION",
            [
                ("Car B", r"-40\ \mathrm{km/h}\ \text{(still constant)}"),
                ("Car A", "velocity changes with the road conditions"),
                ("Goal", "describe motion without pretending one v works everywhere"),
            ],
            width=8.0, label_size=22, value_size=23,
        ).scale(0.83).move_to([0, 2.05, 0])
        stage = VGroup(road, car_a, car_b, data)
        self.assert_content_safe(stage, "scene 02 reality interrupts")

        self.play(FadeIn(data), run_time=RUN_NORMAL)
        self.play(FadeIn(road), FadeIn(car_a), FadeIn(car_b), run_time=RUN_NORMAL)
        for event in events:
            self.play(FadeIn(event, shift=UP * 0.08), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — PIECEWISE SCHEDULE
    # ------------------------------------------------------------------
    def scene_03_piecewise_schedule(self) -> None:
        self.set_header(
            3,
            "ONE CONSTANT VELOCITY IS NO LONGER ENOUGH",
            "Use one velocity for each interval, then accumulate displacement to update the position.",
        )
        rows = [
            ["0.00–0.75 h", r"+80", "open road", r"+60", r"60"],
            ["0.75–1.25 h", r"0", "lunch stop", r"0", r"60"],
            ["1.25–1.75 h", r"+60", "traffic builds", r"+30", r"90"],
            ["1.75–2.00 h", r"0", "accident stop", r"0", r"90"],
            ["2.00–3.00 h", r"+30", "heavy traffic", r"+30", r"120"],
        ]
        table = self.build_table(
            headers=("TIME", "v (km/h)", "EVENT", "Δx (km)", "x END (km)"),
            body_rows=rows,
            column_widths=(2.7, 2.1, 3.6, 2.3, 2.6),
            math_columns=(1, 3, 4),
            row_height=0.64,
            header_height=0.72,
            body_font_size=23,
            header_font_size=20,
        )
        table.group.move_to([0, -0.25, 0])
        rule = self.formula_panel(r"\Delta x=v\,\Delta t,\qquad x_{\mathrm{new}}=x_{\mathrm{old}}+\Delta x", width=9.6, height=1.02, font_size=36)
        rule.move_to([0, -3.36, 0])
        stage = VGroup(table.group, rule)
        self.assert_content_safe(stage, "scene 03 schedule table")

        self.animate_table_rows(table, include_header=True, pause=PAUSE_SHORT)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — LIVE TWO-CAR MOTION
    # ------------------------------------------------------------------
    def scene_04_live_two_car_motion(self) -> None:
        self.set_header(
            4,
            "WATCH TIME KEEP MOVING EVEN WHEN CAR A STOPS",
            "Car B continues toward the left while Car A alternates between moving, stopping, and slowing down.",
        )
        road, x_from_km, _ = road_model(y=0.55, show_events=True)
        t = ValueTracker(0.0)

        car_a = always_redraw(
            lambda: classroom_car("A", +1, 0, 0.48).move_to([x_from_km(car_a_position(t.get_value())), 0.80, 0])
        )
        car_b = always_redraw(
            lambda: classroom_car("B", -1, 1, 0.48).move_to([x_from_km(car_b_position(t.get_value())), 0.30, 0])
        )

        meet_x = x_from_km(REAL_MEETING_X_KM)
        meet_line = DashedLine([meet_x, -0.20, 0], [meet_x, 2.58, 0], color=BLACK_LINE, stroke_width=2.0)
        meet_label = MathTex(r"x=120\ \mathrm{km}", font_size=26, color=BLACK_TEXT).next_to(meet_line, UP, buff=0.07)

        info_box = RoundedRectangle(
            width=13.1, height=1.18, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE_FILL, fill_opacity=1,
        ).move_to([0, -2.72, 0])
        labels = ["t =", "vA =", "xA =", "xB =", "gap ="]
        numbers = [
            DecimalNumber(0.0, num_decimal_places=2, font_size=23, color=BLACK_TEXT),
            DecimalNumber(80.0, num_decimal_places=0, font_size=23, color=BLACK_TEXT),
            DecimalNumber(0.0, num_decimal_places=1, font_size=23, color=BLACK_TEXT),
            DecimalNumber(240.0, num_decimal_places=1, font_size=23, color=BLACK_TEXT),
            DecimalNumber(240.0, num_decimal_places=1, font_size=23, color=BLACK_TEXT),
        ]
        unit_text = ["h", "km/h", "km", "km", "km"]
        entries = VGroup()
        for lab, num, unit in zip(labels, numbers, unit_text):
            entries.add(VGroup(
                Text(lab, font_size=21, color=BLACK_TEXT, weight=BOLD),
                num,
                Text(unit, font_size=20, color=MID_GRAY),
            ).arrange(RIGHT, buff=0.06))
        entries.arrange(RIGHT, buff=0.42).move_to(info_box)

        numbers[0].add_updater(lambda m: m.set_value(t.get_value()))
        numbers[1].add_updater(lambda m: m.set_value(car_a_velocity(t.get_value())))
        numbers[2].add_updater(lambda m: m.set_value(car_a_position(t.get_value())))
        numbers[3].add_updater(lambda m: m.set_value(car_b_position(t.get_value())))
        numbers[4].add_updater(lambda m: m.set_value(max(0.0, car_b_position(t.get_value()) - car_a_position(t.get_value()))))

        stage = VGroup(road, meet_line, meet_label, info_box, entries)
        self.assert_content_safe(stage, "scene 04 live two car motion")
        self.play(FadeIn(road), FadeIn(car_a), FadeIn(car_b), run_time=RUN_NORMAL)
        self.play(Create(meet_line), FadeIn(meet_label), FadeIn(info_box), FadeIn(entries), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        # Move through every interval so the two stops are visible, not skipped.
        timeline = [
            (0.75, 2.4),
            (1.25, 1.8),
            (1.75, 2.0),
            (2.00, 1.25),
            (3.00, 3.2),
        ]
        for target, runtime in timeline:
            self.play(t.animate.set_value(target), run_time=runtime, rate_func=linear)
            self.wait(PAUSE_SHORT)

        self.play(Circumscribe(VGroup(car_a, car_b), color=BLACK_LINE, buff=0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        for num in numbers:
            num.clear_updaters()
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — VELOCITY–TIME GRAPH
    # ------------------------------------------------------------------
    def scene_05_velocity_time_graph(self) -> None:
        self.set_header(
            5,
            "THE VELOCITY–TIME GRAPH NOW HAS SEVERAL LEVELS",
            "A horizontal segment means constant velocity only inside that interval — not for the entire trip.",
        )
        axes = Axes(
            x_range=[0, 3.2, 0.5],
            y_range=[-60, 100, 20],
            x_length=8.2,
            y_length=5.0,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            tips=True,
        ).move_to([-2.65, -0.55, 0])
        x_lab = MathTex(r"t\ (\mathrm{h})", font_size=27, color=BLACK_TEXT).next_to(axes.x_axis.get_end(), DOWN, buff=0.10)
        y_lab = MathTex(r"v\ (\mathrm{km/h})", font_size=27, color=BLACK_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.09)

        a_lines = VGroup()
        transition_guides = VGroup()
        for i, (t0, t1, v, _) in enumerate(A_SEGMENTS):
            a_lines.add(Line(axes.c2p(t0, v), axes.c2p(t1, v), color=BLACK_LINE, stroke_width=3.1))
            if i < len(A_SEGMENTS) - 1:
                next_v = A_SEGMENTS[i + 1][2]
                transition_guides.add(
                    DashedLine(axes.c2p(t1, v), axes.c2p(t1, next_v), color=MID_GRAY, stroke_width=1.6, dash_length=0.10)
                )
        b_base = Line(axes.c2p(0, V_B_KMH), axes.c2p(3.0, V_B_KMH), color=BLACK_LINE, stroke_width=2.6)
        b_line = DashedVMobject(b_base, num_dashes=28)
        a_label = Text("Car A: 80 → 0 → 60 → 0 → 30", font_size=22, color=BLACK_TEXT, weight=BOLD)
        b_label = Text("Car B: constant −40 km/h (dashed)", font_size=22, color=BLACK_TEXT, weight=BOLD)
        legend = VGroup(a_label, b_label).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.55, 1.65, 0])
        note = self.note_panel(
            "WHAT THE GRAPH SAYS",
            [
                "v = 0 means stopped",
                "smaller positive v means slower forward motion",
                "each change in height is a change in velocity",
                "the vertical jump is a classroom idealization",
            ],
            width=5.0, title_size=24, body_size=21,
        ).move_to([4.55, -1.10, 0])
        stage = VGroup(axes, x_lab, y_lab, a_lines, transition_guides, b_line, legend, note)
        self.assert_content_safe(stage, "scene 05 velocity time graph")

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=RUN_NORMAL)
        for line in a_lines:
            self.play(Create(line), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.play(*[Create(g) for g in transition_guides], run_time=RUN_NORMAL)
        self.play(Create(b_line), FadeIn(legend), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — POSITION–TIME GRAPH
    # ------------------------------------------------------------------
    def scene_06_position_time_graph(self) -> None:
        self.set_header(
            6,
            "THE POSITION GRAPH CHANGES SLOPE WHEN VELOCITY CHANGES",
            "Steep rise, flat stop, gentler rise: the slope of x(t) is telling the velocity story.",
        )
        axes = Axes(
            x_range=[0, 3.2, 0.5],
            y_range=[0, 260, 40],
            x_length=8.2,
            y_length=5.0,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            tips=True,
        ).move_to([-2.65, -0.55, 0])
        x_lab = MathTex(r"t\ (\mathrm{h})", font_size=27, color=BLACK_TEXT).next_to(axes.x_axis.get_end(), DOWN, buff=0.10)
        y_lab = MathTex(r"x\ (\mathrm{km})", font_size=27, color=BLACK_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.09)

        a_points = [axes.c2p(t, x) for t, x in zip(A_BREAKS, A_POSITIONS)]
        a_graph = VMobject(color=BLACK_LINE, stroke_width=3.1)
        a_graph.set_points_as_corners(a_points)
        b_base = Line(axes.c2p(0, X_B0_KM), axes.c2p(3.0, REAL_MEETING_X_KM), color=BLACK_LINE, stroke_width=2.8)
        b_graph = DashedVMobject(b_base, num_dashes=30)
        meet = Dot(axes.c2p(REAL_MEETING_TIME_H, REAL_MEETING_X_KM), radius=0.08, color=BLACK_LINE)
        gx = DashedLine(axes.c2p(3, 0), axes.c2p(3, 120), color=MID_GRAY, stroke_width=1.4)
        gy = DashedLine(axes.c2p(0, 120), axes.c2p(3, 120), color=MID_GRAY, stroke_width=1.4)
        meet_lab = MathTex(r"(3\ \mathrm{h},\ 120\ \mathrm{km})", font_size=27, color=BLACK_TEXT).next_to(meet, UL, buff=0.12)

        slope_cards = VGroup(
            self.formula_panel(r"m=80", width=2.35, height=0.82, font_size=29),
            self.formula_panel(r"m=0", width=2.35, height=0.82, font_size=29),
            self.formula_panel(r"m=60", width=2.35, height=0.82, font_size=29),
            self.formula_panel(r"m=0", width=2.35, height=0.82, font_size=29),
            self.formula_panel(r"m=30", width=2.35, height=0.82, font_size=29),
        ).arrange(DOWN, buff=0.12).scale(0.88).move_to([4.55, -0.15, 0])
        label = Text("Car A slope = velocity", font_size=23, color=BLACK_TEXT, weight=BOLD).next_to(slope_cards, UP, buff=0.18)
        stage = VGroup(axes, x_lab, y_lab, a_graph, b_graph, meet, gx, gy, meet_lab, slope_cards, label)
        self.assert_content_safe(stage, "scene 06 position graph")

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=RUN_NORMAL)
        self.play(Create(a_graph), run_time=RUN_SLOW)
        self.play(Create(b_graph), run_time=RUN_SLOW)
        self.play(FadeIn(label), run_time=RUN_NORMAL)
        for card in slope_cards:
            self.play(FadeIn(card), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.play(Create(gx), Create(gy), FadeIn(meet), FadeIn(meet_lab), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — COMPARE IDEAL AND REAL MEETING
    # ------------------------------------------------------------------
    def scene_07_compare_meeting_results(self) -> None:
        self.set_header(
            7,
            "THE MEETING EVENT CHANGES WHEN THE VELOCITY HISTORY CHANGES",
            "Same cities, same Car B — but Car A's stops and slowdowns delay the meeting and move its location.",
        )
        left = self.note_panel(
            "IDEAL MRU MODEL",
            [
                "Car A: +80 km/h all the time",
                "Car B: −40 km/h all the time",
                "Meeting: 2.00 h",
                "Position: 160 km from City A",
            ],
            width=6.0, title_size=26, body_size=23,
        ).move_to([-3.55, -0.35, 0])
        right = self.note_panel(
            "VARIABLE-VELOCITY MODEL",
            [
                "Car A: 80 → 0 → 60 → 0 → 30 km/h",
                "Car B: −40 km/h",
                "Meeting: 3.00 h",
                "Position: 120 km from City A",
            ],
            width=6.0, title_size=26, body_size=23,
        ).move_to([3.55, -0.35, 0])
        delta = self.formula_panel(
            r"\Delta t=+1.00\ \mathrm{h},\qquad \Delta x_{\mathrm{meeting}}=-40\ \mathrm{km}",
            width=9.5, height=1.05, font_size=36,
        ).move_to([0, -3.25, 0])
        arrow = Arrow([-0.75, 1.95, 0], [0.75, 1.95, 0], buff=0.05, color=BLACK_LINE, stroke_width=3.2)
        caption = Text("same problem → more realistic assumptions", font_size=24, color=BLACK_TEXT, weight=BOLD).next_to(arrow, UP, buff=0.10)
        stage = VGroup(left, right, delta, arrow, caption)
        self.assert_content_safe(stage, "scene 07 ideal real comparison")

        self.play(FadeIn(left), run_time=RUN_NORMAL)
        self.play(GrowArrow(arrow), FadeIn(caption), run_time=RUN_NORMAL)
        self.play(FadeIn(right), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(delta), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — AVERAGE VS ACTUAL VELOCITY
    # ------------------------------------------------------------------
    def scene_08_average_vs_actual_velocity(self) -> None:
        self.set_header(
            8,
            "AVERAGE VELOCITY DOES NOT MEAN THE CAR MOVED AT THAT SPEED ALL THE TIME",
            "One number can summarize a trip, but it cannot reconstruct the full motion history.",
        )
        avg = self.formula_panel(
            r"\bar v_A=\frac{\Delta x}{\Delta t}=\frac{120-0}{3-0}=40\ \mathrm{km/h}",
            width=7.2, height=1.18, font_size=40,
        ).move_to([-3.40, 1.25, 0])
        actual = self.note_panel(
            "ACTUAL MODELED VELOCITIES",
            [
                "80 km/h on the open road",
                "0 km/h while eating",
                "60 km/h as traffic builds",
                "0 km/h at the accident stop",
                "30 km/h in heavy traffic",
            ],
            width=6.2, title_size=25, body_size=22,
        ).move_to([3.70, 0.30, 0])
        statement = self.note_panel(
            "INTERPRETATION",
            [
                "40 km/h is the trip's displacement-per-time average.",
                "It is not the velocity at every instant.",
                "To describe the motion in detail, we need v as a function of time.",
            ],
            width=7.2, title_size=25, body_size=22,
        ).move_to([-3.40, -1.25, 0])
        vt = self.formula_panel(r"\boxed{v=v(t)}", width=4.3, height=1.05, font_size=48).move_to([3.70, -2.55, 0])
        stage = VGroup(avg, actual, statement, vt)
        self.assert_content_safe(stage, "scene 08 average vs actual")

        self.play(FadeIn(avg), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(actual), run_time=RUN_NORMAL)
        self.play(FadeIn(statement), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(vt), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — REAL CHANGES REQUIRE ACCELERATION
    # ------------------------------------------------------------------
    def scene_09_real_changes_need_acceleration(self) -> None:
        self.set_header(
            9,
            "A REAL CAR DOES NOT JUMP FROM 80 km/h TO 0 INSTANTLY",
            "Braking and speeding up take time: during those intervals the velocity changes continuously.",
        )
        axes = Axes(
            x_range=[0, 9, 2],
            y_range=[0, 25, 5],
            x_length=6.8,
            y_length=4.6,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            tips=True,
        ).move_to([-3.65, -0.55, 0])
        x_lab = MathTex(r"t\ (\mathrm{s})", font_size=27, color=BLACK_TEXT).next_to(axes.x_axis.get_end(), DOWN, buff=0.10)
        y_lab = MathTex(r"v\ (\mathrm{m/s})", font_size=27, color=BLACK_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.08)
        brake = Line(axes.c2p(0, BRAKE_VI_MS), axes.c2p(BRAKE_DT_S, 0), color=BLACK_LINE, stroke_width=3.2)
        start_dot = Dot(axes.c2p(0, BRAKE_VI_MS), radius=0.07, color=BLACK_LINE)
        end_dot = Dot(axes.c2p(BRAKE_DT_S, 0), radius=0.07, color=BLACK_LINE)
        start_lab = MathTex(r"22.2\ \mathrm{m/s}", font_size=24, color=BLACK_TEXT).next_to(start_dot, UR, buff=0.10)
        end_lab = MathTex(r"0", font_size=24, color=BLACK_TEXT).next_to(end_dot, UL, buff=0.10)

        derivation = self.equation_stack(
            [
                r"80\ \mathrm{km/h}=22.2\ \mathrm{m/s}",
                r"a=\frac{\Delta v}{\Delta t}",
                r"a=\frac{0-22.2}{8}",
                r"\boxed{a\approx -2.78\ \mathrm{m/s^2}}",
            ],
            sizes=[32, 38, 38, 42], max_width=5.9, buff=0.28,
        ).move_to([3.75, 0.35, 0])
        insight = self.note_panel(
            "PHYSICAL MEANING",
            [
                "negative acceleration here means braking",
                "real driving contains many short acceleration/deceleration intervals",
                "the step graph is useful, but it is still a model",
            ],
            width=5.7, title_size=24, body_size=21,
        ).move_to([3.75, -2.15, 0])
        stage = VGroup(axes, x_lab, y_lab, brake, start_dot, end_dot, start_lab, end_lab, derivation, insight)
        self.assert_content_safe(stage, "scene 09 acceleration")

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=RUN_NORMAL)
        self.play(FadeIn(start_dot), FadeIn(start_lab), run_time=RUN_NORMAL)
        self.play(Create(brake), run_time=RUN_SLOW)
        self.play(FadeIn(end_dot), FadeIn(end_lab), run_time=RUN_NORMAL)
        self.animate_equation_stack(derivation, pause=PAUSE_READ)
        self.play(FadeIn(insight), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 — MODELING SUMMARY
    # ------------------------------------------------------------------
    def scene_10_modeling_summary(self) -> None:
        self.set_header(
            10,
            "FROM MRU TO A MORE REALISTIC DESCRIPTION OF MOTION",
            "The question is no longer only 'what is the velocity?' but 'how does the velocity change with time?'",
        )
        route = self.process_map(
            [
                ("1", "OBSERVE EVENTS"),
                ("2", "TRACK v(t)"),
                ("3", "READ x(t) SLOPE"),
                ("4", "IDENTIFY STOPS"),
                ("5", "MEASURE Δv/Δt"),
                ("6", "BUILD A BETTER MODEL"),
            ],
            card_width=4.35,
            card_height=1.16,
            columns=3,
        )
        route.move_to([0, -0.55, 0])
        takeaways = self.note_panel(
            "CORE IDEA",
            [
                "MRU: velocity is approximately constant over a chosen interval.",
                "Real motion: velocity often changes repeatedly and, during transitions, continuously.",
                "Acceleration is the quantity that describes how velocity changes with time.",
            ],
            width=11.7, title_size=26, body_size=23,
        ).move_to([0, -3.05, 0])
        stage = VGroup(route, takeaways)
        self.assert_content_safe(stage, "scene 10 summary")

        for card in route:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(takeaways), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()


if __name__ == "__main__":
    validate_variable_motion_data()
