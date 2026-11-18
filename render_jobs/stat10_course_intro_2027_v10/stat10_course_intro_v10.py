# -*- coding: utf-8 -*-
"""STATISTICS 10 | 2027 COURSE OPENING FILM V10 | Native ManimCE v0.20.1

Annual roadmap source: IJR Grade-10 Statistics 2026 curriculum (Periods I-III).
The *only* confirmed 2027 timetable source here is Statistics_10_2027_P1.docx,
This film presents the 2026 thematic map as the annual reference for 2027.
It does not claim unverified weekly scheduling.

Design inheritance: V6/V7/V8 classroom white/black, real LaTeX, 16:9,
numbered headers and vector-based temporal transformations.
All examples are fictional and use no personal data.

Native commands:
  manim -ql stat10_course_intro_v10.py Statistics10CourseIntroV10
  manim -qh stat10_course_intro_v10.py Statistics10CourseIntroV10
"""
from __future__ import annotations
import sys
from collections import Counter
from pathlib import Path
import numpy as np
from manim import *

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"stat10_2027_native_v6"))
sys.path.insert(0,str(HERE.parent/"stat10_2027_v8"))
from statistics10_latex_v6 import (
    ClassroomLatex, INK, GRID, PALE, SECONDARY, latex_text, fit, box
)
from stat10_guided_v8_common import table as classroom_table, dot_matrix

config.pixel_width=1920
config.pixel_height=1080
config.frame_width=16
config.frame_height=9
config.frame_rate=30
config.background_color=WHITE

RAW_TRANSPORT=("Bus","Walk","Bike","Car","Walk","Bus",
               "Bike","Bus","Walk","Car","Bus","Bike")
FREQ={"Bus":4, "Walk":3, "Bike":3, "Car":2}
GROUPED_TIME=(8,10,11,13,14,15,16,17,18,20,22,24)
CENTRE=(4,6,6,8,11)
SPREAD_A=(6,7,8,9,10)
SPREAD_B=(2,5,8,11,14)
BOX_VALUES=(2,4,6,8,10,12,14,16,18)
assert len(RAW_TRANSPORT)==len(GROUPED_TIME)==12
assert Counter(RAW_TRANSPORT)==FREQ
assert sum(FREQ.values())==12
assert len([x for x in GROUPED_TIME if 0<=x<10])==1
assert len([x for x in GROUPED_TIME if 10<=x<20])==8
assert len([x for x in GROUPED_TIME if 20<=x<30])==3
assert np.mean(CENTRE)==7 and np.median(CENTRE)==6 and Counter(CENTRE)[6]==2
assert np.mean(SPREAD_A)==np.mean(SPREAD_B)==8
assert max(SPREAD_A)-min(SPREAD_A)==4
assert max(SPREAD_B)-min(SPREAD_B)==12
assert np.median(BOX_VALUES)==10 and (4+6)/2==5 and (14+16)/2==15

def tx(content,size=34,bold=False):
    return latex_text(content,size,bold)

def mx(latex,size=52):
    return MathTex(latex,font_size=size,color=INK)

def caption(content,y=-2.84,size=32):
    t=tx(content,size,True)
    fit(t,13.8,.72)
    t.move_to([0,y,0])
    return t

def label_above(textual,obj,size=26,gap=.23):
    l=tx(textual,size,True)
    fit(l,obj.width+.8,.58)
    l.next_to(obj,UP,buff=gap)
    return l

