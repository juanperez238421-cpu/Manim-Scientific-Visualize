#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sistema diédrico / Método de Monge — V4 faithful reconstruction.

A true 3D teaching scene based on the geometric definition of the dihedral
system: two mutually perpendicular projection planes (PV and PH), their
intersection LT, orthogonal projectors, alzado/planta, and a rigid 90°
unfolding of PH about LT.

Research/design brief:
    RESEARCH_SISTEMA_DIEDRICO_MONGE_V4.md

Target: ManimCE 0.20.1, white classroom style, literal -pqh render.
"""
from __future__ import annotations

import os
import numpy as np
from manim import *

config.background_color = WHITE

# ---------------------------------------------------------------------------
# Classroom palette
# ---------------------------------------------------------------------------
INK = "#111111"
MUTED = "#626262"
GRID = "#B8B8B8"
PV_COLOR = "#8AA9C7"
PH_COLOR = "#D7B77A"
FRONT_COLOR = "#355F8A"
TOP_COLOR = "#A86D13"
SOLID_FILL = "#D9D9D9"
SOFT_BG = "#F5F5F5"

TIME_SCALE = max(0.03, float(os.getenv("LESSON_TIME_SCALE", "1.0")))


def T(seconds: float) -> float:
    return max(0.05, seconds * TIME_SCALE)


class DihedralSystemMongeFaithfulV4(ThreeDScene):
    """Source-faithful 3D construction of the Monge dihedral system."""

    # ------------------------------------------------------------------
    # Small visual helpers
    # ------------------------------------------------------------------
    def chip(self, text: str, width: float, font_size: int = 25) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=0.56,
            corner_radius=0.09,
            stroke_color=GRID,
            stroke_width=1.3,
            fill_color=WHITE,
            fill_opacity=0.96,
        )
        label = Text(text, font_size=font_size, color=INK, weight=MEDIUM)
        label.scale_to_fit_width(width - 0.28)
        label.move_to(box)
        return VGroup(box, label)

    def fixed_fade_in(self, *mobjects, run_time=0.7):
        self.add_fixed_in_frame_mobjects(*mobjects)
        for mob in mobjects:
            mob.set_opacity(0)
        self.play(*[mob.animate.set_opacity(1) for mob in mobjects], run_time=T(run_time))

    def box3d(self, dimensions, center, fill=SOLID_FILL, opacity=0.34):
        """Nonuniform coherent box, dimensioned in world x/y/z coordinates."""
        cube = Cube(
            side_length=1,
            fill_color=fill,
            fill_opacity=opacity,
            stroke_color=INK,
            stroke_width=1.65,
        )
        cube.stretch(float(dimensions[0]), 0)
        cube.stretch(float(dimensions[1]), 1)
        cube.stretch(float(dimensions[2]), 2)
        cube.move_to(np.array(center, dtype=float))
        return cube

    def projector(self, start, end, color=GRID, width=1.45):
        return Line(
            np.array(start, dtype=float),
            np.array(end, dtype=float),
            color=color,
            stroke_width=width,
            stroke_opacity=0.78,
        )

    def front_step_outline(self, y=0.025):
        """Exact alzado of the stepped solid used in the 3D model."""
        pts = [
            [-1.70, y, 0.60],
            [ 1.70, y, 0.60],
            [ 1.70, y, 1.40],
            [ 0.05, y, 1.40],
            [ 0.05, y, 2.40],
            [-1.35, y, 2.40],
            [-1.35, y, 1.40],
            [-1.70, y, 1.40],
        ]
        return Polygon(
            *[np.array(p) for p in pts],
            color=FRONT_COLOR,
            stroke_width=4.0,
            fill_opacity=0,
        )

    def top_step_view(self, z=0.025):
        """Exact planta: base footprint + visible upper-block footprint."""
        outer = Polygon(
            np.array([-1.70, 0.65, z]),
            np.array([ 1.70, 0.65, z]),
            np.array([ 1.70, 2.25, z]),
            np.array([-1.70, 2.25, z]),
            color=TOP_COLOR,
            stroke_width=4.0,
            fill_opacity=0,
        )
        upper = Polygon(
            np.array([-1.35, 0.825, z]),
            np.array([ 0.05, 0.825, z]),
            np.array([ 0.05, 1.675, z]),
            np.array([-1.35, 1.675, z]),
            color=TOP_COLOR,
            stroke_width=3.0,
            fill_opacity=0,
        )
        return VGroup(outer, upper)

    def make_stepped_solid(self):
        """One object; dimensions are shared by the 3D body and both views."""
        # Base: x[-1.70,1.70], y[0.65,2.25], z[0.60,1.40]
        base = self.box3d(
            dimensions=[3.40, 1.60, 0.80],
            center=[0.00, 1.45, 1.00],
            fill=SOLID_FILL,
            opacity=0.34,
        )
        # Upper: x[-1.35,0.05], y[0.825,1.675], z[1.40,2.40]
        upper = self.box3d(
            dimensions=[1.40, 0.85, 1.00],
            center=[-0.65, 1.25, 1.90],
            fill="#CFCFCF",
            opacity=0.38,
        )
        return VGroup(base, upper)

    # ------------------------------------------------------------------
    # Main construction
    # ------------------------------------------------------------------
    def construct(self):
        self.set_camera_orientation(
            phi=67 * DEGREES,
            theta=-48 * DEGREES,
            gamma=0,
            zoom=0.92,
        )

        # Fixed title/subtitle stay stable while the 3D camera moves.
        title = Text(
            "SISTEMA DIÉDRICO · MÉTODO DE MONGE",
            font_size=37,
            color=INK,
            weight=BOLD,
        ).to_edge(UP, buff=0.30)
        subtitle = Text(
            "Proyección ortogonal sobre PV y PH → abatimiento real de 90° sobre la Línea de Tierra",
            font_size=22,
            color=MUTED,
        ).next_to(title, DOWN, buff=0.12)
        self.fixed_fade_in(title, subtitle, run_time=0.9)

        legend = VGroup(
            self.chip("PV · PLANO VERTICAL", 3.15, 20),
            self.chip("PH · PLANO HORIZONTAL", 3.15, 20),
            self.chip("LT · LÍNEA DE TIERRA", 3.15, 20),
        ).arrange(DOWN, buff=0.08).to_corner(UL, buff=0.35).shift(DOWN * 1.15)
        legend[0][0].set_fill(PV_COLOR, opacity=0.22)
        legend[1][0].set_fill(PH_COLOR, opacity=0.22)
        self.fixed_fade_in(legend, run_time=0.7)

        # ------------------------------------------------------------------
        # 1) The real dihedral structure: two perpendicular half-planes.
        # Coordinates: x = LT direction, y = distance from PV, z = height.
        # First dihedral here is y > 0 and z > 0.
        # ------------------------------------------------------------------
        pv = Rectangle(
            width=8.50,
            height=3.25,
            stroke_color=PV_COLOR,
            stroke_width=1.8,
            fill_color=PV_COLOR,
            fill_opacity=0.14,
        )
        pv.rotate(PI / 2, axis=RIGHT)
        pv.shift(OUT * (3.25 / 2))  # z in [0, 3.25]

        ph = Rectangle(
            width=8.50,
            height=3.10,
            stroke_color=PH_COLOR,
            stroke_width=1.8,
            fill_color=PH_COLOR,
            fill_opacity=0.14,
        )
        ph.shift(UP * (3.10 / 2))   # y in [0, 3.10], z = 0

        lt = Line(
            LEFT * 4.25,
            RIGHT * 4.25,
            color=INK,
            stroke_width=3.0,
        )

        self.play(Create(pv), Create(ph), Create(lt), run_time=T(1.6))
        relation = self.chip("PV ⟂ PH   ·   PV ∩ PH = LT", 4.15, 22).to_corner(UR, buff=0.38).shift(DOWN * 1.10)
        self.fixed_fade_in(relation, run_time=0.6)
        self.wait(T(1.25))

        # ------------------------------------------------------------------
        # 2) A point establishes the logic before the solid.
        # ------------------------------------------------------------------
        point_note = self.chip("1 · UN PUNTO A SE PROYECTA PERPENDICULARMENTE", 6.0, 21)
        point_note.to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(point_note, run_time=0.6)

        A = np.array([0.95, 1.70, 2.20])
        Av = np.array([0.95, 0.025, 2.20])  # onto PV: remove y
        Ah = np.array([0.95, 1.70, 0.025])  # onto PH: remove z
        dot_A = Dot3D(point=A, radius=0.075, color=INK)
        dot_Av = Dot3D(point=Av, radius=0.060, color=FRONT_COLOR)
        dot_Ah = Dot3D(point=Ah, radius=0.060, color=TOP_COLOR)
        ray_v = self.projector(A, Av, FRONT_COLOR, 2.0)
        ray_h = self.projector(A, Ah, TOP_COLOR, 2.0)

        lab_A = Text("A", font_size=28, color=INK).move_to(A + np.array([0.18, 0.12, 0.18]))
        lab_Av = Text("a′  (alzado)", font_size=22, color=FRONT_COLOR).move_to(Av + np.array([0.65, 0.0, 0.12]))
        lab_Ah = Text("a  (planta)", font_size=22, color=TOP_COLOR).move_to(Ah + np.array([0.65, 0.18, 0.0]))
        self.add_fixed_orientation_mobjects(lab_A, lab_Av, lab_Ah)
        lab_A.set_opacity(0); lab_Av.set_opacity(0); lab_Ah.set_opacity(0)

        self.play(FadeIn(dot_A), lab_A.animate.set_opacity(1), run_time=T(0.6))
        self.play(Create(ray_v), FadeIn(dot_Av), lab_Av.animate.set_opacity(1), run_time=T(0.9))
        self.play(Create(ray_h), FadeIn(dot_Ah), lab_Ah.animate.set_opacity(1), run_time=T(0.9))
        self.wait(T(1.4))

        self.play(
            FadeOut(dot_A), FadeOut(dot_Av), FadeOut(dot_Ah),
            FadeOut(ray_v), FadeOut(ray_h),
            lab_A.animate.set_opacity(0), lab_Av.animate.set_opacity(0), lab_Ah.animate.set_opacity(0),
            run_time=T(0.8),
        )
        self.remove_fixed_in_frame_mobjects(point_note)
        self.play(FadeOut(point_note), run_time=T(0.35))

        # ------------------------------------------------------------------
        # 3) The same construction is applied to one coherent asymmetric solid.
        # ------------------------------------------------------------------
        solid_note = self.chip("2 · EL MISMO PRINCIPIO, AHORA SOBRE UN SÓLIDO", 5.6, 21)
        solid_note.to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(solid_note, run_time=0.6)

        solid = self.make_stepped_solid()
        self.play(FadeIn(solid, shift=OUT * 0.08), run_time=T(1.2))
        self.wait(T(0.8))

        # FRONT projection: rays are all parallel to y and therefore normal to PV.
        front_sources = [
            [-1.70, 0.65, 0.60], [1.70, 0.65, 0.60],
            [ 1.70, 0.65, 1.40], [-1.70, 0.65, 1.40],
            [-1.35, 0.825, 2.40], [0.05, 0.825, 2.40],
        ]
        front_rays = VGroup(*[
            self.projector(p, [p[0], 0.025, p[2]], FRONT_COLOR, 1.6)
            for p in front_sources
        ])
        front_outline = self.front_step_outline(y=0.025)

        cue_front = self.chip("ALZADO → proyección normal a PV", 4.2, 20).to_edge(DOWN, buff=0.28)
        self.remove_fixed_in_frame_mobjects(solid_note)
        self.play(FadeOut(solid_note), run_time=T(0.3))
        self.fixed_fade_in(cue_front, run_time=0.45)
        self.play(LaggedStart(*[Create(r) for r in front_rays], lag_ratio=0.07), run_time=T(1.3))
        self.play(Create(front_outline), run_time=T(1.1))
        self.wait(T(0.9))
        self.play(FadeOut(front_rays), run_time=T(0.55))
        self.remove_fixed_in_frame_mobjects(cue_front)
        self.play(FadeOut(cue_front), run_time=T(0.3))

        # TOP projection: rays are all parallel to z and therefore normal to PH.
        top_sources = [
            [-1.70, 0.65, 1.40], [1.70, 0.65, 1.40],
            [ 1.70, 2.25, 1.40], [-1.70, 2.25, 1.40],
            [-1.35, 0.825, 2.40], [0.05, 0.825, 2.40],
            [ 0.05, 1.675, 2.40], [-1.35, 1.675, 2.40],
        ]
        top_rays = VGroup(*[
            self.projector(p, [p[0], p[1], 0.025], TOP_COLOR, 1.45)
            for p in top_sources
        ])
        top_view = self.top_step_view(z=0.025)
        cue_top = self.chip("PLANTA → proyección normal a PH", 4.2, 20).to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(cue_top, run_time=0.45)
        self.play(LaggedStart(*[Create(r) for r in top_rays], lag_ratio=0.055), run_time=T(1.35))
        self.play(Create(top_view), run_time=T(1.1))
        self.wait(T(1.0))
        self.play(FadeOut(top_rays), run_time=T(0.55))
        self.remove_fixed_in_frame_mobjects(cue_top)
        self.play(FadeOut(cue_top), run_time=T(0.3))

        # The object is no longer needed: preserve only its two projections.
        keep_note = self.chip("3 · CONSERVAMOS LAS DOS PROYECCIONES", 4.9, 21).to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(keep_note, run_time=0.45)
        self.play(FadeOut(solid), run_time=T(0.85))
        self.wait(T(0.8))

        # ------------------------------------------------------------------
        # 4) Literal abatimiento: PH and its projection rotate together 90°
        # around LT.  LT remains fixed because it is the hinge/charnela.
        # ------------------------------------------------------------------
        self.remove_fixed_in_frame_mobjects(keep_note)
        self.play(FadeOut(keep_note), run_time=T(0.25))
        unfold_note = self.chip("4 · ABATIR PH 90° ALREDEDOR DE LT", 4.9, 21).to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(unfold_note, run_time=0.45)

        ph_with_projection = VGroup(ph, top_view)
        self.play(
            Rotate(
                ph_with_projection,
                angle=-PI / 2,
                axis=RIGHT,
                about_point=ORIGIN,
                rate_func=smooth,
            ),
            run_time=T(2.8),
        )
        self.wait(T(0.9))

        # Move the camera to the observer's frontal direction.  Both views are
        # now genuinely coplanar in the x-z plane.
        self.move_camera(
            phi=90 * DEGREES,
            theta=90 * DEGREES,
            gamma=0,
            zoom=1.02,
            run_time=T(2.0),
        )
        self.remove_fixed_in_frame_mobjects(unfold_note)
        self.play(FadeOut(unfold_note), run_time=T(0.25))

        # ------------------------------------------------------------------
        # 5) Reference lines make the correspondence explicit.
        # ------------------------------------------------------------------
        ref_note = self.chip("MISMA x → PROYECCIONES ALINEADAS ⟂ LT", 5.4, 20).to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(ref_note, run_time=0.45)

        # Lines lie just in front of the final drawing plane to avoid z-fighting.
        refs = VGroup(*[
            Line(
                np.array([x, 0.040, 2.55]),
                np.array([x, 0.040, -2.35]),
                color=GRID,
                stroke_width=1.25,
                stroke_opacity=0.72,
            )
            for x in (-1.70, -1.35, 0.05, 1.70)
        ])
        self.play(LaggedStart(*[Create(r) for r in refs], lag_ratio=0.12), run_time=T(1.15))
        self.wait(T(1.0))

        final_labels = VGroup(
            self.chip("ALZADO · PV", 2.35, 22).move_to(UP * 2.25 + RIGHT * 4.55),
            self.chip("LT · CHARNELA", 2.65, 22).move_to(RIGHT * 4.35 + DOWN * 0.05),
            self.chip("PLANTA · PH ABATIDO", 3.25, 22).move_to(DOWN * 2.30 + RIGHT * 4.20),
        )
        self.fixed_fade_in(final_labels, run_time=0.6)
        self.wait(T(1.2))
        self.play(FadeOut(refs), run_time=T(0.65))
        self.remove_fixed_in_frame_mobjects(ref_note)
        self.play(FadeOut(ref_note), run_time=T(0.25))

        conclusion = self.chip(
            "PRIMER DIEDRO: ALZADO SOBRE LT · PLANTA BAJO LT",
            6.25,
            22,
        ).to_edge(DOWN, buff=0.28)
        self.fixed_fade_in(conclusion, run_time=0.55)
        self.wait(T(2.1))

        # Clean ending preserves the final geometric state long enough for class.
        self.play(
            *[FadeOut(m) for m in final_labels],
            run_time=T(0.45),
        )
        self.remove_fixed_in_frame_mobjects(conclusion)
        self.play(FadeOut(conclusion), run_time=T(0.25))
        self.wait(T(0.7))
