#!/usr/bin/env python3
"""Deterministically build V10.1 from the rendered V10 source.

Senior visual-QA corrections:
1) move meeting callouts away from the data chip and racers;
2) replace crowded per-row ratio arrows with two clean symbolic rules;
3) replace metadata Transform with a fade/change so intermediate glyphs never merge.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
src_path = ROOT / "achilles_tortoise_senior_v10.py"
out_path = ROOT / "achilles_tortoise_senior_v10_1.py"
s = src_path.read_text(encoding="utf-8")

s = s.replace(
    '"""Senior QA V10 continuous-diagram English reconstruction',
    '"""Senior QA V10.1 continuous-diagram English reconstruction',
    1,
)

old = 'meet_callout_group = VGroup(callout_box, meet_callout).move_to([4.25, 2.45, 0])'
new = 'meet_callout_group = VGroup(callout_box, meet_callout).move_to([4.90, 2.90, 0])'
assert old in s
s = s.replace(old, new, 1)

old = 'final_callout=VGroup(final_box,final_callout_text).move_to([4.15,2.42,0])'
new = 'final_callout=VGroup(final_box,final_callout_text).move_to([4.90,2.90,0])'
assert old in s
s = s.replace(old, new, 1)

old = '''                self.play(lens["runner"].animate.move_to([lens["x_l"],lens["y"]+0.62,0]),
                    lens["tortoise"].animate.move_to([lens["x_target"],lens["y"]+0.10,0]), Transform(lens["meta"],new_meta),
                    Transform(m["band"],new_band),Transform(m["connectors"],new_connectors),FadeOut(gap_visual),run_time=RUN_CAMERA,rate_func=smooth)'''
new = '''                old_meta = lens["meta"]
                self.play(
                    lens["runner"].animate.move_to([lens["x_l"],lens["y"]+0.62,0]),
                    lens["tortoise"].animate.move_to([lens["x_target"],lens["y"]+0.10,0]),
                    FadeOut(old_meta),
                    Transform(m["band"],new_band),
                    Transform(m["connectors"],new_connectors),
                    FadeOut(gap_visual),
                    run_time=RUN_CAMERA,
                    rate_func=smooth,
                )
                lens["meta"] = new_meta
                self.play(FadeIn(lens["meta"]), run_time=RUN_QUICK)'''
assert old in s
s = s.replace(old, new, 1)

old = '''        ratio_arrows=VGroup()
        for a,b in zip(times[:-1],times[1:]):
            arrow=Arrow(a.get_right()+RIGHT*0.16,b.get_right()+RIGHT*0.16,buff=0.02,color=MID_GRAY,stroke_width=1.5,max_tip_length_to_length_ratio=0.12)
            label=self.math(r"\\times\\frac{1}{10}",18).next_to(arrow,RIGHT,buff=0.05);ratio_arrows.add(VGroup(arrow,label))
        partials=VGroup(self.math(r"S_1=1.000",25),self.math(r"S_2=1.100",25),self.math(r"S_3=1.110",25),self.math(r"S_4=1.111",25)).arrange(DOWN,aligned_edge=LEFT,buff=0.14).move_to([3.25,-2.02,0])
        divider=Line([0,-0.92,0],[0,-3.10,0],color=LIGHT_GRAY,stroke_width=1.4)
        self.play(Write(left_title),Write(right_title),Create(divider),run_time=RUN_NORMAL)
        for i in range(4):
            self.play(Write(times[i]),Write(partials[i]),run_time=RUN_NORMAL)
            if i<3:self.play(GrowArrow(ratio_arrows[i][0]),Write(ratio_arrows[i][1]),run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT*0.35)
        pattern_line=self.math(r"\\Delta t_n=\\left(\\frac{1}{10}\\right)^{n-1}\\mathrm{s}",29).move_to([0,-3.35,0])
        self.play(Write(pattern_line),run_time=RUN_NORMAL);self.wait(PAUSE_READ)
        step1_group=VGroup(left_title,right_title,times,ratio_arrows,partials,divider,pattern_line)'''
new = '''        ratio_rule = self.math(
            r"\\Delta t_{n+1}=\\frac{1}{10}\\Delta t_n",
            25,
        ).move_to([-3.55,-3.22,0])
        partials=VGroup(self.math(r"S_1=1.000",25),self.math(r"S_2=1.100",25),self.math(r"S_3=1.110",25),self.math(r"S_4=1.111",25)).arrange(DOWN,aligned_edge=LEFT,buff=0.14).move_to([3.25,-2.02,0])
        divider=Line([0,-0.92,0],[0,-3.10,0],color=LIGHT_GRAY,stroke_width=1.4)
        self.play(Write(left_title),Write(right_title),Create(divider),run_time=RUN_NORMAL)
        for i in range(4):
            self.play(Write(times[i]),Write(partials[i]),run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT*0.35)
        pattern_line=self.math(r"\\Delta t_n=\\left(\\frac{1}{10}\\right)^{n-1}\\mathrm{s}",25).move_to([3.25,-3.22,0])
        self.play(Write(ratio_rule), Write(pattern_line),run_time=RUN_NORMAL);self.wait(PAUSE_READ)
        step1_group=VGroup(left_title,right_title,times,ratio_rule,partials,divider,pattern_line)'''
assert old in s
s = s.replace(old, new, 1)

out_path.write_text(s, encoding="utf-8")
print(out_path)
