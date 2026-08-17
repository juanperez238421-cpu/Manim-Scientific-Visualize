#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior QA V2 for Position vs. Time Graph.

Keeps the exact JP classroom visual contract from main.py while enlarging
all classroom-facing typography and rebuilding the motion -> time/position
registration stage as an explicit OBSERVE -> READ -> RECORD sequence.
Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pqh final render.
"""
from main import *


class PositionTimeGraphLessonV2(PositionTimeGraphLesson):
    """QA-refined, larger and more explicit classroom version."""

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(
            width=0.78, height=0.56, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=WHITE_FILL, fill_opacity=1.0,
        )
        number_text = self.text(f"{number:02d}", 25, BOLD).move_to(number_box)
        title_text = self.text(title, 38, BOLD)
        self.fit(title_text, SAFE_WIDTH - 1.1, 0.58)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 96:
            mid = len(words) // 2
            subtitle_text = VGroup(
                self.text(" ".join(words[:mid]), 23),
                self.text(" ".join(words[mid:]), 23),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_text = self.text(subtitle, 24)
        self.fit(subtitle_text, 14.25, 0.72)
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

    def note_panel(self, title: str, lines, width=5.2, title_size=28, body_size=25):
        title_m = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14
        )
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.62, 3.65)
        box = RoundedRectangle(
            width=width, height=max(1.15, content.height + 0.62),
            corner_radius=0.12, stroke_color=BLACK_LINE,
            stroke_width=1.8, fill_color=WHITE, fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

    def standard_opening(self, course_label, title, subtitle, promise):
        group = VGroup(
            self.text(course_label, 31, BOLD),
            self.text(title, 56, BOLD),
            Line(LEFT * 5.7, RIGHT * 5.7, color=BLACK_LINE, stroke_width=2.2),
            self.text(subtitle, 30),
            self.text(promise, 28, MEDIUM),
        ).arrange(DOWN, buff=0.30)
        self.fit(group, 14.4, 6.6)
        self.play(FadeIn(group[0], shift=UP * 0.18), run_time=RUN_NORMAL)
        self.play(Write(group[1]), run_time=RUN_SLOW)
        self.play(Create(group[2]), FadeIn(group[3]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(group[4], shift=UP * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str):
        closing = self.text(sentence, 39, BOLD)
        self.fit(closing, 13.8, 1.25)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)

    def make_axes(self, x_len=9.1, y_len=4.85):
        axes = Axes(
            x_range=[0, 8, 1], y_range=[0, 7, 1],
            x_length=x_len, y_length=y_len,
            axis_config={
                "color": BLACK_LINE, "stroke_width": 2.5,
                "include_numbers": True, "font_size": 28,
                "include_ticks": True, "tick_size": 0.06,
            },
            x_axis_config={"numbers_to_include": list(range(0, 8))},
            y_axis_config={"numbers_to_include": list(range(0, 7))},
            tips=False,
        )
        labels = axes.get_axis_labels(
            self.math(r"t\;(\mathrm{s})", 33),
            self.math(r"x\;(\mathrm{m})", 33),
        )
        return axes, labels

    def axes_meaning(self):
        self.set_header(
            1, "WHAT DOES THE GRAPH RECORD?",
            "A position–time graph does not draw the path. It records position x at each time t.",
        )
        left = self.note_panel(
            "HORIZONTAL AXIS", ["Quantity: time", "Symbol: t", "Unit: seconds (s)"], width=5.7
        )
        right = self.note_panel(
            "VERTICAL AXIS", ["Quantity: position", "Symbol: x", "Unit: metres (m)"], width=5.7
        )
        cards = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(UP * 0.35)
        meaning = self.formula_panel(
            r"(t,x)\;\Longleftrightarrow\;\text{position }x\text{ at time }t",
            width=11.4, height=1.28, font_size=42,
        )
        meaning.next_to(cards, DOWN, buff=0.45)
        self.play(FadeIn(left, shift=RIGHT * 0.1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def motion_to_data(self):
        self.set_header(
            2, "MEASURE POSITION BEFORE DRAWING THE GRAPH",
            "Watch the object, read the clock, then register the matching time and position as one data pair.",
        )

        # LEFT: enlarged motion/position representation.
        track = NumberLine(
            x_range=[0, 7, 1], length=7.35,
            color=BLACK_LINE, stroke_width=2.8,
            include_numbers=True, font_size=31, include_tip=False,
        ).move_to(LEFT * 3.55 + DOWN * 0.62)
        label = self.text("POSITION TRACK   x (m)", 29, BOLD).next_to(track, UP, buff=0.34)
        observe_badge = self.text("1  OBSERVE", 24, BOLD).next_to(label, UP, buff=0.32).align_to(track, LEFT)
        mover = Dot(track.n2p(0), radius=0.14, color=BLACK_LINE)
        mover_label = self.text("object", 24, BOLD).next_to(mover, UP, buff=0.14)

        # Explicit live measurement card: time reading + position reading.
        measure_box = RoundedRectangle(
            width=6.65, height=1.48, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=PAPER_GRAY, fill_opacity=1,
        ).move_to(LEFT * 3.55 + UP * 1.38)
        measure_title = self.text("CURRENT MEASUREMENT", 22, BOLD)
        time_value = self.math(r"t=0\;\mathrm{s}", 39)
        pos_value = self.math(r"x=0\;\mathrm{m}", 39)
        measure_values = VGroup(time_value, pos_value).arrange(RIGHT, buff=0.95)
        measure_content = VGroup(measure_title, measure_values).arrange(DOWN, buff=0.16).move_to(measure_box)
        measurement = VGroup(measure_box, measure_content)

        # RIGHT: a substantially larger registration table.
        table_box = RoundedRectangle(
            width=5.0, height=5.35, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 4.65 + DOWN * 0.52)
        table_box.set_z_index(-5)
        record_badge = self.text("2  RECORD", 24, BOLD).next_to(table_box, UP, buff=0.16).align_to(table_box, LEFT)
        header = VGroup(
            self.text("time  t (s)", 28, BOLD),
            self.text("position  x (m)", 28, BOLD),
        ).arrange(RIGHT, buff=0.60)
        rows = VGroup(*[
            VGroup(self.math(str(int(t)), 31), self.math(str(int(x)), 31)).arrange(RIGHT, buff=1.68)
            for t, x in zip(TIMES, POSITIONS)
        ]).arrange(DOWN, buff=0.10)
        VGroup(header, rows).arrange(DOWN, buff=0.17).move_to(table_box)
        header_rule = Line(
            table_box.get_left() + RIGHT * 0.30 + UP * 1.72,
            table_box.get_right() + LEFT * 0.30 + UP * 1.72,
            color=LIGHT_GRAY, stroke_width=2,
        )

        self.play(
            Create(track), FadeIn(label), FadeIn(observe_badge),
            FadeIn(mover), FadeIn(mover_label), FadeIn(measurement),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_READ)
        self.play(
            FadeIn(table_box), FadeIn(record_badge), FadeIn(header), Create(header_rule),
            run_time=RUN_NORMAL,
        )

        previous_highlight = None
        current_time = time_value
        current_pos = pos_value
        for idx, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            target = track.n2p(x)
            new_time = self.math(rf"t={int(t)}\;\mathrm{{s}}", 39).move_to(current_time)
            new_pos = self.math(rf"x={int(x)}\;\mathrm{{m}}", 39).move_to(current_pos)
            highlight = SurroundingRectangle(
                rows[idx], buff=0.105, color=MID_GRAY, stroke_width=1.5,
                fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0,
            )
            highlight.set_z_index(-1)

            animations = [
                mover.animate.move_to(target),
                mover_label.animate.next_to(target, UP, buff=0.14),
                ReplacementTransform(current_time, new_time),
                ReplacementTransform(current_pos, new_pos),
            ]
            if previous_highlight is not None:
                animations.append(FadeOut(previous_highlight))
            self.play(*animations, run_time=0.90)
            current_time, current_pos = new_time, new_pos

            self.play(FadeIn(highlight), FadeIn(rows[idx], shift=UP * 0.06), run_time=0.58)
            previous_highlight = highlight
            self.wait(0.62)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def plot_points(self):
        self.set_header(
            3, "PLOT EACH ORDERED PAIR (t, x)",
            "Move across to the time, then up to the measured position, and place a point at the intersection.",
        )
        axes, labels = self.make_axes(9.55, 5.10)
        VGroup(axes, labels).move_to(LEFT * 2.0 + DOWN * 0.45)
        note = self.note_panel(
            "EXAMPLE: (3 s, 6 m)",
            ["Across → t = 3 s", "Up → x = 6 m", "The intersection is one measurement."],
            width=4.35, title_size=26, body_size=23,
        ).move_to(RIGHT * 5.1 + DOWN * 0.25)
        self.play(Create(axes.x_axis), Create(axes.y_axis), FadeIn(labels), FadeIn(note), run_time=RUN_SLOW)
        for t, x in zip(TIMES, POSITIONS):
            v = DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.4, dash_length=0.08)
            h = DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.4, dash_length=0.08)
            d = Dot(axes.c2p(t, x), radius=0.092, color=BLACK_LINE)
            tag = self.math(rf"({int(t)},{int(x)})", 24).next_to(d, UR, buff=0.06)
            self.play(Create(v), run_time=0.28)
            self.play(Create(h), run_time=0.28)
            self.play(FadeIn(d, scale=0.7), FadeIn(tag), run_time=0.34)
            self.wait(0.22)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def connect_and_read(self):
        self.set_header(
            4, "CONNECT THE DATA AND READ THE MOTION",
            "Rising, horizontal, and falling segments represent forward motion, rest, and motion back toward the origin.",
        )
        axes, labels = self.make_axes(9.15, 4.85)
        VGroup(axes, labels).move_to(LEFT * 2.25 + DOWN * 0.45)
        pts = VGroup(*[Dot(axes.c2p(t, x), radius=0.085, color=BLACK_LINE) for t, x in zip(TIMES, POSITIONS)])
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=4.4),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=4.4),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=4.4),
        )
        notes = VGroup(
            self.note_panel("0–3 s", ["Position increases", "Moving forward"], width=4.15, title_size=25, body_size=23),
            self.note_panel("3–5 s", ["Position is constant", "Object is at rest"], width=4.15, title_size=25, body_size=23),
            self.note_panel("5–7 s", ["Position decreases", "Moving back"], width=4.15, title_size=25, body_size=23),
        ).arrange(DOWN, buff=0.16).move_to(RIGHT * 5.05 + DOWN * 0.45)
        self.play(Create(axes), FadeIn(labels), FadeIn(pts), run_time=RUN_NORMAL)
        for seg, note in zip(segs, notes):
            self.play(Create(seg), FadeIn(note, shift=LEFT * 0.08), run_time=RUN_SLOW)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def slope_velocity(self):
        self.set_header(
            5, "SLOPE OF x(t) = VELOCITY",
            "Calculate change in position divided by change in time. The sign of the slope gives the direction of motion.",
        )
        axes, labels = self.make_axes(8.75, 4.65)
        VGroup(axes, labels).move_to(LEFT * 2.75 + DOWN * 0.45)
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=4.4),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=4.4),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=4.4),
        )
        formula = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}", width=5.25, height=1.08, font_size=46)
        c1 = self.formula_panel(r"v_1=\frac{6-0}{3-0}=+2\;\mathrm{m/s}", width=5.45, height=1.08, font_size=34)
        c2 = self.formula_panel(r"v_2=\frac{6-6}{5-3}=0\;\mathrm{m/s}", width=5.45, height=1.08, font_size=34)
        c3 = self.formula_panel(r"v_3=\frac{2-6}{7-5}=-2\;\mathrm{m/s}", width=5.45, height=1.08, font_size=34)
        VGroup(formula, c1, c2, c3).arrange(DOWN, buff=0.16).move_to(RIGHT * 4.85 + DOWN * 0.45)
        self.play(Create(axes), FadeIn(labels), Create(segs), FadeIn(formula), run_time=RUN_NORMAL)

        rise = Line(axes.c2p(0, 0), axes.c2p(0, 6), color=MID_GRAY, stroke_width=2.2)
        run = Line(axes.c2p(0, 6), axes.c2p(3, 6), color=MID_GRAY, stroke_width=2.2)
        self.play(Create(rise), Create(run), FadeIn(c1), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(rise), FadeOut(run), FadeIn(c2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        drop = Line(axes.c2p(5, 6), axes.c2p(5, 2), color=MID_GRAY, stroke_width=2.2)
        run3 = Line(axes.c2p(5, 2), axes.c2p(7, 2), color=MID_GRAY, stroke_width=2.2)
        self.play(Create(drop), Create(run3), FadeIn(c3), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary(self):
        self.set_header(
            6, "FROM MOTION TO GRAPH — THE METHOD",
            "Use this sequence every time you construct or interpret a position–time graph.",
        )
        items = [
            ("1", "CHOOSE ORIGIN"), ("2", "RECORD t AND x"), ("3", "LABEL AXES + UNITS"),
            ("4", "PLOT (t, x)"), ("5", "CONNECT DATA"), ("6", "READ SLOPE"),
        ]
        cards = VGroup()
        for num, txt in items:
            badge = RoundedRectangle(
                width=0.70, height=0.54, corner_radius=0.08,
                stroke_color=BLACK_LINE, fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
            )
            btxt = self.text(num, 22, BOLD).move_to(badge)
            body = self.text(txt, 24, BOLD)
            content = VGroup(VGroup(badge, btxt), body).arrange(RIGHT, buff=0.18)
            box = RoundedRectangle(
                width=4.50, height=1.18, corner_radius=0.10,
                stroke_color=BLACK_LINE, stroke_width=1.5,
                fill_color=WHITE, fill_opacity=1,
            )
            content.move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(cols=3, buff=(0.22, 0.25)).move_to(UP * 0.35)
        key = self.formula_panel(
            r"\boxed{\text{point: position at a time}}\qquad\boxed{\text{slope: velocity}}",
            width=12.1, height=1.32, font_size=38,
        )
        key.next_to(cards, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.12), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Position tells where. Slope tells how position is changing.")
