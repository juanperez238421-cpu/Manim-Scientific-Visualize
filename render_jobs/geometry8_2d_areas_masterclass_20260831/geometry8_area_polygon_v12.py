#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V12 regular-polygon derivation layout QA.

V12 preserves the validated V11 story and rebuilds only STAGE 03 · DERIVE.
The V11 screenshot exposed a real collision: BUILD THE FORMULA, ONE TRIANGLE,
the extracted triangle, and the stacked equations shared the same vertical band.

V12 uses explicit non-intersecting zones inside a taller panel:
- title band at the top;
- triangle visual on the upper-left;
- one-triangle formula on the upper-right;
- six-triangle equation in a dedicated middle row;
- perimeter substitution and final formula in a dedicated bottom row.

Runtime bounding-box assertions guard the critical gaps before animation.
Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaPolygonV12Mixin:
    """V11 regular-polygon story with an overlap-free derivation panel."""

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
        # STAGE 03 · DERIVE — V12 fixed-zone layout.
        # ==============================================================
        self.mark_stage(strip, 2)
        self.play(
            FadeOut(parts_title),
            FadeOut(parts_sub),
            FadeOut(label_note),
            FadeOut(center_label),
            run_time=.25,
        )

        # V12: a taller panel with explicit title / upper / middle / final rows.
        # This replaces the V11 stack where title, triangle-name, triangle and
        # equations occupied the same vertical band.
        deriv_panel = self._safe_panel(
            6.15,
            4.15,
            RIGHT * 3.55 + DOWN * .55,
            stroke=LIGHT,
            fill=WHITE,
            opacity=.997,
        )
        deriv_title = self.txt("BUILD THE FORMULA", 23, True)
        deriv_title.move_to(deriv_panel.get_top() + DOWN * .29)
        self.play(FadeIn(deriv_panel), FadeIn(deriv_title), run_time=.34)

        # Upper-left zone: isolated triangle only. No heading sits above it.
        tri_center = np.array([2.10, .06, 0])
        tri_visual = Polygon(
            tri_center + np.array([-.88, -.38, 0]),
            tri_center + np.array([.88, -.38, 0]),
            tri_center + np.array([0, .66, 0]),
            stroke_color=INK,
            stroke_width=3.0,
            fill_color=FILL,
            fill_opacity=.42,
        )
        tri_alt = DashedLine(
            tri_center + np.array([0, .66, 0]),
            tri_center + np.array([0, -.38, 0]),
            color=INK,
            stroke_width=2.3,
        )
        tri_s = self.eq("s", 27).next_to(tri_visual, DOWN, buff=.035)
        tri_a = self.eq("a", 27).next_to(tri_alt, RIGHT, buff=.06)

        # Upper-right zone: one-triangle formula, fully separated from drawing.
        eq1_label = self.txt("AREA OF ONE TRIANGLE", 18, True)
        eq1_label.move_to(RIGHT * 4.70 + UP * .46)
        eq1 = self.eq(r"A_1=\frac{s\,a}{2}", 34)
        eq1.move_to(RIGHT * 4.70 + DOWN * .02)
        eq1_group = VGroup(eq1_label, eq1)

        divider_1 = Line(
            np.array([.92, -.69, 0]),
            np.array([6.18, -.69, 0]),
            color=LIGHT,
            stroke_width=1.5,
        )

        # Middle row: the six-triangle multiplication gets its own horizontal lane.
        eq2_label = self.txt("6 TRIANGLES", 18, True)
        eq2_label.move_to(RIGHT * 1.52 + DOWN * 1.07)
        eq2 = self.eq(r"A=6A_1=6\left(\frac{s\,a}{2}\right)", 32)
        self.fit(eq2, 4.05, .58)
        eq2.move_to(RIGHT * 4.28 + DOWN * 1.07)
        eq2_group = VGroup(eq2_label, eq2)

        divider_2 = Line(
            np.array([.92, -1.51, 0]),
            np.array([6.18, -1.51, 0]),
            color=LIGHT,
            stroke_width=1.5,
        )

        # Bottom row: perimeter substitution and final boxed formula.
        eq3 = self.eq(r"P=6s", 29)
        eq3.move_to(RIGHT * 1.52 + DOWN * 2.06)
        arrow = self.eq(r"\Longrightarrow", 27)
        arrow.move_to(RIGHT * 3.02 + DOWN * 2.06)
        formula = self.box(r"A=\frac{P\,a}{2}", 2.30, 38)
        formula.move_to(RIGHT * 4.85 + DOWN * 2.06)
        final_row = VGroup(eq3, arrow, formula)
        self.fit(final_row, 5.15, .68)
        final_row.move_to(RIGHT * 3.55 + DOWN * 2.06)

        # Runtime geometric QA: fail the render if the protected zones collide.
        triangle_group = VGroup(tri_visual, tri_alt, tri_s, tri_a)
        assert deriv_title.get_bottom()[1] > max(triangle_group.get_top()[1], eq1_group.get_top()[1]) + .10
        assert triangle_group.get_right()[0] + .16 < eq1_group.get_left()[0]
        assert eq1_group.get_bottom()[1] > divider_1.get_y() + .10
        assert eq2_group.get_top()[1] < divider_1.get_y() - .10
        assert eq2_group.get_bottom()[1] > divider_2.get_y() + .10
        assert final_row.get_top()[1] < divider_2.get_y() - .10
        assert final_row.get_bottom()[1] > deriv_panel.get_bottom()[1] + .12

        self.play(
            TransformFromCopy(one_triangle, tri_visual),
            FadeIn(tri_alt),
            FadeIn(tri_s),
            FadeIn(tri_a),
            run_time=.58,
        )
        self.wait(.34)
        self.play(FadeIn(eq1_label), Write(eq1), run_time=.46)
        self.wait(.38)
        self.play(Create(divider_1), run_time=.22)
        self.play(FadeIn(eq2_label), Write(eq2), run_time=.48)
        self.wait(.40)
        self.play(Create(divider_2), run_time=.22)
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
            FadeOut(eq1),
            FadeOut(eq1_label),
            FadeOut(eq2),
            FadeOut(eq2_label),
            FadeOut(divider_1),
            FadeOut(divider_2),
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
