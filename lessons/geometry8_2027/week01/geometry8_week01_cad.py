#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry Grade 8 / First Quarter 2027 / Week 01 (Jan 19-22).

Two separate, complete institutional CAD-House educational ManimCE videos.

Curriculum authority: "malla curricular - geometría 8° (2026).docx",
Period I, axes: basic geometry concepts/definitions; sets/logical diagrams.
The two-lesson split is an instructional ADAPTATION of those first two axes;
the accessible 2026 curriculum is NOT an individual 2027 weekly class planner.

Style: exact shared Physics9 CanonicalCADPhysics + original IJR PNG via
Week03Base (white / Tex Write / color-coded sketch / phase HUD / pauses).
Reference full-pipeline: Physics9_2027_Week03, verified ManimCE v0.20.1.

Run (from repo root):
  manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad.py Geometry8W01_Foundations
  manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad.py Geometry8W01_Sets
  manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad.py Geometry8W01_Foundations
  manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad.py Geometry8W01_Sets

Do not introduce detailed parallel lines, protractor angle operations or
compass constructions in this lesson; those follow in later weeks.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / "physics9_2027" / "week03"))
from week03_physics9_cad import Week03Base
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, NEGATIVE, TERRAIN, SLAB


class Geometry8Base(Week03Base):
    """The same CAD/PNG presentation as Physics 9 Week 3, with geometry texts."""
    HUD_TITLE = "GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 01"
    HUD_TITLE_SIZE = 30
    HUD_SUBTITLE = "Geometric foundations and sets  /  January 19--22"
    HUD_SUB_SIZE = 19
    COURSE_TITLE = "GEOMETRY 8"
    READING_PAUSE = 3.15
    FINAL_OBSERVATION_PAUSE = 4.15
    MICRO_PAUSE = 1.1

    def institutional_cover(self):
        if not self.LOGO.exists():
            raise FileNotFoundError(f"Missing original IJR PNG: {self.LOGO}")
        logo=ImageMobject(str(self.LOGO)).scale_to_fit_height(2.17)
        logo.to_edge(UP,buff=.33)
        school=self.text(self.INSTITUTION,27,BOLD,DARK)
        subject=self.text("GEOMETRY 8",51,BOLD,DARK)
        period=self.text("2027 -- QUARTER 1 -- WEEK 01",26,BOLD,SKETCH)
        dates=self.text("JANUARY 19--22, 2027",25,BOLD,POSITIVE)
        heading=self.text(self.COVER_TITLE,30,BOLD,DARK)
        section=self.text(self.LESSON_LABEL,24,BOLD,POSITIVE)
        teacher=self.text(f"Teacher: {self.TEACHER}",23,NORMAL,MID)
        blue_rule=Line(LEFT*5.4,RIGHT*5.4,color=SKETCH,stroke_width=2.4)
        gray_rule=Line(LEFT*4.2,RIGHT*4.2,color=LIGHT,stroke_width=1.3)
        stack=VGroup(school,subject,period,dates,blue_rule,heading,section,gray_rule,teacher)
        stack.arrange(DOWN,buff=.13)
        stack.next_to(logo,DOWN,buff=.09)
        if stack.get_bottom()[1]<-3.53:
            stack.scale_to_fit_height(5.10)
            stack.next_to(logo,DOWN,buff=.09)
        all_items=[logo,*stack]
        for x in all_items:
            self.add_fixed_in_frame_mobjects(x)
        self.play(FadeIn(logo),Write(school),run_time=1.1)
        self.play(Write(subject),Write(period),run_time=1.35)
        self.play(Write(dates),Create(blue_rule),run_time=.9)
        self.play(Write(heading),Write(section),run_time=1.55)
        self.play(Create(gray_rule),Write(teacher),run_time=.9)
        self.wait(4.4)
        self.play(*[FadeOut(x) for x in all_items],run_time=.80)
        for x in all_items:
            self.remove_fixed_in_frame_mobjects(x)
            self.remove(x)

    def label_figure(self,s,x,y,size=28,color=DARK,bold=False,width=4.8):
        return self.put(s,(x,y),size,color,bold,width)

    def finish(self,heading,first,second):
        self.stage_clear()
        self.set_phase(99,"CHECK / EXPLAIN",POSITIVE)
        title=self.put(heading,(0,1.35),43,POSITIVE,True,12.7)
        a=self.put(first,(0,.08),34,DARK,False,12.7)
        b=self.put(second,(0,-1.03),31,SKETCH,False,12.7)
        self.appearance(title,time=1.1)
        self.appearance(a,b,time=1.65)
        self.caption("Describe your construction and justify each answer.")
        self.wait(7.0)
        self.stage_clear()
        self.footer_cleanup()


