#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Inclined Plane Laboratory · Stopwatch + Sensors.

Dedicated classroom/laboratory video package in the consolidated JP classroom
style: white background, black geometry/text, restrained gray hierarchy,
large readable type, 16:9 framing, explicit section headers, and frame-safe
independent layout zones.

Pedagogical scope
-----------------
The experiment is a Galileo-inspired classroom reconstruction. Students measure
position along a shallow inclined plane as a function of elapsed time, then test
whether x vs t or x vs t^2 is closer to a straight-line relationship.

Two executable laboratory variants are included:
1. Stopwatch method: no electronic sensors required; repeat each timing 3 times.
2. Sensor method: photogates are the primary implementation; a motion detector
   is shown as an alternative when available and appropriate for the moving body.

The lesson intentionally postpones a formal acceleration derivation. The main
experimental conclusion is the square-time pattern x ∝ t².

Render targets
--------------
Master combined video:
  manim -pqh Physics9_Inclined_Plane_Lab_Stopwatch_Sensors_FINAL.py \
    Physics9InclinedPlaneLabMaster --disable_caching

Stopwatch-only video:
  manim -pqh Physics9_Inclined_Plane_Lab_Stopwatch_Sensors_FINAL.py \
    Physics9InclinedPlaneLabStopwatch --disable_caching

Sensors-only video:
  manim -pqh Physics9_Inclined_Plane_Lab_Stopwatch_Sensors_FINAL.py \
    Physics9InclinedPlaneLabSensors --disable_caching
