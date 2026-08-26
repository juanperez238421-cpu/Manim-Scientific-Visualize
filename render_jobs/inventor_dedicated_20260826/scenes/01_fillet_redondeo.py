from manim import *
from library.inventor_pro_ui import *

class InventorFilletDetailed(JPMiscCADScene):
    OPERATION="Fillet / Redondeo"
    def construct(self):
        self.opening("REDONDEO  •  FILLET","Replace a sharp edge with a tangent radius after the base solid is understood.",["EDGE","RADIUS","TANGENCY","FILLETED SOLID"])
        h=self.section_header(1,"CORE IDEA: SHARP CORNER → TANGENT ARC","Fillet is local geometry: the original faces remain while their sharp intersection is replaced by radius R.")
        sharp=VGroup(Line(LEFT*5+DOWN,LEFT*3+DOWN,color=BLACK,stroke_width=5),Line(LEFT*3+DOWN,LEFT*3+UP,color=BLACK,stroke_width=5))
        arc=Arc(radius=1,start_angle=PI,angle=-PI/2,arc_center=RIGHT*2+ORIGIN,color=BLACK,stroke_width=5)
        legs=VGroup(Line(RIGHT*0+DOWN,RIGHT*1+DOWN,color=BLACK,stroke_width=5),Line(RIGHT*2,RIGHT*2+UP,color=BLACK,stroke_width=5),arc)
        labs=VGroup(self.text("SHARP",23,BOLD).move_to(LEFT*4+DOWN*2),self.text("R = 6 mm",23,BOLD).move_to(RIGHT*1.3+DOWN*2)); self.fixed(labs)
        self.play(Create(sharp),FadeIn(labs[0]),run_time=1); self.play(TransformFromCopy(sharp,legs),FadeIn(labs[1]),run_time=1.5); self.wait(EXPLAIN); self.clear_scene()
        body=self.base_plate_from_sketch(2,width=5,depth=3,height=.72,dims="80 × 48 mm",extrude="12 mm")
        h=self.section_header(3,"SELECT THE 3D EDGES THAT SHARE THE SAME RADIUS","The sketch is finished. Now work on existing edges of Extrusion1."); self.fixed(h)
        edges=VGroup(*[Line3D([sx*2.5,sy*1.5,-.36],[sx*2.5,sy*1.5,.36],color=BLACK,thickness=.035) for sx,sy in [(1,1),(-1,1),(-1,-1),(1,-1)]])
        card=self.parameter_card("FILLET",[("Selection","4 Edges"),("Radius","6 mm"),("Mode","Constant")]); self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.16),FadeIn(card),run_time=1.35); self.wait(READ)
        self.play(FadeOut(card),run_time=.3); self.move_camera(phi=5*DEGREES,theta=-90*DEGREES,zoom=1,run_time=1)
        top=Rectangle(width=5,height=3,color=BLACK,stroke_width=4); self.play(FadeOut(body),FadeOut(edges),FadeIn(top),run_time=.7)
        pts=[np.array(p) for p in rounded_rect_points(5,3,.42,10,0)]; rounded=VMobject(color=BLACK,stroke_width=4).set_points_as_corners(pts+[pts[0]])
        caption=self.text("TOP VIEW — corner geometry changes before the 3D reveal",23,BOLD).to_edge(DOWN,buff=.34); self.fixed(caption)
        self.play(FadeIn(caption),Transform(top,rounded),run_time=2.2); self.wait(READ); self.play(FadeOut(caption),run_time=.3)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); result=rounded_plate(5,3,.72,.42,.60)
        self.play(FadeOut(top),FadeIn(result),run_time=1.25)
        note=self.note("CHECK BEFORE OK",["Radius fits inside adjacent faces.","No nearby feature is consumed.","The transition stays tangent."],width=5.8).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("EDGE + RADIUS + TANGENCY = FILLETED FEATURE")
