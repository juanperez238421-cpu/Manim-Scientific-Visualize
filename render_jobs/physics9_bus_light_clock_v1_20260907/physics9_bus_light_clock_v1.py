#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Special Relativity
Bus light-clock exercise: from constant c to time dilation.

Source problem
--------------
A futuristic bus moves at v = 0.60c. Inside the bus Ana has a vertical
light clock with mirror separation L = 3.0 m. Carlos observes from the road.
The lesson derives the different measured times geometrically and numerically.

Final render:
    manim -pqh physics9_bus_light_clock_v1.py Physics9BusLightClockV1 \
        --format=mp4 --disable_caching

Compatible target: Manim Community Edition 0.20.1.
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
# VISUAL SYSTEM — JP CLASSROOM / PROJECTOR SAFE
# =============================================================================
INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D8D8D8"
VERY_LIGHT = "#EEEEEE"
PAPER = "#F7F7F7"
AMBER = "#D6A000"   # reserved for the light pulse/path
WHITE_FILL = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_FAST = 0.65
RUN = 1.00
RUN_SLOW = 1.40
RUN_MOTION = 2.50
PAUSE_SHORT = 0.80
PAUSE_READ = 1.65
PAUSE_EXPLAIN = 2.55
PAUSE_COPY = 3.40
PAUSE_SUMMARY = 4.10
PAUSE_FINAL = 4.80


