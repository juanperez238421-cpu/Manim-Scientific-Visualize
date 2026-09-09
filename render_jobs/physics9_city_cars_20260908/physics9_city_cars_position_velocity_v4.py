"""Physics 9 — City Cars V4 · JP Classroom Standard.

V4 keeps the improved V3 road/city and physically mirrored car diagrams, but
rebuilds the lesson using the canonical JP classroom architecture:
- white 16:9 canvas and monochrome UI hierarchy;
- persistent numbered section header + subtitle;
- safe content zones and consistent panels;
- diagram + equations visible together when they explain the same idea;
- restrained colors only for Car A, Car B, and the meeting result;
- explicit step-by-step algebra and reproducible method summary.

Exact physics is unchanged:
    x_A(0)=0 km,      v_A=+80 km/h
    x_B(0)=240 km,   v_B=-40 km/h
    meeting: t=2 h, x=160 km

ManimCE target: 0.20.1
Final render:
    manim -pqh render_jobs/physics9_city_cars_20260908/physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4 --disable_caching
Fast QA:
    LESSON_TIME_SCALE=0.06 manim -ql render_jobs/physics9_city_cars_20260908/physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4 --disable_caching
"""

from __future__ import annotations

import os
import numpy as np
from manim import *


# =============================================================================
# JP CLASSROOM RENDER + VISUAL CONTRACT
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

FRAME_WIDTH = 16.0
SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.60
CONTENT_BOTTOM_Y = -4.05

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"
WHITE_FILL = WHITE

# Semantic accents only.
BLUE_A = "#1F67D2"
RED_B = "#D74747"
GREEN_MEET = "#27865E"
GOLD_LIGHT = "#B47A16"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.35
PAUSE_SHORT = 0.85
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80
PAUSE_SUMMARY = 4.60
PAUSE_FINAL = 5.20


# =============================================================================
# EXACT LESSON DATA — UNCHANGED FROM V3
# =============================================================================
A0 = 0.0
B0 = 240.0
VA = 80.0
VB = -40.0
T_MEET = 2.0
X_MEET = 160.0


def assert_close(actual: float, expected: float, tol: float = 1e-10, label: str = "value") -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


