#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — 2D Areas — V8 Senior Layout QA.

V8 preserves the accepted V7 worked-example grid and all validated geometry/math,
while correcting the remaining text/figure collisions found by frame-by-frame QA.

Senior layout principles:
- geometry and explanatory text live in disjoint safe zones;
- long derivations are contained in opaque fitted panels;
- external dimension labels use explicit gutters;
- the circle-sector proof has separate note, strip, dimension and formula bands;
- formula-guide cards use fixed internal title / figure / formula / note zones;
- the atlas uses a 2-column x 3-row projector grid instead of a compressed stack.

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *
from Geometry8_2D_Areas_Masterclass_FINAL_QA import *


class Geometry8AreaSeniorLayoutV8Mixin:
    """Frame-safe senior layout overrides on top of V7."""

    def _safe_panel(self, width, height, center, stroke=LIGHT, fill=WHITE, opacity=.985):
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=.13,
            stroke_color=stroke,
            stroke_width=1.45,
            fill_color=fill,
            fill_opacity=opacity,
        )
        panel.move_to(center)
        return panel

    def _place_in_zone(self, mob, center, max_width, max_height):
        """Fit then center an object inside a hard rectangular safe zone."""
        self.fit(mob, max_width, max_height)
        mob.move_to(center)
        return mob

    def _derivation_panel(self, items, center=RIGHT*3.55+DOWN*.10, width=5.90, height=3.05):
        """Opaque derivation zone with guaranteed separation from the left figure."""
        panel = self._safe_panel(width, height, center, stroke=LIGHT, fill=WHITE, opacity=.992)
        body = VGroup(*items).arrange(DOWN, buff=.25)
        self.fit(body, width-.58, height-.48)
        body.move_to(panel)
        return VGroup(panel, body)

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
        deriv=self._derivation_panel([
            self.txt("b unit columns repeated through h unit rows",27,True),
            self.eq(r"A=\underbrace{b+b+\cdots+b}_{h\ \text{rows}}",40),
            self.box(r"A=b\,h",4.80,60),
        ], center=RIGHT*3.70+DOWN*.18, width=5.95, height=3.08)
        self.play(FadeIn(deriv[0]),run_time=.28)
        for item in deriv[1]:
            self.play(FadeIn(item,shift=UP*.03),run_time=.40); self.wait(.30)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),run_time=.35)
        ex=self.example_stack("Given: b = 8 cm, h = 3 cm",r"A=b\,h",r"A=(8)(3)",r"A=24\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def trapezoid_explicit(self):
        h=self.header(8,"5 · TRAPEZOID","Two parallel bases, B and b, share one perpendicular height h.")
        strip=self.stage_strip(); self.add(h,strip)

        A=np.array([-6.35,-1.30,0]); Bp=np.array([-3.25,-1.30,0]); C=np.array([-3.85,1.25,0]); D=np.array([-5.55,1.25,0]); foot=np.array([D[0],A[1],0])
        trap=Polygon(A,Bp,C,D,stroke_color=INK,stroke_width=5,fill_color=FILL,fill_opacity=.66)

        self.mark_stage(strip,0)
        self.play(Create(Line(A,Bp,color=INK,stroke_width=5)),run_time=.45)
        self.play(Create(Line(Bp,C,color=INK,stroke_width=5)),Create(Line(C,D,color=INK,stroke_width=5)),Create(Line(D,A,color=INK,stroke_width=5)),FadeIn(trap.copy().set_stroke(opacity=0)),run_time=.82)

        self.mark_stage(strip,1)
        dB=self.dimension(A+DOWN*.34,Bp+DOWN*.34,"B",DOWN)
        db=self.dimension(D+UP*.34,C+UP*.34,"b",UP)
        alt=DashedLine(D,foot,color=MID,stroke_width=3)
        dh=self.dimension(foot+LEFT*.78,D+LEFT*.78,"h",LEFT,32)
        self.play(GrowFromCenter(dB[0]),GrowFromCenter(db[0]),FadeIn(dB[1]),FadeIn(db[1]),Create(alt),GrowFromCenter(dh[0]),FadeIn(dh[1]),FadeIn(self.right_mark(foot)),run_time=.82)

        self.mark_stage(strip,2)
        copy=trap.copy().set_fill(PAPER,opacity=.90).set_stroke(MID,width=4)
        pivot=(Bp+C)/2
        self.add(copy)
        self.play(Rotate(copy,angle=PI,about_point=pivot),run_time=1.05,rate_func=smooth)
        copy_A=Bp+C-A
        copy_D=Bp+C-D
        para=Polygon(A,copy_D,copy_A,D,stroke_color=INK,stroke_width=4,fill_opacity=0)
        sum_base=self.dimension(A+DOWN*.37,copy_D+DOWN*.37,"B+b",DOWN,34)
        self.play(FadeOut(dB),FadeOut(db),Create(para),GrowFromCenter(sum_base[0]),FadeIn(sum_base[1]),run_time=.58)
        deriv=VGroup(
            self.txt("2 congruent trapezoids → one parallelogram",26,True),
            self.eq(r"2A=(B+b)h",43),
            self.box(r"A=\frac{(B+b)h}{2}",6.1,55),
        ).arrange(DOWN,buff=.22).move_to(RIGHT*3.55)
        for item in deriv:
            self.play(FadeIn(item,shift=UP*.03),run_time=.38); self.wait(.24)

        self.mark_stage(strip,3)
        self.play(FadeOut(deriv),FadeOut(copy),FadeOut(para),FadeOut(sum_base),run_time=.32)
        ex=self.example_stack("Given: B = 10 cm, b = 6 cm, h = 4 cm",r"A=\frac{(B+b)h}{2}",r"A=\frac{(10+6)(4)}{2}",r"A=32\ \mathrm{cm}^2")
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def circle_explicit(self):
        h = self.header(
            10,
            "7 · CIRCLE",
            "The radius generates the circle; sector rearrangement connects circumference to area.",
        )
        strip = self.stage_strip(); self.add(h, strip)

        center = np.array([-4.05, -.25, 0])
        radius = 1.62
        circle = Circle(radius, color=INK, stroke_width=5, fill_color=FILL, fill_opacity=.18).move_to(center)
        sweep = Line(center, center + RIGHT*radius, color=INK, stroke_width=4)
        dot = Dot(center, radius=.07, color=INK)

        self.mark_stage(strip, 0)
        self.play(FadeIn(dot), Create(sweep), run_time=.42)
        self.play(Create(circle), Rotate(sweep, angle=TAU, about_point=center), run_time=1.15, rate_func=linear)

        self.mark_stage(strip, 1)
        diameter = DashedLine(center + LEFT*radius, center + RIGHT*radius, color=MID, stroke_width=2.8)
        rlab = self.eq("r", 38).next_to(Line(center, center + RIGHT*radius), UP, buff=.06)
        dlab = self.eq("d=2r", 35).next_to(diameter, DOWN, buff=.10)
        self.play(Create(diameter), FadeIn(rlab), FadeIn(dlab), run_time=.60)

        self.mark_stage(strip, 2)
        n = 16
        theta = TAU / n
        sectors = VGroup()
        for k in range(n):
            sectors.add(Sector(
                arc_center=center,
                radius=radius,
                start_angle=k*theta,
                angle=theta,
                stroke_color=INK,
                stroke_width=1.4,
                fill_color=FILL if k % 2 == 0 else PAPER,
                fill_opacity=.72 if k % 2 == 0 else .92,
            ))

        source_outline = Circle(radius, color=LIGHT, stroke_width=2.0, fill_opacity=0).move_to(center)
        self.play(FadeOut(circle), FadeIn(source_outline), FadeIn(sectors), run_time=.55)
        divide_note = self.txt("Divide the circle into equal sectors.", 27, True).move_to(RIGHT*3.50 + UP*1.70)
        self.play(FadeIn(divide_note), run_time=.35)
        self.wait(.35)

        step = (math.pi * radius) / n
        x0 = .72
        sector_y = -.42
        targets = VGroup()
        for i in range(n):
            x = x0 + i*step
            if i % 2 == 0:
                apex = np.array([x, -radius/2 + sector_y, 0])
                start = PI/2 - theta/2
            else:
                apex = np.array([x, radius/2 + sector_y, 0])
                start = 3*PI/2 - theta/2
            targets.add(Sector(
                arc_center=apex,
                radius=radius,
                start_angle=start,
                angle=theta,
                stroke_color=INK,
                stroke_width=1.25,
                fill_color=FILL if i % 2 == 0 else PAPER,
                fill_opacity=.72 if i % 2 == 0 else .92,
            ))

        self.play(
            LaggedStart(*[Transform(sectors[i], targets[i]) for i in range(n)], lag_ratio=.025),
            FadeOut(divide_note),
            run_time=1.65,
            rate_func=smooth,
        )

        proof_panel = self._safe_panel(6.05, 1.18, RIGHT*3.55 + UP*1.48, stroke=LIGHT, fill=WHITE, opacity=.995)
        limit_note = self.txt("More sectors → straighter top and bottom edges", 24, True)
        base_note = self.eq(r"\frac{C}{2}=\frac{2\pi r}{2}=\pi r", 36)
        proof_text = VGroup(limit_note, base_note).arrange(DOWN, buff=.10)
        self.fit(proof_text, 5.55, .88); proof_text.move_to(proof_panel)
        proof = VGroup(proof_panel, proof_text)
        self.play(FadeIn(proof_panel), FadeIn(proof_text), run_time=.52)

        left_x = x0 - .10
        right_x = x0 + (n-1)*step + .16
        base_y = -1.58
        base = self.dimension([left_x, base_y, 0], [right_x, base_y, 0], r"\pi r", DOWN, 31)
        height = self.dimension(
            [right_x+.35, -radius/2 + sector_y, 0],
            [right_x+.35, radius/2 + sector_y, 0],
            "r", RIGHT, 32,
        )
        self.play(GrowFromCenter(base[0]), FadeIn(base[1]), GrowFromCenter(height[0]), FadeIn(height[1]), run_time=.60)

        formula = self.box(r"A=(\pi r)(r)=\pi r^2", 5.60, 52).move_to(RIGHT*3.50 + DOWN*2.50)
        self.play(FadeIn(formula), run_time=.45)
        self.wait(.95)

        self.mark_stage(strip, 3)
        self.play(
            FadeOut(sectors), FadeOut(base), FadeOut(height), FadeOut(proof), FadeOut(formula),
            run_time=.36,
        )
        self.play(source_outline.animate.set_stroke(INK, width=4), run_time=.25)
        ex = self.example_stack(
            "Given: r = 4 cm",
            r"A=\pi r^2",
            r"A=\pi(4)^2=16\pi",
            r"A\approx50.27\ \mathrm{cm}^2",
        )
        self.show_example(ex)
        self.wait(.80); self.wipe()

    def _formula_card_v6(self, kind, name, formula, symbols):
        inherited = super()._formula_card_v6(kind, name, formula, symbols)
        _, title_row, figure, formula_group, sym = inherited

        card = RoundedRectangle(
            width=6.28,
            height=1.62,
            corner_radius=.12,
            stroke_color=INK,
            stroke_width=1.55,
            fill_color=WHITE,
            fill_opacity=1,
        )
        c = card.get_center()

        self._place_in_zone(title_row, c + LEFT*1.78 + UP*.50, 2.78, .31)
        self._place_in_zone(figure, c + LEFT*1.84 + DOWN*.19, 2.20, .72)
        self._place_in_zone(formula_group, c + RIGHT*1.63 + UP*.12, 2.70, .64)
        self._place_in_zone(sym, c + RIGHT*1.63 + DOWN*.49, 2.72, .23)

        return VGroup(card, title_row, figure, formula_group, sym)

    def formula_atlas(self):
        """Two 2-column projector pages; no global scaling and no title/figure collisions."""
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

        positions = [
            LEFT*3.30 + UP*1.38,
            RIGHT*3.30 + UP*1.38,
            LEFT*3.30 + DOWN*.49,
            RIGHT*3.30 + DOWN*.49,
            LEFT*3.30 + DOWN*2.36,
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
            for card, pos in zip(cards, positions):
                card.move_to(pos)

            for i, card in enumerate(cards):
                self.play(FadeIn(card, shift=UP*.04), run_time=.34)
                if i in (1,3,4): self.wait(.42)
            self.wait(4.20)
            self.wipe()
