#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6 Senior Layout/Camera rebuild — Sistema diédrico ISO E / ISO A.

This version is based on the real V5 PQH render and its frame-by-frame review.
Main corrections:
- global 16:9 safe-area layout with a dedicated header band;
- substantially larger 3D part and orthographic drawings;
- no colour-fill flash/highlight bug on view cards;
- rebalanced first-angle/third-angle sheets;
- larger direct comparison, symbols, algorithm and challenge;
- smoother camera moves and longer stable observer holds;
- less empty space and clearer visual hierarchy.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, -pqh.
"""
from __future__ import annotations

import sys
from pathlib import Path
from manim import *

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for p in (str(HERE.parent / "technical_drawing_diedric_iso_v5_20260909"), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

import diedric_iso_ntc1777_v5 as base
import diedric_iso_ntc1777_v5_final as v5final
from Core.technical_drawing_tools import *

# V6 pacing after visual review of the 404 s V5 render.
base.RT_CAMERA = 2.85
base.PAUSE_OBSERVER = 4.60
base.PAUSE_VIEW = 3.55
base.PAUSE_READ = 2.85
base.PAUSE_LONG = 5.00
base.PAUSE_EXPLAIN = 3.55
base.PAUSE_CHALLENGE = 9.0

SAFE_X = 7.35
HEADER_Y = 4.14
SUBTITLE_Y = 3.48
CONTENT_Y = -0.20


class DiedricISOProjectionV6SeniorLayoutQA(v5final.DiedricISOProjectionV5SeniorFinal):
    """Full-total V6 with corrected size, position and camera staging."""

    # ---------- fixed-frame UI ----------
    def header(self, number, title, subtitle):
        bar = Rectangle(
            width=16.0, height=0.72, stroke_width=0,
            fill_color=NAVY, fill_opacity=1
        ).move_to([0, HEADER_Y, 0])

        nbox = RoundedRectangle(
            width=0.55, height=0.45, corner_radius=0.08,
            stroke_color=CYAN, stroke_width=1.6,
            fill_color=NAVY, fill_opacity=1
        )
        ntext = safe_text(str(number), 20, CYAN, BOLD).move_to(nbox)
        t = safe_text(title, 30, PAPER, BOLD, 12.7)
        row = VGroup(VGroup(nbox, ntext), t).arrange(RIGHT, buff=0.20)
        row.move_to([-6.80 + row.width / 2, HEADER_Y, 0])

        sub = safe_text(subtitle, 18, DARK, NORMAL, 14.2).move_to([0, SUBTITLE_Y, 0])
        h = VGroup(bar, row, sub)
        self.fadd(h)
        self.play(FadeIn(bar), FadeIn(row, shift=RIGHT * 0.05), FadeIn(sub), run_time=base.RT_FAST)
        return h

    def top_tag(self, text, color=BLUE, width=5.1):
        tag = callout(text, color, width, 21).move_to([-5.05, 2.72, 0])
        self.fadd(tag)
        self.play(FadeIn(tag, shift=RIGHT * 0.06), run_time=base.RT_FAST)
        return tag

    def view_fullscreen(self, key, color, caption):
        """True large-view presentation. No Circumscribe fill artefacts."""
        panel = paper_panel(12.45, 6.12, 0.44).move_to([0, -0.22, 0])
        scale_map = {
            "front": 1.18, "rear": 1.18,
            "top": 1.00, "bottom": 1.00,
            "right": 1.08, "left": 1.08,
        }
        card = view_card(key, 10.55, 5.12, scale_map[key], True).move_to([0, -0.22, 0])
        cap = callout(caption, color, 6.8, 21).move_to([0, 2.72, 0])

        outline = RoundedRectangle(
            width=10.78, height=5.35, corner_radius=0.15,
            stroke_color=color, stroke_width=2.4, fill_opacity=0
        ).move_to(card)

        group = VGroup(panel, card, cap)
        self.fadd(group)
        self.play(FadeIn(panel), FadeIn(card, scale=0.985), FadeIn(cap), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_VIEW)
        self.fadd(outline)
        self.play(Create(outline), run_time=base.RT)
        self.wait(base.PAUSE_READ)
        self.play(FadeOut(outline), run_time=base.RT_FAST)
        self.frem(outline)
        self.cleanup(group, run_time=base.RT)

    # ---------- opening ----------
    def opening(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=1.03)
        part = mechanical_bracket_3d().scale(0.98).shift(DOWN * 0.55)
        self.play(LaggedStart(*[FadeIn(x, scale=0.985) for x in part[:6]], lag_ratio=0.08),
                  run_time=base.RT_DRAW)
        self.play(FadeIn(VGroup(*part[6:])), run_time=base.RT)
        self.begin_ambient_camera_rotation(rate=0.050)

        title = VGroup(
            safe_text("SISTEMA DIÉDRICO", 52, NAVY, BOLD),
            safe_text("De una pieza 3D a vistas 2D", 28, DARK, NORMAL),
            VGroup(
                badge("PRIMER DIEDRO · ISO E", ORANGE, 18),
                badge("TERCER DIEDRO · ISO A", TEAL, 18),
            ).arrange(RIGHT, buff=0.28),
        ).arrange(DOWN, buff=0.18).move_to([0, 2.65, 0])

        self.fadd(title)
        self.play(FadeIn(title, shift=DOWN * 0.08), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_READ)

        idea = callout("LA PIEZA NO CAMBIA · CAMBIA EL PUNTO DE VISTA", BLUE, 8.5, 23).move_to([0, -3.55, 0])
        self.fadd(idea)
        self.play(FadeIn(idea), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(idea, title)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(part), run_time=base.RT_SMOOTH)

    # ---------- projection ----------
    def projection(self):
        self.transition(1, "PROYECCIÓN ORTOGONAL", "Observador → pieza → rayos paralelos → plano → vista")
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.98)
        h = self.header(1, "PROYECCIÓN ORTOGONAL", "Una dirección exacta produce una vista 2D sin perspectiva.")

        part = mechanical_bracket_3d().scale(0.88).shift(RIGHT * 0.55 + DOWN * 0.05)
        plane = vertical_projection_plane(-3.45, 8.3, 5.65, 2.45, 0.5)
        self.play(FadeIn(part), FadeIn(plane[0]), run_time=base.RT_SMOOTH)
        self.play(LaggedStart(*[Create(g) for g in plane[1]], lag_ratio=0.012), run_time=base.RT)

        observer = VGroup(observer_icon(BLUE, 0.82), badge("OBSERVADOR", BLUE, 16)).arrange(DOWN, buff=0.10)
        observer.move_to([-6.15, 1.25, 0])
        self.fadd(observer)
        self.play(FadeIn(observer), run_time=base.RT)

        src = [
            [-3.20, -0.20, 0.42], [-2.75, -0.20, 1.49], [-1.50, -0.20, 1.49],
            [-0.95, -0.20, 1.55], [0.78, -0.20, 1.55], [1.65, -0.20, 3.56],
            [2.84, -0.20, 3.56], [3.20, -0.20, 0.42], [2.25, -0.20, 2.25],
        ]
        rays = VGroup(*[projection_ray(p, [p[0], -3.45, p[2]], ORANGE) for p in src])
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.07), run_time=base.RT_DRAW)

        tag = self.top_tag("RAYOS PARALELOS · SIN PERSPECTIVA", ORANGE, 5.55)
        self.wait(base.PAUSE_EXPLAIN)
        trace = front_trace_3d(-3.455, BLUE)
        self.play(Create(trace), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.cleanup(tag)

        tag = self.top_tag("ALINEAR LA CÁMARA = ELIMINAR LA PERSPECTIVA", TEAL, 6.2)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=1.12,
                         run_time=base.RT_CAMERA, rate_func=smooth)
        self.wait(base.PAUSE_OBSERVER)
        self.cleanup(tag)

        self.play(FadeOut(rays), FadeOut(part), FadeOut(plane), FadeOut(trace), run_time=base.RT_SMOOTH)
        self.cleanup(observer)
        self.view_fullscreen("front", BLUE, "ALZADO · PROYECCIÓN RESULTANTE")
        self.cleanup(h)

    # ---------- six principal views ----------
    def observer_views(self):
        self.transition(2, "SEIS DIRECCIONES PRINCIPALES", "Observa en 3D → fija la dirección → confirma la vista 2D")
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=1.03)
        h = self.header(2, "SEIS VISTAS PRINCIPALES",
                        "Cada dirección se mantiene estable antes de mostrar su proyección ortográfica.")

        part = mechanical_bracket_3d().scale(0.98).shift(DOWN * 0.36)
        self.play(FadeIn(part), run_time=base.RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.035)
        self.wait(base.PAUSE_READ)
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
            tag = self.top_tag(label, color, 5.25)
            self.move_camera(phi=phi * DEGREES, theta=theta * DEGREES, zoom=1.15,
                             run_time=base.RT_CAMERA, rate_func=smooth)
            self.wait(base.PAUSE_OBSERVER)

            focus = RoundedRectangle(
                width=4.7, height=3.6, corner_radius=0.16,
                stroke_color=color, stroke_width=2.0, fill_opacity=0
            ).move_to([0, -0.15, 0])
            self.fadd(focus)
            self.play(Create(focus), run_time=base.RT_FAST)
            self.wait(base.PAUSE_BEAT)
            self.play(FadeOut(focus), run_time=base.RT_FAST)
            self.frem(focus)

            self.play(FadeOut(part), run_time=base.RT)
            self.cleanup(tag)
            self.view_fullscreen(key, color, caption)
            self.play(FadeIn(part), run_time=base.RT)

        self.play(FadeOut(part), run_time=base.RT_SMOOTH)

        overview_title = callout("LAS SEIS VISTAS · MISMA PIEZA", BLUE, 5.6, 22).move_to([0, 2.78, 0])
        cards = VGroup(*[
            view_card(k, 4.62, 2.58, 0.55 if k in ("front", "rear") else 0.53)
            for k in ["front", "top", "right", "left", "rear", "bottom"]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.24, 0.24)).shift(DOWN * 0.48)

        self.fadd(overview_title, cards)
        self.play(FadeIn(overview_title),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards], lag_ratio=0.09),
                  run_time=base.RT_DRAW)
        self.wait(base.PAUSE_LONG)
        self.cleanup(overview_title, cards, h)

    # ---------- dihedral planes ----------
    def unfolding(self):
        self.transition(3, "EL SISTEMA DIÉDRICO", "PV y PH son perpendiculares; PH se abate 90°")
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.96)
        h = self.header(3, "PLANOS DIÉDRICOS", "PV = vertical · PH = horizontal · LT = línea de tierra.")

        pv, ph, lt = dihedral_planes(8.2)
        part = mechanical_bracket_3d().scale(0.66).shift(DOWN * 0.10)
        self.play(FadeIn(pv), FadeIn(ph), Create(lt), FadeIn(part), run_time=base.RT_SMOOTH)

        labels = VGroup(
            badge("PV · ALZADO", BLUE, 16),
            badge("PH · PLANTA", TEAL, 16),
            badge("LT · LÍNEA DE TIERRA", INK, 16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([-5.65, 1.55, 0])
        self.fadd(labels)
        self.play(FadeIn(labels), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)

        front = front_trace_3d(0.015, BLUE).scale(0.54).shift(UP * 0.15)
        top = orthographic_view("top", 0.46).shift(OUT * 0.03)
        self.play(Create(front), Create(top), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        ab = callout("ABATIMIENTO · PH GIRA 90° ALREDEDOR DE LT", ORANGE, 6.7, 21).move_to([0, -3.52, 0])
        self.fadd(ab)
        self.play(FadeIn(ab), run_time=base.RT_FAST)
        self.play(Rotate(ph, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  Rotate(top, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  run_time=base.RT_CAMERA, rate_func=smooth)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(ab)

        self.play(FadeOut(pv), FadeOut(ph), FadeOut(lt), FadeOut(part), FadeOut(front), FadeOut(top),
                  run_time=base.RT_SMOOTH)
        self.cleanup(labels)

        sheet = paper_panel(13.0, 6.15, 0.42).move_to([0, -0.25, 0])
        fv = view_card("front", 5.45, 2.67, 0.60).move_to([-3.05, 0.72, 0])
        tv = view_card("top", 5.45, 2.67, 0.58).move_to([-3.05, -2.03, 0])
        line = Line([-5.85, -0.66, 0], [5.85, -0.66, 0], color=INK, stroke_width=2.3)
        rule = VGroup(
            safe_text("DESPUÉS DEL ABATIMIENTO", 23, BLUE, BOLD),
            safe_text("PV y PH quedan en una misma lámina 2D", 22, DARK, NORMAL, 5.4),
        ).arrange(DOWN, buff=0.14).move_to([3.15, 0.35, 0])
        group = VGroup(sheet, fv, tv, line, rule)
        self.fadd(group)
        self.play(FadeIn(sheet), Create(line), FadeIn(fv), FadeIn(tv), FadeIn(rule), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_LONG)
        self.cleanup(group, h)

    # ---------- first / third angle ----------
    def _angle_method(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        name = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        rule = "VISTAS AL LADO OPUESTO" if first else "VISTAS EN EL MISMO LADO"
        self.transition(number, name, order)
        h = self.header(number, name, "Primero interpreta el orden físico; después ubica las vistas en la lámina.")

        observer = observer_icon(color, 0.88).move_to([-6.05, 0.05, 0])
        object_box = RoundedRectangle(width=3.65, height=4.10, corner_radius=0.16,
                                      stroke_color=LIGHT, stroke_width=1.5,
                                      fill_color=PAPER, fill_opacity=1)
        object_view = orthographic_view("front", 0.49).move_to(object_box)
        object_group = VGroup(object_box, object_view).move_to([0.0 if first else 4.85, 0.00, 0])
        plane = RoundedRectangle(width=0.24, height=4.55, corner_radius=0.05,
                                 stroke_color=BLUE, stroke_width=2.3,
                                 fill_color=PALE_BLUE, fill_opacity=0.68)
        plane.move_to([5.45, 0.0, 0] if first else [-0.70, 0.0, 0])

        if first:
            arr1 = Arrow([-5.05, 0, 0], [-2.05, 0, 0], buff=0.10, color=color, stroke_width=3.4)
            arr2 = Arrow([2.00, 0, 0], [5.05, 0, 0], buff=0.10, color=color, stroke_width=3.4)
        else:
            arr1 = Arrow([-5.05, 0, 0], [-1.10, 0, 0], buff=0.10, color=color, stroke_width=3.4)
            arr2 = Arrow([-0.30, 0, 0], [2.95, 0, 0], buff=0.10, color=color, stroke_width=3.4)

        physical = VGroup(observer, object_group, plane, arr1, arr2)
        self.fadd(physical)
        self.play(FadeIn(observer), run_time=base.RT)
        if first:
            self.play(GrowArrow(arr1), FadeIn(object_group), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(plane), run_time=base.RT_SMOOTH)
        else:
            self.play(GrowArrow(arr1), FadeIn(plane), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(object_group), run_time=base.RT_SMOOTH)

        order_tag = callout(order, color, 6.5, 22).move_to([0, -3.42, 0])
        self.fadd(order_tag)
        self.play(FadeIn(order_tag), run_time=base.RT_FAST)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(physical, order_tag)

        sheet = paper_panel(14.0, 6.15, 0.44).move_to([0, -0.25, 0])
        front = view_card("front", 4.55, 2.55, 0.54).move_to([0, -0.10, 0])
        top = view_card("top", 4.55, 2.50, 0.52)
        right = view_card("right", 4.55, 2.55, 0.54)
        if first:
            top.move_to([0, -2.54, 0])
            right.move_to([-4.78, -0.10, 0])
            rule_tag = callout(rule, color, 5.4, 21).move_to([0, 2.66, 0])
        else:
            top.move_to([0, 2.02, 0])
            right.move_to([4.78, -0.10, 0])
            rule_tag = callout(rule, color, 5.4, 21).move_to([0, -3.34, 0])

        layout = VGroup(sheet, front, top, right, rule_tag)
        self.fadd(layout)
        self.play(FadeIn(sheet), FadeIn(front, scale=0.98), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(top, shift=DOWN * 0.08 if first else UP * 0.08), run_time=base.RT)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.08 if first else RIGHT * 0.08), run_time=base.RT)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(rule_tag), run_time=base.RT_FAST)
        self.wait(base.PAUSE_LONG)
        self.cleanup(layout, h)

    # ---------- comparison ----------
    def compare(self):
        self.transition(6, "ISO E vs ISO A", "Mismas vistas; cambia su posición respecto al alzado")
        h = self.header(6, "COMPARACIÓN DIRECTA",
                        "El alzado es el ancla. Compara únicamente la posición de planta y lateral derecho.")

        left_sheet = paper_panel(7.48, 6.05, 0.46).move_to([-3.87, -0.28, 0])
        right_sheet = paper_panel(7.48, 6.05, 0.46).move_to([3.87, -0.28, 0])
        left_title = badge("PRIMER DIEDRO · ISO E", ORANGE, 18).move_to([-3.87, 2.62, 0])
        right_title = badge("TERCER DIEDRO · ISO A", TEAL, 18).move_to([3.87, 2.62, 0])

        lf = view_card("front", 3.05, 1.88, 0.36).move_to([-3.62, -0.18, 0])
        lt = view_card("top", 3.05, 1.88, 0.35).move_to([-3.62, -2.14, 0])
        lr = view_card("right", 3.05, 1.88, 0.36).move_to([-6.02, -0.18, 0])

        rf = view_card("front", 3.05, 1.88, 0.36).move_to([3.62, -0.18, 0])
        rt = view_card("top", 3.05, 1.88, 0.35).move_to([3.62, 1.74, 0])
        rr = view_card("right", 3.05, 1.88, 0.36).move_to([6.02, -0.18, 0])

        labels = VGroup(
            callout("OPUESTO", ORANGE, 2.7, 19).move_to([-3.87, -3.31, 0]),
            callout("MISMO LADO", TEAL, 3.1, 19).move_to([3.87, -3.31, 0]),
        )
        group = VGroup(left_sheet, right_sheet, left_title, right_title, lf, lt, lr, rf, rt, rr, labels)
        self.fadd(group)
        self.play(FadeIn(left_sheet), FadeIn(right_sheet), FadeIn(left_title), FadeIn(right_title),
                  run_time=base.RT_SMOOTH)
        self.play(LaggedStart(FadeIn(lf), FadeIn(lt), FadeIn(lr), lag_ratio=0.16), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(LaggedStart(FadeIn(rf), FadeIn(rt), FadeIn(rr), lag_ratio=0.16), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(labels), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(group, h)

    # ---------- symbols ----------
    def symbols(self):
        self.transition(7, "EL SÍMBOLO LO DECIDE", "Identifica el método antes de interpretar posiciones")
        h = self.header(7, "SÍMBOLOS DE PROYECCIÓN",
                        "El tronco de cono y la vista circular codifican el método de proyección.")

        p1 = paper_panel(6.75, 5.05, 0.44).move_to([-3.62, -0.22, 0])
        p3 = paper_panel(6.75, 5.05, 0.44).move_to([3.62, -0.22, 0])
        t1 = VGroup(safe_text("PRIMER DIEDRO", 31, ORANGE, BOLD),
                    badge("First-angle · ISO E", ORANGE, 18)).arrange(DOWN, buff=0.15).move_to([-3.62, 2.34, 0])
        t3 = VGroup(safe_text("TERCER DIEDRO", 31, TEAL, BOLD),
                    badge("Third-angle · ISO A", TEAL, 18)).arrange(DOWN, buff=0.15).move_to([3.62, 2.34, 0])

        self.fadd(p1, p3, t1, t3)
        self.play(FadeIn(p1), FadeIn(p3), FadeIn(t1), FadeIn(t3), run_time=base.RT_SMOOTH)

        s1 = projection_symbol(True, 1.55).move_to([-3.62, -0.30, 0])
        s3 = projection_symbol(False, 1.55).move_to([3.62, -0.30, 0])
        self.fadd(s1)
        self.play(Create(s1), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.fadd(s3)
        self.play(Create(s3), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        reminder = callout("ANTES DE LEER UNA LÁMINA: LOCALIZA ESTE SÍMBOLO", RED, 7.5, 21).move_to([0, -3.45, 0])
        self.fadd(reminder)
        self.play(FadeIn(reminder), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(reminder, s1, s3, p1, p3, t1, t3, h)

    # ---------- Colombia / NTC ----------
    def colombia(self):
        self.transition(8, "COLOMBIA · NTC 1777:2001", "Norma técnica de representación y métodos de proyección")
        h = self.header(8, "CONTEXTO COLOMBIANO",
                        "NTC 1777:2001 es una norma técnica; no es, por sí sola, una ley.")

        title = safe_text("NTC 1777:2001", 54, NAVY, BOLD)
        cards = VGroup(
            callout("RECONOCE PRIMER DIEDRO", ORANGE, 6.3, 24),
            callout("RECONOCE TERCER DIEDRO", TEAL, 6.3, 24),
            callout("SÍMBOLO → MÉTODO → POSICIÓN DE VISTAS", BLUE, 7.7, 23),
        ).arrange(DOWN, buff=0.38)
        block = VGroup(title, cards).arrange(DOWN, buff=0.48).move_to([0, -0.20, 0])
        self.fadd(block)
        self.play(FadeIn(title), run_time=base.RT)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in cards], lag_ratio=0.20),
                  run_time=base.RT_DRAW)
        self.wait(base.PAUSE_LONG)
        self.cleanup(block, h)

    # ---------- reading algorithm ----------
    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(9, "LEE UNA LÁMINA EN 6 PASOS",
                        "Sistema → alzado → distribución → reconstrucción.")

        steps = [
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 5.05),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 5.05),
            step_chip(3, "UBICA EL ALZADO", BLUE, 5.05),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 5.05),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 5.05),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 5.05),
        ]
        step_group = VGroup(*steps).arrange(DOWN, buff=0.12).move_to([-4.85, -0.32, 0])

        sheet = paper_panel(8.05, 5.90, 0.42).move_to([3.25, -0.32, 0])
        self.fadd(sheet)
        self.play(FadeIn(sheet), run_time=base.RT)

        sym = projection_symbol(False, 0.72).move_to([0.45, -2.62, 0])
        method = badge("ISO A · TERCER DIEDRO", TEAL, 17).move_to([4.75, -2.64, 0])
        front = view_card("front", 3.15, 1.92, 0.36).move_to([3.15, -0.15, 0])
        top = view_card("top", 3.15, 1.92, 0.35).move_to([3.15, 1.92, 0])
        right = view_card("right", 3.15, 1.92, 0.36).move_to([5.72, -0.15, 0])
        reconstruction = callout("VISTAS COHERENTES → FORMA 3D", PURPLE, 5.3, 19).move_to([3.45, -2.62, 0])

        for i, step in enumerate(steps):
            self.fadd(step)
            self.play(FadeIn(step, shift=RIGHT * 0.06), run_time=base.RT_FAST)
            if i == 0:
                self.fadd(sym); self.play(Create(sym), run_time=base.RT)
            elif i == 1:
                self.fadd(method); self.play(FadeIn(method), run_time=base.RT)
            elif i == 2:
                self.fadd(front); self.play(FadeIn(front, scale=0.98), run_time=base.RT)
            elif i == 3:
                self.fadd(top, right)
                self.play(FadeIn(top, shift=DOWN * 0.05), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeIn(right, shift=LEFT * 0.05), run_time=base.RT)
            elif i == 4:
                guide = RoundedRectangle(width=6.0, height=4.4, corner_radius=0.18,
                                         stroke_color=GREEN, stroke_width=2.2, fill_opacity=0).move_to([4.0, 0.7, 0])
                self.fadd(guide); self.play(Create(guide), run_time=base.RT); self.play(FadeOut(guide), run_time=base.RT_FAST); self.frem(guide)
            elif i == 5:
                self.fadd(reconstruction)
                self.play(ReplacementTransform(method, reconstruction), run_time=base.RT_SMOOTH)
                self.frem(method)
            self.wait(1.65)

        self.wait(base.PAUSE_LONG)
        self.cleanup(*steps, sheet, sym, front, top, right, reconstruction, h)

    # ---------- guided challenge ----------
    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        h = self.header(10, "DESAFÍO DE LECTURA",
                        "Con el símbolo dado, ubica la planta y el lateral derecho.")

        left_panel = paper_panel(4.75, 5.55, 0.42).move_to([-5.28, -0.27, 0])
        sym = projection_symbol(False, 1.05).move_to([-5.28, 0.10, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 17).move_to([-5.28, 2.30, 0])
        self.fadd(left_panel, q)
        self.play(FadeIn(left_panel), FadeIn(q), run_time=base.RT)
        self.fadd(sym); self.play(Create(sym), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        main_panel = paper_panel(9.55, 5.55, 0.42).move_to([2.40, -0.27, 0])
        front = view_card("front", 3.45, 2.10, 0.40).move_to([1.55, -0.20, 0])
        self.fadd(main_panel, front)
        self.play(FadeIn(main_panel), FadeIn(front, scale=0.98), run_time=base.RT_SMOOTH)

        top_slot = RoundedRectangle(width=3.45, height=2.10, corner_radius=0.13,
                                    stroke_color=TEAL, stroke_width=1.8,
                                    fill_color=PALE_TEAL, fill_opacity=0.16).move_to([1.55, 2.05, 0])
        right_slot = RoundedRectangle(width=3.45, height=2.10, corner_radius=0.13,
                                      stroke_color=ORANGE, stroke_width=1.8,
                                      fill_color=PALE_ORANGE, fill_opacity=0.16).move_to([5.38, -0.20, 0])
        top_q = safe_text("PLANTA ?", 24, TEAL, BOLD).move_to(top_slot)
        right_q = safe_text("LATERAL D. ?", 24, ORANGE, BOLD).move_to(right_slot)
        prompt = callout("PIENSA ANTES DE REVELAR", INK, 5.8, 21).move_to([2.40, -3.38, 0])
        self.fadd(top_slot, right_slot, top_q, right_q, prompt)
        self.play(FadeIn(top_slot), FadeIn(right_slot), FadeIn(top_q), FadeIn(right_q), FadeIn(prompt),
                  run_time=base.RT_SMOOTH)

        dots = VGroup(*[Dot(radius=0.07, color=MID) for _ in range(6)]).arrange(RIGHT, buff=0.14).move_to([2.40, -2.78, 0])
        self.fadd(dots); self.play(FadeIn(dots), run_time=base.RT_FAST)
        for d in dots:
            self.play(d.animate.set_color(BLUE).scale(1.25), run_time=0.24)
            self.play(d.animate.set_color(MID).scale(0.80), run_time=0.24)
        self.wait(base.PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.3, 22).move_to([-5.28, -2.35, 0])
        self.fadd(method)
        self.play(FadeOut(prompt), FadeOut(dots), FadeIn(method), run_time=base.RT)
        self.wait(base.PAUSE_READ)

        top_view = view_card("top", 3.45, 2.10, 0.39).move_to(top_slot)
        self.fadd(top_view)
        self.play(ReplacementTransform(top_slot, top_view), FadeOut(top_q), run_time=base.RT_SMOOTH)
        self.frem(top_slot, top_q)
        self.wait(base.PAUSE_VIEW)

        right_view = view_card("right", 3.45, 2.10, 0.40).move_to(right_slot)
        self.fadd(right_view)
        self.play(ReplacementTransform(right_slot, right_view), FadeOut(right_q), run_time=base.RT_SMOOTH)
        self.frem(right_slot, right_q)
        self.wait(base.PAUSE_VIEW)

        answer = callout("MISMO LADO · PLANTA ARRIBA · LATERAL DERECHO A LA DERECHA",
                         GREEN, 8.1, 21).move_to([2.40, -3.38, 0])
        self.fadd(answer); self.play(FadeIn(answer), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(left_panel, sym, q, main_panel, front, method, top_view, right_view, answer, h)

    # ---------- closing ----------
    def closing(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=1.00)
        part = mechanical_bracket_3d().scale(0.82).shift(RIGHT * 4.45 + DOWN * 0.40)
        self.play(FadeIn(part), run_time=base.RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.042)

        block = VGroup(
            safe_text("MÉTODO FINAL", 29, BLUE, BOLD),
            safe_text("SÍMBOLO → ALZADO → POSICIÓN → 3D", 37, NAVY, BOLD, 8.6),
            step_chip(1, "IDENTIFICA EL MÉTODO", BLUE, 4.75),
            step_chip(2, "ANCLA EN EL ALZADO", ORANGE, 4.75),
            step_chip(3, "LEE PLANTA Y LATERALES", TEAL, 4.75),
            step_chip(4, "VERIFICA Y RECONSTRUYE", GREEN, 4.75),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-3.10, -0.05, 0])
        self.fadd(block)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.06) for x in block], lag_ratio=0.12),
                  run_time=base.RT_DRAW)
        self.wait(base.PAUSE_LONG)

        final = callout("3D → 2D SIN AMBIGÜEDAD", GREEN, 5.8, 23).move_to([-3.10, -3.42, 0])
        self.fadd(final); self.play(FadeIn(final), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.stop_ambient_camera_rotation()
        self.cleanup(final, block)
        self.play(FadeOut(part), run_time=base.RT_SMOOTH)
