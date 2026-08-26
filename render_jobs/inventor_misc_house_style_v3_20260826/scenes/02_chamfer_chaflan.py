from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorChamferHouseStyle(JPMiscCADScene):
    OPERATION = "Chamfer / Chaflán"

    def construct(self):
        self.opening("CHAFLÁN  •  CHAMFER",
                     "Replace a sharp corner with a flat bevel controlled by distance and/or angle.",
                     ["EDGE", "DISTANCE", "ANGLE", "BEVELED SOLID"])
        self.core_idea(); self.build_select(); self.animate_cut(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: CHAMFER CREATES A FLAT TRANSITION",
                                "Unlike Fillet, the transition is planar. The corner is removed by a straight cutting line in section.")
        left = VGroup(Line(LEFT*5.3+DOWN*0.6, LEFT*3.3+DOWN*0.6, color=BLACK, stroke_width=5),
                      Line(LEFT*3.3+DOWN*0.6, LEFT*3.3+UP*1.4, color=BLACK, stroke_width=5))
        right = VGroup(Line(RIGHT*0.2+DOWN*0.6, RIGHT*1.2+DOWN*0.6, color=BLACK, stroke_width=5),
                       Line(RIGHT*2.2+UP*0.4, RIGHT*2.2+UP*1.4, color=BLACK, stroke_width=5),
                       Line(RIGHT*1.2+DOWN*0.6, RIGHT*2.2+UP*0.4, color=BLACK, stroke_width=5))
        b1 = self.text("SHARP", 23, BOLD).move_to(LEFT*4.2+DOWN*2)
        b2 = self.text("6 mm × 45°", 23, BOLD).move_to(RIGHT*1.2+DOWN*2)
        self.fixed(b1, b2)
        self.play(Create(left), FadeIn(b1), run_time=1.0)
        self.play(TransformFromCopy(left, right), FadeIn(b2), run_time=1.35)
        card = self.note("CHAMFER PARAMETERS", ["Distance–Angle: 6 mm and 45°", "Equal Distance: d1 = d2", "Two Distances: d1 and d2"], width=5.6).to_corner(DR, buff=0.45).shift(UP*0.35)
        self.fixed(card); self.play(FadeIn(card), run_time=0.8); self.wait(EXPLAIN); self.clear_scene()

    def build_select(self):
        body = self.base_plate_from_sketch(2, width=5.0, depth=3.0, height=0.72, dims="80 × 48 mm", extrude="12 mm")
        h = self.section_header(3, "SELECT THE CORNER EDGES TO BE BEVELED",
                                "This example chamfers all four vertical edges so the top profile becomes an eight-sided perimeter.")
        self.fixed(h)
        w, d, z0, z1 = 2.5, 1.5, -0.36, 0.36
        edges = VGroup(*[Line3D([sx*w, sy*d, z0], [sx*w, sy*d, z1], color=BLACK, thickness=0.035) for sx, sy in [(1,1),(-1,1),(-1,-1),(1,-1)]])
        card = self.parameter_card("CHAMFER", [("Selection", "4 Edges"), ("Type", "Distance + Angle"), ("Distance", "6 mm"), ("Angle", "45 deg")])
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.16), FadeIn(card), run_time=1.35); self.wait(READ)
        self._body, self._edges, self._card, self._header = body, edges, card, h

    def animate_cut(self):
        self.play(FadeOut(self._card), run_time=0.3)
        self.move_camera(phi=4*DEGREES, theta=-90*DEGREES, zoom=1, run_time=1.0)
        sharp = Rectangle(width=5.0, height=3.0, color=BLACK, stroke_width=4)
        self.play(FadeOut(self._body), FadeOut(self._edges), FadeIn(sharp), run_time=0.7)
        c = 0.40; w = 2.5; d = 1.5
        cuts = VGroup(Line([w-c,d,0],[w,d-c,0],color=BLACK,stroke_width=4),
                      Line([-w+c,d,0],[-w,d-c,0],color=BLACK,stroke_width=4),
                      Line([-w+c,-d,0],[-w,-d+c,0],color=BLACK,stroke_width=4),
                      Line([w-c,-d,0],[w,-d+c,0],color=BLACK,stroke_width=4))
        self.play(LaggedStart(*[Create(x) for x in cuts], lag_ratio=0.18), run_time=1.5)
        pts = [[-w+c,-d,0],[w-c,-d,0],[w,-d+c,0],[w,d-c,0],[w-c,d,0],[-w+c,d,0],[-w,d-c,0],[-w,-d+c,0]]
        chamfer2d = Polygon(*[np.array(p) for p in pts], color=BLACK, stroke_width=4)
        self.play(FadeOut(sharp), FadeOut(cuts), FadeIn(chamfer2d), run_time=1.0); self.wait(READ)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9, run_time=1.1)
        result = chamfered_plate(5.0, 3.0, 0.72, 0.40, opacity=0.60)
        self.play(FadeOut(chamfer2d), FadeIn(result), run_time=1.25)
        self._result = result

    def finish(self):
        note = self.note("WHY CHAMFER?", ["Break a dangerous sharp edge.", "Create assembly lead-in geometry.", "Prepare edges for manufacturing or welding."], width=5.8).to_corner(DR, buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN); self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("EDGE + DISTANCE / ANGLE = CHAMFERED FEATURE")
