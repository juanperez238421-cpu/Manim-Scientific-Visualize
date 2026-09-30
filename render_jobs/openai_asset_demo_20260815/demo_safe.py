#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from manim import *
from jp_classroom_style import *

ASSET = Path("assets/images/openai_inclined_plane.webp")


class OpenAIAssetSafeDemo(JPMathClassroomScene):
    def validate_lesson_data(self):
        if not ASSET.exists():
            raise FileNotFoundError(ASSET)
        m, g, theta = 10.0, 9.81, np.deg2rad(30.0)
        assert abs(m * g * np.sin(theta) - 49.05) < 1e-10

    def construct(self):
        self.standard_opening(
            "PHYSICS / OPENAI ASSET PIPELINE",
            "GENERATED IMAGE + MANIMCE",
            "One reusable visual asset; every explanation remains editable",
            "The image supplies context. Manim supplies the scientific reasoning.",
        )

        # SECTION 1 — generated object + native force annotations
        self.set_header(
            1,
            "FROM GENERATED ASSET TO PHYSICS DIAGRAM",
            "The OpenAI image remains a raster object while vectors, symbols and equations are native Manim elements.",
        )
        frame = RoundedRectangle(
            width=8.0, height=5.1, corner_radius=.12,
            stroke_color=LIGHT_GRAY, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(LEFT * 3.20 + DOWN * .55)
        img = ImageMobject(str(ASSET)).scale_to_fit_width(7.45)
        img.move_to(frame)
        self.play(FadeIn(frame), run_time=RUN_NORMAL)
        self.add(img)  # Raster stays static: never passed to FadeIn/FadeOut.
        self.wait(PAUSE_READ)

        c = LEFT * 3.25 + UP * .15
        normal_dir = np.array([.46, 1.0, 0.0]); normal_dir /= np.linalg.norm(normal_dir)
        slope_dir = np.array([1.0, -.46, 0.0]); slope_dir /= np.linalg.norm(slope_dir)
        weight = Arrow(c, c + DOWN * 1.62, buff=0, color=BLACK_LINE, stroke_width=5)
        normal = Arrow(c, c + normal_dir * 1.55, buff=0, color=BLACK_LINE, stroke_width=5)
        parallel = Arrow(c, c + slope_dir * 1.78, buff=0, color=BLACK_LINE, stroke_width=5)
        w_label = self.math(r"\vec W=m\vec g", 30).next_to(weight.get_end(), RIGHT, buff=.10)
        n_label = self.math(r"\vec N", 30).next_to(normal.get_end(), UR, buff=.10)
        p_label = self.math(r"\vec W_{\parallel}", 30).next_to(parallel.get_end(), DR, buff=.10)

        explanation = VGroup(
            self.text("NATIVE MANIM OVERLAYS", 25, BOLD),
            self.text("• vectors grow independently", 21),
            self.text("• labels remain mathematically precise", 21),
            self.text("• the same image can be reused", 21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.22)
        explanation.move_to(RIGHT * 4.25 + UP * .55)
        formula = self.formula_panel(
            r"W_{\parallel}=mg\sin\theta",
            width=5.3, height=1.18, font_size=38,
        ).move_to(RIGHT * 4.25 + DOWN * 1.45)

        for arrow, label in ((weight, w_label), (normal, n_label), (parallel, p_label)):
            self.play(GrowArrow(arrow), FadeIn(label), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.play(FadeIn(explanation, shift=LEFT * .10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        # Remove raster explicitly before any bulk FadeOut from the style library.
        self.remove(img)
        self.clear_stage(keep_header=True)

        # SECTION 2 — same asset, now supporting a worked mathematical model.
        self.set_header(
            2,
            "THE SAME IMAGE SUPPORTS THE CALCULATION",
            "No regenerated diagram is required: the visual context stays reusable while the mathematics changes dynamically.",
        )
        frame2 = RoundedRectangle(
            width=6.6, height=4.85, corner_radius=.12,
            stroke_color=LIGHT_GRAY, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(LEFT * 3.65 + DOWN * .55)
        img2 = ImageMobject(str(ASSET)).scale_to_fit_width(6.10).move_to(frame2)
        self.play(FadeIn(frame2), run_time=RUN_NORMAL)
        self.add(img2)

        equations = self.equation_stack(
            [
                r"m=10\,\mathrm{kg},\quad \theta=30^{\circ}",
                r"W=mg=(10)(9.81)=98.1\,\mathrm{N}",
                r"W_{\parallel}=98.1\sin30^{\circ}=49.05\,\mathrm{N}",
                r"N=98.1\cos30^{\circ}\approx84.96\,\mathrm{N}",
            ],
            sizes=[32, 32, 30, 30],
            buff=.34,
            max_width=6.7,
            max_height=4.4,
        ).move_to(RIGHT * 3.65 + DOWN * .55)

        for line in equations:
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_SUMMARY)

        self.remove(img2)
        self.standard_closing(
            "Generate the visual once — animate the explanation natively in ManimCE."
        )
