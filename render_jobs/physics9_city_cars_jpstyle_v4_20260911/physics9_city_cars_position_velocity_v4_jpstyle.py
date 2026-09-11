#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — City-to-city motion, V4 JP Classroom Standard.

Pedagogical sequence:
physical road -> sign convention -> position equations -> meeting condition ->
live motion -> position-time graph -> velocity-time graph -> independent checks.

Target: Manim Community Edition 0.20.1
Final render: manim -pqh physics9_city_cars_position_velocity_v4_jpstyle.py Physics9CityCarsJPStyleV4
"""

from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *


# =============================================================================
# LESSON DATA — every displayed numerical claim is validated before animation.
# =============================================================================
CITY_DISTANCE_KM = 240.0
X_A0_KM = 0.0
X_B0_KM = 240.0
V_A_KMH = 80.0
V_B_KMH = -40.0
MEETING_TIME_H = 2.0
MEETING_X_KM = 160.0
DIST_A_KM = 160.0
DIST_B_KM = 80.0
RELATIVE_SPEED_KMH = 120.0


def validate_city_car_data() -> None:
    t = (X_B0_KM - X_A0_KM) / (V_A_KMH - V_B_KMH)
    x_a = X_A0_KM + V_A_KMH * t
    x_b = X_B0_KM + V_B_KMH * t
    assert_close(t, MEETING_TIME_H, label="meeting time")
    assert_close(x_a, MEETING_X_KM, label="Car A meeting position")
    assert_close(x_b, MEETING_X_KM, label="Car B meeting position")
    assert_close(abs(V_A_KMH - V_B_KMH), RELATIVE_SPEED_KMH, label="relative speed")
    assert_close(V_A_KMH * MEETING_TIME_H, DIST_A_KM, label="Car A distance")
    assert_close(abs(V_B_KMH) * MEETING_TIME_H, DIST_B_KM, label="Car B distance")
    assert_close(DIST_A_KM + DIST_B_KM, CITY_DISTANCE_KM, label="distance closure")


# =============================================================================
# MONOCHROME VISUAL PRIMITIVES — intentionally compatible with JP classroom style.
# =============================================================================
def city_icon(label: str, variant: int = 0) -> VGroup:
    """Simple monochrome skyline. `variant` prevents the two cities looking identical."""
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
    """Directional car with asymmetric nose so direction is visible without color."""
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


def road_model(*, y: float = -0.20, left: float = -5.60, right: float = 5.60, cars: bool = True):
    """Build a road and return (group, x_from_km, car_pair)."""
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
        [left + 0.12, y, 0],
        [right - 0.12, y, 0],
        dash_length=0.26,
        dashed_ratio=0.52,
        color=MID_GRAY,
        stroke_width=2.0,
    )
    top = Line([left, y + 0.47, 0], [right, y + 0.47, 0], color=BLACK_LINE, stroke_width=1.4)
    bottom = Line([left, y - 0.47, 0], [right, y - 0.47, 0], color=BLACK_LINE, stroke_width=1.4)

    city_a = city_icon("CITY A", 0).scale(0.78).move_to([left, y + 1.52, 0])
    city_b = city_icon("CITY B", 1).scale(0.78).move_to([right, y + 1.52, 0])
    zero = MathTex(r"0\ \mathrm{km}", font_size=25, color=BLACK_TEXT).move_to([left, y - 1.05, 0])
    twoforty = MathTex(r"240\ \mathrm{km}", font_size=25, color=BLACK_TEXT).move_to([right, y - 1.05, 0])
    plus_arrow = Arrow([2.65, y - 1.36, 0], [4.25, y - 1.36, 0], buff=0, color=BLACK_LINE, stroke_width=3.0)
    plus_x = MathTex(r"+x", font_size=29, color=BLACK_TEXT).next_to(plus_arrow, RIGHT, buff=0.10)

    def x_from_km(km: float) -> float:
        return left + (right - left) * (km / CITY_DISTANCE_KM)

    group = VGroup(road, center, top, bottom, city_a, city_b, zero, twoforty, plus_arrow, plus_x)
    pair = None
    if cars:
        car_a = classroom_car("A", +1, 0, 0.54).move_to([x_from_km(35), y + 0.26, 0])
        car_b = classroom_car("B", -1, 1, 0.54).move_to([x_from_km(205), y - 0.26, 0])
        group.add(car_a, car_b)
        pair = (car_a, car_b)
    return group, x_from_km, pair


# =============================================================================
# MAIN LESSON
# =============================================================================
class Physics9CityCarsJPStyleV4(JPMathClassroomScene):
    """City-car meeting problem rebuilt with the consolidated JP classroom architecture."""

    def validate_lesson_data(self) -> None:
        validate_city_car_data()

    def construct(self) -> None:
        self.opening()
        self.scene_01_physical_model()
        self.scene_02_sign_convention()
        self.scene_03_position_equations()
        self.scene_04_solve_meeting()
        self.scene_05_live_meeting()
        self.scene_06_position_graph()
        self.scene_07_velocity_graph()
        self.scene_08_checks()
        self.scene_09_method_map()
        self.standard_closing(
            "Direction → sign → equation → meeting → graph. Keep this order."
        )

    # ------------------------------------------------------------------
    # 00 — OPENING
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9 / ONE-DIMENSIONAL MOTION",
            "CITY-TO-CITY MOTION",
            "Two cars approach each other on one straight road.",
            "Read the physical direction first; let the equations describe the same story.",
        )

    # ------------------------------------------------------------------
    # 01 — PHYSICAL MODEL
    # ------------------------------------------------------------------
    def scene_01_physical_model(self) -> None:
        self.set_header(
            1,
            "READ THE ROAD BEFORE THE EQUATION",
            "City A and City B are 240 km apart. The arrows show the real directions of travel.",
        )
        road, _, _ = road_model(y=-0.55)
        distance = DoubleArrow(
            [-5.55, 2.15, 0], [5.55, 2.15, 0],
            buff=0.05, color=BLACK_LINE, stroke_width=2.5,
        )
        distance_label = MathTex(r"240\ \mathrm{km}", font_size=33, color=BLACK_TEXT).next_to(distance, UP, buff=0.08)
        data = self.key_value_panel(
            "GIVEN DATA",
            [
                ("Car A", r"80\ \mathrm{km/h}\;\rightarrow"),
                ("Car B", r"40\ \mathrm{km/h}\;\leftarrow"),
                ("Question", "When and where do they meet?"),
            ],
            width=5.4,
            label_size=22,
            value_size=25,
        )
        data.scale(0.82).move_to([0, -2.92, 0])
        stage = VGroup(road, distance, distance_label, data)
        self.assert_content_safe(stage, "scene 01 physical model")

        self.play(FadeIn(road), run_time=RUN_NORMAL)
        self.play(GrowArrow(distance), FadeIn(distance_label), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(data, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 — SIGN CONVENTION
    # ------------------------------------------------------------------
    def scene_02_sign_convention(self) -> None:
        self.set_header(
            2,
            "CHOOSE +x BEFORE USING VELOCITY",
            "A direction is geometry. A velocity sign is mathematics. Choose the axis first.",
        )
        road, _, _ = road_model(y=0.35)
        road.scale(0.84).shift(UP * 0.10)

        left_card = self.formula_panel(r"v_A=+80\ \mathrm{km/h}", width=5.4, height=1.16, font_size=39)
        right_card = self.formula_panel(r"v_B=-40\ \mathrm{km/h}", width=5.4, height=1.16, font_size=39)
        cards = VGroup(left_card, right_card).arrange(RIGHT, buff=0.48).move_to([0, -2.08, 0])
        note = self.note_panel(
            "SIGN LOGIC",
            [
                "Rightward motion → positive velocity",
                "Leftward motion → negative velocity",
                "The speed magnitudes are still 80 and 40 km/h.",
            ],
            width=7.8,
            title_size=24,
            body_size=21,
        ).scale(0.84).move_to([0, -3.30, 0])
        stage = VGroup(road, cards, note)
        self.assert_content_safe(stage, "scene 02 sign convention")

        self.play(FadeIn(road), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(left_card, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right_card, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — POSITION EQUATIONS
    # ------------------------------------------------------------------
    def scene_03_position_equations(self) -> None:
        self.set_header(
            3,
            "BUILD ONE POSITION EQUATION PER CAR",
            "Use the same model for each object: current position = initial position + velocity × time.",
        )

        base = self.formula_panel(r"x(t)=x_0+vt", width=6.0, height=1.10, font_size=42)
        base.move_to([0, 1.75, 0])
        a_stack = self.equation_stack(
            [
                r"x_A(t)=x_{A0}+v_A t",
                r"x_A(t)=0+(+80)t",
                r"\boxed{x_A(t)=80t}",
            ],
            sizes=[34, 34, 39], max_width=5.8,
        )
        b_stack = self.equation_stack(
            [
                r"x_B(t)=x_{B0}+v_B t",
                r"x_B(t)=240+(-40)t",
                r"\boxed{x_B(t)=240-40t}",
            ],
            sizes=[34, 34, 39], max_width=5.8,
        )
        left_panel = self.figure_panel(
            a_stack, width=6.25, height=3.65,
            title="CAR A", caption="Starts at 0 km and moves in +x.",
        )
        right_panel = self.figure_panel(
            b_stack, width=6.25, height=3.65,
            title="CAR B", caption="Starts at 240 km and moves in −x.",
            fill_color=VERY_LIGHT_GRAY,
        )
        layout = self.split_layout(left_panel.group, right_panel.group, center_y=-0.85, max_height=4.05)
        stage = VGroup(base, layout.group)
        self.assert_content_safe(stage, "scene 03 position equations")

        self.play(FadeIn(base), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(left_panel.box), FadeIn(left_panel.title), FadeIn(left_panel.caption), run_time=RUN_NORMAL)
        self.animate_equation_stack(a_stack, pause=PAUSE_READ)
        self.play(FadeIn(right_panel.box), FadeIn(right_panel.title), FadeIn(right_panel.caption), run_time=RUN_NORMAL)
        self.animate_equation_stack(b_stack, pause=PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — SOLVE MEETING
    # ------------------------------------------------------------------
    def scene_04_solve_meeting(self) -> None:
        self.set_header(
            4,
            "MEETING MEANS SAME POSITION AT THE SAME TIME",
            "At the meeting instant there is one shared x-coordinate, so set the two position functions equal.",
        )
        equations = self.equation_stack(
            [
                r"x_A=x_B",
                r"80t=240-40t",
                r"120t=240",
                r"\boxed{t=2\ \mathrm{h}}",
                r"x=80(2)=\boxed{160\ \mathrm{km}}",
            ],
            sizes=[39, 39, 39, 45, 42],
            buff=0.28,
            max_width=6.8,
        )
        equations.move_to([-3.60, -0.50, 0])
        logic = self.note_panel(
            "WHY THESE STEPS WORK",
            [
                "1. Equal positions define the meeting.",
                "2. Substitute the two x(t) equations.",
                "3. Combine the velocity terms.",
                "4. Solve for time.",
                "5. Substitute time back to find position.",
            ],
            width=6.15,
            title_size=25,
            body_size=22,
        ).move_to([3.78, -0.50, 0])
        stage = VGroup(equations, logic)
        self.assert_content_safe(stage, "scene 04 solve meeting")

        self.play(FadeIn(logic), run_time=RUN_NORMAL)
        self.animate_equation_stack(equations, pause=PAUSE_EXPLAIN)
        self.focus_on(equations[-2:], width=6.3, pause=PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — LIVE MOTION
    # ------------------------------------------------------------------
    def scene_05_live_meeting(self) -> None:
        self.set_header(
            5,
            "WATCH BOTH POSITIONS EVOLVE",
            "The road model and the equations must tell the same story at every instant.",
        )
        road, x_from_km, pair = road_model(y=0.50, cars=False)
        t = ValueTracker(0.0)

        car_a = always_redraw(
            lambda: classroom_car("A", +1, 0, 0.52).move_to(
                [x_from_km(X_A0_KM + V_A_KMH * t.get_value()), 0.72, 0]
            )
        )
        car_b = always_redraw(
            lambda: classroom_car("B", -1, 1, 0.52).move_to(
                [x_from_km(X_B0_KM + V_B_KMH * t.get_value()), 0.28, 0]
            )
        )
        meet_x = x_from_km(MEETING_X_KM)
        meet_line = DashedLine([meet_x, -0.20, 0], [meet_x, 2.55, 0], color=BLACK_LINE, stroke_width=2.2)
        meet_label = MathTex(r"x=160\ \mathrm{km}", font_size=27, color=BLACK_TEXT).next_to(meet_line, UP, buff=0.08)

        info_box = RoundedRectangle(
            width=9.4, height=1.18, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=WHITE_FILL, fill_opacity=1,
        ).move_to([0, -2.52, 0])
        labels = VGroup(
            Text("t =", font_size=23, color=BLACK_TEXT, weight=BOLD),
            Text("xA =", font_size=23, color=BLACK_TEXT, weight=BOLD),
            Text("xB =", font_size=23, color=BLACK_TEXT, weight=BOLD),
            Text("gap =", font_size=23, color=BLACK_TEXT, weight=BOLD),
        )
        t_num = DecimalNumber(0.0, num_decimal_places=2, font_size=25, color=BLACK_TEXT)
        xa_num = DecimalNumber(0.0, num_decimal_places=1, font_size=25, color=BLACK_TEXT)
        xb_num = DecimalNumber(240.0, num_decimal_places=1, font_size=25, color=BLACK_TEXT)
        gap_num = DecimalNumber(240.0, num_decimal_places=1, font_size=25, color=BLACK_TEXT)
        units = VGroup(
            Text("h", font_size=21, color=MID_GRAY),
            Text("km", font_size=21, color=MID_GRAY),
            Text("km", font_size=21, color=MID_GRAY),
            Text("km", font_size=21, color=MID_GRAY),
        )
        values = VGroup()
        for lab, num, unit in zip(labels, [t_num, xa_num, xb_num, gap_num], units):
            values.add(VGroup(lab, num, unit).arrange(RIGHT, buff=0.08))
        values.arrange(RIGHT, buff=0.56).move_to(info_box)

        t_num.add_updater(lambda m: m.set_value(t.get_value()))
        xa_num.add_updater(lambda m: m.set_value(X_A0_KM + V_A_KMH * t.get_value()))
        xb_num.add_updater(lambda m: m.set_value(X_B0_KM + V_B_KMH * t.get_value()))
        gap_num.add_updater(lambda m: m.set_value(max(0.0, (X_B0_KM + V_B_KMH * t.get_value()) - (X_A0_KM + V_A_KMH * t.get_value()))))

        stage = VGroup(road, meet_line, meet_label, info_box, values)
        self.assert_content_safe(stage, "scene 05 live meeting")

        self.play(FadeIn(road), FadeIn(car_a), FadeIn(car_b), run_time=RUN_NORMAL)
        self.play(Create(meet_line), FadeIn(meet_label), run_time=RUN_NORMAL)
        self.play(FadeIn(info_box), FadeIn(values), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(t.animate.set_value(MEETING_TIME_H), run_time=6.2, rate_func=linear)
        self.wait(PAUSE_WORK)
        self.play(Circumscribe(VGroup(car_a, car_b), color=BLACK_LINE, buff=0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        for num in (t_num, xa_num, xb_num, gap_num):
            num.clear_updaters()
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — POSITION GRAPH
    # ------------------------------------------------------------------
    def scene_06_position_graph(self) -> None:
        self.set_header(
            6,
            "POSITION–TIME GRAPH: TWO STORIES ON ONE SET OF AXES",
            "The intersection represents the same position at the same time; each line's slope is its velocity.",
        )
        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[0, 260, 40],
            x_length=8.1,
            y_length=5.0,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            tips=True,
        )
        axes.move_to([-2.65, -0.55, 0])
        x_label = MathTex(r"t\ (\mathrm{h})", font_size=28, color=BLACK_TEXT).next_to(axes.x_axis.get_end(), DOWN, buff=0.12)
        y_label = MathTex(r"x\ (\mathrm{km})", font_size=28, color=BLACK_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.10)

        graph_a = axes.plot(lambda q: 80 * q, x_range=[0, 3.0], color=BLACK_LINE, stroke_width=3.0)
        graph_b = DashedVMobject(axes.plot(lambda q: 240 - 40 * q, x_range=[0, 3.0], color=BLACK_LINE, stroke_width=2.8), num_dashes=28)
        meet_dot = Dot(axes.c2p(MEETING_TIME_H, MEETING_X_KM), radius=0.08, color=BLACK_LINE)
        guide_x = DashedLine(axes.c2p(2, 0), axes.c2p(2, 160), color=MID_GRAY, stroke_width=1.6)
        guide_y = DashedLine(axes.c2p(0, 160), axes.c2p(2, 160), color=MID_GRAY, stroke_width=1.6)
        meet_text = MathTex(r"(2\ \mathrm{h},\ 160\ \mathrm{km})", font_size=27, color=BLACK_TEXT).next_to(meet_dot, UR, buff=0.14)
        labels = VGroup(
            Text("A: solid, slope +80", font_size=22, color=BLACK_TEXT, weight=BOLD),
            Text("B: dashed, slope −40", font_size=22, color=BLACK_TEXT, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend_box = RoundedRectangle(
            width=4.7, height=1.35, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE_FILL, fill_opacity=1,
        )
        legend = VGroup(legend_box, labels)
        labels.move_to(legend_box).align_to(legend_box, LEFT).shift(RIGHT * 0.24)
        legend.move_to([4.65, 1.75, 0])
        note = self.note_panel(
            "GRAPH READING",
            [
                "Positive slope → motion to the right",
                "Negative slope → motion to the left",
                "Intersection → same x at the same t",
            ],
            width=4.8, title_size=24, body_size=21,
        ).move_to([4.65, -1.20, 0])

        stage = VGroup(axes, x_label, y_label, graph_a, graph_b, meet_dot, guide_x, guide_y, meet_text, legend, note)
        self.assert_content_safe(stage, "scene 06 position graph")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=RUN_NORMAL)
        self.play(Create(graph_a), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(Create(graph_b), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(legend), run_time=RUN_NORMAL)
        self.play(Create(guide_x), Create(guide_y), FadeIn(meet_dot), FadeIn(meet_text), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — VELOCITY GRAPH
    # ------------------------------------------------------------------
    def scene_07_velocity_graph(self) -> None:
        self.set_header(
            7,
            "VELOCITY–TIME GRAPH: DIRECTION BECOMES HEIGHT",
            "Constant velocity appears as a horizontal line; the sign tells which side of the chosen axis the motion follows.",
        )
        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[-60, 100, 20],
            x_length=8.1,
            y_length=5.0,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            tips=True,
        ).move_to([-2.65, -0.55, 0])
        x_label = MathTex(r"t\ (\mathrm{h})", font_size=28, color=BLACK_TEXT).next_to(axes.x_axis.get_end(), DOWN, buff=0.12)
        y_label = MathTex(r"v\ (\mathrm{km/h})", font_size=27, color=BLACK_TEXT).next_to(axes.y_axis.get_end(), UP, buff=0.10)

        va_line = Line(axes.c2p(0, 80), axes.c2p(3, 80), color=BLACK_LINE, stroke_width=3.0)
        vb_base = Line(axes.c2p(0, -40), axes.c2p(3, -40), color=BLACK_LINE, stroke_width=2.8)
        vb_line = DashedVMobject(vb_base, num_dashes=28)
        va_lab = MathTex(r"v_A=+80\ \mathrm{km/h}", font_size=28, color=BLACK_TEXT).next_to(va_line, UP, buff=0.14)
        vb_lab = MathTex(r"v_B=-40\ \mathrm{km/h}", font_size=28, color=BLACK_TEXT).next_to(vb_base, DOWN, buff=0.14)

        meaning = self.note_panel(
            "READ THE SIGN",
            [
                "Above 0 → rightward motion",
                "Below 0 → leftward motion",
                "Horizontal line → constant velocity",
                "Magnitude = vertical distance from 0",
            ],
            width=4.95, title_size=24, body_size=21,
        ).move_to([4.70, -0.15, 0])
        stage = VGroup(axes, x_label, y_label, va_line, vb_line, va_lab, vb_lab, meaning)
        self.assert_content_safe(stage, "scene 07 velocity graph")

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=RUN_NORMAL)
        self.play(Create(va_line), FadeIn(va_lab), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Create(vb_line), FadeIn(vb_lab), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — CHECKS
    # ------------------------------------------------------------------
    def scene_08_checks(self) -> None:
        self.set_header(
            8,
            "VERIFY THE RESULT — DO NOT TRUST ONE METHOD ALONE",
            "A correct solution survives independent checks using distance, relative speed, and graph interpretation.",
        )
        rows = [
            ["Car A distance", r"80(2)", r"160\ \mathrm{km}"],
            ["Car B distance", r"40(2)", r"80\ \mathrm{km}"],
            ["Distance closure", r"160+80", r"240\ \mathrm{km}"],
            ["Relative speed", r"80+40", r"120\ \mathrm{km/h}"],
            ["Meeting time", r"240/120", r"2\ \mathrm{h}"],
        ]
        table = self.build_table(
            headers=("CHECK", "CALCULATION", "RESULT"),
            body_rows=rows,
            column_widths=(4.3, 3.7, 3.6),
            math_columns=(1, 2),
            row_height=0.64,
            header_height=0.72,
            body_font_size=26,
            header_font_size=23,
        )
        table.group.move_to([0, -0.30, 0])
        conclusion = self.formula_panel(
            r"\boxed{t=2\ \mathrm{h}},\qquad \boxed{x=160\ \mathrm{km\ from\ City\ A}}",
            width=10.8, height=1.06, font_size=38,
        ).move_to([0, -3.36, 0])
        stage = VGroup(table.group, conclusion)
        self.assert_content_safe(stage, "scene 08 independent checks")

        self.animate_table_rows(table, include_header=True, pause=PAUSE_SHORT)
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — METHOD MAP
    # ------------------------------------------------------------------
    def scene_09_method_map(self) -> None:
        self.set_header(
            9,
            "REUSABLE METHOD FOR EVERY TWO-OBJECT MEETING PROBLEM",
            "The numbers can change. The logic does not: define direction, model each position, solve one shared event, then verify.",
        )
        route = self.process_map(
            [
                ("1", "CHOOSE +x"),
                ("2", "ASSIGN SIGNS"),
                ("3", "WRITE x(t)"),
                ("4", "SET POSITIONS EQUAL"),
                ("5", "SOLVE t AND x"),
                ("6", "CHECK WITH GRAPHS"),
            ],
            card_width=4.35,
            card_height=1.16,
            columns=3,
        )
        route.move_to([0, -0.65, 0])
        takeaway = self.note_panel(
            "FINAL TAKEAWAY",
            ["Direction → sign → equation → meeting → graph."],
            width=8.2,
            title_size=25,
            body_size=24,
        ).move_to([0, -3.18, 0])
        stage = VGroup(route, takeaway)
        self.assert_content_safe(stage, "scene 09 method map")

        for card in route:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()


if __name__ == "__main__":
    validate_city_car_data()
