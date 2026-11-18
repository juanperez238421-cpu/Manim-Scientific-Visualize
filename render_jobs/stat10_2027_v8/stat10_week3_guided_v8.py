# -*- coding: utf-8 -*-
"""WEEK 3 - GUIDED CHALLENGE 2 | A numerical code is not a quantity.
Statistical variable meaning, anonymized observational records and ambiguous cases.
IJR Statistics 10 Week 3, 1-5 February 2027.
Run: manim -qh stat10_week3_guided_v8.py Stat10Week3GuidedV8
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from stat10_guided_v8_common import *

RECORDS=[
 ("S01","12","18.4","2","4"),
 ("S02","15","12.1","0","5"),
 ("S03","21","25.0","3","3"),
 ("S04","12","10.2","1","4"),
 ("S05","15","23.3","2","2"),
 ("S06","21","15.8","1","5"),
]
CODES={"12":"Bus","15":"Walk","21":"Bike"}
assert len(RECORDS)==6 and len({r[0] for r in RECORDS})==6
assert all(r[1] in CODES for r in RECORDS)
assert all(float(r[2])>0 and int(r[3])>=0 and 1<=int(r[4])<=5 for r in RECORDS)

class Stat10Week3GuidedV8(GuidedClassroomV8):
    week=3
    def construct(self):
        self.cover("WEEK 3: THE NUMERIC CODE TRAP",
                   "2027 / Q1 / Guided exercise 2: read a dataset by meaning")

        self.section(1,"SIX RECORDS, FIVE FIELDS",
                     "Each row describes one fictitious student.")
        t=table(["ID","Route code","Minutes","Siblings","Rating"],
              RECORDS,widths=[1.7,2.8,2.65,2.5,2.5],height=.54,fontsize=27)
        self.show_table(t,pos=(0,.06,0))
        self.wait(2)
        self.indicate_row(t[3],duration=1.4)
        self.answer("The observational unit is a student, not a column.",2.5)

        self.section(2,"EXTRACT THE VARIABLE AND ITS VALUE",
                     "Do not confuse the column name with one response.")
        key=box("VARIABLE",["Travel duration","Measured in minutes"],6.15,2.75)
        value=box("ONE OBSERVATION",["18.4 minutes","Recorded for S01"],6.15,2.75)
        pair=VGroup(key,value).arrange(RIGHT,buff=.65).move_to([0,.25,0])
        self.play(GrowFromCenter(key),run_time=1.2)
        self.play(GrowFromCenter(value),run_time=1.2)
        eq=math(r"x_{\mathrm{S01}}=18.4\ \mathrm{min}",55).move_to([0,-2.23,0])
        self.play(Write(eq),run_time=2.0)
        self.wait(2.1)

        self.section(3,"IDENTICAL DIGITS, DIFFERENT MEANINGS",
                     "Does the number 12 count twelve objects?")
        route=box("ROUTE 12",["A bus-line identifier","Qualitative category"],6.05,2.7)
        distance=box("12 KILOMETERS",["A measured distance","Quantitative value"],6.05,2.7)
        pair=VGroup(route,distance).arrange(RIGHT,buff=.67).move_to([0,.24,0])
        self.play(FadeIn(route,shift=LEFT*.31),run_time=1.2)
        self.play(FadeIn(distance,shift=RIGHT*.31),run_time=1.2)
        a=math(r"12",69).move_to([-3.32,-2.0,0])
        b=math(r"12",69).move_to([3.32,-2.0,0])
        self.play(Write(a),Write(b),run_time=1.2)
        self.answer("Type follows what the variable represents, not its digits.",2.5)

        self.section(4,"READ THE CODING DICTIONARY",
                     "The number is a code assigned to a transport category.")
        t=table(["Stored code","Meaning","Actual type"],
            [["12","Bus","Qualitative"],["15","Walk","Qualitative"],
             ["21","Bike","Qualitative"]],
             widths=[3.25,3.25,4.15],height=.76,fontsize=30)
        self.show_table(t,pos=(0,.24,0))
        label=text("Coding is a naming convention, not arithmetic.",32,True).move_to([0,-2.21,0])
        self.play(Write(label),run_time=2.1)
        self.wait(2.2)

        self.section(5,"DECODE THE ORIGINAL STUDY",
                     "The same records become understandable when we know the codebook.")
        codes=[["S01","12","Bus"],["S02","15","Walk"],["S03","21","Bike"],
               ["S04","12","Bus"],["S05","15","Walk"],["S06","21","Bike"]]
        t=table(["ID","Stored code","Interpreted category"],codes,
                 widths=[2.8,3.6,5.1],height=.60,fontsize=30)
        self.show_table(t,pos=(0,.06,0))
        self.wait(2.8)
        self.answer("The code identifies a mode; it is not a measured magnitude.",2.2)

        self.section(6,"IS ARITHMETIC MEANINGFUL ON CODES?",
                     "A typical mathematical operation may not answer any real question.")
        expr=math(r"\frac{12+21}{2}=16.5",70).move_to([0,.48,0])
        self.play(Write(expr),run_time=2.0)
        self.pause_for_class("Does route 16.5 describe a transport mode?",3)
        caution=box("NO",["The average of route labels","does not describe a route"],10.3,2.1)
        caution.move_to([0,-1.66,0])
        self.play(FadeIn(caution,shift=UP*.2),run_time=1.35)
        self.wait(2.7)

        self.section(7,"AMBIGUOUS CASE: A RATING OF FIVE",
                     "A 1--5 satisfaction scale is a coded ordered response.")
        score=math(r"1,\;2,\;3,\;4,\;5",69).move_to([0,1.20,0])
        self.play(Write(score),run_time=2)
        a,b,_=two_cards("5 STARS",["Ordered response","Category level"],
                        "5 MINUTES",["Measured duration","Numerical amount"],y=-.96)
        self.play(FadeIn(a,shift=LEFT*.25),run_time=1.1)
        self.play(FadeIn(b,shift=RIGHT*.25),run_time=1.1)
        self.wait(2.7)
        self.answer("Meaning and recording conventions determine the type.",2.3)

        self.section(8,"WRITE A SMALL DATA DICTIONARY",
                     "Precisely define what each column records.")
        desc=[
          ["ID","Record label","Qualitative"],
          ["Route code","Transport mode","Qualitative"],
          ["Minutes","Travel duration","Quantitative"],
          ["Siblings","Count of siblings","Quantitative"],
          ["Rating","1--5 ordered levels","Qualitative"],
        ]
        t=table(["Field","What it means","Classification"],desc,
             widths=[3.1,5.0,4.2],height=.62,fontsize=28)
        self.show_table(t,pos=(0,.10,0))
        self.wait(2.1)
        self.answer("A variable needs its meaning, not only a column name.",2.3)

        self.section(9,"FINAL ERROR-DETECTION CHALLENGE",
                     "Evaluate and correct the following statements.")
        self.task(["1. Route code 21 is a quantitative amount.",
                   "2. ID S01 is a measured student characteristic.",
                   "3. Travel time 25.0 is a quantitative observation.",
                   "4. A rating of 5 must represent five objects.",
                   "5. Explain two cases where numbers are not quantities."],
                  "Correct claims 1, 2 and 4; justify every classification.",thinking=7)
