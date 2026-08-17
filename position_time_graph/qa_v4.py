#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior projection QA V4 for Position vs. Time Graph.

Goals after inspecting the actual V3 1920x1080 render:
- use substantially more of the available teaching canvas,
- strengthen motion -> reading -> ordered pair -> recorded row causality,
- enlarge graph construction and slope geometry,
- make the six-step method readable from the back of a classroom,
- preserve the JP classroom monochrome visual contract and V3 header behavior.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, literal -pqh final render.
"""
from qa_v3 import *


class PositionTimeGraphLessonV4(PositionTimeGraphLessonV3):
    """Senior QA revision driven by rendered-pixel inspection of V3."""

    def standard_opening(self, course_label, title, subtitle, promise):
        group = VGroup(
            self.text(course_label, 34, BOLD),
            self.text(title, 66, BOLD),
            Line(LEFT * 6.15, RIGHT * 6.15, color=BLACK_LINE, stroke_width=2.4),
            self.text(subtitle, 35),
            self.text(promise, 32, MEDIUM),
        ).arrange(DOWN, buff=0.34)
        self.fit(group, 14.5, 6.9)
        self.play(FadeIn(group[0], shift=UP * 0.16), run_time=RUN_NORMAL)
        self.play(Write(group[1]), run_time=RUN_SLOW)
        self.play(Create(group[2]), FadeIn(group[3]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(group[4], shift=UP * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str):
        closing = self.text(sentence, 46, BOLD)
        self.fit(closing, 14.0, 1.35)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_QUICK)
        self.wait(0.25)

    def make_axes(self, x_len=10.1, y_len=5.25):
        axes = Axes(
            x_range=[0, 8, 1], y_range=[0, 7, 1],
            x_length=x_len, y_length=y_len,
            axis_config={
                "color": BLACK_LINE, "stroke_width": 2.7,
                "include_numbers": True, "font_size": 31,
                "include_ticks": True, "tick_size": 0.065,
            },
            x_axis_config={"numbers_to_include": list(range(0, 8))},
            y_axis_config={"numbers_to_include": list(range(0, 7))},
            tips=False,
        )
        labels = axes.get_axis_labels(
            self.math(r"t\;(\mathrm{s})", 36),
            self.math(r"x\;(\mathrm{m})", 36),
        )
        return axes, labels

    def axes_meaning(self):
        self.set_header(
            1, "WHAT DOES THE GRAPH RECORD?",
            "A position–time graph records where the object is at each clock reading: horizontal is time, vertical is position.",
        )
        left = self.note_panel(
            "HORIZONTAL AXIS",
            ["Quantity: time", "Symbol: t", "Unit: seconds (s)"],
            width=6.35, title_size=31, body_size=28,
        )
        right = self.note_panel(
            "VERTICAL AXIS",
            ["Quantity: position", "Symbol: x", "Unit: metres (m)"],
            width=6.35, title_size=31, body_size=28,
        )
        cards = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(UP * 0.45)
        meaning = self.formula_panel(
            r"(t,x)\;=\;\text{one clock reading paired with one position reading}",
            width=13.25, height=1.42, font_size=45,
        )
        meaning.next_to(cards, DOWN, buff=0.50)
        self.play(FadeIn(left, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def motion_to_data(self):
        self.set_header(
            2, "MEASURE POSITION BEFORE DRAWING THE GRAPH",
            "For every clock reading: locate the object, form the ordered pair (t, x), then record that same pair in the data table.",
        )

        left_center = -3.25
        track = NumberLine(
            x_range=[0, 7, 1], length=7.35,
            color=BLACK_LINE, stroke_width=3.2,
            include_numbers=False, include_tip=False,
        ).move_to([left_center, -1.05, 0])
        track_numbers = VGroup(*[
            self.math(str(n), 31).next_to(track.n2p(n), DOWN, buff=0.14)
            for n in range(8)
        ])
        track_label = self.text("POSITION TRACK   x (m)", 34, BOLD).next_to(track, UP, buff=0.36)
        origin_tag = self.text("origin", 23, MEDIUM).next_to(track.n2p(0), DOWN, buff=0.55)

        mover = Dot(track.n2p(0), radius=0.17, color=BLACK_LINE)
        mover_label = self.text("object", 28, BOLD).next_to(mover, UP, buff=0.15)

        measure_box = RoundedRectangle(
            width=7.10, height=1.58, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.3,
            fill_color=PAPER_GRAY, fill_opacity=1,
        ).move_to([left_center, 1.22, 0])
        step1 = self.text("1  OBSERVE + READ", 29, BOLD).next_to(measure_box, UP, buff=0.13).align_to(measure_box, LEFT)
        measure_title = self.text("CURRENT MEASUREMENT", 26, BOLD)
        time_value = self.math(r"t=0\;\mathrm{s}", 47)
        pos_value = self.math(r"x=0\;\mathrm{m}", 47)
        measure_values = VGroup(time_value, pos_value).arrange(RIGHT, buff=1.10)
        measure_content = VGroup(measure_title, measure_values).arrange(DOWN, buff=0.16).move_to(measure_box)
        measurement = VGroup(measure_box, measure_content)

        pair_box = RoundedRectangle(
            width=6.35, height=0.92, corner_radius=0.10,
            stroke_color=MID_GRAY, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        ).move_to([left_center, -2.33, 0])
        pair_label = self.text("2  FORM  (t, x) =", 27, BOLD).move_to(pair_box).shift(LEFT * 1.58)
        pair_source = VGroup(self.math("0", 38), self.math("0", 38)).arrange(RIGHT, buff=1.20)
        pair_source.move_to(pair_box).shift(RIGHT * 1.72)

        table_box = RoundedRectangle(
            width=5.45, height=6.05, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 4.25 + DOWN * 0.48)
        table_box.set_z_index(-5)
        step3 = self.text("3  RECORD THE SAME PAIR", 28, BOLD).next_to(table_box, UP, buff=0.13).align_to(table_box, LEFT)

        tx = table_box.get_center()[0]
        left_x = tx - 1.38
        right_x = tx + 1.37
        header_y = 1.18
        left_header = self.text("time  t (s)", 31, BOLD).move_to([left_x, header_y, 0])
        right_header = self.text("position  x (m)", 31, BOLD).move_to([right_x, header_y, 0])
        self.fit(left_header, 2.20, 0.55)
        self.fit(right_header, 2.38, 0.55)
        header = VGroup(left_header, right_header)
        header_rule = Line(
            [table_box.get_left()[0] + 0.30, 0.80, 0],
            [table_box.get_right()[0] - 0.30, 0.80, 0],
            color=LIGHT_GRAY, stroke_width=2,
        )
        divider = Line([tx, 1.52, 0], [tx, -2.72, 0], color=VERY_LIGHT_GRAY, stroke_width=1.4)

        row_y = [0.42 - 0.43 * i for i in range(len(TIMES))]
        rows = VGroup(*[
            VGroup(
                self.math(str(int(t)), 38).move_to([left_x, y, 0]),
                self.math(str(int(x)), 38).move_to([right_x, y, 0]),
            )
            for (t, x), y in zip(zip(TIMES, POSITIONS), row_y)
        ])

        self.play(
            FadeIn(step1), FadeIn(measurement),
            Create(track), FadeIn(track_numbers), FadeIn(track_label), FadeIn(origin_tag),
            FadeIn(mover), FadeIn(mover_label),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_READ)
        self.play(FadeIn(pair_box), FadeIn(pair_label), FadeIn(pair_source), run_time=RUN_NORMAL)
        self.play(FadeIn(table_box), FadeIn(step3), FadeIn(header), Create(header_rule), Create(divider), run_time=RUN_NORMAL)

        previous_highlight = None
        current_time = time_value
        current_pos = pos_value
        current_pair = pair_source
        for idx, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            target = track.n2p(x)
            new_time = self.math(rf"t={int(t)}\;\mathrm{{s}}", 47).move_to(current_time)
            new_pos = self.math(rf"x={int(x)}\;\mathrm{{m}}", 47).move_to(current_pos)
            new_pair = VGroup(self.math(str(int(t)), 38), self.math(str(int(x)), 38)).arrange(RIGHT, buff=1.20).move_to(pair_box).shift(RIGHT * 1.72)
            highlight = RoundedRectangle(
                width=4.72, height=0.40, corner_radius=0.04,
                color=MID_GRAY, stroke_width=1.4,
                fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
            ).move_to([tx, row_y[idx], 0])
            highlight.set_z_index(-1)

            move_anims = [
                mover.animate.move_to(target),
                mover_label.animate.next_to(target, UP, buff=0.15),
                ReplacementTransform(current_time, new_time),
                ReplacementTransform(current_pos, new_pos),
                ReplacementTransform(current_pair, new_pair),
            ]
            if previous_highlight is not None:
                move_anims.append(FadeOut(previous_highlight))
            self.play(*move_anims, run_time=0.95)
            current_time, current_pos, current_pair = new_time, new_pos, new_pair

            self.play(FadeIn(highlight), run_time=0.25)
            self.play(TransformFromCopy(current_pair, rows[idx]), run_time=0.72)
            previous_highlight = highlight
            self.wait(0.72)

        final_note = self.text("One clock reading + one position reading = one graph point.", 29, BOLD)
        final_note.move_to([left_center, -3.18, 0])
        self.play(FadeIn(final_note, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def plot_points(self):
        self.set_header(
            3, "PLOT EACH ORDERED PAIR (t, x)",
            "For each recorded pair, move across to t, move up to x, and place the point where those two readings meet.",
        )
        axes, labels = self.make_axes(10.65, 5.50)
        VGroup(axes, labels).move_to(LEFT * 1.55 + DOWN * 0.55)

        note = self.note_panel(
            "READ ONE PAIR",
            ["Across → time t", "Up → position x", "Intersection → one point"],
            width=3.75, title_size=29, body_size=25,
        ).move_to(RIGHT * 5.55 + UP * 0.55)
        pair_box = self.formula_panel(r"(t,x)=(0,0)", width=3.75, height=1.08, font_size=38)
        pair_box.next_to(note, DOWN, buff=0.28)

        self.play(Create(axes.x_axis), Create(axes.y_axis), FadeIn(labels), FadeIn(note), FadeIn(pair_box), run_time=RUN_SLOW)
        current_pair_box = pair_box
        for idx, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            new_pair_box = self.formula_panel(rf"(t,x)=({int(t)},{int(x)})", width=3.75, height=1.08, font_size=38)
            new_pair_box.move_to(current_pair_box)
            if idx > 0:
                self.play(ReplacementTransform(current_pair_box, new_pair_box), run_time=0.35)
                current_pair_box = new_pair_box

            v = DashedLine(axes.c2p(t, 0), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.6, dash_length=0.08)
            h = DashedLine(axes.c2p(0, x), axes.c2p(t, x), color=MID_GRAY, stroke_width=1.6, dash_length=0.08)
            d = Dot(axes.c2p(t, x), radius=0.105, color=BLACK_LINE)
            tag = self.math(rf"({int(t)},{int(x)})", 27).next_to(d, UR, buff=0.07)
            self.play(Create(v), run_time=0.28)
            self.play(Create(h), run_time=0.28)
            self.play(TransformFromCopy(current_pair_box[1], d), FadeIn(tag), run_time=0.42)
            self.wait(0.26)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def connect_and_read(self):
        self.set_header(
            4, "CONNECT THE DATA AND READ THE MOTION",
            "Now read the shape in time order: rising means position increases, flat means no change in position, falling means position decreases.",
        )
        axes, labels = self.make_axes(10.25, 5.25)
        VGroup(axes, labels).move_to(LEFT * 1.80 + DOWN * 0.55)
        pts = VGroup(*[
            Dot(axes.c2p(t, x), radius=0.10, color=BLACK_LINE)
            for t, x in zip(TIMES, POSITIONS)
        ])
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=5.0),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=5.0),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=5.0),
        )
        notes = VGroup(
            self.note_panel("0–3 s  RISING", ["Position increases", "Motion: forward"], width=3.90, title_size=27, body_size=25),
            self.note_panel("3–5 s  FLAT", ["Position stays constant", "Motion: at rest"], width=3.90, title_size=27, body_size=25),
            self.note_panel("5–7 s  FALLING", ["Position decreases", "Motion: back"], width=3.90, title_size=27, body_size=25),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 5.45 + DOWN * 0.52)

        self.play(Create(axes), FadeIn(labels), FadeIn(pts), run_time=RUN_NORMAL)
        for seg, note in zip(segs, notes):
            self.play(Create(seg), FadeIn(note, shift=LEFT * 0.08), run_time=RUN_SLOW)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def slope_velocity(self):
        self.set_header(
            5, "SLOPE OF x(t) = VELOCITY",
            "Slope compares the vertical change in position with the horizontal change in time; its sign tells the direction of motion.",
        )
        axes, labels = self.make_axes(9.60, 5.10)
        VGroup(axes, labels).move_to(LEFT * 2.45 + DOWN * 0.55)
        segs = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(3, 6), color=BLACK_LINE, stroke_width=4.8),
            Line(axes.c2p(3, 6), axes.c2p(5, 6), color=BLACK_LINE, stroke_width=4.8),
            Line(axes.c2p(5, 6), axes.c2p(7, 2), color=BLACK_LINE, stroke_width=4.8),
        )

        formula = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}", width=4.90, height=1.16, font_size=50)
        c1 = self.formula_panel(r"v_1=\frac{6-0}{3-0}=+2\;\mathrm{m/s}", width=5.05, height=1.14, font_size=36)
        c2 = self.formula_panel(r"v_2=\frac{6-6}{5-3}=0\;\mathrm{m/s}", width=5.05, height=1.14, font_size=36)
        c3 = self.formula_panel(r"v_3=\frac{2-6}{7-5}=-2\;\mathrm{m/s}", width=5.05, height=1.14, font_size=36)
        VGroup(formula, c1, c2, c3).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.95 + DOWN * 0.52)

        self.play(Create(axes), FadeIn(labels), Create(segs), FadeIn(formula), run_time=RUN_NORMAL)

        rise = Line(axes.c2p(0, 0), axes.c2p(0, 6), color=MID_GRAY, stroke_width=2.6)
        run = Line(axes.c2p(0, 6), axes.c2p(3, 6), color=MID_GRAY, stroke_width=2.6)
        dx = self.math(r"\Delta x=+6\;\mathrm{m}", 30).next_to(rise, LEFT, buff=0.12)
        dt = self.math(r"\Delta t=3\;\mathrm{s}", 30).next_to(run, UP, buff=0.10)
        self.play(Create(rise), Create(run), FadeIn(dx), FadeIn(dt), FadeIn(c1), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        rest_tag = self.text("flat segment → Δx = 0", 27, BOLD).next_to(segs[1], UP, buff=0.18)
        self.play(FadeOut(rise), FadeOut(run), FadeOut(dx), FadeOut(dt), FadeIn(rest_tag), FadeIn(c2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(rest_tag), run_time=RUN_QUICK)

        drop = Line(axes.c2p(5, 6), axes.c2p(5, 2), color=MID_GRAY, stroke_width=2.6)
        run3 = Line(axes.c2p(5, 2), axes.c2p(7, 2), color=MID_GRAY, stroke_width=2.6)
        dx3 = self.math(r"\Delta x=-4\;\mathrm{m}", 30).next_to(drop, LEFT, buff=0.12)
        dt3 = self.math(r"\Delta t=2\;\mathrm{s}", 30).next_to(run3, DOWN, buff=0.10)
        self.play(Create(drop), Create(run3), FadeIn(dx3), FadeIn(dt3), FadeIn(c3), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary(self):
        self.set_header(
            6, "FROM MOTION TO GRAPH — THE METHOD",
            "A reliable construction always follows the same chain: define position, measure pairs, plot them, connect them, then interpret the slope.",
        )
        items = [
            ("1", "CHOOSE ORIGIN", "Define where x = 0 m"),
            ("2", "MEASURE t AND x", "Read clock + position together"),
            ("3", "LABEL AXES + UNITS", "t in s; x in m"),
            ("4", "PLOT EACH (t, x)", "Across to t, then up to x"),
            ("5", "CONNECT IN TIME ORDER", "Reveal the motion shape"),
            ("6", "READ THE SLOPE", "Slope gives velocity"),
        ]
        cards = VGroup()
        for num, title, body_text in items:
            badge = RoundedRectangle(
                width=0.76, height=0.58, corner_radius=0.08,
                stroke_color=BLACK_LINE, fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
            )
            btxt = self.text(num, 24, BOLD).move_to(badge)
            title_m = self.text(title, 28, BOLD)
            body_m = self.text(body_text, 24)
            words = VGroup(title_m, body_m).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            content = VGroup(VGroup(badge, btxt), words).arrange(RIGHT, buff=0.22)
            box = RoundedRectangle(
                width=6.25, height=1.34, corner_radius=0.10,
                stroke_color=BLACK_LINE, stroke_width=1.6,
                fill_color=WHITE, fill_opacity=1,
            )
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.32)
            cards.add(VGroup(box, content))

        cards.arrange_in_grid(rows=3, cols=2, buff=(0.30, 0.22)).move_to(UP * 0.10)
        key = self.formula_panel(
            r"\boxed{\text{point = position at one time}}\qquad\boxed{\text{slope = velocity}}",
            width=12.80, height=1.42, font_size=42,
        )
        key.next_to(cards, DOWN, buff=0.38)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.10), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Position tells where. Slope tells how position is changing.")
