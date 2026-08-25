#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 QA overrides for the Geometry 8 calendar continuation.

The base lesson file contains the full pedagogical sequence. This revision keeps that
content while widening the separation between the scaling diagrams and explanation
panel, and uses accent-free MathTex identifiers in the integrated garden example.
"""
from __future__ import annotations

from manim import *
from jp_classroom_style import *
from Geometry8_Shaded_Areas_Calendar_Sequence_20260825 import (
    Geometry8Week4SimpleShadedAreas,
    Geometry8Week5ComplexShadedAreas,
    Geometry8Week6ScalingPerimeterArea,
    Geometry8Week7IntegratedAreaPerimeterChallenge,
    Geometry8ContinuationBase,
    COPY,
)


class Geometry8Week4SimpleShadedAreasV2(Geometry8Week4SimpleShadedAreas):
    pass


class Geometry8Week5ComplexShadedAreasV2(Geometry8Week5ComplexShadedAreas):
    pass


class Geometry8Week6ScalingPerimeterAreaV2(Geometry8Week6ScalingPerimeterArea):
    """Safer projector spacing for both scaling examples."""

    def rectangle_example(self) -> None:
        self.section_header(2, "EJEMPLO 1 · RECTÁNGULO CON k = 3", "Comparar lado, perímetro y área en la misma pantalla evita la confusión.")
        small = Rectangle(width=2.55, height=1.45, stroke_color=BLACK_LINE, stroke_width=5, fill_color=PAPER_GRAY, fill_opacity=1)
        large = Rectangle(width=4.75, height=2.70, stroke_color=BLACK_LINE, stroke_width=5, fill_color=LIGHT_GRAY, fill_opacity=0.55)
        small_label = VGroup(self.text("4 × 7", 34, BOLD), self.text("P = 22 · A = 28", 30)).arrange(DOWN, buff=0.12).next_to(small, DOWN, buff=0.14)
        large_label = VGroup(self.text("12 × 21", 34, BOLD), self.text("P = 66 · A = 252", 30)).arrange(DOWN, buff=0.12).next_to(large, DOWN, buff=0.14)
        diagrams = VGroup(VGroup(small, small_label), VGroup(large, large_label)).arrange(RIGHT, buff=0.55)
        diagrams.move_to(LEFT * 3.45 + DOWN * 0.30)
        card = self.notebook_card(
            "COMPARACIÓN",
            ["Lados: ×3.", "Perímetro: 22 → 66 = ×3.", "Área: 28 → 252 = ×9."],
            r"k=3\Rightarrow P' =3P,\quad A'=9A",
            width=5.25,
        ).move_to(RIGHT * 4.65 + DOWN * 0.35)
        group = VGroup(diagrams, card)
        self.assert_content_safe(group, "V2 rectangle scaling separated layout")
        assert diagrams.get_right()[0] < card.get_left()[0] - 0.08
        self.play(Create(small), FadeIn(small_label), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(small, large), FadeIn(large_label), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()

    def circle_example(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CÍRCULO CON k = 2", "Duplicar el radio duplica la circunferencia, pero cuadruplica el área.")
        c1 = Circle(radius=1.05, stroke_color=BLACK_LINE, stroke_width=5, fill_color=WHITE, fill_opacity=1)
        c2 = Circle(radius=1.85, stroke_color=BLACK_LINE, stroke_width=5, fill_color=LIGHT_GRAY, fill_opacity=0.35)
        g1 = VGroup(c1, self.math("r=3", 36).next_to(c1, DOWN, buff=0.12), self.math("C=6\pi,\;A=9\pi", 34).next_to(c1, UP, buff=0.12))
        g2 = VGroup(c2, self.math("r=6", 36).next_to(c2, DOWN, buff=0.12), self.math("C=12\pi,\;A=36\pi", 34).next_to(c2, UP, buff=0.12))
        diagrams = VGroup(g1, g2).arrange(RIGHT, buff=0.65).move_to(LEFT * 3.55 + DOWN * 0.30)
        card = self.notebook_card(
            "RADIO ×2",
            ["Circunferencia: ×2.", "Área: ×4.", "El exponente 2 explica el cambio del área."],
            r"k=2\Rightarrow P' =2P,\quad A'=4A",
            width=5.20,
        ).move_to(RIGHT * 4.70 + DOWN * 0.35)
        group = VGroup(diagrams, card)
        self.assert_content_safe(group, "V2 circle scaling separated layout")
        assert diagrams.get_right()[0] < card.get_left()[0] - 0.08
        self.play(Create(c1), FadeIn(VGroup(g1[1], g1[2])), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(c1, c2), FadeIn(VGroup(g2[1], g2[2])), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()


class Geometry8Week7IntegratedAreaPerimeterChallengeV2(Geometry8Week7IntegratedAreaPerimeterChallenge):
    """Use simple MathTex identifiers for maximum pdfLaTeX portability."""

    def garden_problem(self) -> None:
        self.section_header(3, "PROBLEMA MODELO · JARDÍN CON ESTANQUE", "La superficie de césped es una resta; la cerca exterior es un perímetro distinto.")
        rect = Rectangle(width=5.6, height=3.35, stroke_color=BLACK_LINE, stroke_width=5,
                         fill_color=LIGHT_GRAY, fill_opacity=0.55)
        pond = Circle(radius=0.90, stroke_color=BLACK_LINE, stroke_width=5, fill_color=WHITE, fill_opacity=1)
        labels = VGroup(
            self.text("20 m × 12 m", 31, BOLD).next_to(rect, DOWN, buff=0.14),
            self.math("r_p=3\,\mathrm{m}", 34).next_to(pond, UP, buff=0.12),
        )
        diagram = VGroup(rect, pond, labels)
        card = self.notebook_card(
            "DOS PREGUNTAS, DOS MAGNITUDES",
            ["Césped: rectángulo − estanque.", "Cerca exterior: perímetro del rectángulo.", "El borde del estanque solo cuenta si lo preguntan."],
            r"A_s=240-9\pi\approx211.73\,\mathrm{m}^2\\P_{ext}=64\,\mathrm{m}",
        )
        self.two_column(diagram, card)
        self.play(Create(rect), Create(pond), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 3)
        self.clear_stage()