# =============================================================================
# COMPACT JP CLASSROOM BASE
# =============================================================================
class JPMathClassroomScene(MovingCameraScene):
    """Compact local implementation of the consolidated JP classroom style."""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group: VGroup | None = None
        self.subtitle_group: Mobject | None = None
        self.validate_lesson_data()

    def validate_lesson_data(self) -> None:
        pass

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] = max(0.05, float(kwargs["run_time"]) * TIME_SCALE)
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(max(0.05, duration * TIME_SCALE), *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, color=BLACK_TEXT, **kwargs) -> Text:
        return Text(
            content,
            font="DejaVu Sans",
            font_size=size,
            color=color,
            weight=weight,
            line_spacing=0.92,
            **kwargs,
        )

    def math(self, expression: str, size: int = 38, color=BLACK_TEXT, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=color, **kwargs)

    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.10) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -FRAME_WIDTH / 2 + margin or right > FRAME_WIDTH / 2 - margin:
            raise ValueError(f"{label} exceeds horizontal frame bounds: left={left:.3f}, right={right:.3f}")
        if bottom < -4.5 + margin or top > 4.5 - margin:
            raise ValueError(f"{label} exceeds vertical frame bounds: bottom={bottom:.3f}, top={top:.3f}")

    def assert_content_safe(self, mob: Mobject, label: str) -> None:
        self.assert_within_frame(mob, label, margin=0.15)
        if mob.get_top()[1] > CONTENT_TOP_Y:
            raise ValueError(f"{label} overlaps the persistent header zone")
        if mob.get_bottom()[1] < CONTENT_BOTTOM_Y:
            raise ValueError(f"{label} exceeds the safe lower content zone")

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(
            width=0.72,
            height=0.52,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)
        number_group = VGroup(number_box, number_text)

        title_text = self.text(title.upper(), 32, BOLD)
        self.fit(title_text, SAFE_WIDTH - 1.10, 0.56)
        title_row = VGroup(number_group, title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        subtitle_text = self.text(subtitle, 20)
        self.fit(subtitle_text, 14.25, 0.68)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)

        new_header = VGroup(title_row, rule)
        if self.header_group is None:
            self.header_group = new_header
            self.add(new_header)
        else:
            old = self.header_group
            self.header_group = new_header
            self.play(ReplacementTransform(old, new_header), run_time=RUN_QUICK)

        if self.subtitle_group is None:
            self.subtitle_group = subtitle_text
            self.add(subtitle_text)
        else:
            old_sub = self.subtitle_group
            self.subtitle_group = subtitle_text
            self.play(ReplacementTransform(old_sub, subtitle_text), run_time=RUN_QUICK)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep_ids: set[int] = set()
        if keep_header:
            for persistent in (self.header_group, self.subtitle_group):
                if persistent is not None:
                    keep_ids.update(id(member) for member in persistent.get_family())
        removable = [mob for mob in self.mobjects if id(mob) not in keep_ids]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_NORMAL)
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)

    def formula_panel(
        self,
        expression: str,
        width: float = 6.0,
        height: float = 1.08,
        font_size: int = 40,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        eq = self.math(expression, font_size)
        self.fit(eq, width - 0.50, height - 0.22)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(
        self,
        title: str,
        lines: list[str],
        width: float = 5.4,
        title_size: int = 25,
        body_size: int = 22,
    ) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.56, 3.15)

        box = RoundedRectangle(
            width=width,
            height=max(1.25, content.height + 0.58),
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def figure_panel(
        self,
        figure: Mobject,
        width: float,
        height: float,
        title: str | None = None,
        caption: str | None = None,
    ) -> tuple[VGroup, RoundedRectangle, Mobject]:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        available_h = height - 0.70
        if title:
            available_h -= 0.45
        if caption:
            available_h -= 0.42
        self.fit(figure, width - 0.55, max(0.8, available_h))
        figure.move_to(box)

        pieces: list[Mobject] = [box, figure]
        if title:
            title_mob = self.text(title, 24, BOLD)
            self.fit(title_mob, width - 0.50, 0.42)
            title_mob.next_to(box.get_top(), DOWN, buff=0.16)
            figure.shift(DOWN * 0.15)
            pieces.append(title_mob)
        if caption:
            caption_mob = self.text(caption, 18)
            self.fit(caption_mob, width - 0.50, 0.34)
            caption_mob.next_to(box.get_bottom(), UP, buff=0.15)
            figure.shift(UP * 0.10)
            pieces.append(caption_mob)
        return VGroup(*pieces), box, figure

    def split_layout(
        self,
        left: Mobject,
        right: Mobject,
        left_width: float,
        right_width: float,
        max_height: float = 5.45,
        gap: float = 0.40,
        center_y: float = -0.50,
    ) -> VGroup:
        self.fit(left, left_width, max_height)
        self.fit(right, right_width, max_height)
        left.move_to(LEFT * ((right_width + gap) / 2) + UP * center_y)
        right.move_to(RIGHT * ((left_width + gap) / 2) + UP * center_y)
        group = VGroup(left, right)
        self.fit(group, 14.4, max_height)
        return group

    def equation_stack(
        self,
        equations: list[str],
        sizes: list[int],
        buff: float = 0.28,
        max_width: float = 6.0,
        max_height: float = 4.5,
    ) -> VGroup:
        stack = VGroup(*[self.math(eq, size) for eq, size in zip(equations, sizes)])
        stack.arrange(DOWN, aligned_edge=LEFT, buff=buff)
        self.fit(stack, max_width, max_height)
        return stack

    def animate_equation_stack(self, stack: VGroup, pause: float = PAUSE_READ) -> None:
        for line in stack:
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(pause)

    def process_map(self, steps: list[tuple[str, str]], columns: int = 3) -> VGroup:
        cards = VGroup()
        card_width, card_height = 4.30, 1.10
        for number, label in steps:
            badge = RoundedRectangle(
                width=0.66,
                height=0.50,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.5,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1,
            )
            badge_text = self.text(number, 19, BOLD).move_to(badge)
            body = self.text(label, 20, BOLD)
            content = VGroup(VGroup(badge, badge_text), body).arrange(RIGHT, buff=0.18)
            self.fit(content, card_width - 0.35, card_height - 0.20)
            box = RoundedRectangle(
                width=card_width,
                height=card_height,
                corner_radius=0.10,
                stroke_color=BLACK_LINE,
                stroke_width=1.5,
                fill_color=WHITE_FILL,
                fill_opacity=1,
            )
            content.move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(cols=columns, buff=(0.25, 0.25))
        return cards

    def standard_opening(self, course_label: str, title: str, subtitle: str, promise: str) -> None:
        label = self.text(course_label, 28, BOLD)
        title_mob = self.text(title, 50, BOLD)
        rule = Line(LEFT * 5.5, RIGHT * 5.5, color=BLACK_LINE, stroke_width=2.2)
        subtitle_mob = self.text(subtitle, 27)
        promise_mob = self.text(promise, 25, MEDIUM)
        group = VGroup(label, title_mob, rule, subtitle_mob, promise_mob).arrange(DOWN, buff=0.30)
        self.fit(group, 14.4, 6.6)

        self.play(FadeIn(label, shift=UP * 0.18), run_time=RUN_NORMAL)
        self.play(Write(title_mob), run_time=RUN_SLOW)
        self.play(Create(rule), FadeIn(subtitle_mob), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(promise_mob, shift=UP * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str) -> None:
        closing = self.text(sentence, 34, BOLD)
        self.fit(closing, 13.8, 1.2)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)


# =============================================================================
# PRESERVED V3 DIAGRAM GEOMETRY
# =============================================================================
def diagram_text(content: str, size: int = 30, color=BLACK_TEXT, weight=NORMAL) -> Text:
    return Text(
        content,
        font="DejaVu Sans",
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=0.92,
    )


def city_icon(name: str, accent) -> VGroup:
    ground = Line(LEFT * 1.0, RIGHT * 1.0, color=BLACK_LINE, stroke_width=2.5)
    blocks = VGroup(
        Rectangle(width=0.50, height=0.72, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1),
        Rectangle(width=0.42, height=1.06, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1),
        Rectangle(width=0.58, height=0.86, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1),
    ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
    blocks.next_to(ground, UP, buff=0)
    roof = Triangle(stroke_color=accent, stroke_width=2.2, fill_color=WHITE_FILL, fill_opacity=1).scale(0.20)
    roof.next_to(blocks[1], UP, buff=0.02)
    label = diagram_text(name, 23, accent, BOLD).next_to(ground, DOWN, buff=0.10)
    return VGroup(ground, blocks, roof, label)


def directional_car(color, facing: int = 1, label: str | None = None, scale: float = 1.0) -> VGroup:
    """Physically asymmetric car from V3.

    facing=+1 -> actual nose/headlight right.
    facing=-1 -> body, cabin, headlight and vector are physically mirrored left.
    """
    s = 1 if facing >= 0 else -1

    body = Polygon(
        np.array([-1.40 * s, -0.20, 0]),
        np.array([-1.22 * s, 0.28, 0]),
        np.array([-0.50 * s, 0.46, 0]),
        np.array([0.20 * s, 0.44, 0]),
        np.array([0.72 * s, 0.27, 0]),
        np.array([1.34 * s, 0.16, 0]),
        np.array([1.48 * s, -0.20, 0]),
        stroke_color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=0.10,
    )

    cabin = Polygon(
        np.array([-0.48 * s, 0.46, 0]),
        np.array([-0.08 * s, 0.88, 0]),
        np.array([0.55 * s, 0.82, 0]),
        np.array([0.83 * s, 0.28, 0]),
        stroke_color=color,
        stroke_width=2.5,
        fill_color=WHITE_FILL,
        fill_opacity=1,
    )
    windshield = Line(
        np.array([0.55 * s, 0.80, 0]),
        np.array([0.82 * s, 0.30, 0]),
        color=color,
        stroke_width=3.6,
    )

    wheels = VGroup(*[
        Circle(radius=0.25, stroke_color=BLACK_LINE, stroke_width=2.6, fill_color=WHITE_FILL, fill_opacity=1)
        .move_to(np.array([x * s, -0.25, 0]))
        for x in (-0.88, 0.93)
    ])
    hubs = VGroup(*[
        Circle(radius=0.065, stroke_width=0, fill_color=MID_GRAY, fill_opacity=1).move_to(w.get_center())
        for w in wheels
    ])

    # Headlight stays at the physical nose in both directions.
    head = RoundedRectangle(
        width=0.16,
        height=0.14,
        corner_radius=0.03,
        stroke_width=0,
        fill_color=GOLD_LIGHT,
        fill_opacity=1,
    ).move_to(np.array([1.40 * s, 0.03, 0]))
    tail = RoundedRectangle(
        width=0.12,
        height=0.16,
        corner_radius=0.03,
        stroke_width=0,
        fill_color=RED_B,
        fill_opacity=0.85,
    ).move_to(np.array([-1.34 * s, 0.02, 0]))

    vector = Arrow(
        np.array([-0.72 * s, 1.18, 0]),
        np.array([0.72 * s, 1.18, 0]),
        buff=0,
        color=color,
        stroke_width=5.4,
        max_tip_length_to_length_ratio=0.20,
    )

    car = VGroup(body, cabin, windshield, wheels, hubs, head, tail, vector)
    if label:
        label_mob = diagram_text(label, 23, color, BOLD).next_to(car, UP, buff=0.06)
        car.add(label_mob)
    return car.scale(scale)


def road_diagram(show_cars: bool = True):
    x_left, x_right, y = -5.60, 5.60, -0.22
    slab = RoundedRectangle(
        width=12.4,
        height=1.28,
        corner_radius=0.18,
        stroke_color=BLACK_LINE,
        stroke_width=1.7,
        fill_color=VERY_LIGHT_GRAY,
        fill_opacity=1,
    ).move_to([0, y, 0])
    edge_top = Line([x_left, y + 0.49, 0], [x_right, y + 0.49, 0], color=BLACK_LINE, stroke_width=1.8)
    edge_bottom = Line([x_left, y - 0.49, 0], [x_right, y - 0.49, 0], color=BLACK_LINE, stroke_width=1.8)
    dashed = DashedLine(
        [x_left + 0.12, y, 0],
        [x_right - 0.12, y, 0],
        dash_length=0.30,
        dashed_ratio=0.56,
        color=WHITE,
        stroke_width=3.6,
    )

    city_a = city_icon("CITY A", BLUE_A).scale(0.76).move_to([x_left, 1.10, 0])
    city_b = city_icon("CITY B", RED_B).scale(0.76).move_to([x_right, 1.10, 0])
    zero = diagram_text("0 km", 21, BLUE_A, BOLD).move_to([x_left, -1.24, 0])
    two_forty = diagram_text("240 km", 21, RED_B, BOLD).move_to([x_right, -1.24, 0])
    plus_x = Arrow([2.75, -1.55, 0], [4.40, -1.55, 0], buff=0, color=BLACK_LINE, stroke_width=3.2)
    plus_label = MathTex(r"+x", color=BLACK_TEXT, font_size=30).next_to(plus_x, RIGHT, buff=0.10)

    def x_for_km(km: float) -> float:
        return x_left + (x_right - x_left) * (km / 240.0)

    group = VGroup(slab, edge_top, edge_bottom, dashed, city_a, city_b, zero, two_forty, plus_x, plus_label)
    cars = None
    if show_cars:
        car_a = directional_car(BLUE_A, +1, scale=0.60).move_to([x_for_km(34), y + 0.27, 0])
        car_b = directional_car(RED_B, -1, scale=0.60).move_to([x_for_km(206), y - 0.27, 0])
        group.add(car_a, car_b)
        cars = (car_a, car_b)
    return group, x_for_km, cars


# =============================================================================
# MAIN V4 LESSON
# =============================================================================
class Physics9CityCarsV4(JPMathClassroomScene):
    """V3 diagrams + canonical JP classroom code/style format."""

    def validate_lesson_data(self) -> None:
        assert_close((B0 - A0) / (VA - VB), T_MEET, label="meeting time")
        assert_close(A0 + VA * T_MEET, X_MEET, label="A meeting position")
        assert_close(B0 + VB * T_MEET, X_MEET, label="B meeting position")
        assert_close(abs(VA) * T_MEET + abs(VB) * T_MEET, B0 - A0, label="distance closure")

    def construct(self) -> None:
        self.opening()
        self.physical_model()
        self.sign_convention()
        self.position_equations()
        self.solve_meeting()
        self.live_meeting()
        self.position_graph()
        self.velocity_graph()
        self.cross_checks()
        self.summary()

    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9 · UNIFORM MOTION",
            "TWO CARS · ONE MEETING POINT",
            "Connect a real road diagram to signed velocity, equations and graphs.",
            "Visualize first. Formalize second. Verify with more than one representation.",
        )

    def physical_model(self) -> None:
        self.set_header(
            1,
            "START FROM THE PHYSICAL MODEL",
            "The diagram establishes initial position, separation and physical direction before any algebra appears.",
        )

        road, x_for_km, _ = road_diagram(show_cars=False)
        car_a = directional_car(BLUE_A, +1, "CAR A", 0.62).move_to([x_for_km(40), 0.05, 0])
        car_b = directional_car(RED_B, -1, "CAR B", 0.62).move_to([x_for_km(200), -0.47, 0])
        road.add(car_a, car_b)
        separation = DoubleArrow(
            [x_for_km(0), 1.95, 0],
            [x_for_km(240), 1.95, 0],
            buff=0.06,
            color=BLACK_LINE,
            stroke_width=2.8,
        )
        separation_label = self.text("240 km separation", 23, BOLD).next_to(separation, UP, buff=0.08)
        figure = VGroup(road, separation, separation_label)
        figure_group, _, _ = self.figure_panel(
            figure,
            width=8.65,
            height=4.95,
            title="PHYSICAL ROAD MODEL",
            caption="The car bodies themselves face the direction of travel.",
        )
        data_panel = self.note_panel(
            "GIVEN DATA",
            [
                "Car A starts at 0 km and moves right at 80 km/h.",
                "Car B starts at 240 km and moves left at 40 km/h.",
                "Question: when and where do they meet?",
            ],
            width=5.15,
            title_size=25,
            body_size=20,
        )
        layout = self.split_layout(figure_group, data_panel, 8.65, 5.15, center_y=-0.55)
        self.assert_content_safe(layout, "physical_model layout")

        self.play(FadeIn(figure_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(data_panel, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def sign_convention(self) -> None:
        self.set_header(
            2,
            "CHOOSE +x, THEN ASSIGN VELOCITY SIGNS",
            "Direction is geometric first. The sign of velocity is the mathematical encoding of that choice.",
        )

        road, _, _ = road_diagram(show_cars=False)
        road.scale(0.83)
        car_a = directional_car(BLUE_A, +1, scale=0.64).move_to([-3.10, 0.05, 0])
        car_b = directional_car(RED_B, -1, scale=0.64).move_to([3.10, -0.40, 0])
        plus_arrow = Arrow([-1.00, -1.55, 0], [1.65, -1.55, 0], buff=0, color=BLACK_LINE, stroke_width=3.5)
        plus_label = self.math(r"+x", 31).next_to(plus_arrow, RIGHT, buff=0.12)
        figure = VGroup(road, car_a, car_b, plus_arrow, plus_label)
        figure_group, _, _ = self.figure_panel(
            figure,
            width=8.20,
            height=4.85,
            title="SIGN CONVENTION",
            caption="Right is positive; left is negative.",
        )

        eq_a = self.formula_panel(r"v_A=+80\;\mathrm{km/h}", width=5.30, height=1.02, font_size=38)
        eq_a[1].set_color(BLUE_A)
        eq_b = self.formula_panel(r"v_B=-40\;\mathrm{km/h}", width=5.30, height=1.02, font_size=38)
        eq_b[1].set_color(RED_B)
        interpretation = self.note_panel(
            "INTERPRETATION",
            ["The negative sign does not mean 'slower'.", "It means motion opposite to +x."],
            width=5.30,
            title_size=24,
            body_size=20,
        )
        right = VGroup(eq_a, eq_b, interpretation).arrange(DOWN, buff=0.24)
        layout = self.split_layout(figure_group, right, 8.20, 5.30, center_y=-0.55)
        self.assert_content_safe(layout, "sign_convention layout")

        self.play(FadeIn(figure_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq_a), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq_b), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def position_equations(self) -> None:
        self.set_header(
            3,
            "WRITE ONE POSITION EQUATION FOR EACH CAR",
            "Use the same motion model for both objects: initial position plus signed velocity multiplied by time.",
        )

        general = self.formula_panel(r"x(t)=x_0+vt", width=5.60, height=1.12, font_size=43)
        general.move_to([0, 1.82, 0])

        road, _, _ = road_diagram(show_cars=True)
        road_group, _, _ = self.figure_panel(
            road,
            width=6.65,
            height=3.85,
            title="READ VALUES FROM THE DIAGRAM",
            caption="Initial positions and directions must match the equations.",
        )
        eq_a = self.formula_panel(r"x_A(t)=0+(80)t=80t", width=6.35, height=1.05, font_size=36)
        eq_a[1].set_color(BLUE_A)
        eq_b = self.formula_panel(r"x_B(t)=240+(-40)t", width=6.35, height=1.05, font_size=36)
        eq_b[1].set_color(RED_B)
        eq_b2 = self.formula_panel(r"x_B(t)=240-40t", width=6.35, height=1.05, font_size=38)
        eq_b2[1].set_color(RED_B)
        equation_stack = VGroup(eq_a, eq_b, eq_b2).arrange(DOWN, buff=0.20)

        body = VGroup(road_group, equation_stack).arrange(RIGHT, buff=0.42)
        body.move_to([0, -0.75, 0])
        self.fit(body, 14.25, 4.55)
        content = VGroup(general, body)
        self.assert_content_safe(content, "position_equations content")

        self.play(FadeIn(general), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(road_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq_a), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq_b), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(eq_b2), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def solve_meeting(self) -> None:
        self.set_header(
            4,
            "SOLVE THE MEETING CONDITION STEP BY STEP",
            "Meeting means the same position at the same time: set x_A(t)=x_B(t), then transform one line at a time.",
        )

        stack = self.equation_stack(
            [r"x_A=x_B", r"80t=240-40t", r"120t=240", r"t=2\;\mathrm{h}"],
            sizes=[40, 40, 40, 46],
            buff=0.32,
            max_width=6.0,
            max_height=4.2,
        )
        stack[-1].set_color(GREEN_MEET)
        stack.move_to([-3.25, -0.35, 0])

        position_1 = self.formula_panel(r"x=80(2)", width=5.10, height=1.00, font_size=39)
        position_1[1].set_color(BLUE_A)
        position_2 = self.formula_panel(r"x=160\;\mathrm{km}", width=5.10, height=1.06, font_size=43)
        position_2[1].set_color(GREEN_MEET)
        result_note = self.note_panel(
            "RESULT",
            ["Meeting time: 2 h", "Meeting position: 160 km from City A"],
            width=5.10,
            title_size=24,
            body_size=20,
        )
        result = VGroup(position_1, position_2, result_note).arrange(DOWN, buff=0.22)
        result.move_to([3.55, -0.35, 0])
        content = VGroup(stack, result)
        self.fit(content, 13.5, 5.0)
        self.assert_content_safe(content, "solve_meeting content")

        self.animate_equation_stack(stack, pause=PAUSE_READ)
        self.play(FadeIn(position_1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(position_2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(result_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def live_meeting(self) -> None:
        self.set_header(
            5,
            "WATCH BOTH POSITIONS EVOLVE ON THE ROAD",
            "The moving diagram and live numerical readout must agree with the equations at every instant, not only at the final answer.",
        )

        x_left, x_right, road_y = -5.70, 5.70, 0.08
        slab = RoundedRectangle(
            width=12.2,
            height=1.34,
            corner_radius=0.18,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).move_to([0, road_y, 0])
        dashed = DashedLine(
            [x_left, road_y, 0],
            [x_right, road_y, 0],
            dash_length=0.32,
            dashed_ratio=0.56,
            color=WHITE,
            stroke_width=3.5,
        )
        city_a = city_icon("A", BLUE_A).scale(0.68).move_to([x_left, 1.42, 0])
        city_b = city_icon("B", RED_B).scale(0.68).move_to([x_right, 1.42, 0])

        def road_x(km: float) -> float:
            return x_left + (x_right - x_left) * (km / 240.0)

        meet_x = road_x(X_MEET)
        meet_line = DashedLine(
            [meet_x, -0.75, 0],
            [meet_x, 1.95, 0],
            dash_length=0.13,
            color=GREEN_MEET,
            stroke_width=2.6,
        )
        meet_label = self.text("meeting: 160 km", 20, BOLD).set_color(GREEN_MEET).next_to(meet_line, UP, buff=0.06)

        tracker = ValueTracker(0.0)
        car_a = always_redraw(
            lambda: directional_car(BLUE_A, +1, scale=0.53).move_to([
                road_x(A0 + VA * tracker.get_value()),
                road_y + 0.27,
                0,
            ])
        )
        car_b = always_redraw(
            lambda: directional_car(RED_B, -1, scale=0.53).move_to([
                road_x(B0 + VB * tracker.get_value()),
                road_y - 0.27,
                0,
            ])
        )

        readout_box = RoundedRectangle(
            width=12.15,
            height=1.34,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        ).move_to([0, -2.30, 0])

        labels = VGroup(
            self.text("t =", 19, BOLD).move_to([-5.10, -2.30, 0]),
            self.text("x_A =", 19, BOLD).set_color(BLUE_A).move_to([-2.40, -2.30, 0]),
            self.text("x_B =", 19, BOLD).set_color(RED_B).move_to([0.85, -2.30, 0]),
            self.text("gap =", 19, BOLD).set_color(GREEN_MEET).move_to([3.95, -2.30, 0]),
        )
        units = VGroup(
            self.text("h", 18, BOLD).move_to([-3.95, -2.30, 0]),
            self.text("km", 18, BOLD).set_color(BLUE_A).move_to([-0.82, -2.30, 0]),
            self.text("km", 18, BOLD).set_color(RED_B).move_to([2.43, -2.30, 0]),
            self.text("km", 18, BOLD).set_color(GREEN_MEET).move_to([5.48, -2.30, 0]),
        )
        time_num = always_redraw(lambda: DecimalNumber(tracker.get_value(), num_decimal_places=2, font_size=27, color=BLACK_TEXT).move_to([-4.48, -2.30, 0]))
        xa_num = always_redraw(lambda: DecimalNumber(A0 + VA * tracker.get_value(), num_decimal_places=2, font_size=27, color=BLUE_A).move_to([-1.55, -2.30, 0]))
        xb_num = always_redraw(lambda: DecimalNumber(B0 + VB * tracker.get_value(), num_decimal_places=2, font_size=27, color=RED_B).move_to([1.60, -2.30, 0]))
        gap_num = always_redraw(
            lambda: DecimalNumber(
                max(0.0, (B0 + VB * tracker.get_value()) - (A0 + VA * tracker.get_value())),
                num_decimal_places=2,
                font_size=27,
                color=GREEN_MEET,
            ).move_to([4.75, -2.30, 0])
        )

        static = VGroup(slab, dashed, city_a, city_b, meet_line, meet_label, readout_box, labels, units)
        self.assert_content_safe(static, "live_meeting static")

        self.play(FadeIn(VGroup(slab, dashed, city_a, city_b)), run_time=RUN_NORMAL)
        self.play(Create(meet_line), FadeIn(meet_label), run_time=RUN_NORMAL)
        self.add(car_a, car_b)
        self.play(FadeIn(readout_box), FadeIn(labels), FadeIn(units), run_time=RUN_NORMAL)
        self.add(time_num, xa_num, xb_num, gap_num)
        self.wait(PAUSE_READ)
        self.play(tracker.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        self.wait(PAUSE_READ)
        self.play(tracker.animate.set_value(2.0), run_time=3.0, rate_func=linear)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def position_graph(self) -> None:
        self.set_header(
            6,
            "POSITION–TIME GRAPH: THE MEETING IS AN INTERSECTION",
            "Each line is the same motion already shown on the road. Equal position at equal time appears as one shared point.",
        )

        axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[0, 240, 40],
            x_length=7.6,
            y_length=4.25,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3], "font_size": 20},
            y_axis_config={"numbers_to_include": [0, 80, 160, 240], "font_size": 20},
        )
        labels = axes.get_axis_labels(self.math(r"t\;(h)", 27), self.math(r"x\;(km)", 27))
        graph_a = axes.plot(lambda t: 80 * t, x_range=[0, 3], color=BLUE_A, stroke_width=4.2)
        graph_b = axes.plot(lambda t: 240 - 40 * t, x_range=[0, 3], color=RED_B, stroke_width=4.2)
        point = Dot(axes.c2p(2, 160), radius=0.085, color=GREEN_MEET)
        vline = DashedLine(axes.c2p(2, 0), axes.c2p(2, 160), color=GREEN_MEET, stroke_width=1.8)
        hline = DashedLine(axes.c2p(0, 160), axes.c2p(2, 160), color=GREEN_MEET, stroke_width=1.8)
        graph = VGroup(axes, labels, graph_a, graph_b, point, vline, hline)
        graph_group, graph_box, _ = self.figure_panel(
            graph,
            width=8.65,
            height=5.00,
            title="POSITION–TIME GRAPH",
            caption="Intersection: (2 h, 160 km).",
        )

        eq_a = self.formula_panel(r"x_A=80t", width=5.0, height=0.94, font_size=33)
        eq_a[1].set_color(BLUE_A)
        eq_b = self.formula_panel(r"x_B=240-40t", width=5.0, height=0.94, font_size=33)
        eq_b[1].set_color(RED_B)
        note = self.note_panel(
            "READ THE GRAPH",
            ["Positive slope → motion right.", "Negative slope → motion left.", "The shared point is the meeting event."],
            width=5.0,
            title_size=24,
            body_size=19,
        )
        right = VGroup(eq_a, eq_b, note).arrange(DOWN, buff=0.20)
        layout = self.split_layout(graph_group, right, 8.65, 5.0, center_y=-0.55)
        self.assert_content_safe(layout, "position_graph layout")

        # Box first; graph content is staged afterward.
        title_caption = VGroup(*[m for m in graph_group if m is not graph and m is not graph_box])
        self.play(FadeIn(graph_box), FadeIn(title_caption), run_time=RUN_NORMAL)
        self.play(Create(axes), FadeIn(labels), run_time=RUN_NORMAL)
        self.play(Create(graph_a), FadeIn(eq_a), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(Create(graph_b), FadeIn(eq_b), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(Create(vline), Create(hline), FadeIn(point, scale=1.4), run_time=RUN_NORMAL)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def velocity_graph(self) -> None:
        self.set_header(
            7,
            "VELOCITY–TIME GRAPH: DIRECTION BECOMES VERTICAL POSITION",
            "Constant velocity produces horizontal lines. The sign tells which direction each object moves relative to +x.",
        )

        axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-60, 100, 20],
            x_length=7.6,
            y_length=4.25,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3], "font_size": 20},
            y_axis_config={"numbers_to_include": [-40, 0, 40, 80], "font_size": 20},
        )
        labels = axes.get_axis_labels(self.math(r"t\;(h)", 27), self.math(r"v\;(km/h)", 27))
        zero = DashedLine(axes.c2p(0, 0), axes.c2p(3, 0), color=MID_GRAY, stroke_width=1.8)
        graph_a = axes.plot(lambda t: 80, x_range=[0, 3], color=BLUE_A, stroke_width=4.5)
        graph_b = axes.plot(lambda t: -40, x_range=[0, 3], color=RED_B, stroke_width=4.5)
        graph = VGroup(axes, labels, zero, graph_a, graph_b)
        graph_group, graph_box, _ = self.figure_panel(
            graph,
            width=8.65,
            height=5.00,
            title="VELOCITY–TIME GRAPH",
            caption="Both lines are horizontal because both velocities are constant.",
        )

        eq_a = self.formula_panel(r"v_A=+80", width=5.0, height=0.94, font_size=35)
        eq_a[1].set_color(BLUE_A)
        eq_b = self.formula_panel(r"v_B=-40", width=5.0, height=0.94, font_size=35)
        eq_b[1].set_color(RED_B)
        note = self.note_panel(
            "READ THE SIGN",
            ["Above zero → positive direction.", "Below zero → negative direction.", "Horizontal line → constant velocity."],
            width=5.0,
            title_size=24,
            body_size=19,
        )
        right = VGroup(eq_a, eq_b, note).arrange(DOWN, buff=0.20)
        layout = self.split_layout(graph_group, right, 8.65, 5.0, center_y=-0.55)
        self.assert_content_safe(layout, "velocity_graph layout")

        title_caption = VGroup(*[m for m in graph_group if m is not graph and m is not graph_box])
        self.play(FadeIn(graph_box), FadeIn(title_caption), run_time=RUN_NORMAL)
        self.play(Create(axes), FadeIn(labels), Create(zero), run_time=RUN_NORMAL)
        self.play(Create(graph_a), FadeIn(eq_a), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(Create(graph_b), FadeIn(eq_b), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def cross_checks(self) -> None:
        self.set_header(
            8,
            "CROSS-CHECK THE RESULT INDEPENDENTLY",
            "A robust physics solution should survive a second method instead of relying on only one algebraic route.",
        )

        left = VGroup(
            self.text("CHECK A · RELATIVE SPEED", 24, BOLD),
            self.formula_panel(r"v_{close}=80+40=120\;\mathrm{km/h}", width=6.15, height=1.02, font_size=34),
            self.formula_panel(r"t=\frac{240}{120}=2\;\mathrm{h}", width=6.15, height=1.08, font_size=40),
            self.text("The 240 km gap closes at 120 km each hour.", 20),
        ).arrange(DOWN, buff=0.24)
        left[2][1].set_color(GREEN_MEET)
        left_box = RoundedRectangle(width=6.55, height=4.65, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE_FILL, fill_opacity=1)
        left.move_to(left_box)
        left_group = VGroup(left_box, left)

        right = VGroup(
            self.text("CHECK B · DISTANCES TRAVELED", 24, BOLD),
            self.formula_panel(r"d_A=80(2)=160\;\mathrm{km}", width=6.15, height=0.98, font_size=34),
            self.formula_panel(r"d_B=40(2)=80\;\mathrm{km}", width=6.15, height=0.98, font_size=34),
            self.formula_panel(r"160+80=240\;\mathrm{km}", width=6.15, height=1.02, font_size=38),
        ).arrange(DOWN, buff=0.20)
        right[1][1].set_color(BLUE_A)
        right[2][1].set_color(RED_B)
        right[3][1].set_color(GREEN_MEET)
        right_box = RoundedRectangle(width=6.55, height=4.65, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE_FILL, fill_opacity=1)
        right.move_to(right_box)
        right_group = VGroup(right_box, right)

        content = VGroup(left_group, right_group).arrange(RIGHT, buff=0.45).move_to([0, -0.58, 0])
        self.fit(content, 13.9, 4.90)
        self.assert_content_safe(content, "cross_checks content")

        self.play(FadeIn(left_box), FadeIn(right_box), run_time=RUN_NORMAL)
        self.play(FadeIn(left[0]), FadeIn(right[0]), run_time=RUN_NORMAL)
        self.play(FadeIn(left[1]), FadeIn(right[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(left[2]), FadeIn(right[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(left[3]), FadeIn(right[3]), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def summary(self) -> None:
        self.set_header(
            9,
            "REUSABLE METHOD FOR TWO-OBJECT MEETING PROBLEMS",
            "Keep the sequence stable: physical direction first, algebra second, and independent checks before accepting the result.",
        )

        route = self.process_map(
            [
                ("01", "DRAW THE ROAD"),
                ("02", "CHOOSE +x"),
                ("03", "ASSIGN SIGNS"),
                ("04", "WRITE x(t)"),
                ("05", "SET POSITIONS EQUAL"),
                ("06", "VERIFY WITH GRAPHS"),
            ],
            columns=3,
        )
        route.move_to([0, -0.10, 0])
        self.fit(route, 13.8, 3.0)
        final = self.formula_panel(r"t=2\;\mathrm{h}\qquad x=160\;\mathrm{km}", width=6.8, height=1.08, font_size=41)
        final[1].set_color(GREEN_MEET)
        final.move_to([0, -2.55, 0])
        content = VGroup(route, final)
        self.assert_content_safe(content, "summary content")

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.10), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Direction → sign → equation → meeting → graph → check.")


if __name__ == "__main__":
    pass
