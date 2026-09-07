#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — 7 reglas para organizar vistas ortogonales.

Parallel scene to the current 3D -> 2D Sistema Diédrico work.  This file does
NOT repeat the 3D construction.  It isolates the view-placement rules and
animates them in Spanish with explicit ``self.play(Write(...))`` sequences.

Source basis
------------
- Rules 1-6 synthesize the supplied Class 6 PowerPoint:
  front view as reference plus the ISO A / ISO E placements for top, bottom,
  left, right and rear views.
- Rule 7 reuses the alignment principle already present in the validated
  3D-to-2D V6 scene: common dimensions must coincide between aligned views.

Visual/render contract
----------------------
- Reuse the validated Class 6 Manim visual language.
- 1920x1080, 30 fps, white background, black/gray hierarchy.
- No equations and no 3D camera work in this scene.
- Rule text enters with Write(), not as a static PowerPoint-like list.
- Manim Community Edition 0.20.1.
"""
from __future__ import annotations

from manim import *

from Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V1_SENIOR import (
    TechnicalDrawingClass6ISO,
    BLACK_TEXT,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT,
    PAPER_GRAY,
    RUN_Q,
    RUN,
    RUN_SLOW,
    PAUSE_R,
    PAUSE_E,
    PAUSE_W,
    PAUSE_SUM,
)


# -----------------------------------------------------------------------------
# Exactly seven pedagogical rules.
# -----------------------------------------------------------------------------
RULES = (
    (
        1,
        "EL ALZADO ES LA REFERENCIA",
        "La vista de frente (a) organiza la posición de las demás vistas.",
    ),
    (
        2,
        "VISTA SUPERIOR",
        "ISO A: arriba · ISO E: debajo.",
    ),
    (
        3,
        "VISTA INFERIOR",
        "ISO A: debajo · ISO E: arriba.",
    ),
    (
        4,
        "VISTA IZQUIERDA",
        "ISO A: izquierda · ISO E: derecha.",
    ),
    (
        5,
        "VISTA DERECHA",
        "ISO A: derecha · ISO E: izquierda.",
    ),
    (
        6,
        "VISTA POSTERIOR",
        "Puede ubicarse a izquierda o derecha, según convenga.",
    ),
    (
        7,
        "ALINEACIÓN ENTRE VISTAS",
        "Las dimensiones comunes deben coincidir entre las vistas alineadas.",
    ),
)


class SevenOrthographicRulesWrite(TechnicalDrawingClass6ISO):
    """Text-first seven-rule animation using the existing Class 6 protocol."""

    CARD_W = 1.24
    CARD_H = 0.96

    def construct(self):
        assert len(RULES) == 7
        assert [r[0] for r in RULES] == list(range(1, 8))

        self.opening()
        self.rule_01_reference()
        self.rule_02_superior()
        self.rule_03_inferior()
        self.rule_04_left()
        self.rule_05_right()
        self.rule_06_rear()
        self.rule_07_alignment()
        self.summary()

    # ------------------------------------------------------------------
    # Shared visual helpers
    # ------------------------------------------------------------------
    def view_shape(self, key: str):
        if key in {"front", "rear"}:
            mob = self.view_front_step(0.30)
            if key == "rear":
                mob = mob.copy().flip(axis=UP)
        elif key in {"top", "bottom"}:
            mob = self.view_top_step(0.27)
        elif key in {"left", "right"}:
            mob = self.view_right_step(0.28)
            if key == "left":
                mob = mob.copy().flip(axis=UP)
        else:
            raise ValueError(key)
        mob.set_stroke(color=BLACK_LINE, width=1.8)
        return mob

    def view_card(self, key: str, label: str, muted: bool = False):
        box = RoundedRectangle(
            width=self.CARD_W,
            height=self.CARD_H,
            corner_radius=0.08,
            stroke_color=MID_GRAY if muted else BLACK_LINE,
            stroke_width=1.35,
            fill_color=WHITE,
            fill_opacity=1,
        )
        shape = self.view_shape(key)
        self.fit(shape, self.CARD_W - 0.22, self.CARD_H - 0.34)
        shape.move_to(box.get_center() + UP * 0.09)
        if muted:
            shape.set_stroke(color=MID_GRAY)
        lab = self.txt(label, 13, BOLD, color=MID_GRAY if muted else BLACK_TEXT)
        self.fit(lab, self.CARD_W - 0.12, 0.20)
        lab.next_to(box.get_bottom(), UP, buff=0.055)
        return VGroup(box, shape, lab)

    def board_positions(self, system: str):
        if system == "A":
            return {
                "front": ORIGIN,
                "top": UP * 1.28,
                "bottom": DOWN * 1.28,
                "left": LEFT * 1.50,
                "right": RIGHT * 1.50,
                "rear": RIGHT * 2.72,
            }
        if system == "E":
            return {
                "front": ORIGIN,
                "top": DOWN * 1.28,
                "bottom": UP * 1.28,
                "left": RIGHT * 1.50,
                "right": LEFT * 1.50,
                "rear": RIGHT * 2.72,
            }
        raise ValueError(system)

    def system_board(
        self,
        system: str,
        visible_keys=("front",),
        *,
        rear_both_sides=False,
        width=6.05,
        height=4.25,
    ):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.6,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        title_text = "ISO A · 3er cuadrante" if system == "A" else "ISO E · 1er cuadrante"
        title = self.txt(title_text, 22, BOLD)
        title.next_to(box, UP, buff=0.10)

        center = box.get_center() + DOWN * 0.08
        positions = self.board_positions(system)
        cards = VGroup()
        card_map = {}
        for key in visible_keys:
            label = {
                "front": "FRENTE",
                "top": "SUPERIOR",
                "bottom": "INFERIOR",
                "left": "IZQUIERDA",
                "right": "DERECHA",
                "rear": "POSTERIOR",
            }[key]
            card = self.view_card(key, label)
            card.move_to(center + positions[key])
            cards.add(card)
            card_map[key] = card

        if rear_both_sides:
            # The source deck explicitly allows the rear view on either side.
            left_rear = self.view_card("rear", "POSTERIOR", muted=True)
            left_rear.move_to(center + LEFT * 2.72)
            cards.add(left_rear)
            card_map["rear_left"] = left_rear

        return VGroup(box, title, cards), card_map

    def write_rule_text(self, rule_index: int, *, y=2.00):
        number, title, body = RULES[rule_index - 1]
        badge = self.chip(f"REGLA {number} DE 7", width=2.45, size=18)
        badge.move_to(LEFT * 5.85 + UP * y)

        heading = self.txt(title, 31, BOLD)
        heading.next_to(badge, RIGHT, buff=0.25)
        self.fit(heading, 8.7, 0.55)

        sentence = self.txt(body, 25, color=DARK_GRAY)
        self.fit(sentence, 13.3, 0.52)
        sentence.next_to(VGroup(badge, heading), DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(Write(badge[1]), Create(badge[0]), run_time=RUN_Q)
        self.play(Write(heading), run_time=RUN)
        self.play(Write(sentence), run_time=RUN_SLOW)
        return VGroup(badge, heading, sentence)

    def paired_iso_visual(self, key: str, left_phrase: str, right_phrase: str):
        a_board, a_map = self.system_board("A", ("front", key))
        e_board, e_map = self.system_board("E", ("front", key))
        pair = VGroup(a_board, e_board).arrange(RIGHT, buff=0.38)
        self.fit(pair, 14.5, 4.55)
        pair.move_to(DOWN * 1.40)

        a_phrase = self.txt(left_phrase, 20, BOLD)
        e_phrase = self.txt(right_phrase, 20, BOLD)
        a_phrase.next_to(a_board, DOWN, buff=0.12)
        e_phrase.next_to(e_board, DOWN, buff=0.12)

        self.play(Create(a_board[0]), Create(e_board[0]), run_time=RUN_Q)
        self.play(Write(a_board[1]), Write(e_board[1]), run_time=RUN_Q)

        self.play(
            FadeIn(a_map["front"], shift=UP * 0.04),
            FadeIn(e_map["front"], shift=UP * 0.04),
            run_time=RUN_Q,
        )
        self.play(
            Create(a_map[key][0]), Write(a_map[key][2]),
            Create(e_map[key][0]), Write(e_map[key][2]),
            run_time=RUN,
        )
        self.play(
            FadeIn(a_map[key][1]),
            FadeIn(e_map[key][1]),
            run_time=RUN_Q,
        )
        self.play(Write(a_phrase), Write(e_phrase), run_time=RUN)
        return VGroup(pair, a_phrase, e_phrase)

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening(self):
        title = self.txt("7 REGLAS PARA ORGANIZAR LAS VISTAS ORTOGONALES", 41, BOLD)
        subtitle = self.txt(
            "Sistema diédrico · ISO A / tercer cuadrante · ISO E / primer cuadrante",
            24,
            color=DARK_GRAY,
        )
        context = self.txt(
            "En Colombia: NTC 1777 derivada de ISO A, según la presentación de Clase 6.",
            21,
            color=MID_GRAY,
        )
        group = VGroup(title, subtitle, context).arrange(DOWN, buff=0.25)
        self.fit(group, 13.9, 2.3)
        group.move_to(UP * 0.35)

        self.play(Write(title), run_time=RUN_SLOW)
        self.play(Write(subtitle), run_time=RUN)
        self.play(Write(context), run_time=RUN)
        self.wait(PAUSE_E)
        self.play(FadeOut(group), run_time=RUN_Q)

    # ------------------------------------------------------------------
    # Rule 1
    # ------------------------------------------------------------------
    def rule_01_reference(self):
        self.set_header(
            "REGLA 1 · ALZADO",
            "Primero se fija la vista de frente; desde ella se organizan todas las demás.",
        )
        self.write_rule_text(1)

        front = self.view_card("front", "VISTA DE FRENTE (a)")
        front.scale(1.62).move_to(DOWN * 1.15)
        axes = VGroup(
            DashedLine(front.get_top() + UP * 0.20, front.get_top() + UP * 1.35,
                       dash_length=0.09, stroke_color=LIGHT_GRAY),
            DashedLine(front.get_bottom() + DOWN * 0.20, front.get_bottom() + DOWN * 1.35,
                       dash_length=0.09, stroke_color=LIGHT_GRAY),
            DashedLine(front.get_left() + LEFT * 0.20, front.get_left() + LEFT * 2.15,
                       dash_length=0.09, stroke_color=LIGHT_GRAY),
            DashedLine(front.get_right() + RIGHT * 0.20, front.get_right() + RIGHT * 2.15,
                       dash_length=0.09, stroke_color=LIGHT_GRAY),
        )
        cue = self.txt("REFERENCIA", 20, BOLD).next_to(front, DOWN, buff=0.25)

        self.play(Create(front[0]), run_time=RUN_Q)
        self.play(Write(front[2]), FadeIn(front[1]), run_time=RUN)
        self.play(LaggedStart(*[Create(line) for line in axes], lag_ratio=0.12), run_time=RUN)
        self.play(Write(cue), run_time=RUN_Q)
        self.wait(PAUSE_W)
        self.clear_content()

    # ------------------------------------------------------------------
    # Rules 2-5: placement pairs
    # ------------------------------------------------------------------
    def rule_02_superior(self):
        self.set_header(
            "REGLA 2 · VISTA SUPERIOR",
            "La misma vista cambia de posición en el papel según el sistema de proyección.",
        )
        self.write_rule_text(2)
        self.paired_iso_visual("top", "ISO A → ARRIBA", "ISO E → DEBAJO")
        self.wait(PAUSE_W)
        self.clear_content()

    def rule_03_inferior(self):
        self.set_header(
            "REGLA 3 · VISTA INFERIOR",
            "La posición se invierte entre tercer y primer cuadrante.",
        )
        self.write_rule_text(3)
        self.paired_iso_visual("bottom", "ISO A → DEBAJO", "ISO E → ARRIBA")
        self.wait(PAUSE_W)
        self.clear_content()

    def rule_04_left(self):
        self.set_header(
            "REGLA 4 · VISTA IZQUIERDA",
            "En ISO A permanece del mismo lado; en ISO E aparece al lado contrario.",
        )
        self.write_rule_text(4)
        self.paired_iso_visual("left", "ISO A → IZQUIERDA", "ISO E → DERECHA")
        self.wait(PAUSE_W)
        self.clear_content()

    def rule_05_right(self):
        self.set_header(
            "REGLA 5 · VISTA DERECHA",
            "La regla lateral es simétrica a la vista izquierda.",
        )
        self.write_rule_text(5)
        self.paired_iso_visual("right", "ISO A → DERECHA", "ISO E → IZQUIERDA")
        self.wait(PAUSE_W)
        self.clear_content()

    # ------------------------------------------------------------------
    # Rule 6
    # ------------------------------------------------------------------
    def rule_06_rear(self):
        self.set_header(
            "REGLA 6 · VISTA POSTERIOR",
            "La presentación permite colocarla a la izquierda o a la derecha, según convenga.",
        )
        self.write_rule_text(6)

        board, card_map = self.system_board(
            "A", ("front", "rear"), rear_both_sides=True, width=9.35, height=4.05
        )
        board.move_to(DOWN * 1.35)
        note_left = self.txt("OPCIÓN 1", 18, BOLD, color=MID_GRAY)
        note_right = self.txt("OPCIÓN 2", 18, BOLD)
        note_left.next_to(card_map["rear_left"], DOWN, buff=0.10)
        note_right.next_to(card_map["rear"], DOWN, buff=0.10)
        connector_left = DashedLine(
            card_map["front"].get_left(),
            card_map["rear_left"].get_right(),
            dash_length=0.10,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.4,
        )
        connector_right = DashedLine(
            card_map["front"].get_right(),
            card_map["rear"].get_left(),
            dash_length=0.10,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.4,
        )

        self.play(Create(board[0]), Write(board[1]), run_time=RUN_Q)
        self.play(FadeIn(card_map["front"]), run_time=RUN_Q)
        self.play(
            Create(connector_left), Create(connector_right),
            run_time=RUN,
        )
        self.play(
            Create(card_map["rear_left"][0]), Write(card_map["rear_left"][2]),
            Create(card_map["rear"][0]), Write(card_map["rear"][2]),
            run_time=RUN,
        )
        self.play(
            FadeIn(card_map["rear_left"][1]), FadeIn(card_map["rear"][1]),
            Write(note_left), Write(note_right),
            run_time=RUN,
        )
        self.wait(PAUSE_W)
        self.clear_content()

    # ------------------------------------------------------------------
    # Rule 7
    # ------------------------------------------------------------------
    def rule_07_alignment(self):
        self.set_header(
            "REGLA 7 · ALINEACIÓN",
            "No son dibujos independientes: todas las vistas representan el mismo objeto.",
        )
        self.write_rule_text(7)

        board, card_map = self.system_board(
            "A",
            ("front", "top", "bottom", "left", "right", "rear"),
            width=10.0,
            height=4.20,
        )
        board.move_to(DOWN * 1.42)
        c = card_map["front"].get_center()
        vertical = DashedLine(
            [c[0], c[1] - 2.02, 0],
            [c[0], c[1] + 2.02, 0],
            dash_length=0.085,
            stroke_color=MID_GRAY,
            stroke_width=1.5,
        )
        horizontal = DashedLine(
            [c[0] - 4.15, c[1], 0],
            [c[0] + 4.15, c[1], 0],
            dash_length=0.085,
            stroke_color=MID_GRAY,
            stroke_width=1.5,
        )
        alignment_note = self.txt(
            "misma geometría · misma escala · misma correspondencia",
            20,
            BOLD,
            color=DARK_GRAY,
        ).next_to(board, DOWN, buff=0.12)

        self.play(Create(board[0]), Write(board[1]), run_time=RUN_Q)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(Create(card[0]), Write(card[2]), FadeIn(card[1]))
                    for card in card_map.values()
                ],
                lag_ratio=0.10,
            ),
            run_time=RUN_SLOW * 1.8,
        )
        self.play(Create(vertical), Create(horizontal), run_time=RUN)
        self.play(Write(alignment_note), run_time=RUN)
        self.wait(PAUSE_SUM)
        self.clear_content()

    # ------------------------------------------------------------------
    # Final compact recap — no new numbered rule.
    # ------------------------------------------------------------------
    def summary(self):
        if self.header is not None:
            self.play(FadeOut(self.header), FadeOut(self.subtitle), run_time=RUN_Q)
            self.header = None
            self.subtitle = None

        title = self.txt("LAS 7 REGLAS · RESUMEN", 38, BOLD).to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=RUN)

        rows = VGroup()
        for number, rule_title, body in RULES:
            n = self.txt(f"{number}.", 23, BOLD)
            t = self.txt(rule_title, 23, BOLD)
            b = self.txt(body, 19, color=DARK_GRAY)
            line1 = VGroup(n, t).arrange(RIGHT, buff=0.15)
            row = VGroup(line1, b).arrange(DOWN, aligned_edge=LEFT, buff=0.055)
            rows.add(row)

        left = VGroup(*rows[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        right = VGroup(*rows[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        columns = VGroup(left, right).arrange(RIGHT, aligned_edge=UP, buff=0.72)
        self.fit(columns, 14.1, 5.7)
        columns.move_to(DOWN * 0.30)

        for row in rows:
            # Every rule is deliberately written, preserving the user's requested
            # self.play(Write()) visual language.
            self.play(Write(row[0]), run_time=RUN_Q)
            self.play(Write(row[1]), run_time=RUN_Q)

        footer = self.chip("ISO A · Colombia", width=3.0, size=19)
        footer.to_edge(DOWN, buff=0.28)
        self.play(Create(footer[0]), Write(footer[1]), run_time=RUN_Q)
        self.wait(PAUSE_SUM)
        self.close_all()


# Preview:
#   manim -pql Dibujo_Tecnico_7_Reglas_Vistas_Ortogonales_V1_WRITE.py SevenOrthographicRulesWrite --disable_caching
# Final:
#   manim -pqh Dibujo_Tecnico_7_Reglas_Vistas_Ortogonales_V1_WRITE.py SevenOrthographicRulesWrite --disable_caching
