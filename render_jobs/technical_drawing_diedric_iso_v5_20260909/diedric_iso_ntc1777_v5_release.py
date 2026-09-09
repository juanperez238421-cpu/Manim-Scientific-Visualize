#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 RELEASE — final measured layout pass.

This layer keeps the V5 Final QA camera/pacing and replaces only the two
remaining dense layouts.  Card extents are calculated so their bounding boxes
have positive gaps from neighboring cards, method tags, and the bottom
narration band.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from diedric_iso_ntc1777_v5_final import *


class DiedricISOProjectionV5Release(DiedricISOProjectionV5FinalQA):
    """Release scene: zero intentional text/card or card/card intersections."""

    def angle_layout(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        method = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        placement = "COLOCACIÓN OPUESTA" if first else "COLOCACIÓN DEL MISMO LADO"
        self.transition(number, method, order)

        title = self.stage_title(method, "Primero entiende la posición física; después lee la lámina.", color)
        strip = observer_sequence_strip(first, color).scale(1.08).move_to([0, -0.45, 0])
        self.fadd(strip)
        groups, arrows = strip[0], strip[1]
        self.play(FadeIn(groups[0]), run_time=RT_REVEAL)
        self.wait(PAUSE_READ)
        for i in range(1, len(groups)):
            self.play(GrowArrow(arrows[i-1]), FadeIn(groups[i]), run_time=RT_REVEAL)
            self.wait(PAUSE_VIEW)
        self.wait(PAUSE_EXPLAIN)
        self.fixed_fade_out(strip, title)

        # Every method gets a full-scale front-view pause before compression.
        title = self.stage_title("1 · ANCLA EN EL ALZADO",
                                 "La proyección se muestra grande antes de organizar la lámina.", color)
        hero = view_reveal_frame("front", BLUE, 8.6, 5.15, True).move_to([0, -0.20, 0])
        self.fadd(hero)
        self.play(FadeIn(hero, scale=0.985), run_time=RT_REVEAL)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(hero, title)

        title = self.stage_title("2 · DISTRIBUYE LAS VISTAS",
                                 "La escala baja únicamente para comparar posiciones relativas.", color)
        # FRONT extents: y [-1.25, 0.75]
        front = view_card("front", 3.85, 2.00, 0.43).move_to([0, -0.25, 0])
        # TOP height=1.45.  ISO E extents [-2.805,-1.355], gap=.105 to front;
        # ISO A extents [.855,2.305], gap=.105 to front.
        top = view_card("top", 3.85, 1.45, 0.36)
        side = view_card("right", 3.05, 2.00, 0.40)

        if first:
            top.move_to([0, -2.08, 0])
            side.move_to([-4.45, -0.25, 0])
            rule_text = "PLANTA abajo · lateral derecho a la izquierda"
            tag_pos = [5.25, 2.22, 0]
        else:
            top.move_to([0, 1.58, 0])
            side.move_to([4.45, -0.25, 0])
            rule_text = "PLANTA arriba · lateral derecho a la derecha"
            tag_pos = [-5.25, 2.22, 0]

        self.fadd(front, top, side)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(top, shift=UP * 0.06 if first else DOWN * 0.06), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(side, shift=RIGHT * 0.06 if first else LEFT * 0.06), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)

        # Method tag is placed opposite the lateral card, never over the top view.
        tag = callout(placement, color, 4.45, 20).move_to(tag_pos)
        rule = safe_bottom_callout(rule_text, color, 7.3, 21)
        self.fadd(tag, rule)
        self.play(FadeIn(tag), FadeIn(rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(front, top, side, tag, rule, title)

    def compare(self):
        self.transition(6, "MISMAS VISTAS · DISTINTA DISTRIBUCIÓN",
                        "Las vistas conservan geometría; cambia su ubicación relativa")
        title = self.stage_title("COMPARACIÓN FINAL",
                                 "Alzado como ancla: izquierda = ISO E · derecha = ISO A.", BLUE)
        left, right_panel, div = split_comparison_panel()
        lt = safe_text("ISO E · OPUESTO", 23, ORANGE, BOLD).move_to([-3.75, 2.18, 0])
        rt = safe_text("ISO A · MISMO LADO", 23, TEAL, BOLD).move_to([3.75, 2.18, 0])

        # Left / ISO E: front and side on the upper row, top below.
        left_front = view_card("front", 2.90, 1.55, 0.32).move_to([-3.75, 0.45, 0])
        left_side = view_card("right", 2.35, 1.55, 0.30).move_to([-6.15, 0.45, 0])
        left_top = view_card("top", 2.90, 1.45, 0.30).move_to([-3.75, -1.60, 0])

        # Right / ISO A: top above, front and side on the lower row.
        right_top = view_card("top", 2.90, 1.45, 0.30).move_to([3.75, 0.75, 0])
        right_front = view_card("front", 2.90, 1.55, 0.32).move_to([3.75, -1.35, 0])
        right_side = view_card("right", 2.35, 1.55, 0.30).move_to([6.15, -1.35, 0])

        left_views = VGroup(left_front, left_side, left_top)
        right_views = VGroup(right_top, right_front, right_side)
        group = VGroup(left, right_panel, div, lt, rt, left_views, right_views)
        self.fadd(group)
        self.play(FadeIn(left), FadeIn(right_panel), Create(div), FadeIn(lt), FadeIn(rt), run_time=RT_SLOW)
        self.play(FadeIn(left_front), FadeIn(right_front), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(left_side), FadeIn(right_side), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(left_top), FadeIn(right_top), run_time=RT_REVEAL)
        self.wait(PAUSE_LONG)
        rule = safe_bottom_callout("ISO E: opuesto  ·  ISO A: mismo lado", BLUE, 6.8, 22)
        self.fadd(rule)
        self.play(FadeIn(rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(rule, group, title)
