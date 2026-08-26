from __future__ import annotations

import math
import os
import numpy as np
from manim import *

# -----------------------------------------------------------------------------
# Senior CAD classroom format — based on the approved House/Sweep/Loft/Revolve
# grammar in this repository: white background, restrained neutral palette,
# orthographic sketch stage, deliberate 2D->3D transition, visible feature
# formation, parameter reasoning, and final model orbit.
# -----------------------------------------------------------------------------

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK = "#303030"
MID = "#707070"
LIGHT = "#D7D7D7"
STEEL = "#B8BEC5"
STEEL_DARK = "#7D8790"
SKETCH = "#2878B5"
VALID = "#2E8B57"
REMOVE = "#C0392B"
PAPER = "#FAFAFA"

TITLE = 50
H1 = 31
BODY = 23
SMALL = 18

MICRO = 0.65
READ = 1.75
EXPLAIN = 2.45
OBSERVE = 2.90


class InventorFilletRedondeoSeniorV4(ThreeDScene):
    """Full lesson: Autodesk Inventor Fillet / Redondeo.

    Narrative contract:
    1) Explain the geometry of a constant-radius fillet in 2D.
    2) Build the base part from a constrained 2D sketch.
    3) Extrude that sketch into a 3D solid.
    4) Select the exact 3D edge that will be modified.
    5) Explain Fillet parameters and the tangent-radius condition.
    6) Show the material removed and the new rounded surface forming.
    7) Validate the preview and discuss common failure conditions.
    8) Show Fillet1 as a parametric feature and edit the radius.
    9) End with a clean orbit and workflow summary.
    """

    BASE_W = 5.6
    BASE_D = 3.4
    BASE_H = 0.86
    R8 = 0.58
    R12 = 0.84

    def box(self, dims, center, color=STEEL, opacity=0.92, stroke=DARK, stroke_width=0.8):
        x, y, z = dims
        mob = Cube(
            side_length=1,
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=stroke,
            stroke_width=stroke_width,
        )
        mob.stretch(x, 0).stretch(y, 1).stretch(z, 2)
        mob.move_to(np.array(center, dtype=float))
        return mob

    def text(self, content, size=BODY, weight=NORMAL, color=BLACK_TEXT):
        return Text(content, font_size=size, weight=weight, color=color)

    def fit(self, mob, max_w=14.6, max_h=7.5):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def fixed(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)

    def clear_fixed_group(self, group, run_time=0.45):
        self.play(FadeOut(group), run_time=run_time)
        self.remove_fixed_in_frame_mobjects(group)
        self.remove(group)

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def one_corner_points(self, radius, z=0.0, samples=18):
        """Rectangle footprint with only the upper-right corner filleted."""
        w = self.BASE_W / 2
        d = self.BASE_D / 2
        r = min(radius, self.BASE_W * 0.28, self.BASE_D * 0.40)
        pts = [
            [-w, -d, z],
            [ w, -d, z],
            [ w,  d - r, z],
        ]
        cx, cy = w - r, d - r
        for a in np.linspace(0, PI / 2, samples):
            pts.append([cx + r * math.cos(a), cy + r * math.sin(a), z])
        pts.append([-w, d, z])
        return [np.array(p, dtype=float) for p in pts]

    def removed_corner_points(self, radius, z=0.0, samples=20):
        """2D area removed from the original sharp corner by the fillet."""
        w = self.BASE_W / 2
        d = self.BASE_D / 2
        r = radius
        cx, cy = w - r, d - r
        pts = [
            [w, d - r, z],
            [w, d, z],
            [w - r, d, z],
        ]
        for a in np.linspace(PI / 2, 0, samples):
            pts.append([cx + r * math.cos(a), cy + r * math.sin(a), z])
        return [np.array(p, dtype=float) for p in pts]

    def extruded_polygon(self, points, height, color=STEEL, opacity=0.92, stroke=DARK):
        front = [np.array(p, dtype=float) for p in points]
        back = [p + OUT * height for p in front]
        f0 = Polygon(*front, fill_color=color, fill_opacity=opacity, stroke_color=stroke, stroke_width=0.8)
        f1 = Polygon(*back, fill_color=color, fill_opacity=opacity, stroke_color=stroke, stroke_width=0.8)
        sides = VGroup()
        for i in range(len(front)):
            j = (i + 1) % len(front)
            sides.add(
                Polygon(
                    front[i], front[j], back[j], back[i],
                    fill_color=color, fill_opacity=opacity,
                    stroke_color=stroke, stroke_width=0.8,
                )
            )
        return VGroup(f0, f1, sides)

    def fillet_surface(self, radius, color=VALID, opacity=0.72, strips=20):
        """Quarter-cylinder-like tangent surface created along the selected edge."""
        w = self.BASE_W / 2
        d = self.BASE_D / 2
        r = radius
        cx, cy = w - r, d - r
        patches = VGroup()
        angles = np.linspace(0, PI / 2, strips + 1)
        for a0, a1 in zip(angles[:-1], angles[1:]):
            p00 = np.array([cx + r * math.cos(a0), cy + r * math.sin(a0), 0.0])
            p10 = np.array([cx + r * math.cos(a1), cy + r * math.sin(a1), 0.0])
            p01 = p00 + OUT * self.BASE_H
            p11 = p10 + OUT * self.BASE_H
            patches.add(
                Polygon(
                    p00, p10, p11, p01,
                    fill_color=color, fill_opacity=opacity,
                    stroke_color=color, stroke_width=0.45,
                )
            )
        return patches

    # ------------------------------------------------------------------
    # Fixed classroom UI — intentionally minimal, not a fake full Inventor UI.
    # ------------------------------------------------------------------
    def top_hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 25, BOLD, DARK)
        subtitle = self.text("FILLET / REDONDEO 3D  ·  explicación paso a paso", 20, NORMAL, MID)
        title.to_corner(UL, buff=0.34)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.06)
        rule = Line(LEFT * 7.55, RIGHT * 7.55, color=LIGHT, stroke_width=1.3).to_edge(UP, buff=1.02)

        box = RoundedRectangle(
            width=5.15, height=0.54, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.98,
            stroke_color=DARK, stroke_width=1.1,
        ).to_corner(UR, buff=0.38)
        phase = self.text("01 · GEOMETRÍA DEL FILLET", 18, BOLD, DARK).move_to(box)

        legend = VGroup(
            Dot(radius=0.055, color=SKETCH), self.text("croquis / selección", 15, BOLD, SKETCH),
            Dot(radius=0.055, color=VALID), self.text("vista previa válida", 15, BOLD, VALID),
            Dot(radius=0.055, color=REMOVE), self.text("material retirado", 15, BOLD, REMOVE),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.22)

        group = VGroup(title, subtitle, rule, box, phase, legend)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), FadeIn(legend), run_time=1.65)
        self.wait(READ)
        return {"group": group, "box": box, "phase": phase}

    def set_phase(self, hud, number, label, color=DARK):
        old = hud["phase"]
        new = self.text(f"{number:02d} · {label}", 18, BOLD, color).move_to(hud["box"])
        self.fixed(new)
        self.play(FadeOut(old), Write(new), run_time=0.65)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        hud["phase"] = new
        self.wait(MICRO)

    def note(self, text, color=DARK, width=9.4):
        label = self.text(text, 19, BOLD, color)
        self.fit(label, width - 0.55, 0.55)
        box = RoundedRectangle(
            width=width, height=0.66, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.96,
            stroke_color=color, stroke_width=1.2,
        )
        label.move_to(box)
        group = VGroup(box, label).to_edge(DOWN, buff=0.55)
        self.fixed(group)
        self.play(FadeIn(box, shift=UP * 0.05), Write(label), run_time=0.75)
        self.wait(MICRO)
        return group

    def remove_note(self, group):
        self.clear_fixed_group(group, run_time=0.32)

    def parameter_card(self):
        rows = [
            ("Selection", "Edge1"),
            ("Radius", "8 mm"),
            ("Type", "Constant"),
            ("Continuity", "Tangent"),
        ]
        head = self.text("FILLET PARAMETERS", 21, BOLD)
        entries = VGroup()
        for left, right in rows:
            a = self.text(left, 17, BOLD, DARK)
            b = self.text(right, 17, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.35, height=0.43, corner_radius=0.05,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.0,
            )
            b.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.12)
            entries.add(VGroup(a, VGroup(field, b)).arrange(RIGHT, buff=0.15))
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        panel = RoundedRectangle(
            width=4.55, height=content.height + 0.48, corner_radius=0.10,
            fill_color=PAPER, fill_opacity=0.98,
            stroke_color=DARK, stroke_width=1.2,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.24)
        group = VGroup(panel, content).to_corner(DR, buff=0.42).shift(UP * 0.78)
        self.fixed(group)
        return group

    def feature_tree(self):
        items = [
            ("Part1.ipt", DARK, BOLD),
            ("  Origin", MID, NORMAL),
            ("  Sketch1", MID, NORMAL),
            ("  Extrusion1", DARK, NORMAL),
            ("  Fillet1   R = 8 mm", VALID, BOLD),
        ]
        lines = VGroup(*[self.text(t, 17, w, c) for t, c, w in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        panel = RoundedRectangle(
            width=3.95, height=lines.height + 0.45, corner_radius=0.08,
            fill_color=WHITE, fill_opacity=0.97,
            stroke_color=DARK, stroke_width=1.0,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.22)
        group = VGroup(panel, lines).to_corner(DL, buff=0.42).shift(UP * 0.70)
        self.fixed(group)
        return group

    # ------------------------------------------------------------------
    # Narrative scenes
    # ------------------------------------------------------------------
    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 25, BOLD, DARK)
        title = self.text("FILLET / REDONDEO", 52, BOLD, BLACK_TEXT)
        sub = self.text("De croquis 2D a superficie tangente 3D", 28, NORMAL, MID)
        rule = Line(LEFT * 5.6, RIGHT * 5.6, color=BLACK, stroke_width=2)

        labels = ["CROQUIS", "EXTRUSIÓN", "ARISTA", "RADIO", "PREVIEW", "FILLET1"]
        pills = VGroup()
        for label in labels:
            t = self.text(label, 17, BOLD)
            b = RoundedRectangle(
                width=max(1.55, t.width + 0.40), height=0.55, corner_radius=0.14,
                fill_color=PAPER, fill_opacity=1, stroke_color=BLACK, stroke_width=1.1,
            )
            t.move_to(b)
            pills.add(VGroup(b, t))
        pills.arrange(RIGHT, buff=0.18)
        arrows = VGroup(*[
            Arrow(
                pills[i].get_right(), pills[i + 1].get_left(), buff=0.06,
                color=BLACK, stroke_width=1.8, max_tip_length_to_length_ratio=0.12,
            )
            for i in range(len(pills) - 1)
        ])
        route = VGroup(pills, arrows)
        group = VGroup(top, title, rule, sub, route).arrange(DOWN, buff=0.32)
        self.fixed(group)

        self.play(FadeIn(top, shift=UP * 0.08), run_time=0.75)
        self.play(Write(title), run_time=1.15)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(p) for p in pills], lag_ratio=0.10), Create(arrows), run_time=1.55)
        self.wait(EXPLAIN)
        self.clear_fixed_group(group, run_time=0.65)

    def concept_2d(self, hud):
        self.set_phase(hud, 1, "GEOMETRÍA DEL FILLET", DARK)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        corner = np.array([2.0, 1.0, 0.0])
        r = 1.20
        center = corner + np.array([-r, -r, 0.0])
        top_edge = Line([-3.0, 1.0, 0], corner, color=DARK, stroke_width=5)
        right_edge = Line([2.0, -2.1, 0], corner, color=DARK, stroke_width=5)
        sharp = Dot(corner, radius=0.085, color=REMOVE)
        label = self.text("ARISTA VIVA = intersección de dos caras", 23, BOLD, REMOVE).shift(LEFT * 3.35 + DOWN * 2.1)
        self.fixed(label)

        self.play(Create(top_edge), Create(right_edge), FadeIn(sharp), Write(label), run_time=1.25)
        self.wait(READ)

        arc = Arc(radius=r, start_angle=0, angle=PI / 2, arc_center=center, color=VALID, stroke_width=7)
        c_dot = Dot(center, radius=0.065, color=SKETCH)
        radius_line = Line(center, [2.0, 1.0 - r, 0], color=SKETCH, stroke_width=3)
        t_right = Dot([2.0, 1.0 - r, 0], radius=0.055, color=VALID)
        t_top = Dot([2.0 - r, 1.0, 0], radius=0.055, color=VALID)
        r_label = self.text("R = 8 mm", 24, BOLD, SKETCH).next_to(radius_line, DOWN, buff=0.10)
        tangency = self.text("La nueva curva es tangente a las dos caras", 22, BOLD, VALID).shift(RIGHT * 2.6 + DOWN * 2.25)
        self.fixed(tangency)

        self.play(Create(radius_line), FadeIn(c_dot), FadeIn(t_right), FadeIn(t_top), Write(r_label), run_time=1.05)
        self.play(Create(arc), run_time=1.25)
        self.play(Write(tangency), run_time=0.85)
        note = self.note("FILLET = sustituir la arista viva por una transición circular de radio constante", VALID, width=10.8)
        self.wait(EXPLAIN)
        self.remove_note(note)

        self.play(FadeOut(top_edge), FadeOut(right_edge), FadeOut(sharp), FadeOut(arc), FadeOut(c_dot), FadeOut(radius_line),
                  FadeOut(t_right), FadeOut(t_top), FadeOut(r_label), run_time=0.55)
        self.clear_fixed_group(label, run_time=0.25)
        self.clear_fixed_group(tangency, run_time=0.25)

    def build_base(self, hud):
        self.set_phase(hud, 2, "CROQUIS 2D · SKETCH1", SKETCH)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.92, run_time=0.70)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5, fill_opacity=0)
        origin = Dot(ORIGIN, radius=0.06, color=REMOVE)
        ch = DashedLine(outline.get_left(), outline.get_right(), color=LIGHT, dash_length=0.12, stroke_width=1.5)
        cv = DashedLine(outline.get_bottom(), outline.get_top(), color=LIGHT, dash_length=0.12, stroke_width=1.5)

        d1 = DoubleArrow([-w/2, -d/2 - 0.45, 0], [w/2, -d/2 - 0.45, 0], buff=0, color=DARK, stroke_width=2)
        d2 = DoubleArrow([w/2 + 0.45, -d/2, 0], [w/2 + 0.45, d/2, 0], buff=0, color=DARK, stroke_width=2)
        l1 = self.text("80 mm", 21, BOLD).next_to(d1, DOWN, buff=0.08)
        l2 = self.text("50 mm", 21, BOLD).rotate(PI / 2).next_to(d2, RIGHT, buff=0.08)
        status = self.text("Sketch1  ·  Fully Constrained", 22, BOLD, SKETCH).shift(UP * 2.45)

        self.play(Create(outline), Create(ch), Create(cv), FadeIn(origin), run_time=1.45)
        self.play(Create(d1), Create(d2), Write(l1), Write(l2), Write(status), run_time=1.15)
        note = self.note("Primero define la forma y las dimensiones. El Fillet todavía NO existe.", SKETCH)
        self.wait(EXPLAIN)
        self.remove_note(note)

        self.set_phase(hud, 3, "EXTRUSIÓN + · EXTRUSION1", VALID)
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(l1), FadeOut(l2), FadeOut(status), run_time=0.35)
        self.move_camera(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=0.88, run_time=1.55)
        seed = self.box((w, d, 0.035), (0, 0, 0.0175), STEEL, 0.82)
        target = self.box((w, d, self.BASE_H), (0, 0, self.BASE_H / 2), STEEL, 0.92)
        self.add(seed)
        note = self.note("Finish Sketch  →  Extrude 12 mm  →  Join  →  Extrusion1", VALID)
        self.play(Transform(seed, target), outline.animate.shift(OUT * self.BASE_H).set_opacity(0.22), run_time=2.25, rate_func=smooth)
        self.wait(READ)
        self.remove_note(note)
        self.play(FadeOut(outline), FadeOut(ch), FadeOut(cv), FadeOut(origin), run_time=0.40)
        return seed

    def select_edge_and_parameters(self, hud, body):
        self.set_phase(hud, 4, "SELECCIONAR ARISTA 3D", SKETCH)
        w, d, h = self.BASE_W, self.BASE_D, self.BASE_H
        edge = Line3D(
            start=[w / 2, d / 2, 0.0],
            end=[w / 2, d / 2, h],
            color=SKETCH,
            thickness=0.055,
        )
        top_point = Dot3D(point=[w/2, d/2, h], radius=0.07, color=SKETCH)
        self.play(Create(edge), FadeIn(top_point), run_time=0.70)
        note = self.note("Selecciona la arista que realmente deseas modificar: Edge1", SKETCH)
        self.wait(EXPLAIN)
        self.remove_note(note)

        self.set_phase(hud, 5, "3D MODEL · MODIFY · FILLET", DARK)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.65)
        note = self.note("Constant Radius: el mismo valor R se aplica a toda la longitud de la arista seleccionada", DARK, width=11.2)
        self.wait(EXPLAIN)
        self.remove_note(note)
        return edge, top_point, card

    def show_radius_on_top_face(self, hud):
        self.set_phase(hud, 6, "RADIO Y TANGENCIA", SKETCH)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.92, run_time=1.45)
        r = self.R8
        w, d = self.BASE_W / 2, self.BASE_D / 2
        center = np.array([w - r, d - r, self.BASE_H + 0.015])
        arc = Arc(radius=r, start_angle=0, angle=PI/2, arc_center=center, color=VALID, stroke_width=6)
        radius = Line(center, [w, d-r, self.BASE_H + 0.015], color=SKETCH, stroke_width=3)
        c = Dot(center, radius=0.055, color=SKETCH)
        tangent_a = Dot([w, d-r, self.BASE_H + 0.015], radius=0.055, color=VALID)
        tangent_b = Dot([w-r, d, self.BASE_H + 0.015], radius=0.055, color=VALID)
        label = self.text("R = 8 mm", 22, BOLD, SKETCH).next_to(radius, DOWN, buff=0.08)
        removed = Polygon(
            *self.removed_corner_points(r, z=self.BASE_H + 0.010),
            fill_color=REMOVE, fill_opacity=0.20, stroke_color=REMOVE, stroke_width=1.3,
        )
        self.play(FadeIn(removed), Create(radius), FadeIn(c), FadeIn(tangent_a), FadeIn(tangent_b), Write(label), run_time=1.05)
        self.play(Create(arc), run_time=1.15)
        note = self.note("El radio debe caber entre las caras vecinas sin colapsar ni autointersectar la geometría", VALID, width=12.0)
        self.wait(EXPLAIN)
        self.remove_note(note)
        return VGroup(arc, radius, c, tangent_a, tangent_b, label, removed)

    def form_fillet_3d(self, hud, body, selected_edge, selected_point, plan_marks, card):
        self.set_phase(hud, 7, "PREVIEW 3D · FORMACIÓN DEL FILLET", VALID)
        self.play(FadeOut(plan_marks), run_time=0.35)
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.90, run_time=1.55)

        removed_prism = self.extruded_polygon(
            self.removed_corner_points(self.R8, z=0.0), self.BASE_H,
            color=REMOVE, opacity=0.24, stroke=REMOVE,
        )
        self.play(FadeIn(removed_prism), selected_edge.animate.set_opacity(0.45), selected_point.animate.set_opacity(0.45), run_time=0.65)
        note = self.note("El volumen rojo se retira; en su lugar aparece una superficie curva tangente", REMOVE, width=10.9)
        self.wait(READ)
        self.remove_note(note)

        surface = self.fillet_surface(self.R8, VALID, 0.72, strips=22)
        self.play(LaggedStart(*[FadeIn(p) for p in surface], lag_ratio=0.055), run_time=2.75)
        self.wait(READ)

        final = self.extruded_polygon(self.one_corner_points(self.R8), self.BASE_H, STEEL, 0.95, DARK)
        self.play(FadeOut(body), FadeOut(removed_prism), FadeOut(surface), FadeOut(selected_edge), FadeOut(selected_point), FadeIn(final), run_time=1.20)
        note = self.note("Vista previa válida: la nueva cara mantiene tangencia con las dos caras originales", VALID, width=11.3)
        self.wait(EXPLAIN)
        self.remove_note(note)
        self.play(FadeOut(card), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        return final

    def validation_and_edit(self, hud, final):
        self.set_phase(hud, 8, "VALIDAR ANTES DE OK", DARK)
        valid = VGroup(
            self.text("✓  R = 8 mm", 24, BOLD, VALID),
            self.text("cabe en las caras vecinas", 18, NORMAL, DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        invalid = VGroup(
            self.text("✕  R demasiado grande", 24, BOLD, REMOVE),
            self.text("puede colapsar / intersectar caras", 18, NORMAL, DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cards = VGroup(valid, invalid).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.78)
        self.fixed(cards)
        self.play(Write(valid), run_time=0.85)
        self.play(Write(invalid), run_time=0.85)
        self.wait(EXPLAIN)
        self.clear_fixed_group(cards, run_time=0.40)

        self.set_phase(hud, 9, "OK · FILLET1 PARAMÉTRICO", VALID)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.65)
        note = self.note("Fillet1 queda después de Extrusion1 y puede editarse sin redibujar Sketch1", VALID, width=11.0)
        self.wait(READ)
        self.remove_note(note)

        bigger = self.extruded_polygon(self.one_corner_points(self.R12), self.BASE_H, STEEL_DARK, 0.95, DARK)
        tag = self.text("Edit Fillet1:  R 8 mm  →  12 mm", 23, BOLD, SKETCH).to_edge(DOWN, buff=0.75)
        self.fixed(tag)
        self.play(Write(tag), run_time=0.75)
        self.play(Transform(final, bigger), run_time=1.65, rate_func=smooth)
        self.wait(READ)
        back = self.extruded_polygon(self.one_corner_points(self.R8), self.BASE_H, STEEL, 0.95, DARK)
        self.play(Transform(final, back), run_time=1.35, rate_func=smooth)
        self.wait(MICRO)
        self.clear_fixed_group(tag, run_time=0.30)
        self.play(FadeOut(tree), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def final_summary(self, hud, final):
        self.set_phase(hud, 10, "RESULTADO FINAL", DARK)
        route_labels = ["Sketch1", "Extrusion1", "Edge1", "R = 8 mm", "Preview", "Fillet1"]
        route = VGroup()
        for label in route_labels:
            t = self.text(label, 17, BOLD)
            b = RoundedRectangle(
                width=max(1.45, t.width + 0.34), height=0.52, corner_radius=0.12,
                fill_color=WHITE, fill_opacity=0.97, stroke_color=DARK, stroke_width=1.0,
            )
            t.move_to(b)
            route.add(VGroup(b, t))
        route.arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.66)
        arrows = VGroup(*[
            Arrow(route[i].get_right(), route[i+1].get_left(), buff=0.05, color=DARK, stroke_width=1.5, max_tip_length_to_length_ratio=0.12)
            for i in range(len(route)-1)
        ])
        flow = VGroup(route, arrows)
        self.fixed(flow)
        self.play(LaggedStart(*[FadeIn(x) for x in route], lag_ratio=0.08), Create(arrows), run_time=1.35)
        note = self.note("FILLET = EDGE + RADIUS + TANGENT PREVIEW + PARAMETRIC FEATURE", DARK, width=10.8)
        self.wait(READ)
        self.remove_note(note)

        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(4.3)
        self.stop_ambient_camera_rotation()
        self.wait(OBSERVE)

    def construct(self):
        self.camera.background_color = WHITE
        self.opening()
        hud = self.top_hud()
        self.concept_2d(hud)
        body = self.build_base(hud)
        edge, point, card = self.select_edge_and_parameters(hud, body)
        plan_marks = self.show_radius_on_top_face(hud)
        final = self.form_fillet_3d(hud, body, edge, point, plan_marks, card)
        final = self.validation_and_edit(hud, final)
        self.final_summary(hud, final)
