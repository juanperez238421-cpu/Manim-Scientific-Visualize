from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorFilletHouseStyle(JPMiscCADScene):
    OPERATION = "Fillet / Redondeo"

    def construct(self):
        self.opening(
            "REDONDEO  •  FILLET",
            "Replace a sharp edge with a tangent radius without rebuilding the original sketch.",
            ["EDGE", "RADIUS", "TANGENCY", "FILLETED SOLID"],
        )
        self.core_idea()
        self.build_and_select()
        self.animate_feature()
        self.engineering_check()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: A SHARP CORNER BECOMES A TANGENT ARC",
                                "Read Fillet as local geometry: two faces + one radius + tangency conditions.")
        sharp = VGroup(Line(LEFT*5.5+DOWN*0.7, LEFT*3.5+DOWN*0.7, color=BLACK, stroke_width=5),
                       Line(LEFT*3.5+DOWN*0.7, LEFT*3.5+UP*1.3, color=BLACK, stroke_width=5))
        arc = Arc(radius=1.0, start_angle=PI, angle=-PI/2, arc_center=RIGHT*2.0+UP*0.3, color=BLACK, stroke_width=5)
        legs = VGroup(Line(RIGHT*0.0+DOWN*0.7, RIGHT*1.0+DOWN*0.7, color=BLACK, stroke_width=5),
                      Line(RIGHT*2.0+UP*0.3, RIGHT*2.0+UP*1.3, color=BLACK, stroke_width=5))
        before = self.text("SHARP", 24, BOLD).move_to(LEFT*4.5+DOWN*2.0)
        after = self.text("RADIUS R", 24, BOLD).move_to(RIGHT*1.2+DOWN*2.0)
        rline = Line(RIGHT*2.0+UP*0.3, RIGHT*1.3+DOWN*0.4, color=MID_GRAY, stroke_width=2)
        rlab = MathTex("R", color=BLACK, font_size=38).next_to(rline, UP, buff=0.05)
        self.fixed(before, after, rlab)
        self.play(Create(sharp), FadeIn(before), run_time=1.0)
        self.play(TransformFromCopy(sharp, VGroup(legs, arc)), FadeIn(after), Create(rline), FadeIn(rlab), run_time=1.45)
        note = self.note("DESIGN MEANING", ["The original faces stay.", "The sharp intersection is replaced.", "The new surface is tangent to both faces."], width=5.5).to_corner(DR, buff=0.45).shift(UP*0.4)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.clear_scene()

    def build_and_select(self):
        body = self.base_plate_from_sketch(2, width=5.0, depth=3.0, height=0.72, dims="80 × 48 mm", extrude="12 mm")
        h = self.section_header(3, "SELECT THE EDGES THAT WILL SHARE ONE RADIUS",
                                "This example rounds the four vertical corner edges of the extruded plate.")
        self.fixed(h)
        w, d, z0, z1 = 2.5, 1.5, -0.36, 0.36
        edges = VGroup(*[
            Line3D([sx*w, sy*d, z0], [sx*w, sy*d, z1], color=BLACK, thickness=0.035)
            for sx, sy in [(1,1),(-1,1),(-1,-1),(1,-1)]
        ])
        card = self.parameter_card("FILLET", [("Selection", "4 Edges"), ("Radius", "R = 6 mm"), ("Mode", "Constant")])
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.18), FadeIn(card), run_time=1.35)
        self.wait(READ)
        process = self.process_row(["SELECT EDGES", "SET RADIUS", "PREVIEW", "OK"])
        self.play(LaggedStart(*[FadeIn(p) for p in process[0]], lag_ratio=0.12), Create(process[1]), run_time=1.2)
        self.wait(READ)
        self._body, self._edges, self._card, self._header, self._process = body, edges, card, h, process

    def animate_feature(self):
        self.play(FadeOut(self._card), run_time=0.35)
        self.move_camera(phi=5*DEGREES, theta=-90*DEGREES, zoom=1.0, run_time=1.05)
        top_sharp = Rectangle(width=5.0, height=3.0, color=BLACK, stroke_width=4)
        self.play(FadeOut(self._body), FadeOut(self._edges), FadeIn(top_sharp), run_time=0.75)
        lab = self.text("TOP VIEW — the corner geometry changes before the 3D reveal", 23, BOLD).to_edge(DOWN, buff=0.34)
        self.fixed(lab); self.play(FadeIn(lab), run_time=0.55)
        rounded_outline = VMobject(color=BLACK, stroke_width=4)
        pts = [np.array(p) for p in rounded_rect_points(5.0, 3.0, 0.42, samples=10, z=0)]
        rounded_outline.set_points_as_corners(pts + [pts[0]])
        self.play(Transform(top_sharp, rounded_outline), run_time=2.2, rate_func=smooth)
        self.wait(READ)
        self.play(FadeOut(lab), run_time=0.3)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.90, run_time=1.15)
        result = rounded_plate(5.0, 3.0, 0.72, 0.42, opacity=0.60)
        self.play(FadeOut(top_sharp), FadeIn(result), run_time=1.25)
        self.wait(PAUSE)
        self._result = result

    def engineering_check(self):
        note = self.note("CHECK BEFORE OK", ["Radius fits inside adjacent faces.", "No nearby feature is consumed.", "All selected edges need the same radius."], width=5.8).to_corner(DR, buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), FadeOut(self._process), run_time=0.45)
        self.final_orbit("EDGE + RADIUS + TANGENCY = FILLETED FEATURE")
