#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Relative Motion, Maxwell, and Einstein
V4: 100% 2D, 100% English, simplified classroom narrative.

Core classroom sequence:
1) Relative motion inside a metro car.
2) The same walker seen by an observer in a building.
3) Use X = X0 + vt explicitly in both frames.
4) Historical bridge: Galileo/Newton -> Maxwell -> Einstein.
5) End with the conceptual reason special relativity is needed.

Final render:
    manim -pqh metro_relative_motion_history_v4.py Physics9RelativeMotionHistoryV4 \
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

INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D8D8D8"
PAPER = "#F5F5F5"
AMBER = "#D6A000"

RUN_FAST = 0.65
RUN = 1.00
RUN_SLOW = 1.45
PAUSE = 1.35
PAUSE_READ = 2.25
PAUSE_COPY = 3.00


class Physics9RelativeMotionHistoryV4(Scene):
    """Simple, projector-safe lesson on reference frames and the road to special relativity."""

    V_TRAIN = 20.0      # m/s = 72 km/h
    V_WALK = 2.0        # m/s relative to train
    V_GROUND = 22.0     # m/s
    T_OBS = 3.0         # s
    C = 3.00e8          # m/s

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs and kwargs["run_time"] is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

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
        kicker = self.txt(f"PHYSICS 9  •  RELATIVITY  •  {number:02d}", 20, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.1, 0.62)
        sub_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 14.0, 0.42)
        group = VGroup(kicker, title_m, sub_m).arrange(DOWN, buff=0.08)
        group.to_edge(UP, buff=0.20)
        rule = Line(LEFT * 7.15, RIGHT * 7.15, color=LIGHT, stroke_width=2)
        rule.next_to(group, DOWN, buff=0.10)
        return VGroup(group, rule)

    def formula_box(self, tex, width=6.2, height=1.05, size=40):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=DARK, stroke_width=1.8,
            fill_color=PAPER, fill_opacity=1.0,
        )
        eq = self.mtex(tex, size)
        self.fit(eq, width - 0.45, height - 0.25)
        eq.move_to(box)
        return VGroup(box, eq)

    def result_box(self, text, width=5.2, height=0.9):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=INK, stroke_width=2.2,
            fill_color=WHITE, fill_opacity=1.0,
        )
        t = self.fit(self.txt(text, 27, BOLD), width - 0.40, height - 0.18)
        t.move_to(box)
        return VGroup(box, t)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    def person(self, scale=1.0, walking=False, seated=False):
        head = Circle(radius=0.18 * scale, stroke_color=INK, stroke_width=2.4,
                      fill_color=WHITE, fill_opacity=1)
        if seated:
            head.shift(UP * 0.72 * scale)
            torso = Line(UP * 0.50 * scale, UP * 0.05 * scale, color=INK, stroke_width=5)
            arm = Line(UP * 0.34 * scale, RIGHT * 0.26 * scale + UP * 0.18 * scale,
                       color=INK, stroke_width=4)
            thigh = Line(UP * 0.05 * scale, RIGHT * 0.32 * scale + DOWN * 0.08 * scale,
                         color=INK, stroke_width=5)
            shin = Line(RIGHT * 0.32 * scale + DOWN * 0.08 * scale,
                        RIGHT * 0.32 * scale + DOWN * 0.48 * scale,
                        color=INK, stroke_width=5)
            return VGroup(head, torso, arm, thigh, shin)

        head.shift(UP * 0.72 * scale)
        torso = Line(UP * 0.52 * scale, DOWN * 0.10 * scale, color=INK, stroke_width=5)
        if walking:
            arm1 = Line(UP * 0.30 * scale, LEFT * 0.28 * scale + UP * 0.08 * scale,
                        color=INK, stroke_width=4)
            arm2 = Line(UP * 0.28 * scale, RIGHT * 0.30 * scale + DOWN * 0.02 * scale,
                        color=INK, stroke_width=4)
            leg1 = Line(DOWN * 0.10 * scale, LEFT * 0.28 * scale + DOWN * 0.58 * scale,
                        color=INK, stroke_width=5)
            leg2 = Line(DOWN * 0.10 * scale, RIGHT * 0.30 * scale + DOWN * 0.48 * scale,
                        color=INK, stroke_width=5)
        else:
            arm1 = Line(UP * 0.30 * scale, LEFT * 0.23 * scale + UP * 0.03 * scale,
                        color=INK, stroke_width=4)
            arm2 = Line(UP * 0.30 * scale, RIGHT * 0.23 * scale + UP * 0.03 * scale,
                        color=INK, stroke_width=4)
            leg1 = Line(DOWN * 0.10 * scale, LEFT * 0.18 * scale + DOWN * 0.58 * scale,
                        color=INK, stroke_width=5)
            leg2 = Line(DOWN * 0.10 * scale, RIGHT * 0.18 * scale + DOWN * 0.58 * scale,
                        color=INK, stroke_width=5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def train(self, width=9.5, height=2.35, exterior=False):
        body = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=INK, stroke_width=2.3,
            fill_color=WHITE, fill_opacity=1.0,
        )
        floor = Line(
            body.get_left() + RIGHT * 0.35 + DOWN * 0.73,
            body.get_right() + LEFT * 0.35 + DOWN * 0.73,
            color=LIGHT, stroke_width=2,
        )
        window_w = min(1.20, width / 7.2)
        windows = VGroup()
        for frac in (-0.34, -0.17, 0.0, 0.17, 0.34):
            win = RoundedRectangle(
                width=window_w, height=0.56, corner_radius=0.07,
                stroke_color=LIGHT, stroke_width=1.3,
                fill_color=PAPER, fill_opacity=1.0,
            )
            win.move_to(body.get_center() + RIGHT * (frac * width) + UP * 0.56)
            windows.add(win)
        door = VGroup(
            Line(UP * 0.86, DOWN * 0.86, color=LIGHT, stroke_width=1.4),
            Line(UP * 0.86, DOWN * 0.86, color=LIGHT, stroke_width=1.4),
        )
        door[0].shift(LEFT * 0.38)
        door[1].shift(RIGHT * 0.38)
        door.move_to(body)
        parts = [body, floor, windows, door]
        if exterior:
            wheels = VGroup(
                Circle(radius=0.16, stroke_color=INK, fill_color=WHITE, fill_opacity=1),
                Circle(radius=0.16, stroke_color=INK, fill_color=WHITE, fill_opacity=1),
            )
            wheels[0].move_to(body.get_center() + LEFT * (width * 0.28) + DOWN * (height / 2 + 0.14))
            wheels[1].move_to(body.get_center() + RIGHT * (width * 0.28) + DOWN * (height / 2 + 0.14))
            parts.append(wheels)
        return VGroup(*parts)

    def building(self):
        shell = Rectangle(width=2.15, height=4.4, stroke_color=DARK, stroke_width=2,
                          fill_color=PAPER, fill_opacity=0.65)
        wins = VGroup()
        for y in (1.25, 0.20, -0.85):
            for x in (-0.48, 0.48):
                r = Rectangle(width=0.62, height=0.62, stroke_color=LIGHT,
                              fill_color=WHITE, fill_opacity=1)
                r.move_to(shell.get_center() + RIGHT * x + UP * y)
                wins.add(r)
        roof = Line(shell.get_corner(UL), shell.get_corner(UR), color=INK, stroke_width=3)
        return VGroup(shell, wins, roof)

    def velocity_arrow(self, start, end, label, label_size=26, color=INK):
        arr = Arrow(start, end, buff=0, stroke_width=4, color=color,
                    max_tip_length_to_length_ratio=0.12)
        lab = self.mtex(label, label_size, color=color).next_to(arr, UP, buff=0.10)
        return VGroup(arr, lab)

    def observer_badge(self, text, center):
        box = RoundedRectangle(width=3.2, height=0.65, corner_radius=0.10,
                               stroke_color=DARK, stroke_width=1.6,
                               fill_color=WHITE, fill_opacity=1)
        t = self.fit(self.txt(text, 22, BOLD), 2.8, 0.40)
        t.move_to(box)
        return VGroup(box, t).move_to(center)

    def construct(self):
        self.opening()
        self.reference_frames()
        self.inside_train()
        self.from_building()
        self.compare_frames()
        self.classical_history()
        self.maxwell()
        self.tension()
        self.einstein()
        self.final_bridge()

    def opening(self):
        title = VGroup(
            self.txt("PHYSICS 9 • RELATIVITY", 24, BOLD, DARK),
            self.fit(self.txt("THE SAME MOTION CAN HAVE TWO VELOCITIES", 46, BOLD), 13.8),
            self.txt("Reference frames first. Light comes later.", 27, NORMAL, DARK),
        ).arrange(DOWN, buff=0.18).shift(UP * 2.45)

        tr = self.train(width=8.6, height=2.05, exterior=True).shift(LEFT * 1.6 + DOWN * 0.55)
        walker = self.person(0.86, walking=True).move_to(tr.get_center() + RIGHT * 0.75 + DOWN * 0.12)
        b = self.building().scale(0.72).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.70)
        obs = self.person(0.62).move_to(b.get_center() + UP * 0.20)
        ground = Line(LEFT * 7.2 + DOWN * 2.05, RIGHT * 7.2 + DOWN * 2.05,
                      color=MID, stroke_width=2)

        self.play(Write(title), run_time=RUN_SLOW)
        self.play(Create(ground), FadeIn(tr), FadeIn(walker), FadeIn(b), FadeIn(obs), run_time=RUN)
        arrow = self.velocity_arrow(LEFT * 4.0 + DOWN * 2.55,
                                    LEFT * 0.5 + DOWN * 2.55,
                                    r"20\,\mathrm{m/s}")
        self.play(GrowArrow(arrow[0]), Write(arrow[1]), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def reference_frames(self):
        h = self.header(1, "WHO IS MEASURING THE MOTION?",
                        "Velocity is always measured relative to a reference frame.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        tr = self.train(width=8.9, height=2.20).move_to(LEFT * 2.1 + DOWN * 0.15)
        you = self.person(0.82, seated=True).move_to(tr.get_center() + LEFT * 2.4 + DOWN * 0.02)
        walker = self.person(0.82, walking=True).move_to(tr.get_center() + RIGHT * 0.25 + DOWN * 0.02)
        b = self.building().scale(0.63).to_edge(RIGHT, buff=0.52).shift(DOWN * 0.35)
        outside = self.person(0.56).move_to(b.get_center() + UP * 0.20)

        badge1 = self.observer_badge("FRAME S' — INSIDE THE TRAIN", LEFT * 3.5 + DOWN * 2.45)
        badge2 = self.observer_badge("FRAME S — BUILDING / GROUND", RIGHT * 4.8 + DOWN * 2.45)

        self.play(FadeIn(tr), FadeIn(you), FadeIn(walker), FadeIn(b), FadeIn(outside), run_time=RUN)
        self.play(FadeIn(badge1), FadeIn(badge2), run_time=RUN)
        eq = self.formula_box(r"X=X_0+vt", width=4.2, size=46).move_to(UP * 1.90)
        self.play(FadeIn(eq), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def inside_train(self):
        h = self.header(2, "INSIDE THE TRAIN: THE TRAIN IS YOUR REFERENCE FRAME",
                        "You are seated. The walker moves at 2 m/s relative to you.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        tr = self.train(width=11.0, height=2.55).shift(DOWN * 0.35)
        you = self.person(0.95, seated=True).move_to(tr.get_center() + LEFT * 3.75 + DOWN * 0.04)
        walker = self.person(0.95, walking=True).move_to(tr.get_center() + LEFT * 1.20 + DOWN * 0.04)
        you_lab = self.txt("YOU", 21, BOLD).next_to(you, DOWN, buff=0.10)
        walk_lab = self.txt("WALKER", 21, BOLD).next_to(walker, DOWN, buff=0.10)

        self.play(FadeIn(tr), FadeIn(you), FadeIn(walker), FadeIn(you_lab), FadeIn(walk_lab), run_time=RUN)
        eq = self.formula_box(r"X'=X'_0+v't", width=5.3, size=42).to_edge(RIGHT, buff=0.55).shift(UP * 1.35)
        self.play(FadeIn(eq), run_time=RUN)

        start = walker.get_center().copy()
        self.play(walker.animate.shift(RIGHT * 4.6), walk_lab.animate.shift(RIGHT * 4.6),
                  run_time=3.0, rate_func=linear)
        dist = DoubleArrow(start + DOWN * 1.18, walker.get_center() + DOWN * 1.18,
                           buff=0, color=MID, stroke_width=2.6)
        dlab = self.txt("6 m in 3 s", 24, BOLD).next_to(dist, DOWN, buff=0.10)
        self.play(GrowFromCenter(dist), FadeIn(dlab), run_time=RUN)

        sub = self.formula_box(r"X'=0+(2)(3)=6\,\mathrm{m}", width=5.3, size=37)
        sub.next_to(eq, DOWN, buff=0.20)
        result = self.result_box("INSIDE TRAIN: 2 m/s", width=5.3).next_to(sub, DOWN, buff=0.20)
        self.play(FadeIn(sub), FadeIn(result), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    def from_building(self):
        h = self.header(3, "FROM THE BUILDING: THE TRAIN AND THE WALKER BOTH MOVE",
                        "The train moves at 20 m/s. The walker also moves 2 m/s inside the train.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        ground = Line(LEFT * 7.2 + DOWN * 2.0, RIGHT * 7.2 + DOWN * 2.0,
                      color=MID, stroke_width=2)
        b = self.building().scale(0.78).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.25)
        obs = self.person(0.65).move_to(b.get_center() + UP * 0.18)
        lab = self.txt("BUILDING OBSERVER", 21, BOLD).next_to(b, DOWN, buff=0.10)

        tr = self.train(width=6.9, height=1.90, exterior=True).move_to(LEFT * 4.7 + DOWN * 0.55)
        walker = self.person(0.70, walking=True).move_to(tr.get_center() + LEFT * 0.75 + DOWN * 0.05)
        self.play(Create(ground), FadeIn(b), FadeIn(obs), FadeIn(lab), FadeIn(tr), FadeIn(walker), run_time=RUN)

        vadd = self.formula_box(
            r"v_{\mathrm{walker,ground}}=20+2=22\,\mathrm{m/s}",
            width=7.2, size=36
        ).move_to(LEFT * 1.3 + UP * 1.55)
        self.play(FadeIn(vadd), run_time=RUN)

        self.play(
            tr.animate.shift(RIGHT * 5.7),
            walker.animate.shift(RIGHT * 6.25),
            run_time=3.2, rate_func=linear
        )
        self.wait(PAUSE)

        self.play(FadeOut(vadd), run_time=RUN_FAST)
        positions = VGroup(
            self.formula_box(r"X_{\mathrm{train}}=0+(20)(3)=60\,\mathrm{m}", width=6.0, size=33),
            self.formula_box(r"X_{\mathrm{walker}}=0+(22)(3)=66\,\mathrm{m}", width=6.0, size=33),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 2.0 + UP * 1.25)
        self.play(FadeIn(positions[0]), run_time=RUN)
        self.play(FadeIn(positions[1]), run_time=RUN)

        diff = self.result_box("AFTER 3 s: 66 m − 60 m = 6 m", width=6.0)
        diff.next_to(positions, DOWN, buff=0.20)
        self.play(FadeIn(diff), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    def compare_frames(self):
        h = self.header(4, "SAME WALKER. TWO CORRECT VELOCITIES.",
                        "Nothing contradictory happened: the observers used different reference frames.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        divider = Line(UP * 2.25, DOWN * 2.65, color=LIGHT, stroke_width=2)
        left_title = self.txt("TRAIN FRAME S'", 27, BOLD).move_to(LEFT * 4.1 + UP * 1.75)
        right_title = self.txt("BUILDING FRAME S", 27, BOLD).move_to(RIGHT * 4.1 + UP * 1.75)

        p1 = self.person(1.15, walking=True).move_to(LEFT * 4.1 + UP * 0.35)
        p2 = self.person(1.15, walking=True).move_to(RIGHT * 4.1 + UP * 0.35)
        r1 = self.result_box("2 m/s", width=3.6).move_to(LEFT * 4.1 + DOWN * 1.15)
        r2 = self.result_box("22 m/s", width=3.6).move_to(RIGHT * 4.1 + DOWN * 1.15)

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), FadeIn(p1), FadeIn(p2), run_time=RUN)
        self.play(FadeIn(r1), FadeIn(r2), run_time=RUN)
        statement = self.fit(self.txt(
            "CLASSICAL RELATIVITY: measured motion depends on the observer's frame.",
            31, BOLD
        ), 13.8).to_edge(DOWN, buff=0.45)
        self.play(Write(statement), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def classical_history(self):
        h = self.header(5, "GALILEO AND NEWTON: CLASSICAL MECHANICS",
                        "For ordinary motion, Galilean velocity addition works extremely well.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        years = self.txt("GALILEO  →  NEWTON 1687", 34, BOLD).shift(UP * 1.65)
        eq = self.formula_box(r"v=v'+V", width=4.8, size=50).shift(UP * 0.45)
        bullets = VGroup(
            self.txt("• The laws of mechanics work in inertial frames.", 28),
            self.txt("• Newtonian time is treated as universal.", 28),
            self.txt("• Velocities add and subtract between frames.", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).shift(DOWN * 1.20)
        self.play(Write(years), FadeIn(eq), run_time=RUN)
        self.play(*[FadeIn(b, shift=UP * 0.10) for b in bullets], run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def maxwell(self):
        h = self.header(6, "JAMES CLERK MAXWELL: LIGHT IS ELECTROMAGNETISM",
                        "In the 1860s Maxwell unified electricity and magnetism.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        name = self.txt("JAMES CLERK MAXWELL", 38, BOLD).shift(UP * 1.70)
        sentence = self.fit(self.txt(
            "Maxwell's equations predict electromagnetic waves with a fixed vacuum wave speed.",
            27
        ), 13.2).shift(UP * 1.05)

        axis = Line(LEFT * 5.5, RIGHT * 5.5, color=MID, stroke_width=2).shift(DOWN * 0.55)
        wave = ParametricFunction(
            lambda t: np.array([t, 0.55 * np.sin(2.3 * t), 0]),
            t_range=[-5.0, 5.0],
            color=AMBER, stroke_width=4,
        ).shift(DOWN * 0.55)
        cbox = self.formula_box(r"c\approx 3.00\times10^8\,\mathrm{m/s}",
                                width=6.0, size=42).shift(DOWN * 2.00)

        self.play(Write(name), FadeIn(sentence), run_time=RUN)
        self.play(Create(axis), Create(wave), run_time=RUN_SLOW)
        self.play(FadeIn(cbox), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def tension(self):
        h = self.header(7, "THE PROBLEM: CLASSICAL VELOCITY ADDITION MEETS MAXWELL",
                        "Galilean kinematics and Maxwell electromagnetism do not transform the same way.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        left = RoundedRectangle(width=6.2, height=4.3, corner_radius=0.16,
                                stroke_color=DARK, stroke_width=2,
                                fill_color=WHITE, fill_opacity=1).shift(LEFT * 3.45 + DOWN * 0.20)
        right = left.copy().shift(RIGHT * 6.90)

        lt = self.txt("GALILEO / NEWTON", 29, BOLD).move_to(left.get_top() + DOWN * 0.45)
        rt = self.txt("MAXWELL", 29, BOLD).move_to(right.get_top() + DOWN * 0.45)
        leq = self.mtex(r"u=u'+V", 45).move_to(left.get_center() + UP * 0.35)
        ltxt = self.fit(self.txt("Applied to light, this would suggest c + V or c − V.", 24),
                        5.45).move_to(left.get_center() + DOWN * 0.85)
        req = self.mtex(r"c=\mathrm{constant\ wave\ speed}", 38).move_to(right.get_center() + UP * 0.35)
        rtxt = self.fit(self.txt("Maxwell's equations are not Galilean-invariant.", 24),
                        5.45).move_to(right.get_center() + DOWN * 0.85)

        self.play(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=RUN)
        self.play(Write(leq), FadeIn(ltxt), run_time=RUN)
        self.play(Write(req), FadeIn(rtxt), run_time=RUN)
        conflict = self.fit(self.txt(
            "A NEW KINEMATICS WAS NEEDED.",
            34, BOLD
        ), 11.5).to_edge(DOWN, buff=0.38)
        self.play(Write(conflict), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def einstein(self):
        h = self.header(8, "EINSTEIN 1905: RECONCILING RELATIVITY WITH ELECTROMAGNETISM",
                        "Einstein did not discard Maxwell; he changed our ideas of space and time.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        title = self.txt("ALBERT EINSTEIN • 1905", 36, BOLD).shift(UP * 1.80)
        p1 = self.result_box("1. Same laws of physics in every inertial frame.", width=10.8, height=0.95)
        p2 = self.result_box("2. Every inertial observer measures the same vacuum light speed c.", width=10.8, height=0.95)
        posts = VGroup(p1, p2).arrange(DOWN, buff=0.25).shift(UP * 0.45)
        consequence = self.fit(self.txt(
            "If c does not change between frames, space and time cannot both remain absolute.",
            30, BOLD
        ), 13.4).shift(DOWN * 1.35)
        bridge = self.txt("This is the doorway to SPECIAL RELATIVITY.", 29, BOLD, DARK).shift(DOWN * 2.25)

        self.play(Write(title), run_time=RUN)
        self.play(FadeIn(posts[0]), run_time=RUN)
        self.play(FadeIn(posts[1]), run_time=RUN)
        self.play(Write(consequence), run_time=RUN_SLOW)
        self.play(FadeIn(bridge), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    def final_bridge(self):
        h = self.header(9, "ONE STORY: FROM A WALKER TO SPECIAL RELATIVITY",
                        "Start with reference frames. Then ask what happens when the moving signal is light.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        tr = self.train(width=8.5, height=2.10).move_to(LEFT * 2.7 + UP * 0.15)
        walker = self.person(0.80, walking=True).move_to(tr.get_center() + RIGHT * 0.20)
        b = self.building().scale(0.62).to_edge(RIGHT, buff=0.55).shift(UP * 0.05)
        obs = self.person(0.55).move_to(b.get_center() + UP * 0.18)
        self.play(FadeIn(tr), FadeIn(walker), FadeIn(b), FadeIn(obs), run_time=RUN)

        matter = VGroup(
            self.txt("WALKER", 25, BOLD),
            self.txt("Train frame: 2 m/s", 25),
            self.txt("Building frame: 22 m/s", 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(LEFT * 4.65 + DOWN * 2.05)

        light = VGroup(
            self.txt("LIGHT", 25, BOLD),
            self.mtex(r"c\ \mathrm{inside}", 31),
            self.mtex(r"c\ \mathrm{outside}", 31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.55 + DOWN * 2.05)

        self.play(FadeIn(matter), run_time=RUN)
        pulse = Circle(radius=0.22, color=AMBER, stroke_width=4).move_to(walker.get_center() + RIGHT * 0.40)
        self.play(FadeIn(pulse), pulse.animate.scale(5.0), run_time=2.0)
        self.play(FadeIn(light), run_time=RUN)

        final = self.fit(self.txt(
            "RELATIVITY: measurements depend on the frame — the laws of physics do not.",
            31, BOLD
        ), 13.6).to_edge(DOWN, buff=0.20)
        self.play(Write(final), run_time=RUN_SLOW)
        self.wait(PAUSE_COPY)
