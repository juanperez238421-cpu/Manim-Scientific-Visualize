#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final V5 visual-QA corrections for the ISO E / ISO A dihedral lesson.

This scene subclasses the first V5 rebuild and corrects issues found by
chronological inspection of the rendered V5 frames:
- removes the full-card colour flash caused by Indicate(view_card);
- enlarges isolated orthographic projections;
- extends observer and projection reading pauses;
- stages the six-step reading algorithm instead of showing all steps at once;
- stages projection symbols and the guided challenge more deliberately.
"""
from __future__ import annotations

import sys
from pathlib import Path
from manim import *

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import diedric_iso_ntc1777_v5 as base
from diedric_iso_ntc1777_v5 import *  # noqa: F401,F403

# Longer holds and smoother camera moves after frame-by-frame review.
base.RT_CAMERA = 2.60
base.PAUSE_OBSERVER = 4.00
base.PAUSE_VIEW = 3.10
base.PAUSE_READ = 2.65
base.PAUSE_LONG = 4.75


class DiedricISOProjectionV5SeniorFinal(base.DiedricISOProjectionV5SeniorFrameQA):
    """V5 final: frame-QA corrected educational render."""

    def view_fullscreen(self, key, color, caption):
        """Show a genuinely large, isolated projection with a clean highlight.

        The earlier V5 used Indicate() on the complete card VGroup; for the red
        posterior view this temporarily recoloured the white card/panel red.
        Circumscribe() now highlights only the drawing region without changing
        fill colours.
        """
        panel = paper_panel(10.6, 5.90, 0.42).move_to([0, -0.28, 0])
        scale_map = {
            "front": 1.02,
            "rear": 1.02,
            "top": 0.88,
            "bottom": 0.88,
            "right": 0.94,
            "left": 0.94,
        }
        card = view_card(key, 8.85, 4.82, scale_map[key], True).move_to([0, -0.28, 0])
        cap = callout(caption, color, 6.05, 20).move_to([4.60, 2.52, 0])
        group = VGroup(panel, card, cap)
        self.fadd(group)
        self.play(
            FadeIn(panel),
            FadeIn(card, scale=0.975),
            FadeIn(cap, shift=LEFT * 0.08),
            run_time=base.RT_SMOOTH,
        )
        self.wait(base.PAUSE_VIEW)
        # Highlight the engineering drawing only; preserve paper/background.
        self.play(Circumscribe(card[3], color=color, fade_out=True, buff=0.14), run_time=base.RT)
        self.wait(base.PAUSE_READ)
        self.cleanup(group, run_time=base.RT)

    def symbols(self):
        self.transition(7, "EL SÍMBOLO LO DECIDE", "Identifica el método antes de interpretar posiciones")
        h = self.header(7, "SÍMBOLOS DE PROYECCIÓN", "El tronco de cono y la vista circular codifican el método.")

        p1 = paper_panel(6.3, 4.55, 0.42).move_to([-3.65, -0.30, 0])
        p3 = paper_panel(6.3, 4.55, 0.42).move_to([3.65, -0.30, 0])
        t1 = VGroup(
            safe_text("PRIMER DIEDRO", 28, ORANGE, BOLD),
            badge("First-angle · ISO E", ORANGE, 17),
        ).arrange(DOWN, buff=0.15).move_to([-3.65, 2.35, 0])
        t3 = VGroup(
            safe_text("TERCER DIEDRO", 28, TEAL, BOLD),
            badge("Third-angle · ISO A", TEAL, 17),
        ).arrange(DOWN, buff=0.15).move_to([3.65, 2.35, 0])

        self.fadd(p1, p3, t1, t3)
        self.play(FadeIn(p1), FadeIn(p3), FadeIn(t1), FadeIn(t3), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_BEAT)

        s1 = projection_symbol(True, 1.35).move_to([-3.65, -0.10, 0])
        self.fadd(s1)
        self.play(Create(s1), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        s3 = projection_symbol(False, 1.35).move_to([3.65, -0.10, 0])
        self.fadd(s3)
        self.play(Create(s3), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        reminder = callout("ANTES DE LEER UNA LÁMINA: LOCALIZA ESTE SÍMBOLO", RED, 7.0, 20).move_to([0, -3.42, 0])
        self.fadd(reminder)
        self.play(FadeIn(reminder), run_time=base.RT)
        self.wait(base.PAUSE_EXPLAIN)
        self.cleanup(reminder, s1, s3, p1, p3, t1, t3, h)

    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos para interpretar cualquier lámina")
        h = self.header(9, "LEE UNA LÁMINA EN 6 PASOS", "Sistema → alzado → distribución → reconstrucción.")

        steps = [
            step_chip(1, "IDENTIFICA EL SÍMBOLO", BLUE, 4.45),
            step_chip(2, "DECIDE ISO E / ISO A", ORANGE, 4.45),
            step_chip(3, "UBICA EL ALZADO", BLUE, 4.45),
            step_chip(4, "LOCALIZA PLANTA Y LATERALES", TEAL, 4.45),
            step_chip(5, "VERIFICA OPUESTO / MISMO LADO", GREEN, 4.45),
            step_chip(6, "RECONSTRUYE EL 3D", PURPLE, 4.45),
        ]
        step_group = VGroup(*steps).arrange(DOWN, buff=0.11).move_to([-4.55, -0.42, 0])

        sheet = paper_panel(7.0, 5.65, 0.42).move_to([3.35, -0.42, 0])
        self.fadd(sheet)
        self.play(FadeIn(sheet), run_time=base.RT)

        sym = projection_symbol(False, 0.62).move_to([1.35, -2.45, 0])
        method = badge("ISO A · TERCER DIEDRO", TEAL, 16).move_to([4.45, -2.48, 0])
        front = view_card("front", 2.75, 1.66, 0.31).move_to([3.35, -0.25, 0])
        top = view_card("top", 2.75, 1.66, 0.30).move_to([3.35, 1.58, 0])
        right = view_card("right", 2.75, 1.66, 0.31).move_to([5.62, -0.25, 0])
        reconstruction = callout("VISTAS COHERENTES → FORMA 3D", PURPLE, 4.7, 18).move_to([3.80, -2.45, 0])

        for i, step in enumerate(steps):
            self.fadd(step)
            self.play(FadeIn(step, shift=RIGHT * 0.08), run_time=base.RT_FAST)

            if i == 0:
                self.fadd(sym)
                self.play(Create(sym), run_time=base.RT)
            elif i == 1:
                self.fadd(method)
                self.play(FadeIn(method, shift=UP * 0.06), run_time=base.RT)
            elif i == 2:
                self.fadd(front)
                self.play(FadeIn(front, scale=0.97), run_time=base.RT)
            elif i == 3:
                self.fadd(top, right)
                self.play(FadeIn(top, shift=DOWN * 0.06), run_time=base.RT)
                self.wait(base.PAUSE_BEAT)
                self.play(FadeIn(right, shift=LEFT * 0.06), run_time=base.RT)
            elif i == 4:
                self.play(Circumscribe(VGroup(front, top, right), color=GREEN, fade_out=True, buff=0.10), run_time=base.RT)
            elif i == 5:
                self.fadd(reconstruction)
                self.play(ReplacementTransform(method, reconstruction), run_time=base.RT_SMOOTH)
                self.frem(method)

            self.wait(1.55)

        self.wait(base.PAUSE_LONG)
        self.cleanup(*steps, sheet, sym, front, top, right, reconstruction, h)

    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        h = self.header(10, "DESAFÍO DE LECTURA", "Con el símbolo dado, ubica planta y lateral derecho.")

        left_panel = paper_panel(4.6, 5.2, 0.42).move_to([-5.15, -0.35, 0])
        sym = projection_symbol(False, 0.90).move_to([-5.15, 0.20, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 16).move_to([-5.15, 2.10, 0])
        self.fadd(left_panel, q)
        self.play(FadeIn(left_panel), FadeIn(q), run_time=base.RT)
        self.fadd(sym)
        self.play(Create(sym), run_time=base.RT_DRAW)
        self.wait(base.PAUSE_READ)

        main_panel = paper_panel(9.2, 5.2, 0.42).move_to([2.35, -0.35, 0])
        front = view_card("front", 3.05, 1.92, 0.36).move_to([1.55, -0.30, 0])
        self.fadd(main_panel, front)
        self.play(FadeIn(main_panel), FadeIn(front, scale=0.97), run_time=base.RT_SMOOTH)
        self.wait(base.PAUSE_BEAT)

        top_slot = RoundedRectangle(
            width=3.05, height=1.92, corner_radius=0.12,
            stroke_color=TEAL, fill_color=PALE_TEAL, fill_opacity=0.18,
        ).move_to([1.55, 1.80, 0])
        right_slot = RoundedRectangle(
            width=3.05, height=1.92, corner_radius=0.12,
            stroke_color=ORANGE, fill_color=PALE_ORANGE, fill_opacity=0.18,
        ).move_to([5.15, -0.30, 0])
        top_q = safe_text("PLANTA ?", 22, TEAL, BOLD).move_to(top_slot)
        right_q = safe_text("LATERAL D. ?", 22, ORANGE, BOLD).move_to(right_slot)
        prompt = callout("PIENSA ANTES DE REVELAR", INK, 5.5, 20).move_to([2.35, -3.30, 0])
        self.fadd(top_slot, right_slot, top_q, right_q, prompt)
        self.play(
            FadeIn(top_slot), FadeIn(right_slot),
            FadeIn(top_q), FadeIn(right_q), FadeIn(prompt),
            run_time=base.RT_SMOOTH,
        )

        dots = VGroup(*[Dot(radius=0.065, color=MID) for _ in range(6)]).arrange(RIGHT, buff=0.12).move_to([2.35, -2.72, 0])
        self.fadd(dots)
        self.play(FadeIn(dots), run_time=base.RT_FAST)
        for d in dots:
            self.play(d.animate.set_color(BLUE).scale(1.30), run_time=0.22)
            self.play(d.animate.set_color(MID).scale(1 / 1.30), run_time=0.22)
        self.wait(base.PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.0, 21).move_to([-5.15, -2.15, 0])
        self.fadd(method)
        self.play(FadeOut(prompt), FadeOut(dots), FadeIn(method), run_time=base.RT)
        self.wait(base.PAUSE_READ)

        top_view = view_card("top", 3.05, 1.92, 0.35).move_to(top_slot)
        self.fadd(top_view)
        self.play(ReplacementTransform(top_slot, top_view), FadeOut(top_q), run_time=base.RT_SMOOTH)
        self.frem(top_slot, top_q)
        self.wait(base.PAUSE_VIEW)

        right_view = view_card("right", 3.05, 1.92, 0.36).move_to(right_slot)
        self.fadd(right_view)
        self.play(ReplacementTransform(right_slot, right_view), FadeOut(right_q), run_time=base.RT_SMOOTH)
        self.frem(right_slot, right_q)
        self.wait(base.PAUSE_VIEW)

        answer = callout(
            "MISMO LADO · PLANTA ARRIBA · LATERAL DERECHO A LA DERECHA",
            GREEN, 7.6, 20,
        ).move_to([2.35, -3.30, 0])
        self.fadd(answer)
        self.play(FadeIn(answer), run_time=base.RT)
        self.wait(base.PAUSE_LONG)
        self.cleanup(left_panel, sym, q, main_panel, front, method, top_view, right_view, answer, h)