class Geometry8W01_Foundations(Geometry8Base):
    LESSON_LABEL="CLASS 01 -- BASIC GEOMETRIC CONCEPTS"
    COVER_TITLE="DISCOVER THE LANGUAGE OF GEOMETRY"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.intro()
        self.points()
        self.line_ray_segment()
        self.dimensions()
        self.model_drawing()
        self.classwork()
        self.finish("GEOMETRY BEGINS WITH SIMPLE OBJECTS",
                    "A point names a location; lines describe direction.",
                    "A segment has exactly two endpoints.")

    def intro(self):
        self.chapter(1,"OBSERVE / DESCRIBE","GEOMETRY IS ALL AROUND US",
                     "We study positions, shapes, sizes and spatial relationships.")
        frame=Rectangle(width=8.3,height=3.15,stroke_color=DARK,
                        stroke_width=3.2,fill_color=WHITE,
                        fill_opacity=0.0).move_to([0,-.44,0])
        floor=Line([-4.13,-1.72,0],[4.13,-1.72,0],stroke_width=2.8,color=MID)
        corner=Dot([-.9,-.93,0],radius=.19,color=SKETCH)
        edge=Line([-2.65,-.90,0],[1.42,-.90,0],stroke_width=5.2,color=SKETCH)
        shape=Polygon([1.68,.20,0],[3.03,.20,0],[3.03,-1.17,0],[1.68,-1.17,0],
                       stroke_color=POSITIVE,stroke_width=3.5,
                       fill_color=TERRAIN,fill_opacity=.6)
        self.draw(frame,floor,time=1.45)
        self.play(FadeIn(corner),Create(edge),run_time=1.2)
        self.play(Create(shape),run_time=1.25)
        self.register(corner,edge,shape)
        for text,x in (("POINT",-3.10),("LINE",-0.15),("SHAPE",2.40)):
            label=self.label_figure(text,x,-2.14,27,SKETCH,True,3.0)
            self.appearance(label,time=.45)
        self.caption("These elements give us a language for describing a diagram.")
        self.wait(3)

    def points(self):
        self.chapter(2,"POINTS / LOCATIONS","A POINT HAS POSITION, NOT SIZE",
                     "Dots are symbols used to show exact mathematical locations.")
        A=np.array([-3.45,-.10,0]);B=np.array([2.75,-.83,0])
        pA=Dot(A,radius=.24,color=SKETCH)
        pB=Dot(B,radius=.24,color=POSITIVE)
        nameA=self.label_figure("A",-3.0,.31,34,SKETCH,True,1.0)
        nameB=self.label_figure("B",3.15,-.43,34,POSITIVE,True,1.0)
        self.play(FadeIn(pA),Write(nameA),run_time=1.3)
        self.play(FadeIn(pB),Write(nameB),run_time=1.3)
        self.register(pA,pB)
        route=DashedLine(A,B,dash_length=.17,color=LIGHT,stroke_width=2.6)
        self.draw(route,time=1.15)
        line=self.put("A point is not a tiny circle: it is an exact location.",
                      (0,-2.12),30,DARK,False,12.2)
        self.appearance(line,time=1.15)
        self.caption("Name points using capital letters, such as A and B.")
        self.wait(4.0)

    def line_ray_segment(self):
        self.chapter(3,"LINE / RAY / SEGMENT","WHICH ONE HAS ENDPOINTS?",
                     "Observe how each construction extends in its direction.")
        # 3 distinct geometric objects, with correctly represented endpoints.
        examples=[
            ("LINE AB", .73, "both directions"),
            ("RAY AB", -.36, "one endpoint"),
            ("SEGMENT AB", -1.49, "two endpoints"),
        ]
        for name,y,note in examples:
            L=np.array([-4.25,y,0]);R=np.array([2.25,y,0])
            if name.startswith("LINE"):
                fig=DoubleArrow(L,R,stroke_width=4.0,color=SKETCH,
                                buff=0,max_tip_length_to_length_ratio=.12)
            elif name.startswith("RAY"):
                fig=Arrow(L,R,stroke_width=4.0,color=SKETCH,
                          buff=0,max_tip_length_to_length_ratio=.12)
            else:
                fig=Line(L,R,stroke_width=4.2,color=SKETCH)
            self.draw(fig,time=1.1)
            # A/B are correctly on each object: interior points for a line,
            # A endpoint/B interior for a ray, both endpoints for a segment.
            if name.startswith("LINE"):
                pA=np.array([-2.80,y,0]);pB=np.array([.35,y,0])
            elif name.startswith("RAY"):
                pA=L;pB=np.array([.35,y,0])
            else:
                pA=L;pB=R
            markerA=Dot(pA,radius=.115,color=POSITIVE)
            markerB=Dot(pB,radius=.115,color=POSITIVE)
            self.play(FadeIn(markerA),FadeIn(markerB),run_time=.45)
            self.register(markerA,markerB)
            labelA=self.label_figure("A",pA[0]-.15,y+.29,24,SKETCH,True,1.0)
            labelB=self.label_figure("B",pB[0]+.15,y+.29,24,SKETCH,True,1.0)
            self.appearance(labelA,labelB,time=.52)
            a=self.label_figure(name,4.35,y+.25,26,DARK,True,3.6)
            b=self.label_figure(note,4.35,y-.18,22,MID,False,3.6)
            self.appearance(a,b,time=.88)
            self.wait(.95)
        self.caption("Line: no endpoints. Ray: one. Segment: two.")
        self.wait(3.2)

    def dimensions(self):
        self.chapter(4,"0D / 1D / 2D / 3D","FROM POINTS TO SPACE",
                     "A model has zero, one, two or three spatial dimensions.")
        centres=[-4.55,-1.56,1.45,4.56]
        zero=Dot([centres[0],-.33,0],radius=.21,color=SKETCH)
        one=Line([centres[1]-1.0,-.33,0],[centres[1]+1.0,-.33,0],
                 color=SKETCH,stroke_width=5)
        two=Square(side_length=1.32,stroke_color=SKETCH,
                   stroke_width=3,fill_color=MODEL,fill_opacity=.56)
        two.move_to([centres[2],-.33,0])
        # Axonometric sketch: visually conveys 3 spatial directions,
        # without introducing volume calculations.
        cube_front=Square(side_length=1.30,stroke_color=DARK,stroke_width=3)
        cube_front.move_to([centres[3]-.24,-.62,0])
        cube_back=Square(side_length=1.30,stroke_color=SKETCH,stroke_width=3)
        cube_back.move_to([centres[3]+.25,-.03,0])
        connectors=VGroup(*[
           Line(p,q,color=SKETCH,stroke_width=2.4)
           for p,q in zip(cube_front.get_vertices(),cube_back.get_vertices())
        ])
        drawings=[zero,one,two,VGroup(cube_front,cube_back,connectors)]
        labels=["0D: POINT","1D: LENGTH","2D: PLANE","3D: SPACE"]
        for x,d,label in zip(centres,drawings,labels):
            self.play(Create(d) if isinstance(d,VMobject) else FadeIn(d),run_time=1.08)
            self.register(d)
            caption=self.label_figure(label,x,-1.90,26,DARK,True,2.9)
            self.appearance(caption,time=.80)
            self.wait(1.0)
        self.caption("A flat diagram can depict a 3D object; the diagram itself is 2D.")
        self.wait(3.7)

    def model_drawing(self):
        self.chapter(5,"PLAN / MODEL","BUILD A GEOMETRIC DRAWING",
                     "Use points and segments to describe a room outline.")
        # A room schematic with four corners A B C D and a door opening.
        coords=[[-3.45,-1.28,0],[3.1,-1.28,0],[3.1,.65,0],[-3.45,.65,0]]
        names=["A","B","C","D"]
        for k in [0,1,2,3]:
            dot=Dot(coords[k],radius=.13,color=SKETCH)
            self.play(FadeIn(dot),run_time=.30);self.register(dot)
            shift=[[-.32,-.20],[.33,-.20],[.33,.28],[-.33,.28]][k]
            tag=self.label_figure(names[k],coords[k][0]+shift[0],
                                  coords[k][1]+shift[1],27,SKETCH,True,1.0)
            self.appearance(tag,time=.28)
        for i in range(4):
            segment=Line(coords[i],coords[(i+1)%4],
                         color=DARK,stroke_width=4)
            self.draw(segment,time=.68)
        doorway=Line([-1.50,-1.28,0],[-.56,-1.28,0],stroke_width=9,color=WHITE)
        self.play(Create(doorway),run_time=.68);self.register(doorway)
        door_arc=Arc(radius=.98,start_angle=0,angle=PI/2,arc_center=[-1.5,-1.28,0],
                     color=POSITIVE,stroke_width=3)
        self.draw(door_arc,time=1.10)
        self.caption("Plan view: a room can be described by points and straight segments.")
        self.wait(3.0)

    def classwork(self):
        self.chapter(6,"PRACTICE / IDENTIFY","CHECK YOUR UNDERSTANDING",
                     "Say which geometric object best fits each description.")
        q=[
            "1. An exact location has no dimensions.",
            "2. A straight path extends infinitely both ways.",
            "3. A finite straight part has two endpoints.",
        ]
        for i,t in enumerate(q):
            label=self.put(t,(0,.63-i*.90),31,DARK,False,12.3)
            self.appearance(label,time=.9)
        self.caption("Pause, answer in pairs, and justify your choice.")
        self.wait(7)
        self.stage_clear()
        answers=["1. POINT","2. LINE","3. SEGMENT"]
        for i,t in enumerate(answers):
            answer=self.put(t,(0,.70-i*.90),37,POSITIVE,True,11)
            self.appearance(answer,time=1.02)
        self.caption("We identify geometry by its defining properties.")
        self.wait(3.3)


