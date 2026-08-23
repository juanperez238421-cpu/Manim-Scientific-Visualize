#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from manim import *
from jp_classroom_style import *

ASSET = Path("assets/images/openai_inclined_plane.webp")

class OpenAIAssetDemo(JPMathClassroomScene):
    def validate_lesson_data(self):
        assert ASSET.exists()
        m, g, th = 10.0, 9.81, np.deg2rad(30)
        assert abs(m*g*np.sin(th)-49.05) < 1e-10

    def construct(self):
        self.standard_opening(
            "PHYSICS • OPENAI ASSET PIPELINE",
            "IMAGE → MANIMCE",
            "One generated asset, many editable explanations",
            "The image gives context; Manim carries the mathematics."
        )
        self.set_header(
            1, "GENERATED ASSET",
            "The OpenAI image is reused as visual context while every label remains a native Manim object."
        )
        img = ImageMobject(str(ASSET)).scale_to_fit_width(7.2)
        img.move_to(LEFT*3.35 + DOWN*0.55)
        box = RoundedRectangle(width=7.7, height=5.1, corner_radius=.12,
            stroke_color=LIGHT_GRAY, stroke_width=1.5, fill_color=WHITE, fill_opacity=1)
        box.move_to(img)
        note = self.note_panel("WHY THIS WORKS", [
            "Generated image = reusable visual object",
            "MathTex = precise equations",
            "Arrows = independently animated forces",
            "Camera = guided visual attention",
        ], width=5.6, body_size=22, max_text_height=3.3)
        note.move_to(RIGHT*3.75 + DOWN*.45)
        self.assert_content_safe(Group(box, img), "asset")
        self.assert_content_safe(note, "note")
        self.play(FadeIn(box), FadeIn(img, shift=UP*.12), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note, shift=LEFT*.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        self.clear_stage(True)
        self.set_header(
            2, "NATIVE FORCE OVERLAYS",
            "The raster asset stays fixed while vectors, angle and symbols are created and animated on top."
        )
        img = ImageMobject(str(ASSET)).scale_to_fit_width(7.4)
        img.move_to(LEFT*3.1 + DOWN*.55)
        frame = RoundedRectangle(width=7.9, height=5.05, corner_radius=.12,
            stroke_color=LIGHT_GRAY, stroke_width=1.5, fill_color=WHITE, fill_opacity=1).move_to(img)
        c = LEFT*3.25 + UP*.15
        w = Arrow(c, c+DOWN*1.65, buff=0, color=BLACK_LINE, stroke_width=5)
        n_dir = np.array([.46,1,0]); n_dir /= np.linalg.norm(n_dir)
        n = Arrow(c, c+n_dir*1.55, buff=0, color=BLACK_LINE, stroke_width=5)
        p_dir = np.array([1,-.46,0]); p_dir /= np.linalg.norm(p_dir)
        p = Arrow(c, c+p_dir*1.8, buff=0, color=BLACK_LINE, stroke_width=5)
        wl = self.math(r"\vec W=m\vec g",30).next_to(w.get_end(),RIGHT,buff=.1)
        nl = self.math(r"\vec N",30).next_to(n.get_end(),UR,buff=.1)
        pl = self.math(r"\vec W_{\parallel}",30).next_to(p.get_end(),DR,buff=.1)
        legend = self.key_value_panel("EDITABLE OVERLAYS", [
            ("Weight",r"\vec W"),("Normal",r"\vec N"),
            ("Along plane",r"\vec W_{\parallel}"),("Angle",r"\theta")
        ], width=5.0, label_size=21, value_size=27)
        legend.move_to(RIGHT*4.45 + DOWN*.45)
        self.play(FadeIn(frame), FadeIn(img), run_time=RUN_NORMAL)
        for arrow,label in ((w,wl),(n,nl),(p,pl)):
            self.play(GrowArrow(arrow), FadeIn(label), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.play(FadeIn(legend), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        self.clear_stage(True)
        self.set_header(
            3, "FROM VISUAL CONTEXT TO EQUATIONS",
            "The same generated image supports a worked model without regenerating or rasterizing the mathematics."
        )
        img = ImageMobject(str(ASSET)).scale_to_fit_width(5.9).move_to(LEFT*3.6+DOWN*.55)
        eq = self.equation_stack([
            r"W=mg",
            r"W_{\parallel}=W\sin\theta",
            r"W_{\perp}=W\cos\theta",
            r"N=W_{\perp}=mg\cos\theta",
            r"W_{\parallel}=49.05\,\mathrm{N}",
            r"N\approx84.96\,\mathrm{N}",
        ], sizes=[40,36,36,36,34,34], max_width=6.5, max_height=4.7)
        eq.move_to(RIGHT*3.55+DOWN*.55)
        self.play(FadeIn(img), run_time=RUN_NORMAL)
        for line in eq:
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_SUMMARY)
        self.standard_closing(
            "Generate the object once — animate the science natively in ManimCE."
        )
