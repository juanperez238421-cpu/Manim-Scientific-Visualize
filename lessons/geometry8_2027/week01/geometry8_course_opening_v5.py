#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEOMETRY 8 · 2027 · V5 CINEMATIC YEAR-OPENING · ACTUAL IJR CURRICULUM.

The user wanted an impressive course opener, NOT the Week01 Class02 Venn lesson.
This video intentionally includes no Venn diagram and no decorative random
triangles/squares. Shapes are genuine constructions, similarity relations,
Pythagorean squares, composite-area partitions and true 3D Platonic solids.

Source: Instituto Jorge Robledo "malla curricular - geometría 8° (2026)(1).docx"
 P1: geometric objects; line/plane; ruler and compass; angle classifications,
     addition, parallel/perpendicular/transversal angles; sets are retained in
     the course syllabus but not foregrounded in this cinematic opening.
 P2: triangles, notable lines; circle; congruence/similarity; Thales; Pythagoras.
 P3: plane perimeter/area; shaded regions; volumes and surface area of solids.
The 2027 class planner confirms Week01 induction only, so these scenes are
PREVIEWS of future content, not unauthorized teaching of later 2027 lessons.

Uses exact same real original IJR PNG, CAD-HOUSE institutional title,
white backdrop, technical TeX type, numbered HUD, blue/green/gray grammar,
and classroom pauses as the successful Geometry8 V4.
The previous Class02 (sets and logical diagrams) remains a separate video.

