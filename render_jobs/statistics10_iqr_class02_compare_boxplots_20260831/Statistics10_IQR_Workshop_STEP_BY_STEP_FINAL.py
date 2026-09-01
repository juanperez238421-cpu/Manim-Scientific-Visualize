#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 — IQR & Box Plots — Workshop: explicit step-by-step practice.

Source-level continuation of the Class 2 Senior-QA V6 lesson.
Design goal: a notebook-friendly workshop video in which every worked exercise is
resolved through clearly numbered steps before a short independent-practice block.

Quartile convention (same as Class 1 / Class 2):
- odd n: exclude the overall median from lower and upper halves;
- even n: split the ordered data into two equal halves;
- Q1 and Q3 are the medians of those halves.

Target: Manim Community Edition 0.20.1, -pqh, 1920x1080, 30 fps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from manim import *

from jp_classroom_style import *


@dataclass(frozen=True)
class BoxSummary:
    data: tuple[float, ...]
    q1: float
    q2: float
    q3: float
    iqr: float
    lf: float
    uf: float
    lower_whisker: float
    upper_whisker: float
    outliers: tuple[float, ...]


def _median(values: Sequence[float]) -> float:
    values = sorted(float(x) for x in values)
    if not values:
        raise ValueError("median requires data")
    n = len(values)
    if n % 2:
        return values[n // 2]
    return (values[n // 2 - 1] + values[n // 2]) / 2.0


def quartiles_class1(values: Sequence[float]) -> tuple[float, float, float]:
    values = sorted(float(x) for x in values)
    if len(values) < 4:
        raise ValueError("at least four observations are required")
    n = len(values)
    q2 = _median(values)
    if n % 2:
        lower = values[: n // 2]
        upper = values[n // 2 + 1 :]
    else:
        lower = values[: n // 2]
        upper = values[n // 2 :]
    return _median(lower), q2, _median(upper)


def modified_box_summary(values: Sequence[float]) -> BoxSummary:
    data = tuple(sorted(float(x) for x in values))
    q1, q2, q3 = quartiles_class1(data)
    iqr = q3 - q1
    lf = q1 - 1.5 * iqr
    uf = q3 + 1.5 * iqr
    regular = tuple(x for x in data if lf <= x <= uf)
    outliers = tuple(x for x in data if x < lf or x > uf)
    return BoxSummary(
        data=data,
        q1=q1,
        q2=q2,
        q3=q3,
        iqr=iqr,
        lf=lf,
        uf=uf,
        lower_whisker=min(regular),
        upper_whisker=max(regular),
        outliers=outliers,
    )


P1 = (4, 7, 8, 9, 10, 12, 13, 15)
P2 = P1
P3 = (3, 5, 6, 7, 8, 9, 10, 24)
GROUP_A = (40, 44, 47, 50, 52, 55, 59, 63)
GROUP_B = (49, 52, 53, 54, 55, 57, 58, 75)
PRACTICE_1 = (6, 8, 9, 10, 12, 13, 15, 17)
PRACTICE_2 = (5, 6, 7, 9, 10, 11, 12, 30)


class Statistics10IQRWorkshopStepByStepFinal(JPMathClassroomScene):
    """Explicitly numbered IQR / modified-boxplot workshop."""

    def validate_lesson_data(self) -> None:
        p1 = modified_box_summary(P1)
        assert (p1.q1, p1.q2, p1.q3) == (7.5, 9.5, 12.5)
        assert p1.iqr == 5.0 and p1.lf == 0.0 and p1.uf == 20.0
        assert p1.outliers == ()

        p3 = modified_box_summary(P3)
        assert (p3.q1, p3.q2, p3.q3) == (5.5, 7.5, 9.5)
        assert p3.iqr == 4.0 and p3.lf == -0.5 and p3.uf == 15.5
        assert p3.lower_whisker == 3.0 and p3.upper_whisker == 10.0
        assert p3.outliers == (24.0,)

        a = modified_box_summary(GROUP_A)
        b = modified_box_summary(GROUP_B)
        assert (a.q1, a.q2, a.q3, a.iqr) == (45.5, 51.0, 57.0, 11.5)
        assert a.outliers == ()
        assert (b.q1, b.q2, b.q3, b.iqr) == (52.5, 54.5, 57.5, 5.0)
        assert b.uf == 65.0 and b.upper_whisker == 58.0 and b.outliers == (75.0,)

        pr1 = modified_box_summary(PRACTICE_1)
        assert (pr1.q1, pr1.q2, pr1.q3, pr1.iqr) == (8.5, 11.0, 14.0, 5.5)
        assert pr1.outliers == ()
        pr2 = modified_box_summary(PRACTICE_2)
        assert (pr2.q1, pr2.q2, pr2.q3, pr2.iqr) == (6.5, 9.5, 11.5, 5.0)
        assert pr2.uf == 19.0 and pr2.outliers == (30.0,)

    def fmt(self, value: float) -> str:
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.1f}"

    def step_badge(self, number: int, label: str, *, width: float = 2.18) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=0.58,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        n = self.text(f"STEP {number}", 21, BOLD)
        lab = self.text(label, 18, BOLD)
        self.fit(lab, width - 0.20, 0.24)
        group = VGroup(n, lab).arrange(DOWN, buff=0.02).move_to(box)
        return VGroup(box, group)

    def step_row(self, number: int, label: str, content: Mobject, *, y: float) -> VGroup:
        badge = self.step_badge(number, label).move_to([-6.15, y, 0])
        self.fit(content, 10.8, 0.75)
        content.move_to([0.65, y, 0]).align_to(badge, UP)
        row = VGroup(badge, content)
        self.assert_content_safe(row, f"step row {number}: {label}")
        return row

    def data_strip(self, values: Sequence[float], *, card_width: float = 0.84) -> VGroup:
        cards = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=card_width,
                height=0.62,
                corner_radius=0.07,
                stroke_color=BLACK_LINE,
                stroke_width=1.6,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            )
            num = self.math(self.fmt(value), 27).move_to(box)
            cards.add(VGroup(box, num))
        cards.arrange(RIGHT, buff=0.08)
        return cards

    def axis(self, x_min: float, x_max: float, step: float, *, y: float, length: float = 12.2) -> NumberLine:
        axis = NumberLine(
            x_range=[x_min, x_max, step],
            length=length,
            include_numbers=True,
            font_size=22,
            include_tip=False,
            color=BLACK_LINE,
            stroke_width=2.0,
            decimal_number_config={"num_decimal_places": 0},
        )
        axis.set_color(BLACK_LINE)
        axis.move_to([0, y, 0])
        return axis

    def boxplot(self, axis: NumberLine, s: BoxSummary, *, y: float, label: str = "") -> VGroup:
        p = axis.n2p
        x1, x2, x3 = p(s.q1)[0], p(s.q2)[0], p(s.q3)[0]
        lw, uw = p(s.lower_whisker)[0], p(s.upper_whisker)[0]
        h = 0.62
        box = Rectangle(
            width=max(0.05, x3 - x1),
            height=h,
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.38,
        ).move_to([(x1 + x3) / 2, y, 0])
        med = Line([x2, y - h / 2, 0], [x2, y + h / 2, 0], color=BLACK_LINE, stroke_width=4)
        whisk_l = Line([lw, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=3)
        whisk_r = Line([x3, y, 0], [uw, y, 0], color=BLACK_LINE, stroke_width=3)
        cap_l = Line([lw, y - 0.21, 0], [lw, y + 0.21, 0], color=BLACK_LINE, stroke_width=3)
        cap_r = Line([uw, y - 0.21, 0], [uw, y + 0.21, 0], color=BLACK_LINE, stroke_width=3)
        out = VGroup()
        for value in s.outliers:
            out.add(Circle(radius=0.10, stroke_color=BLACK_LINE, stroke_width=2.4).move_to([p(value)[0], y, 0]))
        parts = VGroup(whisk_l, whisk_r, cap_l, cap_r, box, med, out)
        if label:
            lab = self.text(label, 21, BOLD).move_to([axis.get_left()[0] - 0.64, y, 0])
            parts.add(lab)
        return parts

    def problem_card(self, number: int, title: str, prompt: str) -> VGroup:
        tag = RoundedRectangle(
            width=1.18, height=0.54, corner_radius=0.08,
            stroke_color=BLACK_LINE, stroke_width=2, fill_color=WHITE_FILL, fill_opacity=1,
        )
        tag_txt = self.text(f"P{number}", 23, BOLD).move_to(tag)
        title_mob = self.text(title, 27, BOLD)
        prompt_mob = self.text(prompt, 22)
        self.fit(prompt_mob, 12.4, 0.75)
        heading = VGroup(VGroup(tag, tag_txt), title_mob).arrange(RIGHT, buff=0.22)
        content = VGroup(heading, prompt_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        box = RoundedRectangle(
            width=14.1,
            height=max(1.35, content.height + 0.45),
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, content)

    def reveal_rows(self, rows: Sequence[VGroup], *, pause: float = PAUSE_READ) -> None:
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=RUN_NORMAL)
            self.wait(pause)

    def construct(self) -> None:
        self.opening()
        self.route_map()
        self.problem1_quartiles()
        self.problem2_iqr_fences()
        self.problem3_outlier()
        self.problem4_construct_boxplot()
        self.problem5_read_boxplot()
        self.problem6_compare_groups()
        self.independent_practice()
        self.answer_key()
        self.exit_ticket()
        self.final_summary()

    def opening(self) -> None:
        title = self.text("IQR & BOX PLOTS — WORKSHOP", 49, BOLD)
        subtitle = self.text("Explicit numbered solutions · copy each step into your notebook", 28)
        line = Line(LEFT * 5.6, RIGHT * 5.6, color=BLACK_LINE, stroke_width=2)
        objective = self.text("Goal: calculate, construct, read and compare modified boxplots.", 25, BOLD)
        group = VGroup(title, subtitle, line, objective).arrange(DOWN, buff=0.28)
        self.fit(group, 14.2, 4.8)
        group.move_to(ORIGIN)
        self.assert_within_frame(group, "opening")
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), Create(line), run_time=RUN_NORMAL)
        self.play(FadeIn(objective), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def route_map(self) -> None:
        self.set_header(1, "WORKSHOP ROUTE", "Every exercise follows the same analysis routine before we interpret the graph.")
        labels = [
            ("1", "ORDER + QUARTILES"),
            ("2", "IQR + FENCES"),
            ("3", "OUTLIERS"),
            ("4", "BOXPLOT"),
            ("5", "READ"),
            ("6", "COMPARE"),
        ]
        cards = VGroup()
        for n, txt in labels:
            card = RoundedRectangle(
                width=4.1, height=1.24, corner_radius=0.12,
                stroke_color=BLACK_LINE, stroke_width=1.8,
                fill_color=WHITE_FILL, fill_opacity=1,
            )
            num = self.text(n, 29, BOLD)
            lab = self.text(txt, 23, BOLD)
            content = VGroup(num, lab).arrange(RIGHT, buff=0.22).move_to(card)
            cards.add(VGroup(card, content))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.40, 0.28))
        self.fit(cards, 10.0, 4.4)
        cards.move_to(DOWN * 0.65)
        self.assert_content_safe(cards, "route cards")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in cards], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def problem1_quartiles(self) -> None:
        self.set_header(2, "PROBLEM 1 — FIND Q1, Q2 AND Q3", "Start by organizing the data. Quartiles are medians of the correct halves, not guesses from position.")
        card = self.problem_card(1, "Quartiles", "For 4, 7, 8, 9, 10, 12, 13, 15, determine Q1, Q2 and Q3.")
        card.scale(0.92).move_to(UP * 1.72)
        strip = self.data_strip(P1).move_to(UP * 0.63)
        self.assert_content_safe(VGroup(card, strip), "problem 1 prompt")
        self.play(FadeIn(card), FadeIn(strip), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)

        row1 = self.step_row(1, "ORDER", self.text("The data are already in ascending order.", 23), y=-0.28)
        row2 = self.step_row(2, "SPLIT", self.math(r"[4,7,8,9]\quad | \quad [10,12,13,15]", 31), y=-1.08)
        row3 = self.step_row(3, "MEDIANS", self.math(r"Q_1=\frac{7+8}{2}=7.5\quad Q_2=\frac{9+10}{2}=9.5\quad Q_3=\frac{12+13}{2}=12.5", 30), y=-1.88)
        row4 = self.step_row(4, "CHECK", self.math(r"Q_1<Q_2<Q_3\;\Rightarrow\;7.5<9.5<12.5", 29), y=-2.68)
        self.reveal_rows([row1, row2, row3, row4], pause=PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem2_iqr_fences(self) -> None:
        self.set_header(3, "PROBLEM 2 — CALCULATE IQR AND FENCES", "Use the quartiles from Problem 1. The fences classify possible outliers; they are not whisker endpoints.")
        top = self.math(r"Q_1=7.5\qquad Q_2=9.5\qquad Q_3=12.5", 35).move_to(UP * 1.68)
        self.play(FadeIn(top), run_time=RUN_NORMAL)

        row1 = self.step_row(1, "IQR", self.math(r"IQR=Q_3-Q_1=12.5-7.5=5", 34), y=0.72)
        row2 = self.step_row(2, "LOWER FENCE", self.math(r"LF=Q_1-1.5(IQR)=7.5-1.5(5)=0", 31), y=-0.18)
        row3 = self.step_row(3, "UPPER FENCE", self.math(r"UF=Q_3+1.5(IQR)=12.5+1.5(5)=20", 31), y=-1.08)
        row4 = self.step_row(4, "CLASSIFY", self.math(r"0\le x\le20\;\text{ for every datum}\;\Rightarrow\;\text{no outliers}", 30), y=-1.98)
        self.reveal_rows([row1, row2, row3, row4], pause=PAUSE_READ)
        conclusion = self.note_panel("Conclusion", ["All observations are regular.", "The whiskers can reach the minimum and maximum."], width=7.4, body_size=22)
        conclusion.move_to([2.5, -3.00, 0])
        self.assert_content_safe(conclusion, "problem 2 conclusion")
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem3_outlier(self) -> None:
        self.set_header(4, "PROBLEM 3 — DETECT THE OUTLIER", "A value becomes an outlier only after it is compared with the fences.")
        card = self.problem_card(3, "Outlier test", "Analyze 3, 5, 6, 7, 8, 9, 10, 24. Is 24 a regular value or an outlier?")
        card.scale(0.90).move_to(UP * 1.65)
        self.play(FadeIn(card), run_time=RUN_NORMAL)

        row1 = self.step_row(1, "QUARTILES", self.math(r"Q_1=5.5\qquad Q_2=7.5\qquad Q_3=9.5", 31), y=0.52)
        row2 = self.step_row(2, "IQR", self.math(r"IQR=9.5-5.5=4", 33), y=-0.30)
        row3 = self.step_row(3, "FENCES", self.math(r"LF=5.5-1.5(4)=-0.5\qquad UF=9.5+1.5(4)=15.5", 29), y=-1.12)
        row4 = self.step_row(4, "TEST 24", self.math(r"24>15.5\;\Rightarrow\;\boxed{24\text{ is an outlier}}", 31), y=-1.94)
        row5 = self.step_row(5, "WHISKERS", self.math(r"\text{lower whisker}=3\qquad\text{upper whisker}=10", 28), y=-2.76)
        self.reveal_rows([row1, row2, row3, row4, row5], pause=PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem4_construct_boxplot(self) -> None:
        self.set_header(5, "PROBLEM 4 — CONSTRUCT THE MODIFIED BOXPLOT", "Build the graph in a fixed order so every mark has a statistical meaning.")
        s = modified_box_summary(P3)
        axis = self.axis(0, 30, 5, y=-2.45, length=12.2)
        p = axis.n2p
        y = -0.55

        instruction = self.text("Use: Q1=5.5, median=7.5, Q3=9.5, regular min=3, regular max=10, outlier=24", 24, BOLD)
        self.fit(instruction, 13.8, 0.46)
        instruction.move_to(UP * 1.75)
        self.play(FadeIn(instruction), run_time=RUN_NORMAL)

        badge1 = self.step_badge(1, "DRAW SCALE").move_to([-6.35, 0.95, 0])
        self.play(FadeIn(badge1), Create(axis), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        x1, x2, x3 = p(s.q1)[0], p(s.q2)[0], p(s.q3)[0]
        box = Rectangle(width=x3-x1, height=0.72, stroke_color=BLACK_LINE, stroke_width=3, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.40).move_to([(x1+x3)/2, y, 0])
        badge2 = self.step_badge(2, "BOX Q1→Q3").move_to([-6.35, 0.28, 0])
        self.play(FadeIn(badge2), Create(box), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        median_line = Line([x2, y-0.36, 0], [x2, y+0.36, 0], color=BLACK_LINE, stroke_width=4)
        badge3 = self.step_badge(3, "MEDIAN").move_to([-6.35, -0.39, 0])
        self.play(FadeIn(badge3), Create(median_line), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        lw, uw = p(s.lower_whisker)[0], p(s.upper_whisker)[0]
        whiskers = VGroup(
            Line([lw,y,0],[x1,y,0],color=BLACK_LINE,stroke_width=3),
            Line([x3,y,0],[uw,y,0],color=BLACK_LINE,stroke_width=3),
            Line([lw,y-0.22,0],[lw,y+0.22,0],color=BLACK_LINE,stroke_width=3),
            Line([uw,y-0.22,0],[uw,y+0.22,0],color=BLACK_LINE,stroke_width=3),
        )
        badge4 = self.step_badge(4, "WHISKERS").move_to([-6.35, -1.06, 0])
        self.play(FadeIn(badge4), Create(whiskers), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        out = Circle(radius=0.11, stroke_color=BLACK_LINE, stroke_width=2.6).move_to([p(24)[0], y, 0])
        badge5 = self.step_badge(5, "OUTLIER").move_to([-6.35, -1.73, 0])
        self.play(FadeIn(badge5), Create(out), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        labels = VGroup(
            self.math(r"3", 24).next_to([lw,y,0], UP, buff=0.26),
            self.math(r"Q_1=5.5", 24).next_to([x1,y,0], UP, buff=0.26),
            self.math(r"Q_2=7.5", 24).next_to([x2,y,0], UP, buff=0.26),
            self.math(r"Q_3=9.5", 24).next_to([x3,y,0], UP, buff=0.26),
            self.math(r"10", 24).next_to([uw,y,0], UP, buff=0.26),
            self.text("24 outlier", 21, BOLD).next_to(out, UP, buff=0.28),
        )
        badge6 = self.step_badge(6, "LABEL + CHECK").move_to([-6.35, -2.40, 0])
        self.assert_content_safe(VGroup(axis, box, median_line, whiskers, out, labels, badge1, badge2, badge3, badge4, badge5, badge6), "constructed boxplot")
        self.play(FadeIn(badge6), FadeIn(labels), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem5_read_boxplot(self) -> None:
        self.set_header(6, "PROBLEM 5 — READ A BOXPLOT", "Read the marks in a consistent order: center, middle spread, regular extremes, then outliers.")
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
        self.reveal_rows(rows, pause=PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def problem6_compare_groups(self) -> None:
        self.set_header(7, "PROBLEM 6 — COMPARE TWO GROUPS", "Use the same numerical scale. Compare center first, then IQR, then whiskers and outliers.")
        a, b = modified_box_summary(GROUP_A), modified_box_summary(GROUP_B)
        axis = self.axis(35, 80, 5, y=-2.62, length=12.5)
        pa = self.boxplot(axis, a, y=0.30, label="A")
        pb = self.boxplot(axis, b, y=-0.90, label="B")
        self.play(Create(axis), Create(pa), Create(pb), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        center = self.step_row(1, "CENTER", self.math(r"Q_{2,A}=51\quad\text{vs}\quad Q_{2,B}=54.5\;\Rightarrow\;B\text{ has the higher center}", 27), y=1.88)
        spread = self.step_row(2, "IQR", self.math(r"IQR_A=11.5\quad\text{vs}\quad IQR_B=5\;\Rightarrow\;B\text{ is more tightly clustered}", 26), y=1.18)
        shape = self.step_row(3, "OUTLIERS", self.math(r"75>UF_B=65\;\Rightarrow\;75\text{ is a Group B outlier}", 27), y=-1.78)
        self.reveal_rows([center, spread, shape], pause=PAUSE_EXPLAIN)
        conclusion = self.text("Final comparison: Group B has a higher typical value, smaller middle spread, and one high outlier.", 24, BOLD)
        self.fit(conclusion, 13.6, 0.50)
        conclusion.to_edge(DOWN, buff=0.28)
        self.assert_content_safe(conclusion, "comparison conclusion")
        self.play(FadeIn(conclusion, shift=UP*0.05), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def independent_practice(self) -> None:
        self.set_header(8, "YOUR TURN — INDEPENDENT PRACTICE", "Pause the video. Solve each prompt using the numbered routine before checking the answer key.")
        prompts = VGroup(
            self.note_panel("A · Quartiles + IQR", ["Data: 6, 8, 9, 10, 12, 13, 15, 17", "Find Q1, Q2, Q3 and IQR."], width=6.4, body_size=22),
            self.note_panel("B · Outlier test", ["Data: 5, 6, 7, 9, 10, 11, 12, 30", "Find the fences and classify 30."], width=6.4, body_size=22),
            self.note_panel("C · Interpretation", ["Which group is more consistent?", "A: IQR = 11.5   B: IQR = 5"], width=6.4, body_size=22),
            self.note_panel("D · Explain", ["Why does a whisker stop at 10", "while 24 is still in the dataset?"], width=6.4, body_size=22),
        )
        prompts.arrange_in_grid(rows=2, cols=2, buff=(0.42,0.34))
        self.fit(prompts, 13.5, 5.0)
        prompts.move_to(DOWN * 0.55)
        self.assert_content_safe(prompts, "practice prompts")
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.04) for p in prompts], lag_ratio=0.10), run_time=RUN_SLOW)
        pause = self.text("PAUSE HERE · show all calculations in your notebook", 26, BOLD).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(pause), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL * 1.55)
        self.clear_stage()

    def answer_key(self) -> None:
        self.set_header(9, "ANSWER KEY — CHECK YOUR PROCESS", "Compare your steps, not only your final number. A correct result should come from a correct quartile split.")
        rows = VGroup(
            self.note_panel("A", ["Q1=8.5, Q2=11, Q3=14", "IQR=5.5; no outliers"], width=6.2, body_size=22),
            self.note_panel("B", ["Q1=6.5, Q2=9.5, Q3=11.5", "LF=-1, UF=19; 30 is an outlier"], width=6.2, body_size=22),
            self.note_panel("C", ["Group B is more consistent", "because its IQR is smaller."], width=6.2, body_size=22),
            self.note_panel("D", ["Whiskers end at regular extremes.", "24 is retained as a separate outlier mark."], width=6.2, body_size=22),
        )
        rows.arrange_in_grid(rows=2, cols=2, buff=(0.45,0.35))
        self.fit(rows, 13.0, 4.8)
        rows.move_to(DOWN * 0.55)
        self.assert_content_safe(rows, "answer key")
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def exit_ticket(self) -> None:
        self.set_header(10, "EXIT TICKET — ONE COMPLETE ANALYSIS", "Write the five numbered steps before the answer appears.")
        prompt = self.problem_card(7, "Exit ticket", "Data: 2, 4, 5, 7, 8, 9, 11, 25. Find Q1, Q2, Q3, IQR, fences, and classify 25.")
        prompt.scale(0.92).move_to(UP * 1.65)
        self.play(FadeIn(prompt), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL * 1.25)

        e = modified_box_summary((2,4,5,7,8,9,11,25))
        assert (e.q1,e.q2,e.q3,e.iqr,e.lf,e.uf,e.outliers)==(4.5,7.5,10.0,5.5,-3.75,18.25,(25.0,))
        rows = [
            self.step_row(1, "QUARTILES", self.math(r"Q_1=4.5\quad Q_2=7.5\quad Q_3=10", 30), y=0.55),
            self.step_row(2, "IQR", self.math(r"IQR=10-4.5=5.5", 31), y=-0.25),
            self.step_row(3, "FENCES", self.math(r"LF=-3.75\qquad UF=18.25", 30), y=-1.05),
            self.step_row(4, "TEST", self.math(r"25>18.25\;\Rightarrow\;25\text{ is an outlier}", 30), y=-1.85),
            self.step_row(5, "WHISKER", self.math(r"\text{upper regular whisker}=11", 29), y=-2.65),
        ]
        self.reveal_rows(rows, pause=PAUSE_READ)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def final_summary(self) -> None:
        self.set_header(11, "THE ROUTINE TO REMEMBER", "Use this exact sequence whenever you solve an IQR / modified-boxplot problem.")
        routine = VGroup(
            self.step_badge(1, "ORDER DATA", width=2.55),
            self.step_badge(2, "FIND Q1,Q2,Q3", width=2.55),
            self.step_badge(3, "CALCULATE IQR", width=2.55),
            self.step_badge(4, "FIND FENCES", width=2.55),
            self.step_badge(5, "CLASSIFY", width=2.55),
            self.step_badge(6, "DRAW / INTERPRET", width=2.55),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.48,0.30))
        routine.move_to(DOWN * 0.35)
        self.assert_content_safe(routine, "final routine")
        self.play(LaggedStart(*[FadeIn(r, shift=UP*0.04) for r in routine], lag_ratio=0.10), run_time=RUN_SLOW)
        line = self.text("Center → spread → whiskers → outliers → conclusion", 29, BOLD).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(line), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)


if __name__ == "__main__":
    pass
