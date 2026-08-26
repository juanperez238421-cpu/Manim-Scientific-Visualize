from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library.jp_misc_cad_style import *


class InventorRectPatternHouseStyle(JPMiscCADScene):
    OPERATION = "Rectangular Pattern / Patrón lineal"

    def construct(self):
        self.opening("PATRÓN LINEAL  •  RECTANGULAR PATTERN",
                     "Repeat one seed feature along a controlled direction using spacing and quantity instead of manual copies.",
                     ["SEED FEATURE", "DIRECTION", "SPACING", "QUANTITY", "PATTERN"])
        self.core_idea(); self.build_seed(); self.animate_pattern(); self.finish()

    def core_idea(self):
        h = self.section_header(1, "CORE IDEA: ONE FEATURE DEFINES THE OTHERS",
                                "The seed controls shape; the direction controls orientation; spacing and quantity control placement.")
        seed = Circle(radius=0.38, color=BLACK, stroke_width=4).move_to(LEFT*4.5)
        arrow = Arrow(LEFT*3.7, RIGHT*4.5, buff=0, color=BLACK, stroke_width=3)
        copies = VGroup(*[seed.copy().shift(RIGHT*i*2.1) for i in range(1,5)])
        self.play(Create(seed), Create(arrow), run_time=1.0)
        self.play(LaggedStart(*[TransformFromCopy(seed,c) for c in copies], lag_ratio=0.22), run_time=2.0)
        lab = self.text("4 occurrences   |   spacing = 35 mm",24,BOLD).to_edge(DOWN,buff=0.34)
        self.fixed(lab); self.play(FadeIn(lab), run_time=0.6); self.wait(EXPLAIN); self.clear_scene()

    def build_seed(self):
        body = self.base_plate_from_sketch(2, width=6.4, depth=3.2, height=0.50, dims="110 × 52 mm", extrude="8 mm")
        h = self.section_header(3, "MODEL ONE SEED BOSS — DO NOT MODEL FOUR BOSSES",
                                "The first feature is fully defined. Pattern should reference the feature, not reproduce its sketch manually.")
        self.fixed(h)
        self.move_camera(phi=5*DEGREES, theta=-90*DEGREES, zoom=1, run_time=1.0)
        plate = Rectangle(width=6.4, height=3.2, color=BLACK, stroke_width=3)
        circle = Circle(radius=0.40, color=BLACK, stroke_width=4).move_to(LEFT*2.35)
        xaxis = Arrow(LEFT*2.9+DOWN*1.15, RIGHT*2.9+DOWN*1.15, buff=0, color=BLACK, stroke_width=2.5)
        lab = self.text("Seed Ø14 mm   |   Direction 1 = X axis",21,BOLD).to_edge(DOWN,buff=0.34)
        self.fixed(lab)
        self.play(FadeOut(body), FadeIn(plate), Create(circle), Create(xaxis), FadeIn(lab), run_time=1.2); self.wait(READ)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.9, run_time=1.1)
        base = cuboid(6.4,3.2,0.50,opacity=0.56)
        seed = cylinder(0.40,0.48,opacity=0.62).shift(LEFT*2.35+OUT*0.49)
        self.play(FadeOut(plate), FadeOut(circle), FadeOut(xaxis), FadeOut(lab), FadeIn(base), FadeIn(seed), run_time=1.1)
        self._base, self._seed, self._header = base, seed, h

    def animate_pattern(self):
        card = self.parameter_card("RECTANGULAR PATTERN", [("Features","Boss1"),("Direction 1","X Axis"),("Quantity","4"),("Spacing","35 mm")])
        self.play(FadeIn(card), run_time=0.8); self.wait(READ)
        offsets = [1.55,3.10,4.65]
        copies = []
        for dx in offsets:
            c = self._seed.copy().shift(RIGHT*dx)
            copies.append(c)
            self.play(TransformFromCopy(self._seed,c), run_time=0.75)
        self.wait(READ); self.play(FadeOut(card), run_time=0.35)
        self._copies = VGroup(*copies)

    def finish(self):
        note = self.note("WHY PATTERN?", ["One edit updates every occurrence.", "Spacing remains exact and dimension-driven.", "Suppression can remove selected occurrences later."], width=5.9).to_corner(DR,buff=0.45).shift(UP*0.45)
        self.fixed(note); self.play(FadeIn(note), run_time=0.8); self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(self._header), run_time=0.4)
        self.final_orbit("SEED + DIRECTION + SPACING + QUANTITY = LINEAR PATTERN")
