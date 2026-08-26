from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorCircularPatternHouseStyle(JPMiscCADScene):
    OPERATION = "Circular Pattern / Patrón circular"

    def construct(self):
        self.opening("PATRÓN CIRCULAR  •  CIRCULAR PATTERN",
                     "Repeat one seed feature around an axis using an angular extent and occurrence count.",
                     ["SEED FEATURE", "AXIS", "ANGLE", "QUANTITY", "CIRCULAR PATTERN"])
        self.core_idea(); self.build_seed(); self.animate_pattern(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: THE AXIS DEFINES THE CENTER OF REPETITION",
                                "For a full pattern, angular step = 360° / quantity. Here: 360° / 8 = 45°.")
        ring = Circle(radius=2.0, color=LIGHT_GRAY, stroke_width=2)
        center = Dot(ORIGIN, color=BLACK, radius=0.08)
        seed = Circle(radius=0.30, color=BLACK, stroke_width=4).move_to(RIGHT*2.0)
        copies = VGroup(*[seed.copy().rotate(k*45*DEGREES, about_point=ORIGIN) for k in range(1,8)])
        formula = MathTex(r"\Delta\theta=\frac{360^\circ}{8}=45^\circ", color=BLACK, font_size=48).to_edge(DOWN,buff=0.35)
        self.fixed(formula)
        self.play(Create(ring), FadeIn(center), Create(seed), run_time=1.0)
        self.play(LaggedStart(*[TransformFromCopy(seed,c) for c in copies], lag_ratio=0.14), run_time=2.5)
        self.play(Write(formula), run_time=0.8); self.wait(EXPLAIN); self.clear_scene()

    def build_seed(self):
        h = self.section_header(2, "BUILD THE HOST DISK AND ONE SEED FEATURE",
                                "A circular pattern is clearest when the host already exposes a stable central axis.")
        self.fixed(h)
        self.set_camera_orientation(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9)
        disk = cylinder(2.85,0.48,opacity=0.56)
        seed = cylinder(0.34,0.50,opacity=0.62).shift(RIGHT*1.85+OUT*0.49)
        axis = DashedLine([0,0,-1.2],[0,0,1.6],dash_length=0.12,color=BLACK,stroke_width=2.2)
        self.play(FadeIn(disk), run_time=0.9)
        self.play(FadeIn(seed), Create(axis), run_time=0.9); self.wait(READ)
        self._disk, self._seed, self._axis, self._header = disk, seed, axis, h

    def animate_pattern(self):
        card = self.parameter_card("CIRCULAR PATTERN", [("Features","Boss1"),("Rotation Axis","Z Axis"),("Placement","Full"),("Quantity","8")])
        self.play(FadeIn(card), run_time=0.8); self.wait(READ)
        copies = []
        for k in range(1,8):
            ang = k*45*DEGREES
            c = self._seed.copy().rotate(ang, axis=OUT, about_point=ORIGIN)
            copies.append(c)
            self.play(TransformFromCopy(self._seed,c), run_time=0.48)
        self.wait(READ); self.play(FadeOut(card), run_time=0.35)
        self._copies = VGroup(*copies)

    def finish(self):
        note = self.note("DESIGN CHECK", ["Axis must be stable and intentional.", "Full pattern distributes occurrences uniformly.", "Changing quantity automatically recalculates angular spacing."], width=6.0).to_corner(DR,buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("SEED + AXIS + ANGLE + QUANTITY = CIRCULAR PATTERN")
