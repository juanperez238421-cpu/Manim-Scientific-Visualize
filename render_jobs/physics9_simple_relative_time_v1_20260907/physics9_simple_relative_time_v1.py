#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Special Relativity
A deliberately simple classroom problem: same light speed, different path,
therefore different measured time.

No gamma, no Lorentz transformations, no velocity-addition formula.
The only calculation is t = d/c.

Target: Manim Community Edition 0.20.1
Final render:
    manim -pqh physics9_simple_relative_time_v1.py Physics9SimpleRelativeTimeV1 \
        --format=mp4 --disable_caching
"""
from __future__ import annotations

import os
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
# Visual system — intentionally aligned with the clean Physics 9 worksheet look
# -----------------------------------------------------------------------------
INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D8D8D8"
PAPER = "#F5F5F5"
AMBER = "#D6A000"   # light only

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_FAST = 0.55
RUN = 0.90
RUN_SLOW = 1.35
PAUSE_SHORT = 0.8
PAUSE_READ = 1.6
PAUSE_EXPLAIN = 2.4
PAUSE_SOLVE = 4.5
PAUSE_FINAL = 4.0


class Physics9SimpleRelativeTimeV1(Scene):
    """Simple light-clock problem for Grade 9 intuition."""

    C = 3.0e8
    ANA_PATH = 6.0
    CARLOS_PATH = 10.0
    ANA_TIME_NS = 20.0
    CARLOS_TIME_NS = 100.0 / 3.0

    # ------------------------------------------------------------------
    # Timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography / layout
    # ------------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=INK):
        return Text(content, font_size=size, weight=weight, color=color)

    def math(self, tex, size=40, color=INK):
        return MathTex(tex, font_size=size, color=color)

    def fit(self, mob, max_w=14.2, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        nbox = RoundedRectangle(
            width=0.56, height=0.56, corner_radius=0.08,
            stroke_color=INK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        ntext = self.txt(f"{number:02d}", 18, BOLD).move_to(nbox)
        title_m = self.fit(self.txt(title, 32, BOLD), 12.6, 0.58)
        row = VGroup(VGroup(nbox, ntext), title_m).arrange(RIGHT, buff=0.16)
        row.to_edge(LEFT, buff=0.42).to_edge(UP, buff=0.20)
        sub = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 14.4, 0.42)
        sub.next_to(row, DOWN, buff=0.08).align_to(row, LEFT)
        rule = Line(LEFT * 7.2, RIGHT * 7.2, color=LIGHT, stroke_width=2)
        rule.next_to(sub, DOWN, buff=0.10)
        return VGroup(row, sub, rule)

    def card(self, title, lines, width=5.8, height=None, title_size=24, body_size=21, fill=WHITE):
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size, NORMAL, DARK) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        if height is None:
            height = max(1.25, content.height + 0.58)
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.7,
            fill_color=fill, fill_opacity=1,
        )
        self.fit(content, width - 0.50, height - 0.30)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        return VGroup(box, content)

    def formula_box(self, tex, width=5.8, height=1.05, size=40, fill=PAPER, color=INK):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.8,
            fill_color=fill, fill_opacity=1,
        )
        eq = self.math(tex, size, color=color)
        self.fit(eq, width - 0.45, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    # ------------------------------------------------------------------
    # Simple pictograms
    # ------------------------------------------------------------------
    def person(self, scale=1.0):
        head = Circle(radius=0.16 * scale, stroke_color=INK, stroke_width=2.2,
                      fill_color=WHITE, fill_opacity=1).shift(UP * 0.68 * scale)
        torso = Line(UP * 0.48 * scale, DOWN * 0.08 * scale, color=INK, stroke_width=4.5)
        arm1 = Line(UP * 0.28 * scale, LEFT * 0.23 * scale + UP * 0.02 * scale, color=INK, stroke_width=3.5)
        arm2 = Line(UP * 0.28 * scale, RIGHT * 0.23 * scale + UP * 0.02 * scale, color=INK, stroke_width=3.5)
        leg1 = Line(DOWN * 0.08 * scale, LEFT * 0.18 * scale + DOWN * 0.54 * scale, color=INK, stroke_width=4.5)
        leg2 = Line(DOWN * 0.08 * scale, RIGHT * 0.18 * scale + DOWN * 0.54 * scale, color=INK, stroke_width=4.5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def bus_cabin(self, width=4.6, height=3.4):
        body = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=INK, stroke_width=2.3,
            fill_color=WHITE, fill_opacity=1,
        )
        floor = Line(body.get_left() + RIGHT * 0.35 + DOWN * 1.15,
                     body.get_right() + LEFT * 0.35 + DOWN * 1.15,
                     color=LIGHT, stroke_width=2)
        roof = Line(body.get_left() + RIGHT * 0.35 + UP * 1.15,
                    body.get_right() + LEFT * 0.35 + UP * 1.15,
                    color=LIGHT, stroke_width=2)
        wheel1 = Circle(radius=0.16, stroke_color=INK, fill_color=WHITE, fill_opacity=1)
        wheel2 = wheel1.copy()
        wheel1.move_to(body.get_center() + LEFT * 1.25 + DOWN * (height / 2 + 0.12))
        wheel2.move_to(body.get_center() + RIGHT * 1.25 + DOWN * (height / 2 + 0.12))
        return VGroup(body, floor, roof, wheel1, wheel2)

    def light_clock_inside(self, center=ORIGIN, height=2.4):
        bottom = center + DOWN * height / 2
        top = center + UP * height / 2
        mirror_bottom = Line(LEFT * 0.38, RIGHT * 0.38, color=INK, stroke_width=5).move_to(bottom)
        mirror_top = Line(LEFT * 0.38, RIGHT * 0.38, color=INK, stroke_width=5).move_to(top)
        guide = DashedLine(bottom, top, color=LIGHT, stroke_width=2)
        return VGroup(mirror_bottom, mirror_top, guide), bottom, top

    # ------------------------------------------------------------------
    # Scientific checks
    # ------------------------------------------------------------------
    def validate(self):
        assert abs(self.ANA_PATH / self.C - 20e-9) < 1e-15
        assert abs(self.CARLOS_PATH / self.C - (100.0 / 3.0) * 1e-9) < 1e-15
        assert self.CARLOS_PATH > self.ANA_PATH
        assert self.CARLOS_TIME_NS > self.ANA_TIME_NS

    # ------------------------------------------------------------------
    # Main sequence
    # ------------------------------------------------------------------
    def construct(self):
        self.validate()
        self.opening()
        self.problem()
        self.ana_view()
        self.carlos_view()
        self.compare_times()
        self.logic_check()
        self.exit_question()

    # ------------------------------------------------------------------
    # 00 — Opening
    # ------------------------------------------------------------------
    def opening(self):
        kicker = self.txt("PHYSICS 9  •  SPECIAL RELATIVITY", 23, BOLD, DARK)
        title = self.fit(self.txt("WHY CAN TWO OBSERVERS MEASURE DIFFERENT TIMES?", 43, BOLD), 13.8)
        subtitle = self.txt("Same light. Same speed. Different path.", 27, NORMAL, DARK)
        top = VGroup(kicker, title, subtitle).arrange(DOWN, buff=0.16).shift(UP * 2.55)

        bus = self.bus_cabin(5.3, 3.15).shift(LEFT * 1.20 + DOWN * 0.42)
        clock, bottom, top_p = self.light_clock_inside(bus.get_center() + RIGHT * 0.75, 2.10)
        ana = self.person(0.72).move_to(bus.get_center() + LEFT * 1.15 + DOWN * 0.18)
        carlos = self.person(0.72).move_to(RIGHT * 5.25 + DOWN * 0.58)
        lab_a = self.txt("ANA", 20, BOLD).next_to(ana, DOWN, buff=0.08)
        lab_c = self.txt("CARLOS", 20, BOLD).next_to(carlos, DOWN, buff=0.08)
        pulse = Dot(bottom, radius=0.09, color=AMBER)
        road = Line(LEFT * 7.1 + DOWN * 2.25, RIGHT * 7.1 + DOWN * 2.25, color=MID, stroke_width=2)

        self.play(Write(top), run_time=RUN_SLOW)
        self.play(Create(road), FadeIn(bus), FadeIn(clock), FadeIn(ana), FadeIn(carlos), FadeIn(lab_a), FadeIn(lab_c), run_time=RUN)
        self.play(MoveAlongPath(pulse, Line(bottom, top_p)), run_time=RUN_SLOW)
        self.play(MoveAlongPath(pulse, Line(top_p, bottom)), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 01 — Problem statement
    # ------------------------------------------------------------------
    def problem(self):
        h = self.header(
            1,
            "THE BASIC PROBLEM",
            "Use only one idea: every inertial observer measures the same speed of light c.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        givens = self.card(
            "GIVEN",
            [
                "Ana rides inside a very fast bus.",
                "Carlos watches the same light clock from the road.",
                "The light leaves the floor, reaches the roof, and returns.",
                "Both observers measure c = 3.0 × 10⁸ m/s.",
            ],
            width=6.5,
            body_size=21,
        ).move_to(LEFT * 3.75 + UP * 0.45)

        paths = self.card(
            "WHAT THEY SEE",
            [
                "Ana: total light path = 6 m.",
                "Carlos: total light path = 10 m.",
                "Same light. Same speed c.",
            ],
            width=5.8,
            body_size=23,
            fill=PAPER,
        ).move_to(RIGHT * 3.75 + UP * 0.55)

        question = self.card(
            "YOUR TASK",
            [
                "How much time does Ana measure?",
                "How much time does Carlos measure?",
                "Are the two times equal?",
            ],
            width=12.4,
            title_size=26,
            body_size=24,
        ).move_to(DOWN * 2.10)
        stop = self.txt("STOP THE VIDEO AND SOLVE WITH  t = distance / speed", 24, BOLD, DARK)
        stop.next_to(question, DOWN, buff=0.26)

        self.play(FadeIn(givens), FadeIn(paths), run_time=RUN)
        self.play(FadeIn(question), FadeIn(stop), run_time=RUN)
        self.wait(PAUSE_SOLVE)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 02 — Ana's frame
    # ------------------------------------------------------------------
    def ana_view(self):
        h = self.header(
            2,
            "ANA IS INSIDE THE BUS",
            "For Ana the light clock is at rest, so the light travels straight up and straight down.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus_cabin(5.1, 3.45).move_to(LEFT * 3.3 + DOWN * 0.35)
        clock, bottom, top_p = self.light_clock_inside(bus.get_center() + RIGHT * 0.70, 2.40)
        ana = self.person(0.73).move_to(bus.get_center() + LEFT * 1.15 + DOWN * 0.18)
        ana_lab = self.txt("ANA", 20, BOLD).next_to(ana, DOWN, buff=0.08)
        height_lab = self.txt("3 m", 22, BOLD, DARK).next_to(clock, RIGHT, buff=0.20)
        pulse = Dot(bottom, radius=0.09, color=AMBER)
        up_line = Line(bottom, top_p, color=AMBER, stroke_width=5)
        down_line = Line(top_p, bottom, color=AMBER, stroke_width=5)

        steps = VGroup(
            self.card("PATH", ["3 m up + 3 m down = 6 m"], width=6.0, body_size=23, fill=PAPER),
            self.formula_box(r"t_A=\frac{6\,\mathrm{m}}{3.0\times10^8\,\mathrm{m/s}}", width=6.0, size=35),
            self.formula_box(r"t_A=2.0\times10^{-8}\,\mathrm{s}=20\,\mathrm{ns}", width=6.0, size=34, fill=WHITE),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.6 + DOWN * 0.35)

        self.play(FadeIn(bus), FadeIn(clock), FadeIn(ana), FadeIn(ana_lab), FadeIn(height_lab), run_time=RUN)
        self.play(Create(up_line), MoveAlongPath(pulse, Line(bottom, top_p)), run_time=RUN_SLOW)
        self.play(Create(down_line), MoveAlongPath(pulse, Line(top_p, bottom)), run_time=RUN_SLOW)
        for item in steps:
            self.play(FadeIn(item, shift=UP * 0.05), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 03 — Carlos's frame
    # ------------------------------------------------------------------
    def carlos_view(self):
        h = self.header(
            3,
            "CARLOS IS ON THE ROAD",
            "The bus moves while the light is in flight, so Carlos sees a longer diagonal path.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        # 3-4-5 geometry in screen units: vertical 2.4, horizontal 3.2.
        y_bottom = -1.25
        y_top = 1.15
        p0 = LEFT * 3.2 + UP * y_bottom
        p1 = UP * y_top
        p2 = RIGHT * 3.2 + UP * y_bottom

        cabin = self.bus_cabin(4.25, 3.15).move_to(LEFT * 3.2 + DOWN * 0.05)
        mirror_bottom = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(p0)
        mirror_top = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(LEFT * 3.2 + UP * y_top)
        clock_parts = VGroup(mirror_bottom, mirror_top)
        cabin_group = VGroup(cabin, clock_parts)

        carlos = self.person(0.66).move_to(LEFT * 6.10 + DOWN * 1.40)
        c_lab = self.txt("CARLOS", 19, BOLD).next_to(carlos, DOWN, buff=0.08)
        pulse = Dot(p0, radius=0.10, color=AMBER)
        leg1 = Line(p0, p1, color=AMBER, stroke_width=5)
        leg2 = Line(p1, p2, color=AMBER, stroke_width=5)
        faint1 = DashedLine(p0, p1, color=LIGHT, stroke_width=2)
        faint2 = DashedLine(p1, p2, color=LIGHT, stroke_width=2)

        tri_v = Line(p0, LEFT * 3.2 + UP * y_top, color=MID, stroke_width=2)
        tri_h = Line(LEFT * 3.2 + UP * y_top, p1, color=MID, stroke_width=2)
        lab3 = self.txt("3 m", 20, BOLD, DARK).next_to(tri_v, LEFT, buff=0.12)
        lab4 = self.txt("4 m", 20, BOLD, DARK).next_to(tri_h, UP, buff=0.10)
        lab5 = self.txt("5 m", 20, BOLD, AMBER).move_to((p0 + p1) / 2 + RIGHT * 0.30)

        calculation = VGroup(
            self.card("CARLOS'S PATH", ["5 m out + 5 m back = 10 m"], width=5.65, body_size=22, fill=PAPER),
            self.formula_box(r"t_C=\frac{10\,\mathrm{m}}{3.0\times10^8\,\mathrm{m/s}}", width=5.65, size=34),
            self.formula_box(r"t_C=3.33\times10^{-8}\,\mathrm{s}=33.3\,\mathrm{ns}", width=5.65, size=32, fill=WHITE),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.25 + DOWN * 0.40)

        self.play(FadeIn(carlos), FadeIn(c_lab), FadeIn(cabin_group), FadeIn(pulse), run_time=RUN)
        self.play(Create(tri_v), Create(tri_h), FadeIn(lab3), FadeIn(lab4), FadeIn(lab5), run_time=RUN)
        self.wait(PAUSE_READ)

        self.add(faint1, faint2)
        self.play(cabin_group.animate.shift(RIGHT * 3.2), MoveAlongPath(pulse, Line(p0, p1)), Create(leg1), run_time=RUN_SLOW * 1.4)
        self.play(cabin_group.animate.shift(RIGHT * 3.2), MoveAlongPath(pulse, Line(p1, p2)), Create(leg2), run_time=RUN_SLOW * 1.4)
        self.wait(PAUSE_SHORT)

        for item in calculation:
            self.play(FadeIn(item, shift=UP * 0.05), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 04 — Compare
    # ------------------------------------------------------------------
    def compare_times(self):
        h = self.header(
            4,
            "COMPARE THE TWO MEASUREMENTS",
            "Nothing happened to the speed of light: both observers still use the same c.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        ana = self.card(
            "ANA • BUS FRAME",
            ["light path = 6 m", "light speed = c", "time = 20 ns"],
            width=5.8, body_size=24,
        ).move_to(LEFT * 3.45 + UP * 0.65)
        carlos = self.card(
            "CARLOS • ROAD FRAME",
            ["light path = 10 m", "light speed = c", "time = 33.3 ns"],
            width=5.8, body_size=24,
        ).move_to(RIGHT * 3.45 + UP * 0.65)

        same_c = self.formula_box(r"c_A=c_C=3.0\times10^8\,\mathrm{m/s}", width=8.0, size=36, fill=PAPER)
        same_c.move_to(DOWN * 1.45)
        result = self.card(
            "RESULT",
            ["Same light speed + different path  →  different measured time.",
             "The time interval depends on the observer's reference frame."],
            width=12.4, body_size=24,
        ).move_to(DOWN * 2.90)

        self.play(FadeIn(ana), FadeIn(carlos), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(same_c), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_FINAL)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 05 — Logic check
    # ------------------------------------------------------------------
    def logic_check(self):
        h = self.header(
            5,
            "THE LOGIC THAT MATTERS",
            "If the path is longer but light must keep the same speed, what quantity has to change?",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        row = VGroup(
            self.card("1", ["Carlos sees a longer path."], width=3.75, body_size=22),
            self.card("2", ["But he must still measure c."], width=3.75, body_size=22),
            self.card("3", ["So he must measure more time."], width=3.75, body_size=22, fill=PAPER),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 1.00)

        wrong = self.formula_box(r"\text{longer path} \Rightarrow \text{faster light}", width=7.1, size=32, fill=WHITE)
        wrong.move_to(DOWN * 0.65)
        strike = Line(wrong.get_left() + RIGHT * 0.28 + DOWN * 0.24,
                      wrong.get_right() + LEFT * 0.28 + UP * 0.24,
                      color=INK, stroke_width=4)
        correct = self.formula_box(r"\text{longer path} + \text{same }c \Rightarrow \text{more time}", width=9.6, size=31, fill=PAPER)
        correct.move_to(DOWN * 2.05)
        takeaway = self.txt("THIS is the first intuition behind time dilation.", 27, BOLD, DARK)
        takeaway.next_to(correct, DOWN, buff=0.25)

        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.05) for x in row], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(wrong), run_time=RUN)
        self.play(Create(strike), run_time=RUN_FAST)
        self.wait(PAUSE_SHORT)
        self.play(FadeIn(correct), FadeIn(takeaway), run_time=RUN)
        self.wait(PAUSE_FINAL)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 06 — Exit question
    # ------------------------------------------------------------------
    def exit_question(self):
        h = self.header(
            6,
            "EXIT QUESTION",
            "Do not use a relativity formula. Use only distance, speed, and the fact that c is the same.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        q = self.card(
            "NEW CASE",
            [
                "Ana sees a 6 m round trip for the light.",
                "Carlos sees a 12 m round trip for the same light.",
                "Both measure the same light speed c.",
                "Who measures more time? Why?",
            ],
            width=10.8,
            title_size=27,
            body_size=25,
            fill=WHITE,
        ).move_to(UP * 0.55)

        hint = self.formula_box(r"t=\frac{d}{c}", width=4.0, size=43, fill=PAPER)
        hint.next_to(q, DOWN, buff=0.35)
        close = self.txt("Explain the answer in one sentence before calculating anything.", 24, BOLD, DARK)
        close.next_to(hint, DOWN, buff=0.28)

        self.play(FadeIn(q), run_time=RUN)
        self.play(FadeIn(hint), FadeIn(close), run_time=RUN)
        self.wait(PAUSE_FINAL + 2.0)


# Preview:
#   manim -pql physics9_simple_relative_time_v1.py Physics9SimpleRelativeTimeV1 --disable_caching
# Final:
#   manim -pqh physics9_simple_relative_time_v1.py Physics9SimpleRelativeTimeV1 --disable_caching
