#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V3 senior redesign — sistema diédrico, primer/tercer diedro y contexto NTC.

Design intent
-------------
This version intentionally replaces the V2 card-heavy look with a much more
visual engineering narrative. One mechanical part is reused throughout the
lesson, projection geometry is animated explicitly, typography is shorter and
larger, and every section is built around a single visual idea.

Target: Manim Community Edition 0.20.x, Cairo renderer, 1920x1080, 30 fps.
"""
from __future__ import annotations

import os
import math
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#F7F9FC"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BG = "#F7F9FC"
WHITE = "#FFFFFF"
NAVY = "#0C2238"
INK = "#182430"
DARK = "#334155"
MID = "#64748B"
LIGHT = "#D7E0EA"
GRID = "#E8EEF4"
BLUE = "#1769AA"
CYAN = "#2AA7D8"
TEAL = "#168C82"
ORANGE = "#E78A18"
GREEN = "#2E8B57"
RED = "#C65353"
PALE_BLUE = "#EAF4FB"
PALE_TEAL = "#E8F6F3"
PALE_ORANGE = "#FFF4E5"
FACE_FRONT = "#EAF0F6"
FACE_SIDE = "#CBD8E4"
FACE_TOP = "#FFFFFF"
FACE_DARK = "#AFC0CF"

RT_FAST = 0.70
RT = 1.10
RT_SLOW = 1.55
RT_HERO = 2.10
PAUSE_BEAT = 1.0
PAUSE_READ = 2.3
PAUSE_EXPLAIN = 3.8
PAUSE_LONG = 5.2
PAUSE_CHALLENGE = 7.0


class TimedScene(Scene):
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)


class DiedricISOProjectionV3Senior(TimedScene):
    def text(self, s: str, size=30, weight=NORMAL, color=INK, **kwargs):
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.92, **kwargs)

    def fit(self, mob: Mobject, max_w=14.7, max_h=7.6):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def clear_stage(self, run_time=0.70):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def section_header(self, n: int, title: str, subtitle: str = ""):
        bar = Rectangle(width=16, height=0.82, stroke_width=0, fill_color=NAVY, fill_opacity=1).to_edge(UP, buff=0)
        badge = RoundedRectangle(width=0.58, height=0.46, corner_radius=0.10, stroke_color=CYAN, stroke_width=2, fill_color=NAVY, fill_opacity=1)
        badge_num = self.text(str(n), 20, BOLD, CYAN).move_to(badge)
        ttl = self.text(title, 31, BOLD, WHITE)
        ttl_group = VGroup(VGroup(badge, badge_num), ttl).arrange(RIGHT, buff=0.20)
        ttl_group.to_edge(LEFT, buff=0.45).to_edge(UP, buff=0.16)
        if subtitle:
            sub = self.text(subtitle, 20, NORMAL, DARK)
            self.fit(sub, 14.8, 0.52)
            sub.to_edge(LEFT, buff=0.48).next_to(bar, DOWN, buff=0.12)
            return VGroup(bar, ttl_group, sub)
        return VGroup(bar, ttl_group)

    def mini_label(self, text: str, color=BLUE, size=18, fill=WHITE):
        t = self.text(text, size, BOLD, color)
        box = RoundedRectangle(width=t.width + 0.45, height=t.height + 0.24, corner_radius=0.12, stroke_color=color, stroke_width=1.6, fill_color=fill, fill_opacity=1)
        t.move_to(box)
        return VGroup(box, t)

    def emphasis(self, text: str, color=BLUE, size=32, width=6.5):
        t = self.text(text, size, BOLD, color)
        self.fit(t, width - 0.7, 0.9)
        box = RoundedRectangle(width=width, height=max(1.05, t.height + 0.45), corner_radius=0.14, stroke_color=color, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        t.move_to(box)
        return VGroup(box, t)

    def blueprint_grid(self, width=7.2, height=5.7, spacing=0.42):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=LIGHT, stroke_width=1.4, fill_color=WHITE, fill_opacity=1)
        lines = VGroup()
        x0 = -width/2 + spacing
        while x0 < width/2:
            lines.add(Line([x0, -height/2, 0], [x0, height/2, 0], color=GRID, stroke_width=0.8))
            x0 += spacing
        y0 = -height/2 + spacing
        while y0 < height/2:
            lines.add(Line([-width/2, y0, 0], [width/2, y0, 0], color=GRID, stroke_width=0.8))
            y0 += spacing
        return VGroup(box, lines)

    def iso_pt(self, x, y, z, s=0.86):
        return s * (x * RIGHT + y * (0.56 * RIGHT + 0.35 * UP) + z * UP)

    def iso_box(self, x0, x1, y0, y1, z0, z1, s=0.86, edge=INK):
        p = lambda x, y, z: self.iso_pt(x, y, z, s)
        front = Polygon(p(x0, y0, z0), p(x1, y0, z0), p(x1, y0, z1), p(x0, y0, z1), stroke_color=edge, stroke_width=2.4, fill_color=FACE_FRONT, fill_opacity=1)
        side = Polygon(p(x1, y0, z0), p(x1, y1, z0), p(x1, y1, z1), p(x1, y0, z1), stroke_color=edge, stroke_width=2.4, fill_color=FACE_SIDE, fill_opacity=1)
        top = Polygon(p(x0, y0, z1), p(x1, y0, z1), p(x1, y1, z1), p(x0, y1, z1), stroke_color=edge, stroke_width=2.4, fill_color=FACE_TOP, fill_opacity=1)
        return VGroup(front, side, top)

    def mechanical_part(self, s=0.86, include_shadow=True):
        boxes = VGroup(
            self.iso_box(0.0, 5.0, 0.0, 3.0, 0.0, 0.55, s),
            self.iso_box(0.60, 1.70, 0.65, 1.85, 0.55, 1.15, s),
            self.iso_box(2.30, 3.90, 0.35, 2.65, 0.55, 1.55, s),
            self.iso_box(3.90, 5.00, 0.55, 2.45, 0.55, 3.10, s),
        )
        tower_hole = Circle(radius=0.37*s, stroke_color=BLUE, stroke_width=3.0, fill_color=FACE_FRONT, fill_opacity=1).move_to(self.iso_pt(4.45, 0.0, 2.08, s))
        tower_cross = VGroup(
            DashedLine(tower_hole.get_left()+LEFT*0.15, tower_hole.get_right()+RIGHT*0.15, dash_length=0.08, color=MID, stroke_width=1.25),
            DashedLine(tower_hole.get_bottom()+DOWN*0.15, tower_hole.get_top()+UP*0.15, dash_length=0.08, color=MID, stroke_width=1.25),
        )
        boss_center = self.iso_pt(1.15, 1.25, 1.15, s)
        boss_hole = Ellipse(width=0.72*s, height=0.27*s, stroke_color=TEAL, stroke_width=2.6, fill_color=WHITE, fill_opacity=1).rotate(0.32).move_to(boss_center)
        part = VGroup(boxes, tower_hole, tower_cross, boss_hole)
        if include_shadow:
            shadow = part.copy()
            shadow.set_fill(BLACK, opacity=0.08)
            shadow.set_stroke(BLACK, opacity=0.0)
            shadow.shift(RIGHT*0.14 + DOWN*0.12)
            return VGroup(shadow, part)
        return part

    def _scaled_poly(self, pts, scale, color=INK, fill=WHITE, stroke=3.0):
        return Polygon(*[np.array([x, y, 0]) * scale for x, y in pts], stroke_color=color, stroke_width=stroke, fill_color=fill, fill_opacity=1)

    def front_view(self, scale=0.78, color=INK, show_centerlines=True):
        pts = [(-2.50, -1.55), (2.50, -1.55), (2.50, 1.55), (1.40, 1.55), (1.40, 0.00), (-0.20, 0.00), (-0.20, -0.55), (-0.80, -0.55), (-0.80, -0.15), (-1.90, -0.15), (-1.90, -0.55), (-2.50, -0.55)]
        outline = self._scaled_poly(pts, scale, color)
        edges = VGroup(
            Line(np.array([-0.20, -1.55, 0])*scale, np.array([-0.20, 0.00, 0])*scale, color=color, stroke_width=2.0),
            Line(np.array([1.40, -1.55, 0])*scale, np.array([1.40, 1.55, 0])*scale, color=color, stroke_width=2.0),
        )
        hole = Circle(radius=0.33*scale, stroke_color=BLUE, stroke_width=2.6, fill_color=WHITE, fill_opacity=1).move_to(np.array([1.95, 0.50, 0])*scale)
        g = VGroup(outline, edges, hole)
        if show_centerlines:
            h = DashedLine(hole.get_left()+LEFT*0.22, hole.get_right()+RIGHT*0.22, dash_length=0.08, color=MID, stroke_width=1.1)
            v = DashedLine(hole.get_bottom()+DOWN*0.22, hole.get_top()+UP*0.22, dash_length=0.08, color=MID, stroke_width=1.1)
            g.add(h, v)
        return g

    def top_view(self, scale=0.78, color=INK):
        outer = Rectangle(width=5.0*scale, height=3.0*scale, stroke_color=color, stroke_width=3.0, fill_color=WHITE, fill_opacity=1)
        mid = Rectangle(width=1.60*scale, height=2.30*scale, stroke_color=color, stroke_width=2.0, fill_opacity=0).move_to(np.array([0.60, 0.0, 0])*scale)
        tower = Rectangle(width=1.10*scale, height=1.90*scale, stroke_color=color, stroke_width=2.0, fill_opacity=0).move_to(np.array([1.95, 0.0, 0])*scale)
        boss = Rectangle(width=1.10*scale, height=1.20*scale, stroke_color=color, stroke_width=2.0, fill_opacity=0).move_to(np.array([-1.35, -0.10, 0])*scale)
        bore = Circle(radius=0.25*scale, stroke_color=TEAL, stroke_width=2.4, fill_color=WHITE, fill_opacity=1).move_to(boss)
        center = VGroup(
            DashedLine(bore.get_left()+LEFT*0.16, bore.get_right()+RIGHT*0.16, dash_length=0.07, color=MID, stroke_width=1.0),
            DashedLine(bore.get_bottom()+DOWN*0.16, bore.get_top()+UP*0.16, dash_length=0.07, color=MID, stroke_width=1.0),
        )
        return VGroup(outer, mid, tower, boss, bore, center)

    def right_view(self, scale=0.78, color=INK, mirror=False):
        pts = [(-1.50, -1.55), (1.50, -1.55), (1.50, -0.55), (1.15, -0.55), (1.15, 0.00), (0.95, 0.00), (0.95, 1.55), (-0.95, 1.55), (-0.95, 0.00), (-1.15, 0.00), (-1.15, -0.55), (-1.50, -0.55)]
        if mirror:
            pts = [(-x, y) for x, y in pts]
        outline = self._scaled_poly(pts, scale, color)
        e1 = Line(np.array([-1.15, -1.55, 0])*scale, np.array([-1.15, -0.55, 0])*scale, color=color, stroke_width=2.0)
        e2 = Line(np.array([1.15, -1.55, 0])*scale, np.array([1.15, -0.55, 0])*scale, color=color, stroke_width=2.0)
        if mirror:
            e1.flip(axis=UP); e2.flip(axis=UP)
        return VGroup(outline, e1, e2)

    def rear_view(self, scale=0.78, color=INK):
        v = self.front_view(scale, color, show_centerlines=False)
        v.flip(axis=UP)
        if len(v) >= 4:
            v[2].set_stroke(MID, width=1.5, opacity=0.55)
        return v

    def bottom_view(self, scale=0.78, color=INK):
        v = self.top_view(scale, color)
        v.flip(axis=RIGHT)
        v[-2].set_stroke(MID, width=1.5, opacity=0.45)
        v[-1].set_opacity(0.25)
        return v

    def view_panel(self, title: str, view: Mobject, width=4.15, height=2.72, accent=BLUE, subtitle: str | None = None):
        panel = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=LIGHT, stroke_width=1.5, fill_color=WHITE, fill_opacity=1)
        accent_line = Line(panel.get_corner(UL)+RIGHT*0.18, panel.get_corner(UR)+LEFT*0.18, color=accent, stroke_width=4)
        ttl = self.text(title, 21, BOLD, accent).next_to(panel.get_top(), DOWN, buff=0.22)
        view.move_to(panel).shift(DOWN*0.12)
        self.fit(view, width-0.55, height-0.80)
        items = [panel, accent_line, view, ttl]
        if subtitle:
            sub = self.text(subtitle, 14, NORMAL, MID).next_to(panel.get_bottom(), UP, buff=0.14)
            items.append(sub)
        return VGroup(*items)

    def observer(self, label="OBSERVADOR", color=BLUE, scale=1.0):
        outer = Arc(radius=0.52*scale, start_angle=0.08*PI, angle=0.84*PI, color=color, stroke_width=2.6)
        lower = Arc(radius=0.52*scale, start_angle=1.08*PI, angle=0.84*PI, color=color, stroke_width=2.6)
        iris = Circle(radius=0.13*scale, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.15)
        pupil = Dot(radius=0.048*scale, color=color)
        eye = VGroup(outer, lower, iris, pupil)
        lab = self.text(label, 16, BOLD, color).next_to(eye, DOWN, buff=0.10)
        return VGroup(eye, lab)

    def vertical_plane(self, width=3.8, height=4.8, color=BLUE, fill=PALE_BLUE):
        return Polygon(LEFT*1.65+DOWN*2.10, RIGHT*1.65+DOWN*1.55, RIGHT*1.65+UP*2.10, LEFT*1.65+UP*1.55, stroke_color=color, stroke_width=2.3, fill_color=fill, fill_opacity=0.76)

    def horizontal_plane(self, width=5.2, height=2.5, color=TEAL, fill=PALE_TEAL):
        return Polygon(LEFT*2.65+UP*0.28, RIGHT*1.95+UP*0.28, RIGHT*2.65+DOWN*1.18, LEFT*1.95+DOWN*1.18, stroke_color=color, stroke_width=2.3, fill_color=fill, fill_opacity=0.76)

    def ray_fan(self, starts, targets, color=ORANGE):
        rays = VGroup()
        for a, b in zip(starts, targets):
            rays.add(Line(a, b, color=color, stroke_width=2.1).set_stroke(opacity=0.70))
        return rays

    def projection_symbol(self, first_angle=True, scale=1.0):
        fr = Polygon(np.array([-1.10, -0.62, 0]), np.array([-1.10, 0.62, 0]), np.array([0.78, 0.38, 0]), np.array([0.78, -0.38, 0]), stroke_color=INK, stroke_width=3.0, fill_color=WHITE, fill_opacity=1).scale(scale)
        axis = DashedLine(fr.get_left()+LEFT*0.16, fr.get_right()+RIGHT*0.16, dash_length=0.09, color=MID, stroke_width=1.2)
        circ = Circle(radius=0.60*scale, stroke_color=INK, stroke_width=3.0, fill_color=WHITE, fill_opacity=1)
        circ_center = VGroup(Line(circ.get_left(), circ.get_right(), color=MID, stroke_width=1.0), Line(circ.get_bottom(), circ.get_top(), color=MID, stroke_width=1.0))
        circle_group = VGroup(circ, circ_center)
        circle_group.next_to(fr, LEFT if first_angle else RIGHT, buff=0.58)
        return VGroup(fr, axis, circle_group)

    def placement_cross(self, first_angle=True, scale=1.0, compact=False):
        f = self.view_panel("ALZADO", self.front_view(0.42 if compact else 0.50), 3.00 if compact else 3.40, 2.15 if compact else 2.45, BLUE)
        t = self.view_panel("PLANTA", self.top_view(0.42 if compact else 0.50), 3.00 if compact else 3.40, 2.15 if compact else 2.45, TEAL)
        r = self.view_panel("LATERAL D.", self.right_view(0.42 if compact else 0.50), 3.00 if compact else 3.40, 2.15 if compact else 2.45, ORANGE)
        f.move_to(ORIGIN)
        if first_angle:
            t.next_to(f, DOWN, buff=0.28)
            r.next_to(f, LEFT, buff=0.28)
        else:
            t.next_to(f, UP, buff=0.28)
            r.next_to(f, RIGHT, buff=0.28)
        return VGroup(f, t, r)

    def construct(self):
        self.opening()
        self.orthographic_projection()
        self.dihedral_system()
        self.six_views()
        self.first_angle()
        self.third_angle()
        self.compare_methods()
        self.symbols_and_colombia()
        self.challenge()
        self.closing()

    def opening(self):
        kicker = self.text("DIBUJO TÉCNICO · SISTEMA DIÉDRICO", 24, BOLD, BLUE)
        title = self.text("UNA PIEZA 3D → VISTAS 2D", 55, BOLD, NAVY)
        subtitle = self.text("Primer diedro · ISO E   vs   Tercer diedro · ISO A", 29, BOLD, DARK)
        intro = VGroup(kicker, title, subtitle).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        intro.to_edge(UP, buff=0.52).to_edge(LEFT, buff=0.70)
        part = self.mechanical_part(0.92).move_to(DOWN*0.65)
        part.scale(1.03)
        ground = Line(LEFT*5.7, RIGHT*5.7, color=LIGHT, stroke_width=1.7).move_to(DOWN*3.30)
        caption = self.text("MISMA PIEZA · DISTINTAS DIRECCIONES DE OBSERVACIÓN", 23, BOLD, MID).next_to(ground, UP, buff=0.18)
        self.play(FadeIn(kicker, shift=UP*0.10), run_time=RT)
        self.play(Write(title), run_time=RT_HERO)
        self.play(FadeIn(subtitle), run_time=RT)
        self.wait(PAUSE_READ)
        self.play(Create(ground), run_time=RT)
        self.play(LaggedStart(*[DrawBorderThenFill(m) for m in part[1][0]], lag_ratio=0.15), run_time=RT_HERO)
        self.play(FadeIn(part[0]), FadeIn(part[1][1:]), run_time=RT)
        self.play(FadeIn(caption), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def orthographic_projection(self):
        h = self.section_header(1, "PROYECCIÓN ORTOGONAL", "Sin perspectiva: cada vista registra la geometría desde una dirección exacta.")
        self.add(h)
        part = self.mechanical_part(0.82).move_to(LEFT*3.55+DOWN*0.52)
        obs = self.observer("OBSERVADOR", BLUE, 1.05).move_to(LEFT*6.55+DOWN*0.40)
        plane = self.vertical_plane().move_to(RIGHT*1.05+DOWN*0.42)
        plane_lab = self.mini_label("PLANO DE PROYECCIÓN", BLUE, 17, PALE_BLUE).move_to(RIGHT*1.00+UP*2.15)
        self.play(FadeIn(obs), DrawBorderThenFill(part[1]), FadeIn(part[0]), run_time=RT_HERO)
        self.play(FadeIn(plane), FadeIn(plane_lab), run_time=RT)
        self.wait(PAUSE_READ)
        target_center = plane.get_center()+RIGHT*0.10
        starts = [part[1].get_corner(UL), part[1].get_corner(UR), part[1].get_corner(DL), part[1].get_corner(DR)]
        targets = [target_center+LEFT*0.95+UP*1.32, target_center+RIGHT*0.95+UP*1.08, target_center+LEFT*0.95+DOWN*1.08, target_center+RIGHT*0.95+DOWN*1.32]
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
        key = self.emphasis("1 dirección → 1 vista", GREEN, 29, 4.5).to_edge(DOWN, buff=0.25).shift(RIGHT*3.8)
        self.play(FadeIn(key), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def dihedral_system(self):
        h = self.section_header(2, "EL SISTEMA DIÉDRICO", "Plano vertical + plano horizontal. Después se abaten para formar una sola lámina.")
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
        pv_targets = [front_trace.get_corner(UL), front_trace.get_corner(UR), front_trace.get_corner(DL), front_trace.get_corner(DR)]
        starts = [part.get_corner(UL), part.get_corner(UR), part.get_corner(DL), part.get_corner(DR)]
        pv_rays = self.ray_fan(starts, pv_targets, ORANGE)
        self.play(LaggedStart(*[Create(r) for r in pv_rays], lag_ratio=0.11), run_time=RT_SLOW)
        self.play(Create(front_trace), run_time=RT_SLOW)
        self.wait(PAUSE_READ)
        top_trace = self.top_view(0.28, TEAL).move_to(LEFT*0.85+DOWN*2.00)
        ph_targets = [top_trace.get_corner(UL), top_trace.get_corner(UR), top_trace.get_corner(DL), top_trace.get_corner(DR)]
        ph_rays = self.ray_fan(starts, ph_targets, ORANGE)
        self.play(LaggedStart(*[Create(r) for r in ph_rays], lag_ratio=0.11), run_time=RT_SLOW)
        self.play(Create(top_trace), run_time=RT_SLOW)
        self.wait(PAUSE_EXPLAIN)
        sheet = self.blueprint_grid(6.05, 5.55).to_edge(RIGHT, buff=0.45).shift(DOWN*0.20)
        sheet_title = self.mini_label("ABATIMIENTO → LÁMINA 2D", NAVY, 18).next_to(sheet, UP, buff=-0.18)
        f2 = self.front_view(0.50).move_to(sheet.get_center()+UP*1.05)
        t2 = self.top_view(0.50).move_to(sheet.get_center()+DOWN*1.55)
        div = Line(sheet.get_left()+RIGHT*0.35, sheet.get_right()+LEFT*0.35, color=LIGHT, stroke_width=1.4).move_to(sheet.get_center()+DOWN*0.12)
        self.play(FadeOut(pv_rays), FadeOut(ph_rays), FadeOut(part), run_time=RT)
        self.play(FadeIn(sheet), FadeIn(sheet_title), Create(div), run_time=RT_SLOW)
        self.play(TransformFromCopy(front_trace, f2), run_time=RT_SLOW)
        self.play(TransformFromCopy(top_trace, t2), run_time=RT_SLOW)
        abate = Arrow(LEFT*0.45+DOWN*0.65, RIGHT*1.55+DOWN*1.45, color=TEAL, stroke_width=3.0)
        note = self.text("PH se abate 90°", 22, BOLD, TEAL).next_to(abate, UP, buff=0.10)
        self.play(GrowArrow(abate), FadeIn(note), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def six_views(self):
        h = self.section_header(3, "SEIS VISTAS PRINCIPALES", "El objeto no cambia. Cambia la dirección desde la que lo observamos.")
        self.add(h)
        part = self.mechanical_part(0.68).move_to(DOWN*0.55)
        ring = Circle(radius=3.00, stroke_color=LIGHT, stroke_width=1.7).move_to(part)
        labels = [("ALZADO", LEFT*5.0+DOWN*0.50, BLUE), ("LATERAL D.", RIGHT*5.0+DOWN*0.50, ORANGE), ("PLANTA", UP*2.55, TEAL), ("LATERAL I.", LEFT*4.0+UP*2.05, GREEN), ("POSTERIOR", RIGHT*4.0+UP*2.05, RED), ("INFERIOR", DOWN*3.25, MID)]
        self.play(FadeIn(ring), DrawBorderThenFill(part[1]), FadeIn(part[0]), run_time=RT_HERO)
        self.wait(PAUSE_READ)
        obs_group = VGroup()
        for name, pos, col in labels:
            obs = self.observer(name, col, 0.68).move_to(pos)
            arrow = Arrow(obs.get_center(), part.get_center(), buff=0.56, color=col, stroke_width=2.6, max_tip_length_to_length_ratio=0.10)
            obs_group.add(obs, arrow)
            self.play(FadeIn(obs), GrowArrow(arrow), run_time=RT_FAST)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(part), FadeOut(ring), FadeOut(obs_group), run_time=RT)
        panels = [self.view_panel("ALZADO", self.front_view(0.50), 4.25, 2.66, BLUE), self.view_panel("PLANTA", self.top_view(0.50), 4.25, 2.66, TEAL), self.view_panel("LATERAL DERECHO", self.right_view(0.50), 4.25, 2.66, ORANGE), self.view_panel("LATERAL IZQUIERDO", self.right_view(0.50, mirror=True), 4.25, 2.66, GREEN), self.view_panel("POSTERIOR", self.rear_view(0.50), 4.25, 2.66, RED), self.view_panel("INFERIOR", self.bottom_view(0.50), 4.25, 2.66, MID)]
        grid = VGroup(*panels).arrange_in_grid(rows=2, cols=3, buff=(0.30, 0.30)).shift(DOWN*0.50)
        self.fit(grid, 13.5, 5.65)
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.12) for p in panels], lag_ratio=0.12), run_time=RT_HERO*1.35)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def first_angle(self):
        h = self.section_header(4, "PRIMER DIEDRO · FIRST-ANGLE · ISO E", "Orden físico: observador → objeto → plano. En la lámina, las vistas quedan al lado opuesto.")
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
        self.play(FadeOut(obs), FadeOut(obj), FadeOut(plane), FadeOut(a1), FadeOut(a2), FadeOut(one), FadeOut(two), FadeOut(three), run_time=RT)
        layout = self.placement_cross(first_angle=True, compact=False).shift(RIGHT*0.75+DOWN*0.05)
        side_note = VGroup(self.text("PRIMER DIEDRO", 29, BOLD, BLUE), self.text("PLANTA ↓", 25, BOLD, TEAL), self.text("LATERAL D. ←", 25, BOLD, ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.75).shift(DOWN*0.20)
        self.play(FadeIn(side_note[0]), run_time=RT)
        self.play(FadeIn(layout[0]), run_time=RT)
        self.play(FadeIn(side_note[1]), FadeIn(layout[1], shift=UP*0.20), run_time=RT_SLOW)
        self.play(FadeIn(side_note[2]), FadeIn(layout[2], shift=RIGHT*0.20), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def third_angle(self):
        h = self.section_header(5, "TERCER DIEDRO · THIRD-ANGLE · ISO A", "Orden físico: observador → plano → objeto. En la lámina, las vistas quedan del mismo lado.")
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
        self.play(FadeOut(obs), FadeOut(obj), FadeOut(plane), FadeOut(a1), FadeOut(a2), FadeOut(one), FadeOut(two), FadeOut(three), run_time=RT)
        layout = self.placement_cross(first_angle=False, compact=False).shift(LEFT*0.25+DOWN*0.08)
        side_note = VGroup(self.text("TERCER DIEDRO", 29, BOLD, BLUE), self.text("PLANTA ↑", 25, BOLD, TEAL), self.text("LATERAL D. →", 25, BOLD, ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.80).shift(DOWN*0.20)
        self.play(FadeIn(side_note[0]), run_time=RT)
        self.play(FadeIn(layout[0]), run_time=RT)
        self.play(FadeIn(side_note[1]), FadeIn(layout[1], shift=DOWN*0.20), run_time=RT_SLOW)
        self.play(FadeIn(side_note[2]), FadeIn(layout[2], shift=LEFT*0.20), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def compare_methods(self):
        h = self.section_header(6, "MISMAS VISTAS · DISTINTA DISTRIBUCIÓN", "La diferencia práctica está en dónde aparecen las vistas alrededor del alzado.")
        self.add(h)
        divider = Line(UP*2.55, DOWN*3.70, color=LIGHT, stroke_width=2.0)
        left_title = self.text("PRIMER DIEDRO · ISO E", 28, BOLD, BLUE).move_to(LEFT*3.85+UP*2.40)
        right_title = self.text("TERCER DIEDRO · ISO A", 28, BOLD, BLUE).move_to(RIGHT*3.85+UP*2.40)
        left = self.placement_cross(True, compact=True).scale(0.82).move_to(LEFT*3.65+DOWN*0.70)
        right = self.placement_cross(False, compact=True).scale(0.82).move_to(RIGHT*3.65+DOWN*0.70)
        first_rule = self.emphasis("OPUESTO", ORANGE, 24, 3.2).move_to(LEFT*3.65+DOWN*3.10)
        third_rule = self.emphasis("MISMO LADO", GREEN, 24, 3.2).move_to(RIGHT*3.65+DOWN*3.10)
        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), run_time=RT)
        self.play(LaggedStart(FadeIn(left[0]), FadeIn(right[0]), lag_ratio=0.18), run_time=RT_SLOW)
        self.play(LaggedStart(FadeIn(left[1]), FadeIn(right[1]), lag_ratio=0.18), run_time=RT_SLOW)
        self.play(LaggedStart(FadeIn(left[2]), FadeIn(right[2]), lag_ratio=0.18), run_time=RT_SLOW)
        self.play(FadeIn(first_rule), FadeIn(third_rule), run_time=RT)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def symbols_and_colombia(self):
        h = self.section_header(7, "EL SÍMBOLO TE DICE QUÉ MÉTODO LEER", "Antes de interpretar la posición de las vistas, identifica el símbolo de proyección.")
        self.add(h)
        first = self.projection_symbol(True, 1.10).move_to(LEFT*3.75+UP*0.75)
        third = self.projection_symbol(False, 1.10).move_to(RIGHT*3.75+UP*0.75)
        first_title = self.text("PRIMER DIEDRO", 28, BOLD, BLUE).next_to(first, UP, buff=0.42)
        first_sub = self.text("First-angle · ISO E", 21, BOLD, MID).next_to(first, DOWN, buff=0.36)
        third_title = self.text("TERCER DIEDRO", 28, BOLD, BLUE).next_to(third, UP, buff=0.42)
        third_sub = self.text("Third-angle · ISO A", 21, BOLD, MID).next_to(third, DOWN, buff=0.36)
        divider = Line(UP*2.35, DOWN*1.55, color=LIGHT, stroke_width=2)
        self.play(Create(divider), run_time=RT)
        self.play(DrawBorderThenFill(first), FadeIn(first_title), FadeIn(first_sub), run_time=RT_HERO)
        self.play(DrawBorderThenFill(third), FadeIn(third_title), FadeIn(third_sub), run_time=RT_HERO)
        self.wait(PAUSE_EXPLAIN)
        colombia = RoundedRectangle(width=13.6, height=1.65, corner_radius=0.16, stroke_color=NAVY, stroke_width=2.0, fill_color=WHITE, fill_opacity=1).to_edge(DOWN, buff=0.35)
        c1 = self.text("COLOMBIA · NTC 1777:2001", 24, BOLD, NAVY)
        c2 = self.text("Norma técnica, no ley. Reconoce los métodos de primer y tercer diedro.", 21, NORMAL, DARK)
        c = VGroup(c1, c2).arrange(DOWN, buff=0.16).move_to(colombia)
        self.play(FadeIn(colombia), FadeIn(c), run_time=RT_SLOW)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def challenge(self):
        h = self.section_header(8, "DESAFÍO DE LECTURA", "Mira el símbolo. Decide dónde deben ir la planta y el lateral derecho.")
        self.add(h)
        symbol = self.projection_symbol(False, 0.92).to_edge(LEFT, buff=0.75).shift(UP*0.85)
        tag = self.mini_label("¿QUÉ MÉTODO ES?", BLUE, 19).next_to(symbol, UP, buff=0.30)
        front_panel = self.view_panel("ALZADO", self.front_view(0.56), 3.70, 2.70, BLUE).move_to(DOWN*1.10)
        top_slot = RoundedRectangle(width=3.70, height=2.70, corner_radius=0.14, stroke_color=TEAL, stroke_width=2.2, fill_opacity=0).next_to(front_panel, UP, buff=0.34)
        right_slot = RoundedRectangle(width=3.70, height=2.70, corner_radius=0.14, stroke_color=ORANGE, stroke_width=2.2, fill_opacity=0).next_to(front_panel, RIGHT, buff=0.34)
        q1 = self.text("PLANTA ?", 23, BOLD, TEAL).move_to(top_slot)
        q2 = self.text("LATERAL D. ?", 23, BOLD, ORANGE).move_to(right_slot)
        self.play(DrawBorderThenFill(symbol), FadeIn(tag), run_time=RT_SLOW)
        self.play(FadeIn(front_panel), Create(top_slot), Create(right_slot), FadeIn(q1), FadeIn(q2), run_time=RT_SLOW)
        prompt = self.emphasis("Piensa antes de revelar la respuesta", NAVY, 25, 5.8).to_edge(LEFT, buff=0.70).shift(DOWN*1.85)
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
        answer = self.emphasis("TERCER DIEDRO → MISMO LADO", GREEN, 26, 5.8).move_to(prompt)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(top_slot), FadeOut(right_slot), Transform(prompt, answer), run_time=RT)
        self.play(FadeIn(top, shift=DOWN*0.20), FadeIn(right, shift=LEFT*0.20), run_time=RT_HERO)
        self.wait(PAUSE_LONG)
        self.clear_stage()

    def closing(self):
        kicker = self.text("MÉTODO DE LECTURA", 24, BOLD, BLUE)
        title = self.text("SÍMBOLO → ALZADO → POSICIÓN DE LAS VISTAS", 46, BOLD, NAVY)
        title_group = VGroup(kicker, title).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        title_group.to_edge(UP, buff=0.60).to_edge(LEFT, buff=0.70)
        steps = [("1", "IDENTIFICA EL SÍMBOLO", BLUE), ("2", "UBICA EL ALZADO", CYAN), ("3", "LEE PLANTA Y LATERALES", TEAL), ("4", "VERIFICA PRIMER / TERCER DIEDRO", ORANGE)]
        cards = VGroup()
        for num, label, col in steps:
            n = Circle(radius=0.34, stroke_color=col, stroke_width=2.4, fill_color=WHITE, fill_opacity=1)
            nt = self.text(num, 22, BOLD, col).move_to(n)
            txt = self.text(label, 24, BOLD, INK)
            row = VGroup(VGroup(n, nt), txt).arrange(RIGHT, buff=0.22)
            box = RoundedRectangle(width=6.2, height=1.02, corner_radius=0.14, stroke_color=LIGHT, stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
            row.move_to(box).align_to(box, LEFT).shift(RIGHT*0.35)
            cards.add(VGroup(box, row))
        cards.arrange(DOWN, buff=0.22).move_to(LEFT*3.55+DOWN*0.75)
        final_part = self.mechanical_part(0.70).move_to(RIGHT*3.25+DOWN*0.60)
        final_note = self.emphasis("3D → 2D SIN AMBIGÜEDAD", GREEN, 27, 5.3).next_to(final_part, DOWN, buff=0.26)
        self.play(FadeIn(kicker), Write(title), run_time=RT_HERO)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.12) for c in cards], lag_ratio=0.13), run_time=RT_HERO*1.2)
        self.play(DrawBorderThenFill(final_part[1]), FadeIn(final_part[0]), run_time=RT_HERO)
        self.play(FadeIn(final_note), run_time=RT)
        self.wait(PAUSE_LONG)


if __name__ == "__main__":
    pass
