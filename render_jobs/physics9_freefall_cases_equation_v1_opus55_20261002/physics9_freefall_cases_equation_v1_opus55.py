#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Casos de caída libre y ecuación maestra.

Consolidación de las versiones actuales de caída libre + lógica ASTRA/Opus visual:
- formato JP Classroom 1920×1080, fondo blanco y jerarquía monocroma;
- fenómeno primero, ecuación después;
- una decisión causal por estado visual;
- movimiento físico continuo gobernado por ValueTracker;
- derivación explícita de v(t) y y(t);
- comparación de los tres signos posibles de v0;
- caso del punto más alto sin el error conceptual a=0;
- ejemplos con validación numérica previa;
- puente Galileo: plano inclinado -> x ∝ t² -> caída libre;
- cierre como método reproducible, no como muro de texto.

Target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from manim import *

from library.jp_classroom_style import *


# =============================================================================
# DATOS FÍSICOS — TODA AFIRMACIÓN NUMÉRICA SE VALIDA ANTES DEL RENDER
# =============================================================================
G = 9.81

# Caso de lanzamiento vertical hacia arriba usado para el punto más alto.
V0_APEX = 14.0
T_APEX = V0_APEX / G
H_APEX = V0_APEX**2 / (2 * G)
T_RETURN = 2 * T_APEX

# Comparación de tres condiciones iniciales desde la misma altura.
Y0_COMPARE = 20.0
V0_RELEASE = 0.0
V0_DOWN = -5.0
V0_UP = 5.0


def impact_time(y0: float, v0: float, g: float = G) -> float:
    """Raíz física positiva de 0 = y0 + v0 t - 1/2 g t²."""
    return (v0 + math.sqrt(v0**2 + 2 * g * y0)) / g


def impact_velocity(y0: float, v0: float, g: float = G) -> float:
    t = impact_time(y0, v0, g)
    return v0 - g * t


T_RELEASE = impact_time(Y0_COMPARE, V0_RELEASE)
V_RELEASE_IMPACT = impact_velocity(Y0_COMPARE, V0_RELEASE)
T_DOWN = impact_time(Y0_COMPARE, V0_DOWN)
V_DOWN_IMPACT = impact_velocity(Y0_COMPARE, V0_DOWN)
T_UP = impact_time(Y0_COMPARE, V0_UP)
V_UP_IMPACT = impact_velocity(Y0_COMPARE, V0_UP)

# Datos normalizados para la evidencia 1:4:9:16.
RAMP_T = np.array([1.0, 2.0, 3.0, 4.0])
RAMP_T2 = RAMP_T**2
RAMP_X = np.array([1.0, 4.0, 9.0, 16.0])


@dataclass
class MotionState:
    t: float
    y: float
    v: float
    a: float


