from manim import *
from library.inventor_pro_ui import *

class InventorRibDetailed(JPMiscCADScene):
    OPERATION="Rib / Nervio"
    def construct(self):
        self.opening("NERVIO  •  RIB","Create a thin structural wall from an open sketch line and terminate it against existing faces.",["OPEN SKETCH","THICKNESS","EXTENT","STRUCTURAL RIB"])
        h=self.section_header(1,"CORE IDEA: RIB STARTS FROM AN OPEN LINE","The line defines the structural path; thickness and extent turn that line into material.")
        line=Line(LEFT*3.8+DOWN*1.3,RIGHT*.2+UP*1.4,color=BLACK,stroke_width=5); ghost=line.copy().set_stroke(width=18,opacity=.18); lab=self.text("OPEN SKETCH LINE → THIN WALL",24,BOLD).to_edge(DOWN,buff=.35); self.fixed(lab)
        self.play(Create(line),FadeIn(lab),run_time=1.1); self.play(FadeIn(ghost),run_time=1.1); self.wait(EXPLAIN); self.clear_scene()
        h=self.section_header(2,"BUILD THE HOST SOLID FIRST","As in House: existing geometry comes first. The rib reinforces a base plate and a vertical wall."); self.fixed(h); self.set_camera_orientation(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9)
        base=cuboid(5.4,3.2,.45,.56).shift(DOWN*.3); wall=cuboid(.45,3.2,2.7,.56).shift(LEFT*2.48+OUT*1.35+DOWN*.3); self.play(FadeIn(base),run_time=.9); self.play(FadeIn(wall),run_time=.9); self.wait(READ)
        self.move_camera(phi=0,theta=-90*DEGREES,zoom=1,run_time=1.1); side_base=Rectangle(width=5.4,height=.45,color=BLACK,stroke_width=3).shift(DOWN*1.1); side_wall=Rectangle(width=.45,height=2.7,color=BLACK,stroke_width=3).move_to(LEFT*2.48+UP*.25); ribline=Line(LEFT*2.22+DOWN*.88,LEFT*.15+UP*1.35,color=BLACK,stroke_width=5)
        dims=VGroup(self.text("OPEN LINE",22,BOLD).next_to(ribline,RIGHT,buff=.25),self.text("Thickness = 6 mm",22,BOLD).to_edge(DOWN,buff=.34)); self.fixed(dims); self.play(FadeOut(base),FadeOut(wall),FadeIn(side_base),FadeIn(side_wall),Create(ribline),FadeIn(dims),run_time=1.3); self.wait(EXPLAIN)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); self.play(FadeOut(side_base),FadeOut(side_wall),FadeOut(ribline),run_time=.4); base=cuboid(5.4,3.2,.45,.56).shift(DOWN*.3); wall=cuboid(.45,3.2,2.7,.56).shift(LEFT*2.48+OUT*1.35+DOWN*.3); self.play(FadeIn(base),FadeIn(wall),run_time=.6)
        seed=Line3D([-2.25,0,0],[-.15,0,1.9],color=BLACK,thickness=.035); self.play(Create(seed),run_time=.7)
        rib=VGroup(Polygon(np.array([-2.25,-.26,-.05]),np.array([-2.25,-.26,1.95]),np.array([-.15,-.26,-.05]),fill_color=GRAY_C,fill_opacity=.56,stroke_color=GRAY_B),Polygon(np.array([-2.25,.26,-.05]),np.array([-2.25,.26,1.95]),np.array([-.15,.26,-.05]),fill_color=GRAY_C,fill_opacity=.56,stroke_color=GRAY_B),Polygon(np.array([-2.25,-.26,1.95]),np.array([-2.25,.26,1.95]),np.array([-.15,.26,-.05]),np.array([-.15,-.26,-.05]),fill_color=GRAY_C,fill_opacity=.56,stroke_color=GRAY_B))
        self.play(FadeIn(rib),seed.animate.set_opacity(.25),run_time=1.6); card=self.parameter_card("RIB",[("Profile","Open Line"),("Thickness","6 mm"),("Direction","Symmetric"),("Extent","To Next")]); self.play(FadeIn(card),run_time=.75); self.wait(EXPLAIN); self.play(FadeOut(card),FadeOut(seed),run_time=.4)
        note=self.note("STRUCTURAL REASONING",["Rib increases stiffness with little material.","Thickness is much smaller than height.","To Next keeps termination attached to the host."],width=6.2).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("OPEN SKETCH + THICKNESS + EXTENT = RIB")
