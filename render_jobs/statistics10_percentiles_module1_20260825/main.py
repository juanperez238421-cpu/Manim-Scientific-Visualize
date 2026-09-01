from manim import *
import math
import os
import sys
from pathlib import Path

# Reuse the exact audited Statistics 10 Week-1 classroom architecture already
# present in this render branch.
BASE_DIR = Path(__file__).resolve().parents[1] / "statistics10_week1_iqr_boxplot_20260824"
sys.path.insert(0, str(BASE_DIR))
from main import Statistics10Week1IQRBoxplot


SCORES = [52, 60, 63, 68, 72, 75, 80, 84, 90, 96]


def percentile(values, k):
    x = sorted(float(v) for v in values)
    r = 1 + (len(x) - 1) * k / 100
    lo, hi = math.floor(r), math.ceil(r)
    if lo == hi:
        return x[lo - 1], r
    d = r - lo
    return x[lo - 1] + d * (x[hi - 1] - x[lo - 1]), r


class Statistics10QuartilesDecilesPercentiles(Statistics10Week1IQRBoxplot):
    """Module 1 — Quartiles, Deciles and Percentiles in Context."""

    def validate_data(self):
        assert percentile(SCORES, 25) == (64.25, 3.25)
        assert percentile(SCORES, 50) == (73.5, 5.5)
        assert percentile(SCORES, 75) == (83.0, 7.75)
        assert percentile(SCORES, 80) == (85.2, 8.2)
        assert percentile(SCORES, 30) == (66.5, 3.7)
        assert percentile(SCORES, 70) == (81.2, 7.3)
        assert percentile([40,45,50,55,60,65,70,75,80], 75)[0] == 70
        assert percentile([60,65,70,75,80,85,90], 75)[0] == 82.5
        assert percentile([50,60,70,80,90,100,110], 75)[0] == 95
        assert percentile([10,12,14,16,18], 75)[0] == 16

    def construct(self):
        self.opening_module()
        self.bridge_quartiles()
        self.meaning_visual()
        self.notation()
        self.convention()
        self.example_p25()
        self.example_p80()
        self.deciles()
        self.context_example()
        self.notebook_content()
        self.practice()
        self.mistakes()
        self.exit_ticket()
        self.summary_module()

    def formula_card(self, expr, width=5.6, fs=40):
        box = RoundedRectangle(width=width, height=1.05, corner_radius=0.12,
                               stroke_color=BLACK, stroke_width=1.8,
                               fill_color="#F7F7F7", fill_opacity=1)
        eq = self.m(expr, fs, BLACK)
        self.fit(eq, width-0.4, 0.78)
        eq.move_to(box)
        return VGroup(box, eq)

    def text_card(self, title, lines, width=6.3, height=2.6):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.13,
                               stroke_color=BLACK, stroke_width=1.8,
                               fill_color=WHITE, fill_opacity=1)
        ttl = self.t(title, 27, BOLD, BLACK)
        body = VGroup(*[self.t(x, 23, NORMAL, BLACK) for x in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        content = VGroup(ttl, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width-0.55, height-0.35)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.28)
        return VGroup(box, content)

    def opening_module(self):
        label = self.t("STATISTICS 10 · MODULE 1", 32, BOLD, BLACK)
        title = self.t("QUARTILES, DECILES AND PERCENTILES", 52, BOLD, BLACK)
        sub = self.t("Position within an ordered dataset", 31, NORMAL, BLACK)
        bridge = self.m(r"Q_1=P_{25}\qquad Q_2=P_{50}\qquad Q_3=P_{75}", 44, BLACK)
        promise = self.t("Meaning first. Calculation second. Interpretation always.", 27, BOLD, BLACK)
        g = VGroup(label, title, sub, bridge, promise).arrange(DOWN, buff=0.34)
        self.fit(g, 14.3, 6.4)
        self.play(FadeIn(label, shift=UP*0.12), Write(title), run_time=1.25)
        self.play(FadeIn(sub), Write(bridge), run_time=1.0)
        self.wait(2.2)
        self.play(FadeIn(promise), run_time=0.7)
        self.wait(3.0)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.8)

    def bridge_quartiles(self):
        self.set_header(1, "FROM BOXPLOTS TO POSITION MEASURES",
                        "The quartiles you already use are special percentiles.")
        relation = VGroup(
            self.formula_card(r"Q_1=P_{25}", 3.7, 42),
            self.formula_card(r"Q_2=P_{50}", 3.7, 42),
            self.formula_card(r"Q_3=P_{75}", 3.7, 42),
        ).arrange(RIGHT, buff=0.35).shift(UP*0.55)
        note = self.text_card("READ THE CONNECTION", [
            "Q1 marks the 25% position.",
            "Q2 is the median: the 50% position.",
            "Q3 marks the 75% position.",
        ], width=9.8, height=2.25).shift(DOWN*1.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in relation], lag_ratio=0.15), run_time=1.4)
        self.wait(2.0)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(3.5)
        self.clear_stage()

    def meaning_visual(self):
        self.set_header(2, "MEANING FIRST: DIVIDE THE ORDERED DATA",
                        "Quartiles, deciles and percentiles use the same idea at different resolutions.")
        rows = []
        specs = [(4, "QUARTILE", "4 parts · 25% each"), (10, "DECILE", "10 parts · 10% each")]
        for parts, name, caption in specs:
            cells = VGroup(*[Rectangle(width=10.5/parts, height=0.70, stroke_color=BLACK,
                                       stroke_width=1.5, fill_color=WHITE, fill_opacity=1) for _ in range(parts)])
            cells.arrange(RIGHT, buff=0)
            lab = self.t(f"{name} — {caption}", 27, BOLD, BLACK)
            rows.append(VGroup(lab, cells).arrange(DOWN, buff=0.18))
        pbar = NumberLine(x_range=[0,100,10], length=10.5, include_numbers=True,
                          font_size=24, color=BLACK, include_tip=False)
        prow = VGroup(self.t("PERCENTILE — 100 position steps", 27, BOLD, BLACK), pbar).arrange(DOWN, buff=0.20)
        g = VGroup(rows[0], rows[1], prow).arrange(DOWN, buff=0.55).move_to(DOWN*0.35)
        self.play(FadeIn(rows[0]), run_time=0.8); self.wait(1.5)
        self.play(FadeIn(rows[1]), run_time=0.8); self.wait(1.5)
        self.play(FadeIn(prow), run_time=0.8); self.wait(3.2)
        self.clear_stage()

    def notation(self):
        self.set_header(3, "NOTATION IS A POSITION LANGUAGE",
                        "The subscript names the requested position; it is not the observed data value.")
        cards = VGroup(
            self.text_card("QUARTILES", ["Qk", "Q1, Q2, Q3", "4 parts"], 4.1, 2.45),
            self.text_card("DECILES", ["Dk", "D3, D7", "10 parts"], 4.1, 2.45),
            self.text_card("PERCENTILES", ["Pk", "P25, P80", "100 parts"], 4.1, 2.45),
        ).arrange(RIGHT, buff=0.35).shift(UP*0.20)
        bridge = self.formula_card(r"D_3=P_{30}\qquad D_7=P_{70}", 8.0, 42).next_to(cards, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.15), run_time=1.3)
        self.wait(2.0)
        self.play(FadeIn(bridge), run_time=0.8)
        self.wait(3.0)
        self.clear_stage()

    def convention(self):
        self.set_header(4, "ONE CLASS CONVENTION — DO NOT MIX METHODS",
                        "Different software can use different percentile rules. This module uses one inclusive linear rule.")
        left = self.text_card("BEFORE THE FORMULA", [
            "1. Order the data.",
            "2. Choose the target percent.",
            "3. Locate its position.",
            "4. Interpolate only if needed.",
        ], 6.2, 3.4).move_to(LEFT*3.55 + DOWN*0.35)
        formula = self.formula_card(r"r=1+(n-1)\frac{k}{100}", 6.2, 46).move_to(RIGHT*3.55 + UP*0.45)
        right = self.text_card("FOR Pk", ["r = position", "n = number of observations", "k = percentile number"],
                               6.2, 2.05).next_to(formula, DOWN, buff=0.35)
        self.play(FadeIn(left), run_time=0.8); self.wait(2.2)
        self.play(FadeIn(formula), run_time=0.8); self.wait(2.0)
        self.play(FadeIn(right), run_time=0.8); self.wait(3.5)
        self.clear_stage()

    def example_p25(self):
        self.set_header(5, "WORKED EXAMPLE 1 — FIND P25",
                        "Every calculation ends with a statistical interpretation.")
        data = self.data_cards(SCORES, y=1.25, box_w=0.95, color=BLACK).scale(0.92)
        steps = VGroup(
            self.formula_card(r"r=1+9(0.25)=3.25", 6.3, 39),
            self.formula_card(r"P_{25}=63+0.25(68-63)", 6.3, 37),
            self.formula_card(r"P_{25}=64.25", 6.3, 45),
        ).arrange(DOWN, buff=0.22).move_to(LEFT*3.65 + DOWN*1.05)
        interp = self.text_card("INTERPRET", [
            "About 25% of the scores are at or below 64.25.",
            "This is the same position idea as Q1.",
        ], 6.1, 2.4).move_to(RIGHT*3.75 + DOWN*1.05)
        self.play(FadeIn(data), run_time=0.8); self.wait(1.6)
        for s in steps:
            self.play(FadeIn(s), run_time=0.65); self.wait(1.3)
        self.play(FadeIn(interp), run_time=0.8); self.wait(3.7)
        self.clear_stage()

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
            "A student near P80 performed as well as or better than about 80% of the observations.",
        ], 6.15, 2.75).move_to(RIGHT*3.72 + DOWN*0.85)
        self.play(FadeIn(data), run_time=0.8)
        self.play(FadeIn(calc[0]), run_time=0.7); self.wait(1.6)
        self.play(FadeIn(calc[1]), run_time=0.7); self.wait(1.8)
        self.play(FadeIn(interp), run_time=0.8); self.wait(4.0)
        self.clear_stage()

    def deciles(self):
        self.set_header(7, "DECILES — SAME METHOD, NEW POSITION",
                        "Convert the decile to a percentile and keep the same calculation rule.")
        left = VGroup(self.formula_card(r"D_3=P_{30}", 5.9, 42),
                      self.formula_card(r"r=1+9(0.30)=3.70", 5.9, 37),
                      self.formula_card(r"D_3=63+0.70(68-63)=66.5", 5.9, 34)).arrange(DOWN, buff=0.24)
        right = VGroup(self.formula_card(r"D_7=P_{70}", 5.9, 42),
                       self.formula_card(r"r=1+9(0.70)=7.30", 5.9, 37),
                       self.formula_card(r"D_7=80+0.30(84-80)=81.2", 5.9, 34)).arrange(DOWN, buff=0.24)
        left.move_to(LEFT*3.45 + DOWN*0.55); right.move_to(RIGHT*3.45 + DOWN*0.55)
        self.play(FadeIn(left[0]), FadeIn(right[0]), run_time=0.8)
        for i in [1,2]:
            self.play(FadeIn(left[i]), FadeIn(right[i]), run_time=0.75); self.wait(1.7)
        self.wait(3.3)
        self.clear_stage()

    def context_example(self):
        self.set_header(8, "CONTEXT EXAMPLE — REACTION TIMES",
                        "The meaning of a percentile depends on what the variable measures.")
        times = [220,230,235,240,248,255,265,280,300]
        data = self.data_cards(times, y=1.15, box_w=1.02, color=BLACK).scale(0.82)
        lab = self.t("Reaction time in milliseconds — smaller is faster", 25, BOLD, BLACK).next_to(data, UP, buff=0.22)
        calc = VGroup(self.formula_card(r"r=1+8(0.75)=7", 5.8, 40),
                      self.formula_card(r"P_{75}=x_7=265\text{ ms}", 5.8, 42)).arrange(DOWN, buff=0.25).move_to(LEFT*3.55+DOWN*0.95)
        note = self.text_card("CONCLUSION", [
            "About 75% of the times are at or below 265 ms.",
            "Here a lower time is faster, so context matters before calling a higher percentile 'better'.",
        ], 6.2, 2.75).move_to(RIGHT*3.7+DOWN*0.95)
        self.play(FadeIn(VGroup(lab,data)), run_time=0.8); self.wait(1.6)
        self.play(FadeIn(calc[0]), run_time=0.7); self.wait(1.4)
        self.play(FadeIn(calc[1]), run_time=0.7); self.wait(1.6)
        self.play(FadeIn(note), run_time=0.8); self.wait(4.0)
        self.clear_stage()

    def notebook_content(self):
        self.set_header(9, "COPY TO NOTEBOOK",
                        "Keep only the definitions, one rule, and interpretation sentence stems.")
        left = self.text_card("POSITION MEASURES", [
            "Quartile -> 4 parts", "Decile -> 10 parts", "Percentile -> 100 parts",
            "Q1=P25, Q2=P50, Q3=P75", "D3=P30, D7=P70",
        ], 6.3, 4.1).move_to(LEFT*3.55+DOWN*0.35)
        formula = self.formula_card(r"r=1+(n-1)\frac{k}{100}", 6.1, 42).move_to(RIGHT*3.55+UP*0.65)
        stems = self.text_card("WRITE THE MEANING", [
            "About k% are at or below ...", "This percentile is higher/lower than ...",
            "In this context, this position means ...",
        ], 6.1, 2.5).next_to(formula, DOWN, buff=0.38)
        self.play(FadeIn(left), run_time=0.8); self.wait(4.8)
        self.play(FadeIn(formula), FadeIn(stems), run_time=0.9); self.wait(5.0)
        self.clear_stage()

    def practice(self):
        self.set_header(10, "STUDENT PRACTICE — NO SOLUTIONS ON THIS SCREEN",
                        "Each numerical task must finish with an interpretation sentence.")
        prompts = [
            ("LEVEL 1 — RECOGNITION", "Match Q2, D7 and P80 with 50%, 70% and 80%."),
            ("LEVEL 2 — CALCULATION", "40,45,50,55,60,65,70,75,80: find P75 and interpret."),
            ("LEVEL 3 — INTERPRETATION", "P30 = 58. Write one correct statistical sentence."),
            ("LEVEL 4 — COMPARISON", "A: 60,65,70,75,80,85,90 | B: 50,60,70,80,90,100,110. Compare P75."),
            ("LEVEL 5 — APPLIED", "An exam report gives P80 = 86. Explain the position in context."),
        ]
        cards = VGroup(*[self.text_card(a,[b],12.8,0.93) for a,b in prompts]).arrange(DOWN,buff=0.12).move_to(DOWN*0.40)
        self.fit(cards, 13.2, 5.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.05) for c in cards], lag_ratio=0.12), run_time=1.5)
        self.wait(6.0)
        self.clear_stage()

    def mistakes(self):
        self.set_header(11, "COMMON MISTAKES",
                        "A correct-looking calculation can still hide a conceptual error.")
        labels = ["ORDER DATA FIRST", "DO NOT MIX CONVENTIONS", "P80 IS NOT THE VALUE 80",
                  "INTERPOLATE WHEN NEEDED", "VALUE != PERCENTILE RANK", "ALWAYS INTERPRET IN CONTEXT"]
        cards = VGroup(*[self.text_card(str(i+1), [txt], 4.25, 1.35) for i,txt in enumerate(labels)])
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.30,0.30)).move_to(DOWN*0.25)
        nextm = self.t("Next module: Percentile Value vs Percentile Rank", 27, BOLD, BLACK).next_to(cards, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.10), run_time=1.5)
        self.wait(3.0)
        self.play(FadeIn(nextm), run_time=0.7); self.wait(3.5)
        self.clear_stage()

    def exit_ticket(self):
        self.set_header(12, "EXIT TICKET — 5 MINUTES",
                        "Conceptual · calculation · interpretation")
        q1 = self.text_card("1. CONCEPTUAL", ["What does D7 mean in an ordered dataset?"], 12.4, 1.45)
        q2 = self.text_card("2. CALCULATION", ["10, 12, 14, 16, 18: find P75 using our class convention."], 12.4, 1.45)
        q3 = self.text_card("3. INTERPRETATION", ["In an exam, P80 = 86 points. Explain this in one sentence."], 12.4, 1.45)
        g = VGroup(q1,q2,q3).arrange(DOWN,buff=0.22).move_to(DOWN*0.35)
        self.play(LaggedStart(*[FadeIn(q, shift=UP*0.08) for q in g], lag_ratio=0.18), run_time=1.3)
        self.wait(6.0)
        self.clear_stage()

    def summary_module(self):
        self.set_header(13, "REPRODUCIBLE METHOD",
                        "Meaning first; calculation second; interpretation always.")
        steps = ["1 ORDER THE DATA", "2 IDENTIFY Q, D OR P", "3 CONVERT TO A PERCENT",
                 "4 LOCATE THE POSITION", "5 INTERPOLATE IF NEEDED", "6 INTERPRET IN CONTEXT"]
        cards = VGroup(*[self.text_card(str(i+1), [s.split(' ',1)[1]], 4.25, 1.35) for i,s in enumerate(steps)])
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.30,0.30)).move_to(UP*0.10)
        bridge = self.formula_card(r"Q_1=P_{25}\qquad Q_2=P_{50}\qquad Q_3=P_{75}", 9.6, 42).next_to(cards, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.10), run_time=1.5)
        self.wait(3.0)
        self.play(FadeIn(bridge), run_time=0.8); self.wait(4.5)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.8)
        final = self.t("Position tells us where a value sits. Interpretation tells us why that position matters.", 34, BOLD, BLACK)
        self.fit(final, 13.6, 1.4)
        self.play(FadeIn(final), run_time=1.0); self.wait(4.5); self.play(FadeOut(final), run_time=0.8)