class Physics9FreeFallCasesEquationOpus55(JPMathClassroomScene):
    """Lección consolidada: casos de caída libre + ecuación maestra."""

    # =========================================================================
    # VALIDACIÓN CIENTÍFICA
    # =========================================================================
    def validate_lesson_data(self) -> None:
        # Punto más alto.
        assert_close(V0_APEX - G * T_APEX, 0.0, label="apex velocity")
        assert_close(
            V0_APEX * T_APEX - 0.5 * G * T_APEX**2,
            H_APEX,
            label="apex height kinematics",
        )
        assert_close(T_RETURN, 2 * T_APEX, label="return symmetry")

        # Tres casos desde 20 m: sustitución directa en y(t) y v(t).
        for v0, t_hit, v_hit in (
            (V0_RELEASE, T_RELEASE, V_RELEASE_IMPACT),
            (V0_DOWN, T_DOWN, V_DOWN_IMPACT),
            (V0_UP, T_UP, V_UP_IMPACT),
        ):
            assert_close(
                Y0_COMPARE + v0 * t_hit - 0.5 * G * t_hit**2,
                0.0,
                label=f"ground root v0={v0}",
            )
            assert_close(v0 - G * t_hit, v_hit, label=f"impact velocity v0={v0}")
            assert_close(
                v_hit**2,
                v0**2 + 2 * G * Y0_COMPARE,
                label=f"time-free relation v0={v0}",
            )

        # Simetría energética: ±5 m/s tienen el mismo v0² y la misma rapidez final.
        assert_close(abs(V_DOWN_IMPACT), abs(V_UP_IMPACT), label="equal impact speed ±v0")

        # Secuencia galileana normalizada.
        assert np.allclose(RAMP_X, RAMP_T2)
        assert np.allclose(np.diff(np.r_[0, RAMP_X]), [1, 3, 5, 7])

    # =========================================================================
    # HELPERS VISUALES
    # =========================================================================
    def ball(self, point, radius: float = 0.18, fill=VERY_LIGHT_GRAY) -> VGroup:
        body = Circle(
            radius=radius,
            stroke_color=BLACK_LINE,
            stroke_width=2.1,
            fill_color=fill,
            fill_opacity=1.0,
        ).move_to(point)
        highlight = Dot(
            np.array(point, dtype=float) + UL * radius * 0.34,
            radius=radius * 0.13,
            color=WHITE_FILL,
        )
        return VGroup(body, highlight)

    def ghost_ball(self, point, radius: float = 0.105) -> Circle:
        return Circle(
            radius=radius,
            stroke_color=MID_GRAY,
            stroke_width=1.25,
            fill_color=WHITE_FILL,
            fill_opacity=0.14,
        ).move_to(point)

    def vector_arrow(
        self,
        start,
        direction,
        label: str,
        *,
        label_size: int = 24,
        label_side=RIGHT,
        stroke_width: float = 3.2,
    ) -> VGroup:
        start = np.array(start, dtype=float)
        direction = np.array(direction, dtype=float)
        if np.linalg.norm(direction) < 1e-3:
            marker = self.math(label, label_size).move_to(start + RIGHT * 0.60)
            return VGroup(marker)
        arrow = Arrow(
            start,
            start + direction,
            buff=0,
            color=BLACK_LINE,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
        )
        lab = self.math(label, label_size).next_to(arrow, label_side, buff=0.08)
        return VGroup(arrow, lab)

    def ground(self, y: float, x0: float, x1: float) -> VGroup:
        line = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.2)
        hatch = VGroup(
            *[
                Line(
                    [x, y - 0.04, 0],
                    [x + 0.23, y - 0.19, 0],
                    color=LIGHT_GRAY,
                    stroke_width=1.1,
                )
                for x in np.arange(x0, x1, 0.46)
            ]
        )
        return VGroup(line, hatch)

    def focus_panel(
        self,
        title: str,
        lines: list[str],
        *,
        equation: str | None = None,
        meaning: str | None = None,
        width: float = 5.4,
        height: float = 3.15,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        ttl = self.text(title, 27, BOLD)
        body = VGroup(*[self.text(line, 25) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        pieces = [ttl, body]
        if equation is not None:
            eq = self.math(equation, 39)
            pieces.append(eq)
        if meaning is not None:
            rule = Line(LEFT * (width - 0.70) / 2, RIGHT * (width - 0.70) / 2, color=LIGHT_GRAY)
            meaning_mob = self.text(meaning, 24, BOLD)
            pieces.extend([rule, meaning_mob])
        content = VGroup(*pieces).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        self.fit(content, width - 0.55, height - 0.38)
        content.move_to(box)
        return VGroup(box, content)

    def phase_card(self, number: int, title: str, statement: str, width: float = 5.0) -> VGroup:
        badge = RoundedRectangle(
            width=0.60,
            height=0.46,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        )
        n = self.text(str(number), 19, BOLD).move_to(badge)
        ttl = self.text(title, 23, BOLD)
        body = self.text(statement, 21)
        self.fit(body, width - 1.25, 0.70)
        words = VGroup(ttl, body).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        row = VGroup(VGroup(badge, n), words).arrange(RIGHT, buff=0.16)
        self.fit(row, width - 0.30, 1.02)
        box = RoundedRectangle(
            width=width,
            height=max(1.18, row.height + 0.24),
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.45,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.16)
        return VGroup(box, row)

    def checkpoint(self, card: Mobject, pause: float = PAUSE_EXPLAIN) -> None:
        self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_QUICK)
        self.wait(pause)
        self.play(FadeOut(card), run_time=RUN_QUICK)

    def live_state_panel(
        self,
        tracker: ValueTracker,
        state_fn,
        *,
        title: str,
        width: float,
        position,
    ) -> Mobject:
        def build():
            s = state_fn(tracker.get_value())
            ttl = self.text(title, 22, BOLD)
            rows = VGroup(
                self.text(f"t = {s.t:0.2f} s", 27, BOLD),
                self.text(f"y = {s.y:+0.2f} m", 27),
                self.text(f"v = {s.v:+0.2f} m/s", 27),
                self.text(f"a = {s.a:+0.2f} m/s²", 27),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            content = VGroup(ttl, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            box = RoundedRectangle(
                width=width,
                height=2.72,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=1.7,
                fill_color=PAPER_GRAY,
                fill_opacity=1.0,
            )
            self.fit(content, width - 0.45, 2.30)
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.23)
            return VGroup(box, content).move_to(position)

        return always_redraw(build)

    # =========================================================================
    # MASTER TIMELINE
    # =========================================================================
    def construct(self) -> None:
        self.standard_opening(
            "FÍSICA 9° · CINEMÁTICA",
            "CASOS DE CAÍDA LIBRE Y ECUACIÓN MAESTRA",
            "Una sola dinámica bajo gravedad; distintas condiciones iniciales cambian la historia del movimiento.",
            "Primero vemos qué hace el objeto. Después dejamos que la ecuación describa exactamente ese movimiento.",
        )
        self.scene_01_what_is_free_fall()
        self.scene_02_axis_and_master_model()
        self.scene_03_derive_velocity()
        self.scene_04_derive_position_from_area()
        self.scene_05_three_initial_velocity_cases()
        self.scene_06_upward_throw_apex()
        self.scene_07_same_height_three_worked_cases()
        self.scene_08_galileo_ramp_square_law()
        self.scene_09_method_map()
        self.standard_closing(
            "Misma gravedad, misma ecuación: fija el eje, identifica v₀, conserva los signos y deja que el modelo prediga el movimiento."
        )

    # =========================================================================
    # 01 — DEFINICIÓN FÍSICA
    # =========================================================================
    def scene_01_what_is_free_fall(self) -> None:
        self.set_header(
            1,
            "CAÍDA LIBRE NO SIGNIFICA ‘MOVERSE HACIA ABAJO’",
            "Un cuerpo está en caída libre cuando, después de liberarlo, la gravedad es la única fuerza relevante del modelo.",
        )

        divider = Line([0, -2.65, 0], [0, 2.05, 0], color=LIGHT_GRAY, stroke_width=1.5)

        # Izquierda: movimiento vertical con contacto -> no es caída libre.
        rail = Line([-4.15, -2.15, 0], [-4.15, 1.60, 0], color=LIGHT_GRAY, stroke_width=2.0)
        block = Square(
            side_length=0.72,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        ).move_to([-4.15, -1.55, 0])
        n_vec = self.vector_arrow([-4.64, -1.38, 0], UP * 0.88, r"\vec N", label_side=LEFT)
        w_vec = self.vector_arrow([-3.68, -1.20, 0], DOWN * 0.88, r"m\vec g")
        ltitle = self.text("MOVIMIENTO VERTICAL", 28, BOLD).move_to([-4.15, 2.15, 0])
        lsub = self.text("hay una fuerza de contacto", 25).move_to([-4.15, 1.70, 0])

        # Derecha: después del lanzamiento, solo gravedad -> sí es caída libre aunque suba.
        guide = DashedLine([4.15, -2.15, 0], [4.15, 1.62, 0], dash_length=0.08, color=LIGHT_GRAY)
        ball = self.ball([4.15, -1.55, 0], 0.20)
        gravity = self.vector_arrow([4.67, -1.39, 0], DOWN * 0.92, r"m\vec g")
        rtitle = self.text("CAÍDA LIBRE IDEAL", 28, BOLD).move_to([4.15, 2.15, 0])
        rsub = self.text("puede subir, detenerse y caer", 25).move_to([4.15, 1.70, 0])

        self.assert_content_safe(
            VGroup(divider, rail, block, n_vec, w_vec, ltitle, lsub, guide, ball, gravity, rtitle, rsub),
            "section 1 static",
        )

        self.play(Create(divider), FadeIn(ltitle), FadeIn(rtitle), FadeIn(lsub), FadeIn(rsub), run_time=RUN_NORMAL)
        self.play(Create(rail), FadeIn(block), FadeIn(n_vec), FadeIn(w_vec), run_time=RUN_NORMAL)
        self.play(block.animate.shift(UP * 2.20), run_time=RUN_SLOW, rate_func=there_and_back)
        left_card = self.phase_card(1, "PREGUNTA CORRECTA", "¿Qué fuerzas siguen actuando? La trayectoria vertical no basta.", 5.7).move_to([-3.95, -3.12, 0])
        self.checkpoint(left_card, PAUSE_EXPLAIN)

        self.play(Create(guide), FadeIn(ball), FadeIn(gravity), run_time=RUN_NORMAL)
        self.play(
            ball.animate.shift(UP * 2.75),
            gravity.animate.shift(UP * 2.75),
            run_time=RUN_SLOW * 1.25,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(
            ball.animate.shift(DOWN * 3.25),
            gravity.animate.shift(DOWN * 3.25),
            run_time=RUN_SLOW * 1.45,
            rate_func=rate_functions.ease_in_quad,
        )
        right_card = self.phase_card(2, "CRITERIO", "Tras soltar o lanzar, si solo modelamos gravedad, todo el tramo es caída libre.", 6.1).move_to([3.45, -3.12, 0])
        self.checkpoint(right_card, PAUSE_EXPLAIN)

        definition = self.formula_panel(
            r"\sum \vec F=m\vec g\qquad\Longrightarrow\qquad \vec a=\vec g",
            width=7.4,
            height=1.05,
            font_size=42,
        ).move_to([0, -2.72, 0])
        self.play(FadeIn(definition), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 02 — EJE, SIGNOS, MODELO MAESTRO
    # =========================================================================
    def scene_02_axis_and_master_model(self) -> None:
        self.set_header(
            2,
            "EL SIGNO NACE DEL EJE, NO DE LA MEMORIA",
            "Elegimos +y hacia arriba. Entonces la gravedad apunta siempre en sentido negativo durante toda la caída libre.",
        )

        axis = Arrow([-5.60, -2.25, 0], [-5.60, 2.10, 0], buff=0, color=BLACK_LINE, stroke_width=2.6)
        plus_y = self.math(r"+y", 30).next_to(axis, UP, buff=0.07)
        origin = Dot([-5.60, -0.15, 0], radius=0.07, color=BLACK_LINE)
        zero = self.text("0", 22).next_to(origin, LEFT, buff=0.08)

        ball = self.ball([-3.20, 0.80, 0], 0.24)
        weight = self.vector_arrow([-2.52, 0.86, 0], DOWN * 1.45, r"m\vec g", label_size=27)
        fbd = self.text("DIAGRAMA DE CUERPO LIBRE", 26, BOLD).move_to([-3.00, 2.05, 0])

        chain = VGroup(
            self.math(r"\sum F_y=ma_y", 48),
            self.math(r"-mg=ma_y", 48),
            self.math(r"a_y=-g", 56),
        ).arrange(DOWN, buff=0.48).move_to([2.85, 0.35, 0])

        meaning = self.focus_panel(
            "MODELO MAESTRO",
            ["g = 9.81 m/s² es una magnitud positiva.", "El signo ‘−’ indica dirección respecto a +y."],
            equation=r"a_y=-g=-9.81\;\mathrm{m/s^2}",
            meaning="LA ACELERACIÓN NO CAMBIA DE SIGNO EN EL PUNTO MÁS ALTO",
            width=6.2,
            height=3.15,
        ).move_to([2.95, -1.60, 0])

        self.assert_content_safe(VGroup(axis, plus_y, origin, zero, ball, weight, fbd, chain), "section 2")
        self.play(FadeIn(axis), FadeIn(plus_y), FadeIn(origin), FadeIn(zero), FadeIn(fbd), FadeIn(ball), run_time=RUN_NORMAL)
        self.play(GrowArrow(weight[0]), FadeIn(weight[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(chain[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(TransformFromCopy(chain[0], chain[1]), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(TransformFromCopy(chain[1], chain[2]), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(chain), FadeIn(meaning), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 03 — DERIVACIÓN DE VELOCIDAD
    # =========================================================================
    def scene_03_derive_velocity(self) -> None:
        self.set_header(
            3,
            "DE a = −g A LA ECUACIÓN DE VELOCIDAD",
            "Aceleración constante significa pendiente constante en v(t): cada segundo la velocidad vertical disminuye 9.81 m/s.",
        )

        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[-16, 16, 4],
            x_length=7.0,
            y_length=4.25,
            axis_config={"color": MID_GRAY, "stroke_width": 1.7, "include_tip": False},
        ).move_to([-3.55, -0.45, 0])
        t_end = 2.55
        v0 = 14.0
        line = Line(axes.c2p(0, v0), axes.c2p(t_end, v0 - G * t_end), color=BLACK_LINE, stroke_width=4.0)
        run = Line(axes.c2p(0, v0), axes.c2p(t_end, v0), color=LIGHT_GRAY, stroke_width=2.0)
        rise = Line(axes.c2p(t_end, v0), axes.c2p(t_end, v0 - G * t_end), color=MID_GRAY, stroke_width=2.0)
        dt = self.math(r"\Delta t", 31).next_to(run, UP, buff=0.10)
        dv = self.math(r"\Delta v", 31).next_to(rise, RIGHT, buff=0.10)
        labels = VGroup(
            self.text("t", 25, BOLD).next_to(axes.x_axis, RIGHT, buff=0.10),
            self.text("vᵧ", 25, BOLD).next_to(axes.y_axis, UP, buff=0.10),
        )

        graph = VGroup(axes, line, run, rise, dt, dv, labels)
        self.assert_content_safe(graph, "section 3 graph")

        self.play(FadeIn(VGroup(axes, labels)), run_time=RUN_NORMAL)
        self.play(Create(line), run_time=RUN_SLOW)
        self.play(Create(run), Create(rise), FadeIn(dt), FadeIn(dv), run_time=RUN_NORMAL)
        slope_note = self.phase_card(1, "LEE LA PENDIENTE", "pendiente de v(t) = Δv/Δt = aᵧ = −g", 5.1).move_to([4.55, 1.75, 0])
        self.checkpoint(slope_note, PAUSE_EXPLAIN)

        chain = [
            r"a_y=\frac{v_y-v_0}{t}",
            r"-g=\frac{v_y-v_0}{t}",
            r"-gt=v_y-v_0",
            r"\boxed{v_y=v_0-gt}",
        ]
        current = self.math(chain[0], 49).move_to([3.70, -0.10, 0])
        self.play(Write(current), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        for expression in chain[1:]:
            target = self.math(expression, 49 if "boxed" not in expression else 53).move_to([3.70, -0.10, 0])
            self.play(TransformMatchingTex(current, target, transform_mismatches=True), run_time=RUN_SLOW)
            current = target
            self.wait(PAUSE_EXPLAIN)

        interpretation = self.focus_panel(
            "INTERPRETACIÓN",
            ["v₀ contiene la condición inicial.", "−gt es el cambio acumulado por gravedad."],
            meaning="LA MISMA ECUACIÓN SERVIRÁ PARA LOS TRES CASOS",
            width=5.6,
            height=2.45,
        ).move_to([3.70, -2.02, 0])
        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 04 — POSICIÓN DESDE EL ÁREA BAJO v(t)
    # =========================================================================
    def scene_04_derive_position_from_area(self) -> None:
        self.set_header(
            4,
            "EL ÁREA BAJO v(t) CONSTRUYE LA POSICIÓN",
            "No memorizamos el término 1/2 gt²: aparece geométricamente al sumar el rectángulo inicial y el triángulo de cambio de velocidad.",
        )

        axes = Axes(
            x_range=[0, 1.0, 0.2],
            y_range=[0, 12, 2],
            x_length=7.0,
            y_length=4.15,
            axis_config={"color": MID_GRAY, "stroke_width": 1.7, "include_tip": False},
        )
        t1 = 0.8
        v0 = 10.0
        v1 = v0 - G * t1
        line = Line(axes.c2p(0, v0), axes.c2p(t1, v1), color=BLACK_LINE, stroke_width=4.0)
        rect = Polygon(
            axes.c2p(0, 0),
            axes.c2p(t1, 0),
            axes.c2p(t1, v0),
            axes.c2p(0, v0),
            stroke_color=LIGHT_GRAY,
            stroke_width=1.4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=0.78,
        )
        tri = Polygon(
            axes.c2p(0, v0),
            axes.c2p(t1, v0),
            axes.c2p(t1, v1),
            stroke_color=BLACK_LINE,
            stroke_width=1.4,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.62,
        )
        graph_labels = VGroup(
            self.text("tiempo", 25, BOLD).next_to(axes.x_axis, DOWN, buff=0.26),
            self.text("velocidad vertical", 25, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.30),
        )
        graph = VGroup(axes, rect, tri, line, graph_labels).move_to([-3.65, -0.55, 0])

        eq1 = self.math(r"A_{rect}=v_0t", 44)
        eq2 = self.math(r"A_{tri}=\frac12(-gt)t=-\frac12gt^2", 40)
        eq3 = self.math(r"\Delta y=v_0t-\frac12gt^2", 45)
        eq4 = self.math(r"\boxed{y=y_0+v_0t-\frac12gt^2}", 47)
        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.46).move_to([3.65, -0.48, 0])

        self.assert_content_safe(VGroup(graph, eqs), "section 4")
        self.play(FadeIn(VGroup(axes, graph_labels, line)), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(rect), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(rect, eq1), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(tri), run_time=RUN_NORMAL)
        self.play(TransformFromCopy(tri, eq2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(eq3), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(eq4), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 05 — TRES SIGNOS DE v0, MISMO RELOJ
    # =========================================================================
    def scene_05_three_initial_velocity_cases(self) -> None:
        self.set_header(
            5,
            "TRES CASOS, UNA SOLA ECUACIÓN",
            "El valor inicial v₀ decide cómo empieza el movimiento; la aceleración sigue siendo −g en los tres paneles.",
        )

        t = ValueTracker(0.0)
        t_show = 0.90
        scale_y = 0.18
        centers = [-4.85, 0.0, 4.85]
        v0s = [0.0, -5.0, 12.0]
        titles = ["SE SUELTA", "SE LANZA HACIA ABAJO", "SE LANZA HACIA ARRIBA"]
        subtitles = [r"v_0=0", r"v_0<0", r"v_0>0"]

        panels = VGroup()
        movers = VGroup()
        vectors = VGroup()
        accel_vectors = VGroup()

        for x, v0, title, subtitle in zip(centers, v0s, titles, subtitles):
            box = RoundedRectangle(
                width=4.35,
                height=3.65,
                corner_radius=0.12,
                stroke_color=LIGHT_GRAY,
                stroke_width=1.5,
                fill_color=WHITE_FILL,
                fill_opacity=1.0,
            ).move_to([x, -0.25, 0])
            ttl = self.text(title, 25, BOLD).move_to([x, 1.78, 0])
            sub = self.math(subtitle, 35).move_to([x, 1.34, 0])
            guide = DashedLine([x, -1.84, 0], [x, 1.05, 0], dash_length=0.08, color=LIGHT_GRAY)
            panels.add(VGroup(box, ttl, sub, guide))

            def yscene(v0_local: float):
                return scale_y * (v0_local * t.get_value() - 0.5 * G * t.get_value() ** 2)

            moving = always_redraw(
                lambda x0=x, v0_local=v0: self.ball([x0, yscene(v0_local), 0], 0.16)
            )
            movers.add(moving)

            def vel_group(x0=x, v0_local=v0):
                vv = v0_local - G * t.get_value()
                y = scale_y * (v0_local * t.get_value() - 0.5 * G * t.get_value() ** 2)
                length = np.clip(vv / 12.0, -1.08, 1.08)
                return self.vector_arrow([x0 + 0.52, y, 0], UP * length, r"v_y", label_size=21)

            vectors.add(always_redraw(vel_group))
            accel_vectors.add(self.vector_arrow([x - 0.67, 0.25, 0], DOWN * 0.72, r"a_y=-g", label_size=20, label_side=LEFT))

        hud_box = RoundedRectangle(
            width=9.0, height=0.96, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=1.7,
            fill_color=PAPER_GRAY, fill_opacity=1.0,
        ).move_to([0, -3.18, 0])
        hud_label = self.text("MISMO INSTANTE", 24, BOLD).move_to([-3.18, -3.18, 0])
        hud_time = always_redraw(
            lambda: self.text(f"t = {t.get_value():0.2f} s", 28, BOLD).move_to([-1.20, -3.18, 0])
        )
        hud_eq = self.math(r"y=y_0+v_0t-\frac12gt^2", 36).move_to([2.15, -3.18, 0])
        time_hud = VGroup(hud_box, hud_label, hud_time, hud_eq)

        self.assert_content_safe(panels, "section 5 panels")
        self.assert_content_safe(VGroup(hud_box, hud_label, hud_eq), "section 5 hud")
        self.play(FadeIn(panels), FadeIn(movers), FadeIn(vectors), FadeIn(accel_vectors), run_time=RUN_NORMAL)
        self.play(FadeIn(time_hud), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        self.play(t.animate.set_value(t_show), run_time=RUN_SLOW * 1.85, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)

        conclusion = self.phase_card(
            1,
            "NO SON TRES FÓRMULAS",
            "Son tres valores de v₀ dentro del mismo modelo. El signo conserva la dirección física.",
            7.5,
        ).move_to([0, -3.22, 0])
        self.play(FadeOut(time_hud), run_time=RUN_QUICK)
        self.checkpoint(conclusion, PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 06 — LANZAMIENTO HACIA ARRIBA Y PUNTO MÁS ALTO
    # =========================================================================
    def scene_06_upward_throw_apex(self) -> None:
        self.set_header(
            6,
            "PUNTO MÁS ALTO: v = 0, PERO a = −g",
            "La pelota se detiene solo un instante. La gravedad no desaparece: es precisamente la aceleración que invierte la velocidad.",
        )

        t = ValueTracker(0.0)
        y_start = -2.15
        span = 3.85

        def state(tt: float) -> MotionState:
            return MotionState(tt, V0_APEX * tt - 0.5 * G * tt**2, V0_APEX - G * tt, -G)

        def y_scene(tt: float) -> float:
            return y_start + span * max(0.0, state(tt).y) / H_APEX

        track = DashedLine([-4.65, -2.15, 0], [-4.65, 1.85, 0], dash_length=0.08, color=LIGHT_GRAY)
        floor = self.ground(-2.15, -5.60, -3.65)
        moving = always_redraw(lambda: self.ball([-4.65, y_scene(t.get_value()), 0], 0.19))

        def velocity_live():
            s = state(t.get_value())
            if abs(s.v) < 0.18:
                return self.math(r"v_y=0", 29).move_to([-3.65, y_scene(t.get_value()), 0])
            length = np.clip(s.v / V0_APEX, -1.10, 1.10)
            return self.vector_arrow([-4.05, y_scene(t.get_value()), 0], UP * length, r"v_y", label_size=23)

        velocity = always_redraw(velocity_live)
        acceleration = always_redraw(
            lambda: self.vector_arrow([-5.20, y_scene(t.get_value()), 0], DOWN * 0.76, r"a_y=-g", label_size=22, label_side=LEFT)
        )
        hud = self.live_state_panel(t, state, title="ESTADO FÍSICO", width=3.85, position=[-1.50, -0.25, 0])

        self.play(FadeIn(track), FadeIn(floor), FadeIn(moving), FadeIn(velocity), FadeIn(acceleration), FadeIn(hud), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(T_APEX), run_time=RUN_SLOW * 1.80, rate_func=linear)

        apex_card = self.focus_panel(
            "EN EL PUNTO MÁS ALTO",
            ["La posición es máxima.", "La velocidad instantánea es cero.", "La aceleración sigue apuntando hacia abajo."],
            equation=r"v_y=0\qquad a_y=-g",
            meaning="v = 0 NO IMPLICA a = 0",
            width=5.55,
            height=3.55,
        ).move_to([4.40, 0.12, 0])
        self.play(FadeIn(apex_card), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        self.play(FadeOut(apex_card), run_time=RUN_QUICK)
        derivation = VGroup(
            self.math(r"0=v_0-gt_{max}", 43),
            self.math(r"t_{max}=\frac{v_0}{g}=1.43\;s", 43),
            self.math(r"\Delta y_{max}=\frac{v_0^2}{2g}=9.99\;m", 43),
        ).arrange(DOWN, buff=0.42).move_to([4.15, -0.10, 0])
        self.assert_content_safe(derivation, "section 6 derivation")
        self.animate_equation_stack(derivation, pause=PAUSE_EXPLAIN)

        self.play(t.animate.set_value(T_RETURN), run_time=RUN_SLOW * 1.90, rate_func=linear)
        symmetry = self.phase_card(
            2,
            "REGRESA A LA ALTURA DE LANZAMIENTO",
            "Sin resistencia del aire, vuelve con la misma rapidez y dirección opuesta.",
            6.2,
        ).move_to([3.85, -2.55, 0])
        self.checkpoint(symmetry, PAUSE_EXPLAIN)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 07 — TRES PROBLEMAS SOBRE LA MISMA ALTURA
    # =========================================================================
    def scene_07_same_height_three_worked_cases(self) -> None:
        self.set_header(
            7,
            "MISMA ALTURA, TRES CONDICIONES INICIALES",
            "Aplicamos la ecuación maestra sin cambiar reglas: y₀ = 20 m, suelo en y = 0 y +y hacia arriba.",
        )

        master = self.formula_panel(
            r"0=20+v_0t-\frac12(9.81)t^2\qquad\quad v=v_0-9.81t",
            width=10.0,
            height=1.05,
            font_size=39,
        ).move_to([0, 1.85, 0])
        self.play(FadeIn(master), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        cases = [
            (
                "A · SE SUELTA",
                ["v₀ = 0 m/s", f"t_impacto = {T_RELEASE:.2f} s", f"v_impacto = {V_RELEASE_IMPACT:.2f} m/s"],
                r"v_0=0",
                "EMPIEZA SIN VELOCIDAD",
            ),
            (
                "B · HACIA ABAJO",
                ["v₀ = −5 m/s", f"t_impacto = {T_DOWN:.2f} s", f"v_impacto = {V_DOWN_IMPACT:.2f} m/s"],
                r"v_0=-5\;\mathrm{m/s}",
                "LLEGA ANTES",
            ),
            (
                "C · HACIA ARRIBA",
                ["v₀ = +5 m/s", f"t_impacto = {T_UP:.2f} s", f"v_impacto = {V_UP_IMPACT:.2f} m/s"],
                r"v_0=+5\;\mathrm{m/s}",
                "PRIMERO SUBE; LUEGO CAE",
            ),
        ]

        current = None
        positions = [0, 0, 0]
        for i, (title, lines, eq, meaning) in enumerate(cases, start=1):
            panel = self.focus_panel(
                title,
                lines,
                equation=eq,
                meaning=meaning,
                width=7.0,
                height=3.55,
            ).move_to([0, -0.75, 0])
            if current is None:
                self.play(FadeIn(panel), run_time=RUN_NORMAL)
            else:
                self.play(ReplacementTransform(current, panel), run_time=RUN_NORMAL)
            current = panel
            self.wait(PAUSE_WORK if i == 1 else PAUSE_EXPLAIN)

        self.play(FadeOut(current), run_time=RUN_QUICK)
        invariant = self.focus_panel(
            "ECUACIÓN SIN TIEMPO",
            [
                "Para comparar rapidez entre dos alturas no necesitamos resolver t.",
                "Los casos ±5 m/s tienen el mismo v₀².",
                f"Por eso ambos impactan con rapidez ≈ {abs(V_DOWN_IMPACT):.2f} m/s.",
            ],
            equation=r"\boxed{v^2=v_0^2-2g(y-y_0)}",
            meaning="LA DIRECCIÓN INICIAL CAMBIA EL TIEMPO; v₀² CONTROLA LA RAPIDEZ EN UNA ALTURA DADA",
            width=10.1,
            height=3.60,
        ).move_to([0, -0.70, 0])
        self.play(FadeIn(invariant), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 08 — GALILEO: PLANO INCLINADO Y LEY CUADRÁTICA
    # =========================================================================
    def scene_08_galileo_ramp_square_law(self) -> None:
        self.set_header(
            8,
            "GALILEO HACE MEDIBLE LA ACELERACIÓN",
            "El plano inclinado alarga el intervalo de medición; la aceleración exacta depende del modelo mecánico, pero la estructura de aceleración constante permanece comprobable.",
        )

        # Fase A — caída libre: ventana temporal corta.
        fall_top = np.array([-3.00, 1.45, 0])
        fall_bottom = np.array([-3.00, -2.15, 0])
        fall_track = Line(fall_top, fall_bottom, color=BLACK_LINE, stroke_width=3.8)
        fall_floor = self.ground(-2.15, -3.85, -2.15)
        ball = self.ball(fall_top, 0.20)
        free_label = self.text("CAÍDA LIBRE", 31, BOLD).move_to([-3.00, 1.95, 0])
        free_panel = self.focus_panel(
            "VENTANA CORTA",
            ["La caída ocurre rápidamente.", "Un error pequeño en t pesa mucho porcentualmente."],
            equation=r"a=g",
            meaning="DIFÍCIL DE CRONOMETRAR CON TECNOLOGÍA ANTIGUA",
            width=5.9,
            height=3.15,
        ).move_to([3.55, -0.15, 0])
        self.assert_content_safe(VGroup(fall_track, fall_floor, ball, free_label, free_panel), "section 8 free fall")
        self.play(FadeIn(fall_track), FadeIn(fall_floor), FadeIn(ball), FadeIn(free_label), FadeIn(free_panel), run_time=RUN_NORMAL)
        self.play(ball.animate.move_to(fall_bottom), run_time=0.72, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(VGroup(fall_track, fall_floor, ball, free_label, free_panel)), run_time=RUN_NORMAL)

        # Fase B — plano inclinado: misma lógica cinemática, tiempo más largo.
        ramp_start = np.array([-5.65, -2.35, 0])
        ramp_end = np.array([0.25, 1.38, 0])
        ramp = Line(ramp_start, ramp_end, color=BLACK_LINE, stroke_width=3.9)
        floor = Line([-6.05, -2.35, 0], [0.75, -2.35, 0], color=LIGHT_GRAY, stroke_width=1.6)
        ramp_ball = self.ball(ramp_end, 0.20)
        ramp_label = self.text("PLANO INCLINADO", 31, BOLD).move_to([-2.65, 1.92, 0])
        ramp_panel = self.focus_panel(
            "VENTANA MÁS LARGA",
            ["Movimiento más lento y observable.", "La aceleración exacta depende de deslizamiento/rodadura."],
            equation=r"x-x_0=\frac12at^2\quad(v_0=0)",
            meaning="OBJETIVO: COMPROBAR a ≈ CONSTANTE",
            width=5.8,
            height=3.25,
        ).move_to([3.65, -0.15, 0])
        self.assert_content_safe(VGroup(ramp, floor, ramp_ball, ramp_label, ramp_panel), "section 8 ramp")
        self.play(FadeIn(ramp), FadeIn(floor), FadeIn(ramp_ball), FadeIn(ramp_label), FadeIn(ramp_panel), run_time=RUN_NORMAL)
        self.play(ramp_ball.animate.move_to(ramp_start), run_time=RUN_SLOW * 1.95, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(ramp_panel), run_time=RUN_QUICK)
        self.play(ramp_ball.animate.move_to(ramp_end), run_time=RUN_QUICK)

        # Fase C — pulsos 1:4:9:16 sin acumular texto sobre la rampa.
        points = [ramp.point_from_proportion(1.0 - q / 16.0) for q in RAMP_X]
        marks = VGroup()
        for p in points:
            tick = Line(DOWN * 0.14, UP * 0.14, color=BLACK_LINE, stroke_width=2.0)
            tick.rotate(ramp.get_angle() + PI / 2)
            tick.move_to(p)
            marks.add(tick)
        self.play(FadeIn(marks), run_time=RUN_NORMAL)

        data_box = RoundedRectangle(
            width=5.4,
            height=3.7,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        ).move_to([3.75, -0.45, 0])
        data_title = self.text("TIEMPOS IGUALES", 28, BOLD).move_to(data_box.get_top() + DOWN * 0.38)
        self.play(FadeIn(data_box), FadeIn(data_title), run_time=RUN_NORMAL)

        current_row = None
        for i, (tt, xx, p) in enumerate(zip(RAMP_T, RAMP_X, points), start=1):
            row = self.text(f"t = {tt:.0f}  →  x/x₁ = {xx:.0f}", 29, BOLD).move_to([3.75, -0.20, 0])
            pulse = self.text(f"{i}", 34, BOLD).move_to(p + UP * 0.48)
            self.play(ramp_ball.animate.move_to(p), FadeIn(pulse), run_time=0.70, rate_func=linear)
            if current_row is None:
                self.play(FadeIn(row), run_time=RUN_QUICK)
            else:
                self.play(ReplacementTransform(current_row, row), run_time=RUN_QUICK)
            current_row = row
            self.wait(PAUSE_READ)
            self.play(FadeOut(pulse), run_time=RUN_QUICK)

        sequence = self.math(r"1:4:9:16=1^2:2^2:3^2:4^2", 42).move_to([3.75, -1.18, 0])
        intervals = self.math(r"\Delta x\;\propto\;1:3:5:7", 38).move_to([3.75, -1.82, 0])
        self.play(FadeIn(sequence), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(intervals), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        measurement_group = VGroup(ramp, floor, ramp_ball, ramp_label, marks, data_box, data_title, current_row, sequence, intervals)
        self.play(FadeOut(measurement_group), run_time=RUN_NORMAL)

        # Fase D — despejar la pantalla y promover x vs t² a evidencia central.
        axes = Axes(
            x_range=[0, 16, 4],
            y_range=[0, 16, 4],
            x_length=8.0,
            y_length=4.55,
            axis_config={"color": BLACK_LINE, "stroke_width": 1.7, "include_tip": False},
        ).move_to([-2.45, -0.55, 0])
        labels = VGroup(
            self.text("t²", 27, BOLD).next_to(axes.x_axis, DOWN, buff=0.26),
            self.text("desplazamiento", 27, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.30),
        )
        tick_labels = VGroup()
        for q in (0, 4, 8, 12, 16):
            tick_labels.add(self.text(str(q), 19).next_to(axes.c2p(q, 0), DOWN, buff=0.07))
            tick_labels.add(self.text(str(q), 19).next_to(axes.c2p(0, q), LEFT, buff=0.07))
        line = Line(axes.c2p(0, 0), axes.c2p(16, 16), color=LIGHT_GRAY, stroke_width=3.0)
        dots = VGroup(*[Dot(axes.c2p(q, q), radius=0.09, color=BLACK_LINE) for q in RAMP_X])
        result = self.focus_panel(
            "PRUEBA LINEAL",
            ["Si x ∝ t², los puntos deben formar una recta.", "La pendiente representa a/2."],
            equation=r"x-x_0=\left(\frac a2\right)t^2",
            meaning="PARA CAÍDA LIBRE: a = g EN MAGNITUD",
            width=5.15,
            height=3.45,
        ).move_to([4.95, -0.45, 0])
        self.assert_content_safe(VGroup(axes, labels, tick_labels, result), "section 8 linearized")
        self.play(FadeIn(axes), FadeIn(labels), FadeIn(tick_labels), FadeIn(result), run_time=RUN_NORMAL)
        self.play(Create(line), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.6) for dot in dots], lag_ratio=0.16), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 09 — MAPA DE DECISIÓN FINAL
    # =========================================================================
    def scene_09_method_map(self) -> None:
        self.set_header(
            9,
            "MÉTODO PARA RESOLVER CUALQUIER CASO DE CAÍDA LIBRE",
            "La estrategia evita memorizar fórmulas separadas para subir, bajar o soltar: primero se fija el sistema de signos y después se sustituye.",
        )

        route = self.process_map(
            [
                ("1", "FIJA +y Y EL ORIGEN"),
                ("2", "ESCRIBE aᵧ = −g"),
                ("3", "IDENTIFICA y₀ Y v₀"),
                ("4", "USA y = y₀ + v₀t − ½gt²"),
                ("5", "USA v = v₀ − gt"),
                ("6", "INTERPRETA SIGNO Y UNIDADES"),
            ],
            card_width=4.45,
            card_height=1.15,
            columns=3,
        ).move_to([0, 0.55, 0])
        self.fit(route, 14.0, 3.2)
        self.assert_content_safe(route, "section 9 route")

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10), run_time=RUN_SLOW * 1.55)
        self.wait(PAUSE_EXPLAIN)

        equations = VGroup(
            self.formula_panel(r"a_y=-g", width=3.7, height=0.95, font_size=42),
            self.formula_panel(r"v_y=v_0-gt", width=4.4, height=0.95, font_size=42),
            self.formula_panel(r"y=y_0+v_0t-\frac12gt^2", width=5.7, height=0.95, font_size=40),
        ).arrange(RIGHT, buff=0.28).move_to([0, -2.10, 0])
        self.assert_content_safe(equations, "section 9 equations")
        self.play(FadeIn(equations[0]), run_time=RUN_NORMAL)
        self.play(FadeIn(equations[1]), run_time=RUN_NORMAL)
        self.play(FadeIn(equations[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)

        final = self.text(
            "Subir, bajar o soltar no cambia la gravedad: cambia v₀. La consistencia de signos convierte todos los casos en un único modelo.",
            27,
            BOLD,
        )
        self.fit(final, 13.8, 0.80)
        final.to_edge(DOWN, buff=0.30)
        self.play(FadeIn(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()
