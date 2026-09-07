#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle area by sector decomposition, step by step.

Dedicated refinement of the existing `derive_area_sectors_v3` animation from
`Geometry8_Circle_V3_Area.py`.

Pedagogical goals
-----------------
1. Start from a circle of radius r and circumference 2πr.
2. Divide the same area into many equal sectors.
3. Separate odd/even sectors and visibly alternate their orientation.
4. Interleave them into an almost-rectangle/parallelogram.
5. Derive the base as HALF the circumference: πr.
6. Derive the height as ONE radius: r, not 2r.
7. Explain the limiting idea: more sectors -> flatter edge -> exact area formula.

Visual contract
---------------
- ManimCE 0.20.1
- 1920x1080, 30 fps
- white background, black/gray classroom style
- projector-scale typography
- explicit camera focus and deliberate reading pauses
- no absolute paths or external assets
"""

from __future__ import annotations

import os
import numpy as np
from manim import *


# -----------------------------------------------------------------------------
# Render configuration
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
BLACK_LINE = BLACK
DARK_GRAY = "#333333"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D8D8D8"
VERY_LIGHT_GRAY = "#F1F1F1"
PAPER = "#FAFAFA"


class Geometry8CircleAreaDecomposition20260827(MovingCameraScene):
    """Full dedicated visual derivation of A = πr² by sector rearrangement."""

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography / layout helpers
    # ------------------------------------------------------------------
    def text(self, s: str, size: int = 30, weight=NORMAL) -> Text:
        return Text(s, font_size=size, color=BLACK, weight=weight)

    def math(self, s: str, size: int = 42) -> MathTex:
        return MathTex(s, font_size=size, color=BLACK)

    def header(self, number: int, title: str, subtitle: str) -> VGroup:
        badge = RoundedRectangle(
            width=0.78, height=0.54, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1,
        )
        badge_text = self.text(f"{number:02d}", 23, BOLD).move_to(badge)
        title_mob = self.text(title, 34, BOLD)
        title_mob.next_to(badge, RIGHT, buff=0.25)
        row = VGroup(VGroup(badge, badge_text), title_mob)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.text(subtitle, 21)
        if sub.width > 14.2:
            sub.scale_to_fit_width(14.2)
        sub.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def formula_panel(self, latex: str, width: float, size: int = 44) -> VGroup:
        box = RoundedRectangle(
            width=width, height=1.15, corner_radius=0.12,
            stroke_color=BLACK, stroke_width=2,
            fill_color=PAPER, fill_opacity=1,
        )
        eq = self.math(latex, size)
        if eq.width > width - 0.5:
            eq.scale_to_fit_width(width - 0.5)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(self, title: str, lines: list[str], width=5.8) -> VGroup:
        title_mob = self.text(title, 27, BOLD)
        body = VGroup(*[self.text(line, 22) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if content.width > width - 0.55:
            content.scale_to_fit_width(width - 0.55)
        box = RoundedRectangle(
            width=width, height=max(1.45, content.height + 0.55),
            corner_radius=0.12, stroke_color=BLACK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def clear_stage(self, *mobs: Mobject) -> None:
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.75)
        else:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.75)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def assert_safe(self, group: Mobject, label: str, margin=0.08) -> None:
        if group.get_left()[0] < -8 + margin or group.get_right()[0] > 8 - margin:
            raise ValueError(f"{label}: horizontal overflow")
        if group.get_bottom()[1] < -4.5 + margin or group.get_top()[1] > 4.5 - margin:
            raise ValueError(f"{label}: vertical overflow")

    # ------------------------------------------------------------------
    # Geometry builders
    # ------------------------------------------------------------------
    def sector_set(self, n: int, r: float, center: np.ndarray) -> VGroup:
        delta = TAU / n
        sectors = VGroup()
        for i in range(n):
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=i * delta,
                stroke_color=BLACK,
                stroke_width=1.15,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1,
            )
            sec.shift(center)
            sectors.add(sec)
        return sectors

    def alternating_stage_targets(self, n: int, r: float) -> VGroup:
        """Two separated rows: even sectors point up, odd sectors point down."""
        delta = TAU / n
        targets = VGroup()
        half = n // 2
        dx = 0.58
        for i in range(n):
            k = i // 2
            x = -3.0 + (k - (half - 1) / 2) * dx
            if i % 2 == 0:
                pivot = np.array([x, 0.25, 0])
                start = PI / 2 - delta / 2
            else:
                pivot = np.array([x + 6.1, 0.25, 0])
                start = -PI / 2 - delta / 2
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=start,
                stroke_color=BLACK,
                stroke_width=1.15,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1,
            )
            sec.shift(pivot)
            targets.add(sec)
        return targets

    def strip_targets(self, n: int, r: float, center=np.array([0.0, -0.15, 0.0])) -> VGroup:
        """Interleaved strip whose width approaches πr and height approaches r."""
        delta = TAU / n
        # n visible sector centers span approximately πr. This matches the
        # original V3 construction while making the half-circumference logic explicit.
        spacing = PI * r / n
        targets = VGroup()
        for i in range(n):
            x = center[0] + (i - (n - 1) / 2) * spacing
            if i % 2 == 0:
                pivot = np.array([x, center[1] - r / 2, 0])
                start = PI / 2 - delta / 2
            else:
                pivot = np.array([x, center[1] + r / 2, 0])
                start = -PI / 2 - delta / 2
            sec = AnnularSector(
                inner_radius=0,
                outer_radius=r,
                angle=delta,
                start_angle=start,
                stroke_color=BLACK,
                stroke_width=1.15,
                fill_color=VERY_LIGHT_GRAY if i % 2 == 0 else WHITE,
                fill_opacity=1,
            )
            sec.shift(pivot)
            targets.add(sec)
        return targets

    def strip_outline_guides(self, r: float) -> VGroup:
        # For the chosen target geometry, x extent is close to ±πr/2.
        x0, x1 = -PI * r / 2, PI * r / 2
        top_y, bottom_y = 0.61, -0.91
        top = DashedLine([x0, top_y, 0], [x1, top_y, 0], color=MID_GRAY, dash_length=0.10)
        bottom = DashedLine([x0, bottom_y, 0], [x1, bottom_y, 0], color=MID_GRAY, dash_length=0.10)
        return VGroup(top, bottom)

    # ------------------------------------------------------------------
    # Scene
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.opening()
        self.step_1_circle()
        self.step_2_cut()
        self.step_3_separate_and_alternate()
        self.step_4_interleave()
        self.step_5_base()
        self.step_6_height_not_2r()
        self.step_7_limit_and_formula()
        self.closing()

    def opening(self) -> None:
        title = self.text("¿POR QUÉ EL ÁREA DEL CÍRCULO ES  πr²?", 48, BOLD)
        subtitle = self.text("Descomponer → alternar → reordenar → medir", 29)
        formula = self.formula_panel(r"A=\pi r^2", 4.6, 54)
        g = VGroup(title, subtitle, formula).arrange(DOWN, buff=0.38)
        self.assert_safe(g, "opening")
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.08), run_time=0.8)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.9)
        self.wait(2.6)
        self.clear_stage(g)

    def step_1_circle(self) -> None:
        h = self.header(1, "PARTIMOS DEL CÍRCULO", "El radio r controla tanto la circunferencia como la altura de cada sector.")
        self.add(h)

        c = np.array([-3.0, -0.35, 0])
        r = 1.82
        circle = Circle(radius=r, color=BLACK, stroke_width=4).move_to(c)
        center_dot = Dot(c, radius=0.07, color=BLACK)
        radius = Arrow(c, c + RIGHT * r, buff=0, color=BLACK, stroke_width=3, tip_length=0.16)
        r_lab = self.math("r", 38).next_to(radius, UP, buff=0.10)
        circumference = self.formula_panel(r"C=2\pi r", 4.7, 46).move_to([3.5, 0.45, 0])
        note = self.note_panel(
            "IDEA CLAVE",
            ["No cambiaremos el área.", "Solo cortaremos y reordenaremos", "las mismas piezas del círculo."],
            width=5.2,
        ).move_to([3.5, -1.25, 0])
        g = VGroup(circle, center_dot, radius, r_lab, circumference, note, h)
        self.assert_safe(g, "step1")

        self.play(Create(circle), FadeIn(center_dot), run_time=1.0)
        self.play(GrowArrow(radius), Write(r_lab), run_time=0.9)
        self.play(FadeIn(circumference, shift=LEFT * 0.12), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.8)
        self.wait(3.0)
        self.clear_stage(VGroup(circle, center_dot, radius, r_lab, circumference, note, h))

    def step_2_cut(self) -> None:
        h = self.header(2, "DIVIDIMOS EL CÍRCULO EN SECTORES IGUALES", "Cada sector conserva radio r; al aumentar el número de sectores, los arcos se vuelven más pequeños.")
        self.add(h)
        n, r = 24, 2.05
        center = np.array([-2.7, -0.35, 0])
        outline = Circle(radius=r, color=BLACK, stroke_width=3).move_to(center)
        sectors = self.sector_set(n, r, center)
        radius = Line(center, center + RIGHT * r, color=BLACK, stroke_width=3)
        r_lab = self.math("r", 34).next_to(radius, UP, buff=0.08)
        count = self.formula_panel(r"24\ \text{sectores iguales}", 5.1, 37).move_to([3.5, 0.55, 0])
        note = self.note_panel(
            "OBSERVA",
            ["Todos llegan del centro al borde.", "Esa distancia siempre es r.", "La suma de sus áreas es el círculo."],
            width=5.5,
        ).move_to([3.5, -1.20, 0])
        g = VGroup(outline, sectors, radius, r_lab, count, note, h)
        self.assert_safe(g, "step2")

        self.play(Create(outline), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.025), run_time=1.8)
        self.play(Create(radius), Write(r_lab), run_time=0.7)
        self.play(FadeIn(count), run_time=0.7)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.8)
        self.wait(3.2)

        # Local focus: show that one sector has radial side length r.
        one = sectors[2]
        self.play(self.camera.frame.animate.set(width=8.8).move_to(center + RIGHT * 0.25), run_time=1.0)
        self.play(Indicate(one, color=MID_GRAY, scale_factor=1.06), run_time=0.9)
        self.wait(1.7)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=1.0)
        self.clear_stage(VGroup(outline, sectors, radius, r_lab, count, note, h))

    def step_3_separate_and_alternate(self) -> None:
        h = self.header(3, "SEPARAMOS Y ALTERNAMOS", "Un sector apunta hacia arriba y el siguiente hacia abajo; todavía no los apilamos.")
        self.add(h)
        n, r = 24, 1.38
        source = self.sector_set(n, r, np.array([0, -0.25, 0]))
        outline = Circle(radius=r, color=BLACK, stroke_width=3).move_to([0, -0.25, 0])
        stage = self.alternating_stage_targets(n, r)
        up_lab = self.text("PUNTAS HACIA ARRIBA", 24, BOLD).move_to([-3.1, -2.30, 0])
        down_lab = self.text("PUNTAS HACIA ABAJO", 24, BOLD).move_to([3.1, -2.30, 0])
        arrow = Arrow([-0.45, -0.25, 0], [0.45, -0.25, 0], color=MID_GRAY, buff=0.05, tip_length=0.16)
        self.assert_safe(VGroup(source, outline, stage, up_lab, down_lab, h), "step3")

        self.play(Create(outline), LaggedStart(*[FadeIn(s) for s in source], lag_ratio=0.02), run_time=1.6)
        self.wait(1.5)
        self.play(FadeOut(outline), run_time=0.45)
        self.play(
            LaggedStart(*[Transform(s, t) for s, t in zip(source, stage)], lag_ratio=0.025),
            run_time=2.8,
        )
        self.play(FadeIn(up_lab), FadeIn(down_lab), GrowArrow(arrow), run_time=0.9)
        self.wait(3.2)
        self.clear_stage(VGroup(source, up_lab, down_lab, arrow, h))

    def step_4_interleave(self) -> None:
        h = self.header(4, "INTERCALAMOS LAS PIEZAS", "Las puntas de una fila entran entre las de la otra: aparece una figura parecida a un rectángulo.")
        self.add(h)
        n, r = 24, 1.72
        source = self.alternating_stage_targets(n, r)
        target = self.strip_targets(n, r, center=np.array([0.0, -0.20, 0.0]))
        before = self.text("SEPARADOS", 24, BOLD).move_to([0, 2.30, 0])
        after = self.text("INTERCALADOS", 24, BOLD).move_to([0, 2.30, 0])
        self.assert_safe(VGroup(source, target, before, h), "step4")

        self.play(FadeIn(source), FadeIn(before), run_time=1.0)
        self.wait(1.4)
        self.play(Transform(before, after), run_time=0.5)
        self.play(
            LaggedStart(*[Transform(s, t) for s, t in zip(source, target)], lag_ratio=0.025),
            run_time=3.0,
        )
        guides = self.strip_outline_guides(r)
        self.play(Create(guides[0]), Create(guides[1]), run_time=0.9)
        note = self.text("Más sectores  →  borde más recto", 27, BOLD).move_to([0, -2.55, 0])
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.7)
        self.wait(3.0)
        self.clear_stage(VGroup(source, before, guides, note, h))

    def step_5_base(self) -> None:
        h = self.header(5, "¿DE DÓNDE SALE LA BASE?", "Los arcos de arriba contienen la mitad de la circunferencia; la otra mitad queda abajo.")
        self.add(h)
        n, r = 32, 1.78
        strip = self.strip_targets(n, r, center=np.array([-1.6, -0.15, 0]))
        self.play(FadeIn(strip), run_time=1.0)

        # A visual circumference is shown at right and split into two semicircles.
        c = np.array([4.7, 0.15, 0])
        small_r = 1.16
        circ = Circle(radius=small_r, color=BLACK, stroke_width=3).move_to(c)
        upper = Arc(radius=small_r, start_angle=0, angle=PI, color=BLACK, stroke_width=7).move_arc_center_to(c)
        lower = Arc(radius=small_r, start_angle=PI, angle=PI, color=MID_GRAY, stroke_width=7).move_arc_center_to(c)
        whole = self.math(r"2\pi r", 34).next_to(circ, DOWN, buff=0.15)
        half = self.formula_panel(r"\frac{2\pi r}{2}=\pi r", 4.5, 41).move_to([4.4, -2.25, 0])

        x0 = -1.6 - PI * r / 2
        x1 = -1.6 + PI * r / 2
        base_line = DoubleArrow([x0, -1.35, 0], [x1, -1.35, 0], color=BLACK, buff=0.02, tip_length=0.12)
        base_lab = self.math(r"\text{base}\approx\pi r", 39).next_to(base_line, DOWN, buff=0.14)
        self.assert_safe(VGroup(strip, circ, upper, lower, whole, half, base_line, base_lab, h), "step5")

        self.play(Create(circ), run_time=0.7)
        self.play(Create(upper), Create(lower), FadeIn(whole), run_time=1.0)
        self.play(self.camera.frame.animate.set(width=9.0).move_to(c + DOWN * 0.65), run_time=0.9)
        self.play(FadeIn(half, shift=UP * 0.08), run_time=0.8)
        self.wait(2.0)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=0.9)
        self.play(GrowFromCenter(base_line), Write(base_lab), run_time=1.0)
        self.wait(3.0)
        self.clear_stage(VGroup(strip, circ, upper, lower, whole, half, base_line, base_lab, h))

    def step_6_height_not_2r(self) -> None:
        h = self.header(6, "¿POR QUÉ LA ALTURA ES r Y NO 2r?", "Dos radios solo aparecerían si apiláramos dos sectores punta con punta; aquí están intercalados.")
        self.add(h)

        # Left: the misleading stacked picture.
        left_title = self.text("APILAR: NO ES LO QUE HACEMOS", 25, BOLD).move_to([-4.35, 2.05, 0])
        tri_up = Polygon([-4.8, -0.10, 0], [-3.9, -0.10, 0], [-4.35, 1.35, 0], color=BLACK, fill_color=VERY_LIGHT_GRAY, fill_opacity=1)
        tri_down = Polygon([-4.8, -0.10, 0], [-3.9, -0.10, 0], [-4.35, -1.55, 0], color=BLACK, fill_color=WHITE, fill_opacity=1)
        wrong_height = DoubleArrow([-3.55, -1.55, 0], [-3.55, 1.35, 0], color=MID_GRAY, buff=0.03, tip_length=0.12)
        wrong_lab = self.math(r"r+r=2r", 36).next_to(wrong_height, RIGHT, buff=0.12)
        midline = DashedLine([-4.9, -0.10, 0], [-3.8, -0.10, 0], color=MID_GRAY)

        # Right: the real interleaved strip.
        right_title = self.text("INTERCALAR: ESTA ES LA FIGURA REAL", 25, BOLD).move_to([2.25, 2.05, 0])
        n, r = 20, 1.72
        strip = self.strip_targets(n, r, center=np.array([2.1, -0.15, 0]))
        top_y, bottom_y = 0.61, -0.91
        top = DashedLine([-0.65, top_y, 0], [4.85, top_y, 0], color=MID_GRAY)
        bottom = DashedLine([-0.65, bottom_y, 0], [4.85, bottom_y, 0], color=MID_GRAY)
        real_height = DoubleArrow([5.20, bottom_y, 0], [5.20, top_y, 0], color=BLACK, buff=0.03, tip_length=0.12)
        real_lab = self.math("r", 42).next_to(real_height, RIGHT, buff=0.12)
        explanation = self.note_panel(
            "LA CLAVE",
            ["Cada sector tiene longitud radial r.", "Las puntas NO se suman verticalmente.", "Una punta entra entre dos sectores opuestos."],
            width=6.3,
        ).move_to([1.95, -2.55, 0])
        self.assert_safe(VGroup(left_title, tri_up, tri_down, wrong_height, wrong_lab, right_title,
                                strip, top, bottom, real_height, real_lab, explanation, h), "step6")

        self.play(FadeIn(left_title), Create(tri_up), Create(tri_down), Create(midline), run_time=1.1)
        self.play(GrowFromCenter(wrong_height), Write(wrong_lab), run_time=0.8)
        self.wait(1.8)
        self.play(FadeIn(right_title), FadeIn(strip), run_time=1.1)
        self.play(Create(top), Create(bottom), GrowFromCenter(real_height), Write(real_lab), run_time=0.9)
        self.play(self.camera.frame.animate.set(width=9.2).move_to([2.15, -0.25, 0]), run_time=0.9)
        self.play(FadeIn(explanation, shift=UP * 0.08), run_time=0.8)
        self.wait(3.2)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=0.9)
        self.clear_stage(VGroup(left_title, tri_up, tri_down, wrong_height, wrong_lab, midline,
                                right_title, strip, top, bottom, real_height, real_lab, explanation, h))

    def step_7_limit_and_formula(self) -> None:
        h = self.header(7, "MÁS SECTORES → MEJOR RECTÁNGULO → FÓRMULA EXACTA", "La reordenación conserva el área; en el límite, la base es πr y la altura es r.")
        self.add(h)

        # Compare 12 vs 40 sectors to make the limiting idea explicit.
        coarse = self.strip_targets(12, 1.42, center=np.array([-3.6, 0.55, 0]))
        fine = self.strip_targets(40, 1.42, center=np.array([3.1, 0.55, 0]))
        c_lab = self.text("12 sectores", 24, BOLD).next_to(coarse, UP, buff=0.22)
        f_lab = self.text("40 sectores", 24, BOLD).next_to(fine, UP, buff=0.22)
        arrow = Arrow([-0.55, 0.55, 0], [0.55, 0.55, 0], color=MID_GRAY, stroke_width=3, tip_length=0.18)
        arrow_lab = self.text("más fino", 22, BOLD).next_to(arrow, UP, buff=0.08)
        eq1 = self.formula_panel(r"A\approx(\pi r)(r)", 5.5, 46).move_to([-3.25, -2.25, 0])
        eq2 = self.formula_panel(r"\boxed{A=\pi r^2}", 5.5, 52).move_to([3.25, -2.25, 0])
        self.assert_safe(VGroup(coarse, fine, c_lab, f_lab, arrow, arrow_lab, eq1, eq2, h), "step7")

        self.play(FadeIn(coarse), FadeIn(c_lab), run_time=0.9)
        self.wait(1.2)
        self.play(GrowArrow(arrow), FadeIn(arrow_lab), FadeIn(fine), FadeIn(f_lab), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(eq1, shift=UP * 0.08), run_time=0.8)
        self.wait(1.7)
        self.play(FadeIn(eq2, shift=UP * 0.08), run_time=0.9)
        self.play(self.camera.frame.animate.set(width=8.2).move_to(eq2), run_time=0.9)
        self.wait(3.0)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=0.9)
        self.clear_stage(VGroup(coarse, fine, c_lab, f_lab, arrow, arrow_lab, eq1, eq2, h))

    def closing(self) -> None:
        title = self.text("RESUMEN PARA EL CUADERNO", 40, BOLD)
        steps = VGroup(
            self.text("1. Circunferencia completa: 2πr", 28),
            self.text("2. Base del reordenamiento: (2πr)/2 = πr", 28),
            self.text("3. Altura del reordenamiento: r", 28),
            self.text("4. Área = base × altura = (πr)(r)", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        formula = self.formula_panel(r"\boxed{A=\pi r^2}", 5.8, 55)
        g = VGroup(title, steps, formula).arrange(DOWN, buff=0.38)
        self.assert_safe(g, "closing")
        self.play(Write(title), run_time=0.9)
        for line in steps:
            self.play(FadeIn(line, shift=RIGHT * 0.10), run_time=0.55)
            self.wait(0.55)
        self.play(FadeIn(formula, shift=UP * 0.10), run_time=0.9)
        self.wait(4.2)


# Preview QA:
#   LESSON_TIME_SCALE=0.05 manim -pql Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827.py Geometry8CircleAreaDecomposition20260827 --disable_caching
# Final:
#   manim -pqh Geometry8_Circle_Area_Decomposition_STEP_BY_STEP_20260827.py Geometry8CircleAreaDecomposition20260827 --disable_caching
