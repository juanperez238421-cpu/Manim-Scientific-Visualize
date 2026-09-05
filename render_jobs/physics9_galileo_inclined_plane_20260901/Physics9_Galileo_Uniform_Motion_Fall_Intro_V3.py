#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · Galileo-inspired experiment · Uniform motion formula and fall preview.

Senior-QA refocus of the previous Galileo masterclass.
Pedagogical target: students experimentally build x = x_i + vt before any
formal treatment of acceleration. The final section only previews the empirical
falling-motion law and its equation; it does not develop acceleration concepts.

ManimCE 0.20.1 · 1920x1080 · JP classroom visual language.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_Galileo_Inclined_Plane_MUA_FINAL import (
    Physics9GalileoInclinedPlaneFinal,
    BLACK_TEXT,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    RUN,
    RUN_FAST,
    RUN_SLOW,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
)


class Physics9GalileoUniformMotionFallIntroV3(Physics9GalileoInclinedPlaneFinal):
    """Experiment -> constant velocity -> x=x_i+vt -> falling-motion preview."""

    def validate_lesson_data(self):
        # Uniform-motion laboratory data used in the scene.
        t = np.array([0, 1, 2, 3, 4], dtype=float)
        xi = 1.0
        v = 1.5
        x = xi + v * t
        assert np.allclose(x, [1.0, 2.5, 4.0, 5.5, 7.0])
        assert np.allclose(np.diff(x), [1.5, 1.5, 1.5, 1.5])
        assert abs((x[-1] - x[0]) / (t[-1] - t[0]) - v) < 1e-12

        # Prediction example.
        assert abs(2.0 + 1.2 * 4.0 - 6.8) < 1e-12

        # Falling-motion preview: distance ratios 1:4:9 for equal times.
        tf = np.array([0, 1, 2, 3], dtype=float)
        d = tf**2
        assert np.allclose(d, [0, 1, 4, 9])

    def construct(self):
        self.opening_refocused()
        self.question_position_prediction()
        self.uniform_motion_apparatus()
        self.equal_time_uniform_data()
        self.derive_position_equation()
        self.interpret_and_predict()
        self.position_time_graph()
        self.falling_motion_transition()
        self.falling_equation_preview()
        self.summary_refocused()

    def opening_refocused(self):
        kicker = self.txt("PHYSICS 9 | KINEMATICS", 27, BOLD)
        main = self.txt("FROM AN EXPERIMENT TO THE MOTION EQUATION", 45, BOLD)
        sub = self.txt("Measure equal times, find the pattern, and build the formula.", 27)
        target = self.formula_panel(r"\boxed{x=x_i+vt}", width=6.2, height=1.25, size=52)
        promise = self.txt("No memorizing first: the equation will come from the measurements.", 23, BOLD, color=DARK_GRAY)
        group = VGroup(kicker, main, sub, target, promise).arrange(DOWN, buff=0.34)
        group.move_to(ORIGIN)
        self.fit(group, 14.2, 7.1)

        self.play(FadeIn(kicker, shift=UP*0.12), run_time=RUN)
        self.play(Write(main), run_time=RUN_SLOW)
        self.play(FadeIn(sub), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.play(FadeIn(promise), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN)

    def question_position_prediction(self):
        self.set_header(
            1,
            "THE QUESTION: CAN WE PREDICT POSITION FROM TIME?",
            "We already know position and time. Now we want one equation that predicts where the object will be.",
        )

        track = Line(LEFT*5.7 + DOWN*1.3, RIGHT*5.7 + DOWN*1.3, color=BLACK, stroke_width=4)
        ticks = VGroup()
        for k in range(9):
            x = -5.2 + 1.3*k
            ticks.add(Line([x,-1.45,0],[x,-1.15,0],color=MID_GRAY,stroke_width=1.5))
        cart = RoundedRectangle(width=0.95, height=0.52, corner_radius=0.08,
                                stroke_color=BLACK, stroke_width=2,
                                fill_color=WHITE, fill_opacity=1).move_to(LEFT*4.6 + DOWN*0.95)
        wheel1 = Circle(radius=0.09, color=BLACK).next_to(cart, DOWN, buff=-0.01).shift(LEFT*0.28)
        wheel2 = Circle(radius=0.09, color=BLACK).next_to(cart, DOWN, buff=-0.01).shift(RIGHT*0.28)
        cartg = VGroup(cart, wheel1, wheel2)

        q = self.formula_panel(r"\text{Given }x_i,\ v,\ t\quad\Longrightarrow\quad x=?", width=9.2, height=1.1, size=38)
        q.shift(UP*1.55)
        note = self.note_panel("MEASUREMENT IDEA", [
            "Mark the cart's position at equal time intervals.",
            "If the spacing repeats, the motion has a simple rule.",
        ], width=8.6, title_size=23, body_size=21)
        note.shift(DOWN*2.6)

        self.play(FadeIn(q), run_time=RUN)
        self.play(Create(track), FadeIn(ticks), FadeIn(cartg), run_time=RUN)
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def uniform_motion_apparatus(self):
        self.set_header(
            2,
            "GALILEO-INSPIRED LAB: START THE BALL, THEN MEASURE ON A HORIZONTAL TRACK",
            "The ramp only starts the motion. We measure the ball after it reaches the horizontal section.",
        )

        ramp_top = np.array([-3.7,1.30,0.0])
        join = np.array([-3.1,-1.15,0.0])
        track_end = np.array([6.15,-1.15,0.0])
        ramp = Line(ramp_top, join, color=BLACK, stroke_width=5)
        track = Line(join, track_end, color=BLACK, stroke_width=5)
        floor = Line(LEFT*6.4+DOWN*1.65, RIGHT*6.4+DOWN*1.65, color=LIGHT_GRAY, stroke_width=1.5)

        ball = Circle(radius=0.18, stroke_color=BLACK, stroke_width=2,
                      fill_color=WHITE, fill_opacity=1).move_to(ramp_top + UP*0.20)
        label_ramp = self.txt("STARTER RAMP", 20, BOLD).move_to(LEFT*4.85 + UP*1.82)
        label_measure = self.txt("MEASUREMENT ZONE: HORIZONTAL TRACK", 20, BOLD).move_to(RIGHT*1.6 + UP*1.10)

        mark_xs = [-2.6,-1.1,0.4,1.9,3.4,4.9]
        marks = VGroup()
        labels = VGroup()
        for i, x in enumerate(mark_xs):
            marks.add(Line([x,-1.42,0],[x,-0.88,0], color=MID_GRAY, stroke_width=1.6))
            labels.add(self.txt(f"{i} s", 17, color=DARK_GRAY).move_to([x,-1.78,0]))

        stopwatch = self.panel(2.55,1.45,fill=WHITE).move_to(RIGHT*4.9 + UP*2.35)
        stopwatch_title = self.txt("EQUAL TIMES", 20, BOLD).next_to(stopwatch.get_top(), DOWN, buff=0.20)
        stopwatch_eq = self.math(r"\Delta t=1\ \mathrm{s}", 30).move_to(stopwatch).shift(DOWN*0.18)
        clock = VGroup(stopwatch, stopwatch_title, stopwatch_eq)

        reminder = self.note_panel("IMPORTANT", [
            "We do NOT use the ramp positions to build x = x_i + vt.",
            "We use only the nearly uniform horizontal-motion measurements.",
        ], width=7.0, title_size=22, body_size=18)
        reminder.move_to(LEFT*1.9 + DOWN*2.7)

        self.play(Create(ramp), Create(track), Create(floor), run_time=RUN)
        self.play(FadeIn(label_ramp), FadeIn(label_measure), FadeIn(clock), run_time=RUN)
        self.play(FadeIn(marks), FadeIn(labels), run_time=RUN_FAST)
        self.play(FadeIn(ball), FadeIn(reminder), run_time=RUN)
        self.wait(PAUSE_READ)

        self.play(MoveAlongPath(ball, Line(ramp_top+UP*0.20, join+UP*0.20)),
                  run_time=1.8, rate_func=rate_functions.ease_in_quad)
        measurement_path = Line(join+UP*0.20, np.array([4.9,-0.95,0.0]))
        self.play(MoveAlongPath(ball, measurement_path), run_time=3.2, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def equal_time_uniform_data(self):
        self.set_header(
            3,
            "THE EXPERIMENTAL PATTERN: EQUAL TIMES -> EQUAL DISTANCES",
            "On the horizontal measurement zone, the ball covers the same distance during each one-second interval.",
        )

        track = Line(LEFT*6.0+DOWN*0.45, RIGHT*6.0+DOWN*0.45, color=BLACK, stroke_width=4)
        xs = [-5.1,-2.55,0.0,2.55,5.10]
        snapshots = VGroup()
        tlabels = VGroup()
        for i, x in enumerate(xs):
            c = Circle(radius=0.16, stroke_color=BLACK, stroke_width=2,
                       fill_color=WHITE, fill_opacity=1).move_to([x,-0.23,0])
            snapshots.add(c)
            tlabels.add(self.txt(f"t = {i} s", 18).move_to([x,-0.95,0]))

        arrows = VGroup()
        dlabels = VGroup()
        for i in range(4):
            a = DoubleArrow([xs[i]+0.22,0.30,0],[xs[i+1]-0.22,0.30,0],
                            color=MID_GRAY, stroke_width=1.8, buff=0)
            arrows.add(a)
            dlabels.add(self.math(r"\Delta x=1.5\,\mathrm{m}", 22).next_to(a, UP, buff=0.08))

        table = Table(
            [["0","1.0"],["1","2.5"],["2","4.0"],["3","5.5"],["4","7.0"]],
            col_labels=[self.txt("t (s)",18,BOLD), self.txt("x (m)",18,BOLD)],
            include_outer_lines=True,
            line_config={"stroke_width":1.2,"color":MID_GRAY},
            element_to_mobject_config={"font_size":18,"color":BLACK},
        ).scale(0.85).shift(UP*2.0 + LEFT*4.8)
        pattern = self.formula_panel(r"\frac{\Delta x}{\Delta t}=\frac{1.5\,\mathrm{m}}{1\,\mathrm{s}}=1.5\,\mathrm{m/s}",
                                     width=7.2, height=1.0, size=34)
        pattern.shift(UP*2.0 + RIGHT*2.6)
        conclusion = self.note_panel("OBSERVATION", [
            "Every 1 s, position increases by 1.5 m.",
            "The ratio distance / time stays constant.",
        ], width=6.2, title_size=23, body_size=20)
        conclusion.shift(DOWN*2.7)

        self.play(FadeIn(table), FadeIn(pattern), run_time=RUN)
        self.play(Create(track), run_time=RUN_FAST)
        for i in range(5):
            self.play(FadeIn(snapshots[i]), FadeIn(tlabels[i]), run_time=0.35)
            if i < 4:
                self.play(Create(arrows[i]), FadeIn(dlabels[i]), run_time=0.35)
        self.play(FadeIn(conclusion), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def derive_position_equation(self):
        self.set_header(
            4,
            "BUILD THE EQUATION FROM THE DEFINITION OF VELOCITY",
            "Start with what the experiment measured, isolate the final position, and interpret every algebraic step.",
        )

        left = self.note_panel("MEASURED QUANTITIES", [
            "initial position: x_i",
            "final position: x",
            "elapsed time: t",
            "constant velocity: v",
        ], width=4.3, title_size=22, body_size=20)
        left.shift(LEFT*4.7 + DOWN*0.1)

        eq1 = self.math(r"v=\frac{\Delta x}{\Delta t}", 48)
        eq2 = self.math(r"v=\frac{x-x_i}{t}", 48)
        eq3 = self.math(r"vt=x-x_i", 48)
        eq4 = self.math(r"\boxed{x=x_i+vt}", 54)
        equations = VGroup(eq1,eq2,eq3,eq4).arrange(DOWN, buff=0.45).shift(RIGHT*2.0 + DOWN*0.05)

        step1 = self.txt("1. Definition", 18, BOLD, color=DARK_GRAY).next_to(eq1, LEFT, buff=0.45)
        step2 = self.txt("2. Replace Δx", 18, BOLD, color=DARK_GRAY).next_to(eq2, LEFT, buff=0.45)
        step3 = self.txt("3. Multiply by t", 18, BOLD, color=DARK_GRAY).next_to(eq3, LEFT, buff=0.45)
        step4 = self.txt("4. Isolate x", 18, BOLD, color=DARK_GRAY).next_to(eq4, LEFT, buff=0.45)
        steps = VGroup(step1,step2,step3,step4)

        note = self.txt("Here t means elapsed time measured from the chosen start instant t = 0.", 19, color=DARK_GRAY)
        note.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(left), run_time=RUN)
        self.play(Write(eq1), FadeIn(step1), run_time=RUN)
        self.play(TransformMatchingTex(eq1.copy(), eq2), FadeIn(step2), run_time=RUN)
        self.play(TransformMatchingTex(eq2.copy(), eq3), FadeIn(step3), run_time=RUN)
        self.play(TransformMatchingTex(eq3.copy(), eq4), FadeIn(step4), run_time=RUN)
        self.play(FadeIn(note), run_time=RUN_FAST)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def interpret_and_predict(self):
        self.set_header(
            5,
            "WHAT THE EQUATION SAYS: STARTING POSITION + TRAVELED DISTANCE",
            "The formula is a position statement, not just an algebra rule.",
        )

        equation = self.formula_panel(r"x=x_i+vt", width=5.6, height=1.0, size=48)
        equation.shift(UP*2.25)

        parts = VGroup(
            self.note_panel("x_i", ["where the object starts"], width=3.6, title_size=25, body_size=18),
            self.note_panel("v t", ["distance added during time t"], width=4.2, title_size=25, body_size=18),
            self.note_panel("x", ["predicted final position"], width=3.6, title_size=25, body_size=18),
        ).arrange(RIGHT, buff=0.35).shift(UP*0.65)

        values = self.formula_panel(r"x_i=2.0\,\mathrm{m},\quad v=1.2\,\mathrm{m/s},\quad t=4.0\,\mathrm{s}",
                                    width=9.6, height=0.92, size=31)
        values.shift(DOWN*0.75)
        calc = self.math(r"x=2.0+(1.2)(4.0)=\boxed{6.8\,\mathrm{m}}", 42).shift(DOWN*1.75)

        numberline = NumberLine(x_range=[0,8,1], length=10.5, include_numbers=True,
                                color=BLACK, font_size=20).shift(DOWN*3.0)
        start_dot = Dot(numberline.n2p(2.0), radius=0.08, color=BLACK)
        end_dot = Dot(numberline.n2p(6.8), radius=0.10, color=BLACK)
        start_lab = self.txt("start",17,BOLD).next_to(start_dot,UP,buff=0.08)
        end_lab = self.txt("prediction",17,BOLD).next_to(end_dot,UP,buff=0.08)
        travel = Arrow(numberline.n2p(2.0)+UP*0.35, numberline.n2p(6.8)+UP*0.35,
                       color=MID_GRAY, stroke_width=2.2, buff=0.05)

        self.play(FadeIn(equation), FadeIn(parts), run_time=RUN)
        self.play(FadeIn(values), run_time=RUN)
        self.play(Write(calc), run_time=RUN)
        self.play(Create(numberline), FadeIn(start_dot), FadeIn(start_lab), run_time=RUN)
        self.play(GrowArrow(travel), FadeIn(end_dot), FadeIn(end_lab), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def position_time_graph(self):
        self.set_header(
            6,
            "THE SAME EQUATION APPEARS AS A STRAIGHT POSITION-TIME GRAPH",
            "The intercept is x_i and the slope is v: the experiment, the algebra, and the graph tell the same story.",
        )

        axes = Axes(
            x_range=[0,5,1], y_range=[0,9,1], x_length=7.1, y_length=4.8,
            axis_config={"color":BLACK,"stroke_width":2,"include_tip":False},
        ).shift(LEFT*3.2 + DOWN*0.45)
        labels = VGroup(
            self.txt("time t (s)",18).next_to(axes.x_axis,DOWN,buff=0.18),
            self.txt("position x (m)",18).rotate(PI/2).next_to(axes.y_axis,LEFT,buff=0.20),
        )
        line = axes.plot(lambda t: 1.0 + 1.5*t, x_range=[0,5], color=BLACK, stroke_width=4)
        intercept = Dot(axes.c2p(0,1.0), radius=0.08, color=BLACK)
        ilab = self.math(r"x_i",26).next_to(intercept,LEFT,buff=0.12)

        p1 = axes.c2p(1,2.5); p3 = axes.c2p(3,5.5)
        run = DashedLine(p1, [p3[0],p1[1],0], color=MID_GRAY)
        rise = DashedLine([p3[0],p1[1],0], p3, color=MID_GRAY)
        slope = self.math(r"v=\frac{\Delta x}{\Delta t}",34).shift(RIGHT*4.1+UP*1.3)
        linear = self.formula_panel(r"x=x_i+vt", width=5.2, height=1.0, size=44).shift(RIGHT*4.1+DOWN*0.15)
        mapnote = self.note_panel("GRAPH ↔ EQUATION", [
            "vertical intercept  ->  x_i",
            "slope               ->  v",
            "straight line       ->  constant v",
        ], width=5.2, title_size=22, body_size=19)
        mapnote.shift(RIGHT*4.1+DOWN*2.0)

        self.play(Create(axes), FadeIn(labels), run_time=RUN)
        self.play(Create(line), FadeIn(intercept), FadeIn(ilab), run_time=RUN)
        self.play(Create(run), Create(rise), FadeIn(slope), run_time=RUN)
        self.play(FadeIn(linear), FadeIn(mapnote), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_motion_transition(self):
        self.set_header(
            7,
            "NEXT QUESTION: DOES x = x_i + vt DESCRIBE A FALLING OBJECT?",
            "Use equal-time snapshots again. This time the spacing between positions does not stay equal.",
        )

        left_box = self.panel(6.6,4.9,fill=WHITE).shift(LEFT*3.6+DOWN*0.35)
        lt = self.txt("UNIFORM MOTION",23,BOLD).next_to(left_box.get_top(),DOWN,buff=0.25)
        hline = Line(LEFT*6.0+DOWN*0.55, LEFT*1.2+DOWN*0.55, color=BLACK, stroke_width=3)
        hxs = [-5.7,-4.55,-3.4,-2.25,-1.1]
        hdots = VGroup(*[Dot([x,-0.37,0],radius=0.075,color=BLACK) for x in hxs])
        htext = self.txt("equal time -> equal spacing",19,BOLD).next_to(hline,DOWN,buff=0.55)

        right_box = self.panel(6.6,4.9,fill=WHITE).shift(RIGHT*3.6+DOWN*0.35)
        rt = self.txt("FALLING MOTION",23,BOLD).next_to(right_box.get_top(),DOWN,buff=0.25)
        fall_line = Line(RIGHT*3.6+UP*1.25, RIGHT*3.6+DOWN*2.05, color=LIGHT_GRAY, stroke_width=2)
        ys = [1.25,0.90,-0.05,-1.65]
        fdots = VGroup(*[Dot([3.6,y,0],radius=0.08,color=BLACK) for y in ys])
        flabels = VGroup(*[self.txt(f"t={i}s",16).next_to(fdots[i],RIGHT,buff=0.12) for i in range(4)])
        ftext = self.txt("equal time -> growing spacing",19,BOLD).next_to(fall_line,DOWN,buff=0.28)

        question = self.formula_panel(r"\text{One constant }v\text{ cannot match all falling intervals.}",
                                      width=9.6,height=0.9,size=30)
        question.to_edge(DOWN,buff=0.25)

        self.play(FadeIn(left_box), FadeIn(right_box), FadeIn(lt), FadeIn(rt), run_time=RUN)
        self.play(Create(hline), FadeIn(hdots), FadeIn(htext), run_time=RUN)
        self.play(Create(fall_line), run_time=RUN_FAST)
        for i in range(4):
            self.play(FadeIn(fdots[i]), FadeIn(flabels[i]), run_time=0.35)
        self.play(FadeIn(ftext), FadeIn(question), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def falling_equation_preview(self):
        self.set_header(
            8,
            "INTRODUCTION TO THE FALLING-MOTION EQUATION",
            "Galileo's equal-time measurements suggest a square-time pattern. We only preview the equation today.",
        )

        table = Table(
            [["0","0"],["1","1"],["2","4"],["3","9"]],
            col_labels=[self.txt("t",18,BOLD), self.txt("relative fall distance",18,BOLD)],
            include_outer_lines=True,
            line_config={"stroke_width":1.2,"color":MID_GRAY},
            element_to_mobject_config={"font_size":19,"color":BLACK},
        ).scale(0.92).shift(LEFT*4.6+UP*0.55)

        law = self.formula_panel(r"d\propto t^2", width=4.3,height=1.0,size=46).shift(LEFT*4.6+DOWN*2.0)
        axis_note = self.note_panel("CHOOSE +y UPWARD", [
            "release from height y_i",
            "the object moves downward as time passes",
        ], width=5.3,title_size=22,body_size=19).shift(RIGHT*3.6+UP*1.65)
        fall_eq = self.formula_panel(r"\boxed{y=y_i-\frac12 g t^2}", width=6.5,height=1.2,size=48).shift(RIGHT*3.6+DOWN*0.10)
        general_preview = self.formula_panel(r"y=y_i+v_i t-\frac12 g t^2", width=6.5,height=1.0,size=39).shift(RIGHT*3.6+DOWN*1.45)
        note = self.txt("Preview only: g represents Earth's gravitational effect near the surface; its physical interpretation comes next.",
                        18,color=DARK_GRAY)
        self.fit(note, 13.5, 0.5)
        note.to_edge(DOWN,buff=0.32)

        self.play(FadeIn(table), run_time=RUN)
        self.play(FadeIn(law), run_time=RUN)
        self.play(FadeIn(axis_note), run_time=RUN)
        self.play(FadeIn(fall_eq), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(general_preview), FadeIn(note), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def summary_refocused(self):
        self.set_header(
            9,
            "SUMMARY: OBSERVE -> DEFINE VELOCITY -> BUILD THE POSITION EQUATION",
            "Today's target is uniform motion. Falling motion is only the bridge to the next lesson.",
        )

        flow = VGroup(
            self.note_panel("1  OBSERVE", ["equal times -> equal distances"], width=3.2,title_size=21,body_size=17),
            self.note_panel("2  DEFINE", [r"v = Δx / Δt"], width=3.2,title_size=21,body_size=17),
            self.note_panel("3  REWRITE", [r"v = (x - x_i) / t"], width=3.2,title_size=21,body_size=17),
            self.note_panel("4  SOLVE", [r"x = x_i + vt"], width=3.2,title_size=21,body_size=17),
        ).arrange(RIGHT,buff=0.30).shift(UP*1.5)

        target = self.formula_panel(r"\boxed{x=x_i+vt}", width=6.0,height=1.2,size=54).shift(DOWN*0.20)
        next_box = self.note_panel("NEXT CLASS", [
            "Why do falling positions spread farther apart?",
            "What does the symbol g tell us physically?",
            "How does the square-time law change our model?",
        ], width=8.7,title_size=24,body_size=20).shift(DOWN*2.25)

        self.play(FadeIn(flow), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.play(FadeIn(next_box), run_time=RUN)
        self.wait(4.0)


# Preview:
# manim -pql Physics9_Galileo_Uniform_Motion_Fall_Intro_V3.py Physics9GalileoUniformMotionFallIntroV3 --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Uniform_Motion_Fall_Intro_V3.py Physics9GalileoUniformMotionFallIntroV3 --disable_caching
