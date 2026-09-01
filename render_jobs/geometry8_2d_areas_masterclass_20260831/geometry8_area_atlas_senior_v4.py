#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior visual/geometry refinements for Geometry 8 — Area of 2D Figures V4.

This layer keeps the V3 lesson content and numerical examples unchanged, while
improving hierarchy, legibility, geometric honesty, and the circle-part visuals.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaSeniorV4Mixin:
    """Senior-QA overrides applied on top of the complete V3 atlas."""

    def stage_strip(self):
        labels = ["CONSTRUCT", "PARTS", "DERIVE", "EXAMPLE"]
        items = VGroup()
        for label in labels:
            box = RoundedRectangle(
                width=1.90, height=.54, corner_radius=.08,
                stroke_color=LIGHT, stroke_width=1.35,
                fill_color=WHITE, fill_opacity=1,
            )
            text = self.txt(label, 21, True).move_to(box).set_opacity(.46)
            items.add(VGroup(box, text))
        items.arrange(RIGHT, buff=.10)
        items.to_edge(RIGHT, buff=.42).shift(UP * 2.56)
        return items

    def mark_stage(self, strip, index):
        animations = []
        for i, item in enumerate(strip):
            active = i == index
            animations.extend([
                item[0].animate.set_stroke(
                    INK if active else LIGHT, width=3.0 if active else 1.25
                ).set_fill(PAPER if active else WHITE, opacity=1),
                item[1].animate.set_opacity(1.0 if active else .42),
            ])
        self.play(*animations, run_time=.30)

    def example_stack(self, given, formula, substitution, result, width=6.15):
        panel = RoundedRectangle(
            width=width, height=4.78, corner_radius=.14,
            stroke_color=LIGHT, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=.98,
        )
        title = self.txt("WORKED EXAMPLE", 33, True)
        guide = self.txt("FORMULA  →  SUBSTITUTE  →  ANSWER", 22, True).set_opacity(.62)
        given_m = self.txt(given, 29)
        self.fit(given_m, width - .62, .48)
        formula_m = self.eq(formula, 50)
        self.fit(formula_m, width - .80, .72)
        sub_m = self.eq(substitution, 45)
        self.fit(sub_m, width - .72, .72)
        answer = self.box(result, width - .66, 56)
        check = self.txt("Check: the answer uses square units.", 25, True)
        self.fit(check, width - .72, .43)

        content = VGroup(title, guide, given_m, formula_m, sub_m, answer, check)
        content.arrange(DOWN, buff=.14)
        self.fit(content, width - .48, 4.34)
        content.move_to(panel)
        return VGroup(panel, content)

    def show_example(self, stack, right_x=3.55):
        stack.move_to(RIGHT * right_x + DOWN * .15)
        panel, content = stack
        self.play(FadeIn(panel, shift=UP*.03), run_time=.30)
        for i, item in enumerate(content):
            self.play(FadeIn(item, shift=UP * .025), run_time=.32)
            if i in (2, 3, 4):
                self.wait(.34)
        self.wait(1.80)

    def circle_explicit(self):
        h = self.header(
            10,
            "7 · CIRCLE",
            "The radius generates the circle; sector rearrangement connects circumference to area.",
        )
        strip = self.stage_strip(); self.add(h, strip)

        center = np.array([-4.05, -.25, 0])
        radius = 1.62
        circle = Circle(radius, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.18).move_to(center)
        sweep = Line(center, center + RIGHT*radius, color=INK, stroke_width=4)
        dot = Dot(center, radius=.07, color=INK)

        self.mark_stage(strip, 0)
        self.play(FadeIn(dot), Create(sweep), run_time=.42)
        self.play(Create(circle), Rotate(sweep, angle=TAU, about_point=center), run_time=1.15, rate_func=linear)

        self.mark_stage(strip, 1)
        diameter = DashedLine(center + LEFT*radius, center + RIGHT*radius, color=MID, stroke_width=2.8)
        rlab = self.eq("r", 38).next_to(Line(center, center + RIGHT*radius), UP, buff=.06)
        dlab = self.eq("d=2r", 35).next_to(diameter, DOWN, buff=.10)
        self.play(Create(diameter), FadeIn(rlab), FadeIn(dlab), run_time=.60)

        self.mark_stage(strip, 2)
        n = 16
        theta = TAU / n
        sectors = VGroup()
        for k in range(n):
            sectors.add(Sector(
                arc_center=center,
                radius=radius,
                start_angle=k*theta,
                angle=theta,
                stroke_color=INK,
                stroke_width=1.4,
                fill_color=FILL if k % 2 == 0 else PAPER,
                fill_opacity=.72 if k % 2 == 0 else .92,
            ))

        source_outline = Circle(radius, color=LIGHT, stroke_width=2.0, fill_opacity=0).move_to(center)
        self.play(FadeOut(circle), FadeIn(source_outline), FadeIn(sectors), run_time=.55)
        divide_note = self.txt("Divide the circle into equal sectors.", 27, True).move_to(RIGHT*3.50 + UP*1.72)
        self.play(FadeIn(divide_note), run_time=.35)
        self.wait(.35)

        step = (math.pi * radius) / n
        x0 = .72
        targets = VGroup()
        for i in range(n):
            x = x0 + i*step
            if i % 2 == 0:
                apex = np.array([x, -radius/2, 0])
                start = PI/2 - theta/2
            else:
                apex = np.array([x, radius/2, 0])
                start = 3*PI/2 - theta/2
            targets.add(Sector(
                arc_center=apex,
                radius=radius,
                start_angle=start,
                angle=theta,
                stroke_color=INK,
                stroke_width=1.25,
                fill_color=FILL if i % 2 == 0 else PAPER,
                fill_opacity=.72 if i % 2 == 0 else .92,
            ))

        self.play(
            LaggedStart(*[Transform(sectors[i], targets[i]) for i in range(n)], lag_ratio=.025),
            FadeOut(divide_note),
            run_time=1.65,
            rate_func=smooth,
        )

        limit_note = self.txt("More sectors → straighter top and bottom edges", 25, True)
        limit_note.move_to(RIGHT*3.52 + UP*1.72)
        base_note = self.eq(r"\frac{C}{2}=\frac{2\pi r}{2}=\pi r", 39).move_to(RIGHT*3.45 + UP*1.18)
        self.play(FadeIn(limit_note), FadeIn(base_note), run_time=.55)

        left_x = x0 - .10
        right_x = x0 + (n-1)*step + .16
        base = self.dimension([left_x, -1.28, 0], [right_x, -1.28, 0], r"\pi r", DOWN, 35)
        height = self.dimension([right_x+.35, -radius/2, 0], [right_x+.35, radius/2, 0], "r", RIGHT, 35)
        self.play(GrowFromCenter(base[0]), FadeIn(base[1]), GrowFromCenter(height[0]), FadeIn(height[1]), run_time=.60)

        formula = self.box(r"A=(\pi r)(r)=\pi r^2", 5.65, 55).move_to(RIGHT*3.50 + DOWN*2.22)
        self.play(FadeIn(formula), run_time=.45)
        self.wait(.95)

        self.mark_stage(strip, 3)
        self.play(
            FadeOut(sectors), FadeOut(base), FadeOut(height), FadeOut(limit_note), FadeOut(base_note), FadeOut(formula),
            run_time=.36,
        )
        self.play(source_outline.animate.set_stroke(INK, width=4), run_time=.25)
        ex = self.example_stack(
            "Given: r = 4 cm",
            r"A=\pi r^2",
            r"A=\pi(4)^2=16\pi",
            r"A\approx50.27\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def semicircle_explicit(self):
        h = self.header(
            12,
            "9 · SEMICIRCLE",
            "A diameter divides one circle into two congruent regions, so each has half the circle's area.",
        )
        strip = self.stage_strip(); self.add(h, strip)

        center = np.array([-3.85, -.35, 0]); radius = 1.82
        outline = Circle(radius, color=INK, stroke_width=5, fill_opacity=0).move_to(center)
        diameter = Line(center + LEFT*radius, center + RIGHT*radius, color=INK, stroke_width=4)
        upper = Sector(
            arc_center=center, radius=radius, start_angle=0, angle=PI,
            stroke_color=INK, stroke_width=3,
            fill_color=FILL, fill_opacity=.78,
        )
        lower = Sector(
            arc_center=center, radius=radius, start_angle=PI, angle=PI,
            stroke_color=LIGHT, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=1,
        )

        self.mark_stage(strip, 0)
        self.play(Create(outline), run_time=.55)
        self.play(Create(diameter), FadeIn(upper), FadeIn(lower), run_time=.60)
        half_note = self.txt("1 of 2 equal regions", 27, True).next_to(outline, DOWN, buff=.32)
        self.play(FadeIn(half_note), run_time=.35)

        self.mark_stage(strip, 1)
        rline = Line(center, center + RIGHT*radius, color=INK, stroke_width=3.5)
        rlab = self.eq("r", 38).next_to(rline, UP, buff=.06)
        dlab = self.eq("d=2r", 35).next_to(diameter, DOWN, buff=.10)
        self.play(Create(rline), FadeIn(rlab), FadeIn(dlab), run_time=.58)

        self.mark_stage(strip, 2)
        deriv = VGroup(
            self.eq(r"A_{circle}=\pi r^2", 47),
            self.eq(r"A_{semi}=\frac12A_{circle}", 47),
            self.box(r"A_{semi}=\frac{\pi r^2}{2}", 5.85, 58),
        ).arrange(DOWN, buff=.25).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item, shift=UP*.03), run_time=.38); self.wait(.25)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), run_time=.32)
        ex = self.example_stack(
            "Given: r = 6 cm",
            r"A=\frac{\pi r^2}{2}",
            r"A=\frac{\pi(6)^2}{2}=18\pi",
            r"A\approx56.55\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def quarter_circle_explicit(self):
        h = self.header(
            13,
            "10 · QUARTER CIRCLE (QUADRANT)",
            "Two perpendicular radii isolate one of four congruent quarters of a circle.",
        )
        strip = self.stage_strip(); self.add(h, strip)

        center = np.array([-3.95, -.55, 0]); radius = 1.92
        outline = Circle(radius, color=INK, stroke_width=5, fill_opacity=0).move_to(center)
        horizontal = Line(center + LEFT*radius, center + RIGHT*radius, color=LIGHT, stroke_width=2.2)
        vertical = Line(center + DOWN*radius, center + UP*radius, color=LIGHT, stroke_width=2.2)
        quarters = VGroup(*[
            Sector(
                arc_center=center, radius=radius,
                start_angle=k*PI/2, angle=PI/2,
                stroke_color=LIGHT, stroke_width=1.2,
                fill_color=PAPER, fill_opacity=.42,
            ) for k in range(4)
        ])

        self.mark_stage(strip, 0)
        self.play(Create(outline), run_time=.55)
        self.play(Create(horizontal), Create(vertical), FadeIn(quarters), run_time=.60)
        self.play(
            quarters[0].animate.set_fill(FILL, opacity=.82).set_stroke(INK, width=4.0),
            run_time=.45,
        )
        qnote = self.txt("1 of 4 equal regions", 27, True).next_to(outline, DOWN, buff=.30)
        self.play(FadeIn(qnote), run_time=.35)

        self.mark_stage(strip, 1)
        r1 = Line(center, center + RIGHT*radius, color=INK, stroke_width=4)
        r2 = Line(center, center + UP*radius, color=INK, stroke_width=4)
        labs = VGroup(
            self.eq("r", 37).next_to(r1, DOWN, buff=.06),
            self.eq("r", 37).next_to(r2, LEFT, buff=.06),
            self.right_mark(center, RIGHT, UP, .28),
        )
        self.play(Create(r1), Create(r2), FadeIn(labs), run_time=.55)

        self.mark_stage(strip, 2)
        deriv = VGroup(
            self.eq(r"A_{circle}=\pi r^2", 47),
            self.eq(r"A_{quarter}=\frac14A_{circle}", 47),
            self.box(r"A_{quarter}=\frac{\pi r^2}{4}", 5.90, 58),
        ).arrange(DOWN, buff=.25).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item, shift=UP*.03), run_time=.38); self.wait(.25)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), run_time=.32)
        ex = self.example_stack(
            "Given: r = 8 cm",
            r"A=\frac{\pi r^2}{4}",
            r"A=\frac{\pi(8)^2}{4}=16\pi",
            r"A\approx50.27\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def formula_atlas(self):
        h = self.header(
            14,
            "COMPLETE 2D AREA FORMULA ATLAS",
            "The symbols in each formula correspond to dimensions you can point to on the figure.",
        )
        self.add(h)

        data = [
            ("SQUARE", r"A=s^2"),
            ("RECTANGLE", r"A=bh"),
            ("TRIANGLE", r"A=\frac{bh}{2}"),
            ("PARALLELOGRAM", r"A=bh"),
            ("TRAPEZOID", r"A=\frac{(B+b)h}{2}"),
            ("RHOMBUS", r"A=\frac{Dd}{2}"),
            ("CIRCLE", r"A=\pi r^2"),
            ("REGULAR POLYGON", r"A=\frac{Pa}{2}"),
            ("SEMICIRCLE", r"A=\frac{\pi r^2}{2}"),
            ("QUARTER CIRCLE", r"A=\frac{\pi r^2}{4}"),
        ]

        cards = VGroup()
        for name, formula in data:
            r = RoundedRectangle(
                width=6.35, height=.78, corner_radius=.09,
                stroke_color=INK, stroke_width=1.6,
                fill_color=PAPER, fill_opacity=1,
            )
            name_m = self.txt(name, 23, True)
            self.fit(name_m, 2.65, .40)
            formula_m = self.eq(formula, 35)
            self.fit(formula_m, 2.70, .48)
            divider = Line(ORIGIN+DOWN*.26, ORIGIN+UP*.26, color=LIGHT, stroke_width=1.2)
            name_m.move_to(r.get_center() + LEFT*1.65)
            divider.move_to(r.get_center())
            formula_m.move_to(r.get_center() + RIGHT*1.62)
            cards.add(VGroup(r, name_m, divider, formula_m))

        cards.arrange_in_grid(rows=5, cols=2, buff=(.24, .12)).shift(DOWN*.30)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*.04) for c in cards], lag_ratio=.045), run_time=1.45)
        self.wait(4.40)
        self.wipe()
