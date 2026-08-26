from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorCoilHouseStyle(JPMiscCADScene):
    OPERATION = "Coil / Bobina"

    def construct(self):
        self.opening("BOBINA  •  COIL",
                     "Move a profile around an axis while advancing along that axis: rotation + translation = helix.",
                     ["PROFILE", "AXIS", "PITCH", "REVOLUTIONS", "HELIX"])
        self.core_idea(); self.sketch_inputs(); self.animate_helix(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: A COIL IS A HELICAL SWEEP",
                                "One revolution advances exactly one pitch. Total height = pitch × number of revolutions.")
        circle = Circle(radius=1.15, color=BLACK, stroke_width=3).shift(LEFT*3.5)
        arrow = Arrow(LEFT*3.5+DOWN*1.8, LEFT*3.5+UP*1.8, buff=0, color=BLACK, stroke_width=3)
        formula = MathTex(r"H=p\,N", color=BLACK, font_size=52).move_to(RIGHT*3.4+UP*0.6)
        ex = self.text("p = 12 mm,  N = 4  →  H = 48 mm",26,BOLD).move_to(RIGHT*3.4+DOWN*0.7)
        self.fixed(formula, ex)
        self.play(Create(circle), Create(arrow), run_time=1.1)
        self.play(Write(formula), FadeIn(ex), run_time=1.0); self.wait(EXPLAIN); self.clear_scene()

    def sketch_inputs(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1)
        h = self.section_header(2, "SKETCH THE PROFILE AND THE AXIS BEFORE CLICKING COIL",
                                "The small circle is the wire section. The centerline is the helical axis.")
        self.fixed(h)
        axis = DashedLine(DOWN*2.4, UP*2.4, color=BLACK, stroke_width=2.5, dash_length=0.12)
        prof = Circle(radius=0.34, color=BLACK, stroke_width=4).move_to(RIGHT*2.0+DOWN*1.8)
        radial = Line(DOWN*1.8, RIGHT*2.0+DOWN*1.8, color=MID_GRAY, stroke_width=2)
        labs = VGroup(self.text("AXIS",21,BOLD).next_to(axis,LEFT,buff=0.2),
                      self.text("Ø6 mm PROFILE",21,BOLD).next_to(prof,RIGHT,buff=0.2),
                      self.text("R = 20 mm",21,BOLD).next_to(radial,UP,buff=0.15))
        self.fixed(labs)
        self.play(Create(axis), Create(radial), Create(prof), FadeIn(labs), run_time=1.3); self.wait(EXPLAIN)
        card = self.parameter_card("COIL", [("Pitch","12 mm"),("Revolutions","4"),("Section","Ø6 mm"),("Operation","New Solid")])
        self.play(FadeIn(card), run_time=0.8); self.wait(READ); self.play(FadeOut(card), run_time=0.35)
        self._axis2d, self._prof2d, self._header = axis, prof, h

    def animate_helix(self):
        self.move_camera(phi=67*DEGREES, theta=-48*DEGREES, zoom=0.88, run_time=1.2)
        self.play(FadeOut(self._axis2d), FadeOut(self._prof2d), run_time=0.35)
        axis = DashedLine([0,0,-2.4], [0,0,2.4], dash_length=0.12, color=BLACK, stroke_width=2.2)
        self.play(Create(axis), run_time=0.7)
        turns = 4; radius = 2.0; height = 4.8
        helix = ParametricFunction(lambda t: np.array([radius*math.cos(t), radius*math.sin(t), -height/2+height*t/(turns*TAU)]),
                                   t_range=[0,turns*TAU], color=BLACK, stroke_width=11)
        guide = helix.copy().set_stroke(width=2, opacity=0.20)
        self.add(guide)
        self.play(Create(helix), run_time=4.0, rate_func=linear)
        pitch_mark = Line3D([2.45,0,-2.4], [2.45,0,-1.2], color=BLACK, thickness=0.025)
        pitch_lab = self.text("pitch = 12 mm",22,BOLD).to_corner(DR,buff=0.55).shift(UP*0.7)
        self.fixed(pitch_lab)
        self.play(Create(pitch_mark), FadeIn(pitch_lab), run_time=0.8); self.wait(EXPLAIN)
        self._helix, self._axis3d, self._pitch_lab = helix, axis, pitch_lab

    def finish(self):
        note = self.note("COIL CONTROLS", ["Pitch controls spacing between turns.", "Revolutions control how many turns are created.", "Profile size controls wire/thread thickness."], width=5.9).to_corner(DR,buff=0.45).shift(UP*0.45)
        self.fixed(note)
        self.play(FadeOut(self._pitch_lab), FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("PROFILE + AXIS + PITCH + REVOLUTIONS = COIL")
