from __future__ import annotations

import math
import numpy as np
from manim import *

from fillet_redondeo_senior_v5 import (
    InventorFilletRedondeoSeniorV5,
    BLACK_TEXT, DARK, MID, LIGHT, STEEL, STEEL_DARK,
    SKETCH, VALID, REMOVE, PAPER,
    TITLE, BODY, MICRO, READ, EXPLAIN, OBSERVE,
)


class InventorPatternSeniorBase(InventorFilletRedondeoSeniorV5):
    """White-background senior visual contract for Inventor pattern lessons.

    The architecture intentionally follows the latest Fillet / Chamfer / Hole
    senior lineage: large monochrome typography, blue sketch geometry, green
    valid previews, red warnings, safe-area assertions, granular phases and a
    complete 2D -> 3D -> feature -> validation -> parametric-edit narrative.
    """

    OPERATION = "PATTERN"
    SUBTITLE = "operación paramétrica 3D"
    ROUTE = "SKETCH  →  EXTRUDE  →  SEED  →  DIRECTION / AXIS  →  PARAMETERS  →  PATTERN"
    FEATURE_NAME = "Pattern1"

    BASE_W = 6.40
    BASE_D = 4.00
    BASE_H = 0.72

    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 28, BOLD, DARK)
        subtitle = self.text(f"{self.OPERATION} · {self.SUBTITLE}", 21, NORMAL, MID)
        title.to_corner(UL, buff=0.34)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.05)
        rule = Line(LEFT * 7.52, RIGHT * 7.52, color=LIGHT, stroke_width=1.4).to_edge(UP, buff=1.08)
        phase_box = RoundedRectangle(
            width=5.65, height=0.62, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=DARK, stroke_width=1.2,
        ).to_corner(UR, buff=0.34)
        phase = self.text("01 · IDEA DEL PATRÓN", 20, BOLD, DARK).move_to(phase_box)
        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.55)
        self.wait(READ)
        return {"group": group, "box": phase_box, "phase": phase}

    def opening(self, tagline):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 28, BOLD, DARK)
        title = self.text(self.OPERATION, TITLE, BOLD)
        sub = self.text(tagline, 30, NORMAL, MID)
        rule = Line(LEFT * 5.85, RIGHT * 5.85, color=BLACK, stroke_width=2)
        route_text = self.text(self.ROUTE, 23, BOLD, DARK)
        group = VGroup(top, title, rule, sub, route_text).arrange(DOWN, buff=0.34)
        self.fit(group, 13.7, 6.2)
        self.fixed(group)
        self.play(FadeIn(top, shift=UP * 0.08), run_time=0.75)
        self.play(Write(title), run_time=1.15)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(Write(route_text), run_time=1.25)
        self.wait(EXPLAIN)
        self.clear_fixed(group, run_time=0.60)

    def generic_parameter_card(self, title, rows, center=(5.20, -0.10, 0), width=5.15):
        head = self.text(title, 25, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 19, BOLD, DARK)
            val = self.text(right, 19, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.45, height=0.50, corner_radius=0.05,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.0,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.13)
            row = VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.15)
            entries.add(row)
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        if content.width > width - 0.45:
            content.scale_to_fit_width(width - 0.45)
        panel = RoundedRectangle(
            width=width, height=content.height + 0.50, corner_radius=0.11,
            fill_color=PAPER, fill_opacity=0.99,
            stroke_color=DARK, stroke_width=1.25,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.24)
        group = VGroup(panel, content).move_to(center)
        self.fixed(group)
        return group

    def generic_feature_tree(self, items, center=(-5.45, -0.35, 0), width=4.45):
        lines = VGroup()
        for text, color, weight in items:
            lines.add(self.text(text, 19, weight, color))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        panel = RoundedRectangle(
            width=width, height=lines.height + 0.52, corner_radius=0.09,
            fill_color=WHITE, fill_opacity=0.98,
            stroke_color=DARK, stroke_width=1.1,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.24)
        group = VGroup(panel, lines).move_to(center)
        self.fixed(group)
        return group

    def base_plate(self, center=(0, 0, 0.36)):
        return self.box((self.BASE_W, self.BASE_D, self.BASE_H), center, STEEL, 0.94)

    def hole_void(self, center_xy, radius=0.25, height=None, opacity=1.0):
        h = height if height is not None else self.BASE_H + 0.06
        return Cylinder(
            radius=radius,
            height=h,
            direction=OUT,
            fill_color=DARK,
            fill_opacity=opacity,
            stroke_color=BLACK,
            stroke_width=0.8,
            resolution=(20, 20),
        ).move_to([center_xy[0], center_xy[1], self.BASE_H / 2])

    def preview_hole(self, center_xy, radius=0.25, opacity=0.48):
        return Cylinder(
            radius=radius,
            height=self.BASE_H + 0.08,
            direction=OUT,
            fill_color=VALID,
            fill_opacity=opacity,
            stroke_color=VALID,
            stroke_width=1.2,
            resolution=(20, 20),
        ).move_to([center_xy[0], center_xy[1], self.BASE_H / 2])

    def top_circle(self, center_xy, radius=0.25, color=SKETCH, width=5):
        return Circle(radius=radius, color=color, stroke_width=width).move_to(
            [center_xy[0], center_xy[1], self.BASE_H + 0.012]
        )

    def axis_arrow(self, start, end, color=SKETCH):
        return Arrow3D(
            start=np.array(start, dtype=float),
            end=np.array(end, dtype=float),
            color=color,
            thickness=0.018,
            height=0.20,
            base_radius=0.075,
        )

    def formula_strip(self, text, color=DARK, y=-3.36, width=11.6):
        label = self.text(text, 25, BOLD, color)
        if label.width > width - 0.55:
            label.scale_to_fit_width(width - 0.55)
        box = RoundedRectangle(
            width=width, height=0.80, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=color, stroke_width=1.25,
        )
        label.move_to(box)
        group = VGroup(box, label).move_to([0, y, 0])
        self.fixed(group)
        self.play(FadeIn(box), Write(label), run_time=0.75)
        return group

    def finish_summary(self, hud, title, lines, model):
        self.set_phase(hud, 11, "RESUMEN + MODELO FINAL", VALID)
        note = self.note(title, VALID, width=12.6)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        summary = VGroup(*[self.text(line, 24, BOLD if i == 0 else NORMAL, DARK)
                           for i, line in enumerate(lines)])
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if summary.width > 8.3:
            summary.scale_to_fit_width(8.3)
        panel = RoundedRectangle(
            width=9.2, height=summary.height + 0.62, corner_radius=0.12,
            fill_color=WHITE, fill_opacity=0.97,
            stroke_color=DARK, stroke_width=1.2,
        )
        summary.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.30)
        card = VGroup(panel, summary).move_to([0, -2.25, 0])
        self.fixed(card)
        self.play(FadeIn(card), run_time=0.85)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(OBSERVE * 2.0)
        self.stop_ambient_camera_rotation()
        self.clear_fixed(card, run_time=0.45)
        self.play(FadeOut(model), run_time=0.65)
        self.play(FadeOut(hud["group"]), run_time=0.50)
        self.remove_fixed_in_frame_mobjects(hud["group"])
