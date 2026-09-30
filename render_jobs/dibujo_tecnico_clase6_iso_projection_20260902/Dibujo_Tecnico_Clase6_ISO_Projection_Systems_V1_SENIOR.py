#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dibujo Tecnico y CAD — Clase 6: sistemas de proyeccion ISO A / ISO E.

Animated ManimCE reconstruction of the supplied 18-slide PowerPoint deck.
Source-derived content preserved:
- Sistema diedrico.
- ISO(A) / third-angle (American) and ISO(E) / first-angle (European).
- Colombia: NTC1777 derived from ISO(A), as stated in the source deck.
- First/third-angle symbols.
- Six principal orthographic views.
- ISO A and ISO E view placement rules.
- Four worked visual examples and source-deck references.

Visual architecture follows the JP classroom protocol: 1920x1080, 30 fps,
white background, black/gray hierarchy, safe projector margins, numbered
section headers, staged animations, explicit pauses, and no external assets.

Target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

import os
import math
import numpy as np
from manim import *


# -----------------------------------------------------------------------------
# Render / visual contract
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#333333"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT = "#F2F2F2"
PAPER_GRAY = "#FAFAFA"

RUN_Q = 0.55
RUN = 0.95
RUN_SLOW = 1.35
RUN_FOLD = 1.75
PAUSE_S = 0.65
PAUSE_R = 1.45
PAUSE_E = 2.15
PAUSE_W = 3.00
PAUSE_SUM = 3.80


