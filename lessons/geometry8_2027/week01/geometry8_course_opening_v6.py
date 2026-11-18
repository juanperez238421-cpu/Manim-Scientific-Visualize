#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8, 2027: V6 cinematic annual preview, margin-safe full review.

Extends the ALREADY APPROVED V5 video so the exact CAD visual identity, title,
original Instituto Jorge Robledo PNG, semantic colors, phase HUD, typeface,
animations and course sequence are preserved. Replaces ONLY figure methods.

Curriculum references: IJR geometry Grade 8 malla (2026) P1/P2/P3;
2027 first four weeks have their own class calendar and are not reassigned here.
P1 line/plane, geometric construction and angle relations;
P2 triangle, similarity, circle and Pythagorean theorem;
P3 perimeter, area, shaded regions, and genuine three-dimensional solids.

Render exact scene (Manim Community Edition 0.20.1):
  manim -pql lessons/geometry8_2027/week01/geometry8_course_opening_v6.py Geometry8_YearOpeningV6
  manim -pqh lessons/geometry8_2027/week01/geometry8_course_opening_v6.py Geometry8_YearOpeningV6
"""
from __future__ import annotations

import numpy as np
from manim import *
from geometry8_course_opening_v5 import Geometry8_YearOpeningV5
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, TERRAIN, SLAB


class Geometry8_YearOpeningV6(Geometry8_YearOpeningV5):
    """Exact V5 institutional House CAD, with stronger 2D and cinematic 3D."""

    COVER_TITLE = "GEOMETRY IN MOTION -- FROM 2D TO 3D"
    LESSON_LABEL = "THE MATHEMATICS WE WILL EXPLORE THIS YEAR"
    HUD_TITLE = "GEOMETRY 8 -- 2027 -- THE YEAR AHEAD"
    HUD_SUBTITLE = "A cinematic preview of the three curriculum periods"

    # 2D drawing-only bounds; titles/subtitles/caption/HUD have own fixed lanes.
    LEFT_BOUND = -5.92
    RIGHT_BOUND = 5.92
    LOWER_BOUND = -2.63
    UPPER_BOUND = 1.21

    def bounds(self, *figures, label="scene"):
        """Reject out-of-margin static geometry, not silently clip it.

        Bounding points are checked BEFORE animations. Dynamic updaters also
        remain within the same known radial/geometric envelopes by design.
        """
        for f in figures:
            if f.get_left()[0] < self.LEFT_BOUND - .025:
                raise ValueError(f"{label} protrudes left: {f.get_left()[0]:.3f}")
            if f.get_right()[0] > self.RIGHT_BOUND + .025:
                raise ValueError(f"{label} protrudes right: {f.get_right()[0]:.3f}")
            if f.get_bottom()[1] < self.LOWER_BOUND - .025:
                raise ValueError(f"{label} protrudes into caption: {f.get_bottom()[1]:.3f}")
            if f.get_top()[1] > self.UPPER_BOUND + .025:
                raise ValueError(f"{label} protrudes into title: {f.get_top()[1]:.3f}")

    def plane_preview(self):
        self.heading(0, "P1 / GEOMETRY OF PLANES",
            "A PLANE EXTENDS IN TWO DIMENSIONS",
            "A finite drawing can represent part of an infinite flat plane.")
        plane=Polygon([-5.22,-2.00,0],[4.40,-2.00,0],
                      [5.26,.78,0],[-4.38,.78,0],
                      stroke_color=SKETCH,stroke_width=4.6,
                      fill_color=MODEL,fill_opacity=.24)
        line=Line([-4.08,-.72,0],[4.15,-.72,0],color=POSITIVE,stroke_width=5.2)
        A=Dot([-2.52,-.72,0],radius=.16,color=DARK)
        B=Dot([2.56,-.72,0],radius=.16,color=DARK)
        self.bounds(plane,line,A,B,label="plane")
        self.draw_stage(plane,runtime=1.65)
        self.play(Create(line),FadeIn(A),FadeIn(B),run_time=1.55)
        self.register(line,A,B)
        self.play(Indicate(A,scale_factor=1.4),Indicate(B,scale_factor=1.4),
                  run_time=1.55)
        self.appearance(self.txt("TWO POINTS -- ONE LINE",-2.10,-2.25,
                                 31,DARK,7.5,True),time=.95)
        self.caption("The geometric plane is infinite; the quadrilateral is just a model.")
        self.wait(3.0)

    def compass_construction(self):
        self.heading(0, "P1 / RULER AND COMPASS",
            "EQUAL RADII CREATE EXACT STRUCTURES",
            "Intersecting arcs locate the perpendicular bisector of a segment.")
        cy=-.78
        A=np.array([-1.38,cy,0]); B=np.array([1.38,cy,0]); R=1.80
        h=np.sqrt(R**2-1.38**2)
        ab=Line(A,B,color=DARK,stroke_width=5.8)
        self.draw_stage(ab,runtime=1.15)
        a=Dot(A,radius=.16,color=SKETCH)
        b=Dot(B,radius=.16,color=SKETCH)
        self.play(FadeIn(a),FadeIn(b),run_time=.55);self.register(a,b)
        t=ValueTracker(.002)
        s=ValueTracker(.002)
        l=always_redraw(lambda: Arc(radius=R,start_angle=-PI/2,
                         angle=max(.002,t.get_value()),arc_center=A,
                         color=SKETCH,stroke_width=4.5))
        r=always_redraw(lambda: Arc(radius=R,start_angle=-PI/2,
                         angle=max(.002,s.get_value()),arc_center=B,
                         color=POSITIVE,stroke_width=4.5))
        # Radius can never exceed 1.80 and cy+R=1.02, cy-R=-2.58.
        self.add(l,r);self.register(l,r)
        self.play(t.animate.set_value(TAU),run_time=3.05,rate_func=smooth)
        self.play(s.animate.set_value(TAU),run_time=3.05,rate_func=smooth)
        upper=Dot([0,cy+h,0],radius=.16,color=DARK)
        lower=Dot([0,cy-h,0],radius=.16,color=DARK)
        perp=DashedLine([0,cy-h-.08,0],[0,cy+h+.08,0],
                        color=DARK,stroke_width=4.7,dash_length=.13)
        self.bounds(upper,lower,perp,label="bisector")
        self.play(FadeIn(upper),FadeIn(lower),run_time=.45)
        self.register(upper,lower)
        self.draw_stage(perp,runtime=1.45)
        self.play(Indicate(upper,scale_factor=1.5),Indicate(lower,scale_factor=1.5),
                  run_time=1.15)
        self.appearance(self.txt("PERPENDICULAR BISECTOR",3.58,-1.92,
                                 29,POSITIVE,5.5,True),time=1.1)
        self.caption("The two intersection points are equidistant from A and B.")
        self.wait(3.2)

    def angle_transformations(self):
        self.heading(0, "P1 / ANGLE CLASSIFICATION",
            "THE SAME VERTEX -- FOUR ANGLE FAMILIES",
            "A rotating ray creates measured changes in angular opening.")
        O=np.array([-3.33,-1.21,0]); rr=2.30
        ray=Arrow(O,O+RIGHT*rr,buff=0,color=DARK,stroke_width=5.5)
        theta=ValueTracker(30*DEGREES)
        movable=always_redraw(lambda:Arrow(
            O,O+rr*np.array([np.cos(theta.get_value()),np.sin(theta.get_value()),0]),
            color=SKETCH,buff=0,stroke_width=5.4))
        arc=always_redraw(lambda:Arc(
            radius=.96,start_angle=0,angle=max(.002,theta.get_value()),
            arc_center=O,color=POSITIVE,stroke_width=5.0))
        guide=Circle(radius=rr,color=LIGHT,stroke_width=1.2).move_to(O)
        # Only the upper semicircle is displayed; not a full circle into caption.
        upper=Arc(radius=rr,start_angle=0,angle=PI,arc_center=O,
                  color=LIGHT,stroke_width=1.4)
        self.bounds(ray,upper,label="angle")
        self.draw_stage(ray,upper,runtime=1.45)
        self.add(movable,arc);self.register(movable,arc)
        center=Dot(O,radius=.16,color=DARK)
        self.play(FadeIn(center),run_time=.36);self.register(center)
        text=self.txt("ACUTE: 30 DEGREES",3.26,-.12,34,SKETCH,5.55,True)
        self.appearance(text,time=.88)
        for degrees,caption in ((90,"RIGHT: 90 DEGREES"),
                                (135,"OBTUSE: 135 DEGREES"),
                                (180,"STRAIGHT: 180 DEGREES")):
            n=self.txt(caption,3.26,-.12,34,SKETCH,5.65,True)
            self.play(theta.animate.set_value(degrees*DEGREES),
                      ReplacementTransform(text,n),run_time=2.65,
                      rate_func=smooth)
            text=n
            self.wait(.55)
        self.caption("The degree measures are exact; the arc is a visual measure.")
        self.wait(2.7)

    def triangle_geometry(self):
        self.heading(0,"P2 / TRIANGLE GEOMETRY",
             "ONE TRIANGLE -- MULTIPLE NOTABLE LINES",
             "Altitude, median and centroid are linked by geometric definitions.")
        P=np.array([-4.72,-1.95,0])
        Q=np.array([.72,-1.95,0])
        R=np.array([-2.32,.98,0])
        tri=Polygon(P,Q,R,stroke_color=SKETCH,stroke_width=5.3,
                    fill_color=MODEL,fill_opacity=.13)
        foot=np.array([R[0],P[1],0])
        alt=DashedLine(R,foot,dash_length=.15,stroke_width=4.3,color=POSITIVE)
        med=Line(R,(P+Q)/2,stroke_width=3.4,color=DARK)
        G=(P+Q+R)/3
        centre=Dot(G,radius=.15,color=DARK)
        self.bounds(tri,alt,med,centre,label="triangles")
        self.draw_stage(tri,runtime=2.0)
        self.draw_stage(alt,runtime=1.7)
        right_angle=Square(side_length=.24,stroke_color=POSITIVE,
                           stroke_width=2.5,fill_opacity=0)
        right_angle.move_to(foot+[.12,.12,0])
        self.draw_stage(right_angle,runtime=.75)
        self.draw_stage(med,runtime=1.35)
        self.play(FadeIn(centre),run_time=.55);self.register(centre)
        self.play(Indicate(centre,scale_factor=1.4),run_time=1.05)
        self.appearance(self.txt("ALTITUDE",3.65,.54,37,POSITIVE,5.5,True),
                        self.txt("MEDIAN",3.65,-.26,37,SKETCH,5.5,True),
                        self.txt("CENTROID",3.65,-1.15,32,DARK,5.5,True),time=1.45)
        self.caption("A median goes to the opposite side's midpoint.")
        self.wait(3.25)

    def thales_similarity(self):
        self.heading(0,"P2 / THALES AND SIMILARITY",
            "A MOVING PARALLEL CREATES SIMILAR TRIANGLES",
            "Corresponding lengths change by the same scale factor.")
        top=np.array([-3.53,1.02,0])
        left=np.array([-4.73,-1.99,0])
        right=np.array([.61,-1.99,0])
        parent=Polygon(top,left,right,
                       stroke_color=DARK,stroke_width=5.1,
                       fill_color=MODEL,fill_opacity=.12)
        self.bounds(parent,label="similarity")
        self.draw_stage(parent,runtime=1.75)
        fraction=ValueTracker(.25)
        points=lambda: (top+fraction.get_value()*(left-top),
                        top+fraction.get_value()*(right-top))
        inset=always_redraw(lambda:Polygon(top,*points(),
                      stroke_color=POSITIVE,stroke_width=4.0,
                      fill_color=TERRAIN,fill_opacity=.47))
        parallel=always_redraw(lambda:Line(*points(),
                        color=SKETCH,stroke_width=4.9))
        self.add(inset,parallel);self.register(inset,parallel)
        self.play(fraction.animate.set_value(.77),run_time=3.6,rate_func=smooth)
        self.play(fraction.animate.set_value(.50),run_time=2.05,rate_func=smooth)
        self.appearance(self.formula(r"\frac{CP}{CA}=\frac{CQ}{CB}",
                                    3.56,.23,54,POSITIVE,5.15),time=1.14)
        self.appearance(self.txt("PARALLEL SEGMENTS",3.53,-.95,
                                 29,SKETCH,5.45,True),time=.82)
        self.caption("Parallelism supports proportionality and similarity.")
        self.wait(3.0)

    def circle_geometry(self):
        self.heading(0,"P2 / CIRCLE GEOMETRY",
            "ONE CIRCLE -- MANY EXACT RELATIONSHIPS",
            "Explore radius, diameter, chord, and arc with shared center.")
        C=np.array([-3.05,-.74,0]);R=1.87
        circ=Circle(radius=R,color=SKETCH,stroke_width=5).move_to(C)
        self.bounds(circ,label="circle")
        self.draw_stage(circ,runtime=2.05)
        centre=Dot(C,radius=.15,color=DARK)
        dia=Line(C+LEFT*R,C+RIGHT*R,color=DARK,stroke_width=3.4)
        radius=Line(C,C+RIGHT*R,color=POSITIVE,stroke_width=5)
        theta1=40*DEGREES;theta2=139*DEGREES
        e1=C+R*np.array([np.cos(theta1),np.sin(theta1),0])
        e2=C+R*np.array([np.cos(theta2),np.sin(theta2),0])
        chord=Line(e1,e2,color=SKETCH,stroke_width=4.7)
        path=Arc(radius=R,start_angle=theta1,
                 angle=theta2-theta1,arc_center=C,
                 color=POSITIVE,stroke_width=6.1)
        self.play(FadeIn(centre),run_time=.36);self.register(centre)
        self.draw_stage(dia,runtime=1.0)
        self.draw_stage(radius,runtime=1.0)
        self.draw_stage(chord,runtime=.95)
        self.draw_stage(path,runtime=1.1)
        # Labels appear in synchrony with the selected geometric evidence.
        for index,title in enumerate(("RADIUS", "DIAMETER", "CHORD", "ARC")):
            label=self.txt(title,3.30,1.00-.74*index,35,
                           POSITIVE if index%2==0 else SKETCH,5.2,True)
            self.appearance(label,time=.57)
        self.play(Indicate(path,scale_factor=1.08),run_time=1.45)
        self.caption("Diameter = two radii; a chord joins points on the circle.")
        self.wait(3.0)

    def pythagoras(self):
        self.heading(0,"P2 / PYTHAGOREAN THEOREM",
            "AN EQUATION THAT CAN BE SEEN",
            "Exact squares are constructed on a 3-4-5 right triangle.")
        A=np.array([-2.90,-1.28,0]); step=.34
        B=A+np.array([4*step,0,0])
        C=A+np.array([0,3*step,0])
        BC=C-B
        n=np.array([BC[1],-BC[0],0])
        tri=Polygon(A,B,C,color=DARK,stroke_width=5,
                    fill_opacity=0)
        leg4=Polygon(A,B,B+DOWN*4*step,A+DOWN*4*step,
                     stroke_color=SKETCH,stroke_width=3.7,
                     fill_color=MODEL,fill_opacity=.70)
        leg3=Polygon(A,C,C+LEFT*3*step,A+LEFT*3*step,
                     stroke_color=POSITIVE,stroke_width=3.7,
                     fill_color=TERRAIN,fill_opacity=.72)
        hyp=Polygon(B,C,C+n,B+n,
                    stroke_color=DARK,stroke_width=4,
                    fill_color=SLAB,fill_opacity=.55)
        self.bounds(tri,leg3,leg4,hyp,label="Pythagoras")
        self.draw_stage(tri,runtime=1.4)
        self.play(Create(leg3),Create(leg4),run_time=1.75)
        self.register(leg3,leg4)
        self.draw_stage(hyp,runtime=1.7)
        self.play(Indicate(leg3,scale_factor=1.06),
                  Indicate(leg4,scale_factor=1.06),
                  Indicate(hyp,scale_factor=1.05),run_time=2.1)
        self.appearance(self.formula(r"3^2+4^2=5^2",
                                    3.54,.43,65,POSITIVE,5.2),time=1.12)
        self.appearance(self.txt("9 + 16 = 25",3.50,-.58,
                                 38,DARK,5.2,True),time=.90)
        self.caption("A right triangle's leg-square areas sum to its hypotenuse square.")
        self.wait(3.45)

    def area_recomposition(self):
        self.heading(0,"P3 / PLANE AREA",
            "COMPLEX AREAS CAN BE RECOMPOSED",
            "A trapezoid becomes a rectangle and two right triangles.")
        xl=-4.78;xr=.66;yt=.90;yb=-1.80
        ul=-3.51;ur=-.68
        frame=Polygon([xl,yb,0],[xr,yb,0],[ur,yt,0],[ul,yt,0],
                      color=DARK,stroke_width=4.3,
                      fill_color=MODEL,fill_opacity=.16)
        l=self.line([ul,yb,0],[ul,yt,0],SKETCH,3.3)
        r=self.line([ur,yb,0],[ur,yt,0],SKETCH,3.3)
        rect=Rectangle(width=ur-ul,height=yt-yb,stroke_width=0,
                       fill_color=MODEL,fill_opacity=.65)
        rect.move_to([(ur+ul)/2,(yt+yb)/2,0])
        t1=Polygon([xl,yb,0],[ul,yb,0],[ul,yt,0],
                   stroke_width=0,fill_color=TERRAIN,fill_opacity=.85)
        t2=Polygon([ur,yt,0],[ur,yb,0],[xr,yb,0],
                   stroke_width=0,fill_color=SLAB,fill_opacity=.67)
        self.bounds(frame,l,r,rect,t1,t2,label="area")
        self.draw_stage(frame,runtime=1.5)
        self.draw_stage(l,r,runtime=1.0)
        self.play(LaggedStart(FadeIn(t1),FadeIn(rect),FadeIn(t2),
                              lag_ratio=.23),run_time=1.75)
        self.register(t1,rect,t2)
        self.play(t1.animate.shift(LEFT*.28),
                  t2.animate.shift(RIGHT*.28),run_time=1.85,
                  rate_func=smooth)
        self.play(t1.animate.shift(RIGHT*.28),
                  t2.animate.shift(LEFT*.28),run_time=1.85,
                  rate_func=smooth)
        self.appearance(self.formula(r"A=\frac{(B+b)h}{2}",
                                    3.36,.10,60,POSITIVE,5.4),time=1.2)
        self.caption("Rearrangement preserves total area without guessing.")
        self.wait(3.1)

    def shaded_area(self):
        self.heading(0,"P3 / SHADED REGIONS",
            "THE AREA IS WHAT REMAINS",
            "Subtract the inner disk from the outer disk.")
        C=np.array([-3.00,-.74,0]);R=1.87;r=.82
        outer=Circle(radius=R,color=DARK,stroke_width=4.7,
                     fill_color=MODEL,fill_opacity=.75).move_to(C)
        inner=Circle(radius=r,color=SKETCH,stroke_width=4.2,
                     fill_color=WHITE,fill_opacity=1).move_to(C)
        self.bounds(outer,inner,label="annulus")
        self.draw_stage(outer,runtime=1.55)
        self.play(FadeIn(inner),run_time=1.1)
        self.register(inner)
        radius=self.line(C,C+RIGHT*R,POSITIVE,4.0)
        radius_inner=self.line(C,C+UP*r,SKETCH,4.0)
        self.draw_stage(radius,radius_inner,runtime=1.05)
        self.play(Indicate(outer,scale_factor=1.04),
                  Indicate(inner,scale_factor=1.08),run_time=1.7)
        self.appearance(self.formula(
            r"A_{\mathrm{shaded}}=\pi(R^2-r^2)",
            3.23,-.10,47,POSITIVE,5.9),time=1.17)
        self.caption("A shaded annulus is the difference between two circle areas.")
        self.wait(3.2)

    def platonic_solids_3d(self):
        """CAD wireframe -> 6-face explosion/reassembly -> two other solids.

        Deliberately never ReplacementTransform between unrelated mesh
        topologies. Preserve the institutional fixed HUD and caption.
        """
        self.stage_clear()
        number=self._phase_number
        self._phase_number+=1
        self.set_phase(number,"P3 / REAL 3D GEOMETRY",SKETCH)
        title=self._hud_fixed(self.txt(
            "GEOMETRY BECOMES A THREE-DIMENSIONAL STRUCTURE",
            0,2.08,37,DARK,12.6,True))
        sub=self._hud_fixed(self.txt(
            "Observe faces, edges and vertices -- then rotate the solid.",
            0,1.43,26,MID,12.4))
        self.play(Write(title),Write(sub),run_time=1.35)
        self.move_camera(phi=61*DEGREES,theta=-48*DEGREES,run_time=1.5)
        pos=LEFT*1.55+DOWN*.78
        cube_wire=Cube(side_length=2.23)
        cube_wire.set_fill(opacity=0)
        cube_wire.set_stroke(color=SKETCH,width=2.8)
        cube_wire.shift(pos)
        self.play(Create(cube_wire),run_time=2.35)
        self.register(cube_wire)
        cube=Cube(side_length=2.23,fill_color=MODEL,fill_opacity=.78)
        cube.set_stroke(color=SKETCH,width=2.9)
        cube.shift(pos)
        self.play(FadeIn(cube),FadeOut(cube_wire),run_time=1.6)
        self.register(cube)
        # Rotate first: assembled cube has no independent accidental shifts.
        self.begin_ambient_camera_rotation(rate=.095)
        self.play(Rotate(cube,angle=PI*.73,axis=UP+RIGHT,
                         about_point=cube.get_center()),run_time=3.4,
                  rate_func=smooth)
        self.stop_ambient_camera_rotation()
        labels=[
            self._hud_fixed(self.formula(r"F=6",3.45,.69,53,SKETCH,4.3)),
            self._hud_fixed(self.formula(r"E=12",3.45,-.15,53,POSITIVE,4.3)),
            self._hud_fixed(self.formula(r"V=8",3.45,-.98,53,DARK,4.3)),
        ]
        self.play(LaggedStart(*[Write(m) for m in labels],
                              lag_ratio=.20),run_time=1.5)
        # Each face moves along its OWN surface normal. The solid never turns
        # into an unrelated geometry; it simply separates into its six faces.
        faces=list(cube)
        center=cube.get_center()
        vectors=[]
        for f in faces:
            v=f.get_center()-center
            norm=np.linalg.norm(v)
            vectors.append(v/max(norm,1e-7)*.36)
        self.play(*[face.animate.shift(d) for face,d in zip(faces,vectors)],
                  run_time=2.0,rate_func=smooth)
        self.wait(.8)
        self.play(*[face.animate.shift(-d) for face,d in zip(faces,vectors)],
                  run_time=2.0,rate_func=smooth)
        self.caption("A cube: six congruent square faces, 12 edges and 8 vertices.")
        self.wait(2.1)
        self.play(*[FadeOut(m) for m in labels],run_time=.58)
        for m in labels:
            self.remove_fixed_in_frame_mobjects(m)
            self.remove(m)

        tetra=Tetrahedron().scale(1.45)
        tetra.set_fill(color=SLAB,opacity=.76)
        tetra.set_stroke(color=SKETCH,width=3.4)
        tetra.move_to(cube.get_center())
        self.play(FadeOut(cube,shift=LEFT*.28),
                  FadeIn(tetra,shift=RIGHT*.25),
                  run_time=1.75)
        self.register(tetra)
        tetra_label=self._hud_fixed(self.txt(
            "TETRAHEDRON: 4 TRIANGULAR FACES",
            3.29,-.33,30,POSITIVE,5.7,True))
        self.play(Write(tetra_label),run_time=1.03)
        self.play(Rotate(tetra,angle=PI*1.30,axis=RIGHT+UP*.40,
                         about_point=tetra.get_center()),
                  run_time=3.45,rate_func=smooth)
        self.wait(.85)
        self.play(FadeOut(tetra_label),run_time=.5)
        self.remove_fixed_in_frame_mobjects(tetra_label)
        self.remove(tetra_label)

        # A third *Platonic* solid makes topology more than decoration.
        octa=Octahedron()
        octa.scale(1.46)
        octa.set_fill(color=TERRAIN,opacity=.77)
        octa.set_stroke(color=SKETCH,width=3.5)
        octa.move_to(tetra.get_center())
        self.play(FadeOut(tetra,shift=LEFT*.26),
                  FadeIn(octa,shift=RIGHT*.26),run_time=1.65)
        self.register(octa)
        oct_label=self._hud_fixed(self.txt(
            "OCTAHEDRON: 8 TRIANGULAR FACES",
            3.29,-.33,30,POSITIVE,5.6,True))
        self.play(Write(oct_label),run_time=1.0)
        self.begin_ambient_camera_rotation(rate=.10)
        self.play(Rotate(octa,angle=PI*1.26,axis=UP+OUT*.65,
                         about_point=octa.get_center()),run_time=4.2,
                  rate_func=smooth)
        self.stop_ambient_camera_rotation()
        self.caption("Different solids have different faces, edges and vertices.")
        self.wait(3.0)
        self.play(FadeOut(octa),FadeOut(oct_label),
                  FadeOut(title),FadeOut(sub),run_time=.85)
        self.remove_fixed_in_frame_mobjects(oct_label,title,sub)
        for m in (oct_label,title,sub):
            self.remove(m)
        self.move_camera(phi=0*DEGREES,theta=-90*DEGREES,
                         zoom=1,run_time=1.45)
