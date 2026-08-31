#!/usr/bin/env python3
"""Generate the Senior-QA V2 lesson from the committed V1 source.

This deliberately patches the exact V1 source instead of rewriting the lesson from
scratch, so Git history preserves a reproducible V1 -> V2 transformation.
"""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_senior_qa_v2.py INPUT.py OUTPUT.py")

src = Path(sys.argv[1])
out = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global s
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    s = s.replace(old, new, 1)


replace_once(
    "Primary emphasis: construction -> interpretation -> comparison -> justification.\n",
    "Primary emphasis: construction -> interpretation -> comparison -> justification.\n"
    "Senior QA V2: improved graph-domain accuracy, stronger visual focus, larger comparison annotations, and clearer conceptual transitions.\n",
    "version note",
)

replace_once(
    "CHALLENGE_D = (13, 15, 16, 17, 18, 19, 20, 32)\n",
    "CHALLENGE_D = (13, 15, 16, 17, 18, 19, 20, 32)\n"
    "READ_EXAMPLE = (3, 8, 9, 11, 13, 16, 18, 35)\n",
    "read dataset",
)

replace_once(
    '''        # Exit ticket.\n        assert_close(26 - 18, 8, label="exit IQR")\n''',
    '''        read_ex = modified_box_summary(READ_EXAMPLE)\n        assert (read_ex.q1, read_ex.q2, read_ex.q3) == (8.5, 12.0, 17.0)\n        assert_close(read_ex.iqr, 8.5, label="read example IQR")\n        assert_close(read_ex.uf, 29.75, label="read example upper fence")\n        assert read_ex.outliers == (35.0,)\n        # Domain guard: every plotted value must lie on the visible axis.\n        assert min(READ_EXAMPLE) >= 0 and max(READ_EXAMPLE) <= 40\n\n        # Exit ticket.\n        assert_close(26 - 18, 8, label="exit IQR")\n''',
    "validation guard",
)

replace_once(
    '''        route = self.process_map(\n            [\n                ("1", "ORDER"),\n                ("2", "QUARTILES"),\n                ("3", "IQR"),\n                ("4", "BOXPLOT"),\n                ("5", "INTERPRET"),\n                ("6", "COMPARE"),\n            ],\n            card_width=2.15,\n            card_height=0.90,\n            columns=6,\n        )\n        route.move_to(DOWN * 0.62)\n''',
    '''        route = self.process_map(\n            [\n                ("1", "CLASSIFY"),\n                ("2", "DRAW"),\n                ("3", "READ"),\n                ("4", "COMPARE"),\n            ],\n            card_width=3.05,\n            card_height=1.02,\n            columns=4,\n        )\n        route.move_to(DOWN * 0.62)\n''',
    "opening route",
)

replace_once(
    '''        # Final two actions become the focus without adding decorative color.\n        self.play(route[4].animate.scale(1.08), route[5].animate.scale(1.08), run_time=RUN_NORMAL)\n''',
    '''        # Reading and comparing are today's new focus.\n        self.play(route[2].animate.scale(1.08), route[3].animate.scale(1.08), run_time=RUN_NORMAL)\n''',
    "opening focus",
)

replace_once(
    '''        self.animate_equation_stack(equations, pause=PAUSE_SHORT)\n        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)\n        self.wait(PAUSE_WORK)\n''',
    '''        self.animate_equation_stack(equations, pause=PAUSE_SHORT)\n        self.play(Circumscribe(equations[3], color=BLACK_LINE, buff=0.08), run_time=RUN_NORMAL)\n        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)\n        self.play(Circumscribe(interpretation[1][1][-1], color=BLACK_LINE, buff=0.06), run_time=RUN_NORMAL)\n        self.wait(PAUSE_WORK)\n''',
    "worked-example focus",
)

