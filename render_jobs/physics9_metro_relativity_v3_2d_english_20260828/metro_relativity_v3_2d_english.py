#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Relative motion, light, and non-absolute time.

V3 redesign: 100% 2D, 100% English, projector-safe proportions, and a
student-centered numerical exercise that uses the general position equation

    X = X0 + v t

first for ordinary Galilean relative motion and then for a light-clock thought
experiment. The final comparison shows that all inertial observers measure the
same light speed c while elapsed coordinate time depends on the frame.

Final render:
    manim -pqh metro_relativity_v3_2d_english.py Physics9MetroRelativityV3 \
        --format=mp4 --disable_caching
"""
from __future__ import annotations

import os
from math import isclose, sqrt
from manim import *

# -----------------------------------------------------------------------------
# Render contract
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#2B2B2B"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D8D8D8"
PAPER_GRAY = "#F5F5F5"
LIGHT_AMBER = "#D49A00"

RUN_QUICK = 0.55
RUN_NORMAL = 0.95
RUN_SLOW = 1.45
RUN_DEMO = 3.2
PAUSE_SHORT = 0.8
PAUSE_READ = 1.6
PAUSE_EXPLAIN = 2.4
PAUSE_WORK = 4.0
PAUSE_FINAL = 5.0


class Physics9MetroRelativityV3(MovingCameraScene):
    """2D-only classroom lesson: relative velocity -> light clock -> relativity of time."""

    TRAIN_MPS = 20.0
    WALK_REL_MPS = 2.0
    WALK_GROUND_MPS = 22.0
    ORDINARY_DT = 5.0

    C = 3.0e8
    BETA = 0.60
    CLOCK_HEIGHT = 2.4
    GAMMA = 1.25
    T_TRAIN_NS = 8.0
    T_GROUND_NS = 10.0
    GROUND_HORIZONTAL_M = 1.8
    GROUND_LIGHT_PATH_M = 3.0

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE
        self.header = None
        self.validate_lesson_data()

    def validate_lesson_data(self) -> None:
        assert isclose(self.TRAIN_MPS + self.WALK_REL_MPS, self.WALK_GROUND_MPS)
        assert isclose(self.TRAIN_MPS * 3.6, 72.0)
        assert isclose(self.WALK_REL_MPS * 3.6, 7.2)
        assert isclose(self.WALK_GROUND_MPS * 3.6, 79.2)
        assert isclose(self.WALK_REL_MPS * self.ORDINARY_DT, 10.0)
        assert isclose(self.TRAIN_MPS * self.ORDINARY_DT, 100.0)
        assert isclose(self.WALK_GROUND_MPS * self.ORDINARY_DT, 110.0)
        assert isclose(self.CLOCK_HEIGHT / self.C * 1e9, self.T_TRAIN_NS)
        assert isclose(1 / sqrt(1 - self.BETA**2), self.GAMMA)
        assert isclose(self.GAMMA * self.T_TRAIN_NS, self.T_GROUND_NS)
        assert isclose(self.BETA * self.C * self.T_GROUND_NS * 1e-9, self.GROUND_HORIZONTAL_M)
        assert isclose(self.C * self.T_GROUND_NS * 1e-9, self.GROUND_LIGHT_PATH_M)
        assert isclose(self.GROUND_HORIZONTAL_M**2 + self.CLOCK_HEIGHT**2, self.GROUND_LIGHT_PATH_M**2)

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def txt(self, content: str, size: int = 30, weight=NORMAL, color=BLACK_TEXT) -> Text:
        return Text(content, font_size=size, color=color, weight=weight)

    def eq(self, expression: str, size: int = 40, color=BLACK_TEXT) -> MathTex:
        return MathTex(expression, font_size=size, color=color)

    def fit(self, mob: Mobject, max_w: float, max_h: float) -> Mobject:
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def clear_stage(self, keep_header=True) -> None:
        keep = {self.header} if keep_header and self.header is not None else set()
        fades = [FadeOut(m) for m in list(self.mobjects) if m not in keep]
        if fades:
            self.play(*fades, run_time=RUN_QUICK)

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        if self.header is not None and self.header in self.mobjects:
            self.play(FadeOut(self.header), run_time=RUN_QUICK)
        tag_box = RoundedRectangle(width=0.68, height=0.46, corner_radius=0.08,
                                   stroke_color=BLACK_LINE, stroke_width=1.8,
                                   fill_color=WHITE, fill_opacity=1)
        tag = self.txt(f"{number:02d}", 22, BOLD).move_to(tag_box)
        title_m = self.txt(title, 31, BOLD)
        self.fit(title_m, 13.3, 0.60)
        top = VGroup(VGroup(tag_box, tag), title_m).arrange(RIGHT, buff=0.24)
        top.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.5, RIGHT * 7.5, color=LIGHT_GRAY, stroke_width=1.7)
        rule.next_to(top, DOWN, buff=0.07)
        subtitle_m = self.txt(subtitle, 19)
        self.fit(subtitle_m, 14.3, 0.48)
        subtitle_m.next_to(rule, DOWN, buff=0.08).align_to(top, LEFT)
        self.header = VGroup(top, rule, subtitle_m)
        self.add(self.header)
        self.play(FadeIn(self.header), run_time=RUN_QUICK)

    def formula_card(self, expression: str, width=5.5, height=1.05, size=38, fill=PAPER_GRAY) -> VGroup:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.11,
                               stroke_color=BLACK_LINE, stroke_width=1.9,
                               fill_color=fill, fill_opacity=1)
        formula = self.eq(expression, size)
        self.fit(formula, width - 0.40, height - 0.22)
        formula.move_to(box)
        return VGroup(box, formula)

    def text_card(self, title: str, lines: list[str], width=5.7, body_size=22) -> VGroup:
        title_m = self.txt(title, 25, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.55, 3.45)
        box = RoundedRectangle(width=width, height=content.height + 0.60, corner_radius=0.12,
                               stroke_color=BLACK_LINE, stroke_width=1.7,
                               fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def answer_chip(self, text: str, width=4.2, size=31) -> VGroup:
        box = RoundedRectangle(width=width, height=0.86, corner_radius=0.10,
                               stroke_color=BLACK_LINE, stroke_width=1.8,
                               fill_color=PAPER_GRAY, fill_opacity=1)
        label = self.txt(text, size, BOLD)
        self.fit(label, width - 0.35, 0.55)
        label.move_to(box)
        return VGroup(box, label)

    def person(self, center=ORIGIN, scale=1.0, pose="stand") -> VGroup:
        head = Circle(radius=0.18, stroke_color=BLACK_LINE, stroke_width=2.2,
                      fill_color=WHITE, fill_opacity=1)
        torso = RoundedRectangle(width=0.44, height=0.76, corner_radius=0.16,
                                 stroke_color=BLACK_LINE, stroke_width=2.2,
                                 fill_color=PAPER_GRAY, fill_opacity=1)
        head.move_to(UP * 0.48)
        torso.move_to(DOWN * 0.02)
        if pose == "sit":
            upper_arm = Line([-0.16, 0.10, 0], [-0.36, -0.15, 0], color=BLACK_LINE, stroke_width=4.0)
            forearm = Line([-0.36, -0.15, 0], [-0.12, -0.32, 0], color=BLACK_LINE, stroke_width=4.0)
            thigh1 = Line([-0.11, -0.38, 0], [0.27, -0.42, 0], color=BLACK_LINE, stroke_width=4.4)
            shin1 = Line([0.27, -0.42, 0], [0.27, -0.86, 0], color=BLACK_LINE, stroke_width=4.4)
            thigh2 = Line([0.08, -0.38, 0], [0.39, -0.42, 0], color=BLACK_LINE, stroke_width=4.4)
            shin2 = Line([0.39, -0.42, 0], [0.39, -0.83, 0], color=BLACK_LINE, stroke_width=4.4)
            parts = VGroup(head, torso, upper_arm, forearm, thigh1, shin1, thigh2, shin2)
        else:
            if pose == "walk_a":
                arm_l_end, arm_r_end = [-0.38, -0.24, 0], [0.38, -0.03, 0]
                leg_l_end, leg_r_end = [-0.31, -0.88, 0], [0.34, -0.74, 0]
            elif pose == "walk_b":
                arm_l_end, arm_r_end = [-0.38, -0.03, 0], [0.38, -0.24, 0]
                leg_l_end, leg_r_end = [-0.34, -0.74, 0], [0.31, -0.88, 0]
            else:
                arm_l_end, arm_r_end = [-0.31, -0.30, 0], [0.31, -0.30, 0]
                leg_l_end, leg_r_end = [-0.23, -0.86, 0], [0.23, -0.86, 0]
            shoulder_l, shoulder_r = [-0.18, 0.10, 0], [0.18, 0.10, 0]
            hip_l, hip_r = [-0.10, -0.37, 0], [0.10, -0.37, 0]
            arm_l = Line(shoulder_l, arm_l_end, color=BLACK_LINE, stroke_width=4.0)
            arm_r = Line(shoulder_r, arm_r_end, color=BLACK_LINE, stroke_width=4.0)
            leg_l = Line(hip_l, leg_l_end, color=BLACK_LINE, stroke_width=4.4)
            leg_r = Line(hip_r, leg_r_end, color=BLACK_LINE, stroke_width=4.4)
            parts = VGroup(head, torso, arm_l, arm_r, leg_l, leg_r)
        parts.scale(scale).move_to(center)
        return parts

    def seat(self, center=ORIGIN, scale=1.0) -> VGroup:
        back = RoundedRectangle(width=0.58, height=0.84, corner_radius=0.08,
                                stroke_color=MID_GRAY, stroke_width=2,
                                fill_color=PAPER_GRAY, fill_opacity=1)
        base = RoundedRectangle(width=0.80, height=0.22, corner_radius=0.06,
                                stroke_color=MID_GRAY, stroke_width=2,
                                fill_color=PAPER_GRAY, fill_opacity=1)
        base.next_to(back, DOWN, buff=-0.03).shift(RIGHT * 0.15)
        leg = Line(base.get_bottom(), base.get_bottom() + DOWN * 0.42, color=MID_GRAY, stroke_width=3)
        return VGroup(back, base, leg).scale(scale).move_to(center)

    def metro_cutaway(self, center=ORIGIN, width=11.5, height=3.0) -> VGroup:
        car = RoundedRectangle(width=width, height=height, corner_radius=0.22,
                               stroke_color=BLACK_LINE, stroke_width=2.5,
                               fill_color=WHITE, fill_opacity=1)
        floor = Line(car.get_corner(DL) + UP * 0.23, car.get_corner(DR) + UP * 0.23,
                     color=DARK_GRAY, stroke_width=2.2)
        windows = VGroup()
        for x in (-4.2, -2.25, 0.0, 2.25, 4.2):
            win = RoundedRectangle(width=1.45, height=0.72, corner_radius=0.08,
                                   stroke_color=LIGHT_GRAY, stroke_width=1.5,
                                   fill_color=PAPER_GRAY, fill_opacity=1)
            win.move_to([x, 0.67, 0])
            windows.add(win)
        door_l = Line([-0.58, -1.28, 0], [-0.58, 0.22, 0], color=LIGHT_GRAY, stroke_width=1.6)
        door_r = Line([0.58, -1.28, 0], [0.58, 0.22, 0], color=LIGHT_GRAY, stroke_width=1.6)
        group = VGroup(car, floor, windows, door_l, door_r)
        group.move_to(center)
        return group

    def track(self, y=-2.20) -> VGroup:
        rail1 = Line(LEFT * 7.3 + UP * 0.12, RIGHT * 7.3 + UP * 0.12, color=DARK_GRAY, stroke_width=2.5)
        rail2 = Line(LEFT * 7.3 + DOWN * 0.12, RIGHT * 7.3 + DOWN * 0.12, color=DARK_GRAY, stroke_width=2.5)
        sleepers = VGroup(*[Line([x, -0.34, 0], [x, 0.34, 0], color=LIGHT_GRAY, stroke_width=1.2)
                            for x in [i * 0.7 for i in range(-10, 11)]])
        return VGroup(sleepers, rail1, rail2).move_to([0, y, 0])

    def velocity_arrow(self, start, end, label: str, size=28, color=BLACK_LINE) -> VGroup:
        arr = Arrow(start, end, buff=0, color=color, stroke_width=4,
                    max_tip_length_to_length_ratio=0.13)
        lab = self.eq(label, size, color=color).next_to(arr, UP, buff=0.10)
        return VGroup(arr, lab)

    def construct(self) -> None:
        self.opening()
        self.reference_frames_and_position_equation()
        self.walker_inside()
        self.walker_station()
        self.classical_comparison()
        self.light_challenge()
        self.light_clock_train_frame()
        self.light_clock_station_frame()
        self.final_synthesis()

    def opening(self) -> None:
        title = VGroup(self.txt("PHYSICS 9 • RELATIVITY EXAMPLE", 25, BOLD),
                       self.txt("RELATIVE MOTION, LIGHT, AND TIME", 44, BOLD),
                       self.txt("One situation. Two reference frames. One invariant speed.", 26)).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.48)
        tracks = self.track(y=-2.45)
        train = self.metro_cutaway(width=10.8, height=2.75).scale(0.72).move_to(LEFT * 5.0 + DOWN * 0.55)
        arrow = self.velocity_arrow(LEFT * 5.7 + DOWN * 2.95, LEFT * 1.6 + DOWN * 2.95,
                                    r"+x\;\text{(South)}", 25)
        self.play(FadeIn(title, shift=UP * 0.15), Create(tracks), FadeIn(train), run_time=RUN_SLOW)
        self.play(GrowArrow(arrow[0]), Write(arrow[1]), run_time=RUN_NORMAL)
        self.play(train.animate.shift(RIGHT * 8.8), run_time=4.4, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(title), FadeOut(tracks), FadeOut(train), FadeOut(arrow), run_time=RUN_NORMAL)

    def reference_frames_and_position_equation(self) -> None:
        self.set_header(1, "START WITH THE OBSERVER AND THE POSITION EQUATION",
                        "A velocity is always measured relative to a reference frame. We will use the same position equation throughout the lesson.")
        car = self.metro_cutaway(center=LEFT * 2.25 + DOWN * 0.20, width=9.0, height=2.65)
        s = self.seat(LEFT * 5.05 + DOWN * 0.60, 0.86)
        seated = self.person(LEFT * 4.73 + DOWN * 0.52, 0.93, "sit")
        walker = self.person(LEFT * 1.40 + DOWN * 0.50, 0.94, "stand")
        station = self.person(RIGHT * 5.55 + DOWN * 0.55, 0.98, "stand")
        ground = Line(RIGHT * 3.75 + DOWN * 1.55, RIGHT * 7.0 + DOWN * 1.55, color=DARK_GRAY, stroke_width=2.2)
        labels = VGroup(self.txt("S'  TRAIN FRAME", 23, BOLD).move_to(LEFT * 3.0 + UP * 1.70),
                        self.txt("S  STATION FRAME", 23, BOLD).move_to(RIGHT * 5.35 + UP * 1.70))
        formula = self.formula_card(r"\boxed{X=X_0+vt}", width=5.4, size=43).move_to(RIGHT * 4.80 + DOWN * 2.55)
        self.play(FadeIn(car), FadeIn(s), FadeIn(seated), FadeIn(walker), FadeIn(station), Create(ground), run_time=RUN_SLOW)
        self.play(LaggedStart(*[Write(m) for m in labels], lag_ratio=0.25), run_time=RUN_NORMAL)
        self.play(FadeIn(formula, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.play(Circumscribe(formula[1], color=MID_GRAY, time_width=0.5), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def walker_inside(self) -> None:
        self.set_header(2, "INSIDE THE METRO: THE TRAIN IS YOUR REFERENCE FRAME",
                        "Use values that are easy to calculate: the walker moves at 2 m/s relative to the train, and we observe for 5 s.")
        car = self.metro_cutaway(center=LEFT * 1.90 + DOWN * 0.10, width=10.4, height=2.80)
        seat = self.seat(LEFT * 5.60 + DOWN * 0.62, 0.84)
        observer = self.person(LEFT * 5.28 + DOWN * 0.55, 0.90, "sit")
        walker = self.person(LEFT * 3.70 + DOWN * 0.54, 0.91, "walk_a")
        inside_tag = self.txt("YOU ARE AT REST IN S'", 22, BOLD).move_to(LEFT * 4.90 + UP * 1.80)
        eq1 = self.formula_card(r"X'_{w}=X'_0+v' t'", width=4.7, size=35)
        eq2 = self.formula_card(r"X'_{w}=0+(2)(5)=10\;\mathrm{m}", width=5.4, size=35)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.85 + UP * 0.55)
        result = self.answer_chip("Inside the train: 2 m/s", width=4.9, size=28).move_to(RIGHT * 4.85 + DOWN * 1.18)
        meter = DoubleArrow(LEFT * 3.68 + DOWN * 1.78, RIGHT * 0.90 + DOWN * 1.78, buff=0.0, color=MID_GRAY, stroke_width=2.5)
        meter_label = self.txt("10 m in 5 s", 22, BOLD).next_to(meter, DOWN, buff=0.10)
        self.play(FadeIn(car), FadeIn(seat), FadeIn(observer), FadeIn(walker), Write(inside_tag), run_time=RUN_SLOW)
        self.play(FadeIn(eq1), run_time=RUN_NORMAL)
        self.play(GrowArrow(meter), Write(meter_label), run_time=RUN_NORMAL)
        for k in range(6):
            target_x = -3.70 + (4.60 * (k + 1) / 6)
            pose = "walk_a" if k % 2 == 0 else "walk_b"
            target = self.person([target_x, -0.54, 0], 0.91, pose)
            self.play(Transform(walker, target), run_time=0.45, rate_func=linear)
        self.play(FadeIn(eq2), FadeIn(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def walker_station(self) -> None:
        self.set_header(3, "FROM THE STATION: THE TRAIN AND THE WALKER BOTH MOVE",
                        "The train moves at 20 m/s (72 km/h). The same 2 m/s walking motion is added in the same direction.")
        ground = Line(LEFT * 7.0 + DOWN * 2.10, RIGHT * 7.0 + DOWN * 2.10, color=DARK_GRAY, stroke_width=2.4)
        station = self.person(RIGHT * 6.15 + DOWN * 1.12, 0.88, "stand")
        station_lab = self.txt("STATION OBSERVER", 20, BOLD).next_to(station, UP, buff=0.15)
        train = self.metro_cutaway(center=LEFT * 4.65 + DOWN * 0.38, width=7.0, height=2.35)
        walker = self.person(LEFT * 5.20 + DOWN * 0.72, 0.72, "walk_a")
        train_group = VGroup(train, walker)
        train_v = self.velocity_arrow(LEFT * 6.4 + DOWN * 2.72, LEFT * 2.4 + DOWN * 2.72, r"v_{train}=20\;\mathrm{m/s}", 25)
        formulas = VGroup(self.formula_card(r"v_{w,S}=20+2=22\;\mathrm{m/s}", width=5.4, size=34),
                          self.formula_card(r"X_{train}=0+(20)(5)=100\;\mathrm{m}", width=5.8, size=31),
                          self.formula_card(r"X_{w}=0+(22)(5)=110\;\mathrm{m}", width=5.8, size=31)).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.80 + UP * 0.52)
        result = self.answer_chip("Station: 22 m/s = 79.2 km/h", width=5.6, size=27).move_to(RIGHT * 3.85 + DOWN * 1.82)
        self.play(Create(ground), FadeIn(station), Write(station_lab), FadeIn(train_group), run_time=RUN_SLOW)
        self.play(GrowArrow(train_v[0]), Write(train_v[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(formulas[0]), run_time=RUN_NORMAL)
        self.play(train.animate.shift(RIGHT * 6.1), walker.animate.shift(RIGHT * 6.7), run_time=4.0, rate_func=linear)
        self.play(FadeIn(formulas[1]), FadeIn(formulas[2]), run_time=RUN_NORMAL)
        difference = self.txt("The walker ends 10 m ahead of the train reference point.", 22, BOLD).move_to(LEFT * 2.10 + UP * 1.70)
        self.play(Write(difference), FadeIn(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def classical_comparison(self) -> None:
        self.set_header(4, "SAME WALKER, TWO CORRECT VELOCITIES",
                        "At everyday speeds, Galilean velocity addition works: the numerical value changes when the reference frame changes.")
        divider = Line(UP * 2.30, DOWN * 3.25, color=LIGHT_GRAY, stroke_width=2)
        left = VGroup(self.txt("TRAIN FRAME S'", 27, BOLD), self.person(ORIGIN, 1.20, "walk_a"), self.answer_chip("2 m/s", width=3.4, size=31)).arrange(DOWN, buff=0.35).move_to(LEFT * 4.0 + DOWN * 0.25)
        right = VGroup(self.txt("STATION FRAME S", 27, BOLD), self.person(ORIGIN, 1.20, "walk_b"), self.answer_chip("22 m/s", width=3.4, size=31)).arrange(DOWN, buff=0.35).move_to(RIGHT * 4.0 + DOWN * 0.25)
        bridge = self.formula_card(r"v_{w,S}=v_{train,S}+v_{w,S'}", width=6.3, size=35).to_edge(DOWN, buff=0.30)
        self.play(Create(divider), FadeIn(left, shift=RIGHT * 0.15), FadeIn(right, shift=LEFT * 0.15), run_time=RUN_SLOW)
        self.play(FadeIn(bridge), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        question = self.txt("What happens if the moving object is light?", 30, BOLD).move_to(UP * 1.85)
        self.play(Write(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def light_challenge(self) -> None:
        self.set_header(5, "TURN ON A LAMP: LIGHT DOES NOT FOLLOW THE CLASSICAL ADDITION RULE",
                        "Every inertial observer measures the same vacuum light speed: c ≈ 3.00 × 10^8 m/s.")
        car = self.metro_cutaway(center=LEFT * 2.2 + DOWN * 0.20, width=9.1, height=2.7)
        seat = self.seat(LEFT * 5.0 + DOWN * 0.62, 0.82)
        observer = self.person(LEFT * 4.70 + DOWN * 0.54, 0.88, "sit")
        walker = self.person(LEFT * 1.40 + DOWN * 0.55, 0.90, "stand")
        lamp = Dot(walker.get_center() + RIGHT * 0.42 + UP * 0.10, radius=0.09, color=LIGHT_AMBER)
        pulse = Circle(radius=0.15, stroke_color=LIGHT_AMBER, stroke_width=4).move_to(lamp)
        station = self.person(RIGHT * 5.55 + DOWN * 0.70, 0.92, "stand")
        ground = Line(RIGHT * 4.10 + DOWN * 1.62, RIGHT * 7.0 + DOWN * 1.62, color=DARK_GRAY, stroke_width=2)
        c_card = self.formula_card(r"c\approx3.00\times10^8\;\mathrm{m/s}", width=5.1, size=36).move_to(RIGHT * 4.75 + UP * 1.35)
        wrong = self.txt("NOT  c + 20 m/s", 27, BOLD).move_to(RIGHT * 4.80 + DOWN * 0.10)
        right = self.txt("STATION ALSO MEASURES  c", 27, BOLD).move_to(RIGHT * 4.80 + DOWN * 0.80)
        self.play(FadeIn(car), FadeIn(seat), FadeIn(observer), FadeIn(walker), FadeIn(station), Create(ground), run_time=RUN_SLOW)
        self.play(FadeIn(lamp), run_time=RUN_QUICK)
        self.play(pulse.animate.scale(13), run_time=2.4, rate_func=smooth)
        self.play(FadeIn(c_card), Write(wrong), run_time=RUN_NORMAL)
        slash = Line(wrong.get_corner(UL), wrong.get_corner(DR), color=MID_GRAY, stroke_width=3)
        self.play(Create(slash), Write(right), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def light_clock_train_frame(self) -> None:
        self.set_header(6, "STUDENT EXERCISE — LIGHT CLOCK IN THE TRAIN FRAME",
                        "To make relativistic effects visible, imagine a hypothetical train moving at 0.60c. First solve the light clock from inside the train.")
        floor_y, ceil_y = -1.45, 1.15
        floor = Line(LEFT * 3.2 + UP * floor_y, RIGHT * 3.2 + UP * floor_y, color=BLACK_LINE, stroke_width=3)
        ceiling = Line(LEFT * 3.2 + UP * ceil_y, RIGHT * 3.2 + UP * ceil_y, color=BLACK_LINE, stroke_width=3)
        source = Dot([0, floor_y, 0], radius=0.10, color=LIGHT_AMBER)
        mirror = RoundedRectangle(width=0.85, height=0.14, corner_radius=0.04, stroke_color=BLACK_LINE, fill_color=PAPER_GRAY, fill_opacity=1).move_to([0, ceil_y, 0])
        height = DoubleArrow([2.55, floor_y, 0], [2.55, ceil_y, 0], buff=0.04, color=MID_GRAY, stroke_width=2.2)
        h_lab = self.eq(r"H=2.4\;\mathrm{m}", 27).next_to(height, RIGHT, buff=0.10)
        frame_lab = self.txt("TRAIN FRAME S'", 27, BOLD).move_to(LEFT * 4.55 + UP * 1.90)
        prompt = self.text_card("YOUR TURN", ["Light travels upward at c.", "Use X = X0 + vt.", "How long until it reaches the ceiling?"], width=5.45, body_size=23).move_to(RIGHT * 4.55 + UP * 0.55)
        generic = self.formula_card(r"X=X_0+vt", width=4.8, size=39).move_to(RIGHT * 4.55 + DOWN * 1.55)
        self.play(Create(floor), Create(ceiling), FadeIn(source), FadeIn(mirror), GrowArrow(height), Write(h_lab), Write(frame_lab), run_time=RUN_SLOW)
        self.play(FadeIn(prompt), FadeIn(generic), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK * 1.25)
        line1 = self.formula_card(r"Y_{light}=0+ct'", width=4.8, size=36)
        line2 = self.formula_card(r"2.4=ct'", width=4.8, size=36)
        line3 = self.formula_card(r"t'=\frac{2.4}{3.00\times10^8}=8.0\;\mathrm{ns}", width=5.5, size=30)
        solution = VGroup(line1, line2, line3).arrange(DOWN, buff=0.16).move_to(RIGHT * 4.55 + DOWN * 0.35)
        self.play(FadeOut(prompt), FadeOut(generic), run_time=RUN_QUICK)
        self.play(FadeIn(line1), run_time=RUN_NORMAL)
        light_dot = Dot(source.get_center(), radius=0.10, color=LIGHT_AMBER)
        path = Line(source.get_center(), mirror.get_center(), color=LIGHT_AMBER, stroke_width=4)
        self.play(FadeIn(light_dot), Create(path), light_dot.animate.move_to(mirror.get_center()), run_time=2.4, rate_func=linear)
        self.play(FadeIn(line2), FadeIn(line3), run_time=RUN_NORMAL)
        result = self.answer_chip("Inside the train: Δt' = 8.0 ns", width=5.2, size=27).move_to(LEFT * 4.60 + DOWN * 2.40)
        self.play(FadeIn(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def light_clock_station_frame(self) -> None:
        self.set_header(7, "THE SAME TWO EVENTS FROM THE STATION FRAME",
                        "The ceiling mirror moves horizontally, but the station observer still measures the light speed as c. This changes the elapsed time.")
        origin = LEFT * 4.40 + DOWN * 1.25
        height = 2.55
        horizontal = 2.55 * (self.GROUND_HORIZONTAL_M / self.CLOCK_HEIGHT)
        source = Dot(origin, radius=0.10, color=LIGHT_AMBER)
        initial_mirror = RoundedRectangle(width=0.72, height=0.13, corner_radius=0.04, stroke_color=MID_GRAY, fill_color=PAPER_GRAY, fill_opacity=1).move_to(origin + UP * height)
        final_mirror = RoundedRectangle(width=0.72, height=0.13, corner_radius=0.04, stroke_color=BLACK_LINE, fill_color=PAPER_GRAY, fill_opacity=1).move_to(origin + RIGHT * horizontal + UP * height)
        base_path = DashedLine(origin, origin + RIGHT * horizontal, color=MID_GRAY, dash_length=0.10)
        vertical = DashedLine(origin + RIGHT * horizontal, origin + RIGHT * horizontal + UP * height, color=MID_GRAY, dash_length=0.10)
        light_path = Line(origin, final_mirror.get_center(), color=LIGHT_AMBER, stroke_width=4)
        moving_arrow = self.velocity_arrow(origin + DOWN * 0.62, origin + RIGHT * horizontal + DOWN * 0.62, r"v=0.60c", 26)
        labels = VGroup(self.eq(r"\Delta x=1.8\;\mathrm{m}", 25).next_to(base_path, DOWN, buff=0.12),
                        self.eq(r"H=2.4\;\mathrm{m}", 25).next_to(vertical, RIGHT, buff=0.12),
                        self.eq(r"d_{light}=3.0\;\mathrm{m}", 25, color=LIGHT_AMBER).next_to(light_path, LEFT, buff=0.12))
        xeq = self.formula_card(r"X_{mirror}=X_0+vt=0+(0.60c)t", width=6.0, size=32).move_to(RIGHT * 4.45 + UP * 1.70)
        prompt = self.text_card("YOUR TURN", ["The light still moves at c.", "The mirror moves at 0.60c.", "What time does the station measure?"], width=5.75, body_size=22).move_to(RIGHT * 4.45 + DOWN * 0.15)
        self.play(FadeIn(source), FadeIn(initial_mirror), FadeIn(final_mirror), Create(base_path), Create(vertical), run_time=RUN_SLOW)
        self.play(GrowArrow(moving_arrow[0]), Write(moving_arrow[1]), FadeIn(xeq), FadeIn(prompt), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK * 1.25)
        self.play(FadeOut(prompt), run_time=RUN_QUICK)
        light_dot = Dot(source.get_center(), radius=0.10, color=LIGHT_AMBER)
        self.play(Create(light_path), FadeIn(light_dot), light_dot.animate.move_to(final_mirror.get_center()), run_time=2.5, rate_func=linear)
        self.play(LaggedStart(*[Write(m) for m in labels], lag_ratio=0.20), run_time=RUN_SLOW)
        derivation = VGroup(self.formula_card(r"(ct)^2=(0.60ct)^2+(2.4)^2", width=6.2, size=30),
                            self.formula_card(r"0.64c^2t^2=5.76", width=6.2, size=32),
                            self.formula_card(r"ct=3.0\;\mathrm{m}", width=6.2, size=34),
                            self.formula_card(r"t=\frac{3.0}{3.00\times10^8}=10.0\;\mathrm{ns}", width=6.2, size=29)).arrange(DOWN, buff=0.14).move_to(RIGHT * 4.45 + DOWN * 0.62)
        self.play(FadeOut(xeq), run_time=RUN_QUICK)
        for card in derivation:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_EXPLAIN)
        left_result = self.answer_chip("Train frame: 8.0 ns", width=4.3, size=27).move_to(LEFT * 4.50 + DOWN * 2.55)
        right_result = self.answer_chip("Station frame: 10.0 ns", width=4.5, size=27).move_to(RIGHT * 4.45 + DOWN * 2.72)
        self.play(FadeIn(left_result), FadeIn(right_result), run_time=RUN_NORMAL)
        conclusion = self.txt("SAME LIGHT SPEED  c  •  DIFFERENT ELAPSED COORDINATE TIME", 28, BOLD).to_edge(DOWN, buff=0.18)
        self.play(Write(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

    def final_synthesis(self) -> None:
        self.set_header(8, "FINAL SYNTHESIS — WHAT CHANGED, AND WHAT DID NOT?",
                        "The position equation organizes the motion. Classical velocities add at everyday speeds; light speed remains invariant, so space and time coordinates cannot both stay absolute.")
        general = self.formula_card(r"\boxed{X=X_0+vt}", width=5.2, size=42).move_to(LEFT * 4.60 + UP * 1.55)
        classical = self.text_card("ORDINARY METRO", ["Train: 20 m/s", "Walker relative to train: 2 m/s", "Walker from station: 22 m/s"], width=5.4, body_size=23).move_to(LEFT * 4.60 + DOWN * 0.45)
        light = self.text_card("RELATIVISTIC LIGHT CLOCK", ["Light speed in S': c", "Light speed in S: c", "Elapsed time: 8.0 ns vs 10.0 ns"], width=5.4, body_size=23).move_to(RIGHT * 4.40 + UP * 0.60)
        verify = self.formula_card(r"\gamma=\frac{1}{\sqrt{1-0.60^2}}=1.25,\qquad 1.25(8.0\,\mathrm{ns})=10.0\,\mathrm{ns}", width=7.2, size=27).move_to(RIGHT * 4.40 + DOWN * 1.65)
        self.play(FadeIn(general), FadeIn(classical), run_time=RUN_SLOW)
        self.play(FadeIn(light), run_time=RUN_NORMAL)
        self.play(FadeIn(verify), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(*[FadeOut(m) for m in [general, classical, light, verify]], run_time=RUN_NORMAL)
        question = VGroup(self.txt("EXIT QUESTION", 27, BOLD),
                          self.txt("If both observers measure the same light speed c,", 30),
                          self.txt("why can they measure different elapsed times for the same two events?", 30, BOLD)).arrange(DOWN, buff=0.22).move_to(DOWN * 0.10)
        self.play(FadeIn(question, shift=UP * 0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)

# Preview:
#   manim -pql metro_relativity_v3_2d_english.py Physics9MetroRelativityV3 --disable_caching
# Final:
#   manim -pqh metro_relativity_v3_2d_english.py Physics9MetroRelativityV3 --disable_caching
