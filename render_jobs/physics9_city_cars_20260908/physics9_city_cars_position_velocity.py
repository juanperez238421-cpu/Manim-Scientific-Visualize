#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Classic City-to-City Car Motion Problem.

Full step-by-step ManimCE lesson:
- Two cars leave opposite cities at the same time.
- Establish the coordinate system and signed velocities.
- Build the two position equations.
- Solve the meeting time and meeting position algebraically.
- Animate the physical motion on the road.
- Construct and interpret the position-vs-time graph for both cars.
- Construct and interpret the velocity-vs-time graph for both cars.
- Verify the result using relative speed and traveled distances.

Target: Manim Community Edition 0.20.1
Render: 1920x1080, 30 fps, H.264 MP4.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE


# =============================================================================
# LESSON DATA — CLASSIC TWO-CITY MEETING PROBLEM
# =============================================================================
CITY_DISTANCE_KM = 240.0
V_A_KMH = 80.0
V_B_KMH = -40.0   # negative because Car B moves toward -x
MEETING_TIME_H = 2.0
MEETING_POSITION_KM = 160.0
DIST_A_KM = 160.0
DIST_B_KM = 80.0

assert abs(V_A_KMH * MEETING_TIME_H - MEETING_POSITION_KM) < 1e-9
assert abs(CITY_DISTANCE_KM + V_B_KMH * MEETING_TIME_H - MEETING_POSITION_KM) < 1e-9
assert abs(DIST_A_KM + DIST_B_KM - CITY_DISTANCE_KM) < 1e-9
assert abs(CITY_DISTANCE_KM / (V_A_KMH + abs(V_B_KMH)) - MEETING_TIME_H) < 1e-9


# =============================================================================
# VISUAL SYSTEM
# =============================================================================
INK = "#111111"
DARK = "#2C2C2C"
MID = "#6E6E6E"
LIGHT = "#D7D7D7"
PALE = "#F5F5F5"
PAPER = "#FBFBFB"
CAR_A = "#1E5AA8"
CAR_B = "#B33A3A"
GOOD = "#2F7D32"
GOLD = "#B27A00"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))


@dataclass
class RoadDiagram:
    group: VGroup
    car_a: VGroup
    car_b: VGroup
    x_to_scene: callable


