# -*- coding: utf-8 -*-
"""STATISTICS 10 | 2027 Q1 | WEEKS 1-4
Native Manim Community Edition 0.20.1 | LaTeX typography | 16:9 FullHD.
Derived from IJR Statistics_10_2027_P1.docx and 2026 Period I curriculum.
Educational examples are fictional. No student records.
Render: manim -pql statistics10_latex_v6.py Statistics10Week1V6
        manim -pqh statistics10_latex_v6.py Statistics10Week1V6
"""
from __future__ import annotations
import numpy as np
from manim import *

config.pixel_width=1920
config.pixel_height=1080
config.frame_width=16
config.frame_height=9
config.frame_rate=30
config.background_color=WHITE

INK="#171717"
SECONDARY="#555555"
GRID="#C7C7C7"
PALE="#F5F5F5"
SELECTED=(2,7,11,14,19,22,28,34,39,44,52,58)
DUMMY_ROWS=[
    ("S01","Bus","18.4","2"),
    ("S02","Walk","12.3","1"),
    ("S03","Bike","9.7","0"),
    ("S04","Bus","25.1","3"),
    ("S05","Walk","14.2","2"),
    ("S06","Car","17.8","1"),
]
assert len(SELECTED)==12 and len(set(SELECTED))==12 and max(SELECTED)<60
assert len(DUMMY_ROWS)==6

def latex_text(s,size=35,bold=False):
    s=s.replace("&",r"\&").replace("%",r"\%").replace("_",r"\_")
    m=Tex(r"\textbf{"+s+"}" if bold else s, font_size=size, color=INK)
    return m

def fit(m,width=14.4,height=5.7):
    if m.width>width:
        m.scale_to_fit_width(width)
    if m.height>height:
        m.scale_to_fit_height(height)
    return m

def text_lines(lines,size=33,spacing=.32):
    g=VGroup(*[latex_text(t,size) for t in lines])
    g.arrange(DOWN,aligned_edge=LEFT,buff=spacing)
    return fit(g,13.7,5)

