#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Relative Motion V7
INTUITION FIRST: Galileo before Einstein, no equations.

Purpose
-------
A classroom opener built around real visible motion rather than formula slides.
Students first *see* why the same motion receives different measured velocities
in different reference frames.

Sequence
--------
0. Cold open: a moving bus, moving scenery, walking passenger.
1. "Who is moving?" — reference frames by direct observation.
2. Galileo's principle of relativity using a tossed ball inside a smooth bus.
3. Inside frame: walker moves at 2 m/s relative to the bus.
4. Road frame: bus moves at 20 m/s; walker is measured at 22 m/s.
5. Split-screen replay: same event, two observers, two measured velocities.
6. Ball replay: vertical path inside, forward curved path from the road.
7. Replace walker with light: both observers still measure the same light speed.
8. Closing intuition map: Galileo first, Einstein next.

No algebraic derivations are shown in this version.
Compatible target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

# -----------------------------------------------------------------------------
# Render configuration
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

# -----------------------------------------------------------------------------
# Visual system
# -----------------------------------------------------------------------------
INK = BLACK
DARK = "#303030"
MID = "#787878"
LIGHT = "#D8D8D8"
PAPER = "#F5F5F5"
ROAD = "#A8A8A8"
AMBER = "#D6A000"
SKY = "#ECECEC"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_FAST = 0.55
RUN = 0.90
RUN_SLOW = 1.25
MOVE = 2.20
MOVE_LONG = 3.20
PAUSE_SHORT = 0.65
PAUSE_READ = 1.50
PAUSE_EXPLAIN = 2.20
PAUSE_FINAL = 3.00


