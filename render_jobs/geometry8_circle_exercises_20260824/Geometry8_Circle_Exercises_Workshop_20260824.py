#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Exercises Workshop — 2026-08-24.

A real ManimCE presentation rendered from vector objects and MathTex.
The scene continues the audited Geometry 8 Circle V4 Senior Projector style:
- large projector-readable figures and typography;
- one focal idea at a time;
- progressive geometric construction;
- explicit think / read / verify pauses;
- clean MovingCameraScene zooms;
- panel containment and safe-frame assertions;
- worked exercises for radius, diameter, circumference/perimeter, full area,
  and circle regions.

Target: Manim Community Edition 0.20.1, horizontal 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *
from Geometry8_Circle_V4_Senior_QA import (
    V4_READ,
    V4_EXPLAIN,
    V4_THINK,
    V4_SUMMARY,
    V4_FINAL,
)
from Geometry8_Circle_Measurement_To_Area_20260823_V4 import (
    Geometry8CircleMeasurementArea20260823V4,
)


PI_APPROX = 3.1416


class Geometry8CircleExercisesWorkshop20260824(Geometry8CircleMeasurementArea20260823V4):
    """Senior projector workshop: circle measures, full area, and regions."""

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()
        assert math.isclose(2 * 7, 14)
        assert math.isclose(18 / 2, 9)
        assert math.isclose(math.pi * 12, 37.6991118431, rel_tol=1e-10)
        assert math.isclose(2 * math.pi * 5, 31.4159265359, rel_tol=1e-10)
        assert math.isclose(math.pi * 6**2, 113.0973355292, rel_tol=1e-10)
        assert math.isclose((14 * math.pi) / math.pi, 14, rel_tol=1e-10)
        assert math.isclose(math.pi * 7**2, 153.9380400259, rel_tol=1e-10)
        assert math.isclose(0.5 * math.pi * 8**2, 100.5309649149, rel_tol=1e-10)
        assert math.isclose(math.pi * 8 + 16, 41.1327412287, rel_tol=1e-10)
        assert math.isclose(0.25 * math.pi * 10**2, 78.5398163397, rel_tol=1e-10)
        assert math.isclose(0.25 * (2 * math.pi * 10) + 20, 35.7079632679, rel_tol=1e-10)
        assert math.isclose((60 / 360) * math.pi * 12**2, 75.3982236862, rel_tol=1e-10)
        assert math.isclose((60 / 360) * 2 * math.pi * 12, 12.5663706144, rel_tol=1e-10)

    def construct(self) -> None:
        self.opening_workshop()
        self.reference_map()
        self.exercise_01_diameter_from_radius()
        self.exercise_02_radius_from_diameter()
        self.exercise_03_perimeter_from_diameter()
        self.exercise_04_perimeter_from_radius()
        self.exercise_05_full_area()
        self.exercise_06_inverse_mixed()
        self.circle_regions_reference()
        self.exercise_07_semicircle()
        self.exercise_08_quadrant()
        self.exercise_09_sector()
        self.independent_practice()
        self.final_summary()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    def _show_formula(self, panel: VGroup, *, zoom_width: float = 7.0, pause: float = V4_EXPLAIN) -> None:
        """Draw panel border and write the equation, then focus the camera."""
        self.play(Create(panel[0]), Write(panel[1]), run_time=RUN_NORMAL * 1.15)
        self._v4_zoom(panel, width=zoom_width, pause=pause)

    def _circle_with_radius(self, *, center: np.ndarray, radius: float, label_tex: str) -> VGroup:
        circle = Circle(radius=radius, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        dot = Dot(center, radius=0.075, color=BLACK_LINE)
        radius_line = Line(center, center + RIGHT * radius, color=BLACK_LINE, stroke_width=5)
        label = self.math(label_tex, 50).next_to(radius_line, UP, buff=0.15)
        return VGroup(circle, dot, radius_line, label)

    def _circle_with_diameter(self, *, center: np.ndarray, radius: float, label_tex: str) -> VGroup:
        circle = Circle(radius=radius, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        dot = Dot(center, radius=0.075, color=BLACK_LINE)
        diameter = DoubleArrow(
            center + LEFT * radius,
            center + RIGHT * radius,
            buff=0.03,
            tip_length=0.16,
            color=BLACK_LINE,
            stroke_width=3.6,
        )
        label = self.math(label_tex, 50).next_to(diameter, DOWN, buff=0.16)
        return VGroup(circle, dot, diameter, label)

    def _animate_basic_figure(self, fig: VGroup) -> None:
        self.play(Create(fig[0]), FadeIn(fig[1]), run_time=RUN_NORMAL)
        self.play(GrowFromCenter(fig[2]), Write(fig[3]), run_time=RUN_NORMAL)

    def _answer_check(self, text: str, *, y: float = -3.00, width: float = 8.8) -> VGroup:
        panel = self._v4_text_panel(
            "COMPROBACIÓN",
            [text],
            width=width,
            title_size=33,
            body_size=31,
            fill_color=PAPER_GRAY,
        ).move_to([0, y, 0])
        self.assert_content_safe(panel, "answer check")
        return panel

    # ------------------------------------------------------------------
    # Opening and reference
    # ------------------------------------------------------------------
    def opening_workshop(self) -> None:
        course = self.text("GEOMETRÍA 8", 34, BOLD)
        title = self.text("TALLER ANIMADO — CÍRCULO Y REGIONES", 60, BOLD)
        subtitle = self.text(
            "Radio, diámetro, perímetro, área completa y regiones del círculo — ejercicio por ejercicio.",
            32,
        )
        self.fit(subtitle, 13.8, 0.76)

        center = np.array([-3.7, -0.65, 0.0])
        circle = Circle(radius=1.85, stroke_color=BLACK_LINE, stroke_width=6).move_to(center)
        center_dot = Dot(center, radius=0.075, color=BLACK_LINE)
        radius = Line(center, center + RIGHT * 1.85, color=BLACK_LINE, stroke_width=5)
        diameter = Line(center + LEFT * 1.85, center + RIGHT * 1.85, color=LIGHT_GRAY, stroke_width=3)

        cards = VGroup(
            self._v4_formula_panel(r"d=2r", width=4.1, height=1.18, size=58),
            self._v4_formula_panel(r"C=\pi d=2\pi r", width=5.5, height=1.18, size=50),
            self._v4_formula_panel(r"A=\pi r^2", width=4.8, height=1.18, size=58),
        ).arrange(DOWN, buff=0.30).move_to([3.5, -0.55, 0])

        top = VGroup(course, title, subtitle).arrange(DOWN, buff=0.25).move_to(UP * 2.15)
        group = VGroup(top, circle, center_dot, radius, diameter, cards)
        self.assert_within_frame(group, "workshop opening", margin=0.16)

        self.play(FadeIn(course, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW * 1.25)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.wait(V4_READ)
        self.play(Create(circle), FadeIn(center_dot), run_time=RUN_NORMAL)
        self.play(GrowFromPoint(radius, center), Create(diameter), run_time=RUN_NORMAL)
        for card in cards:
            self.play(Create(card[0]), Write(card[1]), run_time=RUN_NORMAL)
            self.wait(V4_READ)
        self._v4_zoom(VGroup(circle, radius, diameter), width=6.4, pause=V4_EXPLAIN)
        self.wait(V4_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def reference_map(self) -> None:
        self._v4_header(
            1,
            "MAPA DE FÓRMULAS — ¿QUÉ QUIERO ENCONTRAR?",
            "Antes de calcular, identifica el dato conocido y la magnitud que te están pidiendo.",
        )

        formulas = [
            (r"d=2r", "DIÁMETRO", "Dos radios forman un diámetro."),
            (r"r=\frac{d}{2}", "RADIO", "El radio es la mitad del diámetro."),
            (r"C=\pi d=2\pi r", "PERÍMETRO", "La circunferencia mide todo el borde."),
            (r"A=\pi r^2", "ÁREA COMPLETA", "El área mide toda la superficie interior."),
        ]
        y_positions = [1.65, 0.25, -1.15, -2.55]
        panels = VGroup()
        for (expr, label, note), y in zip(formulas, y_positions):
            formula = self.math(expr, 55)
            text = VGroup(self.text(label, 31, BOLD), self.text(note, 27)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            row = VGroup(formula, text).arrange(RIGHT, buff=0.75)
            panel = self._v4_panel(row, width=12.5, height=1.18, fill_color=WHITE).move_to([0, y, 0])
            panels.add(panel)

        self.assert_content_safe(panels, "formula reference map")
        for panel in panels:
            self.play(Create(panel[0]), FadeIn(panel[1], shift=RIGHT * 0.08), run_time=RUN_NORMAL)
            self._v4_zoom(panel, width=12.8, pause=V4_READ)
        self.wait(V4_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 1: diameter
    # ------------------------------------------------------------------
    def exercise_01_diameter_from_radius(self) -> None:
        self._v4_header(
            2,
            "EJERCICIO 1 — DEL RADIO AL DIÁMETRO",
            "Una rueda tiene radio de 7 cm. Determina su diámetro.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        fig = self._circle_with_radius(center=center, radius=2.05, label_tex=r"r=7\text{ cm}")
        prompt = self._v4_text_panel(
            "PIENSA PRIMERO",
            ["¿Cuántos radios caben exactamente en un diámetro?"],
            width=6.3,
            title_size=34,
            body_size=31,
            fill_color=PAPER_GRAY,
        ).move_to([3.75, 0.25, 0])
        self.assert_content_safe(VGroup(fig, prompt), "exercise 1 prompt")

        self._animate_basic_figure(fig)
        self.play(FadeIn(prompt, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self._v4_zoom(fig, width=6.4, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), fig.animate.shift(LEFT * 0.30), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"d=2r", width=5.8, height=1.35, size=62).move_to([3.65, 1.15, 0])
        p2 = self._v4_formula_panel(r"d=2(7\text{ cm})", width=6.2, height=1.35, size=56).move_to([3.65, -0.50, 0])
        p3 = self._v4_formula_panel(r"\boxed{d=14\text{ cm}}", width=6.2, height=1.45, size=62).move_to([3.65, -2.20, 0])
        self.assert_content_safe(VGroup(fig, p1, p2, p3), "exercise 1 solution")
        self._show_formula(p1)
        self._show_formula(p2)
        self._show_formula(p3, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 2: radius
    # ------------------------------------------------------------------
    def exercise_02_radius_from_diameter(self) -> None:
        self._v4_header(
            3,
            "EJERCICIO 2 — DEL DIÁMETRO AL RADIO",
            "Un plato circular tiene diámetro de 18 cm. Determina su radio.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        fig = self._circle_with_diameter(center=center, radius=2.05, label_tex=r"d=18\text{ cm}")
        prompt = self._v4_text_panel(
            "PREGUNTA CLAVE",
            ["Si el diámetro contiene dos radios, ¿qué operación permite recuperar uno solo?"],
            width=6.4,
            title_size=34,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.70, 0.20, 0])
        self.assert_content_safe(VGroup(fig, prompt), "exercise 2 prompt")

        self._animate_basic_figure(fig)
        self.play(FadeIn(prompt), run_time=RUN_NORMAL)
        self._v4_zoom(fig, width=6.5, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"r=\frac{d}{2}", width=5.8, height=1.35, size=62).move_to([3.65, 1.15, 0])
        p2 = self._v4_formula_panel(r"r=\frac{18}{2}\text{ cm}", width=6.2, height=1.35, size=56).move_to([3.65, -0.50, 0])
        p3 = self._v4_formula_panel(r"\boxed{r=9\text{ cm}}", width=6.2, height=1.45, size=62).move_to([3.65, -2.20, 0])
        self.assert_content_safe(VGroup(fig, p1, p2, p3), "exercise 2 solution")
        self._show_formula(p1)
        self._show_formula(p2)
        self._show_formula(p3, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 3: perimeter from diameter
    # ------------------------------------------------------------------
    def exercise_03_perimeter_from_diameter(self) -> None:
        self._v4_header(
            4,
            "EJERCICIO 3 — PERÍMETRO CON DIÁMETRO",
            "Una tapa circular tiene diámetro de 12 cm. Determina la longitud completa de su borde.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        fig = self._circle_with_diameter(center=center, radius=2.05, label_tex=r"d=12\text{ cm}")
        trace = fig[0].copy().set_stroke(BLACK_LINE, width=10)
        tracer = Dot(trace.point_at_angle(0), radius=0.095, color=BLACK_LINE)
        prompt = self._v4_text_panel(
            "PERÍMETRO DEL CÍRCULO",
            ["El perímetro de un círculo se llama circunferencia: mide solamente el borde."],
            width=6.4,
            title_size=33,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.70, 0.20, 0])
        self.assert_content_safe(VGroup(fig, prompt), "exercise 3 prompt")

        self._animate_basic_figure(fig)
        self.play(FadeIn(prompt), run_time=RUN_NORMAL)
        self.play(Create(trace), MoveAlongPath(tracer, trace), run_time=RUN_SLOW * 2.25)
        self.play(FadeOut(tracer), run_time=RUN_QUICK)
        self._v4_zoom(VGroup(fig[0], trace, fig[2], fig[3]), width=6.6, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"C=\pi d", width=5.8, height=1.35, size=62).move_to([3.65, 1.15, 0])
        p2 = self._v4_formula_panel(r"C=\pi(12)=12\pi", width=6.2, height=1.35, size=56).move_to([3.65, -0.50, 0])
        p3 = self._v4_formula_panel(r"\boxed{C\approx37.70\text{ cm}}", width=6.4, height=1.45, size=56).move_to([3.65, -2.20, 0])
        self.assert_content_safe(VGroup(fig, trace, p1, p2, p3), "exercise 3 solution")
        self._show_formula(p1)
        self._show_formula(p2)
        self._show_formula(p3, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 4: perimeter from radius
    # ------------------------------------------------------------------
    def exercise_04_perimeter_from_radius(self) -> None:
        self._v4_header(
            5,
            "EJERCICIO 4 — PERÍMETRO CON RADIO",
            "Una fuente circular tiene radio de 5 m. Determina su perímetro.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        fig = self._circle_with_radius(center=center, radius=2.05, label_tex=r"r=5\text{ m}")
        prompt = self._v4_text_panel(
            "ELIGE LA FORMA MÁS DIRECTA",
            ["Como conocemos r, podemos usar C = 2πr sin calcular primero el diámetro."],
            width=6.4,
            title_size=32,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.70, 0.20, 0])
        self.assert_content_safe(VGroup(fig, prompt), "exercise 4 prompt")

        self._animate_basic_figure(fig)
        self.play(FadeIn(prompt), run_time=RUN_NORMAL)
        self._v4_zoom(fig, width=6.4, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"C=2\pi r", width=5.8, height=1.35, size=62).move_to([3.65, 1.15, 0])
        p2 = self._v4_formula_panel(r"C=2\pi(5)=10\pi", width=6.2, height=1.35, size=56).move_to([3.65, -0.50, 0])
        p3 = self._v4_formula_panel(r"\boxed{C\approx31.42\text{ m}}", width=6.4, height=1.45, size=56).move_to([3.65, -2.20, 0])
        self.assert_content_safe(VGroup(fig, p1, p2, p3), "exercise 4 solution")
        self._show_formula(p1)
        self._show_formula(p2)
        self._show_formula(p3, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 5: full area
    # ------------------------------------------------------------------
    def exercise_05_full_area(self) -> None:
        self._v4_header(
            6,
            "EJERCICIO 5 — ÁREA COMPLETA DEL CÍRCULO",
            "Una zona circular tiene radio de 6 m. Determina toda su superficie interior.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        fig = self._circle_with_radius(center=center, radius=2.05, label_tex=r"r=6\text{ m}")
        fill = Circle(radius=2.05, stroke_width=0, fill_color=LIGHT_GRAY, fill_opacity=0.62).move_to(center)
        prompt = self._v4_text_panel(
            "BORDE VS. SUPERFICIE",
            ["Aquí no medimos el borde: debemos cubrir todo el interior, por eso usamos área."],
            width=6.4,
            title_size=33,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.70, 0.20, 0])
        self.assert_content_safe(VGroup(fig, prompt), "exercise 5 prompt")

        self._animate_basic_figure(fig)
        self.play(FadeIn(prompt), run_time=RUN_NORMAL)
        self.play(FadeIn(fill), run_time=RUN_SLOW * 1.30)
        self._v4_zoom(VGroup(fill, fig), width=6.5, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"A=\pi r^2", width=5.8, height=1.35, size=62).move_to([3.65, 1.15, 0])
        p2 = self._v4_formula_panel(r"A=\pi(6)^2=36\pi", width=6.2, height=1.35, size=56).move_to([3.65, -0.50, 0])
        p3 = self._v4_formula_panel(r"\boxed{A\approx113.10\text{ m}^2}", width=6.5, height=1.45, size=54).move_to([3.65, -2.20, 0])
        self.assert_content_safe(VGroup(fig, fill, p1, p2, p3), "exercise 5 solution")
        self._show_formula(p1)
        self._show_formula(p2)
        self._show_formula(p3, pause=V4_THINK)
        unit = self._answer_check("Área → unidades cuadradas: m².", y=-3.02, width=8.6)
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(fill), p3.animate.move_to([0, -1.35, 0]), run_time=RUN_NORMAL)
        self.play(FadeIn(unit), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(p3, unit), width=9.2, pause=V4_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 6: inverse mixed problem
    # ------------------------------------------------------------------
    def exercise_06_inverse_mixed(self) -> None:
        self._v4_header(
            7,
            "EJERCICIO 6 — PROBLEMA INVERSO",
            "La circunferencia de una mesa mide aproximadamente 43.98 cm. Estima diámetro, radio y área completa.",
        )
        center = np.array([-3.55, -0.35, 0.0])
        circle = Circle(radius=2.05, stroke_color=BLACK_LINE, stroke_width=7).move_to(center)
        trace = circle.copy().set_stroke(BLACK_LINE, width=11)
        tracer = Dot(trace.point_at_angle(0), radius=0.10, color=BLACK_LINE)
        label = self.math(r"C\approx43.98\text{ cm}", 48).next_to(circle, DOWN, buff=0.25)
        prompt = self._v4_text_panel(
            "TRABAJA HACIA ATRÁS",
            ["Primero recupera d desde C = πd; después encuentra r y finalmente el área."],
            width=6.4,
            title_size=33,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.70, 0.15, 0])
        self.assert_content_safe(VGroup(circle, label, prompt), "exercise 6 prompt")

        self.play(Create(circle), Write(label), FadeIn(prompt), run_time=RUN_NORMAL)
        self.play(Create(trace), MoveAlongPath(tracer, trace), run_time=RUN_SLOW * 2.10)
        self.play(FadeOut(tracer), run_time=RUN_QUICK)
        self._v4_zoom(VGroup(circle, trace, label), width=6.7, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), VGroup(circle, trace, label).animate.shift(LEFT * 0.35), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"d=\frac{C}{\pi}\approx\frac{43.98}{\pi}\approx14.00\text{ cm}", width=7.0, height=1.35, size=46).move_to([3.55, 1.15, 0])
        p2 = self._v4_formula_panel(r"r=\frac{d}{2}\approx7.00\text{ cm}", width=6.6, height=1.35, size=50).move_to([3.55, -0.50, 0])
        p3 = self._v4_formula_panel(r"A=\pi r^2\approx\boxed{153.94\text{ cm}^2}", width=7.0, height=1.45, size=48).move_to([3.55, -2.20, 0])
        self.assert_content_safe(VGroup(circle, label, p1, p2, p3), "exercise 6 solution")
        self._show_formula(p1, zoom_width=7.6)
        self._show_formula(p2, zoom_width=7.2)
        self._show_formula(p3, zoom_width=7.6, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Regions reference
    # ------------------------------------------------------------------
    def circle_regions_reference(self) -> None:
        self._v4_header(
            8,
            "REGIONES DEL CÍRCULO",
            "La circunferencia es solamente el borde; semicírculos, cuadrantes, sectores y segmentos son regiones del círculo.",
        )
        centers = [np.array([-5.25, 0.35, 0]), np.array([-1.75, 0.35, 0]), np.array([1.75, 0.35, 0]), np.array([5.25, 0.35, 0])]
        r = 1.30

        semi = AnnularSector(inner_radius=0, outer_radius=r, angle=PI, start_angle=0,
                             stroke_color=BLACK_LINE, stroke_width=4,
                             fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(centers[0])
        semi_label = self.text("SEMICÍRCULO", 30, BOLD).next_to(semi, DOWN, buff=0.25)

        quad = AnnularSector(inner_radius=0, outer_radius=r, angle=PI/2, start_angle=0,
                             stroke_color=BLACK_LINE, stroke_width=4,
                             fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(centers[1])
        quad_label = self.text("CUADRANTE", 30, BOLD).next_to(quad, DOWN, buff=0.25)

        sec = AnnularSector(inner_radius=0, outer_radius=r, angle=PI/3, start_angle=0,
                            stroke_color=BLACK_LINE, stroke_width=4,
                            fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(centers[2])
        sec_label = self.text("SECTOR", 30, BOLD).next_to(sec, DOWN, buff=0.25)

        seg_circle = Circle(radius=r, stroke_color=BLACK_LINE, stroke_width=4).move_to(centers[3])
        a1, a2 = 35 * DEGREES, 145 * DEGREES
        p1 = centers[3] + r * np.array([math.cos(a1), math.sin(a1), 0])
        p2 = centers[3] + r * np.array([math.cos(a2), math.sin(a2), 0])
        chord = Line(p1, p2, color=BLACK_LINE, stroke_width=4)
        seg_label = self.text("SEGMENTO", 30, BOLD).next_to(seg_circle, DOWN, buff=0.25)

        figures = VGroup(
            VGroup(semi, semi_label),
            VGroup(quad, quad_label),
            VGroup(sec, sec_label),
            VGroup(seg_circle, chord, seg_label),
        )
        note = self._v4_text_panel(
            "FRACCIÓN DEL CÍRCULO",
            ["Semicírculo = 1/2", "Cuadrante = 1/4", "Sector = θ / 360°"],
            width=10.2,
            title_size=34,
            body_size=31,
            fill_color=PAPER_GRAY,
        ).move_to(DOWN * 2.55)
        self.assert_content_safe(VGroup(figures, note), "circle regions reference")

        for item in figures:
            self.play(Create(item[0]), *([Create(item[1])] if len(item) == 3 else []), Write(item[-1]), run_time=RUN_NORMAL)
            self._v4_zoom(item, width=4.8, pause=V4_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self._v4_zoom(note, width=10.8, pause=V4_EXPLAIN)
        self.wait(V4_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 7: semicircle area + perimeter
    # ------------------------------------------------------------------
    def exercise_07_semicircle(self) -> None:
        self._v4_header(
            9,
            "EJERCICIO 7 — SEMICÍRCULO",
            "Un semicírculo tiene radio de 8 cm. Determina su área y el perímetro completo de la región.",
        )
        center = np.array([-3.60, -0.55, 0.0])
        r = 2.15
        semi = AnnularSector(inner_radius=0, outer_radius=r, angle=PI, start_angle=0,
                             stroke_color=BLACK_LINE, stroke_width=6,
                             fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(center)
        radius = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=5)
        r_label = self.math(r"r=8\text{ cm}", 48).next_to(radius, UP, buff=0.14)
        prompt = self._v4_text_panel(
            "DOS PREGUNTAS DIFERENTES",
            ["Área: toma la mitad del círculo.", "Perímetro: suma el arco semicircular y el diámetro."],
            width=6.5,
            title_size=32,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.65, 0.15, 0])
        self.assert_content_safe(VGroup(semi, radius, r_label, prompt), "semicircle prompt")

        self.play(Create(semi), GrowFromPoint(radius, center), Write(r_label), FadeIn(prompt), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(semi, radius, r_label), width=6.7, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"A=\frac12\pi r^2=32\pi\approx100.53\text{ cm}^2", width=7.0, height=1.45, size=46).move_to([3.45, 0.85, 0])
        p2 = self._v4_formula_panel(r"P=\pi r+2r=8\pi+16\approx41.13\text{ cm}", width=7.0, height=1.45, size=44).move_to([3.45, -1.10, 0])
        self.assert_content_safe(VGroup(semi, radius, r_label, p1, p2), "semicircle solution")
        self._show_formula(p1, zoom_width=7.6, pause=V4_EXPLAIN)
        self._show_formula(p2, zoom_width=7.6, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 8: quadrant
    # ------------------------------------------------------------------
    def exercise_08_quadrant(self) -> None:
        self._v4_header(
            10,
            "EJERCICIO 8 — CUADRANTE",
            "Un cuadrante tiene radio de 10 cm. Determina su área y el perímetro de la región.",
        )
        center = np.array([-3.60, -0.55, 0.0])
        r = 2.25
        quad = AnnularSector(inner_radius=0, outer_radius=r, angle=PI/2, start_angle=0,
                             stroke_color=BLACK_LINE, stroke_width=6,
                             fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(center)
        r1 = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=5)
        r2 = Line(center, center + UP * r, color=BLACK_LINE, stroke_width=5)
        label = self.math(r"r=10\text{ cm}", 48).next_to(r1, DOWN, buff=0.16)
        angle = self.math(r"90^\circ", 44).move_to(center + UR * 0.55)
        prompt = self._v4_text_panel(
            "CUARTA PARTE",
            ["90° de 360° = 1/4 del círculo completo."],
            width=6.3,
            title_size=34,
            body_size=31,
            fill_color=PAPER_GRAY,
        ).move_to([3.65, 0.15, 0])
        self.assert_content_safe(VGroup(quad, r1, r2, label, angle, prompt), "quadrant prompt")

        self.play(Create(quad), Create(r1), Create(r2), Write(label), Write(angle), FadeIn(prompt), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(quad, r1, r2, label, angle), width=6.8, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"A=\frac14\pi(10)^2=25\pi\approx78.54\text{ cm}^2", width=7.0, height=1.45, size=44).move_to([3.45, 0.85, 0])
        p2 = self._v4_formula_panel(r"P=\frac14(2\pi r)+2r=5\pi+20\approx35.71\text{ cm}", width=7.0, height=1.45, size=40).move_to([3.45, -1.10, 0])
        self.assert_content_safe(VGroup(quad, r1, r2, p1, p2), "quadrant solution")
        self._show_formula(p1, zoom_width=7.7, pause=V4_EXPLAIN)
        self._show_formula(p2, zoom_width=7.7, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Exercise 9: sector
    # ------------------------------------------------------------------
    def exercise_09_sector(self) -> None:
        self._v4_header(
            11,
            "EJERCICIO 9 — SECTOR CIRCULAR",
            "Un sector tiene ángulo central de 60° y radio de 12 cm. Determina su área, longitud de arco y perímetro.",
        )
        center = np.array([-3.60, -0.55, 0.0])
        r = 2.30
        angle_value = 60 * DEGREES
        sec = AnnularSector(inner_radius=0, outer_radius=r, angle=angle_value, start_angle=0,
                            stroke_color=BLACK_LINE, stroke_width=6,
                            fill_color=VERY_LIGHT_GRAY, fill_opacity=1).shift(center)
        r1 = Line(center, center + RIGHT * r, color=BLACK_LINE, stroke_width=5)
        r2 = Line(center, center + r * np.array([math.cos(angle_value), math.sin(angle_value), 0]), color=BLACK_LINE, stroke_width=5)
        r_label = self.math(r"r=12\text{ cm}", 46).next_to(r1, DOWN, buff=0.16)
        theta = self.math(r"60^\circ", 44).move_to(center + 0.70 * np.array([math.cos(angle_value/2), math.sin(angle_value/2), 0]))
        prompt = self._v4_text_panel(
            "USA LA FRACCIÓN ANGULAR",
            ["60° / 360° = 1/6. La misma fracción sirve para área y longitud de arco."],
            width=6.4,
            title_size=32,
            body_size=30,
            fill_color=PAPER_GRAY,
        ).move_to([3.65, 0.15, 0])
        self.assert_content_safe(VGroup(sec, r1, r2, r_label, theta, prompt), "sector prompt")

        self.play(Create(sec), Create(r1), Create(r2), Write(r_label), Write(theta), FadeIn(prompt), run_time=RUN_NORMAL)
        self._v4_zoom(VGroup(sec, r1, r2, r_label, theta), width=6.8, pause=V4_THINK)
        self.wait(V4_THINK)
        self.play(FadeOut(prompt), run_time=RUN_NORMAL)

        p1 = self._v4_formula_panel(r"A=\frac{60}{360}\pi(12)^2=24\pi\approx75.40\text{ cm}^2", width=7.0, height=1.35, size=40).move_to([3.45, 1.20, 0])
        p2 = self._v4_formula_panel(r"L=\frac{60}{360}(2\pi\cdot12)=4\pi\approx12.57\text{ cm}", width=7.0, height=1.35, size=40).move_to([3.45, -0.45, 0])
        p3 = self._v4_formula_panel(r"P=L+2r\approx12.57+24=\boxed{36.57\text{ cm}}", width=7.0, height=1.35, size=40).move_to([3.45, -2.10, 0])
        self.assert_content_safe(VGroup(sec, r1, r2, p1, p2, p3), "sector solution")
        self._show_formula(p1, zoom_width=7.6, pause=V4_EXPLAIN)
        self._show_formula(p2, zoom_width=7.6, pause=V4_EXPLAIN)
        self._show_formula(p3, zoom_width=7.6, pause=V4_THINK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Independent practice
    # ------------------------------------------------------------------
    def independent_practice(self) -> None:
        self._v4_header(
            12,
            "AHORA TÚ — PRÁCTICA INDEPENDIENTE",
            "Identifica el dato, elige la fórmula y escribe siempre la unidad correcta antes de comparar respuestas.",
        )
        problems = [
            "1. r = 9 cm → determina d y C.",
            "2. d = 24 cm → determina r y A.",
            "3. C = 62.83 cm → estima d y r.",
            "4. Semicírculo: r = 4 m → determina A y P.",
            "5. Sector: r = 6 cm y θ = 120° → determina A y longitud de arco.",
        ]
        cards = VGroup()
        for i, text in enumerate(problems):
            card = self._v4_text_panel(
                f"PROBLEMA {i+1}",
                [text],
                width=6.35,
                title_size=31,
                body_size=30,
                fill_color=WHITE,
            )
            cards.add(card)
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.35, 0.32), flow_order="rd")
        self.fit(cards, 13.4, 5.65)
        cards.move_to(DOWN * 0.30)
        self.assert_content_safe(cards, "independent practice cards")

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.14), run_time=RUN_SLOW * 1.70)
        self.wait(V4_THINK)
        for card in cards:
            self._v4_zoom(card, width=7.0, pause=V4_READ)
        self.wait(V4_FINAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Final method summary
    # ------------------------------------------------------------------
    def final_summary(self) -> None:
        self._v4_header(
            13,
            "MÉTODO FINAL — CINCO DECISIONES",
            "La meta no es memorizar un ejemplo: es reconocer qué medida conoces y qué región debes calcular.",
        )
        steps = [
            ("1", "LEE", "¿Qué dato conozco?"),
            ("2", "DIBUJA", "Marca r, d, arco o región."),
            ("3", "ELIGE", "Selecciona la fórmula adecuada."),
            ("4", "CALCULA", "Sustituye y conserva unidades."),
            ("5", "VERIFICA", "Longitud o área: ¿cm o cm²?"),
        ]
        cards = VGroup()
        for num, title, note in steps:
            content = VGroup(
                self.text(num, 38, BOLD),
                self.text(title, 32, BOLD),
                self.text(note, 27),
            ).arrange(DOWN, buff=0.12)
            cards.add(self._v4_panel(content, width=2.62, height=2.55, fill_color=PAPER_GRAY))
        cards.arrange(RIGHT, buff=0.24).move_to(DOWN * 0.10)
        self.assert_content_safe(cards, "final method cards")

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.14), run_time=RUN_SLOW * 1.80)
        self.wait(V4_READ)
        for card in cards:
            self._v4_zoom(card, width=4.8, pause=V4_READ)
        self.wait(V4_SUMMARY)

        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        closing = VGroup(
            self.text("RADIO • DIÁMETRO • PERÍMETRO • ÁREA • REGIONES", 50, BOLD),
            self.text("Dibuja. Elige. Calcula. Verifica la unidad.", 39),
        ).arrange(DOWN, buff=0.40).move_to(ORIGIN)
        self.fit(closing, 14.0, 3.2)
        self.play(FadeIn(closing, shift=UP * 0.14), run_time=RUN_SLOW)
        self.wait(V4_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)
