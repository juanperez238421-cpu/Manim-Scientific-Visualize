#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6.2 final: LaTeX-portable mass-cancellation derivation.

Keeps V6.1's optimized live timer and replaces the optional \\cancel notation
with a standard algebraic division step that compiles under the project default
ManimCE 0.20.1 LaTeX template.
"""
from manim import *

from Physics9_Galileo_Pisa_Mass_Independence_V6_1_SENIOR_FINAL import (
    Physics9GalileoPisaMassIndependenceV61SeniorFinal,
)
from Physics9_Galileo_Pisa_Mass_Independence_V6_FINAL import (
    RUN, RUN_FAST, PAUSE_WORK,
)


class Physics9GalileoPisaMassIndependenceV62SeniorFinal(Physics9GalileoPisaMassIndependenceV61SeniorFinal):
    def pisa_force_reasoning(self):
        self.set_header(
            10,
            "WHY MASS DOES NOT CHANGE IDEAL FREE-FALL ACCELERATION",
            "A heavier object feels more gravitational force, but it also has proportionally more inertia.",
        )

        left = self.panel(6.55, 4.75, fill=WHITE).move_to(LEFT * 3.65 + DOWN * 0.25)
        right = self.panel(6.55, 4.75, fill=WHITE).move_to(RIGHT * 3.65 + DOWN * 0.25)

        lt = self.txt("COMPARE GRAVITATIONAL FORCES", 22, BOLD).next_to(left.get_top(), DOWN, buff=0.24)
        force_rows = VGroup(
            self.formula_panel(r"m_1=1\,\mathrm{kg}:\quad F_{g1}=m_1g=9.81\,\mathrm{N}", width=5.75, height=0.90, size=26),
            self.formula_panel(r"m_2=10\,\mathrm{kg}:\quad F_{g2}=m_2g=98.1\,\mathrm{N}", width=5.75, height=0.90, size=26),
            self.txt("10x the mass -> 10x the gravitational force", 18, BOLD),
        ).arrange(DOWN, buff=0.28).move_to(left.get_center() + DOWN * 0.15)

        rt = self.txt("APPLY NEWTON'S SECOND LAW", 22, BOLD).next_to(right.get_top(), DOWN, buff=0.24)
        derivation = VGroup(
            self.math(r"F_{\mathrm{net}}=ma", 34),
            self.math(r"F_g=mg", 34),
            self.math(r"ma=mg", 38),
            self.math(r"\frac{ma}{m}=\frac{mg}{m}\qquad(m\neq0)", 34),
            self.math(r"\boxed{a=g}", 46),
        ).arrange(DOWN, buff=0.23).move_to(right.get_center() + DOWN * 0.18)

        result = self.formula_panel(
            r"\boxed{a_{1\,\mathrm{kg}}=a_{10\,\mathrm{kg}}=g\approx9.81\,\mathrm{m/s^2}}",
            width=9.5, height=0.95, size=33,
        ).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(left), FadeIn(right), FadeIn(lt), FadeIn(rt), run_time=RUN)
        for item in force_rows:
            self.play(FadeIn(item), run_time=RUN_FAST)
        for item in derivation:
            self.play(FadeIn(item), run_time=RUN_FAST)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.clear_stage()


# Preview:
# manim -pql Physics9_Galileo_Pisa_Mass_Independence_V6_2_SENIOR_FINAL.py Physics9GalileoPisaMassIndependenceV62SeniorFinal --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Pisa_Mass_Independence_V6_2_SENIOR_FINAL.py Physics9GalileoPisaMassIndependenceV62SeniorFinal --disable_caching
