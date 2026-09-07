#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 simple relative-time V2.

This refinement keeps the V1 lesson logic and removes the only dense layout:
Carlos's moving-bus animation is shown first; the numerical calculation is
shown only after the motion diagram clears. This preserves the worksheet-like
one-step-at-a-time visual rhythm.
"""
from physics9_simple_relative_time_v1 import *


class Physics9SimpleRelativeTimeV2(Physics9SimpleRelativeTimeV1):
    """Same lesson as V1 with a cleaner Carlos-view sequence."""

    def carlos_view(self):
        h = self.header(
            3,
            "CARLOS IS ON THE ROAD",
            "The bus moves while the light is in flight, so Carlos sees a longer diagonal path.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        # A simple 3-4-5 triangle: vertical 3 m, horizontal 4 m, light path 5 m.
        y_bottom = -1.25
        y_top = 1.15
        p0 = LEFT * 3.2 + UP * y_bottom
        p1 = UP * y_top
        p2 = RIGHT * 3.2 + UP * y_bottom

        cabin = self.bus_cabin(4.25, 3.15).move_to(LEFT * 3.2 + DOWN * 0.05)
        mirror_bottom = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(p0)
        mirror_top = Line(LEFT * 0.34, RIGHT * 0.34, color=INK, stroke_width=5).move_to(LEFT * 3.2 + UP * y_top)
        cabin_group = VGroup(cabin, mirror_bottom, mirror_top)

        carlos = self.person(0.66).move_to(LEFT * 6.10 + DOWN * 1.40)
        c_lab = self.txt("CARLOS", 19, BOLD).next_to(carlos, DOWN, buff=0.08)
        pulse = Dot(p0, radius=0.10, color=AMBER)
        leg1 = Line(p0, p1, color=AMBER, stroke_width=5)
        leg2 = Line(p1, p2, color=AMBER, stroke_width=5)
        faint1 = DashedLine(p0, p1, color=LIGHT, stroke_width=2)
        faint2 = DashedLine(p1, p2, color=LIGHT, stroke_width=2)

        tri_v = Line(p0, LEFT * 3.2 + UP * y_top, color=MID, stroke_width=2)
        tri_h = Line(LEFT * 3.2 + UP * y_top, p1, color=MID, stroke_width=2)
        lab3 = self.txt("3 m", 20, BOLD, DARK).next_to(tri_v, LEFT, buff=0.12)
        lab4 = self.txt("4 m", 20, BOLD, DARK).next_to(tri_h, UP, buff=0.10)
        lab5 = self.txt("5 m", 20, BOLD, AMBER).move_to((p0 + p1) / 2 + RIGHT * 0.30)

        motion_note = self.card(
            "ONE HALF OF THE TICK",
            ["3-4-5 triangle  →  light travels 5 m"],
            width=5.6,
            body_size=21,
            fill=PAPER,
        ).move_to(RIGHT * 4.25 + UP * 2.15)

        self.play(FadeIn(carlos), FadeIn(c_lab), FadeIn(cabin_group), FadeIn(pulse), run_time=RUN)
        self.play(Create(tri_v), Create(tri_h), FadeIn(lab3), FadeIn(lab4), FadeIn(lab5), FadeIn(motion_note), run_time=RUN)
        self.wait(PAUSE_READ)
        self.add(faint1, faint2)

        self.play(
            cabin_group.animate.shift(RIGHT * 3.2),
            MoveAlongPath(pulse, Line(p0, p1)),
            Create(leg1),
            run_time=RUN_SLOW * 1.4,
        )
        self.play(
            cabin_group.animate.shift(RIGHT * 3.2),
            MoveAlongPath(pulse, Line(p1, p2)),
            Create(leg2),
            run_time=RUN_SLOW * 1.4,
        )
        self.wait(PAUSE_EXPLAIN)

        # Clear the moving diagram before calculations: one visual task at a time.
        diagram = VGroup(
            carlos, c_lab, cabin_group, pulse,
            leg1, leg2, faint1, faint2,
            tri_v, tri_h, lab3, lab4, lab5, motion_note,
        )
        self.play(FadeOut(diagram), run_time=RUN_FAST)

        calculation = VGroup(
            self.card(
                "STEP 1 • TOTAL PATH",
                ["5 m out + 5 m back = 10 m"],
                width=8.0,
                body_size=24,
                fill=WHITE,
            ),
            self.card(
                "STEP 2 • SAME LIGHT SPEED",
                ["Carlos must still measure c = 3.0 × 10⁸ m/s"],
                width=8.0,
                body_size=23,
                fill=PAPER,
            ),
            self.formula_box(
                r"t_C=\frac{10\,\mathrm{m}}{3.0\times10^8\,\mathrm{m/s}}=33.3\,\mathrm{ns}",
                width=8.0,
                size=33,
                fill=WHITE,
            ),
        ).arrange(DOWN, buff=0.30).move_to(DOWN * 0.15)

        for item in calculation:
            self.play(FadeIn(item, shift=UP * 0.05), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()


# Final:
#   manim -pqh physics9_simple_relative_time_v2.py Physics9SimpleRelativeTimeV2 --disable_caching
