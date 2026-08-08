from __future__ import annotations

import importlib.util
from pathlib import Path
from manim import *

BASE = Path(__file__).resolve().parents[1] / "vector_calc_masterclass_v3_20260807" / "main.py"
spec = importlib.util.spec_from_file_location("vector_calc_masterclass_v3", BASE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
V3 = mod.VectorCalculusSurfacesMasterclassV3


class IndividualLessonBase(V3):
    """Autonomous microclass wrapper around the validated V3 visual library."""

    def intro(self, code: str, title: str, subtitle: str, method: str):
        a = self.text(code, 26, BOLD)
        b = self.text(title, 48, BOLD)
        r = Line(LEFT*5.4, RIGHT*5.4, color=BLACK, stroke_width=2)
        c = self.text(subtitle, 27)
        d = self.text(method, 22, MEDIUM)
        g = VGroup(a,b,r,c,d).arrange(DOWN, buff=0.25)
        self.register_fixed(g)
        self.paced_play(FadeIn(a), pause=0.7)
        self.paced_play(Write(b), Create(r), run_time=1.18, pause=1.25)
        self.paced_play(FadeIn(c), pause=1.85)
        self.paced_play(FadeIn(d), pause=2.45)
        self.play(FadeOut(g), run_time=0.86)
        self.clear()

    def outro(self, family: str, checklist):
        title = self.text(f"MÉTODO FINAL · {family.upper()}", 38, BOLD).to_edge(UP, buff=0.55)
        cards = VGroup()
        for i, line in enumerate(checklist, 1):
            box = RoundedRectangle(width=11.4, height=0.72, corner_radius=0.08,
                                   stroke_color="#C8C8C8", stroke_width=1.2,
                                   fill_color=WHITE, fill_opacity=1)
            txt = self.fit(self.text(f"{i}. {line}", 23, BOLD if i in (1,len(checklist)) else MEDIUM), 10.8, 0.46)
            txt.move_to(box)
            cards.add(VGroup(box,txt))
        cards.arrange(DOWN,buff=0.15).move_to(DOWN*0.35)
        self.register_fixed(title,cards)
        self.paced_play(FadeIn(title), pause=1.25)
        for card in cards:
            self.paced_play(FadeIn(card, shift=UP*0.06), run_time=0.52, pause=0.70)
        self.wait(3.40)

    def fade_to_outro(self):
        mobs=list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.70)
        self.clear()
