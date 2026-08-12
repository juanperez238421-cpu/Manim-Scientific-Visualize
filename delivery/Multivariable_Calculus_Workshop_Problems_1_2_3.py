#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Taller 1 de Cálculo de Varias Variables — problemas 1, 2 y 3.

ManimCE 0.20.x.  Uses jp_classroom_style.py as the visual architecture.
Source: ITM, Taller 1, p. 1.
"""

from __future__ import annotations

import math
import numpy as np
from manim import *
from jp_classroom_style import *


# -----------------------------------------------------------------------------
# Small reusable visual helpers
# -----------------------------------------------------------------------------
class FirstThreeProblems(JPMathClassroomScene):
    """Professional step-by-step solution of the first three workshop problems."""

    def validate_lesson_data(self) -> None:
        # Problem 1
        assert (-3) ** 2 - 9 == 0
        assert 3 ** 2 - 9 == 0
        # Problem 2
        assert_close(1 + 1, 2.0, label="2a i")
        assert_close((5 * 1 - 1) / (1 + 1), 2.0, label="2a j")
        assert_close((2 * math.exp(0) - 2) / 1, 0.0, label="2a k")
        assert_close(2 + 3, 5.0, label="2b i")
        assert_close((4 + 4 - 3) / (2 - 21), -5 / 19, label="2b j")
        assert_close(1 + math.cos(0), 2.0, label="2c i")
        assert_close(math.e ** 1, math.e, label="2c k")
        # Problem 3 tangent data
        # 3a
        assert_close(math.sin(0), 0.0)
        assert_close(0**2 - math.cos(0), -1.0)
        assert_close(-math.exp(0), -1.0)
        # 3b
        assert_close(math.tan(math.pi), 0.0, tol=1e-12)
        # 3c
        assert_close(6 * 1 / (1 + 1), 3.0)
        assert_close((2 * 1**2 + 1) ** 2, 9.0)
        assert_close(6 / (1 + 1) ** 2, 1.5)
        assert_close(8 * 1 * (2 * 1**2 + 1), 24.0)
        # 3d
        assert_close(math.exp(0) * math.cos(0), 1.0)
        assert_close(math.exp(0) * math.sin(0), 0.0)

    def construct(self) -> None:
        self.opening()
        self.problem_1_domains()
        self.problem_2_limits()
        self.problem_3_tangent_lines()
        self.final_summary()

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------
    def small_tag(self, text_value: str, width: float = 2.1) -> VGroup:
        box = RoundedRectangle(
            width=width, height=0.55, corner_radius=0.09,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        )
        txt = self.text(text_value, 20, BOLD)
        self.fit(txt, width - 0.25, 0.38)
        txt.move_to(box)
        return VGroup(box, txt)

    def result_box(self, expr: str, width: float = 6.2, size: int = 38) -> VGroup:
        panel = RoundedRectangle(
            width=width, height=1.05, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=2.3,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        eq = self.math(expr, size)
        self.fit(eq, width - 0.45, 0.75)
        eq.move_to(panel)
        return VGroup(panel, eq)

    def equation_card(self, label: str, expr: str, width: float = 6.6, size: int = 31) -> VGroup:
        tag = self.small_tag(label, width=1.15)
        eq = self.math(expr, size)
        body = VGroup(tag, eq).arrange(RIGHT, buff=0.22)
        self.fit(body, width - 0.40, 0.78)
        box = RoundedRectangle(
            width=width, height=0.96, corner_radius=0.10,
            stroke_color=LIGHT_GRAY, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        )
        body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.20)
        return VGroup(box, body)

    def domain_number_line(self, kind: str) -> VGroup:
        """Stylized number-line diagrams for Problem 1."""
        axis = NumberLine(
            x_range=[-7, 7, 1], length=8.6, include_numbers=False,
            include_tip=False, stroke_width=2.2, color=BLACK_LINE,
        )
        ticks = VGroup()
        labels = VGroup()
        for val in [-6, -3, 0, 2, 3, 6]:
            x = axis.n2p(val)
            ticks.add(Line(x + DOWN * 0.10, x + UP * 0.10, color=BLACK_LINE, stroke_width=1.5))
            if val in {-6, -3, 0, 2, 3}:
                labels.add(self.math(str(val), 21).next_to(x, DOWN, buff=0.10))
        group = VGroup(axis, ticks, labels)

        def seg(a, b, y=0.0):
            return Line(axis.n2p(a) + UP * y, axis.n2p(b) + UP * y, color=BLACK_LINE, stroke_width=7)

        marks = VGroup()
        if kind == "outside3":
            marks.add(seg(-7, -3), seg(3, 7))
            marks.add(Dot(axis.n2p(-3), radius=0.08, color=BLACK_LINE), Dot(axis.n2p(3), radius=0.08, color=BLACK_LINE))
        elif kind == "all":
            marks.add(seg(-7, 7))
        elif kind == "sqrt_and_holes":
            marks.add(seg(-6, -3), seg(-3, 3), seg(3, 7))
            marks.add(Dot(axis.n2p(-6), radius=0.08, color=BLACK_LINE))
            for val in (-3, 3):
                marks.add(Circle(radius=0.10, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE, fill_opacity=1).move_to(axis.n2p(val)))
        elif kind == "greater2":
            marks.add(seg(2, 7))
            marks.add(Circle(radius=0.10, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE, fill_opacity=1).move_to(axis.n2p(2)))
        return VGroup(group, marks)

    def show_domain_case(
        self,
        label: str,
        function_expr: str,
        conditions: list[str],
        result_expr: str,
        numberline_kind: str,
        insight_lines: list[str],
    ) -> None:
        top = self.formula_panel(function_expr, width=11.2, height=1.05, font_size=34)
        top.move_to(UP * 1.70)

        left = self.note_panel(
            "RESTRICCIONES",
            conditions,
            width=6.2,
            title_size=24,
            body_size=22,
            max_text_height=2.05,
        )
        left.move_to(LEFT * 3.75 + DOWN * 0.05)

        right = self.note_panel(
            "JUSTIFICACIÓN",
            insight_lines,
            width=6.2,
            title_size=24,
            body_size=21,
            max_text_height=2.05,
        )
        right.move_to(RIGHT * 3.75 + DOWN * 0.05)

        line = self.domain_number_line(numberline_kind)
        line.scale(0.88).move_to(DOWN * 2.05)
        result = self.result_box(result_expr, width=7.6, size=34)
        result.move_to(DOWN * 3.20)

        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.play(FadeIn(left, shift=RIGHT * 0.10), FadeIn(right, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(line), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(result, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def limit_component_stack(self, rows: list[tuple[str, str]], result: str) -> None:
        cards = VGroup(*[self.equation_card(lbl, expr, width=11.4, size=30) for lbl, expr in rows])
        cards.arrange(DOWN, buff=0.16).move_to(DOWN * 0.25)
        self.fit(cards, 12.0, 3.70)
        result_box = self.result_box(result, width=8.6, size=36)
        result_box.move_to(DOWN * 3.15)
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.play(FadeIn(result_box, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def tangent_visual(self) -> VGroup:
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2.2, 2.2, 1],
            x_length=5.6, y_length=3.7,
            axis_config={"color": MID_GRAY, "stroke_width": 1.7, "include_tip": False},
        )
        curve = axes.plot(lambda x: 0.16 * x**3 - 0.48 * x, x_range=[-2.7, 2.7], color=BLACK_LINE, stroke_width=3)
        x0 = 0.8
        y0 = 0.16 * x0**3 - 0.48 * x0
        slope = 0.48 * x0**2 - 0.48
        tangent = axes.plot(lambda x: y0 + slope * (x - x0), x_range=[-1.2, 2.8], color=DARK_GRAY, stroke_width=3)
        p = Dot(axes.c2p(x0, y0), radius=0.08, color=BLACK_LINE)
        lab = self.text("punto de tangencia", 19, MEDIUM).next_to(p, UP + RIGHT, buff=0.12)
        return VGroup(axes, curve, tangent, p, lab)

    def show_tangent_case(
        self,
        label: str,
        r_expr: str,
        t0_expr: str,
        point_expr: str,
        deriv_expr: str,
        velocity_expr: str,
        line_expr: str,
    ) -> None:
        top = self.formula_panel(r_expr, width=12.4, height=1.0, font_size=31)
        top.move_to(UP * 1.85)
        t0 = self.small_tag(f"en t = {t0_expr}", width=2.4).next_to(top, DOWN, buff=0.18).align_to(top, LEFT)

        cards = VGroup(
            self.equation_card("P", point_expr, width=12.0, size=29),
            self.equation_card("D", deriv_expr, width=12.0, size=27),
            self.equation_card("V", velocity_expr, width=12.0, size=29),
        ).arrange(DOWN, buff=0.14)
        cards.move_to(DOWN * 0.95)

        result = self.result_box(line_expr, width=12.0, size=31)
        result.move_to(DOWN * 3.35)

        self.play(FadeIn(top), FadeIn(t0), run_time=RUN_NORMAL)
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.play(FadeIn(result, shift=UP * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "CÁLCULO DE VARIAS VARIABLES · TALLER 1",
            "Problemas 1–3 · Solución paso a paso",
            "Dominios de funciones vectoriales · límites vectoriales · rectas tangentes",
            "Primero identificamos la regla; luego resolvemos cada componente y verificamos el resultado.",
        )

    # ------------------------------------------------------------------
    # Problem 1
    # ------------------------------------------------------------------
    def problem_1_domains(self) -> None:
        self.set_header(
            1,
            "DOMINIO DE UNA FUNCIÓN VECTORIAL",
            "El dominio total es la intersección de los dominios de sus tres componentes.",
        )
        method = self.process_map([
            ("1", "SEPARAR COMPONENTES"),
            ("2", "BUSCAR RESTRICCIONES"),
            ("3", "INTERSECTAR"),
            ("4", "ESCRIBIR INTERVALOS"),
        ], columns=2)
        method.move_to(DOWN * 0.20)
        formula = self.formula_panel(
            r"\operatorname{Dom}(\mathbf r)=D_x\cap D_y\cap D_z",
            width=7.2, height=1.08, font_size=40,
        ).move_to(UP * 2.0)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in method], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

        self.set_header(1, "1(a) · RADICAL", "Una raíz cuadrada exige que el radicando sea no negativo.")
        self.show_domain_case(
            "1(a)",
            r"\mathbf r(t)=\sqrt{t^2-9}\,\mathbf i+t^2\,\mathbf j+\mathbf k",
            ["Raíz cuadrada:  t² − 9 ≥ 0", "Polinomio y constante: sin restricción", "Resolver:  (t − 3)(t + 3) ≥ 0"],
            r"\boxed{\operatorname{Dom}(\mathbf r)=(-\infty,-3]\cup[3,\infty)}",
            "outside3",
            ["El radical es real únicamente fuera de las raíces −3 y 3.", "Los extremos se incluyen porque √0 está definida."],
        )

        self.set_header(1, "1(b) · SIN RESTRICCIONES", "Seno, coseno y la exponencial están definidos para todo t real.")
        self.show_domain_case(
            "1(b)",
            r"\mathbf r(t)=\cos(2t)\,\mathbf i+e^{-t}\,\mathbf j+\sin(2t)\,\mathbf k",
            ["cos(2t): definida para todo t real", "e^(−t): definida para todo t real", "sin(2t): definida para todo t real"],
            r"\boxed{\operatorname{Dom}(\mathbf r)=\mathbb R}",
            "all",
            ["No aparece denominador, logaritmo ni raíz par.", "La intersección de tres dominios ℝ sigue siendo ℝ."],
        )

        self.set_header(1, "1(c) · RADICAL + DENOMINADOR", "Combinar ambas restricciones antes de escribir el conjunto final.")
        self.show_domain_case(
            "1(c)",
            r"\mathbf r(t)=\sqrt{t+6}\,\mathbf i+3t\,\mathbf j+\frac{1}{t^2-9}\,\mathbf k",
            ["Raíz cuadrada:  t + 6 ≥ 0  →  t ≥ −6", "Denominador:  t² − 9 ≠ 0  →  t ≠ ±3", "El término lineal 3t no impone restricción"],
            r"\boxed{[-6,-3)\cup(-3,3)\cup(3,\infty)}",
            "sqrt_and_holes",
            ["El dominio comienza en −6 por la raíz.", "Se excluyen −3 y 3 porque no se permite dividir por cero."],
        )

        self.set_header(1, "1(d) · LOGARITMO + EXPONENCIAL", "El logaritmo determina la restricción decisiva en este caso.")
        self.show_domain_case(
            "1(d)",
            r"\mathbf r(t)=\ln(t-2)\,\mathbf i+e^{1/t}\,\mathbf j-\cos(2t)\,\mathbf k",
            ["Logaritmo:  t − 2 > 0  →  t > 2", "Exponente e^(1/t): exige t ≠ 0", "cos(2t): no impone restricción"],
            r"\boxed{\operatorname{Dom}(\mathbf r)=(2,\infty)}",
            "greater2",
            ["Intersectar t > 2 con t ≠ 0.", "Como todo t > 2 ya es distinto de cero, el dominio final es simplemente (2,∞)."],
        )

    # ------------------------------------------------------------------
    # Problem 2
    # ------------------------------------------------------------------
    def problem_2_limits(self) -> None:
        self.set_header(
            2,
            "LÍMITES DE FUNCIONES VECTORIALES",
            "Un límite vectorial existe cuando el límite de cada componente existe y es finito.",
        )
        formula = self.formula_panel(
            r"\lim_{t\to a}\mathbf r(t)=\left\langle\lim x(t),\lim y(t),\lim z(t)\right\rangle",
            width=11.5, height=1.15, font_size=37,
        ).move_to(UP * 1.75)
        logic = self.process_map([
            ("1", "SEPARAR i, j, k"),
            ("2", "SIMPLIFICAR SI ES NECESARIO"),
            ("3", "EVALUAR CADA LÍMITE"),
            ("4", "ARMAR EL VECTOR RESULTANTE"),
        ], columns=2).move_to(DOWN * 0.35)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in logic], lag_ratio=0.11), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

        self.set_header(2, "2(a) · COMPONENTE A COMPONENTE", "Solo la primera componente requiere cancelación algebraica; en las otras dos se sustituye directamente.")
        top = self.formula_panel(
            r"\lim_{t\to1}\left(\frac{t^2-1}{t-1}\mathbf i+\frac{5t-1}{t+1}\mathbf j+\frac{2e^{t-1}-2}{t}\mathbf k\right)",
            width=13.4, height=1.02, font_size=30,
        ).move_to(UP * 2.0)
        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.limit_component_stack([
            ("i", r"\frac{t^2-1}{t-1}=\frac{(t-1)(t+1)}{t-1}=t+1\ \longrightarrow\ 2"),
            ("j", r"\frac{5t-1}{t+1}\ \longrightarrow\ \frac{4}{2}=2"),
            ("k", r"\frac{2e^{t-1}-2}{t}\ \longrightarrow\ \frac{2e^0-2}{1}=0"),
        ], r"\boxed{\lim_{t\to1}\mathbf r(t)=\langle2,2,0\rangle}")

        self.set_header(2, "2(b) · FACTORIZAR PRIMERO", "La primera componente produce 0/0; por eso se factoriza el numerador antes de sustituir.")
        top = self.formula_panel(
            r"\lim_{t\to2}\left(\frac{t^2+t-6}{t-2}\mathbf i+\frac{t^2+2t-3}{t-21}\mathbf j+(\sqrt t-3)\mathbf k\right)",
            width=13.4, height=1.02, font_size=29,
        ).move_to(UP * 2.0)
        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.limit_component_stack([
            ("i", r"\frac{t^2+t-6}{t-2}=\frac{(t-2)(t+3)}{t-2}=t+3\ \longrightarrow\ 5"),
            ("j", r"\frac{t^2+2t-3}{t-21}\ \longrightarrow\ \frac{4+4-3}{2-21}=-\frac{5}{19}"),
            ("k", r"\sqrt t-3\ \longrightarrow\ \sqrt2-3"),
        ], r"\boxed{\lim_{t\to2}\mathbf r(t)=\left\langle5,-\frac5{19},\sqrt2-3\right\rangle}")

        self.set_header(2, "2(c) · SIMPLIFICACIÓN TRIGONOMÉTRICA", "Reescribir la primera componente y usar el límite notable sin(t)/t → 1.")
        top = self.formula_panel(
            r"\lim_{t\to0}\left(\frac{1-\cos^2t}{1-\cos t}\mathbf i+\frac{t^2}{\sin t}\mathbf j+e^{-t+1}\mathbf k\right)",
            width=13.4, height=1.02, font_size=29,
        ).move_to(UP * 2.0)
        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.limit_component_stack([
            ("i", r"\frac{1-\cos^2t}{1-\cos t}=\frac{(1-\cos t)(1+\cos t)}{1-\cos t}=1+\cos t\to2"),
            ("j", r"\frac{t^2}{\sin t}=t\left(\frac{t}{\sin t}\right)\ \longrightarrow\ 0\cdot1=0"),
            ("k", r"e^{-t+1}\ \longrightarrow\ e^1=e"),
        ], r"\boxed{\lim_{t\to0}\mathbf r(t)=\langle2,0,e\rangle}")

    # ------------------------------------------------------------------
    # Problem 3
    # ------------------------------------------------------------------
    def problem_3_tangent_lines(self) -> None:
        self.set_header(
            3,
            "RECTA TANGENTE A UNA CURVA VECTORIAL",
            "El punto se obtiene con r(t₀); la dirección tangente se obtiene con r′(t₀).",
        )
        diagram = self.tangent_visual()
        panel = self.figure_panel(
            diagram, width=6.4, height=4.7,
            title="IDEA GEOMÉTRICA",
            caption="La recta tangente comparte la dirección instantánea de la curva en el punto elegido.",
        )
        formula_side = VGroup(
            self.formula_panel(r"\mathbf L(s)=\mathbf r(t_0)+s\,\mathbf r'(t_0)", width=6.6, height=1.08, font_size=38),
            self.note_panel(
                "TRES PASOS",
                ["1. Evaluar r(t₀) → punto P", "2. Derivar r(t) componente a componente", "3. Evaluar r′(t₀) → vector dirección"],
                width=6.6, title_size=24, body_size=22,
            ),
        ).arrange(DOWN, buff=0.28)
        layout = self.split_layout(panel.group, formula_side, center_y=-0.55)
        self.play(FadeIn(panel.group), run_time=RUN_NORMAL)
        self.play(FadeIn(formula_side), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

        self.set_header(3, "3(a) · t₀ = 0", "Evaluar primero el punto y luego derivar cada componente.")
        self.show_tangent_case(
            "3(a)",
            r"\mathbf r(t)=\langle\sin t,\ t^2-\cos t,\ -e^t\rangle",
            "0",
            r"\mathbf r(0)=\langle0,-1,-1\rangle",
            r"\mathbf r'(t)=\langle\cos t,\ 2t+\sin t,\ -e^t\rangle",
            r"\mathbf r'(0)=\langle1,0,-1\rangle",
            r"\boxed{\mathbf L(s)=\langle0,-1,-1\rangle+s\langle1,0,-1\rangle}",
        )

        self.set_header(3, "3(b) · t₀ = π", "La derivada de −tan(t) es −sec²(t); por tanto, la componente k de la dirección tangente vale −1 en π.")
        self.show_tangent_case(
            "3(b)",
            r"\mathbf r(t)=\langle te^t,\ t^2-2t,\ -\tan t\rangle",
            "π",
            r"\mathbf r(\pi)=\langle\pi e^\pi,\ \pi^2-2\pi,\ 0\rangle",
            r"\mathbf r'(t)=\langle(1+t)e^t,\ 2t-2,\ -\sec^2t\rangle",
            r"\mathbf r'(\pi)=\langle(1+\pi)e^\pi,\ 2\pi-2,\ -1\rangle",
            r"\boxed{\mathbf L(s)=\langle\pi e^\pi,\pi^2-2\pi,0\rangle+s\langle(1+\pi)e^\pi,2\pi-2,-1\rangle}",
        )

        self.set_header(3, "3(c) · t₀ = 1", "Leer con cuidado el orden impreso: la componente i es t³−t y la componente j es 6t/(t+1).")
        self.show_tangent_case(
            "3(c)",
            r"\mathbf r(t)=\left\langle t^3-t,\ \frac{6t}{t+1},\ (2t^2+1)^2\right\rangle",
            "1",
            r"\mathbf r(1)=\langle0,3,9\rangle",
            r"\mathbf r'(t)=\left\langle3t^2-1,\ \frac{6}{(t+1)^2},\ 8t(2t^2+1)\right\rangle",
            r"\mathbf r'(1)=\left\langle2,\frac32,24\right\rangle",
            r"\boxed{\mathbf L(s)=\langle0,3,9\rangle+s\left\langle2,\frac32,24\right\rangle}",
        )

        self.set_header(3, "3(d) · t₀ = 0", "Aplicar la regla del producto en las dos primeras componentes porque ambas contienen e^(−t).")
        self.show_tangent_case(
            "3(d)",
            r"\mathbf r(t)=\langle e^{-t}\cos t,\ e^{-t}\sin t,\ e^{-t}\rangle",
            "0",
            r"\mathbf r(0)=\langle1,0,1\rangle",
            r"\mathbf r'(t)=\langle-e^{-t}(\cos t+\sin t),\ e^{-t}(\cos t-\sin t),\ -e^{-t}\rangle",
            r"\mathbf r'(0)=\langle-1,1,-1\rangle",
            r"\boxed{\mathbf L(s)=\langle1,0,1\rangle+s\langle-1,1,-1\rangle}",
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    def final_summary(self) -> None:
        self.set_header(
            4,
            "MAPA DE MÉTODO PARA EL PARCIAL",
            "Tres algoritmos reutilizables cubren todos los ejercicios resueltos en este video.",
        )
        cards = self.process_map([
            ("1", "DOMINIO: restricciones → intersección"),
            ("2", "LÍMITE: resolver i, j, k por separado"),
            ("3", "TANGENTE: punto r(t₀)"),
            ("4", "TANGENTE: dirección r′(t₀)"),
            ("5", "VERIFICAR valores prohibidos / cancelaciones"),
            ("6", "ESCRIBIR EL VECTOR FINAL CON CLARIDAD"),
        ], columns=2)
        cards.move_to(DOWN * 0.30)
        self.fit(cards, 13.8, 4.8)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.10), run_time=RUN_SLOW * 1.5)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Restringir. Simplificar. Evaluar. Derivar. Verificar.")


# Quick QA:
#   manim -pql first3_full.py FirstThreeProblems --disable_caching
# Final requested render:
#   manim -pqh first3_full.py FirstThreeProblems --disable_caching
