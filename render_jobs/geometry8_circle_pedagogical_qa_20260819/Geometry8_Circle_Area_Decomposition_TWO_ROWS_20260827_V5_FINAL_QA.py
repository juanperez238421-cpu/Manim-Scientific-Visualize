#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle area V5 FINAL QA.

Final micro-layout correction after inspecting the V4 PQH audit frames:
the FILA 2 label P/2 = pi r was too close to the summary formula panel.
This version preserves all V4 animation behavior and rebuilds Step 04 with
additional vertical clearance so both rows read cleanly at projector scale.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V4_POLISHED import (  # noqa: E402
    Geometry8CircleAreaTwoRows20260827V4Polished,
)


class Geometry8CircleAreaTwoRows20260827V5FinalQA(Geometry8CircleAreaTwoRows20260827V4Polished):
    """V4 polished lesson + final safe spacing for the two-row measurements."""

    def step_4_measure_rows(self) -> None:
        h = self.header(
            4,
            "MEDIMOS FILA 1 Y FILA 2 ANTES DE ENCAJAR",
            "En cada fila: la distancia radial mide r y la suma de sus arcos representa la mitad del perímetro.",
        )
        self.add(h)
        n, r = 24, 1.42
        top_y, bottom_y = 0.58, -0.36
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        arcs_top, arcs_bottom = self.row_boundary_arcs(n, r, top_y, bottom_y)
        measures = self.row_measurements(rows, r, top_y, bottom_y)

        fila1 = self.text("FILA 1", 28, BOLD).move_to([-4.45, 1.25, 0])
        fila2 = self.text("FILA 2", 28, BOLD).move_to([-4.45, -1.02, 0])

        # Lower and slightly smaller than V4 so the lower P/2 label remains
        # completely visible. The panel is still well inside the safe frame.
        formula = self.formula_panel(
            r"P=2\pi r\qquad\Rightarrow\qquad\frac{P}{2}=\pi r",
            6.6,
            40,
        ).move_to([0.0, -3.48, 0])

        self.assert_safe(
            VGroup(rows, arcs_top, arcs_bottom, measures, fila1, fila2, formula, h),
            "v5 step4 safe measurements",
        )

        self.play(FadeIn(rows), FadeIn(fila1), FadeIn(fila2), run_time=0.80)

        # FILA 1: first establish its curved-edge total and its radial depth r.
        self.play(
            LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.025),
            run_time=0.95,
        )
        self.play(
            GrowFromCenter(measures[0]),
            Write(measures[1]),
            GrowFromCenter(measures[4]),
            Write(measures[5]),
            run_time=0.95,
        )
        self.wait(1.25)

        # FILA 2: repeat exactly the same measurement logic.
        self.play(
            LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.025),
            run_time=0.95,
        )
        self.play(
            GrowFromCenter(measures[2]),
            Write(measures[3]),
            GrowFromCenter(measures[6]),
            Write(measures[7]),
            run_time=0.95,
        )
        self.wait(1.25)

        # Only after both rows are individually measured do we formalize P/2.
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.70)
        self.wait(3.0)
        self.clear_stage(VGroup(rows, arcs_top, arcs_bottom, measures, fila1, fila2, formula, h))


# Preview:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V5_FINAL_QA.py Geometry8CircleAreaTwoRows20260827V5FinalQA --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V5_FINAL_QA.py Geometry8CircleAreaTwoRows20260827V5FinalQA --disable_caching
