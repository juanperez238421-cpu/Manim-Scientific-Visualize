#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frame-audited final QA revision for Position vs. Time Graph.

This revision keeps the JP classroom contract and the larger V2 typography,
while fixing defects only visible after inspecting the actual 1920x1080 render:
- make the OBSERVE/READ badge fully visible,
- guarantee numeric position-track labels,
- give the table headers safe horizontal margins,
- enlarge row values,
- transition header + subtitle simultaneously.
"""
from qa_v2 import *


class PositionTimeGraphLessonV3(PositionTimeGraphLessonV2):
    """Final senior QA revision after rendered-frame inspection."""

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
        if self.header_group is None and self.subtitle_group is None:
            self.header_group = new_header
            self.subtitle_group = subtitle_text
            self.add(new_header, subtitle_text)
        elif self.header_group is not None and self.subtitle_group is not None:
            old_header = self.header_group
            old_subtitle = self.subtitle_group
            self.header_group = new_header
            self.subtitle_group = subtitle_text
            # One synchronized transition avoids old-subtitle/new-header mismatch.
            self.play(
                ReplacementTransform(old_header, new_header),
                ReplacementTransform(old_subtitle, subtitle_text),
                run_time=RUN_QUICK,
            )
        else:
            if self.header_group is not None:
                self.remove(self.header_group)
            if self.subtitle_group is not None:
                self.remove(self.subtitle_group)
            self.header_group = new_header
            self.subtitle_group = subtitle_text
            self.add(new_header, subtitle_text)

    def motion_to_data(self):
        self.set_header(
            2, "MEASURE POSITION BEFORE DRAWING THE GRAPH",
            "Watch the object, read the clock, then register the matching time and position as one data pair.",
        )

        # LEFT: large physical motion representation.
        track = NumberLine(
            x_range=[0, 7, 1], length=7.05,
            color=BLACK_LINE, stroke_width=3.0,
            include_numbers=False, include_tip=False,
        ).move_to(LEFT * 3.30 + DOWN * 0.72)
        track_numbers = VGroup(*[
            self.math(str(n), 28).next_to(track.n2p(n), DOWN, buff=0.13)
            for n in range(8)
        ])
        track_label = self.text("POSITION TRACK   x (m)", 31, BOLD).next_to(track, UP, buff=0.34)

        mover = Dot(track.n2p(0), radius=0.15, color=BLACK_LINE)
        mover_label = self.text("object", 25, BOLD).next_to(mover, UP, buff=0.14)

        # Explicit READ card.
        measure_box = RoundedRectangle(
            width=6.45, height=1.52, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.2,
            fill_color=PAPER_GRAY, fill_opacity=1,
        ).move_to(LEFT * 3.30 + UP * 1.22)
        step1 = self.text("1  OBSERVE + READ", 26, BOLD)
        step1.next_to(measure_box, UP, buff=0.12).align_to(measure_box, LEFT)
        measure_title = self.text("CURRENT MEASUREMENT", 24, BOLD)
        time_value = self.math(r"t=0\;\mathrm{s}", 43)
        pos_value = self.math(r"x=0\;\mathrm{m}", 43)
        measure_values = VGroup(time_value, pos_value).arrange(RIGHT, buff=0.90)
        measure_content = VGroup(measure_title, measure_values).arrange(DOWN, buff=0.15).move_to(measure_box)
        measurement = VGroup(measure_box, measure_content)

        # RIGHT: custom table with guaranteed safe margins and larger row values.
        table_box = RoundedRectangle(
            width=5.25, height=5.45, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 4.25 + DOWN * 0.54)
        table_box.set_z_index(-5)
        step2 = self.text("2  RECORD", 26, BOLD)
        step2.next_to(table_box, UP, buff=0.12).align_to(table_box, LEFT)

        tx = table_box.get_center()[0]
        left_x = tx - 1.30
        right_x = tx + 1.26
        header_y = 0.92
        left_header = self.text("time  t (s)", 29, BOLD).move_to([left_x, header_y, 0])
        right_header = self.text("position  x (m)", 29, BOLD).move_to([right_x, header_y, 0])
        self.fit(left_header, 2.15, 0.52)
        self.fit(right_header, 2.28, 0.52)
        header = VGroup(left_header, right_header)
        header_rule = Line(
            [table_box.get_left()[0] + 0.28, 0.57, 0],
            [table_box.get_right()[0] - 0.28, 0.57, 0],
            color=LIGHT_GRAY, stroke_width=2,
        )
        divider = Line(
            [tx, 1.25, 0], [tx, -2.42, 0],
            color=VERY_LIGHT_GRAY, stroke_width=1.2,
        )

        row_y = [0.24 - 0.36 * i for i in range(len(TIMES))]
        rows = VGroup(*[
            VGroup(
                self.math(str(int(t)), 34).move_to([left_x, y, 0]),
                self.math(str(int(x)), 34).move_to([right_x, y, 0]),
            )
            for (t, x), y in zip(zip(TIMES, POSITIONS), row_y)
        ])

        self.play(
            FadeIn(step1), FadeIn(measurement),
            Create(track), FadeIn(track_numbers), FadeIn(track_label),
            FadeIn(mover), FadeIn(mover_label),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_READ)
        self.play(
            FadeIn(table_box), FadeIn(step2), FadeIn(header),
            Create(header_rule), Create(divider),
            run_time=RUN_NORMAL,
        )

        previous_highlight = None
        current_time = time_value
        current_pos = pos_value
        for idx, (t, x) in enumerate(zip(TIMES, POSITIONS)):
            target = track.n2p(x)
            new_time = self.math(rf"t={int(t)}\;\mathrm{{s}}", 43).move_to(current_time)
            new_pos = self.math(rf"x={int(x)}\;\mathrm{{m}}", 43).move_to(current_pos)
            highlight = RoundedRectangle(
                width=4.55, height=0.34, corner_radius=0.04,
                color=MID_GRAY, stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0,
            ).move_to([tx, row_y[idx], 0])
            highlight.set_z_index(-1)

            anims = [
                mover.animate.move_to(target),
                mover_label.animate.next_to(target, UP, buff=0.14),
                ReplacementTransform(current_time, new_time),
                ReplacementTransform(current_pos, new_pos),
            ]
            if previous_highlight is not None:
                anims.append(FadeOut(previous_highlight))
            self.play(*anims, run_time=0.92)
            current_time, current_pos = new_time, new_pos

            self.play(FadeIn(highlight), FadeIn(rows[idx], shift=UP * 0.05), run_time=0.60)
            previous_highlight = highlight
            self.wait(0.66)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()
