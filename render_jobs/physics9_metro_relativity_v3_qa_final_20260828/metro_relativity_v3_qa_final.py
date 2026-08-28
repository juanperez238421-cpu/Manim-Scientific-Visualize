#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final QA patch for Physics 9 Metro Relativity V3.

This file inherits the fully rendered 100% 2D / 100% English V3 lesson and
replaces only the two screens where post-render full-resolution QA found
collisions: the station walker calculation and the station light-clock result.
"""
from __future__ import annotations

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "physics9_metro_relativity_v3_2d_english_20260828"
sys.path.insert(0, str(BASE))

from metro_relativity_v3_2d_english import *  # noqa: F401,F403


class Physics9MetroRelativityV3QA(Physics9MetroRelativityV3):
    """V3 with final collision-free layout corrections after frame audit."""

    def walker_station(self) -> None:
        self.set_header(
            3,
            "FROM THE STATION: THE TRAIN AND THE WALKER BOTH MOVE",
            "The train moves at 20 m/s (72 km/h). The same 2 m/s walking motion is added in the same direction.",
        )
        ground = Line(
            LEFT * 7.0 + DOWN * 2.10,
            RIGHT * 7.0 + DOWN * 2.10,
            color=DARK_GRAY,
            stroke_width=2.4,
        )
        station = self.person(RIGHT * 6.15 + DOWN * 1.12, 0.88, "stand")
        station_lab = self.txt("STATION OBSERVER", 20, BOLD).next_to(station, UP, buff=0.15)
        train = self.metro_cutaway(center=LEFT * 4.65 + DOWN * 0.38, width=7.0, height=2.35)
        walker = self.person(LEFT * 5.20 + DOWN * 0.72, 0.72, "walk_a")
        train_group = VGroup(train, walker)
        train_v = self.velocity_arrow(
            LEFT * 6.4 + DOWN * 2.72,
            LEFT * 2.4 + DOWN * 2.72,
            r"v_{train}=20\;\mathrm{m/s}",
            25,
        )
        velocity_card = self.formula_card(
            r"v_{w,S}=20+2=22\;\mathrm{m/s}", width=5.2, size=33
        ).move_to(RIGHT * 3.85 + UP * 1.55)

        self.play(
            Create(ground),
            FadeIn(station),
            Write(station_lab),
            FadeIn(train_group),
            run_time=RUN_SLOW,
        )
        self.play(GrowArrow(train_v[0]), Write(train_v[1]), FadeIn(velocity_card), run_time=RUN_NORMAL)
        self.play(
            train.animate.shift(RIGHT * 6.1),
            walker.animate.shift(RIGHT * 6.7),
            run_time=4.0,
            rate_func=linear,
        )

        # QA fix: separate the physical animation from the position calculation.
        # The train becomes a compact visual reference on the left; equations own the right half.
        self.play(
            FadeOut(station),
            FadeOut(station_lab),
            FadeOut(train_v),
            FadeOut(velocity_card),
            FadeOut(ground),
            train_group.animate.scale(0.72).move_to(LEFT * 3.75 + DOWN * 0.55),
            run_time=RUN_NORMAL,
        )

        difference_chip = self.answer_chip(
            "After 5 s: 110 m - 100 m = 10 m",
            width=5.8,
            size=23,
        ).move_to(LEFT * 3.75 + UP * 1.55)
        position_cards = VGroup(
            self.formula_card(r"X_{train}=0+(20)(5)=100\;\mathrm{m}", width=5.8, size=31),
            self.formula_card(r"X_{w}=0+(22)(5)=110\;\mathrm{m}", width=5.8, size=31),
        ).arrange(DOWN, buff=0.26).move_to(RIGHT * 3.95 + UP * 0.20)
        result = self.answer_chip(
            "Station: 22 m/s = 79.2 km/h",
            width=5.6,
            size=27,
        ).move_to(RIGHT * 3.95 + DOWN * 2.15)

        self.play(FadeIn(difference_chip), run_time=RUN_NORMAL)
        self.play(FadeIn(position_cards[0]), run_time=RUN_NORMAL)
        self.play(FadeIn(position_cards[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def light_clock_station_frame(self) -> None:
        self.set_header(
            7,
            "THE SAME TWO EVENTS FROM THE STATION FRAME",
            "The ceiling mirror moves horizontally, but the station observer still measures the light speed as c. This changes the elapsed time.",
        )
        origin = LEFT * 4.40 + DOWN * 1.25
        height = 2.55
        horizontal = 2.55 * (self.GROUND_HORIZONTAL_M / self.CLOCK_HEIGHT)

        source = Dot(origin, radius=0.10, color=LIGHT_AMBER)
        initial_mirror = RoundedRectangle(
            width=0.72,
            height=0.13,
            corner_radius=0.04,
            stroke_color=MID_GRAY,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        ).move_to(origin + UP * height)
        final_mirror = RoundedRectangle(
            width=0.72,
            height=0.13,
            corner_radius=0.04,
            stroke_color=BLACK_LINE,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        ).move_to(origin + RIGHT * horizontal + UP * height)
        base_path = DashedLine(origin, origin + RIGHT * horizontal, color=MID_GRAY, dash_length=0.10)
        vertical = DashedLine(
            origin + RIGHT * horizontal,
            origin + RIGHT * horizontal + UP * height,
            color=MID_GRAY,
            dash_length=0.10,
        )
        light_path = Line(origin, final_mirror.get_center(), color=LIGHT_AMBER, stroke_width=4)
        moving_arrow = self.velocity_arrow(
            origin + DOWN * 0.70,
            origin + RIGHT * horizontal + DOWN * 0.70,
            r"v=0.60c",
            25,
        )

        # QA fix: Δx is above the dashed base; v = 0.60c remains below its arrow.
        dx_label = self.eq(r"\Delta x=1.8\;\mathrm{m}", 25).next_to(base_path, UP, buff=0.13)
        h_label = self.eq(r"H=2.4\;\mathrm{m}", 25).next_to(vertical, RIGHT, buff=0.12)
        d_label = self.eq(r"d_{light}=3.0\;\mathrm{m}", 25, color=LIGHT_AMBER).next_to(light_path, LEFT, buff=0.12)
        labels = VGroup(dx_label, h_label, d_label)

        xeq = self.formula_card(
            r"X_{mirror}=X_0+vt=0+(0.60c)t", width=6.0, size=32
        ).move_to(RIGHT * 4.45 + UP * 1.70)
        prompt = self.text_card(
            "YOUR TURN",
            ["The light still moves at c.", "The mirror moves at 0.60c.", "What time does the station measure?"],
            width=5.75,
            body_size=22,
        ).move_to(RIGHT * 4.45 + DOWN * 0.15)

        self.play(
            FadeIn(source),
            FadeIn(initial_mirror),
            FadeIn(final_mirror),
            Create(base_path),
            Create(vertical),
            run_time=RUN_SLOW,
        )
        self.play(
            GrowArrow(moving_arrow[0]),
            Write(moving_arrow[1]),
            FadeIn(xeq),
            FadeIn(prompt),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_WORK * 1.25)
        self.play(FadeOut(prompt), run_time=RUN_QUICK)

        light_dot = Dot(source.get_center(), radius=0.10, color=LIGHT_AMBER)
        self.add(light_dot)
        self.play(
            Create(light_path),
            light_dot.animate.move_to(final_mirror.get_center()),
            run_time=2.5,
            rate_func=linear,
        )
        self.play(LaggedStart(*[Write(m) for m in labels], lag_ratio=0.20), run_time=RUN_SLOW)

        derivation = VGroup(
            self.formula_card(r"(ct)^2=(0.60ct)^2+(2.4)^2", width=6.2, size=30),
            self.formula_card(r"0.64c^2t^2=5.76", width=6.2, size=32),
            self.formula_card(r"ct=3.0\;\mathrm{m}", width=6.2, size=34),
            self.formula_card(r"t=\frac{3.0}{3.00\times10^8}=10.0\;\mathrm{ns}", width=6.2, size=29),
        ).arrange(DOWN, buff=0.14).move_to(RIGHT * 4.45 + DOWN * 0.62)
        self.play(FadeOut(xeq), run_time=RUN_QUICK)
        for card in derivation:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_EXPLAIN)

        # QA fix: clear the derivation before presenting the final comparison chips.
        self.play(FadeOut(derivation), run_time=RUN_QUICK)
        left_result = self.answer_chip(
            "Train frame: 8.0 ns", width=4.3, size=27
        ).move_to(LEFT * 3.90 + DOWN * 2.35)
        right_result = self.answer_chip(
            "Station frame: 10.0 ns", width=4.6, size=27
        ).move_to(RIGHT * 3.90 + DOWN * 2.35)
        self.play(FadeIn(left_result), FadeIn(right_result), run_time=RUN_NORMAL)

        conclusion = self.txt(
            "SAME LIGHT SPEED  c  •  DIFFERENT ELAPSED COORDINATE TIME", 27, BOLD
        ).to_edge(DOWN, buff=0.18)
        self.play(Write(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()


# Final QA render:
# manim -pqh metro_relativity_v3_qa_final.py Physics9MetroRelativityV3QA --disable_caching
