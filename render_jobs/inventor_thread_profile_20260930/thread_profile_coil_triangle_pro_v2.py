from __future__ import annotations

import math
import os
import numpy as np
from manim import *

from library.inventor_pro_ui import (
    CANVAS, PREVIEW, SELECT, SKETCH, STEEL, STEEL_DARK, TEXT, TEXT_LIGHT,
    UI_DARK, UI_DARK_2, UI_LIGHT, UI_LINE, UI_MID, WHITE, fit, txt, cylinder,
)
from thread_profile_coil_triangle_senior import (
    InventorThreadProfileTriangleSenior,
    PITCH_MM, D_MAJOR_MM, D_MINOR_MM, FLANK_ANGLE_DEG,
    RADIAL_DEPTH_MM, PROFILE_WIDTH_MM, REMAINDER_MM,
    R_MAJOR, R_MINOR, DEPTH_WORLD, PITCH_WORLD, PROFILE_WIDTH_WORLD,
    Z0, TURNS, CUT, TIME_SCALE,
    helix_center, helix_curve, triangular_thread_surface, sharp_profile_triangle,
)

# -----------------------------------------------------------------------------
# PROFESSIONAL V2 — UI / MOTION / TEXT REFINEMENT
# -----------------------------------------------------------------------------
NAVY = "#17324D"
NAVY_2 = "#0F2538"
BLUE = "#2D7DBD"
CYAN = "#31A6C7"
GREEN = "#2E8B57"
ORANGE = SELECT
RED = CUT
PURPLE = "#7B61A8"
PANEL = "#F7F8F9"
PANEL_ALT = "#ECEFF1"
GRID = "#CCD2D7"
INK = "#202326"
MUTED = "#5F6A72"