def unit_grid(n=60,columns=10,r=.12,gapx=.43,gapy=.53):
    dots=VGroup()
    for k in range(n):
        row,col=divmod(k,columns)
        d=Circle(radius=r,stroke_width=2.2,stroke_color=INK,
                 fill_color=WHITE,fill_opacity=1)
        d.move_to([(col-(columns-1)/2)*gapx,
                   ((n-1)//columns/2-row)*gapy,0])
        dots.add(d)
    return dots

def box(title,body,width=5.85,height=2.4):
    rect=RoundedRectangle(corner_radius=.12,width=width,height=height,
             stroke_color=INK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
    title=latex_text(title,32,True)
    lines=VGroup(*[latex_text(b,29) for b in body])
    lines.arrange(DOWN,buff=.22)
    group=VGroup(title,lines).arrange(DOWN,buff=.34)
    fit(group,width-.55,height-.45)
    group.move_to(rect)
    return VGroup(rect,group)

def raw_table():
    headings=["ID","Transport","Time (min)","Siblings"]
    rows=[headings]+[list(row) for row in DUMMY_ROWS]
    cells=[]
    for r,row in enumerate(rows):
        g=VGroup()
        for c,value in enumerate(row):
            cell=Rectangle(width=[1.6,3.5,3.1,2.3][c],height=.62,
              stroke_color=GRID,stroke_width=1.2,
              fill_color=PALE if r==0 else WHITE,fill_opacity=1)
            label=latex_text(value,28 if r==0 else 29,r==0)
            fit(label,cell.width-.18,.46)
            label.move_to(cell)
            g.add(VGroup(cell,label))
        g.arrange(RIGHT,buff=0)
        cells.append(g)
    group=VGroup(*cells).arrange(DOWN,buff=0)
    fit(group,13.1,5.0)
    return group

class ClassroomLatex(MovingCameraScene):
    week=0
    def construct(self):
        raise NotImplementedError

    def slide(self,number,title,subtitle):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.48)
        self.camera.frame.set(width=16).move_to(ORIGIN)
        eyebrow=latex_text(f"STATISTICS 10  /  2027  /  PERIOD I  /  WEEK {self.week:02d}",21,True)
        eyebrow.to_corner(UL,buff=.38).shift(RIGHT*.35)
        heading=latex_text(title,44,True)
        fit(heading,14.5,1.0)
        heading.move_to([-7.14,3.42,0],aligned_edge=LEFT)
        subtitle=latex_text(subtitle,26)
        fit(subtitle,14.2,.75)
        subtitle.move_to([-7.12,2.82,0],aligned_edge=LEFT)
        rule=Line([-7.3,2.52,0],[7.3,2.52,0],color=GRID,stroke_width=2)
        page=latex_text(f"{number:02d}",25,True).to_corner(DR,buff=.40)
        self.play(FadeIn(eyebrow,shift=RIGHT*.15),FadeIn(heading,shift=UP*.1),
                  FadeIn(subtitle),Create(rule),FadeIn(page),run_time=.92)

    def stage(self,m):
        fit(m,14.2,5.55)
        m.move_to([0,-.27,0])
        return m

    def item(self,body,pause=1.5):
        self.play(FadeIn(body,shift=UP*.22),run_time=1.0)
        self.wait(pause)

    def conclusion(self,statement,y=-2.76):
        t=fit(latex_text(statement,32,True),13.9,.68).move_to([0,y,0])
        self.play(Write(t),run_time=1.25)
        self.wait(1.7)
        return t

    def title_cover(self,topic,daterange):
        self.slide(0,f"WEEK {self.week}: {topic}",daterange)
        number=MathTex(r"\mathrm{DATA}\longrightarrow\mathrm{EVIDENCE}",
                       font_size=68,color=INK)
        number.move_to(UP*.2)
        underline=Line(number.get_left()+DOWN*.45,number.get_right()+DOWN*.45,
             color=INK,stroke_width=3)
        self.play(Write(number),run_time=2.1)
        self.play(Create(underline),run_time=.75)
        self.wait(2.0)

class Statistics10Week1V6(ClassroomLatex):
    week=1
    def construct(self):
        self.title_cover("INTRODUCTION TO STATISTICS","19--22 January 2027 | What is a statistical question?")
        self.slide(1,"WHAT DOES STATISTICS STUDY?","Collect observations to describe a group and make informed decisions.")
        chain=VGroup(*[box(s,[],3.2,1.45) for s in
                        ["ASK","OBSERVE","DESCRIBE","INTERPRET"]]).arrange(RIGHT,buff=.34)
        chain=self.stage(chain)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in chain],lag_ratio=.25),run_time=3.3)
        for item in chain:
            self.play(Indicate(item,scale_factor=1.04,color=SECONDARY),run_time=.48)
        self.conclusion("A statistical conclusion needs observations.")

        self.slide(2,"WHICH QUESTION IS STATISTICAL?","A statistical question expects answers that can vary.")
        a=box("FIXED ANSWER",["How many minutes","are in one hour?"],6.4,2.5)
        b=box("VARIABLE ANSWERS",["How long do students","read each day?"],6.4,2.5)
        pair=VGroup(a,b).arrange(RIGHT,buff=.5).move_to(UP*.22)
        self.play(LaggedStart(FadeIn(a,shift=LEFT*.3),FadeIn(b,shift=RIGHT*.3),
                              lag_ratio=.32),run_time=1.8)
        fixed=MathTex(r"60",font_size=63,color=INK).move_to([-3.38,-2.0,0])
        varying=MathTex(r"10,\;25,\;40,\;20,\;35",font_size=49,color=INK).move_to([3.3,-2.0,0])
        self.play(Write(fixed),run_time=1.1)
        self.play(Write(varying),run_time=1.9)
        self.wait(3)

        self.slide(3,"LOOK FOR VARIABILITY","Six fictional daily reading-time observations.")
        vals=[10,25,40,20,35,55]
        axis=NumberLine(x_range=[0,60,10],length=11.0,
            include_numbers=True,label_direction=DOWN,
            color=INK).move_to(DOWN*.55)
        q=latex_text("How many minutes did each student read?",37,True).move_to(UP*1.65)
        self.play(Write(q),Create(axis),run_time=2)
        dots=VGroup(*[Dot(axis.n2p(v),radius=.125,color=INK) for v in vals])
        for d in dots:
            d.shift(UP*(.11+ .1*list(dots).index(d)%2))
        self.play(LaggedStart(*[GrowFromCenter(x) for x in dots],lag_ratio=.2),run_time=2.8)
        self.conclusion("Different observations are expected.")

        self.slide(4,"POPULATION: THE ENTIRE GROUP","Specify who the research question concerns.")
        population=unit_grid().move_to(LEFT*3.55+DOWN*.25)
        desc=VGroup(latex_text("All Grade 10 students",36,True),
                    MathTex(r"N=60",font_size=68,color=INK)).arrange(DOWN,buff=.48)
        desc.move_to(RIGHT*3.4+DOWN*.15)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in population],
                              lag_ratio=.012),run_time=3)
        self.play(FadeIn(desc,shift=RIGHT*.25),run_time=1.3)
        self.wait(2.5)

        self.slide(5,"SAMPLE: PART OF THE POPULATION","A sample contains selected units from the same population.")
        population=unit_grid().move_to(LEFT*3.5+DOWN*.1)
        self.play(FadeIn(population),run_time=.9)
        chosen=[population[i] for i in SELECTED]
        self.play(LaggedStart(*[d.animate.set_fill(INK,opacity=1) for d in chosen],
                              lag_ratio=.1),run_time=2.7)
        clones=VGroup(*[x.copy() for x in chosen])
        self.add(clones)
        target=unit_grid(12,4,r=.21,gapx=.73,gapy=.73).move_to(RIGHT*3.3+DOWN*.2)
        self.play(Transform(clones,target),run_time=2.5)
        labels=VGroup(MathTex(r"N=60",font_size=54,color=INK),
                      MathTex(r"n=12",font_size=54,color=INK))
        labels[0].move_to([-3.5,1.85,0]);labels[1].move_to([3.3,1.85,0])
        self.play(Write(labels),run_time=1.3)
        relation=MathTex(r"n<N,\qquad S\subseteq P",font_size=49,color=INK).move_to(DOWN*2.65)
        self.play(Write(relation),run_time=2)
        self.wait(2.3)

        self.slide(6,"TWO GUIDED CASES","Always state both the target group and its sample.")
        cards=VGroup(
          box("CASE A: STUDENTS",["Population: 60 students","Sample: 12 students"],6.1,3.0),
          box("CASE B: TEACHERS",["Population: 24 teachers","Sample: 6 teachers"],6.1,3.0)
        ).arrange(RIGHT,buff=.55).move_to(DOWN*.05)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.32) for c in cards],
                lag_ratio=.28),run_time=2.4)
        self.conclusion("The sample must belong to the target population.")

        self.slide(7,"EXIT TICKET","Independent written response -- justify your reasoning.")
        q=text_lines(["1. Write one statistical question about school life.",
                      "2. Define its population.",
                      "3. Propose a sample and explain the relationship."],32)
        self.stage(q);self.play(Write(q),run_time=3.7)
        self.wait(7.0)
        self.conclusion("Question  +  population  +  sample")

