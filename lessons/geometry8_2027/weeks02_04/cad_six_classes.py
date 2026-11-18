#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 • 2027 Q1 • Weeks 02, 03, 04 • SIX complete CAD House lessons.

Source: original uploaded Geometry_8_2027_P1.docx class planner (2027),
rechecked against IJR malla curricular - geometría 8° (2026), Period I.
Six source-specific lessons, in documented two-class order each week.
No claim of particular group/day within weekly date window.

Render with ManimCE v0.20.1:
  manim -pql lessons/geometry8_2027/weeks02_04/cad_six_classes.py <SceneName>
  manim -pqh lessons/geometry8_2027/weeks02_04/cad_six_classes.py <SceneName> --fps 30

The accepted authentic institutional crest, white technical diagram language,
fixed numbered CAD HUD, annotation panel, blue sketches and green verified
relationships are exactly inherited from the Week01 V2 CAD lesson base.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "week01"))
from geometry8_week01_cad_v2 import Geometry8V2Base
from physics9_week01_cad import DARK,MID,LIGHT,MODEL,SKETCH,POSITIVE,NEGATIVE,TERRAIN,SLAB

class CADGeometry8(Geometry8V2Base):
    """Shared real PNG cover, safe CAD HUD and consistent teaching gestures."""
    WEEK=2
    DATES="JANUARY 25--29, 2027"
    COVER_TITLE="GEOMETRIC RELATIONSHIPS"
    LESSON_LABEL="CLASS 01"
    HUD_SUBTITLE="Lines, planes, and spatial relationships"
    FINAL_OBSERVATION_PAUSE=4.0
    MICRO_PAUSE=.65

    def institutional_cover(self):
        if not self.LOGO.exists(): raise FileNotFoundError(self.LOGO)
        crest=ImageMobject(str(self.LOGO)).scale_to_fit_height(2.19).to_edge(UP,buff=.32)
        items=[
           self.text(self.INSTITUTION,27,BOLD,DARK),
           self.text("GEOMETRY 8",52,BOLD,DARK),
           self.text(f"2027 -- QUARTER 1 -- WEEK {self.WEEK:02d}",27,BOLD,SKETCH),
           self.text(self.DATES,24,BOLD,POSITIVE),
           Line(LEFT*5.3,RIGHT*5.3,color=SKETCH,stroke_width=2.1),
           self.text(self.COVER_TITLE,30,BOLD,DARK),
           self.text(self.LESSON_LABEL,25,BOLD,POSITIVE),
           Line(LEFT*4.5,RIGHT*4.5,color=LIGHT,stroke_width=1.4),
           self.text(f"Teacher: {self.TEACHER}",23,NORMAL,MID),
        ]
        stack=VGroup(*items).arrange(DOWN,buff=.14).next_to(crest,DOWN,buff=.07)
        if stack.height>4.75: stack.scale_to_fit_height(4.75).next_to(crest,DOWN,buff=.07)
        self.play(FadeIn(crest),Write(items[0]),run_time=1.0)
        self.play(*[Write(m) if isinstance(m,Tex) else Create(m) for m in items[1:]],run_time=2.25)
        self.wait(3.2)
        self.play(FadeOut(crest),FadeOut(stack),run_time=.7)

    def t(self,s,x=0,y=0,z=34,color=DARK,w=12.3,bold=False):
        obj=self.big_text(s,x,y,z,color,w,bold)
        return obj

    def formula(self,s,x=0,y=0,z=47,color=POSITIVE,w=11.8):
        return self.big_math(s,x,y,z,color,w)

    def show(self,*m,run=1.0):
        self.play(*[FadeIn(a) for a in m],run_time=run)
        self.register(*m)

    def trace(self,*m,run=1.5):
        self.play(*[Create(a) for a in m],run_time=run)
        self.register(*m)

    def panel(self,n,tag,title,subtitle):
        self.chapter(n,tag,title,subtitle)

    def quiz(self,questions,answers):
        self.stage_clear()
        self.panel(8,"CHECK / REASON","PAUSE AND CLASSIFY",
                   "Discuss, sketch, and give a reason for every answer.")
        for i,q in enumerate(questions):
            x=self.t(q,0,.94-i*.91,30,DARK,12.4)
            self.appearance(x,time=.85)
        self.caption("Pause the video and compare reasoning with a partner.")
        self.wait(8)
        self.stage_clear()
        self.panel(9,"VERIFY / EXPLAIN","MODEL RESPONSES",
                   "Every response should refer to a geometric property.")
        for i,a in enumerate(answers):
            x=self.t(a,0,.94-i*.90,31,POSITIVE,12.5,True)
            self.appearance(x,time=.86)
        self.caption("Check your diagram, labels and justification.")
        self.wait(5.0)

    def run_lesson(self,sections,questions,answers):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        for s in sections: s()
        self.quiz(questions,answers)
        self.stage_clear()
        self.footer_cleanup()

    def axes_lines(self,kind):
        """Large exact examples: parallel, intersecting, perpendicular, coincident."""
        y=.04
        if kind=="parallel":
            return VGroup(
                Line([-4.5,y+.70,0],[4.5,y+.70,0],color=SKETCH,stroke_width=5),
                Line([-4.5,y-.70,0],[4.5,y-.70,0],color=POSITIVE,stroke_width=5))
        if kind=="perpendicular":
            a=Line([-4.4,y-.54,0],[4.4,y-.54,0],color=SKETCH,stroke_width=5)
            b=Line([.15,-2.18,0],[.15,1.62,0],color=POSITIVE,stroke_width=5)
            marker=Square(side_length=.40,color=POSITIVE,stroke_width=3).move_to([.35,y-.34,0])
            return VGroup(a,b,marker)
        if kind=="intersect":
            return VGroup(Line([-4,-1.18,0],[4,1.20,0],color=SKETCH,stroke_width=5),
                          Line([-4,1.20,0],[4,-1.18,0],color=POSITIVE,stroke_width=5))
        return VGroup(Line([-4.4,y,0],[4.4,y,0],color=SKETCH,stroke_width=8),
                      Line([-4.4,y,0],[4.4,y,0],color=POSITIVE,stroke_width=3))

