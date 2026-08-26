from __future__ import annotations

import numpy as np
from manim import *

from hole_agujero_senior_v3 import InventorHoleAgujeroSeniorV3
from fillet_redondeo_senior_v5 import (
    BLACK_TEXT, DARK, MID, LIGHT, STEEL, STEEL_DARK,
    SKETCH, VALID, REMOVE, PAPER, WHITE,
    BOLD, NORMAL, TITLE, MICRO, READ, EXPLAIN, smooth,
)


class InventorEmbossRepujadoSeniorV1(InventorHoleAgujeroSeniorV3):
    """Full senior classroom lesson for Autodesk Inventor Emboss / Repujado.

    Consolidated visual contract inherited from the latest Fillet / Chamfer /
    Hole family: white background, black institutional typography, large labels,
    Sketch -> Feature causality, restrained accent colors, 2D/3D camera changes,
    explicit parameter panel, validation before OK, parametric edit and final orbit.

    Focus operation:
        Sketch1 rectangle 90 x 52 mm -> Extrusion1 9 mm -> Top Face ->
        Sketch2 centered hexagon 24 mm across flats -> Emboss from Face ->
        Depth 3 mm -> Emboss1.

    The lesson also contrasts Emboss and Engrave in section view so students can
    distinguish adding shallow relief from cutting a recessed mark.
    """

    BASE_W = 7.20
    BASE_D = 4.30
    BASE_H = 1.05
    PROFILE_R = 1.00
    EMBOSS_DEPTH = 0.38
    EMBOSS_DEPTH_EDIT = 0.66
    PANEL_CLEARANCE = 1.10

    # ------------------------------------------------------------------
    # Fixed-frame composition helpers
    # ------------------------------------------------------------------
    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 31, BOLD, DARK)
        subtitle = self.text("EMBOSS / REPUJADO 3D · relieve paramétrico", 24, NORMAL, MID)
        title.to_corner(UL, buff=0.32)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.045)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.5).to_edge(UP, buff=1.13)

        phase_box = RoundedRectangle(
            width=5.85, height=0.68, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        ).to_corner(UR, buff=0.32)
        phase = self.text("01 · IDEA DEL REPUJADO", 23, BOLD, DARK).move_to(phase_box)

        if subtitle.get_right()[0] > phase_box.get_left()[0] - 0.18:
            raise ValueError("HUD subtitle overlaps phase box")

        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.55)
        self.wait(READ)
        return {"group": group, "box": phase_box, "phase": phase}

    def parameter_card(self):
        rows = [
            ("Profile", "Sketch2 Region"),
            ("Mode", "Emboss from Face"),
            ("Depth", "3 mm"),
            ("Direction", "Outward"),
            ("Taper", "0 deg"),
        ]
        head = self.text("EMBOSS PARAMETERS", 28, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 21, BOLD, DARK)
            val = self.text(right, 20, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.95, height=0.55, corner_radius=0.05,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.0,
            )
            if val.width > field.width - 0.28:
                val.scale_to_fit_width(field.width - 0.28)
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.14)
            row = VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.18)
            entries.add(row)
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.23)
        panel = RoundedRectangle(
            width=5.45, height=content.height+0.56, corner_radius=0.11,
            fill_color=PAPER, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.27)
        group = VGroup(panel, content).move_to([4.92, -0.16, 0])
        self.fixed(group)
        if group.get_right()[0] > 7.88:
            raise ValueError("Emboss parameter card exceeds right safe area")
        return group

    def feature_tree(self):
        items = [
            ("Part1.ipt", DARK, BOLD),
            ("Origin", MID, NORMAL),
            ("Sketch1", MID, NORMAL),
            ("Extrusion1   9 mm", DARK, NORMAL),
            ("Sketch2   Hexagon 24 mm", SKETCH, NORMAL),
            ("Emboss1   +3 mm", VALID, BOLD),
        ]
        lines = VGroup(*[
            self.text(t, 21, w, c) for t, c, w in items
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

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def profile_hexagon(self, color=SKETCH, z=0.0, stroke_width=5.0):
        h = RegularPolygon(n=6, radius=self.PROFILE_R, color=color, stroke_width=stroke_width)
        h.rotate(30*DEGREES)
        h.shift(OUT*z)
        return h

    def emboss_badge(self, depth=None, color=STEEL_DARK, opacity=0.98):
        d = self.EMBOSS_DEPTH if depth is None else depth
        badge = Cylinder(
            radius=self.PROFILE_R,
            height=d,
            resolution=(6, 12),
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=DARK,
            stroke_width=0.85,
        )
        badge.rotate(30*DEGREES, axis=OUT)
        badge.move_to([0, 0, self.BASE_H + d/2])
        return badge

    def embossed_body(self, depth=None, body_color=STEEL):
        return VGroup(self.base_body(body_color), self.emboss_badge(depth))

    def profile_plan(self):
        plate = RoundedRectangle(
            width=self.BASE_W, height=self.BASE_D, corner_radius=0.10,
            fill_color=PAPER, fill_opacity=1,
            stroke_color=DARK, stroke_width=3.4,
        )
        hexagon = self.profile_hexagon(SKETCH, 0, 5.2)
        center = Dot(ORIGIN, radius=0.07, color=REMOVE)
        return VGroup(plate, hexagon, center)

    # ------------------------------------------------------------------
    # Narrative sections
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 30, BOLD, DARK)
        title = self.text("EMBOSS / REPUJADO", TITLE, BOLD)
        sub = self.text("Crear un relieve o grabado superficial controlado desde un croquis", 30, NORMAL, MID)
        rule = Line(LEFT*6.15, RIGHT*6.15, color=BLACK, stroke_width=2)
        route1 = self.text("SKETCH1  →  EXTRUSION1  →  TOP FACE  →  SKETCH2", 25, BOLD, DARK)
        route2 = self.text("CLOSED PROFILE  →  +3 mm  →  EMBOSS FROM FACE  →  EMBOSS1", 26, BOLD, VALID)
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
        self.set_phase(hud, 1, "IDEA DEL REPUJADO", DARK)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)

        plate = RoundedRectangle(
            width=8.0, height=4.45, corner_radius=0.12,
            fill_color=PAPER, fill_opacity=1,
            stroke_color=DARK, stroke_width=4.0,
        )
        hexagon = RegularPolygon(n=6, radius=1.05, color=SKETCH, stroke_width=6).rotate(30*DEGREES)
        up = Arrow([2.25, -0.55, 0], [2.25, 1.15, 0], buff=0.04, color=VALID, stroke_width=3)
        lab1 = self.text("PERFIL CERRADO", 25, BOLD, SKETCH).next_to(hexagon, DOWN, buff=0.27)
        lab2 = self.text("+ PROFUNDIDAD", 25, BOLD, VALID).next_to(up, RIGHT, buff=0.18)
        self.fixed(VGroup(lab1, lab2))

        self.play(FadeIn(plate), run_time=0.55)
        self.play(Create(hexagon), Write(lab1), run_time=0.90)
        self.play(GrowArrow(up), Write(lab2), run_time=0.75)
        note = self.note_big(
            "Emboss necesita una REGIÓN CERRADA sobre una cara y una PROFUNDIDAD de relieve.",
            DARK,
        )
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(VGroup(plate, hexagon, up)), run_time=0.40)
        self.remove_fixed_in_frame_mobjects(lab1, lab2)
        self.remove(lab1, lab2)

    def sketch1(self, hud):
        self.set_phase(hud, 2, "SKETCH1 · BASE", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.70)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5.5)
        h_axis = DashedLine([-w/2-0.35, 0, 0], [w/2+0.35, 0, 0], color=LIGHT, dash_length=0.12, stroke_width=1.5)
        v_axis = DashedLine([0, -d/2-0.30, 0], [0, d/2+0.30, 0], color=LIGHT, dash_length=0.12, stroke_width=1.5)
        origin = Dot(ORIGIN, radius=0.07, color=REMOVE)
        dim_w = DoubleArrow([-w/2, -d/2-0.50, 0], [w/2, -d/2-0.50, 0], buff=0, color=DARK, stroke_width=2.1)
        dim_d = DoubleArrow([w/2+0.55, -d/2, 0], [w/2+0.55, d/2, 0], buff=0, color=DARK, stroke_width=2.1)
        lab_w = self.text("90 mm", 27, BOLD, DARK).next_to(dim_w, DOWN, buff=0.08)
        lab_d = self.text("52 mm", 27, BOLD, DARK).next_to(dim_d, RIGHT, buff=0.08).rotate(90*DEGREES)
        dims = VGroup(dim_w, dim_d, lab_w, lab_d)
        self.fixed(VGroup(dims))
        self.play(Create(h_axis), Create(v_axis), FadeIn(origin), run_time=0.55)
        self.play(Create(outline), run_time=1.20)
        self.play(Create(dim_w), Write(lab_w), Create(dim_d), Write(lab_d), run_time=0.95)
        note = self.note_big("PASO 1 · Croquis completamente restringido: 90 × 52 mm.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.remove_fixed_in_frame_mobjects(dims)
        self.remove(dims)
        self.play(FadeOut(VGroup(outline, h_axis, v_axis, origin)), run_time=0.40)

    def extrusion1(self, hud):
        self.set_phase(hud, 3, "EXTRUSION1 · 9 mm", DARK)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.90, run_time=1.00)
        base = self.base_body(STEEL)
        self.play(FadeIn(base, shift=OUT*0.06), run_time=1.05)
        note = self.note_big("PASO 2 · Extrude el rectángulo 9 mm para obtener la pieza base.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return base

    def top_face_sketch2(self, hud, base):
        self.set_phase(hud, 4, "TOP FACE · SKETCH2", SKETCH)
        note = self.note_big("PASO 3 · Selecciona la cara superior y crea Sketch2.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.95)
        self.play(FadeOut(base), run_time=0.35)

        plan = self.profile_plan()
        self.play(FadeIn(plan[0]), run_time=0.50)
        self.play(Create(plan[1]), FadeIn(plan[2]), run_time=1.00)

        flat = 2*self.PROFILE_R*np.cos(PI/6)
        arrow = DoubleArrow([-flat/2, -1.43, 0], [flat/2, -1.43, 0], buff=0, color=DARK, stroke_width=2.1)
        label = self.text("24 mm across flats", 26, BOLD, DARK).next_to(arrow, DOWN, buff=0.12)
        axis_note = self.small_callout("CENTERED ON ORIGIN", SKETCH, point=[-3.95, 1.38, 0], width=4.25)
        self.fixed(VGroup(arrow, label))
        self.play(Create(arrow), Write(label), FadeIn(axis_note), run_time=0.85)
        note = self.note_big("PASO 4 · Dibuja un hexágono cerrado y céntralo antes de Finish Sketch.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(axis_note, 0.25)
        self.remove_fixed_in_frame_mobjects(arrow, label)
        self.remove(arrow, label)
        return plan

    def command_and_parameters(self, hud, plan):
        self.set_phase(hud, 5, "3D MODEL · EMBOSS", DARK)
        cmd = self.small_callout("3D MODEL  >  CREATE  >  EMBOSS", DARK, point=[-3.85, 1.60, 0], width=5.35)
        self.play(FadeIn(cmd), run_time=0.55)
        note = self.note_big("PASO 5 · Finish Sketch y abre el comando Emboss.", DARK)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(cmd, 0.25)

        self.set_phase(hud, 6, "PARÁMETROS", DARK)
        self.play(plan.animate.shift(LEFT*self.PANEL_CLEARANCE), run_time=0.60, rate_func=smooth)
        card = self.parameter_card()
        self.play(FadeIn(card[0]), Write(card[1]), run_time=1.10)
        note = self.note_big("PASO 6 · Profile = Sketch2 · Emboss from Face · Depth = 3 mm · Outward.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return card

    def preview_3d(self, hud, plan, card):
        self.set_phase(hud, 7, "PREVIEW · +3 mm", VALID)
        self.play(FadeOut(card), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(FadeOut(plan), run_time=0.35)

        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.88, run_time=1.00)
        base = self.base_body(STEEL)
        sketch = self.profile_hexagon(VALID, self.BASE_H+0.018, 6.5)
        preview = self.emboss_badge(self.EMBOSS_DEPTH, VALID, 0.22)
        self.play(FadeIn(base), run_time=0.50)
        self.play(Create(sketch), run_time=0.80)
        self.play(FadeIn(preview), run_time=1.20)
        note = self.note_big("PASO 7 · El preview debe elevar el perfil desde la cara, no crear un sólido separado.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(sketch), run_time=0.25)
        return VGroup(base, preview)

    def section_emboss_vs_engrave(self, hud, preview_group):
        self.set_phase(hud, 8, "EMBOSS vs ENGRAVE", DARK)
        self.play(FadeOut(preview_group), run_time=0.35)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=0.80)

        surf_y = -0.30
        base_l = Rectangle(width=5.55, height=1.05, stroke_color=DARK, stroke_width=2.5, fill_color=STEEL, fill_opacity=0.45).move_to([-3.35, surf_y-0.52, 0])
        raise_l = Rectangle(width=1.75, height=0.65, stroke_color=VALID, stroke_width=3.2, fill_color=VALID, fill_opacity=0.14).next_to(base_l, UP, buff=0).shift(UP*0.005)
        base_r = Rectangle(width=5.55, height=1.05, stroke_color=DARK, stroke_width=2.5, fill_color=STEEL, fill_opacity=0.45).move_to([3.35, surf_y-0.52, 0])
        recess = Rectangle(width=1.75, height=0.62, stroke_color=REMOVE, stroke_width=3.2, fill_color=WHITE, fill_opacity=1).move_to([3.35, surf_y-0.28, 0])
        emb = self.text("EMBOSS  +3 mm", 29, BOLD, VALID).next_to(base_l, UP, buff=1.02)
        eng = self.text("ENGRAVE  -3 mm", 29, BOLD, REMOVE).next_to(base_r, UP, buff=1.02)
        plus = Arrow([-4.80, 0.00, 0], [-4.80, 0.76, 0], buff=0, color=VALID, stroke_width=2.7)
        minus = Arrow([4.80, 0.05, 0], [4.80, -0.72, 0], buff=0, color=REMOVE, stroke_width=2.7)
        self.fixed(VGroup(emb, eng, plus, minus))

        self.play(FadeIn(base_l), FadeIn(base_r), run_time=0.55)
        self.play(FadeIn(raise_l), FadeIn(recess), run_time=0.75)
        self.play(Write(emb), Write(eng), GrowArrow(plus), GrowArrow(minus), run_time=0.90)
        note = self.note_big("Emboss AÑADE relieve; Engrave HUNDE el mismo perfil dentro de la cara.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.remove_fixed_in_frame_mobjects(emb, eng, plus, minus)
        self.remove(emb, eng, plus, minus)
        self.play(FadeOut(VGroup(base_l, base_r, raise_l, recess)), run_time=0.40)

    def validation(self, hud):
        self.set_phase(hud, 9, "VALIDAR ANTES DE OK", DARK)
        self.move_camera(phi=64*DEGREES, theta=-48*DEGREES, zoom=0.88, run_time=0.90)
        final = self.embossed_body(self.EMBOSS_DEPTH)
        self.play(FadeIn(final), run_time=0.65)
        self.play(final.animate.shift(UP*0.78), run_time=0.65, rate_func=smooth)

        ok = self.validation_card(
            "VÁLIDO",
            ["perfil cerrado", "3 mm sobre la cara", "sin atravesar la pieza"],
            VALID,
            center=[-3.05, -2.72, 0],
        )
        bad = self.validation_card(
            "REVISAR",
            ["croquis abierto", "profundidad excesiva", "dirección incorrecta"],
            REMOVE,
            center=[3.05, -2.72, 0],
        )
        cards = VGroup(ok, bad)
        self.fixed(cards)
        self.play(FadeIn(ok[0]), Write(ok[1]), run_time=0.90)
        self.wait(0.45)
        self.play(FadeIn(bad[0]), Write(bad[1]), run_time=0.90)
        self.wait(EXPLAIN)
        self.clear_fixed(cards, 0.40)
        self.play(final.animate.shift(DOWN*0.78), run_time=0.60, rate_func=smooth)
        return final

    def commit_feature(self, hud, final):
        self.set_phase(hud, 10, "OK · EMBOSS1", VALID)
        self.play(final.animate.shift(RIGHT*1.18 + UP*0.46), run_time=0.70, rate_func=smooth)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.60)
        note = self.note_big("PASO 8 · OK crea Emboss1 después de Sketch2 en el árbol paramétrico.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return tree

    def parametric_edit(self, hud, final, tree):
        self.set_phase(hud, 11, "EDIT EMBOSS1", SKETCH)
        edit = self.small_callout("EDIT EMBOSS1  ·  DEPTH: 3 mm  →  5 mm", SKETCH, point=[0.55, -2.75, 0], width=6.55)
        self.play(FadeIn(edit), run_time=0.55)

        bigger = self.embossed_body(self.EMBOSS_DEPTH_EDIT)
        bigger.shift(RIGHT*1.18 + UP*0.46)
        self.play(Transform(final, bigger), run_time=1.75, rate_func=smooth)
        self.wait(READ)
        self.clear_fixed(edit, 0.25)

        note = self.note_big("Diseño paramétrico: cambia la profundidad sin redibujar Sketch1 ni Sketch2.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)

        back = self.embossed_body(self.EMBOSS_DEPTH)
        back.shift(RIGHT*1.18 + UP*0.46)
        self.play(Transform(final, back), run_time=1.35, rate_func=smooth)
        self.play(FadeOut(tree), final.animate.shift(LEFT*1.18 + DOWN*0.46), run_time=0.65)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def applications(self, hud, final):
        self.set_phase(hud, 12, "CUÁNDO USARLO", DARK)
        self.play(final.animate.shift(LEFT*2.25), run_time=0.65, rate_func=smooth)
        card = self.validation_card(
            "USOS DEL REPUJADO",
            ["logos e identificación", "marcas o agarres superficiales", "detalle poco profundo"],
            DARK,
            center=[3.55, -0.45, 0],
        )
        self.fixed(card)
        self.play(FadeIn(card[0]), Write(card[1]), run_time=0.95)
        self.wait(EXPLAIN)
        self.clear_fixed(card, 0.35)
        self.play(final.animate.shift(RIGHT*2.25), run_time=0.55)
        return final

    def final_orbit(self, hud, final):
        self.set_phase(hud, 13, "RESULTADO FINAL", VALID)
        note = self.note_big("FACE + CLOSED PROFILE + DEPTH = EMBOSS", VALID)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(hud["group"], 0.45)

        self.move_camera(phi=68*DEGREES, theta=-42*DEGREES, zoom=0.94, run_time=0.85)
        self.begin_ambient_camera_rotation(rate=0.09)
        self.wait(6.0)
        self.stop_ambient_camera_rotation()

        title = self.text("EMBOSS / REPUJADO", 42, BOLD, DARK).to_edge(UP, buff=0.38)
        sub = self.text("Sketch2 cerrado  +  3 mm  +  Emboss from Face  →  Emboss1", 27, BOLD, VALID).next_to(title, DOWN, buff=0.12)
        self.fixed(VGroup(title, sub))
        self.play(Write(title), Write(sub), run_time=1.05)
        self.wait(EXPLAIN)

    def construct(self):
        if not (self.PROFILE_R < min(self.BASE_W, self.BASE_D)/2 - 0.35):
            raise ValueError("Emboss profile does not fit on base face")
        if not (0 < self.EMBOSS_DEPTH < self.BASE_H):
            raise ValueError("Emboss depth must remain a shallow face feature")

        self.camera.background_color = WHITE
        self.opening()
        hud = self.hud()
        self.concept(hud)
        self.sketch1(hud)
        base = self.extrusion1(hud)
        plan = self.top_face_sketch2(hud, base)
        card = self.command_and_parameters(hud, plan)
        preview = self.preview_3d(hud, plan, card)
        self.section_emboss_vs_engrave(hud, preview)
        final = self.validation(hud)
        tree = self.commit_feature(hud, final)
        final = self.parametric_edit(hud, final, tree)
        final = self.applications(hud, final)
        self.final_orbit(hud, final)
