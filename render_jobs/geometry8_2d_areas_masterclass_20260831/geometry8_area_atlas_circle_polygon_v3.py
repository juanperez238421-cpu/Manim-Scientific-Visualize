#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *

class Geometry8AreaCirclePolygonMixin:
    """Explicit figure chapters."""

    def circle_explicit(self):
        h=self.header(10,"7 · CIRCLE","The radius generates the circle; sector rearrangement connects circumference to area.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-3.75,-.10,0]); radius=1.75
        c=Circle(radius,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.25).move_to(center)
        rline=Line(center,center+RIGHT*radius,color=INK,stroke_width=4)
        dot=Dot(center,radius=.07,color=INK)

        self.mark_stage(strip,0)
        self.play(FadeIn(dot),Create(rline),run_time=.42)
        self.play(Create(c),Rotate(rline,angle=TAU,about_point=center),run_time=1.25,rate_func=linear)

        self.mark_stage(strip,1)
        diam=DashedLine(center+LEFT*radius,center+RIGHT*radius,color=MID,stroke_width=2.8)
        rlab=self.eq("r",36).next_to(Line(center,center+RIGHT*radius),UP,buff=.07)
        dlab=self.eq("d=2r",34).next_to(diam,DOWN,buff=.12)
        self.play(Create(diam),FadeIn(rlab),FadeIn(dlab),run_time=.60)

        self.mark_stage(strip,2)
        radial=VGroup()
        for k in range(16):
            angle=TAU*k/16
            radial.add(Line(center,center+radius*np.array([math.cos(angle),math.sin(angle),0]),color=LIGHT,stroke_width=1.4))
        self.play(LaggedStart(*[Create(x) for x in radial],lag_ratio=.03),run_time=.90)
        strip_shape=Polygon(
            [1.00,-1.05,0],[5.85,-1.05,0],[5.55,1.05,0],[.70,1.05,0],
            stroke_color=INK,stroke_width=4,fill_color=FILL,fill_opacity=.62,
        )
        saw_top=VGroup(*[Line([.70+i*.61,1.05,0],[1.00+i*.61,1.24,0],color=MID,stroke_width=1.5) for i in range(8)])
        saw_bot=VGroup(*[Line([1.00+i*.61,-1.05,0],[1.30+i*.61,-1.24,0],color=MID,stroke_width=1.5) for i in range(8)])
        self.play(FadeIn(strip_shape,shift=RIGHT*.08),FadeIn(saw_top),FadeIn(saw_bot),run_time=.65)
        base=self.dimension([.75,-1.47,0],[5.75,-1.47,0],r"\pi r",DOWN,34)
        height=self.dimension([6.18,-1.05,0],[6.18,1.05,0],"r",RIGHT,34)
        self.play(GrowFromCenter(base[0]),GrowFromCenter(height[0]),FadeIn(base[1]),FadeIn(height[1]),run_time=.62)
        formula=self.box(r"A=(\pi r)(r)=\pi r^2",5.9,55).move_to(RIGHT*3.55+UP*1.82)
        self.play(FadeIn(formula),run_time=.48); self.wait(.55)

        self.mark_stage(strip,3)
        self.play(FadeOut(strip_shape),FadeOut(saw_top),FadeOut(saw_bot),FadeOut(base),FadeOut(height),FadeOut(formula),run_time=.35)
        ex=self.example_stack("Given: r = 4 cm",r"A=\pi r^2",r"A=\pi(4)^2=16\pi",r"A\approx50.27\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def regular_polygon_explicit(self):
        h=self.header(11,"8 · REGULAR POLYGON","Split the polygon from its center: equal triangles connect apothem a and perimeter P.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-3.70,-.10,0]); R=1.90
        vertices=[center+R*np.array([math.cos(PI/6+k*TAU/6),math.sin(PI/6+k*TAU/6),0]) for k in range(6)]
        poly=Polygon(*vertices,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.62)

        self.mark_stage(strip,0)
        self.play(Create(poly),FadeIn(Dot(center,radius=.07,color=INK)),run_time=.75)

        self.mark_stage(strip,1)
        spokes=VGroup(*[Line(center,v,color=MID,stroke_width=2.2) for v in vertices])
        side_mid=(vertices[0]+vertices[1])/2
        ap=DashedLine(center,side_mid,color=INK,stroke_width=2.8)
        alab=self.eq("a",35).next_to(ap,RIGHT,buff=.07)
        side=Line(vertices[0],vertices[1])
        slab=self.eq("s",34).next_to(side,UR,buff=.05)
        # The apothem is perpendicular to a side; show this explicitly because
        # it is the height used in every center triangle.
        ap_dir=(side_mid-center)/np.linalg.norm(side_mid-center)
        side_dir=(vertices[1]-vertices[0])/np.linalg.norm(vertices[1]-vertices[0])
        right=self.right_mark(side_mid,-ap_dir,side_dir,.22)
        plab=self.eq(r"P=\text{sum of all side lengths}",31).move_to([-3.70,-2.45,0])
        self.play(LaggedStart(*[Create(s) for s in spokes],lag_ratio=.06),Create(ap),FadeIn(alab),FadeIn(slab),FadeIn(right),FadeIn(plab),run_time=.85)

        self.mark_stage(strip,2)
        one=Polygon(center,vertices[0],vertices[1],stroke_color=INK,stroke_width=3,fill_color=WHITE,fill_opacity=.80)
        self.play(FadeIn(one),run_time=.38)
        deriv=VGroup(
            self.eq(r"A_{1\,\triangle}=\frac12 s a",39),
            self.eq(r"A=\frac12(ns)a",39),
            self.eq(r"ns=P",39),
            self.box(r"A=\frac{P\,a}{2}",5.5,58),
        ).arrange(DOWN,buff=.18).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.36); self.wait(.22)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),FadeOut(one),run_time=.32)
        ex=self.example_stack("Given: P = 30 cm, a = 4 cm",r"A=\frac{P\,a}{2}",r"A=\frac{(30)(4)}{2}",r"A=60\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()