class Geometry8W02_Class01(CADGeometry8):
    WEEK=2;DATES="JANUARY 25--29, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 02"
    HUD_SUBTITLE="Line and plane relations / January 25--29"
    COVER_TITLE="LINES, PLANES, AND RELATIONSHIPS"
    LESSON_LABEL="CLASS 01 -- OBSERVE AND LABEL"

    def construct(self):
        self.run_lesson([self.classroom,self.four_cases,self.plane],
            ["1. Can two different parallel lines meet?",
             "2. What angle do perpendicular lines form?",
             "3. Is a drawn plane boundary a true edge?"],
            ["1. NO -- DIFFERENT PARALLELS NEVER INTERSECT.",
             "2. A RIGHT ANGLE, 90 DEGREES.",
             "3. NO -- THE PLANE EXTENDS INFINITELY."])

    def classroom(self):
        self.panel(1,"OBSERVE / REAL WORLD","GEOMETRY IN A CLASSROOM",
                   "Notebook edges, floor tiles and walls are models of ideal geometry.")
        room=Rectangle(width=7.5,height=3.3,color=DARK,stroke_width=4).move_to([-1.3,-.25,0])
        v=Line([-1.5,-1.9,0],[-1.5,1.35,0],color=SKETCH,stroke_width=5)
        h=Line([-4.8,.40,0],[2.1,.40,0],color=POSITIVE,stroke_width=5)
        self.trace(room,v,h,run=2.4)
        x=self.t("HORIZONTAL",4.15,.63,29,POSITIVE,3.6,True)
        y=self.t("VERTICAL",4.15,-.55,29,SKETCH,3.6,True)
        self.appearance(x,y,time=1.3)
        self.caption("Models help us find relationships; drawings represent ideal lines.")
        self.wait(3.8)

    def four_cases(self):
        for n,kind,label in [
           (2,"intersect","INTERSECTING: ONE SHARED POINT"),
           (3,"parallel","PARALLEL: NO SHARED POINT"),
           (4,"perpendicular","PERPENDICULAR: 90 DEGREES"),
           (5,"coincident","COINCIDENT: ALL POINTS SHARED")]:
            self.panel(n,"COMPARE / CLASSIFY",label,
                       "Watch the strokes and justify the defining property.")
            strokes=self.axes_lines(kind)
            self.trace(*strokes,run=2.1)
            self.caption("In diagrams, extensions are mathematical; drawn lines are finite.")
            self.wait(3.2)

    def plane(self):
        self.panel(6,"PLANE / INCIDENCE","A LINE CAN LIE WITHIN A PLANE",
                   "The visible parallelogram represents only part of an infinite plane.")
        region=Polygon([-5,-1.45,0],[3.1,-1.45,0],[5,1.12,0],[-3.1,1.12,0],
            color=SKETCH,stroke_width=4,fill_color=MODEL,fill_opacity=.40)
        l=Line([-4,-.50,0],[3.55,-.50,0],color=POSITIVE,stroke_width=5)
        self.play(DrawBorderThenFill(region),run_time=2)
        self.register(region)
        self.trace(l,run=1.6)
        m=self.formula(r"\ell\subset\alpha",0,-2.02,53)
        self.appearance(m,time=1.25)
        self.caption("This example places the complete ideal line in plane alpha.")
        self.wait(4.0)

