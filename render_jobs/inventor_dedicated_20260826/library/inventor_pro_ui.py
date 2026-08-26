from __future__ import annotations

import math
import os
from typing import Sequence
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"
WHITE_FILL = WHITE
TITLE = 50
H1 = 33
BODY = 23
SMALL = 19
RUN = 0.95
RUN_SLOW = 1.35
PAUSE = 1.15
READ = 1.90
EXPLAIN = 2.75


def cuboid(width: float, depth: float, height: float, opacity: float = 0.58, color=GRAY_C) -> Cube:
    c = Cube(side_length=1.0, fill_color=color, fill_opacity=opacity, stroke_color=GRAY_B, stroke_width=0.8)
    c.stretch_to_fit_width(width); c.stretch_to_fit_height(depth); c.stretch_to_fit_depth(height)
    return c


def cylinder(radius: float, height: float, opacity: float = 0.58, color=GRAY_C, direction=OUT) -> Cylinder:
    return Cylinder(radius=radius, height=height, direction=direction, resolution=(30, 8),
                    fill_color=color, fill_opacity=opacity, stroke_color=GRAY_B, stroke_width=0.75)


def extruded_polygon(points: Sequence[Sequence[float]], depth: float, opacity: float = 0.58, color=GRAY_C) -> VGroup:
    pts = [np.array(p, dtype=float) for p in points]
    back = [p + OUT * depth for p in pts]
    front_face = Polygon(*pts, fill_color=color, fill_opacity=opacity, stroke_color=GRAY_B, stroke_width=0.8)
    back_face = Polygon(*back, fill_color=color, fill_opacity=opacity, stroke_color=GRAY_B, stroke_width=0.8)
    sides = VGroup(*[Polygon(pts[i], pts[(i+1)%len(pts)], back[(i+1)%len(pts)], back[i],
                             fill_color=color, fill_opacity=opacity, stroke_color=GRAY_B, stroke_width=0.8)
                     for i in range(len(pts))])
    return VGroup(front_face, back_face, sides)


def rounded_rect_points(width: float, depth: float, radius: float, samples: int = 8, z: float = 0.0):
    w, d = width/2, depth/2
    r = min(radius, w*0.48, d*0.48)
    centers = [(w-r,d-r),(-w+r,d-r),(-w+r,-d+r),(w-r,-d+r)]
    arcs = [(0,PI/2),(PI/2,PI),(PI,3*PI/2),(3*PI/2,TAU)]
    pts=[]
    for (cx,cy),(a0,a1) in zip(centers,arcs):
        for a in np.linspace(a0,a1,samples,endpoint=False):
            pts.append([cx+r*math.cos(a),cy+r*math.sin(a),z])
    return pts


def rounded_plate(width: float, depth: float, height: float, radius: float, opacity=0.58, color=GRAY_C) -> VGroup:
    return extruded_polygon(rounded_rect_points(width,depth,radius,10,-height/2), height, opacity, color)


def chamfered_plate(width: float, depth: float, height: float, chamfer: float, opacity=0.58, color=GRAY_C) -> VGroup:
    w,d=width/2,depth/2; c=min(chamfer,w*0.45,d*0.45)
    pts=[[-w+c,-d,-height/2],[w-c,-d,-height/2],[w,-d+c,-height/2],[w,d-c,-height/2],
         [w-c,d,-height/2],[-w+c,d,-height/2],[-w,d-c,-height/2],[-w,-d+c,-height/2]]
    return extruded_polygon(pts,height,opacity,color)


