#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Movimiento vertical y caída libre
V4 TYPOGRAPHY SAFE LAYOUT

Purpose
-------
Rebuild the theory lesson using the user's consolidated JP Classroom format, with a hard projector-safe typography and margin contract:
- white / monochrome classroom visual system;
- persistent numbered header + concise subtitle;
- explicit step-by-step reasoning;
- controlled pauses for reading, explanation and student work;
- fluid continuous motion inside each section;
- equations, geometry, graphs and experiment logic kept spatially integrated;
- MovingCameraScene focus only when it strengthens the causal explanation;
- all displayed numerical claims validated before rendering;\n- teaching text uses explicit size floors and wrapped blocks;\n- no teaching-critical text may cross the JP safe margins;\n- dynamic updater families are frozen before section exits.

Target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from manim import *

from library.jp_classroom_style import *


# =============================================================================
# PHYSICS DATA
# =============================================================================
G = 9.81
V0_UP = 14.0
T_APEX = V0_UP / G
H_APEX = V0_UP**2 / (2 * G)
T_RETURN = 2 * T_APEX

DROP_H = 20.0
T_DROP = math.sqrt(2 * DROP_H / G)
V_IMPACT = G * T_DROP

# Classroom-scale theoretical prediction: maximum fall distance < 0.8 m.
LAB_TIMES = np.array([0.10, 0.20, 0.30, 0.40], dtype=float)
LAB_T2 = LAB_TIMES**2
LAB_D = 0.5 * G * LAB_T2


@dataclass
class MotionState:
    t: float
    y: float
    v: float
    a: float


