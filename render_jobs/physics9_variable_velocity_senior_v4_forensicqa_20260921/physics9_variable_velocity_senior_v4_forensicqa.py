#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Variable velocity, senior V4, forensic-QA rebuild.

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

ROUTE_STEPS = [
    {"n": "01", "title": "Departure acceleration", "detail": "Speed rises from 0 to 70 km/h.", "fraction": 0.12, "speed": 70},
    {"n": "02", "title": "Highway cruise", "detail": "The car travels near 70 km/h.", "fraction": 0.28, "speed": 70},
    {"n": "03", "title": "Brake for lunch", "detail": "Speed falls from 70 to 0 km/h.", "fraction": 0.38, "speed": 0},
    {"n": "04", "title": "Lunch stop", "detail": "The car stays at the same position for 15 min.", "fraction": 0.38, "speed": 0},
    {"n": "05", "title": "Return to the road", "detail": "Speed rises again from 0 to 65 km/h.", "fraction": 0.55, "speed": 65},
    {"n": "06", "title": "Accident zone", "detail": "The driver reduces speed from 65 to 25 km/h.", "fraction": 0.72, "speed": 25},
    {"n": "07", "title": "Heavy traffic", "detail": "Traffic reduces the speed further to 10 km/h.", "fraction": 0.84, "speed": 10},
    {"n": "08", "title": "Traffic clears", "detail": "The car recovers speed and reaches 55 km/h.", "fraction": 0.96, "speed": 55},
]

GRAPH_STEPS = [
    {"n":"01","interval":"0–10 min","title":"Accelerate","detail":"0 → 70 km/h","graph":"rising line","segment":0,"t":10.0,"v":70.0},
    {"n":"02","interval":"10–35 min","title":"Cruise","detail":"70 km/h constant","graph":"horizontal line","segment":1,"t":35.0,"v":70.0},
    {"n":"03","interval":"35–40 min","title":"Brake","detail":"70 → 0 km/h","graph":"falling line","segment":2,"t":40.0,"v":0.0},
    {"n":"04","interval":"40–55 min","title":"Lunch stop","detail":"0 km/h constant","graph":"horizontal line on v = 0","segment":3,"t":55.0,"v":0.0},
    {"n":"05","interval":"55–60 min","title":"Re-accelerate","detail":"0 → 65 km/h","graph":"rising line","segment":4,"t":60.0,"v":65.0},
    {"n":"06","interval":"60–75 min","title":"Cruise","detail":"65 km/h constant","graph":"horizontal line","segment":5,"t":75.0,"v":65.0},
    {"n":"07","interval":"75–82 min","title":"Brake for accident","detail":"65 → 25 km/h","graph":"falling line","segment":6,"t":82.0,"v":25.0},
    {"n":"08","interval":"82–92 min","title":"Pass accident","detail":"25 km/h constant","graph":"horizontal line","segment":7,"t":92.0,"v":25.0},
    {"n":"09","interval":"92–100 min","title":"Enter heavy traffic","detail":"25 → 10 km/h","graph":"falling line","segment":8,"t":100.0,"v":10.0},
    {"n":"10","interval":"100–108 min","title":"Heavy traffic","detail":"10 km/h constant","graph":"horizontal line","segment":9,"t":108.0,"v":10.0},
    {"n":"11","interval":"108–115 min","title":"Recover speed","detail":"10 → 55 km/h","graph":"rising line","segment":10,"t":115.0,"v":55.0},
    {"n":"12","interval":"115–120 min","title":"Final cruise","detail":"55 km/h constant","graph":"horizontal line","segment":11,"t":120.0,"v":55.0},
]


# -----------------------------------------------------------------------------
# Kinematics helpers

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


