#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 City Cars V2 — layout-safe senior revision.

This revision inherits the fully validated V1 lesson and corrects the two
visual issues found in sampled-frame QA:
1. very long section headers are automatically fitted inside the 16:9 frame;
2. the final green takeaway sentence is fitted to the safe width.

All physics, graphs, numerical values, equations and pedagogical sequencing
remain unchanged from V1.
"""

from physics9_city_cars_position_velocity import *


class Physics9CityCarsV2(Physics9CityCars):
    """V2 with dynamic header fitting and final safe-area fitting."""

    def stage_title(self, number: str, title: str, subtitle: str | None = None):
        badge = Circle(
            radius=0.32,
            stroke_color=INK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        badge_num = self.txt(number, 24, BOLD).move_to(badge)
        main = self.txt(title, 34, BOLD)
        # Reserve horizontal space for badge + gap + margins.
        if main.width > 13.55:
            main.scale_to_fit_width(13.55)
        top = VGroup(VGroup(badge, badge_num), main).arrange(RIGHT, buff=0.26)
        top.to_edge(UP, buff=0.26).to_edge(LEFT, buff=0.42)

        line = Line(
            LEFT * 7.55,
            RIGHT * 7.55,
            color=LIGHT,
            stroke_width=1.4,
        ).next_to(top, DOWN, buff=0.16)
        group = VGroup(top, line)

        if subtitle:
            sub = self.txt(subtitle, 22, color=DARK)
            if sub.width > 14.70:
                sub.scale_to_fit_width(14.70)
            sub.next_to(line, DOWN, buff=0.10).align_to(top, LEFT)
            group.add(sub)
        return group

    def final_method_map(self):
        header = self.stage_title(
            "9",
            "METHOD YOU CAN REUSE FOR ANY TWO-CAR MEETING PROBLEM",
            "The graph and the algebra are two representations of the same motion.",
        )
        self.play(FadeIn(header), run_time=0.7)

        items = [
            ("1", "CHOOSE +x"),
            ("2", "ASSIGN SIGNS"),
            ("3", "WRITE x(t)"),
            ("4", "SET x_A = x_B"),
            ("5", "SOLVE t"),
            ("6", "FIND x"),
            ("7", "DRAW x–t"),
            ("8", "DRAW v–t"),
            ("9", "VERIFY"),
        ]
        cards = VGroup()
        for number, label in items:
            box = RoundedRectangle(
                width=3.75,
                height=1.02,
                corner_radius=0.12,
                stroke_color=INK,
                stroke_width=1.7,
                fill_color=WHITE,
                fill_opacity=1,
            )
            num = Circle(
                radius=0.22,
                stroke_color=INK,
                stroke_width=1.5,
                fill_color=PALE,
                fill_opacity=1,
            )
            nt = self.txt(number, 18, BOLD).move_to(num)
            text = self.txt(label, 22, BOLD)
            content = VGroup(VGroup(num, nt), text).arrange(RIGHT, buff=0.18).move_to(box)
            cards.add(VGroup(box, content))

        cards.arrange_in_grid(rows=3, cols=3, buff=(0.30, 0.28)).move_to(DOWN * 0.25)
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.10) for card in cards],
                lag_ratio=0.10,
            ),
            run_time=2.4,
        )
        self.wait(3.6)

        final = self.txt(
            "POSITION tells you WHERE.   VELOCITY tells you HOW FAST and IN WHICH DIRECTION.",
            27,
            BOLD,
            GOOD,
        )
        if final.width > 14.35:
            final.scale_to_fit_width(14.35)
        final.to_edge(DOWN, buff=0.30)
        self.play(FadeIn(final), run_time=0.8)
        self.wait(4.2)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)

        closing = VGroup(
            self.txt("PHYSICS 9", 38, BOLD),
            self.txt("Two cars. One coordinate system. One consistent story.", 34, BOLD),
            self.mth(r"x_A(2)=x_B(2)=160\ \text{km}", 43, GOOD),
        ).arrange(DOWN, buff=0.34)
        self.fit(closing, width=14.35, height=6.5)
        self.play(FadeIn(closing, shift=UP * 0.10), run_time=1.0)
        self.wait(4.0)


# Preview:
#   LESSON_TIME_SCALE=0.08 manim -pql physics9_city_cars_position_velocity_v2.py Physics9CityCarsV2 --fps 15 --disable_caching
# Final:
#   LESSON_TIME_SCALE=1.0 manim -pqh physics9_city_cars_position_velocity_v2.py Physics9CityCarsV2 --fps 30 --disable_caching
