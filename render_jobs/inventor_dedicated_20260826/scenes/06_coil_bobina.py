from manim import *
from library.inventor_pro_ui import *

class InventorCoilDetailed(JPMiscCADScene):
    OPERATION="Coil / Bobina"
    def construct(self):
        self.opening("BOBINA  •  COIL","Move a profile around an axis while advancing along it: rotation + translation = helix.",["PROFILE","AXIS","PITCH","REVOLUTIONS","HELIX"])
        h=self.section_header(1,"CORE IDEA: ONE REVOLUTION ADVANCES ONE PITCH","Total height is controlled by pitch p and revolution count N: H = pN.")
        circle=Circle(radius=1.15,color=BLACK,stroke_width=3).shift(LEFT*3.5); arrow=Arrow(LEFT*3.5+DOWN*1.8,LEFT*3.5+UP*1.8,buff=0,color=BLACK,stroke_width=3); formula=MathTex(r"H=p\,N",color=BLACK,font_size=52).move_to(RIGHT*3.4+UP*.6); ex=self.text("p = 12 mm,  N = 4  →  H = 48 mm",26,BOLD).move_to(RIGHT*3.4+DOWN*.7); self.fixed(formula,ex)
        self.play(Create(circle),Create(arrow),run_time=1.1); self.play(Write(formula),FadeIn(ex),run_time=1); self.wait(EXPLAIN); self.clear_scene()
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1); h=self.section_header(2,"SKETCH PROFILE + AXIS BEFORE CLICKING COIL","The small circle is the wire section. The centerline is the helical axis."); self.fixed(h)
        axis=DashedLine(DOWN*2.4,UP*2.4,color=BLACK,stroke_width=2.5,dash_length=.12); prof=Circle(radius=.34,color=BLACK,stroke_width=4).move_to(RIGHT*2+DOWN*1.8); radial=Line(DOWN*1.8,RIGHT*2+DOWN*1.8,color=MID_GRAY,stroke_width=2)
        labs=VGroup(self.text("AXIS",21,BOLD).next_to(axis,LEFT,buff=.2),self.text("Ø6 mm PROFILE",21,BOLD).next_to(prof,RIGHT,buff=.2),self.text("R = 20 mm",21,BOLD).next_to(radial,UP,buff=.15)); self.fixed(labs); self.play(Create(axis),Create(radial),Create(prof),FadeIn(labs),run_time=1.3); self.wait(EXPLAIN)
        card=self.parameter_card("COIL",[("Pitch","12 mm"),("Revolutions","4"),("Section","Ø6 mm"),("Operation","New Solid")]); self.play(FadeIn(card),run_time=.8); self.wait(READ); self.play(FadeOut(card),run_time=.35)
        self.move_camera(phi=67*DEGREES,theta=-48*DEGREES,zoom=.88,run_time=1.2); self.play(FadeOut(axis),FadeOut(prof),run_time=.35); axis3=DashedLine([0,0,-2.4],[0,0,2.4],dash_length=.12,color=BLACK,stroke_width=2.2); self.play(Create(axis3),run_time=.7)
        turns=4; radius=2.; height=4.8; helix=ParametricFunction(lambda t: np.array([radius*math.cos(t),radius*math.sin(t),-height/2+height*t/(turns*TAU)]),t_range=[0,turns*TAU],color=BLACK,stroke_width=11); guide=helix.copy().set_stroke(width=2,opacity=.18); self.add(guide); self.play(Create(helix),run_time=4,rate_func=linear)
        pitch=self.text("pitch = 12 mm",22,BOLD).to_corner(DR,buff=.55).shift(UP*.7); self.fixed(pitch); self.play(FadeIn(pitch),run_time=.7); self.wait(EXPLAIN); self.play(FadeOut(pitch),run_time=.3)
        note=self.note("COIL CONTROLS",["Pitch controls spacing between turns.","Revolutions control turn count.","Profile size controls wire/thread thickness."],width=5.9).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("PROFILE + AXIS + PITCH + REVOLUTIONS = COIL")
