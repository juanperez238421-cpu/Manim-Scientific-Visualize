#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""History of Velocity — Senior V4 visual reconstruction.

This file extends the validated V3 lesson but replaces the visually weak/static
sections with larger, synchronized, concept-driven animations.  It is designed
for ManimCE 0.20.1 and the exact JP classroom style.
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *
from history_of_velocity_FINAL_V3 import (
    HistoryOfVelocity,
    solve_kepler,
    ellipse_point_from_mean_anomaly,
    SOFT,
    LINE,
)


class HistoryOfVelocityV4(HistoryOfVelocity):
    """Senior reconstruction focused on visual hierarchy, motion and pedagogy."""

    # ------------------------------------------------------------------
    # V4 helpers
    # ------------------------------------------------------------------
    def panel(self, width: float, height: float, center=ORIGIN, fill=PAPER_GRAY, stroke=BLACK_LINE) -> RoundedRectangle:
        return RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=stroke, stroke_width=1.8,
            fill_color=fill, fill_opacity=1.0,
        ).move_to(center)

    def big_caption(self, text: str, center, width: float = 6.2, size: int = 28) -> Text:
        m = self.text(text, size, BOLD).move_to(center)
        self.fit(m, width, 0.78)
        return m

    def readout(self, label: str, value: str, center, width: float = 3.4) -> VGroup:
        box = self.panel(width, 0.92, center, fill=WHITE)
        a = self.text(label, 18, BOLD)
        b = MathTex(value, color=BLACK, font_size=31)
        g = VGroup(a, b).arrange(DOWN, buff=0.04).move_to(box)
        self.fit(g, width - 0.35, 0.66)
        return VGroup(box, g)

    def divider(self, x: float = 0.0, top: float = 2.05, bottom: float = -3.55) -> Line:
        return Line([x, top, 0], [x, bottom, 0], color=LIGHT_GRAY, stroke_width=1.6)

    # ------------------------------------------------------------------
    # Scene 0 — stronger opening choreography
    # ------------------------------------------------------------------
    def cold_open(self) -> None:
        eq = MathTex(r"v=\frac{\Delta x}{\Delta t}", color=BLACK, font_size=84)
        box = SurroundingRectangle(eq, buff=0.32, color=BLACK_LINE, stroke_width=2.4)
        self.play(Write(eq), Create(box), run_time=1.35)
        self.wait(1.2)

        labels = VGroup(
            self.mini_tag("SPACE", 27),
            self.mini_tag("TIME", 27),
            self.mini_tag("CHANGE", 27),
        ).arrange(RIGHT, buff=0.48).move_to(DOWN * 1.45)
        arrows = VGroup(
            Arrow(labels[0].get_top(), eq.get_bottom() + LEFT * 1.05, buff=0.12, color=MID_GRAY, stroke_width=2.4),
            Arrow(labels[1].get_top(), eq.get_bottom() + RIGHT * 1.05, buff=0.12, color=MID_GRAY, stroke_width=2.4),
        )
        self.play(LaggedStart(FadeIn(labels[0]), GrowArrow(arrows[0]), FadeIn(labels[1]), GrowArrow(arrows[1]), FadeIn(labels[2]), lag_ratio=0.16), run_time=1.7)

        statement = self.big_caption(
            "The formula is short. The problem behind it is not.",
            DOWN * 2.72, width=12.5, size=31,
        )
        self.play(FadeIn(statement, shift=UP * 0.10), run_time=0.8)
        self.wait(1.6)

        self.play(
            VGroup(eq, box).animate.scale(0.63).move_to(UP * 2.10),
            FadeOut(VGroup(labels, arrows, statement)),
            run_time=1.0,
        )
        q = self.question_card("Can velocity exist at one exact instant?", 10.2, 34).move_to(ORIGIN)
        ages = VGroup(
            self.text("~450 BC", 25, BOLD),
            Arrow(ORIGIN, RIGHT * 1.0, buff=0, color=BLACK_LINE),
            self.text("1600s", 25, BOLD),
            Arrow(ORIGIN, RIGHT * 1.0, buff=0, color=BLACK_LINE),
            self.text("1905", 25, BOLD),
        ).arrange(RIGHT, buff=0.26).move_to(DOWN * 1.50)
        self.play(FadeIn(q, shift=UP * 0.12), run_time=0.85)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in ages], lag_ratio=0.12), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(VGroup(eq, box, q, ages)), run_time=0.9)

    # ------------------------------------------------------------------
    # Scene 2 — Aristotle: theory vs measurement
    # ------------------------------------------------------------------
    def aristotle(self) -> None:
        self.set_header(2, "ARISTOTLE — BUILDING A THEORY OF MOTION", "~350 BC · A qualitative framework organized motion before precise measurement existed.")

        centers = [LEFT * 4.55 + DOWN * 0.15, DOWN * 0.15, RIGHT * 4.55 + DOWN * 0.15]
        titles = ["REST", "FORCED MOTION", "FALLING"]
        boxes = VGroup(*[self.panel(3.75, 3.85, c, fill=WHITE) for c in centers])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.14), run_time=1.2)

        ground1 = Line(LEFT * 1.35, RIGHT * 1.35, color=BLACK_LINE, stroke_width=2.5).move_to(centers[0] + DOWN * 0.75)
        block1 = Square(0.68, color=BLACK_LINE, fill_color=SOFT, fill_opacity=1).next_to(ground1, UP, buff=0)
        ground2 = Line(LEFT * 1.35, RIGHT * 1.35, color=BLACK_LINE, stroke_width=2.5).move_to(centers[1] + DOWN * 0.75)
        block2 = Square(0.68, color=BLACK_LINE, fill_color=SOFT, fill_opacity=1).move_to(ground2.get_left() + RIGHT * 0.45 + UP * 0.34)
        force2 = Arrow(block2.get_left() + LEFT * 0.85, block2.get_left() - LEFT * 0.04, buff=0, color=BLACK_LINE, stroke_width=4)
        ground3 = Line(LEFT * 1.35, RIGHT * 1.35, color=BLACK_LINE, stroke_width=2.5).move_to(centers[2] + DOWN * 0.95)
        ball3 = Circle(0.33, color=BLACK_LINE, fill_color=SOFT, fill_opacity=1).move_to(centers[2] + UP * 0.85)
        down3 = Arrow(ball3.get_bottom() + DOWN * 0.05, ball3.get_bottom() + DOWN * 0.90, buff=0, color=BLACK_LINE, stroke_width=3.5)

        heads = VGroup(*[self.text(t, 23, BOLD).move_to(c + UP * 1.50) for t, c in zip(titles, centers)])
        self.play(FadeIn(heads), Create(ground1), Create(ground2), Create(ground3), FadeIn(block1), FadeIn(block2), FadeIn(ball3), run_time=1.1)
        self.play(GrowArrow(force2), GrowArrow(down3), run_time=0.7)
        self.play(block2.animate.shift(RIGHT * 1.45), ball3.animate.shift(DOWN * 1.45), run_time=1.65)

        claims = VGroup(
            self.big_caption("natural state", centers[0] + DOWN * 1.35, 3.2, 20),
            self.big_caption("force sustains motion", centers[1] + DOWN * 1.35, 3.2, 20),
            self.big_caption("natural downward motion", centers[2] + DOWN * 1.35, 3.2, 20),
        )
        self.play(LaggedStart(*[FadeIn(c) for c in claims], lag_ratio=0.16), run_time=1.0)

        ribbon = self.question_card("Important step: build a coherent model. Missing step: measure motion precisely.", 13.4, 27).move_to(DOWN * 3.18)
        self.play(FadeIn(ribbon, shift=UP * 0.08), run_time=0.8)
        self.wait(2.4)
        self.clear_stage()

    def archimedes(self) -> None:
        self.set_header(3, "ARCHIMEDES — TURNING THE INFINITE INTO A TOOL", "~250 BC · Approximation shows how repeated refinement can approach an exact geometric quantity.")
        center = LEFT * 3.55 + DOWN * 0.45
        circle = Circle(2.0, color=BLACK_LINE, stroke_width=2.6).move_to(center)
        self.play(Create(circle), run_time=1.0)
        ns = [6, 12, 24, 48]
        polygons = [RegularPolygon(n=n, radius=2.0, color=BLACK_LINE, stroke_width=2.2).move_to(center) for n in ns]
        count = self.readout("SIDES", "6", RIGHT * 3.65 + UP * 1.10, 3.4)
        principle = self.note_panel("REFINEMENT", ["more sides", "smaller geometric error", "stable limiting value"], width=5.4, title_size=27, body_size=25).move_to(RIGHT * 3.65 + DOWN * 0.85)
        self.play(Create(polygons[0]), FadeIn(count), FadeIn(principle), run_time=1.0)
        current = polygons[0]
        for i, n in enumerate(ns[1:], start=1):
            new = polygons[i]
            new_count = self.readout("SIDES", str(n), RIGHT * 3.65 + UP * 1.10, 3.4)
            self.play(ReplacementTransform(current, new), Transform(count, new_count), run_time=0.95)
            current = new
            self.wait(0.35)
        ring = Annulus(inner_radius=1.90, outer_radius=2.06, color=LIGHT_GRAY, fill_opacity=0.65, stroke_width=0).move_to(center)
        self.play(FadeIn(ring), run_time=0.6)
        chain = VGroup(self.mini_tag("FINITE STEPS", 24), Arrow(ORIGIN, RIGHT * 0.8, buff=0, color=BLACK_LINE), self.mini_tag("REFINEMENT", 24), Arrow(ORIGIN, RIGHT * 0.8, buff=0, color=BLACK_LINE), self.mini_tag("LIMIT IDEA", 24)).arrange(RIGHT, buff=0.18).move_to(DOWN * 3.28)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in chain], lag_ratio=0.10), run_time=1.25)
        self.wait(2.4)
        self.clear_stage()

    def galileo(self) -> None:
        self.set_header(4, "GALILEO — MEASURE MOTION", "Early 1600s · Distance and time become data; motion can now be represented quantitatively.")
        divider = self.divider(0.2)
        self.play(Create(divider), run_time=0.5)
        ramp_start = LEFT * 6.4 + UP * 1.45
        ramp_end = LEFT * 0.85 + DOWN * 2.05
        ramp = Line(ramp_start, ramp_end, color=BLACK_LINE, stroke_width=4.2)
        floor = Line(LEFT * 6.5 + DOWN * 2.05, LEFT * 0.65 + DOWN * 2.05, color=LIGHT_GRAY, stroke_width=2)
        ball = Dot(ramp_start, radius=0.17, color=BLACK)
        timer = DecimalNumber(0, num_decimal_places=1, color=BLACK, font_size=36)
        timer_lab = self.text("t =", 24, BOLD)
        timer_unit = self.text("s", 22, BOLD)
        timer_g = VGroup(timer_lab, timer, timer_unit).arrange(RIGHT, buff=0.10).move_to(LEFT * 3.55 + UP * 2.05)
        t = ValueTracker(0.0)
        timer.add_updater(lambda m: m.set_value(t.get_value()))
        self.play(Create(ramp), Create(floor), FadeIn(ball), FadeIn(timer_g), run_time=1.0)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 16, 4], x_length=5.8, y_length=4.35, axis_config={"color": BLACK_LINE, "stroke_width": 2.0}, tips=True).move_to(RIGHT * 3.55 + DOWN * 0.50)
        xlab = self.text("time", 20, BOLD).next_to(ax.x_axis, DOWN, buff=0.14)
        ylab = self.text("distance", 20, BOLD).rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.12)
        graph = ax.plot(lambda x: x*x, x_range=[0, 4], color=BLACK_LINE, stroke_width=3.2)
        self.play(Create(ax), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        trace = TracedPath(ball.get_center, stroke_color=MID_GRAY, stroke_width=5, dissipating_time=None)
        gdot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), t.get_value()**2), radius=0.09, color=BLACK))
        vline = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(), 0), ax.c2p(t.get_value(), t.get_value()**2), color=MID_GRAY, stroke_width=1.5))
        self.add(trace, gdot, vline)
        ball.add_updater(lambda m: m.move_to(interpolate(ramp_start, ramp_end, min(1.0, (t.get_value()/4.0)**2))))
        self.play(Create(graph), t.animate.set_value(4.0), run_time=4.6, rate_func=linear)
        ball.clear_updaters()
        self.wait(0.8)
        relation = self.question_card("Equal time steps do NOT produce equal distance steps → speed is changing.", 13.1, 28).move_to(DOWN * 3.30)
        self.play(FadeIn(relation), run_time=0.8)
        self.wait(2.5)
        self.clear_stage()

    def average_vs_instantaneous_velocity(self) -> None:
        self.set_header(5, "AVERAGE VELOCITY IS NOT ENOUGH", "A smaller interval produces a more local slope; the limiting slope defines instantaneous velocity.")
        ax = Axes(x_range=[0, 4.6, 1], y_range=[0, 18, 4], x_length=9.0, y_length=5.05, axis_config={"color": BLACK_LINE, "stroke_width": 2.0}, tips=True).move_to(LEFT * 1.6 + DOWN * 0.55)
        curve = ax.plot(lambda x: x*x, x_range=[0, 4.2], color=BLACK_LINE, stroke_width=3.4)
        self.play(Create(ax), Create(curve), run_time=1.35)
        x0 = 2.0
        h = ValueTracker(1.6)
        p0 = ax.c2p(x0, x0*x0)
        p1 = always_redraw(lambda: Dot(ax.c2p(x0+h.get_value(), (x0+h.get_value())**2), radius=0.10, color=BLACK))
        p0dot = Dot(p0, radius=0.10, color=BLACK)
        secant = always_redraw(lambda: Line(ax.c2p(x0-0.70, x0*x0 - ((x0+h.get_value())**2-x0*x0)/h.get_value()*0.70), ax.c2p(x0+h.get_value()+0.45, (x0+h.get_value())**2 + ((x0+h.get_value())**2-x0*x0)/h.get_value()*0.45), color=MID_GRAY, stroke_width=3.2))
        dx = always_redraw(lambda: Line(p0, ax.c2p(x0+h.get_value(), x0*x0), color=BLACK_LINE, stroke_width=2))
        dy = always_redraw(lambda: Line(ax.c2p(x0+h.get_value(), x0*x0), ax.c2p(x0+h.get_value(), (x0+h.get_value())**2), color=BLACK_LINE, stroke_width=2))
        self.add(secant, dx, dy, p0dot, p1)
        h_num = DecimalNumber(h.get_value(), num_decimal_places=2, color=BLACK, font_size=34)
        h_num.add_updater(lambda m: m.set_value(h.get_value()))
        slope_num = DecimalNumber(2*x0+h.get_value(), num_decimal_places=2, color=BLACK, font_size=34)
        slope_num.add_updater(lambda m: m.set_value(2*x0+h.get_value()))
        read = VGroup(VGroup(self.text("Δt =", 23, BOLD), h_num).arrange(RIGHT, buff=0.10), VGroup(self.text("secant slope =", 23, BOLD), slope_num).arrange(RIGHT, buff=0.10)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rbox = self.panel(4.4, 1.65, RIGHT * 4.75 + UP * 0.90, fill=WHITE)
        read.move_to(rbox)
        self.play(FadeIn(rbox), FadeIn(read), run_time=0.8)
        for target in [0.8, 0.35, 0.12, 0.035]:
            self.play(h.animate.set_value(target), run_time=1.25, rate_func=smooth)
            self.wait(0.25)
        tangent = ax.plot(lambda x: 4*x-4, x_range=[0.7, 3.5], color=BLACK_LINE, stroke_width=4.0)
        tangent_lab = MathTex(r"v(2)=\frac{dx}{dt}=4", color=BLACK, font_size=45).move_to(RIGHT * 4.75 + DOWN * 0.75)
        self.play(Transform(secant, tangent), FadeIn(tangent_lab, shift=UP*0.10), run_time=1.0)
        limit = MathTex(r"\lim_{\Delta t\to0}\frac{\Delta x}{\Delta t}", color=BLACK, font_size=44).move_to(RIGHT * 4.75 + DOWN * 2.0)
        self.play(Write(limit), run_time=0.9)
        self.wait(2.3)
        self.clear_stage()

    def kepler(self) -> None:
        self.set_header(6, "KEPLER — EVEN THE PLANETS CHANGE SPEED", "1609 · Equal time intervals sweep equal areas, so orbital speed cannot remain constant.")
        center = LEFT * 2.55 + DOWN * 0.45
        a, b = 4.4, 2.45
        e = math.sqrt(1-(b*b)/(a*a))
        focus = center + LEFT * (a*e)
        ellipse = Ellipse(width=2*a, height=2*b, color=BLACK_LINE, stroke_width=2.6).move_to(center)
        sun = Dot(focus, radius=0.16, color=BLACK)
        self.play(Create(ellipse), FadeIn(sun), run_time=1.1)
        intervals = [(0.15, 0.80), (2.75, 3.40)]
        wedges = VGroup(); arc_labels = VGroup()
        for idx, (m0, m1) in enumerate(intervals):
            p0 = center + ellipse_point_from_mean_anomaly(m0, a, b, e)
            p1 = center + ellipse_point_from_mean_anomaly(m1, a, b, e)
            tri = Polygon(focus, p0, p1, stroke_color=MID_GRAY, stroke_width=2, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.75)
            wedges.add(tri)
            arc_labels.add(self.mini_tag("same Δt", 21).move_to((p0+p1)/2 + (UP if idx else DOWN)*0.55))
        self.play(LaggedStart(*[FadeIn(w) for w in wedges], lag_ratio=0.15), FadeIn(arc_labels), run_time=1.0)
        dot = Dot(radius=0.12, color=BLACK); self.add(dot)
        read = VGroup(self.readout("NEAR SUN", r"\text{long arc}", RIGHT*4.75+UP*0.75, 3.7), self.readout("FAR FROM SUN", r"\text{short arc}", RIGHT*4.75+DOWN*0.55, 3.7))
        self.play(FadeIn(read), run_time=0.8)
        for m0, m1 in intervals:
            path = VMobject(stroke_opacity=0)
            pts=[center+ellipse_point_from_mean_anomaly(M,a,b,e) for M in np.linspace(m0,m1,60)]
            path.set_points_smoothly(pts); dot.move_to(pts[0])
            self.play(MoveAlongPath(dot, path), run_time=1.65, rate_func=linear); self.wait(0.35)
        conclusion = self.question_card("Same time interval + different arc length → different speed.", 11.5, 30).move_to(DOWN*3.30)
        self.play(FadeIn(conclusion), run_time=0.8); self.wait(2.3); self.clear_stage()

    def calculus_problem(self) -> None:
        self.set_header(7, "THE NEED FOR CALCULUS", "The unresolved question is local: what is the rate of change at one instant, not across a large interval?")
        chain = VGroup(self.mini_tag("POSITION x(t)", 28), Arrow(ORIGIN, RIGHT*0.85, buff=0, color=BLACK_LINE), self.mini_tag("?", 34), Arrow(ORIGIN, RIGHT*0.85, buff=0, color=BLACK_LINE), self.mini_tag("VELOCITY v(t)", 28)).arrange(RIGHT, buff=0.22).move_to(UP*1.70)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m,Arrow) else FadeIn(m) for m in chain],lag_ratio=0.10),run_time=1.2)
        ax = Axes(x_range=[0,4,1], y_range=[0,10,2], x_length=8.2, y_length=3.9, axis_config={"color":BLACK_LINE,"stroke_width":2}).move_to(LEFT*1.55+DOWN*0.65)
        curve=ax.plot(lambda t:0.55*t*t, x_range=[0,4], color=BLACK_LINE, stroke_width=3.2)
        self.play(Create(ax),Create(curve),run_time=1.0)
        t0=2.2; p=Dot(ax.c2p(t0,0.55*t0*t0),radius=0.11,color=BLACK); self.play(FadeIn(p),run_time=0.5)
        intervals=VGroup()
        for width in [1.5,0.8,0.36,0.14]:
            intervals.add(Line(ax.c2p(t0-width/2,0),ax.c2p(t0+width/2,0),color=MID_GRAY,stroke_width=6))
        current=intervals[0]; self.play(Create(current),run_time=0.6)
        for nxt in intervals[1:]: self.play(Transform(current,nxt),run_time=0.75)
        local=self.panel(4.3,2.25,RIGHT*4.55+DOWN*0.75,fill=WHITE)
        local_txt=VGroup(self.text("AVERAGE",22,BOLD),MathTex(r"\frac{\Delta x}{\Delta t}",color=BLACK,font_size=43),self.text("interval shrinks",20),MathTex(r"\Downarrow",color=BLACK,font_size=30),self.text("INSTANTANEOUS",22,BOLD)).arrange(DOWN,buff=0.08).move_to(local)
        self.play(Create(local),FadeIn(local_txt),run_time=0.8)
        q=self.question_card("How do we make Δt approach zero without dividing by zero?",11.4,29).move_to(DOWN*3.28)
        self.play(FadeIn(q),run_time=0.8); self.wait(2.5); self.clear_stage()

    def newton_leibniz(self) -> None:
        self.set_header(8, "NEWTON + LEIBNIZ — CALCULUS", "1660s–1680s · Two notational traditions formalize the same limiting idea: instantaneous change.")
        left=self.panel(6.2,3.55,LEFT*3.55+UP*0.10,fill=WHITE); right=self.panel(6.2,3.55,RIGHT*3.55+UP*0.10,fill=WHITE)
        self.play(Create(left),Create(right),run_time=0.9)
        lh=self.text("NEWTON · FLUXIONS",27,BOLD).move_to(left.get_top()+DOWN*0.42); rh=self.text("LEIBNIZ · DIFFERENTIALS",27,BOLD).move_to(right.get_top()+DOWN*0.42)
        self.play(FadeIn(lh),FadeIn(rh),run_time=0.6)
        lax=Axes(x_range=[0,3,1],y_range=[0,5,1],x_length=4.2,y_length=2.0,axis_config={"color":BLACK_LINE,"stroke_width":1.7}).move_to(left.get_center()+DOWN*0.25)
        lcurve=lax.plot(lambda x:0.5*x*x,x_range=[0,3],color=BLACK_LINE,stroke_width=2.8); ldot=Dot(lax.c2p(0.3,0.045),radius=0.09,color=BLACK)
        self.play(Create(lax),Create(lcurve),FadeIn(ldot),run_time=0.8); self.play(MoveAlongPath(ldot,lcurve),run_time=1.6,rate_func=linear)
        flux=MathTex(r"\dot x",color=BLACK,font_size=52).move_to(left.get_bottom()+UP*0.55); self.play(Write(flux),run_time=0.6)
        base=RIGHT*3.55+DOWN*0.45
        dx=Line(base+LEFT*1.45,base+RIGHT*1.2,color=BLACK_LINE,stroke_width=4); dt=Line(base+LEFT*1.45,base+LEFT*1.45+UP*1.25,color=MID_GRAY,stroke_width=4)
        dxt=self.text("dx",23,BOLD).next_to(dx,DOWN,buff=0.08); dtt=self.text("dt",23,BOLD).next_to(dt,LEFT,buff=0.08)
        self.play(Create(dx),Create(dt),FadeIn(dxt),FadeIn(dtt),run_time=0.8)
        self.play(VGroup(dx,dxt).animate.scale(0.38,about_point=base+LEFT*1.45),VGroup(dt,dtt).animate.scale(0.38,about_point=base+LEFT*1.45),run_time=1.0)
        leib=MathTex(r"\frac{dx}{dt}",color=BLACK,font_size=52).move_to(right.get_bottom()+UP*0.55); self.play(Write(leib),run_time=0.6)
        central=MathTex(r"\boxed{v(t)=\lim_{\Delta t\to0}\frac{\Delta x}{\Delta t}=\frac{dx}{dt}}",color=BLACK,font_size=45).move_to(DOWN*2.05)
        self.play(Write(central),run_time=1.1)
        core=self.question_card("Different notation — same central idea: a LIMIT of average rates.",12.6,29).move_to(DOWN*3.22)
        self.play(FadeIn(core),run_time=0.8); self.wait(2.5); self.clear_stage()

    def newtons_laws(self) -> None:
        self.set_header(9, "NEWTON — A NEW THEORY OF MOTION", "1687 · Forces explain changes in velocity; they do not need to sustain uniform motion.")
        upper=UP*0.70; lower=DOWN*0.85
        tracks=VGroup(Line(LEFT*5.5,RIGHT*5.5,color=BLACK_LINE,stroke_width=2.5).move_to(upper),Line(LEFT*5.5,RIGHT*5.5,color=BLACK_LINE,stroke_width=2.5).move_to(lower))
        labs=VGroup(self.mini_tag("ROUGH",21).next_to(tracks[0],LEFT,buff=0.18),self.mini_tag("IDEAL",21).next_to(tracks[1],LEFT,buff=0.18))
        r=Square(0.54,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(tracks[0].get_left()+RIGHT*0.7+UP*0.27); s=Square(0.54,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(tracks[1].get_left()+RIGHT*0.7+UP*0.27)
        self.play(Create(tracks),FadeIn(labs),FadeIn(r),FadeIn(s),run_time=0.9)
        trail_r=TracedPath(r.get_center,stroke_color=MID_GRAY,stroke_width=3); trail_s=TracedPath(s.get_center,stroke_color=MID_GRAY,stroke_width=3); self.add(trail_r,trail_s)
        self.play(r.animate.shift(RIGHT*4.0),s.animate.shift(RIGHT*8.5),run_time=2.3,rate_func=linear)
        law1=MathTex(r"\sum \vec F=0\Rightarrow \vec v=\mathrm{constant}",color=BLACK,font_size=40).move_to(DOWN*2.45); self.play(Write(law1),run_time=0.75); self.wait(1.1)
        self.play(FadeOut(VGroup(tracks,labs,r,s,trail_r,trail_s,law1)),run_time=0.75)
        body=Square(0.72,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(LEFT*5.1+DOWN*0.20); force=Arrow(body.get_left()+LEFT*1.2,body.get_left()-LEFT*0.05,buff=0,color=BLACK_LINE,stroke_width=5)
        self.play(FadeIn(body),GrowArrow(force),run_time=0.7)
        vel_len=ValueTracker(0.8); vel=always_redraw(lambda:Arrow(body.get_right(),body.get_right()+RIGHT*vel_len.get_value(),buff=0,color=MID_GRAY,stroke_width=4)); self.add(vel)
        for d,L in [(1.4,1.2),(1.6,1.75),(1.8,2.35)]: self.play(body.animate.shift(RIGHT*d),vel_len.animate.set_value(L),force.animate.shift(RIGHT*d),run_time=1.0,rate_func=rate_functions.ease_in_quad)
        eq=MathTex(r"\boxed{\sum\vec F=m\vec a}\qquad \vec a=\frac{\Delta\vec v}{\Delta t}",color=BLACK,font_size=43).move_to(DOWN*2.25); self.play(Write(eq),run_time=0.9); self.wait(1.2)
        self.play(FadeOut(VGroup(body,force,vel,eq)),run_time=0.75)
        A=Circle(0.44,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(LEFT*1.0); B=Circle(0.44,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(RIGHT*1.0); pair=MathTex(r"\vec F_{AB}=-\vec F_{BA}",color=BLACK,font_size=45).move_to(UP*1.45)
        self.play(FadeIn(A),FadeIn(B),Write(pair),run_time=0.8)
        f1=Arrow(A.get_center(),A.get_center()+LEFT*1.4,buff=0.46,color=BLACK_LINE,stroke_width=4); f2=Arrow(B.get_center(),B.get_center()+RIGHT*1.4,buff=0.46,color=MID_GRAY,stroke_width=4)
        self.play(GrowArrow(f1),GrowArrow(f2),run_time=0.7); self.play(A.animate.shift(LEFT*2.8),B.animate.shift(RIGHT*2.8),f1.animate.shift(LEFT*2.8),f2.animate.shift(RIGHT*2.8),run_time=1.7,rate_func=smooth)
        conclusion=self.question_card("Forces explain WHY velocity changes. Kinematics describes HOW it changes.",12.6,29).move_to(DOWN*3.22)
        self.play(FadeIn(conclusion),run_time=0.8); self.wait(2.4); self.clear_stage()

    def position_velocity_acceleration(self) -> None:
        self.set_header(10, "POSITION → VELOCITY → ACCELERATION", "One motion, three synchronized views. A shared vertical cursor keeps the same instant aligned across all graphs.")
        xlen=10.2; ys=[1.35,-0.45,-2.25]; funcs=[lambda t:0.5*t*t,lambda t:t,lambda t:1.0]; yranges=[[0,8,2],[0,4,1],[0,2,1]]; names=[("x–t",r"x=\frac12t^2"),("v–t",r"v=t"),("a–t",r"a=1")]
        axes=[]; groups=VGroup()
        for y,fn,yr,(name,eq) in zip(ys,funcs,yranges,names):
            box=self.panel(12.3,1.55,[0,y,0],fill=WHITE,stroke=LIGHT_GRAY); ax=Axes(x_range=[0,4,1],y_range=yr,x_length=xlen,y_length=1.05,axis_config={"color":BLACK_LINE,"stroke_width":1.5},tips=False).move_to([0.15,y,0]); graph=ax.plot(fn,x_range=[0,4],color=BLACK_LINE,stroke_width=2.8); tag=self.mini_tag(name,22).move_to([-6.4,y+0.35,0]); formula=MathTex(eq,color=BLACK,font_size=27).move_to([6.35,y-0.10,0]); groups.add(VGroup(box,ax,graph,tag,formula)); axes.append(ax)
        self.play(LaggedStart(*[FadeIn(g) for g in groups],lag_ratio=0.12),run_time=1.4)
        t=ValueTracker(0.15)
        cursors=VGroup(*[always_redraw(lambda i=i: DashedLine(axes[i].c2p(t.get_value(),yranges[i][0]),axes[i].c2p(t.get_value(),yranges[i][1]),color=MID_GRAY,stroke_width=1.4)) for i in range(3)])
        dots=VGroup(*[always_redraw(lambda i=i: Dot(axes[i].c2p(t.get_value(),funcs[i](t.get_value())),radius=0.075,color=BLACK)) for i in range(3)])
        tnum=DecimalNumber(t.get_value(),num_decimal_places=1,color=BLACK,font_size=31); tnum.add_updater(lambda m:m.set_value(t.get_value())); read=VGroup(self.text("SAME INSTANT  t =",22,BOLD),tnum,self.text("s",20,BOLD)).arrange(RIGHT,buff=0.10).move_to(UP*2.15)
        self.add(cursors,dots,read); self.play(t.animate.set_value(4.0),run_time=4.0,rate_func=linear)
        chain=VGroup(self.mini_tag("slope of x–t = v",22),Arrow(ORIGIN,RIGHT*0.65,buff=0,color=BLACK_LINE),self.mini_tag("slope of v–t = a",22)).arrange(RIGHT,buff=0.18).move_to(DOWN*3.42)
        self.play(LaggedStart(*[GrowArrow(m) if isinstance(m,Arrow) else FadeIn(m) for m in chain],lag_ratio=0.10),run_time=1.0); self.wait(2.2); self.clear_stage()

    def velocity_as_vector(self) -> None:
        self.set_header(11, "VELOCITY IS A VECTOR", "Speed is only the magnitude. Velocity also carries direction, so a turn changes velocity even at constant speed.")
        start=LEFT*5.8+DOWN*1.30; corner=LEFT*0.7+DOWN*1.30; end=LEFT*0.7+UP*1.95
        road=VGroup(Line(start,corner,color=LIGHT_GRAY,stroke_width=8),Line(corner,end,color=LIGHT_GRAY,stroke_width=8)); car=RoundedRectangle(width=1.0,height=0.52,corner_radius=0.12,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(start); angle=ValueTracker(0.0); arrow=always_redraw(lambda:Arrow(car.get_center(),car.get_center()+2.0*np.array([math.cos(angle.get_value()),math.sin(angle.get_value()),0]),buff=0.45,color=BLACK_LINE,stroke_width=4))
        self.play(Create(road),FadeIn(car),run_time=0.8); self.add(arrow)
        speed=self.readout("SPEED",r"20\,\mathrm{m/s}",RIGHT*4.35+UP*1.35,4.2); vec=self.readout("VELOCITY",r"(20,0)\,\mathrm{m/s}",RIGHT*4.35+DOWN*0.05,4.2)
        self.play(FadeIn(speed),FadeIn(vec),run_time=0.8); self.play(car.animate.move_to(corner+LEFT*0.5),run_time=2.0,rate_func=linear)
        newvec=self.readout("VELOCITY",r"(0,20)\,\mathrm{m/s}",RIGHT*4.35+DOWN*0.05,4.2)
        self.play(car.animate.move_to(corner+UP*0.55),angle.animate.set_value(PI/2),Transform(vec,newvec),run_time=1.3,rate_func=smooth); self.play(car.animate.move_to(end),run_time=1.6,rate_func=linear)
        delta=MathTex(r"\Delta\vec v=(-20,20)\,\mathrm{m/s}",color=BLACK,font_size=40).move_to(RIGHT*4.35+DOWN*1.55); self.play(Write(delta),run_time=0.8)
        note=self.question_card("Same speed. Different direction. Therefore the velocity changed.",11.9,29).move_to(DOWN*3.25); self.play(FadeIn(note),run_time=0.8); self.wait(2.3); self.clear_stage()

    def light_problem(self) -> None:
        self.set_header(12, "LIGHT CREATES A NEW PROBLEM", "19th century · Classical velocity addition predicts different light speeds for different observers — experiments do not.")
        left=self.panel(6.35,4.45,LEFT*3.55+DOWN*0.45,fill=WHITE); right=self.panel(6.35,4.45,RIGHT*3.55+DOWN*0.45,fill=WHITE)
        self.play(Create(left),Create(right),run_time=0.9); heads=VGroup(self.text("GROUND FRAME",25,BOLD).move_to(left.get_top()+DOWN*0.42),self.text("MOVING FRAME",25,BOLD).move_to(right.get_top()+DOWN*0.42)); self.play(FadeIn(heads),run_time=0.6)
        rails=[]; photons=[]; clocks=[]
        for box in [left,right]:
            rail=Line(box.get_left()+RIGHT*0.55+DOWN*0.55,box.get_right()+LEFT*0.55+DOWN*0.55,color=BLACK_LINE,stroke_width=2.5); photon=Dot(rail.get_left()+RIGHT*0.15,radius=0.11,color=BLACK); clock=DecimalNumber(0,num_decimal_places=1,color=BLACK,font_size=30).move_to(box.get_center()+UP*1.05); lab=self.text("time",18,BOLD).next_to(clock,LEFT,buff=0.12); rails.append(rail); photons.append(photon); clocks.append(VGroup(lab,clock))
        self.play(*[Create(r) for r in rails],*[FadeIn(p) for p in photons],*[FadeIn(c) for c in clocks],run_time=0.9)
        self.play(photons[0].animate.move_to(rails[0].get_right()+LEFT*0.15),photons[1].animate.move_to(rails[1].get_right()+LEFT*0.15),clocks[0][1].animate.set_value(1.0),clocks[1][1].animate.set_value(1.0),run_time=2.3,rate_func=linear)
        c1=MathTex(r"c=3.00\times10^8\,\mathrm{m/s}",color=BLACK,font_size=31).move_to(left.get_bottom()+UP*0.55); c2=MathTex(r"c=3.00\times10^8\,\mathrm{m/s}",color=BLACK,font_size=31).move_to(right.get_bottom()+UP*0.55)
        self.play(Write(c1),Write(c2),run_time=0.8)
        classical=MathTex(r"c-v\quad\text{?}",color=BLACK,font_size=43).move_to(DOWN*3.25+LEFT*1.7); strike=Line(classical.get_left()+LEFT*0.15,classical.get_right()+RIGHT*0.15,color=BLACK_LINE,stroke_width=4).rotate(-0.15).move_to(classical); fact=self.mini_tag("BOTH MEASURE c",26).move_to(DOWN*3.25+RIGHT*2.55)
        self.play(Write(classical),Create(strike),FadeIn(fact),run_time=0.9); self.wait(2.3); self.clear_stage()

    def einstein(self) -> None:
        self.set_header(13, "EINSTEIN — SPACE AND TIME MUST CHANGE", "1905 · If every inertial observer measures the same c, distances and time intervals cannot stay universally identical.")
        left=self.panel(6.2,4.25,LEFT*3.55+DOWN*0.35,fill=WHITE); right=self.panel(6.2,4.25,RIGHT*3.55+DOWN*0.35,fill=WHITE); self.play(Create(left),Create(right),run_time=0.8)
        self.play(FadeIn(self.text("LIGHT CLOCK AT REST",23,BOLD).move_to(left.get_top()+DOWN*0.38)),FadeIn(self.text("SAME CLOCK MOVING",23,BOLD).move_to(right.get_top()+DOWN*0.38)),run_time=0.6)
        yb=-1.4; yt=0.95; lbase=LEFT*3.55
        mirrors_l=VGroup(Line(lbase+LEFT*1.0+[0,yb,0],lbase+RIGHT*1.0+[0,yb,0],color=BLACK_LINE,stroke_width=3),Line(lbase+LEFT*1.0+[0,yt,0],lbase+RIGHT*1.0+[0,yt,0],color=BLACK_LINE,stroke_width=3)); lp=Dot(lbase+[0,yb+0.12,0],radius=0.10,color=BLACK)
        rbase=RIGHT*3.55; mirrors_r=VGroup(Line(rbase+LEFT*1.0+[0,yb,0],rbase+RIGHT*1.0+[0,yb,0],color=BLACK_LINE,stroke_width=3),Line(rbase+LEFT*0.2+[0,yt,0],rbase+RIGHT*1.8+[0,yt,0],color=BLACK_LINE,stroke_width=3)); rp=Dot(rbase+[0,yb+0.12,0],radius=0.10,color=BLACK)
        diag=DashedLine(rp.get_center(),rbase+RIGHT*0.8+[0,yt-0.12,0],color=MID_GRAY,stroke_width=2); vert=DashedLine(lp.get_center(),lbase+[0,yt-0.12,0],color=MID_GRAY,stroke_width=2)
        self.play(FadeIn(mirrors_l),FadeIn(mirrors_r),FadeIn(lp),FadeIn(rp),Create(vert),Create(diag),run_time=0.9); self.play(lp.animate.move_to(lbase+[0,yt-0.12,0]),rp.animate.move_to(rbase+RIGHT*0.8+[0,yt-0.12,0]),run_time=1.7,rate_func=linear)
        relation=VGroup(MathTex(r"c=\frac{\text{path length}}{\Delta t}",color=BLACK,font_size=42),self.text("Longer light path + same c → larger measured time interval",26,BOLD)).arrange(DOWN,buff=0.24).move_to(DOWN*2.80); self.fit(relation,13.0,1.15)
        self.play(FadeIn(relation),run_time=0.9); self.wait(2.2); self.clear_stage()

    def minkowski(self) -> None:
        self.set_header(14, "MINKOWSKI — SPACETIME", "1908 · Motion becomes a worldline: a geometric history through one combined space–time diagram.")
        origin=LEFT*3.3+DOWN*2.15; xaxis=Arrow(origin,origin+RIGHT*6.0,buff=0,color=BLACK_LINE,stroke_width=3); ctaxis=Arrow(origin,origin+UP*4.7,buff=0,color=BLACK_LINE,stroke_width=3); light1=Line(origin,origin+UR*3.25,color=MID_GRAY,stroke_width=2.4); light2=Line(origin,origin+UL*3.25,color=MID_GRAY,stroke_width=2.4); shade=Polygon(origin,origin+UR*3.20,origin+UP*4.55,origin+UL*3.20,stroke_width=0,fill_color=VERY_LIGHT_GRAY,fill_opacity=0.75); labs=VGroup(self.text("x",24,BOLD).next_to(xaxis.get_end(),RIGHT,buff=0.05),self.text("ct",24,BOLD).next_to(ctaxis.get_end(),UP,buff=0.05))
        self.play(FadeIn(shade),GrowArrow(xaxis),GrowArrow(ctaxis),FadeIn(labs),Create(light1),Create(light2),run_time=1.2)
        world=VMobject(color=BLACK_LINE,stroke_width=4); world.set_points_smoothly([origin,origin+UP*1.1+RIGHT*0.2,origin+UP*2.25+RIGHT*0.65,origin+UP*3.55+RIGHT*1.15]); event=Dot(world.get_start(),radius=0.10,color=BLACK)
        self.play(Create(world),FadeIn(event),run_time=0.8); self.play(MoveAlongPath(event,world),run_time=2.2,rate_func=linear)
        right=self.note_panel("READ THE DIAGRAM",["vertical tendency → low spatial speed","tilted worldline → larger spatial speed","45° boundary → light"],width=5.6,title_size=27,body_size=24).move_to(RIGHT*4.35+UP*0.25); self.play(FadeIn(right),run_time=0.8)
        spacetime=MathTex(r"\boxed{\text{motion}=\text{worldline in spacetime}}",color=BLACK,font_size=40).move_to(RIGHT*4.0+DOWN*2.05); self.play(Write(spacetime),run_time=0.85); self.wait(2.5); self.clear_stage()

    def return_to_beginning(self) -> None:
        self.set_header(15, "RETURN TO THE BEGINNING", "The modern formula condenses a long chain of conceptual advances rather than replacing that history.")
        line=Line(LEFT*6.4,RIGHT*6.4,color=BLACK_LINE,stroke_width=3).move_to(DOWN*0.35); xs=np.linspace(-5.9,5.9,6); data=[("ZENO","continuity"),("GALILEO","measurement"),("KEPLER","variable speed"),("CALCULUS","instantaneous rate"),("NEWTON","dynamics"),("EINSTEIN","observer")]; nodes=VGroup(); labels=VGroup()
        for idx,(x,(name,idea)) in enumerate(zip(xs,data)):
            d=Dot([x,-0.35,0],radius=0.12,color=BLACK); nodes.add(d); lab=VGroup(self.text(name,22,BOLD),self.text(idea,18)).arrange(DOWN,buff=0.04).move_to([x,0.52 if idx%2==0 else -1.22,0]); labels.add(lab)
        self.play(Create(line),run_time=0.7)
        for d,lab in zip(nodes,labels): self.play(FadeIn(d),FadeIn(lab,shift=UP*0.06),run_time=0.45)
        eq=MathTex(r"\boxed{v=\frac{\Delta x}{\Delta t}\quad\longrightarrow\quad v(t)=\frac{dx}{dt}}",color=BLACK,font_size=52).move_to(UP*2.05); self.play(Write(eq),run_time=1.0)
        sweep=Dot(line.get_left(),radius=0.10,color=BLACK); self.add(sweep); self.play(MoveAlongPath(sweep,line),run_time=3.2,rate_func=linear)
        q=self.question_card("A short formula now carries 2,000+ years of ideas about continuity, measurement and change.",13.1,28).move_to(DOWN*3.25); self.play(FadeIn(q),run_time=0.8); self.wait(2.2); self.clear_stage()

    def course_bridge(self) -> None:
        self.set_header(16, "CONNECTION TO THIS PERIOD", "We now turn the historical questions into practical tools: forces, motion diagrams and synchronized graphs.")
        left=self.panel(6.3,4.45,LEFT*3.6+DOWN*0.45,fill=WHITE); right=self.panel(6.3,4.45,RIGHT*3.6+DOWN*0.45,fill=WHITE); self.play(Create(left),Create(right),run_time=0.8)
        self.play(FadeIn(self.text("WHY MOTION CHANGES",25,BOLD).move_to(left.get_top()+DOWN*0.40)),FadeIn(self.text("HOW MOTION CHANGES",25,BOLD).move_to(right.get_top()+DOWN*0.40)),run_time=0.6)
        ramp=Line(left.get_left()+RIGHT*0.75+DOWN*1.15,left.get_right()+LEFT*0.65+UP*0.90,color=BLACK_LINE,stroke_width=4); block=Square(0.58,color=BLACK_LINE,fill_color=SOFT,fill_opacity=1).move_to(ramp.point_from_proportion(0.82)+UP*0.18); mg=Arrow(block.get_center(),block.get_center()+DOWN*1.15,buff=0.05,color=BLACK_LINE,stroke_width=3); para=Arrow(block.get_center(),block.get_center()+DL*1.05,buff=0.05,color=MID_GRAY,stroke_width=4)
        self.play(Create(ramp),FadeIn(block),GrowArrow(mg),GrowArrow(para),run_time=0.8); self.play(block.animate.move_to(ramp.point_from_proportion(0.12)+UP*0.18),run_time=2.0,rate_func=rate_functions.ease_in_quad); why=MathTex(r"\sum F\Rightarrow a",color=BLACK,font_size=43).move_to(left.get_bottom()+UP*0.55); self.play(Write(why),run_time=0.7)
        y0=[0.9,-0.35,-1.60]; fns=[lambda t:0.5*t*t,lambda t:t,lambda t:1]; yr=[[0,5,1],[0,3,1],[0,2,1]]; tags=["x–t","v–t","a–t"]
        for y,fn,yrr,tag in zip(y0,fns,yr,tags):
            ax=Axes(x_range=[0,3,1],y_range=yrr,x_length=3.8,y_length=0.85,axis_config={"color":BLACK_LINE,"stroke_width":1.3},tips=False).move_to(right.get_center()+[0,y,0]); gr=ax.plot(fn,x_range=[0,3],color=BLACK_LINE,stroke_width=2.4); lab=self.mini_tag(tag,19).next_to(ax,LEFT,buff=0.15); self.play(Create(ax),Create(gr),FadeIn(lab),run_time=0.55)
        bridge=self.question_card("FORCES explain why. GRAPHS reveal how.",9.4,31).move_to(DOWN*3.25); self.play(FadeIn(bridge),run_time=0.8); self.wait(2.4); self.clear_stage()

    def final_question(self) -> None:
        self.set_header(17, "FINAL DISCUSSION", "Use the history to explain why velocity was difficult to define — then connect that explanation to graphs.")
        q=self.question_card("Why was defining velocity historically difficult?",10.6,34).move_to(UP*1.85); self.play(FadeIn(q),run_time=0.8)
        ideas=[("CONTINUITY",LEFT*4.5+UP*0.30),("INSTANT",LEFT*2.25+DOWN*1.35),("CHANGE",DOWN*0.05),("DIRECTION",RIGHT*2.25+DOWN*1.35),("OBSERVER",RIGHT*4.5+UP*0.30)]
        cards=VGroup(*[self.mini_tag(name,24).move_to(pos) for name,pos in ideas]); self.play(LaggedStart(*[FadeIn(c,shift=UP*0.08) for c in cards],lag_ratio=0.14),run_time=1.6)
        center=MathTex(r"\boxed{\vec v(t)=\frac{d\vec x}{dt}}",color=BLACK,font_size=57).move_to(DOWN*0.10); arrows=VGroup(*[Arrow(c.get_center(),center.get_center(),buff=0.58,color=LIGHT_GRAY,stroke_width=2) for c in cards]); self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=0.08),Write(center),run_time=1.6); self.wait(1.8)
        self.play(FadeOut(VGroup(q,cards,arrows)),center.animate.move_to(UP*1.20),run_time=0.9)
        nextline=VGroup(self.mini_tag("x–t",28),Arrow(ORIGIN,RIGHT*0.85,buff=0,color=BLACK_LINE),self.mini_tag("v–t",28),Arrow(ORIGIN,RIGHT*0.85,buff=0,color=BLACK_LINE),self.mini_tag("a–t",28)).arrange(RIGHT,buff=0.22).move_to(DOWN*0.55); self.play(LaggedStart(*[GrowArrow(m) if isinstance(m,Arrow) else FadeIn(m) for m in nextline],lag_ratio=0.10),run_time=1.25)
        closing=self.big_caption("NEXT: learn to read motion from graphs, not just formulas.",DOWN*2.30,12.0,31); self.play(FadeIn(closing,shift=UP*0.10),run_time=0.8); self.wait(3.2); self.standard_closing("Motion is a story written in change — and graphs let us read it.")


# Preview:
#   LESSON_TIME_SCALE=0.55 manim -pql history_of_velocity_FINAL_V4.py HistoryOfVelocityV4 --fps 15 --disable_caching
# Final:
#   LESSON_TIME_SCALE=1.0 manim -pqh history_of_velocity_FINAL_V4.py HistoryOfVelocityV4 --fps 30 --disable_caching
