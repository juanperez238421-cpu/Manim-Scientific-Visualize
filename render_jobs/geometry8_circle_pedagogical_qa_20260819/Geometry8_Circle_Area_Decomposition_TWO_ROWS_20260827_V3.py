#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle area derivation V3: TWO ROWS -> INTERLOCK -> A = pi r^2.

This refinement is intentionally aligned to the classroom explanation:

1. Cut the circle into equal sectors.
2. Separate alternating sectors into FILA 1 and FILA 2.
3. Before interlocking, show explicitly for EACH row:
      radial depth = r
      curved-edge total = perimeter / 2 = pi r
4. Interlock the two rows with a clean vertical motion (no crossing fan effect).
5. Show why the final height is r, not 2r: both rows occupy the SAME vertical band.
6. Show that the final base is one half of the circumference, not the sum of both rows.
7. Pass to the limiting almost-rectangle and derive A = pi r^2.

Target: Manim Community Edition 0.20.1, white classroom background,
projector-safe 16:9, 1920x1080 @ 30 fps for -pqh.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827_V2 import (  # noqa: E402
    Geometry8CircleAreaDecomposition20260827V2,
)
from Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827 import (  # noqa: E402
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER,
)


class Geometry8CircleAreaTwoRows20260827V3(Geometry8CircleAreaDecomposition20260827V2):
    """Classroom-aligned two-row derivation with controlled interlocking motion."""

    # ------------------------------------------------------------------
    # Geometry helpers dedicated to the two-row explanation
    # ------------------------------------------------------------------
    def two_row_targets(
        self,
        n: int,
        r: float,
        top_pivot_y: float = 0.52,
        bottom_pivot_y: float = -0.52,
        center_x: float = 0.0,
    ) -> VGroup:
        """Alternating sectors in two clean horizontal rows.

        Even sectors form FILA 1. Odd sectors form FILA 2.  The x positions are
        already the final interlocking x positions; therefore the later merge is
        essentially vertical and remains visually clean throughout the animation.
        """
        delta = TAU / n
        dx = PI * r / n
        targets = VGroup()
        for i in range(n):
            x = center_x + (i - (n - 1) / 2) * dx
            if i % 2 == 0:
                pivot = np.array([x, top_pivot_y, 0.0])
                start = PI / 2 - delta / 2
                fill = VERY_LIGHT_GRAY
            else:
                pivot = np.array([x, bottom_pivot_y, 0.0])
                start = -PI / 2 - delta / 2
                fill = WHITE
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=start,
                stroke_color=BLACK,
                stroke_width=1.25,
                fill_color=fill,
                fill_opacity=1,
            )
            sec.shift(pivot)
            targets.add(sec)
        return targets

    def row_boundary_arcs(
        self,
        n: int,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
        center_x: float = 0.0,
    ) -> tuple[VGroup, VGroup]:
        """Overlay the curved edges whose sums are P/2 for each row."""
        delta = TAU / n
        dx = PI * r / n
        top = VGroup()
        bottom = VGroup()
        for i in range(n):
            x = center_x + (i - (n - 1) / 2) * dx
            if i % 2 == 0:
                pivot = np.array([x, top_pivot_y, 0.0])
                arc = Arc(
                    radius=r,
                    start_angle=PI / 2 - delta / 2,
                    angle=delta,
                    color=BLACK,
                    stroke_width=6,
                ).move_arc_center_to(pivot)
                top.add(arc)
            else:
                pivot = np.array([x, bottom_pivot_y, 0.0])
                arc = Arc(
                    radius=r,
                    start_angle=-PI / 2 - delta / 2,
                    angle=delta,
                    color=MID_GRAY,
                    stroke_width=6,
                ).move_arc_center_to(pivot)
                bottom.add(arc)
        return top, bottom

    def row_measurements(
        self,
        rows: VGroup,
        r: float,
        top_pivot_y: float,
        bottom_pivot_y: float,
    ) -> VGroup:
        x0 = rows.get_left()[0]
        x1 = rows.get_right()[0]
        top_y = top_pivot_y + r
        bottom_y = bottom_pivot_y - r
        # Curved-edge totals are shown as horizontal measurement guides.
        top_base = DoubleArrow(
            [x0, top_y + 0.27, 0], [x1, top_y + 0.27, 0],
            color=BLACK, buff=0.02, tip_length=0.11, stroke_width=2.4,
        )
        top_base_lab = self.math(r"\frac{P}{2}=\pi r", 34).next_to(top_base, UP, buff=0.08)
        bottom_base = DoubleArrow(
            [x0, bottom_y - 0.27, 0], [x1, bottom_y - 0.27, 0],
            color=MID_GRAY, buff=0.02, tip_length=0.11, stroke_width=2.4,
        )
        bottom_base_lab = self.math(r"\frac{P}{2}=\pi r", 34).next_to(bottom_base, DOWN, buff=0.08)

        xh = x1 + 0.48
        top_h = DoubleArrow(
            [xh, top_pivot_y, 0], [xh, top_y, 0],
            color=BLACK, buff=0.02, tip_length=0.11, stroke_width=2.4,
        )
        top_h_lab = self.math("r", 38).next_to(top_h, RIGHT, buff=0.10)
        bottom_h = DoubleArrow(
            [xh, bottom_y, 0], [xh, bottom_pivot_y, 0],
            color=MID_GRAY, buff=0.02, tip_length=0.11, stroke_width=2.4,
        )
        bottom_h_lab = self.math("r", 38).next_to(bottom_h, RIGHT, buff=0.10)

        return VGroup(
            top_base, top_base_lab, bottom_base, bottom_base_lab,
            top_h, top_h_lab, bottom_h, bottom_h_lab,
        )

    def final_row_arc_overlays(self, n: int, r: float, center_y: float = -0.08) -> tuple[VGroup, VGroup]:
        """Highlight the final top and bottom boundaries by row ownership."""
        delta = TAU / n
        dx = PI * r / n
        top = VGroup()
        bottom = VGroup()
        for i in range(n):
            x = (i - (n - 1) / 2) * dx
            if i % 2 == 0:
                pivot = np.array([x, center_y - r / 2, 0.0])
                top.add(
                    Arc(
                        radius=r,
                        start_angle=PI / 2 - delta / 2,
                        angle=delta,
                        color=BLACK,
                        stroke_width=6,
                    ).move_arc_center_to(pivot)
                )
            else:
                pivot = np.array([x, center_y + r / 2, 0.0])
                bottom.add(
                    Arc(
                        radius=r,
                        start_angle=-PI / 2 - delta / 2,
                        angle=delta,
                        color=MID_GRAY,
                        stroke_width=6,
                    ).move_arc_center_to(pivot)
                )
        return top, bottom

    # ------------------------------------------------------------------
    # Revised lesson timeline
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening()
        self.step_1_circle()
        self.step_2_cut()
        self.step_3_two_rows()
        self.step_4_measure_rows()
        self.step_5_interlock_cleanly()
        self.step_6_shared_height()
        self.step_7_base_from_half_perimeter()
        self.step_8_limit_and_formula()
        self.closing_two_rows()

    def step_3_two_rows(self) -> None:
        h = self.header(
            3,
            "SEPARAMOS LOS SECTORES EN DOS FILAS",
            "Tomamos sectores alternos: la mitad forma FILA 1 y la otra mitad forma FILA 2.",
        )
        self.add(h)
        n, r = 24, 1.58
        source = self.sector_set(n, r, np.array([0.0, -0.12, 0.0]))
        outline = Circle(radius=r, color=BLACK, stroke_width=3).move_to([0.0, -0.12, 0.0])
        rows = self.two_row_targets(n, r)
        fila1 = self.text("FILA 1", 28, BOLD).move_to([-4.35, 1.32, 0])
        fila2 = self.text("FILA 2", 28, BOLD).move_to([-4.35, -1.32, 0])
        split_note = self.formula_panel(r"24\ \text{sectores}\;\longrightarrow\;12+12", 5.8, 38).move_to([4.65, -2.55, 0])

        self.assert_safe(VGroup(source, outline, rows, fila1, fila2, split_note, h), "v3 step3")
        self.play(Create(outline), LaggedStart(*[FadeIn(s) for s in source], lag_ratio=0.015), run_time=1.45)
        self.wait(1.1)
        self.play(FadeOut(outline), run_time=0.35)
        # All sectors move together; this avoids the visually noisy crossing fan of V2.
        self.play(
            AnimationGroup(*[Transform(s, t) for s, t in zip(source, rows)], lag_ratio=0.0),
            run_time=2.4,
            rate_func=smooth,
        )
        self.play(FadeIn(fila1, shift=RIGHT * 0.10), FadeIn(fila2, shift=RIGHT * 0.10), run_time=0.65)
        self.play(FadeIn(split_note, shift=UP * 0.08), run_time=0.65)
        self.wait(2.6)
        self.clear_stage(VGroup(source, fila1, fila2, split_note, h))

    def step_4_measure_rows(self) -> None:
        h = self.header(
            4,
            "MEDIMOS FILA 1 Y FILA 2 ANTES DE ENCAJAR",
            "En cada fila, la distancia radial es r y la suma de los arcos es la mitad del perímetro.",
        )
        self.add(h)
        n, r = 24, 1.48
        top_y, bottom_y = 0.50, -0.50
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        arcs_top, arcs_bottom = self.row_boundary_arcs(n, r, top_y, bottom_y)
        measures = self.row_measurements(rows, r, top_y, bottom_y)
        fila1 = self.text("FILA 1", 26, BOLD).move_to([-4.45, 1.18, 0])
        fila2 = self.text("FILA 2", 26, BOLD).move_to([-4.45, -1.18, 0])
        formula = self.formula_panel(
            r"P=2\pi r\quad\Rightarrow\quad\frac{P}{2}=\pi r",
            6.7,
            40,
        ).move_to([0.0, -3.15, 0])

        self.assert_safe(VGroup(rows, arcs_top, arcs_bottom, measures, fila1, fila2, formula, h), "v3 step4")
        self.play(FadeIn(rows), FadeIn(fila1), FadeIn(fila2), run_time=0.8)
        self.play(LaggedStart(*[Create(a) for a in arcs_top], lag_ratio=0.03), run_time=1.0)
        self.play(GrowFromCenter(measures[0]), Write(measures[1]), GrowFromCenter(measures[4]), Write(measures[5]), run_time=0.95)
        self.wait(1.25)
        self.play(LaggedStart(*[Create(a) for a in arcs_bottom], lag_ratio=0.03), run_time=1.0)
        self.play(GrowFromCenter(measures[2]), Write(measures[3]), GrowFromCenter(measures[6]), Write(measures[7]), run_time=0.95)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.7)
        self.wait(3.1)
        self.clear_stage(VGroup(rows, arcs_top, arcs_bottom, measures, fila1, fila2, formula, h))

    def step_5_interlock_cleanly(self) -> None:
        h = self.header(
            5,
            "ENCAJAMOS LAS DOS FILAS",
            "FILA 1 baja y FILA 2 sube: sus puntas entran en los espacios de la fila opuesta.",
        )
        self.add(h)
        n, r = 24, 1.72
        top_y, bottom_y = 0.48, -0.48
        rows = self.two_row_targets(n, r, top_y, bottom_y)
        target = self.strip_targets(n, r, center=np.array([0.0, -0.08, 0.0]))
        fila1 = self.text("FILA 1  ↓", 27, BOLD).move_to([-4.60, 1.32, 0])
        fila2 = self.text("FILA 2  ↑", 27, BOLD).move_to([-4.60, -1.32, 0])
        cue = self.text("MISMAS PIEZAS · MISMA ÁREA", 27, BOLD).move_to([0, -3.05, 0])

        self.assert_safe(VGroup(rows, target, fila1, fila2, cue, h), "v3 step5")
        self.play(FadeIn(rows), FadeIn(fila1), FadeIn(fila2), run_time=0.85)
        # Highlight one pair so the interlocking mechanism is readable.
        self.play(Indicate(rows[10], color=MID_GRAY, scale_factor=1.05), Indicate(rows[11], color=MID_GRAY, scale_factor=1.05), run_time=0.9)
        self.wait(0.6)
        # Critical refinement: all pieces move simultaneously to their final x position.
        self.play(
            AnimationGroup(*[Transform(s, t) for s, t in zip(rows, target)], lag_ratio=0.0),
            FadeOut(fila1),
            FadeOut(fila2),
            run_time=2.6,
            rate_func=smooth,
        )
        top_line = DashedLine([-3.25, 0.78, 0], [3.25, 0.78, 0], color=LIGHT_GRAY, dash_length=0.10)
        bottom_line = DashedLine([-3.25, -0.94, 0], [3.25, -0.94, 0], color=LIGHT_GRAY, dash_length=0.10)
        self.play(Create(top_line), Create(bottom_line), FadeIn(cue, shift=UP * 0.08), run_time=0.75)
        self.wait(3.0)
        self.clear_stage(VGroup(rows, top_line, bottom_line, cue, h))

    def step_6_shared_height(self) -> None:
        h = self.header(
            6,
            "LAS DOS FILAS COMPARTEN LA MISMA ALTURA r",
            "Cada sector mide r desde su punta hasta su arco; al encajarse, las filas no se apilan: ocupan la misma franja.",
        )
        self.add(h)
        n, r = 28, 1.82
        center_y = -0.10
        strip = self.strip_targets(n, r, center=np.array([0.0, center_y, 0.0]))
        top_y = center_y + r / 2
        bottom_y = center_y - r / 2
        top_line = DashedLine([-3.55, top_y, 0], [3.55, top_y, 0], color=MID_GRAY, dash_length=0.10)
        bottom_line = DashedLine([-3.55, bottom_y, 0], [3.55, bottom_y, 0], color=MID_GRAY, dash_length=0.10)

        # Two representative radial measurements, one from each row.
        even = 12
        odd = 15
        x_even = (even - (n - 1) / 2) * PI * r / n
        x_odd = (odd - (n - 1) / 2) * PI * r / n
        row1_r = DoubleArrow([x_even, bottom_y, 0], [x_even, top_y, 0], color=BLACK, buff=0.03, tip_length=0.10, stroke_width=2.5)
        row2_r = DoubleArrow([x_odd, top_y, 0], [x_odd, bottom_y, 0], color=MID_GRAY, buff=0.03, tip_length=0.10, stroke_width=2.5)
        row1_lab = self.text("FILA 1", 23, BOLD).next_to(row1_r, LEFT, buff=0.12)
        row2_lab = self.text("FILA 2", 23, BOLD).next_to(row2_r, RIGHT, buff=0.12)

        final_h = DoubleArrow([4.15, bottom_y, 0], [4.15, top_y, 0], color=BLACK, buff=0.03, tip_length=0.12, stroke_width=3)
        final_h_lab = self.math(r"\text{altura}=r", 39).next_to(final_h, RIGHT, buff=0.14)
        not_sum = self.formula_panel(r"\text{NO}\; r+r\qquad\text{SÍ}\; r", 6.2, 42).move_to([0.0, -2.75, 0])
        note = self.text("Las filas se INTERCALAN; no se colocan una encima de la otra.", 25, BOLD).move_to([0, 2.15, 0])

        self.assert_safe(VGroup(strip, top_line, bottom_line, row1_r, row2_r, row1_lab, row2_lab, final_h, final_h_lab, not_sum, note, h), "v3 step6")
        self.play(FadeIn(strip), Create(top_line), Create(bottom_line), run_time=0.9)
        self.play(GrowFromCenter(row1_r), FadeIn(row1_lab), run_time=0.75)
        self.play(GrowFromCenter(row2_r), FadeIn(row2_lab), run_time=0.75)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.65)
        self.wait(1.7)
        self.play(FadeOut(row1_r), FadeOut(row2_r), FadeOut(row1_lab), FadeOut(row2_lab), run_time=0.5)
        self.play(GrowFromCenter(final_h), Write(final_h_lab), FadeIn(not_sum, shift=UP * 0.08), run_time=0.9)
        self.wait(3.2)
        self.clear_stage(VGroup(strip, top_line, bottom_line, final_h, final_h_lab, not_sum, note, h))

    def step_7_base_from_half_perimeter(self) -> None:
        h = self.header(
            7,
            "LA BASE ES EL PERÍMETRO DIVIDIDO ENTRE 2",
            "Los arcos de FILA 1 forman el borde superior y los de FILA 2 el inferior; cada borde contiene P/2.",
        )
        self.add(h)
        n, r = 32, 1.78
        center_y = -0.05
        strip = self.strip_targets(n, r, center=np.array([0.0, center_y, 0.0]))
        top_arcs, bottom_arcs = self.final_row_arc_overlays(n, r, center_y)
        x0, x1 = strip.get_left()[0], strip.get_right()[0]
        base = DoubleArrow([x0, -1.34, 0], [x1, -1.34, 0], color=BLACK, buff=0.02, tip_length=0.12, stroke_width=2.8)
        base_lab = self.math(r"\text{base}=\frac{P}{2}=\pi r", 40).next_to(base, DOWN, buff=0.12)
        top_lab = self.math(r"\text{FILA 1}:\ \frac{P}{2}", 34).move_to([4.75, 1.15, 0])
        bottom_lab = self.math(r"\text{FILA 2}:\ \frac{P}{2}", 34).move_to([4.75, -0.15, 0])
        key = self.note_panel(
            "IMPORTANTE",
            ["La base NO es P/2 + P/2.", "Elegimos un borde del rectángulo:", "arriba o abajo, ambos miden P/2."],
            width=5.3,
        ).move_to([4.75, -2.35, 0])

        self.assert_safe(VGroup(strip, top_arcs, bottom_arcs, base, base_lab, top_lab, bottom_lab, key, h), "v3 step7")
        self.play(FadeIn(strip), run_time=0.8)
        self.play(LaggedStart(*[Create(a) for a in top_arcs], lag_ratio=0.025), Write(top_lab), run_time=1.15)
        self.wait(1.0)
        self.play(LaggedStart(*[Create(a) for a in bottom_arcs], lag_ratio=0.025), Write(bottom_lab), run_time=1.15)
        self.wait(1.0)
        self.play(GrowFromCenter(base), Write(base_lab), run_time=0.9)
        self.play(FadeIn(key, shift=UP * 0.08), run_time=0.7)
        self.wait(3.2)
        self.clear_stage(VGroup(strip, top_arcs, bottom_arcs, base, base_lab, top_lab, bottom_lab, key, h))

    def step_8_limit_and_formula(self) -> None:
        h = self.header(
            8,
            "MÁS SECTORES → BORDES MÁS RECTOS → RESULTADO EXACTO",
            "La reordenación conserva exactamente el área del círculo; en el límite, base = P/2 = pi r y altura = r.",
        )
        self.add(h)
        coarse = self.strip_targets(12, 1.45, center=np.array([-3.55, 0.55, 0]))
        fine = self.strip_targets(48, 1.45, center=np.array([3.05, 0.55, 0]))
        c_lab = self.text("12 sectores", 25, BOLD).next_to(coarse, UP, buff=0.20)
        f_lab = self.text("48 sectores", 25, BOLD).next_to(fine, UP, buff=0.20)
        arrow = Arrow([-0.55, 0.55, 0], [0.55, 0.55, 0], color=MID_GRAY, stroke_width=3, tip_length=0.18)
        more = self.text("más sectores", 22, BOLD).next_to(arrow, UP, buff=0.08)
        eq1 = self.formula_panel(r"A\approx\left(\frac{P}{2}\right)r", 5.5, 44).move_to([-3.25, -2.15, 0])
        eq2 = self.formula_panel(r"A=\left(\frac{2\pi r}{2}\right)r=\pi r^2", 6.4, 45).move_to([3.05, -2.15, 0])

        self.assert_safe(VGroup(coarse, fine, c_lab, f_lab, arrow, more, eq1, eq2, h), "v3 step8")
        self.play(FadeIn(coarse), FadeIn(c_lab), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(more), FadeIn(fine), FadeIn(f_lab), run_time=1.0)
        self.wait(1.8)
        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=0.75)
        self.wait(1.2)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=0.85)
        self.play(self.camera.frame.animate.set(width=8.1).move_to(eq2), run_time=0.9)
        self.wait(3.0)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=0.9)
        self.clear_stage(VGroup(coarse, fine, c_lab, f_lab, arrow, more, eq1, eq2, h))

    def closing_two_rows(self) -> None:
        title = self.text("RESUMEN — MÉTODO DE LAS DOS FILAS", 40, BOLD)
        steps = VGroup(
            self.text("1. Dividimos el círculo en sectores iguales.", 27),
            self.text("2. Separamos sectores alternos: FILA 1 y FILA 2.", 27),
            self.text("3. En cada fila: longitud radial = r y arcos = P/2 = πr.", 27),
            self.text("4. Encajamos las filas: comparten una sola altura r.", 27),
            self.text("5. Base = P/2 = πr; entonces A = (πr)(r).", 27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        formula = self.formula_panel(r"\boxed{A=\pi r^2}", 5.9, 56)
        g = VGroup(title, steps, formula).arrange(DOWN, buff=0.34)
        self.assert_safe(g, "v3 closing")
        self.play(Write(title), run_time=0.9)
        for line in steps:
            self.play(FadeIn(line, shift=RIGHT * 0.10), run_time=0.52)
            self.wait(0.45)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.9)
        self.wait(4.2)


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V3.py Geometry8CircleAreaTwoRows20260827V3 --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_Decomposition_TWO_ROWS_20260827_V3.py Geometry8CircleAreaTwoRows20260827V3 --disable_caching
