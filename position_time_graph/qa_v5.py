#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior final QA V5 after full-resolution inspection of the V4 render.

V5 corrects rendered-pixel issues found during senior QA:
1) guarantee explicit numeric tick labels on every position-time graph;
2) display a literal ordered pair (t, x) with parentheses/comma before copying
   its two components into the data-table row;
3) keep all registration labels fully inside their cards with projection-safe spacing;
4) keep graph axis titles inside the safe graph envelope so side panels never cover them.

All other senior V4 improvements and the JP classroom contract are preserved.
"""
from qa_v4 import *


class PositionTimeGraphLessonV5(PositionTimeGraphLessonV4):
    """Final senior revision with guaranteed coordinate readability."""

    def make_axes(self, x_len=10.1, y_len=5.25):
        axes = Axes(
            x_range=[0, 8, 1], y_range=[0, 7, 1],
            x_length=x_len, y_length=y_len,
            axis_config={
                "color": BLACK_LINE, "stroke_width": 2.7,
                "include_numbers": False,
                "include_ticks": True, "tick_size": 0.065,
            },
            tips=False,
        )
        x_name = self.math(r"t\;(\mathrm{s})", 36)
        x_name.next_to(axes.x_axis.get_end(), DOWN, buff=0.13).shift(LEFT * 0.45)
        y_name = self.math(r"x\;(\mathrm{m})", 36)
        y_name.next_to(axes.y_axis.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.10)
        axis_names = VGroup(x_name, y_name)
        x_numbers = VGroup(*[
            self.math(str(n), 28).next_to(axes.c2p(n, 0), DOWN, buff=0.11)
            for n in range(0, 8)
        ])
        y_numbers = VGroup(*[
            self.math(str(n), 28).next_to(axes.c2p(0, n), LEFT, buff=0.11)
            for n in range(1, 7)
        ])
        labels = VGroup(axis_names, x_numbers, y_numbers)
        return axes, labels

    def _ordered_pair(self, t: int, x: int, size: int = 39):
        lpar = self.math("(", size)
        t_m = self.math(str(int(t)), size)
        comma = self.math(",", size)
        x_m = self.math(str(int(x)), size)
        rpar = self.math(")", size)
        pair = VGroup(lpar, t_m, comma, x_m, rpar).arrange(RIGHT, buff=0.075)
        return pair, t_m, x_m

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
        track_label = self.text("POSITION TRACK   x (m)", 34, BOLD).next_to(track, UP, buff=0.52)
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
        pair_label = self.text("2  FORM DATA PAIR", 27, BOLD).move_to(pair_box).align_to(pair_box, LEFT).shift(RIGHT * 0.28)
        pair_source, pair_t, pair_x = self._ordered_pair(0, 0)
        pair_source.move_to(pair_box).shift(RIGHT * 1.73)

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
        current_pair_t = pair_t
        current_pair_x = pair_x

        for idx, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            target = track.n2p(x)
            new_time = self.math(rf"t={int(t)}\;\mathrm{{s}}", 47).move_to(current_time)
            new_pos = self.math(rf"x={int(x)}\;\mathrm{{m}}", 47).move_to(current_pos)
            new_pair, new_pair_t, new_pair_x = self._ordered_pair(t, x)
            new_pair.move_to(pair_box).shift(RIGHT * 1.73)
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
            current_time, current_pos = new_time, new_pos
            current_pair = new_pair
            current_pair_t, current_pair_x = new_pair_t, new_pair_x

            self.play(FadeIn(highlight), run_time=0.25)
            self.play(
                TransformFromCopy(current_pair_t, rows[idx][0]),
                TransformFromCopy(current_pair_x, rows[idx][1]),
                run_time=0.72,
            )
            previous_highlight = highlight
            self.wait(0.72)

        final_note = self.text("One clock reading + one position reading = one graph point.", 29, BOLD)
        final_note.move_to([left_center, -3.18, 0])
        self.play(FadeIn(final_note, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()
