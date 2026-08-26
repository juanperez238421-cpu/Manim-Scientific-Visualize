from __future__ import annotations

import numpy as np
from manim import *

from chamfer_chaflan_senior_v3 import (
    InventorChamferChaflanSeniorV3,
    DARK, SKETCH, VALID, BOLD, smooth,
)
from chamfer_chaflan_senior_v2 import REMOVE


class InventorChamferChaflanSeniorV4(InventorChamferChaflanSeniorV3):
    """Final label-clearance QA pass for Chamfer / Chaflán.

    V4 fixes the last visual merge found in V3 frame inspection: the horizontal
    6 mm label crossed the green chamfer line in both the conceptual section and
    the enlarged corner-detail section. The label is now reserved above its
    dimension arrow, in the clear strip between the dimension line and top edge.
    """

    def concept_geometry(self, hud, sharp_geom, corner):
        self.set_phase(hud, 2, "DISTANCIA + ÁNGULO", SKETCH)
        c = 1.65
        a = corner + LEFT*c
        b = corner + DOWN*c
        cut = Line(a, b, color=VALID, stroke_width=9)
        tri = Polygon(
            a, corner, b,
            fill_color=REMOVE, fill_opacity=0.15,
            stroke_color=REMOVE, stroke_width=1.4,
        )
        a_dot = Dot(a, radius=0.075, color=VALID)
        b_dot = Dot(b, radius=0.075, color=VALID)
        h_dim = DoubleArrow(
            a+DOWN*0.48, corner+DOWN*0.48, buff=0,
            color=SKETCH, stroke_width=2.5,
        )
        v_dim = DoubleArrow(
            corner+RIGHT*0.48, b+RIGHT*0.48, buff=0,
            color=SKETCH, stroke_width=2.5,
        )
        # QA V4: horizontal label is ABOVE the dimension line, away from the
        # green diagonal. This removes the V3 text/geometry merge.
        h_lab = self.text("6 mm", 29, BOLD, SKETCH).next_to(h_dim, UP, buff=0.06)
        v_lab = self.text("6 mm", 30, BOLD, SKETCH).rotate(PI/2).next_to(v_dim, RIGHT, buff=0.10)
        angle = Arc(
            radius=0.62, start_angle=3*PI/4, angle=PI/4,
            arc_center=a, color=SKETCH, stroke_width=3.5,
        )
        angle_lab = self.text("45°", 29, BOLD, SKETCH).move_to(a+RIGHT*0.68+UP*0.42)
        planar = self.small_callout("CARA PLANA", VALID, point=[-2.15, -1.55, 0], width=3.75)

        self.play(FadeIn(tri), run_time=0.45)
        self.play(Create(h_dim), Write(h_lab), FadeIn(a_dot), run_time=0.90)
        self.play(Create(v_dim), Write(v_lab), FadeIn(b_dot), run_time=0.90)
        self.play(Create(cut), run_time=1.25, rate_func=smooth)
        self.play(Create(angle), Write(angle_lab), run_time=0.70)
        self.play(FadeIn(planar), run_time=0.50)
        note = self.note(
            "A 45°, dos offsets iguales generan un bisel simétrico: DISTANCE = 6 mm.",
            VALID,
        )
        self.wait(2.0)
        self.clear_fixed(note)
        self.clear_fixed(planar, 0.25)
        self.play(
            FadeOut(sharp_geom), FadeOut(tri), FadeOut(a_dot), FadeOut(b_dot),
            FadeOut(h_dim), FadeOut(v_dim), FadeOut(h_lab), FadeOut(v_lab),
            FadeOut(cut), FadeOut(angle), FadeOut(angle_lab),
            run_time=0.60,
        )

    def distance_on_face(self, hud, body, edge, p0, p1, card):
        self.set_phase(hud, 8, "DETALLE DEL CORTE", SKETCH)
        self.play(FadeOut(card), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)

        # Fully recenter the part only AFTER the parameter card has disappeared.
        total_shift = 1.15 + self.EXTRA_PANEL_CLEARANCE
        self.play(
            body.animate.shift(RIGHT*total_shift),
            edge.animate.shift(RIGHT*total_shift),
            p0.animate.shift(RIGHT*total_shift),
            p1.animate.shift(RIGHT*total_shift),
            run_time=0.75,
            rate_func=smooth,
        )
        self.play(FadeOut(body), FadeOut(edge), FadeOut(p0), FadeOut(p1), run_time=0.45)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.00, run_time=0.90)

        corner = np.array([2.30, 1.15, 0])
        top_edge = Line([-3.90, 1.15, 0], corner, color=DARK, stroke_width=7)
        right_edge = Line(corner, [2.30, -2.15, 0], color=DARK, stroke_width=7)
        c = 1.70
        a = corner + LEFT*c
        b = corner + DOWN*c
        removed = Polygon(
            a, corner, b,
            fill_color=REMOVE, fill_opacity=0.22,
            stroke_color=REMOVE, stroke_width=1.6,
        )
        cut = Line(a, b, color=VALID, stroke_width=9)
        da = DoubleArrow(
            a+DOWN*0.52, corner+DOWN*0.52, buff=0,
            color=SKETCH, stroke_width=2.5,
        )
        db = DoubleArrow(
            corner+RIGHT*0.52, b+RIGHT*0.52, buff=0,
            color=SKETCH, stroke_width=2.5,
        )
        # QA V4: reserve label above horizontal dimension, so it cannot cross
        # the diagonal cut line. Vertical label remains outside the part.
        la = self.text("6 mm", 29, BOLD, SKETCH).next_to(da, UP, buff=0.05)
        lb = self.text("6 mm", 31, BOLD, SKETCH).rotate(PI/2).next_to(db, RIGHT, buff=0.09)
        angle = Arc(
            radius=0.64, start_angle=3*PI/4, angle=PI/4,
            arc_center=a, color=SKETCH, stroke_width=3.5,
        )
        angle_lab = self.text("45°", 30, BOLD, SKETCH).move_to(a+RIGHT*0.72+UP*0.44)
        detail = self.small_callout(
            "DETAIL A · CORNER", DARK,
            point=[-2.70, 2.20, 0], width=4.55,
        )

        self.play(Create(top_edge), Create(right_edge), FadeIn(detail), run_time=0.95)
        self.play(FadeIn(removed), run_time=0.50)
        self.play(Create(da), Write(la), run_time=0.80)
        self.play(Create(db), Write(lb), run_time=0.80)
        self.play(Create(cut), run_time=1.15, rate_func=smooth)
        self.play(Create(angle), Write(angle_lab), run_time=0.70)
        note = self.note(
            "PASO 5 · Antes de OK, verifica visualmente 6 mm y 45° en la esquina.",
            VALID,
        )
        self.wait(2.05)
        self.clear_fixed(note)
        self.clear_fixed(detail, 0.25)
        return VGroup(top_edge, right_edge, removed, cut, da, db, la, lb, angle, angle_lab)
