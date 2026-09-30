#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 Circle — Pedagogical Sequence Senior QA V2.

Runtime-only follow-up to Geometry8CirclePedagogicalSequenceSeniorQA.

The full PQL audit reached the final Exit Ticket and exposed one Manim object-
hierarchy edge case: ReplacementTransform on the nested exit-ticket groups can
leave shared family members in ``self.mobjects``.  The inherited generic
``standard_closing()`` then bulk-FadeOuts every top-level mobject and Manim may
attempt to animate a repeated child, raising ``TypeError: ... cannot be
converted to an animation``.

V2 preserves the complete approved master scene and every prior QA layout fix.
Only ``exit_ticket_qa()`` is overridden so the final teaching state is removed
cleanly before a fresh, projector-size closing sentence is animated.
"""
from __future__ import annotations

from manim import *
from Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA import (
    Geometry8CirclePedagogicalSequenceSeniorQA,
)


class Geometry8CirclePedagogicalSequenceSeniorQAV2(
    Geometry8CirclePedagogicalSequenceSeniorQA
):
    """Final runtime-safe revision of the approved pedagogical master scene."""

    def exit_ticket_qa(self) -> None:
        self.set_header(
            11,
            "EXIT TICKET",
            "Three quick checks: identify, relate, choose.",
        )
        questions = [
            (
                "1 — IDENTIFY",
                "A line touches a circle at one point. Name it.",
                "TANGENT",
                False,
            ),
            (
                "2 — RELATE",
                "Central angle = 90°. Same-arc inscribed angle = ?",
                r"45^\circ",
                True,
            ),
            (
                "3 — CHOOSE",
                "Paint covers a circular logo: circumference or area?",
                "AREA",
                False,
            ),
        ]

        holder = RoundedRectangle(
            width=12.6,
            height=4.25,
            corner_radius=0.14,
            stroke_color=BLACK_LINE,
            stroke_width=2.1,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).move_to(DOWN * 0.38)
        self.play(FadeIn(holder), run_time=RUN_NORMAL)

        current = None
        for idx, (title, question, answer_text, is_math) in enumerate(
            questions,
            start=1,
        ):
            index = self.text(
                f"QUESTION {idx} OF 3",
                28,
                BOLD,
            ).next_to(holder.get_top(), DOWN, buff=0.28)
            title_m = self.text(title, 34, BOLD)
            body = self.text(question, 31)
            self.fit(body, 10.6, 0.78)
            prompt = (
                VGroup(title_m, body)
                .arrange(DOWN, buff=0.30)
                .move_to(holder)
                .shift(UP * 0.35)
            )
            answer = (
                self.math(answer_text, 48)
                if is_math
                else self.text(answer_text, 40, BOLD)
            )
            answer.next_to(prompt, DOWN, buff=0.45)
            state = VGroup(index, prompt)

            if current is None:
                self.play(FadeIn(state), run_time=RUN_NORMAL)
            else:
                self.play(
                    ReplacementTransform(current, state),
                    run_time=RUN_NORMAL,
                )
            self.wait(5.0)
            self.play(FadeIn(answer), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
            self.play(FadeOut(answer), run_time=RUN_QUICK)
            current = state

        self.wait(PAUSE_FINAL)

        # Runtime QA fix: do not bulk-FadeOut a hierarchy that has undergone
        # nested ReplacementTransform operations. Remove it atomically, reset
        # the persistent-header references, then animate one fresh closing.
        self.remove(*list(self.mobjects))
        self.header_group = None
        self.subtitle_group = None

        closing = self.text(
            "Workshop complete — circle fundamentals are ready for the next unit.",
            40,
            BOLD,
        )
        self.fit(closing, 13.8, 1.25)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)


# Preview QA:
# LESSON_TIME_SCALE=0.08 manim -pql \
#   Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA_V2.py \
#   Geometry8CirclePedagogicalSequenceSeniorQAV2 \
#   --fps 15 --disable_caching
#
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh \
#   Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA_V2.py \
#   Geometry8CirclePedagogicalSequenceSeniorQAV2 \
#   --fps 30 --disable_caching
