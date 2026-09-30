#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Area V6 ENGLISH MASTERCLASS.

A full visual/pacing redesign of the audited V5 two-row derivation.

Design goals after reviewing the rendered V5 video frame-by-frame:
- substantially larger circle, rows, strip, labels and equations;
- less unused white space and fewer small side panels;
- direct object-to-object transformations instead of repeated fade/rebuild cycles;
- longer reading pauses at the three conceptual checkpoints;
- explicit TWO-ROW classroom method before the rows are interlocked;
- each row is independently measured as height r and curved-edge total P/2 = pi r;
- a slow representative pair demonstrates the interlocking mechanism first;
- the final strip clearly shows shared height r (not 2r) and base P/2 (not P);
- English-only classroom language;
- clean white / black / gray projector-safe visual system.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps, H.264/yuv420p.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V5_FINAL_QA import (  # noqa: E402
    Geometry8CircleAreaTwoRows20260827V5FinalQA,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER,
)


class Geometry8CircleAreaTwoRowsEnglish20260827V6Master(Geometry8CircleAreaTwoRows20260827V5FinalQA):
    """English master version with enlarged geometry and deliberate classroom pacing."""

    # ------------------------------------------------------------------
    # Larger projector-first layout helpers
    # ------------------------------------------------------------------
    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        badge = RoundedRectangle(
            width=0.82,
            height=0.56,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 24, BOLD).move_to(badge)
        title_mob = self.text(title, 38, BOLD)
        if title_mob.width > 12.7:
            title_mob.scale_to_fit_width(12.7)
        title_mob.next_to(badge, RIGHT, buff=0.24)
        row = VGroup(VGroup(badge, badge_text), title_mob)
        row.move_to([-0.15, 4.05, 0]).align_to([-7.45, 4.05, 0], LEFT)

        rule_y = row.get_bottom()[1] - 0.11
        rule = Line([-7.45, rule_y, 0], [7.45, rule_y, 0], color=LIGHT_GRAY, stroke_width=2)

        subtitle_mob = self.text(subtitle, 25)
        if subtitle_mob.width > 14.2:
            subtitle_mob.scale_to_fit_width(14.2)
        subtitle_mob.next_to(rule, DOWN, buff=0.10).align_to(row, LEFT)
        return VGroup(row, rule, subtitle_mob)

    def big_formula(self, latex: str, width: float = 7.0, size: int = 50) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=1.28,
            corner_radius=0.14,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=PAPER,
            fill_opacity=1,
        )
        eq = self.math(latex, size)
        if eq.width > width - 0.50:
            eq.scale_to_fit_width(width - 0.50)
        eq.move_to(box)
        return VGroup(box, eq)

    def row_guides(self, rows: VGroup, top_pivot_y: float, bottom_pivot_y: float, r: float) -> VGroup:
        x0 = rows.get_left()[0] - 0.05
        x1 = rows.get_right()[0] + 0.05
        top_y = top_pivot_y + r
        bottom_y = bottom_pivot_y - r
        return VGroup(
            DashedLine([x0, top_y, 0], [x1, top_y, 0], color=LIGHT_GRAY, dash_length=0.10),
            DashedLine([x0, top_pivot_y, 0], [x1, top_pivot_y, 0], color=LIGHT_GRAY, dash_length=0.10),
            DashedLine([x0, bottom_pivot_y, 0], [x1, bottom_pivot_y, 0], color=LIGHT_GRAY, dash_length=0.10),
            DashedLine([x0, bottom_y, 0], [x1, bottom_y, 0], color=LIGHT_GRAY, dash_length=0.10),
        )

    def english_row_measurements(
        self,
        rows: VGroup,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
    ) -> VGroup:
        x0 = rows.get_left()[0]
        x1 = rows.get_right()[0]
        top_y = top_pivot_y + r
        bottom_y = bottom_pivot_y - r

        top_base = DoubleArrow(
            [x0, top_y + 0.28, 0], [x1, top_y + 0.28, 0],
            color=BLACK, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        top_base_lab = self.math(r"\frac{P}{2}=\pi r", 42).next_to(top_base, UP, buff=0.07)

        bottom_base = DoubleArrow(
            [x0, bottom_y - 0.28, 0], [x1, bottom_y - 0.28, 0],
            color=MID_GRAY, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        bottom_base_lab = self.math(r"\frac{P}{2}=\pi r", 42).next_to(bottom_base, DOWN, buff=0.07)

        xh = x1 + 0.58
        top_h = DoubleArrow(
            [xh, top_pivot_y, 0], [xh, top_y, 0],
            color=BLACK, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        top_h_lab = self.math("r", 44).next_to(top_h, RIGHT, buff=0.12)

        bottom_h = DoubleArrow(
            [xh, bottom_y, 0], [xh, bottom_pivot_y, 0],
            color=MID_GRAY, buff=0.01, tip_length=0.12, stroke_width=2.8,
        )
        bottom_h_lab = self.math("r", 44).next_to(bottom_h, RIGHT, buff=0.12)

        return VGroup(
            top_base, top_base_lab,
            bottom_base, bottom_base_lab,
            top_h, top_h_lab,
            bottom_h, bottom_h_lab,
        )

    # ------------------------------------------------------------------
    # Full English master timeline
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening_english()
        self.step_1_circle_english()
        self.step_2_cut_english()
        self.step_3_two_rows_english()
        self.step_4_measure_rows_english()
        self.step_5_interlock_english()
        self.step_6_shared_height_english()
        self.step_7_base_english()
        self.step_8_limit_english()
        self.closing_english()

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening_english(self) -> None:
        title = self.text("WHY IS THE AREA OF A CIRCLE  πr²?", 54, BOLD)
        subtitle = self.text("A visual derivation with the TWO-ROW method", 32)
        flow = self.text("CUT  →  SPLIT  →  MEASURE  →  INTERLOCK  →  AREA", 28, BOLD)
        formula = self.big_formula(r"A=\pi r^2", 5.0, 58)
        group = VGroup(title, subtitle, flow, formula).arrange(DOWN, buff=0.38)
        self.assert_safe(group, "v6 opening")

        self.play(Write(title), run_time=1.35)
        self.play(FadeIn(subtitle, shift=UP * 0.08), run_time=0.85)
        self.play(FadeIn(flow, shift=UP * 0.08), run_time=0.90)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.90)
        self.wait(3.6)
        self.clear_stage(group)

    # ------------------------------------------------------------------
    # 01 — Circle
    # ------------------------------------------------------------------
    def step_1_circle_english(self) -> None:
        h = self.header(
            1,
            "START WITH THE CIRCLE",
            "We will keep exactly the same pieces and the same area; only their position will change.",
        )
        self.add(h)

        center = np.array([-3.25, -0.20, 0.0])
        r = 2.30
        circle = Circle(radius=r, color=BLACK, stroke_width=4.2).move_to(center)
        dot = Dot(center, radius=0.075, color=BLACK)
        radius = Arrow(center, center + RIGHT * r, buff=0, color=BLACK, stroke_width=3.4, tip_length=0.18)
        r_lab = self.math("r", 46).next_to(radius, UP, buff=0.12)

        c_title = self.text("CIRCUMFERENCE", 29, BOLD)
        c_formula = self.big_formula(r"P=2\pi r", 4.9, 52)
        c_group = VGroup(c_title, c_formula).arrange(DOWN, buff=0.18).move_to([3.75, 0.65, 0])

        key1 = self.text("Same circle", 28, BOLD)
        key2 = self.text("Same pieces", 28, BOLD)
        key3 = self.text("Same total area", 28, BOLD)
        keys = VGroup(key1, key2, key3).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.55, -1.55, 0])

        g = VGroup(circle, dot, radius, r_lab, c_group, keys, h)
        self.assert_safe(g, "v6 step1")

        self.play(Create(circle), FadeIn(dot), run_time=1.05)
        self.play(GrowArrow(radius), Write(r_lab), run_time=0.90)
        self.wait(0.75)
        self.play(FadeIn(c_group, shift=LEFT * 0.12), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.06) for k in keys], lag_ratio=0.20), run_time=1.10)
        self.wait(4.0)
        self.clear_stage(VGroup(circle, dot, radius, r_lab, c_group, keys, h))

    # ------------------------------------------------------------------
    # 02 — Equal sectors, with one sector physically extracted
    # ------------------------------------------------------------------
    def step_2_cut_english(self) -> None:
        h = self.header(
            2,
            "CUT THE CIRCLE INTO EQUAL SECTORS",
            "Every sector reaches from the center to the circle, so its radial length is still r.",
        )
        self.add(h)

        n, r = 24, 2.48
        center = np.array([-1.45, -0.30, 0.0])
        sectors = self.sector_set(n, r, center)
        outline = Circle(radius=r, color=BLACK, stroke_width=3.4).move_to(center)
        count = self.big_formula(r"24\ \text{equal sectors}", 5.0, 42).move_to([4.75, 0.70, 0])
        statement = self.text("Each radial side has length  r", 30, BOLD).move_to([4.60, -0.65, 0])

        self.assert_safe(VGroup(sectors, outline, count, statement, h), "v6 step2")
        self.play(Create(outline), run_time=0.70)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.025), run_time=1.75)
        self.play(FadeIn(count, shift=LEFT * 0.10), run_time=0.75)
        self.wait(1.0)

        idx = 2
        chosen = sectors[idx]
        original = chosen.copy()
        delta = TAU / n
        mid_angle = idx * delta + delta / 2
        pull = 0.70 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
        self.play(chosen.animate.shift(pull), run_time=1.15, rate_func=smooth)

        # Radius marker placed on the extracted sector.
        pivot = center + pull
        end = pivot + r * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
        rad = DoubleArrow(pivot, end, color=BLACK, buff=0.04, tip_length=0.12, stroke_width=2.6)
        rad_lab = self.math("r", 44).next_to(rad.get_center(), UP + RIGHT, buff=0.10)
        sector_label = self.text("ONE SECTOR", 29, BOLD).move_to([4.45, -1.70, 0])
        arrow = Arrow([3.45, -1.55, 0], chosen.get_center() + RIGHT * 0.15, color=MID_GRAY, stroke_width=2.5, tip_length=0.14)
        self.play(GrowFromCenter(rad), Write(rad_lab), FadeIn(statement), FadeIn(sector_label), GrowArrow(arrow), run_time=1.00)
        self.wait(3.8)
        self.play(FadeOut(rad), FadeOut(rad_lab), FadeOut(sector_label), FadeOut(arrow), chosen.animate.become(original), run_time=0.85)
        self.wait(0.6)
        self.clear_stage(VGroup(sectors, outline, count, statement, h))

    # ------------------------------------------------------------------
    # 03 — Direct circle-to-two-row transformation
    # ------------------------------------------------------------------
    def step_3_two_rows_english(self) -> None:
        h = self.header(
            3,
            "SPLIT ALTERNATING SECTORS INTO TWO ROWS",
            "Half of the sectors become ROW 1; the alternating half become ROW 2.",
        )
        self.add(h)

        n, r = 24, 1.90
        source = self.sector_set(n, r, np.array([0.0, -0.18, 0.0]))
        outline = Circle(radius=r, color=BLACK, stroke_width=3.2).move_to([0.0, -0.18, 0.0])
        top_y, bottom_y = 0.74, -0.74
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        row1 = self.text("ROW 1", 34, BOLD).move_to([-5.65, 1.45, 0])
        row2 = self.text("ROW 2", 34, BOLD).move_to([-5.65, -1.45, 0])
        split = self.big_formula(r"24\ \text{sectors}\;\longrightarrow\;12+12", 6.2, 43).move_to([4.20, -2.65, 0])

        self.assert_safe(VGroup(source, outline, rows, row1, row2, split, h), "v6 step3")
        self.play(Create(outline), LaggedStart(*[FadeIn(s) for s in source], lag_ratio=0.015), run_time=1.30)
        self.wait(1.0)
        self.play(FadeOut(outline), run_time=0.30)

        # Slight stagger by parity makes the split readable without producing a crossing fan.
        even_anims = [Transform(source[i], rows[i]) for i in range(0, n, 2)]
        odd_anims = [Transform(source[i], rows[i]) for i in range(1, n, 2)]
        self.play(AnimationGroup(*even_anims, lag_ratio=0.025), FadeIn(row1, shift=RIGHT * 0.10), run_time=1.65, rate_func=smooth)
        self.play(AnimationGroup(*odd_anims, lag_ratio=0.025), FadeIn(row2, shift=RIGHT * 0.10), run_time=1.65, rate_func=smooth)
        self.play(FadeIn(split, shift=UP * 0.08), run_time=0.75)
        self.wait(4.0)
        self.clear_stage(VGroup(source, row1, row2, split, h))

    # ------------------------------------------------------------------
    # 04 — Measure EACH row separately, at a large scale
    # ------------------------------------------------------------------
    def step_4_measure_rows_english(self) -> None:
        h = self.header(
            4,
            "MEASURE ROW 1 AND ROW 2 BEFORE INTERLOCKING",
            "For each row: radial height = r, while the curved-edge total = half the perimeter = P/2.",
        )
        self.add(h)

        n, r = 24, 1.72
        top_y, bottom_y = 0.62, -0.62
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        arcs_top, arcs_bottom = self.row_boundary_arcs(n, r, top_y, bottom_y)
        measures = self.english_row_measurements(rows, r, top_y, bottom_y)
        guides = self.row_guides(rows, top_y, bottom_y, r)
        row1 = self.text("ROW 1", 33, BOLD).move_to([-5.65, 1.30, 0])
        row2 = self.text("ROW 2", 33, BOLD).move_to([-5.65, -1.30, 0])

        self.assert_safe(VGroup(rows, arcs_top, arcs_bottom, measures, guides, row1, row2, h), "v6 step4")
        self.play(FadeIn(rows), FadeIn(row1), FadeIn(row2), FadeIn(guides), run_time=0.85)
        self.wait(0.8)

        # ROW 1 is measured first and left visible.
        self.play(LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.035), run_time=1.10)
        self.play(
            GrowFromCenter(measures[0]), Write(measures[1]),
            GrowFromCenter(measures[4]), Write(measures[5]),
            run_time=1.15,
        )
        row1_note = self.text("ROW 1:  height r   •   curved edge P/2 = πr", 29, BOLD).move_to([0.0, -3.25, 0])
        self.play(FadeIn(row1_note, shift=UP * 0.06), run_time=0.65)
        self.wait(3.2)

        # ROW 2 repeats the exact same logic.
        self.play(LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.035), run_time=1.10)
        self.play(
            GrowFromCenter(measures[2]), Write(measures[3]),
            GrowFromCenter(measures[6]), Write(measures[7]),
            run_time=1.15,
        )
        row2_note = self.text("ROW 2:  height r   •   curved edge P/2 = πr", 29, BOLD).move_to([0.0, -3.70, 0])
        self.play(FadeIn(row2_note, shift=UP * 0.06), run_time=0.65)
        self.wait(4.2)

        self.clear_stage(VGroup(rows, arcs_top, arcs_bottom, measures, guides, row1, row2, row1_note, row2_note, h))

    # ------------------------------------------------------------------
    # 05 — One pair first, then all pieces with a soft cascade
    # ------------------------------------------------------------------
    def step_5_interlock_english(self) -> None:
        h = self.header(
            5,
            "INTERLOCK THE TWO ROWS",
            "ROW 1 moves down and ROW 2 moves up; their tips fill the opposite gaps.",
        )
        self.add(h)

        n, r = 24, 2.00
        top_y, bottom_y = 0.78, -0.78
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        target = self.strip_targets(n, r, center=np.array([0.0, -0.10, 0.0]))
        row1 = self.text("ROW 1   ↓", 34, BOLD).move_to([-5.75, 1.60, 0])
        row2 = self.text("ROW 2   ↑", 34, BOLD).move_to([-5.75, -1.60, 0])
        band_top = DashedLine([-3.85, 0.90, 0], [3.85, 0.90, 0], color=LIGHT_GRAY, dash_length=0.10)
        band_bottom = DashedLine([-3.85, -1.10, 0], [3.85, -1.10, 0], color=LIGHT_GRAY, dash_length=0.10)
        first = self.text("FIRST: WATCH ONE PAIR", 30, BOLD).move_to([0.0, -3.12, 0])

        self.assert_safe(VGroup(rows, target, row1, row2, band_top, band_bottom, first, h), "v6 step5")
        self.play(FadeIn(rows), FadeIn(row1), FadeIn(row2), run_time=0.85)
        self.play(Create(band_top), Create(band_bottom), FadeIn(first, shift=UP * 0.06), run_time=0.70)

        pair = (10, 11)
        self.play(
            Indicate(rows[pair[0]], color=MID_GRAY, scale_factor=1.10),
            Indicate(rows[pair[1]], color=MID_GRAY, scale_factor=1.10),
            run_time=1.05,
        )
        self.wait(0.75)
        self.play(
            Transform(rows[pair[0]], target[pair[0]]),
            Transform(rows[pair[1]], target[pair[1]]),
            run_time=1.70,
            rate_func=smooth,
        )
        self.wait(1.2)

        repeat = self.text("NOW REPEAT THE SAME MOTION WITH EVERY PAIR", 29, BOLD).move_to(first)
        self.play(Transform(first, repeat), run_time=0.55)
        remaining = [i for i in range(n) if i not in pair]
        ordered = sorted(remaining, key=lambda i: abs(i - 11.5))
        self.play(
            LaggedStart(*[Transform(rows[i], target[i]) for i in ordered], lag_ratio=0.035),
            FadeOut(row1), FadeOut(row2),
            run_time=3.10,
            rate_func=smooth,
        )
        self.play(FadeOut(first), run_time=0.35)
        same_area = self.text("SAME PIECES  →  SAME TOTAL AREA", 32, BOLD).move_to([0.0, -3.15, 0])
        self.play(FadeIn(same_area, shift=UP * 0.08), run_time=0.70)
        self.wait(4.0)
        self.clear_stage(VGroup(rows, band_top, band_bottom, same_area, h))

    # ------------------------------------------------------------------
    # 06 — Shared height r, not 2r
    # ------------------------------------------------------------------
    def step_6_shared_height_english(self) -> None:
        h = self.header(
            6,
            "THE TWO ROWS SHARE ONE HEIGHT:  r",
            "The rows interlock inside the same vertical band; they are not stacked one above the other.",
        )
        self.add(h)

        n, r = 32, 2.15
        strip = self.strip_targets(n, r, center=np.array([-0.55, -0.10, 0.0]))
        top_y = -0.10 + r / 2
        bottom_y = -0.10 - r / 2
        top = DashedLine([-4.50, top_y, 0], [4.00, top_y, 0], color=MID_GRAY, dash_length=0.10)
        bottom = DashedLine([-4.50, bottom_y, 0], [4.00, bottom_y, 0], color=MID_GRAY, dash_length=0.10)
        height = DoubleArrow([4.35, bottom_y, 0], [4.35, top_y, 0], color=BLACK, buff=0.02, tip_length=0.14, stroke_width=3.0)
        h_lab = self.math("r", 52).next_to(height, RIGHT, buff=0.16)

        row1_tag = self.text("ROW 1 pieces", 28, BOLD).move_to([-5.45, 0.68, 0])
        row2_tag = self.text("ROW 2 pieces", 28, BOLD).move_to([-5.45, -0.88, 0])
        arrows1 = VGroup(*[
            Arrow([-4.55, 0.60, 0], strip[i].get_center(), color=MID_GRAY, stroke_width=1.8, tip_length=0.10)
            for i in (4, 10, 16)
        ])
        arrows2 = VGroup(*[
            Arrow([-4.55, -0.80, 0], strip[i].get_center(), color=MID_GRAY, stroke_width=1.8, tip_length=0.10)
            for i in (5, 11, 17)
        ])
        key = self.big_formula(r"\text{height}=r\qquad\text{NOT}\qquad 2r", 7.4, 47).move_to([0.0, -3.12, 0])

        self.assert_safe(VGroup(strip, top, bottom, height, h_lab, row1_tag, row2_tag, arrows1, arrows2, key, h), "v6 step6")
        self.play(FadeIn(strip), run_time=0.85)
        self.play(Create(top), Create(bottom), run_time=0.65)
        self.play(FadeIn(row1_tag), FadeIn(row2_tag), LaggedStart(*[GrowArrow(a) for a in arrows1], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in arrows2], lag_ratio=0.15), run_time=1.10)
        self.wait(1.4)
        self.play(GrowFromCenter(height), Write(h_lab), run_time=1.00)
        self.play(FadeIn(key, shift=UP * 0.08), run_time=0.75)
        self.wait(5.0)
        self.clear_stage(VGroup(strip, top, bottom, height, h_lab, row1_tag, row2_tag, arrows1, arrows2, key, h))

    # ------------------------------------------------------------------
    # 07 — Base P/2, not P
    # ------------------------------------------------------------------
    def step_7_base_english(self) -> None:
        h = self.header(
            7,
            "THE BASE IS HALF THE PERIMETER",
            "ROW 1 forms one long boundary and ROW 2 forms the opposite boundary; one base uses only one of them.",
        )
        self.add(h)

        n, r = 32, 2.05
        strip = self.strip_targets(n, r, center=np.array([-1.15, -0.08, 0.0]))
        arcs_top, arcs_bottom = self.final_row_arc_overlays(n, r, center_y=-0.08)
        arcs_top.shift(LEFT * 1.15)
        arcs_bottom.shift(LEFT * 1.15)
        x0, x1 = strip.get_left()[0], strip.get_right()[0]
        base = DoubleArrow([x0, -1.52, 0], [x1, -1.52, 0], color=BLACK, buff=0.02, tip_length=0.14, stroke_width=3.0)
        base_lab = self.math(r"\text{base}=\frac{P}{2}=\pi r", 46).next_to(base, DOWN, buff=0.10)

        row1 = self.text("ROW 1 boundary  =  P/2", 29, BOLD).move_to([4.85, 0.70, 0])
        row2 = self.text("ROW 2 boundary  =  P/2", 29, BOLD).move_to([4.85, -0.15, 0])
        notsum = self.text("Choose ONE boundary for the base — do not add them.", 27, BOLD).move_to([3.25, -2.55, 0])

        self.assert_safe(VGroup(strip, arcs_top, arcs_bottom, base, base_lab, row1, row2, notsum, h), "v6 step7")
        self.play(FadeIn(strip), run_time=0.80)
        self.play(LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.035), FadeIn(row1, shift=LEFT * 0.08), run_time=1.15)
        self.wait(1.0)
        self.play(LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.035), FadeIn(row2, shift=LEFT * 0.08), run_time=1.15)
        self.wait(1.1)
        self.play(GrowFromCenter(base), Write(base_lab), run_time=1.10)
        self.play(FadeIn(notsum, shift=UP * 0.06), run_time=0.70)
        self.wait(5.0)
        self.clear_stage(VGroup(strip, arcs_top, arcs_bottom, base, base_lab, row1, row2, notsum, h))

    # ------------------------------------------------------------------
    # 08 — More sectors, straighter edge, exact rectangle limit
    # ------------------------------------------------------------------
    def step_8_limit_english(self) -> None:
        h = self.header(
            8,
            "MORE SECTORS → STRAIGHTER EDGES → EXACT AREA",
            "As sectors become thinner, the interlocked strip approaches a rectangle with base πr and height r.",
        )
        self.add(h)

        r = 2.05
        coarse = self.strip_targets(12, r, center=np.array([0.0, -0.10, 0.0]))
        medium = self.strip_targets(24, r, center=np.array([0.0, -0.10, 0.0]))
        fine = self.strip_targets(64, r, center=np.array([0.0, -0.10, 0.0]))
        label = self.text("12 sectors", 32, BOLD).move_to([0.0, 2.15, 0])

        self.assert_safe(VGroup(coarse, medium, fine, label, h), "v6 step8a")
        self.play(FadeIn(coarse), FadeIn(label), run_time=0.80)
        self.wait(1.3)
        l24 = self.text("24 sectors", 32, BOLD).move_to(label)
        self.play(Transform(coarse, medium), Transform(label, l24), run_time=1.45, rate_func=smooth)
        self.wait(1.3)
        l64 = self.text("64 sectors", 32, BOLD).move_to(label)
        self.play(Transform(coarse, fine), Transform(label, l64), run_time=1.60, rate_func=smooth)
        self.wait(1.8)

        # Rectangle guide around the limiting strip.
        rect = Rectangle(width=PI * r, height=r, color=MID_GRAY, stroke_width=2.8).move_to([0.0, -0.10, 0.0])
        base = DoubleArrow([-PI*r/2, -1.50, 0], [PI*r/2, -1.50, 0], color=BLACK, buff=0.02, tip_length=0.13, stroke_width=2.8)
        base_lab = self.math(r"\pi r", 44).next_to(base, DOWN, buff=0.09)
        height = DoubleArrow([3.55, -1.125, 0], [3.55, 0.925, 0], color=BLACK, buff=0.02, tip_length=0.13, stroke_width=2.8)
        height_lab = self.math("r", 44).next_to(height, RIGHT, buff=0.12)
        self.play(Create(rect), GrowFromCenter(base), Write(base_lab), GrowFromCenter(height), Write(height_lab), run_time=1.10)
        self.wait(2.2)

        equation = self.big_formula(r"A=(\pi r)(r)=\pi r^2", 7.2, 54).move_to([0.0, -3.10, 0])
        self.play(FadeIn(equation, shift=UP * 0.10), run_time=0.80)
        self.wait(4.5)

        self.play(
            FadeOut(coarse), FadeOut(label), FadeOut(rect), FadeOut(base), FadeOut(base_lab),
            FadeOut(height), FadeOut(height_lab), FadeOut(h),
            equation.animate.move_to([0.0, 0.0, 0]).scale(1.18),
            run_time=1.10,
        )
        final_title = self.text("AREA OF A CIRCLE", 40, BOLD).move_to([0.0, 1.25, 0])
        self.play(FadeIn(final_title, shift=UP * 0.08), run_time=0.70)
        self.wait(4.5)
        self.clear_stage(VGroup(equation, final_title))

    # ------------------------------------------------------------------
    # Closing notebook checkpoint
    # ------------------------------------------------------------------
    def closing_english(self) -> None:
        title = self.text("TWO-ROW METHOD — NOTEBOOK SUMMARY", 42, BOLD)
        lines = VGroup(
            self.text("1. Cut the circle into equal sectors.", 31),
            self.text("2. Put alternating sectors into ROW 1 and ROW 2.", 31),
            self.text("3. Each row has radial height  r  and curved-edge total  P/2 = πr.", 31),
            self.text("4. Interlock the rows: they share the same height  r.", 31),
            self.text("5. One long boundary becomes the base:  P/2 = πr.", 31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        formula = self.big_formula(r"A=(\pi r)(r)=\pi r^2", 7.0, 54)
        group = VGroup(title, lines, formula).arrange(DOWN, buff=0.42)
        if group.height > 7.6:
            group.scale_to_fit_height(7.6)
        self.assert_safe(group, "v6 closing")

        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.80)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.08) for line in lines], lag_ratio=0.18), run_time=2.25)
        self.wait(2.0)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.85)
        self.wait(6.0)


# Preview:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_TWO_ROWS_ENGLISH_20260827_V6_MASTER.py Geometry8CircleAreaTwoRowsEnglish20260827V6Master --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_TWO_ROWS_ENGLISH_20260827_V6_MASTER.py Geometry8CircleAreaTwoRowsEnglish20260827V6Master --disable_caching
