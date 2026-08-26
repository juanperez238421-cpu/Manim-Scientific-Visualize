from manim import *
from library.inventor_pro_ui import *

class InventorCircularPatternDetailed(JPMiscCADScene):
    OPERATION="Circular Pattern / Patrón circular"
    def construct(self):
        self.opening("PATRÓN CIRCULAR  •  CIRCULAR PATTERN","Repeat one seed feature around an axis using angular extent and occurrence count.",["SEED FEATURE","AXIS","ANGLE","QUANTITY","CIRCULAR PATTERN"])
        h=self.section_header(1,"CORE IDEA: THE AXIS DEFINES THE CENTER OF REPETITION","For a full pattern, angular step = 360° / quantity. Here: 360° / 8 = 45°.")
        ring=Circle(radius=2,color=LIGHT_GRAY,stroke_width=2); center=Dot(ORIGIN,color=BLACK,radius=.08); seed=Circle(radius=.30,color=BLACK,stroke_width=4).move_to(RIGHT*2); copies=VGroup(*[seed.copy().rotate(k*45*DEGREES,about_point=ORIGIN) for k in range(1,8)]); formula=MathTex(r"\Delta\theta=\frac{360^\circ}{8}=45^\circ",color=BLACK,font_size=48).to_edge(DOWN,buff=.35); self.fixed(formula)
        self.play(Create(ring),FadeIn(center),Create(seed),run_time=1); self.play(LaggedStart(*[TransformFromCopy(seed,c) for c in copies],lag_ratio=.14),run_time=2.5); self.play(Write(formula),run_time=.8); self.wait(EXPLAIN); self.clear_scene()
        h=self.section_header(2,"BUILD THE HOST DISK AND ONE SEED FEATURE","The host exposes a stable central Z axis. Only the first boss is modeled manually."); self.fixed(h); self.set_camera_orientation(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9)
        disk=cylinder(2.85,.48,.56); seed3=cylinder(.34,.50,.62).shift(RIGHT*1.85+OUT*.49); axis=DashedLine([0,0,-1.2],[0,0,1.6],dash_length=.12,color=BLACK,stroke_width=2.2); self.play(FadeIn(disk),run_time=.9); self.play(FadeIn(seed3),Create(axis),run_time=.9); self.wait(READ)
        card=self.parameter_card("CIRCULAR PATTERN",[("Features","Boss1"),("Rotation Axis","Z Axis"),("Placement","Full"),("Quantity","8")]); self.play(FadeIn(card),run_time=.8); self.wait(READ)
        for k in range(1,8): self.play(TransformFromCopy(seed3,seed3.copy().rotate(k*45*DEGREES,axis=OUT,about_point=ORIGIN)),run_time=.48)
        self.wait(READ); self.play(FadeOut(card),run_time=.35)
        note=self.note("DESIGN CHECK",["Axis must be stable and intentional.","Full pattern distributes occurrences uniformly.","Changing quantity recalculates angular spacing."],width=6).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("SEED + AXIS + ANGLE + QUANTITY = CIRCULAR PATTERN")
