from __future__ import annotations

import numpy as np
from manim import *

from pattern_senior_base import *


class InventorRectangularPatternSeniorV1(InventorPatternSeniorBase):
    """Full senior lesson: one Hole1 seed -> two-direction rectangular pattern."""

    OPERATION = "RECTANGULAR PATTERN"
    SUBTITLE = "matriz asociativa en dos direcciones"
    ROUTE = "SKETCH  →  EXTRUDE  →  HOLE1  →  DIRECTION 1  →  DIRECTION 2  →  PATTERN"
    FEATURE_NAME = "RectangularPattern1"

    NX = 4
    NY = 3
    DX = 1.22
    DY = 1.05
    SEED = np.array([-1.85, -1.12])

    def construct(self):
        self.opening("Una sola operación semilla controla toda una matriz 3D")
        hud = self.hud()

        self.phase_01_why_pattern(hud)
        plate = self.phase_02_base_feature(hud)
        seed = self.phase_03_seed_hole(hud, plate)
        tree, card = self.phase_04_select_feature(hud)
        row_preview, arrow_x = self.phase_05_direction_one(hud, seed)
        grid_preview, arrow_y = self.phase_06_direction_two(hud, seed, row_preview)
        final_holes = self.phase_07_commit_pattern(hud, seed, grid_preview, row_preview, arrow_x, arrow_y)
        self.phase_08_count_logic(hud)
        self.phase_09_validate_edges(hud, final_holes)
        self.phase_10_parametric_edit(hud, final_holes)

        self.clear_fixed(tree, 0.30)
        self.clear_fixed(card, 0.30)
        model = VGroup(plate, final_holes)
        self.finish_summary(
            hud,
            "RectangularPattern1 = una semilla + dos direcciones + parámetros editables.",
            [
                "RECTANGULAR PATTERN — método reproducible",
                "1. Modela una sola feature semilla (Hole1).",
                "2. Selecciona Direction 1 y define Quantity + Spacing.",
                "3. Activa Direction 2 y define su propia matriz.",
                "4. Valida bordes, colisiones y sentido de las flechas.",
                "5. Edita RectangularPattern1: todas las ocurrencias se regeneran.",
            ],
            model,
        )

    def phase_01_why_pattern(self, hud):
        self.set_phase(hud, 1, "¿POR QUÉ USAR PATTERN?", DARK)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.02)

        seed = Circle(radius=0.27, color=SKETCH, stroke_width=6).move_to([-2.6, 0.7, 0])
        seed_label = self.small_callout("1 FEATURE SEMILLA", SKETCH, point=[-2.55, -1.15, 0], width=4.15)
        arrow = Arrow(seed_label.get_top(), seed.get_bottom(), buff=0.12, color=SKETCH, stroke_width=2.2)
        self.fixed(arrow)

        ghosts = VGroup()
        for j in range(3):
            for i in range(4):
                if i == 0 and j == 0:
                    continue
                ghosts.add(Circle(radius=0.27, color=LIGHT, stroke_width=3).move_to([-2.6 + i*1.25, 0.7 + j*0.88, 0]))

        manual = self.small_callout("NO: dibujar 12 perfiles a mano", REMOVE, point=[3.5, -1.18, 0], width=5.15)
        self.play(Create(seed), FadeIn(seed_label), GrowArrow(arrow), run_time=0.95)
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.08), run_time=1.35)
        self.play(FadeIn(manual), run_time=0.65)
        note = self.note("Pattern repite la FEATURE completa: una edición de Hole1 actualiza todas las ocurrencias.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(seed_label, 0.20)
        self.clear_fixed(arrow, 0.20)
        self.clear_fixed(manual, 0.20)
        self.play(FadeOut(seed), FadeOut(ghosts), run_time=0.55)

    def phase_02_base_feature(self, hud):
        self.set_phase(hud, 2, "SKETCH1 → EXTRUSION1", SKETCH)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=0.94)

        sketch = Rectangle(width=self.BASE_W, height=self.BASE_D, color=SKETCH, stroke_width=5)
        hline = Line(LEFT * self.BASE_W/2, RIGHT * self.BASE_W/2, color=LIGHT, stroke_width=1.3)
        vline = Line(DOWN * self.BASE_D/2, UP * self.BASE_D/2, color=LIGHT, stroke_width=1.3)
        self.play(Create(sketch), Create(hline), Create(vline), run_time=1.05)
        note = self.note("Sketch1: rectángulo totalmente restringido 110 mm × 60 mm.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)

        self.move_camera(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=0.88, run_time=1.15)
        plate = self.base_plate()
        self.play(FadeOut(sketch), FadeOut(hline), FadeOut(vline), FadeIn(plate), run_time=0.95)
        note = self.note("Finish Sketch → Extrude 8 mm → Extrusion1.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return plate

    def phase_03_seed_hole(self, hud, plate):
        self.set_phase(hud, 3, "SKETCH2 → HOLE1", SKETCH)
        self.move_camera(phi=58 * DEGREES, theta=-48 * DEGREES, zoom=0.92, run_time=0.85)

        xy = self.SEED
        circle = self.top_circle(xy, radius=0.25)
        center = Dot3D([xy[0], xy[1], self.BASE_H + 0.02], radius=0.055, color=SKETCH)
        self.play(Create(circle), FadeIn(center), run_time=0.65)
        note = self.note("Sketch2: un solo Point1 acotado desde referencias estables.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)

        hole = self.hole_void(xy, radius=0.25)
        self.play(FadeOut(circle), FadeOut(center), FadeIn(hole), run_time=0.70)
        note = self.note("Hole1: Ø 8 mm · Through All. Ésta es la ÚNICA semilla del patrón.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return hole

    def phase_04_select_feature(self, hud):
        self.set_phase(hud, 4, "SELECCIONA LA SEMILLA", DARK)
        tree = self.generic_feature_tree([
            ("Part1.ipt", DARK, BOLD),
            ("Origin", MID, NORMAL),
            ("Sketch1", MID, NORMAL),
            ("Extrusion1", DARK, NORMAL),
            ("Sketch2", MID, NORMAL),
            ("Hole1   Ø 8 mm", SKETCH, BOLD),
            ("RectangularPattern1", VALID, BOLD),
        ])
        card = self.generic_parameter_card(
            "RECTANGULAR PATTERN",
            [
                ("Features", "Hole1"),
                ("Direction 1", "X Axis"),
                ("Quantity 1", "4"),
                ("Spacing 1", "25 mm"),
                ("Direction 2", "Y Axis"),
                ("Quantity 2", "3"),
                ("Spacing 2", "18 mm"),
            ],
            center=(5.18, -0.10, 0),
            width=5.18,
        )
        self.play(FadeIn(tree), FadeIn(card), run_time=0.85)
        note = self.note("3D Model → Pattern → Rectangular → Features: selecciona Hole1, no Sketch2.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return tree, card

    def phase_05_direction_one(self, hud, seed):
        self.set_phase(hud, 5, "DIRECTION 1 · X AXIS", SKETCH)
        x0, y0 = self.SEED
        arrow = self.axis_arrow(
            [x0 - 0.15, y0 - 0.62, self.BASE_H + 0.20],
            [2.25, y0 - 0.62, self.BASE_H + 0.20],
            SKETCH,
        )
        self.play(Create(arrow), run_time=0.60)

        previews = VGroup()
        for i in range(1, self.NX):
            previews.add(self.preview_hole([x0 + i*self.DX, y0]))
        self.play(LaggedStart(*[FadeIn(p) for p in previews], lag_ratio=0.18), run_time=1.20)
        note = self.note("Direction 1: X Axis · Quantity = 4 · Spacing = 25 mm (centro a centro).", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return previews, arrow

    def phase_06_direction_two(self, hud, seed, row_preview):
        self.set_phase(hud, 6, "DIRECTION 2 · Y AXIS", SKETCH)
        x0, y0 = self.SEED
        arrow = self.axis_arrow(
            [x0 - 0.62, y0 - 0.10, self.BASE_H + 0.20],
            [x0 - 0.62, 1.55, self.BASE_H + 0.20],
            SKETCH,
        )
        self.play(Create(arrow), run_time=0.60)

        previews = VGroup()
        for j in range(1, self.NY):
            for i in range(self.NX):
                previews.add(self.preview_hole([x0 + i*self.DX, y0 + j*self.DY]))
        self.play(LaggedStart(*[FadeIn(p) for p in previews], lag_ratio=0.08), run_time=1.45)
        note = self.note("Direction 2: Y Axis · Quantity = 3 · Spacing = 18 mm → aparece una matriz 4 × 3.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return previews, arrow

    def phase_07_commit_pattern(self, hud, seed, grid_preview, row_preview, arrow_x, arrow_y):
        self.set_phase(hud, 7, "PREVIEW → OK", VALID)
        x0, y0 = self.SEED
        finals = VGroup(seed)
        new_holes = VGroup()
        for j in range(self.NY):
            for i in range(self.NX):
                if i == 0 and j == 0:
                    continue
                new_holes.add(self.hole_void([x0 + i*self.DX, y0 + j*self.DY], radius=0.25))
        finals.add(*new_holes)
        self.play(
            FadeOut(row_preview), FadeOut(grid_preview), FadeOut(arrow_x), FadeOut(arrow_y),
            LaggedStart(*[FadeIn(h) for h in new_holes], lag_ratio=0.06),
            run_time=1.35,
        )
        note = self.note("OK: RectangularPattern1 se guarda como UNA operación paramétrica con 12 ocurrencias.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return finals

    def phase_08_count_logic(self, hud):
        self.set_phase(hud, 8, "LÓGICA DE CANTIDADES", DARK)
        strip = self.formula_strip("TOTAL = Quantity 1 × Quantity 2 = 4 × 3 = 12 ocurrencias", DARK)
        self.wait(OBSERVE)
        self.clear_fixed(strip)
        note = self.note("Quantity incluye la semilla. Inventor añade 11 copias; no 12 copias adicionales.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)

    def phase_09_validate_edges(self, hud, final_holes):
        self.set_phase(hud, 9, "VALIDA BORDES + COLISIONES", REMOVE)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.94, run_time=1.00)
        boundary = Rectangle(width=self.BASE_W, height=self.BASE_D, color=REMOVE, stroke_width=4)
        warning = self.small_callout("MARGEN AL BORDE", REMOVE, point=[4.65, 1.25, 0], width=4.25)
        edge_arrow = Arrow(warning.get_left(), [2.15, 1.0, 0], buff=0.15, color=REMOVE, stroke_width=2.2)
        self.fixed(edge_arrow)
        self.play(Create(boundary), FadeIn(warning), GrowArrow(edge_arrow), run_time=0.95)
        note = self.note("Antes de aceptar: revisa que ninguna ocurrencia salga de la cara o invada otra feature.", REMOVE)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(warning, 0.25)
        self.clear_fixed(edge_arrow, 0.25)
        self.play(FadeOut(boundary), run_time=0.35)
        self.move_camera(phi=58 * DEGREES, theta=-48 * DEGREES, zoom=0.92, run_time=0.90)

    def phase_10_parametric_edit(self, hud, final_holes):
        self.set_phase(hud, 10, "EDICIÓN PARAMÉTRICA", VALID)
        x0, y0 = self.SEED
        extra = VGroup(*[
            self.preview_hole([x0 + 4*self.DX, y0 + j*self.DY], opacity=0.58)
            for j in range(self.NY)
        ])
        note = self.note("Edit Feature: Quantity 1 cambia 4 → 5. No redibujes: el patrón se regenera.", VALID)
        self.play(LaggedStart(*[FadeIn(h) for h in extra], lag_ratio=0.14), run_time=1.05)
        self.wait(OBSERVE)
        self.play(FadeOut(extra), run_time=0.65)
        self.clear_fixed(note)
        note2 = self.note("Restauramos Quantity 1 = 4: RectangularPattern1 vuelve inmediatamente a 12 ocurrencias.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note2)
