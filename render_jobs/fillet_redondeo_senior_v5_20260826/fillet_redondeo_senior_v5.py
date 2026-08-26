from __future__ import annotations

import math
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK = "#303030"
MID = "#6D6D6D"
LIGHT = "#D7D7D7"
STEEL = "#B9C0C7"
STEEL_DARK = "#858F98"
SKETCH = "#2878B5"
VALID = "#2E8B57"
REMOVE = "#C0392B"
PAPER = "#FAFAFA"

TITLE = 54
BODY = 25
MICRO = 0.55
READ = 1.65
EXPLAIN = 2.35
OBSERVE = 2.80


class InventorFilletRedondeoSeniorV5(ThreeDScene):
    """Full senior lesson for Autodesk Inventor Fillet / Redondeo.

    Visual contract: House + Barrido + Solevacion + Revolucion.
    QA V5: larger text/model, safe margins, shorter phase labels, no competing
    captions, isolated parameter layout, granular steps, smooth 2D->3D flow,
    progressive material removal/surface creation, validation and parametric edit.
    """

    BASE_W = 6.35
    BASE_D = 3.85
    BASE_H = 0.96
    R8 = 0.66
    R12 = 0.95

    def text(self, content, size=BODY, weight=NORMAL, color=BLACK_TEXT):
        return Text(content, font_size=size, weight=weight, color=color)

    def fit(self, mob, max_w=14.9, max_h=7.6):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def assert_safe(self, mob, margin_x=0.18, margin_y=0.14):
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -8 + margin_x or right > 8 - margin_x:
            raise ValueError(f"Horizontal safe-area violation: {left=:.3f}, {right=:.3f}")
        if bottom < -4.5 + margin_y or top > 4.5 - margin_y:
            raise ValueError(f"Vertical safe-area violation: {bottom=:.3f}, {top=:.3f}")
        return mob

    def fixed(self, *mobs):
        for mob in mobs:
            self.assert_safe(mob)
        self.add_fixed_in_frame_mobjects(*mobs)

    def clear_fixed(self, mob, run_time=0.35):
        self.play(FadeOut(mob), run_time=run_time)
        self.remove_fixed_in_frame_mobjects(mob)
        self.remove(mob)

    def box(self, dims, center, color=STEEL, opacity=0.94, stroke=DARK, stroke_width=0.8):
        x, y, z = dims
        mob = Cube(side_length=1, fill_color=color, fill_opacity=opacity,
                   stroke_color=stroke, stroke_width=stroke_width)
        mob.stretch(x, 0).stretch(y, 1).stretch(z, 2)
        mob.move_to(np.array(center, dtype=float))
        return mob

    def one_corner_points(self, radius, z=0.0, samples=30):
        w, d = self.BASE_W / 2, self.BASE_D / 2
        r = min(radius, self.BASE_W * 0.28, self.BASE_D * 0.40)
        pts = [[-w, -d, z], [w, -d, z], [w, d-r, z]]
        cx, cy = w-r, d-r
        for a in np.linspace(0, PI/2, samples):
            pts.append([cx+r*math.cos(a), cy+r*math.sin(a), z])
        pts.append([-w, d, z])
        return [np.array(p, dtype=float) for p in pts]

    def removed_corner_points(self, radius, z=0.0, samples=30):
        w, d = self.BASE_W / 2, self.BASE_D / 2
        r = radius
        cx, cy = w-r, d-r
        pts = [[w, d-r, z], [w, d, z], [w-r, d, z]]
        for a in np.linspace(PI/2, 0, samples):
            pts.append([cx+r*math.cos(a), cy+r*math.sin(a), z])
        return [np.array(p, dtype=float) for p in pts]

    def extruded_polygon(self, points, height, color=STEEL, opacity=0.94, stroke=DARK):
        front = [np.array(p, dtype=float) for p in points]
        back = [p + OUT * height for p in front]
        f0 = Polygon(*front, fill_color=color, fill_opacity=opacity,
                     stroke_color=stroke, stroke_width=0.8)
        f1 = Polygon(*back, fill_color=color, fill_opacity=opacity,
                     stroke_color=stroke, stroke_width=0.8)
        sides = VGroup()
        for i in range(len(front)):
            j = (i+1) % len(front)
            sides.add(Polygon(front[i], front[j], back[j], back[i],
                              fill_color=color, fill_opacity=opacity,
                              stroke_color=stroke, stroke_width=0.8))
        return VGroup(f0, f1, sides)

    def fillet_surface(self, radius, opacity=0.78, strips=28):
        w, d = self.BASE_W / 2, self.BASE_D / 2
        r = radius
        cx, cy = w-r, d-r
        patches = VGroup()
        angles = np.linspace(0, PI/2, strips+1)
        for a0, a1 in zip(angles[:-1], angles[1:]):
            p00 = np.array([cx+r*math.cos(a0), cy+r*math.sin(a0), 0.0])
            p10 = np.array([cx+r*math.cos(a1), cy+r*math.sin(a1), 0.0])
            p01, p11 = p00 + OUT*self.BASE_H, p10 + OUT*self.BASE_H
            patches.add(Polygon(p00, p10, p11, p01,
                                fill_color=VALID, fill_opacity=opacity,
                                stroke_color=VALID, stroke_width=0.42))
        return patches

    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 28, BOLD, DARK)
        subtitle = self.text("FILLET / REDONDEO 3D · construcción y lógica paramétrica", 21, NORMAL, MID)
        title.to_corner(UL, buff=0.34)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.05)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.4).to_edge(UP, buff=1.08)
        phase_box = RoundedRectangle(width=5.65, height=0.62, corner_radius=0.11,
                                     fill_color=WHITE, fill_opacity=0.99,
                                     stroke_color=DARK, stroke_width=1.2).to_corner(UR, buff=0.34)
        phase = self.text("01 · IDEA DEL FILLET", 20, BOLD, DARK).move_to(phase_box)
        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.55)
        self.wait(READ)
        return {"group": group, "box": phase_box, "phase": phase}

    def set_phase(self, hud, number, label, color=DARK):
        old = hud["phase"]
        new = self.text(f"{number:02d} · {label}", 20, BOLD, color)
        if new.width > hud["box"].width - 0.35:
            new.scale_to_fit_width(hud["box"].width - 0.35)
        new.move_to(hud["box"])
        self.fixed(new)
        self.play(FadeOut(old, shift=UP*0.03), FadeIn(new, shift=UP*0.03), run_time=0.55)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        hud["phase"] = new
        self.wait(MICRO)

    def note(self, text, color=DARK, width=12.2, y=-3.42, font=22):
        label = self.text(text, font, BOLD, color)
        if label.width > width - 0.60:
            label.scale_to_fit_width(width - 0.60)
        box = RoundedRectangle(width=width, height=0.76, corner_radius=0.11,
                               fill_color=WHITE, fill_opacity=0.985,
                               stroke_color=color, stroke_width=1.25)
        label.move_to(box)
        group = VGroup(box, label).move_to([0, y, 0])
        self.fixed(group)
        self.play(FadeIn(box, shift=UP*0.06), Write(label), run_time=0.70)
        self.wait(MICRO)
        return group

    def small_callout(self, text, color=DARK, point=ORIGIN, width=4.4):
        label = self.text(text, 21, BOLD, color)
        if label.width > width - 0.4:
            label.scale_to_fit_width(width - 0.4)
        box = RoundedRectangle(width=width, height=0.62, corner_radius=0.10,
                               fill_color=WHITE, fill_opacity=0.97,
                               stroke_color=color, stroke_width=1.1)
        label.move_to(box)
        g = VGroup(box, label).move_to(point)
        self.fixed(g)
        return g

    def parameter_card(self):
        rows = [("Selection", "Edge1"), ("Radius", "8 mm"),
                ("Type", "Constant"), ("Continuity", "Tangent")]
        head = self.text("FILLET PARAMETERS", 25, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 20, BOLD, DARK)
            val = self.text(right, 20, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(width=2.55, height=0.52, corner_radius=0.05,
                                     fill_color=WHITE, fill_opacity=1,
                                     stroke_color=MID, stroke_width=1.0)
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.14)
            entries.add(VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.18))
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel = RoundedRectangle(width=5.15, height=content.height+0.55, corner_radius=0.11,
                                 fill_color=PAPER, fill_opacity=0.99,
                                 stroke_color=DARK, stroke_width=1.25)
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.28)
        group = VGroup(panel, content).move_to([5.20, -0.05, 0])
        self.fixed(group)
        return group

    def feature_tree(self):
        items = [("Part1.ipt", DARK, BOLD), ("Origin", MID, NORMAL),
                 ("Sketch1", MID, NORMAL), ("Extrusion1", DARK, NORMAL),
                 ("Fillet1   R = 8 mm", VALID, BOLD)]
        lines = VGroup(*[self.text(t, 20, w, c) for t, c, w in items]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        panel = RoundedRectangle(width=4.35, height=lines.height+0.55, corner_radius=0.09,
                                 fill_color=WHITE, fill_opacity=0.98,
                                 stroke_color=DARK, stroke_width=1.1)
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.26)
        group = VGroup(panel, lines).move_to([-5.45, -0.40, 0])
        self.fixed(group)
        return group

    def opening(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.0)
        top = self.text("DIBUJO TÉCNICO Y CAD", 28, BOLD, DARK)
        title = self.text("FILLET / REDONDEO", TITLE, BOLD)
        sub = self.text("De una arista viva a una transición tangente 3D", 30, NORMAL, MID)
        rule = Line(LEFT*5.85, RIGHT*5.85, color=BLACK, stroke_width=2)
        route_text = self.text("SKETCH  →  EXTRUDE  →  EDGE  →  RADIUS  →  PREVIEW  →  FILLET1", 24, BOLD, DARK)
        group = VGroup(top, title, rule, sub, route_text).arrange(DOWN, buff=0.34)
        self.fit(group, 13.6, 6.2)
        self.fixed(group)
        self.play(FadeIn(top, shift=UP*0.08), run_time=0.75)
        self.play(Write(title), run_time=1.15)
        self.play(Create(rule), Write(sub), run_time=0.95)
        self.play(Write(route_text), run_time=1.30)
        self.wait(EXPLAIN)
        self.clear_fixed(group, run_time=0.60)

    def concept_problem(self, hud):
        self.set_phase(hud, 1, "IDEA DEL FILLET", DARK)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1.02)
        corner = np.array([1.50, 0.85, 0])
        top_edge = Line([-3.25, 0.85, 0], corner, color=DARK, stroke_width=6)
        right_edge = Line([1.50, -2.05, 0], corner, color=DARK, stroke_width=6)
        sharp = Dot(corner, radius=0.095, color=REMOVE)
        call = self.small_callout("ARISTA VIVA", REMOVE, point=[-2.55, -1.55, 0], width=3.45)
        arrow = Arrow(call.get_top(), corner+LEFT*0.10+DOWN*0.10, buff=0.16,
                      color=REMOVE, stroke_width=2.2)
        self.fixed(arrow)
        self.play(Create(top_edge), Create(right_edge), FadeIn(sharp), run_time=1.05)
        self.play(FadeIn(call), GrowArrow(arrow), run_time=0.85)
        note = self.note("Fillet modifica una ARISTA existente; no crea el sólido base.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(call, 0.25)
        self.clear_fixed(arrow, 0.25)
        return VGroup(top_edge, right_edge, sharp), corner

    def concept_geometry(self, hud, sharp_geom, corner):
        self.set_phase(hud, 2, "RADIO + TANGENCIA", SKETCH)
        r = 1.20
        center = corner + np.array([-r, -r, 0])
        radius_line = Line(center, [corner[0], corner[1]-r, 0], color=SKETCH, stroke_width=3.4)
        c_dot = Dot(center, radius=0.07, color=SKETCH)
        t_right = Dot([corner[0], corner[1]-r, 0], radius=0.065, color=VALID)
        t_top = Dot([corner[0]-r, corner[1], 0], radius=0.065, color=VALID)
        arc = Arc(radius=r, start_angle=0, angle=PI/2, arc_center=center,
                  color=VALID, stroke_width=8)
        r_label = self.text("R = 8 mm", 27, BOLD, SKETCH).next_to(radius_line, DOWN, buff=0.10)
        tangent_word = self.small_callout("TANGENTE A AMBAS CARAS", VALID,
                                          point=[-1.85, -1.62, 0], width=5.2)
        self.play(Create(radius_line), FadeIn(c_dot), Write(r_label), run_time=0.95)
        self.play(FadeIn(t_right), FadeIn(t_top), run_time=0.45)
        self.play(Create(arc), run_time=1.45, rate_func=smooth)
        self.play(FadeIn(tangent_word), run_time=0.65)
        note = self.note("La esquina se reemplaza por un arco de radio constante, conectado sin quiebre.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(tangent_word, 0.25)
        self.play(FadeOut(sharp_geom), FadeOut(radius_line), FadeOut(c_dot),
                  FadeOut(t_right), FadeOut(t_top), FadeOut(arc), FadeOut(r_label), run_time=0.55)

    def sketch_base(self, hud):
        self.set_phase(hud, 3, "SKETCH1 · PERFIL", SKETCH)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.02, run_time=0.85)
        w, d = self.BASE_W, self.BASE_D
        outline = Rectangle(width=w, height=d, stroke_color=SKETCH, stroke_width=5.2)
        origin = Dot(ORIGIN, radius=0.065, color=REMOVE)
        h_axis = DashedLine([-w/2-0.35, 0, 0], [w/2+0.35, 0, 0], color=LIGHT,
                            dash_length=0.12, stroke_width=1.5)
        v_axis = DashedLine([0, -d/2-0.25, 0], [0, d/2+0.25, 0], color=LIGHT,
                            dash_length=0.12, stroke_width=1.5)
        status = self.small_callout("Sketch1 · CLOSED PROFILE", SKETCH,
                                    point=[0, 2.55, 0], width=5.25)
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
        d1 = DoubleArrow([-w/2, -d/2-0.48, 0], [w/2, -d/2-0.48, 0], buff=0,
                         color=DARK, stroke_width=2.2)
        d2 = DoubleArrow([w/2+0.50, -d/2, 0], [w/2+0.50, d/2, 0], buff=0,
                         color=DARK, stroke_width=2.2)
        l1 = self.text("80 mm", 24, BOLD).next_to(d1, DOWN, buff=0.08)
        l2 = self.text("50 mm", 24, BOLD).rotate(PI/2).next_to(d2, RIGHT, buff=0.08)
        fully = self.small_callout("FULLY CONSTRAINED", VALID,
                                   point=[-2.15, 2.58, 0], width=4.45)
        self.play(Create(d1), Write(l1), run_time=0.75)
        self.play(Create(d2), Write(l2), run_time=0.75)
        self.play(FadeIn(fully), run_time=0.55)
        note = self.note("Paso 2: fija tamaño y posición. Todavía NO existe Fillet1.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(fully, 0.25)
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(l1), FadeOut(l2), run_time=0.35)

    def extrude_base(self, hud, outline, origin, h_axis, v_axis):
        self.set_phase(hud, 5, "EXTRUDE · 12 mm", VALID)
        note = self.note("Finish Sketch  →  Extrude = 12 mm  →  Join  →  Extrusion1", VALID)
        self.move_camera(phi=62*DEGREES, theta=-48*DEGREES, zoom=1.02, run_time=1.65)
        seed = self.box((self.BASE_W, self.BASE_D, 0.04), (0,0,0.02), STEEL, 0.80)
        target = self.box((self.BASE_W, self.BASE_D, self.BASE_H),
                          (0,0,self.BASE_H/2), STEEL, 0.94)
        self.add(seed)
        self.play(Transform(seed, target),
                  outline.animate.shift(OUT*self.BASE_H).set_opacity(0.18),
                  run_time=2.45, rate_func=smooth)
        self.wait(READ)
        self.clear_fixed(note)
        self.play(FadeOut(outline), FadeOut(origin), FadeOut(h_axis), FadeOut(v_axis), run_time=0.40)
        return seed

    def select_edge(self, hud, body):
        self.set_phase(hud, 6, "SELECCIONAR EDGE1", SKETCH)
        w, d, h = self.BASE_W, self.BASE_D, self.BASE_H
        edge = Line3D([w/2, d/2, 0], [w/2, d/2, h], color=SKETCH, thickness=0.065)
        p0 = Dot3D([w/2, d/2, 0], radius=0.075, color=SKETCH)
        p1 = Dot3D([w/2, d/2, h], radius=0.075, color=SKETCH)
        self.play(Create(edge), FadeIn(p0), FadeIn(p1), run_time=0.85)
        self.play(body.animate.shift(LEFT*1.00), edge.animate.shift(LEFT*1.00),
                  p0.animate.shift(LEFT*1.00), p1.animate.shift(LEFT*1.00), run_time=0.85)
        label = self.small_callout("EDGE1", SKETCH, point=[4.75, 1.70, 0], width=2.4)
        self.play(FadeIn(label), run_time=0.45)
        note = self.note("Paso 3: selecciona la arista 3D que realmente quieres suavizar.", SKETCH)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(label, 0.25)
        return edge, p0, p1

    def command_parameters(self, hud):
        self.set_phase(hud, 7, "MODIFY · FILLET", DARK)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.65)
        note = self.note("Paso 4: 3D Model → Modify → Fillet. Define Edge1 y Radius = 8 mm.", DARK)
        self.wait(READ)
        self.clear_fixed(note)
        constant = self.small_callout("CONSTANT RADIUS", DARK,
                                      point=[5.15, -2.35, 0], width=4.25)
        self.play(FadeIn(constant), run_time=0.45)
        note = self.note("Constant Radius = el mismo radio se aplica a toda la longitud de Edge1.", DARK)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(constant, 0.25)
        return card

    def radius_on_face(self, hud, body, edge, p0, p1, card):
        self.set_phase(hud, 8, "COMPROBAR RADIO", SKETCH)
        self.play(FadeOut(card), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)
        self.play(body.animate.shift(RIGHT*1.00), edge.animate.shift(RIGHT*1.00),
                  p0.animate.shift(RIGHT*1.00), p1.animate.shift(RIGHT*1.00), run_time=0.70)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.04, run_time=1.45)
        r = self.R8
        w, d = self.BASE_W/2, self.BASE_D/2
        center = np.array([w-r, d-r, self.BASE_H+0.02])
        removed = Polygon(*self.removed_corner_points(r, self.BASE_H+0.014),
                          fill_color=REMOVE, fill_opacity=0.20,
                          stroke_color=REMOVE, stroke_width=1.4)
        radius = Line(center, [w, d-r, self.BASE_H+0.02], color=SKETCH, stroke_width=3.4)
        arc = Arc(radius=r, start_angle=0, angle=PI/2, arc_center=center,
                  color=VALID, stroke_width=7)
        c = Dot(center, radius=0.06, color=SKETCH)
        ta = Dot([w, d-r, self.BASE_H+0.02], radius=0.06, color=VALID)
        tb = Dot([w-r, d, self.BASE_H+0.02], radius=0.06, color=VALID)
        label = self.text("R = 8 mm", 25, BOLD, SKETCH).next_to(radius, DOWN, buff=0.08)
        self.play(FadeIn(removed), run_time=0.55)
        self.play(Create(radius), FadeIn(c), Write(label), run_time=0.75)
        self.play(FadeIn(ta), FadeIn(tb), Create(arc), run_time=1.25)
        note = self.note("Paso 5: verifica que R cabe entre las caras vecinas y conserva tangencia.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return VGroup(removed, radius, arc, c, ta, tb, label)

    def preview_3d(self, hud, body, edge, p0, p1, marks):
        self.set_phase(hud, 9, "PREVIEW 3D", VALID)
        self.play(FadeOut(marks), run_time=0.35)
        self.move_camera(phi=64*DEGREES, theta=-46*DEGREES, zoom=1.05, run_time=1.55)
        removed_prism = self.extruded_polygon(self.removed_corner_points(self.R8),
                                              self.BASE_H, REMOVE, 0.27, REMOVE)
        self.play(FadeIn(removed_prism), run_time=0.65)
        note = self.note("Paso 6A: el volumen rojo representa el material que desaparece.", REMOVE)
        self.wait(READ)
        self.clear_fixed(note)
        surface = self.fillet_surface(self.R8, opacity=0.80, strips=30)
        note = self.note("Paso 6B: la nueva superficie tangente se genera progresivamente sobre Edge1.", VALID)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT*0.02) for p in surface], lag_ratio=0.040),
                  removed_prism.animate.set_opacity(0.10),
                  edge.animate.set_opacity(0.25), p0.animate.set_opacity(0.25),
                  p1.animate.set_opacity(0.25), run_time=3.25, rate_func=smooth)
        self.wait(READ)
        self.clear_fixed(note)
        final = self.extruded_polygon(self.one_corner_points(self.R8),
                                      self.BASE_H, STEEL, 0.96, DARK)
        self.play(FadeOut(body), FadeOut(removed_prism), FadeOut(surface),
                  FadeOut(edge), FadeOut(p0), FadeOut(p1), FadeIn(final), run_time=1.15)
        note = self.note("Preview válido: no hay arista viva; aparece una transición continua de R = 8 mm.", VALID)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        return final

    def validate(self, hud, final):
        self.set_phase(hud, 10, "VALIDAR ANTES DE OK", DARK)
        ok_head = self.text("VÁLIDO", 27, BOLD, VALID)
        ok_lines = VGroup(self.text("R = 8 mm", 22, BOLD, DARK),
                          self.text("cabe entre las caras", 20, NORMAL, DARK),
                          self.text("sin autointersección", 20, NORMAL, DARK)).arrange(
                              DOWN, aligned_edge=LEFT, buff=0.10)
        ok = VGroup(ok_head, ok_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ok_box = SurroundingRectangle(ok, buff=0.24, corner_radius=0.10,
                                      color=VALID, stroke_width=1.4)
        ok_card = VGroup(ok_box, ok).move_to([-3.4, -2.15, 0])
        bad_head = self.text("NO VÁLIDO", 27, BOLD, REMOVE)
        bad_lines = VGroup(self.text("R demasiado grande", 22, BOLD, DARK),
                           self.text("colapsa una cara", 20, NORMAL, DARK),
                           self.text("o genera intersección", 20, NORMAL, DARK)).arrange(
                               DOWN, aligned_edge=LEFT, buff=0.10)
        bad = VGroup(bad_head, bad_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        bad_box = SurroundingRectangle(bad, buff=0.24, corner_radius=0.10,
                                       color=REMOVE, stroke_width=1.4)
        bad_card = VGroup(bad_box, bad).move_to([3.4, -2.15, 0])
        cards = VGroup(ok_card, bad_card)
        self.fixed(cards)
        self.play(FadeIn(ok_box), Write(ok), run_time=0.85)
        self.wait(0.60)
        self.play(FadeIn(bad_box), Write(bad), run_time=0.85)
        self.wait(EXPLAIN)
        self.clear_fixed(cards, 0.45)
        return final

    def parametric_edit(self, hud, final):
        self.set_phase(hud, 11, "OK · FILLET1", VALID)
        self.play(final.animate.shift(RIGHT*1.15), run_time=0.70)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.65)
        note = self.note("Paso 7: OK crea Fillet1 después de Extrusion1 en el árbol paramétrico.", VALID)
        self.wait(READ)
        self.clear_fixed(note)
        edit = self.small_callout("EDIT FILLET1", SKETCH, point=[0.2, -2.25, 0], width=3.8)
        self.play(FadeIn(edit), run_time=0.45)
        bigger = self.extruded_polygon(self.one_corner_points(self.R12),
                                       self.BASE_H, STEEL_DARK, 0.96, DARK).shift(RIGHT*1.15)
        change = self.small_callout("R: 8 mm  →  12 mm", SKETCH,
                                    point=[0.2, -3.02, 0], width=4.7)
        self.play(FadeIn(change), run_time=0.45)
        self.play(Transform(final, bigger), run_time=1.85, rate_func=smooth)
        self.wait(READ)
        note = self.note("La pieza se actualiza sin redibujar Sketch1: eso es diseño paramétrico.",
                         DARK, y=-3.78)
        self.wait(EXPLAIN)
        self.clear_fixed(note)
        back = self.extruded_polygon(self.one_corner_points(self.R8),
                                     self.BASE_H, STEEL, 0.96, DARK).shift(RIGHT*1.15)
        self.play(Transform(final, back), run_time=1.55, rate_func=smooth)
        self.wait(MICRO)
        self.clear_fixed(edit, 0.25)
        self.clear_fixed(change, 0.25)
        self.play(FadeOut(tree), final.animate.shift(LEFT*1.15), run_time=0.55)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final

    def final_summary(self, hud, final):
        self.set_phase(hud, 12, "INSPECCIÓN FINAL", DARK)
        summary = self.text("Sketch1  →  Extrusion1  →  Edge1  →  R = 8 mm  →  Preview  →  Fillet1",
                            23, BOLD, DARK).to_edge(DOWN, buff=0.34)
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
        marks = self.radius_on_face(hud, body, edge, p0, p1, card)
        final = self.preview_3d(hud, body, edge, p0, p1, marks)
        final = self.validate(hud, final)
        final = self.parametric_edit(hud, final)
        self.final_summary(hud, final)
