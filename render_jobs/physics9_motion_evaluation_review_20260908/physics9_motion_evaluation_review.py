#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Motion Evaluation Review.

Full ManimCE scene built from the competency structure of the three evaluation
versions (A/B/C), but using new numerical data so it functions as practice and
review rather than as an answer key.

Target: Manim Community Edition 0.20.1
Render: 1920x1080, 30 fps, white classroom style.
"""

from __future__ import annotations

import math
from manim import *

# -----------------------------------------------------------------------------
# Render configuration
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

# -----------------------------------------------------------------------------
# Visual system
# -----------------------------------------------------------------------------
INK = BLACK
DARK = "#2B2B2B"
MID = "#6C6C6C"
LIGHT = "#D6D6D6"
PALE = "#F4F4F4"
ACCENT = "#1E5AA8"
ACCENT_2 = "#2F7D32"
WARN = "#B33A3A"

FRAME_W = 16.0
FRAME_H = 9.0
SAFE_W = 14.8

RUN_FAST = 0.55
RUN = 0.9
RUN_SLOW = 1.35
PAUSE = 1.1
READ = 1.8
EXPLAIN = 2.5
WORK = 3.3


# -----------------------------------------------------------------------------
# Validated practice data — deliberately different from evaluation A/B/C
# -----------------------------------------------------------------------------
P1_LEAD = 18.0
P1_FAST = 12.0
P1_SLOW = 6.0
P1_T = P1_LEAD / (P1_FAST - P1_SLOW)
P1_X = P1_FAST * P1_T

P2_X0 = -24.0
P2_V = 7.0
P2_QUERY_T = 6.0
P2_X_AT_QUERY = P2_X0 + P2_V * P2_QUERY_T
P2_TARGET = 32.0
P2_TARGET_T = (P2_TARGET - P2_X0) / P2_V

P3_L = 180.0
P3_VA = 70.0
P3_VB_SIGNED = -50.0
P3_T = P3_L / (P3_VA + abs(P3_VB_SIGNED))
P3_X = P3_VA * P3_T

P4_T = list(range(8))
P4_X = [-1, 2, 5, 8, 8, 8, 6, 4]
P4_V1 = (P4_X[3] - P4_X[0]) / 3
P4_V2 = (P4_X[5] - P4_X[3]) / 2
P4_V3 = (P4_X[7] - P4_X[5]) / 2


def validate_data() -> None:
    assert math.isclose(P1_T, 3.0)
    assert math.isclose(P1_X, 36.0)
    assert math.isclose(P2_X_AT_QUERY, 18.0)
    assert math.isclose(P2_TARGET_T, 8.0)
    assert math.isclose(P3_T, 1.5)
    assert math.isclose(P3_X, 105.0)
    assert math.isclose(P3_L + P3_VB_SIGNED * P3_T, P3_X)
    assert P4_V1 == 3.0
    assert P4_V2 == 0.0
    assert P4_V3 == -2.0
    assert max(abs(x) for x in P4_X) == 8


# -----------------------------------------------------------------------------
# Reusable drawing helpers
# -----------------------------------------------------------------------------
def fit(mob: Mobject, max_w: float, max_h: float | None = None) -> Mobject:
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    if max_h is not None and mob.height > max_h:
        mob.scale_to_fit_height(max_h)
    return mob


def label_text(text: str, size: int = 28, weight=NORMAL, color=INK) -> Text:
    return Text(text, font_size=size, weight=weight, color=color)


def make_panel(width: float, height: float, fill_color=WHITE, stroke_color=DARK) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.13,
        stroke_color=stroke_color,
        stroke_width=1.8,
        fill_color=fill_color,
        fill_opacity=1,
    )


def make_vehicle(name: str, scale: float = 1.0, color=ACCENT) -> VGroup:
    body = RoundedRectangle(
        width=1.15,
        height=0.46,
        corner_radius=0.10,
        stroke_color=color,
        fill_color=WHITE,
        fill_opacity=1,
        stroke_width=2.4,
    )
    cab = Polygon(
        [-0.18, 0.23, 0],
        [0.16, 0.23, 0],
        [0.34, 0.05, 0],
        [-0.18, 0.05, 0],
        stroke_color=color,
        fill_color=WHITE,
        fill_opacity=1,
        stroke_width=2,
    ).shift(RIGHT * 0.10)
    w1 = Circle(radius=0.09, color=DARK, fill_color=DARK, fill_opacity=1).shift(LEFT * 0.34 + DOWN * 0.26)
    w2 = Circle(radius=0.09, color=DARK, fill_color=DARK, fill_opacity=1).shift(RIGHT * 0.34 + DOWN * 0.26)
    tag = label_text(name, 18, BOLD, color).next_to(body, UP, buff=0.10)
    return VGroup(body, cab, w1, w2, tag).scale(scale)


def number_line_track(x_min: float, x_max: float, length: float = 11.7) -> tuple[NumberLine, float]:
    line = NumberLine(
        x_range=[x_min, x_max, max(1, (x_max - x_min) / 6)],
        length=length,
        include_numbers=False,
        include_tip=True,
        color=DARK,
        stroke_width=2,
    )
    return line, length / (x_max - x_min)


class Physics9MotionEvaluationReview(Scene):
    """Full lesson/review scene aligned to the evaluation competency structure."""

    def setup(self):
        super().setup()
        validate_data()
        self.camera.background_color = WHITE
        self.header_group = None

    # ------------------------------------------------------------------
    # Scene infrastructure
    # ------------------------------------------------------------------
    def clear_stage(self, keep_header: bool = True, run_time: float = RUN_FAST):
        keep = {self.header_group} if (keep_header and self.header_group is not None) else set()
        to_remove = [m for m in self.mobjects if m not in keep]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove], run_time=run_time)

    def set_header(self, n: int, title: str, subtitle: str):
        if self.header_group is not None:
            self.play(FadeOut(self.header_group), run_time=RUN_FAST)
        badge = Circle(radius=0.35, stroke_color=DARK, stroke_width=2, fill_color=PALE, fill_opacity=1)
        num = label_text(str(n), 28, BOLD).move_to(badge)
        title_m = label_text(title, 31, BOLD)
        subtitle_m = label_text(subtitle, 20, NORMAL, MID)
        left = VGroup(badge, num)
        text_group = VGroup(title_m, subtitle_m).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        group = VGroup(left, text_group).arrange(RIGHT, buff=0.28, aligned_edge=UP)
        fit(group, 14.3, 1.0)
        group.to_edge(UP, buff=0.22).to_edge(LEFT, buff=0.55)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, color=LIGHT, stroke_width=1.5).next_to(group, DOWN, buff=0.16)
        self.header_group = VGroup(group, rule)
        self.play(FadeIn(self.header_group, shift=DOWN * 0.08), run_time=RUN)

    def formula_box(self, formula: str, width=6.3, height=1.05, size=42, color=INK) -> VGroup:
        box = make_panel(width, height, fill_color=PALE)
        eq = MathTex(formula, color=color, font_size=size)
        fit(eq, width - 0.45, height - 0.18)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_box(self, title: str, lines: list[str], width=6.2, body_size=23) -> VGroup:
        heading = label_text(title, 25, BOLD)
        body = VGroup(*[label_text(line, body_size) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(heading, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fit(content, width - 0.55, 3.6)
        box = make_panel(width, content.height + 0.58)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    # ------------------------------------------------------------------
    # Opening / evaluation map
    # ------------------------------------------------------------------
    def opening(self):
        title = label_text("PHYSICS 9 — MOTION REVIEW", 50, BOLD)
        sub = label_text("Practice problems aligned to the evaluation structure", 28, NORMAL, MID)
        tag = label_text("Uniform Motion • Position–Time Graphs • Velocity", 24, BOLD, ACCENT)
        group = VGroup(title, sub, tag).arrange(DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=RUN)
        self.play(FadeIn(sub), FadeIn(tag), run_time=RUN)
        self.wait(READ)

        cards_data = [
            ("A", "Pursuit + equations", "15 pts"),
            ("B", "Uniform motion", "15 pts"),
            ("C", "Two-object meeting", "20 pts"),
            ("D", "Build x–t graph", "25 pts"),
            ("E", "Slope → velocity", "25 pts"),
        ]
        cards = VGroup()
        for letter, name, pts in cards_data:
            box = make_panel(2.65, 1.35, fill_color=WHITE)
            l = label_text(letter, 28, BOLD, ACCENT)
            nm = label_text(name, 19, BOLD)
            p = label_text(pts, 18, NORMAL, MID)
            content = VGroup(l, nm, p).arrange(DOWN, buff=0.08).move_to(box)
            fit(content, 2.3, 1.08)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.16).move_to(DOWN * 1.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.12), run_time=RUN_SLOW * 1.5)
        self.wait(WORK)
        self.play(FadeOut(group), FadeOut(cards), run_time=RUN)

    # ------------------------------------------------------------------
    # Problem 1 — pursuit
    # ------------------------------------------------------------------
    def problem_1_pursuit(self):
        self.set_header(1, "PURSUIT: WHEN DOES THE FASTER OBJECT CATCH THE OTHER?", "Translate the picture into two position equations, then set the positions equal.")

        statement = self.note_box(
            "PRACTICE PROBLEM",
            [
                "A patrol robot starts at x = 0 m.",
                "A service cart is 18 m ahead.",
                "They move in +x at 12 m/s and 6 m/s.",
                "Find the catching time and meeting position.",
            ],
            width=5.8,
            body_size=22,
        ).move_to(LEFT * 4.6 + DOWN * 0.35)

        track, _ = number_line_track(0, 48, 7.1)
        track.move_to(RIGHT * 3.2 + DOWN * 0.85)
        x0 = track.n2p(0)
        x18 = track.n2p(18)
        x36 = track.n2p(36)
        robot = make_vehicle("robot", 0.72, ACCENT).move_to(x0 + UP * 0.55)
        cart = make_vehicle("cart", 0.72, ACCENT_2).move_to(x18 + UP * 0.55)
        markers = VGroup(
            label_text("0 m", 18, NORMAL, MID).next_to(track.n2p(0), DOWN, buff=0.16),
            label_text("18 m", 18, NORMAL, MID).next_to(track.n2p(18), DOWN, buff=0.16),
            label_text("36 m", 18, NORMAL, MID).next_to(track.n2p(36), DOWN, buff=0.16),
        )
        arrows = VGroup(
            Arrow(robot.get_right(), robot.get_right() + RIGHT * 1.05, buff=0.05, color=ACCENT, stroke_width=4),
            Arrow(cart.get_right(), cart.get_right() + RIGHT * 0.70, buff=0.05, color=ACCENT_2, stroke_width=4),
        )
        speed_labels = VGroup(
            MathTex(r"12\,\mathrm{m/s}", color=ACCENT, font_size=28).next_to(arrows[0], UP, buff=0.05),
            MathTex(r"6\,\mathrm{m/s}", color=ACCENT_2, font_size=28).next_to(arrows[1], UP, buff=0.05),
        )
        visual = VGroup(track, markers, robot, cart, arrows, speed_labels)

        self.play(FadeIn(statement), FadeIn(track), FadeIn(markers), run_time=RUN)
        self.play(FadeIn(robot), FadeIn(cart), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(speed_labels), run_time=RUN)
        self.wait(EXPLAIN)

        eqs = VGroup(
            self.formula_box(r"x_1(t)=0+12t", width=3.6, height=0.88, size=34),
            self.formula_box(r"x_2(t)=18+6t", width=3.6, height=0.88, size=34),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.2 + UP * 1.55)
        self.play(FadeIn(eqs[0]), run_time=RUN)
        self.play(FadeIn(eqs[1]), run_time=RUN)
        self.wait(READ)

        meet_eq = self.formula_box(r"12t=18+6t", width=4.2, height=0.95, size=38, color=ACCENT).move_to(RIGHT * 3.2 + UP * 0.15)
        self.play(FadeIn(meet_eq), run_time=RUN)
        self.wait(PAUSE)
        solve = VGroup(
            MathTex(r"6t=18", color=INK, font_size=38),
            MathTex(r"t=3\,\mathrm{s}", color=ACCENT, font_size=42),
            MathTex(r"x=12(3)=36\,\mathrm{m}", color=ACCENT_2, font_size=38),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.2 + DOWN * 2.25)
        self.play(Write(solve[0]), run_time=RUN)
        self.play(Write(solve[1]), run_time=RUN)
        self.play(robot.animate.move_to(x36 + UP * 0.55), cart.animate.move_to(x36 + UP * 0.55), run_time=2.2, rate_func=linear)
        self.play(Write(solve[2]), run_time=RUN)
        self.wait(EXPLAIN)

        zeno = self.note_box(
            "ZENO'S IDEA — THE KEY POINT",
            [
                "Infinitely many described checkpoints can fit",
                "inside a finite total time.",
                "The intervals get smaller; their sum can converge.",
            ],
            width=6.0,
            body_size=21,
        ).move_to(LEFT * 4.6 + DOWN * 2.70)
        self.play(FadeIn(zeno, shift=UP * 0.10), run_time=RUN)
        self.wait(WORK)
        self.clear_stage(keep_header=True)

    # ------------------------------------------------------------------
    # Problem 2 — general uniform motion
    # ------------------------------------------------------------------
    def problem_2_uniform_motion(self):
        self.set_header(2, "GENERAL EQUATION OF UNIFORM MOTION", "Read the initial position and the signed velocity before substituting any number.")

        base_formula = self.formula_box(r"x=x_i+vt", width=4.2, height=1.05, size=46).move_to(LEFT * 4.9 + UP * 1.95)
        data = self.note_box(
            "PRACTICE DATA",
            [
                "xᵢ = −24 m",
                "v = +7 m/s",
                "Find x at t = 6 s.",
                "Then find when x = 32 m.",
            ],
            width=5.1,
            body_size=23,
        ).move_to(LEFT * 4.9 + DOWN * 0.45)

        track, _ = number_line_track(-30, 40, 7.7)
        track.move_to(RIGHT * 3.4 + DOWN * 0.70)
        p0 = track.n2p(P2_X0)
        p6 = track.n2p(P2_X_AT_QUERY)
        pt = track.n2p(P2_TARGET)
        trolley = make_vehicle("trolley", 0.78, ACCENT).move_to(p0 + UP * 0.58)
        dots = VGroup(
            Dot(p0, radius=0.055, color=DARK),
            Dot(p6, radius=0.055, color=ACCENT_2),
            Dot(pt, radius=0.055, color=WARN),
        )
        labels = VGroup(
            label_text("−24 m", 18, NORMAL, MID).next_to(p0, DOWN, buff=0.15),
            label_text("18 m", 18, NORMAL, ACCENT_2).next_to(p6, DOWN, buff=0.15),
            label_text("32 m target", 18, NORMAL, WARN).next_to(pt, DOWN, buff=0.15),
        )

        self.play(FadeIn(base_formula), FadeIn(data), FadeIn(track), FadeIn(trolley), FadeIn(dots), FadeIn(labels), run_time=RUN)
        self.wait(READ)

        equation = self.formula_box(r"x(t)=-24+7t", width=5.0, height=0.98, size=40).move_to(RIGHT * 3.45 + UP * 2.05)
        self.play(FadeIn(equation), run_time=RUN)
        sub = MathTex(r"x(6)=-24+7(6)=18\,\mathrm{m}", color=ACCENT_2, font_size=38).move_to(RIGHT * 3.45 + UP * 0.75)
        self.play(Write(sub), run_time=RUN)
        self.play(trolley.animate.move_to(p6 + UP * 0.58), run_time=1.8, rate_func=linear)
        self.wait(EXPLAIN)

        target_steps = VGroup(
            MathTex(r"32=-24+7t", color=INK, font_size=36),
            MathTex(r"56=7t", color=INK, font_size=36),
            MathTex(r"t=8\,\mathrm{s}", color=ACCENT, font_size=42),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.45 + DOWN * 2.15)
        self.play(Write(target_steps[0]), run_time=RUN)
        self.play(Write(target_steps[1]), run_time=RUN)
        self.play(Write(target_steps[2]), trolley.animate.move_to(pt + UP * 0.58), run_time=1.6)
        sign_note = label_text("Positive velocity → motion in +x", 22, BOLD, ACCENT).next_to(track, DOWN, buff=0.75)
        self.play(FadeIn(sign_note), run_time=RUN)
        self.wait(WORK)
        self.clear_stage(keep_header=True)

    # ------------------------------------------------------------------
    # Problem 3 — two cars
    # ------------------------------------------------------------------
    def problem_3_meeting(self):
        self.set_header(3, "TWO VEHICLES: WHERE DO THEY MEET?", "Choose one axis first. The object moving toward −x must have a negative signed velocity.")

        city_a = VGroup(
            Rectangle(width=1.1, height=0.65, stroke_color=DARK, fill_color=PALE, fill_opacity=1),
            Triangle(color=DARK, fill_color=WHITE, fill_opacity=1).scale(0.48).shift(UP * 0.48),
            label_text("CITY A", 20, BOLD).shift(DOWN * 0.62),
        ).move_to(LEFT * 5.4 + DOWN * 0.45)
        city_b = city_a.copy().move_to(RIGHT * 5.4 + DOWN * 0.45)
        city_b[-1].become(label_text("CITY B", 20, BOLD).move_to(city_b[-1]))
        road = Line(city_a.get_right() + RIGHT * 0.2, city_b.get_left() + LEFT * 0.2, color=DARK, stroke_width=3)
        mid_label = label_text("180 km", 22, BOLD, MID).next_to(road, DOWN, buff=0.25)
        plusx = Arrow(road.get_center() + DOWN * 0.62 + LEFT * 1.0, road.get_center() + DOWN * 0.62 + RIGHT * 1.0, buff=0, color=ACCENT, stroke_width=3)
        plusx_lab = MathTex(r"+x", color=ACCENT, font_size=28).next_to(plusx, RIGHT, buff=0.10)

        car_a = make_vehicle("A", 0.65, ACCENT).move_to(city_a.get_right() + RIGHT * 0.65 + UP * 0.35)
        car_b = make_vehicle("B", 0.65, ACCENT_2).move_to(city_b.get_left() + LEFT * 0.65 + UP * 0.35)

        self.play(FadeIn(city_a), FadeIn(city_b), Create(road), FadeIn(mid_label), GrowArrow(plusx), FadeIn(plusx_lab), run_time=RUN)
        self.play(FadeIn(car_a), FadeIn(car_b), run_time=RUN)

        signed = VGroup(
            self.formula_box(r"x_A(0)=0,\quad v_A=+70\,\mathrm{km/h}", width=6.3, height=0.86, size=31),
            self.formula_box(r"x_B(0)=180,\quad v_B=-50\,\mathrm{km/h}", width=6.3, height=0.86, size=31),
        ).arrange(DOWN, buff=0.16).move_to(LEFT * 4.35 + UP * 2.05)
        eqs = VGroup(
            MathTex(r"x_A(t)=70t", color=ACCENT, font_size=36),
            MathTex(r"x_B(t)=180-50t", color=ACCENT_2, font_size=36),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.7 + UP * 2.05)
        self.play(FadeIn(signed), FadeIn(eqs), run_time=RUN)
        self.wait(READ)

        meet = VGroup(
            MathTex(r"70t=180-50t", color=INK, font_size=38),
            MathTex(r"120t=180", color=INK, font_size=38),
            MathTex(r"t=1.5\,\mathrm{h}", color=ACCENT, font_size=42),
            MathTex(r"x=70(1.5)=105\,\mathrm{km}", color=ACCENT_2, font_size=38),
        ).arrange(DOWN, buff=0.14).move_to(DOWN * 2.15)
        for m in meet[:3]:
            self.play(Write(m), run_time=RUN)
        meeting_point = city_a.get_center()[0] + (city_b.get_center()[0] - city_a.get_center()[0]) * (P3_X / P3_L)
        target = np.array([meeting_point, road.get_y() + 0.35, 0])
        self.play(car_a.animate.move_to(target), car_b.animate.move_to(target), run_time=2.3, rate_func=linear)
        self.play(Write(meet[3]), run_time=RUN)
        meaning = label_text("At the meeting instant, both objects have the same position coordinate.", 22, BOLD).next_to(meet, DOWN, buff=0.22)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(WORK)
        self.clear_stage(keep_header=True)

    # ------------------------------------------------------------------
    # Problem 4 — construct and interpret x-t graph
    # ------------------------------------------------------------------
    def problem_4_position_graph(self):
        self.set_header(4, "CONSTRUCT AND INTERPRET A POSITION–TIME GRAPH", "Plot the measured points first; only then interpret direction, rest, and distance from the origin.")

        table_data = [[str(t) for t in P4_T], [str(x) for x in P4_X]]
        table = Table(
            table_data,
            row_labels=[MathTex(r"t\,(s)", color=INK), MathTex(r"x\,(m)", color=INK)],
            include_outer_lines=True,
            line_config={"stroke_color": DARK, "stroke_width": 1.3},
            element_to_mobject_config={"color": INK, "font_size": 24},
        ).scale(0.58).move_to(LEFT * 3.45 + UP * 1.95)

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[-2, 9, 1],
            x_length=7.15,
            y_length=5.15,
            axis_config={"color": DARK, "stroke_width": 2, "include_numbers": True, "font_size": 22, "include_tip": True},
            tips=True,
        ).move_to(RIGHT * 3.35 + DOWN * 0.55)
        xlab = axes.get_x_axis_label(MathTex(r"t\,(s)", color=INK, font_size=28), edge=RIGHT, direction=DOWN, buff=0.12)
        ylab = axes.get_y_axis_label(MathTex(r"x\,(m)", color=INK, font_size=28), edge=UP, direction=LEFT, buff=0.10)

        guide = self.note_box(
            "GRAPHING ROUTE",
            [
                "1. Time goes on the horizontal axis.",
                "2. Position goes on the vertical axis.",
                "3. Plot all eight coordinates.",
                "4. Connect chronological measurements.",
            ],
            width=5.8,
            body_size=20,
        ).move_to(LEFT * 3.5 + DOWN * 1.10)

        self.play(FadeIn(table), FadeIn(guide), Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=RUN)
        self.wait(READ)

        points = VGroup(*[Dot(axes.c2p(t, x), radius=0.065, color=ACCENT) for t, x in zip(P4_T, P4_X)])
        segments = VGroup(*[
            Line(axes.c2p(P4_T[i], P4_X[i]), axes.c2p(P4_T[i + 1], P4_X[i + 1]), color=ACCENT, stroke_width=3)
            for i in range(len(P4_T) - 1)
        ])
        for i, dot in enumerate(points):
            self.play(FadeIn(dot, scale=1.5), run_time=0.22)
            if i > 0:
                self.play(Create(segments[i - 1]), run_time=0.28)
        self.wait(EXPLAIN)

        self.play(FadeOut(table), FadeOut(guide), run_time=RUN_FAST)
        interpretation = VGroup(
            self.note_box("0–3 s", ["Position increases", "→ moving in +x"], width=3.45, body_size=20),
            self.note_box("3–5 s", ["Position is constant", "→ at rest"], width=3.45, body_size=20),
            self.note_box("5–7 s", ["Position decreases", "→ moving in −x"], width=3.45, body_size=20),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 4.8 + DOWN * 0.20)
        self.play(LaggedStart(*[FadeIn(card, shift=RIGHT * 0.10) for card in interpretation], lag_ratio=0.18), run_time=RUN_SLOW * 1.6)

        highlight_top = Line(axes.c2p(3, 8), axes.c2p(5, 8), color=ACCENT_2, stroke_width=7)
        far = label_text("Farthest from the origin: |x| = 8 m during 3–5 s", 22, BOLD, ACCENT_2).next_to(axes, DOWN, buff=0.42)
        self.play(Create(highlight_top), FadeIn(far), run_time=RUN)
        self.wait(WORK)
        # Keep graph for the next section; clear only left interpretation and top highlight note.
        self.play(FadeOut(interpretation), FadeOut(far), FadeOut(highlight_top), run_time=RUN_FAST)
        self.position_axes = axes
        self.position_xlab = xlab
        self.position_ylab = ylab
        self.position_points = points
        self.position_segments = segments

    # ------------------------------------------------------------------
    # Problem 5 — slope and velocity graph
    # ------------------------------------------------------------------
    def problem_5_velocity(self):
        # Clear previous header only, preserve graph while switching section.
        if self.header_group is not None:
            self.play(FadeOut(self.header_group), run_time=RUN_FAST)
        self.header_group = None
        self.set_header(5, "VELOCITY IS THE SLOPE OF AN x–t GRAPH", "For each straight segment, compute Δx/Δt; then transfer that constant value to a v–t graph.")

        # Move the existing position graph to the left to create a side-by-side comparison.
        xgraph = VGroup(self.position_axes, self.position_xlab, self.position_ylab, self.position_points, self.position_segments)
        self.play(xgraph.animate.scale(0.80).move_to(LEFT * 3.65 + DOWN * 0.55), run_time=RUN)

        slope_formula = self.formula_box(r"v=\mathrm{slope}=\frac{\Delta x}{\Delta t}", width=5.1, height=1.02, size=40).move_to(RIGHT * 3.8 + UP * 2.05)
        self.play(FadeIn(slope_formula), run_time=RUN)

        calculations = VGroup(
            MathTex(r"0\to3:\quad v=\frac{8-(-1)}{3-0}=3\,\mathrm{m/s}", color=ACCENT, font_size=32),
            MathTex(r"3\to5:\quad v=\frac{8-8}{5-3}=0\,\mathrm{m/s}", color=ACCENT_2, font_size=32),
            MathTex(r"5\to7:\quad v=\frac{4-8}{7-5}=-2\,\mathrm{m/s}", color=WARN, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.85 + UP * 0.45)
        for calc in calculations:
            self.play(Write(calc), run_time=RUN)
            self.wait(PAUSE)

        meaning = self.note_box(
            "PHYSICAL MEANING OF SLOPE",
            [
                "positive slope → +x motion",
                "zero slope → rest",
                "negative slope → −x motion",
            ],
            width=5.6,
            body_size=21,
        ).move_to(RIGHT * 3.85 + DOWN * 2.18)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(EXPLAIN)

        self.play(FadeOut(slope_formula), FadeOut(calculations), FadeOut(meaning), run_time=RUN_FAST)
        self.play(xgraph.animate.scale(0.78).move_to(LEFT * 4.05 + DOWN * 0.55), run_time=RUN)

        v_axes = Axes(
            x_range=[0, 7, 1],
            y_range=[-3, 4, 1],
            x_length=6.2,
            y_length=4.55,
            axis_config={"color": DARK, "stroke_width": 2, "include_numbers": True, "font_size": 20, "include_tip": True},
            tips=True,
        ).move_to(RIGHT * 3.8 + DOWN * 0.55)
        vxl = v_axes.get_x_axis_label(MathTex(r"t\,(s)", color=INK, font_size=26), edge=RIGHT, direction=DOWN, buff=0.10)
        vyl = v_axes.get_y_axis_label(MathTex(r"v\,(m/s)", color=INK, font_size=26), edge=UP, direction=LEFT, buff=0.08)
        self.play(Create(v_axes), FadeIn(vxl), FadeIn(vyl), run_time=RUN)

        step1 = Line(v_axes.c2p(0, P4_V1), v_axes.c2p(3, P4_V1), color=ACCENT, stroke_width=6)
        step2 = Line(v_axes.c2p(3, P4_V2), v_axes.c2p(5, P4_V2), color=ACCENT_2, stroke_width=6)
        step3 = Line(v_axes.c2p(5, P4_V3), v_axes.c2p(7, P4_V3), color=WARN, stroke_width=6)
        connectors = VGroup(
            DashedLine(v_axes.c2p(3, P4_V1), v_axes.c2p(3, P4_V2), dash_length=0.08, color=LIGHT),
            DashedLine(v_axes.c2p(5, P4_V2), v_axes.c2p(5, P4_V3), dash_length=0.08, color=LIGHT),
        )
        labels = VGroup(
            MathTex(r"+3", color=ACCENT, font_size=30).next_to(step1, UP, buff=0.10),
            MathTex(r"0", color=ACCENT_2, font_size=30).next_to(step2, UP, buff=0.10),
            MathTex(r"-2", color=WARN, font_size=30).next_to(step3, DOWN, buff=0.10),
        )
        self.play(Create(step1), FadeIn(labels[0]), run_time=RUN)
        self.play(Create(connectors[0]), Create(step2), FadeIn(labels[1]), run_time=RUN)
        self.play(Create(connectors[1]), Create(step3), FadeIn(labels[2]), run_time=RUN)
        transfer = label_text("Same motion, two graphs: slope in x–t becomes height in v–t.", 23, BOLD).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(transfer), run_time=RUN)
        self.wait(WORK)
        self.clear_stage(keep_header=True)

    # ------------------------------------------------------------------
    # Final method map
    # ------------------------------------------------------------------
    def summary(self):
        self.set_header(6, "A REPRODUCIBLE METHOD FOR THE EVALUATION", "Use the same reasoning pattern even when the numbers, signs, or contexts change.")
        cards_data = [
            ("1", "CHOOSE +x", "Fix the coordinate system before assigning signs."),
            ("2", "WRITE x(t)", "Use x = xᵢ + vt for each uniform-motion object."),
            ("3", "SAME PLACE?", "At a meeting or catch: set the two positions equal."),
            ("4", "READ x–t", "Increasing / flat / decreasing tells the direction or rest."),
            ("5", "SLOPE = v", "Compute Δx/Δt, then draw the corresponding v–t level."),
        ]
        cards = VGroup()
        for num, title, body in cards_data:
            box = make_panel(4.55, 1.36, fill_color=WHITE)
            badge = Circle(radius=0.28, color=ACCENT, stroke_width=2).move_to(box.get_left() + RIGHT * 0.48)
            n = label_text(num, 21, BOLD, ACCENT).move_to(badge)
            t = label_text(title, 21, BOLD).move_to(box.get_center() + UP * 0.25 + LEFT * 0.40).align_to(box, LEFT).shift(RIGHT * 0.95)
            b = label_text(body, 17, NORMAL, MID).next_to(t, DOWN, buff=0.10, aligned_edge=LEFT)
            fit(b, 3.25, 0.45)
            cards.add(VGroup(box, badge, n, t, b))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.32, 0.25)).move_to(DOWN * 0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in cards], lag_ratio=0.10), run_time=RUN_SLOW * 2)
        final = self.formula_box(r"x=x_i+vt\qquad v=\frac{\Delta x}{\Delta t}", width=7.1, height=1.0, size=40).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(final), run_time=RUN)
        self.wait(WORK)
        closing = label_text("Practice the method — not the memorized numbers.", 29, BOLD, ACCENT)
        closing.move_to(UP * 0.05)
        self.play(FadeOut(cards), FadeOut(final), run_time=RUN)
        self.play(Write(closing), run_time=RUN)
        self.wait(EXPLAIN)
        self.play(FadeOut(closing), FadeOut(self.header_group), run_time=RUN)

    # ------------------------------------------------------------------
    # Full timeline
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.problem_1_pursuit()
        self.problem_2_uniform_motion()
        self.problem_3_meeting()
        self.problem_4_position_graph()
        self.problem_5_velocity()
        self.summary()


# Preview:
# manim -pql physics9_motion_evaluation_review.py Physics9MotionEvaluationReview --disable_caching
# Final:
# manim -pqh physics9_motion_evaluation_review.py Physics9MotionEvaluationReview --fps 30 --disable_caching
