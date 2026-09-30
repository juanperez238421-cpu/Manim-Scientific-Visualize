#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle area V4 POLISHED: classroom two-row method.

Polish pass over V3 after dense-frame QA:
- removes the inherited camera zoom that clipped the observation panel;
- makes the FILA 1 / FILA 2 mechanism the visual center of the lesson;
- animates one representative sector pair first, then the remaining pieces;
- keeps row measurements explicit: radial depth r and arc total P/2 for EACH row;
- keeps final height r and base P/2 visually separate;
- replaces the cluttered final camera zoom with a clean formula isolation.

Target: ManimCE 0.20.1, 1920x1080, 30 fps, white classroom style.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V3 import (  # noqa: E402
    Geometry8CircleAreaTwoRows20260827V3,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    MID_GRAY,
    LIGHT_GRAY,
)


class Geometry8CircleAreaTwoRows20260827V4Polished(Geometry8CircleAreaTwoRows20260827V3):
    """Final polished two-row derivation aligned to the classroom explanation."""

    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening()
        self.step_1_circle()
        self.step_2_cut_polished()
        self.step_3_two_rows()
        self.step_4_measure_rows()
        self.step_5_interlock_pair_first()
        self.step_6_shared_height()
        self.step_7_base_from_half_perimeter()
        self.step_8_limit_and_formula_polished()
        self.closing_two_rows()

    # ------------------------------------------------------------------
    # 02 — no camera clipping: one sector is highlighted in-place
    # ------------------------------------------------------------------
    def step_2_cut_polished(self) -> None:
        h = self.header(
            2,
            "DIVIDIMOS EL CÍRCULO EN SECTORES IGUALES",
            "Cada sector conserva el mismo radio r; solo cambia el ángulo del sector.",
        )
        self.add(h)
        n, r = 24, 2.00
        center = np.array([-2.75, -0.30, 0.0])
        outline = Circle(radius=r, color=BLACK, stroke_width=3).move_to(center)
        sectors = self.sector_set(n, r, center)
        radius = Line(center, center + RIGHT * r, color=BLACK, stroke_width=3)
        r_lab = self.math("r", 36).next_to(radius, UP, buff=0.08)
        count = self.formula_panel(r"24\ \text{sectores iguales}", 5.1, 38).move_to([3.55, 0.58, 0])
        note = self.note_panel(
            "OBSERVA",
            [
                "Todos los sectores van del centro al borde.",
                "Esa distancia radial siempre mide r.",
                "Juntos conservan exactamente el área del círculo.",
            ],
            width=5.7,
        ).move_to([3.55, -1.18, 0])
        one_label = self.text("UN SECTOR", 24, BOLD).move_to([-0.10, 1.90, 0])
        one_arrow = Arrow([-0.25, 1.72, 0], center + np.array([1.35, 1.18, 0]), color=MID_GRAY, stroke_width=2.2, tip_length=0.13)

        self.assert_safe(VGroup(outline, sectors, radius, r_lab, count, note, one_label, one_arrow, h), "v4 step2")
        self.play(Create(outline), run_time=0.75)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.020), run_time=1.55)
        self.play(Create(radius), Write(r_lab), FadeIn(count), run_time=0.75)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.70)
        self.wait(1.25)
        # No zoom: the class keeps the complete circle and explanation visible.
        self.play(Indicate(sectors[3], color=MID_GRAY, scale_factor=1.07), FadeIn(one_label), GrowArrow(one_arrow), run_time=0.95)
        self.wait(1.85)
        self.play(FadeOut(one_label), FadeOut(one_arrow), run_time=0.45)
        self.wait(0.65)
        self.clear_stage(VGroup(outline, sectors, radius, r_lab, count, note, h))

    # ------------------------------------------------------------------
    # 05 — demonstrate one pair first, then let all pairs follow
    # ------------------------------------------------------------------
    def step_5_interlock_pair_first(self) -> None:
        h = self.header(
            5,
            "ENCAJAMOS FILA 1 CON FILA 2",
            "Primero observamos una pareja: una pieza baja y la otra sube hasta ocupar el espacio opuesto.",
        )
        self.add(h)
        n, r = 24, 1.72
        top_y, bottom_y = 0.48, -0.48
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        targets = self.strip_targets(n, r, center=np.array([0.0, -0.08, 0.0]))
        fila1 = self.text("FILA 1  ↓", 28, BOLD).move_to([-4.60, 1.34, 0])
        fila2 = self.text("FILA 2  ↑", 28, BOLD).move_to([-4.60, -1.34, 0])
        pair_caption = self.text("1 pareja: así se intercalan", 25, BOLD).move_to([0.0, -2.55, 0])
        all_caption = self.text("AHORA REPETIMOS EL MISMO MOVIMIENTO CON TODAS LAS PIEZAS", 24, BOLD).move_to([0.0, -2.55, 0])
        conserved = self.text("MISMAS PIEZAS  ·  MISMA ÁREA", 28, BOLD).move_to([0.0, -2.95, 0])

        self.assert_safe(VGroup(rows, targets, fila1, fila2, pair_caption, all_caption, conserved, h), "v4 step5")
        self.play(FadeIn(rows), FadeIn(fila1), FadeIn(fila2), run_time=0.80)

        pair = (10, 11)
        self.play(
            Indicate(rows[pair[0]], color=MID_GRAY, scale_factor=1.08),
            Indicate(rows[pair[1]], color=MID_GRAY, scale_factor=1.08),
            FadeIn(pair_caption, shift=UP * 0.06),
            run_time=0.95,
        )
        self.wait(0.55)
        self.play(
            Transform(rows[pair[0]], targets[pair[0]]),
            Transform(rows[pair[1]], targets[pair[1]]),
            run_time=1.25,
            rate_func=smooth,
        )
        self.wait(0.70)
        self.play(Transform(pair_caption, all_caption), run_time=0.55)

        remaining = [i for i in range(n) if i not in pair]
        self.play(
            AnimationGroup(*[Transform(rows[i], targets[i]) for i in remaining], lag_ratio=0.0),
            FadeOut(fila1),
            FadeOut(fila2),
            run_time=2.35,
            rate_func=smooth,
        )
        self.play(FadeOut(pair_caption), run_time=0.35)

        top_line = DashedLine([-3.25, 0.78, 0], [3.25, 0.78, 0], color=LIGHT_GRAY, dash_length=0.10)
        bottom_line = DashedLine([-3.25, -0.94, 0], [3.25, -0.94, 0], color=LIGHT_GRAY, dash_length=0.10)
        self.play(Create(top_line), Create(bottom_line), FadeIn(conserved, shift=UP * 0.08), run_time=0.75)
        self.wait(2.65)
        self.clear_stage(VGroup(rows, top_line, bottom_line, conserved, h))

    # ------------------------------------------------------------------
    # 08 — isolate the final formula instead of zooming through leftovers
    # ------------------------------------------------------------------
    def step_8_limit_and_formula_polished(self) -> None:
        h = self.header(
            8,
            "MÁS SECTORES → BORDES MÁS RECTOS → RESULTADO EXACTO",
            "La reordenación conserva el área; en el límite, la base es P/2 = πr y la altura es r.",
        )
        self.add(h)
        coarse = self.strip_targets(12, 1.45, center=np.array([-3.55, 0.55, 0]))
        fine = self.strip_targets(48, 1.45, center=np.array([3.05, 0.55, 0]))
        c_lab = self.text("12 sectores", 26, BOLD).next_to(coarse, UP, buff=0.20)
        f_lab = self.text("48 sectores", 26, BOLD).next_to(fine, UP, buff=0.20)
        arrow = Arrow([-0.55, 0.55, 0], [0.55, 0.55, 0], color=MID_GRAY, stroke_width=3, tip_length=0.18)
        more = self.text("más sectores", 22, BOLD).next_to(arrow, UP, buff=0.08)
        eq1 = self.formula_panel(r"A\approx\left(\frac{P}{2}\right)r", 5.5, 45).move_to([-3.25, -2.15, 0])
        eq2 = self.formula_panel(r"A=\left(\frac{2\pi r}{2}\right)r=\pi r^2", 6.4, 46).move_to([3.05, -2.15, 0])

        self.assert_safe(VGroup(coarse, fine, c_lab, f_lab, arrow, more, eq1, eq2, h), "v4 step8")
        self.play(FadeIn(coarse), FadeIn(c_lab), run_time=0.75)
        self.play(GrowArrow(arrow), FadeIn(more), FadeIn(fine), FadeIn(f_lab), run_time=0.95)
        self.wait(1.55)
        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=0.70)
        self.wait(1.10)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=0.80)
        self.wait(1.45)

        # Clean isolation: no partial panels or clipped strips remain in frame.
        self.play(
            FadeOut(coarse), FadeOut(fine), FadeOut(c_lab), FadeOut(f_lab),
            FadeOut(arrow), FadeOut(more), FadeOut(eq1), FadeOut(h),
            run_time=0.75,
        )
        final_label = self.text("ÁREA DEL CÍRCULO", 34, BOLD).move_to([0.0, 1.18, 0])
        self.play(eq2.animate.move_to(ORIGIN).scale(1.18), FadeIn(final_label, shift=UP * 0.08), run_time=1.05)
        self.wait(3.25)
        self.clear_stage(VGroup(eq2, final_label))


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V4_POLISHED.py Geometry8CircleAreaTwoRows20260827V4Polished --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V4_POLISHED.py Geometry8CircleAreaTwoRows20260827V4Polished --disable_caching