class Geometry8W02_Class02(CADGeometry8):
    WEEK=2;DATES="JANUARY 25--29, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 02"
    HUD_SUBTITLE="Reasoning and counterexamples / January 25--29"
    COVER_TITLE="REASONING WITH SPATIAL DIAGRAMS"
    LESSON_LABEL="CLASS 02 -- DRAW AND JUSTIFY"

    def construct(self):
        self.run_lesson([self.draw_pair,self.counterexample,self.line_plane,self.verification],
            ["1. Do two parallel lines share any point?",
             "2. Are every two intersecting lines perpendicular?",
             "3. Can a line intersect a plane at one point?"],
            ["1. NO.",
             "2. NO -- THEIR ANGLE MAY BE DIFFERENT FROM 90.",
             "3. YES -- IF IT IS NOT CONTAINED IN THE PLANE."])

    def draw_pair(self):
        self.panel(1,"REASON / DRAW","DRAW TWO CONFIGURATIONS",
                   "Compare an intersection with a right-angle intersection.")
        a=Line([-5,-1,0],[-.5,1,0],color=SKETCH,stroke_width=4.5)
        b=Line([-5,1,0],[-.5,-1,0],color=POSITIVE,stroke_width=4.5)
        c=Line([1,-.6,0],[5.4,-.6,0],color=SKETCH,stroke_width=4.5)
        d=Line([3.2,-1.92,0],[3.2,1.40,0],color=POSITIVE,stroke_width=4.5)
        self.trace(a,b,run=2.0)
        self.trace(c,d,run=2.0)
        self.appearance(self.t("INTERSECTION",-2.77,-1.76,28,DARK,4.8,True),
                        self.t("90-DEGREE INTERSECTION",3.2,-1.93,27,DARK,5.2,True),time=1.1)
        self.wait(4)

    def counterexample(self):
        self.panel(2,"COUNTEREXAMPLE","INTERSECTING DOES NOT IMPLY 90 DEGREES",
                   "Use a counterexample to reject a statement that is too broad.")
        a=Line([-4,0,0],[3.8,0,0],color=SKETCH,stroke_width=5)
        tracker=ValueTracker(72*DEGREES)
        b=always_redraw(lambda:Line([0,0,0],
             [3.05*np.cos(tracker.get_value()),3.05*np.sin(tracker.get_value()),0],
             color=POSITIVE,stroke_width=5))
        a0=Arc(radius=.83,start_angle=0,angle=72*DEGREES,
               color=POSITIVE,stroke_width=3)
        self.trace(a,run=1.0)
        self.add(b);self.register(b)
        self.play(tracker.animate.set_value(38*DEGREES),run_time=3.1,rate_func=smooth)
        self.play(Indicate(b),run_time=1.1)
        self.appearance(self.formula(r"38^\circ\ne90^\circ",2.30,-1.50,56),time=1)
        self.caption("Both lines still meet, but their angle is not a right angle.")
        self.wait(4)

    def line_plane(self):
        self.panel(3,"SPATIAL / REASON","THREE RELATIONSHIPS WITH A PLANE",
                   "A line can lie in a plane, intersect at one point, or be parallel.")
        plane=Polygon([-4.8,-1.18,0],[3,-1.18,0],[4.0,.75,0],[-3.8,.75,0],
            color=SKETCH,stroke_width=4,fill_color=MODEL,fill_opacity=.28)
        self.play(DrawBorderThenFill(plane),run_time=1.65);self.register(plane)
        in_line=Line([-4.10,-.48,0],[2.75,-.48,0],color=POSITIVE,stroke_width=4.5)
        self.trace(in_line,run=1.1)
        self.appearance(self.t("LINE IN THE PLANE",0,-1.90,30,POSITIVE,8,True),time=.9)
        self.wait(2.8)
        self.stage_clear()
        self.panel(4,"SPATIAL / REASON","A LINE CAN CROSS A PLANE ONCE",
                   "A 2D projection is only a schematic of a 3D incidence relation.")
        plane=Polygon([-4.8,-1.18,0],[3,-1.18,0],[4,.75,0],[-3.8,.75,0],
            color=SKETCH,stroke_width=4,fill_color=MODEL,fill_opacity=.28)
        cross=Line([-1.0,-2,0],[1.0,1.74,0],color=POSITIVE,stroke_width=5)
        self.play(DrawBorderThenFill(plane),run_time=1.5);self.register(plane)
        self.trace(cross,run=1.5)
        self.caption("A crossing line is not necessarily contained in the plane.")
        self.wait(3.9)

    def verification(self):
        self.panel(5,"CHECK / PROPERTIES","A DRAWING IS NOT THE DEFINITION",
                   "Compare what the strokes appear to do with the ideal objects.")
        phrases=["PARALLEL: no intersection",
                 "PERPENDICULAR: intersection at 90 degrees",
                 "COINCIDENT: every point belongs to both",
                 "LINE IN PLANE: all line points belong to plane"]
        for i,p in enumerate(phrases):
            m=self.t(p,0,.86-i*.78,32,DARK,11.8)
            self.appearance(m,time=.95)
        self.caption("Explain your classification orally and in writing.")
        self.wait(5)

