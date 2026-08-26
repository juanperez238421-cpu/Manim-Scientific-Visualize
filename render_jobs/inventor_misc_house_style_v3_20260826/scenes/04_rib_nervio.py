from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorRibHouseStyle(JPMiscCADScene):
    OPERATION = "Rib / Nervio"

    def construct(self):
        self.opening("NERVIO  •  RIB",
                     "Create a thin structural wall from an open sketch line and let Inventor terminate it against neighboring faces.",
                     ["OPEN SKETCH", "THICKNESS", "EXTENT", "STRUCTURAL RIB"])
        self.core_idea(); self.build_bracket(); self.draw_rib_sketch(); self.grow_rib(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: RIB STARTS FROM A LINE, NOT A CLOSED REGION",
                                "The line defines the center/side of a thin wall; thickness and extent turn that line into material.")
        line = Line(LEFT*3.8+DOWN*1.3, RIGHT*0.2+UP*1.4, color=BLACK, stroke_width=5)
        ghost = line.copy().set_stroke(width=18, opacity=0.18)
        labels = VGroup(self.text("OPEN SKETCH LINE",22,BOLD).next_to(line,DOWN,buff=0.25),
                        self.text("THICKEN",22,BOLD).move_to(RIGHT*3.6+DOWN*1.6))
        self.fixed(labels)
        self.play(Create(line), FadeIn(labels[0]), run_time=1.1)
        self.play(FadeIn(ghost), FadeIn(labels[1]), run_time=1.1)
        card = self.note("RIB INPUTS", ["One open line or open chain", "Thickness: 6 mm", "Direction: symmetric", "Extent: To Next"], width=5.5).to_corner(DR,buff=0.45).shift(UP*0.35)
        self.fixed(card); self.play(FadeIn(card), run_time=0.8); self.wait(EXPLAIN); self.clear_scene()

    def build_bracket(self):
        h = self.section_header(2, "BUILD THE HOST SOLID FIRST",
                                "A rib normally reinforces geometry that already exists. Here: base plate + vertical wall.")
        self.fixed(h)
        self.set_camera_orientation(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9)
        base = cuboid(5.4, 3.2, 0.45, opacity=0.56).shift(DOWN*0.3)
        wall = cuboid(0.45, 3.2, 2.7, opacity=0.56).shift(LEFT*2.48+OUT*1.35+DOWN*0.3)
        self.play(FadeIn(base), run_time=0.9)
        self.play(FadeIn(wall), run_time=0.9); self.wait(READ)
        self._base, self._wall, self._header = base, wall, h

    def draw_rib_sketch(self):
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1, run_time=1.1)
        side_base = Rectangle(width=5.4, height=0.45, color=BLACK, stroke_width=3).shift(DOWN*1.1)
        side_wall = Rectangle(width=0.45, height=2.7, color=BLACK, stroke_width=3).move_to(LEFT*2.48+UP*0.25)
        ribline = Line(LEFT*2.22+DOWN*0.88, LEFT*0.15+UP*1.35, color=BLACK, stroke_width=5)
        dims = VGroup(self.text("OPEN LINE",22,BOLD).next_to(ribline,RIGHT,buff=0.25),
                      self.text("Thickness = 6 mm",22,BOLD).to_edge(DOWN,buff=0.34))
        self.fixed(dims)
        self.play(FadeOut(self._base), FadeOut(self._wall), FadeIn(side_base), FadeIn(side_wall), Create(ribline), FadeIn(dims), run_time=1.3)
        self.wait(EXPLAIN)
        self._side = VGroup(side_base, side_wall)
        self._ribline = ribline

    def grow_rib(self):
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9, run_time=1.1)
        self.play(FadeOut(self._side), FadeOut(self._ribline), run_time=0.4)
        base = cuboid(5.4,3.2,0.45,opacity=0.56).shift(DOWN*0.3)
        wall = cuboid(0.45,3.2,2.7,opacity=0.56).shift(LEFT*2.48+OUT*1.35+DOWN*0.3)
        self.play(FadeIn(base), FadeIn(wall), run_time=0.6)
        rib = VGroup(
            Polygon(np.array([-2.25,-0.26,-0.05]),np.array([-2.25,-0.26,1.95]),np.array([-0.15,-0.26,-0.05]),fill_color=GRAY_C,fill_opacity=0.56,stroke_color=GRAY_B,stroke_width=0.8),
            Polygon(np.array([-2.25,0.26,-0.05]),np.array([-2.25,0.26,1.95]),np.array([-0.15,0.26,-0.05]),fill_color=GRAY_C,fill_opacity=0.56,stroke_color=GRAY_B,stroke_width=0.8),
            Polygon(np.array([-2.25,-0.26,-0.05]),np.array([-2.25,0.26,-0.05]),np.array([-2.25,0.26,1.95]),np.array([-2.25,-0.26,1.95]),fill_color=GRAY_C,fill_opacity=0.56,stroke_color=GRAY_B,stroke_width=0.8),
            Polygon(np.array([-2.25,-0.26,1.95]),np.array([-2.25,0.26,1.95]),np.array([-0.15,0.26,-0.05]),np.array([-0.15,-0.26,-0.05]),fill_color=GRAY_C,fill_opacity=0.56,stroke_color=GRAY_B,stroke_width=0.8),
        )
        seedline = Line3D([-2.25,0,0],[-0.15,0,1.9],color=BLACK,thickness=0.035)
        self.play(Create(seedline), run_time=0.7)
        self.play(FadeIn(rib), seedline.animate.set_opacity(0.25), run_time=1.6)
        card = self.parameter_card("RIB", [("Profile","Open Line"),("Thickness","6 mm"),("Direction","Symmetric"),("Extent","To Next")])
        self.play(FadeIn(card), run_time=0.75); self.wait(EXPLAIN)
        self.play(FadeOut(card), FadeOut(seedline), run_time=0.4)
        self._rib = rib

    def finish(self):
        note = self.note("STRUCTURAL REASONING", ["The rib increases stiffness with little material.", "Its thickness is usually much smaller than its height.", "To Next keeps termination attached to the host geometry."], width=6.2).to_corner(DR,buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("OPEN SKETCH + THICKNESS + EXTENT = RIB")
