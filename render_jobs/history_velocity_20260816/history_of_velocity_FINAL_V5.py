#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""History of Velocity — Senior V5 audited reconstruction.

V5 is based on the fully rendered V4 diagnostic. It fixes the layout defects
found in the 4-second full-timeline visual audit and introduces a restrained
animated reflection beat between sections so students get real reading time
without long frozen frames.

ManimCE target: 0.20.1
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *
from history_of_velocity_FINAL_V4 import HistoryOfVelocityV4, SOFT, LINE


class HistoryOfVelocityV5(HistoryOfVelocityV4):
    """Frame-audited senior version."""

    def clear_stage(self, keep_header: bool = True) -> None:
        """Add a quiet visual reading beat before clearing a section."""
        if keep_header and self.mobjects:
            y = 2.12
            track = Line(LEFT * 5.35 + UP * y, RIGHT * 5.35 + UP * y,
                         color=LIGHT_GRAY, stroke_width=1.5)
            pulse = Dot(track.get_start(), radius=0.055, color=BLACK)
            label = self.text("REFLECT • CONNECT THE IDEA", 14, BOLD).next_to(
                track, UP, buff=0.06, aligned_edge=LEFT
            )
            self.play(FadeIn(label), Create(track), FadeIn(pulse), run_time=0.30)
            self.play(pulse.animate.move_to(track.get_end()), run_time=2.05, rate_func=linear)
            self.play(FadeOut(VGroup(label, track, pulse)), run_time=0.25)
        super().clear_stage(keep_header=keep_header)

    def zeno(self) -> None:
        self.set_header(
            1,
            "ZENO OF ELEA — THE PROBLEM OF MOTION",
            "~450 BC · Achilles and the tortoise expose a deep question about infinity, continuity and an exact instant.",
        )
        track = Line(LEFT * 5.9, RIGHT * 5.9, color=BLACK_LINE, stroke_width=3.0).move_to(DOWN * 0.65)
        ach = Dot(track.get_left() + RIGHT * 0.45, radius=0.16, color=BLACK)
        tor = RegularPolygon(n=6, radius=0.19, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1.0)
        tor.move_to(track.get_left() + RIGHT * 3.05)
        ach_lab = self.text("ACHILLES", 22, BOLD).next_to(ach, UP, buff=0.18)
        tor_lab = self.text("TORTOISE", 22, BOLD).next_to(tor, UP, buff=0.18)
        head = self.question_card("Achilles is faster — so why does the argument seem to require infinitely many catches?", 12.7, 28).move_to(UP * 1.52)
        self.play(FadeIn(head), Create(track), FadeIn(ach), FadeIn(tor), FadeIn(ach_lab), FadeIn(tor_lab), run_time=1.0)
        positions = [
            track.get_left() + RIGHT * 3.05,
            track.get_left() + RIGHT * 5.75,
            track.get_left() + RIGHT * 7.55,
            track.get_left() + RIGHT * 8.75,
        ]
        ghosts = VGroup()
        for i in range(3):
            ghost = Dot(positions[i], radius=0.075, color=MID_GRAY)
            mark = self.text(f"P{i}", 18, BOLD).next_to(ghost, DOWN, buff=0.10)
            ghosts.add(VGroup(ghost, mark))
            step = self.mini_tag(f"STEP {i+1}: reach where the tortoise WAS", 22).move_to(DOWN * 2.00)
            self.play(FadeIn(ghosts[-1]), FadeIn(step), run_time=0.45)
            self.play(
                ach.animate.move_to(positions[i]),
                tor.animate.move_to(positions[i+1]),
                ach_lab.animate.next_to(positions[i], UP, buff=0.18),
                tor_lab.animate.next_to(positions[i+1], UP, buff=0.18),
                run_time=1.55,
                rate_func=smooth,
            )
            self.play(FadeOut(step), run_time=0.25)
        series = MathTex(r"d_1+d_2+d_3+\cdots", color=BLACK, font_size=44).move_to(UP * 0.50)
        self.play(Write(series), run_time=0.85)
        concepts = VGroup(
            self.mini_tag("INFINITELY MANY SUB-INTERVALS", 22),
            Arrow(ORIGIN, RIGHT * 0.65, buff=0, color=BLACK_LINE, stroke_width=2.2),
            self.mini_tag("FINITE TOTAL?", 22),
            Arrow(ORIGIN, RIGHT * 0.65, buff=0, color=BLACK_LINE, stroke_width=2.2),
            self.mini_tag("WHAT IS AN INSTANT?", 22),
        ).arrange(RIGHT, buff=0.16).move_to(DOWN * 2.88)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in concepts], lag_ratio=0.10), run_time=1.25)
        self.wait(1.4)
        self.clear_stage()

    def newton_leibniz(self) -> None:
        self.set_header(8, "NEWTON + LEIBNIZ — CALCULUS", "1660s–1680s · Two notational traditions formalize the same limiting idea: instantaneous change.")
        left = self.panel(5.9, 2.85, LEFT * 3.35 + UP * 0.42, fill=WHITE)
        right = self.panel(5.9, 2.85, RIGHT * 3.35 + UP * 0.42, fill=WHITE)
        self.play(Create(left), Create(right), run_time=0.8)
        lh = self.text("NEWTON · FLUXIONS", 25, BOLD).move_to(left.get_top() + DOWN * 0.34)
        rh = self.text("LEIBNIZ · DIFFERENTIALS", 25, BOLD).move_to(right.get_top() + DOWN * 0.34)
        self.play(FadeIn(lh), FadeIn(rh), run_time=0.55)
        lax = Axes(x_range=[0, 3, 1], y_range=[0, 5, 1], x_length=3.85, y_length=1.50,
                   axis_config={"color": BLACK_LINE, "stroke_width": 1.6}, tips=True).move_to(left.get_center() + DOWN * 0.15)
        lcurve = lax.plot(lambda x: 0.5 * x * x, x_range=[0, 3], color=BLACK_LINE, stroke_width=2.7)
        ldot = Dot(lax.c2p(0.25, 0.031), radius=0.085, color=BLACK)
        self.play(Create(lax), Create(lcurve), FadeIn(ldot), run_time=0.75)
        self.play(MoveAlongPath(ldot, lcurve), run_time=1.45, rate_func=linear)
        flux = MathTex(r"\dot{x}", color=BLACK, font_size=43).move_to(left.get_bottom() + UP * 0.36)
        self.play(Write(flux), run_time=0.50)
        base = right.get_center() + DOWN * 0.20 + LEFT * 0.25
        dx = Line(base + LEFT * 1.10, base + RIGHT * 1.20, color=BLACK_LINE, stroke_width=3.5)
        dt = Line(base + LEFT * 1.10, base + LEFT * 1.10 + UP * 1.00, color=MID_GRAY, stroke_width=3.5)
        dxt = self.text("dx", 21, BOLD).next_to(dx, DOWN, buff=0.07)
        dtt = self.text("dt", 21, BOLD).next_to(dt, LEFT, buff=0.07)
        self.play(Create(dx), Create(dt), FadeIn(dxt), FadeIn(dtt), run_time=0.70)
        self.play(VGroup(dx, dxt).animate.scale(0.38, about_point=base + LEFT * 1.10),
                  VGroup(dt, dtt).animate.scale(0.38, about_point=base + LEFT * 1.10), run_time=0.95)
        leib = MathTex(r"\frac{dx}{dt}", color=BLACK, font_size=43).move_to(right.get_bottom() + UP * 0.36)
        self.play(Write(leib), run_time=0.50)
        formula_box = self.panel(11.8, 0.95, DOWN * 2.03, fill=VERY_LIGHT_GRAY, stroke=LIGHT_GRAY)
        central = MathTex(r"v(t)=\lim_{\Delta t\to0}\frac{\Delta x}{\Delta t}=\frac{dx}{dt}", color=BLACK, font_size=37).move_to(formula_box)
        self.play(FadeIn(formula_box), Write(central), run_time=0.95)
        core = self.question_card("Different notation — same central idea: the LIMIT of average rates.", 11.8, 27).move_to(DOWN * 3.18)
        self.play(FadeIn(core), run_time=0.70)
        self.wait(1.4)
        self.clear_stage()

    def position_velocity_acceleration(self) -> None:
        self.set_header(10, "POSITION → VELOCITY → ACCELERATION", "One motion, three synchronized views. A shared vertical cursor keeps the same instant aligned across all graphs.")
        ys = [1.28, -0.47, -2.22]
        funcs = [lambda t: 0.5*t*t, lambda t: t, lambda t: 1.0]
        yranges = [[0, 8, 2], [0, 4, 1], [0, 2, 1]]
        names = [("x–t", r"x=\frac12t^2"), ("v–t", r"v=t"), ("a–t", r"a=1")]
        axes, groups = [], VGroup()
        for y, fn, yr, (name, eq) in zip(ys, funcs, yranges, names):
            box = self.panel(12.15, 1.47, [0, y, 0], fill=WHITE, stroke=LIGHT_GRAY)
            ax = Axes(x_range=[0, 4, 1], y_range=yr, x_length=9.15, y_length=0.98,
                      axis_config={"color": BLACK_LINE, "stroke_width": 1.5}, tips=False).move_to([-0.10, y, 0])
            graph = ax.plot(fn, x_range=[0, 4], color=BLACK_LINE, stroke_width=2.8)
            tag = self.mini_tag(name, 21).move_to([-6.10, y + 0.30, 0])
            formula = MathTex(eq, color=BLACK, font_size=25).move_to([5.78, y - 0.08, 0])
            self.fit(formula, 1.35, 0.45)
            groups.add(VGroup(box, ax, graph, tag, formula)); axes.append(ax)
        self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.12), run_time=1.3)
        t = ValueTracker(0.15)
        cursors = VGroup(*[
            always_redraw(lambda i=i: DashedLine(
                axes[i].c2p(t.get_value(), yranges[i][0]),
                axes[i].c2p(t.get_value(), yranges[i][1]),
                color=MID_GRAY, stroke_width=1.4)) for i in range(3)
        ])
        dots = VGroup(*[
            always_redraw(lambda i=i: Dot(axes[i].c2p(t.get_value(), funcs[i](t.get_value())), radius=0.075, color=BLACK))
            for i in range(3)
        ])
        tnum = DecimalNumber(t.get_value(), num_decimal_places=1, color=BLACK, font_size=29)
        tnum.add_updater(lambda m: m.set_value(t.get_value()))
        read = VGroup(self.text("SAME INSTANT  t =", 21, BOLD), tnum, self.text("s", 19, BOLD)).arrange(RIGHT, buff=0.09).move_to(UP * 2.06)
        self.add(cursors, dots, read)
        self.play(t.animate.set_value(4.0), run_time=3.8, rate_func=linear)
        chain = VGroup(
            self.mini_tag("slope of x–t = v", 21), Arrow(ORIGIN, RIGHT * 0.62, buff=0, color=BLACK_LINE),
            self.mini_tag("slope of v–t = a", 21),
        ).arrange(RIGHT, buff=0.16).move_to(DOWN * 3.35)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in chain], lag_ratio=0.10), run_time=0.95)
        self.wait(1.4)
        self.clear_stage()

    def velocity_as_vector(self) -> None:
        self.set_header(11, "VELOCITY IS A VECTOR", "Speed is only the magnitude. Velocity also carries direction, so a turn changes velocity even at constant speed.")
        start = LEFT * 5.75 + DOWN * 1.25; corner = LEFT * 0.95 + DOWN * 1.25; end = LEFT * 0.95 + UP * 1.80
        road = VGroup(Line(start, corner, color=MID_GRAY, stroke_width=10), Line(corner, end, color=MID_GRAY, stroke_width=10))
        car = RoundedRectangle(width=1.28, height=0.66, corner_radius=0.14, color=BLACK_LINE, stroke_width=2.3, fill_color=SOFT, fill_opacity=1).move_to(start)
        angle = ValueTracker(0.0)
        arrow = always_redraw(lambda: Arrow(car.get_center(), car.get_center() + 2.2*np.array([math.cos(angle.get_value()), math.sin(angle.get_value()), 0]), buff=0.55, color=BLACK_LINE, stroke_width=4.5))
        self.play(Create(road), FadeIn(car), run_time=0.75); self.add(arrow)
        speed = self.readout("SPEED", r"20\,\mathrm{m/s}", RIGHT*4.25+UP*1.30, 4.25)
        vec = self.readout("VELOCITY", r"(20,0)\,\mathrm{m/s}", RIGHT*4.25+DOWN*0.10, 4.25)
        self.play(FadeIn(speed), FadeIn(vec), run_time=0.75)
        self.play(car.animate.move_to(corner + LEFT*0.58), run_time=1.8, rate_func=linear)
        newvec = self.readout("VELOCITY", r"(0,20)\,\mathrm{m/s}", RIGHT*4.25+DOWN*0.10, 4.25)
        self.play(car.animate.move_to(corner + UP*0.62), angle.animate.set_value(PI/2), Transform(vec, newvec), run_time=1.2, rate_func=smooth)
        self.play(car.animate.move_to(end), run_time=1.45, rate_func=linear)
        delta = MathTex(r"\Delta\vec v=(-20,20)\,\mathrm{m/s}", color=BLACK, font_size=38).move_to(RIGHT*4.25+DOWN*1.55)
        self.play(Write(delta), run_time=0.75)
        note = self.question_card("Same speed. Different direction. Therefore the velocity changed.", 11.7, 28).move_to(DOWN*3.22)
        self.play(FadeIn(note), run_time=0.70); self.wait(1.3); self.clear_stage()

    def einstein(self) -> None:
        self.set_header(13, "EINSTEIN — SPACE AND TIME MUST CHANGE", "1905 · If every inertial observer measures the same c, distances and time intervals cannot stay universally identical.")
        left = self.panel(6.05, 3.55, LEFT*3.45+UP*0.18, fill=WHITE)
        right = self.panel(6.05, 3.55, RIGHT*3.45+UP*0.18, fill=WHITE)
        self.play(Create(left), Create(right), run_time=0.75)
        self.play(FadeIn(self.text("LIGHT CLOCK AT REST", 22, BOLD).move_to(left.get_top()+DOWN*0.34)),
                  FadeIn(self.text("SAME CLOCK MOVING", 22, BOLD).move_to(right.get_top()+DOWN*0.34)), run_time=0.55)
        yb=-1.08; yt=1.03; lbase=LEFT*3.45; rbase=RIGHT*3.45
        mirrors_l=VGroup(Line(lbase+LEFT*1.0+[0,yb,0],lbase+RIGHT*1.0+[0,yb,0],color=BLACK_LINE,stroke_width=3),Line(lbase+LEFT*1.0+[0,yt,0],lbase+RIGHT*1.0+[0,yt,0],color=BLACK_LINE,stroke_width=3))
        mirrors_r=VGroup(Line(rbase+LEFT*1.0+[0,yb,0],rbase+RIGHT*1.0+[0,yb,0],color=BLACK_LINE,stroke_width=3),Line(rbase+LEFT*0.2+[0,yt,0],rbase+RIGHT*1.8+[0,yt,0],color=BLACK_LINE,stroke_width=3))
        lp=Dot(lbase+[0,yb+0.12,0],radius=0.10,color=BLACK); rp=Dot(rbase+[0,yb+0.12,0],radius=0.10,color=BLACK)
        ltop=lbase+[0,yt-0.12,0]; rtop=rbase+RIGHT*0.8+[0,yt-0.12,0]
        vert=DashedLine(lp.get_center(),ltop,color=MID_GRAY,stroke_width=2); diag=DashedLine(rp.get_center(),rtop,color=MID_GRAY,stroke_width=2)
        self.play(FadeIn(mirrors_l),FadeIn(mirrors_r),FadeIn(lp),FadeIn(rp),Create(vert),Create(diag),run_time=0.8)
        self.play(lp.animate.move_to(ltop), rp.animate.move_to(rtop), run_time=1.55, rate_func=linear)
        conclusion_box=self.panel(12.4,1.25,DOWN*2.62,fill=VERY_LIGHT_GRAY,stroke=LIGHT_GRAY)
        relation=VGroup(MathTex(r"c=\frac{\text{path length}}{\Delta t}",color=BLACK,font_size=35),self.text("Longer light path + same c  →  larger measured time interval",24,BOLD)).arrange(DOWN,buff=0.10).move_to(conclusion_box)
        self.fit(relation,11.7,0.90)
        self.play(FadeIn(conclusion_box),FadeIn(relation),run_time=0.8); self.wait(1.5); self.clear_stage()

    def minkowski(self) -> None:
        self.set_header(14, "MINKOWSKI — SPACETIME", "1908 · Motion becomes a worldline: a geometric history through one combined space–time diagram.")
        origin=LEFT*3.55+DOWN*2.05
        xaxis=Arrow(origin,origin+RIGHT*5.45,buff=0,color=BLACK_LINE,stroke_width=3)
        ctaxis=Arrow(origin,origin+UP*4.45,buff=0,color=BLACK_LINE,stroke_width=3)
        light1=Line(origin,origin+UR*3.05,color=MID_GRAY,stroke_width=2.3); light2=Line(origin,origin+UL*3.05,color=MID_GRAY,stroke_width=2.3)
        shade=Polygon(origin,origin+UR*3.00,origin+UP*4.30,origin+UL*3.00,stroke_width=0,fill_color=VERY_LIGHT_GRAY,fill_opacity=0.75)
        labs=VGroup(self.text("x",23,BOLD).next_to(xaxis.get_end(),RIGHT,buff=0.05),self.text("ct",23,BOLD).next_to(ctaxis.get_end(),UP,buff=0.05))
        self.play(FadeIn(shade),GrowArrow(xaxis),GrowArrow(ctaxis),FadeIn(labs),Create(light1),Create(light2),run_time=1.05)
        world=VMobject(color=BLACK_LINE,stroke_width=4); world.set_points_smoothly([origin,origin+UP*1.0+RIGHT*0.18,origin+UP*2.05+RIGHT*0.58,origin+UP*3.35+RIGHT*1.08])
        event=Dot(world.get_start(),radius=0.10,color=BLACK)
        self.play(Create(world),FadeIn(event),run_time=0.70); self.play(MoveAlongPath(event,world),run_time=2.0,rate_func=linear)
        right=self.note_panel("READ THE DIAGRAM",["more vertical → lower spatial speed","more tilted → larger spatial speed","45° boundary → light"],width=5.25,title_size=25,body_size=22).move_to(RIGHT*4.25+UP*0.55)
        self.play(FadeIn(right),run_time=0.75)
        formula_box=self.panel(5.45,0.90,RIGHT*4.25+DOWN*1.55,fill=WHITE,stroke=LIGHT_GRAY)
        spacetime=MathTex(r"\text{motion}=\text{worldline in spacetime}",color=BLACK,font_size=31).move_to(formula_box)
        self.fit(spacetime,4.95,0.52)
        self.play(FadeIn(formula_box),Write(spacetime),run_time=0.75); self.wait(1.5); self.clear_stage()

    def final_question(self) -> None:
        self.set_header(17, "FINAL DISCUSSION", "Use the history to explain why velocity was difficult to define — then connect that explanation to graphs.")
        q=self.question_card("Why was defining velocity historically difficult?",10.6,34).move_to(UP*1.75)
        self.play(FadeIn(q),run_time=0.75)
        ideas=[("CONTINUITY",[-4.30,0.50,0]),("INSTANT",[-2.45,-1.05,0]),("CHANGE",[0,0.72,0]),("DIRECTION",[2.45,-1.05,0]),("OBSERVER",[4.30,0.50,0])]
        cards=VGroup(*[self.mini_tag(name,23).move_to(pos) for name,pos in ideas])
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.08) for c in cards],lag_ratio=0.13),run_time=1.45)
        target=Dot([0,-0.42,0],radius=0.01,color=WHITE).set_opacity(0)
        arrows=VGroup(*[Arrow(c.get_center(),target.get_center(),buff=0.70,color=LIGHT_GRAY,stroke_width=2) for c in cards])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=0.08),run_time=1.05)
        center=MathTex(r"\boxed{\vec v(t)=\frac{d\vec x}{dt}}",color=BLACK,font_size=53).move_to([0,-0.42,0])
        self.play(Write(center),run_time=0.75); self.wait(1.0)
        self.play(FadeOut(VGroup(q,cards,arrows,target)),center.animate.move_to(UP*1.15),run_time=0.80)
        nextline=VGroup(self.mini_tag("x–t",27),Arrow(ORIGIN,RIGHT*0.80,buff=0,color=BLACK_LINE),self.mini_tag("v–t",27),Arrow(ORIGIN,RIGHT*0.80,buff=0,color=BLACK_LINE),self.mini_tag("a–t",27)).arrange(RIGHT,buff=0.20).move_to(DOWN*0.55)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m,Arrow) else FadeIn(m) for m in nextline],lag_ratio=0.10),run_time=1.10)
        closing=self.big_caption("NEXT: learn to read motion from graphs, not just formulas.",DOWN*2.28,12.0,30)
        self.play(FadeIn(closing,shift=UP*0.10),run_time=0.75); self.wait(2.0)
        self.standard_closing("Motion is a story written in change — and graphs let us read it.")


# Preview:
#   LESSON_TIME_SCALE=0.35 manim -pql history_of_velocity_FINAL_V5.py HistoryOfVelocityV5 --fps 15 --disable_caching
# Final target after audit:
#   LESSON_TIME_SCALE=1.65 manim -pqh history_of_velocity_FINAL_V5.py HistoryOfVelocityV5 --fps 30 --disable_caching
