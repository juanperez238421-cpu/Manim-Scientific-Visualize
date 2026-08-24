#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle Exercises Workshop V4 — Large Text Projector Edition.

Purpose: preserve the accepted V3 geometry/animation while substantially increasing
classroom readability. The layout deliberately shows less text at once instead of
shrinking typography.
"""
from __future__ import annotations

from manim import *
from jp_classroom_style import *
from Geometry8_Circle_V4_Senior_QA import V4_READ, V4_EXPLAIN, V4_THINK, V4_SUMMARY, V4_FINAL
from Geometry8_Circle_Exercises_Workshop_20260824_V3 import Geometry8CircleExercisesWorkshop20260824V3


class Geometry8CircleExercisesWorkshop20260824V4LargeText(Geometry8CircleExercisesWorkshop20260824V3):
    """Projector-first V4: same figures, larger text, fewer simultaneous words."""

    # Static-QA markers inherited from the full V3 scene:
    # exercise_09_sector
    # self._v4_zoom
    # assert_content_safe

    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()

    # ------------------------------------------------------------------
    # Global typography upgrades
    # ------------------------------------------------------------------
    def _v4_text_panel(
        self,
        title,
        body_lines,
        *,
        width=6.4,
        title_size=34,
        body_size=30,
        fill_color=WHITE,
        **kwargs,
    ):
        """Increase panel typography without allowing text to become microscopic."""
        title_size = max(title_size, 38)
        body_size = max(body_size, 36)
        return super()._v4_text_panel(
            title,
            body_lines,
            width=width,
            title_size=title_size,
            body_size=body_size,
            fill_color=fill_color,
            **kwargs,
        )

    def _v4_formula_panel(self, tex, *, width=6.0, height=1.35, size=56, **kwargs):
        """Make worked equations dominant on screen."""
        size = max(size, 64)
        return super()._v4_formula_panel(tex, width=width, height=height, size=size, **kwargs)

    # ------------------------------------------------------------------
    # Opening: larger and simpler
    # ------------------------------------------------------------------
    def opening_workshop(self) -> None:
        course = self.text("GEOMETRÍA 8", 38, BOLD)
        title = self.text("TALLER ANIMADO — CÍRCULO", 62, BOLD)
        subtitle = self.text("Radio • diámetro • perímetro • área • regiones", 40)
        self.fit(title, 13.6, 0.92)
        self.fit(subtitle, 13.2, 0.82)

        center = LEFT * 3.8 + DOWN * 0.55
        circle = Circle(radius=2.05, stroke_color=BLACK_LINE, stroke_width=7).move_to(center)
        center_dot = Dot(center, radius=0.085, color=BLACK_LINE)
        radius = Line(center, center + RIGHT * 2.05, color=BLACK_LINE, stroke_width=6)
        diameter = Line(center + LEFT * 2.05, center + RIGHT * 2.05, color=LIGHT_GRAY, stroke_width=4)

        cards = VGroup(
            self._v4_formula_panel(r"d=2r", width=4.8, height=1.35, size=70),
            self._v4_formula_panel(r"C=\pi d=2\pi r", width=5.8, height=1.35, size=66),
            self._v4_formula_panel(r"A=\pi r^2", width=5.2, height=1.35, size=70),
        ).arrange(DOWN, buff=0.30).move_to([3.55, -0.55, 0])

        top = VGroup(course, title, subtitle).arrange(DOWN, buff=0.26).move_to(UP * 2.15)
        group = VGroup(top, circle, center_dot, radius, diameter, cards)
        self.assert_within_frame(group, "V4 large-text opening", margin=0.16)

        self.play(FadeIn(course, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW * 1.20)
        self.play(Write(subtitle), run_time=RUN_NORMAL)
        self.wait(V4_READ)
        self.play(Create(circle), FadeIn(center_dot), run_time=RUN_NORMAL)
        self.play(GrowFromPoint(radius, center), Create(diameter), run_time=RUN_NORMAL)
        for card in cards:
            self.play(Create(card[0]), Write(card[1]), run_time=RUN_NORMAL)
            self._v4_zoom(card, width=6.5, pause=V4_READ)
        self.wait(V4_SUMMARY)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    # ------------------------------------------------------------------
    # Formula map: one formula at a time at near-full width
    # ------------------------------------------------------------------
    def reference_map(self) -> None:
        self._v4_header(
            1,
            "MAPA DE FÓRMULAS",
            "Primero decide qué magnitud debes encontrar.",
        )
        rows = [
            (r"d=2r", "DIÁMETRO", "dos radios"),
            (r"r=\frac{d}{2}", "RADIO", "mitad del diámetro"),
            (r"C=\pi d=2\pi r", "PERÍMETRO", "longitud del borde"),
            (r"A=\pi r^2", "ÁREA", "superficie interior"),
        ]
        for expr, name, note in rows:
            title = self.text(name, 46, BOLD)
            formula = self.math(expr, 82)
            desc = self.text(note, 38)
            content = VGroup(title, formula, desc).arrange(DOWN, buff=0.30)
            panel = self._v4_panel(content, width=11.6, height=3.2, fill_color=WHITE).move_to(DOWN * 0.20)
            self.assert_content_safe(panel, f"V4 formula map {name}")
            self.play(Create(panel[0]), FadeIn(title), Write(formula), FadeIn(desc), run_time=RUN_SLOW * 1.15)
            self._v4_zoom(panel, width=12.2, pause=V4_EXPLAIN)
            self.play(FadeOut(panel), run_time=RUN_NORMAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Independent practice: one large problem card at a time
    # ------------------------------------------------------------------
    def independent_practice(self) -> None:
        self._v4_header(
            12,
            "AHORA TÚ — PRÁCTICA INDEPENDIENTE",
            "Un problema por pantalla. Identifica el dato y escribe la fórmula antes de calcular.",
        )
        problems = [
            ("PROBLEMA 1", "r = 9 cm", "Determina d y C."),
            ("PROBLEMA 2", "d = 24 cm", "Determina r y A."),
            ("PROBLEMA 3", "C = 62.83 cm", "Estima d y r."),
            ("PROBLEMA 4", "Semicírculo: r = 4 m", "Determina A y P."),
            ("PROBLEMA 5", "Sector: r = 6 cm, θ = 120°", "Determina A y longitud de arco."),
        ]

        for title_txt, datum, task in problems:
            title = self.text(title_txt, 46, BOLD)
            datum_mob = self.text(datum, 52, BOLD)
            task_mob = self.text(task, 42)
            content = VGroup(title, datum_mob, task_mob).arrange(DOWN, buff=0.38)
            self.fit(content, 10.8, 3.8)
            panel = self._v4_panel(content, width=11.8, height=4.3, fill_color=WHITE).move_to(DOWN * 0.10)
            self.assert_content_safe(panel, f"V4 independent {title_txt}")
            self.play(Create(panel[0]), Write(title), FadeIn(datum_mob), Write(task_mob), run_time=RUN_SLOW * 1.15)
            self._v4_zoom(panel, width=12.2, pause=V4_THINK)
            self.wait(V4_THINK)
            self.play(FadeOut(panel), run_time=RUN_NORMAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Final summary: full-screen steps instead of five small cards
    # ------------------------------------------------------------------
    def final_summary(self) -> None:
        self._v4_header(
            13,
            "MÉTODO FINAL",
            "Cinco decisiones para resolver cualquier ejercicio del taller.",
        )
        steps = [
            ("1", "LEE", "¿Qué dato conozco?"),
            ("2", "DIBUJA", "Marca radio, diámetro, arco o región."),
            ("3", "ELIGE", "Selecciona la fórmula adecuada."),
            ("4", "CALCULA", "Sustituye y conserva las unidades."),
            ("5", "VERIFICA", "¿La respuesta es longitud o área?"),
        ]
        for num, title_txt, note in steps:
            num_mob = self.text(num, 74, BOLD)
            title = self.text(title_txt, 58, BOLD)
            body = self.text(note, 44)
            self.fit(body, 11.0, 0.90)
            content = VGroup(num_mob, title, body).arrange(DOWN, buff=0.36)
            panel = self._v4_panel(content, width=11.8, height=4.2, fill_color=PAPER_GRAY).move_to(DOWN * 0.10)
            self.assert_content_safe(panel, f"V4 final step {num}")
            self.play(Create(panel[0]), Write(num_mob), Write(title), FadeIn(body), run_time=RUN_SLOW * 1.10)
            self._v4_zoom(panel, width=12.2, pause=V4_READ)
            self.wait(V4_READ)
            self.play(FadeOut(panel), run_time=RUN_NORMAL)

        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        closing = VGroup(
            self.text("RADIO • DIÁMETRO • PERÍMETRO", 52, BOLD),
            self.text("ÁREA • REGIONES", 58, BOLD),
            self.text("Dibuja • Elige • Calcula • Verifica", 42),
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        self.fit(closing, 13.7, 4.3)
        self.play(FadeIn(closing, shift=UP * 0.12), run_time=RUN_SLOW)
        self.wait(V4_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)