class JPMiscCADScene(ThreeDScene):
    OPERATION = "CAD feature"

    def setup(self):
        super().setup(); self.camera.background_color = WHITE

    def play(self,*animations,**kwargs):
        if kwargs.get("run_time") is not None: kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations,**kwargs)

    def wait(self,duration=DEFAULT_WAIT_TIME,*args,**kwargs):
        return super().wait(duration*TIME_SCALE,*args,**kwargs)

    def text(self,content,size=BODY,weight=NORMAL,color=BLACK_TEXT,**kwargs):
        return Text(content,font_size=size,color=color,weight=weight,**kwargs)

    def fit(self,mob,max_w=14.4,max_h=7.5):
        if mob.width>max_w: mob.scale_to_fit_width(max_w)
        if mob.height>max_h: mob.scale_to_fit_height(max_h)
        return mob

    def fixed(self,*mobs): self.add_fixed_in_frame_mobjects(*mobs)

    def section_header(self,n,title,subtitle):
        badge=RoundedRectangle(width=0.72,height=0.52,corner_radius=0.09,stroke_color=BLACK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
        num=self.text(f"{n:02d}",22,BOLD).move_to(badge)
        head=self.text(title,H1,BOLD); self.fit(head,13.0,0.62)
        row=VGroup(VGroup(badge,num),head).arrange(RIGHT,buff=0.22).to_edge(UP,buff=0.16).to_edge(LEFT,buff=0.48)
        rule=Line(LEFT*7.45,RIGHT*7.45,color=LIGHT_GRAY,stroke_width=1.8).next_to(row,DOWN,buff=0.06)
        sub=self.text(subtitle,SMALL); self.fit(sub,14.1,0.58); sub.next_to(rule,DOWN,buff=0.08).align_to(row,LEFT)
        g=VGroup(row,rule,sub); self.fixed(g); return g

    def pill(self,text,width=None,size=SMALL):
        t=self.text(text,size,BOLD); w=max(t.width+0.48,width or 0)
        box=RoundedRectangle(width=w,height=0.62,corner_radius=0.16,stroke_color=BLACK,stroke_width=1.5,fill_color=PAPER_GRAY,fill_opacity=1)
        t.move_to(box); return VGroup(box,t)

    def note(self,title,lines,width=5.6,body_size=21):
        h=self.text(title,24,BOLD)
        body=VGroup(*[self.text(x,body_size) for x in lines]).arrange(DOWN,aligned_edge=LEFT,buff=0.13)
        content=VGroup(h,body).arrange(DOWN,aligned_edge=LEFT,buff=0.18); self.fit(content,width-0.55,3.5)
        box=RoundedRectangle(width=width,height=max(1.35,content.height+0.56),corner_radius=0.12,stroke_color=BLACK,stroke_width=1.5,fill_color=WHITE,fill_opacity=0.97)
        content.move_to(box).align_to(box,LEFT).shift(RIGHT*0.28); return VGroup(box,content)

    def process_row(self,labels,y=-3.42):
        pills=VGroup(*[self.pill(x) for x in labels]).arrange(RIGHT,buff=0.24)
        arrows=VGroup(*[Arrow(pills[i].get_right(),pills[i+1].get_left(),buff=0.08,color=BLACK,stroke_width=2,max_tip_length_to_length_ratio=0.12) for i in range(len(pills)-1)])
        g=VGroup(pills,arrows).move_to([0,y,0]); self.fixed(g); return g

    def opening(self,title,subtitle,labels):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        top=self.text("AUTODESK INVENTOR PROFESSIONAL",25,BOLD); ttl=self.text(title,TITLE,BOLD)
        rule=Line(LEFT*5.6,RIGHT*5.6,color=BLACK,stroke_width=2); sub=self.text(subtitle,27)
        pills=VGroup(*[self.pill(x,size=21) for x in labels]).arrange(RIGHT,buff=0.32)
        arrows=VGroup(*[Arrow(pills[i].get_right(),pills[i+1].get_left(),buff=0.08,color=BLACK,stroke_width=2,max_tip_length_to_length_ratio=0.12) for i in range(len(pills)-1)])
        route=VGroup(pills,arrows); g=VGroup(top,ttl,rule,sub,route).arrange(DOWN,buff=0.34); self.fixed(g)
        self.play(FadeIn(top,shift=UP*0.1),run_time=RUN); self.play(Write(ttl),run_time=RUN_SLOW)
        self.play(Create(rule),FadeIn(sub),run_time=RUN); self.play(LaggedStart(*[FadeIn(p) for p in pills],lag_ratio=0.12),Create(arrows),run_time=1.65)
        self.wait(EXPLAIN); self.clear_scene()

    def base_plate_from_sketch(self,n,width=5.2,depth=3.1,height=0.62,dims="80 × 50 mm",extrude="10 mm"):
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=self.section_header(n,"BUILD THE BASE FROM A 2D SKETCH","As in the House lesson: define and dimension the sketch first, then create volume.")
        outline=Rectangle(width=width,height=depth,color=BLACK,stroke_width=4)
        ch=DashedLine(outline.get_left(),outline.get_right(),color=LIGHT_GRAY,dash_length=0.12)
        cv=DashedLine(outline.get_bottom(),outline.get_top(),color=LIGHT_GRAY,dash_length=0.12)
        lab=self.text(dims,23,BOLD).next_to(outline,DOWN,buff=0.24); self.fixed(lab)
        self.play(Create(outline),Create(ch),Create(cv),FadeIn(lab),run_time=1.4); self.wait(READ)
        row=self.process_row(["SKETCH","DIMENSION",f"EXTRUDE {extrude}","BASE SOLID"])
        self.play(LaggedStart(*[FadeIn(p) for p in row[0]],lag_ratio=0.10),Create(row[1]),run_time=1.35); self.wait(READ)
        self.play(FadeOut(lab),run_time=0.3); self.move_camera(phi=64*DEGREES,theta=-48*DEGREES,zoom=0.88,run_time=1.15)
        preview=cuboid(width,depth,0.05,0.24); self.play(FadeIn(preview),outline.animate.set_opacity(0.28),run_time=0.5)
        body=cuboid(width,depth,height,0.56); self.play(ReplacementTransform(preview,body),FadeOut(outline),FadeOut(ch),FadeOut(cv),run_time=1.25)
        self.play(FadeOut(h),FadeOut(row),run_time=0.45); return body

    def parameter_card(self,title,rows):
        head=self.text(title,23,BOLD); entries=VGroup()
        for label,value in rows:
            lab=self.text(label,19,BOLD); val=self.text(value,19)
            field=RoundedRectangle(width=2.7,height=0.48,corner_radius=0.05,stroke_color=MID_GRAY,stroke_width=1.2,fill_color=WHITE,fill_opacity=1)
            val.move_to(field).align_to(field,LEFT).shift(RIGHT*0.14); entries.add(VGroup(lab,VGroup(field,val)).arrange(RIGHT,buff=0.18))
        entries.arrange(DOWN,aligned_edge=LEFT,buff=0.12); content=VGroup(head,entries).arrange(DOWN,aligned_edge=LEFT,buff=0.22); self.fit(content,4.6,3.4)
        box=RoundedRectangle(width=5.0,height=content.height+0.48,corner_radius=0.10,stroke_color=BLACK,stroke_width=1.5,fill_color="#FAFAFA",fill_opacity=0.98)
        content.move_to(box).align_to(box,LEFT).shift(RIGHT*0.24); g=VGroup(box,content).to_corner(DR,buff=0.48).shift(UP*0.55); self.fixed(g); return g

    def final_orbit(self,message):
        tag=self.text(message,27,BOLD).to_edge(DOWN,buff=0.30); self.fixed(tag); self.play(FadeIn(tag),run_time=0.75)
        self.begin_ambient_camera_rotation(rate=0.10); self.wait(3.0); self.stop_ambient_camera_rotation(); self.wait(0.8)

    def clear_scene(self):
        mobs=list(self.mobjects)
        if mobs: self.play(*[FadeOut(m) for m in mobs],run_time=0.55)
        for m in mobs: self.remove(m)
