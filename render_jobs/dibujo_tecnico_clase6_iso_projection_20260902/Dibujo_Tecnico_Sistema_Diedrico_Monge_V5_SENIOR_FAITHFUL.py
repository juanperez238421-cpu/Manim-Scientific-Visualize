#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sistema diédrico / Método de Monge — V5 Senior Faithful.

True ThreeDScene reconstruction based on the source research brief:
- PV and PH are mutually perpendicular half-planes.
- LT is their real common intersection / hinge.
- Orthographic projectors are normal to the receiving plane.
- A point is demonstrated first (a' / a).
- One coherent asymmetric solid generates alzado and planta.
- PH and the planta rotate rigidly by 90 degrees around LT.
- Final first-dihedral arrangement: alzado above LT, planta below LT.

V5 keeps the mathematical model from V4 but reduces the plane/camera envelope
so the entire 90-degree abatimiento remains inside the 16:9 safe frame.
Target: ManimCE 0.20.1, literal -pqh final render.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

config.background_color = WHITE

INK = "#111111"
MUTED = "#686868"
GRID = "#BEBEBE"
PV_COLOR = "#7598BB"
PH_COLOR = "#D1AE6C"
FRONT_COLOR = "#2F5D86"
TOP_COLOR = "#9B6514"
SOLID_1 = "#D9D9D9"
SOLID_2 = "#C9C9C9"

TIME_SCALE = max(0.03, float(os.getenv("LESSON_TIME_SCALE", "1.0")))


def T(seconds: float) -> float:
    return max(0.05, seconds * TIME_SCALE)


class DihedralSystemMongeSeniorV5(ThreeDScene):
    """Faithful and classroom-readable Monge dihedral-system animation."""

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def chip(self, text: str, width: float, font_size: int = 23) -> VGroup:
        box = RoundedRectangle(
            width=width, height=0.52, corner_radius=0.08,
            stroke_color=GRID, stroke_width=1.25,
            fill_color=WHITE, fill_opacity=0.97,
        )
        label = Text(text, font_size=font_size, color=INK)
        label.scale_to_fit_width(width - 0.26)
        label.move_to(box)
        return VGroup(box, label)

    def fixed_fade_in(self, *mobjects, run_time=0.6):
        self.add_fixed_in_frame_mobjects(*mobjects)
        for m in mobjects:
            m.set_opacity(0)
        self.play(*[m.animate.set_opacity(1) for m in mobjects], run_time=T(run_time))

    def fixed_fade_out(self, *mobjects, run_time=0.35):
        self.play(*[FadeOut(m) for m in mobjects], run_time=T(run_time))
        for m in mobjects:
            self.remove_fixed_in_frame_mobjects(m)

    # ------------------------------------------------------------------
    # Coherent geometry model
    # ------------------------------------------------------------------
    def box3d(self, dims, center, fill, opacity=0.36):
        c = Cube(
            side_length=1,
            fill_color=fill,
            fill_opacity=opacity,
            stroke_color=INK,
            stroke_width=1.55,
        )
        c.stretch(float(dims[0]), 0)
        c.stretch(float(dims[1]), 1)
        c.stretch(float(dims[2]), 2)
        c.move_to(np.array(center, dtype=float))
        return c

    def make_solid(self):
        """Asymmetric two-level solid, dimensionally shared by both views."""
        # Base: x[-1.45,1.45], y[0.55,1.95], z[0.45,1.15]
        base = self.box3d([2.90, 1.40, 0.70], [0.00, 1.25, 0.80], SOLID_1, 0.34)
        # Upper: x[-1.15,0.10], y[0.72,1.48], z[1.15,2.00]
        upper = self.box3d([1.25, 0.76, 0.85], [-0.525, 1.10, 1.575], SOLID_2, 0.39)
        return VGroup(base, upper)

    def front_outline(self, y=0.018):
        pts = [
            [-1.45, y, 0.45], [1.45, y, 0.45],
            [1.45, y, 1.15], [0.10, y, 1.15],
            [0.10, y, 2.00], [-1.15, y, 2.00],
            [-1.15, y, 1.15], [-1.45, y, 1.15],
        ]
        return Polygon(
            *[np.array(p) for p in pts],
            stroke_color=FRONT_COLOR, stroke_width=4.0,
            fill_opacity=0,
        )

    def top_outline(self, z=0.018):
        base = Polygon(
            np.array([-1.45, 0.55, z]), np.array([1.45, 0.55, z]),
            np.array([1.45, 1.95, z]), np.array([-1.45, 1.95, z]),
            stroke_color=TOP_COLOR, stroke_width=4.0, fill_opacity=0,
        )
        upper = Polygon(
            np.array([-1.15, 0.72, z]), np.array([0.10, 0.72, z]),
            np.array([0.10, 1.48, z]), np.array([-1.15, 1.48, z]),
            stroke_color=TOP_COLOR, stroke_width=3.0, fill_opacity=0,
        )
        return VGroup(base, upper)

    def projector(self, a, b, color):
        return Line(
            np.array(a, dtype=float), np.array(b, dtype=float),
            stroke_color=color, stroke_width=1.55, stroke_opacity=0.78,
        )

    # ------------------------------------------------------------------
    # Scene
    # ------------------------------------------------------------------
    def construct(self):
        # World convention:
        #   x -> LT direction
        #   y -> distance in front of PV
        #   z -> height above PH
        # Therefore PV: y=0, PH: z=0, LT: y=z=0.
        self.set_camera_orientation(
            phi=66 * DEGREES,
            theta=-48 * DEGREES,
            gamma=0,
            zoom=0.78,
        )

        title = Text(
            "SISTEMA DIÉDRICO · MÉTODO DE MONGE",
            font_size=35, color=INK, weight=BOLD,
        ).to_edge(UP, buff=0.30)
        subtitle = Text(
            "Dos planos perpendiculares · proyección ortogonal · abatimiento sobre LT",
            font_size=21, color=MUTED,
        ).next_to(title, DOWN, buff=0.10)
        self.fixed_fade_in(title, subtitle, run_time=0.8)

        legend = VGroup(
            self.chip("PV · PLANO VERTICAL", 2.90, 19),
            self.chip("PH · PLANO HORIZONTAL", 2.90, 19),
            self.chip("LT · LÍNEA DE TIERRA", 2.90, 19),
        ).arrange(DOWN, buff=0.07).to_corner(UL, buff=0.40).shift(DOWN * 1.08)
        legend[0][0].set_fill(PV_COLOR, opacity=0.20)
        legend[1][0].set_fill(PH_COLOR, opacity=0.20)
        self.fixed_fade_in(legend, run_time=0.55)

        # Smaller bounded half-planes: enough for the construction without
        # touching the video edge during the 90-degree rotation.
        PLANE_W = 6.60
        PV_H = 2.72
        PH_D = 2.55

        pv = Rectangle(
            width=PLANE_W, height=PV_H,
            stroke_color=PV_COLOR, stroke_width=1.7,
            fill_color=PV_COLOR, fill_opacity=0.13,
        )
        pv.rotate(PI / 2, axis=RIGHT)
        pv.shift(OUT * (PV_H / 2))

        ph = Rectangle(
            width=PLANE_W, height=PH_D,
            stroke_color=PH_COLOR, stroke_width=1.7,
            fill_color=PH_COLOR, fill_opacity=0.13,
        )
        ph.shift(UP * (PH_D / 2))

        lt = Line(LEFT * (PLANE_W / 2), RIGHT * (PLANE_W / 2), color=INK, stroke_width=3.0)

        self.play(Create(pv), Create(ph), Create(lt), run_time=T(1.45))
        relation = self.chip("PV ⟂ PH     y     PV ∩ PH = LT", 3.75, 20)
        relation.to_corner(UR, buff=0.42).shift(DOWN * 1.08)
        self.fixed_fade_in(relation, run_time=0.5)
        self.wait(T(1.0))

        # ------------------------------------------------------------------
        # Step 1: point A.  These are literal orthogonal projections.
        # ------------------------------------------------------------------
        step1 = self.chip("1 · PUNTO A → DOS PROYECCIONES ORTOGONALES", 5.50, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(step1, run_time=0.45)

        A = np.array([0.72, 1.46, 1.82])
        Av = np.array([0.72, 0.018, 1.82])  # a' on PV
        Ah = np.array([0.72, 1.46, 0.018])  # a on PH
        dA = Dot3D(A, radius=0.070, color=INK)
        dAv = Dot3D(Av, radius=0.058, color=FRONT_COLOR)
        dAh = Dot3D(Ah, radius=0.058, color=TOP_COLOR)
        rv = self.projector(A, Av, FRONT_COLOR)
        rh = self.projector(A, Ah, TOP_COLOR)

        labA = Text("A", font_size=26, color=INK).move_to(A + np.array([0.16, 0.08, 0.15]))
        labAv = Text("a′ · alzado", font_size=20, color=FRONT_COLOR).move_to(Av + np.array([0.52, 0.0, 0.10]))
        labAh = Text("a · planta", font_size=20, color=TOP_COLOR).move_to(Ah + np.array([0.52, 0.14, 0.0]))
        self.add_fixed_orientation_mobjects(labA, labAv, labAh)
        labA.set_opacity(0); labAv.set_opacity(0); labAh.set_opacity(0)

        self.play(FadeIn(dA), labA.animate.set_opacity(1), run_time=T(0.55))
        self.play(Create(rv), FadeIn(dAv), labAv.animate.set_opacity(1), run_time=T(0.85))
        self.play(Create(rh), FadeIn(dAh), labAh.animate.set_opacity(1), run_time=T(0.85))
        self.wait(T(1.15))
        self.play(
            FadeOut(dA), FadeOut(dAv), FadeOut(dAh), FadeOut(rv), FadeOut(rh),
            labA.animate.set_opacity(0), labAv.animate.set_opacity(0), labAh.animate.set_opacity(0),
            run_time=T(0.65),
        )
        self.fixed_fade_out(step1, run_time=0.25)

        # ------------------------------------------------------------------
        # Step 2: one coherent asymmetric solid.
        # ------------------------------------------------------------------
        step2 = self.chip("2 · EL MISMO PRINCIPIO SOBRE UN SÓLIDO", 4.70, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(step2, run_time=0.45)
        solid = self.make_solid()
        self.play(FadeIn(solid, shift=OUT * 0.06), run_time=T(1.0))
        self.wait(T(0.75))
        self.fixed_fade_out(step2, run_time=0.25)

        # FRONT / alzado: projectors are parallel to y, hence normal to PV.
        cue_f = self.chip("ALZADO · proyectantes ⟂ PV", 3.65, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(cue_f, run_time=0.4)
        front_sources = [
            [-1.45,0.55,0.45], [1.45,0.55,0.45], [1.45,0.55,1.15],
            [-1.45,0.55,1.15], [-1.15,0.72,2.00], [0.10,0.72,2.00],
        ]
        front_rays = VGroup(*[
            self.projector(p, [p[0],0.018,p[2]], FRONT_COLOR) for p in front_sources
        ])
        front = self.front_outline()
        self.play(LaggedStart(*[Create(r) for r in front_rays], lag_ratio=0.07), run_time=T(1.10))
        self.play(Create(front), run_time=T(0.95))
        self.wait(T(0.65))
        self.play(FadeOut(front_rays), run_time=T(0.45))
        self.fixed_fade_out(cue_f, run_time=0.22)

        # TOP / planta: projectors are parallel to z, hence normal to PH.
        cue_t = self.chip("PLANTA · proyectantes ⟂ PH", 3.65, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(cue_t, run_time=0.4)
        top_sources = [
            [-1.45,0.55,1.15], [1.45,0.55,1.15], [1.45,1.95,1.15], [-1.45,1.95,1.15],
            [-1.15,0.72,2.00], [0.10,0.72,2.00], [0.10,1.48,2.00], [-1.15,1.48,2.00],
        ]
        top_rays = VGroup(*[
            self.projector(p, [p[0],p[1],0.018], TOP_COLOR) for p in top_sources
        ])
        top = self.top_outline()
        self.play(LaggedStart(*[Create(r) for r in top_rays], lag_ratio=0.05), run_time=T(1.15))
        self.play(Create(top), run_time=T(0.95))
        self.wait(T(0.70))
        self.play(FadeOut(top_rays), run_time=T(0.45))
        self.fixed_fade_out(cue_t, run_time=0.22)

        # Preserve the projections and remove the source body before unfolding.
        keep = self.chip("3 · CONSERVAMOS ALZADO + PLANTA", 4.35, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(keep, run_time=0.4)
        self.play(FadeOut(solid), run_time=T(0.70))
        self.wait(T(0.55))
        self.fixed_fade_out(keep, run_time=0.22)

        # ------------------------------------------------------------------
        # Step 4: literal rigid-body abatimiento.
        # LT is the hinge axis. PH and the top view rotate together.
        # ------------------------------------------------------------------
        unfold = self.chip("4 · ABATIMIENTO: PH GIRA 90° SOBRE LT", 4.95, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(unfold, run_time=0.4)
        ph_and_top = VGroup(ph, top)
        self.play(
            Rotate(
                ph_and_top,
                angle=-PI/2,
                axis=RIGHT,
                about_point=ORIGIN,
                rate_func=smooth,
            ),
            run_time=T(2.55),
        )
        self.wait(T(0.65))

        # Camera turns to a clean frontal view of the now-coplanar projections.
        # Reduced zoom is deliberate: no plane or LT edge approaches the hard frame.
        self.move_camera(
            phi=90 * DEGREES,
            theta=90 * DEGREES,
            gamma=0,
            zoom=0.80,
            run_time=T(1.65),
        )
        self.fixed_fade_out(unfold, run_time=0.22)

        # ------------------------------------------------------------------
        # Final epure / drawing sheet logic.
        # ------------------------------------------------------------------
        aligned = self.chip("5 · MISMA x → CORRESPONDENCIA ⟂ LT", 4.60, 20).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(aligned, run_time=0.4)
        refs = VGroup(*[
            Line(
                np.array([x, 0.035, 2.15]), np.array([x, 0.035, -2.05]),
                stroke_color=GRID, stroke_width=1.2, stroke_opacity=0.70,
            )
            for x in (-1.45, -1.15, 0.10, 1.45)
        ])
        self.play(LaggedStart(*[Create(r) for r in refs], lag_ratio=0.12), run_time=T(0.95))
        self.wait(T(0.75))

        labels = VGroup(
            self.chip("ALZADO · PV", 2.20, 20).move_to(RIGHT*4.15 + UP*1.90),
            self.chip("LT · CHARNELA", 2.45, 20).move_to(RIGHT*4.10 + DOWN*0.02),
            self.chip("PLANTA · PH ABATIDO", 3.15, 20).move_to(RIGHT*4.00 + DOWN*1.90),
        )
        self.fixed_fade_in(labels, run_time=0.5)
        self.wait(T(1.0))
        self.play(FadeOut(refs), run_time=T(0.45))
        self.fixed_fade_out(aligned, run_time=0.22)

        final = self.chip("PRIMER DIEDRO: ALZADO SOBRE LT · PLANTA BAJO LT", 6.10, 21).to_edge(DOWN, buff=0.36)
        self.fixed_fade_in(final, run_time=0.5)
        self.wait(T(2.0))
