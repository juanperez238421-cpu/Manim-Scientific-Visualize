#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Exercises: area, perimeter, diameter and fractional regions.

Workshop-style presentation built on the validated V10 TOTAL QA animation system.
No arc-length exercises are included.  Problems progress from direct formula use
to inverse reasoning and deduction of semicircle / quarter-circle area formulas.

Target: ManimCE 0.20.1, literal -pqh, 1920x1080, 30 fps.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Geometry8_Circle_Foundations_HALVES_TWO_ROWS_20260830_V10_TOTAL_QA import (
    Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (
    MID_GRAY,
    LIGHT_GRAY,
    PAPER,
)


class Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQA(
    Geometry8CircleFoundationsHalvesTwoRows20260830V10TotalQA
):
    """Projector-first circle workshop using the V10 timing and QA foundation."""

    PAUSE_SCALE = 1.36

    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening_workshop()
        self.formula_toolkit()
        self.exercise_area_to_perimeter_1()
        self.exercise_area_to_perimeter_2()
        self.exercise_perimeter_to_diameter()
        self.exercise_parts_and_metrics()
        self.exercise_diameter_to_all()
        self.derive_semicircle_area()
        self.exercise_semicircle_inverse()
        self.derive_quarter_circle_area()
        self.exercise_quarter_inverse()
        self.final_challenge()
        self.closing_workshop()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def workshop_header(self, number: int, title: str, subtitle: str) -> VGroup:
        return self.header(number, title, subtitle)

    def problem_panel(self, prompt: str, width: float = 13.9, height: float = 1.35) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.14,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=PAPER,
            fill_opacity=1.0,
        )
        txt = self.text(prompt, 34, BOLD)
        if txt.width > width - 0.55:
            txt.scale_to_fit_width(width - 0.55)
        txt.move_to(box)
        return VGroup(box, txt)

    def solution_panel(self, *lines: Mobject, width: float = 7.0, height: float = 3.9) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        body = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        if body.width > width - 0.55:
            body.scale_to_fit_width(width - 0.55)
        if body.height > height - 0.45:
            body.scale_to_fit_height(height - 0.45)
        body.move_to(box)
        return VGroup(box, body)

    def circle_metrics_diagram(
        self,
        radius: float = 1.55,
        center: np.ndarray = np.array([-3.9, -0.35, 0.0]),
        show_radius: bool = True,
        show_diameter: bool = False,
        shade_fraction: float | None = None,
    ) -> VGroup:
        circle = Circle(radius=radius, color=BLACK, stroke_width=3.0).move_to(center)
        dot = Dot(center, radius=0.055, color=BLACK)
        items = [circle, dot]

        if shade_fraction is not None:
            angle = TAU * shade_fraction
            sector = Sector(
                outer_radius=radius,
                angle=angle,
                start_angle=0,
                fill_color=LIGHT_GRAY,
                fill_opacity=0.48,
                stroke_color=BLACK,
                stroke_width=2.0,
            ).move_to(center)
            items.insert(0, sector)

        if show_radius:
            rline = Line(center, center + RIGHT * radius, color=BLACK, stroke_width=3.2)
            rlab = self.math("r", 50).next_to(rline, UP, buff=0.08)
            items.extend([rline, rlab])

        if show_diameter:
            dline = Line(center + LEFT * radius, center + RIGHT * radius, color=BLACK, stroke_width=3.2)
            dlab = self.math("d", 50).next_to(dline, DOWN, buff=0.12)
            items.extend([dline, dlab])

        return VGroup(*items)

    def reveal_steps(self, panel: VGroup, lines: list[Mobject], final_wait: float = 4.2) -> None:
        self.play(FadeIn(panel[0], shift=UP * 0.04), run_time=0.65)
        for i, line in enumerate(lines):
            self.play(FadeIn(line, shift=RIGHT * 0.08), run_time=0.72)
            if i < len(lines) - 1:
                self.wait(0.75)
        self.wait(final_wait)

    def think_pause(self, seconds: float = 5.0) -> None:
        cue = self.text("YOUR TURN — calculate before the solution appears", 31, BOLD)
        cue.move_to([0.0, -3.55, 0])
        self.play(FadeIn(cue, shift=UP * 0.05), run_time=0.55)
        self.wait(seconds)
        self.play(FadeOut(cue), run_time=0.45)

    # ------------------------------------------------------------------
    # Opening and toolkit
    # ------------------------------------------------------------------
    def opening_workshop(self) -> None:
        title = self.text("CIRCLE WORKSHOP", 66, BOLD)
        subtitle = self.text("AREA • PERIMETER • RADIUS • DIAMETER • FRACTIONAL REGIONS", 36, BOLD)
        note = self.text("No arc length — focus on formulas, inverse reasoning and circle parts", 32)
        formula = self.big_formula(r"A=\pi r^2\qquad P=2\pi r=\pi d", 10.4, 62)
        group = VGroup(title, subtitle, note, formula).arrange(DOWN, buff=0.45)
        self.projector_safe(group, "circle exercises opening")
        self.play(Write(title), run_time=1.35)
        self.wait(0.70)
        self.play(FadeIn(subtitle, shift=UP * 0.08), run_time=0.85)
        self.wait(0.65)
        self.play(FadeIn(note, shift=UP * 0.06), run_time=0.80)
        self.wait(0.70)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.90)
        self.wait(4.8)
        self.clear_stage(group)

    def formula_toolkit(self) -> None:
        h = self.workshop_header(
            0,
            "FORMULA TOOLKIT — WHAT CAN YOU FIND?",
            "Start with the quantity you know, solve for r or d, then choose the formula you need.",
        )
        self.add(h)
        diag = self.circle_metrics_diagram(radius=1.78, center=np.array([-4.25, -0.35, 0]), show_radius=True, show_diameter=True)
        formulas = VGroup(
            self.math(r"A=\pi r^2", 62),
            self.math(r"P=2\pi r", 62),
            self.math(r"P=\pi d", 62),
            self.math(r"d=2r", 60),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.75, -0.25, 0])
        strategy = self.text("Known → isolate r or d → compute the requested quantity", 33, BOLD).move_to([0.0, -3.25, 0])
        group = VGroup(h, diag, formulas, strategy)
        self.projector_safe(group, "formula toolkit")
        self.play(Create(diag[0]), FadeIn(diag[1]), run_time=0.85)
        self.play(*[Create(m) if isinstance(m, Line) else FadeIn(m) for m in diag[2:]], run_time=1.10)
        self.wait(1.3)
        self.play(LaggedStart(*[Write(f) for f in formulas], lag_ratio=0.22), run_time=2.4)
        self.wait(2.0)
        self.play(FadeIn(strategy, shift=UP * 0.06), run_time=0.80)
        self.wait(4.2)
        self.clear_stage(group)

    # ------------------------------------------------------------------
    # Exercises
    # ------------------------------------------------------------------
    def exercise_area_to_perimeter_1(self) -> None:
        h = self.workshop_header(1, "AREA → RADIUS → PERIMETER", "Given the area, recover the radius first. Then calculate the perimeter.")
        self.add(h)
        problem = self.problem_panel("A circle has area 49π cm². Find its perimeter.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.55, center=np.array([-4.15, -0.35, 0]))
        self.play(FadeIn(problem, shift=DOWN * 0.05), FadeIn(diag), run_time=1.0)
        self.think_pause(5.2)
        lines = [
            self.math(r"49\pi=\pi r^2", 54),
            self.math(r"r^2=49\Rightarrow r=7\text{ cm}", 50),
            self.math(r"P=2\pi r=2\pi(7)", 50),
            self.math(r"\boxed{P=14\pi\text{ cm}}", 56),
        ]
        sol = self.solution_panel(*lines, width=7.7, height=4.25).move_to([2.70, -0.35, 0])
        self.reveal_steps(sol, lines, 4.5)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def exercise_area_to_perimeter_2(self) -> None:
        h = self.workshop_header(2, "AREA → DIAMETER AND PERIMETER", "Use the area to find r, then double it for d and use either perimeter formula.")
        self.add(h)
        problem = self.problem_panel("The area is 81π m². Determine the diameter and perimeter.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.55, center=np.array([-4.15, -0.35, 0]), show_diameter=True)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(5.0)
        lines = [
            self.math(r"81\pi=\pi r^2\Rightarrow r=9\text{ m}", 48),
            self.math(r"d=2r=18\text{ m}", 52),
            self.math(r"P=\pi d=\pi(18)", 50),
            self.math(r"\boxed{P=18\pi\text{ m}}", 56),
        ]
        sol = self.solution_panel(*lines, width=7.9, height=4.15).move_to([2.70, -0.35, 0])
        self.reveal_steps(sol, lines, 4.5)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def exercise_perimeter_to_diameter(self) -> None:
        h = self.workshop_header(3, "PERIMETER → DIAMETER", "When P is known, P = πd is usually the fastest route to the diameter.")
        self.add(h)
        problem = self.problem_panel("A circle has perimeter 20π cm. Find its diameter, radius and area.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.55, center=np.array([-4.15, -0.35, 0]), show_diameter=True)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(5.3)
        lines = [
            self.math(r"20\pi=\pi d\Rightarrow d=20\text{ cm}", 48),
            self.math(r"r=\frac{d}{2}=10\text{ cm}", 50),
            self.math(r"A=\pi r^2=\pi(10)^2", 50),
            self.math(r"\boxed{A=100\pi\text{ cm}^2}", 55),
        ]
        sol = self.solution_panel(*lines, width=8.1, height=4.2).move_to([2.70, -0.35, 0])
        self.reveal_steps(sol, lines, 4.6)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def exercise_parts_and_metrics(self) -> None:
        h = self.workshop_header(4, "CIRCLE PARTS + CALCULATION", "Use the diagram: O is the center, OA is a radius and AB passes through the center.")
        self.add(h)
        problem = self.problem_panel("If OA = 6 cm, identify OA and AB, then find AB, perimeter and area.").move_to([0, 2.55, 0])

        center = np.array([-4.15, -0.35, 0])
        r = 1.62
        circle = Circle(radius=r, color=BLACK, stroke_width=3.0).move_to(center)
        a = center + RIGHT * r
        b = center + LEFT * r
        radius_line = Line(center, a, color=BLACK, stroke_width=3.2)
        diameter_line = Line(b, a, color=BLACK, stroke_width=2.2)
        O = self.text("O", 30, BOLD).next_to(Dot(center, radius=0.04), DOWN + LEFT, buff=0.07)
        A = self.text("A", 30, BOLD).next_to(a, RIGHT, buff=0.08)
        B = self.text("B", 30, BOLD).next_to(b, LEFT, buff=0.08)
        six = self.text("6 cm", 30, BOLD).next_to(radius_line, UP, buff=0.10)
        diagram = VGroup(circle, diameter_line, radius_line, Dot(center, radius=0.05, color=BLACK), O, A, B, six)
        self.play(FadeIn(problem), Create(circle), Create(diameter_line), Create(radius_line), FadeIn(VGroup(O, A, B, six)), run_time=1.15)
        self.think_pause(5.0)
        lines = [
            self.text("OA is a radius; AB is a diameter.", 32, BOLD),
            self.math(r"AB=d=2r=12\text{ cm}", 48),
            self.math(r"P=2\pi(6)=12\pi\text{ cm}", 48),
            self.math(r"A=\pi(6)^2=36\pi\text{ cm}^2", 48),
        ]
        sol = self.solution_panel(*lines, width=8.2, height=4.25).move_to([2.65, -0.35, 0])
        self.reveal_steps(sol, lines, 4.6)
        self.clear_stage(VGroup(h, problem, diagram, sol))

    def exercise_diameter_to_all(self) -> None:
        h = self.workshop_header(5, "DIAMETER → RADIUS → AREA", "The radius is half the diameter. Keep linear units and square units distinct.")
        self.add(h)
        problem = self.problem_panel("A circle has diameter 16 cm. Find its radius, perimeter and area.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.58, center=np.array([-4.15, -0.35, 0]), show_radius=False, show_diameter=True)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(4.8)
        lines = [
            self.math(r"r=\frac{16}{2}=8\text{ cm}", 50),
            self.math(r"P=\pi d=16\pi\text{ cm}", 50),
            self.math(r"A=\pi(8)^2", 52),
            self.math(r"\boxed{A=64\pi\text{ cm}^2}", 56),
        ]
        sol = self.solution_panel(*lines, width=7.8, height=4.15).move_to([2.70, -0.35, 0])
        self.reveal_steps(sol, lines, 4.5)
        self.clear_stage(VGroup(h, problem, diag, sol))

    # ------------------------------------------------------------------
    # Fractional regions: derive formula first, then inverse reasoning
    # ------------------------------------------------------------------
    def derive_semicircle_area(self) -> None:
        h = self.workshop_header(6, "DEDUCE THE AREA OF A SEMICIRCLE", "A semicircle is exactly one half of the full circular region.")
        self.add(h)
        full = self.circle_metrics_diagram(radius=1.72, center=np.array([-4.15, -0.25, 0]), show_radius=True)
        half = self.circle_metrics_diagram(radius=1.72, center=np.array([0.15, -0.25, 0]), show_radius=True, shade_fraction=0.5)
        full_lab = self.text("FULL CIRCLE", 32, BOLD).next_to(full, DOWN, buff=0.20)
        half_lab = self.text("ONE HALF", 32, BOLD).next_to(half, DOWN, buff=0.20)
        arrow = Arrow([2.0, -0.25, 0], [3.15, -0.25, 0], buff=0.0, color=BLACK, stroke_width=3.0)
        question = self.math(r"A_{1/2}=?", 58).move_to([5.15, 0.30, 0])
        group = VGroup(h, full, half, full_lab, half_lab, arrow, question)
        self.projector_safe(group, "semicircle derivation layout")
        self.play(FadeIn(full), FadeIn(full_lab), run_time=0.90)
        self.wait(1.2)
        self.play(FadeIn(half), FadeIn(half_lab), GrowArrow(arrow), Write(question), run_time=1.0)
        self.think_pause(4.7)
        eq1 = self.math(r"A_{1/2}=\frac{1}{2}A_{\text{circle}}", 52).move_to([4.65, -1.15, 0])
        eq2 = self.math(r"A_{1/2}=\frac{1}{2}\pi r^2", 58).move_to([4.65, -2.10, 0])
        box = SurroundingRectangle(eq2, buff=0.22, corner_radius=0.10, color=BLACK, stroke_width=2.2)
        self.play(Write(eq1), run_time=0.85)
        self.wait(1.2)
        self.play(Write(eq2), Create(box), run_time=1.0)
        self.wait(5.0)
        self.clear_stage(VGroup(group, eq1, eq2, box))

    def exercise_semicircle_inverse(self) -> None:
        h = self.workshop_header(7, "SEMICIRCLE — INVERSE REASONING", "Given the area of half the circle, recover the full-circle area before solving for r.")
        self.add(h)
        problem = self.problem_panel("A semicircle has area 50π cm². Find the radius and the full-circle perimeter.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.62, center=np.array([-4.15, -0.35, 0]), show_radius=True, shade_fraction=0.5)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(5.2)
        lines = [
            self.math(r"A_{\text{circle}}=2(50\pi)=100\pi", 48),
            self.math(r"100\pi=\pi r^2\Rightarrow r=10\text{ cm}", 46),
            self.math(r"P=2\pi r=20\pi\text{ cm}", 50),
            self.math(r"\boxed{r=10\text{ cm},\;P=20\pi\text{ cm}}", 50),
        ]
        sol = self.solution_panel(*lines, width=8.4, height=4.25).move_to([2.65, -0.35, 0])
        self.reveal_steps(sol, lines, 4.7)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def derive_quarter_circle_area(self) -> None:
        h = self.workshop_header(8, "DEDUCE THE AREA OF A QUARTER CIRCLE", "Four equal quarters reconstruct one complete circle.")
        self.add(h)
        full = self.circle_metrics_diagram(radius=1.65, center=np.array([-4.30, -0.30, 0]), show_radius=True)
        quarter = self.circle_metrics_diagram(radius=1.65, center=np.array([0.0, -0.30, 0]), show_radius=True, shade_fraction=0.25)
        brace_note = self.text("1 of 4 equal regions", 32, BOLD).next_to(quarter, DOWN, buff=0.20)
        self.play(FadeIn(full), run_time=0.85)
        self.wait(1.0)
        self.play(FadeIn(quarter), FadeIn(brace_note), run_time=0.95)
        self.think_pause(4.5)
        eq1 = self.math(r"A_{1/4}=\frac{1}{4}A_{\text{circle}}", 52).move_to([4.55, 0.10, 0])
        eq2 = self.math(r"A_{1/4}=\frac{1}{4}\pi r^2", 58).move_to([4.55, -1.05, 0])
        box = SurroundingRectangle(eq2, buff=0.22, corner_radius=0.10, color=BLACK, stroke_width=2.2)
        self.play(Write(eq1), run_time=0.85)
        self.wait(1.1)
        self.play(Write(eq2), Create(box), run_time=1.0)
        example = self.math(r"r=12\Rightarrow A_{1/4}=\frac14\pi(12)^2=36\pi", 48).move_to([3.65, -2.45, 0])
        self.play(FadeIn(example, shift=UP * 0.06), run_time=0.85)
        self.wait(5.0)
        self.clear_stage(VGroup(h, full, quarter, brace_note, eq1, eq2, box, example))

    def exercise_quarter_inverse(self) -> None:
        h = self.workshop_header(9, "QUARTER CIRCLE — WORK BACKWARD", "Multiply a quarter-circle area by 4 to recover the area of the complete circle.")
        self.add(h)
        problem = self.problem_panel("A quarter-circle region has area 25π m². Find the radius and diameter of the full circle.").move_to([0, 2.55, 0])
        diag = self.circle_metrics_diagram(radius=1.62, center=np.array([-4.15, -0.35, 0]), show_radius=True, shade_fraction=0.25)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(5.1)
        lines = [
            self.math(r"A_{\text{circle}}=4(25\pi)=100\pi", 48),
            self.math(r"100\pi=\pi r^2", 50),
            self.math(r"r=10\text{ m}\qquad d=20\text{ m}", 52),
            self.math(r"\boxed{r=10\text{ m},\;d=20\text{ m}}", 54),
        ]
        sol = self.solution_panel(*lines, width=8.1, height=4.15).move_to([2.70, -0.35, 0])
        self.reveal_steps(sol, lines, 4.6)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def final_challenge(self) -> None:
        h = self.workshop_header(10, "FINAL CHALLENGE — CONNECT THE FORMULAS", "Use more than one relationship. Do not calculate arc length.")
        self.add(h)
        problem = self.problem_panel("A circle has area 144π cm². Find r, d, P, half-circle area and quarter-circle area.", height=1.40).move_to([0, 2.50, 0])
        diag = self.circle_metrics_diagram(radius=1.60, center=np.array([-4.35, -0.30, 0]), show_radius=True, show_diameter=True)
        self.play(FadeIn(problem), FadeIn(diag), run_time=0.95)
        self.think_pause(6.0)
        lines = [
            self.math(r"r=12\text{ cm}\qquad d=24\text{ cm}", 47),
            self.math(r"P=24\pi\text{ cm}", 49),
            self.math(r"A_{1/2}=\frac12(144\pi)=72\pi\text{ cm}^2", 45),
            self.math(r"A_{1/4}=\frac14(144\pi)=36\pi\text{ cm}^2", 45),
        ]
        sol = self.solution_panel(*lines, width=8.5, height=4.2).move_to([2.60, -0.35, 0])
        self.reveal_steps(sol, lines, 5.0)
        self.clear_stage(VGroup(h, problem, diag, sol))

    def closing_workshop(self) -> None:
        title = self.text("CIRCLE WORKSHOP — KEY REASONING", 52, BOLD)
        bullets = VGroup(
            self.text("1. From area: divide by π, then take the square root to recover r.", 34),
            self.text("2. From perimeter: P = πd finds d directly; P = 2πr finds r.", 34),
            self.text("3. Diameter and radius differ by a factor of 2.", 34),
            self.text("4. Half-circle area = 1/2 of πr²; quarter-circle area = 1/4 of πr².", 34),
            self.text("5. Area uses square units; perimeter, radius and diameter use linear units.", 34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        for line in bullets:
            if line.width > 14.35:
                line.scale_to_fit_width(14.35)
        formula = self.big_formula(r"A=\pi r^2\qquad P=2\pi r=\pi d", 10.2, 60)
        group = VGroup(title, bullets, formula).arrange(DOWN, buff=0.42)
        self.projector_safe(group, "circle exercises closing")
        self.play(FadeIn(title, shift=UP * 0.06), run_time=0.90)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.07) for line in bullets], lag_ratio=0.20), run_time=3.0)
        self.wait(2.8)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.95)
        self.play(Circumscribe(formula[1], color=MID_GRAY, time_width=0.9), run_time=1.15)
        self.wait(7.0)


# Preview:
# LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQA --disable_caching
# Final:
# manim -pqh Geometry8_Circle_Exercises_AREA_PERIMETER_PARTS_20260831_V1_TOTAL_QA.py Geometry8CircleExercisesAreaPerimeterParts20260831V1TotalQA --disable_caching
