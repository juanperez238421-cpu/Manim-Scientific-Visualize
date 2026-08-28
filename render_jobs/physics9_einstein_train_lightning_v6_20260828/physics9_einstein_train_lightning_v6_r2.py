#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6 R2 visual-QA override.

Keeps the complete V6 physics/narrative and replaces the two scenes where the
first PQH render revealed layout collisions:
1) platform-observer arrival + calculation;
2) moving-train observer reception callouts.
"""
from __future__ import annotations

import numpy as np
from manim import *
from physics9_einstein_train_lightning_v6 import *


class Physics9EinsteinTrainLightningV6R2(Physics9EinsteinTrainLightningV6):
    """Release candidate with post-render collision corrections."""

    def platform_observer(self):
        h = self.header(
            3,
            "PLATFORM OBSERVER: THE FLASHES ARRIVE TOGETHER",
            "The observer is fixed at x = 0 and is equally distant from both strike positions.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        rail = Line(LEFT * 7.1 + DOWN * 1.55, RIGHT * 7.1 + DOWN * 1.55,
                    color=MID, stroke_width=2)
        train = self.train_shell(8.0, 1.80).shift(DOWN * 0.50)
        pobs = self.person(0.58).move_to(DOWN * 2.35)
        plab = self.txt("PLATFORM OBSERVER", 20, BOLD).next_to(pobs, DOWN, buff=0.08)
        lb = self.lightning(-4.0, 1.40, 0.68)
        rb = self.lightning(4.0, 1.40, 0.68)
        lp = self.pulse(np.array([-4.0, -0.10, 0.0]))
        rp = self.pulse(np.array([4.0, -0.10, 0.0]))
        t = ValueTracker(0.0)
        badge = always_redraw(
            lambda: self.formula_box(
                rf"t={t.get_value():.3f}\,\mu\mathrm{{s}}",
                3.15, 0.76, 30, WHITE,
            ).move_to(RIGHT * 5.25 + UP * 1.55)
        )

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

        # Keep the conceptual result away from the live time badge.
        arrive = self.text_box(
            "SIMULTANEOUS ARRIVAL AT x = 0",
            6.3, 0.86, 24,
        ).move_to(LEFT * 2.15 + UP * 1.18)
        self.play(FadeIn(arrive, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_READ)

        # Deliberately separate the motion diagram from the calculation screen.
        motion_group = VGroup(rail, train, pobs, plab, lb, rb, lp, rp, badge, arrive)
        self.play(FadeOut(motion_group), run_time=RUN_FAST)

        eq_title = self.txt("USE THE GENERAL MOTION EQUATION FOR EITHER LIGHT PULSE", 26, BOLD)
        eq_title.move_to(UP * 1.55)
        master = self.formula_box(r"X=X_0+vt", 4.5, 0.92, 44).move_to(UP * 0.55)
        front = self.formula_box(
            r"0=150-ct",
            5.8, 0.88, 38,
        ).move_to(DOWN * 0.55)
        calc = self.formula_box(
            r"t=\frac{150}{c}=0.500\,\mu\mathrm{s}",
            6.6, 0.94, 38, WHITE,
        ).move_to(DOWN * 1.72)
        result = self.text_box(
            "REAR FLASH GIVES THE SAME 0.500 μs RESULT",
            7.4, 0.84, 23,
        ).move_to(DOWN * 2.82)

        self.play(FadeIn(eq_title), FadeIn(master), run_time=RUN)
        self.play(FadeIn(front, shift=UP * 0.06), run_time=RUN)
        self.play(FadeIn(calc, shift=UP * 0.06), run_time=RUN)
        self.play(FadeIn(result, shift=UP * 0.06), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_all()

    def train_observer_animation(self):
        h = self.header(
            4,
            "TRAIN OBSERVER: MOVE TOWARD ONE FLASH, AWAY FROM THE OTHER",
            "The train midpoint moves right at 0.60c while both light pulses still move at c.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        rail = Line(LEFT * 7.1 + DOWN * 1.75, RIGHT * 7.1 + DOWN * 1.75,
                    color=MID, stroke_width=2)
        train = self.train_shell(8.0, 1.88).shift(DOWN * 0.62)
        obs = self.person(0.68, seated=True).move_to(np.array([0.0, -0.62, 0.0]))
        obs_lab = self.txt("TRAIN MIDPOINT", 20, BOLD).next_to(obs, DOWN, buff=0.06)
        lp = self.pulse(np.array([-4.0, -0.20, 0.0]))
        rp = self.pulse(np.array([4.0, -0.20, 0.0]))
        t = ValueTracker(0.0)
        badge = always_redraw(
            lambda: self.formula_box(
                rf"t={t.get_value():.4f}\,\mu\mathrm{{s}}",
                3.55, 0.76, 28, WHITE,
            ).move_to(RIGHT * 5.25 + UP * 1.55)
        )
        note = self.txt(
            "Exact ground-frame positions are used; the train body is faded when it would leave the screen.",
            18, NORMAL, DARK,
        )
        self.fit(note, 12.8)
        note.to_edge(DOWN, buff=0.14)

        self.play(
            Create(rail), FadeIn(train), FadeIn(obs), FadeIn(obs_lab),
            FadeIn(lp), FadeIn(rp), FadeIn(badge), FadeIn(note), run_time=RUN,
        )

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

        # Left-side callout is geometrically independent of the right-side clock.
        front_first = self.text_box(
            "FRONT FLASH ARRIVES FIRST",
            5.4, 0.84, 24,
        ).move_to(LEFT * 2.75 + UP * 1.15)
        self.play(FadeIn(front_first), Indicate(rp, color=AMBER), run_time=RUN)
        self.wait(PAUSE)

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

        rear_later = self.text_box(
            "REAR FLASH ARRIVES LATER",
            5.4, 0.84, 24,
        ).move_to(LEFT * 2.75 + UP * 1.15)
        self.play(FadeIn(rear_later), Indicate(lp, color=AMBER), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_all()
