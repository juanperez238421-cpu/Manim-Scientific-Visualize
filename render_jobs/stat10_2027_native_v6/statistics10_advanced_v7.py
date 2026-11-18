# -*- coding: utf-8 -*-
"""Statistics 10: Four ADVANCED companion example films, 2027 Quarter 1.
Manim Community Edition 0.20.1. Native LaTeX typography, 1920x1080 @ 30fps.
Designed to COMPLEMENT, not replace, the four V6 weekly lessons.
Curriculum anchor: Statistics_10_2027_P1.docx (Weeks 1-4) and IJR 2026 P1 malla.
All data are invented; no personal student information.

Render one native film:
  manim -ql statistics10_advanced_v7.py Stat10AppliedWeek1V7
  manim -qh statistics10_advanced_v7.py Stat10AppliedWeek1V7
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from statistics10_latex_v6 import (
    ClassroomLatex, INK, SECONDARY, GRID, PALE,
    latex_text, fit, text_lines, box, unit_grid, raw_table
)
from manim import *
import numpy as np

# -----------------------------------------------------------------------------
# Pedagogical test data. Every numerical assertion is checked before rendering.
# -----------------------------------------------------------------------------
READING=[20,35,45,20,60,50,70,15,55,40,30,65]
GROUP_A=42
GROUP_B=38
SAMPLE_A=6
SAMPLE_B=6
MORNING=80
AFTERNOON=40
DRAW=24
ALLOC_M=16
ALLOC_A=8
SIBLINGS=[2,1,0,3,2,1]
TRAVEL=[18.4,12.3,9.7,25.1,14.2,17.8]
assert len(READING)==12 and min(READING)>=0 and max(READING)<=80
assert GROUP_A+GROUP_B==80 and SAMPLE_A+SAMPLE_B==12
assert MORNING+AFTERNOON==120 and ALLOC_M+ALLOC_A==DRAW
assert MORNING/120==ALLOC_M/24 and AFTERNOON/120==ALLOC_A/24
assert len(SIBLINGS)==len(TRAVEL)==6 and all(x>=0 and int(x)==x for x in SIBLINGS)
assert all(x>0 for x in TRAVEL)

def mt(expression, size=49):
    return MathTex(expression, font_size=size, color=INK)

def center_group(*objects, gap=.42, y=-.12):
    g=VGroup(*objects).arrange(DOWN,buff=gap)
    fit(g,14.0,5.6)
    g.move_to([0,y,0])
    return g

def pointer_note(label,width=5.2):
    r=RoundedRectangle(width=width,height=.94,corner_radius=.12,
                       stroke_width=1.7,stroke_color=INK,fill_color=WHITE,fill_opacity=1)
    t=fit(latex_text(label,30,True),width-.45,.58).move_to(r)
    return VGroup(r,t)

def make_worksheet_table(headers, data, widths=None, cell_h=.60, size=27):
    """Native vector and LaTeX table: independent cells, rows and columns."""
    if widths is None: widths=[2.2]*len(headers)
    assert len(headers)==len(widths)
    built=[]
    for i,row in enumerate([headers]+data):
        cells=[]
        assert len(row)==len(headers)
        for j,string in enumerate(row):
            rect=Rectangle(width=widths[j],height=cell_h,
                stroke_color=GRID,stroke_width=1.45,
                fill_color=PALE if i==0 else WHITE,fill_opacity=1)
            if isinstance(string,str) and string.startswith("MATH:"):
                tex=mt(string[5:], size)
            else:
                tex=latex_text(str(string),size if i else size-2,i==0)
            fit(tex,rect.width-.24,rect.height-.20)
            tex.move_to(rect)
            cells.append(VGroup(rect,tex))
        built.append(VGroup(*cells).arrange(RIGHT,buff=0))
    g=VGroup(*built).arrange(DOWN,buff=0)
    return fit(g,14.0,5.20)

class AppliedLesson(ClassroomLatex):
    """Matches V6: paper-white canvas, black/gray LaTeX, numbered headers."""
    def cover(self,caption):
        self.slide(0,f"WEEK {self.week}  |  APPLIED PROBLEM",
                   "Companion lesson: worked example, interpretation, independent check")
        heading=latex_text(caption,53,True)
        fit(heading,13.8,1.5).move_to(UP*.40)
        subtitle=mt(r"\mathrm{QUESTION}\ \longrightarrow\ \mathrm{REASONING}\ \longrightarrow\ \mathrm{EVIDENCE}",45)
        subtitle.move_to(DOWN*1.15)
        self.play(FadeIn(heading,shift=UP*.32),run_time=1.4)
        self.play(Write(subtitle),run_time=2.0)
        self.wait(2.8)

    def step(self,n,title,detail):
        self.slide(n,title,detail)

    def equation(self,expression,where=ORIGIN,size=55):
        x=mt(expression,size)
        fit(x,13.4,1.4)
        x.move_to(where)
        return x

    def prompt(self,lines,reveal,wait_time=5):
        q=text_lines(lines,34,spacing=.4)
        self.stage(q)
        self.play(LaggedStart(*[Write(i) for i in q],lag_ratio=.25),run_time=3.6)
        self.wait(wait_time)
        ans=latex_text(reveal,32,True)
        fit(ans,13.8,.75)
        ans.move_to(DOWN*2.72)
        self.play(FadeIn(ans,shift=UP*.18),run_time=1.0)
        self.wait(2.0)

# =============================================================================
# FILM 1 — two-stage research design + paired contexts + raw variability
# =============================================================================
class Stat10AppliedWeek1V7(AppliedLesson):
    week=1
    def construct(self):
        self.cover("DESIGN A STATISTICAL INVESTIGATION")

        self.step(1,"START FROM AN AUTHENTIC QUESTION",
                  "Study time for Grade 10 students: what could vary?")
        fixed=box("NOT STATISTICAL",["How many minutes","are in one hour?"],6.2,2.4)
        variable=box("STATISTICAL",["How long do Grade 10","students study at home?"],6.2,2.4)
        pair=VGroup(fixed,variable).arrange(RIGHT,buff=.55).move_to(UP*.34)
        self.play(FadeIn(fixed,shift=LEFT*.35),run_time=1.1)
        self.play(FadeIn(variable,shift=RIGHT*.35),run_time=1.1)
        a=mt("60",64).move_to([-3.45,-2.05,0])
        b=mt(r"20,\;35,\;45,\;\ldots",56).move_to([3.5,-2.05,0])
        self.play(Write(a),run_time=1.1)
        self.play(Write(b),run_time=1.7)
        self.wait(3)
        self.play(Circumscribe(variable,color=INK,buff=.12,run_time=1.5))
        self.wait(1.5)

        self.step(2,"DEFINE THE POPULATION PRECISELY",
                  "The same question can refer to a very different target group.")
        c1=box("SECTION 10A",["42 students","Defined group A"],5.5,2.65)
        c2=box("SECTION 10B",["38 students","Defined group B"],5.5,2.65)
        pair=VGroup(c1,c2).arrange(RIGHT,buff=.8).move_to(UP*.55)
        self.play(LaggedStart(GrowFromCenter(c1),GrowFromCenter(c2),lag_ratio=.4),run_time=2.4)
        total=mt(r"N=42+38=80",66).move_to(DOWN*2.0)
        self.play(TransformFromCopy(pair,total),run_time=1.7)
        self.wait(3)
        self.conclusion("Population = all students in the defined two sections.")

        self.step(3,"SHOW THE SUBSET, NOT JUST THE NUMBERS",
                  "Twelve fictional observations from a target of eighty.")
        pop=unit_grid(n=80,columns=10,r=.12,gapx=.46,gapy=.45).move_to(LEFT*3.45+DOWN*.13)
        selected=[1,6,10,15,26,31,40,44,49,57,65,72]
        self.play(LaggedStart(*[GrowFromCenter(d) for d in pop],lag_ratio=.009),run_time=2.7)
        self.play(LaggedStart(*[pop[i].animate.set_fill(INK,opacity=1) for i in selected],lag_ratio=.09),run_time=2.0)
        clones=VGroup(*[pop[i].copy() for i in selected])
        self.add(clones)
        target=unit_grid(n=12,columns=4,r=.21,gapx=.72,gapy=.72).move_to(RIGHT*3.4+DOWN*.20)
        self.play(Transform(clones,target),run_time=2.5)
        n1=mt(r"N=80",52).move_to([-3.4,2.0,0])
        n2=mt(r"n=12",52).move_to([3.4,2.0,0])
        self.play(Write(VGroup(n1,n2)),run_time=1.2)
        rule=mt(r"12<80,\quad S\subset P",47).move_to(DOWN*2.75)
        self.play(Write(rule),run_time=1.5)
        self.wait(2.8)

        self.step(4,"COMPARE TWO SECTIONS",
                  "The sample may contain observations from both sections.")
        table=make_worksheet_table(
            ["Group","Population","In sample"],
            [["10A","42","6"],["10B","38","6"],["Total","80","12"]],
            widths=[3.6,3.6,3.6],cell_h=.73,size=32)
        table.move_to(UP*.27)
        self.play(LaggedStart(*[FadeIn(row,shift=RIGHT*.22) for row in table],lag_ratio=.22),run_time=2.8)
        rule=mt(r"n_A+n_B=6+6=12",54).move_to(DOWN*2.27)
        self.play(Write(rule),run_time=1.6)
        self.conclusion("Knowing the sample size alone does not prove fairness.")

        self.step(5,"OBSERVE THE ANSWERS VARIATION",
                  "The 12 invented daily study times are measurements in minutes.")
        axis=NumberLine(x_range=[0,80,10],length=12.5,include_numbers=True,
                        label_direction=DOWN,color=INK).move_to(DOWN*.42)
        caption=latex_text("Study time per day (minutes)",38,True).move_to(UP*1.8)
        self.play(FadeIn(caption),Create(axis),run_time=1.8)
        rows=[0]*len(READING)
        seen={}
        for i,v in enumerate(READING):
            rows[i]=seen.get(v,0)
            seen[v]=rows[i]+1
        dots=VGroup(*[Dot(axis.n2p(v)+UP*(.19+.3*rows[i]),radius=.16,color=INK)
                     for i,v in enumerate(READING)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],lag_ratio=.11),run_time=2.8)
        self.wait(2.4)
        endpoint=VGroup(SurroundingRectangle(dots[0],buff=.15,color=INK),
                         SurroundingRectangle(dots[-1],buff=.15,color=INK))
        self.play(Create(endpoint),run_time=1.1)
        self.conclusion("Individual responses differ: variability is visible.")

        self.step(6,"WHAT CAN THESE OBSERVATIONS SUPPORT?",
                  "Distinguish what the sample shows from a population conclusion.")
        good=box("SUPPORTED",["The 12 observed","times are not identical"],6.0,2.85)
        caution=box("NOT ESTABLISHED",["Every Grade 10 student","studies the same amount"],6.0,2.85)
        group=VGroup(good,caution).arrange(RIGHT,buff=.58).move_to(DOWN*.10)
        self.play(FadeIn(good,shift=LEFT*.25),run_time=1.2)
        self.play(FadeIn(caution,shift=RIGHT*.25),run_time=1.2)
        self.play(Circumscribe(good,color=INK,run_time=1.4))
        self.conclusion("A sample is evidence, not the entire population.")

        self.step(7,"CLASSROOM CHALLENGE",
                  "Build a different statistical investigation.")
        self.prompt(["1. Propose a question with varying answers.",
                     "2. Define exactly who belongs to the population.",
                     "3. Identify a sample that is a subset.",
                     "4. Write one conclusion you cannot justify yet."],
                    "Explain your choices, not just the values.",6)

# =============================================================================
# FILM 2 — representative coverage / proportional allocation / wording
# =============================================================================
class Stat10AppliedWeek2V7(AppliedLesson):
    week=2
    def construct(self):
        self.cover("WHO SHOULD WE ASK?")

        self.step(1,"A SCHOOL STUDY WITH TWO SCHEDULES",
                  "Survey target: 120 students across two attendance schedules.")
        morning=box("MORNING",["80 enrolled students","One part of the population"],5.75,2.4)
        evening=box("AFTERNOON",["40 enrolled students","The other part"],5.75,2.4)
        grp=VGroup(morning,evening).arrange(RIGHT,buff=.75).move_to(UP*.42)
        self.play(LaggedStart(GrowFromCenter(morning),GrowFromCenter(evening),lag_ratio=.35),run_time=2.5)
        eq=mt(r"N=80+40=120",67).move_to(DOWN*2.0)
        self.play(Write(eq),run_time=1.6)
        self.wait(3)

        self.step(2,"SEE THE POPULATION COMPOSITION",
                  "Each rectangle has width proportional to its number of students.")
        left=Rectangle(width=7.2,height=1.65,stroke_color=INK,fill_color=PALE,fill_opacity=1)
        right=Rectangle(width=3.6,height=1.65,stroke_color=INK,fill_color=WHITE,fill_opacity=1)
        blocks=VGroup(left,right).arrange(RIGHT,buff=0).move_to(UP*.10)
        lbl=VGroup(mt("80",60).move_to(left),mt("40",60).move_to(right))
        legend=VGroup(latex_text("Morning",32),latex_text("Afternoon",32))
        legend[0].next_to(left,DOWN,buff=.45);legend[1].next_to(right,DOWN,buff=.45)
        self.play(GrowFromEdge(left,LEFT),GrowFromEdge(right,LEFT),run_time=2.2)
        self.play(Write(lbl),FadeIn(legend),run_time=1.2)
        ratios=mt(r"\frac{80}{120}=\frac23,\quad\frac{40}{120}=\frac13",56).move_to(DOWN*2.35)
        self.play(Write(ratios),run_time=2.5)
        self.wait(2.6)

        self.step(3,"PLAN A: CONVENIENCE SELECTION",
                  "24 responses, all gathered from the morning schedule.")
        table=make_worksheet_table(["Schedule","Population","Responses"],
                     [["Morning","80","24"],["Afternoon","40","0"],["Total","120","24"]],
                     widths=[3.9,3.2,3.5],cell_h=.77,size=31)
        table.move_to(UP*.36)
        self.play(LaggedStart(*[FadeIn(r,shift=LEFT*.21) for r in table],lag_ratio=.2),run_time=2.7)
        missing=SurroundingRectangle(table[2][2],color=INK,stroke_width=3,buff=.12)
        self.play(Create(missing),run_time=1.0)
        self.wait(2.0)
        self.conclusion("Forty students have zero chance to appear in Plan A.")

        self.step(4,"PLAN B: PROPORTIONAL COVERAGE",
                  "Allocate 24 responses following the two schedule sizes.")
        expr1=mt(r"n_M=24\cdot\frac{80}{120}=16",55)
        expr2=mt(r"n_A=24\cdot\frac{40}{120}=8",55)
        expr3=mt(r"n_M+n_A=16+8=24",55)
        column=center_group(expr1,expr2,expr3,gap=.6,y=-.1)
        self.play(Write(expr1),run_time=2.2)
        self.wait(.8)
        self.play(Write(expr2),run_time=2.2)
        self.wait(.8)
        self.play(Write(expr3),run_time=1.9)
        self.wait(2.2)
        self.play(Indicate(expr3,scale_factor=1.08,color=SECONDARY),run_time=1.1)

        self.step(5,"COMPARE THE TWO PLANS",
                  "Proportional allocation improves schedule coverage.")
        table=make_worksheet_table(["Schedule","Population","Plan A","Plan B"],
                  [["Morning","80","24","16"],["Afternoon","40","0","8"],["Total","120","24","24"]],
                  widths=[3.3,2.6,2.5,2.5],cell_h=.74,size=30)
        table.move_to(UP*.26)
        self.play(LaggedStart(*[FadeIn(r,shift=UP*.22) for r in table],lag_ratio=.22),run_time=2.7)
        highlight=SurroundingRectangle(VGroup(*[row[3] for row in table[1:]]),color=INK,buff=.07,stroke_width=3)
        self.play(Create(highlight),run_time=1.3)
        self.conclusion("Proportional does not automatically mean unbiased.")

        self.step(6,"METHOD AND QUESTION WORDING MATTER",
                  "Collect the same variable without nudging the answer.")
        bad=box("LEADING WORDING",["Is our excellent bus","service your favorite?"],6.15,2.7)
        good=box("NEUTRAL WORDING",["How do you usually","travel to school?"],6.15,2.7)
        cards=VGroup(bad,good).arrange(RIGHT,buff=.55).move_to(DOWN*.08)
        self.play(FadeIn(bad,shift=LEFT*.22),run_time=1.15)
        self.play(FadeIn(good,shift=RIGHT*.22),run_time=1.15)
        self.wait(2)
        self.play(Circumscribe(good,color=INK,run_time=1.5))
        self.conclusion("A good sample with a poor question may still mislead.")

        self.step(7,"DESIGN A BETTER INVESTIGATION",
                  "Apply the sampling and data-collection criteria together.")
        self.prompt(["1. State the population and observational unit.",
                     "2. Calculate the 16 + 8 allocation.",
                     "3. Choose survey or observation, with a reason.",
                     "4. Identify one remaining source of bias."],
                    "Good design requires both coverage and careful measurement.",6)

# =============================================================================
# FILM 3 — unit vs variable vs recorded value, same number / different meaning
# =============================================================================
class Stat10AppliedWeek3V7(AppliedLesson):
    week=3
    def construct(self):
        self.cover("READ A REALISTIC DATASET")

        self.step(1,"ONE UNIT, SEVERAL CHARACTERISTICS",
                  "Fictional record: each row is one observational unit.")
        sample=make_worksheet_table(["Student ID","Travel mode","Minutes","Siblings"],
                    [["S01","Bus","18.4","2"]],
                    widths=[2.5,3.6,3.0,2.8],cell_h=1.05,size=33)
        sample.move_to(UP*.35)
        self.play(FadeIn(sample,shift=UP*.3),run_time=1.6)
        highlight=SurroundingRectangle(sample[1],color=INK,stroke_width=3,buff=.1)
        self.play(Create(highlight),run_time=1.0)
        self.wait(2)
        concept=mt(r"\mathrm{UNIT}\ \longrightarrow\ \mathrm{VARIABLE}\ \longrightarrow\ \mathrm{VALUE}",50).move_to(DOWN*2.1)
        self.play(Write(concept),run_time=2.1)
        self.wait(2)

        self.step(2,"READ ALL SIX OBSERVATIONS",
                  "Anonymized, fictional records allow multiple variable types.")
        table=raw_table().move_to(DOWN*.23)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.18) for r in table],lag_ratio=.23),run_time=3.1)
        self.wait(2)
        for idx in [1,2,3]:
            cells=VGroup(*[row[idx] for row in table])
            line=SurroundingRectangle(cells,color=INK,buff=.07,stroke_width=2.4)
            self.play(Create(line),run_time=.65)
            self.wait(.75)
            self.play(FadeOut(line),run_time=.35)

        self.step(3,"TWO VARIABLES WITH DIFFERENT MEANINGS",
                  "Ask what the values describe, not what they look like.")
        cat=box("TRAVEL MODE",["Bus, Walk, Bike, Car","Qualitative categories"],6.2,2.9)
        qty=box("TRAVEL TIME",["18.4, 12.3, 9.7 ...","Quantitative amounts"],6.2,2.9)
        pair=VGroup(cat,qty).arrange(RIGHT,buff=.62).move_to(UP*.02)
        self.play(FadeIn(cat,shift=LEFT*.33),run_time=1.3)
        self.play(FadeIn(qty,shift=RIGHT*.33),run_time=1.3)
        arrows=mt(r"\mathrm{TYPE}\neq\mathrm{APPEARANCE}",47).move_to(DOWN*2.45)
        self.play(Write(arrows),run_time=1.8)
        self.wait(2)

        self.step(4,"WHY DIGITS CAN BE CATEGORIES",
                  "Route number 12 is a code, not twelve measured buses.")
        numeral=mt("12",108).move_to(UP*.76)
        self.play(GrowFromCenter(numeral),run_time=1.5)
        left=box("ROUTE 12",["Identifier","Qualitative"],5.8,2.25)
        right=box("12 SIBLINGS",["A number counted","Quantitative"],5.8,2.25)
        pair=VGroup(left,right).arrange(RIGHT,buff=.9).move_to(DOWN*1.45)
        self.play(TransformFromCopy(numeral,left),TransformFromCopy(numeral,right),run_time=2.0)
        self.wait(2.2)
        self.play(Circumscribe(left,color=INK,run_time=1.2))
        self.play(Circumscribe(right,color=INK,run_time=1.2))
        self.wait(1.2)

        self.step(5,"IDENTIFIERS AND MEASUREMENTS",
                  "Never confuse an ID column with the study's measured variable.")
        table=make_worksheet_table(["Field","Observed value","Interpretation"],
                  [["Student code","S01","Identifier"],
                   ["Route code","12","Category"],
                   ["Travel time","18.4 min","Amount"],
                   ["Siblings","2","Amount"]],
                   widths=[3.25,3.45,4.1],cell_h=.71,size=28)
        table.move_to(UP*.15)
        self.play(LaggedStart(*[FadeIn(r,shift=UP*.12) for r in table],lag_ratio=.23),run_time=3)
        self.wait(2.5)
        note=latex_text("An identifier distinguishes records; it is not a measured outcome.",29,True)
        fit(note,13.5,.75).move_to(DOWN*2.6)
        self.play(Write(note),run_time=1.7)
        self.wait(1.7)

        self.step(6,"A MORE DIFFICULT BORDERLINE CASE",
                  "A score on a 1--5 preference scale may encode ordered categories.")
        score=mt(r"1,\;2,\;3,\;4,\;5",75).move_to(UP*.85)
        under=latex_text("Ordered response levels, not necessarily measured amounts.",37,True).move_to(DOWN*.48)
        fit(under,13.6,.8)
        self.play(Write(score),run_time=2.2)
        self.play(FadeIn(under,shift=UP*.14),run_time=1.3)
        self.wait(3)
        self.conclusion("The coding scheme and question determine the variable type.")

        self.step(7,"CLASSIFY FIVE FIELDS",
                  "Give a reason for every answer.")
        self.prompt(["1. Favorite sport and preferred route number",
                     "2. Number of siblings and travel duration",
                     "3. A coded satisfaction level from 1 to 5",
                     "4. Explain why the student ID is a separate field."],
                    "Categories and numerical amounts require different interpretations.",6)

# =============================================================================
# FILM 4 — complete variable classification + precision + raw data protocol
# =============================================================================
class Stat10AppliedWeek4V7(AppliedLesson):
    week=4
    def construct(self):
        self.cover("CLASSIFY AND RECORD OBSERVATIONS")

        self.step(1,"BUILD THE DECISION TREE",
                  "Choose a category, count, or measured quantity.")
        parent=pointer_note("What does the observed value represent?",10.6).move_to(UP*1.65)
        cat=box("CATEGORY OR CODE",["Qualitative","Examples: route, ID"],5.5,2.2).move_to(LEFT*3.35+DOWN*.9)
        num=box("NUMERICAL AMOUNT",["Quantitative","Count or measurement"],5.5,2.2).move_to(RIGHT*3.35+DOWN*.9)
        self.play(GrowFromCenter(parent),run_time=1.2)
        connectors=VGroup(Line(parent.get_bottom(),cat.get_top(),color=INK),
                          Line(parent.get_bottom(),num.get_top(),color=INK))
        self.play(Create(connectors),run_time=1.2)
        self.play(LaggedStart(FadeIn(cat),FadeIn(num),lag_ratio=.5),run_time=2.3)
        self.wait(3)

        self.step(2,"DISCRETE: VALUES YOU COUNT",
                  "Number of siblings in six fictional records.")
        values=mt(r"2,\;1,\;0,\;3,\;2,\;1",60).move_to(UP*1.7)
        self.play(Write(values),run_time=1.8)
        points=VGroup()
        for k in range(4):
            pile=VGroup(*[Dot(radius=.16,color=INK) for i in range(k)])
            if k==0:
                frame=Circle(radius=.18,color=GRID,stroke_width=2)
                pile.add(frame)
            else:
                pile.arrange(UP,buff=.10)
            pile.move_to([-4.2+k*2.8,-.45,0])
            points.add(pile)
        labels=VGroup(*[mt(str(k),38).move_to([-4.2+k*2.8,-2.05,0]) for k in range(4)])
        self.play(LaggedStart(*[FadeIn(p,shift=UP*.25) for p in points],lag_ratio=.25),run_time=2.2)
        self.play(Write(labels),run_time=1.3)
        self.conclusion("No individual can have 1.5 siblings in this counting task.")

        self.step(3,"CONTINUOUS: QUANTITIES YOU MEASURE",
                  "Travel duration can lie between recorded whole minutes.")
        line=NumberLine(x_range=[0,30,5],length=12.2,include_numbers=True,
                label_direction=DOWN,color=INK).move_to(DOWN*.24)
        marker=Dot(line.n2p(0),radius=.16,color=INK)
        target=18.4
        self.play(Create(line),FadeIn(marker),run_time=1.8)
        self.play(marker.animate.move_to(line.n2p(target)),run_time=3.2,rate_func=smooth)
        annotation=mt(r"t=18.4\ \mathrm{min}",68).move_to(UP*1.55)
        self.play(Write(annotation),run_time=1.7)
        self.wait(2)
        self.play(Indicate(marker,scale_factor=1.7,color=SECONDARY),run_time=1.1)
        self.conclusion("A clock measurement approximates an underlying duration.")

        self.step(4,"WHY ROUNDING DOES NOT CHANGE TYPE",
                  "A measured value can be reported with fewer decimals.")
        eq=mt(r"18.4\ \mathrm{min}\ \approx\ 18\ \mathrm{min}",74)
        eq.move_to(UP*.35)
        self.play(Write(eq),run_time=2.1)
        note=box("IMPORTANT",["Rounded time stays continuous.","A rounded integer need not be a count."],10.8,2.2)
        note.move_to(DOWN*1.72)
        self.play(FadeIn(note,shift=UP*.2),run_time=1.5)
        self.wait(3.5)

        self.step(5,"FOUR NUMBERS; FOUR DIFFERENT ROLES",
                  "The meaning comes from how each observation was defined.")
        table=make_worksheet_table(["Observation","Meaning","Classification"],
                  [["Bus route 12","Code","Qualitative"],
                   ["Two siblings","Count","Quant. discrete"],
                   ["Time 18.4 min","Duration","Quant. continuous"],
                   ["Satisfaction 5","Ordered level","Qualitative ordinal"]],
                  widths=[4.0,3.15,4.25],cell_h=.72,size=28)
        table.move_to(UP*.07)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*.1) for r in table],lag_ratio=.22),run_time=3.0)
        self.wait(3.1)
        self.conclusion("A digit does not determine the statistical variable type.")

        self.step(6,"CONSTRUCT THE RAW-DATA RECORD",
                  "Six anonymous observations; one unit per row.")
        table=raw_table().move_to(DOWN*.14)
        self.play(LaggedStart(*[FadeIn(r,shift=UP*.13) for r in table],lag_ratio=.24),run_time=3.0)
        self.wait(2.0)
        for col in (1,2,3):
            cells=VGroup(*[row[col] for row in table])
            rect=SurroundingRectangle(cells,buff=.05,color=INK,stroke_width=2.5)
            self.play(Create(rect),run_time=.55)
            self.wait(.6)
            self.play(FadeOut(rect),run_time=.3)
        self.conclusion("Record values first; frequency tables come in later lessons.")

        self.step(7,"CHECK COMPLETENESS BEFORE GRAPHING",
                  "This class prepares clean observations, not grouped statistics.")
        notes=center_group(
            latex_text("Is each observational unit recorded exactly once?",34,True),
            latex_text("Do the columns have clear units and categories?",34,True),
            latex_text("Can another person reproduce each classification?",34,True),
            gap=.55,y=.0)
        self.play(LaggedStart(*[FadeIn(i,shift=LEFT*.22) for i in notes],
               lag_ratio=.3),run_time=3.3)
        self.wait(3)
        self.conclusion("Clear records prevent ambiguous interpretation.")

        self.step(8,"FINAL MULTI-STEP CHALLENGE",
                  "Propose, justify, record.")
        self.prompt(["1. Create a school study with four variables.",
                     "2. Include one category, one count, one measurement.",
                     "3. Add a numerical code that is NOT a quantity.",
                     "4. Record two invented observations, with units."],
                     "Do not construct a frequency table or a graph yet.",7)