class Physics9VariableVelocitySeniorV4ForensicQA(JPMathClassroomScene):
    """Forensic-QA rebuild with exact interval-by-interval graph construction."""

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

    def timeline_badges(self, count: int, active: int = 0) -> VGroup:
        """Compact numbered progress diagram. active is 1-based; 0 means none."""
        badges = VGroup()
        for i in range(1, count + 1):
            is_active = i == active
            box = RoundedRectangle(
                width=0.72,
                height=0.50,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.6,
                fill_color=BLACK_LINE if is_active else WHITE_FILL,
                fill_opacity=1.0,
            )
            label = Text(
                f"{i:02d}",
                font_size=17,
                color=WHITE if is_active else BLACK_TEXT,
                weight=BOLD,
            ).move_to(box)
            badges.add(VGroup(box, label))
        badges.arrange(RIGHT, buff=0.13)
        connector = Line(
            badges[0].get_left() + LEFT * 0.12,
            badges[-1].get_right() + RIGHT * 0.12,
            color=LIGHT_GRAY,
            stroke_width=2.0,
        )
        connector.set_z_index(-1)
        return VGroup(connector, badges)

    def graph_step_card(self, step: dict) -> VGroup:
        badge = self.text(f"STEP {step['n']} / 12", 20, BOLD)
        interval = self.text(step["interval"], 19, MEDIUM)
        title = self.text(step["title"], 25, BOLD)
        detail = self.text(step["detail"], 22)
        graph = self.text(f"Graph: {step['graph']}", 19)
        content = VGroup(
            VGroup(badge, interval).arrange(RIGHT, buff=0.22),
            title,
            detail,
            graph,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        self.fit(content, 4.45, 1.55)
        box = RoundedRectangle(
            width=4.85,
            height=1.95,
            corner_radius=0.11,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.23)
        return VGroup(box, content)

    def velocity_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 10],
            x_length=7.55,
            y_length=3.60,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )

    def position_axes(self) -> Axes:
        return Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 10],
            x_length=7.55,
            y_length=3.60,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
            tips=False,
        )

    def axis_number_labels(self, axes: Axes, *, y_step: int = 20) -> VGroup:
        labels = VGroup()
        for x in range(0, 121, 20):
            lab = self.text(str(x), 13)
            lab.next_to(axes.c2p(x, 0), DOWN, buff=0.08)
            labels.add(lab)
        for y in range(y_step, 81, y_step):
            lab = self.text(str(y), 13)
            lab.next_to(axes.c2p(0, y), LEFT, buff=0.08)
            labels.add(lab)
        return labels

    def build_velocity_segments(self, axes: Axes) -> list[Line]:
        pts = [axes.c2p(t, v) for t, v in PROFILE]
        return [
            Line(pts[i], pts[i + 1], color=BLACK_LINE, stroke_width=4.0)
            for i in range(len(pts) - 1)
        ]

    def build_position_curve(self, axes: Axes) -> VMobject:
        # Dense polyline: visually smooth, but without spline overshoot that could
        # distort the physical meaning of flat/transition regions.
        ts = np.linspace(0, 120, 300)
        points = [axes.c2p(float(t), position_at(float(t))) for t in ts]
        return VMobject(stroke_color=BLACK_LINE, stroke_width=4.0).set_points_as_corners(points)

    def guide_bundle(self, axes: Axes, t: float, y: float) -> VGroup:
        point = axes.c2p(t, y)
        dot = Dot(point, radius=0.075, color=BLACK_LINE)
        parts = [dot]
        if y > 1e-6:
            parts.append(
                DashedLine(
                    axes.c2p(t, 0), point,
                    dash_length=0.07, color=MID_GRAY, stroke_width=1.4,
                )
            )
            parts.append(
                DashedLine(
                    axes.c2p(0, y), point,
                    dash_length=0.07, color=MID_GRAY, stroke_width=1.4,
                )
            )
        else:
            parts.append(
                DashedLine(
                    axes.c2p(0, 0), point,
                    dash_length=0.07, color=MID_GRAY, stroke_width=1.4,
                )
            )
        return VGroup(*parts)

    # ------------------------------------------------------------------
    # Sections    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9",
            "WHEN VELOCITY STOPS BEING CONSTANT",
            "From an ideal constant-velocity model to a realistic two-city trip.",
            "We will connect the road story to x(t), then construct v(t) through 12 exact intervals.",
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
        x_local = np.linspace(-2.30, 2.30, 5)
        for tick, x in zip(ticks, x_local):
            tick.move_to([x, -0.47, 0])
        labels = VGroup(*[self.text(f"{15*i} min", 16) for i in range(5)])
        for label, tick in zip(labels, ticks):
            label.next_to(tick, DOWN, buff=0.08)
        car.move_to([x_local[0], road[0].get_center()[1] + 0.10, 0])
        visual = VGroup(road, ticks, labels, car)

        left_panel = self.figure_panel(
            visual,
            width=8.8,
            height=4.80,
            title="Ideal constant-velocity motion",
            caption="Equal time intervals → approximately equal changes in position.",
        )
        formula = self.formula_panel(r"x(t)=x_0+vt", width=4.55, height=1.18, font_size=38)
        idea = self.note_panel(
            "READ THE MODEL",
            [
                "Same distance in equal time.",
                "One velocity describes the whole trip.",
                "x(t) has one constant slope.",
            ],
            width=4.55,
            body_size=22,
        )
        right = VGroup(formula, idea).arrange(DOWN, buff=0.34)
        layout = self.split_layout(
            left_panel.group, right,
            left_width=9.0, right_width=4.65,
            max_height=5.25, center_y=-0.42,
        )
        self.assert_content_safe(layout.group, "section 1")

        # Recompute car targets AFTER the panel/layout transformations.
        # This prevents the moving car from leaving the road panel.
        road_left = road[0].get_left()[0] + 0.46
        road_right = road[0].get_right()[0] - 0.46
        car_y = road[0].get_center()[1] + 0.10
        car_positions = np.linspace(road_left, road_right, 5)
        car.move_to([car_positions[0], car_y, 0])
        assert all(
            road[0].get_left()[0] < x < road[0].get_right()[0]
            for x in car_positions
        )

        self.play(FadeIn(left_panel.group), FadeIn(right), run_time=RUN_NORMAL)
        for x in car_positions[1:]:
            self.play(car.animate.move_to([x, car_y, 0]), run_time=0.72, rate_func=linear)
            self.wait(PAUSE_SHORT * 0.35)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_2_storyboard(self) -> None:
        self.set_header(
            2,
            "THE REAL TRIP: EIGHT NUMBERED MOTION EVENTS",
            "The car accelerates, cruises, stops for lunch, slows for an accident, enters traffic, and later recovers speed.",
        )

        road = self.make_road(width=8.1)
        cities = self.make_city_markers(road)
        car = self.make_car(0.62)
        route_figure = VGroup(road, cities, car)

        route_panel = self.figure_panel(
            route_figure,
            width=9.65,
            height=2.55,
            title="Two-city route",
            caption="The active number below tells us which motion event is happening.",
        )
        route_panel.group.move_to([-2.10, 1.10, 0])

        # Compute road coordinates only after all panel transformations.
        road_left = road[0].get_left()[0] + 0.38
        road_right = road[0].get_right()[0] - 0.38
        car_y = road[0].get_center()[1] + 0.10
        car.move_to([road_left, car_y, 0])

        speed_panel, speed_number = self.speed_panel(0)
        speed_panel.move_to([5.55, 1.10, 0])

        timeline = self.timeline_badges(len(ROUTE_STEPS), active=0)
        timeline.move_to([0.0, -0.72, 0])

        active_card = self.event_card(
            "00", "Start at City A", "The car is initially at rest: v = 0 km/h.",
            width=9.8, height=1.42,
        )
        active_card.move_to([0.0, -2.55, 0])

        stage = VGroup(route_panel.group, speed_panel, timeline, active_card)
        self.assert_content_safe(stage, "section 2")
        self.play(FadeIn(route_panel.group), FadeIn(speed_panel), FadeIn(timeline), FadeIn(active_card))

        current_card = active_card
        current_timeline = timeline
        for idx, item in enumerate(ROUTE_STEPS, start=1):
            target_card = self.event_card(
                item["n"], item["title"], item["detail"],
                width=9.8, height=1.42,
            ).move_to(current_card)
            target_timeline = self.timeline_badges(len(ROUTE_STEPS), active=idx).move_to(current_timeline)

            x = road_left + item["fraction"] * (road_right - road_left)
            # Remove the previous event label BEFORE velocity changes.
            # This prevents a transient contradiction such as "Lunch stop"
            # being visible while the speed readout is already increasing.
            self.play(
                FadeOut(current_card),
                FadeOut(current_timeline),
                run_time=0.18,
            )
            self.play(
                car.animate.move_to([x, car_y, 0]),
                ChangeDecimalToValue(speed_number, item["speed"]),
                run_time=0.74 if idx != 4 else 0.48,
                rate_func=smooth,
            )
            self.play(
                FadeIn(target_card, shift=UP * 0.04),
                FadeIn(target_timeline),
                run_time=0.28,
            )
            current_card = target_card
            current_timeline = target_timeline
            self.wait(PAUSE_SHORT * (0.75 if idx == 4 else 0.42))

        idea = self.formula_panel(r"v=v(t)", width=3.8, height=1.00, font_size=40)
        idea.move_to([5.45, -2.55, 0])
        self.play(FadeOut(current_card), FadeIn(idea, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_3_position_graph(self) -> None:
        self.set_header(
            3,
            "POSITION-TIME GRAPH: READ THE SLOPE",
            "The slope of x(t) represents velocity. A changing slope means the velocity is changing.",
        )

        axes = self.position_axes()
        numbers = self.axis_number_labels(axes, y_step=20)
        x_label = self.text("time (min)", 18).next_to(axes.x_axis, DOWN, buff=0.30)
        y_label = self.text("position (km)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.35)
        fig = VGroup(axes, numbers, x_label, y_label)
        panel = self.figure_panel(
            fig,
            width=9.35,
            height=5.40,
            title="Position-time graph",
            caption="Read slope, compare intervals, then connect the slope to velocity.",
        )
        panel.group.move_to([-2.50, -0.45, 0])

        # Build the curve after panel movement so it uses transformed axes.
        curve = self.build_position_curve(axes)

        rule = self.note_panel(
            "THREE READING RULES",
            [
                "1. Steeper slope → larger velocity.",
                "2. Smaller slope → smaller velocity.",
                "3. Horizontal x(t) → v = 0.",
            ],
            width=4.75,
            body_size=21,
        )
        rule.move_to([5.15, 1.30, 0])

        current = self.event_card(
            "01", "Highway cruise", "A nearly constant slope corresponds to nearly constant velocity.",
            width=4.85, height=1.55,
        )
        current.move_to([5.15, -0.75, 0])

        summary = self.formula_panel(
            r"v\;\longleftrightarrow\;\text{slope of }x(t)",
            width=4.85, height=1.08, font_size=31,
        )
        summary.move_to([5.15, -2.55, 0])

        stage = VGroup(panel.group, rule, current, summary)
        self.assert_content_safe(stage, "section 3")
        self.play(FadeIn(panel.group), FadeIn(rule), FadeIn(current), FadeIn(summary))
        self.play(Create(curve), run_time=2.0)

        readings = [
            ("01", 25.0, "Highway cruise", "Nearly constant slope → nearly constant velocity."),
            ("02", 48.0, "Lunch stop", "Horizontal graph → position is constant → v = 0."),
            ("03", 85.0, "Accident zone", "Smaller slope → the car is moving more slowly."),
            ("04", 104.0, "Heavy traffic", "Very small slope → very small velocity."),
        ]
        guide = None
        for n, t, title, detail in readings:
            target = self.event_card(n, title, detail, width=4.85, height=1.55).move_to(current)
            new_guide = self.guide_bundle(axes, t, position_at(t))
            anims = [FadeOut(current)]
            if guide is not None:
                anims.append(FadeOut(guide))
            self.play(*anims, run_time=RUN_QUICK * 0.65)
            self.play(FadeIn(target), FadeIn(new_guide), run_time=RUN_QUICK)
            current = target
            guide = new_guide
            self.wait(PAUSE_READ * 0.55)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_4_velocity_graph_construction(self) -> None:
        self.set_header(
            4,
            "VELOCITY-TIME GRAPH: CONSTRUCT ALL 12 INTERVALS",
            "Each line segment comes directly from one time interval in the trip. No interval is skipped or merged.",
        )

        axes = self.velocity_axes()
        numbers = self.axis_number_labels(axes, y_step=10)
        x_label = self.text("time (min)", 18).next_to(axes.x_axis, DOWN, buff=0.30)
        y_label = self.text("velocity (km/h)", 18).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.35)
        base_fig = VGroup(axes, numbers, x_label, y_label)
        graph_panel = self.figure_panel(
            base_fig,
            width=9.45,
            height=5.45,
            title="Velocity-time graph",
            caption="Build one exact interval at a time: rising, falling, or horizontal.",
        )
        graph_panel.group.move_to([-2.45, -0.45, 0])

        formula = self.formula_panel(r"v=v(t)", width=4.55, height=1.00, font_size=40)
        formula.move_to([5.20, 1.95, 0])

        rules = self.note_panel(
            "HOW TO DRAW EACH INTERVAL",
            [
                "Rising line → velocity increases.",
                "Falling line → velocity decreases.",
                "Horizontal line → velocity is constant.",
            ],
            width=4.75,
            body_size=20,
        )
        rules.move_to([5.20, 0.55, 0])

        current_card = self.graph_step_card(GRAPH_STEPS[0])
        current_card.move_to([5.20, -1.55, 0])

        stage = VGroup(graph_panel.group, formula, rules, current_card)
        self.assert_content_safe(stage, "section 4")
        self.play(FadeIn(graph_panel.group), FadeIn(formula), FadeIn(rules), FadeIn(current_card))

        # Segments are generated after the panel transform; therefore every
        # endpoint is guaranteed to be expressed in the final graph coordinates.
        segments = self.build_velocity_segments(axes)
        current_guide = None
        permanent_dots = VGroup()

        for i, step in enumerate(GRAPH_STEPS):
            target_card = self.graph_step_card(step).move_to(current_card)
            new_guide = self.guide_bundle(axes, step["t"], step["v"])
            endpoint = Dot(axes.c2p(step["t"], step["v"]), radius=0.055, color=BLACK_LINE)

            fade_anims = [FadeOut(current_card)]
            if current_guide is not None:
                fade_anims.append(FadeOut(current_guide))
            self.play(*fade_anims, run_time=0.24)

            self.play(
                Create(segments[step["segment"]]),
                FadeIn(target_card),
                FadeIn(new_guide),
                FadeIn(endpoint),
                run_time=0.72,
            )
            permanent_dots.add(endpoint)
            current_card = target_card
            current_guide = new_guide
            self.wait(PAUSE_READ * 0.34)

        if current_guide is not None:
            self.play(FadeOut(current_guide), run_time=RUN_QUICK * 0.6)

        final_note = self.note_panel(
            "WHAT THE FINISHED GRAPH SAYS",
            [
                "The car does not have one velocity for the whole trip.",
                "Every road event changes the shape of v(t).",
                "The 12 intervals preserve the actual sequence of motion.",
            ],
            width=4.75,
            body_size=20,
        )
        final_note.move_to([5.20, -1.10, 0])
        self.play(FadeOut(current_card), FadeOut(rules), FadeIn(final_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_5_acceleration_bridge(self) -> None:
        self.set_header(
            5,
            "VELOCITY CHANGE LEADS TO ACCELERATION",
            "Average acceleration measures the change in velocity divided by the time taken for that change.",
        )

        formula = self.formula_panel(
            r"a_{\mathrm{avg}}=\frac{\Delta v}{\Delta t}",
            width=5.6, height=1.18, font_size=43,
        )
        formula.move_to([0, 1.95, 0])

        example = self.note_panel(
            "WORKED EXAMPLE — INTERVAL 01",
            [
                "0 → 70 km/h in 10 min",
                "70 km/h = 19.4 m/s",
                "10 min = 600 s",
            ],
            width=6.55,
            body_size=22,
        )
        example.move_to([-3.65, -0.20, 0])

        result = self.formula_panel(
            r"a_{\mathrm{avg}}=\frac{19.4-0}{600}\approx 0.032\ \mathrm{m/s^2}",
            width=6.45, height=1.42, font_size=34,
        )
        meaning = self.note_panel(
            "SIGN OF ACCELERATION",
            [
                "positive → speeding up",
                "negative → braking",
                "approximately zero → constant velocity",
            ],
            width=6.45,
            body_size=21,
        )
        right = VGroup(result, meaning).arrange(DOWN, buff=0.34)
        right.move_to([3.65, -0.50, 0])

        stage = VGroup(formula, example, right)
        self.assert_content_safe(stage, "section 5")

        self.play(FadeIn(formula[0]), run_time=RUN_QUICK)
        self.play(Write(formula[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(example), run_time=RUN_NORMAL)
        self.play(FadeIn(result[0]), Write(result[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_6_summary(self) -> None:
        self.set_header(
            6,
            "FINAL SYNTHESIS",
            "A realistic motion model is built by connecting the road story, position-time slope, velocity-time intervals, and acceleration.",
        )

        ideal = self.note_panel(
            "IDEAL CONSTANT-VELOCITY MODEL",
            [
                "one value of v",
                "one constant slope in x(t)",
                "useful for simplified motion",
            ],
            width=6.35,
            body_size=23,
        )
        realistic = self.note_panel(
            "MORE REALISTIC MODEL",
            [
                "v changes with time",
                "the slope of x(t) changes",
                "v(t) is built interval by interval",
            ],
            width=6.35,
            body_size=23,
        )
        comparison = self.split_layout(
            ideal, realistic,
            left_width=6.45, right_width=6.45,
            max_height=3.20, gap=0.72, center_y=0.55,
        )

        steps = self.process_map(
            [
                ("01", "observe the road events"),
                ("02", "number the motion intervals"),
                ("03", "read slope on x(t)"),
                ("04", "construct all 12 v(t) intervals"),
            ],
            card_width=6.15,
            card_height=1.00,
            columns=2,
        )
        # Keep a dedicated vertical band between the comparison and the
        # 2x2 process map. This avoids any overlap with the bottom-row cards.
        steps.move_to([0, -2.72, 0])

        takeaway = self.formula_panel(
            r"\text{realistic motion}\;\Rightarrow\;v=v(t)",
            width=6.2, height=0.90, font_size=30,
        )
        takeaway.move_to([0, -1.28, 0])

        stage = VGroup(comparison.group, steps, takeaway)
        self.assert_content_safe(stage, "section 6")
        self.play(FadeIn(ideal), FadeIn(realistic))
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.06) for card in steps], lag_ratio=0.12),
            run_time=RUN_SLOW,
        )
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
