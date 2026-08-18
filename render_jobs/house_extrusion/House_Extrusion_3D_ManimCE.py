#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""House construction with positive and negative extrusion in ManimCE 0.20.x.

Pedagogical sequence
--------------------
1) Terrain + architectural grid.
2) 2D footprint sketch.
3) Positive extrusion: slab, columns and walls.
4) Negative extrusion: door and window cuts.
5) Positive extrusion: roof slab.
6) Final camera orbit and operation summary.

Visual contract follows the JP Classroom family: 1920x1080, 30 fps, white
background, black typography, safe margins, restrained functional color.
"""

from manim import *
import numpy as np


# -----------------------------------------------------------------------------
# JP CLASSROOM / RENDER CONTRACT
# -----------------------------------------------------------------------------
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
PAPER = "#F7F7F7"
TERRAIN = "#E8EEE5"
SLAB = "#B8BEC5"
COLUMN = "#4F5B66"
WALL = "#E5E7E9"
SKETCH = "#2878B5"
POSITIVE = "#2E8B57"
NEGATIVE = "#C0392B"
GLASS = "#BFD7EA"


class HouseExtrusion3D(ThreeDScene):
    """Full 3D construction example for CAD extrusion concepts."""

    # Geometry parameters in conceptual metres (scaled directly to Manim units).
    FLOOR_Z = 0.30
    WALL_H = 2.75
    WALL_T = 0.18
    COL_H = 3.05
    COL_S = 0.28
    HOUSE_W = 9.20
    HOUSE_D = 6.20

    def box(self, dims, center, color, opacity=1.0, stroke=DARK, stroke_width=0.8):
        """Create an axis-aligned rectangular prism with deterministic dimensions."""
        x, y, z = dims
        mob = Cube(
            side_length=1.0,
            fill_color=color,
            fill_opacity=opacity,
            stroke_color=stroke,
            stroke_width=stroke_width,
        )
        mob.stretch(x, 0)
        mob.stretch(y, 1)
        mob.stretch(z, 2)
        mob.move_to(np.array(center, dtype=float))
        return mob

    def text(self, content, size=28, weight=NORMAL, color=BLACK_TEXT):
        return Text(content, font_size=size, weight=weight, color=color)

    def fixed_hud(self):
        """Persistent screen-space header, phase label and operation legend."""
        title = self.text("MODELADO CAD · VIVIENDA 3D", 30, BOLD)
        subtitle = self.text("Extrusión positiva y negativa · construcción paso a paso", 19, NORMAL, MID)
        title.to_corner(UL, buff=0.38)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)

        rule = Line(LEFT * 7.55, RIGHT * 7.55, color=LIGHT, stroke_width=1.3)
        rule.to_edge(UP, buff=1.08)

        phase_box = RoundedRectangle(
            width=4.55,
            height=0.52,
            corner_radius=0.10,
            fill_color=WHITE,
            fill_opacity=0.96,
            stroke_color=DARK,
            stroke_width=1.1,
        )
        phase_box.to_corner(UR, buff=0.40)
        phase = self.text("01 · TERRENO + CROQUIS", 20, BOLD)
        phase.move_to(phase_box)
        phase_group = VGroup(phase_box, phase)

        add_dot = Circle(radius=0.07, fill_color=POSITIVE, fill_opacity=1, stroke_width=0)
        add_text = self.text("+  AÑADIR MATERIAL", 17, BOLD, POSITIVE)
        rem_dot = Circle(radius=0.07, fill_color=NEGATIVE, fill_opacity=1, stroke_width=0)
        rem_text = self.text("−  RETIRAR MATERIAL", 17, BOLD, NEGATIVE)
        legend = VGroup(add_dot, add_text, rem_dot, rem_text).arrange(RIGHT, buff=0.25)
        legend.to_edge(DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(title, subtitle, rule, phase_group, legend)
        self.add(title, subtitle, rule, phase_group, legend)
        return phase_group

    def set_phase(self, phase_group, number, label, color=DARK):
        old_box, old_text = phase_group
        new_text = self.text(f"{number:02d} · {label}", 20, BOLD, color)
        new_text.move_to(old_box)
        self.play(Transform(old_text, new_text), run_time=0.55)

    def footprint_lines(self, z=0.36, color=SKETCH, width=3.0):
        """2D architectural sketch: exterior perimeter + internal partitions."""
        w, d = self.HOUSE_W, self.HOUSE_D
        pts = [
            np.array([-w/2, -d/2, z]),
            np.array([ w/2, -d/2, z]),
            np.array([ w/2,  d/2, z]),
            np.array([-w/2,  d/2, z]),
        ]
        exterior = VGroup(*[
            Line(pts[i], pts[(i + 1) % 4], color=color, stroke_width=width)
            for i in range(4)
        ])
        interior_specs = [
            ((0.70, -2.55), (0.70, 2.35)),
            ((-4.05, 0.75), (0.70, 0.75)),
            ((0.70, 0.75), (4.05, 0.75)),
            ((-1.90, 0.75), (-1.90, 2.70)),
        ]
        interior = VGroup(*[
            Line([a[0], a[1], z], [b[0], b[1], z], color=color, stroke_width=width * 0.78)
            for a, b in interior_specs
        ])
        return VGroup(exterior, interior)

    def grow_box_from_base(self, dims, base_z, color, opacity=1.0, run_time=1.0):
        """Return a seed prism and its target so Transform reads as linear extrusion."""
        x, y, z = dims
        seed_h = 0.025
        seed = self.box((x, y, seed_h), (0, 0, base_z + seed_h / 2), color, opacity)
        target = self.box((x, y, z), (0, 0, base_z + z / 2), color, opacity)
        return seed, target

    def column_specs(self):
        xvals = [-4.35, 0.70, 4.35]
        yvals = [-2.85, 0.75, 2.85]
        return [(x, y) for x in xvals for y in yvals]

    def full_walls(self):
        """Continuous positive-extrusion wall state, prior to negative cuts."""
        zc = self.FLOOR_Z + self.WALL_H / 2
        w, d, t = self.HOUSE_W, self.HOUSE_D, self.WALL_T
        front = self.box((w, t, self.WALL_H), (0, -d/2, zc), WALL, 0.97)
        back = self.box((w, t, self.WALL_H), (0, d/2, zc), WALL, 0.97)
        left = self.box((t, d - 2*t, self.WALL_H), (-w/2, 0, zc), WALL, 0.97)
        right = self.box((t, d - 2*t, self.WALL_H), (w/2, 0, zc), WALL, 0.97)

        interior = VGroup(
            self.box((t, 4.90, self.WALL_H), (0.70, -0.10, zc), WALL, 0.94),
            self.box((4.75, t, self.WALL_H), (-1.675, 0.75, zc), WALL, 0.94),
            self.box((3.35, t, self.WALL_H), (2.375, 0.75, zc), WALL, 0.94),
            self.box((t, 1.95, self.WALL_H), (-1.90, 1.725, zc), WALL, 0.94),
        )
        return front, back, left, right, interior

    def front_after_door(self):
        """Front wall after subtracting a full-height doorway."""
        y = -self.HOUSE_D / 2
        t = self.WALL_T
        z0 = self.FLOOR_Z
        top = z0 + self.WALL_H
        door_l, door_r, door_top = -2.55, -1.35, z0 + 2.15
        parts = VGroup(
            self.box((door_l + self.HOUSE_W/2, t, self.WALL_H),
                     ((-self.HOUSE_W/2 + door_l)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((self.HOUSE_W/2 - door_r, t, self.WALL_H),
                     ((door_r + self.HOUSE_W/2)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((door_r-door_l, t, top-door_top),
                     ((door_l+door_r)/2, y, (door_top+top)/2), WALL, 0.97),
        )
        return parts

    def front_final(self):
        """Front wall after doorway + window subtraction."""
        y = -self.HOUSE_D / 2
        t = self.WALL_T
        z0 = self.FLOOR_Z
        top = z0 + self.WALL_H
        door_l, door_r, door_top = -2.55, -1.35, z0 + 2.15
        win_l, win_r = 1.30, 3.15
        win_bottom, win_top = z0 + 0.88, z0 + 2.05

        parts = VGroup(
            self.box((door_l + self.HOUSE_W/2, t, self.WALL_H),
                     ((-self.HOUSE_W/2 + door_l)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((win_l - door_r, t, self.WALL_H),
                     ((door_r + win_l)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((self.HOUSE_W/2 - win_r, t, self.WALL_H),
                     ((win_r + self.HOUSE_W/2)/2, y, z0 + self.WALL_H/2), WALL, 0.97),
            self.box((door_r-door_l, t, top-door_top),
                     ((door_l+door_r)/2, y, (door_top+top)/2), WALL, 0.97),
            self.box((win_r-win_l, t, win_bottom-z0),
                     ((win_l+win_r)/2, y, (z0+win_bottom)/2), WALL, 0.97),
            self.box((win_r-win_l, t, top-win_top),
                     ((win_l+win_r)/2, y, (win_top+top)/2), WALL, 0.97),
        )
        return parts

    def vertical_profile(self, x_center, width, bottom, height, y_plane, color=NEGATIVE):
        """Closed sketch profile on the front facade plane (x-z rectangle)."""
        rect = Rectangle(
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=4.0,
            fill_color=color,
            fill_opacity=0.10,
        )
        rect.rotate(PI/2, axis=RIGHT)
        rect.move_to([x_center, y_plane, bottom + height/2])
        return rect

    def cutter_front(self, x_center, width, bottom, height):
        """Transparent cutting volume extending from outside through the front wall."""
        depth = 0.90
        y_front = -self.HOUSE_D / 2
        target_center_y = y_front + 0.18
        cutter = self.box(
            (width, depth, height),
            (x_center, target_center_y, bottom + height/2),
            NEGATIVE,
            opacity=0.24,
            stroke=NEGATIVE,
            stroke_width=1.6,
        )
        return cutter

    def construct(self):
        self.camera.background_color = WHITE
        phase = self.fixed_hud()

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.78)

        terrain = self.box((11.2, 8.2, 0.16), (0, 0, -0.08), TERRAIN, 1.0, stroke=LIGHT, stroke_width=0.7)
        self.play(FadeIn(terrain), run_time=0.8)

        grid = VGroup()
        for x in np.arange(-5.0, 5.01, 1.0):
            grid.add(Line([x, -3.65, 0.015], [x, 3.65, 0.015], color=LIGHT, stroke_width=0.65))
        for y in np.arange(-3.5, 3.51, 1.0):
            grid.add(Line([-5.15, y, 0.015], [5.15, y, 0.015], color=LIGHT, stroke_width=0.65))
        self.play(Create(grid), run_time=1.2)

        sketch = self.footprint_lines(z=0.045)
        self.play(LaggedStart(*[Create(m) for m in sketch[0]], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[Create(m) for m in sketch[1]], lag_ratio=0.12), run_time=1.4)
        self.wait(0.8)

        self.set_phase(phase, 2, "EXTRUSIÓN + · LOSA", POSITIVE)
        self.move_camera(phi=58 * DEGREES, theta=-52 * DEGREES, zoom=0.75, run_time=2.0)

        slab_seed = self.box((self.HOUSE_W + 0.25, self.HOUSE_D + 0.25, 0.025), (0, 0, 0.0125), SLAB, 0.96)
        slab_target = self.box((self.HOUSE_W + 0.25, self.HOUSE_D + 0.25, self.FLOOR_Z), (0, 0, self.FLOOR_Z/2), SLAB, 0.96)
        self.add(slab_seed)
        self.play(Transform(slab_seed, slab_target), run_time=1.8, rate_func=smooth)
        slab = slab_seed
        self.play(sketch.animate.set_opacity(0.55).shift(OUT * self.FLOOR_Z), run_time=0.7)
        self.wait(0.6)

        self.set_phase(phase, 3, "EXTRUSIÓN + · COLUMNAS", POSITIVE)
        col_seeds = []
        col_targets = []
        for x, y in self.column_specs():
            seed_h = 0.03
            col_seeds.append(self.box((self.COL_S, self.COL_S, seed_h), (x, y, self.FLOOR_Z + seed_h/2), COLUMN, 0.98))
            col_targets.append(self.box((self.COL_S, self.COL_S, self.COL_H), (x, y, self.FLOOR_Z + self.COL_H/2), COLUMN, 0.98))
        self.add(*col_seeds)
        self.play(
            LaggedStart(*[Transform(a, b) for a, b in zip(col_seeds, col_targets)], lag_ratio=0.10),
            run_time=2.8,
        )
        self.wait(0.5)

        self.set_phase(phase, 4, "EXTRUSIÓN + · MUROS", POSITIVE)
        front_target, back_target, left_target, right_target, interior_targets = self.full_walls()

        wall_targets = [front_target, back_target, left_target, right_target, *interior_targets]
        wall_seeds = []
        for target in wall_targets:
            center = target.get_center()
            mins = target.get_all_points().min(axis=0)
            maxs = target.get_all_points().max(axis=0)
            dx, dy = maxs[0]-mins[0], maxs[1]-mins[1]
            seed_h = 0.025
            wall_seeds.append(self.box((dx, dy, seed_h), (center[0], center[1], self.FLOOR_Z + seed_h/2), WALL, 0.96))

        self.add(*wall_seeds)
        self.play(
            LaggedStart(*[Transform(a, b) for a, b in zip(wall_seeds, wall_targets)], lag_ratio=0.08),
            run_time=4.0,
            rate_func=smooth,
        )
        front_wall = wall_seeds[0]
        other_walls = VGroup(*wall_seeds[1:])
        self.wait(0.8)

        self.set_phase(phase, 5, "EXTRUSIÓN − · PUERTA", NEGATIVE)
        self.move_camera(phi=68 * DEGREES, theta=-28 * DEGREES, zoom=0.92, run_time=1.5)

        door_x = -1.95
        door_w = 1.20
        door_bottom = self.FLOOR_Z
        door_h = 2.15
        door_profile = self.vertical_profile(door_x, door_w, door_bottom, door_h, -self.HOUSE_D/2 - 0.12)
        self.play(Create(door_profile), run_time=1.0)

        door_cutter = self.cutter_front(door_x, door_w, door_bottom, door_h)
        door_cutter.shift(IN * 0.75)
        self.play(FadeIn(door_cutter), run_time=0.4)
        self.play(door_cutter.animate.shift(OUT * 0.75), run_time=1.4, rate_func=smooth)

        after_door = self.front_after_door()
        self.play(
            FadeOut(front_wall, run_time=0.55),
            FadeIn(after_door, run_time=0.75),
            FadeOut(door_cutter, run_time=0.55),
            FadeOut(door_profile, run_time=0.45),
        )
        front_wall = after_door
        self.wait(0.7)

        self.set_phase(phase, 6, "EXTRUSIÓN − · VENTANA", NEGATIVE)
        win_x = 2.225
        win_w = 1.85
        win_bottom = self.FLOOR_Z + 0.88
        win_h = 1.17
        win_profile = self.vertical_profile(win_x, win_w, win_bottom, win_h, -self.HOUSE_D/2 - 0.12)
        self.play(Create(win_profile), run_time=0.9)

        win_cutter = self.cutter_front(win_x, win_w, win_bottom, win_h)
        win_cutter.shift(IN * 0.75)
        self.play(FadeIn(win_cutter), run_time=0.35)
        self.play(win_cutter.animate.shift(OUT * 0.75), run_time=1.3, rate_func=smooth)

        final_front = self.front_final()
        self.play(
            FadeOut(front_wall, run_time=0.55),
            FadeIn(final_front, run_time=0.75),
            FadeOut(win_cutter, run_time=0.50),
            FadeOut(win_profile, run_time=0.40),
        )
        front_wall = final_front

        glass = self.box((win_w * 0.94, 0.035, win_h * 0.94),
                         (win_x, -self.HOUSE_D/2 + 0.01, win_bottom + win_h/2), GLASS, 0.42, stroke=SKETCH, stroke_width=0.8)
        self.play(FadeIn(glass), run_time=0.55)
        self.wait(0.8)

        self.set_phase(phase, 7, "EXTRUSIÓN + · CUBIERTA", POSITIVE)
        roof_base = self.FLOOR_Z + self.COL_H
        roof_seed = self.box((self.HOUSE_W + 0.45, self.HOUSE_D + 0.45, 0.025), (0, 0, roof_base + 0.0125), SLAB, 0.72)
        roof_target = self.box((self.HOUSE_W + 0.45, self.HOUSE_D + 0.45, 0.24), (0, 0, roof_base + 0.12), SLAB, 0.72)
        self.add(roof_seed)
        self.play(Transform(roof_seed, roof_target), run_time=1.7)
        roof = roof_seed
        self.play(roof.animate.set_fill(opacity=0.22), run_time=0.8)

        self.set_phase(phase, 8, "MODELO 3D COMPLETO", DARK)
        self.move_camera(phi=63 * DEGREES, theta=-48 * DEGREES, zoom=0.82, run_time=1.6)
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(4.2)
        self.stop_ambient_camera_rotation()

        summary_box = RoundedRectangle(
            width=6.6,
            height=1.10,
            corner_radius=0.12,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=DARK,
            stroke_width=1.3,
        )
        summary_box.to_edge(DOWN, buff=0.52)
        line1 = self.text("PERFIL 2D  +  DIRECCIÓN  +  DISTANCIA", 22, BOLD, DARK)
        line2 = self.text("EXTRUSIÓN + = construir    ·    EXTRUSIÓN − = abrir vacíos", 19, NORMAL, DARK)
        lines = VGroup(line1, line2).arrange(DOWN, buff=0.12).move_to(summary_box)
        summary = VGroup(summary_box, lines)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary, shift=UP * 0.15), run_time=0.8)
        self.wait(3.5)
        self.play(FadeOut(summary), run_time=0.6)
        self.wait(0.6)
