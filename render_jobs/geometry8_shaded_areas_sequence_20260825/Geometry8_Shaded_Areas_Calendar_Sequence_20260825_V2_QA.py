#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 QA overrides for the Geometry 8 calendar continuation.

Compatibility target: ManimCE 0.20.1.  This layer fixes Sector construction,
preserves projector-safe separation, and keeps portable MathTex identifiers.
"""
from __future__ import annotations

from manim import *
from jp_classroom_style import *
from Geometry8_Shaded_Areas_Calendar_Sequence_20260825 import (
    Geometry8Week4SimpleShadedAreas,
    Geometry8Week5ComplexShadedAreas,
    Geometry8Week6ScalingPerimeterArea,
    Geometry8Week7IntegratedAreaPerimeterChallenge,
    COPY,
)


class Geometry8Week4SimpleShadedAreasV2(Geometry8Week4SimpleShadedAreas):
    """ManimCE 0.20.1-compatible quadrant construction."""

    def example_square_quadrant(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CUADRADO MENOS CUADRANTE", "Un cuadrante es un cuarto de círculo: 90° de 360°.")
        s = 4.6
        sq = Square(side_length=s, stroke_color=BLACK_LINE, stroke_width=5,
                    fill_color=LIGHT_GRAY, fill_opacity=0.55)
        corner = sq.get_corner(DL)
        sector = Sector(
            radius=s,
            angle=PI / 2,
            start_angle=0,
            arc_center=corner,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        radius_label = self.math(r"r=8\,\mathrm{cm}", 36).move_to(corner + RIGHT * 2.3 + DOWN * 0.35)
        side_label = self.text("8 cm", 31, BOLD).next_to(sq, LEFT, buff=0.18)
        diagram = VGroup(sq, sector, radius_label, side_label)
        card = self.notebook_card(
            "CUADRANTE = 1/4 DEL CÍRCULO",
            ["Área del cuadrado: 8² = 64.", "Área del cuadrante: 16π.", "La esquina gris es la diferencia."],
            r"A_s=64-16\pi\approx13.73\,\mathrm{cm}^2",
        )
        self.two_column(diagram, card)
        self.play(Create(sq), run_time=RUN_NORMAL)
        self.play(FadeIn(sector), FadeIn(VGroup(radius_label, side_label)), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()


class Geometry8Week5ComplexShadedAreasV2(Geometry8Week5ComplexShadedAreas):
    """ManimCE 0.20.1-compatible four-quadrant construction."""

    def four_quadrants_example(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CUATRO CUADRANTES", "Cuatro cuartos de círculo forman exactamente un círculo completo.")
        side = 4.8
        sq = Square(side_length=side, stroke_color=BLACK_LINE, stroke_width=5,
                    fill_color=LIGHT_GRAY, fill_opacity=0.65)
        corners = [sq.get_corner(DL), sq.get_corner(DR), sq.get_corner(UR), sq.get_corner(UL)]
        starts = [0, PI / 2, PI, 3 * PI / 2]
        sectors = VGroup(*[
            Sector(
                radius=side / 2,
                angle=PI / 2,
                start_angle=a,
                arc_center=c,
                stroke_color=BLACK_LINE,
                stroke_width=3,
                fill_color=WHITE,
                fill_opacity=1,
            )
            for c, a in zip(corners, starts)
        ])
        label = self.text("lado = 12 cm · radio = 6 cm", 30, BOLD).next_to(sq, DOWN, buff=0.15)
        diagram = VGroup(sq, sectors, label)
        card = self.notebook_card(
            "SIMPLIFICA ANTES DE CALCULAR",
            ["4 cuadrantes = 1 círculo.", "Área del cuadrado: 144.", "Área de los 4 cuadrantes: 36π."],
            r"A_s=144-36\pi\approx30.90\,\mathrm{cm}^2",
        )
        self.two_column(diagram, card)
        self.play(Create(sq), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.12), FadeIn(label), run_time=RUN_SLOW * 1.3)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()


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
        g1 = VGroup(c1, self.math("r=3", 36).next_to(c1, DOWN, buff=0.12), self.math(r"C=6\pi,\;A=9\pi", 34).next_to(c1, UP, buff=0.12))
        g2 = VGroup(c2, self.math("r=6", 36).next_to(c2, DOWN, buff=0.12), self.math(r"C=12\pi,\;A=36\pi", 34).next_to(c2, UP, buff=0.12))
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
            self.math(r"r_p=3\,\mathrm{m}", 34).next_to(pond, UP, buff=0.12),
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
