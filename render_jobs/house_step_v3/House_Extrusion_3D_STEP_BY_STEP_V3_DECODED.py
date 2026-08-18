#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Senior step-by-step CAD house construction in ManimCE 0.20.x.

Sequence:
1. Terrain/grid only.
2. Draw slab footprint on terrain.
3. Positive extrusion: slab.
4. Draw wall + column sketches ON the slab top face.
5. Positive extrusion: columns.
6. Positive extrusion: perimeter walls, then interior walls.
7. Negative extrusion: doorway.
8. Negative extrusion: window.
9. Positive extrusion: roof slab.
10. Final orbit + CAD operation summary.
"""

from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D7D7D7"
TERRAIN = "#E8EEE5"
SLAB = "#B8BEC5"
COLUMN = "#4F5B66"
WALL = "#E5E7E9"
SKETCH = "#2878B5"
POSITIVE = "#2E8B57"
NEGATIVE = "#C0392B"
GLASS = "#BFD7EA"


class HouseExtrusion3D(ThreeDScene):
    FLOOR_Z = 0.30
    WALL_H = 2.75
    WALL_T = 0.18
    COL_H = 3.05
    COL_S = 0.28
    HOUSE_W = 9.20
    HOUSE_D = 6.20

    def box(self, dims, center, color, opacity=1.0, stroke=DARK, stroke_width=0.8):
        x, y, z = dims
        mob = Cube(
            side_length=1.0,
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=stroke,
            stroke_width=stroke_width,
        )
        mob.stretch(x, 0).stretch(y, 1).stretch(z, 2)
        mob.move_to(np.array(center, dtype=float))
        return mob

    def text(self, content, size=28, weight=NORMAL, color=BLACK_TEXT):
        return Text(content, font_size=size, weight=weight, color=color)

    # ------------------------------------------------------------------
    # HUD: create/recreate fixed text instead of morphing glyph geometry.
    # ------------------------------------------------------------------
    def fixed_hud(self):
        title = self.text("MODELADO CAD · VIVIENDA 3D", 30, BOLD)
        subtitle = self.text("Extrusión positiva y negativa · construcción paso a paso", 19, NORMAL, MID)
        title.to_corner(UL, buff=0.38)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)

        rule = Line(LEFT * 7.55, RIGHT * 7.55, color=LIGHT, stroke_width=1.3)
        rule.to_edge(UP, buff=1.08)

        box = RoundedRectangle(
            width=5.75, height=0.52, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.97,
            stroke_color=DARK, stroke_width=1.1,
        ).to_corner(UR, buff=0.40)
        phase = self.text("01 · PREPARAR TERRENO", 19, BOLD).move_to(box)

        add_dot = Circle(radius=0.07, fill_color=POSITIVE, fill_opacity=1, stroke_width=0)
        add_text = self.text("+  AÑADIR MATERIAL", 17, BOLD, POSITIVE)
        rem_dot = Circle(radius=0.07, fill_color=NEGATIVE, fill_opacity=1, stroke_width=0)
        rem_text = self.text("−  RETIRAR MATERIAL", 17, BOLD, NEGATIVE)
        legend = VGroup(add_dot, add_text, rem_dot, rem_text).arrange(RIGHT, buff=0.25)
        legend.to_edge(DOWN, buff=0.25)

        for mob in (title, subtitle, rule, box, phase, legend):
            self.add_fixed_in_frame_mobjects(mob)
        return {"box": box, "text": phase}

    def set_phase(self, state, number, label, color=DARK):
        old = state["text"]
        new = self.text(f"{number:02d} · {label}", 19, BOLD, color).move_to(state["box"])
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=0.38)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        state["text"] = new

    # ------------------------------------------------------------------
    # 2D CAD sketches
    # ------------------------------------------------------------------
    def slab_outline(self, z=0.045):
        w, d = self.HOUSE_W, self.HOUSE_D
        p = [
            [-w/2, -d/2, z], [w/2, -d/2, z],
            [w/2, d/2, z], [-w/2, d/2, z]
        ]
        return VGroup(*[
            Line(p[i], p[(i + 1) % 4], color=SKETCH, stroke_width=4.2)
            for i in range(4)
        ])

    def wall_trace(self, z):
        w, d = self.HOUSE_W, self.HOUSE_D
        p = [
            [-w/2, -d/2, z], [w/2, -d/2, z],
            [w/2, d/2, z], [-w/2, d/2, z]
        ]
        exterior = VGroup(*[
            Line(p[i], p[(i + 1) % 4], color=SKETCH, stroke_width=3.6)
            for i in range(4)
        ])
        specs = [
            ((0.70, -2.55), (0.70, 2.35)),
            ((-4.05, 0.75), (0.70, 0.75)),
            ((0.70, 0.75), (4.05, 0.75)),
            ((-1.90, 0.75), (-1.90, 2.70)),
        ]
        interior = VGroup(*[
            Line([a[0], a[1], z], [b[0], b[1], z], color=SKETCH, stroke_width=3.0)
            for a, b in specs
        ])
        return exterior, interior

    def column_specs(self):
        xvals = [-4.35, 0.70, 4.35]
        yvals = [-2.85, 0.75, 2.85]
        return [(x, y) for x in xvals for y in yvals]

    def column_profiles(self, z):
        profiles = VGroup()
        for x, y in self.column_specs():
            s = Square(
                side_length=self.COL_S * 1.18,
                stroke_color=SKETCH, stroke_width=3.2,
                fill_color=SKETCH, fill_opacity=0.08,
            ).move_to([x, y, z])
            profiles.add(s)
        return profiles

    # ------------------------------------------------------------------
    # 3D wall states
    # ------------------------------------------------------------------
    def wall_specs(self):
        w, d, t = self.HOUSE_W, self.HOUSE_D, self.WALL_T
        zc = self.FLOOR_Z + self.WALL_H / 2
        exterior = [
            ((w, t, self.WALL_H), (0, -d/2, zc)),
            ((w, t, self.WALL_H), (0,  d/2, zc)),
            ((t, d - 2*t, self.WALL_H), (-w/2, 0, zc)),
            ((t, d - 2*t, self.WALL_H), ( w/2, 0, zc)),
        ]
        interior = [
            ((t, 4.90, self.WALL_H), (0.70, -0.10, zc)),
            ((4.75, t, self.WALL_H), (-1.675, 0.75, zc)),
            ((3.35, t, self.WALL_H), (2.375, 0.75, zc)),
            ((t, 1.95, self.WALL_H), (-1.90, 1.725, zc)),
        ]
        return exterior, interior

    def make_wall_extrusion(self, specs):
        seeds, targets = [], []
        h0 = 0.025
        for dims, center in specs:
            dx, dy, dz = dims
            seeds.append(self.box((dx, dy, h0), (center[0], center[1], self.FLOOR_Z + h0/2), WALL, 0.96))
            targets.append(self.box(dims, center, WALL, 0.97))
        return seeds, targets

    def front_after_door(self):
        y, t, z0 = -self.HOUSE_D/2, self.WALL_T, self.FLOOR_Z
        top = z0 + self.WALL_H
        dl, dr, dt = -2.55, -1.35, z0 + 2.15
        return VGroup(
            self.box((dl + self.HOUSE_W/2, t, self.WALL_H), ((-self.HOUSE_W/2 + dl)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((self.HOUSE_W/2 - dr, t, self.WALL_H), ((dr + self.HOUSE_W/2)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((dr-dl, t, top-dt), ((dl+dr)/2, y, (dt+top)/2), WALL, 0.97),
        )

    def front_final(self):
        y, t, z0 = -self.HOUSE_D/2, self.WALL_T, self.FLOOR_Z
        top = z0 + self.WALL_H
        dl, dr, dt = -2.55, -1.35, z0 + 2.15
        wl, wr = 1.30, 3.15
        wb, wt = z0 + 0.88, z0 + 2.05
        return VGroup(
            self.box((dl + self.HOUSE_W/2, t, self.WALL_H), ((-self.HOUSE_W/2 + dl)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((wl-dr, t, self.WALL_H), ((dr+wl)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((self.HOUSE_W/2-wr, t, self.WALL_H), ((wr+self.HOUSE_W/2)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((dr-dl, t, top-dt), ((dl+dr)/2, y, (dt+top)/2), WALL, 0.97),
            self.box((wr-wl, t, wb-z0), ((wl+wr)/2, y, (z0+wb)/2), WALL, 0.97),
            self.box((wr-wl, t, top-wt), ((wl+wr)/2, y, (wt+top)/2), WALL, 0.97),
        )

    def vertical_profile(self, x_center, width, bottom, height, y_plane):
        rect = Rectangle(
            width=width, height=height,
            stroke_color=NEGATIVE, stroke_width=4.2,
            fill_color=NEGATIVE, fill_opacity=0.10,
        )
        rect.rotate(PI/2, axis=RIGHT)
        rect.move_to([x_center, y_plane, bottom + height/2])
        return rect

    def cutter_front(self, x_center, width, bottom, height):
        depth = 0.95
        y_front = -self.HOUSE_D/2
        return self.box(
            (width, depth, height),
            (x_center, y_front + 0.18, bottom + height/2),
            NEGATIVE, 0.25, stroke=NEGATIVE, stroke_width=1.8,
        )

    def phase_note(self, text, color=DARK):
        box = RoundedRectangle(
            width=6.4, height=0.64, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.94,
            stroke_color=color, stroke_width=1.2,
        ).to_edge(DOWN, buff=0.58)
        label = self.text(text, 20, BOLD, color).move_to(box)
        group = VGroup(box, label)
        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group, shift=UP*0.08), run_time=0.45)
        return group

    def remove_note(self, note):
        self.play(FadeOut(note), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(note)
        self.remove(note)

    # ------------------------------------------------------------------
    # MAIN NARRATIVE
    # ------------------------------------------------------------------
    def construct(self):
        self.camera.background_color = WHITE
        phase = self.fixed_hud()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=0.80)

        # 01 — terrain only
        terrain = self.box((11.2, 8.2, 0.16), (0, 0, -0.08), TERRAIN, 1.0, stroke=LIGHT, stroke_width=0.7)
        self.play(FadeIn(terrain), run_time=0.8)
        grid = VGroup()
        for x in np.arange(-5.0, 5.01, 1.0):
            grid.add(Line([x, -3.65, 0.015], [x, 3.65, 0.015], color=LIGHT, stroke_width=0.65))
        for y in np.arange(-3.5, 3.51, 1.0):
            grid.add(Line([-5.15, y, 0.015], [5.15, y, 0.015], color=LIGHT, stroke_width=0.65))
        self.play(Create(grid), run_time=1.3)
        note = self.phase_note("Primero creamos una superficie de referencia")
        self.wait(1.1)
        self.remove_note(note)

        # 02 — slab footprint only
        self.set_phase(phase, 2, "CROQUIS · LOSA", SKETCH)
        slab_sketch = self.slab_outline(z=0.045)
        note = self.phase_note("Croquis 2D cerrado sobre el terreno", SKETCH)
        self.play(LaggedStart(*[Create(m) for m in slab_sketch], lag_ratio=0.16), run_time=2.3)
        self.wait(1.1)
        self.remove_note(note)

        # 03 — slab positive extrusion
        self.set_phase(phase, 3, "EXTRUSIÓN + · LOSA", POSITIVE)
        self.move_camera(phi=56*DEGREES, theta=-52*DEGREES, zoom=0.72, run_time=2.0)
        note = self.phase_note("El perfil cerrado gana espesor: + material", POSITIVE)
        slab_seed = self.box((self.HOUSE_W+0.25, self.HOUSE_D+0.25, 0.025), (0,0,0.0125), SLAB, 0.96)
        slab_target = self.box((self.HOUSE_W+0.25, self.HOUSE_D+0.25, self.FLOOR_Z), (0,0,self.FLOOR_Z/2), SLAB, 0.96)
        self.add(slab_seed)
        self.play(Transform(slab_seed, slab_target), slab_sketch.animate.shift(OUT*self.FLOOR_Z), run_time=2.2, rate_func=smooth)
        slab = slab_seed
        self.wait(1.0)
        self.remove_note(note)
        self.play(FadeOut(slab_sketch), run_time=0.5)

        # 04 — NEW sketch on the top face of slab
        self.set_phase(phase, 4, "CROQUIS · MUROS + COLUMNAS", SKETCH)
        self.move_camera(phi=36*DEGREES, theta=-58*DEGREES, zoom=0.75, run_time=1.6)
        zsk = self.FLOOR_Z + 0.025
        ext_trace, int_trace = self.wall_trace(zsk)
        col_profiles = self.column_profiles(zsk + 0.003)
        note = self.phase_note("Nueva cara activa: dibujamos encima de la losa", SKETCH)
        self.play(LaggedStart(*[Create(m) for m in ext_trace], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[Create(m) for m in int_trace], lag_ratio=0.12), run_time=1.6)
        self.play(LaggedStart(*[Create(m) for m in col_profiles], lag_ratio=0.07), run_time=2.0)
        self.wait(1.6)
        self.remove_note(note)

        # 05 — columns
        self.set_phase(phase, 5, "EXTRUSIÓN + · COLUMNAS", POSITIVE)
        note = self.phase_note("Cada cuadrado se extruye verticalmente", POSITIVE)
        col_seeds, col_targets = [], []
        h0 = 0.03
        for x, y in self.column_specs():
            col_seeds.append(self.box((self.COL_S,self.COL_S,h0), (x,y,self.FLOOR_Z+h0/2), COLUMN, 0.98))
            col_targets.append(self.box((self.COL_S,self.COL_S,self.COL_H), (x,y,self.FLOOR_Z+self.COL_H/2), COLUMN, 0.98))
        self.add(*col_seeds)
        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(col_seeds,col_targets)], lag_ratio=0.10), run_time=3.6, rate_func=smooth)
        self.play(FadeOut(col_profiles), run_time=0.5)
        self.wait(0.9)
        self.remove_note(note)

        # 06 — perimeter then internal walls
        self.set_phase(phase, 6, "EXTRUSIÓN + · MUROS", POSITIVE)
        ext_specs, int_specs = self.wall_specs()
        ext_seeds, ext_targets = self.make_wall_extrusion(ext_specs)
        int_seeds, int_targets = self.make_wall_extrusion(int_specs)

        note = self.phase_note("Primero perímetro exterior", POSITIVE)
        self.add(*ext_seeds)
        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(ext_seeds,ext_targets)], lag_ratio=0.10), run_time=3.7, rate_func=smooth)
        self.remove_note(note)
        self.play(FadeOut(ext_trace), run_time=0.45)

        note = self.phase_note("Después divisiones interiores", POSITIVE)
        self.add(*int_seeds)
        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(int_seeds,int_targets)], lag_ratio=0.11), run_time=3.4, rate_func=smooth)
        self.play(FadeOut(int_trace), run_time=0.45)
        self.wait(0.8)
        self.remove_note(note)

        front_wall = ext_seeds[0]
        other_walls = VGroup(*ext_seeds[1:], *int_seeds)

        # 07 — negative extrusion door
        self.set_phase(phase, 7, "EXTRUSIÓN − · PUERTA", NEGATIVE)
        self.move_camera(phi=66*DEGREES, theta=-55*DEGREES, zoom=0.78, run_time=1.8)
        door_x, door_w = -1.95, 1.20
        door_bottom, door_h = self.FLOOR_Z, 2.15
        profile = self.vertical_profile(door_x, door_w, door_bottom, door_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Perfil rojo = volumen que será retirado", NEGATIVE)
        self.play(Create(profile), run_time=1.2)
        cutter = self.cutter_front(door_x, door_w, door_bottom, door_h)
        cutter.shift(DOWN*0.95)  # outside facade: negative Y
        self.play(FadeIn(cutter), run_time=0.4)
        self.play(front_wall.animate.set_fill(opacity=0.42), run_time=0.45)
        self.play(cutter.animate.shift(UP*0.95), run_time=1.8, rate_func=smooth)
        after_door = self.front_after_door()
        self.play(FadeOut(front_wall), FadeIn(after_door), FadeOut(cutter), FadeOut(profile), run_time=0.9)
        front_wall = after_door
        self.wait(1.0)
        self.remove_note(note)

        # 08 — negative extrusion window
        self.set_phase(phase, 8, "EXTRUSIÓN − · VENTANA", NEGATIVE)
        win_x, win_w = 2.225, 1.85
        win_bottom, win_h = self.FLOOR_Z + 0.88, 1.17
        profile2 = self.vertical_profile(win_x, win_w, win_bottom, win_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Misma operación: croquis → profundidad → corte", NEGATIVE)
        self.play(Create(profile2), run_time=1.1)
        cutter2 = self.cutter_front(win_x, win_w, win_bottom, win_h)
        cutter2.shift(DOWN*0.95)
        self.play(FadeIn(cutter2), run_time=0.4)
        self.play(front_wall.animate.set_opacity(0.48), run_time=0.45)
        self.play(cutter2.animate.shift(UP*0.95), run_time=1.7, rate_func=smooth)
        final_front = self.front_final()
        self.play(FadeOut(front_wall), FadeIn(final_front), FadeOut(cutter2), FadeOut(profile2), run_time=0.9)
        front_wall = final_front
        glass = self.box((win_w*0.94,0.035,win_h*0.94), (win_x,-self.HOUSE_D/2+0.01,win_bottom+win_h/2), GLASS, 0.42, stroke=SKETCH, stroke_width=0.8)
        self.play(FadeIn(glass), run_time=0.55)
        self.wait(1.0)
        self.remove_note(note)

        # 09 — roof positive extrusion
        self.set_phase(phase, 9, "EXTRUSIÓN + · CUBIERTA", POSITIVE)
        note = self.phase_note("Última operación aditiva: cubierta", POSITIVE)
        roof_base = self.FLOOR_Z + self.COL_H
        roof_outline = VGroup(*[
            Line(a,b,color=SKETCH,stroke_width=3.3) for a,b in [
                ([-self.HOUSE_W/2-0.22,-self.HOUSE_D/2-0.22,roof_base+0.02],[self.HOUSE_W/2+0.22,-self.HOUSE_D/2-0.22,roof_base+0.02]),
                ([self.HOUSE_W/2+0.22,-self.HOUSE_D/2-0.22,roof_base+0.02],[self.HOUSE_W/2+0.22,self.HOUSE_D/2+0.22,roof_base+0.02]),
                ([self.HOUSE_W/2+0.22,self.HOUSE_D/2+0.22,roof_base+0.02],[-self.HOUSE_W/2-0.22,self.HOUSE_D/2+0.22,roof_base+0.02]),
                ([-self.HOUSE_W/2-0.22,self.HOUSE_D/2+0.22,roof_base+0.02],[-self.HOUSE_W/2-0.22,-self.HOUSE_D/2-0.22,roof_base+0.02]),
            ]
        ])
        self.play(LaggedStart(*[Create(m) for m in roof_outline], lag_ratio=0.14), run_time=1.5)
        roof_seed = self.box((self.HOUSE_W+0.45,self.HOUSE_D+0.45,0.025), (0,0,roof_base+0.0125), SLAB, 0.72)
        roof_target = self.box((self.HOUSE_W+0.45,self.HOUSE_D+0.45,0.24), (0,0,roof_base+0.12), SLAB, 0.72)
        self.add(roof_seed)
        self.play(Transform(roof_seed, roof_target), FadeOut(roof_outline), run_time=2.1, rate_func=smooth)
        self.play(roof_seed.animate.set_fill(opacity=0.22), run_time=0.8)
        self.wait(0.8)
        self.remove_note(note)

        # 10 — final verification orbit
        self.set_phase(phase, 10, "MODELO 3D COMPLETO", DARK)
        self.move_camera(phi=63*DEGREES, theta=-50*DEGREES, zoom=0.72, run_time=1.8)
        self.begin_ambient_camera_rotation(rate=0.085)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()

        summary_box = RoundedRectangle(
            width=7.2, height=1.20, corner_radius=0.12,
            fill_color=WHITE, fill_opacity=0.96,
            stroke_color=DARK, stroke_width=1.3,
        ).to_edge(DOWN, buff=0.50)
        l1 = self.text("CARA → CROQUIS → DIRECCIÓN → DISTANCIA", 22, BOLD, DARK)
        l2 = self.text("+ construye volumen     ·     − retira volumen", 20, NORMAL, DARK)
        summary = VGroup(summary_box, VGroup(l1,l2).arrange(DOWN,buff=0.12).move_to(summary_box))
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary, shift=UP*0.12), run_time=0.8)
        self.wait(4.0)
        self.play(FadeOut(summary), run_time=0.6)
        self.wait(0.7)
