#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Galileo V7 visual redesign, senior final.

Purpose of V7
-------------
This is a substantial visual/pedagogical rebuild of the V6.2 lesson after
reviewing the rendered 1920x1080 video. The redesign targets the concrete
issues visible in that render:

* eliminate crowded/overlapping captions and tiny multi-panel text;
* enlarge the main figures, equations, axes, labels and numerical examples;
* replace abstract inclined-plane labels (0, Δt, 2Δt, ...) with a concrete
  modern classroom reconstruction using Δt = 0.50 s;
* show the corresponding measured positions explicitly:
      t (s): 0.00, 0.50, 1.00, 1.50, 2.00
      s (m): 0.00, 0.10, 0.40, 0.90, 1.60
  so every interval is 0.50 s and the interval distances are
      0.10, 0.30, 0.50, 0.70 m  ->  1:3:5:7;
* use more pauses, staged reveals, copy-transforms, replacement transforms,
  moving highlights and physically legible motion;
* keep the historical water-clock explanation distinct from the modern SI
  numerical reconstruction;
* retain the Pisa mass-independence section but present it with larger objects
  and fewer simultaneous text blocks.

The numerical ramp data are an explicitly labeled classroom reconstruction;
they are not claimed to be Galileo's exact historical SI measurements.

Target: ManimCE 0.20.1, white-background JP classroom style, -pqh.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from Physics9_Galileo_Pisa_Mass_Independence_V6_2_SENIOR_FINAL import (
    Physics9GalileoPisaMassIndependenceV62SeniorFinal,
)


BLACK_TEXT = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D9D9D9"
VERY_LIGHT = "#F4F4F4"

RUN = 1.15
RUN_FAST = 0.82
RUN_SLOW = 1.55
PAUSE_SHORT = 1.25
PAUSE_READ = 2.40
PAUSE_EXPLAIN = 3.40
PAUSE_WORK = 4.60


