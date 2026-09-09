#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V8 Lower/Large — Sistema diédrico ISO E / ISO A.

Direct correction of the real V7 PQH render and user review.

V7 solved most overlap failures, but introduced a new trade-off: several 3D
views and 2D projection tiles were made too small to obtain clearance. V8 does
not solve vertical-position problems by shrinking content. Instead it:

- lowers the 3D bracket by explicit world-space centering, especially along Z
  for front/rear/side observer views;
- restores a larger 3D scale while keeping the title/subtitle bands protected;
- lowers the complete orthogonal-projection construction as one geometric unit;
- restores larger ISO E / ISO A projection cards inside explicit non-overlap
  cells;
- enlarges comparison, algorithm and challenge projections without allowing
  card intersections;
- adds runtime bounding-box separation assertions to prevent layout regressions.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, -pqh.
"""
from __future__ import annotations

import sys
from pathlib import Path
from manim import *

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V7_DIR = HERE.parent / "technical_drawing_diedric_iso_v7_20260909"
for p in (str(V7_DIR), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

import diedric_iso_ntc1777_v7 as v7
import diedric_iso_ntc1777_v5 as base
from Core.technical_drawing_tools import *

# Preserve the successful V7 pacing.
base.RT_CAMERA = 3.00
base.PAUSE_OBSERVER = 5.00
base.PAUSE_VIEW = 3.65
base.PAUSE_READ = 2.95
base.PAUSE_LONG = 5.10
base.PAUSE_EXPLAIN = 3.70
base.PAUSE_CHALLENGE = 9.0


class DiedricISOProjectionV8LowerLarge(v7.DiedricISOProjectionV7SafeLayout):
    """V8: lower 3D geometry + restored projection scale with hard layout gates."""

    def assert_disjoint(self, *mobs: Mobject, gap: float = 0.04) -> None:
        """Fail the render if any selected 2D layout cells intersect."""
        for i, a in enumerate(mobs):
            al, ar = a.get_left()[0], a.get_right()[0]
            ab, at = a.get_bottom()[1], a.get_top()[1]
            for b in mobs[i + 1:]:
                bl, br = b.get_left()[0], b.get_right()[0]
                bb, bt = b.get_bottom()[1], b.get_top()[1]
                separated = (
                    ar + gap <= bl or br + gap <= al or
                    at + gap <= bb or bt + gap <= ab
                )
                if not separated:
                    raise ValueError(
                        f"V8 safe-layout failure: {a.__class__.__name__} intersects "
                        f"{b.__class__.__name__}"
                    )

    # ------------------------------------------------------------------
    # Opening: V7 was still visually high and smaller than the desired hero.
    # Lower the *centre* of the 3D object instead of reducing scale.
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.88)

        part = mechanical_bracket_3d().scale(0.90)
        part.move_to([0.0, -0.48, -0.72])
        self.play(
            LaggedStart(*[FadeIn(x, scale=0.985) for x in part[:6]], lag_ratio=0.08),
            run_time=base.RT_DRAW,
        )
        self.play(FadeIn(VGroup(*part[6:])), run_time=base.RT)
        self.begin_ambient_camera_rotation(rate=0.044)

        title_back = Rectangle(
            width=16.0, height=2.28, stroke_width=0,
            fill_color=BG, fill_opacity=0.97,
        ).move_to([0, 3.34, 0])
        title = VGroup(
            safe_text("SISTEMA DIÉDRICO", 50, NAVY, BOLD),
            safe_text("De una pieza 3D a vistas 2D", 27, DARK, NORMAL),
            VGroup(
                badge("PRIMER DIEDRO · ISO E", ORANGE, 17),
                badge("TERCER DIEDRO · ISO A", TEAL, 17),
            ).arrange(RIGHT, buff=0.28),
        ).arrange(DOWN, buff=0.16).move_to([0, 2.82, 0])
        self.fadd(title_back, title)
        self.play(FadeIn(title_back), FadeIn(title, shift=DOWN * 0.06), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_READ)

        idea = callout(
            "LA PIEZA NO CAMBIA · CAMBIA EL PUNTO DE VISTA",
            BLUE, 8.4, 22,
        ).move_to([0, -3.42, 0])
        self.fadd(idea)
        self.play(FadeIn(idea), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(idea, title, title_back)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(part), run_time=base.RT_SMOOTH)

    # ------------------------------------------------------------------
    # Projection: lower the whole construction together so rays/trace remain
    # geometrically coherent. Do not shrink the V6/V7 geometry.
    # ------------------------------------------------------------------
    def projection(self):
        self.transition(1, "PROYECCIÓN ORTOGONAL", "Observador → pieza → rayos paralelos → plano → vista")
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.98)
        h = self.header(1, "PROYECCIÓN ORTOGONAL", "Una dirección exacta produce una vista 2D sin perspectiva.")

        scene_shift = IN * 0.72 + DOWN * 0.12
        part = mechanical_bracket_3d().scale(0.90).shift(RIGHT * 0.55 + scene_shift)
        plane = vertical_projection_plane(-3.45, 8.3, 5.65, 2.45, 0.5).shift(scene_shift)
        self.play(FadeIn(part), FadeIn(plane[0]), run_time=base.RT_SMOOTH)
        self.play(LaggedStart(*[Create(g) for g in plane[1]], lag_ratio=0.012), run_time=base.RT)

        observer = VGroup(observer_icon(BLUE, 0.82), badge("OBSERVADOR", BLUE, 16)).arrange(DOWN, buff=0.10)
        observer.move_to([-6.15, 1.12, 0])
        self.fadd(observer)
        self.play(FadeIn(observer), run_time=base.RT)

        src = [
            [-3.20, -0.20, 0.42], [-2.75, -0.20, 1.49], [-1.50, -0.20, 1.49],
            [-0.95, -0.20, 1.55], [0.78, -0.20, 1.55], [1.65, -0.20, 3.56],
            [2.84, -0.20, 3.56], [3.20, -0.20, 0.42], [2.25, -0.20, 2.25],
        ]
        shift_vec = scene_shift.get_center() if hasattr(scene_shift, "get_center") else scene_shift
        # scene_shift is a numpy vector in Manim; explicit vector arithmetic keeps
        # all rays registered to the shifted plane and trace.
        rays = VGroup(*[
            projection_ray(
                np.array(p, dtype=float) + scene_shift,
                np.array([p[0], -3.45, p[2]], dtype=float) + scene_shift,
                ORANGE,
            ) for p in src
        ])
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.07), run_time=base.RT_DRAW)

        tag = self.top_tag("RAYOS PARALELOS · SIN PERSPECTIVA", ORANGE, 5.55)
        self.wait(base.PAUSE_EXPLAIN)
        trace = front_trace_3d(-3.455, BLUE).shift(scene_shift)
        self.play(Create(trace), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.cleanup(tag)

        tag = self.top_tag("ALINEAR LA CÁMARA = ELIMINAR LA PERSPECTIVA", TEAL, 6.2)
        self.move_camera(
            phi=90 * DEGREES, theta=-90 * DEGREES, zoom=1.08,
            run_time=base.RT_CAMERA, rate_func=smooth,
        )
        self.wait(base.PAUSE_OBSERVER)
        self.cleanup(tag)

        self.play(FadeOut(rays), FadeOut(part), FadeOut(plane), FadeOut(trace), run_time=base.RT_SMOOTH)
        self.cleanup(observer)
        self.view_fullscreen("front", BLUE, "ALZADO · PROYECCIÓN RESULTANTE")
        self.cleanup(h)

    # ------------------------------------------------------------------
    # Six 3D observer directions: V7 used scale=0.74. V8 restores scale=0.90
    # and explicitly moves the object centre down for every camera direction.
    # ------------------------------------------------------------------
    def observer_views(self):
        self.transition(
            2, "SEIS DIRECCIONES PRINCIPALES",
            "Observa en 3D → fija la dirección → confirma la vista 2D",
        )
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=0.94)
        h = self.header(
            2, "SEIS VISTAS PRINCIPALES",
            "Cada dirección se mantiene estable antes de mostrar su proyección ortográfica.",
        )

        part = mechanical_bracket_3d().scale(0.90)
        part.move_to([0.0, -0.35, -0.68])
        self.play(FadeIn(part), run_time=base.RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.028)
        self.wait(base.PAUSE_READ)
        self.stop_ambient_camera_rotation()

        stops = [
            (90, -90, 0.98, np.array([0.0, 0.00, -0.78]), "ALZADO", "front", BLUE, "MIRADA FRONTAL"),
            (0, -90, 0.92, np.array([0.0, -0.62, 0.00]), "PLANTA", "top", TEAL, "MIRADA SUPERIOR"),
            (90, 0, 1.00, np.array([0.0, 0.00, -0.78]), "LATERAL DERECHO", "right", ORANGE, "MIRADA DESDE LA DERECHA"),
            (90, 90, 0.98, np.array([0.0, 0.00, -0.78]), "POSTERIOR", "rear", RED, "MIRADA POSTERIOR"),
            (90, 180, 1.00, np.array([0.0, 0.00, -0.78]), "LATERAL IZQUIERDO", "left", PURPLE, "MIRADA DESDE LA IZQUIERDA"),
            (180, -90, 0.92, np.array([0.0, 0.62, 0.00]), "INFERIOR", "bottom", GREEN, "MIRADA INFERIOR"),
        ]

        for phi, theta, zoom, target, label, key, color, caption in stops:
            tag = callout(label, color, 4.90, 20).move_to([-5.05, 2.43, 0])
            self.fadd(tag)
            self.play(FadeIn(tag, shift=RIGHT * 0.05), run_time=base.RT_FAST)
            self.play(part.animate.move_to(target), run_time=base.RT_FAST)
            self.move_camera(
                phi=phi * DEGREES, theta=theta * DEGREES, zoom=zoom,
                run_time=base.RT_CAMERA, rate_func=smooth,
            )
            self.wait(base.PAUSE_OBSERVER)

            focus = RoundedRectangle(
                width=6.40, height=4.45, corner_radius=0.15,
                stroke_color=color, stroke_width=1.8, fill_opacity=0,
            ).move_to([0, -0.68, 0])
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

        overview_title = callout("LAS SEIS VISTAS · MISMA PIEZA", BLUE, 5.6, 21).move_to([0, 2.62, 0])
        cards = VGroup(*[
            view_card(k, 4.65, 2.45, 0.54 if k in ("front", "rear") else 0.52)
            for k in ["front", "top", "right", "left", "rear", "bottom"]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.22)).shift(DOWN * 0.58)
        self.fadd(overview_title, cards)
        self.play(
            FadeIn(overview_title),
            LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards], lag_ratio=0.09),
            run_time=base.RT_DRAW,
        )
        self.wait(base.PAUSE_LONG)
        self.cleanup(overview_title, cards, h)

    # ------------------------------------------------------------------
    # ISO E / ISO A: restore larger cards; clearance comes from cell positions,
    # not scale reduction.
    # ------------------------------------------------------------------
    def _angle_method(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        name = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        rule = "VISTAS AL LADO OPUESTO" if first else "VISTAS EN EL MISMO LADO"
        self.transition(number, name, order)
        h = self.header(number, name, "Primero interpreta el orden físico; después ubica las vistas en la lámina.")

        observer = observer_icon(color, 0.90).move_to([-5.98, -0.48, 0])
        object_box = RoundedRectangle(
            width=3.60, height=3.90, corner_radius=0.15,
            stroke_color=LIGHT, stroke_width=1.4,
            fill_color=PAPER, fill_opacity=1,
        )
        object_view = orthographic_view("front", 0.48).move_to(object_box)
        object_group = VGroup(object_box, object_view).move_to([0.0 if first else 4.65, -0.48, 0])
        plane = RoundedRectangle(
            width=0.23, height=4.28, corner_radius=0.05,
            stroke_color=BLUE, stroke_width=2.1,
            fill_color=PALE_BLUE, fill_opacity=0.68,
        )
        plane.move_to([5.28, -0.48, 0] if first else [-0.75, -0.48, 0])
        if first:
            arr1 = Arrow([-5.00, -0.48, 0], [-2.02, -0.48, 0], buff=0.10, color=color, stroke_width=3.2)
            arr2 = Arrow([2.02, -0.48, 0], [4.88, -0.48, 0], buff=0.10, color=color, stroke_width=3.2)
        else:
            arr1 = Arrow([-5.00, -0.48, 0], [-1.15, -0.48, 0], buff=0.10, color=color, stroke_width=3.2)
            arr2 = Arrow([-0.35, -0.48, 0], [2.72, -0.48, 0], buff=0.10, color=color, stroke_width=3.2)
        physical = VGroup(observer, object_group, plane, arr1, arr2)
        self.fadd(physical)
        self.play(FadeIn(observer), run_time=base.RT)
        if first:
            self.play(GrowArrow(arr1), FadeIn(object_group), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(plane), run_time=base.RT_SMOOTH)
        else:
            self.play(GrowArrow(arr1), FadeIn(plane), run_time=base.RT_SMOOTH)
            self.play(GrowArrow(arr2), FadeIn(object_group), run_time=base.RT_SMOOTH)
        order_tag = callout(order, color, 6.3, 21).move_to([0, -3.28, 0])
        self.fadd(order_tag)
        self.play(FadeIn(order_tag), run_time=base.RT_FAST)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(physical, order_tag)

        sheet = paper_panel(14.15, 5.90, 0.42).move_to([0, -0.32, 0])
        front = view_card("front", 4.35, 2.10, 0.50)
        top = view_card("top", 4.35, 2.10, 0.48)
        right = view_card("right", 4.35, 2.10, 0.50)
        if first:
            front.move_to([0.00, 0.52, 0])
            top.move_to([0.00, -1.78, 0])
            right.move_to([-4.70, 0.52, 0])
            rule_tag = callout(rule, color, 4.9, 19).move_to([4.70, -1.78, 0])
        else:
            front.move_to([0.00, -0.58, 0])
            top.move_to([0.00, 1.72, 0])
            right.move_to([4.70, -0.58, 0])
            rule_tag = callout(rule, color, 4.9, 19).move_to([-4.70, 1.72, 0])
        self.assert_disjoint(front, top, right, gap=0.06)

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
    # Comparison: larger tiles than V7, still fully separated.
    # ------------------------------------------------------------------
    def compare(self):
        self.transition(6, "ISO E vs ISO A", "Mismas vistas; cambia su posición respecto al alzado")
        h = self.header(6, "COMPARACIÓN DIRECTA", "El alzado es el ancla. Compara únicamente la posición de planta y lateral derecho.")

        left_sheet = paper_panel(7.30, 5.75, 0.44).move_to([-3.75, -0.30, 0])
        right_sheet = paper_panel(7.30, 5.75, 0.44).move_to([3.75, -0.30, 0])
        left_title = badge("PRIMER DIEDRO · ISO E", ORANGE, 17).move_to([-3.75, 2.36, 0])
        right_title = badge("TERCER DIEDRO · ISO A", TEAL, 17).move_to([3.75, 2.36, 0])

        lf = self.compact_tile("front", "ALZADO", BLUE, 2.52, 1.66, 0.32).move_to([-3.38, 0.46, 0])
        lt = self.compact_tile("top", "PLANTA", TEAL, 2.52, 1.66, 0.31).move_to([-3.38, -1.40, 0])
        lr = self.compact_tile("right", "LATERAL D.", ORANGE, 2.52, 1.66, 0.32).move_to([-6.00, 0.46, 0])
        rf = self.compact_tile("front", "ALZADO", BLUE, 2.52, 1.66, 0.32).move_to([3.38, -0.46, 0])
        rt = self.compact_tile("top", "PLANTA", TEAL, 2.52, 1.66, 0.31).move_to([3.38, 1.40, 0])
        rr = self.compact_tile("right", "LATERAL D.", ORANGE, 2.52, 1.66, 0.32).move_to([6.00, -0.46, 0])
        self.assert_disjoint(lf, lt, lr, gap=0.05)
        self.assert_disjoint(rf, rt, rr, gap=0.05)

        left_guides = VGroup(self.projector_pair(lf, lt), self.projector_pair(lf, lr))
        right_guides = VGroup(self.projector_pair(rf, rt), self.projector_pair(rf, rr))
        labels = VGroup(
            callout("OPUESTO", ORANGE, 2.65, 18).move_to([-3.75, -2.72, 0]),
            callout("MISMO LADO", TEAL, 2.95, 18).move_to([3.75, -2.72, 0]),
        )
        group = VGroup(left_sheet, right_sheet, left_title, right_title, left_guides, right_guides, lf, lt, lr, rf, rt, rr, labels)
        self.fadd(group)
        self.play(FadeIn(left_sheet), FadeIn(right_sheet), FadeIn(left_title), FadeIn(right_title), run_time=base.RT_SMOOTH)
        self.play(FadeIn(lf), FadeIn(lt), FadeIn(lr), Create(left_guides), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(rf), FadeIn(rt), FadeIn(rr), Create(right_guides), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)
        self.play(FadeIn(labels), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(group, h)

    # ------------------------------------------------------------------
    # Algorithm: restore readable projection scale using a wider right sheet.
    # ------------------------------------------------------------------
    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(9, "LEE UNA LÁMINA EN 6 PASOS", "Sistema → alzado → distribución → reconstrucción.")

        steps = [
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 4.85),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 4.85),
            step_chip(3, "UBICA EL ALZADO", BLUE, 4.85),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 4.85),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 4.85),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 4.85),
        ]
        VGroup(*steps).arrange(DOWN, buff=0.13).move_to([-4.85, -0.35, 0])

        sheet = paper_panel(8.35, 5.82, 0.42).move_to([3.48, -0.34, 0])
        self.fadd(sheet)
        self.play(FadeIn(sheet), run_time=base.RT)

        sym = projection_symbol(False, 0.61).move_to([0.70, 1.52, 0])
        method = badge("ISO A · TERCER DIEDRO", TEAL, 16).move_to([1.28, 0.35, 0])
        front = self.compact_tile("front", "ALZADO", BLUE, 2.55, 1.64, 0.32).move_to([3.72, -0.28, 0])
        top = self.compact_tile("top", "PLANTA", TEAL, 2.55, 1.64, 0.31).move_to([3.72, 1.58, 0])
        right = self.compact_tile("right", "LATERAL D.", ORANGE, 2.55, 1.64, 0.32).move_to([6.34, -0.28, 0])
        self.assert_disjoint(front, top, right, gap=0.04)
        reconstruction = callout("VISTAS COHERENTES → FORMA 3D", PURPLE, 5.25, 18).move_to([4.05, -2.48, 0])

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
                guides = VGroup(self.projector_pair(front, top), self.projector_pair(front, right))
                self.fadd(guides); self.play(Create(guides), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeOut(guides), run_time=base.RT_FAST); self.frem(guides)
            elif i == 5:
                self.fadd(reconstruction)
                self.play(FadeIn(reconstruction, shift=UP * 0.05), run_time=base.RT_SMOOTH)
            self.wait(1.55)
        self.wait(base.PAUSE_LONG)
        self.cleanup(*steps, sheet, sym, method, front, top, right, reconstruction, h)

    # ------------------------------------------------------------------
    # Challenge: return close to V6 scale, but with V8 cell separation.
    # ------------------------------------------------------------------
    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        h = self.header(10, "DESAFÍO DE LECTURA", "Con el símbolo dado, ubica la planta y el lateral derecho.")

        left_panel = paper_panel(4.65, 5.40, 0.42).move_to([-5.20, -0.34, 0])
        sym = projection_symbol(False, 0.96).move_to([-5.20, 0.22, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 17).move_to([-5.20, 2.10, 0])
        self.fadd(left_panel, q)
        self.play(FadeIn(left_panel), FadeIn(q), run_time=base.RT)
        self.fadd(sym); self.play(Create(sym), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        main_panel = paper_panel(9.75, 5.40, 0.42).move_to([2.45, -0.34, 0])
        front = self.compact_tile("front", "ALZADO", BLUE, 3.35, 2.02, 0.40).move_to([1.40, -0.48, 0])
        top_slot = RoundedRectangle(
            width=3.35, height=2.02, corner_radius=0.12,
            stroke_color=TEAL, stroke_width=1.7,
            fill_color=PALE_TEAL, fill_opacity=0.16,
        ).move_to([1.40, 1.72, 0])
        right_slot = RoundedRectangle(
            width=3.35, height=2.02, corner_radius=0.12,
            stroke_color=ORANGE, stroke_width=1.7,
            fill_color=PALE_ORANGE, fill_opacity=0.16,
        ).move_to([5.12, -0.48, 0])
        self.assert_disjoint(front, top_slot, right_slot, gap=0.05)
        top_q = safe_text("PLANTA ?", 23, TEAL, BOLD).move_to(top_slot)
        right_q = safe_text("LATERAL D. ?", 23, ORANGE, BOLD).move_to(right_slot)
        prompt = callout("PIENSA ANTES DE REVELAR", INK, 5.6, 20).move_to([2.45, -3.12, 0])
        self.fadd(main_panel, front, top_slot, right_slot, top_q, right_q, prompt)
        self.play(FadeIn(main_panel), FadeIn(front), run_time=base.RT_SMOOTH)
        self.play(FadeIn(top_slot), FadeIn(right_slot), FadeIn(top_q), FadeIn(right_q), FadeIn(prompt), run_time=base.RT)

        dots = VGroup(*[Dot(radius=0.065, color=MID) for _ in range(6)]).arrange(RIGHT, buff=0.13).move_to([2.45, -2.54, 0])
        self.fadd(dots); self.play(FadeIn(dots), run_time=base.RT_FAST)
        for d in dots:
            self.play(d.animate.set_color(BLUE).scale(1.24), run_time=0.24)
            self.play(d.animate.set_color(MID).scale(1 / 1.24), run_time=0.24)
        self.wait(base.PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.1, 20).move_to([-5.20, -2.18, 0])
        self.fadd(method)
        self.play(FadeOut(prompt), FadeOut(dots), FadeIn(method), run_time=base.RT)
        self.wait(base.PAUSE_READ)

        top_view = self.compact_tile("top", "PLANTA", TEAL, 3.35, 2.02, 0.39).move_to(top_slot)
        right_view = self.compact_tile("right", "LATERAL D.", ORANGE, 3.35, 2.02, 0.40).move_to(right_slot)
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
            GREEN, 7.8, 19,
        ).move_to([2.45, -3.12, 0])
        self.fadd(answer); self.play(FadeIn(answer), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(left_panel, sym, q, main_panel, front, method, top_view, right_view, answer, h)

    # ------------------------------------------------------------------
    # Closing: larger 3D hero, moved down instead of shrunk.
    # ------------------------------------------------------------------
    def closing(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.96)
        part = mechanical_bracket_3d().scale(0.90)
        part.move_to([4.70, -0.55, -0.68])
        self.play(FadeIn(part), run_time=base.RT_SMOOTH)
        self.begin_ambient_camera_rotation(rate=0.040)

        block = VGroup(
            safe_text("MÉTODO FINAL", 29, BLUE, BOLD),
            safe_text("SÍMBOLO → ALZADO → POSICIÓN → 3D", 37, NAVY, BOLD, 8.6),
            step_chip(1, "IDENTIFICA EL MÉTODO", BLUE, 4.75),
            step_chip(2, "ANCLA EN EL ALZADO", ORANGE, 4.75),
            step_chip(3, "LEE PLANTA Y LATERALES", TEAL, 4.75),
            step_chip(4, "VERIFICA Y RECONSTRUYE", GREEN, 4.75),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-3.10, -0.05, 0])
        self.fadd(block)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.06) for x in block], lag_ratio=0.12), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_LONG)

        final = callout("3D → 2D SIN AMBIGÜEDAD", GREEN, 5.8, 23).move_to([-3.10, -3.42, 0])
        self.fadd(final); self.play(FadeIn(final), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.stop_ambient_camera_rotation()
        self.cleanup(final, block)
        self.play(FadeOut(part), run_time=base.RT_SMOOTH)
