#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V7 SENIOR QA · objeto 3D → vistas 2D.

Revision goals after full V6 visual/code audit:
- reclaim the unused 16:9 canvas;
- enlarge the geometric construction and center the camera on the geometry;
- replace the too-simple two-box object with a three-tier stepped bracket whose
  FRONT / TOP / RIGHT orthographic views are all visually distinctive;
- slow important geometric motions and add intentional classroom pauses;
- remove the V6 method-card Indicate fill bug that temporarily turned cards dark;
- derive every 2D view from the exact same dimensional model;
- preserve literal PV / PH geometry and the 90° Monge abatimiento around LT.

ManimCE 0.20.1 · 1920×1080 · 30 fps · final literal -pqh render.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Dibujo_Tecnico_Sistema_Diedrico_Monge_V5_SENIOR_FAITHFUL import (
    DihedralSystemMongeSeniorV5,
    INK, MUTED, GRID,
    PV_COLOR, PH_COLOR,
    FRONT_COLOR, TOP_COLOR,
    T,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

RIGHT_COLOR = "#5D7462"
SOLID_BASE = "#E8EBEE"
SOLID_MID = "#D5DBE1"
SOLID_TOP = "#BEC8D2"
PAPER = "#FBFBFB"
SOFT = "#F2F4F5"


class Projection3Dto2DSeniorV7(DihedralSystemMongeSeniorV5):
    """Large-format, pause-driven orthographic projection lesson."""

    # ------------------------------------------------------------------
    # Shared dimensional model
    # ------------------------------------------------------------------
    # Base      x[-2.30, 2.30], y[0.75, 3.05], z[0.35, 1.05]
    # Mid tier  x[-1.70, 0.85], y[1.00, 2.72], z[1.05, 1.85]
    # Top tier  x[-1.25,-0.15], y[1.28, 2.34], z[1.85, 2.75]
    # This creates a clear three-step FRONT silhouette, nested TOP footprint
    # and a three-step RIGHT silhouette.

    def make_solid(self):
        base = self.box3d([4.60, 2.30, 0.70], [0.00, 1.90, 0.70], SOLID_BASE, 0.62)
        mid = self.box3d([2.55, 1.72, 0.80], [-0.425, 1.86, 1.45], SOLID_MID, 0.68)
        top = self.box3d([1.10, 1.06, 0.90], [-0.70, 1.81, 2.30], SOLID_TOP, 0.74)
        return VGroup(base, mid, top)

    def front_outline(self, y=0.025):
        pts = [
            [-2.30, y, 0.35], [2.30, y, 0.35],
            [2.30, y, 1.05], [0.85, y, 1.05],
            [0.85, y, 1.85], [-0.15, y, 1.85],
            [-0.15, y, 2.75], [-1.25, y, 2.75],
            [-1.25, y, 1.85], [-1.70, y, 1.85],
            [-1.70, y, 1.05], [-2.30, y, 1.05],
        ]
        return Polygon(
            *[np.array(p, dtype=float) for p in pts],
            stroke_color=FRONT_COLOR, stroke_width=5.0,
            fill_color=FRONT_COLOR, fill_opacity=0.035,
        )

    def top_outline(self, z=0.025):
        base = Polygon(
            np.array([-2.30, 0.75, z]), np.array([2.30, 0.75, z]),
            np.array([2.30, 3.05, z]), np.array([-2.30, 3.05, z]),
            stroke_color=TOP_COLOR, stroke_width=5.0,
            fill_color=TOP_COLOR, fill_opacity=0.025,
        )
        mid = Polygon(
            np.array([-1.70, 1.00, z]), np.array([0.85, 1.00, z]),
            np.array([0.85, 2.72, z]), np.array([-1.70, 2.72, z]),
            stroke_color=TOP_COLOR, stroke_width=3.4, fill_opacity=0,
        )
        top = Polygon(
            np.array([-1.25, 1.28, z]), np.array([-0.15, 1.28, z]),
            np.array([-0.15, 2.34, z]), np.array([-1.25, 2.34, z]),
            stroke_color=TOP_COLOR, stroke_width=3.0, fill_opacity=0,
        )
        return VGroup(base, mid, top)

    def right_outline(self, x=2.58):
        pts = [
            [x, 0.75, 0.35], [x, 3.05, 0.35],
            [x, 3.05, 1.05], [x, 2.72, 1.05],
            [x, 2.72, 1.85], [x, 2.34, 1.85],
            [x, 2.34, 2.75], [x, 1.28, 2.75],
            [x, 1.28, 1.85], [x, 1.00, 1.85],
            [x, 1.00, 1.05], [x, 0.75, 1.05],
        ]
        return Polygon(
            *[np.array(p, dtype=float) for p in pts],
            stroke_color=RIGHT_COLOR, stroke_width=5.0,
            fill_color=RIGHT_COLOR, fill_opacity=0.035,
        )

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def section_chip(self, text, width=7.0):
        chip = self.chip(text, width, 23)
        chip.to_edge(DOWN, buff=0.28)
        return chip

    def plane_label_3d(self, text, pos, color):
        lab = Text(text, font_size=24, color=color, weight=BOLD).move_to(pos)
        self.add_fixed_orientation_mobjects(lab)
        return lab

    def direction_label_3d(self, text, pos, color):
        lab = Text(text, font_size=23, color=color, weight=BOLD).move_to(pos)
        self.add_fixed_orientation_mobjects(lab)
        return lab

    # ------------------------------------------------------------------
    # Exact screen-space 2D versions of the same model
    # ------------------------------------------------------------------
    def front_view_2d(self, scale=1.0):
        pts = [
            (-2.30, -1.20), (2.30, -1.20),
            (2.30, -0.50), (0.85, -0.50),
            (0.85, 0.30), (-0.15, 0.30),
            (-0.15, 1.20), (-1.25, 1.20),
            (-1.25, 0.30), (-1.70, 0.30),
            (-1.70, -0.50), (-2.30, -0.50),
        ]
        return Polygon(
            *[np.array([x, y, 0.0]) * scale for x, y in pts],
            stroke_color=FRONT_COLOR, stroke_width=4.4,
            fill_color=WHITE, fill_opacity=1.0,
        )

    def top_view_2d(self, scale=1.0):
        outer = Rectangle(
            width=4.60 * scale, height=2.30 * scale,
            stroke_color=TOP_COLOR, stroke_width=4.4,
            fill_color=WHITE, fill_opacity=1.0,
        )
        mid = Rectangle(
            width=2.55 * scale, height=1.72 * scale,
            stroke_color=TOP_COLOR, stroke_width=3.1, fill_opacity=0,
        )
        top = Rectangle(
            width=1.10 * scale, height=1.06 * scale,
            stroke_color=TOP_COLOR, stroke_width=2.8, fill_opacity=0,
        )
        # offsets measured from base center x=0, y=1.90
        mid.move_to(outer.get_center() + LEFT * (0.425 * scale) + DOWN * (0.04 * scale))
        top.move_to(outer.get_center() + LEFT * (0.70 * scale) + DOWN * (0.09 * scale))
        return VGroup(outer, mid, top)

    def right_view_2d(self, scale=1.0):
        # horizontal axis = depth y (0.75..3.05), vertical = z
        pts = [
            (-1.15, -1.20), (1.15, -1.20),
            (1.15, -0.50), (0.82, -0.50),
            (0.82, 0.30), (0.44, 0.30),
            (0.44, 1.20), (-0.62, 1.20),
            (-0.62, 0.30), (-0.90, 0.30),
            (-0.90, -0.50), (-1.15, -0.50),
        ]
        return Polygon(
            *[np.array([x, y, 0.0]) * scale for x, y in pts],
            stroke_color=RIGHT_COLOR, stroke_width=4.4,
            fill_color=WHITE, fill_opacity=1.0,
        )

    def view_panel(self, view, label, color, width, height):
        panel = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=GRID, stroke_width=1.5,
            fill_color=PAPER, fill_opacity=1.0,
        )
        if view.width > width - 0.50:
            view.scale_to_fit_width(width - 0.50)
        if view.height > height - 0.70:
            view.scale_to_fit_height(height - 0.70)
        view.move_to(panel.get_center() + UP * 0.10)
        lab = Text(label, font_size=24, color=color, weight=BOLD).next_to(panel, DOWN, buff=0.10)
        return VGroup(panel, view, lab)

    def method_bar(self, number, title, detail):
        box = RoundedRectangle(
            width=11.8, height=0.82, corner_radius=0.10,
            stroke_color=GRID, stroke_width=1.35,
            fill_color=WHITE, fill_opacity=1.0,
        )
        badge = Circle(radius=0.24, stroke_color=INK, stroke_width=1.8, fill_color=SOFT, fill_opacity=1)
        n = Text(str(number), font_size=23, color=INK, weight=BOLD).move_to(badge)
        title_m = Text(title, font_size=23, color=INK, weight=BOLD)
        detail_m = Text(detail, font_size=18, color=MUTED)
        txt = VGroup(title_m, detail_m).arrange(RIGHT, buff=0.25)
        txt.move_to(box.get_center() + RIGHT * 0.25)
        txt.align_to(box, LEFT).shift(RIGHT * 0.95)
        return VGroup(box, badge.move_to(box.get_left() + RIGHT * 0.43), n.move_to(box.get_left() + RIGHT * 0.43), txt)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------
    def construct(self):
        focus = np.array([0.0, 1.85, 1.48])
        self.set_camera_orientation(
            phi=64 * DEGREES,
            theta=-52 * DEGREES,
            gamma=0,
            zoom=1.06,
            frame_center=focus,
        )

        # 0 · Title only while students establish the object.
        title = Text("DE UN OBJETO 3D A SUS VISTAS 2D", font_size=42, color=INK, weight=BOLD)
        subtitle = Text(
            "La vista se construye por proyección ortogonal, no por perspectiva.",
            font_size=23, color=MUTED,
        )
        title.to_edge(UP, buff=0.30)
        subtitle.next_to(title, DOWN, buff=0.10)
        self.fixed_fade_in(title, subtitle, run_time=0.75)

        intro = self.section_chip("0 · PRIMERO: RECONOCEMOS EL VOLUMEN", 5.70)
        self.fixed_fade_in(intro, run_time=0.42)

        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.10), run_time=T(1.05))
        self.wait(T(1.10))

        # Slower, smoother orbit than V6.
        self.move_camera(theta=-68 * DEGREES, phi=60 * DEGREES, zoom=1.10, frame_center=focus, run_time=T(1.65))
        self.move_camera(theta=-35 * DEGREES, phi=70 * DEGREES, zoom=1.08, frame_center=focus, run_time=T(1.65))
        self.move_camera(theta=-52 * DEGREES, phi=64 * DEGREES, zoom=1.06, frame_center=focus, run_time=T(1.55))
        self.wait(T(1.25))
        self.fixed_fade_out(intro, run_time=0.25)

        # Reclaim the title area before the geometric construction.
        self.fixed_fade_out(title, subtitle, run_time=0.45)

        # 1 · Observation directions.
        cue = self.section_chip("1 · UN OBJETO · TRES DIRECCIONES DE OBSERVACIÓN", 6.60)
        self.fixed_fade_in(cue, run_time=0.42)

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

        self.play(
            LaggedStart(FadeIn(front_arrow), FadeIn(top_arrow), FadeIn(right_arrow), lag_ratio=0.18),
            lf.animate.set_opacity(1), lt.animate.set_opacity(1), lr.animate.set_opacity(1),
            run_time=T(1.25),
        )
        self.wait(T(1.40))
        self.play(
            FadeOut(front_arrow), FadeOut(top_arrow), FadeOut(right_arrow),
            lf.animate.set_opacity(0), lt.animate.set_opacity(0), lr.animate.set_opacity(0),
            run_time=T(0.65),
        )
        self.fixed_fade_out(cue, run_time=0.22)

        # 2 · Projection planes, sized around the new larger solid.
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
        self.fixed_fade_in(planes_cue, run_time=0.42)
        self.move_camera(zoom=0.98, frame_center=np.array([0.0, 1.72, 1.48]), run_time=T(0.75))
        self.play(Create(pv), pv_lab.animate.set_opacity(1), run_time=T(0.80))
        self.play(Create(ph), ph_lab.animate.set_opacity(1), Create(line_earth), run_time=T(0.80))
        self.play(Create(side), pr_lab.animate.set_opacity(1), run_time=T(0.80))
        self.wait(T(1.25))
        self.fixed_fade_out(planes_cue, run_time=0.22)

        # 3 · FRONT
        cue_f = self.section_chip("3 · FRONT → ALZADO", 3.65)
        self.fixed_fade_in(cue_f, run_time=0.40)
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
        self.play(LaggedStart(*[Create(r) for r in front_rays], lag_ratio=0.055), run_time=T(1.45))
        self.play(Create(front), run_time=T(1.00))
        self.play(Indicate(front, color=FRONT_COLOR, scale_factor=1.015), run_time=T(0.80))
        self.wait(T(1.45))
        self.play(FadeOut(front_rays), run_time=T(0.55))
        self.fixed_fade_out(cue_f, run_time=0.22)

        # 4 · TOP
        cue_t = self.section_chip("4 · TOP → PLANTA", 3.60)
        self.fixed_fade_in(cue_t, run_time=0.40)
        top_sources = [
            [-2.30,0.75,1.05], [2.30,0.75,1.05], [2.30,3.05,1.05], [-2.30,3.05,1.05],
            [-1.70,1.00,1.85], [0.85,1.00,1.85], [0.85,2.72,1.85], [-1.70,2.72,1.85],
            [-1.25,1.28,2.75], [-0.15,1.28,2.75], [-0.15,2.34,2.75], [-1.25,2.34,2.75],
        ]
        top_rays = VGroup(*[
            self.projector(p, [p[0], p[1], 0.025], TOP_COLOR) for p in top_sources
        ])
        top = self.top_outline()
        self.play(LaggedStart(*[Create(r) for r in top_rays], lag_ratio=0.045), run_time=T(1.55))
        self.play(Create(top), run_time=T(1.00))
        self.play(Indicate(top, color=TOP_COLOR, scale_factor=1.012), run_time=T(0.80))
        self.wait(T(1.45))
        self.play(FadeOut(top_rays), run_time=T(0.55))
        self.fixed_fade_out(cue_t, run_time=0.22)

        # 5 · RIGHT
        cue_r = self.section_chip("5 · RIGHT → PERFIL", 3.80)
        self.fixed_fade_in(cue_r, run_time=0.40)
        right_sources = [
            [2.30,0.75,0.35], [2.30,3.05,0.35], [2.30,3.05,1.05], [2.30,0.75,1.05],
            [0.85,1.00,1.85], [0.85,2.72,1.85],
            [-0.15,1.28,2.75], [-0.15,2.34,2.75],
        ]
        right_rays = VGroup(*[
            self.projector(p, [SIDE_X, p[1], p[2]], RIGHT_COLOR) for p in right_sources
        ])
        right = self.right_outline(SIDE_X)
        self.play(LaggedStart(*[Create(r) for r in right_rays], lag_ratio=0.06), run_time=T(1.45))
        self.play(Create(right), run_time=T(1.00))
        self.play(Indicate(right, color=RIGHT_COLOR, scale_factor=1.012), run_time=T(0.80))
        self.wait(T(1.45))
        self.play(FadeOut(right_rays), run_time=T(0.55))
        self.fixed_fade_out(cue_r, run_time=0.22)

        # Hold the complete physical construction.
        complete = self.section_chip("MISMO OBJETO 3D → TRES PROYECCIONES 2D", 6.10)
        self.fixed_fade_in(complete, run_time=0.40)
        self.move_camera(theta=-61 * DEGREES, phi=61 * DEGREES, zoom=0.95, frame_center=np.array([0.0,1.70,1.45]), run_time=T(1.35))
        self.move_camera(theta=-48 * DEGREES, phi=65 * DEGREES, zoom=0.98, frame_center=np.array([0.0,1.70,1.45]), run_time=T(1.25))
        self.wait(T(1.55))
        self.fixed_fade_out(complete, run_time=0.22)

        # 6 · Remove source body, projections remain.
        keep = self.section_chip("6 · RETIRAMOS EL OBJETO · LAS VISTAS PERMANECEN", 6.45)
        self.fixed_fade_in(keep, run_time=0.40)
        self.play(FadeOut(solid), run_time=T(0.95))
        self.wait(T(1.10))
        self.fixed_fade_out(keep, run_time=0.22)

        # Right plane is not part of the PV–PH Monge fold demonstration.
        self.play(FadeOut(side), FadeOut(right), pr_lab.animate.set_opacity(0), run_time=T(0.65))

        # 7 · Literal abatimiento.
        unfold = self.section_chip("7 · ABATIMIENTO · PH GIRA 90° SOBRE LT", 5.55)
        self.fixed_fade_in(unfold, run_time=0.40)
        self.play(
            Rotate(
                VGroup(ph, top),
                angle=-PI / 2,
                axis=RIGHT,
                about_point=ORIGIN,
                rate_func=smooth,
            ),
            run_time=T(3.00),
        )
        self.wait(T(1.10))
        self.move_camera(
            phi=90 * DEGREES, theta=90 * DEGREES, gamma=0,
            zoom=1.10, frame_center=np.array([0.0, 0.0, 0.05]),
            run_time=T(1.80),
        )
        self.wait(T(1.20))
        self.fixed_fade_out(unfold, run_time=0.22)

        # 8 · Alignment guides.
        align = self.section_chip("8 · LAS MEDIDAS COMUNES QUEDAN ALINEADAS", 5.65)
        self.fixed_fade_in(align, run_time=0.40)
        guides = VGroup(*[
            Line(
                np.array([x, 0.03, 3.00]), np.array([x, 0.03, -3.00]),
                stroke_color=GRID, stroke_width=1.6, stroke_opacity=0.78,
            )
            for x in (-2.30, -1.70, -1.25, -0.15, 0.85, 2.30)
        ])
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.08), run_time=T(1.20))
        self.wait(T(1.65))
        self.play(FadeOut(guides), run_time=T(0.45))
        self.fixed_fade_out(align, run_time=0.22)

        # Clear the 3D construction.
        self.play(
            FadeOut(pv), FadeOut(ph), FadeOut(line_earth), FadeOut(front), FadeOut(top),
            pv_lab.animate.set_opacity(0), ph_lab.animate.set_opacity(0),
            run_time=T(0.80),
        )

        # 9 · Large clean drawing sheet, no tiny axonometric thumbnail.
        sheet_title = Text("UN OBJETO · TRES DESCRIPCIONES 2D", font_size=34, color=INK, weight=BOLD)
        sheet_title.to_edge(UP, buff=0.35)

        f_panel = self.view_panel(self.front_view_2d(0.90), "FRONT / ALZADO", FRONT_COLOR, 5.35, 3.05)
        t_panel = self.view_panel(self.top_view_2d(0.82), "TOP / PLANTA", TOP_COLOR, 5.35, 2.70)
        r_panel = self.view_panel(self.right_view_2d(0.95), "RIGHT / PERFIL", RIGHT_COLOR, 3.25, 3.05)

        f_panel.move_to(np.array([-1.55, -1.35, 0]))
        t_panel.move_to(np.array([-1.55, 2.00, 0]))
        r_panel.move_to(np.array([4.10, -1.35, 0]))

        # faint alignment cues between top/front and front/right
        vguide = DashedLine(UP * 0.55, DOWN * 0.55, dash_length=0.08, color=GRID, stroke_width=1.6)
        vguide.move_to(np.array([-1.55, 0.30, 0]))
        hguide = DashedLine(LEFT * 0.70, RIGHT * 0.70, dash_length=0.08, color=GRID, stroke_width=1.6)
        hguide.move_to(np.array([1.25, -1.35, 0]))

        sheet_group = VGroup(sheet_title, f_panel, t_panel, r_panel, vguide, hguide)
        self.add_fixed_in_frame_mobjects(sheet_group)
        for m in (sheet_title, f_panel, t_panel, r_panel, vguide, hguide):
            m.set_opacity(0)

        self.play(sheet_title.animate.set_opacity(1), run_time=T(0.50))
        self.play(t_panel.animate.set_opacity(1), run_time=T(0.75))
        self.play(vguide.animate.set_opacity(1), f_panel.animate.set_opacity(1), run_time=T(0.85))
        self.play(hguide.animate.set_opacity(1), r_panel.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(2.20))

        self.play(sheet_group.animate.set_opacity(0), run_time=T(0.65))
        self.remove_fixed_in_frame_mobjects(sheet_group)

        # 10 · Large readable five-step method. Reveal, do not dark-fill.
        method_title = Text("MÉTODO PARA PASAR DE 3D A 2D", font_size=34, color=INK, weight=BOLD)
        bars = VGroup(
            self.method_bar(1, "ELIGE LA DIRECCIÓN", "frontal · superior · lateral"),
            self.method_bar(2, "COLOCA EL PLANO", "perpendicular a la dirección de observación"),
            self.method_bar(3, "PROYECTA LOS PUNTOS", "usa líneas paralelas y ortogonales al plano"),
            self.method_bar(4, "TRAZA LA VISTA", "une las aristas visibles con la geometría correcta"),
            self.method_bar(5, "ALINEA LAS VISTAS", "conserva las dimensiones comunes entre proyecciones"),
        ).arrange(DOWN, buff=0.16)
        method = VGroup(method_title, bars).arrange(DOWN, buff=0.38)
        method.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(method)
        method.set_opacity(0)
        self.play(method_title.animate.set_opacity(1), run_time=T(0.50))
        for bar in bars:
            bar.set_opacity(0)
        for bar in bars:
            self.play(bar.animate.set_opacity(1), run_time=T(0.42))
            self.play(Circumscribe(bar[0], color=FRONT_COLOR, buff=0.04, time_width=0.35), run_time=T(0.60))
            self.wait(T(0.38))
        self.wait(T(1.45))
        self.play(method.animate.set_opacity(0), run_time=T(0.60))
        self.remove_fixed_in_frame_mobjects(method)

        # 11 · Closing statement, large and sparse on purpose.
        close1 = Text("OBJETO 3D", font_size=48, color=INK, weight=BOLD)
        arr1 = Arrow(LEFT * 0.72, RIGHT * 0.72, buff=0, color=INK, stroke_width=3.0)
        close2 = Text("PROYECCIÓN ORTOGONAL", font_size=34, color=INK, weight=BOLD)
        arr2 = Arrow(LEFT * 0.72, RIGHT * 0.72, buff=0, color=INK, stroke_width=3.0)
        close3 = Text("VISTAS 2D", font_size=48, color=INK, weight=BOLD)
        synthesis = VGroup(close1, arr1, close2, arr2, close3).arrange(RIGHT, buff=0.35)
        synthesis.scale_to_fit_width(13.7)
        note = Text(
            "Cada vista conserva la forma que el objeto proyecta desde una dirección definida.",
            font_size=25, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.55)
        final = VGroup(synthesis, note)
        self.add_fixed_in_frame_mobjects(final)
        final.set_opacity(0)
        self.play(final.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(3.00))
        self.play(final.animate.set_opacity(0), run_time=T(0.70))
        self.remove_fixed_in_frame_mobjects(final)


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA.py Projection3Dto2DSeniorV7 --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA.py Projection3Dto2DSeniorV7 --disable_caching
