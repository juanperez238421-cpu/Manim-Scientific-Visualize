#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Tecnico y CAD — Clase 6 · V2 Senior QA geometry rebuild.

This V2 subclasses the exact V1 lesson so source-deck content, typography,
section order, symbols, references and timing contract remain intact.
Only the release-blocking 3D / orthographic-projection layer is rebuilt.

Corrections:
- coherent isometric solids from shared model coordinates;
- orthographic views dimensionally match the same solids;
- distinct FRONT/REAR, LEFT/RIGHT and TOP/BOTTOM views;
- gable-roof example is one consistent solid in 3D and all views;
- projection planes use parallel projectors and explicit 90° unfolding;
- observation arrows align to the object's axonometric axes;
- larger 3D figures and view cards;
- staged projection cues replace direct full-solid -> silhouette morphs.

Target: ManimCE 0.20.1.
"""
from __future__ import annotations

import numpy as np
from manim import *

from Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V1_SENIOR import (
    TechnicalDrawingClass6ISO,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT,
    RUN_Q,
    RUN,
    RUN_SLOW,
    RUN_FOLD,
    PAUSE_R,
    PAUSE_E,
    PAUSE_W,
)

TOP_FILL = "#FBFBFB"
FRONT_FILL = "#E8E8E8"
SIDE_FILL = "#D4D4D4"


class TechnicalDrawingClass6ISOV2(TechnicalDrawingClass6ISO):
    """V2 senior correction of the V1 projection geometry."""

    @staticmethod
    def _iso_basis(scale=1.0):
        ex = np.array([0.94, 0.44, 0.0]) * scale
        ey = np.array([-0.94, 0.44, 0.0]) * scale
        ez = np.array([0.00, 1.00, 0.0]) * scale
        return ex, ey, ez

    def iso_point(self, xyz, origin=ORIGIN, scale=1.0):
        ex, ey, ez = self._iso_basis(scale)
        x, y, z = xyz
        return origin + x * ex + y * ey + z * ez

    def iso_face(self, pts, origin=ORIGIN, scale=1.0, fill=WHITE, sw=2.4):
        return Polygon(
            *[self.iso_point(p, origin, scale) for p in pts],
            stroke_color=BLACK_LINE,
            stroke_width=sw,
            fill_color=fill,
            fill_opacity=1,
        )

    def iso_edge(self, a, b, origin=ORIGIN, scale=1.0, hidden=False, sw=2.2):
        A = self.iso_point(a, origin, scale)
        B = self.iso_point(b, origin, scale)
        if hidden:
            return DashedLine(A, B, dash_length=0.09, stroke_color=MID_GRAY, stroke_width=1.6)
        return Line(A, B, stroke_color=BLACK_LINE, stroke_width=sw)

    def triad(self, scale=0.75):
        o = ORIGIN
        x = Arrow(o, o + np.array([1.1, 0.52, 0]), buff=0, color=BLACK_LINE, stroke_width=2)
        y = Arrow(o, o + np.array([-1.1, 0.52, 0]), buff=0, color=MID_GRAY, stroke_width=2)
        z = Arrow(o, o + UP * 1.25, buff=0, color=BLACK_LINE, stroke_width=2)
        lx = self.txt("x", 18, BOLD).next_to(x.get_end(), RIGHT, buff=0.05)
        ly = self.txt("y", 18, BOLD, color=MID_GRAY).next_to(y.get_end(), LEFT, buff=0.05)
        lz = self.txt("z", 18, BOLD).next_to(z.get_end(), UP, buff=0.05)
        return VGroup(x, y, z, lx, ly, lz).scale(scale)

    def make_step_solid(self, scale=0.78, show_hidden=False):
        """Base 3×2×1 plus tower 1.25×1.10 from z=1 to z=2.10."""
        o = ORIGIN
        faces = VGroup(
            self.iso_face([(0,0,0),(3,0,0),(3,0,1),(0,0,1)], o, scale, FRONT_FILL),
            self.iso_face([(3,0,0),(3,2,0),(3,2,1),(3,0,1)], o, scale, SIDE_FILL),
            self.iso_face([(0,0,1),(3,0,1),(3,2,1),(0,2,1)], o, scale, TOP_FILL),
            self.iso_face([(0,0,1),(1.25,0,1),(1.25,0,2.10),(0,0,2.10)], o, scale, "#E2E2E2"),
            self.iso_face([(1.25,0,1),(1.25,1.10,1),(1.25,1.10,2.10),(1.25,0,2.10)], o, scale, "#CCCCCC"),
            self.iso_face([(0,0,2.10),(1.25,0,2.10),(1.25,1.10,2.10),(0,1.10,2.10)], o, scale, WHITE),
        )
        edges = VGroup(
            self.iso_edge((0,0,0),(3,0,0),o,scale),
            self.iso_edge((3,0,0),(3,2,0),o,scale),
            self.iso_edge((0,0,0),(0,0,1),o,scale),
            self.iso_edge((3,0,0),(3,0,1),o,scale),
            self.iso_edge((3,2,0),(3,2,1),o,scale),
            self.iso_edge((0,0,1),(3,0,1),o,scale),
            self.iso_edge((3,0,1),(3,2,1),o,scale),
            self.iso_edge((3,2,1),(0,2,1),o,scale),
            self.iso_edge((0,2,1),(0,0,1),o,scale),
            self.iso_edge((0,0,1),(0,0,2.10),o,scale),
            self.iso_edge((1.25,0,1),(1.25,0,2.10),o,scale),
            self.iso_edge((1.25,1.10,1),(1.25,1.10,2.10),o,scale),
            self.iso_edge((0,0,2.10),(1.25,0,2.10),o,scale),
            self.iso_edge((1.25,0,2.10),(1.25,1.10,2.10),o,scale),
            self.iso_edge((1.25,1.10,2.10),(0,1.10,2.10),o,scale),
            self.iso_edge((0,1.10,2.10),(0,0,2.10),o,scale),
        )
        hidden = VGroup()
        if show_hidden:
            hidden.add(
                self.iso_edge((0,2,0),(3,2,0),o,scale,hidden=True),
                self.iso_edge((0,0,0),(0,2,0),o,scale,hidden=True),
                self.iso_edge((0,2,0),(0,2,1),o,scale,hidden=True),
            )
        return VGroup(faces, hidden, edges)

    def make_house_solid(self, scale=0.72):
        """True gable-roof prism: wall 3×2, eave z=1.2, ridge x=1.5 z=2.2."""
        o = ORIGIN
        front_wall = self.iso_face([(0,0,0),(3,0,0),(3,0,1.2),(0,0,1.2)], o, scale, FRONT_FILL)
        right_wall = self.iso_face([(3,0,0),(3,2,0),(3,2,1.2),(3,0,1.2)], o, scale, SIDE_FILL)
        left_roof = self.iso_face([(0,0,1.2),(0,2,1.2),(1.5,2,2.2),(1.5,0,2.2)], o, scale, TOP_FILL)
        right_roof = self.iso_face([(3,0,1.2),(3,2,1.2),(1.5,2,2.2),(1.5,0,2.2)], o, scale, "#DFDFDF")
        gable = self.iso_face([(0,0,1.2),(3,0,1.2),(1.5,0,2.2)], o, scale, "#ECECEC")
        edges = VGroup(
            self.iso_edge((0,0,0),(3,0,0),o,scale),
            self.iso_edge((3,0,0),(3,2,0),o,scale),
            self.iso_edge((0,0,0),(0,0,1.2),o,scale),
            self.iso_edge((3,0,0),(3,0,1.2),o,scale),
            self.iso_edge((3,2,0),(3,2,1.2),o,scale),
            self.iso_edge((0,0,1.2),(3,0,1.2),o,scale),
            self.iso_edge((3,0,1.2),(3,2,1.2),o,scale),
            self.iso_edge((0,0,1.2),(0,2,1.2),o,scale),
            self.iso_edge((0,0,1.2),(1.5,0,2.2),o,scale),
            self.iso_edge((3,0,1.2),(1.5,0,2.2),o,scale),
            self.iso_edge((1.5,0,2.2),(1.5,2,2.2),o,scale),
            self.iso_edge((0,2,1.2),(1.5,2,2.2),o,scale),
            self.iso_edge((3,2,1.2),(1.5,2,2.2),o,scale),
        )
        return VGroup(VGroup(front_wall, right_wall, left_roof, right_roof, gable), edges)

    def _poly_units(self, pts, unit=1.0):
        poly = Polygon(
            *[np.array([x,y,0.0])*unit for x,y in pts],
            stroke_color=BLACK_LINE, stroke_width=2.5,
            fill_color=WHITE, fill_opacity=1,
        )
        poly.move_to(ORIGIN)
        return poly

    def view_front_step(self, scale=1.0):
        return self._poly_units([(0,0),(3,0),(3,1),(1.25,1),(1.25,2.10),(0,2.10)],0.92*scale)

    def view_rear_step(self, scale=1.0):
        return self.view_front_step(scale).copy().flip(axis=UP)

    def view_top_step(self, scale=1.0):
        u=0.92*scale
        outer=Rectangle(width=3*u,height=2*u,stroke_color=BLACK_LINE,stroke_width=2.5,fill_color=WHITE,fill_opacity=1)
        tower=Rectangle(width=1.25*u,height=1.10*u,stroke_color=BLACK_LINE,stroke_width=2.2,fill_opacity=0)
        tower.align_to(outer,LEFT).align_to(outer,DOWN)
        return VGroup(outer,tower)

    def view_bottom_step(self, scale=1.0):
        u=0.92*scale
        return Rectangle(width=3*u,height=2*u,stroke_color=BLACK_LINE,stroke_width=2.5,fill_color=WHITE,fill_opacity=1)

    def view_right_step(self, scale=1.0):
        return self._poly_units([(0,0),(2,0),(2,1),(1.10,1),(1.10,2.10),(0,2.10)],0.92*scale)

    def view_left_step(self, scale=1.0):
        return self.view_right_step(scale).copy().flip(axis=UP)

    def view_house_front(self, scale=1.0):
        return self._poly_units([(0,0),(3,0),(3,1.2),(1.5,2.2),(0,1.2)],0.90*scale)

    def view_house_top(self, scale=1.0):
        u=0.90*scale
        outer=Rectangle(width=3*u,height=2*u,stroke_color=BLACK_LINE,stroke_width=2.5,fill_color=WHITE,fill_opacity=1)
        ridge=Line(UP*u,DOWN*u,stroke_color=BLACK_LINE,stroke_width=2.0).move_to(outer)
        return VGroup(outer,ridge)

    def view_house_right(self, scale=1.0):
        u=0.90*scale
        outer=Rectangle(width=2*u,height=2.2*u,stroke_color=BLACK_LINE,stroke_width=2.5,fill_color=WHITE,fill_opacity=1)
        y=outer.get_bottom()[1]+1.2*u
        eave=Line([outer.get_left()[0],y,0],[outer.get_right()[0],y,0],stroke_color=BLACK_LINE,stroke_width=2.0)
        return VGroup(outer,eave)

    def framed_view(self, mob, label, width=2.2, height=1.65):
        box=RoundedRectangle(width=width,height=height,corner_radius=0.09,stroke_color=LIGHT_GRAY,stroke_width=1.4,fill_color=WHITE,fill_opacity=1)
        self.fit(mob,width-0.40,height-0.58)
        mob.move_to(box.get_center()+UP*0.10)
        lab=self.txt(label,18,BOLD).next_to(box,DOWN,buff=0.08)
        return VGroup(box,mob,lab)

    def projection_panel(self, system="A", scale=1.0):
        front=self.framed_view(self.view_front_step(0.43*scale),"FRONT")
        rear=self.framed_view(self.view_rear_step(0.43*scale),"REAR")
        top=self.framed_view(self.view_top_step(0.43*scale),"TOP")
        bottom=self.framed_view(self.view_bottom_step(0.43*scale),"BOTTOM")
        left=self.framed_view(self.view_left_step(0.43*scale),"LEFT")
        right=self.framed_view(self.view_right_step(0.43*scale),"RIGHT")
        front.move_to(ORIGIN)
        if system=="A":
            top.move_to(UP*1.80); bottom.move_to(DOWN*1.80)
            left.move_to(LEFT*2.55); right.move_to(RIGHT*2.55); rear.move_to(RIGHT*4.95)
        else:
            top.move_to(DOWN*1.80); bottom.move_to(UP*1.80)
            left.move_to(RIGHT*2.55); right.move_to(LEFT*2.55); rear.move_to(RIGHT*4.95)
        return VGroup(front,top,bottom,left,right,rear)

    def orthographic_triplet(self, front, top, right, system="A", gap=2.25):
        f=self.framed_view(front,"FRONT",3.0,2.25)
        t=self.framed_view(top,"TOP",3.0,2.25)
        r=self.framed_view(right,"RIGHT",3.0,2.25)
        f.move_to(ORIGIN)
        if system=="A":
            t.move_to(UP*gap); r.move_to(RIGHT*3.45)
        else:
            t.move_to(DOWN*gap); r.move_to(LEFT*3.45)
        return VGroup(f,t,r)

    def projection_rays(self, start, end, count=4):
        start=np.array(start); end=np.array(end); v=end-start
        perp=np.array([-v[1],v[0],0.0]); n=np.linalg.norm(perp)
        if n>1e-9: perp=perp/n
        return VGroup(*[
            DashedLine(start+k*perp,end+k*perp,dash_length=0.08,stroke_color=MID_GRAY,stroke_width=1.6)
            for k in np.linspace(-0.44,0.44,count)
        ])

    def dihedral_system(self):
        self.set_header("SISTEMA DIEDRICO", "Project the same solid orthogonally onto perpendicular FRONT and TOP planes, then unfold the planes.")
        solid=self.make_step_solid(0.78).move_to(LEFT*4.70+DOWN*0.55)
        triad=self.triad(0.76).next_to(solid,DOWN+LEFT,buff=0.18)
        obj=self.chip("ONE COHERENT 3D OBJECT",4.0,22).next_to(solid,UP,buff=0.38)
        self.play(FadeIn(solid,shift=UP*0.12),FadeIn(obj),FadeIn(triad),run_time=RUN_SLOW)
        self.wait(PAUSE_R)

        vplane=Rectangle(width=4.4,height=4.35,stroke_color=MID_GRAY,stroke_width=1.8,fill_color=VERY_LIGHT,fill_opacity=0.35).move_to(RIGHT*3.45+UP*0.25)
        hplane=Polygon([1.15,-0.30,0],[5.55,-0.30,0],[6.45,-1.70,0],[2.05,-1.70,0],stroke_color=MID_GRAY,stroke_width=1.8,fill_color=VERY_LIGHT,fill_opacity=0.42)
        hinge=Line([1.15,-2.05,0],[1.15,2.45,0],stroke_color=BLACK_LINE,stroke_width=2.0)
        front=self.view_front_step(0.60).move_to(vplane.get_center()+UP*0.10)
        top=self.view_top_step(0.57).move_to(RIGHT*3.85+DOWN*1.15)
        vlab=self.chip("VERTICAL PLANE · FRONT",4.1,20).move_to(RIGHT*3.45+UP*2.55)
        hlab=self.chip("HORIZONTAL PLANE · TOP",4.2,20).move_to(RIGHT*3.85+DOWN*2.40)
        self.play(Create(vplane),Create(hplane),Create(hinge),FadeIn(vlab),FadeIn(hlab),run_time=RUN_SLOW)

        rf=self.projection_rays(solid.get_right()+RIGHT*0.10,front.get_left()+LEFT*0.10,5)
        rt=self.projection_rays(solid.get_top()+RIGHT*0.05,top.get_left()+LEFT*0.05,4)
        self.play(LaggedStart(*[Create(r) for r in rf],lag_ratio=0.08),run_time=RUN_FOLD)
        self.play(Create(front),run_time=RUN)
        self.play(LaggedStart(*[Create(r) for r in rt],lag_ratio=0.08),run_time=RUN_FOLD)
        self.play(Create(top),run_time=RUN)
        self.wait(PAUSE_E)

        cue=self.chip("UNFOLD 90° -> ONE DRAWING SHEET",5.4,21).move_to(RIGHT*3.0+DOWN*3.10)
        f2=front.copy().move_to(RIGHT*3.05+DOWN*0.45)
        t2=top.copy().move_to(RIGHT*3.05+UP*1.75)
        self.play(FadeIn(cue),run_time=RUN)
        self.play(TransformFromCopy(front,f2),TransformFromCopy(top,t2),run_time=RUN_FOLD)
        self.wait(PAUSE_W)
        self.clear_content()

    def projection_systems(self):
        self.set_header("SISTEMAS DE PROYECCION", "The 3D object is fixed. ISO A / ISO E change only where the extracted views are placed on the sheet.")
        solid=self.make_step_solid(0.72).move_to(DOWN*0.50)
        self.play(FadeIn(solid,shift=UP*0.10),run_time=RUN_SLOW)
        center=solid.get_center()
        dirs=[
            (UP*2.45,"TOP"),(DOWN*2.45,"BOTTOM"),
            (np.array([3.25,-1.55,0]),"FRONT"),(np.array([-3.25,1.55,0]),"REAR"),
            (np.array([-3.25,-1.55,0]),"LEFT"),(np.array([3.25,1.55,0]),"RIGHT"),
        ]
        arrows=VGroup(); labels=VGroup()
        for vec,lab in dirs:
            arrows.add(Arrow(center+vec,center,buff=0.70,color=MID_GRAY,stroke_width=2,max_tip_length_to_length_ratio=0.10))
            labels.add(self.chip(lab,2.15,20).move_to(center+vec*1.03))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=0.08),run_time=RUN_SLOW*1.7)
        self.play(LaggedStart(*[FadeIn(l) for l in labels],lag_ratio=0.08),run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def types_of_views(self):
        self.set_header("TIPOS DE VISTA", "Opposite observation directions generate six distinct principal views: front/rear, left/right and top/bottom.")
        solid=self.make_step_solid(0.76).move_to(LEFT*3.65+DOWN*0.45)
        pairs=VGroup(
            self.card("FRONT <-> REAR",["opposite directions","rear silhouette mirrors front"],width=5.7,body_size=21),
            self.card("LEFT <-> RIGHT",["opposite directions","side silhouettes mirror"],width=5.7,body_size=21),
            self.card("TOP <-> BOTTOM",["top shows tower footprint","bottom shows base footprint"],width=5.7,body_size=21),
        ).arrange(DOWN,buff=0.26).move_to(RIGHT*3.55+DOWN*0.25)
        self.play(FadeIn(solid),run_time=RUN)
        self.play(LaggedStart(*[FadeIn(p,shift=LEFT*0.10) for p in pairs],lag_ratio=0.15),run_time=RUN_SLOW*1.7)
        self.wait(PAUSE_R)
        views=VGroup(
            self.view_front_step(0.35),self.view_rear_step(0.35),self.view_left_step(0.35),
            self.view_right_step(0.35),self.view_top_step(0.35),self.view_bottom_step(0.35),
        ).arrange_in_grid(rows=2,cols=3,buff=(0.34,0.34)).move_to(RIGHT*3.55+DOWN*0.25)
        self.play(FadeOut(pairs),run_time=RUN_Q)
        self.play(LaggedStart(*[Create(v) for v in views],lag_ratio=0.10),run_time=RUN_SLOW*1.6)
        self.wait(PAUSE_E)
        self.clear_content()

    def iso_a_rules(self):
        self.set_header("ISO A · THIRD-ANGLE / AMERICAN", "With FRONT fixed, neighboring views stay on the same side from which the object is observed.")
        panel=self.projection_panel("A",0.92).move_to(LEFT*2.55+DOWN*0.45)
        rules=self.card("PLACEMENT RULES",[
            "Top view     -> above","Bottom view  -> below","Left view    -> left","Right view   -> right","Rear view    -> left or right",
        ],width=5.0,body_size=22).move_to(RIGHT*5.15+DOWN*0.20)
        self.play(Create(panel[0]),run_time=RUN)
        self.play(LaggedStart(*[Create(v) for v in panel[1:]],lag_ratio=0.12),run_time=RUN_SLOW*1.9)
        self.play(FadeIn(rules),run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_rules(self):
        self.set_header("ISO E · FIRST-ANGLE / EUROPEAN", "With FRONT fixed, neighboring views appear on the opposite side after the projection planes unfold.")
        panel=self.projection_panel("E",0.92).move_to(LEFT*2.55+DOWN*0.45)
        rules=self.card("PLACEMENT RULES",[
            "Top view     -> below","Bottom view  -> above","Left view    -> right","Right view   -> left","Rear view    -> left or right",
        ],width=5.0,body_size=22).move_to(RIGHT*5.15+DOWN*0.20)
        self.play(Create(panel[0]),run_time=RUN)
        self.play(LaggedStart(*[Create(v) for v in panel[1:]],lag_ratio=0.12),run_time=RUN_SLOW*1.9)
        self.play(FadeIn(rules),run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def _example_triplet(self, solid, trip, cues=None):
        self.play(FadeIn(solid,shift=UP*0.10),run_time=RUN_SLOW)
        self.wait(PAUSE_R)
        for i,word in enumerate(("FRONT","TOP","RIGHT")):
            cue=self.chip(f"PROJECT {word}",3.15,20).move_to(LEFT*4.55+DOWN*2.68)
            rays=self.projection_rays(solid.get_right()+RIGHT*0.05,trip[i].get_left()+LEFT*0.08,4)
            self.play(FadeIn(cue),LaggedStart(*[Create(r) for r in rays],lag_ratio=0.07),run_time=RUN_FOLD)
            self.play(Create(trip[i]),run_time=RUN)
            self.play(FadeOut(rays),FadeOut(cue),run_time=RUN_Q)

    def iso_a_example_1(self):
        self.set_header("EJEMPLO ISO A · 1", "A true gable-roof solid produces coherent FRONT, TOP and RIGHT views in third-angle placement.")
        solid=self.make_house_solid(0.78).move_to(LEFT*4.55+DOWN*0.50)
        trip=self.orthographic_triplet(self.view_house_front(0.62),self.view_house_top(0.62),self.view_house_right(0.62),"A",2.25).move_to(RIGHT*2.55+DOWN*0.30)
        self._example_triplet(solid,trip)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_a_example_2(self):
        self.set_header("EJEMPLO ISO A · 2", "The stepped solid keeps exact 3×2×2.10 proportions and its 1.25×1.10 tower footprint in every view.")
        solid=self.make_step_solid(0.82).move_to(LEFT*4.55+DOWN*0.50)
        trip=self.orthographic_triplet(self.view_front_step(0.63),self.view_top_step(0.63),self.view_right_step(0.63),"A",2.25).move_to(RIGHT*2.55+DOWN*0.30)
        self._example_triplet(solid,trip)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_example_1(self):
        self.set_header("EJEMPLO ISO E · 1", "Use the same stepped solid and the same extracted views; only their positions change in first-angle projection.")
        solid=self.make_step_solid(0.82).move_to(LEFT*4.55+DOWN*0.50)
        trip=self.orthographic_triplet(self.view_front_step(0.63),self.view_top_step(0.63),self.view_right_step(0.63),"E",2.18).move_to(RIGHT*2.65+DOWN*0.25)
        cue=self.card("FIRST-ANGLE CUE",["TOP goes below FRONT","RIGHT view goes to the left"],width=4.6,body_size=21).move_to(LEFT*4.55+DOWN*2.55)
        self.play(FadeIn(solid),FadeIn(cue),run_time=RUN_SLOW)
        self.play(Create(trip[0]),run_time=RUN)
        self.play(Create(trip[1]),run_time=RUN)
        self.play(Create(trip[2]),run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_example_2(self):
        self.set_header("EJEMPLO ISO E · 2", "The gable-roof geometry is unchanged; identify the first-angle symbol before placing the views.")
        solid=self.make_house_solid(0.78).move_to(LEFT*4.55+DOWN*0.50)
        trip=self.orthographic_triplet(self.view_house_front(0.62),self.view_house_top(0.62),self.view_house_right(0.62),"E",2.18).move_to(RIGHT*2.65+DOWN*0.25)
        sym=self.first_third_symbol(False,0.74).move_to(LEFT*4.55+DOWN*2.60)
        self.play(FadeIn(solid),FadeIn(sym),run_time=RUN_SLOW)
        self.play(LaggedStart(Create(trip[0]),Create(trip[1]),Create(trip[2]),lag_ratio=0.18),run_time=RUN_FOLD)
        self.wait(PAUSE_W)
        self.clear_content()


# Preview: manim -pql Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V2_SENIOR_QA.py TechnicalDrawingClass6ISOV2 --disable_caching
# Final:   manim -pqh Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V2_SENIOR_QA.py TechnicalDrawingClass6ISOV2 --disable_caching
