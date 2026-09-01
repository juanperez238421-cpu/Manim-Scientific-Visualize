#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *

class Geometry8AreaAtlasHelpersMixin:
    """Shared visual language and summary screens for the figure-by-figure area atlas."""

    def stage_strip(self):
        labels = ["CONSTRUCT", "PARTS", "DERIVE", "EXAMPLE"]
        items = VGroup()
        for label in labels:
            box = RoundedRectangle(
                width=1.95,
                height=.48,
                corner_radius=.08,
                stroke_color=LIGHT,
                stroke_width=1.5,
                fill_color=WHITE,
                fill_opacity=1,
            )
            text = self.txt(label, 20, True).move_to(box)
            items.add(VGroup(box, text))
        items.arrange(RIGHT, buff=.10)
        items.to_edge(RIGHT, buff=.45).shift(UP * 2.58)
        return items

    def mark_stage(self, strip, index):
        animations = []
        for i, item in enumerate(strip):
            target_width = 3.2 if i == index else 1.5
            target_fill = PAPER if i == index else WHITE
            animations.append(item[0].animate.set_stroke(INK if i == index else LIGHT, width=target_width).set_fill(target_fill, opacity=1))
        self.play(*animations, run_time=.28)

    def dimension(self, start, end, label, label_direction=DOWN, size=36):
        arrow = DoubleArrow(start, end, buff=0, color=INK, stroke_width=2.2)
        lab = self.eq(label, size).next_to(arrow, label_direction, buff=.05)
        return VGroup(arrow, lab)

    def right_mark(self, corner, x_dir=RIGHT, y_dir=UP, size=.28):
        p0 = np.array(corner, dtype=float)
        p1 = p0 + x_dir * size
        p2 = p1 + y_dir * size
        p3 = p0 + y_dir * size
        return VMobject(color=INK, stroke_width=2.2).set_points_as_corners([p1, p2, p3])

    def example_stack(self, given, formula, substitution, result, width=6.25):
        title = self.txt("WORKED EXAMPLE", 29, True)
        given_m = self.txt(given, 27)
        formula_m = self.eq(formula, 43)
        sub_m = self.eq(substitution, 40)
        answer = self.box(result, width, 49)
        check = self.txt("Check: the answer uses square units.", 25, True)
        group = VGroup(title, given_m, formula_m, sub_m, answer, check).arrange(DOWN, buff=.18)
        self.fit(group, width, 4.70)
        return group

    def show_example(self, stack, right_x=3.55):
        stack.move_to(RIGHT * right_x + DOWN * .10)
        for i, item in enumerate(stack):
            self.play(FadeIn(item, shift=UP * .03), run_time=.38)
            if i in (1, 2, 3):
                self.wait(.30)
        self.wait(1.55)

    def atlas_opening(self):
        title = VGroup(
            self.txt("GEOMETRY 8 · AREA OF 2D FIGURES", 54, True),
            self.txt("FIGURE-BY-FIGURE CONSTRUCTION ATLAS", 58, True),
            self.txt("Build it · name its parts · derive its area · solve one example", 31),
        ).arrange(DOWN, buff=.17).shift(UP * 1.65)
        # The opening is intentionally fit as one unit: this keeps the long
        # atlas title inside the 16:9 safe area on every renderer/font metric.
        self.fit(title, 14.55, 2.05)

        labels = ["1  CONSTRUCT", "2  PARTS", "3  DERIVE", "4  EXAMPLE"]
        cards = VGroup()
        for label in labels:
            r = RoundedRectangle(
                width=3.15,
                height=1.35,
                corner_radius=.12,
                stroke_color=INK,
                stroke_width=2,
                fill_color=PAPER,
                fill_opacity=1,
            )
            t = self.txt(label, 27, True).move_to(r)
            cards.add(VGroup(r, t))
        cards.arrange(RIGHT, buff=.25).shift(DOWN * .35)

        note = self.txt("Every formula must come from the geometry — not from memorization alone.", 31, True).shift(DOWN * 2.15)
        self.fit(note, 14.30, .65)

        self.play(Write(title[0]), run_time=.70)
        self.play(Write(title[1]), FadeIn(title[2]), run_time=1.00)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .07) for c in cards], lag_ratio=.10), run_time=1.15)
        self.play(FadeIn(note), run_time=.55)
        self.wait(2.70)
        self.wipe()

    def formula_atlas(self):
        h=self.header(14,"COMPLETE 2D AREA FORMULA ATLAS","The symbols in each formula correspond to dimensions you can point to on the figure.")
        self.add(h)

        data=[
            ("SQUARE",r"A=s^2"),
            ("RECTANGLE",r"A=bh"),
            ("TRIANGLE",r"A=\frac{bh}{2}"),
            ("PARALLELOGRAM",r"A=bh"),
            ("TRAPEZOID",r"A=\frac{(B+b)h}{2}"),
            ("RHOMBUS",r"A=\frac{Dd}{2}"),
            ("CIRCLE",r"A=\pi r^2"),
            ("REGULAR POLYGON",r"A=\frac{Pa}{2}"),
            ("SEMICIRCLE",r"A=\frac{\pi r^2}{2}"),
            ("QUARTER CIRCLE",r"A=\frac{\pi r^2}{4}"),
        ]
        cards=VGroup()
        for name,formula in data:
            r=RoundedRectangle(width=2.75,height=1.72,corner_radius=.11,stroke_color=INK,stroke_width=1.8,fill_color=PAPER,fill_opacity=1)
            t=self.txt(name,21,True); self.fit(t,2.42,.42)
            e=self.eq(formula,31); self.fit(e,2.40,.62)
            c=VGroup(t,e).arrange(DOWN,buff=.15).move_to(r)
            cards.add(VGroup(r,c))
        cards.arrange_in_grid(rows=2,cols=5,buff=(.18,.25)).shift(DOWN*.28)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.05) for c in cards],lag_ratio=.06),run_time=1.50)
        self.wait(4.00)
        self.wipe()

    def final_method(self):
        h=self.header(15,"HOW TO SOLVE ANY BASIC AREA PROBLEM","Do not start with arithmetic. Start by reading the geometry and identifying the required dimensions.")
        self.add(h)
        steps=[
            "1 · IDENTIFY THE FIGURE",
            "2 · LABEL THE REQUIRED PARTS",
            "3 · WRITE THE AREA FORMULA",
            "4 · SUBSTITUTE WITH UNITS",
            "5 · CALCULATE",
            "6 · REPORT SQUARE UNITS",
        ]
        cards=VGroup()
        for text in steps:
            r=RoundedRectangle(width=4.25,height=1.28,corner_radius=.11,stroke_color=INK,stroke_width=2,fill_color=PAPER,fill_opacity=1)
            t=self.txt(text,26,True); self.fit(t,3.85,.72); t.move_to(r); cards.add(VGroup(r,t))
        cards.arrange_in_grid(rows=2,cols=3,buff=(.30,.28)).shift(DOWN*.15)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.05) for c in cards],lag_ratio=.09),run_time=1.35)
        self.wait(3.00)
        end=self.txt("CONSTRUCT → IDENTIFY → DERIVE → CALCULATE → VERIFY",34,True).to_edge(DOWN,buff=.30)
        self.play(FadeIn(end),run_time=.55)
        self.wait(3.20)
