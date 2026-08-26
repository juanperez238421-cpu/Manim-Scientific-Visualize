from __future__ import annotations

import numpy as np
from manim import *

from hole_agujero_senior_v2 import (
    InventorHoleAgujeroSeniorV2,
    SKETCH, VALID, REMOVE, BOLD, smooth,
)


class InventorHoleAgujeroSeniorV3(InventorHoleAgujeroSeniorV2):
    """Final visual QA pass for Hole / Agujero.

    V3 fixes the only overlap detected in the rendered V2 24-frame audit:
    the Ø12 mm label intersected the circular preview. The diameter arrow remains
    through the center, while the text is reserved below the circle with explicit
    clearance.
    """

    def top_preview(self, hud, sketch2, card):
        self.set_phase(hud, 7, "PREVIEW · Ø12 mm", VALID)
        self.play(FadeOut(card), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(
            sketch2.animate.shift(RIGHT*(1.05+self.PANEL_CLEARANCE)),
            run_time=0.65,
            rate_func=smooth,
        )

        point = np.array([self.POINT_X, self.POINT_Y, 0])
        circle = Circle(radius=self.HOLE_R, color=VALID, stroke_width=8).move_to(point)
        dia = DoubleArrow(
            point+LEFT*self.HOLE_R,
            point+RIGHT*self.HOLE_R,
            buff=0,
            color=SKETCH,
            stroke_width=2.6,
        )
        # Senior V3 QA: label is anchored to the circle boundary rather than the
        # centerline arrow, guaranteeing clear separation from the preview.
        lab = self.text("Ø 12 mm", 31, BOLD, SKETCH).next_to(circle, DOWN, buff=0.25)
        red = Circle(
            radius=self.HOLE_R*0.90,
            fill_color=REMOVE,
            fill_opacity=0.12,
            stroke_width=0,
        ).move_to(point)

        self.play(FadeIn(red), run_time=0.40)
        self.play(Create(circle), run_time=0.95)
        self.play(Create(dia), run_time=0.55)
        self.play(Write(lab), run_time=0.55)
        note = self.note_big(
            "PASO 7 · El preview circular debe quedar centrado exactamente sobre Point1.",
            VALID,
        )
        self.wait(2.0)
        self.clear_fixed(note)
        self.play(FadeOut(VGroup(sketch2, red, circle, dia, lab)), run_time=0.45)