class InventorThreadProfileTriangleProV2(InventorThreadProfileTriangleSenior):
    """Professional V2 of the thread-profile/Coil lesson.

    Improvements over V1:
    - denser Inventor-style interface with contextual ribbon, model browser,
      property panel, view cube, status bar, and stage navigator;
    - shorter, more readable Spanish instructional text;
    - explicit animated parameter acquisition and geometric construction;
    - progressive triangle construction, pitch duplication, helical profile slices,
      section/axial validation, and a parametric pitch edit demonstration;
    - all camera moves preserve fixed UI and safe viewport margins.
    """

    OPERATION = "Coil"
    FEATURE_NODE = "Coil1"

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super(InventorThreadProfileTriangleSenior, self).play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super(InventorThreadProfileTriangleSenior, self).wait(duration * TIME_SCALE, *args, **kwargs)

    def _text(self, s, size=18, color=INK, weight=NORMAL):
        return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)

    def _panel(self, w, h, fill=PANEL, stroke=UI_LINE, radius=0.06, opacity=0.985):
        return RoundedRectangle(
            width=w, height=h, corner_radius=radius,
            fill_color=fill, fill_opacity=opacity,
            stroke_color=stroke, stroke_width=0.9,
        )

    def _safe_fit(self, mob, width, height=None):
        if mob.width > width:
            mob.scale_to_fit_width(width)
        if height is not None and mob.height > height:
            mob.scale_to_fit_height(height)
        return mob

    def install_hud(self, property_rows, browser_nodes):
        top = Rectangle(width=16, height=0.38, fill_color=NAVY_2, fill_opacity=1, stroke_width=0).to_edge(UP, buff=0)
        app = RoundedRectangle(width=0.30, height=0.30, corner_radius=0.025,
                               fill_color=ORANGE, fill_opacity=1, stroke_width=0).move_to([-7.74, 4.31, 0])
        app_t = self._text("I", 18, WHITE, BOLD).move_to(app)
        title = self._text("Autodesk Inventor Professional 2026", 15, TEXT_LIGHT, MEDIUM).move_to([-6.10, 4.31, 0])
        doc = self._text("Thread_Profile_Coil.ipt", 14, "#D7E0E6", NORMAL).move_to([0.05, 4.31, 0])
        mode = self._text("3D MODELING", 12, "#B9C4CC", BOLD).move_to([6.42, 4.31, 0])

        tabs_bg = Rectangle(width=16, height=0.36, fill_color="#F7F8F9", fill_opacity=1, stroke_width=0).move_to([0, 3.94, 0])
        tab_names = ["File", "3D Model", "Sketch", "Annotate", "Inspect", "Tools", "Manage", "View"]
        tabs = VGroup()
        x = -7.55
        for name in tab_names:
            t = self._text(name, 14, INK, BOLD if name == "3D Model" else NORMAL)
            t.move_to([x + t.width / 2, 3.94, 0])
            tabs.add(t)
            x += t.width + 0.30
        tab_line = Line([-6.74, 3.77, 0], [-5.67, 3.77, 0], color=ORANGE, stroke_width=3.0)

        ribbon = Rectangle(width=16, height=0.92, fill_color="#E9ECEF", fill_opacity=1,
                           stroke_color=UI_LINE, stroke_width=0.8).move_to([0, 3.30, 0])
        tool_specs = [
            ("Sketch", -6.95, 0.98), ("Extrude", -5.83, 0.96), ("Revolve", -4.75, 0.96),
            ("Sweep", -3.67, 0.90), ("Loft", -2.67, 0.82), ("Fillet", -1.73, 0.84),
            ("Chamfer", -0.74, 0.98), ("Hole", 0.31, 0.78), ("Pattern", 1.28, 0.96),
            ("Mirror", 2.34, 0.86), ("Rib", 3.28, 0.74), ("Emboss", 4.17, 0.92),
            ("Coil", 5.23, 0.82), ("Measure", 6.27, 0.92),
        ]
        tools = VGroup()
        self._tool_centers = {}
        for label, xpos, width in tool_specs:
            tile = RoundedRectangle(width=width, height=0.56, corner_radius=0.045,
                                    fill_color="#F7F8F9", fill_opacity=1,
                                    stroke_color=UI_LINE, stroke_width=0.8).move_to([xpos, 3.34, 0])
            icon = Square(side_length=0.15, fill_color=STEEL, fill_opacity=1,
                          stroke_color=UI_MID, stroke_width=0.8).move_to([xpos, 3.47, 0])
            lab = self._text(label, 11, INK, NORMAL)
            self._safe_fit(lab, width - 0.08, 0.14)
            lab.move_to([xpos, 3.17, 0])
            tools.add(VGroup(tile, icon, lab))
            self._tool_centers[label] = np.array([xpos, 3.34, 0])
        tool_highlight = RoundedRectangle(width=0.98, height=0.62, corner_radius=0.05,
                                          fill_opacity=0, stroke_color=ORANGE, stroke_width=2.3)
        tool_highlight.move_to(self._tool_centers["Sketch"])
        self._tool_highlight = tool_highlight

        browser = Rectangle(width=2.36, height=6.15, fill_color="#F7F8F9", fill_opacity=0.99,
                            stroke_color=UI_LINE, stroke_width=0.8).move_to([-6.82, -0.18, 0])
        bhead = Rectangle(width=2.36, height=0.42, fill_color="#E0E4E7", fill_opacity=1,
                          stroke_width=0).move_to([-6.82, 2.67, 0])
        btitle = self._text("MODEL", 15, INK, BOLD).move_to([-7.60, 2.67, 0])
        filter_box = RoundedRectangle(width=0.68, height=0.26, corner_radius=0.04,
                                      fill_color=WHITE, fill_opacity=1, stroke_color=UI_LINE, stroke_width=0.7).move_to([-5.94, 2.67, 0])
        filter_t = self._text("Filter", 10, MUTED).move_to(filter_box)
        rows = [
            ("Part1.ipt", 2.30, BOLD), ("Origin", 1.94, NORMAL), ("XY Plane", 1.59, NORMAL),
            ("XZ Plane", 1.24, NORMAL), ("Sketch1", 0.89, NORMAL), ("Axis", 0.54, NORMAL),
            ("Coil1", 0.19, NORMAL),
        ]
        tree = VGroup()
        self._browser_y = {}
        for i, (label, y, weight) in enumerate(rows):
            prefix = "▾  " if i == 0 else ("   ▸  " if label == "Origin" else "      •  ")
            t = self._text(prefix + label, 13, INK if i == 0 else MUTED, weight)
            self._safe_fit(t, 2.03)
            t.move_to([-7.88 + t.width / 2, y, 0])
            tree.add(t)
            self._browser_y[label] = y
        feature_highlight = RoundedRectangle(width=2.10, height=0.29, corner_radius=0.03,
                                             fill_color="#DDEFF9", fill_opacity=0.85,
                                             stroke_color=BLUE, stroke_width=1.0).move_to([-6.83, self._browser_y["Sketch1"], 0])
        feature_highlight.set_z_index(1)
        tree.set_z_index(2)
        self._feature_highlight = feature_highlight

        prop = Rectangle(width=3.18, height=6.15, fill_color="#F7F8F9", fill_opacity=0.99,
                         stroke_color=UI_LINE, stroke_width=0.8).move_to([6.16, -0.18, 0])
        phead = Rectangle(width=3.18, height=0.46, fill_color=NAVY, fill_opacity=1, stroke_width=0).move_to([6.16, 2.65, 0])
        ptitle = self._text("COIL / THREAD PROFILE", 15, WHITE, BOLD).move_to(phead)
        section = self._text("Profile geometry", 12, MUTED, BOLD).move_to([5.02, 2.25, 0])
        self._fields = {}
        field_rows = [
            ("Pitch", f"{PITCH_MM:.2f} mm"),
            ("Major Ø", f"{D_MAJOR_MM:.3f} mm"),
            ("Minor Ø", f"{D_MINOR_MM:.3f} mm"),
            ("Depth h", f"{RADIAL_DEPTH_MM:.3f} mm"),
            ("Flank angle", "60 deg"),
            ("Profile b", f"{PROFILE_WIDTH_MM:.3f} mm"),
            ("Type", "Pitch & Rev"),
            ("Operation", "Cut"),
        ]
        props = VGroup()
        y = 1.88
        for label, value in field_rows:
            lab = self._text(label, 12, MUTED, NORMAL)
            lab.move_to([4.70 + lab.width / 2, y, 0])
            box = RoundedRectangle(width=1.40, height=0.31, corner_radius=0.035,
                                   fill_color=WHITE, fill_opacity=1, stroke_color=UI_LINE, stroke_width=0.8).move_to([6.72, y, 0])
            val = self._text(value, 12, INK, BOLD).move_to(box)
            self._safe_fit(val, 1.28, 0.20)
            row = VGroup(lab, box, val)
            props.add(row)
            self._fields[label] = row
            y -= 0.46
        ok = RoundedRectangle(width=0.92, height=0.36, corner_radius=0.05,
                              fill_color=ORANGE, fill_opacity=1, stroke_width=0).move_to([6.70, -2.94, 0])
        ok_t = self._text("OK", 14, WHITE, BOLD).move_to(ok)
        cancel = RoundedRectangle(width=1.06, height=0.36, corner_radius=0.05,
                                  fill_color=WHITE, fill_opacity=1, stroke_color=UI_LINE, stroke_width=0.8).move_to([5.44, -2.94, 0])
        cancel_t = self._text("Cancel", 13, INK).move_to(cancel)
        self._ok_group = VGroup(ok, ok_t)

        cube = VGroup(
            Square(side_length=0.68, fill_color="#F5F6F7", fill_opacity=0.96, stroke_color=UI_MID, stroke_width=0.9),
            self._text("TOP", 10, MUTED, BOLD),
            self._text("FRONT", 9, MUTED, BOLD),
        )
        cube[1].move_to(cube[0]).shift(UP * 0.10)
        cube[2].move_to(cube[0]).shift(DOWN * 0.10)
        cube.move_to([4.55, 2.16, 0])
        nav = VGroup(
            self._text("Orbit", 11, MUTED), self._text("Pan", 11, MUTED), self._text("Zoom", 11, MUTED), self._text("Fit", 11, MUTED)
        ).arrange(RIGHT, buff=0.28).move_to([2.72, -3.60, 0])

        status_bar = Rectangle(width=16, height=0.36, fill_color="#F2F4F5", fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
        self._status_text = self._text("Ready  |  Select geometry  |  Units: mm", 12, MUTED).move_to([-2.10, -4.31, 0])
        self._status_text.align_to(status_bar, LEFT).shift(RIGHT * 0.28)
        self._stage_nodes = VGroup()
        stage_labels = ["Datos", "Profundidad", "Perfil", "Coil", "Validación", "Resultado"]
        x0 = -3.85
        for i, label in enumerate(stage_labels):
            c = Circle(radius=0.13, fill_color=WHITE, fill_opacity=1, stroke_color=UI_LINE, stroke_width=1.2)
            n = self._text(str(i + 1), 10, MUTED, BOLD).move_to(c)
            lab = self._text(label, 10, MUTED).next_to(c, RIGHT, buff=0.05)
            node = VGroup(c, n, lab).move_to([x0 + i * 1.52, -3.72, 0])
            self._stage_nodes.add(node)
        self._stage_index = -1

        ui = VGroup(
            top, app, app_t, title, doc, mode,
            tabs_bg, tabs, tab_line,
            ribbon, tools, tool_highlight,
            browser, bhead, btitle, filter_box, filter_t, feature_highlight, tree,
            prop, phead, ptitle, section, props, ok, ok_t, cancel, cancel_t,
            cube, nav, status_bar, self._status_text, self._stage_nodes,
        )
        self.add_fixed_in_frame_mobjects(ui)
        ui.set_z_index(100)
        self._ui_group = ui
        self.hud = None
        self.step_box = None
        self.set_stage(0, animate=False)

    def set_stage(self, index, animate=True):
        index = max(0, min(index, len(self._stage_nodes) - 1))
        anims = []
        for i, node in enumerate(self._stage_nodes):
            fill = GREEN if i < index else ORANGE if i == index else WHITE
            stroke = fill if i <= index else UI_LINE
            num_color = WHITE if i <= index else MUTED
            lab_color = INK if i <= index else MUTED
            if animate:
                anims += [
                    node[0].animate.set_fill(fill, 1).set_stroke(stroke),
                    node[1].animate.set_color(num_color),
                    node[2].animate.set_color(lab_color),
                ]
            else:
                node[0].set_fill(fill, 1).set_stroke(stroke)
                node[1].set_color(num_color)
                node[2].set_color(lab_color)
        if animate:
            self.play(*anims, run_time=0.35)
        self._stage_index = index

    def set_tool(self, label):
        if label not in self._tool_centers:
            return
        self.play(self._tool_highlight.animate.move_to(self._tool_centers[label]), run_time=0.34)

    def set_feature(self, name):
        if name not in self._browser_y:
            return
        self.play(self._feature_highlight.animate.move_to([-6.83, self._browser_y[name], 0]), run_time=0.34)

    def pulse_field(self, name, color=ORANGE):
        row = self._fields.get(name)
        if row is None:
            return
        self.play(row[1].animate.set_stroke(color, width=2.3), row[2].animate.set_color(color), run_time=0.28)
        self.play(row[1].animate.set_stroke(UI_LINE, width=0.8), row[2].animate.set_color(INK), run_time=0.28)

    def set_field_value(self, name, value, color=INK):
        row = self._fields[name]
        old = row[2]
        new = self._text(value, 12, color, BOLD).move_to(row[1])
        self._safe_fit(new, 1.28, 0.20)
        self.add_fixed_in_frame_mobjects(new)
        self.play(ReplacementTransform(old, new), run_time=0.36)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        row.submobjects[2] = new
        self._fields[name] = row

    def flash_status(self, content: str):
        old = self._status_text
        new = self._text(content, 12, MUTED).move_to(old)
        self._safe_fit(new, 12.8, 0.18)
        new.align_to(old, LEFT)
        self.add_fixed_in_frame_mobjects(new)
        self.play(ReplacementTransform(old, new), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        self._status_text = new

    def step(self, number: int, title: str, detail: str, duration: float = 1.8):
        if self.step_box is not None:
            self.play(FadeOut(self.step_box, shift=DOWN * 0.04), run_time=0.18)
            self.remove_fixed_in_frame_mobjects(self.step_box)
            self.remove(self.step_box)
        panel = RoundedRectangle(width=9.15, height=0.82, corner_radius=0.07,
                                 fill_color="#FAFBFC", fill_opacity=0.985,
                                 stroke_color=UI_LINE, stroke_width=0.8).move_to([-0.32, -3.05, 0])
        num_box = RoundedRectangle(width=0.58, height=0.58, corner_radius=0.06,
                                   fill_color=ORANGE, fill_opacity=1, stroke_width=0).move_to(panel.get_left() + RIGHT * 0.42)
        n = self._text(str(number), 18, WHITE, BOLD).move_to(num_box)
        t = self._text(title, 17, INK, BOLD)
        d = self._text(detail, 13, MUTED, NORMAL)
        self._safe_fit(t, 7.95, 0.24)
        self._safe_fit(d, 7.95, 0.20)
        t.move_to(panel.get_left() + RIGHT * 0.84 + UP * 0.13, aligned_edge=LEFT)
        d.next_to(t, DOWN, aligned_edge=LEFT, buff=0.06)
        self.step_box = VGroup(panel, num_box, n, t, d)
        self.add_fixed_in_frame_mobjects(self.step_box)
        self.step_box.set_z_index(150)
        self.play(FadeIn(self.step_box, shift=UP * 0.05), run_time=0.28)
        self.wait(duration)

    def intro(self, subtitle: str):
        card = self._panel(8.75, 2.36, fill="#F9FAFB", stroke=BLUE, radius=0.14).move_to([-0.25, 0.10, 0])
        title = self._text("PERFIL TRIANGULAR PARA COIL", 30, NAVY, BOLD)
        sub = self._text("De tres datos medibles a una hélice paramétrica", 19, MUTED, MEDIUM)
        title.move_to(card).shift(UP * 0.69)
        sub.next_to(title, DOWN, buff=0.10)

        chips = VGroup()
        for label, value, color in [
            ("P", f"{PITCH_MM:.2f} mm", ORANGE),
            ("Øext", f"{D_MAJOR_MM:.3f}", BLUE),
            ("Øint", f"{D_MINOR_MM:.3f}", RED),
            ("h", f"{RADIAL_DEPTH_MM:.3f}", GREEN),
            ("60°", "flancos", PURPLE),
            ("Coil", "hélice 3D", CYAN),
        ]:
            box = RoundedRectangle(width=1.12, height=0.54, corner_radius=0.06,
                                   fill_color=WHITE, fill_opacity=1, stroke_color=color, stroke_width=1.4)
            a = self._text(label, 15, color, BOLD)
            b = self._text(value, 10, MUTED, NORMAL)
            VGroup(a, b).arrange(DOWN, buff=0.01).move_to(box)
            chips.add(VGroup(box, a, b))
        chips.arrange(RIGHT, buff=0.16).move_to(card).shift(DOWN * 0.62)
        group = VGroup(card, title, sub, chips)
        self.add_fixed_in_frame_mobjects(group)
        group.set_z_index(160)
        self.play(FadeIn(card, scale=0.97), Write(title), run_time=0.80)
        self.play(FadeIn(sub), run_time=0.42)
        self.play(LaggedStart(*[FadeIn(ch, shift=UP * 0.05) for ch in chips], lag_ratio=0.12), run_time=1.25)
        for ch in chips:
            self.play(Indicate(ch[0], color=ch[0].get_stroke_color(), scale_factor=1.03), run_time=0.22)
        self.wait(0.60)
        self.play(FadeOut(group, shift=UP * 0.05), run_time=0.45)
        self.remove_fixed_in_frame_mobjects(group)
        self.remove(group)

    def callout(self, title, body, color=BLUE, center=(-0.25, 0.70, 0), width=6.8, height=1.35):
        box = self._panel(width, height, fill="#FAFBFC", stroke=color, radius=0.09)
        head = self._text(title, 18, color, BOLD)
        text = self._text(body, 14, INK, NORMAL)
        self._safe_fit(head, width - 0.45)
        self._safe_fit(text, width - 0.45)
        content = VGroup(head, text).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        g = VGroup(box, content).move_to(center)
        self.add_fixed_in_frame_mobjects(g)
        g.set_z_index(155)
        self.play(FadeIn(box, scale=0.98), Write(head), FadeIn(text), run_time=0.50)
        return g

    def clear_callout(self, g, rt=0.28):
        self.play(FadeOut(g), run_time=rt)
        self.remove_fixed_in_frame_mobjects(g)
        self.remove(g)

    def profile_slice(self, u: float, color=CYAN, opacity=0.18):
        def p(v):
            r = R_MINOR + DEPTH_WORLD * (1.0 - abs(v))
            z = Z0 + (PITCH_WORLD / TAU) * u + v * (PROFILE_WIDTH_WORLD / 2.0)
            return np.array([r * math.cos(u), r * math.sin(u), z])
        return Polygon(p(-1.0), p(0.0), p(1.0),
                       stroke_color=color, stroke_width=2.2,
                       fill_color=color, fill_opacity=opacity)

    def pitch_helix(self, pitch_world: float, z_start=-2.15, z_span=4.60, color=PREVIEW, width=7.0):
        turns = z_span / pitch_world
        k = pitch_world / TAU
        r = (R_MAJOR + R_MINOR) / 2
        return ParametricFunction(
            lambda t: np.array([r * math.cos(t), r * math.sin(t), z_start + k * t]),
            t_range=[0, turns * TAU, 0.035], color=color, stroke_width=width,
        ).set_opacity(0.76)

    def precision_sketch(self):
        panel = self._panel(8.55, 4.92, fill="#FBFCFD", stroke=UI_LINE, radius=0.08).move_to([-0.20, 0.05, 0])
        head = self._text("SKETCH1 · CONSTRUCCIÓN DEL PERFIL", 20, NAVY, BOLD).move_to(panel.get_top() + DOWN * 0.28)
        sub = self._text("Sección axial · perfil V simétrico · unidades mm", 12, MUTED).next_to(head, DOWN, buff=0.04)

        grid = VGroup()
        for x in np.arange(-3.7, 3.61, 0.35):
            grid.add(Line([x, -1.63, 0], [x, 1.50, 0], color=GRID, stroke_width=0.35).set_opacity(0.55))
        for y in np.arange(-1.6, 1.51, 0.35):
            grid.add(Line([-3.70, y, 0], [3.60, y, 0], color=GRID, stroke_width=0.35).set_opacity(0.55))

        y_maj = 0.95
        y_min = -0.48
        x_left, x_right = -3.40, 3.20
        major = Line([x_left, y_maj, 0], [x_right, y_maj, 0], color=BLUE, stroke_width=4.1)
        minor = Line([x_left, y_min, 0], [x_right, y_min, 0], color=RED, stroke_width=3.5)
        major_lab = self._text(f"Ø exterior = {D_MAJOR_MM:.3f}", 14, BLUE, BOLD).move_to([2.02, 1.20, 0])
        minor_lab = self._text(f"Ø interior = {D_MINOR_MM:.3f}", 14, RED, BOLD).move_to([2.02, -0.76, 0])

        cx = -0.20
        pitch_vis = 2.18
        base_vis = pitch_vis * (PROFILE_WIDTH_MM / PITCH_MM)
        c1, c2 = cx - pitch_vis / 2, cx + pitch_vis / 2
        centers = VGroup(
            DashedLine([c1, y_maj + 0.30, 0], [c1, y_min - 0.35, 0], color=MUTED, dash_length=0.08, stroke_width=1.2),
            DashedLine([c2, y_maj + 0.30, 0], [c2, y_min - 0.35, 0], color=MUTED, dash_length=0.08, stroke_width=1.2),
        )
        pitch_arrow = DoubleArrow([c1, y_min - 0.52, 0], [c2, y_min - 0.52, 0], buff=0, color=ORANGE, stroke_width=2.2)
        pitch_lab = self._text(f"P = {PITCH_MM:.2f}", 14, ORANGE, BOLD).next_to(pitch_arrow, DOWN, buff=0.04)

        xl, xr = cx - base_vis / 2, cx + base_vis / 2
        left_flank = Line([xl, y_maj, 0], [cx, y_min, 0], color=SKETCH, stroke_width=4.2)
        right_flank = Line([cx, y_min, 0], [xr, y_maj, 0], color=SKETCH, stroke_width=4.2)
        crest_line = Line([xl, y_maj, 0], [xr, y_maj, 0], color=SKETCH, stroke_width=2.2).set_opacity(0.35)
        depth_arrow = DoubleArrow([xr + 0.48, y_maj, 0], [xr + 0.48, y_min, 0], buff=0, color=GREEN, stroke_width=2.2)
        depth_lab = self._text(f"h = {RADIAL_DEPTH_MM:.3f}", 14, GREEN, BOLD).next_to(depth_arrow, RIGHT, buff=0.07)
        base_arrow = DoubleArrow([xl, y_maj + 0.36, 0], [xr, y_maj + 0.36, 0], buff=0, color=PURPLE, stroke_width=2.0)
        base_lab = self._text(f"b = {PROFILE_WIDTH_MM:.3f}", 13, PURPLE, BOLD).next_to(base_arrow, UP, buff=0.03)
        angle_arc = Arc(radius=0.43, start_angle=60 * DEGREES, angle=60 * DEGREES,
                        arc_center=[cx, y_min, 0], color=ORANGE, stroke_width=2.5)
        angle_lab = self._text("60°", 14, ORANGE, BOLD).move_to([cx, y_min + 0.54, 0])
        half_left = self._text("30°", 11, MUTED, BOLD).move_to([cx - 0.30, y_min + 0.29, 0])
        half_right = self._text("30°", 11, MUTED, BOLD).move_to([cx + 0.30, y_min + 0.29, 0])

        formula = VGroup(
            self._text("h = (Øext − Øint) / 2", 15, GREEN, BOLD),
            self._text("b = 2 h tan(30°)", 15, PURPLE, BOLD),
            self._text("P = repetición axial", 15, ORANGE, BOLD),
        ).arrange(RIGHT, buff=0.52).move_to([0.0, -1.53, 0])
        self._safe_fit(formula, 7.65)

        return {
            "all": VGroup(panel, head, sub, grid, major, minor, major_lab, minor_lab, centers,
                          pitch_arrow, pitch_lab, left_flank, right_flank, crest_line,
                          depth_arrow, depth_lab, base_arrow, base_lab, angle_arc, angle_lab,
                          half_left, half_right, formula),
            "panel": panel, "head": head, "sub": sub, "grid": grid,
            "major": major, "minor": minor, "major_lab": major_lab, "minor_lab": minor_lab,
            "centers": centers, "pitch_arrow": pitch_arrow, "pitch_lab": pitch_lab,
            "left": left_flank, "right": right_flank, "crest": crest_line,
            "depth_arrow": depth_arrow, "depth_lab": depth_lab,
            "base_arrow": base_arrow, "base_lab": base_lab,
            "angle_arc": angle_arc, "angle_lab": angle_lab, "half_left": half_left, "half_right": half_right,
            "formula": formula,
            "triangle_points": ([xl, y_maj, 0], [cx, y_min, 0], [xr, y_maj, 0]),
            "pitch_vis": pitch_vis,
        }

    def construct(self):
        self.install_hud([], [])
        self.intro("De tres datos medibles a una hélice paramétrica")

        self.set_stage(0)
        self.set_tool("Measure")
        self.set_feature("Sketch1")
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.88, run_time=0.80)

        outer = cylinder(R_MAJOR, 4.65, STEEL, 0.16)
        minor = cylinder(R_MINOR, 4.65, STEEL_DARK, 0.92)
        axis = DashedLine([0, 0, -2.55], [0, 0, 2.55], color=UI_MID, dash_length=0.12, stroke_width=2.2)
        top_outer = Circle(radius=R_MAJOR, color=BLUE, stroke_width=3.0).move_to([0, 0, 2.33])
        top_minor = Circle(radius=R_MINOR, color=RED, stroke_width=2.8).move_to([0, 0, 2.34])
        major_rad = Line3D([0, 0, 2.36], [R_MAJOR, 0, 2.36], color=BLUE, thickness=0.018)
        minor_rad = Line3D([0, 0, 2.38], [R_MINOR, 0, 2.38], color=RED, thickness=0.018)

        self.play(FadeIn(minor), Create(axis), run_time=0.75)
        self.play(FadeIn(outer), Create(top_outer), Create(top_minor), run_time=0.85)
        self.play(Create(major_rad), run_time=0.45)
        self.pulse_field("Major Ø", BLUE)
        self.step(1, "Mide el diámetro exterior", "La cresta del filete queda contenida por Øext.", 1.35)
        self.play(Create(minor_rad), run_time=0.45)
        self.pulse_field("Minor Ø", RED)
        self.step(2, "Mide el diámetro interior", "La raíz del filete queda contenida por Øint.", 1.35)
        self.pulse_field("Pitch", ORANGE)
        self.step(3, "Registra el paso P", "P es la distancia axial entre puntos equivalentes de dos filetes.", 1.45)
        self.flash_status("Measured: Øext 20.000 mm  |  Øint 17.294 mm  |  Pitch 2.50 mm")

        self.set_stage(1)
        self.set_tool("Inspect")
        depth_seg = Line3D([R_MINOR, 0, 1.15], [R_MAJOR, 0, 1.15], color=GREEN, thickness=0.030)
        depth_dot_a = Dot3D([R_MINOR, 0, 1.15], radius=0.050, color=GREEN)
        depth_dot_b = Dot3D([R_MAJOR, 0, 1.15], radius=0.050, color=GREEN)
        self.play(FadeOut(major_rad), FadeOut(minor_rad), Create(depth_seg), FadeIn(depth_dot_a), FadeIn(depth_dot_b), run_time=0.72)
        card = self.callout(
            "PROFUNDIDAD RADIAL",
            f"h = (20.000 − 17.294) / 2 = {RADIAL_DEPTH_MM:.3f} mm",
            GREEN, center=[-0.28, 0.72, 0], width=6.70, height=1.12,
        )
        self.set_field_value("Depth h", f"{RADIAL_DEPTH_MM:.3f} mm", GREEN)
        self.pulse_field("Depth h", GREEN)
        self.step(4, "Convierte diferencia de diámetros en profundidad", "La diferencia diametral se divide entre 2 para obtener la altura radial del perfil.", 1.65)
        self.clear_callout(card)

        self.play(FadeOut(outer), minor.animate.set_opacity(0.18), FadeOut(top_outer), FadeOut(top_minor), FadeOut(depth_seg), FadeOut(depth_dot_a), FadeOut(depth_dot_b), run_time=0.55)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=0.80)
        self.play(FadeOut(minor), FadeOut(axis), run_time=0.35)

        self.set_stage(2)
        self.set_tool("Sketch")
        self.set_feature("Sketch1")
        sk = self.precision_sketch()
        self.add_fixed_in_frame_mobjects(sk["all"])
        sk["all"].set_z_index(140)
        self.play(FadeIn(sk["panel"]), Write(sk["head"]), FadeIn(sk["sub"]), run_time=0.55)
        self.play(LaggedStart(*[Create(line) for line in sk["grid"]], lag_ratio=0.003), run_time=0.70)
        self.play(Create(sk["major"]), FadeIn(sk["major_lab"]), run_time=0.48)
        self.play(Create(sk["minor"]), FadeIn(sk["minor_lab"]), run_time=0.48)
        self.step(5, "Proyecta Øext y Øint en la sección", "Dos envolventes radiales fijan exactamente la altura h.", 1.45)

        self.play(Create(sk["centers"]), GrowArrow(sk["pitch_arrow"]), FadeIn(sk["pitch_lab"]), run_time=0.68)
        self.step(6, "Separa estaciones consecutivas una distancia P", "P coloca la repetición del filete; todavía no define la base del triángulo.", 1.55)

        self.play(Create(sk["left"]), run_time=0.58)
        self.play(Create(sk["right"]), run_time=0.58)
        self.play(Create(sk["crest"]), run_time=0.30)
        self.play(GrowArrow(sk["depth_arrow"]), FadeIn(sk["depth_lab"]), run_time=0.50)
        self.pulse_field("Depth h", GREEN)
        self.play(Create(sk["angle_arc"]), FadeIn(sk["angle_lab"]), FadeIn(sk["half_left"]), FadeIn(sk["half_right"]), run_time=0.55)
        self.pulse_field("Flank angle", PURPLE)
        self.step(7, "Construye dos flancos simétricos", "60° entre flancos implica 30° a cada lado del eje del perfil.", 1.70)

        self.play(GrowArrow(sk["base_arrow"]), FadeIn(sk["base_lab"]), run_time=0.55)
        self.set_field_value("Profile b", f"{PROFILE_WIDTH_MM:.3f} mm", PURPLE)
        self.pulse_field("Profile b", PURPLE)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.03) for x in sk["formula"]], lag_ratio=0.18), run_time=0.80)
        self.step(8, "Calcula la base geométrica b", "b = 2h·tan(30°) = 1.562 mm; aquí b < P.", 1.70)

        p0, p1, p2 = [np.array(p) for p in sk["triangle_points"]]
        tri_copy = Polygon(p0, p1, p2, stroke_color=CYAN, stroke_width=3.3, fill_color=CYAN, fill_opacity=0.08)
        tri_copy.shift(RIGHT * sk["pitch_vis"])
        ghost_arrow = Arrow([p1[0], p1[1] - 0.18, 0], [p1[0] + sk["pitch_vis"], p1[1] - 0.18, 0], buff=0.02, color=ORANGE, stroke_width=2.3)
        self.add_fixed_in_frame_mobjects(tri_copy, ghost_arrow)
        self.play(FadeIn(tri_copy, shift=RIGHT * 0.10), GrowArrow(ghost_arrow), run_time=0.70)
        self.play(Indicate(tri_copy, color=CYAN, scale_factor=1.02), run_time=0.45)
        self.step(9, "Duplica el perfil exactamente una distancia P", "Esta repetición 2D anticipa la separación axial que usará Coil.", 1.55)
        self.play(FadeOut(tri_copy), FadeOut(ghost_arrow), run_time=0.30)
        self.remove_fixed_in_frame_mobjects(tri_copy, ghost_arrow)

        self.play(FadeOut(sk["all"]), run_time=0.48)
        self.remove_fixed_in_frame_mobjects(sk["all"])
        self.remove(sk["all"])

        self.set_stage(3)
        self.set_tool("Coil")
        self.set_feature("Axis")
        self.move_camera(phi=66 * DEGREES, theta=-50 * DEGREES, zoom=0.88, run_time=0.86)
        outer = cylinder(R_MAJOR, 4.65, STEEL, 0.10)
        minor = cylinder(R_MINOR, 4.65, STEEL_DARK, 0.78)
        axis = DashedLine([0, 0, -2.58], [0, 0, 2.58], color=UI_MID, dash_length=0.12, stroke_width=2.2)
        profile = sharp_profile_triangle(SKETCH, 0.18)
        radial = Line3D([0, 0, Z0], [R_MINOR, 0, Z0], color=ORANGE, thickness=0.018)
        self.play(FadeIn(minor), FadeIn(outer), Create(axis), run_time=0.65)
        self.play(FadeIn(profile, scale=1.08), Create(radial), run_time=0.62)
        self.set_feature("Sketch1")
        self.step(10, "Selecciona Sketch1 como Profile", "El triángulo es la sección que viajará por la trayectoria helicoidal.", 1.55)
        self.set_feature("Axis")
        self.play(Indicate(axis, color=ORANGE, scale_factor=1.02), run_time=0.48)
        self.step(11, "Selecciona la Centerline como Axis", "El eje controla el giro; el Pitch controla el avance axial por vuelta.", 1.55)
        self.pulse_field("Type", BLUE)
        self.pulse_field("Pitch", ORANGE)

        path = helix_curve(PREVIEW, 7.5, 0.76)
        tracer = Dot3D(helix_center(0), radius=0.062, color=ORANGE)
        self.play(Create(path), run_time=1.15)
        self.play(MoveAlongPath(tracer, path), run_time=2.25, rate_func=linear)
        self.step(12, "Previsualiza la hélice", "Después de 360°, el perfil avanza exactamente P = 2.50 mm.", 1.55)

        sample_us = np.linspace(0.0, 2.8 * TAU, 10)
        slices = VGroup(*[self.profile_slice(float(u), CYAN, 0.13) for u in sample_us])
        self.play(LaggedStart(*[FadeIn(s, scale=0.94) for s in slices], lag_ratio=0.10), run_time=1.65)
        self.play(LaggedStart(*[Indicate(s, color=CYAN, scale_factor=1.02) for s in slices], lag_ratio=0.06), run_time=1.10)
        self.step(13, "Observa el barrido del mismo triángulo", "Las secciones sucesivas revelan cómo Coil transporta el perfil sin cambiar su forma.", 1.65)

        swept = triangular_thread_surface(PREVIEW, 0.46)
        self.play(FadeIn(swept), FadeOut(slices), profile.animate.set_opacity(0.28), path.animate.set_opacity(0.18), FadeOut(tracer), run_time=1.05)
        self.pulse_field("Operation", RED)
        self.step(14, "Revisa la operación Cut", "Para una rosca exterior, el perfil puede representar material removido alrededor del cilindro base.", 1.70)
        self.begin_ambient_camera_rotation(rate=0.055)
        self.wait(1.30)
        self.stop_ambient_camera_rotation()

        self.set_stage(4)
        self.set_tool("Inspect")
        self.set_feature("Coil1")
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.90, run_time=0.80)
        section = self.callout(
            "SECTION A–A",
            "Verifica h, 60° y separación P sin depender de la perspectiva.",
            PURPLE, center=[-0.25, 1.62, 0], width=6.50, height=1.04,
        )
        self.play(Indicate(swept, color=PURPLE, scale_factor=1.01), run_time=0.58)
        self.step(15, "Valida el perfil en sección", "La sección debe conservar la altura h y los flancos simétricos.", 1.45)
        self.clear_callout(section)

        self.move_camera(phi=8 * DEGREES, theta=-90 * DEGREES, zoom=0.94, run_time=0.80)
        axial_outer = Circle(radius=R_MAJOR, color=BLUE, stroke_width=3.0).move_to([0, 0, 2.36])
        axial_minor = Circle(radius=R_MINOR, color=RED, stroke_width=2.6).move_to([0, 0, 2.37])
        self.play(Create(axial_outer), Create(axial_minor), run_time=0.62)
        axial = self.callout(
            "AXIAL VIEW",
            "Comprueba concentricidad entre Øext, Øint y Axis.",
            BLUE, center=[-0.25, 1.70, 0], width=5.85, height=0.98,
        )
        self.step(16, "Valida concentricidad", "Si las envolventes no son concéntricas, el perfil o el eje están mal referenciados.", 1.45)
        self.clear_callout(axial)
        self.play(FadeOut(axial_outer), FadeOut(axial_minor), run_time=0.35)

        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.82)
        self.set_tool("Coil")
        edit_card = self.callout(
            "EDICIÓN PARAMÉTRICA",
            "Pitch: 2.50 mm → 3.00 mm → 2.50 mm",
            ORANGE, center=[-0.25, 1.66, 0], width=6.10, height=1.02,
        )
        path25 = self.pitch_helix(PITCH_WORLD, color=ORANGE, width=7.2)
        path30 = self.pitch_helix(PITCH_WORLD * (3.0 / 2.5), color=ORANGE, width=7.2)
        self.play(FadeOut(swept), FadeOut(path), FadeIn(path25), run_time=0.48)
        self.set_field_value("Pitch", "3.00 mm", ORANGE)
        self.play(Transform(path25, path30), run_time=1.50, rate_func=smooth)
        self.wait(0.35)
        self.set_field_value("Pitch", f"{PITCH_MM:.2f} mm", INK)
        self.play(Transform(path25, self.pitch_helix(PITCH_WORLD, color=ORANGE, width=7.2)), run_time=1.40, rate_func=smooth)
        self.step(17, "Comprueba que Pitch controla la separación", "Mayor P separa vueltas; el triángulo conserva h, b y 60°.", 1.55)
        self.clear_callout(edit_card)
        self.play(FadeOut(path25), run_time=0.35)

        self.set_stage(5)
        self.set_tool("Coil")
        self.set_feature("Coil1")
        final_thread = triangular_thread_surface(STEEL, 0.96)
        self.play(FadeOut(profile), FadeOut(radial), FadeOut(outer), FadeIn(final_thread), minor.animate.set_opacity(1.0), axis.animate.set_opacity(0.16), run_time=1.00)
        self.flash_status("Coil1 updated  |  Profile: Sketch1  |  Axis: Centerline  |  Pitch 2.50 mm  |  Operation: Cut")
        self.play(Indicate(self._ok_group, color=ORANGE, scale_factor=1.04), run_time=0.55)
        self.step(18, "Confirma Coil1", "El árbol paramétrico conserva Sketch1, Axis y todos los parámetros editables.", 1.70)

        summary = self.callout(
            "MÉTODO COMPLETO",
            "Øext, Øint → h   |   h + 60° → b   |   P → repetición helicoidal   |   Coil → geometría 3D",
            GREEN, center=[-0.25, 1.58, 0], width=8.05, height=1.15,
        )
        self.begin_ambient_camera_rotation(rate=0.060)
        self.wait(2.20)
        self.stop_ambient_camera_rotation()
        self.clear_callout(summary)

        rigor = self.callout(
            "NOTA DE RIGOR",
            "El perfil V es didáctico. Una rosca normalizada real incorpora truncamientos y radios de cresta/raíz definidos por su norma.",
            RED, center=[-0.25, 1.56, 0], width=8.10, height=1.20,
        )
        self.wait(1.45)
        self.clear_callout(rigor)
        self.begin_ambient_camera_rotation(rate=0.045)
        self.wait(2.10)
        self.stop_ambient_camera_rotation()
        self.wait(0.50)
