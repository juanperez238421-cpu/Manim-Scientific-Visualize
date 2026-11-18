# -*- coding: utf-8 -*-
"""WEEK 4 - GUIDED CHALLENGE 2 | Discrete/continuous and reliable raw records.
IJR Statistics 10 Week 4, 8-12 February 2027.
NO frequency tables, histograms or statistical frequency plots are introduced.
Run: manim -qh stat10_week4_guided_v8.py Stat10Week4GuidedV8
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from stat10_guided_v8_common import *

DEVICE_COUNTS=(2,0,1,3,1,2)
WAIT_SECONDS=(12.36,8.40,10.25,14.10,None,11.65)
TRANSPORT=(12,15,21,12,15,21)
TEMPERATURE=(24.1,23.8,24.0,24.2,23.9,24.1)
assert len(DEVICE_COUNTS)==len(WAIT_SECONDS)==len(TRANSPORT)==len(TEMPERATURE)==6
assert all(int(n)==n and n>=0 for n in DEVICE_COUNTS)
assert sum(v is None for v in WAIT_SECONDS)==1

class Stat10Week4GuidedV8(GuidedClassroomV8):
    week=4
    def construct(self):
        self.cover("WEEK 4: COUNTS, MEASUREMENTS AND MISSING DATA",
                   "2027 / Q1 / Guided exercise 2: classification under uncertainty")

        self.section(1,"START WITH MEANING, NOT THE DIGITS",
                     "A full decision separates labels, counts, and measurements.")
        a=box("CATEGORY / CODE",["Qualitative value","Example: route 12"],5.15,2.5)
        b=box("COUNT",["Discrete quantitative","Example: two devices"],5.15,2.5)
        c=box("MEASUREMENT",["Continuous quantitative","Example: 12.36 seconds"],5.15,2.5)
        grp=VGroup(a,b,c).arrange(RIGHT,buff=.25).move_to([0,.02,0])
        fit(grp,14.5,4.2)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in grp],
                  lag_ratio=.35),run_time=3.2)
        self.wait(3)
        self.answer("Numbers may represent labels, counts, or measurements.",2)

        self.section(2,"DISCRETE: AN EXACT COUNT",
                     "Counting the number of devices brought to school.")
        counts=DEVICE_COUNTS
        label=math(r"2,\;0,\;1,\;3,\;1,\;2",65).move_to([0,1.72,0])
        self.play(Write(label),run_time=2)
        g=VGroup()
        for i,count in enumerate(counts):
            dots=VGroup(*[Dot(radius=.15,color=INK) for _ in range(count)])
            if count:
                dots.arrange(UP,buff=.10)
            else:
                dots=VGroup(Circle(radius=.18,stroke_color=GRID,stroke_width=2.1))
            dots.move_to([-5.0+2*i,-.46,0])
            g.add(dots)
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.20) for x in g],lag_ratio=.23),
                  run_time=3)
        indexes=VGroup(*[math(f"S{i+1}",36).move_to([-5.0+2*i,-1.63,0])
                        for i in range(6)])
        # S1..S6 are graphical record labels, not numerical quantities.
        self.play(FadeIn(indexes,shift=UP*.08),run_time=.95)
        self.answer("A count uses separated possible whole-number values.",2.5)

        self.section(3,"CONTINUOUS: THE STOPWATCH MODEL",
                     "Elapsed waiting time varies between whole-number seconds.")
        line=NumberLine(x_range=[8,16,2],length=11.6,
              include_numbers=True,label_direction=DOWN,color=INK).move_to([0,-.63,0])
        dot=Dot(line.n2p(8),radius=.18,color=INK)
        self.play(Create(line),FadeIn(dot),run_time=1.6)
        duration=3.9
        self.play(dot.animate.move_to(line.n2p(12.36)),
                   run_time=duration,rate_func=smooth)
        value=math(r"t=12.36\ \mathrm{s}",65).move_to([0,1.52,0])
        self.play(Write(value),run_time=1.8)
        self.wait(2.7)
        self.answer("Time is measured on a continuum, not counted in objects.",2.3)

        self.section(4,"ROUNDING CHANGES RESOLUTION, NOT TYPE",
                     "Same measured phenomenon, different recording precision.")
        a=math(r"12.36\ \mathrm{s}",71).move_to([0,.36,0])
        b=math(r"12.4\ \mathrm{s}",71).move_to([0,.36,0])
        c=math(r"12\ \mathrm{s}",71).move_to([0,.36,0])
        self.play(Write(a),run_time=1.7)
        self.pause_for_class("Report the measurement to one decimal place.",2.6)
        self.play(TransformMatchingTex(a,b),run_time=1.8)
        self.wait(1.7)
        self.play(TransformMatchingTex(b,c),run_time=1.8)
        self.wait(2.6)
        self.answer("Rounded time remains a continuous variable.",2.5)

        self.section(5,"FOUR HARD CASES: SAME LOOK, DIFFERENT TYPE",
                     "Decide whether each value is a code, count, or measurement.")
        t=table(["Recorded value","Meaning","Correct classification"],
              [["Route 204","Service identifier","Qualitative"],
               ["204 books","Exact number of books","Quant. discrete"],
               ["24.1 C","Temperature observed","Quant. continuous"],
               ["Age 15 yr","Rounded elapsed time","Quant. continuous"]],
              widths=[3.0,4.6,5.0],height=.70,fontsize=28)
        self.show_table(t,pos=(0,.25,0))
        self.indicate_row(t[1],duration=.85)
        self.indicate_row(t[4],duration=.85)
        self.answer("Classify the underlying variable, not its formatting.",2.5)

        self.section(6,"BUILD A SIX-ROW RAW DATA RECORD",
                     "One row per fictional observational unit, with units in headings.")
        obs=[
             ["S01","12","2","12.36","24.1"],
             ["S02","15","0","8.40","23.8"],
             ["S03","21","1","10.25","24.0"],
             ["S04","12","3","14.10","24.2"],
             ["S05","15","1","Missing","23.9"],
             ["S06","21","2","11.65","24.1"],
        ]
        t=table(["ID","Route","Devices","Wait (s)","Temp. (C)"],
                obs,widths=[1.8,2.1,2.65,2.85,3.3],height=.54,fontsize=27)
        self.show_table(t,pos=(0,.17,0))
        self.wait(2.2)
        self.answer("Keep units explicit and do not replace missing values with zero.",2.5)

        self.section(7,"ZERO IS NOT THE SAME AS MISSING",
                     "These two records express different information.")
        a,b,_=two_cards("OBSERVED ZERO",["Student S02","0 devices"],
                        "UNKNOWN VALUE",["Student S05","Wait time missing"],y=.22)
        self.play(FadeIn(a,shift=LEFT*.23),run_time=1.3)
        self.play(FadeIn(b,shift=RIGHT*.23),run_time=1.3)
        cmp=math(r"0\neq\mathrm{missing}",60).move_to([0,-2.15,0])
        self.play(Write(cmp),run_time=1.7)
        self.wait(2.7)
        self.answer("A missing response must not be invented.",2.0)

        self.section(8,"CHECK EVERY VARIABLE BEFORE ANALYSIS",
                     "Use a classification and recording checklist.")
        t=table(["Field","Kind","What to check"],
                [["Route","Category","Codes documented"],
                 ["Devices","Discrete","Nonnegative integers"],
                 ["Wait (s)","Continuous","Units and missing cells"],
                 ["Temp. (C)","Continuous","Measurement precision"]],
                widths=[3.2,3.45,5.3],height=.70,fontsize=29)
        self.show_table(t,pos=(0,.14,0))
        self.answer("Quality control comes before frequency tables and graphs.",2.5)

        self.section(9,"FINAL GUIDED EXERCISE",
                     "A last transfer task using no statistical frequency table.")
        self.task(["1. Is a student identifier qualitative or quantitative?",
                   "2. Why are the number of devices and wait time different?",
                   "3. Does rounding a thermometer create a discrete variable?",
                   "4. What should a blank response mean in a raw record?",
                   "5. Create two valid invented observations with units."],
                  "Define, classify, justify and record before graphing.",thinking=7)
