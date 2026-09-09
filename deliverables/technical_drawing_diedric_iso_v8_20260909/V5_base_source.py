#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 Senior Frame-QA — Sistema diédrico, ISO E / ISO A, NTC 1777:2001.

Rebuild based on V4, focused on the issues found in the rendered lesson:
- fixed-frame safe zones to avoid text/figure overlap;
- larger orthographic projections;
- longer observer-view holds;
- smoother camera transitions;
- clearer separation between 3D observation and 2D projection;
- less simultaneous information on screen.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, -pqh.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Core.technical_drawing_tools import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = BG

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RT_FAST = 0.65
RT = 1.00
RT_SMOOTH = 1.55
RT_CAMERA = 2.35
RT_DRAW = 2.15
PAUSE_BEAT = 1.15
PAUSE_READ = 2.35
PAUSE_EXPLAIN = 3.25
PAUSE_OBSERVER = 3.10
PAUSE_VIEW = 2.45
PAUSE_LONG = 4.35
PAUSE_CHALLENGE = 8.0


class DiedricISOProjectionV5SeniorFrameQA(ThreeDScene):
    """Full V5 rebuild with explicit visual-safe regions."""

    def play(self, *anims, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*anims, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def fadd(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)
        self.add(*mobs)

    def frem(self, *mobs):
        try:
            self.remove_fixed_in_frame_mobjects(*mobs)
        except Exception:
            pass
        self.remove(*mobs)

    def cleanup(self, *mobs, run_time=RT):
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            self.frem(*mobs)

    def header(self, number, title, subtitle):
        h = section_header(number, title, subtitle)
        self.fadd(h)
        self.play(FadeIn(h, shift=DOWN * 0.06), run_time=RT_FAST)
        return h

    def transition(self, number, title, subtitle):
        veil = Rectangle(width=16, height=9, stroke_width=0,
                         fill_color=NAVY, fill_opacity=1)
        line = Rectangle(width=2.5, height=0.05, stroke_width=0,
                         fill_color=CYAN, fill_opacity=1)
        block = VGroup(
            safe_text(f"{number:02d}", 54, CYAN, BOLD),
            safe_text(title, 46, PAPER, BOLD, 13.2),
            line,
            safe_text(subtitle, 22, "#CBD8E5", NORMAL, 12.8),
        ).arrange(DOWN, buff=0.20)
        self.fadd(veil, block)
        self.play(FadeIn(veil), FadeIn(block, shift=UP * 0.18), run_time=RT)
        self.wait(PAUSE_BEAT)
        self.play(FadeOut(block), FadeOut(veil), run_time=RT)
        self.frem(veil, block)

    def top_tag(self, text, color=BLUE, width=4.7):
        tag = callout(text, color, width, 20).move_to([-5.15, 2.55, 0])
        self.fadd(tag)
        self.play(FadeIn(tag, shift=RIGHT * 0.08), run_time=RT_FAST)
        return tag

    def view_fullscreen(self, key, color, caption):
        """Large 2D projection in the safe center band, no footer collisions."""
        panel = paper_panel(9.2, 5.25, 0.42).move_to([0, -0.36, 0])
        card = view_card(key, 7.2, 4.15, 0.78 if key in ("front", "rear") else 0.72, True)
        card.move_to([0, -0.34, 0])
        cap = callout(caption, color, 5.7, 20).move_to([4.85, 2.42, 0])
        group = VGroup(panel, card, cap)
        self.fadd(group)
        self.play(FadeIn(panel), FadeIn(card, scale=0.98), FadeIn(cap), run_time=RT_SMOOTH)
        self.wait(PAUSE_VIEW)
        self.play(Indicate(card, color=color, scale_factor=1.015), run_time=RT)
        self.wait(PAUSE_READ)
        self.cleanup(group, run_time=RT)

    def construct(self):
        self.camera.background_color = BG
        for fn in [
            self.opening,
            self.projection,
            self.observer_views,
            self.unfolding,
            self.first_angle,
            self.third_angle,
            self.compare,
            self.symbols,
            self.colombia,
            self.algorithm,
            self.challenge,
            self.closing,
        ]:
            fn()

    def opening(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.88)
        part = mechanical_bracket_3d().scale(0.84).shift(DOWN * 0.45)
        self.play(LaggedStart(*[FadeIn(x, scale=0.97) for x in part[:6]], lag_ratio=0.09), run_time=RT_DRAW)
        self.play(FadeIn(VGroup(*part[6:])), run_time=RT)
        self.begin_ambient_camera_rotation(rate=0.065)

        title = VGroup(
            safe_text("SISTEMA DIÉDRICO", 49, NAVY, BOLD),
            safe_text("De una pieza 3D a vistas 2D", 27, DARK, NORMAL),
            VGroup(
                badge("PRIMER DIEDRO · ISO E", ORANGE, 17),
                badge("TERCER DIEDRO · ISO A", TEAL, 17),
            ).arrange(RIGHT, buff=0.24),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.24)
        self.fadd(title)
        self.play(FadeIn(title[0], shift=DOWN * 0.10), FadeIn(title[1]), FadeIn(title[2]), run_time=RT_SMOOTH)
        self.wait(PAUSE_READ)

        idea = callout("LA PIEZA NO CAMBIA · CAMBIA EL PUNTO DE VISTA", BLUE, 7.8, 22).move_to([0, -3.55, 0])
        self.fadd(idea)
        self.play(FadeIn(idea), run_time=RT)
        self.wait(PAUSE_EXPLAIN)
        self.cleanup(idea, title)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(part), run_time=RT_SMOOTH)

    def projection(self):
        self.transition(1, "PROYECCIÓN ORTOGONAL", "Observador → pieza → rayos paralelos → plano → vista")
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.82)
        h = self.header(1, "PROYECCIÓN ORTOGONAL", "Una dirección exacta produce una vista 2D sin perspectiva.")

        part = mechanical_bracket_3d().scale(0.72).shift(UP * 0.10)
        plane = vertical_projection_plane(-3.25, 7.2, 5.0, 2.35)
        self.play(FadeIn(part), FadeIn(plane[0]), run_time=RT_SMOOTH)
        self.play(LaggedStart(*[Create(g) for g in plane[1]], lag_ratio=0.015), run_time=RT)

        observer = VGroup(observer_icon(BLUE, 0.72), badge("OBSERVADOR", BLUE, 15)).arrange(DOWN, buff=0.10)
        observer.move_to([-5.55, 1.85, 0])
        self.fadd(observer)
        self.play(FadeIn(observer), run_time=RT)

        src = [
            [-3.20, -0.20, 0.42], [-2.75, -0.20, 1.49], [-1.50, -0.20, 1.49],
            [-0.95, -0.20, 1.55], [0.78, -0.20, 1.55], [1.65, -0.20, 3.56],
            [2.84, -0.20, 3.56], [3.20, -0.20, 0.42], [2.25, -0.20, 2.25],
        ]
        rays = VGroup(*[projection_ray(p, [p[0], -3.25, p[2]], ORANGE) for p in src])
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.075), run_time=RT_DRAW)
        tag = self.top_tag("RAYOS PARALELOS · SIN PERSPECTIVA", ORANGE, 5.3)
        self.wait(PAUSE_EXPLAIN)

        trace = front_trace_3d(-3.255, BLUE)
        self.play(Create(trace), run_time=RT_DRAW)
        self.wait(PAUSE_READ)
        self.play(Indicate(trace, color=BLUE), run_time=RT)
        self.wait(PAUSE_READ)
        self.cleanup(tag)

        tag = self.top_tag("CÁMARA ALINEADA CON LA DIRECCIÓN DE OBSERVACIÓN", TEAL, 6.0)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=1.02,
                         run_time=RT_CAMERA, rate_func=smooth)
        self.wait(PAUSE_OBSERVER)
        self.cleanup(tag)
        self.play(FadeOut(rays), FadeOut(part), FadeOut(plane), FadeOut(trace), run_time=RT_SMOOTH)
        self.cleanup(observer)

        self.view_fullscreen("front", BLUE, "ALZADO · PROYECCIÓN RESULTANTE")
        self.cleanup(h)

    def observer_views(self):
        self.transition(2, "SEIS DIRECCIONES PRINCIPALES", "Primero observa en 3D; después confirma la proyección 2D")
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=0.80)
        h = self.header(2, "SEIS VISTAS PRINCIPALES", "Cada pausa fija una dirección antes de mostrar su vista ortográfica.")
        part = mechanical_bracket_3d().scale(0.80).shift(DOWN * 0.20)
        self.play(FadeIn(part), run_time=RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.045)
        self.wait(PAUSE_READ)
        self.stop_ambient_camera_rotation()

        stops = [
            (90, -90, "ALZADO", "front", BLUE, "MIRADA FRONTAL"),
            (0, -90, "PLANTA", "top", TEAL, "MIRADA SUPERIOR"),
            (90, 0, "LATERAL DERECHO", "right", ORANGE, "MIRADA DESDE LA DERECHA"),
            (90, 90, "POSTERIOR", "rear", RED, "MIRADA POSTERIOR"),
            (90, 180, "LATERAL IZQUIERDO", "left", PURPLE, "MIRADA DESDE LA IZQUIERDA"),
            (180, -90, "INFERIOR", "bottom", GREEN, "MIRADA INFERIOR"),
        ]

        for phi, theta, label, key, color, caption in stops:
            tag = self.top_tag(label, color, 4.8)
            self.move_camera(phi=phi * DEGREES, theta=theta * DEGREES, zoom=0.98,
                             run_time=RT_CAMERA, rate_func=smooth)
            self.wait(PAUSE_OBSERVER)
            self.play(Indicate(part, color=color, scale_factor=1.015), run_time=RT_FAST)
            self.wait(PAUSE_BEAT)
            self.play(FadeOut(part), run_time=RT)
            self.cleanup(tag)
            self.view_fullscreen(key, color, caption)
            self.play(FadeIn(part), run_time=RT)

        self.play(FadeOut(part), run_time=RT_SMOOTH)
        overview_title = callout("LAS SEIS VISTAS · MISMA PIEZA", BLUE, 5.0, 21).move_to([0, 2.55, 0])
        cards = VGroup(*[
            view_card(k, 4.55, 2.55, 0.51 if k in ("front", "rear") else 0.49)
            for k in ["front", "top", "right", "left", "rear", "bottom"]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.30, 0.30)).scale(0.89).shift(DOWN * 0.48)
        self.fadd(overview_title, cards)
        self.play(FadeIn(overview_title), LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in cards], lag_ratio=0.10), run_time=RT_DRAW)
        self.wait(PAUSE_LONG)
        self.cleanup(overview_title, cards, h)

    def unfolding(self):
        self.transition(3, "EL SISTEMA DIÉDRICO", "PV y PH son perpendiculares; PH se abate 90°")
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.82)
        h = self.header(3, "PLANOS DIÉDRICOS", "PV = vertical · PH = horizontal · LT = línea de tierra.")

        pv, ph, lt = dihedral_planes(7.0)
        part = mechanical_bracket_3d().scale(0.50).shift(DOWN * 0.12)
        self.play(FadeIn(pv), FadeIn(ph), Create(lt), FadeIn(part), run_time=RT_SMOOTH)

        labels = VGroup(
            badge("PV · ALZADO", BLUE, 15),
            badge("PH · PLANTA", TEAL, 15),
            badge("LT · LÍNEA DE TIERRA", INK, 15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-5.4, 1.70, 0])
        self.fadd(labels)
        self.play(FadeIn(labels), run_time=RT)
        self.wait(PAUSE_EXPLAIN)

        front = front_trace_3d(0.015, BLUE).scale(0.47).shift(UP * 0.16)
        top = orthographic_view("top", 0.38).shift(OUT * 0.03)
        self.play(Create(front), Create(top), run_time=RT_DRAW)
        self.wait(PAUSE_READ)

        ab = callout("ABATIMIENTO · PH GIRA 90° ALREDEDOR DE LT", ORANGE, 6.1, 20).move_to([0, -3.48, 0])
        self.fadd(ab)
        self.play(FadeIn(ab), run_time=RT_FAST)
        self.play(Rotate(ph, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  Rotate(top, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  run_time=RT_CAMERA, rate_func=smooth)
        self.wait(PAUSE_EXPLAIN)
        self.cleanup(ab)

        self.play(FadeOut(pv), FadeOut(ph), FadeOut(lt), FadeOut(part), FadeOut(front), FadeOut(top), run_time=RT_SMOOTH)
        self.cleanup(labels)

        sheet = paper_panel(11.2, 5.7, 0.40).move_to([0, -0.40, 0])
        fv = view_card("front", 5.05, 2.50, 0.52).move_to([-2.75, 0.55, 0])
        tv = view_card("top", 5.05, 2.50, 0.50).move_to([-2.75, -2.02, 0])
        line = Line([-5.15, -0.73, 0], [5.15, -0.73, 0], color=INK, stroke_width=2.2)
        rule = VGroup(
            safe_text("DESPUÉS DEL ABATIMIENTO", 20, BLUE, BOLD),
            safe_text("las vistas comparten una sola lámina 2D", 21, DARK, NORMAL, 5.2),
        ).arrange(DOWN, buff=0.15).move_to([3.1, 0.25, 0])
        group = VGroup(sheet, fv, tv, line, rule)
        self.fadd(group)
        self.play(FadeIn(sheet), Create(line), FadeIn(fv), FadeIn(tv), FadeIn(rule), run_time=RT_DRAW)
        self.wait(PAUSE_LONG)
        self.cleanup(group, h)

    def _angle_method(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        name = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        rule = "LAS VISTAS SE COLOCAN AL LADO OPUESTO" if first else "LAS VISTAS SE COLOCAN EN EL MISMO LADO"
        self.transition(number, name, order)
        h = self.header(number, name, "Primero entiende la posición física; luego lee la distribución en la lámina.")

        # Physical-order lane: deliberately centered below header and above footer.
        observer = observer_icon(color, 0.72).move_to([-5.2, 0.10, 0])
        object_box = RoundedRectangle(width=3.0, height=3.35, corner_radius=0.14,
                                      stroke_color=LIGHT, fill_color=PAPER, fill_opacity=1)
        object_view = orthographic_view("front", 0.39).move_to(object_box)
        object_group = VGroup(object_box, object_view).move_to([0.0 if first else 4.55, 0.05, 0])
        plane = RoundedRectangle(width=0.20, height=3.9, corner_radius=0.05,
                                 stroke_color=BLUE, stroke_width=2.0,
                                 fill_color=PALE_BLUE, fill_opacity=0.65)
        plane.move_to([4.75, 0.05, 0] if first else [-0.45, 0.05, 0])
        arr1 = Arrow([-4.35, 0.05, 0], [-1.8 if first else -1.0, 0.05, 0], buff=0.10,
                     color=color, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        arr2 = Arrow([1.8 if first else 0.2, 0.05, 0], [4.25 if first else 3.0, 0.05, 0], buff=0.10,
                     color=color, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        physical = VGroup(observer, object_group, plane, arr1, arr2)
        self.fadd(physical)
        self.play(FadeIn(observer), run_time=RT)
        if first:
            self.play(FadeIn(object_group), GrowArrow(arr1), run_time=RT_SMOOTH)
            self.play(FadeIn(plane), GrowArrow(arr2), run_time=RT_SMOOTH)
        else:
            self.play(FadeIn(plane), GrowArrow(arr1), run_time=RT_SMOOTH)
            self.play(FadeIn(object_group), GrowArrow(arr2), run_time=RT_SMOOTH)
        order_tag = callout(order, color, 6.0, 21).move_to([0, -3.40, 0])
        self.fadd(order_tag)
        self.play(FadeIn(order_tag), run_time=RT_FAST)
        self.wait(PAUSE_EXPLAIN)
        self.cleanup(physical, order_tag)

        # Large projection sheet. No footer callout; labels live inside their own cards.
        sheet = paper_panel(13.4, 6.00, 0.44).move_to([0, -0.42, 0])
        front = view_card("front", 3.85, 2.20, 0.43).move_to([0, -0.35, 0])
        top = view_card("top", 3.85, 2.15, 0.41)
        right = view_card("right", 3.85, 2.20, 0.43)
        if first:
            top.move_to([0, -2.62, 0])
            right.move_to([-4.15, -0.35, 0])
        else:
            top.move_to([0, 1.92, 0])
            right.move_to([4.15, -0.35, 0])
        rule_tag = callout(rule, color, 6.4, 20).move_to([0, 2.62 if first else -3.32, 0])
        layout = VGroup(sheet, front, top, right, rule_tag)
        self.fadd(layout)
        self.play(FadeIn(sheet), FadeIn(front), run_time=RT_SMOOTH)
        self.wait(PAUSE_READ)
        self.play(FadeIn(top, shift=DOWN * 0.10 if first else UP * 0.10), run_time=RT)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.10 if first else RIGHT * 0.10), run_time=RT)
        self.wait(PAUSE_READ)
        self.play(FadeIn(rule_tag), run_time=RT_FAST)
        self.wait(PAUSE_LONG)
        self.cleanup(layout, h)

    def first_angle(self):
        self._angle_method(True)

    def third_angle(self):
        self._angle_method(False)

    def compare(self):
        self.transition(6, "ISO E vs ISO A", "Mismas vistas; cambia su posición respecto al alzado")
        h = self.header(6, "COMPARACIÓN DIRECTA", "El alzado es el ancla. Observa dónde quedan planta y lateral derecho.")

        left_sheet = paper_panel(7.25, 5.85, 0.46).move_to([-3.95, -0.45, 0])
        right_sheet = paper_panel(7.25, 5.85, 0.46).move_to([3.95, -0.45, 0])
        left_title = badge("PRIMER DIEDRO · ISO E", ORANGE, 17).move_to([-3.95, 2.53, 0])
        right_title = badge("TERCER DIEDRO · ISO A", TEAL, 17).move_to([3.95, 2.53, 0])

        lf = view_card("front", 2.75, 1.72, 0.32).move_to([-3.7, -0.30, 0])
        lt = view_card("top", 2.75, 1.72, 0.31).move_to([-3.7, -2.20, 0])
        lr = view_card("right", 2.75, 1.72, 0.32).move_to([-6.05, -0.30, 0])
        rf = view_card("front", 2.75, 1.72, 0.32).move_to([3.7, -0.30, 0])
        rt = view_card("top", 2.75, 1.72, 0.31).move_to([3.7, 1.55, 0])
        rr = view_card("right", 2.75, 1.72, 0.32).move_to([6.05, -0.30, 0])
        labels = VGroup(
            callout("OPUESTO", ORANGE, 2.5, 18).move_to([-3.95, -3.25, 0]),
            callout("MISMO LADO", TEAL, 2.8, 18).move_to([3.95, -3.25, 0]),
        )
        group = VGroup(left_sheet, right_sheet, left_title, right_title, lf, lt, lr, rf, rt, rr, labels)
        self.fadd(group)
        self.play(FadeIn(left_sheet), FadeIn(right_sheet), FadeIn(left_title), FadeIn(right_title), run_time=RT_SMOOTH)
        self.play(LaggedStart(FadeIn(lf), FadeIn(lt), FadeIn(lr), lag_ratio=0.15), run_time=RT_DRAW)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(FadeIn(rf), FadeIn(rt), FadeIn(rr), lag_ratio=0.15), run_time=RT_DRAW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(labels), run_time=RT)
        self.wait(PAUSE_LONG)
        self.cleanup(group, h)

    def symbols(self):
        self.transition(7, "EL SÍMBOLO LO DECIDE", "Identifica el método antes de interpretar posiciones")
        h = self.header(7, "SÍMBOLOS DE PROYECCIÓN", "El tronco de cono y la vista circular codifican el método.")

        p1 = paper_panel(6.3, 4.55, 0.42).move_to([-3.65, -0.30, 0])
        p3 = paper_panel(6.3, 4.55, 0.42).move_to([3.65, -0.30, 0])
        s1 = projection_symbol(True, 1.28).move_to([-3.65, -0.10, 0])
        s3 = projection_symbol(False, 1.28).move_to([3.65, -0.10, 0])
        t1 = VGroup(safe_text("PRIMER DIEDRO", 28, ORANGE, BOLD), badge("First-angle · ISO E", ORANGE, 17)).arrange(DOWN, buff=0.15).move_to([-3.65, 2.35, 0])
        t3 = VGroup(safe_text("TERCER DIEDRO", 28, TEAL, BOLD), badge("Third-angle · ISO A", TEAL, 17)).arrange(DOWN, buff=0.15).move_to([3.65, 2.35, 0])
        g = VGroup(p1, p3, s1, s3, t1, t3)
        self.fadd(g)
        self.play(FadeIn(p1), FadeIn(p3), FadeIn(t1), FadeIn(t3), run_time=RT_SMOOTH)
        self.play(Create(s1), run_time=RT_DRAW)
        self.wait(PAUSE_READ)
        self.play(Create(s3), run_time=RT_DRAW)
        self.wait(PAUSE_READ)
        reminder = callout("ANTES DE LEER UNA LÁMINA: LOCALIZA ESTE SÍMBOLO", RED, 7.0, 20).move_to([0, -3.42, 0])
        self.fadd(reminder)
        self.play(FadeIn(reminder), run_time=RT)
        self.wait(PAUSE_EXPLAIN)
        self.cleanup(reminder, g, h)

    def colombia(self):
        self.transition(8, "COLOMBIA · NTC 1777:2001", "Norma técnica de representación y métodos de proyección")
        h = self.header(8, "CONTEXTO COLOMBIANO", "NTC 1777:2001 es una norma técnica; no es, por sí sola, una ley.")
        title = safe_text("NTC 1777:2001", 44, NAVY, BOLD)
        cards = VGroup(
            callout("RECONOCE PRIMER DIEDRO", ORANGE, 5.4, 22),
            callout("RECONOCE TERCER DIEDRO", TEAL, 5.4, 22),
            callout("SÍMBOLO → MÉTODO → POSICIÓN DE VISTAS", BLUE, 6.8, 21),
        ).arrange(DOWN, buff=0.32)
        block = VGroup(title, cards).arrange(DOWN, buff=0.42).move_to([0, -0.28, 0])
        self.fadd(block)
        self.play(FadeIn(title), run_time=RT)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in cards], lag_ratio=0.22), run_time=RT_DRAW)
        self.wait(PAUSE_LONG)
        self.cleanup(block, h)

    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(9, "LEE UNA LÁMINA EN 6 PASOS", "Sistema → alzado → distribución → reconstrucción.")

        steps = VGroup(
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 4.45),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 4.45),
            step_chip(3, "UBICA EL ALZADO", BLUE, 4.45),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 4.45),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 4.45),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 4.45),
        ).arrange(DOWN, buff=0.11).move_to([-4.55, -0.42, 0])

        sheet = paper_panel(7.0, 5.65, 0.42).move_to([3.35, -0.42, 0])
        front = view_card("front", 2.65, 1.60, 0.30).move_to([3.35, -0.25, 0])
        top = view_card("top", 2.65, 1.60, 0.29).move_to([3.35, 1.55, 0])
        right = view_card("right", 2.65, 1.60, 0.30).move_to([5.55, -0.25, 0])
        sym = projection_symbol(False, 0.58).move_to([1.35, -2.45, 0])
        self.fadd(steps, sheet, front, top, right, sym)
        self.play(FadeIn(sheet), run_time=RT)

        for i, step in enumerate(steps):
            self.play(FadeIn(step, shift=RIGHT * 0.06), run_time=RT_FAST)
            if i == 0:
                self.play(Create(sym), run_time=RT)
            elif i == 2:
                self.play(FadeIn(front), run_time=RT)
            elif i == 3:
                self.play(FadeIn(top), FadeIn(right), run_time=RT)
            elif i == 4:
                self.play(Circumscribe(VGroup(front, top, right), color=GREEN), run_time=RT)
            self.wait(PAUSE_BEAT)
        self.wait(PAUSE_LONG)
        self.cleanup(steps, sheet, front, top, right, sym, h)

    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        h = self.header(10, "DESAFÍO DE LECTURA", "Con el símbolo dado, ubica planta y lateral derecho.")

        left_panel = paper_panel(4.6, 5.2, 0.42).move_to([-5.15, -0.35, 0])
        sym = projection_symbol(False, 0.90).move_to([-5.15, 0.20, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 16).move_to([-5.15, 2.10, 0])
        main_panel = paper_panel(9.2, 5.2, 0.42).move_to([2.35, -0.35, 0])
        front = view_card("front", 3.05, 1.92, 0.36).move_to([1.55, -0.30, 0])
        top_slot = RoundedRectangle(width=3.05, height=1.92, corner_radius=0.12,
                                    stroke_color=TEAL, fill_color=PALE_TEAL, fill_opacity=0.18).move_to([1.55, 1.80, 0])
        right_slot = RoundedRectangle(width=3.05, height=1.92, corner_radius=0.12,
                                      stroke_color=ORANGE, fill_color=PALE_ORANGE, fill_opacity=0.18).move_to([5.15, -0.30, 0])
        top_q = safe_text("PLANTA ?", 22, TEAL, BOLD).move_to(top_slot)
        right_q = safe_text("LATERAL D. ?", 22, ORANGE, BOLD).move_to(right_slot)
        prompt = callout("PIENSA ANTES DE REVELAR", INK, 5.5, 20).move_to([2.35, -3.30, 0])
        setup = VGroup(left_panel, sym, q, main_panel, front, top_slot, right_slot, top_q, right_q, prompt)
        self.fadd(setup)
        self.play(FadeIn(left_panel), FadeIn(main_panel), Create(sym), FadeIn(q), run_time=RT_DRAW)
        self.play(FadeIn(front), FadeIn(top_slot), FadeIn(right_slot), FadeIn(top_q), FadeIn(right_q), FadeIn(prompt), run_time=RT_SMOOTH)

        dots = VGroup(*[Dot(radius=0.065, color=MID) for _ in range(6)]).arrange(RIGHT, buff=0.12).move_to([2.35, -2.72, 0])
        self.fadd(dots)
        self.play(FadeIn(dots), run_time=RT_FAST)
        for d in dots:
            self.play(d.animate.set_color(BLUE).scale(1.30), run_time=0.22)
            self.play(d.animate.set_color(MID).scale(1 / 1.30), run_time=0.22)
        self.wait(PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.0, 21).move_to([-5.15, -2.15, 0])
        top_view = view_card("top", 3.05, 1.92, 0.35).move_to(top_slot)
        right_view = view_card("right", 3.05, 1.92, 0.36).move_to(right_slot)
        answer = callout("MISMO LADO · PLANTA ARRIBA · LATERAL DERECHO A LA DERECHA", GREEN, 7.6, 20).move_to([2.35, -3.30, 0])
        self.fadd(method, top_view, right_view, answer)
        self.play(FadeOut(prompt), FadeOut(dots), FadeIn(method), run_time=RT)
        self.play(ReplacementTransform(top_slot, top_view), FadeOut(top_q), run_time=RT_SMOOTH)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(right_slot, right_view), FadeOut(right_q), run_time=RT_SMOOTH)
        self.wait(PAUSE_READ)
        self.play(FadeIn(answer), run_time=RT)
        self.wait(PAUSE_LONG)
        self.cleanup(left_panel, sym, q, main_panel, front, method, top_view, right_view, answer, h)

    def closing(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.88)
        part = mechanical_bracket_3d().scale(0.62).shift(RIGHT * 4.7 + DOWN * 0.3)
        self.play(FadeIn(part), run_time=RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.050)
        block = VGroup(
            safe_text("MÉTODO FINAL", 27, BLUE, BOLD),
            safe_text("SÍMBOLO → ALZADO → POSICIÓN → 3D", 35, NAVY, BOLD, 9.2),
            step_chip(1, "IDENTIFICA EL MÉTODO", BLUE, 4.25),
            step_chip(2, "ANCLA EN EL ALZADO", ORANGE, 4.25),
            step_chip(3, "LEE PLANTA Y LATERALES", TEAL, 4.25),
            step_chip(4, "VERIFICA Y RECONSTRUYE", GREEN, 4.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.23).move_to([-2.85, -0.10, 0])
        self.fadd(block)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.08) for x in block], lag_ratio=0.13), run_time=RT_DRAW)
        self.wait(PAUSE_LONG)
        final = callout("3D → 2D SIN AMBIGÜEDAD", GREEN, 5.2, 22).move_to([-2.85, -3.45, 0])
        self.fadd(final)
        self.play(FadeIn(final), run_time=RT)
        self.wait(PAUSE_EXPLAIN)
        self.stop_ambient_camera_rotation()
        self.cleanup(final, block)
        self.play(FadeOut(part), run_time=RT_SMOOTH)
