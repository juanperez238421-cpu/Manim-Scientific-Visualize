#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Variable velocity, senior V3, fully in English.

Main improvement goals requested by the user
--------------------------------------------
1. All narration and on-screen text in English.
2. Clearer step-by-step numbering of the route events.
3. A more explicit construction of the velocity-time graph.
4. More detailed visual construction logic, not only final static graphs.

Target: Manim Community Edition 0.20.x.
This file uses the local JP classroom style library if available.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from jp_classroom_style import *  # noqa: F401,F403,E402


# -----------------------------------------------------------------------------
# Motion profile (time in minutes, speed in km/h)
# -----------------------------------------------------------------------------
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

STEP_DATA = [
    {
        "n": "01",
        "title": "Acceleration",
        "detail": "0 to 70 km/h in the first 10 min",
        "graph": "rising segment",
        "time_label": "0-10 min",
    },
    {
        "n": "02",
        "title": "Cruising",
        "detail": "constant 70 km/h from min 10 to 35",
        "graph": "horizontal segment at 70",
        "time_label": "10-35 min",
    },
    {
        "n": "03",
        "title": "Lunch stop",
        "detail": "brake to 0, then remain stopped",
        "graph": "drop to 0 and horizontal on the axis",
        "time_label": "35-55 min",
    },
    {
        "n": "04",
        "title": "Accident zone",
        "detail": "return to the road, then slow to 25 km/h",
        "graph": "up, then down, then horizontal at 25",
        "time_label": "55-92 min",
    },
    {
        "n": "05",
        "title": "Heavy traffic and recovery",
        "detail": "slow to 10 km/h, then recover to 55 km/h",
        "graph": "down, horizontal at 10, then up",
        "time_label": "92-120 min",
    },
]


