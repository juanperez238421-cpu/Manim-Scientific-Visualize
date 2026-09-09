#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final V8 QA correction.

The first V8 PQH render successfully lowered and enlarged the 3D geometry and
restored larger orthographic views. Dense frame inspection then found one
remaining collision in section 09: the ISO A method badge extended beneath the
FRONT projection card. This final overlay moves that badge to its own lower-left
cell and applies the same hard disjoint check used by the other V8 layouts.
"""
from __future__ import annotations

import sys
from pathlib import Path
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import diedric_iso_ntc1777_v8 as v8
import diedric_iso_ntc1777_v5 as base
from diedric_iso_ntc1777_v8 import *  # noqa: F401,F403


class DiedricISOProjectionV8Final(v8.DiedricISOProjectionV8LowerLarge):
    """V8 final after post-render visual inspection."""

    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(9, "LEE UNA LÁMINA EN 6 PASOS", "Sistema → alzado → distribución → reconstrucción.")

        steps = [
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 4.85),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 4.85),
            step_chip(3, "UBICA EL ALZADO", BLUE, 4.85),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 4.85),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 4.85),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 4.85),
        ]
        VGroup(*steps).arrange(DOWN, buff=0.13).move_to([-4.85, -0.35, 0])

        sheet = paper_panel(8.35, 5.82, 0.42).move_to([3.48, -0.34, 0])
        self.fadd(sheet)
        self.play(FadeIn(sheet), run_time=base.RT)

        # Left information lane inside the sheet.
        sym = projection_symbol(False, 0.61).move_to([0.82, 1.50, 0])
        method = badge("ISO A · TERCER DIEDRO", TEAL, 16).move_to([1.42, -1.48, 0])

        # Right orthographic cross. Sizes are preserved from V8; spacing, not
        # shrinking, provides clearance.
        front = self.compact_tile("front", "ALZADO", BLUE, 2.55, 1.64, 0.32).move_to([3.72, -0.28, 0])
        top = self.compact_tile("top", "PLANTA", TEAL, 2.55, 1.64, 0.31).move_to([3.72, 1.58, 0])
        right = self.compact_tile("right", "LATERAL D.", ORANGE, 2.55, 1.64, 0.32).move_to([6.34, -0.28, 0])
        reconstruction = callout("VISTAS COHERENTES → FORMA 3D", PURPLE, 5.25, 18).move_to([4.05, -2.48, 0])

        self.assert_disjoint(front, top, right, gap=0.04)
        self.assert_disjoint(method, front, top, right, gap=0.02)

        for i, step in enumerate(steps):
            self.fadd(step)
            self.play(FadeIn(step, shift=RIGHT * 0.06), run_time=base.RT_FAST)
            if i == 0:
                self.fadd(sym)
                self.play(Create(sym), run_time=base.RT)
            elif i == 1:
                self.fadd(method)
                self.play(FadeIn(method), run_time=base.RT)
            elif i == 2:
                self.fadd(front)
                self.play(FadeIn(front, scale=0.98), run_time=base.RT)
            elif i == 3:
                self.fadd(top, right)
                self.play(FadeIn(top, shift=DOWN * 0.05), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeIn(right, shift=LEFT * 0.05), run_time=base.RT)
            elif i == 4:
                guides = VGroup(self.projector_pair(front, top), self.projector_pair(front, right))
                self.fadd(guides)
                self.play(Create(guides), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeOut(guides), run_time=base.RT_FAST)
                self.frem(guides)
            elif i == 5:
                self.fadd(reconstruction)
                self.play(FadeIn(reconstruction, shift=UP * 0.05), run_time=base.RT_SMOOTH)
            self.wait(1.55)

        self.wait(base.PAUSE_LONG)
        self.cleanup(*steps, sheet, sym, method, front, top, right, reconstruction, h)
