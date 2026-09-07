#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo-first dynamic bus relativity V6.

This scene inherits the validated V5 visual/math system but replaces the first
half with continuous physical animation: moving roadside parallax, walking
motion, synchronized inside/outside frames, a Galileo ball-toss thought
experiment, and a moving light pulse. The later Maxwell/Einstein mathematics
remain from V5.
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

BASE = Path(__file__).resolve().parents[1] / "physics9_bus_relativity_v5_20260907"
sys.path.insert(0, str(BASE))
from physics9_bus_relativity_v5 import *  # noqa: E402,F401,F403


class Physics9GalileoBusRelativityV6(Physics9BusRelativityV5):
    """Start the class with Galileo, then continue naturally to Einstein."""

    def construct(self):
        self.validate_data()
        self.cold_open_motion()
        self.galileo_principle()
        self.reference_frames()
        self.ordinary_velocity_addition()
        self.position_check()
        self.replace_with_light()
        self.maxwell_to_einstein()
        self.relativistic_velocity_addition()
        self.everyday_limit()
        self.summary()

    def roadside(self):
        ground = Line(LEFT * 8 + DOWN * 2.15, RIGHT * 8 + DOWN * 2.15,
                      color=MID, stroke_width=2)
        dashes = VGroup(*[
            Line(LEFT * 0.36, RIGHT * 0.36, color=LIGHT, stroke_width=5)
            .shift(RIGHT * x + DOWN * 2.48)
            for x in np.linspace(-7.2, 7.2, 10)
        ])
        buildings = VGroup()
        for i, x in enumerate(np.linspace(-7.2, 7.2, 8)):
            height = 1.0 + 0.28 * (i % 3)
            b = Rectangle(width=1.05, height=height, stroke_color=LIGHT,
                          stroke_width=1.3, fill_color=PAPER, fill_opacity=0.75)
            b.shift(RIGHT * x + DOWN * (2.15 - height / 2))
            buildings.add(b)
        poles = VGroup(*[
            Line(DOWN * 2.15, DOWN * 0.55, color=LIGHT, stroke_width=2)
            .shift(RIGHT * x)
            for x in (-5.8, -2.0, 1.8, 5.5)
        ])
        return VGroup(ground, dashes, buildings, poles)

    def alt_walker(self, scale=1.0):
        head = Circle(radius=0.18 * scale, stroke_color=INK, stroke_width=2.4,
                      fill_color=WHITE, fill_opacity=1).shift(UP * 0.72 * scale)
        torso = Line(UP * 0.52 * scale, DOWN * 0.10 * scale,
                     color=INK, stroke_width=5)
        arm1 = Line(UP * 0.30 * scale, RIGHT * 0.30 * scale + UP * 0.04 * scale,
                    color=INK, stroke_width=4)
        arm2 = Line(UP * 0.28 * scale, LEFT * 0.30 * scale + DOWN * 0.02 * scale,
                    color=INK, stroke_width=4)
        leg1 = Line(DOWN * 0.10 * scale, RIGHT * 0.30 * scale + DOWN * 0.56 * scale,
                    color=INK, stroke_width=5)
        leg2 = Line(DOWN * 0.10 * scale, LEFT * 0.26 * scale + DOWN * 0.48 * scale,
                    color=INK, stroke_width=5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def cold_open_motion(self):
        env = self.roadside()
        bus = self.bus(9.0, 2.35).shift(DOWN * 0.52)
        seated = self.person(0.82, seated=True).move_to(bus.get_center() + LEFT * 2.55)
        walker = self.person(0.84, walking=True).move_to(bus.get_center() + LEFT * 1.00)
        prompt = self.text_box("WATCH FIRST: HOW FAST IS THE WALKER?", 6.5, 0.78, 23)
        prompt.to_edge(UP, buff=0.30)

        self.add(env, bus, seated, walker)
        self.play(FadeIn(prompt), run_time=RUN_FAST)
        alt = self.alt_walker(0.84).move_to(walker.get_center() + RIGHT * 0.65)
        self.play(env[1:].animate.shift(LEFT * 2.3),
                  Transform(walker, alt),
                  run_time=1.55, rate_func=linear)
        normal = self.person(0.84, walking=True).move_to(walker.get_center() + RIGHT * 0.65)
        self.play(env[1:].animate.shift(LEFT * 2.3),
                  Transform(walker, normal),
                  run_time=1.55, rate_func=linear)

        q = self.fit(self.txt("One walker. Two observers. Two velocities.", 43, BOLD), 13.0)
        q.shift(UP * 2.45)
        self.play(ReplacementTransform(prompt, q), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def galileo_principle(self):
        title = VGroup(
            self.txt("GALILEO'S PRINCIPLE OF RELATIVITY", 44, BOLD),
            self.txt("Uniform straight-line motion cannot be detected by an internal mechanical experiment alone.",
                     24, NORMAL, DARK),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.30)
        self.play(Write(title), run_time=RUN_SLOW)

        left_box = RoundedRectangle(width=6.4, height=4.55, corner_radius=0.16,
                                    stroke_color=DARK, stroke_width=2,
                                    fill_color=WHITE, fill_opacity=1)
        right_box = left_box.copy()
        VGroup(left_box, right_box).arrange(RIGHT, buff=0.55).shift(DOWN * 0.65)
        left_lab = self.txt("BUS AT REST", 23, BOLD).next_to(left_box, UP, buff=0.12)
        right_lab = self.txt("BUS MOVING AT CONSTANT v", 23, BOLD).next_to(right_box, UP, buff=0.12)

        bus_l = self.bus(4.6, 1.50).move_to(left_box.get_center() + DOWN * 0.45)
        bus_r = self.bus(4.6, 1.50).move_to(right_box.get_center() + DOWN * 0.45)
        p_l = self.person(0.60, seated=True).move_to(bus_l.get_center() + LEFT * 1.15)
        p_r = self.person(0.60, seated=True).move_to(bus_r.get_center() + LEFT * 1.15)
        ball_l = Dot(bus_l.get_center() + RIGHT * 0.45, radius=0.09, color=INK)
        ball_r = Dot(bus_r.get_center() + RIGHT * 0.45, radius=0.09, color=INK)
        path_l = Line(ball_l.get_center(), ball_l.get_center() + UP * 1.35)
        path_r = Line(ball_r.get_center(), ball_r.get_center() + UP * 1.35)

        self.play(FadeIn(left_box), FadeIn(right_box), FadeIn(left_lab), FadeIn(right_lab),
                  FadeIn(bus_l), FadeIn(bus_r), FadeIn(p_l), FadeIn(p_r),
                  FadeIn(ball_l), FadeIn(ball_r), run_time=RUN)
        self.play(MoveAlongPath(ball_l, path_l), MoveAlongPath(ball_r, path_r),
                  run_time=1.25, rate_func=there_and_back)
        same = self.text_box("INSIDE: THE EXPERIMENT LOOKS THE SAME", 6.6, 0.82, 25)
        same.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(same), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def reference_frames(self):
        h = self.header(1, "INSIDE THE BUS: YOU MEASURE THE WALKER RELATIVE TO THE BUS",
                        "Because you move with the bus, the bus is at rest in your frame S'.")
        self.play(FadeIn(h), run_time=RUN_FAST)
        bus = self.bus(10.2, 2.55).shift(DOWN * 0.55)
        you = self.person(0.90, seated=True).move_to(bus.get_center() + LEFT * 3.10)
        walker = self.person(0.90, walking=True).move_to(bus.get_center() + LEFT * 1.15)
        self.play(FadeIn(bus), FadeIn(you), FadeIn(walker), run_time=RUN)

        start = walker.get_center().copy()
        alt = self.alt_walker(0.90).move_to(start + RIGHT * 0.90)
        self.play(Transform(walker, alt), run_time=0.85, rate_func=linear)
        normal = self.person(0.90, walking=True).move_to(start + RIGHT * 1.80)
        self.play(Transform(walker, normal), run_time=0.85, rate_func=linear)

        arrow = self.velocity_arrow(start + DOWN * 1.12,
                                    start + RIGHT * 2.2 + DOWN * 1.12,
                                    r"u'=2\,\mathrm{m/s}")
        result = self.text_box("INSIDE OBSERVER: 2 m/s", 5.0, 0.90, 28)
        result.move_to(RIGHT * 3.90 + UP * 1.90)
        self.play(GrowArrow(arrow[0]), Write(arrow[1]), FadeIn(result), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def ordinary_velocity_addition(self):
        h = self.header(2, "FROM THE ROAD: THE SAME WALKER HAS A DIFFERENT VELOCITY",
                        "The road observer sees 20 m/s from the bus plus 2 m/s from the walking motion.")
        self.play(FadeIn(h), run_time=RUN_FAST)
        env = self.roadside()
        bus = self.bus(6.4, 1.95).shift(LEFT * 4.35 + DOWN * 0.60)
        walker = self.person(0.72, walking=True).move_to(bus.get_center() + RIGHT * 0.20)
        observer = self.person(0.76).move_to(RIGHT * 5.65 + DOWN * 1.20)
        observer_lab = self.txt("ROAD OBSERVER", 19, BOLD).next_to(observer, UP, buff=0.08)
        self.add(env)
        self.play(FadeIn(bus), FadeIn(walker), FadeIn(observer), FadeIn(observer_lab), run_time=RUN)

        self.play(bus.animate.shift(RIGHT * 5.4),
                  walker.animate.shift(RIGHT * 6.25),
                  run_time=2.65, rate_func=linear)

        eq = self.formula_box(r"u=u'+v=2+20=22\,\mathrm{m/s}", 7.2, 1.05, 39)
        eq.move_to(UP * 1.90)
        r = self.text_box("ROAD OBSERVER: 22 m/s", 5.3, 0.90, 28)
        r.next_to(eq, DOWN, buff=0.28)
        self.play(FadeIn(eq), FadeIn(r), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def position_check(self):
        h = self.header(3, "SAME EVENT, DIFFERENT FRAME: CHECK IT WITH POSITION AND A TOSSED BALL",
                        "After 3 s the road sees 60 m for the bus and 66 m for the walker; inside, their separation is only 6 m.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        axis = NumberLine(x_range=[0, 70, 10], length=11.8, include_numbers=True,
                          font_size=24, color=MID).shift(UP * 1.15)
        bus_dot = Dot(axis.n2p(0), radius=0.10, color=INK)
        walker_dot = Dot(axis.n2p(0), radius=0.10, color=INK).shift(UP * 0.34)
        bus_lab = self.txt("BUS", 20, BOLD).next_to(bus_dot, DOWN, buff=0.10)
        walk_lab = self.txt("WALKER", 20, BOLD).next_to(walker_dot, UP, buff=0.10)
        self.play(Create(axis), FadeIn(bus_dot), FadeIn(walker_dot), FadeIn(bus_lab), FadeIn(walk_lab), run_time=RUN)
        self.play(bus_dot.animate.move_to(axis.n2p(60)), walker_dot.animate.move_to(axis.n2p(66) + UP * 0.34),
                  bus_lab.animate.next_to(axis.n2p(60), DOWN, buff=0.10),
                  walk_lab.animate.next_to(axis.n2p(66) + UP * 0.34, UP, buff=0.10),
                  run_time=2.35, rate_func=linear)

        eq = self.formula_box(r"X=X_0+vt\quad\Rightarrow\quad 60\,m,\ 66\,m,\ \Delta X=6\,m", 9.6, 1.0, 36)
        eq.move_to(DOWN * 0.20)
        self.play(FadeIn(eq), run_time=RUN)

        left = self.text_box("INSIDE: VERTICAL TOSS", 4.6, 0.74, 22).move_to(LEFT * 3.8 + DOWN * 1.35)
        right = self.text_box("ROAD: FORWARD PARABOLA", 4.6, 0.74, 22).move_to(RIGHT * 3.8 + DOWN * 1.35)
        self.play(FadeIn(left), FadeIn(right), run_time=RUN_FAST)
        l0 = LEFT * 3.8 + DOWN * 3.0
        r0 = RIGHT * 2.35 + DOWN * 3.0
        ball_l = Dot(l0, radius=0.08, color=INK)
        ball_r = Dot(r0, radius=0.08, color=INK)
        path_l = ParametricFunction(lambda t: l0 + UP * (1.3 * 4 * t * (1 - t)), t_range=[0,1], color=MID)
        path_r = ParametricFunction(lambda t: r0 + RIGHT * (2.9 * t) + UP * (1.3 * 4 * t * (1 - t)), t_range=[0,1], color=MID)
        self.play(FadeIn(ball_l), FadeIn(ball_r), Create(path_l), Create(path_r), run_time=RUN)
        self.play(MoveAlongPath(ball_l, path_l), MoveAlongPath(ball_r, path_r), run_time=1.9, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def replace_with_light(self):
        h = self.header(4, "NOW REPLACE THE WALKER WITH LIGHT",
                        "Galilean addition would suggest c + 20 m/s, but experiments give the same c to both inertial observers.")
        self.play(FadeIn(h), run_time=RUN_FAST)
        bus = self.bus(9.4, 2.35).shift(DOWN * 0.62)
        passenger = self.person(0.84, seated=True).move_to(bus.get_center() + LEFT * 2.55)
        start = bus.get_center() + LEFT * 1.35 + UP * 0.10
        pulse = Dot(start, radius=0.11, color=AMBER)
        beam = Line(start, start + RIGHT * 5.0, color=AMBER, stroke_width=7)
        self.play(FadeIn(bus), FadeIn(passenger), FadeIn(pulse), run_time=RUN)
        self.play(MoveAlongPath(pulse, beam), Create(beam), run_time=1.45, rate_func=linear)

        inside = self.text_box("PASSENGER MEASURES c", 4.7, 0.86, 27, stroke=AMBER)
        inside.move_to(LEFT * 3.6 + DOWN * 2.85)
        wrong = self.formula_box(r"c+20\,\mathrm{m/s}", 4.6, 1.0, 38)
        wrong.move_to(UP * 1.95)
        self.play(FadeIn(inside), FadeIn(wrong), run_time=RUN)
        self.play(Create(Cross(wrong, stroke_color=AMBER, stroke_width=6)), run_time=RUN)
        outside = self.text_box("ROAD OBSERVER ALSO MEASURES c", 6.1, 0.86, 26, stroke=AMBER)
        outside.move_to(RIGHT * 3.4 + DOWN * 2.85)
        self.play(FadeIn(outside), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    def summary(self):
        h = self.header(8, "GALILEO FIRST. EINSTEIN SECOND.",
                        "The observer defines the measured velocity; light is the case that forces us beyond simple Galilean addition.")
        self.play(FadeIn(h), run_time=RUN_FAST)
        cards = VGroup(
            self.text_box("1  FRAME\nInside or road?", 4.0, 1.30, 24),
            self.text_box("2  GALILEO\nu = u' + v", 4.0, 1.30, 24),
            self.text_box("3  LIGHT\nBoth measure c", 4.0, 1.30, 24, stroke=AMBER),
        ).arrange(RIGHT, buff=0.38).shift(UP * 0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.15), run_time=1.7)
        final = self.fit(self.txt("Same event. Different reference frame. Different measured velocity.", 32, BOLD), 13.5)
        final.move_to(DOWN * 1.75)
        light = self.fit(self.txt("Except light: every inertial observer measures c.", 30, BOLD, AMBER), 13.5)
        light.next_to(final, DOWN, buff=0.30)
        self.play(FadeIn(final), FadeIn(light), run_time=RUN)
        self.wait(PAUSE_FINAL)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN)


# Preview:
# manim -pql physics9_galileo_bus_relativity_v6.py Physics9GalileoBusRelativityV6 --disable_caching
# Final:
# manim -pqh physics9_galileo_bus_relativity_v6.py Physics9GalileoBusRelativityV6 --disable_caching
