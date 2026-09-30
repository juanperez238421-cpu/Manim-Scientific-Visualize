#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAI generated image asset -> JP Classroom ManimCE demonstration.

The PNG is a real OpenAI-generated asset from the current project workflow.
All instructional overlays remain native Manim objects so they can be animated,
edited, restyled, and reused independently of the raster asset.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
from manim import *

from jp_classroom_style import (
    JPMathClassroomScene,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_SUMMARY,
    PAUSE_FINAL,
)

ASSET_PATH = Path("assets/images/openai_inclined_plane_block_760_q55.webp")


class OpenAIAssetInclinedPlaneLesson(JPMathClassroomScene):
    """Professional 2D ManimCE lesson integrating an OpenAI-generated asset."""

    def validate_lesson_data(self) -> None:
        if not ASSET_PATH.exists():
            raise FileNotFoundError(ASSET_PATH)
        theta_deg = 30.0
        mass = 10.0
        g = 9.81
        expected_parallel = mass * g * np.sin(np.deg2rad(theta_deg))
        expected_perp = mass * g * np.cos(np.deg2rad(theta_deg))
        assert abs(expected_parallel - 49.05) < 1e-10
        assert abs(expected_perp - 84.95709226070895) < 1e-10

    def _asset(self, width: float = 6.55) -> ImageMobject:
        image = ImageMobject(str(ASSET_PATH))
        image.scale_to_fit_width(width)
        return image

    def _image_panel(
        self,
        image: ImageMobject,
        *,
        width: float,
        height: float,
        title: str | None = None,
        caption: str | None = None,
    ):
        """Raster-safe companion to the style library's figure panel.

        ImageMobject is a general Mobject rather than a VMobject in ManimCE.
        Group therefore provides the portable container while all typography,
        sizing, palette and layout rules still come from the exact JP style.
        """
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        title_mob = self.text(title, 25, BOLD) if title else None
        caption_mob = self.text(caption, 19) if caption else None

        available_h = height - 0.76
        if title_mob is not None:
            available_h -= 0.55
        if caption_mob is not None:
            available_h -= 0.48
        self.fit(image, width - 0.76, max(0.8, available_h))
        image.move_to(box)

        components = [box, image]
        if title_mob is not None:
            self.fit(title_mob, width - 0.55, 0.42)
            title_mob.next_to(box.get_top(), DOWN, buff=0.18)
            image.shift(DOWN * 0.18)
            components.append(title_mob)
        if caption_mob is not None:
            self.fit(caption_mob, width - 0.55, 0.40)
            caption_mob.next_to(box.get_bottom(), UP, buff=0.18)
            image.shift(UP * 0.12)
            components.append(caption_mob)

        return Group(*components), box, image, title_mob, caption_mob

    def _force_arrow(
        self,
        start: np.ndarray,
        direction: np.ndarray,
        length: float,
        label_tex: str,
        label_shift: np.ndarray,
        *,
        dashed: bool = False,
        stroke_width: float = 5.0,
    ) -> VGroup:
        unit = direction / np.linalg.norm(direction)
        end = start + unit * length
        arrow = Arrow(
            start=start,
            end=end,
            buff=0,
            color=BLACK_LINE,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.14,
        )
        if dashed:
            arrow.set_stroke(opacity=0.55)
        label = self.math(label_tex, 31)
        label.next_to(end, label_shift, buff=0.10)
        return VGroup(arrow, label)

    def construct(self) -> None:
        self.standard_opening(
            "PHYSICS • GENERATED ASSET PIPELINE",
            "FROM OPENAI IMAGE TO MANIMCE",
            "A reusable image becomes an editable animated scientific explanation",
            "Raster for the object. Native Manim for the reasoning.",
        )

        self.set_header(
            1,
            "THE GENERATED ASSET",
            "The OpenAI-generated PNG contains only the physical object; labels and mathematics stay native to ManimCE.",
        )

        asset = self._asset(7.20)
        panel_group, panel_box, panel_figure, panel_title, panel_caption = self._image_panel(
            asset,
            width=7.45,
            height=5.05,
            title="Reusable technical asset",
            caption="Transparent source • no baked text • no baked equations",
        )
        panel_group.move_to(LEFT * 3.55 + DOWN * 0.48)

        principles = self.note_panel(
            "ASSET CONTRACT",
            [
                "1. Generate the visual object once",
                "2. Keep explanations outside the image",
                "3. Animate every concept independently",
                "4. Reuse the same asset in many lessons",
            ],
            width=5.75,
            title_size=26,
            body_size=22,
            max_text_height=3.35,
        )
        principles.move_to(RIGHT * 3.70 + DOWN * 0.46)

        self.assert_content_safe(panel_group, "generated asset panel")
        self.assert_content_safe(principles, "asset contract panel")

        self.play(FadeIn(panel_box), run_time=RUN_QUICK)
        self.play(FadeIn(panel_figure, shift=UP * 0.12), run_time=RUN_SLOW)
        if panel_title is not None:
            self.play(FadeIn(panel_title), run_time=RUN_NORMAL)
        if panel_caption is not None:
            self.play(FadeIn(panel_caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(principles, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        self.clear_stage(keep_header=True)
        self.set_header(
            2,
            "NATIVE MANIM ANNOTATIONS",
            "Vectors remain mathematical objects: they can grow, transform, fade, relabel and participate in later derivations.",
        )

        asset2 = self._asset(7.65)
        asset2.move_to(LEFT * 3.25 + DOWN * 0.60)
        image_box = RoundedRectangle(
            width=8.05,
            height=5.20,
            corner_radius=0.12,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(asset2)

        block_center = LEFT * 3.35 + UP * 0.17
        downhill = np.array([1.0, -0.46, 0.0])
        uphill_normal = np.array([0.46, 1.0, 0.0])

        weight = self._force_arrow(block_center, DOWN, 1.72, r"\vec{W}=m\vec{g}", RIGHT)
        normal = self._force_arrow(block_center, uphill_normal, 1.58, r"\vec{N}", UR)
        parallel = self._force_arrow(block_center, downhill, 1.82, r"\vec{W}_{\parallel}", DR)
        perp = self._force_arrow(
            block_center,
            -uphill_normal,
            1.48,
            r"\vec{W}_{\perp}",
            LEFT,
            dashed=True,
            stroke_width=4.0,
        )

        angle_origin = LEFT * 6.02 + DOWN * 2.14
        angle_base = Line(angle_origin, angle_origin + RIGHT * 1.20, color=MID_GRAY, stroke_width=2)
        slope_dir = UP * 0.46 + RIGHT
        slope_dir = slope_dir / np.linalg.norm(slope_dir)
        angle_slope = Line(angle_origin, angle_origin + slope_dir * 1.20, color=BLACK_LINE, stroke_width=2)
        angle_mark = Angle(angle_base, angle_slope, radius=0.42, color=BLACK_LINE, stroke_width=2)
        theta = self.math(r"\theta", 30).next_to(angle_mark, UR, buff=0.04)
        angle_group = VGroup(angle_base, angle_slope, angle_mark, theta)

        legend = self.key_value_panel(
            "EVERY OVERLAY IS EDITABLE",
            [
                ("Weight", r"\vec W"),
                ("Normal", r"\vec N"),
                ("Along plane", r"\vec W_{\parallel}"),
                ("Into plane", r"\vec W_{\perp}"),
            ],
            width=5.10,
            label_size=21,
            value_size=27,
        )
        legend.move_to(RIGHT * 4.45 + DOWN * 0.50)

        self.assert_content_safe(Group(image_box, asset2, weight, normal, parallel, perp, angle_group), "annotated generated asset")
        self.assert_content_safe(legend, "force legend")

        self.play(FadeIn(image_box), FadeIn(asset2), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(weight[0]), FadeIn(weight[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(normal[0]), FadeIn(normal[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Create(angle_base), Create(angle_slope), Create(angle_mark), FadeIn(theta), run_time=RUN_NORMAL)
        self.wait(PAUSE_SHORT)
        self.play(GrowArrow(parallel[0]), FadeIn(parallel[1]), run_time=RUN_NORMAL)
        self.play(GrowArrow(perp[0]), FadeIn(perp[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(legend, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        force_focus = VGroup(weight, normal, parallel, perp)
        self.focus_on(force_focus, width=5.6, pause=PAUSE_READ)

        self.clear_stage(keep_header=True)
        self.set_header(
            3,
            "THE IMAGE BECOMES A MATHEMATICAL MODEL",
            "The asset provides visual context; equations are generated, sequenced and transformed natively in ManimCE.",
        )

        asset3 = self._asset(5.85)
        left_group, left_box, left_figure, left_title, left_caption = self._image_panel(
            asset3,
            width=6.35,
            height=4.85,
            title="Visual context",
            caption="Same OpenAI-generated asset",
        )

        eq_stack = self.equation_stack(
            [
                r"W=mg",
                r"W_{\parallel}=W\sin\theta",
                r"W_{\perp}=W\cos\theta",
                r"N=W_{\perp}=mg\cos\theta",
            ],
            sizes=[42, 38, 38, 38],
            buff=0.34,
            max_width=6.10,
            max_height=3.55,
        )
        eq_box = RoundedRectangle(
            width=6.25,
            height=4.85,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=PAPER_GRAY,
            fill_opacity=1.0,
        )
        eq_title = self.text("Force decomposition", 26, BOLD)
        eq_title.next_to(eq_box.get_top(), DOWN, buff=0.20)
        eq_stack.move_to(eq_box).shift(DOWN * 0.18)
        right_panel = VGroup(eq_box, eq_title, eq_stack)

        self.fit(left_group, 6.35, 5.05)
        self.fit(right_panel, 6.35, 5.05)
        left_group.move_to(LEFT * 3.40 + DOWN * 0.52)
        right_panel.move_to(RIGHT * 3.40 + DOWN * 0.52)
        split_group = Group(left_group, right_panel)
        self.fit_content_zone(split_group, max_width=14.4, max_height=5.05)
        self.assert_content_safe(split_group, "image plus equation split layout")

        self.play(FadeIn(left_box), FadeIn(left_figure), run_time=RUN_NORMAL)
        if left_title is not None:
            self.play(FadeIn(left_title), run_time=RUN_QUICK)
        if left_caption is not None:
            self.play(FadeIn(left_caption), run_time=RUN_QUICK)
        self.play(FadeIn(eq_box), FadeIn(eq_title), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        for equation in eq_stack:
            self.play(Write(equation), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_EXPLAIN)

        self.clear_stage(keep_header=True)
        self.set_header(
            4,
            "QUICK NUMERICAL CHECK",
            "For m = 10 kg and θ = 30°, the same visual asset supports a complete worked example without regenerating the image.",
        )

        givens = self.key_value_panel(
            "GIVEN",
            [
                ("Mass", r"m=10\,\mathrm{kg}"),
                ("Angle", r"\theta=30^{\circ}"),
                ("Gravity", r"g=9.81\,\mathrm{m/s^2}"),
            ],
            width=5.20,
            label_size=22,
            value_size=28,
        )
        givens.move_to(LEFT * 4.25 + DOWN * 0.52)

        chain = self.equation_stack(
            [
                r"W=mg=(10)(9.81)=98.1\,\mathrm{N}",
                r"W_{\parallel}=98.1\sin 30^{\circ}=49.05\,\mathrm{N}",
                r"W_{\perp}=98.1\cos 30^{\circ}\approx84.96\,\mathrm{N}",
                r"N\approx84.96\,\mathrm{N}",
            ],
            sizes=[33, 32, 32, 35],
            buff=0.34,
            max_width=7.90,
            max_height=4.20,
        )
        result_box = RoundedRectangle(
            width=8.15,
            height=4.72,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        chain.move_to(result_box)
        result = VGroup(result_box, chain).move_to(RIGHT * 3.30 + DOWN * 0.52)

        self.assert_content_safe(givens, "given data panel")
        self.assert_content_safe(result, "numerical calculation panel")

        self.play(FadeIn(givens, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(result_box), run_time=RUN_NORMAL)
        for line in chain:
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_SUMMARY)

        self.standard_closing(
            "Generate the asset once — animate the science, mathematics and narrative in ManimCE."
        )
