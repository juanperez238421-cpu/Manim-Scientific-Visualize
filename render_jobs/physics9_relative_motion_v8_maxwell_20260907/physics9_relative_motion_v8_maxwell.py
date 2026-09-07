#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Relative Motion V8 · Maxwell intuition first.

Goal
----
Start the class with real visible motion. Students first compare the same walker
from inside a moving bus and from the road. Then the lesson shifts to Maxwell:
light is an electromagnetic wave and Maxwell's theory predicts one propagation
speed in vacuum. No algebraic derivation is shown in this opener.

Target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D8D8D8"
PAPER = "#F4F4F4"
AMBER = "#D6A000"
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN = 0.9
RUN_FAST = 0.55
MOVE = 2.6
MOVE_LONG = 3.5
PAUSE = 1.25
PAUSE_READ = 1.8
PAUSE_LONG = 2.6


class Physics9RelativeMotionV8Maxwell(Scene):
    """Motion-first introduction to Galileo, Maxwell and the light-speed puzzle."""

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def txt(self, s, size=30, weight=NORMAL, color=INK):
        return Text(s, font_size=size, weight=weight, color=color)

    def fit(self, mob, max_w=14.0, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def label(self, text, width=4.0, height=0.72, size=23, color=INK):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.10,
                               stroke_color=color, stroke_width=2,
                               fill_color=WHITE, fill_opacity=0.96)
        t = self.fit(self.txt(text, size, BOLD, color), width - 0.35, height - 0.18)
        t.move_to(box)
        return VGroup(box, t)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    # ------------------------------------------------------------------
    # People and bus
    # ------------------------------------------------------------------
    def person(self, scale=1.0, gait=0, seated=False):
        head = Circle(radius=0.17 * scale, stroke_color=INK, stroke_width=2.2,
                      fill_color=WHITE, fill_opacity=1).shift(UP * 0.74 * scale)
        if seated:
            torso = Line(UP * 0.53 * scale, UP * 0.04 * scale, color=INK, stroke_width=5)
            arm = Line(UP * 0.34 * scale, RIGHT * 0.30 * scale + UP * 0.08 * scale,
                       color=INK, stroke_width=4)
            thigh = Line(UP * 0.04 * scale, RIGHT * 0.33 * scale + DOWN * 0.08 * scale,
                         color=INK, stroke_width=5)
            shin = Line(RIGHT * 0.33 * scale + DOWN * 0.08 * scale,
                        RIGHT * 0.33 * scale + DOWN * 0.52 * scale,
                        color=INK, stroke_width=5)
            return VGroup(head, torso, arm, thigh, shin)

        torso = Line(UP * 0.54 * scale, DOWN * 0.12 * scale, color=INK, stroke_width=5)
        if gait == 0:
            a1 = LEFT * 0.21 * scale + UP * 0.05 * scale
            a2 = RIGHT * 0.21 * scale + UP * 0.05 * scale
            l1 = LEFT * 0.14 * scale + DOWN * 0.60 * scale
            l2 = RIGHT * 0.14 * scale + DOWN * 0.60 * scale
        elif gait > 0:
            a1 = LEFT * 0.34 * scale + DOWN * 0.01 * scale
            a2 = RIGHT * 0.33 * scale + UP * 0.10 * scale
            l1 = LEFT * 0.31 * scale + DOWN * 0.58 * scale
            l2 = RIGHT * 0.28 * scale + DOWN * 0.48 * scale
        else:
            a1 = LEFT * 0.33 * scale + UP * 0.10 * scale
            a2 = RIGHT * 0.34 * scale + DOWN * 0.01 * scale
            l1 = LEFT * 0.28 * scale + DOWN * 0.48 * scale
            l2 = RIGHT * 0.31 * scale + DOWN * 0.58 * scale
        arm1 = Line(UP * 0.31 * scale, a1, color=INK, stroke_width=4)
        arm2 = Line(UP * 0.31 * scale, a2, color=INK, stroke_width=4)
        leg1 = Line(DOWN * 0.12 * scale, l1, color=INK, stroke_width=5)
        leg2 = Line(DOWN * 0.12 * scale, l2, color=INK, stroke_width=5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def walk_cycle(self, walker, dx=2.6, steps=8, duration=2.8):
        start = walker.get_center()
        base_h = self.person(1.0).height
        scale = walker.height / base_h
        for i in range(steps):
            pose = self.person(scale, 1 if i % 2 == 0 else -1)
            pose.move_to(start + RIGHT * dx * (i + 1) / steps)
            self.play(ReplacementTransform(walker, pose), run_time=duration / steps)
            walker = pose
        return walker

    def bus(self, width=8.7, height=2.35):
        body = RoundedRectangle(width=width, height=height, corner_radius=0.22,
                                stroke_color=INK, stroke_width=2.6,
                                fill_color=WHITE, fill_opacity=1)
        windows = VGroup()
        for frac in (-0.31, -0.10, 0.11, 0.31):
            w = RoundedRectangle(width=1.25, height=0.69, corner_radius=0.06,
                                 stroke_color=LIGHT, stroke_width=1.4,
                                 fill_color=PAPER, fill_opacity=1)
            w.move_to(body.get_center() + RIGHT * frac * width + UP * 0.50)
            windows.add(w)
        floor = Line(body.get_left() + RIGHT * 0.35 + DOWN * 0.72,
                     body.get_right() + LEFT * 0.35 + DOWN * 0.72,
                     color=LIGHT, stroke_width=2)
        wheels = VGroup()
        for frac in (-0.28, 0.28):
            tire = Circle(radius=0.21, stroke_color=INK, stroke_width=2.2,
                          fill_color=WHITE, fill_opacity=1)
            spoke1 = Line(LEFT * 0.14, RIGHT * 0.14, color=MID, stroke_width=1.4)
            spoke2 = Line(DOWN * 0.14, UP * 0.14, color=MID, stroke_width=1.4)
            wheel = VGroup(tire, spoke1, spoke2)
            wheel.move_to(body.get_center() + RIGHT * frac * width + DOWN * (height / 2 + 0.17))
            wheels.add(wheel)
        return VGroup(body, windows, floor, wheels)

    def roadside(self):
        road = Line(LEFT * 7.3 + DOWN * 2.0, RIGHT * 7.3 + DOWN * 2.0,
                    color=MID, stroke_width=2)
        dashes = VGroup(*[
            Line(LEFT * 0.25, RIGHT * 0.25, color=LIGHT, stroke_width=2)
            .move_to(RIGHT * x + DOWN * 2.30)
            for x in np.linspace(-7, 7, 12)
        ])
        trees = VGroup()
        for x in (-6.5, -2.8, 1.2, 5.3):
            trunk = Line(DOWN * 0.30, UP * 0.34, color=MID, stroke_width=3)
            crown = Circle(radius=0.28, stroke_color=MID, fill_color=WHITE, fill_opacity=1)
            crown.move_to(UP * 0.52)
            trees.add(VGroup(trunk, crown).move_to(RIGHT * x + DOWN * 1.20))
        return road, dashes, trees

    def pulse(self, start, end):
        glow = Line(start, end, color=AMBER, stroke_width=14).set_opacity(0.18)
        beam = Arrow(start, end, buff=0, color=AMBER, stroke_width=6,
                     max_tip_length_to_length_ratio=0.10)
        return VGroup(glow, beam)

    # ------------------------------------------------------------------
    # Lesson
    # ------------------------------------------------------------------
    def construct(self):
        self.cold_open()
        self.inside_view()
        self.road_view()
        self.galileo_idea()
        self.maxwell_intro()
        self.maxwell_light_speed()
        self.light_bus_test()
        self.final_question()

    def cold_open(self):
        q = self.label("HOW FAST IS THE WALKER?", 4.6, 0.78, 26).to_edge(UP, buff=0.25)
        road, dashes, trees = self.roadside()
        bus = self.bus().shift(DOWN * 0.18)
        seated = self.person(0.84, seated=True).move_to(bus.get_center() + LEFT * 2.55)
        walker = self.person(0.84, 1).move_to(bus.get_center() + LEFT * 0.85)
        self.add(road, dashes, trees, bus, seated, walker)
        self.play(FadeIn(q), run_time=RUN)
        self.play(trees.animate.shift(LEFT * 5.5), dashes.animate.shift(LEFT * 5.5),
                  *[w.animate.rotate(-TAU * 2.2) for w in bus[-1]],
                  run_time=MOVE_LONG, rate_func=linear)
        walker = self.walk_cycle(walker, dx=2.2, steps=8, duration=2.8)
        self.wait(PAUSE)
        self.clear_scene()

    def inside_view(self):
        title = self.label("VIEW FROM INSIDE THE BUS", 4.6, 0.76, 24).to_edge(UP, buff=0.25)
        bus = self.bus(9.6, 2.65).shift(DOWN * 0.20)
        seated = self.person(0.92, seated=True).move_to(bus.get_center() + LEFT * 3.0)
        walker = self.person(0.92, 1).move_to(bus.get_center() + LEFT * 1.30)
        self.play(FadeIn(title), FadeIn(bus), FadeIn(seated), FadeIn(walker), run_time=RUN)
        walker = self.walk_cycle(walker, dx=3.4, steps=10, duration=3.4)
        speed = self.label("THE WALKER: 2 m/s", 3.5, 0.74, 23).to_edge(DOWN, buff=0.40)
        self.play(FadeIn(speed, shift=UP * 0.10), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def road_view(self):
        title = self.label("VIEW FROM THE ROAD", 3.8, 0.76, 24).to_edge(UP, buff=0.25)
        road, dashes, trees = self.roadside()
        observer = self.person(0.72).move_to(RIGHT * 6.2 + DOWN * 0.9)
        obs_lab = self.txt("OBSERVER", 19, BOLD).next_to(observer, DOWN, buff=0.08)
        bus = self.bus(7.2, 2.0).move_to(LEFT * 4.7 + DOWN * 0.35)
        walker = self.person(0.69, 1).move_to(bus.get_center() + LEFT * 0.75)
        self.add(road, dashes, trees, observer, obs_lab)
        self.play(FadeIn(title), FadeIn(bus), FadeIn(walker), run_time=RUN)
        self.play(bus.animate.shift(RIGHT * 7.0), walker.animate.shift(RIGHT * 8.1),
                  *[w.animate.rotate(-TAU * 2.5) for w in bus[-1]],
                  run_time=MOVE_LONG, rate_func=linear)
        speed = self.label("THE SAME WALKER: 22 m/s", 4.3, 0.74, 23).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(speed), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    def galileo_idea(self):
        heading = self.txt("GALILEO'S IDEA", 38, BOLD).to_edge(UP, buff=0.55)
        bus = self.bus(8.4, 2.25).shift(DOWN * 0.35)
        seated = self.person(0.82, seated=True).move_to(bus.get_center() + LEFT * 2.4)
        walker = self.person(0.82, 1).move_to(bus.get_center() + LEFT * 0.7)
        line1 = self.txt("Inside a smoothly moving vehicle, ordinary mechanical motion behaves normally.", 27)
        line2 = self.txt("Different observers can describe the same motion with different velocities.", 28, BOLD)
        line1.next_to(heading, DOWN, buff=0.30)
        line2.to_edge(DOWN, buff=0.45)
        self.play(Write(heading), FadeIn(line1), FadeIn(bus), FadeIn(seated), FadeIn(walker), run_time=RUN)
        walker = self.walk_cycle(walker, dx=2.8, steps=8, duration=2.8)
        self.play(FadeIn(line2), run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_scene()

    def maxwell_intro(self):
        heading = self.txt("THEN MAXWELL CHANGED THE QUESTION", 38, BOLD).to_edge(UP, buff=0.50)
        statement = self.txt("Maxwell's theory connected electricity, magnetism and light.", 30, BOLD)
        statement.next_to(heading, DOWN, buff=0.28)

        x0, x1 = -5.3, 5.3
        electric = ParametricFunction(
            lambda t: np.array([t, 0.55 * np.sin(2.3 * t), 0]),
            t_range=[x0, x1], color=DARK, stroke_width=4,
        ).shift(DOWN * 0.55)
        magnetic = ParametricFunction(
            lambda t: np.array([t, 0.35 * np.sin(2.3 * t + PI / 2), 0]),
            t_range=[x0, x1], color=MID, stroke_width=3,
        ).shift(DOWN * 0.55)
        e_lab = self.txt("electric field", 22, BOLD, DARK).move_to(LEFT * 4.8 + DOWN * 2.45)
        m_lab = self.txt("magnetic field", 22, BOLD, MID).move_to(RIGHT * 4.7 + DOWN * 2.45)
        note = self.txt("A changing electric field and a changing magnetic field can travel together as a wave.", 25)
        note.to_edge(DOWN, buff=0.34)

        self.play(Write(heading), FadeIn(statement), run_time=RUN)
        self.play(Create(electric), Create(magnetic), FadeIn(e_lab), FadeIn(m_lab), run_time=1.8)
        self.play(electric.animate.shift(RIGHT * 1.2), magnetic.animate.shift(RIGHT * 1.2), run_time=1.4, rate_func=linear)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_scene()

    def maxwell_light_speed(self):
        heading = self.txt("MAXWELL'S LIGHT", 40, BOLD).to_edge(UP, buff=0.52)
        big1 = self.txt("LIGHT IS AN ELECTROMAGNETIC WAVE", 38, BOLD)
        big1.move_to(UP * 1.15)
        big2 = self.txt("IN VACUUM IT TRAVELS AT ABOUT 300,000 km/s", 37, BOLD, AMBER)
        big2.move_to(DOWN * 0.20)
        expl = VGroup(
            self.txt("Maxwell's theory predicts a specific propagation speed for electromagnetic waves.", 26),
            self.txt("It does not contain a different vacuum light speed for every moving observer.", 26, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.60)
        left = Dot(LEFT * 5.6 + DOWN * 2.75, radius=0.10, color=AMBER)
        ray = self.pulse(LEFT * 5.3 + DOWN * 2.75, RIGHT * 5.3 + DOWN * 2.75)
        self.play(Write(heading), run_time=RUN)
        self.play(FadeIn(big1), run_time=RUN)
        self.play(FadeIn(big2), run_time=RUN)
        self.play(FadeIn(left), GrowArrow(ray[1]), FadeIn(ray[0]), run_time=1.6)
        self.play(FadeIn(expl), run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_scene()

    def light_bus_test(self):
        title = self.txt("NOW REPLACE THE WALKER WITH LIGHT", 37, BOLD).to_edge(UP, buff=0.50)
        bus = self.bus(9.2, 2.55).shift(DOWN * 0.35)
        passenger = self.person(0.86, seated=True).move_to(bus.get_center() + LEFT * 2.65)
        source = Dot(bus.get_center() + LEFT * 1.45, radius=0.10, color=AMBER)
        inside = self.label("PASSENGER: SAME LIGHT SPEED", 4.7, 0.70, 21, AMBER)
        inside.move_to(LEFT * 3.7 + DOWN * 3.25)
        outside = self.label("ROAD OBSERVER: SAME LIGHT SPEED", 5.1, 0.70, 21, AMBER)
        outside.move_to(RIGHT * 3.6 + DOWN * 3.25)
        self.play(Write(title), FadeIn(bus), FadeIn(passenger), FadeIn(source), run_time=RUN)
        pulse = self.pulse(source.get_center(), bus.get_center() + RIGHT * 3.65)
        self.play(FadeIn(pulse[0]), GrowArrow(pulse[1]), run_time=1.8)
        self.play(FadeIn(inside), FadeIn(outside), run_time=RUN)
        contrast = self.txt("Walking speed changed with the observer.  Light speed does not.", 31, BOLD)
        contrast.move_to(UP * 2.55)
        self.play(FadeIn(contrast), run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_scene()

    def final_question(self):
        small = self.txt("GALILEO + MAXWELL", 24, BOLD, DARK).move_to(UP * 2.45)
        q1 = self.txt("ORDINARY MOTION DEPENDS ON THE OBSERVER.", 37, BOLD).move_to(UP * 1.05)
        q2 = self.txt("MAXWELL'S LIGHT SPEED DOES NOT.", 39, BOLD, AMBER).move_to(DOWN * 0.15)
        q3 = self.txt("So what must change?", 45, BOLD).move_to(DOWN * 1.55)
        q4 = self.txt("That is Einstein's next step.", 28, color=DARK).move_to(DOWN * 2.55)
        self.play(FadeIn(small), run_time=RUN)
        self.play(FadeIn(q1), run_time=RUN)
        self.play(FadeIn(q2), run_time=RUN)
        self.play(FadeIn(q3, shift=UP * 0.12), run_time=RUN)
        self.play(FadeIn(q4), run_time=RUN)
        self.wait(3.5)