class Statistics10Week2V6(ClassroomLatex):
    week=2
    def construct(self):
        self.title_cover("SAMPLES AND DATA COLLECTION","25--29 January 2027 | How can we select a useful sample?")
        self.slide(1,"REVISIT THE RESEARCH QUESTION","How do Grade 10 students travel to school?")
        pop=unit_grid().move_to(LEFT*3.4+DOWN*.2)
        label=latex_text("Target population",40,True).move_to(RIGHT*3.4+UP*.8)
        count=MathTex(r"N=60",font_size=70,color=INK).move_to(RIGHT*3.4+DOWN*.55)
        self.play(FadeIn(pop),Write(label),Write(count),run_time=2)
        self.wait(2)

        self.slide(2,"CENSUS OR SAMPLE?","The distinction concerns how many members are observed.")
        pop=unit_grid().move_to(LEFT*3.35+DOWN*.35)
        whole=VGroup(latex_text("CENSUS",40,True),
            MathTex(r"N=60",font_size=60,color=INK),
            latex_text("Every member",29)).arrange(DOWN,buff=.25).move_to(RIGHT*3.3+UP*.35)
        self.play(FadeIn(pop),FadeIn(whole),run_time=1.6)
        self.play(LaggedStart(*[d.animate.set_fill(INK,opacity=1) for d in pop],
            lag_ratio=.008),run_time=2.5)
        sample=VGroup(latex_text("SAMPLE",40,True),
            MathTex(r"n=12",font_size=60,color=INK),
            latex_text("Selected members",29)).arrange(DOWN,buff=.25).move_to(whole)
        self.play(ReplacementTransform(whole,sample),
                  *[pop[i].animate.set_fill(WHITE,opacity=1) for i in range(60)
                    if i not in SELECTED],run_time=2.8)
        self.wait(3)

        self.slide(3,"WHO IS INCLUDED?","Easy access does not guarantee balanced coverage.")
        left=box("CONVENIENCE",["Only one entrance","Only the morning shift"],6.15,3.0)
        right=box("BETTER COVERAGE",["Different entrances","Different arrival times"],6.15,3.0)
        pair=VGroup(left,right).arrange(RIGHT,buff=.65).move_to(UP*.05)
        self.play(FadeIn(left,shift=LEFT*.35),run_time=1.1)
        self.play(FadeIn(right,shift=RIGHT*.35),run_time=1.1)
        self.conclusion("Broader coverage helps, but it is not proof of representativeness.")

        self.slide(4,"HOW WOULD YOU COLLECT THE DATA?","Match the collection method to the question.")
        methods=VGroup(*[box(a,b,4.15,2.75) for a,b in [
            ("SURVEY",["Ask a question"]),
            ("OBSERVATION",["Watch and record"]),
            ("MEASUREMENT",["Use an instrument"])]]).arrange(RIGHT,buff=.45)
        self.stage(methods)
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.3) for x in methods],
             lag_ratio=.4),run_time=3)
        self.wait(3)

        self.slide(5,"COMPARE TWO STUDY PLANS","Which plan better addresses the population?")
        a=box("PLAN A",["Ask 12 students","at the same entrance"],6.0,3.0)
        b=box("PLAN B",["Include students from","different arrival contexts"],6.0,3.0)
        pair=VGroup(a,b).arrange(RIGHT,buff=.8).move_to(DOWN*.05)
        self.play(FadeIn(pair),run_time=1.6)
        self.wait(5)
        ring=SurroundingRectangle(b,color=INK,stroke_width=4,buff=.14)
        self.play(Create(ring),run_time=1.3)
        self.conclusion("Plan B improves coverage; both plans may still have limitations.")

        self.slide(6,"PARTNER INVESTIGATION","Propose a collection plan and identify one limitation.")
        p=text_lines(["1. State the target population and the unit.",
                      "2. Choose who will be asked or observed.",
                      "3. Name the collection method.",
                      "4. Explain who might be missing."],32)
        self.stage(p);self.play(LaggedStart(*[Write(t) for t in p],
                   lag_ratio=.26),run_time=4)
        self.wait(7)
        self.conclusion("Your method should answer your original question.")

