#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEOMETRY 8 / 2027 / WEEK01 CLASS01 / V4.

Target: ALL TEN Period I thematic axes, in the original order found on p.1 of
user-uploaded Instituto Jorge Robledo 'malla curricular - geometría 8° (2026)(1).docx'.
Period I list (2026 reference, NOT a fabricated 2027 weekly schedule):
 1 basic geometric concepts/definitions
 2 sets and logical diagrams
 3 lines, planes and relations
 4 straightedge/compass constructions
 5 concept and measurement of angle
 6 angle: definition/elements/measure
 7 types of angles
 8 angle-addition postulate
 9 parallel, perpendicular and transversal lines
10 notable angles formed by parallel lines

Actual 2027 Week01 Class01 lesson: induction, point/line/segment/ray/plane;
the V3 source already preserves it and the 2027 Week01–04 mini-planner.
This V4 is an INTRODUCTORY OVERVIEW of P1 ideas, not teaching W2–W4
procedures ahead of the course. Original V3 overview of Periods II and III
and the original Week01 pedagogical sequence are retained.

Rendering: pinned ManimCE 0.20.1, -pql before final -pqh; real IJR PNG
logo, exact institutional House-Extrusion CAD palette/HUD via inheritance.

Commands:
manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad_v4_period1.py Geometry8W01_Period1RoadmapV4
manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad_v4_period1.py Geometry8W01_Period1RoadmapV4
"""
from __future__ import annotations
import numpy as np
from manim import *
from geometry8_week01_cad_v3_roadmap import Geometry8W01_YearRoadmapV3
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, NEGATIVE, TERRAIN, SLAB


class Geometry8W01_Period1RoadmapV4(Geometry8W01_YearRoadmapV3):
    """V3 institutional CAD, V4 precise and visually explicit Period I roadmap."""
    LESSON_LABEL = "CLASS 01 -- PERIOD I AND COURSE ROADMAP"
    COVER_TITLE = "FROM GEOMETRIC OBJECTS TO ANGLE RELATIONS"

    # 2026 malla curricular, Period I, p.1, ten axes -- preserve source order.
    P1_TOPICS = (
        "Basic geometric concepts and definitions",
        "Sets and logical diagrams",
        "Lines, planes and their relationships",
        "Constructions with ruler and compass",
        "Concept of angle and measurement",
        "Angle: definition, elements and measure",
        "Types of angles",
        "Angle-addition postulate",
        "Parallel, perpendicular and transversal lines",
        "Notable angles between parallel lines",
    )

    def heading(self,n,phase,title,subtitle):
        # Automatically number all inherited and V4 scenes in visual order.
        number=self._phase_number
        self._phase_number+=1
        return self.chapter(number,phase,title,subtitle)

    def construct(self):
        self._phase_number=0
        self.institutional_cover()
        self.ph=self.fixed_hud()

        # Introductory full-year overview, consistent with prior V3.
        self.year_map()

        # The detailed original-source Period I introduction.
        self.period_one_map()
        self.period_one_second_half()
        self.period_one_motion()  # inherited V3: moving Venn shape and transversal
        self.line_plane_relations_preview()
        self.construction_tools_preview()
        self.angle_types_preview()
        self.angle_addition_preview()
        self.parallel_angles_preview()

        # Period II/III previews and actual Week01–04 2027 timeline,
        # both inherited and unchanged from the accepted V3.
        self.period_two_map()
        self.period_two_motion()
        self.period_three_map()
        self.period_three_motion()
        self.verified_2027_four_weeks()

        # Preserve 2027 Week 1 Class01 teaching core exactly as in V2/V3.
        self.course_conventions()
        self.a_point()
        self.line_ray_segment()
        self.plane()
        self.notation()
        self.model_and_counterexample()
        self.practice()
        self.exit_review(
            "PERIOD I BEGINS WITH A GEOMETRIC LANGUAGE",
            "Today: name and compare points, lines, rays, segments and planes.")

    def _topic_group(self,items,number_offset):
        """Large, explicit, numbered 2026 malla topics, with aligned leader rules."""
        for idx,topic in enumerate(items):
            i=number_offset+idx+1
            y=1.05-idx*.75
            marker=Dot([-5.45,y-.01,0],radius=.105,color=SKETCH if i%2 else POSITIVE)
            divider=Line([-4.86,y-.33,0],[5.70,y-.33,0],
                         stroke_width=1.65,color=LIGHT)
            n=self.big_text(f"{i:02d}",-5.14,y,29,SKETCH,1.10,True)
            label=self.big_text(topic,.25,y,30,DARK,10.65)
            self.play(FadeIn(marker),Write(n),Write(label),
                      Create(divider),run_time=1.20)
            self.register(marker,divider)
            self.wait(.62)
        self.watch(3.9)

    def period_one_map(self):
        self.heading(1,"P1 / TOPICS 01-05","PERIOD I -- FIRST FIVE TOPICS",
                     "Exact scope and order: IJR Grade 8 Geometry malla, 2026.")
        self._topic_group(self.P1_TOPICS[:5],0)
        self.caption("These are previews of concepts that will be developed in Period I.")
        self.watch(3.8)

    def period_one_second_half(self):
        self.heading(2,"P1 / TOPICS 06-10","PERIOD I -- NEXT FIVE TOPICS",
                     "Angle structure, addition and relationships between parallel lines.")
        self._topic_group(self.P1_TOPICS[5:],5)
        self.caption("We will learn to justify relationships, not just name figures.")
        self.watch(4.1)

    def line_plane_relations_preview(self):
        self.heading(4,"P1 / LINES AND PLANES","HOW DO GEOMETRIC OBJECTS RELATE?",
                     "A diagram can show incidence, parallelism and perpendicularity.")
        # Model of a plane: boundary is schematic, NOT a true plane edge.
        plane=Polygon([-5.10,-1.48,0],[-.90,-1.48,0],
                      [.02,.48,0],[-4.17,.48,0],
                      stroke_color=SKETCH,stroke_width=4.2,
                      fill_color=SKETCH,fill_opacity=.08)
        segment=Line([-4.55,-.84,0],[-.48,-.84,0],
                     stroke_width=4.8,color=POSITIVE)
        dot=Dot([-2.33,-.84,0],radius=.15,color=DARK)
        self.draw_stage(plane,runtime=1.45)
        self.draw_stage(segment,runtime=1.05)
        self.play(FadeIn(dot),run_time=.55)
        self.register(dot)
        a=self.big_text("LINE IN A PLANE",-2.65,-2.05,28,SKETCH,5.2,True)
        self.appearance(a,time=.75)

        # Right-hand views; distinct parallel and perpendicular cases.
        p1=Line([1.43,.54,0],[5.63,.54,0],color=DARK,stroke_width=4)
        p2=Line([1.43,-.12,0],[5.63,-.12,0],color=DARK,stroke_width=4)
        self.draw_stage(p1,p2,runtime=1.05)
        label1=self.big_text("PARALLEL",3.50,1.20,29,SKETCH,4.0,True)
        self.appearance(label1,time=.55)
        h=Line([1.65,-1.45,0],[5.46,-1.45,0],
               color=DARK,stroke_width=4)
        v=Line([3.55,-2.19,0],[3.55,-.71,0],
               color=POSITIVE,stroke_width=4)
        box=Square(side_length=.29,stroke_color=POSITIVE,
                   stroke_width=2.3,fill_opacity=0)
        box.move_to([3.695,-1.305,0])
        self.draw_stage(h,v,box,runtime=1.16)
        label2=self.big_text("PERPENDICULAR",3.50,-2.32,25,POSITIVE,4.50,True)
        self.appearance(label2,time=.66)
        self.caption("Straight objects and planes can be compared by their spatial relations.")
        self.watch(4.7)

    def construction_tools_preview(self):
        self.heading(5,"P1 / RULER AND COMPASS","TWO TOOLS, TWO GEOMETRIC IDEAS",
                     "A ruler creates straight edges; a compass traces equal-radius arcs.")
        # IJR's DBA specifies a ruler WITHOUT graduations for constructions.
        # Distinguish the straightedge from a measuring scale.
        ruler=RoundedRectangle(width=5.20,height=.46,corner_radius=.07,
                stroke_color=MID,stroke_width=2.6,
                fill_color=MODEL,fill_opacity=.34).move_to([-3.08,-.89,0])
        edge=Line([-5.64,-.61,0],[-.52,-.61,0],
                  color=SKETCH,stroke_width=4.3)
        self.draw_stage(ruler,edge,runtime=1.80)
        m1=self.big_text("UNMARKED RULER: STRAIGHT EDGE",
                         -3.05,-1.64,28,DARK,6.35,True)
        self.appearance(m1,time=.80)

        c=np.array([3.20,-.55,0]);radius=1.31
        angle=ValueTracker(.0001)
        trace=always_redraw(lambda: Arc(
            radius=radius,start_angle=0,
            angle=angle.get_value(),arc_center=c,
            stroke_color=SKETCH,stroke_width=5.0))
        arm=always_redraw(lambda:Line(
            c,c+radius*np.array([np.cos(angle.get_value()),
                                 np.sin(angle.get_value()),0]),
            color=POSITIVE,stroke_width=4))
        pivot=Dot(c,radius=.135,color=DARK)
        self.add(trace,arm,pivot)
        self.register(trace,arm,pivot)
        self.play(angle.animate.set_value(TAU),
                  run_time=3.75,rate_func=linear)
        m2=self.big_text("COMPASS: FIXED RADIUS",3.20,-2.21,29,POSITIVE,5.3,True)
        self.appearance(m2,time=.77)
        self.caption("Tool preview only: detailed construction techniques belong to Week 3.")
        self.watch(5.0)

    def angle_types_preview(self):
        self.heading(6,"P1 / ANGLES AND TYPES","A ROTATING RAY GENERATES ANGLES",
                     "Vertex O joins two rays; turning angle determines its type.")
        c=np.array([-3.21,-.61,0]);r=2.36
        theta=ValueTracker(35*DEGREES)
        origin=Dot(c,radius=.15,color=DARK)
        fixed=Arrow(c,c+RIGHT*r,buff=0,color=DARK,stroke_width=4.7,
                    max_tip_length_to_length_ratio=.11)
        moving=always_redraw(lambda:Arrow(
            c,c+r*np.array([np.cos(theta.get_value()),
                            np.sin(theta.get_value()),0]),
            buff=0,color=SKETCH,stroke_width=4.8,
            max_tip_length_to_length_ratio=.11))
        arc=always_redraw(lambda:Arc(
            radius=.86,start_angle=0,angle=max(.001,theta.get_value()),
            arc_center=c,color=POSITIVE,stroke_width=4))
        self.draw_stage(fixed,runtime=1.14)
        self.add(origin,moving,arc);self.register(origin,moving,arc)
        desc=self.big_text("ACUTE",3.36,.69,42,SKETCH,5.7,True)
        measure=self.big_math(r"35^\circ",3.30,-.35,67,POSITIVE,4.6)
        self.appearance(desc,measure,time=1.2)
        for degree,name in [(90,"RIGHT"),(125,"OBTUSE"),(180,"STRAIGHT")]:
            next_desc=self.big_text(name,3.36,.69,42,SKETCH,5.7,True)
            next_m=self.big_math(str(degree)+r"^\circ",3.30,-.35,67,POSITIVE,4.6)
            self.play(theta.animate.set_value(degree*DEGREES),
                      ReplacementTransform(desc,next_desc),
                      ReplacementTransform(measure,next_m),
                      run_time=2.25,rate_func=smooth)
            desc,measure=next_desc,next_m
            self.watch(1.0)
        caption=self.big_text("Angle measure follows the ray's turn.",3.25,-1.58,30,DARK,5.55)
        self.appearance(caption,time=.94)
        self.caption("Illustrative angle types; precise measurement is covered later.")
        self.watch(4.9)

    def angle_addition_preview(self):
        self.heading(7,"P1 / ANGLE ADDITION","ADJACENT ANGLES CAN BE ADDED",
                     "A shared vertex and a common ray form adjacent angles.")
        O=np.array([-3.51,-1.28,0]);r=2.59
        def point(deg):
            return O+r*np.array([np.cos(deg*DEGREES),
                                 np.sin(deg*DEGREES),0])
        A,B,C=point(0),point(30),point(80)
        OA=Line(O,A,color=DARK,stroke_width=4.8)
        OB=Line(O,B,color=SKETCH,stroke_width=4.8)
        OC=Line(O,C,color=POSITIVE,stroke_width=4.8)
        origin=Dot(O,radius=.14,color=DARK)
        self.draw_stage(OA,runtime=1.02)
        self.draw_stage(OB,OC,runtime=1.45)
        self.play(FadeIn(origin),run_time=.35);self.register(origin)
        for at,letter,offset in (
            (O,"O",(-.27,-.27)),
            (A,"A",(.21,-.20)),
            (B,"B",(.10,.30)),
            (C,"C",(-.02,.28))):
            self.appearance(self.big_text(letter,at[0]+offset[0],
                             at[1]+offset[1],25,SKETCH,1.0,True),time=.45)
        arc1=Arc(radius=.80,start_angle=0,angle=30*DEGREES,arc_center=O,
                 color=SKETCH,stroke_width=4)
        arc2=Arc(radius=.80,start_angle=30*DEGREES,
                 angle=50*DEGREES,arc_center=O,
                 color=POSITIVE,stroke_width=4)
        arc3=Arc(radius=1.30,start_angle=0,angle=80*DEGREES,arc_center=O,
                 color=DARK,stroke_width=3.4)
        self.draw_stage(arc1,arc2,runtime=1.52)
        self.draw_stage(arc3,runtime=1.00)
        eq=self.big_math(r"30^\circ+50^\circ=80^\circ",
                         3.09,.15,52,POSITIVE,6.35)
        self.appearance(eq,time=1.2)
        note=self.big_math(r"\angle AOC=\angle AOB+\angle BOC",
                           3.05,-.84,40,DARK,6.25)
        self.appearance(note,time=.97)
        self.caption("Angle-addition postulate: parts add to the whole angle.")
        self.watch(5.9)

    def parallel_angles_preview(self):
        self.heading(8,"P1 / TRANSVERSAL ANGLES","PARALLEL LINES CREATE EQUAL ANGLES",
                     "Corresponding angles are congruent for parallel lines.")
        upper_y=.82;lower_y=-1.04
        xu=-2.30
        xl=xu+(lower_y-upper_y)/np.sqrt(3.0)
        upper=Line([-5.60,upper_y,0],[.45,upper_y,0],
                   color=DARK,stroke_width=4.0)
        lower=Line([-5.60,lower_y,0],[.45,lower_y,0],
                   color=DARK,stroke_width=4.0)
        trans=Line(
           [xu+(-1.80-upper_y)/np.sqrt(3),-1.80,0],
           [xu+(1.67-upper_y)/np.sqrt(3),1.67,0],
           color=SKETCH,stroke_width=4.5)
        self.draw_stage(upper,lower,runtime=1.2)
        self.draw_stage(trans,runtime=1.35)
        a=Arc(radius=.59,start_angle=0,angle=PI/3,
              arc_center=[xu,upper_y,0],
              color=POSITIVE,stroke_width=4.4)
        b=Arc(radius=.59,start_angle=0,angle=PI/3,
              arc_center=[xl,lower_y,0],
              color=POSITIVE,stroke_width=4.4)
        self.draw_stage(a,b,runtime=1.5)
        one=self.big_text("1",xu+.83,upper_y+.42,28,POSITIVE,1.0,True)
        two=self.big_text("2",xl+.83,lower_y+.42,28,POSITIVE,1.0,True)
        self.appearance(one,two,time=.85)
        heading=self.big_text("CORRESPONDING",3.20,.80,32,SKETCH,5.5,True)
        eq=self.big_math(r"\angle 1=\angle 2=60^\circ",
                         3.17,-.22,45,POSITIVE,5.95)
        self.appearance(heading,eq,time=1.15)
        self.play(Indicate(a,scale_factor=1.12),
                  Indicate(b,scale_factor=1.12),
                  run_time=2.10)
        self.caption("The equal 60-degree angles depend on the two lines being parallel.")
        self.watch(6.1)
