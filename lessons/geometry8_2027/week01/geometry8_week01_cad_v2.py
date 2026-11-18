#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEOMETRY 8 / 2027 / Q1 / WEEK 01 / V2 -- real CAD House format.

Exact authoritative teaching sequence:
Geometry_8_2027_P1.docx, Week 1, 19–22 January 2027.
Class 1: Course induction; notebook and drawing conventions; point, line,
         segment, ray, plane; labeled diagrams and their differences.
Class 2: Sets and logical diagrams; geometric sorting by dimensions,
         two-circle diagrams, membership and intersection with justification.
2026 Geometry 8 curriculum confirms both opening thematic axes.
Do NOT advance W2 line-plane relationships, W3 compass constructions, W4 angles.

This source intentionally imports the validated Geometry8Base CAD house design,
institutional logo PNG, fixed numbered HUD, Tex/MathTex and semantic palette.
Animations do NOT depend on generated or fake institutional imagery.
Compatible with ManimCE v0.20.1. Always render PQL before PQH.

  manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad_v2.py Geometry8W01_FoundationsV2
  manim -pql lessons/geometry8_2027/week01/geometry8_week01_cad_v2.py Geometry8W01_LogicalSetsV2
  manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad_v2.py Geometry8W01_FoundationsV2
  manim -pqh lessons/geometry8_2027/week01/geometry8_week01_cad_v2.py Geometry8W01_LogicalSetsV2
