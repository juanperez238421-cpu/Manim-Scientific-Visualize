#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *

class Geometry8AreaQuadrilateralFiguresMixin:
    """Explicit figure chapters."""

    def parallelogram_explicit(self):
        h=self.header(7,"4 · PARALLELOGRAM","A cut-and-translate preserves area and turns the slanted figure into a rectangle.")
        strip=self.stage_strip(); self.add(h,strip)

        A=np.array([-5.80,-1.35,0]); E=np.array([-4.80,-1.35,0]); B=np.array([-1.40,-1.35,0]); F=np.array([-.40,-1.35,0]); C=np.array([-.40,1.35,0]); D=np.array([-4.80,1.35,0])
        full=Polygon(A,B,C,D,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)

        self.mark_stage(strip,0)
        self.play(Create(full),run_time=.70)

        self.mark_stage(strip,1)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        alt=DashedLine(D,E,color=MID,stroke_width=3)
        dh=self.dimension(E+LEFT*.30,D+LEFT*.30,"h",LEFT)
        slanted=self.txt("slanted side ≠ height",25,True).next_to(Line(A,D),LEFT,buff=.12)
        self.play(GrowFromCenter(db[0]),FadeIn(db[1]),Create(alt),GrowFromCenter(dh[0]),FadeIn(dh[1]),FadeIn(slanted),run_time=.78)

        self.mark_stage(strip,2)
        left_piece=Polygon(A,E,D,stroke_color=INK,stroke_width=4,fill_color=WHITE,fill_opacity=1)
        remain=Polygon(E,B,C,D,stroke_color=INK,stroke_width=4,fill_color=FILL,fill_opacity=.66)
        self.play(FadeOut(full),FadeIn(left_piece),FadeIn(remain),FadeOut(slanted),run_time=.42)
        motion=Arrow(left_piece.get_center()+UP*1.80,left_piece.get_center()+UP*1.80+RIGHT*4.35,buff=.05,color=MID,stroke_width=3)
        self.play(GrowArrow(motion),run_time=.35)
        self.play(left_piece.animate.shift(RIGHT*4.4),run_time=1.10,rate_func=smooth)
        rect=Polygon(E,F,C,D,stroke_color=INK,stroke_width=5,fill_opacity=0)
        self.play(FadeOut(motion),Create(rect),run_time=.45)
        deriv=VGroup(self.txt("Same pieces → same area as a rectangle",27,True),self.box(r"A=b\,h",5.3,62)).arrange(DOWN,buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv),run_time=.55)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: b = 7 cm, h = 4 cm",r"A=b\,h",r"A=(7)(4)",r"A=28\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def trapezoid_explicit(self):
        h=self.header(8,"5 · TRAPEZOID","Two parallel bases, B and b, share one perpendicular height h.")
        strip=self.stage_strip(); self.add(h,strip)

        # Compact left-side construction leaves room for the correctly joined duplicate.
        A=np.array([-6.35,-1.30,0]); Bp=np.array([-3.25,-1.30,0]); C=np.array([-3.85,1.25,0]); D=np.array([-5.55,1.25,0]); foot=np.array([D[0],A[1],0])
        trap=Polygon(A,Bp,C,D,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)

        self.mark_stage(strip,0)
        self.play(Create(Line(A,Bp,color=INK,stroke_width=5)),run_time=.45)
        self.play(Create(Line(Bp,C,color=INK,stroke_width=5)),Create(Line(C,D,color=INK,stroke_width=5)),Create(Line(D,A,color=INK,stroke_width=5)),FadeIn(trap.copy().set_stroke(opacity=0)),run_time=.82)

        self.mark_stage(strip,1)
        dB=self.dimension(A+DOWN*.34,Bp+DOWN*.34,"B",DOWN)
        db=self.dimension(D+UP*.34,C+UP*.34,"b",UP)
        alt=DashedLine(D,foot,color=MID,stroke_width=3)
        dh=self.dimension(foot+LEFT*.28,D+LEFT*.28,"h",LEFT)
        self.play(GrowFromCenter(dB[0]),GrowFromCenter(db[0]),FadeIn(dB[1]),FadeIn(db[1]),Create(alt),GrowFromCenter(dh[0]),FadeIn(dh[1]),FadeIn(self.right_mark(foot)),run_time=.82)

        self.mark_stage(strip,2)
        # A 180° rotation about the midpoint of the right leg makes the duplicate
        # share that leg exactly. The union is a true parallelogram with base B+b.
        copy=trap.copy().set_fill(PAPER,opacity=.90).set_stroke(MID,width=4)
        pivot=(Bp+C)/2
        self.add(copy)
        self.play(Rotate(copy,angle=PI,about_point=pivot),run_time=1.05,rate_func=smooth)
        copy_A=Bp+C-A
        copy_D=Bp+C-D
        para=Polygon(A,copy_D,copy_A,D,stroke_color=INK,stroke_width=4,fill_opacity=0)
        sum_base=self.dimension(A+DOWN*.37,copy_D+DOWN*.37,"B+b",DOWN,34)
        self.play(FadeOut(dB),FadeOut(db),Create(para),GrowFromCenter(sum_base[0]),FadeIn(sum_base[1]),run_time=.58)
        deriv=VGroup(
            self.txt("2 congruent trapezoids → one parallelogram",26,True),
            self.eq(r"2A=(B+b)h",43),
            self.box(r"A=\frac{(B+b)h}{2}",6.1,55),
        ).arrange(DOWN,buff=.22).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.38); self.wait(.24)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),FadeOut(copy),FadeOut(para),FadeOut(sum_base),run_time=.32)
        ex=self.example_stack("Given: B = 10 cm, b = 6 cm, h = 4 cm",r"A=\frac{(B+b)h}{2}",r"A=\frac{(10+6)(4)}{2}",r"A=32\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def rhombus_explicit(self):
        h=self.header(9,"6 · RHOMBUS","The diagonals D and d cross at right angles and divide the rhombus into four triangles.")
        strip=self.stage_strip(); self.add(h,strip)

        L=np.array([-5.60,0,0]); T=np.array([-3.55,1.70,0]); R=np.array([-1.50,0,0]); Bm=np.array([-3.55,-1.70,0]); O=np.array([-3.55,0,0])
        rh=Polygon(L,T,R,Bm,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)

        self.mark_stage(strip,0)
        self.play(Create(rh),run_time=.72)

        self.mark_stage(strip,1)
        Dline=DashedLine(L,R,color=INK,stroke_width=2.8); dline=DashedLine(Bm,T,color=INK,stroke_width=2.8)
        Dlab=self.eq("D",36).next_to(Dline,UP,buff=.06); dlab=self.eq("d",36).next_to(dline,RIGHT,buff=.07)
        self.play(Create(Dline),Create(dline),FadeIn(Dlab),FadeIn(dlab),FadeIn(self.right_mark(O)),run_time=.72)

        self.mark_stage(strip,2)
        triangles=VGroup(
            Polygon(O,T,R,stroke_color=MID,stroke_width=2,fill_color=WHITE,fill_opacity=.25),
            Polygon(O,R,Bm,stroke_color=MID,stroke_width=2,fill_color=PAPER,fill_opacity=.25),
            Polygon(O,Bm,L,stroke_color=MID,stroke_width=2,fill_color=WHITE,fill_opacity=.25),
            Polygon(O,L,T,stroke_color=MID,stroke_width=2,fill_color=PAPER,fill_opacity=.25),
        )
        self.play(LaggedStart(*[FadeIn(t) for t in triangles],lag_ratio=.10),run_time=.65)
        deriv=VGroup(
            self.eq(r"A=4\left[\frac12\left(\frac D2\right)\left(\frac d2\right)\right]",37),
            self.box(r"A=\frac{D\,d}{2}",5.5,60),
        ).arrange(DOWN,buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv[0]),run_time=.45); self.wait(.35); self.play(FadeIn(deriv[1]),run_time=.45)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: D = 12 cm, d = 8 cm",r"A=\frac{D\,d}{2}",r"A=\frac{(12)(8)}{2}",r"A=48\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()