class Geometry8W01_Sets(Geometry8Base):
    LESSON_LABEL="CLASS 02 -- SETS AND LOGICAL DIAGRAMS"
    COVER_TITLE="CLASSIFY FIGURES WITH LOGICAL SETS"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.set_definition()
        self.venn()
        self.intersection()
        self.union()
        self.counting()
        self.practice()
        self.finish("SETS ORGANIZE GEOMETRIC OBJECTS",
                    "Intersection requires BOTH properties.",
                    "Union requires AT LEAST ONE property.")

    def set_definition(self):
        self.chapter(1,"SET / MEMBER","WHAT IS A GEOMETRIC SET?",
                     "A set groups objects with a well-defined shared property.")
        outlines=VGroup(
            Triangle().scale(.48).set_stroke(SKETCH,width=3),
            Square(side_length=.88).set_stroke(POSITIVE,width=3),
            Circle(radius=.42).set_stroke(DARK,width=3),
        )
        for obj,x in zip(outlines,[-3.4,0,3.4]):
            obj.move_to([x,-.33,0])
            self.play(Create(obj),run_time=.88)
            self.register(obj)
        tag=self.put("A set can be described by a rule or by listing its members.",
                     (0,-1.79),30,POSITIVE,True,12.5)
        self.appearance(tag,time=1.1)
        self.caption("Example rule: all triangular figures in a selected collection.")
        self.wait(3.2)

    def venn_objects(self):
        # Common exact reference collection for EVERY subsequent set scene.
        frame=Rectangle(width=12.05,height=3.33,stroke_color=LIGHT,
                        stroke_width=1.8).move_to([0,-.43,0])
        circleA=Circle(radius=1.32,stroke_color=SKETCH,
                       stroke_width=3.3).move_to([-1.04,-.42,0])
        circleB=Circle(radius=1.32,stroke_color=POSITIVE,
                       stroke_width=3.3).move_to([1.04,-.42,0])
        A_label=self.label_figure("A: TRIANGLES",-2.8,.91,25,SKETCH,True,3.0)
        B_label=self.label_figure("B: BLUE",2.72,.91,25,POSITIVE,True,3.0)
        # A-only: green triangle. Both: blue triangle.
        # B-only: blue square. Neither: gray square.
        A_only=Triangle().scale(.37).set_stroke(POSITIVE,width=3.3)
        A_only.move_to([-1.93,-.46,0])
        AB=Triangle().scale(.37).set_stroke(SKETCH,width=3.3)
        AB.move_to([0,-.46,0])
        B_only=Square(side_length=.70).set_stroke(SKETCH,width=3.3)
        B_only.move_to([1.93,-.46,0])
        neither=Square(side_length=.70).set_stroke(MID,width=3.3)
        neither.move_to([4.50,-.86,0])
        objects=(frame,circleA,circleB,A_only,AB,B_only,neither)
        self.draw(frame,time=.65)
        self.draw(circleA,circleB,time=1.7)
        self.appearance(A_label,B_label,time=.95)
        self.play(*[Create(o) for o in (A_only,AB,B_only,neither)],run_time=1.7)
        self.register(A_only,AB,B_only,neither)
        return objects

    def venn(self):
        self.chapter(2,"LOGICAL DIAGRAM","TRIANGLES AND BLUE FIGURES",
                     "Every object is placed where its properties are satisfied.")
        self.venn_objects()
        self.caption("A: triangles. B: blue figures. The blue triangle belongs to both.")
        self.wait(4.2)

    def intersection(self):
        self.chapter(3,"INTERSECTION / AND","A AND B: THE OVERLAPPING REGION",
                     "An object must satisfy BOTH conditions to belong here.")
        self.venn_objects()
        m=self.eq(r"A\cap B=\{\text{blue triangle}\}",
                  (0,-2.23),42,POSITIVE,11.8)
        self.appearance(m,time=1.35)
        self.caption("The blue triangle is in the intersection; the blue square is not.")
        self.wait(4.2)

    def union(self):
        self.chapter(4,"UNION / OR","A OR B: EITHER PROPERTY",
                     "The union includes objects satisfying at least one condition.")
        self.venn_objects()
        msg=self.put("A union B: both triangles AND the blue square.",
                     (0,-2.22),32,POSITIVE,True,12.3)
        self.appearance(msg,time=1.18)
        self.caption("The gray square belongs to neither set; it is excluded.")
        self.wait(4.1)

    def counting(self):
        self.chapter(5,"COUNTING / NO DOUBLE COUNT","HOW MANY IN THE UNION?",
                     "Do not count the blue triangle twice.")
        m1=self.eq(r"|A|=2,\quad |B|=2",(0,.66),49,SKETCH)
        self.appearance(m1,time=1.26)
        m2=self.eq(r"|A\cap B|=1",(0,-.22),49,DARK)
        self.appearance(m2,time=1.06)
        m3=self.eq(r"|A\cup B|=2+2-1=3",(0,-1.17),51,POSITIVE)
        self.appearance(m3,time=1.33)
        self.caption("Count the overlap once: 2 + 2 - 1 = 3 distinct objects.")
        self.wait(4.0)

    def practice(self):
        self.chapter(6,"PAIR TASK / EXPLAIN","CLASSIFY BEFORE YOU COUNT",
                     "A = triangles, B = blue figures. Use the preceding diagram.")
        qs=[
            "1. Which object belongs to both A and B?",
            "2. Which object belongs only to B?",
            "3. Which object belongs to neither set?",
        ]
        for i,txt in enumerate(qs):
            m=self.put(txt,(0,.68-i*.87),31,DARK,False,12.6)
            self.appearance(m,time=.95)
        self.caption("Pause and identify the property that justifies each answer.")
        self.wait(7.0)
        self.stage_clear()
        answers=["1. BLUE TRIANGLE","2. BLUE SQUARE","3. GRAY SQUARE"]
        for i,txt in enumerate(answers):
            m=self.put(txt,(0,.71-i*.90),36,POSITIVE,True,11.8)
            self.appearance(m,time=.95)
        self.caption("Every answer follows from the original set definitions.")
        self.wait(3.2)
