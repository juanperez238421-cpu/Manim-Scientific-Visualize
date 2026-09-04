#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Uniform Motion + Galileo V5.3 · full-total visual rebuild.

This version is a frame-by-frame redesign of V5.2.  The instructional scope is
unchanged: constant-velocity motion -> x(t) and v(t) graphs -> deduction of
x = x_i + vt -> Galileo's inclined-plane experiment -> time/position data ->
square-time law -> falling-motion preview.  Formal acceleration is postponed.

V5.3 intentionally uses fewer simultaneous elements, larger text, independent
layout zones, and clean section transitions.  It also removes the compressed
0,1,4,9,16 number-line view that forced t=0 and t=1 labels to collide.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_UniformMotion_Galileo_V5_2_FINAL_QA import (
    Physics9UniformMotionGalileoV52FinalQA,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    RUN_FAST,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)
from Physics9_UniformMotion_Galileo_V5_1_SENIOR_QA import PAUSE_WORK


class Physics9UniformMotionGalileoV53TotalQA(Physics9UniformMotionGalileoV52FinalQA):
    """V5.3: larger, separated, transition-safe classroom master scene."""

    def set_header(self, number, title, subtitle):
        if self.header_group is not None:
            self.remove(self.header_group)
            self.header_group = None
        num_box = RoundedRectangle(width=0.72,height=0.52,corner_radius=0.10,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1)
        num = self.txt(f"{number:02d}", 22, BOLD).move_to(num_box)
        title_m = self.txt(title, 28, BOLD)
        self.fit(title_m, 12.9, 0.48)
        row = VGroup(VGroup(num_box, num), title_m).arrange(RIGHT, buff=0.20)
        self.fit(row, 14.35, 0.56)
        row.to_edge(UP, buff=0.15).align_to(LEFT * 7.22, LEFT)
        subtitle_m = self.txt(subtitle, 19, color=DARK_GRAY)
        self.fit(subtitle_m, 13.8, 0.50)
        subtitle_m.next_to(row, DOWN, buff=0.08).align_to(row, LEFT)
        rule = Line(LEFT * 7.25, RIGHT * 7.25, color=LIGHT_GRAY, stroke_width=1.5)
        rule.next_to(subtitle_m, DOWN, buff=0.08)
        self.header_group = VGroup(row, subtitle_m, rule)
        self.add(self.header_group)

    def clear_stage(self):
        targets = list(self.mobjects)
        if targets:
            self.play(*[FadeOut(m) for m in targets], run_time=0.55)
        self.header_group = None
        self.wait(0.10)

    def opening_v5(self):
        kicker = self.txt("PHYSICS 9 | KINEMATICS", 29, BOLD)
        main = self.txt("FROM MOTION GRAPHS TO GALILEO'S EXPERIMENT", 43, BOLD)
        sub = self.txt("Observe -> graph -> deduce -> test a new kind of motion", 27)
        target = self.formula_panel(r"\boxed{x=x_i+vt}", width=5.4, height=1.18, size=52)
        question = self.txt("Will the same rule describe a ball rolling down an inclined plane?",24,BOLD,color=DARK_GRAY)
        group = VGroup(kicker, main, sub, target, question).arrange(DOWN, buff=0.38)
        group.move_to(ORIGIN)
        self.fit(group, 14.0, 6.7)
        self.play(FadeIn(kicker, shift=UP * 0.10), run_time=RUN)
        self.play(Write(main), run_time=RUN)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.play(FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    def uniform_motion_two_graphs(self):
        self.set_header(1,"ONE UNIFORM MOTION, TWO GRAPHS","Equal distance in equal time gives a straight x-t graph and a horizontal v-t graph.")
        left_panel = self.panel(5.05, 5.20, fill=WHITE).move_to(LEFT * 4.35 + DOWN * 0.12)
        left_title = self.txt("PHYSICAL MOTION", 24, BOLD).next_to(left_panel.get_top(), DOWN, buff=0.23)
        speed = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",width=4.25,height=0.90,size=31).move_to(left_panel.get_center() + UP * 1.55)
        track_y = 0.20
        track = Line([-6.15, track_y, 0], [-2.55, track_y, 0], color=BLACK, stroke_width=4)
        marks = VGroup(*[Line([-5.88 + i * 0.82, track_y - 0.18, 0],[-5.88 + i * 0.82, track_y + 0.18, 0],color=MID_GRAY,stroke_width=1.5) for i in range(5)])
        cart = RoundedRectangle(width=0.92,height=0.48,corner_radius=0.08,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([-5.75, track_y + 0.38, 0])
        wheels = VGroup(Circle(radius=0.078,color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+LEFT*0.23),Circle(radius=0.078,color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+RIGHT*0.23))
        cartg = VGroup(cart, wheels)
        equal_note = self.txt("1.5 m each second", 21, BOLD, color=DARK_GRAY).next_to(track, DOWN, buff=0.20)
        interpretation = VGroup(self.txt("x-t graph -> constant slope",20,BOLD),self.txt("v-t graph -> constant value",20,BOLD)).arrange(DOWN,aligned_edge=LEFT,buff=0.16)
        interpretation.move_to(left_panel.get_center() + DOWN * 1.55)
        x_box = self.panel(7.60, 2.72, fill=WHITE).move_to(RIGHT * 3.15 + UP * 1.38)
        v_box = self.panel(7.60, 2.52, fill=WHITE).move_to(RIGHT * 3.15 + DOWN * 1.80)
        xaxes = Axes(x_range=[0,4.4,1],y_range=[0,7.8,1],x_length=5.95,y_length=1.72,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(x_box.get_center()+DOWN*0.12)
        xgraph = xaxes.plot(lambda t:1+1.5*t,x_range=[0,4],color=BLACK,stroke_width=4)
        xtitle = self.txt("POSITION vs TIME",22,BOLD).next_to(x_box.get_top(),DOWN,buff=0.17)
        xlabs = VGroup(self.txt("t (s)",17).next_to(xaxes.x_axis,DOWN,buff=0.08),self.txt("x (m)",17).rotate(PI/2).next_to(xaxes.y_axis,LEFT,buff=0.11))
        x0=Dot(xaxes.c2p(0,1),radius=0.06,color=BLACK); x4=Dot(xaxes.c2p(4,7),radius=0.06,color=BLACK)
        slope_label=self.math(r"\frac{\Delta x}{\Delta t}=1.5\,\mathrm{m/s}",24).move_to(x_box.get_right()+LEFT*1.50+DOWN*0.82)
        vaxes=Axes(x_range=[0,4.4,1],y_range=[0,2.2,0.5],x_length=5.95,y_length=1.48,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(v_box.get_center()+DOWN*0.10)
        vgraph=vaxes.plot(lambda t:1.5,x_range=[0,4],color=BLACK,stroke_width=4)
        vtitle=self.txt("VELOCITY vs TIME",22,BOLD).next_to(v_box.get_top(),DOWN,buff=0.16)
        vlabs=VGroup(self.txt("t (s)",17).next_to(vaxes.x_axis,DOWN,buff=0.07),self.txt("v (m/s)",17).rotate(PI/2).next_to(vaxes.y_axis,LEFT,buff=0.11))
        vlabel=self.math(r"v=1.5\,\mathrm{m/s}",25).next_to(vaxes.c2p(2.7,1.5),UP,buff=0.05)
        self.play(FadeIn(left_panel),FadeIn(left_title),FadeIn(speed),run_time=RUN)
        self.play(Create(track),FadeIn(marks),FadeIn(cartg),FadeIn(equal_note),run_time=RUN)
        self.play(FadeIn(x_box),FadeIn(xtitle),Create(xaxes),FadeIn(xlabs),run_time=RUN)
        self.play(Create(xgraph),FadeIn(x0),FadeIn(x4),FadeIn(slope_label),run_time=RUN)
        self.play(FadeIn(v_box),FadeIn(vtitle),Create(vaxes),FadeIn(vlabs),run_time=RUN)
        self.play(Create(vgraph),FadeIn(vlabel),run_time=RUN)
        self.play(FadeIn(interpretation),run_time=RUN)
        self.play(cartg.animate.shift(RIGHT*2.75),run_time=2.2,rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def derive_position_equation(self):
        self.set_header(2,"DEDUCE x = x_i + vt FROM THE VELOCITY DEFINITION","Use displacement = final position - initial position, then isolate the final position.")
        measured=self.note_panel("WHAT WE MEASURE",["x_i : initial position","x   : final position","t   : elapsed time","v   : constant velocity"],width=4.25,title_size=24,body_size=21).move_to(LEFT*5.05+DOWN*0.10)
        row_y=[1.75,0.60,-0.55,-1.70]
        labels=VGroup(
            self.txt("1  Start with velocity",21,BOLD,color=DARK_GRAY).move_to([-1.0,row_y[0],0]),
            self.txt("2  Replace displacement",21,BOLD,color=DARK_GRAY).move_to([-1.0,row_y[1],0]),
            self.txt("3  Multiply by t",21,BOLD,color=DARK_GRAY).move_to([-1.0,row_y[2],0]),
            self.txt("4  Isolate x",21,BOLD,color=DARK_GRAY).move_to([-1.0,row_y[3],0]),
        )
        eqs=VGroup(self.math(r"v=\frac{\Delta x}{\Delta t}",50).move_to([3.20,row_y[0],0]),self.math(r"v=\frac{x-x_i}{t}",50).move_to([3.20,row_y[1],0]),self.math(r"vt=x-x_i",50).move_to([3.20,row_y[2],0]),self.math(r"\boxed{x=x_i+vt}",58).move_to([3.20,row_y[3],0]))
        arrows=VGroup(*[Arrow([3.20,row_y[i]-0.34,0],[3.20,row_y[i+1]+0.34,0],buff=0.08,color=MID_GRAY,stroke_width=1.8) for i in range(3)])
        meaning=self.formula_panel(r"\text{final position}=\text{starting position}+\text{distance traveled}",width=10.4,height=0.95,size=31).to_edge(DOWN,buff=0.30).shift(RIGHT*0.85)
        self.play(FadeIn(measured),run_time=RUN)
        self.play(FadeIn(labels[0]),Write(eqs[0]),run_time=RUN)
        for i in range(1,4): self.play(GrowArrow(arrows[i-1]),FadeIn(labels[i]),Write(eqs[i]),run_time=RUN)
        self.play(FadeIn(meaning),run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def graph_equation_connection(self):
        self.set_header(3,"READ x = x_i + vt DIRECTLY FROM THE POSITION-TIME GRAPH","The intercept tells where the object starts; the slope tells how fast position changes.")
        graph_box=self.panel(8.30,5.35,fill=WHITE).move_to(LEFT*3.30+DOWN*0.15)
        axes=Axes(x_range=[0,4.5,1],y_range=[0,7.8,1],x_length=6.55,y_length=3.65,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(graph_box.get_center()+DOWN*0.20)
        graph=axes.plot(lambda t:1+1.5*t,x_range=[0,4],color=BLACK,stroke_width=4)
        title=self.txt("POSITION vs TIME",23,BOLD).next_to(graph_box.get_top(),DOWN,buff=0.18)
        labs=VGroup(self.txt("t (s)",18).next_to(axes.x_axis,DOWN,buff=0.10),self.txt("x (m)",18).rotate(PI/2).next_to(axes.y_axis,LEFT,buff=0.14))
        intercept=Dot(axes.c2p(0,1),radius=0.075,color=BLACK)
        ilab=self.math(r"x_i=1\,\mathrm{m}",29).next_to(intercept,RIGHT+UP,buff=0.14)
        tri=Polygon(axes.c2p(1,2.5),axes.c2p(3,2.5),axes.c2p(3,5.5),color=MID_GRAY,stroke_width=2,fill_opacity=0)
        dt=self.math(r"\Delta t=2\,\mathrm{s}",25).move_to(axes.c2p(2,2.15)); dx=self.math(r"\Delta x=3\,\mathrm{m}",25).move_to(axes.c2p(3.55,4.0))
        slope_card=self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=\frac{3}{2}=1.5\,\mathrm{m/s}",width=5.45,height=1.05,size=31).move_to(RIGHT*4.55+UP*1.85)
        meaning=self.note_panel("EQUATION MAP",["x_i -> vertical intercept","v   -> slope of the line","t   -> horizontal coordinate","x   -> predicted position"],width=5.35,title_size=24,body_size=20).move_to(RIGHT*4.55+DOWN*0.35)
        quick=self.formula_panel(r"x=2+(1.2)(4)=6.8\,\mathrm{m}",width=5.35,height=0.95,size=31).move_to(RIGHT*4.55+DOWN*2.70)
        self.play(FadeIn(graph_box),FadeIn(title),Create(axes),FadeIn(labs),run_time=RUN)
        self.play(Create(graph),FadeIn(intercept),FadeIn(ilab),run_time=RUN)
        self.play(Create(tri),FadeIn(dt),FadeIn(dx),run_time=RUN)
        self.play(FadeIn(slope_card),FadeIn(meaning),FadeIn(quick),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_question_v5(self):
        self.set_header(4,"WHY DID GALILEO USE AN INCLINED PLANE?","Vertical fall is too fast for precise position-time measurements; the incline slows the motion enough to study it.")
        left=self.panel(6.35,4.45,fill=WHITE).move_to(LEFT*3.55+DOWN*0.15); right=self.panel(6.35,4.45,fill=WHITE).move_to(RIGHT*3.55+DOWN*0.15)
        ltitle=self.txt("VERTICAL FALL",25,BOLD).next_to(left.get_top(),DOWN,buff=0.25); rtitle=self.txt("INCLINED PLANE",25,BOLD).next_to(right.get_top(),DOWN,buff=0.25)
        fall_line=Line(LEFT*4.75+UP*1.00,LEFT*4.75+DOWN*1.05,color=BLACK,stroke_width=3)
        ball1=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(fall_line.get_start())
        lnote=self.txt("too fast to time accurately",20,BOLD,color=DARK_GRAY).move_to(left.get_bottom()+UP*0.55)
        ramp=Line(RIGHT*1.95+DOWN*0.80,RIGHT*5.10+UP*0.85,color=BLACK,stroke_width=4); floor=Line(RIGHT*1.55+DOWN*0.80,RIGHT*5.50+DOWN*0.80,color=BLACK,stroke_width=2)
        ball2=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(ramp.get_end()+UP*0.18)
        rnote=self.txt("slower motion -> measurable positions",20,BOLD,color=DARK_GRAY).move_to(right.get_bottom()+UP*0.55)
        q=self.formula_panel(r"\text{At equal times, will the traveled distances remain equal?}",width=10.4,height=0.95,size=32).to_edge(DOWN,buff=0.28)
        self.play(FadeIn(left),FadeIn(ltitle),Create(fall_line),FadeIn(ball1),FadeIn(lnote),run_time=RUN)
        self.play(FadeIn(right),FadeIn(rtitle),Create(ramp),Create(floor),FadeIn(ball2),FadeIn(rnote),run_time=RUN)
        self.play(FadeIn(q),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_real_apparatus_v5(self):
        self.set_header(5,"GALILEO'S INCLINED-PLANE EXPERIMENT","Historical reconstruction: same release point, water-clock timing, and repeated position measurements along a shallow ramp.")
        ramp_panel=self.panel(9.45,5.25,fill=WHITE).move_to(LEFT*2.55+DOWN*0.12); instr_panel=self.panel(4.25,5.25,fill=WHITE).move_to(RIGHT*5.05+DOWN*0.12)
        start=np.array([-6.15,-1.35,0.0]); end=np.array([1.15,1.25,0.0])
        ramp=Line(start,end,color=BLACK,stroke_width=5); floor=Line([-6.45,-1.35,0],[1.55,-1.35,0],color=BLACK,stroke_width=2); support=Line(end,[1.15,-1.35,0],color=MID_GRAY,stroke_width=2)
        ball=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(end)
        release=self.txt("same release point",19,BOLD).move_to([0.10,1.75,0]); leader=Arrow(release.get_bottom(),ball.get_top(),buff=0.10,color=MID_GRAY,stroke_width=1.6,max_tip_length_to_length_ratio=0.12)
        direction=(start-end)/np.linalg.norm(start-end); normal=np.array([-direction[1],direction[0],0.0]); us=[0.0,1/16,4/16,9/16,1.0]; points=[end+u*(start-end) for u in us]
        markers=VGroup(); labels=VGroup(); label_offsets=[normal*0.50+direction*0.05,-normal*0.52+direction*0.05,normal*0.43,-normal*0.45,normal*0.42]
        for i,(p,off) in enumerate(zip(points,label_offsets)):
            markers.add(Dot(p,radius=0.055,color=BLACK)); labels.add(self.txt(f"t={i}",19,BOLD,color=DARK_GRAY).move_to(p+off))
        ramp_caption=self.formula_panel(r"\text{record the ball position at equal time intervals}",width=7.65,height=0.88,size=29).move_to(ramp_panel.get_center()+DOWN*2.00)
        ptitle=self.txt("HOW TIME WAS MEASURED",23,BOLD).next_to(instr_panel.get_top(),DOWN,buff=0.22)
        steps=VGroup(self.txt("1  Release without pushing",19,BOLD),self.txt("2  Collect water while ball moves",19),self.txt("3  Compare equal water amounts",19)).arrange(DOWN,aligned_edge=LEFT,buff=0.14)
        steps.next_to(ptitle,DOWN,buff=0.20).align_to(instr_panel,LEFT).shift(RIGHT*0.32)
        divider=Line(instr_panel.get_left()+RIGHT*0.30,instr_panel.get_right()+LEFT*0.30,color=LIGHT_GRAY,stroke_width=1.5).move_to(instr_panel.get_center()+DOWN*0.35)
        ctitle=self.txt("WATER CLOCK",22,BOLD).next_to(divider,DOWN,buff=0.16)
        tank=RoundedRectangle(width=1.25,height=0.95,corner_radius=0.08,stroke_color=BLACK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1).next_to(ctitle,DOWN,buff=0.12)
        water=Rectangle(width=1.05,height=0.40,stroke_width=0,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(tank).align_to(tank,DOWN).shift(UP*0.06)
        nozzle=Line(tank.get_bottom(),tank.get_bottom()+DOWN*0.18,color=BLACK,stroke_width=1.8); drop=Dot(nozzle.get_end()+DOWN*0.10,radius=0.035,color=BLACK)
        collector=RoundedRectangle(width=1.15,height=0.34,corner_radius=0.05,stroke_color=BLACK,stroke_width=1.6,fill_color=WHITE,fill_opacity=1).next_to(drop,DOWN,buff=0.07)
        cnote=self.txt("same water amount -> same time",18,BOLD,color=DARK_GRAY).move_to(instr_panel.get_bottom()+UP*0.40)
        self.play(FadeIn(ramp_panel),FadeIn(instr_panel),run_time=RUN); self.play(Create(ramp),Create(floor),Create(support),FadeIn(ball),run_time=RUN)
        self.play(FadeIn(release),GrowArrow(leader),FadeIn(markers),FadeIn(labels),run_time=RUN); self.play(FadeIn(ramp_caption),run_time=RUN)
        self.play(FadeIn(ptitle),FadeIn(steps),Create(divider),run_time=RUN); self.play(FadeIn(ctitle),FadeIn(tank),FadeIn(water),Create(nozzle),FadeIn(drop),FadeIn(collector),FadeIn(cnote),run_time=RUN)
        self.wait(PAUSE_READ); self.play(MoveAlongPath(ball,Line(end,start)),run_time=2.8,rate_func=rate_functions.ease_in_quad); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_equal_time_pattern_v5(self):
        self.set_header(6,"TIME-POSITION ANALYSIS: WHAT DID THE MEASUREMENTS SHOW?","Equal time steps produce positions 0, 1, 4, 9, 16 and interval distances 1, 3, 5, 7.")
        left=self.panel(6.20,4.85,fill=WHITE).move_to(LEFT*3.65+DOWN*0.12); right=self.panel(6.70,4.85,fill=WHITE).move_to(RIGHT*3.45+DOWN*0.12)
        lt=self.txt("CUMULATIVE POSITION",24,BOLD).next_to(left.get_top(),DOWN,buff=0.24); rt=self.txt("DISTANCE DURING EACH NEXT SECOND",23,BOLD).next_to(right.get_top(),DOWN,buff=0.24)
        headers=VGroup(self.txt("time t (s)",20,BOLD),self.txt("position x",20,BOLD)).arrange(RIGHT,buff=1.05).move_to(left.get_center()+UP*1.40)
        rows=VGroup(*[VGroup(self.txt(str(t),23),self.txt(str(x),23,BOLD)).arrange(RIGHT,buff=2.00) for t,x in zip([0,1,2,3,4],[0,1,4,9,16])]).arrange(DOWN,buff=0.21).move_to(left.get_center()+DOWN*0.25)
        table_rule=Line(left.get_left()+RIGHT*0.40,left.get_right()+LEFT*0.40,color=LIGHT_GRAY,stroke_width=1.4).move_to(left.get_center()+UP*0.92)
        bars=VGroup(); bar_labels=VGroup(); values=[1,3,5,7]; yvals=[1.10,0.25,-0.60,-1.45]; scale=0.40
        for i,(val,y) in enumerate(zip(values,yvals),start=1):
            prefix=self.txt(f"second {i}",20,BOLD).move_to([1.85,y,0])
            bar=Line([3.00,y,0],[3.00+val*scale,y,0],color=BLACK,stroke_width=7)
            value_lab=self.math(fr"\Delta x={val}",27).next_to(bar,RIGHT,buff=0.14)
            bars.add(VGroup(prefix,bar)); bar_labels.add(value_lab)
        pattern=self.formula_panel(r"1,3,5,7\quad\Longrightarrow\quad\text{distance per second is increasing}",width=10.9,height=0.94,size=30).to_edge(DOWN,buff=0.28)
        self.play(FadeIn(left),FadeIn(right),FadeIn(lt),FadeIn(rt),run_time=RUN); self.play(FadeIn(headers),Create(table_rule),run_time=RUN_FAST)
        for row in rows: self.play(FadeIn(row),run_time=0.30)
        for bar,lab in zip(bars,bar_labels): self.play(FadeIn(bar[0]),Create(bar[1]),FadeIn(lab),run_time=0.38)
        self.play(FadeIn(pattern),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def galileo_deduction_v5(self):
        self.set_header(7,"FROM THE DATA TO THE SQUARE-TIME LAW","The position values are square numbers, so the position-time graph is curved rather than linear.")
        left=self.panel(4.55,5.00,fill=WHITE).move_to(LEFT*5.00+DOWN*0.10); lt=self.txt("LOOK AT THE NUMBERS",23,BOLD).next_to(left.get_top(),DOWN,buff=0.23)
        squares=VGroup(self.math(r"1=1^2",40),self.math(r"4=2^2",40),self.math(r"9=3^2",40),self.math(r"16=4^2",40)).arrange(DOWN,buff=0.34).move_to(left.get_center()+DOWN*0.25)
        law=self.formula_panel(r"\boxed{x\propto t^2}",width=4.5,height=1.12,size=50).move_to(LEFT*0.55+UP*1.75)
        explanation=self.txt("doubling time does NOT just double position",20,BOLD,color=DARK_GRAY).move_to(LEFT*0.55+UP*0.85)
        graph_box=self.panel(6.15,5.00,fill=WHITE).move_to(RIGHT*4.35+DOWN*0.10); gt=self.txt("POSITION vs TIME",23,BOLD).next_to(graph_box.get_top(),DOWN,buff=0.22)
        axes=Axes(x_range=[0,4.4,1],y_range=[0,17,4],x_length=4.65,y_length=3.35,axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(graph_box.get_center()+DOWN*0.18)
        curve=axes.plot(lambda t:t**2,x_range=[0,4],color=BLACK,stroke_width=4); ax_labs=VGroup(self.txt("t",18).next_to(axes.x_axis,DOWN,buff=0.08),self.txt("x",18).next_to(axes.y_axis,LEFT,buff=0.10))
        steep=self.txt("curve gets steeper",19,BOLD,color=DARK_GRAY).move_to(graph_box.get_bottom()+UP*0.35)
        contrast=self.formula_panel(r"\text{uniform motion: straight line}\qquad\text{Galileo ramp: curve}",width=9.2,height=0.90,size=29).to_edge(DOWN,buff=0.28).shift(LEFT*0.25)
        self.play(FadeIn(left),FadeIn(lt),run_time=RUN); self.play(Write(squares),run_time=RUN); self.play(FadeIn(law),FadeIn(explanation),run_time=RUN)
        self.play(FadeIn(graph_box),FadeIn(gt),Create(axes),FadeIn(ax_labs),run_time=RUN); self.play(Create(curve),FadeIn(steep),run_time=RUN); self.play(FadeIn(contrast),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(8,"INTRODUCTION TO FALLING MOTION","The inclined plane slows the motion; vertical fall shows the same growing-distance pattern much faster.")
        left=self.panel(5.70,5.00,fill=WHITE).move_to(LEFT*4.15+DOWN*0.10); lt=self.txt("EQUAL TIMES -> BIGGER GAPS",23,BOLD).next_to(left.get_top(),DOWN,buff=0.23)
        line_x=-5.00; y0=1.25; k=0.28; ys=[y0-k*(i**2) for i in range(4)]; line=Line([line_x,y0+0.20,0],[line_x,ys[-1]-0.20,0],color=BLACK,stroke_width=3)
        balls=VGroup(); labs=VGroup()
        for i,y in enumerate(ys):
            b=Circle(radius=0.16,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([line_x,y,0]); balls.add(b); labs.add(self.txt(f"t={i}",20,BOLD,color=DARK_GRAY).next_to(b,RIGHT,buff=0.24))
        gap_labels=VGroup(self.txt("1",18,BOLD).move_to([-4.20,(ys[0]+ys[1])/2,0]),self.txt("3",18,BOLD).move_to([-4.20,(ys[1]+ys[2])/2,0]),self.txt("5",18,BOLD).move_to([-4.20,(ys[2]+ys[3])/2,0]))
        left_note=self.txt("successive gaps grow 1 : 3 : 5",21,BOLD,color=DARK_GRAY).move_to(left.get_bottom()+UP*0.42)
        eq1=self.formula_panel(r"\boxed{y=y_i-\frac12gt^2}",width=6.1,height=1.12,size=44).move_to(RIGHT*3.55+UP*1.65); release=self.txt("release from rest",21,BOLD,color=DARK_GRAY).next_to(eq1,UP,buff=0.14)
        eq2=self.formula_panel(r"y=y_i+v_it-\frac12gt^2",width=6.3,height=1.12,size=41).next_to(eq1,DOWN,buff=0.34)
        preview=self.note_panel("PREVIEW ONLY",["The important feature today is the t² term.","The meaning of g and changing velocity comes next."],width=6.35,title_size=24,body_size=20).move_to(RIGHT*3.55+DOWN*1.80)
        self.play(FadeIn(left),FadeIn(lt),Create(line),run_time=RUN)
        for b,lab in zip(balls,labs): self.play(FadeIn(b),FadeIn(lab),run_time=0.34)
        self.play(FadeIn(gap_labels),FadeIn(left_note),run_time=RUN); self.play(FadeIn(release),FadeIn(eq1),FadeIn(eq2),run_time=RUN); self.play(FadeIn(preview),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def summary_v5(self):
        self.set_header(9,"FINAL MAP: TWO MOTION PATTERNS","Use the measurements and graph shape to decide whether position changes linearly with time or follows a square-time pattern.")
        left=self.panel(6.40,4.55,fill=WHITE).move_to(LEFT*3.55+DOWN*0.15); right=self.panel(6.40,4.55,fill=WHITE).move_to(RIGHT*3.55+DOWN*0.15)
        lt=self.txt("UNIFORM MOTION",27,BOLD).next_to(left.get_top(),DOWN,buff=0.28); rt=self.txt("GALILEO RAMP / FALL PREVIEW",25,BOLD).next_to(right.get_top(),DOWN,buff=0.28)
        lbody=VGroup(self.txt("equal times -> equal distances",22,BOLD),self.txt("x-t graph -> straight line",22),self.txt("v-t graph -> horizontal line",22),self.math(r"\boxed{x=x_i+vt}",40)).arrange(DOWN,buff=0.31).move_to(left.get_center()+DOWN*0.20)
        rbody=VGroup(self.txt("equal times -> increasing distances",22,BOLD),self.txt("positions -> 0, 1, 4, 9, 16",22),self.txt("x-t graph -> curved",22),self.math(r"\boxed{x\propto t^2}",40)).arrange(DOWN,buff=0.31).move_to(right.get_center()+DOWN*0.20)
        final=self.formula_panel(r"\boxed{\text{straight line in time}\quad\neq\quad\text{square-time curve}}",width=10.2,height=1.00,size=33).to_edge(DOWN,buff=0.26)
        self.play(FadeIn(left),FadeIn(right),FadeIn(lt),FadeIn(rt),run_time=RUN); self.play(FadeIn(lbody),FadeIn(rbody),run_time=RUN); self.play(FadeIn(final),run_time=RUN); self.wait(4.4)


# Preview:
# manim -pql Physics9_UniformMotion_Galileo_V5_3_TOTAL_QA.py Physics9UniformMotionGalileoV53TotalQA --disable_caching
# Final:
# manim -pqh Physics9_UniformMotion_Galileo_V5_3_TOTAL_QA.py Physics9UniformMotionGalileoV53TotalQA --disable_caching
