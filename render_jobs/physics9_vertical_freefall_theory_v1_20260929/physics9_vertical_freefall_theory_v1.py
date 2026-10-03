#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Movimiento vertical y caída libre
THEORY V1 — consolidated classroom scene for the laboratory sequence
ManimCE 0.20.x | 1920x1080 | 30 fps

Purpose
-------
Build the complete theory foundation BEFORE the laboratory:
1. Distinguish vertical motion from ideal free fall.
2. Define the signed vertical axis.
3. Derive a_y = -g from Newton's second law.
4. Derive the constant-acceleration equations.
5. Unify drop, upward launch and downward launch.
6. Explain the highest point correctly: v = 0 but a = -g.
7. Read y(t), v(t) and a(t) as one physical story.
8. Connect theory to the experiment through d = 1/2 g t^2
   and the linear test d versus t^2.

Physical model
--------------
- +y upward.
- Near Earth's surface, g = 9.81 m/s^2 downward.
- Ideal free fall: gravity is the only relevant force after release.
- Air resistance is neglected unless explicitly discussed.
"""

from __future__ import annotations

import math
import os

import numpy as np
from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE


# =============================================================================
# PHYSICS DATA
# =============================================================================
G = 9.81

# Worked upward throw
V0_UP = 14.0
T_UP = V0_UP / G
H_MAX = V0_UP**2 / (2 * G)
T_RETURN = 2 * T_UP

# Worked drop
DROP_H = 20.0
T_DROP = math.sqrt(2 * DROP_H / G)
V_DROP = G * T_DROP

# Equal-time theoretical free-fall samples used only as a prediction bridge
LAB_TIMES = [0.2, 0.4, 0.6, 0.8]
LAB_DIST = [0.5 * G * t**2 for t in LAB_TIMES]

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))


# =============================================================================
# VISUAL SYSTEM — JP CLASSROOM MONOCHROME
# =============================================================================
INK = "#202020"
MID = "#666666"
LIGHT = "#D7D7D7"
PALE = "#F5F5F5"
PAPER = "#FAFAFA"

SAFE_W = 14.4
SAFE_H = 7.25


def verify_data() -> None:
    """Numerically validate every displayed worked value."""
    assert abs(V0_UP - G * T_UP) < 1e-12
    assert abs(H_MAX - (V0_UP * T_UP - 0.5 * G * T_UP**2)) < 1e-12
    assert abs(T_RETURN - 2 * T_UP) < 1e-12
    assert abs(0.5 * G * T_DROP**2 - DROP_H) < 1e-12
    assert abs(V_DROP - math.sqrt(2 * G * DROP_H)) < 1e-12
    ratios = [d / LAB_DIST[0] for d in LAB_DIST]
    for got, expected in zip(ratios, [1, 4, 9, 16]):
        assert abs(got - expected) < 1e-12


class Physics9VerticalFreeFallTheoryV1(Scene):
    """Full theory scene preceding the vertical-motion/free-fall laboratory."""

    def setup(self) -> None:
        verify_data()
        self.camera.background_color = WHITE

    # -------------------------------------------------------------------------
    # Timing wrappers
    # -------------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Typography and safe fitting
    # -------------------------------------------------------------------------
    def text(self, s: str, size=30, weight=NORMAL, color=INK) -> Text:
        return Text(
            s,
            font_size=size,
            weight=weight,
            color=color,
            line_spacing=0.90,
        )

    def math(self, s: str, size=38, color=INK) -> MathTex:
        return MathTex(s, font_size=size, color=color)

    def fit(self, mob: Mobject, w=SAFE_W, h=SAFE_H) -> Mobject:
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def clear_stage(self) -> None:
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        badge = Circle(
            radius=0.27,
            stroke_color=INK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.text(str(number), 21, BOLD).move_to(badge)
        title_m = self.text(title, 31, BOLD)
        left = VGroup(badge, num, title_m).arrange(RIGHT, buff=0.17)

        sub = self.text(subtitle, 21, color=MID)
        self.fit(sub, 14.25, 0.62)

        group = VGroup(left, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        group.to_edge(UP, buff=0.24).to_edge(LEFT, buff=0.45)

        rule = Line(
            LEFT * 7.48,
            RIGHT * 7.48,
            color=LIGHT,
            stroke_width=1.5,
        ).next_to(group, DOWN, buff=0.11)

        self.add(group, rule)
        return VGroup(group, rule)

    def panel(
        self,
        title: str,
        lines: list[str],
        width=6.3,
        height=None,
        body_size=21,
    ) -> VGroup:
        tt = self.text(title, 24, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(tt, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.55, 4.6)

        h = height if height else max(1.22, content.height + 0.58)
        box = RoundedRectangle(
            width=width,
            height=h,
            corner_radius=0.12,
            stroke_color=INK,
            stroke_width=1.7,
            fill_color=WHITE,
            fill_opacity=1,
        )
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def formula_box(self, expr: str, width=6.1, size=41, height=1.06) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=INK,
            stroke_width=1.8,
            fill_color=PALE,
            fill_opacity=1,
        )
        eq = self.math(expr, size)
        self.fit(eq, width - 0.45, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    def ball(self, p, radius=0.20) -> Circle:
        return Circle(
            radius=radius,
            stroke_color=INK,
            stroke_width=2.4,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(p)

    def vector_arrow(self, start, vec, label, label_side=RIGHT) -> VGroup:
        arrow = Arrow(
            start,
            start + vec,
            buff=0,
            color=INK,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18,
        )
        lab = self.math(label, 26).next_to(arrow, label_side, buff=0.08)
        return VGroup(arrow, lab)

    # =========================================================================
    # MASTER TIMELINE
    # =========================================================================
    def construct(self) -> None:
        self.opening()
        self.scene_01_vertical_vs_freefall()
        self.scene_02_axis_and_signs()
        self.scene_03_force_to_acceleration()
        self.scene_04_equation_derivation()
        self.scene_05_three_initial_conditions()
        self.scene_06_highest_point_and_symmetry()
        self.scene_07_graphs_one_story()
        self.scene_08_worked_examples()
        self.scene_09_theory_to_lab()
        self.scene_10_model_limits_and_check()
        self.closing()

    # =========================================================================
    # OPENING
    # =========================================================================
    def opening(self) -> None:
        course = self.text("FÍSICA 9° · CINEMÁTICA VERTICAL", 27, BOLD)
        title = self.text("MOVIMIENTO VERTICAL Y CAÍDA LIBRE", 49, BOLD)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=INK, stroke_width=2)
        sub = self.text(
            "Teoría consolidada antes del laboratorio: fuerza, signos, ecuaciones, gráficas y predicción experimental.",
            25,
        )
        promise = self.text(
            "MODELO FÍSICO → ECUACIONES → INTERPRETACIÓN → PRUEBA EXPERIMENTAL",
            23,
            BOLD,
        )
        group = VGroup(course, title, line, sub, promise).arrange(DOWN, buff=0.27)
        self.fit(group, 14.2, 6.2)

        self.play(FadeIn(course, shift=UP * 0.12))
        self.play(Write(title), run_time=1.15)
        self.play(Create(line), FadeIn(sub))
        self.wait(2.0)
        self.play(FadeIn(promise))
        self.wait(2.4)
        self.clear_stage()

    # =========================================================================
    # 1 — VERTICAL MOTION VS FREE FALL
    # =========================================================================
    def scene_01_vertical_vs_freefall(self) -> None:
        self.header(
            1,
            "MOVIMIENTO VERTICAL NO ES SINÓNIMO DE CAÍDA LIBRE",
            "Movimiento vertical describe la trayectoria. Caída libre describe qué fuerzas actúan.",
        )

        vertical = self.panel(
            "MOVIMIENTO VERTICAL",
            [
                "La posición cambia sobre un eje vertical.",
                "El objeto puede subir, bajar o cambiar de sentido.",
                "Puede haber gravedad, tensión, normal o resistencia del aire.",
            ],
            6.5,
        ).move_to(LEFT * 3.55 + DOWN * 0.20)

        free = self.panel(
            "CAÍDA LIBRE IDEAL",
            [
                "Después de soltar o lanzar, solo actúa la gravedad.",
                "No hay contacto, tensión ni empuje sostenido.",
                "En el modelo elemental se desprecia el aire.",
            ],
            6.5,
        ).move_to(RIGHT * 3.55 + DOWN * 0.20)

        self.play(FadeIn(vertical, shift=RIGHT * 0.10))
        self.wait(1.5)
        self.play(FadeIn(free, shift=LEFT * 0.10))
        self.wait(2.2)

        key = self.formula_box(
            r"\text{caída libre ideal}\;\Longrightarrow\;\sum \vec F=\vec W=m\vec g",
            width=9.2,
            size=37,
        ).to_edge(DOWN, buff=0.47)
        self.play(FadeIn(key))
        self.wait(2.8)
        self.clear_stage()

    # =========================================================================
    # 2 — COORDINATE AXIS AND SIGNS
    # =========================================================================
    def scene_02_axis_and_signs(self) -> None:
        self.header(
            2,
            "ANTES DE USAR ECUACIONES: FIJAMOS EL EJE",
            "Usaremos +y hacia arriba. La gravedad apunta hacia abajo, por eso a_y = −g.",
        )

        axis = Arrow(
            LEFT * 4.8 + DOWN * 2.2,
            LEFT * 4.8 + UP * 2.25,
            buff=0,
            color=INK,
            stroke_width=3,
        )
        origin = Dot(LEFT * 4.8 + DOWN * 0.25, radius=0.07, color=INK)
        plus = self.text("+y", 24, BOLD).next_to(axis, UP, buff=0.08)
        minus = self.text("−y", 24, BOLD).next_to(axis, DOWN, buff=0.08)
        zero = self.text("origen", 20).next_to(origin, RIGHT, buff=0.12)

        ball = self.ball(LEFT * 3.2 + UP * 1.20)
        vup = self.vector_arrow(ball.get_center() + LEFT * 0.45, UP * 1.15, r"v_y>0", LEFT)
        gdown = self.vector_arrow(ball.get_center() + RIGHT * 0.48, DOWN * 1.35, r"a_y=-g")

        self.play(GrowArrow(axis), FadeIn(origin), FadeIn(plus), FadeIn(minus), FadeIn(zero))
        self.play(FadeIn(ball))
        self.play(FadeIn(vup), FadeIn(gdown))
        self.wait(2.0)

        signs = self.panel(
            "LECTURA DE SIGNOS",
            [
                "Sube: v_y > 0.",
                "Instante más alto: v_y = 0.",
                "Baja: v_y < 0.",
                "Durante toda la caída libre: a_y = −9.81 m/s².",
            ],
            6.9,
        ).move_to(RIGHT * 3.3 + DOWN * 0.15)

        self.play(FadeIn(signs))
        self.wait(3.0)

        bottom = self.text(
            "El signo de la velocidad puede cambiar. El signo de la aceleración gravitatoria no cambia.",
            22,
            BOLD,
        )
        self.fit(bottom, 13.8, 0.58)
        bottom.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(bottom))
        self.wait(2.6)
        self.clear_stage()

    # =========================================================================
    # 3 — FORCE MODEL TO ACCELERATION
    # =========================================================================
    def scene_03_force_to_acceleration(self) -> None:
        self.header(
            3,
            "LA ACELERACIÓN NO SE MEMORIZA: SE OBTIENE DE LAS FUERZAS",
            "En caída libre ideal, la segunda ley de Newton conduce directamente a a_y = −g.",
        )

        ball = self.ball(LEFT * 4.0 + UP * 0.80, 0.28)
        weight = self.vector_arrow(
            ball.get_center() + RIGHT * 0.55,
            DOWN * 1.70,
            r"\vec W=m\vec g",
        )
        label = self.text("DIAGRAMA DE CUERPO LIBRE", 22, BOLD).move_to(LEFT * 3.7 + UP * 2.45)

        self.play(FadeIn(label), FadeIn(ball))
        self.play(GrowArrow(weight[0]), FadeIn(weight[1]))
        self.wait(1.7)

        equations = VGroup(
            self.formula_box(r"\sum F_y=ma_y", 6.2, 41),
            self.formula_box(r"-mg=ma_y", 6.2, 41),
            self.formula_box(r"a_y=-g=-9.81\,\mathrm{m/s^2}", 6.2, 39),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 2.7 + UP * 0.45)

        for eq in equations:
            self.play(FadeIn(eq), run_time=0.55)
            self.wait(0.9)

        mass = self.formula_box(
            r"a_y=\frac{-mg}{m}=-g",
            5.5,
            39,
        ).move_to(RIGHT * 2.7 + DOWN * 2.05)
        self.play(FadeIn(mass))
        self.wait(1.7)

        note = self.text(
            "En vacío, todos los cuerpos tienen la misma aceleración gravitatoria: la masa se cancela.",
            21,
            BOLD,
        )
        self.fit(note, 13.8, 0.55)
        note.to_edge(DOWN, buff=0.20)
        self.play(FadeIn(note))
        self.wait(2.7)
        self.clear_stage()

    # =========================================================================
    # 4 — DERIVE KINEMATIC EQUATIONS
    # =========================================================================
    def scene_04_equation_derivation(self) -> None:
        self.header(
            4,
            "DE a(t) A v(t) Y y(t): UNA SOLA CADENA LÓGICA",
            "Con aceleración constante a_y = −g, integramos una vez para velocidad y otra vez para posición.",
        )

        left = VGroup(
            self.formula_box(r"a_y=\frac{dv_y}{dt}=-g", 6.2, 38),
            self.formula_box(r"dv_y=-g\,dt", 6.2, 39),
            self.formula_box(r"v_y(t)=v_0-gt", 6.2, 42),
        ).arrange(DOWN, buff=0.23).move_to(LEFT * 3.45 + DOWN * 0.05)

        right = VGroup(
            self.formula_box(r"v_y=\frac{dy}{dt}=v_0-gt", 6.2, 35),
            self.formula_box(r"dy=(v_0-gt)\,dt", 6.2, 36),
            self.formula_box(r"y(t)=y_0+v_0t-\frac12gt^2", 6.2, 37),
        ).arrange(DOWN, buff=0.23).move_to(RIGHT * 3.45 + DOWN * 0.05)

        self.play(FadeIn(left[0]))
        self.wait(0.8)
        self.play(FadeIn(left[1]))
        self.wait(0.8)
        self.play(FadeIn(left[2]))
        self.wait(1.3)

        bridge = Arrow(
            LEFT * 0.65 + DOWN * 0.10,
            RIGHT * 0.65 + DOWN * 0.10,
            buff=0,
            color=INK,
            stroke_width=3,
        )
        self.play(GrowArrow(bridge))

        self.play(FadeIn(right[0]))
        self.wait(0.8)
        self.play(FadeIn(right[1]))
        self.wait(0.8)
        self.play(FadeIn(right[2]))
        self.wait(1.8)

        elim = self.formula_box(
            r"v_y^2=v_0^2-2g(y-y_0)",
            7.0,
            40,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(elim))
        self.wait(2.8)
        self.clear_stage()

    # =========================================================================
    # 5 — THREE INITIAL CONDITIONS, ONE MODEL
    # =========================================================================
    def motion_card(self, x, title, v0_expr, direction) -> VGroup:
        box = RoundedRectangle(
            width=4.25,
            height=4.65,
            corner_radius=0.12,
            stroke_color=INK,
            stroke_width=1.6,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to([x, -0.25, 0])

        tt = self.text(title, 23, BOLD).next_to(box.get_top(), DOWN, buff=0.18)
        b = self.ball(np.array([x, 0.65, 0]), 0.22)

        if direction == "up":
            v = self.vector_arrow(np.array([x - 0.42, 0.55, 0]), UP * 1.05, r"\vec v_0", LEFT)
        elif direction == "down":
            v = self.vector_arrow(np.array([x - 0.42, 0.80, 0]), DOWN * 1.05, r"\vec v_0", LEFT)
        else:
            v = self.math(r"v_0=0", 27).move_to([x - 0.80, 0.85, 0])

        g = self.vector_arrow(np.array([x + 0.45, 0.75, 0]), DOWN * 1.25, r"\vec g")
        initial = self.math(v0_expr, 29).move_to([x, -1.05, 0])
        common = self.math(r"a_y=-g", 29).move_to([x, -1.62, 0])
        equation = self.math(r"y=y_0+v_0t-\frac12gt^2", 25).move_to([x, -2.20, 0])

        return VGroup(box, tt, b, v, g, initial, common, equation)

    def scene_05_three_initial_conditions(self) -> None:
        self.header(
            5,
            "TRES SITUACIONES, LAS MISMAS ECUACIONES",
            "Soltar, lanzar hacia arriba o lanzar hacia abajo cambia v₀; la aceleración gravitatoria permanece igual.",
        )

        cards = VGroup(
            self.motion_card(-4.65, "SE SUELTA", r"v_0=0", "zero"),
            self.motion_card(0.00, "SE LANZA HACIA ARRIBA", r"v_0>0", "up"),
            self.motion_card(4.65, "SE LANZA HACIA ABAJO", r"v_0<0", "down"),
        )

        self.play(FadeIn(cards[0], shift=UP * 0.08))
        self.wait(1.0)
        self.play(FadeIn(cards[1], shift=UP * 0.08))
        self.wait(1.0)
        self.play(FadeIn(cards[2], shift=UP * 0.08))
        self.wait(2.2)

        note = self.text(
            "La dirección inicial está en v₀. La gravedad entra siempre como −g porque nuestro +y apunta hacia arriba.",
            21,
            BOLD,
        )
        self.fit(note, 14.1, 0.55)
        note.to_edge(DOWN, buff=0.17)
        self.play(FadeIn(note))
        self.wait(2.8)
        self.clear_stage()

    # =========================================================================
    # 6 — APEX AND SYMMETRY
    # =========================================================================
    def scene_06_highest_point_and_symmetry(self) -> None:
        self.header(
            6,
            "PUNTO MÁS ALTO: v = 0 NO SIGNIFICA a = 0",
            "Para un lanzamiento vertical hacia arriba, la velocidad cambia de signo mientras la aceleración sigue apuntando hacia abajo.",
        )

        x = -3.8
        y0 = -2.10
        ytop = 1.65
        path = DashedLine([x, y0, 0], [x, ytop + 0.50, 0], color=LIGHT, dash_length=0.12)
        ball = self.ball([x, y0 + 0.35, 0], 0.22)

        up_v = self.vector_arrow(ball.get_center() + LEFT * 0.42, UP * 1.15, r"v>0", LEFT)
        g1 = self.vector_arrow(ball.get_center() + RIGHT * 0.46, DOWN * 1.10, r"a=-g")

        self.play(Create(path), FadeIn(ball), FadeIn(up_v), FadeIn(g1))
        self.wait(1.5)

        self.play(
            ball.animate.move_to([x, ytop, 0]),
            FadeOut(up_v),
            g1.animate.shift(UP * (ytop - (y0 + 0.35))),
            run_time=1.6,
        )

        apex = self.math(r"v=0\quad\text{pero}\quad a=-g", 34).move_to(LEFT * 2.4 + UP * 2.45)
        self.play(FadeIn(apex))
        self.wait(1.8)

        down_v = self.vector_arrow(np.array([x - 0.42, 0.65, 0]), DOWN * 1.15, r"v<0", LEFT)
        self.play(
            ball.animate.move_to([x, 0.65, 0]),
            FadeIn(down_v),
            g1.animate.shift(DOWN * 1.0),
            run_time=1.3,
        )

        data = self.panel(
            "EJEMPLO: v₀ = 14.0 m/s",
            [
                f"Tiempo para llegar arriba: t = v₀/g ≈ {T_UP:.2f} s.",
                f"Altura adicional máxima: Δy = v₀²/(2g) ≈ {H_MAX:.2f} m.",
                f"Si regresa a la misma altura: T ≈ {T_RETURN:.2f} s.",
            ],
            7.1,
        ).move_to(RIGHT * 3.25 + DOWN * 0.05)
        self.play(FadeIn(data))
        self.wait(3.2)

        sym = self.text(
            "Sin aire y al comparar la misma altura: misma rapidez al subir y al bajar, con signo opuesto.",
            21,
            BOLD,
        )
        self.fit(sym, 13.9, 0.55)
        sym.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(sym))
        self.wait(2.6)
        self.clear_stage()

    # =========================================================================
    # 7 — POSITION, VELOCITY, ACCELERATION GRAPHS
    # =========================================================================
    def scene_07_graphs_one_story(self) -> None:
        self.header(
            7,
            "UNA MISMA TRAYECTORIA, TRES REPRESENTACIONES",
            "Usamos el lanzamiento de 14 m/s que vuelve a la misma altura: y(t), v(t) y a(t) deben ser coherentes entre sí.",
        )

        tmax = T_RETURN

        ax_y = Axes(
            x_range=[0, tmax, 1],
            y_range=[0, 11, 2],
            x_length=4.35,
            y_length=2.55,
            axis_config={"color": INK, "stroke_width": 1.6, "include_tip": False},
        ).move_to(LEFT * 4.85 + DOWN * 0.20)

        ax_v = Axes(
            x_range=[0, tmax, 1],
            y_range=[-15, 15, 5],
            x_length=4.35,
            y_length=2.55,
            axis_config={"color": INK, "stroke_width": 1.6, "include_tip": False},
        ).move_to(DOWN * 0.20)

        ax_a = Axes(
            x_range=[0, tmax, 1],
            y_range=[-12, 2, 4],
            x_length=4.35,
            y_length=2.55,
            axis_config={"color": INK, "stroke_width": 1.6, "include_tip": False},
        ).move_to(RIGHT * 4.85 + DOWN * 0.20)

        curve_y = ax_y.plot(
            lambda t: V0_UP * t - 0.5 * G * t * t,
            x_range=[0, tmax],
            color=INK,
            stroke_width=3,
        )
        curve_v = ax_v.plot(
            lambda t: V0_UP - G * t,
            x_range=[0, tmax],
            color=INK,
            stroke_width=3,
        )
        curve_a = ax_a.plot(
            lambda t: -G,
            x_range=[0, tmax],
            color=INK,
            stroke_width=3,
        )

        titles = VGroup(
            self.text("POSICIÓN y(t)", 22, BOLD).next_to(ax_y, UP, buff=0.12),
            self.text("VELOCIDAD v(t)", 22, BOLD).next_to(ax_v, UP, buff=0.12),
            self.text("ACELERACIÓN a(t)", 22, BOLD).next_to(ax_a, UP, buff=0.12),
        )
        formulas = VGroup(
            self.math(r"y=v_0t-\frac12gt^2", 25).next_to(ax_y, DOWN, buff=0.12),
            self.math(r"v=v_0-gt", 25).next_to(ax_v, DOWN, buff=0.12),
            self.math(r"a=-g", 25).next_to(ax_a, DOWN, buff=0.12),
        )

        self.play(FadeIn(ax_y), FadeIn(ax_v), FadeIn(ax_a), FadeIn(titles))
        self.play(Create(curve_y), run_time=1.3)
        self.play(Create(curve_v), run_time=1.2)
        self.play(Create(curve_a), run_time=1.0)
        self.play(FadeIn(formulas))
        self.wait(2.2)

        relation = self.panel(
            "CÓMO LEERLAS JUNTAS",
            [
                "Pendiente de y(t) = v(t).",
                "Pendiente de v(t) = a(t).",
                "a(t) constante → v(t) recta → y(t) parábola.",
            ],
            7.5,
            height=1.62,
            body_size=19,
        ).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(relation))
        self.wait(3.1)
        self.clear_stage()

    # =========================================================================
    # 8 — WORKED NUMERICAL FALL
    # =========================================================================
    def scene_08_worked_examples(self) -> None:
        self.header(
            8,
            "EJEMPLO COMPLETO: SOLTAR DESDE 20 m",
            "Partimos de y₀ = 20 m, v₀ = 0 y usamos +y hacia arriba. El suelo será y = 0.",
        )

        tower_x = -4.7
        ground_y = -2.32
        top_y = 1.95

        wall = Line(
            [tower_x - 0.85, ground_y, 0],
            [tower_x - 0.85, top_y + 0.28, 0],
            color=INK,
            stroke_width=4,
        )
        ground = Line(
            [tower_x - 1.45, ground_y, 0],
            [tower_x + 1.15, ground_y, 0],
            color=INK,
            stroke_width=3,
        )

        marks = VGroup()
        for val in [0, 5, 10, 15, 20]:
            y = ground_y + (val / 20.0) * (top_y - ground_y)
            tick = Line(
                [tower_x - 1.00, y, 0],
                [tower_x - 0.70, y, 0],
                color=INK,
                stroke_width=1.4,
            )
            lab = self.text(f"{val} m", 18).next_to(tick, LEFT, buff=0.07)
            marks.add(tick, lab)

        ball = Dot([tower_x, top_y, 0], radius=0.16, color=INK)

        self.play(Create(wall), Create(ground), FadeIn(marks), FadeIn(ball))

        derivation = VGroup(
            self.math(r"0=20-\frac12gt^2", 34),
            self.math(
                r"t=\sqrt{\frac{2(20)}{9.81}}\approx " + f"{T_DROP:.2f}" + r"\,\mathrm{s}",
                33,
            ),
            self.math(
                r"v=-gt\approx -" + f"{V_DROP:.2f}" + r"\,\mathrm{m/s}",
                33,
            ),
            self.math(
                r"|v|\approx " + f"{V_DROP:.2f}" + r"\,\mathrm{m/s}",
                33,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to(RIGHT * 2.5 + UP * 0.60)

        for eq in derivation[:2]:
            self.play(FadeIn(eq))
            self.wait(1.0)

        tracker = ValueTracker(0)
        clock = DecimalNumber(0, num_decimal_places=2, font_size=34, color=INK)
        speed = DecimalNumber(0, num_decimal_places=2, font_size=34, color=INK)

        readout = VGroup(
            VGroup(self.text("t =", 22, BOLD), clock, self.text("s", 22)).arrange(RIGHT, buff=0.08),
            VGroup(self.text("|v| =", 22, BOLD), speed, self.text("m/s", 22)).arrange(RIGHT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to(RIGHT * 3.0 + DOWN * 1.25)

        clock.add_updater(lambda d: d.set_value(tracker.get_value()))
        speed.add_updater(lambda d: d.set_value(G * tracker.get_value()))
        ball.add_updater(
            lambda q: q.move_to([
                tower_x,
                top_y - (top_y - ground_y) * (tracker.get_value() / T_DROP) ** 2,
                0,
            ])
        )

        self.play(FadeIn(readout))
        self.play(tracker.animate.set_value(T_DROP), run_time=3.0, rate_func=linear)

        ball.clear_updaters()
        clock.clear_updaters()
        speed.clear_updaters()

        self.play(FadeIn(derivation[2]))
        self.wait(0.9)
        self.play(FadeIn(derivation[3]))
        self.wait(2.7)

        sign_note = self.text(
            "v es negativa porque el objeto baja; la rapidez es el valor positivo |v|.",
            21,
            BOLD,
        )
        self.fit(sign_note, 13.5, 0.55)
        sign_note.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(sign_note))
        self.wait(2.7)
        self.clear_stage()

    # =========================================================================
    # 9 — THEORY TO LABORATORY
    # =========================================================================
    def scene_09_theory_to_lab(self) -> None:
        self.header(
            9,
            "LA PREDICCIÓN QUE EL LABORATORIO DEBE PONER A PRUEBA",
            "Si soltamos desde reposo y medimos distancia de caída d ≥ 0, la teoría predice d = ½gt².",
        )

        prediction = VGroup(
            self.formula_box(r"d=\frac12gt^2", 5.6, 45),
            self.formula_box(r"\frac{d}{t^2}=\frac{g}{2}=\text{constante}", 5.6, 35),
        ).arrange(DOWN, buff=0.23).move_to(LEFT * 4.25 + UP * 0.80)

        self.play(FadeIn(prediction[0]))
        self.wait(1.1)
        self.play(FadeIn(prediction[1]))
        self.wait(1.6)

        table_title = self.text("PREDICCIÓN PARA INTERVALOS DE TIEMPO IGUALES", 21, BOLD)
        header = VGroup(
            self.text("t (s)", 19, BOLD),
            self.text("d (m)", 19, BOLD),
            self.text("d/d₁", 19, BOLD),
        ).arrange(RIGHT, buff=0.85)

        rows = VGroup()
        for i, (t, d, ratio) in enumerate(zip(LAB_TIMES, LAB_DIST, [1, 4, 9, 16])):
            row = VGroup(
                self.text(f"{t:.1f}", 20),
                self.text(f"{d:.3f}", 20),
                self.text(str(ratio), 20, BOLD),
            ).arrange(RIGHT, buff=1.15)
            rows.add(row)

        rows.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        table = VGroup(table_title, header, rows).arrange(DOWN, buff=0.22)
        table.move_to(LEFT * 3.95 + DOWN * 1.55)

        self.play(FadeIn(table))
        self.wait(2.2)

        ax = Axes(
            x_range=[0, 0.70, 0.10],
            y_range=[0, 3.5, 0.5],
            x_length=5.2,
            y_length=3.45,
            axis_config={"color": INK, "stroke_width": 1.7, "include_tip": False},
        ).move_to(RIGHT * 3.95 + DOWN * 0.20)

        line = ax.plot(
            lambda t2: 0.5 * G * t2,
            x_range=[0, 0.64],
            color=INK,
            stroke_width=3,
        )

        points = VGroup(*[
            Dot(ax.c2p(t * t, d), radius=0.065, color=INK)
            for t, d in zip(LAB_TIMES, LAB_DIST)
        ])

        labels = VGroup(
            self.math(r"t^2\;[\mathrm{s^2}]", 24).next_to(ax, DOWN, buff=0.08),
            self.math(r"d\;[\mathrm{m}]", 24).next_to(ax, LEFT, buff=0.10),
            self.text("d vs t²", 23, BOLD).next_to(ax, UP, buff=0.12),
        )

        self.play(FadeIn(ax), FadeIn(labels))
        self.play(Create(line), FadeIn(points), run_time=1.5)
        self.wait(1.6)

        slope = self.formula_box(
            r"\text{pendiente}=\frac{\Delta d}{\Delta(t^2)}=\frac{g}{2}",
            6.4,
            33,
        ).next_to(ax, DOWN, buff=0.42)
        self.play(FadeIn(slope))
        self.wait(2.8)

        bridge = self.text(
            "En el laboratorio no buscamos “que dé perfecto”: buscamos si los datos apoyan esta relación dentro de la incertidumbre.",
            20,
            BOLD,
        )
        self.fit(bridge, 14.1, 0.55)
        bridge.to_edge(DOWN, buff=0.10)
        self.play(FadeIn(bridge))
        self.wait(3.0)
        self.clear_stage()

    # =========================================================================
    # 10 — MODEL LIMITS AND EXPERIMENTAL THINKING
    # =========================================================================
    def scene_10_model_limits_and_check(self) -> None:
        self.header(
            10,
            "QUÉ DEBEMOS CONTROLAR ANTES DE MEDIR",
            "El modelo es simple; el experimento real no. Identificamos qué puede separar los datos de la predicción ideal.",
        )

        cards = VGroup(
            self.panel(
                "CONDICIÓN DE LIBERACIÓN",
                ["Soltar sin impulso inicial.", "Definir un mismo punto de referencia."],
                6.5,
                1.55,
                19,
            ),
            self.panel(
                "TIEMPO",
                ["La resolución temporal limita la precisión.", "Video o fotopuerta reduce error humano."],
                6.5,
                1.55,
                19,
            ),
            self.panel(
                "DISTANCIA",
                ["Calibrar la escala.", "Evitar paralaje y cambiar de referencia."],
                6.5,
                1.55,
                19,
            ),
            self.panel(
                "MODELO IDEAL",
                ["Objetos muy livianos sienten más el aire.", "g ≈ constante solo para alturas pequeñas."],
                6.5,
                1.55,
                19,
            ),
            self.panel(
                "REPETICIONES",
                ["Repetir permite estimar dispersión.", "No elegir solo el dato que “se ve mejor”."],
                6.5,
                1.55,
                19,
            ),
            self.panel(
                "CRITERIO DE EVIDENCIA",
                ["Comprobar d ∝ t².", "Estimar g desde 2·pendiente."],
                6.5,
                1.55,
                19,
            ),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.34, 0.24)).move_to(DOWN * 0.27)

        self.fit(cards, 14.2, 5.75)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.06), run_time=0.33)
            self.wait(0.25)

        self.wait(3.2)
        self.clear_stage()

    # =========================================================================
    # CLOSING
    # =========================================================================
    def closing(self) -> None:
        title = self.text("MAPA DE TEORÍA → LABORATORIO", 34, BOLD)

        steps = VGroup(
            self.panel("1", ["Fuerzas"], 2.25, 0.95, 19),
            self.panel("2", ["Eje y signos"], 2.25, 0.95, 19),
            self.panel("3", ["a = −g"], 2.25, 0.95, 19),
            self.panel("4", ["v(t), y(t)"], 2.25, 0.95, 19),
            self.panel("5", ["d ∝ t²"], 2.25, 0.95, 19),
            self.panel("6", ["Medir y contrastar"], 2.25, 0.95, 19),
        ).arrange(RIGHT, buff=0.16)

        final = self.text(
            "La teoría no termina en una fórmula: termina en una predicción que puede medirse.",
            29,
            BOLD,
        )
        self.fit(final, 13.8, 0.82)

        next_step = self.text(
            "SIGUIENTE: montaje, protocolo de medición, tabla de datos, gráfica d vs t² y estimación experimental de g.",
            22,
        )
        self.fit(next_step, 13.8, 0.65)

        group = VGroup(title, steps, final, next_step).arrange(DOWN, buff=0.48)
        self.fit(group, 14.5, 6.3)

        self.play(FadeIn(title))
        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.06) for s in steps], lag_ratio=0.14),
            run_time=1.8,
        )
        self.wait(1.6)
        self.play(FadeIn(final))
        self.wait(2.2)
        self.play(FadeIn(next_step))
        self.wait(4.0)
        self.clear_stage()
