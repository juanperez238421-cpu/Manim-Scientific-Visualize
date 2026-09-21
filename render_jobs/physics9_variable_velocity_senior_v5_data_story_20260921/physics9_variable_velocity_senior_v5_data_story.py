#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Variable velocity V5: data-story approach.

This rebuild is explicitly based on the pedagogical/visual approach of the
uploaded reference video "Class 5(3).mp4":

    observe motion -> organize measurements -> build a graph ->
    identify the mathematical/physical pattern -> explain the motion

The scene keeps the JP classroom render contract while adopting the reference
video's cleaner scientific lecture rhythm: one strong title, one short
subtitle, a central diagram/data object, and a step-by-step mathematical
construction.

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
# PHYSICAL DATA
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

ROUTE_EVENTS = [
    ("01", "Departure", "accelerate to 70 km/h", 0.10, 70),
    ("02", "Highway cruise", "hold 70 km/h", 0.27, 70),
    ("03", "Brake for lunch", "70 → 0 km/h", 0.38, 0),
    ("04", "Lunch stop", "15 min at rest", 0.38, 0),
    ("05", "Return to road", "0 → 65 km/h", 0.55, 65),
    ("06", "Accident zone", "65 → 25 km/h", 0.72, 25),
    ("07", "Heavy traffic", "25 → 10 km/h", 0.84, 10),
    ("08", "Traffic clears", "10 → 55 km/h", 0.96, 55),
]

GRAPH_STEPS = [
    ("01", "0–10", "0 → 70", "rising", 0),
    ("02", "10–35", "70", "horizontal", 1),
    ("03", "35–40", "70 → 0", "falling", 2),
    ("04", "40–55", "0", "horizontal on v = 0", 3),
    ("05", "55–60", "0 → 65", "rising", 4),
    ("06", "60–75", "65", "horizontal", 5),
    ("07", "75–82", "65 → 25", "falling", 6),
    ("08", "82–92", "25", "horizontal", 7),
    ("09", "92–100", "25 → 10", "falling", 8),
    ("10", "100–108", "10", "horizontal", 9),
    ("11", "108–115", "10 → 55", "rising", 10),
    ("12", "115–120", "55", "horizontal", 11),
]


