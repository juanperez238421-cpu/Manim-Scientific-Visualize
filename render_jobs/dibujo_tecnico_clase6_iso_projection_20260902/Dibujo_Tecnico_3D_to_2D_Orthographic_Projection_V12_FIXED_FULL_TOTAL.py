#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V12 FIXED FULL TOTAL.

Full-total revision of the validated V8 orthographic-projection lesson.

The V8 full-frame audit revealed a systematic vertical-composition defect:
after the opening title, the 3D construction occupied the lower half of the
1920×1080 frame.  The geometry was correct, but the camera frame center and the
fixed bottom chips made the lesson read visually too low.

V11 preserves the validated stepped solid, FRONT/TOP/RIGHT projections, PV/PH
fold, alignment logic and final 2D views, while correcting the composition:

* the title is presented as a clean title-only beat;
* every subsequent 3D stage is lifted on screen by lowering the camera's world
  z frame center (screen-space effect = content moves UP);
* all fixed section chips are lifted away from the lower safe edge;
* the final sheet, five-step method and synthesis are shifted upward modestly;
* pacing is kept classroom-friendly with clear holds before/after transitions;
* V8's stronger labels, view strokes and publication-safe style are retained.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh final.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_FULL_TOTAL_DOWNLOAD_SAFE import (
    Projection3Dto2DFullTotalV8,
)
from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA import (
    INK,
    MUTED,
    GRID,
    PV_COLOR,
    PH_COLOR,
    FRONT_COLOR,
    TOP_COLOR,
    RIGHT_COLOR,
    T as BASE_T,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

# ---------------------------------------------------------------------------
# Director controls
# ---------------------------------------------------------------------------
# At phi≈64°, world +z contributes strongly to screen +y. Lowering camera
# frame-center z therefore raises the entire 3D construction on screen.
CAMERA_Z_UPSHIFT = 1.55
CHIP_UPSHIFT = 0.75
SCREEN_GROUP_UPSHIFT = 0.55
V11_GLOBAL_PACE = 1.25
V12_DELIVERY_QA_REVISION = "hard-tech + visual-audit + immutable-redownload"
FOLD_EXTRA_UPSHIFT = 1.20
FINAL_UPSHIFT = 1.15


def T(seconds):
    # Classroom pace wrapper: keep preview scaling while making the final easier to read.
    return BASE_T(seconds * V11_GLOBAL_PACE)


class Projection3Dto2DV12FixedFullTotal(Projection3Dto2DFullTotalV8):
    """V8 geometry/legibility + corrected upper-screen composition."""

    def section_chip(self, text, width=7.0):
        """Keep stage captions inside the lower safe zone, but visibly higher."""
        chip = super().section_chip(text, width)
        chip.shift(UP * CHIP_UPSHIFT)
        return chip

    @staticmethod
    def lifted_center(x: float, y: float, z: float):
        """Convert a validated V7/V8 camera center to the V9 upper layout."""
        return np.array([x, y, z - CAMERA_Z_UPSHIFT], dtype=float)

    def construct(self):
        # Camera is already prepared for the post-title upper composition.
        focus = self.lifted_center(0.0, 1.85, 1.48)
        self.set_camera_orientation(
            phi=64 * DEGREES,
            theta=-52 * DEGREES,
            gamma=0,
            zoom=1.06,
            frame_center=focus,
        )

        # ------------------------------------------------------------------
        # 0 · TITLE ONLY.  Do not compete with geometry yet.
        # ------------------------------------------------------------------
        title = Text("DE UN OBJETO 3D A SUS VISTAS 2D", font_size=44, color=INK, weight=BOLD)
        subtitle = Text(
            "La vista se construye por proyección ortogonal, no por perspectiva.",
            font_size=24, color=MUTED,
        )
        title.to_edge(UP, buff=0.55)
        subtitle.next_to(title, DOWN, buff=0.14)
        self.fixed_fade_in(title, subtitle, run_time=T(0.80))
        self.wait(T(1.80))
        self.fixed_fade_out(title, subtitle, run_time=T(0.60))
        self.wait(T(0.35))

        # ------------------------------------------------------------------
        # 1 · RECOGNIZE THE VOLUME — now intentionally in upper-middle frame.
        # ------------------------------------------------------------------
        intro = self.section_chip("0 · PRIMERO: RECONOCEMOS EL VOLUMEN", 5.70)
        self.fixed_fade_in(intro, run_time=T(0.42))

        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.10), run_time=T(1.05))
        self.wait(T(1.25))

        self.move_camera(
            theta=-68 * DEGREES, phi=60 * DEGREES, zoom=1.10,
            frame_center=focus, run_time=T(1.75),
        )
        self.wait(T(0.45))
        self.move_camera(
            theta=-35 * DEGREES, phi=70 * DEGREES, zoom=1.08,
            frame_center=focus, run_time=T(1.75),
        )
        self.wait(T(0.45))
        self.move_camera(
            theta=-52 * DEGREES, phi=64 * DEGREES, zoom=1.06,
            frame_center=focus, run_time=T(1.65),
        )
        self.wait(T(1.35))
        self.fixed_fade_out(intro, run_time=T(0.25))

        # ------------------------------------------------------------------
        # 2 · OBSERVATION DIRECTIONS
        # ------------------------------------------------------------------
        cue = self.section_chip("1 · UN OBJETO · TRES DIRECCIONES DE OBSERVACIÓN", 6.60)
        self.fixed_fade_in(cue, run_time=T(0.42))

        front_arrow = Arrow3D(
            start=np.array([0.15, 4.15, 1.55]), end=np.array([0.15, 3.30, 1.55]),
            color=FRONT_COLOR, thickness=0.025, height=0.26, base_radius=0.085,
        )
        top_arrow = Arrow3D(
            start=np.array([-0.35, 1.90, 3.85]), end=np.array([-0.35, 1.90, 3.00]),
            color=TOP_COLOR, thickness=0.025, height=0.26, base_radius=0.085,
        )
        right_arrow = Arrow3D(
            start=np.array([3.65, 1.80, 1.55]), end=np.array([2.78, 1.80, 1.55]),
            color=RIGHT_COLOR, thickness=0.025, height=0.26, base_radius=0.085,
        )
        lf = self.direction_label_3d("FRONT", np.array([0.15, 4.28, 1.78]), FRONT_COLOR)
        lt = self.direction_label_3d("TOP", np.array([-0.35, 1.95, 4.02]), TOP_COLOR)
        lr = self.direction_label_3d("RIGHT", np.array([3.80, 1.80, 1.83]), RIGHT_COLOR)
        for lab in (lf, lt, lr):
            lab.set_opacity(0)

        self.play(FadeIn(front_arrow), lf.animate.set_opacity(1), run_time=T(0.70))
        self.wait(T(0.55))
        self.play(FadeIn(top_arrow), lt.animate.set_opacity(1), run_time=T(0.70))
        self.wait(T(0.55))
        self.play(FadeIn(right_arrow), lr.animate.set_opacity(1), run_time=T(0.70))
        self.wait(T(1.35))
        self.play(
            FadeOut(front_arrow), FadeOut(top_arrow), FadeOut(right_arrow),
            lf.animate.set_opacity(0), lt.animate.set_opacity(0), lr.animate.set_opacity(0),
            run_time=T(0.70),
        )
        self.fixed_fade_out(cue, run_time=T(0.22))

        # ------------------------------------------------------------------
        # 3 · PROJECTION PLANES
        # ------------------------------------------------------------------
        PLANE_W = 5.75
        PV_H = 3.30
        PH_D = 3.55
        SIDE_X = 2.58

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
        side = Rectangle(
            width=PH_D, height=PV_H,
            stroke_color=RIGHT_COLOR, stroke_width=2.0,
            fill_color=RIGHT_COLOR, fill_opacity=0.085,
        ).rotate(PI / 2, axis=UP).move_to(np.array([SIDE_X, PH_D / 2, PV_H / 2]))
        line_earth = Line(
            np.array([-PLANE_W / 2, 0, 0]), np.array([PLANE_W / 2, 0, 0]),
            color=INK, stroke_width=3.4,
        )

        pv_lab = self.plane_label_3d("PV · FRONT", np.array([-2.05, 0.04, 3.05]), PV_COLOR)
        ph_lab = self.plane_label_3d("PH · TOP", np.array([-2.05, 3.12, 0.08]), TOP_COLOR)
        pr_lab = self.plane_label_3d("PL · RIGHT", np.array([2.62, 3.15, 2.92]), RIGHT_COLOR)
        for lab in (pv_lab, ph_lab, pr_lab):
            lab.set_opacity(0)

        planes_cue = self.section_chip("2 · CADA MIRADA RECIBE UNA PROYECCIÓN PERPENDICULAR", 7.75)
        self.fixed_fade_in(planes_cue, run_time=T(0.42))
        plane_center = self.lifted_center(0.0, 1.72, 1.48)
        self.move_camera(zoom=0.98, frame_center=plane_center, run_time=T(0.85))
        self.play(Create(pv), pv_lab.animate.set_opacity(1), run_time=T(0.90))
        self.wait(T(0.55))
        self.play(Create(ph), ph_lab.animate.set_opacity(1), Create(line_earth), run_time=T(0.90))
        self.wait(T(0.55))
        self.play(Create(side), pr_lab.animate.set_opacity(1), run_time=T(0.90))
        self.wait(T(1.40))
        self.fixed_fade_out(planes_cue, run_time=T(0.22))

        # ------------------------------------------------------------------
        # 4 · FRONT → ALZADO — explicit three-beat construction
        # ------------------------------------------------------------------
        cue_f = self.section_chip("3 · ALZADO · 1 DIRECCIÓN → 2 PROYECTORES → 3 CONTORNO", 7.55)
        self.fixed_fade_in(cue_f, run_time=T(0.45))
        self.wait(T(0.80))
        front_sources = [
            [-2.30,0.75,0.35], [2.30,0.75,0.35], [2.30,0.75,1.05],
            [0.85,1.00,1.05], [0.85,1.00,1.85], [-0.15,1.28,1.85],
            [-0.15,1.28,2.75], [-1.25,1.28,2.75], [-1.70,1.00,1.85],
            [-2.30,0.75,1.05],
        ]
        front_rays = VGroup(*[
            self.projector(p, [p[0], 0.025, p[2]], FRONT_COLOR) for p in front_sources
        ])
        front = self.front_outline()
        self.play(
            LaggedStart(*[Create(r) for r in front_rays[:4]], lag_ratio=0.12),
            run_time=T(1.20),
        )
        self.wait(T(0.95))
        self.play(
            LaggedStart(*[Create(r) for r in front_rays[4:]], lag_ratio=0.08),
            run_time=T(1.55),
        )
        self.wait(T(0.90))
        self.play(Create(front), run_time=T(1.35))
        self.wait(T(0.65))
        self.play(Indicate(front, color=FRONT_COLOR, scale_factor=1.015), run_time=T(1.00))
        self.wait(T(2.00))
        self.play(FadeOut(front_rays), run_time=T(0.75))
        self.wait(T(0.70))
        self.fixed_fade_out(cue_f, run_time=T(0.25))

        # ------------------------------------------------------------------
        # 5 · TOP → PLANTA — outer footprint, then inner tiers
        # ------------------------------------------------------------------
        cue_t = self.section_chip("4 · PLANTA · 1 DIRECCIÓN → 2 PROYECTORES → 3 CONTORNO", 7.55)
        self.fixed_fade_in(cue_t, run_time=T(0.45))
        self.wait(T(0.80))
        top_sources = [
            [-2.30,0.75,1.05], [2.30,0.75,1.05], [2.30,3.05,1.05], [-2.30,3.05,1.05],
            [-1.70,1.00,1.85], [0.85,1.00,1.85], [0.85,2.72,1.85], [-1.70,2.72,1.85],
            [-1.25,1.28,2.75], [-0.15,1.28,2.75], [-0.15,2.34,2.75], [-1.25,2.34,2.75],
        ]
        top_rays = VGroup(*[
            self.projector(p, [p[0], p[1], 0.025], TOP_COLOR) for p in top_sources
        ])
        top = self.top_outline()
        self.play(
            LaggedStart(*[Create(r) for r in top_rays[:4]], lag_ratio=0.12),
            run_time=T(1.20),
        )
        self.wait(T(0.95))
        self.play(
            LaggedStart(*[Create(r) for r in top_rays[4:]], lag_ratio=0.07),
            run_time=T(1.70),
        )
        self.wait(T(0.90))
        self.play(Create(top[0]), run_time=T(0.95))
        self.wait(T(0.55))
        self.play(Create(top[1]), run_time=T(0.80))
        self.wait(T(0.50))
        self.play(Create(top[2]), run_time=T(0.80))
        self.play(Indicate(top, color=TOP_COLOR, scale_factor=1.012), run_time=T(1.00))
        self.wait(T(2.00))
        self.play(FadeOut(top_rays), run_time=T(0.75))
        self.wait(T(0.70))
        self.fixed_fade_out(cue_t, run_time=T(0.25))

        # ------------------------------------------------------------------
        # 6 · RIGHT → PERFIL — explicit anchor projectors and contour
        # ------------------------------------------------------------------
        cue_r = self.section_chip("5 · PERFIL · 1 DIRECCIÓN → 2 PROYECTORES → 3 CONTORNO", 7.55)
        self.fixed_fade_in(cue_r, run_time=T(0.45))
        self.wait(T(0.80))
        right_sources = [
            [2.30,0.75,0.35], [2.30,3.05,0.35], [2.30,3.05,1.05], [2.30,0.75,1.05],
            [0.85,1.00,1.85], [0.85,2.72,1.85],
            [-0.15,1.28,2.75], [-0.15,2.34,2.75],
        ]
        right_rays = VGroup(*[
            self.projector(p, [SIDE_X, p[1], p[2]], RIGHT_COLOR) for p in right_sources
        ])
        right = self.right_outline(SIDE_X)
        self.play(
            LaggedStart(*[Create(r) for r in right_rays[:4]], lag_ratio=0.12),
            run_time=T(1.20),
        )
        self.wait(T(0.95))
        self.play(
            LaggedStart(*[Create(r) for r in right_rays[4:]], lag_ratio=0.10),
            run_time=T(1.35),
        )
        self.wait(T(0.90))
        self.play(Create(right), run_time=T(1.35))
        self.wait(T(0.65))
        self.play(Indicate(right, color=RIGHT_COLOR, scale_factor=1.012), run_time=T(1.00))
        self.wait(T(2.00))
        self.play(FadeOut(right_rays), run_time=T(0.75))
        self.wait(T(0.70))
        self.fixed_fade_out(cue_r, run_time=T(0.25))

        # Hold the complete physical construction with a slow camera read.
        complete = self.section_chip("MISMO OBJETO 3D → TRES PROYECCIONES 2D", 6.10)
        self.fixed_fade_in(complete, run_time=T(0.45))
        complete_center = self.lifted_center(0.0, 1.70, 1.45)
        self.move_camera(
            theta=-61 * DEGREES, phi=61 * DEGREES, zoom=0.95,
            frame_center=complete_center, run_time=T(1.90),
        )
        self.wait(T(1.15))
        self.move_camera(
            theta=-48 * DEGREES, phi=65 * DEGREES, zoom=0.98,
            frame_center=complete_center, run_time=T(1.80),
        )
        self.wait(T(2.40))
        self.fixed_fade_out(complete, run_time=T(0.25))

        # ------------------------------------------------------------------
        # 7 · REMOVE SOURCE BODY
        # ------------------------------------------------------------------
        keep = self.section_chip("6 · RETIRAMOS EL OBJETO · LAS PROYECCIONES PERMANECEN", 7.05)
        self.fixed_fade_in(keep, run_time=T(0.45))
        self.wait(T(0.85))
        self.play(FadeOut(solid), run_time=T(1.25))
        self.wait(T(1.90))
        self.fixed_fade_out(keep, run_time=T(0.25))
        self.play(FadeOut(side), FadeOut(right), pr_lab.animate.set_opacity(0), run_time=T(0.90))
        self.wait(T(0.90))

        # ------------------------------------------------------------------
        # 8 · LITERAL PH ABATIMIENTO — preserve V10 safe-area correction
        # ------------------------------------------------------------------
        unfold = self.section_chip("7 · ABATIMIENTO · PH GIRA 90° SOBRE LA LÍNEA DE TIERRA", 7.25)
        self.fixed_fade_in(unfold, run_time=T(0.45))
        self.wait(T(0.90))
        fold_center = self.lifted_center(0.0, 1.62, 1.00) + np.array([0.0, 0.0, -FOLD_EXTRA_UPSHIFT])
        self.move_camera(zoom=0.94, frame_center=fold_center, run_time=T(1.35))
        self.wait(T(1.15))
        self.play(
            Rotate(
                VGroup(ph, top),
                angle=-PI / 2,
                axis=RIGHT,
                about_point=ORIGIN,
                rate_func=smooth,
            ),
            run_time=T(4.80),
        )
        self.wait(T(2.20))
        self.move_camera(
            phi=90 * DEGREES, theta=90 * DEGREES, gamma=0,
            zoom=1.10, frame_center=self.lifted_center(0.0, 0.0, 0.05),
            run_time=T(2.30),
        )
        self.wait(T(2.00))
        self.fixed_fade_out(unfold, run_time=T(0.25))

        # ------------------------------------------------------------------
        # 9 · ALIGNMENT GUIDES
        # ------------------------------------------------------------------
        align = self.section_chip("8 · LAS DIMENSIONES COMUNES QUEDAN ALINEADAS", 6.05)
        self.fixed_fade_in(align, run_time=T(0.45))
        self.wait(T(0.85))
        guides = VGroup(*[
            Line(
                np.array([x, 0.03, 3.00]), np.array([x, 0.03, -3.00]),
                stroke_color=GRID, stroke_width=1.6, stroke_opacity=0.78,
            )
            for x in (-2.30, -1.70, -1.25, -0.15, 0.85, 2.30)
        ])
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.10), run_time=T(1.65))
        self.wait(T(2.50))
        self.play(FadeOut(guides), run_time=T(0.65))
        self.fixed_fade_out(align, run_time=T(0.25))

        self.play(
            FadeOut(pv), FadeOut(ph), FadeOut(line_earth), FadeOut(front), FadeOut(top),
            pv_lab.animate.set_opacity(0), ph_lab.animate.set_opacity(0),
            run_time=T(1.10),
        )
        self.wait(T(1.20))

        # ------------------------------------------------------------------
        # 10 · 2D CONSTRUCTION STUDIO — one view at a time, then park RIGHT
        # ------------------------------------------------------------------
        studio_title = Text("CONSTRUCCIÓN 2D · UNA VISTA A LA VEZ", font_size=36, color=INK, weight=BOLD)
        studio_title.move_to(np.array([-1.15, 3.76, 0]))
        archive_title = Text("VISTAS TERMINADAS", font_size=23, color=MUTED, weight=BOLD)
        archive_title.move_to(np.array([5.30, 3.28, 0]))
        divider = Line(np.array([3.18, 3.05, 0]), np.array([3.18, -3.45, 0]), color=GRID, stroke_width=1.5)
        studio_shell = VGroup(studio_title, archive_title, divider)
        self.add_fixed_in_frame_mobjects(studio_shell)
        studio_shell.set_opacity(0)
        self.play(studio_title.animate.set_opacity(1), run_time=T(0.75))
        self.wait(T(1.20))
        self.play(archive_title.animate.set_opacity(1), divider.animate.set_opacity(1), run_time=T(0.75))
        self.wait(T(0.80))

        def segmented_polygon(poly, color, stroke_width=4.6):
            verts = list(poly.get_vertices())
            return VGroup(*[
                Line(verts[i], verts[(i + 1) % len(verts)], color=color, stroke_width=stroke_width)
                for i in range(len(verts))
            ])

        def make_card_frame(width, height, label, color, center):
            box = RoundedRectangle(
                width=width, height=height, corner_radius=0.12,
                stroke_color=GRID, stroke_width=1.6,
                fill_color=WHITE, fill_opacity=1.0,
            ).move_to(center)
            lab = Text(label, font_size=25, color=color, weight=BOLD).next_to(box, DOWN, buff=0.10)
            return box, lab

        def phase_text(text, color):
            m = Text(text, font_size=24, color=color, weight=BOLD)
            m.move_to(np.array([-1.55, 2.86, 0]))
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0)
            return m

        work_center = np.array([-1.55, -0.25, 0])
        archive_x = 5.30

        # 10A · FRONT / ALZADO
        phase = phase_text("ALZADO · PASO 1/3 · IDENTIFICA LA DIRECCIÓN FRONTAL", FRONT_COLOR)
        fbox, flab = make_card_frame(7.10, 4.00, "FRONT / ALZADO", FRONT_COLOR, work_center)
        fpoly = self.front_view_2d(1.12).move_to(work_center + UP * 0.05)
        fsegments = segmented_polygon(fpoly, FRONT_COLOR, 4.8)
        front_card = VGroup(fbox, fsegments, flab)
        self.add_fixed_in_frame_mobjects(front_card)
        fbox.set_opacity(0); flab.set_opacity(0)
        for seg in fsegments: seg.set_opacity(0)
        self.play(fbox.animate.set_opacity(1), phase.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.80))
        self.play(phase.animate.set_opacity(0), run_time=T(0.40))
        phase2 = phase_text("ALZADO · PASO 2/3 · LOS RAYOS LLEGAN PERPENDICULARES AL PV", FRONT_COLOR)
        self.play(phase2.animate.set_opacity(1), run_time=T(0.55))
        self.wait(T(1.85))
        self.play(phase2.animate.set_opacity(0), run_time=T(0.40))
        phase3 = phase_text("ALZADO · PASO 3/3 · TRAZA EL CONTORNO VISIBLE", FRONT_COLOR)
        self.play(phase3.animate.set_opacity(1), run_time=T(0.55))
        self.play(
            LaggedStart(*[seg.animate.set_opacity(1) for seg in fsegments], lag_ratio=0.085),
            run_time=T(2.70),
        )
        self.play(flab.animate.set_opacity(1), run_time=T(0.60))
        self.wait(T(2.10))
        self.play(phase3.animate.set_opacity(0), run_time=T(0.40))
        self.remove_fixed_in_frame_mobjects(phase, phase2, phase3)
        self.play(
            front_card.animate.scale(0.50).move_to(np.array([archive_x, 2.05, 0])),
            run_time=T(1.65), rate_func=smooth,
        )
        self.wait(T(1.55))

        # 10B · TOP / PLANTA
        phase = phase_text("PLANTA · PASO 1/3 · IDENTIFICA LA DIRECCIÓN SUPERIOR", TOP_COLOR)
        tbox, tlab = make_card_frame(7.10, 4.00, "TOP / PLANTA", TOP_COLOR, work_center)
        tshapes = self.top_view_2d(1.10).move_to(work_center + UP * 0.05)
        top_card = VGroup(tbox, tshapes, tlab)
        self.add_fixed_in_frame_mobjects(top_card)
        tbox.set_opacity(0); tlab.set_opacity(0)
        for shape in tshapes: shape.set_opacity(0)
        self.play(tbox.animate.set_opacity(1), phase.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.80))
        self.play(phase.animate.set_opacity(0), run_time=T(0.40))
        phase2 = phase_text("PLANTA · PASO 2/3 · LOS RAYOS BAJAN PERPENDICULARES AL PH", TOP_COLOR)
        self.play(phase2.animate.set_opacity(1), run_time=T(0.55))
        self.wait(T(1.85))
        self.play(phase2.animate.set_opacity(0), run_time=T(0.40))
        phase3 = phase_text("PLANTA · PASO 3/3 · BASE → NIVEL MEDIO → NIVEL SUPERIOR", TOP_COLOR)
        self.play(phase3.animate.set_opacity(1), run_time=T(0.55))
        self.play(tshapes[0].animate.set_opacity(1), run_time=T(1.00))
        self.wait(T(0.75))
        self.play(tshapes[1].animate.set_opacity(1), run_time=T(0.90))
        self.wait(T(0.75))
        self.play(tshapes[2].animate.set_opacity(1), run_time=T(0.90))
        self.play(tlab.animate.set_opacity(1), run_time=T(0.60))
        self.wait(T(2.10))
        self.play(phase3.animate.set_opacity(0), run_time=T(0.40))
        self.remove_fixed_in_frame_mobjects(phase, phase2, phase3)
        self.play(
            top_card.animate.scale(0.50).move_to(np.array([archive_x, 0.00, 0])),
            run_time=T(1.65), rate_func=smooth,
        )
        self.wait(T(1.55))

        # 10C · RIGHT / PERFIL
        phase = phase_text("PERFIL · PASO 1/3 · IDENTIFICA LA DIRECCIÓN LATERAL", RIGHT_COLOR)
        rbox, rlab = make_card_frame(6.45, 4.00, "RIGHT / PERFIL", RIGHT_COLOR, work_center)
        rpoly = self.right_view_2d(1.18).move_to(work_center + UP * 0.05)
        rsegments = segmented_polygon(rpoly, RIGHT_COLOR, 4.8)
        right_card = VGroup(rbox, rsegments, rlab)
        self.add_fixed_in_frame_mobjects(right_card)
        rbox.set_opacity(0); rlab.set_opacity(0)
        for seg in rsegments: seg.set_opacity(0)
        self.play(rbox.animate.set_opacity(1), phase.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.80))
        self.play(phase.animate.set_opacity(0), run_time=T(0.40))
        phase2 = phase_text("PERFIL · PASO 2/3 · LOS RAYOS LLEGAN PERPENDICULARES AL PL", RIGHT_COLOR)
        self.play(phase2.animate.set_opacity(1), run_time=T(0.55))
        self.wait(T(1.85))
        self.play(phase2.animate.set_opacity(0), run_time=T(0.40))
        phase3 = phase_text("PERFIL · PASO 3/3 · TRAZA EL CONTORNO LATERAL", RIGHT_COLOR)
        self.play(phase3.animate.set_opacity(1), run_time=T(0.55))
        self.play(
            LaggedStart(*[seg.animate.set_opacity(1) for seg in rsegments], lag_ratio=0.085),
            run_time=T(2.70),
        )
        self.play(rlab.animate.set_opacity(1), run_time=T(0.60))
        self.wait(T(2.10))
        self.play(phase3.animate.set_opacity(0), run_time=T(0.40))
        self.remove_fixed_in_frame_mobjects(phase, phase2, phase3)
        self.play(
            right_card.animate.scale(0.50).move_to(np.array([archive_x, -2.05, 0])),
            run_time=T(1.65), rate_func=smooth,
        )
        self.wait(T(2.20))

        # ------------------------------------------------------------------
        # 11 · SAME CARDS → CONVENTIONAL ALIGNED DRAWING SHEET
        # ------------------------------------------------------------------
        final_title = Text("UN OBJETO · TRES DESCRIPCIONES 2D", font_size=35, color=INK, weight=BOLD)
        final_title.move_to(np.array([0.0, 3.72, 0]))
        self.add_fixed_in_frame_mobjects(final_title)
        final_title.set_opacity(0)
        self.play(
            studio_title.animate.set_opacity(0),
            archive_title.animate.set_opacity(0),
            divider.animate.set_opacity(0),
            final_title.animate.set_opacity(1),
            front_card.animate.scale(1.22).move_to(np.array([-1.75, -1.18, 0])),
            top_card.animate.scale(1.22).move_to(np.array([-1.75, 1.78, 0])),
            right_card.animate.scale(1.22).move_to(np.array([3.25, -1.18, 0])),
            run_time=T(2.50), rate_func=smooth,
        )
        vguide = DashedLine(UP * 0.46, DOWN * 0.46, dash_length=0.08, color=GRID, stroke_width=1.6)
        vguide.move_to(np.array([-1.75, 0.30, 0]))
        hguide = DashedLine(LEFT * 0.74, RIGHT * 0.74, dash_length=0.08, color=GRID, stroke_width=1.6)
        hguide.move_to(np.array([0.80, -1.18, 0]))
        self.add_fixed_in_frame_mobjects(vguide, hguide)
        vguide.set_opacity(0); hguide.set_opacity(0)
        self.play(vguide.animate.set_opacity(1), run_time=T(0.80))
        self.wait(T(0.85))
        self.play(hguide.animate.set_opacity(1), run_time=T(0.80))
        self.wait(T(3.60))
        sheet_group = VGroup(final_title, front_card, top_card, right_card, vguide, hguide)
        self.play(sheet_group.animate.set_opacity(0), run_time=T(0.90))
        self.remove_fixed_in_frame_mobjects(sheet_group, studio_shell)

        # ------------------------------------------------------------------
        # 12 · FIVE-STEP METHOD — slower classroom read
        # ------------------------------------------------------------------
        method_title = Text("MÉTODO PARA PASAR DE 3D A 2D", font_size=35, color=INK, weight=BOLD)
        bars = VGroup(
            self.method_bar(1, "ELIGE LA DIRECCIÓN", "frontal · superior · lateral"),
            self.method_bar(2, "COLOCA EL PLANO", "perpendicular a la dirección de observación"),
            self.method_bar(3, "PROYECTA LOS PUNTOS", "usa líneas paralelas y ortogonales al plano"),
            self.method_bar(4, "TRAZA LA VISTA", "une las aristas visibles con la geometría correcta"),
            self.method_bar(5, "ALINEA LAS VISTAS", "conserva las dimensiones comunes entre proyecciones"),
        ).arrange(DOWN, buff=0.16)
        method = VGroup(method_title, bars).arrange(DOWN, buff=0.38)
        method.move_to(ORIGIN + UP * 0.65)
        self.add_fixed_in_frame_mobjects(method)
        method.set_opacity(0)
        self.play(method_title.animate.set_opacity(1), run_time=T(0.70))
        self.wait(T(0.80))
        for bar in bars:
            bar.set_opacity(0)
        for bar in bars:
            self.play(bar.animate.set_opacity(1), run_time=T(0.60))
            self.play(Circumscribe(bar[0], color=FRONT_COLOR, buff=0.04, time_width=0.35), run_time=T(0.85))
            self.wait(T(1.05))
        self.wait(T(2.20))
        self.play(method.animate.set_opacity(0), run_time=T(0.80))
        self.remove_fixed_in_frame_mobjects(method)

        # ------------------------------------------------------------------
        # 13 · CLOSING SYNTHESIS — keep the three views as a visual memory cue
        # ------------------------------------------------------------------
        close1 = Text("OBJETO 3D", font_size=46, color=INK, weight=BOLD)
        arr1 = Arrow(LEFT * 0.72, RIGHT * 0.72, buff=0, color=INK, stroke_width=3.0)
        close2 = Text("PROYECCIÓN ORTOGONAL", font_size=32, color=INK, weight=BOLD)
        arr2 = Arrow(LEFT * 0.72, RIGHT * 0.72, buff=0, color=INK, stroke_width=3.0)
        close3 = Text("VISTAS 2D", font_size=46, color=INK, weight=BOLD)
        synthesis = VGroup(close1, arr1, close2, arr2, close3).arrange(RIGHT, buff=0.35)
        synthesis.scale_to_fit_width(13.4)
        note = Text(
            "Una dirección de observación produce una vista; las tres describen el mismo objeto.",
            font_size=25, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.50)
        mini_front = self.front_view_2d(0.34)
        mini_top = self.top_view_2d(0.31)
        mini_right = self.right_view_2d(0.38)
        mini_views = VGroup(mini_front, mini_top, mini_right).arrange(RIGHT, buff=0.70)
        mini_views.next_to(note, DOWN, buff=0.55)
        final = VGroup(synthesis, note, mini_views).shift(UP * FINAL_UPSHIFT)
        self.add_fixed_in_frame_mobjects(final)
        final.set_opacity(0)
        self.play(final.animate.set_opacity(1), run_time=T(1.10))
        self.wait(T(4.80))
        self.play(final.animate.set_opacity(0), run_time=T(0.90))
        self.remove_fixed_in_frame_mobjects(final)


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V11_STEPWISE_VIEWS_DIRECTOR_QA.py Projection3Dto2DV12FixedFullTotal --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V11_STEPWISE_VIEWS_DIRECTOR_QA.py Projection3Dto2DV12FixedFullTotal --disable_caching
