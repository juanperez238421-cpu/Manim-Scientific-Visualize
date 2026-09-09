#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V14 REBUILT CHOREOGRAPHY.

This is a real presentation rebuild, not a timing wrapper.

Sources reviewed before the rebuild:
- V12/V13 3D→2D orthographic scene: strong geometry, but V13 only changed pace.
- Sistema Diédrico / Monge V5: excellent point-first explanation and literal PH fold.
- ISO A / ISO E V3 presentation: stronger sequential extraction, temporary projection
  logic, clean no-crossing rays, and explicit final sheet placement.

V14 therefore changes the visual grammar itself:
1. Point A first: one point -> two orthogonal projections.
2. Same rule applied to the solid.
3. FRONT, TOP and RIGHT are taught one at a time, with a visible observation cue.
4. Projectors arrive in waves; landing points appear before the contour is traced.
5. Finished views remain on their real receiving planes.
6. Source object is removed; projections remain.
7. PH and PL are unfolded as literal rigid-body motions around their hinges.
8. Final aligned sheet is held and then connected to ISO A / ISO E placement logic.
9. Large, sparse instructional text replaces dense small captions.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V12_FIXED_FULL_TOTAL import (
    Projection3Dto2DV12FixedFullTotal,
)
from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA import (
    INK, MUTED, GRID, PV_COLOR, PH_COLOR,
    FRONT_COLOR, TOP_COLOR, RIGHT_COLOR,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = max(0.03, float(os.getenv("LESSON_TIME_SCALE", "1.0")))


def T(seconds: float) -> float:
    return max(0.05, seconds * TIME_SCALE)


class Projection3Dto2DV14RebuiltChoreography(Projection3Dto2DV12FixedFullTotal):
    """Rebuilt classroom choreography using the validated V12 geometry model."""

    # ------------------------------------------------------------------
    # Fixed-screen instructional UI
    # ------------------------------------------------------------------
    def banner(self, kicker: str, title: str, accent=INK, width=12.8):
        box = RoundedRectangle(
            width=width, height=1.00, corner_radius=0.12,
            stroke_color=GRID, stroke_width=1.25,
            fill_color=WHITE, fill_opacity=0.98,
        )
        k = Text(kicker, font_size=20, color=accent, weight=BOLD)
        t = Text(title, font_size=31, color=INK, weight=BOLD)
        group = VGroup(k, t).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        group.move_to(box.get_center()).shift(LEFT * 0.10)
        result = VGroup(box, group).to_edge(UP, buff=0.28)
        return result

    def mini_note(self, text: str, accent=INK, width=6.6):
        box = RoundedRectangle(
            width=width, height=0.56, corner_radius=0.09,
            stroke_color=GRID, stroke_width=1.15,
            fill_color=WHITE, fill_opacity=0.97,
        )
        lab = Text(text, font_size=22, color=accent, weight=BOLD)
        lab.scale_to_fit_width(width - 0.30)
        lab.move_to(box)
        return VGroup(box, lab).to_edge(DOWN, buff=0.30)

    def fixed_show(self, *mobs, run_time=0.55):
        self.add_fixed_in_frame_mobjects(*mobs)
        for m in mobs:
            m.set_opacity(0)
        self.play(*[m.animate.set_opacity(1) for m in mobs], run_time=T(run_time), rate_func=smooth)

    def fixed_hide(self, *mobs, run_time=0.35):
        self.play(*[m.animate.set_opacity(0) for m in mobs], run_time=T(run_time), rate_func=smooth)
        for m in mobs:
            self.remove_fixed_in_frame_mobjects(m)

    def swap_banner(self, old, kicker, title, accent=INK):
        new = self.banner(kicker, title, accent)
        self.add_fixed_in_frame_mobjects(new)
        new.set_opacity(0)
        self.play(old.animate.set_opacity(0), new.animate.set_opacity(1), run_time=T(0.55), rate_func=smooth)
        self.remove_fixed_in_frame_mobjects(old)
        return new

    def landing_dots(self, points, color, radius=0.045):
        return VGroup(*[Dot3D(np.array(p, dtype=float), radius=radius, color=color) for p in points])

    def trace_polygon_segments(self, poly, color, stroke_width=4.4):
        verts = list(poly.get_vertices())
        return VGroup(*[
            Line(verts[i], verts[(i + 1) % len(verts)], color=color, stroke_width=stroke_width)
            for i in range(len(verts))
        ])

    def observation_arrow(self, start, end, label, color):
        arrow = Arrow3D(
            start=np.array(start, dtype=float), end=np.array(end, dtype=float),
            color=color, thickness=0.032, height=0.30, base_radius=0.095,
        )
        lab = Text(label, font_size=24, color=color, weight=BOLD)
        lab.move_to(np.array(start, dtype=float) + np.array([0.0, 0.0, 0.30]))
        self.add_fixed_orientation_mobjects(lab)
        lab.set_opacity(0)
        return arrow, lab

    # ------------------------------------------------------------------
    # Main rebuilt presentation
    # ------------------------------------------------------------------
    def construct(self):
        focus = self.lifted_center(0.0, 1.70, 1.42)
        self.set_camera_orientation(
            phi=64 * DEGREES,
            theta=-52 * DEGREES,
            gamma=0,
            zoom=1.08,
            frame_center=focus,
        )

        # ================================================================
        # 0 · TITLE — large and quiet
        # ================================================================
        title = Text("DE 3D A 2D", font_size=64, color=INK, weight=BOLD)
        subtitle = Text("Sistema diédrico · proyección ortogonal · abatimiento", font_size=28, color=MUTED)
        rule = Line(LEFT * 3.8, RIGHT * 3.8, color=GRID, stroke_width=2.0)
        intro = VGroup(title, rule, subtitle).arrange(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(intro)
        intro.set_opacity(0)
        self.play(intro.animate.set_opacity(1), run_time=T(0.95), rate_func=smooth)
        self.wait(T(2.10))
        self.play(intro.animate.set_opacity(0), run_time=T(0.65), rate_func=smooth)
        self.remove_fixed_in_frame_mobjects(intro)

        # ================================================================
        # 1 · BUILD THE DIHEDRAL REFERENCE FIRST
        # ================================================================
        b = self.banner("IDEA 1", "Antes del sólido: entendamos qué significa proyectar un punto", FRONT_COLOR)
        self.fixed_show(b, run_time=0.65)

        PLANE_W = 5.85
        PV_H = 3.25
        PH_D = 3.50
        SIDE_X = 2.62

        pv = Rectangle(
            width=PLANE_W, height=PV_H,
            stroke_color=PV_COLOR, stroke_width=2.0,
            fill_color=PV_COLOR, fill_opacity=0.10,
        ).rotate(PI / 2, axis=RIGHT).shift(OUT * (PV_H / 2))
        ph = Rectangle(
            width=PLANE_W, height=PH_D,
            stroke_color=PH_COLOR, stroke_width=2.0,
            fill_color=PH_COLOR, fill_opacity=0.10,
        ).shift(UP * (PH_D / 2))
        lt = Line(
            np.array([-PLANE_W/2, 0, 0]), np.array([PLANE_W/2, 0, 0]),
            color=INK, stroke_width=3.2,
        )

        self.play(Create(pv), run_time=T(1.00), rate_func=smooth)
        self.wait(T(0.45))
        self.play(Create(ph), Create(lt), run_time=T(1.05), rate_func=smooth)
        self.wait(T(1.10))

        pv_lab = Text("PV · PLANO VERTICAL", font_size=22, color=PV_COLOR, weight=BOLD)
        ph_lab = Text("PH · PLANO HORIZONTAL", font_size=22, color=TOP_COLOR, weight=BOLD)
        lt_lab = Text("LT", font_size=22, color=INK, weight=BOLD)
        pv_lab.move_to(np.array([-2.0, 0.05, 3.10]))
        ph_lab.move_to(np.array([-2.0, 3.10, 0.08]))
        lt_lab.move_to(np.array([2.72, 0.02, 0.20]))
        self.add_fixed_orientation_mobjects(pv_lab, ph_lab, lt_lab)
        for m in (pv_lab, ph_lab, lt_lab): m.set_opacity(0)
        self.play(
            pv_lab.animate.set_opacity(1), ph_lab.animate.set_opacity(1), lt_lab.animate.set_opacity(1),
            run_time=T(0.75),
        )

        # Point A demo — the clearest idea from the Monge scene.
        A = np.array([0.55, 1.70, 2.25])
        Av = np.array([0.55, 0.025, 2.25])
        Ah = np.array([0.55, 1.70, 0.025])
        dA = Dot3D(A, radius=0.075, color=INK)
        dAv = Dot3D(Av, radius=0.060, color=FRONT_COLOR)
        dAh = Dot3D(Ah, radius=0.060, color=TOP_COLOR)
        ray_v = self.projector(A, Av, FRONT_COLOR)
        ray_h = self.projector(A, Ah, TOP_COLOR)
        la = Text("A", font_size=26, color=INK, weight=BOLD).move_to(A + np.array([0.18,0.10,0.20]))
        lav = Text("a′", font_size=24, color=FRONT_COLOR, weight=BOLD).move_to(Av + np.array([0.28,0.02,0.10]))
        lah = Text("a", font_size=24, color=TOP_COLOR, weight=BOLD).move_to(Ah + np.array([0.26,0.12,0.06]))
        self.add_fixed_orientation_mobjects(la, lav, lah)
        for m in (la, lav, lah): m.set_opacity(0)

        self.play(FadeIn(dA, scale=0.7), la.animate.set_opacity(1), run_time=T(0.65))
        self.wait(T(0.70))
        note = self.mini_note("La proyección siempre viaja perpendicular al plano receptor", FRONT_COLOR, 7.3)
        self.fixed_show(note, run_time=0.45)
        self.play(Create(ray_v), run_time=T(1.15), rate_func=linear)
        self.play(FadeIn(dAv, scale=0.7), lav.animate.set_opacity(1), run_time=T(0.50))
        self.wait(T(0.75))
        self.play(Create(ray_h), run_time=T(1.15), rate_func=linear)
        self.play(FadeIn(dAh, scale=0.7), lah.animate.set_opacity(1), run_time=T(0.50))
        self.wait(T(1.70))
        self.fixed_hide(note, run_time=0.30)

        # ================================================================
        # 2 · SAME RULE -> THE SOLID
        # ================================================================
        b = self.swap_banner(b, "IDEA 2", "El sólido es el mismo problema, repetido sobre sus vértices y aristas", INK)
        self.play(
            FadeOut(dA), FadeOut(dAv), FadeOut(dAh), FadeOut(ray_v), FadeOut(ray_h),
            la.animate.set_opacity(0), lav.animate.set_opacity(0), lah.animate.set_opacity(0),
            run_time=T(0.75),
        )
        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.10), run_time=T(1.20), rate_func=smooth)
        self.wait(T(1.25))

        # ================================================================
        # 3 · FRONT / ALZADO — observation -> rays -> landing -> contour
        # ================================================================
        b = self.swap_banner(b, "VISTA 1 · ALZADO", "Primero miro de frente; después proyecto; al final trazo", FRONT_COLOR)
        front_arrow, front_arrow_lab = self.observation_arrow(
            [0.15, 4.20, 1.65], [0.15, 3.22, 1.65], "MIRADA FRONTAL", FRONT_COLOR
        )
        self.play(FadeIn(front_arrow), front_arrow_lab.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.05))
        self.play(FadeOut(front_arrow), front_arrow_lab.animate.set_opacity(0), run_time=T(0.55))

        front_sources = [
            [-2.30,0.75,0.35], [2.30,0.75,0.35], [2.30,0.75,1.05],
            [0.85,1.00,1.05], [0.85,1.00,1.85], [-0.15,1.28,1.85],
            [-0.15,1.28,2.75], [-1.25,1.28,2.75], [-1.70,1.00,1.85],
            [-2.30,0.75,1.05],
        ]
        front_land = [[p[0], 0.025, p[2]] for p in front_sources]
        front_rays = VGroup(*[self.projector(p, q, FRONT_COLOR) for p, q in zip(front_sources, front_land)])
        fsrc = self.landing_dots(front_sources, FRONT_COLOR, 0.040)
        fland = self.landing_dots(front_land, FRONT_COLOR, 0.045)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in fsrc], lag_ratio=0.06), run_time=T(0.80))
        self.play(LaggedStart(*[Create(r) for r in front_rays], lag_ratio=0.10), run_time=T(2.30), rate_func=linear)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in fland], lag_ratio=0.06), run_time=T(0.85))
        self.wait(T(1.05))
        front_poly = self.front_outline()
        front_segments = self.trace_polygon_segments(front_poly, FRONT_COLOR, 4.8)
        self.play(LaggedStart(*[Create(s) for s in front_segments], lag_ratio=0.12), run_time=T(2.40), rate_func=smooth)
        self.wait(T(1.40))
        self.play(FadeOut(front_rays), FadeOut(fsrc), FadeOut(fland), run_time=T(0.70))

        # ================================================================
        # 4 · TOP / PLANTA
        # ================================================================
        b = self.swap_banner(b, "VISTA 2 · PLANTA", "Ahora miro desde arriba; la profundidad se vuelve visible", TOP_COLOR)
        top_arrow, top_arrow_lab = self.observation_arrow(
            [-0.30,1.85,3.90], [-0.30,1.85,2.92], "MIRADA SUPERIOR", TOP_COLOR
        )
        self.play(FadeIn(top_arrow), top_arrow_lab.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.05))
        self.play(FadeOut(top_arrow), top_arrow_lab.animate.set_opacity(0), run_time=T(0.55))

        top_sources = [
            [-2.30,0.75,1.05], [2.30,0.75,1.05], [2.30,3.05,1.05], [-2.30,3.05,1.05],
            [-1.70,1.00,1.85], [0.85,1.00,1.85], [0.85,2.72,1.85], [-1.70,2.72,1.85],
            [-1.25,1.28,2.75], [-0.15,1.28,2.75], [-0.15,2.34,2.75], [-1.25,2.34,2.75],
        ]
        top_land = [[p[0], p[1], 0.025] for p in top_sources]
        top_rays = VGroup(*[self.projector(p, q, TOP_COLOR) for p, q in zip(top_sources, top_land)])
        tsrc = self.landing_dots(top_sources, TOP_COLOR, 0.040)
        tland = self.landing_dots(top_land, TOP_COLOR, 0.045)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in tsrc], lag_ratio=0.05), run_time=T(0.80))
        self.play(LaggedStart(*[Create(r) for r in top_rays], lag_ratio=0.085), run_time=T(2.45), rate_func=linear)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in tland], lag_ratio=0.05), run_time=T(0.90))
        self.wait(T(1.05))
        top = self.top_outline()
        self.play(Create(top[0]), run_time=T(1.20), rate_func=smooth)
        self.wait(T(0.55))
        self.play(Create(top[1]), run_time=T(1.00), rate_func=smooth)
        self.wait(T(0.55))
        self.play(Create(top[2]), run_time=T(1.00), rate_func=smooth)
        self.wait(T(1.35))
        self.play(FadeOut(top_rays), FadeOut(tsrc), FadeOut(tland), run_time=T(0.70))

        # ================================================================
        # 5 · RIGHT / PERFIL — side plane only appears when it becomes useful
        # ================================================================
        b = self.swap_banner(b, "VISTA 3 · PERFIL", "El plano lateral aparece ahora: una tercera mirada, una tercera vista", RIGHT_COLOR)
        side = Rectangle(
            width=PH_D, height=PV_H,
            stroke_color=RIGHT_COLOR, stroke_width=2.0,
            fill_color=RIGHT_COLOR, fill_opacity=0.085,
        ).rotate(PI / 2, axis=UP).move_to(np.array([SIDE_X, PH_D/2, PV_H/2]))
        side_lab = Text("PL · PLANO LATERAL", font_size=22, color=RIGHT_COLOR, weight=BOLD)
        side_lab.move_to(np.array([2.66, 3.10, 2.92]))
        self.add_fixed_orientation_mobjects(side_lab)
        side_lab.set_opacity(0)
        self.play(Create(side), side_lab.animate.set_opacity(1), run_time=T(1.10))
        self.wait(T(0.75))

        right_arrow, right_arrow_lab = self.observation_arrow(
            [3.72,1.80,1.60], [2.80,1.80,1.60], "MIRADA LATERAL", RIGHT_COLOR
        )
        self.play(FadeIn(right_arrow), right_arrow_lab.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.05))
        self.play(FadeOut(right_arrow), right_arrow_lab.animate.set_opacity(0), run_time=T(0.55))

        right_sources = [
            [2.30,0.75,0.35], [2.30,3.05,0.35], [2.30,3.05,1.05], [2.30,0.75,1.05],
            [0.85,1.00,1.85], [0.85,2.72,1.85], [-0.15,1.28,2.75], [-0.15,2.34,2.75],
        ]
        right_land = [[SIDE_X, p[1], p[2]] for p in right_sources]
        right_rays = VGroup(*[self.projector(p, q, RIGHT_COLOR) for p, q in zip(right_sources, right_land)])
        rsrc = self.landing_dots(right_sources, RIGHT_COLOR, 0.040)
        rland = self.landing_dots(right_land, RIGHT_COLOR, 0.045)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rsrc], lag_ratio=0.06), run_time=T(0.75))
        self.play(LaggedStart(*[Create(r) for r in right_rays], lag_ratio=0.10), run_time=T(2.20), rate_func=linear)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in rland], lag_ratio=0.06), run_time=T(0.85))
        self.wait(T(1.00))
        right_poly = self.right_outline(SIDE_X)
        right_segments = self.trace_polygon_segments(right_poly, RIGHT_COLOR, 4.8)
        self.play(LaggedStart(*[Create(s) for s in right_segments], lag_ratio=0.12), run_time=T(2.30), rate_func=smooth)
        self.wait(T(1.30))
        self.play(FadeOut(right_rays), FadeOut(rsrc), FadeOut(rland), run_time=T(0.70))

        # ================================================================
        # 6 · THREE REAL PROJECTIONS — orbit to read the construction
        # ================================================================
        b = self.swap_banner(b, "RESULTADO 3D", "Tres planos reciben tres descripciones del mismo objeto", INK)
        self.move_camera(theta=-62*DEGREES, phi=60*DEGREES, zoom=0.98, frame_center=focus, run_time=T(2.20))
        self.wait(T(1.15))
        self.move_camera(theta=-45*DEGREES, phi=67*DEGREES, zoom=1.00, frame_center=focus, run_time=T(2.10))
        self.wait(T(1.70))

        # ================================================================
        # 7 · REMOVE THE SOURCE OBJECT
        # ================================================================
        b = self.swap_banner(b, "IDEA 3", "Retiro el objeto; las proyecciones no desaparecen", INK)
        self.play(FadeOut(solid), run_time=T(1.35), rate_func=smooth)
        self.wait(T(2.00))

        # Convert segmented front/right back to coherent groups for folding/readability.
        front = VGroup(*front_segments)
        right = VGroup(*right_segments)

        # ================================================================
        # 8 · LITERAL UNFOLDING — PH first, PL second
        # ================================================================
        b = self.swap_banner(b, "ABATIMIENTO", "Ahora convierto los tres planos del espacio en una sola hoja", INK)
        fold_note = self.mini_note("1 · PH gira 90° alrededor de LT", TOP_COLOR, 5.6)
        self.fixed_show(fold_note, run_time=0.45)
        fold_center = self.lifted_center(0.0, 1.60, 0.15)
        self.move_camera(zoom=0.94, frame_center=fold_center, run_time=T(1.15))
        self.play(
            Rotate(VGroup(ph, top), angle=-PI/2, axis=RIGHT, about_point=ORIGIN, rate_func=smooth),
            run_time=T(4.50),
        )
        self.wait(T(1.35))
        self.fixed_hide(fold_note, run_time=0.30)

        side_hinge = np.array([SIDE_X, 0.0, 0.0])
        side_note = self.mini_note("2 · PL gira 90° alrededor de su charnela vertical", RIGHT_COLOR, 6.8)
        self.fixed_show(side_note, run_time=0.45)
        self.play(
            Rotate(VGroup(side, right), angle=-PI/2, axis=OUT, about_point=side_hinge, rate_func=smooth),
            run_time=T(4.50),
        )
        self.wait(T(1.35))
        self.fixed_hide(side_note, run_time=0.30)

        # Frontal camera: everything is now a drawing sheet.
        self.move_camera(
            phi=90*DEGREES, theta=90*DEGREES, gamma=0,
            zoom=1.04, frame_center=self.lifted_center(0.0,0.0,0.10),
            run_time=T(2.40),
        )
        self.wait(T(1.80))

        # ================================================================
        # 9 · ALIGNMENT — explicitly show shared dimensions
        # ================================================================
        b = self.swap_banner(b, "HOJA 2D", "Las vistas quedan relacionadas por líneas de correspondencia", FRONT_COLOR)
        guides = VGroup(*[
            Line(np.array([x, 0.03, 3.00]), np.array([x, 0.03, -3.00]), color=GRID, stroke_width=1.5)
            for x in (-2.30, -1.70, -1.25, -0.15, 0.85, 2.30)
        ])
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.10), run_time=T(1.90))
        self.wait(T(2.10))
        self.play(FadeOut(guides), run_time=T(0.75))

        # Hold the real folded construction.
        hold = self.mini_note("Mismo ancho · misma altura · misma profundidad, conservadas entre vistas", INK, 8.4)
        self.fixed_show(hold, run_time=0.45)
        self.wait(T(2.30))
        self.fixed_hide(hold, run_time=0.30)

        # Fade the physical planes; keep only their projected drawings.
        self.play(
            FadeOut(pv), FadeOut(ph), FadeOut(side), FadeOut(lt),
            pv_lab.animate.set_opacity(0), ph_lab.animate.set_opacity(0), lt_lab.animate.set_opacity(0),
            side_lab.animate.set_opacity(0),
            run_time=T(1.10),
        )
        self.wait(T(1.00))

        # ================================================================
        # 10 · ISO A / ISO E CONNECTION — use the stronger A/E presentation idea
        # ================================================================
        self.fixed_hide(b, run_time=0.35)
        iso_title = Text("LAS VISTAS SON LAS MISMAS · CAMBIA SU POSICIÓN EN LA HOJA", font_size=36, color=INK, weight=BOLD)
        iso_title.to_edge(UP, buff=0.38)
        iso_sub = Text("ISO A (tercer diedro) frente a ISO E (primer diedro)", font_size=25, color=MUTED)
        iso_sub.next_to(iso_title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(iso_title, iso_sub)
        iso_title.set_opacity(0); iso_sub.set_opacity(0)
        self.play(iso_title.animate.set_opacity(1), iso_sub.animate.set_opacity(1), run_time=T(0.75))

        # Use inherited clean 2D view factories; animate actual relocation, not a static diagram.
        fa = self.front_view_2d(0.52)
        ta = self.top_view_2d(0.47)
        ra = self.right_view_2d(0.55)
        fe = fa.copy(); te = ta.copy(); re = ra.copy()

        labA = Text("ISO A", font_size=28, color=FRONT_COLOR, weight=BOLD).move_to(LEFT*4.15 + UP*2.55)
        labE = Text("ISO E", font_size=28, color=TOP_COLOR, weight=BOLD).move_to(RIGHT*4.15 + UP*2.55)
        sep = Line(UP*2.70, DOWN*2.70, color=GRID, stroke_width=1.4)
        groupA = VGroup(fa,ta,ra)
        groupE = VGroup(fe,te,re)
        fa.move_to(LEFT*4.15 + DOWN*0.20)
        ta.move_to(LEFT*4.15 + UP*1.55)
        ra.move_to(LEFT*1.85 + DOWN*0.20)
        fe.move_to(RIGHT*4.15 + DOWN*0.20)
        te.move_to(RIGHT*4.15 + DOWN*2.00)
        re.move_to(RIGHT*1.85 + DOWN*0.20)
        self.add_fixed_in_frame_mobjects(labA, labE, sep, groupA, groupE)
        for m in (labA, labE, sep, groupA, groupE): m.set_opacity(0)
        self.play(labA.animate.set_opacity(1), labE.animate.set_opacity(1), sep.animate.set_opacity(1), run_time=T(0.65))
        self.play(groupA.animate.set_opacity(1), run_time=T(1.00))
        self.wait(T(1.20))
        self.play(groupE.animate.set_opacity(1), run_time=T(1.00))
        self.wait(T(2.60))

        # ================================================================
        # 11 · FINAL MENTAL MODEL — large, sparse, memorable
        # ================================================================
        self.play(
            iso_title.animate.set_opacity(0), iso_sub.animate.set_opacity(0),
            labA.animate.set_opacity(0), labE.animate.set_opacity(0), sep.animate.set_opacity(0),
            groupA.animate.set_opacity(0), groupE.animate.set_opacity(0),
            run_time=T(0.80),
        )
        self.remove_fixed_in_frame_mobjects(iso_title, iso_sub, labA, labE, sep, groupA, groupE)

        words = [
            ("MIRAR", FRONT_COLOR),
            ("PROYECTAR ⟂", INK),
            ("TRAZAR", TOP_COLOR),
            ("ABATIR", RIGHT_COLOR),
            ("ALINEAR", INK),
        ]
        cards = VGroup()
        for i,(txt,col) in enumerate(words, start=1):
            circ = Circle(radius=0.32, stroke_color=col, stroke_width=2.6, fill_color=WHITE, fill_opacity=1)
            num = Text(str(i), font_size=24, color=col, weight=BOLD).move_to(circ)
            lab = Text(txt, font_size=26, color=INK, weight=BOLD)
            card = VGroup(VGroup(circ,num), lab).arrange(DOWN, buff=0.16)
            cards.add(card)
        cards.arrange(RIGHT, buff=0.70)
        cards.scale_to_fit_width(13.4)
        final_title = Text("DE UN OBJETO 3D A UNA HOJA 2D", font_size=43, color=INK, weight=BOLD)
        final_note = Text("No es perspectiva: cada vista nace de proyectantes paralelas y perpendiculares al plano.", font_size=25, color=MUTED)
        final = VGroup(final_title, cards, final_note).arrange(DOWN, buff=0.52)
        self.add_fixed_in_frame_mobjects(final)
        final.set_opacity(0)
        self.play(final_title.animate.set_opacity(1), run_time=T(0.70))
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.10) for c in cards], lag_ratio=0.14), run_time=T(2.20))
        self.play(final_note.animate.set_opacity(1), run_time=T(0.70))
        self.wait(T(4.60))
        self.play(final.animate.set_opacity(0), run_time=T(0.90))
        self.remove_fixed_in_frame_mobjects(final)


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V14_REBUILT_CHOREOGRAPHY.py Projection3Dto2DV14RebuiltChoreography --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V14_REBUILT_CHOREOGRAPHY.py Projection3Dto2DV14RebuiltChoreography --disable_caching
