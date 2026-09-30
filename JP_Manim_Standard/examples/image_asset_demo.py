#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JP Manim Standard — generated image asset integration test."""

from pathlib import Path
from manim import *
from jp_manim_standard import *

ASSET = Path(__file__).resolve().parents[1] / "assets" / "generated" / "physics" / "inclined_plane_block_v1.png"


class GeneratedAssetInclinedPlaneDemo(JPMathClassroomScene):
    def construct(self):
        self.standard_opening(
            "PHYSICS / VISUAL ASSET TEST",
            "INCLINED PLANE",
            "Generated asset + dynamic ManimCE annotations",
            "The image provides the object; Manim provides the explanation.",
        )

        self.set_header(
            1,
            "GENERATED ASSET + NATIVE MANIM ANNOTATIONS",
            "Keep labels, equations, arrows and highlights editable as native Manim objects.",
        )

        asset = ImageMobject(str(ASSET))
        asset.scale_to_fit_width(6.3)
        asset.move_to(LEFT * 3.55 + DOWN * 0.35)

        panel_box = RoundedRectangle(
            width=6.8,
            height=5.05,
            corner_radius=0.12,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(asset)

        # Dynamic annotations: NEVER baked into the PNG.
        theta = self.math(r"\theta", 42).move_to(LEFT * 5.30 + DOWN * 2.15)
        slope_arrow = Arrow(
            start=LEFT * 5.0 + DOWN * 1.55,
            end=LEFT * 2.25 + UP * 0.25,
            buff=0,
            color=BLACK_LINE,
            stroke_width=4,
        )
        weight = Arrow(
            start=LEFT * 3.20 + UP * 0.35,
            end=LEFT * 3.20 + DOWN * 1.30,
            buff=0,
            color=BLACK_LINE,
            stroke_width=4,
        )
        weight_label = self.math(r"\vec{W}=m\vec{g}", 34).next_to(weight, RIGHT, buff=0.18)

        explanation = VGroup(
            self.formula_panel(r"W=mg", width=5.6, height=1.05, font_size=42),
            self.note_panel(
                "WHY THIS PIPELINE?",
                [
                    "Asset = reusable visual geometry",
                    "Manim = labels, forces and equations",
                    "One PNG supports many lessons",
                ],
                width=5.6,
                title_size=25,
                body_size=22,
            ),
        ).arrange(DOWN, buff=0.32)
        explanation.move_to(RIGHT * 3.65 + DOWN * 0.20)

        self.play(FadeIn(panel_box), FadeIn(asset), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(slope_arrow), FadeIn(theta), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(GrowArrow(weight), FadeIn(weight_label), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(explanation), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.standard_closing("Generate the object once. Explain it dynamically with ManimCE.")
