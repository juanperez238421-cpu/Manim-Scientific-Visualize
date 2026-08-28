#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Einstein Train & Lightning Thought Experiment
V6: relativity of simultaneity using X = X0 + vt, explicit calculations,
animated train/light propagation, and a spacetime diagram.

Render:
    manim -pqh physics9_einstein_train_lightning_v6.py Physics9EinsteinTrainLightningV6 \
        --format=mp4 --disable_caching
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

# ---------------------------------------------------------------------
# Render contract
# ---------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

# ---------------------------------------------------------------------
# Visual system
# ---------------------------------------------------------------------
INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D9D9D9"
PAPER = "#F5F5F5"
AMBER = "#D6A000"
AMBER_SOFT = "#E8C95A"
BLUE_GREY = "#5E6B73"

RUN_FAST = 0.55
RUN = 0.95
RUN_SLOW = 1.35
PAUSE = 1.10
PAUSE_READ = 1.90
PAUSE_COPY = 2.70


class Physics9EinsteinTrainLightningV6(Scene):
    """Projector-safe 2D lesson on Einstein's train/lightning thought experiment."""

    C = 3.00e8             # m/s
    C_US = 300.0           # m per microsecond
    BETA = 0.60            # v/c
    V_US = BETA * C_US     # 180 m/us
    A = 150.0              # strike positions are x = +/-150 m in ground frame
    GAMMA = 1.25

    T_PLATFORM = 0.5000    # us, both flashes reach x=0
    T_FRONT = 0.3125       # us, front flash reaches moving train midpoint
    T_REAR = 1.2500        # us, rear flash reaches moving train midpoint
    X_FRONT_MEET = 56.25   # m
    X_REAR_MEET = 225.0    # m
    TP_FRONT = -0.375      # us, front strike time in train frame
    TP_REAR = 0.375        # us, rear strike time in train frame

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs and kwargs["run_time"] is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -----------------------------------------------------------------
    # Typography and layout helpers
    # -----------------------------------------------------------------
    def txt(self, s, size=30, weight=NORMAL, color=INK):
        return Text(s, font_size=size, weight=weight, color=color)

    def mtex(self, s, size=40, color=INK):
        return MathTex(s, font_size=size, color=color)

    def fit(self, mob, max_w=14.0, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        kicker = self.txt(f"PHYSICS 9  •  SPECIAL RELATIVITY  •  {number:02d}", 19, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.0, 0.62)
        sub_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 13.8, 0.42)
        stack = VGroup(kicker, title_m, sub_m).arrange(DOWN, buff=0.07)
        stack.to_edge(UP, buff=0.18)
        rule = Line(LEFT * 7.10, RIGHT * 7.10, color=LIGHT, stroke_width=2)
        rule.next_to(stack, DOWN, buff=0.09)
        return VGroup(stack, rule)

    def formula_box(self, tex, width=6.0, height=1.00, size=40, fill=PAPER):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.7,
            fill_color=fill, fill_opacity=1.0,
        )
        eq = self.mtex(tex, size)
        self.fit(eq, width - 0.42, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def text_box(self, text, width=5.5, height=0.86, size=25, weight=BOLD, fill=WHITE):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=DARK, stroke_width=1.8,
            fill_color=fill, fill_opacity=1.0,
        )
        t = self.fit(self.txt(text, size, weight), width - 0.38, height - 0.18)
        t.move_to(box)
        return VGroup(box, t)

    def clear_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # Geometry helpers
    # -----------------------------------------------------------------
    def train_shell(self, width=8.0, height=2.0):
        body = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=INK, stroke_width=2.3,
            fill_color=WHITE, fill_opacity=1.0,
        )
        windows = VGroup()
        for frac in (-0.34, -0.17, 0.0, 0.17, 0.34):
            w = RoundedRectangle(
                width=min(1.05, width / 7.5), height=0.48,
                corner_radius=0.06, stroke_color=LIGHT, stroke_width=1.2,
                fill_color=PAPER, fill_opacity=1.0,
            )
            w.move_to(body.get_center() + RIGHT * frac * width + UP * 0.45)
            windows.add(w)
        floor = Line(
            body.get_left() + RIGHT * 0.30 + DOWN * 0.55,
            body.get_right() + LEFT * 0.30 + DOWN * 0.55,
            color=LIGHT, stroke_width=2,
        )
        wheels = VGroup()
        for xf in (-0.27, 0.27):
            wh = Circle(radius=0.16, stroke_color=INK, stroke_width=2,
                        fill_color=WHITE, fill_opacity=1)
            wh.move_to(body.get_center() + RIGHT * width * xf + DOWN * (height / 2 + 0.16))
            wheels.add(wh)
        return VGroup(body, windows, floor, wheels)

    def person(self, scale=1.0, seated=False):
        head = Circle(radius=0.17 * scale, stroke_color=INK, stroke_width=2.4,
                      fill_color=WHITE, fill_opacity=1)
        if seated:
            head.move_to(UP * 0.70 * scale)
            torso = Line(UP * 0.50 * scale, UP * 0.05 * scale, color=INK, stroke_width=5)
            thigh = Line(UP * 0.05 * scale, RIGHT * 0.30 * scale + DOWN * 0.08 * scale,
                         color=INK, stroke_width=5)
            shin = Line(RIGHT * 0.30 * scale + DOWN * 0.08 * scale,
                        RIGHT * 0.30 * scale + DOWN * 0.48 * scale,
                        color=INK, stroke_width=5)
            arm = Line(UP * 0.34 * scale, RIGHT * 0.25 * scale + UP * 0.15 * scale,
                       color=INK, stroke_width=4)
            return VGroup(head, torso, thigh, shin, arm)
        head.move_to(UP * 0.70 * scale)
        torso = Line(UP * 0.50 * scale, DOWN * 0.08 * scale, color=INK, stroke_width=5)
        arms = VGroup(
            Line(UP * 0.30 * scale, LEFT * 0.24 * scale + UP * 0.04 * scale, color=INK, stroke_width=4),
            Line(UP * 0.30 * scale, RIGHT * 0.24 * scale + UP * 0.04 * scale, color=INK, stroke_width=4),
        )
        legs = VGroup(
            Line(DOWN * 0.08 * scale, LEFT * 0.18 * scale + DOWN * 0.56 * scale, color=INK, stroke_width=5),
            Line(DOWN * 0.08 * scale, RIGHT * 0.18 * scale + DOWN * 0.56 * scale, color=INK, stroke_width=5),
        )
        return VGroup(head, torso, arms, legs)

    def lightning(self, x, y=2.0, scale=1.0):
        pts = [
            np.array([0.00, 0.95, 0]), np.array([-0.18, 0.28, 0]),
            np.array([0.02, 0.28, 0]), np.array([-0.12, -0.20, 0]),
            np.array([0.18, -0.20, 0]), np.array([0.02, -0.95, 0]),
            np.array([0.45, -0.08, 0]), np.array([0.18, -0.08, 0]),
            np.array([0.34, 0.40, 0]), np.array([0.10, 0.40, 0]),
        ]
        p = Polygon(*[q * scale for q in pts], stroke_color=AMBER,
                    fill_color=AMBER_SOFT, fill_opacity=0.95, stroke_width=2)
        p.move_to(np.array([x, y, 0.0]))
        return p

    def pulse(self, center):
        core = Dot(center, radius=0.09, color=AMBER)
        ring = Circle(radius=0.22, stroke_color=AMBER_SOFT, stroke_width=2).move_to(center)
        return VGroup(core, ring)

    def scale_x(self, x_m):
        return x_m * (4.0 / self.A)

    # -----------------------------------------------------------------
    # Sequence
    # -----------------------------------------------------------------
    def construct(self):
        # Fail-fast numerical checks.
        assert abs(self.BETA * self.C_US - self.V_US) < 1e-12
        assert abs(self.A / self.C_US - self.T_PLATFORM) < 1e-12
        assert abs(self.A / (self.C_US + self.V_US) - self.T_FRONT) < 1e-12
        assert abs(self.A / (self.C_US - self.V_US) - self.T_REAR) < 1e-12
        assert abs(self.V_US * self.T_FRONT - self.X_FRONT_MEET) < 1e-12
        assert abs(self.V_US * self.T_REAR - self.X_REAR_MEET) < 1e-12
        assert abs(1 / np.sqrt(1 - self.BETA**2) - self.GAMMA) < 1e-12
        assert abs(self.GAMMA * (-self.BETA * self.A / self.C_US) - self.TP_FRONT) < 1e-12
        assert abs(self.GAMMA * (+self.BETA * self.A / self.C_US) - self.TP_REAR) < 1e-12

        self.opening()
        self.setup_events()
        self.general_motion_equation()
        self.platform_observer()
        self.train_observer_animation()
        self.solve_front_reception()
        self.solve_rear_reception()
        self.spacetime_diagram()
        self.lorentz_confirmation()
        self.final_summary()

    # -----------------------------------------------------------------
    # 00 opening
    # -----------------------------------------------------------------
    def opening(self):
        title = VGroup(
            self.txt("PHYSICS 9 • SPECIAL RELATIVITY", 22, BOLD, DARK),
            self.fit(self.txt("EINSTEIN'S TRAIN AND LIGHTNING", 46, BOLD), 13.6),
            self.txt("A step-by-step calculation of relative simultaneity", 27, NORMAL, DARK),
        ).arrange(DOWN, buff=0.16).shift(UP * 2.45)

        rail = Line(LEFT * 7.1 + DOWN * 1.78, RIGHT * 7.1 + DOWN * 1.78, color=MID, stroke_width=2)
        train = self.train_shell(8.0, 1.95).shift(DOWN * 0.55)
        observer = self.person(0.70, seated=True).move_to(train.get_center() + DOWN * 0.02)
        platform_obs = self.person(0.58).move_to(DOWN * 2.55)
        left_bolt = self.lightning(-4.0, 1.55, 0.72)
        right_bolt = self.lightning(4.0, 1.55, 0.72)

        self.play(Write(title), run_time=RUN_SLOW)
        self.play(Create(rail), FadeIn(train), FadeIn(observer), FadeIn(platform_obs), run_time=RUN)
        self.play(FadeIn(left_bolt, scale=1.35), FadeIn(right_bolt, scale=1.35), run_time=0.35)
        self.play(Indicate(left_bolt, color=AMBER), Indicate(right_bolt, color=AMBER), run_time=0.75)
        question = self.text_box("Do both observers agree that the lightning strikes were simultaneous?", 10.8, 0.90, 26)
        question.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(question, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_all()

    # -----------------------------------------------------------------
    # 01 setup
    # -----------------------------------------------------------------
    def setup_events(self):
        h = self.header(1, "DEFINE THE EVENTS IN THE PLATFORM FRAME", "At t = 0, two lightning strikes occur simultaneously at x = -150 m and x = +150 m.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        axis = NumberLine(x_range=[-180, 180, 60], length=11.2, include_numbers=True,
                          color=MID, stroke_width=2).shift(DOWN * 0.35)
        left_mark = Dot(axis.n2p(-150), color=AMBER, radius=0.09)
        right_mark = Dot(axis.n2p(150), color=AMBER, radius=0.09)
        center = Dot(axis.n2p(0), color=INK, radius=0.08)
        l1 = self.txt("REAR STRIKE", 22, BOLD).next_to(left_mark, UP, buff=0.35)
        l2 = self.txt("FRONT STRIKE", 22, BOLD).next_to(right_mark, UP, buff=0.35)
        c0 = self.txt("x = 0", 20, BOLD).next_to(center, DOWN, buff=0.20)

        given = VGroup(
            self.formula_box(r"x_R(0)=-150\,\mathrm{m}", 4.5, 0.90, 34),
            self.formula_box(r"x_F(0)=+150\,\mathrm{m}", 4.5, 0.90, 34),
            self.formula_box(r"v_{\mathrm{train}}=0.60c", 4.5, 0.90, 34),
        ).arrange(RIGHT, buff=0.22).shift(DOWN * 2.10)

        self.play(Create(axis), FadeIn(left_mark), FadeIn(right_mark), FadeIn(center), run_time=RUN)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(c0), run_time=RUN)
        self.play(*[FadeIn(g, shift=UP * 0.08) for g in given], run_time=RUN_SLOW)
        note = self.txt("All positions and times on this screen belong to the PLATFORM / GROUND frame.", 22, BOLD, DARK)
        note.to_edge(DOWN, buff=0.18)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 02 X = X0 + vt
    # -----------------------------------------------------------------
    def general_motion_equation(self):
        h = self.header(2, "ONE GENERAL EQUATION DESCRIBES EVERY WORLDLINE", "Use X = X0 + vt for the train observer and for each light pulse.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        master = self.formula_box(r"\boxed{X=X_0+vt}", 5.0, 1.10, 50, WHITE).shift(UP * 1.65)
        self.play(FadeIn(master, scale=0.96), run_time=RUN)

        rows = VGroup(
            self.formula_box(r"x_T(t)=0+(0.60c)t", 6.2, 0.88, 36),
            self.formula_box(r"x_F(t)=150-ct", 6.2, 0.88, 36),
            self.formula_box(r"x_R(t)=-150+ct", 6.2, 0.88, 36),
            self.formula_box(r"x_P(t)=0", 6.2, 0.88, 36),
        ).arrange(DOWN, buff=0.16).move_to(LEFT * 2.35 + DOWN * 0.65)

        labels = VGroup(
            self.txt("TRAIN MIDPOINT OBSERVER", 21, BOLD),
            self.txt("FRONT FLASH MOVES LEFT", 21, BOLD),
            self.txt("REAR FLASH MOVES RIGHT", 21, BOLD),
            self.txt("PLATFORM OBSERVER", 21, BOLD),
        )
        for lab, row in zip(labels, rows):
            lab.next_to(row, RIGHT, buff=0.30)
            self.fit(lab, 5.0)

        for row, lab in zip(rows, labels):
            self.play(FadeIn(row, shift=RIGHT * 0.08), FadeIn(lab), run_time=0.62)

        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 03 platform observer
    # -----------------------------------------------------------------
    def platform_observer(self):
        h = self.header(3, "PLATFORM OBSERVER: THE FLASHES ARRIVE TOGETHER", "The observer is fixed at x = 0 and is equally distant from both strike positions.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        rail = Line(LEFT * 7.1 + DOWN * 1.55, RIGHT * 7.1 + DOWN * 1.55, color=MID, stroke_width=2)
        train = self.train_shell(8.0, 1.80).shift(DOWN * 0.50)
        pobs = self.person(0.58).move_to(DOWN * 2.35)
        plab = self.txt("PLATFORM OBSERVER", 20, BOLD).next_to(pobs, DOWN, buff=0.08)
        lb = self.lightning(-4.0, 1.40, 0.68)
        rb = self.lightning(4.0, 1.40, 0.68)
        lp = self.pulse(np.array([-4.0, -0.10, 0.0]))
        rp = self.pulse(np.array([4.0, -0.10, 0.0]))
        t = ValueTracker(0.0)
        badge = always_redraw(lambda: self.formula_box(
            rf"t={t.get_value():.3f}\,\mu\mathrm{{s}}", 3.3, 0.78, 31, WHITE
        ).move_to(RIGHT * 5.2 + UP * 1.65))

        self.play(Create(rail), FadeIn(train), FadeIn(pobs), FadeIn(plab), run_time=RUN)
        self.play(FadeIn(lb), FadeIn(rb), FadeIn(lp), FadeIn(rp), FadeIn(badge), run_time=0.55)
        self.play(
            train.animate.shift(RIGHT * 2.40),
            lp.animate.move_to(np.array([0.0, -0.10, 0.0])),
            rp.animate.move_to(np.array([0.0, -0.10, 0.0])),
            t.animate.set_value(self.T_PLATFORM),
            run_time=3.8,
            rate_func=linear,
        )
        arrive = self.text_box("BOTH LIGHT PULSES REACH x = 0 AT THE SAME TIME", 9.0, 0.88, 24)
        arrive.move_to(UP * 1.25)
        calc = self.formula_box(r"0=150-ct\quad\Rightarrow\quad t=0.500\,\mu\mathrm{s}", 7.5, 0.92, 34).move_to(DOWN * 2.85)
        self.play(FadeIn(arrive, shift=UP * 0.08), FadeIn(calc, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 04 moving train observer
    # -----------------------------------------------------------------
    def train_observer_animation(self):
        h = self.header(4, "TRAIN OBSERVER: MOVE TOWARD ONE FLASH, AWAY FROM THE OTHER", "The train midpoint moves right at 0.60c while both light pulses still move at c.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        rail = Line(LEFT * 7.1 + DOWN * 1.75, RIGHT * 7.1 + DOWN * 1.75, color=MID, stroke_width=2)
        train = self.train_shell(8.0, 1.88).shift(DOWN * 0.62)
        obs = self.person(0.68, seated=True).move_to(np.array([0.0, -0.62, 0.0]))
        obs_lab = self.txt("TRAIN MIDPOINT", 20, BOLD).next_to(obs, DOWN, buff=0.06)
        lp = self.pulse(np.array([-4.0, -0.20, 0.0]))
        rp = self.pulse(np.array([4.0, -0.20, 0.0]))
        t = ValueTracker(0.0)
        badge = always_redraw(lambda: self.formula_box(
            rf"t={t.get_value():.4f}\,\mu\mathrm{{s}}", 3.7, 0.78, 29, WHITE
        ).move_to(RIGHT * 5.1 + UP * 1.55))
        note = self.txt("Schematic motion; calculations below use the exact equations.", 19, NORMAL, DARK)
        note.to_edge(DOWN, buff=0.16)

        self.play(Create(rail), FadeIn(train), FadeIn(obs), FadeIn(obs_lab), FadeIn(lp), FadeIn(rp), FadeIn(badge), FadeIn(note), run_time=RUN)

        # Exact scaled positions at t = 0.3125 us: train midpoint = +56.25 m,
        # rear pulse = -56.25 m, front pulse = +56.25 m.
        first_x = self.scale_x(self.X_FRONT_MEET)
        rear_x_at_first = self.scale_x(-self.X_FRONT_MEET)
        self.play(
            train.animate.shift(RIGHT * first_x),
            obs.animate.shift(RIGHT * first_x),
            obs_lab.animate.shift(RIGHT * first_x),
            rp.animate.move_to(np.array([first_x, -0.20, 0.0])),
            lp.animate.move_to(np.array([rear_x_at_first, -0.20, 0.0])),
            t.animate.set_value(self.T_FRONT),
            run_time=3.2,
            rate_func=linear,
        )
        front_first = self.text_box("FRONT FLASH REACHES THE TRAIN OBSERVER FIRST", 8.2, 0.86, 23)
        front_first.move_to(UP * 1.10)
        self.play(FadeIn(front_first), Indicate(rp, color=AMBER), run_time=RUN)
        self.wait(PAUSE)

        # Full train would leave the screen by the rear reception event. Keep the
        # observer/worldline marker and continue with exact ground-frame scaling.
        self.play(FadeOut(train), FadeOut(rp), FadeOut(front_first), run_time=RUN_FAST)
        final_x = self.scale_x(self.X_REAR_MEET)
        self.play(
            obs.animate.move_to(np.array([final_x, -0.62, 0.0])),
            obs_lab.animate.move_to(np.array([final_x, -1.38, 0.0])),
            lp.animate.move_to(np.array([final_x, -0.20, 0.0])),
            t.animate.set_value(self.T_REAR),
            run_time=4.0,
            rate_func=linear,
        )
        rear_later = self.text_box("REAR FLASH REACHES THE SAME OBSERVER LATER", 7.6, 0.86, 23)
        rear_later.move_to(UP * 1.10)
        self.play(FadeIn(rear_later), Indicate(lp, color=AMBER), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_all()

    # -----------------------------------------------------------------
    # 05 solve front
    # -----------------------------------------------------------------
    def solve_front_reception(self):
        h = self.header(5, "CALCULATION 1: WHEN DOES THE FRONT FLASH REACH THE TRAIN OBSERVER?", "Set the train position equal to the front-light position.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        master = self.formula_box(r"X=X_0+vt", 4.4, 0.92, 44).shift(UP * 1.65)
        rows = VGroup(
            self.formula_box(r"x_T(t)=0+(0.60c)t", 7.1, 0.88, 36),
            self.formula_box(r"x_F(t)=150-ct", 7.1, 0.88, 36),
            self.formula_box(r"0.60ct=150-ct", 7.1, 0.88, 38),
            self.formula_box(r"1.60ct=150", 7.1, 0.88, 38),
            self.formula_box(r"t_F=\frac{150}{1.60c}=0.3125\,\mu\mathrm{s}", 7.1, 0.96, 37, WHITE),
        ).arrange(DOWN, buff=0.14).shift(DOWN * 0.60)

        self.play(FadeIn(master), run_time=RUN)
        for r in rows:
            self.play(FadeIn(r, shift=UP * 0.06), run_time=0.62)
        result = self.text_box("FRONT RECEPTION: 0.3125 μs", 5.8, 0.86, 26)
        result.to_edge(DOWN, buff=0.20)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 06 solve rear
    # -----------------------------------------------------------------
    def solve_rear_reception(self):
        h = self.header(6, "CALCULATION 2: WHEN DOES THE REAR FLASH REACH THE TRAIN OBSERVER?", "Now set the train position equal to the rear-light position.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        master = self.formula_box(r"X=X_0+vt", 4.4, 0.92, 44).shift(UP * 1.65)
        rows = VGroup(
            self.formula_box(r"x_T(t)=0+(0.60c)t", 7.1, 0.88, 36),
            self.formula_box(r"x_R(t)=-150+ct", 7.1, 0.88, 36),
            self.formula_box(r"0.60ct=-150+ct", 7.1, 0.88, 38),
            self.formula_box(r"0.40ct=150", 7.1, 0.88, 38),
            self.formula_box(r"t_R=\frac{150}{0.40c}=1.250\,\mu\mathrm{s}", 7.1, 0.96, 37, WHITE),
        ).arrange(DOWN, buff=0.14).shift(DOWN * 0.60)

        self.play(FadeIn(master), run_time=RUN)
        for r in rows:
            self.play(FadeIn(r, shift=UP * 0.06), run_time=0.62)
        result = self.text_box("REAR RECEPTION: 1.250 μs", 5.8, 0.86, 26)
        result.to_edge(DOWN, buff=0.20)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 07 spacetime diagram
    # -----------------------------------------------------------------
    def spacetime_diagram(self):
        h = self.header(7, "THE SAME CALCULATION AS A SPACETIME DIAGRAM", "Intersections of worldlines are reception events: same physics, visualized geometrically.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        axes = Axes(
            x_range=[-180, 240, 60], y_range=[0, 1.35, 0.25],
            x_length=11.3, y_length=4.6,
            axis_config={"color": MID, "stroke_width": 2, "include_tip": True},
            x_axis_config={"numbers_to_include": [-150, 0, 150]},
            y_axis_config={"numbers_to_include": [0.5, 1.0, 1.25]},
        ).shift(DOWN * 0.55)
        xlab = self.mtex(r"x\ (\mathrm{m})", 27).next_to(axes.x_axis, RIGHT, buff=0.14)
        tlab = self.mtex(r"t\ (\mu\mathrm{s})", 27).next_to(axes.y_axis, UP, buff=0.10)

        train_line = ParametricFunction(
            lambda tau: axes.c2p(self.V_US * tau, tau),
            t_range=[0, self.T_REAR], color=INK, stroke_width=4,
        )
        front_line = ParametricFunction(
            lambda tau: axes.c2p(self.A - self.C_US * tau, tau),
            t_range=[0, self.T_PLATFORM], color=AMBER, stroke_width=4,
        )
        rear_line = ParametricFunction(
            lambda tau: axes.c2p(-self.A + self.C_US * tau, tau),
            t_range=[0, self.T_REAR], color=AMBER_SOFT, stroke_width=4,
        )
        platform_line = Line(axes.c2p(0, 0), axes.c2p(0, 1.30), color=BLUE_GREY, stroke_width=3)

        self.play(Create(axes), FadeIn(xlab), FadeIn(tlab), run_time=RUN)
        self.play(Create(platform_line), run_time=RUN)
        self.play(Create(train_line), run_time=RUN_SLOW)
        self.play(Create(front_line), Create(rear_line), run_time=RUN_SLOW)

        p_platform = Dot(axes.c2p(0, self.T_PLATFORM), color=BLUE_GREY, radius=0.08)
        p_front = Dot(axes.c2p(self.X_FRONT_MEET, self.T_FRONT), color=AMBER, radius=0.09)
        p_rear = Dot(axes.c2p(self.X_REAR_MEET, self.T_REAR), color=AMBER, radius=0.09)

        l_platform = self.txt("platform: both at 0.500 μs", 19, BOLD, BLUE_GREY).next_to(p_platform, LEFT, buff=0.20)
        l_front = self.txt("train: front 0.3125 μs", 19, BOLD).next_to(p_front, RIGHT, buff=0.18)
        l_rear = self.txt("train: rear 1.250 μs", 19, BOLD).next_to(p_rear, LEFT, buff=0.18)
        self.fit(l_platform, 4.0)
        self.fit(l_front, 4.0)
        self.fit(l_rear, 4.0)

        self.play(FadeIn(p_platform), FadeIn(l_platform), run_time=RUN)
        self.play(FadeIn(p_front), FadeIn(l_front), run_time=RUN)
        self.play(FadeIn(p_rear), FadeIn(l_rear), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 08 Lorentz confirmation
    # -----------------------------------------------------------------
    def lorentz_confirmation(self):
        h = self.header(8, "RECEPTION TIMES DIFFER — DO THE LIGHTNING EVENTS THEMSELVES?", "Use the Lorentz time transformation to compare the strike events in the train frame.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        gamma = self.formula_box(r"\gamma=\frac{1}{\sqrt{1-0.60^2}}=1.25", 6.2, 0.95, 39).shift(UP * 1.62)
        transform = self.formula_box(r"t'=\gamma\left(t-\frac{vx}{c^2}\right)", 6.2, 0.95, 42).shift(UP * 0.47)
        self.play(FadeIn(gamma), FadeIn(transform), run_time=RUN)

        front = self.formula_box(
            r"t'_F=1.25\left(0-\frac{(0.60c)(150)}{c^2}\right)=-0.375\,\mu\mathrm{s}",
            11.7, 0.95, 33, WHITE,
        ).shift(DOWN * 0.75)
        rear = self.formula_box(
            r"t'_R=1.25\left(0-\frac{(0.60c)(-150)}{c^2}\right)=+0.375\,\mu\mathrm{s}",
            11.7, 0.95, 33, WHITE,
        ).shift(DOWN * 1.90)
        self.play(FadeIn(front, shift=UP * 0.06), run_time=RUN)
        self.play(FadeIn(rear, shift=UP * 0.06), run_time=RUN)

        result = self.text_box("TRAIN FRAME: FRONT STRIKE OCCURS 0.750 μs BEFORE REAR STRIKE", 10.4, 0.90, 24)
        result.to_edge(DOWN, buff=0.18)
        self.play(FadeIn(result, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    # -----------------------------------------------------------------
    # 09 final summary
    # -----------------------------------------------------------------
    def final_summary(self):
        h = self.header(9, "RELATIVITY OF SIMULTANEITY", "The two observers agree on the physical events but disagree about whether the strikes are simultaneous.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        left = RoundedRectangle(width=6.4, height=3.8, corner_radius=0.15,
                                stroke_color=DARK, stroke_width=2, fill_color=WHITE, fill_opacity=1).shift(LEFT * 3.4 + DOWN * 0.25)
        right = left.copy().shift(RIGHT * 6.8)
        lt = self.txt("PLATFORM FRAME", 28, BOLD).move_to(left.get_top() + DOWN * 0.42)
        rt = self.txt("TRAIN FRAME", 28, BOLD).move_to(right.get_top() + DOWN * 0.42)

        l1 = self.formula_box(r"t_R=t_F=0", 4.8, 0.82, 35).move_to(left.get_center() + UP * 0.55)
        l2 = self.formula_box(r"t_{\mathrm{arrival}}=0.500\,\mu\mathrm{s}", 4.8, 0.82, 33).move_to(left.get_center() + DOWN * 0.55)
        l3 = self.txt("The strikes are simultaneous.", 23, BOLD).move_to(left.get_center() + DOWN * 1.35)

        r1 = self.formula_box(r"t'_F=-0.375\,\mu\mathrm{s}", 4.8, 0.82, 33).move_to(right.get_center() + UP * 0.70)
        r2 = self.formula_box(r"t'_R=+0.375\,\mu\mathrm{s}", 4.8, 0.82, 33).move_to(right.get_center() + DOWN * 0.30)
        r3 = self.txt("The front strike happens first.", 23, BOLD).move_to(right.get_center() + DOWN * 1.35)

        self.play(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=RUN)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=RUN)
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=RUN)

        bridge = self.fit(self.txt("SIMULTANEITY IS NOT ABSOLUTE: it depends on the observer's inertial frame.", 31, BOLD), 13.5)
        bridge.to_edge(DOWN, buff=0.28)
        self.play(Write(bridge), run_time=RUN_SLOW)
        self.wait(PAUSE_COPY)
        self.clear_all()