class TechnicalDrawingClass6ISO(Scene):
    """Full animated class: dihedral system and ISO A / ISO E projections."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.header = None
        self.subtitle = None
        self.section_no = 0

    # ------------------------------------------------------------------
    # Global timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography and safe layout
    # ------------------------------------------------------------------
    def txt(self, s, size=30, weight=NORMAL, color=BLACK_TEXT, **kwargs):
        return Text(s, font_size=size, weight=weight, color=color, **kwargs)

    def fit(self, mob, w=14.3, h=6.2):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def card(self, title, lines, width=6.0, height=None, title_size=26, body_size=22):
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.55, 4.7)
        if height is None:
            height = max(1.35, content.height + 0.62)
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def chip(self, text, width=4.4, size=26, fill=VERY_LIGHT):
        box = RoundedRectangle(
            width=width, height=0.78, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=fill, fill_opacity=1,
        )
        lab = self.txt(text, size, BOLD)
        self.fit(lab, width - 0.35, 0.48)
        lab.move_to(box)
        return VGroup(box, lab)

    def set_header(self, title, subtitle):
        self.section_no += 1
        num_box = RoundedRectangle(
            width=0.70, height=0.50, corner_radius=0.09,
            stroke_color=BLACK_LINE, stroke_width=1.9,
            fill_color=WHITE, fill_opacity=1,
        )
        num = self.txt(f"{self.section_no:02d}", 22, BOLD).move_to(num_box)
        heading = self.txt(title, 34, BOLD)
        self.fit(heading, 13.2, 0.58)
        row = VGroup(VGroup(num_box, num), heading).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.17).to_edge(LEFT, buff=0.46)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, stroke_color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.txt(subtitle, 20, color=DARK_GRAY)
        self.fit(sub, 14.2, 0.42)
        sub.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        new_h = VGroup(row, rule)
        if self.header is None:
            self.header = new_h
            self.subtitle = sub
            self.play(FadeIn(new_h), FadeIn(sub), run_time=RUN_Q)
        else:
            old_h, old_s = self.header, self.subtitle
            self.header, self.subtitle = new_h, sub
            self.play(ReplacementTransform(old_h, new_h), ReplacementTransform(old_s, sub), run_time=RUN_Q)

    def clear_content(self):
        keep = set()
        for persistent in (self.header, self.subtitle):
            if persistent is not None:
                keep.update(id(m) for m in persistent.get_family())
        remove = [m for m in self.mobjects if id(m) not in keep]
        if remove:
            self.play(*[FadeOut(m) for m in remove], run_time=RUN_Q)

    def close_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN)

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def iso_axes(self, origin=ORIGIN, scale=1.0):
        ex = np.array([0.90, 0.46, 0.0]) * scale
        ey = np.array([-0.90, 0.46, 0.0]) * scale
        ez = np.array([0.0, 1.0, 0.0]) * scale
        return origin, ex, ey, ez

    def iso_poly(self, pts, origin, ex, ey, ez, fill=WHITE, opacity=1.0, sw=2.0):
        def p(t):
            x, y, z = t
            return origin + x * ex + y * ey + z * ez
        return Polygon(
            *[p(t) for t in pts],
            stroke_color=BLACK_LINE, stroke_width=sw,
            fill_color=fill, fill_opacity=opacity,
        )

    def make_step_solid(self, scale=0.78):
        """Simple isometric step solid built from visible polygon faces."""
        o, ex, ey, ez = self.iso_axes(ORIGIN, scale)
        # footprint 3 x 2, lower height 1; back-left tower height 2
        top_low = self.iso_poly([(0,0,1),(3,0,1),(3,2,1),(0,2,1)], o, ex, ey, ez, VERY_LIGHT)
        front = self.iso_poly([(0,0,0),(3,0,0),(3,0,1),(0,0,1)], o, ex, ey, ez, "#E7E7E7")
        right = self.iso_poly([(3,0,0),(3,2,0),(3,2,1),(3,0,1)], o, ex, ey, ez, "#D7D7D7")
        left = self.iso_poly([(0,0,0),(0,2,0),(0,2,1),(0,0,1)], o, ex, ey, ez, "#EFEFEF")
        tower_front = self.iso_poly([(0,0,1),(1.25,0,1),(1.25,0,2.1),(0,0,2.1)], o, ex, ey, ez, "#DCDCDC")
        tower_side = self.iso_poly([(1.25,0,1),(1.25,1.1,1),(1.25,1.1,2.1),(1.25,0,2.1)], o, ex, ey, ez, "#CFCFCF")
        tower_top = self.iso_poly([(0,0,2.1),(1.25,0,2.1),(1.25,1.1,2.1),(0,1.1,2.1)], o, ex, ey, ez, WHITE)
        return VGroup(left, front, right, top_low, tower_front, tower_side, tower_top)

    def make_house_solid(self, scale=0.72):
        o, ex, ey, ez = self.iso_axes(ORIGIN, scale)
        base_top = self.iso_poly([(0,0,1.2),(3,0,1.2),(3,2,1.2),(0,2,1.2)], o, ex, ey, ez, VERY_LIGHT)
        front = self.iso_poly([(0,0,0),(3,0,0),(3,0,1.2),(0,0,1.2)], o, ex, ey, ez, "#E0E0E0")
        right = self.iso_poly([(3,0,0),(3,2,0),(3,2,1.2),(3,0,1.2)], o, ex, ey, ez, "#D1D1D1")
        roof_front = self.iso_poly([(0,0,1.2),(3,0,1.2),(2.1,0,2.15),(0.9,0,2.15)], o, ex, ey, ez, "#F2F2F2")
        roof_top = self.iso_poly([(0.9,0,2.15),(2.1,0,2.15),(2.1,2,2.15),(0.9,2,2.15)], o, ex, ey, ez, WHITE)
        roof_side = self.iso_poly([(3,0,1.2),(3,2,1.2),(2.1,2,2.15),(2.1,0,2.15)], o, ex, ey, ez, "#D9D9D9")
        return VGroup(front, right, base_top, roof_front, roof_side, roof_top)

    def view_front_step(self, scale=1.0):
        outer = Polygon([-1.7,-1,0],[1.7,-1,0],[1.7,0,0],[0.25,0,0],[0.25,1.05,0],[-1.7,1.05,0],
                        stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
        return outer.scale(scale)

    def view_top_step(self, scale=1.0):
        outer = Rectangle(width=3.4, height=2.0, stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
        inner = Rectangle(width=1.4, height=1.05, stroke_color=BLACK_LINE, stroke_width=2.0, fill_opacity=0)
        inner.align_to(outer, LEFT).align_to(outer, UP)
        return VGroup(outer, inner).scale(scale)

    def view_right_step(self, scale=1.0):
        outer = Polygon([-1.2,-1,0],[1.2,-1,0],[1.2,0,0],[0.2,0,0],[0.2,1.05,0],[-1.2,1.05,0],
                        stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
        return outer.scale(scale)

    def view_house_front(self, scale=1.0):
        p = Polygon([-1.7,-1,0],[1.7,-1,0],[1.7,0.15,0],[0.75,1.15,0],[-0.75,1.15,0],[-1.7,0.15,0],
                    stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
        return p.scale(scale)

    def view_house_top(self, scale=1.0):
        return Rectangle(width=3.4, height=2.0, stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1).scale(scale)

    def view_house_right(self, scale=1.0):
        return Rectangle(width=2.0, height=1.55, stroke_color=BLACK_LINE, stroke_width=2.4, fill_color=WHITE, fill_opacity=1).scale(scale)

    def label_under(self, mob, text, size=21):
        return self.txt(text, size, BOLD).next_to(mob, DOWN, buff=0.13)

    def projection_panel(self, system="A", scale=1.0):
        """Canonical six-view placement around a central front view."""
        front = self.view_front_step(0.48 * scale)
        top = self.view_top_step(0.48 * scale)
        bottom = self.view_top_step(0.48 * scale)
        left = self.view_right_step(0.48 * scale)
        right = self.view_right_step(0.48 * scale)
        rear = self.view_front_step(0.48 * scale)
        center = ORIGIN
        front.move_to(center)
        if system == "A":
            top.move_to(center + UP * 2.05)
            bottom.move_to(center + DOWN * 2.05)
            left.move_to(center + LEFT * 3.15)
            right.move_to(center + RIGHT * 3.15)
            rear.move_to(center + RIGHT * 5.75)
        else:
            top.move_to(center + DOWN * 2.05)
            bottom.move_to(center + UP * 2.05)
            left.move_to(center + RIGHT * 3.15)
            right.move_to(center + LEFT * 3.15)
            rear.move_to(center + RIGHT * 5.75)
        labels = VGroup(
            self.label_under(front, "FRONT", 18),
            self.label_under(top, "TOP", 18),
            self.label_under(bottom, "BOTTOM", 18),
            self.label_under(left, "LEFT", 18),
            self.label_under(right, "RIGHT", 18),
            self.label_under(rear, "REAR", 18),
        )
        return VGroup(front, top, bottom, left, right, rear, labels)

    def first_third_symbol(self, third=True, scale=1.0):
        """Simplified frustum + end view symbol."""
        frustum = Polygon([-1.30,-0.55,0],[0.75,-0.32,0],[0.75,0.32,0],[-1.30,0.55,0],
                          stroke_color=BLACK_LINE, stroke_width=2.3, fill_color=WHITE, fill_opacity=1)
        axis = DashedLine([-1.5,0,0],[0.95,0,0], color=MID_GRAY, dash_length=0.08, stroke_width=1.4)
        circ = Circle(radius=0.58, stroke_color=BLACK_LINE, stroke_width=2.3, fill_color=WHITE, fill_opacity=1)
        circ.add(Circle(radius=0.28, stroke_color=BLACK_LINE, stroke_width=1.7))
        if third:
            circ.next_to(frustum, LEFT, buff=0.55)
        else:
            circ.next_to(frustum, RIGHT, buff=0.55)
        return VGroup(frustum, axis, circ).scale(scale)

    def orthographic_triplet(self, front, top, right, system="A", gap=2.3):
        front.move_to(ORIGIN)
        if system == "A":
            top.move_to(UP * gap)
            right.move_to(RIGHT * 3.2)
        else:
            top.move_to(DOWN * gap)
            right.move_to(LEFT * 3.2)
        labels = VGroup(
            self.label_under(front, "FRONT", 19),
            self.label_under(top, "TOP", 19),
            self.label_under(right, "RIGHT", 19),
        )
        return VGroup(front, top, right, labels)

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.agenda()
        self.dihedral_system()
        self.standards()
        self.symbols()
        self.projection_systems()
        self.types_of_views()
        self.iso_a_rules()
        self.iso_a_example_1()
        self.iso_a_example_2()
        self.iso_e_rules()
        self.iso_e_example_1()
        self.iso_e_example_2()
        self.comparison()
        self.references()
        self.closing()

    def opening(self):
        title = self.txt("DIBUJO TECNICO Y CAD", 46, BOLD)
        topic = self.txt("Cotas y norma basicas (ANSI)", 34, BOLD)
        sub = self.txt("Sistema diedrico y proyecciones ISO A / ISO E", 26, color=DARK_GRAY)
        line = Line(LEFT * 4.7, RIGHT * 4.7, color=BLACK_LINE, stroke_width=2)
        course = VGroup(
            self.txt("360204003-3", 24, BOLD),
            self.txt("Lunes - Miercoles 12:00AM - 2:00PM", 21),
            self.txt("Juan Diego Perez Alvarez · Ingenieria Mecatronica · Medellin 2024", 20),
        ).arrange(DOWN, buff=0.11)
        block = VGroup(title, topic, sub, line, course).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        frame = RoundedRectangle(width=12.8, height=5.6, corner_radius=0.18, stroke_color=BLACK_LINE,
                                 stroke_width=2.0, fill_color=WHITE, fill_opacity=1)
        self.play(Create(frame), run_time=RUN)
        self.play(LaggedStart(FadeIn(title, shift=UP*0.15), FadeIn(topic), FadeIn(sub), Create(line), FadeIn(course), lag_ratio=0.16), run_time=RUN_SLOW*2)
        self.wait(PAUSE_W)
        self.play(FadeOut(block), FadeOut(frame), run_time=RUN)

    def agenda(self):
        self.set_header("ROADMAP", "We will move from the dihedral idea to view placement, then solve ISO A and ISO E visual examples.")
        items = [
            ("1", "THEORY", "Dihedral system · standards · symbols"),
            ("2", "ISO A", "Third-angle / American arrangement"),
            ("3", "ISO E", "First-angle / European arrangement"),
            ("4", "REFERENCES", "Source-deck bibliography and closing"),
        ]
        cards = VGroup()
        for n, t, d in items:
            c = self.card(f"{n}  {t}", [d], width=6.1, title_size=27, body_size=21)
            cards.add(c)
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.45,0.45)).move_to(DOWN*0.35)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.12) for c in cards], lag_ratio=0.13), run_time=RUN_SLOW*1.6)
        self.wait(PAUSE_E)
        self.clear_content()

    def dihedral_system(self):
        self.set_header("SISTEMA DIEDRICO", "Orthographic drawing begins by projecting one object onto mutually perpendicular planes and then unfolding those planes.")
        solid = self.make_step_solid(0.63).move_to(LEFT*3.8 + DOWN*0.55)
        vplane = Rectangle(width=4.4, height=4.8, stroke_color=MID_GRAY, stroke_width=1.8, fill_color=VERY_LIGHT, fill_opacity=0.35).move_to(RIGHT*2.4 + UP*0.35)
        hplane = Polygon([-2.2,-1.25,0],[2.2,-1.25,0],[3.0,0.0,0],[-1.4,0.0,0], stroke_color=MID_GRAY, stroke_width=1.8, fill_color=VERY_LIGHT, fill_opacity=0.42).move_to(RIGHT*2.4 + DOWN*1.4)
        front = self.view_front_step(0.55).move_to(vplane.get_center())
        top = self.view_top_step(0.52).move_to(RIGHT*2.4 + DOWN*1.25)
        arr1 = Arrow(solid.get_right()+RIGHT*0.1, front.get_left()+LEFT*0.1, buff=0.05, stroke_width=2.0, color=BLACK_LINE)
        self.play(FadeIn(solid, shift=UP*0.15), run_time=RUN)
        self.wait(PAUSE_R)
        self.play(Create(vplane), Create(hplane), run_time=RUN)
        self.play(GrowArrow(arr1), FadeIn(front), FadeIn(top), run_time=RUN_SLOW)
        self.wait(PAUSE_E)
        label1 = self.chip("PROJECT", 3.0, 24).move_to(UP*2.25 + RIGHT*2.45)
        label2 = self.chip("UNFOLD PLANES", 3.6, 23).move_to(RIGHT*2.45 + DOWN*2.85)
        self.play(FadeIn(label1), FadeIn(label2), run_time=RUN)
        # unfold visual: views slide into common sheet
        front_t = front.copy().move_to(RIGHT*2.3 + DOWN*0.3)
        top_t = top.copy().move_to(RIGHT*2.3 + UP*2.05)
        self.play(TransformFromCopy(front, front_t), TransformFromCopy(top, top_t), run_time=RUN_FOLD)
        self.wait(PAUSE_W)
        self.clear_content()

    def standards(self):
        self.set_header("SISTEMAS DE REPRESENTACION SEGUN NORMA", "The source deck distinguishes ISO(A) / third quadrant and ISO(E) / first quadrant, and states the Colombian NTC1777 relation to ISO(A).")
        cross = VGroup(
            Line(LEFT*2.5, RIGHT*2.5, color=BLACK_LINE, stroke_width=2),
            Line(DOWN*2.4, UP*2.4, color=BLACK_LINE, stroke_width=2),
        ).move_to(LEFT*3.8 + DOWN*0.4)
        qlabs = VGroup(
            self.txt("1st", 22, BOLD).move_to(LEFT*2.75 + UP*1.4),
            self.txt("2nd", 22, BOLD).move_to(LEFT*4.95 + UP*1.4),
            self.txt("3rd", 22, BOLD).move_to(LEFT*4.95 + DOWN*1.5),
            self.txt("4th", 22, BOLD).move_to(LEFT*2.75 + DOWN*1.5),
        )
        panel = VGroup(cross, qlabs)
        iso_a = self.card("ISO(A) / AMERICAN", ["Third quadrant", "Third-angle projection"], width=5.7)
        iso_e = self.card("ISO(E) / EUROPEAN", ["First quadrant", "First-angle projection"], width=5.7)
        col = self.card("COLOMBIA", ["Source deck: NTC1777", "derived from ISO(A)"], width=5.7)
        stack = VGroup(iso_a, iso_e, col).arrange(DOWN, buff=0.26).move_to(RIGHT*3.4 + DOWN*0.42)
        self.play(Create(cross), FadeIn(qlabs), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT*0.12) for x in stack], lag_ratio=0.14), run_time=RUN_SLOW*1.6)
        self.wait(PAUSE_W)
        self.clear_content()

    def symbols(self):
        self.set_header("SIMBOLOGIA", "The frustum-and-circle symbol identifies whether a drawing uses first-angle or third-angle projection.")
        third = self.first_third_symbol(True, 1.1).move_to(LEFT*3.7 + DOWN*0.25)
        first = self.first_third_symbol(False, 1.1).move_to(RIGHT*3.7 + DOWN*0.25)
        t1 = self.chip("AMERICAN · THIRD ANGLE", 5.3, 24).next_to(third, UP, buff=0.55)
        t2 = self.chip("EUROPEAN · FIRST ANGLE", 5.3, 24).next_to(first, UP, buff=0.55)
        hint1 = self.txt("circle opposite the frustum", 20, color=DARK_GRAY).next_to(third, DOWN, buff=0.45)
        hint2 = self.txt("circle switches sides", 20, color=DARK_GRAY).next_to(first, DOWN, buff=0.45)
        self.play(FadeIn(t1), FadeIn(t2), run_time=RUN)
        self.play(Create(third), Create(first), run_time=RUN_SLOW)
        self.play(FadeIn(hint1), FadeIn(hint2), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def projection_systems(self):
        self.set_header("SISTEMAS DE PROYECCION", "The object does not change; the standard changes where the resulting orthographic views are placed on the sheet.")
        solid = self.make_step_solid(0.48).move_to(ORIGIN + DOWN*0.65)
        rays = VGroup()
        for direction in (UP, DOWN, LEFT, RIGHT):
            rays.add(Arrow(solid.get_center(), solid.get_center()+direction*2.3, buff=0.55, color=MID_GRAY, stroke_width=1.8))
        a = self.chip("ISO A", 2.8, 26).move_to(LEFT*4.7 + UP*1.9)
        e = self.chip("ISO E", 2.8, 26).move_to(RIGHT*4.7 + UP*1.9)
        note_a = self.card("THIRD ANGLE", ["View goes to the same side", "from which it is observed"], width=4.8, body_size=20).move_to(LEFT*4.6 + DOWN*1.0)
        note_e = self.card("FIRST ANGLE", ["View appears on the opposite side", "after the projection plane unfolds"], width=4.8, body_size=20).move_to(RIGHT*4.6 + DOWN*1.0)
        self.play(FadeIn(solid), run_time=RUN)
        self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.10), run_time=RUN_SLOW)
        self.play(FadeIn(a), FadeIn(e), FadeIn(note_a), FadeIn(note_e), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def types_of_views(self):
        self.set_header("TIPOS DE VISTA", "Six principal orthographic directions are used around the object: front, top, bottom, left, right and rear.")
        solid = self.make_step_solid(0.43).move_to(ORIGIN + DOWN*0.55)
        dirs = [
            (UP*2.2, "TOP"), (DOWN*2.2, "BOTTOM"), (LEFT*2.8, "LEFT"),
            (RIGHT*2.8, "RIGHT"), (UP*0.3+LEFT*4.5, "FRONT"), (UP*0.3+RIGHT*4.5, "REAR"),
        ]
        arrows, labels = VGroup(), VGroup()
        for vec, lab in dirs:
            arr = Arrow(solid.get_center()+vec, solid.get_center(), buff=0.55, color=BLACK_LINE, stroke_width=1.8, max_tip_length_to_length_ratio=0.10)
            labels.add(self.chip(lab, 2.0, 20).move_to(solid.get_center()+vec))
            arrows.add(arr)
        self.play(FadeIn(solid), run_time=RUN)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.10), LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.10), run_time=RUN_SLOW*1.8)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_a_rules(self):
        self.set_header("ISO A · THIRD-ANGLE / AMERICAN", "With the front view as reference, each neighboring view is placed on the same side from which it is observed.")
        panel = self.projection_panel("A", 0.78).move_to(LEFT*2.25 + DOWN*0.25)
        rules = self.card("PLACEMENT RULES", [
            "Top view     -> above",
            "Bottom view  -> below",
            "Left view    -> left",
            "Right view   -> right",
            "Rear view    -> left or right",
        ], width=5.3, body_size=22).move_to(RIGHT*4.9 + DOWN*0.2)
        self.play(FadeIn(panel[0]), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(m, shift=0.08*UP) for m in panel[1:6]], lag_ratio=0.12), run_time=RUN_SLOW*1.8)
        self.play(FadeIn(panel[6]), FadeIn(rules), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_a_example_1(self):
        self.set_header("EJEMPLO ISO A · 1", "Project an isometric house-like solid into front, top and right views using third-angle placement.")
        solid = self.make_house_solid(0.55).move_to(LEFT*4.7 + DOWN*0.45)
        front = self.view_house_front(0.55)
        top = self.view_house_top(0.55)
        right = self.view_house_right(0.55)
        trip = self.orthographic_triplet(front, top, right, "A", gap=2.1).move_to(RIGHT*2.6 + DOWN*0.35)
        arrows = VGroup(
            Arrow(solid.get_right()+RIGHT*0.15, trip[0].get_left()+LEFT*0.15, buff=0.05, color=MID_GRAY, stroke_width=1.8),
            Arrow(solid.get_top()+UP*0.15, trip[1].get_left()+LEFT*0.25, buff=0.05, color=MID_GRAY, stroke_width=1.8),
        )
        self.play(FadeIn(solid), run_time=RUN)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.20), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[0]), TransformFromCopy(solid, trip[1]), TransformFromCopy(solid, trip[2]), run_time=RUN_FOLD)
        self.play(FadeIn(trip[3]), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_a_example_2(self):
        self.set_header("EJEMPLO ISO A · 2", "A stepped solid produces different silhouettes in each direction; third-angle placement keeps orientation intuitive.")
        solid = self.make_step_solid(0.62).move_to(LEFT*4.4 + DOWN*0.45)
        front = self.view_front_step(0.58)
        top = self.view_top_step(0.58)
        right = self.view_right_step(0.58)
        trip = self.orthographic_triplet(front, top, right, "A", gap=2.1).move_to(RIGHT*2.7 + DOWN*0.35)
        method = VGroup(
            self.chip("1 · choose FRONT", 3.7, 21),
            self.chip("2 · project edges", 3.7, 21),
            self.chip("3 · place views", 3.7, 21),
        ).arrange(DOWN, buff=0.18).move_to(LEFT*4.6 + DOWN*2.55)
        self.play(FadeIn(solid, shift=UP*0.1), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT*0.08) for x in method], lag_ratio=0.12), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[0]), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[1]), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[2]), FadeIn(trip[3]), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_rules(self):
        self.set_header("ISO E · FIRST-ANGLE / EUROPEAN", "With the front view as reference, the neighboring views appear on the opposite side after the projection planes unfold.")
        panel = self.projection_panel("E", 0.78).move_to(LEFT*2.25 + DOWN*0.25)
        rules = self.card("PLACEMENT RULES", [
            "Top view     -> below",
            "Bottom view  -> above",
            "Left view    -> right",
            "Right view   -> left",
            "Rear view    -> left or right",
        ], width=5.3, body_size=22).move_to(RIGHT*4.9 + DOWN*0.2)
        self.play(FadeIn(panel[0]), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(m, shift=0.08*UP) for m in panel[1:6]], lag_ratio=0.12), run_time=RUN_SLOW*1.8)
        self.play(FadeIn(panel[6]), FadeIn(rules), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_example_1(self):
        self.set_header("EJEMPLO ISO E · 1", "Use the same object, but place top and side views according to first-angle projection.")
        solid = self.make_step_solid(0.62).move_to(LEFT*4.4 + DOWN*0.5)
        front = self.view_front_step(0.58)
        top = self.view_top_step(0.58)
        right = self.view_right_step(0.58)
        trip = self.orthographic_triplet(front, top, right, "E", gap=2.0).move_to(RIGHT*2.7 + DOWN*0.35)
        cue = self.card("FIRST-ANGLE CUE", ["TOP goes below FRONT", "RIGHT view goes to the left"], width=4.7, body_size=21).move_to(LEFT*4.6 + DOWN*2.45)
        self.play(FadeIn(solid), FadeIn(cue), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[0]), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[1]), run_time=RUN)
        self.play(TransformFromCopy(solid, trip[2]), FadeIn(trip[3]), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def iso_e_example_2(self):
        self.set_header("EJEMPLO ISO E · 2", "The geometry is unchanged. Only the view-placement convention changes, so always identify the projection symbol first.")
        solid = self.make_house_solid(0.56).move_to(LEFT*4.4 + DOWN*0.5)
        front = self.view_house_front(0.56)
        top = self.view_house_top(0.56)
        right = self.view_house_right(0.56)
        trip = self.orthographic_triplet(front, top, right, "E", gap=2.0).move_to(RIGHT*2.7 + DOWN*0.35)
        sym = self.first_third_symbol(False, 0.70).move_to(LEFT*4.6 + DOWN*2.55)
        self.play(FadeIn(solid), FadeIn(sym), run_time=RUN)
        self.play(LaggedStart(TransformFromCopy(solid, trip[0]), TransformFromCopy(solid, trip[1]), TransformFromCopy(solid, trip[2]), lag_ratio=0.20), run_time=RUN_FOLD)
        self.play(FadeIn(trip[3]), run_time=RUN)
        self.wait(PAUSE_W)
        self.clear_content()

    def comparison(self):
        self.set_header("ISO A vs ISO E · FINAL COMPARISON", "Read the symbol first, keep the same FRONT view, then place TOP/LEFT/RIGHT according to the selected convention.")
        a_sym = self.first_third_symbol(True, 0.68)
        e_sym = self.first_third_symbol(False, 0.68)
        a_card = self.card("ISO A · THIRD ANGLE", ["TOP above FRONT", "LEFT left", "RIGHT right"], width=5.6, body_size=21)
        e_card = self.card("ISO E · FIRST ANGLE", ["TOP below FRONT", "LEFT right", "RIGHT left"], width=5.6, body_size=21)
        ga = VGroup(a_sym, a_card).arrange(DOWN, buff=0.36).move_to(LEFT*3.5 + DOWN*0.25)
        ge = VGroup(e_sym, e_card).arrange(DOWN, buff=0.36).move_to(RIGHT*3.5 + DOWN*0.25)
        center_rule = self.chip("SAME OBJECT · DIFFERENT VIEW PLACEMENT", 6.4, 23).move_to(DOWN*3.05)
        self.play(FadeIn(ga, shift=RIGHT*0.12), FadeIn(ge, shift=LEFT*0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_R)
        self.play(FadeIn(center_rule), run_time=RUN)
        self.wait(PAUSE_SUM)
        self.clear_content()

    def references(self):
        self.set_header("REFERENCIAS", "The source deck closes with three technical-drawing / metrology references; the titles are retained here.")
        refs = VGroup(
            self.card("REFERENCE 1", ["Dibujo y diseno en ingenieria"], width=4.2, height=1.75, body_size=21),
            self.card("REFERENCE 2", ["Metrologia"], width=4.2, height=1.75, body_size=21),
            self.card("REFERENCE 3", ["Dibujo de ingenieria"], width=4.2, height=1.75, body_size=21),
        ).arrange(RIGHT, buff=0.38).move_to(DOWN*0.4)
        self.play(LaggedStart(*[FadeIn(r, shift=UP*0.12) for r in refs], lag_ratio=0.16), run_time=RUN_SLOW*1.6)
        self.wait(PAUSE_W)
        self.clear_content()

    def closing(self):
        self.close_all()
        title = self.txt("MUCHAS GRACIAS", 54, BOLD)
        line = Line(LEFT*3.5, RIGHT*3.5, color=BLACK_LINE, stroke_width=2)
        take = self.txt("Identify the symbol · choose the front view · project · place · verify", 25, color=DARK_GRAY)
        course = self.txt("Dibujo Tecnico y CAD · Clase 6", 22, BOLD)
        group = VGroup(title, line, take, course).arrange(DOWN, buff=0.28)
        self.play(FadeIn(title, shift=UP*0.16), run_time=RUN)
        self.play(Create(line), FadeIn(take), FadeIn(course), run_time=RUN)
        self.wait(PAUSE_SUM)


# Preview: manim -pql Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V1_SENIOR.py TechnicalDrawingClass6ISO --disable_caching
# Final:   manim -pqh Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V1_SENIOR.py TechnicalDrawingClass6ISO --disable_caching