"""
from __future__ import annotations

import os
import math
import numpy as np
from manim import *

# -----------------------------------------------------------------------------
# Global classroom style
# -----------------------------------------------------------------------------
config.background_color = WHITE

BLACK_2 = "#161616"
DARK_GRAY = "#444444"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT = "#F4F4F4"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))


def scaled_time(seconds: float) -> float:
    """Keep preview animations fast without dropping below one visible frame."""
    return max(0.05, seconds * TIME_SCALE)


class Physics9InclinedPlaneLabBase(Scene):
    """Reusable visual language and experiment scenes for all three renders."""

    def setup(self):
        self.header_group = None

    # ------------------------------------------------------------------
    # Utility / layout primitives
    # ------------------------------------------------------------------
    def txt(self, text, size=26, weight=NORMAL, color=BLACK_2):
        return Text(text, font="DejaVu Sans", font_size=size, weight=weight, color=color)

    def math(self, tex, size=40, color=BLACK_2):
        return MathTex(tex, font_size=size, color=color)

    def fit(self, mob: Mobject, max_width: float, max_height: float | None = None):
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if max_height is not None and mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def panel(self, width, height, fill=WHITE, stroke=LIGHT_GRAY, radius=0.14):
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=radius,
            stroke_color=stroke,
            stroke_width=1.6,
            fill_color=fill,
            fill_opacity=1,
        )

    def formula_panel(self, tex, width, height=0.92, size=34):
        box = self.panel(width, height, fill=VERY_LIGHT, stroke=LIGHT_GRAY, radius=0.12)
        formula = self.math(tex, size=size)
        self.fit(formula, width - 0.42, height - 0.24)
        formula.move_to(box)
        return VGroup(box, formula)

    def note_panel(self, title, lines, width=5.4, height=2.4, title_size=23, body_size=20):
        box = self.panel(width, height, fill=WHITE)
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size, BOLD if i == 0 else NORMAL, DARK_GRAY)
                        for i, line in enumerate(lines)])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.fit(title_m, width - 0.52, 0.42)
        self.fit(body, width - 0.60, height - 0.90)
        title_m.next_to(box.get_top(), DOWN, buff=0.22)
        body.next_to(title_m, DOWN, buff=0.18).align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, title_m, body)

    def play_t(self, *animations, run_time=0.75, **kwargs):
        self.play(*animations, run_time=scaled_time(run_time), **kwargs)

    def wait_t(self, duration=1.0):
        self.wait(scaled_time(duration))

    def set_header(self, number, title, subtitle):
        if self.header_group is not None:
            self.remove(self.header_group)
            self.header_group = None

        badge = RoundedRectangle(
            width=0.72, height=0.52, corner_radius=0.10,
            stroke_color=BLACK_2, stroke_width=2, fill_color=WHITE, fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 22, BOLD).move_to(badge)
        title_m = self.txt(title, 29, BOLD)
        self.fit(title_m, 12.75, 0.52)
        row = VGroup(VGroup(badge, num), title_m).arrange(RIGHT, buff=0.20)
        self.fit(row, 14.0, 0.58)
        row.to_edge(UP, buff=0.13).align_to(LEFT * 7.0, LEFT)

        subtitle_m = self.txt(subtitle, 19, NORMAL, DARK_GRAY)
        self.fit(subtitle_m, 13.75, 0.48)
        subtitle_m.next_to(row, DOWN, buff=0.07).align_to(row, LEFT)

        rule = Line(LEFT * 7.0, RIGHT * 7.0, color=LIGHT_GRAY, stroke_width=1.5)
        rule.next_to(subtitle_m, DOWN, buff=0.08)
        self.header_group = VGroup(row, subtitle_m, rule)
        self.add(self.header_group)

    def clear_stage(self):
        targets = list(self.mobjects)
        if targets:
            self.play_t(*[FadeOut(m) for m in targets], run_time=0.48)
        self.header_group = None
        self.wait_t(0.10)

    # ------------------------------------------------------------------
    # Drawing primitives for laboratory apparatus
    # ------------------------------------------------------------------
    def ramp_geometry(self, start=(-5.8, -1.35, 0), end=(1.25, 1.15, 0)):
        start = np.array(start, dtype=float)
        end = np.array(end, dtype=float)
        ramp = Line(start, end, color=BLACK_2, stroke_width=5)
        floor = Line([start[0] - 0.30, start[1], 0], [end[0] + 0.45, start[1], 0], color=BLACK_2, stroke_width=2)
        support = Line(end, [end[0], start[1], 0], color=MID_GRAY, stroke_width=2)
        direction_down = (start - end) / np.linalg.norm(start - end)
        normal = np.array([-direction_down[1], direction_down[0], 0.0])
        ball = Circle(radius=0.17, stroke_color=BLACK_2, stroke_width=2,
                      fill_color=WHITE, fill_opacity=1).move_to(end + normal * 0.18)
        return start, end, ramp, floor, support, ball, direction_down, normal

    def stopwatch_icon(self, scale=1.0):
        body = Circle(radius=0.45 * scale, stroke_color=BLACK_2, stroke_width=2.2,
                      fill_color=WHITE, fill_opacity=1)
        crown = RoundedRectangle(width=0.22 * scale, height=0.13 * scale,
                                 corner_radius=0.03 * scale, stroke_color=BLACK_2,
                                 stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
        crown.next_to(body, UP, buff=0.02 * scale)
        hand = Line(body.get_center(), body.get_center() + UP * 0.26 * scale,
                    color=BLACK_2, stroke_width=2)
        tick1 = Line(body.get_center() + UP * 0.34 * scale,
                     body.get_center() + UP * 0.41 * scale, color=MID_GRAY, stroke_width=1.5)
        tick2 = tick1.copy().rotate(PI / 2, about_point=body.get_center())
        tick3 = tick1.copy().rotate(PI, about_point=body.get_center())
        tick4 = tick1.copy().rotate(3 * PI / 2, about_point=body.get_center())
        return VGroup(body, crown, hand, tick1, tick2, tick3, tick4)

    def photogate(self, point, normal, size=0.34):
        p = np.array(point)
        n = normal / np.linalg.norm(normal)
        d = np.array([n[1], -n[0], 0.0])
        left = p - n * size
        right = p + n * size
        beam = DashedLine(left, right, dash_length=0.06, color=MID_GRAY, stroke_width=1.4)
        post1 = Line(left - d * 0.15, left + d * 0.15, color=BLACK_2, stroke_width=2.3)
        post2 = Line(right - d * 0.15, right + d * 0.15, color=BLACK_2, stroke_width=2.3)
        return VGroup(post1, post2, beam)

    def sensor_box(self):
        box = RoundedRectangle(width=1.25, height=0.72, corner_radius=0.10,
                               stroke_color=BLACK_2, stroke_width=2,
                               fill_color=WHITE, fill_opacity=1)
        face = VGroup(*[
            Arc(radius=0.18 + 0.10 * i, start_angle=-PI / 4, angle=PI / 2,
                color=MID_GRAY, stroke_width=1.5)
            for i in range(3)
        ])
        face.rotate(PI).move_to(box.get_center() + RIGHT * 0.15)
        label = self.txt("MOTION", 14, BOLD).move_to(box.get_center() + LEFT * 0.25)
        return VGroup(box, face, label)

    def compact_table(self, headers, rows, width=6.0, row_height=0.47, font_size=19):
        cols = len(headers)
        nrows = len(rows) + 1
        col_w = width / cols
        height = row_height * nrows
        outer = RoundedRectangle(width=width, height=height, corner_radius=0.07,
                                 stroke_color=LIGHT_GRAY, stroke_width=1.4,
                                 fill_color=WHITE, fill_opacity=1)
        grid = VGroup()
        for c in range(1, cols):
            x = outer.get_left()[0] + c * col_w
            grid.add(Line([x, outer.get_bottom()[1], 0], [x, outer.get_top()[1], 0],
                          color=LIGHT_GRAY, stroke_width=1.0))
        for r in range(1, nrows):
            y = outer.get_top()[1] - r * row_height
            grid.add(Line([outer.get_left()[0], y, 0], [outer.get_right()[0], y, 0],
                          color=LIGHT_GRAY, stroke_width=1.0))
        texts = VGroup()
        all_rows = [headers] + rows
        for r, row in enumerate(all_rows):
            for c, value in enumerate(row):
                tm = self.txt(str(value), font_size, BOLD if r == 0 else NORMAL,
                              BLACK_2 if r == 0 else DARK_GRAY)
                self.fit(tm, col_w - 0.16, row_height - 0.12)
                x = outer.get_left()[0] + (c + 0.5) * col_w
                y = outer.get_top()[1] - (r + 0.5) * row_height
                tm.move_to([x, y, 0])
                texts.add(tm)
        return VGroup(outer, grid, texts)

    # ------------------------------------------------------------------
    # Shared opening and experimental design
    # ------------------------------------------------------------------
    def opening(self, mode="BOTH"):
        kicker = self.txt("PHYSICS 9 | EXPERIMENTAL KINEMATICS", 28, BOLD)
        title = self.txt("GALILEO-INSPIRED INCLINED-PLANE LAB", 44, BOLD)
        subtitle = self.txt("Measure position vs time on a real classroom ramp", 27, NORMAL, DARK_GRAY)
        if mode == "STOPWATCH":
            mode_text = "VERSION A  |  STOPWATCH — NO SENSORS REQUIRED"
        elif mode == "SENSORS":
            mode_text = "VERSION B  |  PHOTOGATES / MOTION SENSOR"
        else:
            mode_text = "TWO VERSIONS  |  STOPWATCH + SENSORS"
        mode_badge = self.formula_panel(r"\text{" + mode_text.replace("_", r"\_") + r"}", width=9.7, height=0.92, size=29)
        question = self.formula_panel(r"\boxed{\text{How does position }x\text{ along the ramp change with time }t\text{?}}",
                                     width=11.1, height=1.05, size=31)
        group = VGroup(kicker, title, subtitle, mode_badge, question).arrange(DOWN, buff=0.36)
        self.fit(group, 13.6, 6.8)
        group.move_to(ORIGIN)
        self.play_t(FadeIn(kicker), run_time=0.65)
        self.play_t(Write(title), run_time=0.95)
        self.play_t(FadeIn(subtitle), run_time=0.60)
        self.play_t(FadeIn(mode_badge), run_time=0.65)
        self.play_t(FadeIn(question), run_time=0.70)
        self.wait_t(2.0)
        self.play_t(FadeOut(group), run_time=0.60)

    def experimental_goal(self, number=1):
        self.set_header(number, "THE EXPERIMENTAL QUESTION",
                        "Use measured data — not an assumed formula — to decide which position-time pattern the ramp produces.")
        left = self.panel(6.3, 4.75).move_to(LEFT * 3.55 + DOWN * 0.18)
        right = self.panel(6.3, 4.75).move_to(RIGHT * 3.55 + DOWN * 0.18)
        lt = self.txt("WHAT WE MEASURE", 25, BOLD).next_to(left.get_top(), DOWN, buff=0.25)
        rt = self.txt("WHAT WE TEST", 25, BOLD).next_to(right.get_top(), DOWN, buff=0.25)

        measured = VGroup(
            self.txt("x  = distance along the ramp", 23, BOLD),
            self.txt("t  = elapsed time from release", 23),
            self.txt("same release point every trial", 23),
            self.txt("same ramp angle during one dataset", 23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(left.get_center() + DOWN * 0.10)
        self.fit(measured, 5.55, 3.30)

        f1 = self.formula_panel(r"x\propto t", width=4.65, height=1.0, size=44)
        f2 = self.formula_panel(r"x\propto t^2", width=4.65, height=1.0, size=44)
        labels = VGroup(
            self.txt("straight x-t pattern?", 21, BOLD, DARK_GRAY),
            self.txt("square-time pattern?", 21, BOLD, DARK_GRAY),
        )
        test = VGroup(VGroup(f1, labels[0]).arrange(DOWN, buff=0.15),
                      VGroup(f2, labels[1]).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.38)
        test.move_to(right.get_center() + DOWN * 0.08)

        foot = self.formula_panel(r"\text{Plot }x\text{ vs }t\quad\text{and}\quad x\text{ vs }t^2",
                                  width=9.2, height=0.90, size=31).to_edge(DOWN, buff=0.26)
        self.play_t(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=0.75)
        self.play_t(FadeIn(measured), run_time=0.70)
        self.play_t(FadeIn(test), run_time=0.75)
        self.play_t(FadeIn(foot), run_time=0.65)
        self.wait_t(2.0)
        self.clear_stage()

    def physical_setup(self, number=2):
        self.set_header(number, "BUILD THE RAMP BEFORE TIMING ANYTHING",
                        "Secure the inclined plane, measure distance along its surface, and define one repeatable release point.")
        left = self.panel(8.65, 5.15).move_to(LEFT * 2.70 + DOWN * 0.10)
        right = self.panel(4.55, 5.15).move_to(RIGHT * 5.02 + DOWN * 0.10)
        start, end, ramp, floor, support, ball, ddown, normal = self.ramp_geometry(
            start=(-6.25, -1.10, 0), end=(1.05, 1.15, 0)
        )
        release_mark = Line(end - normal * 0.18, end + normal * 0.30, color=BLACK_2, stroke_width=3)
        rlab = self.txt("release line  x = 0", 20, BOLD).move_to([-0.75, 1.75, 0])
        rlead = Arrow(rlab.get_bottom() + RIGHT * 0.42, end + normal * 0.14,
                      buff=0.08, color=MID_GRAY, stroke_width=1.5,
                      max_tip_length_to_length_ratio=0.12)

        # Four equal-distance target marks along the ramp.
        fracs = [0.25, 0.50, 0.75, 1.00]
        targets = [end + f * (start - end) for f in fracs]
        marks = VGroup()
        labels = VGroup()
        for i, (f, p) in enumerate(zip(fracs, targets), start=1):
            marks.add(Line(p - normal * 0.16, p + normal * 0.16,
                           color=BLACK_2, stroke_width=2.2))
            label_pos = p + normal * (0.42 if i % 2 else -0.42)
            labels.add(self.txt(f"{f:.2f} m", 17, BOLD, DARK_GRAY).move_to(label_pos))

        along = Arrow(end + normal * 0.62, start + normal * 0.62, buff=0.05,
                      color=MID_GRAY, stroke_width=1.7,
                      max_tip_length_to_length_ratio=0.05)
        along_lab = self.txt("measure x ALONG the ramp", 19, BOLD, DARK_GRAY).next_to(along, UP, buff=0.09)

        checklist = self.note_panel("SETUP CHECK", [
            "1  Clamp / secure the ramp",
            "2  Start with a shallow angle",
            "3  Mark 0.25, 0.50, 0.75, 1.00 m",
            "4  Use one release line — never push",
            "5  Keep the landing area clear",
        ], width=4.05, height=4.15, title_size=23, body_size=18).move_to(right)

        safety = self.formula_panel(r"\text{Safety: secure ramp + clear catch zone + controlled release}",
                                    width=10.3, height=0.85, size=27).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), run_time=0.65)
        self.play_t(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=0.75)
        self.play_t(Create(release_mark), FadeIn(rlab), GrowArrow(rlead), run_time=0.65)
        self.play_t(FadeIn(marks), FadeIn(labels), GrowArrow(along), FadeIn(along_lab), run_time=0.75)
        self.play_t(FadeIn(checklist), FadeIn(safety), run_time=0.75)
        self.wait_t(2.2)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Stopwatch version
    # ------------------------------------------------------------------
    def stopwatch_protocol(self, number=3):
        self.set_header(number, "VERSION A — STOPWATCH METHOD",
                        "Use this version when no electronic timing sensors are available. Repetition is what makes the data useful.")
        left = self.panel(8.7, 5.15).move_to(LEFT * 2.65 + DOWN * 0.10)
        right = self.panel(4.55, 5.15).move_to(RIGHT * 5.0 + DOWN * 0.10)
        start, end, ramp, floor, support, ball, ddown, normal = self.ramp_geometry(
            start=(-6.25, -1.05, 0), end=(1.10, 1.20, 0)
        )
        fracs = [0.25, 0.50, 0.75, 1.00]
        points = [end + f * (start - end) for f in fracs]
        target_marks = VGroup(*[
            Line(p - normal * 0.16, p + normal * 0.16, color=BLACK_2, stroke_width=2.2)
            for p in points
        ])
        tlabels = VGroup(*[
            self.txt(f"x={f:.2f} m", 17, BOLD, DARK_GRAY).move_to(p + normal * (0.42 if i % 2 == 0 else -0.42))
            for i, (f, p) in enumerate(zip(fracs, points))
        ])
        start_tag = self.txt("START TIMER", 19, BOLD).move_to([0.0, 1.72, 0])
        start_arrow = Arrow(start_tag.get_bottom(), end + normal * 0.20, buff=0.10,
                            color=MID_GRAY, stroke_width=1.5,
                            max_tip_length_to_length_ratio=0.12)
        stop = self.stopwatch_icon(0.95).move_to([-4.95, 1.50, 0])
        stop_label = self.txt("one timer", 18, BOLD, DARK_GRAY).next_to(stop, DOWN, buff=0.10)

        roles = self.note_panel("3-STUDENT TEAM", [
            "A  releases — no push",
            "B  starts / stops the watch",
            "C  records the time",
            "rotate roles after each target",
        ], width=4.00, height=2.45, title_size=23, body_size=18).move_to(right.get_center() + UP * 1.05)
        steps = self.note_panel("FOR EACH TARGET", [
            "1  reset ball at x = 0",
            "2  time until target crossing",
            "3  repeat 3 trials",
            "4  calculate mean time",
        ], width=4.00, height=2.25, title_size=22, body_size=18).move_to(right.get_center() + DOWN * 1.55)

        rule = self.formula_panel(r"\boxed{\text{Never change the release point during one dataset}}",
                                  width=9.8, height=0.86, size=28).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), run_time=0.60)
        self.play_t(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=0.70)
        self.play_t(FadeIn(target_marks), FadeIn(tlabels), FadeIn(stop), FadeIn(stop_label), run_time=0.70)
        self.play_t(FadeIn(start_tag), GrowArrow(start_arrow), FadeIn(roles), FadeIn(steps), run_time=0.75)
        self.play_t(FadeIn(rule), run_time=0.60)
        self.wait_t(2.2)
        self.clear_stage()

    def stopwatch_trial(self, number=4):
        self.set_header(number, "ONE COMPLETE STOPWATCH TRIAL",
                        "Example: time the ball from the release line to the 0.75 m target, then repeat the same target two more times.")
        left = self.panel(9.5, 5.10).move_to(LEFT * 2.28 + DOWN * 0.12)
        right = self.panel(3.75, 5.10).move_to(RIGHT * 5.20 + DOWN * 0.12)
        start, end, ramp, floor, support, ball, ddown, normal = self.ramp_geometry(
            start=(-6.10, -1.00, 0), end=(1.50, 1.25, 0)
        )
        target = end + 0.75 * (start - end)
        mark = Line(target - normal * 0.22, target + normal * 0.22, color=BLACK_2, stroke_width=4)
        target_lab = self.txt("TARGET  x = 0.75 m", 20, BOLD).move_to(target + normal * 0.55)
        release_lab = self.txt("release at x = 0", 18, BOLD, DARK_GRAY).move_to([0.40, 1.80, 0])
        release_arrow = Arrow(release_lab.get_bottom(), ball.get_center(), buff=0.10,
                              color=MID_GRAY, stroke_width=1.4,
                              max_tip_length_to_length_ratio=0.11)

        icon = self.stopwatch_icon(1.10).move_to(right.get_center() + UP * 1.45)
        timer_label = self.txt("ELAPSED TIME", 21, BOLD).next_to(icon, DOWN, buff=0.20)
        timer_box = self.panel(2.45, 0.92, fill=VERY_LIGHT, stroke=LIGHT_GRAY).next_to(timer_label, DOWN, buff=0.18)
        timer = DecimalNumber(0.00, num_decimal_places=2, font_size=43, color=BLACK_2)
        unit = self.txt("s", 24, BOLD, DARK_GRAY)
        timer_group = VGroup(timer, unit).arrange(RIGHT, buff=0.10).move_to(timer_box)
        tracker = ValueTracker(0.00)
        timer.add_updater(lambda m: m.set_value(tracker.get_value()))

        result = self.note_panel("TRIAL RECORD", [
            "target: 0.75 m",
            "trial 1: 0.79 s",
            "repeat: trials 2 and 3",
        ], width=3.25, height=1.70, title_size=21, body_size=17).move_to(right.get_center() + DOWN * 1.65)
        cue = self.formula_panel(r"\text{release and start the stopwatch at the same instant}",
                                 width=9.3, height=0.84, size=27).to_edge(DOWN, buff=0.27)

        self.play_t(FadeIn(left), FadeIn(right), run_time=0.60)
        self.play_t(Create(ramp), Create(floor), Create(support), FadeIn(ball), Create(mark), FadeIn(target_lab), run_time=0.75)
        self.play_t(FadeIn(release_lab), GrowArrow(release_arrow), FadeIn(icon), FadeIn(timer_label), FadeIn(timer_box), FadeIn(timer_group), run_time=0.70)
        self.play_t(FadeIn(cue), run_time=0.55)
        self.play(
            MoveAlongPath(ball, Line(ball.get_center(), target + normal * 0.18), rate_func=rate_functions.ease_in_quad),
            tracker.animate.set_value(0.79),
            run_time=scaled_time(2.6),
        )
        timer.clear_updaters()
        self.play_t(FadeIn(result), run_time=0.65)
        self.wait_t(2.3)
        self.clear_stage()

    def stopwatch_analysis(self, number=5):
        self.set_header(number, "STOPWATCH DATA — REPEAT, AVERAGE, THEN GRAPH",
                        "The sample values below are illustrative only. Students must replace them with their own measured times.")
        left = self.panel(7.65, 5.05).move_to(LEFT * 3.25 + DOWN * 0.10)
        right = self.panel(5.35, 5.05).move_to(RIGHT * 4.35 + DOWN * 0.10)
        title_l = self.txt("ILLUSTRATIVE DATASET", 23, BOLD).next_to(left.get_top(), DOWN, buff=0.22)

        headers = ["x (m)", "t1", "t2", "t3", "mean", "mean²"]
        rows = [
            ["0.25", "0.48", "0.46", "0.47", "0.47", "0.22"],
            ["0.50", "0.66", "0.64", "0.65", "0.65", "0.42"],
            ["0.75", "0.79", "0.78", "0.80", "0.79", "0.62"],
            ["1.00", "0.92", "0.90", "0.91", "0.91", "0.83"],
        ]
        table = self.compact_table(headers, rows, width=6.75, row_height=0.56, font_size=18)
        table.move_to(left.get_center() + UP * 0.35)
        avg = self.formula_panel(r"\bar t=\frac{t_1+t_2+t_3}{3}", width=4.30, height=0.82, size=31)
        avg.move_to(left.get_center() + DOWN * 1.58)
        note = self.txt("Example only — use your own measurements", 18, BOLD, DARK_GRAY)
        note.move_to(left.get_bottom() + UP * 0.28)

        gt = self.txt("TEST  x  vs  t²", 23, BOLD).next_to(right.get_top(), DOWN, buff=0.22)
        axes = Axes(x_range=[0, 0.9, 0.2], y_range=[0, 1.1, 0.25],
                    x_length=4.15, y_length=3.00,
                    axis_config={"color": BLACK_2, "stroke_width": 2, "include_tip": False})
        axes.move_to(right.get_center() + DOWN * 0.25)
        xvals = [0.22, 0.42, 0.62, 0.83]
        yvals = [0.25, 0.50, 0.75, 1.00]
        pts = VGroup(*[Dot(axes.c2p(a, b), radius=0.065, color=BLACK_2) for a, b in zip(xvals, yvals)])
        line = axes.plot(lambda q: 1.20 * q, x_range=[0, 0.85], color=MID_GRAY, stroke_width=3)
        labels = VGroup(
            self.txt("t² (s²)", 17).next_to(axes.x_axis, DOWN, buff=0.09),
            self.txt("x (m)", 17).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.11),
        )
        concl = self.formula_panel(r"\boxed{x\propto t^2\ \text{approximately}}", width=4.4, height=0.84, size=30)
        concl.move_to(right.get_bottom() + UP * 0.50)

        error = self.formula_panel(r"\text{Main stopwatch limitation: human reaction time}",
                                   width=8.9, height=0.84, size=28).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), FadeIn(title_l), FadeIn(gt), run_time=0.65)
        self.play_t(FadeIn(table), FadeIn(avg), FadeIn(note), run_time=0.80)
        self.play_t(Create(axes), FadeIn(labels), FadeIn(pts), run_time=0.75)
        self.play_t(Create(line), FadeIn(concl), run_time=0.70)
        self.play_t(FadeIn(error), run_time=0.55)
        self.wait_t(2.4)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Sensor version
    # ------------------------------------------------------------------
    def sensor_protocol(self, number=6):
        self.set_header(number, "VERSION B — AUTOMATIC TIMING WITH SENSORS",
                        "Use photogates when available; a motion detector can be an alternative if it reliably tracks the moving object.")
        left = self.panel(9.3, 5.15).move_to(LEFT * 2.35 + DOWN * 0.10)
        right = self.panel(3.95, 5.15).move_to(RIGHT * 5.15 + DOWN * 0.10)
        start, end, ramp, floor, support, ball, ddown, normal = self.ramp_geometry(
            start=(-6.05, -1.05, 0), end=(1.45, 1.20, 0)
        )
        fracs = [0.0, 0.25, 0.50, 0.75, 1.00]
        points = [end + f * (start - end) for f in fracs]
        gates = VGroup(*[self.photogate(p, normal, 0.25) for p in points])
        gate_labels = VGroup(*[
            self.txt(f"G{i}", 16, BOLD, DARK_GRAY).move_to(p + normal * (0.50 if i % 2 == 0 else -0.50))
            for i, p in enumerate(points)
        ])
        logger = self.panel(2.55, 1.25, fill=VERY_LIGHT, stroke=LIGHT_GRAY).move_to(right.get_center() + UP * 1.45)
        logger_t = self.txt("DATA LOGGER", 20, BOLD).move_to(logger.get_center() + UP * 0.27)
        logger_s = self.txt("timestamps each crossing", 16, NORMAL, DARK_GRAY).move_to(logger.get_center() + DOWN * 0.25)
        cable = Arrow(points[2] + normal * 0.45, logger.get_left(), buff=0.10,
                      color=MID_GRAY, stroke_width=1.3,
                      max_tip_length_to_length_ratio=0.05)

        primary = self.note_panel("PRIMARY: PHOTOGATES", [
            "gate at x = 0 starts timing",
            "later gates timestamp crossings",
            "no human stop-button delay",
        ], width=3.35, height=2.15, title_size=20, body_size=16).move_to(right.get_center() + DOWN * 0.45)
        alt_sensor = self.sensor_box().scale(0.72).move_to(right.get_center() + DOWN * 2.00 + LEFT * 0.80)
        alt_text = self.txt("alternative: motion sensor", 16, BOLD, DARK_GRAY).next_to(alt_sensor, RIGHT, buff=0.15)
        self.fit(alt_text, 2.15, 0.28)

        foot = self.formula_panel(r"\boxed{\text{Calibrate / align sensors before collecting the dataset}}",
                                  width=9.8, height=0.86, size=28).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), run_time=0.60)
        self.play_t(Create(ramp), Create(floor), Create(support), FadeIn(ball), run_time=0.70)
        self.play_t(FadeIn(gates), FadeIn(gate_labels), run_time=0.70)
        self.play_t(FadeIn(logger), FadeIn(logger_t), FadeIn(logger_s), GrowArrow(cable), run_time=0.65)
        self.play_t(FadeIn(primary), FadeIn(alt_sensor), FadeIn(alt_text), FadeIn(foot), run_time=0.75)
        self.wait_t(2.3)
        self.clear_stage()

    def sensor_acquisition(self, number=7):
        self.set_header(number, "SENSOR RUN — WATCH THE TIMESTAMPS APPEAR",
                        "The ball crosses fixed positions while the electronics records elapsed times automatically.")
        left = self.panel(8.85, 5.10).move_to(LEFT * 2.58 + DOWN * 0.12)
        right = self.panel(4.30, 5.10).move_to(RIGHT * 4.95 + DOWN * 0.12)
        start, end, ramp, floor, support, ball, ddown, normal = self.ramp_geometry(
            start=(-6.15, -1.05, 0), end=(1.20, 1.20, 0)
        )
        fracs = [0.0, 0.25, 0.50, 0.75, 1.00]
        points = [end + f * (start - end) for f in fracs]
        gates = VGroup(*[self.photogate(p, normal, 0.24) for p in points])
        positions = ["0.00", "0.25", "0.50", "0.75", "1.00"]
        times = ["0.000", "0.447", "0.632", "0.775", "0.894"]
        rows = [[p, "—"] for p in positions]
        table = self.compact_table(["x (m)", "time (s)"], rows, width=3.35, row_height=0.55, font_size=19)
        table.move_to(right.get_center() + UP * 0.15)
        title = self.txt("AUTOMATIC RECORD", 22, BOLD).next_to(table, UP, buff=0.23)
        exnote = self.txt("illustrative sensor data", 17, BOLD, DARK_GRAY).next_to(table, DOWN, buff=0.18)

        # Live timestamps placed beside gates as the ball passes.
        stamp_labels = VGroup()
        for i, (p, t) in enumerate(zip(points, times)):
            pos = p + normal * (0.48 if i % 2 == 0 else -0.48)
            stamp_labels.add(self.txt(f"{t} s", 16, BOLD, DARK_GRAY).move_to(pos))

        self.play_t(FadeIn(left), FadeIn(right), run_time=0.60)
        self.play_t(Create(ramp), Create(floor), Create(support), FadeIn(ball), FadeIn(gates), run_time=0.75)
        self.play_t(FadeIn(title), FadeIn(table), FadeIn(exnote), run_time=0.65)
        self.play_t(FadeIn(stamp_labels[0]), run_time=0.35)

        # Accelerating visual motion: each successive equal-distance segment takes less time.
        segment_durations = [0.95, 0.68, 0.55, 0.46]
        for i in range(1, 5):
            self.play_t(MoveAlongPath(ball, Line(ball.get_center(), points[i] + normal * 0.18),
                                      rate_func=linear), run_time=segment_durations[i - 1])
            self.play_t(FadeIn(stamp_labels[i]), run_time=0.30)

        auto = self.formula_panel(r"\text{equal distance segments take less and less time}",
                                  width=9.0, height=0.84, size=28).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(auto), run_time=0.60)
        self.wait_t(2.2)
        self.clear_stage()

    def sensor_analysis(self, number=8):
        self.set_header(number, "SENSOR DATA — TEST THE SAME SQUARE-TIME RELATION",
                        "Automatic timing improves temporal resolution, but the analysis logic is exactly the same as the stopwatch method.")
        left = self.panel(6.35, 5.00).move_to(LEFT * 3.55 + DOWN * 0.10)
        right = self.panel(6.35, 5.00).move_to(RIGHT * 3.55 + DOWN * 0.10)
        lt = self.txt("ILLUSTRATIVE SENSOR DATA", 22, BOLD).next_to(left.get_top(), DOWN, buff=0.22)
        headers = ["x (m)", "t (s)", "t² (s²)"]
        rows = [
            ["0.00", "0.000", "0.000"],
            ["0.25", "0.447", "0.200"],
            ["0.50", "0.632", "0.399"],
            ["0.75", "0.775", "0.601"],
            ["1.00", "0.894", "0.799"],
        ]
        table = self.compact_table(headers, rows, width=5.35, row_height=0.53, font_size=19)
        table.move_to(left.get_center() + UP * 0.25)
        note = self.formula_panel(r"x\approx1.25\,t^2", width=3.8, height=0.84, size=34)
        note.move_to(left.get_center() + DOWN * 1.72)
        ex = self.txt("example only — replace with measured sensor output", 16, BOLD, DARK_GRAY)
        ex.move_to(left.get_bottom() + UP * 0.25)

        rt = self.txt("x  vs  t²", 24, BOLD).next_to(right.get_top(), DOWN, buff=0.22)
        axes = Axes(x_range=[0, 0.9, 0.2], y_range=[0, 1.1, 0.25],
                    x_length=4.8, y_length=3.10,
                    axis_config={"color": BLACK_2, "stroke_width": 2, "include_tip": False})
        axes.move_to(right.get_center() + DOWN * 0.20)
        tx = [0.0, 0.200, 0.399, 0.601, 0.799]
        xx = [0.0, 0.25, 0.50, 0.75, 1.00]
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.06, color=BLACK_2) for a, b in zip(tx, xx)])
        line = axes.plot(lambda q: 1.25 * q, x_range=[0, 0.80], color=BLACK_2, stroke_width=3.5)
        labs = VGroup(
            self.txt("t² (s²)", 17).next_to(axes.x_axis, DOWN, buff=0.08),
            self.txt("x (m)", 17).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.11),
        )
        conclusion = self.formula_panel(r"\boxed{\text{straight }x\text{ vs }t^2\ \Rightarrow\ x\propto t^2}",
                                        width=9.7, height=0.90, size=30).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=0.65)
        self.play_t(FadeIn(table), FadeIn(note), FadeIn(ex), run_time=0.75)
        self.play_t(Create(axes), FadeIn(labs), FadeIn(dots), run_time=0.70)
        self.play_t(Create(line), FadeIn(conclusion), run_time=0.70)
        self.wait_t(2.4)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Comparison, interpretation, and closing
    # ------------------------------------------------------------------
    def compare_methods(self, number=9):
        self.set_header(number, "WHICH VERSION SHOULD YOU USE IN THE LAB?",
                        "Both methods answer the same question. Choose the measurement system that your classroom actually has.")
        left = self.panel(6.35, 4.90).move_to(LEFT * 3.55 + DOWN * 0.10)
        right = self.panel(6.35, 4.90).move_to(RIGHT * 3.55 + DOWN * 0.10)
        lt = self.txt("A  STOPWATCH", 26, BOLD).next_to(left.get_top(), DOWN, buff=0.26)
        rt = self.txt("B  SENSORS", 26, BOLD).next_to(right.get_top(), DOWN, buff=0.26)
        sw = self.stopwatch_icon(0.72).next_to(lt, DOWN, buff=0.20)
        sg = self.photogate(ORIGIN, UP, 0.24).scale(1.05).next_to(rt, DOWN, buff=0.25)
        lbody = VGroup(
            self.txt("+ works with basic equipment", 21, BOLD),
            self.txt("+ excellent for teamwork", 21),
            self.txt("− human start/stop uncertainty", 21),
            self.txt("→ repeat 3 trials per target", 21, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.23).move_to(left.get_center() + DOWN * 0.65)
        rbody = VGroup(
            self.txt("+ automatic timestamps", 21, BOLD),
            self.txt("+ more precise timing", 21),
            self.txt("− requires alignment / calibration", 21),
            self.txt("→ verify every sensor before release", 21, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.23).move_to(right.get_center() + DOWN * 0.65)
        common = self.formula_panel(r"\boxed{\text{Same physics: same ramp, same release, same }x\text{ vs }t^2\text{ test}}",
                                    width=10.6, height=0.92, size=29).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), FadeIn(sw), FadeIn(sg), run_time=0.70)
        self.play_t(FadeIn(lbody), FadeIn(rbody), run_time=0.75)
        self.play_t(FadeIn(common), run_time=0.60)
        self.wait_t(2.4)
        self.clear_stage()

    def scientific_conclusion(self, number=10, mode="BOTH"):
        self.set_header(number, "FROM MEASUREMENTS TO GALILEO'S SQUARE-TIME PATTERN",
                        "Do not claim the result from one run: use repeated measurements, a graph, and the pattern of the complete dataset.")
        left = self.panel(5.25, 4.75).move_to(LEFT * 4.45 + DOWN * 0.10)
        mid = self.panel(3.55, 4.75).move_to(DOWN * 0.10)
        right = self.panel(5.25, 4.75).move_to(RIGHT * 4.45 + DOWN * 0.10)
        ltitle = self.txt("1  MEASURE", 24, BOLD).next_to(left.get_top(), DOWN, buff=0.25)
        mtitle = self.txt("2  TRANSFORM", 24, BOLD).next_to(mid.get_top(), DOWN, buff=0.25)
        rtitle = self.txt("3  TEST", 24, BOLD).next_to(right.get_top(), DOWN, buff=0.25)
        if mode == "STOPWATCH":
            measure_lines = ["3 trials per target", "mean elapsed time", "record x and mean t"]
        elif mode == "SENSORS":
            measure_lines = ["automatic crossing times", "verify sensor alignment", "record x and t"]
        else:
            measure_lines = ["stopwatch OR sensors", "same release each run", "record x and t"]
        lb = VGroup(*[self.txt(s, 21, BOLD if i == 0 else NORMAL, DARK_GRAY)
                      for i, s in enumerate(measure_lines)]).arrange(DOWN, buff=0.28)
        lb.move_to(left.get_center() + DOWN * 0.15)
        mb = VGroup(self.math(r"t\rightarrow t^2", 44),
                    self.txt("add a t² column", 21, BOLD, DARK_GRAY),
                    self.txt("do not change x", 21, DARK_GRAY)).arrange(DOWN, buff=0.35)
        mb.move_to(mid.get_center() + DOWN * 0.05)
        rb = VGroup(self.txt("plot x vs t²", 22, BOLD),
                    self.txt("look for a straight trend", 22),
                    self.formula_panel(r"\boxed{x\propto t^2}", width=3.9, height=0.95, size=39)).arrange(DOWN, buff=0.34)
        rb.move_to(right.get_center() + DOWN * 0.12)
        final = self.formula_panel(r"\text{Experimental claim: position grows approximately with the square of time}",
                                   width=11.5, height=0.90, size=29).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(left), FadeIn(mid), FadeIn(right), FadeIn(ltitle), FadeIn(mtitle), FadeIn(rtitle), run_time=0.70)
        self.play_t(FadeIn(lb), FadeIn(mb), FadeIn(rb), run_time=0.80)
        self.play_t(FadeIn(final), run_time=0.60)
        self.wait_t(2.5)
        self.clear_stage()

    def lab_checklist(self, number=11, mode="BOTH"):
        self.set_header(number, "STUDENT LAB CHECKLIST",
                        "A clean experiment is more valuable than a complicated setup. Keep the procedure repeatable and the data traceable.")
        if mode == "STOPWATCH":
            title = "STOPWATCH VERSION — READY TO RUN"
            lines = [
                "□ ramp secured and catch zone clear",
                "□ 0.25 m target marks measured along ramp",
                "□ one release line marked",
                "□ 3 trials planned for every target",
                "□ recorder table prepared before release",
                "□ calculate mean t, then t², then graph",
            ]
        elif mode == "SENSORS":
            title = "SENSOR VERSION — READY TO RUN"
            lines = [
                "□ ramp secured and catch zone clear",
                "□ sensor positions measured along ramp",
                "□ release gate / x = 0 defined",
                "□ every gate aligned and detected",
                "□ one test run completed before data run",
                "□ export x and t, then compute t² and graph",
            ]
        else:
            title = "CHOOSE A METHOD — THEN RUN THE SAME PHYSICS"
            lines = [
                "□ ramp secured and catch zone clear",
                "□ distances measured along ramp",
                "□ one fixed release line — no push",
                "□ Stopwatch: 3 trials per target",
                "□ Sensors: align / calibrate before recording",
                "□ plot x vs t² and defend the conclusion",
            ]
        card = self.note_panel(title, lines, width=10.8, height=4.65, title_size=27, body_size=22)
        card.move_to(DOWN * 0.12)
        bottom = self.formula_panel(r"\boxed{\text{OBSERVE}\ \rightarrow\ \text{MEASURE}\ \rightarrow\ \text{GRAPH}\ \rightarrow\ \text{CONCLUDE}}",
                                    width=9.8, height=0.92, size=31).to_edge(DOWN, buff=0.27)
        self.play_t(FadeIn(card), run_time=0.80)
        self.play_t(FadeIn(bottom), run_time=0.60)
        self.wait_t(3.5)


class Physics9InclinedPlaneLabMaster(Physics9InclinedPlaneLabBase):
    """Full combined laboratory presentation: stopwatch + sensors."""

    def construct(self):
        self.opening("BOTH")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.stopwatch_protocol(3)
        self.stopwatch_trial(4)
        self.stopwatch_analysis(5)
        self.sensor_protocol(6)
        self.sensor_acquisition(7)
        self.sensor_analysis(8)
        self.compare_methods(9)
        self.scientific_conclusion(10, "BOTH")
        self.lab_checklist(11, "BOTH")


class Physics9InclinedPlaneLabStopwatch(Physics9InclinedPlaneLabBase):
    """Standalone no-sensor laboratory video."""

    def construct(self):
        self.opening("STOPWATCH")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.stopwatch_protocol(3)
        self.stopwatch_trial(4)
        self.stopwatch_analysis(5)
        self.scientific_conclusion(6, "STOPWATCH")
        self.lab_checklist(7, "STOPWATCH")


class Physics9InclinedPlaneLabSensors(Physics9InclinedPlaneLabBase):
    """Standalone sensor-based laboratory video."""

    def construct(self):
        self.opening("SENSORS")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.sensor_protocol(3)
        self.sensor_acquisition(4)
        self.sensor_analysis(5)
        self.scientific_conclusion(6, "SENSORS")
        self.lab_checklist(7, "SENSORS")
