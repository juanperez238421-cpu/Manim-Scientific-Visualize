from pathlib import Path
import sys

path = Path(sys.argv[1])
s = path.read_text()

def rep(old, new, count=None):
    global s
    n = s.count(old)
    if count is not None and n != count:
        raise RuntimeError(f"Expected {count} occurrences, found {n}: {old[:80]!r}")
    if n == 0:
        raise RuntimeError(f"Pattern not found: {old[:120]!r}")
    s = s.replace(old, new)

rep('class Geometry8Week2SeniorV4(JPMathClassroomScene):', 'class Geometry8Week2SeniorV5(JPMathClassroomScene):', 1)
rep('title_text = self.text(title, 36, BOLD)', 'title_text = self.text(title, 38, BOLD)', 1)
rep('sub = self.text(subtitle, 25)', 'sub = self.text(subtitle, 28)', 1)
rep('self.fit(sub, 14.25, 0.48)', 'self.fit(sub, 14.25, 0.54)', 1)
rep('heading = self.text(title, 32, BOLD)', 'heading = self.text(title, 34, BOLD)', 1)
rep('body = VGroup(*[self.text(line, 29) for line in lines])', 'body = VGroup(*[self.text(line, 30) for line in lines])', 1)

for old, new in {
    'Shape first → measurement second → formula third.': 'Shape → measurement → formula.',
    'Bases are parallel. Height is perpendicular. Legs belong to the boundary.': 'Parallel bases. Perpendicular height. Legs are boundary.',
    'Trace the outer border first. Build the sum from the traced sides.': 'Trace the outside. Build the sum one side at a time.',
    'Cut → separate → calculate each region → reassemble.': 'Cut → separate → calculate → rebuild.',
    'Duplicate one trapezoid. Rotate it. Join the pair into a parallelogram.': 'Duplicate. Rotate. Join. Compare the areas.',
    'Perimeter activates the border. Area activates the bases and perpendicular height.': 'Border question vs. interior question.',
    'Four equal sides make the perimeter a repeated-addition problem.': 'Four equal sides. Trace each side once.',
    'Diagonals split the rhombus into four congruent right triangles.': 'Diagonals create four congruent right triangles.',
    'If every side has length s and there are n sides, then P = ns.': 'Equal side s repeated n times: P = ns.',
    'Use familiar shapes inside the figure instead of inventing a new formula.': 'Split the figure into familiar shapes.',
    'Use one decision at a time. Keep the units consistent with what is measured.': 'Decide: border or interior. Then choose units.',
}.items():
    rep(old, new, 1)

rep('''t = self.build_trapezoid(scale=0.53, values=False)\n        t["group"].shift(LEFT * 3.45 + DOWN * 0.45)\n        anchor = RIGHT * 3.45 + DOWN * 0.20''',
    '''t = self.build_trapezoid(scale=0.50, values=False)\n        t["group"].shift(LEFT * 3.80 + DOWN * 0.45)\n        anchor = RIGHT * 4.35 + DOWN * 0.20''', 1)
rep('width=6.15).move_to(card_anchor)', 'width=5.55).move_to(card_anchor)', 3)

rep('''        self.play(FadeOut(cut_note), FadeOut(t["fill"]), FadeOut(t["labels"]),\n                  FadeIn(tri_l), FadeIn(rect), FadeIn(tri_r), run_time=RUN_NORMAL)\n        # Separate pieces far enough that no outlines merge visually.\n        self.play(\n            tri_l.animate.move_to(LEFT * 4.65 + DOWN * 0.20),\n            rect.animate.move_to(ORIGIN + DOWN * 0.20),\n            tri_r.animate.move_to(RIGHT * 4.65 + DOWN * 0.20),\n            t["edges"].animate.set_stroke(opacity=0.12),\n            cut_l.animate.set_stroke(opacity=0.12), cut_r.animate.set_stroke(opacity=0.12),\n            run_time=RUN_SLOW,\n        )''',
'''        self.play(FadeOut(cut_note), FadeOut(t["fill"]), FadeOut(t["labels"]),\n                  FadeIn(tri_l), FadeIn(rect), FadeIn(tri_r), run_time=RUN_NORMAL)\n        # Remove the original outline before the pieces move.\n        self.play(FadeOut(t["edges"]), FadeOut(cut_l), FadeOut(cut_r), run_time=RUN_QUICK)\n        self.play(\n            tri_l.animate.move_to(LEFT * 4.65 + DOWN * 0.20),\n            rect.animate.move_to(ORIGIN + DOWN * 0.20),\n            tri_r.animate.move_to(RIGHT * 4.65 + DOWN * 0.20),\n            run_time=RUN_SLOW,\n        )''', 1)
rep('''        self.play(t["edges"].animate.set_stroke(opacity=1.0),\n                  cut_l.animate.set_stroke(opacity=1.0), cut_r.animate.set_stroke(opacity=1.0), run_time=RUN_QUICK)''',
    '''        self.play(FadeIn(t["edges"]), FadeIn(cut_l), FadeIn(cut_r), run_time=RUN_QUICK)''', 1)