def velocity_at(t_min: float) -> float:
    if t_min <= PROFILE[0][0]:
        return PROFILE[0][1]
    if t_min >= PROFILE[-1][0]:
        return PROFILE[-1][1]
    for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:]):
        if t0 <= t_min <= t1:
            alpha = (t_min - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    raise ValueError(t_min)


def position_at(t_min: float) -> float:
    samples = np.linspace(0.0, t_min, max(2, int(t_min * 12) + 2))
    values = np.array([velocity_at(float(t)) for t in samples])
    return float(np.trapezoid(values, samples / 60.0))


POSITIONS = [position_at(t) for t, _ in PROFILE]
FINAL_DISTANCE_KM = POSITIONS[-1]


# =============================================================================
# SCENE
# =============================================================================
class Physics9VariableVelocitySeniorV5DataStory(JPMathClassroomScene):
    """Reference-inspired data-to-law narrative for variable velocity."""

    def validate_lesson_data(self) -> None:
        assert_close(FINAL_DISTANCE_KM, 78.3333333333, tol=0.03, label="route distance")
        assert len(PROFILE) == 13
        assert len(GRAPH_STEPS) == 12
        assert velocity_at(47.0) == 0.0
        assert velocity_at(104.0) == 10.0
        assert abs(velocity_at(120.0) - 55.0) < 1e-9
        assert abs((70 / 3.6) / 600 - 0.0324074) < 1e-5
        assert abs((0 - 70 / 3.6) / 300 + 0.0648148) < 1e-5
        sample_t = np.linspace(0, 120, 241)
        x = [position_at(float(t)) for t in sample_t]
        assert all(b >= a - 1e-5 for a, b in zip(x[:-1], x[1:]))

    def construct(self) -> None:
        self.opening()
        self.section_1_uniform_motion()
        self.section_2_real_trip()
        self.section_3_measurement_log_a()
        self.section_4_measurement_log_b()
        self.section_5_construct_velocity_graph()
        self.section_6_position_graph()
        self.section_7_acceleration()
        self.section_8_connected_story()
        self.standard_closing(
            "Measure the motion. Then let the data reveal how velocity changes."
        )

    # -------------------------------------------------------------------------
    # Reference-inspired scientific header
    # -------------------------------------------------------------------------
    def lecture_header(self, number: int, title: str, subtitle: str) -> None:
        kicker = self.text("PHYSICS 9  |  KINEMATICS", 19, BOLD)
        badge = RoundedRectangle(
            width=0.62, height=0.42, corner_radius=0.07,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 17, BOLD).move_to(badge)
        title_mob = self.text(title, 30, BOLD)
        title_row = VGroup(VGroup(badge, badge_text), title_mob).arrange(RIGHT, buff=0.20)
        self.fit(title_row, 14.2, 0.50)
        subtitle_mob = self.text(subtitle, 18)
        self.fit(subtitle_mob, 14.0, 0.45)
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
            fading = [old_header]
            if old_subtitle is not None:
                fading.append(old_subtitle)
            self.play(*[FadeOut(m) for m in fading], run_time=0.32)
        self.play(FadeIn(new_header), FadeIn(subtitle_mob), run_time=0.38)

    # -------------------------------------------------------------------------
    # Reusable assets
    # -------------------------------------------------------------------------
    def make_car(self, scale: float = 1.0) -> VGroup:
        body = RoundedRectangle(
            width=1.25, height=0.42, corner_radius=0.08,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        )
        roof = Polygon(
            [-0.34, 0.21, 0], [-0.13, 0.48, 0],
            [0.32, 0.48, 0], [0.48, 0.21, 0],
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        wheels = VGroup(
            Circle(0.11, stroke_color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1).move_to([-0.38, -0.23, 0]),
            Circle(0.11, stroke_color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1).move_to([0.38, -0.23, 0]),
        )
        return VGroup(body, roof, wheels).scale(scale)

    def make_road(self, width: float = 9.0, height: float = 0.95) -> VGroup:
        road = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=LIGHT_GRAY, fill_opacity=0.55,
        )
        dashes = VGroup(*[
            Line(LEFT * 0.15, RIGHT * 0.15, color=WHITE, stroke_width=4)
            for _ in range(max(7, int(width / 0.75)))
        ])
        dashes.arrange(RIGHT, buff=0.34).move_to(road)
        dashes.scale_to_fit_width(width - 0.55)
        return VGroup(road, dashes)

    def speed_box(self, value: float = 0) -> tuple[VGroup, DecimalNumber]:
        label = self.text("speed", 18, BOLD)
        number = DecimalNumber(value, num_decimal_places=0, font_size=38, color=BLACK_TEXT)
        unit = self.text("km/h", 18).next_to(number, RIGHT, buff=0.10)
        unit.add_updater(lambda m: m.next_to(number, RIGHT, buff=0.10))
        row = VGroup(number, unit)
        content = VGroup(label, row).arrange(DOWN, buff=0.10)
        box = RoundedRectangle(
            width=2.45, height=1.12, corner_radius=0.08,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content), number

    def event_note(self, number: str, title: str, detail: str, width: float = 7.5) -> VGroup:
        badge = RoundedRectangle(
            width=0.58, height=0.44, corner_radius=0.07,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        )
        badge_text = self.text(number, 16, BOLD).move_to(badge)
        t = self.text(title, 23, BOLD)
        d = self.text(detail, 19)
        text_block = VGroup(t, d).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        content = VGroup(VGroup(badge, badge_text), text_block).arrange(RIGHT, buff=0.18)
        self.fit(content, width - 0.35, 0.82)
        box = RoundedRectangle(
            width=width, height=1.08, corner_radius=0.08,
            stroke_color=BLACK_LINE, stroke_width=1.4,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.22)
        return VGroup(box, content)

    def progress_dots(self, count: int, active: int) -> VGroup:
        group = VGroup()
        for i in range(1, count + 1):
            circ = Circle(
                radius=0.18,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_color=BLACK_LINE if i == active else WHITE_FILL,
                fill_opacity=1,
            )
            lab = Text(
                str(i), font_size=13,
                color=WHITE if i == active else BLACK_TEXT,
                weight=BOLD,
            ).move_to(circ)
            group.add(VGroup(circ, lab))
        group.arrange(RIGHT, buff=0.22)
        line = Line(
            group[0].get_center(), group[-1].get_center(),
            color=LIGHT_GRAY, stroke_width=1.5,
        ).set_z_index(-1)
        return VGroup(line, group)

    def simple_table(self, headers: list[str], rows: list[list[str]], widths: list[float]) -> VGroup:
        row_h = 0.48
        cell_rows = VGroup()
        all_rows = [headers] + rows
        for r, row in enumerate(all_rows):
            cells = VGroup()
            for text_value, width in zip(row, widths):
                rect = Rectangle(
                    width=width, height=row_h,
                    stroke_color=BLACK_LINE if r == 0 else LIGHT_GRAY,
                    stroke_width=1.2 if r == 0 else 0.9,
                    fill_color=VERY_LIGHT_GRAY if r == 0 else WHITE_FILL,
                    fill_opacity=1,
                )
                txt = self.text(text_value, 16 if r else 17, BOLD if r == 0 else NORMAL)
                self.fit(txt, width - 0.18, row_h - 0.10)
                txt.move_to(rect)
                cells.add(VGroup(rect, txt))
            cells.arrange(RIGHT, buff=0)
            cell_rows.add(cells)
        cell_rows.arrange(DOWN, buff=0)
        return cell_rows

    def graph_axes(self, kind: str) -> Axes:
        y_range = [0, 85, 10]
        if kind == "position":
            y_range = [0, 85, 10]
        return Axes(
            x_range=[0, 120, 20],
            y_range=y_range,
            x_length=7.75,
            y_length=3.65,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.7, "include_ticks": True},
            tips=False,
        )

    def axis_numbers(self, axes: Axes, y_step: int = 20) -> VGroup:
        labels = VGroup()
        for x in range(0, 121, 20):
            lab = self.text(str(x), 13).next_to(axes.c2p(x, 0), DOWN, buff=0.07)
            labels.add(lab)
        for y in range(y_step, 81, y_step):
            lab = self.text(str(y), 13).next_to(axes.c2p(0, y), LEFT, buff=0.07)
            labels.add(lab)
        return labels

    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9  |  KINEMATICS",
            "FROM UNIFORM MOTION TO A REALISTIC TRIP",
            "Observe motion → organize data → build graphs → explain changing velocity.",
            "Start with x = x_i + vt. Then ask what changes when one constant v is no longer enough.",
        )

    # -------------------------------------------------------------------------
    # 01 — uniform motion baseline
    # -------------------------------------------------------------------------
    def section_1_uniform_motion(self) -> None:
        self.lecture_header(
            1,
            "UNIFORM MOTION: EQUAL TIMES GIVE EQUAL DISTANCES",
            "Begin with the model we already understand: constant velocity.",
        )

        road = self.make_road(width=7.2)
        car = self.make_car(0.62)
        marks = VGroup()
        labels = VGroup()
        for i in range(4):
            x = -2.65 + i * 1.75
            tick = Line(DOWN * 0.12, UP * 0.12, color=BLACK_LINE, stroke_width=1.7).move_to([x, -0.48, 0])
            marks.add(tick)
            labels.add(self.text(f"{10*i} min", 14).next_to(tick, DOWN, buff=0.06))
        car.move_to([-2.65, 0.08, 0])
        road_group = VGroup(road, marks, labels, car)

        left = self.figure_panel(
            road_group, width=8.7, height=2.55,
            title="Example: v = 60 km/h",
            caption="Every 10 min the car covers the same 10 km.",
        )

        axes = Axes(
            x_range=[0, 30, 10], y_range=[0, 30, 10],
            x_length=4.3, y_length=2.45,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.5, "include_ticks": True},
            tips=False,
        )
        points = [axes.c2p(t, t) for t in (0, 10, 20, 30)]
        graph = VGroup(
            axes,
            Line(points[0], points[-1], color=BLACK_LINE, stroke_width=3),
            *[Dot(p, radius=0.06, color=BLACK_LINE) for p in points],
        )
        xlab = self.text("time (min)", 15).next_to(axes.x_axis, DOWN, buff=0.15)
        ylab = self.text("position (km)", 15).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.15)
        graph.add(xlab, ylab)
        right = self.figure_panel(
            graph, width=5.3, height=3.75,
            title="Straight position-time graph",
            caption="Constant slope → constant velocity.",
        )

        layout = self.split_layout(left.group, right.group, left_width=8.8, right_width=5.35, max_height=4.9, center_y=-0.65)
        self.assert_content_safe(layout.group, "uniform motion layout")

        formula = self.formula_panel(r"x=x_i+vt", width=4.0, height=0.95, font_size=34)
        formula.move_to([0, -3.25, 0])
        self.assert_content_safe(formula, "uniform formula")

        self.play(FadeIn(left.group), FadeIn(right.group), FadeIn(formula))
        xs = np.linspace(road[0].get_left()[0] + 0.55, road[0].get_right()[0] - 0.55, 4)
        car_y = road[0].get_center()[1] + 0.08
        car.move_to([xs[0], car_y, 0])
        for x in xs[1:]:
            self.play(car.animate.move_to([x, car_y, 0]), run_time=0.82, rate_func=linear)
            self.wait(PAUSE_SHORT * 0.35)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 02 — real trip story
    # -------------------------------------------------------------------------
    def section_2_real_trip(self) -> None:
        self.lecture_header(
            2,
            "WHAT IF THE TRIP DOES NOT KEEP ONE VELOCITY?",
            "A realistic road trip contains acceleration, stops, braking, traffic, and recovery.",
        )

        road = self.make_road(width=10.6)
        city_a = self.text("CITY A", 18, BOLD).next_to(road, LEFT, buff=0.16)
        city_b = self.text("CITY B", 18, BOLD).next_to(road, RIGHT, buff=0.16)
        car = self.make_car(0.62)
        route = VGroup(road, city_a, city_b, car)
        route_panel = self.figure_panel(
            route, width=12.6, height=2.35,
            title="Real trip: approximately 78 km",
            caption="One value of velocity is no longer enough.",
        )
        route_panel.group.move_to([0, 0.75, 0])

        speed_group, speed = self.speed_box(0)
        speed_group.move_to([5.35, -1.15, 0])
        progress = self.progress_dots(8, 1).move_to([0, -1.05, 0])
        note = self.event_note("01", "Departure", "accelerate to 70 km/h", width=8.7).move_to([-1.40, -2.35, 0])

        stage = VGroup(route_panel.group, speed_group, progress, note)
        self.assert_content_safe(stage, "real trip stage")

        road_left = road[0].get_left()[0] + 0.45
        road_right = road[0].get_right()[0] - 0.45
        car_y = road[0].get_center()[1] + 0.08
        car.move_to([road_left, car_y, 0])

        self.play(FadeIn(route_panel.group), FadeIn(speed_group), FadeIn(progress), FadeIn(note))

        current_progress = progress
        current_note = note
        for idx, (n, title, detail, frac, target_v) in enumerate(ROUTE_EVENTS, start=1):
            target_progress = self.progress_dots(8, idx).move_to(current_progress)
            target_note = self.event_note(n, title, detail, width=8.7).move_to(current_note)
            x = road_left + frac * (road_right - road_left)
            self.play(
                car.animate.move_to([x, car_y, 0]),
                ChangeDecimalToValue(speed, target_v),
                FadeOut(current_progress), FadeOut(current_note),
                run_time=0.92,
                rate_func=smooth,
            )
            self.play(FadeIn(target_progress), FadeIn(target_note), run_time=0.28)
            current_progress = target_progress
            current_note = target_note
            self.wait(PAUSE_SHORT * 0.42)

        conclusion = self.formula_panel(r"v=v(t)", width=3.6, height=0.90, font_size=36)
        conclusion.move_to([5.25, -2.35, 0])
        self.play(FadeOut(current_note), FadeIn(conclusion))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 03 — measurement log A
    # -------------------------------------------------------------------------
    def section_3_measurement_log_a(self) -> None:
        self.lecture_header(
            3,
            "MEASURE THE TRIP: RECORD EACH CHANGE POINT",
            "Like Galileo's data table, we organize the motion before trying to explain it.",
        )

        rows = []
        for (t, v), x in zip(PROFILE[:7], POSITIONS[:7]):
            rows.append([f"{t:.0f}", f"{v:.0f}", f"{x:.1f}"])
        table = self.simple_table(
            ["time (min)", "velocity (km/h)", "position (km)"],
            rows,
            [2.3, 2.9, 2.6],
        )
        table.move_to([-2.65, -0.55, 0])

        idea = self.note_panel(
            "FIRST HALF OF THE TRIP",
            [
                "0–10 min: acceleration",
                "10–35 min: constant 70 km/h",
                "35–40 min: braking",
                "40–55 min: lunch stop",
                "55–60 min: acceleration again",
            ],
            width=5.4, body_size=20,
        )
        idea.move_to([4.55, 0.25, 0])

        formula = self.formula_panel(
            r"\text{data first}\;\longrightarrow\;\text{graph second}",
            width=5.3, height=1.00, font_size=29,
        )
        formula.move_to([4.55, -2.35, 0])

        stage = VGroup(table, idea, formula)
        self.assert_content_safe(stage, "measurement log A")
        self.play(FadeIn(table[0]), FadeIn(idea), FadeIn(formula))
        for row in table[1:]:
            self.play(FadeIn(row, shift=UP * 0.04), run_time=0.38)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 04 — measurement log B
    # -------------------------------------------------------------------------
    def section_4_measurement_log_b(self) -> None:
        self.lecture_header(
            4,
            "CONTINUE THE LOG: ACCIDENT, TRAFFIC, RECOVERY",
            "The second half contains several different velocity regimes.",
        )

        rows = []
        for (t, v), x in zip(PROFILE[6:], POSITIONS[6:]):
            rows.append([f"{t:.0f}", f"{v:.0f}", f"{x:.1f}"])
        table = self.simple_table(
            ["time (min)", "velocity (km/h)", "position (km)"],
            rows,
            [2.3, 2.9, 2.6],
        )
        table.move_to([-2.65, -0.55, 0])

        idea = self.note_panel(
            "SECOND HALF OF THE TRIP",
            [
                "60–75 min: constant 65 km/h",
                "75–82 min: brake for accident",
                "82–92 min: pass at 25 km/h",
                "92–108 min: heavy traffic",
                "108–120 min: recovery + final cruise",
            ],
            width=5.4, body_size=20,
        )
        idea.move_to([4.55, 0.25, 0])

        result = self.note_panel(
            "WHAT THE LOG SHOWS",
            [
                "Velocity is not one number.",
                "It must be read interval by interval.",
            ],
            width=5.3, body_size=21,
        )
        result.move_to([4.55, -2.25, 0])

        stage = VGroup(table, idea, result)
        self.assert_content_safe(stage, "measurement log B")
        self.play(FadeIn(table[0]), FadeIn(idea), FadeIn(result))
        for row in table[1:]:
            self.play(FadeIn(row, shift=UP * 0.04), run_time=0.38)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 05 — build velocity graph
    # -------------------------------------------------------------------------
    def section_5_construct_velocity_graph(self) -> None:
        self.lecture_header(
            5,
            "FROM THE DATA TABLE TO THE VELOCITY-TIME GRAPH",
            "Construct the graph one interval at a time. Every interval has a physical meaning.",
        )

        axes = self.graph_axes("velocity")
        nums = self.axis_numbers(axes, y_step=10)
        xlab = self.text("time (min)", 17).next_to(axes.x_axis, DOWN, buff=0.28)
        ylab = self.text("velocity (km/h)", 17).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.34)
        graph_base = VGroup(axes, nums, xlab, ylab)
        panel = self.figure_panel(
            graph_base, width=9.7, height=5.45,
            title="Velocity-time graph",
            caption="Rising = speeding up   |   falling = slowing down   |   horizontal = constant velocity",
        )
        panel.group.move_to([-2.25, -0.45, 0])

        # Important: generate segments only after the final axes transformation.
        points = [axes.c2p(t, v) for t, v in PROFILE]
        segments = [
            Line(points[i], points[i + 1], color=BLACK_LINE, stroke_width=4.0)
            for i in range(12)
        ]

        step_title = self.text("STEP 01 / 12", 20, BOLD)
        interval = self.text("0–10 min", 20)
        change = self.text("0 → 70 km/h", 25, BOLD)
        shape = self.text("draw a rising line", 19)
        card_content = VGroup(step_title, interval, change, shape).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        card_box = RoundedRectangle(
            width=4.55, height=2.15, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        card_content.move_to(card_box).align_to(card_box, LEFT).shift(RIGHT * 0.28)
        card = VGroup(card_box, card_content).move_to([5.25, 0.70, 0])

        rules = self.note_panel(
            "DRAWING RULE",
            [
                "Read the interval.",
                "Read the velocity change.",
                "Connect the two endpoints.",
            ],
            width=4.55, body_size=20,
        )
        rules.move_to([5.25, -1.90, 0])

        stage = VGroup(panel.group, card, rules)
        self.assert_content_safe(stage, "velocity graph construction")
        self.play(FadeIn(panel.group), FadeIn(card), FadeIn(rules))

        current_card = card
        guides = VGroup()
        dots = VGroup()
        for i, (n, interval_text, velocity_text, graph_text, seg_idx) in enumerate(GRAPH_STEPS):
            title = self.text(f"STEP {n} / 12", 20, BOLD)
            interval_mob = self.text(f"{interval_text} min", 20)
            change_mob = self.text(f"{velocity_text} km/h", 25, BOLD)
            shape_mob = self.text(f"draw a {graph_text} line", 19)
            content = VGroup(title, interval_mob, change_mob, shape_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            box = RoundedRectangle(
                width=4.55, height=2.15, corner_radius=0.10,
                stroke_color=BLACK_LINE, stroke_width=1.5,
                fill_color=WHITE_FILL, fill_opacity=1,
            )
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
            target_card = VGroup(box, content).move_to(current_card)

            t1, v1 = PROFILE[seg_idx + 1]
            endpoint = Dot(axes.c2p(t1, v1), radius=0.055, color=BLACK_LINE)
            guide = DashedLine(
                axes.c2p(t1, 0), axes.c2p(t1, v1),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.2,
            ) if v1 > 0 else DashedLine(
                axes.c2p(0, 0), axes.c2p(t1, 0),
                dash_length=0.06, color=LIGHT_GRAY, stroke_width=1.2,
            )

            self.play(FadeOut(current_card), run_time=0.18)
            self.play(
                Create(segments[seg_idx]),
                FadeIn(endpoint),
                FadeIn(guide),
                FadeIn(target_card),
                run_time=0.78,
            )
            dots.add(endpoint)
            guides.add(guide)
            current_card = target_card
            self.wait(PAUSE_READ * 0.28)

        final = self.note_panel(
            "FINISHED GRAPH",
            [
                "One constant velocity cannot describe this trip.",
                "The full story is the function v(t).",
            ],
            width=4.55, body_size=20,
        ).move_to([5.25, 0.45, 0])

        self.play(FadeOut(current_card), FadeOut(rules), FadeOut(guides), FadeIn(final))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 06 — position graph from changing velocity
    # -------------------------------------------------------------------------
    def section_6_position_graph(self) -> None:
        self.lecture_header(
            6,
            "THE POSITION-TIME GRAPH CHANGES ITS SLOPE",
            "The velocity graph tells us how the slope of position must change.",
        )

        axes = self.graph_axes("position")
        nums = self.axis_numbers(axes, y_step=20)
        xlab = self.text("time (min)", 17).next_to(axes.x_axis, DOWN, buff=0.28)
        ylab = self.text("position (km)", 17).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.34)
        graph_base = VGroup(axes, nums, xlab, ylab)
        panel = self.figure_panel(
            graph_base, width=9.7, height=5.45,
            title="Position-time graph",
            caption="Large slope = fast   |   small slope = slow   |   flat = stopped",
        )
        panel.group.move_to([-2.25, -0.45, 0])

        # Piecewise construction: each interval is generated from the transformed axes.
        x_segments = []
        for (t0, _), (t1, _) in zip(PROFILE[:-1], PROFILE[1:]):
            ts = np.linspace(t0, t1, 36)
            pts = [axes.c2p(float(t), position_at(float(t))) for t in ts]
            x_segments.append(
                VMobject(stroke_color=BLACK_LINE, stroke_width=4.0).set_points_as_corners(pts)
            )

        note = self.note_panel(
            "CONNECT THE TWO GRAPHS",
            [
                "During lunch: v = 0 → x(t) is flat.",
                "In traffic: small v → small slope.",
                "After traffic clears: slope increases again.",
            ],
            width=4.6, body_size=20,
        )
        note.move_to([5.25, 0.45, 0])

        formula = self.formula_panel(
            r"v\;\longleftrightarrow\;\text{slope of }x(t)",
            width=4.6, height=1.00, font_size=31,
        )
        formula.move_to([5.25, -2.05, 0])

        stage = VGroup(panel.group, note, formula)
        self.assert_content_safe(stage, "position graph")
        self.play(FadeIn(panel.group), FadeIn(note), FadeIn(formula))

        for i, seg in enumerate(x_segments):
            self.play(Create(seg), run_time=0.48)
            if i in (2, 3, 8, 10):
                self.wait(PAUSE_SHORT * 0.28)

        stop_marker = Dot(axes.c2p(48, position_at(48)), radius=0.07, color=BLACK_LINE)
        traffic_marker = Dot(axes.c2p(104, position_at(104)), radius=0.07, color=BLACK_LINE)
        self.play(FadeIn(stop_marker), FadeIn(traffic_marker))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 07 — acceleration as quantified velocity change
    # -------------------------------------------------------------------------
    def section_7_acceleration(self) -> None:
        self.lecture_header(
            7,
            "ACCELERATION QUANTIFIES THE CHANGE IN VELOCITY",
            "Use the same data intervals to calculate how quickly velocity changes.",
        )

        formula = self.formula_panel(
            r"a_{\mathrm{avg}}=\frac{\Delta v}{\Delta t}",
            width=5.0, height=1.08, font_size=42,
        )
        formula.move_to([0, 1.65, 0])

        accel = self.note_panel(
            "STEP 01 — SPEEDING UP",
            [
                "0 → 70 km/h in 10 min",
                "70 km/h = 19.4 m/s",
                "10 min = 600 s",
            ],
            width=6.3, body_size=21,
        )
        accel.move_to([-3.45, -0.55, 0])
        accel_result = self.formula_panel(
            r"a_{\mathrm{avg}}\approx +0.032\;\mathrm{m/s^2}",
            width=5.7, height=0.95, font_size=32,
        )
        accel_result.next_to(accel, DOWN, buff=0.25)

        brake = self.note_panel(
            "STEP 03 — BRAKING",
            [
                "70 → 0 km/h in 5 min",
                "Δv = -19.4 m/s",
                "5 min = 300 s",
            ],
            width=6.3, body_size=21,
        )
        brake.move_to([3.45, -0.55, 0])
        brake_result = self.formula_panel(
            r"a_{\mathrm{avg}}\approx -0.065\;\mathrm{m/s^2}",
            width=5.7, height=0.95, font_size=32,
        )
        brake_result.next_to(brake, DOWN, buff=0.25)

        stage = VGroup(formula, accel, accel_result, brake, brake_result)
        self.assert_content_safe(stage, "acceleration section")
        self.play(FadeIn(formula[0]), Write(formula[1]))
        self.play(FadeIn(accel), FadeIn(brake))
        self.play(FadeIn(accel_result[0]), Write(accel_result[1]))
        self.play(FadeIn(brake_result[0]), Write(brake_result[1]))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # -------------------------------------------------------------------------
    # 08 — connected story
    # -------------------------------------------------------------------------
    def section_8_connected_story(self) -> None:
        self.lecture_header(
            8,
            "CONNECTED STORY: OBSERVE → MEASURE → MODEL → EXPLAIN",
            "The goal is not to memorize a graph. The goal is to reconstruct the motion from evidence.",
        )

        steps = [
            ("1", "OBSERVE", "The road conditions change the car's motion."),
            ("2", "MEASURE", "Record time, velocity, and position at change points."),
            ("3", "MODEL", "Build v(t) interval by interval and read x(t) slope."),
            ("4", "EXPLAIN", "Use acceleration to quantify velocity changes."),
        ]
        cards = VGroup()
        for n, title, body in steps:
            badge = RoundedRectangle(
                width=0.58, height=0.46, corner_radius=0.07,
                stroke_color=BLACK_LINE, stroke_width=1.5,
                fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
            )
            num = self.text(n, 17, BOLD).move_to(badge)
            t = self.text(title, 22, BOLD)
            b = self.text(body, 18)
            text_block = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            content = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.18)
            self.fit(content, 12.3, 0.80)
            box = RoundedRectangle(
                width=13.0, height=1.03, corner_radius=0.08,
                stroke_color=BLACK_LINE, stroke_width=1.3,
                fill_color=WHITE_FILL, fill_opacity=1,
            )
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
            cards.add(VGroup(box, content))
        cards.arrange(DOWN, buff=0.20).move_to([0, -0.25, 0])

        takeaway = self.formula_panel(
            r"\text{realistic motion}\;\Rightarrow\;v=v(t)",
            width=6.4, height=1.00, font_size=32,
        )
        takeaway.move_to([0, -3.25, 0])

        stage = VGroup(cards, takeaway)
        self.assert_content_safe(stage, "connected story")
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.05) for card in cards], lag_ratio=0.18),
            run_time=RUN_SLOW,
        )
        self.play(FadeIn(takeaway))
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
