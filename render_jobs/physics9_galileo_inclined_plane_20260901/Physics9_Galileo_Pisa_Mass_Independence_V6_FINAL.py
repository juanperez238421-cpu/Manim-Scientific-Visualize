#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V6 — Galileo inclined plane + Pisa mass-independence extension.

Direct continuation of the audited V5.9 classroom lesson. The new section adds
an explicit mass-independence investigation commonly associated with Galileo's
Leaning Tower of Pisa argument, while carefully distinguishing:

- gravitational force: F_g = mg (depends on mass),
- free-fall acceleration: a = g (independent of test mass in the ideal model),
- real-air effects: drag can make objects with different shapes fall differently.

The Pisa sequence is presented as a traditional Galileo account / conceptual
experiment, not as an unqualified historical claim that the famous tower drop
is independently documented exactly as often retold.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_9_POST_RENDER_QA import (
    Physics9UniformMotionGalileoV59PostRenderQA,
)


DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
RUN = 1.00
RUN_FAST = 0.70
RUN_SLOW = 1.35
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80


class Physics9GalileoPisaMassIndependenceV6Final(Physics9UniformMotionGalileoV59PostRenderQA):
    """Full lesson: motion graphs -> Galileo ramp -> falling motion -> Pisa test."""

    def validate_lesson_data(self):
        super().validate_lesson_data()
        g = 9.81
        h = 20.0
        t = math.sqrt(2.0 * h / g)
        vf = g * t
        assert abs(t - 2.0193) < 0.002
        assert abs(vf - 19.81) < 0.03
        for m in (1.0, 10.0):
            fg = m * g
            assert abs(fg / m - g) < 1e-12

    def construct(self):
        self.opening_v5()
        self.uniform_motion_two_graphs()
        self.derive_position_equation()
        self.graph_equation_connection()
        self.galileo_question_v5()
        self.galileo_real_apparatus_v5()
        self.galileo_equal_time_pattern_v5()
        self.galileo_deduction_v5()
        self.falling_equation_preview_v5()
        self.pisa_question()
        self.pisa_force_reasoning()
        self.pisa_numeric_drop()
        self.air_resistance_caveat()
        self.summary_v6()

    # ------------------------------------------------------------------
    # Pisa visual helpers
    # ------------------------------------------------------------------
    def _pisa_tower(self, center=LEFT * 4.35 + DOWN * 0.25, scale=1.0):
        """Stylized leaning-tower line art; no external asset required."""
        w = 1.55 * scale
        h = 4.55 * scale
        lean = 0.42 * scale
        c = np.array(center, dtype=float)
        bl = c + np.array([-w / 2, -h / 2, 0])
        br = c + np.array([w / 2, -h / 2, 0])
        tl = c + np.array([-w / 2 + lean, h / 2, 0])
        tr = c + np.array([w / 2 + lean, h / 2, 0])
        shell = Polygon(
            bl, br, tr, tl,
            stroke_color=BLACK,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        floors = VGroup()
        for frac in np.linspace(0.13, 0.88, 7):
            left = bl + frac * (tl - bl)
            right = br + frac * (tr - br)
            floors.add(Line(left, right, color=MID_GRAY, stroke_width=1.2))
        roof = Line(tl + LEFT * 0.08, tr + RIGHT * 0.08, color=BLACK, stroke_width=2.2)
        base = Line(bl + LEFT * 0.22, br + RIGHT * 0.22, color=BLACK, stroke_width=2.6)
        return VGroup(shell, floors, roof, base)

    def pisa_question(self):
        self.set_header(
            9,
            "GALILEO'S MASS QUESTION: DOES A HEAVIER OBJECT FALL FASTER?",
            "Traditional Pisa account: compare two compact objects released together from the same height.",
        )

        tower = self._pisa_tower()
        ground = Line(LEFT * 6.5 + DOWN * 2.65, RIGHT * 6.7 + DOWN * 2.65,
                      color=BLACK, stroke_width=2.4)
        history = self.note_panel(
            "HISTORICAL NOTE",
            [
                "The Leaning Tower story is traditionally associated with Galileo.",
                "Our purpose here is the physical test: same height, same release time.",
            ],
            width=6.6,
            title_size=22,
            body_size=18,
        ).move_to(RIGHT * 3.35 + UP * 1.65)

        p1 = np.array([-2.55, 1.40, 0])
        p2 = np.array([-1.55, 1.40, 0])
        small = Circle(radius=0.14, stroke_color=BLACK, stroke_width=2,
                       fill_color=WHITE, fill_opacity=1).move_to(p1)
        large = Circle(radius=0.25, stroke_color=BLACK, stroke_width=2.2,
                       fill_color=LIGHT_GRAY, fill_opacity=1).move_to(p2)
        labels = VGroup(
            self.math(r"m_1=1\,\mathrm{kg}", 24).next_to(small, UP, buff=0.17),
            self.math(r"m_2=10\,\mathrm{kg}", 24).next_to(large, UP, buff=0.17),
        )
        arrows = VGroup(
            Arrow(small.get_bottom(), small.get_bottom() + DOWN * 0.78, buff=0.05,
                  color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.16),
            Arrow(large.get_bottom(), large.get_bottom() + DOWN * 0.78, buff=0.05,
                  color=BLACK, stroke_width=2, max_tip_length_to_length_ratio=0.16),
        )
        glabs = VGroup(
            self.math(r"\vec g", 24).next_to(arrows[0], RIGHT, buff=0.10),
            self.math(r"\vec g", 24).next_to(arrows[1], RIGHT, buff=0.10),
        )
        question = self.formula_panel(
            r"\text{Prediction: }a_{1\,kg}\;?\;a_{10\,kg}",
            width=6.4,
            height=0.95,
            size=31,
        ).move_to(RIGHT * 3.35 + DOWN * 1.25)
        ideal = self.txt("IDEAL FREE FALL: ignore air resistance", 19, BOLD, color=DARK_GRAY)
        ideal.move_to(RIGHT * 3.35 + DOWN * 2.20)

        self.play(FadeIn(tower), Create(ground), run_time=RUN)
        self.play(FadeIn(small), FadeIn(large), FadeIn(labels), run_time=RUN)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(glabs), run_time=RUN)
        self.play(FadeIn(history), FadeIn(question), FadeIn(ideal), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def pisa_force_reasoning(self):
        self.set_header(
            10,
            "WHY MASS CANCELS IN IDEAL FREE FALL",
            "A heavier object feels more gravitational force, but it also has proportionally more inertia.",
        )

        left = self.panel(6.55, 4.75, fill=WHITE).move_to(LEFT * 3.65 + DOWN * 0.25)
        right = self.panel(6.55, 4.75, fill=WHITE).move_to(RIGHT * 3.65 + DOWN * 0.25)

        lt = self.txt("COMPARE FORCES", 23, BOLD).next_to(left.get_top(), DOWN, buff=0.24)
        force_rows = VGroup(
            self.formula_panel(r"m_1=1\,kg:\quad F_{g1}=m_1g=9.81\,N",
                               width=5.65, height=0.90, size=27),
            self.formula_panel(r"m_2=10\,kg:\quad F_{g2}=m_2g=98.1\,N",
                               width=5.65, height=0.90, size=27),
            self.txt("The 10 kg object has 10x the gravitational force.", 19, BOLD),
        ).arrange(DOWN, buff=0.28).move_to(left.get_center() + DOWN * 0.15)

        rt = self.txt("APPLY NEWTON'S SECOND LAW", 23, BOLD).next_to(right.get_top(), DOWN, buff=0.24)
        derivation = VGroup(
            self.math(r"F_{\mathrm{net}}=ma", 35),
            self.math(r"F_g=mg", 35),
            self.math(r"ma=mg", 39),
            self.math(r"\cancel{m}\,a=\cancel{m}\,g", 39),
            self.math(r"\boxed{a=g}", 46),
        ).arrange(DOWN, buff=0.24).move_to(right.get_center() + DOWN * 0.18)

        result = self.formula_panel(
            r"\boxed{a_{1\,kg}=a_{10\,kg}=g\approx9.81\,\mathrm{m/s^2}}",
            width=9.4,
            height=0.95,
            size=34,
        ).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=RUN)
        for item in force_rows:
            self.play(FadeIn(item), run_time=RUN_FAST)
        for item in derivation:
            self.play(FadeIn(item), run_time=RUN_FAST)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def pisa_numeric_drop(self):
        self.set_header(
            11,
            "SAME HEIGHT + SAME INITIAL VELOCITY -> SAME FALL TIME",
            "Numerical check from h = 20 m: both compact objects follow the same ideal free-fall kinematics.",
        )

        h = 20.0
        g = 9.81
        t_hit = math.sqrt(2 * h / g)
        vf = g * t_hit

        left = self.panel(7.0, 5.1, fill=WHITE).move_to(LEFT * 3.65 + DOWN * 0.12)
        right = self.panel(6.2, 5.1, fill=WHITE).move_to(RIGHT * 3.85 + DOWN * 0.12)

        top_y, bottom_y = 1.72, -1.78
        x1, x2 = -4.55, -2.75
        path1 = Line([x1, top_y, 0], [x1, bottom_y, 0], color=LIGHT_GRAY, stroke_width=2)
        path2 = Line([x2, top_y, 0], [x2, bottom_y, 0], color=LIGHT_GRAY, stroke_width=2)
        ground = Line([-5.65, bottom_y, 0], [-1.65, bottom_y, 0], color=BLACK, stroke_width=2.2)
        b1 = Circle(radius=0.14, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(path1.get_start())
        b2 = Circle(radius=0.24, color=BLACK, fill_color=LIGHT_GRAY, fill_opacity=1).move_to(path2.get_start())
        mlabels = VGroup(
            self.math(r"1\,kg", 22).next_to(b1, UP, buff=0.10),
            self.math(r"10\,kg", 22).next_to(b2, UP, buff=0.10),
        )
        height = DoubleArrow([-5.35, top_y, 0], [-5.35, bottom_y, 0], buff=0.03,
                             color=MID_GRAY, stroke_width=1.5,
                             max_tip_length_to_length_ratio=0.05)
        hlab = self.math(r"h=20\,m", 22).next_to(height, LEFT, buff=0.10)
        clock = self.math(r"t=0.00\,s", 28).move_to([-3.65, 2.18, 0])

        calc = VGroup(
            self.txt("IDEAL DROP FROM REST", 22, BOLD),
            self.math(r"h=\frac12gt^2", 36),
            self.math(r"t=\sqrt{\frac{2h}{g}}", 36),
            self.math(rf"t=\sqrt{{\frac{{2(20)}}{{9.81}}}}\approx{t_hit:.2f}\,s", 31),
            self.math(rf"v_f=gt\approx(9.81)({t_hit:.2f})\approx{vf:.1f}\,m/s", 30),
            self.formula_panel(r"\boxed{t_1=t_2\quad\text{and}\quad v_{f1}=v_{f2}}",
                               width=5.3, height=0.85, size=28),
        ).arrange(DOWN, buff=0.25).move_to(right.get_center())
        self.fit(calc, 5.55, 4.4)

        self.play(FadeIn(left), FadeIn(right), Create(path1), Create(path2), Create(ground), run_time=RUN)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(mlabels), GrowArrow(height), FadeIn(hlab), FadeIn(clock), run_time=RUN)
        self.play(FadeIn(calc), run_time=RUN)

        # Same normalized progress for both balls: visually identical acceleration history.
        tracker = ValueTracker(0.0)
        def y_of_alpha(alpha):
            return top_y + (bottom_y - top_y) * (alpha ** 2)
        b1.add_updater(lambda m: m.move_to([x1, y_of_alpha(tracker.get_value()), 0]))
        b2.add_updater(lambda m: m.move_to([x2, y_of_alpha(tracker.get_value()), 0]))
        clock.add_updater(lambda m: m.become(self.math(
            rf"t={t_hit * tracker.get_value():.2f}\,s", 28
        ).move_to([-3.65, 2.18, 0])))
        self.play(tracker.animate.set_value(1.0), run_time=2.7, rate_func=linear)
        b1.clear_updaters(); b2.clear_updaters(); clock.clear_updaters()

        impact = self.txt("SIMULTANEOUS IMPACT", 23, BOLD).move_to([-3.65, -2.24, 0])
        self.play(FadeIn(impact), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def air_resistance_caveat(self):
        self.set_header(
            12,
            "WHY A FEATHER AND A BALL CAN FALL DIFFERENTLY IN AIR",
            "Mass-independent g describes free fall; air resistance adds another force that depends strongly on shape and speed.",
        )

        left = self.panel(6.25, 4.55, fill=WHITE).move_to(LEFT * 3.55 + DOWN * 0.18)
        right = self.panel(6.25, 4.55, fill=WHITE).move_to(RIGHT * 3.55 + DOWN * 0.18)
        lt = self.txt("VACUUM / IDEAL MODEL", 22, BOLD).next_to(left.get_top(), DOWN, buff=0.25)
        rt = self.txt("AIR PRESENT", 22, BOLD).next_to(right.get_top(), DOWN, buff=0.25)

        ball_l = Circle(radius=0.24, color=BLACK, fill_color=LIGHT_GRAY, fill_opacity=1).move_to([-4.25, 0.75, 0])
        feather_l = self._simple_feather(np.array([-2.85, 0.75, 0]))
        same = self.formula_panel(r"a_{ball}=a_{feather}=g", width=5.1, height=0.85, size=29).move_to([-3.55, -1.15, 0])

        ball_r = Circle(radius=0.24, color=BLACK, fill_color=LIGHT_GRAY, fill_opacity=1).move_to([2.85, 0.55, 0])
        feather_r = self._simple_feather(np.array([4.25, 1.10, 0]))
        drag = VGroup(
            Arrow([4.25, 0.65, 0], [4.25, 1.75, 0], buff=0.05, color=MID_GRAY,
                  stroke_width=2, max_tip_length_to_length_ratio=0.12),
            self.math(r"F_{air}", 23).move_to([4.82, 1.32, 0]),
        )
        net = self.formula_panel(r"\vec F_{net}=m\vec g+\vec F_{air}", width=5.25, height=0.85, size=29).move_to([3.55, -1.15, 0])
        note = self.txt("Different arrival times in air do NOT mean different values of g.", 21, BOLD)
        self.fit(note, 12.8, 0.45)
        note.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=RUN)
        self.play(FadeIn(ball_l), FadeIn(feather_l), FadeIn(same), run_time=RUN)
        self.play(FadeIn(ball_r), FadeIn(feather_r), FadeIn(drag), FadeIn(net), run_time=RUN)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def _simple_feather(self, center):
        shaft = Line(center + DOWN * 0.55, center + UP * 0.55, color=BLACK, stroke_width=2)
        vanes = VGroup()
        for y, length in [(-0.28, 0.30), (-0.05, 0.42), (0.18, 0.38), (0.38, 0.25)]:
            p = center + UP * y
            vanes.add(Line(p, p + LEFT * length + UP * 0.14, color=BLACK, stroke_width=1.5))
            vanes.add(Line(p, p + RIGHT * length + UP * 0.14, color=BLACK, stroke_width=1.5))
        return VGroup(shaft, vanes)

    def summary_v6(self):
        self.set_header(
            13,
            "FROM GALILEO'S RAMP TO FREE FALL: ONE CONNECTED IDEA",
            "Use experiments to identify the motion pattern, then use equations to explain what the measurements mean.",
        )

        ramp = self.note_panel(
            "1 | INCLINED PLANE",
            [
                "Slow the motion so positions can be measured.",
                "Equal time steps reveal growing distances.",
                "The pattern points toward square-time motion.",
            ], width=4.45, title_size=22, body_size=18,
        )
        fall = self.note_panel(
            "2 | FREE FALL",
            [
                "Near Earth: acceleration is approximately constant.",
                "For an ideal release from rest: distance grows as t².",
                "g is the common gravitational acceleration.",
            ], width=4.45, title_size=22, body_size=18,
        )
        mass = self.note_panel(
            "3 | MASS TEST",
            [
                "Gravitational force is larger for larger mass.",
                "But F = ma gives ma = mg.",
                "Therefore the ideal free-fall acceleration is a = g.",
            ], width=4.45, title_size=22, body_size=18,
        )
        cards = VGroup(ramp, fall, mass).arrange(RIGHT, buff=0.28).move_to(UP * 0.30)
        self.fit(cards, 14.2, 4.6)

        final = self.formula_panel(
            r"\boxed{F_g=mg\quad\text{but}\quad a=g\;\text{(ideal free fall)}}",
            width=9.2, height=1.05, size=35,
        ).to_edge(DOWN, buff=0.45)
        takeaway = self.txt(
            "The mass changes the gravitational force — not the value of free-fall acceleration g.",
            24, BOLD,
        ).next_to(final, UP, buff=0.25)
        self.fit(takeaway, 13.5, 0.55)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.16), run_time=RUN_SLOW * 1.8)
        self.play(FadeIn(takeaway), FadeIn(final), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN)

        end = VGroup(
            self.txt("PHYSICS 9 | GALILEO", 27, BOLD),
            self.txt("OBSERVE -> MEASURE -> MODEL -> EXPLAIN", 42, BOLD),
            self.math(r"a=g\quad\text{for ideal free fall}", 38),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeIn(end, shift=UP * 0.12), run_time=RUN_SLOW)
        self.wait(3.6)
        self.play(FadeOut(end), run_time=RUN)


# Preview:
# manim -pql Physics9_Galileo_Pisa_Mass_Independence_V6_FINAL.py Physics9GalileoPisaMassIndependenceV6Final --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Pisa_Mass_Independence_V6_FINAL.py Physics9GalileoPisaMassIndependenceV6Final --disable_caching
