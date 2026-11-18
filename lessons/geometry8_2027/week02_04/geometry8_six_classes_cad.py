#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEOMETRY 8 • 2027 Q1 • WEEKS 02–04 • SIX CAD HOUSE CLASSES.

Exact 2027 planner: Geometry_8_2027_P1.docx, Grades 8, Week 2–4,
two ordered lessons in each week. Reference 2026 IJR malla curricular,
Period I, basic geometry -> line/plane -> constructions -> angles.

Reusable heritage: Geometry8V2Base => Geometry8Base => Week03Base
=> CanonicalCADPhysics. Identical PNG IJR crest, same white technical
CAD UI, color semantics, numbered HUD, animated stages and pauses.
School planner details are intentionally not extended beyond the first
four weeks. All explanatory figures are 2D representations of ideals.

Scenes (six independent MP4):
 Geometry8W02_Class01_LinePlane
 Geometry8W02_Class02_SpatialReasoning
 Geometry8W03_Class01_Instruments
 Geometry8W03_Class02_Constructions
 Geometry8W04_Class01_Angles
 Geometry8W04_Class02_Protractor

Compatible with ManimCE 0.20.1. Run PQL then PQH.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from manim import *

# Explicit source imports, never depend on caller's PYTHONPATH.
BASE=Path(__file__).resolve().parents[1] / "week01"
sys.path.insert(0,str(BASE))
from geometry8_week01_cad_v2 import Geometry8V2Base
from physics9_week01_cad import (
    DARK,MID,LIGHT,MODEL,SKETCH,POSITIVE,NEGATIVE,TERRAIN,SLAB
)


def point(x,y):
    return np.array([x,y,0.0])


