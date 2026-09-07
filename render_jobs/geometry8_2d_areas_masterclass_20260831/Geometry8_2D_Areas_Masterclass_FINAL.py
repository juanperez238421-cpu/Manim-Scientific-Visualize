#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Period III — Area of 2D Figures.
Direct continuation of the audited Circle classroom sequence.
Target: ManimCE 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations
import math, os
import numpy as np
from manim import *

config.pixel_width=1920
config.pixel_height=1080
config.frame_width=16
config.frame_height=9
config.frame_rate=30
config.background_color=WHITE

TS=float(os.getenv("LESSON_TIME_SCALE","1.0"))
INK=BLACK
MID="#777777"
LIGHT="#D8D8D8"
PAPER="#F5F5F5"
FILL="#ECECEC"

class Geometry8Areas2DMasterclassFinal(MovingCameraScene):
    """Geometry-first masterclass: derive, transform, calculate, verify."""
    def setup(self):
        super().setup(); self.camera.background_color=WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.validate_lesson_data()

    def validate_lesson_data(self):
        assert 5*3==15 and 4**2==16
        assert 6*3==18 and 0.5*6*4==12
        assert abs(math.pi*3**2-28.2743338823)<1e-8
        assert 36+6==42
        assert abs(100-9*math.pi-71.7256661177)<1e-8
        assert 2*(6+4)==20

    def play(self,*anims,**kw):
        if kw.get("run_time") is not None: kw["run_time"]*=TS
        return super().play(*anims,**kw)
    def wait(self,duration=1.0,*args,**kw):
        return super().wait(duration*TS,*args,**kw)

    def txt(self,s,size=34,bold=False):
        return Text(s,font_size=size,color=INK,weight=BOLD if bold else NORMAL,line_spacing=0.92)
    def eq(self,s,size=48):
        return MathTex(s,font_size=size,color=INK)
    def fit(self,m,w=14.4,h=5.9):
        if m.width>w: m.scale_to_fit_width(w)
        if m.height>h: m.scale_to_fit_height(h)
        return m
    def header(self,n,title,subtitle):
        b=RoundedRectangle(width=.82,height=.56,corner_radius=.1,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1)
        num=self.txt(f"{n:02d}",24,True).move_to(b)
        t=self.txt(title,39,True); self.fit(t,12.8,.62)
        row=VGroup(VGroup(b,num),t).arrange(RIGHT,buff=.24).to_edge(UP,buff=.16).to_edge(LEFT,buff=.46)
        rule=Line([-7.45,row.get_bottom()[1]-.09,0],[7.45,row.get_bottom()[1]-.09,0],color=LIGHT,stroke_width=2)
        s=self.txt(subtitle,25); self.fit(s,14.3,.62); s.next_to(rule,DOWN,buff=.08).align_to(row,LEFT)
        return VGroup(row,rule,s)
    def box(self,tex,w=6.0,size=54):
        r=RoundedRectangle(width=w,height=1.22,corner_radius=.13,stroke_color=INK,stroke_width=2,fill_color=PAPER,fill_opacity=1)
        e=self.eq(tex,size); self.fit(e,w-.5,.9); e.move_to(r); return VGroup(r,e)
    def note(self,title,lines,w=5.8):
        t=self.txt(title,30,True); body=VGroup(*[self.txt(x,27) for x in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.13)
        c=VGroup(t,body).arrange(DOWN,aligned_edge=LEFT,buff=.2); self.fit(c,w-.55,3.7)
        r=RoundedRectangle(width=w,height=max(1.4,c.height+.62),corner_radius=.13,stroke_color=INK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
        c.move_to(r).align_to(r,LEFT).shift(RIGHT*.28); return VGroup(r,c)
    def wipe(self):
        if self.mobjects: self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.5)
        self.remove(*list(self.mobjects)); self.camera.frame.set(width=16).move_to(ORIGIN)
    def grid(self,c,r,side=.72):
        g=VGroup()
        for j in range(r):
            for i in range(c):
                q=Square(side_length=side,stroke_color=MID,stroke_width=1.3,fill_color=FILL,fill_opacity=.75)
                q.move_to([(i-(c-1)/2)*side,(j-(r-1)/2)*side,0]); g.add(q)
        return g

    def construct(self):
        self.opening(); self.circle_bridge(); self.area_vs_perimeter(); self.unit_squares()
        self.rectangle(); self.square(); self.parallelogram(); self.triangle()
        self.extended_toolkit(); self.circle_area(); self.circle_parts(); self.formula_map()
        self.composite(); self.shaded_simple(); self.shaded_complex(); self.scaling()
        self.applied(); self.errors(); self.challenge(); self.summary(); self.surface_bridge()

    def opening(self):
        top=VGroup(self.txt("GEOMETRY 8 · PERIOD III",46,True),self.txt("AREA OF 2D FIGURES",68,True),self.txt("From measuring the circle to measuring any plane region",34)).arrange(DOWN,buff=.2).shift(UP*1.85)
        shapes=VGroup(Circle(.7,color=INK,stroke_width=4),Rectangle(width=1.5,height=1,color=INK,stroke_width=4),Square(1.08,color=INK,stroke_width=4),Polygon([-.65,-.45,0],[.65,-.45,0],[0,.6,0],color=INK,stroke_width=4),Polygon([-.7,-.48,0],[.52,-.48,0],[.8,.48,0],[-.42,.48,0],color=INK,stroke_width=4)).arrange(RIGHT,buff=.6).shift(DOWN*.55)
        c=self.txt("AREA = HOW MUCH 2D REGION IS COVERED",39,True).shift(DOWN*2.0)
        q=self.txt("Can different area formulas come from the same geometric idea?",31).shift(DOWN*2.75)
        self.play(Write(top[0]),run_time=.8); self.play(Write(top[1]),FadeIn(top[2]),run_time=1.2)
        self.play(LaggedStart(*[Create(s) for s in shapes],lag_ratio=.12),run_time=1.5)
        self.play(*[s.animate.set_fill(FILL,opacity=.72) for s in shapes],run_time=.7)
        self.play(FadeIn(c),run_time=.7); self.wait(1.7); self.play(FadeIn(q),run_time=.7); self.wait(2.8); self.wipe()

    def circle_bridge(self):
        h=self.header(1,"BRIDGE FROM THE CIRCLE","We already moved from diameter and circumference to the covered region of a circle."); self.add(h)
        c=Circle(2,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.4).shift(LEFT*3.4+DOWN*.35)
        r=Line(c.get_center(),c.get_right(),color=INK,stroke_width=4); d=Line(c.get_left(),c.get_right(),color=MID,stroke_width=3)
        labs=VGroup(self.eq("r",42).next_to(r,UP,buff=.08),self.eq("d=2r",38).next_to(d,DOWN,buff=.15))
        chain=VGroup(self.box(r"\pi=\frac{C}{d}",5.2,48),self.box(r"C=\pi d=2\pi r",5.2,48),self.box(r"A=\pi r^2",5.2,60)).arrange(DOWN,buff=.28).move_to(RIGHT*3.55+DOWN*.25)
        self.play(Create(c),Create(r),FadeIn(Dot(c.get_center(),color=INK)),run_time=1); self.play(Create(d),FadeIn(labs),run_time=.7)
        for x in chain: self.play(FadeIn(x,shift=UP*.05),run_time=.65); self.wait(.8)
        self.play(Circumscribe(chain[-1][1],color=GRAY),run_time=.9); self.wait(2.5); self.wipe()

    def area_vs_perimeter(self):
        h=self.header(2,"AREA VS PERIMETER","Perimeter measures the boundary; area measures the region inside it."); self.add(h)
        r=Rectangle(width=5.4,height=3.3,color=INK,stroke_width=6,fill_color=WHITE,fill_opacity=1).shift(LEFT*3.35+DOWN*.3)
        p=self.txt("PERIMETER = boundary length",31,True).next_to(r,DOWN,buff=.28)
        fill=r.copy().set_stroke(opacity=0).set_fill(FILL,opacity=.9); a=self.txt("AREA = covered region",31,True).next_to(r,DOWN,buff=.28)
        n=self.note("UNITS",["Perimeter: cm, m, km","Area: cm², m², km²","Area uses square units."],5.6).move_to(RIGHT*3.6+DOWN*.25)
        self.play(Create(r),run_time=.8); self.play(Indicate(r,color=GRAY),FadeIn(p),run_time=.8); self.wait(1.1)
        self.play(FadeOut(p),FadeIn(fill),FadeIn(a),run_time=.7); self.play(FadeIn(n),run_time=.7); self.wait(2.8); self.wipe()

    def unit_squares(self):
        h=self.header(3,"SQUARE UNITS","Area counts how many 1×1 squares cover a region without gaps or overlaps."); self.add(h)
        g=self.grid(5,3,.78).shift(LEFT*2.7+DOWN*.2); count=self.eq(r"5\times3=15\ \text{unit squares}",46).move_to(RIGHT*3.55+UP*.5); ans=self.box(r"A=15\ \text{units}^2",5.8,58).move_to(RIGHT*3.55+DOWN*.8)
        self.play(LaggedStart(*[FadeIn(x,scale=.85) for x in g],lag_ratio=.04),run_time=1.7); self.play(Write(count),run_time=.7); self.play(FadeIn(ans),run_time=.7); self.wait(2.6); self.wipe()

    def rectangle(self):
        h=self.header(4,"RECTANGLE — THE BASE MODEL","Rows × columns becomes base × height."); self.add(h)
        g=self.grid(5,3,.72).shift(LEFT*3.2+DOWN*.2); out=Rectangle(width=3.6,height=2.16,color=INK,stroke_width=5).move_to(g)
        rhs=VGroup(self.txt("5 squares per row",30),self.txt("3 rows",30),self.eq(r"5+5+5=3\cdot5",43),self.box(r"A=b\,h",5.2,64)).arrange(DOWN,buff=.28).move_to(RIGHT*3.5+DOWN*.05)
        self.play(LaggedStart(*[FadeIn(x) for x in g],lag_ratio=.03),Create(out),run_time=1.4)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.6)
        self.wait(2.3); self.wipe()

    def square(self):
        h=self.header(5,"SQUARE — A SPECIAL RECTANGLE","Equal base and height turn A = bh into A = s²."); self.add(h)
        s=Square(3.5,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.65).shift(LEFT*3.2+DOWN*.2)
        labs=VGroup(self.txt("s",36,True).next_to(s,DOWN,buff=.17),self.txt("s",36,True).next_to(s,LEFT,buff=.17))
        rhs=VGroup(self.eq(r"A=b\,h",50),self.eq(r"b=s,\quad h=s",45),self.box(r"A=s^2",5.2,66),self.txt("s = 4 cm → A = 16 cm²",30,True)).arrange(DOWN,buff=.3).move_to(RIGHT*3.4+DOWN*.05)
        self.play(Create(s),FadeIn(labs),run_time=.9)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.65)
        self.wait(2.4); self.wipe()

    def parallelogram(self):
        h=self.header(6,"PARALLELOGRAM — CUT AND TRANSLATE","Move one triangular piece; the area stays the same while the shape becomes a rectangle."); self.add(h)
        A=np.array([-5.5,-1.5,0]); B=np.array([-1,-1.5,0]); C=np.array([0,1.35,0]); D=np.array([-4.5,1.35,0])
        p=Polygon(A,B,C,D,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.62); cut=DashedLine([-4.5,-1.5,0],D,color=MID,stroke_width=3)
        tri=Polygon(A,[-4.5,-1.5,0],D,color=INK,stroke_width=4,fill_color=WHITE,fill_opacity=1)
        e=self.box(r"A=b\,h",5.4,64).move_to(RIGHT*4.2+DOWN*.1); same=self.txt("Same pieces → same area",31,True).move_to(RIGHT*4.2+UP*1.25)
        self.play(Create(p),Create(cut),run_time=.9); self.play(FadeIn(tri),run_time=.5); self.play(tri.animate.shift(RIGHT*4.5),run_time=1.2)
        rect=Rectangle(width=4.5,height=2.85,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.62).move_to([-2.25,-.075,0])
        self.play(ReplacementTransform(p,rect),FadeOut(cut),FadeOut(tri),run_time=.9); self.play(FadeIn(same),FadeIn(e),run_time=.7); self.wait(2.8); self.wipe()

    def triangle(self):
        h=self.header(7,"TRIANGLE — HALF OF A PARALLELOGRAM","Two equal triangles form a parallelogram with the same base and height."); self.add(h)
        tri=Polygon([-5.4,-1.5,0],[-1.2,-1.5,0],[-3.7,1.4,0],color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.65); cp=tri.copy().set_fill(WHITE,opacity=1)
        rhs=VGroup(self.txt("2 equal triangles",33,True),self.eq(r"2A_{\triangle}=b\,h",48),self.box(r"A_{\triangle}=\frac12b\,h",6.0,58)).arrange(DOWN,buff=.35).move_to(RIGHT*3.55+DOWN*.05)
        self.play(Create(tri),run_time=.8); self.play(TransformFromCopy(tri,cp),run_time=.6); self.play(cp.animate.rotate(PI).shift(RIGHT*1.0),run_time=1.2)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.6); self.wait(.7)
        self.wait(2.5); self.wipe()

    def extended_toolkit(self):
        h=self.header(8,"EXTENDED 2D AREA TOOLKIT","The same decomposition idea extends to trapezoids and rhombi."); self.add(h)
        t=Polygon([-6.2,-1.1,0],[-2.4,-1.1,0],[-3.2,1.2,0],[-5.4,1.2,0],color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.62)
        te=self.box(r"A=\frac{(b_1+b_2)h}{2}",6.1,50).move_to([-4.25,-2.45,0])
        rh=Polygon([2,0,0],[4,1.55,0],[6,0,0],[4,-1.55,0],color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.62); d1=DashedLine([2,0,0],[6,0,0],color=INK); d2=DashedLine([4,-1.55,0],[4,1.55,0],color=INK)
        re=self.box(r"A=\frac{d_1d_2}{2}",5.0,54).move_to([4,-2.45,0])
        self.play(Create(t),run_time=.8); self.play(FadeIn(te),run_time=.6); self.play(Create(rh),Create(d1),Create(d2),run_time=.8); self.play(FadeIn(re),run_time=.6); self.wait(3); self.wipe()

    def circle_area(self):
        h=self.header(9,"CIRCLE AREA — RECAP","Our earlier sector rearrangement gave base ≈ πr and height = r."); self.add(h)
        c=Circle(1.8,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.55).shift(LEFT*3.6+DOWN*.1)
        r=Line(c.get_center(),c.get_right(),color=INK,stroke_width=4); left=VGroup(c,r,self.eq("r",40).next_to(r,UP,buff=.08))
        rhs=VGroup(self.txt("sector rearrangement",31,True),self.eq(r"\text{base}\approx\pi r",44),self.eq(r"\text{height}=r",44),self.box(r"A=(\pi r)(r)=\pi r^2",6.2,56)).arrange(DOWN,buff=.3).move_to(RIGHT*3.45+DOWN*.05)
        self.play(Create(c),Create(r),FadeIn(left[2]),run_time=.9)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.65)
        self.wait(2.5); self.wipe()

    def circle_parts(self):
        h=self.header(10,"CIRCLE PARTS — FRACTIONS OF THE FULL AREA","Semicircles and quadrants use a fraction of A = πr²."); self.add(h)
        s=Sector(outer_radius=1.75,angle=PI,start_angle=0,color=INK,stroke_width=4,fill_color=FILL,fill_opacity=.75).shift(LEFT*4+DOWN*.1)
        q=Sector(outer_radius=1.75,angle=PI/2,start_angle=0,color=INK,stroke_width=4,fill_color=FILL,fill_opacity=.75).shift(RIGHT*2.9+DOWN*.1)
        e1=self.box(r"A_{semi}=\frac12\pi r^2",5.1,48).next_to(s,DOWN,buff=.25); e2=self.box(r"A_{quad}=\frac14\pi r^2",5.1,48).next_to(q,DOWN,buff=.25)
        self.play(Create(s),run_time=.7); self.play(FadeIn(e1),run_time=.55); self.play(Create(q),run_time=.7); self.play(FadeIn(e2),run_time=.55); self.wait(2.8); self.wipe()

    def formula_map(self):
        h=self.header(11,"ONE FAMILY OF AREA FORMULAS","See the relationships instead of memorizing isolated formulas."); self.add(h)
        data=[("RECTANGLE",r"A=bh"),("SQUARE",r"A=s^2"),("PARALLELOGRAM",r"A=bh"),("TRIANGLE",r"A=\frac12bh"),("CIRCLE",r"A=\pi r^2")]
        cards=VGroup()
        for name,f in data:
            r=RoundedRectangle(width=2.55,height=2.1,corner_radius=.12,stroke_color=INK,stroke_width=2,fill_color=PAPER,fill_opacity=1); c=VGroup(self.txt(name,23,True),self.eq(f,36)).arrange(DOWN,buff=.2).move_to(r); cards.add(VGroup(r,c))
        cards.arrange(RIGHT,buff=.25).shift(DOWN*.25)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.06) for c in cards],lag_ratio=.12),run_time=1.5); self.wait(3.8); self.wipe()

    def composite(self):
        h=self.header(12,"COMPOSITE FIGURES — ADD KNOWN AREAS","Break one unfamiliar figure into familiar pieces, then add."); self.add(h)
        L=Polygon([-5.5,-2,0],[-.7,-2,0],[-.7,-.1,0],[-2.5,-.1,0],[-2.5,1.7,0],[-5.5,1.7,0],color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.65); split=DashedLine([-2.5,-2,0],[-2.5,-.1,0],color=MID,stroke_width=3)
        rhs=VGroup(self.txt("Decompose into 2 rectangles",31,True),self.eq(r"A_1=6\cdot6=36",42),self.eq(r"A_2=2\cdot3=6",42),self.box(r"A_{total}=36+6=42",6.0,52)).arrange(DOWN,buff=.28).move_to(RIGHT*3.5+DOWN*.05)
        self.play(Create(L),Create(split),run_time=.9)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.6)
        self.wait(2.5); self.wipe()

    def shaded_simple(self):
        h=self.header(13,"SIMPLE SHADED AREA — WHOLE MINUS MISSING","Write the subtraction before substituting numbers."); self.add(h)
        sq=Square(4.5,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.72).shift(LEFT*3.2+DOWN*.1); c=Circle(1.35,color=INK,stroke_width=5,fill_color=WHITE,fill_opacity=1).move_to(sq)
        rhs=VGroup(self.txt("Square side = 10 cm",30,True),self.txt("Circle radius = 3 cm",30,True),self.eq(r"A_s=10^2-\pi(3)^2",44),self.box(r"A_s\approx71.73\ \mathrm{cm}^2",6.1,48)).arrange(DOWN,buff=.28).move_to(RIGHT*3.45+DOWN*.05)
        self.play(Create(sq),Create(c),run_time=.9)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.6)
        self.wait(2.4); self.wipe()

    def shaded_complex(self):
        h=self.header(14,"COMPLEX SHADED AREA — SIMPLIFY FIRST","Recognize repeated pieces before calculating."); self.add(h)
        sq=Square(4.7,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.72).shift(LEFT*3.2+DOWN*.05); corners=[sq.get_corner(DL),sq.get_corner(DR),sq.get_corner(UR),sq.get_corner(UL)]; starts=[0,PI/2,PI,3*PI/2]
        sectors=VGroup(*[Sector(arc_center=c,outer_radius=2.35,angle=PI/2,start_angle=a,stroke_color=INK,stroke_width=3,fill_color=WHITE,fill_opacity=1) for c,a in zip(corners,starts)])
        rhs=VGroup(self.txt("4 quadrants = 1 full circle",30,True),self.eq(r"A_s=12^2-\pi(6)^2",44),self.box(r"A_s=144-36\pi\approx30.90",6.1,48)).arrange(DOWN,buff=.34).move_to(RIGHT*3.45+DOWN*.05)
        self.play(Create(sq),LaggedStart(*[FadeIn(s) for s in sectors],lag_ratio=.1),run_time=1.1)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.58); self.wait(.65)
        self.wait(2.5); self.wipe()

    def scaling(self):
        h=self.header(15,"SCALING — PERIMETER × k, AREA × k²","Doubling every length doubles perimeter but quadruples area."); self.add(h)
        a=Rectangle(width=2.4,height=1.8,color=INK,stroke_width=5,fill_color=WHITE,fill_opacity=1).move_to(LEFT*4.6+DOWN*.15); b=Rectangle(width=4.8,height=3.6,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.65).move_to(LEFT*1+DOWN*.15)
        la=self.txt("4×3: P=14, A=12",27,True).next_to(a,DOWN,buff=.15); lb=self.txt("8×6: P=28, A=48",27,True).next_to(b,DOWN,buff=.15); rule=VGroup(self.box(r"P'=kP",4.6,52),self.box(r"A'=k^2A",4.6,52)).arrange(DOWN,buff=.32).move_to(RIGHT*4.7+DOWN*.1)
        self.play(Create(a),FadeIn(la),run_time=.8); self.play(TransformFromCopy(a,b),FadeIn(lb),run_time=1); self.play(FadeIn(rule),run_time=.7); self.wait(3.2); self.wipe()

    def applied(self):
        h=self.header(16,"APPLIED 2D PROBLEM — FLOOR AND BORDER","Decide whether the question asks for surface, boundary, or both."); self.add(h)
        floor=Rectangle(width=5.3,height=3.3,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.65).shift(LEFT*3.3+DOWN*.1); labs=VGroup(self.txt("6 m",30,True).next_to(floor,DOWN,buff=.16),self.txt("4 m",30,True).next_to(floor,LEFT,buff=.16).rotate(PI/2))
        rhs=VGroup(self.txt("Tiles cover inside → AREA",30,True),self.eq(r"A=6\cdot4=24\ \mathrm{m}^2",43),self.txt("Trim follows edge → PERIMETER",30,True),self.eq(r"P=2(6+4)=20\ \mathrm{m}",43)).arrange(DOWN,buff=.3).move_to(RIGHT*3.4+DOWN*.05)
        self.play(Create(floor),FadeIn(labs),run_time=.9)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.65)
        self.wait(2.4); self.wipe()

    def errors(self):
        h=self.header(17,"COMMON ERRORS","Check the geometry before trusting the arithmetic."); self.add(h)
        cards=VGroup(self.note("ERROR 1",["Slanted side ≠ height","Height is perpendicular."],4.25),self.note("ERROR 2",["cm is not cm²","Area uses square units."],4.25),self.note("ERROR 3",["Missing region? subtract.","Whole − missing."],4.25)).arrange(RIGHT,buff=.3).shift(DOWN*.3)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.06) for c in cards],lag_ratio=.13),run_time=1.3); self.wait(3.8); self.wipe()

    def challenge(self):
        h=self.header(18,"STUDENT CHALLENGE","Pause: write the structure first, then calculate."); self.add(h)
        shape=VGroup(Rectangle(width=5.3,height=3.5,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.7),Circle(.95,color=INK,stroke_width=5,fill_color=WHITE,fill_opacity=1)).shift(LEFT*3.25+DOWN*.1)
        p=self.note("CHALLENGE",["Rectangle: 14 cm × 8 cm","Circular hole: r = 4 cm","Find shaded area + outer perimeter."],6.0).move_to(RIGHT*3.55+DOWN*.05)
        self.play(Create(shape[0]),Create(shape[1]),FadeIn(p),run_time=1); self.wait(6)
        a=self.box(r"A_s=112-16\pi\quad;\quad P_{outer}=44",7.0,45).move_to(RIGHT*3.55+DOWN*2.35); self.play(FadeIn(a),run_time=.7); self.wait(3); self.wipe()

    def summary(self):
        h=self.header(19,"FINAL METHOD","See the region first; arithmetic comes last."); self.add(h)
        labels=["1 · IDENTIFY REGION","2 · NAME SIMPLE SHAPES","3 · ADD OR SUBTRACT","4 · WRITE RELATION","5 · SUBSTITUTE","6 · CHECK SQUARE UNITS"]
        cards=VGroup()
        for s in labels:
            r=RoundedRectangle(width=4.2,height=1.3,corner_radius=.12,stroke_color=INK,stroke_width=2,fill_color=PAPER,fill_opacity=1); t=self.txt(s,27,True); self.fit(t,3.8,.85); t.move_to(r); cards.add(VGroup(r,t))
        cards.arrange_in_grid(rows=2,cols=3,buff=(.32,.32)).shift(DOWN*.2)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.05) for c in cards],lag_ratio=.1),run_time=1.4); self.wait(3.5)
        f=self.txt("SEE → TRANSFORM → CALCULATE → VERIFY → INTERPRET",35,True).to_edge(DOWN,buff=.34); self.play(FadeIn(f),run_time=.6); self.wait(3); self.wipe()

    def surface_bridge(self):
        h=self.header(20,"NEXT: 3D SURFACE AREA","A solid can be unfolded into 2D faces; surface area is the sum of those face areas."); self.add(h)
        net=VGroup(*[Square(1.12,color=INK,stroke_width=3,fill_color=FILL,fill_opacity=.62) for _ in range(6)]); pts=[(-1.12,0),(0,0),(1.12,0),(2.24,0),(0,1.12),(0,-1.12)]
        for m,(x,y) in zip(net,pts): m.move_to([x,y,0])
        net.shift(LEFT*3.3+DOWN*.1); rhs=VGroup(self.txt("Each face is a 2D region",31,True),self.eq(r"SA=A_1+A_2+\cdots+A_n",46),self.txt("Today's area toolkit becomes the 3D toolkit.",30)).arrange(DOWN,buff=.36).move_to(RIGHT*3.45+DOWN*.05)
        self.play(LaggedStart(*[FadeIn(f) for f in net],lag_ratio=.1),run_time=1.2)
        for x in rhs: self.play(FadeIn(x,shift=UP*.04),run_time=.55); self.wait(.65)
        self.wait(3); end=self.txt("GEOMETRY 8 · PERIOD III · 2D AREA TOOLKIT COMPLETE",34,True).to_edge(DOWN,buff=.32); self.play(FadeIn(end),run_time=.7); self.wait(3)

# Preview: LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_Masterclass_FINAL.py Geometry8Areas2DMasterclassFinal --fps 15 --disable_caching
# Final:   LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_Masterclass_FINAL.py Geometry8Areas2DMasterclassFinal --fps 30 --disable_caching
