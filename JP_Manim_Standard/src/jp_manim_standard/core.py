"""Core scene behavior: timing, typography, headers, safe layout and camera focus."""
from __future__ import annotations
from collections.abc import Sequence
from manim import *
from .theme import *

class CoreMixin:
    def setup(self) -> None:
        super().setup()
        self.validate_lesson_data()
        self.camera.background_color = WHITE
        if hasattr(self.camera, "frame"):
            self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group = None
        self.subtitle_group = None

    def validate_lesson_data(self) -> None:
        """Override and assert every displayed numerical claim."""

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight, line_spacing=0.92, **kwargs)

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def fit_content_zone(self, mob: Mobject, max_width: float = 14.4, max_height: float = 5.85) -> Mobject:
        return self.fit(mob, max_width, max_height)

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE_FILL, fill_opacity=1.0)
        number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)
        title_text = self.text(title, 34, BOLD)
        self.fit(title_text, SAFE_WIDTH - number_box.width - 0.38, 0.56)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2).next_to(title_row, DOWN, buff=0.07)
        subtitle_text = self.text(subtitle, 21)
        self.fit(subtitle_text, 14.25, 0.70)
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
            old = self.subtitle_group
            self.subtitle_group = subtitle_text
            self.play(ReplacementTransform(old, subtitle_text), run_time=RUN_QUICK)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep = set()
        if keep_header:
            for group in (self.header_group, self.subtitle_group):
                if group is not None:
                    keep.add(group)
        targets = [mob for mob in list(self.mobjects) if mob not in keep]
        if targets:
            self.play(*[FadeOut(mob) for mob in targets], run_time=RUN_QUICK)

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.03) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -FRAME_WIDTH / 2 + margin or right > FRAME_WIDTH / 2 - margin:
            raise AssertionError(f"{label}: horizontal frame overflow")
        if bottom < -FRAME_HEIGHT / 2 + margin or top > FRAME_HEIGHT / 2 - margin:
            raise AssertionError(f"{label}: vertical frame overflow")

    def assert_content_safe(self, mob: Mobject, label: str) -> None:
        self.assert_within_frame(mob, label)
        if mob.get_top()[1] > CONTENT_TOP_Y or mob.get_bottom()[1] < CONTENT_BOTTOM_Y:
            raise AssertionError(f"{label}: outside classroom content zone")

    def focus_on(self, mob: Mobject, width: float = 8.0, pause: float = PAUSE_READ) -> None:
        if not hasattr(self.camera, "frame"):
            return
        hidden = [g for g in (self.header_group, self.subtitle_group) if g is not None]
        self.camera.frame.save_state()
        animations = [self.camera.frame.animate.set(width=width).move_to(mob)]
        animations += [FadeOut(g) for g in hidden]
        self.play(*animations, run_time=RUN_CAMERA)
        self.wait(pause)
        self.play(Restore(self.camera.frame), *[FadeIn(g) for g in hidden], run_time=RUN_CAMERA)

    def focus_sequence(self, mobs: Sequence[Mobject], width: float = 8.0, pause: float = PAUSE_READ) -> None:
        for mob in mobs:
            self.focus_on(mob, width=width, pause=pause)
