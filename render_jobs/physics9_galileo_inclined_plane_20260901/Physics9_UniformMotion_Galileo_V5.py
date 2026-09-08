#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 V5 · Graphs first, Galileo inclined-plane experiment second.

Pedagogical order:
1) Position-time and velocity-time graphs for uniform motion.
2) Deduce x = x_i + vt from velocity definition.
3) Present Galileo's inclined-plane experiment with equal-time position records.
4) Observe 0,1,4,9,16 cumulative positions and 1,3,5,7 interval distances.
5) Deduce x proportional to t^2 and preview the falling-motion equation.

No formal acceleration lesson is included.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_Galileo_Uniform_Motion_Fall_Intro_V3 import (
    Physics9GalileoUniformMotionFallIntroV3,
    BLACK_TEXT,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    RUN,
    RUN_FAST,
    RUN_SLOW,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
)


class Physics9UniformMotionGalileoV5(Physics9GalileoUniformMotionFallIntroV3):
    """Uniform-motion graphs -> x=x_i+vt -> Galileo experiment -> t^2 preview."""

    def validate_lesson_data(self):
        t = np.array([0, 1, 2, 3, 4], dtype=float)
        xi = 1.0
        v = 1.5
        x = xi + v * t
        assert np.allclose(x, [1.0, 2.5, 4.0, 5.5, 7.0])
        assert np.allclose(np.diff(x), [1.5, 1.5, 1.5, 1.5])
        s = t ** 2
        assert np.allclose(s, [0, 1, 4, 9, 16])
        assert np.allclose(np.diff(s), [1, 3, 5, 7])

    def construct(self):
        self.opening_v5()
        self.uniform_motion_two_graphs()
        self.derive_position_equation()
        self.graph_equation_connection()
        self.galileo_question_v5()
        self.galileo_real_apparatus_v5()
        self.galileo_equal_time_pattern_v5()
        self.galileo_deduction_v5()
        self.falling_equation_preview_v5()
        self.summary_v5()

    def opening_v5(self):
        kicker = self.txt("PHYSICS 9 | KINEMATICS", 27, BOLD)
        main = self.txt("MOTION GRAPHS -> EQUATION -> GALILEO", 45, BOLD)
        sub = self.txt("First understand uniform motion. Then compare it with Galileo's inclined-plane experiment.", 25)
        eqs = VGroup(
            self.formula_panel(r"\boxed{x=x_i+vt}", width=4.4, height=1.05, size=48),
            self.formula_panel(r"\boxed{x\propto t^2}", width=4.4, height=1.05, size=44),
        ).arrange(RIGHT, buff=0.45)
        promise = self.txt("Observe the graphs. Deduce the equation. Then discover a different motion pattern.", 22, BOLD, color=DARK_GRAY)
        group = VGroup(kicker, main, sub, eqs, promise).arrange(DOWN, buff=0.34)
        group.move_to(ORIGIN)
        self.fit(group, 14.2, 7.1)
        self.play(FadeIn(kicker, shift=UP*0.12), run_time=RUN)
        self.play(Write(main), run_time=RUN_SLOW)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(eqs), run_time=RUN)
        self.play(FadeIn(promise), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    def uniform_motion_two_graphs(self):
        self.set_header(
            1,
            "ONE UNIFORM MOTION, TWO GRAPHS",
            "Constant velocity appears as a straight position-time graph and a horizontal velocity-time graph.",
        )

        # Physical track on the left.
        track = Line(LEFT*6.0 + DOWN*2.55, LEFT*1.0 + DOWN*2.55, color=BLACK, stroke_width=4)
        ticks = VGroup()
        for i in range(5):
            x = -5.5 + 1.05*i
            ticks.add(Line([x,-2.72,0],[x,-2.38,0], color=MID_GRAY, stroke_width=1.4))
        cart = RoundedRectangle(width=0.90, height=0.48, corner_radius=0.08,
                                stroke_color=BLACK, stroke_width=2,
                                fill_color=WHITE, fill_opacity=1).move_to(LEFT*5.45 + DOWN*2.20)
        wheel1 = Circle(radius=0.08, color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+LEFT*0.23)
        wheel2 = Circle(radius=0.08, color=BLACK).move_to(cart.get_bottom()+DOWN*0.02+RIGHT*0.23)
        cartg = VGroup(cart, wheel1, wheel2)
        track_note = self.txt("equal distance every second", 17, color=DARK_GRAY).next_to(track, DOWN, buff=0.15)

        # x-t graph top right.
        xaxes = Axes(
            x_range=[0,4.4,1], y_range=[0,7.8,1], x_length=5.0, y_length=2.85,
            axis_config={"color":BLACK,"stroke_width":2,"include_tip":False},
        ).shift(RIGHT*3.2 + UP*0.85)
        xgraph = xaxes.plot(lambda t: 1+1.5*t, x_range=[0,4], color=BLACK, stroke_width=4)
        xtitle = self.txt("POSITION vs TIME", 20, BOLD).next_to(xaxes, UP, buff=0.14)
        xlabs = VGroup(
            self.txt("t (s)", 16).next_to(xaxes.x_axis, DOWN, buff=0.10),
            self.txt("x (m)", 16).rotate(PI/2).next_to(xaxes.y_axis, LEFT, buff=0.15),
        )
        p0 = Dot(xaxes.c2p(0,1), radius=0.06, color=BLACK)
        p1 = Dot(xaxes.c2p(4,7), radius=0.06, color=BLACK)
        dtx = DashedLine(xaxes.c2p(0,1), xaxes.c2p(4,1), color=MID_GRAY)
        dxx = DashedLine(xaxes.c2p(4,1), xaxes.c2p(4,7), color=MID_GRAY)
        slope = self.formula_panel(r"\text{slope}=\frac{\Delta x}{\Delta t}=v", width=4.8, height=0.82, size=29)
        slope.next_to(xaxes, DOWN, buff=0.18)

        # v-t graph bottom right.
        vaxes = Axes(
            x_range=[0,4.4,1], y_range=[0,2.2,0.5], x_length=5.0, y_length=2.05,
            axis_config={"color":BLACK,"stroke_width":2,"include_tip":False},
        ).shift(RIGHT*3.2 + DOWN*2.05)
        vgraph = vaxes.plot(lambda t: 1.5, x_range=[0,4], color=BLACK, stroke_width=4)
        vtitle = self.txt("VELOCITY vs TIME", 20, BOLD).next_to(vaxes, UP, buff=0.14)
        vlabs = VGroup(
            self.txt("t (s)", 16).next_to(vaxes.x_axis, DOWN, buff=0.10),
            self.txt("v (m/s)", 16).rotate(PI/2).next_to(vaxes.y_axis, LEFT, buff=0.15),
        )
        vlabel = self.math(r"v=1.5\,\mathrm{m/s}", 23).next_to(vaxes.c2p(2.6,1.5), UP, buff=0.08)

        idea = self.note_panel(
            "READ BOTH GRAPHS",
            [
                "x-t: straight line -> constant slope",
                "v-t: horizontal line -> constant velocity",
                "Both describe the SAME motion.",
            ], width=5.2, title_size=22, body_size=18,
        ).move_to(LEFT*3.7 + UP*0.25)

        self.play(Create(track), FadeIn(ticks), FadeIn(cartg), FadeIn(track_note), run_time=RUN)
        self.play(Create(xaxes), FadeIn(xtitle), FadeIn(xlabs), run_time=RUN)
        self.play(Create(xgraph), FadeIn(p0), FadeIn(p1), run_time=RUN)
        self.play(Create(dtx), Create(dxx), FadeIn(slope), run_time=RUN_FAST)
        self.play(Create(vaxes), FadeIn(vtitle), FadeIn(vlabs), run_time=RUN)
        self.play(Create(vgraph), FadeIn(vlabel), run_time=RUN)
        self.play(FadeIn(idea), run_time=RUN)
        self.play(cartg.animate.shift(RIGHT*3.6), run_time=2.3, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def graph_equation_connection(self):
        self.set_header(
            3,
            "CONNECT x = x_i + vt TO THE POSITION-TIME GRAPH",
            "The initial position is the intercept and the velocity is the slope.",
        )
        axes = Axes(
            x_range=[0,4.5,1], y_range=[0,7.8,1], x_length=6.2, y_length=3.9,
            axis_config={"color":BLACK,"stroke_width":2,"include_tip":False},
        ).shift(LEFT*2.9 + DOWN*0.20)
        graph = axes.plot(lambda t: 1+1.5*t, x_range=[0,4], color=BLACK, stroke_width=4)
        title = self.txt("x(t) = x_i + vt", 24, BOLD).next_to(axes, UP, buff=0.15)
        labs = VGroup(
            self.txt("t (s)", 17).next_to(axes.x_axis, DOWN, buff=0.12),
            self.txt("x (m)", 17).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.17),
        )
        intercept = Dot(axes.c2p(0,1), radius=0.07, color=BLACK)
        ilab = self.math(r"x_i=1\,\mathrm{m}", 27).next_to(intercept, LEFT, buff=0.18)
        tri = Polygon(axes.c2p(1,2.5), axes.c2p(3,2.5), axes.c2p(3,5.5),
                      color=MID_GRAY, stroke_width=1.8, fill_opacity=0)
        slope_eq = self.formula_panel(r"v=\frac{\Delta x}{\Delta t}=\frac{3}{2}=1.5\,\mathrm{m/s}", width=5.9, height=0.95, size=30)
        slope_eq.move_to(RIGHT*4.0 + UP*1.4)
        interpretation = self.note_panel(
            "EQUATION MEANING",
            [
                "x_i -> where the line starts",
                "v -> how steep the line is",
                "t -> how long the motion continues",
                "vt -> position added after time t",
            ], width=5.5, title_size=22, body_size=19,
        ).move_to(RIGHT*4.0 + DOWN*1.2)
        quick = self.formula_panel(r"x=2+(1.2)(4)=6.8\,\mathrm{m}", width=6.0, height=0.90, size=31)
        quick.to_edge(DOWN, buff=0.28).shift(LEFT*0.6)

        self.play(Create(axes), FadeIn(title), FadeIn(labs), run_time=RUN)
        self.play(Create(graph), FadeIn(intercept), FadeIn(ilab), run_time=RUN)
        self.play(Create(tri), FadeIn(slope_eq), run_time=RUN)
        self.play(FadeIn(interpretation), FadeIn(quick), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_question_v5(self):
        self.set_header(
            4,
            "GALILEO'S QUESTION: WHAT IF EQUAL TIMES DO NOT GIVE EQUAL DISTANCES?",
            "Free fall is too fast for easy measurement. A shallow inclined plane slows the motion while keeping the changing-motion pattern visible.",
        )
        left = self.panel(6.1,4.4,fill=WHITE).shift(LEFT*3.6+DOWN*0.25)
        ltitle = self.txt("VERTICAL FALL",24,BOLD).next_to(left.get_top(),DOWN,buff=0.26)
        fall_line = Line(LEFT*4.8+UP*0.95, LEFT*4.8+DOWN*1.35, color=BLACK, stroke_width=3)
        ball1 = Circle(radius=0.17, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(fall_line.get_start())
        lnote = self.txt("motion changes too quickly",20).next_to(fall_line,RIGHT,buff=0.35)

        right = self.panel(6.1,4.4,fill=WHITE).shift(RIGHT*3.6+DOWN*0.25)
        rtitle = self.txt("GALILEO'S INCLINED PLANE",24,BOLD).next_to(right.get_top(),DOWN,buff=0.26)
        ramp = Line(RIGHT*1.75+DOWN*1.35, RIGHT*5.0+UP*0.85, color=BLACK, stroke_width=4)
        floor = Line(RIGHT*1.35+DOWN*1.35, RIGHT*5.55+DOWN*1.35, color=BLACK, stroke_width=2)
        ball2 = Circle(radius=0.17, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(ramp.get_end()+UP*0.17)
        rnote = self.txt("slower -> measurable positions",20).next_to(ramp,LEFT,buff=0.25)

        q = self.formula_panel(r"\text{At equal times, how do the traveled distances change?}", width=9.2, height=0.90, size=31)
        q.to_edge(DOWN,buff=0.35)
        self.play(FadeIn(left),FadeIn(ltitle),Create(fall_line),FadeIn(ball1),FadeIn(lnote),run_time=RUN)
        self.play(FadeIn(right),FadeIn(rtitle),Create(ramp),Create(floor),FadeIn(ball2),FadeIn(rnote),run_time=RUN)
        self.play(FadeIn(q),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_real_apparatus_v5(self):
        self.set_header(
            5,
            "GALILEO'S EXPERIMENT: INCLINED RAMP + WATER CLOCK + POSITION MARKS",
            "Release the ball from the same point, measure equal time intervals, and record position along the ramp.",
        )
        start=np.array([-5.95,-1.85,0.0]); end=np.array([1.65,1.30,0.0])
        ramp=Line(start,end,color=BLACK,stroke_width=5)
        floor=Line(np.array([-6.45,-1.85,0.0]),np.array([2.20,-1.85,0.0]),color=BLACK,stroke_width=2)
        support=Line(end,np.array([1.65,-1.85,0.0]),color=MID_GRAY,stroke_width=2)
        ref=DashedLine(start,start+RIGHT*2.0,color=LIGHT_GRAY,stroke_width=1.4)
        theta=Angle(ref,ramp,radius=0.48,color=BLACK,stroke_width=1.8)
        tlab=self.math(r"\theta",26).next_to(theta,UR,buff=0.03)
        ball=Circle(radius=0.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(end)
        release=self.txt("same release point",18,BOLD).next_to(ball,UP+LEFT,buff=0.13)

        # Cumulative positions proportional to 0,1,4,9,16.
        us=[0.0,1/16,4/16,9/16,1.0]
        points=[end+u*(start-end) for u in us]
        marks=VGroup(); labels=VGroup()
        for i,p in enumerate(points):
            marks.add(Line(p+np.array([-0.09,-0.08,0]),p+np.array([0.09,0.08,0]),color=MID_GRAY,stroke_width=1.5))
            labels.add(self.txt(f"t={i}",16,color=DARK_GRAY).move_to(p+np.array([0.17,-0.32,0])))

        cpanel=self.panel(3.0,2.8,fill=WHITE).move_to(RIGHT*5.15+DOWN*0.25)
        ctitle=self.txt("WATER CLOCK",21,BOLD).next_to(cpanel.get_top(),DOWN,buff=0.18)
        tank=RoundedRectangle(width=1.15,height=1.08,corner_radius=0.08,stroke_color=BLACK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1).move_to(cpanel.get_center()+UP*0.20)
        water=Rectangle(width=0.98,height=0.48,stroke_width=0,fill_color=LIGHT_GRAY,fill_opacity=1).move_to(tank).align_to(tank,DOWN).shift(UP*0.07)
        nozzle=Line(tank.get_bottom(),tank.get_bottom()+DOWN*0.24,color=BLACK,stroke_width=1.8)
        drops=VGroup(Dot(nozzle.get_end()+DOWN*0.11,radius=0.04,color=BLACK),Dot(nozzle.get_end()+DOWN*0.25,radius=0.03,color=MID_GRAY))
        collector=RoundedRectangle(width=1.0,height=0.4,corner_radius=0.06,stroke_color=BLACK,stroke_width=1.6,fill_color=WHITE,fill_opacity=1).next_to(drops,DOWN,buff=0.08)
        cnote=self.txt("equal water volume = equal time",15,BOLD).next_to(cpanel.get_bottom(),UP,buff=0.15)
        clock=VGroup(cpanel,ctitle,tank,water,nozzle,drops,collector,cnote)

        proc=self.note_panel("MEASUREMENT CYCLE",[
            "1. same starting point",
            "2. release - do not push",
            "3. compare equal times",
            "4. mark each position",
        ],width=4.0,title_size=21,body_size=17).move_to(RIGHT*4.85+UP*2.05)

        self.play(Create(ramp),Create(floor),Create(support),run_time=RUN)
        self.play(Create(ref),Create(theta),FadeIn(tlab),run_time=RUN_FAST)
        self.play(FadeIn(ball),FadeIn(release),FadeIn(marks),FadeIn(labels),run_time=RUN)
        self.play(FadeIn(clock),FadeIn(proc),run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(MoveAlongPath(ball,Line(end,start)),run_time=2.8,rate_func=rate_functions.ease_in_quad)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_equal_time_pattern_v5(self):
        self.set_header(
            6,
            "EQUAL TIMES, BUT THE DISTANCES GET LARGER",
            "Galileo's position pattern is 0, 1, 4, 9, 16; therefore the successive interval distances are 1, 3, 5, 7.",
        )
        baseline=Line(LEFT*5.7+DOWN*0.55,RIGHT*5.5+DOWN*0.55,color=BLACK,stroke_width=4)
        xs=[-5.15,-4.50,-2.55,0.65,5.0]
        balls=VGroup(); tlabs=VGroup()
        for i,x in enumerate(xs):
            balls.add(Circle(radius=0.15,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([x,-0.30,0]))
            tlabs.add(self.txt(f"t={i}",18).move_to([x,-0.96,0]))
        arrows=VGroup(); ilabs=VGroup(); vals=[1,3,5,7]
        for i in range(4):
            a=DoubleArrow([xs[i]+0.18,0.27,0],[xs[i+1]-0.18,0.27,0],color=MID_GRAY,stroke_width=1.7,buff=0)
            arrows.add(a); ilabs.add(self.math(fr"{vals[i]}",28).next_to(a,UP,buff=0.05))

        table=Table([["0","0"],["1","1"],["2","4"],["3","9"],["4","16"]],
                    col_labels=[self.txt("time",18,BOLD),self.txt("position",18,BOLD)],
                    include_outer_lines=True,
                    line_config={"stroke_width":1.2,"color":MID_GRAY},
                    element_to_mobject_config={"font_size":18,"color":BLACK}).scale(0.86).move_to(LEFT*5.0+UP*2.05)
        p1=self.formula_panel(r"\text{positions: }0,1,4,9,16",width=5.5,height=0.86,size=29).move_to(RIGHT*3.25+UP*2.05)
        p2=self.formula_panel(r"\text{intervals: }1,3,5,7",width=4.6,height=0.86,size=30).next_to(p1,DOWN,buff=0.18)
        compare=self.note_panel("COMPARE",[
            "uniform motion: equal times -> equal distances",
            "Galileo ramp: equal times -> increasing distances",
            "therefore x = x_i + vt cannot describe this ramp motion",
        ],width=6.3,title_size=21,body_size=18).move_to(RIGHT*3.2+DOWN*2.05)

        self.play(FadeIn(table),FadeIn(p1),FadeIn(p2),run_time=RUN)
        self.play(Create(baseline),run_time=RUN_FAST)
        for i in range(5):
            self.play(FadeIn(balls[i]),FadeIn(tlabs[i]),run_time=0.35)
            if i<4:
                self.play(Create(arrows[i]),FadeIn(ilabs[i]),run_time=0.35)
        self.play(FadeIn(compare),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def galileo_deduction_v5(self):
        self.set_header(
            7,
            "DEDUCE THE NEW PATTERN: POSITION IS PROPORTIONAL TO TIME SQUARED",
            "The recorded positions are perfect squares, so the position-time relation is quadratic rather than linear.",
        )
        squares=VGroup(
            self.math(r"0=0^2",38),self.math(r"1=1^2",38),self.math(r"4=2^2",38),
            self.math(r"9=3^2",38),self.math(r"16=4^2",38),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.20).shift(LEFT*4.7+DOWN*0.05)
        law=self.formula_panel(r"\boxed{x\propto t^2}",width=4.2,height=1.0,size=46).move_to(RIGHT*2.4+UP*1.55)
        axes=Axes(x_range=[0,4.4,1],y_range=[0,17,4],x_length=5.0,y_length=3.2,
                  axis_config={"color":BLACK,"stroke_width":2,"include_tip":False}).move_to(RIGHT*2.5+DOWN*1.35)
        curve=axes.plot(lambda t:t**2,x_range=[0,4],color=BLACK,stroke_width=4)
        title=self.txt("POSITION vs TIME becomes curved",20,BOLD).next_to(axes,UP,buff=0.14)
        contrast=self.note_panel("LINEAR vs QUADRATIC",[
            "uniform: x changes by equal amounts -> straight line",
            "Galileo: x changes by larger amounts -> curved line",
            "the experiment reveals the t² pattern",
        ],width=5.5,title_size=21,body_size=18).move_to(RIGHT*4.6+DOWN*2.55)
        self.play(Write(squares),run_time=RUN)
        self.play(FadeIn(law),run_time=RUN)
        self.play(Create(axes),FadeIn(title),Create(curve),run_time=RUN)
        self.play(FadeIn(contrast),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview_v5(self):
        self.set_header(
            8,
            "INTRODUCTION TO FALLING MOTION",
            "The inclined plane made the pattern measurable. Vertical fall shows the same qualitative t² behavior, only much faster.",
        )
        line=Line(LEFT*4.8+UP*1.65,LEFT*4.8+DOWN*1.55,color=BLACK,stroke_width=3)
        ys=[1.65,1.20,0.20,-1.55]
        balls=VGroup(); labs=VGroup()
        for i,y in enumerate(ys):
            b=Circle(radius=0.15,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to(LEFT*4.8+UP*y)
            balls.add(b); labs.add(self.txt(f"t={i}",16,color=DARK_GRAY).next_to(b,RIGHT,buff=0.18))
        observation=self.txt("equal times -> increasingly larger fall distances",20,BOLD).move_to(LEFT*1.75+UP*2.15)
        eq1=self.formula_panel(r"\boxed{y=y_i-\frac12gt^2}",width=5.5,height=1.0,size=40).move_to(RIGHT*3.55+UP*1.0)
        eq2=self.formula_panel(r"y=y_i+v_it-\frac12gt^2",width=5.8,height=1.0,size=37).next_to(eq1,DOWN,buff=0.26)
        note=self.note_panel("TODAY'S LIMIT",[
            "We are introducing the equation, not deriving g yet.",
            "The important observation is the t² term.",
            "Next lessons can explain the changing velocity formally.",
        ],width=6.1,title_size=22,body_size=18).move_to(RIGHT*3.55+DOWN*2.05)
        self.play(Create(line),FadeIn(observation),run_time=RUN)
        for b,l in zip(balls,labs): self.play(FadeIn(b),FadeIn(l),run_time=0.38)
        self.play(FadeIn(eq1),FadeIn(eq2),run_time=RUN)
        self.play(FadeIn(note),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def summary_v5(self):
        self.set_header(
            9,
            "FINAL MAP: TWO MOTION PATTERNS",
            "Use the graphs and experiment to decide whether the motion is linear in time or follows a t² pattern.",
        )
        left=self.note_panel("UNIFORM MOTION",[
            "equal times -> equal distances",
            "x-t graph: straight line",
            "v-t graph: horizontal line",
            "x = x_i + vt",
        ],width=5.2,title_size=23,body_size=19).move_to(LEFT*3.8+DOWN*0.15)
        right=self.note_panel("GALILEO / FALL PREVIEW",[
            "equal times -> increasing distances",
            "x-t graph: curved",
            "positions follow square numbers",
            "x proportional to t²",
        ],width=5.5,title_size=23,body_size=19).move_to(RIGHT*3.65+DOWN*0.15)
        center=self.formula_panel(r"\boxed{\text{straight line} \quad\text{vs}\quad t^2\text{ curve}}",width=7.2,height=1.0,size=34)
        center.to_edge(DOWN,buff=0.38)
        self.play(FadeIn(left),FadeIn(right),run_time=RUN)
        self.play(FadeIn(center),run_time=RUN)
        self.wait(4.2)


# Preview:
# manim -pql Physics9_UniformMotion_Galileo_V5.py Physics9UniformMotionGalileoV5 --disable_caching
# Final:
# manim -pqh Physics9_UniformMotion_Galileo_V5.py Physics9UniformMotionGalileoV5 --disable_caching