class Physics9RelativeMotionV7(Scene):
    """Galileo-first, motion-first introduction to relative motion."""

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Typography / layout
    # -------------------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=INK):
        return Text(content, font_size=size, weight=weight, color=color)

    def fit(self, mob, max_w=14.2, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        kicker = self.txt(f"PHYSICS 9  •  RELATIVE MOTION  •  {number:02d}", 18, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.0, 0.62)
        subtitle_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 14.0, 0.45)
        group = VGroup(kicker, title_m, subtitle_m).arrange(DOWN, buff=0.06)
        group.to_edge(UP, buff=0.18)
        rule = Line(LEFT * 7.2, RIGHT * 7.2, color=LIGHT, stroke_width=2)
        rule.next_to(group, DOWN, buff=0.09)
        return VGroup(group, rule)

    def label_box(self, text, width=3.6, height=0.72, size=23, color=INK, fill=WHITE):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=color,
            stroke_width=2,
            fill_color=fill,
            fill_opacity=1,
        )
        label = self.fit(self.txt(text, size, BOLD, color), width - 0.32, height - 0.18)
        label.move_to(box)
        return VGroup(box, label)

    def statement(self, text, y=-3.15, size=28, color=INK):
        t = self.fit(self.txt(text, size, BOLD, color), 13.6, 0.65)
        t.move_to(UP * y)
        return t

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_FAST)

    # -------------------------------------------------------------------------
    # People
    # -------------------------------------------------------------------------
    def person(self, scale=1.0, gait=0, seated=False):
        """Simple articulated pictogram. gait=-1/0/+1 changes walking pose."""
        head = Circle(
            radius=0.17 * scale,
            stroke_color=INK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1,
        ).shift(UP * 0.74 * scale)

        if seated:
            torso = Line(UP * 0.53 * scale, UP * 0.03 * scale, color=INK, stroke_width=5.2)
            upper_arm = Line(UP * 0.34 * scale, RIGHT * 0.23 * scale + UP * 0.18 * scale,
                             color=INK, stroke_width=4.2)
            forearm = Line(RIGHT * 0.23 * scale + UP * 0.18 * scale,
                           RIGHT * 0.38 * scale + UP * 0.02 * scale,
                           color=INK, stroke_width=4.2)
            thigh = Line(UP * 0.03 * scale, RIGHT * 0.33 * scale + DOWN * 0.08 * scale,
                         color=INK, stroke_width=5.0)
            shin = Line(RIGHT * 0.33 * scale + DOWN * 0.08 * scale,
                        RIGHT * 0.33 * scale + DOWN * 0.51 * scale,
                        color=INK, stroke_width=5.0)
            return VGroup(head, torso, upper_arm, forearm, thigh, shin)

        torso = Line(UP * 0.54 * scale, DOWN * 0.12 * scale, color=INK, stroke_width=5.2)

        if gait == 0:
            arm1_end = LEFT * 0.21 * scale + UP * 0.05 * scale
            arm2_end = RIGHT * 0.21 * scale + UP * 0.05 * scale
            leg1_end = LEFT * 0.14 * scale + DOWN * 0.60 * scale
            leg2_end = RIGHT * 0.14 * scale + DOWN * 0.60 * scale
        elif gait > 0:
            arm1_end = LEFT * 0.34 * scale + DOWN * 0.01 * scale
            arm2_end = RIGHT * 0.33 * scale + UP * 0.10 * scale
            leg1_end = LEFT * 0.31 * scale + DOWN * 0.58 * scale
            leg2_end = RIGHT * 0.28 * scale + DOWN * 0.48 * scale
        else:
            arm1_end = LEFT * 0.33 * scale + UP * 0.10 * scale
            arm2_end = RIGHT * 0.34 * scale + DOWN * 0.01 * scale
            leg1_end = LEFT * 0.28 * scale + DOWN * 0.48 * scale
            leg2_end = RIGHT * 0.31 * scale + DOWN * 0.58 * scale

        arm1 = Line(UP * 0.31 * scale, arm1_end, color=INK, stroke_width=4.2)
        arm2 = Line(UP * 0.31 * scale, arm2_end, color=INK, stroke_width=4.2)
        leg1 = Line(DOWN * 0.12 * scale, leg1_end, color=INK, stroke_width=5.0)
        leg2 = Line(DOWN * 0.12 * scale, leg2_end, color=INK, stroke_width=5.0)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def walk_cycle(self, walker, displacement=RIGHT * 2.2, steps=6, run_time=2.4):
        """Animate translation plus alternating articulated walking poses."""
        start = walker.get_center()
        scale = walker.height / self.person(1.0, 0).height
        for i in range(steps):
            gait = 1 if i % 2 == 0 else -1
            nxt = self.person(scale, gait)
            alpha = (i + 1) / steps
            nxt.move_to(start + displacement * alpha)
            self.play(ReplacementTransform(walker, nxt), run_time=run_time / steps)
            walker = nxt
        return walker

    # -------------------------------------------------------------------------
    # Bus and environment
    # -------------------------------------------------------------------------
    def bus(self, width=8.4, height=2.35, windows=True, wheels=True):
        body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.22,
            stroke_color=INK,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1,
        )
        front = Arc(
            radius=0.52,
            start_angle=-PI / 2,
            angle=PI / 2,
            color=INK,
            stroke_width=2.3,
        ).stretch_to_fit_height(height * 0.92).move_to(body.get_right() + LEFT * 0.20)

        glass = VGroup()
        if windows:
            for frac in (-0.31, -0.10, 0.11, 0.31):
                win = RoundedRectangle(
                    width=min(1.35, width / 6.0),
                    height=0.70,
                    corner_radius=0.06,
                    stroke_color=LIGHT,
                    stroke_width=1.4,
                    fill_color=PAPER,
                    fill_opacity=1,
                )
                win.move_to(body.get_center() + RIGHT * (frac * width) + UP * 0.50)
                glass.add(win)

        floor = Line(
            body.get_left() + RIGHT * 0.35 + DOWN * 0.72,
            body.get_right() + LEFT * 0.40 + DOWN * 0.72,
            color=LIGHT,
            stroke_width=2,
        )

        wheel_group = VGroup()
        if wheels:
            for frac in (-0.28, 0.28):
                tire = Circle(radius=0.21, stroke_color=INK, stroke_width=2.2,
                              fill_color=WHITE, fill_opacity=1)
                hub = Dot(radius=0.045, color=INK)
                spoke1 = Line(LEFT * 0.14, RIGHT * 0.14, color=MID, stroke_width=1.4)
                spoke2 = Line(DOWN * 0.14, UP * 0.14, color=MID, stroke_width=1.4)
                wheel = VGroup(tire, hub, spoke1, spoke2)
                wheel.move_to(body.get_center() + RIGHT * (frac * width)
                              + DOWN * (height / 2 + 0.17))
                wheel_group.add(wheel)

        return VGroup(body, front, glass, floor, wheel_group)

    def roadside(self, width=15.5, y=-2.10):
        road = Line(LEFT * width / 2 + UP * y, RIGHT * width / 2 + UP * y,
                    color=ROAD, stroke_width=2.2)
        dashes = VGroup()
        for x in np.linspace(-7, 7, 11):
            dashes.add(Line(LEFT * 0.25, RIGHT * 0.25, color=LIGHT, stroke_width=2)
                       .move_to(RIGHT * x + UP * (y - 0.28)))
        return VGroup(road, dashes)

    def scenery(self):
        """Layered, simple scenery for parallax."""
        far = VGroup()
        for x in (-6.5, -3.8, -0.5, 2.6, 5.6):
            building = Rectangle(
                width=1.0 + 0.15 * ((x + 7) % 3),
                height=1.4 + 0.25 * ((x + 5) % 2),
                stroke_color=LIGHT,
                stroke_width=1.2,
                fill_color=PAPER,
                fill_opacity=0.55,
            ).move_to(RIGHT * x + DOWN * 1.05)
            far.add(building)

        near = VGroup()
        for x in (-6.8, -2.8, 1.5, 5.2):
            trunk = Line(DOWN * 0.35, UP * 0.38, color=MID, stroke_width=3)
            crown = Circle(radius=0.30, stroke_color=MID, stroke_width=1.5,
                           fill_color=WHITE, fill_opacity=1).move_to(UP * 0.56)
            tree = VGroup(trunk, crown).move_to(RIGHT * x + DOWN * 1.30)
            near.add(tree)

        return far, near

    def speed_tag(self, text, center, width=2.7):
        return self.label_box(text, width=width, height=0.68, size=22).move_to(center)

    # -------------------------------------------------------------------------
    # Motion helpers
    # -------------------------------------------------------------------------
    def spin_wheels(self, bus, turns=2.5):
        wheels = bus[-1]
        return [wheel.animate.rotate(-TAU * turns) for wheel in wheels]

    def moving_bus_camera(self, duration=3.0):
        """Bus stays central while the world streams backward."""
        road = self.roadside()
        far, near = self.scenery()
        bus = self.bus(8.5, 2.30).shift(DOWN * 0.25)
        seated = self.person(0.83, seated=True).move_to(bus.get_center() + LEFT * 2.65 + DOWN * 0.03)
        walker = self.person(0.83, gait=1).move_to(bus.get_center() + LEFT * 0.75 + DOWN * 0.03)

        self.add(far, near, road, bus, seated, walker)
        self.play(
            far.animate.shift(LEFT * 4.0),
            near.animate.shift(LEFT * 6.2),
            road[1].animate.shift(LEFT * 5.5),
            *self.spin_wheels(bus, 2.0),
            run_time=duration,
            rate_func=linear,
        )
        return bus, seated, walker, far, near, road

    def ball(self, center, radius=0.09, color=INK):
        return Dot(center, radius=radius, color=color)

    # -------------------------------------------------------------------------
    # Orchestration
    # -------------------------------------------------------------------------
    def construct(self):
        self.cold_open()
        self.who_is_moving()
        self.galileo_principle()
        self.inside_frame()
        self.road_frame()
        self.split_replay()
        self.ball_two_frames()
        self.light_surprise()
        self.closing()

    # -------------------------------------------------------------------------
    # 00 — Cold open
    # -------------------------------------------------------------------------
    def cold_open(self):
        question = self.label_box("WATCH FIRST: HOW FAST IS THE WALKER?", 6.2, 0.82, 25)
        question.to_edge(UP, buff=0.28)
        self.play(FadeIn(question, shift=DOWN * 0.12), run_time=RUN)

        road = self.roadside()
        far, near = self.scenery()
        bus = self.bus(8.7, 2.35).shift(DOWN * 0.25)
        seated = self.person(0.86, seated=True).move_to(bus.get_center() + LEFT * 2.65 + DOWN * 0.02)
        walker = self.person(0.86, gait=1).move_to(bus.get_center() + LEFT * 1.0 + DOWN * 0.02)

        self.play(FadeIn(far), FadeIn(near), Create(road), FadeIn(bus), FadeIn(seated), FadeIn(walker),
                  run_time=RUN)

        for i in range(5):
            gait = -1 if i % 2 == 0 else 1
            nxt = self.person(0.86, gait=gait)
            nxt.move_to(walker.get_center() + RIGHT * 0.42)
            self.play(
                ReplacementTransform(walker, nxt),
                far.animate.shift(LEFT * 0.60),
                near.animate.shift(LEFT * 0.95),
                road[1].animate.shift(LEFT * 0.78),
                *self.spin_wheels(bus, 0.35),
                run_time=0.42,
                rate_func=linear,
            )
            walker = nxt

        self.wait(PAUSE_SHORT)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 01 — Reference frame intuition
    # -------------------------------------------------------------------------
    def who_is_moving(self):
        h = self.header(1, "WHO IS MOVING?", "The answer depends on who is doing the measuring.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus(8.6, 2.40).move_to(DOWN * 0.20)
        passenger = self.person(0.86, seated=True).move_to(bus.get_center() + LEFT * 2.65 + DOWN * 0.03)
        walker = self.person(0.86, gait=1).move_to(bus.get_center() + LEFT * 1.05 + DOWN * 0.03)
        inside_tag = self.speed_tag("INSIDE: WALKER MOVES", UP * 1.85, 3.8)
        self.play(FadeIn(bus), FadeIn(passenger), FadeIn(walker), FadeIn(inside_tag), run_time=RUN)
        walker = self.walk_cycle(walker, RIGHT * 2.0, steps=6, run_time=2.0)
        self.wait(PAUSE_SHORT)

        outside_tag = self.speed_tag("ROAD: BUS + WALKER MOVE", UP * 1.85, 4.3)
        self.play(ReplacementTransform(inside_tag, outside_tag), run_time=RUN_FAST)
        road = self.roadside()
        road.shift(DOWN * 0.05)
        far, near = self.scenery()
        self.play(FadeIn(far), FadeIn(near), FadeIn(road), run_time=RUN_FAST)
        self.play(
            bus.animate.shift(RIGHT * 2.0),
            passenger.animate.shift(RIGHT * 2.0),
            walker.animate.shift(RIGHT * 2.45),
            far.animate.shift(LEFT * 0.8),
            near.animate.shift(LEFT * 1.25),
            run_time=MOVE,
            rate_func=linear,
        )
        takeaway = self.statement("Same walker. Different reference frame.", -3.25, 30)
        self.play(FadeIn(takeaway), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 02 — Galileo principle of relativity
    # -------------------------------------------------------------------------
    def galileo_principle(self):
        h = self.header(2, "GALILEO'S PRINCIPLE OF RELATIVITY",
                        "Inside a smoothly moving vehicle, ordinary mechanics behaves normally.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        left_title = self.txt("BUS AT REST", 23, BOLD).move_to(LEFT * 4.0 + UP * 1.85)
        right_title = self.txt("BUS MOVING SMOOTHLY", 23, BOLD).move_to(RIGHT * 4.0 + UP * 1.85)

        bus_a = self.bus(5.1, 1.75).move_to(LEFT * 4.0 + DOWN * 0.25)
        bus_b = self.bus(5.1, 1.75).move_to(RIGHT * 4.0 + DOWN * 0.25)
        person_a = self.person(0.62).move_to(bus_a.get_center() + LEFT * 1.25 + DOWN * 0.02)
        person_b = self.person(0.62).move_to(bus_b.get_center() + LEFT * 1.25 + DOWN * 0.02)

        ball_a = self.ball(bus_a.get_center() + DOWN * 0.05)
        ball_b = self.ball(bus_b.get_center() + DOWN * 0.05)

        self.play(FadeIn(left_title), FadeIn(right_title), FadeIn(bus_a), FadeIn(bus_b),
                  FadeIn(person_a), FadeIn(person_b), FadeIn(ball_a), FadeIn(ball_b), run_time=RUN)

        self.play(
            ball_a.animate.shift(UP * 1.15),
            ball_b.animate.shift(UP * 1.15),
            *self.spin_wheels(bus_b, 0.6),
            run_time=1.05,
            rate_func=there_and_back,
        )
        self.play(
            ball_a.animate.shift(UP * 1.05),
            ball_b.animate.shift(UP * 1.05),
            *self.spin_wheels(bus_b, 0.6),
            run_time=1.05,
            rate_func=there_and_back,
        )

        same = self.label_box("FROM INSIDE, BOTH EXPERIMENTS LOOK THE SAME", 7.4, 0.78, 22)
        same.move_to(DOWN * 2.55)
        self.play(FadeIn(same), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 03 — Inside frame
    # -------------------------------------------------------------------------
    def inside_frame(self):
        h = self.header(3, "RIDE WITH THE BUS", "Now the bus is your reference frame.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus(9.4, 2.55).move_to(DOWN * 0.30)
        passenger = self.person(0.92, seated=True).move_to(bus.get_center() + LEFT * 3.0 + DOWN * 0.03)
        walker = self.person(0.92, gait=1).move_to(bus.get_center() + LEFT * 1.30 + DOWN * 0.03)

        tag = self.speed_tag("YOU MEASURE: 2 m/s", RIGHT * 4.7 + UP * 1.65, 3.2)
        self.play(FadeIn(bus), FadeIn(passenger), FadeIn(walker), FadeIn(tag), run_time=RUN)
        walker = self.walk_cycle(walker, RIGHT * 2.7, steps=8, run_time=2.5)

        note = self.statement("The bus feels still. Only the walker crosses the cabin.", -3.30, 28)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 04 — Road frame
    # -------------------------------------------------------------------------
    def road_frame(self):
        h = self.header(4, "NOW STAND ON THE ROAD", "The same walker is carried forward by the bus while also walking inside.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        road = self.roadside()
        observer = self.person(0.74).move_to(RIGHT * 5.8 + DOWN * 1.10)
        observer_label = self.txt("ROAD OBSERVER", 20, BOLD).next_to(observer, DOWN, buff=0.12)

        bus = self.bus(7.4, 2.10).move_to(LEFT * 5.1 + DOWN * 0.28)
        walker = self.person(0.74, gait=1).move_to(bus.get_center() + LEFT * 0.75 + DOWN * 0.02)
        tag_bus = self.speed_tag("BUS: 20 m/s", LEFT * 3.0 + UP * 1.65, 2.7)
        tag_walk = self.speed_tag("WALKER: 22 m/s", RIGHT * 2.8 + UP * 1.65, 3.0)

        self.play(Create(road), FadeIn(observer), FadeIn(observer_label), FadeIn(bus), FadeIn(walker),
                  FadeIn(tag_bus), FadeIn(tag_walk), run_time=RUN)

        for i in range(6):
            gait = -1 if i % 2 == 0 else 1
            next_walker = self.person(0.74, gait=gait)
            next_walker.move_to(walker.get_center() + RIGHT * 0.82)
            self.play(
                bus.animate.shift(RIGHT * 0.72),
                ReplacementTransform(walker, next_walker),
                run_time=0.46,
                rate_func=linear,
            )
            walker = next_walker

        result = self.statement("Outside, the walker covers more ground in the same time.", -3.25, 28)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 05 — Split-screen replay
    # -------------------------------------------------------------------------
    def split_replay(self):
        h = self.header(5, "REPLAY THE SAME EVENT", "Nothing changed about the walker. Only the observer changed.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        divider = Line(UP * 2.3, DOWN * 3.3, color=LIGHT, stroke_width=2)
        self.play(Create(divider), run_time=RUN_FAST)

        left_title = self.txt("INSIDE THE BUS", 24, BOLD).move_to(LEFT * 4.0 + UP * 1.9)
        right_title = self.txt("FROM THE ROAD", 24, BOLD).move_to(RIGHT * 4.0 + UP * 1.9)

        bus_l = self.bus(5.8, 1.80).move_to(LEFT * 4.0 + DOWN * 0.35)
        pass_l = self.person(0.58, seated=True).move_to(bus_l.get_center() + LEFT * 1.65)
        walk_l = self.person(0.58, gait=1).move_to(bus_l.get_center() + LEFT * 0.50)

        road_r = Line(RIGHT * 0.35 + DOWN * 1.35, RIGHT * 7.4 + DOWN * 1.35, color=ROAD, stroke_width=2)
        bus_r = self.bus(4.8, 1.65).move_to(RIGHT * 2.0 + DOWN * 0.35)
        walk_r = self.person(0.54, gait=1).move_to(bus_r.get_center() + LEFT * 0.45)

        tag_l = self.speed_tag("2 m/s", LEFT * 4.0 + DOWN * 2.45, 1.9)
        tag_r = self.speed_tag("22 m/s", RIGHT * 4.0 + DOWN * 2.45, 2.1)

        self.play(FadeIn(left_title), FadeIn(right_title), FadeIn(bus_l), FadeIn(pass_l),
                  FadeIn(walk_l), Create(road_r), FadeIn(bus_r), FadeIn(walk_r), run_time=RUN)

        for i in range(5):
            gait = -1 if i % 2 == 0 else 1
            next_l = self.person(0.58, gait=gait).move_to(walk_l.get_center() + RIGHT * 0.32)
            next_r = self.person(0.54, gait=gait).move_to(walk_r.get_center() + RIGHT * 0.47)
            self.play(
                ReplacementTransform(walk_l, next_l),
                bus_r.animate.shift(RIGHT * 0.38),
                ReplacementTransform(walk_r, next_r),
                run_time=0.42,
                rate_func=linear,
            )
            walk_l, walk_r = next_l, next_r

        self.play(FadeIn(tag_l), FadeIn(tag_r), run_time=RUN_FAST)
        statement = self.statement("Two measurements can both be correct.", -3.28, 30)
        self.play(FadeIn(statement), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 06 — Ball trajectories
    # -------------------------------------------------------------------------
    def ball_two_frames(self):
        h = self.header(6, "THE SAME BALL CAN TRACE TWO PATHS", "Galileo's idea becomes visible when we change reference frame.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        divider = Line(UP * 2.2, DOWN * 3.2, color=LIGHT, stroke_width=2)
        self.play(Create(divider), run_time=RUN_FAST)

        bus_l = self.bus(5.6, 1.75).move_to(LEFT * 4.0 + DOWN * 0.45)
        thrower_l = self.person(0.58).move_to(bus_l.get_center() + LEFT * 1.30)
        ball_l = self.ball(bus_l.get_center() + LEFT * 0.65 + UP * 0.15)
        vertical_path = DashedLine(
            ball_l.get_center(),
            ball_l.get_center() + UP * 1.70,
            dash_length=0.10,
            color=MID,
            stroke_width=2,
        )
        left_lab = self.label_box("INSIDE: STRAIGHT UP", 3.4, 0.68, 21).move_to(LEFT * 4.0 + UP * 1.70)

        road = Line(RIGHT * 0.45 + DOWN * 1.55, RIGHT * 7.45 + DOWN * 1.55, color=ROAD, stroke_width=2)
        bus_r = self.bus(4.5, 1.55).move_to(RIGHT * 1.8 + DOWN * 0.55)
        thrower_r = self.person(0.52).move_to(bus_r.get_center() + LEFT * 1.0)
        start = bus_r.get_center() + LEFT * 0.40 + UP * 0.10
        path = ParametricFunction(
            lambda t: start + RIGHT * (3.4 * t) + UP * (2.5 * t * (1 - t)),
            t_range=[0, 1],
            color=MID,
            stroke_width=2.4,
        )
        ball_r = self.ball(start)
        right_lab = self.label_box("ROAD: MOVES FORWARD TOO", 3.8, 0.68, 21).move_to(RIGHT * 4.0 + UP * 1.70)

        self.play(FadeIn(bus_l), FadeIn(thrower_l), FadeIn(ball_l), FadeIn(left_lab),
                  Create(road), FadeIn(bus_r), FadeIn(thrower_r), FadeIn(ball_r), FadeIn(right_lab),
                  run_time=RUN)
        self.play(Create(vertical_path), Create(path), run_time=RUN)

        self.play(
            MoveAlongPath(ball_l, vertical_path),
            MoveAlongPath(ball_r, path),
            bus_r.animate.shift(RIGHT * 1.6),
            thrower_r.animate.shift(RIGHT * 1.6),
            run_time=MOVE_LONG,
            rate_func=linear,
        )

        same = self.statement("Same throw. Different observed path.", -3.15, 30)
        self.play(FadeIn(same), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 07 — Light surprise
    # -------------------------------------------------------------------------
    def light_surprise(self):
        h = self.header(7, "NOW REPLACE THE WALKER WITH LIGHT", "This is where the classical intuition reaches its limit.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus(9.0, 2.45).move_to(DOWN * 0.25)
        passenger = self.person(0.82, seated=True).move_to(bus.get_center() + LEFT * 2.8)
        emitter = Dot(bus.get_center() + LEFT * 1.0 + UP * 0.18, radius=0.09, color=AMBER)
        pulse = Dot(emitter.get_center(), radius=0.12, color=AMBER)
        track = Line(emitter.get_center(), bus.get_center() + RIGHT * 3.2 + UP * 0.18,
                     color=AMBER, stroke_width=5).set_opacity(0.35)

        self.play(FadeIn(bus), FadeIn(passenger), FadeIn(emitter), FadeIn(track), FadeIn(pulse), run_time=RUN)
        self.play(pulse.animate.move_to(track.get_end()), run_time=1.55, rate_func=linear)
        inside = self.label_box("PASSENGER: LIGHT SPEED", 3.7, 0.74, 22, color=AMBER)
        inside.move_to(LEFT * 3.7 + DOWN * 2.55)
        self.play(FadeIn(inside), run_time=RUN_FAST)

        self.play(FadeOut(track), FadeOut(pulse), run_time=RUN_FAST)
        road = self.roadside()
        observer = self.person(0.68).move_to(RIGHT * 5.8 + DOWN * 1.0)
        pulse2 = Dot(emitter.get_center(), radius=0.12, color=AMBER)
        self.play(FadeIn(road), FadeIn(observer), FadeIn(pulse2), run_time=RUN_FAST)

        target = pulse2.get_center() + RIGHT * 5.3
        self.play(
            bus.animate.shift(RIGHT * 1.6),
            passenger.animate.shift(RIGHT * 1.6),
            emitter.animate.shift(RIGHT * 1.6),
            pulse2.animate.move_to(target),
            run_time=1.75,
            rate_func=linear,
        )
        road_lab = self.label_box("ROAD OBSERVER: SAME LIGHT SPEED", 4.5, 0.74, 22, color=AMBER)
        road_lab.move_to(RIGHT * 3.2 + DOWN * 2.55)
        self.play(FadeIn(road_lab), run_time=RUN_FAST)

        surprise = self.statement("For light, changing the observer does NOT change the measured speed.", -3.35, 27, AMBER)
        self.play(FadeIn(surprise), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 08 — Closing
    # -------------------------------------------------------------------------
    def closing(self):
        h = self.header(8, "GALILEO FIRST. EINSTEIN NEXT.",
                        "Keep the physical picture before introducing the mathematics.")
        self.play(FadeIn(h), run_time=RUN_FAST)

        cards = VGroup(
            self.label_box("1  CHOOSE AN OBSERVER", 3.8, 1.05, 22),
            self.label_box("2  WATCH THE SAME EVENT", 3.8, 1.05, 22),
            self.label_box("3  COMPARE WHAT CHANGES", 3.8, 1.05, 22),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 0.30)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.15),
            run_time=RUN_SLOW,
        )

        line1 = self.txt("Ordinary motion: different frames can give different measured velocities.", 28, BOLD)
        line2 = self.txt("Light: every inertial observer measures the same light speed.", 28, BOLD, AMBER)
        lines = VGroup(line1, line2).arrange(DOWN, buff=0.28).move_to(DOWN * 1.65)
        self.fit(lines, 13.5, 1.5)
        self.play(FadeIn(lines), run_time=RUN)

        final = self.label_box("NEXT QUESTION: WHAT MUST CHANGE IF LIGHT SPEED DOES NOT?", 8.5, 0.90, 24)
        final.move_to(DOWN * 3.05)
        self.play(FadeIn(final, shift=UP * 0.10), run_time=RUN)
        self.wait(PAUSE_FINAL)
