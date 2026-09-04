#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V11 explicit regular-polygon chapter.

V11 replaces the V10 polygon chapter with one single, coherent visual story:

1. Start from a familiar regular hexagon.
2. Count its six equal sides.
3. Locate the center and split the hexagon into six congruent triangles.
4. Isolate ONE triangle and identify base ``s`` and apothem ``a``.
5. Derive A_triangle = sa/2.
6. Add the six triangles and substitute P = 6s to obtain A = Pa/2.
7. Solve one numerical example in four explicit rows.

The goal is to reduce cognitive load: no house-shaped composite polygon, no sudden
abstract summation, and no dense forest of labels.  The complete V10 lesson is
otherwise preserved through inheritance.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaPolygonV11Mixin:
    """Single-story, step-by-step regular polygon explanation."""

    def regular_polygon_explicit(self):
        h = self.header(
            11,
            "8 · REGULAR POLYGONS",
            "A regular polygon can be split into equal triangles. Build the formula one step at a time.",
        )
        strip = self.stage_strip()
        self.add(h, strip)

        # ------------------------------------------------------------------
        # LEFT TEACHING FIGURE: a large regular hexagon with generous margins.
        # ------------------------------------------------------------------
        center = np.array([-4.10, -0.25, 0])
        R = 1.70
        start_angle = PI / 6
        vertices = [
            center
            + R
            * np.array(
                [
                    math.cos(start_angle + k * TAU / 6),
                    math.sin(start_angle + k * TAU / 6),
                    0,
                ]
            )
            for k in range(6)
        ]

        hexagon = Polygon(
            *vertices,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.48,
        )

        # ==============================================================
        # STAGE 01 · CONSTRUCT — recognize and count the six sides.
        # ==============================================================
        self.mark_stage(strip, 0)
        self.play(Create(hexagon), run_time=.78)

        title = self.txt("REGULAR HEXAGON", 27, True)
        title.move_to(RIGHT * 3.55 + UP * 1.23)
        rule = self.txt("6 sides · all sides have the same length", 25, False)
        rule.move_to(RIGHT * 3.55 + UP * .74)
        self.play(FadeIn(title), FadeIn(rule), run_time=.40)
        self.wait(.55)

        # A moving side highlight gives students a clear one-by-one count
        # without leaving six permanent labels around the polygon.
        counter_panel = self._safe_panel(
            4.55,
            .88,
            RIGHT * 3.55 + DOWN * .10,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.995,
        )
        counter_label = self.txt("COUNT THE SIDES", 21, True)
        counter_value = self.txt("1 / 6", 30, True)
        counter_group = VGroup(counter_label, counter_value).arrange(RIGHT, buff=.35)
        self.fit(counter_group, 4.10, .58)
        counter_group.move_to(counter_panel)
        self.play(FadeIn(counter_panel), FadeIn(counter_group), run_time=.30)

        side_highlight = Line(vertices[0], vertices[1], color=INK, stroke_width=9)
        self.play(Create(side_highlight), run_time=.28)
        for i in range(1, 6):
            next_side = Line(vertices[i], vertices[(i + 1) % 6], color=INK, stroke_width=9)
            next_value = self.txt(f"{i + 1} / 6", 30, True)
            next_counter = VGroup(counter_label.copy(), next_value).arrange(RIGHT, buff=.35)
            self.fit(next_counter, 4.10, .58)
            next_counter.move_to(counter_panel)
            self.play(
                Transform(side_highlight, next_side),
                Transform(counter_group, next_counter),
                run_time=.30,
            )
            self.wait(.12)

        conclusion = self.txt("So n = 6 equal sides", 25, True)
        conclusion.move_to(counter_panel)
        self.play(FadeOut(counter_group), FadeIn(conclusion), run_time=.28)
        self.wait(.55)
        self.play(FadeOut(side_highlight), FadeOut(counter_panel), FadeOut(conclusion), run_time=.28)

        # ==============================================================
        # STAGE 02 · PARTS — center, triangles, side s and apothem a.
        # ==============================================================
        self.mark_stage(strip, 1)
        self.play(FadeOut(title), FadeOut(rule), run_time=.25)

        center_dot = Dot(center, radius=.075, color=INK)
        center_label = self.txt("CENTER", 20, True).next_to(center_dot, DOWN, buff=.13)
        parts_title = self.txt("CONNECT THE CENTER TO EVERY VERTEX", 24, True)
        parts_title.move_to(RIGHT * 3.55 + UP * 1.20)
        parts_sub = self.txt("The hexagon becomes 6 equal triangles", 24, False)
        parts_sub.move_to(RIGHT * 3.55 + UP * .73)

        self.play(FadeIn(center_dot), FadeIn(center_label), FadeIn(parts_title), FadeIn(parts_sub), run_time=.40)

        spokes = VGroup()
        for v in vertices:
            spokes.add(Line(center, v, color=LIGHT, stroke_width=2.3))

        triangle_count_panel = self._safe_panel(
            4.35,
            .80,
            RIGHT * 3.55 + DOWN * .05,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.995,
        )
        triangle_count = self.txt("Triangle 1 of 6", 25, True).move_to(triangle_count_panel)
        self.play(FadeIn(triangle_count_panel), FadeIn(triangle_count), run_time=.28)

        # Build each radial division sequentially and briefly highlight the new
        # triangle. Only the spokes remain, keeping the final picture clean.
        for i in range(6):
            tri = Polygon(
                center,
                vertices[i],
                vertices[(i + 1) % 6],
                stroke_color=INK,
                stroke_width=2.2,
                fill_color=WHITE,
                fill_opacity=.72,
            )
            new_count = self.txt(f"Triangle {i + 1} of 6", 25, True).move_to(triangle_count_panel)
            self.play(
                Create(spokes[i]),
                FadeIn(tri),
                Transform(triangle_count, new_count),
                run_time=.32,
            )
            self.wait(.12)
            self.play(FadeOut(tri), run_time=.16)

        self.wait(.35)
        self.play(FadeOut(triangle_count_panel), FadeOut(triangle_count), run_time=.24)

        # Identify ONE side and ONE apothem only after the six-triangle idea is
        # already understood. This avoids simultaneous-label overload.
        chosen_side = Line(vertices[0], vertices[1], color=INK, stroke_width=7)
        side_mid = (vertices[0] + vertices[1]) / 2
        apothem = DashedLine(center, side_mid, color=INK, stroke_width=3.0)
        side_label = self.eq("s", 34).next_to(chosen_side, UR, buff=.08)
        apothem_label = self.eq("a", 34).next_to(apothem, RIGHT, buff=.10)

        ap_dir = (side_mid - center) / np.linalg.norm(side_mid - center)
        side_dir = (vertices[1] - vertices[0]) / np.linalg.norm(vertices[1] - vertices[0])
        right_mark = self.right_mark(side_mid, -ap_dir, side_dir, .20)

        one_triangle = Polygon(
            center,
            vertices[0],
            vertices[1],
            stroke_color=INK,
            stroke_width=3,
            fill_color=WHITE,
            fill_opacity=.78,
        )
        label_note = self.txt("For ONE triangle: base = s, height = a", 24, True)
        label_note.move_to(RIGHT * 3.55 + DOWN * .12)

        self.play(
            FadeIn(one_triangle),
            Create(chosen_side),
            Create(apothem),
            FadeIn(side_label),
            FadeIn(apothem_label),
            FadeIn(right_mark),
            FadeIn(label_note),
            run_time=.65,
        )
        self.wait(.75)

        # ==============================================================
        # STAGE 03 · DERIVE — isolate one triangle, then scale to all six.
        # ==============================================================
        self.mark_stage(strip, 2)
        self.play(
            FadeOut(parts_title),
            FadeOut(parts_sub),
            FadeOut(label_note),
            FadeOut(center_label),
            run_time=.25,
        )

        # Dedicated right-side derivation panel. Each row is fixed and spaced;
        # nothing is allowed to share the polygon's drawing zone.
        deriv_panel = self._safe_panel(
            5.90,
            3.65,
            RIGHT * 3.55 + DOWN * .42,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.997,
        )
        deriv_title = self.txt("BUILD THE FORMULA", 24, True)
        deriv_title.move_to(deriv_panel.get_top() + DOWN * .34)
        self.play(FadeIn(deriv_panel), FadeIn(deriv_title), run_time=.34)

        # Visual extraction: transform a copy of the highlighted wedge into a
        # clean teaching triangle inside the panel.
        tri_center = np.array([3.55, .18, 0])
        tri_visual = Polygon(
            tri_center + np.array([-1.12, -.48, 0]),
            tri_center + np.array([1.12, -.48, 0]),
            tri_center + np.array([0, .86, 0]),
            stroke_color=INK,
            stroke_width=3.2,
            fill_color=FILL,
            fill_opacity=.42,
        )
        tri_alt = DashedLine(
            tri_center + np.array([0, .86, 0]),
            tri_center + np.array([0, -.48, 0]),
            color=INK,
            stroke_width=2.4,
        )
        tri_s = self.eq("s", 29).next_to(tri_visual, DOWN, buff=.05)
        tri_a = self.eq("a", 29).next_to(tri_alt, RIGHT, buff=.07)
        tri_name = self.txt("ONE TRIANGLE", 20, True).next_to(tri_visual, UP, buff=.08)

        self.play(
            TransformFromCopy(one_triangle, tri_visual),
            FadeIn(tri_alt),
            FadeIn(tri_s),
            FadeIn(tri_a),
            FadeIn(tri_name),
            run_time=.60,
        )
        self.wait(.40)

        eq1 = self.eq(r"A_1=\frac{s\,a}{2}", 35)
        eq1.move_to(RIGHT * 3.55 + DOWN * 1.35)
        eq1_label = self.txt("1 triangle", 19, True).next_to(eq1, LEFT, buff=.26)
        self.play(FadeIn(eq1_label), Write(eq1), run_time=.46)
        self.wait(.42)

        eq2 = self.eq(r"A=6A_1=6\left(\frac{s\,a}{2}\right)", 34)
        eq2.move_to(RIGHT * 3.55 + DOWN * 1.92)
        eq2_label = self.txt("6 triangles", 19, True).next_to(eq2, LEFT, buff=.26)
        self.play(FadeIn(eq2_label), Write(eq2), run_time=.48)
        self.wait(.42)

        # Replace 6s by the perimeter explicitly instead of jumping to a
        # summation expression.
        eq3 = self.eq(r"P=6s", 33)
        eq3.move_to(RIGHT * 2.55 + DOWN * 2.48)
        arrow = self.eq(r"\Longrightarrow", 31)
        arrow.next_to(eq3, RIGHT, buff=.22)
        formula = self.box(r"A=\frac{P\,a}{2}", 2.75, 42)
        formula.next_to(arrow, RIGHT, buff=.22)
        final_row = VGroup(eq3, arrow, formula)
        self.fit(final_row, 5.20, .62)
        final_row.move_to(RIGHT * 3.55 + DOWN * 2.48)
        self.play(FadeIn(eq3), FadeIn(arrow), FadeIn(formula), run_time=.55)
        self.wait(1.05)

        # ==============================================================
        # STAGE 04 · EXAMPLE — four explicit numbered rows.
        # ==============================================================
        self.mark_stage(strip, 3)
        self.play(
            FadeOut(deriv_panel),
            FadeOut(deriv_title),
            FadeOut(tri_visual),
            FadeOut(tri_alt),
            FadeOut(tri_s),
            FadeOut(tri_a),
            FadeOut(tri_name),
            FadeOut(eq1),
            FadeOut(eq1_label),
            FadeOut(eq2),
            FadeOut(eq2_label),
            FadeOut(eq3),
            FadeOut(arrow),
            FadeOut(formula),
            run_time=.42,
        )

        ex_panel = self._safe_panel(
            5.95,
            3.82,
            RIGHT * 3.55 + DOWN * .38,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.997,
        )
        ex_title = self.txt("WORKED EXAMPLE · REGULAR HEXAGON", 23, True)
        ex_title.move_to(ex_panel.get_top() + DOWN * .33)

        rows = VGroup(
            self.eq(r"\boxed{1}\quad s=5\ \mathrm{cm},\quad a=4.33\ \mathrm{cm},\quad n=6", 31),
            self.eq(r"\boxed{2}\quad P=6s=6(5)=30\ \mathrm{cm}", 31),
            self.eq(r"\boxed{3}\quad A=\frac{P\,a}{2}=\frac{(30)(4.33)}{2}", 31),
            self.eq(r"\boxed{4}\quad A\approx64.95\ \mathrm{cm}^2", 34),
        ).arrange(DOWN, buff=.30, aligned_edge=LEFT)
        self.fit(rows, 5.35, 2.82)
        rows.move_to(ex_panel.get_center() + DOWN * .12)
        rows.align_to(ex_panel.get_left() + RIGHT * .30, LEFT)

        self.play(FadeIn(ex_panel), FadeIn(ex_title), run_time=.34)
        for row in rows:
            self.play(FadeIn(row, shift=UP * .025), run_time=.40)
            self.wait(.40)
        self.wait(1.10)

        # Final 1-line transfer rule. It appears only after the worked example
        # and replaces the panel, so it cannot overlap any calculation row.
        self.play(FadeOut(ex_panel), FadeOut(ex_title), FadeOut(rows), run_time=.34)
        transfer = self._safe_panel(
            5.55,
            1.30,
            RIGHT * 3.55 + DOWN * .28,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.997,
        )
        transfer_text = VGroup(
            self.txt("REMEMBER", 22, True),
            self.txt("Regular polygon: perimeter P + apothem a → A = Pa / 2", 23, True),
        ).arrange(DOWN, buff=.14)
        self.fit(transfer_text, 5.05, .92)
        transfer_text.move_to(transfer)
        self.play(FadeIn(transfer), FadeIn(transfer_text), run_time=.40)
        self.wait(.95)

        self.wipe()