class Physics9VerticalFreeFallTheoryV4TypographySafe(JPMathClassroomScene):
    """Fluid, paused and explicitly sequenced theory lesson."""

    # =========================================================================
    # VALIDATION
    # =========================================================================
    def validate_lesson_data(self) -> None:
        assert_close(V0_UP - G * T_APEX, 0.0, label="apex velocity")
        assert_close(
            H_APEX,
            V0_UP * T_APEX - 0.5 * G * T_APEX**2,
            label="apex height",
        )
        assert_close(0.5 * G * T_DROP**2, DROP_H, label="20 m drop distance")
        assert_close(V_IMPACT, math.sqrt(2 * G * DROP_H), label="impact speed")
        assert np.allclose(LAB_D / LAB_D[0], [1, 4, 9, 16])
        assert np.allclose(np.diff(np.array([0, 1, 4, 9, 16])), [1, 3, 5, 7])

    # =========================================================================
    # SMALL VISUAL HELPERS — all remain inside JP monochrome language
    # =========================================================================
    def ball(self, point, radius: float = 0.18, fill=VERY_LIGHT_GRAY) -> VGroup:
        outer = Circle(
            radius=radius,
            stroke_color=BLACK_LINE,
            stroke_width=2.1,
            fill_color=fill,
            fill_opacity=1.0,
        ).move_to(point)
        highlight = Dot(
            np.array(point) + UL * radius * 0.34,
            radius=radius * 0.13,
            color=WHITE_FILL,
        )
        return VGroup(outer, highlight)

    def ghost_ball(self, point, radius: float = 0.12) -> Circle:
        return Circle(
            radius=radius,
            stroke_color=MID_GRAY,
            stroke_width=1.25,
            fill_color=WHITE_FILL,
            fill_opacity=0.18,
        ).move_to(point)

    def vector_arrow(
        self,
        start,
        direction,
        label: str,
        *,
        stroke_width: float = 3.6,
        label_size: int = 24,
        label_side=RIGHT,
    ) -> VGroup:
        start = np.array(start, dtype=float)
        direction = np.array(direction, dtype=float)
        if np.linalg.norm(direction) < 1e-4:
            marker = self.math(label, label_size).move_to(start + RIGHT * 0.58)
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

    def vertical_axis(self, x: float, y0: float, y1: float, *, label: str = "+y") -> VGroup:
        axis = Arrow(
            [x, y0, 0],
            [x, y1, 0],
            buff=0,
            color=BLACK_LINE,
            stroke_width=2.5,
        )
        lab = self.math(label, 29).next_to(axis, UP, buff=0.08)
        return VGroup(axis, lab)

    def ground(self, y: float = -2.55, x0: float = -6.3, x1: float = 6.3) -> VGroup:
        line = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.2)
        hatch = VGroup(
            *[
                Line(
                    [x, y - 0.04, 0],
                    [x + 0.26, y - 0.22, 0],
                    color=LIGHT_GRAY,
                    stroke_width=1.2,
                )
                for x in np.arange(x0, x1, 0.5)
            ]
        )
        return VGroup(line, hatch)

    def phase_card(self, number: int, title: str, statement: str, width: float = 4.1) -> VGroup:
        badge = RoundedRectangle(
            width=0.62,
            height=0.48,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        )
        n = self.text(str(number), 23, BOLD).move_to(badge)
        text_width = width - 1.08
        title_m = self.text_block(
            title,
            26,
            BOLD,
            max_width=text_width,
            max_lines=1,
            min_size=25,
        )
        statement_m = self.text_block(
            statement,
            24,
            max_width=text_width,
            max_lines=2,
            min_size=23,
            line_buff=0.035,
        )
        text_group = VGroup(title_m, statement_m).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.08,
        )
        row = VGroup(VGroup(badge, n), text_group).arrange(RIGHT, buff=0.17)
        self.fit_or_fail(
            row,
            width - 0.32,
            1.30,
            min_scale=0.94,
            label=f"phase_card[{title}]",
        )
        box = RoundedRectangle(
            width=width,
            height=max(1.38, row.height + 0.28),
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.45,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.16)
        return VGroup(box, row)

    def live_state_panel(
        self,
        tracker: ValueTracker,
        state_fn,
        *,
        title: str,
        width=4.0,
        position=ORIGIN,
    ):
        def build():
            s = state_fn(tracker.get_value())
            rows = VGroup(
                self.text(f"t = {s.t:0.2f} s", 26, BOLD),
                self.text(f"y = {s.y:0.2f} m", 26),
                self.text(f"v = {s.v:+0.2f} m/s", 26),
                self.text(f"a = {s.a:+0.2f} m/s²", 26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
            ttl = self.text(title, 25, BOLD)
            content = VGroup(ttl, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            box = RoundedRectangle(
                width=width,
                height=2.70,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=1.6,
                fill_color=PAPER_GRAY,
                fill_opacity=1.0,
            )
            self.fit(content, width - 0.45, 2.30)
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.24)
            return VGroup(box, content).move_to(position)
        return always_redraw(build)

    def checkpoint_pause(self, card: Mobject, *, explain: float = PAUSE_EXPLAIN) -> None:
        self.play(FadeIn(card, shift=UP * 0.08), run_time=RUN_QUICK)
        self.wait(explain)
        self.play(FadeOut(card), run_time=RUN_QUICK)

    # =========================================================================
    # MASTER TIMELINE
    # =========================================================================
    def construct(self) -> None:
        self.standard_opening(
            "FÍSICA 9° · CLASE LABORATORIO",
            "MOVIMIENTO VERTICAL Y CAÍDA LIBRE",
            "De las fuerzas al modelo y del modelo a una predicción medible",
            "Cada ecuación aparecerá después del fenómeno que explica.",
        )
        self.scene_01_vertical_motion_vs_free_fall()
        self.scene_02_axis_signs_and_three_phases()
        self.scene_03_newton_to_gravity()
        self.scene_04_derive_velocity_and_position()
        self.scene_05_three_initial_conditions()
        self.scene_06_upward_throw_worked_motion()
        self.scene_07_motion_graphs_synchronized()
        self.scene_08_twenty_meter_drop_stepwise()
        self.scene_09_stroboscopic_square_law()
        self.scene_10_mass_independence_and_model_limit()
        self.scene_11_lab_prediction_table_and_linearization()
        self.scene_12_experimental_protocol_bridge()
        self.standard_closing(
            "Fuerzas → a = −g → v(t) → y(t) → d ∝ t² → medir, graficar y estimar g."
        )

    # =========================================================================
    # 01
    # =========================================================================
    def scene_01_vertical_motion_vs_free_fall(self) -> None:
        self.set_header(
            1,
            "TRAYECTORIA VERTICAL ≠ CAÍDA LIBRE",
            "Primero observamos la trayectoria; después inspeccionamos qué fuerzas permanecen actuando.",
        )

        divider = Line([0, -2.72, 0], [0, 2.08, 0], color=LIGHT_GRAY, stroke_width=1.6)

        # Supported vertical motion
        rail = Line([-4.2, -2.25, 0], [-4.2, 1.85, 0], color=LIGHT_GRAY, stroke_width=2)
        support = Square(
            0.70,
            stroke_color=BLACK_LINE,
            stroke_width=2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to([-4.2, -1.55, 0])
        normal = self.vector_arrow([-4.65, -1.42, 0], UP * 0.95, r"\vec N", label_side=LEFT)
        weight_left = self.vector_arrow([-3.76, -1.20, 0], DOWN * 0.95, r"m\vec g")
        left_title = self.text("VERTICAL TRAJECTORY", 26, BOLD).move_to([-4.2, 2.20, 0])

        # Free fall
        guide = DashedLine(
            [4.2, -2.25, 0],
            [4.2, 1.85, 0],
            dash_length=0.09,
            color=LIGHT_GRAY,
        )
        right_ball = self.ball([4.2, 1.55, 0], 0.20)
        weight_right = self.vector_arrow([4.68, 1.42, 0], DOWN * 1.02, r"m\vec g")
        right_title = self.text("IDEAL FREE FALL", 26, BOLD).move_to([4.2, 2.20, 0])

        step1 = self.phase_card(1, "ASK ABOUT THE PATH", "Both motions are vertical.", 4.2).move_to([-3.85, -3.18, 0])
        step2 = self.phase_card(2, "ASK ABOUT FORCES", "Only the right case has gravity as the relevant force.", 5.3).move_to([3.25, -3.18, 0])

        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), run_time=RUN_NORMAL)
        self.play(Create(rail), FadeIn(support), FadeIn(normal), FadeIn(weight_left), run_time=RUN_NORMAL)
        self.play(support.animate.shift(UP * 2.35), run_time=RUN_SLOW * 1.35, rate_func=there_and_back)
        self.checkpoint_pause(step1, explain=PAUSE_READ)

        self.play(Create(guide), FadeIn(right_ball), FadeIn(weight_right), run_time=RUN_NORMAL)
        self.play(
            right_ball.animate.move_to([4.2, -1.95, 0]),
            weight_right.animate.shift(DOWN * 3.50),
            run_time=RUN_SLOW * 1.65,
            rate_func=rate_functions.ease_in_quad,
        )
        self.checkpoint_pause(step2, explain=PAUSE_EXPLAIN)

        definition = self.formula_panel(
            r"\text{caída libre ideal:}\qquad \sum \vec F=m\vec g",
            width=7.7,
            height=1.05,
            font_size=36,
        )
        definition.move_to([0, -2.55, 0])
        self.assert_text_safe(definition, "scene01 definition")
        self.play(FadeIn(definition), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 02
    # =========================================================================
    def scene_02_axis_signs_and_three_phases(self) -> None:
        self.set_header(
            2,
            "EL SIGNO SE DEFINE ANTES DE CALCULAR",
            "Elegimos +y hacia arriba: la velocidad cambia de signo; la aceleración gravitacional no.",
        )

        axis = self.vertical_axis(-5.65, -2.50, 2.10)
        zero = Dot([-5.65, -0.35, 0], radius=0.065, color=BLACK_LINE)
        zero_label = self.text("0", 22).next_to(zero, LEFT, buff=0.08)

        tracker = ValueTracker(0.0)
        y_floor = -2.0
        y_peak = 1.70

        def y_scene(q):
            return y_floor + (y_peak - y_floor) * (4 * q * (1 - q))

        moving_ball = always_redraw(
            lambda: self.ball([-2.55, y_scene(tracker.get_value()), 0], 0.18)
        )

        def live_v():
            q = tracker.get_value()
            s = 1 - 2 * q
            y = y_scene(q)
            if abs(s) < 0.055:
                return self.math(r"v_y=0", 28).move_to([-1.43, y, 0])
            return self.vector_arrow(
                [-1.95, y, 0],
                UP * (1.10 * s),
                r"v_y",
                label_side=RIGHT,
            )

        velocity = always_redraw(live_v)
        acceleration = always_redraw(
            lambda: self.vector_arrow(
                [-3.15, y_scene(tracker.get_value()), 0],
                DOWN * 0.86,
                r"a_y=-g",
                label_side=LEFT,
            )
        )

        phase_box = self.note_panel(
            "THE THREE PHASES",
            [
                "1. Rising: v_y > 0, a_y < 0",
                "2. Highest point: v_y = 0, a_y < 0",
                "3. Falling: v_y < 0, a_y < 0",
            ],
            width=5.7,
            title_size=25,
            body_size=24,
        ).move_to([4.15, -0.10, 0])

        self.play(FadeIn(axis), FadeIn(zero), FadeIn(zero_label), FadeIn(phase_box), run_time=RUN_NORMAL)
        self.play(FadeIn(moving_ball), FadeIn(velocity), FadeIn(acceleration), run_time=RUN_QUICK)

        rise_card = self.phase_card(1, "RISING", "v_y > 0 but gravity points downward.", 4.7).move_to([3.8, 2.05, 0])
        apex_card = self.phase_card(2, "APEX", "v_y = 0 for one instant; a_y is still −g.", 4.9).move_to([3.7, 2.05, 0])
        fall_card = self.phase_card(3, "FALLING", "v_y < 0 and a_y remains −g.", 4.7).move_to([3.8, 2.05, 0])

        self.checkpoint_pause(rise_card, explain=PAUSE_READ)
        self.play(tracker.animate.set_value(0.5), run_time=RUN_SLOW * 1.55, rate_func=linear)
        self.checkpoint_pause(apex_card, explain=PAUSE_EXPLAIN)
        self.play(tracker.animate.set_value(1.0), run_time=RUN_SLOW * 1.55, rate_func=linear)
        self.checkpoint_pause(fall_card, explain=PAUSE_READ)

        constant = self.formula_panel(
            r"a_y=-g=-9.81\;\mathrm{m/s^2}\qquad\text{during all three phases}",
            width=8.9,
            height=1.05,
            font_size=33,
        ).move_to([0, -2.82, 0])
        self.assert_text_safe(constant, "scene02 constant-acceleration statement")
        self.play(FadeIn(constant), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 03
    # =========================================================================
    def scene_03_newton_to_gravity(self) -> None:
        self.set_header(
            3,
            "DE LAS FUERZAS A a = −g",
            "La ecuación a_y = −g se obtiene del diagrama de cuerpo libre; no se memoriza aislada.",
        )

        ball = self.ball([-4.60, 0.45, 0], 0.28)
        weight = self.vector_arrow([-3.95, 0.58, 0], DOWN * 1.60, r"\vec W=m\vec g", label_size=27)
        fbd_label = self.text("FREE-BODY DIAGRAM", 26, BOLD).move_to([-4.35, 2.02, 0])

        self.play(FadeIn(fbd_label), FadeIn(ball), run_time=RUN_NORMAL)
        self.play(GrowArrow(weight[0]), FadeIn(weight[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        chain = [
            r"\sum F_y=ma_y",
            r"-mg=ma_y",
            r"\frac{-mg}{m}=a_y",
            r"a_y=-g",
        ]

        step_cards = VGroup(
            self.phase_card(1, "CHOOSE +y", "Upward is positive, so weight is negative.", 5.2),
            self.phase_card(2, "APPLY NEWTON", "The only relevant force is −mg.", 5.2),
            self.phase_card(3, "CANCEL MASS", "The same m multiplies force and inertia.", 5.2),
            self.phase_card(4, "INTERPRET", "Ideal free-fall acceleration does not depend on mass.", 5.2),
        )
        for card in step_cards:
            card.move_to([3.45, -2.40, 0])

        current = self.math(chain[0], 48).move_to([2.55, 1.30, 0])
        self.play(Write(current), run_time=RUN_NORMAL)
        self.checkpoint_pause(step_cards[0], explain=PAUSE_READ)

        for i, expression in enumerate(chain[1:], start=1):
            target = self.math(expression, 48 if i < 3 else 56).move_to([2.55, 1.30, 0])
            self.play(TransformMatchingTex(current, target), run_time=RUN_SLOW)
            current = target
            self.checkpoint_pause(step_cards[i], explain=PAUSE_EXPLAIN)

        self.focus_on(current, width=5.6, pause=PAUSE_EXPLAIN)
        conclusion = self.text(
            "More mass → more weight, but also more inertia in exactly the same proportion.",
            22,
            BOLD,
        ).move_to([1.85, -1.16, 0])
        self.fit(conclusion, 9.6, 0.7)
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 04
    # =========================================================================
    def scene_04_derive_velocity_and_position(self) -> None:
        self.set_header(
            4,
            "DE a(t) A v(t) Y y(t)",
            "Usamos aceleración constante y velocidad media; cada transformación conserva el significado físico.",
        )

        # Left: velocity derivation
        vel_title = self.text("A. VELOCITY", 26, BOLD).move_to([-3.75, 2.02, 0])
        vel_stack = self.equation_stack(
            [
                r"a_y=\frac{v_y-v_0}{t}",
                r"-g=\frac{v_y-v_0}{t}",
                r"-gt=v_y-v_0",
                r"v_y=v_0-gt",
            ],
            sizes=[38, 38, 38, 44],
            max_width=6.0,
            max_height=3.8,
        ).move_to([-3.70, -0.15, 0])

        divider = Line([0, -2.65, 0], [0, 2.12, 0], color=LIGHT_GRAY, stroke_width=1.5)

        pos_title = self.text("B. POSITION", 26, BOLD).move_to([3.75, 2.02, 0])
        pos_stack = self.equation_stack(
            [
                r"\Delta y=v_{\mathrm{avg}}t",
                r"v_{\mathrm{avg}}=\frac{v_0+v_y}{2}",
                r"\Delta y=\frac{v_0+(v_0-gt)}{2}t",
                r"\Delta y=v_0t-\frac12gt^2",
                r"y=y_0+v_0t-\frac12gt^2",
            ],
            sizes=[36, 36, 34, 40, 42],
            max_width=6.4,
            max_height=4.2,
        ).move_to([3.70, -0.18, 0])

        self.play(FadeIn(vel_title), FadeIn(pos_title), Create(divider), run_time=RUN_NORMAL)

        for i, line in enumerate(vel_stack):
            self.play(Write(line), run_time=RUN_NORMAL)
            if i == 0:
                card = self.phase_card(1, "START FROM DEFINITION", "Constant acceleration links velocity change to elapsed time.", 5.5).move_to([-3.75, -2.65, 0])
            elif i == 1:
                card = self.phase_card(2, "INSERT THE SIGN", "Because +y is upward, gravity enters as −g.", 5.5).move_to([-3.75, -2.65, 0])
            elif i == 2:
                card = self.phase_card(3, "CLEAR THE FRACTION", "Multiply the relation by t.", 5.5).move_to([-3.75, -2.65, 0])
            else:
                card = self.phase_card(4, "ISOLATE v_y", "Velocity decreases linearly with time.", 5.5).move_to([-3.75, -2.65, 0])
            self.checkpoint_pause(card, explain=PAUSE_READ)

        self.play(Circumscribe(vel_stack[-1], color=BLACK_LINE), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        for i, line in enumerate(pos_stack):
            self.play(Write(line), run_time=RUN_NORMAL)
            pause = PAUSE_READ if i < 3 else PAUSE_EXPLAIN
            self.wait(pause)

        self.play(Circumscribe(pos_stack[-1], color=BLACK_LINE), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 05
    # =========================================================================
    def scene_05_three_initial_conditions(self) -> None:
        self.set_header(
            5,
            "TRES CONDICIONES, UNA MISMA GRAVEDAD",
            "Soltar, lanzar hacia arriba o lanzar hacia abajo cambia v₀; no cambia a_y = −g.",
        )

        xs = [-4.75, 0.0, 4.75]
        titles = ["DROP", "UPWARD LAUNCH", "DOWNWARD LAUNCH"]
        t = ValueTracker(0.0)

        cards = VGroup()
        for x, title in zip(xs, titles):
            box = RoundedRectangle(
                width=4.15,
                height=4.55,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=1.55,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            ).move_to([x, -0.15, 0])
            ttl = self.text(title, 25, BOLD).next_to(box.get_top(), DOWN, buff=0.18)
            guide = DashedLine([x, -1.80, 0], [x, 1.40, 0], dash_length=0.08, color=LIGHT_GRAY)
            cards.add(VGroup(box, ttl, guide))

        drop = always_redraw(
            lambda: self.ball([-4.75, 1.25 - 2.95 * t.get_value() ** 2, 0], 0.16)
        )
        upward = always_redraw(
            lambda: self.ball([0, -1.25 + 3.25 * 4 * t.get_value() * (1 - t.get_value()), 0], 0.16)
        )
        downward = always_redraw(
            lambda: self.ball([4.75, 1.25 - 2.95 * (0.22 * t.get_value() + 0.78 * t.get_value() ** 2), 0], 0.16)
        )

        grav = VGroup(
            *[
                self.vector_arrow([x + 0.55, 0.62, 0], DOWN * 0.78, r"\vec g", label_size=23)
                for x in xs
            ]
        )

        conditions = VGroup(
            VGroup(self.math(r"v_0=0", 30), self.math(r"a_y=-g", 30)).arrange(DOWN, buff=0.10).move_to([-4.75, -2.00, 0]),
            VGroup(self.math(r"v_0>0", 30), self.math(r"a_y=-g", 30)).arrange(DOWN, buff=0.10).move_to([0, -2.00, 0]),
            VGroup(self.math(r"v_0<0", 30), self.math(r"a_y=-g", 30)).arrange(DOWN, buff=0.10).move_to([4.75, -2.00, 0]),
        )

        self.play(FadeIn(cards), FadeIn(drop), FadeIn(upward), FadeIn(downward), FadeIn(grav), FadeIn(conditions), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(t.animate.set_value(1.0), run_time=RUN_SLOW * 2.15, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)

        master = self.formula_panel(
            r"y=y_0+v_0t-\frac12gt^2",
            width=6.2,
            height=1.05,
            font_size=44,
        ).move_to([0, -2.92, 0])
        self.play(FadeIn(master), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 06
    # =========================================================================
    def scene_06_upward_throw_worked_motion(self) -> None:
        self.set_header(
            6,
            "LANZAMIENTO VERTICAL: 14 m/s",
            "Detenemos el movimiento en los instantes físicamente importantes y resolvemos una pregunta por vez.",
        )

        t = ValueTracker(0.0)

        def state(tt: float) -> MotionState:
            return MotionState(
                tt,
                V0_UP * tt - 0.5 * G * tt**2,
                V0_UP - G * tt,
                -G,
            )

        def y_scene(tt: float) -> float:
            return -2.20 + 4.15 * (state(tt).y / H_APEX)

        axis = self.vertical_axis(-5.75, -2.45, 2.00)
        ground = self.ground(-2.45, -6.35, 0.85)

        moving = always_redraw(lambda: self.ball([-3.15, y_scene(t.get_value()), 0], 0.18))

        def velocity_visual():
            s = state(t.get_value())
            y = y_scene(t.get_value())
            if abs(s.v) < 0.45:
                return self.math(r"v=0", 30).move_to([-1.95, y, 0])
            return self.vector_arrow(
                [-2.55, y, 0],
                UP * np.clip(s.v / 11.0, -1.20, 1.20),
                r"\vec v",
                label_size=23,
            )

        live_v = always_redraw(velocity_visual)
        live_a = always_redraw(
            lambda: self.vector_arrow(
                [-3.72, y_scene(t.get_value()), 0],
                DOWN * 0.78,
                r"\vec a=-\vec g",
                label_size=23,
                label_side=LEFT,
            )
        )
        hud = self.live_state_panel(
            t,
            state,
            title="LIVE STATE",
            width=4.0,
            position=[4.35, 0.95, 0],
        )

        self.play(FadeIn(axis), FadeIn(ground), FadeIn(moving), FadeIn(live_v), FadeIn(live_a), FadeIn(hud), run_time=RUN_NORMAL)

        knowns = self.phase_card(1, "KNOWNS", "v₀ = +14 m/s, a = −9.81 m/s².", 4.8).move_to([4.15, -1.35, 0])
        self.checkpoint_pause(knowns, explain=PAUSE_EXPLAIN)

        self.play(t.animate.set_value(T_APEX), run_time=RUN_SLOW * 1.85, rate_func=linear)

        apex = self.phase_card(2, "APEX CONDITION", "At the highest point, v = 0.", 4.8).move_to([4.15, -1.35, 0])
        self.checkpoint_pause(apex, explain=PAUSE_EXPLAIN)

        eq_up = VGroup(
            self.math(r"0=14-9.81t", 35),
            self.math(r"t_{\max}=\frac{14}{9.81}\approx " + f"{T_APEX:.2f}" + r"\;s", 35),
        ).arrange(DOWN, buff=0.18).move_to([4.10, -1.30, 0])
        self.play(Write(eq_up[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(eq_up[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(eq_up), run_time=RUN_QUICK)

        h_eq = VGroup(
            self.math(r"\Delta y=v_0t-\frac12gt^2", 34),
            self.math(r"\Delta y_{\max}\approx " + f"{H_APEX:.2f}" + r"\;m", 38),
        ).arrange(DOWN, buff=0.18).move_to([4.10, -1.30, 0])
        self.play(Write(h_eq[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(h_eq[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(h_eq), run_time=RUN_QUICK)

        symmetry = self.phase_card(
            3,
            "RETURN TO SAME HEIGHT",
            f"Ignoring air: total time ≈ {T_RETURN:.2f} s.",
            4.9,
        ).move_to([4.10, -1.35, 0])
        self.checkpoint_pause(symmetry, explain=PAUSE_EXPLAIN)
        self.play(t.animate.set_value(T_RETURN), run_time=RUN_SLOW * 1.85, rate_func=linear)

        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 07
    # =========================================================================
    def scene_07_motion_graphs_synchronized(self) -> None:
        self.set_header(
            7,
            "MOVIMIENTO Y GRÁFICAS: UN MISMO RELOJ",
            "La pelota, y(t), v(t) y a(t) se leen en el mismo instante; no son cuatro historias diferentes.",
        )

        t = ValueTracker(0.0)

        track = Line([-6.10, -2.25, 0], [-6.10, 1.95, 0], color=LIGHT_GRAY, stroke_width=2)
        moving = always_redraw(
            lambda: self.ball(
                [
                    -6.10,
                    -2.25
                    + 4.20
                    * ((V0_UP * t.get_value() - 0.5 * G * t.get_value() ** 2) / H_APEX),
                    0,
                ],
                0.13,
            )
        )

        ax_y = Axes(
            x_range=[0, T_RETURN, 0.7],
            y_range=[0, 11, 2],
            x_length=4.55,
            y_length=1.55,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_tip": False},
        ).move_to([-1.45, 1.46, 0])
        ax_v = Axes(
            x_range=[0, T_RETURN, 0.7],
            y_range=[-15, 15, 5],
            x_length=4.55,
            y_length=1.55,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_tip": False},
        ).move_to([-1.45, -0.45, 0])
        ax_a = Axes(
            x_range=[0, T_RETURN, 0.7],
            y_range=[-12, 2, 4],
            x_length=4.55,
            y_length=1.50,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_tip": False},
        ).move_to([-1.45, -2.23, 0])

        curve_y = ax_y.plot(lambda q: V0_UP * q - 0.5 * G * q**2, x_range=[0, T_RETURN], color=BLACK_LINE, stroke_width=3.0)
        curve_v = ax_v.plot(lambda q: V0_UP - G * q, x_range=[0, T_RETURN], color=BLACK_LINE, stroke_width=3.0)
        curve_a = ax_a.plot(lambda q: -G, x_range=[0, T_RETURN], color=BLACK_LINE, stroke_width=3.0)

        dot_y = always_redraw(lambda: Dot(ax_y.c2p(t.get_value(), V0_UP * t.get_value() - 0.5 * G * t.get_value()**2), radius=0.065, color=BLACK_LINE))
        dot_v = always_redraw(lambda: Dot(ax_v.c2p(t.get_value(), V0_UP - G * t.get_value()), radius=0.065, color=BLACK_LINE))
        dot_a = always_redraw(lambda: Dot(ax_a.c2p(t.get_value(), -G), radius=0.065, color=BLACK_LINE))

        labels = VGroup(
            self.text("y(t)", 23, BOLD).next_to(ax_y, LEFT, buff=0.15),
            self.text("v(t)", 23, BOLD).next_to(ax_v, LEFT, buff=0.15),
            self.text("a(t)", 23, BOLD).next_to(ax_a, LEFT, buff=0.15),
        )

        hud = self.live_state_panel(
            t,
            lambda q: MotionState(q, V0_UP * q - 0.5 * G * q**2, V0_UP - G * q, -G),
            title="SAME INSTANT",
            width=3.8,
            position=[5.05, -0.10, 0],
        )

        self.play(FadeIn(track), FadeIn(moving), FadeIn(ax_y), FadeIn(ax_v), FadeIn(ax_a), FadeIn(labels), run_time=RUN_NORMAL)
        self.play(Create(curve_y), Create(curve_v), Create(curve_a), run_time=RUN_SLOW)
        self.play(FadeIn(dot_y), FadeIn(dot_v), FadeIn(dot_a), FadeIn(hud), run_time=RUN_QUICK)

        self.play(t.animate.set_value(T_APEX), run_time=RUN_SLOW * 1.70, rate_func=linear)
        apex_note = self.phase_card(
            1,
            "READ THE APEX",
            "y is maximum exactly when v crosses zero; a remains constant.",
            5.0,
        ).move_to([4.85, 2.02, 0])
        self.checkpoint_pause(apex_note, explain=PAUSE_EXPLAIN)

        self.play(t.animate.set_value(T_RETURN), run_time=RUN_SLOW * 1.70, rate_func=linear)

        link = self.note_panel(
            "SLOPE CONNECTION",
            [
                "slope of y(t) → velocity",
                "slope of v(t) → acceleration",
                "constant a → linear v → parabolic y",
            ],
            width=4.3,
            title_size=25,
            body_size=23,
        ).move_to([5.00, -2.16, 0])
        self.play(FadeIn(link), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 08
    # =========================================================================
    def scene_08_twenty_meter_drop_stepwise(self) -> None:
        self.set_header(
            8,
            "CAÍDA DESDE 20 m: SOLUCIÓN COMPLETA",
            "La animación y la solución avanzan juntas: datos → ecuación → tiempo → velocidad de impacto → verificación.",
        )

        t = ValueTracker(0.0)

        def state(tt: float) -> MotionState:
            return MotionState(tt, DROP_H - 0.5 * G * tt**2, -G * tt, -G)

        def y_scene(tt: float) -> float:
            return -2.45 + 4.70 * (state(tt).y / DROP_H)

        ruler = Line([-5.55, -2.45, 0], [-5.55, 2.25, 0], color=BLACK_LINE, stroke_width=2)
        marks = VGroup()
        for m in (0, 5, 10, 15, 20):
            yy = -2.45 + 4.70 * m / 20
            tick = Line([-5.67, yy, 0], [-5.43, yy, 0], color=BLACK_LINE, stroke_width=1.3)
            lab = self.text(f"{m} m", 22).next_to(tick, LEFT, buff=0.08)
            marks.add(tick, lab)

        floor = self.ground(-2.45, -6.35, 0.15)
        moving = always_redraw(lambda: self.ball([-3.28, y_scene(t.get_value()), 0], 0.18))
        vel = always_redraw(
            lambda: self.vector_arrow(
                [-2.65, y_scene(t.get_value()), 0],
                DOWN * max(0.12, min(1.25, abs(state(t.get_value()).v) / 15.5)),
                r"\vec v",
                label_size=23,
            )
        )
        hud = self.live_state_panel(
            t,
            state,
            title="20 m DROP",
            width=3.9,
            position=[4.55, 1.15, 0],
        )

        solution_box = RoundedRectangle(
            width=5.9,
            height=3.0,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to([4.45, -1.50, 0])
        sol_title = self.text("STEP-BY-STEP SOLUTION", 25, BOLD).next_to(solution_box.get_top(), DOWN, buff=0.18)

        steps = [
            self.math(r"1.\quad y_0=20\,m,\;v_0=0,\;a=-g", 29),
            self.math(r"2.\quad 0=20-\frac12gt^2", 29),
            self.math(r"3.\quad t=\sqrt{\frac{40}{9.81}}\approx " + f"{T_DROP:.2f}" + r"\,s", 29),
            self.math(r"4.\quad v=-gt\approx -" + f"{V_IMPACT:.2f}" + r"\,m/s", 29),
        ]
        stack = VGroup(*steps).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        self.fit(stack, 5.45, 2.05)
        stack.move_to(solution_box).shift(DOWN * 0.18)

        self.assert_text_safe(VGroup(solution_box, sol_title), "scene08 solution panel")
        self.play(FadeIn(ruler), FadeIn(marks), FadeIn(floor), FadeIn(moving), FadeIn(vel), FadeIn(hud), FadeIn(solution_box), FadeIn(sol_title), run_time=RUN_NORMAL)

        for i, line in enumerate(stack):
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN if i in (1, 2) else PAUSE_READ)

        self.play(t.animate.set_value(T_DROP), run_time=RUN_SLOW * 2.10, rate_func=linear)

        impact = self.phase_card(
            5,
            "INTERPRET THE SIGN",
            f"v ≈ −{V_IMPACT:.2f} m/s means downward; speed is {V_IMPACT:.2f} m/s.",
            5.6,
        ).move_to([3.75, -3.15, 0])
        self.checkpoint_pause(impact, explain=PAUSE_EXPLAIN)

        check = self.math(r"\sqrt{2gh}=\sqrt{2(9.81)(20)}\approx " + f"{V_IMPACT:.2f}" + r"\,m/s", 31).move_to([3.95, -2.85, 0])
        self.play(Write(check), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 09
    # =========================================================================
    def scene_09_stroboscopic_square_law(self) -> None:
        self.set_header(
            9,
            "FOTOGRAMAS IGUALES: d ∝ t²",
            "Antes de mostrar la fórmula, observamos cómo crecen los desplazamientos durante intervalos de tiempo iguales.",
        )

        x = -2.75
        top_y = 2.05
        dt = 0.10
        times = np.array([0, dt, 2 * dt, 3 * dt, 4 * dt])
        normalized = np.array([0, 1, 4, 9, 16], dtype=float)
        scale = 0.255

        guide = Line([x, -2.35, 0], [x, top_y, 0], color=LIGHT_GRAY, stroke_width=2)
        timer = self.note_panel(
            "HIGH-SPEED VIEW",
            ["Equal frame interval: Δt = 0.10 s", "The camera samples position at equal times."],
            width=5.2,
            title_size=26,
            body_size=23,
        ).move_to([3.85, 1.55, 0])

        self.play(Create(guide), FadeIn(timer), run_time=RUN_NORMAL)

        balls = VGroup()
        time_labels = VGroup()
        for tt, sq in zip(times, normalized):
            y = top_y - scale * sq
            b = self.ghost_ball([x, y, 0], 0.13)
            lab = self.text(f"t={tt:.1f}s", 22).next_to(b, LEFT, buff=0.15)
            balls.add(b)
            time_labels.add(lab)
            self.play(FadeIn(b, scale=0.6), FadeIn(lab), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT * 0.55)

        brackets = VGroup()
        odd_labels = VGroup()
        for i in range(1, len(times)):
            y0 = top_y - scale * normalized[i - 1]
            y1 = top_y - scale * normalized[i]
            bracket = DoubleArrow(
                [x + 0.62, y0, 0],
                [x + 0.62, y1, 0],
                buff=0.02,
                color=BLACK_LINE,
                stroke_width=2.0,
                tip_length=0.10,
            )
            lab = self.text(str(2 * i - 1), 24, BOLD).next_to(bracket, RIGHT, buff=0.10)
            brackets.add(bracket)
            odd_labels.add(lab)

        self.play(LaggedStart(*[GrowArrow(b) for b in brackets], lag_ratio=0.18), run_time=RUN_SLOW * 1.5)
        self.play(FadeIn(odd_labels), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        odd_note = self.phase_card(
            1,
            "SUCCESSIVE INTERVALS",
            "Distances added each equal interval grow as 1 : 3 : 5 : 7.",
            5.4,
        ).move_to([3.85, 0.20, 0])
        self.checkpoint_pause(odd_note, explain=PAUSE_EXPLAIN)

        cumulative = self.phase_card(
            2,
            "CUMULATIVE DISTANCE",
            "After 1,2,3,4 intervals: 1 : 4 : 9 : 16 = 1² : 2² : 3² : 4².",
            5.7,
        ).move_to([3.85, -0.25, 0])
        self.checkpoint_pause(cumulative, explain=PAUSE_EXPLAIN)

        relation = self.formula_panel(
            r"d\propto t^2\qquad\Longrightarrow\qquad d=\frac12gt^2\;\;(v_0=0)",
            width=8.3,
            height=1.10,
            font_size=38,
        ).move_to([3.55, -1.95, 0])
        self.play(FadeIn(relation), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 10
    # =========================================================================
    def scene_10_mass_independence_and_model_limit(self) -> None:
        self.set_header(
            10,
            "MASA Y LÍMITES DEL MODELO",
            "Separamos una afirmación del modelo gravitacional de los efectos reales de resistencia del aire.",
        )

        t = ValueTracker(0.0)
        xs = [-3.0, 3.0]
        guides = VGroup(
            DashedLine([-3, -2.10, 0], [-3, 1.85, 0], dash_length=0.08, color=LIGHT_GRAY),
            DashedLine([3, -2.10, 0], [3, 1.85, 0], dash_length=0.08, color=LIGHT_GRAY),
        )
        b1 = always_redraw(lambda: self.ball([-3, 1.55 - 3.40 * t.get_value()**2, 0], 0.16))
        b2 = always_redraw(lambda: self.ball([3, 1.55 - 3.40 * t.get_value()**2, 0], 0.24, fill=PAPER_GRAY))
        m1 = self.text("1 kg", 24, BOLD).move_to([-3, 2.15, 0])
        m2 = self.text("5 kg", 24, BOLD).move_to([3, 2.15, 0])

        w1 = self.vector_arrow([-2.45, 0.95, 0], DOWN * 0.70, r"m_1g", label_size=23)
        w2 = self.vector_arrow([3.60, 0.95, 0], DOWN * 1.18, r"m_2g", label_size=23)

        self.play(FadeIn(guides), FadeIn(b1), FadeIn(b2), FadeIn(m1), FadeIn(m2), FadeIn(w1), FadeIn(w2), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(1.0), run_time=RUN_SLOW * 1.8, rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)

        derivation = self.formula_panel(
            r"a=\frac{F}{m}=\frac{mg}{m}=g",
            width=5.0,
            height=1.08,
            font_size=44,
        ).move_to([0, -2.67, 0])
        self.play(FadeIn(derivation), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        caveat = self.note_panel(
            "MODEL LIMIT",
            [
                "Vacuum model: same g for both masses.",
                "Real air: drag depends on shape, area and speed.",
                "Therefore choose compact objects for the classroom test.",
            ],
            width=6.9,
            title_size=26,
            body_size=23,
        ).move_to([0, 0.0, 0])
        self.play(FadeOut(w1), FadeOut(w2), FadeIn(caveat), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 11
    # =========================================================================
    def scene_11_lab_prediction_table_and_linearization(self) -> None:
        self.set_header(
            11,
            "DEL MODELO A LA GRÁFICA LINEAL",
            "Construimos la tabla teórica, graficamos d vs t y después cambiamos la variable horizontal a t².",
        )

        rows = [
            [
                f"{t:.2f}",
                f"{t*t:.4f}",
                f"{d:.4f}",
            ]
            for t, d in zip(LAB_TIMES, LAB_D)
        ]
        table = self.build_table(
            headers=("t (s)", "t^2 (s^2)", "d theoretical (m)"),
            body_rows=rows,
            column_widths=(1.8, 2.1, 2.9),
            math_columns=(0, 1, 2),
            row_height=0.58,
            header_height=0.66,
            body_font_size=25,
            header_font_size=24,
        )
        table.group.move_to([-3.90, -0.15, 0])

        self.play(FadeIn(table.header), run_time=RUN_NORMAL)
        for row in table.rows[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.10), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)

        ax1 = Axes(
            x_range=[0, 0.42, 0.1],
            y_range=[0, 0.85, 0.2],
            x_length=4.7,
            y_length=3.25,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_tip": False},
        ).move_to([3.65, 0.55, 0])
        title1 = self.text("d vs t", 24, BOLD).next_to(ax1, UP, buff=0.12)
        pts1 = VGroup(*[Dot(ax1.c2p(t, d), radius=0.065, color=BLACK_LINE) for t, d in zip(LAB_TIMES, LAB_D)])
        curve = ax1.plot(lambda q: 0.5 * G * q**2, x_range=[0, 0.41], color=BLACK_LINE, stroke_width=2.8)

        self.play(FadeIn(ax1), FadeIn(title1), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts1], lag_ratio=0.18), run_time=RUN_SLOW)
        self.play(Create(curve), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        # Replace graph by t² linearized graph.
        ax2 = Axes(
            x_range=[0, 0.17, 0.04],
            y_range=[0, 0.85, 0.2],
            x_length=4.7,
            y_length=3.25,
            axis_config={"color": MID_GRAY, "stroke_width": 1.4, "include_tip": False},
        ).move_to(ax1)
        title2 = self.text("d vs t²", 24, BOLD).move_to(title1)
        pts2 = VGroup(*[Dot(ax2.c2p(t2, d), radius=0.065, color=BLACK_LINE) for t2, d in zip(LAB_T2, LAB_D)])
        line = ax2.plot(lambda q: 0.5 * G * q, x_range=[0, 0.165], color=BLACK_LINE, stroke_width=2.8)

        change = self.phase_card(
            1,
            "LINEARIZE",
            "Replace horizontal coordinate t by t²; the curved pattern becomes a straight line.",
            5.3,
        ).move_to([3.60, -2.05, 0])
        self.checkpoint_pause(change, explain=PAUSE_EXPLAIN)

        self.play(
            ReplacementTransform(ax1, ax2),
            ReplacementTransform(title1, title2),
            ReplacementTransform(pts1, pts2),
            FadeOut(curve),
            run_time=RUN_SLOW,
        )
        self.play(Create(line), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        slope = self.formula_panel(
            r"m=\frac{\Delta d}{\Delta(t^2)}=\frac g2\qquad\Longrightarrow\qquad g=2m",
            width=7.5,
            height=1.05,
            font_size=35,
        ).move_to([2.85, -2.64, 0])
        self.play(FadeIn(slope), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # =========================================================================
    # 12
    # =========================================================================
    def scene_12_experimental_protocol_bridge(self) -> None:
        self.set_header(
            12,
            "PROTOCOLO EXPERIMENTAL",
            "La teoría termina cuando produce una predicción que puede medirse, repetirse, graficarse y contrastarse.",
        )

        route = self.process_map(
            [
                ("1", "RELEASE WITHOUT PUSH"),
                ("2", "CALIBRATE DISTANCE"),
                ("3", "MEASURE TIME"),
                ("4", "REPEAT TRIALS"),
                ("5", "PLOT d vs t²"),
                ("6", "ESTIMATE g = 2m"),
            ],
            card_width=4.15,
            card_height=1.05,
            columns=3,
        )
        route.move_to([0, 0.70, 0])
        self.fit(route, 13.7, 3.0)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.7,
        )
        self.wait(PAUSE_EXPLAIN)

        controls = self.note_panel(
            "CONTROL THE MAIN SOURCES OF ERROR",
            [
                "same release point and same reference zero",
                "camera perpendicular to the motion plane",
                "visible calibrated scale and known frame rate",
                "compact object to reduce air-drag effects",
                "repeat measurements instead of trusting one fall",
            ],
            width=7.2,
            title_size=26,
            body_size=23,
        ).move_to([-3.70, -2.05, 0])

        decision = VGroup(
            self.formula_panel(r"g_{\mathrm{exp}}=2m", width=4.8, height=1.00, font_size=40),
            self.formula_panel(
                r"\%\,\mathrm{error}=\frac{|g_{\mathrm{exp}}-9.81|}{9.81}\times100",
                width=5.7,
                height=1.00,
                font_size=30,
            ),
        ).arrange(DOWN, buff=0.22).move_to([4.25, -2.05, 0])

        self.play(FadeIn(controls), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(decision[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(decision[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)

        final = self.text(
            "The laboratory question is not “Can we get exactly 9.81?” — it is “Do our measurements support the t² model within experimental uncertainty?”",
            22,
            BOLD,
        )
        self.fit(final, 13.6, 0.75)
        final.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()