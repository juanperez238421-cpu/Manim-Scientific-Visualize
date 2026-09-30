#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — From measured circles to circumference and area.

Pedagogical continuation of the audited Circle Fundamentals / Class 2 / Workshop
sequence.  The lesson starts from the students' previous homework: measure three
real circular objects, record diameter d and circumference C, and compare C/d.

The displayed measurements are explicitly illustrative; students should compare
them with their own three objects.

Target: Manim Community Edition 0.20.1
Style: JP Classroom monochrome 16:9 / 1920x1080 / 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA_V2 import (
    Geometry8CirclePedagogicalSequenceSeniorQAV2,
)
from jp_classroom_style import *


SAMPLE_DATA = [
    ("Object A", 8.0, 25.1),
    ("Object B", 10.0, 31.4),
    ("Object C", 6.5, 20.4),
]
SAMPLE_RATIOS = [c / d for _, d, c in SAMPLE_DATA]
SAMPLE_MEAN = sum(SAMPLE_RATIOS) / len(SAMPLE_RATIOS)


class Geometry8CircleMeasurementArea20260823(
    Geometry8CirclePedagogicalSequenceSeniorQAV2
):
    """Homework evidence -> pi -> circumference -> area -> integrated practice."""

    def validate_lesson_data(self) -> None:
        # The experimental values are intentionally realistic, not perfectly pi.
        assert all(3.0 < value < 3.3 for value in SAMPLE_RATIOS)
        assert abs(SAMPLE_MEAN - 3.138653846153846) < 1e-12

        # Displayed worked examples.
        assert abs(12 * math.pi - 37.69911184307752) < 1e-12
        assert abs(14 * math.pi - 43.982297150257104) < 1e-12
        assert abs(25 * math.pi - 78.53981633974483) < 1e-12
        assert abs(49 * math.pi - 153.93804002589985) < 1e-12
        assert abs(31.4 / 3.14 - 10.0) < 1e-12

    def construct(self) -> None:
        self.opening_measurement_bridge()
        self.homework_measurements()
        self.discover_pi()
        self.elements_radius_diameter()
        self.circumference_worked_example()
        self.boundary_vs_surface()
        self.derive_area_visually()
        self.area_worked_example()
        self.integrated_exercises()
        self.lesson_summary()

    def opening_measurement_bridge(self) -> None:
        self.standard_opening(
            "GEOMETRY 8",
            "CIRCLES — FROM MEASUREMENT TO AREA",
            "Use real measurements to discover pi, calculate circumference, and introduce circle area.",
            "Measure first. Find the pattern. Then choose the correct measurement.",
        )

    def homework_measurements(self) -> None:
        self.set_header(
            1,
            "START WITH YOUR THREE REAL OBJECTS",
            "Last class: measure diameter d and circumference C, then compare the ratio C / d.",
        )

        task = self.note_panel(
            "HOMEWORK RECAP",
            [
                "1. Choose 3 circular objects.",
                "2. Measure diameter d.",
                "3. Measure circumference C.",
                "4. Calculate C / d for each object.",
            ],
            width=4.95,
            title_size=28,
            body_size=25,
            max_text_height=3.05,
        )

        rows = []
        for name, d, c in SAMPLE_DATA:
            rows.append([name, f"{d:.1f}", f"{c:.1f}", f"{c/d:.3f}"])
        table = self.build_table(
            headers=("Object", "d (cm)", "C (cm)", "C / d"),
            body_rows=rows,
            column_widths=(2.05, 1.60, 1.70, 1.70),
            math_columns=(1, 2, 3),
            row_height=0.68,
            header_height=0.76,
            body_font_size=26,
            header_font_size=24,
        )
        table.group.scale(0.98)

        label = self.text("Illustrative measurements — compare with your own data", 21)
        right = VGroup(table.group, label).arrange(DOWN, buff=0.22)
        layout = self.split_layout(task, right, gap=0.50, center_y=-0.40)
        self.assert_content_safe(layout.group, "homework measurement layout")

        self.play(FadeIn(task), run_time=RUN_NORMAL)
        self.animate_table_rows(table, include_header=True)
        self.play(FadeIn(label), run_time=RUN_QUICK)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def discover_pi(self) -> None:
        self.set_header(
            2,
            "THE RATIO STAYS ALMOST THE SAME",
            "Different circles give nearly the same quotient; small differences come from measurement error.",
        )

        circles = VGroup()
        radii = [0.68, 0.92, 1.18]
        x_positions = [-5.5, -3.0, -0.15]
        names = ["A", "B", "C"]
        for r, x, name, ratio in zip(radii, x_positions, names, SAMPLE_RATIOS):
            circ = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=3.5)
            circ.move_to([x, -0.15, 0])
            diameter = Line(circ.get_left(), circ.get_right(), color=BLACK_LINE, stroke_width=2.5)
            center = Dot(circ.get_center(), radius=0.045, color=BLACK_LINE)
            ratio_text = self.math(rf"\frac{{C}}{{d}}\approx {ratio:.3f}", 30)
            ratio_text.next_to(circ, DOWN, buff=0.22)
            name_text = self.text(f"OBJECT {name}", 21, BOLD).next_to(circ, UP, buff=0.18)
            circles.add(VGroup(circ, diameter, center, ratio_text, name_text))

        mean_panel = VGroup(
            self.formula_panel(
                rf"\text{{mean ratio}}\approx {SAMPLE_MEAN:.3f}",
                width=5.2,
                height=1.02,
                font_size=36,
            ),
            self.formula_panel(
                r"\pi=3.14159\ldots",
                width=5.2,
                height=1.02,
                font_size=42,
            ),
            self.note_panel(
                "EXPERIMENTAL IDEA",
                ["For every circle: circumference is about 3.14 diameters long."],
                width=5.2,
                title_size=25,
                body_size=23,
                max_text_height=1.15,
            ),
        ).arrange(DOWN, buff=0.22)
        mean_panel.move_to(RIGHT * 4.3 + DOWN * 0.35)

        group = VGroup(circles, mean_panel)
        self.assert_content_safe(group, "pi discovery layout")
        self.play(
            LaggedStart(*[FadeIn(item, shift=UP * 0.08) for item in circles], lag_ratio=0.18),
            run_time=RUN_SLOW * 1.4,
        )
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(mean_panel[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(mean_panel[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(mean_panel[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def elements_radius_diameter(self) -> None:
        self.set_header(
            3,
            "CENTER, RADIUS, DIAMETER, CIRCUMFERENCE",
            "These four elements connect the physical measurement to the formulas.",
        )

        center = np.array([-3.7, -0.45, 0.0])
        radius = 1.82
        circ = self._circle(center, radius=radius)
        o = Dot(center, radius=0.055, color=BLACK_LINE)
        r_line = Line(center, center + RIGHT * radius, color=BLACK_LINE, stroke_width=4)
        d_line = Line(center + LEFT * radius, center + RIGHT * radius, color=MID_GRAY, stroke_width=3)
        r_lab = self.math("r", 38).next_to(r_line, UP, buff=0.10)
        d_lab = self.math("d", 38).next_to(d_line, DOWN, buff=0.12)
        o_lab = self.math("O", 30).next_to(o, UL, buff=0.10)
        c_lab = self.text("circumference", 23, BOLD).next_to(circ, LEFT, buff=0.20)
        figure = VGroup(circ, d_line, r_line, o, r_lab, d_lab, o_lab, c_lab)
        fig_panel = self.figure_panel(
            figure,
            width=6.8,
            height=4.7,
            title="THE MEASURABLE CIRCLE",
            caption="Diameter passes through the center; radius is half the diameter.",
        )

        equations = VGroup(
            self.formula_panel(r"d=2r", width=5.5, height=1.02, font_size=44),
            self.formula_panel(r"\frac{C}{d}=\pi", width=5.5, height=1.02, font_size=44),
            self.formula_panel(r"C=\pi d=2\pi r", width=5.5, height=1.05, font_size=42),
        ).arrange(DOWN, buff=0.28)

        layout = self.split_layout(fig_panel.group, equations, gap=0.55, center_y=-0.40)
        self.assert_content_safe(layout.group, "circle elements layout")
        self.play(FadeIn(fig_panel.group), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        for panel in equations:
            self.play(FadeIn(panel), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.clear_stage()

    def circumference_worked_example(self) -> None:
        self.set_header(
            4,
            "WORKED EXAMPLE — CIRCUMFERENCE (PERIMETER)",
            "When the question asks for the distance around the circle, the answer uses linear units.",
        )

        circle = Circle(radius=1.62, stroke_color=BLACK_LINE, stroke_width=6)
        diameter = Line(circle.get_left(), circle.get_right(), color=BLACK_LINE, stroke_width=3)
        d_label = self.math(r"d=12\text{ cm}", 34).next_to(diameter, DOWN, buff=0.14)
        visual = VGroup(circle, diameter, d_label)
        fig_panel = self.figure_panel(
            visual,
            width=6.2,
            height=4.45,
            title="DISTANCE AROUND THE EDGE",
            caption="The circumference is the perimeter of a circle.",
        )

        stack = self.equation_stack(
            [
                r"d=12\text{ cm}",
                r"C=\pi d",
                r"C=12\pi\text{ cm}",
                r"C\approx 37.7\text{ cm}",
            ],
            sizes=[38, 42, 42, 46],
            max_width=5.8,
            buff=0.34,
        )
        check = self.note_panel(
            "UNIT CHECK",
            ["Circumference measures length, so the unit is cm — not cm²."],
            width=5.8,
            title_size=25,
            body_size=23,
            max_text_height=1.15,
        )
        right = VGroup(stack, check).arrange(DOWN, buff=0.30)
        layout = self.split_layout(fig_panel.group, right, gap=0.55, center_y=-0.40)
        self.assert_content_safe(layout.group, "circumference example")

        self.play(FadeIn(fig_panel.group), run_time=RUN_NORMAL)
        self.animate_equation_stack(stack, pause=PAUSE_READ)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def boundary_vs_surface(self) -> None:
        self.set_header(
            5,
            "THE NEXT QUESTION: AROUND OR INSIDE?",
            "Circumference measures the boundary; area measures the region covered by the circle.",
        )

        left_circle = Circle(radius=1.45, stroke_color=BLACK_LINE, stroke_width=7)
        left_title = self.text("BOUNDARY LENGTH", 29, BOLD)
        left_unit = self.math(r"C\;\rightarrow\;\text{cm, m, ...}", 34)
        left = VGroup(left_title, left_circle, left_unit).arrange(DOWN, buff=0.26)

        right_circle = Circle(
            radius=1.45,
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.72,
        )
        right_title = self.text("COVERED REGION", 29, BOLD)
        right_unit = self.math(r"A\;\rightarrow\;\text{cm}^2,\text{ m}^2, ...", 34)
        right = VGroup(right_title, right_circle, right_unit).arrange(DOWN, buff=0.26)

        comparison = VGroup(left, right).arrange(RIGHT, buff=2.20).move_to(DOWN * 0.30)
        question = self.note_panel(
            "BEFORE CALCULATING",
            ["Ask: am I measuring the edge, or covering the inside?"],
            width=9.2,
            title_size=27,
            body_size=25,
            max_text_height=1.12,
        ).to_edge(DOWN, buff=0.42)

        group = VGroup(comparison, question)
        self.assert_content_safe(group, "boundary versus surface")
        self.play(FadeIn(left), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(right), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def derive_area_visually(self) -> None:
        self.set_header(
            6,
            "WHY DOES THE AREA FORMULA CONTAIN pi?",
            "Slice the circle into many thin sectors and rearrange them into an almost-rectangle.",
        )

        r = 1.65
        center = np.array([-3.85, -0.35, 0.0])
        sectors = VGroup()
        n = 16
        for i in range(n):
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=TAU / n,
                start_angle=i * TAU / n,
                stroke_color=BLACK_LINE,
                stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1.0,
            ).move_to(center)
            sectors.add(sector)
        radius_line = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=3)
        radius_label = self.math("r", 34).next_to(radius_line, UP, buff=0.08)
        sliced = VGroup(sectors, radius_line, radius_label)

        arrow = Arrow(LEFT * 0.2, RIGHT * 1.2, color=BLACK_LINE, stroke_width=3, buff=0)
        arrow.move_to([0.0, -0.25, 0])

        almost_rect = Polygon(
            [-2.65, -1.10, 0],
            [2.45, -1.10, 0],
            [2.75, 1.10, 0],
            [-2.35, 1.10, 0],
            stroke_color=BLACK_LINE,
            stroke_width=3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.85,
        ).scale(0.84).move_to([3.75, -0.25, 0])
        teeth = VGroup()
        top_y = almost_rect.get_top()[1]
        bottom_y = almost_rect.get_bottom()[1]
        x0 = almost_rect.get_left()[0] + 0.35
        x1 = almost_rect.get_right()[0] - 0.35
        xs = np.linspace(x0, x1, 10)
        for x in xs:
            teeth.add(Line([x, bottom_y, 0], [x + 0.18, top_y, 0], color=LIGHT_GRAY, stroke_width=1.5))
        base_label = self.math(r"\text{base}\approx\pi r", 32).next_to(almost_rect, DOWN, buff=0.16)
        height_line = DoubleArrow(
            almost_rect.get_right() + RIGHT * 0.22 + DOWN * 0.78,
            almost_rect.get_right() + RIGHT * 0.22 + UP * 0.78,
            color=BLACK_LINE,
            stroke_width=2.2,
            buff=0.0,
            tip_length=0.12,
        )
        height_label = self.math("r", 32).next_to(height_line, RIGHT, buff=0.10)
        rearranged = VGroup(almost_rect, teeth, base_label, height_line, height_label)

        formula = self.formula_panel(
            r"A\approx (\pi r)(r)\quad\Longrightarrow\quad A=\pi r^2",
            width=9.3,
            height=1.12,
            font_size=40,
        ).to_edge(DOWN, buff=0.42)

        group = VGroup(sliced, arrow, rearranged, formula)
        self.assert_content_safe(group, "area derivation")
        self.play(FadeIn(sliced), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(GrowArrow(arrow), run_time=RUN_NORMAL)
        self.play(FadeIn(rearranged), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def area_worked_example(self) -> None:
        self.set_header(
            7,
            "WORKED EXAMPLE — AREA",
            "When the question asks how much surface is covered, square the radius and use square units.",
        )

        circle = Circle(
            radius=1.58,
            stroke_color=BLACK_LINE,
            stroke_width=3.5,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.68,
        )
        radius = Line(circle.get_center(), circle.get_right(), color=BLACK_LINE, stroke_width=4)
        label = self.math(r"r=5\text{ cm}", 34).next_to(radius, UP, buff=0.12)
        visual = VGroup(circle, radius, label)
        fig_panel = self.figure_panel(
            visual,
            width=6.2,
            height=4.45,
            title="SURFACE INSIDE THE CIRCLE",
            caption="Radius is the required input for A = pi r².",
        )

        stack = self.equation_stack(
            [
                r"r=5\text{ cm}",
                r"A=\pi r^2",
                r"A=\pi(5)^2",
                r"A=25\pi\text{ cm}^2",
                r"A\approx 78.5\text{ cm}^2",
            ],
            sizes=[36, 42, 42, 42, 46],
            max_width=5.8,
            buff=0.28,
        )
        check = self.note_panel(
            "UNIT CHECK",
            ["Area measures two dimensions, so the unit is squared: cm²."],
            width=5.8,
            title_size=25,
            body_size=23,
            max_text_height=1.15,
        )
        right = VGroup(stack, check).arrange(DOWN, buff=0.25)
        layout = self.split_layout(fig_panel.group, right, gap=0.55, center_y=-0.40)
        self.assert_content_safe(layout.group, "area example")

        self.play(FadeIn(fig_panel.group), run_time=RUN_NORMAL)
        self.animate_equation_stack(stack, pause=PAUSE_READ)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def _exercise_state(self, number: int, title: str, prompt: str) -> VGroup:
        holder = RoundedRectangle(
            width=12.2,
            height=3.25,
            corner_radius=0.14,
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        index = self.text(f"EXERCISE {number}", 25, BOLD)
        heading = self.text(title, 35, BOLD)
        body = self.text(prompt, 30)
        self.fit(body, 10.8, 0.85)
        content = VGroup(index, heading, body).arrange(DOWN, buff=0.25).move_to(holder)
        return VGroup(holder, content)

    def integrated_exercises(self) -> None:
        self.set_header(
            8,
            "GUIDED PRACTICE — CHOOSE, CALCULATE, CHECK",
            "Do not start with a formula. First identify what the question is measuring.",
        )

        exercises = [
            (
                "DIAMETER GIVEN",
                "A circular lid has diameter 14 cm. Find r, circumference C, and area A.",
                VGroup(
                    self.math(r"r=7\text{ cm}", 38),
                    self.math(r"C=14\pi\approx 44.0\text{ cm}", 38),
                    self.math(r"A=49\pi\approx 153.9\text{ cm}^2", 38),
                ).arrange(DOWN, buff=0.20),
            ),
            (
                "CIRCUMFERENCE GIVEN",
                "A round table has C = 31.4 cm. Using pi ≈ 3.14, estimate d, r, and A.",
                VGroup(
                    self.math(r"d=\frac{C}{\pi}=10\text{ cm}", 38),
                    self.math(r"r=5\text{ cm}", 38),
                    self.math(r"A\approx 78.5\text{ cm}^2", 38),
                ).arrange(DOWN, buff=0.20),
            ),
            (
                "FORMULA CHOICE",
                "A circular garden needs a fence and grass seed. Which measurement is used for each?",
                VGroup(
                    self.text("Fence → circumference (boundary length)", 31, BOLD),
                    self.text("Grass seed → area (covered region)", 31, BOLD),
                ).arrange(DOWN, buff=0.28),
            ),
        ]

        for idx, (title, prompt, answer) in enumerate(exercises, start=1):
            card = self._exercise_state(idx, title, prompt).move_to(UP * 0.50)
            answer_box = RoundedRectangle(
                width=10.8,
                height=2.20,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=1.8,
                fill_color=PAPER_GRAY,
                fill_opacity=1.0,
            ).move_to(DOWN * 2.25)
            answer.move_to(answer_box)
            self.fit(answer, 9.9, 1.65)
            answer_group = VGroup(answer_box, answer)
            self.assert_content_safe(VGroup(card, answer_group), f"integrated exercise {idx}")

            self.play(FadeIn(card), run_time=RUN_NORMAL)
            self.wait(5.0)
            self.play(FadeIn(answer_group, shift=UP * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN)
            self.play(FadeOut(card), FadeOut(answer_group), run_time=RUN_NORMAL)

        self.clear_stage()

    def lesson_summary(self) -> None:
        self.set_header(
            9,
            "METHOD MAP — FROM A REAL OBJECT TO AREA",
            "Use this route with any of the three objects you measured at home.",
        )

        route = self.process_map(
            [
                ("1", "MEASURE d AND C"),
                ("2", "CALCULATE C / d"),
                ("3", "RECOGNIZE pi"),
                ("4", "FIND r = d / 2"),
                ("5", "CHOOSE C OR A"),
                ("6", "CHECK THE UNITS"),
            ],
            columns=3,
        )
        self.fit(route, 13.2, 3.25)
        route.move_to(UP * 0.22)

        extension = self.note_panel(
            "USE YOUR OWN DATA",
            [
                "Pick one of your three objects.",
                "Use its measured diameter to predict C and calculate A.",
                "Compare predicted C with the circumference you actually measured.",
            ],
            width=10.8,
            title_size=28,
            body_size=25,
            max_text_height=1.90,
        ).to_edge(DOWN, buff=0.38)

        group = VGroup(route, extension)
        self.assert_content_safe(group, "lesson summary")
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.8,
        )
        self.wait(PAUSE_WORK)
        self.play(FadeIn(extension), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing(
            "Measure the circle. Discover pi. Decide: boundary or surface. Then calculate."
        )


# Preview QA:
# LESSON_TIME_SCALE=0.08 manim -pql \
#   Geometry8_Circle_Measurement_To_Area_20260823.py \
#   Geometry8CircleMeasurementArea20260823 \
#   --fps 15 --disable_caching
#
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh \
#   Geometry8_Circle_Measurement_To_Area_20260823.py \
#   Geometry8CircleMeasurementArea20260823 \
#   --fps 30 --disable_caching
