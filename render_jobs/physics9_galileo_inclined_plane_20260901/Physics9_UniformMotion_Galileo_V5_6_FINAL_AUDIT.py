#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5.6 — final residual visual correction after V5.5 render audit."""
from __future__ import annotations
import numpy as np
from manim import *
from Physics9_UniformMotion_Galileo_V5_5_FRAME_BY_FRAME_FINAL import (
    Physics9UniformMotionGalileoV55FrameByFrameFinal,
    DARK_GRAY, MID_GRAY, LIGHT_GRAY, RUN, PAUSE_READ, PAUSE_EXPLAIN,
)

class Physics9UniformMotionGalileoV56FinalAudit(Physics9UniformMotionGalileoV55FrameByFrameFinal):
    """Correct the three residual collisions visible in the rendered V5.5 audit."""

    def graph_equation_connection(self):
        self.set_header(
            3,
            "READ THE EQUATION FROM THE POSITION-TIME GRAPH",
            "The intercept is the initial position; the slope is the constant velocity.",
        )
        box = self.panel(8.30, 5.35, fill=WHITE).move_to(LEFT*3.30 + DOWN*0.15)
        ax = Axes(
            x_range=[0,4.5,1], y_range=[0,7.8,1], x_length=6.55, y_length=3.65,
            axis_config={"color":BLACK,"stroke_width":2,"include_tip":False},
        ).move_to(box.get_center()+DOWN*0.20)
        gr = ax.plot(lambda t: 1+1.5*t, x_range=[0,4], color=BLACK, stroke_width=4)
        title = self.txt("POSITION vs TIME",23,BOLD).next_to(box.get_top(),DOWN,buff=0.18)
        labs = VGroup(
            self.txt("t (s)",18).next_to(ax.x_axis,DOWN,buff=0.10),
            self.txt("x (m)",18).rotate(PI/2).next_to(ax.y_axis,LEFT,buff=0.14),
        )
        p = Dot(ax.c2p(0,1),radius=0.075,color=BLACK)
        ilab = self.formula_panel(r"x_i=1\,\mathrm{m}",width=2.35,height=0.72,size=28)
        ilab.move_to(box.get_left()+RIGHT*1.65+UP*1.35)
        leader = Arrow(
            ilab.get_bottom()+LEFT*0.42,
            p.get_center()+UP*0.05,
            buff=0.08,color=MID_GRAY,stroke_width=1.5,max_tip_length_to_length_ratio=0.10,
        )
        tri = Polygon(
            ax.c2p(1,2.5),ax.c2p(3,2.5),ax.c2p(3,5.5),
            color=MID_GRAY,stroke_width=2,fill_opacity=0,
        )
        dt = self.math(r"\Delta t=2\,\mathrm{s}",25).move_to(ax.c2p(2,2.12))
        dx = self.math(r"\Delta x=3\,\mathrm{m}",25).move_to(ax.c2p(3.58,4.0))
        slope = self.formula_panel(
            r"v=\frac{\Delta x}{\Delta t}=\frac32=1.5\,\mathrm{m/s}",
            width=5.45,height=1.05,size=31,
        ).move_to(RIGHT*4.55+UP*1.85)
        mp = self.note_panel(
            "EQUATION MAP",
            ["x_i  →  vertical intercept","v    →  slope of the line","t    →  horizontal coordinate","x    →  predicted position"],
            width=5.35,title_size=24,body_size=20,
        ).move_to(RIGHT*4.55+DOWN*0.35)
        quick = self.formula_panel(r"x=2+(1.2)(4)=6.8\,\mathrm{m}",width=5.35,height=0.95,size=31).move_to(RIGHT*4.55+DOWN*2.70)
        self.play(FadeIn(box),FadeIn(title),Create(ax),FadeIn(labs),run_time=RUN)
        self.play(Create(gr),FadeIn(p),FadeIn(ilab),GrowArrow(leader),run_time=RUN)
        self.play(Create(tri),FadeIn(dt),FadeIn(dx),run_time=RUN)
        self.play(FadeIn(slope),FadeIn(mp),FadeIn(quick),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S INCLINED-PLANE EXPERIMENT",
            "Historical reconstruction: same release point, water-clock timing, and repeated position measurements on a shallow ramp.",
        )
        rp = self.panel(9.45,5.25,fill=WHITE).move_to(LEFT*2.55+DOWN*0.12)
        ip = self.panel(4.25,5.25,fill=WHITE).move_to(RIGHT*5.05+DOWN*0.12)
        start=np.array([-6.15,-1.35,0.0]); end=np.array([1.15,1.25,0.0])
        ramp=Line(start,end,color=BLACK,stroke_width=5)
        floor=Line([-6.45,-1.35,0],[1.55,-1.35,0],color=BLACK,stroke_width=2)
        support=Line(end,[1.15,-1.35,0],color=MID_GRAY,stroke_width=2)
        ball=Circle(radius=0.17,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(end)
        release=self.txt("same release point",19,BOLD).move_to([-0.55,1.98,0])
        lead=Arrow(release.get_bottom()+RIGHT*0.55,ball.get_top(),buff=0.12,color=MID_GRAY,stroke_width=1.6,max_tip_length_to_length_ratio=0.12)
        us=[0.0,1/16,4/16,9/16,1.0]
        pts=[end+u*(start-end) for u in us]
        dots=VGroup(*[Dot(p,radius=0.055,color=BLACK) for p in pts])
        lpos=[
            np.array([1.82,1.15,0.0]),
            np.array([0.52,1.52,0.0]),
            np.array([-0.92,1.02,0.0]),
            np.array([-3.28,0.35,0.0]),
            np.array([-5.62,-0.45,0.0]),
        ]
        labels=VGroup(); leaders=VGroup()
        for i,(p,pos) in enumerate(zip(pts,lpos)):
            lab=self.txt(f"t={i}",19,BOLD,color=DARK_GRAY).move_to(pos)
            labels.add(lab)
            leaders.add(Line(lab.get_bottom(),p,color=LIGHT_GRAY,stroke_width=1.2))
        cap=self.formula_panel(r"\text{record position at equal time intervals}",width=7.20,height=0.80,size=27).move_to(rp.get_center()+DOWN*2.03)
        pt=self.txt("HOW TIME WAS MEASURED",21,BOLD).next_to(ip.get_top(),DOWN,buff=0.20)
        steps=VGroup(
            self.txt("1  Release without pushing",18,BOLD),
            self.txt("2  Collect water during motion",18),
            self.txt("3  Compare equal water amounts",18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.13)
        self.fit(steps,3.55,1.15)
        steps.next_to(pt,DOWN,buff=0.18).align_to(ip,LEFT).shift(RIGHT*0.34)
        div=Line(ip.get_left()+RIGHT*0.30,ip.get_right()+LEFT*0.30,color=LIGHT_GRAY,stroke_width=1.5).move_to(ip.get_center()+DOWN*0.03)
        ct=self.txt("WATER CLOCK",21,BOLD).next_to(div,DOWN,buff=0.13)
        tank=RoundedRectangle(width=1.15,height=0.82,corner_radius=0.08,stroke_color=BLACK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1).next_to(ct,DOWN,buff=0.09)
        water=Rectangle(width=0.97,height=0.34,stroke_width=0,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(tank).align_to(tank,DOWN).shift(UP*0.055)
        noz=Line(tank.get_bottom(),tank.get_bottom()+DOWN*0.15,color=BLACK,stroke_width=1.8)
        drop=Dot(noz.get_end()+DOWN*0.08,radius=0.032,color=BLACK)
        collector=RoundedRectangle(width=1.10,height=0.30,corner_radius=0.05,stroke_color=BLACK,stroke_width=1.6,fill_color=WHITE,fill_opacity=1).next_to(drop,DOWN,buff=0.05)
        note=self.txt("equal water amount = equal time",16,BOLD,color=DARK_GRAY)
        self.fit(note,3.35,0.32); note.move_to(ip.get_bottom()+UP*0.30)
        clock=VGroup(ct,tank,water,noz,drop,collector)
        if clock.get_bottom()[1] < note.get_top()[1]+0.10:
            clock.shift(UP*(note.get_top()[1]+0.14-clock.get_bottom()[1]))
        self.play(FadeIn(rp),FadeIn(ip),run_time=RUN)
        self.play(Create(ramp),Create(floor),Create(support),FadeIn(ball),run_time=RUN)
        self.play(FadeIn(release),GrowArrow(lead),FadeIn(dots),FadeIn(leaders),FadeIn(labels),run_time=RUN)
        self.play(FadeIn(cap),run_time=RUN)
        self.play(FadeIn(pt),FadeIn(steps),Create(div),run_time=RUN)
        self.play(FadeIn(clock),FadeIn(note),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(MoveAlongPath(ball,Line(end,start)),run_time=2.8,rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(
            8,
            "INTRODUCTION TO FALLING MOTION",
            "Vertical fall shows the same growing-distance pattern much faster than the inclined-plane experiment.",
        )
        L=self.panel(5.75,5.00,fill=WHITE).move_to(LEFT*4.15+DOWN*0.10)
        lt=self.txt("EQUAL TIMES  →  BIGGER GAPS",23,BOLD).next_to(L.get_top(),DOWN,buff=0.23)
        x=-4.95; y0=1.42; u=0.36
        ys=[y0,y0-u,y0-4*u,y0-9*u]
        line=Line([x,y0+0.16,0],[x,ys[-1]-0.16,0],color=BLACK,stroke_width=3)
        balls=VGroup(); labels=VGroup()
        for i,y in enumerate(ys):
            balls.add(Circle(radius=0.085,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([x,y,0]))
            labels.add(self.txt(f"t={i}",19,BOLD,color=DARK_GRAY).move_to([x+0.70,y,0]))
        gx=-5.72
        gaps=VGroup(
            self.txt("1",19,BOLD).move_to([gx,(ys[0]+ys[1])/2,0]),
            self.txt("3",19,BOLD).move_to([gx,(ys[1]+ys[2])/2,0]),
            self.txt("5",19,BOLD).move_to([gx,(ys[2]+ys[3])/2,0]),
        )
        note=self.txt("successive gaps: 1 : 3 : 5",21,BOLD,color=DARK_GRAY).move_to(L.get_bottom()+UP*0.38)
        eq1=self.formula_panel(r"y=y_i-\frac12gt^2",width=6.1,height=1.12,size=44).move_to(RIGHT*3.55+UP*1.65)
        rel=self.txt("release from rest",21,BOLD,color=DARK_GRAY).next_to(eq1,UP,buff=0.14)
        eq2=self.formula_panel(r"y=y_i+v_it-\frac12gt^2",width=6.3,height=1.12,size=41).next_to(eq1,DOWN,buff=0.34)
        prev=self.note_panel(
            "PREVIEW ONLY",
            ["Focus on the t² pattern today.","The meaning of g and changing velocity comes next."],
            width=6.35,title_size=24,body_size=20,
        ).move_to(RIGHT*3.55+DOWN*1.80)
        self.play(FadeIn(L),FadeIn(lt),Create(line),run_time=RUN)
        for b,l in zip(balls,labels):
            self.play(FadeIn(b),FadeIn(l),run_time=0.34)
        self.play(FadeIn(gaps),FadeIn(note),run_time=RUN)
        self.play(FadeIn(rel),FadeIn(eq1),FadeIn(eq2),run_time=RUN)
        self.play(FadeIn(prev),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

# Preview: manim -pql Physics9_UniformMotion_Galileo_V5_6_FINAL_AUDIT.py Physics9UniformMotionGalileoV56FinalAudit --disable_caching
# Final:   manim -pqh Physics9_UniformMotion_Galileo_V5_6_FINAL_AUDIT.py Physics9UniformMotionGalileoV56FinalAudit --disable_caching
