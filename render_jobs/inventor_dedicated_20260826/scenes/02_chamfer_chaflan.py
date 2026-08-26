from manim import *
from library.inventor_pro_ui import *

class InventorChamferDetailed(JPMiscCADScene):
    OPERATION="Chamfer / Chaflán"
    def construct(self):
        self.opening("CHAFLÁN  •  CHAMFER","Replace a sharp corner with a flat bevel controlled by distance and angle.",["EDGE","DISTANCE","ANGLE","BEVELED SOLID"])
        h=self.section_header(1,"CORE IDEA: CHAMFER CREATES A FLAT TRANSITION","Unlike Fillet, the new transition is planar; a straight cutting line removes the corner in section.")
        sharp=VGroup(Line(LEFT*5+DOWN,LEFT*3+DOWN,color=BLACK,stroke_width=5),Line(LEFT*3+DOWN,LEFT*3+UP,color=BLACK,stroke_width=5))
        bevel=VGroup(Line(RIGHT*0+DOWN,RIGHT*1+DOWN,color=BLACK,stroke_width=5),Line(RIGHT*2,RIGHT*2+UP,color=BLACK,stroke_width=5),Line(RIGHT*1+DOWN,RIGHT*2,color=BLACK,stroke_width=5))
        labs=VGroup(self.text("SHARP",23,BOLD).move_to(LEFT*4+DOWN*2),self.text("6 mm × 45°",23,BOLD).move_to(RIGHT*1.3+DOWN*2)); self.fixed(labs)
        self.play(Create(sharp),FadeIn(labs[0]),run_time=1); self.play(TransformFromCopy(sharp,bevel),FadeIn(labs[1]),run_time=1.4); self.wait(EXPLAIN); self.clear_scene()
        body=self.base_plate_from_sketch(2,width=5,depth=3,height=.72,dims="80 × 48 mm",extrude="12 mm")
        h=self.section_header(3,"SELECT THE CORNER EDGES TO BE BEVELED","This example chamfers the four vertical corners after Extrusion1 is complete."); self.fixed(h)
        edges=VGroup(*[Line3D([sx*2.5,sy*1.5,-.36],[sx*2.5,sy*1.5,.36],color=BLACK,thickness=.035) for sx,sy in [(1,1),(-1,1),(-1,-1),(1,-1)]])
        card=self.parameter_card("CHAMFER",[("Selection","4 Edges"),("Type","Distance + Angle"),("Distance","6 mm"),("Angle","45 deg")]); self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.16),FadeIn(card),run_time=1.35); self.wait(READ)
        self.play(FadeOut(card),run_time=.3); self.move_camera(phi=5*DEGREES,theta=-90*DEGREES,zoom=1,run_time=1)
        top=Rectangle(width=5,height=3,color=BLACK,stroke_width=4); self.play(FadeOut(body),FadeOut(edges),FadeIn(top),run_time=.7)
        w,d,c=2.5,1.5,.40; cuts=VGroup(Line([w-c,d,0],[w,d-c,0],color=BLACK,stroke_width=4),Line([-w+c,d,0],[-w,d-c,0],color=BLACK,stroke_width=4),Line([-w+c,-d,0],[-w,-d+c,0],color=BLACK,stroke_width=4),Line([w-c,-d,0],[w,-d+c,0],color=BLACK,stroke_width=4))
        self.play(LaggedStart(*[Create(x) for x in cuts],lag_ratio=.18),run_time=1.5)
        pts=[[-w+c,-d,0],[w-c,-d,0],[w,-d+c,0],[w,d-c,0],[w-c,d,0],[-w+c,d,0],[-w,d-c,0],[-w,-d+c,0]]; poly=Polygon(*[np.array(p) for p in pts],color=BLACK,stroke_width=4)
        self.play(FadeOut(top),FadeOut(cuts),FadeIn(poly),run_time=1); self.wait(READ)
        self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=.9,run_time=1.1); result=chamfered_plate(5,3,.72,.40,.60); self.play(FadeOut(poly),FadeIn(result),run_time=1.25)
        note=self.note("WHY CHAMFER?",["Break a dangerous sharp edge.","Create assembly lead-in geometry.","Prepare edges for manufacturing."],width=5.8).to_corner(DR,buff=.45).shift(UP*.45); self.fixed(note); self.play(FadeIn(note),run_time=.8); self.wait(EXPLAIN); self.play(FadeOut(note),FadeOut(h),run_time=.4)
        self.final_orbit("EDGE + DISTANCE / ANGLE = CHAMFERED FEATURE")
