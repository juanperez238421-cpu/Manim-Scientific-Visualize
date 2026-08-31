from manim import *
import os
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
INK = BLACK
MUTED = "#666666"
PAPER = "#F7F7F7"
ACCENT = "#2457C5"
ACCENT2 = "#15803D"
ALERT = "#B91C1C"
GOLD = "#A16207"


class Statistics10Week1IQRBoxplot(MovingCameraScene):
    """Grade 10 Statistics — Week 1: IQR & boxplot consolidation."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.subheader = None
        self.validate_data()

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def validate_data(self):
        regular = np.array([2,3,4,5,6,7,8,9], dtype=float)
        extreme = np.array([2,3,4,5,6,7,8,20], dtype=float)
        assert abs(float(np.var(regular)) - 5.25) < 1e-12
        assert abs(float(np.var(extreme)) - 28.109375) < 1e-12
        assert self.quartiles([2,3,4,5,6,7,8,20]) == (3.5, 5.5, 7.5)
        assert self.quartiles([3,4,5,6,7,8,10,14]) == (4.5, 6.5, 9.0)
        assert self.quartiles([4,5,5,6,7,8,9,15]) == (5.0, 6.5, 8.5)

    @staticmethod
    def quartiles(values):
        v = sorted(values)
        n = len(v)
        lo, hi = v[:n//2], v[n//2:]
        q2 = (v[n//2-1] + v[n//2]) / 2
        m = len(lo)
        q1 = (lo[m//2-1] + lo[m//2]) / 2
        q3 = (hi[m//2-1] + hi[m//2]) / 2
        return float(q1), float(q2), float(q3)

    def t(self, text, size=30, weight=NORMAL, color=INK):
        return Text(text, font_size=size, weight=weight, color=color, line_spacing=0.9)

    def m(self, expression, size=40, color=INK):
        return MathTex(expression, font_size=size, color=color)

    def fit(self, mob, max_w=14.4, max_h=6.0):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def set_header(self, num, title, subtitle):
        nbox = RoundedRectangle(width=0.76, height=0.58, corner_radius=0.10,
                                stroke_color=INK, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        ntxt = self.t(f"{num:02d}", 24, BOLD).move_to(nbox)
        title_m = self.t(title, 36, BOLD)
        row = VGroup(VGroup(nbox, ntxt), title_m).arrange(RIGHT, buff=0.28)
        row.to_edge(UP, buff=0.18).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT*7.45, RIGHT*7.45, stroke_color="#D0D0D0", stroke_width=2)
        rule.next_to(row, DOWN, buff=0.08)
        sub = self.t(subtitle, 23, NORMAL, MUTED)
        self.fit(sub, 14.3, 0.75)
        sub.next_to(rule, DOWN, buff=0.10).align_to(row, LEFT)
        new_h, new_s = VGroup(row, rule), sub
        if self.header is None:
            self.add(new_h, new_s)
        else:
            self.play(ReplacementTransform(self.header, new_h),
                      ReplacementTransform(self.subheader, new_s), run_time=0.6)
        self.header, self.subheader = new_h, new_s

    def clear_stage(self):
        keep = set()
        for root in (self.header, self.subheader):
            if root is not None:
                keep.update(id(x) for x in root.get_family())
        mobs = [x for x in self.mobjects if id(x) not in keep]
        if mobs:
            self.play(*[FadeOut(x) for x in mobs], run_time=0.65)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def panel(self, width, height, title=None):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.14,
                               stroke_color=INK, stroke_width=1.8,
                               fill_color=PAPER, fill_opacity=1)
        if not title:
            return box
        label = self.t(title, 25, BOLD).move_to(box.get_top() + DOWN*0.32)
        return VGroup(box, label)

    def data_cards(self, values, y=0.5, box_w=0.84, color=ACCENT):
        cards = VGroup()
        for value in values:
            sq = RoundedRectangle(width=box_w, height=0.78, corner_radius=0.09,
                                  stroke_color=color, stroke_width=2,
                                  fill_color=WHITE, fill_opacity=1)
            num = self.m(str(value), 34).move_to(sq)
            cards.add(VGroup(sq, num))
        cards.arrange(RIGHT, buff=0.12).move_to([0, y, 0])
        return cards

    def number_line(self, x_min=0, x_max=22, length=12.8, step=2):
        return NumberLine(x_range=[x_min, x_max, step], length=length,
                          include_numbers=True, font_size=26, color=INK,
                          stroke_width=2, include_tip=False)

    def make_boxplot(self, q1, median, q3, wmin, wmax, outliers=(),
                     x_min=0, x_max=22, length=12.0, color=ACCENT,
                     label="", scale_height=0.72):
        line = self.number_line(x_min, x_max, length, step=2)
        p = line.n2p
        y0 = 0.55
        box = Rectangle(width=max(0.01, p(q3)[0]-p(q1)[0]), height=scale_height,
                        stroke_color=color, stroke_width=3,
                        fill_color=color, fill_opacity=0.08)
        box.move_to([(p(q1)[0]+p(q3)[0])/2, y0, 0])
        med = Line([p(median)[0], y0-scale_height/2, 0], [p(median)[0], y0+scale_height/2, 0],
                   color=ALERT, stroke_width=4)
        lw = Line([p(wmin)[0], y0, 0], [p(q1)[0], y0, 0], color=color, stroke_width=3)
        rw = Line([p(q3)[0], y0, 0], [p(wmax)[0], y0, 0], color=color, stroke_width=3)
        cap_l = Line([p(wmin)[0], y0-0.25, 0], [p(wmin)[0], y0+0.25, 0], color=color, stroke_width=3)
        cap_r = Line([p(wmax)[0], y0-0.25, 0], [p(wmax)[0], y0+0.25, 0], color=color, stroke_width=3)
        dots = VGroup(*[Dot([p(v)[0], y0, 0], radius=0.09, color=ALERT) for v in outliers])
        title = self.t(label, 24, BOLD, color).next_to(line, UP, buff=0.55).align_to(line, LEFT) if label else VGroup()
        return VGroup(line, lw, rw, cap_l, cap_r, box, med, dots, title)

    def step_card(self, num, title, body, width=4.25):
        box = RoundedRectangle(width=width, height=1.55, corner_radius=0.14,
                               stroke_color=INK, stroke_width=1.6,
                               fill_color=WHITE, fill_opacity=1)
        tag = Circle(radius=0.23, stroke_color=ACCENT, stroke_width=2, fill_opacity=0)
        n = self.t(str(num), 22, BOLD, ACCENT).move_to(tag)
        heading = self.t(title, 24, BOLD)
        body_m = self.t(body, 20, NORMAL, MUTED)
        self.fit(body_m, width-0.55, 0.52)
        content = VGroup(VGroup(tag,n), heading, body_m).arrange(DOWN, buff=0.08)
        content.move_to(box)
        return VGroup(box, content)

    def construct(self):
        self.opening()
        self.bridge_variance_iqr()
        self.quartiles_and_iqr()
        self.fences_and_outlier()
        self.build_boxplot()
        self.interpret_shape()
        self.compare_groups()
        self.guided_practice()
        self.summary()

    def opening(self):
        top = self.t("STATISTICS 10 · WEEK 1", 31, BOLD, ACCENT)
        title = self.t("IQR & BOXPLOT CONSOLIDATION", 56, BOLD)
        subtitle = self.t("Median · Quartiles · IQR · 1.5 IQR fences · Outliers · Comparison", 27, NORMAL, MUTED)
        goals = VGroup(
            self.step_card(1, "CALCULATE", "Q1, median, Q3 and IQR"),
            self.step_card(2, "BUILD", "A boxplot line by line"),
            self.step_card(3, "INTERPRET", "Center, spread, shape and outliers"),
        ).arrange(RIGHT, buff=0.35)
        VGroup(top, title, subtitle, goals).arrange(DOWN, buff=0.34).move_to(DOWN*0.05)
        self.play(FadeIn(top, shift=UP*0.12), Write(title), run_time=1.25)
        self.play(FadeIn(subtitle), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.10) for c in goals], lag_ratio=0.16), run_time=1.25)
        self.wait(3.0)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.8)

    def bridge_variance_iqr(self):
        self.set_header(1, "FROM VARIANCE TO IQR", "Two measures of spread react differently when an extreme value appears.")
        left = self.panel(6.6, 4.7, "DATASET WITHOUT EXTREME VALUE")
        right = self.panel(6.6, 4.7, "REPLACE 9 WITH 20")
        left.move_to(LEFT*3.55 + DOWN*0.50)
        right.move_to(RIGHT*3.55 + DOWN*0.50)
        a = self.data_cards([2,3,4,5,6,7,8,9], y=0).scale(0.74).move_to(left[0]).shift(UP*0.55)
        b = self.data_cards([2,3,4,5,6,7,8,20], y=0, color=ALERT).scale(0.74).move_to(right[0]).shift(UP*0.55)
        var_a = self.m(r"\sigma^2=5.25", 40).next_to(a, DOWN, buff=0.48)
        var_b = self.m(r"\sigma^2=28.11", 40, ALERT).next_to(b, DOWN, buff=0.48)
        iqr_a = self.m(r"IQR=4", 40, ACCENT2).next_to(var_a, DOWN, buff=0.24)
        iqr_b = self.m(r"IQR=4", 40, ACCENT2).next_to(var_b, DOWN, buff=0.24)
        takeaway = self.t("Variance reacts strongly to distance from the mean.  IQR tracks the middle 50%.", 29, BOLD).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        self.play(FadeIn(a), FadeIn(b), run_time=0.9)
        self.play(Write(var_a), Write(var_b), run_time=0.9)
        self.play(Write(iqr_a), Write(iqr_b), run_time=0.9)
        self.play(FadeIn(takeaway, shift=UP*0.08), run_time=0.8)
        self.wait(3.2)
        self.clear_stage()

    def quartiles_and_iqr(self):
        self.set_header(2, "ORDER → QUARTILES → IQR", "Quartiles are positional measures: always sort the data before locating Q1, Q2 and Q3.")
        unsorted = self.data_cards([7,2,20,5,3,8,4,6], y=1.0)
        sorted_cards = self.data_cards([2,3,4,5,6,7,8,20], y=0.8, color=ACCENT2)
        caption = self.t("Original order", 24, NORMAL, MUTED).next_to(unsorted, DOWN, buff=0.18)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in unsorted], lag_ratio=0.08), FadeIn(caption), run_time=1.3)
        self.wait(1.5)
        self.play(ReplacementTransform(unsorted, sorted_cards), FadeOut(caption), run_time=1.1)
        q1box = SurroundingRectangle(VGroup(sorted_cards[1], sorted_cards[2]), color=GOLD, buff=0.10, stroke_width=3)
        q2box = SurroundingRectangle(VGroup(sorted_cards[3], sorted_cards[4]), color=ALERT, buff=0.10, stroke_width=3)
        q3box = SurroundingRectangle(VGroup(sorted_cards[5], sorted_cards[6]), color=ACCENT2, buff=0.10, stroke_width=3)
        q1 = self.m(r"Q_1=\frac{3+4}{2}=3.5", 38, GOLD).move_to(DOWN*1.45 + LEFT*3.6)
        q2 = self.m(r"Q_2=\frac{5+6}{2}=5.5", 38, ALERT).move_to(DOWN*1.45)
        q3 = self.m(r"Q_3=\frac{7+8}{2}=7.5", 38, ACCENT2).move_to(DOWN*1.45 + RIGHT*3.6)
        iqr = self.m(r"IQR=Q_3-Q_1=7.5-3.5=4", 47, ACCENT).to_edge(DOWN, buff=0.35)
        self.play(Create(q2box), Write(q2), run_time=0.8); self.wait(1.0)
        self.play(Create(q1box), Write(q1), run_time=0.8); self.wait(1.0)
        self.play(Create(q3box), Write(q3), run_time=0.8); self.wait(1.0)
        self.play(Write(iqr), run_time=1.0)
        self.wait(3.4)
        self.clear_stage()

    def fences_and_outlier(self):
        self.set_header(3, "1.5 IQR FENCES", "The fences are decision thresholds for potential outliers; they are not the whisker endpoints themselves.")
        formula = VGroup(
            self.m(r"LF=Q_1-1.5(IQR)=3.5-1.5(4)=-2.5", 42),
            self.m(r"UF=Q_3+1.5(IQR)=7.5+1.5(4)=13.5", 42),
        ).arrange(DOWN, buff=0.34).move_to(UP*1.2)
        self.play(Write(formula[0]), run_time=0.95); self.wait(1.0)
        self.play(Write(formula[1]), run_time=0.95); self.wait(1.0)
        decision = VGroup(
            self.t("Regular values", 27, BOLD, ACCENT2), self.m(r"2,3,4,5,6,7,8", 37),
            self.t("Potential outlier", 27, BOLD, ALERT), self.m(r"20>13.5", 42, ALERT),
        ).arrange(DOWN, buff=0.16).move_to(DOWN*1.05)
        self.play(FadeIn(decision, shift=UP*0.10), run_time=1.0)
        note = self.t("Therefore the right whisker stops at 8, and 20 is plotted as a separate point.", 29, BOLD).to_edge(DOWN, buff=0.36)
        self.play(FadeIn(note), run_time=0.75)
        self.wait(3.6)
        self.clear_stage()

    def build_boxplot(self):
        self.set_header(4, "BUILD THE BOXPLOT LINE BY LINE", "Use the five-number structure, then separate any value beyond the fences.")
        line = self.number_line(0, 22, 13.2, 2).shift(DOWN*0.65)
        self.play(Create(line), run_time=1.0)
        y0 = 0.25
        p = line.n2p
        box = Rectangle(width=p(7.5)[0]-p(3.5)[0], height=1.05,
                        stroke_color=ACCENT, stroke_width=4, fill_color=ACCENT, fill_opacity=0.08)
        box.move_to([(p(3.5)[0]+p(7.5)[0])/2, y0, 0])
        med = Line([p(5.5)[0], y0-0.525, 0], [p(5.5)[0], y0+0.525, 0], color=ALERT, stroke_width=5)
        whisk_l = Line([p(2)[0], y0, 0], [p(3.5)[0], y0, 0], color=ACCENT, stroke_width=4)
        whisk_r = Line([p(7.5)[0], y0, 0], [p(8)[0], y0, 0], color=ACCENT, stroke_width=4)
        cap_l = Line([p(2)[0], y0-0.34, 0], [p(2)[0], y0+0.34, 0], color=ACCENT, stroke_width=4)
        cap_r = Line([p(8)[0], y0-0.34, 0], [p(8)[0], y0+0.34, 0], color=ACCENT, stroke_width=4)
        out = Dot([p(20)[0], y0, 0], radius=0.12, color=ALERT)
        qlabels = VGroup(
            self.m(r"Q_1=3.5", 30, GOLD).next_to([p(3.5)[0], y0+0.6, 0], UP, buff=0.10),
            self.m(r"Q_2=5.5", 30, ALERT).next_to([p(5.5)[0], y0+0.6, 0], UP, buff=0.10),
            self.m(r"Q_3=7.5", 30, ACCENT2).next_to([p(7.5)[0], y0+0.6, 0], UP, buff=0.10),
        )
        step = self.t("1. Draw the box from Q1 to Q3", 29, BOLD, ACCENT).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(step), Create(box), run_time=0.9); self.wait(1.3)
        step2 = self.t("2. Draw the median inside the box", 29, BOLD, ALERT).move_to(step)
        self.play(ReplacementTransform(step, step2), Create(med), run_time=0.8); self.wait(1.3)
        step3 = self.t("3. Add whiskers to the smallest and largest regular values", 29, BOLD, ACCENT2).move_to(step2)
        self.play(ReplacementTransform(step2, step3), Create(whisk_l), Create(whisk_r), Create(cap_l), Create(cap_r), run_time=0.9); self.wait(1.3)
        step4 = self.t("4. Plot 20 separately because it exceeds the upper fence", 29, BOLD, ALERT).move_to(step3)
        self.play(ReplacementTransform(step3, step4), GrowFromCenter(out), FadeIn(qlabels), run_time=0.9)
        self.wait(4.0)
        self.clear_stage()

    def interpret_shape(self):
        self.set_header(5, "READ THE BOXPLOT AS A SENTENCE", "A calculation is incomplete until you state what the graph says about center, spread, shape and unusual values.")
        bp = self.make_boxplot(3.5,5.5,7.5,2,8,[20], label="GROUP A", color=ACCENT)
        bp.move_to(UP*0.8)
        self.play(FadeIn(bp), run_time=1.0)
        cards = VGroup(
            self.step_card(1, "CENTER", "Median = 5.5", 3.35),
            self.step_card(2, "MIDDLE SPREAD", "IQR = 4", 3.35),
            self.step_card(3, "UNUSUAL VALUE", "20 is a high outlier", 3.35),
            self.step_card(4, "SHAPE CLUE", "Extreme value on the right", 3.35),
        ).arrange(RIGHT, buff=0.20).scale(0.96).to_edge(DOWN, buff=0.42)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.14), run_time=1.5)
        self.wait(3.8)
        self.clear_stage()

    def compare_groups(self):
        self.set_header(6, "COMPARE TWO GROUPS ON THE SAME SCALE", "Use the same axis, then compare median, IQR, whiskers and outliers before writing a contextual conclusion.")
        a = self.make_boxplot(3.5,5.5,7.5,2,8,[20], label="GROUP A", color=ACCENT).scale(0.90).move_to(UP*1.05)
        b = self.make_boxplot(4.5,6.5,9.0,3,14,[], label="GROUP B", color=ACCENT2).scale(0.90).move_to(DOWN*1.18)
        self.play(FadeIn(a), run_time=1.0)
        self.play(FadeIn(b), run_time=1.0)
        conclusion = self.t("Group B has the higher median (6.5 vs 5.5) and a slightly larger IQR (4.5 vs 4).\nGroup A has a high outlier at 20; Group B has a longer upper whisker but no outlier.", 28, BOLD)
        self.fit(conclusion, 14.1, 1.05)
        conclusion.to_edge(DOWN, buff=0.25)
        panel = RoundedRectangle(width=14.5, height=1.25, corner_radius=0.12,
                                 stroke_color=INK, stroke_width=1.5, fill_color=PAPER, fill_opacity=1).move_to(conclusion)
        self.play(FadeIn(panel), FadeIn(conclusion), run_time=0.9)
        self.wait(4.2)
        self.clear_stage()

    def guided_practice(self):
        self.set_header(7, "YOU TRY — THEN CHECK", "Calculate the quartiles, IQR and fences before deciding whether 15 is an outlier.")
        data = self.data_cards([4,5,5,6,7,8,9,15], y=0.95, color=ACCENT)
        prompt = self.t("Find Q1, median, Q3, IQR, lower fence and upper fence.", 31, BOLD).next_to(data, DOWN, buff=0.45)
        timer = self.t("PAUSE THE VIDEO · WORK IN YOUR NOTEBOOK", 28, BOLD, ALERT).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(data), FadeIn(prompt), FadeIn(timer), run_time=0.9)
        self.wait(6.0)
        self.play(FadeOut(prompt), FadeOut(timer), run_time=0.6)
        solution = VGroup(
            self.m(r"Q_1=5,\quad Q_2=6.5,\quad Q_3=8.5", 40),
            self.m(r"IQR=8.5-5=3.5", 43, ACCENT),
            self.m(r"LF=5-1.5(3.5)=-0.25", 38),
            self.m(r"UF=8.5+1.5(3.5)=13.75", 38),
            self.m(r"15>13.75\;\Rightarrow\;15\text{ is an outlier}", 43, ALERT),
        ).arrange(DOWN, buff=0.22).move_to(DOWN*0.75)
        self.play(LaggedStart(*[Write(x) for x in solution], lag_ratio=0.22), run_time=2.5)
        self.wait(4.0)
        self.clear_stage()

    def summary(self):
        self.set_header(8, "WEEK 1 METHOD", "Repeat the same reasoning every time: organize, calculate, classify, draw, and interpret.")
        cards = VGroup(
            self.step_card(1, "ORDER", "Sort smallest → largest", 2.62),
            self.step_card(2, "QUARTILES", "Find Q1, Q2, Q3", 2.62),
            self.step_card(3, "IQR", "Q3 − Q1", 2.62),
            self.step_card(4, "FENCES", "Q1 − 1.5IQR; Q3 + 1.5IQR", 2.62),
            self.step_card(5, "BOXPLOT", "Box, median, whiskers, outliers", 2.62),
        ).arrange(RIGHT, buff=0.18).move_to(UP*0.65)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.12), run_time=1.7)
        closing = self.t("Final habit: after every calculation, write one sentence about center, spread, shape and unusual values.", 31, BOLD)
        self.fit(closing, 13.8, 0.85)
        closing.move_to(DOWN*1.55)
        self.play(FadeIn(closing), run_time=0.9)
        exitq = self.t("EXIT TICKET: Which group is more consistent — and what evidence from the boxplot supports your answer?", 27, BOLD, ACCENT)
        self.fit(exitq, 13.8, 0.75)
        exitq.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(exitq), run_time=0.8)
        self.wait(5.0)