class Physics9BusLightClockV1(Scene):
    """Full animated derivation of time dilation from a vertical light clock."""

    C = 3.0e8
    V_FRAC = 0.60
    V = V_FRAC * C
    L = 3.0
    T0 = 1.0e-8
    GAMMA = 1.25
    T = 1.25e-8
    DX = 2.25
    LIGHT_PATH = 3.75

    # -------------------------------------------------------------------------
    # Global timing wrappers
    # -------------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Typography / layout helpers
    # -------------------------------------------------------------------------
    def txt(self, content, size=30, weight=NORMAL, color=INK):
        return Text(content, font_size=size, weight=weight, color=color)

    def mathtex(self, expression, size=40, color=INK):
        return MathTex(expression, font_size=size, color=color)

    def fit(self, mob, max_w=14.2, max_h=None):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if max_h is not None and mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def header(self, number, title, subtitle):
        kicker = self.txt(f"FÍSICA 9  •  RELATIVIDAD ESPECIAL  •  {number:02d}", 18, BOLD, DARK)
        title_m = self.fit(self.txt(title, 34, BOLD), 14.1, 0.62)
        sub_m = self.fit(self.txt(subtitle, 20, NORMAL, DARK), 14.0, 0.45)
        group = VGroup(kicker, title_m, sub_m).arrange(DOWN, buff=0.07)
        group.to_edge(UP, buff=0.16)
        rule = Line(LEFT * 7.25, RIGHT * 7.25, color=LIGHT, stroke_width=2)
        rule.next_to(group, DOWN, buff=0.09)
        return VGroup(group, rule)

    def formula_box(self, tex, width=6.0, height=1.00, size=39, stroke=DARK, fill=PAPER):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=stroke,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1.0,
        )
        eq = self.mathtex(tex, size)
        self.fit(eq, width - 0.45, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def text_box(self, text, width=5.4, height=0.90, size=25, bold=True, stroke=DARK, fill=WHITE):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=stroke,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1.0,
        )
        label = self.fit(self.txt(text, size, BOLD if bold else NORMAL), width - 0.42, height - 0.20)
        label.move_to(box)
        return VGroup(box, label)

    def note_box(self, title, lines, width=6.0, title_size=24, body_size=21, fill=WHITE):
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.58, 3.7)
        box = RoundedRectangle(
            width=width,
            height=max(1.2, content.height + 0.60),
            corner_radius=0.10,
            stroke_color=DARK,
            stroke_width=1.6,
            fill_color=fill,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.29)
        return VGroup(box, content)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_FAST)

    def assert_frame(self, mob, label, margin=0.04):
        if mob.get_left()[0] < -8 + margin or mob.get_right()[0] > 8 - margin:
            raise ValueError(f"{label} exceeds horizontal frame")
        if mob.get_bottom()[1] < -4.5 + margin or mob.get_top()[1] > 4.5 - margin:
            raise ValueError(f"{label} exceeds vertical frame")

    # -------------------------------------------------------------------------
    # Reusable pictograms
    # -------------------------------------------------------------------------
    def person(self, scale=1.0, seated=False):
        head = Circle(
            radius=0.18 * scale,
            stroke_color=INK,
            stroke_width=2.4,
            fill_color=WHITE,
            fill_opacity=1,
        ).shift(UP * 0.72 * scale)
        if seated:
            torso = Line(UP * 0.50 * scale, UP * 0.02 * scale, color=INK, stroke_width=5)
            arm = Line(UP * 0.32 * scale, RIGHT * 0.25 * scale + UP * 0.17 * scale, color=INK, stroke_width=4)
            thigh = Line(UP * 0.02 * scale, RIGHT * 0.32 * scale + DOWN * 0.10 * scale, color=INK, stroke_width=5)
            shin = Line(
                RIGHT * 0.32 * scale + DOWN * 0.10 * scale,
                RIGHT * 0.32 * scale + DOWN * 0.50 * scale,
                color=INK,
                stroke_width=5,
            )
            return VGroup(head, torso, arm, thigh, shin)
        torso = Line(UP * 0.52 * scale, DOWN * 0.10 * scale, color=INK, stroke_width=5)
        arm1 = Line(UP * 0.30 * scale, LEFT * 0.23 * scale + UP * 0.03 * scale, color=INK, stroke_width=4)
        arm2 = Line(UP * 0.30 * scale, RIGHT * 0.23 * scale + UP * 0.03 * scale, color=INK, stroke_width=4)
        leg1 = Line(DOWN * 0.10 * scale, LEFT * 0.18 * scale + DOWN * 0.58 * scale, color=INK, stroke_width=5)
        leg2 = Line(DOWN * 0.10 * scale, RIGHT * 0.18 * scale + DOWN * 0.58 * scale, color=INK, stroke_width=5)
        return VGroup(head, torso, arm1, arm2, leg1, leg2)

    def bus(self, width=8.4, height=2.8, include_clock=True):
        body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.22,
            stroke_color=INK,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1,
        )
        windows = VGroup()
        for frac in (-0.31, -0.10, 0.11, 0.32):
            w = RoundedRectangle(
                width=min(1.35, width / 5.9),
                height=0.70,
                corner_radius=0.07,
                stroke_color=LIGHT,
                stroke_width=1.4,
                fill_color=PAPER,
                fill_opacity=1,
            )
            w.move_to(body.get_center() + RIGHT * (frac * width) + UP * 0.65)
            windows.add(w)
        floor = Line(
            body.get_left() + RIGHT * 0.35 + DOWN * 0.85,
            body.get_right() + LEFT * 0.35 + DOWN * 0.85,
            color=LIGHT,
            stroke_width=2,
        )
        wheels = VGroup(
            Circle(radius=0.19, stroke_color=INK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1),
            Circle(radius=0.19, stroke_color=INK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1),
        )
        wheels[0].move_to(body.get_center() + LEFT * (width * 0.29) + DOWN * (height / 2 + 0.14))
        wheels[1].move_to(body.get_center() + RIGHT * (width * 0.29) + DOWN * (height / 2 + 0.14))

        base = VGroup(body, windows, floor, wheels)
        if not include_clock:
            return base

        x_clock = body.get_center()[0] + width * 0.22
        lower = Line(LEFT * 0.36, RIGHT * 0.36, color=INK, stroke_width=6)
        upper = lower.copy()
        lower.move_to(np.array([x_clock, body.get_center()[1] - 0.84, 0]))
        upper.move_to(np.array([x_clock, body.get_center()[1] + 0.84, 0]))
        clock_line = DashedLine(lower.get_center(), upper.get_center(), dash_length=0.10, color=LIGHT, stroke_width=2)
        return VGroup(body, windows, floor, wheels, lower, upper, clock_line)

    def light_pulse(self, center, radius=0.085):
        glow = Circle(radius=radius * 2.4, stroke_width=0, fill_color=AMBER, fill_opacity=0.18).move_to(center)
        dot = Dot(center, radius=radius, color=AMBER)
        return VGroup(glow, dot)

    def velocity_arrow(self, start, end, label, size=26):
        arrow = Arrow(start, end, buff=0, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.13)
        lab = self.mathtex(label, size).next_to(arrow, UP, buff=0.10)
        return VGroup(arrow, lab)

    def observer_badge(self, label, center, width=3.1):
        box = RoundedRectangle(
            width=width,
            height=0.62,
            corner_radius=0.08,
            stroke_color=DARK,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=1,
        )
        text = self.fit(self.txt(label, 20, BOLD), width - 0.35, 0.38).move_to(box)
        return VGroup(box, text).move_to(center)

    def clock_card(self, title, value_tex, subtitle, width=5.4):
        box = RoundedRectangle(
            width=width,
            height=2.20,
            corner_radius=0.12,
            stroke_color=DARK,
            stroke_width=1.7,
            fill_color=PAPER,
            fill_opacity=1,
        )
        title_m = self.txt(title, 24, BOLD)
        value = self.mathtex(value_tex, 42)
        sub = self.fit(self.txt(subtitle, 20, NORMAL, DARK), width - 0.45, 0.45)
        stack = VGroup(title_m, value, sub).arrange(DOWN, buff=0.18).move_to(box)
        return VGroup(box, stack)

    # -------------------------------------------------------------------------
    # Scientific validation
    # -------------------------------------------------------------------------
    def validate_data(self):
        assert math.isclose(self.T0, self.L / self.C, rel_tol=0, abs_tol=1e-16)
        gamma = 1.0 / math.sqrt(1.0 - self.V_FRAC**2)
        assert math.isclose(gamma, self.GAMMA, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(self.T, self.GAMMA * self.T0, rel_tol=0, abs_tol=1e-16)
        assert math.isclose(self.V * self.T, self.DX, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(self.C * self.T, self.LIGHT_PATH, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(self.LIGHT_PATH**2, self.L**2 + self.DX**2, rel_tol=0, abs_tol=1e-12)
        assert math.isclose(2 * self.T0, 20e-9, rel_tol=0, abs_tol=1e-16)
        assert math.isclose(2 * self.T, 25e-9, rel_tol=0, abs_tol=1e-16)

    # -------------------------------------------------------------------------
    # Orchestration
    # -------------------------------------------------------------------------
    def construct(self):
        self.validate_data()
        self.opening()
        self.ana_inside()
        self.carlos_outside()
        self.freeze_triangle()
        self.derive_time_dilation()
        self.calculate_bus_case()
        self.interpret_result()
        self.classical_conflict()
        self.low_speed_limit()
        self.discussion_question()
        self.summary()

    # -------------------------------------------------------------------------
    # 00 — Opening
    # -------------------------------------------------------------------------
    def opening(self):
        top = VGroup(
            self.txt("FÍSICA 9 • RELATIVIDAD ESPECIAL", 22, BOLD, DARK),
            self.fit(self.txt("EL BUS EXTREMADAMENTE RÁPIDO Y EL RELOJ DE LUZ", 42, BOLD), 14.0),
            self.txt("¿Puede la luz mantener la misma velocidad para dos observadores?", 25, NORMAL, DARK),
        ).arrange(DOWN, buff=0.15).shift(UP * 2.70)

        road = Line(LEFT * 7.2 + DOWN * 2.15, RIGHT * 7.2 + DOWN * 2.15, color=MID, stroke_width=2)
        bus = self.bus(8.7, 2.75, include_clock=True).shift(LEFT * 1.05 + DOWN * 0.32)
        ana = self.person(0.68).move_to(bus.get_center() + LEFT * 1.15 + DOWN * 0.14)
        carlos = self.person(0.70).move_to(RIGHT * 5.20 + DOWN * 0.80)
        label_ana = self.txt("ANA", 20, BOLD).next_to(ana, DOWN, buff=0.08)
        label_carlos = self.txt("CARLOS", 20, BOLD).next_to(carlos, DOWN, buff=0.08)
        speed = self.velocity_arrow(LEFT * 4.6 + DOWN * 2.72, LEFT * 1.2 + DOWN * 2.72, r"v=0.60c")
        clock_label = self.txt("reloj de luz", 19, BOLD, DARK).next_to(bus[5], RIGHT, buff=0.15)

        self.play(Write(top), run_time=RUN_SLOW)
        self.play(Create(road), FadeIn(bus), FadeIn(ana), FadeIn(carlos), FadeIn(label_ana), FadeIn(label_carlos), run_time=RUN)
        self.play(GrowArrow(speed[0]), Write(speed[1]), FadeIn(clock_label), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 01 — Ana inside the bus
    # -------------------------------------------------------------------------
    def ana_inside(self):
        h = self.header(
            1,
            "ANA DENTRO DEL BUS: LA LUZ SUBE Y BAJA VERTICALMENTE",
            "En el marco del bus, los espejos están quietos y separados por L = 3.0 m.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        clock_box = RoundedRectangle(
            width=5.1,
            height=4.75,
            corner_radius=0.16,
            stroke_color=DARK,
            stroke_width=2,
            fill_color=PAPER,
            fill_opacity=1,
        ).move_to(LEFT * 3.8 + DOWN * 0.60)
        lower = Line(LEFT * 0.75, RIGHT * 0.75, color=INK, stroke_width=7).move_to(clock_box.get_center() + DOWN * 1.55)
        upper = lower.copy().move_to(clock_box.get_center() + UP * 1.55)
        height_line = DoubleArrow(
            lower.get_center() + RIGHT * 1.15,
            upper.get_center() + RIGHT * 1.15,
            buff=0.05,
            color=INK,
            stroke_width=3,
            tip_length=0.16,
        )
        height_label = self.mathtex(r"L=3.0\,\mathrm{m}", 28).next_to(height_line, RIGHT, buff=0.10)
        pulse = self.light_pulse(lower.get_center())
        path_up = Line(lower.get_center(), upper.get_center())
        path_down = Line(upper.get_center(), lower.get_center())
        caption = self.txt("Para Ana, el bus está en reposo.", 22, BOLD).next_to(clock_box, DOWN, buff=0.18)

        equations = VGroup(
            self.formula_box(r"t_0=\frac{L}{c}", 5.6, 1.02, 42),
            self.formula_box(r"t_0=\frac{3.0}{3.0\times10^8}", 5.6, 1.02, 37),
            self.formula_box(r"t_0=1.0\times10^{-8}\,\mathrm{s}=10\,\mathrm{ns}", 5.6, 1.08, 33),
        ).arrange(DOWN, buff=0.27).move_to(RIGHT * 3.35 + DOWN * 0.25)
        note = self.text_box("Este es el tiempo de un medio recorrido: piso → techo.", 6.1, 0.86, 21, False)
        note.next_to(equations, DOWN, buff=0.28)

        visual = VGroup(clock_box, lower, upper, height_line, height_label, caption)
        self.assert_frame(VGroup(visual, equations, note, h), "ana_inside")
        self.play(FadeIn(clock_box), Create(lower), Create(upper), GrowFromCenter(height_line), Write(height_label), FadeIn(caption), run_time=RUN)
        self.play(FadeIn(pulse), run_time=RUN_FAST)
        self.play(MoveAlongPath(pulse, path_up), run_time=RUN_MOTION)
        self.play(MoveAlongPath(pulse, path_down), run_time=RUN_MOTION)
        self.wait(PAUSE_SHORT)
        for eq in equations:
            self.play(FadeIn(eq, shift=UP * 0.08), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_FAST)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 02 — Carlos outside
    # -------------------------------------------------------------------------
    def carlos_outside(self):
        h = self.header(
            2,
            "CARLOS DESDE AFUERA: LA TRAYECTORIA YA NO ES VERTICAL",
            "Mientras la luz sube, el bus avanza. Carlos ve una trayectoria diagonal.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        road = Line(LEFT * 7.2 + DOWN * 2.25, RIGHT * 7.2 + DOWN * 2.25, color=MID, stroke_width=2)
        bus = self.bus(7.7, 2.55, include_clock=True).move_to(LEFT * 2.15 + DOWN * 0.65)
        carlos = self.person(0.66).move_to(RIGHT * 6.15 + DOWN * 1.00)
        carlos_lab = self.txt("CARLOS", 19, BOLD).next_to(carlos, DOWN, buff=0.07)
        velocity = self.velocity_arrow(LEFT * 5.7 + DOWN * 2.74, LEFT * 3.0 + DOWN * 2.74, r"0.60c", 24)

        start = bus[4].get_center().copy()
        upper_initial = bus[5].get_center().copy()
        horizontal_shift = 3.20
        end = upper_initial + RIGHT * horizontal_shift
        pulse = self.light_pulse(start)
        trace = TracedPath(pulse.get_center, stroke_color=AMBER, stroke_width=6, dissipating_time=None)

        self.play(Create(road), FadeIn(bus), FadeIn(carlos), FadeIn(carlos_lab), GrowArrow(velocity[0]), Write(velocity[1]), run_time=RUN)
        self.play(FadeIn(pulse), run_time=RUN_FAST)
        self.add(trace)
        self.play(
            bus.animate.shift(RIGHT * horizontal_shift),
            pulse.animate.move_to(end),
            run_time=RUN_MOTION * 1.25,
            rate_func=linear,
        )
        self.wait(PAUSE_SHORT)

        corner = np.array([end[0], start[1], 0])
        horiz = DashedLine(start, corner, dash_length=0.12, color=DARK, stroke_width=2.5)
        vert = DashedLine(corner, end, dash_length=0.12, color=DARK, stroke_width=2.5)
        diag = DashedLine(start, end, dash_length=0.12, color=AMBER, stroke_width=3.5)
        a = self.txt("A", 24, BOLD).next_to(start, DOWN + LEFT, buff=0.08)
        b = self.txt("B", 24, BOLD).next_to(end, UP, buff=0.08)
        lab_vt = self.mathtex(r"vt", 30).next_to(horiz, DOWN, buff=0.10)
        lab_l = self.mathtex(r"L", 30).next_to(vert, RIGHT, buff=0.10)
        lab_ct = self.mathtex(r"ct", 30, AMBER).move_to((start + end) / 2 + LEFT * 0.20 + UP * 0.18)
        key = self.text_box("Carlos también debe medir que la luz viaja a c.", 6.4, 0.88, 22, True)
        key.move_to(RIGHT * 2.85 + DOWN * 3.55)

        self.play(Create(horiz), Create(vert), Create(diag), FadeIn(a), FadeIn(b), Write(lab_vt), Write(lab_l), Write(lab_ct), run_time=RUN_SLOW)
        self.play(FadeIn(key), run_time=RUN_FAST)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 03 — Freeze geometry
    # -------------------------------------------------------------------------
    def freeze_triangle(self):
        h = self.header(
            3,
            "CONGELAMOS EL MOVIMIENTO: APARECE UN TRIÁNGULO RECTÁNGULO",
            "Altura L, avance horizontal vt y recorrido de la luz ct.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        A = np.array([-5.8, -2.15, 0])
        C = np.array([-1.25, -2.15, 0])
        B = np.array([-1.25, 2.05, 0])
        tri = Polygon(A, C, B, stroke_color=INK, stroke_width=3, fill_opacity=0)
        diag = Line(A, B, color=AMBER, stroke_width=6)
        right_mark = Square(side_length=0.38, stroke_color=INK, stroke_width=2, fill_opacity=0)
        right_mark.move_to(C + LEFT * 0.19 + UP * 0.19)
        label_l = self.mathtex(r"L=3.0\,\mathrm{m}", 29).next_to(Line(C, B), RIGHT, buff=0.16)
        label_vt = self.mathtex(r"vt=2.25\,\mathrm{m}", 29).next_to(Line(A, C), DOWN, buff=0.16)
        label_ct = self.mathtex(r"ct=3.75\,\mathrm{m}", 29, AMBER).move_to((A + B) / 2 + LEFT * 0.28 + UP * 0.08)
        dots = VGroup(Dot(A, radius=0.06, color=INK), Dot(B, radius=0.06, color=INK), Dot(C, radius=0.06, color=INK))

        pyth = VGroup(
            self.formula_box(r"(ct)^2=L^2+(vt)^2", 6.1, 1.08, 39),
            self.formula_box(r"(3.75)^2=(3.0)^2+(2.25)^2", 6.1, 1.08, 34),
            self.formula_box(r"14.0625=9+5.0625", 6.1, 1.08, 35),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.35 + DOWN * 0.25)
        note = self.note_box(
            "LA CLAVE",
            [
                "La luz recorre más distancia para Carlos.",
                "Pero su velocidad sigue siendo c.",
                "Entonces el tiempo medido no puede ser el mismo.",
            ],
            width=6.1,
            title_size=24,
            body_size=21,
        ).next_to(pyth, DOWN, buff=0.25)

        self.play(Create(tri), Create(diag), FadeIn(dots), FadeIn(right_mark), run_time=RUN_SLOW)
        self.play(Write(label_l), Write(label_vt), Write(label_ct), run_time=RUN)
        for box in pyth:
            self.play(FadeIn(box, shift=UP * 0.08), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_FAST)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 04 — Algebraic derivation
    # -------------------------------------------------------------------------
    def derive_time_dilation(self):
        h = self.header(
            4,
            "DERIVAMOS LA DILATACIÓN TEMPORAL PASO A PASO",
            "Usamos Pitágoras y la relación L = ct₀ medida en el marco del bus.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        steps = [
            r"(ct)^2=L^2+(vt)^2",
            r"(ct)^2=(ct_0)^2+(vt)^2",
            r"c^2t^2=c^2t_0^2+v^2t^2",
            r"t^2=t_0^2+\frac{v^2}{c^2}t^2",
            r"t^2\left(1-\frac{v^2}{c^2}\right)=t_0^2",
            r"t=\frac{t_0}{\sqrt{1-\frac{v^2}{c^2}}}",
        ]
        eqs = VGroup(*[self.mathtex(s, 40 if i < 5 else 46) for i, s in enumerate(steps)])
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.33)
        self.fit(eqs, 8.2, 5.9)
        eqs.move_to(LEFT * 2.6 + DOWN * 0.35)

        guide = self.note_box(
            "QUÉ HACEMOS EN CADA PASO",
            [
                "1. Escribimos Pitágoras.",
                "2. Sustituimos L = ct₀.",
                "3. Expandimos los cuadrados.",
                "4. Dividimos entre c².",
                "5. Agrupamos los términos con t.",
                "6. Despejamos t.",
            ],
            width=5.5,
            title_size=23,
            body_size=20,
        ).move_to(RIGHT * 4.55 + DOWN * 0.25)

        final_box = RoundedRectangle(
            width=8.4,
            height=1.05,
            corner_radius=0.10,
            stroke_color=INK,
            stroke_width=2.5,
            fill_color=PAPER,
            fill_opacity=1,
        ).move_to(eqs[-1])

        self.play(FadeIn(guide), run_time=RUN)
        for i, eq in enumerate(eqs):
            self.play(FadeIn(eq, shift=UP * 0.08), run_time=RUN_FAST)
            self.wait(PAUSE_READ if i < len(eqs) - 1 else PAUSE_EXPLAIN)
        self.play(Create(final_box), run_time=RUN_FAST)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 05 — Numerical substitution
    # -------------------------------------------------------------------------
    def calculate_bus_case(self):
        h = self.header(
            5,
            "SUSTITUIMOS v = 0.60c",
            "El factor temporal resulta 1.25: para Carlos, el mismo proceso tarda más.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        stack = VGroup(
            self.mathtex(r"t=\frac{t_0}{\sqrt{1-(0.60)^2}}", 42),
            self.mathtex(r"t=\frac{t_0}{\sqrt{1-0.36}}", 42),
            self.mathtex(r"t=\frac{t_0}{\sqrt{0.64}}", 42),
            self.mathtex(r"t=\frac{t_0}{0.80}", 42),
            self.mathtex(r"t=1.25t_0", 48),
        ).arrange(DOWN, buff=0.36, aligned_edge=LEFT).move_to(LEFT * 3.55 + DOWN * 0.20)
        self.fit(stack, 7.2, 5.4)

        cards = VGroup(
            self.clock_card("ANA · medio recorrido", r"t_0=10\,\mathrm{ns}", "piso → techo", 5.6),
            self.clock_card("CARLOS · medio recorrido", r"t=12.5\,\mathrm{ns}", "mismo pulso de luz", 5.6),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 3.95 + DOWN * 0.20)
        full_tick = self.text_box("Tic completo: Ana = 20 ns   •   Carlos = 25 ns", 6.2, 0.85, 21, True)
        full_tick.next_to(cards, DOWN, buff=0.28)

        for eq in stack:
            self.play(FadeIn(eq, shift=RIGHT * 0.08), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.play(FadeIn(cards[0]), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(cards[1]), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(full_tick), run_time=RUN_FAST)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 06 — Interpretation
    # -------------------------------------------------------------------------
    def interpret_result(self):
        h = self.header(
            6,
            "¿QUÉ SIGNIFICA EL RESULTADO?",
            "Carlos observa que el reloj que se mueve con el bus necesita más tiempo para cada tic.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        left = self.clock_card("MARCO DEL BUS · ANA", r"20\,\mathrm{ns}", "tic completo del reloj de luz", 5.7)
        right = self.clock_card("MARCO DE LA CARRETERA · CARLOS", r"25\,\mathrm{ns}", "ese mismo tic observado desde afuera", 5.7)
        left.move_to(LEFT * 3.45 + UP * 0.95)
        right.move_to(RIGHT * 3.45 + UP * 0.95)

        line_left = NumberLine(x_range=[0, 20, 5], length=5.2, include_numbers=True, font_size=20, color=INK)
        line_right = NumberLine(x_range=[0, 25, 5], length=5.2, include_numbers=True, font_size=20, color=INK)
        line_left.next_to(left, DOWN, buff=0.45)
        line_right.next_to(right, DOWN, buff=0.45)
        dot_left = Dot(line_left.n2p(0), radius=0.07, color=INK)
        dot_right = Dot(line_right.n2p(0), radius=0.07, color=INK)
        ns_l = self.txt("ns", 18, BOLD).next_to(line_left, RIGHT, buff=0.08)
        ns_r = self.txt("ns", 18, BOLD).next_to(line_right, RIGHT, buff=0.08)

        conclusion = self.text_box("EL RELOJ EN MOVIMIENTO FUNCIONA MÁS LENTAMENTE", 9.5, 0.95, 28, True)
        conclusion.move_to(DOWN * 3.20)
        sentence = self.txt("No es un defecto del reloj: el tiempo medido depende del observador.", 24, NORMAL, DARK)
        sentence.next_to(conclusion, UP, buff=0.30)

        self.play(FadeIn(left), FadeIn(right), run_time=RUN)
        self.play(Create(line_left), Create(line_right), FadeIn(dot_left), FadeIn(dot_right), FadeIn(ns_l), FadeIn(ns_r), run_time=RUN)
        self.play(
            dot_left.animate.move_to(line_left.n2p(20)),
            dot_right.animate.move_to(line_right.n2p(25)),
            run_time=RUN_MOTION,
            rate_func=linear,
        )
        self.play(FadeIn(sentence), FadeIn(conclusion), run_time=RUN)
        self.wait(PAUSE_SUMMARY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 07 — Classical conflict
    # -------------------------------------------------------------------------
    def classical_conflict(self):
        h = self.header(
            7,
            "LA CONTRADICCIÓN CON LA SUMA CLÁSICA DE VELOCIDADES",
            "Newton funciona para velocidades ordinarias, pero la luz no obedece una suma c + v.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        classical = self.note_box(
            "PREDICCIÓN CLÁSICA",
            [
                "velocidad respecto al suelo =",
                "velocidad respecto al bus + velocidad del bus",
            ],
            width=6.5,
            title_size=24,
            body_size=20,
        ).move_to(LEFT * 3.65 + UP * 1.15)
        false_eq = self.formula_box(r"c+0.60c=1.60c", 5.6, 1.05, 42)
        false_eq.next_to(classical, DOWN, buff=0.30)
        strike = Line(false_eq.get_left() + RIGHT * 0.25 + DOWN * 0.20, false_eq.get_right() + LEFT * 0.25 + UP * 0.20, color=INK, stroke_width=4)
        incorrect = self.txt("INCORRECTO PARA LA LUZ", 20, BOLD, DARK).next_to(false_eq, DOWN, buff=0.14)

        invariant = self.note_box(
            "LO QUE MIDEN ANA Y CARLOS",
            [
                "Ana mide c para la luz.",
                "Carlos también mide c.",
                "La velocidad de la luz permanece invariante.",
            ],
            width=6.4,
            title_size=24,
            body_size=21,
        ).move_to(RIGHT * 3.65 + UP * 1.15)
        cbox = self.formula_box(r"c=3.0\times10^8\,\mathrm{m/s}", 5.7, 1.05, 38)
        cbox.next_to(invariant, DOWN, buff=0.30)

        postulates = self.note_box(
            "EINSTEIN CONSERVA DOS IDEAS",
            [
                "1. Las leyes de la física son las mismas en marcos inerciales.",
                "2. Todos los observadores inerciales miden la misma c.",
                "Consecuencia: el tiempo no puede ser absoluto.",
            ],
            width=12.9,
            title_size=24,
            body_size=21,
            fill=PAPER,
        ).move_to(DOWN * 2.65)

        self.play(FadeIn(classical), run_time=RUN)
        self.play(FadeIn(false_eq), run_time=RUN_FAST)
        self.play(Create(strike), FadeIn(incorrect), run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(invariant), FadeIn(cbox), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(postulates), run_time=RUN)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 08 — Low-speed limit and gamma curve
    # -------------------------------------------------------------------------
    def low_speed_limit(self):
        h = self.header(
            8,
            "¿POR QUÉ NO NOTAMOS ESTO EN LA VIDA COTIDIANA?",
            "A bajas velocidades, el factor relativista es prácticamente 1; cerca de c crece rápidamente.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        axes = Axes(
            x_range=[0, 0.98, 0.2],
            y_range=[1, 5.2, 1],
            x_length=7.0,
            y_length=4.35,
            tips=False,
            axis_config={"color": INK, "stroke_width": 2},
        ).move_to(LEFT * 2.85 + DOWN * 0.45)
        curve = axes.plot(lambda x: 1 / np.sqrt(1 - x**2), x_range=[0.0, 0.98], color=INK, stroke_width=3)
        xlab = self.mathtex(r"\beta=\frac{v}{c}", 29).next_to(axes.x_axis, DOWN, buff=0.18).shift(RIGHT * 3.0)
        ylab = self.mathtex(r"\gamma", 32).next_to(axes.y_axis, UP, buff=0.10)
        marker = Dot(axes.c2p(0.60, 1.25), radius=0.08, color=AMBER)
        guide_x = DashedLine(axes.c2p(0.60, 1.0), axes.c2p(0.60, 1.25), color=AMBER, stroke_width=2)
        guide_y = DashedLine(axes.c2p(0.0, 1.25), axes.c2p(0.60, 1.25), color=AMBER, stroke_width=2)
        marker_lab = self.mathtex(r"(0.60,\ 1.25)", 26, AMBER).next_to(marker, UR, buff=0.12)

        notes = VGroup(
            self.formula_box(r"\gamma=\frac{1}{\sqrt{1-\frac{v^2}{c^2}}}", 5.8, 1.10, 39),
            self.note_box(
                "SI v ≪ c",
                [
                    "v²/c² es casi cero.",
                    "Entonces γ ≈ 1 y t ≈ t₀.",
                    "Newton es una excelente aproximación.",
                ],
                width=5.8,
                title_size=23,
                body_size=20,
            ),
            self.note_box(
                "SI v → c",
                [
                    "γ aumenta rápidamente.",
                    "La diferencia entre los tiempos se vuelve importante.",
                ],
                width=5.8,
                title_size=23,
                body_size=20,
            ),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.30 + DOWN * 0.25)

        self.play(Create(axes), Write(xlab), Write(ylab), run_time=RUN)
        self.play(Create(curve), run_time=RUN_SLOW * 1.3)
        self.play(Create(guide_x), Create(guide_y), FadeIn(marker), Write(marker_lab), run_time=RUN)
        for n in notes:
            self.play(FadeIn(n, shift=UP * 0.06), run_time=RUN_FAST)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_COPY)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 09 — Discussion prompt
    # -------------------------------------------------------------------------
    def discussion_question(self):
        h = self.header(
            9,
            "PREGUNTA FINAL PARA DISCUTIR",
            "Dos estudiantes sincronizan sus relojes, se separan y luego vuelven a encontrarse.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        earth = Circle(radius=1.05, stroke_color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1)
        earth.move_to(LEFT * 4.6 + DOWN * 0.20)
        earth_label = self.txt("TIERRA", 23, BOLD).move_to(earth)
        clock_earth = self.clock_card("ESTUDIANTE A", r"?", "permanece en la Tierra", 3.5).scale(0.82)
        clock_earth.next_to(earth, DOWN, buff=0.35)

        ship = RoundedRectangle(width=2.1, height=0.85, corner_radius=0.25, stroke_color=INK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1)
        ship.move_to(RIGHT * 4.55 + UP * 0.20)
        nose = Triangle(stroke_color=INK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1).scale(0.34).rotate(-PI / 2)
        nose.next_to(ship, RIGHT, buff=-0.05)
        ship_group = VGroup(ship, nose)
        ship_label = self.txt("VIAJE CERCA DE c", 21, BOLD).next_to(ship_group, UP, buff=0.20)
        clock_ship = self.clock_card("ESTUDIANTE B", r"?", "viaja y regresa", 3.5).scale(0.82)
        clock_ship.next_to(ship_group, DOWN, buff=0.40)

        outbound = CurvedArrow(earth.get_top() + RIGHT * 0.5, ship_group.get_top() + LEFT * 0.4, angle=-0.35, color=INK, stroke_width=3)
        inbound = CurvedArrow(ship_group.get_bottom() + LEFT * 0.4, earth.get_bottom() + RIGHT * 0.5, angle=-0.35, color=INK, stroke_width=3)

        question = self.text_box("CUANDO VUELVAN A ENCONTRARSE: ¿deberían sus relojes marcar exactamente el mismo tiempo?", 13.2, 1.05, 24, True)
        question.move_to(DOWN * 3.28)
        instruction = self.txt("Explica tu respuesta utilizando el reloj de luz del bus.", 22, NORMAL, DARK)
        instruction.next_to(question, UP, buff=0.24)

        self.play(FadeIn(earth), FadeIn(earth_label), FadeIn(clock_earth), run_time=RUN)
        self.play(FadeIn(ship_group), FadeIn(ship_label), FadeIn(clock_ship), run_time=RUN)
        self.play(Create(outbound), Create(inbound), run_time=RUN_SLOW)
        self.play(FadeIn(instruction), FadeIn(question), run_time=RUN)
        self.wait(PAUSE_FINAL)
        self.clear_scene()

    # -------------------------------------------------------------------------
    # 10 — Summary / reproducible reasoning map
    # -------------------------------------------------------------------------
    def summary(self):
        h = self.header(
            10,
            "IDEA CENTRAL: QUÉ DEBE PODER REPRODUCIR EL ESTUDIANTE",
            "La dilatación temporal aparece al exigir que ambos observadores midan la misma velocidad de la luz.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        labels = [
            ("1", "ANA: luz vertical"),
            ("2", "CARLOS: luz diagonal"),
            ("3", "Pitágoras"),
            ("4", "L = ct₀"),
            ("5", "Despejar t"),
            ("6", "v = 0.60c → 1.25"),
        ]
        cards = VGroup()
        for num, text in labels:
            box = RoundedRectangle(
                width=4.20,
                height=1.15,
                corner_radius=0.11,
                stroke_color=DARK,
                stroke_width=1.7,
                fill_color=WHITE,
                fill_opacity=1,
            )
            nbox = RoundedRectangle(
                width=0.58,
                height=0.58,
                corner_radius=0.08,
                stroke_color=INK,
                stroke_width=1.7,
                fill_color=PAPER,
                fill_opacity=1,
            )
            ntext = self.txt(num, 21, BOLD).move_to(nbox)
            label = self.fit(self.txt(text, 21, BOLD), 3.18, 0.62)
            row = VGroup(VGroup(nbox, ntext), label).arrange(RIGHT, buff=0.20).move_to(box)
            cards.add(VGroup(box, row))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.34, 0.36)).move_to(UP * 0.55)

        formula = self.formula_box(r"t=\frac{t_0}{\sqrt{1-\frac{v^2}{c^2}}}", 7.1, 1.12, 42)
        formula.move_to(DOWN * 1.75)
        result = self.formula_box(r"10\,\mathrm{ns}\longrightarrow12.5\,\mathrm{ns}\quad(v=0.60c)", 8.4, 1.05, 35)
        result.next_to(formula, DOWN, buff=0.30)
        close = self.text_box("Newton funciona muy bien cuando v ≪ c. Cerca de c, el tiempo deja de ser absoluto.", 12.5, 0.92, 23, True, fill=PAPER)
        close.next_to(result, DOWN, buff=0.30)

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.12), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(close), run_time=RUN)
        self.wait(PAUSE_FINAL)


# Preview:
#   manim -pql physics9_bus_light_clock_v1.py Physics9BusLightClockV1 --disable_caching
# Final:
#   manim -pqh physics9_bus_light_clock_v1.py Physics9BusLightClockV1 --disable_caching
