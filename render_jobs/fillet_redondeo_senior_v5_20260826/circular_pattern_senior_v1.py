from __future__ import annotations

import math
import numpy as np
from manim import *

from pattern_senior_base import *


class InventorCircularPatternSeniorV1(InventorPatternSeniorBase):
    """Full senior lesson: one Hole1 seed -> full 360-degree circular pattern."""

    OPERATION = "CIRCULAR PATTERN"
    SUBTITLE = "distribución asociativa alrededor de un eje"
    ROUTE = "SKETCH  →  EXTRUDE  →  HOLE1  →  ROTATION AXIS  →  QUANTITY  →  360° PATTERN"
    FEATURE_NAME = "CircularPattern1"

    DISK_R = 2.72
    RADIAL = 1.72
    N = 8

    def construct(self):
        self.opening("Una sola semilla se distribuye con precisión angular alrededor de un eje")
        hud = self.hud()

        self.phase_01_why_pattern(hud)
        disk = self.phase_02_base_feature(hud)
        seed = self.phase_03_seed_hole(hud)
        tree, card, axis = self.phase_04_select_axis(hud)
        preview = self.phase_05_full_placement(hud, seed)
        final_holes = self.phase_06_commit_pattern(hud, seed, preview)
        self.phase_07_angle_logic(hud)
        self.phase_08_validate_axis_radius(hud, axis)
        self.phase_09_partial_vs_full(hud, final_holes)
        self.phase_10_parametric_edit(hud, final_holes)

        self.play(FadeOut(axis), run_time=0.35)
        self.clear_fixed(tree, 0.30)
        self.clear_fixed(card, 0.30)
        model = VGroup(disk, final_holes)
        self.finish_summary(
            hud,
            "CircularPattern1 = una semilla + un eje estable + distribución angular editable.",
            [
                "CIRCULAR PATTERN — método reproducible",
                "1. Modela una sola feature semilla (Hole1).",
                "2. Selecciona un Rotation Axis estable, normalmente Origin → Z Axis.",
                "3. Define Placement, Quantity y ángulo total.",
                "4. Valida radio de la semilla, sentido y separación entre ocurrencias.",
                "5. Edita CircularPattern1: todas las copias se recalculan automáticamente.",
            ],
            model,
        )

    def phase_01_why_pattern(self, hud):
        self.set_phase(hud, 1, "¿POR QUÉ USAR PATTERN?", DARK)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.02)

        ring = Circle(radius=2.15, color=LIGHT, stroke_width=2.5)
        seed = Circle(radius=0.25, color=SKETCH, stroke_width=6).move_to([2.15, 0, 0])
        ghosts = VGroup()
        for k in range(1, self.N):
            a = k * TAU / self.N
            ghosts.add(Circle(radius=0.25, color=LIGHT, stroke_width=3).move_to([2.15*math.cos(a), 2.15*math.sin(a), 0]))
        call = self.small_callout("1 FEATURE SEMILLA", SKETCH, point=[-3.95, -1.80, 0], width=4.05)
        arrow = Arrow(call.get_right(), seed.get_left(), buff=0.18, color=SKETCH, stroke_width=2.2)
        self.fixed(arrow)
        manual = self.small_callout("NO: dibujar 8 agujeros", REMOVE, point=[4.05, -1.80, 0], width=4.55)

        self.play(Create(ring), Create(seed), run_time=0.85)
        self.play(FadeIn(call), GrowArrow(arrow), run_time=0.70)
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.09), run_time=1.30)
        self.play(FadeIn(manual), run_time=0.65)
        note = self.note("Circular Pattern repite la FEATURE; Quantity y Rotation Axis gobiernan toda la distribución.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(call, 0.20)
        self.clear_fixed(arrow, 0.20)
        self.clear_fixed(manual, 0.20)
        self.play(FadeOut(ring), FadeOut(seed), FadeOut(ghosts), run_time=0.55)

    def phase_02_base_feature(self, hud):
        self.set_phase(hud, 2, "SKETCH1 → EXTRUSION1", SKETCH)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=0.94)

        sketch = Circle(radius=self.DISK_R, color=SKETCH, stroke_width=5)
        center = Dot(ORIGIN, radius=0.06, color=SKETCH)
        hline = Line(LEFT*self.DISK_R, RIGHT*self.DISK_R, color=LIGHT, stroke_width=1.3)
        vline = Line(DOWN*self.DISK_R, UP*self.DISK_R, color=LIGHT, stroke_width=1.3)
        self.play(Create(sketch), FadeIn(center), Create(hline), Create(vline), run_time=1.05)
        note = self.note("Sketch1: círculo Ø 90 mm con centro coincidente con el origen.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)

        self.move_camera(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=0.88, run_time=1.15)
        disk = Cylinder(
            radius=self.DISK_R,
            height=self.BASE_H,
            direction=OUT,
            fill_color=STEEL,
            fill_opacity=0.94,
            stroke_color=DARK,
            stroke_width=0.8,
            resolution=(36, 18),
        ).move_to([0, 0, self.BASE_H/2])
        self.play(FadeOut(sketch), FadeOut(center), FadeOut(hline), FadeOut(vline), FadeIn(disk), run_time=0.95)
        note = self.note("Finish Sketch → Extrude 8 mm → Extrusion1. El eje Z permanece como referencia robusta.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return disk

    def phase_03_seed_hole(self, hud):
        self.set_phase(hud, 3, "SKETCH2 → HOLE1", SKETCH)
        xy = np.array([self.RADIAL, 0.0])
        circle = self.top_circle(xy, radius=0.25)
        radial_line = Line(
            [0, 0, self.BASE_H + 0.015],
            [xy[0], xy[1], self.BASE_H + 0.015],
            color=SKETCH,
            stroke_width=2.4,
        )
        self.play(Create(radial_line), Create(circle), run_time=0.70)
        note = self.note("Sketch2: Point1 a un radio acotado desde el origen; esa distancia define el círculo patrón.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)

        hole = self.hole_void(xy, radius=0.25)
        self.play(FadeOut(circle), FadeOut(radial_line), FadeIn(hole), run_time=0.70)
        note = self.note("Hole1: Ø 8 mm · Through All. Sólo se modela UNA ocurrencia antes de abrir Circular Pattern.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return hole

    def phase_04_select_axis(self, hud):
        self.set_phase(hud, 4, "FEATURE + ROTATION AXIS", DARK)
        tree = self.generic_feature_tree([
            ("Part1.ipt", DARK, BOLD),
            ("Origin", DARK, BOLD),
            ("  X Axis", MID, NORMAL),
            ("  Y Axis", MID, NORMAL),
            ("  Z Axis", SKETCH, BOLD),
            ("Sketch1", MID, NORMAL),
            ("Extrusion1", DARK, NORMAL),
            ("Hole1   Ø 8 mm", SKETCH, BOLD),
            ("CircularPattern1", VALID, BOLD),
        ])
        card = self.generic_parameter_card(
            "CIRCULAR PATTERN",
            [
                ("Features", "Hole1"),
                ("Rotation Axis", "Z Axis"),
                ("Placement", "Full"),
                ("Quantity", "8"),
                ("Angle", "360 deg"),
            ],
            center=(5.18, -0.10, 0),
            width=5.18,
        )
        axis = self.axis_arrow([0, 0, -0.70], [0, 0, 1.75], SKETCH)
        self.play(FadeIn(tree), FadeIn(card), Create(axis), run_time=0.90)
        note = self.note("3D Model → Pattern → Circular → Features: Hole1 → Rotation Axis: Origin / Z Axis.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return tree, card, axis

    def phase_05_full_placement(self, hud, seed):
        self.set_phase(hud, 5, "FULL · QUANTITY = 8", SKETCH)
        preview = VGroup()
        for k in range(1, self.N):
            a = k * TAU / self.N
            preview.add(self.preview_hole([self.RADIAL*math.cos(a), self.RADIAL*math.sin(a)]))
        self.play(LaggedStart(*[FadeIn(h) for h in preview], lag_ratio=0.10), run_time=1.40)
        note = self.note("Placement = Full distribuye Quantity = 8 uniformemente alrededor de los 360°.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return preview

    def phase_06_commit_pattern(self, hud, seed, preview):
        self.set_phase(hud, 6, "PREVIEW → OK", VALID)
        finals = VGroup(seed)
        new_holes = VGroup()
        for k in range(1, self.N):
            a = k * TAU / self.N
            new_holes.add(self.hole_void([self.RADIAL*math.cos(a), self.RADIAL*math.sin(a)], radius=0.25))
        finals.add(*new_holes)
        self.play(FadeOut(preview), LaggedStart(*[FadeIn(h) for h in new_holes], lag_ratio=0.06), run_time=1.25)
        note = self.note("OK: CircularPattern1 queda en el árbol como UNA feature con ocho ocurrencias asociativas.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return finals

    def phase_07_angle_logic(self, hud):
        self.set_phase(hud, 7, "SEPARACIÓN ANGULAR", DARK)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.95, run_time=0.95)
        arc = Arc(radius=0.88, start_angle=0, angle=TAU/self.N, color=SKETCH, stroke_width=5)
        arc.shift(OUT * (self.BASE_H + 0.02))
        self.play(Create(arc), run_time=0.55)
        strip = self.formula_strip("INCREMENTO = 360° / 8 = 45° entre centros consecutivos", DARK)
        self.wait(OBSERVE)
        self.clear_fixed(strip)
        self.play(FadeOut(arc), run_time=0.30)

    def phase_08_validate_axis_radius(self, hud, axis):
        self.set_phase(hud, 8, "VALIDA EJE + RADIO", REMOVE)
        radius_line = Line(
            [0, 0, self.BASE_H + 0.02],
            [self.RADIAL, 0, self.BASE_H + 0.02],
            color=REMOVE,
            stroke_width=3.5,
        )
        self.play(Create(radius_line), run_time=0.55)
        warning = self.small_callout("RADIO DE HOLE1", REMOVE, point=[4.35, 1.35, 0], width=4.25)
        self.play(FadeIn(warning), run_time=0.55)
        note = self.note("Un eje desplazado cambia TODO el centro del patrón; un radio de semilla incorrecto se replica ocho veces.", REMOVE)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(warning, 0.25)
        self.play(FadeOut(radius_line), run_time=0.30)
        self.move_camera(phi=58 * DEGREES, theta=-48 * DEGREES, zoom=0.92, run_time=0.90)

    def phase_09_partial_vs_full(self, hud, final_holes):
        self.set_phase(hud, 9, "FULL VS ANGLE", DARK)
        half_arc = Arc(radius=2.15, start_angle=0, angle=PI, color=SKETCH, stroke_width=5)
        half_arc.shift(OUT * (self.BASE_H + 0.03))
        self.play(Create(half_arc), run_time=0.65)
        note = self.note("Full = 360°. Si eliges Angle = 180°, las ocurrencias sólo ocupan el sector especificado.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(half_arc), run_time=0.35)

    def phase_10_parametric_edit(self, hud, final_holes):
        self.set_phase(hud, 10, "EDICIÓN PARAMÉTRICA", VALID)
        preview6 = VGroup()
        for k in range(6):
            a = k * TAU / 6
            preview6.add(self.preview_hole([self.RADIAL*math.cos(a), self.RADIAL*math.sin(a)], opacity=0.58))
        note = self.note("Edit Feature: Quantity cambia 8 → 6; el incremento se recalcula automáticamente a 60°.", VALID)
        self.play(final_holes.animate.set_opacity(0.20), LaggedStart(*[FadeIn(h) for h in preview6], lag_ratio=0.08), run_time=1.10)
        self.wait(OBSERVE)
        self.play(FadeOut(preview6), final_holes.animate.set_opacity(1.0), run_time=0.75)
        self.clear_fixed(note)
        note2 = self.note("Restauramos Quantity = 8: CircularPattern1 vuelve a 45° entre ocurrencias sin redibujar Hole1.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note2)
