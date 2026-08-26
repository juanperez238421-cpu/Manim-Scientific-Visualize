from manim import *
from library.inventor_pro_ui import *

class InventorMirrorDetailed(JPMiscCADScene):
    OPERATION="Mirror / Simetría"
    def construct(self):
        self.opening("SIMETRÍA  •  MIRROR","Reflect one existing feature across a stable work plane instead of remodeling it.",["SOURCE FEATURE","MIRROR PLANE","REFLECTION","SYMMETRIC MODEL"])
        h=self.section_header(1,"CORE IDEA: EQUAL DISTANCE TO THE MIRROR PLANE","The reflected feature is not placed by guessed coordinates; the plane is the exact geometric reference.")
        plane=DashedLine(UP*2.3,DOWN*2.3,color=BLACK,stroke_width=2.5,dash_length=.13); p=Dot(LEFT*3+UP*.5,color=BLACK,radius=.09); q=Dot(RIGHT*3+UP*.5,color=BLACK,radius=.09)
        d1=DoubleArrow(LEFT*3+UP*.1,UP*.1,buff=0,color=BLACK,stroke_width=2); d2=DoubleArrow(UP*.1,RIGHT*3+UP*.1,buff=0,color=BLACK,stroke_width=2)
        labs=VGroup(self.text("SOURCE",22,BOLD).next_to(p,UP),self.text("MIRROR",22,BOLD).next_to(q,UP),self.text("d",20,BOLD).next_to(d1,DOWN),self.text("d",20,BOLD).next_to(d2,DOWN)); self.fixed(labs)
        self.play(Create(plane),FadeIn(p),Create(d1),run_time=1); self.play(TransformFromCopy(p,q),Create(d2),FadeIn(labs),run_time=1.3); self.wait(EXPLAIN); self.clear_scene()
        body=self.base_plate_from_sketch(2,width=5.6,depth=3.2,height=.55,dims="90 × 52 mm",extrude="9 mm")
        h=self.section_header(3,"MODEL ONE SEED FEATURE — THEN MIRROR IT","The seed boss is fully defined on the left side. The central YZ plane generates the right-side feature."); self.fixed(h)
        self.move_camera(phi=5*DEGREES,theta=-90*DEGREES,zoom=1,run_time=1); plate=Rectangle(width=5.6,height=3.2,color=BLACK,stroke_width=3); circle=Circle(radius=.46,color=BLACK,stroke_width=4).move_to(LEFT*1.65); axis=DashedLine(UP*1.6,DOWN*1.6,color=MID_GRAY,stroke_width=2,dash_length=.12)
        lab=self.text("Ø16 mm   |   center 28 mm from symmetry plane",21,BOLD).to_edge(DOWN,buff=.34); self.fixed(lab); self.play(FadeOut(body),FadeIn(plate),Create(axis),Create(circle),FadeIn(lab),run_time=1.2); self.wait(READ)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); base=cuboid(5.6,3.2,.55,.56); seed=cylinder(.46,.55,.62).shift(LEFT*1.65+OUT*.55); self.play(FadeOut(plate),FadeOut(axis),FadeOut(circle),FadeOut(lab),FadeIn(base),FadeIn(seed),run_time=1.1)
        plane3=Rectangle(width=3.9,height=2.5,stroke_color=BLACK,stroke_width=1.6,fill_color=LIGHT_GRAY,fill_opacity=.18).rotate(PI/2,axis=UP)
        card=self.parameter_card("MIRROR",[("Features","Boss1"),("Mirror Plane","YZ Plane"),("Operation","Join")]); self.play(FadeIn(plane3),FadeIn(card),run_time=.9); self.wait(READ)
        ghost=seed.copy().set_opacity(.24); self.add(ghost); self.play(ghost.animate.shift(RIGHT*3.30),run_time=2.2,rate_func=smooth); mirror=ghost.copy().set_opacity(.62); self.play(ReplacementTransform(ghost,mirror),FadeOut(card),run_time=.75); self.play(FadeOut(plane3),run_time=.4)
        note=self.note("PROFESSIONAL HABIT",["Mirror features, not manually redrawn sketches.","Use a stable origin or work plane.","Edit the seed and both sides update."],width=6).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("SOURCE FEATURE + PLANE = PARAMETRIC MIRROR")
