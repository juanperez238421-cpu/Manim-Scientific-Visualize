#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Position vs. Time Graph — step-by-step JP classroom lesson.

Visual contract integrated from the supplied jp_classroom_style(2).py:
1920x1080, 30 fps, white background, black/gray hierarchy, persistent
numbered headers, safe margins, deliberate pauses, and visual + equation
integration. Target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

# -----------------------------------------------------------------------------
# Exact project render/visual contract
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"
WHITE_FILL = WHITE
FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.60
CONTENT_BOTTOM_Y = -4.05
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.35
RUN_CAMERA = 1.25
PAUSE_SHORT = 0.85
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80
PAUSE_FINAL = 5.20

TIMES = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=float)
POSITIONS = np.array([0, 2, 4, 6, 6, 6, 4, 2], dtype=float)


def assert_close(actual: float, expected: float, tol: float = 1e-10) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"expected {expected}, got {actual}")


class JPClassroomScene(MovingCameraScene):
    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group = None
        self.subtitle_group = None

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight,
                    line_spacing=0.92, **kwargs)

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(self, mob: Mobject, max_width=SAFE_WIDTH, max_height=SAFE_HEIGHT):
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10,
                                      stroke_color=BLACK_LINE, stroke_width=2.0,
                                      fill_color=WHITE_FILL, fill_opacity=1.0)
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)
        title_text = self.text(title, 34, BOLD)
        self.fit(title_text, SAFE_WIDTH - 1.1, 0.56)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)
        words = subtitle.split()
        if len(subtitle) > 96:
            mid = len(words) // 2
            subtitle_text = VGroup(self.text(" ".join(words[:mid]), 20),
                                   self.text(" ".join(words[mid:]), 20)).arrange(
                                       DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_text = self.text(subtitle, 21)
        self.fit(subtitle_text, 14.25, 0.70)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)
        new_header = VGroup(title_row, rule)
        if self.header_group is None:
            self.header_group = new_header
            self.add(new_header)
        else:
            old = self.header_group
            self.header_group = new_header
            self.play(ReplacementTransform(old, new_header), run_time=RUN_QUICK)
        if self.subtitle_group is None:
            self.subtitle_group = subtitle_text
            self.add(subtitle_text)
        else:
            old = self.subtitle_group
            self.subtitle_group = subtitle_text
            self.play(ReplacementTransform(old, subtitle_text), run_time=RUN_QUICK)

    def clear_stage(self, keep_header=True) -> None:
        keep_ids = set()
        if keep_header:
            for item in (self.header_group, self.subtitle_group):
                if item is not None:
                    keep_ids.update(id(x) for x in item.get_family())
        removable = [m for m in self.mobjects if id(m) not in keep_ids]
        if removable:
            self.play(*[FadeOut(m) for m in removable], run_time=RUN_NORMAL)
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)

    def formula_panel(self, expression: str, width=8.4, height=1.25, font_size=42):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                               stroke_color=BLACK_LINE, stroke_width=2,
                               fill_color=PAPER_GRAY, fill_opacity=1)
        eq = self.math(expression, font_size)
        self.fit(eq, width - 0.55, height - 0.28)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(self, title: str, lines, width=5.2, title_size=25, body_size=22):
        title_m = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.62, 3.65)
        box = RoundedRectangle(width=width, height=max(1.15, content.height + 0.62),
                               corner_radius=0.12, stroke_color=BLACK_LINE,
                               stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

    def standard_opening(self, course_label, title, subtitle, promise):
        group = VGroup(self.text(course_label, 28, BOLD), self.text(title, 50, BOLD),
                       Line(LEFT * 5.5, RIGHT * 5.5, color=BLACK_LINE, stroke_width=2.2),
                       self.text(subtitle, 27), self.text(promise, 25, MEDIUM))
        group.arrange(DOWN, buff=0.30)
        self.fit(group, 14.4, 6.6)
        self.play(FadeIn(group[0], shift=UP * 0.18), run_time=RUN_NORMAL)
        self.play(Write(group[1]), run_time=RUN_SLOW)
        self.play(Create(group[2]), FadeIn(group[3]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(group[4], shift=UP * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str):
        closing = self.text(sentence, 34, BOLD)
        self.fit(closing, 13.8, 1.2)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)

    def focus_on(self, mob: Mobject, width=6.0, pause=PAUSE_READ):
        persistent = [x for x in (self.header_group, self.subtitle_group) if x is not None]
        if persistent:
            self.play(*[FadeOut(x) for x in persistent], run_time=RUN_QUICK)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=max(width, mob.width + 0.8)).move_to(mob),
                  run_time=RUN_CAMERA)
        self.wait(pause)
        self.play(Restore(self.camera.frame), run_time=RUN_CAMERA)
        if persistent:
            self.play(*[FadeIn(x) for x in persistent], run_time=RUN_QUICK)


