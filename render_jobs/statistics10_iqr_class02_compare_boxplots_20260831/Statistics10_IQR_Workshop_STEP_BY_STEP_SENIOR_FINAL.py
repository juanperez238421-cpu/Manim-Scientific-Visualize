#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 IQR Workshop — Senior QA V2.

Source-level QA pass over the validated senior workshop. This version fixes the
remaining visual/animation defects found by full-timeline review of the PQH render:

1. Persistent headers no longer morph glyph-by-glyph between sections. A clean
   fade-out/fade-in transition prevents transient broken/cut title lettering.
2. Problem 4 uses collision-free annotation lanes for Q1, median, Q3, regular
   extremes and the outlier. Pairwise bounding-box guards fail the render if the
   labels overlap again.
3. Problems 5 and 6 directly focus the graph marks while each numbered reading
   step is revealed, so the animation explains what the formula refers to.
4. The final summary explicitly separates the SOLVE routine from the READ routine.

Target: ManimCE 0.20.1; literal -pql gate then literal -pqh production render.
"""

from __future__ import annotations

from itertools import combinations

from manim import *

from Statistics10_IQR_Workshop_STEP_BY_STEP_FINAL import (
    Statistics10IQRWorkshopStepByStepFinal,
    GROUP_A,
    GROUP_B,
    P3,
    modified_box_summary,
)
from jp_classroom_style import *


class Statistics10IQRWorkshopStepByStepSeniorFinal(Statistics10IQRWorkshopStepByStepFinal):
    """Projector-safe senior QA V2 pass over the complete workshop."""

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        """Render a clean persistent header transition without text morph artifacts."""
        number_box = RoundedRectangle(
            width=0.72,
            height=0.52,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)

        title_text = self.text(title, 34, BOLD)
        available_title_width = SAFE_WIDTH - number_box.width - 0.38
        self.fit(title_text, available_title_width, 0.56)
        title_row = VGroup(VGroup(number_box, number_text), title_text)
        title_row.arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 96:
            midpoint = len(words) // 2
            best = midpoint
            best_gap = 10**9
            for index in range(max(1, midpoint - 5), min(len(words), midpoint + 6)):
                gap = abs(len(" ".join(words[:index])) - len(" ".join(words[index:])))
                if gap < best_gap:
                    best = index
                    best_gap = gap
            subtitle_lines = [" ".join(words[:best]), " ".join(words[best:])]
            subtitle_text = VGroup(*[self.text(line, 20) for line in subtitle_lines])
            subtitle_text.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_text = self.text(subtitle, 21)

        self.fit(subtitle_text, 14.25, 0.70)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)
        new_header = VGroup(title_row, rule)

        old_header = self.header_group
        old_subtitle = self.subtitle_group
        self.header_group = new_header
        self.subtitle_group = subtitle_text

        if old_header is None and old_subtitle is None:
            self.add(new_header, subtitle_text)
            return

        outgoing = VGroup(*[m for m in (old_header, old_subtitle) if m is not None])
        if len(outgoing) > 0:
            self.play(FadeOut(outgoing), run_time=RUN_QUICK * 0.70)
        self.play(FadeIn(new_header), FadeIn(subtitle_text), run_time=RUN_QUICK * 0.70)

    def assert_no_overlap(self, mobs: list[Mobject], label: str, padding: float = 0.04) -> None:
        """Fail the render if any annotation bounding boxes overlap."""
        for (i, a), (j, b) in combinations(enumerate(mobs), 2):
            a_left, a_right = a.get_left()[0] - padding, a.get_right()[0] + padding
            a_bottom, a_top = a.get_bottom()[1] - padding, a.get_top()[1] + padding
            b_left, b_right = b.get_left()[0] - padding, b.get_right()[0] + padding
            b_bottom, b_top = b.get_bottom()[1] - padding, b.get_top()[1] + padding
            intersects = (
                a_left < b_right
                and a_right > b_left
                and a_bottom < b_top
                and a_top > b_bottom
            )
            if intersects:
                raise ValueError(f"{label}: annotation {i} overlaps annotation {j}")

    def problem4_construct_boxplot(self) -> None:
        self.set_header(
            5,
            "PROBLEM 4 — CONSTRUCT THE MODIFIED BOXPLOT",
            "Build the graph in a fixed order so every mark has a statistical meaning.",
        )
        s = modified_box_summary(P3)
        axis = self.axis(0, 30, 5, y=-2.45, length=12.2)
        p = axis.n2p
        y = -0.55

        instruction = self.text(
            "Use: Q1=5.5, median=7.5, Q3=9.5, regular min=3, regular max=10, outlier=24",
            24,
            BOLD,
        )
        self.fit(instruction, 13.8, 0.46)
        instruction.move_to(UP * 1.75)
        self.play(FadeIn(instruction), run_time=RUN_NORMAL)

        badge1 = self.step_badge(1, "DRAW SCALE").move_to([-6.35, 0.95, 0])
        self.play(FadeIn(badge1), Create(axis), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        x1, x2, x3 = p(s.q1)[0], p(s.q2)[0], p(s.q3)[0]
        box = Rectangle(
            width=x3 - x1,
            height=0.72,
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.40,
        ).move_to([(x1 + x3) / 2, y, 0])
        badge2 = self.step_badge(2, "BOX Q1→Q3").move_to([-6.35, 0.28, 0])
        self.play(FadeIn(badge2), Create(box), run_time=RUN_NORMAL)
        self.play(Circumscribe(box, color=BLACK_LINE, buff=0.08), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        median_line = Line([x2, y - 0.36, 0], [x2, y + 0.36, 0], color=BLACK_LINE, stroke_width=4)
        badge3 = self.step_badge(3, "MEDIAN").move_to([-6.35, -0.39, 0])
        self.play(FadeIn(badge3), Create(median_line), run_time=RUN_NORMAL)
        self.play(Circumscribe(median_line, color=BLACK_LINE, buff=0.10), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        lw, uw = p(s.lower_whisker)[0], p(s.upper_whisker)[0]
        whiskers = VGroup(
            Line([lw, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=3),
            Line([x3, y, 0], [uw, y, 0], color=BLACK_LINE, stroke_width=3),
            Line([lw, y - 0.22, 0], [lw, y + 0.22, 0], color=BLACK_LINE, stroke_width=3),
            Line([uw, y - 0.22, 0], [uw, y + 0.22, 0], color=BLACK_LINE, stroke_width=3),
        )
        badge4 = self.step_badge(4, "WHISKERS").move_to([-6.35, -1.06, 0])
        self.play(FadeIn(badge4), Create(whiskers), run_time=RUN_NORMAL)
        self.play(Circumscribe(whiskers, color=BLACK_LINE, buff=0.10), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        out = Circle(radius=0.11, stroke_color=BLACK_LINE, stroke_width=2.6).move_to([p(24)[0], y, 0])
        badge5 = self.step_badge(5, "OUTLIER").move_to([-6.35, -1.73, 0])
        self.play(FadeIn(badge5), Create(out), run_time=RUN_NORMAL)
        self.play(Circumscribe(out, color=BLACK_LINE, buff=0.12), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        q1_label = self.math(r"Q_1=5.5", 23).move_to([x1 - 0.58, 0.43, 0])
        q2_label = self.math(r"Q_2=7.5", 23).move_to([x2, 0.93, 0])
        q3_label = self.math(r"Q_3=9.5", 23).move_to([x3 + 0.72, 0.43, 0])
        min_label = self.math(r"3", 23).move_to([lw, -1.08, 0])
        max_label = self.math(r"10", 23).move_to([uw, -1.08, 0])
        outlier_label = self.text("24 = outlier", 22, BOLD).move_to([p(24)[0], 0.32, 0])
        label_mobs = [q1_label, q2_label, q3_label, min_label, max_label, outlier_label]
        self.assert_no_overlap(label_mobs, "problem 4 collision-free annotation lanes", padding=0.03)

        guides = VGroup(
            Line(q1_label.get_bottom(), [x1, y + 0.38, 0], color=BLACK_LINE, stroke_width=1.4),
            Line(q2_label.get_bottom(), [x2, y + 0.38, 0], color=BLACK_LINE, stroke_width=1.4),
            Line(q3_label.get_bottom(), [x3, y + 0.38, 0], color=BLACK_LINE, stroke_width=1.4),
            Line(min_label.get_top(), [lw, y - 0.24, 0], color=BLACK_LINE, stroke_width=1.3),
            Line(max_label.get_top(), [uw, y - 0.24, 0], color=BLACK_LINE, stroke_width=1.3),
            Line(outlier_label.get_bottom(), [p(24)[0], y + 0.13, 0], color=BLACK_LINE, stroke_width=1.3),
        )
        labels = VGroup(*label_mobs)
        badge6 = self.step_badge(6, "LABEL + CHECK").move_to([-6.35, -2.40, 0])
        construction = VGroup(
            axis, box, median_line, whiskers, out, labels, guides,
            badge1, badge2, badge3, badge4, badge5, badge6,
        )
        self.assert_content_safe(construction, "constructed boxplot V2")
        self.play(FadeIn(badge6), Create(guides), FadeIn(labels), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem5_read_boxplot(self) -> None:
        self.set_header(
            6,
            "PROBLEM 5 — READ A BOXPLOT",
            "Read the marks in a consistent order: center, middle spread, regular extremes, then outliers.",
        )
        s = modified_box_summary(P3)
        axis = self.axis(0, 30, 5, y=-2.45, length=12.1)
        plot = self.boxplot(axis, s, y=0.10)
        self.play(Create(axis), Create(plot), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        rows = [
            self.step_row(1, "CENTER", self.math(r"\text{Median}=Q_2=7.5", 31), y=1.72),
            self.step_row(2, "MIDDLE 50%", self.math(r"IQR=Q_3-Q_1=9.5-5.5=4", 30), y=1.02),
            self.step_row(3, "REGULAR RANGE", self.math(r"3\;\text{ to }\;10", 31), y=-0.83),
            self.step_row(4, "OUTLIER", self.math(r"24\;\text{ is plotted separately}", 30), y=-1.53),
        ]
        focus_targets = [
            plot[5],
            plot[4],
            VGroup(plot[0], plot[1], plot[2], plot[3]),
            plot[6],
        ]
        for row, target in zip(rows, focus_targets):
            self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=RUN_NORMAL)
            self.play(Circumscribe(target, color=BLACK_LINE, buff=0.10), run_time=RUN_QUICK)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem6_compare_groups(self) -> None:
        self.set_header(
            7,
            "PROBLEM 6 — COMPARE TWO GROUPS",
            "Use the same numerical scale. Compare center first, then IQR, then whiskers and outliers.",
        )
        a, b = modified_box_summary(GROUP_A), modified_box_summary(GROUP_B)
        axis = self.axis(35, 80, 5, y=-2.62, length=12.5)
        pa = self.boxplot(axis, a, y=0.30, label="A")
        pb = self.boxplot(axis, b, y=-0.90, label="B")
        self.play(Create(axis), Create(pa), Create(pb), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        center = self.step_row(
            1,
            "CENTER",
            self.math(
                r"Q_{2,A}=51\quad\text{vs}\quad Q_{2,B}=54.5"
                r"\;\Rightarrow\;B\text{ has the higher center}",
                27,
            ),
            y=1.88,
        )
        spread = self.step_row(
            2,
            "IQR",
            self.math(
                r"IQR_A=11.5\quad\text{vs}\quad IQR_B=5"
                r"\;\Rightarrow\;B\text{ is more tightly clustered}",
                26,
            ),
            y=1.18,
        )
        outlier = self.step_row(
            3,
            "OUTLIER",
            self.math(r"75>UF_B=65\;\Rightarrow\;75\text{ is a Group B outlier}", 27),
            y=-1.78,
        )

        comparison_steps = [
            (center, VGroup(pa[5], pb[5])),
            (spread, VGroup(pa[4], pb[4])),
            (outlier, pb[6]),
        ]
        for row, target in comparison_steps:
            self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=RUN_NORMAL)
            self.play(Circumscribe(target, color=BLACK_LINE, buff=0.10), run_time=RUN_QUICK)
            self.wait(PAUSE_EXPLAIN)
        self.wait(PAUSE_READ)

        self.play(FadeOut(VGroup(center, spread, outlier, axis, pa, pb)), run_time=RUN_QUICK)
        conclusion = self.note_panel(
            "Statistical conclusion",
            [
                "Group B has the higher typical value.",
                "Its middle 50% is more tightly clustered.",
                "It also contains one high outlier: 75.",
            ],
            width=8.9,
            body_size=22,
        )
        conclusion.move_to([0, 0.25, 0])
        self.assert_content_safe(conclusion, "comparison conclusion panel")
        self.play(FadeIn(conclusion, shift=UP * 0.05), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def independent_practice(self) -> None:
        self.set_header(
            8,
            "YOUR TURN — INDEPENDENT PRACTICE",
            "Pause the video. Solve each prompt using the numbered routine before checking the answer key.",
        )
        prompts = VGroup(
            self.note_panel(
                "A · Quartiles + IQR",
                ["Data: 6, 8, 9, 10, 12, 13, 15, 17", "Find Q1, Q2, Q3 and IQR."],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "B · Outlier test",
                ["Data: 5, 6, 7, 9, 10, 11, 12, 30", "Find the fences and classify 30."],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "C · Interpretation",
                ["Which group is more consistent?", "A: IQR = 11.5   B: IQR = 5"],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "D · Explain",
                ["Why does a whisker stop at 10", "while 24 is still in the dataset?"],
                width=6.4,
                body_size=22,
            ),
        )
        prompts.arrange_in_grid(rows=2, cols=2, buff=(0.42, 0.34))
        self.fit(prompts, 13.5, 4.65)
        prompts.move_to(DOWN * 0.38)
        self.assert_content_safe(prompts, "practice prompts")
        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.04) for p in prompts], lag_ratio=0.10),
            run_time=RUN_SLOW,
        )
        pause = self.text("PAUSE HERE · show all calculations in your notebook", 25, BOLD)
        self.fit(pause, 11.8, 0.44)
        pause.move_to([0, -3.00, 0])
        self.assert_content_safe(pause, "practice pause instruction")
        self.play(FadeIn(pause), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL * 1.55)
        self.clear_stage()

    def final_summary(self) -> None:
        self.set_header(
            11,
            "THE ROUTINE TO REMEMBER",
            "Use this exact sequence whenever you solve an IQR / modified-boxplot problem.",
        )
        routine = VGroup(
            self.step_badge(1, "ORDER DATA", width=2.55),
            self.step_badge(2, "FIND Q1,Q2,Q3", width=2.55),
            self.step_badge(3, "CALCULATE IQR", width=2.55),
            self.step_badge(4, "FIND FENCES", width=2.55),
            self.step_badge(5, "CLASSIFY", width=2.55),
            self.step_badge(6, "DRAW / INTERPRET", width=2.55),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.48, 0.30))
        routine.move_to([0, -0.05, 0])
        self.assert_content_safe(routine, "final routine")
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.04) for r in routine], lag_ratio=0.10),
            run_time=RUN_SLOW,
        )

        solve_line = self.text(
            "SOLVE: order → quartiles → IQR → fences → classify → draw",
            25,
            BOLD,
        )
        read_line = self.text(
            "READ: center → middle 50% → whiskers → outliers → conclusion",
            24,
            BOLD,
        )
        self.fit(solve_line, 11.8, 0.44)
        self.fit(read_line, 11.8, 0.44)
        solve_line.move_to([0, -2.35, 0])
        read_line.move_to([0, -2.83, 0])
        summary_lines = VGroup(solve_line, read_line)
        self.assert_content_safe(summary_lines, "final summary lines")
        self.play(FadeIn(solve_line), run_time=RUN_NORMAL)
        self.play(FadeIn(read_line), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)


if __name__ == "__main__":
    pass
