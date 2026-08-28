#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Relative Motion, Maxwell, Einstein, and Relative Time
V5: 100% 2D, 100% English, fluid motion + fully worked time-dilation exercise.

Pedagogical spine
-----------------
1) A person walks inside a train.
2) A seated passenger measures 2 m/s.
3) A building observer measures 22 m/s because the train moves at 20 m/s.
4) Use the general position equation X = X0 + vt in both frames.
5) Historical bridge: Galileo/Newton -> Maxwell -> Einstein.
6) A light-clock exercise derives relative time step by step.

Final render:
    manim -pqh physics9_relative_motion_time_v5.py Physics9RelativeMotionTimeV5 \
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
LIGHT = "#D8D8D8"
PAPER = "#F5F5F5"
AMBER = "#D6A000"
AMBER_SOFT = "#E7C85A"

RUN_FAST = 0.55
RUN = 0.95
RUN_SLOW = 1.35
PAUSE = 1.10
PAUSE_READ = 1.85
PAUSE_COPY = 2.60

# ---------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------
class Physics9RelativeMotionTimeV5(Scene):
    """Projector-safe lesson with articulated walking, parallax motion,
    observer sightlines, and a derived time-dilation exercise.
    """

    # Classical example
    V_TRAIN = 20.0      # m/s
    V_WALK = 2.0        # m/s relative to train
    V_GROUND = 22.0     # m/s relative to ground
    T_OBS = 3.0         # s

    # Relativistic light-clock example
    C = 3.00e8          # m/s
    BETA = 0.60         # v/c
    H = 3.0             # m, mirror separation
    HALF_TRAIN_NS = 10.0
    FULL_TRAIN_NS = 20.0
    HALF_GROUND_NS = 12.5
    FULL_GROUND_NS = 25.0
    GAMMA = 1.25

    # ------------------------- timing wrappers -------------------------
    def play(self, *animations, **kwargs):
        if "run_time" in kwargs and kwargs["run_time"] is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------- text/layout helpers ---------------------
    def txt(self, s, size=30, weight=NORMAL, color=INK):
        return Text(s, font_size=size, weight=weight, color=color)

    def mtex(self, s, size=40, color=INK):
        return MathTex(s, font_size=size, color=color)

    def fit(self, mob, max_w=14.2, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        kicker = self.txt(f"PHYSICS 9  •  RELATIVITY  •  {number:02d}", 19, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.0, 0.62)
        sub_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 13.8, 0.42)
        stack = VGroup(kicker, title_m, sub_m).arrange(DOWN, buff=0.07)
        stack.to_edge(UP, buff=0.18)
        rule = Line(LEFT * 7.10, RIGHT * 7.10, color=LIGHT, stroke_width=2)
        rule.next_to(stack, DOWN, buff=0.09)
        return VGroup(stack, rule)

    def formula_box(self, tex, width=6.0, height=1.0, size=40, fill=PAPER):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.7,
            fill_color=fill, fill_opacity=1.0,
        )
        eq = self.mtex(tex, size)
        self.fit(eq, width - 0.42, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def text_box(self, text, width=5.5, height=0.88, size=26, weight=BOLD, fill=WHITE):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=DARK, stroke_width=1.8,
            fill_color=fill, fill_opacity=1.0,
        )
        t = self.fit(self.txt(text, size, weight), width - 0.38, height - 0.18)
        t.move_to(box)
        return VGroup(box, t)

    def section_transition(self, old_group, new_header):
        """Fluid section hand-off without a long blank frame."""
        anims = []
        if old_group is not None:
            anims.append(FadeOut(old_group, shift=LEFT * 0.18))
        anims.append(FadeIn(new_header, shift=UP * 0.08))
        self.play(*anims, run_time=RUN_FAST)

    # ------------------------- figure geometry -------------------------
    @staticmethod
    def _vec(angle, length):
        """Vector measured from vertical-down direction."""
        return np.array([np.sin(angle) * length, -np.cos(angle) * length, 0.0])

    def person_pose(self, phase=0.0, scale=1.0, seated=False, facing=1):
        """Articulated 2D person. Walking phase continuously changes arms,
        thighs, knees, feet, torso bob, and head bob.
        """
        if seated:
            hip = np.array([0.0, 0.05, 0.0]) * scale
            shoulder = hip + UP * 0.54 * scale
            head_c = shoulder + UP * 0.31 * scale
            head = Circle(
                radius=0.18 * scale, stroke_color=INK, stroke_width=2.4,
                fill_color=WHITE, fill_opacity=1.0,
            ).move_to(head_c)
            torso = Line(shoulder, hip, color=INK, stroke_width=5)
            elbow = shoulder + RIGHT * 0.24 * scale * facing + DOWN * 0.20 * scale
            hand = elbow + RIGHT * 0.18 * scale * facing + DOWN * 0.08 * scale
            arm1 = Line(shoulder, elbow, color=INK, stroke_width=4)
            arm2 = Line(elbow, hand, color=INK, stroke_width=4)
            knee = hip + RIGHT * 0.34 * scale * facing + DOWN * 0.08 * scale
            foot = knee + DOWN * 0.45 * scale
            thigh = Line(hip, knee, color=INK, stroke_width=5)
            shin = Line(knee, foot, color=INK, stroke_width=5)
            shoe = Line(foot, foot + RIGHT * 0.20 * scale * facing, color=INK, stroke_width=4)
            return VGroup(head, torso, arm1, arm2, thigh, shin, shoe)

        # Natural gait: one cycle = TAU.
        bob = 0.028 * np.cos(2 * phase) * scale
        hip = np.array([0.0, 0.0 + bob, 0.0])
        shoulder = hip + UP * 0.57 * scale
        head_c = shoulder + UP * (0.31 * scale + 0.012 * np.cos(2 * phase) * scale)

        head = Circle(
            radius=0.18 * scale, stroke_color=INK, stroke_width=2.4,
            fill_color=WHITE, fill_opacity=1.0,
        ).move_to(head_c)
        torso = Line(shoulder, hip, color=INK, stroke_width=5)

        leg_swing = 0.52 * np.sin(phase) * facing
        leg_swing_2 = 0.52 * np.sin(phase + PI) * facing
        arm_swing = 0.62 * np.sin(phase + PI) * facing
        arm_swing_2 = 0.62 * np.sin(phase) * facing

        thigh_len = 0.43 * scale
        shin_len = 0.43 * scale
        arm_len = 0.38 * scale

        knee1 = hip + self._vec(leg_swing, thigh_len)
        knee2 = hip + self._vec(leg_swing_2, thigh_len)

        # Flex the rear knee more strongly to avoid a rigid "scissor" gait.
        flex1 = 0.28 * max(0.0, np.sin(phase + PI / 2))
        flex2 = 0.28 * max(0.0, np.sin(phase + 3 * PI / 2))
        foot1 = knee1 + self._vec(leg_swing - flex1 * facing, shin_len)
        foot2 = knee2 + self._vec(leg_swing_2 - flex2 * facing, shin_len)

        hand1 = shoulder + self._vec(PI + arm_swing, arm_len)
        hand2 = shoulder + self._vec(PI + arm_swing_2, arm_len)

        arm1 = Line(shoulder, hand1, color=INK, stroke_width=4)
        arm2 = Line(shoulder, hand2, color=INK, stroke_width=4)
        leg1a = Line(hip, knee1, color=INK, stroke_width=5)
        leg1b = Line(knee1, foot1, color=INK, stroke_width=5)
        leg2a = Line(hip, knee2, color=INK, stroke_width=5)
        leg2b = Line(knee2, foot2, color=INK, stroke_width=5)
        shoe1 = Line(
            foot1, foot1 + RIGHT * 0.16 * scale * facing,
            color=INK, stroke_width=4,
        )
        shoe2 = Line(
            foot2, foot2 + RIGHT * 0.16 * scale * facing,
            color=INK, stroke_width=4,
        )
        return VGroup(head, torso, arm1, arm2, leg1a, leg1b, leg2a, leg2b, shoe1, shoe2)

    def train_shell(self, width=9.2, height=2.25, exterior=False):
        """Metro geometry with proportional windows that remain inside body."""
        body = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=INK, stroke_width=2.3,
            fill_color=WHITE, fill_opacity=1.0,
        )
        floor_y = -height * 0.31
        floor = Line(
            body.get_left() + RIGHT * 0.35 + UP * floor_y,
            body.get_right() + LEFT * 0.35 + UP * floor_y,
            color=LIGHT, stroke_width=2,
        )
        window_w = min(1.12, width / 7.4)
        window_h = min(0.58, height * 0.25)
        windows = VGroup()
        for frac in (-0.34, -0.17, 0.0, 0.17, 0.34):
            win = RoundedRectangle(
                width=window_w, height=window_h, corner_radius=0.06,
                stroke_color=LIGHT, stroke_width=1.2,
                fill_color=PAPER, fill_opacity=1.0,
            )
            win.move_to(body.get_center() + RIGHT * (frac * width) + UP * (height * 0.24))
            windows.add(win)

        door_h = height * 0.70
        door_sep = min(0.38, width * 0.045)
        door = VGroup(
            Line(UP * door_h / 2, DOWN * door_h / 2, color=LIGHT, stroke_width=1.4),
            Line(UP * door_h / 2, DOWN * door_h / 2, color=LIGHT, stroke_width=1.4),
        )
        door[0].shift(LEFT * door_sep)
        door[1].shift(RIGHT * door_sep)
        door.move_to(body)

        parts = [body, floor, windows, door]
        if exterior:
            wheels = VGroup()
            for xfrac in (-0.28, 0.28):
                wheel = Circle(
                    radius=0.17, stroke_color=INK, stroke_width=2,
                    fill_color=WHITE, fill_opacity=1,
                )
                spoke1 = Line(LEFT * 0.13, RIGHT * 0.13, color=MID, stroke_width=1.4)
                spoke2 = Line(DOWN * 0.13, UP * 0.13, color=MID, stroke_width=1.4)
                wg = VGroup(wheel, spoke1, spoke2)
                wg.move_to(body.get_center() + RIGHT * (width * xfrac) + DOWN * (height / 2 + 0.16))
                wheels.add(wg)
            parts.append(wheels)
        return VGroup(*parts)

    def building(self, scale=1.0):
        shell = Rectangle(
            width=2.15 * scale, height=4.35 * scale,
            stroke_color=DARK, stroke_width=2,
            fill_color=PAPER, fill_opacity=0.70,
        )
        wins = VGroup()
        for y in (1.20, 0.18, -0.84):
            for x in (-0.48, 0.48):
                r = Rectangle(
                    width=0.62 * scale, height=0.62 * scale,
                    stroke_color=LIGHT, stroke_width=1.4,
                    fill_color=WHITE, fill_opacity=1.0,
                )
                r.move_to(shell.get_center() + RIGHT * x * scale + UP * y * scale)
                wins.add(r)
        return VGroup(shell, wins)

    def sightline(self, observer, target):
        return DashedLine(
            observer.get_center() + UP * 0.45,
            target.get_center() + UP * 0.52,
            dash_length=0.08,
            color=MID,
            stroke_width=1.8,
        )

    def velocity_arrow(self, start, end, label, color=INK, size=25):
        arr = Arrow(
            start, end, buff=0, color=color, stroke_width=4,
            max_tip_length_to_length_ratio=0.13,
        )
        lab = self.mtex(label, size, color=color).next_to(arr, UP, buff=0.08)
        return VGroup(arr, lab)

    def clock_badge(self, label, tracker, unit="s", decimals=1, center=ORIGIN):
        box = RoundedRectangle(
            width=2.55, height=0.78, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        prefix = self.txt(label, 21, BOLD).move_to(box.get_left() + RIGHT * 0.48)
        number = DecimalNumber(
            tracker.get_value(), num_decimal_places=decimals,
            font_size=28, color=INK,
        )
        unit_m = self.txt(unit, 19, BOLD)
        row = VGroup(prefix, number, unit_m).arrange(RIGHT, buff=0.10)
        row.move_to(box)
        number.add_updater(lambda d: d.set_value(tracker.get_value()))
        return VGroup(box, row)

    def distance_badge(self, label, tracker, unit="m", center=ORIGIN, decimals=1):
        box = RoundedRectangle(
            width=3.20, height=0.78, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        prefix = self.txt(label, 20, BOLD)
        number = DecimalNumber(
            tracker.get_value(), num_decimal_places=decimals,
            font_size=27, color=INK,
        )
        suffix = self.txt(unit, 19, BOLD)
        row = VGroup(prefix, number, suffix).arrange(RIGHT, buff=0.10)
        row.move_to(box)
        number.add_updater(lambda d: d.set_value(tracker.get_value()))
        return VGroup(box, row)

    # ------------------------- main sequence ---------------------------
    def construct(self):
        # Numerical safety checks: fail fast if educational claims drift.
        assert abs(self.V_TRAIN + self.V_WALK - self.V_GROUND) < 1e-12
        assert abs(self.H / self.C * 1e9 - self.HALF_TRAIN_NS) < 1e-12
        gamma = 1.0 / np.sqrt(1.0 - self.BETA**2)
        assert abs(gamma - self.GAMMA) < 1e-12
        assert abs(self.HALF_TRAIN_NS * gamma - self.HALF_GROUND_NS) < 1e-12
        assert abs(2 * self.HALF_GROUND_NS - self.FULL_GROUND_NS) < 1e-12

        self.opening()
        self.inside_frame()
        self.ground_frame()
        self.same_motion_compare()
        self.history_bridge()
        self.maxwell_and_conflict()
        self.einstein_bridge()
        self.light_clock_train_frame()
        self.light_clock_ground_frame()
        self.solve_relative_time()
        self.final_summary()

    # -----------------------------------------------------------------
    # 00 — opening
    # -----------------------------------------------------------------
    def opening(self):
        title = VGroup(
            self.txt("PHYSICS 9 • RELATIVITY", 23, BOLD, DARK),
            self.fit(self.txt("ONE MOTION. DIFFERENT OBSERVERS.", 47, BOLD), 13.6),
            self.txt("First ordinary motion. Then light. Then time.", 27, NORMAL, DARK),
        ).arrange(DOWN, buff=0.16).shift(UP * 2.45)

        ground = Line(LEFT * 7.2 + DOWN * 2.05, RIGHT * 7.2 + DOWN * 2.05, color=MID, stroke_width=2)
        building = self.building(0.72).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.65)
        observer = self.person_pose(0, 0.58).move_to(building.get_center() + UP * 0.18)

        train = self.train_shell(7.4, 1.88, exterior=True).move_to(LEFT * 4.10 + DOWN * 0.75)

        walk_x = ValueTracker(-4.10)
        phase = ValueTracker(0.0)
        walker = always_redraw(
            lambda: self.person_pose(phase.get_value(), 0.67)
            .move_to(np.array([walk_x.get_value(), -0.78, 0.0]))
        )
        eye = always_redraw(lambda: self.sightline(observer, walker))

        self.play(Write(title), run_time=RUN_SLOW)
        self.play(Create(ground), FadeIn(building), FadeIn(observer), FadeIn(train), FadeIn(walker), run_time=RUN)
        self.add(eye)

        self.play(
            train.animate.shift(RIGHT * 4.50),
            walk_x.animate.set_value(0.95),
            phase.animate.set_value(5.5 * TAU),
            run_time=4.2,
            rate_func=linear,
        )
        self.wait(PAUSE)
        self.play(FadeOut(eye), FadeOut(VGroup(title, ground, building, observer, train, walker)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 01 — inside the train
    # -----------------------------------------------------------------
    def inside_frame(self):
        h = self.header(
            1,
            "INSIDE THE TRAIN: YOU SEE THE WALKER MOVE",
            "Your reference frame moves with the train, so the train itself is at rest for you.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        train = self.train_shell(8.4, 2.45).move_to(LEFT * 3.05 + DOWN * 0.25)
        you = self.person_pose(0, 0.92, seated=True).move_to(train.get_center() + LEFT * 2.45 + DOWN * 0.02)
        you_label = self.txt("YOU", 20, BOLD).next_to(you, DOWN, buff=0.08)

        x_scene = ValueTracker(-4.15)
        phase = ValueTracker(0.0)
        t = ValueTracker(0.0)
        x_phys = ValueTracker(0.0)

        walker = always_redraw(
            lambda: self.person_pose(phase.get_value(), 0.92)
            .move_to(np.array([x_scene.get_value(), -0.29, 0.0]))
        )
        walker_label = always_redraw(
            lambda: self.txt("WALKER", 20, BOLD).next_to(walker, DOWN, buff=0.08)
        )

        vel = self.velocity_arrow(LEFT * 5.25 + DOWN * 1.82, LEFT * 1.65 + DOWN * 1.82, r"v'=2\,\mathrm{m/s}")
        t_badge = self.clock_badge("t' =", t, "s", 1, RIGHT * 4.55 + UP * 1.35)
        x_badge = self.distance_badge("X' =", x_phys, "m", RIGHT * 4.55 + UP * 0.35)

        equation = self.formula_box(r"X'=X'_0+v't", width=5.0, size=42).move_to(RIGHT * 4.55 + DOWN * 0.88)

        self.play(FadeIn(train), FadeIn(you), FadeIn(you_label), FadeIn(walker), FadeIn(walker_label), run_time=RUN)
        self.play(GrowArrow(vel[0]), Write(vel[1]), FadeIn(t_badge), FadeIn(x_badge), FadeIn(equation), run_time=RUN)

        self.play(
            x_scene.animate.set_value(-0.35),
            phase.animate.set_value(4.0 * TAU),
            t.animate.set_value(self.T_OBS),
            x_phys.animate.set_value(self.V_WALK * self.T_OBS),
            run_time=4.2,
            rate_func=linear,
        )

        result = self.formula_box(r"X'=0+(2)(3)=6\,\mathrm{m}", width=5.2, size=36).move_to(RIGHT * 4.55 + DOWN * 2.00)
        self.play(FadeIn(result, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)

        group = VGroup(h, train, you, you_label, walker, walker_label, vel, t_badge, x_badge, equation, result)
        self.play(FadeOut(group, shift=LEFT * 0.12), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 02 — building / ground frame
    # -----------------------------------------------------------------
    def ground_frame(self):
        h = self.header(
            2,
            "FROM THE BUILDING: THE TRAIN AND WALKER BOTH MOVE",
            "The observer is fixed to the ground. Now the train contributes to the walker's velocity.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        ground = Line(LEFT * 7.2 + DOWN * 2.05, RIGHT * 7.2 + DOWN * 2.05, color=MID, stroke_width=2)
        building = self.building(0.76).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.48)
        observer = self.person_pose(0, 0.60).move_to(building.get_center() + UP * 0.18)
        obs_label = self.text_box("BUILDING OBSERVER", 3.2, 0.68, 19).move_to(RIGHT * 5.40 + DOWN * 2.55)

        train = self.train_shell(6.7, 1.78, exterior=True).move_to(LEFT * 4.40 + DOWN * 0.82)

        walk_x = ValueTracker(-4.80)
        phase = ValueTracker(0.0)
        time = ValueTracker(0.0)
        train_phys = ValueTracker(0.0)
        walker_phys = ValueTracker(0.0)

        walker = always_redraw(
            lambda: self.person_pose(phase.get_value(), 0.66)
            .move_to(np.array([walk_x.get_value(), -0.85, 0.0]))
        )
        sight = always_redraw(lambda: self.sightline(observer, walker))

        v_train = self.velocity_arrow(LEFT * 5.5 + DOWN * 2.60, LEFT * 2.25 + DOWN * 2.60, r"20\,\mathrm{m/s}", MID, 24)
        v_walk_rel = self.velocity_arrow(LEFT * 1.90 + DOWN * 2.60, LEFT * 0.55 + DOWN * 2.60, r"+\,2\,\mathrm{m/s}", INK, 24)
        v_total = self.formula_box(r"v_{\mathrm{walker,ground}}=20+2=22\,\mathrm{m/s}", width=6.5, size=34).move_to(LEFT * 1.55 + UP * 1.55)

        t_badge = self.clock_badge("t =", time, "s", 1, RIGHT * 2.65 + UP * 1.55)
        train_badge = self.distance_badge("Xtrain =", train_phys, "m", RIGHT * 3.05 + UP * 0.50)
        walker_badge = self.distance_badge("Xwalker =", walker_phys, "m", RIGHT * 3.05 + DOWN * 0.45)

        self.play(
            Create(ground), FadeIn(building), FadeIn(observer), FadeIn(obs_label),
            FadeIn(train), FadeIn(walker), run_time=RUN
        )
        self.add(sight)
        self.play(
            GrowArrow(v_train[0]), Write(v_train[1]),
            GrowArrow(v_walk_rel[0]), Write(v_walk_rel[1]),
            FadeIn(v_total), FadeIn(t_badge), FadeIn(train_badge), FadeIn(walker_badge),
            run_time=RUN
        )

        self.play(
            train.animate.shift(RIGHT * 4.85),
            walk_x.animate.set_value(0.62),
            phase.animate.set_value(5.0 * TAU),
            time.animate.set_value(self.T_OBS),
            train_phys.animate.set_value(self.V_TRAIN * self.T_OBS),
            walker_phys.animate.set_value(self.V_GROUND * self.T_OBS),
            run_time=4.4,
            rate_func=linear,
        )
        self.wait(PAUSE)

        self.play(FadeOut(sight), FadeOut(VGroup(
            ground, building, observer, obs_label, train, walker,
            v_train, v_walk_rel, v_total, t_badge, train_badge, walker_badge
        )), run_time=RUN_FAST)

        # Calculation screen: one dominant equation at a time.
        eq0 = self.formula_box(r"X=X_0+vt", width=4.7, size=46).shift(UP * 1.55)
        eq1 = self.formula_box(r"X_{\mathrm{train}}=0+(20)(3)=60\,\mathrm{m}", width=7.3, size=36).shift(UP * 0.30)
        eq2 = self.formula_box(r"X_{\mathrm{walker}}=0+(22)(3)=66\,\mathrm{m}", width=7.3, size=36).shift(DOWN * 0.85)
        diff = self.text_box("The walker is 6 m ahead of the train reference point.", 8.4, 0.90, 25, BOLD).shift(DOWN * 2.05)

        self.play(FadeIn(eq0), run_time=RUN)
        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(diff, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.play(FadeOut(VGroup(h, eq0, eq1, eq2, diff)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 03 — same motion, two frames
    # -----------------------------------------------------------------
    def same_motion_compare(self):
        h = self.header(
            3,
            "SAME WALKER. TWO CORRECT VELOCITIES.",
            "Relativity begins with a simple idea: a measured velocity depends on the reference frame.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        divider = Line(UP * 2.15, DOWN * 2.55, color=LIGHT, stroke_width=2)
        left_title = self.txt("TRAIN FRAME S'", 27, BOLD).move_to(LEFT * 4.05 + UP * 1.65)
        right_title = self.txt("GROUND FRAME S", 27, BOLD).move_to(RIGHT * 4.05 + UP * 1.65)

        p1_phase = ValueTracker(0.0)
        p2_phase = ValueTracker(0.0)
        p1 = always_redraw(lambda: self.person_pose(p1_phase.get_value(), 1.08).move_to(LEFT * 4.05 + UP * 0.25))
        p2 = always_redraw(lambda: self.person_pose(p2_phase.get_value(), 1.08).move_to(RIGHT * 4.05 + UP * 0.25))
        r1 = self.text_box("2 m/s", 3.5, 0.82, 27).move_to(LEFT * 4.05 + DOWN * 1.25)
        r2 = self.text_box("22 m/s", 3.5, 0.82, 27).move_to(RIGHT * 4.05 + DOWN * 1.25)
        statement = self.fit(
            self.txt("Different measurements do not mean different physics.", 31, BOLD),
            13.6
        ).to_edge(DOWN, buff=0.45)

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), FadeIn(p1), FadeIn(p2), run_time=RUN)
        self.play(p1_phase.animate.set_value(2 * TAU), p2_phase.animate.set_value(2 * TAU), run_time=2.2, rate_func=linear)
        self.play(FadeIn(r1), FadeIn(r2), Write(statement), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeOut(VGroup(h, divider, left_title, right_title, p1, p2, r1, r2, statement)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 04 — Galileo/Newton historical bridge
    # -----------------------------------------------------------------
    def history_bridge(self):
        h = self.header(
            4,
            "GALILEO AND NEWTON: THE CLASSICAL RULE",
            "For ordinary speeds, Galilean velocity addition works extremely well.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        train_arrow = self.velocity_arrow(LEFT * 4.8 + UP * 0.70, LEFT * 1.2 + UP * 0.70, r"V=20\,\mathrm{m/s}", MID, 26)
        walk_arrow = self.velocity_arrow(LEFT * 1.0 + UP * 0.70, RIGHT * 0.25 + UP * 0.70, r"v'=2\,\mathrm{m/s}", INK, 26)
        total_arrow = self.velocity_arrow(LEFT * 4.8 + DOWN * 0.35, RIGHT * 0.25 + DOWN * 0.35, r"v=22\,\mathrm{m/s}", INK, 28)

        rule = self.formula_box(r"v=v'+V", width=4.8, size=50).move_to(RIGHT * 4.20 + UP * 0.35)
        time_rule = self.text_box("Newtonian model: time is universal.", 5.0, 0.88, 25, BOLD).move_to(RIGHT * 4.20 + DOWN * 0.90)
        history = self.txt("Galileo  →  Newton 1687", 30, BOLD, DARK).move_to(RIGHT * 4.20 + DOWN * 2.00)

        self.play(GrowArrow(train_arrow[0]), Write(train_arrow[1]), run_time=RUN)
        self.play(GrowArrow(walk_arrow[0]), Write(walk_arrow[1]), run_time=RUN)
        self.play(GrowArrow(total_arrow[0]), Write(total_arrow[1]), run_time=RUN)
        self.play(FadeIn(rule), FadeIn(time_rule), Write(history), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeOut(VGroup(h, train_arrow, walk_arrow, total_arrow, rule, time_rule, history)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 05 — Maxwell + conflict
    # -----------------------------------------------------------------
    def maxwell_and_conflict(self):
        h = self.header(
            5,
            "JAMES CLERK MAXWELL: LIGHT IS AN ELECTROMAGNETIC WAVE",
            "In the 1860s Maxwell unified electricity and magnetism.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        phase = ValueTracker(0.0)
        axis = Line(LEFT * 5.8, RIGHT * 5.8, color=LIGHT, stroke_width=2).shift(DOWN * 0.15)
        wave = always_redraw(
            lambda: ParametricFunction(
                lambda x: np.array([x, 0.58 * np.sin(2.25 * x - phase.get_value()), 0]),
                t_range=[-5.5, 5.5],
                color=AMBER,
                stroke_width=4,
            ).shift(DOWN * 0.15)
        )
        maxwell = self.txt("JAMES CLERK MAXWELL", 36, BOLD).shift(UP * 1.72)
        cbox = self.formula_box(r"c\approx3.00\times10^8\,\mathrm{m/s}", width=6.0, size=42).shift(DOWN * 1.55)
        sentence = self.fit(
            self.txt("Maxwell's equations predict a fixed wave speed in vacuum.", 27),
            13.2
        ).shift(UP * 1.05)

        self.play(Write(maxwell), FadeIn(sentence), Create(axis), FadeIn(wave), run_time=RUN)
        self.play(phase.animate.set_value(4 * PI), run_time=3.2, rate_func=linear)
        self.play(FadeIn(cbox), run_time=RUN)
        self.wait(PAUSE_READ)

        conflict_left = self.formula_box(r"u=u'+V", width=4.0, size=45).move_to(LEFT * 3.65 + DOWN * 2.45)
        conflict_right = self.formula_box(r"c=\mathrm{same\ vacuum\ speed}", width=5.2, size=35).move_to(RIGHT * 3.15 + DOWN * 2.45)
        self.play(FadeOut(cbox), FadeIn(conflict_left), FadeIn(conflict_right), run_time=RUN)
        conflict_text = self.fit(
            self.txt("Galilean transformations do not preserve Maxwell's equations.", 29, BOLD),
            13.2
        ).to_edge(DOWN, buff=0.18)
        self.play(Write(conflict_text), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeOut(VGroup(h, axis, wave, maxwell, sentence, conflict_left, conflict_right, conflict_text)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 06 — Einstein bridge
    # -----------------------------------------------------------------
    def einstein_bridge(self):
        h = self.header(
            6,
            "EINSTEIN 1905: KEEP RELATIVITY AND KEEP c",
            "Einstein reconciled the relativity principle with Maxwell's electromagnetism.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        title = self.txt("ALBERT EINSTEIN • 1905", 36, BOLD).shift(UP * 1.72)
        p1 = self.text_box("1. The laws of physics are the same in every inertial frame.", 10.8, 0.92, 25, BOLD)
        p2 = self.text_box("2. Every inertial observer measures the same vacuum light speed c.", 10.8, 0.92, 25, BOLD)
        posts = VGroup(p1, p2).arrange(DOWN, buff=0.22).shift(UP * 0.35)
        consequence = self.fit(
            self.txt("If c stays the same, space and time cannot both stay absolute.", 31, BOLD),
            13.3
        ).shift(DOWN * 1.35)
        question = self.text_box("So what must happen to time?", 6.3, 0.95, 29, BOLD, PAPER).shift(DOWN * 2.35)

        self.play(Write(title), run_time=RUN)
        self.play(FadeIn(posts[0], shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(posts[1], shift=UP * 0.08), run_time=RUN)
        self.play(Write(consequence), run_time=RUN_SLOW)
        self.play(FadeIn(question, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.play(FadeOut(VGroup(h, title, posts, consequence, question)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 07 — light clock in train frame
    # -----------------------------------------------------------------
    def light_clock_train_frame(self):
        h = self.header(
            7,
            "EXERCISE — STEP 1: A LIGHT CLOCK INSIDE THE TRAIN",
            "A pulse travels between two mirrors separated by H = 3.0 m.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        # Left: train-frame light clock diagram.
        cabin = RoundedRectangle(
            width=5.2, height=4.2, corner_radius=0.14,
            stroke_color=DARK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(LEFT * 3.85 + DOWN * 0.05)
        bottom = Line(LEFT * 1.10, RIGHT * 1.10, color=INK, stroke_width=4).move_to(cabin.get_center() + DOWN * 1.35)
        top = bottom.copy().move_to(cabin.get_center() + UP * 1.65)
        vertical = DashedLine(bottom.get_center(), top.get_center(), color=AMBER, stroke_width=2.4)
        bracket = DoubleArrow(
            bottom.get_center() + LEFT * 1.50,
            top.get_center() + LEFT * 1.50,
            buff=0, color=MID, stroke_width=2.4,
        )
        hlabel = self.mtex(r"H=3.0\,\mathrm{m}", 31).next_to(bracket, LEFT, buff=0.10)

        pulse = Dot(bottom.get_center(), radius=0.10, color=AMBER)
        glow = Circle(radius=0.22, stroke_color=AMBER_SOFT, stroke_opacity=0.6).move_to(pulse)

        # Right: step-by-step equations.
        step1 = self.text_box("Train frame S': mirrors are at rest.", 5.5, 0.78, 23, BOLD).move_to(RIGHT * 4.35 + UP * 1.55)
        eq1 = self.formula_box(r"t'_{\frac12}=\frac{H}{c}", width=5.0, size=43).move_to(RIGHT * 4.35 + UP * 0.50)
        eq2 = self.formula_box(
            r"t'_{\frac12}=\frac{3.0}{3.00\times10^8}=10.0\,\mathrm{ns}",
            width=6.2, size=32
        ).move_to(RIGHT * 4.35 + DOWN * 0.62)
        eq3 = self.formula_box(r"\Delta t'=2(10.0\,\mathrm{ns})=20.0\,\mathrm{ns}", width=6.2, size=34).move_to(RIGHT * 4.35 + DOWN * 1.80)

        self.play(FadeIn(cabin), Create(bottom), Create(top), Create(bracket), Write(hlabel), FadeIn(step1), run_time=RUN)
        self.play(Create(vertical), FadeIn(pulse), FadeIn(glow), run_time=RUN)

        up_path = Line(bottom.get_center(), top.get_center())
        down_path = Line(top.get_center(), bottom.get_center())
        self.play(
            MoveAlongPath(pulse, up_path),
            MoveAlongPath(glow, up_path),
            run_time=2.1,
            rate_func=linear,
        )
        self.play(Flash(top.get_center(), color=AMBER, flash_radius=0.35, line_length=0.12), run_time=RUN_FAST)
        self.play(FadeIn(eq1), run_time=RUN)
        self.play(FadeIn(eq2), run_time=RUN)
        self.play(
            MoveAlongPath(pulse, down_path),
            MoveAlongPath(glow, down_path),
            run_time=2.1,
            rate_func=linear,
        )
        self.play(Flash(bottom.get_center(), color=AMBER, flash_radius=0.35, line_length=0.12), run_time=RUN_FAST)
        self.play(FadeIn(eq3), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.play(FadeOut(VGroup(h, cabin, bottom, top, vertical, bracket, hlabel, pulse, glow, step1, eq1, eq2, eq3)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 08 — light clock in ground frame
    # -----------------------------------------------------------------
    def light_clock_ground_frame(self):
        h = self.header(
            8,
            "EXERCISE — STEP 2: THE SAME LIGHT CLOCK FROM THE GROUND",
            "Now the train moves at v = 0.60c while the light still moves at c.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        # Coordinate plane region on left.
        baseline = Line(LEFT * 7.0 + DOWN * 2.15, RIGHT * 0.8 + DOWN * 2.15, color=LIGHT, stroke_width=2)
        origin_mark = Line(DOWN * 2.28, DOWN * 2.02, color=MID, stroke_width=2).shift(LEFT * 5.20)
        origin_label = self.txt("x = 0", 18, BOLD, MID).next_to(origin_mark, DOWN, buff=0.05)

        # Scale: 1 scene unit = 1 metre for the triangle.
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
        pulse = always_redraw(lambda: Dot(
            np.array([pulse_x.get_value(), pulse_y.get_value(), 0]),
            radius=0.10, color=AMBER
        ))
        glow = always_redraw(lambda: Circle(
            radius=0.22, stroke_color=AMBER_SOFT, stroke_opacity=0.55
        ).move_to(pulse))

        self.play(Create(baseline), Create(origin_mark), FadeIn(origin_label), FadeIn(cabin), FadeIn(pulse), FadeIn(glow), run_time=RUN)

        motion_label = self.text_box("TRAIN SPEED: 0.60c", 3.8, 0.76, 23, BOLD).move_to(LEFT * 2.15 + UP * 1.65)
        self.play(FadeIn(motion_label), run_time=RUN)

        # First half trip: cabin moves +2.25 m, light moves diagonally 3.75 m.
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
        self.play(Flash(first_end, color=AMBER, flash_radius=0.34, line_length=0.12), run_time=RUN_FAST)

        # Second half: another 2.25 m horizontally, back to bottom mirror.
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
        self.play(Flash(second_end, color=AMBER, flash_radius=0.34, line_length=0.12), run_time=RUN_FAST)

        # Keep the geometric path, remove moving cabin so equations can enter cleanly.
        self.play(FadeOut(VGroup(cabin, pulse, glow, motion_label)), run_time=RUN_FAST)

        label_path = self.txt("The ground observer sees a longer diagonal path.", 24, BOLD).move_to(LEFT * 3.2 + UP * 1.92)
        self.play(FadeIn(label_path), run_time=RUN)

        # Right side: connect to general position equation.
        general = self.formula_box(r"X=X_0+vt", width=4.5, size=45).move_to(RIGHT * 4.30 + UP * 1.55)
        mirror_x = self.formula_box(r"x_{\mathrm{mirror}}=0+(0.60c)t", width=5.8, size=36).move_to(RIGHT * 4.30 + UP * 0.35)
        light_d = self.formula_box(r"d_{\mathrm{light}}=ct", width=4.7, size=40).move_to(RIGHT * 4.30 + DOWN * 0.82)
        clue = self.text_box("Use the right triangle for ONE half-trip.", 5.8, 0.80, 23, BOLD, PAPER).move_to(RIGHT * 4.30 + DOWN * 2.00)

        self.play(FadeIn(general), run_time=RUN)
        self.play(FadeIn(mirror_x), run_time=RUN)
        self.play(FadeIn(light_d), FadeIn(clue), run_time=RUN)
        self.wait(PAUSE_COPY)

        self.play(FadeOut(VGroup(h, baseline, origin_mark, origin_label, path_up, path_down, label_path, general, mirror_x, light_d, clue)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 09 — solve time dilation
    # -----------------------------------------------------------------
    def solve_relative_time(self):
        h = self.header(
            9,
            "EXERCISE — STEP 3: SOLVE FOR THE GROUND-FRAME TIME",
            "The same light pulse has speed c, but it travels a longer path.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        # Left geometric triangle with clean 2.25–3.00–3.75 proportions.
        A = LEFT * 5.35 + DOWN * 1.55
        B = LEFT * 3.10 + DOWN * 1.55
        C = LEFT * 3.10 + UP * 1.45
        tri = VGroup(
            Line(A, B, color=MID, stroke_width=3),
            Line(B, C, color=MID, stroke_width=3),
            Line(A, C, color=AMBER, stroke_width=4),
        )
        right_marker = Square(side_length=0.22, stroke_color=MID, stroke_width=1.8).move_to(B + LEFT * 0.11 + UP * 0.11)
        lab_h = self.mtex(r"H=3.0\,\mathrm{m}", 29).next_to(tri[1], RIGHT, buff=0.12)
        lab_x = self.mtex(r"0.60ct", 29).next_to(tri[0], DOWN, buff=0.10)
        lab_c = self.mtex(r"ct", 31, AMBER).next_to(tri[2], LEFT, buff=0.10)

        self.play(Create(tri), FadeIn(right_marker), Write(lab_h), Write(lab_x), Write(lab_c), run_time=RUN)

        # Right derivation, staged one line at a time.
        eq1 = self.formula_box(r"(ct)^2=H^2+(0.60ct)^2", width=7.2, size=39).move_to(RIGHT * 3.55 + UP * 1.58)
        eq2 = self.formula_box(r"c^2t^2(1-0.36)=9", width=6.4, size=39).move_to(RIGHT * 3.55 + UP * 0.45)
        eq3 = self.formula_box(r"0.64c^2t^2=9", width=5.6, size=41).move_to(RIGHT * 3.55 + DOWN * 0.68)
        eq4 = self.formula_box(r"ct=3.75\,\mathrm{m}", width=4.8, size=42).move_to(RIGHT * 3.55 + DOWN * 1.80)

        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(eq3, shift=UP * 0.08), run_time=RUN)
        self.play(FadeIn(eq4, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_READ)

        self.play(FadeOut(VGroup(tri, right_marker, lab_h, lab_x, lab_c, eq1, eq2, eq3, eq4)), run_time=RUN_FAST)

        # Time result screen.
        half = self.formula_box(
            r"t_{\frac12}=\frac{3.75}{3.00\times10^8}=12.5\,\mathrm{ns}",
            width=8.0, size=36
        ).shift(UP * 1.40)
        full = self.formula_box(
            r"\Delta t=2(12.5\,\mathrm{ns})=25.0\,\mathrm{ns}",
            width=7.2, size=38
        ).shift(UP * 0.12)
        compare = VGroup(
            self.text_box("TRAIN CLOCK", 4.2, 0.78, 22, BOLD),
            self.text_box("20.0 ns", 4.2, 0.90, 29, BOLD),
            self.text_box("GROUND CLOCK", 4.2, 0.78, 22, BOLD),
            self.text_box("25.0 ns", 4.2, 0.90, 29, BOLD),
        )
        left_pair = VGroup(compare[0], compare[1]).arrange(DOWN, buff=0.10).move_to(LEFT * 3.5 + DOWN * 1.45)
        right_pair = VGroup(compare[2], compare[3]).arrange(DOWN, buff=0.10).move_to(RIGHT * 3.5 + DOWN * 1.45)
        neq = self.mtex(r"20.0\,\mathrm{ns}\neq25.0\,\mathrm{ns}", 48).move_to(DOWN * 0.98)

        self.play(FadeIn(half), run_time=RUN)
        self.play(FadeIn(full), run_time=RUN)
        self.play(FadeIn(left_pair), FadeIn(right_pair), Write(neq), run_time=RUN_SLOW)
        self.wait(PAUSE_COPY)

        # Verify with gamma, but only after the geometry has done the teaching.
        self.play(FadeOut(VGroup(half, full, left_pair, right_pair, neq)), run_time=RUN_FAST)
        gamma1 = self.formula_box(r"\gamma=\frac{1}{\sqrt{1-(0.60)^2}}=1.25", width=7.0, size=39).shift(UP * 0.80)
        gamma2 = self.formula_box(r"\Delta t=\gamma\Delta t'=1.25(20.0)=25.0\,\mathrm{ns}", width=8.6, size=37).shift(DOWN * 0.55)
        conclusion = self.text_box("TIME IS NOT ABSOLUTE.", 6.2, 1.00, 31, BOLD, PAPER).shift(DOWN * 1.95)

        self.play(FadeIn(gamma1), run_time=RUN)
        self.play(FadeIn(gamma2), run_time=RUN)
        self.play(FadeIn(conclusion, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.play(FadeOut(VGroup(h, gamma1, gamma2, conclusion)), run_time=RUN_FAST)

    # -----------------------------------------------------------------
    # 10 — final summary
    # -----------------------------------------------------------------
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
            self.text_box("LIGHT CLOCK — 20 ns inside, 25 ns from ground", 8.2, 0.86, 25, BOLD),
        ).arrange(DOWN, buff=0.18).shift(LEFT * 2.75 + DOWN * 0.15)

        arrow = Arrow(LEFT * 0.2, RIGHT * 2.2, color=AMBER, stroke_width=5).shift(RIGHT * 1.0 + DOWN * 0.05)
        final = VGroup(
            self.txt("c stays invariant", 28, BOLD, AMBER),
            self.txt("↓", 33, BOLD, DARK),
            self.txt("space and time must adjust", 29, BOLD),
            self.txt("↓", 33, BOLD, DARK),
            self.txt("SPECIAL RELATIVITY", 34, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(RIGHT * 4.25 + DOWN * 0.15)

        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in rows], lag_ratio=0.16), run_time=RUN_SLOW)
        self.play(GrowArrow(arrow), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.06) for x in final], lag_ratio=0.16), run_time=RUN_SLOW)
        self.wait(PAUSE_COPY)

        exit_q = self.text_box(
            "EXIT QUESTION: Why do the two observers disagree about elapsed time?",
            11.4, 0.92, 26, BOLD, PAPER
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(exit_q, shift=UP * 0.08), run_time=RUN)
        self.wait(PAUSE_COPY)
