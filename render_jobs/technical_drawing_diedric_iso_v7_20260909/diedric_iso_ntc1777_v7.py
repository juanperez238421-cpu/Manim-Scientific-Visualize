#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V7 Safe-Layout rebuild — Sistema diédrico ISO E / ISO A.

This version is a direct visual correction of the real V6 PQH render.
The user-supplied frames and the V6 QA contact sheet exposed four concrete
layout failures:

1) opening / six observer directions: the 3D bracket occupied the title and
   subtitle bands because the camera zoom and object scale were too aggressive;
2) first/third-angle sheets: vertical spacing between FRONT and TOP cards was
   insufficient, especially in third-angle projection;
3) direct comparison: card widths/heights exceeded the half-sheet cells and
   labels collided across the ISO E / ISO A layouts;
4) six-step algorithm: TOP/FRONT/RIGHT cards and the projection symbol shared
   the same lower-right space, causing visible overlap and visual clutter.

V7 uses explicit safe rectangles, compact projection tiles, smaller 3D camera
framing, and a strict no-overlap cross-layout for ISO E / ISO A.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, -pqh.
"""
from __future__ import annotations

import sys
from pathlib import Path
from manim import *

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V6_DIR = HERE.parent / "technical_drawing_diedric_iso_v6_20260909"
for p in (str(V6_DIR), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

import diedric_iso_ntc1777_v6 as v6
import diedric_iso_ntc1777_v5 as base
from Core.technical_drawing_tools import *

# Keep the deliberate V6 pacing, but slightly lengthen observer holds.
base.RT_CAMERA = 2.95
base.PAUSE_OBSERVER = 4.90
base.PAUSE_VIEW = 3.55
base.PAUSE_READ = 2.90
base.PAUSE_LONG = 5.00
base.PAUSE_EXPLAIN = 3.60
base.PAUSE_CHALLENGE = 9.0


class DiedricISOProjectionV7SafeLayout(v6.DiedricISOProjectionV6SeniorLayoutQA):
    """V7 full-total scene with strict safe-area composition."""

    # ------------------------------------------------------------------
    # reusable compact 2D projection tile
    # ------------------------------------------------------------------
    def compact_tile(
        self,
        key: str,
        label: str,
        color: str,
        width: float = 2.35,
        height: float = 1.55,
        view_scale: float = 0.30,
    ) -> VGroup:
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=LIGHT,
            stroke_width=1.25,
            fill_color=PAPER,
            fill_opacity=1,
        )
        accent = Line(
            panel.get_corner(UL) + RIGHT * 0.12,
            panel.get_corner(UR) + LEFT * 0.12,
            stroke_color=color,
            stroke_width=3.0,
        )
        title = safe_text(label, 14, color, BOLD, width - 0.28).next_to(
            panel.get_top(), DOWN, buff=0.10
        )
        view = orthographic_view(key, view_scale, False)
        if view.width > width - 0.28:
            view.scale_to_fit_width(width - 0.28)
        if view.height > height - 0.48:
            view.scale_to_fit_height(height - 0.48)
        view.move_to(panel).shift(DOWN * 0.09)
        return VGroup(panel, accent, title, view)

    def projector_pair(self, a: Mobject, b: Mobject, color=MID) -> VGroup:
        """Subtle alignment guides between two orthographic tiles."""
        ax = a.get_center()[0]
        ay = a.get_center()[1]
        bx = b.get_center()[0]
        by = b.get_center()[1]
        guides = VGroup()
        if abs(ax - bx) < 0.25:
            guides.add(
                DashedLine(
                    [ax, min(ay, by) + 0.72, 0],
                    [bx, max(ay, by) - 0.72, 0],
                    dash_length=0.10,
                    stroke_color=color,
                    stroke_width=1.0,
                    stroke_opacity=0.55,
                )
            )
        if abs(ay - by) < 0.25:
            guides.add(
                DashedLine(
                    [min(ax, bx) + 1.05, ay, 0],
                    [max(ax, bx) - 1.05, by, 0],
                    dash_length=0.10,
                    stroke_color=color,
                    stroke_width=1.0,
                    stroke_opacity=0.55,
                )
            )
        return guides

    # ------------------------------------------------------------------
    # opening — lower the real 3D bracket and protect title hierarchy
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.82)

        # Z translation (IN) lowers the bracket in the projected screen much
        # more consistently than the V6 Y-only shift.
        part = mechanical_bracket_3d().scale(0.80).shift(IN * 0.92 + DOWN * 0.12)
        self.play(
            LaggedStart(*[FadeIn(x, scale=0.985) for x in part[:6]], lag_ratio=0.08),
            run_time=base.RT_DRAW,
        )
        self.play(FadeIn(VGroup(*part[6:])), run_time=base.RT)
        self.begin_ambient_camera_rotation(rate=0.046)

        title_back = Rectangle(
            width=16.0,
            height=2.35,
            stroke_width=0,
            fill_color=BG,
            fill_opacity=0.96,
        ).move_to([0, 3.30, 0])
        title = VGroup(
            safe_text("SISTEMA DIÉDRICO", 50, NAVY, BOLD),
            safe_text("De una pieza 3D a vistas 2D", 27, DARK, NORMAL),
            VGroup(
                badge("PRIMER DIEDRO · ISO E", ORANGE, 17),
                badge("TERCER DIEDRO · ISO A", TEAL, 17),
            ).arrange(RIGHT, buff=0.28),
        ).arrange(DOWN, buff=0.16).move_to([0, 2.78, 0])
        self.fadd(title_back, title)
        self.play(FadeIn(title_back), FadeIn(title, shift=DOWN * 0.06), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_READ)

        idea = callout(
            "LA PIEZA NO CAMBIA · CAMBIA EL PUNTO DE VISTA",
            BLUE, 8.3, 22,
        ).move_to([0, -3.42, 0])
        self.fadd(idea)
        self.play(FadeIn(idea), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(idea, title, title_back)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(part), run_time=base.RT_SMOOTH)

    # ------------------------------------------------------------------
    # observer views — eliminate top clipping and oversized silhouettes
    # ------------------------------------------------------------------
    def observer_views(self):
        self.transition(
            2,
            "SEIS DIRECCIONES PRINCIPALES",
            "Observa en 3D → fija la dirección → confirma la vista 2D",
        )
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=0.88)
        h = self.header(
            2,
            "SEIS VISTAS PRINCIPALES",
            "Cada dirección se mantiene estable antes de mostrar su proyección ortográfica.",
        )

        part = mechanical_bracket_3d().scale(0.74).shift(IN * 0.55)
        self.play(FadeIn(part), run_time=base.RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.030)
        self.wait(base.PAUSE_READ)
        self.stop_ambient_camera_rotation()

        # Per-view zooms are intentionally < 1.0. V6 used 1.15 for every view,
        # which produced the clipping visible at ~01:10 and ~02:21.
        stops = [
            (90, -90, 0.88, "ALZADO", "front", BLUE, "MIRADA FRONTAL"),
            (0, -90, 0.82, "PLANTA", "top", TEAL, "MIRADA SUPERIOR"),
            (90, 0, 0.92, "LATERAL DERECHO", "right", ORANGE, "MIRADA DESDE LA DERECHA"),
            (90, 90, 0.88, "POSTERIOR", "rear", RED, "MIRADA POSTERIOR"),
            (90, 180, 0.92, "LATERAL IZQUIERDO", "left", PURPLE, "MIRADA DESDE LA IZQUIERDA"),
            (180, -90, 0.82, "INFERIOR", "bottom", GREEN, "MIRADA INFERIOR"),
        ]

        for phi, theta, zoom, label, key, color, caption in stops:
            tag = callout(label, color, 4.80, 20).move_to([-5.10, 2.47, 0])
            self.fadd(tag)
            self.play(FadeIn(tag, shift=RIGHT * 0.05), run_time=base.RT_FAST)
            self.move_camera(
                phi=phi * DEGREES,
                theta=theta * DEGREES,
                zoom=zoom,
                run_time=base.RT_CAMERA,
                rate_func=smooth,
            )
            self.wait(base.PAUSE_OBSERVER)

            focus = RoundedRectangle(
                width=6.00,
                height=4.25,
                corner_radius=0.15,
                stroke_color=color,
                stroke_width=1.8,
                fill_opacity=0,
            ).move_to([0, -0.48, 0])
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

        overview_title = callout(
            "LAS SEIS VISTAS · MISMA PIEZA", BLUE, 5.4, 21
        ).move_to([0, 2.66, 0])
        cards = VGroup(*[
            view_card(k, 4.35, 2.30, 0.49 if k in ("front", "rear") else 0.47)
            for k in ["front", "top", "right", "left", "rear", "bottom"]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.32, 0.30)).shift(DOWN * 0.56)
        self.fadd(overview_title, cards)
        self.play(
            FadeIn(overview_title),
            LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards], lag_ratio=0.09),
            run_time=base.RT_DRAW,
        )
        self.wait(base.PAUSE_LONG)
        self.cleanup(overview_title, cards, h)

    # ------------------------------------------------------------------
    # ISO E / ISO A — strict cross-layout, no card overlap
    # ------------------------------------------------------------------
    def _angle_method(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        name = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        rule = "VISTAS AL LADO OPUESTO" if first else "VISTAS EN EL MISMO LADO"
        self.transition(number, name, order)
        h = self.header(
            number,
            name,
            "Primero interpreta el orden físico; después ubica las vistas en la lámina.",
        )

        # Physical order: keep the useful V6 concept, but reduce the object box
        # and move the sequence below the subtitle band.
        observer = observer_icon(color, 0.82).move_to([-5.95, -0.10, 0])
        object_box = RoundedRectangle(
            width=3.25,
            height=3.65,
            corner_radius=0.15,
            stroke_color=LIGHT,
            stroke_width=1.4,
            fill_color=PAPER,
            fill_opacity=1,
        )
        object_view = orthographic_view("front", 0.44).move_to(object_box)
        object_group = VGroup(object_box, object_view).move_to([0.0 if first else 4.55, -0.15, 0])
        plane = RoundedRectangle(
            width=0.22,
            height=4.10,
            corner_radius=0.05,
            stroke_color=BLUE,
            stroke_width=2.1,
            fill_color=PALE_BLUE,
            fill_opacity=0.68,
        )
        plane.move_to([5.20, -0.15, 0] if first else [-0.75, -0.15, 0])
        if first:
            arr1 = Arrow([-5.00, -0.15, 0], [-1.85, -0.15, 0], buff=0.10, color=color, stroke_width=3.2)
            arr2 = Arrow([1.80, -0.15, 0], [4.80, -0.15, 0], buff=0.10, color=color, stroke_width=3.2)
        else:
            arr1 = Arrow([-5.00, -0.15, 0], [-1.15, -0.15, 0], buff=0.10, color=color, stroke_width=3.2)
            arr2 = Arrow([-0.35, -0.15, 0], [2.80, -0.15, 0], buff=0.10, color=color, stroke_width=3.2)
        physical = VGroup(observer, object_group, plane, arr1, arr2)
        self.fadd(physical)
        self.play(FadeIn(observer), run_time=base.RT)
        if first:
            self.play(GrowArrow(arr1), FadeIn(object_group), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(plane), run_time=base.RT_SMOOTH)
        else:
            self.play(GrowArrow(arr1), FadeIn(plane), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(object_group), run_time=base.RT_SMOOTH)
        order_tag = callout(order, color, 6.2, 21).move_to([0, -3.25, 0])
        self.fadd(order_tag)
        self.play(FadeIn(order_tag), run_time=base.RT_FAST)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(physical, order_tag)

        # Projection sheet. Each tile occupies a non-intersecting cell.
        sheet = paper_panel(13.8, 5.72, 0.42).move_to([0, -0.30, 0])
        front = view_card("front", 3.80, 1.95, 0.43)
        top = view_card("top", 3.80, 1.95, 0.41)
        right = view_card("right", 3.80, 1.95, 0.43)

        if first:
            front.move_to([0.00, 0.48, 0])
            top.move_to([0.00, -1.72, 0])
            right.move_to([-4.18, 0.48, 0])
            rule_tag = callout(rule, color, 4.8, 19).move_to([4.15, -1.75, 0])
        else:
            front.move_to([0.00, -0.58, 0])
            top.move_to([0.00, 1.62, 0])
            right.move_to([4.18, -0.58, 0])
            rule_tag = callout(rule, color, 4.8, 19).move_to([-4.15, 1.62, 0])

        g1 = self.projector_pair(front, top, MID)
        g2 = self.projector_pair(front, right, MID)
        guides = VGroup(g1, g2)
        layout = VGroup(sheet, guides, front, top, right, rule_tag)
        self.fadd(layout)
        self.play(FadeIn(sheet), FadeIn(front, scale=0.98), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(top, shift=DOWN * 0.06 if first else UP * 0.06), run_time=base.RT)
        self.play(Create(g1), run_time=base.RT_FAST)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.06 if first else RIGHT * 0.06), run_time=base.RT)
        self.play(Create(g2), run_time=base.RT_FAST)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(rule_tag), run_time=base.RT_FAST)
        self.wait(base.PAUSE_LONG)
        self.cleanup(layout, h)

    # ------------------------------------------------------------------
    # direct comparison — two independent cross diagrams
    # ------------------------------------------------------------------
    def compare(self):
        self.transition(6, "ISO E vs ISO A", "Mismas vistas; cambia su posición respecto al alzado")
        h = self.header(
            6,
            "COMPARACIÓN DIRECTA",
            "El alzado es el ancla. Compara únicamente la posición de planta y lateral derecho.",
        )

        left_sheet = paper_panel(7.15, 5.70, 0.44).move_to([-3.72, -0.30, 0])
        right_sheet = paper_panel(7.15, 5.70, 0.44).move_to([3.72, -0.30, 0])
        left_title = badge("PRIMER DIEDRO · ISO E", ORANGE, 16).move_to([-3.72, 2.32, 0])
        right_title = badge("TERCER DIEDRO · ISO A", TEAL, 16).move_to([3.72, 2.32, 0])

        # ISO E: right view left of front; top view below front.
        lf = self.compact_tile("front", "ALZADO", BLUE, 2.18, 1.48, 0.28).move_to([-3.22, 0.45, 0])
        lt = self.compact_tile("top", "PLANTA", TEAL, 2.18, 1.48, 0.27).move_to([-3.22, -1.28, 0])
        lr = self.compact_tile("right", "LATERAL D.", ORANGE, 2.18, 1.48, 0.28).move_to([-5.55, 0.45, 0])

        # ISO A: right view right of front; top view above front.
        rf = self.compact_tile("front", "ALZADO", BLUE, 2.18, 1.48, 0.28).move_to([3.22, -0.52, 0])
        rt = self.compact_tile("top", "PLANTA", TEAL, 2.18, 1.48, 0.27).move_to([3.22, 1.20, 0])
        rr = self.compact_tile("right", "LATERAL D.", ORANGE, 2.18, 1.48, 0.28).move_to([5.55, -0.52, 0])

        left_guides = VGroup(self.projector_pair(lf, lt), self.projector_pair(lf, lr))
        right_guides = VGroup(self.projector_pair(rf, rt), self.projector_pair(rf, rr))
        labels = VGroup(
            callout("OPUESTO", ORANGE, 2.55, 18).move_to([-3.72, -2.72, 0]),
            callout("MISMO LADO", TEAL, 2.85, 18).move_to([3.72, -2.72, 0]),
        )

        group = VGroup(
            left_sheet, right_sheet, left_title, right_title,
            left_guides, right_guides,
            lf, lt, lr, rf, rt, rr, labels,
        )
        self.fadd(group)
        self.play(
            FadeIn(left_sheet), FadeIn(right_sheet),
            FadeIn(left_title), FadeIn(right_title),
            run_time=base.RT_SMOOTH,
        )
        self.play(FadeIn(lf), FadeIn(lt), FadeIn(lr), Create(left_guides), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(rf), FadeIn(rt), FadeIn(rr), Create(right_guides), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(labels), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(group, h)

    # ------------------------------------------------------------------
    # six-step reading algorithm — dedicated cells, no lower-right collision
    # ------------------------------------------------------------------
    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(
            9,
            "LEE UNA LÁMINA EN 6 PASOS",
            "Sistema → alzado → distribución → reconstrucción.",
        )

        steps = [
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 4.60),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 4.60),
            step_chip(3, "UBICA EL ALZADO", BLUE, 4.60),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 4.60),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 4.60),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 4.60),
        ]
        VGroup(*steps).arrange(DOWN, buff=0.13).move_to([-4.95, -0.35, 0])

        sheet = paper_panel(7.65, 5.78, 0.42).move_to([3.42, -0.34, 0])
        self.fadd(sheet)
        self.play(FadeIn(sheet), run_time=base.RT)

        # Dedicated cells: symbol/method on the left inside the sheet,
        # orthographic cross on the right, reconstruction at the bottom.
        sym = projection_symbol(False, 0.55).move_to([0.90, 1.58, 0])
        method = badge("ISO A · TERCER DIEDRO", TEAL, 15).move_to([1.20, 0.45, 0])
        front = self.compact_tile("front", "ALZADO", BLUE, 2.40, 1.48, 0.29).move_to([4.35, -0.28, 0])
        top = self.compact_tile("top", "PLANTA", TEAL, 2.40, 1.48, 0.28).move_to([4.35, 1.42, 0])
        right = self.compact_tile("right", "LATERAL D.", ORANGE, 2.40, 1.48, 0.29).move_to([6.30, -0.28, 0])
        reconstruction = callout(
            "VISTAS COHERENTES → FORMA 3D", PURPLE, 5.10, 18
        ).move_to([3.95, -2.48, 0])

        for i, step in enumerate(steps):
            self.fadd(step)
            self.play(FadeIn(step, shift=RIGHT * 0.06), run_time=base.RT_FAST)
            if i == 0:
                self.fadd(sym)
                self.play(Create(sym), run_time=base.RT)
            elif i == 1:
                self.fadd(method)
                self.play(FadeIn(method), run_time=base.RT)
            elif i == 2:
                self.fadd(front)
                self.play(FadeIn(front, scale=0.98), run_time=base.RT)
            elif i == 3:
                self.fadd(top, right)
                self.play(FadeIn(top, shift=DOWN * 0.05), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeIn(right, shift=LEFT * 0.05), run_time=base.RT)
            elif i == 4:
                guides = VGroup(self.projector_pair(front, top), self.projector_pair(front, right))
                self.fadd(guides)
                self.play(Create(guides), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeOut(guides), run_time=base.RT_FAST)
                self.frem(guides)
            elif i == 5:
                self.fadd(reconstruction)
                self.play(FadeIn(reconstruction, shift=UP * 0.05), run_time=base.RT_SMOOTH)
            self.wait(1.55)

        self.wait(base.PAUSE_LONG)
        self.cleanup(*steps, sheet, sym, method, front, top, right, reconstruction, h)

    # ------------------------------------------------------------------
    # challenge — same safe tile system used in the teaching example
    # ------------------------------------------------------------------
    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        h = self.header(
            10,
            "DESAFÍO DE LECTURA",
            "Con el símbolo dado, ubica la planta y el lateral derecho.",
        )

        left_panel = paper_panel(4.55, 5.35, 0.42).move_to([-5.25, -0.32, 0])
        sym = projection_symbol(False, 0.88).move_to([-5.25, 0.25, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 16).move_to([-5.25, 2.08, 0])
        self.fadd(left_panel, q)
        self.play(FadeIn(left_panel), FadeIn(q), run_time=base.RT)
        self.fadd(sym)
        self.play(Create(sym), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        main_panel = paper_panel(9.55, 5.35, 0.42).move_to([2.38, -0.32, 0])
        front = self.compact_tile("front", "ALZADO", BLUE, 3.15, 1.90, 0.38).move_to([1.50, -0.40, 0])
        top_slot = RoundedRectangle(
            width=3.15, height=1.90, corner_radius=0.12,
            stroke_color=TEAL, stroke_width=1.7,
            fill_color=PALE_TEAL, fill_opacity=0.16,
        ).move_to([1.50, 1.65, 0])
        right_slot = RoundedRectangle(
            width=3.15, height=1.90, corner_radius=0.12,
            stroke_color=ORANGE, stroke_width=1.7,
            fill_color=PALE_ORANGE, fill_opacity=0.16,
        ).move_to([5.15, -0.40, 0])
        top_q = safe_text("PLANTA ?", 22, TEAL, BOLD).move_to(top_slot)
        right_q = safe_text("LATERAL D. ?", 22, ORANGE, BOLD).move_to(right_slot)
        prompt = callout("PIENSA ANTES DE REVELAR", INK, 5.5, 20).move_to([2.38, -3.15, 0])
        self.fadd(main_panel, front, top_slot, right_slot, top_q, right_q, prompt)
        self.play(FadeIn(main_panel), FadeIn(front), run_time=base.RT_SMOOTH)
        self.play(FadeIn(top_slot), FadeIn(right_slot), FadeIn(top_q), FadeIn(right_q), FadeIn(prompt), run_time=base.RT)

        dots = VGroup(*[Dot(radius=0.065, color=MID) for _ in range(6)]).arrange(RIGHT, buff=0.13).move_to([2.38, -2.55, 0])
        self.fadd(dots)
        self.play(FadeIn(dots), run_time=base.RT_FAST)
        for d in dots:
            self.play(d.animate.set_color(BLUE).scale(1.24), run_time=0.24)
            self.play(d.animate.set_color(MID).scale(1 / 1.24), run_time=0.24)
        self.wait(base.PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.0, 20).move_to([-5.25, -2.18, 0])
        self.fadd(method)
        self.play(FadeOut(prompt), FadeOut(dots), FadeIn(method), run_time=base.RT)
        self.wait(base.PAUSE_READ)

        top_view = self.compact_tile("top", "PLANTA", TEAL, 3.15, 1.90, 0.37).move_to(top_slot)
        right_view = self.compact_tile("right", "LATERAL D.", ORANGE, 3.15, 1.90, 0.38).move_to(right_slot)
        self.fadd(top_view)
        self.play(ReplacementTransform(top_slot, top_view), FadeOut(top_q), run_time=base.RT_SMOOTH)
        self.frem(top_slot, top_q)
        self.wait(base.PAUSE_VIEW)
        self.fadd(right_view)
        self.play(ReplacementTransform(right_slot, right_view), FadeOut(right_q), run_time=base.RT_SMOOTH)
        self.frem(right_slot, right_q)
        self.wait(base.PAUSE_VIEW)

        answer = callout(
            "MISMO LADO · PLANTA ARRIBA · LATERAL DERECHO A LA DERECHA",
            GREEN, 7.7, 19,
        ).move_to([2.38, -3.15, 0])
        self.fadd(answer)
        self.play(FadeIn(answer), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(left_panel, sym, q, main_panel, front, method, top_view, right_view, answer, h)