class Physics9CityCars(MovingCameraScene):
    """Complete senior classroom animation for the classic two-city car problem."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography / generic helpers
    # ------------------------------------------------------------------
    def txt(self, content: str, size: int = 30, weight=NORMAL, color=INK, **kwargs):
        return Text(content, font_size=size, weight=weight, color=color, **kwargs)

    def mth(self, content: str, size: int = 38, color=INK, **kwargs):
        return MathTex(content, font_size=size, color=color, **kwargs)

    def fit(self, mob: Mobject, width=14.6, height=7.3):
        if mob.width > width:
            mob.scale_to_fit_width(width)
        if mob.height > height:
            mob.scale_to_fit_height(height)
        return mob

    def stage_title(self, number: str, title: str, subtitle: str | None = None):
        badge = Circle(radius=0.32, stroke_color=INK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1)
        badge_num = self.txt(number, 24, BOLD).move_to(badge)
        main = self.txt(title, 34, BOLD)
        top = VGroup(VGroup(badge, badge_num), main).arrange(RIGHT, buff=0.26)
        top.to_edge(UP, buff=0.26).to_edge(LEFT, buff=0.42)
        line = Line(LEFT * 7.55, RIGHT * 7.55, color=LIGHT, stroke_width=1.4).next_to(top, DOWN, buff=0.16)
        group = VGroup(top, line)
        if subtitle:
            sub = self.txt(subtitle, 22, color=DARK)
            sub.next_to(line, DOWN, buff=0.10).align_to(top, LEFT)
            group.add(sub)
        return group

    def formula_panel(self, expression: str, width=7.0, height=1.10, size=42, stroke=INK):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                               stroke_color=stroke, stroke_width=2,
                               fill_color=PAPER, fill_opacity=1)
        eq = self.mth(expression, size)
        if eq.width > width - 0.5:
            eq.scale_to_fit_width(width - 0.5)
        if eq.height > height - 0.2:
            eq.scale_to_fit_height(height - 0.2)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(self, title: str, lines: list[str], width=6.2, title_size=25, body_size=23):
        t = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        content = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if content.width > width - 0.58:
            content.scale_to_fit_width(width - 0.58)
        h = max(1.15, content.height + 0.64)
        box = RoundedRectangle(width=width, height=h, corner_radius=0.12,
                               stroke_color=INK, stroke_width=1.7,
                               fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.29)
        return VGroup(box, content)

    def clear_stage(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.55)

    # ------------------------------------------------------------------
    # Vector drawings
    # ------------------------------------------------------------------
    def city_icon(self, label: str, color=DARK):
        base = VGroup(
            Rectangle(width=0.72, height=0.92, stroke_color=color, stroke_width=2,
                      fill_color=PALE, fill_opacity=1),
            Rectangle(width=0.48, height=1.22, stroke_color=color, stroke_width=2,
                      fill_color=WHITE, fill_opacity=1).shift(RIGHT * 0.72),
            Rectangle(width=0.66, height=0.75, stroke_color=color, stroke_width=2,
                      fill_color=PALE, fill_opacity=1).shift(RIGHT * 1.32),
        )
        windows = VGroup()
        for building in base:
            for yy in (-0.20, 0.18):
                windows.add(Square(side_length=0.10, stroke_color=color, stroke_width=1).move_to(building.get_center() + UP * yy))
        body = VGroup(base, windows)
        text = self.txt(label, 23, BOLD, color=color).next_to(body, DOWN, buff=0.12)
        return VGroup(body, text)

    def car_icon(self, label: str, color: str):
        body = RoundedRectangle(width=1.02, height=0.34, corner_radius=0.10,
                                stroke_color=color, stroke_width=2.2,
                                fill_color=WHITE, fill_opacity=1)
        roof = Polygon([-0.28, 0.17, 0], [-0.08, 0.43, 0], [0.28, 0.43, 0], [0.44, 0.17, 0],
                       stroke_color=color, stroke_width=2.2, fill_color=WHITE, fill_opacity=1)
        wheel1 = Circle(radius=0.10, stroke_color=color, stroke_width=2, fill_color=WHITE, fill_opacity=1).shift(LEFT * 0.30 + DOWN * 0.18)
        wheel2 = Circle(radius=0.10, stroke_color=color, stroke_width=2, fill_color=WHITE, fill_opacity=1).shift(RIGHT * 0.30 + DOWN * 0.18)
        car = VGroup(body, roof, wheel1, wheel2)
        tag = self.txt(label, 19, BOLD, color=color).next_to(car, UP, buff=0.08)
        return VGroup(car, tag)

    def road_diagram(self, show_velocity_labels=True, show_coordinate=True):
        x_left, x_right = -6.0, 6.0
        y_road = -0.35
        road = Line([x_left, y_road, 0], [x_right, y_road, 0], color=INK, stroke_width=4)
        center_dash = DashedLine([x_left, y_road - 0.24, 0], [x_right, y_road - 0.24, 0],
                                 dash_length=0.25, color=LIGHT, stroke_width=2)
        city_a = self.city_icon("CITY A   x = 0 km").scale(0.86).move_to([x_left + 0.35, 0.75, 0])
        city_b = self.city_icon("CITY B   x = 240 km").scale(0.86).move_to([x_right - 0.95, 0.75, 0])
        car_a = self.car_icon("CAR A", CAR_A).scale(0.88).move_to([x_left + 0.55, y_road + 0.48, 0])
        car_b = self.car_icon("CAR B", CAR_B).scale(0.88).move_to([x_right - 0.55, y_road + 0.48, 0])

        pieces = VGroup(road, center_dash, city_a, city_b, car_a, car_b)

        if show_velocity_labels:
            a_arrow = Arrow([x_left + 0.55, y_road + 1.00, 0], [x_left + 2.05, y_road + 1.00, 0],
                            buff=0, color=CAR_A, stroke_width=5, max_tip_length_to_length_ratio=0.15)
            a_lab = self.txt("80 km/h", 24, BOLD, CAR_A).next_to(a_arrow, UP, buff=0.08)
            b_arrow = Arrow([x_right - 0.55, y_road + 1.00, 0], [x_right - 2.05, y_road + 1.00, 0],
                            buff=0, color=CAR_B, stroke_width=5, max_tip_length_to_length_ratio=0.15)
            b_lab = self.txt("40 km/h", 24, BOLD, CAR_B).next_to(b_arrow, UP, buff=0.08)
            pieces.add(a_arrow, a_lab, b_arrow, b_lab)

        if show_coordinate:
            axis = Arrow([x_left, y_road - 0.72, 0], [x_right + 0.3, y_road - 0.72, 0],
                         buff=0, color=INK, stroke_width=2.4, max_tip_length_to_length_ratio=0.025)
            plus = self.mth(r"+x", 30).next_to(axis.get_end(), UP, buff=0.05)
            pieces.add(axis, plus)

        def x_to_scene(x_km: float):
            return x_left + (x_km / CITY_DISTANCE_KM) * (x_right - x_left)

        return RoadDiagram(pieces, car_a, car_b, x_to_scene)

    # ------------------------------------------------------------------
    # Main narrative
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.problem_statement()
        self.coordinate_system()
        self.position_equations()
        self.solve_meeting()
        self.animate_physical_meeting()
        self.position_time_graph()
        self.velocity_time_graph()
        self.cross_check()
        self.final_method_map()

    def opening(self):
        title = self.txt("PHYSICS 9", 42, BOLD)
        subtitle = self.txt("CLASSIC CITY-TO-CITY CAR MOTION", 48, BOLD)
        objective = self.txt("From physical motion  →  equations  →  x–t graph  →  v–t graph", 28, color=DARK)
        key = self.formula_panel(r"x=x_i+vt", width=5.2, height=1.15, size=48, stroke=CAR_A)
        group = VGroup(title, subtitle, objective, key).arrange(DOWN, buff=0.32)
        group.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.8)
        self.play(Write(subtitle), run_time=1.2)
        self.play(FadeIn(objective), run_time=0.8)
        self.play(FadeIn(key), run_time=0.8)
        self.wait(2.8)
        self.clear_stage()

    def problem_statement(self):
        header = self.stage_title("1", "THE CLASSIC TWO-CITY PROBLEM",
                                  "Two cars start at the same time and move toward each other with constant velocities.")
        self.play(FadeIn(header), run_time=0.7)

        road = self.road_diagram()
        road.group.scale(0.90).move_to(DOWN * 0.30)
        self.play(Create(road.group[0]), FadeIn(road.group[1]), run_time=1.0)
        self.play(FadeIn(VGroup(*road.group[2:])), run_time=1.0)

        problem = self.note_panel(
            "PROBLEM",
            [
                "City A and City B are 240 km apart.",
                "Car A leaves City A at 80 km/h toward City B.",
                "Car B leaves City B at 40 km/h toward City A.",
                "Find when and where the cars meet.",
                "Then construct x–t and v–t graphs for BOTH cars.",
            ],
            width=7.2,
            title_size=26,
            body_size=22,
        )
        problem.scale(0.86).to_corner(DR, buff=0.34)
        self.play(FadeIn(problem, shift=UP * 0.12), run_time=0.8)
        self.wait(4.2)
        self.clear_stage()

    def coordinate_system(self):
        header = self.stage_title("2", "STEP 1 — CHOOSE ONE COORDINATE SYSTEM",
                                  "The sign of velocity comes from the chosen +x direction, not from the car itself.")
        self.play(FadeIn(header), run_time=0.7)

        road = self.road_diagram(show_velocity_labels=False, show_coordinate=True)
        road.group.scale(0.82).shift(UP * 0.65)
        self.play(FadeIn(road.group), run_time=1.0)

        a_data = self.note_panel("CAR A", ["Initial position:  x_A(0) = 0 km", "Velocity:  v_A = +80 km/h"], width=5.7, body_size=24)
        b_data = self.note_panel("CAR B", ["Initial position:  x_B(0) = 240 km", "Velocity:  v_B = −40 km/h"], width=5.7, body_size=24)
        a_data[0].set_stroke(CAR_A, width=2.2)
        b_data[0].set_stroke(CAR_B, width=2.2)
        cards = VGroup(a_data, b_data).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.20)
        self.play(FadeIn(a_data, shift=RIGHT * 0.15), run_time=0.8)
        self.wait(1.6)
        self.play(FadeIn(b_data, shift=LEFT * 0.15), run_time=0.8)
        self.wait(2.2)

        sign_note = self.txt("Car B has a negative velocity because it moves opposite to +x.", 25, BOLD, color=CAR_B)
        sign_note.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(sign_note), run_time=0.7)
        self.wait(2.6)
        self.clear_stage()

    def position_equations(self):
        header = self.stage_title("3", "STEP 2 — WRITE ONE POSITION EQUATION FOR EACH CAR",
                                  "Use the same equation x = x_i + vt for both objects.")
        self.play(FadeIn(header), run_time=0.7)

        general = self.formula_panel(r"x=x_i+vt", width=5.3, height=1.10, size=48)
        general.move_to(UP * 1.85)
        self.play(FadeIn(general), run_time=0.8)
        self.wait(1.6)

        a_stack = VGroup(
            self.txt("CAR A", 28, BOLD, CAR_A),
            self.mth(r"x_A=x_{i,A}+v_A t", 36, CAR_A),
            self.mth(r"x_A=0+(80)t", 36, CAR_A),
            self.mth(r"\boxed{x_A=80t}", 42, CAR_A),
        ).arrange(DOWN, buff=0.28)
        b_stack = VGroup(
            self.txt("CAR B", 28, BOLD, CAR_B),
            self.mth(r"x_B=x_{i,B}+v_B t", 36, CAR_B),
            self.mth(r"x_B=240+(-40)t", 36, CAR_B),
            self.mth(r"\boxed{x_B=240-40t}", 42, CAR_B),
        ).arrange(DOWN, buff=0.28)
        a_stack.move_to(LEFT * 3.75 + DOWN * 0.85)
        b_stack.move_to(RIGHT * 3.75 + DOWN * 0.85)

        for mob in a_stack:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.55)
            self.wait(0.75)
        for mob in b_stack:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.55)
            self.wait(0.75)

        self.wait(2.4)
        self.clear_stage()

    def solve_meeting(self):
        header = self.stage_title("4", "STEP 3 — AT THE MEETING, THE POSITIONS ARE EQUAL",
                                  "Meeting means same place at the same instant:  x_A = x_B.")
        self.play(FadeIn(header), run_time=0.7)

        equality = self.formula_panel(r"x_A=x_B", width=4.7, height=1.0, size=46, stroke=GOOD).move_to(UP * 1.95)
        self.play(FadeIn(equality), run_time=0.7)
        self.wait(1.4)

        steps = VGroup(
            self.mth(r"80t=240-40t", 40),
            self.mth(r"80t+40t=240", 40),
            self.mth(r"120t=240", 40),
            self.mth(r"\boxed{t=2\ \text{h}}", 46, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(LEFT * 2.9 + DOWN * 0.45)

        for i, line in enumerate(steps):
            self.play(FadeIn(line, shift=RIGHT * 0.10), run_time=0.65)
            self.wait(1.15 if i < 3 else 1.8)

        pos_steps = VGroup(
            self.txt("MEETING POSITION", 27, BOLD),
            self.mth(r"x_A=80t", 36, CAR_A),
            self.mth(r"x_A=80(2)", 36, CAR_A),
            self.mth(r"\boxed{x=160\ \text{km}}", 44, GOOD),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.55 + DOWN * 0.45)
        for mob in pos_steps:
            self.play(FadeIn(mob, shift=LEFT * 0.08), run_time=0.60)
            self.wait(0.9)

        final = self.txt("Answer: the cars meet after 2 h, 160 km from City A.", 28, BOLD, GOOD).to_edge(DOWN, buff=0.32)
        self.play(FadeIn(final), run_time=0.7)
        self.wait(3.4)
        self.clear_stage()

    def animate_physical_meeting(self):
        header = self.stage_title("5", "STEP 4 — WATCH THE PHYSICS MATCH THE ALGEBRA",
                                  "Car A travels 160 km while Car B travels 80 km during the same 2 h.")
        self.play(FadeIn(header), run_time=0.7)

        road = self.road_diagram(show_velocity_labels=True, show_coordinate=True)
        road.group.scale(0.93).move_to(DOWN * 0.20)
        self.play(FadeIn(road.group), run_time=1.0)
        self.wait(1.6)

        # Find the scaled scene location of x = 160 km by interpolating between road endpoints.
        road_line = road.group[0]
        start = road_line.get_start()
        end = road_line.get_end()
        meet_point = start + (MEETING_POSITION_KM / CITY_DISTANCE_KM) * (end - start)
        target = meet_point + UP * 0.48

        time_label = self.mth(r"t=0\ \text{h}", 34).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(time_label), run_time=0.5)

        new_time = self.mth(r"t=2\ \text{h}", 34, GOOD).move_to(time_label)
        self.play(
            road.car_a.animate.move_to(target + LEFT * 0.36),
            road.car_b.animate.move_to(target + RIGHT * 0.36),
            Transform(time_label, new_time),
            run_time=4.0,
            rate_func=linear,
        )
        marker = DashedLine(meet_point + DOWN * 0.45, meet_point + UP * 1.95,
                            color=GOOD, dash_length=0.14, stroke_width=2.4)
        label = self.txt("MEETING  x = 160 km", 25, BOLD, GOOD).next_to(marker, UP, buff=0.10)
        self.play(Create(marker), FadeIn(label), run_time=0.8)
        self.wait(3.0)
        self.clear_stage()

    def position_time_graph(self):
        header = self.stage_title("6", "STEP 5 — CONSTRUCT THE POSITION–TIME GRAPH",
                                  "The two lines intersect exactly where x_A = x_B:  (2 h, 160 km).")
        self.play(FadeIn(header), run_time=0.7)

        axes = Axes(
            x_range=[0, 3.1, 0.5],
            y_range=[0, 280, 40],
            x_length=7.0,
            y_length=5.4,
            tips=False,
            axis_config={"color": INK, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3], "font_size": 23},
            y_axis_config={"numbers_to_include": [0, 80, 160, 240], "font_size": 23},
        ).move_to(LEFT * 2.9 + DOWN * 0.30)
        xlab = self.txt("Time t (h)", 23, BOLD).next_to(axes.x_axis, DOWN, buff=0.20)
        ylab = self.txt("Position x (km)", 23, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.20)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=1.0)

        graph_a = axes.plot(lambda t: 80 * t, x_range=[0, 3], color=CAR_A, stroke_width=4)
        graph_b = axes.plot(lambda t: 240 - 40 * t, x_range=[0, 3], color=CAR_B, stroke_width=4)
        lab_a = self.mth(r"x_A=80t", 30, CAR_A).move_to(axes.c2p(2.65, 225) + UP * 0.34)
        lab_b = self.mth(r"x_B=240-40t", 30, CAR_B).move_to(axes.c2p(1.45, 205) + UP * 0.34)

        self.play(Create(graph_a), FadeIn(lab_a), run_time=1.4)
        self.wait(1.3)
        self.play(Create(graph_b), FadeIn(lab_b), run_time=1.4)
        self.wait(1.8)

        tracker = ValueTracker(0)
        dot_a = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 80 * tracker.get_value()), radius=0.075, color=CAR_A))
        dot_b = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 240 - 40 * tracker.get_value()), radius=0.075, color=CAR_B))
        self.add(dot_a, dot_b)
        self.play(tracker.animate.set_value(2), run_time=4.0, rate_func=linear)

        meet = axes.c2p(2, 160)
        meet_dot = Dot(meet, radius=0.10, color=GOOD)
        vdash = DashedLine(axes.c2p(2, 0), meet, color=GOOD, dash_length=0.12, stroke_width=2)
        hdash = DashedLine(axes.c2p(0, 160), meet, color=GOOD, dash_length=0.12, stroke_width=2)
        meet_label = self.mth(r"(2\ \text{h},\ 160\ \text{km})", 31, GOOD).next_to(meet_dot, RIGHT, buff=0.18)
        self.play(FadeIn(meet_dot), Create(vdash), Create(hdash), FadeIn(meet_label), run_time=0.9)

        interpretation = self.note_panel(
            "HOW TO READ THIS GRAPH",
            [
                "Car A starts at x = 0 km and its line rises.",
                "Car B starts at x = 240 km and its line falls.",
                "Slope of each x–t line = that car's velocity.",
                "Intersection = same position at the same time.",
            ],
            width=5.3,
            body_size=22,
        ).move_to(RIGHT * 4.45 + DOWN * 0.45)
        interpretation[0].set_stroke(GOOD, width=1.8)
        self.play(FadeIn(interpretation), run_time=0.8)
        self.wait(4.0)
        dot_a.clear_updaters(); dot_b.clear_updaters()
        self.clear_stage()

    def velocity_time_graph(self):
        header = self.stage_title("7", "STEP 6 — CONSTRUCT THE VELOCITY–TIME GRAPH",
                                  "Constant velocity appears as a horizontal line; the sign tells the direction.")
        self.play(FadeIn(header), run_time=0.7)

        axes = Axes(
            x_range=[0, 3.1, 0.5],
            y_range=[-60, 100, 20],
            x_length=7.1,
            y_length=5.3,
            tips=False,
            axis_config={"color": INK, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3], "font_size": 23},
            y_axis_config={"numbers_to_include": [-40, 0, 40, 80], "font_size": 23},
        ).move_to(LEFT * 2.85 + DOWN * 0.28)
        xlab = self.txt("Time t (h)", 23, BOLD).next_to(axes.x_axis, DOWN, buff=0.20)
        ylab = self.txt("Velocity v (km/h)", 23, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=1.0)

        va = Line(axes.c2p(0, 80), axes.c2p(3, 80), color=CAR_A, stroke_width=4)
        vb = Line(axes.c2p(0, -40), axes.c2p(3, -40), color=CAR_B, stroke_width=4)
        la = self.mth(r"v_A=+80\ \text{km/h}", 31, CAR_A).next_to(va, UP, buff=0.12).shift(RIGHT * 1.1)
        lb = self.mth(r"v_B=-40\ \text{km/h}", 31, CAR_B).next_to(vb, DOWN, buff=0.12).shift(RIGHT * 1.1)
        self.play(Create(va), FadeIn(la), run_time=1.2)
        self.wait(1.2)
        self.play(Create(vb), FadeIn(lb), run_time=1.2)

        meet_line = DashedLine(axes.c2p(2, -60), axes.c2p(2, 100), color=GOOD, dash_length=0.12, stroke_width=2)
        meet_tag = self.txt("meeting time  t = 2 h", 23, BOLD, GOOD).next_to(meet_line, UP, buff=0.08)
        self.play(Create(meet_line), FadeIn(meet_tag), run_time=0.8)

        panel = self.note_panel(
            "IMPORTANT",
            [
                "The cars meet at t = 2 h, but their velocities are NOT equal.",
                "Meeting is an equality of position:  x_A = x_B.",
                "Car A remains at +80 km/h; Car B remains at −40 km/h.",
                "Horizontal v–t lines confirm uniform motion.",
            ],
            width=5.45,
            body_size=21,
        ).move_to(RIGHT * 4.45 + DOWN * 0.35)
        panel[0].set_stroke(GOLD, width=2.0)
        self.play(FadeIn(panel), run_time=0.8)
        self.wait(4.4)
        self.clear_stage()

    def cross_check(self):
        header = self.stage_title("8", "STEP 7 — VERIFY THE ANSWER TWO DIFFERENT WAYS",
                                  "A correct physics solution should survive an independent check.")
        self.play(FadeIn(header), run_time=0.7)

        left = self.note_panel(
            "CHECK A — RELATIVE SPEED",
            [
                "Cars approach each other at:",
                "80 + 40 = 120 km/h",
                "time = distance / closing speed",
                "t = 240 / 120 = 2 h",
            ],
            width=6.1,
            body_size=23,
        )
        right = self.note_panel(
            "CHECK B — DISTANCES TRAVELED",
            [
                "Car A:  d_A = 80(2) = 160 km",
                "Car B:  d_B = 40(2) = 80 km",
                "160 + 80 = 240 km",
                "The full city separation is recovered.",
            ],
            width=6.1,
            body_size=23,
        )
        left[0].set_stroke(CAR_A, width=2.0)
        right[0].set_stroke(CAR_B, width=2.0)
        cards = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.20)
        self.play(FadeIn(left, shift=RIGHT * 0.12), run_time=0.9)
        self.wait(2.4)
        self.play(FadeIn(right, shift=LEFT * 0.12), run_time=0.9)
        self.wait(3.2)

        conclusion = self.formula_panel(r"\boxed{t=2\ \text{h},\qquad x=160\ \text{km}}", width=7.2, height=1.05, size=43, stroke=GOOD)
        conclusion.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(conclusion), run_time=0.8)
        self.wait(3.2)
        self.clear_stage()

    def final_method_map(self):
        header = self.stage_title("9", "METHOD YOU CAN REUSE FOR ANY TWO-CAR MEETING PROBLEM",
                                  "The graph and the algebra are two representations of the same motion.")
        self.play(FadeIn(header), run_time=0.7)

        items = [
            ("1", "CHOOSE +x"),
            ("2", "ASSIGN SIGNS"),
            ("3", "WRITE x(t)"),
            ("4", "SET x_A = x_B"),
            ("5", "SOLVE t"),
            ("6", "FIND x"),
            ("7", "DRAW x–t"),
            ("8", "DRAW v–t"),
            ("9", "VERIFY"),
        ]
        cards = VGroup()
        for number, label in items:
            box = RoundedRectangle(width=3.75, height=1.02, corner_radius=0.12,
                                   stroke_color=INK, stroke_width=1.7,
                                   fill_color=WHITE, fill_opacity=1)
            num = Circle(radius=0.22, stroke_color=INK, stroke_width=1.5, fill_color=PALE, fill_opacity=1)
            nt = self.txt(number, 18, BOLD).move_to(num)
            text = self.txt(label, 22, BOLD)
            content = VGroup(VGroup(num, nt), text).arrange(RIGHT, buff=0.18).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(rows=3, cols=3, buff=(0.30, 0.28)).move_to(DOWN * 0.25)

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.10), run_time=2.4)
        self.wait(3.6)

        final = self.txt("POSITION tells you WHERE.   VELOCITY tells you HOW FAST and IN WHICH DIRECTION.", 27, BOLD, GOOD)
        final.to_edge(DOWN, buff=0.24)
        self.play(FadeIn(final), run_time=0.8)
        self.wait(4.2)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)

        closing = VGroup(
            self.txt("PHYSICS 9", 38, BOLD),
            self.txt("Two cars. One coordinate system. One consistent story.", 34, BOLD),
            self.mth(r"x_A(2)=x_B(2)=160\ \text{km}", 43, GOOD),
        ).arrange(DOWN, buff=0.34)
        self.play(FadeIn(closing, shift=UP * 0.10), run_time=1.0)
        self.wait(4.0)


# Preview:
#   LESSON_TIME_SCALE=0.08 manim -pql physics9_city_cars_position_velocity.py Physics9CityCars --fps 15 --disable_caching
# Final:
#   LESSON_TIME_SCALE=1.0 manim -pqh physics9_city_cars_position_velocity.py Physics9CityCars --fps 30 --disable_caching
