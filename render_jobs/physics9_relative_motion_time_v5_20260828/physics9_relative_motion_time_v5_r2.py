#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 Relativity V5 R2 — post-render senior visual QA patch.

This subclass keeps the full V5 pedagogy and numerical validation while
correcting defects found in the first PQH contact-sheet inspection:
1) walking arms were rotated around the wrong reference direction;
2) inside-train velocity label touched the train body;
3) ground-frame information cards overlapped one another and the train;
4) light-clock speed card covered the moving cabin/path;
5) final synthesis arrow crossed the conclusion text.
"""
from __future__ import annotations

import numpy as np
from manim import *
from physics9_relative_motion_time_v5 import (
    Physics9RelativeMotionTimeV5,
    INK, DARK, MID, LIGHT, PAPER, AMBER, AMBER_SOFT,
    RUN_FAST, RUN, RUN_SLOW, PAUSE, PAUSE_READ, PAUSE_COPY,
)


class Physics9RelativeMotionTimeV5R2(Physics9RelativeMotionTimeV5):
    """Visual-QA corrected release candidate."""

    def person_pose(self, phase=0.0, scale=1.0, seated=False, facing=1):
        if seated:
            return super().person_pose(phase, scale, seated=True, facing=facing)

        bob = 0.028 * np.cos(2 * phase) * scale
        hip = np.array([0.0, bob, 0.0])
        shoulder = hip + UP * 0.57 * scale
        head_c = shoulder + UP * (0.31 * scale + 0.012 * np.cos(2 * phase) * scale)

        head = Circle(
            radius=0.18 * scale,
            stroke_color=INK,
            stroke_width=2.4,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(head_c)
        torso = Line(shoulder, hip, color=INK, stroke_width=5)

        leg_swing = 0.56 * np.sin(phase) * facing
        leg_swing_2 = 0.56 * np.sin(phase + PI) * facing
        arm_swing = 0.68 * np.sin(phase + PI) * facing
        arm_swing_2 = 0.68 * np.sin(phase) * facing

        thigh_len = 0.43 * scale
        shin_len = 0.43 * scale
        arm_len = 0.40 * scale

        knee1 = hip + self._vec(leg_swing, thigh_len)
        knee2 = hip + self._vec(leg_swing_2, thigh_len)

        flex1 = 0.34 * max(0.0, np.sin(phase + PI / 2))
        flex2 = 0.34 * max(0.0, np.sin(phase + 3 * PI / 2))
        foot1 = knee1 + self._vec(leg_swing - flex1 * facing, shin_len)
        foot2 = knee2 + self._vec(leg_swing_2 - flex2 * facing, shin_len)

        # _vec(0) points DOWN. Arms therefore use the swing angle directly.
        hand1 = shoulder + self._vec(arm_swing, arm_len)
        hand2 = shoulder + self._vec(arm_swing_2, arm_len)

        arm1 = Line(shoulder, hand1, color=INK, stroke_width=4)
        arm2 = Line(shoulder, hand2, color=INK, stroke_width=4)
        leg1a = Line(hip, knee1, color=INK, stroke_width=5)
        leg1b = Line(knee1, foot1, color=INK, stroke_width=5)
        leg2a = Line(hip, knee2, color=INK, stroke_width=5)
        leg2b = Line(knee2, foot2, color=INK, stroke_width=5)
        shoe1 = Line(foot1, foot1 + RIGHT * 0.16 * scale * facing, color=INK, stroke_width=4)
        shoe2 = Line(foot2, foot2 + RIGHT * 0.16 * scale * facing, color=INK, stroke_width=4)

        return VGroup(
            head, torso, arm1, arm2,
            leg1a, leg1b, leg2a, leg2b, shoe1, shoe2
        )

    def inside_frame(self):
        h = self.header(
            1,
            "INSIDE THE TRAIN: YOU SEE THE WALKER MOVE",
            "Your reference frame moves with the train, so the train itself is at rest for you.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        train = self.train_shell(8.4, 2.45).move_to(LEFT * 3.05 + DOWN * 0.25)
        you = self.person_pose(0, 0.92, seated=True).move_to(
            train.get_center() + LEFT * 2.45 + DOWN * 0.02
        )
        you_label = self.txt("YOU", 20, BOLD).next_to(you, DOWN, buff=0.08)

        x_scene = ValueTracker(-4.15)
        phase = ValueTracker(0.0)
        t = ValueTracker(0.0)
        x_phys = ValueTracker(0.0)

        walker = always_redraw(
            lambda: self.person_pose(phase.get_value(), 0.92).move_to(
                np.array([x_scene.get_value(), -0.29, 0.0])
            )
        )
        walker_label = always_redraw(
            lambda: self.txt("WALKER", 20, BOLD).next_to(walker, DOWN, buff=0.08)
        )

        vel = self.velocity_arrow(
            LEFT * 5.25 + DOWN * 1.95,
            LEFT * 1.65 + DOWN * 1.95,
            r"v'=2\,\mathrm{m/s}",
        )
        # Explicit post-render QA fix: keep label below arrow and outside train body.
        vel[1].next_to(vel[0], DOWN, buff=0.08)

        t_badge = self.clock_badge("t' =", t, "s", 1, RIGHT * 4.55 + UP * 1.35)
        x_badge = self.distance_badge("X' =", x_phys, "m", RIGHT * 4.55 + UP * 0.35)
        equation = self.formula_box(
            r"X'=X'_0+v't", width=5.0, size=42
        ).move_to(RIGHT * 4.55 + DOWN * 0.88)

        self.play(
            FadeIn(train), FadeIn(you), FadeIn(you_label),
            FadeIn(walker), FadeIn(walker_label),
            run_time=RUN,
        )
        self.play(
            GrowArrow(vel[0]), Write(vel[1]),
            FadeIn(t_badge), FadeIn(x_badge), FadeIn(equation),
            run_time=RUN,
        )
        self.play(
            x_scene.animate.set_value(-0.35),
            phase.animate.set_value(4.0 * TAU),
            t.animate.set_value(self.T_OBS),
            x_phys.animate.set_value(self.V_WALK * self.T_OBS),
            run_time=4.2,
            rate_func=linear,
        )

        result = self.formula_box(
            r"X'=0+(2)(3)=6\,\mathrm{m}", width=5.2, size=36
        ).move_to(RIGHT * 4.55 + DOWN * 2.00)
        self.play(FadeIn(result, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)

        self.play(
            FadeOut(VGroup(
                h, train, you, you_label, walker, walker_label,
                vel, t_badge, x_badge, equation, result
            ), shift=LEFT * 0.12),
            run_time=RUN_FAST,
        )

    def ground_frame(self):
        h = self.header(
            2,
            "FROM THE BUILDING: THE TRAIN AND WALKER BOTH MOVE",
            "The observer is fixed to the ground. Now the train contributes to the walker's velocity.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        ground = Line(
            LEFT * 7.2 + DOWN * 2.05,
            RIGHT * 7.2 + DOWN * 2.05,
            color=MID,
            stroke_width=2,
        )
        building = self.building(0.76).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.48)
        observer = self.person_pose(0, 0.60).move_to(building.get_center() + UP * 0.18)
        obs_label = self.text_box(
            "BUILDING OBSERVER", 3.2, 0.68, 19
        ).move_to(RIGHT * 5.40 + DOWN * 2.55)

        train = self.train_shell(6.7, 1.78, exterior=True).move_to(
            LEFT * 4.40 + DOWN * 0.82
        )

        walk_x = ValueTracker(-4.80)
        phase = ValueTracker(0.0)
        time = ValueTracker(0.0)
        train_phys = ValueTracker(0.0)
        walker_phys = ValueTracker(0.0)

        walker = always_redraw(
            lambda: self.person_pose(phase.get_value(), 0.66).move_to(
                np.array([walk_x.get_value(), -0.85, 0.0])
            )
        )
        sight = always_redraw(lambda: self.sightline(observer, walker))

        # Lower strip = velocity decomposition.
        v_train = self.velocity_arrow(
            LEFT * 5.5 + DOWN * 2.60,
            LEFT * 2.25 + DOWN * 2.60,
            r"20\,\mathrm{m/s}",
            MID,
            24,
        )
        v_walk_rel = self.velocity_arrow(
            LEFT * 1.90 + DOWN * 2.60,
            LEFT * 0.55 + DOWN * 2.60,
            r"+\,2\,\mathrm{m/s}",
            INK,
            24,
        )

        # Upper strip = information. Fixed columns prevent card/train collisions.
        v_total = self.formula_box(
            r"v_{\mathrm{walker,ground}}=20+2=22\,\mathrm{m/s}",
            width=6.0,
            size=32,
        ).move_to(LEFT * 2.30 + UP * 1.55)

        t_badge = self.clock_badge(
            "t =", time, "s", 1, RIGHT * 4.05 + UP * 1.55
        )
        train_badge = self.distance_badge(
            "Xtrain =", train_phys, "m", RIGHT * 4.05 + UP * 0.55
        )
        walker_badge = self.distance_badge(
            "Xwalker =", walker_phys, "m", RIGHT * 4.05 + DOWN * 0.45
        )

        self.play(
            Create(ground), FadeIn(building), FadeIn(observer), FadeIn(obs_label),
            FadeIn(train), FadeIn(walker),
            run_time=RUN,
        )
        self.add(sight)
        self.play(
            GrowArrow(v_train[0]), Write(v_train[1]),
            GrowArrow(v_walk_rel[0]), Write(v_walk_rel[1]),
            FadeIn(v_total),
            FadeIn(t_badge), FadeIn(train_badge), FadeIn(walker_badge),
            run_time=RUN,
        )

        # Visual travel is compressed to keep the moving train outside the info column.
        self.play(
            train.animate.shift(RIGHT * 3.40),
            walk_x.animate.set_value(-0.05),
            phase.animate.set_value(5.0 * TAU),
            time.animate.set_value(self.T_OBS),
            train_phys.animate.set_value(self.V_TRAIN * self.T_OBS),
            walker_phys.animate.set_value(self.V_GROUND * self.T_OBS),
            run_time=4.4,
            rate_func=linear,
        )
        self.wait(PAUSE)

        self.play(
            FadeOut(sight),
            FadeOut(VGroup(
                ground, building, observer, obs_label, train, walker,
                v_train, v_walk_rel, v_total,
                t_badge, train_badge, walker_badge,
            )),
            run_time=RUN_FAST,
        )

        eq0 = self.formula_box(r"X=X_0+vt", width=4.7, size=46).shift(UP * 1.55)
        eq1 = self.formula_box(
            r"X_{\mathrm{train}}=0+(20)(3)=60\,\mathrm{m}",
            width=7.3,
            size=36,
        ).shift(UP * 0.30)
        eq2 = self.formula_box(
            r"X_{\mathrm{walker}}=0+(22)(3)=66\,\mathrm{m}",
            width=7.3,
            size=36,
        ).shift(DOWN * 0.85)
        diff = self.text_box(
            "The walker is 6 m ahead of the train reference point.",
            8.4, 0.90, 25, BOLD,
        ).shift(DOWN * 2.05)

        self.play(FadeIn(eq0), run_time=RUN)
        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(diff, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.play(FadeOut(VGroup(h, eq0, eq1, eq2, diff)), run_time=RUN_FAST)

    def light_clock_ground_frame(self):
        h = self.header(
            8,
            "EXERCISE — STEP 2: THE SAME LIGHT CLOCK FROM THE GROUND",
            "Now the train moves at v = 0.60c while the light still moves at c.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        baseline = Line(
            LEFT * 7.0 + DOWN * 2.15,
            RIGHT * 0.8 + DOWN * 2.15,
            color=LIGHT,
            stroke_width=2,
        )
        origin_mark = Line(
            DOWN * 2.28, DOWN * 2.02, color=MID, stroke_width=2
        ).shift(LEFT * 5.20)
        origin_label = self.txt(
            "x = 0", 18, BOLD, MID
        ).next_to(origin_mark, DOWN, buff=0.05)

        start_x = -5.20
        cabin_x = ValueTracker(start_x)
        pulse_x = ValueTracker(start_x)
        pulse_y = ValueTracker(-1.60)

        def moving_cabin():
            body = RoundedRectangle(
                width=2.5, height=3.6, corner_radius=0.12,
                stroke_color=DARK, stroke_width=2,
                fill_color=WHITE, fill_opacity=0.92,
            )
            body.move_to(np.array([cabin_x.get_value(), -0.10, 0]))
            bot = Line(LEFT * 0.82, RIGHT * 0.82, color=INK, stroke_width=3.5)
            top = bot.copy()
            bot.move_to(body.get_center() + DOWN * 1.50)
            top.move_to(body.get_center() + UP * 1.50)
            return VGroup(body, bot, top)

        cabin = always_redraw(moving_cabin)
        pulse = always_redraw(
            lambda: Dot(
                np.array([pulse_x.get_value(), pulse_y.get_value(), 0]),
                radius=0.10,
                color=AMBER,
            )
        )
        glow = always_redraw(
            lambda: Circle(
                radius=0.22,
                stroke_color=AMBER_SOFT,
                stroke_opacity=0.55,
            ).move_to(pulse)
        )

        self.play(
            Create(baseline), Create(origin_mark), FadeIn(origin_label),
            FadeIn(cabin), FadeIn(pulse), FadeIn(glow),
            run_time=RUN,
        )

        # QA fix: right-side card cannot cover the cabin or diagonal light path.
        motion_label = self.text_box(
            "TRAIN SPEED: 0.60c", 3.8, 0.76, 23, BOLD
        ).move_to(RIGHT * 4.25 + UP * 1.55)
        self.play(FadeIn(motion_label), run_time=RUN)

        first_start = np.array([start_x, -1.60, 0])
        first_end = np.array([start_x + 2.25, 1.40, 0])
        path_up = Line(first_start, first_end, color=AMBER, stroke_width=2.8)

        self.play(
            cabin_x.animate.set_value(start_x + 2.25),
            pulse_x.animate.set_value(start_x + 2.25),
            pulse_y.animate.set_value(1.40),
            Create(path_up),
            run_time=3.4,
            rate_func=linear,
        )
        self.play(
            Flash(first_end, color=AMBER, flash_radius=0.34, line_length=0.12),
            run_time=RUN_FAST,
        )

        second_end = np.array([start_x + 4.50, -1.60, 0])
        path_down = Line(first_end, second_end, color=AMBER, stroke_width=2.8)
        self.play(
            cabin_x.animate.set_value(start_x + 4.50),
            pulse_x.animate.set_value(start_x + 4.50),
            pulse_y.animate.set_value(-1.60),
            Create(path_down),
            run_time=3.4,
            rate_func=linear,
        )
        self.play(
            Flash(second_end, color=AMBER, flash_radius=0.34, line_length=0.12),
            run_time=RUN_FAST,
        )

        self.play(
            FadeOut(VGroup(cabin, pulse, glow, motion_label)),
            run_time=RUN_FAST,
        )

        label_path = self.txt(
            "The ground observer sees a longer diagonal path.", 24, BOLD
        ).move_to(LEFT * 3.2 + UP * 1.92)
        self.play(FadeIn(label_path), run_time=RUN)

        general = self.formula_box(
            r"X=X_0+vt", width=4.5, size=45
        ).move_to(RIGHT * 4.30 + UP * 1.55)
        mirror_x = self.formula_box(
            r"x_{\mathrm{mirror}}=0+(0.60c)t",
            width=5.8,
            size=36,
        ).move_to(RIGHT * 4.30 + UP * 0.35)
        light_d = self.formula_box(
            r"d_{\mathrm{light}}=ct", width=4.7, size=40
        ).move_to(RIGHT * 4.30 + DOWN * 0.82)
        clue = self.text_box(
            "Use the right triangle for ONE half-trip.",
            5.8, 0.80, 23, BOLD, PAPER,
        ).move_to(RIGHT * 4.30 + DOWN * 2.00)

        self.play(FadeIn(general), run_time=RUN)
        self.play(FadeIn(mirror_x), run_time=RUN)
        self.play(FadeIn(light_d), FadeIn(clue), run_time=RUN)
        self.wait(PAUSE_COPY)

        self.play(
            FadeOut(VGroup(
                h, baseline, origin_mark, origin_label,
                path_up, path_down, label_path,
                general, mirror_x, light_d, clue,
            )),
            run_time=RUN_FAST,
        )

    def final_summary(self):
        h = self.header(
            10,
            "FROM RELATIVE VELOCITY TO RELATIVE TIME",
            "The reference frame changes measurements, but the laws of physics remain consistent.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        rows = VGroup(
            self.text_box("WALKER — train frame: 2 m/s", 7.0, 0.86, 25, BOLD),
            self.text_box("WALKER — ground frame: 22 m/s", 7.0, 0.86, 25, BOLD),
            self.text_box("LIGHT — every inertial observer: c", 7.0, 0.86, 25, BOLD),
            self.text_box(
                "LIGHT CLOCK — 20 ns inside, 25 ns from ground",
                8.2, 0.86, 25, BOLD,
            ),
        ).arrange(DOWN, buff=0.18).shift(LEFT * 2.75 + DOWN * 0.15)

        # QA fix: short connector ends before conclusion text starts.
        arrow = Arrow(
            RIGHT * 0.65,
            RIGHT * 1.45,
            color=AMBER,
            stroke_width=5,
            buff=0,
        )
        final = VGroup(
            self.txt("c stays invariant", 28, BOLD, AMBER),
            self.txt("↓", 33, BOLD, DARK),
            self.txt("space and time must adjust", 29, BOLD),
            self.txt("↓", 33, BOLD, DARK),
            self.txt("SPECIAL RELATIVITY", 34, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(RIGHT * 4.65 + DOWN * 0.15)

        self.play(
            LaggedStart(
                *[FadeIn(r, shift=UP * 0.08) for r in rows],
                lag_ratio=0.16,
            ),
            run_time=RUN_SLOW,
        )
        self.play(GrowArrow(arrow), run_time=RUN)
        self.play(
            LaggedStart(
                *[FadeIn(x, shift=UP * 0.06) for x in final],
                lag_ratio=0.16,
            ),
            run_time=RUN_SLOW,
        )
        self.wait(PAUSE_COPY)

        exit_q = self.text_box(
            "EXIT QUESTION: Why do the two observers disagree about elapsed time?",
            11.4, 0.92, 26, BOLD, PAPER,
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(exit_q, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