class Geometry8W03_Class01(CADGeometry8):
    WEEK=3;DATES="FEBRUARY 1--5, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 03"
    HUD_SUBTITLE="Construction instruments / February 1--5"
    COVER_TITLE="STRAIGHTEDGE AND COMPASS"
    LESSON_LABEL="CLASS 01 -- TOOLS AND SEGMENTS"

    def construct(self):
        self.run_lesson([self.tools,self.measure,self.copy_segment,self.instructions],
           ["1. What does a straightedge make?",
            "2. What quantity does a compass preserve?",
            "3. What must a reproducible construction include?"],
           ["1. A STRAIGHT LINE.",
            "2. A FIXED DISTANCE (RADIUS).",
            "3. CLEAR ORDERED STEPS AND LABELS."])

    def tools(self):
        self.panel(1,"TOOLS / COMPARE","RULER VERSUS STRAIGHTEDGE",
                   "A marked ruler measures length; an unmarked edge guides lines.")
        a=RoundedRectangle(width=5.2,height=.56,corner_radius=.09,
                color=SKETCH,stroke_width=3,fill_color=MODEL,fill_opacity=.42)
        a.move_to([-3.3,.35,0])
        b=a.copy().move_to([3.3,.35,0])
        marks=VGroup(*[
          Line([-5.67+i*.49,.11,0],[-5.67+i*.49,.44,0],
              color=DARK,stroke_width=2) for i in range(10)])
        self.trace(a,b,run=1.8);self.trace(marks,run=1.4)
        self.appearance(self.t("MARKED RULER",-3.3,-.70,29,DARK,5,True),
             self.t("UNMARKED STRAIGHTEDGE",3.3,-.70,26,DARK,5.4,True),time=1)
        self.caption("A compass transfers distances without reading a scale.")
        self.wait(4)

    def measure(self):
        self.panel(2,"MEASURE / DRAW","CONSTRUCT A GIVEN SEGMENT LENGTH",
                   "For a 5 cm segment, mark endpoints at the correct ruler separation.")
        start=np.array([-3.9,-.30,0]);end=np.array([2.30,-.30,0])
        l=Line(start,end,color=SKETCH,stroke_width=5)
        A=Dot(start,radius=.16,color=POSITIVE)
        B=Dot(end,radius=.16,color=POSITIVE)
        self.show(A,run=.55);self.trace(l,run=2.2);self.show(B,run=.55)
        self.appearance(self.t("A",-4.20,.15,36,SKETCH,1,True),
             self.t("B",2.60,.15,36,SKETCH,1,True),time=.85)
        self.appearance(self.formula(r"\overline{AB}=5\,\mathrm{cm}",0,-1.53,56),time=1.1)
        self.caption("This drawing is schematic: physical measurement needs a ruler.")
        self.wait(4.3)

    def copy_segment(self):
        self.panel(3,"TRANSFER / COMPASS","REPRODUCE LENGTH WITH AN ARC",
                   "Carry AB to a new location using one fixed compass radius.")
        A=np.array([-4.4,.79,0]);B=np.array([-1.33,.79,0])
        C=np.array([-3.2,-1.13,0]);D=C+RIGHT*3.07
        seg=Line(A,B,color=SKETCH,stroke_width=4.5)
        self.trace(seg,run=1.2)
        for p,n in [(A,"A"),(B,"B"),(C,"C")]:
            self.show(Dot(p,radius=.13,color=POSITIVE),run=.35)
            self.appearance(self.t(n,p[0],p[1]+.29,29,DARK,1,True),time=.3)
        theta=ValueTracker(.001)
        arc=always_redraw(lambda:Arc(radius=3.07,start_angle=-.35,
                angle=theta.get_value(),arc_center=C,
                color=POSITIVE,stroke_width=4))
        self.add(arc);self.register(arc)
        self.play(theta.animate.set_value(.70),run_time=3.0,rate_func=linear)
        new=Line(C,D,color=POSITIVE,stroke_width=4.5)
        self.trace(new,run=1.6)
        self.show(Dot(D,radius=.13,color=SKETCH),run=.35)
        self.appearance(self.t("D",D[0]+.21,D[1]+.22,29,SKETCH,1,True),time=.55)
        self.caption("Compass radius AB equals the transferred segment CD.")
        self.wait(4)

    def instructions(self):
        self.panel(4,"REPEAT / VERIFY","DOCUMENT A REPEATABLE METHOD",
                   "Write actions in order and include your checks.")
        lines=["01  Draw a ray starting at C.",
               "02  Set compass opening to AB.",
               "03  Draw an arc from centre C.",
               "04  Name intersection D and compare lengths."]
        for i,s in enumerate(lines):
            self.appearance(self.t(s,0,.94-.88*i,31,DARK,12.3),time=.9)
        self.caption("Check AB = CD without relying on the screen scale.")
        self.wait(5)

