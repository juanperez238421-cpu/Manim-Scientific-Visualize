#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sistema diédrico: first-angle vs third-angle + Colombia normative check.
Target: ManimCE 0.20.x, 1920x1080, 30 fps, white classroom background.
"""
from __future__ import annotations
import os
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
INK = "#111111"
DARK = "#303030"
MID = "#6C6C6C"
LIGHT = "#D8D8D8"
PAPER = "#F6F6F6"
PLANE = "#ECECEC"


class TimedScene(Scene):
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)


class DihedralISOProjectionNTC1777(TimedScene):
    def text(self, s, size=30, weight=NORMAL, color=INK):
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.92)

    def fit(self, mob, w=14.6, h=7.6):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def header(self, n, title, subtitle):
        box = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10,
                               stroke_color=INK, stroke_width=2,
                               fill_color=WHITE, fill_opacity=1)
        num = self.text(f"{n:02d}", 23, BOLD).move_to(box)
        ttl = self.text(title, 34, BOLD)
        row = VGroup(VGroup(box, num), ttl).arrange(RIGHT, buff=0.24)
        row.to_edge(UP, buff=0.18).to_edge(LEFT, buff=0.52)
        rule = Line(LEFT*7.45, RIGHT*7.45, color=LIGHT, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.08)
        sub = self.text(subtitle, 20, NORMAL, DARK)
        self.fit(sub, 14.2, 0.70)
        sub.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def clear(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)

    def pill(self, s, size=22):
        t = self.text(s, size, BOLD)
        b = RoundedRectangle(width=t.width+0.5, height=t.height+0.28,
                             corner_radius=0.14, stroke_color=INK,
                             stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
        t.move_to(b)
        return VGroup(b, t)

    def card(self, title, lines, width=6.1, height=3.0):
        t = self.text(title, 27, BOLD)
        body = VGroup(*[self.text(x, 22) for x in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        content = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        self.fit(content, width-0.55, height-0.45)
        b = RoundedRectangle(width=width, height=height, corner_radius=0.14,
                             stroke_color=INK, stroke_width=1.8,
                             fill_color=PAPER, fill_opacity=1)
        content.move_to(b).align_to(b, LEFT).shift(RIGHT*0.28)
        return VGroup(b, content)

    # ----------------------- object and view geometry -----------------------
    def iso(self, x, y, z, s=0.72):
        return s*(x*RIGHT + y*(0.55*RIGHT+0.36*UP) + z*UP)

    def stepped_object(self, s=0.72):
        boxes = [(0,3.6,0,2.4,0,0.75), (2.2,3.6,0,2.4,0.75,1.75), (2.8,3.6,0,2.4,1.75,2.75)]
        g = VGroup()
        for x0,x1,y0,y1,z0,z1 in boxes:
            p = lambda x,y,z: self.iso(x,y,z,s)
            g.add(Polygon(p(x0,y0,z0),p(x1,y0,z0),p(x1,y0,z1),p(x0,y0,z1),
                          stroke_color=INK,stroke_width=2.2,fill_color="#FBFBFB",fill_opacity=1))
            g.add(Polygon(p(x1,y0,z0),p(x1,y1,z0),p(x1,y1,z1),p(x1,y0,z1),
                          stroke_color=INK,stroke_width=2.2,fill_color="#E9E9E9",fill_opacity=1))
            g.add(Polygon(p(x0,y0,z1),p(x1,y0,z1),p(x1,y1,z1),p(x0,y1,z1),
                          stroke_color=INK,stroke_width=2.2,fill_color="#F2F2F2",fill_opacity=1))
        return g

    def front_view(self, s=0.72):
        pts=[LEFT*2+DOWN*1.15,RIGHT*2+DOWN*1.15,RIGHT*2+UP*1.75,RIGHT*1.15+UP*1.75,
             RIGHT*1.15+UP*0.65,RIGHT*0.35+UP*0.65,RIGHT*0.35+DOWN*0.35,LEFT*2+DOWN*0.35]
        p=Polygon(*[x*s for x in pts],stroke_color=INK,stroke_width=3,fill_color=WHITE,fill_opacity=1)
        e1=Line(RIGHT*0.35*s+DOWN*1.15*s,RIGHT*0.35*s+DOWN*0.35*s,color=INK,stroke_width=2)
        e2=Line(RIGHT*1.15*s+DOWN*1.15*s,RIGHT*1.15*s+UP*0.65*s,color=INK,stroke_width=2)
        return VGroup(p,e1,e2)

    def top_view(self, s=0.72):
        r=Rectangle(width=4*s,height=2.45*s,stroke_color=INK,stroke_width=3,fill_color=WHITE,fill_opacity=1)
        l1=Line(RIGHT*0.35*s+DOWN*1.225*s,RIGHT*0.35*s+UP*1.225*s,color=INK,stroke_width=2)
        l2=Line(RIGHT*1.15*s+DOWN*1.225*s,RIGHT*1.15*s+UP*1.225*s,color=INK,stroke_width=2)
        return VGroup(r,l1,l2)

    def right_view(self, s=0.72):
        r=Rectangle(width=2.45*s,height=2.90*s,stroke_color=INK,stroke_width=3,fill_color=WHITE,fill_opacity=1)
        l1=Line(LEFT*1.225*s+DOWN*0.38*s,RIGHT*1.225*s+DOWN*0.38*s,color=INK,stroke_width=2)
        l2=Line(LEFT*1.225*s+UP*0.65*s,RIGHT*1.225*s+UP*0.65*s,color=INK,stroke_width=2)
        return VGroup(r,l1,l2)

    def labeled_view(self, view, label, size=17):
        tag=self.pill(label,size).next_to(view,DOWN,buff=0.15)
        return VGroup(view,tag)

    def projection_symbol(self, third=True):
        fr=Polygon(LEFT*1.10+DOWN*0.55,LEFT*1.10+UP*0.55,RIGHT*0.78+UP*0.35,RIGHT*0.78+DOWN*0.35,
                   stroke_color=INK,stroke_width=2.6,fill_color=WHITE,fill_opacity=1)
        ax=DashedLine(LEFT*1.3,RIGHT*1.05,color=MID,stroke_width=1.2,dash_length=0.10)
        c=Circle(radius=0.56,stroke_color=INK,stroke_width=2.6,fill_color=WHITE,fill_opacity=1)
        cv=Line(UP*0.56,DOWN*0.56,color=MID,stroke_width=1).move_to(c)
        ch=Line(LEFT*0.56,RIGHT*0.56,color=MID,stroke_width=1).move_to(c)
        cg=VGroup(c,cv,ch)
        cg.next_to(fr,RIGHT if third else LEFT,buff=0.50)
        return VGroup(fr,ax,cg)

    def observer(self):
        eye=VGroup(Arc(radius=0.42,start_angle=0.10*PI,angle=0.80*PI,color=INK,stroke_width=2),
                   Arc(radius=0.42,start_angle=1.10*PI,angle=0.80*PI,color=INK,stroke_width=2),
                   Dot(radius=0.08,color=INK))
        return VGroup(eye,self.text("OBSERVER",18,BOLD).next_to(eye,DOWN,buff=0.10))

    def plane(self):
        r=Rectangle(width=1.05,height=4.0,stroke_color=INK,stroke_width=2.2,fill_color=PLANE,fill_opacity=0.75)
        return VGroup(r,self.text("PLANE",17,BOLD).rotate(PI/2).move_to(r))

    # ------------------------------- lesson -------------------------------
    def construct(self):
        self.opening(); self.dihedral(); self.six_views(); self.key_difference(); self.first_angle(); self.third_angle(); self.compare(); self.symbols(); self.colombia(); self.summary()

    def opening(self):
        g=VGroup(self.text("DIBUJO TÉCNICO Y CAD",24,BOLD,DARK),
                 self.text("SISTEMA DIÉDRICO",62,BOLD),
                 self.text("De un objeto 3D a vistas 2D — ISO A vs ISO E",30,NORMAL,DARK),
                 self.pill("MISMAS VISTAS · DISTINTO MÉTODO DE PROYECCIÓN",22)).arrange(DOWN,buff=0.34)
        self.play(FadeIn(g[0]),Write(g[1]),run_time=1.2); self.play(FadeIn(g[2]),FadeIn(g[3]),run_time=0.9); self.wait(3); self.clear()

    def dihedral(self):
        h=self.header(1,"THE DIHEDRAL IDEA","Two perpendicular planes turn a 3D object into orthographic 2D information."); self.add(h)
        obj=self.stepped_object(0.62).move_to(LEFT*0.6+DOWN*0.55)
        pv=Rectangle(width=0.14,height=4.6,stroke_color=INK,stroke_width=2,fill_color=PLANE,fill_opacity=0.7).move_to(LEFT*2.8+DOWN*0.2)
        ph=Polygon(LEFT*3+DOWN*1,RIGHT*3+DOWN*1,RIGHT*3.8+DOWN*2,LEFT*2.2+DOWN*2,stroke_color=INK,stroke_width=2,fill_color=PLANE,fill_opacity=0.7).shift(LEFT*0.1)
        note=self.card("WHAT THE PLANES RECORD",["PV → front view","PH → top view","Unfold both planes into one drawing."],5.0,2.75).move_to(RIGHT*4.45+DOWN*0.55)
        self.play(FadeIn(pv),FadeIn(ph),FadeIn(obj),run_time=1.0); self.play(FadeIn(note),run_time=0.8); self.wait(3.5)
        self.play(FadeIn(self.text("UNFOLD → FLAT ORTHOGRAPHIC DRAWING",25,BOLD).to_edge(DOWN,buff=0.28)),run_time=0.7); self.wait(2); self.clear()

    def six_views(self):
        h=self.header(2,"THE SIX PRINCIPAL VIEWS","Front, rear, top, bottom, left and right exist in both projection systems."); self.add(h)
        obj=self.stepped_object(0.55).move_to(DOWN*0.55); self.play(FadeIn(obj),run_time=0.8)
        items=[("FRONT",LEFT*4.6),("REAR",RIGHT*4.6),("TOP",UP*2.2),("BOTTOM",DOWN*2.9),("LEFT",LEFT*3+UP*1.8),("RIGHT",RIGHT*3+UP*1.8)]
        tags=VGroup(); arr=VGroup()
        for label,pos in items:
            t=self.pill(label,19).move_to(pos); tags.add(t); arr.add(Arrow(t.get_center(),obj.get_center(),buff=0.55,color=MID,stroke_width=2,max_tip_length_to_length_ratio=0.12))
        self.play(LaggedStart(*[FadeIn(x) for x in tags],lag_ratio=0.06),run_time=1.1); self.play(LaggedStart(*[GrowArrow(x) for x in arr],lag_ratio=0.05),run_time=1.1)
        c=self.card("KEY IDEA",["Same object.","Same six view directions.","Only the final placement changes."],4.6,2.55).to_edge(RIGHT,buff=0.5).shift(DOWN*1.25)
        self.play(FadeIn(c),run_time=0.8); self.wait(3.5); self.clear()

    def key_difference(self):
        h=self.header(3,"THE ONE DIFFERENCE TO REMEMBER","Where is the projection plane relative to the observer and the object?"); self.add(h)
        a=self.card("FIRST-ANGLE · ISO E",["Observer → Object → Plane","Object between observer and plane.","Views appear on the opposite side."],6.3,3.1)
        b=self.card("THIRD-ANGLE · ISO A",["Observer → Plane → Object","Plane between observer and object.","Views stay on the same side."],6.3,3.1)
        VGroup(a,b).arrange(RIGHT,buff=0.55).move_to(DOWN*0.25); self.play(FadeIn(a,shift=LEFT*0.15),FadeIn(b,shift=RIGHT*0.15),run_time=1); self.wait(4); self.clear()

    def first_angle(self):
        h=self.header(4,"FIRST-ANGLE PROJECTION","Common classroom label: ISO E / European. In NTC 1777: first-angle, formerly method E."); self.add(h)
        obs=self.observer().move_to(LEFT*5.3+DOWN*0.5); obj=self.stepped_object(0.45).move_to(LEFT*1.5+DOWN*0.55); pl=self.plane().move_to(RIGHT*1.5+DOWN*0.4)
        self.play(FadeIn(obs),FadeIn(obj),FadeIn(pl),run_time=1); self.play(GrowArrow(Arrow(obs.get_right(),obj.get_left(),buff=0.18,color=MID)),GrowArrow(Arrow(obj.get_right(),pl.get_left(),buff=0.18,color=MID)),run_time=0.8)
        note=self.card("AFTER UNFOLDING",["TOP → below FRONT","RIGHT view → left of FRONT","LEFT view → right of FRONT"],4.9,2.85).to_edge(RIGHT,buff=0.48).shift(DOWN*1.0); self.play(FadeIn(note),run_time=0.8); self.wait(3)
        f=self.labeled_view(self.front_view(0.40),"FRONT"); t=self.labeled_view(self.top_view(0.36),"TOP"); r=self.labeled_view(self.right_view(0.36),"RIGHT")
        f.move_to(ORIGIN); t.next_to(f,DOWN,buff=0.24); r.next_to(f,LEFT,buff=0.30); cluster=VGroup(f,t,r).scale(0.82).to_edge(RIGHT,buff=0.65).shift(UP*1.15)
        self.play(FadeIn(cluster),run_time=0.8); self.wait(2.5); self.clear()

    def third_angle(self):
        h=self.header(5,"THIRD-ANGLE PROJECTION","Common classroom label: ISO A / American. In NTC 1777: third-angle, formerly method A."); self.add(h)
        obs=self.observer().move_to(LEFT*5.3+DOWN*0.5); pl=self.plane().move_to(LEFT*1.5+DOWN*0.4); obj=self.stepped_object(0.45).move_to(RIGHT*1.9+DOWN*0.55)
        self.play(FadeIn(obs),FadeIn(pl),FadeIn(obj),run_time=1); self.play(GrowArrow(Arrow(obs.get_right(),pl.get_left(),buff=0.18,color=MID)),GrowArrow(Arrow(pl.get_right(),obj.get_left(),buff=0.18,color=MID)),run_time=0.8)
        note=self.card("AFTER UNFOLDING",["TOP → above FRONT","RIGHT view → right of FRONT","LEFT view → left of FRONT"],4.9,2.85).to_edge(RIGHT,buff=0.48).shift(DOWN*1.0); self.play(FadeIn(note),run_time=0.8); self.wait(3)
        f=self.labeled_view(self.front_view(0.40),"FRONT"); t=self.labeled_view(self.top_view(0.36),"TOP"); r=self.labeled_view(self.right_view(0.36),"RIGHT")
        f.move_to(ORIGIN); t.next_to(f,UP,buff=0.24); r.next_to(f,RIGHT,buff=0.30); cluster=VGroup(f,t,r).scale(0.82).to_edge(RIGHT,buff=0.65).shift(UP*0.35)
        self.play(FadeIn(cluster),run_time=0.8); self.wait(2.5); self.clear()

    def compare(self):
        h=self.header(6,"SAME VIEWS — DIFFERENT LAYOUT","Compare TOP and RIGHT relative to FRONT."); self.add(h)
        f1=self.labeled_view(self.front_view(0.39),"FRONT"); t1=self.labeled_view(self.top_view(0.35),"TOP"); r1=self.labeled_view(self.right_view(0.35),"RIGHT"); f1.move_to(ORIGIN); t1.next_to(f1,DOWN,buff=0.22); r1.next_to(f1,LEFT,buff=0.28); g1=VGroup(f1,t1,r1).scale(0.82); l1=self.pill("FIRST-ANGLE · ISO E",20).next_to(g1,UP,buff=0.25); G1=VGroup(g1,l1).move_to(LEFT*4+DOWN*0.5)
        f2=self.labeled_view(self.front_view(0.39),"FRONT"); t2=self.labeled_view(self.top_view(0.35),"TOP"); r2=self.labeled_view(self.right_view(0.35),"RIGHT"); f2.move_to(ORIGIN); t2.next_to(f2,UP,buff=0.22); r2.next_to(f2,RIGHT,buff=0.28); g2=VGroup(f2,t2,r2).scale(0.82); l2=self.pill("THIRD-ANGLE · ISO A",20).next_to(g2,UP,buff=0.25); G2=VGroup(g2,l2).move_to(RIGHT*4+DOWN*0.5)
        self.play(FadeIn(G1),FadeIn(G2),Create(Line(UP*2.5,DOWN*3.2,color=LIGHT,stroke_width=2)),run_time=1); self.play(FadeIn(self.text("FIRST = OPPOSITE SIDE    |    THIRD = SAME SIDE",28,BOLD).to_edge(DOWN,buff=0.28)),run_time=0.7); self.wait(5); self.clear()

    def symbols(self):
        h=self.header(7,"PROJECTION SYMBOLS","Use the frustum-and-circle symbol to identify the method before reading the view layout."); self.add(h)
        s1=self.projection_symbol(False).scale(1.3); s2=self.projection_symbol(True).scale(1.3)
        c1=self.card("FIRST-ANGLE",["Circle on the left","Top below front"],5.1,2.0); c2=self.card("THIRD-ANGLE",["Circle on the right","Top above front"],5.1,2.0)
        G1=VGroup(s1,c1).arrange(DOWN,buff=0.4).move_to(LEFT*4+DOWN*0.35); G2=VGroup(s2,c2).arrange(DOWN,buff=0.4).move_to(RIGHT*4+DOWN*0.35)
        self.play(FadeIn(G1),FadeIn(G2),run_time=1); self.wait(4.2); self.clear()

    def colombia(self):
        h=self.header(8,"COLOMBIA — NORMATIVE CHECK","Correction: NTC 1777 is a technical standard; calling it 'legislation' is imprecise."); self.add(h)
        a=self.card("NTC 1777:2001",["Technical drawing — general principles of presentation.","Published as equivalent to ISO 128.","Recognizes BOTH first-angle and third-angle methods."],6.9,3.35)
        b=self.card("WHAT IT ACTUALLY SAYS",["First-angle = formerly method E.","Third-angle = formerly method A.","They are alternative orthographic methods of similar value."],6.9,3.35)
        VGroup(a,b).arrange(RIGHT,buff=0.42).move_to(DOWN*0.25); self.play(FadeIn(a),FadeIn(b),run_time=1); self.wait(3.8)
        foot=self.text("2026 check: ICONTEC catalog lists NTC 1915:1984 · Building drawing — Projection methods as VIGENTE.",21,BOLD,DARK); self.fit(foot,14.2,0.52); foot.to_edge(DOWN,buff=0.32); self.play(FadeIn(foot),run_time=0.7); self.wait(4); self.clear()

    def summary(self):
        h=self.header(9,"READ ANY ORTHOGRAPHIC DRAWING","1) identify FRONT, 2) find the projection symbol, 3) place the other views accordingly."); self.add(h)
        steps=[("1","FRONT"),("2","SYMBOL"),("3","FIRST / THIRD"),("4","TOP"),("5","SIDES"),("6","VERIFY")]
        cards=VGroup()
        for n,label in steps:
            b=RoundedRectangle(width=4.1,height=1.0,corner_radius=0.12,stroke_color=INK,stroke_width=1.6,fill_color=PAPER,fill_opacity=1)
            c=Circle(radius=0.26,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1); nt=self.text(n,18,BOLD).move_to(c); lab=self.text(label,20,BOLD).next_to(c,RIGHT,buff=0.2); VGroup(c,nt,lab).move_to(b); cards.add(VGroup(b,c,nt,lab))
        cards.arrange_in_grid(rows=2,cols=3,buff=(0.38,0.42)).move_to(DOWN*0.35); self.play(LaggedStart(*[FadeIn(x,shift=UP*0.08) for x in cards],lag_ratio=0.10),run_time=1.6); self.wait(3.5)
        self.play(FadeIn(self.pill("FIRST = OPPOSITE · THIRD = SAME SIDE",26).to_edge(DOWN,buff=0.30)),run_time=0.7); self.wait(4); self.clear()
        end=VGroup(self.text("SISTEMA DIÉDRICO",48,BOLD),self.text("3D object → 2D views → correct projection method",26,NORMAL,DARK),self.pill("READ THE SYMBOL BEFORE THE LAYOUT",22)).arrange(DOWN,buff=0.32)
        self.play(FadeIn(end,shift=UP*0.12),run_time=0.9); self.wait(3.5)


# Preview:
# manim -pql render_jobs/technical_drawing_diedric_iso_20260908/diedric_iso_ntc1777.py DihedralISOProjectionNTC1777 --disable_caching
# Final:
# manim -pqh render_jobs/technical_drawing_diedric_iso_20260908/diedric_iso_ntc1777.py DihedralISOProjectionNTC1777 --disable_caching