class Statistics10CourseIntroV10(ClassroomLatex):
    week=0

    def slide(self,number,title,subtitle):
        # Recreate the existing consolidated V6 classroom header but replace
        # "WEEK 00" with "COURSE INTRODUCTION".
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.48)
        self.camera.frame.set(width=16).move_to(ORIGIN)
        eyebrow=tx("STATISTICS 10  /  2027  /  COURSE INTRODUCTION",21,True)
        eyebrow.to_corner(UL,buff=.38).shift(RIGHT*.35)
        heading=tx(title,44,True)
        fit(heading,14.5,1.0)
        heading.move_to([-7.14,3.42,0],aligned_edge=LEFT)
        subtitle=tx(subtitle,26)
        fit(subtitle,14.2,.75)
        subtitle.move_to([-7.12,2.82,0],aligned_edge=LEFT)
        rule=Line([-7.3,2.52,0],[7.3,2.52,0],color=GRID,stroke_width=2)
        page=tx(f"{number:02d}",25,True).to_corner(DR,buff=.40)
        self.play(FadeIn(eyebrow,shift=RIGHT*.15),
                  FadeIn(heading,shift=UP*.1),FadeIn(subtitle),
                  Create(rule),FadeIn(page),run_time=.92)

    def note(self,s,hold=1.8,y=-2.90):
        obj=caption(s,y=y)
        self.play(FadeIn(obj,shift=UP*.16),run_time=.95)
        self.wait(hold)
        return obj

    def construct(self):
        self.opening()
        self.annual_overview()
        self.investigation()
        self.population_sample()
        self.period_one_topics()
        self.variable_types()
        self.frequencies()
        self.graphs()
        self.grouped_intervals()
        self.period_two()
        self.dispersion()
        self.period_three()
        self.normal_distribution()
        self.closing()

    def opening(self):
        self.slide(0,"STATISTICS 10","Course introduction | Three periods | One way to reason with data")
        cover=tx("FROM DATA TO DECISIONS",65,True).move_to([0,.55,0])
        fit(cover,13.6,1.3)
        path=mx(r"\mathrm{QUESTION}\longrightarrow\mathrm{EVIDENCE}",59)
        path.move_to([0,-.83,0])
        dashes=VGroup(*[Dot([x,-1.95,0],radius=.055,color=INK) for x in
                        np.linspace(-5,5,29)])
        self.play(Write(cover),run_time=2.1)
        self.play(Write(path),run_time=2.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dashes],
                   lag_ratio=.02),run_time=1.4)
        self.wait(2.2)

    def annual_overview(self):
        self.slide(1,"THREE PERIODS. ONE BIG PICTURE.",
                   "Annual thematic roadmap based on the IJR Grade 10 curriculum.")
        titles=("PERIOD I","PERIOD II","PERIOD III")
        lines=(["Gather and","organize data"],
               ["Describe center","and variability"],
               ["Locate, compare","and interpret"])
        cards=VGroup(*[box(t,b,width=4.20,height=2.75)
                       for t,b in zip(titles,lines)])
        cards.arrange(RIGHT,buff=.54).move_to([0,.40,0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cards],
                  lag_ratio=.35),run_time=3.15)
        arrows=VGroup(*[Arrow(cards[i].get_right()+RIGHT*.02,
                               cards[i+1].get_left()+LEFT*.02,
                               color=INK,stroke_width=2.8,
                               buff=.02,max_tip_length_to_length_ratio=.24)
                       for i in range(2)])
        self.play(*[GrowArrow(a) for a in arrows],run_time=1.3)
        for card in cards:
            self.play(Indicate(card,scale_factor=1.035,color=SECONDARY),
                      run_time=.72)
        self.note("Collect  /  Describe  /  Interpret",hold=2.5)

    def investigation(self):
        self.slide(2,"STATISTICS BEGINS WITH A QUESTION",
                   "How do students travel to school? The answers are not identical.")
        question=tx("How do students travel to school?",41,True)
        question.move_to([0,1.95,0])
        vals=[tx(t,30,True) for t in ("Bus","Walk","Bike","Car")]
        terms=VGroup(*vals).arrange(RIGHT,buff=.85).move_to([0,.02,0])
        self.play(Write(question),run_time=1.9)
        self.play(LaggedStart(*[FadeIn(t,shift=DOWN*.3) for t in terms],
                   lag_ratio=.25),run_time=2.45)
        group=VGroup(*[Dot(radius=.13,color=INK) for _ in range(12)])
        group.arrange_in_grid(rows=2,cols=6,buff=(.34,.30)).move_to([0,-1.48,0])
        self.play(LaggedStart(*[GrowFromCenter(x) for x in group],
                   lag_ratio=.06),run_time=1.8)
        self.note("The question determines which observations we need.")

    def population_sample(self):
        self.slide(3,"PERIOD I  /  WHO DO WE STUDY?",
                   "Population, sample, observational unit and data collection.")
        pop=dot_matrix(60,columns=10,radius=.12,sx=.46,sy=.49).move_to([-3.25,-.12,0])
        inds=[1,4,11,15,21,27,31,34,41,45,52,58]
        self.play(LaggedStart(*[GrowFromCenter(x) for x in pop],
                  lag_ratio=.018),run_time=2.7)
        self.play(LaggedStart(*[pop[i].animate.set_fill(INK,opacity=1)
                              for i in inds],lag_ratio=.085),run_time=2.1)
        targets=dot_matrix(12,columns=4,radius=.20,sx=.64,sy=.68).move_to([3.4,-.18,0])
        moving=VGroup(*[pop[i].copy() for i in inds])
        self.add(moving)
        self.play(Transform(moving,targets),run_time=2.4,rate_func=smooth)
        labels=VGroup(mx(r"N=60",52).move_to([-3.25,1.96,0]),
                      mx(r"n=12",52).move_to([3.4,1.96,0]))
        self.play(Write(labels),run_time=1.2)
        self.note("A statistical conclusion must name the group it describes.")

    def period_one_topics(self):
        self.slide(4,"PERIOD I  /  THE TOOLKIT",
                   "Collect observations, classify data, construct tables and graphs.")
        left=VGroup(*[tx(s,31) for s in [
            "1. Population, sample and variables",
            "2. Qualitative and quantitative data",
            "3. Absolute and relative frequencies",
            "4. Cumulative frequencies",
        ]]).arrange(DOWN,aligned_edge=LEFT,buff=.35)
        right=VGroup(*[tx(s,31) for s in [
            "5. Grouped and ungrouped tables",
            "6. Class intervals and midpoints",
            "7. Bar, histogram, pie and polygon",
            "8. Read and compare representations",
        ]]).arrange(DOWN,aligned_edge=LEFT,buff=.35)
        left.move_to([-3.55,-.15,0])
        right.move_to([3.57,-.15,0])
        fit(left,6.75,4.9)
        fit(right,6.75,4.9)
        self.play(LaggedStart(*[FadeIn(l,shift=RIGHT*.22) for l in left],
                lag_ratio=.18),run_time=2.8)
        self.play(LaggedStart(*[FadeIn(l,shift=RIGHT*.22) for l in right],
                lag_ratio=.18),run_time=2.8)
        self.wait(2.6)

    def variable_types(self):
        self.slide(5,"WHAT KIND OF DATA DO WE RECORD?",
                   "A number may describe a count, a measurement or a label.")
        c=VGroup(
           box("TRAVEL MODE",["Bus / Walk / Bike","Qualitative"],width=4.2,height=2.6),
           box("SIBLINGS",["0 / 1 / 2 / 3","Quantitative count"],width=4.2,height=2.6),
           box("TRAVEL TIME",["12.4 / 18.6 min","Quantitative measure"],width=4.2,height=2.6)
        ).arrange(RIGHT,buff=.52).move_to([0,.20,0])
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.32) for x in c],
                  lag_ratio=.4),run_time=3.1)
        eq=mx(r"\mathrm{TYPE}\ \neq\ \mathrm{APPEARANCE}",57).move_to([0,-2.18,0])
        self.play(Write(eq),run_time=2)
        self.wait(2.2)

    def frequencies(self):
        self.slide(6,"FROM RAW DATA TO A FREQUENCY TABLE",
                   "Count observations, then compute proportions.")
        raw=tx("Bus, Walk, Bike, Car, Walk, Bus, Bike, Bus, Walk, Car, Bus, Bike",27)
        fit(raw,14.15,.65)
        raw.move_to([0,1.95,0])
        self.play(Write(raw),run_time=2.6)
        data=[["Bus","4","4/12"],
              ["Walk","3","3/12"],
              ["Bike","3","3/12"],
              ["Car","2","2/12"],
              ["TOTAL","12","1"]]
        tab=classroom_table(["Category","Frequency","Relative frequency"],
                data,widths=[3.3,3.4,4.2],height=.62,fontsize=29)
        tab.move_to([0,-.25,0])
        self.play(LaggedStart(*[FadeIn(r,shift=UP*.15) for r in tab],
                    lag_ratio=.27),run_time=3.9)
        outline=SurroundingRectangle(tab[-1],color=INK,stroke_width=2.8,buff=.06)
        self.play(Create(outline),run_time=1.05)
        self.note("A valid frequency table accounts for every observation.",hold=2)

    def graphs(self):
        self.slide(7,"ONE DATASET. MULTIPLE GRAPHS.",
                   "Bar charts, histograms, pie charts and frequency polygons.")
        x0=-4.5
        baseline=-1.75
        widths=.95
        heights=[2.6,1.95,1.95,1.3]
        labels=["Bus","Walk","Bike","Car"]
        vals=[4,3,3,2]
        bars=VGroup()
        names=VGroup()
        for i,(h,name,v) in enumerate(zip(heights,labels,vals)):
            rect=Rectangle(width=widths,height=h,stroke_width=2,
                     stroke_color=INK,fill_color=PALE,
                     fill_opacity=1)
            rect.move_to([x0+i*2.65,baseline+h/2,0])
            bars.add(rect)
            names.add(tx(name,28,True).move_to([x0+i*2.65,baseline-.36,0]))
        self.play(LaggedStart(*[GrowFromEdge(r,DOWN) for r in bars],
                  lag_ratio=.23),run_time=2.8)
        self.play(FadeIn(names,shift=UP*.12),run_time=.9)
        labels_count=VGroup(*[mx(str(v),40).next_to(b,UP,buff=.20)
                              for v,b in zip(vals,bars)])
        self.play(LaggedStart(*[Write(k) for k in labels_count],
                  lag_ratio=.18),run_time=1.6)
        self.wait(1.4)
        self.play(Indicate(bars,scale_factor=1.015,color=SECONDARY),run_time=1.1)
        self.note("Choose the graph based on the type of variable.",hold=2)

    def grouped_intervals(self):
        self.slide(8,"NUMERIC DATA MAY NEED CLASS INTERVALS",
                   "Range, class width, lower and upper limits, and class marks.")
        intervals=classroom_table(["Interval (min)","Class mark","Frequency"],
            [["[0,10)","5","1"],["[10,20)","15","8"],["[20,30)","25","3"],["Total","", "12"]],
            widths=[2.85,2.2,2.25],height=.72,fontsize=30)
        intervals.move_to([-3.55,-.15,0])
        self.play(LaggedStart(*[FadeIn(r,shift=LEFT*.2) for r in intervals],
                lag_ratio=.25),run_time=3.0)
        base_x=3.25; y0=-1.72; width=.88
        hist=VGroup()
        for i,n in enumerate([1,8,3]):
            h=n*.36
            r=Rectangle(width=width,height=h,stroke_color=INK,
              stroke_width=1.8,fill_color=PALE,fill_opacity=1)
            r.move_to([base_x+i*width,y0+h/2,0])
            hist.add(r)
        self.play(LaggedStart(*[GrowFromEdge(h,DOWN) for h in hist],
                  lag_ratio=.32),run_time=2.5)
        self.note("An interval groups values without losing the total.",hold=2.2)

    def period_two(self):
        self.slide(9,"PERIOD II  /  WHERE IS THE CENTER?",
                   "Mean, median and mode for grouped and ungrouped data.")
        values=mx(r"4\qquad6\qquad6\qquad8\qquad11",67)
        values.move_to([0,1.42,0])
        self.play(Write(values),run_time=2.5)
        means=VGroup(
           mx(r"\overline{x}=\frac{4+6+6+8+11}{5}=7",53),
           mx(r"\mathrm{Median}=6",50),
           mx(r"\mathrm{Mode}=6",50)
        ).arrange(DOWN,buff=.31)
        means.move_to([0,-.74,0])
        self.play(LaggedStart(*[Write(m) for m in means],lag_ratio=.32),
                  run_time=4)
        self.note("Different measures answer different questions.",hold=2.1)

    def dispersion(self):
        self.slide(10,"PERIOD II  /  HOW SPREAD OUT?",
                   "Range, variance, standard deviation and coefficient of variation.")
        nline1=NumberLine(x_range=[0,16,2],length=11,include_numbers=True,
                   label_direction=DOWN,color=INK)
        nline1.move_to([0,.80,0])
        nline2=nline1.copy().move_to([0,-1.53,0])
        a=VGroup(*[Dot(nline1.n2p(v),radius=.14,color=INK) for v in SPREAD_A])
        b=VGroup(*[Dot(nline2.n2p(v),radius=.14,color=INK) for v in SPREAD_B])
        names=VGroup(tx("A  /  tightly grouped",28,True).move_to([0,1.84,0]),
                     tx("B  /  spread out",28,True).move_to([0,-.53,0]))
        self.play(Create(nline1),Create(nline2),FadeIn(names),run_time=2.1)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in a],
                  lag_ratio=.16),run_time=1.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in b],
                  lag_ratio=.16),run_time=1.5)
        eq=mx(r"\overline{x}_A=\overline{x}_B=8,\quad R_A=4,\quad R_B=12",46)
        eq.move_to([0,-2.80,0])
        self.play(Write(eq),run_time=2.1)
        self.wait(3)

    def period_three(self):
        """Faithful V9 replacement: one coherent axis, one scale, and IQR."""
        self.slide(11, "PERIOD III  /  QUARTILES AND IQR",
                   "Sorted observations, the five-number summary, and the interquartile range.")

        # Fixed, auditable nine-observation example. Quartile convention:
        # exclude the overall median when taking medians of the two halves.
        values = tuple(sorted(BOX_VALUES))
        assert values == (2, 4, 6, 8, 10, 12, 14, 16, 18)
        min_v, q1, q2, q3, max_v = (2, 5, 10, 15, 18)
        assert np.median(values) == q2
        assert (values[1]+values[2])/2 == q1
        assert (values[6]+values[7])/2 == q3
        assert q3 - q1 == 10

        ordered = mx(r"2,\;4,\;6,\;8,\;10,\;12,\;14,\;16,\;18", 44)
        ordered.move_to([0, 2.02, 0])
        derivation = mx(
            r"Q_1=\frac{4+6}{2}=5,\quad Q_2=10,\quad Q_3=\frac{14+16}{2}=15", 40
        ).move_to([0, 1.25, 0])
        fit(derivation, 13.5, .73)
        self.play(Write(ordered), run_time=2.4)
        self.play(Write(derivation), run_time=2.9)

        # All coordinates are derived from the SAME NumberLine mapping.
        axis = NumberLine(
            x_range=[0,20,2], length=11.6, include_numbers=True,
            label_direction=DOWN, color=INK,
        ).move_to([0, -1.10, 0])
        self.play(Create(axis), run_time=1.6)

        x_min = axis.n2p(min_v)[0]
        x_q1 = axis.n2p(q1)[0]
        x_med = axis.n2p(q2)[0]
        x_q3 = axis.n2p(q3)[0]
        x_max = axis.n2p(max_v)[0]
        y_box = -.20
        half_height = .32

        left_whisker = Line([x_min,y_box,0],[x_q1,y_box,0],
                            stroke_color=INK,stroke_width=3)
        right_whisker = Line([x_q3,y_box,0],[x_max,y_box,0],
                             stroke_color=INK,stroke_width=3)
        ends = VGroup(
            Line([x_min,y_box-.16,0],[x_min,y_box+.16,0],
                 stroke_color=INK,stroke_width=3),
            Line([x_max,y_box-.16,0],[x_max,y_box+.16,0],
                 stroke_color=INK,stroke_width=3),
        )
        # Correct box: LEFT = Q1, RIGHT = Q3. Do not shift it
        # independently of the number line.
        qbox = Rectangle(
            width=x_q3-x_q1, height=2*half_height,
            stroke_color=INK, stroke_width=3,
            fill_color=PALE, fill_opacity=.86,
        )
        qbox.move_to([(x_q1+x_q3)/2,y_box,0])
        medline = Line(
            [x_med,y_box-half_height,0], [x_med,y_box+half_height,0],
            stroke_color=INK, stroke_width=3.3,
        )
        self.play(Create(left_whisker), Create(right_whisker),
                  Create(ends), run_time=1.5)
        self.play(GrowFromCenter(qbox), Create(medline), run_time=2.1)

        qlabels = VGroup()
        for x, latex in [(x_q1,r"Q_1"), (x_med,r"Q_2"), (x_q3,r"Q_3")]:
            tick = Line([x,y_box+half_height,0], [x,.55,0],
                        stroke_color=SECONDARY,stroke_width=2)
            label = mx(latex,39).move_to([x,.80,0])
            qlabels.add(VGroup(tick,label))
        self.play(LaggedStart(*[Create(mark[0]) for mark in qlabels],
                  lag_ratio=.20),run_time=1.2)
        self.play(LaggedStart(*[FadeIn(mark[1],shift=UP*.12) for mark in qlabels],
                  lag_ratio=.24),run_time=1.3)

        # A bracket spans exactly Q1 to Q3 beneath the axis.
        y_bracket = -1.89
        bracket = VGroup(
            Line([x_q1,y_bracket,0],[x_q3,y_bracket,0],
                 stroke_color=INK,stroke_width=3),
            Line([x_q1,y_bracket-.10,0],[x_q1,y_bracket+.10,0],
                 stroke_color=INK,stroke_width=3),
            Line([x_q3,y_bracket-.10,0],[x_q3,y_bracket+.10,0],
                 stroke_color=INK,stroke_width=3),
        )
        result = mx(r"\mathrm{IQR}=Q_3-Q_1=15-5=10",48)
        result.move_to([0,-2.47,0])
        self.play(Create(bracket),run_time=1.3)
        self.play(Write(result),run_time=2.1)
        self.note("IQR measures the spread of the middle half of the data.",
                  hold=2.6,y=-3.16)

    def normal_distribution(self):
        self.slide(12,"PERIOD III  /  RECOGNIZE DATA PATTERNS",
                   "The normal distribution is one model; not every dataset is normal.")
        axes=Axes(x_range=[-3.7,3.7,1],y_range=[0,.5,.1],
            x_length=11.2,y_length=4.4,
            tips=False,
            axis_config={"color":INK,"stroke_width":2.3},
            y_axis_config={"include_numbers":False},
            x_axis_config={"include_numbers":False})
        axes.move_to([0,-.22,0])
        bell=axes.plot(lambda x:np.exp(-(x*x)/2)/np.sqrt(2*np.pi),
                       x_range=[-3.5,3.5,.02],
                       color=INK,stroke_width=4)
        self.play(Create(axes),run_time=1.4)
        self.play(Create(bell),run_time=3.2,rate_func=linear)
        mu=DashedLine(axes.c2p(0,0),axes.c2p(0,1/np.sqrt(2*np.pi)),
              color=SECONDARY,dash_length=.10)
        minus=DashedLine(axes.c2p(-1,0),axes.c2p(-1,np.exp(-.5)/np.sqrt(2*np.pi)),
              color=GRID,dash_length=.1)
        plus=DashedLine(axes.c2p(1,0),axes.c2p(1,np.exp(-.5)/np.sqrt(2*np.pi)),
              color=GRID,dash_length=.1)
        self.play(Create(mu),Create(minus),Create(plus),run_time=1.5)
        eq=mx(r"X\sim\mathcal{N}(\mu,\sigma^2)",56).move_to([0,-2.73,0])
        self.play(Write(eq),run_time=1.6)
        self.wait(3)

    def closing(self):
        self.slide(13,"THE HABIT OF A STATISTICIAN",
                   "Ask carefully. Organize honestly. Interpret critically.")
        steps=VGroup(*[tx(s,40,True) for s in
                       ("DEFINE THE QUESTION","EXAMINE THE DATA",
                        "JUSTIFY THE CONCLUSION")])
        steps.arrange(DOWN,buff=.61).move_to([0,.27,0])
        self.play(LaggedStart(*[Write(s) for s in steps],
                  lag_ratio=.34),run_time=4.3)
        check=mx(r"\mathrm{DATA}\ \rightarrow\ \mathrm{EVIDENCE}\ \rightarrow\ \mathrm{DECISION}",50)
        check.move_to([0,-2.5,0])
        self.play(Write(check),run_time=2.5)
        self.wait(3)
