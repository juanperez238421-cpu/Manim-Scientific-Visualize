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
    WHITE_FILL,
    BOLD,
    NORMAL,
    READ,
    EXPLAIN,
    RUN,
    RUN_SLOW,
)


class InventorMirrorSimetriaSenior(JPMiscCADScene):
    """Full Autodesk Inventor Mirror / Simetría lesson.

    Design contract
    ---------------
    - 1920x1080, 30 fps, white classroom background.
    - Large black typography and neutral-gray CAD solids.
    - Explicit 2D sketch -> 3D feature -> mirror plane -> preview -> result flow.
    - No guessed placement: the YZ origin plane is the exact geometric reference.
    - Includes validation, feature tree, and a parametric edit proving that both
      sides update from one seed feature.
    """

    OPERATION = "Mirror / Simetría"
    BASE_W = 6.8
    BASE_D = 3.9
    BASE_H = 0.58
    BOSS_R = 0.50
    BOSS_R_EDIT = 0.70
    BOSS_H = 0.82
    OFFSET = 1.72

    def safe_fixed(self, *mobs):
        for mob in mobs:
            if mob.get_left()[0] < -7.82 or mob.get_right()[0] > 7.82:
                raise ValueError("Horizontal safe-area violation")
            if mob.get_bottom()[1] < -4.36 or mob.get_top()[1] > 4.36:
                raise ValueError("Vertical safe-area violation")
        self.fixed(*mobs)

    def feature_tree(self):
        lines = VGroup(
            self.text("Part1.ipt", 23, BOLD),
            self.text("Origin", 21, NORMAL, MID_GRAY),
            self.text("  YZ Plane", 21, BOLD),
            self.text("Sketch1", 21, NORMAL, MID_GRAY),
            self.text("Extrusion1   10 mm", 21),
            self.text("Sketch2", 21, NORMAL, MID_GRAY),
            self.text("Boss1   Ø16 mm", 21),
            self.text("Mirror1   Boss1 / YZ Plane", 21, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        panel = RoundedRectangle(
            width=4.85,
            height=lines.height + 0.62,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=1.35,
            fill_color=WHITE,
            fill_opacity=0.99,
        )
        lines.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.28)
        group = VGroup(panel, lines).move_to([-5.15, -0.35, 0])
        self.safe_fixed(group)
        return group

    def mirror_parameter_card(self):
        rows = [
            ("Features", "Boss1"),
            ("Mirror Plane", "YZ Plane"),
            ("Operation", "Join"),
            ("Preview", "Enabled"),
        ]
        card = self.parameter_card("MIRROR PARAMETERS", rows)
        if card.get_right()[0] > 7.78:
            raise ValueError("Mirror parameter card safe-area failure")
        return card

    def validation_card(self, title, lines, center):
        head = self.text(title, 27, BOLD)
        body = VGroup(*[self.text(line, 20 if i else 21, BOLD if i == 0 else NORMAL)
                        for i, line in enumerate(lines)])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if content.width > 4.25:
            content.scale_to_fit_width(4.25)
        panel = RoundedRectangle(
            width=4.75,
            height=max(1.65, content.height + 0.52),
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=1.35,
            fill_color=WHITE,
            fill_opacity=0.99,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.25)
        group = VGroup(panel, content).move_to(center)
        self.safe_fixed(group)
        return group

    def base(self):
        return cuboid(self.BASE_W, self.BASE_D, self.BASE_H, 0.62, GRAY_C)

    def boss(self, x, radius=None, opacity=0.68):
        radius = self.BOSS_R if radius is None else radius
        return cylinder(radius, self.BOSS_H, opacity, GRAY_B).shift(
            RIGHT * x + OUT * (self.BASE_H / 2 + self.BOSS_H / 2)
        )

    def opening_scene(self):
        self.opening(
            "SIMETRÍA  •  MIRROR",
            "Crear una copia paramétrica exacta de una operación respecto a un plano estable.",
            ["SEED FEATURE", "MIRROR PLANE", "PREVIEW", "MIRROR1"],
        )

    def concept(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        h = self.section_header(
            1,
            "THE MIRROR PLANE IS THE GEOMETRIC REFERENCE",
            "The copied feature stays at the same perpendicular distance on the opposite side of the selected plane.",
        )
        plane = DashedLine(UP * 2.45, DOWN * 2.45, color=BLACK, stroke_width=3, dash_length=0.14)
        source = Dot(LEFT * 3.0 + UP * 0.50, radius=0.11, color=BLACK)
        target = Dot(RIGHT * 3.0 + UP * 0.50, radius=0.11, color=BLACK)
        a1 = DoubleArrow(LEFT * 3.0 + DOWN * 0.05, DOWN * 0.05, buff=0, color=BLACK, stroke_width=2.2)
        a2 = DoubleArrow(DOWN * 0.05, RIGHT * 3.0 + DOWN * 0.05, buff=0, color=BLACK, stroke_width=2.2)
        labels = VGroup(
            self.text("SOURCE", 24, BOLD).next_to(source, UP, buff=0.14),
            self.text("MIRROR", 24, BOLD).next_to(target, UP, buff=0.14),
            self.text("d", 23, BOLD).next_to(a1, DOWN, buff=0.10),
            self.text("d", 23, BOLD).next_to(a2, DOWN, buff=0.10),
        )
        self.safe_fixed(labels)
        self.play(Create(plane), FadeIn(source), Create(a1), run_time=1.10)
        self.play(TransformFromCopy(source, target), Create(a2), FadeIn(labels), run_time=1.45)
        note = self.note(
            "CORE IDEA",
            [
                "One seed feature is modeled once.",
                "The work plane controls orientation and distance.",
                "No manual second sketch is required.",
            ],
            width=5.9,
        ).to_corner(DR, buff=0.48).shift(UP * 0.48)
        self.safe_fixed(note)
        self.play(FadeIn(note), run_time=0.75)
        self.wait(EXPLAIN)
        self.clear_scene()

    def build_base(self):
        return self.base_plate_from_sketch(
            2,
            width=self.BASE_W,
            depth=self.BASE_D,
            height=self.BASE_H,
            dims="110 × 62 mm",
            extrude="10 mm",
        )

    def seed_feature(self, old_body):
        self.play(FadeOut(old_body), run_time=0.40)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        h = self.section_header(
            3,
            "MODEL ONE SEED FEATURE ON THE LEFT SIDE",
            "Sketch2 defines one circular boss. Its center is dimensioned from the symmetry plane, not from an arbitrary point.",
        )
        plate = Rectangle(width=self.BASE_W, height=self.BASE_D, color=BLACK, stroke_width=3.2)
        plane = DashedLine(UP * self.BASE_D / 2, DOWN * self.BASE_D / 2,
                           color=MID_GRAY, stroke_width=2.2, dash_length=0.12)
        circle = Circle(radius=self.BOSS_R, color=BLACK, stroke_width=4.2).move_to(LEFT * self.OFFSET)
        center = Dot(circle.get_center(), radius=0.075, color=BLACK)
        dim = DoubleArrow(ORIGIN + DOWN * 1.35, LEFT * self.OFFSET + DOWN * 1.35,
                          buff=0, color=BLACK, stroke_width=2.0)
        lab1 = self.text("Ø16 mm", 25, BOLD).next_to(circle, UP, buff=0.12)
        lab2 = self.text("28 mm", 24, BOLD).next_to(dim, DOWN, buff=0.08)
        labels = VGroup(lab1, lab2)
        self.safe_fixed(labels)
        self.play(FadeIn(plate), Create(plane), run_time=0.85)
        self.play(Create(circle), FadeIn(center), Create(dim), FadeIn(labels), run_time=1.15)
        self.wait(READ)

        row = self.process_row(["TOP FACE", "SKETCH2", "Ø16", "EXTRUDE BOSS1"])
        self.play(LaggedStart(*[FadeIn(p) for p in row[0]], lag_ratio=0.10), Create(row[1]), run_time=1.30)
        self.wait(READ)

        self.play(FadeOut(labels), FadeOut(row), run_time=0.35)
        self.move_camera(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.90, run_time=1.10)
        base = self.base()
        seed = self.boss(-self.OFFSET)
        self.play(FadeOut(plate), FadeOut(plane), FadeOut(circle), FadeOut(center), FadeOut(dim),
                  FadeIn(base), run_time=0.70)
        self.play(FadeIn(seed, shift=OUT * 0.10), run_time=0.90)
        label = self.text("Boss1 = SEED FEATURE", 25, BOLD).to_edge(DOWN, buff=0.34)
        self.safe_fixed(label)
        self.play(FadeIn(label), run_time=0.55)
        self.wait(EXPLAIN)
        self.play(FadeOut(label), FadeOut(h), run_time=0.40)
        return base, seed

    def select_plane_and_preview(self, base, seed):
        h = self.section_header(
            4,
            "SELECT BOSS1 + THE ORIGIN YZ PLANE",
            "The Mirror command needs two things: what to reproduce and the plane that defines the reflection.",
        )
        plane3 = Rectangle(
            width=4.25,
            height=3.15,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.22,
        ).rotate(PI / 2, axis=UP).move_to([0, 0, 0.60])
        card = self.mirror_parameter_card()
        self.play(FadeIn(plane3), run_time=0.65)
        self.play(FadeIn(card), run_time=0.75)
        self.wait(READ)

        ghost = seed.copy().set_opacity(0.24)
        self.add(ghost)
        self.play(ghost.animate.shift(RIGHT * (2 * self.OFFSET)), run_time=2.15, rate_func=smooth)
        mirror = self.boss(self.OFFSET, opacity=0.72)
        self.play(ReplacementTransform(ghost, mirror), run_time=0.85)
        self.wait(READ)

        note = self.note(
            "PREVIEW CHECK",
            [
                "Boss1 remains the source.",
                "The YZ plane stays centered.",
                "The reflected boss appears at equal distance.",
            ],
            width=5.95,
        ).to_corner(DL, buff=0.48).shift(UP * 0.55)
        self.safe_fixed(note)
        self.play(FadeIn(note), run_time=0.75)
        self.wait(EXPLAIN)
        self.play(FadeOut(note), FadeOut(card), FadeOut(plane3), FadeOut(h), run_time=0.45)
        return mirror

    def exact_distance_check(self, base, seed, mirror):
        self.play(FadeOut(base), FadeOut(seed), FadeOut(mirror), run_time=0.40)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        h = self.section_header(
            5,
            "VERIFY EQUAL DISTANCE IN TOP VIEW",
            "A correct mirror is defined by the plane: 28 mm to Boss1 becomes 28 mm to the mirrored boss.",
        )
        plate = Rectangle(width=self.BASE_W, height=self.BASE_D, color=BLACK, stroke_width=3.0)
        axis = DashedLine(UP * self.BASE_D / 2, DOWN * self.BASE_D / 2,
                          color=BLACK, stroke_width=2.0, dash_length=0.12)
        c1 = Circle(radius=self.BOSS_R, color=BLACK, stroke_width=4).move_to(LEFT * self.OFFSET)
        c2 = Circle(radius=self.BOSS_R, color=BLACK, stroke_width=4).move_to(RIGHT * self.OFFSET)
        d1 = DoubleArrow(LEFT * self.OFFSET + DOWN * 1.45, DOWN * 1.45,
                         buff=0, color=BLACK, stroke_width=2.0)
        d2 = DoubleArrow(DOWN * 1.45, RIGHT * self.OFFSET + DOWN * 1.45,
                         buff=0, color=BLACK, stroke_width=2.0)
        labels = VGroup(
            self.text("28 mm", 24, BOLD).next_to(d1, DOWN, buff=0.08),
            self.text("28 mm", 24, BOLD).next_to(d2, DOWN, buff=0.08),
            self.text("YZ PLANE", 23, BOLD).next_to(axis, UP, buff=0.10),
        )
        self.safe_fixed(labels)
        self.play(FadeIn(plate), Create(axis), Create(c1), run_time=0.80)
        self.play(TransformFromCopy(c1, c2), Create(d1), Create(d2), FadeIn(labels), run_time=1.25)
        self.wait(EXPLAIN)
        self.clear_scene()

    def validation(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        h = self.section_header(
            6,
            "VALIDATE THE REFERENCE BEFORE PRESSING OK",
            "A stable work plane makes the feature robust; a fragile face reference can fail when upstream geometry changes.",
        )
        good = self.validation_card(
            "ROBUST",
            ["Origin YZ Plane", "stable reference", "recommended"],
            [-3.05, -0.35, 0],
        )
        bad = self.validation_card(
            "FRAGILE",
            ["temporary face", "may disappear after edits", "avoid when possible"],
            [3.05, -0.35, 0],
        )
        self.play(FadeIn(good), run_time=0.80)
        self.wait(READ)
        self.play(FadeIn(bad), run_time=0.80)
        self.wait(EXPLAIN)
        self.clear_scene()

    def parametric_edit(self):
        self.move_camera(phi=64 * DEGREES, theta=-48 * DEGREES, zoom=0.88, run_time=0.80)
        h = self.section_header(
            7,
            "EDIT THE SEED — BOTH SIDES UPDATE",
            "Mirror1 depends on Boss1, so changing the seed diameter updates the reflected feature without rebuilding it.",
        )
        base = self.base().shift(RIGHT * 1.0)
        seed = self.boss(-self.OFFSET).shift(RIGHT * 1.0)
        mirror = self.boss(self.OFFSET).shift(RIGHT * 1.0)
        self.play(FadeIn(base), FadeIn(seed), FadeIn(mirror), run_time=0.90)

        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.65)
        edit = self.pill("EDIT BOSS1: Ø16 mm  →  Ø22 mm", width=5.35, size=22).move_to([1.0, -3.15, 0])
        self.safe_fixed(edit)
        self.play(FadeIn(edit), run_time=0.60)
        self.wait(READ)

        seed_big = self.boss(-self.OFFSET, self.BOSS_R_EDIT).shift(RIGHT * 1.0)
        mirror_big = self.boss(self.OFFSET, self.BOSS_R_EDIT).shift(RIGHT * 1.0)
        self.play(
            Transform(seed, seed_big),
            Transform(mirror, mirror_big),
            run_time=1.80,
            rate_func=smooth,
        )
        self.wait(EXPLAIN)
        self.play(FadeOut(edit), FadeOut(tree), FadeOut(h), run_time=0.45)

        tag = self.text("ONE EDIT  →  TWO SYNCHRONIZED FEATURES", 28, BOLD).to_edge(DOWN, buff=0.28)
        self.safe_fixed(tag)
        self.play(FadeIn(tag), run_time=0.70)
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(3.2)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)

    def construct(self):
        self.opening_scene()
        self.concept()
        body = self.build_base()
        base, seed = self.seed_feature(body)
        mirror = self.select_plane_and_preview(base, seed)
        self.exact_distance_check(base, seed, mirror)
        self.validation()
        self.parametric_edit()
