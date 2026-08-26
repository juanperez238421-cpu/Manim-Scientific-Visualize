from __future__ import annotations

import math
from dataclasses import dataclass
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#D7D9DC"

UI_DARK = "#25282B"
UI_DARK_2 = "#303438"
UI_MID = "#555B60"
UI_LINE = "#A9ADB1"
UI_LIGHT = "#F4F5F6"
UI_PANEL = "#ECEEEF"
UI_PANEL_2 = "#E1E4E6"
CANVAS = "#D7D9DC"
TEXT = "#202326"
TEXT_LIGHT = "#F7F7F7"
STEEL = "#B8BDC1"
STEEL_DARK = "#8D9499"
SKETCH = "#276FBF"
SELECT = "#E78913"
PREVIEW = "#6E9F76"
WHITE = "#FFFFFF"


def txt(content: str, size: int = 24, color: str = TEXT, weight=NORMAL) -> Text:
    return Text(content, font_size=size, color=color, weight=weight, font="DejaVu Sans")


def fit(mob: Mobject, max_width: float, max_height: float | None = None) -> Mobject:
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    if max_height is not None and mob.height > max_height:
        mob.scale_to_fit_height(max_height)
    return mob


def cuboid(width: float, depth: float, height: float, color: str = STEEL, opacity: float = 1.0) -> Cube:
    obj = Cube(side_length=1.0, fill_color=color, fill_opacity=opacity,
               stroke_color=UI_MID, stroke_width=1.15)
    obj.stretch_to_fit_width(width)
    obj.stretch_to_fit_height(depth)
    obj.stretch_to_fit_depth(height)
    return obj


def cylinder(radius: float, height: float, color: str = STEEL, opacity: float = 1.0) -> Cylinder:
    return Cylinder(radius=radius, height=height, direction=OUT,
                    fill_color=color, fill_opacity=opacity,
                    stroke_color=UI_MID, stroke_width=1.05,
                    resolution=(8, 24))


def rounded_plate(width: float, depth: float, height: float, radius: float, color: str = STEEL) -> VGroup:
    body_x = cuboid(width - 2 * radius, depth, height, color)
    body_y = cuboid(width, depth - 2 * radius, height, color)
    corners = VGroup()
    for sx in (-1, 1):
        for sy in (-1, 1):
            cap = cylinder(radius, height, color)
            cap.shift([sx * (width / 2 - radius), sy * (depth / 2 - radius), 0])
            corners.add(cap)
    return VGroup(body_x, body_y, corners)


def extruded_polygon(points: list[tuple[float, float]], height: float,
                     color: str = STEEL, opacity: float = 1.0) -> VGroup:
    z0, z1 = -height / 2, height / 2
    lower = [np.array([x, y, z0]) for x, y in points]
    upper = [np.array([x, y, z1]) for x, y in points]
    faces = VGroup(
        Polygon(*lower, fill_color=color, fill_opacity=opacity, stroke_color=UI_MID, stroke_width=1.1),
        Polygon(*upper, fill_color=color, fill_opacity=opacity, stroke_color=UI_MID, stroke_width=1.1),
    )
    for i in range(len(points)):
        j = (i + 1) % len(points)
        faces.add(Polygon(lower[i], lower[j], upper[j], upper[i],
                          fill_color=color, fill_opacity=opacity,
                          stroke_color=UI_MID, stroke_width=1.0))
    return faces


@dataclass
class HUD:
    group: VGroup
    status_text: Text