# -----------------------------------------------------------------------------
# Kinematics helpers
# -----------------------------------------------------------------------------
def velocity_at(t_min: float) -> float:
    """Piecewise-linear velocity profile."""
    if t_min <= PROFILE[0][0]:
        return PROFILE[0][1]
    if t_min >= PROFILE[-1][0]:
        return PROFILE[-1][1]
    for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:]):
        if t0 <= t_min <= t1:
            alpha = (t_min - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    raise ValueError(f"time outside profile: {t_min}")


def position_at(t_min: float) -> float:
    """Numerical integral of the profile, in kilometres."""
    samples = np.linspace(0.0, t_min, max(2, int(t_min * 6) + 2))
    values = np.array([velocity_at(float(t)) for t in samples])
    return float(np.trapezoid(values, samples / 60.0))


FINAL_DISTANCE_KM = position_at(120.0)


class Physics9VariableVelocitySeniorV3English(JPMathClassroomScene):
    """Full English revision with clearer numbered construction."""

    def validate_lesson_data(self) -> None:
        assert_close(FINAL_DISTANCE_KM, 78.3333333333, tol=0.02, label="final distance")
        assert abs(velocity_at(47.0) - 0.0) < 1e-9
        assert abs(velocity_at(104.0) - 10.0) < 1e-9
        assert abs(velocity_at(120.0) - 55.0) < 1e-9
        sample_t = np.linspace(0, 120, 121)
        positions = [position_at(float(t)) for t in sample_t]
        assert all(b >= a - 1e-6 for a, b in zip(positions[:-1], positions[1:]))
        assert all(velocity_at(float(t)) >= 0 for t in sample_t)

    # ------------------------------------------------------------------
    # Core scene flow
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening()
        self.section_1_mru_recap()
        self.section_2_storyboard()
        self.section_3_position_graph()
        self.section_4_velocity_graph_construction()
        self.section_5_acceleration_bridge()
        self.section_6_summary()
        self.standard_closing(
            "A more realistic description of motion follows how velocity changes with time."
        )

    # ------------------------------------------------------------------
    # Basic assets
    # ------------------------------------------------------------------
    def make_car(self, scale: float = 1.0) -> VGroup:
        body = RoundedRectangle(
            width=1.25,
            height=0.44,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        )
        roof = Polygon(
            [-0.34, 0.22, 0],
            [-0.13, 0.50, 0],
            [0.32, 0.50, 0],
            [0.48, 0.22, 0],
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        wheels = VGroup(
            Circle(0.115, color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1.0).move_to([-0.38, -0.24, 0]),
            Circle(0.115, color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1.0).move_to([0.38, -0.24, 0]),
        )
        return VGroup(body, roof, wheels).scale(scale)

    def make_road(self, width: float = 8.2, height: float = 1.08) -> VGroup:
        road = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.72,
        )
        dash_count = max(5, int(width / 0.85))
        lane = VGroup(*[
            Line(LEFT * 0.18, RIGHT * 0.18, color=WHITE, stroke_width=4.2)
            for _ in range(dash_count)
        ])
        lane.arrange(RIGHT, buff=0.38).move_to(road)
        lane.scale_to_fit_width(width - 0.55)
        return VGroup(road, lane)

    def make_city_markers(self, road: VGroup) -> VGroup:
        city_a = self.text("CITY A", 19, BOLD).next_to(road, LEFT, buff=0.14)
        city_b = self.text("CITY B", 19, BOLD).next_to(road, RIGHT, buff=0.14)
        return VGroup(city_a, city_b)

    def event_card(self, number: str, title: str, detail: str, *, width: float = 5.2, height: float = 1.25) -> VGroup:
        badge = RoundedRectangle(
            width=0.64,
            height=0.50,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        badge_text = self.text(number, 18, BOLD).move_to(badge)
        title_mob = self.text(title, 24, BOLD)
        detail_mob = self.text(detail, 20)
        text_group = VGroup(title_mob, detail_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        content = VGroup(VGroup(badge, badge_text), text_group).arrange(RIGHT, buff=0.20)
        self.fit(content, width - 0.35, height - 0.18)
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content)

    def speed_panel(self, value: float = 0.0) -> tuple[VGroup, DecimalNumber]:
        title = self.text("CAR SPEED", 20, BOLD)
        speed = DecimalNumber(value, num_decimal_places=0, font_size=44, color=BLACK_TEXT)
        unit = self.text("km/h", 21, MEDIUM).next_to(speed, RIGHT, buff=0.12)
        unit.add_updater(lambda mob: mob.next_to(speed, RIGHT, buff=0.12))
        numeric = VGroup(speed, unit)
        content = VGroup(title, numeric).arrange(DOWN, buff=0.14)
        box = RoundedRectangle(
            width=3.15,
            height=1.45,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content), speed

    def step_strip(self) -> VGroup:
        """Five numbered route steps, shown as a compact diagram."""
        cards = VGroup()
        for item in STEP_DATA:
            badge = RoundedRectangle(
                width=0.52,
                height=0.42,
                corner_radius=0.06,
                stroke_color=BLACK_LINE,
                stroke_width=1.5,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1,
            )
            badge_text = self.text(item["n"], 16, BOLD).move_to(badge)
            line1 = self.text(item["title"], 18, BOLD)
            line2 = self.text(item["time_label"], 16)
            text_block = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            content = VGroup(VGroup(badge, badge_text), text_block).arrange(RIGHT, buff=0.14)
            box = RoundedRectangle(
                width=2.65,
                height=0.92,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.3,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            )
            self.fit(content, 2.35, 0.70)
            content.move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.16)
        return cards

    def velocity_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 10],
            y_range=[0, 80, 10],
            x_length=7.4,
            y_length=3.55,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )

    def position_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 10],
            y_range=[0, 80, 10],
            x_length=7.4,
            y_length=3.55,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )

    def build_velocity_segments(self, axes: Axes) -> list[Line]:
        pts = [axes.c2p(t, v) for t, v in PROFILE]
        return [Line(pts[i], pts[i+1], color=BLACK_LINE, stroke_width=4.0) for i in range(len(pts) - 1)]

    def build_position_curve(self, axes: Axes) -> VMobject:
        ts = np.linspace(0, 120, 240)
        points = [axes.c2p(float(t), position_at(float(t))) for t in ts]
        return VMobject(stroke_color=BLACK_LINE, stroke_width=4.0).set_points_smoothly(points)

    def guide_bundle(self, axes: Axes, t: float, y: float) -> VGroup:
        dot = Dot(axes.c2p(t, y), radius=0.08, color=BLACK_LINE)
        vline = DashedLine(axes.c2p(t, 0), axes.c2p(t, y), dash_length=0.07, color=MID_GRAY, stroke_width=1.5)
        hline = DashedLine(axes.c2p(0, y), axes.c2p(t, y), dash_length=0.07, color=MID_GRAY, stroke_width=1.5)
        return VGroup(dot, vline, hline)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9",
            "WHEN VELOCITY STOPS BEING CONSTANT",
            "From ideal constant-speed motion to a more realistic two-city trip.",
            "We will observe the trip, number each event, and build the graphs step by step.",
        )

    def section_1_mru_recap(self) -> None:
        self.set_header(
            1,
            "STARTING POINT: CONSTANT VELOCITY",
            "In the ideal model, equal time intervals correspond to equal changes in position.",
        )

        road = self.make_road(width=6.0).move_to(ORIGIN)
        car = self.make_car(0.70)
        ticks = VGroup(*[
            Line(DOWN * 0.11, UP * 0.11, color=BLACK_LINE, stroke_width=2.0)
            for _ in range(5)
        ])
        x_positions = np.linspace(-2.30, 2.30, 5)
        for tick, x in zip(ticks, x_positions):
            tick.move_to([x, -0.47, 0])
        labels = VGroup(*[self.text(f"{15*i} min", 16) for i in range(5)])
        for label, tick in zip(labels, ticks):
            label.next_to(tick, DOWN, buff=0.08)
        car_y = road[0].get_center()[1] + 0.10
        car.move_to([x_positions[0], car_y, 0])
        visual = VGroup(road, ticks, labels, car)

        left_panel = self.figure_panel(
            visual,
            width=8.7,
            height=4.75,
            title="Ideal constant-speed motion",
            caption="The car covers approximately the same road length every 15 minutes.",
        )

        formula = self.formula_panel(r"x(t)=x_0+vt", width=4.7, height=1.18, font_size=38)
        idea = self.note_panel(
            "MAIN IDEA",
            [
                "One single velocity describes the whole trip.",
                "The slope of x(t) stays constant.",
                "This is useful, but it is only an ideal model.",
            ],
            width=4.7,
            body_size=20,
        )
        right = VGroup(formula, idea).arrange(DOWN, buff=0.34)
        layout = self.split_layout(left_panel.group, right, left_width=9.0, right_width=4.8, max_height=5.25, center_y=-0.42)
        self.assert_content_safe(layout.group, "section 1")

        self.play(FadeIn(left_panel.group), FadeIn(right), run_time=RUN_NORMAL)
        for x in x_positions[1:]:
            self.play(car.animate.move_to([x, car_y, 0]), run_time=0.72, rate_func=linear)
            self.wait(PAUSE_SHORT * 0.40)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_2_storyboard(self) -> None:
        self.set_header(
            2,
            "A MORE REALISTIC STORY OF THE TRIP",
            "Now the same trip includes a stop for lunch, an accident zone, traffic reduction, and later recovery.",
        )

        road = self.make_road(width=7.6)
        cities = self.make_city_markers(road)
        car = self.make_car(0.62)
        road_left = road[0].get_left()[0] + 0.35
        road_right = road[0].get_right()[0] - 0.35
        car.move_to([road_left, road[0].get_center()[1] + 0.10, 0])
        route_figure = VGroup(road, cities, car)

        route_panel = self.figure_panel(
            route_figure,
            width=8.95,
            height=2.55,
            title="Two-city route",
            caption="We will describe the motion using five numbered events.",
        )
        route_panel.group.move_to([-2.45, 1.15, 0])

        speed_panel, speed_number = self.speed_panel(0)
        speed_panel.move_to([5.10, 1.15, 0])

        strip = self.step_strip()
        strip.scale(0.92)
        strip.move_to([0.0, -0.65, 0])

        active_card = self.event_card("01", STEP_DATA[0]["title"], STEP_DATA[0]["detail"], width=6.1, height=1.35)
        active_card.move_to([0.0, -2.65, 0])

        stage = VGroup(route_panel.group, speed_panel, strip, active_card)
        self.assert_content_safe(stage, "section 2")
        self.play(FadeIn(route_panel.group), FadeIn(speed_panel), FadeIn(strip), FadeIn(active_card))

        fractions = [0.16, 0.34, 0.47, 0.74, 0.96]
        speed_targets = [70, 70, 0, 25, 55]
        current_card = active_card
        for item, frac, target_speed in zip(STEP_DATA, fractions, speed_targets):
            target_card = self.event_card(item["n"], item["title"], item["detail"], width=6.1, height=1.35)
            target_card.move_to(current_card)
            x = road_left + frac * (road_right - road_left)
            self.play(
                car.animate.move_to([x, road[0].get_center()[1] + 0.10, 0]),
                ChangeDecimalToValue(speed_number, target_speed),
                FadeOut(current_card),
                run_time=1.0,
                rate_func=smooth,
            )
            self.play(FadeIn(target_card, shift=UP * 0.05), run_time=0.30)
            current_card = target_card
            self.wait(PAUSE_SHORT * 0.50)

        idea = self.formula_panel(r"v=v(t)", width=3.7, height=1.00, font_size=40)
        idea.move_to([5.15, -2.70, 0])
        self.play(FadeIn(idea, shift=UP * 0.08))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_3_position_graph(self) -> None:
        self.set_header(
            3,
            "READING THE POSITION-TIME GRAPH",
            "The slope of x(t) tells us how fast position changes. Different slopes mean different velocities.",
        )

        axes = self.position_axes()
        curve = self.build_position_curve(axes)
        x_label = self.text("time (min)", 18).next_to(axes.x_axis, DOWN, buff=0.18)
        y_label = self.text("position (km)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)
        fig = VGroup(axes, x_label, y_label)
        panel = self.figure_panel(
            fig,
            width=9.0,
            height=5.35,
            title="Position-time graph",
            caption="Steeper slope means larger velocity. A horizontal stretch means the car is stopped.",
        )
        panel.group.move_to([-2.55, -0.45, 0])

        step_box = self.note_panel(
            "HOW TO READ IT",
            [
                "Step 1: Look at the slope.",
                "Step 2: Compare one interval with the next one.",
                "Step 3: Horizontal means velocity is zero.",
            ],
            width=4.85,
            body_size=19,
        )
        step_box.move_to([5.20, 1.35, 0])

        event_box = self.event_card("03", "Lunch stop", "The graph becomes horizontal because position does not change.", width=5.25, height=1.45)
        event_box.move_to([5.18, -0.55, 0])

        mini_steps = self.process_map(
            [
                ("01", "rising quickly"),
                ("02", "steady slope"),
                ("03", "flat segment"),
                ("04", "smaller slope"),
            ],
            card_width=2.38,
            card_height=0.90,
            columns=2,
        )
        mini_steps.scale(0.92)
        mini_steps.move_to([5.20, -2.55, 0])

        stage = VGroup(panel.group, step_box, event_box, mini_steps)
        self.assert_content_safe(stage, "section 3")

        self.play(FadeIn(panel.group), FadeIn(step_box), FadeIn(event_box), FadeIn(mini_steps))
        self.play(Create(curve), run_time=2.2)
        self.add(curve)

        guide = self.guide_bundle(axes, 48, position_at(48))
        self.play(FadeIn(guide), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_4_velocity_graph_construction(self) -> None:
        self.set_header(
            4,
            "BUILDING THE VELOCITY-TIME GRAPH STEP BY STEP",
            "This graph must show real changes of velocity with time, not only a single average value.",
        )

        axes = self.velocity_axes()
        x_label = self.text("time (min)", 18).next_to(axes.x_axis, DOWN, buff=0.18)
        y_label = self.text("velocity (km/h)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)
        base_fig = VGroup(axes, x_label, y_label)
        graph_panel = self.figure_panel(
            base_fig,
            width=8.95,
            height=5.35,
            title="Velocity-time graph",
            caption="We construct the graph interval by interval from the trip story.",
        )
        graph_panel.group.move_to([-2.55, -0.45, 0])

        formula = self.formula_panel(r"v=v(t)", width=4.2, height=1.05, font_size=41)
        formula.move_to([5.15, 1.95, 0])

        instructions = self.note_panel(
            "CONSTRUCTION RULE",
            [
                "1. Each event becomes one or more graph segments.",
                "2. Rising line: velocity increases.",
                "3. Falling line: velocity decreases.",
                "4. Horizontal line: velocity stays constant.",
            ],
            width=4.95,
            body_size=18,
        )
        instructions.move_to([5.15, 0.15, 0])

        step_card = self.event_card("01", STEP_DATA[0]["title"], STEP_DATA[0]["graph"], width=5.25, height=1.40)
        step_card.move_to([5.15, -2.55, 0])

        stage = VGroup(graph_panel.group, formula, instructions, step_card)
        self.assert_content_safe(stage, "section 4")
        self.play(FadeIn(graph_panel.group), FadeIn(formula), FadeIn(instructions), FadeIn(step_card))

        segments = self.build_velocity_segments(axes)
        groupings = [
            [0],
            [1],
            [2, 3],
            [4, 5, 6],
            [7, 8, 9, 10, 11],
        ]
        representative_points = [
            (10, 70),
            (35, 70),
            (55, 0),
            (82, 25),
            (120, 55),
        ]

        current_card = step_card
        current_guide = None
        for item, seg_ids, (t, v) in zip(STEP_DATA, groupings, representative_points):
            target_card = self.event_card(item["n"], item["title"], item["graph"], width=5.25, height=1.40)
            target_card.move_to(current_card)
            anims = [Create(segments[i]) for i in seg_ids]
            new_guide = self.guide_bundle(axes, t, v)
            if current_guide is None:
                self.play(*anims, FadeOut(current_card), run_time=1.25)
                self.play(FadeIn(target_card, shift=UP * 0.05), FadeIn(new_guide), run_time=0.35)
            else:
                self.play(*anims, FadeOut(current_card), FadeOut(current_guide), run_time=1.25)
                self.play(FadeIn(target_card, shift=UP * 0.05), FadeIn(new_guide), run_time=0.35)
            current_card = target_card
            current_guide = new_guide
            self.wait(PAUSE_READ * 0.45)

        key_message = self.note_panel(
            "KEY MESSAGE",
            [
                "A realistic trip does not use one constant velocity.",
                "The graph changes because the motion conditions change.",
            ],
            width=9.5,
            body_size=20,
        )
        key_message.move_to([0.0, -3.33, 0])
        self.play(FadeIn(key_message), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_5_acceleration_bridge(self) -> None:
        self.set_header(
            5,
            "WHEN VELOCITY CHANGES, ACCELERATION APPEARS",
            "Acceleration is the measure of how much velocity changes over a time interval.",
        )

        formula = self.formula_panel(
            r"a_{\mathrm{avg}}=\frac{\Delta v}{\Delta t}",
            width=6.2,
            height=1.30,
            font_size=45,
        )
        formula.move_to([0, 1.80, 0])

        map_cards = self.process_map(
            [
                ("01", "speeding up"),
                ("02", "constant velocity"),
                ("03", "braking"),
                ("04", "stopped"),
                ("05", "slowing in traffic"),
                ("06", "recovering speed"),
            ],
            card_width=4.20,
            card_height=1.05,
            columns=3,
        )
        map_cards.move_to([0, -0.15, 0])

        note = self.note_panel(
            "IMPORTANT PRECISION",
            [
                "In real motion, changes usually occur during time intervals.",
                "That is why an average acceleration is a useful first description.",
            ],
            width=11.2,
            body_size=20,
        )
        note.move_to([0, -2.95, 0])
        stage = VGroup(formula, map_cards, note)
        self.assert_content_safe(stage, "section 5")

        self.play(FadeIn(formula[0]), run_time=RUN_QUICK)
        self.play(Write(formula[1]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in map_cards], lag_ratio=0.10), run_time=RUN_SLOW)
        self.play(FadeIn(note))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_6_summary(self) -> None:
        self.set_header(
            6,
            "FINAL SUMMARY",
            "We started with constant velocity, then built a more realistic description using the route events and the graphs.",
        )

        left = self.note_panel(
            "CONSTANT-VELOCITY MODEL",
            [
                "one value of v for the whole motion",
                "x(t) has constant slope",
                "useful for simplified situations",
            ],
            width=6.3,
            body_size=21,
        )
        right = self.note_panel(
            "MORE REALISTIC MODEL",
            [
                "velocity changes with time",
                "the slope of x(t) changes",
                "the v(t) graph must be built interval by interval",
            ],
            width=6.3,
            body_size=21,
        )
        comparison = self.split_layout(
            left,
            right,
            left_width=6.45,
            right_width=6.45,
            max_height=3.4,
            gap=0.72,
            center_y=0.25,
        )

        steps = self.process_map(
            [
                ("1", "observe the trip"),
                ("2", "number the events"),
                ("3", "read x(t)"),
                ("4", "build v(t)"),
                ("5", "interpret acceleration"),
            ],
            card_width=2.55,
            card_height=1.00,
            columns=5,
        )
        steps.move_to([0, -2.80, 0])
        stage = VGroup(comparison.group, steps)
        self.assert_content_safe(stage, "section 6")

        self.play(FadeIn(left), FadeIn(right))
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in steps], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
