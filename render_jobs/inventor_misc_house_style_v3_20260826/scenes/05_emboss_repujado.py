from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorEmbossHouseStyle(JPMiscCADScene):
    OPERATION = "Emboss / Repujado"

    def construct(self):
        self.opening("REPUJADO  •  EMBOSS",
                     "Project a closed sketch onto a face and raise or engrave that region by a controlled depth.",
                     ["FACE", "CLOSED SKETCH", "DEPTH", "EMBOSSED FEATURE"])
        self.core_idea(); self.build_face(); self.sketch_logo(); self.raise_feature(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: THE SKETCH LIVES ON A FACE",
                                "Emboss uses a closed region on the selected face; depth decides whether the region rises or sinks.")
        face = Rectangle(width=5.8, height=3.2, color=BLACK, stroke_width=3)
        hexagon = RegularPolygon(6, radius=0.85, color=BLACK, stroke_width=4)
        arrow = Arrow(DOWN*0.15, UP*1.45, buff=0.05, color=BLACK, stroke_width=3)
        labs = VGroup(self.text("CLOSED PROFILE",22,BOLD).next_to(hexagon,DOWN,buff=0.3),
                      self.text("+3 mm",22,BOLD).next_to(arrow,RIGHT,buff=0.2))
        self.fixed(labs)
        self.play(Create(face), Create(hexagon), FadeIn(labs[0]), run_time=1.1)
        self.play(Create(arrow), FadeIn(labs[1]), run_time=0.8)
        note = self.note("TWO DIRECTIONS", ["Emboss: add material above the face.", "Engrave/Deboss: remove or sink the region."], width=5.7).to_corner(DR,buff=0.45).shift(UP*0.35)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN); self.clear_scene()

    def build_face(self):
        self._body = self.base_plate_from_sketch(2, width=5.6, depth=3.2, height=0.55, dims="90 × 52 mm", extrude="9 mm")

    def sketch_logo(self):
        h = self.section_header(3, "DRAW THE EMBOSS PROFILE ON THE TOP FACE",
                                "The face becomes the sketch plane. Keep the profile closed and fully constrained before leaving Sketch mode.")
        self.fixed(h)
        self.move_camera(phi=5*DEGREES, theta=-90*DEGREES, zoom=1, run_time=1.0)
        plate = Rectangle(width=5.6, height=3.2, color=BLACK, stroke_width=3)
        logo = RegularPolygon(6, radius=0.82, color=BLACK, stroke_width=4)
        center = Dot(ORIGIN, color=BLACK, radius=0.06)
        dim = self.text("Hexagon: 24 mm across flats   |   centered on origin",21,BOLD).to_edge(DOWN,buff=0.34)
        self.fixed(dim)
        self.play(FadeOut(self._body), FadeIn(plate), Create(logo), FadeIn(center), FadeIn(dim), run_time=1.2); self.wait(EXPLAIN)
        self._plate2d, self._logo2d, self._header = plate, logo, h

    def raise_feature(self):
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9, run_time=1.1)
        self.play(FadeOut(self._plate2d), FadeOut(self._logo2d), run_time=0.35)
        base = cuboid(5.6,3.2,0.55,opacity=0.56)
        self.play(FadeIn(base), run_time=0.6)
        pts = []
        for a in np.linspace(0,TAU,6,endpoint=False):
            pts.append([0.82*math.cos(a),0.82*math.sin(a),0.275])
        emblem = extruded_polygon(pts,0.24,opacity=0.20,color=GRAY_C)
        self.play(FadeIn(emblem), run_time=1.5)
        card = self.parameter_card("EMBOSS", [("Profile","Sketch2 region"),("Depth","3 mm"),("Direction","Positive"),("Operation","Emboss")])
        self.play(FadeIn(card), run_time=0.8); self.wait(EXPLAIN)
        final = extruded_polygon(pts,0.24,opacity=0.62,color=GRAY_C)
        self.play(Transform(emblem,final), FadeOut(card), run_time=0.8)
        self._base, self._emblem = base, emblem

    def finish(self):
        note = self.note("WHEN TO USE IT", ["Logos and identification marks.", "Raised grip or decorative geometry.", "Shallow face detail without a separate thick extrusion."], width=6.0).to_corner(DR,buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("FACE + CLOSED PROFILE + DEPTH = EMBOSS")