replace_once(
    '''        summary = modified_box_summary([3, 8, 9, 11, 13, 16, 18, 35])\n        axis = self.common_axis(0, 30, 5, length=12.4, y=-2.15)\n        plot = self.boxplot_on_axis(axis, summary, y=0.65, label="EXAMPLE")\n        self.play(Create(axis), Create(plot), run_time=RUN_SLOW)\n\n        qlabels = VGroup(\n            self.math(rf"Q_1={self._fmt(summary.q1)}", 26).move_to([axis.n2p(summary.q1)[0], 1.45, 0]),\n            self.math(rf"Q_2={self._fmt(summary.q2)}", 26).move_to([axis.n2p(summary.q2)[0], 1.45, 0]),\n            self.math(rf"Q_3={self._fmt(summary.q3)}", 26).move_to([axis.n2p(summary.q3)[0], 1.45, 0]),\n        )\n        self.play(FadeIn(qlabels), run_time=RUN_NORMAL)\n''',
    '''        summary = modified_box_summary(READ_EXAMPLE)\n        # Senior-QA fix: the axis must include the outlier at 35.\n        axis = self.common_axis(0, 40, 5, length=12.4, y=-2.15)\n        plot = self.boxplot_on_axis(axis, summary, y=0.65, label="EXAMPLE")\n        self.play(Create(axis), Create(plot), run_time=RUN_SLOW)\n\n        qlabels = VGroup(\n            self.math(rf"Q_1={self._fmt(summary.q1)}", 27).move_to([axis.n2p(summary.q1)[0], 1.45, 0]),\n            self.math(rf"Q_2={self._fmt(summary.q2)}", 27).move_to([axis.n2p(summary.q2)[0], 1.45, 0]),\n            self.math(rf"Q_3={self._fmt(summary.q3)}", 27).move_to([axis.n2p(summary.q3)[0], 1.45, 0]),\n        )\n        self.play(FadeIn(qlabels), run_time=RUN_NORMAL)\n\n        uf_x = axis.n2p(summary.uf)[0]\n        uf_guide = DashedLine([uf_x, -1.35, 0], [uf_x, 1.20, 0], color=MID_GRAY, stroke_width=2.0)\n        uf_label = self.math(rf"UF={self._fmt(summary.uf)}", 25).next_to(uf_guide, UP, buff=0.06)\n        outlier_ring = Circle(radius=0.18, stroke_color=BLACK_LINE, stroke_width=2.4, fill_opacity=0).move_to([axis.n2p(35)[0], 0.65, 0])\n        outlier_note = self.text("35 is beyond the upper fence", 23, BOLD).next_to(outlier_ring, UP, buff=0.20)\n        self.fit(outlier_note, 4.5, 0.50)\n        self.play(Create(uf_guide), FadeIn(uf_label), Create(outlier_ring), FadeIn(outlier_note), run_time=RUN_NORMAL)\n''',
    "read graph axis and outlier focus",
)

replace_once(
    '''        data_a = self.text("A: 40, 44, 47, 50, 52, 55, 59, 63", 22)\n        data_b = self.text("B: 49, 52, 53, 54, 55, 57, 58, 75", 22)\n''',
    '''        data_a = self.text("A: 40, 44, 47, 50, 52, 55, 59, 63", 24)\n        data_b = self.text("B: 49, 52, 53, 54, 55, 57, 58, 75", 24)\n''',
    "comparison data size",
)

replace_once(
    '''        self.play(Create(guides), run_time=RUN_NORMAL)\n        self.play(FadeIn(statement, shift=UP * 0.06), run_time=RUN_NORMAL)\n        self.wait(PAUSE_EXPLAIN)\n        self.play(FadeOut(guides), FadeOut(statement), run_time=RUN_QUICK)\n''',
    '''        focus_a = RoundedRectangle(width=0.42, height=1.18, corner_radius=0.06, stroke_color=MID_GRAY, stroke_width=1.6, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.30).move_to([axis.n2p(a.q2)[0], 0.70, 0])\n        focus_b = RoundedRectangle(width=0.42, height=1.18, corner_radius=0.06, stroke_color=MID_GRAY, stroke_width=1.6, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.30).move_to([axis.n2p(b.q2)[0], -0.80, 0])\n        self.play(Create(guides), FadeIn(focus_a), FadeIn(focus_b), run_time=RUN_NORMAL)\n        self.play(FadeIn(statement, shift=UP * 0.06), run_time=RUN_NORMAL)\n        self.wait(PAUSE_EXPLAIN)\n        self.play(FadeOut(guides), FadeOut(focus_a), FadeOut(focus_b), FadeOut(statement), run_time=RUN_QUICK)\n''',
    "median visual focus",
)

replace_once(
    '''            self.text("A lower: 40 to 45.5", 21, BOLD).move_to([axis.n2p(43)[0], 1.42, 0]),\n            self.text("A upper: 57 to 63", 21, BOLD).move_to([axis.n2p(60)[0], 1.42, 0]),\n            self.text("B lower: 49 to 52.5", 21, BOLD).move_to([axis.n2p(50.7)[0], -1.55, 0]),\n            self.text("B upper: 57.5 to 58", 21, BOLD).move_to([axis.n2p(58)[0], -1.55, 0]),\n''',
    '''            self.text("A lower: 40 to 45.5", 23, BOLD).move_to([axis.n2p(43)[0], 1.42, 0]),\n            self.text("A upper: 57 to 63", 23, BOLD).move_to([axis.n2p(60)[0], 1.42, 0]),\n            self.text("B lower: 49 to 52.5", 23, BOLD).move_to([axis.n2p(50.7)[0], -1.55, 0]),\n            self.text("B upper: 57.5 to 58", 23, BOLD).move_to([axis.n2p(58)[0], -1.55, 0]),\n''',
    "whisker label size",
)

replace_once(
    '''            24,\n            BOLD,\n        ).to_edge(UP, buff=1.58)\n''',
    '''            26,\n            BOLD,\n        ).to_edge(UP, buff=1.58)\n''',
    "student challenge size",
)

out.write_text(s, encoding="utf-8")
print(f"Senior-QA V2 source written: {out}")