class Statistics10Week3V6(ClassroomLatex):
    week=3
    def construct(self):
        self.title_cover("STATISTICAL VARIABLES","1--5 February 2027 | Qualitative and quantitative")
        self.slide(1,"WHAT IS A VARIABLE?","A characteristic recorded for each observational unit.")
        m=MathTex(r"\mathrm{UNIT}\ \longrightarrow\ \mathrm{VARIABLE}\ \longrightarrow\ \mathrm{VALUE}",
                  font_size=55,color=INK)
        m=self.stage(m)
        self.play(Write(m),run_time=3.0)
        self.wait(2)

        self.slide(2,"WHAT INFORMATION IS RECORDED?","One student can provide several distinct observations.")
        table=raw_table();self.stage(table)
        self.play(LaggedStart(*[FadeIn(row,shift=RIGHT*.17) for row in table],
                 lag_ratio=.18),run_time=3.3)
        self.wait(3)
        self.play(Indicate(table[0],scale_factor=1.02,color=SECONDARY),run_time=1.0)
        self.wait(1.0)

        self.slide(3,"TWO TYPES OF VARIABLE","Classify what the recorded values actually represent.")
        choices=VGroup(box("QUALITATIVE",["Category or label","Example: transport"],6.3,3.0),
                       box("QUANTITATIVE",["Amount or measurement","Example: travel time"],6.3,3.0))
        choices.arrange(RIGHT,buff=.65).move_to(DOWN*.1)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in choices],
                  lag_ratio=.4),run_time=2.8)
        self.conclusion("A variable is defined by its meaning, not by its digits.")

        self.slide(4,"CATEGORIES ARE NOT AMOUNTS","Travel mode is recorded as a category.")
        modes=VGroup(*[latex_text(x,43,True) for x in
                 ["BUS","WALK","BIKE","CAR"]]).arrange(RIGHT,buff=.85)
        self.stage(modes)
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.44) for x in modes],
                  lag_ratio=.35),run_time=3.1)
        self.conclusion("These values describe types, not measured amounts.")

        self.slide(5,"QUANTITIES REPRESENT AMOUNTS","Counted or measured numerical values.")
        times=MathTex(r"18.4,\ 12.3,\ 9.7,\ 25.1,\ 14.2,\ 17.8",
                  font_size=49,color=INK).move_to(UP*.15)
        indicator=MathTex(r"x_i\in\mathbb{R}",font_size=60,color=INK).move_to(DOWN*1.65)
        self.play(Write(times),run_time=2.7)
        self.play(TransformFromCopy(times,indicator),run_time=1.5)
        self.wait(3)

        self.slide(6,"NUMBERS CAN ALSO BE IDENTIFIERS","The route number 12 is not a quantity of buses.")
        route=MathTex(r"\boxed{12}",font_size=100,color=INK).move_to(UP*.15)
        caption=latex_text("Bus route identifier",39,True).move_to(DOWN*1.6)
        self.play(GrowFromCenter(route),run_time=1.6)
        self.play(Write(caption),run_time=1.3)
        self.conclusion("A numeric code may be qualitative.")

        self.slide(7,"CLASSIFY AND JUSTIFY","Discuss two borderline examples with a partner.")
        prompt=text_lines(["Favorite color: qualitative",
                           "Height: quantitative",
                           "Jersey number: qualitative identifier",
                           "Number of siblings: quantitative"],34)
        self.stage(prompt)
        self.play(LaggedStart(*[FadeIn(t,shift=RIGHT*.2) for t in prompt],
                 lag_ratio=.32),run_time=3.4)
        self.wait(5)
        self.conclusion("Always explain what the values mean.")

