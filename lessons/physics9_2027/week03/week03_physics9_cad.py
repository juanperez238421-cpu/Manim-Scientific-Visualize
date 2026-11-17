#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 • 2027 Q1 WEEK 03 • 1–5 Feb 2027.
Two independent ManimCE scenes, grounded in Physics_9_2027_P1.docx:
Class 1: Conversions and dimensional consistency.
Class 2: Significant figures and precision.
No Week 4 calipers or uncertainty mini-lab are introduced.

Reference visual system: House Extrusion CAD V6 and Physics 9 V5;
inherits institutional PNG, Tex/MathTex, fixed numbered HUD, semantic palette.
Run with ManimCE 0.20.1:
  manim -pql week03_physics9_cad.py Physics9W03_Conversions
  manim -pqh week03_physics9_cad.py Physics9W03_Conversions
  manim -pql week03_physics9_cad.py Physics9W03_SignificantFigures
  manim -pqh week03_physics9_cad.py Physics9W03_SignificantFigures
"""
from __future__ import annotations
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "week01" / "cad_canonical"))
from physics9_week01_cad import (
    CanonicalCADPhysics, DARK, MID, LIGHT, MODEL, SKETCH, POSITIVE, NEGATIVE,
    TERRAIN, SLAB
)
from manim import *


class Week03Base(CanonicalCADPhysics):
    TITLE = "PHYSICS 9 -- 2027 -- QUARTER 1 -- WEEK 03"
    HUD_TITLE = "PHYSICS 9 -- 2027 -- WEEK 03"
    HUD_TITLE_SIZE = 31
    HUD_SUBTITLE = "Unit conversion and significant figures  /  February 1--5"
    HUD_SUB_SIZE = 19
    COURSE_TITLE = "PHYSICS 9"
    SAFE_LEFT = -6.5
    SAFE_RIGHT = 6.5
    CONTENT_TOP = 2.39
    CONTENT_BOTTOM = -2.47
    READING_PAUSE = 3.0
    MICRO_PAUSE = 1.05
    FINAL_OBSERVATION_PAUSE = 3.7

    def institutional_cover(self):
        """The actual 2027 Week 03 cover; do not inherit Week 01 literal."""
        if not self.LOGO.exists():
            raise FileNotFoundError(f"Missing institutional PNG: {self.LOGO}")
        crest=ImageMobject(str(self.LOGO)).scale_to_fit_height(2.25)
        crest.to_edge(UP,buff=.34)
        institution=self.text(self.INSTITUTION,27,BOLD,DARK)
        course=self.text("PHYSICS 9",52,BOLD,DARK)
        period=self.text("2027 -- QUARTER 1 -- WEEK 03",26,BOLD,SKETCH)
        dates=self.text("FEBRUARY 1--5, 2027",25,BOLD,POSITIVE)
        main=self.text(self.COVER_TITLE,29,BOLD,DARK)
        lesson=self.text(self.LESSON_LABEL,24,BOLD,POSITIVE)
        teacher=self.text(f"Teacher: {self.TEACHER}",23,NORMAL,MID)
        top_line=Line(LEFT*5.5,RIGHT*5.5,color=SKETCH,stroke_width=2.4)
        bottom_line=Line(LEFT*4.2,RIGHT*4.2,color=LIGHT,stroke_width=1.4)
        stack=VGroup(institution,course,period,dates,top_line,main,
                     lesson,bottom_line,teacher)
        stack.arrange(DOWN,buff=.13)
        stack.next_to(crest,DOWN,buff=.08)
        if stack.get_bottom()[1] < -3.6:
            stack.scale_to_fit_height(5.2)
            stack.next_to(crest,DOWN,buff=.08)
        all_items=[crest,*stack]
        for o in all_items:
            self.add_fixed_in_frame_mobjects(o)
        self.play(FadeIn(crest),Write(institution),run_time=1.1)
        self.play(Write(course),Write(period),run_time=1.4)
        self.play(Write(dates),Create(top_line),run_time=.85)
        self.play(Write(main),Write(lesson),run_time=1.5)
        self.play(Create(bottom_line),Write(teacher),run_time=.9)
        self.wait(4.5)
        self.play(*[FadeOut(o) for o in all_items],run_time=.85)
        for o in all_items:
            self.remove_fixed_in_frame_mobjects(o)
            self.remove(o)

    def put(self, text, pos, size=36, color=DARK, bold=False, max_width=12.7):
        m = self.label(text, pos, size, color, bold)
        if m.width > max_width:
            m.scale_to_fit_width(max_width)
        if (m.get_left()[0] < self.SAFE_LEFT or m.get_right()[0] > self.SAFE_RIGHT or
            m.get_top()[1] > self.CONTENT_TOP or
            m.get_bottom()[1] < self.CONTENT_BOTTOM):
            raise ValueError(f"Week03 outside safe region: {text}")
        return m

    def eq(self, latex, pos=(0,0), size=51, color=DARK, max_width=12.6):
        m = self.math(latex, size, color)
        m.move_to([pos[0], pos[1],0])
        if m.width > max_width:
            m.scale_to_fit_width(max_width)
        if (m.get_left()[0]<self.SAFE_LEFT or m.get_right()[0]>self.SAFE_RIGHT or
            m.get_top()[1]>self.CONTENT_TOP or m.get_bottom()[1]<self.CONTENT_BOTTOM):
            raise ValueError(f"Week03 equation outside safe region: {latex}")
        self.register(m)
        return m

    def chapter(self, index, phase, heading, sub):
        self.stage_clear()
        self.set_phase(index, phase, SKETCH if index%2 else POSITIVE)
        title = self.put(heading,(0,2.06),39,DARK,True,13.0)
        subtitle = self.put(sub,(0,1.42),26,MID,False,13.0)
        self.play(Write(title),run_time=.90)
        self.play(Write(subtitle),run_time=.78)
        self.wait(1.3)
        return title,subtitle

    def appearance(self,*mobjects,time=1.1):
        self.play(*[Write(x) for x in mobjects],run_time=time)

    def draw(self,*mobjects,time=1.1):
        self.register(*mobjects)
        self.play(*[Create(x) for x in mobjects],run_time=time)

    def line(self,a,b,color=DARK,width=3.0):
        return Line([a[0],a[1],0],[b[0],b[1],0],
                    color=color,stroke_width=width)

    def close_week(self, heading, first, second):
        self.stage_clear()
        self.set_phase(99,"CHECK YOUR REASONING",POSITIVE)
        title=self.put(heading,(0,1.43),46,POSITIVE,True,13.1)
        a=self.put(first,(0,.13),34,DARK,False,13.1)
        b=self.put(second,(0,-1.02),32,SKETCH,False,13.1)
        self.appearance(title,time=1.2)
        self.appearance(a,b,time=1.8)
        self.caption("Stop, justify every step, and communicate your answer with its unit.")
        self.wait(6.5)
        self.stage_clear()
        self.footer_cleanup()


class Physics9W03_Conversions(Week03Base):
    LESSON_LABEL = "CLASS 01 -- CONVERSIONS AND DIMENSIONAL CONSISTENCY"
    COVER_TITLE = "ONE QUANTITY -- MANY EQUIVALENT UNITS"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.meaning()
        self.factors()
        self.length_conversion()
        self.mass_time()
        self.speed_conversion()
        self.error_check()
        self.practice()
        self.close_week("UNITS MUST CANCEL CORRECTLY",
                        "A conversion factor is equal to one.",
                        "Change the unit, not the physical quantity.")

    def meaning(self):
        self.chapter(1,"EQUIVALENT MEASURES","SAME LENGTH -- DIFFERENT UNITS",
                     "A numerical value changes when the chosen unit changes.")
        x0,x1=-5.5,5.6;y=-.46
        ruler=Rectangle(width=x1-x0,height=.54,color=DARK,
                        stroke_width=2.5,fill_color=MODEL,fill_opacity=1).move_to([(x0+x1)/2,y,0])
        tick_group=VGroup()
        for i in range(11):
            x=x0+(x1-x0)*i/10
            tick_group.add(self.line((x,y+.26),(x,y-.26 if i%5==0 else y-.12),DARK,1.8))
        progress=ValueTracker(0)
        bar=always_redraw(lambda: Line([x0,.50,0],
                [x0+(x1-x0)*max(.0001,progress.get_value()),.50,0],
                color=SKETCH,stroke_width=7))
        endpoint=always_redraw(lambda: Dot([x0+(x1-x0)*progress.get_value(),.50,0],
                                          radius=.16,color=POSITIVE))
        self.draw(ruler,tick_group,time=1.6)
        self.put("0 m",(-5.50,-1.06),25,MID,False,1.0)
        self.put("2 m",(5.60,-1.06),25,MID,False,1.0)
        self.add(bar,endpoint);self.register(bar,endpoint)
        self.play(progress.animate.set_value(.625),run_time=3.4,rate_func=smooth)
        e1=self.eq(r"1.25\,\mathrm{m}=125\,\mathrm{cm}",(0,-1.65),60,POSITIVE)
        self.appearance(e1,time=1.7)
        self.caption("The object does not change size: only its unit and numerical value change.")
        self.wait(3)

    def factors(self):
        self.chapter(2,"FACTOR OF ONE","A CONVERSION FACTOR EQUALS ONE",
                     "Choose the orientation that cancels the unwanted unit.")
        left=self.eq(r"1\,\mathrm{m}=100\,\mathrm{cm}",(0,.64),58,SKETCH)
        equal=self.eq(r"\frac{1\,\mathrm{m}}{100\,\mathrm{cm}}=1",
                      (-3.1,-.70),48,POSITIVE,6.2)
        inverse=self.eq(r"\frac{100\,\mathrm{cm}}{1\,\mathrm{m}}=1",
                      (3.1,-.70),48,POSITIVE,6.2)
        self.appearance(left,time=1.15)
        self.play(TransformFromCopy(left,equal),run_time=1.4)
        self.play(TransformFromCopy(left,inverse),run_time=1.4)
        self.caption("Both ratios represent the number one, but only one cancels the given unit.")
        self.wait(3.5)

    def length_conversion(self):
        self.chapter(3,"LENGTH / CANCEL UNITS","CENTIMETRES TO METRES",
                     "Start with the given value and multiply by an exact unit ratio.")
        initial=self.eq(r"125\,\mathrm{cm}",(-4.7,.53),60,SKETCH,3.9)
        mult=self.eq(r"\times\,\frac{1\,\mathrm{m}}{100\,\mathrm{cm}}",
                     (.25,.53),56,DARK,5.55)
        answer=self.eq(r"=1.25\,\mathrm{m}",(4.75,.53),56,POSITIVE,3.9)
        self.appearance(initial,time=.8)
        self.play(Write(mult),run_time=1.3)
        mark=self.put("cm above and below cancel",(0,-.85),33,POSITIVE,True,10.5)
        arrows=VGroup(
            Arrow([-4.62,-.05,0],[-1.98,-.05,0],buff=.1,color=POSITIVE,stroke_width=3),
            Arrow([1.20,-.05,0],[3.25,-.05,0],buff=.1,color=POSITIVE,stroke_width=3)
        )
        self.draw(arrows,time=1.15)
        self.appearance(mark,time=1.15)
        self.play(Write(answer),run_time=1.40)
        self.caption("125 cm × (1 m / 100 cm) = 1.25 m. Units cancel exactly.")
        self.wait(4.0)

    def mass_time(self):
        self.chapter(4,"MASS AND TIME","TWO MORE EXACT CONVERSIONS",
                     "Use base-ten mass prefixes and the sixty-second minute.")
        e1=self.eq(r"0.75\,\mathrm{kg}\times\frac{1000\,\mathrm{g}}{1\,\mathrm{kg}}",
                   (0,.50),49,SKETCH)
        a1=self.eq(r"=750\,\mathrm{g}",(0,-.42),53,POSITIVE,7)
        self.appearance(e1,time=1.35)
        self.play(Write(a1),run_time=1.1)
        self.wait(2.0)
        self.stage_clear()
        # Preserve phase; second example fills clean content region.
        e2=self.eq(r"3\,\mathrm{min}\times\frac{60\,\mathrm{s}}{1\,\mathrm{min}}",
                   (0,.74),51,SKETCH)
        a2=self.eq(r"=180\,\mathrm{s}",(0,-.24),55,POSITIVE)
        self.appearance(e2,time=1.35)
        self.play(Write(a2),run_time=1.2)
        self.caption("Kilogram and minute labels disappear when their factors are arranged correctly.")
        self.wait(3.2)

    def speed_conversion(self):
        self.chapter(5,"SPEED / TWO FACTORS","KILOMETRES PER HOUR TO METRES PER SECOND",
                     "Both the numerator and the denominator must change.")
        top=self.eq(r"72\,\frac{\mathrm{km}}{\mathrm{h}}",
                    (0,.65),62,SKETCH)
        self.appearance(top,time=1.1)
        factors=self.eq(r"\times\frac{1000\,\mathrm{m}}{1\,\mathrm{km}}\times"
                        r"\frac{1\,\mathrm{h}}{3600\,\mathrm{s}}",
                        (0,-.44),51,DARK)
        self.appearance(factors,time=2.2)
        answer=self.eq(r"=20\,\mathrm{m/s}",(0,-1.48),57,POSITIVE)
        self.appearance(answer,time=1.3)
        self.caption("km cancels with km, h cancels with h; the remaining unit is m/s.")
        self.wait(4)

    def error_check(self):
        self.chapter(6,"ERROR DETECTION","IS THIS CONVERSION CORRECT?",
                     "Reading the units reveals an incomplete calculation.")
        wrong=self.eq(r"72\,\frac{\mathrm{km}}{\mathrm{h}}\times"
                      r"\frac{1000\,\mathrm{m}}{\mathrm{km}}",
                      (0,.62),51,DARK)
        self.appearance(wrong,time=1.45)
        guess=self.eq(r"\neq 72000\,\mathrm{m/s}",
                      (0,-.29),50,NEGATIVE)
        actual=self.eq(r"=72000\,\mathrm{m/h}",
                       (0,-1.37),52,POSITIVE)
        self.appearance(guess,time=1.1)
        self.wait(2)
        self.appearance(actual,time=1.2)
        self.caption("The hour remains in the denominator: another factor is required.")
        self.wait(3.4)

    def practice(self):
        self.chapter(7,"PAIR CHECK","YOUR TURN: CONVERT EACH QUANTITY",
                     "Show the factor and cross out only matching units.")
        prompts=[
            r"3.6\,\mathrm{km}\ \rightarrow\ \mathrm{m}",
            r"90\,\mathrm{min}\ \rightarrow\ \mathrm{h}",
            r"54\,\mathrm{km/h}\ \rightarrow\ \mathrm{m/s}",
        ]
        ys=[.66,-.17,-1.02]
        for t,y in zip(prompts,ys):
            equation=self.eq(t,(-1.8,y),41,DARK,8)
            self.appearance(equation,time=.95)
        self.caption("Pause and solve the three conversions before revealing the answers.")
        self.wait(7.5)
        self.stage_clear()
        answers=[r"3.6\,\mathrm{km}=3600\,\mathrm{m}",
                 r"90\,\mathrm{min}=1.5\,\mathrm{h}",
                 r"54\,\mathrm{km/h}=15\,\mathrm{m/s}"]
        for i,mathtext in enumerate(answers):
            e=self.eq(mathtext,(0,.82-i*.94),46,POSITIVE)
            self.appearance(e,time=1.05)
            self.wait(.65)
        self.caption("Partner review: show the unit factor behind each answer.")
        self.wait(3.2)


class Physics9W03_SignificantFigures(Week03Base):
    LESSON_LABEL = "CLASS 02 -- SIGNIFICANT FIGURES AND PRECISION"
    COVER_TITLE = "MEASUREMENTS NEED HONEST PRECISION"

    def construct(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()
        self.different_reports()
        self.scale_marks()
        self.count_digits()
        self.zeros()
        self.rounding()
        self.errors()
        self.exit_ticket()
        self.close_week("REPORT ONLY JUSTIFIED DIGITS",
                        "The last reported place communicates rounding precision.",
                        "A precise number is not automatically an accurate measurement.")

    def different_reports(self):
        self.chapter(1,"ONE VALUE / THREE REPORTS",
                     "2 m, 2.0 m AND 2.00 m",
                     "The written digits communicate different reporting increments.")
        cols=[-4.18,0,4.18]
        specs=[
            (r"2\,\mathrm{m}","nearest 1 m","1 significant digit"),
            (r"2.0\,\mathrm{m}","nearest 0.1 m","2 significant digits"),
            (r"2.00\,\mathrm{m}","nearest 0.01 m","3 significant digits"),
        ]
        for i,(val,increment,digits) in enumerate(specs):
            x=cols[i]
            eq=self.eq(val,(x,.59),59,SKETCH,3.75)
            self.appearance(eq,time=1.0)
            inc=self.put(increment,(x,-.30),26,DARK,False,3.7)
            sig=self.put(digits,(x,-1.13),24,POSITIVE,True,3.7)
            self.appearance(inc,sig,time=.9)
        self.caption("These are example reported values, not proof of instrument accuracy.")
        self.wait(4)

    def scale_marks(self):
        self.chapter(2,"INSTRUMENT RESOLUTION",
                     "SMALLER DIVISIONS -- MORE DETAIL",
                     "A scale's marked increments constrain what can be read directly.")
        baselines=[.79,-.29,-1.32]
        subdivisions=[2,11,51]
        names=["1 m divisions (schematic)",
               "0.1 m divisions (schematic)",
               "0.02 m divisions (schematic)"]
        # 0–1 m drawing for direct 1 m, 0.1 m, 0.02 m tick scales.
        for j,y in enumerate(baselines):
            x0,x1=-4.60,4.65
            axis=self.line((x0,y),(x1,y),DARK,3.8)
            ticks=VGroup()
            for i in range(subdivisions[j]):
                x=x0+(x1-x0)*i/(subdivisions[j]-1)
                height=.36 if i%(max(1,(subdivisions[j]-1)//5))==0 else .20
                ticks.add(self.line((x,y+.06),(x,y-height),SKETCH,2.0))
            self.draw(axis,ticks,time=.85 if j<2 else 1.8)
            label=self.put(names[j],(0,y+.35),24,DARK,False,10.8)
            self.appearance(label,time=.75)
        self.caption("A resolution claim needs a real scale, not just many printed digits.")
        self.wait(3.1)

    def count_digits(self):
        self.chapter(3,"WHAT IS SIGNIFICANT?",
                     "COUNT THE DIGITS THAT CARRY MEANING",
                     "Nonzero digits count; some zeros also carry precision.")
        examples=[(r"4.7","2"),(r"4.70","3"),(r"4.700","4")]
        for j,(num,count) in enumerate(examples):
            y=.62-.94*j
            self.appearance(self.eq(num,(-2.7,y),56,SKETCH,4),time=.85)
            m=self.eq(r"\longrightarrow\ "+count+r"\ \mathrm{sig.\ figs.}",
                      (2.4,y),43,POSITIVE,6)
            self.appearance(m,time=.95)
        self.caption("Trailing zeros to the right of a decimal are significant.")
        self.wait(3.3)

    def zeros(self):
        self.chapter(4,"LEADING AND TRAILING ZEROS",
                     "POSITION MATTERS",
                     "Leading zeros locate the decimal point; they are not significant.")
        r1=self.eq(r"0.00450\ \longrightarrow\ 3\ \mathrm{sig.\ figs.}",
                   (0,.57),50,POSITIVE)
        r2=self.eq(r"1.020\ \longrightarrow\ 4\ \mathrm{sig.\ figs.}",
                   (0,-.40),50,SKETCH)
        r3=self.eq(r"2.00\times 10^{3}\ \longrightarrow\ 3\ \mathrm{sig.\ figs.}",
                   (0,-1.35),45,DARK)
        self.appearance(r1,time=1.25);self.wait(.6)
        self.appearance(r2,time=1.15);self.wait(.6)
        self.appearance(r3,time=1.15)
        self.caption("Scientific notation removes ambiguity about trailing zeros in large numbers.")
        self.wait(4)

    def rounding(self):
        self.chapter(5,"ROUND A MEASURED VALUE",
                     "4.736 m TO THREE SIGNIFICANT FIGURES",
                     "Keep 4, 7 and 3; inspect the next digit, 6.")
        start=self.eq(r"4.736\,\mathrm{m}",(0,.78),64,SKETCH)
        self.appearance(start,time=1.2)
        arrow=Arrow([0,.24,0],[0,-.37,0],stroke_width=5.0,
                    color=POSITIVE,buff=0)
        self.draw(arrow,time=.9)
        result=self.eq(r"4.74\,\mathrm{m}",(0,-.91),66,POSITIVE)
        self.appearance(result,time=1.45)
        desc=self.put("The 6 rounds the hundredths digit upward.",
                      (0,-1.82),30,DARK)
        self.appearance(desc,time=1.0)
        self.caption("To three significant digits: 4.736 m rounds to 4.74 m.")
        self.wait(4.0)

    def errors(self):
        self.chapter(6,"MAGNITUDE VS PRECISION",
                     "MORE DIGITS DO NOT GUARANTEE ACCURACY",
                     "A number with many digits may still be measured incorrectly.")
        target=Circle(radius=.91,color=DARK,stroke_width=2.8).move_to([-3.05,-.40,0])
        ring=Circle(radius=.46,color=LIGHT,stroke_width=2.5).move_to([-3.05,-.40,0])
        center=Dot([-3.05,-.40,0],radius=.10,color=POSITIVE)
        cluster=VGroup(*[
            Dot([-1.76+.09*np.sin(j*1.3),.22+.08*np.cos(j*2.3),0],
                radius=.075,color=NEGATIVE)
            for j in range(5)])
        self.draw(target,ring,time=1.2)
        self.play(FadeIn(center),FadeIn(cluster),run_time=.8)
        self.register(center,cluster)
        left=self.put("True value",(-3.05,-1.62),28,POSITIVE,True,5.5)
        right=self.put("Repeatable, but biased",(2.15,-.82),31,NEGATIVE,True,6.6)
        self.appearance(left,right,time=1.15)
        self.caption("Precision is repeatability or fine resolution; accuracy is closeness to truth.")
        self.wait(4)

    def exit_ticket(self):
        self.chapter(7,"DISCUSS AND CHECK",
                     "YOUR TURN: DIGITS AND ROUNDING",
                     "Think first, then justify each conclusion to your partner.")
        prompts=[
            "How many significant digits are in 0.00520?",
            "Round 6.284 m to three significant figures.",
            "Which report has finer increment: 2.0 m or 2.00 m?",
        ]
        for j,prompt in enumerate(prompts):
            m=self.put(prompt,(0,.72-j*.95),31,DARK,False,12.2)
            self.appearance(m,time=.87)
        self.caption("Students: pause to answer before comparing with the model response.")
        self.wait(7.0)
        self.stage_clear()
        solutions=[
            r"0.00520\ \longrightarrow\ 3",
            r"6.284\,\mathrm{m}\ \longrightarrow\ 6.28\,\mathrm{m}",
            r"2.00\,\mathrm{m}\ \longrightarrow\ 0.01\,\mathrm{m\ place}",
        ]
        for j,x in enumerate(solutions):
            a=self.eq(x,(0,.78-j*.98),46,POSITIVE)
            self.appearance(a,time=.9)
            self.wait(.75)
        self.caption("Peer review: explain WHY the zeros count and HOW the rounding works.")
        self.wait(3.2)
