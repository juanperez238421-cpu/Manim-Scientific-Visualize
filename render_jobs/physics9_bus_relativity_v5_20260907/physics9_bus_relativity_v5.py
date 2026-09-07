#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Relative Motion to Special Relativity
V5 consolidated bus lesson, 100% 2D and 100% English.

Pedagogical design
------------------
This version deliberately uses one everyday situation from beginning to end:
a bus, a passenger walking inside it, and an observer standing on the road.
The narrative follows the simple public-explanation pattern often used by
Javier Santaolalla: begin with familiar velocity addition, then ask what
changes when the moving object is light, and only then introduce Einstein's
velocity-addition rule.

Core sequence
-------------
1. Two observers / two reference frames.
2. Ordinary motion: 20 m/s bus + 2 m/s walker = 22 m/s from the road.
3. Confirm the same idea with X = X0 + vt over 3 s.
4. Replace the walker with a light pulse: both observers measure c.
5. Maxwell -> Einstein historical bridge in one screen.
6. Relativistic velocity addition and u'=c => u=c.
7. Show why everyday motion still looks Galilean.
8. Close with one reproducible conceptual map.

Final render:
    manim -pqh physics9_bus_relativity_v5.py Physics9BusRelativityV5 \
        --format=mp4 --disable_caching

Compatible target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import os
import math
import numpy as np
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
# VISUAL SYSTEM
# =============================================================================
INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D8D8D8"
PAPER = "#F5F5F5"
AMBER = "#D6A000"   # reserved for light only
WHITE_FILL = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_FAST = 0.65
RUN = 1.00
RUN_SLOW = 1.35
PAUSE_SHORT = 0.85
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.65
PAUSE_COPY = 3.40
PAUSE_FINAL = 4.30


