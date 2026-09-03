#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Area of 2D Figures — V6 explicit classroom guidance.

V6 preserves the accepted V5 mathematics and geometry, but makes the lesson
more explicit for Grade 8 students:
- numbered stage strip;
- slower worked-example reveals;
- visible step logic and reading pauses;
- final formula guide rebuilt as large visual cards containing figure,
  defining dimensions and formula.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaExplicitGuideV6Mixin:
    """Readability / explicit-step overrides on top of the accepted V5 lesson."""

    def stage_strip(self):
        labels = [
            ("01", "CONSTRUCT"),
            ("02", "PARTS"),
            ("03", "DERIVE"),
            ("04", "EXAMPLE"),
        ]
        items = VGroup()
        for number, label in labels:
            box = RoundedRectangle(
                width=2.12,
                height=.58,
                corner_radius=.08,
                stroke_color=LIGHT,
                stroke_width=1.35,
                fill_color=WHITE,
                fill_opacity=1,
            )
            num = self.txt(number, 18, True).set_opacity(.55)
            txt = self.txt(label, 20, True).set_opacity(.46)
            content = VGroup(num, txt).arrange(RIGHT, buff=.12).move_to(box)
            items.add(VGroup(box, content))
        items.arrange(RIGHT, buff=.08)
        items.to_edge(RIGHT, buff=.38).shift(UP * 2.54)
        return items

    def mark_stage(self, strip, index):
        animations = []
        for i, item in enumerate(strip):
            active = i == index
            animations.extend([
                item[0].animate.set_stroke(
                    INK if active else LIGHT,
                    width=3.1 if active else 1.25,
                ).set_fill(PAPER if active else WHITE, opacity=1),
                item[1].animate.set_opacity(1.0 if active else .43),
            ])
        self.play(*animations, run_time=.40)
        self.wait(.35)

    def show_example(self, stack, right_x=3.55):
        """Reveal a worked example as explicit student notebook steps."""
        stack.move_to(RIGHT * right_x + DOWN * .15)
        panel, content = stack
        self.play(FadeIn(panel, shift=UP*.03), run_time=.40)

        # title + guide
        self.play(FadeIn(content[0], shift=UP*.025), run_time=.38)
        self.play(FadeIn(content[1], shift=UP*.025), run_time=.38)
        self.wait(.55)

        step_labels = [
            self.txt("STEP 1 · READ THE GIVEN VALUES", 20, True),
            self.txt("STEP 2 · CHOOSE THE FORMULA", 20, True),
            self.txt("STEP 3 · SUBSTITUTE", 20, True),
            self.txt("STEP 4 · CALCULATE + USE SQUARE UNITS", 20, True),
        ]
        for label in step_labels:
            self.fit(label, stack.width - .60, .36)
            label.set_opacity(.62)

        # given
        step_labels[0].next_to(content[2], UP, buff=.08).align_to(content[2], LEFT)
        self.play(FadeIn(step_labels[0]), FadeIn(content[2], shift=UP*.02), run_time=.42)
        self.wait(.80)

        # formula
        step_labels[1].next_to(content[3], UP, buff=.08).align_to(content[3], LEFT)
        self.play(FadeIn(step_labels[1]), FadeIn(content[3], shift=UP*.02), run_time=.42)
        self.wait(.90)

        # substitution
        step_labels[2].next_to(content[4], UP, buff=.08).align_to(content[4], LEFT)
        self.play(FadeIn(step_labels[2]), FadeIn(content[4], shift=UP*.02), run_time=.42)
        self.wait(1.00)

        # result and check
        step_labels[3].next_to(content[5], UP, buff=.08).align_to(content[5], LEFT)
        self.play(FadeIn(step_labels[3]), FadeIn(content[5], shift=UP*.02), run_time=.48)
        self.wait(1.20)
        self.play(FadeIn(content[6], shift=UP*.02), run_time=.36)
        self.wait(2.20)

    # ------------------------------------------------------------------
    # Final visual formula guide
    # ------------------------------------------------------------------
    def _mini_dimension(self, p1, p2, label, direction=DOWN, size=25):
        line = DoubleArrow(
            p1, p2,
            buff=0,
            tip_length=.10,
            stroke_width=1.7,
            color=INK,
        )
        lab = self.eq(label, size).next_to(line, direction, buff=.05)
        return VGroup(line, lab)

    def _formula_card_v6(self, kind, name, formula, symbols):
        card = RoundedRectangle(
            width=6.75,
            height=1.55,
            corner_radius=.12,
            stroke_color=INK,
            stroke_width=1.7,
            fill_color=WHITE,
            fill_opacity=1,
        )
        number = self.txt(kind, 22, True)
        title = self.txt(name, 24, True)
        title_row = VGroup(number, title).arrange(RIGHT, buff=.16)
        title_row.move_to(card.get_center() + LEFT*1.95 + UP*.50)
        self.fit(title_row, 2.80, .38)

        figure_center = card.get_center() + LEFT*2.05 + DOWN*.18
        f = VGroup()

        if name == "SQUARE":
            shape = Square(0.78, color=INK, stroke_width=2.6).move_to(figure_center)
            dim = self._mini_dimension(shape.get_corner(DL)+DOWN*.12, shape.get_corner(DR)+DOWN*.12, "s", DOWN, 22)
            side = self.eq("s", 22).next_to(shape, RIGHT, buff=.06)
            f = VGroup(shape, dim, side)
        elif name == "RECTANGLE":
            shape = Rectangle(width=1.18, height=.72, color=INK, stroke_width=2.6).move_to(figure_center)
            db = self._mini_dimension(shape.get_corner(DL)+DOWN*.12, shape.get_corner(DR)+DOWN*.12, "b", DOWN, 22)
            dh = self._mini_dimension(shape.get_corner(DR)+RIGHT*.12, shape.get_corner(UR)+RIGHT*.12, "h", RIGHT, 22)
            f = VGroup(shape, db, dh)
        elif name == "TRIANGLE":
            a=figure_center+LEFT*.62+DOWN*.35; b=figure_center+RIGHT*.62+DOWN*.35; c=figure_center+UP*.48
            shape=Polygon(a,b,c,color=INK,stroke_width=2.6)
            foot=np.array([c[0],a[1],0])
            alt=DashedLine(c,foot,color=MID,stroke_width=1.7)
            right=Square(.13,color=INK,stroke_width=1.3).move_to(foot+UR*.065)
            db=self._mini_dimension(a+DOWN*.12,b+DOWN*.12,"b",DOWN,22)
            hlab=self.eq("h",22).next_to(alt,RIGHT,buff=.04)
            f=VGroup(shape,alt,right,db,hlab)
        elif name == "PARALLELOGRAM":
            a=figure_center+LEFT*.68+DOWN*.34; b=figure_center+RIGHT*.50+DOWN*.34; c=b+RIGHT*.22+UP*.72; d=a+RIGHT*.22+UP*.72
            shape=Polygon(a,b,c,d,color=INK,stroke_width=2.6)
            foot=np.array([d[0],a[1],0]); alt=DashedLine(d,foot,color=MID,stroke_width=1.7)
            db=self._mini_dimension(a+DOWN*.12,b+DOWN*.12,"b",DOWN,22); hlab=self.eq("h",22).next_to(alt,RIGHT,buff=.04)
            f=VGroup(shape,alt,db,hlab)
        elif name == "TRAPEZOID":
            a=figure_center+LEFT*.70+DOWN*.34; b=figure_center+RIGHT*.70+DOWN*.34; c=figure_center+RIGHT*.43+UP*.38; d=figure_center+LEFT*.43+UP*.38
            shape=Polygon(a,b,c,d,color=INK,stroke_width=2.6)
            top=self._mini_dimension(d+UP*.12,c+UP*.12,"b",UP,21)
            bot=self._mini_dimension(a+DOWN*.12,b+DOWN*.12,"B",DOWN,21)
            foot=np.array([d[0],a[1],0]); alt=DashedLine(d,foot,color=MID,stroke_width=1.6); hlab=self.eq("h",21).next_to(alt,RIGHT,buff=.03)
            f=VGroup(shape,top,bot,alt,hlab)
        elif name == "RHOMBUS":
            l=figure_center+LEFT*.70; r=figure_center+RIGHT*.70; u=figure_center+UP*.48; d=figure_center+DOWN*.48
            shape=Polygon(l,u,r,d,color=INK,stroke_width=2.6)
            hd=DashedLine(l,r,color=MID,stroke_width=1.5); vd=DashedLine(d,u,color=MID,stroke_width=1.5)
            D=self.eq("D",21).next_to(vd,RIGHT,buff=.04); dd=self.eq("d",21).next_to(hd,DOWN,buff=.03)
            f=VGroup(shape,hd,vd,D,dd)
        elif name == "CIRCLE":
            shape=Circle(.53,color=INK,stroke_width=2.6).move_to(figure_center)
            c=Dot(figure_center,radius=.035,color=INK); rline=Line(figure_center,figure_center+UR*.40,color=INK,stroke_width=2)
            rlab=self.eq("r",22).next_to(rline,UP,buff=.02)
            diam=DashedLine(figure_center+LEFT*.53,figure_center+RIGHT*.53,color=MID,stroke_width=1.5); dlab=self.eq("d",20).next_to(diam,DOWN,buff=.03)
            f=VGroup(shape,c,rline,rlab,diam,dlab)
        elif name == "REGULAR POLYGON":
            shape=RegularPolygon(6,radius=.58,color=INK,stroke_width=2.6).move_to(figure_center)
            c=Dot(figure_center,radius=.035,color=INK)
            bottom=shape.get_vertices()[4] if len(shape.get_vertices())>4 else figure_center+DOWN*.5
            ap=Line(figure_center,figure_center+DOWN*.50,color=INK,stroke_width=1.8)
            alab=self.eq("a",21).next_to(ap,RIGHT,buff=.03)
            plab=self.eq("P",21).next_to(shape,DOWN,buff=.03)
            f=VGroup(shape,c,ap,alab,plab)
        elif name == "SEMICIRCLE":
            arc=Arc(radius=.60,start_angle=0,angle=PI,color=INK,stroke_width=2.6,arc_center=figure_center+DOWN*.15)
            base=Line(figure_center+LEFT*.60+DOWN*.15,figure_center+RIGHT*.60+DOWN*.15,color=INK,stroke_width=2.6)
            c=Dot(figure_center+DOWN*.15,radius=.032,color=INK)
            rline=Line(figure_center+DOWN*.15,figure_center+UR*.40,color=INK,stroke_width=1.8)
            rlab=self.eq("r",21).next_to(rline,UP,buff=.02)
            f=VGroup(arc,base,c,rline,rlab)
        elif name == "QUARTER CIRCLE":
            center=figure_center+LEFT*.22+DOWN*.24
            arc=Arc(radius=.66,start_angle=0,angle=PI/2,color=INK,stroke_width=2.6,arc_center=center)
            h=Line(center,center+RIGHT*.66,color=INK,stroke_width=2.6); v=Line(center,center+UP*.66,color=INK,stroke_width=2.6)
            rlab=self.eq("r",21).next_to(Line(center,center+UR*.47),UP,buff=.01)
            f=VGroup(arc,h,v,rlab)

        formula_box = RoundedRectangle(
            width=2.85, height=.76, corner_radius=.08,
            stroke_color=LIGHT, stroke_width=1.4,
            fill_color=PAPER, fill_opacity=1,
        )
        fm = self.eq(formula, 34)
        self.fit(fm, 2.55, .55); fm.move_to(formula_box)
        formula_group=VGroup(formula_box,fm).move_to(card.get_center()+RIGHT*1.82+DOWN*.02)

        sym=self.txt(symbols,18)
        self.fit(sym,2.72,.32)
        sym.next_to(formula_group,DOWN,buff=.08)

        return VGroup(card,title_row,f,formula_group,sym)

    def formula_atlas(self):
        """Two readable visual formula-guide screens matching the student handout logic."""
        data = [
            ("01", "SQUARE", r"A=s^2", "s = side"),
            ("02", "RECTANGLE", r"A=b\,h", "b = base · h = perpendicular height"),
            ("03", "TRIANGLE", r"A=\frac{b\,h}{2}", "h is perpendicular to b"),
            ("04", "PARALLELOGRAM", r"A=b\,h", "use perpendicular h, not slanted side"),
            ("05", "TRAPEZOID", r"A=\frac{(B+b)h}{2}", "B,b = parallel bases · h = height"),
            ("06", "RHOMBUS", r"A=\frac{D\,d}{2}", "D,d = diagonals"),
            ("07", "CIRCLE", r"A=\pi r^2", "r = radius · d = 2r"),
            ("08", "REGULAR POLYGON", r"A=\frac{P\,a}{2}", "P = perimeter · a = apothem"),
            ("09", "SEMICIRCLE", r"A=\frac{\pi r^2}{2}", "half of a full circle"),
            ("10", "QUARTER CIRCLE", r"A=\frac{\pi r^2}{4}", "one of four equal quarters"),
        ]

        for page in range(2):
            h = self.header(
                14,
                f"COMPLETE 2D AREA FORMULA GUIDE · {page+1}/2",
                "Read the figure first: identify the marked dimensions, then select the matching area formula.",
            )
            self.add(h)
            subset=data[page*5:(page+1)*5]
            cards=VGroup(*[self._formula_card_v6(*row) for row in subset])
            cards.arrange(DOWN,buff=.10).scale(.86).move_to(DOWN*.38)
            self.fit(cards,14.55,5.86)

            for i,card in enumerate(cards):
                self.play(FadeIn(card,shift=RIGHT*.08),run_time=.36)
                if i in (0,2,4): self.wait(.38)
            self.wait(4.20)
            self.wipe()

    def final_method(self):
        h = self.header(
            15,
            "AREA PROBLEM METHOD · USE THIS EVERY TIME",
            "A repeatable five-step routine prevents most formula and unit errors.",
        )
        self.add(h)
        steps=[
            ("01","DRAW / IDENTIFY THE FIGURE"),
            ("02","MARK THE REQUIRED DIMENSIONS"),
            ("03","CHOOSE THE MATCHING AREA FORMULA"),
            ("04","SUBSTITUTE AND CALCULATE"),
            ("05","WRITE THE ANSWER IN SQUARE UNITS"),
        ]
        cards=VGroup()
        for n,text in steps:
            box=RoundedRectangle(width=11.6,height=.82,corner_radius=.10,stroke_color=INK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
            badge=RoundedRectangle(width=.82,height=.50,corner_radius=.08,stroke_color=INK,stroke_width=1.5,fill_color=PAPER,fill_opacity=1)
            nm=self.txt(n,22,True).move_to(badge)
            tx=self.txt(text,29,True)
            row=VGroup(VGroup(badge,nm),tx).arrange(RIGHT,buff=.28).move_to(box).align_to(box,LEFT).shift(RIGHT*.28)
            cards.add(VGroup(box,row))
        cards.arrange(DOWN,buff=.16).move_to(DOWN*.35)
        for card in cards:
            self.play(FadeIn(card,shift=UP*.06),run_time=.42)
            self.wait(.52)
        self.wait(3.2)
        self.wipe()
