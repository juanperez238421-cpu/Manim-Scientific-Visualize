#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V6 FULL TOTAL · del objeto 3D a las vistas 2D.

Concept-first ManimCE lesson derived from the validated Class 6 / Sistema
Diédrico stack.  The purpose is not to imitate a PowerPoint slide deck; it is
to make the geometric operation physically visible:

1. One coherent asymmetric 3D object.
2. Real perpendicular projection planes PV / PH and a lateral plane.
3. Parallel orthographic projectors normal to the receiving plane.
4. FRONT / ALZADO, TOP / PLANTA and RIGHT / PERFIL generated from the SAME
   object coordinates.
5. Literal 90° abatimiento of PH about LT.
6. Final 2D drawing-sheet arrangement plus a reproducible five-step method.

The scene intentionally keeps formulas out of the main narrative.  Students
should understand the geometry before formal conventions ISO A / ISO E.

Base geometry and visual grammar reuse the validated V5 Monge scene.
Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps, literal -pqh.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

from Dibujo_Tecnico_Sistema_Diedrico_Monge_V5_SENIOR_FAITHFUL import (
    DihedralSystemMongeSeniorV5,
    INK,
    MUTED,
    GRID,
    PV_COLOR,
    PH_COLOR,
    FRONT_COLOR,
    TOP_COLOR,
    T,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

RIGHT_COLOR = "#5D7462"
PAPER = "#FAFAFA"
SOFT = "#F2F2F2"
TIME_SCALE = max(0.03, float(os.getenv("LESSON_TIME_SCALE", "1.0")))


class Projection3Dto2DFullTotalV6(DihedralSystemMongeSeniorV5):
    """Full conceptual class: physically derive 2D views from one 3D object."""

    # ------------------------------------------------------------------
    # 3D geometry additions
    # ------------------------------------------------------------------
    def right_outline(self, x=1.72):
        """Right orthographic silhouette in the y-z plane.

        The coordinates are derived from the same V5 stepped solid:
        base y=[0.55,1.95], z=[0.45,1.15]
        upper y=[0.72,1.48], z=[1.15,2.00]
        """
        pts = [
            [x, 0.55, 0.45], [x, 1.95, 0.45],
            [x, 1.95, 1.15], [x, 1.48, 1.15],
            [x, 1.48, 2.00], [x, 0.72, 2.00],
            [x, 0.72, 1.15], [x, 0.55, 1.15],
        ]
        return Polygon(
            *[np.array(p, dtype=float) for p in pts],
            stroke_color=RIGHT_COLOR,
            stroke_width=4.0,
            fill_opacity=0,
        )

    def plane_label_3d(self, text, position, color=INK, size=19):
        lab = Text(text, font_size=size, color=color, weight=BOLD).move_to(position)
        self.add_fixed_orientation_mobjects(lab)
        return lab

    # ------------------------------------------------------------------
    # Screen-space 2D view helpers for the final drawing sheet
    # ------------------------------------------------------------------
    def front_view_2d(self, scale=1.0):
        pts = [
            (-1.45, -0.775), (1.45, -0.775),
            (1.45, -0.075), (0.10, -0.075),
            (0.10, 0.775), (-1.15, 0.775),
            (-1.15, -0.075), (-1.45, -0.075),
        ]
        return Polygon(
            *[np.array([x, y, 0.0]) * scale for x, y in pts],
            stroke_color=FRONT_COLOR, stroke_width=3.4,
            fill_color=WHITE, fill_opacity=1.0,
        )

    def top_view_2d(self, scale=1.0):
        outer = Rectangle(
            width=2.90 * scale, height=1.40 * scale,
            stroke_color=TOP_COLOR, stroke_width=3.4,
            fill_color=WHITE, fill_opacity=1.0,
        )
        inner = Rectangle(
            width=1.25 * scale, height=0.76 * scale,
            stroke_color=TOP_COLOR, stroke_width=2.5,
            fill_opacity=0,
        )
        # Offset matches the actual upper-block position in plan.
        inner.move_to(
            outer.get_center()
            + LEFT * (0.525 * scale)
            + DOWN * (0.15 * scale)
        )
        return VGroup(outer, inner)

    def right_view_2d(self, scale=1.0):
        pts = [
            (-0.70, -0.775), (0.70, -0.775),
            (0.70, -0.075), (0.23, -0.075),
            (0.23, 0.775), (-0.53, 0.775),
            (-0.53, -0.075), (-0.70, -0.075),
        ]
        return Polygon(
            *[np.array([x, y, 0.0]) * scale for x, y in pts],
            stroke_color=RIGHT_COLOR, stroke_width=3.4,
            fill_color=WHITE, fill_opacity=1.0,
        )

    def view_card(self, view, title, color, width=3.35, height=2.35):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=GRID, stroke_width=1.5,
            fill_color=PAPER, fill_opacity=1.0,
        )
        if view.width > width - 0.48:
            view.scale_to_fit_width(width - 0.48)
        if view.height > height - 0.66:
            view.scale_to_fit_height(height - 0.66)
        view.move_to(box.get_center() + UP * 0.10)
        lab = Text(title, font_size=20, color=color, weight=BOLD)
        lab.next_to(box, DOWN, buff=0.10)
        return VGroup(box, view, lab)

    def step_card(self, number, title, detail, width=4.15):
        box = RoundedRectangle(
            width=width, height=1.20, corner_radius=0.11,
            stroke_color=GRID, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=1.0,
        )
        n = Text(str(number), font_size=25, color=INK, weight=BOLD)
        circ = Circle(radius=0.23, stroke_color=INK, stroke_width=1.7)
        badge = VGroup(circ, n).move_to(box.get_left() + RIGHT * 0.43)
        n.scale_to_fit_height(0.25)
        n.move_to(circ)
        t = Text(title, font_size=21, color=INK, weight=BOLD)
        d = Text(detail, font_size=16, color=MUTED)
        text = VGroup(t, d).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        if text.width > width - 1.15:
            text.scale_to_fit_width(width - 1.15)
        text.move_to(box.get_center() + RIGHT * 0.35)
        text.align_to(box, LEFT).shift(RIGHT * 0.92)
        return VGroup(box, badge, text)

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------
    def construct(self):
        self.set_camera_orientation(
            phi=66 * DEGREES,
            theta=-48 * DEGREES,
            gamma=0,
            zoom=0.79,
        )

        title = Text(
            "OBJETO 3D → VISTAS 2D",
            font_size=39, color=INK, weight=BOLD,
        ).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Sistema diédrico: observar · proyectar perpendicularmente · conservar la forma visible",
            font_size=20, color=MUTED,
        ).next_to(title, DOWN, buff=0.09)
        self.fixed_fade_in(title, subtitle, run_time=0.75)

        # ------------------------------------------------------------------
        # 0 · Start with the real 3D object
        # ------------------------------------------------------------------
        intro = self.chip("0 · UN SOLO OBJETO · MUCHAS DIRECCIONES DE OBSERVACIÓN", 6.40, 20)
        intro.to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(intro, run_time=0.45)

        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.08), run_time=T(1.15))

        # A short camera orbit makes the volume unmistakably three-dimensional.
        self.move_camera(theta=-64 * DEGREES, phi=61 * DEGREES, zoom=0.82, run_time=T(1.35))
        self.move_camera(theta=-35 * DEGREES, phi=70 * DEGREES, zoom=0.79, run_time=T(1.35))
        self.move_camera(theta=-48 * DEGREES, phi=66 * DEGREES, zoom=0.79, run_time=T(1.20))
        self.wait(T(0.75))
        self.fixed_fade_out(intro, run_time=0.22)

        # ------------------------------------------------------------------
        # 1 · Build the real projection planes around the SAME object
        # ------------------------------------------------------------------
        step1 = self.chip("1 · COLOCAMOS PLANOS DE PROYECCIÓN", 4.85, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(step1, run_time=0.40)

        PLANE_W = 6.45
        PV_H = 2.72
        PH_D = 2.55

        pv = Rectangle(
            width=PLANE_W, height=PV_H,
            stroke_color=PV_COLOR, stroke_width=1.7,
            fill_color=PV_COLOR, fill_opacity=0.12,
        )
        pv.rotate(PI / 2, axis=RIGHT)
        pv.shift(OUT * (PV_H / 2))

        ph = Rectangle(
            width=PLANE_W, height=PH_D,
            stroke_color=PH_COLOR, stroke_width=1.7,
            fill_color=PH_COLOR, fill_opacity=0.12,
        )
        ph.shift(UP * (PH_D / 2))

        side_plane = Rectangle(
            width=2.70, height=2.75,
            stroke_color=RIGHT_COLOR, stroke_width=1.7,
            fill_color=RIGHT_COLOR, fill_opacity=0.10,
        )
        side_plane.rotate(PI / 2, axis=UP)
        side_plane.move_to(np.array([1.72, 1.25, 1.24]))

        lt = Line(LEFT * (PLANE_W / 2), RIGHT * (PLANE_W / 2), color=INK, stroke_width=3.0)

        pv_lab = self.plane_label_3d("PV · FRONT", np.array([-2.25, 0.02, 2.45]), PV_COLOR)
        ph_lab = self.plane_label_3d("PH · TOP", np.array([-2.15, 2.20, 0.08]), TOP_COLOR)
        pp_lab = self.plane_label_3d("PL · RIGHT", np.array([1.76, 2.16, 2.35]), RIGHT_COLOR)
        for lab in (pv_lab, ph_lab, pp_lab):
            lab.set_opacity(0)

        self.play(Create(pv), Create(ph), Create(lt), run_time=T(1.15))
        self.play(Create(side_plane), run_time=T(0.80))
        self.play(
            pv_lab.animate.set_opacity(1),
            ph_lab.animate.set_opacity(1),
            pp_lab.animate.set_opacity(1),
            run_time=T(0.55),
        )
        self.wait(T(0.75))
        self.fixed_fade_out(step1, run_time=0.22)

        # ------------------------------------------------------------------
        # 2 · FRONT / ALZADO
        # ------------------------------------------------------------------
        front_cue = self.chip("2 · MIRADA FRONTAL → ALZADO", 4.35, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(front_cue, run_time=0.38)

        front_sources = [
            [-1.45, 0.55, 0.45], [1.45, 0.55, 0.45],
            [1.45, 0.55, 1.15], [-1.45, 0.55, 1.15],
            [-1.15, 0.72, 2.00], [0.10, 0.72, 2.00],
        ]
        front_rays = VGroup(*[
            self.projector(p, [p[0], 0.018, p[2]], FRONT_COLOR)
            for p in front_sources
        ])
        front = self.front_outline()
        normal_front = Arrow3D(
            start=np.array([2.60, 1.95, 1.55]),
            end=np.array([2.60, 0.25, 1.55]),
            color=FRONT_COLOR,
            thickness=0.018,
            height=0.22,
            base_radius=0.07,
        )
        self.play(FadeIn(normal_front), run_time=T(0.45))
        self.play(LaggedStart(*[Create(r) for r in front_rays], lag_ratio=0.07), run_time=T(1.15))
        self.play(Create(front), run_time=T(0.95))
        self.wait(T(0.75))
        self.play(FadeOut(front_rays), FadeOut(normal_front), run_time=T(0.45))
        self.fixed_fade_out(front_cue, run_time=0.22)

        # ------------------------------------------------------------------
        # 3 · TOP / PLANTA
        # ------------------------------------------------------------------
        top_cue = self.chip("3 · MIRADA SUPERIOR → PLANTA", 4.35, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(top_cue, run_time=0.38)

        top_sources = [
            [-1.45, 0.55, 1.15], [1.45, 0.55, 1.15],
            [1.45, 1.95, 1.15], [-1.45, 1.95, 1.15],
            [-1.15, 0.72, 2.00], [0.10, 0.72, 2.00],
            [0.10, 1.48, 2.00], [-1.15, 1.48, 2.00],
        ]
        top_rays = VGroup(*[
            self.projector(p, [p[0], p[1], 0.018], TOP_COLOR)
            for p in top_sources
        ])
        top = self.top_outline()
        normal_top = Arrow3D(
            start=np.array([2.20, 1.60, 2.55]),
            end=np.array([2.20, 1.60, 0.30]),
            color=TOP_COLOR,
            thickness=0.018,
            height=0.22,
            base_radius=0.07,
        )
        self.play(FadeIn(normal_top), run_time=T(0.45))
        self.play(LaggedStart(*[Create(r) for r in top_rays], lag_ratio=0.05), run_time=T(1.20))
        self.play(Create(top), run_time=T(0.95))
        self.wait(T(0.75))
        self.play(FadeOut(top_rays), FadeOut(normal_top), run_time=T(0.45))
        self.fixed_fade_out(top_cue, run_time=0.22)

        # ------------------------------------------------------------------
        # 4 · RIGHT / PERFIL
        # ------------------------------------------------------------------
        right_cue = self.chip("4 · MIRADA DERECHA → PERFIL", 4.45, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(right_cue, run_time=0.38)

        right_sources = [
            [1.45, 0.55, 0.45], [1.45, 1.95, 0.45],
            [1.45, 1.95, 1.15], [1.45, 0.55, 1.15],
            [0.10, 0.72, 2.00], [0.10, 1.48, 2.00],
        ]
        right_rays = VGroup(*[
            self.projector(p, [1.72, p[1], p[2]], RIGHT_COLOR)
            for p in right_sources
        ])
        right = self.right_outline()
        normal_right = Arrow3D(
            start=np.array([-0.20, 2.25, 1.65]),
            end=np.array([1.55, 2.25, 1.65]),
            color=RIGHT_COLOR,
            thickness=0.018,
            height=0.22,
            base_radius=0.07,
        )
        self.play(FadeIn(normal_right), run_time=T(0.45))
        self.play(LaggedStart(*[Create(r) for r in right_rays], lag_ratio=0.07), run_time=T(1.10))
        self.play(Create(right), run_time=T(0.95))
        self.wait(T(0.75))
        self.play(FadeOut(right_rays), FadeOut(normal_right), run_time=T(0.45))
        self.fixed_fade_out(right_cue, run_time=0.22)

        # ------------------------------------------------------------------
        # 5 · Remove the object: the projections remain
        # ------------------------------------------------------------------
        keep = self.chip("5 · EL OBJETO DESAPARECE · LAS PROYECCIONES PERMANECEN", 6.50, 20)
        keep.to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(keep, run_time=0.42)
        self.play(FadeOut(solid), run_time=T(0.75))
        self.wait(T(0.75))
        self.fixed_fade_out(keep, run_time=0.22)

        # The right plane was only needed to derive the side profile.  Keep the
        # profile conceptually, but clear this plane before the dihedral fold so
        # students focus on the PV–PH hinge relationship.
        self.play(
            FadeOut(side_plane), FadeOut(right),
            pp_lab.animate.set_opacity(0),
            run_time=T(0.60),
        )

        # ------------------------------------------------------------------
        # 6 · Literal dihedral unfolding
        # ------------------------------------------------------------------
        unfold = self.chip("6 · ABATIMIENTO: PH GIRA 90° SOBRE LT", 5.15, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(unfold, run_time=0.40)
        ph_and_top = VGroup(ph, top)
        self.play(
            Rotate(
                ph_and_top,
                angle=-PI / 2,
                axis=RIGHT,
                about_point=ORIGIN,
                rate_func=smooth,
            ),
            run_time=T(2.60),
        )
        self.wait(T(0.65))

        self.move_camera(
            phi=90 * DEGREES,
            theta=90 * DEGREES,
            gamma=0,
            zoom=0.80,
            run_time=T(1.60),
        )
        self.fixed_fade_out(unfold, run_time=0.22)

        # Reference lines make the correspondence between the two 2D views
        # explicit without using equations.
        align_cue = self.chip("MISMAS x → PUNTOS ALINEADOS ENTRE ALZADO Y PLANTA", 6.35, 19)
        align_cue.to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(align_cue, run_time=0.40)
        refs = VGroup(*[
            Line(
                np.array([x, 0.035, 2.15]),
                np.array([x, 0.035, -2.05]),
                stroke_color=GRID,
                stroke_width=1.2,
                stroke_opacity=0.72,
            )
            for x in (-1.45, -1.15, 0.10, 1.45)
        ])
        self.play(LaggedStart(*[Create(r) for r in refs], lag_ratio=0.11), run_time=T(1.00))
        self.wait(T(1.20))
        self.play(FadeOut(refs), run_time=T(0.40))
        self.fixed_fade_out(align_cue, run_time=0.22)

        # ------------------------------------------------------------------
        # 7 · Transition from the physical construction to the clean sheet
        # ------------------------------------------------------------------
        sheet_cue = self.chip("7 · AHORA YA PODEMOS DIBUJAR LAS VISTAS EN 2D", 6.10, 20)
        sheet_cue.to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(sheet_cue, run_time=0.42)
        self.play(
            FadeOut(pv), FadeOut(ph), FadeOut(lt), FadeOut(front), FadeOut(top),
            pv_lab.animate.set_opacity(0), ph_lab.animate.set_opacity(0),
            run_time=T(0.75),
        )
        self.wait(T(0.40))
        self.fixed_fade_out(sheet_cue, run_time=0.22)

        # Screen-space drawing sheet: these are exact 2D views of the same model.
        f_card = self.view_card(self.front_view_2d(0.72), "FRONT / ALZADO", FRONT_COLOR)
        t_card = self.view_card(self.top_view_2d(0.72), "TOP / PLANTA", TOP_COLOR)
        r_card = self.view_card(self.right_view_2d(0.72), "RIGHT / PERFIL", RIGHT_COLOR)

        f_card.move_to(DOWN * 0.35)
        t_card.move_to(UP * 2.55)
        r_card.move_to(RIGHT * 4.15 + DOWN * 0.35)

        # Include a compact axonometric reminder so students never lose the
        # one-object / multiple-view relationship.
        mini_solid = self.make_solid().scale(0.62)
        mini_solid.move_to(LEFT * 4.55 + DOWN * 0.15)
        reminder = self.chip("MISMO OBJETO 3D", 3.35, 18).move_to(LEFT * 4.55 + DOWN * 2.55)

        self.add_fixed_in_frame_mobjects(f_card, t_card, r_card, reminder)
        f_card.set_opacity(0); t_card.set_opacity(0); r_card.set_opacity(0); reminder.set_opacity(0)
        self.play(FadeIn(mini_solid), reminder.animate.set_opacity(1), run_time=T(0.70))
        self.play(f_card.animate.set_opacity(1), run_time=T(0.75))
        self.play(t_card.animate.set_opacity(1), run_time=T(0.75))
        self.play(r_card.animate.set_opacity(1), run_time=T(0.75))
        self.wait(T(2.10))

        # ------------------------------------------------------------------
        # 8 · Reproducible method
        # ------------------------------------------------------------------
        self.play(
            FadeOut(mini_solid),
            f_card.animate.set_opacity(0),
            t_card.animate.set_opacity(0),
            r_card.animate.set_opacity(0),
            reminder.animate.set_opacity(0),
            run_time=T(0.65),
        )
        for mob in (f_card, t_card, r_card, reminder):
            self.remove_fixed_in_frame_mobjects(mob)

        method_title = Text(
            "MÉTODO PARA PASAR DE 3D A 2D",
            font_size=30, color=INK, weight=BOLD,
        ).move_to(UP * 2.70)
        cards = VGroup(
            self.step_card(1, "ELIGE LA DIRECCIÓN", "frontal, superior o lateral"),
            self.step_card(2, "IMAGINA EL PLANO", "perpendicular a tu mirada"),
            self.step_card(3, "PROYECTA LOS PUNTOS", "líneas paralelas y ortogonales"),
            self.step_card(4, "TRAZA LA SILUETA", "conserva la geometría visible"),
            self.step_card(5, "ALINEA LAS VISTAS", "las medidas comunes deben coincidir"),
        )
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.34, 0.32))
        cards.move_to(DOWN * 0.55)
        method = VGroup(method_title, cards)
        self.add_fixed_in_frame_mobjects(method)
        method.set_opacity(0)
        self.play(method.animate.set_opacity(1), run_time=T(0.65))
        self.play(
            LaggedStart(*[Indicate(c[0], color=INK, scale_factor=1.02) for c in cards], lag_ratio=0.18),
            run_time=T(2.60),
        )
        self.wait(T(2.20))

        # ------------------------------------------------------------------
        # Closing synthesis
        # ------------------------------------------------------------------
        self.play(method.animate.set_opacity(0), run_time=T(0.55))
        self.remove_fixed_in_frame_mobjects(method)

        synthesis = VGroup(
            Text("3D", font_size=46, color=INK, weight=BOLD),
            Arrow(LEFT * 0.65, RIGHT * 0.65, buff=0, color=INK, stroke_width=2.6),
            Text("PROYECCIÓN ORTOGONAL", font_size=31, color=INK, weight=BOLD),
            Arrow(LEFT * 0.65, RIGHT * 0.65, buff=0, color=INK, stroke_width=2.6),
            Text("VISTA 2D", font_size=46, color=INK, weight=BOLD),
        ).arrange(RIGHT, buff=0.36)
        if synthesis.width > 13.5:
            synthesis.scale_to_fit_width(13.5)
        synthesis.move_to(UP * 0.30)
        final_note = Text(
            "La vista 2D no es una fotografía: es la proyección geométrica del objeto desde una dirección definida.",
            font_size=23, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.55)
        final_note.scale_to_fit_width(12.8)
        final_group = VGroup(synthesis, final_note)
        self.add_fixed_in_frame_mobjects(final_group)
        final_group.set_opacity(0)
        self.play(final_group.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(3.20))

        self.play(
            final_group.animate.set_opacity(0),
            title.animate.set_opacity(0),
            subtitle.animate.set_opacity(0),
            run_time=T(0.75),
        )
        self.remove_fixed_in_frame_mobjects(final_group, title, subtitle)


# Preview:
#   manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V6_FULL_TOTAL.py Projection3Dto2DFullTotalV6 --disable_caching
# Final:
#   manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V6_FULL_TOTAL.py Projection3Dto2DFullTotalV6 --disable_caching