class Physics9BusRelativityV5(Scene):
    """Projector-safe introduction from ordinary relative motion to invariant c."""

    V_BUS = 20.0
    V_WALK = 2.0
    V_GROUND = 22.0
    T_OBS = 3.0
    C = 3.00e8

    # -------------------------------------------------------------------------
    # Global timing wrappers
    # -------------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Typography and layout helpers
    # -------------------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=INK):
        return Text(content, font_size=size, weight=weight, color=color)

    def mathtex(self, expression, size=40, color=INK):
        return MathTex(expression, font_size=size, color=color)

    def fit(self, mob, max_w=14.2, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        kicker = self.txt(f"PHYSICS 9  •  RELATIVE MOTION  •  {number:02d}", 19, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.0, 0.60)
        sub_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 14.0, 0.42)
        group = VGroup(kicker, title_m, sub_m).arrange(DOWN, buff=0.07)
        group.to_edge(UP, buff=0.18)
        rule = Line(LEFT * 7.20, RIGHT * 7.20, color=LIGHT, stroke_width=2)
        rule.next_to(group, DOWN, buff=0.09)
        return VGroup(group, rule)

    def formula_box(self, tex, width=6.0, height=1.00, size=39, color=INK):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=DARK,
            stroke_width=1.8,
            fill_color=PAPER,
            fill_opacity=1.0,
        )
        eq = self.mathtex(tex, size, color=color)
        self.fit(eq, width - 0.45, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    def text_box(self, text, width=5.4, height=0.88, size=26, bold=True, stroke=DARK):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=stroke,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        label = self.fit(self.txt(text, size, BOLD if bold else NORMAL), width - 0.42, height - 0.20)
        label.move_to(box)
        return VGroup(box, label)

    def note_box(self, title, lines, width=5.8, title_size=24, body_size=22):
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.58, 3.5)
        box = RoundedRectangle(
            width=width,
            height=max(1.2, content.height + 0.60),
            corner_radius=0.10,
            stroke_color=DARK,
            stroke_width=1.7,
            fill_color=WHITE,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.29)
        return VGroup(box, content)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    # -------------------------------------------------------------------------
    # Reusable pictograms
    # -------------------------------------------------------------------------
    def person(self, scale=1.0, walking=False, seated=False):
        head = Circle(
            radius=0.18 * scale,
            stroke_color=INK,
            stroke_width=2.4,
            fill_color=WHITE,
            fill_opacity=1,
        ).shift(UP * 0.72 * scale)

        if seated:
            torso = Line(UP * 0.50 * scale, UP * 0.02 * scale, color=INK, stroke_width=5)
            arm = Line(UP * 0.32 * scale, RIGHT * 0.25 * scale + UP * 0.17 * scale, color=INK, stroke_width=4)
            thigh = Line(UP * 0.02 * scale, RIGHT * 0.32 * scale + DOWN * 0.10 * scale, color=INK, stroke_width=5)
            shin = Line(RIGHT * 0.32 * scale + DOWN * 0.10 * scale,
                        RIGHT * 0.32 * scale + DOWN * 0.50 * scale, color=INK, stroke_width=5)
            return VGroup(head, torso, arm, thigh, shin)

        torso = Line(UP * 0.52 * scale, DOWN * 0.10 * scale, color=INK, stroke_width=5)
        if walking:
            arm1 = Line(UP * 0.30 * scale, LEFT * 0.28 * scale + UP * 0.08 * scale, color=INK, stroke_width=4)
            arm2 = Line(UP * 0.28 * scale, RIGHT * 0.30 * scale + DOWN * 0.02 * scale, color=INK, stroke_width=4)
            leg1 = Line(DOWN * 0.10 * scale, LEFT * 0.29 * scale + DOWN * 0.58 * scale, color=INK, stroke_width=5)
            leg2 = Line(DOWN * 0.10 * scale, RIGHT * 0.30 * scale + DOWN * 0.48 * scale, color=INK, stroke_width=5)
        else:
            arm1 = Line(UP * 0.30 * scale, LEFT * 0.23 * scale + UP * 0.03 * scale, color=INK, stroke_width=4)
            arm2 = Line(UP * 0.30 * scale, RIGHT * 0.23 * scale + UP * 0.03 * scale, color=INK, stroke_width=4)
            leg1 = Line(DOWN * 0.10 * scale, LEFT * 0.18 * scale + DOWN * 0.58 * scale, color=INK, stroke_width=5)
            leg2 = Line(DOWN * 0.10 * scale, RIGHT * 0.18 * scale + DOWN * 0.58 * scale, color=INK, stroke_width=5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def bus(self, width=8.2, height=2.3):
        body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.20,
            stroke_color=INK,
            stroke_width=2.5,
            fill_color=WHITE,
            fill_opacity=1,
        )
        windows = VGroup()
        for frac in (-0.30, -0.10, 0.10, 0.30):
            w = RoundedRectangle(
                width=min(1.24, width / 5.9),
                height=0.68,
                corner_radius=0.07,
                stroke_color=LIGHT,
                stroke_width=1.4,
                fill_color=PAPER,
                fill_opacity=1,
            )
            w.move_to(body.get_center() + RIGHT * (frac * width) + UP * 0.52)
            windows.add(w)
        floor = Line(
            body.get_left() + RIGHT * 0.35 + DOWN * 0.70,
            body.get_right() + LEFT * 0.35 + DOWN * 0.70,
            color=LIGHT,
            stroke_width=2,
        )
        wheels = VGroup(
            Circle(radius=0.17, stroke_color=INK, fill_color=WHITE, fill_opacity=1),
            Circle(radius=0.17, stroke_color=INK, fill_color=WHITE, fill_opacity=1),
        )
        wheels[0].move_to(body.get_center() + LEFT * (width * 0.28) + DOWN * (height / 2 + 0.13))
        wheels[1].move_to(body.get_center() + RIGHT * (width * 0.28) + DOWN * (height / 2 + 0.13))
        return VGroup(body, windows, floor, wheels)

    def velocity_arrow(self, start, end, label, color=INK, size=27):
        arrow = Arrow(start, end, buff=0, stroke_width=4, color=color,
                      max_tip_length_to_length_ratio=0.13)
        lab = self.mathtex(label, size, color=color).next_to(arrow, UP, buff=0.10)
        return VGroup(arrow, lab)

    def observer_badge(self, text, center, width=3.4):
        box = RoundedRectangle(width=width, height=0.64, corner_radius=0.09,
                               stroke_color=DARK, stroke_width=1.6,
                               fill_color=WHITE, fill_opacity=1)
        label = self.fit(self.txt(text, 20, BOLD), width - 0.35, 0.38).move_to(box)
        return VGroup(box, label).move_to(center)

    def light_pulse(self, start, end):
        beam = Arrow(start, end, buff=0, stroke_width=7, color=AMBER,
                     max_tip_length_to_length_ratio=0.12)
        glow = Line(start, end, color=AMBER, stroke_width=13).set_opacity(0.18)
        return VGroup(glow, beam)

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    def validate_data(self):
        assert math.isclose(self.V_BUS + self.V_WALK, self.V_GROUND, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(self.V_BUS * self.T_OBS, 60.0, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(self.V_GROUND * self.T_OBS, 66.0, rel_tol=0, abs_tol=1e-12)
        assert math.isclose((self.V_GROUND - self.V_BUS) * self.T_OBS, 6.0, rel_tol=0, abs_tol=1e-12)
        correction = self.V_WALK * self.V_BUS / self.C**2
        assert correction < 5e-16
        relativistic_light = (self.C + self.V_BUS) / (1 + self.C * self.V_BUS / self.C**2)
        assert math.isclose(relativistic_light, self.C, rel_tol=1e-15)

    # -------------------------------------------------------------------------
    # Orchestration
    # -------------------------------------------------------------------------
    def construct(self):
        self.validate_data()
        self.opening()
        self.reference_frames()
        self.ordinary_velocity_addition()
        self.position_check()
        self.replace_with_light()
        self.maxwell_to_einstein()
        self.relativistic_velocity_addition()
        self.everyday_limit()
        self.summary()

    # -------------------------------------------------------------------------
    # 00 — Opening
    # -------------------------------------------------------------------------
    def opening(self):
        top = VGroup(
            self.txt("PHYSICS 9 • SPECIAL RELATIVITY", 23, BOLD, DARK),
            self.fit(self.txt("ONE BUS. TWO OBSERVERS. ONE SURPRISE.", 45, BOLD), 13.6),
            self.txt("Start with ordinary motion. Then replace the walker with light.", 26, NORMAL, DARK),
        ).arrange(DOWN, buff=0.16).shift(UP * 2.60)

        bus = self.bus(8.7, 2.25).shift(LEFT * 1.45 + DOWN * 0.45)
        walker = self.person(0.86, walking=True).move_to(bus.get_center() + RIGHT * 0.55 + DOWN * 0.03)
        road_obs = self.person(0.72).move_to(RIGHT * 5.05 + DOWN * 0.52)
        road = Line(LEFT * 7.20 + DOWN * 2.03, RIGHT * 7.20 + DOWN * 2.03, color=MID, stroke_width=2)
        obs_lab = self.txt("ROAD OBSERVER", 20, BOLD).next_to(road_obs, DOWN, buff=0.10)
        bus_arrow = self.velocity_arrow(LEFT * 4.6 + DOWN * 2.58,
                                        LEFT * 1.5 + DOWN * 2.58,
                                        r"20\,\mathrm{m/s}")

        self.play(Write(top), run_time=RUN_SLOW)
        self.play(Create(road), FadeIn(bus), FadeIn(walker), FadeIn(road_obs), FadeIn(obs_lab), run_time=RUN)
        self.play(GrowArrow(bus_arrow[0]), Write(bus_arrow[1]), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 01 — Frames
    # -------------------------------------------------------------------------
    def reference_frames(self):
        h = self.header(1, "FIRST QUESTION: WHO IS MEASURING?",
                        "Velocity is not a property of the object alone; it is measured relative to a frame.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus(8.0, 2.35).move_to(LEFT * 2.25 + DOWN * 0.25)
        seated = self.person(0.83, seated=True).move_to(bus.get_center() + LEFT * 2.20 + DOWN * 0.02)
        walker = self.person(0.84, walking=True).move_to(bus.get_center() + RIGHT * 0.45 + DOWN * 0.02)
        outside = self.person(0.70).move_to(RIGHT * 5.05 + DOWN * 0.20)
        ground = Line(RIGHT * 3.75 + DOWN * 1.05, RIGHT * 6.30 + DOWN * 1.05, color=MID, stroke_width=2)

        in_badge = self.observer_badge("FRAME S' — INSIDE BUS", LEFT * 2.25 + DOWN * 2.55, 3.8)
        out_badge = self.observer_badge("FRAME S — ROAD", RIGHT * 5.05 + DOWN * 1.65, 3.2)
        question = self.text_box("Same walker. Different measurements.", width=5.0, height=0.86, size=24)
        question.move_to(RIGHT * 4.60 + UP * 1.45)

        self.play(FadeIn(bus), FadeIn(seated), FadeIn(walker), FadeIn(outside), Create(ground), run_time=RUN)
        self.play(FadeIn(in_badge), FadeIn(out_badge), FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 02 — Classical addition
    # -------------------------------------------------------------------------
    def ordinary_velocity_addition(self):
        h = self.header(2, "ORDINARY MOTION: VELOCITIES ADD",
                        "The passenger inside measures the walker relative to the bus; the road observer includes the bus motion too.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        divider = Line(UP * 2.35, DOWN * 3.45, color=LIGHT, stroke_width=2)
        self.play(Create(divider), run_time=RUN_FAST)

        # Left: inside frame
        left_title = self.txt("INSIDE THE BUS", 25, BOLD).move_to(LEFT * 3.95 + UP * 2.05)
        mini_bus_l = self.bus(5.4, 1.75).move_to(LEFT * 3.90 + DOWN * 0.05)
        walker_l = self.person(0.66, walking=True).move_to(mini_bus_l.get_center() + RIGHT * 0.55 + DOWN * 0.03)
        arr_l = self.velocity_arrow(LEFT * 5.55 + DOWN * 1.55, LEFT * 3.45 + DOWN * 1.55,
                                    r"v'=2\,\mathrm{m/s}")
        res_l = self.text_box("Passenger measures: 2 m/s", width=5.2, height=0.78, size=23)
        res_l.move_to(LEFT * 3.95 + DOWN * 2.65)

        # Right: road frame
        right_title = self.txt("FROM THE ROAD", 25, BOLD).move_to(RIGHT * 3.95 + UP * 2.05)
        eq1 = self.formula_box(r"v_{\mathrm{ground}}=v_{\mathrm{bus}}+v'", width=6.0, height=1.00, size=36)
        eq1.move_to(RIGHT * 3.90 + UP * 0.75)
        eq2 = self.formula_box(r"v_{\mathrm{ground}}=20+2=22\,\mathrm{m/s}", width=6.0, height=1.00, size=36)
        eq2.move_to(RIGHT * 3.90 + DOWN * 0.60)
        res_r = self.text_box("Road observer measures: 22 m/s", width=5.4, height=0.82, size=24)
        res_r.move_to(RIGHT * 3.90 + DOWN * 2.05)

        self.play(FadeIn(left_title), FadeIn(mini_bus_l), FadeIn(walker_l), FadeIn(right_title), run_time=RUN)
        self.play(GrowArrow(arr_l[0]), Write(arr_l[1]), FadeIn(res_l), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq1), run_time=RUN)
        self.play(FadeIn(eq2), FadeIn(res_r), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 03 — Position check
    # -------------------------------------------------------------------------
    def position_check(self):
        h = self.header(3, "CHECK IT WITH POSITION: X = X0 + vt",
                        "After the same 3 s interval, the road observer can compare how far the bus and walker moved.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        master = self.formula_box(r"X=X_0+vt", width=4.2, height=0.95, size=45)
        master.move_to(UP * 1.90)
        self.play(FadeIn(master), run_time=RUN)

        left = VGroup(
            self.txt("BUS", 24, BOLD),
            self.formula_box(r"X_{\mathrm{bus}}=0+(20)(3)=60\,\mathrm{m}", width=6.2, height=1.00, size=35),
        ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.70 + DOWN * 0.15)

        right = VGroup(
            self.txt("WALKER FROM ROAD", 24, BOLD),
            self.formula_box(r"X_{\mathrm{walker}}=0+(22)(3)=66\,\mathrm{m}", width=6.2, height=1.00, size=34),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.70 + DOWN * 0.15)

        gap = self.formula_box(r"\Delta X=66-60=6\,\mathrm{m}", width=5.0, height=1.00, size=39)
        gap.move_to(DOWN * 2.15)
        note = self.txt("Inside the bus: (2 m/s)(3 s) = 6 m — same relative displacement.", 23, NORMAL, DARK)
        note.move_to(DOWN * 3.05)

        self.play(FadeIn(left), run_time=RUN)
        self.play(FadeIn(right), run_time=RUN)
        self.play(FadeIn(gap), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(Write(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 04 — Replace walker with light
    # -------------------------------------------------------------------------
    def replace_with_light(self):
        h = self.header(4, "NOW REPLACE THE WALKER WITH LIGHT",
                        "If ordinary velocities add, should the road observer measure c + 20 m/s?")
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus(8.0, 2.25).move_to(LEFT * 2.25 + DOWN * 0.15)
        passenger = self.person(0.82, seated=True).move_to(bus.get_center() + LEFT * 2.15 + DOWN * 0.01)
        lamp = Dot(radius=0.10, color=AMBER).move_to(bus.get_center() + LEFT * 0.70 + UP * 0.15)
        beam = self.light_pulse(lamp.get_center() + RIGHT * 0.08, bus.get_right() + RIGHT * 0.95 + UP * 0.15)
        observer = self.person(0.68).move_to(RIGHT * 5.25 + DOWN * 0.20)
        ground = Line(RIGHT * 4.00 + DOWN * 1.02, RIGHT * 6.45 + DOWN * 1.02, color=MID, stroke_width=2)

        inside = self.text_box("Passenger measures light: c", width=4.7, height=0.82, size=23)
        inside.move_to(LEFT * 2.25 + DOWN * 2.25)
        naive = self.formula_box(r"c+20\,\mathrm{m/s}\ ?", width=4.3, height=0.95, size=39)
        naive.move_to(RIGHT * 4.85 + UP * 1.15)
        cross1 = Line(naive.get_corner(UL) + DOWN * 0.08, naive.get_corner(DR) + UP * 0.08, color=DARK, stroke_width=4)
        cross2 = Line(naive.get_corner(DL) + UP * 0.08, naive.get_corner(UR) + DOWN * 0.08, color=DARK, stroke_width=4)
        correct = self.text_box("Road observer also measures: c", width=5.0, height=0.88, size=24, stroke=AMBER)
        correct.move_to(RIGHT * 4.85 + DOWN * 0.65)

        self.play(FadeIn(bus), FadeIn(passenger), FadeIn(lamp), FadeIn(observer), Create(ground), run_time=RUN)
        self.play(FadeIn(inside), run_time=RUN)
        self.play(FadeIn(naive), run_time=RUN)
        self.wait(PAUSE_SHORT)
        self.play(Create(cross1), Create(cross2), run_time=RUN_FAST)
        self.play(FadeIn(beam), FadeIn(correct), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 05 — Historical bridge
    # -------------------------------------------------------------------------
    def maxwell_to_einstein(self):
        h = self.header(5, "THE HISTORICAL BRIDGE: MAXWELL TO EINSTEIN",
                        "The puzzle was not that motion is relative; the puzzle was that light keeps the same speed for inertial observers.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        line = Line(LEFT * 5.5, RIGHT * 5.5, color=MID, stroke_width=3).move_to(DOWN * 0.15)
        m_dot = Dot(line.point_from_proportion(0.22), radius=0.10, color=INK)
        e_dot = Dot(line.point_from_proportion(0.78), radius=0.10, color=INK)
        self.play(Create(line), FadeIn(m_dot), FadeIn(e_dot), run_time=RUN)

        maxwell = self.note_box(
            "MAXWELL — ELECTROMAGNETISM",
            [
                "Electromagnetic waves propagate at a fixed speed c.",
                "Light is an electromagnetic wave.",
            ], width=5.8, title_size=23, body_size=21,
        ).move_to(LEFT * 3.45 + UP * 1.05)

        einstein = self.note_box(
            "EINSTEIN — 1905",
            [
                "Keep the relativity principle.",
                "Keep c the same for every inertial observer.",
            ], width=5.8, title_size=23, body_size=21,
        ).move_to(RIGHT * 3.45 + UP * 1.05)

        consequence = self.text_box("Then space and time cannot both remain absolute.", width=7.2, height=0.92, size=26)
        consequence.move_to(DOWN * 2.10)

        self.play(FadeIn(maxwell), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(einstein), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(consequence), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 06 — Relativistic velocity addition
    # -------------------------------------------------------------------------
    def relativistic_velocity_addition(self):
        h = self.header(6, "RELATIVISTIC VELOCITY ADDITION",
                        "Einstein's rule agrees with ordinary addition at low speeds and automatically keeps light at c.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        general = self.formula_box(
            r"u=\frac{u'+v}{1+\frac{u'v}{c^2}}",
            width=6.1, height=1.15, size=45,
        ).move_to(UP * 1.85)
        labels = self.txt("u' = speed measured inside the bus    •    v = bus speed    •    u = speed measured from the road",
                          21, NORMAL, DARK)
        self.fit(labels, 13.7, 0.42)
        labels.next_to(general, DOWN, buff=0.18)

        self.play(FadeIn(general), Write(labels), run_time=RUN)
        self.wait(PAUSE_READ)

        step1 = self.formula_box(
            r"u'=c\quad\Rightarrow\quad u=\frac{c+v}{1+\frac{cv}{c^2}}",
            width=8.5, height=1.05, size=39,
        ).move_to(DOWN * 0.15)
        step2 = self.formula_box(
            r"u=\frac{c+v}{1+v/c}=\frac{c(c+v)}{c+v}=c",
            width=8.5, height=1.05, size=39,
        ).move_to(DOWN * 1.55)
        final = self.text_box("LIGHT: both inertial observers measure c", width=6.9, height=0.88, size=25, stroke=AMBER)
        final.move_to(DOWN * 2.90)

        self.play(FadeIn(step1), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(step2), run_time=RUN)
        self.play(FadeIn(final), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 07 — Everyday limit
    # -------------------------------------------------------------------------
    def everyday_limit(self):
        h = self.header(7, "WHY DO WE STILL USE 20 + 2 = 22?",
                        "Because ordinary classroom speeds are tiny compared with c, the relativistic correction is effectively invisible.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        correction = self.formula_box(
            r"\frac{u'v}{c^2}=\frac{(2)(20)}{(3.00\times10^8)^2}\approx4.44\times10^{-16}",
            width=9.2, height=1.10, size=38,
        ).move_to(UP * 1.55)
        approx = self.formula_box(
            r"1+\frac{u'v}{c^2}\approx1",
            width=5.6, height=1.00, size=42,
        ).move_to(DOWN * 0.05)
        result = self.formula_box(
            r"u\approx u'+v=2+20=22\,\mathrm{m/s}",
            width=7.3, height=1.05, size=41,
        ).move_to(DOWN * 1.55)
        note = self.text_box("Newton/Galileo is the excellent low-speed approximation.", width=7.6, height=0.86, size=25)
        note.move_to(DOWN * 2.95)

        self.play(FadeIn(correction), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(approx), run_time=RUN)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 08 — Summary
    # -------------------------------------------------------------------------
    def summary(self):
        h = self.header(8, "THE WHOLE IDEA IN THREE STEPS",
                        "Use this map whenever a relative-motion problem begins to look confusing.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        cards = VGroup()
        specs = [
            ("1", "CHOOSE THE FRAME", "Who is measuring?\nInside the bus or on the road?"),
            ("2", "ORDINARY OBJECTS", "At low speed:\n20 + 2 = 22 m/s"),
            ("3", "LIGHT", "Not c + v.\nEvery inertial observer measures c."),
        ]
        for number, title, body in specs:
            box = RoundedRectangle(width=4.35, height=3.25, corner_radius=0.14,
                                   stroke_color=DARK, stroke_width=2,
                                   fill_color=WHITE, fill_opacity=1)
            n = self.txt(number, 28, BOLD)
            circle = Circle(radius=0.31, stroke_color=DARK, stroke_width=2,
                            fill_color=PAPER, fill_opacity=1)
            n.move_to(circle)
            title_m = self.fit(self.txt(title, 23, BOLD), 3.65, 0.52)
            body_lines = body.split("\n")
            body_m = VGroup(*[self.txt(line, 21, NORMAL, DARK) for line in body_lines])
            body_m.arrange(DOWN, buff=0.10)
            content = VGroup(VGroup(circle, n), title_m, body_m).arrange(DOWN, buff=0.25)
            content.move_to(box)
            cards.add(VGroup(box, content))

        cards.arrange(RIGHT, buff=0.42).move_to(DOWN * 0.25)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.16), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_COPY)

        closing = self.text_box("Reference frame matters. The speed of light does not change with the observer.",
                                width=11.2, height=0.90, size=26, stroke=AMBER)
        closing.move_to(DOWN * 2.95)
        self.play(FadeIn(closing), run_time=RUN)
        self.wait(PAUSE_FINAL)
        self.clear_scene()
