from __future__ import annotations

import numpy as np
from manim import *
from library.inventor_pro_ui import (
    JPMiscCADScene,
    cuboid,
    cylinder,
    BLACK_TEXT,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    BOLD,
    NORMAL,
    READ,
    EXPLAIN,
)

# Senior core accent colors already used by the dedicated Inventor lessons.
SKETCH = "#2878B5"
VALID = "#2E8B57"
WARNING = "#C0392B"
STEEL = "#B9C0C7"
STEEL_DARK = "#858F98"


class InventorMirrorSimetriaSeniorV3(JPMiscCADScene):
    """QA-rebuilt Autodesk Inventor Mirror / Simetría lesson.

    V3 is intentionally based on the current Mirror code plus the stronger
    persistent-HUD lesson core used by the recent dedicated Hole/Fillet renders.

    QA objectives
    -------------
    - Keep the white minimal Inventor-like classroom aesthetic.
    - Replace transient full-width section headings with a persistent HUD.
    - Increase 3D contrast and model scale.
    - Make the seed/plane/preview relationship explicit and sequential.
    - Remove the ambiguous Mirror "Operation = Join" row.
    - Keep all critical labels large enough for notebook/classroom projection.
    - Show the Browser dependency and prove parametric propagation by editing Boss1.
    """

    OPERATION = "Mirror / Simetría"
    BASE_W = 6.65
    BASE_D = 3.75
    BASE_H = 0.72
    BOSS_R = 0.52
    BOSS_R_EDIT = 0.72
    BOSS_H = 0.90
    OFFSET = 1.82

    # ---------- QA / layout helpers ----------
    def assert_safe(self, mob, margin_x=0.20, margin_y=0.16):
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -8 + margin_x or right > 8 - margin_x:
            raise ValueError(f"Horizontal safe-area violation: {left=:.3f}, {right=:.3f}")
        if bottom < -4.5 + margin_y or top > 4.5 - margin_y:
            raise ValueError(f"Vertical safe-area violation: {bottom=:.3f}, {top=:.3f}")
        return mob

    def fixed_safe(self, *mobs):
        for mob in mobs:
            self.assert_safe(mob)
        self.fixed(*mobs)

    def clear_fixed(self, mob, run_time=0.32):
        self.play(FadeOut(mob), run_time=run_time)
        self.remove_fixed_in_frame_mobjects(mob)
        self.remove(mob)

    # ---------- Persistent Inventor-style HUD ----------
    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 29, BOLD, DARK_GRAY)
        subtitle = self.text("MIRROR / SIMETRÍA 3D · operación paramétrica", 22, NORMAL, MID_GRAY)
        title.to_corner(UL, buff=0.34)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.05)
        rule = Line(LEFT * 7.50, RIGHT * 7.50, color=LIGHT_GRAY, stroke_width=1.45).to_edge(UP, buff=1.10)
        phase_box = RoundedRectangle(
            width=5.70,
            height=0.64,
            corner_radius=0.11,
            fill_color=WHITE,
            fill_opacity=0.99,
            stroke_color=DARK_GRAY,
            stroke_width=1.2,
        ).to_corner(UR, buff=0.34)
        phase = self.text("01 · IDEA GEOMÉTRICA", 21, BOLD, DARK_GRAY).move_to(phase_box)
        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed_safe(group)
        self.play(Write(title), Write(subtitle), Create(rule), FadeIn(phase_box), Write(phase), run_time=1.45)
        self.wait(0.70)
        return {"group": group, "box": phase_box, "phase": phase}

    def set_phase(self, hud, number, label, color=DARK_GRAY):
        old = hud["phase"]
        new = self.text(f"{number:02d} · {label}", 21, BOLD, color)
        if new.width > hud["box"].width - 0.34:
            new.scale_to_fit_width(hud["box"].width - 0.34)
        new.move_to(hud["box"])
        self.fixed_safe(new)
        self.play(FadeOut(old, shift=UP * 0.03), FadeIn(new, shift=UP * 0.03), run_time=0.48)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        hud["phase"] = new
        self.wait(0.35)

    def bottom_note(self, text, color=DARK_GRAY, width=13.3, y=-3.63, font=24):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.62:
            label.scale_to_fit_width(width - 0.62)
        box = RoundedRectangle(
            width=width,
            height=0.78,
            corner_radius=0.11,
            fill_color=WHITE,
            fill_opacity=0.99,
            stroke_color=color,
            stroke_width=1.25,
        )
        label.move_to(box)
        group = VGroup(box, label).move_to([0, y, 0])
        self.fixed_safe(group)
        self.play(FadeIn(box, shift=UP * 0.05), Write(label), run_time=0.68)
        return group

    def callout(self, text, point, color=DARK_GRAY, width=4.1, font=22):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.40:
            label.scale_to_fit_width(width - 0.40)
        box = RoundedRectangle(
            width=width,
            height=0.64,
            corner_radius=0.10,
            fill_color=WHITE,
            fill_opacity=0.985,
            stroke_color=color,
            stroke_width=1.15,
        )
        label.move_to(box)
        group = VGroup(box, label).move_to(point)
        self.fixed_safe(group)
        return group

    # ---------- CAD geometry ----------
    def base(self, opacity=0.95):
        return cuboid(self.BASE_W, self.BASE_D, self.BASE_H, opacity, STEEL)

    def boss(self, x, radius=None, opacity=0.94, color=STEEL_DARK):
        radius = self.BOSS_R if radius is None else radius
        return cylinder(radius, self.BOSS_H, opacity, color).shift(
            RIGHT * x + OUT * (self.BASE_H / 2 + self.BOSS_H / 2)
        )

    def mirror_plane_3d(self):
        return Rectangle(
            width=4.30,
            height=3.25,
            stroke_color=SKETCH,
            stroke_width=2.3,
            fill_color=SKETCH,
            fill_opacity=0.10,
        ).rotate(PI / 2, axis=UP).move_to([0, 0, 0.63])

    def parameter_card(self):
        rows = [
            ("Object Type", "Features"),
            ("Features", "Boss1"),
            ("Mirror Plane", "YZ Plane"),
            ("Preview", "Enabled"),
        ]
        head = self.text("MIRROR PARAMETERS", 25, BOLD, DARK_GRAY)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 20, BOLD, DARK_GRAY)
            val = self.text(right, 20, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.55,
                height=0.50,
                corner_radius=0.05,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_color=MID_GRAY,
                stroke_width=1.0,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.14)
            entries.add(VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.18))
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel = RoundedRectangle(
            width=5.10,
            height=content.height + 0.55,
            corner_radius=0.11,
            fill_color=PAPER_GRAY,
            fill_opacity=0.995,
            stroke_color=DARK_GRAY,
            stroke_width=1.25,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.27)
        group = VGroup(panel, content).move_to([5.15, -0.05, 0])
        self.fixed_safe(group)
        return group

    def feature_tree(self, edited=False):
        boss_label = "Boss1   Ø22 mm" if edited else "Boss1   Ø16 mm"
        items = [
            ("Part1.ipt", DARK_GRAY, BOLD),
            ("Origin", MID_GRAY, NORMAL),
            ("  YZ Plane", SKETCH, BOLD),
            ("Sketch1", MID_GRAY, NORMAL),
            ("Extrusion1   10 mm", DARK_GRAY, NORMAL),
            ("Sketch2", MID_GRAY, NORMAL),
            (boss_label, DARK_GRAY, BOLD),
            ("Mirror1   Boss1 / YZ Plane", VALID, BOLD),
        ]
        lines = VGroup(*[self.text(t, 21, w, c) for t, c, w in items]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.11
        )
        panel = RoundedRectangle(
            width=4.65,
            height=lines.height + 0.58,
            corner_radius=0.10,
            fill_color=WHITE,
            fill_opacity=0.985,
            stroke_color=DARK_GRAY,
            stroke_width=1.15,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.26)
        group = VGroup(panel, lines).move_to([-5.40, -0.35, 0])
        self.fixed_safe(group)
        return group

    # ---------- Narrative ----------
    def opening_scene(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 29, BOLD, DARK_GRAY)
        title = self.text("MIRROR / SIMETRÍA", 55, BOLD, BLACK_TEXT)
        sub = self.text("Duplicar una operación 3D respecto a un plano estable, sin redibujarla.", 28, NORMAL, DARK_GRAY)
        route = self.text("Boss1  →  YZ Plane  →  Preview  →  Mirror1", 26, BOLD, SKETCH)
        rule = Line(LEFT * 5.7, RIGHT * 5.7, color=DARK_GRAY, stroke_width=1.8)
        group = VGroup(top, title, rule, sub, route).arrange(DOWN, buff=0.32)
        self.fixed_safe(group)
        self.play(FadeIn(top, shift=UP * 0.08), run_time=0.70)
        self.play(Write(title), run_time=1.10)
        self.play(Create(rule), FadeIn(sub), run_time=0.85)
        self.play(Write(route), run_time=1.10)
        self.wait(EXPLAIN)
        self.play(FadeOut(group), run_time=0.55)
        self.remove_fixed_in_frame_mobjects(group)
        self.remove(group)

    def concept(self, hud):
        self.set_phase(hud, 1, "IDEA GEOMÉTRICA", DARK_GRAY)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        plane = DashedLine(UP * 2.25, DOWN * 2.25, color=SKETCH, stroke_width=3.1, dash_length=0.14)
        source = Dot(LEFT * 3.05 + UP * 0.40, radius=0.12, color=DARK_GRAY)
        target = Dot(RIGHT * 3.05 + UP * 0.40, radius=0.12, color=VALID)
        d1 = DoubleArrow(LEFT * 3.05 + DOWN * 0.18, DOWN * 0.18, buff=0, color=DARK_GRAY, stroke_width=2.2)
        d2 = DoubleArrow(DOWN * 0.18, RIGHT * 3.05 + DOWN * 0.18, buff=0, color=DARK_GRAY, stroke_width=2.2)
        labels = VGroup(
            self.text("SEMILLA", 26, BOLD, DARK_GRAY).next_to(source, UP, buff=0.14),
            self.text("COPIA", 26, BOLD, VALID).next_to(target, UP, buff=0.14),
            self.text("d", 25, BOLD, DARK_GRAY).next_to(d1, DOWN, buff=0.10),
            self.text("d", 25, BOLD, DARK_GRAY).next_to(d2, DOWN, buff=0.10),
            self.text("YZ PLANE", 23, BOLD, SKETCH).next_to(plane, UP, buff=0.10),
        )
        self.fixed_safe(labels)
        note = self.bottom_note("La simetría conserva la distancia perpendicular al plano: d a un lado = d al otro.", SKETCH)
        self.play(Create(plane), FadeIn(source), Create(d1), run_time=1.00)
        self.play(TransformFromCopy(source, target), Create(d2), FadeIn(labels), run_time=1.35)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(plane), FadeOut(source), FadeOut(target), FadeOut(d1), FadeOut(d2), FadeOut(labels), run_time=0.45)
        self.remove_fixed_in_frame_mobjects(labels)

    def sketch_base(self, hud):
        self.set_phase(hud, 2, "SKETCH1 · BASE", SKETCH)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        outline = Rectangle(width=self.BASE_W, height=self.BASE_D, color=SKETCH, stroke_width=4.0)
        h_axis = DashedLine(outline.get_left(), outline.get_right(), color=LIGHT_GRAY, dash_length=0.11)
        v_axis = DashedLine(outline.get_bottom(), outline.get_top(), color=LIGHT_GRAY, dash_length=0.11)
        center = Dot(ORIGIN, radius=0.055, color=WARNING)
        dim_w = DoubleArrow(LEFT * self.BASE_W / 2 + DOWN * 2.25, RIGHT * self.BASE_W / 2 + DOWN * 2.25,
                            buff=0, color=DARK_GRAY, stroke_width=2.0)
        dim_h = DoubleArrow(RIGHT * 3.72 + DOWN * self.BASE_D / 2, RIGHT * 3.72 + UP * self.BASE_D / 2,
                            buff=0, color=DARK_GRAY, stroke_width=2.0)
        labels = VGroup(
            self.text("110 mm", 25, BOLD).next_to(dim_w, DOWN, buff=0.08),
            self.text("62 mm", 25, BOLD).next_to(dim_h, RIGHT, buff=0.10).rotate(PI / 2),
        )
        self.fixed_safe(labels)
        self.play(Create(outline), Create(h_axis), Create(v_axis), FadeIn(center), run_time=1.15)
        self.play(Create(dim_w), Create(dim_h), FadeIn(labels), run_time=1.10)
        tag = self.callout("FULLY CONSTRAINED", [0, 2.75, 0], VALID, width=4.20)
        self.play(FadeIn(tag), run_time=0.55)
        note = self.bottom_note("Paso 1: crea y acota Sketch1 antes de generar volumen.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)
        self.play(FadeOut(dim_w), FadeOut(dim_h), FadeOut(labels), FadeOut(center), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(labels)
        return outline, h_axis, v_axis

    def extrude_base(self, hud, outline, h_axis, v_axis):
        self.set_phase(hud, 3, "EXTRUSION1 · 10 mm", DARK_GRAY)
        self.move_camera(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.94, run_time=1.20)
        preview = cuboid(self.BASE_W, self.BASE_D, 0.06, 0.24, SKETCH)
        self.play(FadeIn(preview), outline.animate.set_opacity(0.28), run_time=0.55)
        body = self.base(0.95)
        self.play(ReplacementTransform(preview, body), FadeOut(outline), FadeOut(h_axis), FadeOut(v_axis), run_time=1.25)
        note = self.bottom_note("Paso 2: Extrude = 10 mm convierte Sketch1 en la pieza base.", DARK_GRAY)
        self.wait(READ)
        self.clear_fixed(note)
        return body

    def sketch_seed(self, hud, body):
        self.set_phase(hud, 4, "SKETCH2 · SEMILLA", SKETCH)
        self.play(FadeOut(body), run_time=0.35)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.02)
        plate = Rectangle(width=self.BASE_W, height=self.BASE_D, color=DARK_GRAY, stroke_width=3.1)
        plane = DashedLine(UP * self.BASE_D / 2, DOWN * self.BASE_D / 2, color=SKETCH, stroke_width=2.5, dash_length=0.12)
        circle = Circle(radius=self.BOSS_R, color=SKETCH, stroke_width=4.2).move_to(LEFT * self.OFFSET)
        center = Dot(circle.get_center(), radius=0.070, color=WARNING)
        d = DoubleArrow(LEFT * self.OFFSET + DOWN * 1.40, DOWN * 1.40, buff=0,
                        color=DARK_GRAY, stroke_width=2.1)
        lab_d = self.text("28 mm", 25, BOLD).next_to(d, DOWN, buff=0.08)
        lab_phi = self.text("Ø16 mm", 27, BOLD, SKETCH).next_to(circle, UP, buff=0.13)
        yz = self.text("YZ PLANE", 23, BOLD, SKETCH).next_to(plane, UP, buff=0.10)
        labels = VGroup(lab_d, lab_phi, yz)
        self.fixed_safe(labels)
        self.play(FadeIn(plate), Create(plane), run_time=0.80)
        self.play(Create(circle), FadeIn(center), Create(d), FadeIn(labels), run_time=1.15)
        note = self.bottom_note("Paso 3: dibuja solo una semilla: Ø16 mm y 28 mm desde el plano YZ.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return plate, plane, circle, center, d, labels

    def extrude_seed(self, hud, plate, plane2d, circle, center, d, labels):
        self.set_phase(hud, 5, "EXTRUDE · BOSS1", DARK_GRAY)
        self.play(FadeOut(labels), FadeOut(d), run_time=0.28)
        self.remove_fixed_in_frame_mobjects(labels)
        self.move_camera(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.98, run_time=1.10)
        base = self.base(0.95)
        seed = self.boss(-self.OFFSET, opacity=0.97)
        self.play(FadeOut(plate), FadeOut(plane2d), FadeOut(circle), FadeOut(center), FadeIn(base), run_time=0.75)
        self.play(FadeIn(seed, shift=OUT * 0.10), run_time=0.95)
        tag = self.callout("Boss1 · FEATURE SEMILLA", [0, -2.35, 0], DARK_GRAY, width=5.0)
        self.play(FadeIn(tag), run_time=0.50)
        note = self.bottom_note("Paso 4: extruye Sketch2 una sola vez. Boss1 será la entrada de Mirror.", DARK_GRAY)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)
        return base, seed

    def choose_feature(self, hud, base, seed):
        self.set_phase(hud, 6, "MIRROR · SELECT BOSS1", SKETCH)
        self.play(base.animate.shift(LEFT * 0.95), seed.animate.shift(LEFT * 0.95), run_time=0.70)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.60)
        halo = seed.copy().set_color(SKETCH).set_opacity(0.48)
        halo.shift(LEFT * 0.95)
        self.play(FadeIn(halo), run_time=0.45)
        tag = self.callout("FEATURES = Boss1", [4.95, -2.25, 0], SKETCH, width=4.3)
        self.play(FadeIn(tag), run_time=0.45)
        note = self.bottom_note("Paso 5: 3D Model → Pattern → Mirror. En Features selecciona Boss1.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)
        self.play(FadeOut(halo), run_time=0.25)
        return card

    def choose_plane_preview(self, hud, base, seed, card):
        self.set_phase(hud, 7, "MIRROR PLANE · YZ", SKETCH)
        self.play(base.animate.shift(RIGHT * 0.95), seed.animate.shift(RIGHT * 0.95), run_time=0.65)
        plane3 = self.mirror_plane_3d()
        self.play(FadeIn(plane3), run_time=0.65)
        tag = self.callout("MIRROR PLANE = YZ", [-4.85, -2.25, 0], SKETCH, width=4.8)
        self.play(FadeIn(tag), run_time=0.45)
        note = self.bottom_note("Paso 6: usa el plano de origen YZ como referencia estable de simetría.", SKETCH)
        self.wait(READ)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)

        self.set_phase(hud, 8, "PREVIEW PARAMÉTRICO", VALID)
        ghost = seed.copy().set_color(SKETCH).set_opacity(0.32)
        self.add(ghost)
        self.play(ghost.animate.shift(RIGHT * (2 * self.OFFSET)), run_time=2.20, rate_func=smooth)
        mirror = self.boss(self.OFFSET, opacity=0.96)
        self.play(ReplacementTransform(ghost, mirror), run_time=0.75)
        ok = self.callout("PREVIEW = EQUAL DISTANCE", [-4.65, -2.25, 0], VALID, width=5.3)
        self.play(FadeIn(ok), run_time=0.45)
        note = self.bottom_note("Paso 7: el preview debe aparecer al lado opuesto, sin crear un segundo sketch.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(ok, 0.25)
        self.play(FadeOut(card), FadeOut(plane3), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        return mirror

    def verify_top_view(self, hud, base, seed, mirror):
        self.set_phase(hud, 9, "VERIFICAR 28 mm = 28 mm", VALID)
        self.play(FadeOut(base), FadeOut(seed), FadeOut(mirror), run_time=0.35)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.02)
        plate = Rectangle(width=self.BASE_W, height=self.BASE_D, color=DARK_GRAY, stroke_width=3.1)
        axis = DashedLine(UP * self.BASE_D / 2, DOWN * self.BASE_D / 2, color=SKETCH, stroke_width=2.5, dash_length=0.12)
        c1 = Circle(radius=self.BOSS_R, color=DARK_GRAY, stroke_width=4.0).move_to(LEFT * self.OFFSET)
        c2 = Circle(radius=self.BOSS_R, color=VALID, stroke_width=4.0).move_to(RIGHT * self.OFFSET)
        d1 = DoubleArrow(LEFT * self.OFFSET + DOWN * 1.43, DOWN * 1.43, buff=0, color=DARK_GRAY, stroke_width=2.0)
        d2 = DoubleArrow(DOWN * 1.43, RIGHT * self.OFFSET + DOWN * 1.43, buff=0, color=DARK_GRAY, stroke_width=2.0)
        labels = VGroup(
            self.text("28 mm", 25, BOLD).next_to(d1, DOWN, buff=0.08),
            self.text("28 mm", 25, BOLD).next_to(d2, DOWN, buff=0.08),
            self.text("YZ PLANE", 23, BOLD, SKETCH).next_to(axis, UP, buff=0.10),
        )
        self.fixed_safe(labels)
        self.play(FadeIn(plate), Create(axis), Create(c1), run_time=0.80)
        self.play(TransformFromCopy(c1, c2), Create(d1), Create(d2), FadeIn(labels), run_time=1.15)
        note = self.bottom_note("Control geométrico: el plano YZ divide dos posiciones equidistantes de 28 mm.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.play(FadeOut(plate), FadeOut(axis), FadeOut(c1), FadeOut(c2), FadeOut(d1), FadeOut(d2), FadeOut(labels), run_time=0.40)
        self.remove_fixed_in_frame_mobjects(labels)

    def validate_reference(self, hud):
        self.set_phase(hud, 10, "VALIDAR REFERENCIA", DARK_GRAY)
        robust_h = self.text("ROBUSTA", 28, BOLD, VALID)
        robust_lines = VGroup(
            self.text("Origin YZ Plane", 23, BOLD, DARK_GRAY),
            self.text("referencia estable", 21, NORMAL, DARK_GRAY),
            self.text("recomendada", 21, NORMAL, DARK_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        robust = VGroup(robust_h, robust_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        robust_box = SurroundingRectangle(robust, buff=0.28, corner_radius=0.10, color=VALID, stroke_width=1.45)
        good = VGroup(robust_box, robust).move_to([-3.35, -0.25, 0])

        fragile_h = self.text("FRÁGIL", 28, BOLD, WARNING)
        fragile_lines = VGroup(
            self.text("cara temporal", 23, BOLD, DARK_GRAY),
            self.text("puede cambiar con edits", 21, NORMAL, DARK_GRAY),
            self.text("evitar si no es necesaria", 21, NORMAL, DARK_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        fragile = VGroup(fragile_h, fragile_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fragile_box = SurroundingRectangle(fragile, buff=0.28, corner_radius=0.10, color=WARNING, stroke_width=1.45)
        bad = VGroup(fragile_box, fragile).move_to([3.35, -0.25, 0])
        cards = VGroup(good, bad)
        self.fixed_safe(cards)
        self.play(FadeIn(robust_box), Write(robust), run_time=0.80)
        self.wait(0.55)
        self.play(FadeIn(fragile_box), Write(fragile), run_time=0.80)
        note = self.bottom_note("Antes de OK: prioriza planos de origen o work planes estables frente a referencias temporales.", DARK_GRAY)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(cards, 0.40)

    def commit_and_edit(self, hud):
        self.set_phase(hud, 11, "OK · MIRROR1", VALID)
        self.move_camera(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.96, run_time=0.90)
        base = self.base(0.95).shift(RIGHT * 1.0)
        seed = self.boss(-self.OFFSET, opacity=0.97).shift(RIGHT * 1.0)
        mirror = self.boss(self.OFFSET, opacity=0.97).shift(RIGHT * 1.0)
        self.play(FadeIn(base), FadeIn(seed), FadeIn(mirror), run_time=0.85)
        tree = self.feature_tree(False)
        self.play(FadeIn(tree), run_time=0.65)
        note = self.bottom_note("Paso 8: OK crea Mirror1 después de Boss1 en el árbol paramétrico.", VALID)
        self.wait(READ)
        self.clear_fixed(note)

        self.set_phase(hud, 12, "EDITAR BOSS1 · Ø22 mm", SKETCH)
        edit = self.callout("EDIT BOSS1: Ø16 → Ø22", [0.65, -2.48, 0], SKETCH, width=5.0)
        self.play(FadeIn(edit), run_time=0.50)
        seed_big = self.boss(-self.OFFSET, self.BOSS_R_EDIT, 0.97).shift(RIGHT * 1.0)
        mirror_big = self.boss(self.OFFSET, self.BOSS_R_EDIT, 0.97).shift(RIGHT * 1.0)
        self.play(Transform(seed, seed_big), Transform(mirror, mirror_big), run_time=1.80, rate_func=smooth)
        tree2 = self.feature_tree(True)
        self.play(ReplacementTransform(tree, tree2), run_time=0.75)
        note = self.bottom_note("Prueba paramétrica: editas Boss1 una vez y Mirror1 actualiza la copia automáticamente.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(edit, 0.25)
        self.play(FadeOut(tree2), base.animate.shift(LEFT * 1.0), seed.animate.shift(LEFT * 1.0), mirror.animate.shift(LEFT * 1.0), run_time=0.60)
        self.remove_fixed_in_frame_mobjects(tree2)
        self.remove(tree2)
        return base, seed, mirror

    def final_inspection(self, hud, base, seed, mirror):
        self.set_phase(hud, 13, "INSPECCIÓN FINAL", DARK_GRAY)
        summary = self.text(
            "Sketch1 → Extrusion1 → Sketch2 → Boss1 → YZ Plane → Preview → Mirror1",
            24,
            BOLD,
            DARK_GRAY,
        ).to_edge(DOWN, buff=0.34)
        if summary.width > 13.8:
            summary.scale_to_fit_width(13.8)
        self.fixed_safe(summary)
        self.play(Write(summary), run_time=1.10)
        self.wait(READ)
        self.begin_ambient_camera_rotation(rate=0.095)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()
        self.wait(1.4)

    def construct(self):
        self.camera.background_color = WHITE
        self.opening_scene()
        hud = self.hud()
        self.concept(hud)
        outline, h_axis, v_axis = self.sketch_base(hud)
        body = self.extrude_base(hud, outline, h_axis, v_axis)
        plate, plane2d, circle, center, d, labels = self.sketch_seed(hud, body)
        base, seed = self.extrude_seed(hud, plate, plane2d, circle, center, d, labels)
        card = self.choose_feature(hud, base, seed)
        mirror = self.choose_plane_preview(hud, base, seed, card)
        self.verify_top_view(hud, base, seed, mirror)
        self.validate_reference(hud)
        base, seed, mirror = self.commit_and_edit(hud)
        self.final_inspection(hud, base, seed, mirror)