"""
from __future__ import annotations
import numpy as np
from manim import *
from geometry8_week01_cad import Geometry8Base
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, NEGATIVE, TERRAIN, SLAB


class Geometry8V2Base(Geometry8Base):
    """A projector-readable layer over the authentic CAD source, no redesign."""
    HUD_SUBTITLE = "Euclidean foundations  /  January 19--22"
    HUD_TITLE_SIZE = 30

    def heading(self,n,phase,title,subtitle):
        self.chapter(n,phase,title,subtitle)

    def big_text(self,s,x,y,size=35,color=DARK,width=12.8,bold=False):
        return self.put(s,(x,y),size,color,bold,width)

    def big_math(self,s,x,y,size=52,color=DARK,width=12.6):
        return self.eq(s,(x,y),size,color,width)

    def watch(self,seconds=4.2):
        """Real reading/observation pause; never claim the source dictates seconds."""
        self.wait(seconds)

    def add_show(self,*items,mode="create",duration=1.3):
        self.register(*items)
        effects=[FadeIn(m) if mode=="fade" else Create(m) for m in items]
        self.play(*effects,run_time=duration)

    def exit_review(self,first,second):
        self.stage_clear()
        self.set_phase(98,"EXPLAIN / VERIFY",POSITIVE)
        a=self.big_text(first,0,.65,43,POSITIVE,12.8,True)
        b=self.big_text(second,0,-.77,32,DARK,12.8)
        self.play(Write(a),run_time=1.4)
        self.play(Write(b),run_time=1.4)
        self.caption("Share one diagram, one definition, and one justification.")
        self.watch(7.0)
        self.stage_clear()
        self.footer_cleanup()


class Geometry8W01_FoundationsV2(Geometry8V2Base):
    """Week01, Class01: source-specific induction + rigorous geometry primitives."""
    LESSON_LABEL = "CLASS 01 -- INDUCTION AND GEOMETRIC OBJECTS"
    COVER_TITLE = "BUILD THE LANGUAGE OF GEOMETRY"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.course_conventions()
        self.a_point()
        self.line_ray_segment()
        self.plane()
        self.notation()
        self.model_and_counterexample()
        self.practice()
        self.exit_review("EVERY LABEL COMMUNICATES A PROPERTY",
                         "Point: location. Line: endless. Ray: one origin. Segment: two ends. Plane: flat.")

    def course_conventions(self):
        self.heading(1,"INDUCTION / DRAWING","HOW WE DRAW AND LABEL",
                     "Notebook conventions make a mathematical explanation readable.")
        # Big paper diagram: lines and labels assembled as an actual drawing.
        paper=RoundedRectangle(width=7.55,height=3.18,corner_radius=.13,
            fill_color=WHITE,fill_opacity=1,stroke_color=LIGHT,
            stroke_width=2.4).move_to([-1.64,-.62,0])
        border=Line([-5.18,.89,0],[1.88,.89,0],color=SKETCH,stroke_width=3)
        ruled=VGroup(*[
            Line([-5.17,y,0],[1.75,y,0],stroke_width=1.0,color=LIGHT)
            for y in (.44,-.07,-.58,-1.09,-1.60,-2.05)
        ])
        margin=Line([-4.48,.85,0],[-4.48,-2.14,0],stroke_width=1.8,color=NEGATIVE)
        self.add_show(paper,border,ruled,margin,duration=1.75)
        date=self.big_text("DATE: 19 JAN 2027",-1.65,.54,29,DARK,6.2,True)
        self.appearance(date,time=.9)
        # A location and a geometrically correct segment; animating the trace.
        A=np.array([-3.68,-.68,0]); B=np.array([.83,-.68,0])
        pa=Dot(A,radius=.13,color=SKETCH);pb=Dot(B,radius=.13,color=SKETCH)
        line=Line(A,B,stroke_width=4.8,color=SKETCH)
        self.play(FadeIn(pa),run_time=.50);self.register(pa)
        self.add_show(line,duration=1.8)
        self.play(FadeIn(pb),run_time=.48);self.register(pb)
        la=self.big_text("A",-3.84,-.35,31,SKETCH,.85,True)
        lb=self.big_text("B",.98,-.35,31,SKETCH,.85,True)
        self.appearance(la,lb,time=.7)
        for i,(s,y) in enumerate([
            ("1  Write the date",.46),
            ("2  Use a ruler",-.42),
            ("3  Label every point",-1.31),
        ]):
            tx=self.big_text(s,4.05,y,30,DARK,3.75,False)
            self.appearance(tx,time=.86);self.watch(1.3)
        self.caption("Notebook task: copy the diagram; label the endpoints accurately.")
        self.watch(6.0)

    def a_point(self):
        self.heading(2,"POINT / POSITION","A POINT NAMES A LOCATION",
                     "The dot is only a visible symbol; an ideal point has zero size.")
        start=np.array([-4.80,-.28,0]); end=np.array([3.52,-.28,0])
        guide=DashedLine(start,end,color=LIGHT,stroke_width=3,dash_length=.20)
        self.add_show(guide,duration=1.3)
        progress=ValueTracker(0.0)
        moving=always_redraw(lambda: Dot(
            interpolate(start,end,progress.get_value()),
            radius=.19,color=SKETCH))
        text=self.text("A",36,BOLD,SKETCH)
        text.add_updater(lambda m: m.move_to(
            interpolate(start,end,progress.get_value())+np.array([.30,.46,0])))
        self.add(moving,text);self.register(moving,text)
        self.play(progress.animate.set_value(.74),
                  run_time=3.8,rate_func=smooth)
        self.watch(1.3)
        self.play(progress.animate.set_value(.30),
                  run_time=2.4,rate_func=smooth)
        concept=self.big_text("A point changes position, not its dimension.",
                              0,-1.65,36,POSITIVE,12.2,True)
        self.appearance(concept,time=1.15)
        self.caption("Always name points using capital letters (A, B, C...).")
        self.watch(4.6)

    def line_ray_segment(self):
        self.heading(3,"FINITE / INFINITE","LINE, RAY AND SEGMENT",
                     "Arrowheads show extension; filled dots identify named points.")
        rows=[(.78,"LINE AB","No endpoints"),
              (-.36,"RAY AB","One endpoint: A"),
              (-1.55,"SEGMENT AB","Endpoints: A, B")]
        for y,name,meaning in rows:
            l=np.array([-5.62,y,0]);r=np.array([2.47,y,0])
            if name.startswith("LINE"):
                obj=DoubleArrow(l,r,buff=0,color=SKETCH,stroke_width=5.5,
                                 max_tip_length_to_length_ratio=.095)
                apos=np.array([-3.90,y,0]);bpos=np.array([1.13,y,0])
            elif name.startswith("RAY"):
                obj=Arrow(l,r,buff=0,color=SKETCH,stroke_width=5.5,
                          max_tip_length_to_length_ratio=.09)
                apos=l;bpos=np.array([1.13,y,0])
            else:
                obj=Line(l,r,color=SKETCH,stroke_width=5.5)
                apos=l;bpos=r
            self.add_show(obj,duration=1.7)
            for point,letter,dx in [(apos,"A",-.18),(bpos,"B",.16)]:
                dot=Dot(point,radius=.14,color=POSITIVE)
                self.play(FadeIn(dot),run_time=.30)
                self.register(dot)
                m=self.big_text(letter,point[0]+dx,y+.32,28,SKETCH,1.0,True)
                self.appearance(m,time=.34)
            meaning_label=self.big_text(name,4.70,y+.16,33,DARK,3.7,True)
            explanation=self.big_text(meaning,4.70,y-.30,25,MID,3.9)
            self.appearance(meaning_label,explanation,time=.9)
            self.watch(1.9)
        self.caption("The displayed ends of a line or ray are NOT physical endpoints.")
        self.watch(5)

    def plane(self):
        self.heading(4,"PLANE / FLAT SURFACE","A PLANE EXTENDS IN TWO DIMENSIONS",
                     "A parallelogram is a DRAWING of part of an infinite plane.")
        # Large perspective drawing, explicit distinction symbol vs ideal object.
        vertices=[[-5.13,-1.48,0],[3.70,-1.48,0],[5.43,.79,0],[-3.30,.79,0]]
        plane=Polygon(*vertices,stroke_color=SKETCH,stroke_width=4.8,
                      fill_color=SKETCH,fill_opacity=.08)
        self.play(DrawBorderThenFill(plane),run_time=2.8)
        self.register(plane)
        # Three non-collinear points determine a unique plane.
        pts=[
            (np.array([-2.85,-.66,0]),"A",(-.30,.37)),
            (np.array([2.00,-.96,0]),"B",(.35,-.26)),
            (np.array([1.10,.14,0]),"C",(.22,.33)),
        ]
        for at,s,(dx,dy) in pts:
            dot=Dot(at,radius=.18,color=POSITIVE)
            self.play(FadeIn(dot),run_time=.57);self.register(dot)
            lab=self.big_text(s,at[0]+dx,at[1]+dy,30,DARK,1.0,True)
            self.appearance(lab,time=.50)
        alpha=self.big_math(r"\alpha",4.45,-.78,69,SKETCH,1.0)
        self.appearance(alpha,time=1.05)
        key=self.big_text("The border is a visual convention, not an edge of the plane.",
                          0,-2.12,30,POSITIVE,12.5,True)
        self.appearance(key,time=1.4)
        self.caption("Three noncollinear points A, B, C define one plane.")
        self.watch(5.5)

    def notation(self):
        self.heading(5,"NOTATION / COMMUNICATE","WRITE THE OBJECT YOU MEAN",
                     "Same named points, different mathematical objects.")
        specs=[
          (r"\overleftrightarrow{AB}",.70,"LINE: BOTH DIRECTIONS","line"),
          (r"\overrightarrow{AB}",-.37,"RAY: STARTS AT A","ray"),
          (r"\overline{AB}",-1.48,"SEGMENT: FROM A TO B","segment"),
        ]
        for notation,y,gloss,kind in specs:
            l=np.array([-5.20,y,0]);r=np.array([-1.63,y,0])
            if kind=="line":
                obj=DoubleArrow(l,r,buff=0,color=SKETCH,stroke_width=4.8,
                        max_tip_length_to_length_ratio=.13)
            elif kind=="ray":
                obj=Arrow(l,r,buff=0,color=SKETCH,stroke_width=4.8,
                          max_tip_length_to_length_ratio=.13)
            else:
                obj=Line(l,r,color=SKETCH,stroke_width=4.8)
            self.add_show(obj,duration=1.02)
            e=self.big_math(notation,0.40,y,56,POSITIVE,3.0)
            self.appearance(e,time=.94)
            s=self.big_text(gloss,4.50,y,30,DARK,4.15,True)
            self.appearance(s,time=.87)
            self.watch(1.6)
        self.caption("An arrow above AB changes its meaning. Label it carefully.")
        self.watch(5.0)

    def model_and_counterexample(self):
        self.heading(6,"VISUAL REASONING","IDEAL OBJECT VS A REAL DRAWING",
                     "A wall is finite; a plane is idealized as endlessly flat.")
        wall=Rectangle(width=7.05,height=2.66,color=DARK,stroke_width=4,
                       fill_color=MODEL,fill_opacity=.45)
        wall.move_to([-2.65,-.52,0])
        self.add_show(wall,duration=2.0)
        ends=VGroup(*[
            Dot([x,y,0],radius=.13,color=NEGATIVE)
            for x in [-6.175,.875] for y in [-1.85,.81]
        ])
        self.play(FadeIn(ends),run_time=.9)
        self.register(ends)
        finite=self.big_text("REAL WALL",3.45,.54,36,DARK,4.3,True)
        infinite=self.big_text("MATHEMATICAL PLANE",3.45,-.26,30,POSITIVE,5.5,True)
        foot=self.big_text("A finite model can represent an infinite plane.",
                           0,-2.20,29,MID,12.3)
        self.appearance(finite,infinite,foot,time=1.7)
        self.caption("A sketch is a representation, not the whole geometric object.")
        self.watch(5)

    def practice(self):
        self.heading(7,"QUICK CHECK / DISCUSS","TELL THE OBJECTS APART",
                     "Identify each by its defining property, then justify.")
        prompts=[
           "1. A straight object extends in both directions.",
           "2. A straight object starts at A and continues.",
           "3. A flat surface extends in two directions.",
           "4. A finite straight part has ends A and B.",
        ]
        for i,item in enumerate(prompts):
            m=self.big_text(item,0,.75-.78*i,33,DARK,12.9)
            self.appearance(m,time=.9)
        self.caption("Pause for oral or notebook answers. Use correct geometry words.")
        self.watch(8.0)
        self.stage_clear()
        for i,item in enumerate(["1  LINE","2  RAY","3  PLANE","4  SEGMENT"]):
            m=self.big_text(item,0,.77-.78*i,38,POSITIVE,10.9,True)
            self.appearance(m,time=.75);self.watch(.78)
        self.caption("Check every reason, not just the object's name.")
        self.watch(4.3)


class Geometry8W01_LogicalSetsV2(Geometry8V2Base):
    """Week01, Class02: dimensional sorting and real animated two-set placement."""
    LESSON_LABEL="CLASS 02 -- SETS AND LOGICAL DIAGRAMS"
    COVER_TITLE="CLASSIFY GEOMETRY WITH LOGICAL SETS"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.dimension_sort()
        self.define_sets()
        self.moving_venn()
        self.membership()
        self.intersection_union()
        self.overlap_count()
        self.exit_task()
        self.exit_review("CLASSIFICATION NEEDS A CLEAR RULE",
                         "In both sets: AND. In the union: at least one property.")

    def dimension_sort(self):
        self.heading(1,"DIMENSION / SORT","CLASSIFY BY DIMENSIONS",
                     "Use the number of independent directions in the object.")
        xs=[-4.85,-1.63,1.63,4.85]
        fig=[
            Dot([xs[0],-.28,0],radius=.21,color=SKETCH),
            Line([xs[1]-.92,-.28,0],[xs[1]+.92,-.28,0],
                 color=SKETCH,stroke_width=6),
            Square(1.40,fill_color=MODEL,fill_opacity=.35,
                   stroke_color=SKETCH,stroke_width=4).move_to([xs[2],-.28,0]),
        ]
        # Schematic cube with linked corners (not a mathematical 3D solid object).
        front=Square(1.27,color=DARK,stroke_width=3.5).move_to([xs[3]-.23,-.55,0])
        rear=Square(1.27,color=SKETCH,stroke_width=3.5).move_to([xs[3]+.23,-.08,0])
        links=VGroup(*[
           Line(a,b,color=SKETCH,stroke_width=3)
           for a,b in zip(front.get_vertices(),rear.get_vertices())
        ])
        fig.append(VGroup(front,rear,links))
        for i,(shape,x) in enumerate(zip(fig,xs)):
            self.add_show(shape,duration=1.25)
            label=self.big_text(["0D: POINT","1D: LINE","2D: PLANE","3D: SOLID"][i],
                                x,-1.71,30,DARK,3.3,True)
            self.appearance(label,time=.80)
            self.watch(1.2)
        self.caption("A cube drawn on a flat screen represents 3D space: it is a 2D image.")
        self.watch(5.5)

    def define_sets(self):
        self.heading(2,"SET / PROPERTY","A SET MUST HAVE A CLEAR RULE",
                     "We will classify four different geometric figures.")
        xs=[-4.35,-1.40,1.45,4.38]
        names=["GREEN TRIANGLE","BLUE TRIANGLE","BLUE SQUARE","GRAY SQUARE"]
        shapes=[
            Triangle().scale(.68).set_stroke(POSITIVE,width=5)
                     .set_fill(POSITIVE,opacity=.40),
            Triangle().scale(.68).set_stroke(SKETCH,width=5)
                     .set_fill(SKETCH,opacity=.42),
            Square(side_length=1.22).set_stroke(SKETCH,width=5)
                     .set_fill(SKETCH,opacity=.42),
            Square(side_length=1.22).set_stroke(MID,width=5)
                     .set_fill(MID,opacity=.25),
        ]
        for x,name,obj in zip(xs,names,shapes):
            obj.move_to([x,-.26,0])
            self.add_show(obj,duration=1.25)
            note=self.big_text(name,x,-1.63,27,DARK,3.7,True)
            self.appearance(note,time=.78)
            self.watch(1.0)
        self.caption("A = triangles. B = blue figures. Some shapes satisfy BOTH rules.")
        self.watch(6)

    def venn_base(self,animate=True):
        """Two actual circles. All symbols satisfy their stated membership."""
        R=1.59;dx=1.12;cy=-.48
        ca=Circle(radius=R,stroke_color=SKETCH,stroke_width=5)
        cb=Circle(radius=R,stroke_color=POSITIVE,stroke_width=5)
        ca.move_to([-dx,cy,0]);cb.move_to([dx,cy,0])
        if animate:
            self.add_show(ca,cb,duration=1.9)
        else:
            self.add(ca,cb);self.register(ca,cb)
        a=self.big_text("A: TRIANGLES",-3.65,.93,29,SKETCH,3.25,True)
        b=self.big_text("B: BLUE FIGURES",3.79,.93,29,POSITIVE,3.6,True)
        self.appearance(a,b,time=1.0)
        return ca,cb,R,dx,cy

    def make_shapes(self):
        g=Triangle().scale(.50).set_stroke(POSITIVE,width=5.2).set_fill(POSITIVE,opacity=.45)
        bt=Triangle().scale(.50).set_stroke(SKETCH,width=5.2).set_fill(SKETCH,opacity=.45)
        bs=Square(side_length=.89).set_stroke(SKETCH,width=5.0).set_fill(SKETCH,opacity=.45)
        gs=Square(side_length=.88).set_stroke(MID,width=5.0).set_fill(MID,opacity=.28)
        return [g,bt,bs,gs]

    def place_four(self,animated=True):
        targets=[[-1.93,-.52,0],[0,-.52,0],[1.93,-.52,0],[5.12,-.62,0]]
        figures=self.make_shapes()
        initial=[[-5.16,-.40,0],[-4.55,-1.73,0],[4.35,-1.73,0],[5.12,-.62,0]]
        for i,(obj,start,dest) in enumerate(zip(figures,initial,targets)):
            obj.move_to(start if animated else dest)
            self.play(FadeIn(obj,scale=.84),run_time=.70)
            self.register(obj)
            if animated and i<3:
                self.play(obj.animate.move_to(dest),
                          run_time=1.85,rate_func=smooth)
                self.watch(.9)
        return figures

    def moving_venn(self):
        self.heading(3,"TWO-CIRCLE DIAGRAM","PLACE EACH SHAPE BY ITS RULE",
                     "A = triangles; B = blue figures. Watch each object move.")
        self.venn_base()
        self.place_four(animated=True)
        self.caption("Green triangle: only A. Blue triangle: both. Blue square: only B.")
        self.watch(5.7)

    def membership(self):
        self.heading(4,"MEMBERSHIP / BELONGS TO","TEST THE TWO CONDITIONS",
                     "A blue triangle is triangular AND blue.")
        _,_,R,dx,cy=self.venn_base()
        objs=self.place_four(animated=False)
        # Emphasize the two-set member by a genuine pulse.
        target=objs[1]
        self.play(Indicate(target,scale_factor=1.35,color=POSITIVE),run_time=2.1)
        formula=self.big_math(r"T_{\mathrm{blue}}\in A\cap B",0,-2.12,44,POSITIVE,10.0)
        self.appearance(formula,time=1.3)
        self.caption("Membership means the figure satisfies the set's stated property.")
        self.watch(5.4)

    def venn_lens(self,R=1.59,dx=1.12,cy=-.48):
        """Construct exact disk intersection lens using analytic circular arcs."""
        h=np.sqrt(R*R-dx*dx)
        ys=np.linspace(-h+.006,h-.006,105)
        left_x=dx-np.sqrt(np.maximum(0,R*R-ys*ys))
        right_x=-dx+np.sqrt(np.maximum(0,R*R-ys*ys))
        left=[np.array([x,y+cy,0]) for x,y in zip(left_x,ys)]
        right=[np.array([x,y+cy,0]) for x,y in zip(right_x[::-1],ys[::-1])]
        lens=VMobject(stroke_color=POSITIVE,stroke_width=2.0,
                       fill_color=POSITIVE,fill_opacity=.19)
        lens.set_points_as_corners(left+right+[left[0]])
        return lens

    def intersection_union(self):
        self.heading(5,"AND / OR","COMPARE INTERSECTION AND UNION",
                     "AND requires both rules. OR requires at least one rule.")
        ca,cb,_,_,_=self.venn_base()
        figures=self.place_four(animated=False)
        lens=self.venn_lens()
        self.play(FadeIn(lens),run_time=1.50)
        self.register(lens)
        self.play(Indicate(figures[1],scale_factor=1.30),run_time=1.50)
        a=self.big_math(r"A\cap B:\ 1\ \mathrm{figure}",4.23,-1.58,
                        41,POSITIVE,4.15)
        self.appearance(a,time=1.0)
        self.caption("INTERSECTION = one blue triangle. The lens is the shared region.")
        self.watch(4.7)
        self.play(FadeOut(lens),run_time=.65)
        fill_a=Circle(radius=1.59,stroke_width=0,
              fill_color=SKETCH,fill_opacity=.085).move_to([-1.12,-.48,0])
        fill_b=Circle(radius=1.59,stroke_width=0,
              fill_color=POSITIVE,fill_opacity=.085).move_to([1.12,-.48,0])
        self.play(FadeIn(fill_a),FadeIn(fill_b),run_time=1.55)
        self.register(fill_a,fill_b)
        self.play(*[Indicate(o,scale_factor=1.15) for o in figures[:3]],
                  run_time=1.7)
        u=self.big_math(r"A\cup B:\ 3\ \mathrm{figures}",4.23,-2.18,
                        40,SKETCH,4.3)
        self.appearance(u,time=1.15)
        self.caption("UNION = the green triangle, blue triangle and blue square.")
        self.watch(4.7)

    def overlap_count(self):
        self.heading(6,"NO DOUBLE COUNTING","COUNT UNIQUE FIGURES",
                     "One blue triangle belongs to two sets but is one object.")
        e1=self.big_math(r"|A|=2",0,.78,62,SKETCH)
        self.appearance(e1,time=1.1)
        e2=self.big_math(r"|B|=2",0,-.06,62,POSITIVE)
        self.appearance(e2,time=1.1)
        e3=self.big_math(r"|A\cap B|=1",0,-.87,61,DARK)
        self.appearance(e3,time=1.1)
        result=self.big_math(r"|A\cup B|=2+2-1=3",0,-1.88,
                             59,POSITIVE,12.5)
        self.appearance(result,time=1.65)
        self.caption("The intersection is subtracted once to avoid double counting.")
        self.watch(5.7)

    def exit_task(self):
        self.heading(7,"SORT / JUSTIFY","EXPLAIN EACH PLACEMENT",
                     "Answer with a geometric property, not a guess.")
        prompts=[
          "1. Which object belongs to A and B?",
          "2. Which object is in B, but not A?",
          "3. Which object belongs to neither?",
          "4. Is a line 1D or 2D? Explain.",
        ]
        for i,prompt in enumerate(prompts):
            o=self.big_text(prompt,0,.79-i*.82,34,DARK,12.8)
            self.appearance(o,time=.85)
        self.caption("Stop and justify your answers in pairs before the solution.")
        self.watch(9.0)
        self.stage_clear()
        for i,answer in enumerate([
            "1. THE BLUE TRIANGLE",
            "2. THE BLUE SQUARE",
            "3. THE GRAY SQUARE",
            "4. LINE = 1D (LENGTH)",
        ]):
            t=self.big_text(answer,0,.78-i*.84,37,POSITIVE,12.3,True)
            self.appearance(t,time=.87)
            self.watch(.85)
        self.caption("Verify the rule defining each set and the dimension of each object.")
        self.watch(4.2)
