#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 Senior QA — Sistema diédrico, ISO E / ISO A, NTC 1777:2001.

Full rebuild of V4 pacing/layout while preserving the technically correct
content.  Main goals:
- eliminate figure/text collisions using explicit safe zones;
- enlarge orthographic projections when they are the teaching focus;
- hold every principal observer direction long enough to read;
- make camera changes slower and smoother;
- add visual bridges between 3D observation and 2D projection;
- keep first-angle / third-angle placement unambiguous.

Target: Manim Community Edition 0.20.1, Cairo, 1920x1080, 30 fps.
"""
from __future__ import annotations
import os, sys
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Core.technical_drawing_tools import *
from Core.technical_drawing_tools_v5 import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = BG

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RT_FAST = 0.65
RT = 1.10
RT_SLOW = 1.70
RT_CAMERA = 2.45
RT_REVEAL = 1.45
RT_HERO = 2.20

PAUSE_BEAT = 1.25
PAUSE_READ = 2.80
PAUSE_VIEW = 3.25
PAUSE_EXPLAIN = 4.00
PAUSE_LONG = 5.60
PAUSE_CHALLENGE = 10.0


class DiedricISOProjectionV5SeniorQA(ThreeDScene):
    """Senior classroom version with safe layout and deliberate pacing."""

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def fadd(self, *mobjects):
        self.add_fixed_in_frame_mobjects(*mobjects)
        self.add(*mobjects)

    def frem(self, *mobjects):
        try:
            self.remove_fixed_in_frame_mobjects(*mobjects)
        except Exception:
            pass
        self.remove(*mobjects)

    def fixed_fade_out(self, *mobjects, run_time=RT_FAST):
        if not mobjects:
            return
        self.play(*[FadeOut(m) for m in mobjects], run_time=run_time)
        self.frem(*mobjects)

    def transition(self, number: int, title: str, subtitle: str):
        veil = Rectangle(width=16, height=9, stroke_width=0,
                         fill_color=NAVY, fill_opacity=1)
        num = safe_text(f"{number:02d}", 64, CYAN, BOLD)
        ttl = safe_text(title, 48, PAPER, BOLD, 13.3)
        sub = safe_text(subtitle, 24, "#C8D6E4", NORMAL, 12.8)
        line = Line(LEFT * 2.0, RIGHT * 2.0, color=CYAN, stroke_width=3)
        block = VGroup(num, ttl, line, sub).arrange(DOWN, buff=0.23)
        self.fadd(veil, block)
        self.play(FadeIn(veil), FadeIn(block, shift=UP * 0.18), run_time=RT_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeOut(block, shift=UP * 0.08), FadeOut(veil), run_time=RT)
        self.frem(veil, block)

    def stage_title(self, title: str, subtitle: str, color=BLUE):
        ttl = safe_text(title, 34, NAVY, BOLD, 13.3)
        sub = safe_text(subtitle, 20, DARK, NORMAL, 13.4)
        rule = Line(LEFT * 5.8, RIGHT * 5.8, color=color, stroke_width=2.5)
        group = VGroup(ttl, sub, rule).arrange(DOWN, buff=0.15)
        group.to_edge(UP, buff=0.24)
        self.fadd(group)
        self.play(FadeIn(group, shift=DOWN * 0.08), run_time=RT)
        return group

    def show_note(self, text: str, color=BLUE, width=6.5, size=21):
        n = safe_bottom_callout(text, color, width, size)
        self.fadd(n)
        self.play(FadeIn(n, shift=UP * 0.08), run_time=RT_FAST)
        return n

    def show_large_view(self, key: str, accent: str, hold=PAUSE_VIEW,
                        dimensions=False, footer: str | None = None):
        board = view_reveal_frame(key, accent, 8.5, 5.35, dimensions)
        board.move_to([0, -0.15, 0])
        items = [board]
        if footer:
            note = safe_bottom_callout(footer, accent, 7.1, 21)
            items.append(note)
        group = VGroup(*items)
        self.fadd(group)
        self.play(FadeIn(board, scale=0.985), run_time=RT_REVEAL)
        if footer:
            self.play(FadeIn(items[1], shift=UP * 0.06), run_time=RT_FAST)
        self.wait(hold)
        self.fixed_fade_out(group, run_time=RT)

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.opening,
            self.projection,
            self.directions,
            self.unfolding,
            self.angle_e,
            self.angle_a,
            self.compare,
            self.symbols,
            self.colombia,
            self.algorithm,
            self.challenge,
            self.closing,
        ]
        for scene in scenes:
            scene()

    # ------------------------------------------------------------------
    # OPENING
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.90)
        title = VGroup(
            safe_text("SISTEMA DIÉDRICO", 58, NAVY, BOLD),
            safe_text("De una pieza 3D a vistas 2D sin ambigüedad", 29, DARK),
            VGroup(
                badge("PRIMER DIEDRO · ISO E", ORANGE, 19),
                badge("TERCER DIEDRO · ISO A", TEAL, 19),
            ).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, buff=0.25)
        self.fadd(title)
        self.play(Write(title[0]), FadeIn(title[1], shift=UP * 0.06),
                  FadeIn(title[2], shift=UP * 0.06), run_time=RT_HERO)
        self.wait(PAUSE_EXPLAIN)
        self.fixed_fade_out(title, run_time=RT)

        part = mechanical_bracket_3d().scale(0.92)
        self.play(LaggedStart(*[FadeIn(x, scale=0.97) for x in part], lag_ratio=0.055),
                  run_time=RT_HERO)
        self.begin_ambient_camera_rotation(rate=0.075)
        self.wait(PAUSE_LONG)
        self.stop_ambient_camera_rotation()
        note = self.show_note("La pieza permanece fija. La vista depende de la dirección de observación.", BLUE, 8.2)
        self.wait(PAUSE_EXPLAIN)
        self.fixed_fade_out(note)
        self.play(FadeOut(part), run_time=RT)

    # ------------------------------------------------------------------
    # 1. PROJECTION
    # ------------------------------------------------------------------
    def projection(self):
        self.transition(1, "PROYECCIÓN ORTOGONAL",
                        "Observador → pieza → rayos paralelos → plano → vista 2D")
        intro = self.stage_title("PROYECCIÓN ORTOGONAL",
                                 "Sin perspectiva: cada dirección produce una vista exacta.", BLUE)
        diagram = VGroup(
            step_chip(1, "OBSERVADOR", BLUE, 3.15),
            step_chip(2, "PIEZA", ORANGE, 3.15),
            step_chip(3, "RAYOS PARALELOS", ORANGE, 3.15),
            step_chip(4, "PLANO", CYAN, 3.15),
            step_chip(5, "VISTA 2D", GREEN, 3.15),
        ).arrange(RIGHT, buff=0.20).scale(0.92).move_to([0, -0.20, 0])
        self.fadd(diagram)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.06) for x in diagram],
                              lag_ratio=0.16), run_time=RT_HERO)
        self.wait(PAUSE_READ)
        self.fixed_fade_out(diagram, intro)

        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.78)
        part = mechanical_bracket_3d().scale(0.77)
        plane = vertical_projection_plane(-3.25, 7.2, 5.0, 2.35)
        self.play(FadeIn(part), FadeIn(plane[0]), run_time=RT_SLOW)
        self.play(LaggedStart(*[Create(g) for g in plane[1]], lag_ratio=0.018), run_time=RT)
        self.wait(PAUSE_BEAT)

        src = [
            [-3.2, -.2, .42], [-2.75, -.2, 1.49], [-1.5, -.2, 1.49],
            [-.95, -.2, 1.55], [.78, -.2, 1.55], [1.65, -.2, 3.56],
            [2.84, -.2, 3.56], [3.2, -.2, .42], [2.25, -.2, 2.25],
        ]
        rays = VGroup(*[projection_ray(p, [p[0], -3.25, p[2]], ORANGE) for p in src])
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.07), run_time=RT_HERO)
        note = self.show_note("Los rayos son paralelos: no existe reducción por perspectiva.", ORANGE, 7.4)
        self.wait(PAUSE_EXPLAIN)

        trace = front_trace_3d(-3.255, BLUE)
        self.play(Create(trace), run_time=RT_HERO)
        self.wait(PAUSE_VIEW)
        self.play(Indicate(trace, color=BLUE, scale_factor=1.035), run_time=RT)
        self.fixed_fade_out(note)

        note = self.show_note("Ahora alineamos la cámara con la misma dirección de observación.", TEAL, 7.3)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.94,
                         run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)
        self.fixed_fade_out(note)
        self.play(FadeOut(rays), FadeOut(part), FadeOut(plane), FadeOut(trace), run_time=RT_SLOW)

        self.show_large_view("front", BLUE, PAUSE_LONG, True,
                             "Resultado: una dirección de observación produce un alzado medible.")

    # ------------------------------------------------------------------
    # 2. SIX OBSERVER DIRECTIONS
    # ------------------------------------------------------------------
    def directions(self):
        self.transition(2, "SEIS DIRECCIONES PRINCIPALES",
                        "Cada perspectiva se observa, se pausa y se convierte en su vista 2D")
        self.set_camera_orientation(phi=62 * DEGREES, theta=-45 * DEGREES, zoom=0.82)
        part = mechanical_bracket_3d().scale(0.84)
        self.play(FadeIn(part), run_time=RT_SLOW)
        self.begin_ambient_camera_rotation(rate=0.055)
        self.wait(PAUSE_READ)
        self.stop_ambient_camera_rotation()

        stops = [
            (90, -90, "ALZADO", "front", BLUE,
             "Observamos perpendicularmente al plano frontal."),
            (0, -90, "PLANTA", "top", TEAL,
             "Observamos desde arriba: aparece la huella horizontal."),
            (90, 0, "LATERAL DERECHO", "right", ORANGE,
             "Observamos desde el costado derecho de la pieza."),
            (90, 90, "POSTERIOR", "rear", RED,
             "La misma pieza, ahora desde la cara posterior."),
            (90, 180, "LATERAL IZQUIERDO", "left", PURPLE,
             "El contorno lateral se lee desde el costado opuesto."),
            (180, -90, "INFERIOR", "bottom", GREEN,
             "Observamos desde abajo: la vista inferior completa el conjunto."),
        ]

        for i, (phi, theta, label, key, color, explanation) in enumerate(stops):
            lab = floating_view_label(f"{i+1}/6 · {label}", color)
            self.fadd(lab)
            self.play(FadeIn(lab, shift=RIGHT * 0.06), run_time=RT_FAST)
            self.move_camera(phi=phi * DEGREES, theta=theta * DEGREES, zoom=0.92,
                             run_time=RT_CAMERA)
            self.wait(PAUSE_VIEW)
            self.play(FadeOut(part), run_time=RT)
            self.fixed_fade_out(lab, run_time=RT_FAST)
            self.show_large_view(key, color, PAUSE_VIEW, key in ["front", "top"], explanation)
            self.play(FadeIn(part), run_time=RT)

        self.play(FadeOut(part), run_time=RT_SLOW)

        title = self.stage_title("LAS SEIS VISTAS EN UNA SOLA LÁMINA",
                                 "La escala se reduce solo aquí para comparar el conjunto completo.", BLUE)
        cards = VGroup(*[
            view_card(k, 4.45, 2.56, 0.51 if k in ["front", "rear"] else 0.49)
            for k in ["front", "top", "right", "left", "rear", "bottom"]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.38, 0.34)).scale(0.93).move_to([0, -0.52, 0])
        self.fadd(cards)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.11),
                  run_time=RT_HERO)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(cards, title)

    # ------------------------------------------------------------------
    # 3. DIHEDRAL PLANES AND UNFOLDING
    # ------------------------------------------------------------------
    def unfolding(self):
        self.transition(3, "EL SISTEMA DIÉDRICO",
                        "PV y PH son perpendiculares; después PH se abate 90°")
        self.set_camera_orientation(phi=66 * DEGREES, theta=-45 * DEGREES, zoom=0.82)
        pv, ph, lt = dihedral_planes(7.2)
        part = mechanical_bracket_3d().scale(0.52)
        self.play(FadeIn(pv), FadeIn(ph), Create(lt), FadeIn(part), run_time=RT_HERO)
        self.wait(PAUSE_READ)

        labels = VGroup(
            badge("PV · PLANO VERTICAL", BLUE, 17),
            badge("PH · PLANO HORIZONTAL", TEAL, 17),
            badge("LT · LÍNEA DE TIERRA", INK, 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DL, buff=0.45).shift(UP * 0.55)
        self.fadd(labels)
        self.play(LaggedStart(*[FadeIn(x) for x in labels], lag_ratio=0.14), run_time=RT)
        self.wait(PAUSE_EXPLAIN)

        front = front_trace_3d(0.015, BLUE).scale(0.46).shift(UP * 0.15)
        top = orthographic_view("top", 0.38).shift(OUT * 0.03)
        self.play(Create(front), Create(top), run_time=RT_HERO)
        self.wait(PAUSE_VIEW)

        note = self.show_note("ABATIMIENTO: PH gira exactamente 90° alrededor de LT.", ORANGE, 7.1)
        self.play(Rotate(ph, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  Rotate(top, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)
        self.fixed_fade_out(note, labels)
        self.play(FadeOut(pv), FadeOut(ph), FadeOut(lt), FadeOut(part),
                  FadeOut(front), FadeOut(top), run_time=RT_SLOW)

        title = self.stage_title("DESPUÉS DEL ABATIMIENTO",
                                 "Alzado y planta quedan alineados en una lámina 2D.", ORANGE)
        sheet = paper_panel(12.4, 5.55, 0.42).move_to([0, -0.52, 0])
        fv = large_view_card("front", 5.35, 2.45, 0.56, False, 20).move_to([-3.0, 0.35, 0])
        tv = large_view_card("top", 5.35, 2.45, 0.55, False, 20).move_to([-3.0, -2.18, 0])
        line = Line([-5.72, -0.92, 0], [5.72, -0.92, 0], color=INK, stroke_width=2.2)
        rule = VGroup(
            step_chip(1, "PV → ALZADO", BLUE, 4.25),
            step_chip(2, "PH → PLANTA", TEAL, 4.25),
            step_chip(3, "LT → ALINEACIÓN", ORANGE, 4.25),
        ).arrange(DOWN, buff=0.22).move_to([3.55, -0.52, 0])
        group = VGroup(sheet, fv, tv, line, rule)
        self.fadd(group)
        self.play(FadeIn(sheet), Create(line), run_time=RT)
        self.play(FadeIn(fv), run_time=RT_REVEAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(tv), run_time=RT_REVEAL)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(x) for x in rule], lag_ratio=0.18), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(group, title)

    # ------------------------------------------------------------------
    # 4-5. FIRST / THIRD ANGLE
    # ------------------------------------------------------------------
    def angle_layout(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        method = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        placement = "COLOCACIÓN OPUESTA" if first else "COLOCACIÓN DEL MISMO LADO"
        self.transition(number, method, order)

        title = self.stage_title(method, "Primero entiende la posición física; después memoriza la lámina.", color)
        strip = observer_sequence_strip(first, color).scale(1.08).move_to([0, -0.45, 0])
        order_tag = safe_top_tag(order, color, 6.5, 22)
        self.fadd(strip, order_tag)
        self.play(FadeIn(order_tag), run_time=RT)
        groups, arrows = strip[0], strip[1]
        self.play(FadeIn(groups[0]), run_time=RT_REVEAL)
        self.wait(PAUSE_BEAT)
        for i in range(1, len(groups)):
            self.play(GrowArrow(arrows[i-1]), FadeIn(groups[i]), run_time=RT_REVEAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)
        self.fixed_fade_out(strip, order_tag, title)

        title = self.stage_title("DISTRIBUCIÓN EN LA LÁMINA",
                                 "El alzado es el ancla. Planta y lateral se ubican respecto a él.", color)
        f = large_view_card("front", 5.15, 3.15, 0.58, False, 21).move_to([0, -0.42, 0])
        t = large_view_card("top", 4.75, 2.52, 0.51, False, 20)
        r = large_view_card("right", 4.35, 3.00, 0.52, False, 20)
        self.fadd(f, t, r)
        self.play(FadeIn(f, scale=0.985), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)

        if first:
            top_pos = [0, -2.40, 0]
            side_pos = [-5.45, -0.42, 0]
            rule_text = "PLANTA abajo · lateral derecho a la izquierda"
        else:
            top_pos = [0, 1.84, 0]
            side_pos = [5.45, -0.42, 0]
            rule_text = "PLANTA arriba · lateral derecho a la derecha"

        t.move_to([0, -0.42, 0]).scale(0.90)
        r.move_to([0, -0.42, 0]).scale(0.90)
        self.play(FadeIn(t, scale=0.96), run_time=RT_FAST)
        self.play(t.animate.move_to(top_pos), run_time=RT_CAMERA)
        self.wait(PAUSE_READ)
        self.play(FadeIn(r, scale=0.96), run_time=RT_FAST)
        self.play(r.animate.move_to(side_pos), run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)

        tag = safe_top_tag(placement, color, 5.4, 22)
        rule = safe_bottom_callout(rule_text, color, 7.3, 21)
        self.fadd(tag, rule)
        self.play(FadeIn(tag), FadeIn(rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(f, t, r, tag, rule, title)

    def angle_e(self):
        self.angle_layout(True)

    def angle_a(self):
        self.angle_layout(False)

    # ------------------------------------------------------------------
    # 6. DIRECT COMPARISON
    # ------------------------------------------------------------------
    def compare(self):
        self.transition(6, "MISMAS VISTAS · DISTINTA DISTRIBUCIÓN",
                        "Primero diedro por diedro; después comparación simultánea")

        title = self.stage_title("PRIMER DIEDRO · ISO E",
                                 "Vista lateral derecha → se coloca a la izquierda del alzado.", ORANGE)
        front = large_view_card("front", 5.2, 3.30, 0.60, False, 21).move_to([0, -0.45, 0])
        right = large_view_card("right", 4.3, 3.05, 0.54, False, 20).move_to([-5.25, -0.45, 0])
        top = large_view_card("top", 4.75, 2.48, 0.51, False, 20).move_to([0, -2.46, 0])
        note = safe_bottom_callout("ISO E = colocación OPUESTA", ORANGE, 5.6, 22)
        g = VGroup(front, right, top, note)
        self.fadd(g)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.play(FadeIn(right, shift=RIGHT * 0.08), run_time=RT_REVEAL)
        self.play(FadeIn(top, shift=UP * 0.08), run_time=RT_REVEAL)
        self.play(FadeIn(note), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(g, title)

        title = self.stage_title("TERCER DIEDRO · ISO A",
                                 "Vista lateral derecha → se coloca a la derecha del alzado.", TEAL)
        front = large_view_card("front", 5.2, 3.30, 0.60, False, 21).move_to([0, -0.45, 0])
        right = large_view_card("right", 4.3, 3.05, 0.54, False, 20).move_to([5.25, -0.45, 0])
        top = large_view_card("top", 4.75, 2.48, 0.51, False, 20).move_to([0, 1.58, 0])
        note = safe_bottom_callout("ISO A = colocación DEL MISMO LADO", TEAL, 6.2, 22)
        g = VGroup(front, right, top, note)
        self.fadd(g)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.play(FadeIn(right, shift=LEFT * 0.08), run_time=RT_REVEAL)
        self.play(FadeIn(top, shift=DOWN * 0.08), run_time=RT_REVEAL)
        self.play(FadeIn(note), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(g, title)

        title = self.stage_title("COMPARACIÓN FINAL",
                                 "Las vistas no cambian: cambia únicamente su posición relativa.", BLUE)
        left, right_panel, div = split_comparison_panel()
        lt = safe_text("ISO E · OPUESTO", 24, ORANGE, BOLD).move_to([-3.75, 2.28, 0])
        rt = safe_text("ISO A · MISMO LADO", 24, TEAL, BOLD).move_to([3.75, 2.28, 0])
        left_views = VGroup(
            view_card("front", 3.15, 2.05, 0.38).move_to([-3.55, -0.20, 0]),
            view_card("right", 2.70, 2.05, 0.36).move_to([-6.05, -0.20, 0]),
            view_card("top", 3.15, 1.85, 0.35).move_to([-3.55, -2.28, 0]),
        )
        right_views = VGroup(
            view_card("front", 3.15, 2.05, 0.38).move_to([3.55, -0.20, 0]),
            view_card("right", 2.70, 2.05, 0.36).move_to([6.05, -0.20, 0]),
            view_card("top", 3.15, 1.85, 0.35).move_to([3.55, 1.70, 0]),
        )
        group = VGroup(left, right_panel, div, lt, rt, left_views, right_views)
        self.fadd(group)
        self.play(FadeIn(left), FadeIn(right_panel), Create(div), FadeIn(lt), FadeIn(rt), run_time=RT_SLOW)
        self.play(LaggedStart(*[FadeIn(x) for x in left_views], lag_ratio=0.12), run_time=RT_SLOW)
        self.play(LaggedStart(*[FadeIn(x) for x in right_views], lag_ratio=0.12), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(group, title)

    # ------------------------------------------------------------------
    # 7. SYMBOLS
    # ------------------------------------------------------------------
    def symbols(self):
        self.transition(7, "SÍMBOLOS DE PROYECCIÓN",
                        "El símbolo permite decidir el método antes de leer posiciones")
        title = self.stage_title("SÍMBOLOS DE PROYECCIÓN",
                                 "Tronco de cono + vista circular = método de proyección.", BLUE)
        s1 = projection_symbol(True, 1.32).move_to([-4.0, -0.15, 0])
        s3 = projection_symbol(False, 1.32).move_to([4.0, -0.15, 0])
        l1 = VGroup(safe_text("PRIMER DIEDRO", 30, ORANGE, BOLD),
                    badge("First-angle · ISO E", ORANGE, 19)).arrange(DOWN, buff=0.18).next_to(s1, DOWN, buff=0.55)
        l3 = VGroup(safe_text("TERCER DIEDRO", 30, TEAL, BOLD),
                    badge("Third-angle · ISO A", TEAL, 19)).arrange(DOWN, buff=0.18).next_to(s3, DOWN, buff=0.55)
        g = VGroup(s1, s3, l1, l3)
        self.fadd(g)
        self.play(Create(s1), run_time=RT_HERO)
        self.wait(PAUSE_READ)
        self.play(FadeIn(l1), run_time=RT)
        self.wait(PAUSE_VIEW)
        self.play(Create(s3), run_time=RT_HERO)
        self.wait(PAUSE_READ)
        self.play(FadeIn(l3), run_time=RT)
        self.wait(PAUSE_VIEW)
        note = self.show_note("Regla: identifica el símbolo ANTES de interpretar la distribución de vistas.", RED, 8.0)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(note, g, title)

    # ------------------------------------------------------------------
    # 8. COLOMBIA / NTC
    # ------------------------------------------------------------------
    def colombia(self):
        self.transition(8, "COLOMBIA · NTC 1777:2001",
                        "Contexto técnico para métodos de proyección")
        title = self.stage_title("CONTEXTO COLOMBIANO",
                                 "NTC 1777:2001 es una norma técnica; no es, por sí sola, una ley.", BLUE)
        hero = safe_text("NTC 1777:2001", 50, NAVY, BOLD)
        blocks = VGroup(
            callout("Reconoce PRIMER DIEDRO", ORANGE, 5.7, 23),
            callout("Reconoce TERCER DIEDRO", TEAL, 5.7, 23),
            callout("Símbolo → método → posición correcta", BLUE, 6.4, 22),
        ).arrange(DOWN, buff=0.30)
        group = VGroup(hero, blocks).arrange(DOWN, buff=0.48).move_to([0, -0.35, 0])
        self.fadd(group)
        self.play(FadeIn(hero, shift=UP * 0.08), run_time=RT_REVEAL)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.07) for x in blocks], lag_ratio=0.20), run_time=RT_HERO)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(group, title)

    # ------------------------------------------------------------------
    # 9. READING ALGORITHM
    # ------------------------------------------------------------------
    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA",
                        "Seis pasos claros para cualquier lámina")
        title = self.stage_title("LEE UNA LÁMINA EN 6 PASOS",
                                 "Una sola decisión por vez; la figura grande permanece legible.", BLUE)
        steps_text = [
            ("IDENTIFICA EL SÍMBOLO", BLUE),
            ("DECIDE ISO E / ISO A", ORANGE),
            ("UBICA EL ALZADO", BLUE),
            ("LOCALIZA PLANTA Y LATERALES", TEAL),
            ("VERIFICA OPUESTO / MISMO", GREEN),
            ("RECONSTRUYE EL 3D", PURPLE),
        ]
        left_steps = VGroup(*[
            step_chip(i + 1, txt, col, 5.15)
            for i, (txt, col) in enumerate(steps_text)
        ]).arrange(DOWN, buff=0.13).move_to([-4.65, -0.50, 0])
        sheet = paper_panel(7.2, 5.75, 0.40).move_to([3.55, -0.42, 0])
        sym = projection_symbol(False, 0.66).move_to([1.3, -2.20, 0])
        front = large_view_card("front", 3.7, 2.35, 0.43, False, 18).move_to([3.55, -0.35, 0])
        top = large_view_card("top", 3.7, 1.95, 0.39, False, 17).move_to([3.55, 1.70, 0])
        right = large_view_card("right", 2.8, 2.35, 0.39, False, 17).move_to([5.75, -0.35, 0])
        self.fadd(left_steps, sheet, sym, front, top, right)
        self.play(FadeIn(sheet), run_time=RT)

        for i, step in enumerate(left_steps):
            self.play(FadeIn(step, shift=RIGHT * 0.06), run_time=RT_FAST)
            self.play(Circumscribe(step, color=steps_text[i][1], fade_out=True), run_time=RT)
            if i == 0:
                self.play(Create(sym), run_time=RT_REVEAL)
            elif i == 1:
                method = badge("TERCER DIEDRO · ISO A", TEAL, 16).move_to([3.55, -2.42, 0])
                self.fadd(method)
                self.play(FadeIn(method), run_time=RT)
                self.wait(PAUSE_READ)
                self.fixed_fade_out(method)
            elif i == 2:
                self.play(FadeIn(front), run_time=RT_REVEAL)
            elif i == 3:
                self.play(FadeIn(top), FadeIn(right), run_time=RT_REVEAL)
            elif i == 4:
                self.play(Circumscribe(VGroup(front, top, right), color=GREEN, fade_out=True), run_time=RT_SLOW)
            elif i == 5:
                self.play(Indicate(front, color=PURPLE), Indicate(top, color=PURPLE),
                          Indicate(right, color=PURPLE), run_time=RT)
            self.wait(PAUSE_READ)

        self.wait(PAUSE_LONG)
        self.fixed_fade_out(left_steps, sheet, sym, front, top, right, title)

    # ------------------------------------------------------------------
    # 10. GUIDED CHALLENGE
    # ------------------------------------------------------------------
    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        title = self.stage_title("DESAFÍO DE LECTURA",
                                 "Decide dónde deben ir la planta y el lateral derecho.", BLUE)
        sym = projection_symbol(False, 0.92).move_to([-5.0, 0.75, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 18).next_to(sym, UP, buff=0.30)
        front = large_view_card("front", 4.2, 2.75, 0.49, False, 20).move_to([0, -0.35, 0])
        top_slot = RoundedRectangle(width=4.0, height=2.35, corner_radius=0.14,
                                    stroke_color=TEAL, stroke_width=1.8,
                                    fill_color=PALE_TEAL, fill_opacity=0.18).move_to([0, 1.95, 0])
        right_slot = RoundedRectangle(width=3.35, height=2.75, corner_radius=0.14,
                                      stroke_color=ORANGE, stroke_width=1.8,
                                      fill_color=PALE_ORANGE, fill_opacity=0.18).move_to([5.15, -0.35, 0])
        tq = safe_text("PLANTA ?", 23, TEAL, BOLD).move_to(top_slot)
        rq = safe_text("LATERAL D. ?", 23, ORANGE, BOLD).move_to(right_slot)
        think = safe_bottom_callout("PIENSA ANTES DE REVELAR", INK, 6.0, 22)
        setup = VGroup(sym, q, front, top_slot, right_slot, tq, rq, think)
        self.fadd(setup)
        self.play(Create(sym), FadeIn(q), run_time=RT_REVEAL)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.play(FadeIn(top_slot), FadeIn(tq), FadeIn(right_slot), FadeIn(rq), run_time=RT_REVEAL)
        self.play(FadeIn(think), run_time=RT)

        dots = progress_dots(6, 0)
        self.fadd(dots)
        self.play(FadeIn(dots), run_time=RT_FAST)
        for i in range(6):
            if i > 0:
                new = progress_dots(6, i)
                self.fadd(new)
                self.play(ReplacementTransform(dots, new), run_time=0.35)
                dots = new
            self.wait(0.60)
        self.wait(PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.6, 23).move_to([-5.0, -1.65, 0])
        tv = large_view_card("top", 4.0, 2.35, 0.44, False, 19).move_to(top_slot)
        rv = large_view_card("right", 3.35, 2.75, 0.44, False, 19).move_to(right_slot)
        ans = safe_bottom_callout("MISMO LADO: planta arriba · lateral derecho a la derecha", GREEN, 8.0, 21)
        reveal = VGroup(method, tv, rv, ans)
        self.fadd(reveal)
        self.play(FadeOut(think), FadeOut(dots), FadeIn(method), run_time=RT)
        self.play(ReplacementTransform(top_slot, tv), FadeOut(tq), run_time=RT_CAMERA)
        self.play(ReplacementTransform(right_slot, rv), FadeOut(rq), run_time=RT_CAMERA)
        self.play(FadeIn(ans), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(sym, q, front, method, tv, rv, ans, title)

    # ------------------------------------------------------------------
    # CLOSING
    # ------------------------------------------------------------------
    def closing(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.86)
        part = mechanical_bracket_3d().scale(0.84)
        self.play(FadeIn(part), run_time=RT_SLOW)
        self.begin_ambient_camera_rotation(rate=0.055)
        self.wait(PAUSE_VIEW)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(part), run_time=RT)

        block = VGroup(
            safe_text("MÉTODO FINAL", 29, BLUE, BOLD),
            safe_text("SÍMBOLO → ALZADO → POSICIÓN → 3D", 42, NAVY, BOLD, 12.0),
            VGroup(
                step_chip(1, "IDENTIFICA EL MÉTODO", BLUE, 4.7),
                step_chip(2, "ANCLA EN EL ALZADO", ORANGE, 4.7),
                step_chip(3, "LEE PLANTA Y LATERALES", TEAL, 4.7),
                step_chip(4, "VERIFICA Y RECONSTRUYE", GREEN, 4.7),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.28).move_to([0, -0.25, 0])
        self.fadd(block)
        self.play(FadeIn(block[0]), FadeIn(block[1], shift=UP * 0.06), run_time=RT_SLOW)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.07) for x in block[2]], lag_ratio=0.18),
                  run_time=RT_HERO)
        self.wait(PAUSE_LONG)
        final = safe_bottom_callout("3D → 2D SIN AMBIGÜEDAD", GREEN, 5.6, 24)
        self.fadd(final)
        self.play(FadeIn(final, shift=UP * 0.08), run_time=RT)
        self.wait(PAUSE_EXPLAIN)
        self.fixed_fade_out(final, block)
