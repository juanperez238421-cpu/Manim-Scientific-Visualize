from manim import *
import numpy as np

# ManimCE 0.20.1 | 1920x1080 | render with -pqh
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#E8EDF2"

BG = "#E8EDF2"
CANVAS = "#DCE3E9"
NAVY = "#123B5D"
NAVY_D = "#0D2A41"
BLUE = "#0A78B9"
CYAN = "#00A7D8"
SKETCH = "#1678C8"
PURPLE = "#8B5CF6"
RED = "#D9485F"
ORANGE = "#F39C34"
GREEN = "#22A06B"
INK = "#20262D"
MUTED = "#64717D"
LINE = "#B9C4CD"
TOP = "#77B4DD"
SIDE_A = "#347FAF"
SIDE_B = "#276B99"
BOTTOM = "#245D82"
HOLE = "#284656"


class InventorSketchToVolume3D(ThreeDScene):
    """True 3D explanation of a constrained Inventor-style sketch extrusion."""

    OUTER = [
        (-3.20, -1.50), (-2.70, -2.00), (2.70, -2.00), (3.20, -1.50),
        (3.20, 1.50), (2.70, 2.00), (-2.70, 2.00), (-3.20, 1.50),
    ]
    HOLES = [
        (-2.20, -1.05, 0.32), (2.20, -1.05, 0.32),
        (2.20, 1.05, 0.32), (-2.20, 1.05, 0.32),
        (0.00, 0.00, 0.72),
    ]
    DEPTH = 1.60

    def construct(self):
        self.camera.background_color = BG
        self.depth = ValueTracker(0.03)
        self.build_ui()
        self.intro()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.92)
        plane = self.show_sketch_plane()
        profile, holes = self.draw_profile()
        annotations = self.constrain_profile(profile, holes)
        selection = self.select_region()
        solid = self.extrude(profile, holes, annotations, selection, plane)
        self.explain_volume(solid)
        self.show_parametric_history(solid)
        self.show_cfd_handoff(solid)
        self.finish(solid)

    # ---------- fixed CAD interface ----------
    def text(self, s, size=24, color=INK, weight=NORMAL):
        return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)

    def panel(self, w, h, fill="#F9FBFC", stroke=LINE, r=0.08):
        return RoundedRectangle(
            width=w, height=h, corner_radius=r,
            fill_color=fill, fill_opacity=0.98,
            stroke_color=stroke, stroke_width=1,
        )

    def build_ui(self):
        top = Rectangle(width=16, height=0.48, fill_color=NAVY_D, fill_opacity=1, stroke_width=0).to_edge(UP, buff=0)
        app = self.text("A", 27, "#E74C4C", BOLD).move_to([-7.52, 4.26, 0])
        name = self.text("Autodesk Inventor-style CAD", 17, WHITE, MEDIUM).next_to(app, RIGHT, buff=0.14)
        file = self.text("CFD_Flange_Extrusion.ipt", 16, "#D9E7F0").move_to([0.1, 4.25, 0])
        ribbon = Rectangle(width=16, height=0.95, fill_color="#F4F6F8", fill_opacity=1, stroke_color=LINE, stroke_width=1).next_to(top, DOWN, buff=0)

        tools = VGroup(*[
            self.tool("Start 2D\nSketch", "✎", True), self.tool("Extrude", "▥"),
            self.tool("Revolve", "↻"), self.tool("Hole", "◎"),
            self.tool("Fillet", "⌒"), self.tool("Inspect", "⌕"),
        ]).arrange(RIGHT, buff=0.08).to_edge(LEFT, buff=0.24).shift(UP * 3.25)

        browser = self.panel(2.65, 6.72, fill="#F7F9FA", r=0.02).to_edge(LEFT, buff=0).shift(DOWN * 0.58)
        browser_title = self.text("MODEL BROWSER", 15, INK, BOLD).move_to([-1.32, 2.53, 0])
        self.tree = VGroup(
            self.text("▾ CFD_Flange_Extrusion.ipt", 14, INK, BOLD),
            self.text("   ▸ Origin", 14, MUTED), self.text("      XY Plane", 13, MUTED),
            self.text("   Sketch1", 14, SKETCH, MEDIUM),
            self.text("   Extrusion1", 14, GREEN, MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-1.22, 1.55, 0], aligned_edge=UL)
        self.tree[3:].set_opacity(0.18)

        self.status_box = self.panel(4.95, 0.78).to_corner(DR, buff=0.22).shift(UP * 0.62)
        self.status_text = VGroup(
            self.text("STEP 1 — SELECT A PLANE", 17, BLUE, BOLD),
            self.text("The XY plane defines the sketch coordinates", 14, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(self.status_box)

        self.steps = VGroup(*[self.step_node(i + 1, label) for i, label in enumerate(["Sketch", "Constrain", "Extrude", "Solid", "CFD"])])
        self.steps.arrange(RIGHT, buff=0.72).to_edge(DOWN, buff=0.18).shift(RIGHT * 1.3)

        ui = VGroup(top, app, name, file, ribbon, tools, browser, browser_title, self.tree, self.status_box, self.status_text, self.steps)
        self.add_fixed_in_frame_mobjects(ui)
        ui.set_z_index(100)
        self.set_step(0, False)

    def tool(self, label, glyph, active=False):
        tile = RoundedRectangle(width=1.08, height=0.64, corner_radius=0.05,
                                fill_color="#DDEFF9" if active else "#F4F6F8", fill_opacity=1,
                                stroke_color=BLUE if active else LINE, stroke_width=1)
        content = VGroup(self.text(glyph, 22, BLUE if active else INK, BOLD), self.text(label, 11, INK, MEDIUM)).arrange(DOWN, buff=0.01).move_to(tile)
        return VGroup(tile, content)

    def step_node(self, n, label):
        c = Circle(radius=0.18, fill_color="#F9FBFC", fill_opacity=1, stroke_color=LINE, stroke_width=2)
        num = self.text(str(n), 14, MUTED, BOLD).move_to(c)
        cap = self.text(label, 12, MUTED, MEDIUM).next_to(c, DOWN, buff=0.05)
        return VGroup(c, num, cap)

    def set_step(self, index, animate=True):
        anims = []
        for i, node in enumerate(self.steps):
            fill = BLUE if i == index else GREEN if i < index else "#F9FBFC"
            tc = WHITE if i <= index else MUTED
            cc = INK if i <= index else MUTED
            if animate:
                anims += [node[0].animate.set_fill(fill, 1).set_stroke(fill), node[1].animate.set_color(tc), node[2].animate.set_color(cc)]
            else:
                node[0].set_fill(fill, 1).set_stroke(fill)
                node[1].set_color(tc); node[2].set_color(cc)
        if animate:
            self.play(*anims, run_time=0.45)

    def set_status(self, title, body, color=BLUE):
        new = VGroup(self.text(title, 17, color, BOLD), self.text(body, 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(self.status_box)
        self.play(Transform(self.status_text, new), run_time=0.45)

    # ---------- geometry builders ----------
    def profile(self, z=0, stroke=SKETCH, fill=SKETCH, fill_opacity=0, width=4):
        p = Polygon(*[np.array([x, y, z]) for x, y in self.OUTER], stroke_color=stroke, stroke_width=width,
                    fill_color=fill, fill_opacity=fill_opacity)
        p.set_shade_in_3d(True)
        return p

    def hole_outlines(self, z=0, color=SKETCH, width=3):
        return VGroup(*[Circle(radius=r, color=color, stroke_width=width).move_to([x, y, z]) for x, y, r in self.HOLES])

    def solid(self, depth, opacity=0.97):
        d = max(float(depth), 0.02)
        bottom_pts = [np.array([x, y, 0]) for x, y in self.OUTER]
        top_pts = [np.array([x, y, d]) for x, y in self.OUTER]
        bottom = Polygon(*bottom_pts, fill_color=BOTTOM, fill_opacity=opacity, stroke_color=NAVY, stroke_width=1)
        top = Polygon(*top_pts, fill_color=TOP, fill_opacity=opacity, stroke_color=NAVY, stroke_width=1.3)
        bottom.set_shade_in_3d(True); top.set_shade_in_3d(True)
        sides = VGroup()
        for i in range(len(bottom_pts)):
            j = (i + 1) % len(bottom_pts)
            face = Polygon(bottom_pts[i], bottom_pts[j], top_pts[j], top_pts[i],
                           fill_color=SIDE_A if i % 2 == 0 else SIDE_B, fill_opacity=opacity,
                           stroke_color=NAVY, stroke_width=0.9)
            face.set_shade_in_3d(True); sides.add(face)
        holes = VGroup(*[self.visual_hole(x, y, r, d) for x, y, r in self.HOLES])
        return VGroup(bottom, sides, top, holes)

    def visual_hole(self, x, y, r, depth):
        wall = Cylinder(radius=r, height=depth, direction=OUT, resolution=(10, 28),
                        fill_color=HOLE, fill_opacity=1, stroke_color=HOLE, stroke_width=0.4).move_to([x, y, depth / 2])
        wall.set_shade_in_3d(True)
        top_open = Circle(radius=r * 0.96, fill_color=BG, fill_opacity=1, stroke_color=NAVY_D, stroke_width=1.1).move_to([x, y, depth + 0.006])
        top_open.set_shade_in_3d(True)
        return VGroup(wall, top_open)

    def sketch_plane(self):
        tile = Rectangle(width=9.1, height=5.8, fill_color=CANVAS, fill_opacity=0.9, stroke_color=BLUE, stroke_width=2).move_to([0, 0, -0.04])
        tile.set_shade_in_3d(True)
        lines = VGroup()
        for x in np.arange(-4.2, 4.21, 0.4):
            lines.add(Line([x, -2.65, -0.02], [x, 2.65, -0.02], color="#C3CED6", stroke_width=0.55))
        for y in np.arange(-2.6, 2.61, 0.4):
            lines.add(Line([-4.2, y, -0.02], [4.2, y, -0.02], color="#C3CED6", stroke_width=0.55))
        axes = VGroup(Line([-4.3, 0, 0], [4.3, 0, 0], color="#D54D5E", stroke_width=2),
                      Line([0, -2.7, 0], [0, 2.7, 0], color="#4B9C70", stroke_width=2))
        return VGroup(tile, lines, axes)

    def dimension(self, a, b, label, offset):
        a = np.array(a, float); b = np.array(b, float); off = np.array(offset, float)
        e1 = Line(a, a + off, color=RED, stroke_width=1.6)
        e2 = Line(b, b + off, color=RED, stroke_width=1.6)
        arr = DoubleArrow(a + off, b + off, buff=0, color=RED, stroke_width=2, tip_length=0.11)
        txt = self.text(label, 17, RED, BOLD).scale(0.62).move_to((a + b) / 2 + off)
        bg = BackgroundRectangle(txt, fill_color=BG, fill_opacity=0.9, buff=0.04, stroke_width=0)
        return VGroup(e1, e2, arr, bg, txt)

    # ---------- animation chapters ----------
    def intro(self):
        card = self.panel(9.8, 2.35, r=0.18).move_to([1.35, 0.35, 0])
        title = self.text("FROM A 2D SKETCH TO A 3D CFD-READY VOLUME", 34, NAVY, BOLD)
        sub = self.text("Real ThreeDScene • parametric extrusion • professional camera movement", 19, MUTED)
        formula = self.text("closed profile + distance × normal vector = solid volume", 21, BLUE, MEDIUM)
        content = VGroup(title, sub, formula).arrange(DOWN, buff=0.22).move_to(card)
        self.add_fixed_in_frame_mobjects(card, content); card.set_z_index(120); content.set_z_index(121)
        self.play(FadeIn(card, scale=0.96), Write(title), run_time=1.1)
        self.play(FadeIn(sub), FadeIn(formula), run_time=0.8); self.wait(1.3)
        self.play(FadeOut(card), FadeOut(content), run_time=0.6)

    def show_sketch_plane(self):
        self.set_status("STEP 1 — SELECT THE XY PLANE", "The plane establishes the 2D coordinate system")
        plane = self.sketch_plane()
        self.play(FadeIn(plane[0], scale=0.94), run_time=0.7)
        self.play(LaggedStart(*[Create(line) for line in plane[1]], lag_ratio=0.01), Create(plane[2]), run_time=1.4)
        origin = Dot3D([0, 0, 0.03], radius=0.08, color=ORANGE)
        self.play(FadeIn(origin, scale=1.5)); self.wait(0.5); self.play(FadeOut(origin))
        return plane

    def draw_profile(self):
        self.set_status("STEP 2 — DRAW CLOSED LOOPS", "Connected edges define the outer region and five holes")
        profile = self.profile()
        holes = self.hole_outlines()
        points = [np.array([x, y, 0.02]) for x, y in self.OUTER]
        edges = VGroup(*[Line(points[i], points[(i + 1) % len(points)], color=SKETCH, stroke_width=4) for i in range(len(points))])
        dots = VGroup(*[Dot3D(p, radius=0.05, color=ORANGE) for p in points])
        self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i]), Create(edges[i])) for i in range(len(edges))], lag_ratio=0.1), run_time=2.4)
        self.play(LaggedStart(*[Create(h) for h in holes], lag_ratio=0.16), run_time=1.3)
        self.add(profile); self.remove(edges); self.play(FadeOut(dots), run_time=0.4)
        self.tree[3].set_opacity(1)
        return profile, holes

    def constrain_profile(self, profile, holes):
        self.set_step(1)
        self.set_status("STEP 3 — CONSTRAIN AND DIMENSION", "Size and geometric relations make the sketch parametric", PURPLE)
        center = VGroup(DashedLine([-3.6, 0, 0.03], [3.6, 0, 0.03], color=PURPLE),
                        DashedLine([0, -2.35, 0.03], [0, 2.35, 0.03], color=PURPLE))
        dims = VGroup(
            self.dimension([-3.2, -1.5, 0.04], [3.2, -1.5, 0.04], "80 mm", [0, -0.75, 0]),
            self.dimension([3.2, -1.5, 0.04], [3.2, 1.5, 0.04], "50 mm", [0.72, 0, 0]),
        )
        leaders = VGroup(
            Line([0.48, 0.48, 0.04], [1.25, 1.25, 0.04], color=RED, stroke_width=2),
            self.text("Ø20 mm", 17, RED, BOLD).scale(0.62).move_to([1.60, 1.42, 0.04]),
            Line([-2.2, -1.05, 0.04], [-3.0, -0.35, 0.04], color=RED, stroke_width=2),
            self.text("4 × Ø8 mm", 17, RED, BOLD).scale(0.62).move_to([-3.38, -0.10, 0.04]),
        )
        icons = VGroup(*[VGroup(Circle(radius=0.16, fill_color=WHITE, fill_opacity=1, stroke_color=PURPLE, stroke_width=1.4), self.text(g, 14, PURPLE, BOLD)) for g in ["H", "V", "⊥", "=", "⊙"]])
        for icon, pos in zip(icons, [[-1.4, -2.0, 0.05], [3.2, 0.6, 0.05], [-2.9, 1.75, 0.05], [2.2, -0.52, 0.05], [0, 0.95, 0.05]]):
            icon[1].move_to(icon[0]); icon.move_to(pos)
        self.play(Create(center), FadeIn(dims), FadeIn(leaders), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(i, scale=1.25) for i in icons], lag_ratio=0.15), run_time=1.0)
        fully = VGroup(self.panel(2.7, 0.46, fill="#E7F5EE", stroke=GREEN, r=0.05), self.text("✓ FULLY CONSTRAINED", 15, GREEN, BOLD))
        fully[1].move_to(fully[0]); fully.move_to([2.35, 2.46, 0.06])
        self.play(FadeIn(fully), profile.animate.set_color(GREEN), holes.animate.set_color(GREEN), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(fully), profile.animate.set_color(SKETCH), holes.animate.set_color(SKETCH), run_time=0.5)
        return VGroup(center, dims, leaders, icons)

    def select_region(self):
        self.set_status("STEP 4 — SELECT THE CLOSED REGION", "Only watertight loops generate an extrusion preview", ORANGE)
        region = self.profile(0.005, ORANGE, ORANGE, 0.34, 4)
        masks = VGroup(*[Circle(radius=r * 0.97, fill_color=CANVAS, fill_opacity=1, stroke_color=ORANGE, stroke_width=2).move_to([x, y, 0.012]) for x, y, r in self.HOLES])
        self.play(FadeIn(region), FadeIn(masks), run_time=0.7)
        self.play(Indicate(region, color=ORANGE, scale_factor=1.025), run_time=0.8)
        return VGroup(region, masks)

    def extrusion_panel(self):
        card = self.panel(3.15, 3.55, fill="#F7F9FA").to_edge(RIGHT, buff=0.24).shift(DOWN * 0.05)
        title = self.text("EXTRUDE", 19, WHITE, BOLD)
        header = Rectangle(width=3.15, height=0.46, fill_color=NAVY, fill_opacity=1, stroke_width=0).align_to(card, UP)
        title.move_to(header)
        rows = VGroup(
            self.text("Profile: Sketch1", 15, GREEN, BOLD),
            self.text("Distance", 13, MUTED), self.text("20 mm", 22, INK, BOLD),
            self.text("Direction: One side (+Z)", 14, BLUE, BOLD),
            self.text("Operation: New solid", 14, GREEN, BOLD),
            self.text("OK", 16, WHITE, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(card).shift(DOWN * 0.18)
        ok = RoundedRectangle(width=1.1, height=0.42, corner_radius=0.05, fill_color=BLUE, fill_opacity=1, stroke_width=0).move_to(rows[-1])
        return VGroup(card, header, title, rows, ok, rows[-1].copy().move_to(ok))

    def extrude(self, profile, holes, annotations, selection, plane):
        self.set_step(2)
        self.set_status("STEP 5 — EXTRUDE ALONG +Z", "Distance = 20 mm; the profile becomes a three-dimensional body")
        self.play(FadeOut(annotations), plane.animate.set_opacity(0.30), run_time=0.7)
        dialog = self.extrusion_panel(); self.add_fixed_in_frame_mobjects(dialog); dialog.set_z_index(125)
        self.play(FadeIn(dialog, shift=LEFT * 0.2), run_time=0.7)
        arrow = Arrow3D([0, 0, 0.08], [0, 0, 2.25], color=ORANGE, thickness=0.035, height=0.22, base_radius=0.08)
        self.play(GrowArrow(arrow), run_time=0.7)
        self.move_camera(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.82, run_time=2.4)
        dynamic = always_redraw(lambda: self.solid(self.depth.get_value()))
        top_ghost = always_redraw(lambda: VGroup(self.profile(self.depth.get_value() + 0.01, ORANGE, ORANGE, 0.08, 2.4), self.hole_outlines(self.depth.get_value() + 0.015, ORANGE, 2)))
        self.add(dynamic, top_ghost)
        self.play(self.depth.animate.set_value(self.DEPTH), rate_func=smooth, run_time=4.0)
        self.play(FadeOut(arrow), FadeOut(top_ghost), FadeOut(profile), FadeOut(holes), FadeOut(selection), FadeOut(plane), run_time=0.8)
        self.remove(dynamic)
        solid = self.solid(self.DEPTH); self.add(solid)
        self.tree[4].set_opacity(1); self.set_step(3)
        self.set_status("RESULT — PARAMETRIC 3D SOLID", "Sketch1 remains editable and Extrusion1 rebuilds automatically", GREEN)
        self.play(FadeOut(dialog, shift=RIGHT * 0.2), run_time=0.6)
        self.begin_ambient_camera_rotation(rate=0.075); self.wait(2.5); self.stop_ambient_camera_rotation()
        return solid

    def explain_volume(self, solid):
        self.set_status("VOLUME = STACKED CROSS-SECTIONS", "Every section is the original profile translated along Z", CYAN)
        slices = VGroup(*[VGroup(self.profile(z, CYAN, CYAN, 0.025, 1.5), self.hole_outlines(z + 0.005, CYAN, 1)) for z in np.linspace(0.1, self.DEPTH - 0.1, 9)])
        self.play(solid.animate.set_opacity(0.28), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s) for s in slices], lag_ratio=0.09), run_time=1.8)
        formula = VGroup(self.panel(4.3, 1.0), self.text("V = A_profile × 20 mm", 22, BLUE, BOLD))
        formula[1].move_to(formula[0]); formula.to_corner(UR, buff=0.26).shift(DOWN * 2.3)
        self.add_fixed_in_frame_mobjects(formula); formula.set_z_index(130)
        self.play(FadeIn(formula)); self.move_camera(phi=74 * DEGREES, theta=-18 * DEGREES, zoom=0.90, run_time=2.0)
        self.move_camera(phi=61 * DEGREES, theta=-58 * DEGREES, zoom=0.84, run_time=2.0)
        self.play(FadeOut(slices), FadeOut(formula), solid.animate.set_opacity(1), run_time=1.0)

    def show_parametric_history(self, solid):
        self.set_status("PARAMETRIC FEATURE HISTORY", "Changing one parameter rebuilds the entire solid", PURPLE)
        card = self.panel(5.1, 1.35).to_corner(UR, buff=0.26).shift(DOWN * 2.2)
        flow = VGroup(self.text("Sketch1", 18, SKETCH, BOLD), Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=LINE), self.text("Extrusion1 = 20 mm", 18, GREEN, BOLD)).arrange(RIGHT, buff=0.18).move_to(card)
        self.add_fixed_in_frame_mobjects(card, flow); card.set_z_index(130); flow.set_z_index(131)
        self.play(FadeIn(card), FadeIn(flow), run_time=0.7)
        self.play(Transform(solid, self.solid(2.15)), run_time=1.2)
        self.play(Transform(solid, self.solid(1.05)), run_time=1.1)
        self.play(Transform(solid, self.solid(self.DEPTH)), run_time=1.2)
        self.play(FadeOut(card), FadeOut(flow), run_time=0.5)

    def surface_mesh(self):
        m = VGroup()
        for x in np.linspace(-2.8, 2.8, 10):
            yl = 1.92 if abs(x) < 2.65 else 1.52
            m.add(Line([x, -yl, self.DEPTH + 0.025], [x, yl, self.DEPTH + 0.025], color=MUTED, stroke_width=0.75))
        for y in np.linspace(-1.7, 1.7, 8):
            xl = 3.12 if abs(y) < 1.45 else 2.72
            m.add(Line([-xl, y, self.DEPTH + 0.026], [xl, y, self.DEPTH + 0.026], color=MUTED, stroke_width=0.75))
        for x, y in self.OUTER:
            m.add(Line3D([x, y, 0.01], [x, y, self.DEPTH + 0.01], color=MUTED, thickness=0.008))
        return m

    def show_cfd_handoff(self, solid):
        self.set_step(4)
        self.set_status("CAD → CFD HANDOFF", "A watertight volume can be embedded in a fluid domain and meshed", CYAN)
        domain = Cube(side_length=1, fill_color=CYAN, fill_opacity=0.04, stroke_color=CYAN, stroke_width=1)
        domain.stretch_to_fit_width(9); domain.stretch_to_fit_height(6); domain.stretch_to_fit_depth(4.2); domain.move_to([0, 0, 0.9]); domain.set_shade_in_3d(True)
        arrows = VGroup(*[Arrow3D([-4.2, y, z], [-3.25, y, z], color=CYAN, thickness=0.016, height=0.13, base_radius=0.045) for y in np.linspace(-2, 2, 6) for z in [0.35, 0.95, 1.55]])
        mesh = self.surface_mesh()
        self.play(FadeIn(domain), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.025), run_time=1.5)
        self.play(Create(mesh), solid.animate.set_opacity(0.78), run_time=1.3)
        pipe = VGroup(*[self.text(t, 15, c, BOLD) for t, c in [("CAD SOLID", BLUE), ("→", MUTED), ("FLUID DOMAIN", CYAN), ("→", MUTED), ("MESH", PURPLE), ("→", MUTED), ("CFD SOLVER", GREEN)]]).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.95).shift(RIGHT * 1.2)
        bg = BackgroundRectangle(pipe, fill_color=WHITE, fill_opacity=0.95, buff=0.15, stroke_color=LINE, stroke_width=1)
        pipeline = VGroup(bg, pipe); self.add_fixed_in_frame_mobjects(pipeline); pipeline.set_z_index(135)
        self.play(FadeIn(pipeline)); self.begin_ambient_camera_rotation(rate=0.055); self.wait(2.8); self.stop_ambient_camera_rotation()
        self.play(FadeOut(domain), FadeOut(arrows), FadeOut(mesh), FadeOut(pipeline), solid.animate.set_opacity(1), run_time=0.9)

    def finish(self, solid):
        self.set_status("WORKFLOW COMPLETE", "A constrained 2D definition is now an editable 3D engineering volume", GREEN)
        self.move_camera(phi=63 * DEGREES, theta=-42 * DEGREES, zoom=0.87, run_time=1.6)
        card = self.panel(9.1, 1.8, r=0.14).move_to([1.3, 0, 0])
        title = self.text("2D SKETCH  →  CONSTRAINTS  →  EXTRUSION  →  3D VOLUME", 29, NAVY, BOLD)
        sub = self.text("Professional parametric geometry prepared for engineering analysis", 19, MUTED)
        content = VGroup(title, sub).arrange(DOWN, buff=0.22).move_to(card)
        self.add_fixed_in_frame_mobjects(card, content); card.set_z_index(140); content.set_z_index(141)
        self.play(FadeIn(card), Write(title), FadeIn(sub), run_time=1.1)
        self.begin_ambient_camera_rotation(rate=0.04); self.wait(3.2); self.stop_ambient_camera_rotation()
        self.play(FadeOut(card), FadeOut(content), FadeOut(solid), run_time=0.9)


class InventorExtrusionSmokeTest(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.9)
        cube = Cube(side_length=2, fill_color=TOP, fill_opacity=1, stroke_color=NAVY)
        cube.stretch_to_fit_width(5); cube.stretch_to_fit_height(3); cube.stretch_to_fit_depth(1.3)
        cube.set_shade_in_3d(True)
        self.play(FadeIn(cube), run_time=0.7)
        self.begin_ambient_camera_rotation(rate=0.12); self.wait(1.4); self.stop_ambient_camera_rotation()
