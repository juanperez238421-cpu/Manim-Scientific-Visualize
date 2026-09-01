#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Precision correction for the parallelogram cut-and-translate chapter.

The previous V4 geometry was mathematically congruent, but the final frame kept
piece outlines and the original base dimension in place. That created a visual
mismatch at the translated right triangle / rectangle boundary. This V5 layer
constructs every point parametrically from the same base, height, and shear,
uses one exact translation vector for all three corresponding vertices, and
rebuilds the final rectangle with a clean internal seam under the outer border.
"""
from __future__ import annotations

import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8ParallelogramPrecisionV5Mixin:
    """Override only the parallelogram chapter; all lesson content stays unchanged."""

    def parallelogram_explicit(self):
        h = self.header(
            7,
            "4 · PARALLELOGRAM",
            "A cut-and-translate preserves area and turns the slanted figure into a rectangle.",
        )
        strip = self.stage_strip()
        self.add(h, strip)

        # One parametric construction controls the original parallelogram,
        # the cut triangle, the target triangle, and the resulting rectangle.
        y0 = -1.35
        height = 2.70
        shear = 1.00
        base = 4.40

        A = np.array([-5.80, y0, 0.0])
        E = A + RIGHT * shear
        D = E + UP * height
        B = A + RIGHT * base
        F = E + RIGHT * base
        C = D + RIGHT * base

        translation = B - A
        # Senior geometry gate: all three triangle vertices use exactly the
        # same translation; therefore the source and target triangles are congruent.
        assert np.allclose(E + translation, F)
        assert np.allclose(D + translation, C)
        assert np.isclose(np.linalg.norm(D - E), np.linalg.norm(C - F))
        assert np.isclose(np.linalg.norm(E - A), np.linalg.norm(F - B))
        assert np.isclose(np.linalg.norm(D - A), np.linalg.norm(C - B))

        full = Polygon(
            A, B, C, D,
            stroke_color=INK,
            stroke_width=5,
            fill_color=FILL,
            fill_opacity=.66,
        )

        self.mark_stage(strip, 0)
        self.play(Create(full), run_time=.70)

        self.mark_stage(strip, 1)
        # Dimensions belong to the original parallelogram in this stage.
        db = self.dimension(A + DOWN*.35, B + DOWN*.35, "b", DOWN)
        alt = DashedLine(D, E, color=MID, stroke_width=3)
        dh = self.dimension(E + LEFT*.30, D + LEFT*.30, "h", LEFT)
        slanted = self.txt("slanted side ≠ height", 25, True).next_to(Line(A, D), LEFT, buff=.12)
        self.play(
            GrowFromCenter(db[0]), FadeIn(db[1]),
            Create(alt), GrowFromCenter(dh[0]), FadeIn(dh[1]), FadeIn(slanted),
            run_time=.78,
        )

        self.mark_stage(strip, 2)
        left_piece = Polygon(
            A, E, D,
            stroke_color=INK,
            stroke_width=4,
            fill_color=WHITE,
            fill_opacity=1,
        )
        remain = Polygon(
            E, B, C, D,
            stroke_color=INK,
            stroke_width=4,
            fill_color=FILL,
            fill_opacity=.66,
        )
        self.play(
            FadeOut(full), FadeIn(left_piece), FadeIn(remain), FadeOut(slanted),
            run_time=.42,
        )

        motion = Arrow(
            left_piece.get_center() + UP*1.80,
            left_piece.get_center() + UP*1.80 + translation,
            buff=.05,
            color=MID,
            stroke_width=3,
        )
        self.play(GrowArrow(motion), run_time=.35)
        # Exact translation: A→B, E→F, D→C. No rotation and no independent scaling.
        self.play(left_piece.animate.shift(translation), run_time=1.10, rate_func=smooth)

        # Once the triangle lands, remove doubled piece strokes before drawing the
        # exact rectangle. This prevents line-cap / overdraw artifacts that made the
        # right triangle appear slightly taller than the rectangle in V4.
        final_fill = Polygon(
            E, F, C, D,
            stroke_opacity=0,
            fill_color=FILL,
            fill_opacity=.66,
        )
        join = Line(B, C, color=INK, stroke_width=3.2)
        rect = Polygon(
            E, F, C, D,
            stroke_color=INK,
            stroke_width=5,
            fill_opacity=0,
        )

        self.play(
            FadeOut(motion),
            left_piece.animate.set_stroke(opacity=0),
            remain.animate.set_stroke(opacity=0),
            FadeIn(final_fill),
            run_time=.30,
        )
        self.play(Create(join), run_time=.28)
        # Draw the outer border last so it masks the diagonal's line caps exactly
        # at B and C and the translated triangle fits the rectangle visually.
        self.play(Create(rect), run_time=.40)

        # Move the base dimension to the rectangle itself. In V4 the old A→B
        # dimension stayed shifted left after the transformation.
        rect_db = self.dimension(E + DOWN*.35, F + DOWN*.35, "b", DOWN)
        self.play(
            FadeOut(db),
            GrowFromCenter(rect_db[0]),
            FadeIn(rect_db[1]),
            run_time=.38,
        )

        deriv = VGroup(
            self.txt("Same pieces → same area as a rectangle", 27, True),
            self.box(r"A=b\,h", 5.3, 62),
        ).arrange(DOWN, buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv), run_time=.55)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), run_time=.32)
        ex = self.example_stack(
            "Given: b = 7 cm, h = 4 cm",
            r"A=b\,h",
            r"A=(7)(4)",
            r"A=28\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80)
        self.wipe()