class InventorOperationScene(ThreeDScene):
    OPERATION = "Feature"
    FEATURE_NODE = "Feature1"

    def setup(self):
        super().setup()
        self.camera.background_color = CANVAS
        self.set_camera_orientation(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86)
        self.hud: HUD | None = None
        self.step_box: VGroup | None = None

    def _tool_button(self, label: str, x: float, y: float, active: bool = False, width: float = 0.92) -> VGroup:
        box = RoundedRectangle(width=width, height=0.58, corner_radius=0.04,
                               stroke_color=SELECT if active else UI_LINE,
                               stroke_width=2.1 if active else 0.8,
                               fill_color=WHITE, fill_opacity=0.95)
        box.move_to([x, y, 0])
        icon = Square(side_length=0.16, stroke_width=1.1, stroke_color=UI_MID,
                      fill_color=STEEL, fill_opacity=1)
        icon.move_to(box.get_top() + DOWN * 0.16)
        t = txt(label, 12, TEXT, BOLD if active else NORMAL)
        fit(t, width - 0.08, 0.16)
        t.next_to(icon, DOWN, buff=0.055)
        return VGroup(box, icon, t)

    def build_hud(self, property_rows: list[tuple[str, str]], browser_nodes: list[str]) -> HUD:
        title_bar = Rectangle(width=16, height=0.42, stroke_width=0,
                              fill_color=UI_DARK, fill_opacity=1).to_edge(UP, buff=0)
        app_mark = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.03,
                                    stroke_width=0, fill_color=SELECT, fill_opacity=1).move_to([-7.72, 4.29, 0])
        app_i = txt("I", 19, WHITE, BOLD).move_to(app_mark)
        title = txt(f"Autodesk Inventor Professional 2026  |  {self.OPERATION}  |  Part1.ipt", 18, TEXT_LIGHT)
        title.move_to([-3.35, 4.29, 0])

        tabs_bg = Rectangle(width=16, height=0.42, stroke_width=0,
                            fill_color=UI_LIGHT, fill_opacity=1).move_to([0, 3.87, 0])
        tab_names = ["File", "3D Model", "Sketch", "Annotate", "Inspect", "Tools", "Manage", "View"]
        tabs = VGroup()
        x = -7.45
        for name in tab_names:
            t = txt(name, 17, TEXT, BOLD if name == "3D Model" else NORMAL)
            t.move_to([x + t.width / 2, 3.88, 0])
            tabs.add(t)
            if name == "3D Model":
                tabs.add(Line([x, 3.69, 0], [x + t.width + 0.12, 3.69, 0], color=SELECT, stroke_width=3))
            x += t.width + 0.34

        ribbon = Rectangle(width=16, height=0.93, stroke_color=UI_LINE, stroke_width=0.8,
                           fill_color=UI_PANEL, fill_opacity=1).move_to([0, 3.20, 0])
        tools = [
            ("Extrude", -6.95, 0.92), ("Revolve", -5.95, 0.92), ("Sweep", -4.95, 0.92), ("Loft", -4.00, 0.82),
            ("Fillet", -2.95, 0.86), ("Chamfer", -1.95, 1.02), ("Shell", -0.90, 0.86),
            ("Rectangular", 0.35, 1.18), ("Circular", 1.65, 0.98), ("Mirror", 2.72, 0.90),
            ("Rib", 3.75, 0.76), ("Emboss", 4.65, 0.94), ("Coil", 5.62, 0.76),
        ]
        ribbon_content = VGroup()
        op_l = self.OPERATION.lower()
        aliases = {
            "rectangular pattern": "rectangular",
            "circular pattern": "circular",
        }
        active_name = aliases.get(op_l, op_l)
        for label, xpos, width in tools:
            active = label.lower() == active_name
            ribbon_content.add(self._tool_button(label, xpos, 3.29, active, width))
        ribbon_content.add(txt("Create", 11, UI_MID).move_to([-5.55, 2.80, 0]))
        ribbon_content.add(txt("Modify", 11, UI_MID).move_to([-1.95, 2.80, 0]))
        ribbon_content.add(txt("Pattern", 11, UI_MID).move_to([1.55, 2.80, 0]))
        ribbon_content.add(txt("Create", 11, UI_MID).move_to([4.65, 2.80, 0]))

        browser = Rectangle(width=2.30, height=6.02, stroke_color=UI_LINE, stroke_width=0.9,
                            fill_color=UI_LIGHT, fill_opacity=0.985).move_to([-6.84, -0.33, 0])
        bhead = Rectangle(width=2.30, height=0.40, stroke_width=0,
                          fill_color=UI_PANEL_2, fill_opacity=1).move_to([-6.84, 2.48, 0])
        btitle = txt("Model", 18, TEXT, BOLD).move_to(bhead)
        tree = VGroup()
        y = 2.10
        for i, node in enumerate(browser_nodes):
            prefix = "▾" if i == 0 else ("  ▸" if node == "Origin" else "    •")
            row = txt(prefix + " " + node, 14, TEXT if i < 2 else UI_MID)
            fit(row, 2.02)
            row.move_to([-7.86 + row.width / 2, y, 0])
            tree.add(row)
            y -= 0.34
        browser_group = VGroup(browser, bhead, btitle, tree)

        prop = Rectangle(width=3.20, height=6.02, stroke_color=UI_LINE, stroke_width=0.9,
                         fill_color=UI_LIGHT, fill_opacity=0.99).move_to([6.15, -0.33, 0])
        phead = Rectangle(width=3.20, height=0.50, stroke_width=0,
                          fill_color=UI_DARK_2, fill_opacity=1).move_to([6.15, 2.43, 0])
        ptitle = txt(self.OPERATION, 19, TEXT_LIGHT, BOLD).move_to(phead)
        rows = VGroup()
        y = 1.92
        for label, value in property_rows:
            l = txt(label, 13, UI_MID).move_to([4.76, y, 0])
            l.align_to(prop, LEFT).shift(RIGHT * 0.15)
            box = RoundedRectangle(width=1.42, height=0.32, corner_radius=0.04,
                                   stroke_color=UI_LINE, stroke_width=0.8,
                                   fill_color=WHITE, fill_opacity=1).move_to([6.72, y, 0])
            v = txt(value, 13, TEXT, BOLD).move_to(box)
            fit(v, 1.30, 0.22)
            rows.add(l, box, v)
            y -= 0.52
        ok = RoundedRectangle(width=0.88, height=0.38, corner_radius=0.05,
                              stroke_width=0, fill_color=SELECT, fill_opacity=1).move_to([6.55, -2.96, 0])
        ok_t = txt("OK", 15, WHITE, BOLD).move_to(ok)
        cancel = RoundedRectangle(width=1.02, height=0.38, corner_radius=0.05,
                                  stroke_color=UI_LINE, stroke_width=0.9,
                                  fill_color=WHITE, fill_opacity=1).move_to([5.35, -2.96, 0])
        cancel_t = txt("Cancel", 14, TEXT).move_to(cancel)
        property_group = VGroup(prop, phead, ptitle, rows, ok, ok_t, cancel, cancel_t)

        cube = Square(side_length=0.72, stroke_color=UI_MID, stroke_width=1.0,
                      fill_color=UI_LIGHT, fill_opacity=0.95).move_to([4.12, 2.05, 0])
        cube_t = txt("TOP\nFRONT", 10, UI_MID, BOLD).move_to(cube)
        nav = txt("Orbit    Zoom    Fit", 12, UI_MID).move_to([3.55, -3.54, 0])
        status = Rectangle(width=16, height=0.38, stroke_width=0,
                           fill_color=UI_LIGHT, fill_opacity=1).to_edge(DOWN, buff=0)
        status_text = txt("Ready     |     Select geometry or use the property panel     |     mm", 13, UI_MID)
        status_text.move_to([-1.25, -4.31, 0])

        group = VGroup(title_bar, app_mark, app_i, title, tabs_bg, tabs, ribbon, ribbon_content,
                       browser_group, property_group, cube, cube_t, nav, status, status_text)
        return HUD(group, status_text)

    def install_hud(self, property_rows: list[tuple[str, str]], browser_nodes: list[str]):
        self.hud = self.build_hud(property_rows, browser_nodes)
        self.add_fixed_in_frame_mobjects(self.hud.group)

    def intro(self, subtitle: str):
        card = RoundedRectangle(width=7.8, height=1.18, corner_radius=0.10,
                                stroke_color=UI_LINE, stroke_width=0.8,
                                fill_color=UI_LIGHT, fill_opacity=0.95)
        title = txt(self.OPERATION.upper(), 29, TEXT, BOLD)
        sub = txt(subtitle, 17, UI_MID)
        fit(title, 7.2)
        fit(sub, 7.2)
        title.move_to(card).shift(UP * 0.20)
        sub.next_to(title, DOWN, buff=0.08)
        group = VGroup(card, title, sub).move_to([-0.25, 0.25, 0])
        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group, scale=0.97), run_time=0.5)
        self.wait(1.7)
        self.play(FadeOut(group), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(group)

    def step(self, number: int, title: str, detail: str, duration: float = 2.35):
        if self.step_box is not None:
            self.remove_fixed_in_frame_mobjects(self.step_box)
            self.remove(self.step_box)
        panel = RoundedRectangle(width=8.45, height=0.76, corner_radius=0.08,
                                 stroke_color=UI_LINE, stroke_width=0.8,
                                 fill_color="#F8F9FA", fill_opacity=0.97).move_to([-0.20, -3.05, 0])
        num = RoundedRectangle(width=0.56, height=0.56, corner_radius=0.08,
                               stroke_width=0, fill_color=SELECT, fill_opacity=1)
        num.move_to(panel.get_left() + RIGHT * 0.38)
        n = txt(str(number), 20, WHITE, BOLD).move_to(num)
        t = txt(title, 18, TEXT, BOLD)
        d = txt(detail, 14, UI_MID)
        fit(t, 7.1)
        fit(d, 7.1)
        t.move_to([-3.82, -2.93, 0])
        t.align_to(panel, LEFT).shift(RIGHT * 0.82)
        d.next_to(t, DOWN, buff=0.05, aligned_edge=LEFT)
        self.step_box = VGroup(panel, num, n, t, d)
        self.add_fixed_in_frame_mobjects(self.step_box)
        self.play(FadeIn(self.step_box, shift=UP * 0.04), run_time=0.35)
        self.wait(duration)

    def flash_status(self, content: str):
        if self.hud is None:
            return
        old = self.hud.status_text
        new = txt(content, 13, UI_MID).move_to(old)
        self.add_fixed_in_frame_mobjects(new)
        self.play(ReplacementTransform(old, new), run_time=0.25)
        self.hud.status_text = new

    def finish(self, final_message: str):
        self.step(6, "Operación creada", final_message, 2.8)
        self.flash_status(f"Feature created: {self.FEATURE_NODE}     |     Model updated     |     mm")
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)
