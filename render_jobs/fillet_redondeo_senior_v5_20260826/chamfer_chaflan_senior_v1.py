from __future__ import annotations

import numpy as np
from manim import *

from fillet_redondeo_senior_v5 import (
    InventorFilletRedondeoSeniorV5,
    BLACK_TEXT,
    DARK,
    MID,
    LIGHT,
    STEEL,
    STEEL_DARK,
    SKETCH,
    VALID,
    REMOVE,
    PAPER,
    WHITE,
    BOLD,
    NORMAL,
    TITLE,
    BODY,
    MICRO,
    READ,
    EXPLAIN,
    OBSERVE,
    smooth,
)


class InventorChamferChaflanSeniorV1(InventorFilletRedondeoSeniorV5):
    """Senior classroom lesson for Autodesk Inventor Chamfer / Chaflan.

    Same visual grammar as the approved Fillet lesson:
    white background, large readable typography, constrained 2D sketch, explicit
    2D-to-3D construction, isolated command parameters, progressive feature
    formation, validation, parametric edit and final orbit.

    Geometry modeled here: one vertical sharp edge of a rectangular prism is
    replaced by a planar 45-degree bevel. The top-view corner is cut by a straight
    segment whose two equal offsets represent a 6 mm x 45 deg chamfer.
    """

    BASE_W = 6.35
    BASE_D = 3.85
    BASE_H = 0.96
    D6 = 0.52
    D10 = 0.84

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def one_corner_chamfer_points(self, distance, z=0.0):
        w, d = self.BASE_W / 2, self.BASE_D / 2
        c = min(distance, self.BASE_W * 0.28, self.BASE_D * 0.40)
        pts = [
            [-w, -d, z],
            [ w, -d, z],
            [ w,  d-c, z],
            [ w-c, d, z],
            [-w,  d, z],
        ]
        return [np.array(p, dtype=float) for p in pts]

    def removed_corner_triangle(self, distance, z=0.0):
        w, d = self.BASE_W / 2, self.BASE_D / 2
        c = distance
        return [
            np.array([w, d-c, z], dtype=float),
            np.array([w, d, z], dtype=float),
            np.array([w-c, d, z], dtype=float),
        ]

    def chamfer_face(self, distance, color=VALID, opacity=0.82, height=None):
        h = self.BASE_H if height is None else height
        w, d = self.BASE_W / 2, self.BASE_D / 2
        c = distance
        a0 = np.array([w, d-c, 0.0])
        b0 = np.array([w-c, d, 0.0])
        a1 = a0 + OUT*h
        b1 = b0 + OUT*h
        return Polygon(
            a0, b0, b1, a1,
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=color,
            stroke_width=1.0,
        )

    # ------------------------------------------------------------------
    # HUD / cards
    # ------------------------------------------------------------------
    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 28, BOLD, DARK)
        subtitle = self.text("CHAMFER / CHAFLÁN 3D · construcción y lógica paramétrica", 21, NORMAL, MID)
        title.to_corner(UL, buff=0.34)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.05)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.4).to_edge(UP, buff=1.08)
        phase_box = RoundedRectangle(
            width=5.65,
            height=0.62,
            corner_radius=0.11,
            fill_color=WHITE,
            fill_opacity=0.99,
            stroke_color=DARK,
            stroke_width=1.2,
        ).to_corner(UR, buff=0.34)
        phase = self.text("01 · IDEA DEL CHAFLÁN", 20, BOLD, DARK).move_to(phase_box)
        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.55)
        self.wait(READ)
        return {"group": group, "box": phase_box, "phase": phase}

    def parameter_card(self):
        rows = [
            ("Selection", "Edge1"),
            ("Type", "Distance + Angle"),
            ("Distance", "6 mm"),
            ("Angle", "45 deg"),
        ]
        head = self.text("CHAMFER PARAMETERS", 25, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 20, BOLD, DARK)
            val = self.text(right, 20, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.75,
                height=0.52,
                corner_radius=0.05,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_color=MID,
                stroke_width=1.0,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.14)
            entries.add(VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.18))
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel = RoundedRectangle(
            width=5.45,
            height=content.height+0.55,
            corner_radius=0.11,
            fill_color=PAPER,
            fill_opacity=0.99,
            stroke_color=DARK,
            stroke_width=1.25,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.28)
        group = VGroup(panel, content).move_to([5.05, -0.05, 0])
        self.fixed(group)
        return group

    def feature_tree(self):
        items = [
            ("Part1.ipt", DARK, BOLD),
            ("Origin", MID, NORMAL),
            ("Sketch1", MID, NORMAL),
            ("Extrusion1", DARK, NORMAL),
            ("Chamfer1   d = 6 mm", VALID, BOLD),
        ]
        lines = VGroup(*[self.text(t, 20, w, c) for t, c, w in items]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12
        )
        panel = RoundedRectangle(
            width=4.55,
            height=lines.height+0.55,
            corner_radius=0.09,
            fill_color=WHITE,
            fill_opacity=0.98,
            stroke_color=DARK,
            stroke_width=1.1,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.26)
        group = VGroup(panel, lines).move_to([-5.35, -0.40, 0])
        self.fixed(group)
        return group

    def validation_card(self, title, lines, color, center):
        head = self.text(title, 27, BOLD, color)
        body = VGroup()
        for i, line in enumerate(lines):
            t = self.text(line, 21 if i == 0 else 19, BOLD if i == 0 else NORMAL, DARK)
            if t.width > 4.05:
                t.scale_to_fit_width(4.05)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        if content.width > 4.15:
            content.scale_to_fit_width(4.15)
        panel = RoundedRectangle(
            width=4.75,
            height=max(1.62, content.height+0.48),
            corner_radius=0.10,
            fill_color=WHITE,
            fill_opacity=0.985,
            stroke_color=color,
            stroke_width=1.4,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.24)
        return VGroup(panel, content).move_to(center)

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 28, BOLD, DARK)
        title = self.text("CHAMFER / CHAFLÁN", TITLE, BOLD)
        sub = self.text("De una arista viva a una cara plana de transición", 30, NORMAL, MID)
        rule = Line(LEFT*5.85, RIGHT*5.85, color=BLACK, stroke_width=2)
        route = self.text(
            "SKETCH  →  EXTRUDE  →  EDGE  →  DISTANCE + ANGLE  →  PREVIEW  →  CHAMFER1",
            23,
            BOLD,
            DARK,
        )
        group = VGroup(top, title, rule, sub, route).arrange(DOWN, buff=0.34)
        self.fit(group, 13.8, 6.2)
        self.fixed(group)
        self.play(FadeIn(top, shift=UP*0.08), run_time=0.75)
        self.play(Write(title), run_time=1.15)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(Write(route), run_time=1.35)
        self.wait(EXPLAIN)
        self.clear_fixed(group, run_time=0.60)

    def concept_problem(self, hud):
        self.set_phase(hud, 1, "IDEA DEL CHAFLÁN", DARK)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.02)
        corner = np.array([1.55, 0.90, 0])
        top_edge = Line([-3.35, 0.90, 0], corner, color=DARK, stroke_width=6)
        right_edge = Line([1.55, -2.05, 0], corner, color=DARK, stroke_width=6)
        sharp = Dot(corner, radius=0.095, color=REMOVE)
        call = self.small_callout("ARISTA VIVA", REMOVE, point=[-2.55, -1.55, 0], width=3.45)
        arrow = Arrow(call.get_top(), corner+LEFT*0.10+DOWN*0.10, buff=0.16, color=REMOVE, stroke_width=2.2)
        self.fixed(arrow)
        self.play(Create(top_edge), Create(right_edge), FadeIn(sharp), run_time=1.05)
        self.play(FadeIn(call), GrowArrow(arrow), run_time=0.85)
        note = self.note("Chamfer modifica una ARISTA existente; la reemplaza por una cara plana.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(call, 0.25)
        self.clear_fixed(arrow, 0.25)
        return VGroup(top_edge, right_edge, sharp), corner

    def concept_geometry(self, hud, sharp_geom, corner):
        self.set_phase(hud, 2, "DISTANCIA + ÁNGULO", SKETCH)
        c = 1.20
        a = corner + LEFT*c
        b = corner + DOWN*c
        cut = Line(a, b, color=VALID, stroke_width=8)
        a_dot = Dot(a, radius=0.065, color=VALID)
        b_dot = Dot(b, radius=0.065, color=VALID)
        h_dim = DoubleArrow(a+DOWN*0.38, corner+DOWN*0.38, buff=0, color=SKETCH, stroke_width=2.1)
        v_dim = DoubleArrow(corner+RIGHT*0.38, b+RIGHT*0.38, buff=0, color=SKETCH, stroke_width=2.1)
        h_lab = self.text("6 mm", 25, BOLD, SKETCH).next_to(h_dim, DOWN, buff=0.08)
        v_lab = self.text("6 mm", 25, BOLD, SKETCH).rotate(PI/2).next_to(v_dim, RIGHT, buff=0.08)
        angle = Arc(radius=0.52, start_angle=PI, angle=PI/4, arc_center=b, color=SKETCH, stroke_width=3)
        angle_lab = self.text("45°", 24, BOLD, SKETCH).move_to(b+LEFT*0.75+UP*0.33)
        planar = self.small_callout("TRANSICIÓN PLANA", VALID, point=[-2.20, -1.72, 0], width=4.55)

        self.play(FadeIn(a_dot), FadeIn(b_dot), Create(h_dim), Write(h_lab), run_time=0.85)
        self.play(Create(v_dim), Write(v_lab), run_time=0.85)
        self.play(Create(cut), run_time=1.15, rate_func=smooth)
        self.play(Create(angle), Write(angle_lab), run_time=0.65)
        self.play(FadeIn(planar), run_time=0.55)
        note = self.note("A 45°, distancias iguales producen un bisel simétrico sobre la esquina.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(planar, 0.25)
        self.play(
            FadeOut(sharp_geom), FadeOut(a_dot), FadeOut(b_dot), FadeOut(h_dim), FadeOut(v_dim),
            FadeOut(h_lab), FadeOut(v_lab), FadeOut(cut), FadeOut(angle), FadeOut(angle_lab),
            run_time=0.55,
        )

    def sketch_base(self, hud):
        self.set_phase(hud, 3, "SKETCH1 · PERFIL", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.02, run_time=0.85)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5.2)
        origin = Dot(ORIGIN, radius=0.065, color=REMOVE)
        h_axis = DashedLine([-w/2-0.35, 0, 0], [w/2+0.35, 0, 0], color=LIGHT, dash_length=0.12, stroke_width=1.5)
        v_axis = DashedLine([0, -d/2-0.25, 0], [0, d/2+0.25, 0], color=LIGHT, dash_length=0.12, stroke_width=1.5)
        status = self.small_callout("Sketch1 · CLOSED PROFILE", SKETCH, point=[0, 2.55, 0], width=5.25)
        self.play(Create(h_axis), Create(v_axis), FadeIn(origin), run_time=0.65)
        self.play(Create(outline), run_time=1.45)
        self.play(FadeIn(status), run_time=0.55)
        note = self.note("Paso 1: dibuja un perfil 2D CERRADO sobre el plano XY.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(status, 0.25)
        return outline, origin, h_axis, v_axis

    def constrain_sketch(self, hud, outline):
        self.set_phase(hud, 4, "COTAS + RESTRICCIONES", SKETCH)
        w, d = self.BASE_W, self.BASE_D
        d1 = DoubleArrow([-w/2, -d/2-0.48, 0], [w/2, -d/2-0.48, 0], buff=0, color=DARK, stroke_width=2.2)
        d2 = DoubleArrow([w/2+0.50, -d/2, 0], [w/2+0.50, d/2, 0], buff=0, color=DARK, stroke_width=2.2)
        l1 = self.text("80 mm", 24, BOLD).next_to(d1, DOWN, buff=0.08)
        l2 = self.text("50 mm", 24, BOLD).rotate(PI/2).next_to(d2, RIGHT, buff=0.08)
        fully = self.small_callout("FULLY CONSTRAINED", VALID, point=[-2.15, 2.58, 0], width=4.45)
        self.play(Create(d1), Write(l1), run_time=0.75)
        self.play(Create(d2), Write(l2), run_time=0.75)
        self.play(FadeIn(fully), run_time=0.55)
        note = self.note("Paso 2: fija tamaño y posición. Todavía NO existe Chamfer1.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(fully, 0.25)
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(l1), FadeOut(l2), run_time=0.35)

    def select_edge(self, hud, body):
        self.set_phase(hud, 6, "SELECCIONAR EDGE1", SKETCH)
        w, d, h = self.BASE_W, self.BASE_D, self.BASE_H
        edge = Line3D([w/2, d/2, 0], [w/2, d/2, h], color=SKETCH, thickness=0.065)
        p0 = Dot3D([w/2, d/2, 0], radius=0.075, color=SKETCH)
        p1 = Dot3D([w/2, d/2, h], radius=0.075, color=SKETCH)
        self.play(Create(edge), FadeIn(p0), FadeIn(p1), run_time=0.85)
        self.play(body.animate.shift(LEFT*1.00), edge.animate.shift(LEFT*1.00), p0.animate.shift(LEFT*1.00), p1.animate.shift(LEFT*1.00), run_time=0.85)
        label = self.small_callout("EDGE1", SKETCH, point=[4.75, 1.70, 0], width=2.4)
        self.play(FadeIn(label), run_time=0.45)
        note = self.note("Paso 3: selecciona la arista 3D que deseas biselar.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(label, 0.25)
        return edge, p0, p1

    def command_parameters(self, hud):
        self.set_phase(hud, 7, "MODIFY · CHAMFER", DARK)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.65)
        note = self.note("Paso 4: 3D Model → Modify → Chamfer. Selecciona Edge1.", DARK)
        self.wait(READ)
        self.clear_fixed(note)
        method = self.small_callout("DISTANCE + ANGLE", DARK, point=[5.05, -2.45, 0], width=4.55)
        self.play(FadeIn(method), run_time=0.45)
        note = self.note("Define Distance = 6 mm y Angle = 45°. La vista previa debe ser plana.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(method, 0.25)
        return card

    def distance_on_face(self, hud, body, edge, p0, p1, card):
        self.set_phase(hud, 8, "COMPROBAR CORTE", SKETCH)
        self.play(FadeOut(card), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(body.animate.shift(RIGHT*1.00), edge.animate.shift(RIGHT*1.00), p0.animate.shift(RIGHT*1.00), p1.animate.shift(RIGHT*1.00), run_time=0.70)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.04, run_time=1.45)

        w, d = self.BASE_W/2, self.BASE_D/2
        c = self.D6
        a = np.array([w-c, d, self.BASE_H+0.02])
        b = np.array([w, d-c, self.BASE_H+0.02])
        corner = np.array([w, d, self.BASE_H+0.02])
        removed = Polygon(
            a, corner, b,
            fill_color=REMOVE, fill_opacity=0.22,
            stroke_color=REMOVE, stroke_width=1.4,
        )
        cut = Line(a, b, color=VALID, stroke_width=7)
        da = DoubleArrow(a+DOWN*0.34, corner+DOWN*0.34, buff=0, color=SKETCH, stroke_width=2.0)
        db = DoubleArrow(corner+RIGHT*0.34, b+RIGHT*0.34, buff=0, color=SKETCH, stroke_width=2.0)
        la = self.text("6 mm", 23, BOLD, SKETCH).next_to(da, DOWN, buff=0.06)
        lb = self.text("6 mm", 23, BOLD, SKETCH).rotate(PI/2).next_to(db, RIGHT, buff=0.06)

        self.play(FadeIn(removed), run_time=0.55)
        self.play(Create(da), Write(la), run_time=0.70)
        self.play(Create(db), Write(lb), run_time=0.70)
        self.play(Create(cut), run_time=1.15, rate_func=smooth)
        note = self.note("Paso 5: comprueba dónde termina el bisel antes de aceptar el comando.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return VGroup(removed, cut, da, db, la, lb)

    def preview_3d(self, hud, body, edge, p0, p1, marks):
        self.set_phase(hud, 9, "PREVIEW 3D", VALID)
        self.play(FadeOut(marks), run_time=0.35)
        self.move_camera(phi=64*DEGREES, theta=-46*DEGREES, zoom=1.05, run_time=1.55)

        removed_prism = self.extruded_polygon(
            self.removed_corner_triangle(self.D6), self.BASE_H,
            REMOVE, 0.27, REMOVE,
        )
        self.play(FadeIn(removed_prism), run_time=0.65)
        note = self.note("Paso 6A: el prisma triangular rojo es el material que se retira.", REMOVE)
        self.wait(READ)
        self.clear_fixed(note)

        full_face = self.chamfer_face(self.D6, VALID, 0.82)
        small_face = self.chamfer_face(self.D6, VALID, 0.82, height=0.04)
        self.add(small_face)
        note = self.note("Paso 6B: una CARA PLANA crece a lo largo de Edge1; no aparece una superficie curva.", VALID)
        self.play(
            Transform(small_face, full_face),
            removed_prism.animate.set_opacity(0.10),
            edge.animate.set_opacity(0.22),
            p0.animate.set_opacity(0.22),
            p1.animate.set_opacity(0.22),
            run_time=3.10,
            rate_func=smooth,
        )
        self.wait(READ)
        self.clear_fixed(note)

        final = self.extruded_polygon(
            self.one_corner_chamfer_points(self.D6), self.BASE_H,
            STEEL, 0.96, DARK,
        )
        self.play(
            FadeOut(body), FadeOut(removed_prism), FadeOut(small_face),
            FadeOut(edge), FadeOut(p0), FadeOut(p1), FadeIn(final),
            run_time=1.15,
        )
        note = self.note("Preview válido: Edge1 desaparece y queda una transición plana de 6 mm × 45°.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return final

    def validate(self, hud, final):
        self.set_phase(hud, 10, "VALIDAR ANTES DE OK", DARK)
        self.play(final.animate.shift(UP*0.82), run_time=0.70, rate_func=smooth)

        ok_card = self.validation_card(
            "VÁLIDO",
            ["d = 6 mm · 45°", "cabe sobre ambas caras", "bisel sin colisiones"],
            VALID,
            center=[-3.05, -2.75, 0],
        )
        bad_card = self.validation_card(
            "NO VÁLIDO",
            ["distancia excesiva", "consume una cara", "o cruza otra geometría"],
            REMOVE,
            center=[3.05, -2.75, 0],
        )
        cards = VGroup(ok_card, bad_card)
        self.fixed(cards)
        self.play(FadeIn(ok_card[0]), Write(ok_card[1]), run_time=0.95)
        self.wait(0.55)
        self.play(FadeIn(bad_card[0]), Write(bad_card[1]), run_time=0.95)
        self.wait(EXPLAIN)
        self.clear_fixed(cards, 0.45)
        self.play(final.animate.shift(DOWN*0.82), run_time=0.65, rate_func=smooth)
        return final

    def parametric_edit(self, hud, final):
        self.set_phase(hud, 11, "OK · CHAMFER1", VALID)
        self.play(final.animate.shift(RIGHT*1.22 + UP*0.48), run_time=0.75, rate_func=smooth)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.65)
        note = self.note("Paso 7: OK crea Chamfer1 después de Extrusion1 en el árbol paramétrico.", VALID)
        self.wait(READ)
        self.clear_fixed(note)

        edit = self.small_callout(
            "EDIT CHAMFER1  ·  d: 6 mm  →  10 mm",
            SKETCH,
            point=[0.35, -2.75, 0],
            width=6.45,
        )
        self.play(FadeIn(edit), run_time=0.55)
        bigger = self.extruded_polygon(
            self.one_corner_chamfer_points(self.D10), self.BASE_H,
            STEEL_DARK, 0.96, DARK,
        ).shift(RIGHT*1.22 + UP*0.48)
        self.play(Transform(final, bigger), run_time=1.90, rate_func=smooth)
        self.wait(READ)
        self.clear_fixed(edit, 0.30)

        note = self.note("La pieza se actualiza sin redibujar Sketch1: solo cambia el parámetro del chaflán.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)

        back = self.extruded_polygon(
            self.one_corner_chamfer_points(self.D6), self.BASE_H,
            STEEL, 0.96, DARK,
        ).shift(RIGHT*1.22 + UP*0.48)
        self.play(Transform(final, back), run_time=1.55, rate_func=smooth)
        self.wait(MICRO)
        self.play(
            FadeOut(tree),
            final.animate.shift(LEFT*1.22 + DOWN*0.48),
            run_time=0.65,
            rate_func=smooth,
        )
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def final_summary(self, hud, final):
        self.set_phase(hud, 12, "INSPECCIÓN FINAL", DARK)
        summary = self.text(
            "Sketch1  →  Extrusion1  →  Edge1  →  6 mm + 45°  →  Preview  →  Chamfer1",
            23,
            BOLD,
            DARK,
        ).to_edge(DOWN, buff=0.34)
        self.fit(summary, 13.9, 0.7)
        self.fixed(summary)
        self.play(Write(summary), run_time=1.20)
        self.wait(READ)
        self.begin_ambient_camera_rotation(rate=0.095)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()
        self.wait(OBSERVE)

    def construct(self):
        self.camera.background_color = WHITE
        self.opening()
        hud = self.hud()
        sharp, corner = self.concept_problem(hud)
        self.concept_geometry(hud, sharp, corner)
        outline, origin, h_axis, v_axis = self.sketch_base(hud)
        self.constrain_sketch(hud, outline)
        body = self.extrude_base(hud, outline, origin, h_axis, v_axis)
        edge, p0, p1 = self.select_edge(hud, body)
        card = self.command_parameters(hud)
        marks = self.distance_on_face(hud, body, edge, p0, p1, card)
        final = self.preview_3d(hud, body, edge, p0, p1, marks)
        final = self.validate(hud, final)
        final = self.parametric_edit(hud, final)
        self.final_summary(hud, final)