class Statistics10Week4V6(ClassroomLatex):
    week=4
    def construct(self):
        self.title_cover("COUNTING OR MEASURING?","8--12 February 2027 | Discrete and continuous")
        self.slide(1,"FIRST: WHAT KIND OF VARIABLE?","Quantitative variables can represent counts or measurements.")
        formula=MathTex(r"\text{Quantitative}\longrightarrow
                 \begin{cases}\text{Discrete}\\ \text{Continuous}\end{cases}",
                 font_size=49,color=INK)
        self.stage(formula)
        self.play(Write(formula),run_time=3.4)
        self.wait(2)

        self.slide(2,"DISCRETE: COUNT THE OBJECTS","A count takes separated possible values.")
        items=VGroup(*[Dot(radius=.19,color=INK) for i in range(7)]).arrange(RIGHT,buff=.5)
        self.stage(items)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in items],
                lag_ratio=.2),run_time=2.5)
        values=MathTex(r"x\in\{0,1,2,3,\ldots\}",font_size=61,color=INK)
        values.move_to(DOWN*2.0)
        self.play(Write(values),run_time=2)
        self.wait(3)

        self.slide(3,"CONTINUOUS: MEASURE A QUANTITY","Travel time can vary between two recorded numbers.")
        line=NumberLine(x_range=[0,10,1],length=11,include_numbers=True,color=INK)
        line.move_to(DOWN*.18)
        marker=Dot(line.n2p(2),radius=.14,color=INK)
        self.play(Create(line),FadeIn(marker),run_time=1.7)
        self.play(marker.animate.move_to(line.n2p(7.83)),run_time=4,
                  rate_func=smooth)
        caption=MathTex(r"t=7.83\ \mathrm{min}",font_size=61,color=INK).move_to(UP*1.45)
        self.play(Write(caption),run_time=1.4)
        self.wait(2.5)

        self.slide(4,"MEASURED DOES NOT MEAN DISCRETE","Rounding only changes the precision of the record.")
        precise=MathTex(r"18.4\ \mathrm{min}",font_size=75,color=INK).move_to(UP*.3)
        approx=MathTex(r"\approx18\ \mathrm{min}",font_size=75,color=INK)
        approx.move_to(precise)
        self.play(Write(precise),run_time=1.5)
        self.play(ReplacementTransform(precise,approx),run_time=2)
        self.conclusion("The underlying variable remains continuous.")

        self.slide(5,"DECISION TREE","Interpret the meaning before classifying.")
        top=box("VALUE",["What does it describe?"],5.2,1.6).move_to(UP*1.65)
        left=box("CATEGORY",["Qualitative variable"],5.4,2.0).move_to(LEFT*3.35+DOWN*1.1)
        right=box("QUANTITY",["Count or measurement"],5.4,2.0).move_to(RIGHT*3.35+DOWN*1.1)
        self.play(GrowFromCenter(top),run_time=.9)
        self.play(Create(Line(top.get_bottom(),left.get_top(),color=INK)),
                  Create(Line(top.get_bottom(),right.get_top(),color=INK)),run_time=1.1)
        self.play(FadeIn(left),FadeIn(right),run_time=1.3)
        self.wait(3)

        self.slide(6,"RAW OBSERVATIONS, NOT FREQUENCIES","Prepare one row per unit for a later statistical study.")
        table=raw_table()
        self.stage(table)
        self.play(LaggedStart(*[FadeIn(row,shift=UP*.11) for row in table],
             lag_ratio=.21),run_time=3.5)
        self.wait(3.5)
        self.conclusion("Do not construct frequency tables or graphs yet.")

        self.slide(7,"FINAL CLASSIFICATION WORKSHOP","Explain each classification with a reason.")
        tasks=text_lines(["Number of siblings: discrete count",
                    "Travel time: continuous measurement",
                    "Bus route 12: qualitative identifier",
                    "Rounded temperature: continuous measurement"],33)
        self.stage(tasks)
        self.play(LaggedStart(*[Write(t) for t in tasks],lag_ratio=.24),
                  run_time=4)
        self.wait(6)
        self.conclusion("Classify, justify, and record before graphing.")
