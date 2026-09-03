#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V9 Total QA Final.

V9 is a real render revision built from the latest V8 source after reviewing
both the reported video frames and the failed V8 PQL log.

Concrete fixes in this revision:
* Scene 06: the equal-time equation never shares a fade transition with the
  numerical timeline, eliminating the faint/ghosted equation seen behind it.
* Scene 09: the free-fall data area is rebuilt as a bordered three-column table
  with two-line headers and explicit column separators, so "distance" and
  "interval distance" cannot merge.
* Scene 12: the numerical Pisa calculation is laid out with geometry-driven
  next_to spacing.  This fixes the exact V8 PQL failure where the clock and
  first equation had only 0.02 scene units of visual gap.
* Critical V9 blocks use runtime disjoint/boundary assertions.
* Pacing remains deliberately slow and staged for classroom reading.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pql -> -pqh.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

import Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL as v7mod
from Physics9_Galileo_V8_DIRECT_DELIVERY_FINAL import (
    Physics9GalileoV8DirectDeliveryFinal,
)


class Physics9GalileoV9TotalQAFinal(Physics9GalileoV8DirectDeliveryFinal):
    """V9: final overlap-safe Galileo + Pisa classroom presentation."""

    # ------------------------------------------------------------------
    # Additional V9 geometry QA
    # ------------------------------------------------------------------
    def _assert_inside(self, mob, label="object", x_limit=6.80, y_limit=3.70):
        x0, x1, y0, y1 = self._bbox(mob)
        if x0 < -x_limit or x1 > x_limit or y0 < -y_limit or y1 > y_limit:
            raise ValueError(
                f"{label}: outside safe frame: "
                f"bbox=({x0:.2f},{x1:.2f},{y0:.2f},{y1:.2f})"
            )

    def _two_line_header(self, top, bottom, center, top_size=23, bottom_size=21):
        group = VGroup(
            self.txt(top, top_size, BOLD),
            self.txt(bottom, bottom_size, BOLD, color=v7mod.DARK_GRAY),
        ).arrange(DOWN, buff=0.035)
        group.move_to(center)
        return group

    # ------------------------------------------------------------------
    # Scene 06 — clean motion/timeline/equality sequencing
    # ------------------------------------------------------------------
    def galileo_timed_run_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            6,
            "THE INCLINED-PLANE RUN WITH REAL NUMERICAL TIMES",
            "Every interval is exactly Δt = 0.50 s in this classroom reconstruction; the ball travels farther in each new interval.",
        )

        release, lower, _, _ = self._ramp_geometry()
        ramp = Line(lower, release, color=BLACK, stroke_width=5)
        floor = Line([-5.55, -0.78, 0], [2.55, -0.78, 0], color=BLACK, stroke_width=2)
        support = Line(release, [release[0], -0.78, 0], color=v7mod.MID_GRAY, stroke_width=2)
        pts = self._ramp_points()
        ball = Circle(
            radius=0.19, stroke_color=BLACK, stroke_width=2.1,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(pts[0])
        ghosts = VGroup(*[Dot(p, radius=0.055, color=v7mod.MID_GRAY) for p in pts])

        # Lower the timeline slightly and reserve the entire band for it.
        timeline, xs, cells, time_labels = self._timeline_numeric(y=-2.24)
        live_box = RoundedRectangle(
            width=3.45, height=1.15, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([4.65, 0.28, 0])
        live_t = self.txt("t = 0.00 s", 28, BOLD).move_to(live_box.get_center() + UP * 0.20)
        live_s = self.txt("s = 0.00 m", 26, BOLD, color=v7mod.DARK_GRAY).move_to(live_box.get_center() + DOWN * 0.24)
        live = VGroup(live_box, live_t, live_s)
        measured = self.txt("measured along the ramp", 22, BOLD, color=v7mod.DARK_GRAY).move_to([4.65, 1.18, 0])

        positions = [0.00, 0.10, 0.40, 0.90, 1.60]
        times = [0.00, 0.50, 1.00, 1.50, 2.00]

        self._assert_disjoint(ramp, timeline, pad=0.16, label="scene06 ramp/timeline")
        self._assert_disjoint(timeline, live, pad=0.12, label="scene06 timeline/live box")
        self._assert_inside(timeline, "scene06 timeline")
        self._assert_inside(live, "scene06 live box")

        self.play(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(timeline), FadeIn(live), FadeIn(measured), run_time=RUN)
        self.add(ghosts[0])
        self.wait(v7mod.PAUSE_SHORT)

        for i in range(1, 5):
            nt = self.txt(f"t = {times[i]:0.2f} s", 28, BOLD).move_to(live_t)
            ns = self.txt(f"s = {positions[i]:0.2f} m", 26, BOLD, color=v7mod.DARK_GRAY).move_to(live_s)
            self.play(
                ball.animate.move_to(pts[i]),
                Transform(live_t, nt),
                Transform(live_s, ns),
                cells[i - 1].animate.set_fill(v7mod.LIGHT_GRAY, opacity=0.85),
                run_time=1.65,
                rate_func=rate_functions.ease_in_quad,
            )
            self.play(FadeIn(ghosts[i], scale=1.45), run_time=0.24)
            self.wait(0.55)

        self.wait(v7mod.PAUSE_READ)

        # V9 rule: the formula is NEVER faded over the timeline.  Remove the
        # timeline band first, then dedicate a clean band to the conclusion.
        self.play(
            FadeOut(timeline, shift=DOWN * 0.04),
            FadeOut(live),
            FadeOut(measured),
            run_time=0.75,
        )
        self.remove(timeline, live, measured)
        self.wait(0.18)

        equality = self.formula_panel(
            r"\boxed{\Delta t_1=\Delta t_2=\Delta t_3=\Delta t_4=0.50\,\mathrm{s}}",
            width=8.10, height=0.96, size=35,
        ).move_to([-0.95, -2.08, 0])
        self._assert_disjoint(VGroup(ramp, floor), equality, pad=0.18, label="scene06 ramp/equality")
        self._assert_inside(equality, "scene06 equality")
        self.play(FadeIn(equality, shift=UP * 0.04), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_EXPLAIN)

        # Complete removal before the scene-wide fade prevents a residual ghost.
        self.play(FadeOut(equality, shift=DOWN * 0.035), run_time=0.55)
        self.remove(equality)
        self.wait(0.15)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Scene 09 — rebuilt free-fall table with non-overlapping headers
    # ------------------------------------------------------------------
    def falling_motion_bridge_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            9,
            "THE SAME SQUARE-TIME PATTERN APPEARS IN IDEAL FREE FALL",
            "Use the same 0.50 s clock spacing. Near Earth, a released object follows y = 1/2 g t² with g ≈ 9.81 m/s².",
        )

        # Left physical lane.
        x = -4.95
        top_y, bottom_y = 1.58, -1.50
        times = np.array([0.00, 0.50, 1.00, 1.50, 2.00])
        dist = 0.5 * 9.81 * times**2
        frac = dist / dist[-1]
        ys = top_y - frac * (top_y - bottom_y)
        fall_line = Line([x, top_y + 0.16, 0], [x, bottom_y - 0.12, 0], color=BLACK, stroke_width=3)
        ball = Circle(
            radius=0.16, stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([x, ys[0], 0])
        ghosts = VGroup(*[Dot([x, y, 0], radius=0.05, color=v7mod.MID_GRAY) for y in ys])
        fall_caption = self.txt("equal 0.50 s snapshots", 22, BOLD, color=v7mod.DARK_GRAY).move_to([x, -2.02, 0])

        # Right table lane.  Headers are intentionally two lines rather than
        # forcing three long phrases into one baseline.
        table_border = RoundedRectangle(
            width=7.55, height=3.42, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([2.35, 0.02, 0])
        col_x = [-0.30, 2.15, 4.85]
        h1 = self._two_line_header("time", "t (s)", [col_x[0], 1.28, 0], 24, 22)
        h2 = self._two_line_header("distance fallen", "y (m)", [col_x[1], 1.28, 0], 23, 22)
        h3 = self._two_line_header("interval distance", "per 0.50 s (m)", [col_x[2], 1.28, 0], 22, 20)
        headings = VGroup(h1, h2, h3)
        hline = Line([-1.16, 0.88, 0], [5.86, 0.88, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.5)
        vline1 = Line([0.82, 1.60, 0], [0.82, -1.58, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.1)
        vline2 = Line([3.48, 1.60, 0], [3.48, -1.58, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.1)

        interval = [None] + list(np.diff(dist))
        body = VGroup()
        row_y = [0.57, 0.08, -0.41, -0.90, -1.39]
        for i, y in enumerate(row_y):
            body.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 27).move_to([col_x[0], y, 0]),
                self.txt(f"{dist[i]:0.2f}", 27, BOLD).move_to([col_x[1], y, 0]),
                self.txt("—" if i == 0 else f"{interval[i]:0.2f}", 27).move_to([col_x[2], y, 0]),
            ))

        table = VGroup(table_border, headings, hline, vline1, vline2, body)
        note = self.txt("same mathematical structure: distance ∝ time²", 24, BOLD)
        self.fit(note, 6.7, 0.48)
        note.move_to([2.35, -1.98, 0])
        eq_ramp = self.formula_panel(
            r"s=0.40t^2\quad\text{(inclined-plane reconstruction)}",
            width=6.30, height=0.82, size=28,
        ).move_to([2.35, -2.72, 0])
        eq_fall = self.formula_panel(
            r"\boxed{y=\frac12gt^2}",
            width=6.30, height=0.86, size=42,
        ).move_to([2.35, -2.72, 0])

        self._assert_disjoint(h1, h2, pad=0.22, label="scene09 header time/distance")
        self._assert_disjoint(h2, h3, pad=0.22, label="scene09 header distance/interval")
        self._assert_disjoint(fall_line, table_border, pad=0.55, label="scene09 physical/table lanes")
        self._assert_disjoint(table_border, note, pad=0.08, label="scene09 table/note")
        self._assert_disjoint(note, eq_ramp, pad=0.12, label="scene09 note/equation")
        for obj, label in [
            (table, "scene09 table"), (note, "scene09 note"),
            (eq_ramp, "scene09 ramp equation"), (fall_caption, "scene09 fall caption"),
        ]:
            self._assert_inside(obj, label)

        self.play(Create(fall_line), FadeIn(ball), FadeIn(fall_caption), run_time=RUN)
        self.play(FadeIn(table_border), FadeIn(headings), Create(hline), Create(vline1), Create(vline2), run_time=RUN)
        self.add(ghosts[0])
        for i, row in enumerate(body):
            self.play(FadeIn(row, shift=RIGHT * 0.05), run_time=0.48)
            if i > 0:
                self.play(
                    ball.animate.move_to([x, ys[i], 0]),
                    FadeIn(ghosts[i]),
                    run_time=0.92,
                    rate_func=rate_functions.ease_in_quad,
                )
                self.wait(0.32)

        self.wait(v7mod.PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN)
        self.play(FadeIn(eq_ramp, shift=UP * 0.03), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_READ)

        # No TransformMatchingTex here: completely remove one panel before the
        # next enters, avoiding transient doubled glyphs.
        self.play(FadeOut(eq_ramp, shift=DOWN * 0.03), run_time=0.55)
        self.remove(eq_ramp)
        self.play(FadeIn(eq_fall, shift=UP * 0.03), run_time=v7mod.RUN_SLOW)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Scene 12 — geometry-driven equation spacing fixes failed V8 PQL gate
    # ------------------------------------------------------------------
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

        # Left experiment lane.
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

        # Right calculation lane.  Every equation is positioned relative to the
        # preceding object, not with guessed absolute y coordinates.
        calc_title = self.txt("SOLVE THE FALL TIME", 29, BOLD).move_to([3.65, 1.82, 0])
        clock_box = RoundedRectangle(
            width=3.15, height=0.58, corner_radius=0.08,
            stroke_color=v7mod.MID_GRAY, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([3.65, 1.15, 0])
        clock_label = self.txt("elapsed time:", 22, BOLD)
        clock_num = DecimalNumber(0.0, num_decimal_places=2, font_size=32, color=BLACK)
        clock_unit = self.txt("s", 22, BOLD)
        clock_content = VGroup(clock_label, clock_num, clock_unit).arrange(RIGHT, buff=0.10).move_to(clock_box)
        clock = VGroup(clock_box, clock_content)

        e1 = self.math(r"h=\frac12gt^2", 38)
        e1.next_to(clock, DOWN, buff=0.20)
        e2 = self.math(r"20=\frac12(9.81)t^2", 37)
        e2.next_to(e1, DOWN, buff=0.20)
        e3 = self.math(r"t=\sqrt{\frac{2(20)}{9.81}}", 37)
        e3.next_to(e2, DOWN, buff=0.20)
        e4 = self.formula_panel(
            r"\boxed{t\approx2.02\,\mathrm{s}}",
            width=4.10, height=0.78, size=37,
        )
        e4.next_to(e3, DOWN, buff=0.20)

        self._assert_disjoint(labels, clock, pad=0.20, label="scene12 labels/clock")
        self._assert_disjoint(calc_title, clock, pad=0.08, label="scene12 title/clock")
        self._assert_disjoint(clock, e1, pad=0.12, label="scene12 clock/e1")
        self._assert_disjoint(e1, e2, pad=0.12, label="scene12 e1/e2")
        self._assert_disjoint(e2, e3, pad=0.12, label="scene12 e2/e3")
        self._assert_disjoint(e3, e4, pad=0.12, label="scene12 e3/e4")
        for obj, label in [
            (labels, "scene12 mass labels"), (clock, "scene12 clock"),
            (e1, "scene12 e1"), (e2, "scene12 e2"),
            (e3, "scene12 e3"), (e4, "scene12 e4"),
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
        self.play(tracker.animate.set_value(1.0), run_time=3.45, rate_func=linear)
        b1.clear_updaters()
        b2.clear_updaters()
        clock_num.clear_updaters()
        self.wait(v7mod.PAUSE_SHORT)

        # Solve only after the observed simultaneous impact; this avoids a wall
        # of formulas appearing before the experiment and improves pacing.
        self.play(FadeIn(e2, shift=UP * 0.035), run_time=RUN)
        self.wait(0.45)
        self.play(FadeIn(e3, shift=UP * 0.035), run_time=RUN)
        self.wait(0.45)
        self.play(FadeIn(e4), run_time=RUN)

        impact = self.formula_panel(
            r"\boxed{t_1=t_2=2.02\,\mathrm{s}}",
            width=4.55, height=0.78, size=33,
        ).move_to([-3.70, -2.48, 0])
        speed = self.math(rf"v_f=gt\approx{vf:.1f}\,\mathrm{{m/s}}", 29)
        speed.next_to(e4, DOWN, buff=0.18)
        self._assert_disjoint(VGroup(b1, b2), impact, pad=0.16, label="scene12 balls/impact")
        self._assert_disjoint(e4, speed, pad=0.10, label="scene12 e4/speed")
        self._assert_inside(impact, "scene12 impact")
        self._assert_inside(speed, "scene12 speed")

        self.play(FadeIn(impact), FadeIn(speed), run_time=RUN)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()