ManimCE v0.20.1:
manim -pql lessons/geometry8_2027/week01/geometry8_course_opening_v5.py Geometry8_YearOpeningV5
manim -pqh lessons/geometry8_2027/week01/geometry8_course_opening_v5.py Geometry8_YearOpeningV5 --fps 30
"""
from __future__ import annotations

import numpy as np
from manim import *
from geometry8_week01_cad_v4_period1 import Geometry8W01_Period1RoadmapV4
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, TERRAIN, SLAB


class Geometry8_YearOpeningV5(Geometry8W01_Period1RoadmapV4):
    COVER_TITLE = "GEOMETRY IN MOTION -- FROM 2D TO 3D"
    LESSON_LABEL = "THE MATHEMATICS WE WILL EXPLORE THIS YEAR"
    HUD_TITLE = "GEOMETRY 8 -- 2027 -- THE YEAR AHEAD"
    HUD_SUBTITLE = "A cinematic preview of the three curriculum periods"
    READING_PAUSE = 2.35
    MICRO_PAUSE = .68

    def construct(self):
        self._phase_number = 0
        self.institutional_cover()
        self.ph = self.fixed_hud()
        self.year_map()                # same approved V4 CAD timeline
        self.geometric_foundations()   # P1: point, line, plane as related objects
        self.plane_preview()           # P1: authentic finite representation of ideal plane
        self.compass_construction()    # P1: two equal-radius arcs => exact bisector
        self.angle_transformations()   # P1: ray rotation; angle types
        self.parallel_transversal()    # P1: equal corresponding angles
        self.triangle_geometry()       # P2: classification and altitude
        self.thales_similarity()       # P2: parallel cut and scaling ratio
        self.circle_geometry()         # P2: radius/diameter/chord/arc
        self.pythagoras()              # P2: actual squares of 3, 4 and 5
        self.area_recomposition()      # P3: trapezoid decomposition
        self.shaded_area()             # P3: annulus = outer minus inner area
        self.platonic_solids_3d()      # P3: true 3D cube and tetrahedron rotations
        self.closing_roadmap()
        self.footer_cleanup()

    def txt(self,text,x,y,size=30,color=DARK,width=11.8,bold=False):
        """Fit technical labels safely within the full-HD CAD content frame."""
        return self.big_text(text,x,y,size,color,width,bold)

    def formula(self,latex,x,y,size=50,color=POSITIVE,width=7.8):
        return self.big_math(latex,x,y,size,color,width)

    def line(self,p,q,color=SKETCH,width=4.5):
        return Line(p,q,color=color,stroke_width=width)

    def geometric_foundations(self):
        self.heading(0,"P1 / GEOMETRIC LANGUAGE",
            "ONE POINT CAN BEGIN AN ENTIRE CONSTRUCTION",
            "Location, direction, length and a plane are different geometric ideas.")
        start=np.array([-4.55,-.52,0])
        end=np.array([3.80,-.52,0])
        point=Dot(start,radius=.16,color=SKETCH)
        guide=DashedLine(start,end,color=LIGHT,stroke_width=2.4,dash_length=.19)
        self.draw_stage(guide,runtime=.90)
        self.play(FadeIn(point),run_time=.46)
        self.register(point)
        self.play(point.animate.move_to(end),run_time=3.1,rate_func=smooth)
        seg=self.line(start,end,SKETCH,4.9)
        self.draw_stage(seg,runtime=1.6)
        A=Dot(start,radius=.13,color=DARK)
        B=Dot(end,radius=.13,color=DARK)
        self.play(FadeIn(A),FadeIn(B),run_time=.52);self.register(A,B)
        title=self.txt("TWO ENDPOINTS DEFINE A SEGMENT",0,.62,33,DARK,10.8,True)
        self.appearance(title,time=1.25)
        self.wait(1.4)
        arrows=DoubleArrow([-5.30,-.52,0],[5.32,-.52,0],
                           buff=0,color=POSITIVE,stroke_width=4.0,
                           max_tip_length_to_length_ratio=.06)
        self.play(Transform(seg,arrows),run_time=2.1)
        self.appearance(self.txt("A LINE EXTENDS IN BOTH DIRECTIONS",
                                 0,-1.43,31,POSITIVE,11.8,True),time=1.0)
        self.caption("Geometric symbols communicate infinite lines and finite segments.")
        self.wait(2.4)

    def plane_preview(self):
        self.heading(0,"P1 / GEOMETRY OF PLANES",
            "A PLANE EXTENDS IN TWO DIMENSIONS",
            "A finite drawing can represent part of an infinite flat plane.")
        plane=Polygon([-4.82,-1.62,0],[3.50,-1.62,0],
                      [4.66,.87,0],[-3.67,.87,0],
                      stroke_color=SKETCH,stroke_width=3.6,
                      fill_color=MODEL,fill_opacity=.34)
        self.draw_stage(plane,runtime=1.75)
        cross=self.line([-3.70,-.56,0],[3.31,-.56,0],POSITIVE,4.6)
        self.draw_stage(cross,runtime=1.34)
        p=Dot([-1.26,-.56,0],radius=.14,color=DARK)
        self.play(FadeIn(p),run_time=.50);self.register(p)
        name=self.txt("PLANE",4.54,-1.36,29,SKETCH,2.65,True)
        self.appearance(name,time=.84)
        self.caption("Points and lines can lie in a plane; the drawn edges are only symbols.")
        self.wait(2.7)

    def compass_construction(self):
        self.heading(0,"P1 / RULER AND COMPASS",
            "A CONSTRUCTION IS A SEQUENCE OF REASONS",
            "Equal distances reveal the perpendicular bisector of a segment.")
        cy=-.54
        A=np.array([-1.35,cy,0]);B=np.array([1.35,cy,0]);R=1.80
        h=np.sqrt(R**2-1.35**2)
        baseline=self.line(A,B,DARK,4.9)
        left=Dot(A,radius=.13,color=SKETCH)
        right=Dot(B,radius=.13,color=SKETCH)
        self.draw_stage(baseline,runtime=.92)
        self.play(FadeIn(left),FadeIn(right),run_time=.5)
        self.register(left,right)
        radius=ValueTracker(.001)
        c1=always_redraw(lambda: Arc(radius=R,start_angle=-PI/2,
                    angle=max(.001,radius.get_value()),arc_center=A,
                    color=SKETCH,stroke_width=3.7))
        self.add(c1);self.register(c1)
        self.play(radius.animate.set_value(TAU),run_time=3.05,rate_func=linear)
        radius2=ValueTracker(.001)
        c2=always_redraw(lambda: Arc(radius=R,start_angle=-PI/2,
                    angle=max(.001,radius2.get_value()),arc_center=B,
                    color=POSITIVE,stroke_width=3.7))
        self.add(c2);self.register(c2)
        self.play(radius2.animate.set_value(TAU),run_time=3.0,rate_func=linear)
        top=Dot([0,cy+h,0],color=DARK,radius=.14)
        bottom=Dot([0,cy-h,0],color=DARK,radius=.14)
        perp=DashedLine([0,cy-h-.24,0],[0,cy+h+.24,0],
                        color=DARK,stroke_width=4,dash_length=.18)
        self.play(FadeIn(top),FadeIn(bottom),run_time=.6)
        self.register(top,bottom)
        self.draw_stage(perp,runtime=1.5)
        note=self.txt("EQUAL-RADIUS ARCS LOCATE THE BISECTOR",
                      0,-2.19,28,DARK,12.6)
        self.appearance(note,time=1.0)
        self.caption("This previews exact constructions with an unmarked ruler and a compass.")
        self.wait(3.0)

    def angle_transformations(self):
        self.heading(0,"P1 / ANGLES",
            "ANGLES ARE MEASURES OF ROTATION",
            "The same two rays can define acute, right, obtuse and straight angles.")
        O=np.array([-2.90,-1.02,0]);r=2.16
        theta=ValueTracker(32*DEGREES)
        base=Arrow(O,O+RIGHT*r,buff=0,color=DARK,stroke_width=4.8)
        mobile=always_redraw(lambda:Arrow(
                O,O+r*np.array([np.cos(theta.get_value()),
                                 np.sin(theta.get_value()),0]),
                buff=0,color=SKETCH,stroke_width=4.9))
        arc=always_redraw(lambda:Arc(
                radius=.76,start_angle=0,
                angle=max(.001,theta.get_value()),arc_center=O,
                color=POSITIVE,stroke_width=4.1))
        self.draw_stage(base,runtime=1.0)
        self.add(mobile,arc);self.register(mobile,arc)
        vertex=Dot(O,radius=.13,color=DARK)
        self.play(FadeIn(vertex),run_time=.3);self.register(vertex)
        old=self.txt("ACUTE: 32 DEGREES",3.00,-.19,34,SKETCH,6.35,True)
        self.appearance(old,time=.9)
        for degrees,label in ((90,"RIGHT: 90 DEGREES"),(128,"OBTUSE: 128 DEGREES"),
                              (180,"STRAIGHT: 180 DEGREES")):
            new=self.txt(label,3.0,-.19,34,SKETCH,6.35,True)
            self.play(theta.animate.set_value(degrees*DEGREES),
                      ReplacementTransform(old,new),
                      run_time=2.3,rate_func=smooth)
            old=new
            self.wait(.75)
        self.caption("Angle measurement and the addition postulate connect these rotations.")
        self.wait(2.3)

    def parallel_transversal(self):
        self.heading(0,"P1 / PARALLELS AND TRANSVERSALS",
            "WHY ARE SOME ANGLES ALWAYS EQUAL?",
            "A transversal crossing parallel lines preserves corresponding angles.")
        y1=.62;y2=-.98;xu=-1.28
        xl=xu+(y2-y1)/np.sqrt(3)
        upper=self.line([-5.25,y1,0],[2.22,y1,0],DARK,4.4)
        lower=self.line([-5.25,y2,0],[2.22,y2,0],DARK,4.4)
        line=self.line([xu+(-2.18-y1)/np.sqrt(3),-2.18,0],
                       [xu+(1.22-y1)/np.sqrt(3),1.22,0],SKETCH,4.9)
        self.draw_stage(upper,lower,runtime=1.4)
        self.draw_stage(line,runtime=1.35)
        arcs=[
            Arc(radius=.63,start_angle=0,angle=PI/3,
                arc_center=[xu,y1,0],color=POSITIVE,stroke_width=4),
            Arc(radius=.63,start_angle=0,angle=PI/3,
                arc_center=[xl,y2,0],color=POSITIVE,stroke_width=4)
        ]
        self.draw_stage(*arcs,runtime=1.3)
        one=self.formula(r"\alpha=60^\circ",3.82,.42,44,POSITIVE,4.6)
        two=self.formula(r"\beta=60^\circ",3.82,-.72,44,POSITIVE,4.6)
        self.appearance(one,time=.9)
        self.appearance(two,time=.9)
        self.play(*[Indicate(a,scale_factor=1.15) for a in arcs],run_time=2.0)
        self.caption("Equal corresponding angles depend on the parallel-line hypothesis.")
        self.wait(2.8)

    def triangle_geometry(self):
        self.heading(0,"P2 / TRIANGLES",
            "A TRIANGLE CONTAINS MORE THAN THREE SIDES",
            "Classification, altitudes and notable lines reveal its structure.")
        P=np.array([-3.65,-1.45,0])
        Q=np.array([.52,-1.45,0])
        R=np.array([-2.10,1.05,0])
        tri=Polygon(P,Q,R,stroke_color=SKETCH,stroke_width=5,
                    fill_color=MODEL,fill_opacity=.12)
        self.draw_stage(tri,runtime=2.0)
        foot=np.array([R[0],P[1],0])
        altitude=DashedLine(R,foot,color=POSITIVE,
                            dash_length=.15,stroke_width=4.1)
        marker=Square(side_length=.24,stroke_color=POSITIVE,
                      stroke_width=2.5).move_to(foot+[.12,.12,0])
        self.draw_stage(altitude,marker,runtime=1.55)
        centroid=(P+Q+R)/3
        median=self.line(R,(P+Q)/2, DARK,2.2)
        self.draw_stage(median,runtime=1.45)
        G=Dot(centroid,radius=.11,color=DARK)
        self.play(FadeIn(G),run_time=.35);self.register(G)
        self.appearance(self.txt("ALTITUDE",3.40,.42,35,POSITIVE,4.7,True),time=.8)
        self.appearance(self.txt("MEDIAN",3.40,-.42,35,SKETCH,4.7,True),time=.8)
        self.caption("Notable lines lead to geometric centers and triangle relationships.")
        self.wait(3.4)

    def thales_similarity(self):
        self.heading(0,"P2 / SIMILARITY AND THALES",
            "THE SAME SHAPE AT DIFFERENT SCALES",
            "A line parallel to one side creates a smaller similar triangle.")
        C=np.array([-3.60,1.10,0])
        A=np.array([-4.10,-1.58,0])
        B=np.array([.85,-1.58,0])
        triangle=Polygon(C,A,B,color=DARK,stroke_width=4.6,
                         fill_color=MODEL,fill_opacity=.10)
        self.draw_stage(triangle,runtime=1.55)
        scale=ValueTracker(.28)
        cut=always_redraw(lambda:Line(
            C+scale.get_value()*(A-C),
            C+scale.get_value()*(B-C),
            color=SKETCH,stroke_width=4.2))
        small=always_redraw(lambda:Polygon(
            C, C+scale.get_value()*(A-C), C+scale.get_value()*(B-C),
            stroke_color=POSITIVE,stroke_width=2.6,
            fill_color=TERRAIN,fill_opacity=.45))
        self.add(small,cut);self.register(small,cut)
        self.play(scale.animate.set_value(.56),run_time=3.05,rate_func=smooth)
        self.play(scale.animate.set_value(.68),run_time=1.5,rate_func=smooth)
        math=self.formula(r"\frac{CP}{CA}=\frac{CQ}{CB}",
                          3.50,.25,48,POSITIVE,5.15)
        self.appearance(math,time=1.2)
        label=self.txt("PARALLEL SIDES",3.47,-.95,30,SKETCH,5.0,True)
        self.appearance(label,time=.9)
        self.caption("Thales' theorem connects parallel lines with proportional segments.")
        self.wait(3.2)

    def circle_geometry(self):
        self.heading(0,"P2 / CIRCLES",
            "ONE CENTER -- MANY GEOMETRIC ELEMENTS",
            "Radius, diameter, chord and arc all belong to the circle.")
        C=np.array([-2.15,-.53,0]);R=1.67
        outline=Circle(radius=R,color=SKETCH,stroke_width=4.4).move_to(C)
        self.draw_stage(outline,runtime=2.0)
        center=Dot(C,radius=.14,color=DARK)
        radius=self.line(C,C+RIGHT*R,POSITIVE,4)
        diameter=self.line(C+LEFT*R,C+RIGHT*R,DARK,2.7)
        angle1=42*DEGREES; angle2=142*DEGREES
        chord=self.line(C+R*np.array([np.cos(angle1),np.sin(angle1),0]),
                        C+R*np.array([np.cos(angle2),np.sin(angle2),0]),
                        SKETCH,4.4)
        arc=Arc(radius=R,start_angle=angle1,angle=angle2-angle1,
                arc_center=C,color=POSITIVE,stroke_width=7)
        self.play(FadeIn(center),run_time=.4);self.register(center)
        self.draw_stage(radius,runtime=1.0)
        self.draw_stage(diameter,runtime=1.1)
        self.draw_stage(chord,runtime=1.1)
        self.draw_stage(arc,runtime=1.2)
        for i,line in enumerate(("RADIUS","DIAMETER","CHORD","ARC")):
            self.appearance(self.txt(line,3.19,1.0-.65*i,30,
                     POSITIVE if i%2==0 else SKETCH,5.3,True),time=.65)
        self.caption("Circle geometry later connects arcs and angles.")
        self.wait(3.3)

    def pythagoras(self):
        self.heading(0,"P2 / PYTHAGOREAN THEOREM",
            "AN EQUATION THAT CAN BE SEEN",
            "The areas on a right triangle's legs add to the area on its hypotenuse.")
        # A right triangle with legs 3 and 4, hypotenuse 5, scaled by .42.
        A=np.array([-2.4,-.67,0])
        B=A+np.array([4*.42,0,0])
        C=A+np.array([0,3*.42,0])
        tri=Polygon(A,B,C,color=DARK,stroke_width=4.5,
                    fill_color=WHITE,fill_opacity=.0)
        self.draw_stage(tri,runtime=1.55)
        AB=B-A;AC=C-A;BC=C-B
        leg4=Polygon(A,B,B+DOWN*4*.42,A+DOWN*4*.42,
                     stroke_color=SKETCH,stroke_width=3.6,
                     fill_color=MODEL,fill_opacity=.55)
        leg3=Polygon(A,C,C+LEFT*3*.42,A+LEFT*3*.42,
                     stroke_color=POSITIVE,stroke_width=3.6,
                     fill_color=TERRAIN,fill_opacity=.60)
        n=np.array([BC[1],-BC[0],0])
        hyp=Polygon(B,C,C+n,B+n,stroke_color=DARK,
                    stroke_width=3.6,fill_color=SLAB,fill_opacity=.42)
        self.draw_stage(leg3,leg4,runtime=1.7)
        self.draw_stage(hyp,runtime=1.7)
        self.play(Indicate(leg3,scale_factor=1.05),
                  Indicate(leg4,scale_factor=1.05),
                  run_time=1.8)
        eq=self.formula(r"3^2+4^2=5^2",3.52,.47,62,POSITIVE,5.3)
        self.appearance(eq,time=1.15)
        self.appearance(self.txt("9 + 16 = 25",3.51,-.59,34,DARK,5.3,True),
                        time=.9)
        self.caption("The Pythagorean relationship holds for all right triangles.")
        self.wait(3.5)

    def area_recomposition(self):
        self.heading(0,"P3 / PLANE AREA",
            "COMPLEX REGIONS CAN BE RECOMPOSED",
            "A trapezoid can be divided into a central rectangle and two triangles.")
        left=-4.50;right=.36;low=-1.38;high=.94
        uleft=-3.42;uright=-.72
        trap=Polygon([left,low,0],[right,low,0],
                     [uright,high,0],[uleft,high,0],
                     color=DARK,stroke_width=4.5,
                     fill_color=MODEL,fill_opacity=.18)
        self.draw_stage(trap,runtime=1.65)
        seg1=self.line([uleft,low,0],[uleft,high,0],SKETCH,3.2)
        seg2=self.line([uright,low,0],[uright,high,0],SKETCH,3.2)
        self.draw_stage(seg1,seg2,runtime=1.1)
        rect=Rectangle(width=uright-uleft,height=high-low,
                       color=SKETCH,stroke_width=0,
                       fill_color=MODEL,fill_opacity=.55)
        rect.move_to([(uleft+uright)/2,(high+low)/2,0])
        lefttri=Polygon([left,low,0],[uleft,low,0],[uleft,high,0],
                        stroke_width=0,fill_color=TERRAIN,fill_opacity=.73)
        righttri=Polygon([uright,high,0],[uright,low,0],[right,low,0],
                         stroke_width=0,fill_color=SLAB,fill_opacity=.55)
        self.play(FadeIn(lefttri),FadeIn(rect),FadeIn(righttri),
                  run_time=1.35)
        self.register(lefttri,rect,righttri)
        self.play(lefttri.animate.shift(LEFT*.37),
                  righttri.animate.shift(RIGHT*.37),
                  run_time=1.55)
        self.wait(.7)
        self.play(lefttri.animate.shift(RIGHT*.37),
                  righttri.animate.shift(LEFT*.37),
                  run_time=1.4)
        eq=self.formula(r"A=\frac{(B+b)h}{2}",3.27,.09,59,POSITIVE,5.3)
        self.appearance(eq,time=1.25)
        self.caption("Perimeter measures the boundary; area measures the interior.")
        self.wait(3.2)

    def shaded_area(self):
        self.heading(0,"P3 / SHADED REGIONS",
            "FIND THE AREA BY SUBTRACTION",
            "The inner disk is removed from the area enclosed by the outer circle.")
        O=np.array([-2.72,-.60,0])
        outer=Circle(radius=1.76,color=DARK,stroke_width=4.5,
                     fill_color=MODEL,fill_opacity=.68).move_to(O)
        inner=Circle(radius=.87,color=SKETCH,stroke_width=3.6,
                     fill_color=WHITE,fill_opacity=1).move_to(O)
        self.draw_stage(outer,runtime=1.55)
        self.play(FadeIn(inner),run_time=1.15);self.register(inner)
        R=self.line(O,O+RIGHT*1.76,POSITIVE,2.8)
        r=self.line(O,O+UP*.87,SKETCH,2.8)
        self.draw_stage(R,r,runtime=1.05)
        eq=self.formula(r"A_{\mathrm{shaded}}=\pi(R^2-r^2)",
                        3.01,-.1,43,POSITIVE,5.9)
        self.appearance(eq,time=1.25)
        self.caption("Shaded areas use decomposition, recomposition or subtraction.")
        self.wait(3.6)

    def _hud_fixed(self,obj):
        self.add_fixed_in_frame_mobjects(obj)
        return obj

    def platonic_solids_3d(self):
        # The original House CAD font/crest/HUD stays screen-fixed.
        self.stage_clear()
        n=self._phase_number;self._phase_number+=1
        self.set_phase(n,"P3 / ACTUAL 3D SOLIDS",SKETCH)
        head=self._hud_fixed(self.txt("FROM FLAT FACES TO THREE-DIMENSIONAL SOLIDS",
                                        0,2.06,37,DARK,12.3,True))
        sub=self._hud_fixed(self.txt("Faces form surfaces; enclosed space defines volume.",
                                       0,1.42,26,MID,12.6))
        self.play(Write(head),Write(sub),run_time=1.38)
        self.move_camera(phi=63*DEGREES,theta=-48*DEGREES,run_time=1.4)
        cube=Cube(side_length=2.33,fill_color=MODEL,fill_opacity=.72)
        cube.set_stroke(color=SKETCH,width=2.7)
        cube.shift(LEFT*.99+DOWN*.24)
        self.play(Create(cube),run_time=2.1);self.register(cube)
        self.play(Rotate(cube,angle=PI*.88,axis=UP,about_point=cube.get_center()),
                  run_time=3.7,rate_func=smooth)
        volume=self._hud_fixed(self.formula(r"V=a^3",3.20,.33,55,POSITIVE,4.8))
        surface=self._hud_fixed(self.formula(r"A_s=6a^2",3.20,-.70,50,SKETCH,4.8))
        self.play(Write(volume),Write(surface),run_time=1.6)
        self.caption("The cube is a Platonic solid: all six faces are congruent squares.")
        self.wait(2.8)
        self.play(FadeOut(volume),FadeOut(surface),run_time=.55)
        for x in (volume,surface):
            self.remove_fixed_in_frame_mobjects(x)
            self.remove(x)
        tetra=Tetrahedron().scale(1.45)
        tetra.set_fill(color=SLAB,opacity=.67)
        tetra.set_stroke(color=SKETCH,width=2.7)
        tetra.move_to(cube.get_center())
        self.play(ReplacementTransform(cube,tetra),run_time=2.0)
        self.register(tetra)
        self.play(Rotate(tetra,angle=PI*1.14,axis=UP,
                         about_point=tetra.get_center()),run_time=3.65,
                  rate_func=smooth)
        self.caption("Platonic solids connect face structure, surface area and volume.")
        self.wait(3.7)
        self.play(FadeOut(tetra),FadeOut(head),FadeOut(sub),run_time=.85)
        self.remove_fixed_in_frame_mobjects(head,sub)
        self.remove(head,sub)
        self.move_camera(phi=0*DEGREES,theta=-90*DEGREES,zoom=1,
                         run_time=1.4)

    def closing_roadmap(self):
        self.stage_clear()
        n=self._phase_number;self._phase_number+=1
        self.set_phase(n,"CONNECT / EXPLORE",POSITIVE)
        heading=self.txt("ONE LANGUAGE -- THREE DIMENSIONS OF THINKING",
                         0,1.45,40,DARK,12.4,True)
        self.appearance(heading,time=1.2)
        for i,(number,theme,color) in enumerate((
            ("I","POINTS, LINES, CONSTRUCTIONS AND ANGLES",SKETCH),
            ("II","TRIANGLES, CIRCLES, SIMILARITY AND THEOREMS",POSITIVE),
            ("III","AREA, SURFACE AND VOLUME",DARK)
        )):
            y=.35-.92*i
            mark=self.txt(number,-4.95,y,39,color,1.2,True)
            text=self.txt(theme,.75,y,30,color,9.8,True)
            self.play(Write(mark),Write(text),run_time=1.0)
            self.wait(.75)
        self.caption("First, we will learn to name and reason about geometric objects.")
        self.wait(5.2)
        self.stage_clear()
