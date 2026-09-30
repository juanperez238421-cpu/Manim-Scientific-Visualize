#!/usr/bin/env python3
"""Reference JP Manim Classroom Standard lesson."""

from __future__ import annotations

import math
import numpy as np
from jp_manim_standard import *

A = 3.0
B = 4.0
C = 5.0

class ClassroomTemplate(JPMathClassroomScene):
    def validate_lesson_data(self) -> None:
        assert_close(A**2 + B**2, C**2, label="Pythagorean relation")
        assert_close(math.sqrt(A**2 + B**2), C, label="hypotenuse")

    def construct(self) -> None:
        self.opening(); self.visual_model(); self.equation_development(); self.summary()

    def opening(self) -> None:
        self.standard_opening("GRADE / SUBJECT", "TOPIC TITLE",
            "Short sentence describing the learning objective",
            "Visualize first. Formalize second. Verify before interpreting.")

    def visual_model(self) -> None:
        self.set_header(1, "START FROM A CLEAR VISUAL MODEL",
            "Keep the figure and mathematical description visible together.")
        p0=np.array([-2.2,-1.25,0]); p1=np.array([1.8,-1.25,0]); p2=np.array([-2.2,1.75,0])
        triangle=Polygon(p0,p1,p2,stroke_color=BLACK_LINE,stroke_width=3)
        labels=VGroup(
            self.math("3",29).next_to(Line(p0,p2),LEFT,buff=0.14),
            self.math("4",29).next_to(Line(p0,p1),DOWN,buff=0.14),
            self.math("5",29).next_to(Line(p1,p2),UR,buff=0.05),
        )
        panel=self.figure_panel(VGroup(triangle,labels),width=6.2,height=4.5,title="RIGHT TRIANGLE",
            caption="The visual remains readable while the equation is developed.")
        right=VGroup(
            self.formula_panel(r"a^2+b^2=c^2",width=5.7,height=1.05,font_size=40),
            self.note_panel("READ THE FIGURE",["Legs: 3 and 4","Hypotenuse: 5","Use the right-angle relation."],width=5.7),
        ).arrange(DOWN,buff=0.28)
        layout=self.split_layout(panel.group,right,center_y=-0.45)
        self.assert_content_safe(layout.group,"visual model")
        self.play(FadeIn(panel.group),run_time=RUN_NORMAL)
        self.play(FadeIn(right),run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK); self.clear_stage()

    def equation_development(self) -> None:
        self.set_header(2,"DEVELOP ONE LOGICAL STEP AT A TIME","Preserve the causal chain.")
        stack=self.equation_stack([r"a^2+b^2=c^2",r"3^2+4^2=c^2",r"25=c^2",r"c=5"],sizes=[40,40,40,46],max_width=7.0)
        self.animate_equation_stack(stack,pause=PAUSE_READ); self.wait(PAUSE_WORK); self.clear_stage()

    def summary(self) -> None:
        self.set_header(3,"END WITH A REPRODUCIBLE METHOD","Students should be able to repeat the process.")
        route=self.process_map([("1","READ"),("2","MODEL"),("3","SUBSTITUTE"),("4","SOLVE"),("5","VERIFY")],columns=3)
        route.move_to(DOWN*0.35); self.fit(route,14.0,4.8)
        self.play(LaggedStart(*[FadeIn(card) for card in route],lag_ratio=0.10),run_time=RUN_SLOW*1.8)
        self.wait(PAUSE_FINAL); self.standard_closing("Visualize. Calculate. Verify. Interpret.")
