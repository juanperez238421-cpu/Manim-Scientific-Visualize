#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *

class Geometry8AreaBasicFiguresMixin:
    """Explicit figure chapters."""

    def square_explicit(self):
        h = self.header(4, "1 · SQUARE", "Four equal sides and four right angles; one side length determines the whole area.")
        strip = self.stage_strip(); self.add(h, strip)

        x0, y0, side = -5.35, -1.45, 3.35
        A = np.array([x0, y0, 0]); B = A + RIGHT * side
        C = B + UP * side; D = A + UP * side
        edges = [Line(A, B, color=INK, stroke_width=5), Line(B, C, color=INK, stroke_width=5), Line(C, D, color=INK, stroke_width=5), Line(D, A, color=INK, stroke_width=5)]
        fill = Polygon(A, B, C, D, stroke_opacity=0, fill_color=FILL, fill_opacity=.66)

        self.mark_stage(strip, 0)
        self.play(Create(edges[0]), run_time=.55)
        self.play(Create(edges[1]), Create(edges[2]), Create(edges[3]), run_time=.85)
        self.play(FadeIn(fill), run_time=.35)

        self.mark_stage(strip, 1)
        bottom = self.dimension(A + DOWN*.35, B + DOWN*.35, "s", DOWN)
        left = self.dimension(A + LEFT*.35, D + LEFT*.35, "s", LEFT)
        marks = VGroup(*[
            Line(e.get_center()+UP*.10, e.get_center()+DOWN*.10, color=INK, stroke_width=2.1).rotate(e.get_angle())
            for e in edges
        ])
        ra = self.right_mark(A, RIGHT, UP)
        self.play(GrowFromCenter(bottom[0]), GrowFromCenter(left[0]), FadeIn(bottom[1]), FadeIn(left[1]), FadeIn(ra), FadeIn(marks), run_time=.70)

        self.mark_stage(strip, 2)
        deriv = VGroup(
            self.txt("A square is a rectangle with b = h = s.", 28, True),
            self.eq(r"A=b\,h", 45),
            self.eq(r"A=s\cdot s", 45),
            self.box(r"A=s^2", 5.2, 62),
        ).arrange(DOWN, buff=.23).move_to(RIGHT*3.55 + UP*.10)
        for item in deriv:
            self.play(FadeIn(item, shift=UP*.03), run_time=.38); self.wait(.25)

        self.mark_stage(strip, 3)
        self.play(FadeOut(deriv), run_time=.35)
        ex = self.example_stack("Given: s = 5 cm", r"A=s^2", r"A=(5)^2", r"A=25\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80)
        self.wipe()

    def rectangle_explicit(self):
        h = self.header(5, "2 · RECTANGLE", "Opposite sides are equal; base and perpendicular height count columns and rows.")
        strip = self.stage_strip(); self.add(h, strip)

        A=np.array([-5.65,-1.20,0]); B=np.array([-1.15,-1.20,0]); C=np.array([-1.15,1.25,0]); D=np.array([-5.65,1.25,0])
        base=Line(A,B,color=INK,stroke_width=5); side=Line(B,C,color=INK,stroke_width=5); top=Line(C,D,color=INK,stroke_width=5); left=Line(D,A,color=INK,stroke_width=5)
        fill=Polygon(A,B,C,D,stroke_opacity=0,fill_color=FILL,fill_opacity=.62)

        self.mark_stage(strip,0)
        self.play(Create(base), run_time=.55)
        self.play(Create(side), Create(top), Create(left), run_time=.80)
        self.play(FadeIn(fill), run_time=.35)

        self.mark_stage(strip,1)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        dh=self.dimension(B+RIGHT*.35,C+RIGHT*.35,"h",RIGHT)
        right=VGroup(self.right_mark(A),self.right_mark(B,LEFT,UP),self.right_mark(C,LEFT,DOWN),self.right_mark(D,RIGHT,DOWN))
        self.play(GrowFromCenter(db[0]),GrowFromCenter(dh[0]),FadeIn(db[1]),FadeIn(dh[1]),FadeIn(right),run_time=.70)

        self.mark_stage(strip,2)
        deriv=VGroup(
            self.txt("b unit columns repeated through h unit rows",28,True),
            self.eq(r"A=\underbrace{b+b+\cdots+b}_{h\ \text{rows}}",40),
            self.box(r"A=b\,h",5.3,62),
        ).arrange(DOWN,buff=.30).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.42); self.wait(.30)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.35)
        ex=self.example_stack("Given: b = 8 cm, h = 3 cm",r"A=b\,h",r"A=(8)(3)",r"A=24\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def triangle_explicit(self):
        h=self.header(6,"3 · TRIANGLE","The height is the perpendicular distance from a vertex to the chosen base.")
        strip=self.stage_strip(); self.add(h,strip)

        A=np.array([-5.55,-1.45,0]); B=np.array([-1.15,-1.45,0]); C=np.array([-4.00,1.40,0]); foot=np.array([C[0],A[1],0])
        tri=Polygon(A,B,C,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.68)

        self.mark_stage(strip,0)
        self.play(Create(Line(A,B,color=INK,stroke_width=5)),run_time=.50)
        self.play(Create(Line(B,C,color=INK,stroke_width=5)),Create(Line(C,A,color=INK,stroke_width=5)),FadeIn(tri.copy().set_stroke(opacity=0)),run_time=.80)

        self.mark_stage(strip,1)
        altitude=DashedLine(C,foot,color=MID,stroke_width=3)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        dh=self.dimension(foot+RIGHT*.28,C+RIGHT*.28,"h",RIGHT)
        ra=self.right_mark(foot,RIGHT,UP,.24)
        self.play(Create(altitude),GrowFromCenter(db[0]),GrowFromCenter(dh[0]),FadeIn(db[1]),FadeIn(dh[1]),FadeIn(ra),run_time=.75)

        self.mark_stage(strip,2)
        copy=tri.copy().set_fill(PAPER,opacity=.90).set_stroke(MID,width=4)
        midpoint=(B+C)/2
        self.add(copy)
        self.play(Rotate(copy,angle=PI,about_point=midpoint),run_time=1.15,rate_func=smooth)
        para=Polygon(A,B,B+C-A,C,stroke_color=INK,stroke_width=4,fill_opacity=0)
        self.play(Create(para),run_time=.45)
        deriv=VGroup(self.eq(r"2A_{\triangle}=b\,h",45),self.box(r"A_{\triangle}=\frac{b\,h}{2}",5.8,58)).arrange(DOWN,buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv[0]),run_time=.40); self.wait(.35); self.play(FadeIn(deriv[1]),run_time=.45)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),FadeOut(copy),FadeOut(para),run_time=.35)
        ex=self.example_stack("Given: b = 10 cm, h = 6 cm",r"A=\frac{b\,h}{2}",r"A=\frac{(10)(6)}{2}",r"A=30\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()
