#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Free fall from a 20 m building + Galileo bridge.

Professional 3D classroom reconstruction using the established JP ManimCE grammar:
- ManimCE 0.20.x / 1920x1080 / 30 fps / white classroom canvas.
- Real 3D context first: terrain -> footprint -> floor-by-floor building extrusion.
- Croquis protocol: 3D model -> deliberate camera transition -> stable facade view.
- One physical state drives object position, velocity vector, timer, HUD and graph.
- Free-fall model is derived only after the phenomenon is observed.
- Equal-time snapshots expose the 1:4:9:16 displacement law.
- Galileo inclined plane is introduced as a measurement strategy, not as decoration.
- Final bridge: constant acceleration -> quadratic displacement.

The numerical claims are asserted before the lesson begins.
"""

from __future__ import annotations

import math
import numpy as np
from manim import *

from library.jp_classroom_style import (
    BLACK_TEXT, BLACK_LINE, DARK_GRAY, MID_GRAY, LIGHT_GRAY, VERY_LIGHT_GRAY,
    PAPER_GRAY, WHITE_FILL, TIME_SCALE,
    RUN_QUICK, RUN_NORMAL, RUN_SLOW, RUN_CAMERA,
    PAUSE_SHORT, PAUSE_READ, PAUSE_EXPLAIN, PAUSE_SUMMARY, PAUSE_FINAL,
)

# =============================================================================
# PHYSICS — DISPLAYED VALUES COME FROM THESE DEFINITIONS
# =============================================================================
G = 9.81
HEIGHT_M = 20.0
T_HIT = math.sqrt(2.0 * HEIGHT_M / G)
V_HIT = -G * T_HIT

SAMPLE_TIMES = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
SAMPLE_DROP = 0.5 * G * SAMPLE_TIMES**2
NORMALIZED_DROP = SAMPLE_DROP[1:] / SAMPLE_DROP[1]

RAMP_THETA = 12.0 * DEGREES
RAMP_LENGTH_M = 4.0
# Ideal solid sphere rolling without slipping: a = (5/7) g sin(theta)
RAMP_A = (5.0 / 7.0) * G * math.sin(RAMP_THETA)
RAMP_T_END = math.sqrt(2.0 * RAMP_LENGTH_M / RAMP_A)

# =============================================================================
# VISUAL SCALE — METRES ARE MAPPED INTO SCENE UNITS ONLY FOR DISPLAY
# =============================================================================
GROUND_Z = 0.0
BUILDING_H = 5.0
BUILDING_W = 3.35
BUILDING_D = 2.55
FLOORS = 5
FLOOR_H = BUILDING_H / FLOORS
BALL_X = 2.22
BALL_Y = -BUILDING_D / 2 - 0.42

ACCENT = "#2F6F9F"
ACCENT_SOFT = "#DCEAF3"
GREEN = "#2E7D55"
AMBER = "#C58A22"
RED = "#B74B4B"


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class Physics9FreeFallBuilding3DCinematic(ThreeDScene):
    """3D cinematic lesson: building context -> free fall -> Galileo."""

    # -------------------------------------------------------------------------
    # Timing wrappers: respect LESSON_TIME_SCALE during PQL/PQM QA.
    # -------------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        assert abs(HEIGHT_M - 0.5 * G * T_HIT**2) < 1e-10
        assert abs(V_HIT**2 - 2.0 * G * HEIGHT_M) < 1e-10
        assert np.allclose(NORMALIZED_DROP, [1.0, 4.0, 9.0, 16.0])
        assert 0 < RAMP_A < G
        assert abs(RAMP_LENGTH_M - 0.5 * RAMP_A * RAMP_T_END**2) < 1e-10

    # -------------------------------------------------------------------------
    # Generic style helpers
    # -------------------------------------------------------------------------
    def txt(self, s: str, size=28, weight=NORMAL, color=BLACK_TEXT) -> Text:
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.92)

    def math(self, s: str, size=40, color=BLACK_TEXT) -> MathTex:
        return MathTex(s, font_size=size, color=color)

    def box3d(self, dims, center, fill=VERY_LIGHT_GRAY, opacity=1.0,
              stroke=BLACK_LINE, stroke_width=0.8) -> Cube:
        x, y, z = dims
        mob = Cube(
            side_length=1.0,
            fill_color=fill,
            fill_opacity=opacity,
            stroke_color=stroke,
            stroke_width=stroke_width,
        )
        mob.stretch(x, 0).stretch(y, 1).stretch(z, 2)
        mob.move_to(np.array(center, dtype=float))
        return mob

    def fixed_header(self):
        title = self.txt("FÍSICA 9° · CAÍDA LIBRE", 31, BOLD)
        subtitle = self.txt(
            "De un edificio de 20 m al modelo de aceleración constante",
            20, NORMAL, MID_GRAY,
        )
        title.to_corner(UL, buff=0.38)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.07)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, color=LIGHT_GRAY, stroke_width=1.2)
        rule.to_edge(UP, buff=1.07)

        phase_box = RoundedRectangle(
            width=5.10, height=0.54, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.2,
            fill_color=WHITE_FILL, fill_opacity=0.96,
        ).to_corner(UR, buff=0.39)
        phase = self.txt("01 · CONTEXTO 3D", 19, BOLD).move_to(phase_box)

        header = VGroup(title, subtitle, rule, phase_box, phase)
        self.add_fixed_in_frame_mobjects(*header)
        return {"group": header, "phase_box": phase_box, "phase": phase}

    def set_phase(self, header, number: int, label: str, color=BLACK_TEXT):
        old = header["phase"]
        new = self.txt(f"{number:02d} · {label}", 19, BOLD, color).move_to(header["phase_box"])
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=RUN_QUICK * 0.55)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        header["phase"] = new

    def fixed_note(self, title: str, body: str, *, color=BLACK_LINE,
                   width=6.5, position=DOWN * 3.30):
        box = RoundedRectangle(
            width=width, height=1.08, corner_radius=0.12,
            stroke_color=color, stroke_width=1.35,
            fill_color=WHITE_FILL, fill_opacity=0.96,
        )
        t = self.txt(title, 19, BOLD, color)
        b = self.txt(body, 19, NORMAL, BLACK_TEXT)
        if b.width > width - 0.55:
            b.scale_to_fit_width(width - 0.55)
        stack = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        stack.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.26)
        g = VGroup(box, stack).move_to(position)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP * 0.08), run_time=RUN_QUICK)
        return g

    def remove_fixed(self, *mobs, run_time=RUN_QUICK):
        group = VGroup(*mobs)
        self.play(FadeOut(group), run_time=run_time)
        for mob in mobs:
            try:
                self.remove_fixed_in_frame_mobjects(mob)
            except Exception:
                pass
            self.remove(mob)

    def formula_panel(self, formula: str, *, width=6.2, size=42, y=-2.85):
        box = RoundedRectangle(
            width=width, height=1.05, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=PAPER_GRAY, fill_opacity=1.0,
        )
        eq = self.math(formula, size)
        if eq.width > width - 0.45:
            eq.scale_to_fit_width(width - 0.45)
        eq.move_to(box)
        g = VGroup(box, eq).move_to([0, y, 0])
        self.add_fixed_in_frame_mobjects(g)
        return g

    # -------------------------------------------------------------------------
    # Building geometry
    # -------------------------------------------------------------------------
    def terrain_and_city(self):
        terrain = self.box3d((12.5, 8.0, 0.12), (0, 0, -0.06),
                             fill="#F3F5F2", stroke=LIGHT_GRAY, stroke_width=0.5)
        roads = VGroup(
            self.box3d((12.5, 1.05, 0.025), (0, 3.0, 0.02),
                       fill="#E1E4E6", stroke=LIGHT_GRAY, stroke_width=0.2),
            self.box3d((1.15, 8.0, 0.025), (-4.6, 0, 0.022),
                       fill="#E1E4E6", stroke=LIGHT_GRAY, stroke_width=0.2),
        )
        context = VGroup(
            self.box3d((1.9, 1.7, 1.4), (-4.1, -1.9, 0.70), fill="#ECECEC", opacity=0.85),
            self.box3d((2.2, 1.8, 2.0), (4.3, 1.65, 1.00), fill="#E7E7E7", opacity=0.85),
            self.box3d((1.6, 1.5, 1.0), (4.55, -2.0, 0.50), fill="#F0F0F0", opacity=0.85),
        )
        return terrain, roads, context

    def building_floor(self, i: int, seed=False):
        target_h = 0.91 if not seed else 0.035
        z_base = i * FLOOR_H
        zc = z_base + target_h / 2.0
        fill = "#E5E7E9" if i % 2 == 0 else "#DDE1E4"
        return self.box3d(
            (BUILDING_W, BUILDING_D, target_h),
            (0, 0, zc),
            fill=fill, opacity=0.96, stroke=DARK_GRAY, stroke_width=0.65,
        )

    def window_band(self, floor: int):
        z = floor * FLOOR_H + 0.53
        front = VGroup()
        for x in (-1.15, -0.38, 0.38, 1.15):
            front.add(self.box3d(
                (0.48, 0.035, 0.29),
                (x, -BUILDING_D / 2 - 0.020, z),
                fill=ACCENT_SOFT, opacity=0.92, stroke=ACCENT, stroke_width=0.40,
            ))
        side = VGroup()
        for y in (-0.82, 0.0, 0.82):
            side.add(self.box3d(
                (0.035, 0.47, 0.29),
                (BUILDING_W / 2 + 0.020, y, z),
                fill=ACCENT_SOFT, opacity=0.92, stroke=ACCENT, stroke_width=0.40,
            ))
        return VGroup(front, side)

    def building_footprint(self):
        w, d = BUILDING_W, BUILDING_D
        z = 0.02
        pts = [
            [-w/2, -d/2, z], [w/2, -d/2, z],
            [w/2, d/2, z], [-w/2, d/2, z],
        ]
        return VGroup(*[
            Line(pts[i], pts[(i + 1) % 4], color=ACCENT, stroke_width=4.0)
            for i in range(4)
        ])

    def physical_z_to_scene(self, y_m: float) -> float:
        return clamp(y_m / HEIGHT_M, 0.0, 1.0) * BUILDING_H

    def y_phys(self, t: float) -> float:
        return max(0.0, HEIGHT_M - 0.5 * G * t * t)

    def v_phys(self, t: float) -> float:
        return -G * min(max(t, 0.0), T_HIT)

    # -------------------------------------------------------------------------
    # Main timeline
    # -------------------------------------------------------------------------
    def construct(self):
        self.validate_lesson_data()
        self.camera.background_color = WHITE
        header = self.fixed_header()

        self.scene_01_build_context(header)
        self.scene_02_define_event(header)
        self.scene_03_live_free_fall(header)
        self.scene_04_equal_time_evidence(header)
        self.scene_05_extract_model(header)
        self.scene_06_sync_graph(header)
        self.scene_07_galileo_ramp(header)
        self.scene_08_synthesis(header)

        self.remove_fixed(\n            header["group"][0], header["group"][1], header["group"][2],\n            header["group"][3], header["phase"], run_time=RUN_NORMAL\n        )

    # -------------------------------------------------------------------------
    # 01 — Build the physical context before equations.
    # -------------------------------------------------------------------------
    def scene_01_build_context(self, header):
        self.set_phase(header, 1, "CONSTRUIR CONTEXTO 3D", ACCENT)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-47 * DEGREES, zoom=0.82)

        terrain, roads, context = self.terrain_and_city()
        self.play(FadeIn(terrain), FadeIn(roads), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(b) for b in context], lag_ratio=0.16), run_time=RUN_NORMAL)

        # CAD-style footprint first, then volumetric extrusion floor by floor.
        footprint = self.building_footprint()
        self.play(Create(footprint), run_time=RUN_SLOW)
        note = self.fixed_note(
            "ESCALA DEL PROBLEMA",
            "El edificio representa 20 m de altura: cinco niveles de 4 m.",
            color=ACCENT, width=7.1,
        )
        self.wait(PAUSE_READ)

        floors = VGroup()
        windows = VGroup()
        for i in range(FLOORS):
            seed = self.building_floor(i, seed=True)
            target = self.building_floor(i, seed=False)
            self.add(seed)
            self.play(Transform(seed, target), run_time=0.70)
            floors.add(seed)
            band = self.window_band(i)
            self.play(FadeIn(band), run_time=0.32)
            windows.add(band)

        roof = self.box3d(
            (BUILDING_W + 0.18, BUILDING_D + 0.18, 0.12),
            (0, 0, BUILDING_H + 0.06),
            fill="#C8CDD1", opacity=1.0, stroke=DARK_GRAY, stroke_width=0.75,
        )
        self.play(FadeIn(roof), FadeOut(footprint), run_time=RUN_NORMAL)
        self.remove_fixed(note, run_time=RUN_QUICK)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(2.2)
        self.stop_ambient_camera_rotation()

        note2 = self.fixed_note(
            "PREGUNTA FÍSICA",
            "Si soltamos una esfera desde la azotea, ¿cómo cambia su movimiento segundo a segundo?",
            color=BLACK_LINE, width=9.1,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(note2, run_time=RUN_QUICK)

        self.city_group = VGroup(terrain, roads, context)
        self.building_group = VGroup(floors, windows, roof)

    # -------------------------------------------------------------------------
    # 02 — Establish the force model at the roof.
    # -------------------------------------------------------------------------
    def scene_02_define_event(self, header):
        self.set_phase(header, 2, "ANTES DE SOLTAR", BLACK_TEXT)
        self.move_camera(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.96, run_time=RUN_CAMERA)

        roof_ball = Sphere(radius=0.18, resolution=(12, 24), fill_color=ACCENT,
                           fill_opacity=1.0, stroke_color=BLACK_LINE, stroke_width=0.8)
        roof_ball.move_to([BALL_X, BALL_Y, BUILDING_H])
        self.play(FadeIn(roof_ball, scale=0.7), run_time=RUN_NORMAL)

        gravity_line = Line(
            [BALL_X + 0.45, BALL_Y, BUILDING_H + 0.10],
            [BALL_X + 0.45, BALL_Y, BUILDING_H - 1.05],
            color=RED, stroke_width=5.0,
        )
        gravity_tip = Triangle(fill_color=RED, fill_opacity=1.0, stroke_width=0).scale(0.09)
        gravity_tip.rotate(PI).move_to([BALL_X + 0.45, BALL_Y, BUILDING_H - 1.05])
        self.play(Create(gravity_line), FadeIn(gravity_tip), run_time=RUN_NORMAL)

        force = self.formula_panel(r"\sum F_y=-mg\quad\Longrightarrow\quad a_y=-g", width=7.4, size=42)
        self.play(FadeIn(force), run_time=RUN_NORMAL)
        note = self.fixed_note(
            "MODELO IDEAL",
            "Después de soltarla, ignoramos la resistencia del aire: la gravedad es la única fuerza relevante.",
            color=RED, width=9.4,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(note, force, run_time=RUN_QUICK)
        self.play(FadeOut(gravity_line), FadeOut(gravity_tip), run_time=RUN_QUICK)

        self.roof_ball = roof_ball

    # -------------------------------------------------------------------------
    # 03 — One tracker controls the actual fall and live measurements.
    # -------------------------------------------------------------------------
    def scene_03_live_free_fall(self, header):
        self.set_phase(header, 3, "CAÍDA · ESTADO EN VIVO", RED)

        t = ValueTracker(0.0)
        self.play(FadeOut(self.roof_ball), run_time=RUN_QUICK)

        moving_ball = always_redraw(lambda: Sphere(
            radius=0.18, resolution=(10, 20),
            fill_color=ACCENT, fill_opacity=1.0,
            stroke_color=BLACK_LINE, stroke_width=0.7,
        ).move_to([
            BALL_X, BALL_Y,
            self.physical_z_to_scene(self.y_phys(t.get_value()))
        ]))

        velocity_line = always_redraw(lambda: Line(
            [
                BALL_X + 0.43, BALL_Y,
                self.physical_z_to_scene(self.y_phys(t.get_value()))
            ],
            [
                BALL_X + 0.43, BALL_Y,
                self.physical_z_to_scene(self.y_phys(t.get_value()))
                - 0.055 * abs(self.v_phys(t.get_value()))
            ],
            color=AMBER, stroke_width=5.0,
        ))

        trail = TracedPath(
            lambda: moving_ball.get_center(),
            stroke_color=ACCENT, stroke_width=3.0, dissipating_time=1.3,
        )

        # Live fixed HUD.
        panel = RoundedRectangle(
            width=4.25, height=2.15, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.4,
            fill_color=WHITE_FILL, fill_opacity=0.95,
        ).move_to([4.85, 1.45, 0])
        ttl = self.txt("ESTADO FÍSICO", 21, BOLD).move_to(panel.get_top() + DOWN * 0.30)
        lab_t = self.txt("t", 21, BOLD).move_to([3.65, 1.55, 0])
        lab_y = self.txt("y", 21, BOLD).move_to([3.65, 0.98, 0])
        lab_v = self.txt("vᵧ", 21, BOLD).move_to([3.65, 0.41, 0])
        val_t = DecimalNumber(0, num_decimal_places=2, font_size=28, color=BLACK_TEXT, unit=" s").move_to([5.05, 1.55, 0])
        val_y = DecimalNumber(HEIGHT_M, num_decimal_places=2, font_size=28, color=BLACK_TEXT, unit=" m").move_to([5.05, 0.98, 0])
        val_v = DecimalNumber(0, num_decimal_places=2, include_sign=True, font_size=28, color=BLACK_TEXT, unit=" m/s").move_to([5.05, 0.41, 0])
        val_t.add_updater(lambda m: m.set_value(t.get_value()))
        val_y.add_updater(lambda m: m.set_value(self.y_phys(t.get_value())))
        val_v.add_updater(lambda m: m.set_value(self.v_phys(t.get_value())))
        hud = VGroup(panel, ttl, lab_t, lab_y, lab_v, val_t, val_y, val_v)
        self.add_fixed_in_frame_mobjects(hud)

        self.add(trail, moving_ball, velocity_line)
        self.play(FadeIn(hud), run_time=RUN_NORMAL)
        self.play(t.animate.set_value(T_HIT), run_time=4.8, rate_func=linear)
        self.wait(PAUSE_SHORT)

        val_t.clear_updaters(); val_y.clear_updaters(); val_v.clear_updaters()
        impact = self.fixed_note(
            "IMPACTO",
            f"Desde 20 m:  t = {T_HIT:.2f} s   ·   v = {V_HIT:.2f} m/s.  La rapidez aumentó durante toda la caída.",
            color=RED, width=10.6,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(impact, hud, run_time=RUN_QUICK)
        self.play(FadeOut(moving_ball), FadeOut(velocity_line), run_time=RUN_QUICK)
        self.remove(trail)

    # -------------------------------------------------------------------------
    # 04 — Orthographic facade + stroboscopic evidence.
    # -------------------------------------------------------------------------
    def scene_04_equal_time_evidence(self, header):
        self.set_phase(header, 4, "FOTOGRAFÍAS A TIEMPOS IGUALES", ACCENT)

        # Croquis protocol: deliberate 3D -> stable facade transition.
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=RUN_CAMERA * 1.35)
        self.wait(0.70)

        ghosts = VGroup()
        for tt in SAMPLE_TIMES:
            y = self.y_phys(min(tt, T_HIT))
            z = self.physical_z_to_scene(y)
            ghost = Sphere(
                radius=0.13, resolution=(8, 16),
                fill_color=WHITE_FILL, fill_opacity=0.82,
                stroke_color=ACCENT, stroke_width=1.7,
            ).move_to([BALL_X, BALL_Y, z])
            ghosts.add(ghost)

        self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in ghosts], lag_ratio=0.18), run_time=RUN_SLOW)

        data_box = RoundedRectangle(
            width=6.65, height=3.25, corner_radius=0.13,
            stroke_color=BLACK_LINE, stroke_width=1.4,
            fill_color=WHITE_FILL, fill_opacity=0.97,
        ).move_to([3.9, -0.25, 0])
        data_title = self.txt("DISTANCIA CAÍDA DESDE EL REPOSO", 20, BOLD).move_to(data_box.get_top() + DOWN * 0.34)
        rows = VGroup(
            self.txt("t (s)     0.5      1.0      1.5      2.0", 22),
            self.txt("d/d₀       1         4         9        16", 26, BOLD, ACCENT),
            self.math(r"d=\frac12gt^2", 42, ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(data_box)
        data = VGroup(data_box, data_title, rows)
        self.add_fixed_in_frame_mobjects(data)
        self.play(FadeIn(data), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        conclusion = self.fixed_note(
            "EVIDENCIA",
            "En intervalos iguales de tiempo, las separaciones crecen: el movimiento no es uniforme; está acelerado.",
            color=ACCENT, width=10.2,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(conclusion, data, run_time=RUN_QUICK)
        self.play(FadeOut(ghosts), run_time=RUN_NORMAL)

    # -------------------------------------------------------------------------
    # 05 — Extract a clean elevation and derive the equations step by step.
    # -------------------------------------------------------------------------
    def scene_05_extract_model(self, header):
        self.set_phase(header, 5, "DEL FENÓMENO AL MODELO", BLACK_TEXT)

        # Fade the 3D context and replace it with a technical facade diagram.
        self.play(self.city_group.animate.set_opacity(0.16),
                  self.building_group.animate.set_opacity(0.20),
                  run_time=RUN_NORMAL)

        facade = Rectangle(
            width=3.0, height=5.0,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=0.45,
        ).move_to([-4.65, -0.35, 0])
        floor_lines = VGroup(*[
            Line(
                facade.get_left() + UP * (-2.5 + i),
                facade.get_right() + UP * (-2.5 + i),
                color=LIGHT_GRAY, stroke_width=1.0,
            )
            for i in range(1, 5)
        ])
        roof_dot = Dot(facade.get_top() + RIGHT * 0.36, radius=0.10, color=ACCENT)
        ground = Line([-6.55, -2.85, 0], [-2.65, -2.85, 0], color=BLACK_LINE, stroke_width=2)
        dim = DoubleArrow(
            [-6.45, -2.80, 0], [-6.45, 2.15, 0],
            buff=0, color=BLACK_LINE, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.06,
        )
        dim_label = self.txt("20 m", 23, BOLD).rotate(PI / 2).next_to(dim, LEFT, buff=0.10)
        y_axis = Arrow([-2.55, -2.75, 0], [-2.55, 2.35, 0], buff=0, color=BLACK_LINE, stroke_width=2.2)
        plus = self.math(r"+y", 27).next_to(y_axis, UP, buff=0.05)
        diagram = VGroup(facade, floor_lines, roof_dot, ground, dim, dim_label, y_axis, plus)
        self.add_fixed_in_frame_mobjects(diagram)
        self.play(FadeIn(diagram), run_time=RUN_NORMAL)

        steps = [
            (r"\sum F_y=-mg", "1 · fuerza neta"),
            (r"ma_y=-mg", "2 · segunda ley de Newton"),
            (r"a_y=-g", "3 · aceleración constante"),
            (r"v_y=v_0-gt", "4 · velocidad"),
            (r"y=y_0+v_0t-\frac12gt^2", "5 · posición"),
        ]

        old = None
        for formula, label in steps:
            label_m = self.txt(label, 20, BOLD, MID_GRAY).move_to([2.2, 1.75, 0])
            eq = self.math(formula, 48).move_to([2.2, 0.55, 0])
            box = RoundedRectangle(
                width=7.2, height=2.35, corner_radius=0.13,
                stroke_color=BLACK_LINE, stroke_width=1.45,
                fill_color=WHITE_FILL, fill_opacity=0.98,
            ).move_to([2.2, 0.55, 0])
            g = VGroup(box, label_m, eq)
            self.add_fixed_in_frame_mobjects(g)
            if old is None:
                self.play(FadeIn(g), run_time=RUN_NORMAL)
            else:
                self.play(FadeOut(old), FadeIn(g), run_time=RUN_NORMAL)
                self.remove_fixed_in_frame_mobjects(old)
                self.remove(old)
            old = g
            self.wait(PAUSE_READ)

        self.remove_fixed(old, run_time=RUN_QUICK)

        release = VGroup(
            self.txt("PARA ESTE CASO", 19, BOLD, ACCENT),
            self.math(r"y_0=20\,m,\qquad v_0=0,\qquad y=0", 40),
            self.math(r"0=20-\frac12(9.81)t^2", 43),
            self.math(r"t=\sqrt{\frac{2(20)}{9.81}}=2.02\,s", 43, ACCENT),
        ).arrange(DOWN, buff=0.28).move_to([2.25, -0.35, 0])
        self.add_fixed_in_frame_mobjects(release)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in release], lag_ratio=0.14), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        check = self.fixed_note(
            "COMPROBACIÓN",
            f"v = -gt = -9.81({T_HIT:.2f}) = {V_HIT:.2f} m/s.",
            color=GREEN, width=7.0,
        )
        self.wait(PAUSE_READ)
        self.remove_fixed(check, release, diagram, run_time=RUN_QUICK)

        self.play(FadeOut(self.building_group), FadeOut(self.city_group), run_time=RUN_NORMAL)

    # -------------------------------------------------------------------------
    # 06 — Re-run the fall as a synchronized elevation + v(t) graph.
    # -------------------------------------------------------------------------
    def scene_06_sync_graph(self, header):
        self.set_phase(header, 6, "MISMO ESTADO · DOS REPRESENTACIONES", AMBER)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)

        t = ValueTracker(0.0)

        # Left: simplified building elevation.
        building = Rectangle(
            width=3.05, height=5.25,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=0.55,
        ).move_to([-4.35, -0.45, 0])
        floors = VGroup(*[
            Line(building.get_left() + UP * (-2.10 + i * 1.05),
                 building.get_right() + UP * (-2.10 + i * 1.05),
                 color=LIGHT_GRAY, stroke_width=1.0)
            for i in range(1, 5)
        ])
        left_title = self.txt("POSICIÓN", 20, BOLD).move_to([-4.35, 2.55, 0])

        top_y = 2.17
        bottom_y = -3.03
        moving = always_redraw(lambda: Dot(
            [-2.55,
             bottom_y + (top_y - bottom_y) * self.y_phys(t.get_value()) / HEIGHT_M,
             0],
            radius=0.11, color=ACCENT,
        ))
        vel_arrow = always_redraw(lambda: Arrow(
            moving.get_center() + RIGHT * 0.28,
            moving.get_center() + RIGHT * 0.28 + DOWN * (0.03 + 0.055 * abs(self.v_phys(t.get_value()))),
            buff=0, color=AMBER, stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        ))

        # Right: live velocity graph.
        axes = Axes(
            x_range=[0, 2.2, 0.5],
            y_range=[-22, 2, 5],
            x_length=6.1, y_length=4.4,
            axis_config={"color": MID_GRAY, "stroke_width": 1.5, "include_tip": False},
            tips=False,
        ).move_to([3.45, -0.35, 0])
        xlab = self.txt("t (s)", 19, BOLD).next_to(axes.x_axis, DOWN, buff=0.15)
        ylab = self.txt("vᵧ (m/s)", 19, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.15)
        graph = always_redraw(lambda: axes.plot(
            lambda x: -G * x,
            x_range=[0, max(0.001, min(t.get_value(), T_HIT))],
            color=AMBER, stroke_width=3.4,
        ))
        graph_dot = always_redraw(lambda: Dot(
            axes.c2p(t.get_value(), self.v_phys(t.get_value())),
            radius=0.075, color=ACCENT,
        ))

        time_display = DecimalNumber(0, num_decimal_places=2, font_size=26, color=BLACK_TEXT, unit=" s")
        time_display.move_to([0.0, -3.40, 0])
        time_display.add_updater(lambda m: m.set_value(t.get_value()))
        time_label = self.txt("t =", 20, BOLD).next_to(time_display, LEFT, buff=0.08)

        fixed = VGroup(building, floors, left_title, moving, vel_arrow,
                       axes, xlab, ylab, graph, graph_dot, time_display, time_label)
        self.add_fixed_in_frame_mobjects(fixed)
        self.play(FadeIn(building), FadeIn(floors), FadeIn(left_title),
                  FadeIn(axes), FadeIn(xlab), FadeIn(ylab), FadeIn(time_display), FadeIn(time_label),
                  run_time=RUN_NORMAL)
        self.add(moving, vel_arrow, graph, graph_dot)
        self.play(t.animate.set_value(T_HIT), run_time=4.8, rate_func=linear)
        self.wait(PAUSE_READ)
        time_display.clear_updaters()

        slope = self.fixed_note(
            "LECTURA DEL GRÁFICO",
            "La pendiente de v(t) es constante y negativa:  Δv/Δt = −9.81 m/s².",
            color=AMBER, width=9.0,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(slope, fixed, run_time=RUN_QUICK)
        self.remove(moving, vel_arrow, graph, graph_dot)

    # -------------------------------------------------------------------------
    # 07 — Galileo: slow the phenomenon to make the quadratic law measurable.
    # -------------------------------------------------------------------------
    def scene_07_galileo_ramp(self, header):
        self.set_phase(header, 7, "GALILEO · HACER MEDIBLE LA ACELERACIÓN", GREEN)
        self.set_camera_orientation(phi=67 * DEGREES, theta=-52 * DEGREES, zoom=0.92)

        base = self.box3d((9.2, 4.8, 0.10), (0, 0, -0.05),
                          fill="#F5F5F2", stroke=LIGHT_GRAY, stroke_width=0.5)
        self.play(FadeIn(base), run_time=RUN_NORMAL)

        # Ramp is a thin board rotated around the y axis.
        ramp = self.box3d((6.4, 1.35, 0.14), (0, 0, 0.0),
                          fill="#E5E7E9", stroke=DARK_GRAY, stroke_width=0.8)
        ramp.rotate(-RAMP_THETA, axis=UP)
        # Shift so both ends sit in a useful camera volume.
        ramp.shift(UP * 0.0 + OUT * 0.78)
        self.play(FadeIn(ramp), run_time=RUN_NORMAL)

        # Approximate endpoints along the board's centre line.
        x0, x1 = -3.05, 3.05
        z0 = 0.78 + 3.05 * math.sin(RAMP_THETA)
        z1 = 0.78 - 3.05 * math.sin(RAMP_THETA)
        start = np.array([x0, -0.10, z0 + 0.18])
        end = np.array([x1, -0.10, z1 + 0.18])

        ball = Sphere(radius=0.18, resolution=(10, 20), fill_color=GREEN,
                      fill_opacity=1.0, stroke_color=BLACK_LINE, stroke_width=0.7).move_to(start)
        self.play(FadeIn(ball), run_time=RUN_NORMAL)

        intro = self.fixed_note(
            "IDEA DE GALILEO",
            "El plano inclinado reduce la aceleración observable y alarga el tiempo de medición.",
            color=GREEN, width=8.6,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(intro, run_time=RUN_QUICK)

        # Equal-time positions generated by s ~ t².
        marks = VGroup()
        fractions = [1/16, 4/16, 9/16, 1.0]
        for i, frac in enumerate(fractions, start=1):
            p = interpolate(start, end, frac)
            marker = Sphere(radius=0.075, resolution=(6, 12),
                            fill_color=ACCENT, fill_opacity=1.0,
                            stroke_color=ACCENT, stroke_width=0.2).move_to(p)
            marks.add(marker)
            self.play(ball.animate.move_to(p), FadeIn(marker), run_time=0.75, rate_func=linear)
            beat = self.fixed_note(
                f"TIEMPO {i}",
                f"Posición acumulada proporcional a {i*i}:   1, 4, 9, 16.",
                color=GREEN, width=6.8,
            )
            self.wait(PAUSE_SHORT)
            self.remove_fixed(beat, run_time=RUN_QUICK * 0.65)

        law = self.formula_panel(r"s=\frac12a_{\rm rampa}t^2", width=6.2, size=43)
        self.play(FadeIn(law), run_time=RUN_NORMAL)
        caveat = self.fixed_note(
            "MODELO DEL CUERPO",
            r"Para una esfera maciza que rueda sin deslizar:  a = (5/7) g sin(theta).  Sigue siendo constante.",
            color=GREEN, width=10.4,
        )
        self.wait(PAUSE_EXPLAIN)
        self.remove_fixed(caveat, law, run_time=RUN_QUICK)

        self.play(FadeOut(VGroup(base, ramp, ball, marks)), run_time=RUN_NORMAL)

        # Linearization in the classroom frame.
        axes = Axes(
            x_range=[0, 16, 4], y_range=[0, 16, 4],
            x_length=7.0, y_length=4.5,
            axis_config={"color": MID_GRAY, "stroke_width": 1.5, "include_tip": False},
            tips=False,
        ).move_to([-1.7, -0.25, 0])
        xlab = self.txt("t²", 21, BOLD).next_to(axes.x_axis, DOWN, buff=0.18)
        ylab = self.txt("s", 21, BOLD).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.18)
        line = Line(axes.c2p(0, 0), axes.c2p(16, 16), color=GREEN, stroke_width=3.0)
        dots = VGroup(*[Dot(axes.c2p(q, q), radius=0.085, color=ACCENT) for q in (1, 4, 9, 16)])
        panel = RoundedRectangle(
            width=5.05, height=3.15, corner_radius=0.13,
            stroke_color=BLACK_LINE, stroke_width=1.4,
            fill_color=WHITE_FILL, fill_opacity=0.97,
        ).move_to([4.85, -0.20, 0])
        text = VGroup(
            self.txt("PRUEBA EXPERIMENTAL", 21, BOLD, GREEN),
            self.txt("Si s ∝ t²,", 24),
            self.txt("la gráfica s vs t²", 24),
            self.txt("debe ser una recta.", 24, BOLD),
            self.math(r"\mathrm{pendiente}=\frac a2", 36, GREEN),
        ).arrange(DOWN, buff=0.16).move_to(panel)
        fixed = VGroup(axes, xlab, ylab, line, dots, panel, text)
        self.add_fixed_in_frame_mobjects(fixed)
        self.play(FadeIn(axes), FadeIn(xlab), FadeIn(ylab), FadeIn(panel), FadeIn(text), run_time=RUN_NORMAL)
        self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.remove_fixed(fixed, run_time=RUN_NORMAL)

    # -------------------------------------------------------------------------
    # 08 — Final synthesis: same mathematical structure, different context.
    # -------------------------------------------------------------------------
    def scene_08_synthesis(self, header):
        self.set_phase(header, 8, "SÍNTESIS", BLACK_TEXT)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)

        title = self.txt("UNA MISMA ESTRUCTURA CINEMÁTICA", 34, BOLD).move_to([0, 1.95, 0])
        eq = self.math(r"\boxed{\Delta x=v_0t+\frac12at^2}", 54).move_to([0, 0.65, 0])

        left = RoundedRectangle(
            width=5.4, height=2.35, corner_radius=0.13,
            stroke_color=ACCENT, stroke_width=1.6,
            fill_color=WHITE_FILL, fill_opacity=1,
        ).move_to([-3.3, -1.35, 0])
        right = RoundedRectangle(
            width=5.4, height=2.35, corner_radius=0.13,
            stroke_color=GREEN, stroke_width=1.6,
            fill_color=WHITE_FILL, fill_opacity=1,
        ).move_to([3.3, -1.35, 0])

        left_text = VGroup(
            self.txt("EDIFICIO · CAÍDA LIBRE", 21, BOLD, ACCENT),
            self.math(r"v_0=0,\quad a=-g", 35),
            self.txt(f"20 m  →  {T_HIT:.2f} s", 24, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(left)
        right_text = VGroup(
            self.txt("PLANO INCLINADO", 21, BOLD, GREEN),
            self.math(r"v_0=0,\quad |a|<g", 35),
            self.txt("Más tiempo para medir la misma ley cuadrática", 20, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(right)
        if right_text.width > 4.9:
            right_text.scale_to_fit_width(4.9)

        final = VGroup(title, eq, left, right, left_text, right_text)
        self.add_fixed_in_frame_mobjects(final)
        self.play(FadeIn(title), run_time=RUN_NORMAL)
        self.play(Write(eq), run_time=RUN_SLOW)
        self.play(FadeIn(left), FadeIn(left_text), run_time=RUN_NORMAL)
        self.play(FadeIn(right), FadeIn(right_text), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        method = self.fixed_note(
            "MÉTODO",
            "1) define el eje  ·  2) identifica fuerzas  ·  3) fija v₀  ·  4) usa a constante  ·  5) interpreta el signo.",
            color=BLACK_LINE, width=11.5,
        )
        self.wait(PAUSE_FINAL)
        self.remove_fixed(method, final, run_time=RUN_NORMAL)
