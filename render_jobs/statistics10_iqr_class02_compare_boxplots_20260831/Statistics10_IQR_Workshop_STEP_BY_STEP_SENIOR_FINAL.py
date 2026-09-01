#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior-final wrapper for the Statistics 10 IQR step-by-step workshop.

This file deliberately reuses the validated workshop implementation and overrides
only the scenes that need tighter projector-safe vertical composition after the
literal PQL runtime gate.  The inherited construct() dispatches to these methods.

Target: ManimCE 0.20.1, literal -pql gate followed by literal -pqh render.
"""

from manim import *

from Statistics10_IQR_Workshop_STEP_BY_STEP_FINAL import (
    Statistics10IQRWorkshopStepByStepFinal,
    GROUP_A,
    GROUP_B,
    modified_box_summary,
)
from jp_classroom_style import *


class Statistics10IQRWorkshopStepByStepSeniorFinal(Statistics10IQRWorkshopStepByStepFinal):
    """Projector-safe senior QA pass over the full numbered workshop."""

    def problem6_compare_groups(self) -> None:
        self.set_header(
            7,
            "PROBLEM 6 — COMPARE TWO GROUPS",
            "Use the same numerical scale. Compare center first, then IQR, then whiskers and outliers.",
        )
        a, b = modified_box_summary(GROUP_A), modified_box_summary(GROUP_B)
        axis = self.axis(35, 80, 5, y=-2.62, length=12.5)
        pa = self.boxplot(axis, a, y=0.30, label="A")
        pb = self.boxplot(axis, b, y=-0.90, label="B")
        self.play(Create(axis), Create(pa), Create(pb), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        center = self.step_row(
            1,
            "CENTER",
            self.math(
                r"Q_{2,A}=51\quad\text{vs}\quad Q_{2,B}=54.5"
                r"\;\Rightarrow\;B\text{ has the higher center}",
                27,
            ),
            y=1.88,
        )
        spread = self.step_row(
            2,
            "IQR",
            self.math(
                r"IQR_A=11.5\quad\text{vs}\quad IQR_B=5"
                r"\;\Rightarrow\;B\text{ is more tightly clustered}",
                26,
            ),
            y=1.18,
        )
        outlier = self.step_row(
            3,
            "OUTLIER",
            self.math(
                r"75>UF_B=65\;\Rightarrow\;75\text{ is a Group B outlier}",
                27,
            ),
            y=-1.78,
        )
        self.reveal_rows([center, spread, outlier], pause=PAUSE_EXPLAIN)
        self.wait(PAUSE_READ)

        # Senior-QA correction: the conclusion receives a dedicated uncluttered
        # presentation state instead of competing with the axis or boxplots.
        self.play(
            FadeOut(VGroup(center, spread, outlier, axis, pa, pb)),
            run_time=RUN_QUICK,
        )
        conclusion = self.note_panel(
            "Statistical conclusion",
            [
                "Group B has the higher typical value.",
                "Its middle 50% is more tightly clustered.",
                "It also contains one high outlier: 75.",
            ],
            width=8.9,
            body_size=22,
        )
        conclusion.move_to([0, 0.25, 0])
        self.assert_content_safe(conclusion, "comparison conclusion panel")
        self.play(FadeIn(conclusion, shift=UP * 0.05), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def independent_practice(self) -> None:
        self.set_header(
            8,
            "YOUR TURN — INDEPENDENT PRACTICE",
            "Pause the video. Solve each prompt using the numbered routine before checking the answer key.",
        )
        prompts = VGroup(
            self.note_panel(
                "A · Quartiles + IQR",
                ["Data: 6, 8, 9, 10, 12, 13, 15, 17", "Find Q1, Q2, Q3 and IQR."],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "B · Outlier test",
                ["Data: 5, 6, 7, 9, 10, 11, 12, 30", "Find the fences and classify 30."],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "C · Interpretation",
                ["Which group is more consistent?", "A: IQR = 11.5   B: IQR = 5"],
                width=6.4,
                body_size=22,
            ),
            self.note_panel(
                "D · Explain",
                ["Why does a whisker stop at 10", "while 24 is still in the dataset?"],
                width=6.4,
                body_size=22,
            ),
        )
        prompts.arrange_in_grid(rows=2, cols=2, buff=(0.42, 0.34))
        self.fit(prompts, 13.5, 4.65)
        prompts.move_to(DOWN * 0.38)
        self.assert_content_safe(prompts, "practice prompts")
        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.04) for p in prompts], lag_ratio=0.10),
            run_time=RUN_SLOW,
        )
        pause = self.text("PAUSE HERE · show all calculations in your notebook", 25, BOLD)
        self.fit(pause, 11.8, 0.44)
        pause.move_to([0, -3.00, 0])
        self.assert_content_safe(pause, "practice pause instruction")
        self.play(FadeIn(pause), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL * 1.55)
        self.clear_stage()

    def final_summary(self) -> None:
        self.set_header(
            11,
            "THE ROUTINE TO REMEMBER",
            "Use this exact sequence whenever you solve an IQR / modified-boxplot problem.",
        )
        routine = VGroup(
            self.step_badge(1, "ORDER DATA", width=2.55),
            self.step_badge(2, "FIND Q1,Q2,Q3", width=2.55),
            self.step_badge(3, "CALCULATE IQR", width=2.55),
            self.step_badge(4, "FIND FENCES", width=2.55),
            self.step_badge(5, "CLASSIFY", width=2.55),
            self.step_badge(6, "DRAW / INTERPRET", width=2.55),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.48, 0.30))
        routine.move_to(DOWN * 0.22)
        self.assert_content_safe(routine, "final routine")
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.04) for r in routine], lag_ratio=0.10),
            run_time=RUN_SLOW,
        )
        line = self.text("Center → spread → whiskers → outliers → conclusion", 28, BOLD)
        self.fit(line, 10.8, 0.46)
        line.move_to([0, -2.93, 0])
        self.assert_content_safe(line, "final summary line")
        self.play(FadeIn(line), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)


if __name__ == "__main__":
    pass
