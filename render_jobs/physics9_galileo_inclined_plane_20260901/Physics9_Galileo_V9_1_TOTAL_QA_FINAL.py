#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V9.1 total QA correction.

This is the corrective render source for the V9 lesson.  It inherits the V9
Scene 06 sequencing fix and rebuilds the two remaining high-risk layouts with
larger geometric safety margins:

* Scene 09 uses three genuinely independent table columns, short two-line
  headers, a shallower table, and reserved note/equation bands.
* Scene 12 uses 0.26-unit equation gaps and a lower isolated impact callout.
* Existing V9/V8 runtime bounding-box checks remain active; this revision does
  not bypass QA in order to obtain a render.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pql -> -pqh.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

import Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL as v7mod
from Physics9_Galileo_V9_TOTAL_QA_FINAL import Physics9GalileoV9TotalQAFinal


class Physics9GalileoV91TotalQAFinal(Physics9GalileoV9TotalQAFinal):
    """V9 final with conservative Scene 09/12 spacing and full runtime QA."""

    def falling_motion_bridge_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            9,
            "THE SAME SQUARE-TIME PATTERN APPEARS IN IDEAL FREE FALL",
            "Use the same 0.50 s clock spacing. Near Earth, a released object follows y = 1/2 g t² with g ≈ 9.81 m/s².",
        )

        # LEFT LANE — physical fall.  It is intentionally isolated from the
        # numerical table by more than three scene units horizontally.
        x = -4.95
        top_y, bottom_y = 1.58, -1.50
        times = np.array([0.00, 0.50, 1.00, 1.50, 2.00])
        dist = 0.5 * 9.81 * times**2
        interval = [None] + list(np.diff(dist))
        frac = dist / dist[-1]
        ys = top_y - frac * (top_y - bottom_y)

        fall_line = Line(
            [x, top_y + 0.16, 0], [x, bottom_y - 0.12, 0],
            color=BLACK, stroke_width=3,
        )
        ball = Circle(
            radius=0.16, stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([x, ys[0], 0])
        ghosts = VGroup(*[
            Dot([x, y, 0], radius=0.05, color=v7mod.MID_GRAY) for y in ys
        ])
        fall_caption = self.txt(
            "equal 0.50 s snapshots", 22, BOLD, color=v7mod.DARK_GRAY,
        ).move_to([x, -2.02, 0])

        # RIGHT LANE — the screenshot failure came from three long headings
        # sharing a baseline.  V9.1 gives every column its own two-line header
        # and physical separators.
        table_border = RoundedRectangle(
            width=7.25, height=2.95, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([2.45, 0.20, 0])

        col_x = [-0.15, 2.20, 4.80]
        h1 = self._two_line_header("TIME", "t (s)", [col_x[0], 1.28, 0], 23, 21)
        h2 = self._two_line_header("TOTAL DISTANCE", "y (m)", [col_x[1], 1.28, 0], 22, 21)
        h3 = self._two_line_header("INTERVAL DISTANCE", "Δy (m)", [col_x[2], 1.28, 0], 21, 21)
        self.fit(h1, 1.65, 0.62)
        self.fit(h2, 2.10, 0.62)
        self.fit(h3, 2.18, 0.62)
        headings = VGroup(h1, h2, h3)

        hline = Line([-1.03, 0.86, 0], [5.93, 0.86, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.5)
        vline1 = Line([0.95, 1.52, 0], [0.95, -1.13, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.1)
        vline2 = Line([3.57, 1.52, 0], [3.57, -1.13, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.1)

        body = VGroup()
        row_y = [0.59, 0.22, -0.15, -0.52, -0.89]
        for i, y in enumerate(row_y):
            body.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 27).move_to([col_x[0], y, 0]),
                self.txt(f"{dist[i]:0.2f}", 27, BOLD).move_to([col_x[1], y, 0]),
                self.txt("—" if i == 0 else f"{interval[i]:0.2f}", 27).move_to([col_x[2], y, 0]),
            ))

        table = VGroup(table_border, headings, hline, vline1, vline2, body)
        note = self.txt("same mathematical structure: distance ∝ time²", 24, BOLD)
        self.fit(note, 6.65, 0.42)
        note.move_to([2.45, -1.65, 0])

        eq_ramp = self.formula_panel(
            r"s=0.40t^2\quad\text{(inclined-plane reconstruction)}",
            width=6.25, height=0.82, size=28,
        ).move_to([2.45, -2.50, 0])
        eq_fall = self.formula_panel(
            r"\boxed{y=\frac12gt^2}",
            width=6.25, height=0.86, size=42,
        ).move_to([2.45, -2.50, 0])

        # Hard runtime QA: these are real geometric margins, not relaxed gates.
        self._assert_disjoint(h1, h2, pad=0.18, label="scene09 header time/total")
        self._assert_disjoint(h2, h3, pad=0.18, label="scene09 header total/interval")
        self._assert_disjoint(fall_line, table_border, pad=0.70, label="scene09 physical/table lanes")
        self._assert_disjoint(table_border, note, pad=0.12, label="scene09 table/note")
        self._assert_disjoint(note, eq_ramp, pad=0.18, label="scene09 note/equation")
        for obj, label in [
            (table, "scene09 table"),
            (note, "scene09 note"),
            (eq_ramp, "scene09 ramp equation"),
            (eq_fall, "scene09 fall equation"),
            (fall_caption, "scene09 fall caption"),
        ]:
            self._assert_inside(obj, label)

        self.play(Create(fall_line), FadeIn(ball), FadeIn(fall_caption), run_time=RUN)
        self.play(
            FadeIn(table_border), FadeIn(headings),
            Create(hline), Create(vline1), Create(vline2),
            run_time=RUN,
        )
        self.add(ghosts[0])

        for i, row in enumerate(body):
            self.play(FadeIn(row, shift=RIGHT * 0.04), run_time=0.52)
            if i > 0:
                self.play(
                    ball.animate.move_to([x, ys[i], 0]),
                    FadeIn(ghosts[i]),
                    run_time=1.00,
                    rate_func=rate_functions.ease_in_quad,
                )
                self.wait(0.38)

        self.wait(v7mod.PAUSE_READ)
        self.play(FadeIn(note, shift=UP * 0.025), run_time=RUN)
        self.wait(0.35)
        self.play(FadeIn(eq_ramp, shift=UP * 0.03), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_READ)

        # Sequential replacement prevents transient doubled formula glyphs.
        self.play(FadeOut(eq_ramp, shift=DOWN * 0.03), run_time=0.60)
        self.remove(eq_ramp)
        self.wait(0.15)
        self.play(FadeIn(eq_fall, shift=UP * 0.03), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()

    def pisa_numeric_drop_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            12,
            "NUMERICAL PISA CHECK: SAME HEIGHT -> SAME IDEAL FALL TIME",
            "Drop both compact objects from rest at h = 20 m. The mass never appears in the fall-time equation.",
        )

        h = 20.0
        g = 9.81
        t_hit = math.sqrt(2 * h / g)
        vf = g * t_hit

        # LEFT LANE — two masses, same vertical displacement.
        x1, x2 = -4.65, -2.75
        top_y, bottom_y = 1.42, -1.58
        p1 = Line([x1, top_y, 0], [x1, bottom_y, 0], color=v7mod.LIGHT_GRAY, stroke_width=2)
        p2 = Line([x2, top_y, 0], [x2, bottom_y, 0], color=v7mod.LIGHT_GRAY, stroke_width=2)
        ground = Line([-5.65, bottom_y, 0], [-1.70, bottom_y, 0], color=BLACK, stroke_width=2.4)
        b1 = Circle(radius=0.17, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(p1.get_start())
        b2 = Circle(radius=0.28, color=BLACK, fill_color=v7mod.LIGHT_GRAY, fill_opacity=1).move_to(p2.get_start())
        labels = VGroup(
            self.math(r"1\,\mathrm{kg}", 27).next_to(b1, UP, buff=0.14),
            self.math(r"10\,\mathrm{kg}", 27).next_to(b2, UP, buff=0.14),
        )
        height = DoubleArrow(
            [-5.45, top_y, 0], [-5.45, bottom_y, 0], buff=0.03,
            color=v7mod.MID_GRAY, stroke_width=1.5,
            max_tip_length_to_length_ratio=0.05,
        )
        hlab = self.math(r"h=20\,\mathrm{m}", 26).next_to(height, LEFT, buff=0.10)

        # RIGHT LANE — reserve a fixed equation stack with 0.26-unit gaps.
        calc_title = self.txt("SOLVE THE FALL TIME", 29, BOLD).move_to([3.65, 1.90, 0])
        clock_box = RoundedRectangle(
            width=3.20, height=0.58, corner_radius=0.08,
            stroke_color=v7mod.MID_GRAY, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([3.65, 1.22, 0])
        clock_label = self.txt("elapsed time:", 22, BOLD)
        clock_num = DecimalNumber(0.0, num_decimal_places=2, font_size=32, color=BLACK)
        clock_unit = self.txt("s", 22, BOLD)
        clock_content = VGroup(clock_label, clock_num, clock_unit).arrange(RIGHT, buff=0.10).move_to(clock_box)
        clock = VGroup(clock_box, clock_content)

        e1 = self.math(r"h=\frac12gt^2", 38).next_to(clock, DOWN, buff=0.26)
        e2 = self.math(r"20=\frac12(9.81)t^2", 37).next_to(e1, DOWN, buff=0.26)
        e3 = self.math(r"t=\sqrt{\frac{2(20)}{9.81}}", 37).next_to(e2, DOWN, buff=0.26)
        e4 = self.formula_panel(
            r"\boxed{t\approx2.02\,\mathrm{s}}",
            width=4.10, height=0.78, size=37,
        ).next_to(e3, DOWN, buff=0.26)

        self._assert_disjoint(labels, clock, pad=0.24, label="scene12 labels/clock")
        self._assert_disjoint(calc_title, clock, pad=0.10, label="scene12 title/clock")
        self._assert_disjoint(clock, e1, pad=0.18, label="scene12 clock/e1")
        self._assert_disjoint(e1, e2, pad=0.18, label="scene12 e1/e2")
        self._assert_disjoint(e2, e3, pad=0.18, label="scene12 e2/e3")
        self._assert_disjoint(e3, e4, pad=0.18, label="scene12 e3/e4")
        for obj, label in [
            (labels, "scene12 mass labels"),
            (clock, "scene12 clock"),
            (e1, "scene12 e1"),
            (e2, "scene12 e2"),
            (e3, "scene12 e3"),
            (e4, "scene12 e4"),
        ]:
            self._assert_inside(obj, label)

        self.play(
            Create(p1), Create(p2), Create(ground),
            FadeIn(b1), FadeIn(b2), FadeIn(labels), FadeIn(height), FadeIn(hlab),
            run_time=RUN,
        )
        self.play(FadeIn(calc_title), FadeIn(clock), Write(e1), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_READ)

        tracker = ValueTracker(0.0)
        def y(alpha):
            return top_y + (bottom_y - top_y) * (alpha**2)

        b1.add_updater(lambda m: m.move_to([x1, y(tracker.get_value()), 0]))
        b2.add_updater(lambda m: m.move_to([x2, y(tracker.get_value()), 0]))
        clock_num.add_updater(lambda m: m.set_value(t_hit * tracker.get_value()))
        self.play(tracker.animate.set_value(1.0), run_time=3.55, rate_func=linear)
        b1.clear_updaters()
        b2.clear_updaters()
        clock_num.clear_updaters()
        self.wait(v7mod.PAUSE_SHORT)

        self.play(FadeIn(e2, shift=UP * 0.03), run_time=RUN)
        self.wait(0.55)
        self.play(FadeIn(e3, shift=UP * 0.03), run_time=RUN)
        self.wait(0.55)
        self.play(FadeIn(e4), run_time=RUN)
        self.wait(0.45)

        impact = self.formula_panel(
            r"\boxed{t_1=t_2=2.02\,\mathrm{s}}",
            width=4.55, height=0.78, size=33,
        ).move_to([-3.70, -2.62, 0])
        speed = self.math(rf"v_f=gt\approx{vf:.1f}\,\mathrm{{m/s}}", 29)
        speed.next_to(e4, DOWN, buff=0.22)

        self._assert_disjoint(VGroup(b1, b2), impact, pad=0.20, label="scene12 balls/impact")
        self._assert_disjoint(e4, speed, pad=0.14, label="scene12 e4/speed")
        self._assert_inside(impact, "scene12 impact")
        self._assert_inside(speed, "scene12 speed")

        self.play(FadeIn(impact), FadeIn(speed), run_time=RUN)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()
