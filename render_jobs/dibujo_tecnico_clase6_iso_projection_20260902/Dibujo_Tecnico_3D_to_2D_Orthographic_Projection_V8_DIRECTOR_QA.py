#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V8 DIRECTOR QA · objeto 3D → vistas 2D.

Full directing pass over V7. The geometry and pedagogical sequence are preserved,
but framing, pauses, transitions, transforms and final 2D composition are rebuilt.
Target: ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA import (
    Projection3Dto2DSeniorV7,
    INK, MUTED, GRID,
    PV_COLOR, PH_COLOR, FRONT_COLOR, TOP_COLOR,
    RIGHT_COLOR, PAPER, SOFT, T,
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE


class Projection3Dto2DDirectorV8(Projection3Dto2DSeniorV7):
    """Same V7 concept, directed as a slower classroom animation."""

    # ------------------------------------------------------------------
    # Fixed-frame UI
    # ------------------------------------------------------------------
    def stage_header(self, number, text, accent=INK, width=13.6):
        box = RoundedRectangle(
            width=width, height=0.82, corner_radius=0.12,
            stroke_color=GRID, stroke_width=1.4,
            fill_color=WHITE, fill_opacity=0.96,
        )
        badge = Circle(
            radius=0.25, stroke_color=accent, stroke_width=2.2,
            fill_color=WHITE, fill_opacity=1,
        )
        n = Text(str(number), font_size=22, color=accent, weight=BOLD).move_to(badge)
        title = Text(text, font_size=27, color=INK, weight=BOLD)
        if title.width > width - 1.35:
            title.scale_to_fit_width(width - 1.35)
        badge.move_to(box.get_left() + RIGHT * 0.48)
        n.move_to(badge)
        title.align_to(box, LEFT).shift(RIGHT * 0.95)
        title.set_y(box.get_y())
        g = VGroup(box, badge, n, title).to_edge(UP, buff=0.18)
        return g

    def show_header(self, new, old=None, rt=0.65):
        self.add_fixed_in_frame_mobjects(new)
        if old is None:
            new.set_opacity(0)
            self.play(new.animate.set_opacity(1), run_time=T(rt))
        else:
            self.play(FadeTransform(old, new), run_time=T(rt))
            self.remove_fixed_in_frame_mobjects(old)
        return new

    def view_card(self, view, label, color, width=4.55, height=4.55):
        card = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=GRID, stroke_width=1.5,
            fill_color=PAPER, fill_opacity=1,
        )
        label_box = RoundedRectangle(
            width=width - 0.34, height=0.64, corner_radius=0.10,
            stroke_color=color, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        )
        label_m = Text(label, font_size=24, color=color, weight=BOLD).move_to(label_box)
        label_g = VGroup(label_box, label_m).move_to(card.get_bottom() + UP * 0.50)
        if view.width > width - 0.60:
            view.scale_to_fit_width(width - 0.60)
        if view.height > height - 1.25:
            view.scale_to_fit_height(height - 1.25)
        view.move_to(card.get_center() + UP * 0.38)
        return VGroup(card, view, label_g)

    def method_bar(self, number, title, detail, accent):
        box = RoundedRectangle(
            width=13.25, height=0.93, corner_radius=0.12,
            stroke_color=GRID, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=1,
        )
        badge = Circle(
            radius=0.26, stroke_color=accent, stroke_width=2,
            fill_color=SOFT, fill_opacity=1,
        )
        n = Text(str(number), font_size=22, color=INK, weight=BOLD).move_to(badge)
        t = Text(title, font_size=24, color=INK, weight=BOLD)
        d = Text(detail, font_size=20, color=MUTED)
        txt = VGroup(t, d).arrange(RIGHT, buff=0.34)
        if txt.width > 11.7:
            txt.scale_to_fit_width(11.7)
        badge.move_to(box.get_left() + RIGHT * 0.48)
        n.move_to(badge)
        txt.align_to(box, LEFT).shift(RIGHT * 0.98)
        txt.set_y(box.get_y())
        return VGroup(box, badge, n, txt)

    # ------------------------------------------------------------------
    # Projection helper: anchor rays → full rays → outline → pause
    # ------------------------------------------------------------------
    def build_projection(self, rays, outline, color, anchors):
        self.play(
            LaggedStart(*[Create(rays[i]) for i in anchors], lag_ratio=0.22),
            run_time=T(1.65),
        )
        self.wait(T(1.15))
        rest = [rays[i] for i in range(len(rays)) if i not in anchors]
        self.play(LaggedStart(*[Create(r) for r in rest], lag_ratio=0.07), run_time=T(2.10))
        self.wait(T(0.90))
        self.play(Create(outline), run_time=T(1.55))
        self.play(
            outline.animate.set_stroke(width=7.0, color=color),
            run_time=T(0.55),
        )
        self.play(
            outline.animate.set_stroke(width=5.0, color=color),
            run_time=T(0.55),
        )
        self.wait(T(2.35))
        self.play(FadeOut(rays), run_time=T(0.75))

    # ------------------------------------------------------------------
    # Main timeline
    # ------------------------------------------------------------------
    def construct(self):
        focus = np.array([0.0, 1.86, 1.50])
        self.set_camera_orientation(
            phi=64 * DEGREES, theta=-52 * DEGREES, gamma=0,
            zoom=1.42, frame_center=focus,
        )

        # 0 · Volume
        header = self.show_header(
            self.stage_header(0, "DE UN OBJETO 3D A SUS VISTAS 2D · RECONOCEMOS EL VOLUMEN", FRONT_COLOR)
        )
        subtitle = Text(
            "Primero entendemos el volumen. Después lo proyectamos.",
            font_size=25, color=MUTED,
        ).to_edge(DOWN, buff=0.32)
        self.add_fixed_in_frame_mobjects(subtitle)
        subtitle.set_opacity(0)
        self.play(subtitle.animate.set_opacity(1), run_time=T(0.65))

        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.16), run_time=T(1.35))
        self.wait(T(2.10))
        for theta, phi, zoom, rt, pause in [
            (-72, 60, 1.48, 2.40, 1.20),
            (-31, 70, 1.44, 2.55, 1.20),
            (-52, 64, 1.42, 2.35, 2.00),
        ]:
            self.move_camera(
                theta=theta * DEGREES, phi=phi * DEGREES,
                zoom=zoom, frame_center=focus, run_time=T(rt),
            )
            self.wait(T(pause))
        self.play(subtitle.animate.set_opacity(0), run_time=T(0.45))
        self.remove_fixed_in_frame_mobjects(subtitle)

        # 1 · Observation directions
        header = self.show_header(
            self.stage_header(1, "UN OBJETO · TRES DIRECCIONES DE OBSERVACIÓN", FRONT_COLOR), header
        )
        front_arrow = Arrow3D(
            start=np.array([0.15, 4.35, 1.55]), end=np.array([0.15, 3.28, 1.55]),
            color=FRONT_COLOR, thickness=0.032, height=0.30, base_radius=0.10,
        )
        top_arrow = Arrow3D(
            start=np.array([-0.30, 1.90, 4.08]), end=np.array([-0.30, 1.90, 2.98]),
            color=TOP_COLOR, thickness=0.032, height=0.30, base_radius=0.10,
        )
        right_arrow = Arrow3D(
            start=np.array([3.95, 1.80, 1.55]), end=np.array([2.72, 1.80, 1.55]),
            color=RIGHT_COLOR, thickness=0.032, height=0.30, base_radius=0.10,
        )
        lf = self.direction_label_3d("FRONT", np.array([0.15, 4.45, 1.88]), FRONT_COLOR)
        lt = self.direction_label_3d("TOP", np.array([-0.30, 1.95, 4.25]), TOP_COLOR)
        lr = self.direction_label_3d("RIGHT", np.array([4.03, 1.80, 1.88]), RIGHT_COLOR)
        for lab in (lf, lt, lr):
            lab.set_opacity(0)
        for arrow, lab in [(front_arrow, lf), (top_arrow, lt), (right_arrow, lr)]:
            self.play(FadeIn(arrow), lab.animate.set_opacity(1), run_time=T(0.85))
            self.wait(T(1.45))
        self.wait(T(0.75))

        # 2 · Planes
        header = self.show_header(
            self.stage_header(2, "CADA DIRECCIÓN NECESITA UN PLANO PERPENDICULAR", PV_COLOR), header
        )
        self.move_camera(zoom=1.22, frame_center=np.array([0.0, 1.74, 1.48]), run_time=T(1.35))
        PLANE_W, PV_H, PH_D, SIDE_X = 5.75, 3.30, 3.55, 2.58
        pv = Rectangle(
            width=PLANE_W, height=PV_H, stroke_color=PV_COLOR, stroke_width=2.1,
            fill_color=PV_COLOR, fill_opacity=0.085,
        ).rotate(PI / 2, axis=RIGHT).shift(OUT * (PV_H / 2))
        ph = Rectangle(
            width=PLANE_W, height=PH_D, stroke_color=PH_COLOR, stroke_width=2.1,
            fill_color=PH_COLOR, fill_opacity=0.085,
        ).shift(UP * (PH_D / 2))
        side = Rectangle(
            width=PH_D, height=PV_H, stroke_color=RIGHT_COLOR, stroke_width=2.1,
            fill_color=RIGHT_COLOR, fill_opacity=0.075,
        ).rotate(PI / 2, axis=UP).move_to(np.array([SIDE_X, PH_D / 2, PV_H / 2]))
        line_earth = Line(
            np.array([-PLANE_W / 2, 0, 0]), np.array([PLANE_W / 2, 0, 0]),
            color=INK, stroke_width=3.6,
        )
        pv_lab = self.plane_label_3d("PV · FRONT", np.array([-2.05, 0.04, 3.05]), PV_COLOR)
        ph_lab = self.plane_label_3d("PH · TOP", np.array([-2.05, 3.12, 0.08]), TOP_COLOR)
        pr_lab = self.plane_label_3d("PL · RIGHT", np.array([2.62, 3.15, 2.92]), RIGHT_COLOR)
        for lab in (pv_lab, ph_lab, pr_lab):
            lab.set_opacity(0)
        for arrow, old_lab, plane, new_lab, extra in [
            (front_arrow, lf, pv, pv_lab, None),
            (top_arrow, lt, ph, ph_lab, line_earth),
            (right_arrow, lr, side, pr_lab, None),
        ]:
            animations = [FadeTransform(arrow, plane), old_lab.animate.set_opacity(0), new_lab.animate.set_opacity(1)]
            if extra is not None:
                animations.append(Create(extra))
            self.play(*animations, run_time=T(1.15))
            self.wait(T(0.85))
        self.wait(T(1.35))

        # 3 · FRONT
        header = self.show_header(
            self.stage_header(3, "FRONT → ALZADO · LOS PUNTOS VIAJAN PERPENDICULARMENTE AL PV", FRONT_COLOR), header
        )
        fsrc = [
            [-2.30,0.75,0.35],[2.30,0.75,0.35],[2.30,0.75,1.05],
            [0.85,1.00,1.05],[0.85,1.00,1.85],[-0.15,1.28,1.85],
            [-0.15,1.28,2.75],[-1.25,1.28,2.75],[-1.70,1.00,1.85],[-2.30,0.75,1.05],
        ]
        frays = VGroup(*[self.projector(p, [p[0], 0.025, p[2]], FRONT_COLOR) for p in fsrc])
        front = self.front_outline()
        self.build_projection(frays, front, FRONT_COLOR, (0,2,6))

        # 4 · TOP
        header = self.show_header(
            self.stage_header(4, "TOP → PLANTA · CAMBIA LA DIRECCIÓN, NO EL OBJETO", TOP_COLOR), header
        )
        tsrc = [
            [-2.30,0.75,1.05],[2.30,0.75,1.05],[2.30,3.05,1.05],[-2.30,3.05,1.05],
            [-1.70,1.00,1.85],[0.85,1.00,1.85],[0.85,2.72,1.85],[-1.70,2.72,1.85],
            [-1.25,1.28,2.75],[-0.15,1.28,2.75],[-0.15,2.34,2.75],[-1.25,2.34,2.75],
        ]
        trays = VGroup(*[self.projector(p, [p[0], p[1], 0.025], TOP_COLOR) for p in tsrc])
        top = self.top_outline()
        self.build_projection(trays, top, TOP_COLOR, (0,2,8))

        # 5 · RIGHT
        header = self.show_header(
            self.stage_header(5, "RIGHT → PERFIL · LA PROFUNDIDAD SE CONVIERTE EN ANCHO DE LA VISTA", RIGHT_COLOR), header
        )
        rsrc = [
            [2.30,0.75,0.35],[2.30,3.05,0.35],[2.30,3.05,1.05],[2.30,0.75,1.05],
            [0.85,1.00,1.85],[0.85,2.72,1.85],[-0.15,1.28,2.75],[-0.15,2.34,2.75],
        ]
        rrays = VGroup(*[self.projector(p, [SIDE_X, p[1], p[2]], RIGHT_COLOR) for p in rsrc])
        right = self.right_outline(SIDE_X)
        self.build_projection(rrays, right, RIGHT_COLOR, (0,2,6))

        # 6 · Complete physical construction; then remove source body
        header = self.show_header(self.stage_header(6, "MISMO OBJETO 3D → TRES PROYECCIONES 2D", INK), header)
        self.move_camera(
            theta=-62 * DEGREES, phi=60 * DEGREES, zoom=1.17,
            frame_center=np.array([0.0,1.70,1.45]), run_time=T(2.00),
        )
        self.wait(T(1.30))
        self.move_camera(
            theta=-47 * DEGREES, phi=65 * DEGREES, zoom=1.20,
            frame_center=np.array([0.0,1.70,1.45]), run_time=T(1.85),
        )
        self.wait(T(2.60))
        self.play(solid.animate.set_opacity(0.30), run_time=T(1.20))
        self.wait(T(1.15))
        self.play(FadeOut(solid), run_time=T(1.10))
        self.wait(T(2.20))

        # 7 · Literal Monge fold, no edge-on camera move afterwards
        header = self.show_header(
            self.stage_header(7, "ABATIMIENTO · EL PH GIRA 90° ALREDEDOR DE LA LÍNEA DE TIERRA", TOP_COLOR), header
        )
        self.play(FadeOut(side), FadeOut(right), pr_lab.animate.set_opacity(0), run_time=T(0.95))
        self.play(Indicate(line_earth, color=INK, scale_factor=1.015), run_time=T(1.10))
        self.wait(T(1.45))
        self.play(
            Rotate(VGroup(ph, top), angle=-PI/2, axis=RIGHT, about_point=ORIGIN, rate_func=smooth),
            run_time=T(4.60),
        )
        self.wait(T(2.80))

        # 8 · Stable 2D bridge and alignment guides
        header = self.show_header(
            self.stage_header(8, "LAS VISTAS CONSERVAN DIMENSIONES COMUNES Y QUEDAN ALINEADAS", FRONT_COLOR), header
        )
        aligned_front = self.front_view_2d(1.10).move_to(UP * 1.28)
        aligned_top = self.top_view_2d(1.00).move_to(DOWN * 1.72)
        flab = Text("ALZADO", font_size=24, color=FRONT_COLOR, weight=BOLD).next_to(aligned_front, RIGHT, buff=0.45)
        tlab = Text("PLANTA", font_size=24, color=TOP_COLOR, weight=BOLD).next_to(aligned_top, RIGHT, buff=0.45)
        pair = VGroup(aligned_front, aligned_top, flab, tlab)
        self.add_fixed_in_frame_mobjects(pair)
        pair.set_opacity(0)
        self.play(
            FadeOut(pv), FadeOut(ph), FadeOut(line_earth), FadeOut(front), FadeOut(top),
            pv_lab.animate.set_opacity(0), ph_lab.animate.set_opacity(0),
            pair.animate.set_opacity(1), run_time=T(1.65),
        )
        self.wait(T(1.60))
        f_left, f_right = aligned_front.get_left()[0], aligned_front.get_right()[0]
        xs_model = (-2.30,-1.70,-1.25,-0.15,0.85,2.30)
        xs = [f_left + (x + 2.30) / 4.60 * (f_right - f_left) for x in xs_model]
        guides = VGroup(*[
            DashedLine(np.array([x,0.18,0]), np.array([x,-0.58,0]), dash_length=0.08, color=GRID, stroke_width=1.7)
            for x in xs
        ])
        self.add_fixed_in_frame_mobjects(guides)
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.12), run_time=T(1.65))
        self.wait(T(3.10))

        # 9 · Balanced three-card 2D sheet
        header = self.show_header(self.stage_header(9, "UN OBJETO · TRES DESCRIPCIONES 2D", INK), header)
        self.play(FadeOut(guides), run_time=T(0.65))
        self.remove_fixed_in_frame_mobjects(guides)
        fcard = self.view_card(self.front_view_2d(1.0), "FRONT / ALZADO", FRONT_COLOR)
        tcard = self.view_card(self.top_view_2d(1.0), "TOP / PLANTA", TOP_COLOR)
        rcard = self.view_card(self.right_view_2d(1.0), "RIGHT / PERFIL", RIGHT_COLOR)
        cards = VGroup(fcard, tcard, rcard).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.15)
        self.add_fixed_in_frame_mobjects(cards)
        for c in cards:
            c.set_opacity(0)
        self.play(pair.animate.set_opacity(0), fcard.animate.set_opacity(1), tcard.animate.set_opacity(1), run_time=T(1.10))
        self.remove_fixed_in_frame_mobjects(pair)
        self.play(rcard.animate.set_opacity(1), run_time=T(0.90))
        self.wait(T(1.40))
        for card, color in [(fcard, FRONT_COLOR),(tcard, TOP_COLOR),(rcard, RIGHT_COLOR)]:
            self.play(Circumscribe(card[0], color=color, buff=0.04), run_time=T(0.90))
            self.wait(T(1.00))
        self.wait(T(3.30))

        # 10 · Large, slow five-step method
        header = self.show_header(self.stage_header(10, "MÉTODO PARA PASAR DE 3D A 2D", INK), header)
        self.play(cards.animate.set_opacity(0), run_time=T(0.85))
        self.remove_fixed_in_frame_mobjects(cards)
        bars = VGroup(
            self.method_bar(1, "ELIGE LA DIRECCIÓN", "frontal · superior · lateral", FRONT_COLOR),
            self.method_bar(2, "COLOCA EL PLANO", "perpendicular a la dirección de observación", PV_COLOR),
            self.method_bar(3, "PROYECTA LOS PUNTOS", "usa líneas paralelas y ortogonales al plano", TOP_COLOR),
            self.method_bar(4, "TRAZA LA VISTA", "une las aristas visibles con la geometría correcta", RIGHT_COLOR),
            self.method_bar(5, "ALINEA LAS VISTAS", "conserva dimensiones comunes entre proyecciones", INK),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 0.20)
        self.add_fixed_in_frame_mobjects(bars)
        for bar in bars:
            bar.set_opacity(0)
        accents = (FRONT_COLOR, PV_COLOR, TOP_COLOR, RIGHT_COLOR, INK)
        for bar, accent in zip(bars, accents):
            self.play(bar.animate.set_opacity(1), run_time=T(0.60))
            self.play(Circumscribe(bar[0], color=accent, buff=0.035, time_width=0.45), run_time=T(0.90))
            self.wait(T(1.45))
        self.wait(T(3.20))

        # 11 · Closing synthesis: keep geometric context on screen
        header = self.show_header(
            self.stage_header(11, "IDEA CENTRAL · UNA PIEZA 3D PUEDE DESCRIBIRSE CON VISTAS 2D", FRONT_COLOR), header
        )
        self.play(bars.animate.set_opacity(0), run_time=T(0.90))
        self.remove_fixed_in_frame_mobjects(bars)
        mini_views = VGroup(
            self.front_view_2d(0.72), self.top_view_2d(0.72), self.right_view_2d(0.82)
        ).arrange(RIGHT, buff=1.10).move_to(UP * 1.45)
        close1 = Text("OBJETO 3D", font_size=46, color=INK, weight=BOLD)
        arr1 = Arrow(LEFT*0.72, RIGHT*0.72, buff=0, color=INK, stroke_width=3.2)
        close2 = Text("PROYECCIÓN ORTOGONAL", font_size=33, color=INK, weight=BOLD)
        arr2 = Arrow(LEFT*0.72, RIGHT*0.72, buff=0, color=INK, stroke_width=3.2)
        close3 = Text("VISTAS 2D", font_size=46, color=INK, weight=BOLD)
        synthesis = VGroup(close1, arr1, close2, arr2, close3).arrange(RIGHT, buff=0.34)
        synthesis.scale_to_fit_width(13.4).move_to(DOWN * 1.20)
        note = Text(
            "La vista 2D conserva la geometría que el objeto proyecta desde una dirección definida.",
            font_size=24, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.48)
        final = VGroup(mini_views, synthesis, note)
        self.add_fixed_in_frame_mobjects(final)
        for m in (mini_views, synthesis, note):
            m.set_opacity(0)
        self.play(mini_views.animate.set_opacity(1), run_time=T(0.95))
        self.wait(T(1.35))
        self.play(synthesis.animate.set_opacity(1), run_time=T(0.95))
        self.wait(T(1.20))
        self.play(note.animate.set_opacity(1), run_time=T(0.75))
        self.wait(T(5.40))
        self.play(final.animate.set_opacity(0), header.animate.set_opacity(0), run_time=T(0.90))
        self.remove_fixed_in_frame_mobjects(final, header)


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_DIRECTOR_QA.py Projection3Dto2DDirectorV8 --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_DIRECTOR_QA.py Projection3Dto2DDirectorV8 --disable_caching
