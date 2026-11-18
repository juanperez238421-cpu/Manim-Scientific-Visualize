#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry8 / 2027 / annual cinematic opener / V6 senior QA revision.

Preserves the exact successful V5 institutional style: true IJR raster crest,
the CAD title/section/footer system, the source-exact three-period structure,
technical grayscale/blue/green palette, Tex typography and classroom pauses.

Main improvements:
  - Explicit safe layout volume for large 2D geometries
  - Larger mathematical objects without title/caption collisions
  - Clearer circle, Thales, triangle and composite-area constructions
  - Real 3D cube assembled from moving faces, ghost-wireframe, camera orbit
  - Truly 3D tetrahedron and an actual curved solid, cylinder
  - Continuous camera/solid-motion transitions, mathematically honest labels
  - Frame integrity checks belong to the isolated V6 CI workflow

This is a course trailer, not the detailed Week 01 sets class. Source is
the IJR Geometry 8 2026 malla for periods I-III, plus the user-supplied
2027 Week01-04 planner for actual first-week chronology only.

Manim Community Edition 0.20.1, render Geometry8_YearOpeningV6.
"""
from __future__ import annotations

import numpy as np
from manim import *
from geometry8_course_opening_v5 import Geometry8_YearOpeningV5
from physics9_week01_cad import DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, TERRAIN, SLAB


class Geometry8_YearOpeningV6(Geometry8_YearOpeningV5):
    COVER_TITLE = "GEOMETRY IN MOTION -- FROM 2D TO 3D"
    LESSON_LABEL = "THE MATHEMATICS WE WILL EXPLORE THIS YEAR"
    HUD_TITLE = "GEOMETRY 8 -- 2027 -- THE YEAR AHEAD"
    HUD_SUBTITLE = "A cinematic preview of the three curriculum periods"

    # Safe 16:9 CAD content zone: HUD above ~2.5; subtitles near 1.3;
    # persistent caption/footer below -2.8. The 2D scene graph stays
    # within x=[-5.9,5.9], y=[-2.48,1.12].
    SAFE_X = 5.78
    SAFE_TOP = 1.12
    SAFE_BOTTOM = -2.47

    def check_safe(self, *mobs, label="geometric figure"):
        """Validate geometry bounding boxes before showing, no silent clipping."""
        for mob in mobs:
            if mob.get_left()[0] < -self.SAFE_X - .08 or mob.get_right()[0] > self.SAFE_X + .08:
                raise ValueError(f"{label}: horizontal CAD safe margin exceeded")
            if mob.get_top()[1] > self.SAFE_TOP + .08 or mob.get_bottom()[1] < self.SAFE_BOTTOM - .08:
                raise ValueError(f"{label}: vertical CAD safe margin exceeded")

    def plane_preview(self):
        self.heading(0,"P1 / GEOMETRY OF PLANES",
            "A PLANE EXTENDS IN TWO DIMENSIONS",
            "The finite sketch represents part of an infinite plane.")
        patch=Polygon([-5.40,-1.96,0],[3.60,-1.96,0],
                      [4.72,.94,0],[-4.30,.94,0],
                      stroke_color=SKETCH,stroke_width=4.4,
                      fill_color=MODEL,fill_opacity=.31)
        inside=self.line([-4.49,-.63,0],[3.74,-.63,0],POSITIVE,5.5)
        a=Dot([-2.42,-.63,0],radius=.17,color=DARK)
        p=Dot([.44,.08,0],radius=.15,color=DARK)
        self.check_safe(patch,inside,a,p,label="plane incidence")
        self.draw_stage(patch,runtime=1.65)
        self.play(Create(inside),FadeIn(a),run_time=1.50)
        self.register(inside,a)
        self.play(FadeIn(p,scale=.4),run_time=.55);self.register(p)
        self.appearance(self.txt("A LINE AND POINTS LIE IN A PLANE",
                                 0,-2.28,29,DARK,11.3,True),time=.96)
        self.caption("The edges of the drawing do not bound the infinite plane.")
        self.wait(2.5)

    def compass_construction(self):
        self.heading(0,"P1 / RULER AND COMPASS",
            "GEOMETRIC PRECISION FROM EQUAL DISTANCES",
            "The same-radius circles locate a perpendicular bisector.")
        A=np.array([-1.47,-.59,0]);B=np.array([1.47,-.59,0]);R=1.90
        y=np.sqrt(R*R-1.47*1.47)
        baseline=self.line(A,B,DARK,5.5)
        self.check_safe(baseline,label="construction baseline")
        self.draw_stage(baseline,runtime=.95)
        ends=VGroup(Dot(A,radius=.15,color=SKETCH),Dot(B,radius=.15,color=POSITIVE))
        self.play(LaggedStart(*[FadeIn(m) for m in ends],lag_ratio=.24),
                  run_time=.80)
        self.register(*ends)
        # Only display upper/lower intersection arcs: avoid oversized full
        # circles crossing the CAD subtitle/footer. Both radii remain equal.
        # Every drawn locus is part of a radius-R circle centered on A or B.
        t=ValueTracker(.001)
        theta0=np.arctan2(y,1.47)
        left_arc=always_redraw(lambda:Arc(
            radius=R,start_angle=-theta0-.37,
            angle=max(.001,min(t.get_value(),2*theta0+.74)),
            arc_center=A,color=SKETCH,stroke_width=4.6))
        right_arc=always_redraw(lambda:Arc(
            radius=R,start_angle=PI-theta0-.37,
            angle=max(.001,min(t.get_value(),2*theta0+.74)),
            arc_center=B,color=POSITIVE,stroke_width=4.6))
        # Alternate full symmetric upper and lower sweeps using stable arcs
        # with clipping-safe fixed ranges; no invented intersection coordinates.
        left_upper=Arc(radius=R,start_angle=theta0-.43,angle=.86,
                       arc_center=A,color=SKETCH,stroke_width=4.8)
        right_upper=Arc(radius=R,start_angle=PI-theta0-.43,angle=.86,
                        arc_center=B,color=POSITIVE,stroke_width=4.8)
        left_lower=Arc(radius=R,start_angle=-theta0-.43,angle=.86,
                       arc_center=A,color=SKETCH,stroke_width=4.8)
        right_lower=Arc(radius=R,start_angle=PI+theta0-.43,angle=.86,
                        arc_center=B,color=POSITIVE,stroke_width=4.8)
        self.check_safe(left_upper,right_upper,left_lower,right_lower,
                        label="equal radius arcs")
        self.play(LaggedStart(*[Create(m) for m in
                       (left_upper,right_upper,left_lower,right_lower)],
                       lag_ratio=.24),run_time=4.0)
        self.register(left_upper,right_upper,left_lower,right_lower)
        top=Dot([0,-.59+y,0],radius=.15,color=DARK)
        bottom=Dot([0,-.59-y,0],radius=.15,color=DARK)
        bisector=DashedLine([0,-.59-y-.15,0],[0,-.59+y+.15,0],
                            color=DARK,stroke_width=4.6,dash_length=.13)
        self.check_safe(top,bottom,bisector,label="perpendicular bisector")
        self.play(FadeIn(top),FadeIn(bottom),run_time=.6);self.register(top,bottom)
        self.draw_stage(bisector,runtime=1.55)
        self.caption("Both intersection points are equidistant from segment endpoints.")
        self.wait(2.8)

    def triangle_geometry(self):
        self.heading(0,"P2 / TRIANGLES",
            "NOTABLE LINES REVEAL HIDDEN STRUCTURE",
            "An altitude is perpendicular to the opposite side.")
        A=np.array([-4.75,-1.89,0]);B=np.array([.87,-1.89,0])
        C=np.array([-2.52,1.03,0])
        tri=Polygon(A,B,C,color=SKETCH,stroke_width=5.8,
                    fill_color=MODEL,fill_opacity=.18)
        foot=np.array([C[0],A[1],0])
        height=DashedLine(C,foot,color=POSITIVE,stroke_width=4.6,
                          dash_length=.15)
        foot_marker=Square(side_length=.28,stroke_color=POSITIVE,
                           stroke_width=3).move_to(foot+RIGHT*.14+UP*.14)
        median=self.line(C,(A+B)/2,DARK,3.6)
        self.check_safe(tri,height,foot_marker,median,label="notable lines")
        self.draw_stage(tri,runtime=1.9)
        self.play(Create(height),FadeIn(foot_marker),run_time=1.35)
        self.register(height,foot_marker)
        self.play(Create(median),run_time=1.35);self.register(median)
        self.appearance(self.txt("ALTITUDE",3.35,.34,36,POSITIVE,4.6,True),
                        self.txt("MEDIAN",3.35,-.57,36,SKETCH,4.6,True),
                        time=1.20)
        self.caption("The altitude and median are distinct geometric constructions.")
        self.wait(2.7)

    def thales_similarity(self):
        self.heading(0,"P2 / SIMILARITY AND THALES",
            "ONE TRIANGLE -- MANY SCALES",
            "A parallel cross-section produces a similar triangle.")
        C=np.array([-3.42,1.05,0])
        A=np.array([-5.10,-2.13,0])
        B=np.array([.89,-2.13,0])
        full=Polygon(C,A,B,color=DARK,stroke_width=5.1,
                     fill_color=MODEL,fill_opacity=.13)
        self.check_safe(full,label="Thales triangle")
        self.draw_stage(full,runtime=1.55)
        s=ValueTracker(.30)
        segment=always_redraw(lambda:Line(
            C+s.get_value()*(A-C),C+s.get_value()*(B-C),
            color=SKETCH,stroke_width=5.3))
        subtriangle=always_redraw(lambda:Polygon(
            C,C+s.get_value()*(A-C),C+s.get_value()*(B-C),
            stroke_color=POSITIVE,stroke_width=3.1,
            fill_color=TERRAIN,fill_opacity=.42))
        self.add(subtriangle,segment)
        self.register(subtriangle,segment)
        self.play(s.animate.set_value(.75),run_time=3.1,rate_func=smooth)
        self.play(s.animate.set_value(.53),run_time=2.1,rate_func=smooth)
        self.appearance(self.formula(r"\frac{CP}{CA}=\frac{CQ}{CB}",
                                     3.42,.04,49,POSITIVE,5.6),time=1.06)
        self.caption("Only proportional sides remain as the section moves.")
        self.wait(2.8)

    def circle_geometry(self):
        self.heading(0,"P2 / CIRCLES",
            "A CIRCLE IS AN ENTIRE FAMILY OF RELATIONS",
            "Its radius defines the diameter, chord and circular arcs.")
        c=np.array([-2.68,-.64,0]);r=1.80
        circle=Circle(radius=r,color=SKETCH,stroke_width=5.1).move_to(c)
        self.check_safe(circle,label="circle envelope")
        self.draw_stage(circle,runtime=2)
        center=Dot(c,radius=.15,color=DARK)
        diameter=self.line(c+LEFT*r,c+RIGHT*r,DARK,3.5)
        rad=self.line(c,c+RIGHT*r,POSITIVE,5)
        a1=46*DEGREES;a2=132*DEGREES
        chord=self.line(c+r*np.array([np.cos(a1),np.sin(a1),0]),
                        c+r*np.array([np.cos(a2),np.sin(a2),0]),
                        SKETCH,5.0)
        arc=Arc(radius=r,start_angle=a1,angle=a2-a1,arc_center=c,
                color=POSITIVE,stroke_width=7)
        self.check_safe(diameter,rad,chord,arc,center,label="circle elements")
        self.play(FadeIn(center),Create(diameter),run_time=1.4);self.register(center,diameter)
        self.play(TransformFromCopy(diameter,rad),run_time=.85);self.register(rad)
        self.play(Create(chord),Create(arc),run_time=1.55);self.register(chord,arc)
        for i,text in enumerate(("RADIUS","DIAMETER","CHORD","ARC")):
            self.appearance(self.txt(text,3.50,.96-.73*i,36,
                            POSITIVE if i%2==0 else SKETCH,5.15,True),time=.55)
        self.caption("Elements of a circle will later connect to angles and theorems.")
        self.wait(2.9)

    def shaded_area(self):
        self.heading(0,"P3 / SHADED REGIONS",
            "THE RING IS AN AREA DIFFERENCE",
            "Remove a disk of radius r from a disk of radius R.")
        c=np.array([-2.75,-.69,0]);R=1.78;r=.84
        outer=Circle(radius=R,stroke_color=DARK,stroke_width=5,
                     fill_color=MODEL,fill_opacity=.66).move_to(c)
        inner=Circle(radius=r,stroke_color=SKETCH,stroke_width=4,
                     fill_color=WHITE,fill_opacity=1).move_to(c)
        self.check_safe(outer,inner,label="annulus")
        self.draw_stage(outer,runtime=1.3)
        self.play(FadeIn(inner,scale=.75),run_time=1.25);self.register(inner)
        big=self.line(c,c+R*RIGHT,POSITIVE,4)
        small=self.line(c,c+r*UP,SKETCH,4)
        self.play(Create(big),Create(small),run_time=1.1);self.register(big,small)
        self.appearance(self.formula(r"A=\pi(R^2-r^2)",
                                     3.17,-.13,51,POSITIVE,5.85),time=1.2)
        self.caption("Composite areas combine addition, subtraction and symmetry.")
        self.wait(3.0)

    @staticmethod
    def cube_wireframe(center,half,color=SKETCH):
        """A genuine twelve-edge cube, no raster picture or flat fake 3D."""
        vertices={}
        for sx in (-1,1):
            for sy in (-1,1):
                for sz in (-1,1):
                    vertices[sx,sy,sz]=center+half*np.array([sx,sy,sz])
        edges=[]
        for key,p in vertices.items():
            for axis in range(3):
                k=list(key)
                if k[axis]<0:
                    k[axis]=1
                    edges.append(Line(p,vertices[tuple(k)],
                                      color=color,stroke_width=3.6))
        return VGroup(*edges)

    def platonic_solids_3d(self):
        """Real 3D CAD showpiece: wireframe -> solid -> orbit -> other solids.

        Camera orbit and object rotation are explicitly separate; a top-left
        fixed HUD and the fixed text band remain screen-stationary. Avoid mesh
        interpolation between solids with different point-array topology.
        """
        self.stage_clear()
        n=self._phase_number;self._phase_number+=1
        self.set_phase(n,"P3 / 3D CONSTRUCTION",SKETCH)
        head=self._hud_fixed(self.txt("SOLIDS ARE BUILT FROM FACES AND EDGES",
                                        0,2.04,38,DARK,12.0,True))
        subtitle=self._hud_fixed(self.txt(
            "Structure, rotation, surface and enclosed volume.",
            0,1.40,27,MID,12.3))
        self.play(Write(head),Write(subtitle),run_time=1.4)
        self.move_camera(phi=65*DEGREES,theta=-50*DEGREES,run_time=1.6)

        center=np.array([-1.43,-.79,0])
        side=2.38;half=side/2
        # Show all actual twelve edges before any faces, then solid surfaces.
        wire=self.cube_wireframe(center,half)
        self.play(LaggedStart(*[Create(edge) for edge in wire],lag_ratio=.055),
                  run_time=2.6)
        self.register(wire)
        cube=Cube(side_length=side,fill_color=MODEL,fill_opacity=.74)
        cube.set_stroke(color=SKETCH,width=1.7)
        cube.move_to(center)
        # A cube is the union of six square faces; reveal them in sequence.
        self.play(LaggedStart(*[FadeIn(face,scale=.88)
                   for face in cube],lag_ratio=.11),run_time=2.6)
        self.register(cube)
        solid=VGroup(cube,wire)
        self.play(Rotate(solid,angle=PI*.78,axis=UP+RIGHT,
                         about_point=center),run_time=4.2,rate_func=smooth)
        # Camera motion produces real parallax, not a 2D screenshot rotation.
        self.move_camera(phi=71*DEGREES,theta=-19*DEGREES,run_time=2.9)
        self.play(Rotate(solid,angle=PI*.42,axis=OUT+RIGHT,
                         about_point=center),run_time=2.8)
        volume=self._hud_fixed(self.formula(r"V=a^3",3.45,.37,55,POSITIVE,4.6))
        surface=self._hud_fixed(self.formula(r"A_s=6a^2",3.45,-.68,50,SKETCH,4.7))
        self.play(Write(volume),Write(surface),run_time=1.8)
        self.caption("A cube has six congruent square faces, twelve edges and eight vertices.")
        self.wait(2.0)
        self.play(FadeOut(volume),FadeOut(surface),run_time=.55)
        self.remove_fixed_in_frame_mobjects(volume,surface)
        self.remove(volume,surface)

        # Exit as wireframe, rotate its edges, then introduce a tetrahedron.
        self.play(cube.animate.set_fill(opacity=.08),
                  wire.animate.set_stroke(width=4.8),
                  run_time=1.25)
        tetra=Tetrahedron().scale(1.34)
        tetra.set_fill(SLAB,opacity=.76)
        tetra.set_stroke(SKETCH,width=3.5)
        tetra.move_to(center)
        self.play(FadeOut(cube),FadeOut(wire),
                  FadeIn(tetra,scale=.72),run_time=1.85)
        self.register(tetra)
        self.play(Rotate(tetra,angle=PI*.91,axis=UP+RIGHT,
                         about_point=center),run_time=4.2,
                  rate_func=smooth)
        self.move_camera(phi=56*DEGREES,theta=-64*DEGREES,run_time=2.4)
        self.caption("A tetrahedron has four equilateral triangular faces.")
        self.wait(1.55)

        # A cylinder is intentionally distinguished from Platonic solids:
        # not every solid has only planar polygonal faces.
        cylinder=Cylinder(radius=1.04,height=2.34,
                          direction=OUT,resolution=(16,32),
                          fill_color=MODEL,fill_opacity=.73)
        cylinder.set_stroke(SKETCH,width=1.6)
        cylinder.move_to(center)
        self.play(FadeOut(tetra,scale=.82),
                  FadeIn(cylinder,scale=.73),run_time=1.9)
        self.register(cylinder)
        self.play(Rotate(cylinder,angle=PI*.75,
                         axis=UP+RIGHT,about_point=center),
                  run_time=3.6,rate_func=smooth)
        self.caption("A cylinder adds curved surfaces: geometry also models non-polyhedra.")
        self.wait(2.25)
        self.play(FadeOut(cylinder),FadeOut(head),FadeOut(subtitle),run_time=1.0)
        self.remove_fixed_in_frame_mobjects(head,subtitle)
        self.remove(head,subtitle)
        self.move_camera(phi=0,theta=-90*DEGREES,zoom=1,run_time=1.5)
