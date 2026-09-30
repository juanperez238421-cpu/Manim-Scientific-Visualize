"""Reusable classroom panels, figures and split layouts."""
from __future__ import annotations
from collections.abc import Sequence
from pathlib import Path
from manim import *
from .models import FigurePanel, SplitLayout
from .theme import *

class PanelsMixin:
    def formula_panel(self, expression: str, width: float = 8.4, height: float = 1.25,
                      font_size: int = 42, fill_opacity: float = 1.0) -> VGroup:
        panel = RoundedRectangle(width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=PAPER_GRAY, fill_opacity=fill_opacity)
        equation = self.math(expression, font_size)
        self.fit(equation, width - 0.55, height - 0.28).move_to(panel)
        return VGroup(panel, equation)

    def note_panel(self, title: str, lines: Sequence[str], width: float = 6.4,
                   title_size: int = 26, body_size: int = 23, max_text_height: float = 2.55) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.62, max_text_height)
        box = RoundedRectangle(width=width, height=max(1.10, content.height + 0.64), corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1.0)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

    def key_value_panel(self, title: str, pairs: Sequence[tuple[str, str]], width: float = 6.0,
                        label_size: int = 23, value_size: int = 28) -> VGroup:
        rows = VGroup()
        for label, value in pairs:
            lhs = self.text(label, label_size, BOLD)
            rhs = self.math(value, value_size) if any(c in value for c in "_^\\=") else self.text(value, value_size)
            rows.add(VGroup(lhs, rhs).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content = VGroup(self.text(title, 26, BOLD), rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.60, 4.8)
        box = RoundedRectangle(width=width, height=max(1.3, content.height + 0.65), corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, content)

    def figure_panel(self, figure: Mobject, width: float = 6.2, height: float = 4.5,
                     title: str | None = None, caption: str | None = None) -> FigurePanel:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
            stroke_color=LIGHT_GRAY, stroke_width=1.7, fill_color=WHITE_FILL, fill_opacity=1)
        title_mob = self.text(title, 24, BOLD) if title else None
        caption_mob = self.text(caption, 19) if caption else None
        usable_h = height - (0.55 if title else 0.20) - (0.50 if caption else 0.20)
        self.fit(figure, width - 0.45, usable_h)
        figure.move_to(box)
        if title_mob:
            self.fit(title_mob, width - 0.45, 0.4)
            title_mob.next_to(box.get_top(), DOWN, buff=0.18)
        if caption_mob:
            self.fit(caption_mob, width - 0.45, 0.42)
            caption_mob.next_to(box.get_bottom(), UP, buff=0.18)
        group = VGroup(box, figure, *[m for m in (title_mob, caption_mob) if m is not None])
        return FigurePanel(group, box, figure, title_mob, caption_mob)

    def image_panel(self, path: str | Path, **kwargs) -> FigurePanel:
        image = ImageMobject(str(path))
        return self.figure_panel(image, **kwargs)

    def split_layout(self, left: Mobject, right: Mobject, center_y: float = -0.45,
                     gap: float = 0.45, total_width: float = 14.4) -> SplitLayout:
        self.fit(left, (total_width-gap)/2, 5.8)
        self.fit(right, (total_width-gap)/2, 5.8)
        group = VGroup(left, right).arrange(RIGHT, buff=gap).move_to(UP * center_y)
        return SplitLayout(group, left, right)

    def labeled_segment(self, start, end, label: str, font_size: int = 25) -> VGroup:
        line = Line(start, end, color=BLACK_LINE, stroke_width=2.5)
        text = self.math(label, font_size).next_to(line.get_center(), UP, buff=0.12)
        return VGroup(line, text)

    def labeled_dot(self, point, label: str, direction=UP, font_size: int = 24) -> VGroup:
        dot = Dot(point, color=BLACK_LINE, radius=0.06)
        text = self.math(label, font_size).next_to(dot, direction, buff=0.10)
        return VGroup(dot, text)