class Geometry8WeekCAD(Geometry8V2Base):
    """Persistent original CAD layout, with correct dates for each week."""
    WEEK=2
    DATE_TITLE="JANUARY 25--29, 2027"
    WEEK_SUBTITLE="Lines and planes / January 25--29"
    LESSON_LABEL="CLASS 01 -- GEOMETRY"
    COVER_TITLE="BUILD GEOMETRIC REASONING"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 02"
    HUD_SUBTITLE="Lines and planes / January 25--29"

    def institutional_cover(self):
        # Do not reuse the old hard-coded Week01 cover dates.
        if not self.LOGO.exists():
            raise FileNotFoundError(f"Authentic IJR PNG required: {self.LOGO}")
        logo=ImageMobject(str(self.LOGO)).scale_to_fit_height(2.17)
        logo.to_edge(UP,buff=.33)
        school=self.text(self.INSTITUTION,27,BOLD,DARK)
        subject=self.text("GEOMETRY 8",51,BOLD,DARK)
        period=self.text(f"2027 -- QUARTER 1 -- WEEK {self.WEEK:02d}",26,BOLD,SKETCH)
        dates=self.text(self.DATE_TITLE,25,BOLD,POSITIVE)
        heading=self.text(self.COVER_TITLE,30,BOLD,DARK)
        section=self.text(self.LESSON_LABEL,24,BOLD,POSITIVE)
        teacher=self.text(f"Teacher: {self.TEACHER}",23,NORMAL,MID)
        lineA=Line(LEFT*5.4,RIGHT*5.4,color=SKETCH,stroke_width=2.4)
        lineB=Line(LEFT*4.2,RIGHT*4.2,color=LIGHT,stroke_width=1.3)
        all_parts=VGroup(school,subject,period,dates,lineA,heading,section,lineB,teacher)
        all_parts.arrange(DOWN,buff=.13)
        all_parts.next_to(logo,DOWN,buff=.09)
        if all_parts.get_bottom()[1]<-3.53:
            all_parts.scale_to_fit_height(5.10)
            all_parts.next_to(logo,DOWN,buff=.09)
        all_items=[logo,*all_parts]
        for o in all_items: self.add_fixed_in_frame_mobjects(o)
        self.play(FadeIn(logo),Write(school),run_time=1.15)
        self.play(Write(subject),Write(period),run_time=1.25)
        self.play(Write(dates),Create(lineA),run_time=.85)
        self.play(Write(heading),Write(section),run_time=1.40)
        self.play(Create(lineB),Write(teacher),run_time=.85)
        self.wait(3.6)
        self.play(*[FadeOut(o) for o in all_items],run_time=.74)
        for o in all_items:
            self.remove_fixed_in_frame_mobjects(o)
            self.remove(o)

    def begin(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()

    def section(self,num,tag,title,subtitle):
        self.chapter(num,tag,title,subtitle)

    def show(self,*objects,seconds=1.2):
        self.register(*objects)
        self.play(*[Create(o) for o in objects],run_time=seconds)

    def phrase(self,s,x=0,y=-2.00,size=31,color=DARK,width=12.2,bold=False):
        t=self.big_text(s,x,y,size,color,width,bold)
        self.appearance(t,time=.92)
        return t

    def mathline(self,latex,x,y,size=48,color=POSITIVE,width=12.1):
        obj=self.big_math(latex,x,y,size,color,width)
        self.appearance(obj,time=1.15)
        return obj

    def callout(self,s,delay=4.2):
        self.caption(s)
        self.watch(delay)

    def arrowline(self,x1,y1,x2,y2,color=SKETCH,width=4.3):
        return DoubleArrow(point(x1,y1),point(x2,y2),
                           color=color,stroke_width=width,buff=0,
                           max_tip_length_to_length_ratio=.105)

    def plane_model(self,cx=-3.0,cy=-.35,scale=1.0,color=SKETCH):
        # Finite parallelogram is a SYMBOL of an infinite mathematical plane.
        verts=[point(cx-2.25*scale,cy-.82*scale),
               point(cx+1.16*scale,cy-.82*scale),
               point(cx+2.22*scale,cy+.90*scale),
               point(cx-1.18*scale,cy+.90*scale)]
        return Polygon(*verts,stroke_color=color,stroke_width=4,
                       fill_color=color,fill_opacity=.075)

    def guided_check(self,items,answers,first_num):
        self.section(first_num,"PAIR CHECK / REASON","JUSTIFY EACH DIAGRAM",
                     "Identify its defining property before naming the object.")
        for i,s in enumerate(items):
            self.phrase(s,0,.81-i*.76,30,DARK,12.55)
        self.callout("Stop and justify your classification in pairs.",7.5)
        self.stage_clear()
        self.set_phase(first_num+1,"ANSWERS / EXPLAIN",POSITIVE)
        for i,s in enumerate(answers):
            self.phrase(s,0,.85-i*.75,33,POSITIVE,11.9,True)
            self.watch(.65)
        self.callout("Explain why each answer satisfies the definition.",3.2)


# =============================================================================
# WEEK 02 — LINES, PLANES, SPATIAL RELATIONSHIPS
# =============================================================================

class Geometry8W02_Class01_LinePlane(Geometry8WeekCAD):
    WEEK=2
    DATE_TITLE="JANUARY 25--29, 2027"
    LESSON_LABEL="CLASS 01 -- LINES AND PLANE RELATIONSHIPS"
    COVER_TITLE="HOW LINES AND PLANES RELATE"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 02"
    HUD_SUBTITLE="Lines, planes and relations / January 25--29"

    def construct(self):
        self.begin()
        self.room_models()
        self.line_configurations()
        self.parallel_vs_perpendicular()
        self.line_and_plane()
        self.guided_check([
           "1. Two lines that never meet in the same plane.",
           "2. Two lines meeting at a 90-degree angle.",
           "3. Two names for the exact same infinite line."
        ],["1. PARALLEL","2. PERPENDICULAR","3. COINCIDENT"],5)
        self.exit_review("IDENTIFY RELATIONS, NOT JUST DRAWINGS",
                         "Parallel, intersecting, perpendicular, coincident.")

    def room_models(self):
        self.section(1,"CLASSROOM / OBSERVE","GEOMETRY IN A CLASSROOM",
                     "Edges of desks, walls and doors suggest geometric relations.")
        frame=Rectangle(width=8.8,height=3.02,color=LIGHT,
                        stroke_width=2.4).move_to([0,-.51,0])
        shelf1=Line(point(-3.8,-.06),point(3.9,-.06),
                    color=SKETCH,stroke_width=5)
        shelf2=Line(point(-3.8,-1.14),point(3.9,-1.14),
                    color=SKETCH,stroke_width=5)
        pillar=Line(point(1.28,.86),point(1.28,-1.88),
                    color=POSITIVE,stroke_width=5)
        self.show(frame,shelf1,shelf2,seconds=2.05)
        self.show(pillar,seconds=1.12)
        mark=Square(side_length=.31,stroke_color=POSITIVE,
                    stroke_width=3).move_to([1.435,-.215,0])
        self.show(mark,seconds=.8)
        self.phrase("PARALLEL EDGES", -3.2,-2.14,27,SKETCH,4.2,True)
        self.phrase("RIGHT ANGLE",2.35,-2.14,27,POSITIVE,4.1,True)
        self.callout("Real edges are finite; mathematical lines extend indefinitely.",4.6)

    def line_configurations(self):
        self.section(2,"FOUR RELATIONS","COMPARE THE SAME TWO LINES",
                     "Use arrows to distinguish an ideal line from a short segment.")
        samples=[
          ("INTERSECTING",(-3.0,.10,.6),((-4.2,.36),(-.55,-.95)),
           ((-4.2,-1.02),(-.65,.52))),
          ("PARALLEL",(3.0,.10,.6),((1.15,.30),(5.70,.30)),
           ((1.15,-.84),(5.70,-.84))),
        ]
        for name,_,a,b in samples:
            x= -2.85 if name=="INTERSECTING" else 3.10
            first=self.arrowline(*a[0],*a[1],color=DARK)
            second=self.arrowline(*b[0],*b[1],color=SKETCH)
            self.show(first,second,seconds=1.65)
            self.phrase(name,x,-1.88,29,POSITIVE,5.4,True)
        self.callout("Crossing lines intersect; parallel lines remain disjoint in their plane.",4.3)
        self.stage_clear()
        self.set_phase(3,"SAME OR ORTHOGONAL",SKETCH)
        h=self.arrowline(-5.4,-.45,-.4,-.45,color=DARK)
        v=self.arrowline(-2.9,-1.72,-2.9,.85,color=SKETCH)
        self.show(h,v,seconds=1.55)
        square=Square(side_length=.34,color=POSITIVE,
                      stroke_width=2.5).move_to([-2.73,-.28,0])
        self.show(square,seconds=.65)
        self.phrase("PERPENDICULAR", -2.83,-2.09,30,POSITIVE,5.4,True)
        coinc=self.arrowline(1.12,-.48,5.65,-.48,color=MID)
        same=self.arrowline(1.12,-.48,5.65,-.48,color=SKETCH,width=2.9)
        self.show(coinc,seconds=1.08)
        self.play(ReplacementTransform(coinc.copy(),same),run_time=1.12)
        self.register(same)
        self.phrase("COINCIDENT",3.36,-2.09,30,POSITIVE,4.7,True)
        self.callout("Coincident lines share all points, not just one intersection.",4.2)

    def parallel_vs_perpendicular(self):
        self.section(4,"RELATION / CHECK","RIGHT ANGLES NEED EVIDENCE",
                     "A crossing point alone does not prove perpendicularity.")
        center=point(-2.45,-.60)
        h=self.arrowline(-5.35,-.60,.50,-.60,color=DARK)
        ray=Line(center,center+point(1.22,1.60),color=SKETCH,stroke_width=5)
        self.show(h,ray,seconds=1.55)
        label=self.phrase("OBLIQUE INTERSECTION",-2.50,-2.08,
                          29,SKETCH,5.75,True)
        self.watch(1.3)
        self.play(Rotate(ray,angle=np.arctan2(1.60,1.22),
                         about_point=center),run_time=2.25,rate_func=smooth)
        # Ray now points to 2*atan2(...) and is not 90. Correct by animate
        # a known adjustment from the initial 52.7 degrees to 90 degrees.
        self.play(Rotate(ray,angle=(PI/2-2*np.arctan2(1.60,1.22)),
                         about_point=center),run_time=1.75)
        sq=Square(side_length=.35,color=POSITIVE,
                  stroke_width=2.8).move_to(center+point(.175,.175))
        self.show(sq,seconds=.75)
        self.phrase("Now the angle is 90 degrees.",2.98,-.48,
                    32,POSITIVE,5.1,True)
        self.callout("Look for an exact right angle, not an almost-square drawing.",4.6)

    def line_and_plane(self):
        self.section(5,"LINE / PLANE","DRAW A LINE WITHIN A PLANE",
                     "The parallelogram is a finite drawing of a boundless plane.")
        poly=self.plane_model(cx=-2.45,cy=-.48,scale=1.05)
        self.play(DrawBorderThenFill(poly),run_time=1.9)
        self.register(poly)
        line=Line(point(-4.2,-.40),point(-.38,-.40),
                  stroke_width=5,color=POSITIVE)
        self.show(line,seconds=1.17)
        pt=Dot(point(-2.4,-.40),radius=.15,color=DARK)
        self.play(FadeIn(pt),run_time=.65);self.register(pt)
        self.phrase("LINE CONTAINED IN A PLANE",2.71,.23,32,SKETCH,5.3,True)
        self.mathline(r"\ell\subset\alpha",2.68,-.67,62,POSITIVE,5.0)
        self.phrase("Other lines may intersect or be parallel to a plane.",
                    2.69,-1.65,28,MID,5.5)
        self.callout("Use a sketch to justify the spatial relation you claim.",4.8)


class Geometry8W02_Class02_SpatialReasoning(Geometry8WeekCAD):
    WEEK=2
    DATE_TITLE="JANUARY 25--29, 2027"
    LESSON_LABEL="CLASS 02 -- REASONING WITH SPATIAL DIAGRAMS"
    COVER_TITLE="CLASSIFY, CHECK AND JUSTIFY"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 02"
    HUD_SUBTITLE="Spatial diagrams and counterexamples / January 25--29"

    def construct(self):
        self.begin()
        self.invariants()
        self.counterexample_intersection()
        self.coincidence_check()
        self.plane_cases()
        self.guided_check([
           "1. Two crossing lines form a 70-degree angle.",
           "2. Two infinite straight lines share every point.",
           "3. A line is entirely drawn on a plane."
        ],["1. INTERSECTING, NOT PERPENDICULAR",
           "2. COINCIDENT",
           "3. THE LINE LIES IN THE PLANE"],5)
        self.exit_review("A DIAGRAM SUPPORTS A CLAIM",
                         "Show a right angle, shared points or a parallel direction.")

    def invariants(self):
        self.section(1,"MEANING / PROPERTIES","WHAT MUST STAY TRUE?",
                     "Correct classification depends on properties, not appearance.")
        rows=[
          ("PARALLEL","Same plane, never intersect",SKETCH),
          ("PERPENDICULAR","Angle at intersection is 90 degrees",POSITIVE),
          ("COINCIDENT","All geometric points are shared",DARK),
        ]
        for i,(head,detail,color) in enumerate(rows):
            y=.78-1.0*i
            ln=Line(point(-5.4,y-.35),point(5.4,y-.35),color=LIGHT,stroke_width=2)
            self.show(ln,seconds=.38)
            self.phrase(head,-3.20,y,34,color,4.6,True)
            self.phrase(detail,2.55,y,27,DARK,6.0)
            self.watch(.85)
        self.callout("Draw counterexamples whenever a classification is uncertain.",4.4)

    def counterexample_intersection(self):
        self.section(2,"COUNTEREXAMPLE","INTERSECTING DOES NOT MEAN 90 DEGREES",
                     "Rotate one line while its intersection point remains fixed.")
        c=point(-2.35,-.39)
        base=self.arrowline(-5.0,-.39,.30,-.39,color=DARK)
        pivot=self.arrowline(-4.20,-1.92,-.50,1.16,color=SKETCH)
        theta=ValueTracker(0)
        self.show(base,pivot,seconds=1.5)
        self.play(Rotate(pivot,angle=20*DEGREES,about_point=c),
                  run_time=2.1,rate_func=smooth)
        self.phrase("THE LINES STILL INTERSECT",3.04,.42,32,SKETCH,5.65,True)
        self.phrase("ONLY 90 DEGREES IS PERPENDICULAR",3.04,-.47,
                    29,POSITIVE,5.7,True)
        self.callout("One meeting point is insufficient evidence of perpendicularity.",5.3)

    def coincidence_check(self):
        self.section(3,"INFINITE OBJECTS","COINCIDENT IS NOT PARALLEL",
                     "Two different names can describe the exact same line.")
        line1=self.arrowline(-5.3,.02,5.3,.02,color=DARK,width=6)
        line2=self.arrowline(-5.3,-1.18,5.3,-1.18,color=SKETCH,width=4)
        self.show(line1,line2,seconds=1.5)
        label=self.phrase("SEPARATE PARALLEL LINES",0,-1.90,32,MID,10,True)
        self.watch(1.4)
        self.play(line2.animate.shift(UP*1.2),run_time=2.5,rate_func=smooth)
        same=self.phrase("NOW THEY ARE COINCIDENT",0,-1.90,
                         33,POSITIVE,10.3,True)
        self.callout("A single infinitely long set of points may have two labels.",5.4)

    def plane_cases(self):
        self.section(4,"MODEL / CHECK","A LINE CAN LIE IN OR MEET A PLANE",
                     "The edge of the drawn parallelogram is not an edge of the plane.")
        left=self.plane_model(cx=-3.15,cy=-.20,scale=.78)
        right=self.plane_model(cx=3.12,cy=-.20,scale=.78)
        self.play(DrawBorderThenFill(left),
                  DrawBorderThenFill(right),run_time=2.1)
        self.register(left,right)
        contained=Line(point(-4.21,-.36),point(-2.0,-.36),
                       color=POSITIVE,stroke_width=5.5)
        pierce=Line(point(3.12,-1.58),point(3.12,.95),
                    color=SKETCH,stroke_width=5)
        self.show(contained,pierce,seconds=1.68)
        self.play(FadeIn(Dot(point(3.12,-.20),radius=.17,color=NEGATIVE)),
                  run_time=.60)
        self.phrase("CONTAINED IN PLANE", -3.15,-2.04,28,POSITIVE,5.9,True)
        self.phrase("INTERSECTS AT A POINT",3.10,-2.04,27,SKETCH,5.6,True)
        self.callout("These are schematic 2D views of distinct spatial relationships.",4.7)


# =============================================================================
# WEEK 03 — COMPASS AND STRAIGHTEDGE CONSTRUCTIONS
# =============================================================================

class Geometry8W03_Class01_Instruments(Geometry8WeekCAD):
    WEEK=3
    DATE_TITLE="FEBRUARY 1--5, 2027"
    LESSON_LABEL="CLASS 01 -- INSTRUMENTS AND BASIC OPERATIONS"
    COVER_TITLE="CONSTRUCT AND COPY GEOMETRIC LENGTHS"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 03"
    HUD_SUBTITLE="Straightedge and compass / February 1--5"

    def construct(self):
        self.begin()
        self.tools()
        self.segment()
        self.compass_transfer()
        self.procedure()
        self.exit_review("ACCURATE CONSTRUCTION IS REPEATABLE",
                         "A fixed compass opening transfers an equal distance.")

    def tools(self):
        self.section(1,"TOOLS / PURPOSE","RULER, STRAIGHTEDGE AND COMPASS",
                     "A marked ruler measures; an unmarked edge guides straight lines.")
        straight=RoundedRectangle(width=5.1,height=.45,
              corner_radius=.06,color=SKETCH,stroke_width=3,
              fill_color=MODEL,fill_opacity=.4).move_to([-3.36,-.25,0])
        marked=RoundedRectangle(width=5.1,height=.45,
              corner_radius=.06,color=SKETCH,stroke_width=3,
              fill_color=MODEL,fill_opacity=.4).move_to([-3.36,-1.14,0])
        ticks=VGroup(*[Line(point(-5.64+i*.45,-.91),
                            point(-5.64+i*.45,-.91-(.20 if i%2 else .32)),
                            color=MID,stroke_width=2)
                        for i in range(11)])
        self.show(straight,marked,ticks,seconds=1.8)
        self.phrase("UNMARKED STRAIGHTEDGE",-3.39,.55,25,DARK,5.55,True)
        self.phrase("MARKED RULER",-3.39,-1.75,26,SKETCH,5.25,True)
        center=point(3.30,-.40)
        radius=1.30
        theta=ValueTracker(.01)
        circle=always_redraw(lambda: Arc(
             radius=radius,start_angle=0,angle=theta.get_value(),
             arc_center=center,color=SKETCH,stroke_width=4.3))
        arm=always_redraw(lambda: Line(
            center,center+radius*point(np.cos(theta.get_value()),
                                      np.sin(theta.get_value())),
            color=POSITIVE,stroke_width=4.0))
        pivot=Dot(center,radius=.13,color=DARK)
        self.add(circle,arm,pivot);self.register(circle,arm,pivot)
        self.play(theta.animate.set_value(TAU),run_time=4.3,rate_func=linear)
        self.phrase("COMPASS: EQUAL RADIUS",3.30,-2.08,28,POSITIVE,5.3,True)
        self.callout("Keep the compass opening fixed when transferring a length.",4.4)

    def segment(self):
        self.section(2,"CONSTRUCT / SEGMENT","MARK A GIVEN LENGTH",
                     "Example: draw segment AB with a measured length of 4 cm.")
        # Diagram is schematic; endpoints and relative lengths are consistent.
        baseline=Line(point(-4.55,-.68),point(4.55,-.68),
                      stroke_width=2.2,color=LIGHT)
        A=point(-2.90,-.68);B=point(1.10,-.68)
        pencil=Dot(A,radius=.17,color=POSITIVE)
        self.show(baseline,seconds=1.05)
        self.play(FadeIn(pencil),run_time=.45);self.register(pencil)
        trace=Line(A,B,color=SKETCH,stroke_width=5)
        self.show(trace,seconds=2.3)
        self.play(pencil.animate.move_to(B),run_time=1.5,rate_func=smooth)
        for p,name in ((A,"A"),(B,"B")):
            dot=Dot(p,radius=.135,color=DARK)
            self.play(FadeIn(dot),run_time=.35);self.register(dot)
            self.phrase(name,p[0],-.27,29,DARK,1.05,True)
        self.mathline(r"\overline{AB}=4\,\mathrm{cm}",0,-1.65,50,POSITIVE,11)
        self.callout("Step 1: mark A. Step 2: mark 4 cm. Step 3: label B.",5.2)

    def compass_transfer(self):
        self.section(3,"COMPASS / TRANSFER","COPY A SEGMENT LENGTH",
                     "Keep the same radius while relocating the compass center.")
        A=point(-4.35,.44);B=point(-1.27,.44)
        C=point(-4.35,-1.23);D=point(-1.27,-1.23)
        first=Line(A,B,stroke_width=5.2,color=SKETCH)
        guide=Line(C,point(1.10,-1.23),stroke_width=2.9,color=LIGHT)
        self.show(first,guide,seconds=1.6)
        for p,label,dy in ((A,"A",.35),(B,"B",.35),(C,"C",-.33)):
            dot=Dot(p,radius=.13,color=DARK)
            self.play(FadeIn(dot),run_time=.3);self.register(dot)
            self.phrase(label,p[0],p[1]+dy,26,SKETCH,1.1,True)
        radius=np.linalg.norm(B-A)
        move=ValueTracker(.01)
        arc=always_redraw(lambda:Arc(radius=radius,start_angle=0,
             angle=move.get_value(),arc_center=C,color=POSITIVE,
             stroke_width=4))
        self.add(arc);self.register(arc)
        self.play(move.animate.set_value(.48),run_time=2.8,rate_func=smooth)
        endpoint=Dot(D,radius=.16,color=POSITIVE)
        copy=Line(C,D,color=POSITIVE,stroke_width=5.0)
        self.show(copy,seconds=1.9)
        self.play(FadeIn(endpoint),run_time=.48);self.register(endpoint)
        self.phrase("D",D[0],D[1]-.34,26,POSITIVE,1.0,True)
        self.mathline(r"AB=CD",3.31,-.10,62,POSITIVE,5.3)
        self.callout("The fixed radius proves the two segments have equal length.",5.6)

    def procedure(self):
        self.section(4,"STEPS / VERIFY","WRITE A REPEATABLE PROCEDURE",
                     "A peer should reproduce your drawing from your written steps.")
        steps=[
          "1. Choose and label your starting point.",
          "2. Measure the required distance once.",
          "3. Keep the compass radius unchanged.",
          "4. Mark the intersection and name it.",
          "5. Verify length and explain why it matches."
        ]
        for i,s in enumerate(steps):
            self.phrase(s,0,1.02-.70*i,31,DARK,12.8)
            self.watch(.8)
        self.callout("Peer check: agree on the same construction and labels.",5.1)


class Geometry8W03_Class02_Constructions(Geometry8WeekCAD):
    WEEK=3
    DATE_TITLE="FEBRUARY 1--5, 2027"
    LESSON_LABEL="CLASS 02 -- PERPENDICULAR AND PARALLEL"
    COVER_TITLE="BUILD LINES WITH COMPASS ARCS"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 03"
    HUD_SUBTITLE="Perpendicular bisectors and parallels / February 1--5"

    def construct(self):
        self.begin()
        self.bisector()
        self.double_perpendicular()
        self.error_check()
        self.guided_check([
          "1. Must the compass radius exceed half of AB?",
          "2. What is the angle at a perpendicular crossing?",
          "3. Lines both perpendicular to m are..."
        ],["1. YES, TO OBTAIN TWO ARC INTERSECTIONS",
           "2. EXACTLY 90 DEGREES",
           "3. PARALLEL TO EACH OTHER"],4)
        self.exit_review("CONSTRUCTIONS NEED A REASON",
                         "Equal-radius arcs give equal distances and right angles.")

    def bisector(self):
        self.section(1,"STEP BY STEP","PERPENDICULAR BISECTOR OF AB",
                     "Use equal-radius arcs; radius must exceed half the segment.")
        A=point(-3.10,-.37); B=point(.90,-.37); M=(A+B)/2
        line=Line(A,B,color=DARK,stroke_width=5)
        self.show(line,seconds=1.34)
        for p,n in ((A,"A"),(B,"B")):
            dot=Dot(p,radius=.13,color=SKETCH)
            self.play(FadeIn(dot),run_time=.35);self.register(dot)
            self.phrase(n,p[0],.02,28,SKETCH,1,True)
        r=2.5
        angle=np.arctan2(1.5,2.0)
        arcs=[]
        for center,angles in (
            (A,[angle,-angle]),(B,[np.pi-angle,np.pi+angle])
        ):
            for t in angles:
                arcs.append(Arc(radius=r,start_angle=t-.17,
                    angle=.34,arc_center=center,
                    color=SKETCH,stroke_width=4))
        for arc in arcs:
            self.show(arc,seconds=.72)
        top=point(M[0],M[1]+1.5)
        bot=point(M[0],M[1]-1.5)
        self.play(FadeIn(Dot(top,radius=.15,color=POSITIVE)),
                  FadeIn(Dot(bot,radius=.15,color=POSITIVE)),
                  run_time=.62)
        bis=Line(top,bot,color=POSITIVE,stroke_width=5)
        self.show(bis,seconds=1.7)
        mark=Square(side_length=.30,color=POSITIVE,
                    stroke_width=2.2).move_to(M+point(.15,.15))
        self.show(mark,seconds=.68)
        self.mathline(r"AM=MB,\quad \ell\perp AB",3.62,-.37,43,POSITIVE,5.45)
        self.callout("Both arc intersections are equally distant from A and B.",5.1)

    def double_perpendicular(self):
        self.section(2,"TWO RIGHT ANGLES","CONSTRUCT A PARALLEL THROUGH P",
                     "Two lines perpendicular to one line are parallel to each other.")
        l=self.arrowline(-5.54,-1.22,5.55,-1.22,color=DARK,width=4.4)
        self.show(l,seconds=1.3)
        P=point(-2.0,.80)
        p=Dot(P,radius=.14,color=SKETCH)
        self.play(FadeIn(p),run_time=.52);self.register(p)
        self.phrase("P",P[0]-.35,P[1]+.23,30,SKETCH,1.1,True)
        perpendicular=self.arrowline(-2.0,-1.92,-2.0,1.04,
                                    color=SKETCH,width=4.7)
        self.show(perpendicular,seconds=1.48)
        right1=Square(side_length=.30,color=POSITIVE,
                      stroke_width=2).move_to([-1.85,-1.07,0])
        self.show(right1,seconds=.65)
        parallel=self.arrowline(-5.54,.80,5.55,.80,
                               color=POSITIVE,width=4.7)
        self.show(parallel,seconds=1.72)
        right2=Square(side_length=.30,color=POSITIVE,
                      stroke_width=2).move_to([-1.85,.95,0])
        self.show(right2,seconds=.65)
        self.mathline(r"\ell\parallel n",3.65,-.30,55,POSITIVE,4.4)
        self.callout("Guided construction: use compass arcs to establish both 90-degree angles.",5.2)

    def error_check(self):
        self.section(3,"PRECISION / VALIDATE","WHY CAN A CONSTRUCTION FAIL?",
                     "A compass radius smaller than half AB yields no shared arc points.")
        A=point(-3.00,-.40); B=point(1.50,-.40);r=1.60
        segment=Line(A,B,color=DARK,stroke_width=4.9)
        self.show(segment,seconds=1.2)
        cA=Circle(radius=r,color=NEGATIVE,stroke_width=3.2).move_to(A)
        cB=Circle(radius=r,color=NEGATIVE,stroke_width=3.2).move_to(B)
        self.show(cA,cB,seconds=1.7)
        self.mathline(r"r<\frac{AB}{2}",3.70,.36,59,NEGATIVE,5.1)
        self.phrase("NO TWO ARC INTERSECTIONS",3.65,-.81,
                    30,NEGATIVE,5.3,True)
        self.callout("Increase both radii equally to more than half the segment.",5.0)


# =============================================================================
# WEEK 04 — ANGLES: MEASUREMENT, NOTATION AND TYPES
# =============================================================================

class Geometry8W04_Class01_Angles(Geometry8WeekCAD):
    WEEK=4
    DATE_TITLE="FEBRUARY 8--12, 2027"
    LESSON_LABEL="CLASS 01 -- ANGLE CONCEPTS AND CLASSIFICATION"
    COVER_TITLE="HOW DO WE NAME AND CLASSIFY AN ANGLE?"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 04"
    HUD_SUBTITLE="Angles, vertices and types / February 8--12"

    def construct(self):
        self.begin()
        self.terms()
        self.classify()
        self.direction()
        self.guided_check([
          "1. The vertex of angle ABC is...",
          "2. An angle of 125 degrees is...",
          "3. An angle of 235 degrees is..."
        ],["1. POINT B","2. OBTUSE","3. REFLEX"],4)
        self.exit_review("VERTEX, RAYS, ROTATION, MEASURE",
                         "Always name the vertex and justify the angle type.")

    def terms(self):
        self.section(1,"DEFINE / NAME","AN ANGLE HAS TWO RAYS AND A VERTEX",
                     "The shared endpoint B is the vertex of angle ABC.")
        B=point(-3.00,-1.17)
        A=B+point(3.60,0)
        C=B+point(2.03,2.42)
        one=Arrow(B,A,buff=0,stroke_width=4.7,color=DARK)
        two=Arrow(B,C,buff=0,stroke_width=4.7,color=SKETCH)
        self.show(one,two,seconds=1.85)
        self.play(FadeIn(Dot(B,radius=.16,color=POSITIVE)),run_time=.47)
        for pt,label,dx,dy in ((B,"B",-.30,-.29),
                               (A,"A",.26,-.13),(C,"C",.18,.30)):
            self.phrase(label,pt[0]+dx,pt[1]+dy,28,SKETCH,1,True)
        arc=Arc(radius=.83,start_angle=0,angle=np.arctan2(2.42,2.03),
                arc_center=B,color=POSITIVE,stroke_width=4)
        self.show(arc,seconds=1.22)
        self.mathline(r"\angle ABC",3.30,.10,76,POSITIVE,5.4)
        self.phrase("The middle letter names the vertex.",3.40,-1.16,29,MID,5.5)
        self.callout("A ray is an arm of the angle; its length does not determine the measure.",4.7)

    def classify(self):
        self.section(2,"MEASURE / SORT","WATCH THE RAY TURN",
                     "Angle classification uses the angle measure in degrees.")
        O=point(-2.64,-.81)
        theta=ValueTracker(35*DEGREES)
        rad=2.32
        baseline=Arrow(O,O+RIGHT*rad,buff=0,color=DARK,stroke_width=4.6)
        arm=always_redraw(lambda:Arrow(
           O,O+rad*point(np.cos(theta.get_value()),
                         np.sin(theta.get_value())),
           buff=0,color=SKETCH,stroke_width=4.6))
        arc=always_redraw(lambda:Arc(
           radius=.78,start_angle=0,angle=max(.001,theta.get_value()),
           arc_center=O,color=POSITIVE,stroke_width=4))
        self.show(baseline,seconds=.9)
        self.add(arm,arc);self.register(arm,arc)
        kind=self.phrase("ACUTE",3.0,.58,40,SKETCH,4.8,True)
        number=self.mathline(r"35^\circ",3.0,-.35,70,POSITIVE,4.9)
        for degrees,label in ((90,"RIGHT"),(125,"OBTUSE"),
                              (180,"STRAIGHT"),(235,"REFLEX")):
            nextkind=self.big_text(label,3.0,.58,40,SKETCH,4.9,True)
            nextnum=self.big_math(str(degrees)+r"^\circ",3.0,-.35,
                                  70,POSITIVE,4.9)
            self.play(theta.animate.set_value(degrees*DEGREES),
                      ReplacementTransform(kind,nextkind),
                      ReplacementTransform(number,nextnum),
                      run_time=2.35,rate_func=smooth)
            kind,number=nextkind,nextnum
            self.watch(1.4)
        self.callout("Acute: below 90; right: 90; obtuse: between 90 and 180.",4.2)

    def direction(self):
        self.section(3,"DIRECTION / MAGNITUDE","DIRECTION IS NOT ANGLE SIZE",
                     "A signed turn is different from its nonnegative magnitude.")
        centers=[point(-3.15,-.42),point(3.16,-.42)]
        for i,c in enumerate(centers):
            h=Line(c,c+RIGHT*1.75,color=DARK,stroke_width=4.5)
            direction=60*DEGREES*(1 if i==0 else -1)
            v=Line(c,c+1.75*point(np.cos(direction),np.sin(direction)),
                   color=SKETCH,stroke_width=4.5)
            arc=Arc(radius=.65,start_angle=0,angle=direction,
                    arc_center=c,color=POSITIVE,stroke_width=4)
            self.show(h,v,arc,seconds=1.48)
            self.phrase("COUNTERCLOCKWISE" if i==0 else "CLOCKWISE",
                        c[0],-1.97,27,SKETCH,5.55,True)
        self.phrase("Both rotations have magnitude 60 degrees.",0,.97,
                    30,POSITIVE,11.4,True)
        self.callout("With signed rotations, the directions have opposite signs.",4.9)


class Geometry8W04_Class02_Protractor(Geometry8WeekCAD):
    WEEK=4
    DATE_TITLE="FEBRUARY 8--12, 2027"
    LESSON_LABEL="CLASS 02 -- MEASURE AND CONSTRUCT ANGLES"
    COVER_TITLE="READ AND DRAW ANGLES WITH A PROTRACTOR"
    HUD_TITLE="GEOMETRY 8 -- 2027 -- QUARTER 1 -- WEEK 04"
    HUD_SUBTITLE="Measure, construct, verify / February 8--12"

    def construct(self):
        self.begin()
        self.protractor()
        self.measure_angle()
        self.construct_angle()
        self.checkpoint()
        self.next_topic()
        self.exit_review("PLACE, ALIGN, READ, DRAW, VERIFY",
                         "Zero line at the arm, center on the vertex.")

    def half_protractor(self,c,rad=1.97):
        arc=Arc(radius=rad,start_angle=0,angle=PI,
                arc_center=c,color=SKETCH,stroke_width=4.5)
        base=Line(c+LEFT*rad,c+RIGHT*rad,color=DARK,stroke_width=3.6)
        ticks=VGroup()
        for deg in range(0,181,10):
            a=deg*DEGREES
            R=rad;inner=rad-(.25 if deg%30==0 else .13)
            ticks.add(Line(c+R*point(np.cos(a),np.sin(a)),
                          c+inner*point(np.cos(a),np.sin(a)),
                          color=MID,stroke_width=2.1))
        self.show(arc,base,ticks,seconds=2.15)
        return arc,base,ticks

    def protractor(self):
        self.section(1,"TOOL / ALIGN","HOW DOES A PROTRACTOR WORK?",
                     "Center on vertex, zero on one ray, then read the correct scale.")
        O=point(-1.90,-1.28)
        self.half_protractor(O,rad=2.21)
        for deg in (0,30,60,90,120,150,180):
            a=deg*DEGREES
            center=O+1.63*point(np.cos(a),np.sin(a))
            self.phrase(str(deg),center[0],center[1],
                        22,SKETCH,1.0,True)
        center=Dot(O,radius=.15,color=POSITIVE)
        self.play(FadeIn(center),run_time=.55);self.register(center)
        self.phrase("CENTER ON VERTEX",3.60,.55,30,DARK,5.8,True)
        self.phrase("ZERO ON FIRST RAY",3.60,-.35,30,SKETCH,5.8,True)
        self.callout("Read from the zero on the arm you aligned, not the other scale.",5.1)

    def measure_angle(self):
        self.section(2,"READ / MEASURE","MEASURE THE ROTATION",
                     "The zero ray is fixed. Follow the second ray to its scale mark.")
        O=point(-2.22,-1.14);r=2.10
        base=Line(O,O+RIGHT*r,color=DARK,stroke_width=5)
        theta=ValueTracker(0)
        moving=always_redraw(lambda:Line(
           O,O+r*point(np.cos(theta.get_value()),np.sin(theta.get_value())),
           color=SKETCH,stroke_width=5))
        arc=always_redraw(lambda:Arc(radius=.73,start_angle=0,
                 angle=max(.001,theta.get_value()),
                 arc_center=O,color=POSITIVE,stroke_width=4))
        self.show(base,seconds=.89)
        self.add(moving,arc);self.register(moving,arc)
        self.play(theta.animate.set_value(65*DEGREES),
                  run_time=3.1,rate_func=smooth)
        self.mathline(r"m\angle AOB=65^\circ",3.24,-.15,
                      48,POSITIVE,5.6)
        self.phrase("65 degrees is ACUTE.",3.25,-1.18,30,DARK,5.55,True)
        self.callout("Check that the protractor's 0-degree baseline matches OA.",4.9)

    def construct_angle(self):
        self.section(3,"CONSTRUCT / 120","DRAW A GIVEN OBTUSE ANGLE",
                     "Draw a baseline, locate the 120-degree mark, then trace the ray.")
        O=point(-2.40,-1.16);r=2.18
        baseline=Line(O,O+RIGHT*r,color=DARK,stroke_width=5)
        self.show(baseline,seconds=1.18)
        self.phrase("STEP 1: DRAW THE ZERO RAY",3.10,.82,
                    27,SKETCH,5.9,True)
        circle=Arc(radius=r,start_angle=0,angle=PI,arc_center=O,
                   stroke_color=LIGHT,stroke_width=2.6)
        self.show(circle,seconds=1.52)
        direction=120*DEGREES
        end=O+r*point(np.cos(direction),np.sin(direction))
        mark=Dot(end,radius=.16,color=POSITIVE)
        self.play(FadeIn(mark),run_time=.5);self.register(mark)
        self.phrase("STEP 2: FIND 120 DEGREES",3.10,-.11,
                    27,SKETCH,5.9,True)
        ray=Line(O,end,color=SKETCH,stroke_width=5)
        self.show(ray,seconds=1.75)
        self.phrase("STEP 3: DRAW THE RAY",3.10,-1.06,
                    27,POSITIVE,5.7,True)
        anglearc=Arc(radius=.74,start_angle=0,angle=direction,
                     arc_center=O,color=POSITIVE,stroke_width=4)
        self.show(anglearc,seconds=1.05)
        self.callout("Verify both the magnitude and the starting zero direction.",5.3)

    def checkpoint(self):
        self.section(4,"MEASURE / CHECK","TRY THREE ANGLES",
                     "Identify their class and justify each measure.")
        specs=[(40,-3.9,"A"),(90,0,"B"),(140,3.9,"C")]
        for degree,x,name in specs:
            c=point(x,-.74);rad=1.28
            h=Line(c,c+RIGHT*rad,color=DARK,stroke_width=3.7)
            d=degree*DEGREES
            v=Line(c,c+rad*point(np.cos(d),np.sin(d)),
                   color=SKETCH,stroke_width=3.7)
            arc=Arc(radius=.48,start_angle=0,angle=d,
                    arc_center=c,color=POSITIVE,stroke_width=3.1)
            self.show(h,v,arc,seconds=1.05)
            self.phrase(name,x,-1.88,30,SKETCH,1.7,True)
        self.callout("Pause: classify A, B and C before revealing their angles.",7)
        for x,d,name in [(-3.9,40,"ACUTE"),(0,90,"RIGHT"),(3.9,140,"OBTUSE")]:
            self.phrase(f"{d} degrees - {name}",x,.82,27,POSITIVE,4.0,True)
        self.watch(4.2)

    def next_topic(self):
        self.section(5,"NEXT TOPIC / PREVIEW","ANGLE ADDITION COMES NEXT",
                     "A larger angle can be decomposed into adjacent parts.")
        O=point(-3,-1.17);r=2.40
        lines=[
          Line(O,O+r*point(np.cos(a*DEGREES),np.sin(a*DEGREES)),
               color=col,stroke_width=4.4)
          for a,col in [(0,DARK),(25,SKETCH),(60,POSITIVE)]
        ]
        self.show(*lines,seconds=1.66)
        arc1=Arc(radius=.73,start_angle=0,angle=25*DEGREES,
                 arc_center=O,color=SKETCH,stroke_width=3.5)
        arc2=Arc(radius=.73,start_angle=25*DEGREES,angle=35*DEGREES,
                 arc_center=O,color=POSITIVE,stroke_width=3.5)
        self.show(arc1,arc2,seconds=1.45)
        self.mathline(r"25^\circ+35^\circ=60^\circ",3.09,-.30,52,POSITIVE,6.0)
        self.callout("This is a preview; formal angle-addition problems follow later.",4.5)
