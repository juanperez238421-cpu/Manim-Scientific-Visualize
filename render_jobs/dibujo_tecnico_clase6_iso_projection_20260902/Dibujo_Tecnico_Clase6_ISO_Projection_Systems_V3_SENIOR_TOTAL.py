#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Tecnico y CAD — Clase 6 · V3 Senior Total.

V3 is the post-render senior QA rebuild of V2.  It keeps the lesson content,
ISO A / ISO E logic, source-deck structure and established classroom styling,
while correcting the remaining projection-animation defects detected in the
actual V2 PQH video.

V3 corrections over V2
----------------------
1. No projector-ray crossings through already-built views.
2. No duplicated/stacked views during the dihedral 90° unfold.
3. Safe margins: no axis/triad marks touch the hard video border.
4. Projection extraction uses a temporary projection plane, then moves the
   completed view to its final ISO A / ISO E sheet position.
5. The gable-roof object is a single coherent coordinate model with one
   pentagonal front gable face and matching orthographic views.
6. Dihedral explanation is sequential: FRONT projection -> TOP projection ->
   90° plane unfolding -> final aligned drawing sheet.

Target: ManimCE 0.20.1, literal -pqh final render.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V2_SENIOR_QA import (
    TechnicalDrawingClass6ISOV2,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT,
    TOP_FILL,
    FRONT_FILL,
    SIDE_FILL,
    RUN_Q,
    RUN,
    RUN_SLOW,
    RUN_FOLD,
    PAUSE_R,
    PAUSE_E,
    PAUSE_W,
)


