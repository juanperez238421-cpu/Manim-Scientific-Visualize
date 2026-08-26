from __future__ import annotations

import numpy as np
from manim import *

from chamfer_chaflan_senior_v1 import (
    InventorChamferChaflanSeniorV1,
    BLACK_TEXT, DARK, MID, LIGHT, STEEL, STEEL_DARK,
    SKETCH, VALID, REMOVE, PAPER, WHITE,
    BOLD, NORMAL, MICRO, READ, EXPLAIN, OBSERVE, smooth,
)


class InventorChamferChaflanSeniorV2(InventorChamferChaflanSeniorV1):
    """Senior QA V2 for Chamfer / Chaflán.

    V2 is a readability-first rebuild of the V1 lesson after frame audit.
    It keeps the correct 2D->3D CAD logic, but reserves screen zones so fixed
    captions never compete with the model, enlarges all instructional elements,
    replaces the cramped top-face measurement shot with a dedicated corner-detail
    view, and separates validation / parametric-edit information sequentially.
    """

    BASE_W = 7.10
    BASE_D = 4.20
    BASE_H = 1.10
    D6 = 0.75
    D10 = 1.18

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
        self.wait(0.35)

    def note(self, text, color=DARK, width=12.35, y=-3.72, font=26):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.70:
            label.scale_to_fit_width(width - 0.70)
        box = RoundedRectangle(
            width=width, height=0.88, corner_radius=0.12,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=color, stroke_width=1.45,
        )
        label.move_to(box)
        group = VGroup(box, label).move_to([0, y, 0])
        self.fixed(group)
        self.play(FadeIn(box, shift=UP*0.05), Write(label), run_time=0.75)
        self.wait(0.35)
        return group

    def small_callout(self, text, color=DARK, point=ORIGIN, width=4.6, font=25):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.50:
            label.scale_to_fit_width(width - 0.50)
        box = RoundedRectangle(
            width=width, height=0.74, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.985,
            stroke_color=color, stroke_width=1.35,
        )
        label.move_to(box)
        group = VGroup(box, label).move_to(point)
        self.fixed(group)
        return group

    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 31, BOLD, DARK)
        subtitle = self.text("CHAMFER / CHAFLÁN 3D · construcción y lógica paramétrica", 24, NORMAL, MID)
        title.to_corner(UL, buff=0.32)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.045)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.5).to_edge(UP, buff=1.13)
        phase_box = RoundedRectangle(
            width=5.85, height=0.68, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        ).to_corner(UR, buff=0.32)
        phase = self.text("01 · IDEA DEL CHAFLÁN", 23, BOLD, DARK).move_to(phase_box)
        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.45)
        self.wait(1.30)
        return {"group": group, "box": phase_box, "phase": phase}

    def parameter_card(self):
        rows = [
            ("Selection", "Edge1"),
            ("Method", "Distance + Angle"),
            ("Distance", "6 mm"),
            ("Angle", "45°"),
        ]
        head = self.text("CHAMFER PARAMETERS", 29, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 23, BOLD, DARK)
            val = self.text(right, 23, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=3.00, height=0.60, corner_radius=0.06,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.1,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.16)
            entries.add(VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.20))
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        panel = RoundedRectangle(
            width=5.55, height=content.height+0.62, corner_radius=0.12,
            fill_color=PAPER, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.35,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.30)
        group = VGroup(panel, content).move_to([4.90, -0.05, 0])
        self.fixed(group)
        return group

    def feature_tree(self):
        items = [
            ("Part1.ipt", DARK, BOLD),
            ("  Origin", MID, NORMAL),
            ("  Sketch1", MID, NORMAL),
            ("  Extrusion1", DARK, NORMAL),
            ("  Chamfer1   d = 6 mm · 45°", VALID, BOLD),
        ]
        lines = VGroup(*[
            self.text(t, 24, w, c) for t, c, w in items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        panel = RoundedRectangle(
            width=5.15, height=lines.height+0.65, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.99,
            stroke_color=DARK, stroke_width=1.2,
        )
        if lines.width > panel.width - 0.50:
            lines.scale_to_fit_width(panel.width - 0.50)
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.28)
        group = VGroup(panel, lines).move_to([-5.00, -0.25, 0])
        self.fixed(group)
        return group

    def validation_card(self, title, lines, color, center):
        head = self.text(title, 30, BOLD, color)
        body = VGroup()
        for i, line in enumerate(lines):
            t = self.text(line, 24 if i == 0 else 22, BOLD if i == 0 else NORMAL, DARK)
            if t.width > 4.30:
                t.scale_to_fit_width(4.30)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel = RoundedRectangle(
            width=5.00, height=max(1.85, content.height+0.52),
            corner_radius=0.11, fill_color=WHITE, fill_opacity=0.99,
            stroke_color=color, stroke_width=1.55,
        )
        if content.width > panel.width - 0.50:
            content.scale_to_fit_width(panel.width - 0.50)
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.26)
        return VGroup(panel, content).move_to(center)

    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 31, BOLD, DARK)
        title = self.text("CHAMFER / CHAFLÁN", 58, BOLD, BLACK_TEXT)
        sub = self.text("Eliminar una arista viva mediante una cara plana controlada", 32, NORMAL, MID)
        rule = Line(LEFT*5.95, RIGHT*5.95, color=BLACK, stroke_width=2.2)
        labels = ["SKETCH1", "EXTRUSION1", "EDGE1", "6 mm + 45°", "PREVIEW", "CHAMFER1"]
        pills = VGroup()
        for label in labels:
            t = self.text(label, 23, BOLD, DARK)
            box = RoundedRectangle(
                width=max(1.75, t.width+0.48), height=0.68, corner_radius=0.15,
                fill_color=PAPER, fill_opacity=1,
                stroke_color=DARK, stroke_width=1.25,
            )
            t.move_to(box)
            pills.add(VGroup(box, t))
        row1 = VGroup(*pills[:3]).arrange(RIGHT, buff=0.35)
        row2 = VGroup(*pills[3:]).arrange(RIGHT, buff=0.35)
        route = VGroup(row1, row2).arrange(DOWN, buff=0.22)
        group = VGroup(top, title, rule, sub, route).arrange(DOWN, buff=0.34)
        self.fit(group, 13.6, 6.6)
        self.fixed(group)
        self.play(FadeIn(top, shift=UP*0.08), run_time=0.65)
        self.play(Write(title), run_time=1.05)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(x) for x in row1], lag_ratio=0.12), run_time=1.15)
        self.play(LaggedStart(*[FadeIn(x) for x in row2], lag_ratio=0.12), run_time=1.15)
        self.wait(2.20)
        self.clear_fixed(group, run_time=0.60)

    def concept_problem(self, hud):
        self.set_phase(hud, 1, "IDEA DEL CHAFLÁN", DARK)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.05)
        corner = np.array([1.35, 0.85, 0])
        top_edge = Line([-4.25, 0.85, 0], corner, color=DARK, stroke_width=7)
        right_edge = Line([1.35, -2.35, 0], corner, color=DARK, stroke_width=7)
        sharp = Dot(corner, radius=0.115, color=REMOVE)
        call = self.small_callout("ARISTA VIVA", REMOVE, point=[-2.55, -1.45, 0], width=3.75)
        arrow = Arrow(call.get_top()+RIGHT*0.45, corner+LEFT*0.12+DOWN*0.10, buff=0.17, color=REMOVE, stroke_width=2.6)
        self.fixed(arrow)
        self.play(Create(top_edge), Create(right_edge), run_time=1.05)
        self.play(FadeIn(sharp), run_time=0.35)
        self.play(FadeIn(call), GrowArrow(arrow), run_time=0.80)
        note = self.note("El chaflán actúa sobre una ARISTA 3D existente; no crea el sólido base.", DARK)
        self.wait(1.80)
        self.clear_fixed(note)
        self.clear_fixed(call, 0.25)
        self.clear_fixed(arrow, 0.25)
        return VGroup(top_edge, right_edge, sharp), corner

    def concept_geometry(self, hud, sharp_geom, corner):
        self.set_phase(hud, 2, "DISTANCIA + ÁNGULO", SKETCH)
        c = 1.65
        a = corner + LEFT*c
        b = corner + DOWN*c
        cut = Line(a, b, color=VALID, stroke_width=9)
        tri = Polygon(a, corner, b, fill_color=REMOVE, fill_opacity=0.15, stroke_color=REMOVE, stroke_width=1.4)
        a_dot = Dot(a, radius=0.075, color=VALID)
        b_dot = Dot(b, radius=0.075, color=VALID)
        h_dim = DoubleArrow(a+DOWN*0.48, corner+DOWN*0.48, buff=0, color=SKETCH, stroke_width=2.5)
        v_dim = DoubleArrow(corner+RIGHT*0.48, b+RIGHT*0.48, buff=0, color=SKETCH, stroke_width=2.5)
        h_lab = self.text("6 mm", 30, BOLD, SKETCH).next_to(h_dim, DOWN, buff=0.10)
        v_lab = self.text("6 mm", 30, BOLD, SKETCH).rotate(PI/2).next_to(v_dim, RIGHT, buff=0.10)
        angle = Arc(radius=0.62, start_angle=3*PI/4, angle=PI/4, arc_center=a, color=SKETCH, stroke_width=3.5)
        angle_lab = self.text("45°", 29, BOLD, SKETCH).move_to(a+RIGHT*0.68+UP*0.42)
        planar = self.small_callout("CARA PLANA", VALID, point=[-2.15, -1.55, 0], width=3.75)
        self.play(FadeIn(tri), run_time=0.45)
        self.play(Create(h_dim), Write(h_lab), FadeIn(a_dot), run_time=0.90)
        self.play(Create(v_dim), Write(v_lab), FadeIn(b_dot), run_time=0.90)
        self.play(Create(cut), run_time=1.25, rate_func=smooth)
        self.play(Create(angle), Write(angle_lab), run_time=0.70)
        self.play(FadeIn(planar), run_time=0.50)
        note = self.note("A 45°, dos offsets iguales generan un bisel simétrico: DISTANCE = 6 mm.", VALID)
        self.wait(2.0)
        self.clear_fixed(note)
        self.clear_fixed(planar, 0.25)
        self.play(FadeOut(sharp_geom), FadeOut(tri), FadeOut(a_dot), FadeOut(b_dot), FadeOut(h_dim), FadeOut(v_dim), FadeOut(h_lab), FadeOut(v_lab), FadeOut(cut), FadeOut(angle), FadeOut(angle_lab), run_time=0.60)

    def sketch_base(self, hud):
        self.set_phase(hud, 3, "SKETCH1 · PERFIL CERRADO", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.00, run_time=0.85)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5.8)
        origin = Dot(ORIGIN, radius=0.075, color=REMOVE)
        h_axis = DashedLine([-w/2-0.40, 0, 0], [w/2+0.40, 0, 0], color=LIGHT, dash_length=0.14, stroke_width=1.7)
        v_axis = DashedLine([0, -d/2-0.28, 0], [0, d/2+0.28, 0], color=LIGHT, dash_length=0.14, stroke_width=1.7)
        status = self.small_callout("SKETCH1 · CLOSED PROFILE", SKETCH, point=[0, 2.75, 0], width=5.85)
        self.play(Create(h_axis), Create(v_axis), FadeIn(origin), run_time=0.65)
        self.play(Create(outline), run_time=1.55)
        self.play(FadeIn(status), run_time=0.55)
        note = self.note("PASO 1 · Dibuja el perfil 2D cerrado sobre el plano XY.", SKETCH)
        self.wait(1.55)
        self.clear_fixed(note)
        self.clear_fixed(status, 0.25)
        return outline, origin, h_axis, v_axis

    def constrain_sketch(self, hud, outline):
        self.set_phase(hud, 4, "COTAS + RESTRICCIONES", SKETCH)
        w, d = self.BASE_W, self.BASE_D
        d1 = DoubleArrow([-w/2, -d/2-0.48, 0], [w/2, -d/2-0.48, 0], buff=0, color=DARK, stroke_width=2.4)
        d2 = DoubleArrow([w/2+0.52, -d/2, 0], [w/2+0.52, d/2, 0], buff=0, color=DARK, stroke_width=2.4)
        l1 = self.text("80 mm", 29, BOLD, DARK).next_to(d1, DOWN, buff=0.08)
        l2 = self.text("50 mm", 29, BOLD, DARK).rotate(PI/2).next_to(d2, RIGHT, buff=0.08)
        fully = self.small_callout("FULLY CONSTRAINED", VALID, point=[-2.15, 2.74, 0], width=4.95)
        self.play(Create(d1), Write(l1), run_time=0.80)
        self.play(Create(d2), Write(l2), run_time=0.80)
        self.play(FadeIn(fully), run_time=0.55)
        note = self.note("PASO 2 · Fija 80 × 50 mm y la posición. Chamfer1 todavía NO existe.", DARK)
        self.wait(1.90)
        self.clear_fixed(note)
        self.clear_fixed(fully, 0.25)
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(l1), FadeOut(l2), run_time=0.38)

    def select_edge(self, hud, body):
        self.set_phase(hud, 6, "SELECCIONAR EDGE1", SKETCH)
        w, d, h = self.BASE_W, self.BASE_D, self.BASE_H
        edge = Line3D([w/2, d/2, 0], [w/2, d/2, h], color=SKETCH, thickness=0.080)
        p0 = Dot3D([w/2, d/2, 0], radius=0.090, color=SKETCH)
        p1 = Dot3D([w/2, d/2, h], radius=0.090, color=SKETCH)
        self.play(Create(edge), FadeIn(p0), FadeIn(p1), run_time=0.90)
        self.play(body.animate.shift(LEFT*1.15), edge.animate.shift(LEFT*1.15), p0.animate.shift(LEFT*1.15), p1.animate.shift(LEFT*1.15), run_time=0.90, rate_func=smooth)
        label = self.small_callout("EDGE1", SKETCH, point=[4.85, 1.65, 0], width=2.75)
        self.play(FadeIn(label), run_time=0.45)
        note = self.note("PASO 3 · Selecciona exactamente la arista que quieres biselar.", SKETCH)
        self.wait(1.75)
        self.clear_fixed(note)
        self.clear_fixed(label, 0.25)
        return edge, p0, p1

    def command_parameters(self, hud):
        self.set_phase(hud, 7, "MODIFY · CHAMFER", DARK)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.70)
        note = self.note("PASO 4A · 3D Model → Modify → Chamfer. Selection = Edge1.", DARK)
        self.wait(1.55)
        self.clear_fixed(note)
        method = self.small_callout("DISTANCE + ANGLE", SKETCH, point=[4.90, -2.62, 0], width=5.10)
        self.play(FadeIn(method), run_time=0.45)
        note = self.note("PASO 4B · Define Distance = 6 mm y Angle = 45°.", SKETCH)
        self.wait(1.70)
        self.clear_fixed(note)
        self.clear_fixed(method, 0.25)
        return card

    def distance_on_face(self, hud, body, edge, p0, p1, card):
        self.set_phase(hud, 8, "DETALLE DEL CORTE", SKETCH)
        self.play(FadeOut(card), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(body.animate.shift(RIGHT*1.15), edge.animate.shift(RIGHT*1.15), p0.animate.shift(RIGHT*1.15), p1.animate.shift(RIGHT*1.15), run_time=0.70, rate_func=smooth)
        self.play(FadeOut(body), FadeOut(edge), FadeOut(p0), FadeOut(p1), run_time=0.45)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.00, run_time=0.90)
        corner = np.array([2.30, 1.15, 0])
        top_edge = Line([-3.90, 1.15, 0], corner, color=DARK, stroke_width=7)
        right_edge = Line(corner, [2.30, -2.15, 0], color=DARK, stroke_width=7)
        c = 1.70
        a = corner + LEFT*c
        b = corner + DOWN*c
        removed = Polygon(a, corner, b, fill_color=REMOVE, fill_opacity=0.22, stroke_color=REMOVE, stroke_width=1.6)
        cut = Line(a, b, color=VALID, stroke_width=9)
        da = DoubleArrow(a+DOWN*0.52, corner+DOWN*0.52, buff=0, color=SKETCH, stroke_width=2.5)
        db = DoubleArrow(corner+RIGHT*0.52, b+RIGHT*0.52, buff=0, color=SKETCH, stroke_width=2.5)
        la = self.text("6 mm", 31, BOLD, SKETCH).next_to(da, DOWN, buff=0.09)
        lb = self.text("6 mm", 31, BOLD, SKETCH).rotate(PI/2).next_to(db, RIGHT, buff=0.09)
        angle = Arc(radius=0.64, start_angle=3*PI/4, angle=PI/4, arc_center=a, color=SKETCH, stroke_width=3.5)
        angle_lab = self.text("45°", 30, BOLD, SKETCH).move_to(a+RIGHT*0.72+UP*0.44)
        detail = self.small_callout("DETAIL A · CORNER", DARK, point=[-2.70, 2.20, 0], width=4.55)
        self.play(Create(top_edge), Create(right_edge), FadeIn(detail), run_time=0.95)
        self.play(FadeIn(removed), run_time=0.50)
        self.play(Create(da), Write(la), run_time=0.80)
        self.play(Create(db), Write(lb), run_time=0.80)
        self.play(Create(cut), run_time=1.15, rate_func=smooth)
        self.play(Create(angle), Write(angle_lab), run_time=0.70)
        note = self.note("PASO 5 · Antes de OK, verifica visualmente 6 mm y 45° en la esquina.", VALID)
        self.wait(2.05)
        self.clear_fixed(note)
        self.clear_fixed(detail, 0.25)
        return VGroup(top_edge, right_edge, removed, cut, da, db, la, lb, angle, angle_lab)

    def preview_3d(self, hud, body, edge, p0, p1, marks):
        self.set_phase(hud, 9, "PREVIEW 3D · FORMACIÓN", VALID)
        self.play(FadeOut(marks), run_time=0.45)
        self.move_camera(phi=64*DEGREES, theta=-46*DEGREES, zoom=1.10, run_time=1.55)
        self.play(FadeIn(body), FadeIn(edge), FadeIn(p0), FadeIn(p1), run_time=0.55)
        removed_prism = self.extruded_polygon(self.removed_corner_triangle(self.D6), self.BASE_H, REMOVE, 0.30, REMOVE)
        self.play(FadeIn(removed_prism), run_time=0.70)
        cut_call = self.small_callout("MATERIAL RETIRADO", REMOVE, point=[-4.70, -2.35, 0], width=4.45)
        self.play(FadeIn(cut_call), run_time=0.45)
        note = self.note("PASO 6A · El prisma triangular rojo es el volumen que desaparece.", REMOVE)
        self.wait(1.60)
        self.clear_fixed(note)
        self.clear_fixed(cut_call, 0.25)
        full_face = self.chamfer_face(self.D6, VALID, 0.88)
        small_face = self.chamfer_face(self.D6, VALID, 0.88, height=0.045)
        self.add(small_face)
        face_call = self.small_callout("NUEVA CARA PLANA", VALID, point=[-4.55, -2.35, 0], width=4.65)
        self.play(FadeIn(face_call), run_time=0.45)
        note = self.note("PASO 6B · La cara plana crece a lo largo de Edge1; NO es una superficie curva.", VALID)
        self.play(Transform(small_face, full_face), removed_prism.animate.set_opacity(0.08), edge.animate.set_opacity(0.18), p0.animate.set_opacity(0.18), p1.animate.set_opacity(0.18), run_time=3.20, rate_func=smooth)
        self.wait(1.20)
        self.clear_fixed(note)
        self.clear_fixed(face_call, 0.25)
        final = self.extruded_polygon(self.one_corner_chamfer_points(self.D6), self.BASE_H, STEEL, 0.97, DARK)
        self.play(FadeOut(body), FadeOut(removed_prism), FadeOut(small_face), FadeOut(edge), FadeOut(p0), FadeOut(p1), FadeIn(final), run_time=1.20)
        note = self.note("PREVIEW VÁLIDO · Edge1 desaparece y queda una cara plana de 6 mm × 45°.", VALID)
        self.wait(2.00)
        self.clear_fixed(note)
        return final

    def validate(self, hud, final):
        self.set_phase(hud, 10, "VALIDAR ANTES DE OK", DARK)
        self.play(final.animate.shift(UP*0.92), run_time=0.75, rate_func=smooth)
        ok_card = self.validation_card("VÁLIDO", ["6 mm · 45°", "cabe sobre ambas caras", "sin colisiones"], VALID, center=[-2.85, -2.68, 0])
        bad_card = self.validation_card("NO VÁLIDO", ["distancia excesiva", "consume una cara", "o cruza geometría"], REMOVE, center=[2.85, -2.68, 0])
        cards = VGroup(ok_card, bad_card)
        self.fixed(cards)
        self.play(FadeIn(ok_card[0]), Write(ok_card[1]), run_time=1.00)
        self.wait(0.70)
        self.play(FadeIn(bad_card[0]), Write(bad_card[1]), run_time=1.00)
        self.wait(2.20)
        self.clear_fixed(cards, 0.45)
        self.play(final.animate.shift(DOWN*0.92), run_time=0.70, rate_func=smooth)
        return final

    def parametric_edit(self, hud, final):
        self.set_phase(hud, 11, "OK · CHAMFER1 PARAMÉTRICO", VALID)
        self.play(final.animate.shift(RIGHT*1.55 + UP*0.48), run_time=0.80, rate_func=smooth)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.70)
        note = self.note("PASO 7A · OK crea Chamfer1 después de Extrusion1 en el árbol.", VALID)
        self.wait(1.70)
        self.clear_fixed(note)
        edit = self.small_callout("EDIT CHAMFER1 · 6 mm → 10 mm", SKETCH, point=[1.05, -2.72, 0], width=6.10, font=24)
        self.play(FadeIn(edit), run_time=0.55)
        bigger = self.extruded_polygon(self.one_corner_chamfer_points(self.D10), self.BASE_H, STEEL_DARK, 0.97, DARK).shift(RIGHT*1.55 + UP*0.48)
        self.play(Transform(final, bigger), run_time=2.00, rate_func=smooth)
        self.wait(1.55)
        self.clear_fixed(edit, 0.30)
        note = self.note("PASO 7B · La pieza se actualiza sin redibujar Sketch1: cambia solo el parámetro.", DARK)
        self.wait(2.00)
        self.clear_fixed(note)
        back = self.extruded_polygon(self.one_corner_chamfer_points(self.D6), self.BASE_H, STEEL, 0.97, DARK).shift(RIGHT*1.55 + UP*0.48)
        self.play(Transform(final, back), run_time=1.60, rate_func=smooth)
        self.wait(0.50)
        self.play(FadeOut(tree), final.animate.shift(LEFT*1.55 + DOWN*0.48), run_time=0.70, rate_func=smooth)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def final_summary(self, hud, final):
        self.set_phase(hud, 12, "INSPECCIÓN FINAL", DARK)
        line1 = self.text("Sketch1  →  Extrusion1  →  Edge1", 29, BOLD, DARK)
        line2 = self.text("6 mm + 45°  →  Preview  →  Chamfer1", 29, BOLD, DARK)
        text = VGroup(line1, line2).arrange(DOWN, buff=0.10)
        panel = RoundedRectangle(width=9.80, height=1.30, corner_radius=0.12, fill_color=WHITE, fill_opacity=0.985, stroke_color=DARK, stroke_width=1.25)
        text.move_to(panel)
        summary = VGroup(panel, text).move_to([0, -3.08, 0])
        self.fixed(summary)
        self.play(FadeIn(panel), Write(text), run_time=1.25)
        self.wait(1.75)
        self.begin_ambient_camera_rotation(rate=0.085)
        self.wait(5.2)
        self.stop_ambient_camera_rotation()
        self.wait(2.6)
