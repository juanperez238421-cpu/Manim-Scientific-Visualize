#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V8 TEXT-SAFE Senior QA.

V8 keeps the validated V5/V6/V7 geometry and mathematics, but replaces the
remaining collision-prone text compositions found in a dense full-video review.

Senior QA corrections:
- worked examples use two physically separate cells per row (label / value),
  rather than free-positioned text around a divider;
- runtime layout-contract assertions verify every label/value stays inside its
  own cell with a positive inter-cell gutter;
- the rectangle derivation is isolated in a protected right-side panel so its
  explanatory sentence cannot touch the height dimension;
- the circle rearrangement explanation is revealed sequentially: the visual
  limit statement disappears before the circumference-half equation appears.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaTextSafeV8Mixin:
    """Senior QA text-layout overrides with explicit bounding-box contracts."""

    # ------------------------------------------------------------------
    # Generic layout contracts
    # ------------------------------------------------------------------
    def _assert_inside(self, inner, outer, margin=.045, name="object"):
        """Fail the render if an object escapes its reserved visual cell."""
        assert inner.get_left()[0] >= outer.get_left()[0] + margin, f"{name}: left overflow"
        assert inner.get_right()[0] <= outer.get_right()[0] - margin, f"{name}: right overflow"
        assert inner.get_bottom()[1] >= outer.get_bottom()[1] + margin, f"{name}: bottom overflow"
        assert inner.get_top()[1] <= outer.get_top()[1] - margin, f"{name}: top overflow"

    def _example_cell_row(self, number, label, value, *, answer=False):
        """Build one row from two disjoint bordered cells: label | value."""
        label_cell = RoundedRectangle(
            width=1.68,
            height=.70,
            corner_radius=.075,
            stroke_color=INK if answer else LIGHT,
            stroke_width=1.55 if answer else 1.30,
            fill_color=PAPER,
            fill_opacity=1,
        )
        value_cell = RoundedRectangle(
            width=3.90,
            height=.70,
            corner_radius=.075,
            stroke_color=INK if answer else LIGHT,
            stroke_width=2.05 if answer else 1.30,
            fill_color=PAPER if answer else WHITE,
            fill_opacity=1,
        )

        badge = RoundedRectangle(
            width=.47,
            height=.34,
            corner_radius=.065,
            stroke_color=INK,
            stroke_width=1.25,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.txt(number, 14, True).move_to(badge)
        lab = self.txt(label, 15, True).set_opacity(.76 if not answer else 1.0)
        self.fit(lab, .96, .27)
        label_content = VGroup(VGroup(badge, num), lab).arrange(RIGHT, buff=.075).move_to(label_cell)

        # Value text is constrained to a completely independent cell.
        self.fit(value, 3.55, .47)
        value.move_to(value_cell)

        left_group = VGroup(label_cell, label_content)
        right_group = VGroup(value_cell, value)
        row = VGroup(left_group, right_group).arrange(RIGHT, buff=.16)

        # Runtime layout contract: changing fonts/renderers must not silently
        # reintroduce V7's label/value collisions.
        self._assert_inside(label_content, label_cell, .045, f"row {number} label")
        self._assert_inside(value, value_cell, .055, f"row {number} value")
        assert left_group.get_right()[0] + .10 <= right_group.get_left()[0], f"row {number}: gutter collapsed"
        return row

    def example_stack(self, given, formula, substitution, result, width=6.15):
        """Cell-based notebook panel with guaranteed non-overlapping text zones."""
        panel = RoundedRectangle(
            width=6.35,
            height=5.22,
            corner_radius=.14,
            stroke_color=LIGHT,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=.992,
        )

        title = self.txt("WORKED EXAMPLE", 30, True)
        title.move_to(panel.get_center() + UP*2.20)

        guide = self.txt("READ  →  FORMULA  →  SUBSTITUTE  →  ANSWER", 17, True).set_opacity(.58)
        self.fit(guide, 5.55, .29)
        guide.move_to(panel.get_center() + UP*1.84)

        top_rule = Line(
            panel.get_left() + RIGHT*.28 + UP*1.57,
            panel.get_right() + LEFT*.28 + UP*1.57,
            color=LIGHT,
            stroke_width=1.20,
        )

        row1 = self._example_cell_row("01", "GIVEN", self.txt(given, 23))
        row2 = self._example_cell_row("02", "FORMULA", self.eq(formula, 37))
        row3 = self._example_cell_row("03", "SUBSTITUTE", self.eq(substitution, 34))
        row4 = self._example_cell_row("04", "ANSWER", self.eq(result, 34), answer=True)
        rows = VGroup(row1, row2, row3, row4).arrange(DOWN, buff=.12)
        rows.move_to(panel.get_center() + DOWN*.25)

        check = self.txt("✓ Square units checked", 18, True).set_opacity(.76)
        self.fit(check, 5.45, .32)
        check.move_to(panel.get_center() + DOWN*2.24)

        # Panel-level contracts protect against vertical crowding as well.
        self._assert_inside(rows, panel, .18, "worked-example rows")
        self._assert_inside(title, panel, .10, "worked-example title")
        self._assert_inside(guide, panel, .10, "worked-example guide")
        self._assert_inside(check, panel, .10, "worked-example check")
        assert guide.get_bottom()[1] > top_rule.get_center()[1] + .07, "guide/rule overlap"
        assert top_rule.get_center()[1] > rows.get_top()[1] + .07, "rule/rows overlap"
        assert rows.get_bottom()[1] > check.get_top()[1] + .07, "rows/check overlap"

        content = VGroup(title, guide, top_rule, row1, row2, row3, row4, check)
        return VGroup(panel, content)

    def show_example(self, stack, right_x=3.55):
        """Reveal each complete text-safe row, preserving explicit student logic."""
        # Lower than V7: this leaves a guaranteed gap under the stage strip.
        stack.move_to(RIGHT*right_x + DOWN*.62)
        panel, content = stack

        assert panel.get_top()[1] < 2.12, "worked-example panel entered stage-strip zone"
        assert panel.get_right()[0] < 7.30, "worked-example panel exceeded right safe area"

        self.play(FadeIn(panel, shift=UP*.025), run_time=.36)
        self.play(FadeIn(content[0], shift=UP*.02), run_time=.32)
        self.play(FadeIn(content[1]), Create(content[2]), run_time=.34)
        self.wait(.55)

        pauses = (.90, 1.00, 1.05, 1.30)
        for row, pause in zip(content[3:7], pauses):
            self.play(FadeIn(row, shift=UP*.02), run_time=.42)
            self.wait(pause)

        self.play(FadeIn(content[7], shift=UP*.015), run_time=.32)
        self.wait(2.05)

    # ------------------------------------------------------------------
    # Confirmed V7 collision: rectangle derivation vs height dimension
    # ------------------------------------------------------------------
    def rectangle_explicit(self):
        h = self.header(5, "2 · RECTANGLE", "Opposite sides are equal; base and perpendicular height count columns and rows.")
        strip = self.stage_strip(); self.add(h, strip)

        A=np.array([-5.65,-1.20,0]); B=np.array([-1.15,-1.20,0]); C=np.array([-1.15,1.25,0]); D=np.array([-5.65,1.25,0])
        base=Line(A,B,color=INK,stroke_width=5); side=Line(B,C,color=INK,stroke_width=5); top=Line(C,D,color=INK,stroke_width=5); left=Line(D,A,color=INK,stroke_width=5)
        fill=Polygon(A,B,C,D,stroke_opacity=0,fill_color=FILL,fill_opacity=.62)

        self.mark_stage(strip,0)
        self.play(Create(base), run_time=.55)
        self.play(Create(side), Create(top), Create(left), run_time=.80)
        self.play(FadeIn(fill), run_time=.35)

        self.mark_stage(strip,1)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        dh=self.dimension(B+RIGHT*.35,C+RIGHT*.35,"h",RIGHT)
        right=VGroup(self.right_mark(A),self.right_mark(B,LEFT,UP),self.right_mark(C,LEFT,DOWN),self.right_mark(D,RIGHT,DOWN))
        self.play(GrowFromCenter(db[0]),GrowFromCenter(dh[0]),FadeIn(db[1]),FadeIn(dh[1]),FadeIn(right),run_time=.70)

        self.mark_stage(strip,2)
        deriv_panel = RoundedRectangle(
            width=5.55, height=3.05, corner_radius=.12,
            stroke_color=LIGHT, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=.99,
        ).move_to(RIGHT*4.18 + DOWN*.05)
        lead=self.txt("b columns repeated through h rows",26,True)
        self.fit(lead,4.90,.43)
        sum_eq=self.eq(r"A=\underbrace{b+b+\cdots+b}_{h\ \text{rows}}",38)
        self.fit(sum_eq,4.85,.70)
        formula=self.box(r"A=b\,h",4.75,58)
        deriv=VGroup(lead,sum_eq,formula).arrange(DOWN,buff=.27).move_to(deriv_panel)
        self.fit(deriv,4.95,2.55)
        deriv.move_to(deriv_panel)
        self._assert_inside(deriv,deriv_panel,.16,"rectangle derivation")
        assert deriv_panel.get_left()[0] > dh.get_right()[0] + .35, "rectangle derivation entered height-dimension zone"

        self.play(FadeIn(deriv_panel,shift=RIGHT*.03),run_time=.30)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.025),run_time=.40); self.wait(.30)

        self.mark_stage(strip,3)
        self.play(FadeOut(VGroup(deriv_panel,deriv)),run_time=.35)
        ex=self.example_stack("Given: b = 8 cm, h = 3 cm",r"A=b\,h",r"A=(8)(3)",r"A=24\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    # ------------------------------------------------------------------
    # Confirmed V7 collision: circle limit note + circumference equation
    # ------------------------------------------------------------------
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
        self.fit(divide_note,5.35,.45)
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

        # V8: show the geometry interpretation and the algebra on separate beats.
        limit_note = self.txt("More sectors → straighter top and bottom edges", 24, True)
        self.fit(limit_note,5.25,.42)
        limit_note.move_to(RIGHT*3.52 + UP*1.72)
        self.play(FadeIn(limit_note), run_time=.42)
        self.wait(.78)
        self.play(FadeOut(limit_note), run_time=.28)

        base_note = self.eq(r"\frac{C}{2}=\frac{2\pi r}{2}=\pi r", 38)
        self.fit(base_note,5.10,.60)
        base_note.move_to(RIGHT*3.48 + UP*1.68)
        self.play(FadeIn(base_note,shift=UP*.02),run_time=.42)
        self.wait(.62)

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
            FadeOut(sectors), FadeOut(base), FadeOut(height), FadeOut(base_note), FadeOut(formula),
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
