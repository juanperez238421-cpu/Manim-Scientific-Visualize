#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior V2 final wrapper for the Physics 9 bus light-clock lesson.

The complete lesson is inherited from V1. This final wrapper tightens the
closing composition and adds a hard frame-safety assertion so the final
summary cannot be clipped at the lower projector edge.
"""

from physics9_bus_light_clock_v1 import *


class Physics9BusLightClockV2Final(Physics9BusLightClockV1):
    """Final QA-safe version of the full time-dilation lesson."""

    def summary(self):
        h = self.header(
            10,
            "IDEA CENTRAL: QUÉ DEBE PODER REPRODUCIR EL ESTUDIANTE",
            "La dilatación temporal aparece al exigir que ambos observadores midan la misma velocidad de la luz.",
        )
        self.play(FadeIn(h), run_time=RUN_FAST)

        labels = [
            ("1", "ANA: luz vertical"),
            ("2", "CARLOS: luz diagonal"),
            ("3", "Pitágoras"),
            ("4", "L = ct₀"),
            ("5", "Despejar t"),
            ("6", "v = 0.60c → 1.25"),
        ]

        cards = VGroup()
        for num, text in labels:
            box = RoundedRectangle(
                width=4.20,
                height=1.08,
                corner_radius=0.11,
                stroke_color=DARK,
                stroke_width=1.7,
                fill_color=WHITE,
                fill_opacity=1,
            )
            nbox = RoundedRectangle(
                width=0.56,
                height=0.56,
                corner_radius=0.08,
                stroke_color=INK,
                stroke_width=1.7,
                fill_color=PAPER,
                fill_opacity=1,
            )
            ntext = self.txt(num, 20, BOLD).move_to(nbox)
            label = self.fit(self.txt(text, 20, BOLD), 3.18, 0.58)
            row = VGroup(VGroup(nbox, ntext), label).arrange(RIGHT, buff=0.20).move_to(box)
            cards.add(VGroup(box, row))

        cards.arrange_in_grid(rows=2, cols=3, buff=(0.34, 0.28)).move_to(UP * 0.78)

        formula = self.formula_box(
            r"t=\frac{t_0}{\sqrt{1-\frac{v^2}{c^2}}}",
            7.1,
            1.05,
            40,
        ).move_to(DOWN * 1.25)

        result = self.formula_box(
            r"10\,\mathrm{ns}\longrightarrow12.5\,\mathrm{ns}\quad(v=0.60c)",
            8.4,
            0.96,
            34,
        )
        result.next_to(formula, DOWN, buff=0.20)

        close = self.text_box(
            "Newton funciona muy bien cuando v ≪ c. Cerca de c, el tiempo deja de ser absoluto.",
            12.5,
            0.82,
            22,
            True,
            fill=PAPER,
        )
        close.next_to(result, DOWN, buff=0.20)

        # Hard QA gate: the complete closing layout must fit in the 16:9 frame.
        final_layout = VGroup(h, cards, formula, result, close)
        self.assert_frame(final_layout, "summary_v2_final", margin=0.08)

        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.08) for card in cards],
                lag_ratio=0.12,
            ),
            run_time=RUN_SLOW * 1.8,
        )
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(result), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(close), run_time=RUN)
        self.wait(PAUSE_FINAL)


# Preview:
#   manim -pql physics9_bus_light_clock_v2_final.py Physics9BusLightClockV2Final --disable_caching
# Final:
#   manim -pqh physics9_bus_light_clock_v2_final.py Physics9BusLightClockV2Final --disable_caching
