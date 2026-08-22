"""Standard lesson opening and closing sequences."""
from __future__ import annotations
from manim import *
from .theme import *

class OpeningMixin:
    def standard_opening(self, course_label: str, title: str, subtitle: str, promise: str) -> None:
        label = self.text(course_label, 28, BOLD)
        title_mob = self.text(title, 50, BOLD)
        rule = Line(LEFT*5.5, RIGHT*5.5, color=BLACK_LINE, stroke_width=2.2)
        subtitle_mob = self.text(subtitle, 27)
        promise_mob = self.text(promise, 25, MEDIUM)
        group = VGroup(label, title_mob, rule, subtitle_mob, promise_mob).arrange(DOWN, buff=0.30)
        self.fit(group, 14.4, 6.6)
        self.play(FadeIn(label, shift=UP*0.18), run_time=RUN_NORMAL)
        self.play(Write(title_mob), run_time=RUN_SLOW)
        self.play(Create(rule), FadeIn(subtitle_mob), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(promise_mob, shift=UP*0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(group), run_time=RUN_NORMAL)

    def standard_closing(self, sentence: str) -> None:
        closing = self.text(sentence, 34, BOLD)
        self.fit(closing, 13.8, 1.2).move_to(ORIGIN)
        current = list(self.mobjects)
        if current:
            self.play(*[FadeOut(mob) for mob in current], run_time=RUN_NORMAL)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)
