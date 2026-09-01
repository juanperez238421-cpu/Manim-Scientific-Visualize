#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5.5 — frame-by-frame residual correction of V5.4."""
from __future__ import annotations
import numpy as np
from manim import *
from Physics9_UniformMotion_Galileo_V5_4_FINAL_FRAME_QA import (
    Physics9UniformMotionGalileoV54FinalFrameQA,DARK_GRAY,MID_GRAY,LIGHT_GRAY,
    RUN,PAUSE_READ,PAUSE_EXPLAIN,
)

class Physics9UniformMotionGalileoV55FrameByFrameFinal(Physics9UniformMotionGalileoV54FinalFrameQA):
    def uniform_motion_two_graphs(self):
        self.set_header(1,"ONE UNIFORM MOTION, TWO GRAPHS","Equal distance in equal time gives a straight position-time graph and a horizontal velocity-time graph.")
        lp=self.panel(5.10,5.15,fill=WHITE).move_to(LEFT*4.35+DOWN*0.10); lt=self.txt("PHYSICAL MOTION",24,BOLD).next_to(lp.get_top(),DOWN,buff=0.22)
        speed=self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",width=4.30,height=0.90,size=31).move_to(lp.get_center()+UP*1.55)
        ty=0.18; track=Line([-6.15,ty,0],[-2.55,ty,0],color=BLACK,stroke_width=4)
        marks=VGroup(*[Line([-5.88+i*0.82,ty-0.18,0],[-5.88+i*0.82,ty+0.18,0],color=MID_GRAY,stroke_width=1.5) for i in range(5)])
        cart=RoundedRectangle(width=0.92,height=0.48,corner_radius=0.08,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([-5.75,ty+0.38,0])
        wheels=VGroup(Circle(radius=0.078,color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+LEFT*0.23),Circle(radius=0.078,color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+RIGHT*0.23)); cartg=VGroup(cart,wheels)
        equal=self.txt("1.5 m each second",21,BOLD,color=DARK_GRAY).next_to(track,DOWN,buff=0.20)
        read=VGroup(self.txt("x-t graph  →  constant slope",20,BOLD),self.txt("v-t graph  →  constant value",20,BOLD)).arrange(DOWN,aligned_edge=LEFT,buff=0.16).move_to(lp.get_center()+DOWN*1.55)
        xb=self.panel(7.60,2.72,fill=WHITE).move_to(RIGHT*3.15+UP*1.38); xt=self.txt("POSITION vs TIME",22,BOLD).next_to(xb.get_top(),DOWN,buff=0.14)
        badge=self.formula_panel(r"\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",width=3.05,height=0.58,size=24).move_to(xb.get_right()+LEFT*1.75+UP*0.73)
        xa=Axes(x_range=[0,4.4,1],y_range=[0,7.8,1],x_length=5.85,y_length=1.60,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(xb.get_center()+DOWN*0.25)
        xg=xa.plot(lambda t:1+1.5*t,x_range=[0,4],color=BLACK,stroke_width=4); xl=VGroup(self.txt("t (s)",17).next_to(xa.x_axis,DOWN,buff=0.07),self.txt("x (m)",17).rotate(PI/2).next_to(xa.y_axis,LEFT,buff=0.11)); x0=Dot(xa.c2p(0,1),radius=0.06,color=BLACK); x4=Dot(xa.c2p(4,7),radius=0.06,color=BLACK)
        vb=self.panel(7.60,2.52,fill=WHITE).move_to(RIGHT*3.15+DOWN*1.80); vt=self.txt("VELOCITY vs TIME",22,BOLD).next_to(vb.get_top(),DOWN,buff=0.16)
        va=Axes(x_range=[0,4.4,1],y_range=[0,2.2,0.5],x_length=5.85,y_length=1.42,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(vb.get_center()+DOWN*0.12)
        vg=va.plot(lambda t:1.5,x_range=[0,4],color=BLACK,stroke_width=4); vl=VGroup(self.txt("t (s)",17).next_to(va.x_axis,DOWN,buff=0.07),self.txt("v (m/s)",17).rotate(PI/2).next_to(va.y_axis,LEFT,buff=0.11)); vlab=self.math(r"v=1.5\,\mathrm{m/s}",25).next_to(va.c2p(2.7,1.5),UP,buff=0.05)
        self.play(FadeIn(lp),FadeIn(lt),FadeIn(speed),run_time=RUN); self.play(Create(track),FadeIn(marks),FadeIn(cartg),FadeIn(equal),run_time=RUN)
        self.play(FadeIn(xb),FadeIn(xt),FadeIn(badge),Create(xa),FadeIn(xl),run_time=RUN); self.play(Create(xg),FadeIn(x0),FadeIn(x4),run_time=RUN)
        self.play(FadeIn(vb),FadeIn(vt),Create(va),FadeIn(vl),run_time=RUN); self.play(Create(vg),FadeIn(vlab),FadeIn(read),run_time=RUN); self.play(cartg.animate.shift(RIGHT*2.75),run_time=2.2,rate_func=linear); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def graph_equation_connection(self):
        self.set_header(3,"READ THE EQUATION FROM THE POSITION-TIME GRAPH","The intercept is the initial position; the slope is the constant velocity.")
        box=self.panel(8.30,5.35,fill=WHITE).move_to(LEFT*3.30+DOWN*0.15); ax=Axes(x_range=[0,4.5,1],y_range=[0,7.8,1],x_length=6.55,y_length=3.65,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(box.get_center()+DOWN*0.20)
        gr=ax.plot(lambda t:1+1.5*t,x_range=[0,4],color=BLACK,stroke_width=4); title=self.txt("POSITION vs TIME",23,BOLD).next_to(box.get_top(),DOWN,buff=0.18); labs=VGroup(self.txt("t (s)",18).next_to(ax.x_axis,DOWN,buff=0.10),self.txt("x (m)",18).rotate(PI/2).next_to(ax.y_axis,LEFT,buff=0.14)); p=Dot(ax.c2p(0,1),radius=0.075,color=BLACK)
        ilab=self.formula_panel(r"x_i=1\,\mathrm{m}",width=2.25,height=0.68,size=27).move_to(ax.c2p(0.75,1.55)); leader=Arrow(ilab.get_left()+DOWN*0.10,p+RIGHT*0.05,buff=0.07,color=MID_GRAY,stroke_width=1.5,max_tip_length_to_length_ratio=0.12)
        tri=Polygon(ax.c2p(1,2.5),ax.c2p(3,2.5),ax.c2p(3,5.5),color=MID_GRAY,stroke_width=2,fill_opacity=0); dt=self.math(r"\Delta t=2\,\mathrm{s}",25).move_to(ax.c2p(2,2.12)); dx=self.math(r"\Delta x=3\,\mathrm{m}",25).move_to(ax.c2p(3.58,4.0))
        slope=self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=\frac32=1.5\,\mathrm{m/s}",width=5.45,height=1.05,size=31).move_to(RIGHT*4.55+UP*1.85)
        mp=self.note_panel("EQUATION MAP",["x_i  →  vertical intercept","v    →  slope of the line","t    →  horizontal coordinate","x    →  predicted position"],width=5.35,title_size=24,body_size=20).move_to(RIGHT*4.55+DOWN*0.35); quick=self.formula_panel(r"x=2+(1.2)(4)=6.8\,\mathrm{m}",width=5.35,height=0.95,size=31).move_to(RIGHT*4.55+DOWN*2.70)
        self.play(FadeIn(box),FadeIn(title),Create(ax),FadeIn(labs),run_time=RUN); self.play(Create(gr),FadeIn(p),FadeIn(ilab),GrowArrow(leader),run_time=RUN); self.play(Create(tri),FadeIn(dt),FadeIn(dx),run_time=RUN); self.play(FadeIn(slope),FadeIn(mp),FadeIn(quick),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_question_v5(self):
        self.set_header(4,"WHY DID GALILEO USE AN INCLINED PLANE?","The incline slows the motion, making position-time measurements easier than in a rapid vertical fall.")
        L=self.panel(6.35,4.45,fill=WHITE).move_to(LEFT*3.55+DOWN*0.15); R=self.panel(6.35,4.45,fill=WHITE).move_to(RIGHT*3.55+DOWN*0.15); lt=self.txt("VERTICAL FALL",25,BOLD).next_to(L.get_top(),DOWN,buff=0.25); rt=self.txt("INCLINED PLANE",25,BOLD).next_to(R.get_top(),DOWN,buff=0.25)
        fl=Line(LEFT*4.75+UP*1.00,LEFT*4.75+DOWN*1.05,color=BLACK,stroke_width=3); b1=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(fl.get_start()); ln=self.txt("too fast to time accurately",20,BOLD,color=DARK_GRAY).move_to(L.get_bottom()+UP*0.55)
        rs=np.array([1.95,-0.80,0.0]); re=np.array([5.10,0.85,0.0]); ramp=Line(rs,re,color=BLACK,stroke_width=4); floor=Line([1.55,-0.80,0],[5.50,-0.80,0],color=BLACK,stroke_width=2); d=(re-rs)/np.linalg.norm(re-rs); n=np.array([-d[1],d[0],0.0]); b2=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(re+n*0.18); rn=self.txt("slower motion  →  measurable positions",20,BOLD,color=DARK_GRAY).move_to(R.get_bottom()+UP*0.55)
        q=self.formula_panel(r"\text{At equal times, will the traveled distances remain equal?}",width=10.4,height=0.95,size=32).to_edge(DOWN,buff=0.28)
        self.play(FadeIn(L),FadeIn(lt),Create(fl),FadeIn(b1),FadeIn(ln),run_time=RUN); self.play(FadeIn(R),FadeIn(rt),Create(ramp),Create(floor),FadeIn(b2),FadeIn(rn),run_time=RUN); self.play(FadeIn(q),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_real_apparatus_v5(self):
        self.set_header(5,"GALILEO'S INCLINED-PLANE EXPERIMENT","Historical reconstruction: same release point, water-clock timing, and repeated position measurements on a shallow ramp.")
        rp=self.panel(9.45,5.25,fill=WHITE).move_to(LEFT*2.55+DOWN*0.12); ip=self.panel(4.25,5.25,fill=WHITE).move_to(RIGHT*5.05+DOWN*0.12); start=np.array([-6.15,-1.35,0.0]); end=np.array([1.15,1.25,0.0]); ramp=Line(start,end,color=BLACK,stroke_width=5); floor=Line([-6.45,-1.35,0],[1.55,-1.35,0],color=BLACK,stroke_width=2); support=Line(end,[1.15,-1.35,0],color=MID_GRAY,stroke_width=2); ball=Circle(radius=0.17,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(end)
        release=self.txt("same release point",19,BOLD).move_to([-0.55,1.95,0]); lead=Arrow(release.get_bottom()+RIGHT*0.55,ball.get_top(),buff=0.12,color=MID_GRAY,stroke_width=1.6,max_tip_length_to_length_ratio=0.12); us=[0.0,1/16,4/16,9/16,1.0]; pts=[end+u*(start-end) for u in us]; dots=VGroup(*[Dot(p,radius=0.055,color=BLACK) for p in pts])
        lpos=[np.array([1.78,0.92,0]),np.array([0.62,0.90,0]),np.array([-0.90,0.48,0]),np.array([-3.30,-0.12,0]),np.array([-5.78,-0.86,0])]; labels=VGroup(); leaders=VGroup()
        for i,(p,pos) in enumerate(zip(pts,lpos)):
            lab=self.txt(f"t={i}",19,BOLD,color=DARK_GRAY).move_to(pos); labels.add(lab); leaders.add(Line(lab.get_bottom(),p,color=LIGHT_GRAY,stroke_width=1.2))
        cap=self.formula_panel(r"\text{record position at equal time intervals}",width=7.35,height=0.82,size=28).move_to(rp.get_center()+DOWN*2.02)
        pt=self.txt("HOW TIME WAS MEASURED",21,BOLD).next_to(ip.get_top(),DOWN,buff=0.20); steps=VGroup(self.txt("1  Release without pushing",18,BOLD),self.txt("2  Collect water during motion",18),self.txt("3  Compare equal water amounts",18)).arrange(DOWN,aligned_edge=LEFT,buff=0.13); self.fit(steps,3.55,1.15); steps.next_to(pt,DOWN,buff=0.18).align_to(ip,LEFT).shift(RIGHT*0.34); div=Line(ip.get_left()+RIGHT*0.30,ip.get_right()+LEFT*0.30,color=LIGHT_GRAY,stroke_width=1.5).move_to(ip.get_center()+DOWN*0.03)
        ct=self.txt("WATER CLOCK",21,BOLD).next_to(div,DOWN,buff=0.13); tank=RoundedRectangle(width=1.15,height=0.82,corner_radius=0.08,stroke_color=BLACK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1).next_to(ct,DOWN,buff=0.09); water=Rectangle(width=0.97,height=0.34,stroke_width=0,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(tank).align_to(tank,DOWN).shift(UP*0.055); noz=Line(tank.get_bottom(),tank.get_bottom()+DOWN*0.15,color=BLACK,stroke_width=1.8); drop=Dot(noz.get_end()+DOWN*0.08,radius=0.032,color=BLACK); collector=RoundedRectangle(width=1.10,height=0.30,corner_radius=0.05,stroke_color=BLACK,stroke_width=1.6,fill_color=WHITE,fill_opacity=1).next_to(drop,DOWN,buff=0.05); note=self.txt("equal water amount = equal time",16,BOLD,color=DARK_GRAY); self.fit(note,3.35,0.32); note.move_to(ip.get_bottom()+UP*0.30); clock=VGroup(ct,tank,water,noz,drop,collector)
        if clock.get_bottom()[1]<note.get_top()[1]+0.10: clock.shift(UP*(note.get_top()[1]+0.14-clock.get_bottom()[1]))
        self.play(FadeIn(rp),FadeIn(ip),run_time=RUN); self.play(Create(ramp),Create(floor),Create(support),FadeIn(ball),run_time=RUN); self.play(FadeIn(release),GrowArrow(lead),FadeIn(dots),FadeIn(leaders),FadeIn(labels),run_time=RUN); self.play(FadeIn(cap),run_time=RUN); self.play(FadeIn(pt),FadeIn(steps),Create(div),run_time=RUN); self.play(FadeIn(clock),FadeIn(note),run_time=RUN); self.wait(PAUSE_READ); self.play(MoveAlongPath(ball,Line(end,start)),run_time=2.8,rate_func=rate_functions.ease_in_quad); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_deduction_v5(self):
        self.set_header(7,"FROM THE DATA TO THE SQUARE-TIME LAW","The cumulative positions are square numbers, so the position-time relation is curved rather than linear.")
        L=self.panel(4.70,4.55,fill=WHITE).move_to(LEFT*4.90+UP*0.05); R=self.panel(7.30,4.55,fill=WHITE).move_to(RIGHT*3.65+UP*0.05); lt=self.txt("LOOK AT THE NUMBERS",23,BOLD).next_to(L.get_top(),DOWN,buff=0.23); sq=VGroup(self.math(r"1=1^2",40),self.math(r"4=2^2",40),self.math(r"9=3^2",40),self.math(r"16=4^2",40)).arrange(DOWN,buff=0.32).move_to(L.get_center()+DOWN*0.18)
        rt=self.txt("POSITION vs TIME",23,BOLD).next_to(R.get_top(),DOWN,buff=0.18); law=self.formula_panel(r"x\propto t^2",width=3.55,height=0.78,size=42).move_to(R.get_center()+UP*1.35); ax=Axes(x_range=[0,4.4,1],y_range=[0,17,4],x_length=5.35,y_length=2.05,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(R.get_center()+DOWN*0.35); curve=ax.plot(lambda t:t**2,x_range=[0,4],color=BLACK,stroke_width=4); labs=VGroup(self.txt("t",18).next_to(ax.x_axis,DOWN,buff=0.06),self.txt("x",18).next_to(ax.y_axis,LEFT,buff=0.09)); strip=self.panel(5.30,0.50,fill=WHITE,stroke=LIGHT_GRAY).move_to(R.get_bottom()+UP*0.30); steep=self.txt("curve becomes steeper as time increases",18,BOLD,color=DARK_GRAY).move_to(strip); contrast=self.formula_panel(r"\text{uniform: straight line}\qquad\neq\qquad\text{Galileo: square-time curve}",width=9.5,height=0.90,size=29).to_edge(DOWN,buff=0.27)
        self.play(FadeIn(L),FadeIn(lt),run_time=RUN); self.play(Write(sq),run_time=RUN); self.play(FadeIn(R),FadeIn(rt),FadeIn(law),run_time=RUN); self.play(Create(ax),FadeIn(labs),Create(curve),run_time=RUN); self.play(FadeIn(strip),FadeIn(steep),FadeIn(contrast),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(8,"INTRODUCTION TO FALLING MOTION","Vertical fall shows the same growing-distance pattern much faster than the inclined-plane experiment.")
        L=self.panel(5.75,5.00,fill=WHITE).move_to(LEFT*4.15+DOWN*0.10); lt=self.txt("EQUAL TIMES  →  BIGGER GAPS",23,BOLD).next_to(L.get_top(),DOWN,buff=0.23); x=-4.95; y0=1.28; u=0.32; ys=[y0,y0-u,y0-4*u,y0-9*u]; line=Line([x,y0+0.18,0],[x,ys[-1]-0.18,0],color=BLACK,stroke_width=3); balls=VGroup(); labels=VGroup()
        for i,y in enumerate(ys): balls.add(Circle(radius=0.11,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([x,y,0])); labels.add(self.txt(f"t={i}",19,BOLD,color=DARK_GRAY).move_to([x+0.65,y,0]))
        gx=-5.72; gaps=VGroup(self.txt("1",19,BOLD).move_to([gx,(ys[0]+ys[1])/2,0]),self.txt("3",19,BOLD).move_to([gx,(ys[1]+ys[2])/2,0]),self.txt("5",19,BOLD).move_to([gx,(ys[2]+ys[3])/2,0])); note=self.txt("successive gaps: 1 : 3 : 5",21,BOLD,color=DARK_GRAY).move_to(L.get_bottom()+UP*0.40)
        eq1=self.formula_panel(r"y=y_i-\frac12gt^2",width=6.1,height=1.12,size=44).move_to(RIGHT*3.55+UP*1.65); rel=self.txt("release from rest",21,BOLD,color=DARK_GRAY).next_to(eq1,UP,buff=0.14); eq2=self.formula_panel(r"y=y_i+v_it-\frac12gt^2",width=6.3,height=1.12,size=41).next_to(eq1,DOWN,buff=0.34); prev=self.note_panel("PREVIEW ONLY",["Focus on the t² pattern today.","The meaning of g and changing velocity comes next."],width=6.35,title_size=24,body_size=20).move_to(RIGHT*3.55+DOWN*1.80)
        self.play(FadeIn(L),FadeIn(lt),Create(line),run_time=RUN)
        for b,l in zip(balls,labels): self.play(FadeIn(b),FadeIn(l),run_time=0.34)
        self.play(FadeIn(gaps),FadeIn(note),run_time=RUN); self.play(FadeIn(rel),FadeIn(eq1),FadeIn(eq2),run_time=RUN); self.play(FadeIn(prev),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

# Preview: manim -pql Physics9_UniformMotion_Galileo_V5_5_FRAME_BY_FRAME_FINAL.py Physics9UniformMotionGalileoV55FrameByFrameFinal --disable_caching
# Final:   manim -pqh Physics9_UniformMotion_Galileo_V5_5_FRAME_BY_FRAME_FINAL.py Physics9UniformMotionGalileoV55FrameByFrameFinal --disable_caching
