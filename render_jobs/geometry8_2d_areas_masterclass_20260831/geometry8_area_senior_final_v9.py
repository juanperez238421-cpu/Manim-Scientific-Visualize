#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V9 final rendered-frame QA layer.

V9 is the final precision pass after inspecting the V8 PQH artifact at full
1920x1080 resolution.  V8 fixed the systemic worked-example collisions and the
rectangle/parallelogram/rhombus defects.  Two presentation issues remained:

1. In the circle derivation, the C/2 = pi r equation still occupied the same
   vertical band as the rearranged-sector top edge.
2. The formula-guide cards were safe but globally scaled too small because five
   cards were stacked in one narrow central column.

V9 gives the circle text, geometry and dimensions independent bands and lays the
five formula cards out as a 3+2 two-column grid so no down-scaling is required.
All formulas, dimensions and numerical results are unchanged.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaSeniorFinalV9Mixin:
    """Final high-resolution spatial corrections on top of V8."""

    def circle_explicit(self):
        h=self.header(10,"7 · CIRCLE","The radius generates the circle; sector rearrangement connects circumference to area.")
        strip=self.stage_strip(); self.add(h,strip)

        center=np.array([-4.05,-.25,0]); radius=1.62
        circle=Circle(radius,color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.18).move_to(center)
        sweep=Line(center,center+RIGHT*radius,color=INK,stroke_width=4)
        dot=Dot(center,radius=.07,color=INK)
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
            sectors.add(Sector(
                arc_center=center,radius=radius,start_angle=k*theta,angle=theta,
                stroke_color=INK,stroke_width=1.4,
                fill_color=FILL if k%2==0 else PAPER,
                fill_opacity=.72 if k%2==0 else .92,
            ))
        source_outline=Circle(radius,color=LIGHT,stroke_width=2.0,fill_opacity=0).move_to(center)
        self.play(FadeOut(circle),FadeIn(source_outline),FadeIn(sectors),run_time=.55)

        divide_note=self.txt("Divide the circle into equal sectors.",26,True)
        self.fit(divide_note,5.35,.43)
        divide_note.move_to(RIGHT*3.75+UP*1.74)
        self.play(FadeIn(divide_note),run_time=.35); self.wait(.35)

        # The rearranged sectors are moved slightly DOWN compared with V8.  This
        # opens a dedicated equation band between the stage strip and geometry.
        step=(math.pi*radius)/n; x0=.72; vertical_shift=-.16; targets=VGroup()
        for i in range(n):
            x=x0+i*step
            if i%2==0:
                apex=np.array([x,-radius/2+vertical_shift,0]); start=PI/2-theta/2
            else:
                apex=np.array([x,radius/2+vertical_shift,0]); start=3*PI/2-theta/2
            targets.add(Sector(
                arc_center=apex,radius=radius,start_angle=start,angle=theta,
                stroke_color=INK,stroke_width=1.25,
                fill_color=FILL if i%2==0 else PAPER,
                fill_opacity=.72 if i%2==0 else .92,
            ))
        self.play(
            LaggedStart(*[Transform(sectors[i],targets[i]) for i in range(n)],lag_ratio=.025),
            FadeOut(divide_note),run_time=1.65,rate_func=smooth,
        )

        # TEXT BAND 1: conceptual sentence.
        limit_note=self.txt("More sectors → straighter top and bottom edges",23,True)
        self.fit(limit_note,5.35,.40)
        limit_note.move_to(RIGHT*3.75+UP*1.78)

        # TEXT BAND 2: circumference-half equation.  For a Sector, Manim's
        # object bounding box includes radial construction geometry and therefore
        # overestimates the visible top envelope after rearrangement.  The true
        # visual top band of the alternating sector strip is known analytically:
        # radius/2 + vertical_shift.  Gate against that rendered envelope.
        base_note=self.eq(r"\frac{C}{2}=\frac{2\pi r}{2}=\pi r",34)
        base_note.move_to(RIGHT*3.75+UP*1.29)
        sector_top=radius/2 + vertical_shift + .03
        assert base_note.get_bottom()[1] > sector_top + .13
        assert limit_note.get_bottom()[1] > base_note.get_top()[1] + .06
        self.play(FadeIn(limit_note),FadeIn(base_note),run_time=.55)

        # GEOMETRY/DIMENSION BAND.
        left_x=x0-.10; right_x=x0+(n-1)*step+.16
        base_dim=self.dimension(
            [left_x,-1.34+vertical_shift,0],
            [right_x,-1.34+vertical_shift,0],
            r"\pi r",DOWN,32,
        )
        height_dim=self.dimension(
            [right_x+.35,-radius/2+vertical_shift,0],
            [right_x+.35,radius/2+vertical_shift,0],
            "r",RIGHT,33,
        )
        self.play(
            GrowFromCenter(base_dim[0]),FadeIn(base_dim[1]),
            GrowFromCenter(height_dim[0]),FadeIn(height_dim[1]),run_time=.60,
        )

        # FORMULA BAND: deliberately below the base-dimension label.
        formula=self.box(r"A=(\pi r)(r)=\pi r^2",5.45,51).move_to(RIGHT*3.55+DOWN*2.73)
        assert formula.get_top()[1] < base_dim[1].get_bottom()[1] - .16
        self.play(FadeIn(formula),run_time=.45); self.wait(.95)

        self.mark_stage(strip,3)
        self.play(
            FadeOut(sectors),FadeOut(base_dim),FadeOut(height_dim),
            FadeOut(limit_note),FadeOut(base_note),FadeOut(formula),run_time=.36,
        )
        self.play(source_outline.animate.set_stroke(INK,width=4),run_time=.25)
        ex=self.example_stack(
            "Given: r = 4 cm",r"A=\pi r^2",r"A=\pi(4)^2=16\pi",
            r"A\approx50.27\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def formula_atlas(self):
        """Two large 3+2 two-column grid pages; no five-card vertical compression."""
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
            h=self.header(
                14,f"COMPLETE 2D AREA FORMULA GUIDE · {page+1}/2",
                "Read the figure first: identify the marked dimensions, then select the matching area formula.",
            )
            self.add(h)
            subset=data[page*5:(page+1)*5]
            card_objs=[self._formula_card_v8(*row) for row in subset]

            left_col=VGroup(*card_objs[:3]).arrange(DOWN,buff=.15)
            right_col=VGroup(*card_objs[3:]).arrange(DOWN,buff=.15)
            columns=VGroup(left_col,right_col).arrange(RIGHT,buff=.22,aligned_edge=UP)
            self.fit(columns,13.55,5.54)
            columns.move_to(DOWN*.38)

            # Frame and inter-card separation gates.  These assertions execute
            # during PQL/PQH construction and prevent accidental regression.
            assert columns.get_left()[0] > -config.frame_x_radius + .20
            assert columns.get_right()[0] < config.frame_x_radius - .20
            assert left_col.get_right()[0] < right_col.get_left()[0] - .12
            for col in (left_col,right_col):
                for a,b in zip(col[:-1],col[1:]):
                    assert a.get_bottom()[1] > b.get_top()[1] + .07

            for i,card in enumerate(card_objs):
                self.play(FadeIn(card,shift=RIGHT*.06),run_time=.36)
                if i in (0,2,4): self.wait(.38)
            self.wait(4.20); self.wipe()
