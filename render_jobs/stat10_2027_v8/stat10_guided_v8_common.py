# -*- coding: utf-8 -*-
"""Shared V8 visual/educational system. ManimCE 0.20.1, LaTeX, native 16:9.
Based on IJR's consolidated Statistics10 V6-V7 classroom system.
Four separate classroom scenes import this module.
"""
from __future__ import annotations
import sys
from pathlib import Path
THIS_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(THIS_DIR))
sys.path.insert(0,str(THIS_DIR.parent / "stat10_2027_native_v6"))
from manim import *
import numpy as np
from statistics10_latex_v6 import (
    ClassroomLatex, INK, GRID, SECONDARY, PALE,
    latex_text, fit, text_lines, box, unit_grid
)

def math(s, size=51):
    return MathTex(s, font_size=size, color=INK)

def text(s, size=34, bold=False):
    return latex_text(s, size, bold)

def stack(*items, buff=.34, center=(0,-.02,0), max_width=13.8, max_height=5.0):
    g=VGroup(*items).arrange(DOWN,buff=buff,aligned_edge=ORIGIN)
    fit(g,max_width,max_height)
    g.move_to(center)
    return g

def two_cards(a_title,a_lines,b_title,b_lines,width=6.25,height=2.8,y=-.02):
    a=box(a_title,a_lines,width,height)
    b=box(b_title,b_lines,width,height)
    pair=VGroup(a,b).arrange(RIGHT,buff=.65)
    pair.move_to([0,y,0])
    return a,b,pair

def table(headers, rows, widths=None, height=.63, fontsize=29):
    """LaTeX in every native vector cell; header and data rows addressable."""
    n=len(headers)
    widths=widths or [3.0]*n
    assert len(widths)==n
    objects=VGroup()
    for i,values in enumerate([headers]+rows):
        assert len(values)==n,(i,values)
        line=VGroup()
        for j,v in enumerate(values):
            rec=Rectangle(width=widths[j],height=height,
                stroke_width=1.2,stroke_color=GRID,
                fill_opacity=1,fill_color=PALE if i==0 else WHITE)
            if str(v).startswith("MATH:"):
                label=math(str(v)[5:],fontsize-1)
            else:
                label=text(str(v),fontsize-(2 if i==0 else 0),i==0)
            fit(label,rec.width-.18,rec.height-.12)
            label.move_to(rec)
            line.add(VGroup(rec,label))
        line.arrange(RIGHT,buff=0)
        objects.add(line)
    objects.arrange(DOWN,buff=0)
    fit(objects,13.9,4.9)
    return objects

def rule(line1,line2=None,y=-2.60):
    label=text(line1,31,True)
    fit(label,14.0,.66)
    label.move_to([0,y,0])
    return label

def dot_matrix(n,columns=12,radius=.10,sx=.43,sy=.46):
    out=VGroup()
    for i in range(n):
        row,col=divmod(i,columns)
        dot=Circle(radius=radius,stroke_color=INK,stroke_width=1.9,
            fill_color=WHITE,fill_opacity=1)
        dot.move_to([(col-(columns-1)/2)*sx,
                     (((n-1)//columns)/2-row)*sy,0])
        out.add(dot)
    return out

class GuidedClassroomV8(ClassroomLatex):
    week=0
    def cover(self,title,tagline):
        self.slide(0,title,tagline)
        formula=math(r"\mathrm{QUESTION}\ \rightarrow\ \mathrm{DATA}\ \rightarrow\ \mathrm{REASONING}",55)
        fit(formula,13.7,1.2).move_to([0,.25,0])
        sub=text("GUIDED INVESTIGATION  /  STEP-BY-STEP SOLUTION",32,True).move_to([0,-1.32,0])
        self.play(Write(formula),run_time=2.4)
        self.play(FadeIn(sub,shift=UP*.19),run_time=1.1)
        self.wait(2.0)

    def section(self,n,title,subtitle):
        self.slide(n,title,subtitle)

    def show_table(self,tab,run_time=2.8,pos=(0,.0,0)):
        fit(tab,13.8,4.8)
        tab.move_to(pos)
        self.play(LaggedStart(*[FadeIn(row,shift=UP*.16) for row in tab],
                    lag_ratio=.19),run_time=run_time)
        self.wait(1.3)
        return tab

    def indicate_row(self,row,duration=1.3):
        outline=SurroundingRectangle(row,color=INK,stroke_width=3,buff=.07)
        self.play(Create(outline),run_time=.66)
        self.wait(duration)
        self.play(FadeOut(outline),run_time=.35)

    def answer(self,statement,hold=2):
        response=rule(statement)
        self.play(FadeIn(response,shift=UP*.16),run_time=1)
        self.wait(hold)
        return response

    def task(self,questions,answer,thinking=5):
        q=text_lines(questions,32,.42)
        fit(q,13.1,4.7)
        q.move_to([0,.16,0])
        self.play(LaggedStart(*[Write(t) for t in q],lag_ratio=.25),
                  run_time=3.7)
        self.wait(thinking)
        self.answer(answer,3)

    def pause_for_class(self,phrase="Think before the next step",duration=3):
        txt=text(phrase,32,True)
        fit(txt,13,.8)
        txt.move_to([0,-2.37,0])
        self.play(FadeIn(txt,shift=UP*.1),run_time=.7)
        self.wait(duration)
        self.play(FadeOut(txt),run_time=.4)
