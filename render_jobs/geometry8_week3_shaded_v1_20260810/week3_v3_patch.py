from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
s=s.replace('class Geometry8Week3ShadedAreasSeniorV2(JPMathClassroomScene):','class Geometry8Week3ShadedAreasSeniorV3(JPMathClassroomScene):')
old1='''        eqs1 = VGroup(left_eq, right_eq, sum_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.26)\n        eqs1.move_to(RIGHT * 3.80 + DOWN * 0.35)\n'''
new1='''        eqs1 = VGroup(left_eq, right_eq, sum_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.26)\n        self.fit(eqs1, 5.75, 3.55)\n        eqs1.move_to(RIGHT * 4.20 + DOWN * 0.35)\n'''
old2='''        eqs2 = VGroup(whole, middle, diff).arrange(DOWN, aligned_edge=LEFT, buff=0.26)\n        eqs2.move_to(RIGHT * 3.80 + DOWN * 0.35)\n'''
new2='''        eqs2 = VGroup(whole, middle, diff).arrange(DOWN, aligned_edge=LEFT, buff=0.26)\n        self.fit(eqs2, 5.75, 3.55)\n        eqs2.move_to(RIGHT * 4.20 + DOWN * 0.35)\n'''
if old1 not in s or old2 not in s:
    raise SystemExit('Expected V2 equation blocks not found')
s=s.replace(old1,new1).replace(old2,new2)
s=s.replace('method1.move_to(RIGHT * 3.75 + UP * 1.65)','method1.move_to(RIGHT * 4.15 + UP * 1.65)')
s=s.replace('method2.move_to(RIGHT * 3.75 + UP * 1.65)','method2.move_to(RIGHT * 4.15 + UP * 1.65)')
p.write_text(s)
print('V3 equation-panel QA patch complete')
