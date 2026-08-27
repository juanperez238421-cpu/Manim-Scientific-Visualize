#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Metro, relative motion and the invariance of light speed.

Mixed 2D/3D ManimCE lesson built for a slow classroom explanation.
The numerical correction is intentional: the speed of light is approximately
300,000 km/s, not 300,000 km/h.

Final render target:
    manim -pqh metro_relativity_lesson.py Physics9MetroRelativity \
        --format=mp4 --disable_caching
"""
from __future__ import annotations

import os
from math import isclose

from manim import *


# -----------------------------------------------------------------------------
# Exact classroom render contract
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#7A7A7A"
LIGHT_GRAY = "#D7D7D7"
PAPER_GRAY = "#F5F5F5"
LIGHT_COLOR = "#D6A000"  # only used for the light pulse

RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.50
RUN_CAMERA = 1.40
PAUSE_SHORT = 0.85
PAUSE_READ = 1.70
PAUSE_EXPLAIN = 2.70
PAUSE_WORK = 3.60
PAUSE_FINAL = 5.00


class Physics9MetroRelativity(ThreeDScene):
    """Galilean relative velocity first, then the special-relativity contrast."""

    TRAIN_KMH = 80.0
    WALK_KMH = 2.0
    GROUND_WALK_KMH = 82.0

    # Physics correction: c ≈ 300000 km/s, not km/h.
    C_APPROX_KM_S = 300000.0
    C_EXACT_KM_S = 299792.458
    C_EXACT_KM_H = 1079252848.8

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE
        self.fixed_items: list[Mobject] = []
        self.header: Mobject | None = None
        self.validate_lesson_data()

    def validate_lesson_data(self) -> None:
        assert isclose(self.TRAIN_KMH + self.WALK_KMH, self.GROUND_WALK_KMH)
        assert isclose(self.C_EXACT_KM_S * 3600.0, self.C_EXACT_KM_H, rel_tol=0, abs_tol=1e-6)
        # Velocity-addition law: if u' = c, every inertial observer also obtains c.
        u_prime = self.C_EXACT_KM_H
        v = self.TRAIN_KMH
        u = (u_prime + v) / (1.0 + (u_prime * v) / (self.C_EXACT_KM_H**2))
        assert isclose(u, self.C_EXACT_KM_H, rel_tol=0, abs_tol=1e-6)

    # ------------------------------------------------------------------
    # Timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography and fixed-frame overlays
    # ------------------------------------------------------------------
    def text(self, content: str, size: int = 30, weight=NORMAL) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight)

    def math(self, expression: str, size: int = 38) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT)

    def fit(self, mob: Mobject, max_width: float, max_height: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def show_fixed(self, mob: Mobject, run_time=RUN_NORMAL) -> None:
        mob.set_opacity(0)
        self.add_fixed_in_frame_mobjects(mob)
        self.fixed_items.append(mob)
        self.play(mob.animate.set_opacity(1), run_time=run_time)

    def remove_fixed(self, mob: Mobject, run_time=RUN_QUICK) -> None:
        if mob not in self.fixed_items:
            return
        self.play(mob.animate.set_opacity(0), run_time=run_time)
        self.remove_fixed_in_frame_mobjects(mob)
        self.remove(mob)
        self.fixed_items.remove(mob)

    def clear_content(self, keep_header=True) -> None:
        fixed_keep = {self.header} if keep_header and self.header is not None else set()
        for mob in list(self.fixed_items):
            if mob not in fixed_keep:
                self.remove_fixed(mob, run_time=RUN_QUICK)
        world = [mob for mob in list(self.mobjects) if mob not in self.fixed_items]
        if world:
            self.play(*[FadeOut(mob) for mob in world], run_time=RUN_NORMAL)

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        if self.header is not None:
            self.remove_fixed(self.header, run_time=RUN_QUICK)
        number_box = RoundedRectangle(
            width=0.72, height=0.52, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)
        title_text = self.text(title, 33, BOLD)
        self.fit(title_text, 13.5, 0.62)
        top = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        top.to_edge(UP, buff=0.18).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(top, DOWN, buff=0.07)
        subtitle_text = self.text(subtitle, 20)
        self.fit(subtitle_text, 14.3, 0.50)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(top, LEFT)
        self.header = VGroup(top, rule, subtitle_text)
        self.show_fixed(self.header, run_time=RUN_QUICK)

    def note_panel(self, title: str, lines: list[str], width=5.5, body_size=23) -> VGroup:
        title_m = self.text(title, 26, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12
        )
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.55, 3.8)
        box = RoundedRectangle(
            width=width, height=content.height + 0.58, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=0.97,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def formula_panel(self, expression: str, width=6.0, height=1.05, size=38) -> VGroup:
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=1.9,
            fill_color=PAPER_GRAY, fill_opacity=0.98,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.40, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    # ------------------------------------------------------------------
    # 3D visual models
    # ------------------------------------------------------------------
    def make_train_3d(self) -> VGroup:
        shell = Prism(dimensions=[7.2, 2.35, 1.85])
        shell.set_fill(WHITE, opacity=0.14)
        shell.set_stroke(BLACK_LINE, width=1.4, opacity=0.80)
        shell.shift(OUT * 0.05)

        floor = Prism(dimensions=[7.35, 2.45, 0.12])
        floor.set_fill(PAPER_GRAY, opacity=0.95)
        floor.set_stroke(BLACK_LINE, width=1.2)
        floor.shift(IN * 0.87)

        roof = Prism(dimensions=[7.20, 2.30, 0.10])
        roof.set_fill(PAPER_GRAY, opacity=0.88)
        roof.set_stroke(BLACK_LINE, width=1.1)
        roof.shift(OUT * 0.98)

        wheels = VGroup()
        for x in (-2.35, 2.35):
            for y in (-1.16, 1.16):
                wheel = Cylinder(radius=0.32, height=0.24, direction=Y_AXIS, resolution=12)
                wheel.set_fill(DARK_GRAY, opacity=0.90)
                wheel.set_stroke(BLACK_LINE, width=0.8)
                wheel.move_to([x, y, -1.02])
                wheels.add(wheel)

        seats = VGroup()
        for x in (-1.9, -0.4, 1.1):
            seat = Prism(dimensions=[0.78, 0.72, 0.52])
            seat.set_fill(LIGHT_GRAY, opacity=0.72)
            seat.set_stroke(BLACK_LINE, width=0.8)
            seat.move_to([x, 0.45, -0.56])
            seats.add(seat)
        return VGroup(shell, floor, roof, wheels, seats)

    def make_person_3d(self, position=ORIGIN, scale=1.0, walker=False) -> VGroup:
        head = Sphere(radius=0.18 * scale, resolution=(10, 18))
        head.set_fill(WHITE, opacity=1)
        head.set_stroke(BLACK_LINE, width=1.0)
        torso = Cylinder(radius=0.12 * scale, height=0.62 * scale, direction=Z_AXIS, resolution=12)
        torso.set_fill(PAPER_GRAY if not walker else LIGHT_GRAY, opacity=1)
        torso.set_stroke(BLACK_LINE, width=0.9)
        head.move_to([0, 0, 0.28 * scale])
        torso.move_to([0, 0, -0.12 * scale])
        leg1 = Line([0, 0, -0.43 * scale], [-0.13 * scale, 0, -0.72 * scale], color=BLACK_LINE, stroke_width=4)
        leg2 = Line([0, 0, -0.43 * scale], [0.13 * scale, 0, -0.72 * scale], color=BLACK_LINE, stroke_width=4)
        person = VGroup(head, torso, leg1, leg2).move_to(position)
        return person

    def make_lamp_3d(self, position=ORIGIN) -> VGroup:
        bulb = Sphere(radius=0.12, resolution=(10, 18))
        bulb.set_fill(LIGHT_COLOR, opacity=0.90)
        bulb.set_stroke(BLACK_LINE, width=0.8)
        handle = Cylinder(radius=0.055, height=0.28, direction=Z_AXIS, resolution=10)
        handle.set_fill(DARK_GRAY, opacity=0.95)
        handle.shift(IN * 0.18)
        lamp = VGroup(bulb, handle).move_to(position)
        return lamp

    def platform_3d(self) -> VGroup:
        rails = VGroup(
            Line([-7, -1.65, -1.25], [7, -1.65, -1.25], color=DARK_GRAY, stroke_width=4),
            Line([-7, 1.65, -1.25], [7, 1.65, -1.25], color=DARK_GRAY, stroke_width=4),
        )
        sleepers = VGroup(*[
            Line([x, -1.95, -1.28], [x, 1.95, -1.28], color=MID_GRAY, stroke_width=2)
            for x in range(-6, 7)
        ])
        return VGroup(rails, sleepers)

    def light_pulse(self, center) -> Sphere:
        pulse = Sphere(radius=0.25, resolution=(12, 24))
        pulse.set_fill(LIGHT_COLOR, opacity=0.06)
        pulse.set_stroke(LIGHT_COLOR, width=1.2, opacity=0.62)
        pulse.move_to(center)
        return pulse

    # ------------------------------------------------------------------
    # 2D visual models
    # ------------------------------------------------------------------
    def train_2d(self, center=ORIGIN, width=8.0) -> VGroup:
        car = RoundedRectangle(
            width=width, height=2.65, corner_radius=0.18,
            stroke_color=BLACK_LINE, stroke_width=2.4,
            fill_color=WHITE, fill_opacity=1,
        )
        doors = VGroup(
            Line([-0.48, -1.30, 0], [-0.48, 1.30, 0], color=LIGHT_GRAY),
            Line([0.48, -1.30, 0], [0.48, 1.30, 0], color=LIGHT_GRAY),
        )
        windows = VGroup(*[
            RoundedRectangle(width=1.35, height=0.72, corner_radius=0.08,
                             stroke_color=MID_GRAY, fill_color=PAPER_GRAY, fill_opacity=1)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.28).shift(UP * 0.48)
        group = VGroup(car, doors, windows).move_to(center)
        return group

    def walker_2d(self, center=ORIGIN) -> VGroup:
        head = Circle(radius=0.16, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1)
        body = Line(DOWN * 0.08, DOWN * 0.70, color=BLACK_LINE, stroke_width=4)
        arm1 = Line(DOWN * 0.30, DOWN * 0.45 + LEFT * 0.28, color=BLACK_LINE, stroke_width=3)
        arm2 = Line(DOWN * 0.30, DOWN * 0.45 + RIGHT * 0.28, color=BLACK_LINE, stroke_width=3)
        leg1 = Line(DOWN * 0.70, DOWN * 1.02 + LEFT * 0.25, color=BLACK_LINE, stroke_width=3)
        leg2 = Line(DOWN * 0.70, DOWN * 1.02 + RIGHT * 0.25, color=BLACK_LINE, stroke_width=3)
        return VGroup(head, body, arm1, arm2, leg1, leg2).move_to(center)

    def velocity_arrow(self, start, end, label: str) -> VGroup:
        arrow = Arrow(start, end, buff=0, color=BLACK_LINE, stroke_width=4, max_tip_length_to_length_ratio=0.14)
        lab = self.math(label, 28).next_to(arrow, UP, buff=0.10)
        return VGroup(arrow, lab)

    # ------------------------------------------------------------------
    # Lesson sequence
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening()
        self.frames_of_reference()
        self.walker_train_frame()
        self.walker_ground_frame()
        self.compare_classical_frames()
        self.light_unit_correction()
        self.light_inside_train_3d()
        self.light_ground_frame_3d()
        self.lorentz_velocity_addition()
        self.final_summary()

    def opening(self) -> None:
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=0.86)
        tracks = self.platform_3d()
        train = self.make_train_3d().shift(LEFT * 3.4)
        self.play(Create(tracks), FadeIn(train), run_time=RUN_SLOW)

        title = VGroup(
            self.text("PHYSICS 9 • RELATIVITY EXAMPLE", 25, BOLD),
            self.text("METRO, WALKER AND LIGHT", 46, BOLD),
            self.text("What changes when the observer changes?", 27),
        ).arrange(DOWN, buff=0.20).to_edge(UP, buff=0.45)
        self.show_fixed(title, run_time=RUN_SLOW)
        self.play(train.animate.shift(RIGHT * 6.8), run_time=4.2, rate_func=linear)
        prompt = self.text("South is our +x direction. The drawings are not to scale.", 22)
        prompt.to_edge(DOWN, buff=0.40)
        self.show_fixed(prompt, run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_content(keep_header=False)
        self.header = None

    def frames_of_reference(self) -> None:
        self.set_header(
            1,
            "FIRST IDEA: A VELOCITY NEEDS AN OBSERVER",
            "The same motion can have different numerical velocities when measured from different reference frames.",
        )
        self.move_camera(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.84, run_time=RUN_CAMERA)
        tracks = self.platform_3d()
        train = self.make_train_3d().move_to(ORIGIN)
        student = self.make_person_3d([0.0, 0.42, -0.08], scale=0.92)
        observer = self.make_person_3d([3.6, -3.15, -0.30], scale=1.05)
        self.play(Create(tracks), FadeIn(train), FadeIn(student), FadeIn(observer), run_time=RUN_SLOW)

        left = self.note_panel("FRAME S' — INSIDE THE METRO", ["You are seated.", "The metro is at rest relative to you.", "You measure motions inside the car."], width=5.5)
        left.move_to(LEFT * 4.6 + DOWN * 2.55)
        right = self.note_panel("FRAME S — STATION / GROUND", ["Observer stands outside.", "Metro moves south at 80 km/h.", "Ground is taken as rest."], width=5.5)
        right.move_to(RIGHT * 4.6 + DOWN * 2.55)
        self.show_fixed(left, run_time=RUN_NORMAL)
        self.show_fixed(right, run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def walker_train_frame(self) -> None:
        self.set_header(
            2,
            "CASE 1 — PERSON WALKS INSIDE THE METRO",
            "First measure the walker from the seat beside them: the train itself is the reference frame.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        car = self.train_2d(center=LEFT * 2.6, width=9.0)
        walker = self.walker_2d(center=LEFT * 5.2 + DOWN * 0.25)
        seat = VGroup(
            Rectangle(width=0.85, height=0.70, color=MID_GRAY, fill_color=PAPER_GRAY, fill_opacity=1),
            self.text("YOU", 19, BOLD).shift(DOWN * 0.02),
        ).move_to(LEFT * 3.3 + DOWN * 0.42)
        direction = self.velocity_arrow(LEFT * 5.3 + DOWN * 1.75, LEFT * 0.3 + DOWN * 1.75, r"+x\;(\mathrm{South})")
        self.play(FadeIn(car), FadeIn(walker), FadeIn(seat), GrowArrow(direction[0]), Write(direction[1]), run_time=RUN_SLOW)

        panel = VGroup(
            self.formula_panel(r"v_{\mathrm{walker/train}}=2\;\mathrm{km/h}", width=5.3, size=34),
            self.note_panel("WHAT YOU SEE FROM THE SEAT", ["The metro walls do not move relative to you.", "The person advances at 2 km/h.", "So the measured relative velocity is 2 km/h."], width=5.3),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 4.45 + DOWN * 0.35)
        self.show_fixed(panel, run_time=RUN_NORMAL)
        self.play(walker.animate.shift(RIGHT * 3.2), run_time=3.6, rate_func=linear)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def walker_ground_frame(self) -> None:
        self.set_header(
            3,
            "CASE 2 — THE SAME WALKER SEEN FROM OUTSIDE",
            "At ordinary speeds, Galilean velocity addition works extremely well: combine the train speed with the walking speed.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        platform = Line(LEFT * 7 + DOWN * 1.7, RIGHT * 7 + DOWN * 1.7, color=DARK_GRAY, stroke_width=4)
        observer = self.walker_2d(center=RIGHT * 5.8 + DOWN * 0.45).scale(0.82)
        car = self.train_2d(center=LEFT * 4.7, width=7.6)
        walker = self.walker_2d(center=LEFT * 5.65 + DOWN * 0.20).scale(0.85)
        moving = VGroup(car, walker)
        self.play(Create(platform), FadeIn(observer), FadeIn(moving), run_time=RUN_SLOW)

        eqs = VGroup(
            self.formula_panel(r"v_{\mathrm{walker/ground}}=v_{\mathrm{train/ground}}+v_{\mathrm{walker/train}}", width=7.0, size=30),
            self.formula_panel(r"v_{\mathrm{walker/ground}}=80+2=82\;\mathrm{km/h}", width=7.0, size=35),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.75 + UP * 1.35)
        self.show_fixed(eqs, run_time=RUN_NORMAL)
        train_arrow = self.velocity_arrow(LEFT * 6.4 + DOWN * 2.50, LEFT * 1.0 + DOWN * 2.50, r"80\;\mathrm{km/h}")
        self.play(GrowArrow(train_arrow[0]), Write(train_arrow[1]), run_time=RUN_NORMAL)
        # 6.0 world units for 80 km/h; the extra 0.15 reflects the 2/80 ratio.
        self.play(car.animate.shift(RIGHT * 6.0), walker.animate.shift(RIGHT * 6.15), run_time=4.2, rate_func=linear)
        result = self.text("OUTSIDE OBSERVER: 82 km/h", 30, BOLD).move_to(RIGHT * 4.1 + DOWN * 2.45)
        self.show_fixed(result, run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def compare_classical_frames(self) -> None:
        self.set_header(
            4,
            "PAUSE: SAME PERSON, TWO CORRECT ANSWERS",
            "2 km/h and 82 km/h are not contradictory because they refer to different reference frames.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        divider = Line(UP * 2.35, DOWN * 3.60, color=LIGHT_GRAY, stroke_width=2)
        left_title = self.text("INSIDE THE METRO", 28, BOLD).move_to(LEFT * 4 + UP * 1.85)
        right_title = self.text("OUTSIDE / GROUND", 28, BOLD).move_to(RIGHT * 4 + UP * 1.85)
        left_car = self.train_2d(LEFT * 4 + DOWN * 0.2, width=6.2).scale(0.78)
        left_person = self.walker_2d(LEFT * 5.3 + DOWN * 0.35).scale(0.70)
        right_car = self.train_2d(RIGHT * 3.4 + DOWN * 0.2, width=5.6).scale(0.72)
        right_person = self.walker_2d(RIGHT * 2.4 + DOWN * 0.35).scale(0.64)
        self.play(Create(divider), Write(left_title), Write(right_title), FadeIn(left_car), FadeIn(left_person), FadeIn(right_car), FadeIn(right_person), run_time=RUN_SLOW)
        left_result = self.formula_panel(r"v'=2\;\mathrm{km/h}", width=4.2, size=40).move_to(LEFT * 4 + DOWN * 2.15)
        right_result = self.formula_panel(r"v=82\;\mathrm{km/h}", width=4.2, size=40).move_to(RIGHT * 4 + DOWN * 2.15)
        self.play(FadeIn(left_result), FadeIn(right_result), run_time=RUN_NORMAL)
        self.play(left_person.animate.shift(RIGHT * 1.6), right_car.animate.shift(RIGHT * 0.65), right_person.animate.shift(RIGHT * 0.72), run_time=3.4, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        bridge = self.text("For matter at everyday speeds: velocity depends on the observer.", 28, BOLD).to_edge(DOWN, buff=0.28)
        self.play(Write(bridge), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def light_unit_correction(self) -> None:
        self.set_header(
            5,
            "NOW TURN ON A LAMP: CHECK THE UNIT FIRST",
            "The speed of light is about 300,000 kilometres per SECOND. This unit correction matters before discussing relativity.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        wrong = VGroup(
            self.text("NOT THE SPEED OF LIGHT", 23, BOLD),
            self.math(r"300\,000\;\mathrm{km/h}", 42),
        ).arrange(DOWN, buff=0.18)
        wrong_box = SurroundingRectangle(wrong, buff=0.28, color=MID_GRAY, stroke_width=2)
        wrong_group = VGroup(wrong_box, wrong).move_to(LEFT * 4.1 + UP * 0.25)
        cross1 = Line(wrong_box.get_corner(UL), wrong_box.get_corner(DR), color=DARK_GRAY, stroke_width=5)
        cross2 = Line(wrong_box.get_corner(DL), wrong_box.get_corner(UR), color=DARK_GRAY, stroke_width=5)

        correct = VGroup(
            self.text("APPROXIMATE LIGHT SPEED", 23, BOLD),
            self.math(r"c\approx300\,000\;\mathrm{km/s}", 42),
            self.math(r"c\approx1.08\times10^9\;\mathrm{km/h}", 34),
        ).arrange(DOWN, buff=0.18)
        correct_box = SurroundingRectangle(correct, buff=0.28, color=BLACK_LINE, stroke_width=2.3)
        correct_group = VGroup(correct_box, correct).move_to(RIGHT * 3.6 + UP * 0.25)
        self.play(FadeIn(wrong_group), run_time=RUN_NORMAL)
        self.play(Create(cross1), Create(cross2), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        self.play(FadeIn(correct_group, shift=LEFT * 0.12), run_time=RUN_SLOW)
        note = self.text("From here on, c means the physical speed of light.", 27, BOLD).to_edge(DOWN, buff=0.52)
        self.play(Write(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def light_inside_train_3d(self) -> None:
        self.set_header(
            6,
            "LIGHT SEEN FROM INSIDE THE METRO",
            "The walker switches on the lamp. A seated observer measures the outgoing light pulse at c, not c + 2 km/h.",
        )
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.84, run_time=RUN_CAMERA)
        train = self.make_train_3d()
        student = self.make_person_3d([-1.4, 0.45, -0.08], scale=0.90)
        walker = self.make_person_3d([0.55, -0.25, -0.04], scale=0.95, walker=True)
        lamp = self.make_lamp_3d([0.85, -0.25, 0.27])
        self.play(FadeIn(train), FadeIn(student), FadeIn(walker), FadeIn(lamp), run_time=RUN_SLOW)
        label = self.formula_panel(r"v_{\mathrm{light/train}}=c", width=4.6, size=39).move_to(RIGHT * 4.7 + DOWN * 2.55)
        self.show_fixed(label, run_time=RUN_NORMAL)
        pulse = self.light_pulse(lamp.get_center())
        self.play(FadeIn(pulse), run_time=RUN_QUICK)
        self.play(pulse.animate.scale(7.5), run_time=4.6, rate_func=linear)
        note = self.text("Inside frame: the wave expands symmetrically around the emission event.", 23)
        note.to_edge(DOWN, buff=0.28)
        self.show_fixed(note, run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def light_ground_frame_3d(self) -> None:
        self.set_header(
            7,
            "LIGHT SEEN FROM THE STATION",
            "The train keeps moving after emission, but the ground observer also measures the light pulse at exactly c.",
        )
        self.move_camera(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=0.82, run_time=RUN_CAMERA)
        tracks = self.platform_3d()
        train = self.make_train_3d().shift(LEFT * 2.6)
        walker = self.make_person_3d([-2.05, -0.25, -0.04], scale=0.95, walker=True)
        lamp = self.make_lamp_3d([-1.75, -0.25, 0.27])
        moving = VGroup(train, walker, lamp)
        observer = self.make_person_3d([4.9, -3.0, -0.30], scale=1.0)
        emission_point = lamp.get_center().copy()
        self.play(Create(tracks), FadeIn(moving), FadeIn(observer), run_time=RUN_SLOW)
        pulse = self.light_pulse(emission_point)
        self.play(FadeIn(pulse), run_time=RUN_QUICK)
        label = VGroup(
            self.formula_panel(r"v_{\mathrm{light/ground}}=c", width=4.8, size=39),
            self.text("NOT c + 80 and NOT c + 82", 24, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 4.6 + DOWN * 2.55)
        self.show_fixed(label, run_time=RUN_NORMAL)
        self.play(pulse.animate.scale(7.5), moving.animate.shift(RIGHT * 3.0), run_time=4.8, rate_func=linear)
        note = self.text("The source moves away from the emission point; the light speed remains c.", 23)
        note.to_edge(DOWN, buff=0.25)
        self.show_fixed(note, run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def lorentz_velocity_addition(self) -> None:
        self.set_header(
            8,
            "WHY DOES CLASSICAL ADDITION FAIL FOR LIGHT?",
            "Special relativity replaces Galilean addition with the relativistic velocity-addition law.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        classical = VGroup(
            self.text("GALILEAN IDEA", 27, BOLD),
            self.math(r"u=u'+v", 42),
            self.math(r"2+80=82\;\mathrm{km/h}", 34),
            self.text("Excellent for ordinary speeds", 22),
        ).arrange(DOWN, buff=0.18)
        box1 = RoundedRectangle(width=6.2, height=3.05, corner_radius=0.14, stroke_color=MID_GRAY, fill_color=WHITE, fill_opacity=1)
        classical.move_to(box1)
        classical_group = VGroup(box1, classical).move_to(LEFT * 4.0 + DOWN * 0.35)

        relativistic = VGroup(
            self.text("RELATIVISTIC LAW", 27, BOLD),
            self.math(r"u=\frac{u'+v}{1+\frac{u'v}{c^2}}", 42),
            self.math(r"u'=c\;\Longrightarrow\;u=c", 38),
            self.text("Light speed stays invariant", 22, BOLD),
        ).arrange(DOWN, buff=0.18)
        box2 = RoundedRectangle(width=6.4, height=3.05, corner_radius=0.14, stroke_color=BLACK_LINE, stroke_width=2.2, fill_color=PAPER_GRAY, fill_opacity=1)
        relativistic.move_to(box2)
        relativistic_group = VGroup(box2, relativistic).move_to(RIGHT * 3.9 + DOWN * 0.35)
        self.play(FadeIn(classical_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(relativistic_group, shift=LEFT * 0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        derivation = self.math(
            r"u=\frac{c+v}{1+\frac{cv}{c^2}}"
            r"=\frac{c+v}{1+\frac{v}{c}}"
            r"=\frac{c\left(1+\frac{v}{c}\right)}{1+\frac{v}{c}}=c",
            30,
        ).to_edge(DOWN, buff=0.32)
        self.play(Write(derivation), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def final_summary(self) -> None:
        self.set_header(
            9,
            "FINAL COMPARISON — WHAT EACH OBSERVER MEASURES",
            "The walker follows ordinary relative-velocity addition; light reveals the special-relativity principle that c is invariant.",
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)

        headers = ["OBJECT", "INSIDE METRO", "GROUND / STATION"]
        rows = [
            ["Metro", "0 km/h", "80 km/h"],
            ["Walker", "2 km/h", "82 km/h"],
            ["Light", "c", "c"],
        ]
        col_w = [3.0, 4.4, 4.6]
        table = VGroup()
        y0 = 1.45
        for c, text_value in enumerate(headers):
            rect = Rectangle(width=col_w[c], height=0.78, stroke_color=BLACK_LINE, stroke_width=2, fill_color=PAPER_GRAY, fill_opacity=1)
            rect.move_to([-4.6 + sum(col_w[:c]) + col_w[c] / 2, y0, 0])
            txt = self.text(text_value, 23, BOLD).move_to(rect)
            table.add(VGroup(rect, txt))
        for r, row in enumerate(rows):
            y = y0 - (r + 1) * 0.86
            for c, text_value in enumerate(row):
                rect = Rectangle(width=col_w[c], height=0.78, stroke_color=LIGHT_GRAY, stroke_width=1.5, fill_color=WHITE, fill_opacity=1)
                rect.move_to([-4.6 + sum(col_w[:c]) + col_w[c] / 2, y, 0])
                txt = self.text(text_value, 27 if c else 24, BOLD if c == 0 else NORMAL).move_to(rect)
                table.add(VGroup(rect, txt))
        self.play(LaggedStart(*[FadeIn(cell) for cell in table], lag_ratio=0.06), run_time=RUN_SLOW * 1.5)
        self.wait(PAUSE_EXPLAIN)

        takeaways = VGroup(
            self.text("1. Always state the reference frame.", 27, BOLD),
            self.text("2. For the walker: 2 km/h inside, 82 km/h outside.", 27),
            self.text("3. For light: every inertial observer measures c.", 27, BOLD),
            self.text("4. This is the doorway to special relativity.", 27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 2.45)
        self.play(LaggedStart(*[Write(line) for line in takeaways], lag_ratio=0.16), run_time=RUN_SLOW * 1.6)
        self.wait(PAUSE_FINAL)

        question = VGroup(
            self.text("EXIT QUESTION", 28, BOLD),
            self.text("Why can the walker's speed change with the observer, while the measured speed of light does not?", 27),
        ).arrange(DOWN, buff=0.18)
        self.fit(question, 13.8, 1.4)
        question_box = SurroundingRectangle(question, buff=0.28, color=BLACK_LINE, stroke_width=2.2)
        final = VGroup(question_box, question).move_to(ORIGIN)
        self.play(FadeOut(table), FadeOut(takeaways), run_time=RUN_NORMAL)
        self.play(FadeIn(final), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(final), run_time=RUN_NORMAL)
        if self.header is not None:
            self.remove_fixed(self.header, run_time=RUN_QUICK)
            self.header = None
