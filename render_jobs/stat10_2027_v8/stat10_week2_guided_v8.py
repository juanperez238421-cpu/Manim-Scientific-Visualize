# -*- coding: utf-8 -*-
"""WEEK 2 - GUIDED CHALLENGE 2 | Census, sampling plans and hidden weighting.
Built on IJR Statistics 10 Week 2 (25-29 Jan 2027).
This is a fictional instructional thought experiment, not a real survey.
Run: manim -qh stat10_week2_guided_v8.py Stat10Week2GuidedV8
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from stat10_guided_v8_common import *
from fractions import Fraction

N_M,N_A=90,30
N=N_M+N_A
SAMPLE=24
RECOMMEND_M,RECOMMEND_A=18,6
BALANCED_M,BALANCED_A=12,12
YES_M,YES_A=4,8
NAIVE=Fraction(YES_M+YES_A,BALANCED_M+BALANCED_A)
WEIGHTED=Fraction(N_M,N)*Fraction(YES_M,BALANCED_M)+Fraction(N_A,N)*Fraction(YES_A,BALANCED_A)
assert (N,N_M,N_A)==(120,90,30)
assert (RECOMMEND_M,RECOMMEND_A)==(18,6)
assert NAIVE==Fraction(1,2)
assert WEIGHTED==Fraction(5,12)

class Stat10Week2GuidedV8(GuidedClassroomV8):
    week=2
    def construct(self):
        self.cover("WEEK 2: TWO SAMPLING PLANS",
                   "2027 / Q1 / Guided exercise 2: why selection changes the answer")

        self.section(1,"WHO SHOULD BE INCLUDED?",
                     "Compare a census with a limited sample of 24 students.")
        cases=table(["Schedule","In population"],
              [["Morning","90"],["Afternoon","30"],["Total","120"]],
              widths=[5.1,4.3],height=.79,fontsize=32)
        self.show_table(cases,pos=(0,.3,0))
        formula=math(r"N=90+30=120",56).move_to([0,-2.04,0])
        self.play(Write(formula),run_time=1.6)
        self.answer("A census observes all 120; a sample observes fewer.",2.2)

        self.section(2,"VISUALIZE THE POPULATION STRUCTURE",
                     "The schedules do not contribute equal numbers of students.")
        morning=Rectangle(width=8.1,height=1.5,stroke_color=INK,
            fill_opacity=1,fill_color=PALE)
        afternoon=Rectangle(width=2.7,height=1.5,stroke_color=INK,
            fill_opacity=1,fill_color=WHITE)
        pair=VGroup(morning,afternoon).arrange(RIGHT,buff=0).move_to([0,.32,0])
        self.play(GrowFromEdge(morning,LEFT),GrowFromEdge(afternoon,LEFT),run_time=2.2)
        self.play(Write(math("90",59).move_to(morning)),
                  Write(math("30",59).move_to(afternoon)),run_time=1.5)
        left=text("Morning",31).next_to(morning,DOWN,buff=.26)
        right=text("Afternoon",31).next_to(afternoon,DOWN,buff=.26)
        self.play(FadeIn(left),FadeIn(right),run_time=.9)
        ratio=math(r"\frac{90}{120}=\frac34,\qquad\frac{30}{120}=\frac14",55).move_to([0,-2.11,0])
        self.play(Write(ratio),run_time=2.3)
        self.wait(3)

        self.section(3,"PLAN A: ONLY THE MORNING",
                     "Convenient does not mean the whole population is covered.")
        t=table(["Schedule","Population","Selected"],
              [["Morning","90","24"],["Afternoon","30","0"],["Total","120","24"]],
              widths=[3.5,3.5,3.2],height=.76,fontsize=32)
        self.show_table(t,pos=(0,.25,0))
        self.indicate_row(t[2],duration=2)
        self.answer("The afternoon schedule has no chance to appear.",2.2)

        self.section(4,"PLAN B: A PROPORTIONAL SAMPLE",
                     "Work out how to distribute a sample of 24.")
        start=math(r"n=24,\quad N=120",54).move_to([0,1.48,0])
        first=math(r"n_M=24\left(\frac{90}{120}\right)=18",53).move_to([0,.13,0])
        second=math(r"n_A=24\left(\frac{30}{120}\right)=6",53).move_to([0,-1.19,0])
        self.play(Write(start),run_time=1.5)
        self.pause_for_class("How many students should come from each schedule?",3)
        self.play(Write(first),run_time=2.0)
        self.play(Write(second),run_time=2.0)
        self.wait(2.2)
        check=math(r"18+6=24",56).move_to([0,-2.37,0])
        self.play(Write(check),run_time=1.4)
        self.wait(2.2)

        self.section(5,"A SECOND PLAN LOOKS BALANCED",
                     "Equal representation is not proportional in this school.")
        t=table(["Schedule","Population","Equal sample","Proportional"],
              [["Morning","90","12","18"],["Afternoon","30","12","6"],
               ["Total","120","24","24"]],
              widths=[3.2,2.5,3.4,3.2],height=.77,fontsize=29)
        self.show_table(t,pos=(0,.12,0))
        frame1=SurroundingRectangle(VGroup(*[r[2] for r in t[1:]]),color=INK,buff=.07)
        self.play(Create(frame1),run_time=.9)
        self.wait(1.2)
        frame2=SurroundingRectangle(VGroup(*[r[3] for r in t[1:]]),color=INK,buff=.07)
        self.play(ReplacementTransform(frame1,frame2),run_time=1.4)
        self.answer("Equal sample counts do not match 90-to-30 population sizes.",2.4)

        self.section(6,"A TRICKY DATA INTERPRETATION",
                     "Hypothetical yes responses under an equal 12 + 12 sample.")
        t=table(["Schedule","Asked","Said yes","Within group"],
              [["Morning","12","4","4 of 12"],["Afternoon","12","8","8 of 12"],
               ["Total","24","12","12 of 24"]],
              widths=[3.3,2.1,2.5,3.4],height=.78,fontsize=30)
        self.show_table(t,pos=(0,.15,0))
        naive=math(r"\frac{12}{24}=50\%",58).move_to([0,-2.30,0])
        self.play(Write(naive),run_time=1.5)
        self.wait(2.1)

        self.section(7,"WHY THE SIMPLE FRACTION IS MISLEADING",
                     "The morning group is three times larger in the population.")
        expr=math(r"\hat p=\frac{90}{120}\frac4{12}+\frac{30}{120}\frac8{12}",56).move_to([0,1.03,0])
        next_expr=math(r"\hat p=\frac34\cdot\frac13+\frac14\cdot\frac23",58).move_to([0,1.03,0])
        result=math(r"\hat p=\frac5{12}\approx41.7\%",67).move_to([0,-.56,0])
        self.play(Write(expr),run_time=2.6)
        self.wait(1.3)
        self.play(TransformMatchingTex(expr,next_expr),run_time=2.0)
        self.play(Write(result),run_time=2.3)
        self.wait(2.1)
        self.answer("50% describes this sample; 41.7% is a weighted estimate.",2.5)

        self.section(8,"CHECK THE ASSUMPTIONS",
                     "A numerical adjustment cannot repair poor selection.")
        card_a,card_b,_=two_cards("STILL A RISK",[
              "Volunteers may differ","from other students"],
              "BETTER PROCEDURE",["Select within each","schedule using a rule"],y=.19)
        self.play(FadeIn(card_a,shift=LEFT*.30),run_time=1.2)
        self.play(FadeIn(card_b,shift=RIGHT*.30),run_time=1.2)
        self.play(Circumscribe(card_b,color=INK,run_time=1.4))
        self.answer("Coverage, selection method and question wording all matter.",2.4)

        self.section(9,"PAIR TASK: COMPLETE AN INVESTIGATION",
                     "Design a sample and identify one limitation.")
        self.task(["1. Census or sample? Explain why n is not N.",
                   "2. Allocate n = 24 using the 90-to-30 composition.",
                   "3. Explain why asking only morning students is risky.",
                   "4. Rewrite one leading survey question neutrally.",
                   "5. State what cannot be concluded with certainty."],
                  "Proportional allocation is useful, not a guarantee.",thinking=7)
