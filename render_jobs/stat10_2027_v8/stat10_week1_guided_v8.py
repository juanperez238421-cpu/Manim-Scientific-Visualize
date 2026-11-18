# -*- coding: utf-8 -*-
"""WEEK 1 - GUIDED CHALLENGE 2 | Four-week statistics companion collection V8.
Statistical question, precise populations, nested sets, samples and justified
conclusions. Based on IJR Statistics 10 Week 1 (19-22 Jan 2027).
Run: manim -qh stat10_week1_guided_v8.py Stat10Week1GuidedV8
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from stat10_guided_v8_common import *
from collections import Counter

GROUPS=(32,29,31)
SELECTION=(2,7,11,21,28,33,37,41,49,54,58,63,67,72,78,81,86,90)
HOURS=(6,7,8,6,7,9,5,8,7,6,7,8,9,6,7,8,5,7)
assert sum(GROUPS)==92 and len(SELECTION)==len(HOURS)==18
assert len(set(SELECTION))==18 and min(SELECTION)>=0 and max(SELECTION)<92
assert [sum(0<=x<32 for x in SELECTION),
        sum(32<=x<61 for x in SELECTION),
        sum(61<=x<92 for x in SELECTION)]==[5,6,7]
assert Counter(HOURS)[7]==6

class Stat10Week1GuidedV8(GuidedClassroomV8):
    week=1
    def construct(self):
        self.cover("WEEK 1: A TRICKIER STATISTICAL QUESTION",
                   "2027 / Q1 / Guided exercise 2: sleep hours and target groups")

        self.section(1,"START WITH THE RIGHT QUESTION",
                     "A fixed fact and a question requiring multiple observations.")
        left,right,_=two_cards("FIXED FACT",["How many hours","are in one day?"],
             "STATISTICAL QUESTION",["How many hours do","Grade 10 students sleep?"],y=.28)
        self.play(FadeIn(left,shift=LEFT*.35),run_time=1.0)
        self.play(FadeIn(right,shift=RIGHT*.35),run_time=1.0)
        v1=math("24",65).move_to([-3.35,-2.0,0])
        v2=math(r"5,\ 6,\ 7,\ 8,\ 9",55).move_to([3.40,-2.0,0])
        self.play(Write(v1),run_time=.95)
        self.play(Write(v2),run_time=1.4)
        self.play(Circumscribe(right,color=INK,run_time=1.1))
        self.wait(2)
        self.section(2,"DEFINE THE TARGET BEFORE COUNTING",
                     "Which students belong to this investigation?")
        t=table(["Section","Enrolled students","Target?"],
             [["10A","32","Yes"],["10B","29","Yes"],["10C","31","Yes"]],
             widths=[3.2,4.1,3.4],height=.74,fontsize=31)
        self.show_table(t,pos=(0,.29,0))
        eq=math(r"N=32+29+31=92",59).move_to([0,-2.08,0])
        self.play(Write(eq),run_time=1.7)
        self.wait(2)
        self.section(3,"CHANGE THE QUESTION, CHANGE THE POPULATION",
                     "The correct population depends on the wording.")
        qa,qb,_=two_cards("ALL GRADE 10",["Three sections","N = 92"],
             "ONLY SECTION 10B",["One section","N = 29"],y=.24)
        self.play(FadeIn(qa,shift=LEFT*.25),FadeIn(qb,shift=RIGHT*.25),run_time=1.8)
        whole=math(r"N_{\mathrm{all}}=92",49).move_to([-3.38,-2.0,0])
        part=math(r"N_{\mathrm{10B}}=29",49).move_to([3.38,-2.0,0])
        self.play(Write(whole),Write(part),run_time=1.7)
        self.answer("A population must match the question's target.",2.8)

        self.section(4,"ANIMATE THE SELECTED SUBSET",
                     "A group of 18 fictional students answers the question.")
        dots=dot_matrix(92,columns=12,radius=.095,sx=.37,sy=.42)
        dots.move_to([-3.35,-.08,0])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],
                lag_ratio=.006),run_time=2.9)
        chosen=VGroup(*[dots[i] for i in SELECTION])
        self.play(LaggedStart(*[d.animate.set_fill(INK,opacity=1) for d in chosen],
                lag_ratio=.075),run_time=2.6)
        copies=chosen.copy()
        self.add(copies)
        target=dot_matrix(18,columns=6,radius=.165,sx=.56,sy=.61)
        target.move_to([3.5,-.1,0])
        self.play(Transform(copies,target),run_time=2.65,rate_func=smooth)
        labs=VGroup(math("N=92",55).move_to([-3.35,1.95,0]),
                    math("n=18",55).move_to([3.50,1.95,0]))
        self.play(Write(labs),run_time=1.4)
        self.answer("A sample is a subset of the defined population.",2)

        self.section(5,"CONNECT SECTION MEMBERSHIP TO THE SAMPLE",
                     "The same 18 sampled observations come from three sections.")
        t=table(["Section","Population","Observed"],
          [["10A","32","5"],["10B","29","6"],["10C","31","7"],["Total","92","18"]],
          widths=[3.5,3.5,3.4],height=.68,fontsize=31)
        self.show_table(t,pos=(0,.20,0))
        self.indicate_row(t[-1],duration=1.0)
        eq=math(r"n=5+6+7=18",53).move_to([0,-2.26,0])
        self.play(Write(eq),run_time=1.6)
        self.wait(2.0)

        self.section(6,"OBSERVE 18 DISTINCT SLEEP RESPONSES",
                     "Each dot is one individual's reported sleep time in hours.")
        axis=NumberLine(x_range=[5,10,1],length=11.4,include_numbers=True,
                  label_direction=DOWN,color=INK).move_to([0,-.73,0])
        heading=text("Sleep duration on a school night (h)",37,True).move_to([0,1.93,0])
        self.play(Write(heading),Create(axis),run_time=2)
        stacked={}
        ds=VGroup()
        for h in HOURS:
            level=stacked.get(h,0); stacked[h]=level+1
            ds.add(Dot(axis.n2p(h)+UP*(.22+.31*level),radius=.13,color=INK))
        self.play(LaggedStart(*[GrowFromCenter(x) for x in ds],
                  lag_ratio=.09),run_time=3.3)
        self.wait(3)
        self.answer("Responses vary from 5 h to 9 h in this observed sample.",2.5)

        self.section(7,"DO NOT CONFUSE TWO DIFFERENT RATIOS",
                     "Sample coverage is not a measured sleep percentage.")
        first=math(r"\frac{18}{92}\approx 19.6\%",56).move_to([0,.98,0])
        second=math(r"\frac{6}{18}=\frac13\approx 33.3\%",56).move_to([0,-.73,0])
        l1=text("Share of the population that was observed",30).next_to(first,DOWN,buff=.22)
        l2=text("Share of the sample reporting 7 hours",30).next_to(second,DOWN,buff=.22)
        self.play(Write(first),FadeIn(l1),run_time=2.0)
        self.play(Write(second),FadeIn(l2),run_time=2.0)
        self.wait(2.5)
        self.answer("Both fractions are correct; they answer different questions.",2.5)

        self.section(8,"A SECOND CASE TO TRANSFER THE METHOD",
                     "A principal asks 8 of 45 teachers about grading time.")
        self.task(["1. What is the population in this teacher study?",
                   "2. Which people belong to its sample?",
                   "3. Does asking 8 teachers mean asking every teacher?",
                   "4. Write a justified conclusion about sample versus population."],
             "Population: 45 teachers. Sample: 8 teachers. No census.",thinking=6)

        self.section(9,"EXIT CHECK: YOUR OWN TWO-SENTENCE ANSWER",
                     "Explain without copying a definition.")
        self.task(["Describe why sleep time is a statistical question.",
                   "Identify a population and a smaller sample.",
                   "State one reason a sample result is not the entire population."],
             "State the target group, observed subset, and limitation.",thinking=7)
