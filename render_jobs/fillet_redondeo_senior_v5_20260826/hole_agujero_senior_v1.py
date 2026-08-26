from __future__ import annotations

import numpy as np
from manim import *

from fillet_redondeo_senior_v5 import (
    InventorFilletRedondeoSeniorV5,
    BLACK_TEXT, DARK, MID, LIGHT, STEEL, STEEL_DARK,
    SKETCH, VALID, REMOVE, PAPER, WHITE,
    BOLD, NORMAL, TITLE, BODY, MICRO, READ, EXPLAIN, OBSERVE, smooth,
)


class InventorHoleAgujeroSeniorV1(InventorFilletRedondeoSeniorV5):
    """Senior classroom lesson for Autodesk Inventor Hole / Agujero.

    Visual contract inherited from the approved Fillet / Chamfer family:
    white background, black institutional typography, large classroom-safe labels,
    explicit Sketch -> Feature logic, isolated command cards, 2D/3D camera changes,
    progressive material removal, validation, parametric edit and final orbit.

    Focus operation:
        Sketch2 Point1 -> Hole -> Simple -> Diameter 12 mm -> Through All -> Hole1

    The 3D scene is complemented by a large section A-A so the Through All
    termination and the removed cylindrical volume are unambiguous.
    """

    BASE_W = 7.20
    BASE_D = 4.30
    BASE_H = 1.10
    HOLE_R = 0.52
    HOLE_R_EDIT = 0.78
    POINT_X = 1.35
    POINT_Y = 0.55
    PANEL_CLEARANCE = 1.15

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------
    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 31, BOLD, DARK)
        subtitle = self.text("HOLE / AGUJERO 3D · herramienta paramétrica", 24, NORMAL, MID)
        title.to_corner(UL, buff=0.32)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.045)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.5).to_edge(UP, buff=1.13)

        phase_box = RoundedRectangle(
            width=5.85, height=0.68, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        ).to_corner(UR, buff=0.32)
        phase = self.text("01 · IDEA DEL AGUJERO", 23, BOLD, DARK).move_to(phase_box)

        # Hard composition contract: left subtitle cannot enter the phase box.
        if subtitle.get_right()[0] > phase_box.get_left()[0] - 0.18:
            raise ValueError("HUD subtitle overlaps phase box")

        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.55)
        self.wait(READ)
        return {"group": group, "box": phase_box, "phase": phase}

    def set_phase(self, hud, number, label, color=DARK):
        old = hud["phase"]
        new = self.text(f"{number:02d} · {label}", 23, BOLD, color)
        if new.width > hud["box"].width - 0.42:
            new.scale_to_fit_width(hud["box"].width - 0.42)
        new.move_to(hud["box"])
        self.fixed(new)
        self.play(FadeOut(old, shift=UP*0.03), FadeIn(new, shift=UP*0.03), run_time=0.50)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        hud["phase"] = new
        self.wait(MICRO)

    def note_big(self, text, color=DARK, y=-3.43, width=13.05, font=25):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.70:
            label.scale_to_fit_width(width - 0.70)
        panel = RoundedRectangle(
            width=width, height=0.84, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.992,
            stroke_color=color, stroke_width=1.35,
        )
        label.move_to(panel)
        group = VGroup(panel, label).move_to([0, y, 0])
        self.fixed(group)
        self.play(FadeIn(panel, shift=UP*0.05), Write(label), run_time=0.70)
        self.wait(MICRO)
        return group

    def parameter_card(self):
        rows = [
            ("Placement", "From Sketch"),
            ("Center", "Point1"),
            ("Hole Type", "Simple"),
            ("Diameter", "Ø 12 mm"),
            ("Termination", "Through All"),
        ]
        head = self.text("HOLE PARAMETERS", 28, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 22, BOLD, DARK)
            val = self.text(right, 22, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=3.05, height=0.56, corner_radius=0.05,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.05,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.16)
            row = VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.20)
            entries.add(row)
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel = RoundedRectangle(
            width=5.65, height=content.height+0.58, corner_radius=0.11,
            fill_color=PAPER, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.30)
        group = VGroup(panel, content).move_to([5.05, -0.20, 0])
        self.fixed(group)
        return group

    def feature_tree(self):
        items = [
            ("Part1.ipt", DARK, BOLD),
            ("Origin", MID, NORMAL),
            ("Sketch1", MID, NORMAL),
            ("Extrusion1   12 mm", DARK, NORMAL),
            ("Sketch2   Point1", SKETCH, NORMAL),
            ("Hole1   Ø12 · Through All", VALID, BOLD),
        ]
        lines = VGroup(*[
            self.text(t, 22, w, c) for t, c, w in items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        panel = RoundedRectangle(
            width=4.95, height=lines.height+0.62, corner_radius=0.09,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=DARK, stroke_width=1.15,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.28)
        group = VGroup(panel, lines).move_to([-5.20, -0.45, 0])
        self.fixed(group)
        return group

    def validation_card(self, title, lines, color, center):
        head = self.text(title, 29, BOLD, color)
        body = VGroup()
        for i, line in enumerate(lines):
            t = self.text(line, 23 if i == 0 else 21, BOLD if i == 0 else NORMAL, DARK)
            if t.width > 4.25:
                t.scale_to_fit_width(4.25)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel = RoundedRectangle(
            width=4.85, height=max(1.72, content.height+0.50), corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=color, stroke_width=1.45,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.25)
        return VGroup(panel, content).move_to(center)

    # ------------------------------------------------------------------
    # 3D helpers
    # ------------------------------------------------------------------
    def base_body(self, color=STEEL):
        return self.box(
            (self.BASE_W, self.BASE_D, self.BASE_H),
            [0, 0, self.BASE_H/2],
            color=color,
            opacity=0.96,
            stroke=DARK,
            stroke_width=0.85,
        )

    def cut_cylinder(self, radius=None, color=REMOVE, opacity=0.28, extra=0.85):
        r = self.HOLE_R if radius is None else radius
        cyl = Cylinder(
            radius=r,
            height=self.BASE_H + extra,
            resolution=(32, 18),
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=color,
            stroke_width=0.65,
        )
        cyl.move_to(np.array([
            self.POINT_X,
            self.POINT_Y,
            self.BASE_H/2,
        ]))
        return cyl

    def hole_visual(self, radius=None, body_color=STEEL):
        """Readable 3D representation of a through-hole.

        The outer plate remains a solid Manim box, while a white top opening,
        dark rim, lower opening and translucent inner cylindrical wall provide
        an unambiguous classroom view of the removed volume. Section A-A later
        gives the exact through-thickness interpretation.
        """
        r = self.HOLE_R if radius is None else radius
        body = self.base_body(body_color)

        top_open = Circle(
            radius=r,
            fill_color=WHITE,
            fill_opacity=1.0,
            stroke_color=DARK,
            stroke_width=2.4,
        ).move_to([self.POINT_X, self.POINT_Y, self.BASE_H + 0.012])
        bottom_open = Circle(
            radius=r*0.98,
            fill_color=WHITE,
            fill_opacity=0.93,
            stroke_color=DARK,
            stroke_width=1.4,
        ).move_to([self.POINT_X, self.POINT_Y, -0.012])
        inner = Cylinder(
            radius=r*0.99,
            height=self.BASE_H,
            resolution=(32, 12),
            fill_color=DARK,
            fill_opacity=0.15,
            stroke_color=DARK,
            stroke_width=0.55,
        ).move_to([self.POINT_X, self.POINT_Y, self.BASE_H/2])
        return VGroup(body, inner, bottom_open, top_open)

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 30, BOLD, DARK)
        title = self.text("HOLE / AGUJERO", TITLE, BOLD)
        sub = self.text("Crear un vacío cilíndrico controlado dentro de una pieza", 31, NORMAL, MID)
        rule = Line(LEFT*6.1, RIGHT*6.1, color=BLACK, stroke_width=2)
        route1 = self.text("SKETCH1  →  EXTRUSION1  →  TOP FACE  →  SKETCH2", 25, BOLD, DARK)
        route2 = self.text("POINT1  →  Ø12 mm  →  THROUGH ALL  →  HOLE1", 27, BOLD, VALID)
        group = VGroup(top, title, rule, sub, route1, route2).arrange(DOWN, buff=0.31)
        self.fit(group, 13.9, 6.55)
        self.fixed(group)
        self.play(FadeIn(top, shift=UP*0.08), run_time=0.70)
        self.play(Write(title), run_time=1.10)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(Write(route1), run_time=1.15)
        self.play(Write(route2), run_time=1.10)
        self.wait(EXPLAIN)
        self.clear_fixed(group, 0.60)

    def concept(self, hud):
        self.set_phase(hud, 1, "IDEA DEL AGUJERO", DARK)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)

        plate = RoundedRectangle(
            width=8.2, height=4.55, corner_radius=0.12,
            fill_color=PAPER, fill_opacity=1,
            stroke_color=DARK, stroke_width=4.0,
        )
        center = Dot([1.20, 0.45, 0], radius=0.10, color=SKETCH)
        cross1 = Line([0.98, 0.45, 0], [1.42, 0.45, 0], color=SKETCH, stroke_width=3)
        cross2 = Line([1.20, 0.23, 0], [1.20, 0.67, 0], color=SKETCH, stroke_width=3)
        hole = Circle(radius=0.70, color=VALID, stroke_width=7).move_to(center)
        call = self.small_callout("CENTRO DEL AGUJERO", SKETCH, point=[-2.60, -1.75, 0], width=4.65)
        arrow = Arrow(call.get_top(), center.get_center()+LEFT*0.10+DOWN*0.08,
                      buff=0.15, color=SKETCH, stroke_width=2.3)
        self.fixed(arrow)

        self.play(FadeIn(plate), run_time=0.55)
        self.play(FadeIn(center), Create(cross1), Create(cross2), run_time=0.70)
        self.play(FadeIn(call), GrowArrow(arrow), run_time=0.65)
        self.play(Create(hole), run_time=1.00)
        note = self.note_big(
            "Hole necesita primero una UBICACIÓN; después define diámetro y profundidad.",
            DARK,
        )
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(call, 0.25)
        self.clear_fixed(arrow, 0.25)
        self.play(FadeOut(VGroup(plate, center, cross1, cross2, hole)), run_time=0.45)

    def sketch1(self, hud):
        self.set_phase(hud, 2, "SKETCH1 · BASE", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.75)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5.5)
        h_axis = DashedLine([-w/2-0.35, 0, 0], [w/2+0.35, 0, 0],
                            color=LIGHT, dash_length=0.12, stroke_width=1.5)
        v_axis = DashedLine([0, -d/2-0.28, 0], [0, d/2+0.28, 0],
                            color=LIGHT, dash_length=0.12, stroke_width=1.5)
        origin = Dot(ORIGIN, radius=0.07, color=REMOVE)
        dim_w = DoubleArrow([-w/2, -d/2-0.52, 0], [w/2, -d/2-0.52, 0],
                            buff=0, color=DARK, stroke_width=2.2)
        dim_d = DoubleArrow([w/2+0.56, -d/2, 0], [w/2+0.56, d/2, 0],
                            buff=0, color=DARK, stroke_width=2.2)
        lab_w = self.text("80 mm", 27, BOLD, DARK).next_to(dim_w, DOWN, buff=0.09)
        lab_d = self.text("50 mm", 27, BOLD, DARK).rotate(PI/2).next_to(dim_d, RIGHT, buff=0.09)

        self.play(Create(h_axis), Create(v_axis), FadeIn(origin), run_time=0.60)
        self.play(Create(outline), run_time=1.30)
        self.play(Create(dim_w), Write(lab_w), run_time=0.75)
        self.play(Create(dim_d), Write(lab_d), run_time=0.75)
        fully = self.small_callout("FULLY CONSTRAINED", VALID, point=[-2.20, 2.70, 0], width=4.55)
        self.play(FadeIn(fully), run_time=0.50)
        note = self.note_big("PASO 1 · Sketch1 define solamente la placa base de 80 × 50 mm.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(fully, 0.25)
        self.play(FadeOut(dim_w), FadeOut(dim_d), FadeOut(lab_w), FadeOut(lab_d), run_time=0.35)
        return outline, h_axis, v_axis, origin

    def extrude(self, hud, outline, h_axis, v_axis, origin):
        self.set_phase(hud, 3, "EXTRUSION1 · 12 mm", DARK)
        self.play(FadeOut(h_axis), FadeOut(v_axis), FadeOut(origin), run_time=0.30)
        self.move_camera(phi=64*DEGREES, theta=-46*DEGREES, zoom=1.02, run_time=1.15)
        body = self.base_body()
        preview = self.base_body(STEEL_DARK).set_opacity(0.20)
        self.play(FadeIn(preview), run_time=0.55)
        self.play(FadeOut(outline), Transform(preview, body), run_time=1.65, rate_func=smooth)
        body = preview
        note = self.note_big("PASO 2 · Extrusion1 convierte Sketch1 en una placa de 12 mm de espesor.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return body

    def select_top_face(self, hud, body):
        self.set_phase(hud, 4, "SELECCIONAR CARA SUPERIOR", SKETCH)
        w, d, h = self.BASE_W, self.BASE_D, self.BASE_H
        face = Polygon(
            [-w/2, -d/2, h+0.015], [w/2, -d/2, h+0.015],
            [w/2, d/2, h+0.015], [-w/2, d/2, h+0.015],
            fill_color=SKETCH, fill_opacity=0.16,
            stroke_color=SKETCH, stroke_width=3.2,
        )
        self.play(FadeIn(face), run_time=0.55)
        tag = self.small_callout("TOP FACE", SKETCH, point=[4.55, 1.90, 0], width=2.90)
        self.play(FadeIn(tag), run_time=0.45)
        note = self.note_big("PASO 3 · Selecciona la cara donde se ubicará el centro del agujero.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)
        self.play(FadeOut(face), run_time=0.30)
        return body

    def sketch2_point(self, hud, body):
        self.set_phase(hud, 5, "SKETCH2 · POINT1", SKETCH)
        self.play(FadeOut(body), run_time=0.30)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.95)

        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=DARK, stroke_width=4.2,
                            fill_color=PAPER, fill_opacity=0.55)
        px, py = self.POINT_X, self.POINT_Y
        point = Dot([px, py, 0], radius=0.105, color=SKETCH)
        cross_h = Line([px-0.28, py, 0], [px+0.28, py, 0], color=SKETCH, stroke_width=3.2)
        cross_v = Line([px, py-0.28, 0], [px, py+0.28, 0], color=SKETCH, stroke_width=3.2)

        xdim = DoubleArrow([-w/2, py-0.58, 0], [px, py-0.58, 0], buff=0,
                           color=SKETCH, stroke_width=2.3)
        ydim = DoubleArrow([px+0.58, -d/2, 0], [px+0.58, py, 0], buff=0,
                           color=SKETCH, stroke_width=2.3)
        xlab = self.text("55 mm", 28, BOLD, SKETCH).next_to(xdim, DOWN, buff=0.07)
        ylab = self.text("32 mm", 28, BOLD, SKETCH).rotate(PI/2).next_to(ydim, RIGHT, buff=0.08)

        self.play(FadeIn(outline), run_time=0.40)
        self.play(FadeIn(point), Create(cross_h), Create(cross_v), run_time=0.70)
        self.play(Create(xdim), Write(xlab), run_time=0.75)
        self.play(Create(ydim), Write(ylab), run_time=0.75)
        fully = self.small_callout("POINT1 · FULLY CONSTRAINED", VALID, point=[-2.05, 2.70, 0], width=5.60)
        self.play(FadeIn(fully), run_time=0.50)
        note = self.note_big("PASO 4 · En Sketch2 coloca y acota Point1. El punto controla la POSICIÓN.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(fully, 0.25)
        self.play(FadeOut(xdim), FadeOut(ydim), FadeOut(xlab), FadeOut(ylab), run_time=0.35)
        return VGroup(outline, point, cross_h, cross_v)

    def invoke_hole(self, hud, sketch2):
        self.set_phase(hud, 6, "3D MODEL · HOLE", DARK)
        self.play(sketch2.animate.shift(LEFT*(1.05+self.PANEL_CLEARANCE)), run_time=0.70, rate_func=smooth)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.65)
        note = self.note_big("PASO 5 · Finish Sketch → 3D Model → Hole. Selecciona Point1.", DARK)
        self.wait(READ)
        self.clear_fixed(note)

        # The left-side sketch and right-side command card are explicitly separated.
        if sketch2.get_right()[0] > card.get_left()[0] - 0.35:
            raise ValueError("Sketch2 overlaps Hole parameter panel")

        focus = self.small_callout("Ø 12 mm  ·  THROUGH ALL", VALID, point=[4.95, -2.80, 0], width=5.00)
        self.play(FadeIn(focus), run_time=0.45)
        note = self.note_big("PASO 6 · El DIÁMETRO controla el tamaño; THROUGH ALL atraviesa todo el sólido.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(focus, 0.25)
        return card

    def top_preview(self, hud, sketch2, card):
        self.set_phase(hud, 7, "PREVIEW · Ø12 mm", VALID)
        self.play(FadeOut(card), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(sketch2.animate.shift(RIGHT*(1.05+self.PANEL_CLEARANCE)), run_time=0.65, rate_func=smooth)

        point = np.array([self.POINT_X, self.POINT_Y, 0])
        circle = Circle(radius=self.HOLE_R, color=VALID, stroke_width=8).move_to(point)
        dia = DoubleArrow(point+LEFT*self.HOLE_R, point+RIGHT*self.HOLE_R,
                          buff=0, color=SKETCH, stroke_width=2.6)
        lab = self.text("Ø 12 mm", 31, BOLD, SKETCH).next_to(dia, DOWN, buff=0.13)
        red = Circle(radius=self.HOLE_R*0.90, fill_color=REMOVE, fill_opacity=0.12,
                     stroke_width=0).move_to(point)
        self.play(FadeIn(red), run_time=0.40)
        self.play(Create(circle), run_time=0.95)
        self.play(Create(dia), Write(lab), run_time=0.75)
        note = self.note_big("PASO 7 · El preview circular debe quedar centrado exactamente sobre Point1.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(VGroup(sketch2, red, circle, dia, lab)), run_time=0.45)

    def section_view(self, hud):
        self.set_phase(hud, 8, "SECCIÓN A–A · THROUGH ALL", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.75)

        plate = Rectangle(width=9.1, height=2.20, stroke_color=DARK, stroke_width=4.2,
                          fill_color=STEEL, fill_opacity=0.55).shift(UP*0.10)
        hole_w = 1.35
        opening = Rectangle(width=hole_w, height=2.30, stroke_width=0,
                            fill_color=WHITE, fill_opacity=1).move_to(plate)
        wall_l = Line([-hole_w/2, -1.00, 0], [-hole_w/2, 1.20, 0], color=VALID, stroke_width=6)
        wall_r = Line([hole_w/2, -1.00, 0], [hole_w/2, 1.20, 0], color=VALID, stroke_width=6)
        axis = DashedLine([0, -1.55, 0], [0, 1.65, 0], color=SKETCH,
                          dash_length=0.12, stroke_width=2.0)
        top_arrow = Arrow([0, 2.40, 0], [0, 1.28, 0], buff=0.08,
                          color=REMOVE, stroke_width=2.7)
        bottom_arrow = Arrow([0, -2.30, 0], [0, -1.08, 0], buff=0.08,
                             color=VALID, stroke_width=2.7)
        top_label = self.text("ENTRADA", 25, BOLD, REMOVE).next_to(top_arrow, UP, buff=0.06)
        bottom_label = self.text("SALIDA", 25, BOLD, VALID).next_to(bottom_arrow, DOWN, buff=0.06)
        thickness = DoubleArrow([5.00, -1.00, 0], [5.00, 1.20, 0], buff=0,
                                color=DARK, stroke_width=2.2)
        thick_lab = self.text("12 mm", 27, BOLD, DARK).rotate(PI/2).next_to(thickness, RIGHT, buff=0.09)
        through = self.small_callout("THROUGH ALL", VALID, point=[-3.55, -2.15, 0], width=4.10)

        self.play(FadeIn(plate), run_time=0.50)
        self.play(FadeIn(opening), Create(wall_l), Create(wall_r), Create(axis), run_time=0.85)
        self.play(GrowArrow(top_arrow), Write(top_label), run_time=0.65)
        self.play(GrowArrow(bottom_arrow), Write(bottom_label), run_time=0.65)
        self.play(Create(thickness), Write(thick_lab), FadeIn(through), run_time=0.75)
        note = self.note_big("SECCIÓN A–A · Through All significa que el vacío cruza TODO el espesor de la placa.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(through, 0.25)
        self.play(FadeOut(VGroup(plate, opening, wall_l, wall_r, axis, top_arrow, bottom_arrow,
                                 top_label, bottom_label, thickness, thick_lab)), run_time=0.45)

    def cut_3d(self, hud):
        self.set_phase(hud, 9, "REMOVER CILINDRO", REMOVE)
        self.move_camera(phi=64*DEGREES, theta=-46*DEGREES, zoom=1.03, run_time=1.15)
        body = self.base_body()
        self.play(FadeIn(body), run_time=0.55)

        cutter = self.cut_cylinder()
        cutter.shift(OUT*1.65)
        self.play(FadeIn(cutter), run_time=0.55)
        note = self.note_big("PASO 8A · El cilindro rojo representa exactamente el material que Hole eliminará.", REMOVE)
        self.wait(READ)
        self.clear_fixed(note)

        self.play(cutter.animate.shift(IN*1.65), run_time=2.25, rate_func=smooth)
        note = self.note_big("PASO 8B · Through All proyecta el cilindro de corte a través de todo el sólido.", REMOVE)
        self.wait(READ)
        self.clear_fixed(note)

        final = self.hole_visual()
        self.play(FadeOut(body), FadeOut(cutter), FadeIn(final), run_time=1.10)
        note = self.note_big("RESULTADO · Hole1 deja una abertura circular y una pared cilíndrica interior.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return final

    def validate(self, hud, final):
        self.set_phase(hud, 10, "VALIDAR ANTES DE OK", DARK)
        self.play(final.animate.shift(UP*0.80), run_time=0.65, rate_func=smooth)

        ok = self.validation_card(
            "VÁLIDO",
            ["Point1 acotado", "Ø12 mm", "Through All"],
            VALID,
            center=[-3.00, -2.70, 0],
        )
        bad = self.validation_card(
            "REVISAR",
            ["punto cerca del borde", "diámetro excesivo", "terminación incorrecta"],
            REMOVE,
            center=[3.00, -2.70, 0],
        )
        cards = VGroup(ok, bad)
        self.fixed(cards)
        self.play(FadeIn(ok[0]), Write(ok[1]), run_time=0.90)
        self.wait(0.45)
        self.play(FadeIn(bad[0]), Write(bad[1]), run_time=0.90)
        self.wait(EXPLAIN)
        self.clear_fixed(cards, 0.40)
        self.play(final.animate.shift(DOWN*0.80), run_time=0.60, rate_func=smooth)
        return final

    def hole_types(self, hud, final):
        self.set_phase(hud, 11, "TIPOS DE HOLE", DARK)
        self.play(final.animate.shift(UP*0.70), run_time=0.55)

        simple = VGroup(
            Circle(radius=0.42, color=VALID, stroke_width=6),
            self.text("SIMPLE", 24, BOLD, VALID),
            self.text("Ø + depth", 21, NORMAL, DARK),
        ).arrange(DOWN, buff=0.17)
        counterbore = VGroup(
            VGroup(Circle(radius=0.52, color=SKETCH, stroke_width=5),
                   Circle(radius=0.26, color=SKETCH, stroke_width=4)),
            self.text("COUNTERBORE", 24, BOLD, SKETCH),
            self.text("2 diámetros", 21, NORMAL, DARK),
        ).arrange(DOWN, buff=0.17)
        countersink = VGroup(
            VGroup(Circle(radius=0.52, color=REMOVE, stroke_width=4),
                   Circle(radius=0.24, color=REMOVE, stroke_width=4)),
            self.text("COUNTERSINK", 24, BOLD, REMOVE),
            self.text("Ø + ángulo", 21, NORMAL, DARK),
        ).arrange(DOWN, buff=0.17)
        row = VGroup(simple, counterbore, countersink).arrange(RIGHT, buff=1.45).move_to([0, -1.35, 0])
        self.fixed(row)
        self.play(FadeIn(simple), run_time=0.55)
        self.play(FadeIn(counterbore), run_time=0.55)
        self.play(FadeIn(countersink), run_time=0.55)
        note = self.note_big("En esta lección usamos SIMPLE + THROUGH ALL; los otros tipos añaden geometría en la entrada.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(row, 0.40)
        self.play(final.animate.shift(DOWN*0.70), run_time=0.55)
        return final

    def parametric_edit(self, hud, final):
        self.set_phase(hud, 12, "OK · HOLE1", VALID)
        self.play(final.animate.shift(RIGHT*1.55 + UP*0.35), run_time=0.70, rate_func=smooth)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.60)
        note = self.note_big("PASO 9 · OK crea Hole1 después de Sketch2 en el árbol paramétrico.", VALID)
        self.wait(READ)
        self.clear_fixed(note)

        edit = self.small_callout("EDIT HOLE1", SKETCH, point=[0.20, -2.30, 0], width=3.60)
        self.play(FadeIn(edit), run_time=0.45)
        change = self.small_callout("Ø 12 mm  →  Ø 18 mm", SKETCH, point=[0.20, -3.02, 0], width=5.30)
        self.play(FadeIn(change), run_time=0.45)

        bigger = self.hole_visual(self.HOLE_R_EDIT, STEEL_DARK).shift(RIGHT*1.55 + UP*0.35)
        self.play(Transform(final, bigger), run_time=1.85, rate_func=smooth)
        self.wait(READ)
        self.clear_fixed(edit, 0.25)
        self.clear_fixed(change, 0.25)

        note = self.note_big("Diseño paramétrico: cambia Ø en Hole1; Sketch1 y Extrusion1 permanecen intactos.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)

        back = self.hole_visual(self.HOLE_R, STEEL).shift(RIGHT*1.55 + UP*0.35)
        self.play(Transform(final, back), run_time=1.45, rate_func=smooth)
        self.play(FadeOut(tree), final.animate.shift(LEFT*1.55 + DOWN*0.35), run_time=0.65)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def final_summary(self, hud, final):
        self.set_phase(hud, 13, "INSPECCIÓN FINAL", DARK)
        route1 = self.text("Sketch1 → Extrusion1 → Top Face → Sketch2 → Point1", 25, BOLD, DARK)
        route2 = self.text("Hole → Ø12 mm → Through All → Hole1", 28, BOLD, VALID)
        summary = VGroup(route1, route2).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.26)
        self.fit(summary, 14.0, 1.30)
        self.fixed(summary)
        self.play(Write(route1), run_time=1.00)
        self.play(Write(route2), run_time=1.00)
        self.wait(READ)
        self.begin_ambient_camera_rotation(rate=0.090)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()
        self.wait(OBSERVE)

    def construct(self):
        self.camera.background_color = WHITE
        self.opening()
        hud = self.hud()
        self.concept(hud)
        outline, h_axis, v_axis, origin = self.sketch1(hud)
        body = self.extrude(hud, outline, h_axis, v_axis, origin)
        body = self.select_top_face(hud, body)
        sketch2 = self.sketch2_point(hud, body)
        card = self.invoke_hole(hud, sketch2)
        self.top_preview(hud, sketch2, card)
        self.section_view(hud)
        final = self.cut_3d(hud)
        final = self.validate(hud, final)
        final = self.hole_types(hud, final)
        final = self.parametric_edit(hud, final)
        self.final_summary(hud, final)
