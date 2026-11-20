#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JP Classroom ManimCE Style — focused runtime subset for Physics 9 Acceleration Graph + Galileo V2 Step-by-Step.

This file preserves the project visual contract used by the full JP classroom
library while keeping only the helpers required by this lesson.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"
WHITE_FILL = WHITE

FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.60
CONTENT_BOTTOM_Y = -4.05

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.35
PAUSE_SHORT = 1.05
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 3.00
PAUSE_SUMMARY = 4.50
PAUSE_FINAL = 4.80


@dataclass
class FigurePanel:
    group: VGroup
    box: RoundedRectangle
    figure: Mobject
    title: Mobject | None
    caption: Mobject | None


@dataclass
class SplitLayout:
    group: VGroup
    left: Mobject
    right: Mobject


class JPClassroomScene(MovingCameraScene):
    def setup(self) -> None:
        super().setup()
        self.validate_lesson_data()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group: VGroup | None = None
        self.subtitle_group: Mobject | None = None

    def validate_lesson_data(self) -> None:
        pass

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(
            content,
            font_size=size,
            color=BLACK_TEXT,
            weight=weight,
            line_spacing=0.92,
            **kwargs,
        )

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def fit_content_zone(self, mob: Mobject, max_width: float = 14.4, max_height: float = 5.85) -> Mobject:
        return self.fit(mob, max_width=max_width, max_height=max_height)

    def formula_panel(
        self,
        expression: str,
        width: float = 8.4,
        height: float = 1.25,
        font_size: int = 42,
        fill_opacity: float = 1.0,
    ) -> VGroup:
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=PAPER_GRAY,
            fill_opacity=fill_opacity,
        )
        equation = self.math(expression, font_size)
        self.fit(equation, width - 0.55, height - 0.28)
        equation.move_to(panel)
        return VGroup(panel, equation)

    def note_panel(
        self,
        title: str,
        lines: Sequence[str],
        width: float = 6.4,
        title_size: int = 26,
        body_size: int = 23,
        max_text_height: float = 2.55,
    ) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.62, max_text_height)
        box_height = max(1.10, content.height + 0.64)
        box = RoundedRectangle(
            width=width,
            height=box_height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

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
        title_text = self.text(title, 34, BOLD)
        self.fit(title_text, SAFE_WIDTH - number_box.width - 0.38, 0.56)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 96:
            midpoint = len(words) // 2
            best = midpoint
            best_gap = 10**9
            for index in range(max(1, midpoint - 5), min(len(words), midpoint + 6)):
                gap = abs(len(" ".join(words[:index])) - len(" ".join(words[index:])))
                if gap < best_gap:
                    best = index
                    best_gap = gap
            subtitle_lines = [" ".join(words[:best]), " ".join(words[best:])]
            subtitle_text = VGroup(*[self.text(line, 20) for line in subtitle_lines])
            subtitle_text.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_text = self.text(subtitle, 21)
        self.fit(subtitle_text, 14.25, 0.70)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)

        new_header = VGroup(title_row, rule)
        old_header = self.header_group
        old_subtitle = self.subtitle_group
        self.header_group = new_header
        self.subtitle_group = subtitle_text

        if old_header is None and old_subtitle is None:
            self.add(new_header, subtitle_text)
        else:
            fading_out = [mob for mob in (old_header, old_subtitle) if mob is not None]
            if fading_out:
                self.play(*[FadeOut(mob) for mob in fading_out], run_time=RUN_QUICK * 0.55)
            self.play(FadeIn(new_header), FadeIn(subtitle_text), run_time=RUN_QUICK * 0.55)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep_family_ids: set[int] = set()
        if keep_header:
            for persistent in (self.header_group, self.subtitle_group):
                if persistent is not None:
                    keep_family_ids.update(id(member) for member in persistent.get_family())
        removable = [mob for mob in self.mobjects if id(mob) not in keep_family_ids]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_NORMAL)
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.03) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -FRAME_WIDTH / 2 + margin or right > FRAME_WIDTH / 2 - margin:
            raise ValueError(f"{label} exceeds horizontal frame bounds: left={left:.3f}, right={right:.3f}")
        if bottom < -FRAME_HEIGHT / 2 + margin or top > FRAME_HEIGHT / 2 - margin:
            raise ValueError(f"{label} exceeds vertical frame bounds: bottom={bottom:.3f}, top={top:.3f}")

    def assert_content_safe(self, mob: Mobject, label: str) -> None:
        self.assert_within_frame(mob, label, margin=0.15)
        if mob.get_top()[1] > CONTENT_TOP_Y:
            raise ValueError(f"{label} overlaps the persistent header zone: top={mob.get_top()[1]:.3f}")
        if mob.get_bottom()[1] < CONTENT_BOTTOM_Y:
            raise ValueError(f"{label} exceeds the safe lower content zone: bottom={mob.get_bottom()[1]:.3f}")

    def figure_panel(
        self,
        figure: Mobject,
        *,
        width: float = 6.2,
        height: float = 4.5,
        title: str | None = None,
        caption: str | None = None,
        inner_margin: float = 0.38,
        title_size: int = 25,
        caption_size: int = 19,
        fill_color=WHITE_FILL,
    ) -> FigurePanel:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=fill_color,
            fill_opacity=1.0,
        )
        title_mob = self.text(title, title_size, BOLD) if title else None
        caption_mob = self.text(caption, caption_size) if caption else None
        available_h = height - 2 * inner_margin
        if title_mob is not None:
            available_h -= 0.55
        if caption_mob is not None:
            available_h -= 0.48
        self.fit(figure, width - 2 * inner_margin, max(0.8, available_h))
        figure.move_to(box)
        components: list[Mobject] = [box, figure]
        if title_mob is not None:
            self.fit(title_mob, width - 0.55, 0.42)
            title_mob.next_to(box.get_top(), DOWN, buff=0.18)
            components.append(title_mob)
            figure.shift(DOWN * 0.18)
        if caption_mob is not None:
            self.fit(caption_mob, width - 0.55, 0.40)
            caption_mob.next_to(box.get_bottom(), UP, buff=0.18)
            components.append(caption_mob)
            figure.shift(UP * 0.12)
        group = VGroup(*components)
        return FigurePanel(group, box, figure, title_mob, caption_mob)

    def split_layout(
        self,
        left: Mobject,
        right: Mobject,
        *,
        left_width: float = 6.7,
        right_width: float = 6.7,
        max_height: float = 5.5,
        gap: float = 0.45,
        center_y: float = -0.40,
    ) -> SplitLayout:
        self.fit(left, left_width, max_height)
        self.fit(right, right_width, max_height)
        left.move_to(LEFT * ((right_width + gap) / 2) + UP * center_y)
        right.move_to(RIGHT * ((left_width + gap) / 2) + UP * center_y)
        group = VGroup(left, right)
        self.fit_content_zone(group, max_width=14.4, max_height=max_height)
        return SplitLayout(group=group, left=left, right=right)

    def process_map(
        self,
        steps: Sequence[tuple[str, str]],
        *,
        card_width: float = 4.3,
        card_height: float = 1.10,
        columns: int = 3,
    ) -> VGroup:
        cards = VGroup()
        for number, text_value in steps:
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
            body = self.text(text_value, 21, BOLD)
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
        self.assert_within_frame(group, "standard opening", margin=0.15)
        self.play(FadeIn(label, shift=UP * 0.18), run_time=RUN_NORMAL)
        self.play(Write(title_mob), run_time=RUN_SLOW)
        self.play(Create(rule), FadeIn(subtitle_mob), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(promise_mob, shift=UP * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str) -> None:
        closing = self.text(sentence, 34, BOLD)
        self.fit(closing, 13.8, 1.2)
        closing.move_to(ORIGIN)
        self.assert_within_frame(closing, "standard closing", margin=0.15)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)


class JPMathClassroomScene(JPClassroomScene):
    pass


def assert_close(actual: float, expected: float, *, tol: float = 1e-10, label: str = "value") -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")
