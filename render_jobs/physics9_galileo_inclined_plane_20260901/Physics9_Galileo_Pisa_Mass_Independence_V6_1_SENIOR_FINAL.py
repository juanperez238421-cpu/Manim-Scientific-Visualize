#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6.1 senior runtime refinement.

Replaces the V6 dynamic MathTex clock with a DecimalNumber-based live timer so
no LaTeX compilation occurs inside a frame updater. All V6 content is retained.
"""
from __future__ import annotations

import math
from manim import *

from Physics9_Galileo_Pisa_Mass_Independence_V6_FINAL import (
    Physics9GalileoPisaMassIndependenceV6Final,
    LIGHT_GRAY,
    MID_GRAY,
    RUN,
    PAUSE_EXPLAIN,
)


class Physics9GalileoPisaMassIndependenceV61SeniorFinal(Physics9GalileoPisaMassIndependenceV6Final):
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
        height = DoubleArrow(
            [-5.35, top_y, 0], [-5.35, bottom_y, 0], buff=0.03,
            color=MID_GRAY, stroke_width=1.5,
            max_tip_length_to_length_ratio=0.05,
        )
        hlab = self.math(r"h=20\,m", 22).next_to(height, LEFT, buff=0.10)

        clock_label = self.txt("t =", 25, BOLD)
        clock_value = DecimalNumber(0.0, num_decimal_places=2, font_size=30, color=BLACK)
        clock_unit = self.txt("s", 24)
        clock = VGroup(clock_label, clock_value, clock_unit).arrange(RIGHT, buff=0.10)
        clock.move_to([-3.65, 2.18, 0])

        calc = VGroup(
            self.txt("IDEAL DROP FROM REST", 22, BOLD),
            self.math(r"h=\frac12gt^2", 36),
            self.math(r"t=\sqrt{\frac{2h}{g}}", 36),
            self.math(rf"t=\sqrt{{\frac{{2(20)}}{{9.81}}}}\approx{t_hit:.2f}\,s", 31),
            self.math(rf"v_f=gt\approx(9.81)({t_hit:.2f})\approx{vf:.1f}\,m/s", 30),
            self.formula_panel(
                r"\boxed{t_1=t_2\quad\text{and}\quad v_{f1}=v_{f2}}",
                width=5.3, height=0.85, size=28,
            ),
        ).arrange(DOWN, buff=0.25).move_to(right.get_center())
        self.fit(calc, 5.55, 4.4)

        self.play(FadeIn(left), FadeIn(right), Create(path1), Create(path2), Create(ground), run_time=RUN)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(mlabels), FadeIn(height), FadeIn(hlab), FadeIn(clock), run_time=RUN)
        self.play(FadeIn(calc), run_time=RUN)

        tracker = ValueTracker(0.0)
        def y_of_alpha(alpha):
            return top_y + (bottom_y - top_y) * (alpha ** 2)

        b1.add_updater(lambda m: m.move_to([x1, y_of_alpha(tracker.get_value()), 0]))
        b2.add_updater(lambda m: m.move_to([x2, y_of_alpha(tracker.get_value()), 0]))
        clock_value.add_updater(lambda m: m.set_value(t_hit * tracker.get_value()))

        self.play(tracker.animate.set_value(1.0), run_time=2.7, rate_func=linear)
        b1.clear_updaters()
        b2.clear_updaters()
        clock_value.clear_updaters()

        impact = self.txt("SIMULTANEOUS IMPACT", 23, BOLD).move_to([-3.65, -2.24, 0])
        self.play(FadeIn(impact), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview:
# manim -pql Physics9_Galileo_Pisa_Mass_Independence_V6_1_SENIOR_FINAL.py Physics9GalileoPisaMassIndependenceV61SeniorFinal --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Pisa_Mass_Independence_V6_1_SENIOR_FINAL.py Physics9GalileoPisaMassIndependenceV61SeniorFinal --disable_caching
