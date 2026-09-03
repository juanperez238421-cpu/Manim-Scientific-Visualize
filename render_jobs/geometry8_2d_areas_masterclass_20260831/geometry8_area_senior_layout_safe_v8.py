#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V8 Senior layout-safe QA layer.

This pass is based on direct inspection of the rendered V7 PQH video, not only
source review.  It introduces explicit spatial cells / safe zones for text and
mathematics, then fixes the remaining rendered collisions:

* worked-example READ GIVEN rows overlapping their values;
* rectangle derivation text touching the height arrow;
* parallelogram warning clipped by the left frame edge;
* rhombus D / d labels colliding at the diagonal intersection;
* circle derivation labels competing with the base dimension / formula box;
* formula-guide symbol notes touching card borders and figure labels.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaSeniorLayoutSafeV8Mixin:
    """Rendered-frame safe-zone overrides on top of V7."""

    # ------------------------------------------------------------------
    # Senior layout primitives
    # ------------------------------------------------------------------
    def _panel_cell(self, mobj, panel, x0, x1, y, max_h, pad=.04):
        """Fit and center ``mobj`` inside a panel-relative rectangular cell.

        x0/x1 are coordinates relative to panel center.  This function is used
        instead of ad-hoc next_to chains so long strings cannot intrude into a
        neighbouring cell after font / LaTeX metrics are resolved.
        """
        assert x1 > x0
        self.fit(mobj, (x1 - x0) - 2*pad, max_h)
        mobj.move_to(panel.get_center() + RIGHT*((x0+x1)/2) + UP*y)
        return mobj

    def _assert_gap(self, left_obj, right_obj, min_gap=.10):
        """Geometry gate used by the render source before animation starts."""
        assert right_obj.get_left()[0] - left_obj.get_right()[0] >= min_gap

    def _safe_note_box(self, text, center, width, height=.58, size=23):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=.09,
            stroke_color=LIGHT,
            stroke_width=1.5,
            fill_color=WHITE,
            fill_opacity=.98,
        ).move_to(center)
        t = self.txt(text, size, True)
        self.fit(t, width-.28, height-.16)
        t.move_to(box)
        return VGroup(box, t)

    # ------------------------------------------------------------------
    # Global worked-example grid — fixes every long GIVEN string at once
    # ------------------------------------------------------------------
    def _example_step_row(self, number, label, value, panel, y_offset):
        badge = RoundedRectangle(
            width=.58,
            height=.34,
            corner_radius=.07,
            stroke_color=INK,
            stroke_width=1.3,
            fill_color=PAPER,
            fill_opacity=1,
        )
        num = self.txt(number, 16, True).move_to(badge)
        lab = self.txt(label, 17, True).set_opacity(.74)
        heading = VGroup(VGroup(badge, num), lab).arrange(RIGHT, buff=.09)

        # Explicit non-overlapping cells.  The divider is not a positioning
        # anchor; both objects are independently constrained to their cells.
        self._panel_cell(heading, panel, -3.02, -.82, y_offset, .40)

        divider_x = -.62
        divider = Line(
            panel.get_center() + RIGHT*divider_x + UP*(y_offset-.29),
            panel.get_center() + RIGHT*divider_x + UP*(y_offset+.29),
            color=LIGHT,
            stroke_width=1.2,
        )

        self._panel_cell(value, panel, -.38, 3.02, y_offset, .50)
        self._assert_gap(heading, value, .13)
        assert value.get_right()[0] <= panel.get_right()[0] - .12
        assert heading.get_left()[0] >= panel.get_left()[0] + .12
        return VGroup(heading, divider, value)

    def example_stack(self, given, formula, substitution, result, width=6.15):
        width = max(width, 6.46)
        panel = RoundedRectangle(
            width=width,
            height=5.04,
            corner_radius=.14,
            stroke_color=LIGHT,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=.988,
        )

        title = self.txt("WORKED EXAMPLE", 31, True)
        title.move_to(panel.get_center() + UP*2.12)

        guide = self.txt("READ  →  FORMULA  →  SUBSTITUTE  →  ANSWER", 18, True).set_opacity(.58)
        self.fit(guide, width-.62, .30)
        guide.move_to(panel.get_center() + UP*1.76)

        top_rule = Line(
            panel.get_left()+RIGHT*.24+UP*1.51,
            panel.get_right()+LEFT*.24+UP*1.51,
            color=LIGHT,
            stroke_width=1.2,
        )

        # Given strings are deliberately a little smaller than formulas.  Long
        # trapezoid / polygon givens are fitted inside the same right cell.
        given_m = self.txt(given, 25)
        formula_m = self.eq(formula, 40)
        sub_m = self.eq(substitution, 38)
        answer_m = self.box(result, 2.92, 41)

        row1 = self._example_step_row("01", "READ GIVEN", given_m, panel, 1.08)
        row2 = self._example_step_row("02", "CHOOSE FORMULA", formula_m, panel, .30)
        row3 = self._example_step_row("03", "SUBSTITUTE", sub_m, panel, -.48)
        row4 = self._example_step_row("04", "CALCULATE", answer_m, panel, -1.27)

        check = self.txt("✓ Answer written in square units", 19, True).set_opacity(.75)
        self.fit(check, width-.82, .32)
        check.move_to(panel.get_center() + DOWN*2.13)

        # Vertical safety assertions keep the footer away from the last row.
        assert row4.get_bottom()[1] > check.get_top()[1] + .12
        content = VGroup(title, guide, top_rule, row1, row2, row3, row4, check)
        return VGroup(panel, content)

    def show_example(self, stack, right_x=3.50):
        # Slight left shift gives the widened panel a reliable right-frame margin.
        stack.move_to(RIGHT*right_x + DOWN*.40)
        panel, content = stack
        assert panel.get_right()[0] < config.frame_x_radius - .12

        self.play(FadeIn(panel, shift=UP*.03), run_time=.38)
        self.play(FadeIn(content[0], shift=UP*.02), run_time=.34)
        self.play(FadeIn(content[1]), Create(content[2]), run_time=.36)
        self.wait(.55)

        pauses = (.90, 1.00, 1.05, 1.30)
        for row, pause in zip(content[3:7], pauses):
            self.play(FadeIn(row, shift=UP*.025), run_time=.44)
            self.wait(pause)

        self.play(FadeIn(content[7], shift=UP*.02), run_time=.34)
        self.wait(2.00)

    # ------------------------------------------------------------------
    # Rectangle — derivation now lives in a dedicated right-side panel
    # ------------------------------------------------------------------
    def rectangle_explicit(self):
        h = self.header(5, "2 · RECTANGLE", "Opposite sides are equal; base and perpendicular height count columns and rows.")
        strip = self.stage_strip(); self.add(h, strip)

        A=np.array([-5.65,-1.20,0]); B=np.array([-1.15,-1.20,0]); C=np.array([-1.15,1.25,0]); D=np.array([-5.65,1.25,0])
        base=Line(A,B,color=INK,stroke_width=5); side=Line(B,C,color=INK,stroke_width=5); top=Line(C,D,color=INK,stroke_width=5); left=Line(D,A,color=INK,stroke_width=5)
        fill=Polygon(A,B,C,D,stroke_opacity=0,fill_color=FILL,fill_opacity=.62)

        self.mark_stage(strip,0)
        self.play(Create(base), run_time=.55)
        self.play(Create(side), Create(top), Create(left), run_time=.80)
        self.play(FadeIn(fill), run_time=.35)

        self.mark_stage(strip,1)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        dh=self.dimension(B+RIGHT*.35,C+RIGHT*.35,"h",RIGHT)
        right=VGroup(self.right_mark(A),self.right_mark(B,LEFT,UP),self.right_mark(C,LEFT,DOWN),self.right_mark(D,RIGHT,DOWN))
        self.play(GrowFromCenter(db[0]),GrowFromCenter(dh[0]),FadeIn(db[1]),FadeIn(dh[1]),FadeIn(right),run_time=.70)

        self.mark_stage(strip,2)
        panel = RoundedRectangle(
            width=5.72, height=2.82, corner_radius=.12,
            stroke_color=LIGHT, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=.97,
        ).move_to(RIGHT*4.02+DOWN*.05)
        idea=self.txt("b unit columns repeated through h unit rows",26,True)
        self.fit(idea,5.10,.48); idea.move_to(panel.get_center()+UP*.88)
        repeated=self.eq(r"A=\underbrace{b+b+\cdots+b}_{h\ \text{rows}}",39).move_to(panel.get_center()+UP*.10)
        formula=self.box(r"A=b\,h",4.65,59).move_to(panel.get_center()+DOWN*.83)
        deriv=VGroup(panel,idea,repeated,formula)
        assert deriv.get_left()[0] > dh.get_right()[0] + .25
        self.play(FadeIn(panel),run_time=.28)
        for item in (idea,repeated,formula):
            self.play(FadeIn(item,shift=UP*.02),run_time=.38); self.wait(.28)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.35)
        ex=self.example_stack("Given: b = 8 cm, h = 3 cm",r"A=b\,h",r"A=(8)(3)",r"A=24\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    # ------------------------------------------------------------------
    # Parallelogram — preserve V5 exact cut/translation, fix clipped warning
    # ------------------------------------------------------------------
    def parallelogram_explicit(self):
        h = self.header(7,"4 · PARALLELOGRAM","A cut-and-translate preserves area and turns the slanted figure into a rectangle.")
        strip = self.stage_strip(); self.add(h, strip)

        y0=-1.35; height=2.70; shear=1.00; base=4.40
        A=np.array([-5.80,y0,0.0]); E=A+RIGHT*shear; D=E+UP*height
        B=A+RIGHT*base; F=E+RIGHT*base; C=D+RIGHT*base
        translation=B-A
        assert np.allclose(E+translation,F) and np.allclose(D+translation,C)

        full=Polygon(A,B,C,D,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)
        self.mark_stage(strip,0); self.play(Create(full),run_time=.70)

        self.mark_stage(strip,1)
        db=self.dimension(A+DOWN*.35,B+DOWN*.35,"b",DOWN)
        alt=DashedLine(D,E,color=MID,stroke_width=3)
        dh=self.dimension(E+LEFT*.30,D+LEFT*.30,"h",LEFT)
        slanted=self._safe_note_box("slanted side ≠ h", LEFT*1.88+UP*1.86, 2.72, .56, 23)
        assert slanted.get_left()[0] > A[0] + 1.60
        assert slanted.get_bottom()[1] > D[1] + .20
        self.play(GrowFromCenter(db[0]),FadeIn(db[1]),Create(alt),GrowFromCenter(dh[0]),FadeIn(dh[1]),FadeIn(slanted),run_time=.78)

        self.mark_stage(strip,2)
        left_piece=Polygon(A,E,D,stroke_color=INK,stroke_width=4,fill_color=WHITE,fill_opacity=1)
        remain=Polygon(E,B,C,D,stroke_color=INK,stroke_width=4,fill_color=FILL,fill_opacity=.66)
        self.play(FadeOut(full),FadeIn(left_piece),FadeIn(remain),FadeOut(slanted),run_time=.42)
        motion=Arrow(left_piece.get_center()+UP*1.80,left_piece.get_center()+UP*1.80+translation,buff=.05,color=MID,stroke_width=3)
        self.play(GrowArrow(motion),run_time=.35)
        self.play(left_piece.animate.shift(translation),run_time=1.10,rate_func=smooth)

        final_fill=Polygon(E,F,C,D,stroke_opacity=0,fill_color=FILL,fill_opacity=.66)
        join=Line(B,C,color=INK,stroke_width=3.2)
        rect=Polygon(E,F,C,D,stroke_color=INK,stroke_width=5,fill_opacity=0)
        self.play(FadeOut(motion),left_piece.animate.set_stroke(opacity=0),remain.animate.set_stroke(opacity=0),FadeIn(final_fill),run_time=.30)
        self.play(Create(join),run_time=.28); self.play(Create(rect),run_time=.40)
        rect_db=self.dimension(E+DOWN*.35,F+DOWN*.35,"b",DOWN)
        self.play(FadeOut(db),GrowFromCenter(rect_db[0]),FadeIn(rect_db[1]),run_time=.38)

        deriv=VGroup(self.txt("Same pieces → same area as a rectangle",27,True),self.box(r"A=b\,h",5.3,62)).arrange(DOWN,buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv),run_time=.55)
        self.mark_stage(strip,3); self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: b = 7 cm, h = 4 cm",r"A=b\,h",r"A=(7)(4)",r"A=28\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    # ------------------------------------------------------------------
    # Rhombus — separate D, d and the right-angle marker
    # ------------------------------------------------------------------
    def rhombus_explicit(self):
        h=self.header(9,"6 · RHOMBUS","The diagonals D and d cross at right angles and divide the rhombus into four triangles.")
        strip=self.stage_strip(); self.add(h,strip)

        L=np.array([-5.60,0,0]); T=np.array([-3.55,1.70,0]); R=np.array([-1.50,0,0]); Bm=np.array([-3.55,-1.70,0]); O=np.array([-3.55,0,0])
        rh=Polygon(L,T,R,Bm,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)
        self.mark_stage(strip,0); self.play(Create(rh),run_time=.72)

        self.mark_stage(strip,1)
        Dline=DashedLine(L,R,color=INK,stroke_width=2.8); dline=DashedLine(Bm,T,color=INK,stroke_width=2.8)
        Dlab=self.eq("D",34).move_to(O+LEFT*.92+UP*.25)
        dlab=self.eq("d",34).move_to(O+RIGHT*.28+UP*.92)
        right_mark=self.right_mark(O)
        assert Dlab.get_right()[0] < right_mark.get_left()[0] - .08
        assert dlab.get_bottom()[1] > right_mark.get_top()[1] + .08
        self.play(Create(Dline),Create(dline),FadeIn(Dlab),FadeIn(dlab),FadeIn(right_mark),run_time=.72)

        self.mark_stage(strip,2)
        triangles=VGroup(
            Polygon(O,T,R,stroke_color=MID,stroke_width=2,fill_color=WHITE,fill_opacity=.25),
            Polygon(O,R,Bm,stroke_color=MID,stroke_width=2,fill_color=PAPER,fill_opacity=.25),
            Polygon(O,Bm,L,stroke_color=MID,stroke_width=2,fill_color=WHITE,fill_opacity=.25),
            Polygon(O,L,T,stroke_color=MID,stroke_width=2,fill_color=PAPER,fill_opacity=.25),
        )
        self.play(LaggedStart(*[FadeIn(t) for t in triangles],lag_ratio=.10),run_time=.65)
        deriv=VGroup(self.eq(r"A=4\left[\frac12\left(\frac D2\right)\left(\frac d2\right)\right]",37),self.box(r"A=\frac{D\,d}{2}",5.5,60)).arrange(DOWN,buff=.28).move_to(RIGHT*3.55)
        self.play(FadeIn(deriv[0]),run_time=.45); self.wait(.35); self.play(FadeIn(deriv[1]),run_time=.45)

        self.mark_stage(strip,3); self.play(FadeOut(deriv),run_time=.32)
        ex=self.example_stack("Given: D = 12 cm, d = 8 cm",r"A=\frac{D\,d}{2}",r"A=\frac{(12)(8)}{2}",r"A=48\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    # ------------------------------------------------------------------
    # Circle — establish independent vertical bands on the derivation side
    # ------------------------------------------------------------------
    def circle_explicit(self):
        h=self.header(10,"7 · CIRCLE","The radius generates the circle; sector rearrangement connects circumference to area.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-4.05,-.25,0]); radius=1.62
        circle=Circle(radius,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.18).move_to(center)
        sweep=Line(center,center+RIGHT*radius,color=INK,stroke_width=4); dot=Dot(center,radius=.07,color=INK)
        self.mark_stage(strip,0)
        self.play(FadeIn(dot),Create(sweep),run_time=.42)
        self.play(Create(circle),Rotate(sweep,angle=TAU,about_point=center),run_time=1.15,rate_func=linear)

        self.mark_stage(strip,1)
        diameter=DashedLine(center+LEFT*radius,center+RIGHT*radius,color=MID,stroke_width=2.8)
        rlab=self.eq("r",38).next_to(Line(center,center+RIGHT*radius),UP,buff=.06)
        dlab=self.eq("d=2r",35).next_to(diameter,DOWN,buff=.10)
        self.play(Create(diameter),FadeIn(rlab),FadeIn(dlab),run_time=.60)

        self.mark_stage(strip,2)
        n=16; theta=TAU/n; sectors=VGroup()
        for k in range(n):
            sectors.add(Sector(arc_center=center,radius=radius,start_angle=k*theta,angle=theta,stroke_color=INK,stroke_width=1.4,fill_color=FILL if k%2==0 else PAPER,fill_opacity=.72 if k%2==0 else .92))
        source_outline=Circle(radius,color=LIGHT,stroke_width=2.0,fill_opacity=0).move_to(center)
        self.play(FadeOut(circle),FadeIn(source_outline),FadeIn(sectors),run_time=.55)

        divide_note=self.txt("Divide the circle into equal sectors.",26,True)
        self.fit(divide_note,5.4,.44); divide_note.move_to(RIGHT*3.72+UP*1.58)
        self.play(FadeIn(divide_note),run_time=.35); self.wait(.35)

        step=(math.pi*radius)/n; x0=.72; targets=VGroup()
        for i in range(n):
            x=x0+i*step
            if i%2==0:
                apex=np.array([x,-radius/2,0]); start=PI/2-theta/2
            else:
                apex=np.array([x,radius/2,0]); start=3*PI/2-theta/2
            targets.add(Sector(arc_center=apex,radius=radius,start_angle=start,angle=theta,stroke_color=INK,stroke_width=1.25,fill_color=FILL if i%2==0 else PAPER,fill_opacity=.72 if i%2==0 else .92))
        self.play(LaggedStart(*[Transform(sectors[i],targets[i]) for i in range(n)],lag_ratio=.025),FadeOut(divide_note),run_time=1.65,rate_func=smooth)

        limit_note=self.txt("More sectors → straighter top and bottom edges",24,True)
        self.fit(limit_note,5.45,.42); limit_note.move_to(RIGHT*3.72+UP*1.64)
        base_note=self.eq(r"\frac{C}{2}=\frac{2\pi r}{2}=\pi r",37).move_to(RIGHT*3.72+UP*.98)
        self.play(FadeIn(limit_note),FadeIn(base_note),run_time=.55)

        left_x=x0-.10; right_x=x0+(n-1)*step+.16
        base_dim=self.dimension([left_x,-1.16,0],[right_x,-1.16,0],r"\pi r",DOWN,33)
        height_dim=self.dimension([right_x+.35,-radius/2,0],[right_x+.35,radius/2,0],"r",RIGHT,34)
        self.play(GrowFromCenter(base_dim[0]),FadeIn(base_dim[1]),GrowFromCenter(height_dim[0]),FadeIn(height_dim[1]),run_time=.60)

        formula=self.box(r"A=(\pi r)(r)=\pi r^2",5.65,53).move_to(RIGHT*3.55+DOWN*2.62)
        assert formula.get_top()[1] < base_dim[1].get_bottom()[1] - .18
        self.play(FadeIn(formula),run_time=.45); self.wait(.95)

        self.mark_stage(strip,3)
        self.play(FadeOut(sectors),FadeOut(base_dim),FadeOut(height_dim),FadeOut(limit_note),FadeOut(base_note),FadeOut(formula),run_time=.36)
        self.play(source_outline.animate.set_stroke(INK,width=4),run_time=.25)
        ex=self.example_stack("Given: r = 4 cm",r"A=\pi r^2",r"A=\pi(4)^2=16\pi",r"A\approx50.27\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    # ------------------------------------------------------------------
    # Formula guide — strict title / figure / formula / symbols bands
    # ------------------------------------------------------------------
    def _formula_card_v8(self, kind, name, formula, symbols):
        card=RoundedRectangle(width=6.95,height=1.62,corner_radius=.12,stroke_color=INK,stroke_width=1.7,fill_color=WHITE,fill_opacity=1)
        number=self.txt(kind,21,True); title=self.txt(name,23,True)
        title_row=VGroup(number,title).arrange(RIGHT,buff=.15)
        self.fit(title_row,2.72,.34); title_row.move_to(card.get_center()+LEFT*1.97+UP*.52)

        figure_center=card.get_center()+LEFT*2.02+DOWN*.22
        f=VGroup()
        if name=="SQUARE":
            shape=Square(.72,color=INK,stroke_width=2.5).move_to(figure_center)
            dim=self._mini_dimension(shape.get_corner(DL)+DOWN*.10,shape.get_corner(DR)+DOWN*.10,"s",DOWN,20)
            side=self.eq("s",20).next_to(shape,RIGHT,buff=.05); f=VGroup(shape,dim,side)
        elif name=="RECTANGLE":
            shape=Rectangle(width=1.10,height=.64,color=INK,stroke_width=2.5).move_to(figure_center)
            db=self._mini_dimension(shape.get_corner(DL)+DOWN*.10,shape.get_corner(DR)+DOWN*.10,"b",DOWN,20)
            dh=self._mini_dimension(shape.get_corner(DR)+RIGHT*.10,shape.get_corner(UR)+RIGHT*.10,"h",RIGHT,20); f=VGroup(shape,db,dh)
        elif name=="TRIANGLE":
            a=figure_center+LEFT*.58+DOWN*.29; b=figure_center+RIGHT*.58+DOWN*.29; c=figure_center+UP*.39
            shape=Polygon(a,b,c,color=INK,stroke_width=2.5); foot=np.array([c[0],a[1],0]); alt=DashedLine(c,foot,color=MID,stroke_width=1.6)
            right=Square(.12,color=INK,stroke_width=1.2).move_to(foot+UR*.06); db=self._mini_dimension(a+DOWN*.10,b+DOWN*.10,"b",DOWN,20); hlab=self.eq("h",20).next_to(alt,RIGHT,buff=.03); f=VGroup(shape,alt,right,db,hlab)
        elif name=="PARALLELOGRAM":
            a=figure_center+LEFT*.63+DOWN*.29; b=figure_center+RIGHT*.46+DOWN*.29; c=b+RIGHT*.19+UP*.62; d=a+RIGHT*.19+UP*.62
            shape=Polygon(a,b,c,d,color=INK,stroke_width=2.5); foot=np.array([d[0],a[1],0]); alt=DashedLine(d,foot,color=MID,stroke_width=1.6)
            db=self._mini_dimension(a+DOWN*.10,b+DOWN*.10,"b",DOWN,20); hlab=self.eq("h",20).next_to(alt,RIGHT,buff=.03); f=VGroup(shape,alt,db,hlab)
        elif name=="TRAPEZOID":
            a=figure_center+LEFT*.64+DOWN*.28; b=figure_center+RIGHT*.64+DOWN*.28; c=figure_center+RIGHT*.39+UP*.29; d=figure_center+LEFT*.39+UP*.29
            shape=Polygon(a,b,c,d,color=INK,stroke_width=2.5)
            top_lab=self.eq("b",19).next_to(Line(d,c),UP,buff=.02); bot_lab=self.eq("B",19).next_to(Line(a,b),DOWN,buff=.02)
            foot=np.array([d[0],a[1],0]); alt=DashedLine(d,foot,color=MID,stroke_width=1.5); hlab=self.eq("h",19).next_to(alt,RIGHT,buff=.02)
            f=VGroup(shape,top_lab,bot_lab,alt,hlab)
        elif name=="RHOMBUS":
            l=figure_center+LEFT*.62; r=figure_center+RIGHT*.62; u=figure_center+UP*.40; d=figure_center+DOWN*.40
            shape=Polygon(l,u,r,d,color=INK,stroke_width=2.5); hd=DashedLine(l,r,color=MID,stroke_width=1.4); vd=DashedLine(d,u,color=MID,stroke_width=1.4)
            D=self.eq("D",18).move_to(figure_center+LEFT*.30+UP*.12); dd=self.eq("d",18).move_to(figure_center+RIGHT*.13+UP*.30); f=VGroup(shape,hd,vd,D,dd)
        elif name=="CIRCLE":
            shape=Circle(.48,color=INK,stroke_width=2.5).move_to(figure_center); c=Dot(figure_center,radius=.032,color=INK)
            rline=Line(figure_center,figure_center+UR*.34,color=INK,stroke_width=1.9); rlab=self.eq("r",19).next_to(rline,UP,buff=.01)
            diam=DashedLine(figure_center+LEFT*.48,figure_center+RIGHT*.48,color=MID,stroke_width=1.4); dlab=self.eq("d",18).next_to(diam,DOWN,buff=.02); f=VGroup(shape,c,rline,rlab,diam,dlab)
        elif name=="REGULAR POLYGON":
            shape=RegularPolygon(6,radius=.51,color=INK,stroke_width=2.5).move_to(figure_center); c=Dot(figure_center,radius=.032,color=INK)
            ap=Line(figure_center,figure_center+DOWN*.43,color=INK,stroke_width=1.7); alab=self.eq("a",19).next_to(ap,RIGHT,buff=.02)
            plab=self.eq("P",18).next_to(shape,RIGHT,buff=.03); f=VGroup(shape,c,ap,alab,plab)
        elif name=="SEMICIRCLE":
            arc=Arc(radius=.53,start_angle=0,angle=PI,color=INK,stroke_width=2.5,arc_center=figure_center+DOWN*.11)
            base=Line(figure_center+LEFT*.53+DOWN*.11,figure_center+RIGHT*.53+DOWN*.11,color=INK,stroke_width=2.5); c=Dot(figure_center+DOWN*.11,radius=.03,color=INK)
            rline=Line(figure_center+DOWN*.11,figure_center+UR*.34,color=INK,stroke_width=1.7); rlab=self.eq("r",19).next_to(rline,UP,buff=.01); f=VGroup(arc,base,c,rline,rlab)
        elif name=="QUARTER CIRCLE":
            center=figure_center+LEFT*.18+DOWN*.20; arc=Arc(radius=.58,start_angle=0,angle=PI/2,color=INK,stroke_width=2.5,arc_center=center)
            hh=Line(center,center+RIGHT*.58,color=INK,stroke_width=2.5); vv=Line(center,center+UP*.58,color=INK,stroke_width=2.5)
            rlab=self.eq("r",19).move_to(center+UR*.29); f=VGroup(arc,hh,vv,rlab)

        # Figure band remains clear of the title band and card border.
        self.fit(f,2.45,.88)
        f.move_to(figure_center)

        formula_box=RoundedRectangle(width=2.88,height=.70,corner_radius=.08,stroke_color=LIGHT,stroke_width=1.35,fill_color=PAPER,fill_opacity=1)
        fm=self.eq(formula,32); self.fit(fm,2.52,.49); fm.move_to(formula_box)
        formula_group=VGroup(formula_box,fm).move_to(card.get_center()+RIGHT*1.84+UP*.09)

        sym=self.txt(symbols,17)
        self.fit(sym,2.78,.25); sym.move_to(card.get_center()+RIGHT*1.84+DOWN*.51)
        assert sym.get_bottom()[1] > card.get_bottom()[1] + .10
        assert formula_group.get_top()[1] < card.get_top()[1] - .19
        assert f.get_top()[1] < title_row.get_bottom()[1] - .04
        return VGroup(card,title_row,f,formula_group,sym)

    def formula_atlas(self):
        data=[
            ("01","SQUARE",r"A=s^2","s = side"),
            ("02","RECTANGLE",r"A=b\,h","b = base · h = perpendicular height"),
            ("03","TRIANGLE",r"A=\frac{b\,h}{2}","h is perpendicular to b"),
            ("04","PARALLELOGRAM",r"A=b\,h","use perpendicular h, not slanted side"),
            ("05","TRAPEZOID",r"A=\frac{(B+b)h}{2}","B,b = parallel bases · h = height"),
            ("06","RHOMBUS",r"A=\frac{D\,d}{2}","D,d = diagonals"),
            ("07","CIRCLE",r"A=\pi r^2","r = radius · d = 2r"),
            ("08","REGULAR POLYGON",r"A=\frac{P\,a}{2}","P = perimeter · a = apothem"),
            ("09","SEMICIRCLE",r"A=\frac{\pi r^2}{2}","half of a full circle"),
            ("10","QUARTER CIRCLE",r"A=\frac{\pi r^2}{4}","one of four equal quarters"),
        ]
        for page in range(2):
            h=self.header(14,f"COMPLETE 2D AREA FORMULA GUIDE · {page+1}/2","Read the figure first: identify the marked dimensions, then select the matching area formula.")
            self.add(h)
            subset=data[page*5:(page+1)*5]
            cards=VGroup(*[self._formula_card_v8(*row) for row in subset])
            cards.arrange(DOWN,buff=.11).move_to(DOWN*.40)
            self.fit(cards,7.35,5.72)
            for i,card in enumerate(cards):
                self.play(FadeIn(card,shift=RIGHT*.08),run_time=.36)
                if i in (0,2,4): self.wait(.38)
            self.wait(4.20); self.wipe()