class Geometry8W03_Class02(CADGeometry8):
    WEEK=3;DATES="FEBRUARY 1--5, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 03"
    HUD_SUBTITLE="Perpendicular bisector and parallels / February 1--5"
    COVER_TITLE="PERPENDICULAR AND PARALLEL CONSTRUCTIONS"
    LESSON_LABEL="CLASS 02 -- STEP-BY-STEP"

    def construct(self):
        self.run_lesson([self.bisector,self.parallel,self.accuracy],
          ["1. What does a perpendicular bisector do?",
           "2. Which property checks a perpendicular?",
           "3. Why should compass opening stay fixed?"],
          ["1. CROSSES THE MIDPOINT AT 90 DEGREES.",
           "2. CHECK THE RIGHT ANGLE.",
           "3. TO KEEP THE SAME DISTANCE."])

    def bisector(self):
        self.panel(1,"CONSTRUCT / BISECT","PERPENDICULAR BISECTOR OF AB",
                   "Two equal-radius pairs of arcs locate points equidistant from A and B.")
        A=np.array([-2.50,-.62,0]);B=np.array([2.50,-.62,0])
        L=Line(A,B,color=DARK,stroke_width=4.7)
        self.trace(L,run=1.35)
        self.show(Dot(A,radius=.13,color=SKETCH),Dot(B,radius=.13,color=SKETCH),run=.6)
        self.appearance(self.t("A",-2.78,-1.01,30,DARK,1,True),
             self.t("B",2.78,-1.01,30,DARK,1,True),time=.6)
        # r=3.13 > 2.5 = half the segment; arc intersections y=±1.88
        radius=3.13
        h=np.sqrt(radius**2-2.5**2)
        top=np.array([0,-.62+h,0]);bottom=np.array([0,-.62-h,0])
        arcs=[]
        for c in (A,B):
            arcs.append(Arc(radius=radius,start_angle=0,angle=TAU,
                   arc_center=c,color=SKETCH,stroke_width=2.2))
        # Draw 2 whole circles as simplified construction traces.
        self.trace(*arcs,run=2.2)
        mid=Line([0,-2.38,0],[0,1.70,0],color=POSITIVE,stroke_width=5)
        self.trace(mid,run=1.7)
        square=Square(side_length=.35,color=POSITIVE,stroke_width=2).move_to([.175,-.445,0])
        self.trace(square,run=.65)
        self.caption("The perpendicular bisector passes through midpoint M of segment AB.")
        self.wait(5.1)

    def parallel(self):
        self.panel(2,"CONSTRUCT / PARALLEL","MOVE A PERPENDICULAR, KEEP ITS ANGLE",
                   "Two lines perpendicular to the same line are parallel in one plane.")
        trans=Line([-4.4,-1.75,0],[-4.4,1.64,0],color=SKETCH,stroke_width=4.5)
        a=Line([-4.4,.78,0],[.5,.78,0],color=DARK,stroke_width=4.5)
        b=Line([-4.4,-1.11,0],[.5,-1.11,0],color=POSITIVE,stroke_width=4.5)
        self.trace(trans,a,run=1.6)
        self.trace(b,run=2.0)
        self.appearance(self.formula(r"\ell_1\parallel\ell_2",3.0,-.11,58),time=1)
        self.caption("The right-angle condition provides evidence of parallelism.")
        self.wait(4.2)

    def accuracy(self):
        self.panel(3,"ERROR / PRECISION","CHECK CONSTRUCTION ACCURACY",
                   "Compare your geometric property, not visual appearance alone.")
        first=Line([-4.5,.38,0],[4.5,.38,0],color=SKETCH,stroke_width=5)
        second=Line([-4.5,-1.16,0],[4.5,-.70,0],color=NEGATIVE,stroke_width=5)
        self.trace(first,second,run=1.7)
        self.appearance(self.t("NOT PARALLEL",-3.25,-1.82,35,NEGATIVE,5,True),time=.8)
        self.play(Transform(second,Line([-4.5,-1.16,0],[4.5,-1.16,0],
                                       color=POSITIVE,stroke_width=5)),
                  run_time=2.5)
        self.appearance(self.t("CHECK THE SEPARATION",2.6,-1.84,30,POSITIVE,6,True),time=.95)
        self.caption("Discuss likely sources of error: arc setting, line thickness, alignment.")
        self.wait(5)

