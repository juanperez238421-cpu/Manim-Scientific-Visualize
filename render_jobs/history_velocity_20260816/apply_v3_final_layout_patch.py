#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path(sys.argv[1])
s = path.read_text(encoding="utf-8")

replacements = [
    (
        'derivative = MathTex(r"\\boxed{v(t)=\\frac{dx}{dt}}", color=BLACK, font_size=54).move_to(DOWN * 1.05)',
        'derivative = MathTex(r"\\boxed{v(t)=\\frac{dx}{dt}}", color=BLACK, font_size=52).move_to(DOWN * 0.82)',
    ),
    (
        'limit = MathTex(r"v(t)=\\lim_{\\Delta t\\to0}\\frac{\\Delta x}{\\Delta t}", color=BLACK, font_size=39).move_to(DOWN * 2.15)',
        'limit = MathTex(r"v(t)=\\lim_{\\Delta t\\to0}\\frac{\\Delta x}{\\Delta t}", color=BLACK, font_size=37).move_to(DOWN * 2.35)',
    ),
    (
        'explanation = self.text("Smaller intervals → a stable instantaneous slope.", 24, BOLD).move_to(DOWN * 3.05)',
        'explanation = self.text("Smaller intervals → a stable instantaneous slope.", 23, BOLD).move_to(DOWN * 3.24)',
    ),
    (
        'formula = MathTex(eq, color=BLACK, font_size=30).next_to(ax, DOWN, buff=0.18)',
        'formula = MathTex(eq, color=BLACK, font_size=27).next_to(ax, DOWN, buff=0.10)',
    ),
    (
        'time_readout = VGroup(time_label, time_num, time_unit).arrange(RIGHT, buff=0.10).move_to(UP*1.65)',
        'time_readout = VGroup(time_label, time_num, time_unit).arrange(RIGHT, buff=0.10).move_to(UP*2.08)',
    ),
    (
'''        questions = VGroup(\n            self.text("WHERE?", 22, BOLD),\n            self.text("HOW FAST IS POSITION CHANGING?", 22, BOLD),\n            self.text("HOW FAST IS VELOCITY CHANGING?", 22, BOLD),\n        )\n        for q, center in zip(questions, centers):\n            q.move_to(center + DOWN*2.05)\n        self.play(LaggedStart(*[FadeIn(q, shift=UP*0.06) for q in questions], lag_ratio=0.16), run_time=1.3)\n        bridge = VGroup(self.mini_tag("x–t", 26), Arrow(ORIGIN,RIGHT*0.75,buff=0,color=BLACK_LINE), self.mini_tag("v–t",26), Arrow(ORIGIN,RIGHT*0.75,buff=0,color=BLACK_LINE), self.mini_tag("a–t",26)).arrange(RIGHT,buff=0.22).move_to(DOWN*3.35)\n''',
'''        # Two-line interpretation labels: each belongs to one graph and stays inside\n        # its own horizontal footprint.\n        questions = VGroup(\n            VGroup(self.text("WHERE IS", 18, BOLD), self.text("THE OBJECT?", 18, BOLD)).arrange(DOWN, buff=0.02),\n            VGroup(self.text("HOW FAST IS", 18, BOLD), self.text("POSITION CHANGING?", 18, BOLD)).arrange(DOWN, buff=0.02),\n            VGroup(self.text("HOW FAST IS", 18, BOLD), self.text("VELOCITY CHANGING?", 18, BOLD)).arrange(DOWN, buff=0.02),\n        )\n        for q, center in zip(questions, centers):\n            q.move_to(center + DOWN*2.25)\n        self.play(LaggedStart(*[FadeIn(q, shift=UP*0.06) for q in questions], lag_ratio=0.16), run_time=1.3)\n        bridge = VGroup(self.mini_tag("x–t", 25), Arrow(ORIGIN,RIGHT*0.70,buff=0,color=BLACK_LINE), self.mini_tag("v–t",25), Arrow(ORIGIN,RIGHT*0.70,buff=0,color=BLACK_LINE), self.mini_tag("a–t",25)).arrange(RIGHT,buff=0.20).move_to(DOWN*3.48)\n''',
    ),
    (
        'Al = self.text("observer A",20,BOLD).next_to(A,DOWN,buff=0.12)',
        'Al = self.text("observer A",18,BOLD).move_to(LEFT*3.8+DOWN*1.48)',
    ),
    (
        'Bl = self.text("moving observer B",20,BOLD).next_to(B,DOWN,buff=0.12)',
        'Bl = self.text("moving observer B",18,BOLD).move_to(RIGHT*1.6+DOWN*1.48)',
    ),
    (
        'vb = Arrow(B.get_center()+DOWN*0.92, B.get_center()+RIGHT*1.7+DOWN*0.92, buff=0, color=BLACK_LINE, stroke_width=3)',
        'vb = Arrow(B.get_center()+UP*0.58, B.get_center()+RIGHT*1.7+UP*0.58, buff=0, color=BLACK_LINE, stroke_width=3)',
    ),
    (
        ').arrange(DOWN,buff=0.14).move_to(LEFT*3.8+UP*0.45)',
        ').arrange(DOWN,buff=0.14).move_to(LEFT*3.8+UP*0.88)',
    ),
]

for old, new in replacements:
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"Patch invariant failed: expected exactly one match, got {count}: {old[:100]!r}")
    s = s.replace(old, new)

path.write_text(s, encoding="utf-8")
print(f"Applied {len(replacements)} final V3 layout corrections to {path}")
