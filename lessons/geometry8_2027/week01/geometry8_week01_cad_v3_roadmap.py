#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEOMETRY 8 · 2027 · WEEK 01 CLASS 01 · V3 FULL-COURSE INTRODUCTION.

AUTHORITATIVE SOURCE BOUNDARIES:
- "malla curricular - geometría 8° (2026).docx" (Instituto Jorge Robledo):
  full THREE-PERIOD thematic syllabus (2026 reference, not 2027 calendar).
- "Geometry_8_2027_P1.docx" (user-uploaded original):
  2027 verified WEEK 1–4 lesson sequence only.
- Periods II/III below are correctly labelled *curriculum overview*, NOT
  validated 2027 week-by-week schedule.

All content from 2027 W1 Class 01 V2 follows the NEW course roadmap;
Class 02 video is intentionally not rebuilt.
Same House Extrusion CAD class base, original IJR PNG, persistent fixed HUD,
semantic blue/green/red, clean white Technical Tex/MathTex notation.

Build with ManimCE v0.20.1:
manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad_v3_roadmap.py Geometry8W01_YearRoadmapV3
manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad_v3_roadmap.py Geometry8W01_YearRoadmapV3 --fps 30
"""
from __future__ import annotations
import numpy as np
from manim import *
from geometry8_week01_cad_v2 import Geometry8W01_FoundationsV2
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, NEGATIVE, TERRAIN, SLAB


class Geometry8W01_YearRoadmapV3(Geometry8W01_FoundationsV2):
    LESSON_LABEL = "CLASS 01 -- THE YEAR AHEAD AND GEOMETRIC OBJECTS"
    COVER_TITLE = "FROM POINTS TO SHAPES AND SOLIDS"

    def construct(self):
        self.institutional_cover()
        self.ph = self.fixed_hud()
        self._in_course_map = True
        self.year_map()
        self.period_one_map()
        self.period_one_motion()
        self.period_two_map()
        self.period_two_motion()
        self.period_three_map()
        self.period_three_motion()
        self.verified_2027_four_weeks()
        self._in_course_map = False
        # The original Week 1 Class 1 V2 teaching material is retained.
        self.course_conventions()
        self.a_point()
        self.line_ray_segment()
        self.plane()
        self.notation()
        self.model_and_counterexample()
        self.practice()
        self.exit_review(
            "A FULL YEAR STARTS WITH CLEAR DEFINITIONS",
            "Today: point, line, ray, segment, plane and precise notation.")

    def heading(self, n, phase, title, subtitle):
        # Continuous numbered sections: roadmap 00–07, lesson content 08–14.
        index = n if getattr(self, "_in_course_map", False) else n + 7
        return self.chapter(index, phase, title, subtitle)

    def draw_stage(self, *objects, runtime=1.4):
        self.register(*objects)
        self.play(*[Create(o) for o in objects], run_time=runtime)

    def show_topic(self, text, x, y, width=7.15, size=31, color=DARK):
        obj = self.big_text(text,x,y,size,color,width,False)
        self.play(Write(obj),run_time=.90)
        self.wait(.28)
        return obj

    def year_map(self):
        self.heading(0,"YEAR / THREE PERIODS","THE JOURNEY THROUGH GEOMETRY",
                     "From geometric language to shapes, measurement and solids.")
        tracks=[
            ("I","FOUNDATIONS","Objects, construction, angles",SKETCH,.69),
            ("II","SHAPES AND RELATIONSHIPS","Triangles, circles, similarity",POSITIVE,-.42),
            ("III","MEASURE AND MODEL","Areas, shaded regions, solids",DARK,-1.53),
        ]
        for idx,(num,title,desc,color,y) in enumerate(tracks):
            start=np.array([-5.28,y-.23,0]);end=np.array([5.25,y-.23,0])
            guide=Line(start,end,color=LIGHT,stroke_width=2.7)
            left=Circle(radius=.32,color=color,stroke_width=3.0,
                        fill_color=WHITE,fill_opacity=1).move_to(start)
            mark=self.big_text(num,start[0],start[1],29,color,.65,True)
            name=self.big_text(title,-2.66,y+.18,37,color,5.6,True)
            sub=self.big_text(desc,1.82,y+.18,28,MID,6.8)
            dot=Dot(start,radius=.12,color=color)
            self.draw_stage(guide,left,runtime=.73)
            self.play(Write(mark),Write(name),Write(sub),run_time=1.12)
            self.play(MoveAlongPath(dot,guide,rate_func=linear),
                      run_time=2.1)
            self.register(dot)
        self.caption("The three periods are taken from the school's 2026 Geometry 8 curriculum.")
        self.watch(4.6)

    def period_one_map(self):
        self.heading(1,"PERIOD I / TOPICS","P1 -- GEOMETRIC FOUNDATIONS",
                     "2026 curriculum preview; 2027 class dates verified for Weeks 1–4.")
        topics=[
           "Basic geometric objects; sets and diagrams",
           "Lines, planes and their relationships",
           "Constructions with straightedge and compass",
           "Angles: elements, measures and types",
           "Angle addition; parallel and perpendicular lines",
           "Transversals; angles between parallel lines",
        ]
        for i,item in enumerate(topics):
            y=.88-.56*i
            self.show_topic(item,-2.32,y,8.0,30)
        # Visual stack shows rotating ray and the parallel/transversal motif.
        c=np.array([4.47,-.54,0])
        theta=ValueTracker(.22)
        ray=always_redraw(lambda:Arrow(
            c,c+1.42*np.array([np.cos(theta.get_value()),
                              np.sin(theta.get_value()),0]),
            buff=0,stroke_width=4.5,color=SKETCH))
        base=Line(c,c+RIGHT*1.42,color=DARK,stroke_width=3.8)
        vertex=Dot(c,radius=.12,color=POSITIVE)
        self.draw_stage(base,runtime=.80)
        self.add(ray,vertex);self.register(ray,vertex)
        self.play(theta.animate.set_value(1.25),run_time=2.35,rate_func=smooth)
        self.play(theta.animate.set_value(.70),run_time=1.65,rate_func=smooth)
        self.caption("Period I builds the vocabulary and tools needed to reason about angles.")
        self.watch(3.6)

    def period_one_motion(self):
        self.heading(2,"PERIOD I / PREVIEW","LINES, SETS AND CONSTRUCTIONS",
                     "The preview illustrates ideas; formal construction comes later.")
        # Two non-identical sets; intersection is physically located in lens.
        ca=Circle(radius=1.52,color=SKETCH,stroke_width=4.5).move_to([-2.48,-.58,0])
        cb=Circle(radius=1.52,color=POSITIVE,stroke_width=4.5).move_to([-.46,-.58,0])
        self.draw_stage(ca,cb,runtime=1.25)
        p=Triangle().scale(.35).set_stroke(SKETCH,width=4.5)
        p.set_fill(SKETCH,opacity=.30).move_to([-5.35,-.64,0])
        self.play(FadeIn(p),run_time=.55)
        self.register(p)
        self.play(p.animate.move_to([-1.47,-.58,0]),run_time=2.75,rate_func=smooth)
        # Two parallel lines, one transverse, all visually meaningful.
        l1=Line([2.00,.40,0],[5.88,.40,0],color=DARK,stroke_width=3.9)
        l2=Line([2.00,-1.18,0],[5.88,-1.18,0],color=DARK,stroke_width=3.9)
        transverse=Line([3.11,1.03,0],[5.06,-1.76,0],color=SKETCH,
                        stroke_width=4.3)
        self.draw_stage(l1,l2,runtime=1.12)
        self.draw_stage(transverse,runtime=1.30)
        angle1=Arc(radius=.42,start_angle=0,
                   angle=np.arctan2(-2.79,1.95)+TAU,
                   arc_center=[3.55,.40,0],color=POSITIVE,stroke_width=3)
        # Arc decorative preview only; avoid numeric angle or equivalence claim.
        self.caption("Sets organize figures; transversals create new angle relationships.")
        self.watch(4.0)

    def period_two_map(self):
        self.heading(3,"PERIOD II / TOPICS","P2 -- SHAPES AND RELATIONSHIPS",
                     "Curriculum overview: triangles and circles reveal useful theorems.")
        topics=[
            "Triangles: types and notable lines",
            "Circles: elements and angles inside circles",
            "Congruence and similarity of triangles",
            "Proportionality and Thales' theorem",
            "Geometric mean and Pythagorean theorem",
        ]
        for i,item in enumerate(topics):
            self.show_topic(item,-2.35,.79-.66*i,8.15,30)
        # Right-hand triangle with correct right angle and moving similarity.
        P=np.array([3.00,-1.65,0]);Q=np.array([5.61,-1.65,0]);R=np.array([3.00,.43,0])
        tri=Polygon(P,Q,R,color=SKETCH,stroke_width=4.7,
                    fill_color=MODEL,fill_opacity=.32)
        right=Square(side_length=.30,color=POSITIVE,
                     stroke_width=2.0).move_to(P+np.array([.15,.15,0]))
        self.draw_stage(tri,right,runtime=1.65)
        small=tri.copy().set_stroke(color=POSITIVE,width=3.5).set_fill(opacity=.05)
        self.play(TransformFromCopy(tri,small),run_time=1.5)
        self.register(small)
        self.play(small.animate.scale(.55,about_point=P),run_time=2.4,
                  rate_func=smooth)
        self.caption("Triangles, circles and proportionality lead toward similarity and Pythagoras.")
        self.watch(3.6)

    def period_two_motion(self):
        self.heading(4,"PERIOD II / PREVIEW","TRIANGLES, CIRCLES AND PYTHAGORAS",
                     "Each diagram represents one topic; we will study it later.")
        center=np.array([-3.38,-.39,0])
        ring=Circle(radius=1.42,color=SKETCH,stroke_width=4.1).move_to(center)
        phase=ValueTracker(.0)
        radius=always_redraw(lambda: Line(
            center,center+1.42*np.array([np.cos(phase.get_value()),
                                        np.sin(phase.get_value()),0]),
            color=POSITIVE,stroke_width=5))
        rim=always_redraw(lambda: Dot(
            center+1.42*np.array([np.cos(phase.get_value()),
                                  np.sin(phase.get_value()),0]),
            radius=.16,color=SKETCH))
        self.draw_stage(ring,runtime=1.15)
        self.add(radius,rim);self.register(radius,rim)
        self.play(phase.animate.set_value(1.65*TAU),
                  run_time=6.0,rate_func=linear)
        # Exact 3–4–5 right triangle with squares as visual proof motif.
        A=np.array([1.10,-1.55,0]); B=np.array([4.30,-1.55,0])
        C=np.array([1.10,.85,0])
        triangle=Polygon(A,B,C,color=DARK,stroke_width=4.5,
                         fill_color=MODEL,fill_opacity=.24)
        self.draw_stage(triangle,runtime=1.6)
        m=self.big_math(r"a^{2}+b^{2}=c^{2}",3.23,-2.02,56,POSITIVE,5.1)
        self.appearance(m,time=1.2)
        self.caption("A rotating radius previews circles; a right triangle previews Pythagoras.")
        self.watch(3.6)

    def period_three_map(self):
        self.heading(5,"PERIOD III / TOPICS","P3 -- MEASUREMENT AND SOLIDS",
                     "Area, perimeter, shaded regions, volume and surface area.")
        topics=[
            "Perimeter and area of plane figures",
            "Simple and composite shaded regions",
            "Volumes of Pythagorean and Platonic solids",
            "Surface area of three-dimensional solids",
        ]
        for i,item in enumerate(topics):
            self.show_topic(item,-2.45,.91-.83*i,7.95,31)
        side=ValueTracker(1.35)
        box=always_redraw(lambda: Square(
            side_length=side.get_value(),color=SKETCH,
            stroke_width=4.5,fill_color=MODEL,fill_opacity=.30)
            .move_to([4.49,-.55,0]))
        self.add(box);self.register(box)
        self.play(side.animate.set_value(2.40),run_time=3.0,rate_func=smooth)
        self.play(side.animate.set_value(1.95),run_time=1.7,rate_func=smooth)
        self.caption("Area changes when side lengths change; solids add a third dimension.")
        self.watch(3.4)

    def period_three_motion(self):
        self.heading(6,"PERIOD III / PREVIEW","COMPOSITE AREAS AND SOLID MODELS",
                     "Split complex regions into simpler parts; model the faces of solids.")
        base=Rectangle(width=4.15,height=2.23,color=SKETCH,
                       stroke_width=4.1,fill_color=MODEL,
                       fill_opacity=.28).move_to([-3.13,-.43,0])
        split=Line([-3.68,-1.55,0],[-3.68,.69,0],color=POSITIVE,
                   stroke_width=4.0)
        shade=Rectangle(width=1.55,height=2.10,stroke_width=0,
                        fill_color=POSITIVE,fill_opacity=.28).move_to([-4.36,-.43,0])
        self.draw_stage(base,runtime=1.1)
        self.play(FadeIn(shade),Create(split),run_time=1.5)
        self.register(shade,split)
        self.play(shade.animate.shift(RIGHT*.67),run_time=1.6,rate_func=smooth)
        self.play(shade.animate.shift(LEFT*.67),run_time=1.2,rate_func=smooth)
        # Axonometric faces, an exploded surface view (schematic CAD 2D).
        v=np.array([3.36,-.83,0])
        front=Polygon(v+[-.90,-.50,0],v+[.65,-.50,0],
                      v+[.65,1.07,0],v+[-.90,1.07,0],
                      color=DARK,stroke_width=3.8,
                      fill_color=SLAB,fill_opacity=.65)
        top=Polygon(v+[-.90,1.07,0],v+[.65,1.07,0],
                    v+[1.32,1.67,0],v+[-.22,1.67,0],
                    color=SKETCH,stroke_width=3.5,
                    fill_color=MODEL,fill_opacity=.65)
        side=Polygon(v+[.65,-.50,0],v+[1.32,.12,0],
                     v+[1.32,1.67,0],v+[.65,1.07,0],
                     color=POSITIVE,stroke_width=3.5,
                     fill_color=TERRAIN,fill_opacity=.75)
        self.draw_stage(front,top,side,runtime=1.95)
        self.play(top.animate.shift(UP*.26),
                  side.animate.shift(RIGHT*.51),
                  run_time=2.1,rate_func=smooth)
        self.caption("Area belongs to surfaces; volume describes space within a solid.")
        self.watch(4.5)

    def verified_2027_four_weeks(self):
        self.heading(7,"2027 / VERIFIED WEEKS","THE FIRST FOUR WEEKS OF 2027",
                     "Dates and topics below come directly from the 2027 class planner.")
        rows=[
            ("W01  JAN 19-22","GEOMETRIC OBJECTS + LOGICAL SETS",SKETCH),
            ("W02  JAN 25-29","LINES, PLANES AND RELATIONS",POSITIVE),
            ("W03  FEB 01-05","RULER-AND-COMPASS CONSTRUCTIONS",SKETCH),
            ("W04  FEB 08-12","ANGLE ELEMENTS, TYPES AND MEASUREMENT",POSITIVE),
        ]
        timeline=Line([-5.25,.90,0],[-5.25,-1.96,0],
                      color=LIGHT,stroke_width=3.0)
        self.draw_stage(timeline,runtime=.80)
        for i,(date,topic,color) in enumerate(rows):
            y=.76-i*.87
            dot=Dot([-5.25,y,0],radius=.14,color=color)
            line=Line([-4.95,y,0],[5.70,y,0],
                      color=LIGHT,stroke_width=1.7)
            self.play(FadeIn(dot),Create(line),run_time=.56)
            self.register(dot,line)
            # Reserve separate horizontal zones for dates and topic names:
            # 2.8 Manim units clear gap prevents any printed-text collision.
            a=self.big_text(date,-3.73,y+.20,27,color,2.65,True)
            b=self.big_text(topic,1.82,y+.20,29,DARK,7.35,True)
            self.appearance(a,b,time=.92)
            self.watch(.63)
        self.caption("Later 2027 lesson dates are not specified in the provided planner.")
        self.watch(5.0)