class Physics9GalileoV7VisualRedesignSeniorFinal(Physics9GalileoPisaMassIndependenceV62SeniorFinal):
    """Complete V7 rebuild with large-layout and explicit numerical timing."""

    # ------------------------------------------------------------------
    # Data / QA
    # ------------------------------------------------------------------
    def validate_lesson_data(self):
        super().validate_lesson_data()

        # Modern classroom reconstruction of the ramp pattern.
        times = np.array([0.00, 0.50, 1.00, 1.50, 2.00])
        positions = np.array([0.00, 0.10, 0.40, 0.90, 1.60])
        interval_dt = np.diff(times)
        interval_ds = np.diff(positions)
        assert np.allclose(interval_dt, 0.50)
        assert np.allclose(interval_ds, [0.10, 0.30, 0.50, 0.70])
        assert np.allclose(positions, 0.40 * times**2)
        assert np.allclose(interval_ds / interval_ds[0], [1, 3, 5, 7])

        # Free fall bridge with same 0.50 s time spacing.
        g = 9.81
        fall_y = 0.5 * g * times**2
        assert np.allclose(fall_y, [0.0, 1.22625, 4.905, 11.03625, 19.62])

    # ------------------------------------------------------------------
    # Shared V7 helpers
    # ------------------------------------------------------------------
    def header_v7(self, number: int, title: str, subtitle: str):
        badge = RoundedRectangle(
            width=0.52, height=0.34, corner_radius=0.07,
            stroke_color=BLACK, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 19, BOLD).move_to(badge)
        title_m = self.txt(title, 30, BOLD)
        title_m.next_to(badge, RIGHT, buff=0.16)
        header = VGroup(badge, num, title_m)
        self.fit(header, 13.35, 0.58)
        header.to_edge(UP, buff=0.13).to_edge(LEFT, buff=0.30)

        subtitle_m = self.txt(subtitle, 21, color=DARK_GRAY)
        self.fit(subtitle_m, 13.5, 0.45)
        subtitle_m.next_to(header, DOWN, aligned_edge=LEFT, buff=0.08)
        line = Line(LEFT*6.80, RIGHT*6.80, color=LIGHT_GRAY, stroke_width=1.2)
        line.next_to(subtitle_m, DOWN, buff=0.08)

        self.play(FadeIn(header, shift=RIGHT*0.08), FadeIn(subtitle_m), Create(line), run_time=RUN)
        return VGroup(header, subtitle_m, line)

    def _timeline_numeric(self, y=-2.34):
        """Concrete 0.50-s timeline. Returns group, centers, cells, labels."""
        times = [0.00, 0.50, 1.00, 1.50, 2.00]
        x0, x1 = -5.15, 2.15
        xs = np.linspace(x0, x1, 5)

        base = Line([x0, y, 0], [x1, y, 0], color=BLACK, stroke_width=2.2)
        ticks = VGroup(*[
            Line([x, y-0.13, 0], [x, y+0.13, 0], color=BLACK, stroke_width=1.8)
            for x in xs
        ])
        labels = VGroup(*[
            self.txt(f"{t:0.2f} s", 22, BOLD).move_to([x, y-0.38, 0])
            for x, t in zip(xs, times)
        ])
        cells = VGroup()
        dt_labels = VGroup()
        for i in range(4):
            cx = (xs[i] + xs[i+1]) / 2
            cell = RoundedRectangle(
                width=(xs[i+1]-xs[i])-0.08, height=0.34,
                corner_radius=0.05, stroke_color=MID_GRAY, stroke_width=1.2,
                fill_color=WHITE, fill_opacity=1,
            ).move_to([cx, y+0.33, 0])
            dt = self.txt("Δt = 0.50 s", 20, BOLD, color=DARK_GRAY).move_to(cell)
            cells.add(cell)
            dt_labels.add(dt)
        return VGroup(base, ticks, cells, dt_labels, labels), xs, cells, labels

    def _ramp_geometry(self):
        release = np.array([2.15, 1.35, 0.0])
        lower = np.array([-5.15, -0.78, 0.0])
        direction = lower - release
        unit = direction / np.linalg.norm(direction)
        normal_up = np.array([unit[1], -unit[0], 0.0])
        return release, lower, unit, normal_up

    def _ramp_points(self):
        release, lower, _, normal_up = self._ramp_geometry()
        positions = np.array([0.00, 0.10, 0.40, 0.90, 1.60])
        frac = positions / positions[-1]
        pts = [release + f*(lower-release) + normal_up*0.18 for f in frac]
        return pts

    # ------------------------------------------------------------------
    # Construct
    # ------------------------------------------------------------------
    def construct(self):
        self.opening_v7()
        self.uniform_motion_v7()
        self.derive_position_equation_v7()
        self.graph_equation_connection_v7()
        self.galileo_question_v7()
        self.galileo_apparatus_v7()
        self.galileo_timed_run_v7()
        self.galileo_data_analysis_v7()
        self.galileo_square_time_graph_v7()
        self.falling_motion_bridge_v7()
        self.pisa_question_v7()
        self.pisa_force_reasoning_v7()
        self.pisa_numeric_drop_v7()
        self.air_resistance_v7()
        self.summary_v7()

    # ------------------------------------------------------------------
    # Opening / uniform motion
    # ------------------------------------------------------------------
    def opening_v7(self):
        kicker = self.txt("PHYSICS 9 | KINEMATICS", 29, BOLD)
        main = self.txt("FROM UNIFORM MOTION TO GALILEO'S FALLING-MOTION PATTERN", 43, BOLD)
        self.fit(main, 13.3, 0.80)
        sub = self.txt("Measure motion -> organize data -> build a graph -> identify the mathematical law", 27)
        self.fit(sub, 12.5, 0.55)
        eq1 = self.formula_panel(r"\boxed{x=x_i+vt}", width=4.8, height=1.15, size=52)
        arrow = Arrow(LEFT*0.50, RIGHT*0.50, color=BLACK, stroke_width=2.2)
        eq2 = self.formula_panel(r"\boxed{s\propto t^2}", width=4.8, height=1.15, size=50)
        equations = VGroup(eq1, arrow, eq2).arrange(RIGHT, buff=0.34)
        question = self.txt("What changes when the object speeds up?", 27, BOLD, color=DARK_GRAY)
        group = VGroup(kicker, main, sub, equations, question).arrange(DOWN, buff=0.42).move_to(ORIGIN)
        self.fit(group, 13.7, 6.8)

        self.play(FadeIn(kicker, shift=UP*0.12), run_time=RUN)
        self.play(Write(main), run_time=RUN_SLOW)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(eq1), run_time=RUN)
        self.play(GrowArrow(arrow), TransformFromCopy(eq1[1], eq2[1]), FadeIn(eq2[0]), run_time=RUN_SLOW)
        self.play(FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    def uniform_motion_v7(self):
        self.header_v7(
            1,
            "UNIFORM MOTION: EQUAL TIMES GIVE EQUAL DISTANCES",
            "Start with a motion we already understand: constant velocity v = 1.5 m/s.",
        )

        # Large physical track.
        track_y = 1.50
        track = Line([-5.55, track_y, 0], [1.20, track_y, 0], color=BLACK, stroke_width=4)
        ticks = VGroup()
        positions_x = np.linspace(-5.25, 0.75, 5)
        for x in positions_x:
            ticks.add(Line([x, track_y-0.16, 0], [x, track_y+0.16, 0], color=MID_GRAY, stroke_width=1.5))
        cart_body = RoundedRectangle(
            width=0.92, height=0.47, corner_radius=0.08,
            stroke_color=BLACK, stroke_width=2.0, fill_color=WHITE, fill_opacity=1,
        ).move_to([positions_x[0], track_y+0.38, 0])
        wheels = VGroup(
            Circle(radius=0.08, color=BLACK).move_to(cart_body.get_bottom()+LEFT*0.25),
            Circle(radius=0.08, color=BLACK).move_to(cart_body.get_bottom()+RIGHT*0.25),
        )
        cart = VGroup(cart_body, wheels)

        timer_box = RoundedRectangle(width=2.05, height=0.72, corner_radius=0.08,
                                     stroke_color=BLACK, stroke_width=1.8,
                                     fill_color=WHITE, fill_opacity=1).move_to([4.65, 1.48, 0])
        timer = self.txt("t = 0 s", 28, BOLD).move_to(timer_box)
        dx_label = self.formula_panel(r"\Delta x=1.5\,\mathrm{m}\;\text{each }1\,\mathrm{s}", width=5.4, height=0.85, size=31)
        dx_label.move_to([-2.25, 0.63, 0])

        self.play(Create(track), FadeIn(ticks), FadeIn(cart), FadeIn(timer_box), FadeIn(timer), run_time=RUN)
        self.play(FadeIn(dx_label), run_time=RUN)
        ghosts = VGroup(Dot([positions_x[0], track_y, 0], radius=0.055, color=MID_GRAY))
        self.add(ghosts)
        for i in range(1, 5):
            new_timer = self.txt(f"t = {i} s", 28, BOLD).move_to(timer_box)
            self.play(
                cart.animate.move_to([positions_x[i], track_y+0.38, 0]),
                Transform(timer, new_timer),
                run_time=1.30,
                rate_func=linear,
            )
            d = Dot([positions_x[i], track_y, 0], radius=0.055, color=MID_GRAY)
            ghosts.add(d)
            self.play(FadeIn(d), run_time=0.20)
        self.wait(PAUSE_READ)

        # Transform physical observations into the x-t graph.
        axes = Axes(
            x_range=[0,4.5,1], y_range=[0,7.8,1], x_length=7.0, y_length=3.15,
            axis_config={"color":BLACK, "stroke_width":2.0, "include_tip":False},
        ).move_to([-2.20, -1.08, 0])
        labs = VGroup(
            self.txt("time t (s)", 20, BOLD).next_to(axes.x_axis, DOWN, buff=0.14),
            self.txt("position x (m)", 20, BOLD).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.18),
        )
        graph_points = VGroup(*[
            Dot(axes.c2p(t, 1+1.5*t), radius=0.07, color=BLACK) for t in range(5)
        ])
        graph = axes.plot(lambda t: 1+1.5*t, x_range=[0,4], color=BLACK, stroke_width=4)
        rule = self.formula_panel(r"\boxed{v=\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}}", width=4.8, height=1.05, size=34)
        rule.move_to([4.25, -0.25, 0])
        meaning = self.txt("straight x-t line -> constant slope -> constant velocity", 23, BOLD)
        self.fit(meaning, 5.1, 0.65)
        meaning.move_to([4.25, -1.55, 0])

        self.play(FadeOut(dx_label), FadeOut(timer_box), FadeOut(timer), run_time=RUN_FAST)
        self.play(Create(axes), FadeIn(labs), run_time=RUN)
        self.play(
            LaggedStart(*[
                TransformFromCopy(ghosts[i], graph_points[i]) for i in range(5)
            ], lag_ratio=0.12),
            run_time=RUN_SLOW*1.6,
        )
        self.play(Create(graph), FadeIn(rule), run_time=RUN)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def derive_position_equation_v7(self):
        self.header_v7(
            2,
            "DEDUCE THE UNIFORM-MOTION POSITION EQUATION",
            "Start with the definition of velocity, replace displacement, then isolate final position.",
        )

        steps = [
            self.math(r"v=\frac{\Delta x}{\Delta t}", 50),
            self.math(r"v=\frac{x-x_i}{t}", 50),
            self.math(r"vt=x-x_i", 50),
            self.math(r"\boxed{x=x_i+vt}", 56),
        ]
        labels = [
            "1  Definition of velocity",
            "2  Replace displacement: Δx = x - xᵢ",
            "3  Multiply both sides by t",
            "4  Isolate the final position x",
        ]

        label = self.txt(labels[0], 28, BOLD).move_to([-3.8, 1.45, 0])
        current = steps[0].move_to([2.2, 0.55, 0])
        separator = Line([0.0, -2.4, 0], [0.0, 1.8, 0], color=LIGHT_GRAY, stroke_width=1.5)
        symbol_box = self.note_panel(
            "SYMBOLS",
            [
                "xᵢ  initial position",
                "x   final position",
                "v   constant velocity",
                "t   elapsed time",
            ],
            width=4.8, title_size=27, body_size=24,
        ).move_to([-3.8, -0.55, 0])

        self.play(FadeIn(symbol_box), Create(separator), FadeIn(label), Write(current), run_time=RUN_SLOW)
        self.wait(PAUSE_SHORT)
        for i in range(1, 4):
            new_label = self.txt(labels[i], 28, BOLD).move_to(label)
            nxt = steps[i].move_to(current)
            self.play(Transform(label, new_label), TransformMatchingTex(current, nxt), run_time=RUN_SLOW)
            current = nxt
            self.wait(PAUSE_SHORT)
        conclusion = self.txt("final position = initial position + distance added by the motion", 25, BOLD, color=DARK_GRAY)
        self.fit(conclusion, 11.8, 0.55)
        conclusion.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(conclusion), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def graph_equation_connection_v7(self):
        self.header_v7(
            3,
            "READ THE POSITION EQUATION DIRECTLY FROM THE GRAPH",
            "The intercept gives xᵢ; the slope gives v. Both parts appear in x = xᵢ + vt.",
        )
        axes = Axes(
            x_range=[0,4.5,1], y_range=[0,7.8,1], x_length=7.2, y_length=4.35,
            axis_config={"color":BLACK,"stroke_width":2.1,"include_tip":False},
        ).move_to([-2.65,-0.45,0])
        graph = axes.plot(lambda t: 1+1.5*t, x_range=[0,4], color=BLACK, stroke_width=4)
        labs = VGroup(
            self.txt("t (s)", 21, BOLD).next_to(axes.x_axis, DOWN, buff=0.14),
            self.txt("x (m)", 21, BOLD).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.18),
        )
        intercept = Dot(axes.c2p(0,1), radius=0.075, color=BLACK)
        ilab = self.formula_panel(r"x_i=1.0\,\mathrm{m}", width=2.9, height=0.75, size=30)
        ilab.move_to([-4.95, 1.05, 0])
        tri = Polygon(axes.c2p(1,2.5), axes.c2p(3,2.5), axes.c2p(3,5.5),
                      color=MID_GRAY, stroke_width=2, fill_opacity=0)
        dt = self.math(r"\Delta t=2\,\mathrm{s}", 25).next_to(tri, DOWN, buff=0.10)
        dx = self.math(r"\Delta x=3\,\mathrm{m}", 25).next_to(tri, RIGHT, buff=0.10)

        slope = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=\frac{3}{2}=1.5\,\mathrm{m/s}", width=5.2, height=1.05, size=32)
        slope.move_to([4.15, 1.15, 0])
        eq = self.formula_panel(r"\boxed{x=x_i+vt}", width=4.6, height=1.15, size=48).move_to([4.15,-0.40,0])
        map_note = self.txt("intercept -> xᵢ    |    slope -> v", 25, BOLD).move_to([4.15,-1.70,0])

        self.play(Create(axes), FadeIn(labs), run_time=RUN)
        self.play(Create(graph), FadeIn(intercept), FadeIn(ilab), run_time=RUN)
        self.play(Create(tri), FadeIn(dt), FadeIn(dx), run_time=RUN)
        self.play(TransformFromCopy(tri, slope), run_time=RUN_SLOW)
        self.play(FadeIn(eq), FadeIn(map_note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Galileo: question -> apparatus -> numerical run -> data -> graph
    # ------------------------------------------------------------------
    def galileo_question_v7(self):
        self.header_v7(
            4,
            "WHY DID GALILEO USE AN INCLINED PLANE?",
            "Free fall changes too quickly for easy timing; a shallow ramp makes the same changing-motion pattern easier to measure.",
        )

        # Start with a large vertical fall.
        fall_line = Line([-2.6, 1.55, 0], [-2.6, -1.65, 0], color=BLACK, stroke_width=4)
        ball = Circle(radius=0.20, stroke_color=BLACK, stroke_width=2.2,
                      fill_color=WHITE, fill_opacity=1).move_to(fall_line.get_start())
        fall_title = self.txt("VERTICAL FALL", 31, BOLD).move_to([-2.6, 2.05, 0])
        fall_note = self.txt("too fast to time accurately with early instruments", 26, BOLD, color=DARK_GRAY)
        fall_note.move_to([1.55, -0.25, 0])
        self.play(Create(fall_line), FadeIn(ball), FadeIn(fall_title), run_time=RUN)
        self.play(ball.animate.move_to(fall_line.get_end()), run_time=0.85, rate_func=rate_functions.ease_in_quad)
        self.play(FadeIn(fall_note), run_time=RUN)
        self.wait(PAUSE_READ)

        # Transform the same idea into a shallow ramp instead of crowding two panels.
        ramp = Line([-4.75, -1.10, 0], [3.55, 1.25, 0], color=BLACK, stroke_width=5)
        floor = Line([-5.15,-1.10,0],[4.15,-1.10,0],color=BLACK,stroke_width=2)
        support = Line([3.55,1.25,0],[3.55,-1.10,0],color=MID_GRAY,stroke_width=2)
        ramp_title = self.txt("INCLINED PLANE", 31, BOLD).move_to([-0.60, 2.02, 0])
        ramp_note = self.txt("slower motion -> positions can be marked at known times", 27, BOLD)
        ramp_note.move_to([0.10, -1.78, 0])

        self.play(
            Transform(fall_line, ramp),
            ball.animate.move_to(ramp.get_end()+UP*0.18),
            Transform(fall_title, ramp_title),
            FadeOut(fall_note),
            Create(floor),
            Create(support),
            run_time=RUN_SLOW*1.5,
        )
        self.play(FadeIn(ramp_note), run_time=RUN)
        q = self.formula_panel(
            r"\text{At equal time intervals, are the traveled distances equal?}",
            width=10.2, height=0.95, size=34,
        ).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(q), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_apparatus_v7(self):
        self.header_v7(
            5,
            "GALILEO'S MEASUREMENT IDEA: RAMP + WATER CLOCK + POSITION MARKS",
            "Historical method: repeat the release and use equal water-flow amounts to define equal time intervals.",
        )

        release, lower, _, normal_up = self._ramp_geometry()
        ramp = Line(lower, release, color=BLACK, stroke_width=5)
        floor = Line([-5.55,-0.78,0],[2.55,-0.78,0],color=BLACK,stroke_width=2)
        support = Line(release,[release[0],-0.78,0],color=MID_GRAY,stroke_width=2)
        ball = Circle(radius=0.19, stroke_color=BLACK, stroke_width=2.1,
                      fill_color=WHITE, fill_opacity=1).move_to(release + normal_up*0.18)
        release_label = self.txt("same release point", 24, BOLD).move_to([0.75, 1.95, 0])
        leader = Arrow(release_label.get_bottom()+RIGHT*0.35, ball.get_top(), buff=0.08,
                       color=MID_GRAY, stroke_width=1.6, max_tip_length_to_length_ratio=0.12)

        # Water-clock graphic, now large enough to read.
        clock_outer = RoundedRectangle(width=2.15, height=1.55, corner_radius=0.10,
                                       stroke_color=BLACK, stroke_width=2,
                                       fill_color=WHITE, fill_opacity=1).move_to([4.75, 0.85, 0])
        water = Rectangle(width=1.80, height=0.62, stroke_width=0,
                          fill_color=LIGHT_GRAY, fill_opacity=1).align_to(clock_outer, DOWN).move_to([4.75,0.53,0])
        nozzle = Line(clock_outer.get_bottom(), clock_outer.get_bottom()+DOWN*0.38, color=BLACK, stroke_width=2)
        drop = Dot(nozzle.get_end()+DOWN*0.12, radius=0.045, color=BLACK)
        cup = RoundedRectangle(width=1.70, height=0.48, corner_radius=0.06,
                               stroke_color=BLACK, stroke_width=1.8,
                               fill_color=WHITE, fill_opacity=1).next_to(drop, DOWN, buff=0.10)
        clock = VGroup(clock_outer, water, nozzle, drop, cup)
        clock_title = self.txt("WATER CLOCK", 25, BOLD).next_to(clock_outer, UP, buff=0.16)
        clock_note = self.txt("equal collected water -> equal time interval", 22, BOLD, color=DARK_GRAY)
        self.fit(clock_note, 3.8, 0.55)
        clock_note.next_to(cup, DOWN, buff=0.18)

        modern = self.note_panel(
            "MODERN CLASSROOM NUMERICAL SCALE",
            [
                "For the next animation we label each equal interval as",
                "Δt = 0.50 s.",
                "These SI values are a reconstruction, not Galileo's exact recorded seconds.",
            ], width=5.0, title_size=24, body_size=21,
        ).move_to([4.25,-1.68,0])
        self.fit(modern, 4.9, 1.95)

        self.play(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(release_label), GrowArrow(leader), run_time=RUN)
        self.play(FadeIn(clock), FadeIn(clock_title), run_time=RUN)
        self.play(FadeIn(clock_note), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(modern), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_timed_run_v7(self):
        self.header_v7(
            6,
            "THE INCLINED-PLANE RUN WITH REAL NUMERICAL TIMES",
            "Every interval is exactly Δt = 0.50 s in this classroom reconstruction; the ball travels farther in each new interval.",
        )

        release, lower, _, _ = self._ramp_geometry()
        ramp = Line(lower, release, color=BLACK, stroke_width=5)
        floor = Line([-5.55,-0.78,0],[2.55,-0.78,0],color=BLACK,stroke_width=2)
        support = Line(release,[release[0],-0.78,0],color=MID_GRAY,stroke_width=2)
        pts = self._ramp_points()
        ball = Circle(radius=0.19, stroke_color=BLACK, stroke_width=2.1,
                      fill_color=WHITE, fill_opacity=1).move_to(pts[0])
        ghosts = VGroup(*[Dot(p, radius=0.055, color=MID_GRAY) for p in pts])

        timeline, xs, cells, time_labels = self._timeline_numeric(y=-2.16)
        live_box = RoundedRectangle(width=3.45, height=1.15, corner_radius=0.10,
                                    stroke_color=BLACK, stroke_width=1.8,
                                    fill_color=WHITE, fill_opacity=1).move_to([4.65, 0.28, 0])
        live_t = self.txt("t = 0.00 s", 28, BOLD).move_to(live_box.get_center()+UP*0.20)
        live_s = self.txt("s = 0.00 m", 26, BOLD, color=DARK_GRAY).move_to(live_box.get_center()+DOWN*0.24)
        live = VGroup(live_box, live_t, live_s)

        table_header = self.txt("measured along the ramp", 22, BOLD, color=DARK_GRAY).move_to([4.65, 1.18, 0])
        positions = [0.00, 0.10, 0.40, 0.90, 1.60]
        times = [0.00, 0.50, 1.00, 1.50, 2.00]

        self.play(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=RUN)
        self.play(FadeIn(timeline), FadeIn(live), FadeIn(table_header), run_time=RUN)
        self.add(ghosts[0])
        self.wait(PAUSE_SHORT)

        for i in range(1, 5):
            nt = self.txt(f"t = {times[i]:0.2f} s", 28, BOLD).move_to(live_t)
            ns = self.txt(f"s = {positions[i]:0.2f} m", 26, BOLD, color=DARK_GRAY).move_to(live_s)
            self.play(
                ball.animate.move_to(pts[i]),
                Transform(live_t, nt),
                Transform(live_s, ns),
                cells[i-1].animate.set_fill(LIGHT_GRAY, opacity=0.85),
                run_time=1.55,
                rate_func=rate_functions.ease_in_quad,
            )
            self.play(FadeIn(ghosts[i], scale=1.5), run_time=0.22)
            self.wait(0.45)

        # Explicitly emphasize the four equal 0.50-s intervals.
        equality = self.formula_panel(
            r"\boxed{\Delta t_1=\Delta t_2=\Delta t_3=\Delta t_4=0.50\,\mathrm{s}}",
            width=7.4, height=0.95, size=34,
        ).move_to([-1.50, -1.18, 0])
        self.play(FadeIn(equality), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_data_analysis_v7(self):
        self.header_v7(
            7,
            "TURN THE RAMP MEASUREMENTS INTO A DATA TABLE",
            "The time intervals stay fixed at 0.50 s, but the distance traveled during each interval grows.",
        )

        # Large five-row table made with Manim objects for reliable sizing.
        x_cols = [-4.95, -3.20, -1.35]
        y_rows = [1.45, 0.82, 0.19, -0.44, -1.07, -1.70]
        headings = VGroup(
            self.txt("time t (s)", 25, BOLD).move_to([x_cols[0], y_rows[0], 0]),
            self.txt("t² (s²)", 25, BOLD).move_to([x_cols[1], y_rows[0], 0]),
            self.txt("position s (m)", 25, BOLD).move_to([x_cols[2], y_rows[0], 0]),
        )
        times = [0.00,0.50,1.00,1.50,2.00]
        t2 = [0.00,0.25,1.00,2.25,4.00]
        pos = [0.00,0.10,0.40,0.90,1.60]
        rows = VGroup()
        for i in range(5):
            y = y_rows[i+1]
            rows.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 27).move_to([x_cols[0], y, 0]),
                self.txt(f"{t2[i]:0.2f}", 27).move_to([x_cols[1], y, 0]),
                self.txt(f"{pos[i]:0.2f}", 27, BOLD).move_to([x_cols[2], y, 0]),
            ))
        table_border = RoundedRectangle(width=5.9, height=4.15, corner_radius=0.10,
                                        stroke_color=BLACK, stroke_width=1.8,
                                        fill_color=WHITE, fill_opacity=1).move_to([-3.20,-0.15,0])
        hline = Line([-5.95,1.12,0],[-0.45,1.12,0],color=LIGHT_GRAY,stroke_width=1.4)

        # Interval-distance side, deliberately large and uncluttered.
        right_title = self.txt("DISTANCE DURING EACH 0.50 s INTERVAL", 27, BOLD).move_to([3.65, 1.62, 0])
        interval_values = [0.10,0.30,0.50,0.70]
        bars = VGroup()
        bar_labels = VGroup()
        starts_y = [0.85,0.15,-0.55,-1.25]
        for i,(val,y) in enumerate(zip(interval_values,starts_y), start=1):
            lab = self.txt(f"interval {i}", 23, BOLD).move_to([1.85,y,0])
            bar = Line([2.75,y,0],[2.75+3.0*(val/0.70),y,0],color=BLACK,stroke_width=8)
            valm = self.txt(f"Δs{i} = {val:0.2f} m", 23, BOLD).next_to(bar, RIGHT, buff=0.18)
            bars.add(bar); bar_labels.add(VGroup(lab,valm))
        ratio = self.formula_panel(
            r"0.10:0.30:0.50:0.70=\boxed{1:3:5:7}",
            width=5.8, height=0.95, size=34,
        ).move_to([3.55,-2.05,0])

        self.play(FadeIn(table_border), FadeIn(headings), Create(hline), run_time=RUN)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.08), run_time=0.45)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right_title), run_time=RUN)
        for bar,lab in zip(bars,bar_labels):
            self.play(FadeIn(lab), Create(bar), run_time=0.72)
        self.play(FadeIn(ratio), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_square_time_graph_v7(self):
        self.header_v7(
            8,
            "FROM THE TABLE TO THE SQUARE-TIME LAW",
            "The measured position is proportional to t²: doubling time makes the position four times as large.",
        )

        axes = Axes(
            x_range=[0,2.1,0.5], y_range=[0,1.75,0.4], x_length=7.5, y_length=4.6,
            axis_config={"color":BLACK,"stroke_width":2.1,"include_tip":False},
        ).move_to([-2.55,-0.40,0])
        labs = VGroup(
            self.txt("time t (s)", 22, BOLD).next_to(axes.x_axis, DOWN, buff=0.14),
            self.txt("position s (m)", 22, BOLD).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.18),
        )
        times = [0.00,0.50,1.00,1.50,2.00]
        positions = [0.00,0.10,0.40,0.90,1.60]
        dots = VGroup(*[Dot(axes.c2p(t,s), radius=0.075, color=BLACK) for t,s in zip(times,positions)])
        curve = axes.plot(lambda t:0.40*t*t, x_range=[0,2.0], color=BLACK, stroke_width=4)

        nums = VGroup(
            self.math(r"0.10=0.40(0.50)^2", 28),
            self.math(r"0.40=0.40(1.00)^2", 28),
            self.math(r"0.90=0.40(1.50)^2", 28),
            self.math(r"1.60=0.40(2.00)^2", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([4.20,0.75,0])
        law = self.formula_panel(r"\boxed{s=0.40\,t^2}", width=4.5, height=1.05, size=45).move_to([4.15,-1.15,0])
        proportional = self.formula_panel(r"\boxed{s\propto t^2}", width=4.5, height=1.05, size=45).move_to([4.15,-2.22,0])

        self.play(Create(axes), FadeIn(labs), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(d, scale=1.7) for d in dots], lag_ratio=0.12), run_time=RUN_SLOW)
        self.play(Create(curve), run_time=RUN_SLOW)
        for eq in nums:
            self.play(FadeIn(eq), run_time=0.55)
        self.play(FadeIn(law), run_time=RUN)
        self.play(TransformFromCopy(law, proportional), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_motion_bridge_v7(self):
        self.header_v7(
            9,
            "THE SAME SQUARE-TIME PATTERN APPEARS IN IDEAL FREE FALL",
            "Use the same 0.50 s clock spacing. Near Earth, a released object follows y = 1/2 g t² with g ≈ 9.81 m/s².",
        )

        x = -3.55
        top_y, bottom_y = 1.65, -1.92
        times = np.array([0.00,0.50,1.00,1.50,2.00])
        dist = 0.5*9.81*times**2
        frac = dist/dist[-1]
        ys = top_y - frac*(top_y-bottom_y)
        fall_line = Line([x,top_y+0.20,0],[x,bottom_y-0.15,0],color=BLACK,stroke_width=3)
        ball = Circle(radius=0.16, stroke_color=BLACK, stroke_width=2,
                      fill_color=WHITE, fill_opacity=1).move_to([x,ys[0],0])
        ghosts = VGroup(*[Dot([x,y,0],radius=0.05,color=MID_GRAY) for y in ys])

        row_x = [0.20,2.00,4.15]
        head = VGroup(
            self.txt("t (s)", 25, BOLD).move_to([row_x[0],1.35,0]),
            self.txt("distance y (m)", 25, BOLD).move_to([row_x[1],1.35,0]),
            self.txt("interval distance (m)", 25, BOLD).move_to([row_x[2],1.35,0]),
        )
        body = VGroup()
        interval = [None] + list(np.diff(dist))
        for i in range(5):
            y = 0.72 - i*0.62
            body.add(VGroup(
                self.txt(f"{times[i]:0.2f}", 25).move_to([row_x[0],y,0]),
                self.txt(f"{dist[i]:0.2f}", 25, BOLD).move_to([row_x[1],y,0]),
                self.txt("—" if i==0 else f"{interval[i]:0.2f}", 25).move_to([row_x[2],y,0]),
            ))
        eq_start = self.formula_panel(r"s=0.40t^2\quad\text{(ramp reconstruction)}", width=5.8, height=0.90, size=30)
        eq_start.move_to([2.55,-2.05,0])
        eq_fall = self.formula_panel(r"\boxed{y=\frac12gt^2}", width=5.8, height=1.05, size=45).move_to([2.55,-2.05,0])

        self.play(Create(fall_line), FadeIn(ball), FadeIn(head), run_time=RUN)
        self.add(ghosts[0])
        for i,r in enumerate(body):
            self.play(FadeIn(r), run_time=0.42)
            if i>0:
                self.play(ball.animate.move_to([x,ys[i],0]), FadeIn(ghosts[i]), run_time=0.78, rate_func=rate_functions.ease_in_quad)
        self.play(FadeIn(eq_start), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(eq_start, eq_fall), run_time=RUN_SLOW)
        note = self.txt("same structure: position ∝ time²", 27, BOLD).next_to(eq_fall, UP, buff=0.22)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Pisa / mass independence — large-layout rebuild
    # ------------------------------------------------------------------
    def pisa_question_v7(self):
        self.header_v7(
            10,
            "GALILEO'S MASS QUESTION: DOES A HEAVIER OBJECT FALL FASTER?",
            "Traditional Pisa account: release two compact objects from the same height at the same instant and compare their motion.",
        )
        tower = self._pisa_tower(center=LEFT*4.55+DOWN*0.25, scale=1.08)
        ground = Line([-6.5,-2.45,0],[6.4,-2.45,0],color=BLACK,stroke_width=2.5)

        p1=np.array([-1.55,1.10,0]); p2=np.array([-0.20,1.10,0])
        b1=Circle(radius=0.20,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(p1)
        b2=Circle(radius=0.32,stroke_color=BLACK,stroke_width=2.2,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(p2)
        l1=self.math(r"m_1=1\,\mathrm{kg}",30).next_to(b1,UP,buff=0.18)
        l2=self.math(r"m_2=10\,\mathrm{kg}",30).next_to(b2,UP,buff=0.18)
        arrows=VGroup(
            Arrow(b1.get_bottom(),b1.get_bottom()+DOWN*0.90,buff=0.06,color=BLACK,stroke_width=2),
            Arrow(b2.get_bottom(),b2.get_bottom()+DOWN*0.90,buff=0.06,color=BLACK,stroke_width=2),
        )
        glab=VGroup(
            self.math(r"\vec g",28).next_to(arrows[0],RIGHT,buff=0.12),
            self.math(r"\vec g",28).next_to(arrows[1],RIGHT,buff=0.12),
        )
        historical = self.note_panel(
            "HISTORICAL NOTE",
            [
                "The tower story is traditionally associated with Galileo.",
                "The physics question is the key point: same height and same release time.",
            ], width=5.6, title_size=25, body_size=22,
        ).move_to([3.75,1.35,0])
        prediction=self.formula_panel(r"\boxed{a_{1\,kg}\;?\;a_{10\,kg}}",width=5.0,height=1.10,size=43).move_to([3.75,-0.75,0])
        ideal=self.txt("IDEAL FREE FALL: ignore air resistance",25,BOLD,color=DARK_GRAY).move_to([3.75,-1.72,0])

        self.play(FadeIn(tower),Create(ground),run_time=RUN)
        self.play(FadeIn(b1),FadeIn(b2),FadeIn(l1),FadeIn(l2),run_time=RUN)
        self.play(GrowArrow(arrows[0]),GrowArrow(arrows[1]),FadeIn(glab),run_time=RUN)
        self.play(FadeIn(historical),run_time=RUN)
        self.play(FadeIn(prediction),FadeIn(ideal),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def pisa_force_reasoning_v7(self):
        self.header_v7(
            11,
            "HEAVIER MASS MEANS MORE FORCE — BUT NOT MORE FREE-FALL ACCELERATION",
            "Gravity force grows with mass. Inertia also grows with mass, so the mass divides out of Newton's second law.",
        )

        f1=self.formula_panel(r"m_1=1\,\mathrm{kg}\quad\Rightarrow\quad F_{g1}=m_1g=9.81\,\mathrm{N}",width=6.0,height=1.08,size=33)
        f2=self.formula_panel(r"m_2=10\,\mathrm{kg}\quad\Rightarrow\quad F_{g2}=m_2g=98.1\,\mathrm{N}",width=6.0,height=1.08,size=33)
        force_pair=VGroup(f1,f2).arrange(RIGHT,buff=0.35).move_to(UP*1.35)
        comparison=self.txt("10× the mass -> 10× the gravitational force",28,BOLD).move_to([0,0.35,0])

        eq1=self.math(r"F_{\mathrm{net}}=ma",46)
        eq2=self.math(r"F_g=mg",46)
        eq3=self.math(r"ma=mg",50)
        eq4=self.math(r"a=g",56)
        deriv=VGroup(eq1,self.txt("and",25,BOLD),eq2).arrange(RIGHT,buff=0.35).move_to([0,-0.55,0])
        result=self.formula_panel(r"\boxed{a_{1\,\mathrm{kg}}=a_{10\,\mathrm{kg}}=g\approx9.81\,\mathrm{m/s^2}}",width=9.8,height=1.12,size=39).move_to([0,-2.05,0])

        self.play(FadeIn(force_pair),run_time=RUN)
        self.play(FadeIn(comparison),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(deriv),run_time=RUN)
        ma = eq3.copy().move_to([0,-0.55,0])
        self.play(ReplacementTransform(deriv,ma),run_time=RUN_SLOW)
        note=self.txt("divide both sides by the same nonzero mass m",26,BOLD,color=DARK_GRAY).move_to([0,-1.20,0])
        self.play(FadeIn(note),run_time=RUN)
        ag=eq4.move_to([0,-0.55,0])
        self.play(TransformMatchingTex(ma,ag),run_time=RUN_SLOW)
        self.play(FadeIn(result),run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def pisa_numeric_drop_v7(self):
        self.header_v7(
            12,
            "NUMERICAL PISA CHECK: SAME HEIGHT -> SAME IDEAL FALL TIME",
            "Drop both compact objects from rest at h = 20 m. The mass never appears in the fall-time equation.",
        )
        h=20.0; g=9.81; t_hit=math.sqrt(2*h/g); vf=g*t_hit

        # Large drop area on the left.
        x1,x2=-4.65,-2.75; top_y=1.55; bottom_y=-1.70
        p1=Line([x1,top_y,0],[x1,bottom_y,0],color=LIGHT_GRAY,stroke_width=2)
        p2=Line([x2,top_y,0],[x2,bottom_y,0],color=LIGHT_GRAY,stroke_width=2)
        ground=Line([-5.65,bottom_y,0],[-1.70,bottom_y,0],color=BLACK,stroke_width=2.4)
        b1=Circle(radius=0.17,color=BLACK,fill_color=WHITE,fill_opacity=1).move_to(p1.get_start())
        b2=Circle(radius=0.28,color=BLACK,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(p2.get_start())
        labels=VGroup(
            self.math(r"1\,\mathrm{kg}",27).next_to(b1,UP,buff=0.14),
            self.math(r"10\,\mathrm{kg}",27).next_to(b2,UP,buff=0.14),
        )
        height=DoubleArrow([-5.45,top_y,0],[-5.45,bottom_y,0],buff=0.03,color=MID_GRAY,stroke_width=1.5,max_tip_length_to_length_ratio=0.05)
        hlab=self.math(r"h=20\,\mathrm{m}",26).next_to(height,LEFT,buff=0.10)

        # Larger, staged calculation on the right.
        calc_title=self.txt("SOLVE THE FALL TIME",29,BOLD).move_to([3.65,1.55,0])
        e1=self.math(r"h=\frac12gt^2",44).move_to([3.65,0.82,0])
        e2=self.math(r"20=\frac12(9.81)t^2",42).move_to([3.65,0.05,0])
        e3=self.math(r"t=\sqrt{\frac{2(20)}{9.81}}",42).move_to([3.65,-0.72,0])
        e4=self.formula_panel(r"\boxed{t\approx2.02\,\mathrm{s}}",width=4.3,height=1.0,size=43).move_to([3.65,-1.65,0])

        clock_label=self.txt("t =",27,BOLD)
        clock_num=DecimalNumber(0.0,num_decimal_places=2,font_size=36,color=BLACK)
        clock_unit=self.txt("s",27,BOLD)
        clock=VGroup(clock_label,clock_num,clock_unit).arrange(RIGHT,buff=0.12).move_to([-3.70,2.04,0])

        self.play(Create(p1),Create(p2),Create(ground),FadeIn(b1),FadeIn(b2),FadeIn(labels),FadeIn(height),FadeIn(hlab),run_time=RUN)
        self.play(FadeIn(calc_title),Write(e1),run_time=RUN)
        self.play(TransformFromCopy(e1,e2),run_time=RUN)
        self.play(TransformFromCopy(e2,e3),run_time=RUN)
        self.play(FadeIn(e4),FadeIn(clock),run_time=RUN)
        self.wait(PAUSE_READ)

        tracker=ValueTracker(0.0)
        def y(alpha): return top_y+(bottom_y-top_y)*(alpha**2)
        b1.add_updater(lambda m:m.move_to([x1,y(tracker.get_value()),0]))
        b2.add_updater(lambda m:m.move_to([x2,y(tracker.get_value()),0]))
        clock_num.add_updater(lambda m:m.set_value(t_hit*tracker.get_value()))
        self.play(tracker.animate.set_value(1.0),run_time=3.15,rate_func=linear)
        b1.clear_updaters(); b2.clear_updaters(); clock_num.clear_updaters()

        impact=self.formula_panel(r"\boxed{t_1=t_2=2.02\,\mathrm{s}}",width=4.6,height=0.90,size=36).move_to([-3.70,-2.27,0])
        speed=self.math(rf"v_f=gt\approx{vf:.1f}\,\mathrm{{m/s}}",30).move_to([3.65,-2.42,0])
        self.play(FadeIn(impact),FadeIn(speed),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def _feather_v7(self,center):
        shaft=Line(center+DOWN*0.65,center+UP*0.65,color=BLACK,stroke_width=2)
        vanes=VGroup()
        for yy,ll in [(-0.34,0.34),(-0.10,0.46),(0.16,0.42),(0.40,0.30)]:
            p=center+UP*yy
            vanes.add(Line(p,p+LEFT*ll+UP*0.15,color=BLACK,stroke_width=1.6))
            vanes.add(Line(p,p+RIGHT*ll+UP*0.15,color=BLACK,stroke_width=1.6))
        return VGroup(shaft,vanes)

    def air_resistance_v7(self):
        self.header_v7(
            13,
            "WHY A FEATHER AND A BALL CAN ARRIVE AT DIFFERENT TIMES IN AIR",
            "The value of g is the same; air resistance adds another force whose effect depends strongly on shape and speed.",
        )

        divider=Line([0,1.75,0],[0,-2.20,0],color=LIGHT_GRAY,stroke_width=1.5)
        left_title=self.txt("VACUUM / IDEAL FREE FALL",28,BOLD).move_to([-3.55,1.60,0])
        right_title=self.txt("AIR PRESENT",28,BOLD).move_to([3.55,1.60,0])

        ball_l=Circle(radius=0.25,color=BLACK,fill_color=LIGHT_GRAY,fill_opacity=1).move_to([-4.20,0.80,0])
        feather_l=self._feather_v7(np.array([-2.80,0.80,0]))
        target_y=-1.20
        vacuum_eq=self.formula_panel(r"a_{ball}=a_{feather}=g",width=4.8,height=0.92,size=36).move_to([-3.55,-1.78,0])

        ball_r=Circle(radius=0.25,color=BLACK,fill_color=LIGHT_GRAY,fill_opacity=1).move_to([2.85,0.80,0])
        feather_r=self._feather_v7(np.array([4.30,0.80,0]))
        drag_arrow=Arrow([4.30,0.30,0],[4.30,1.20,0],buff=0.04,color=MID_GRAY,stroke_width=2)
        drag_lab=self.math(r"F_{air}",28).next_to(drag_arrow,RIGHT,buff=0.10)
        air_eq=self.formula_panel(r"\vec F_{net}=m\vec g+\vec F_{air}",width=5.1,height=0.92,size=34).move_to([3.55,-1.78,0])

        self.play(Create(divider),FadeIn(left_title),FadeIn(right_title),run_time=RUN)
        self.play(FadeIn(ball_l),FadeIn(feather_l),FadeIn(ball_r),FadeIn(feather_r),run_time=RUN)
        self.play(FadeIn(vacuum_eq),FadeIn(air_eq),GrowArrow(drag_arrow),FadeIn(drag_lab),run_time=RUN)
        self.wait(PAUSE_READ)

        # Vacuum pair moves together; air pair visibly separates.
        self.play(
            ball_l.animate.move_to([-4.20,target_y,0]),
            feather_l.animate.move_to([-2.80,target_y,0]),
            ball_r.animate.move_to([2.85,target_y,0]),
            feather_r.animate.move_to([4.30,-0.25,0]),
            run_time=2.50,
            rate_func=rate_functions.ease_in_quad,
        )
        conclusion=self.txt("Different arrival times in air do NOT mean different values of g.",28,BOLD)
        conclusion.to_edge(DOWN,buff=0.30)
        self.play(FadeIn(conclusion),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def summary_v7(self):
        self.header_v7(
            14,
            "ONE CONNECTED STORY: OBSERVE -> MEASURE -> MODEL -> EXPLAIN",
            "Galileo's method turns a difficult motion into measurable data, then mathematics reveals the general pattern.",
        )
        stages=[
            ("1  OBSERVE","Falling motion changes; equal times do not give equal distances."),
            ("2  MEASURE","Use a shallow ramp and equal time intervals. In our reconstruction: Δt = 0.50 s."),
            ("3  MODEL","The ramp data follow s = 0.40t², so position is proportional to time²."),
            ("4  EXPLAIN","Ideal free fall follows y = 1/2 gt² and the acceleration is a = g, independent of test mass."),
        ]
        cards=VGroup()
        for title,body in stages:
            card=self.note_panel(title,[body],width=11.5,title_size=29,body_size=25)
            self.fit(card,11.5,1.05)
            cards.add(card)
        cards.arrange(DOWN,buff=0.20).move_to([0,-0.10,0])
        self.fit(cards,12.1,4.85)

        for i,card in enumerate(cards):
            if i==0:
                self.play(FadeIn(card,shift=RIGHT*0.15),run_time=RUN)
            else:
                self.play(TransformFromCopy(cards[i-1],card),run_time=RUN)
            self.wait(0.70)

        final=self.formula_panel(
            r"\boxed{s\propto t^2\qquad y=\frac12gt^2\qquad a=g\;\text{(ideal free fall)}}",
            width=10.5,height=1.15,size=39,
        ).to_edge(DOWN,buff=0.25)
        self.play(FadeIn(final),run_time=RUN)
        self.wait(PAUSE_WORK)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=RUN)

        end1=self.txt("PHYSICS 9 | GALILEO",30,BOLD)
        end2=self.txt("MEASURE THE MOTION. THEN LET THE DATA REVEAL THE LAW.",42,BOLD)
        self.fit(end2,13.0,0.85)
        end3=self.math(r"\Delta t=0.50\,\mathrm{s}\;\Rightarrow\;\Delta s=0.10,0.30,0.50,0.70\,\mathrm{m}",34)
        end=VGroup(end1,end2,end3).arrange(DOWN,buff=0.42).move_to(ORIGIN)
        self.play(FadeIn(end,shift=UP*0.12),run_time=RUN_SLOW)
        self.wait(4.20)
        self.play(FadeOut(end),run_time=RUN)


# Preview:
# manim -pql Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL.py Physics9GalileoV7VisualRedesignSeniorFinal --disable_caching
# Final:
# manim -pqh Physics9_Galileo_V7_VISUAL_REDESIGN_SENIOR_FINAL.py Physics9GalileoV7VisualRedesignSeniorFinal --disable_caching
