#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Relative time V3: PROBLEM ONLY.

Pedagogical goal
----------------
Present one very simple, copyable problem statement and animate only the
physical situation. The video deliberately DOES NOT solve the exercise.
Students use the familiar kinematics relation t = d / v after the video.

Given data:
- Ana sees a total light path of 6 m.
- Carlos sees the same light pulse travel a total path of 10 m.
- Both measure the same light speed c = 3.0e8 m/s.

No gamma, no Lorentz transformations, no Pythagorean derivation, no computed
travel times, and no final numerical answers are shown.

Target: Manim Community Edition 0.20.1
Final:
    manim -pqh physics9_simple_relative_time_v3_problem_only.py \
        Physics9RelativeTimeProblemOnlyV3 --disable_caching
"""

from physics9_simple_relative_time_v1 import *


class Physics9RelativeTimeProblemOnlyV3(Physics9SimpleRelativeTimeV1):
    """Short Grade-9 prompt + physical animation, without the solution."""

    def construct(self):
        self.opening_prompt()
        self.copy_problem()
        self.ana_motion()
        self.carlos_motion()
        self.student_task()

    # ------------------------------------------------------------------
    # 00 — Opening: the question, not the answer
    # ------------------------------------------------------------------
    def opening_prompt(self):
        kicker = self.txt("PHYSICS 9  •  RELATIVE MOTION", 23, BOLD, DARK)
        title = self.fit(self.txt("CAN TWO OBSERVERS MEASURE DIFFERENT TIMES?", 44, BOLD), 13.8)
        subtitle = self.txt("Same light pulse. Same light speed. Different observed path.", 26, NORMAL, DARK)
        top = VGroup(kicker, title, subtitle).arrange(DOWN, buff=0.18).shift(UP * 2.55)

        road = Line(LEFT * 7.1 + DOWN * 2.35, RIGHT * 7.1 + DOWN * 2.35, color=MID, stroke_width=2)
        bus = self.bus_cabin(5.0, 3.0).move_to(LEFT * 1.3 + DOWN * 0.35)
        clock, bottom, top_p = self.light_clock_inside(bus.get_center() + RIGHT * 0.75, 2.0)
        ana = self.person(0.70).move_to(bus.get_center() + LEFT * 1.15 + DOWN * 0.15)
        carlos = self.person(0.70).move_to(RIGHT * 5.30 + DOWN * 0.70)
        lab_a = self.txt("ANA", 19, BOLD).next_to(ana, DOWN, buff=0.07)
        lab_c = self.txt("CARLOS", 19, BOLD).next_to(carlos, DOWN, buff=0.07)
        pulse = Dot(bottom, radius=0.10, color=AMBER)

        self.play(FadeIn(top), run_time=RUN)
        self.play(Create(road), FadeIn(bus), FadeIn(clock), FadeIn(ana), FadeIn(carlos),
                  FadeIn(lab_a), FadeIn(lab_c), FadeIn(pulse), run_time=RUN)
        self.play(MoveAlongPath(pulse, Line(bottom, top_p)), run_time=RUN_SLOW)
        self.play(MoveAlongPath(pulse, Line(top_p, bottom)), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 01 — Copyable problem statement
    # ------------------------------------------------------------------
    def copy_problem(self):
        h = self.header(
            1,
            "COPY THE PROBLEM",
            "Read first. Then copy the statement exactly into your notebook.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        box = RoundedRectangle(
            width=13.4, height=5.45, corner_radius=0.12,
            stroke_color=DARK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(DOWN * 0.35)

        title = self.txt("PROBLEM", 28, BOLD).move_to(box.get_top() + DOWN * 0.45)
        lines = VGroup(
            self.txt("Ana is inside a very fast bus with a light clock.", 24, NORMAL, DARK),
            self.txt("A light pulse leaves the floor, reaches the roof, and returns to the floor.", 24, NORMAL, DARK),
            self.txt("Ana sees the light travel a total distance of 6 m.", 24, NORMAL, DARK),
            self.txt("Carlos, standing on the road, sees the same light pulse travel 10 m in total.", 24, NORMAL, DARK),
            self.txt("Both observers measure the same speed of light:", 24, NORMAL, DARK),
            self.math(r"c=3.0\times10^8\ \mathrm{m/s}", 38),
            self.txt("Find the travel time measured by Ana and by Carlos. Compare the two times.", 24, BOLD, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(lines, 12.35, 4.35)
        lines.next_to(title, DOWN, buff=0.28)
        lines.align_to(box, LEFT).shift(RIGHT * 0.45)

        self.play(FadeIn(box), FadeIn(title), run_time=RUN_FAST)
        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.03), run_time=RUN_FAST)
        # Long copy pause: this screen is intentionally notebook-friendly.
        self.wait(9.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 02 — Ana sees the simple vertical path
    # ------------------------------------------------------------------
    def ana_motion(self):
        h = self.header(
            2,
            "WHAT DOES ANA SEE?",
            "Inside the bus, the light goes straight up and straight down.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        bus = self.bus_cabin(6.1, 4.0).move_to(LEFT * 1.6 + DOWN * 0.25)
        clock, bottom, top_p = self.light_clock_inside(bus.get_center() + RIGHT * 1.0, 2.55)
        ana = self.person(0.82).move_to(bus.get_center() + LEFT * 1.35 + DOWN * 0.20)
        ana_lab = self.txt("ANA", 20, BOLD).next_to(ana, DOWN, buff=0.07)
        pulse = Dot(bottom, radius=0.11, color=AMBER)

        info = self.card(
            "ANA'S OBSERVATION",
            [
                "Light path: vertical",
                "Total distance: 6 m",
                "Light speed: c",
            ],
            width=4.6,
            body_size=23,
            fill=PAPER,
        ).move_to(RIGHT * 4.55 + UP * 0.20)

        up_path = Line(bottom, top_p, color=AMBER, stroke_width=5)
        down_path = Line(top_p, bottom, color=AMBER, stroke_width=5)

        self.play(FadeIn(bus), FadeIn(clock), FadeIn(ana), FadeIn(ana_lab), FadeIn(info), FadeIn(pulse), run_time=RUN)
        self.play(Create(up_path), MoveAlongPath(pulse, Line(bottom, top_p)), run_time=RUN_SLOW * 1.3)
        self.play(Create(down_path), MoveAlongPath(pulse, Line(top_p, bottom)), run_time=RUN_SLOW * 1.3)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 03 — Carlos sees the same pulse along a longer path
    # ------------------------------------------------------------------
    def carlos_motion(self):
        h = self.header(
            3,
            "WHAT DOES CARLOS SEE?",
            "The bus moves while the same light pulse is travelling.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        road = Line(LEFT * 7.1 + DOWN * 2.45, RIGHT * 7.1 + DOWN * 2.45, color=MID, stroke_width=2)
        carlos = self.person(0.72).move_to(LEFT * 6.15 + DOWN * 1.38)
        carlos_lab = self.txt("CARLOS", 19, BOLD).next_to(carlos, DOWN, buff=0.07)

        # Start, top-hit, and return events. Geometry is deliberately unlabeled:
        # students are GIVEN the 10 m path; they do not need a triangle derivation.
        y_bottom = -1.15
        y_top = 1.20
        p0 = LEFT * 3.7 + UP * y_bottom
        p1 = ORIGIN + UP * y_top
        p2 = RIGHT * 3.7 + UP * y_bottom

        cabin = self.bus_cabin(4.1, 3.0).move_to(LEFT * 3.7 + DOWN * 0.02)
        mirror_bottom = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(p0)
        mirror_top = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(LEFT * 3.7 + UP * y_top)
        cabin_group = VGroup(cabin, mirror_bottom, mirror_top)

        pulse = Dot(p0, radius=0.11, color=AMBER)
        path1 = Line(p0, p1, color=AMBER, stroke_width=5)
        path2 = Line(p1, p2, color=AMBER, stroke_width=5)

        info = self.card(
            "CARLOS'S OBSERVATION",
            [
                "Same light pulse",
                "Longer diagonal path",
                "Total distance: 10 m",
                "Light speed: c",
            ],
            width=4.7,
            body_size=22,
            fill=PAPER,
        ).move_to(RIGHT * 4.75 + UP * 1.55)

        same_c = self.formula_box(r"v_{\mathrm{light}}=c", width=4.4, height=0.95, size=36, fill=WHITE)
        same_c.next_to(info, DOWN, buff=0.28)

        self.play(Create(road), FadeIn(carlos), FadeIn(carlos_lab), FadeIn(cabin_group),
                  FadeIn(pulse), FadeIn(info), FadeIn(same_c), run_time=RUN)
        self.play(
            cabin_group.animate.shift(RIGHT * 3.7),
            Create(path1),
            MoveAlongPath(pulse, Line(p0, p1)),
            run_time=RUN_SLOW * 1.6,
        )
        self.play(
            cabin_group.animate.shift(RIGHT * 3.7),
            Create(path2),
            MoveAlongPath(pulse, Line(p1, p2)),
            run_time=RUN_SLOW * 1.6,
        )
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 04 — Student task only; do not reveal any solution
    # ------------------------------------------------------------------
    def student_task(self):
        h = self.header(
            4,
            "NOW YOU SOLVE IT",
            "Use the motion equation you already know. Do not use any new relativity formula.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        relation = self.formula_box(r"t=\frac{d}{v}", width=4.2, height=1.15, size=48, fill=PAPER)
        relation.move_to(UP * 1.75)

        data = VGroup(
            self.card("ANA", ["d = 6 m", "v = c"], width=4.5, body_size=25),
            self.card("CARLOS", ["d = 10 m", "v = c"], width=4.5, body_size=25),
        ).arrange(RIGHT, buff=0.55).move_to(UP * 0.10)

        questions = self.card(
            "QUESTIONS",
            [
                "1. What time does Ana measure?",
                "2. What time does Carlos measure?",
                "3. Are the two times equal?",
                "4. If the light speed is the same, what changed?",
            ],
            width=10.7,
            body_size=24,
            fill=WHITE,
        ).move_to(DOWN * 2.15)

        no_solution = self.txt("STOP HERE • SOLVE IN YOUR NOTEBOOK", 22, BOLD, DARK)
        no_solution.to_edge(DOWN, buff=0.20)

        self.play(FadeIn(relation), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.05) for x in data], lag_ratio=0.18), run_time=RUN)
        self.play(FadeIn(questions), FadeIn(no_solution), run_time=RUN)
        self.wait(10.0)


# Preview:
#   manim -pql physics9_simple_relative_time_v3_problem_only.py Physics9RelativeTimeProblemOnlyV3 --disable_caching
# Final:
#   manim -pqh physics9_simple_relative_time_v3_problem_only.py Physics9RelativeTimeProblemOnlyV3 --disable_caching
