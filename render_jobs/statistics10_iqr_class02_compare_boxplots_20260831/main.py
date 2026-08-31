#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 — IQR / Boxplot Class 02.

Case study: compare two distributions on the same scale.

Pedagogical focus
-----------------
- Reconnect the five-number summary with a boxplot.
- Compare center, IQR, overall spread and outliers.
- Show why two boxplots must use the same horizontal scale.
- Interpret a real classroom-style decision instead of only calculating.

Visual lineage
--------------
- JP classroom format: 1920x1080, 30 fps, white background.
- Large projector-safe typography.
- Persistent numbered section header + subtitle.
- Restrained accent colors only for semantic emphasis.
- ManimCE 0.20.1 compatible.
"""

from __future__ import annotations

import os
from statistics import median
from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

INK = BLACK
MUTED = "#666666"
LIGHT = "#D7D7D7"
PAPER = "#F7F7F7"
ACCENT = "#2457C5"
ACCENT2 = "#15803D"
ALERT = "#B91C1C"
GOLD = "#A16207"

SAFE_X = 7.55
SAFE_TOP = 2.55
SAFE_BOTTOM = -4.05


# =============================================================================
# DATA / VALIDATION
# =============================================================================
GROUP_A = [4, 5, 6, 6, 7, 7, 8, 8, 9, 10, 10, 11]
GROUP_B = [3, 4, 5, 6, 7, 7, 8, 9, 10, 12, 14, 22]


def quartiles_halves(values):
    """Median-of-halves convention used in the previous IQR lesson."""
    v = sorted(values)
    n = len(v)
    if n % 2:
        q2 = float(v[n // 2])
        lo = v[: n // 2]
        hi = v[n // 2 + 1 :]
    else:
        q2 = (v[n // 2 - 1] + v[n // 2]) / 2
        lo = v[: n // 2]
        hi = v[n // 2 :]

    q1 = float(median(lo))
    q3 = float(median(hi))
    return q1, float(q2), q3


def summary(values):
    q1, q2, q3 = quartiles_halves(values)
    iqr = q3 - q1
    lf = q1 - 1.5 * iqr
    uf = q3 + 1.5 * iqr
    inliers = [x for x in values if lf <= x <= uf]
    outliers = [x for x in values if x < lf or x > uf]
    return {
        "q1": q1,
        "median": q2,
        "q3": q3,
        "iqr": iqr,
        "lf": lf,
        "uf": uf,
        "wmin": min(inliers),
        "wmax": max(inliers),
        "outliers": outliers,
        "range": max(values) - min(values),
    }


A = summary(GROUP_A)
B = summary(GROUP_B)


# =============================================================================
# MAIN SCENE
# =============================================================================
class Statistics10IQRClass02CompareBoxplots(MovingCameraScene):
    """Class 02: comparison and interpretation of two boxplots."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.subheader = None
        self.validate_lesson_data()

    # ------------------------------------------------------------------
    # Timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_lesson_data(self):
        assert GROUP_A == sorted(GROUP_A)
        assert GROUP_B == sorted(GROUP_B)
        assert (A["q1"], A["median"], A["q3"], A["iqr"]) == (6.0, 7.5, 9.5, 3.5)
        assert (A["lf"], A["uf"], A["wmin"], A["wmax"]) == (0.75, 14.75, 4, 11)
        assert A["outliers"] == []
        assert (B["q1"], B["median"], B["q3"], B["iqr"]) == (5.5, 7.5, 11.0, 5.5)
        assert (B["lf"], B["uf"], B["wmin"], B["wmax"]) == (-2.75, 19.25, 3, 14)
        assert B["outliers"] == [22]
        assert A["median"] == B["median"] == 7.5
        assert B["iqr"] > A["iqr"]

    # ------------------------------------------------------------------
    # Typography / layout helpers
    # ------------------------------------------------------------------
    def t(self, text, size=30, weight=NORMAL, color=INK):
        return Text(text, font_size=size, weight=weight, color=color, line_spacing=0.92)

    def m(self, expression, size=40, color=INK):
        return MathTex(expression, font_size=size, color=color)

    def fit(self, mob, max_w=14.6, max_h=6.0):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def safe(self, mob, label, top=SAFE_TOP, bottom=SAFE_BOTTOM):
        if mob.get_left()[0] < -SAFE_X or mob.get_right()[0] > SAFE_X:
            raise ValueError(f"{label}: horizontal safe-frame violation")
        if mob.get_top()[1] > top or mob.get_bottom()[1] < bottom:
            raise ValueError(f"{label}: vertical safe-frame violation")

    def set_header(self, num, title, subtitle):
        nbox = RoundedRectangle(
            width=0.76, height=0.58, corner_radius=0.10,
            stroke_color=INK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        ntxt = self.t(f"{num:02d}", 24, BOLD).move_to(nbox)
        title_m = self.t(title, 36, BOLD)
        self.fit(title_m, 13.7, 0.60)
        row = VGroup(VGroup(nbox, ntxt), title_m).arrange(RIGHT, buff=0.28)
        row.to_edge(UP, buff=0.18).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.45, RIGHT * 7.45, stroke_color=LIGHT, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.08)
        sub = self.t(subtitle, 22, NORMAL, MUTED)
        self.fit(sub, 14.2, 0.74)
        sub.next_to(rule, DOWN, buff=0.10).align_to(row, LEFT)

        new_h, new_s = VGroup(row, rule), sub
        if self.header is None:
            self.add(new_h, new_s)
        else:
            self.play(
                ReplacementTransform(self.header, new_h),
                ReplacementTransform(self.subheader, new_s),
                run_time=0.65,
            )
        self.header, self.subheader = new_h, new_s

    def clear_stage(self):
        keep = set()
        for root in (self.header, self.subheader):
            if root is not None:
                keep.update(id(x) for x in root.get_family())
        removable = [x for x in self.mobjects if id(x) not in keep]
        if removable:
            self.play(*[FadeOut(x) for x in removable], run_time=0.75)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def panel(self, width, height, title=None):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=INK, stroke_width=1.8,
            fill_color=PAPER, fill_opacity=1,
        )
        if title is None:
            return box
        label = self.t(title, 25, BOLD).move_to(box.get_top() + DOWN * 0.32)
        return VGroup(box, label)

    def data_row(self, values, color=INK, box_w=0.72):
        cards = VGroup()
        for value in values:
            r = RoundedRectangle(
                width=box_w, height=0.70, corner_radius=0.08,
                stroke_color=color, stroke_width=1.8,
                fill_color=WHITE, fill_opacity=1,
            )
            n = self.m(str(value), 28, color if value == 22 else INK).move_to(r)
            cards.add(VGroup(r, n))
        cards.arrange(RIGHT, buff=0.08)
        return cards

    def number_line(self, x_min=0, x_max=24, length=12.3, step=2):
        return NumberLine(
            x_range=[x_min, x_max, step], length=length,
            include_numbers=True, font_size=25, color=INK,
            stroke_width=2, include_tip=False,
        )

    def boxplot_on_line(self, line, stats, y, color=ACCENT, label=""):
        p = line.n2p
        h = 0.62
        q1, q2, q3 = stats["q1"], stats["median"], stats["q3"]
        wmin, wmax = stats["wmin"], stats["wmax"]

        box = Rectangle(
            width=p(q3)[0] - p(q1)[0], height=h,
            stroke_color=color, stroke_width=3,
            fill_color=color, fill_opacity=0.08,
        ).move_to([(p(q1)[0] + p(q3)[0]) / 2, y, 0])
        med = Line([p(q2)[0], y - h / 2, 0], [p(q2)[0], y + h / 2, 0], color=ALERT, stroke_width=4)
        lw = Line([p(wmin)[0], y, 0], [p(q1)[0], y, 0], color=color, stroke_width=3)
        rw = Line([p(q3)[0], y, 0], [p(wmax)[0], y, 0], color=color, stroke_width=3)
        cl = Line([p(wmin)[0], y - 0.20, 0], [p(wmin)[0], y + 0.20, 0], color=color, stroke_width=3)
        cr = Line([p(wmax)[0], y - 0.20, 0], [p(wmax)[0], y + 0.20, 0], color=color, stroke_width=3)
        dots = VGroup(*[
            Dot([p(x)[0], y, 0], radius=0.095, color=ALERT)
            for x in stats["outliers"]
        ])
        tag = self.t(label, 24, BOLD, color).next_to([p(0)[0], y, 0], LEFT, buff=0.25) if label else VGroup()
        return VGroup(lw, rw, cl, cr, box, med, dots, tag)

    def mini_summary(self, title, stats, width=5.9, color=ACCENT):
        box = RoundedRectangle(
            width=width, height=3.35, corner_radius=0.14,
            stroke_color=color, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        head = self.t(title, 27, BOLD, color)
        r1 = self.m(rf"Q_1={stats['q1']:g}\quad M={stats['median']:g}\quad Q_3={stats['q3']:g}", 34)
        r2 = self.m(rf"IQR={stats['iqr']:g}", 37, color)
        r3 = self.m(rf"LF={stats['lf']:g}\quad UF={stats['uf']:g}", 31)
        if stats["outliers"]:
            out = self.m(r"22>19.25\Rightarrow \text{outlier}", 32, ALERT)
        else:
            out = self.t("No values outside the fences", 23, BOLD, ACCENT2)
        content = VGroup(head, r1, r2, r3, out).arrange(DOWN, buff=0.18)
        self.fit(content, width - 0.45, 2.85)
        content.move_to(box)
        return VGroup(box, content)

    def metric_card(self, label, a_text, b_text, verdict, color=INK):
        box = RoundedRectangle(
            width=4.25, height=1.50, corner_radius=0.13,
            stroke_color=color, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        h = self.t(label, 23, BOLD, color)
        vals = self.t(f"A: {a_text}     B: {b_text}", 22)
        v = self.t(verdict, 19, BOLD, MUTED)
        content = VGroup(h, vals, v).arrange(DOWN, buff=0.08).move_to(box)
        self.fit(content, 3.88, 1.16)
        return VGroup(box, content)

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.recap()
        self.case_data()
        self.five_number_summaries()
        self.same_scale_boxplots()
        self.compare_metrics()
        self.outlier_meaning()
        self.decision_case()
        self.summary_scene()

    def opening(self):
        top = self.t("STATISTICS 10 · IQR CLASS 02", 31, BOLD, ACCENT)
        title = self.t("COMPARE TWO BOXPLOTS", 58, BOLD)
        subtitle = self.t("Same median does not mean same distribution", 31, NORMAL, MUTED)
        mission = self.t("Compare center, middle spread, whiskers and unusual values on one common scale.", 28, BOLD)
        group = VGroup(top, title, subtitle, mission).arrange(DOWN, buff=0.33).move_to(DOWN * 0.10)
        self.safe(group, "opening", top=3.8, bottom=-3.7)
        self.play(FadeIn(top, shift=UP * 0.10), Write(title), run_time=1.25)
        self.play(FadeIn(subtitle), run_time=0.70)
        self.play(FadeIn(mission, shift=UP * 0.08), run_time=0.85)
        self.wait(3.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.85)

    def recap(self):
        self.set_header(1, "RECAP THE READING ORDER", "A boxplot is a compressed summary. Read its components in a fixed order before making a conclusion.")
        cards = VGroup(
            self.metric_card("1 · CENTER", "median", "median", "Compare typical position", ACCENT),
            self.metric_card("2 · MIDDLE 50%", "IQR", "IQR", "Compare consistency", ACCENT2),
            self.metric_card("3 · WHISKERS", "non-outliers", "non-outliers", "Compare ordinary spread", GOLD),
            self.metric_card("4 · OUTLIERS", "unusual?", "unusual?", "Flag values for investigation", ALERT),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.42)).move_to(DOWN * 0.55)
        self.safe(cards, "recap cards")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.12), run_time=1.55)
        self.wait(3.6)
        self.clear_stage()

    def case_data(self):
        self.set_header(2, "THE CASE: TWO GROUPS", "Both groups have twelve scores. The data are already ordered so the comparison can focus on the boxplots.")
        pa = self.panel(13.3, 1.65, "GROUP A")
        pb = self.panel(13.3, 1.65, "GROUP B")
        pa.move_to(UP * 0.55)
        pb.move_to(DOWN * 1.55)
        ra = self.data_row(GROUP_A, ACCENT).scale(0.96).move_to(pa[0]).shift(DOWN * 0.13)
        rb = self.data_row(GROUP_B, ACCENT2).scale(0.96).move_to(pb[0]).shift(DOWN * 0.13)
        highlight = SurroundingRectangle(rb[-1], color=ALERT, buff=0.08, stroke_width=3)
        q = self.t("Question: Which group is more consistent, and what should we say about 22?", 29, BOLD).to_edge(DOWN, buff=0.28)
        self.safe(VGroup(pa, pb, q), "case data")
        self.play(FadeIn(pa), FadeIn(pb), run_time=0.85)
        self.play(LaggedStart(*[FadeIn(c) for c in ra], lag_ratio=0.06), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(c) for c in rb], lag_ratio=0.06), run_time=1.0)
        self.play(Create(highlight), run_time=0.65)
        self.play(FadeIn(q, shift=UP * 0.08), run_time=0.80)
        self.wait(4.2)
        self.clear_stage()

    def five_number_summaries(self):
        self.set_header(3, "CALCULATE ONLY WHAT THE BOXPLOT NEEDS", "Use the same quartile convention as Class 01, then compute IQR and the 1.5 IQR fences.")
        left = self.mini_summary("GROUP A", A, color=ACCENT).move_to(LEFT * 3.35 + DOWN * 0.20)
        right = self.mini_summary("GROUP B", B, color=ACCENT2).move_to(RIGHT * 3.35 + DOWN * 0.20)
        same = self.m(r"M_A=M_B=7.5", 48, ALERT).to_edge(DOWN, buff=0.35)
        self.safe(VGroup(left, right, same), "summary panels")
        self.play(FadeIn(left, shift=RIGHT * 0.08), run_time=1.0)
        self.play(FadeIn(right, shift=LEFT * 0.08), run_time=1.0)
        self.play(Write(same), run_time=0.9)
        self.wait(4.0)
        self.clear_stage()

    def same_scale_boxplots(self):
        self.set_header(4, "PUT BOTH BOXPLOTS ON THE SAME SCALE", "Only a common number line makes horizontal lengths directly comparable.")
        line = self.number_line().move_to(DOWN * 1.60)
        aplot = self.boxplot_on_line(line, A, y=0.70, color=ACCENT, label="A")
        bplot = self.boxplot_on_line(line, B, y=-0.45, color=ACCENT2, label="B")
        med_x = line.n2p(7.5)[0]
        guide = DashedLine([med_x, 1.35, 0], [med_x, -1.05, 0], color=ALERT, dash_length=0.12, stroke_width=2.5)
        med_label = self.m(r"M=7.5", 34, ALERT).next_to(guide, UP, buff=0.12)
        out_label = self.t("22 is plotted separately", 23, BOLD, ALERT).next_to([line.n2p(22)[0], -0.45, 0], UP, buff=0.22)
        stage = VGroup(line, aplot, bplot, guide, med_label, out_label)
        self.safe(stage, "same scale boxplots")
        self.play(Create(line), run_time=1.0)
        self.play(Create(aplot), run_time=1.25)
        self.play(Create(bplot), run_time=1.25)
        self.play(Create(guide), FadeIn(med_label), run_time=0.75)
        self.play(FadeIn(out_label), run_time=0.65)
        self.wait(4.6)
        self.clear_stage()

    def compare_metrics(self):
        self.set_header(5, "COMPARE ONE FEATURE AT A TIME", "Do not judge a boxplot by its total visual size. Compare center, IQR, whiskers and outliers separately.")
        cards = VGroup(
            self.metric_card("MEDIAN", "7.5", "7.5", "Same center", ALERT),
            self.metric_card("IQR", "3.5", "5.5", "A has tighter middle 50%", ACCENT),
            self.metric_card("WHISKER SPAN", "4 to 11", "3 to 14", "B has more ordinary spread", GOLD),
            self.metric_card("OUTLIERS", "none", "22", "B has one unusual high value", ACCENT2),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.48, 0.45)).move_to(DOWN * 0.45)
        conclusion = self.t("Therefore: same typical score, but Group A is more consistent.", 31, BOLD, ACCENT).to_edge(DOWN, buff=0.28)
        self.safe(VGroup(cards, conclusion), "comparison metrics")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.14), run_time=1.65)
        self.wait(2.0)
        self.play(FadeIn(conclusion, shift=UP * 0.08), run_time=0.8)
        self.wait(4.0)
        self.clear_stage()

    def outlier_meaning(self):
        self.set_header(6, "AN OUTLIER IS A FLAG, NOT AN AUTOMATIC ERROR", "The 1.5 IQR rule identifies unusual values. Interpretation still requires context.")
        formula = self.m(r"UF_B=11+1.5(5.5)=19.25", 46)
        test = self.m(r"22>19.25\Rightarrow 22\text{ is a potential outlier}", 43, ALERT)
        questions = VGroup(
            self.t("Check 1: Was 22 recorded correctly?", 27, BOLD),
            self.t("Check 2: Is 22 a real exceptional performance?", 27, BOLD),
            self.t("Check 3: Does the conclusion change with and without it?", 27, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        note = self.t("Do not delete an outlier only because it is far from the box.", 29, BOLD, ALERT)
        stage = VGroup(formula, test, questions, note).arrange(DOWN, buff=0.45).move_to(DOWN * 0.40)
        self.fit(stage, 13.8, 5.35)
        self.safe(stage, "outlier meaning")
        self.play(Write(formula), run_time=0.85)
        self.play(Write(test), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.08) for q in questions], lag_ratio=0.16), run_time=1.2)
        self.play(FadeIn(note), run_time=0.75)
        self.wait(4.5)
        self.clear_stage()

    def decision_case(self):
        self.set_header(7, "TURN THE GRAPH INTO A DECISION", "Imagine the values are completion times where a lower and more consistent result is preferred.")
        prompt = self.t("Which group would you describe as more predictable?", 35, BOLD)
        pause = self.t("PAUSE - justify with at least two boxplot features", 27, BOLD, GOLD)
        answer = VGroup(
            self.t("GROUP A is more predictable", 38, BOLD, ACCENT),
            self.t("Evidence 1: both medians are 7.5, so the typical result is the same.", 26),
            self.t("Evidence 2: A has the smaller IQR: 3.5 < 5.5.", 26),
            self.t("Evidence 3: A has no flagged high outlier.", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        pre = VGroup(prompt, pause).arrange(DOWN, buff=0.50).move_to(UP * 0.20)
        self.safe(pre, "decision prompt")
        self.play(FadeIn(prompt), run_time=0.75)
        self.play(FadeIn(pause), run_time=0.65)
        self.wait(5.5)
        self.play(FadeOut(pre), run_time=0.65)
        answer.move_to(DOWN * 0.30)
        self.safe(answer, "decision answer")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.08) for x in answer], lag_ratio=0.16), run_time=1.65)
        self.wait(4.5)
        self.clear_stage()

    def summary_scene(self):
        self.set_header(8, "CLASS 02 METHOD", "Use this six-step routine whenever you compare two distributions with boxplots.")
        steps = [
            ("1", "USE THE SAME SCALE"),
            ("2", "COMPARE MEDIANS"),
            ("3", "COMPARE IQRs"),
            ("4", "COMPARE WHISKERS"),
            ("5", "CHECK OUTLIERS"),
            ("6", "WRITE A CONTEXTUAL CONCLUSION"),
        ]
        cards = VGroup()
        for n, txt in steps:
            box = RoundedRectangle(
                width=4.25, height=1.34, corner_radius=0.13,
                stroke_color=INK, stroke_width=1.7,
                fill_color=WHITE, fill_opacity=1,
            )
            badge = Circle(radius=0.23, stroke_color=ACCENT, stroke_width=2)
            num = self.t(n, 21, BOLD, ACCENT).move_to(badge)
            label = self.t(txt, 21, BOLD)
            content = VGroup(VGroup(badge, num), label).arrange(RIGHT, buff=0.18).move_to(box)
            self.fit(content, 3.90, 0.90)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.42)).move_to(DOWN * 0.35)
        exit_q = self.t("Exit ticket: Can two groups have the same median but different consistency? Explain.", 28, BOLD).to_edge(DOWN, buff=0.27)
        self.safe(VGroup(cards, exit_q), "summary")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.10), run_time=1.75)
        self.wait(2.4)
        self.play(FadeIn(exit_q), run_time=0.80)
        self.wait(5.2)


# Preview QA:
#   manim -pql main.py Statistics10IQRClass02CompareBoxplots --disable_caching
# Final:
#   manim -pqh main.py Statistics10IQRClass02CompareBoxplots --disable_caching
