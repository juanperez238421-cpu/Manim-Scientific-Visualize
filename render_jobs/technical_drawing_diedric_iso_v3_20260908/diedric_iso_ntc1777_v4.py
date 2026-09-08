#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V4 senior QA correction over the V3 diedric-system redesign.

This revision keeps the successful V3 visual language but corrects the issues
found by frame-by-frame QA: muddy multi-face shadows, clipped final title,
first/third-angle layout collisions, a projection-plane label collision, the
dihedral ground-line label collision, and the challenge prompt overlap.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
from manim import *

# Load V3 from the same folder explicitly so the render is independent of the
# caller's working directory / Python path.
_BASE_PATH = Path(__file__).with_name("diedric_iso_ntc1777_v3.py")
_SPEC = importlib.util.spec_from_file_location("_diedric_v3_base", _BASE_PATH)
_BASE = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_BASE)

DiedricBase = _BASE.DiedricISOProjectionV3Senior

# Reuse the established V3 palette/timing so V4 is a genuine QA revision,
# not an unrelated style reset.
BLUE = _BASE.BLUE
CYAN = _BASE.CYAN
TEAL = _BASE.TEAL
ORANGE = _BASE.ORANGE
GREEN = _BASE.GREEN
MID = _BASE.MID
NAVY = _BASE.NAVY
INK = _BASE.INK
LIGHT = _BASE.LIGHT
PALE_BLUE = _BASE.PALE_BLUE
PALE_TEAL = _BASE.PALE_TEAL
PALE_ORANGE = _BASE.PALE_ORANGE
FACE_FRONT = _BASE.FACE_FRONT
WHITE = _BASE.WHITE
RT_FAST = _BASE.RT_FAST
RT = _BASE.RT
RT_SLOW = _BASE.RT_SLOW
RT_HERO = _BASE.RT_HERO
PAUSE_READ = _BASE.PAUSE_READ
PAUSE_EXPLAIN = _BASE.PAUSE_EXPLAIN
PAUSE_LONG = _BASE.PAUSE_LONG