class Geometry8W04_Class01(CADGeometry8):
    WEEK=4;DATES="FEBRUARY 8--12, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 04"
    HUD_SUBTITLE="Angle elements and types / February 8--12"
    COVER_TITLE="ANGLES: ELEMENTS AND CLASSIFICATION"
    LESSON_LABEL="CLASS 01 -- ANGLE CONCEPTS"

    def construct(self):
        self.run_lesson([self.angle_parts,self.rotate,self.classify],
          ["1. What is the angle vertex?",
           "2. Is 125 degrees acute, right or obtuse?",
           "3. Is 240 degrees a reflex angle?"],
          ["1. THE COMMON ENDPOINT OF TWO RAYS.",
           "2. OBTUSE.",
           "3. YES -- BETWEEN 180 AND 360 DEGREES."])

    def angle_parts(self):
        self.panel(1,"VERTEX / ARMS","WHAT DEFINES AN ANGLE?",
                   "Two rays with a common endpoint are the arms of an angle.")
        O=np.array([-2.72,-1.20,0])
        r1=Line(O,O+RIGHT*4.35,color=DARK,stroke_width=5)
        r2=Line(O,O+4.30*np.array([np.cos(65*DEGREES),np.sin(65*DEGREES),0]),
                color=SKETCH,stroke_width=5)
        vertex=Dot(O,radius=.18,color=POSITIVE)
        self.trace(r1,r2,run=2.1);self.show(vertex,run=.5)
        arc=Arc(radius=.85,start_angle=0,angle=65*DEGREES,
                  arc_center=O,color=POSITIVE,stroke_width=4)
        self.trace(arc,run=.95)
        self.appearance(self.t("VERTEX O",-3.75,-1.87,31,POSITIVE,3.6,True),
             self.formula(r"\angle AOB=65^\circ",2.75,-.65,51),time=1.3)
        self.caption("Angle notation puts the vertex letter in the middle.")
        self.wait(4)

    def rotate(self):
        self.panel(2,"TURN / MEASURE","ANGLE MAGNITUDE IS A ROTATION",
                   "Direction is the arm's orientation; measure is the turn between arms.")
        O=np.array([-2.8,-.64,0]);tracker=ValueTracker(30*DEGREES)
        h=Arrow(O,O+RIGHT*2.72,buff=0,color=DARK,stroke_width=5)
        m=always_redraw(lambda:Arrow(O,O+2.72*np.array([
                np.cos(tracker.get_value()),np.sin(tracker.get_value()),0]),
                buff=0,color=SKETCH,stroke_width=5))
        arc=always_redraw(lambda:Arc(radius=1.0,start_angle=0,
                     angle=tracker.get_value(),arc_center=O,
                     color=POSITIVE,stroke_width=4))
        self.trace(h,run=1)
        self.add(m,arc);self.register(m,arc)
        for deg in [90,135,180,250]:
            self.play(tracker.animate.set_value(deg*DEGREES),run_time=2.45,
                      rate_func=smooth)
            note=self.formula(f"{deg}^\\circ",3.18,-.62,64)
            self.appearance(note,time=.85)
            self.wait(.8)
            self.play(FadeOut(note),run_time=.3)
        self.caption("The displayed angle here turns counterclockwise from the base ray.")
        self.wait(4)

    def classify(self):
        self.panel(3,"ANGLE / CLASSIFY","CLASSIFY BY DEGREE MEASURE",
                   "Different measures correspond to distinct categories.")
        rows=["ACUTE       0 to 90 degrees (not including 90)",
              "RIGHT       exactly 90 degrees",
              "OBTUSE      between 90 and 180 degrees",
              "STRAIGHT    exactly 180 degrees",
              "REFLEX      between 180 and 360 degrees"]
        for i,s in enumerate(rows):
            self.appearance(self.t(s,0,1.03-i*.68,31,DARK,12.5),time=.8)
        self.caption("Classify by measure, not by the drawing's apparent direction.")
        self.wait(5)

