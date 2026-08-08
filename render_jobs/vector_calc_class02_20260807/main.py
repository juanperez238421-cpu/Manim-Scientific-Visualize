#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vector Calculus — Class 02: Surfaces in R^3.

Protocol target
---------------
Manim Community Edition 0.20.1
Final command:
    manim -pqh main.py VectorCalculusSurfacesClass02Detailed \
        --format=mp4 --disable_caching

Design rules
------------
- 1920×1080, 30 fps, 16:9.
- White background, black/neutral-gray visual system.
- Stable 3D camera: no ambient rotation and no camera animation while explaining.
- Fixed-frame text and mathematics; 3D geometry stays in a dedicated left region.
- Every surface is built progressively from algebra → traces → repeated sections → surface.
- Every explicit animation is followed by a pedagogical pause.
"""
from __future__ import annotations

import math
import os
from typing import Callable, Iterable, Sequence

import numpy as np
from manim import *


config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#747474"
LIGHT_GRAY = "#D2D2D2"
VERY_LIGHT_GRAY = "#ECECEC"
PAPER_GRAY = "#F7F7F7"
WHITE_FILL = WHITE

FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.8
SAFE_HEIGHT = 7.65

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_QUICK = 0.65
RUN_NORMAL = 0.95
RUN_SLOW = 1.25

PAUSE_TINY = 0.45
PAUSE_SHORT = 0.90
PAUSE_READ = 1.65
PAUSE_EXPLAIN = 2.40
PAUSE_CONNECT = 3.00
PAUSE_WORK = 3.80
PAUSE_SUMMARY = 4.40
PAUSE_FINAL = 5.20


class VectorCalculusSurfacesClass02Detailed(ThreeDScene):
    """Detailed, stable-camera lesson on cylindrical and quadric surfaces."""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE
        self._section_fixed: list[Mobject] = []

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def paced_play(self, *animations, run_time=RUN_NORMAL, pause=PAUSE_SHORT, **kwargs):
        self.play(*animations, run_time=run_time, **kwargs)
        self.wait(pause)

    def text(self, content: str, size: int = 28, weight=NORMAL, **kwargs) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight, line_spacing=0.92, **kwargs)

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(self, mob: Mobject, max_width: float, max_height: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def register_fixed(self, *mobs: Mobject) -> None:
        for mob in mobs:
            self.add_fixed_in_frame_mobjects(mob)
            self._section_fixed.append(mob)

    def make_header(self, number: int, title: str, subtitle: str) -> VGroup:
        number_box = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE_FILL, fill_opacity=1.0)
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)
        title_text = self.fit(self.text(title, 33, BOLD), 13.45, 0.54)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.15).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.065)
        words = subtitle.split()
        if len(subtitle) > 82:
            target = len(subtitle) / 2
            running = 0
            split = 1
            for i, word in enumerate(words[:-1], start=1):
                running += len(word) + 1
                if running >= target:
                    split = i
                    break
            sub = VGroup(self.text(" ".join(words[:split]), 19), self.text(" ".join(words[split:]), 19)).arrange(DOWN, aligned_edge=LEFT, buff=0.025)
        else:
            sub = self.text(subtitle, 20)
        self.fit(sub, 14.25, 0.68)
        sub.next_to(rule, DOWN, buff=0.065).align_to(title_row, LEFT)
        group = VGroup(title_row, rule, sub)
        self.register_fixed(group)
        self.add(group)
        return group

    def formula_panel(self, expression: str, *, title: str = "ECUACIÓN", y: float = 2.30, width: float = 5.55, font_size: int = 36) -> VGroup:
        title_mob = self.text(title, 20, BOLD)
        equation = self.fit(self.math(expression, font_size), width - 0.55, 0.72)
        content = VGroup(title_mob, equation).arrange(DOWN, buff=0.13)
        box = RoundedRectangle(width=width, height=max(1.25, content.height + 0.42), corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=PAPER_GRAY, fill_opacity=1.0)
        content.move_to(box)
        group = VGroup(box, content).move_to([4.25, y, 0])
        self.register_fixed(group)
        return group

    def step_panel(self, step: str, title: str, lines: Sequence[str], *, y: float = -0.15, width: float = 5.55, body_size: int = 21) -> VGroup:
        chip_box = RoundedRectangle(width=1.12, height=0.40, corner_radius=0.08, stroke_color=BLACK_LINE, stroke_width=1.4, fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
        chip_text = self.text(step, 17, BOLD).move_to(chip_box)
        title_mob = self.text(title, 24, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.115)
        head = VGroup(VGroup(chip_box, chip_text), title_mob).arrange(RIGHT, buff=0.18)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        self.fit(content, width - 0.50, 2.55)
        box = RoundedRectangle(width=width, height=max(1.45, content.height + 0.48), corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=1.45, fill_color=WHITE_FILL, fill_opacity=1.0)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        group = VGroup(box, content).move_to([4.25, y, 0])
        self.register_fixed(group)
        return group

    def term_panel(self, entries: Sequence[tuple[str, str]], *, y=-2.55, width=5.55) -> VGroup:
        rows = VGroup()
        for symbol, meaning in entries:
            s = self.math(symbol, 27)
            m = self.text(meaning, 19)
            self.fit(m, 3.75, 0.45)
            row = VGroup(s, m).arrange(RIGHT, buff=0.20)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        self.fit(rows, width - 0.5, 1.75)
        box = RoundedRectangle(width=width, height=max(1.15, rows.height + 0.40), corner_radius=0.10, stroke_color=LIGHT_GRAY, stroke_width=1.3, fill_color=WHITE_FILL, fill_opacity=1.0)
        rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        group = VGroup(box, rows).move_to([4.25, y, 0])
        self.register_fixed(group)
        return group

    def replace_fixed_panel(self, old: VGroup, new: VGroup, pause=PAUSE_READ) -> VGroup:
        self.remove(new)
        self.paced_play(ReplacementTransform(old, new), run_time=RUN_QUICK, pause=pause)
        return new

    def set_stable_camera(self) -> None:
        self.set_camera_orientation(phi=67 * DEGREES, theta=-52 * DEGREES, zoom=0.82)

    def axes3d(self) -> ThreeDAxes:
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-4, 4, 1], x_length=6.15, y_length=6.15, z_length=5.2, axis_config={"color": BLACK_LINE, "stroke_width": 1.45, "include_ticks": False, "include_tip": True})
        axes.shift(LEFT * 2.65 + DOWN * 0.35)
        return axes

    def axis_labels(self, axes: ThreeDAxes) -> VGroup:
        return axes.get_axis_labels(self.math("x", 26), self.math("y", 26), self.math("z", 26))

    def style_surface(self, surface: Surface, opacity=0.34) -> Surface:
        surface.set_style(fill_opacity=opacity, stroke_color=MID_GRAY, stroke_width=0.48)
        surface.set_fill(LIGHT_GRAY, opacity=opacity)
        return surface

    def trace_curve(self, axes: ThreeDAxes, fn: Callable[[float], np.ndarray], t0=0, t1=TAU, width=3.0):
        return ParametricFunction(lambda t: axes.c2p(*fn(t)), t_range=[t0, t1], color=BLACK_LINE, stroke_width=width)

    def horizontal_plane(self, axes: ThreeDAxes, z_value: float) -> Surface:
        plane = Surface(lambda u, v: axes.c2p(u, v, z_value), u_range=[-3.4, 3.4], v_range=[-3.4, 3.4], resolution=(2, 2))
        plane.set_style(fill_opacity=0.09, stroke_color=LIGHT_GRAY, stroke_width=0.3)
        plane.set_fill(VERY_LIGHT_GRAY, opacity=0.16)
        return plane

    def clear_section(self) -> None:
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=RUN_NORMAL)
        self.clear()
        self._section_fixed.clear()
        self.wait(PAUSE_SHORT)

    def build_circular_cylinder(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        base = self.trace_curve(axes, lambda t: np.array([2*np.cos(t), 2*np.sin(t), 0]))
        self.paced_play(Create(base), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step2 = self.step_panel("PASO 2", "DEJAR z LIBRE", ["La ecuación no restringe z.", "Para cualquier z = k aparece el mismo círculo."])
        step = self.replace_fixed_panel(step, step2)
        slices = VGroup()
        for z in (-2.4, -1.2, 1.2, 2.4):
            c = self.trace_curve(axes, lambda t, z=z: np.array([2*np.cos(t), 2*np.sin(t), z]), width=2.0)
            slices.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        step3 = self.step_panel("PASO 3", "MOSTRAR GENERATRICES", ["El mismo punto (x,y) se desplaza paralelo al eje z.", "Esas rectas forman la dirección del cilindro."])
        step = self.replace_fixed_panel(step, step3)
        generators = VGroup()
        for angle in (0, PI/2, PI, 3*PI/2):
            x, y = 2*np.cos(angle), 2*np.sin(angle)
            line = Line3D(axes.c2p(x, y, -2.8), axes.c2p(x, y, 2.8), color=DARK_GRAY, thickness=0.012)
            generators.add(line)
            self.paced_play(Create(line), run_time=RUN_QUICK, pause=PAUSE_TINY)
        step4 = self.step_panel("PASO 4", "CERRAR LA SUPERFICIE", ["Todas las copias del círculo llenan una pared continua.", "Resultado: cilindro circular paralelo a z."])
        step = self.replace_fixed_panel(step, step4)
        surf = Surface(lambda u, v: axes.c2p(2*np.cos(u), 2*np.sin(u), v), u_range=[0, TAU], v_range=[-2.8, 2.8], resolution=(30, 16))
        self.style_surface(surf, opacity=0.30)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(base, slices, generators, surf)

    def build_parabolic_cylinder(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        curve = self.trace_curve(axes, lambda t: np.array([t, (t**2)/2.25, 0]), t0=-2.3, t1=2.3, width=3.0)
        self.paced_play(Create(curve), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step2 = self.step_panel("PASO 2", "IDENTIFICAR LA VARIABLE AUSENTE", ["z no aparece.", "La parábola no cambia cuando z toma otros valores."])
        step = self.replace_fixed_panel(step, step2)
        copies = VGroup()
        for z in (-2.2, -1.1, 1.1, 2.2):
            c = self.trace_curve(axes, lambda t, z=z: np.array([t, (t**2)/2.25, z]), t0=-2.3, t1=2.3, width=1.8)
            copies.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        step3 = self.step_panel("PASO 3", "EXTRUIR LA PARÁBOLA", ["Cada punto de la parábola genera una recta paralela a z.", "La extrusión produce un cilindro parabólico."])
        step = self.replace_fixed_panel(step, step3)
        surf = Surface(lambda u, v: axes.c2p(u, (u**2)/2.25, v), u_range=[-2.3, 2.3], v_range=[-2.5, 2.5], resolution=(24, 16))
        self.style_surface(surf, opacity=0.30)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(curve, copies, surf)

    def build_ellipsoid_progressive(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        xy = self.trace_curve(axes, lambda t: np.array([3*np.cos(t), 2*np.sin(t), 0]))
        self.paced_play(Create(xy), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step2 = self.step_panel("PASO 2", "SEGUNDA TRAZA: x = 0", ["Queda y²/4 + z²/3 = 1.", "Otra elipse, ahora en el plano yz."])
        step = self.replace_fixed_panel(step, step2)
        yz = self.trace_curve(axes, lambda t: np.array([0, 2*np.cos(t), math.sqrt(3)*np.sin(t)]))
        self.paced_play(Create(yz), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step3 = self.step_panel("PASO 3", "TERCERA TRAZA: y = 0", ["Queda x²/9 + z²/3 = 1.", "Las tres trazas son cerradas y acotadas."])
        step = self.replace_fixed_panel(step, step3)
        xz = self.trace_curve(axes, lambda t: np.array([3*np.cos(t), 0, math.sqrt(3)*np.sin(t)]))
        self.paced_play(Create(xz), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step4 = self.step_panel("PASO 4", "INTERPOLAR LAS TRAZAS", ["Las secciones se deforman suavemente entre los interceptos.", "La superficie resultante es cerrada: un elipsoide."])
        step = self.replace_fixed_panel(step, step4)
        surf = Surface(lambda u, v: axes.c2p(3*np.cos(u)*np.sin(v), 2*np.sin(u)*np.sin(v), math.sqrt(3)*np.cos(v)), u_range=[0, TAU], v_range=[0, PI], resolution=(30, 18))
        self.style_surface(surf, opacity=0.31)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(xy, yz, xz, surf)

    def build_hyperboloid_one_sheet(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        waist = self.trace_curve(axes, lambda t: np.array([2*np.cos(t), math.sqrt(2)*np.sin(t), 0]))
        self.paced_play(Create(waist), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step2 = self.step_panel("PASO 2", "AUMENTAR |z|", ["Si z = k, los denominadores no cambian.", "El lado derecho efectivo crece: la elipse se ensancha."])
        step = self.replace_fixed_panel(step, step2)
        slices = VGroup()
        for z in (-2.0, -1.0, 1.0, 2.0):
            factor = math.sqrt(1 + (z*z)/4)
            c = self.trace_curve(axes, lambda t, z=z, factor=factor: np.array([2*factor*np.cos(t), math.sqrt(2)*factor*np.sin(t), z]), width=1.9)
            slices.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        step3 = self.step_panel("PASO 3", "RECONOCER EL EJE", ["El término negativo es −z²/4.", "La cintura está en z = 0 y la superficie se abre en ±z."])
        step = self.replace_fixed_panel(step, step3)
        surf = Surface(lambda u, v: axes.c2p(2*np.cosh(v)*np.cos(u), math.sqrt(2)*np.cosh(v)*np.sin(u), 2*np.sinh(v)), u_range=[0, TAU], v_range=[-1.0, 1.0], resolution=(30, 18))
        self.style_surface(surf, opacity=0.30)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(waist, slices, surf)

    def build_two_sheet_hyperboloid(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        plane = self.horizontal_plane(axes, 0)
        self.paced_play(FadeIn(plane), run_time=RUN_NORMAL, pause=PAUSE_READ)
        step2 = self.step_panel("PASO 2", "BUSCAR EL PRIMER PUNTO REAL", ["z²/4 = 1 + x²/4 + y²/4 ≥ 1.", "Por tanto |z| ≥ 2: existe un hueco alrededor de z = 0."])
        step = self.replace_fixed_panel(step, step2)
        p_top = Dot3D(axes.c2p(0, 0, 2), radius=0.07, color=BLACK)
        p_bottom = Dot3D(axes.c2p(0, 0, -2), radius=0.07, color=BLACK)
        self.paced_play(FadeIn(p_top), FadeIn(p_bottom), run_time=RUN_NORMAL, pause=PAUSE_EXPLAIN)
        step3 = self.step_panel("PASO 3", "ABRIR DOS RAMAS", ["Cuando |z| aumenta, aparecen elipses cada vez mayores.", "Las ramas superior e inferior nunca se conectan."])
        step = self.replace_fixed_panel(step, step3)
        slices = VGroup()
        for z in (-3.0, -2.5, 2.5, 3.0):
            r = 2*math.sqrt((z*z)/4 - 1)
            c = self.trace_curve(axes, lambda t, z=z, r=r: np.array([r*np.cos(t), r*np.sin(t), z]), width=1.9)
            slices.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        top = Surface(lambda u, v: axes.c2p(2*np.sinh(v)*np.cos(u), 2*np.sinh(v)*np.sin(u), 2*np.cosh(v)), u_range=[0, TAU], v_range=[0, 1.0], resolution=(26, 14))
        bot = Surface(lambda u, v: axes.c2p(2*np.sinh(v)*np.cos(u), 2*np.sinh(v)*np.sin(u), -2*np.cosh(v)), u_range=[0, TAU], v_range=[0, 1.0], resolution=(26, 14))
        self.style_surface(top, opacity=0.30); self.style_surface(bot, opacity=0.30)
        self.paced_play(FadeIn(top), FadeIn(bot), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(plane, p_top, p_bottom, slices, top, bot)

    def build_cone(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        apex = Dot3D(axes.c2p(0,0,0), radius=0.07, color=BLACK)
        self.paced_play(FadeIn(apex), run_time=RUN_NORMAL, pause=PAUSE_READ)
        step2 = self.step_panel("PASO 2", "CORTES HORIZONTALES", ["z² = x² + y².", "Para z = k, el radio es |k|: círculos que crecen linealmente."])
        step = self.replace_fixed_panel(step, step2)
        slices = VGroup()
        for z in (-2.4, -1.2, 1.2, 2.4):
            r = abs(z)
            c = self.trace_curve(axes, lambda t, z=z, r=r: np.array([r*np.cos(t), r*np.sin(t), z]), width=1.8)
            slices.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        step3 = self.step_panel("PASO 3", "UNIR CON EL VÉRTICE", ["Todas las secciones colapsan en (0,0,0).", "Se forman dos nappes: una para z>0 y otra para z<0."])
        step = self.replace_fixed_panel(step, step3)
        surf = Surface(lambda u, v: axes.c2p(abs(v)*np.cos(u), abs(v)*np.sin(u), v), u_range=[0, TAU], v_range=[-2.7, 2.7], resolution=(28, 18))
        self.style_surface(surf, opacity=0.28)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(apex, slices, surf)

    def build_elliptic_paraboloid(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        vertex = Dot3D(axes.c2p(0,0,0), radius=0.07, color=BLACK)
        self.paced_play(FadeIn(vertex), run_time=RUN_NORMAL, pause=PAUSE_READ)
        step2 = self.step_panel("PASO 2", "TRAZAS z = k", ["k = x²/4 + y²/4 exige k ≥ 0.", "Cada k positivo produce un círculo de radio 2√k."])
        step = self.replace_fixed_panel(step, step2)
        slices = VGroup()
        for z in (0.45, 1.0, 1.8, 2.6):
            r = 2*math.sqrt(z)
            c = self.trace_curve(axes, lambda t, z=z, r=r: np.array([r*np.cos(t), r*np.sin(t), z]), width=1.8)
            slices.add(c)
            self.paced_play(Create(c), run_time=RUN_QUICK, pause=PAUSE_SHORT)
        step3 = self.step_panel("PASO 3", "TRAZAS VERTICALES", ["x = 0 o y = 0 deja una parábola.", "Todas abren hacia +z: la superficie es una copa."])
        step = self.replace_fixed_panel(step, step3)
        vertical = self.trace_curve(axes, lambda t: np.array([2*t, 0, t*t]), t0=-1.7, t1=1.7, width=2.7)
        self.paced_play(Create(vertical), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        surf = Surface(lambda u, v: axes.c2p(2*v*np.cos(u), 2*v*np.sin(u), v*v), u_range=[0, TAU], v_range=[0, 1.7], resolution=(28, 16))
        self.style_surface(surf, opacity=0.30)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(vertex, slices, vertical, surf)

    def build_hyperbolic_paraboloid(self, axes: ThreeDAxes, step: VGroup) -> VGroup:
        l1 = ParametricFunction(lambda t: axes.c2p(t, t, 0), t_range=[-2.5,2.5], color=BLACK, stroke_width=2.5)
        l2 = ParametricFunction(lambda t: axes.c2p(t, -t, 0), t_range=[-2.5,2.5], color=BLACK, stroke_width=2.5)
        self.paced_play(Create(l1), Create(l2), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step2 = self.step_panel("PASO 2", "TRAZA y = 0", ["z = x²/4.", "Parábola que abre hacia +z."])
        step = self.replace_fixed_panel(step, step2)
        pos = self.trace_curve(axes, lambda t: np.array([t,0,(t*t)/4]), t0=-2.7,t1=2.7,width=2.8)
        self.paced_play(Create(pos), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        step3 = self.step_panel("PASO 3", "TRAZA x = 0", ["z = −y²/4.", "Parábola que abre hacia −z: aparece la silla."])
        step = self.replace_fixed_panel(step, step3)
        neg = self.trace_curve(axes, lambda t: np.array([0,t,-(t*t)/4]), t0=-2.7,t1=2.7,width=2.8)
        self.paced_play(Create(neg), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        surf = Surface(lambda u,v: axes.c2p(u,v,(u*u-v*v)/4), u_range=[-2.7,2.7], v_range=[-2.7,2.7], resolution=(22,22))
        self.style_surface(surf, opacity=0.29)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_WORK)
        return VGroup(l1,l2,pos,neg,surf)

    def opening(self) -> None:
        course = self.text("CÁLCULO VECTORIAL · CLASE 02", 28, BOLD)
        title = self.text("SUPERFICIES EN R³", 52, BOLD)
        rule = Line(LEFT*5.25, RIGHT*5.25, color=BLACK_LINE, stroke_width=2)
        subtitle = self.text("Superficies cilíndricas y superficies cuádricas", 28)
        method = self.text("Ecuación → trazas → construcción progresiva → clasificación", 23, MEDIUM)
        group = VGroup(course, title, rule, subtitle, method).arrange(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(group)
        self.paced_play(FadeIn(course, shift=UP*0.12), run_time=RUN_NORMAL, pause=PAUSE_SHORT)
        self.paced_play(Write(title), Create(rule), run_time=RUN_SLOW, pause=PAUSE_READ)
        self.paced_play(FadeIn(subtitle), run_time=RUN_NORMAL, pause=PAUSE_EXPLAIN)
        self.paced_play(FadeIn(method), run_time=RUN_NORMAL, pause=PAUSE_FINAL)
        self.play(FadeOut(group), run_time=RUN_NORMAL); self.clear()

    def vocabulary_and_traces(self) -> None:
        self.make_header(1, "VOCABULARIO: ¿QUÉ REPRESENTA UNA SUPERFICIE?", "Antes de clasificar una ecuación, conecte cada símbolo con una idea geométrica en R³.")
        formula = self.formula_panel(r"F(x,y,z)=0", title="FORMA IMPLÍCITA")
        step = self.step_panel("IDEA 1", "SUPERFICIE", ["Es el conjunto de puntos (x,y,z) que satisface una relación.", "Una ecuación puede describir infinitos puntos en el espacio."])
        terms = self.term_panel([(r"x,y,z", "coordenadas del punto"), (r"F", "relación que deben satisfacer"), (r"F=0", "condición implícita")])
        self.paced_play(FadeIn(formula), FadeIn(step), FadeIn(terms), pause=PAUSE_CONNECT)
        step2 = self.step_panel("IDEA 2", "TRAZA", ["Una traza es una intersección con un plano coordenado.", "Fijar z=k convierte la ecuación 3D en una curva 2D."])
        step = self.replace_fixed_panel(step, step2, pause=PAUSE_EXPLAIN)
        self.set_stable_camera(); axes = self.axes3d(); labels = self.axis_labels(axes)
        self.paced_play(Create(axes), FadeIn(labels), run_time=RUN_SLOW, pause=PAUSE_READ)
        surf = Surface(lambda u,v: axes.c2p(3*np.cos(u)*np.sin(v), 2*np.sin(u)*np.sin(v), math.sqrt(3)*np.cos(v)), u_range=[0,TAU], v_range=[0,PI], resolution=(28,16))
        self.style_surface(surf, opacity=0.24)
        self.paced_play(FadeIn(surf), run_time=RUN_SLOW, pause=PAUSE_READ)
        plane = self.horizontal_plane(axes, 0)
        trace = self.trace_curve(axes, lambda t: np.array([3*np.cos(t),2*np.sin(t),0]))
        step3 = self.step_panel("IDEA 3", "EJEMPLO: z = 0", ["Sustituir z=0 deja x²/9 + y²/4 = 1.", "La intersección es una elipse en el plano xy."])
        step = self.replace_fixed_panel(step, step3)
        self.paced_play(FadeIn(plane), run_time=RUN_NORMAL, pause=PAUSE_READ)
        self.paced_play(Create(trace), run_time=RUN_SLOW, pause=PAUSE_CONNECT)
        self.clear_section()

    def cylindrical_surfaces(self) -> None:
        self.make_header(2, "SUPERFICIES CILÍNDRICAS: LA REGLA DE LA VARIABLE AUSENTE", "Si una variable no aparece, la curva generatriz se repite en la dirección de esa variable.")
        formula = self.formula_panel(r"x^2+y^2=4")
        step = self.step_panel("PASO 1", "CONSTRUIR LA TRAZA 2D", ["En z=0: x²+y²=4.", "Es un círculo de radio 2 en el plano xy."])
        terms = self.term_panel([(r"x^2+y^2", "distancia radial al eje z"), (r"4=2^2", "radio al cuadrado"), (r"z", "no aparece → dirección libre")])
        self.paced_play(FadeIn(formula), FadeIn(step), FadeIn(terms), pause=PAUSE_READ)
        self.set_stable_camera(); axes = self.axes3d(); labels = self.axis_labels(axes)
        self.paced_play(Create(axes), FadeIn(labels), run_time=RUN_SLOW, pause=PAUSE_READ)
        self.build_circular_cylinder(axes, step); self.clear_section()
        self.make_header(3, "SEGUNDO EJEMPLO: CILINDRO PARABÓLICO", "La curva generatriz no tiene que ser un círculo; la misma regla funciona con cualquier curva plana.")
        formula = self.formula_panel(r"y=\frac{x^2}{2.25}")
        step = self.step_panel("PASO 1", "DIBUJAR LA PARÁBOLA", ["En z=0 aparece una parábola en el plano xy.", "El vértice está en el origen y abre hacia +y."])
        terms = self.term_panel([(r"x^2", "genera curvatura parabólica"), (r"y", "variable dependiente en la traza"), (r"z", "ausente → extrusión paralela a z")])
        self.paced_play(FadeIn(formula), FadeIn(step), FadeIn(terms), pause=PAUSE_READ)
        self.set_stable_camera(); axes = self.axes3d(); labels=self.axis_labels(axes)
        self.paced_play(Create(axes), FadeIn(labels), run_time=RUN_SLOW, pause=PAUSE_READ)
        self.build_parabolic_cylinder(axes, step); self.clear_section()

    def quadric_language(self) -> None:
        self.make_header(4, "SUPERFICIES CUÁDRICAS: LEER EL POLINOMIO ANTES DE GRAFICAR", "Una cuádrica proviene de una ecuación de grado total 2; completar cuadrados y normalizar revela su familia.")
        equation = self.math(r"Ax^2+By^2+Cz^2+Dx+Ey+Fz+G=0", 44); self.register_fixed(equation); equation.move_to(UP*1.7)
        self.paced_play(Write(equation), run_time=RUN_SLOW, pause=PAUSE_EXPLAIN)
        definitions = VGroup(self.text("A, B, C: controlan los términos cuadrados y sus signos", 23), self.text("D, E, F: desplazan el centro o el vértice al completar cuadrados", 23), self.text("G: fija el nivel o término constante", 23)).arrange(DOWN, aligned_edge=LEFT, buff=0.20).move_to(UP*0.15)
        self.register_fixed(definitions)
        for line in definitions: self.paced_play(FadeIn(line, shift=RIGHT*0.10), run_time=RUN_NORMAL, pause=PAUSE_READ)
        recipe = VGroup(self.text("1. COMPLETAR CUADRADOS", 22, BOLD), self.text("2. DIVIDIR PARA OBTENER 1 O 0", 22, BOLD), self.text("3. CONTAR CUADRADOS Y COMPARAR SIGNOS", 22, BOLD), self.text("4. VERIFICAR CON TRAZAS", 22, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN*2.0)
        self.register_fixed(recipe)
        for line in recipe: self.paced_play(FadeIn(line, shift=UP*0.08), run_time=RUN_NORMAL, pause=PAUSE_SHORT)
        self.wait(PAUSE_SUMMARY); self.clear_section()

    def ellipsoid_section(self) -> None:
        self.make_header(5, "ELIPSOIDE: TRES CUADRADOS CON EL MISMO SIGNO", "Los denominadores determinan los semiejes; las tres trazas coordenadas son elipses cerradas.")
        formula = self.formula_panel(r"\frac{x^2}{9}+\frac{y^2}{4}+\frac{z^2}{3}=1")
        step = self.step_panel("PASO 1", "PRIMERA TRAZA: z = 0", ["Queda x²/9 + y²/4 = 1.", "Semiejes: 3 en x y 2 en y."])
        terms = self.term_panel([(r"9=3^2", "semieje sobre x"), (r"4=2^2", "semieje sobre y"), (r"3=(\sqrt3)^2", "semieje sobre z")])
        self.paced_play(FadeIn(formula), FadeIn(step), FadeIn(terms), pause=PAUSE_READ)
        self.set_stable_camera(); axes=self.axes3d(); labels=self.axis_labels(axes)
        self.paced_play(Create(axes), FadeIn(labels), run_time=RUN_SLOW, pause=PAUSE_READ)
        self.build_ellipsoid_progressive(axes, step); self.clear_section()

    def hyperboloids_and_cone(self) -> None:
        self.make_header(6, "HIPERBOLOIDE DE UNA HOJA: UN SIGNO DIFERENTE", "La superficie permanece conectada; el término con signo diferente identifica el eje característico.")
        formula=self.formula_panel(r"\frac{x^2}{4}+\frac{y^2}{2}-\frac{z^2}{4}=1")
        step=self.step_panel("PASO 1", "LOCALIZAR LA CINTURA", ["Con z=0 queda x²/4 + y²/2 = 1.", "Esta elipse es la sección mínima de la superficie."])
        terms=self.term_panel([(r"+,+,-", "dos signos iguales y uno diferente"), (r"-z^2/4", "eje característico: z"), (r"=1", "superficie conectada")])
        self.paced_play(FadeIn(formula),FadeIn(step),FadeIn(terms),pause=PAUSE_READ)
        self.set_stable_camera(); axes=self.axes3d();labels=self.axis_labels(axes)
        self.paced_play(Create(axes),FadeIn(labels),run_time=RUN_SLOW,pause=PAUSE_READ)
        self.build_hyperboloid_one_sheet(axes,step); self.clear_section()
        self.make_header(7, "HIPERBOLOIDE DE DOS HOJAS: EL HUECO CENTRAL", "Dos términos tienen signo negativo y el término positivo aislado determina el eje de las dos ramas.")
        formula=self.formula_panel(r"\frac{z^2}{4}-\frac{x^2}{4}-\frac{y^2}{4}=1")
        step=self.step_panel("PASO 1", "PROBAR z = 0", ["Se obtiene −x²/4 − y²/4 = 1.", "No existen puntos reales: el plano z=0 no corta la superficie."])
        terms=self.term_panel([(r"+,-,-", "un término positivo aislado"), (r"z^2/4", "eje de las dos hojas"), (r"|z|\ge2", "separación mínima respecto al origen")])
        self.paced_play(FadeIn(formula),FadeIn(step),FadeIn(terms),pause=PAUSE_READ)
        self.set_stable_camera(); axes=self.axes3d();labels=self.axis_labels(axes)
        self.paced_play(Create(axes),FadeIn(labels),run_time=RUN_SLOW,pause=PAUSE_READ)
        self.build_two_sheet_hyperboloid(axes,step); self.clear_section()
        self.make_header(8, "CONO ELÍPTICO: EL MISMO PATRÓN, PERO IGUALADO A CERO", "Cuando los términos cuadrados con signos opuestos se igualan a 0, las ramas se encuentran en un vértice.")
        formula=self.formula_panel(r"z^2-x^2-y^2=0")
        step=self.step_panel("PASO 1", "ENCONTRAR EL VÉRTICE", ["x=y=z=0 satisface la ecuación.", "Todas las secciones horizontales se contraen hasta el origen."])
        terms=self.term_panel([(r"z^2", "controla la altura"), (r"x^2+y^2", "radio radial"), (r"=0", "las dos nappes se tocan en el vértice")])
        self.paced_play(FadeIn(formula),FadeIn(step),FadeIn(terms),pause=PAUSE_READ)
        self.set_stable_camera();axes=self.axes3d();labels=self.axis_labels(axes)
        self.paced_play(Create(axes),FadeIn(labels),run_time=RUN_SLOW,pause=PAUSE_READ)
        self.build_cone(axes,step); self.clear_section()

    def paraboloids_section(self) -> None:
        self.make_header(9, "PARABOLOIDE ELÍPTICO: UNA VARIABLE LINEAL Y CUADRADOS DEL MISMO SIGNO", "Las trazas horizontales son elipses; las verticales son parábolas que abren en la dirección de la variable lineal.")
        formula=self.formula_panel(r"z=\frac{x^2}{4}+\frac{y^2}{4}")
        step=self.step_panel("PASO 1", "LOCALIZAR EL VÉRTICE", ["El valor mínimo es z=0 cuando x=y=0.", "El vértice está en el origen."])
        terms=self.term_panel([(r"z", "variable lineal → eje de apertura"), (r"+x^2,+y^2", "mismo signo → copa"), (r"z\ge0", "la superficie abre hacia +z")])
        self.paced_play(FadeIn(formula),FadeIn(step),FadeIn(terms),pause=PAUSE_READ)
        self.set_stable_camera();axes=self.axes3d();labels=self.axis_labels(axes)
        self.paced_play(Create(axes),FadeIn(labels),run_time=RUN_SLOW,pause=PAUSE_READ)
        self.build_elliptic_paraboloid(axes,step); self.clear_section()
        self.make_header(10, "PARABOLOIDE HIPERBÓLICO: LA SILLA", "La variable lineal sigue marcando el eje, pero los cuadrados tienen signos opuestos.")
        formula=self.formula_panel(r"z=\frac{x^2}{4}-\frac{y^2}{4}")
        step=self.step_panel("PASO 1", "TRAZA z = 0", ["x²/4 − y²/4 = 0.", "Se factoriza: (x−y)(x+y)=0 → dos rectas y=±x."])
        terms=self.term_panel([(r"z", "variable lineal"), (r"+x^2", "curvatura hacia +z"), (r"-y^2", "curvatura hacia −z")])
        self.paced_play(FadeIn(formula),FadeIn(step),FadeIn(terms),pause=PAUSE_READ)
        self.set_stable_camera();axes=self.axes3d();labels=self.axis_labels(axes)
        self.paced_play(Create(axes),FadeIn(labels),run_time=RUN_SLOW,pause=PAUSE_READ)
        self.build_hyperbolic_paraboloid(axes,step); self.clear_section()

    def worked_examples(self) -> None:
        self.make_header(11, "CLASIFICACIÓN PASO A PASO: TRES ECUACIONES", "Aplique siempre el algoritmo algebraico antes de dibujar; la gráfica debe confirmar la clasificación.")
        title_a=self.text("EJEMPLO A",23,BOLD).move_to(LEFT*5.7+UP*2.0); eq_a=self.math(r"x^2+4y^2=16",38).next_to(title_a,RIGHT,buff=0.4)
        self.register_fixed(title_a,eq_a); self.paced_play(FadeIn(title_a),Write(eq_a),run_time=RUN_NORMAL,pause=PAUSE_READ)
        a1=self.math(r"\frac{x^2}{16}+\frac{y^2}{4}=1",34).move_to(UP*0.9); a2=self.text("z no aparece → elipse repetida para todo z",24).next_to(a1,DOWN,buff=0.30); a3=self.text("CLASIFICACIÓN: CILINDRO ELÍPTICO paralelo a z",26,BOLD).next_to(a2,DOWN,buff=0.28)
        self.register_fixed(a1,a2,a3); self.paced_play(Write(a1),run_time=RUN_SLOW,pause=PAUSE_READ); self.paced_play(FadeIn(a2),run_time=RUN_NORMAL,pause=PAUSE_READ); self.paced_play(FadeIn(a3),run_time=RUN_NORMAL,pause=PAUSE_CONNECT)
        divider=Line(LEFT*6.8,RIGHT*6.8,color=LIGHT_GRAY,stroke_width=1.5).move_to(DOWN*0.55); self.register_fixed(divider); self.paced_play(Create(divider),run_time=RUN_QUICK,pause=PAUSE_SHORT)
        title_b=self.text("EJEMPLO B",23,BOLD).move_to(LEFT*5.7+DOWN*1.15); eq_b=self.math(r"4x^2+y^2-z^2=4",38).next_to(title_b,RIGHT,buff=0.4)
        self.register_fixed(title_b,eq_b); self.paced_play(FadeIn(title_b),Write(eq_b),run_time=RUN_NORMAL,pause=PAUSE_READ)
        b1=self.math(r"x^2+\frac{y^2}{4}-\frac{z^2}{4}=1",34).move_to(DOWN*2.15); b2=self.text("dos signos positivos + uno negativo = 1",23).next_to(b1,DOWN,buff=0.20); b3=self.text("CLASIFICACIÓN: HIPERBOLOIDE DE UNA HOJA, eje z",25,BOLD).next_to(b2,DOWN,buff=0.18)
        self.register_fixed(b1,b2,b3); self.paced_play(Write(b1),run_time=RUN_SLOW,pause=PAUSE_READ); self.paced_play(FadeIn(b2),run_time=RUN_NORMAL,pause=PAUSE_READ); self.paced_play(FadeIn(b3),run_time=RUN_NORMAL,pause=PAUSE_CONNECT); self.clear_section()
        self.make_header(12, "EJEMPLO FINAL: IDENTIFICAR APERTURA Y VÉRTICE", "Una clasificación completa debe decir el tipo de superficie, su eje/dirección y un rasgo geométrico verificable.")
        eq=self.math(r"z=9-x^2-y^2",46).move_to(UP*1.7); self.register_fixed(eq); self.paced_play(Write(eq),run_time=RUN_SLOW,pause=PAUSE_READ)
        lines=[self.text("1. z es lineal → familia paraboloide",25), self.text("2. −x² y −y² tienen el mismo signo → paraboloide elíptico",25), self.text("3. z=9 en x=y=0 → vértice (0,0,9)",25), self.text("4. Los cuadrados restan → abre hacia −z",25)]
        group=VGroup(*lines).arrange(DOWN,aligned_edge=LEFT,buff=0.28).move_to(DOWN*0.35); self.register_fixed(group)
        for line in lines: self.paced_play(FadeIn(line,shift=RIGHT*0.10),run_time=RUN_NORMAL,pause=PAUSE_READ)
        result=self.text("PARABOLOIDE ELÍPTICO · VÉRTICE (0,0,9) · APERTURA −z",28,BOLD).to_edge(DOWN,buff=0.65); self.register_fixed(result); self.paced_play(FadeIn(result),run_time=RUN_NORMAL,pause=PAUSE_SUMMARY); self.clear_section()

    def final_method(self) -> None:
        self.make_header(13, "MÉTODO FINAL: DE LA ECUACIÓN A LA SUPERFICIE", "Use esta secuencia como receta de examen y como guía para construir la gráfica sin depender primero de software.")
        steps=["1  SIMPLIFICAR Y COMPLETAR CUADRADOS", "2  NORMALIZAR: llevar la ecuación a = 1 o = 0", "3  BUSCAR VARIABLE AUSENTE", "4  IDENTIFICAR CUADRADOS, SIGNOS Y VARIABLE LINEAL", "5  CONSTRUIR TRAZAS x=k, y=k, z=k", "6  LOCALIZAR INTERCEPTOS, VÉRTICE, CINTURA O HUECO", "7  UNIR LAS TRAZAS Y CONFIRMAR LA FAMILIA"]
        cards=VGroup()
        for s in steps:
            box=RoundedRectangle(width=11.2,height=0.68,corner_radius=0.08,stroke_color=LIGHT_GRAY,stroke_width=1.2,fill_color=WHITE,fill_opacity=1); txt=self.text(s,21,BOLD if s.startswith(("1","3","5","7")) else MEDIUM); self.fit(txt,10.6,0.42); txt.move_to(box); cards.add(VGroup(box,txt))
        cards.arrange(DOWN,buff=0.13).shift(DOWN*0.35); self.register_fixed(cards)
        for card in cards: self.paced_play(FadeIn(card,shift=UP*0.06),run_time=RUN_QUICK,pause=PAUSE_SHORT)
        self.wait(PAUSE_SUMMARY)
        closing=self.text("PRIMERO LEA LA ECUACIÓN. DESPUÉS CONSTRUYA LA GEOMETRÍA.",28,BOLD).to_edge(DOWN,buff=0.30); self.register_fixed(closing); self.paced_play(FadeIn(closing),run_time=RUN_NORMAL,pause=PAUSE_FINAL); self.clear_section()

    def construct(self) -> None:
        self.opening()
        self.vocabulary_and_traces()
        self.cylindrical_surfaces()
        self.quadric_language()
        self.ellipsoid_section()
        self.hyperboloids_and_cone()
        self.paraboloids_section()
        self.worked_examples()
        self.final_method()
