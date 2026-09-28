#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Free Fall, Weight, Apparent Weight and Weightlessness
Senior QA V2 — phenomenon-first, full-screen, dynamic ManimCE lesson.

Target:
- ManimCE 0.20.x
- 1920x1080, 30 fps
- No external assets
- +y is upward
"""

from __future__ import annotations

import math
import os
import numpy as np
from manim import *

# =============================================================================
# RENDER
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#F7F8FA"

# =============================================================================
# PHYSICS
# =============================================================================
G = 9.81
M = 60.0
W = M * G
H = 20.0
T_HIT = math.sqrt(2 * H / G)
V_HIT = G * T_HIT
A_E = 3.0
N_STATIC = M * G
N_UP = M * (G + A_E)
N_DOWN = M * (G - A_E)

R_E_KM = 6371.0
H_ORBIT_KM = 400.0
G_ORBIT = G * (R_E_KM / (R_E_KM + H_ORBIT_KM)) ** 2

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

# =============================================================================
# VISUAL SYSTEM
# =============================================================================
INK = "#102A43"
BLUE = "#1565C0"
CYAN = "#00838F"
RED = "#C62828"
GREEN = "#2E7D32"
ORANGE = "#EF6C00"
PURPLE = "#6A1B9A"
MID = "#52606D"
LIGHT = "#D9E2EC"
PAPER = "#FFFFFF"
PALE_BLUE = "#EAF3FF"
PALE_RED = "#FDECEC"
PALE_GREEN = "#EAF6EC"
PALE_ORANGE = "#FFF2E5"
PALE_PURPLE = "#F3EAF8"


def validate_physics() -> None:
    assert abs(W - 588.6) < 1e-9
    assert abs(N_STATIC - 588.6) < 1e-9
    assert abs(N_UP - 768.6) < 1e-9
    assert abs(N_DOWN - 408.6) < 1e-9
    assert abs(0.5 * G * T_HIT**2 - H) < 1e-10
    assert abs(V_HIT - math.sqrt(2 * G * H)) < 1e-10
    assert 0.88 < G_ORBIT / G < 0.89


class Physics9FreeFallSeniorQAV2(MovingCameraScene):
    """
    V2 design goals:
    1. Use the whole frame.
    2. Animate causes before equations.
    3. Keep vectors large and color-coded.
    4. Reuse the same physical object across states.
    5. Explicitly distinguish gravitational weight W from scale reading N.
    6. Show weightlessness as common free fall, not absence of gravity.
    7. Synchronize real motion with graphs.
    """

    # -------------------------------------------------------------------------
    # Lifecycle and timing
    # -------------------------------------------------------------------------
    def setup(self) -> None:
        super().setup()
        validate_physics()
        self.camera.background_color = "#F7F8FA"
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Typography / layout
    # -------------------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=INK, **kwargs):
        return Text(
            content,
            font_size=size,
            weight=weight,
            color=color,
            line_spacing=0.92,
            **kwargs,
        )

    def math(self, expr, size=40, color=INK):
        return MathTex(expr, font_size=size, color=color)

    def fit(self, mob, max_w=14.7, max_h=7.4):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def section(self, number, title, subtitle):
        badge = RoundedRectangle(
            width=0.72, height=0.54, corner_radius=0.14,
            stroke_color=INK, stroke_width=0,
            fill_color=INK, fill_opacity=1,
        )
        badge_n = self.txt(str(number), 22, BOLD, WHITE).move_to(badge)
        title_m = self.txt(title, 34, BOLD, INK)
        heading = VGroup(VGroup(badge, badge_n), title_m).arrange(RIGHT, buff=0.20)

        subtitle_m = self.txt(subtitle, 22, color=MID)
        self.fit(subtitle_m, 14.5, 0.55)

        group = VGroup(heading, subtitle_m).arrange(
            DOWN, aligned_edge=LEFT, buff=0.10
        )
        group.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.52)

        rule = Line(
            LEFT * 7.45, RIGHT * 7.45,
            stroke_color=LIGHT, stroke_width=1.8,
        ).next_to(group, DOWN, buff=0.14)

        self.play(FadeIn(group, shift=RIGHT * 0.15), Create(rule), run_time=0.55)
        return VGroup(group, rule)

    def stage_clear(self, fast=False):
        mobs = list(self.mobjects)
        if mobs:
            self.play(
                *[FadeOut(m) for m in mobs],
                run_time=0.28 if fast else 0.48,
            )
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def card(self, title, lines, width=6.2, height=None, fill=PAPER, accent=INK,
             title_size=26, body_size=22):
        title_m = self.txt(title, title_size, BOLD, accent)
        body = VGroup(*[
            self.txt(line, body_size, color=INK) for line in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title_m, body).arrange(
            DOWN, aligned_edge=LEFT, buff=0.20
        )
        self.fit(content, width - 0.65, 4.8)
        h = height if height is not None else max(1.35, content.height + 0.70)
        box = RoundedRectangle(
            width=width, height=h, corner_radius=0.16,
            stroke_color=LIGHT, stroke_width=1.7,
            fill_color=fill, fill_opacity=1,
        )
        accent_bar = Rectangle(
            width=0.10, height=h - 0.18,
            stroke_width=0, fill_color=accent, fill_opacity=1,
        ).next_to(box.get_left(), RIGHT, buff=0.08)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.42)
        return VGroup(box, accent_bar, content)

    def formula_card(self, expr, width=6.2, height=1.12, size=42,
                     fill=PALE_BLUE, color=INK):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=LIGHT, stroke_width=1.5,
            fill_color=fill, fill_opacity=1,
        )
        eq = self.math(expr, size, color=color)
        self.fit(eq, width - 0.48, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    # -------------------------------------------------------------------------
    # Physical drawing helpers
    # -------------------------------------------------------------------------
    def ball(self, center, radius=0.24, color=BLUE):
        outer = Circle(
            radius=radius,
            stroke_color=color, stroke_width=3.0,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        shine = Dot(
            center + np.array([-0.07, 0.08, 0]),
            radius=radius * 0.14,
            color=color,
        )
        return VGroup(outer, shine)

    def block(self, center, label, side=0.82, color=BLUE):
        box = RoundedRectangle(
            width=side, height=side, corner_radius=0.10,
            stroke_color=color, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        lab = self.txt(label, 20, BOLD, color).move_to(box)
        return VGroup(box, lab)

    def vector(self, start, vec, label, color, label_side=RIGHT,
               stroke=6, label_size=29):
        arrow = Arrow(
            start=start,
            end=start + vec,
            buff=0,
            stroke_width=stroke,
            color=color,
            max_tip_length_to_length_ratio=0.17,
        )
        lab = self.math(label, label_size, color=color).next_to(
            arrow, label_side, buff=0.10
        )
        return VGroup(arrow, lab)

    def person(self, center, scale=1.0):
        c = np.array(center)
        head = Circle(
            radius=0.18 * scale,
            stroke_color=INK, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(c + UP * 0.70 * scale)
        body = Line(
            c + UP * 0.50 * scale,
            c + DOWN * 0.22 * scale,
            color=INK, stroke_width=4,
        )
        arms = VGroup(
            Line(c + UP * 0.27 * scale, c + LEFT * 0.34 * scale, color=INK, stroke_width=3),
            Line(c + UP * 0.27 * scale, c + RIGHT * 0.34 * scale, color=INK, stroke_width=3),
        )
        legs = VGroup(
            Line(c + DOWN * 0.22 * scale, c + LEFT * 0.25 * scale + DOWN * 0.72 * scale, color=INK, stroke_width=3),
            Line(c + DOWN * 0.22 * scale, c + RIGHT * 0.25 * scale + DOWN * 0.72 * scale, color=INK, stroke_width=3),
        )
        return VGroup(head, body, arms, legs)

    def scale_pad(self, center, width=1.55):
        pad = RoundedRectangle(
            width=width, height=0.28, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=2.8,
            fill_color=PALE_GREEN, fill_opacity=1,
        ).move_to(center)
        display = RoundedRectangle(
            width=0.72, height=0.34, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).next_to(pad, DOWN, buff=0.10)
        return VGroup(pad, display)

    def cabin(self, center=ORIGIN, width=5.1, height=5.1):
        c = np.array(center)
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.15,
            stroke_color=INK, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(c)
        floor = Line(
            c + LEFT * (width * 0.42) + DOWN * (height * 0.30),
            c + RIGHT * (width * 0.42) + DOWN * (height * 0.30),
            color=INK, stroke_width=4,
        )
        roof = Line(
            c + LEFT * (width * 0.42) + UP * (height * 0.30),
            c + RIGHT * (width * 0.42) + UP * (height * 0.30),
            color=LIGHT, stroke_width=2,
        )
        return VGroup(shell, floor, roof)

    def earth(self, center, radius=1.55):
        e = Circle(
            radius=radius,
            stroke_color=BLUE, stroke_width=3,
            fill_color=PALE_BLUE, fill_opacity=1,
        ).move_to(center)
        arc1 = Arc(
            radius=radius * 0.66, start_angle=-0.2, angle=1.55,
            color=CYAN, stroke_width=5,
        ).move_to(center + LEFT * 0.25 + UP * 0.05)
        arc2 = Arc(
            radius=radius * 0.46, start_angle=2.8, angle=1.30,
            color=GREEN, stroke_width=5,
        ).move_to(center + RIGHT * 0.25 + DOWN * 0.22)
        return VGroup(e, arc1, arc2)

    # -------------------------------------------------------------------------
    # Lesson sequence
    # -------------------------------------------------------------------------
    def construct(self):
        self.opening_hook()
        self.scene_release_force_switch()
        self.scene_upward_toss()
        self.scene_mass_independence()
        self.scene_scale_sequence()
        self.scene_weightlessness_lab_and_orbit()
        self.scene_newton_to_kinematics()
        self.scene_twenty_meter_strobe()
        self.scene_motion_graph_sync()
        self.scene_air_drag()
        self.scene_misconception_qa()
        self.closing_map()

    # -------------------------------------------------------------------------
    # Opening
    # -------------------------------------------------------------------------
    def opening_hook(self):
        cabin = self.cabin(LEFT * 3.3, width=5.0, height=5.6)
        scale = self.scale_pad(LEFT * 3.3 + DOWN * 1.80)
        human = self.person(LEFT * 3.3 + DOWN * 0.70, scale=1.15)
        w = self.vector(
            LEFT * 2.65 + UP * 0.10,
            DOWN * 1.45,
            r"\vec W",
            RED,
        )
        n = self.vector(
            LEFT * 3.95 + DOWN * 1.25,
            UP * 1.45,
            r"\vec N",
            GREEN,
            LEFT,
        )

        question = self.txt(
            "¿QUÉ DESAPARECE CUANDO “NO PESAMOS”?",
            42, BOLD, INK
        ).move_to(RIGHT * 3.2 + UP * 1.30)
        sub = self.txt(
            "La gravedad... ¿o el apoyo?",
            31, BOLD, MID
        ).next_to(question, DOWN, buff=0.28)
        hint = self.txt(
            "Mira los vectores, no la sensación.",
            24, color=MID
        ).next_to(sub, DOWN, buff=0.20)

        self.play(FadeIn(cabin), FadeIn(scale), FadeIn(human), run_time=0.8)
        self.play(GrowArrow(w[0]), FadeIn(w[1]), GrowArrow(n[0]), FadeIn(n[1]), run_time=0.8)
        self.play(FadeIn(question, shift=UP * 0.15), FadeIn(sub), FadeIn(hint), run_time=0.8)
        self.wait(2.0)

        falling_label = self.txt("CAÍDA LIBRE", 29, BOLD, BLUE).move_to(RIGHT * 3.15 + DOWN * 0.20)
        eq = self.formula_card(r"N\rightarrow 0\qquad W=mg\neq 0", 5.8, 1.18, 40, PALE_PURPLE)
        eq.move_to(RIGHT * 3.15 + DOWN * 1.25)

        self.play(
            FadeOut(n),
            human.animate.shift(UP * 0.55),
            scale.animate.shift(DOWN * 0.18),
            cabin.animate.shift(DOWN * 0.28),
            run_time=1.1,
        )
        self.play(FadeIn(falling_label), FadeIn(eq), run_time=0.7)
        self.wait(2.1)

        title = self.txt("CAÍDA LIBRE · PESO · INGRAVIDEZ", 44, BOLD, INK)
        title.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(title, shift=UP * 0.18), run_time=0.7)
        self.wait(2.0)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 1. Release: normal disappears, weight remains
    # -------------------------------------------------------------------------
    def scene_release_force_switch(self):
        self.section(
            1,
            "EL INSTANTE DE SOLTAR: CAMBIA EL DIAGRAMA DE FUERZAS",
            "Antes de soltar hay apoyo; después de soltar, en el modelo ideal, queda solo la gravedad.",
        )

        ground = Line(LEFT * 6.6 + DOWN * 2.20, LEFT * 0.5 + DOWN * 2.20, color=INK, stroke_width=3)
        pedestal = RoundedRectangle(
            width=2.1, height=0.36, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color=PALE_GREEN, fill_opacity=1,
        ).move_to(LEFT * 3.6 + DOWN * 1.78)
        obj = self.block(LEFT * 3.6 + DOWN * 1.05, "m", 1.0, BLUE)

        w_before = self.vector(
            obj.get_center() + RIGHT * 0.72,
            DOWN * 1.30,
            r"\vec W= m\vec g",
            RED,
        )
        n_before = self.vector(
            obj.get_center() + LEFT * 0.72 + DOWN * 0.45,
            UP * 1.30,
            r"\vec N",
            GREEN,
            LEFT,
        )

        state1 = self.card(
            "ANTES DE SOLTAR",
            [
                "El soporte empuja al objeto.",
                "N = W si está en reposo.",
                "Aceleración: a = 0.",
            ],
            width=6.2, fill=PALE_GREEN, accent=GREEN,
        ).move_to(RIGHT * 3.6 + DOWN * 0.15)

        self.play(Create(ground), FadeIn(pedestal), FadeIn(obj))
        self.play(FadeIn(w_before), FadeIn(n_before), FadeIn(state1))
        self.wait(2.2)

        release = self.txt("SOLTAR", 29, BOLD, ORANGE).move_to(ORIGIN + UP * 1.55)
        self.play(FadeIn(release, scale=1.2), run_time=0.45)
        self.play(
            pedestal.animate.shift(DOWN * 1.1).set_opacity(0.15),
            FadeOut(n_before),
            FadeOut(state1),
            run_time=0.95,
        )
        self.wait(0.3)

        w_after = self.vector(
            obj.get_center() + RIGHT * 0.72,
            DOWN * 1.55,
            r"\vec W= m\vec g",
            RED,
        )
        a_after = self.vector(
            obj.get_center() + LEFT * 0.72 + UP * 0.35,
            DOWN * 1.55,
            r"\vec a=\vec g",
            ORANGE,
            LEFT,
        )
        state2 = self.card(
            "DESPUÉS DE SOLTAR",
            [
                "N = 0: ya no existe soporte.",
                "La fuerza gravitatoria W sigue actuando.",
                "ΣF = W = mg  ⇒  a = g.",
            ],
            width=6.2, fill=PALE_RED, accent=RED,
        ).move_to(RIGHT * 3.6 + DOWN * 0.15)

        self.play(Transform(w_before, w_after), FadeIn(a_after), FadeIn(state2), FadeOut(release))
        self.play(obj.animate.shift(DOWN * 0.85), w_before.animate.shift(DOWN * 0.85), a_after.animate.shift(DOWN * 0.85), run_time=1.1)
        self.wait(2.7)

        key = self.formula_card(
            r"\boxed{\text{Caida\ libre\ ideal:}\ \sum\vec F=\vec W}",
            9.2, 1.05, 34, PALE_BLUE,
        )
        key.to_edge(DOWN, buff=0.24).shift(RIGHT * 1.4)
        self.play(FadeIn(key))
        self.wait(2.0)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 2. Toss: v changes sign, a does not
    # -------------------------------------------------------------------------
    def scene_upward_toss(self):
        self.section(
            2,
            "SUBIR, DETENERSE Y BAJAR: LA ACELERACIÓN NO CAMBIA DE SIGNO",
            "Después de abandonar la mano, una pelota lanzada hacia arriba también está en caída libre ideal.",
        )

        x = -4.1
        bottom = -2.25
        top = 2.05
        path = DashedLine(
            np.array([x, bottom, 0]),
            np.array([x, top, 0]),
            dash_length=0.13, color=LIGHT,
        )
        ball = self.ball(np.array([x, -1.72, 0]), 0.28, BLUE)
        self.play(Create(path), FadeIn(ball))

        # Constant acceleration indicator
        accel = self.vector(
            np.array([x + 1.0, 1.65, 0]),
            DOWN * 1.45,
            r"\vec a=-g\,\hat y",
            ORANGE,
        )
        constant_tag = self.txt("CONSTANTE", 19, BOLD, ORANGE).next_to(accel, UP, buff=0.05)
        self.play(FadeIn(accel), FadeIn(constant_tag))

        phase_panel = self.card(
            "VELOCIDAD",
            [
                "Subiendo: v > 0",
                "Cima: v = 0 solo un instante",
                "Bajando: v < 0",
                "En las tres etapas: a = −g",
            ],
            width=6.2, fill=PAPER, accent=BLUE,
        ).move_to(RIGHT * 3.55 + DOWN * 0.10)
        self.play(FadeIn(phase_panel))

        v_up = self.vector(
            ball.get_center() + LEFT * 0.62,
            UP * 1.60,
            r"\vec v",
            BLUE,
            LEFT,
        )
        self.play(FadeIn(v_up))
        self.play(ball.animate.move_to([x, 0.05, 0]), v_up.animate.scale(0.62).shift(UP * 1.77), run_time=1.0)

        v_mid = self.vector(
            np.array([x - 0.62, 0.15, 0]),
            UP * 0.60,
            r"\vec v",
            BLUE,
            LEFT,
        )
        self.play(Transform(v_up, v_mid), ball.animate.move_to([x, 1.45, 0]), run_time=0.9)

        apex = self.txt("v = 0", 31, BOLD, BLUE).move_to([x - 1.05, 1.65, 0])
        self.play(FadeOut(v_up), FadeIn(apex, scale=1.15), run_time=0.55)
        self.wait(1.2)

        v_down = self.vector(
            np.array([x - 0.62, 0.95, 0]),
            DOWN * 0.90,
            r"\vec v",
            BLUE,
            LEFT,
        )
        self.play(FadeIn(v_down), FadeOut(apex), ball.animate.move_to([x, 0.95, 0]))
        self.play(ball.animate.move_to([x, -1.20, 0]), v_down.animate.scale(1.55).shift(DOWN * 2.15), run_time=1.1)

        law = self.formula_card(
            r"v(t)=v_0-gt\qquad a(t)=-g",
            6.6, 1.08, 40, PALE_BLUE,
        ).move_to(RIGHT * 3.55 + DOWN * 2.55)
        self.play(FadeIn(law))
        self.wait(2.8)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 3. Mass independence
    # -------------------------------------------------------------------------
    def scene_mass_independence(self):
        self.section(
            3,
            "DOS MASAS DIFERENTES, LA MISMA ACELERACIÓN EN VACÍO",
            "El objeto más pesado tiene mayor W, pero también mayor inercia; la masa se cancela en F = ma.",
        )

        x1, x2 = -4.7, -1.7
        y_top, y_bottom = 1.95, -2.10

        rail1 = DashedLine([x1, y_top, 0], [x1, y_bottom, 0], color=LIGHT)
        rail2 = DashedLine([x2, y_top, 0], [x2, y_bottom, 0], color=LIGHT)
        b1 = self.block(np.array([x1, y_top, 0]), "1 kg", 0.92, CYAN)
        b5 = self.block(np.array([x2, y_top, 0]), "5 kg", 1.08, PURPLE)
        self.play(Create(rail1), Create(rail2), FadeIn(b1), FadeIn(b5))

        f1 = self.vector(b1.get_center() + RIGHT * 0.72, DOWN * 0.85, r"W_1=m_1g", RED)
        f5 = self.vector(b5.get_center() + RIGHT * 0.80, DOWN * 1.45, r"W_5=m_5g", RED)
        self.play(FadeIn(f1), FadeIn(f5))
        self.wait(1.4)

        deriv = VGroup(
            self.formula_card(r"m_1 a_1=m_1g\Rightarrow a_1=g", 5.8, 1.02, 35, PALE_BLUE),
            self.formula_card(r"m_5 a_5=m_5g\Rightarrow a_5=g", 5.8, 1.02, 35, PALE_PURPLE),
            self.formula_card(r"\boxed{a_1=a_5=g}", 5.8, 1.02, 39, PALE_GREEN),
        ).arrange(DOWN, buff=0.20).move_to(RIGHT * 3.65 + UP * 0.25)
        self.play(FadeIn(deriv[0]))
        self.play(FadeIn(deriv[1]))
        self.play(FadeIn(deriv[2]))
        self.wait(1.2)

        # Stroboscopic equal-time positions
        dots = VGroup()
        for frac in [0.22, 0.48, 0.78]:
            y = y_top - (y_top - y_bottom) * (frac ** 2)
            dots.add(
                Dot([x1, y, 0], radius=0.07, color=CYAN),
                Dot([x2, y, 0], radius=0.07, color=PURPLE),
            )
        self.play(FadeIn(dots, lag_ratio=0.08), run_time=0.65)

        self.play(
            b1.animate.move_to([x1, y_bottom, 0]),
            b5.animate.move_to([x2, y_bottom, 0]),
            f1.animate.shift(DOWN * (y_top - y_bottom)),
            f5.animate.shift(DOWN * (y_top - y_bottom)),
            run_time=2.0,
            rate_func=rate_functions.ease_in_quad,
        )

        same = self.txt("MISMO TIEMPO DE CAÍDA", 26, BOLD, GREEN)
        same.move_to(LEFT * 3.2 + DOWN * 2.70)
        self.play(FadeIn(same))
        self.wait(2.5)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 4. Scale / apparent weight as a continuous sequence
    # -------------------------------------------------------------------------
    def scene_scale_sequence(self):
        self.section(
            4,
            "LA BÁSCULA NO MIDE W: MIDE LA FUERZA NORMAL N",
            "Aquí llamamos peso gravitatorio W = mg y peso aparente a la lectura de la báscula, proporcional a N.",
        )

        cab = self.cabin(LEFT * 3.4, width=5.2, height=5.4)
        scale = self.scale_pad(LEFT * 3.4 + DOWN * 1.72, 1.65)
        person = self.person(LEFT * 3.4 + DOWN * 0.62, 1.15)

        w = self.vector(
            LEFT * 2.65 + UP * 0.10,
            DOWN * 1.35,
            r"W=mg",
            RED,
        )
        n = self.vector(
            LEFT * 4.15 + DOWN * 1.15,
            UP * 1.35,
            r"N",
            GREEN,
            LEFT,
        )

        self.play(FadeIn(cab), FadeIn(scale), FadeIn(person), FadeIn(w), FadeIn(n))

        state_title = self.txt("1 · REPOSO / VELOCIDAD CONSTANTE", 27, BOLD, INK).move_to(RIGHT * 3.55 + UP * 1.95)
        state_eq = self.formula_card(r"N-mg=0\Rightarrow N=mg", 6.1, 1.10, 38, PALE_GREEN).move_to(RIGHT * 3.55 + UP * 0.85)
        read = self.card(
            "LECTURA PARA m = 60 kg",
            [f"N = {N_STATIC:.1f} N"],
            5.1, 1.35, fill=PALE_GREEN, accent=GREEN,
            title_size=23, body_size=27,
        ).move_to(RIGHT * 3.55 + DOWN * 0.55)

        self.play(FadeIn(state_title), FadeIn(state_eq), FadeIn(read))
        self.wait(1.8)

        # Upward acceleration
        new_title = self.txt("2 · ACELERACIÓN HACIA ARRIBA", 27, BOLD, INK).move_to(state_title)
        new_eq = self.formula_card(r"N-mg=ma\Rightarrow N=m(g+a)", 6.1, 1.10, 36, PALE_GREEN).move_to(state_eq)
        new_read = self.card(
            "LA BÁSCULA MARCA MÁS",
            [f"N = {N_UP:.1f} N"],
            5.1, 1.35, fill=PALE_GREEN, accent=GREEN,
            title_size=23, body_size=27,
        ).move_to(read)
        n_up = self.vector(
            LEFT * 4.15 + DOWN * 1.15,
            UP * 1.78,
            r"N",
            GREEN,
            LEFT,
        )
        accel_up = self.vector(
            LEFT * 1.35 + DOWN * 0.20,
            UP * 1.30,
            r"\vec a",
            ORANGE,
        )

        self.play(
            Transform(state_title, new_title),
            Transform(state_eq, new_eq),
            Transform(read, new_read),
            Transform(n, n_up),
            FadeIn(accel_up),
            cab.animate.shift(UP * 0.20),
            scale.animate.shift(UP * 0.20),
            person.animate.shift(UP * 0.20),
            w.animate.shift(UP * 0.20),
            run_time=0.9,
        )
        self.wait(1.7)

        # Downward acceleration
        title_down = self.txt("3 · ACELERACIÓN HACIA ABAJO", 27, BOLD, INK).move_to(state_title)
        eq_down = self.formula_card(r"N-mg=-ma\Rightarrow N=m(g-a)", 6.1, 1.10, 36, PALE_ORANGE).move_to(state_eq)
        read_down = self.card(
            "LA BÁSCULA MARCA MENOS",
            [f"N = {N_DOWN:.1f} N"],
            5.1, 1.35, fill=PALE_ORANGE, accent=ORANGE,
            title_size=23, body_size=27,
        ).move_to(read)
        n_down = self.vector(
            LEFT * 4.15 + DOWN * 0.95,
            UP * 0.94,
            r"N",
            GREEN,
            LEFT,
        )
        accel_down = self.vector(
            LEFT * 1.35 + UP * 0.70,
            DOWN * 1.30,
            r"\vec a",
            ORANGE,
        )
        self.play(
            Transform(state_title, title_down),
            Transform(state_eq, eq_down),
            Transform(read, read_down),
            Transform(n, n_down),
            Transform(accel_up, accel_down),
            run_time=0.9,
        )
        self.wait(1.7)

        # Free fall
        title_free = self.txt("4 · CAÍDA LIBRE DEL SISTEMA", 27, BOLD, BLUE).move_to(state_title)
        eq_free = self.formula_card(r"N-mg=-mg\Rightarrow \boxed{N=0}", 6.1, 1.10, 39, PALE_PURPLE).move_to(state_eq)
        read_free = self.card(
            "PESO APARENTE CERO",
            ["La báscula deja de comprimirse."],
            5.1, 1.35, fill=PALE_PURPLE, accent=PURPLE,
            title_size=23, body_size=23,
        ).move_to(read)
        a_free = self.vector(
            LEFT * 1.35 + UP * 0.80,
            DOWN * 1.55,
            r"\vec a=\vec g",
            ORANGE,
        )
        self.play(
            Transform(state_title, title_free),
            Transform(state_eq, eq_free),
            Transform(read, read_free),
            FadeOut(n),
            Transform(accel_up, a_free),
            person.animate.shift(UP * 0.48),
            scale.animate.shift(DOWN * 0.13),
            run_time=1.0,
        )
        self.wait(2.3)

        punch = self.txt("N = 0  ≠  W = 0", 34, BOLD, PURPLE).move_to(RIGHT * 3.55 + DOWN * 2.12)
        self.play(FadeIn(punch, scale=1.15))
        self.wait(2.2)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 5. Weightlessness: local free-fall lab + orbit
    # -------------------------------------------------------------------------
    def scene_weightlessness_lab_and_orbit(self):
        self.section(
            5,
            "INGRAVIDEZ APARENTE = CAER JUNTOS",
            "Persona, báscula, objetos y nave comparten casi la misma aceleración gravitatoria; por eso no se comprimen entre sí.",
        )

        # LEFT: freely falling lab
        cab = self.cabin(LEFT * 3.7, width=5.6, height=5.2)
        p = self.person(LEFT * 4.25 + UP * 0.15, 1.05)
        loose = self.ball(LEFT * 2.80 + UP * 0.95, 0.24, BLUE)
        coin = Dot(LEFT * 3.05 + DOWN * 0.55, radius=0.12, color=ORANGE)
        self.play(FadeIn(cab), FadeIn(p), FadeIn(loose), FadeIn(coin))

        common = VGroup(
            self.vector(LEFT * 4.85 + UP * 1.55, DOWN * 1.10, r"\vec g", ORANGE, LEFT, label_size=25),
            self.vector(LEFT * 3.35 + UP * 1.55, DOWN * 1.10, r"\vec g", ORANGE, LEFT, label_size=25),
            self.vector(LEFT * 2.25 + UP * 1.55, DOWN * 1.10, r"\vec g", ORANGE, RIGHT, label_size=25),
        )
        self.play(FadeIn(common))
        self.wait(1.2)

        lab_note = self.card(
            "VISTO DESDE DENTRO",
            [
                "Todos caen casi igual.",
                "No hay apoyo sostenido: N ≈ 0.",
                "Separación relativa ≈ constante.",
            ],
            5.3, fill=PALE_PURPLE, accent=PURPLE,
        ).move_to(LEFT * 3.7 + DOWN * 2.35)
        self.play(FadeIn(lab_note))
        self.play(
            p.animate.shift(UP * 0.30),
            loose.animate.shift(DOWN * 0.12),
            coin.animate.shift(UP * 0.18),
            run_time=1.0,
        )
        self.wait(1.7)

        # RIGHT: orbit
        e = self.earth(RIGHT * 3.80 + DOWN * 0.35, 1.62)
        sat = RoundedRectangle(
            width=0.58, height=0.34, corner_radius=0.06,
            stroke_color=PURPLE, stroke_width=2.6,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 3.80 + UP * 2.15)
        orbit = Circle(
            radius=2.50, stroke_color=LIGHT, stroke_width=2,
        ).move_to(RIGHT * 3.80 + DOWN * 0.35)
        vtan = self.vector(
            sat.get_center() + RIGHT * 0.10,
            RIGHT * 1.35,
            r"\vec v_{\mathrm{orb}}",
            BLUE,
            UP,
            label_size=24,
        )
        gvec = self.vector(
            sat.get_center() + LEFT * 0.30,
            DOWN * 1.20,
            r"\vec g",
            ORANGE,
            LEFT,
            label_size=24,
        )
        self.play(FadeIn(e), Create(orbit), FadeIn(sat), FadeIn(vtan), FadeIn(gvec))

        orbit_note = self.card(
            "A 400 km DE ALTURA",
            [
                f"g ≈ {G_ORBIT:.2f} m/s²",
                f"≈ {100*G_ORBIT/G:.1f}% de g en superficie",
                "La órbita es caída libre continua.",
            ],
            5.25, fill=PALE_BLUE, accent=BLUE,
        ).move_to(RIGHT * 3.80 + DOWN * 2.35)
        self.play(FadeIn(orbit_note))
        self.wait(2.7)

        nuance = self.txt(
            "Matiz senior: localmente “flotan”; a gran escala permanecen gradientes de gravedad (efectos de marea).",
            21, BOLD, MID,
        )
        self.fit(nuance, 14.2, 0.56)
        nuance.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(nuance))
        self.wait(2.4)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 6. Newton -> kinematics
    # -------------------------------------------------------------------------
    def scene_newton_to_kinematics(self):
        self.section(
            6,
            "DE NEWTON A LAS ECUACIONES DE CAÍDA LIBRE",
            "No memorizamos una fórmula aislada: primero obtenemos a = −g y después conectamos aceleración, velocidad y posición.",
        )

        left = VGroup(
            self.formula_card(r"\sum F_y=-mg=ma_y", 5.6, 1.05, 38, PALE_RED),
            self.formula_card(r"\boxed{a_y=-g}", 5.6, 1.05, 42, PALE_ORANGE),
        ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.65 + UP * 0.65)

        axis = Arrow(
            LEFT * 6.25 + DOWN * 2.10,
            LEFT * 6.25 + UP * 2.05,
            buff=0, color=INK, stroke_width=4,
        )
        axis_lab = self.txt("+y", 22, BOLD, INK).next_to(axis, UP, buff=0.04)
        grav = self.vector(LEFT * 5.05 + UP * 1.40, DOWN * 1.35, r"\vec g", ORANGE)

        self.play(GrowArrow(axis), FadeIn(axis_lab), FadeIn(grav))
        self.play(FadeIn(left[0]))
        self.play(TransformFromCopy(left[0], left[1]))
        self.wait(1.4)

        arrows = VGroup(
            Arrow(LEFT * 0.4 + UP * 1.50, RIGHT * 1.15 + UP * 1.50, color=MID, stroke_width=3),
            Arrow(RIGHT * 3.0 + UP * 1.50, RIGHT * 4.15 + UP * 1.50, color=MID, stroke_width=3),
        )
        boxes = VGroup(
            self.card("ACELERACIÓN", ["constante: −g"], 2.75, 1.5, fill=PALE_ORANGE, accent=ORANGE),
            self.card("VELOCIDAD", ["cambia linealmente"], 2.75, 1.5, fill=PALE_BLUE, accent=BLUE),
            self.card("POSICIÓN", ["cambia parabólicamente"], 2.75, 1.5, fill=PALE_PURPLE, accent=PURPLE),
        ).arrange(RIGHT, buff=0.75).move_to(RIGHT * 2.30 + UP * 1.50)

        self.play(FadeIn(boxes[0]))
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]))
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]))
        self.wait(1.2)

        equations = VGroup(
            self.formula_card(r"v(t)=v_0-gt", 4.8, 1.02, 40, PALE_BLUE),
            self.formula_card(r"y(t)=y_0+v_0t-\frac12gt^2", 6.2, 1.02, 36, PALE_PURPLE),
            self.formula_card(r"v^2=v_0^2-2g(y-y_0)", 5.8, 1.02, 36, PALE_GREEN),
        ).arrange(DOWN, buff=0.20).move_to(RIGHT * 3.20 + DOWN * 1.05)
        for eq in equations:
            self.play(FadeIn(eq, shift=UP * 0.08), run_time=0.45)
            self.wait(0.55)

        self.wait(2.0)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 7. 20m stroboscopic fall
    # -------------------------------------------------------------------------
    def scene_twenty_meter_strobe(self):
        self.section(
            7,
            "CAÍDA DESDE 20 m: OBSERVA CÓMO CRECE LA DISTANCIA RECORRIDA",
            "En intervalos iguales de tiempo, las posiciones se separan cada vez más porque la rapidez aumenta.",
        )

        x = -4.65
        y_ground = -2.35
        y_top = 2.15

        wall = Line([x - 0.95, y_ground, 0], [x - 0.95, y_top + 0.30, 0], color=INK, stroke_width=4)
        ground = Line([x - 1.45, y_ground, 0], [x + 1.30, y_ground, 0], color=INK, stroke_width=3)
        self.play(Create(wall), Create(ground))

        marks = VGroup()
        for h in [0, 5, 10, 15, 20]:
            yy = y_ground + (h / 20.0) * (y_top - y_ground)
            tick = Line([x - 1.12, yy, 0], [x - 0.82, yy, 0], color=INK, stroke_width=2)
            lab = self.txt(f"{h} m", 19, color=MID).next_to(tick, LEFT, buff=0.08)
            marks.add(tick, lab)
        self.play(FadeIn(marks))

        times = [0.0, 0.5, 1.0, 1.5, 2.0]
        strobe = VGroup()
        time_labels = VGroup()
        for t in times:
            y_m = max(0.0, H - 0.5 * G * t**2)
            yy = y_ground + (y_m / H) * (y_top - y_ground)
            b = self.ball(np.array([x, yy, 0]), 0.18, BLUE)
            tl = self.txt(f"{t:.1f} s", 18, BOLD, BLUE).next_to(b, RIGHT, buff=0.12)
            strobe.add(b)
            time_labels.add(tl)

        self.play(FadeIn(strobe[0]), FadeIn(time_labels[0]))
        for i in range(1, len(strobe)):
            self.play(
                FadeIn(strobe[i], scale=0.75),
                FadeIn(time_labels[i]),
                run_time=0.45,
            )
            self.wait(0.22)

        deriv = VGroup(
            self.formula_card(r"y(t)=20-\frac12(9.81)t^2", 6.3, 1.05, 36, PALE_PURPLE),
            self.formula_card(
                r"0=20-\frac12gt^2\Rightarrow t_{\rm hit}\approx 2.02\,s",
                6.3, 1.05, 32, PALE_BLUE,
            ),
            self.formula_card(
                r"|v_{\rm hit}|=gt_{\rm hit}\approx 19.81\,m/s",
                6.3, 1.05, 33, PALE_GREEN,
            ),
        ).arrange(DOWN, buff=0.23).move_to(RIGHT * 3.60 + UP * 0.35)
        for eq in deriv:
            self.play(FadeIn(eq), run_time=0.50)

        intervals = self.card(
            "IGUALES Δt, DISTANCIAS CRECIENTES",
            [
                "0 → 0.5 s: poco desplazamiento",
                "1.5 → 2.0 s: mucho más desplazamiento",
                "La pendiente de y(t) se hace más negativa.",
            ],
            6.3, fill=PALE_ORANGE, accent=ORANGE,
        ).move_to(RIGHT * 3.60 + DOWN * 2.05)
        self.play(FadeIn(intervals))
        self.wait(3.0)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 8. Synchronized motion + graphs
    # -------------------------------------------------------------------------
    def scene_motion_graph_sync(self):
        self.section(
            8,
            "MOVIMIENTO Y GRÁFICAS SINCRONIZADOS",
            "El mismo instante t determina simultáneamente la altura, la velocidad y la aceleración.",
        )

        tracker = ValueTracker(0.0)
        tmax = T_HIT

        # Physical fall at left
        x = -5.55
        y0 = 1.95
        yg = -2.25
        rail = Line([x, yg, 0], [x, y0, 0], color=LIGHT, stroke_width=3)
        ground = Line([x - 0.75, yg, 0], [x + 0.75, yg, 0], color=INK, stroke_width=3)
        self.play(Create(rail), Create(ground))

        moving_ball = always_redraw(
            lambda: self.ball(
                np.array([
                    x,
                    yg + max(0.0, H - 0.5 * G * min(tracker.get_value(), tmax)**2) / H * (y0 - yg),
                    0,
                ]),
                0.22, BLUE,
            )
        )
        vel_vec = always_redraw(
            lambda: Arrow(
                np.array([x + 0.55, moving_ball.get_center()[1] + 0.10, 0]),
                np.array([
                    x + 0.55,
                    moving_ball.get_center()[1] + 0.10 - min(1.45, 0.075 * G * tracker.get_value()),
                    0,
                ]),
                buff=0, color=BLUE, stroke_width=5,
                max_tip_length_to_length_ratio=0.20,
            )
        )
        self.add(moving_ball, vel_vec)

        # Graphs
        ax_y = Axes(
            x_range=[0, tmax, 0.5], y_range=[0, 20, 5],
            x_length=4.0, y_length=2.25,
            axis_config={"color": INK, "stroke_width": 1.8, "include_tip": False},
        ).move_to(LEFT * 1.65 + UP * 0.45)
        ax_v = Axes(
            x_range=[0, tmax, 0.5], y_range=[-20, 0, 5],
            x_length=4.0, y_length=2.25,
            axis_config={"color": INK, "stroke_width": 1.8, "include_tip": False},
        ).move_to(RIGHT * 2.65 + UP * 0.45)
        ax_a = Axes(
            x_range=[0, tmax, 0.5], y_range=[-12, 0, 3],
            x_length=4.0, y_length=2.25,
            axis_config={"color": INK, "stroke_width": 1.8, "include_tip": False},
        ).move_to(RIGHT * 2.65 + DOWN * 2.00)

        lab_y = self.txt("y(t)", 22, BOLD, PURPLE).next_to(ax_y, UP, buff=0.08)
        lab_v = self.txt("v(t)", 22, BOLD, BLUE).next_to(ax_v, UP, buff=0.08)
        lab_a = self.txt("a(t)", 22, BOLD, ORANGE).next_to(ax_a, UP, buff=0.08)

        curve_y = ax_y.plot(
            lambda t: H - 0.5 * G * t**2,
            x_range=[0, tmax],
            color=PURPLE, stroke_width=3.5,
        )
        curve_v = ax_v.plot(
            lambda t: -G * t,
            x_range=[0, tmax],
            color=BLUE, stroke_width=3.5,
        )
        curve_a = ax_a.plot(
            lambda t: -G,
            x_range=[0, tmax],
            color=ORANGE, stroke_width=3.5,
        )

        self.play(FadeIn(ax_y), FadeIn(ax_v), FadeIn(ax_a), FadeIn(lab_y), FadeIn(lab_v), FadeIn(lab_a))
        self.play(Create(curve_y), Create(curve_v), Create(curve_a), run_time=1.2)

        dot_y = always_redraw(
            lambda: Dot(
                ax_y.c2p(
                    min(tracker.get_value(), tmax),
                    max(0.0, H - 0.5 * G * min(tracker.get_value(), tmax)**2),
                ),
                radius=0.07, color=PURPLE,
            )
        )
        dot_v = always_redraw(
            lambda: Dot(
                ax_v.c2p(
                    min(tracker.get_value(), tmax),
                    -G * min(tracker.get_value(), tmax),
                ),
                radius=0.07, color=BLUE,
            )
        )
        dot_a = always_redraw(
            lambda: Dot(
                ax_a.c2p(min(tracker.get_value(), tmax), -G),
                radius=0.07, color=ORANGE,
            )
        )
        self.add(dot_y, dot_v, dot_a)

        time_num = DecimalNumber(
            0, num_decimal_places=2,
            font_size=34, color=INK,
        )
        time_num.add_updater(lambda d: d.set_value(tracker.get_value()))
        time_row = VGroup(
            self.txt("t =", 25, BOLD, INK),
            time_num,
            self.txt("s", 25, color=INK),
        ).arrange(RIGHT, buff=0.08).move_to(LEFT * 5.55 + DOWN * 2.80)
        self.add(time_row)

        self.play(tracker.animate.set_value(tmax), run_time=4.6, rate_func=linear)
        time_num.clear_updaters()
        self.wait(1.0)

        relation = self.txt(
            "La curva y(t), la recta v(t) y la línea a(t) describen el mismo movimiento.",
            23, BOLD, MID,
        )
        self.fit(relation, 13.8, 0.58)
        relation.to_edge(DOWN, buff=0.10)
        self.play(FadeIn(relation))
        self.wait(2.5)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 9. Air drag / terminal velocity
    # -------------------------------------------------------------------------
    def scene_air_drag(self):
        self.section(
            9,
            "CAÍDA REAL EN AIRE: YA NO ACTÚA SOLO W",
            "La resistencia del aire crece con la rapidez; por eso la aceleración puede disminuir hasta aproximarse a cero.",
        )

        obj = self.ball(LEFT * 3.65 + UP * 0.55, 0.34, BLUE)
        w = self.vector(
            LEFT * 2.90 + UP * 0.70,
            DOWN * 1.85,
            r"W=mg",
            RED,
        )
        drag_small = self.vector(
            LEFT * 4.40 + DOWN * 0.05,
            UP * 0.65,
            r"D",
            CYAN,
            LEFT,
        )

        wind = VGroup(*[
            Line(
                LEFT * 5.7 + DOWN * 1.7 + UP * i * 0.45,
                LEFT * 1.7 + DOWN * 1.7 + UP * i * 0.45,
                color=LIGHT, stroke_width=2,
            )
            for i in range(8)
        ])

        self.play(FadeIn(wind), FadeIn(obj), FadeIn(w), FadeIn(drag_small))

        stages = VGroup(
            self.card("AL PRINCIPIO", ["v pequeña", "D pequeña", "a ≈ g"], 3.3, 2.2, fill=PALE_BLUE, accent=BLUE),
            self.card("MÁS RÁPIDO", ["D aumenta", "F_net disminuye", "|a| disminuye"], 3.3, 2.2, fill=PALE_ORANGE, accent=ORANGE),
            self.card("LÍMITE", ["D ≈ mg", "F_net ≈ 0", "v ≈ v_terminal"], 3.3, 2.2, fill=PALE_GREEN, accent=GREEN),
        ).arrange(RIGHT, buff=0.22).move_to(RIGHT * 2.85 + DOWN * 0.20)

        self.play(FadeIn(stages[0]))
        self.wait(1.0)

        drag_mid = self.vector(
            LEFT * 4.40 + DOWN * 0.15,
            UP * 1.12,
            r"D",
            CYAN,
            LEFT,
        )
        self.play(
            Transform(drag_small, drag_mid),
            obj.animate.shift(DOWN * 0.55),
            FadeIn(stages[1]),
            run_time=0.8,
        )
        self.wait(1.0)

        drag_equal = self.vector(
            LEFT * 4.40 + DOWN * 0.72,
            UP * 1.82,
            r"D\approx mg",
            CYAN,
            LEFT,
        )
        self.play(
            Transform(drag_small, drag_equal),
            obj.animate.shift(DOWN * 0.75),
            FadeIn(stages[2]),
            run_time=0.8,
        )

        eq = self.formula_card(
            r"mg-D=ma\qquad D\rightarrow mg\Rightarrow a\rightarrow 0",
            8.2, 1.05, 35, PALE_ORANGE,
        ).to_edge(DOWN, buff=0.30).shift(RIGHT * 1.6)
        self.play(FadeIn(eq))
        self.wait(2.7)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # 10. Senior misconception QA
    # -------------------------------------------------------------------------
    def scene_misconception_qa(self):
        self.section(
            10,
            "SENIOR QA: CINCO AFIRMACIONES QUE DEBEN QUEDAR RESUELTAS",
            "No basta con recordar fórmulas; cada respuesta debe poder justificarse con fuerzas, signos o definiciones.",
        )

        items = [
            ("“En la cima, a = 0.”", "FALSO", "v = 0, pero a = −g mientras actúe la gravedad.", RED),
            ("“Ingravidez significa g = 0.”", "FALSO", "En caída libre N ≈ 0, aunque W = mg siga actuando.", RED),
            ("“Más masa implica mayor a en vacío.”", "FALSO", "mg = ma ⇒ a = g; la masa se cancela.", RED),
            ("“La báscula mide directamente W.”", "FALSO", "La báscula responde a la fuerza normal N.", RED),
            ("“Con aire, a siempre vale exactamente g.”", "FALSO", "El arrastre añade otra fuerza y modifica a.", RED),
        ]

        y_positions = [1.75, 0.75, -0.25, -1.25, -2.25]
        cards = []
        for i, ((claim, verdict, why, color), y) in enumerate(zip(items, y_positions), start=1):
            num = RoundedRectangle(
                width=0.62, height=0.62, corner_radius=0.12,
                fill_color=INK, fill_opacity=1, stroke_width=0,
            ).move_to(LEFT * 6.45 + UP * y)
            num_t = self.txt(str(i), 20, BOLD, WHITE).move_to(num)
            claim_t = self.txt(claim, 24, BOLD, INK).move_to(LEFT * 3.65 + UP * y)
            verdict_t = self.txt(verdict, 22, BOLD, color).move_to(RIGHT * 0.65 + UP * y)
            why_t = self.txt(why, 21, color=MID)
            self.fit(why_t, 6.3, 0.48)
            why_t.move_to(RIGHT * 4.30 + UP * y)
            cards.append(VGroup(num, num_t, claim_t, verdict_t, why_t))

        for c in cards:
            self.play(FadeIn(c, shift=RIGHT * 0.12), run_time=0.42)
            self.wait(0.38)

        final = self.formula_card(
            r"\boxed{W=mg\quad\text{mientras}\quad N\ \text{depende del apoyo}}",
            9.0, 1.05, 34, PALE_PURPLE,
        ).to_edge(DOWN, buff=0.10)
        self.play(FadeIn(final))
        self.wait(3.0)
        self.stage_clear()

    # -------------------------------------------------------------------------
    # Closing
    # -------------------------------------------------------------------------
    def closing_map(self):
        title = self.txt("MAPA MENTAL FINAL", 39, BOLD, INK)

        cards = VGroup(
            self.card("1 · FUERZAS", ["¿Qué fuerzas reales actúan?"], 2.55, 1.55, fill=PALE_RED, accent=RED, title_size=22, body_size=19),
            self.card("2 · APOYO", ["¿Existe N, tensión o contacto?"], 2.55, 1.55, fill=PALE_GREEN, accent=GREEN, title_size=22, body_size=19),
            self.card("3 · NEWTON", ["ΣF = ma determina a."], 2.55, 1.55, fill=PALE_ORANGE, accent=ORANGE, title_size=22, body_size=19),
            self.card("4 · CINEMÁTICA", ["a → v(t) → y(t)"], 2.55, 1.55, fill=PALE_BLUE, accent=BLUE, title_size=22, body_size=19),
            self.card("5 · INTERPRETA", ["Peso real ≠ peso aparente."], 2.55, 1.55, fill=PALE_PURPLE, accent=PURPLE, title_size=22, body_size=19),
        ).arrange(RIGHT, buff=0.20)

        take = self.txt(
            "INGRAVIDEZ APARENTE: NO DESAPARECE LA GRAVEDAD; DESAPARECE EL APOYO.",
            31, BOLD, PURPLE,
        )
        self.fit(take, 14.0, 0.80)

        sub = self.txt(
            "En caída libre ideal, W = mg sigue presente y N → 0.",
            27, BOLD, INK,
        )

        group = VGroup(title, cards, take, sub).arrange(DOWN, buff=0.48)
        self.fit(group, 14.7, 6.8)
        self.play(FadeIn(title, shift=UP * 0.15))
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.15),
            run_time=1.7,
        )
        self.wait(1.1)
        self.play(FadeIn(take, scale=1.05))
        self.play(FadeIn(sub))
        self.wait(4.0)
        self.stage_clear()