class Geometry8W04_Class02(CADGeometry8):
    WEEK=4;DATES="FEBRUARY 8--12, 2027"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- WEEK 04"
    HUD_SUBTITLE="Protractor measurement and construction / February 8--12"
    COVER_TITLE="MEASURE AND CONSTRUCT ANGLES"
    LESSON_LABEL="CLASS 02 -- PROTRACTOR"

    def construct(self):
        self.run_lesson([self.instrument,self.read_scale,self.construct_angle,self.next_topic],
          ["1. Which point of the protractor aligns with the vertex?",
           "2. From which zero should you read an angle?",
           "3. What is 45 degrees plus 35 degrees?"],
          ["1. THE CENTRE / ORIGIN MARK.",
           "2. THE ZERO ALIGNED WITH THE STARTING RAY.",
           "3. 80 DEGREES -- ANGLE ADDITION PREVIEW."])

    def instrument(self):
        self.panel(1,"PROTRACTOR / ZERO","ALIGN THE PROTRACTOR CORRECTLY",
                   "Centre at the vertex; the zero line follows the base ray.")
        O=np.array([-1.0,-1.0,0]);radius=2.80
        semi=Arc(radius=radius,start_angle=0,angle=PI,
                 arc_center=O,color=SKETCH,stroke_width=4)
        baseline=Line(O+LEFT*radius,O+RIGHT*radius,color=DARK,stroke_width=4)
        self.trace(semi,baseline,run=1.9)
        ticks=VGroup()
        for degree in range(0,181,15):
            d=degree*DEGREES
            v=np.array([np.cos(d),np.sin(d),0])
            p=O+radius*v
            q=O+(radius-.20)*v
            ticks.add(Line(p,q,color=SKETCH,stroke_width=2))
        self.trace(ticks,run=2.0)
        center=Dot(O,radius=.17,color=POSITIVE)
        self.show(center,run=.5)
        ray=Line(O,O+radius*RIGHT,color=POSITIVE,stroke_width=5)
        self.trace(ray,run=1)
        self.appearance(self.t("CENTRE ON VERTEX",3.42,-.88,29,POSITIVE,5.0,True),time=1.1)
        self.caption("A real protractor has two directions of numbering; choose the correct zero.")
        self.wait(4)

    def read_scale(self):
        self.panel(2,"MEASURE / READ","READ A 65-DEGREE ANGLE",
                   "Follow the scale from the zero at the initial ray.")
        O=np.array([-2.15,-1.21,0]);base=Line(O,O+RIGHT*3.70,color=DARK,stroke_width=5)
        end=O+3.70*np.array([np.cos(65*DEGREES),np.sin(65*DEGREES),0])
        moving=Line(O,end,color=SKETCH,stroke_width=5)
        self.trace(base,run=1.2);self.trace(moving,run=1.8)
        arc=Arc(radius=1.11,start_angle=0,angle=65*DEGREES,arc_center=O,
                color=POSITIVE,stroke_width=4.4)
        self.trace(arc,run=1.1)
        self.appearance(self.formula(r"\theta=65^\circ",3.2,-.74,55),time=1.0)
        self.caption("Measure the turn from the chosen initial ray, not the other end of the scale.")
        self.wait(4)

    def construct_angle(self):
        self.panel(3,"DRAW / CONSTRUCT","CONSTRUCT AN ANGLE OF 120 DEGREES",
                   "Draw a base ray, align the protractor, mark 120 degrees, draw the second ray.")
        O=np.array([-2.33,-1.22,0]);rad=3.10
        base=Arrow(O,O+RIGHT*rad,buff=0,color=DARK,stroke_width=5)
        self.trace(base,run=1.25)
        tracker=ValueTracker(0.001)
        ray=always_redraw(lambda:Arrow(
             O,O+rad*np.array([np.cos(tracker.get_value()),np.sin(tracker.get_value()),0]),
             buff=0,color=SKETCH,stroke_width=5))
        arc=always_redraw(lambda:Arc(radius=.92,start_angle=0,
                    angle=tracker.get_value(),arc_center=O,
                    color=POSITIVE,stroke_width=4))
        self.add(ray,arc);self.register(ray,arc)
        self.play(tracker.animate.set_value(120*DEGREES),run_time=3.5,rate_func=smooth)
        self.appearance(self.formula(r"\angle AOB=120^\circ",3.15,-.58,51),time=1.0)
        self.caption("Verify that 120 degrees is obtuse and that the vertex is named correctly.")
        self.wait(4)

    def next_topic(self):
        self.panel(4,"PREVIEW / NEXT TOPIC","ADJACENT ANGLES CAN ADD",
                   "The next activity introduces the angle-addition postulate.")
        O=np.array([-3.0,-1.34,0]);r=3.1
        arms=[]
        for degree,color in [(0,DARK),(45,SKETCH),(80,POSITIVE)]:
            v=np.array([np.cos(degree*DEGREES),np.sin(degree*DEGREES),0])
            arms.append(Line(O,O+r*v,color=color,stroke_width=4.6))
        self.trace(*arms,run=2.0)
        arc1=Arc(radius=.80,start_angle=0,angle=45*DEGREES,arc_center=O,
                 color=SKETCH,stroke_width=4)
        arc2=Arc(radius=.80,start_angle=45*DEGREES,angle=35*DEGREES,
                 arc_center=O,color=POSITIVE,stroke_width=4)
        self.trace(arc1,arc2,run=1.5)
        self.appearance(self.formula(r"45^\circ+35^\circ=80^\circ",3.25,-.43,49),time=1.1)
        self.caption("This is a preview, not an additional Week 4 lesson.")
        self.wait(4.0)
