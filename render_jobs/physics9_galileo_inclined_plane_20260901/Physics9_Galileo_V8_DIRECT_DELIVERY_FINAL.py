#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V8 Direct Delivery Final, frame-QA revision.

This revision keeps the complete V8 lesson/pacing while rebuilding the three
layouts where frame-by-frame review of the rendered 1920x1080 video exposed
actual element collisions:

* Scene 07: ramp-data table vs. interval-distance heading;
* Scene 09: free-fall table column headings + lower explanatory note;
* Scene 12: live timer vs. 1 kg / 10 kg release labels and impact callout.

The corrected layouts use explicit left/right zones, larger inter-object gaps,
and runtime bounding-box assertions so a future edit cannot silently recreate
those overlaps.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pql -> -pqh.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

import Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL as v7mod
import Physics9_Galileo_V7_1_SENIOR_POLISH_FINAL as v71mod
from Physics9_Galileo_V7_1_SENIOR_POLISH_FINAL import (
    Physics9GalileoV71SeniorPolishFinal,
)


class Physics9GalileoV8DirectDeliveryFinal(Physics9GalileoV71SeniorPolishFinal):
    """V8 with senior pacing plus explicit anti-overlap geometry QA."""

    def construct(self):
        v7mod.RUN = 1.30
        v7mod.RUN_FAST = 0.95
        v7mod.RUN_SLOW = 1.85
        v7mod.PAUSE_SHORT = 1.55
        v7mod.PAUSE_READ = 2.90
        v7mod.PAUSE_EXPLAIN = 4.10
        v7mod.PAUSE_WORK = 5.20
        v71mod.RUN = 1.30
        super().construct()

    def clear_stage(self):
        """Use a smooth full-stage fade instead of an abrupt scene reset."""
        if self.mobjects:
            stage = Group(*self.mobjects)
            self.play(
                FadeOut(stage, shift=DOWN * 0.025),
                run_time=0.95,
                rate_func=smooth,
            )
        self.clear()
        self.wait(0.22)

    # ------------------------------------------------------------------
    # Frame-QA helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _bbox(mob):
        return (
            float(mob.get_left()[0]),
            float(mob.get_right()[0]),
            float(mob.get_bottom()[1]),
            float(mob.get_top()[1]),
        )

    def _assert_disjoint(self, a, b, pad=0.06, label="layout"):
        """Fail the render if two intended-disjoint visual blocks collide."""
        ax0, ax1, ay0, ay1 = self._bbox(a)
        bx0, bx1, by0, by1 = self._bbox(b)
        separated = (
            ax1 + pad <= bx0 or bx1 + pad <= ax0 or
            ay1 + pad <= by0 or by1 + pad <= ay0
        )
        if not separated:
            raise ValueError(
                f"{label}: overlap detected: "
                f"A=({ax0:.2f},{ax1:.2f},{ay0:.2f},{ay1:.2f}) "
                f"B=({bx0:.2f},{bx1:.2f},{by0:.2f},{by1:.2f})"
            )

    # ------------------------------------------------------------------
    # Scene 07 — rebuild with explicit left/right zones
    # ------------------------------------------------------------------
    def galileo_data_analysis_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            7,
            "TURN THE RAMP MEASUREMENTS INTO A DATA TABLE",
            "The time intervals stay fixed at 0.50 s, but the distance traveled during each interval grows.",
        )

        # LEFT ZONE: compact but large five-row table.  Its right edge ends at
        # x=-1.05, leaving a hard visual gutter before the interval analysis.
        x_cols = [-5.25, -3.65, -2.05]
        y_rows = [1.40, 0.78, 0.16, -0.46, -1.08, -1.70]
        headings = VGroup(
            self.txt("time t (s)", 25, BOLD).move_to([x_cols[0], y_rows[0], 0]),
            self.txt("t² (s²)", 25, BOLD).move_to([x_cols[1], y_rows[0], 0]),
            self.txt("position s (m)", 24, BOLD).move_to([x_cols[2], y_rows[0], 0]),
        )
        times = [0.00, 0.50, 1.00, 1.50, 2.00]
        t2 = [0.00, 0.25, 1.00, 2.25, 4.00]
        pos = [0.00, 0.10, 0.40, 0.90, 1.60]
        rows = VGroup()
        for i in range(5):
            y = y_rows[i + 1]
            rows.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 28).move_to([x_cols[0], y, 0]),
                self.txt(f"{t2[i]:0.2f}", 28).move_to([x_cols[1], y, 0]),
                self.txt(f"{pos[i]:0.2f}", 28, BOLD).move_to([x_cols[2], y, 0]),
            ))
        table_border = RoundedRectangle(
            width=5.55, height=4.12, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([-3.65, -0.15, 0])
        hline = Line([-6.25, 1.08, 0], [-1.05, 1.08, 0], color=v7mod.LIGHT_GRAY, stroke_width=1.4)
        table_group = VGroup(table_border, headings, rows, hline)

        # RIGHT ZONE: title and bars are centered farther right.  The title is
        # fitted to a known width instead of being allowed to grow into table.
        right_title = self.txt("DISTANCE DURING EACH 0.50 s INTERVAL", 27, BOLD)
        self.fit(right_title, 5.10, 0.55)
        right_title.move_to([3.70, 1.48, 0])

        interval_values = [0.10, 0.30, 0.50, 0.70]
        bars = VGroup()
        bar_labels = VGroup()
        starts_y = [0.72, 0.02, -0.68, -1.38]
        for i, (val, y) in enumerate(zip(interval_values, starts_y), start=1):
            lab = self.txt(f"interval {i}", 23, BOLD).move_to([1.45, y, 0])
            bar = Line(
                [2.30, y, 0], [2.30 + 2.45 * (val / 0.70), y, 0],
                color=BLACK, stroke_width=8,
            )
            valm = self.txt(f"Δs{i} = {val:0.2f} m", 22, BOLD).next_to(bar, RIGHT, buff=0.16)
            bars.add(bar)
            bar_labels.add(VGroup(lab, valm))

        ratio = self.formula_panel(
            r"0.10:0.30:0.50:0.70=\boxed{1:3:5:7}",
            width=5.55, height=0.88, size=32,
        ).move_to([3.65, -2.18, 0])
        right_group = VGroup(right_title, bars, bar_labels, ratio)

        self._assert_disjoint(table_group, right_title, pad=0.12, label="scene07 table/title")
        self._assert_disjoint(table_group, right_group, pad=0.04, label="scene07 left/right zones")

        self.play(FadeIn(table_border), FadeIn(headings), Create(hline), run_time=RUN)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.08), run_time=0.48)
        self.wait(v7mod.PAUSE_READ)
        self.play(FadeIn(right_title), run_time=RUN)
        for bar, lab in zip(bars, bar_labels):
            self.play(FadeIn(lab), Create(bar), run_time=0.78)
        self.play(FadeIn(ratio), run_time=RUN)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Scene 09 — rebuild free-fall table and lower explanation
    # ------------------------------------------------------------------
    def falling_motion_bridge_v7(self):
        RUN = v7mod.RUN
        self.header_v7(
            9,
            "THE SAME SQUARE-TIME PATTERN APPEARS IN IDEAL FREE FALL",
            "Use the same 0.50 s clock spacing. Near Earth, a released object follows y = 1/2 g t² with g ≈ 9.81 m/s².",
        )

        # LEFT: falling object, moved farther left to free horizontal room.
        x = -4.55
        top_y, bottom_y = 1.58, -1.48
        times = np.array([0.00, 0.50, 1.00, 1.50, 2.00])
        dist = 0.5 * 9.81 * times**2
        frac = dist / dist[-1]
        ys = top_y - frac * (top_y - bottom_y)
        fall_line = Line([x, top_y + 0.18, 0], [x, bottom_y - 0.12, 0], color=BLACK, stroke_width=3)
        ball = Circle(
            radius=0.16, stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([x, ys[0], 0])
        ghosts = VGroup(*[Dot([x, y, 0], radius=0.05, color=v7mod.MID_GRAY) for y in ys])

        # RIGHT: three columns with dedicated width envelopes.  The third
        # heading uses Δy notation so the pedagogical meaning is preserved
        # without forcing three long strings into the same horizontal band.
        row_x = [-0.25, 2.10, 4.95]
        head1 = self.txt("time t (s)", 24, BOLD)
        head2 = self.txt("distance y (m)", 24, BOLD)
        head3 = self.txt("Δy per 0.50 s (m)", 23, BOLD)
        self.fit(head1, 1.55, 0.48)
        self.fit(head2, 2.20, 0.48)
        self.fit(head3, 2.65, 0.48)
        head1.move_to([row_x[0], 1.32, 0])
        head2.move_to([row_x[1], 1.32, 0])
        head3.move_to([row_x[2], 1.32, 0])
        head = VGroup(head1, head2, head3)

        self._assert_disjoint(head1, head2, pad=0.16, label="scene09 headings 1/2")
        self._assert_disjoint(head2, head3, pad=0.16, label="scene09 headings 2/3")

        body = VGroup()
        interval = [None] + list(np.diff(dist))
        body_y = [0.72, 0.20, -0.32, -0.84, -1.36]
        for i, y in enumerate(body_y):
            body.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 26).move_to([row_x[0], y, 0]),
                self.txt(f"{dist[i]:0.2f}", 26, BOLD).move_to([row_x[1], y, 0]),
                self.txt("—" if i == 0 else f"{interval[i]:0.2f}", 26).move_to([row_x[2], y, 0]),
            ))

        # Explanatory note and equations get their own lower band.  In V8 the
        # note sat directly on the last table row; here there is a hard gap.
        note = self.txt("same structure: position ∝ time²", 25, BOLD)
        note.move_to([2.45, -1.78, 0])
        eq_start = self.formula_panel(
            r"s=0.40t^2\quad\text{(ramp reconstruction)}",
            width=5.55, height=0.82, size=29,
        ).move_to([2.45, -2.42, 0])
        eq_fall = self.formula_panel(
            r"\boxed{y=\frac12gt^2}",
            width=5.55, height=0.86, size=42,
        ).move_to([2.45, -2.42, 0])

        self._assert_disjoint(body[-1], note, pad=0.12, label="scene09 body/note")
        self._assert_disjoint(note, eq_start, pad=0.10, label="scene09 note/equation")

        self.play(Create(fall_line), FadeIn(ball), FadeIn(head), run_time=RUN)
        self.add(ghosts[0])
        for i, r in enumerate(body):
            self.play(FadeIn(r), run_time=0.44)
            if i > 0:
                self.play(
                    ball.animate.move_to([x, ys[i], 0]),
                    FadeIn(ghosts[i]),
                    run_time=0.82,
                    rate_func=rate_functions.ease_in_quad,
                )
        self.play(FadeIn(eq_start), run_time=RUN)
        self.wait(v7mod.PAUSE_READ)
        self.play(ReplacementTransform(eq_start, eq_fall), run_time=v7mod.RUN_SLOW)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Scene 12 — move live clock away from mass labels; clear impact zone
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

        # LEFT DROP ZONE
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

        # RIGHT CALCULATION ZONE.  The clock now lives here instead of over
        # the two mass labels, eliminating the collision visible in V8.
        calc_title = self.txt("SOLVE THE FALL TIME", 29, BOLD).move_to([3.65, 1.55, 0])
        clock_box = RoundedRectangle(
            width=3.00, height=0.58, corner_radius=0.08,
            stroke_color=v7mod.MID_GRAY, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([3.65, 1.02, 0])
        clock_label = self.txt("elapsed time:", 22, BOLD)
        clock_num = DecimalNumber(0.0, num_decimal_places=2, font_size=32, color=BLACK)
        clock_unit = self.txt("s", 22, BOLD)
        clock_content = VGroup(clock_label, clock_num, clock_unit).arrange(RIGHT, buff=0.10).move_to(clock_box)
        clock = VGroup(clock_box, clock_content)

        e1 = self.math(r"h=\frac12gt^2", 40).move_to([3.65, 0.42, 0])
        e2 = self.math(r"20=\frac12(9.81)t^2", 39).move_to([3.65, -0.18, 0])
        e3 = self.math(r"t=\sqrt{\frac{2(20)}{9.81}}", 39).move_to([3.65, -0.80, 0])
        e4 = self.formula_panel(
            r"\boxed{t\approx2.02\,\mathrm{s}}",
            width=4.15, height=0.86, size=39,
        ).move_to([3.65, -1.52, 0])

        self._assert_disjoint(labels, clock, pad=0.20, label="scene12 labels/clock")
        self._assert_disjoint(calc_title, clock, pad=0.07, label="scene12 title/clock")
        self._assert_disjoint(clock, e1, pad=0.09, label="scene12 clock/e1")

        self.play(
            Create(p1), Create(p2), Create(ground),
            FadeIn(b1), FadeIn(b2), FadeIn(labels), FadeIn(height), FadeIn(hlab),
            run_time=RUN,
        )
        self.play(FadeIn(calc_title), FadeIn(clock), Write(e1), run_time=RUN)
        self.play(TransformFromCopy(e1, e2), run_time=RUN)
        self.play(TransformFromCopy(e2, e3), run_time=RUN)
        self.play(FadeIn(e4), run_time=RUN)
        self.wait(v7mod.PAUSE_READ)

        tracker = ValueTracker(0.0)

        def y(alpha):
            return top_y + (bottom_y - top_y) * (alpha**2)

        b1.add_updater(lambda m: m.move_to([x1, y(tracker.get_value()), 0]))
        b2.add_updater(lambda m: m.move_to([x2, y(tracker.get_value()), 0]))
        clock_num.add_updater(lambda m: m.set_value(t_hit * tracker.get_value()))
        self.play(tracker.animate.set_value(1.0), run_time=3.35, rate_func=linear)
        b1.clear_updaters()
        b2.clear_updaters()
        clock_num.clear_updaters()

        impact = self.formula_panel(
            r"\boxed{t_1=t_2=2.02\,\mathrm{s}}",
            width=4.55, height=0.78, size=33,
        ).move_to([-3.70, -2.28, 0])
        speed = self.math(rf"v_f=gt\approx{vf:.1f}\,\mathrm{{m/s}}", 29).move_to([3.65, -2.32, 0])

        # At impact the callout remains clearly below the balls/ground.
        balls_at_impact = VGroup(b1, b2)
        self._assert_disjoint(balls_at_impact, impact, pad=0.10, label="scene12 balls/impact")

        self.play(FadeIn(impact), FadeIn(speed), run_time=RUN)
        self.wait(v7mod.PAUSE_EXPLAIN)
        self.clear_stage()