rep('''        r = self.build_rhombus(scale=0.46, values=True)\n        r["group"].shift(LEFT * 3.55 + DOWN * 0.45)\n        self.play(FadeIn(r["fill"]), Create(r["edges"]), FadeIn(r["ticks"]), FadeIn(r["labels"][2]), run_time=RUN_NORMAL)''',
'''        r = self.build_rhombus(scale=0.46, values=True)\n        r["group"].shift(LEFT * 3.45 + DOWN * 0.45)\n        side_label = self.math(r"s=10\\,\\mathrm{cm}", 43).move_to(LEFT * 5.05 + UP * 1.38)\n        self.play(FadeIn(r["fill"]), Create(r["edges"]), FadeIn(r["ticks"]), FadeIn(side_label), run_time=RUN_NORMAL)''', 1)
rep('TransformFromCopy(r["labels"][2], terms[i])', 'TransformFromCopy(side_label, terms[i])', 1)

rep('''        # Isolate one triangle and show its half-diagonal legs in large type.\n        self.play(FadeOut(names), tris[1].animate.set_opacity(0.18), tris[2].animate.set_opacity(0.18),\n                  tris[3].animate.set_opacity(0.18), run_time=RUN_QUICK)\n        legD = self.math(r"D/2=8\\,\\mathrm{cm}", 45).move_to(LEFT * 0.75 + UP * 1.25)\n        legd = self.math(r"d/2=6\\,\\mathrm{cm}", 45).move_to(LEFT * 0.75 + UP * 0.50)\n        eq1 = self.math(r"A_{1\\triangle}=\\frac12(8)(6)=24\\,\\mathrm{cm}^2", 49).move_to(LEFT * 0.25 + DOWN * 0.55)\n        eq2 = self.math(r"A=4(24)=96\\,\\mathrm{cm}^2", 52).move_to(LEFT * 0.25 + DOWN * 1.65)\n        eq3 = self.math(r"\\boxed{A=\\frac{Dd}{2}}", 58).move_to(LEFT * 0.25 + DOWN * 2.85)''',
'''        # Isolate one triangle completely. No translucent pieces remain behind the math.\n        self.play(FadeOut(names), FadeOut(tris[1]), FadeOut(tris[2]), FadeOut(tris[3]),\n                  tris[0].animate.move_to(LEFT * 4.15 + DOWN * 0.25), run_time=RUN_NORMAL)\n        focus = self.text("ONE OF FOUR EQUAL TRIANGLES", 31, BOLD).next_to(tris[0], UP, buff=0.18)\n        legD = self.math(r"D/2=8\\,\\mathrm{cm}", 47).move_to(RIGHT * 2.45 + UP * 1.35)\n        legd = self.math(r"d/2=6\\,\\mathrm{cm}", 47).move_to(RIGHT * 2.45 + UP * 0.55)\n        eq1 = self.math(r"A_{1\\triangle}=\\frac12(8)(6)=24\\,\\mathrm{cm}^2", 49).move_to(RIGHT * 2.45 + DOWN * 0.40)\n        eq2 = self.math(r"A=4(24)=96\\,\\mathrm{cm}^2", 53).move_to(RIGHT * 2.45 + DOWN * 1.45)\n        eq3 = self.math(r"\\boxed{A=\\frac{Dd}{2}}", 60).move_to(RIGHT * 2.45 + DOWN * 2.55)\n        self.play(FadeIn(focus), run_time=RUN_QUICK)''', 1)

rep('''        self.play(FadeIn(rect), FadeIn(roof), house.animate.set_stroke(opacity=0.12), run_time=RUN_NORMAL)\n        self.play(rect.animate.shift(DOWN * 0.70), roof.animate.shift(UP * 0.85), run_time=RUN_SLOW)\n        self.wait(PAUSE_EXPLAIN)''',
'''        self.play(FadeIn(rect), FadeIn(roof), run_time=RUN_NORMAL)\n        self.play(FadeOut(house), FadeOut(split), FadeOut(altitude),\n                  FadeOut(base_lab), FadeOut(rect_h_lab), FadeOut(roof_h_lab), run_time=RUN_QUICK)\n        self.play(rect.animate.shift(DOWN * 0.78), roof.animate.shift(UP * 0.95), run_time=RUN_SLOW)\n        rect_dims = VGroup(\n            self.math(r"16\\,\\mathrm{cm}", 41).next_to(rect, DOWN, buff=0.14),\n            self.math(r"6\\,\\mathrm{cm}", 41).next_to(rect, LEFT, buff=0.14),\n        )\n        roof_dims = VGroup(\n            self.math(r"b=16\\,\\mathrm{cm}", 41).next_to(roof, DOWN, buff=0.14),\n            self.math(r"h=6\\,\\mathrm{cm}", 41).next_to(roof, RIGHT, buff=0.14),\n        )\n        self.play(FadeIn(rect_dims), FadeIn(roof_dims), run_time=RUN_NORMAL)\n        self.wait(PAUSE_EXPLAIN)''', 1)

path.write_text(s)
print(f"V5 patch applied to {path}")
