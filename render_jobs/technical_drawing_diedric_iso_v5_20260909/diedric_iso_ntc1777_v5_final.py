#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V5 FINAL layout patch.

Overrides the dense 2D teaching stages from V5 Senior QA.  Every final layout
uses measured vertical gaps between cards; large views are shown sequentially
before compact comparison layouts are introduced.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from diedric_iso_ntc1777_v5 import *


class DiedricISOProjectionV5FinalQA(DiedricISOProjectionV5SeniorQA):
    """V5 final: collision-free 2D layouts + retained V5 camera/pause system."""

    def unfolding(self):
        self.transition(3, "EL SISTEMA DIÉDRICO",
                        "PV y PH son perpendiculares; después PH se abate 90°")
        self.set_camera_orientation(phi=66 * DEGREES, theta=-45 * DEGREES, zoom=0.82)
        pv, ph, lt = dihedral_planes(7.2)
        part = mechanical_bracket_3d().scale(0.52)
        self.play(FadeIn(pv), FadeIn(ph), Create(lt), FadeIn(part), run_time=RT_HERO)
        self.wait(PAUSE_READ)

        labels = VGroup(
            badge("PV · PLANO VERTICAL", BLUE, 17),
            badge("PH · PLANO HORIZONTAL", TEAL, 17),
            badge("LT · LÍNEA DE TIERRA", INK, 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DL, buff=0.45).shift(UP * 0.55)
        self.fadd(labels)
        self.play(LaggedStart(*[FadeIn(x) for x in labels], lag_ratio=0.14), run_time=RT)
        self.wait(PAUSE_EXPLAIN)

        front = front_trace_3d(0.015, BLUE).scale(0.46).shift(UP * 0.15)
        top = orthographic_view("top", 0.38).shift(OUT * 0.03)
        self.play(Create(front), Create(top), run_time=RT_HERO)
        self.wait(PAUSE_VIEW)
        note = self.show_note("ABATIMIENTO: PH gira exactamente 90° alrededor de LT.", ORANGE, 7.1)
        self.play(Rotate(ph, PI / 2, axis=RIGHT, about_point=ORIGIN),
                  Rotate(top, PI / 2, axis=RIGHT, about_point=ORIGIN), run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)
        self.fixed_fade_out(note, labels)
        self.play(FadeOut(pv), FadeOut(ph), FadeOut(lt), FadeOut(part),
                  FadeOut(front), FadeOut(top), run_time=RT_SLOW)

        title = self.stage_title("DESPUÉS DEL ABATIMIENTO",
                                 "Alzado y planta quedan alineados en una lámina 2D.", ORANGE)
        sheet = paper_panel(12.6, 5.55, 0.42).move_to([0, -0.50, 0])
        # Exact non-overlap: FV bottom=-0.625; TV top=-0.825; gap=0.20.
        fv = large_view_card("front", 5.30, 2.45, 0.56, False, 20).move_to([-3.15, 0.60, 0])
        tv = large_view_card("top", 5.30, 2.45, 0.55, False, 20).move_to([-3.15, -2.05, 0])
        line = Line([-5.82, -0.72, 0], [5.82, -0.72, 0], color=INK, stroke_width=2.2)
        rule = VGroup(
            step_chip(1, "PV → ALZADO", BLUE, 4.20),
            step_chip(2, "PH → PLANTA", TEAL, 4.20),
            step_chip(3, "LT → ALINEACIÓN", ORANGE, 4.20),
        ).arrange(DOWN, buff=0.25).move_to([3.55, -0.48, 0])
        group = VGroup(sheet, fv, tv, line, rule)
        self.fadd(group)
        self.play(FadeIn(sheet), Create(line), run_time=RT)
        self.play(FadeIn(fv), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(tv), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(LaggedStart(*[FadeIn(x) for x in rule], lag_ratio=0.18), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(group, title)

    def angle_layout(self, first=True):
        number = 4 if first else 5
        color = ORANGE if first else TEAL
        method = "PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"
        order = "OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"
        placement = "COLOCACIÓN OPUESTA" if first else "COLOCACIÓN DEL MISMO LADO"
        self.transition(number, method, order)

        # Physical ordering shown alone: no projection cards compete with it.
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

        # Large alzado first, full teaching scale.
        title = self.stage_title("1 · ANCLA EN EL ALZADO",
                                 "Antes de distribuir vistas, identifica el frente principal.", color)
        hero = view_reveal_frame("front", BLUE, 8.6, 5.15, True).move_to([0, -0.20, 0])
        self.fadd(hero)
        self.play(FadeIn(hero, scale=0.985), run_time=RT_REVEAL)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(hero, title)

        # Compact arrangement only after each view has been read at large scale.
        title = self.stage_title("2 · DISTRIBUYE LAS VISTAS",
                                 "Las tarjetas reducen escala solo para mostrar posición relativa.", color)
        front = view_card("front", 3.90, 2.10, 0.44).move_to([0, -0.28, 0])
        top = view_card("top", 3.90, 1.78, 0.40)
        side = view_card("right", 3.15, 2.10, 0.42)
        if first:
            top.move_to([0, -2.45, 0])          # top edge=-1.56; front bottom=-1.33
            side.move_to([-4.55, -0.28, 0])
            text = "PLANTA abajo · lateral derecho a la izquierda"
        else:
            top.move_to([0, 1.48, 0])           # bottom=0.59; front top=0.77
            side.move_to([4.55, -0.28, 0])
            text = "PLANTA arriba · lateral derecho a la derecha"

        self.fadd(front, top, side)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(top, shift=DOWN * 0.06 if not first else UP * 0.06), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(side, shift=RIGHT * 0.06 if first else LEFT * 0.06), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        tag = safe_top_tag(placement, color, 5.35, 21)
        rule = safe_bottom_callout(text, color, 7.3, 21)
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
        lt = safe_text("ISO E · OPUESTO", 24, ORANGE, BOLD).move_to([-3.75, 2.18, 0])
        rt = safe_text("ISO A · MISMO LADO", 24, TEAL, BOLD).move_to([3.75, 2.18, 0])
        left_views = VGroup(
            view_card("front", 3.05, 1.95, 0.36).move_to([-3.60, -0.18, 0]),
            view_card("right", 2.55, 1.95, 0.34).move_to([-6.05, -0.18, 0]),
            view_card("top", 3.05, 1.68, 0.33).move_to([-3.60, -2.10, 0]),
        )
        right_views = VGroup(
            view_card("front", 3.05, 1.95, 0.36).move_to([3.60, -0.18, 0]),
            view_card("right", 2.55, 1.95, 0.34).move_to([6.05, -0.18, 0]),
            view_card("top", 3.05, 1.68, 0.33).move_to([3.60, 1.42, 0]),
        )
        group = VGroup(left, right_panel, div, lt, rt, left_views, right_views)
        self.fadd(group)
        self.play(FadeIn(left), FadeIn(right_panel), Create(div), FadeIn(lt), FadeIn(rt), run_time=RT_SLOW)
        self.play(FadeIn(left_views[0]), FadeIn(right_views[0]), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(left_views[1]), FadeIn(right_views[1]), run_time=RT_REVEAL)
        self.wait(PAUSE_VIEW)
        self.play(FadeIn(left_views[2]), FadeIn(right_views[2]), run_time=RT_REVEAL)
        self.wait(PAUSE_LONG)
        rule = safe_bottom_callout("ISO E: opuesto  ·  ISO A: mismo lado", BLUE, 6.8, 22)
        self.fadd(rule)
        self.play(FadeIn(rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(rule, group, title)

    def algorithm(self):
        self.transition(9, "MÉTODO DE LECTURA", "Seis pasos claros para cualquier lámina")
        title = self.stage_title("LEE UNA LÁMINA EN 6 PASOS",
                                 "Una decisión por vez; la figura nunca queda cubierta por texto.", BLUE)
        steps_data = [
            ("IDENTIFICA EL SÍMBOLO", BLUE),
            ("DECIDE ISO E / ISO A", ORANGE),
            ("UBICA EL ALZADO", BLUE),
            ("LOCALIZA PLANTA Y LATERALES", TEAL),
            ("VERIFICA OPUESTO / MISMO", GREEN),
            ("RECONSTRUYE EL 3D", PURPLE),
        ]
        steps = VGroup(*[step_chip(i+1, text, col, 5.0) for i,(text,col) in enumerate(steps_data)])
        steps.arrange(DOWN, buff=0.12).move_to([-4.55, -0.50, 0])
        sheet = paper_panel(7.0, 5.55, 0.40).move_to([3.60, -0.50, 0])
        sym = projection_symbol(False, 0.58).move_to([1.45, -2.30, 0])
        # Measured gaps: top bottom=0.60; front top=0.45.
        front = view_card("front", 3.40, 1.90, 0.37).move_to([3.55, -0.50, 0])
        top = view_card("top", 3.40, 1.70, 0.34).move_to([3.55, 1.45, 0])
        side = view_card("right", 2.55, 1.90, 0.34).move_to([5.72, -0.50, 0])
        self.fadd(steps, sheet, sym, front, top, side)
        self.play(FadeIn(sheet), run_time=RT)
        for i, step in enumerate(steps):
            self.play(FadeIn(step, shift=RIGHT * 0.05), run_time=RT_FAST)
            self.play(Circumscribe(step, color=steps_data[i][1], fade_out=True), run_time=RT)
            if i == 0:
                self.play(Create(sym), run_time=RT_REVEAL)
            elif i == 2:
                self.play(FadeIn(front), run_time=RT_REVEAL)
            elif i == 3:
                self.play(FadeIn(top), FadeIn(side), run_time=RT_REVEAL)
            elif i == 4:
                self.play(Circumscribe(VGroup(front, top, side), color=GREEN, fade_out=True), run_time=RT_SLOW)
            elif i == 5:
                self.play(Indicate(front, color=PURPLE), Indicate(top, color=PURPLE),
                          Indicate(side, color=PURPLE), run_time=RT)
            self.wait(PAUSE_READ)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(steps, sheet, sym, front, top, side, title)

    def challenge(self):
        self.transition(10, "DESAFÍO GUIADO", "Predice primero; verifica después")
        title = self.stage_title("DESAFÍO DE LECTURA",
                                 "Decide dónde deben ir la planta y el lateral derecho.", BLUE)
        sym = projection_symbol(False, 0.82).move_to([-5.10, 0.50, 0])
        q = badge("¿QUÉ MÉTODO ES?", BLUE, 17).next_to(sym, UP, buff=0.26)
        # Slots are separated vertically: front top=0.50; top-slot bottom=0.65.
        front = view_card("front", 3.75, 2.20, 0.42).move_to([0, -0.60, 0])
        top_slot = RoundedRectangle(width=3.75, height=1.75, corner_radius=0.14,
                                    stroke_color=TEAL, stroke_width=1.8,
                                    fill_color=PALE_TEAL, fill_opacity=0.18).move_to([0, 1.525, 0])
        side_slot = RoundedRectangle(width=3.05, height=2.20, corner_radius=0.14,
                                     stroke_color=ORANGE, stroke_width=1.8,
                                     fill_color=PALE_ORANGE, fill_opacity=0.18).move_to([5.05, -0.60, 0])
        tq = safe_text("PLANTA ?", 22, TEAL, BOLD).move_to(top_slot)
        sq = safe_text("LATERAL D. ?", 22, ORANGE, BOLD).move_to(side_slot)
        think = safe_bottom_callout("PIENSA ANTES DE REVELAR", INK, 6.0, 22)
        setup = VGroup(sym, q, front, top_slot, side_slot, tq, sq, think)
        self.fadd(setup)
        self.play(Create(sym), FadeIn(q), run_time=RT_REVEAL)
        self.play(FadeIn(front), run_time=RT_REVEAL)
        self.play(FadeIn(top_slot), FadeIn(tq), FadeIn(side_slot), FadeIn(sq), run_time=RT_REVEAL)
        self.play(FadeIn(think), run_time=RT)
        self.wait(PAUSE_CHALLENGE)

        method = callout("TERCER DIEDRO · ISO A", TEAL, 4.6, 22).move_to([-5.05, -1.62, 0])
        top_view_card = view_card("top", 3.75, 1.75, 0.37).move_to(top_slot)
        side_view_card = view_card("right", 3.05, 2.20, 0.38).move_to(side_slot)
        ans = safe_bottom_callout("MISMO LADO: planta arriba · lateral derecho a la derecha", GREEN, 8.0, 21)
        self.fadd(method)
        self.play(FadeOut(think), FadeIn(method), run_time=RT)
        self.fadd(top_view_card)
        self.play(FadeOut(top_slot), FadeOut(tq), FadeIn(top_view_card), run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)
        self.fadd(side_view_card)
        self.play(FadeOut(side_slot), FadeOut(sq), FadeIn(side_view_card), run_time=RT_CAMERA)
        self.wait(PAUSE_VIEW)
        self.fadd(ans)
        self.play(FadeIn(ans), run_time=RT)
        self.wait(PAUSE_LONG)
        self.fixed_fade_out(sym, q, front, method, top_view_card, side_view_card, ans, title)
