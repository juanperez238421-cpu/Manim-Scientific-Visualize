#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle — Pedagogical Sequence Senior QA.

Single ManimCE master scene matching the approved pedagogical PDF order:
    Fundamentals -> Class 2 (Parts, Arcs and Lines) -> bridge -> Workshop.

QA focus
--------
The original workshop builds six 5.7-unit cards (PROBLEM / THINK / STRATEGY /
SOLVE / CHECK / ANSWER), arranges them vertically, then fits the entire stack
inside a 5.35-unit content height. That uniform fit is the direct reason some
workshop text and boxes become too small for projection.

This revision preserves the exact existing workshop methods and data, but
intercepts `_show_guided_solution()` after layout. Each card is restored to
projector scale and presented sequentially. The final state keeps PROBLEM plus
SOLVE + CHECK + ANSWER visible at readable size.

Target: Manim Community Edition 0.20.1 + jp_classroom_style.py
Final scene: Geometry8CirclePedagogicalSequenceSeniorQA
"""
from __future__ import annotations

import math
import numpy as np
from manim import *

from jp_classroom_style import *
from Geometry8_Circle_Fundamentals_FINAL import Geometry8CircleFundamentalsFinal
from Geometry8_Circle_Class2_Parts_Arcs import Geometry8CircleClass2PartsArcs
from Geometry8_Circle_Workshop_FINAL import Geometry8CircleWorkshopFinal


QA_CARD_WIDTH = 5.85
QA_RIGHT_X = 4.25
QA_PROBLEM_Y = 1.55
QA_FINAL_MAX_HEIGHT = 4.05


class Geometry8CirclePedagogicalSequenceSeniorQA(Geometry8CircleWorkshopFinal):
    """Master lesson reproducing the PDF sequence with workshop projection QA."""

    # ------------------------------------------------------------------
    # Cross-module compatibility
    # ------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        Geometry8CircleFundamentalsFinal.validate_lesson_data(self)
        Geometry8CircleClass2PartsArcs.validate_lesson_data(self)
        Geometry8CircleWorkshopFinal.validate_lesson_data(self)

    def _circle(self, center: np.ndarray, radius: float = 1.75, *, fill_opacity: float = 0.0) -> Circle:
        return Circle(
            radius=radius,
            stroke_color=BLACK_LINE,
            stroke_width=4.0,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=fill_opacity,
        ).move_to(center)

    def _term_card(self, title: str, body, width: float = 5.4) -> VGroup:
        """Use each source module's proven typography contract.

        Fundamentals passes a single string and its geometry/labels were audited
        with the original 27/24 typography. Class 2 passes a list of lines and
        benefits from the larger 30/27 projector typography. Keeping these two
        cases separate prevents a Class-2 readability upgrade from perturbing
        the already-validated Fundamentals layouts.
        """
        if isinstance(body, str):
            return self.note_panel(
                title,
                [body],
                width=width,
                title_size=27,
                body_size=24,
                max_text_height=1.60,
            )
        return self.note_panel(
            title,
            list(body),
            width=width,
            title_size=30,
            body_size=27,
            max_text_height=2.35,
        )

    def _answer_panel(self, expression: str, width: float = 5.4, size: int = 46) -> VGroup:
        return self.formula_panel(expression, width=width, height=1.15, font_size=size)

    @staticmethod
    def _bisector_point(vertex: np.ndarray, p1: np.ndarray, p2: np.ndarray, distance: float) -> np.ndarray:
        u1 = (p1 - vertex) / np.linalg.norm(p1 - vertex)
        u2 = (p2 - vertex) / np.linalg.norm(p2 - vertex)
        direction = u1 + u2
        direction /= np.linalg.norm(direction)
        return vertex + direction * distance

    # ------------------------------------------------------------------
    # Workshop QA core fix
    # ------------------------------------------------------------------
    def _restore_card_width(self, mob: Mobject, width: float = QA_CARD_WIDTH) -> Mobject:
        """Undo the six-card stack shrink without changing card content."""
        if mob.width < width:
            mob.scale(width / mob.width)
        return mob

    def _show_guided_solution(
        self,
        *,
        problem: Mobject,
        think: Mobject,
        strategy: Mobject,
        solve: Mobject,
        check: Mobject,
        answer: Mobject,
        think_time: float = 5.0,
    ) -> None:
        """Projection-safe replacement for the original six-card stack.

        All card contents are the exact objects created by the existing workshop
        methods. Only their scale, position and presentation order change.
        """
        for mob in (problem, think, strategy, solve, check, answer):
            self._restore_card_width(mob)

        problem.move_to([QA_RIGHT_X, QA_PROBLEM_Y, 0])
        think.move_to([QA_RIGHT_X, -0.35, 0])
        strategy.move_to(think)

        final_stack = VGroup(solve, check, answer).arrange(DOWN, buff=0.14)
        if final_stack.height > QA_FINAL_MAX_HEIGHT:
            final_stack.scale_to_fit_height(QA_FINAL_MAX_HEIGHT)
        final_stack.next_to(problem, DOWN, buff=0.18)
        final_stack.align_to(problem, RIGHT)

        # Runtime safe-frame acceptance: the final teaching state must fit.
        self.assert_content_safe(VGroup(problem, final_stack), "workshop QA right column")
        self.assert_within_frame(VGroup(problem, final_stack), "workshop QA final state", margin=0.13)

        self.play(FadeIn(problem), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(think, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(think_time)
        self.play(ReplacementTransform(think, strategy), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(ReplacementTransform(strategy, solve), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)

    # ------------------------------------------------------------------
    # Exact approved PDF module order
    # ------------------------------------------------------------------
    def construct(self) -> None:
        # A. Fundamentals: same content, but postpone its closing bridge.
        Geometry8CircleFundamentalsFinal.opening(self)
        Geometry8CircleFundamentalsFinal.circle_definition(self)
        Geometry8CircleFundamentalsFinal.basic_elements(self)
        Geometry8CircleFundamentalsFinal.lines_and_arcs(self)
        Geometry8CircleFundamentalsFinal.radius_diameter(self)
        Geometry8CircleFundamentalsFinal.central_angle(self)
        Geometry8CircleFundamentalsFinal.inscribed_angle(self)
        Geometry8CircleFundamentalsFinal.angle_relationship(self)
        Geometry8CircleFundamentalsFinal.pi_and_circumference(self)
        Geometry8CircleFundamentalsFinal.area_bridge(self)
        self.fundamentals_summary_without_closing()
        self.header_group = None
        self.subtitle_group = None

        # B. Class 2: Parts, arcs, lines and angle links.
        Geometry8CircleClass2PartsArcs.opening(self)
        Geometry8CircleClass2PartsArcs.recap(self)
        Geometry8CircleClass2PartsArcs.chord(self)
        Geometry8CircleClass2PartsArcs.arcs(self)
        Geometry8CircleClass2PartsArcs.tangent(self)
        Geometry8CircleClass2PartsArcs.secant(self)
        Geometry8CircleClass2PartsArcs.compare_lines(self)
        Geometry8CircleClass2PartsArcs.central_angle(self)
        Geometry8CircleClass2PartsArcs.inscribed_angle(self)
        self.class2_summary_qa()

        # C. PDF bridge placed after Class 2.
        self.standard_closing("Circle fundamentals recovered — ready for guided practice.")
        self.header_group = None
        self.subtitle_group = None

        # D. Workshop: original source methods, improved by the QA override above.
        Geometry8CircleWorkshopFinal.opening(self)
        Geometry8CircleWorkshopFinal.warmup_identification(self)
        Geometry8CircleWorkshopFinal.exercise_radius_diameter(self)
        Geometry8CircleWorkshopFinal.exercise_circle_lines(self)
        Geometry8CircleWorkshopFinal.exercise_central_angle(self)
        Geometry8CircleWorkshopFinal.exercise_inscribed_angle(self)
        Geometry8CircleWorkshopFinal.exercise_intercepted_arc(self)
        Geometry8CircleWorkshopFinal.exercise_circumference(self)
        Geometry8CircleWorkshopFinal.exercise_area(self)
        self.exercise_formula_choice_qa()
        Geometry8CircleWorkshopFinal.preview_shaded_area(self)
        self.exit_ticket_qa()

    def class2_summary_qa(self) -> None:
        """Render the exact Class-2 checklist with a TeX-safe takeaway.

        The historical source concatenates two raw strings directly after
        ``\\qquad``. Python removes the source-line boundary, so TeX sees the
        invalid control sequence ``\\qquadm``. This local reconstruction keeps
        the same mathematical content while making the separator explicit.
        """
        self.set_header(
            9,
            "CLASS 2 CHECKLIST",
            "Recognize the object first. Then use the relationship that belongs to it.",
        )
        data = [
            ("1  CHORD", "2 endpoints on the circle"),
            ("2  ARC", "curved part of the boundary"),
            ("3  TANGENT", "1 contact point"),
            ("4  SECANT", "2 intersection points"),
            ("5  CENTRAL ANGLE", "angle measure = arc measure"),
            ("6  INSCRIBED ANGLE", "angle measure = arc / 2"),
        ]
        cards = VGroup(
            *[
                self.note_panel(
                    title,
                    [line],
                    width=4.25,
                    title_size=27,
                    body_size=25,
                    max_text_height=1.10,
                )
                for title, line in data
            ]
        )
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.34))
        cards.move_to(UP * 0.10)
        takeaway = self.formula_panel(
            r"m\angle AOB=m\widehat{AB}\qquad\;m\angle AVB=\frac{1}{2}m\widehat{AB}",
            width=9.7,
            height=1.05,
            font_size=34,
        )
        takeaway.next_to(cards, DOWN, buff=0.30)
        group = VGroup(cards, takeaway).move_to(DOWN * 0.38)
        self.assert_content_safe(group, "class2 summary group")
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.8,
        )
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.standard_closing(
            "Identify the element. Count the intersections. Read the arc. Then calculate."
        )

    def fundamentals_summary_without_closing(self) -> None:
        """Same Fundamentals page 10, with closing deferred until after Class 2."""
        self.set_header(
            10,
            "CIRCLE FUNDAMENTALS CHECK",
            "Identify the object first; choose the relationship second; calculate only after that.",
        )
        route = self.process_map(
            [
                ("1", "CENTER / RADIUS / DIAMETER"),
                ("2", "CHORD / ARC"),
                ("3", "TANGENT / SECANT"),
                ("4", "CENTRAL ANGLE"),
                ("5", "INSCRIBED ANGLE"),
                ("6", "CIRCUMFERENCE / AREA"),
            ],
            columns=3,
        )
        self.fit(route, 13.2, 3.35)
        route.move_to(UP * 0.25)
        challenge = VGroup(
            self.text("FINAL CHALLENGE", 30, BOLD),
            self.math(r"\theta_{central}=120^\circ\quad\Longrightarrow\quad\theta_{inscribed}=?", 41),
            self.math(r"\boxed{60^\circ}", 48),
        ).arrange(DOWN, buff=0.20)
        challenge.to_edge(DOWN, buff=0.78)
        group = VGroup(route, challenge)
        self.assert_content_safe(group, "fundamentals summary")
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.09),
            run_time=RUN_SLOW * 1.7,
        )
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(challenge[0]), Write(challenge[1]), run_time=RUN_NORMAL)
        self.wait(5.5)
        self.play(FadeIn(challenge[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage(keep_header=False)

    # ------------------------------------------------------------------
    # Additional workshop readability fixes found in full contact-sheet QA
    # ------------------------------------------------------------------
    def exercise_formula_choice_qa(self) -> None:
        self.set_header(9, "EXERCISE — CHOOSE THE MEASUREMENT", "Decide circumference or area before using any formula.")
        cards = VGroup()
        answers = VGroup()
        scenarios = [
            ("FENCE", "around a circular garden", "CIRCUMFERENCE"),
            ("PAINT", "covering a circular sign", "AREA"),
            ("WHEEL", "distance around one revolution", "CIRCUMFERENCE"),
        ]
        for idx, (title, body, answer_text) in enumerate(scenarios):
            box = RoundedRectangle(
                width=4.35,
                height=4.25,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=2.0,
                fill_color=WHITE,
                fill_opacity=1.0,
            )
            heading = self.text(title, 32, BOLD)
            circ = Circle(
                radius=0.86,
                stroke_color=BLACK_LINE,
                stroke_width=4,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=0.72 if idx == 1 else 0.0,
            )
            desc = self.text(body, 27)
            self.fit(desc, 3.65, 0.65)
            content = VGroup(heading, circ, desc).arrange(DOWN, buff=0.24).move_to(box).shift(UP * 0.16)
            answer = self.text(answer_text, 29, BOLD).next_to(box.get_bottom(), UP, buff=0.31)
            cards.add(VGroup(box, content))
            answers.add(answer)

        cards.arrange(RIGHT, buff=0.32).move_to(DOWN * 0.35)
        for answer, card in zip(answers, cards):
            answer.move_to(card[0].get_bottom() + UP * 0.40)

        think = self.note_panel(
            "THINK",
            ["What is being measured: boundary length or covered region?"],
            width=9.1,
            title_size=29,
            body_size=28,
            max_text_height=1.05,
        )
        think.to_edge(DOWN, buff=0.42)
        group = VGroup(cards, answers, think)
        self.assert_content_safe(group, "formula choice QA")

        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.12), run_time=RUN_SLOW)
        self.play(FadeIn(think), run_time=RUN_NORMAL)
        self.wait(6.0)
        self.play(LaggedStart(*[FadeIn(a) for a in answers], lag_ratio=0.18), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

    def exit_ticket_qa(self) -> None:
        self.set_header(11, "EXIT TICKET", "Three quick checks: identify, relate, choose.")
        questions = [
            ("1 — IDENTIFY", "A line touches a circle at one point. Name it.", "TANGENT", False),
            ("2 — RELATE", "Central angle = 90°. Same-arc inscribed angle = ?", r"45^\circ", True),
            ("3 — CHOOSE", "Paint covers a circular logo: circumference or area?", "AREA", False),
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
        for idx, (title, question, answer_text, is_math) in enumerate(questions, start=1):
            index = self.text(f"QUESTION {idx} OF 3", 28, BOLD).next_to(holder.get_top(), DOWN, buff=0.28)
            title_m = self.text(title, 34, BOLD)
            body = self.text(question, 31)
            self.fit(body, 10.6, 0.78)
            prompt = VGroup(title_m, body).arrange(DOWN, buff=0.30).move_to(holder).shift(UP * 0.35)
            answer = self.math(answer_text, 48) if is_math else self.text(answer_text, 40, BOLD)
            answer.next_to(prompt, DOWN, buff=0.45)
            state = VGroup(index, prompt)

            if current is None:
                self.play(FadeIn(state), run_time=RUN_NORMAL)
            else:
                self.play(ReplacementTransform(current, state), run_time=RUN_NORMAL)
            self.wait(5.0)
            self.play(FadeIn(answer), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
            self.play(FadeOut(answer), run_time=RUN_QUICK)
            current = state

        self.wait(PAUSE_FINAL)
        self.standard_closing("Workshop complete — circle fundamentals are ready for the next unit.")


# Preview QA:
# LESSON_TIME_SCALE=0.08 manim -pql Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA.py \
#   Geometry8CirclePedagogicalSequenceSeniorQA --fps 15 --disable_caching
# Final:
# LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA.py \
#   Geometry8CirclePedagogicalSequenceSeniorQA --fps 30 --disable_caching
