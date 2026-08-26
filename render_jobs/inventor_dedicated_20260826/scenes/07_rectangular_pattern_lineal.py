from manim import *
from library.inventor_pro_ui import *

class InventorRectPatternDetailed(JPMiscCADScene):
    OPERATION="Rectangular Pattern / Patrón lineal"
    def construct(self):
        self.opening("PATRÓN LINEAL  •  RECTANGULAR PATTERN","Repeat one seed feature along a controlled direction using spacing and quantity.",["SEED FEATURE","DIRECTION","SPACING","QUANTITY","PATTERN"])
        h=self.section_header(1,"CORE IDEA: ONE FEATURE DEFINES EVERY OCCURRENCE","Seed controls shape; direction controls orientation; spacing and quantity control placement.")
        seed=Circle(radius=.38,color=BLACK,stroke_width=4).move_to(LEFT*4.5); arrow=Arrow(LEFT*3.7,RIGHT*4.5,buff=0,color=BLACK,stroke_width=3); copies=VGroup(*[seed.copy().shift(RIGHT*i*2.1) for i in range(1,5)]); lab=self.text("4 occurrences   |   spacing = 35 mm",24,BOLD).to_edge(DOWN,buff=.34); self.fixed(lab)
        self.play(Create(seed),Create(arrow),run_time=1); self.play(LaggedStart(*[TransformFromCopy(seed,c) for c in copies],lag_ratio=.22),run_time=2); self.play(FadeIn(lab),run_time=.6); self.wait(EXPLAIN); self.clear_scene()
        body=self.base_plate_from_sketch(2,width=6.4,depth=3.2,height=.50,dims="110 × 52 mm",extrude="8 mm")
        h=self.section_header(3,"MODEL ONE SEED BOSS — DO NOT DRAW FOUR BOSSES","Pattern should reference the finished feature, not reproduce its sketch manually."); self.fixed(h)
        self.move_camera(phi=5*DEGREES,theta=-90*DEGREES,zoom=1,run_time=1); plate=Rectangle(width=6.4,height=3.2,color=BLACK,stroke_width=3); circle=Circle(radius=.40,color=BLACK,stroke_width=4).move_to(LEFT*2.35); xaxis=Arrow(LEFT*2.9+DOWN*1.15,RIGHT*2.9+DOWN*1.15,buff=0,color=BLACK,stroke_width=2.5); lab=self.text("Seed Ø14 mm   |   Direction 1 = X axis",21,BOLD).to_edge(DOWN,buff=.34); self.fixed(lab)
        self.play(FadeOut(body),FadeIn(plate),Create(circle),Create(xaxis),FadeIn(lab),run_time=1.2); self.wait(READ)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); base=cuboid(6.4,3.2,.50,.56); seed3=cylinder(.40,.48,.62).shift(LEFT*2.35+OUT*.49); self.play(FadeOut(plate),FadeOut(circle),FadeOut(xaxis),FadeOut(lab),FadeIn(base),FadeIn(seed3),run_time=1.1)
        card=self.parameter_card("RECTANGULAR PATTERN",[("Features","Boss1"),("Direction 1","X Axis"),("Quantity","4"),("Spacing","35 mm")]); self.play(FadeIn(card),run_time=.8); self.wait(READ)
        for dx in [1.55,3.10,4.65]: self.play(TransformFromCopy(seed3,seed3.copy().shift(RIGHT*dx)),run_time=.75)
        self.wait(READ); self.play(FadeOut(card),run_time=.35)
        note=self.note("WHY PATTERN?",["One edit updates every occurrence.","Spacing remains dimension-driven.","Selected occurrences can later be suppressed."],width=5.9).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("SEED + DIRECTION + SPACING + QUANTITY = LINEAR PATTERN")