class TechnicalDrawingClass6ISOV3(TechnicalDrawingClass6ISOV2):
    """Final senior geometry/projection correction layer."""

    # ------------------------------------------------------------------
    # Coherent 3D teaching solids
    # ------------------------------------------------------------------
    def make_house_solid(self, scale=0.72):
        """Coherent gable-roof prism: 3×2 plan, eave 1.2, ridge 2.2.

        The FRONT face is one pentagon.  Roof faces share the same ridge
        coordinates used by the TOP and RIGHT orthographic views.
        """
        o = ORIGIN
        front = self.iso_face(
            [(0, 0, 0), (3, 0, 0), (3, 0, 1.2), (1.5, 0, 2.2), (0, 0, 1.2)],
            o, scale, FRONT_FILL,
        )
        right_wall = self.iso_face(
            [(3, 0, 0), (3, 2, 0), (3, 2, 1.2), (3, 0, 1.2)],
            o, scale, SIDE_FILL,
        )
        roof_right = self.iso_face(
            [(3, 0, 1.2), (3, 2, 1.2), (1.5, 2, 2.2), (1.5, 0, 2.2)],
            o, scale, "#E1E1E1",
        )
        roof_left = self.iso_face(
            [(0, 0, 1.2), (1.5, 0, 2.2), (1.5, 2, 2.2), (0, 2, 1.2)],
            o, scale, TOP_FILL,
        )
        faces = VGroup(front, right_wall, roof_right, roof_left)
        edges = VGroup(
            self.iso_edge((0, 0, 0), (3, 0, 0), o, scale),
            self.iso_edge((0, 0, 0), (0, 0, 1.2), o, scale),
            self.iso_edge((3, 0, 0), (3, 0, 1.2), o, scale),
            self.iso_edge((3, 0, 0), (3, 2, 0), o, scale),
            self.iso_edge((3, 2, 0), (3, 2, 1.2), o, scale),
            self.iso_edge((0, 0, 1.2), (1.5, 0, 2.2), o, scale),
            self.iso_edge((1.5, 0, 2.2), (3, 0, 1.2), o, scale),
            self.iso_edge((3, 0, 1.2), (3, 2, 1.2), o, scale),
            self.iso_edge((1.5, 0, 2.2), (1.5, 2, 2.2), o, scale),
            self.iso_edge((3, 2, 1.2), (1.5, 2, 2.2), o, scale),
            self.iso_edge((0, 0, 1.2), (0, 2, 1.2), o, scale),
            self.iso_edge((0, 2, 1.2), (1.5, 2, 2.2), o, scale),
            # Eave line on the front gable is intentionally visible.
            self.iso_edge((0, 0, 1.2), (3, 0, 1.2), o, scale, sw=1.8),
        )
        return VGroup(faces, edges)

    # ------------------------------------------------------------------
    # Projection animation primitives
    # ------------------------------------------------------------------
    def parallel_bundle(self, start_center, end_center, count=5, spread=0.65, sw=1.5):
        """Parallel orthographic projectors between two anchor centers."""
        start_center = np.array(start_center, dtype=float)
        end_center = np.array(end_center, dtype=float)
        direction = end_center - start_center
        norm = np.linalg.norm(direction[:2])
        if norm < 1e-8:
            direction = RIGHT.copy()
            norm = 1.0
        u = direction / norm
        perp = np.array([-u[1], u[0], 0.0])
        rays = VGroup()
        for offset in np.linspace(-spread, spread, count):
            a = start_center + offset * perp
            b = end_center + offset * perp
            rays.add(
                DashedLine(
                    a, b, dash_length=0.085,
                    stroke_color=MID_GRAY, stroke_width=sw,
                )
            )
        return rays

    def observation_arrow(self, label, direction=RIGHT):
        """Compact observation-direction cue that stays inside safe margins."""
        d = np.array(direction, dtype=float)
        d = d / max(np.linalg.norm(d), 1e-8)
        arrow = Arrow(-d * 0.72, d * 0.72, buff=0, color=BLACK_LINE, stroke_width=2.2)
        chip = self.chip(label, 2.8, 18).next_to(arrow, DOWN, buff=0.10)
        return VGroup(arrow, chip)

    def compact_view_card(self, view, label, width=2.50, height=1.82):
        return self.framed_view(view, label, width=width, height=height)

    def _view_targets(self, front, top, right, system="A"):
        """Safe, non-overlapping final sheet positions."""
        front.move_to(RIGHT * 2.75 + DOWN * 0.40)
        if system == "A":
            top.move_to(RIGHT * 2.75 + UP * 1.82)
            right.move_to(RIGHT * 5.35 + DOWN * 0.40)
        else:
            top.move_to(RIGHT * 2.75 + DOWN * 2.58)
            right.move_to(RIGHT * 0.15 + DOWN * 0.40)
        return VGroup(front, top, right)

    def _extract_view_to_target(self, solid, target_card, view_factory, label, cue_text, temp_center):
        """Project one view into a temporary plane, then move it to its sheet slot.

        Crucially, projector rays end at the temporary plane.  They never pass
        through previously completed view cards.
        """
        temp_view = view_factory()
        temp_card = self.compact_view_card(temp_view, label)
        temp_card.move_to(temp_center)
        plane = RoundedRectangle(
            width=2.72, height=2.05, corner_radius=0.07,
            stroke_color=MID_GRAY, stroke_width=1.5,
            fill_color=VERY_LIGHT, fill_opacity=0.25,
        ).move_to(temp_card.get_center())
        cue = self.chip(cue_text, 3.0, 19).move_to(LEFT * 4.25 + DOWN * 2.55)
        start = solid.get_right() + RIGHT * 0.10
        end = plane.get_left() + LEFT * 0.10
        rays = self.parallel_bundle(start, end, count=5, spread=0.56)

        self.play(FadeIn(cue), Create(plane), run_time=RUN_Q)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.08), run_time=RUN_FOLD)
        self.play(Create(temp_card), run_time=RUN)
        self.wait(PAUSE_R * 0.55)
        # Move the actual completed view card.  No copy remains behind.
        self.play(
            FadeOut(rays), FadeOut(plane), FadeOut(cue),
            Transform(temp_card, target_card),
            run_time=RUN_FOLD,
        )
        self.wait(PAUSE_R * 0.40)
        return temp_card

    # ------------------------------------------------------------------
    # Rebuilt dihedral scene — no duplicate views, no ray crossings
    # ------------------------------------------------------------------
    def dihedral_system(self):
        self.set_header(
            "SISTEMA DIEDRICO",
            "One fixed solid is projected orthogonally onto FRONT and TOP planes; then the TOP plane unfolds 90 degrees.",
        )

        solid = self.make_step_solid(0.82).move_to(LEFT * 4.25 + DOWN * 0.28)
        tag = self.chip("ONE COHERENT 3D OBJECT", 4.0, 21).next_to(solid, UP, buff=0.34)
        self.play(FadeIn(solid, shift=UP * 0.10), FadeIn(tag), run_time=RUN_SLOW)
        self.wait(PAUSE_R)

        # FRONT plane: vertical rectangle, clearly separated from the object.
        front_plane = RoundedRectangle(
            width=3.45, height=2.45, corner_radius=0.06,
            stroke_color=MID_GRAY, stroke_width=1.7,
            fill_color=VERY_LIGHT, fill_opacity=0.32,
        ).move_to(RIGHT * 3.05 + UP * 0.88)
        front_label = self.chip("VERTICAL PLANE · FRONT", 4.1, 19).next_to(front_plane, UP, buff=0.10)
        front_view = self.view_front_step(0.56).move_to(front_plane.get_center())

        self.play(Create(front_plane), FadeIn(front_label), run_time=RUN)
        rays_f = self.parallel_bundle(
            solid.get_right() + RIGHT * 0.10,
            front_plane.get_left() + LEFT * 0.10,
            count=6, spread=0.62,
        )
        cue_f = self.chip("ORTHOGRAPHIC FRONT PROJECTION", 4.7, 18).move_to(DOWN * 2.70 + LEFT * 2.05)
        self.play(FadeIn(cue_f), LaggedStart(*[Create(r) for r in rays_f], lag_ratio=0.07), run_time=RUN_FOLD)
        self.play(Create(front_view), run_time=RUN)
        self.wait(PAUSE_R)
        self.play(FadeOut(rays_f), FadeOut(cue_f), run_time=RUN_Q)

        # TOP plane initially appears as an oblique plane below the front plane.
        h_center = RIGHT * 3.05 + DOWN * 1.48
        w, h = 3.45, 1.48
        hplane = Polygon(
            h_center + np.array([-w/2, 0.34, 0]),
            h_center + np.array([ w/2, 0.34, 0]),
            h_center + np.array([ w/2 + 0.48, -h + 0.34, 0]),
            h_center + np.array([-w/2 + 0.48, -h + 0.34, 0]),
            stroke_color=MID_GRAY, stroke_width=1.7,
            fill_color=VERY_LIGHT, fill_opacity=0.32,
        )
        h_label = self.chip("HORIZONTAL PLANE · TOP", 4.1, 19).next_to(hplane, DOWN, buff=0.10)
        top_view = self.view_top_step(0.48).move_to(hplane.get_center() + UP * 0.08)
        self.play(Create(hplane), FadeIn(h_label), run_time=RUN)

        # Sequential top projection: front rays are already gone, so no crossing web.
        top_start = solid.get_top() + RIGHT * 0.20 + DOWN * 0.15
        top_end = hplane.get_left() + LEFT * 0.05 + UP * 0.15
        rays_t = self.parallel_bundle(top_start, top_end, count=5, spread=0.52)
        cue_t = self.chip("ORTHOGRAPHIC TOP PROJECTION", 4.5, 18).move_to(DOWN * 2.70 + LEFT * 2.05)
        self.play(FadeIn(cue_t), LaggedStart(*[Create(r) for r in rays_t], lag_ratio=0.07), run_time=RUN_FOLD)
        self.play(Create(top_view), run_time=RUN)
        self.wait(PAUSE_R)
        self.play(FadeOut(rays_t), FadeOut(cue_t), run_time=RUN_Q)

        # Explicit hinge and 90° unfolding.  Transform existing objects instead
        # of creating copies; this removes the V2 stacked-view defect.
        hinge_y = front_plane.get_bottom()[1]
        hinge = Line(
            [front_plane.get_left()[0], hinge_y, 0],
            [front_plane.get_right()[0], hinge_y, 0],
            stroke_color=BLACK_LINE, stroke_width=2.0,
        )
        self.play(Create(hinge), run_time=RUN_Q)
        unfold_cue = self.chip("UNFOLD TOP PLANE 90°", 4.1, 20).move_to(LEFT * 0.30 + DOWN * 2.80)
        self.play(FadeIn(unfold_cue), run_time=RUN_Q)

        unfolded_plane = RoundedRectangle(
            width=3.45, height=2.05, corner_radius=0.06,
            stroke_color=MID_GRAY, stroke_width=1.7,
            fill_color=VERY_LIGHT, fill_opacity=0.28,
        ).move_to(RIGHT * 3.05 + DOWN * 1.60)
        unfolded_top = self.view_top_step(0.50).move_to(unfolded_plane.get_center())
        unfolded_label = self.chip("TOP VIEW · UNFOLDED", 3.7, 19).next_to(unfolded_plane, DOWN, buff=0.10)

        self.play(
            Transform(hplane, unfolded_plane),
            Transform(top_view, unfolded_top),
            FadeOut(h_label),
            run_time=RUN_FOLD * 1.15,
        )
        self.play(FadeIn(unfolded_label), run_time=RUN_Q)
        self.wait(PAUSE_E)

        final_note = self.chip("FRONT + TOP ARE NOW COPLANAR ON THE DRAWING SHEET", 6.5, 19)
        final_note.move_to(RIGHT * 2.45 + DOWN * 3.15)
        self.play(ReplacementTransform(unfold_cue, final_note), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    # ------------------------------------------------------------------
    # Cleaner example projection sequence
    # ------------------------------------------------------------------
    def _run_example(self, solid, front_factory, top_factory, right_factory, system="A"):
        """Sequential projection/extraction with a reusable clean projection zone."""
        # Final sheet cards are targets only; they are not visible during rays.
        f_target = self.compact_view_card(front_factory(), "FRONT")
        t_target = self.compact_view_card(top_factory(), "TOP")
        r_target = self.compact_view_card(right_factory(), "RIGHT")
        self._view_targets(f_target, t_target, r_target, system)

        self.play(FadeIn(solid, shift=UP * 0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_R)

        temp = LEFT * 0.15 + DOWN * 0.35
        built = []
        built.append(self._extract_view_to_target(solid, f_target, front_factory, "FRONT", "PROJECT FRONT", temp))
        built.append(self._extract_view_to_target(solid, t_target, top_factory, "TOP", "PROJECT TOP", temp))
        built.append(self._extract_view_to_target(solid, r_target, right_factory, "RIGHT", "PROJECT RIGHT", temp))

        sheet = self.chip(
            "THIRD-ANGLE PLACEMENT" if system == "A" else "FIRST-ANGLE PLACEMENT",
            4.2, 19,
        ).move_to(RIGHT * 3.80 + DOWN * 3.02)
        self.play(FadeIn(sheet), run_time=RUN_Q)
        self.wait(PAUSE_W)
        return VGroup(*built, sheet)

    def iso_a_example_1(self):
        self.set_header(
            "EJEMPLO ISO A · 1",
            "A coherent gable-roof solid produces matching FRONT, TOP and RIGHT views in third-angle placement.",
        )
        solid = self.make_house_solid(0.80).move_to(LEFT * 4.45 + DOWN * 0.38)
        self._run_example(
            solid,
            lambda: self.view_house_front(0.61),
            lambda: self.view_house_top(0.61),
            lambda: self.view_house_right(0.61),
            system="A",
        )
        self.clear_content()

    def iso_a_example_2(self):
        self.set_header(
            "EJEMPLO ISO A · 2",
            "The stepped solid keeps exact 3×2×2.10 proportions and its 1.25×1.10 tower footprint in every view.",
        )
        solid = self.make_step_solid(0.84).move_to(LEFT * 4.45 + DOWN * 0.38)
        self._run_example(
            solid,
            lambda: self.view_front_step(0.62),
            lambda: self.view_top_step(0.62),
            lambda: self.view_right_step(0.62),
            system="A",
        )
        self.clear_content()

    def iso_e_example_1(self):
        self.set_header(
            "EJEMPLO ISO E · 1",
            "The same stepped solid generates the same views; first-angle changes only their final positions on the sheet.",
        )
        solid = self.make_step_solid(0.84).move_to(LEFT * 4.45 + DOWN * 0.38)
        cue = self.card(
            "FIRST-ANGLE CUE",
            ["TOP goes below FRONT", "RIGHT view goes to the left"],
            width=4.3, body_size=20,
        ).move_to(LEFT * 4.45 + DOWN * 2.55)
        self.play(FadeIn(cue), run_time=RUN_Q)
        self._run_example(
            solid,
            lambda: self.view_front_step(0.62),
            lambda: self.view_top_step(0.62),
            lambda: self.view_right_step(0.62),
            system="E",
        )
        self.clear_content()

    def iso_e_example_2(self):
        self.set_header(
            "EJEMPLO ISO E · 2",
            "The gable-roof geometry is unchanged; identify the first-angle symbol, then place TOP below and RIGHT to the left.",
        )
        solid = self.make_house_solid(0.80).move_to(LEFT * 4.45 + DOWN * 0.38)
        symbol = self.first_third_symbol(False, 0.72).move_to(LEFT * 4.45 + DOWN * 2.55)
        self.play(FadeIn(symbol), run_time=RUN_Q)
        self._run_example(
            solid,
            lambda: self.view_house_front(0.61),
            lambda: self.view_house_top(0.61),
            lambda: self.view_house_right(0.61),
            system="E",
        )
        self.clear_content()


# Preview:
# manim -pql Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V3_SENIOR_TOTAL.py TechnicalDrawingClass6ISOV3 --disable_caching
# Final protocol render:
# manim -pqh Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V3_SENIOR_TOTAL.py TechnicalDrawingClass6ISOV3 --disable_caching
