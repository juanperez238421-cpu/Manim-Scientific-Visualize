#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Técnico y CAD — V16 CLEAN DIRECTOR FINAL.

Director-final refinement of the real V14 choreography rebuild.

Review basis:
- V13: only a pacing wrapper; visually almost identical to V12.
- Monge V5: best point-first projection explanation and literal abatimiento.
- ISO A / ISO E V3: best sequential projection/extraction language and clean rays.
- V14: successfully rebuilt the lesson using those ideas.
- V15 audit: proved that embedding a full ISO A/E comparison at the end created
  unnecessary visual stacking and weakened the 3D→2D learning objective.

V16 keeps the complete V14 rebuilt core, then deliberately stops before the
full A/E comparison and replaces that tail with a clean, focused synthesis:
1) three finished 2D views;
2) one concise note that ISO A/E changes placement, not the projection process;
3) a large five-step mental model with separate animated cards.

ManimCE 0.20.1 · 1920×1080 · 30 fps · literal -pqh.
"""
from __future__ import annotations

from manim import *

from Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V14_REBUILT_CHOREOGRAPHY import (
    Projection3Dto2DV14RebuiltChoreography,
    T,
    INK, MUTED, GRID,
    FRONT_COLOR, TOP_COLOR, RIGHT_COLOR,
)


class _BeginISOComparison(Exception):
    """Internal director signal: V14 core is finished; replace its old tail."""


class Projection3Dto2DV16CleanDirectorFinal(Projection3Dto2DV14RebuiltChoreography):
    """V14 core + clean director ending."""

    @staticmethod
    def _texts(mob):
        out = []
        txt = getattr(mob, "text", None)
        if isinstance(txt, str):
            out.append(txt)
        for sub in getattr(mob, "submobjects", []):
            out.extend(Projection3Dto2DV16CleanDirectorFinal._texts(sub))
        return out

    @classmethod
    def _has_text(cls, mob, phrase):
        return any(phrase in t for t in cls._texts(mob))

    def add_fixed_in_frame_mobjects(self, *mobjects):
        # V14 attempts to begin a full ISO A/E comparison after the real
        # 3D→2D construction is complete.  Stop exactly there and hand control
        # back to V16's cleaner ending.
        if any(self._has_text(m, "LAS VISTAS SON LAS MISMAS") for m in mobjects):
            raise _BeginISOComparison

        # Generic safe-width guard for fixed classroom text.
        for mob in mobjects:
            try:
                if mob.width > 14.1:
                    mob.scale_to_fit_width(14.1)
            except Exception:
                pass
        return super().add_fixed_in_frame_mobjects(*mobjects)

    def _fixed_fade(self, mob, opacity, run_time):
        self.play(mob.animate.set_opacity(opacity), run_time=T(run_time), rate_func=smooth)

    def _clean_finale(self):
        # At this point V14 has already:
        # - projected FRONT/TOP/RIGHT,
        # - removed the source solid,
        # - folded PH and PL,
        # - demonstrated correspondence,
        # - faded the physical planes.
        # The remaining geometry is therefore the correct place to transition
        # from physical construction to a clean 2D summary.
        current = list(self.mobjects)
        if current:
            self.play(*[FadeOut(m) for m in current], run_time=T(0.85), rate_func=smooth)
            self.remove(*current)
        self.wait(T(0.55))

        # ------------------------------------------------------------------
        # A · CLEAN THREE-VIEW SHEET
        # ------------------------------------------------------------------
        title = Text("TRES VISTAS · UN MISMO OBJETO", font_size=44, color=INK, weight=BOLD)
        subtitle = Text("La geometría ya está proyectada: ahora solo la organizamos en la hoja.", font_size=25, color=MUTED)
        title.to_edge(UP, buff=0.38)
        subtitle.next_to(title, DOWN, buff=0.12)

        front = self.front_view_2d(0.68)
        top = self.top_view_2d(0.60)
        right = self.right_view_2d(0.72)

        front.move_to(LEFT * 1.55 + DOWN * 0.75)
        top.move_to(LEFT * 1.55 + UP * 1.75)
        right.move_to(RIGHT * 3.00 + DOWN * 0.75)

        lf = Text("ALZADO", font_size=24, color=FRONT_COLOR, weight=BOLD).next_to(front, DOWN, buff=0.18)
        lt = Text("PLANTA", font_size=24, color=TOP_COLOR, weight=BOLD).next_to(top, DOWN, buff=0.18)
        lr = Text("PERFIL", font_size=24, color=RIGHT_COLOR, weight=BOLD).next_to(right, DOWN, buff=0.18)

        vg = DashedLine(UP * 0.66, DOWN * 0.66, dash_length=0.08, color=GRID, stroke_width=1.5)
        vg.move_to(LEFT * 1.55 + UP * 0.50)
        hg = DashedLine(LEFT * 0.90, RIGHT * 0.90, dash_length=0.08, color=GRID, stroke_width=1.5)
        hg.move_to(RIGHT * 0.72 + DOWN * 0.75)

        sheet = VGroup(title, subtitle, front, top, right, lf, lt, lr, vg, hg)
        self.add_fixed_in_frame_mobjects(*sheet)
        for m in sheet:
            m.set_opacity(0)

        self._fixed_fade(title, 1, 0.70)
        self._fixed_fade(subtitle, 1, 0.55)
        self.play(FadeIn(front, shift=UP*0.08), FadeIn(lf), run_time=T(0.90), rate_func=smooth)
        self.wait(T(0.65))
        self.play(FadeIn(top, shift=DOWN*0.08), FadeIn(lt), run_time=T(0.90), rate_func=smooth)
        self.wait(T(0.65))
        self.play(FadeIn(right, shift=LEFT*0.08), FadeIn(lr), run_time=T(0.90), rate_func=smooth)
        self.wait(T(0.70))
        self.play(Create(vg), run_time=T(0.75))
        self.wait(T(0.45))
        self.play(Create(hg), run_time=T(0.75))
        self.wait(T(2.20))

        # ------------------------------------------------------------------
        # B · A/E CONNECTION WITHOUT DERAILING THE LESSON
        # ------------------------------------------------------------------
        ae = RoundedRectangle(
            width=11.9, height=1.02, corner_radius=0.12,
            stroke_color=GRID, stroke_width=1.2,
            fill_color=WHITE, fill_opacity=0.98,
        ).to_edge(DOWN, buff=0.28)
        ae1 = Text("ISO A / ISO E", font_size=24, color=INK, weight=BOLD)
        ae2 = Text("cambia la posición de las vistas en la hoja · no cambia cómo se proyectan", font_size=23, color=MUTED)
        ae_text = VGroup(ae1, ae2).arrange(DOWN, buff=0.08).move_to(ae)
        ae_group = VGroup(ae, ae_text)
        self.add_fixed_in_frame_mobjects(ae_group)
        ae_group.set_opacity(0)
        self.play(ae_group.animate.set_opacity(1), run_time=T(0.70), rate_func=smooth)
        self.wait(T(2.35))

        # Clear the sheet deliberately, not abruptly.
        self.play(*[m.animate.set_opacity(0) for m in sheet], ae_group.animate.set_opacity(0), run_time=T(0.85), rate_func=smooth)
        self.remove_fixed_in_frame_mobjects(*sheet, ae_group)
        self.wait(T(0.45))

        # ------------------------------------------------------------------
        # C · FIVE-STEP MENTAL MODEL — independent cards, large text
        # ------------------------------------------------------------------
        final_title = Text("DE 3D A 2D · MÉTODO MENTAL", font_size=43, color=INK, weight=BOLD)
        final_title.to_edge(UP, buff=0.48)
        final_sub = Text("Cada vista sigue exactamente la misma secuencia.", font_size=25, color=MUTED)
        final_sub.next_to(final_title, DOWN, buff=0.14)
        self.add_fixed_in_frame_mobjects(final_title, final_sub)
        final_title.set_opacity(0); final_sub.set_opacity(0)
        self._fixed_fade(final_title, 1, 0.65)
        self._fixed_fade(final_sub, 1, 0.50)

        specs = [
            (1, "MIRAR", "elige una dirección", FRONT_COLOR),
            (2, "PROYECTAR ⟂", "rayos perpendiculares", INK),
            (3, "TRAZAR", "forma el contorno", TOP_COLOR),
            (4, "ABATIR", "lleva el plano a la hoja", RIGHT_COLOR),
            (5, "ALINEAR", "conserva dimensiones", INK),
        ]
        cards = VGroup()
        for n, head, body, col in specs:
            box = RoundedRectangle(
                width=2.45, height=2.15, corner_radius=0.16,
                stroke_color=GRID, stroke_width=1.25,
                fill_color=WHITE, fill_opacity=1.0,
            )
            circ = Circle(radius=0.30, stroke_color=col, stroke_width=2.5)
            num = Text(str(n), font_size=22, color=col, weight=BOLD).move_to(circ)
            h = Text(head, font_size=22, color=INK, weight=BOLD)
            b = Text(body, font_size=17, color=MUTED)
            b.scale_to_fit_width(2.00)
            content = VGroup(VGroup(circ, num), h, b).arrange(DOWN, buff=0.14).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.22)
        cards.scale_to_fit_width(13.45)
        cards.move_to(DOWN * 0.35)

        for card in cards:
            self.add_fixed_in_frame_mobjects(card)
            card.set_opacity(0)
        for card in cards:
            self.play(FadeIn(card, shift=UP*0.10), run_time=T(0.62), rate_func=smooth)
            self.wait(T(0.48))

        closing = Text(
            "Objeto 3D  →  proyectantes ortogonales  →  vistas 2D",
            font_size=28, color=INK, weight=BOLD,
        ).to_edge(DOWN, buff=0.46)
        self.add_fixed_in_frame_mobjects(closing)
        closing.set_opacity(0)
        self._fixed_fade(closing, 1, 0.70)
        self.wait(T(4.20))

        self.play(
            final_title.animate.set_opacity(0), final_sub.animate.set_opacity(0),
            closing.animate.set_opacity(0),
            *[c.animate.set_opacity(0) for c in cards],
            run_time=T(0.90), rate_func=smooth,
        )
        self.remove_fixed_in_frame_mobjects(final_title, final_sub, closing, *list(cards))

    def construct(self):
        try:
            super().construct()
        except _BeginISOComparison:
            self._clean_finale()


# Preview:
# manim -pql Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V16_CLEAN_DIRECTOR_FINAL.py Projection3Dto2DV16CleanDirectorFinal --disable_caching
# Final:
# manim -pqh Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V16_CLEAN_DIRECTOR_FINAL.py Projection3Dto2DV16CleanDirectorFinal --disable_caching
