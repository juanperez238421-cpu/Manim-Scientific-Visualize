#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 - IQR & Box Plots - Class 2.

Direct continuation of the Grade 10 third-period IQR/Boxplot sequence.
Primary emphasis: construction -> interpretation -> comparison -> justification.
Senior QA V2: improved graph-domain accuracy, stronger visual focus, larger comparison annotations, and clearer conceptual transitions.

Quartile convention (must match Class 1):
- odd n: identify Q2 and EXCLUDE it from the lower/upper halves;
- even n: split the ordered data into equal halves;
- Q1/Q3 are the medians of those halves.

Target: Manim Community Edition 0.20.1.
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
    if not values:
        raise ValueError("median requires at least one value")
    v = sorted(float(x) for x in values)
    n = len(v)
    if n % 2:
        return v[n // 2]
    return (v[n // 2 - 1] + v[n // 2]) / 2.0


def quartiles_class1(values: Sequence[float]) -> tuple[float, float, float]:
    """Return Q1, Q2, Q3 using the exact Class 1 split convention."""
    v = sorted(float(x) for x in values)
    if len(v) < 4:
        raise ValueError("at least four observations are required")
    n = len(v)
    q2 = _median(v)
    if n % 2:
        lower = v[: n // 2]
        upper = v[n // 2 + 1 :]
    else:
        lower = v[: n // 2]
        upper = v[n // 2 :]
    return _median(lower), q2, _median(upper)


def modified_box_summary(values: Sequence[float]) -> BoxSummary:
    v = tuple(sorted(float(x) for x in values))
    q1, q2, q3 = quartiles_class1(v)
    iqr = q3 - q1
    lf = q1 - 1.5 * iqr
    uf = q3 + 1.5 * iqr
    regular = tuple(x for x in v if lf <= x <= uf)
    outliers = tuple(x for x in v if x < lf or x > uf)
    if not regular:
        raise ValueError("modified boxplot requires at least one regular observation")
    return BoxSummary(
        data=v,
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


# Main lesson datasets ---------------------------------------------------------
OUTLIER_EXAMPLE = (2, 3, 4, 5, 6, 7, 8, 20)
GROUP_A = (40, 44, 47, 50, 52, 55, 59, 63)
GROUP_B = (49, 52, 53, 54, 55, 57, 58, 75)
CHALLENGE_C = (12, 14, 15, 16, 17, 18, 19, 20)
CHALLENGE_D = (13, 15, 16, 17, 18, 19, 20, 32)
READ_EXAMPLE = (3, 8, 9, 11, 13, 16, 18, 35)


class Statistics10IQRClass02CompareBoxplotsFinal(JPMathClassroomScene):
    """Class 2: formal fences, modified whiskers, reading and comparing boxplots."""

    # ------------------------------------------------------------------
    # Validation - every displayed numerical claim is asserted here.
    # ------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        # Convention guard: odd n excludes the overall median from both halves.
        assert quartiles_class1([1, 2, 3, 4, 5, 6, 7]) == (2.0, 4.0, 6.0)
        assert quartiles_class1(OUTLIER_EXAMPLE) == (3.5, 5.5, 7.5)

        ex = modified_box_summary(OUTLIER_EXAMPLE)
        assert_close(ex.iqr, 4.0, label="example IQR")
        assert_close(ex.lf, -2.5, label="example lower fence")
        assert_close(ex.uf, 13.5, label="example upper fence")
        assert_close(ex.lower_whisker, 2.0, label="example lower whisker")
        assert_close(ex.upper_whisker, 8.0, label="example upper whisker")
        assert ex.outliers == (20.0,)

        a = modified_box_summary(GROUP_A)
        b = modified_box_summary(GROUP_B)
        assert (a.q1, a.q2, a.q3) == (45.5, 51.0, 57.0)
        assert_close(a.iqr, 11.5, label="Group A IQR")
        assert a.outliers == ()
        assert_close(a.lower_whisker, 40.0, label="Group A lower whisker")
        assert_close(a.upper_whisker, 63.0, label="Group A upper whisker")

        assert (b.q1, b.q2, b.q3) == (52.5, 54.5, 57.5)
        assert_close(b.iqr, 5.0, label="Group B IQR")
        assert_close(b.lf, 45.0, label="Group B lower fence")
        assert_close(b.uf, 65.0, label="Group B upper fence")
        assert_close(b.lower_whisker, 49.0, label="Group B lower whisker")
        assert_close(b.upper_whisker, 58.0, label="Group B upper whisker")
        assert b.outliers == (75.0,)

        c = modified_box_summary(CHALLENGE_C)
        d = modified_box_summary(CHALLENGE_D)
        assert (c.q1, c.q2, c.q3, c.iqr) == (14.5, 16.5, 18.5, 4.0)
        assert c.outliers == ()
        assert (d.q1, d.q2, d.q3, d.iqr) == (15.5, 17.5, 19.5, 4.0)
        assert_close(d.uf, 25.5, label="challenge D upper fence")
        assert d.outliers == (32.0,)

        read_ex = modified_box_summary(READ_EXAMPLE)
        assert (read_ex.q1, read_ex.q2, read_ex.q3) == (8.5, 12.0, 17.0)
        assert_close(read_ex.iqr, 8.5, label="read example IQR")
        assert_close(read_ex.uf, 29.75, label="read example upper fence")
        assert read_ex.outliers == (35.0,)
        # Domain guard: every plotted value must lie on the visible axis.
        assert min(READ_EXAMPLE) >= 0 and max(READ_EXAMPLE) <= 40

        # Exit ticket.
        assert_close(26 - 18, 8, label="exit IQR")
        assert_close(18 - 1.5 * 8, 6, label="exit lower fence")
        assert_close(26 + 1.5 * 8, 38, label="exit upper fence")
        assert 41 > 38

    # ------------------------------------------------------------------
    # Small lesson-specific helpers.
    # ------------------------------------------------------------------
    def _fmt(self, value: float) -> str:
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.1f}"

    def data_strip(self, values: Sequence[float], width: float = 0.82) -> VGroup:
        cards = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=width,
                height=0.68,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.6,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            )
            number = self.math(self._fmt(float(value)), 29).move_to(box)
            cards.add(VGroup(box, number))
        cards.arrange(RIGHT, buff=0.10)
        return cards

    def common_axis(
        self,
        x_min: float,
        x_max: float,
        step: float,
        *,
        length: float = 13.0,
        y: float = -2.45,
    ) -> NumberLine:
        axis = NumberLine(
            x_range=[x_min, x_max, step],
            length=length,
            include_numbers=True,
            font_size=23,
            include_tip=False,
            color=BLACK_LINE,
            stroke_width=2.0,
            decimal_number_config={"num_decimal_places": 0},
        )
        axis.move_to([0, y, 0])
        return axis

    def boxplot_on_axis(
        self,
        axis: NumberLine,
        summary: BoxSummary,
        *,
        y: float,
        label: str,
        stroke_color=BLACK_LINE,
        box_height: float = 0.68,
        dashed_outlier_guide: bool = False,
    ) -> VGroup:
        p = axis.n2p
        x1, x2, x3 = p(summary.q1)[0], p(summary.q2)[0], p(summary.q3)[0]
        lw, uw = p(summary.lower_whisker)[0], p(summary.upper_whisker)[0]

        box = Rectangle(
            width=max(0.05, x3 - x1),
            height=box_height,
            stroke_color=stroke_color,
            stroke_width=3.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.35,
        ).move_to([(x1 + x3) / 2, y, 0])
        med = Line(
            [x2, y - box_height / 2, 0],
            [x2, y + box_height / 2, 0],
            color=stroke_color,
            stroke_width=4.2,
        )
        left_whisker = Line([lw, y, 0], [x1, y, 0], color=stroke_color, stroke_width=3.0)
        right_whisker = Line([x3, y, 0], [uw, y, 0], color=stroke_color, stroke_width=3.0)
        cap_l = Line([lw, y - 0.22, 0], [lw, y + 0.22, 0], color=stroke_color, stroke_width=3.0)
        cap_r = Line([uw, y - 0.22, 0], [uw, y + 0.22, 0], color=stroke_color, stroke_width=3.0)

        outlier_marks = VGroup()
        for value in summary.outliers:
            mark = Circle(
                radius=0.10,
                stroke_color=BLACK_LINE,
                stroke_width=2.4,
                fill_opacity=0,
            ).move_to([p(value)[0], y, 0])
            outlier_marks.add(mark)
            if dashed_outlier_guide:
                outlier_marks.add(
                    DashedLine(
                        [p(value)[0], y - 0.42, 0],
                        [p(value)[0], axis.get_y() + 0.12, 0],
                        color=LIGHT_GRAY,
                        stroke_width=1.4,
                        dash_length=0.08,
                    )
                )

        label_mob = self.text(label, 22, BOLD)
        self.fit(label_mob, 1.15, 0.42)
        label_mob.move_to([axis.get_left()[0] - 0.68, y, 0])

        group = VGroup(
            left_whisker,
            right_whisker,
            cap_l,
            cap_r,
            box,
            med,
            outlier_marks,
            label_mob,
        )
        return group

    def fence_guides(
        self,
        axis: NumberLine,
        summary: BoxSummary,
        *,
        y_bottom: float = -1.8,
        y_top: float = 1.8,
        include_labels: bool = True,
    ) -> VGroup:
        guides = VGroup()
        for value, name in ((summary.lf, "LF"), (summary.uf, "UF")):
            x = axis.n2p(value)[0]
            line = DashedLine(
                [x, y_bottom, 0],
                [x, y_top, 0],
                color=MID_GRAY,
                stroke_width=2.0,
                dash_length=0.10,
            )
            guides.add(line)
            if include_labels:
                label = self.math(rf"{name}={self._fmt(value)}", 26)
                label.next_to(line, UP, buff=0.08)
                guides.add(label)
        return guides

    def _comparison_base(self) -> VGroup:
        """Create the same-scale Group A / Group B display used across several scenes."""
        a = modified_box_summary(GROUP_A)
        b = modified_box_summary(GROUP_B)
        axis = self.common_axis(35, 80, 5, length=12.6, y=-2.40)
        plot_a = self.boxplot_on_axis(axis, a, y=0.70, label="GROUP A", stroke_color=BLACK_LINE)
        plot_b = self.boxplot_on_axis(axis, b, y=-0.80, label="GROUP B", stroke_color=DARK_GRAY)
        scale = self.text("SAME SCALE · 35 to 80", 21, BOLD).next_to(axis, DOWN, buff=0.24)
        base = VGroup(axis, plot_a, plot_b, scale)
        self.assert_content_safe(base, "same-scale comparison")
        self.compare_axis = axis
        self.compare_a = a
        self.compare_b = b
        self.compare_plot_a = plot_a
        self.compare_plot_b = plot_b
        self.compare_base = base
        return base

    # ------------------------------------------------------------------
    # Lesson orchestration.
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening()
        self.bridge_from_class1()
        self.fences_meaning()
        self.correct_whiskers()
        self.outlier_worked_example()
        self.read_a_boxplot()
        self.compare_two_groups()
        self.compare_center()
        self.compare_iqr()
        self.compare_whiskers()
        self.inspect_asymmetry()
        self.inspect_outliers()
        self.contextual_conclusion()
        self.common_mistakes()
        self.student_challenge()
        self.exit_ticket()
        self.next_lesson_bridge()

    # ------------------------------------------------------------------
    # SCENE 00 - Opening.
    # ------------------------------------------------------------------
    def opening(self) -> None:
        label = self.text("STATISTICS 10 · IQR / BOX PLOTS", 29, BOLD)
        class_tag = self.text("CLASS 2", 30, BOLD)
        title = self.text("FROM CONSTRUCTION TO INTERPRETATION", 49, BOLD)
        subtitle = self.text("Fences · Outliers · Whiskers · Spread · Shape · Comparison", 25)
        VGroup(label, class_tag, title, subtitle).arrange(DOWN, buff=0.20).shift(UP * 1.55)

        route = self.process_map(
            [
                ("1", "CLASSIFY"),
                ("2", "DRAW"),
                ("3", "READ"),
                ("4", "COMPARE"),
            ],
            card_width=3.05,
            card_height=1.02,
            columns=4,
        )
        route.move_to(DOWN * 0.62)
        bridge = self.text(
            "Last class we learned how to build the graph. Today we learn how to read it.",
            25,
            MEDIUM,
        ).to_edge(DOWN, buff=0.58)

        self.play(FadeIn(label, shift=UP * 0.10), FadeIn(class_tag), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.6,
        )
        self.wait(PAUSE_READ)
        # Reading and comparing are today's new focus.
        self.play(route[2].animate.scale(1.08), route[3].animate.scale(1.08), run_time=RUN_NORMAL)
        self.play(FadeIn(bridge, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)

    # ------------------------------------------------------------------
    # SCENE 01 - Recall without reteaching.
    # ------------------------------------------------------------------
    def bridge_from_class1(self) -> None:
        self.set_header(
            1,
            "RECALL: WHAT DO WE ALREADY KNOW?",
            "Read the box before adding a new rule: Q2 describes center and Q3 - Q1 describes the middle 50%.",
        )
        demo = modified_box_summary([2, 4, 6, 8, 10, 12, 14, 16])
        axis = self.common_axis(0, 18, 2, length=11.5, y=-1.15)
        plot = self.boxplot_on_axis(axis, demo, y=0.65, label="")
        labels = VGroup(
            self.math(r"Q_1", 30).move_to([axis.n2p(demo.q1)[0], 1.52, 0]),
            self.math(r"Q_2", 30).move_to([axis.n2p(demo.q2)[0], 1.52, 0]),
            self.math(r"Q_3", 30).move_to([axis.n2p(demo.q3)[0], 1.52, 0]),
        )
        meanings = VGroup(
            self.formula_panel(r"Q_2\;\rightarrow\;\text{center}", width=4.0, height=0.92, font_size=33),
            self.formula_panel(r"Q_3-Q_1\;\rightarrow\;\text{middle }50\%", width=5.7, height=0.92, font_size=32),
            self.formula_panel(r"\text{whiskers}\;\rightarrow\;\text{extreme regular values}", width=5.9, height=0.92, font_size=29),
        ).arrange(RIGHT, buff=0.20).scale(0.88)
        meanings.to_edge(DOWN, buff=0.50)
        question = self.text("But what happens when one value is very far away?", 31, BOLD)
        question.move_to(UP * 2.02)

        self.play(FadeIn(axis), Create(plot), run_time=RUN_SLOW)
        self.play(FadeIn(labels), run_time=RUN_NORMAL)
        self.play(FadeIn(meanings[0]), FadeIn(meanings[1]), FadeIn(meanings[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(question, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 02 - Why fences exist.
    # ------------------------------------------------------------------
    def fences_meaning(self) -> None:
        self.set_header(
            2,
            "WHY FENCES EXIST",
            "Fences are decision limits used to classify unusually distant observations; they are not data values we invent.",
        )
        ex = modified_box_summary(OUTLIER_EXAMPLE)
        axis = self.common_axis(-4, 22, 2, length=13.4, y=0.25)
        strip = self.data_strip(OUTLIER_EXAMPLE).scale(0.92).move_to(UP * 1.92)
        dots = VGroup()
        for value in OUTLIER_EXAMPLE:
            dot = Dot(axis.n2p(value) + UP * 0.26, radius=0.075, color=BLACK_LINE)
            dots.add(dot)
        far = self.text("20 is far from the cluster 2-8", 23, BOLD).next_to(axis.n2p(20) + UP * 0.25, UP, buff=0.22)
        self.fit(far, 4.2, 0.55)
        prompt = self.text("Should the whisker automatically extend all the way to 20?", 28, BOLD)
        prompt.next_to(axis, DOWN, buff=0.46)

        self.play(LaggedStart(*[FadeIn(card) for card in strip], lag_ratio=0.06), run_time=RUN_NORMAL)
        self.play(Create(axis), LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.05), run_time=RUN_NORMAL)
        self.play(FadeIn(far), run_time=RUN_QUICK)
        self.play(FadeIn(prompt, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)

        self.play(FadeOut(prompt), FadeOut(far), run_time=RUN_QUICK)
        calculations = VGroup(
            self.math(r"Q_1=3.5\qquad Q_2=5.5\qquad Q_3=7.5", 34),
            self.math(r"IQR=Q_3-Q_1=7.5-3.5=4", 37),
        ).arrange(DOWN, buff=0.18)
        calculations.move_to(DOWN * 1.05)
        self.play(Write(calculations[0]), run_time=RUN_NORMAL)
        self.play(Write(calculations[1]), run_time=RUN_NORMAL)

        fence_calc = VGroup(
            self.math(r"LF=Q_1-1.5(IQR)=3.5-1.5(4)=-2.5", 31),
            self.math(r"UF=Q_3+1.5(IQR)=7.5+1.5(4)=13.5", 31),
        ).arrange(DOWN, buff=0.14)
        fence_calc.to_edge(DOWN, buff=0.48)
        self.play(Write(fence_calc[0]), run_time=RUN_NORMAL)
        self.play(Write(fence_calc[1]), run_time=RUN_NORMAL)
        guides = self.fence_guides(axis, ex, y_bottom=-0.20, y_top=1.35, include_labels=True)
        self.play(Create(guides), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 03 - Correct whiskers.
    # ------------------------------------------------------------------
    def correct_whiskers(self) -> None:
        self.set_header(
            3,
            "FENCES ARE NOT WHISKER ENDPOINTS",
            "A modified boxplot stops each whisker at a real non-outlier observation and plots observations beyond the fences separately.",
        )
        ex = modified_box_summary(OUTLIER_EXAMPLE)
        axis = self.common_axis(-4, 22, 2, length=13.2, y=-1.85)
        guides = self.fence_guides(axis, ex, y_bottom=-1.20, y_top=1.75, include_labels=True)
        plot = self.boxplot_on_axis(axis, ex, y=0.45, label="MODIFIED BOXPLOT")

        decision = self.note_panel(
            "DECISION LIMITS",
            ["LF = -2.5", "UF = 13.5", "These limits classify data."],
            width=4.2,
            title_size=24,
            body_size=22,
        ).move_to(LEFT * 4.80 + UP * 1.10)
        real_values = self.note_panel(
            "REAL DATA VALUES",
            ["Lower whisker = 2", "Upper whisker = 8", "Outlier = 20"],
            width=4.2,
            title_size=24,
            body_size=22,
        ).move_to(RIGHT * 4.80 + UP * 1.10)

        self.play(Create(axis), run_time=RUN_NORMAL)
        self.play(Create(guides), run_time=RUN_NORMAL)
        self.play(Create(plot), run_time=RUN_SLOW)
        self.play(FadeIn(decision), FadeIn(real_values), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)

        rule = self.formula_panel(
            r"\text{whisker}=\text{most extreme REAL observation still inside the fences}",
            width=11.8,
            height=0.92,
            font_size=30,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(rule, shift=UP * 0.06), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 04 - Worked classification.
    # ------------------------------------------------------------------
    def outlier_worked_example(self) -> None:
        self.set_header(
            4,
            "WORKED EXAMPLE: CLASSIFY BEFORE DRAWING",
            "The arithmetic creates the decision rule; the ordered data then determines the actual whisker endpoints.",
        )
        ex = modified_box_summary(OUTLIER_EXAMPLE)
        strip = self.data_strip(ex.data).move_to(UP * 1.70)
        equations = self.equation_stack(
            [
                r"IQR=7.5-3.5=4",
                r"LF=3.5-1.5(4)=-2.5",
                r"UF=7.5+1.5(4)=13.5",
                r"20>13.5\;\Rightarrow\;20\text{ is an upper outlier}",
            ],
            sizes=[34, 32, 32, 33],
            max_width=7.0,
            max_height=3.4,
        ).move_to(LEFT * 3.70 + DOWN * 0.55)
        interpretation = self.note_panel(
            "NOW READ THE DATA",
            [
                "Smallest regular value: 2",
                "Largest regular value: 8",
                "20 is drawn as a separate point.",
                "The whisker does NOT end at 13.5.",
            ],
            width=5.5,
            title_size=26,
            body_size=23,
        ).move_to(RIGHT * 4.05 + DOWN * 0.52)
        self.assert_content_safe(VGroup(strip, equations, interpretation), "worked outlier example")

        self.play(LaggedStart(*[FadeIn(card) for card in strip], lag_ratio=0.05), run_time=RUN_NORMAL)
        self.animate_equation_stack(equations, pause=PAUSE_SHORT)
        self.play(Circumscribe(equations[3], color=BLACK_LINE, buff=0.08), run_time=RUN_NORMAL)
        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)
        self.play(Circumscribe(interpretation[1][1][-1], color=BLACK_LINE, buff=0.06), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 05 - Read one boxplot.
    # ------------------------------------------------------------------
    def read_a_boxplot(self) -> None:
        self.set_header(
            5,
            "READ THE GRAPH, NOT ONLY THE FORMULA",
            "A boxplot communicates center, middle-50% spread, regular extremes and unusual observations on one numerical scale.",
        )
        summary = modified_box_summary(READ_EXAMPLE)
        # Senior-QA fix: the axis must include the outlier at 35.
        axis = self.common_axis(0, 40, 5, length=12.4, y=-2.15)
        plot = self.boxplot_on_axis(axis, summary, y=0.65, label="EXAMPLE")
        self.play(Create(axis), Create(plot), run_time=RUN_SLOW)

        qlabels = VGroup(
            self.math(rf"Q_1={self._fmt(summary.q1)}", 27).move_to([axis.n2p(summary.q1)[0], 1.45, 0]),
            self.math(rf"Q_2={self._fmt(summary.q2)}", 27).move_to([axis.n2p(summary.q2)[0], 1.45, 0]),
            self.math(rf"Q_3={self._fmt(summary.q3)}", 27).move_to([axis.n2p(summary.q3)[0], 1.45, 0]),
        )
        self.play(FadeIn(qlabels), run_time=RUN_NORMAL)

        uf_x = axis.n2p(summary.uf)[0]
        uf_guide = DashedLine([uf_x, -1.35, 0], [uf_x, 1.20, 0], color=MID_GRAY, stroke_width=2.0)
        uf_label = self.math(rf"UF={self._fmt(summary.uf)}", 25).next_to(uf_guide, UP, buff=0.06)
        outlier_ring = Circle(radius=0.18, stroke_color=BLACK_LINE, stroke_width=2.4, fill_opacity=0).move_to([axis.n2p(35)[0], 0.65, 0])
        outlier_note = self.text("35 is beyond the upper fence", 23, BOLD).next_to(outlier_ring, UP, buff=0.20)
        self.fit(outlier_note, 4.5, 0.50)
        self.play(Create(uf_guide), FadeIn(uf_label), Create(outlier_ring), FadeIn(outlier_note), run_time=RUN_NORMAL)

        meaning = VGroup(
            self.note_panel("CENTER", [f"Median = {self._fmt(summary.q2)}"], width=3.3, title_size=23, body_size=22),
            self.note_panel(
                "MIDDLE 50%",
                [f"IQR = {self._fmt(summary.iqr)} units", "Half the data lie inside the box."],
                width=4.4,
                title_size=23,
                body_size=21,
            ),
            self.note_panel(
                "REGULAR EXTENT",
                [f"Whiskers: {self._fmt(summary.lower_whisker)} to {self._fmt(summary.upper_whisker)}", f"Outlier: {self._fmt(summary.outliers[0])}"],
                width=4.2,
                title_size=23,
                body_size=21,
            ),
        ).arrange(RIGHT, buff=0.22)
        self.fit(meaning, 13.6, 1.6)
        meaning.to_edge(DOWN, buff=0.42)
        self.play(LaggedStart(*[FadeIn(card) for card in meaning], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENES 06-11 - Same-scale comparison sequence.
    # ------------------------------------------------------------------
    def compare_two_groups(self) -> None:
        self.set_header(
            6,
            "COMPARE TWO BOXPLOTS ON THE SAME SCALE",
            "Use one numerical scale before comparing center, middle spread, whiskers, possible asymmetry and outliers.",
        )
        base = self._comparison_base()
        data_a = self.text("A: 40, 44, 47, 50, 52, 55, 59, 63", 24)
        data_b = self.text("B: 49, 52, 53, 54, 55, 57, 58, 75", 24)
        VGroup(data_a, data_b).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(UP, buff=1.60).to_edge(LEFT, buff=1.10)
        self.compare_data_labels = VGroup(data_a, data_b)
        self.play(FadeIn(self.compare_data_labels), run_time=RUN_NORMAL)
        self.play(Create(base[0]), run_time=RUN_NORMAL)
        self.play(Create(base[1]), run_time=RUN_NORMAL)
        self.play(Create(base[2]), FadeIn(base[3]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

    def compare_center(self) -> None:
        self.set_header(
            7,
            "COMPARE CENTER FIRST",
            "Median position answers a center question; do not confuse a higher median with greater variability.",
        )
        axis = self.compare_axis
        a, b = self.compare_a, self.compare_b
        guides = VGroup(
            DashedLine([axis.n2p(a.q2)[0], -1.25, 0], [axis.n2p(a.q2)[0], 1.25, 0], color=LIGHT_GRAY, stroke_width=1.8),
            DashedLine([axis.n2p(b.q2)[0], -1.25, 0], [axis.n2p(b.q2)[0], 1.25, 0], color=LIGHT_GRAY, stroke_width=1.8),
        )
        statement = self.formula_panel(
            r"Q_{2,B}=54.5>Q_{2,A}=51\quad\Rightarrow\quad\text{Group B has the higher median.}",
            width=10.8,
            height=0.92,
            font_size=30,
        ).to_edge(DOWN, buff=0.42)
        focus_a = RoundedRectangle(width=0.42, height=1.18, corner_radius=0.06, stroke_color=MID_GRAY, stroke_width=1.6, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.30).move_to([axis.n2p(a.q2)[0], 0.70, 0])
        focus_b = RoundedRectangle(width=0.42, height=1.18, corner_radius=0.06, stroke_color=MID_GRAY, stroke_width=1.6, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.30).move_to([axis.n2p(b.q2)[0], -0.80, 0])
        self.play(Create(guides), FadeIn(focus_a), FadeIn(focus_b), run_time=RUN_NORMAL)
        self.play(FadeIn(statement, shift=UP * 0.06), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(guides), FadeOut(focus_a), FadeOut(focus_b), FadeOut(statement), run_time=RUN_QUICK)

    def compare_iqr(self) -> None:
        self.set_header(
            8,
            "COMPARE THE MIDDLE 50% WITH IQR",
            "The box width is meaningful only because both boxplots use the same numerical scale.",
        )
        axis = self.compare_axis
        a, b = self.compare_a, self.compare_b
        brace_a = BraceBetweenPoints(
            [axis.n2p(a.q1)[0], 0.20, 0],
            [axis.n2p(a.q3)[0], 0.20, 0],
            direction=DOWN,
            color=BLACK_LINE,
        )
        brace_b = BraceBetweenPoints(
            [axis.n2p(b.q1)[0], -1.28, 0],
            [axis.n2p(b.q3)[0], -1.28, 0],
            direction=DOWN,
            color=BLACK_LINE,
        )
        lab_a = self.math(r"IQR_A=11.5", 27).next_to(brace_a, DOWN, buff=0.08)
        lab_b = self.math(r"IQR_B=5", 27).next_to(brace_b, DOWN, buff=0.08)
        statement = self.text(
            "Group B has a smaller IQR, so its central observations are more tightly clustered.",
            26,
            BOLD,
        ).to_edge(DOWN, buff=0.42)
        self.fit(statement, 13.8, 0.55)
        self.play(GrowFromCenter(brace_a), FadeIn(lab_a), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(brace_b), FadeIn(lab_b), run_time=RUN_NORMAL)
        self.play(FadeIn(statement, shift=UP * 0.06), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(VGroup(brace_a, brace_b, lab_a, lab_b, statement)), run_time=RUN_QUICK)

    def compare_whiskers(self) -> None:
        self.set_header(
            9,
            "READ THE REGULAR EXTERIOR SPREAD",
            "Whisker lengths describe how far the regular observations extend outside the middle 50%; they are not fence distances.",
        )
        axis = self.compare_axis
        labels = VGroup(
            self.text("A lower: 40 to 45.5", 23, BOLD).move_to([axis.n2p(43)[0], 1.42, 0]),
            self.text("A upper: 57 to 63", 23, BOLD).move_to([axis.n2p(60)[0], 1.42, 0]),
            self.text("B lower: 49 to 52.5", 23, BOLD).move_to([axis.n2p(50.7)[0], -1.55, 0]),
            self.text("B upper: 57.5 to 58", 23, BOLD).move_to([axis.n2p(58)[0], -1.55, 0]),
        )
        statement = self.text(
            "Group A is fairly balanced outside the box; Group B has a very short upper regular whisker.",
            23,
            BOLD,
        ).move_to(UP * 2.05)
        self.fit(statement, 12.8, 0.50)
        self.play(FadeOut(self.compare_data_labels), FadeIn(statement), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(labels), FadeOut(statement), run_time=RUN_QUICK)

    def inspect_asymmetry(self) -> None:
        self.set_header(
            10,
            "SHAPE CLUES: BE CAUTIOUS",
            "Unequal box halves or whiskers can suggest asymmetry, but a boxplot is a compact summary - not a complete picture of distribution shape.",
        )
        a, b = self.compare_a, self.compare_b
        axis = self.compare_axis
        median_a = Dot([axis.n2p(a.q2)[0], 0.70, 0], radius=0.11, color=BLACK_LINE)
        median_b = Dot([axis.n2p(b.q2)[0], -0.80, 0], radius=0.11, color=BLACK_LINE)
        note = VGroup(
            self.text("Group A looks roughly balanced around its median.", 22, BOLD),
            self.text("Group B shows an upper-side irregularity - a clue, not proof of shape.", 22, BOLD),
        ).arrange(DOWN, buff=0.10).move_to(UP * 1.95)
        self.fit(note, 12.7, 0.95)
        self.play(FadeIn(note), FadeIn(median_a), FadeIn(median_b), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(note), FadeOut(median_a), FadeOut(median_b), run_time=RUN_QUICK)

    def inspect_outliers(self) -> None:
        self.set_header(
            11,
            "OUTLIERS MUST STAY SEPARATE",
            "An outlier is still part of the dataset, but the modified whisker stops at the most extreme regular observation.",
        )
        b = self.compare_b
        axis = self.compare_axis
        x_uf = axis.n2p(b.uf)[0]
        guide = DashedLine([x_uf, -1.50, 0], [x_uf, -0.12, 0], color=MID_GRAY, stroke_width=2)
        uf_label = self.math(r"UF_B=65", 26).next_to(guide, UP, buff=0.06)
        out_x = axis.n2p(75)[0]
        out_circle = Circle(radius=0.18, stroke_color=BLACK_LINE, stroke_width=2.4, fill_opacity=0).move_to([out_x, -0.80, 0])
        out_label = self.text("75 is plotted separately", 24, BOLD).next_to(out_circle, UP, buff=0.22)
        whisker_label = self.text("upper whisker ends at 58", 23).move_to([axis.n2p(58)[0], -0.15, 0])
        self.play(Create(guide), FadeIn(uf_label), run_time=RUN_NORMAL)
        self.play(Create(out_circle), FadeIn(out_label), FadeIn(whisker_label), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(VGroup(guide, uf_label, out_circle, out_label, whisker_label)), run_time=RUN_QUICK)
        # Comparison sequence ends here.
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 12 - Contextual conclusion.
    # ------------------------------------------------------------------
    def contextual_conclusion(self) -> None:
        self.set_header(
            12,
            "TURN NUMBERS INTO A STATISTICAL CONCLUSION",
            "A strong comparison names the feature, cites evidence and explains what the evidence means in context.",
        )
        cards = VGroup(
            self.note_panel(
                "CENTER",
                ["Group B has the higher median:", "54.5 compared with 51."],
                width=4.25,
                title_size=24,
                body_size=22,
            ),
            self.note_panel(
                "MIDDLE 50%",
                ["Group B spans only 5 units.", "Group A spans 11.5 units."],
                width=4.25,
                title_size=24,
                body_size=22,
            ),
            self.note_panel(
                "QUALIFICATION",
                ["Group B also contains", "one unusually high value: 75."],
                width=4.25,
                title_size=24,
                body_size=22,
            ),
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.55)
        conclusion = self.text(
            "Therefore: Group B is more tightly clustered in its central 50%, but it also has an unusually high observation.",
            27,
            BOLD,
        )
        self.fit(conclusion, 13.8, 0.70)
        conclusion.to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(conclusion, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 13 - Common mistakes.
    # ------------------------------------------------------------------
    def common_mistakes(self) -> None:
        self.set_header(
            13,
            "COMMON MISTAKES TO AVOID",
            "Each mistake changes the statistical meaning of the graph or makes a comparison invalid.",
        )
        mistakes = self.process_map(
            [
                ("1", "USING A FENCE AS A WHISKER"),
                ("2", "CONNECTING AN OUTLIER TO THE WHISKER"),
                ("3", "COMPARING PLOTS WITH DIFFERENT SCALES"),
                ("4", "SAYING ONLY: 'THIS GRAPH IS BIGGER'"),
            ],
            card_width=6.35,
            card_height=1.22,
            columns=2,
        )
        mistakes.move_to(UP * 0.15)
        correction = self.formula_panel(
            r"\text{Compare: center + IQR + regular spread + asymmetry clues + outliers}",
            width=11.8,
            height=0.95,
            font_size=29,
        ).to_edge(DOWN, buff=0.38)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in mistakes], lag_ratio=0.14), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(correction), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 14 - Student challenge.
    # ------------------------------------------------------------------
    def student_challenge(self) -> None:
        self.set_header(
            14,
            "YOUR TURN: COMPARE BEFORE THE REVEAL",
            "Use the same order every time: center -> IQR -> whiskers -> possible asymmetry -> outliers -> conclusion.",
        )
        c = modified_box_summary(CHALLENGE_C)
        d = modified_box_summary(CHALLENGE_D)
        axis = self.common_axis(8, 34, 2, length=12.8, y=-2.25)
        pc = self.boxplot_on_axis(axis, c, y=0.70, label="GROUP C")
        pd = self.boxplot_on_axis(axis, d, y=-0.75, label="GROUP D", stroke_color=DARK_GRAY)
        task = self.text(
            "1) Which group has the higher median?    2) Compare IQR.    3) Identify any outlier.",
            26,
            BOLD,
        ).to_edge(UP, buff=1.58)
        self.fit(task, 13.6, 0.55)
        self.play(FadeIn(task), Create(axis), run_time=RUN_NORMAL)
        self.play(Create(pc), Create(pd), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK * 1.55)

        reveal = VGroup(
            self.formula_panel(r"Q_{2,D}=17.5>Q_{2,C}=16.5", width=4.4, height=0.84, font_size=29),
            self.formula_panel(r"IQR_C=IQR_D=4", width=4.1, height=0.84, font_size=29),
            self.formula_panel(r"32>UF_D=25.5\Rightarrow\text{ upper outlier}", width=5.2, height=0.84, font_size=27),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(panel) for panel in reveal], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 15 - Exit ticket.
    # ------------------------------------------------------------------
    def exit_ticket(self) -> None:
        self.set_header(
            15,
            "EXIT TICKET",
            "Answer each question in words as well as with arithmetic; the meaning is part of the answer.",
        )
        prompt = self.note_panel(
            "GIVEN",
            ["Q1 = 18", "Q3 = 26", "Largest observations include 35 and 41."],
            width=4.6,
            title_size=25,
            body_size=23,
        ).move_to(LEFT * 4.65 + UP * 0.65)
        questions = self.note_panel(
            "QUESTIONS",
            [
                "1. Find IQR, LF and UF.",
                "2. Is 41 an outlier? Explain.",
                "3. What does IQR = 8 mean?",
            ],
            width=7.4,
            title_size=25,
            body_size=23,
        ).move_to(RIGHT * 2.90 + UP * 0.65)
        self.play(FadeIn(prompt), FadeIn(questions), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK * 1.70)

        answer = VGroup(
            self.math(r"IQR=26-18=8", 32),
            self.math(r"LF=18-1.5(8)=6\qquad UF=26+1.5(8)=38", 31),
            self.math(r"41>38\Rightarrow 41\text{ is an upper outlier}", 31),
            self.text("Interpretation: the middle 50% of the observations spans 8 units.", 24, BOLD),
        ).arrange(DOWN, buff=0.18)
        self.fit(answer, 12.4, 2.1)
        answer.to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.05) for line in answer], lag_ratio=0.16), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # SCENE 16 - Bridge to next lesson.
    # ------------------------------------------------------------------
    def next_lesson_bridge(self) -> None:
        self.set_header(
            16,
            "NEXT: FROM QUARTILES TO MORE POSITION MEASURES",
            "Today ends with interpretation. The next lesson generalizes position using deciles and percentiles.",
        )
        route = self.process_map(
            [
                ("1", "QUARTILES"),
                ("2", "DECILES"),
                ("3", "PERCENTILES"),
            ],
            card_width=3.9,
            card_height=1.16,
            columns=3,
        ).move_to(UP * 0.85)
        preview = VGroup(
            self.formula_panel(r"Q_1=P_{25}", width=3.7, height=0.90, font_size=34),
            self.formula_panel(r"Q_2=P_{50}", width=3.7, height=0.90, font_size=34),
            self.formula_panel(r"Q_3=P_{75}", width=3.7, height=0.90, font_size=34),
        ).arrange(RIGHT, buff=0.26).move_to(DOWN * 0.75)
        final = self.text(
            "Class 2 takeaway: construct correctly, then compare with evidence and precise statistical language.",
            27,
            BOLD,
        )
        self.fit(final, 13.6, 0.70)
        final.to_edge(DOWN, buff=0.44)
        self.play(LaggedStart(*[FadeIn(card) for card in route], lag_ratio=0.14), run_time=RUN_SLOW)
        self.play(LaggedStart(*[FadeIn(card) for card in preview], lag_ratio=0.14), run_time=RUN_SLOW)
        self.play(FadeIn(final, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Construct. Read. Compare. Justify.")


# Preview (protocol gate):
#   LESSON_TIME_SCALE=0.08 manim -pql Statistics10_IQR_Class02_Compare_Boxplots_FINAL.py Statistics10IQRClass02CompareBoxplotsFinal --disable_caching
# Final:
#   manim -pqh Statistics10_IQR_Class02_Compare_Boxplots_FINAL.py Statistics10IQRClass02CompareBoxplotsFinal --disable_caching
