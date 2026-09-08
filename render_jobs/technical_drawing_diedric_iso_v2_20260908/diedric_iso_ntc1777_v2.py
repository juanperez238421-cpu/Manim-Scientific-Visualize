#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior classroom animation: Sistema diedrico, ISO E vs ISO A, Colombia NTC context.

Design goals for V2:
- richer pseudo-3D technical figures;
- explicit projection rays and unfolding motion;
- larger, readable view drawings;
- step-by-step first-angle and third-angle placement;
- restrained engineering color coding;
- long pedagogical pauses;
- robust ManimCE 0.20.x Cairo rendering.
"""
from __future__ import annotations
import os
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

INK = "#121820"
DARK = "#2A3440"
MID = "#66727F"
LIGHT = "#D8DEE5"
PAPER = "#F7F9FB"
PLANE_BLUE = "#DDEAF5"
PLANE_TEAL = "#DFF1ED"
OBJ_FRONT = "#E9EEF3"
OBJ_SIDE = "#D6E0E8"
OBJ_TOP = "#F4F7F9"
ACCENT_BLUE = "#1F6F9F"
ACCENT_TEAL = "#16867A"
ACCENT_ORANGE = "#D9822B"
ACCENT_RED = "#B94A48"
ACCENT_GREEN = "#3C8C59"

RUN_FAST = 0.75
RUN = 1.10
RUN_SLOW = 1.60
PAUSE_SHORT = 1.1
PAUSE_READ = 2.4
PAUSE_EXPLAIN = 4.0
PAUSE_COMPARE = 5.0
PAUSE_LONG = 6.0

class SeniorTimedScene(Scene):
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

class DiedricISOProjectionV2Senior(SeniorTimedScene):
    def txt(self, s: str, size=30, weight=NORMAL, color=INK):
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.94)

    def fit(self, mob, max_w=14.7, max_h=7.6):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def clear_stage(self, run_time=0.65):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def header(self, n: int, title: str, subtitle: str):
        badge = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10, stroke_color=ACCENT_BLUE, stroke_width=2.3, fill_color=WHITE, fill_opacity=1)
        num = self.txt(f"{n:02d}", 22, BOLD, ACCENT_BLUE).move_to(badge)
        ttl = self.txt(title, 34, BOLD, INK)
        self.fit(ttl, 12.9, 0.58)
        row = VGroup(VGroup(badge, num), ttl).arrange(RIGHT, buff=0.22)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.44)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.txt(subtitle, 20, NORMAL, DARK)
        self.fit(sub, 14.35, 0.68)
        sub.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def pill(self, s: str, size=20, color=INK, fill=WHITE):
        t = self.txt(s, size, BOLD, color)
        b = RoundedRectangle(width=t.width + 0.52, height=t.height + 0.30, corner_radius=0.14, stroke_color=color, stroke_width=1.7, fill_color=fill, fill_opacity=1)
        t.move_to(b)
        return VGroup(b, t)

    def card(self, title: str, lines: list[str], width=5.7, height=3.2, accent=ACCENT_BLUE):
        title_m = self.txt(title, 27, BOLD, accent)
        body = VGroup(*[self.txt(line, 22, NORMAL, DARK) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        self.fit(content, width-0.60, height-0.50)
        box = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=accent, stroke_width=2.0, fill_color=PAPER, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.30)
        stripe = Line(box.get_corner(UL)+RIGHT*0.17+DOWN*0.20, box.get_corner(DL)+RIGHT*0.17+UP*0.20, color=accent, stroke_width=5)
        return VGroup(box, stripe, content)

    def number_step(self, n: int, text: str, width=4.0, color=ACCENT_BLUE):
        circle = Circle(radius=0.24, stroke_color=color, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        num = self.txt(str(n), 18, BOLD, color).move_to(circle)
        label = self.txt(text, 21, BOLD, INK)
        self.fit(label, width-0.7, 0.48)
        return VGroup(VGroup(circle, num), label).arrange(RIGHT, buff=0.18)

    def iso(self, x, y, z, s=0.72):
        return s * (x*RIGHT + y*(0.52*RIGHT + 0.33*UP) + z*UP)

    def box3d(self, x0, x1, y0, y1, z0, z1, s=0.72, edge=INK):
        p = lambda x, y, z: self.iso(x, y, z, s)
        front = Polygon(p(x0,y0,z0), p(x1,y0,z0), p(x1,y0,z1), p(x0,y0,z1), stroke_color=edge, stroke_width=2.3, fill_color=OBJ_FRONT, fill_opacity=1)
        side = Polygon(p(x1,y0,z0), p(x1,y1,z0), p(x1,y1,z1), p(x1,y0,z1), stroke_color=edge, stroke_width=2.3, fill_color=OBJ_SIDE, fill_opacity=1)
        top = Polygon(p(x0,y0,z1), p(x1,y0,z1), p(x1,y1,z1), p(x0,y1,z1), stroke_color=edge, stroke_width=2.3, fill_color=OBJ_TOP, fill_opacity=1)
        return VGroup(front, side, top)

    def stepped_object(self, s=0.72):
        boxes = [(0.0, 4.0, 0.0, 2.6, 0.0, 0.70), (2.05, 4.0, 0.0, 2.6, 0.70, 1.65), (2.95, 4.0, 0.0, 1.65, 1.65, 2.75), (0.55, 1.55, 0.35, 1.55, 0.70, 1.25)]
        g = VGroup(*[self.box3d(*b, s=s) for b in boxes])
        hole = Circle(radius=0.20*s, stroke_color=ACCENT_BLUE, stroke_width=2.0, fill_opacity=0)
        hole.move_to(self.iso(0.98, 0, 0.95, s))
        cross = VGroup(Line(hole.get_left(), hole.get_right(), color=ACCENT_BLUE, stroke_width=1.1), Line(hole.get_top(), hole.get_bottom(), color=ACCENT_BLUE, stroke_width=1.1))
        return VGroup(g, hole, cross)

    def front_view(self, scale=0.66, color=INK):
        pts = [LEFT*2.0+DOWN*1.20, RIGHT*2.0+DOWN*1.20, RIGHT*2.0+UP*1.75, RIGHT*1.00+UP*1.75, RIGHT*1.00+UP*0.60, RIGHT*0.05+UP*0.60, RIGHT*0.05+DOWN*0.42, LEFT*0.45+DOWN*0.42, LEFT*0.45+UP*0.02, LEFT*1.45+UP*0.02, LEFT*1.45+DOWN*0.42, LEFT*2.0+DOWN*0.42]
        outline = Polygon(*[p*scale for p in pts], stroke_color=color, stroke_width=3.0, fill_color=WHITE, fill_opacity=1)
        e1 = Line((RIGHT*0.05+DOWN*1.2)*scale,(RIGHT*0.05+DOWN*0.42)*scale,color=color,stroke_width=2)
        e2 = Line((RIGHT*1.0+DOWN*1.2)*scale,(RIGHT*1.0+UP*0.60)*scale,color=color,stroke_width=2)
        hole = Circle(radius=0.16*scale, stroke_color=ACCENT_BLUE, stroke_width=2).move_to((LEFT*0.95+DOWN*0.18)*scale)
        return VGroup(outline,e1,e2,hole)

    def top_view(self, scale=0.66, color=INK):
        r = Rectangle(width=4.0*scale, height=2.6*scale, stroke_color=color, stroke_width=3, fill_color=WHITE, fill_opacity=1)
        l1 = Line((RIGHT*0.05+DOWN*1.3)*scale,(RIGHT*0.05+UP*1.3)*scale,color=color,stroke_width=2)
        l2 = Line((RIGHT*1.0+DOWN*1.3)*scale,(RIGHT*1.0+UP*1.3)*scale,color=color,stroke_width=2)
        notch = Rectangle(width=1.0*scale,height=1.2*scale,stroke_color=color,stroke_width=2,fill_opacity=0)
        notch.move_to((LEFT*0.95+DOWN*0.25)*scale)
        return VGroup(r,l1,l2,notch)

    def side_view(self, scale=0.66, color=INK, mirror=False):
        pts=[LEFT*1.30+DOWN*1.20, RIGHT*1.30+DOWN*1.20, RIGHT*1.30+UP*1.75, LEFT*0.15+UP*1.75, LEFT*0.15+UP*0.62, LEFT*1.30+UP*0.62]
        if mirror:
            pts=[np.array([-p[0],p[1],0]) for p in pts]
        poly=Polygon(*[p*scale for p in pts],stroke_color=color,stroke_width=3,fill_color=WHITE,fill_opacity=1)
        e=Line((LEFT*0.15+DOWN*1.20)*scale,(LEFT*0.15+UP*0.62)*scale,color=color,stroke_width=2)
        if mirror:
            e=Line((RIGHT*0.15+DOWN*1.20)*scale,(RIGHT*0.15+UP*0.62)*scale,color=color,stroke_width=2)
        return VGroup(poly,e)

    def rear_view(self, scale=0.66):
        v=self.front_view(scale)
        v.flip(axis=UP)
        return v

    def bottom_view(self, scale=0.66):
        v=self.top_view(scale)
        v.flip(axis=RIGHT)
        return v

    def labeled_view(self, view, label, label_color=ACCENT_BLUE):
        lab=self.pill(label,17,label_color)
        lab.next_to(view,DOWN,buff=0.12)
        return VGroup(view,lab)

    def observer(self, label="OBSERVER", color=INK):
        eye = VGroup(Arc(radius=0.42,start_angle=0.08*PI,angle=0.84*PI,color=color,stroke_width=2.2), Arc(radius=0.42,start_angle=1.08*PI,angle=0.84*PI,color=color,stroke_width=2.2), Dot(radius=0.075,color=color))
        t=self.txt(label,17,BOLD,color).next_to(eye,DOWN,buff=0.08)
        return VGroup(eye,t)

    def projection_plane(self, vertical=True, width=1.0, height=4.4, fill=PLANE_BLUE, label="PROJECTION PLANE"):
        if vertical:
            poly=Polygon(LEFT*0.35+DOWN*2.0, RIGHT*0.35+DOWN*1.7, RIGHT*0.35+UP*2.0, LEFT*0.35+UP*1.7, stroke_color=ACCENT_BLUE,stroke_width=2.3,fill_color=fill,fill_opacity=0.80)
        else:
            poly=Polygon(LEFT*2.3+UP*0.25, RIGHT*1.9+UP*0.25, RIGHT*2.45+DOWN*0.60, LEFT*1.75+DOWN*0.60, stroke_color=ACCENT_TEAL,stroke_width=2.3,fill_color=fill,fill_opacity=0.80)
        lab=self.txt(label,16,BOLD,ACCENT_BLUE if vertical else ACCENT_TEAL)
        lab.rotate(PI/2 if vertical else 0).move_to(poly)
        return VGroup(poly,lab)

    def ray_bundle(self, starts, targets, color=ACCENT_ORANGE):
        return VGroup(*[DashedLine(a,b,dash_length=0.10,stroke_width=2.0,color=color) for a,b in zip(starts,targets)])

    def view_frame(self, label, view, width=3.7, height=3.0, accent=ACCENT_BLUE):
        box=RoundedRectangle(width=width,height=height,corner_radius=0.13,stroke_color=accent,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
        lab=self.pill(label,17,accent).next_to(box,UP,buff=-0.18)
        view.move_to(box).shift(DOWN*0.05)
        self.fit(view,width-0.50,height-0.60)
        return VGroup(box,view,lab)

    def projection_symbol(self, third=True):
        fr=Polygon(LEFT*1.10+DOWN*0.58, LEFT*1.10+UP*0.58, RIGHT*0.78+UP*0.36, RIGHT*0.78+DOWN*0.36, stroke_color=INK,stroke_width=2.8,fill_color=WHITE,fill_opacity=1)
        axis=DashedLine(LEFT*1.30,RIGHT*1.12,dash_length=0.10,color=MID,stroke_width=1.3)
        c=Circle(radius=0.57,stroke_color=INK,stroke_width=2.8,fill_color=WHITE,fill_opacity=1)
        cv=Line(c.get_top(),c.get_bottom(),color=MID,stroke_width=1.1)
        ch=Line(c.get_left(),c.get_right(),color=MID,stroke_width=1.1)
        cg=VGroup(c,cv,ch)
        cg.next_to(fr, RIGHT if third else LEFT, buff=0.48)
        return VGroup(fr,axis,cg)

    def construct(self):
        self.opening(); self.from_3d_to_2d(); self.dihedral_apparatus(); self.six_views_walkaround(); self.first_angle_story(); self.third_angle_story(); self.direct_comparison(); self.symbols_scene(); self.colombia_scene(); self.reading_method(); self.challenge_scene(); self.closing()

    def opening(self):
        obj=self.stepped_object(0.60).move_to(LEFT*3.9+DOWN*0.45)
        front=self.view_frame("FRONT",self.front_view(0.42),3.2,2.5,ACCENT_BLUE).move_to(RIGHT*3.85+UP*1.60)
        top=self.view_frame("TOP",self.top_view(0.42),3.2,2.5,ACCENT_TEAL).move_to(RIGHT*3.85+DOWN*1.35)
        arrow1=Arrow(obj.get_right(),front.get_left(),buff=0.18,color=ACCENT_ORANGE,stroke_width=3)
        arrow2=Arrow(obj.get_right(),top.get_left(),buff=0.18,color=ACCENT_ORANGE,stroke_width=3)
        title=VGroup(self.txt("DIBUJO TÉCNICO Y CAD",23,BOLD,DARK), self.txt("SISTEMA DIÉDRICO",58,BOLD,INK), self.txt("ISO E · FIRST-ANGLE   vs   ISO A · THIRD-ANGLE",28,BOLD,ACCENT_BLUE), self.txt("How a 3D part becomes an unambiguous 2D technical drawing",23,NORMAL,DARK)).arrange(DOWN,buff=0.20,aligned_edge=LEFT).move_to(UP*0.25)
        title.to_edge(UP,buff=0.60)
        self.play(FadeIn(title[0]),Write(title[1]),run_time=RUN_SLOW)
        self.play(FadeIn(title[2]),FadeIn(title[3]),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(DrawBorderThenFill(obj),run_time=RUN_SLOW)
        self.play(GrowArrow(arrow1),GrowArrow(arrow2),run_time=RUN)
        self.play(FadeIn(front,shift=LEFT*0.15),FadeIn(top,shift=LEFT*0.15),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def from_3d_to_2d(self):
        h=self.header(1,"FROM 3D OBJECT TO 2D VIEWS","Orthographic projection removes perspective: every view records shape and size from one exact direction.")
        self.add(h)
        obj=self.stepped_object(0.78).move_to(LEFT*3.9+DOWN*0.60)
        self.play(DrawBorderThenFill(obj),run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        dirs=VGroup(self.pill("LOOK FROM FRONT",19,ACCENT_BLUE).move_to(LEFT*0.3+UP*1.75), self.pill("LOOK FROM TOP",19,ACCENT_TEAL).move_to(LEFT*0.3+DOWN*0.15), self.pill("LOOK FROM RIGHT",19,ACCENT_ORANGE).move_to(LEFT*0.3+DOWN*2.05))
        arrows=VGroup(Arrow(dirs[0].get_left(),obj.get_right(),buff=0.25,color=ACCENT_BLUE,stroke_width=3), Arrow(dirs[1].get_left(),obj.get_right()+UP*0.85,buff=0.25,color=ACCENT_TEAL,stroke_width=3), Arrow(dirs[2].get_left(),obj.get_right()+DOWN*0.55,buff=0.25,color=ACCENT_ORANGE,stroke_width=3))
        self.play(LaggedStart(*[FadeIn(x) for x in dirs],lag_ratio=0.18),run_time=RUN_SLOW)
        self.play(LaggedStart(*[GrowArrow(x) for x in arrows],lag_ratio=0.20),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        views=VGroup(self.view_frame("FRONT",self.front_view(0.45),3.35,2.20,ACCENT_BLUE), self.view_frame("TOP",self.top_view(0.45),3.35,2.20,ACCENT_TEAL), self.view_frame("RIGHT",self.side_view(0.45),3.35,2.20,ACCENT_ORANGE)).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.45).shift(DOWN*0.35)
        for v in views:
            self.play(FadeIn(v,shift=RIGHT*0.18),run_time=RUN)
            self.wait(PAUSE_SHORT)
        takeaway=self.pill("NO PERSPECTIVE · ONE DIRECTION PER VIEW",20,ACCENT_GREEN).to_edge(DOWN,buff=0.24)
        self.play(FadeIn(takeaway),run_time=RUN_FAST)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def dihedral_apparatus(self):
        h=self.header(2,"THE DIHEDRAL APPARATUS","Two perpendicular reference planes capture front and top information, then unfold into the sheet.")
        self.add(h)
        pv=Polygon(LEFT*2.85+DOWN*1.45, LEFT*0.45+DOWN*0.75, LEFT*0.45+UP*2.50, LEFT*2.85+UP*1.80, stroke_color=ACCENT_BLUE,stroke_width=2.5,fill_color=PLANE_BLUE,fill_opacity=0.65)
        ph=Polygon(LEFT*2.85+DOWN*1.45, RIGHT*2.20+DOWN*1.45, RIGHT*3.15+DOWN*2.65, LEFT*1.95+DOWN*2.65, stroke_color=ACCENT_TEAL,stroke_width=2.5,fill_color=PLANE_TEAL,fill_opacity=0.65)
        lt=Line(LEFT*2.85+DOWN*1.45,RIGHT*2.20+DOWN*1.45,color=INK,stroke_width=4)
        lt_lab=self.pill("GROUND LINE / LT",17,INK).next_to(lt,DOWN,buff=0.14)
        pv_lab=self.pill("PV → FRONT",18,ACCENT_BLUE).move_to(LEFT*2.0+UP*1.55)
        ph_lab=self.pill("PH → TOP",18,ACCENT_TEAL).move_to(LEFT*0.15+DOWN*2.30)
        obj=self.stepped_object(0.52).move_to(LEFT*0.90+DOWN*0.70)
        self.play(FadeIn(pv),FadeIn(ph),Create(lt),run_time=RUN_SLOW)
        self.play(FadeIn(pv_lab),FadeIn(ph_lab),FadeIn(lt_lab),run_time=RUN)
        self.play(DrawBorderThenFill(obj),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        starts=[obj.get_corner(UL),obj.get_corner(UR),obj.get_corner(DL),obj.get_corner(DR)]
        targets_pv=[LEFT*1.72+UP*1.35,LEFT*0.85+UP*1.10,LEFT*1.72+DOWN*0.60,LEFT*0.85+DOWN*0.30]
        rays_pv=self.ray_bundle(starts,targets_pv,ACCENT_ORANGE)
        self.play(LaggedStart(*[Create(r) for r in rays_pv],lag_ratio=0.12),run_time=RUN_SLOW)
        front_trace=self.front_view(0.28,ACCENT_BLUE).move_to(LEFT*1.27+UP*0.30)
        self.play(Create(front_trace),run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        targets_ph=[LEFT*1.15+DOWN*1.75,RIGHT*0.35+DOWN*1.75,LEFT*1.15+DOWN*2.22,RIGHT*0.35+DOWN*2.22]
        rays_ph=self.ray_bundle(starts,targets_ph,ACCENT_ORANGE)
        self.play(LaggedStart(*[Create(r) for r in rays_ph],lag_ratio=0.12),run_time=RUN_SLOW)
        top_trace=self.top_view(0.25,ACCENT_TEAL).move_to(LEFT*0.40+DOWN*2.02)
        self.play(Create(top_trace),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        flat=RoundedRectangle(width=6.0,height=5.8,corner_radius=0.10,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1).to_edge(RIGHT,buff=0.55).shift(DOWN*0.30)
        flat_lab=self.pill("UNFOLDED DRAWING SHEET",18,INK).next_to(flat,UP,buff=-0.18)
        f2=self.labeled_view(self.front_view(0.43),"FRONT",ACCENT_BLUE).move_to(flat.get_center()+UP*0.75)
        t2=self.labeled_view(self.top_view(0.43),"TOP",ACCENT_TEAL).move_to(flat.get_center()+DOWN*1.55)
        self.play(FadeOut(rays_pv),FadeOut(rays_ph),run_time=RUN_FAST)
        self.play(FadeIn(flat),FadeIn(flat_lab),run_time=RUN)
        self.play(TransformFromCopy(front_trace,f2),TransformFromCopy(top_trace,t2),run_time=RUN_SLOW)
        note=self.card("THIS IS THE CORE IDEA",["Project onto reference planes.","Unfold the planes.","Read the resulting 2D views."],4.8,2.55,ACCENT_GREEN).move_to(RIGHT*3.8+UP*2.15)
        self.play(FadeIn(note),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def six_views_walkaround(self):
        h=self.header(3,"WALK AROUND THE PART: SIX PRINCIPAL VIEWS","The observer changes direction; the object does not. Each direction produces one orthographic view.")
        self.add(h)
        obj=self.stepped_object(0.62).move_to(DOWN*0.55)
        halo=Circle(radius=2.75,stroke_color=LIGHT,stroke_width=2.0).move_to(obj)
        self.play(FadeIn(halo),DrawBorderThenFill(obj),run_time=RUN_SLOW)
        positions=[("FRONT",LEFT*5.1+DOWN*0.55,ACCENT_BLUE,self.front_view(0.30)), ("RIGHT",RIGHT*4.9+DOWN*0.55,ACCENT_ORANGE,self.side_view(0.30)), ("TOP",UP*2.35,ACCENT_TEAL,self.top_view(0.30)), ("LEFT",LEFT*4.0+UP*2.05,ACCENT_GREEN,self.side_view(0.30,mirror=True)), ("REAR",RIGHT*4.0+UP*2.05,ACCENT_RED,self.rear_view(0.30)), ("BOTTOM",DOWN*3.15,MID,self.bottom_view(0.30))]
        for name,pos,col,view in positions:
            observer=self.observer(name,col).scale(0.72).move_to(pos)
            arrow=Arrow(observer.get_center(),obj.get_center(),buff=0.55,color=col,stroke_width=2.7,max_tip_length_to_length_ratio=0.10)
            tile=self.view_frame(name,view,2.3,1.55,col).move_to(pos).scale(0.88)
            self.play(FadeIn(observer),GrowArrow(arrow),run_time=RUN)
            self.wait(PAUSE_SHORT)
            self.play(ReplacementTransform(observer,tile),FadeOut(arrow),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        center_note=self.pill("SAME SIX DIRECTIONS IN BOTH SYSTEMS",21,ACCENT_GREEN).move_to(obj.get_center()+DOWN*2.15)
        self.play(FadeIn(center_note),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def first_angle_story(self):
        h=self.header(4,"FIRST-ANGLE PROJECTION · ISO E","Observer → object → projection plane. The object lies between the observer and the plane.")
        self.add(h)
        obs=self.observer("OBSERVER",ACCENT_BLUE).move_to(LEFT*5.5+DOWN*0.70)
        obj=self.stepped_object(0.52).move_to(LEFT*1.75+DOWN*0.70)
        plane=self.projection_plane(True,fill=PLANE_BLUE,label="PLANE").move_to(RIGHT*1.15+DOWN*0.55)
        order=self.number_step(1,"Observer sees the object first",4.6,ACCENT_BLUE).move_to(RIGHT*4.9+UP*1.55)
        order2=self.number_step(2,"Rays continue to the plane",4.6,ACCENT_ORANGE).next_to(order,DOWN,buff=0.28).align_to(order,LEFT)
        order3=self.number_step(3,"Unfold: views land opposite",4.6,ACCENT_GREEN).next_to(order2,DOWN,buff=0.28).align_to(order,LEFT)
        self.play(FadeIn(obs),DrawBorderThenFill(obj),FadeIn(plane),run_time=RUN_SLOW)
        a1=Arrow(obs.get_right(),obj.get_left(),buff=0.15,color=ACCENT_BLUE,stroke_width=3)
        a2=Arrow(obj.get_right(),plane.get_left(),buff=0.15,color=ACCENT_ORANGE,stroke_width=3)
        self.play(GrowArrow(a1),run_time=RUN)
        self.play(FadeIn(order),run_time=RUN_FAST)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(a2),run_time=RUN)
        self.play(FadeIn(order2),run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)
        starts=[obj.get_corner(UL),obj.get_corner(UR),obj.get_corner(DL),obj.get_corner(DR)]
        targets=[plane[0].get_center()+UP*1.25,plane[0].get_center()+UP*0.55,plane[0].get_center()+DOWN*0.70,plane[0].get_center()+DOWN*1.35]
        rays=self.ray_bundle(starts,targets,ACCENT_ORANGE)
        self.play(LaggedStart(*[Create(r) for r in rays],lag_ratio=0.12),run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(order3),run_time=RUN_FAST)
        self.wait(PAUSE_READ)
        self.play(*[FadeOut(x) for x in [obs,obj,plane,a1,a2,rays]],run_time=RUN)
        front=self.view_frame("FRONT",self.front_view(0.56),4.2,3.10,ACCENT_BLUE).move_to(ORIGIN+UP*0.15)
        top=self.view_frame("TOP",self.top_view(0.52),4.2,2.45,ACCENT_TEAL).next_to(front,DOWN,buff=0.28)
        rightv=self.view_frame("RIGHT VIEW",self.side_view(0.52),3.2,3.10,ACCENT_ORANGE).next_to(front,LEFT,buff=0.35)
        leftv=self.view_frame("LEFT VIEW",self.side_view(0.52,mirror=True),3.2,3.10,ACCENT_GREEN).next_to(front,RIGHT,buff=0.35)
        VGroup(front,top,rightv,leftv).scale(0.92).shift(DOWN*0.22)
        self.play(FadeIn(front),run_time=RUN)
        self.wait(PAUSE_READ)
        top_seed=self.view_frame("TOP",self.top_view(0.42),3.2,2.0,ACCENT_TEAL).move_to(front.get_center()+UP*2.35)
        self.play(FadeIn(top_seed),run_time=RUN)
        self.play(top_seed.animate.move_to(top.get_center()).scale(1.08),run_time=RUN_SLOW)
        self.play(FadeOut(top_seed),FadeIn(top),run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)
        rv_seed=self.view_frame("RIGHT VIEW",self.side_view(0.42),2.6,2.4,ACCENT_ORANGE).move_to(front.get_center()+RIGHT*2.9)
        self.play(FadeIn(rv_seed),run_time=RUN)
        self.play(rv_seed.animate.move_to(rightv.get_center()).scale(1.08),run_time=RUN_SLOW)
        self.play(FadeOut(rv_seed),FadeIn(rightv),run_time=RUN_FAST)
        self.play(FadeIn(leftv),run_time=RUN)
        key=self.pill("FIRST-ANGLE = VIEWS MOVE TO THE OPPOSITE SIDE",20,ACCENT_GREEN).to_edge(DOWN,buff=0.20)
        self.play(FadeIn(key),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def third_angle_story(self):
        h=self.header(5,"THIRD-ANGLE PROJECTION · ISO A","Observer → projection plane → object. The plane lies between the observer and the object.")
        self.add(h)
        obs=self.observer("OBSERVER",ACCENT_BLUE).move_to(LEFT*5.5+DOWN*0.70)
        plane=self.projection_plane(True,fill=PLANE_BLUE,label="PLANE").move_to(LEFT*1.9+DOWN*0.55)
        obj=self.stepped_object(0.52).move_to(RIGHT*1.1+DOWN*0.70)
        order=self.number_step(1,"Observer meets the plane first",4.7,ACCENT_BLUE).move_to(RIGHT*4.9+UP*1.55)
        order2=self.number_step(2,"Rays continue to the object",4.7,ACCENT_ORANGE).next_to(order,DOWN,buff=0.28).align_to(order,LEFT)
        order3=self.number_step(3,"Unfold: views stay same side",4.7,ACCENT_GREEN).next_to(order2,DOWN,buff=0.28).align_to(order,LEFT)
        self.play(FadeIn(obs),FadeIn(plane),DrawBorderThenFill(obj),run_time=RUN_SLOW)
        a1=Arrow(obs.get_right(),plane.get_left(),buff=0.15,color=ACCENT_BLUE,stroke_width=3)
        a2=Arrow(plane.get_right(),obj.get_left(),buff=0.15,color=ACCENT_ORANGE,stroke_width=3)
        self.play(GrowArrow(a1),FadeIn(order),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(a2),FadeIn(order2),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        starts=[obs.get_right()+UP*0.25,obs.get_right()+UP*0.05,obs.get_right()+DOWN*0.15,obs.get_right()+DOWN*0.35]
        targets=[plane[0].get_center()+UP*1.25,plane[0].get_center()+UP*0.55,plane[0].get_center()+DOWN*0.65,plane[0].get_center()+DOWN*1.35]
        rays=self.ray_bundle(starts,targets,ACCENT_ORANGE)
        self.play(LaggedStart(*[Create(r) for r in rays],lag_ratio=0.12),run_time=RUN_SLOW)
        self.play(FadeIn(order3),run_time=RUN_FAST)
        self.wait(PAUSE_READ)
        self.play(*[FadeOut(x) for x in [obs,obj,plane,a1,a2,rays]],run_time=RUN)
        front=self.view_frame("FRONT",self.front_view(0.56),4.2,3.10,ACCENT_BLUE).move_to(ORIGIN+DOWN*0.05)
        top=self.view_frame("TOP",self.top_view(0.52),4.2,2.45,ACCENT_TEAL).next_to(front,UP,buff=0.28)
        rightv=self.view_frame("RIGHT VIEW",self.side_view(0.52),3.2,3.10,ACCENT_ORANGE).next_to(front,RIGHT,buff=0.35)
        leftv=self.view_frame("LEFT VIEW",self.side_view(0.52,mirror=True),3.2,3.10,ACCENT_GREEN).next_to(front,LEFT,buff=0.35)
        VGroup(front,top,rightv,leftv).scale(0.90).shift(DOWN*0.25)
        self.play(FadeIn(front),run_time=RUN)
        self.wait(PAUSE_READ)
        top_seed=self.view_frame("TOP",self.top_view(0.42),3.2,2.0,ACCENT_TEAL).move_to(front.get_center()+DOWN*2.35)
        self.play(FadeIn(top_seed),run_time=RUN)
        self.play(top_seed.animate.move_to(top.get_center()).scale(1.08),run_time=RUN_SLOW)
        self.play(FadeOut(top_seed),FadeIn(top),run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)
        rv_seed=self.view_frame("RIGHT VIEW",self.side_view(0.42),2.6,2.4,ACCENT_ORANGE).move_to(front.get_center()+LEFT*2.9)
        self.play(FadeIn(rv_seed),run_time=RUN)
        self.play(rv_seed.animate.move_to(rightv.get_center()).scale(1.08),run_time=RUN_SLOW)
        self.play(FadeOut(rv_seed),FadeIn(rightv),FadeIn(leftv),run_time=RUN)
        key=self.pill("THIRD-ANGLE = VIEWS STAY ON THE SAME SIDE",20,ACCENT_GREEN).to_edge(DOWN,buff=0.20)
        self.play(FadeIn(key),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def direct_comparison(self):
        h=self.header(6,"SAME PART · SAME VIEWS · DIFFERENT PLACEMENT","Anchor the FRONT view. Watch where TOP and RIGHT move in each system.")
        self.add(h)
        divider=Line(UP*2.45,DOWN*3.55,color=LIGHT,stroke_width=2).move_to(ORIGIN)
        self.add(divider)
        left_title=self.pill("FIRST-ANGLE · ISO E",21,ACCENT_BLUE).move_to(LEFT*4.0+UP*2.10)
        right_title=self.pill("THIRD-ANGLE · ISO A",21,ACCENT_TEAL).move_to(RIGHT*4.0+UP*2.10)
        self.play(FadeIn(left_title),FadeIn(right_title),run_time=RUN)
        lf=self.labeled_view(self.front_view(0.42),"FRONT",ACCENT_BLUE).move_to(LEFT*4.0+DOWN*0.10)
        rf=self.labeled_view(self.front_view(0.42),"FRONT",ACCENT_BLUE).move_to(RIGHT*4.0+DOWN*0.10)
        lt=self.labeled_view(self.top_view(0.37),"TOP",ACCENT_TEAL).move_to(LEFT*4.0+UP*1.05)
        rt=self.labeled_view(self.top_view(0.37),"TOP",ACCENT_TEAL).move_to(RIGHT*4.0+DOWN*2.05)
        lr=self.labeled_view(self.side_view(0.37),"RIGHT",ACCENT_ORANGE).move_to(LEFT*2.2+DOWN*0.10)
        rr=self.labeled_view(self.side_view(0.37),"RIGHT",ACCENT_ORANGE).move_to(RIGHT*2.2+DOWN*0.10)
        self.play(FadeIn(lf),FadeIn(rf),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(lt),FadeIn(rt),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(lr),FadeIn(rr),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        v1=Arrow(lf.get_top(),lt.get_bottom(),buff=0.15,color=ACCENT_TEAL,stroke_width=3)
        v2=Arrow(rf.get_bottom(),rt.get_top(),buff=0.15,color=ACCENT_TEAL,stroke_width=3)
        h1=Arrow(lf.get_right(),lr.get_left(),buff=0.15,color=ACCENT_ORANGE,stroke_width=3)
        h2=Arrow(rf.get_left(),rr.get_right(),buff=0.15,color=ACCENT_ORANGE,stroke_width=3)
        self.play(GrowArrow(v1),GrowArrow(v2),GrowArrow(h1),GrowArrow(h2),run_time=RUN_SLOW)
        bottom=VGroup(self.pill("FIRST: TOP BELOW · RIGHT VIEW LEFT",19,ACCENT_BLUE), self.pill("THIRD: TOP ABOVE · RIGHT VIEW RIGHT",19,ACCENT_TEAL)).arrange(RIGHT,buff=0.45).to_edge(DOWN,buff=0.18)
        self.play(FadeIn(bottom),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def symbols_scene(self):
        h=self.header(7,"READ THE PROJECTION SYMBOL BEFORE THE LAYOUT","The standardized frustum-and-circle symbol tells you which projection method the drawing uses.")
        self.add(h)
        first=self.projection_symbol(False).scale(1.20).move_to(LEFT*3.8+DOWN*0.15)
        third=self.projection_symbol(True).scale(1.20).move_to(RIGHT*3.8+DOWN*0.15)
        first_lab=VGroup(self.pill("FIRST-ANGLE",20,ACCENT_BLUE),self.txt("circle on the LEFT",22,BOLD,ACCENT_BLUE)).arrange(DOWN,buff=0.18).next_to(first,UP,buff=0.45)
        third_lab=VGroup(self.pill("THIRD-ANGLE",20,ACCENT_TEAL),self.txt("circle on the RIGHT",22,BOLD,ACCENT_TEAL)).arrange(DOWN,buff=0.18).next_to(third,UP,buff=0.45)
        self.play(FadeIn(first_lab[0]),FadeIn(third_lab[0]),run_time=RUN)
        self.play(DrawBorderThenFill(first),DrawBorderThenFill(third),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(first_lab[1]),FadeIn(third_lab[1]),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(Circumscribe(first,color=ACCENT_BLUE,buff=0.22),Circumscribe(third,color=ACCENT_TEAL,buff=0.22),run_time=RUN_SLOW)
        note=self.card("PRACTICAL RULE",["Do not guess from geography.","Do not guess from memory.","Read the symbol, then place the views."],5.9,2.55,ACCENT_GREEN).to_edge(DOWN,buff=0.28)
        self.play(FadeIn(note),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def colombia_scene(self):
        h=self.header(8,"COLOMBIA · NORMATIVE CONTEXT","Use precise language: NTC standards are technical standards; calling them legislation is not precise by itself.")
        self.add(h)
        doc1=self.card("NTC 1777:2001",["Technical drawing — general principles of presentation.","Equivalent to ISO 128 at publication.","Recognizes first-angle and third-angle methods."],6.6,3.25,ACCENT_BLUE).move_to(LEFT*3.65+DOWN*0.15)
        doc2=self.card("NTC 1915:1984",["Building drawing — Projection methods.","ICONTEC catalog cross-check used for this lesson:","listed as VIGENTE in 2026."],6.6,3.25,ACCENT_TEAL).move_to(RIGHT*3.65+DOWN*0.15)
        self.play(FadeIn(doc1,shift=UP*0.15),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(doc2,shift=UP*0.15),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        correction=self.pill("CORRECT CLASSROOM WORDING: COLOMBIAN TECHNICAL STANDARD",20,ACCENT_GREEN).to_edge(DOWN,buff=0.32)
        self.play(FadeIn(correction),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def reading_method(self):
        h=self.header(9,"A RELIABLE METHOD FOR ANY ORTHOGRAPHIC DRAWING","Use the same sequence every time; do not start by memorizing where every view goes.")
        self.add(h)
        steps=["Identify FRONT","Find projection symbol","Decide FIRST or THIRD","Place TOP from FRONT","Place side views","Verify corresponding edges"]
        cards=VGroup()
        for i,s in enumerate(steps,1):
            c=RoundedRectangle(width=4.3,height=1.35,corner_radius=0.14,stroke_color=ACCENT_BLUE if i<4 else ACCENT_TEAL,stroke_width=2,fill_color=PAPER,fill_opacity=1)
            n=Circle(radius=0.27,stroke_color=ACCENT_BLUE,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(c.get_left()+RIGHT*0.55)
            nt=self.txt(str(i),18,BOLD,ACCENT_BLUE).move_to(n)
            tx=self.txt(s,22,BOLD,INK).move_to(c).shift(RIGHT*0.32)
            self.fit(tx,3.3,0.55)
            cards.add(VGroup(c,n,nt,tx))
        cards.arrange_in_grid(rows=2,cols=3,buff=(0.38,0.48)).move_to(DOWN*0.35)
        for c in cards:
            self.play(FadeIn(c,shift=UP*0.10),run_time=RUN_FAST)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_EXPLAIN)
        rule=self.pill("SYMBOL FIRST → LAYOUT SECOND",22,ACCENT_GREEN).to_edge(DOWN,buff=0.24)
        self.play(FadeIn(rule),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def challenge_scene(self):
        h=self.header(10,"QUICK CHECK: CAN YOU PREDICT THE LAYOUT?","A third-angle symbol is shown. Predict where TOP and RIGHT must go before the answer appears.")
        self.add(h)
        obj=self.stepped_object(0.62).move_to(LEFT*4.6+DOWN*0.65)
        symbol=self.projection_symbol(True).scale(0.62).move_to(LEFT*4.6+UP*1.85)
        front=self.view_frame("FRONT",self.front_view(0.52),4.2,3.0,ACCENT_BLUE).move_to(RIGHT*1.15+DOWN*0.35)
        blank_top=RoundedRectangle(width=4.2,height=2.15,corner_radius=0.13,stroke_color=LIGHT,stroke_width=2,fill_color=WHITE,fill_opacity=1).next_to(front,UP,buff=0.28)
        blank_right=RoundedRectangle(width=3.1,height=3.0,corner_radius=0.13,stroke_color=LIGHT,stroke_width=2,fill_color=WHITE,fill_opacity=1).next_to(front,RIGHT,buff=0.30)
        q1=self.txt("TOP ?",22,BOLD,MID).move_to(blank_top)
        q2=self.txt("RIGHT ?",22,BOLD,MID).move_to(blank_right)
        self.play(DrawBorderThenFill(obj),FadeIn(symbol),run_time=RUN_SLOW)
        self.play(FadeIn(front),Create(blank_top),Create(blank_right),FadeIn(q1),FadeIn(q2),run_time=RUN_SLOW)
        prompt=self.pill("THINK BEFORE REVEAL",20,ACCENT_ORANGE).to_edge(DOWN,buff=0.25)
        self.play(FadeIn(prompt),run_time=RUN)
        self.wait(8.0)
        top=self.top_view(0.50).move_to(blank_top)
        rightv=self.side_view(0.50).move_to(blank_right)
        self.play(FadeOut(q1),FadeOut(q2),Create(top),Create(rightv),run_time=RUN_SLOW)
        answer=self.pill("THIRD-ANGLE → TOP ABOVE · RIGHT VIEW RIGHT",20,ACCENT_GREEN).to_edge(DOWN,buff=0.25)
        self.play(ReplacementTransform(prompt,answer),run_time=RUN)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def closing(self):
        title=self.txt("SISTEMA DIÉDRICO",54,BOLD,INK)
        line1=self.txt("3D object → orthographic views → projection method → correct layout",25,BOLD,DARK)
        first=self.pill("FIRST-ANGLE: OPPOSITE SIDE",21,ACCENT_BLUE)
        third=self.pill("THIRD-ANGLE: SAME SIDE",21,ACCENT_TEAL)
        rules=VGroup(first,third).arrange(RIGHT,buff=0.45)
        final=self.pill("READ THE SYMBOL BEFORE YOU READ THE SHEET",22,ACCENT_GREEN)
        g=VGroup(title,line1,rules,final).arrange(DOWN,buff=0.35)
        self.play(Write(title),run_time=RUN_SLOW)
        self.play(FadeIn(line1),run_time=RUN)
        self.play(FadeIn(rules),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(final),run_time=RUN)
        self.wait(PAUSE_LONG)

# QA preview:
# manim -pql diedric_iso_ntc1777_v2.py DiedricISOProjectionV2Senior --disable_caching
# Final:
# manim -pqh diedric_iso_ntc1777_v2.py DiedricISOProjectionV2Senior --disable_caching
