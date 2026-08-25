#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — calendar-aligned continuation after the Circle unit.

Sequence encoded from the current third-period planning:
- Week 4 (Sep 7–11): simple shaded areas.
- Week 5 (Sep 14–18): complex shaded areas.
- Week 6 (Sep 21–25): perimeter vs area under scaling.
- Week 7 (Sep 28–Oct 2): integrated area/perimeter challenge.

Target: Manim Community Edition 0.20.1 + audited JP classroom style.
Design: Full HD 16:9, white background, black/gray hierarchy, projector-scale text,
explicit notebook pauses, strict safe-frame checks, no decorative color dependence.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *

COPY = 6.0
READ = 4.0
THINK = 6.0
SUMMARY = 7.0


class Geometry8ContinuationBase(JPMathClassroomScene):
    """Shared large-text visual grammar for the four scheduled continuation lessons."""

    def section_header(self, number: int, title: str, subtitle: str) -> None:
        old = [m for m in (self.header_group, self.subtitle_group) if m is not None]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=RUN_QUICK)
            self.remove(*old)
            self.header_group = None
            self.subtitle_group = None
        JPMathClassroomScene.set_header(self, number, title, subtitle)

    def panel(self, content: Mobject, *, width: float = 6.2, height: float = 4.7,
              fill_color=WHITE, stroke_width: float = 2.4) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            stroke_color=BLACK_LINE,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=1.0,
        )
        self.fit(content, width - 0.65, height - 0.55)
        content.move_to(box)
        return VGroup(box, content)

    def notebook_card(self, title: str, lines: list[str], formula: str | None = None,
                      *, width: float = 6.35, height: float = 4.65) -> VGroup:
        title_m = self.text(title, 40, BOLD)
        body = VGroup(*[self.text(line, 32) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        pieces: list[Mobject] = [title_m, body]
        if formula:
            pieces.append(self.math(formula, 52))
        content = VGroup(*pieces).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        card = self.panel(content, width=width, height=height, fill_color=WHITE)
        content.align_to(card[0], LEFT).shift(RIGHT * 0.30)
        return card

    def formula_card(self, expression: str, caption: str, *, width: float = 6.0) -> VGroup:
        formula = self.math(expression, 66)
        text = self.text(caption, 34)
        content = VGroup(formula, text).arrange(DOWN, buff=0.25)
        return self.panel(content, width=width, height=2.05, fill_color=PAPER_GRAY)

    def two_column(self, left: Mobject, right: Mobject, *, y: float = -0.45) -> VGroup:
        left.move_to(LEFT * 3.75 + UP * y)
        right.move_to(RIGHT * 3.55 + UP * y)
        group = VGroup(left, right)
        self.assert_content_safe(group, "two-column continuation layout")
        return group

    def centered_step(self, title: str, body: str, formula: str | None = None,
                      *, fill=PAPER_GRAY) -> VGroup:
        title_m = self.text(title, 48, BOLD)
        body_m = self.text(body, 39)
        self.fit(body_m, 11.2, 1.2)
        parts: list[Mobject] = [title_m, body_m]
        if formula:
            parts.append(self.math(formula, 64))
        content = VGroup(*parts).arrange(DOWN, buff=0.33)
        out = self.panel(content, width=12.0, height=4.1, fill_color=fill).move_to(DOWN * 0.20)
        self.assert_content_safe(out, f"centered step {title}")
        return out

    def animate_step(self, card: VGroup, pause: float = READ) -> None:
        self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
        self.wait(pause)
        self.play(FadeOut(card), run_time=RUN_NORMAL)

    def problem_card(self, number: int, prompt: str, data: str) -> VGroup:
        badge = self.text(f"PROBLEMA {number}", 44, BOLD)
        prompt_m = self.text(prompt, 40)
        data_m = self.text(data, 44, BOLD)
        self.fit(prompt_m, 10.8, 1.25)
        content = VGroup(badge, prompt_m, data_m).arrange(DOWN, buff=0.34)
        out = self.panel(content, width=11.9, height=3.9, fill_color=WHITE).move_to(DOWN * 0.10)
        self.assert_content_safe(out, f"practice problem {number}")
        return out

    def fade_all(self) -> None:
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        self.header_group = None
        self.subtitle_group = None


class Geometry8Week4SimpleShadedAreas(Geometry8ContinuationBase):
    """Week 4 — simple shaded areas after the circle-area consolidation."""

    def validate_lesson_data(self) -> None:
        self.rect_shaded = 12 * 10 - math.pi * 3**2
        self.quadrant_shaded = 8**2 - math.pi * 8**2 / 4
        assert abs(self.rect_shaded - 91.7256661177) < 1e-8
        assert abs(self.quadrant_shaded - 13.7345175426) < 1e-8

    def construct(self) -> None:
        self.standard_opening(
            "GEOMETRÍA 8 · SEMANA 4",
            "ÁREAS SOMBREADAS SIMPLES",
            "Restar áreas conocidas para encontrar la región que realmente importa",
            "Dibuja primero. Decide qué quitar. Calcula al final.",
        )
        self.idea()
        self.example_rectangle_circle()
        self.example_square_quadrant()
        self.decision_rule()
        self.practice()
        self.summary()

    def idea(self) -> None:
        self.section_header(1, "IDEA CENTRAL", "Una región sombreada simple suele resolverse con una resta de áreas conocidas.")
        card = self.centered_step(
            "ÁREA SOMBREADA = ÁREA TOTAL − ÁREA QUE NO QUIERO",
            "La figura exterior da el total; la figura interior indica qué debemos quitar.",
            r"A_s=A_T-A_N",
        )
        self.animate_step(card, COPY)
        self.clear_stage()

    def example_rectangle_circle(self) -> None:
        self.section_header(2, "EJEMPLO 1 · RECTÁNGULO MENOS CÍRCULO", "Mantén las dos figuras visibles mientras escribes la resta.")
        rect = Rectangle(width=5.2, height=4.2, stroke_color=BLACK_LINE, stroke_width=5,
                         fill_color=LIGHT_GRAY, fill_opacity=0.55)
        circ = Circle(radius=1.25, stroke_color=BLACK_LINE, stroke_width=5,
                      fill_color=WHITE, fill_opacity=1.0)
        d1 = DoubleArrow(rect.get_left(), rect.get_right(), buff=0, color=BLACK_LINE, stroke_width=2.4)
        d1.next_to(rect, DOWN, buff=0.18)
        d2 = DoubleArrow(rect.get_bottom(), rect.get_top(), buff=0, color=BLACK_LINE, stroke_width=2.4)
        d2.next_to(rect, LEFT, buff=0.18)
        labels = VGroup(
            self.text("12 cm", 30, BOLD).next_to(d1, DOWN, buff=0.08),
            self.text("10 cm", 30, BOLD).next_to(d2, LEFT, buff=0.08).rotate(PI / 2),
            self.math("r=3\,\mathrm{cm}", 36).next_to(circ, UP, buff=0.18),
        )
        diagram = VGroup(rect, circ, d1, d2, labels)
        card = self.notebook_card(
            "COPIA EL PROCEDIMIENTO",
            ["1. Área total: rectángulo.", "2. Área blanca: círculo.", "3. Resta total − círculo."],
            r"A_s=120-9\pi\approx91.73\,\mathrm{cm}^2",
        )
        self.two_column(diagram, card)
        self.play(Create(rect), run_time=RUN_NORMAL)
        self.play(Create(circ), FadeIn(VGroup(d1, d2, labels)), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()

    def example_square_quadrant(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CUADRADO MENOS CUADRANTE", "Un cuadrante es un cuarto de círculo: 90° de 360°.")
        s = 4.6
        sq = Square(side_length=s, stroke_color=BLACK_LINE, stroke_width=5,
                    fill_color=LIGHT_GRAY, fill_opacity=0.55)
        corner = sq.get_corner(DL)
        sector = Sector(
            outer_radius=s,
            inner_radius=0,
            angle=PI/2,
            start_angle=0,
            arc_center=corner,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        radius_label = self.math("r=8\,\mathrm{cm}", 36).move_to(corner + RIGHT * 2.3 + DOWN * 0.35)
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

    def decision_rule(self) -> None:
        self.section_header(4, "REGLA DE DECISIÓN", "Antes de calcular, nombra la figura total y la figura que se resta.")
        for title, body, formula in [
            ("PASO 1 · IDENTIFICA EL TOTAL", "¿Rectángulo, cuadrado, círculo, semicírculo o cuadrante?", None),
            ("PASO 2 · IDENTIFICA LO BLANCO", "Esa región es la que debes quitar del total.", None),
            ("PASO 3 · ESCRIBE LA RESTA", "No sustituyas números hasta tener clara la estructura.", r"A_s=A_T-A_N"),
            ("PASO 4 · UNIDADES", "El área siempre termina en unidades cuadradas.", r"\mathrm{cm}^2,\;\mathrm{m}^2"),
        ]:
            self.animate_step(self.centered_step(title, body, formula), READ)
        self.clear_stage()

    def practice(self) -> None:
        self.section_header(5, "WORKSHOP · PRÁCTICA GUIADA", "Primero dibuja. Después escribe la resta. No empieces con la calculadora.")
        problems = [
            ("Cuadrado de lado 10 cm con círculo interior de radio 3 cm.", "Encuentra el área sombreada fuera del círculo."),
            ("Rectángulo 15 cm × 8 cm con un semicírculo de radio 4 cm.", "Resta el semicírculo al rectángulo."),
            ("Cuadrado de lado 12 cm con un cuadrante de radio 12 cm.", "Encuentra la región que queda fuera del cuadrante."),
        ]
        for i, (data, task) in enumerate(problems, 1):
            card = self.problem_card(i, task, data)
            self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
            self.wait(THINK)
            self.play(FadeOut(card), run_time=RUN_NORMAL)
        self.clear_stage()

    def summary(self) -> None:
        self.section_header(6, "CIERRE DE SEMANA 4", "La clave no es memorizar dibujos: es reconocer una resta de áreas conocidas.")
        card = self.centered_step("MÉTODO", "Total → identifica lo que se quita → resta → verifica unidades cuadradas.", r"A_s=A_T-A_N")
        self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
        self.wait(SUMMARY)
        self.fade_all()


class Geometry8Week5ComplexShadedAreas(Geometry8ContinuationBase):
    """Week 5 — complex shaded areas with decomposition and multiple subtractions."""

    def validate_lesson_data(self) -> None:
        self.annulus = math.pi * (6**2 - 3**2)
        self.central = 12**2 - math.pi * 6**2
        self.rect_circle = 14 * 8 - math.pi * 4**2
        assert abs(self.annulus - 84.8230016469) < 1e-8
        assert abs(self.central - 30.9026644708) < 1e-8
        assert abs(self.rect_circle - 61.7345175426) < 1e-8

    def construct(self) -> None:
        self.standard_opening(
            "GEOMETRÍA 8 · SEMANA 5",
            "ÁREAS SOMBREADAS COMPLEJAS",
            "Descomponer una figura en piezas simples antes de calcular",
            "Una figura difícil se vuelve manejable cuando decides qué sumar y qué restar.",
        )
        self.strategy()
        self.annulus_example()
        self.four_quadrants_example()
        self.multiple_removal_example()
        self.practice()
        self.summary()

    def strategy(self) -> None:
        self.section_header(1, "ESTRATEGIA DE DESCOMPOSICIÓN", "No busques una fórmula nueva: combina fórmulas que ya conoces.")
        for title, body, formula in [
            ("1 · SEPARA", "Divide mentalmente la figura en rectángulos, círculos, semicírculos o cuadrantes.", None),
            ("2 · DECIDE SIGNOS", "Las piezas que pertenecen a la sombra se suman; los huecos se restan.", r"A_s=\sum A_{+}-\sum A_{-}"),
            ("3 · CALCULA AL FINAL", "Primero construye la expresión completa; después sustituye valores.", None),
        ]:
            self.animate_step(self.centered_step(title, body, formula), READ)
        self.clear_stage()

    def annulus_example(self) -> None:
        self.section_header(2, "EJEMPLO 1 · CORONA CIRCULAR", "La región entre dos círculos concéntricos es una resta directa.")
        outer = Circle(radius=2.25, stroke_color=BLACK_LINE, stroke_width=5,
                       fill_color=LIGHT_GRAY, fill_opacity=0.65)
        inner = Circle(radius=1.12, stroke_color=BLACK_LINE, stroke_width=5,
                       fill_color=WHITE, fill_opacity=1.0)
        labels = VGroup(
            self.math("R=6\,\mathrm{cm}", 37).next_to(outer, UP, buff=0.16),
            self.math("r=3\,\mathrm{cm}", 37).next_to(inner, DOWN, buff=0.14),
        )
        diagram = VGroup(outer, inner, labels)
        card = self.notebook_card(
            "CORONA CIRCULAR",
            ["Área grande − área pequeña.", "Ambos círculos tienen el mismo centro.", "Factoriza π para revisar el cálculo."],
            r"A=\pi(6^2-3^2)=27\pi\approx84.82\,\mathrm{cm}^2",
        )
        self.two_column(diagram, card)
        self.play(Create(outer), Create(inner), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()

    def four_quadrants_example(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CUATRO CUADRANTES", "Cuatro cuartos de círculo forman exactamente un círculo completo.")
        side = 4.8
        sq = Square(side_length=side, stroke_color=BLACK_LINE, stroke_width=5,
                    fill_color=LIGHT_GRAY, fill_opacity=0.65)
        corners = [sq.get_corner(DL), sq.get_corner(DR), sq.get_corner(UR), sq.get_corner(UL)]
        starts = [0, PI/2, PI, 3*PI/2]
        sectors = VGroup(*[
            Sector(outer_radius=side/2, angle=PI/2, start_angle=a, arc_center=c,
                   stroke_color=BLACK_LINE, stroke_width=3, fill_color=WHITE, fill_opacity=1)
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

    def multiple_removal_example(self) -> None:
        self.section_header(4, "EJEMPLO 3 · VARIAS PIEZAS", "Cuando hay varios huecos, agrúpalos antes de restarlos.")
        rect = Rectangle(width=5.5, height=3.2, stroke_color=BLACK_LINE, stroke_width=5,
                         fill_color=LIGHT_GRAY, fill_opacity=0.65)
        holes = VGroup(
            Circle(radius=0.70, stroke_color=BLACK_LINE, stroke_width=4, fill_color=WHITE, fill_opacity=1).shift(LEFT * 1.35),
            Circle(radius=0.70, stroke_color=BLACK_LINE, stroke_width=4, fill_color=WHITE, fill_opacity=1).shift(RIGHT * 1.35),
        )
        labels = VGroup(
            self.text("14 cm × 8 cm", 31, BOLD).next_to(rect, DOWN, buff=0.16),
            self.text("dos círculos iguales", 30).next_to(rect, UP, buff=0.15),
        )
        diagram = VGroup(rect, holes, labels)
        card = self.notebook_card(
            "AGRUPA LOS HUECOS",
            ["Total: rectángulo 14 × 8.", "Huecos: dos círculos iguales.", "Usa 2·A_círculo en una sola expresión."],
            r"A_s=112-2\pi r^2",
        )
        self.two_column(diagram, card)
        self.play(Create(rect), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Create(h) for h in holes], lag_ratio=0.20), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY)
        self.clear_stage()

    def practice(self) -> None:
        self.section_header(5, "WORKSHOP · ÁREAS COMPLEJAS", "Escribe primero la expresión completa con sumas y restas.")
        problems = [
            ("Corona circular con R = 10 cm y r = 6 cm.", "Calcula el área sombreada."),
            ("Cuadrado de lado 16 cm con cuatro cuadrantes de radio 8 cm.", "Calcula la región central."),
            ("Rectángulo 18 cm × 10 cm con dos círculos de radio 2 cm.", "Calcula el área que queda."),
            ("Círculo de radio 8 cm con dos huecos circulares de radio 2 cm.", "Calcula la región sombreada."),
        ]
        for i, (data, task) in enumerate(problems, 1):
            card = self.problem_card(i, task, data)
            self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
            self.wait(THINK)
            self.play(FadeOut(card), run_time=RUN_NORMAL)
        self.clear_stage()

    def summary(self) -> None:
        self.section_header(6, "CIERRE DE SEMANA 5", "La complejidad visual no cambia las fórmulas; cambia la organización.")
        card = self.centered_step("DESCOMPÓN → ASIGNA SIGNOS → CALCULA", "Convierte la figura en piezas conocidas y conserva una sola expresión hasta el final.", r"A_s=\sum A_{+}-\sum A_{-}")
        self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
        self.wait(SUMMARY)
        self.fade_all()


class Geometry8Week6ScalingPerimeterArea(Geometry8ContinuationBase):
    """Week 6 — perimeter and area under scale transformations."""

    def validate_lesson_data(self) -> None:
        assert 2 * (4 + 7) == 22
        assert 2 * (12 + 21) == 66
        assert 4 * 7 == 28
        assert 12 * 21 == 252
        assert 66 / 22 == 3
        assert 252 / 28 == 9

    def construct(self) -> None:
        self.standard_opening(
            "GEOMETRÍA 8 · SEMANA 6",
            "PERÍMETRO VS. ÁREA AL ESCALAR",
            "Entender qué cambia cuando una figura se agranda o se reduce",
            "Las longitudes crecen con k; las áreas crecen con k².",
        )
        self.core_rule()
        self.rectangle_example()
        self.circle_example()
        self.misconception()
        self.practice()
        self.summary()

    def core_rule(self) -> None:
        self.section_header(1, "REGLA DE ESCALA", "Si todas las longitudes se multiplican por k, perímetro y área no cambian igual.")
        length = self.formula_card(r"P' = kP", "Perímetro: una dimensión", width=5.7)
        area = self.formula_card(r"A' = k^2A", "Área: dos dimensiones", width=5.7)
        group = VGroup(length, area).arrange(DOWN, buff=0.40).move_to(DOWN * 0.15)
        self.assert_content_safe(group, "scaling core rule")
        self.play(FadeIn(length), run_time=RUN_NORMAL)
        self.wait(READ)
        self.play(FadeIn(area), run_time=RUN_NORMAL)
        self.wait(COPY)
        self.clear_stage()

    def rectangle_example(self) -> None:
        self.section_header(2, "EJEMPLO 1 · RECTÁNGULO CON k = 3", "Comparar lado, perímetro y área en la misma pantalla evita la confusión.")
        small = Rectangle(width=2.8, height=1.6, stroke_color=BLACK_LINE, stroke_width=5, fill_color=PAPER_GRAY, fill_opacity=1)
        large = Rectangle(width=5.3, height=3.0, stroke_color=BLACK_LINE, stroke_width=5, fill_color=LIGHT_GRAY, fill_opacity=0.55)
        small_label = VGroup(self.text("4 × 7", 34, BOLD), self.text("P = 22 · A = 28", 30)).arrange(DOWN, buff=0.12).next_to(small, DOWN, buff=0.14)
        large_label = VGroup(self.text("12 × 21", 34, BOLD), self.text("P = 66 · A = 252", 30)).arrange(DOWN, buff=0.12).next_to(large, DOWN, buff=0.14)
        diagrams = VGroup(VGroup(small, small_label), VGroup(large, large_label)).arrange(RIGHT, buff=0.75).move_to(LEFT * 2.7 + DOWN * 0.25)
        card = self.notebook_card(
            "COMPARACIÓN",
            ["Lados: ×3.", "Perímetro: 22 → 66 = ×3.", "Área: 28 → 252 = ×9."],
            r"k=3\Rightarrow P' =3P,\quad A'=9A",
            width=5.6,
        ).move_to(RIGHT * 4.45 + DOWN * 0.35)
        group = VGroup(diagrams, card)
        self.assert_content_safe(group, "rectangle scaling example")
        self.play(Create(small), FadeIn(small_label), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(small, large), FadeIn(large_label), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()

    def circle_example(self) -> None:
        self.section_header(3, "EJEMPLO 2 · CÍRCULO CON k = 2", "Duplicar el radio duplica la circunferencia, pero cuadruplica el área.")
        c1 = Circle(radius=1.25, stroke_color=BLACK_LINE, stroke_width=5, fill_color=WHITE, fill_opacity=1)
        c2 = Circle(radius=2.20, stroke_color=BLACK_LINE, stroke_width=5, fill_color=LIGHT_GRAY, fill_opacity=0.35)
        g1 = VGroup(c1, self.math("r=3", 36).next_to(c1, DOWN, buff=0.12), self.math("C=6\pi,\;A=9\pi", 34).next_to(c1, UP, buff=0.12))
        g2 = VGroup(c2, self.math("r=6", 36).next_to(c2, DOWN, buff=0.12), self.math("C=12\pi,\;A=36\pi", 34).next_to(c2, UP, buff=0.12))
        diagrams = VGroup(g1, g2).arrange(RIGHT, buff=0.85).move_to(LEFT * 2.8 + DOWN * 0.25)
        card = self.notebook_card(
            "RADIO ×2",
            ["Circunferencia: ×2.", "Área: ×4.", "El exponente 2 explica el cambio del área."],
            r"k=2\Rightarrow P' =2P,\quad A'=4A",
            width=5.5,
        ).move_to(RIGHT * 4.45 + DOWN * 0.35)
        self.assert_content_safe(VGroup(diagrams, card), "circle scaling example")
        self.play(Create(c1), FadeIn(VGroup(g1[1], g1[2])), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(c1, c2), FadeIn(VGroup(g2[1], g2[2])), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 2)
        self.clear_stage()

    def misconception(self) -> None:
        self.section_header(4, "ERROR TÍPICO", "No uses el mismo factor para área y perímetro.")
        wrong = self.centered_step("SI k = 4…", "Perímetro ×4, pero área NO es ×4.", r"A'=4^2A=16A")
        self.play(Create(wrong[0]), FadeIn(wrong[1]), run_time=RUN_SLOW)
        self.wait(COPY)
        self.play(FadeOut(wrong), run_time=RUN_NORMAL)
        self.clear_stage()

    def practice(self) -> None:
        self.section_header(5, "WORKSHOP · ESCALA", "Indica k antes de tocar las fórmulas.")
        problems = [
            ("Un cuadrado pasa de lado 5 cm a lado 15 cm.", "¿Por qué factor cambian P y A?"),
            ("Un círculo de radio 4 cm se reduce a radio 2 cm.", "¿Por qué factor cambian C y A?"),
            ("Una figura semejante tiene k = 1.5 y área original 40 cm².", "Calcula el área nueva."),
        ]
        for i, (data, task) in enumerate(problems, 1):
            card = self.problem_card(i, task, data)
            self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
            self.wait(THINK)
            self.play(FadeOut(card), run_time=RUN_NORMAL)
        self.clear_stage()

    def summary(self) -> None:
        self.section_header(6, "CIERRE DE SEMANA 6", "Piensa en dimensiones: longitud tiene una potencia; área tiene dos.")
        card = self.centered_step("REGLA FINAL", "Factor de escala k: longitudes y perímetros ×k; áreas ×k².", r"P'=kP\qquad A'=k^2A")
        self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
        self.wait(SUMMARY)
        self.fade_all()


class Geometry8Week7IntegratedAreaPerimeterChallenge(Geometry8ContinuationBase):
    """Week 7 — integrated perimeter/area problem solving."""

    def validate_lesson_data(self) -> None:
        self.stadium_area = 16 * 8 + math.pi * 4**2
        self.stadium_perimeter = 2 * 16 + 2 * math.pi * 4
        self.garden_grass = 20 * 12 - math.pi * 3**2
        assert abs(self.stadium_area - 178.2654824574) < 1e-8
        assert abs(self.stadium_perimeter - 57.1327412287) < 1e-8
        assert abs(self.garden_grass - 211.7256661177) < 1e-8

    def construct(self) -> None:
        self.standard_opening(
            "GEOMETRÍA 8 · SEMANA 7",
            "RETO INTEGRADO · ÁREA Y PERÍMETRO",
            "Elegir la magnitud correcta en figuras compuestas y contextos reales",
            "La pregunta decide si calculas borde, superficie o ambos.",
        )
        self.read_question()
        self.stadium_problem()
        self.garden_problem()
        self.choose_measure()
        self.final_challenge()
        self.summary()

    def read_question(self) -> None:
        self.section_header(1, "ANTES DE CALCULAR", "Subraya palabras que indican longitud o superficie.")
        for title, body, formula in [
            ("BORDE · CONTORNO · CERCA", "Estas palabras piden perímetro o longitud de arco.", r"\text{unidad lineal: cm, m}"),
            ("SUPERFICIE · PISO · PINTURA", "Estas palabras piden área.", r"\text{unidad cuadrada: cm}^2\text{, m}^2"),
            ("FIGURA COMPUESTA", "Divide en partes, decide qué lados cuentan y qué regiones se suman o restan.", None),
        ]:
            self.animate_step(self.centered_step(title, body, formula), READ)
        self.clear_stage()

    def stadium_problem(self) -> None:
        self.section_header(2, "PROBLEMA MODELO · PISTA TIPO ESTADIO", "Dos semicírculos forman un círculo completo; los diámetros interiores no cuentan en el perímetro.")
        stadium = RoundedRectangle(width=6.4, height=2.5, corner_radius=1.25,
                                   stroke_color=BLACK_LINE, stroke_width=6,
                                   fill_color=LIGHT_GRAY, fill_opacity=0.45)
        straight = Line(stadium.get_left() + RIGHT * 1.25 + UP * 0.5,
                        stadium.get_right() + LEFT * 1.25 + UP * 0.5,
                        color=MID_GRAY, stroke_width=2)
        labels = VGroup(
            self.text("tramo recto = 16 m", 31, BOLD).next_to(stadium, DOWN, buff=0.16),
            self.text("radio de cada extremo = 4 m", 29).next_to(stadium, UP, buff=0.16),
        )
        diagram = VGroup(stadium, straight, labels)
        card = self.notebook_card(
            "ÁREA Y PERÍMETRO",
            ["Área: rectángulo + círculo.", "Perímetro: 2 tramos + circunferencia.", "No cuentes diámetros internos."],
            r"A=128+16\pi\approx178.27\,\mathrm{m}^2\\P=32+8\pi\approx57.13\,\mathrm{m}",
        )
        self.two_column(diagram, card)
        self.play(Create(stadium), FadeIn(labels), run_time=RUN_SLOW)
        self.play(Create(straight), run_time=RUN_QUICK)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 3)
        self.clear_stage()

    def garden_problem(self) -> None:
        self.section_header(3, "PROBLEMA MODELO · JARDÍN CON ESTANQUE", "La superficie de césped es una resta; la cerca exterior es un perímetro distinto.")
        rect = Rectangle(width=5.6, height=3.35, stroke_color=BLACK_LINE, stroke_width=5,
                         fill_color=LIGHT_GRAY, fill_opacity=0.55)
        pond = Circle(radius=0.90, stroke_color=BLACK_LINE, stroke_width=5, fill_color=WHITE, fill_opacity=1)
        labels = VGroup(
            self.text("20 m × 12 m", 31, BOLD).next_to(rect, DOWN, buff=0.14),
            self.math("r_{\text{estanque}}=3\,\mathrm{m}", 34).next_to(pond, UP, buff=0.12),
        )
        diagram = VGroup(rect, pond, labels)
        card = self.notebook_card(
            "DOS PREGUNTAS, DOS MAGNITUDES",
            ["Césped: rectángulo − estanque.", "Cerca exterior: perímetro del rectángulo.", "El borde del estanque solo cuenta si lo preguntan."],
            r"A_{\text{césped}}=240-9\pi\approx211.73\,\mathrm{m}^2\\P_{\text{exterior}}=64\,\mathrm{m}",
        )
        self.two_column(diagram, card)
        self.play(Create(rect), Create(pond), FadeIn(labels), run_time=RUN_SLOW)
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.wait(COPY + 3)
        self.clear_stage()

    def choose_measure(self) -> None:
        self.section_header(4, "¿QUÉ DEBO CALCULAR?", "La misma figura puede producir respuestas distintas según la pregunta.")
        cases = [
            ("PINTAR", "Calcula superficie → área."),
            ("CERCAR", "Calcula borde exterior → perímetro."),
            ("PONER CINTA EN UN ARCO", "Calcula solo la longitud de ese arco."),
            ("CUBRIR UNA REGIÓN SOMBREADA", "Descompón y calcula área."),
        ]
        for idx, (verb, rule) in enumerate(cases, 1):
            self.animate_step(self.centered_step(f"{idx} · {verb}", rule), READ)
        self.clear_stage()

    def final_challenge(self) -> None:
        self.section_header(5, "RETO FINAL", "Resuelve con un diagrama propio y justifica por qué cada longitud o área entra en la expresión.")
        problems = [
            ("Una pista tiene tramo recto 24 m y extremos semicirculares de radio 5 m.", "Calcula área y perímetro."),
            ("Un patio 18 m × 14 m contiene una fuente circular de radio 4 m.", "Calcula superficie libre y perímetro exterior."),
            ("La misma figura se amplía con k = 2.5.", "Explica cómo cambian su perímetro y su área."),
        ]
        for i, (data, task) in enumerate(problems, 1):
            card = self.problem_card(i, task, data)
            self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
            self.wait(THINK + 1)
            self.play(FadeOut(card), run_time=RUN_NORMAL)
        self.clear_stage()

    def summary(self) -> None:
        self.section_header(6, "CIERRE DEL BLOQUE", "Conecta el círculo con áreas sombreadas, escala y problemas compuestos.")
        steps = [
            "1. Lee la pregunta y decide: longitud o área.",
            "2. Dibuja y marca solo las medidas útiles.",
            "3. Divide la figura en piezas conocidas.",
            "4. Escribe una expresión completa antes de calcular.",
            "5. Verifica unidades y sentido de la respuesta.",
        ]
        body = VGroup(*[self.text(s, 36) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        card = self.panel(VGroup(self.text("MÉTODO INTEGRADO", 48, BOLD), body).arrange(DOWN, buff=0.36),
                          width=12.2, height=4.8, fill_color=PAPER_GRAY).move_to(DOWN * 0.22)
        self.assert_content_safe(card, "integrated final method")
        self.play(Create(card[0]), FadeIn(card[1]), run_time=RUN_SLOW)
        self.wait(SUMMARY + 2)
        self.fade_all()
