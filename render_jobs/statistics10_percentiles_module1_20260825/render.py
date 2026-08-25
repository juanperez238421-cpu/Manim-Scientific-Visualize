import importlib.util
import sys
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
SCENE_PATH = HERE / "main.py"

# Load the lesson source under a unique module name. This avoids colliding with
# the inherited Week-1 file that the lesson itself imports as module `main`.
spec = importlib.util.spec_from_file_location("statistics10_percentiles_scene", SCENE_PATH)
scene_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scene_module
spec.loader.exec_module(scene_module)

Statistics10QuartilesDecilesPercentiles = scene_module.Statistics10QuartilesDecilesPercentiles
SCORES = scene_module.SCORES
percentile = scene_module.percentile


class Statistics10QuartilesDecilesPercentilesFinal(Statistics10QuartilesDecilesPercentiles):
    """Validated final scene wrapper with projector-scale interpretation text."""

    def validate_data(self):
        checks = [
            (percentile(SCORES, 25), (64.25, 3.25)),
            (percentile(SCORES, 50), (73.5, 5.5)),
            (percentile(SCORES, 75), (83.0, 7.75)),
            (percentile(SCORES, 80), (85.2, 8.2)),
            (percentile(SCORES, 30), (66.5, 3.7)),
            (percentile(SCORES, 70), (81.2, 7.3)),
        ]
        for got, expected in checks:
            assert abs(got[0] - expected[0]) < 1e-9
            assert abs(got[1] - expected[1]) < 1e-9
        assert abs(percentile([40,45,50,55,60,65,70,75,80], 75)[0] - 70) < 1e-9
        assert abs(percentile([60,65,70,75,80,85,90], 75)[0] - 82.5) < 1e-9
        assert abs(percentile([50,60,70,80,90,100,110], 75)[0] - 95) < 1e-9
        assert abs(percentile([10,12,14,16,18], 75)[0] - 16) < 1e-9

    def example_p80(self):
        self.set_header(6, "WORKED EXAMPLE 2 — FIND P80",
                        "A higher percentile is farther to the right in the ordered list.")
        data = self.data_cards(SCORES, y=1.25, box_w=0.95, color=BLACK).scale(0.92)
        calc = VGroup(
            self.formula_card(r"r=1+9(0.80)=8.20", 6.2, 39),
            self.formula_card(r"P_{80}=84+0.20(90-84)=85.2", 6.2, 36),
        ).arrange(DOWN, buff=0.25).move_to(LEFT*3.65 + DOWN*0.85)
        interp = self.text_card("WHAT DOES 85.2 MEAN?", [
            "About 80% of the scores are at or below 85.2.",
            "A student near P80 performed as well as or better",
            "than about 80% of the observations.",
        ], 6.15, 2.90).move_to(RIGHT*3.72 + DOWN*0.85)
        self.play(FadeIn(data), run_time=0.8)
        self.play(FadeIn(calc[0]), run_time=0.7); self.wait(1.6)
        self.play(FadeIn(calc[1]), run_time=0.7); self.wait(1.8)
        self.play(FadeIn(interp), run_time=0.8); self.wait(4.0)
        self.clear_stage()

    def context_example(self):
        self.set_header(8, "CONTEXT EXAMPLE — REACTION TIMES",
                        "The meaning of a percentile depends on what the variable measures.")
        times = [220,230,235,240,248,255,265,280,300]
        data = self.data_cards(times, y=1.15, box_w=1.02, color=BLACK).scale(0.82)
        lab = self.t("Reaction time in milliseconds — smaller is faster", 25, BOLD, BLACK).next_to(data, UP, buff=0.22)
        calc = VGroup(
            self.formula_card(r"r=1+8(0.75)=7", 5.8, 40),
            self.formula_card(r"P_{75}=x_7=265\text{ ms}", 5.8, 42),
        ).arrange(DOWN, buff=0.25).move_to(LEFT*3.55+DOWN*0.95)
        note = self.text_card("CONCLUSION", [
            "About 75% of the times are at or below 265 ms.",
            "Here a lower time is faster.",
            "Context matters before calling a higher percentile 'better'.",
        ], 6.2, 2.95).move_to(RIGHT*3.7+DOWN*0.95)
        self.play(FadeIn(VGroup(lab,data)), run_time=0.8); self.wait(1.6)
        self.play(FadeIn(calc[0]), run_time=0.7); self.wait(1.4)
        self.play(FadeIn(calc[1]), run_time=0.7); self.wait(1.6)
        self.play(FadeIn(note), run_time=0.8); self.wait(4.0)
        self.clear_stage()
