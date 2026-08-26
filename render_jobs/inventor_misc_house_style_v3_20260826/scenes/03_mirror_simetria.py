from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorMirrorHouseStyle(JPMiscCADScene):
    OPERATION = "Mirror / Simetría"

    def construct(self):
        self.opening("SIMETRÍA  •  MIRROR",
                     "Reuse an existing feature by reflecting it across a work plane instead of remodeling it.",
                     ["SOURCE FEATURE", "MIRROR PLANE", "REFLECTION", "SYMMETRIC MODEL"])
        self.plan_logic(); self.build_seed(); self.reflect_feature(); self.finish()

    def plan_logic(self):
        h = self.section_header(1, "CORE IDEA: EVERY POINT KEEPS THE SAME NORMAL DISTANCE TO THE PLANE",
                                "A mirror is not a copy with guessed coordinates; the plane is the exact geometric reference.")
        plane = DashedLine(UP*2.3, DOWN*2.3, color=BLACK, stroke_width=2.5, dash_length=0.13)
        p = Dot(LEFT*3.0+UP*0.5, color=BLACK, radius=0.09)
        q = Dot(RIGHT*3.0+UP*0.5, color=BLACK, radius=0.09)
        d1 = DoubleArrow(LEFT*3.0+UP*0.1, UP*0.1, buff=0, color=BLACK, stroke_width=2)
        d2 = DoubleArrow(UP*0.1, RIGHT*3.0+UP*0.1, buff=0, color=BLACK, stroke_width=2)
        labs = VGroup(self.text("SOURCE",22,BOLD).next_to(p,UP), self.text("MIRROR",22,BOLD).next_to(q,UP),
                      self.text("d",20,BOLD).next_to(d1,DOWN), self.text("d",20,BOLD).next_to(d2,DOWN))
        self.fixed(labs)
        self.play(Create(plane), FadeIn(p), Create(d1), run_time=1.0)
        self.play(TransformFromCopy(p, q), Create(d2), FadeIn(labs), run_time=1.3)
        self.wait(EXPLAIN); self.clear_scene()

    def build_seed(self):
        body = self.base_plate_from_sketch(2, width=5.6, depth=3.2, height=0.55, dims="90 × 52 mm", extrude="9 mm")
        h = self.section_header(3, "CREATE ONLY ONE SIDE — THEN MIRROR THE FEATURE",
                                "The seed boss is modeled once on the left side of the plate. The central YZ plane generates the right-side feature.")
        self.fixed(h)
        self.move_camera(phi=5*DEGREES, theta=-90*DEGREES, zoom=1, run_time=1.0)
        plate = Rectangle(width=5.6, height=3.2, color=BLACK, stroke_width=3)
        circle = Circle(radius=0.46, color=BLACK, stroke_width=4).move_to(LEFT*1.65)
        axis = DashedLine(UP*1.6, DOWN*1.6, color=MID_GRAY, stroke_width=2, dash_length=0.12)
        dims = self.text("Ø16 mm   |   center 28 mm from symmetry plane", 21, BOLD).to_edge(DOWN, buff=0.35)
        self.fixed(dims)
        self.play(FadeOut(body), FadeIn(plate), Create(axis), Create(circle), FadeIn(dims), run_time=1.2); self.wait(READ)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9, run_time=1.1)
        base = cuboid(5.6, 3.2, 0.55, opacity=0.55)
        seed = cylinder(0.46, 0.55, opacity=0.62).shift(LEFT*1.65+OUT*0.55)
        self.play(FadeOut(plate), FadeOut(axis), FadeOut(circle), FadeOut(dims), FadeIn(base), FadeIn(seed), run_time=1.15)
        self._base, self._seed, self._header = base, seed, h

    def reflect_feature(self):
        plane = Rectangle(width=3.9, height=2.5, stroke_color=BLACK, stroke_width=1.6, fill_color=LIGHT_GRAY, fill_opacity=0.18)
        plane.rotate(PI/2, axis=UP)
        card = self.parameter_card("MIRROR", [("Features","Boss1"), ("Mirror Plane","YZ Plane"), ("Operation","Join")])
        self.play(FadeIn(plane), FadeIn(card), run_time=0.9); self.wait(READ)
        ghost = self._seed.copy().set_opacity(0.25)
        self.add(ghost)
        self.play(ghost.animate.shift(RIGHT*3.30), run_time=2.2, rate_func=smooth)
        mirror = ghost.copy().set_opacity(0.62)
        self.play(ReplacementTransform(ghost, mirror), FadeOut(card), run_time=0.75); self.wait(READ)
        self.play(FadeOut(plane), run_time=0.45)
        self._mirror = mirror

    def finish(self):
        note = self.note("PROFESSIONAL HABIT", ["Mirror features, not manually redrawn sketches.", "Use a stable origin or work plane.", "Edit the seed feature and both sides update."], width=6.0).to_corner(DR, buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN); self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("SOURCE FEATURE + PLANE = PARAMETRIC MIRROR")
