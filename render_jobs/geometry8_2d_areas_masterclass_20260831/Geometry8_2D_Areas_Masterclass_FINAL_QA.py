#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility QA layer for Geometry 8 2D Areas Masterclass.
Fixes ManimCE 0.20.1 Sector constructor usage discovered by literal PQL.
"""
from __future__ import annotations

from Geometry8_2D_Areas_Masterclass_FINAL import *


class Geometry8Areas2DMasterclassFinalQA(Geometry8Areas2DMasterclassFinal):
    """PQL/PQH release class with ManimCE 0.20.1-compatible sectors."""

    def circle_parts(self):
        h = self.header(
            10,
            "CIRCLE PARTS — FRACTIONS OF THE FULL AREA",
            "Semicircles and quadrants use a fraction of A = πr².",
        )
        self.add(h)
        s = Sector(
            radius=1.75,
            angle=PI,
            start_angle=0,
            color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.75,
        ).shift(LEFT * 4 + DOWN * .1)
        q = Sector(
            radius=1.75,
            angle=PI / 2,
            start_angle=0,
            color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.75,
        ).shift(RIGHT * 2.9 + DOWN * .1)
        e1 = self.box(r"A_{semi}=\frac12\pi r^2", 5.1, 48).next_to(s, DOWN, buff=.25)
        e2 = self.box(r"A_{quad}=\frac14\pi r^2", 5.1, 48).next_to(q, DOWN, buff=.25)
        self.play(Create(s), run_time=.7)
        self.play(FadeIn(e1), run_time=.55)
        self.play(Create(q), run_time=.7)
        self.play(FadeIn(e2), run_time=.55)
        self.wait(2.8)
        self.wipe()

    def shaded_complex(self):
        h = self.header(
            14,
            "COMPLEX SHADED AREA — SIMPLIFY FIRST",
            "Recognize repeated pieces before calculating.",
        )
        self.add(h)
        sq = Square(
            4.7,
            color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.72,
        ).shift(LEFT * 3.2 + DOWN * .05)
        corners = [sq.get_corner(DL), sq.get_corner(DR), sq.get_corner(UR), sq.get_corner(UL)]
        starts = [0, PI / 2, PI, 3 * PI / 2]
        sectors = VGroup(*[
            Sector(
                arc_center=c,
                radius=2.35,
                angle=PI / 2,
                start_angle=a,
                stroke_color=INK,
                stroke_width=3,
                fill_color=WHITE,
                fill_opacity=1,
            )
            for c, a in zip(corners, starts)
        ])
        rhs = VGroup(
            self.txt("4 quadrants = 1 full circle", 30, True),
            self.eq(r"A_s=12^2-\pi(6)^2", 44),
            self.box(r"A_s=144-36\pi\approx30.90", 6.1, 48),
        ).arrange(DOWN, buff=.34).move_to(RIGHT * 3.45 + DOWN * .05)
        self.play(
            Create(sq),
            LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=.1),
            run_time=1.1,
        )
        for x in rhs:
            self.play(FadeIn(x, shift=UP * .04), run_time=.58)
            self.wait(.65)
        self.wait(2.5)
        self.wipe()


# Preview:
# LESSON_TIME_SCALE=0.045 manim -pql Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_Masterclass_FINAL_QA.py Geometry8Areas2DMasterclassFinalQA --disable_caching