class DiedricISOProjectionV4Senior(DiedricBase):
    """Frame-QA corrected final classroom scene."""

    def mechanical_part(self, s=0.86, include_shadow=True):
        """Same asymmetric bracket, with one clean floor shadow only."""
        boxes = VGroup(
            self.iso_box(0.0, 5.0, 0.0, 3.0, 0.0, 0.55, s),
            self.iso_box(0.60, 1.70, 0.65, 1.85, 0.55, 1.15, s),
            self.iso_box(2.30, 3.90, 0.35, 2.65, 0.55, 1.55, s),
            self.iso_box(3.90, 5.00, 0.55, 2.45, 0.55, 3.10, s),
        )
        tower_hole = Circle(
            radius=0.37*s,
            stroke_color=BLUE,
            stroke_width=3.0,
            fill_color=FACE_FRONT,
            fill_opacity=1,
        ).move_to(self.iso_pt(4.45, 0.0, 2.08, s))
        tower_cross = VGroup(
            DashedLine(
                tower_hole.get_left()+LEFT*0.15,
                tower_hole.get_right()+RIGHT*0.15,
                dash_length=0.08,
                color=MID,
                stroke_width=1.25,
            ),
            DashedLine(
                tower_hole.get_bottom()+DOWN*0.15,
                tower_hole.get_top()+UP*0.15,
                dash_length=0.08,
                color=MID,
                stroke_width=1.25,
            ),
        )
        boss_center = self.iso_pt(1.15, 1.25, 1.15, s)
        boss_hole = Ellipse(
            width=0.72*s,
            height=0.27*s,
            stroke_color=TEAL,
            stroke_width=2.6,
            fill_color=WHITE,
            fill_opacity=1,
        ).rotate(0.32).move_to(boss_center)
        part = VGroup(boxes, tower_hole, tower_cross, boss_hole)
        if include_shadow:
            floor_shadow = Ellipse(
                width=5.7*s,
                height=0.46*s,
                stroke_width=0,
                fill_color=BLACK,
                fill_opacity=0.07,
            ).move_to(self.iso_pt(2.65, 1.35, 0.0, s) + DOWN*(0.20*s))
            return VGroup(floor_shadow, part)
        return part

    def orthographic_projection(self):
        h = self.section_header(
            1,
            "PROYECCIÓN ORTOGONAL",
            "Sin perspectiva: cada vista registra la geometría desde una dirección exacta.",
        )
        self.add(h)
        part = self.mechanical_part(0.82).move_to(LEFT*3.55+DOWN*0.52)
        obs = self.observer("OBSERVADOR", BLUE, 1.05).move_to(LEFT*6.55+DOWN*0.40)
        plane = self.vertical_plane().move_to(RIGHT*1.05+DOWN*0.42)
        plane_lab = self.mini_label("PLANO DE PROYECCIÓN", BLUE, 17, PALE_BLUE).move_to(RIGHT*1.00+UP*2.15)

        self.play(FadeIn(obs), DrawBorderThenFill(part[1]), FadeIn(part[0]), run_time=RT_HERO)
        self.play(FadeIn(plane), FadeIn(plane_lab), run_time=RT)
        self.wait(PAUSE_READ)

        target_center = plane.get_center()+RIGHT*0.10
        starts = [
            part[1].get_corner(UL), part[1].get_corner(UR),
            part[1].get_corner(DL), part[1].get_corner(DR),
        ]
        targets = [
            target_center+LEFT*0.95+UP*1.32,
            target_center+RIGHT*0.95+UP*1.08,
            target_center+LEFT*0.95+DOWN*1.08,
            target_center+RIGHT*0.95+DOWN*1.32,
        ]
        rays = self.ray_fan(starts, targets)
        arrow = Arrow(obs.get_right(), part.get_left(), buff=0.20, color=BLUE, stroke_width=3.5)
        self.play(GrowArrow(arrow), run_time=RT)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.12), run_time=RT_SLOW)
        self.wait(PAUSE_EXPLAIN)

        front = self.front_view(0.48, BLUE).move_to(plane.get_center())
        self.play(Create(front), run_time=RT_SLOW)
        self.play(Indicate(front, color=CYAN, scale_factor=1.03), run_time=RT_SLOW)
        self.wait(PAUSE_READ)

        drawing = self.blueprint_grid(5.4, 5.25).to_edge(RIGHT, buff=0.38).shift(DOWN*0.25)
        front_big = self.front_view(0.69).move_to(drawing)
        label = self.mini_label("ALZADO / FRONT", BLUE, 19).next_to(drawing, UP, buff=-0.18)
        self.play(FadeOut(rays), FadeOut(arrow), run_time=RT_FAST)
        self.play(FadeIn(drawing), FadeIn(label), run_time=RT)
        self.play(TransformFromCopy(front, front_big), run_time=RT_HERO)

        # QA correction: the apparatus is removed after the transfer so the
        # plane label cannot sit beneath the drawing sheet.
        self.play(
            FadeOut(obs), FadeOut(part), FadeOut(plane), FadeOut(plane_lab), FadeOut(front),
            run_time=RT,
        )
        key = self.emphasis("1 dirección → 1 vista", GREEN, 29, 4.5).to_edge(DOWN, buff=0.25).shift(RIGHT*3.8)
        self.play(FadeIn(key), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def dihedral_system(self):
        h = self.section_header(
            2,
            "EL SISTEMA DIÉDRICO",
            "Plano vertical + plano horizontal. Después se abaten para formar una sola lámina.",
        )
        self.add(h)
        pv = self.vertical_plane().move_to(LEFT*2.70+UP*0.10)
        ph = self.horizontal_plane().move_to(LEFT*1.25+DOWN*2.00)
        lt = Line(LEFT*4.38+DOWN*1.38, RIGHT*0.72+DOWN*1.38, color=NAVY, stroke_width=4)
        lt_lab = self.mini_label("LÍNEA DE TIERRA", NAVY, 16).next_to(lt, DOWN, buff=0.12)
        pv_lab = self.mini_label("PV · ALZADO", BLUE, 17, PALE_BLUE).move_to(LEFT*2.65+UP*2.25)
        ph_lab = self.mini_label("PH · PLANTA", TEAL, 17, PALE_TEAL).move_to(LEFT*0.90+DOWN*2.80)
        part = self.mechanical_part(0.56).move_to(LEFT*1.75+DOWN*0.75)

        self.play(FadeIn(pv), FadeIn(ph), Create(lt), run_time=RT_SLOW)
        self.play(FadeIn(pv_lab), FadeIn(ph_lab), FadeIn(lt_lab), run_time=RT)
        self.play(DrawBorderThenFill(part[1]), FadeIn(part[0]), run_time=RT_HERO)
        self.wait(PAUSE_EXPLAIN)

        front_trace = self.front_view(0.30, BLUE).move_to(LEFT*2.45+UP*0.18)
        pv_targets = [
            front_trace.get_corner(UL), front_trace.get_corner(UR),
            front_trace.get_corner(DL), front_trace.get_corner(DR),
        ]
        starts = [part.get_corner(UL), part.get_corner(UR), part.get_corner(DL), part.get_corner(DR)]
        pv_rays = self.ray_fan(starts, pv_targets, ORANGE)
        self.play(LaggedStart(*[Create(r) for r in pv_rays], lag_ratio=0.11), run_time=RT_SLOW)
        self.play(Create(front_trace), run_time=RT_SLOW)
        self.wait(PAUSE_READ)

        top_trace = self.top_view(0.28, TEAL).move_to(LEFT*0.85+DOWN*2.00)
        ph_targets = [
            top_trace.get_corner(UL), top_trace.get_corner(UR),
            top_trace.get_corner(DL), top_trace.get_corner(DR),
        ]
        ph_rays = self.ray_fan(starts, ph_targets, ORANGE)
        self.play(LaggedStart(*[Create(r) for r in ph_rays], lag_ratio=0.11), run_time=RT_SLOW)
        self.play(Create(top_trace), run_time=RT_SLOW)
        self.wait(PAUSE_EXPLAIN)

        sheet = self.blueprint_grid(6.05, 5.55).to_edge(RIGHT, buff=0.45).shift(DOWN*0.20)
        sheet_title = self.mini_label("ABATIMIENTO → LÁMINA 2D", NAVY, 18).next_to(sheet, UP, buff=-0.18)
        f2 = self.front_view(0.50).move_to(sheet.get_center()+UP*1.05)
        t2 = self.top_view(0.50).move_to(sheet.get_center()+DOWN*1.55)
        div = Line(
            sheet.get_left()+RIGHT*0.35,
            sheet.get_right()+LEFT*0.35,
            color=LIGHT,
            stroke_width=1.4,
        ).move_to(sheet.get_center()+DOWN*0.12)

        # QA correction: remove the ground-line label before the lower trace
        # and sheet occupy the same visual zone.
        self.play(FadeOut(pv_rays), FadeOut(ph_rays), FadeOut(part), FadeOut(lt_lab), run_time=RT)
        self.play(FadeIn(sheet), FadeIn(sheet_title), Create(div), run_time=RT_SLOW)
        self.play(TransformFromCopy(front_trace, f2), run_time=RT_SLOW)
        self.play(TransformFromCopy(top_trace, t2), run_time=RT_SLOW)
        abate = Arrow(LEFT*0.45+DOWN*0.65, RIGHT*1.55+DOWN*1.45, color=TEAL, stroke_width=3.0)
        note = self.text("PH se abate 90°", 22, BOLD, TEAL).next_to(abate, UP, buff=0.10)
        self.play(GrowArrow(abate), FadeIn(note), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def first_angle(self):
        h = self.section_header(
            4,
            "PRIMER DIEDRO · FIRST-ANGLE · ISO E",
            "Orden físico: observador → objeto → plano. En la lámina, las vistas quedan al lado opuesto.",
        )
        self.add(h)
        obs = self.observer("OBSERVADOR", BLUE, 0.95).move_to(LEFT*6.10+DOWN*0.45)
        obj = self.mechanical_part(0.48).move_to(LEFT*2.75+DOWN*0.55)
        plane = self.vertical_plane().scale(0.82).move_to(RIGHT*0.25+DOWN*0.45)
        one = self.mini_label("1 · OBSERVADOR", BLUE, 18).move_to(LEFT*5.55+UP*2.10)
        two = self.mini_label("2 · OBJETO", ORANGE, 18, PALE_ORANGE).move_to(LEFT*2.75+UP*2.10)
        three = self.mini_label("3 · PLANO", TEAL, 18, PALE_TEAL).move_to(RIGHT*0.20+UP*2.10)
        a1 = Arrow(obs.get_right(), obj.get_left(), buff=0.18, color=BLUE, stroke_width=3.4)
        a2 = Arrow(obj.get_right(), plane.get_left(), buff=0.18, color=ORANGE, stroke_width=3.4)

        self.play(FadeIn(obs), DrawBorderThenFill(obj[1]), FadeIn(obj[0]), FadeIn(plane), run_time=RT_HERO)
        self.play(FadeIn(one), FadeIn(two), FadeIn(three), run_time=RT)
        self.play(GrowArrow(a1), run_time=RT)
        self.play(GrowArrow(a2), run_time=RT)
        self.wait(PAUSE_EXPLAIN)

        rule = self.emphasis("La vista se coloca en el lado OPUESTO", ORANGE, 27, 5.7).to_edge(RIGHT, buff=0.48).shift(DOWN*2.45)
        self.play(FadeIn(rule), run_time=RT)
        self.wait(PAUSE_READ)

        self.play(
            FadeOut(obs), FadeOut(obj), FadeOut(plane), FadeOut(a1), FadeOut(a2),
            FadeOut(one), FadeOut(two), FadeOut(three), FadeOut(rule),
            run_time=RT,
        )

        # QA correction: center the full cross first, then reserve a dedicated
        # left text column. No panel can sit behind the explanatory copy.
        layout = self.placement_cross(first_angle=True, compact=False).move_to(RIGHT*1.55+DOWN*0.42)
        side_note = VGroup(
            self.text("PRIMER DIEDRO", 28, BOLD, BLUE),
            self.text("PLANTA ↓", 24, BOLD, TEAL),
            self.text("LATERAL D. ←", 24, BOLD, ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).to_edge(LEFT, buff=0.55).shift(UP*0.10)
        compact_rule = self.emphasis("OPUESTO", ORANGE, 25, 3.25).next_to(side_note, DOWN, buff=0.42).align_to(side_note, LEFT)

        self.play(FadeIn(side_note[0]), run_time=RT)
        self.play(FadeIn(layout[0]), run_time=RT)
        self.play(FadeIn(side_note[1]), FadeIn(layout[1], shift=UP*0.20), run_time=RT_SLOW)
        self.play(FadeIn(side_note[2]), FadeIn(layout[2], shift=RIGHT*0.20), run_time=RT_SLOW)
        self.play(FadeIn(compact_rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def third_angle(self):
        h = self.section_header(
            5,
            "TERCER DIEDRO · THIRD-ANGLE · ISO A",
            "Orden físico: observador → plano → objeto. En la lámina, las vistas quedan del mismo lado.",
        )
        self.add(h)
        obs = self.observer("OBSERVADOR", BLUE, 0.95).move_to(LEFT*6.10+DOWN*0.45)
        plane = self.vertical_plane().scale(0.82).move_to(LEFT*2.40+DOWN*0.45)
        obj = self.mechanical_part(0.48).move_to(RIGHT*0.55+DOWN*0.55)
        one = self.mini_label("1 · OBSERVADOR", BLUE, 18).move_to(LEFT*5.55+UP*2.10)
        two = self.mini_label("2 · PLANO", TEAL, 18, PALE_TEAL).move_to(LEFT*2.40+UP*2.10)
        three = self.mini_label("3 · OBJETO", ORANGE, 18, PALE_ORANGE).move_to(RIGHT*0.55+UP*2.10)
        a1 = Arrow(obs.get_right(), plane.get_left(), buff=0.18, color=BLUE, stroke_width=3.4)
        a2 = Arrow(plane.get_right(), obj.get_left(), buff=0.18, color=ORANGE, stroke_width=3.4)

        self.play(FadeIn(obs), FadeIn(plane), DrawBorderThenFill(obj[1]), FadeIn(obj[0]), run_time=RT_HERO)
        self.play(FadeIn(one), FadeIn(two), FadeIn(three), run_time=RT)
        self.play(GrowArrow(a1), run_time=RT)
        self.play(GrowArrow(a2), run_time=RT)
        self.wait(PAUSE_EXPLAIN)

        rule = self.emphasis("La vista se coloca en el MISMO lado", GREEN, 27, 5.7).to_edge(RIGHT, buff=0.48).shift(DOWN*2.45)
        self.play(FadeIn(rule), run_time=RT)
        self.wait(PAUSE_READ)

        self.play(
            FadeOut(obs), FadeOut(obj), FadeOut(plane), FadeOut(a1), FadeOut(a2),
            FadeOut(one), FadeOut(two), FadeOut(three), FadeOut(rule),
            run_time=RT,
        )

        # QA correction: move the *whole* layout using its bounding box; this
        # keeps the upper plan view safely below the header/subtitle zone.
        layout = self.placement_cross(first_angle=False, compact=False).move_to(LEFT*1.45+DOWN*0.42)
        side_note = VGroup(
            self.text("TERCER DIEDRO", 28, BOLD, BLUE),
            self.text("PLANTA ↑", 24, BOLD, TEAL),
            self.text("LATERAL D. →", 24, BOLD, ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).to_edge(RIGHT, buff=0.55).shift(UP*0.10)
        compact_rule = self.emphasis("MISMO LADO", GREEN, 25, 3.65).next_to(side_note, DOWN, buff=0.42).align_to(side_note, LEFT)

        self.play(FadeIn(side_note[0]), run_time=RT)
        self.play(FadeIn(layout[0]), run_time=RT)
        self.play(FadeIn(side_note[1]), FadeIn(layout[1], shift=DOWN*0.20), run_time=RT_SLOW)
        self.play(FadeIn(side_note[2]), FadeIn(layout[2], shift=LEFT*0.20), run_time=RT_SLOW)
        self.play(FadeIn(compact_rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def challenge(self):
        h = self.section_header(
            8,
            "DESAFÍO DE LECTURA",
            "Mira el símbolo. Decide dónde deben ir la planta y el lateral derecho.",
        )
        self.add(h)
        symbol = self.projection_symbol(False, 0.92).to_edge(LEFT, buff=0.75).shift(UP*0.85)
        tag = self.mini_label("¿QUÉ MÉTODO ES?", BLUE, 19).next_to(symbol, UP, buff=0.30)
        front_panel = self.view_panel("ALZADO", self.front_view(0.56), 3.70, 2.70, BLUE).move_to(DOWN*1.10)
        top_slot = RoundedRectangle(
            width=3.70, height=2.70, corner_radius=0.14,
            stroke_color=TEAL, stroke_width=2.2, fill_opacity=0,
        ).next_to(front_panel, UP, buff=0.34)
        right_slot = RoundedRectangle(
            width=3.70, height=2.70, corner_radius=0.14,
            stroke_color=ORANGE, stroke_width=2.2, fill_opacity=0,
        ).next_to(front_panel, RIGHT, buff=0.34)
        q1 = self.text("PLANTA ?", 23, BOLD, TEAL).move_to(top_slot)
        q2 = self.text("LATERAL D. ?", 23, BOLD, ORANGE).move_to(right_slot)

        self.play(DrawBorderThenFill(symbol), FadeIn(tag), run_time=RT_SLOW)
        self.play(FadeIn(front_panel), Create(top_slot), Create(right_slot), FadeIn(q1), FadeIn(q2), run_time=RT_SLOW)

        # QA correction: the instruction sits in its own left-bottom zone,
        # completely clear of the ALZADO panel.
        prompt = self.emphasis("Piensa antes de revelar la respuesta", NAVY, 23, 4.75).move_to(LEFT*5.15+DOWN*2.55)
        self.play(FadeIn(prompt), run_time=RT)

        counter_anchor = LEFT*5.55+DOWN*0.30
        for n in [5, 4, 3, 2, 1]:
            c = Circle(radius=0.48, stroke_color=BLUE, stroke_width=2.3, fill_color=WHITE, fill_opacity=1).move_to(counter_anchor)
            num = self.text(str(n), 29, BOLD, BLUE).move_to(c)
            g = VGroup(c, num)
            self.play(FadeIn(g, scale=0.85), run_time=RT_FAST)
            self.wait(0.70)
            self.play(FadeOut(g, scale=1.08), run_time=RT_FAST)

        top = self.view_panel("PLANTA", self.top_view(0.56), 3.70, 2.70, TEAL).move_to(top_slot)
        right = self.view_panel("LATERAL DERECHO", self.right_view(0.56), 3.70, 2.70, ORANGE).move_to(right_slot)
        answer = self.emphasis("TERCER DIEDRO → MISMO LADO", GREEN, 23, 4.75).move_to(prompt)
        self.play(
            FadeOut(q1), FadeOut(q2), FadeOut(top_slot), FadeOut(right_slot),
            Transform(prompt, answer),
            run_time=RT,
        )
        self.play(FadeIn(top, shift=DOWN*0.20), FadeIn(right, shift=LEFT*0.20), run_time=RT_HERO)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def closing(self):
        kicker = self.text("MÉTODO DE LECTURA", 24, BOLD, BLUE)
        title = self.text("SÍMBOLO → ALZADO → POSICIÓN DE LAS VISTAS", 40, BOLD, NAVY)
        self.fit(title, 14.4, 0.82)
        title_group = VGroup(kicker, title).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        title_group.to_edge(UP, buff=0.60).to_edge(LEFT, buff=0.70)

        steps = [
            ("1", "IDENTIFICA EL SÍMBOLO", BLUE),
            ("2", "UBICA EL ALZADO", CYAN),
            ("3", "LEE PLANTA Y LATERALES", TEAL),
            ("4", "VERIFICA PRIMER / TERCER DIEDRO", ORANGE),
        ]
        cards = VGroup()
        for num, label, col in steps:
            n = Circle(radius=0.34, stroke_color=col, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
            nt = self.text(num, 22, BOLD, col).move_to(n)
            txt = self.text(label, 24, BOLD, INK)
            row = VGroup(VGroup(n, nt), txt).arrange(RIGHT, buff=0.22)
            box = RoundedRectangle(
                width=6.2, height=1.02, corner_radius=0.14,
                stroke_color=LIGHT, stroke_width=1.6,
                fill_color=WHITE, fill_opacity=1,
            )
            row.move_to(box).align_to(box, LEFT).shift(RIGHT*0.35)
            cards.add(VGroup(box, row))
        cards.arrange(DOWN, buff=0.22).move_to(LEFT*3.55+DOWN*0.75)

        final_part = self.mechanical_part(0.70).move_to(RIGHT*3.25+DOWN*0.60)
        final_note = self.emphasis("3D → 2D SIN AMBIGÜEDAD", GREEN, 27, 5.3).next_to(final_part, DOWN, buff=0.26)

        self.play(FadeIn(kicker), Write(title), run_time=RT_HERO)
        self.play(
            LaggedStart(*[FadeIn(c, shift=RIGHT*0.12) for c in cards], lag_ratio=0.13),
            run_time=RT_HERO*1.2,
        )
        self.play(DrawBorderThenFill(final_part[1]), FadeIn(final_part[0]), run_time=RT_HERO)
        self.play(FadeIn(final_note), run_time=RT)
        self.wait(PAUSE_LONG)


if __name__ == "__main__":
    pass