class PositionTimeGraphLesson(JPClassroomScene):
    def construct(self) -> None:
        self.validate_data()
        self.opening()
        self.axes_meaning()
        self.motion_to_data()
        self.plot_points()
        self.connect_and_read()
        self.slope_velocity()
        self.summary()

    def validate_data(self):
        assert_close((6 - 0) / (3 - 0), 2.0)
        assert_close((6 - 6) / (5 - 3), 0.0)
        assert_close((2 - 6) / (7 - 5), -2.0)

    def make_axes(self, x_len=8.7, y_len=4.6):
        axes = Axes(
            x_range=[0, 8, 1], y_range=[0, 7, 1], x_length=x_len, y_length=y_len,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.3,
                         "include_numbers": True, "font_size": 23,
                         "include_ticks": True, "tick_size": 0.055},
            x_axis_config={"numbers_to_include": list(range(0, 8))},
            y_axis_config={"numbers_to_include": list(range(0, 7))},
            tips=False,
        )
        labels = axes.get_axis_labels(self.math(r"t\;(\mathrm{s})", 28),
                                      self.math(r"x\;(\mathrm{m})", 28))
        return axes, labels

    def opening(self):
        self.standard_opening(
            "MOTION • POSITION & TIME", "POSITION VS. TIME GRAPH",
            "Build the graph from a motion story, one decision at a time.",
            "Every point answers: Where is the object at this time?"
        )

    def axes_meaning(self):
        self.set_header(1, "WHAT DOES THE GRAPH RECORD?",
                        "A position–time graph does not draw the path. It records position x at each time t.")
        left = self.note_panel("HORIZONTAL AXIS",
                               ["Quantity: time", "Symbol: t", "Unit: seconds (s)"], width=5.4)
        right = self.note_panel("VERTICAL AXIS",
                                ["Quantity: position", "Symbol: x", "Unit: metres (m)"], width=5.4)
        cards = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(UP * 0.35)
        meaning = self.formula_panel(r"(t,x)\;\Longleftrightarrow\;\text{position }x\text{ at time }t",
                                     width=10.7, height=1.2, font_size=38)
        meaning.next_to(cards, DOWN, buff=0.45)
        self.play(FadeIn(left, shift=RIGHT * 0.1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def motion_to_data(self):
        self.set_header(2, "MEASURE POSITION BEFORE DRAWING THE GRAPH",
                        "Watch the object on a one-dimensional track and record its position once per second.")
        track = NumberLine(x_range=[0, 7, 1], length=6.6, color=BLACK_LINE,
                           stroke_width=2.4, include_numbers=True, font_size=24,
                           include_tip=False)
        track.move_to(LEFT * 3.8 + DOWN * 0.2)
        label = self.text("POSITION TRACK (m)", 24, BOLD).next_to(track, UP, buff=0.35)
        mover = Dot(track.n2p(0), radius=0.105, color=BLACK_LINE)
        mover_label = self.text("object", 20, BOLD).next_to(mover, UP, buff=0.12)

        # Data table built explicitly to preserve independently addressable rows.
        header = VGroup(self.text("t (s)", 23, BOLD), self.text("x (m)", 23, BOLD)).arrange(RIGHT, buff=0.9)
        rows = VGroup(*[
            VGroup(self.math(str(int(t)), 25), self.math(str(int(x)), 25)).arrange(RIGHT, buff=1.05)
            for t, x in zip(TIMES, POSITIONS)
        ]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        table_content = VGroup(header, rows).arrange(DOWN, buff=0.18)
        table_box = RoundedRectangle(width=4.0, height=5.05, corner_radius=0.12,
                                     stroke_color=BLACK_LINE, stroke_width=1.8,
                                     fill_color=WHITE, fill_opacity=1)
        table_content.move_to(table_box)
        table = VGroup(table_box, table_content).move_to(RIGHT * 4.7 + DOWN * 0.35)

        self.play(Create(track), FadeIn(label), FadeIn(mover), FadeIn(mover_label), run_time=RUN_NORMAL)
        self.play(FadeIn(table_box), FadeIn(header), run_time=RUN_NORMAL)
        for idx, x in enumerate(POSITIONS):
            target = track.n2p(x)
            self.play(mover.animate.move_to(target),
                      mover_label.animate.next_to(target, UP, buff=0.12),
                      FadeIn(rows[idx], shift=UP * 0.04), run_time=0.62)
            self.wait(0.35)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def plot_points(self):
        self.set_header(3, "PLOT EACH ORDERED PAIR (t, x)",
                        "Move across to the time, then up to the measured position, and place a point at the intersection.")
        axes, labels = self.make_axes(9.0, 4.8)
        graph_group = VGroup(axes, labels).move_to(LEFT * 2.0 + DOWN * 0.45)
        note = self.note_panel("EXAMPLE: (3 s, 6 m)",
                               ["Across → t = 3 s", "Up → x = 6 m",
                                "The intersection is one measurement."], width=4.6)
        note.move_to(RIGHT * 5.1 + DOWN * 0.25)
        self.play(Create(axes.x_axis), Create(axes.y_axis), FadeIn(labels), FadeIn(note), run_time=RUN_SLOW)
        dots = VGroup()
        guides = VGroup()
        for t, x in zip(TIMES, POSITIONS):
            v = DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY,
                           stroke_width=1.2, dash_length=0.08)
            h = DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY,
                           stroke_width=1.2, dash_length=0.08)
            d = Dot(axes.c2p(t, x), radius=0.075, color=BLACK_LINE)
            tag = self.math(rf"({int(t)},{int(x)})", 21).next_to(d, UR, buff=0.05)
            self.play(Create(v), run_time=0.28)
            self.play(Create(h), run_time=0.28)
            self.play(FadeIn(d, scale=0.7), FadeIn(tag), run_time=0.34)
            self.wait(0.20)
            dots.add(d, tag)
            guides.add(v, h)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def connect_and_read(self):
        self.set_header(4, "CONNECT THE DATA AND READ THE MOTION",
                        "Rising, horizontal, and falling segments represent forward motion, rest, and motion back toward the origin.")
        axes, labels = self.make_axes(8.6, 4.55)
        axes_group = VGroup(axes, labels).move_to(LEFT * 2.3 + DOWN * 0.45)
        pts = VGroup(*[Dot(axes.c2p(t, x), radius=0.07, color=BLACK_LINE)
                       for t, x in zip(TIMES, POSITIONS)])
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=4),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=4),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=4),
        )
        notes = VGroup(
            self.note_panel("0–3 s", ["Position increases", "Moving forward"], width=4.3, body_size=21),
            self.note_panel("3–5 s", ["Position is constant", "Object is at rest"], width=4.3, body_size=21),
            self.note_panel("5–7 s", ["Position decreases", "Moving back"], width=4.3, body_size=21),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 5.05 + DOWN * 0.45)
        self.play(Create(axes), FadeIn(labels), FadeIn(pts), run_time=RUN_NORMAL)
        for seg, note in zip(segs, notes):
            self.play(Create(seg), FadeIn(note, shift=LEFT * 0.08), run_time=RUN_SLOW)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def slope_velocity(self):
        self.set_header(5, "SLOPE OF x(t) = VELOCITY",
                        "Calculate change in position divided by change in time. The sign of the slope gives the direction of motion.")
        axes, labels = self.make_axes(8.1, 4.35)
        VGroup(axes, labels).move_to(LEFT * 2.7 + DOWN * 0.45)
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=4),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=4),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=4),
        )
        formula = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}", width=4.6, height=1.0, font_size=43)
        c1 = self.formula_panel(r"v_1=\frac{6-0}{3-0}=+2\;\mathrm{m/s}", width=5.2, height=1.0, font_size=31)
        c2 = self.formula_panel(r"v_2=\frac{6-6}{5-3}=0\;\mathrm{m/s}", width=5.2, height=1.0, font_size=31)
        c3 = self.formula_panel(r"v_3=\frac{2-6}{7-5}=-2\;\mathrm{m/s}", width=5.2, height=1.0, font_size=31)
        calcs = VGroup(formula, c1, c2, c3).arrange(DOWN, buff=0.18).move_to(RIGHT * 4.85 + DOWN * 0.45)
        self.play(Create(axes), FadeIn(labels), Create(segs), FadeIn(formula), run_time=RUN_NORMAL)

        rise = Line(axes.c2p(0, 0), axes.c2p(0, 6), color=MID_GRAY, stroke_width=2)
        run = Line(axes.c2p(0, 6), axes.c2p(3, 6), color=MID_GRAY, stroke_width=2)
        self.play(Create(rise), Create(run), FadeIn(c1), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(rise), FadeOut(run), FadeIn(c2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        drop = Line(axes.c2p(5, 6), axes.c2p(5, 2), color=MID_GRAY, stroke_width=2)
        run3 = Line(axes.c2p(5, 2), axes.c2p(7, 2), color=MID_GRAY, stroke_width=2)
        self.play(Create(drop), Create(run3), FadeIn(c3), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary(self):
        self.set_header(6, "FROM MOTION TO GRAPH — THE METHOD",
                        "Use this sequence every time you construct or interpret a position–time graph.")
        items = [
            ("1", "CHOOSE ORIGIN"), ("2", "RECORD t AND x"),
            ("3", "LABEL AXES + UNITS"), ("4", "PLOT (t, x)"),
            ("5", "CONNECT DATA"), ("6", "READ SLOPE"),
        ]
        cards = VGroup()
        for num, txt in items:
            badge = RoundedRectangle(width=0.66, height=0.50, corner_radius=0.08,
                                     stroke_color=BLACK_LINE, fill_color=VERY_LIGHT_GRAY,
                                     fill_opacity=1)
            btxt = self.text(num, 19, BOLD).move_to(badge)
            body = self.text(txt, 21, BOLD)
            content = VGroup(VGroup(badge, btxt), body).arrange(RIGHT, buff=0.18)
            box = RoundedRectangle(width=4.3, height=1.10, corner_radius=0.10,
                                   stroke_color=BLACK_LINE, stroke_width=1.5,
                                   fill_color=WHITE, fill_opacity=1)
            content.move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(cols=3, buff=(0.25, 0.25)).move_to(UP * 0.35)
        key = self.formula_panel(r"\boxed{\text{point: position at a time}}\qquad\boxed{\text{slope: velocity}}",
                                 width=11.5, height=1.25, font_size=34)
        key.next_to(cards, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in cards], lag_ratio=0.10),
                  run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Position tells where. Slope tells how position is changing.")


# Local preview:
# manim -pql main.py PositionTimeGraphLesson --format=mp4 --disable_caching
# Final:
# manim -pqh main.py PositionTimeGraphLesson --format=mp4 --disable_caching
