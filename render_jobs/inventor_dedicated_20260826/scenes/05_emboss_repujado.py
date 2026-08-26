from manim import *
from library.inventor_pro_ui import *

class InventorEmbossDetailed(JPMiscCADScene):
    OPERATION="Emboss / Repujado"
    def construct(self):
        self.opening("REPUJADO  •  EMBOSS","Project a closed sketch on a face and raise or sink it by a controlled depth.",["FACE","CLOSED SKETCH","DEPTH","EMBOSSED FEATURE"])
        h=self.section_header(1,"CORE IDEA: THE PROFILE LIVES ON A FACE","Emboss uses a closed region. Positive depth raises it; negative direction creates an engraved/debossed detail.")
        face=Rectangle(width=5.8,height=3.2,color=BLACK,stroke_width=3); hexagon=RegularPolygon(6,radius=.85,color=BLACK,stroke_width=4); arrow=Arrow(DOWN*.15,UP*1.45,buff=.05,color=BLACK,stroke_width=3)
        labs=VGroup(self.text("CLOSED PROFILE",22,BOLD).next_to(hexagon,DOWN,buff=.3),self.text("+3 mm",22,BOLD).next_to(arrow,RIGHT,buff=.2)); self.fixed(labs); self.play(Create(face),Create(hexagon),FadeIn(labs[0]),run_time=1.1); self.play(Create(arrow),FadeIn(labs[1]),run_time=.8); self.wait(EXPLAIN); self.clear_scene()
        body=self.base_plate_from_sketch(2,width=5.6,depth=3.2,height=.55,dims="90 × 52 mm",extrude="9 mm")
        h=self.section_header(3,"DRAW THE EMBOSS PROFILE ON THE TOP FACE","Use the finished face as Sketch2 plane. Close and constrain the profile before creating the feature."); self.fixed(h)
        self.move_camera(phi=5*DEGREES,theta=-90*DEGREES,zoom=1,run_time=1); plate=Rectangle(width=5.6,height=3.2,color=BLACK,stroke_width=3); logo=RegularPolygon(6,radius=.82,color=BLACK,stroke_width=4); center=Dot(ORIGIN,color=BLACK,radius=.06); dim=self.text("Hexagon: 24 mm across flats   |   centered",21,BOLD).to_edge(DOWN,buff=.34); self.fixed(dim)
        self.play(FadeOut(body),FadeIn(plate),Create(logo),FadeIn(center),FadeIn(dim),run_time=1.2); self.wait(EXPLAIN)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); self.play(FadeOut(plate),FadeOut(logo),run_time=.35); base=cuboid(5.6,3.2,.55,.56); self.play(FadeIn(base),run_time=.6)
        pts=[[.82*math.cos(a),.82*math.sin(a),.275] for a in np.linspace(0,TAU,6,endpoint=False)]; emblem=extruded_polygon(pts,.24,.20); self.play(FadeIn(emblem),run_time=1.5)
        card=self.parameter_card("EMBOSS",[("Profile","Sketch2 region"),("Depth","3 mm"),("Direction","Positive"),("Operation","Emboss")]); self.play(FadeIn(card),run_time=.8); self.wait(EXPLAIN); final=extruded_polygon(pts,.24,.62); self.play(Transform(emblem,final),FadeOut(card),run_time=.8)
        note=self.note("WHEN TO USE IT",["Logos and identification marks.","Raised grip or decorative geometry.","Shallow face detail without a tall extrusion."],width=6).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("FACE + CLOSED PROFILE + DEPTH = EMBOSS")
