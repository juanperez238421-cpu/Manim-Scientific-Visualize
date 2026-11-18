#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9, 2027 Q1 — Weeks 02 and 04, four complete CAD-format lessons.

Planner: Physics_9_2027_P1.docx. Institutional theme:
House Extrusion CAD V6 via the validated Week03Base / CanonicalCADPhysics.
Week 02 (January 25–29): SI and orders of magnitude; scientific notation.
Week 04 (February 8–12): vernier and micrometer; repeated measurement lab.

All readings in these four videos are explicitly illustrative; no learner data.
ManimCE 0.20.1. Render -pql before -pqh, FPS 30, Full-HD.
"""
from __future__ import annotations
import sys
import numpy as np
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"week03"))
from week03_physics9_cad import Week03Base, DARK, MID, LIGHT, MODEL, \
    SKETCH, POSITIVE, NEGATIVE, TERRAIN, SLAB
from manim import WHITE, BOLD, NORMAL


class CadIntroBase(Week03Base):
    """Common, actually reused institutional PNG and safe CAD teaching layout."""
    WEEK = 2
    DATES = "JANUARY 25--29, 2027"
    HUD_TITLE_SIZE = 29
    HUD_SUB_SIZE = 20
    MICRO_PAUSE = 0.82
    READING_PAUSE = 2.9
    FINAL_OBSERVATION_PAUSE = 3.5

    def institutional_cover(self):
        if not self.LOGO.exists():
            raise FileNotFoundError(f"Original IJR logo PNG missing: {self.LOGO}")
        crest=ImageMobject(str(self.LOGO)).scale_to_fit_height(2.22)
        crest.to_edge(UP,buff=.34)
        institution=self.text(self.INSTITUTION,27,BOLD,DARK)
        course=self.text("PHYSICS 9",53,BOLD,DARK)
        week=self.text(f"2027 -- QUARTER 1 -- WEEK {self.WEEK:02d}",26,BOLD,SKETCH)
        dates=self.text(self.DATES,25,BOLD,POSITIVE)
        title=self.text(self.COVER_TITLE,30,BOLD,DARK)
        lesson=self.text(self.LESSON_LABEL,23,BOLD,POSITIVE)
        teacher=self.text(f"Teacher: {self.TEACHER}",23,NORMAL,MID)
        topline=Line(LEFT*5.50,RIGHT*5.50,stroke_width=2.2,color=SKETCH)
        underline=Line(LEFT*4.20,RIGHT*4.20,stroke_width=1.4,color=LIGHT)
        stack=VGroup(institution,course,week,dates,topline,title,lesson,underline,teacher)
        stack.arrange(DOWN,buff=.135).next_to(crest,DOWN,buff=.09)
        if stack.get_bottom()[1]<-3.60:
            stack.scale_to_fit_height(5.24)
            stack.next_to(crest,DOWN,buff=.07)
        items=[crest,*stack]
        for m in items:self.add_fixed_in_frame_mobjects(m)
        self.play(FadeIn(crest),Write(institution),run_time=1.25)
        self.play(Write(course),Write(week),run_time=1.38)
        self.play(Write(dates),Create(topline),run_time=1.06)
        self.play(Write(title),Write(lesson),run_time=1.38)
        self.play(Create(underline),Write(teacher),run_time=.88)
        self.wait(4.2)
        self.play(*[FadeOut(o) for o in items],run_time=.90)
        for m in items:
            self.remove_fixed_in_frame_mobjects(m)
            self.remove(m)

    def start(self):
        self.institutional_cover()
        self.ph=self.fixed_hud()

    def textline(self, content, y, color=DARK, size=35, bold=False, width=12.0, x=0):
        result=self.put(content,(x,y),size,color,bold,width)
        self.play(Write(result),run_time=1.0)
        return result

    def formula(self, expression, y, color=SKETCH, size=55, width=12.2, x=0):
        result=self.eq(expression,(x,y),size,color,width)
        self.play(Write(result),run_time=1.25)
        return result

    def vector_glyph(self,x,y,kind):
        if kind=="length":
            return DoubleArrow([x-.65,y,0],[x+.65,y,0],buff=0,
                               stroke_width=4,color=SKETCH)
        if kind=="mass":
            return RoundedRectangle(width=1.12,height=.84,corner_radius=.10,
                            stroke_color=SKETCH,stroke_width=3,
                            fill_color=MODEL,fill_opacity=1).move_to([x,y,0])
        if kind=="time":
            return Circle(radius=.49,stroke_color=SKETCH,stroke_width=3).move_to([x,y,0])
        if kind=="temperature":
            return VGroup(Line([x,y+.52,0],[x,y-.25,0],color=SKETCH,
                              stroke_width=10),Dot([x,y-.48,0],radius=.19,color=NEGATIVE))
        return Dot([x,y,0],radius=.20,color=SKETCH)


class Physics9W02_SI_Units(CadIntroBase):
    WEEK = 2
    DATES = "JANUARY 25--29, 2027"
    HUD_TITLE = "PHYSICS 9 -- 2027 -- WEEK 02"
    HUD_SUBTITLE = "SI quantities and orders of magnitude  /  January 25--29"
    COVER_TITLE = "UNITS GIVE NUMBERS PHYSICAL MEANING"
    LESSON_LABEL = "CLASS 01 -- SI UNITS AND SIZE SCALES"

    def construct(self):
        self.start()
        self.why_standards()
        self.base_units()
        self.derived_units()
        self.logarithmic_scale()
        self.class_check()
        self.close_week("CONSISTENT UNITS MAKE SCIENCE REPRODUCIBLE",
                        "Base quantities are measured with agreed standard units.",
                        "Derived units combine fundamental dimensions.")

    def why_standards(self):
        self.chapter(1,"COMPARE / OBSERVE","CAN WE COMPARE TWO MEASUREMENTS?",
                     "Numbers are meaningful when the same unit is understood.")
        left=Rectangle(width=4.5,height=.61,stroke_width=3,color=DARK,
                       fill_color=MODEL,fill_opacity=1).move_to([-2.5,-.38,0])
        right=Rectangle(width=4.5,height=.61,stroke_width=3,color=DARK,
                        fill_color=TERRAIN,fill_opacity=1).move_to([2.5,-.38,0])
        left_text=self.put("2.0",( -2.5,.58),60,SKETCH,True,3.2)
        right_text=self.put("200", (2.5,.58),60,POSITIVE,True,3.2)
        self.draw(left,right,time=1.45)
        self.appearance(left_text,right_text,time=.90)
        self.wait(1.6)
        left_units=self.put("m",(-2.5,-1.3),50,DARK,True,2)
        right_units=self.put("cm",(2.5,-1.3),50,DARK,True,2)
        self.appearance(left_units,right_units,time=1.2)
        self.formula(r"2.0\,\mathrm{m}=200\,\mathrm{cm}",-2.08,POSITIVE,44)
        self.caption("Without a unit, numerical comparisons may be misleading.")
        self.wait(3.3)

    def base_units(self):
        self.chapter(2,"BASE QUANTITIES","THE SI: FOUR EVERYDAY EXAMPLES",
                     "Length, mass, time and thermodynamic temperature.")
        columns=[-4.85,-1.65,1.65,4.85]
        entries=[("LENGTH","m","length"),("MASS","kg","mass"),
                 ("TIME","s","time"),("TEMPERATURE","K","temperature")]
        for idx,(name,unit,kind) in enumerate(entries):
            x=columns[idx]
            glyph=self.vector_glyph(x,-.14,kind)
            self.draw(glyph,time=.55)
            label=self.put(name,(x,.82),27,DARK,True,2.8)
            unit_text=self.put(unit,(x,-1.06),44,POSITIVE,True,2.65)
            self.appearance(label,unit_text,time=.82)
            self.wait(.48)
        self.caption("These are four of the seven SI base units, not the complete list.")
        self.wait(4.0)

    def derived_units(self):
        self.chapter(3,"DERIVED QUANTITIES","SPEED IS DISTANCE DIVIDED BY TIME",
                     "Combining metres and seconds creates metres per second.")
        axis=self.line((-5.75,-.65),(5.75,-.65),DARK,3.6)
        tick_start=self.line((-5.50,-.88),(-5.50,-.42),SKETCH,3)
        tick_end=self.line((4.9,-.88),(4.9,-.42),SKETCH,3)
        time=ValueTracker(0)
        x0=-5.5; distance=10.4
        runner=always_redraw(lambda: VGroup(
            RoundedRectangle(width=1.15,height=.56,corner_radius=.12,
                        fill_color=MODEL,fill_opacity=1,stroke_color=DARK,
                        stroke_width=2.5)
                .move_to([x0+distance*time.get_value()/3,-.26,0]),
            Circle(radius=.14,color=DARK,fill_color=DARK,fill_opacity=1)
                .move_to([x0+distance*time.get_value()/3-.32,-.63,0]),
            Circle(radius=.14,color=DARK,fill_color=DARK,fill_opacity=1)
                .move_to([x0+distance*time.get_value()/3+.32,-.63,0])))
        self.draw(axis,tick_start,tick_end,time=1)
        self.add(runner);self.register(runner)
        self.play(time.animate.set_value(3),run_time=4.3,rate_func=linear)
        self.formula(r"v=\frac{\Delta x}{\Delta t}=\frac{6\,\mathrm{m}}{3\,\mathrm{s}}"
                     r"=2\,\mathrm{m/s}",-1.48,POSITIVE,49)
        self.caption("A derived unit can be checked from the formula itself.")
        self.wait(3.4)

    def logarithmic_scale(self):
        self.chapter(4,"POWERS OF TEN","COMPARE SCALES WITHOUT HUGE NUMBERS",
                     "Use a logarithmic scale: each equal step changes by 1000.")
        exponents=[-9,-6,-3,0,3,6]
        labels=["nm","um","mm","m","km","Mm"]
        for i,(exp,word) in enumerate(zip(exponents,labels)):
            x=-5.55+i*2.23
            dot=Dot([x,-.23,0],radius=.14,color=SKETCH if exp!=0 else POSITIVE)
            axis=self.line((x,-.23),(x,-.48),DARK,2)
            t=self.eq(r"10^{%d}\,\mathrm{m}"%exp,(x,-1.16),30,DARK,2.16)
            wordtext=self.put(word,(x,.55),28,POSITIVE if exp==0 else SKETCH,True,2.05)
            self.draw(dot,axis,time=.45)
            self.play(Write(t),Write(wordtext),run_time=.7)
            self.wait(.30)
        baseline=self.line((-5.55,-.23),(5.60,-.23),MID,2.6)
        self.draw(baseline,time=1)
        self.caption("nm, um, mm, m, km and Mm are successively 1000 times apart.")
        self.wait(4.0)

    def class_check(self):
        self.chapter(5,"PAIR / QUICK CHECK","MATCH QUANTITIES TO SI UNITS",
                     "Explain why the chosen unit has that physical dimension.")
        items=[("Distance between desks","m"),
               ("Mass of a schoolbag","kg"),
               ("Duration of a run","s"),
               ("Speed of a moving cart","m/s")]
        for i,(label,unit) in enumerate(items):
            y=.82-i*.76
            a=self.put(label,(-2.45,y),30,DARK,False,7.0)
            self.appearance(a,time=.69)
            self.wait(.75)
            b=self.put(unit,(4.5,y),35,POSITIVE,True,2.5)
            self.appearance(b,time=.64)
        self.caption("A speed unit is derived from length divided by time.")
        self.wait(3.3)


class Physics9W02_ScientificNotation(CadIntroBase):
    WEEK = 2
    DATES = "JANUARY 25--29, 2027"
    HUD_TITLE = "PHYSICS 9 -- 2027 -- WEEK 02"
    HUD_SUBTITLE = "Writing very large and very small physical values"
    COVER_TITLE = "SCIENTIFIC NOTATION CONNECTS PHYSICAL SCALES"
    LESSON_LABEL = "CLASS 02 -- SCIENTIFIC NOTATION"

    def construct(self):
        self.start()
        self.form_definition()
        self.large_number()
        self.small_number()
        self.compare_powers()
        self.negative_sign()
        self.practice()
        self.close_week("READ THE EXPONENT BEFORE COMPARING",
                        "Move the decimal point and track its power of ten.",
                        "A valid coefficient has magnitude from 1 to less than 10.")

    def form_definition(self):
        self.chapter(1,"VALID STRUCTURE","ONE COEFFICIENT TIMES A POWER OF TEN",
                     "For any nonzero number: coefficient times ten to integer power.")
        self.formula(r"N=a\times10^n",.49,SKETCH,73)
        self.formula(r"1\leq |a|<10,\quad n\in\mathbb{Z}",-.53,POSITIVE,52)
        self.textline("n counts decimal places, not significant digits.",-1.64,DARK,29)
        self.caption("One nonzero number has a unique normalized scientific notation.")
        self.wait(3.2)

    def large_number(self):
        self.chapter(2,"POSITIVE EXPONENT","A LARGE DISTANCE",
                     "The decimal point moves left while the exponent grows.")
        self.formula(r"4\,500\,000\,\mathrm{m}",.67,DARK,63)
        t=ValueTracker(0)
        arrow=always_redraw(lambda: Arrow(
            [-4.6,-.38,0],[-4.6+max(.02,8.1*t.get_value()),-.38,0],
            buff=0,color=SKETCH,stroke_width=5))
        self.add(arrow);self.register(arrow)
        self.play(t.animate.set_value(1),run_time=2.1,rate_func=smooth)
        self.formula(r"4.5\times10^{6}\,\mathrm{m}",-1.36,POSITIVE,61)
        self.caption("Move the decimal six places left: the positive exponent is +6.")
        self.wait(3.5)

    def small_number(self):
        self.chapter(3,"NEGATIVE EXPONENT","A VERY SMALL LENGTH",
                     "Moving the decimal point right creates a negative exponent.")
        self.formula(r"0.0000032\,\mathrm{m}",.66,DARK,62)
        t=ValueTracker(0)
        pointer=always_redraw(lambda: Arrow(
            [3.70,-.32,0],[3.70-max(.02,7.4*t.get_value()),-.32,0],
            color=SKETCH,buff=0,stroke_width=5))
        self.add(pointer);self.register(pointer)
        self.play(t.animate.set_value(1),run_time=2.15,rate_func=smooth)
        self.formula(r"3.2\times10^{-6}\,\mathrm{m}",-1.35,POSITIVE,60)
        self.caption("Move six places right to obtain 3.2, so the exponent is -6.")
        self.wait(3.5)

    def compare_powers(self):
        self.chapter(4,"COMPARE / FACTOR OF 100",
                     "IDENTICAL COEFFICIENTS -- DIFFERENT POWERS",
                     "Increasing the exponent by two multiplies a quantity by 100.")
        self.formula(r"A=2\times10^3\,\mathrm{m}",.72,SKETCH,51)
        self.formula(r"B=2\times10^5\,\mathrm{m}",-.13,DARK,51)
        self.formula(r"\frac{B}{A}=\frac{2\times10^5}{2\times10^3}=10^2=100",
                     -1.31,POSITIVE,49)
        self.caption("On the same dimension and unit, ratio comparisons are meaningful.")
        self.wait(3.8)

    def negative_sign(self):
        self.chapter(5,"COMMON MISTAKE","THE EXPONENT IS NOT THE SIGN OF THE VALUE",
                     "A negative exponent can still represent a positive distance.")
        self.formula(r"3.2\times10^{-6}\,\mathrm{m}>0",.43,POSITIVE,62)
        self.formula(r"10^{-6}=\frac{1}{1\,000\,000}",-.65,SKETCH,56)
        self.caption("The negative exponent means a fraction of one, not a negative length.")
        self.wait(4)

    def practice(self):
        self.chapter(6,"PAUSE / SOLVE","PRACTISE BOTH DIRECTIONS",
                     "Try each conversion before its answer is shown.")
        tasks=[
            (r"6.2\times10^4",r"=62\,000"),
            (r"0.00081",r"=8.1\times10^{-4}"),
            (r"9.4\times10^3",r"=9400"),
        ]
        for idx,(left,right) in enumerate(tasks):
            y=.78-idx*.95
            e=self.eq(left,(-2.55,y),48,SKETCH,5.4)
            self.appearance(e,time=.8)
            self.wait(2.2)
            ans=self.eq(right,(2.7,y),47,POSITIVE,5.25)
            self.appearance(ans,time=.88)
        self.caption("Check that the coefficient lies between 1 and 10 in magnitude.")
        self.wait(4.0)


class Physics9W04_Instruments(CadIntroBase):
    WEEK = 4
    DATES = "FEBRUARY 8--12, 2027"
    HUD_TITLE = "PHYSICS 9 -- 2027 -- WEEK 04"
    HUD_SUBTITLE = "Vernier caliper and micrometer  /  February 8--12"
    COVER_TITLE = "PRECISION INSTRUMENTS: HOW TO READ THEM"
    LESSON_LABEL = "CLASS 01 -- VERNIER CALIPER AND MICROMETER"

    def construct(self):
        self.start()
        self.components()
        self.vernier_zero_and_reading()
        self.micrometer_components()
        self.micrometer_reading()
        self.choice()
        self.practice()
        self.close_week("READ THE SCALE BEFORE WRITING THE RESULT",
                        "First zero-check; then identify main and fine-scale readings.",
                        "Always include the unit and actual instrument resolution.")

    def components(self):
        self.chapter(1,"CALIPER / PARTS","IDENTIFY THE FIXED AND MOVING ELEMENTS",
                     "Main scale, fixed jaw, sliding jaw, vernier and zero mark.")
        beam=Rectangle(width=10.8,height=.46,color=DARK,stroke_width=2.7,
                       fill_color=MODEL,fill_opacity=1).move_to([0,.01,0])
        fixed=Rectangle(width=.25,height=1.22,color=SKETCH,stroke_width=2.2,
                        fill_color=SLAB,fill_opacity=1).move_to([-5.2,-.38,0])
        tracker=ValueTracker(-3.30)
        slide=always_redraw(lambda: VGroup(
            Rectangle(width=1.58,height=.65,color=SKETCH,stroke_width=2.7,
                      fill_color=TERRAIN,fill_opacity=.98)
                .move_to([tracker.get_value(),-.26,0]),
            Rectangle(width=.25,height=1.25,color=SKETCH,stroke_width=2.7,
                      fill_color=SLAB,fill_opacity=1)
                .move_to([tracker.get_value()-.70,-.80,0])))
        self.draw(beam,fixed,time=1.25)
        self.add(slide);self.register(slide)
        self.play(tracker.animate.set_value(1.70),run_time=3.45,rate_func=smooth)
        self.textline("Moving jaw", -1.68, SKETCH,34,True)
        self.caption("This is a simplified dimensional drawing, not a photograph.")
        self.wait(3.0)

    def vernier_zero_and_reading(self):
        self.chapter(2,"CALIPER / VERNIER","MAIN SCALE PLUS VERNIER READING",
                     "Example: a 0.1 mm vernier with ten divisions spanning 9 mm.")
        x0=-5.36; dx=.232; y=.23
        main=self.line((x0,y),(x0+45*dx,y),DARK,3.8)
        marks=VGroup(*[
            self.line((x0+i*dx,y+.10),
                      (x0+i*dx,y-(.42 if i%5==0 else .24)),
                      DARK,1.85) for i in range(46)])
        self.draw(main,marks,time=2)
        for j in (0,10,20,30,40):
            x=x0+j*dx
            lab=self.put(str(j),(x,.80),26,DARK,False,1.25)
            self.appearance(lab,time=.36)
        sliderpos=ValueTracker(0)
        def moving_marks():
            origin=x0+sliderpos.get_value()*dx
            return VGroup(*[
                Line([origin+j*.9*dx,-.73,0],
                     [origin+j*.9*dx,-1.11 if j%5==0 else -1.00,0],
                     color=SKETCH,stroke_width=2.5)
                for j in range(11)])
        vernier=always_redraw(moving_marks)
        zero=always_redraw(lambda: Dot(
            [x0+sliderpos.get_value()*dx,-.73,0],radius=.12,color=POSITIVE))
        self.add(vernier,zero)
        self.register(vernier,zero)
        self.wait(.85)
        self.caption("Zero check: with closed jaws, the two zero marks must coincide.")
        self.wait(2.4)
        self.play(sliderpos.animate.set_value(24.6),run_time=3.8,rate_func=smooth)
        # 24.6 + 6*(0.9) = 30 mm, so vernier mark 6 aligns with main mark 30.
        x30=x0+30*dx
        alignment=DashedLine([x30,.24,0],[x30,-1.17,0],
                             dash_length=.12,color=POSITIVE)
        self.draw(alignment,time=.82)
        self.formula(r"24\,\mathrm{mm}+6(0.1\,\mathrm{mm})"
                     r"=24.6\,\mathrm{mm}",-1.93,POSITIVE,50)
        self.caption("Read 24 mm on the main scale; matching vernier line 6 adds 0.6 mm.")
        self.wait(4.4)

    def micrometer_components(self):
        self.chapter(3,"MICROMETER / PARTS","A ROTATING THIMBLE MOVES THE SPINDLE",
                     "Sleeve scale, thimble, anvil and zero check.")
        sleeve=RoundedRectangle(width=5.60,height=1.03,corner_radius=.12,
                                color=DARK,stroke_width=2.9,
                                fill_color=MODEL,fill_opacity=1).move_to([-1.9,-.25,0])
        body=RoundedRectangle(width=2.60,height=1.72,corner_radius=.16,
                             color=SKETCH,stroke_width=3,
                             fill_color=TERRAIN,fill_opacity=1).move_to([2.36,-.25,0])
        spindle=self.line((-4.67,-.25),(-5.42,-.25),SKETCH,8)
        thimble_line=VGroup(*[
            self.line((1.2+i*.15,-.95),(1.2+i*.15,-.65),DARK,1.6)
            for i in range(16)])
        self.draw(sleeve,body,spindle,thimble_line,time=2.3)
        points=[(-3.7,-1.49,"SLEEVE"),(2.3,-1.49,"THIMBLE"),(-5.1,.80,"ANVIL / SPINDLE")]
        for x,y,word in points:
            self.textline(word,y,SKETCH,26,False,5.6,x)
        self.caption("A real micrometer must be checked at zero before taking a measurement.")
        self.wait(4.2)

    def micrometer_reading(self):
        self.chapter(4,"MICROMETER / SCALE","SLEEVE READING + THIMBLE READING",
                     "Illustrative 0.01 mm-resolution instrument, pitch 0.5 mm per turn.")
        self.formula(r"\mathrm{sleeve}=7.50\,\mathrm{mm}",.72,SKETCH,52)
        dial=Circle(radius=.92,color=DARK,stroke_width=3.0).move_to([0,-.55,0])
        ticks=VGroup()
        centre=np.array([0,-.55,0])
        for n in range(50):
            angle=TAU*n/50
            p=centre+.77*np.array([np.sin(angle),np.cos(angle),0])
            q=centre+.91*np.array([np.sin(angle),np.cos(angle),0])
            ticks.add(Line(p,q,color=POSITIVE if n==28 else DARK,
                           stroke_width=3.6 if n==28 else 1.4))
        self.draw(dial,ticks,time=2.5)
        needle=Arrow(centre,
                centre+.64*np.array([np.sin(TAU*28/50),np.cos(TAU*28/50),0]),
                color=POSITIVE,stroke_width=4.2,buff=0)
        self.draw(needle,time=.82)
        add=self.eq(r"28(0.01\,\mathrm{mm})=0.28\,\mathrm{mm}",(3.15,-1.33),42,DARK,6)
        self.appearance(add,time=1.3)
        result=self.eq(r"7.50+0.28=7.78\,\mathrm{mm}",(-2.55,-2.16),44,POSITIVE,7.9)
        self.appearance(result,time=1.3)
        self.caption("Schematic thimble with index 28: an illustrative reading of 7.78 mm.")
        self.wait(3.8)

    def choice(self):
        self.chapter(5,"FIT THE TOOL TO THE OBJECT",
                     "CHOOSE RANGE AND RESOLUTION",
                     "These are the example specifications of the instruments shown.")
        cal=self.put("VERNIER CALIPER",(-3.36,.63),38,SKETCH,True,6.2)
        mic=self.put("MICROMETER",(3.39,.63),38,POSITIVE,True,6.2)
        self.appearance(cal,mic,time=1.2)
        self.formula(r"0.1\,\mathrm{mm}",-.34,SKETCH,53,5.2,-3.36)
        self.formula(r"0.01\,\mathrm{mm}",-.34,POSITIVE,53,5.2,3.36)
        self.textline("Outer / inner dimensions",-1.3,DARK,27,False,6.1,-3.36)
        self.textline("Thin wire or small thickness",-1.3,DARK,27,False,6.1,3.36)
        self.caption("A finer division does not guarantee greater accuracy by itself.")
        self.wait(4.0)

    def practice(self):
        self.chapter(6,"PRACTICE / READINGS","CALCULATE THE TWO FINAL RESULTS",
                     "Give students time to add the main scale and fractional reading.")
        tasks=[r"12\,\mathrm{mm}+3(0.1\,\mathrm{mm})",
               r"5.50\,\mathrm{mm}+47(0.01\,\mathrm{mm})"]
        for i,expr in enumerate(tasks):
            y=.72-i*1.02
            e=self.eq(expr,(0,y),51,SKETCH)
            self.appearance(e,time=1.1)
        self.caption("Pause: calculate, label the unit, and compare with your partner.")
        self.wait(6.1)
        self.stage_clear()
        self.formula(r"12.3\,\mathrm{mm}",.58,POSITIVE,57)
        self.formula(r"5.97\,\mathrm{mm}",-.53,POSITIVE,57)
        self.caption("Answers are schematic examples, not measurements from a live instrument.")
        self.wait(3.3)


class Physics9W04_UncertaintyLab(CadIntroBase):
    WEEK = 4
    DATES = "FEBRUARY 8--12, 2027"
    HUD_TITLE = "PHYSICS 9 -- 2027 -- WEEK 04"
    HUD_SUBTITLE = "Mini-lab, repeated measurements, range and instrument choice"
    COVER_TITLE = "REPEAT MEASUREMENTS -- REPORT THE EVIDENCE"
    LESSON_LABEL = "CLASS 02 -- MEASUREMENT AND UNCERTAINTY"

    def construct(self):
        self.start()
        self.protocol()
        self.two_objects()
        self.readings_table()
        self.range_calculation()
        self.data_plot()
        self.uncertainty()
        self.practice()
        self.close_week("REPORT WHAT YOUR DATA SUPPORT",
                        "Record repeated values with the correct unit and resolution.",
                        "The observed range alone is not a complete uncertainty budget.")

    def protocol(self):
        self.chapter(1,"LAB PROTOCOL / TWO OBJECTS",
                     "OBSERVE, ZERO-CHECK, MEASURE, REPEAT",
                     "Measure each object three times using an appropriate tool.")
        steps=["1. Check the instrument zero.","2. Record its resolution.",
               "3. Measure the same feature three times.",
               "4. Compute maximum minus minimum.",
               "5. Discuss spread and possible measurement errors."]
        for i,step in enumerate(steps):
            y=.88-i*.67
            m=self.put(step,(0,y),31,DARK,False,12.25)
            self.appearance(m,time=.66)
            self.wait(.40)
        self.caption("Do not adjust the measurements to match an expected value.")
        self.wait(3.5)

    def two_objects(self):
        self.chapter(2,"CHOOSING AN INSTRUMENT",
                     "SMALL WIRE DIAMETER AND A SOLID BLOCK",
                     "Example: micrometer for wire; caliper for block width.")
        wire=Circle(radius=.55,stroke_color=SKETCH,stroke_width=4,
                    fill_color=MODEL,fill_opacity=1).move_to([-3.5,-.33,0])
        width_arrow=DoubleArrow([-4.04,-1.15,0],[-2.96,-1.15,0],
                               color=SKETCH,buff=0,stroke_width=3.3)
        block=RoundedRectangle(width=2.47,height=1.20,
                               corner_radius=.14,stroke_color=POSITIVE,
                               stroke_width=3.1,fill_color=TERRAIN,
                               fill_opacity=1).move_to([3.38,-.34,0])
        block_arrow=DoubleArrow([2.15,-1.27,0],[4.61,-1.27,0],
                               buff=0,color=POSITIVE,stroke_width=3.3)
        self.draw(wire,width_arrow,block,block_arrow,time=2)
        self.textline("Wire diameter",-.02,SKETCH,27,True,5.2,-3.50)
        self.textline("Block width",-1.95,POSITIVE,27,True,5.4,3.35)
        self.caption("Illustrative objects: choose a tool with suitable range and resolution.")
        self.wait(3.8)

    def readings_table(self):
        self.chapter(3,"REPEATED OBSERVATIONS","WRITE A LAB TABLE WITH UNITS",
                     "The following values are invented examples, not student data.")
        headers=["OBJECT","READINGS (mm)","RANGE","TOOL","RES."]
        rows=[
            ["Wire","1.22, 1.23, 1.22","0.01","Micrometer","0.01 mm"],
            ["Block","32.1, 32.2, 32.1","0.1","Caliper","0.1 mm"],
        ]
        widths=[1.72,4.12,1.63,2.60,2.20];total=sum(widths);start=-total/2
        for i,row in enumerate([headers,*rows]):
            x=start
            for j,(v,w) in enumerate(zip(row,widths)):
                cx=x+w/2;cy=.75-i*1.05
                rect=Rectangle(width=w,height=.97,
                               stroke_color=LIGHT,stroke_width=1.7,
                               fill_color=TERRAIN if i==0 else WHITE,
                               fill_opacity=1).move_to([cx,cy,0])
                label=self.put(v,(cx,cy),24 if i==0 else 25,
                        SKETCH if i==0 else DARK,i==0,w-.17)
                self.draw(rect,time=.13)
                self.play(Write(label),run_time=.27)
                x+=w
            self.wait(1.55)
        self.caption("Keep object identity, all readings, instrument and resolution together.")
        self.wait(3.8)

    def range_calculation(self):
        self.chapter(4,"MEASUREMENT SPREAD","RANGE = MAXIMUM MINUS MINIMUM",
                     "A range summarizes the spread in the repeated data.")
        r1=self.eq(r"R_{\rm wire}=1.23-1.22=0.01\,\mathrm{mm}",
                   (0,.69),49,SKETCH)
        r2=self.eq(r"R_{\rm block}=32.2-32.1=0.1\,\mathrm{mm}",
                   (0,-.33),49,POSITIVE)
        self.appearance(r1,time=1.5)
        self.wait(1)
        self.appearance(r2,time=1.5)
        self.textline("Different instruments have different resolutions.",-1.56,DARK,30)
        self.caption("The range is measured spread; it is not automatically total uncertainty.")
        self.wait(4.4)

    def data_plot(self):
        self.chapter(5,"COMPARE WITHIN EACH SCALE",
                     "PLOT ALL THREE REPEATED MEASUREMENTS",
                     "Each object uses its own labelled horizontal scale.")
        setups=[
            (-3.40,"WIRE / mm",1.20,1.25,[1.22,1.23,1.22],SKETCH),
            (3.40,"BLOCK / mm",32.0,32.3,[32.1,32.2,32.1],POSITIVE),
        ]
        for cx,description,lo,hi,values,c in setups:
            self.textline(description,1.03,c,31,True,5.4,cx)
            x0=cx-2.28;x1=cx+2.28;y=-.42
            baseline=self.line((x0,y),(x1,y),DARK,2.8)
            self.draw(baseline,time=.6)
            for index,v in enumerate(values):
                px=x0+(v-lo)/(hi-lo)*(x1-x0)
                py=y+(.35 if index==1 else -.30 if index==0 else .65)
                mark=Dot([px,py,0],radius=.16,color=c)
                self.play(FadeIn(mark),run_time=.50)
                self.register(mark)
            lb=self.put(f"{lo:.2f}" if hi<2 else f"{lo:.1f}",
                        (x0,-1.16),23,DARK,False,1.55)
            hb=self.put(f"{hi:.2f}" if hi<2 else f"{hi:.1f}",
                        (x1,-1.16),23,DARK,False,1.55)
            self.appearance(lb,hb,time=.57)
        self.caption("Never put unrelated instrument scales on an unlabeled common axis.")
        self.wait(4.2)

    def uncertainty(self):
        self.chapter(6,"RESOLUTION VS UNCERTAINTY",
                     "A FINE SCALE DOES NOT REMOVE ALL ERROR",
                     "Repeated spread, resolution and calibration each matter.")
        words=[
            ("RESOLUTION","Smallest displayed instrument increment",SKETCH),
            ("RANGE","Difference between largest and smallest reading",POSITIVE),
            ("UNCERTAINTY","A supported estimate considering relevant sources",NEGATIVE),
        ]
        for i,(title,explanation,col) in enumerate(words):
            y=.90-i*1.10
            self.textline(title,y,col,33,True,5.20,-3.90)
            self.textline(explanation,y,DARK,25,False,7.70,2.05)
            self.wait(.77)
        self.caption("Do not equate range, resolution and total measurement uncertainty.")
        self.wait(4.6)

    def practice(self):
        self.chapter(7,"CLASSROOM MINI-LAB","REPEAT TWO REAL MEASUREMENTS",
                     "Use your own tools and values, never the illustrative numbers.")
        steps=[
            "A. Measure a small object's thickness three times.",
            "B. Measure a second object's width three times.",
            "C. Record units and instrument resolution.",
            "D. Find each object's maximum, minimum and range.",
            "E. Explain which tool was more appropriate.",
        ]
        for i,s in enumerate(steps):
            p=self.put(s,(0,.82-i*.70),30,DARK,False,12.25)
            self.appearance(p,time=.73)
            self.wait(.35)
        self.caption("Exit ticket: Does a small range prove that the result is accurate?")
        self.wait(7.0)
