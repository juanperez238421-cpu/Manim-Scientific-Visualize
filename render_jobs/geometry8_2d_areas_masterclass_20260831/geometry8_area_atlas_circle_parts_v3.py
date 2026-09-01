#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *

class Geometry8AreaCirclePartsMixin:
    """Explicit figure chapters."""

    def semicircle_explicit(self):
        h=self.header(12,"9 · SEMICIRCLE","A diameter divides one circle into two congruent regions, so each has half the circle's area.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-3.70,-.35,0]); radius=1.85
        circle=Circle(radius,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.40).move_to(center)
        diameter=Line(center+LEFT*radius,center+RIGHT*radius,color=INK,stroke_width=4)

        self.mark_stage(strip,0)
        self.play(Create(circle),run_time=.65); self.play(Create(diameter),run_time=.45)
        lower=Sector(arc_center=center,radius=radius,start_angle=PI,angle=PI,stroke_color=INK,stroke_width=4,fill_color=WHITE,fill_opacity=1)
        self.play(FadeIn(lower),run_time=.45)

        self.mark_stage(strip,1)
        rline=Line(center,center+RIGHT*radius,color=INK,stroke_width=3.5)
        rlab=self.eq("r",36).next_to(rline,UP,buff=.07)
        dlab=self.eq("d=2r",34).next_to(diameter,DOWN,buff=.10)
        self.play(Create(rline),FadeIn(rlab),FadeIn(dlab),run_time=.58)

        self.mark_stage(strip,2)
        deriv=VGroup(
            self.eq(r"A_{circle}=\pi r^2",43),
            self.eq(r"A_{semi}=\frac12A_{circle}",43),
            self.box(r"A_{semi}=\frac{\pi r^2}{2}",5.8,56),
        ).arrange(DOWN,buff=.26).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.38); self.wait(.24)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: r = 6 cm",r"A=\frac{\pi r^2}{2}",r"A=\frac{\pi(6)^2}{2}=18\pi",r"A\approx56.55\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def quarter_circle_explicit(self):
        h=self.header(13,"10 · QUARTER CIRCLE (QUADRANT)","Two perpendicular radii isolate one of four congruent quarters of a circle.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-3.85,-1.00,0]); radius=2.05
        circle=Circle(radius,color=INK,stroke_width=4,fill_opacity=0).move_to(center)
        r1=Line(center,center+RIGHT*radius,color=INK,stroke_width=4)
        r2=Line(center,center+UP*radius,color=INK,stroke_width=4)
        quarter=Sector(arc_center=center,radius=radius,start_angle=0,angle=PI/2,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.70)

        self.mark_stage(strip,0)
        self.play(Create(circle),run_time=.58)
        self.play(Create(r1),Create(r2),FadeIn(quarter),run_time=.62)

        self.mark_stage(strip,1)
        labs=VGroup(self.eq("r",35).next_to(r1,DOWN,buff=.06),self.eq("r",35).next_to(r2,LEFT,buff=.06),self.right_mark(center,RIGHT,UP,.28))
        self.play(FadeIn(labs),run_time=.50)

        self.mark_stage(strip,2)
        deriv=VGroup(
            self.eq(r"A_{circle}=\pi r^2",43),
            self.eq(r"A_{quarter}=\frac14A_{circle}",43),
            self.box(r"A_{quarter}=\frac{\pi r^2}{4}",5.9,55),
        ).arrange(DOWN,buff=.26).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.38); self.wait(.24)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: r = 8 cm",r"A=\frac{\pi r^2}{4}",r"A=\frac{\pi(8)^2}{4}=16\pi",r"A\approx50.27\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()
