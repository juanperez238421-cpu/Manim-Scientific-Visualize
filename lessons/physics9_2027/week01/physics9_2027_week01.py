#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 · 2027 · Quarter 1 · Week 1, two ManimCE classroom videos.

Based on the IJR Class Planner (19–22 Jan 2027).
Visual lineage: House Extrusion 3D step-by-step technical Manim presentation.
2D adaptation: white drafting board, measured lines, parametric demonstrations,
big readable lettering, visible question→observation→measurement progression.

ManimCE 0.20.1; each class is independently renderable in 16:9.
manim -pql physics9_2027_week01.py Physics9Week1Class1
manim -pqh physics9_2027_week01.py Physics9Week1Class1
manim -pql physics9_2027_week01.py Physics9Week1Class2
manim -pqh physics9_2027_week01.py Physics9Week1Class2
"""
from __future__ import annotations
from manim import *
import numpy as np

config.background_color = WHITE
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30

INK = "#18252B"
FOREST = "#256952"
BLUEPRINT = "#246E92"
MID = "#66777C"
LINE = "#D8E1DF"
PAPER = "#F5F8F7"
AMBER = "#B86F26"
FONT = "DejaVu Sans"


def tx(message: str, size: int = 30, color: str = INK, bold: bool = False):
    return Text(message, font=FONT, font_size=size,
                weight=BOLD if bold else NORMAL, color=color)


def rect(width, height, fill=PAPER, edge=LINE, radius=0.14):
    return RoundedRectangle(
        width=width, height=height, corner_radius=radius,
        color=edge, stroke_width=1.8,
        fill_color=fill, fill_opacity=1,
    )


def card(title, content, width=5.7, height=2.1, accent=FOREST):
    shell = rect(width, height)
    bar = Rectangle(width=0.08, height=height - 0.40, color=accent,
                    stroke_width=0, fill_color=accent, fill_opacity=1)
    bar.move_to(shell.get_left() + RIGHT * 0.19)
    head = tx(title, 29, accent, True)
    head.move_to(shell.get_top() + DOWN * 0.45).align_to(shell, LEFT).shift(RIGHT * 0.42)
    body = tx(content, 24, INK)
    if body.width > width - 0.85:
        body.scale_to_fit_width(width - 0.85)
    body.next_to(head, DOWN, aligned_edge=LEFT, buff=0.26)
    return VGroup(shell, bar, head, body)


class PhysicsBoard(Scene):
    """Modular 2D scene architecture, no external assets or absolute paths."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE

    def clear_board(self):
        things = list(self.mobjects)
        if things:
            self.play(*[FadeOut(m) for m in things], run_time=0.50)

    def titlebar(self, number: str, title: str, subtitle: str = ""):
        # All 16:9 slides reserve y<2.75 for the content area.
        tag = tx("PHYSICS 9   /   2027   /   WEEK 01", 23, FOREST, True)
        tag.move_to([-4.5, 3.85, 0])
        section = tx(number, 25, FOREST, True).move_to([-6.77, 3.12, 0])
        headline = tx(title, 41, INK, True).move_to([0, 3.13, 0])
        if headline.width > 11.4:
            headline.scale_to_fit_width(11.4)
        headline.align_to(np.array([-5.65, 3.12, 0]), LEFT)
        line = Line([-7.2, 2.64, 0], [7.2, 2.64, 0], color=LINE, stroke_width=2.2)
        group = VGroup(tag, section, headline, line)
        if subtitle:
            sub = tx(subtitle, 24, MID)
            if sub.width > 13.8:
                sub.scale_to_fit_width(13.8)
            sub.move_to([0, 2.28, 0])
            group.add(sub)
        self.play(FadeIn(group, shift=DOWN * 0.14), run_time=0.7)
        return group

    def bottom(self, message: str):
        t = tx(message, 22, MID)
        if t.width > 13.7:
            t.scale_to_fit_width(13.7)
        t.move_to([0, -3.86, 0])
        self.play(FadeIn(t), run_time=0.4)
        return t

    def opening(self, lesson: str, title: str, aim: str):
        heading = tx("INSTITUTO JORGE ROBLEDO", 30, FOREST, True).move_to([0, 3.42, 0])
        eyebrow = tx("PHYSICS 9  /  2027  /  QUARTER 1  /  WEEK 1", 24, MID).move_to([0, 2.78, 0])
        title_obj = tx(title, 61, INK, True)
        if title_obj.width > 12.8:
            title_obj.scale_to_fit_width(12.8)
        title_obj.move_to([0, 1.62, 0])
        lesson_obj = tx(lesson, 29, FOREST, True).move_to([0, 0.80, 0])
        aim_obj = tx(aim, 31, INK)
        if aim_obj.width > 13.4:
            aim_obj.scale_to_fit_width(13.4)
        aim_obj.move_to([0, -2.60, 0])
        line = Line([-3.7, -3.06, 0], [3.7, -3.06, 0], color=FOREST, stroke_width=3)
        self.play(FadeIn(heading), FadeIn(eyebrow), run_time=0.8)
        self.play(Write(title_obj), run_time=1.4)
        self.play(FadeIn(lesson_obj, shift=UP * 0.15), run_time=0.65)
        self.play(FadeIn(aim_obj), Create(line), run_time=0.85)
        self.wait(2.5)
        self.clear_board()

    def close(self, title: str, summary: str):
        self.clear_board()
        t = tx(title, 55, FOREST, True).move_to([0, 2.2, 0])
        s = tx(summary, 31, INK)
        if s.width > 13.3:
            s.scale_to_fit_width(13.3)
        s.move_to([0, 0.3, 0])
        foot = tx("NEXT: SI UNITS AND SCIENTIFIC NOTATION  /  WEEK 2", 23, MID)
        foot.move_to([0, -2.9, 0])
        self.play(Write(t), FadeIn(s, shift=UP * 0.18), run_time=1.6)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(3.0)


class Physics9Week1Class1(PhysicsBoard):
    """Class 1: Physics induction; phenomena, testable questions, quantities."""

    def construct(self):
        self.opening("CLASS 01  /  PHENOMENA AND QUANTITIES",
                     "What does physics study?",
                     "From everyday phenomena to evidence-based questions.")
        self.house_phenomenon()
        self.observing()
        self.questions()
        self.quantity_cards()
        self.models()
        self.think()
        self.close("PHYSICS STARTS WITH EVIDENCE",
                   "Observe a phenomenon. Ask a testable question. Name a quantity.")

    def house_phenomenon(self):
        self.titlebar("01", "The physical world is our laboratory",
                      "A familiar house can reveal motion, light, and temperature.")
        # Drafting-house motif deliberately echoes the existing 3D extrusion project.
        house = Rectangle(width=3.5, height=2.10, color=INK, stroke_width=3.2,
                          fill_color=PAPER, fill_opacity=1).move_to([-3.2, -0.65, 0])
        roof = Polygon([-5.22, 0.41, 0], [-1.18, 0.41, 0], [-3.20, 1.89, 0],
                       color=INK, stroke_width=3.2, fill_color=LINE, fill_opacity=0.55)
        door = Rectangle(width=0.75, height=1.35, color=INK, stroke_width=2.4,
                         fill_color=WHITE, fill_opacity=1).move_to([-3.2, -1.03, 0])
        window = Square(side_length=0.61, color=INK, stroke_width=2.3,
                        fill_color=WHITE, fill_opacity=1).move_to([-2.18, -0.45, 0])
        guide = DashedLine([-5.8, -1.72, 0], [-0.5, -1.72, 0],
                           color=MID, dash_length=0.13)
        sun = Circle(radius=0.47, color=AMBER, stroke_width=3,
                     fill_color="#FFF7E8", fill_opacity=1).move_to([-0.17, 1.35, 0])
        rays = VGroup(*[
            Line(sun.get_center() + 0.61 * np.array([np.cos(a), np.sin(a), 0]),
                 sun.get_center() + 0.83 * np.array([np.cos(a), np.sin(a), 0]),
                 color=AMBER, stroke_width=2.1)
            for a in np.linspace(0, TAU, 9)[:-1]
        ])
        right = VGroup(
            tx("MOTION", 28, BLUEPRINT, True),
            tx("LIGHT", 28, AMBER, True),
            tx("TEMPERATURE", 28, FOREST, True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).move_to([3.60, 0.0, 0])
        ball = Dot(point=[-1.15, 1.65, 0], radius=0.18, color=BLUEPRINT)
        self.play(Create(house), Create(roof), run_time=1.7)
        self.play(Create(door), Create(window), Create(guide), run_time=1.1)
        self.play(FadeIn(sun), Create(rays), FadeIn(ball), run_time=1.0)
        self.play(ball.animate.move_to([-1.15, -1.46, 0]),
                  FadeIn(right, shift=RIGHT * 0.4), run_time=2.0)
        self.bottom("Physics studies natural phenomena using observation, measurement, and models.")
        self.wait(3.0)
        self.clear_board()

    def observing(self):
        self.titlebar("02", "What can we observe?",
                      "Describe what happens before trying to explain why.")
        line = Line([-5.0, -1.30, 0], [1.20, -1.30, 0],
                    color=INK, stroke_width=3)
        guide = DashedLine([-4.40, 1.40, 0], [-4.40, -1.20, 0],
                           color=MID, dash_length=0.15)
        ball = Dot([-4.40, 1.40, 0], radius=0.25, color=BLUEPRINT)
        eye = card("OBSERVATION", "The ball moves downward.", width=5.1, height=1.80)
        eye.move_to([3.85, 0.6, 0])
        question = card("QUESTION", "What changes as it falls?", width=5.1,
                        height=1.80, accent=BLUEPRINT)
        question.move_to([3.85, -1.52, 0])
        self.play(Create(line), Create(guide), FadeIn(ball), run_time=0.9)
        self.play(FadeIn(eye), run_time=0.7)
        self.play(ball.animate.move_to([-4.40, -0.98, 0]), run_time=2.2)
        self.play(FadeIn(question, shift=UP * 0.16), run_time=0.9)
        self.bottom("An observation is evidence about what happens; it is not yet a complete explanation.")
        self.wait(3)
        self.clear_board()

    def questions(self):
        self.titlebar("03", "Science asks questions we can test",
                      "Evidence is the difference between a claim and a scientific explanation.")
        valid = card("TESTABLE QUESTION",
                     "How long does the fall take?", 6.10, 2.75, FOREST)
        invalid = card("UNSUPPORTED CLAIM",
                       "The ball falls because it wants to.", 6.10, 2.75, AMBER)
        valid.move_to([-3.32, -0.20, 0])
        invalid.move_to([3.32, -0.20, 0])
        check = tx("We can measure time.", 28, FOREST, True).move_to([-3.32, -2.22, 0])
        bad = tx("No testable evidence is provided.", 27, AMBER).move_to([3.32, -2.22, 0])
        self.play(FadeIn(valid, shift=UP * 0.25), run_time=0.85)
        self.play(FadeIn(check), run_time=0.6)
        self.wait(1.1)
        self.play(FadeIn(invalid, shift=UP * 0.25), run_time=0.85)
        self.play(FadeIn(bad), run_time=0.6)
        self.wait(3.0)
        self.clear_board()

    def quantity_cards(self):
        self.titlebar("04", "Four measurable physical quantities",
                      "A quantity identifies what we measure; its unit tells us the scale.")
        data = [
            ("LENGTH", "metre  /  m", FOREST),
            ("MASS", "kilogram  /  kg", BLUEPRINT),
            ("TIME", "second  /  s", FOREST),
            ("TEMPERATURE", "kelvin  /  K", BLUEPRINT),
        ]
        blocks = VGroup()
        for head, unit, accent in data:
            p = card(head, unit, width=6.15, height=1.92, accent=accent)
            blocks.add(p)
        blocks.arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.55))
        blocks.move_to([0, -0.25, 0])
        for block in blocks:
            self.play(FadeIn(block, shift=UP * 0.22), run_time=0.7)
        self.bottom("SI base quantities include length, mass, time, and temperature.")
        self.wait(3.3)
        self.clear_board()

    def models(self):
        self.titlebar("05", "A physical model simplifies reality",
                      "We keep what matters to answer a specific question.")
        labels = ["REAL PHENOMENON", "MEASURED QUANTITIES", "SIMPLE MODEL"]
        detail = ["Moving ball", "Distance and time", "Speed = distance / time"]
        colors = [BLUEPRINT, FOREST, BLUEPRINT]
        group = VGroup()
        for i in range(3):
            item = card(labels[i], detail[i], width=4.18, height=2.2, accent=colors[i])
            item.move_to([(-4.58 + i * 4.58), 0.1, 0])
            group.add(item)
        arrows = VGroup(
            Arrow(group[0].get_right() + RIGHT * 0.05,
                  group[1].get_left() + LEFT * 0.05,
                  color=MID, buff=0.12, stroke_width=3.1),
            Arrow(group[1].get_right() + RIGHT * 0.05,
                  group[2].get_left() + LEFT * 0.05,
                  color=MID, buff=0.12, stroke_width=3.1),
        )
        self.play(FadeIn(group[0]), run_time=0.65)
        self.play(Create(arrows[0]), FadeIn(group[1]), run_time=1.0)
        self.play(Create(arrows[1]), FadeIn(group[2]), run_time=1.0)
        note = tx("Length and time are base quantities; speed is derived.", 30, INK)
        note.move_to([0, -2.17, 0])
        self.play(FadeIn(note), run_time=0.65)
        self.wait(3.1)
        self.clear_board()

    def think(self):
        self.titlebar("06", "Quick check: observation or measurement?",
                      "Pause and discuss with a partner.")
        prompt = tx("The runner is fast.", 49, INK, True).move_to([0, 1.02, 0])
        q = tx("Is this a numerical measurement?", 32, BLUEPRINT).move_to([0, 0.12, 0])
        answer = card("IMPROVED SCIENTIFIC RECORD",
                      "The runner covers 20 m in 4 s.", width=8.1, height=2.10)
        answer.move_to([0, -1.93, 0])
        self.play(Write(prompt), FadeIn(q), run_time=1.1)
        self.wait(3.0)  # Discussion pause before feedback.
        self.play(FadeIn(answer, shift=UP * 0.18), run_time=1.0)
        self.wait(3.0)


class Physics9Week1Class2(PhysicsBoard):
    """Class 2: observations to measurements; estimate, use units and instruments."""

    def construct(self):
        self.opening("CLASS 02  /  OBSERVATIONS TO MEASUREMENTS",
                     "How do we measure?",
                     "Estimate → choose an instrument → measure → record → compare.")
        self.procedure()
        self.ruler()
        self.clock()
        self.record_table()
        self.compare()
        self.class_activity()
        self.close("A NUMBER NEEDS A UNIT",
                   "Record the quantity, numerical value, unit, and instrument.")

    def procedure(self):
        self.titlebar("01", "The five-step measurement process",
                      "A measurement should be reproducible by another student.")
        steps = [
            ("1", "OBSERVE"), ("2", "ESTIMATE"), ("3", "MEASURE"),
            ("4", "RECORD"), ("5", "COMPARE"),
        ]
        blocks = VGroup()
        for number, name in steps:
            box = rect(2.48, 1.65)
            n = tx(number, 40, FOREST, True).move_to(box.get_center() + UP * 0.35)
            s = tx(name, 22, INK, True).move_to(box.get_center() + DOWN * 0.33)
            blocks.add(VGroup(box, n, s))
        blocks.arrange(RIGHT, buff=0.20).move_to([0, 0.0, 0])
        for i, obj in enumerate(blocks):
            self.play(FadeIn(obj, shift=UP * 0.22), run_time=0.48)
            if i < 4:
                self.wait(0.24)
        self.bottom("An estimate is a reasoned prediction; a measurement uses a calibrated instrument.")
        self.wait(3.0)
        self.clear_board()

    def ruler(self):
        self.titlebar("02", "Measure length: a ruler example",
                      "Read the scale and always include the unit.")
        # Hypothetical 50 cm scale; a 46 cm segment ends 92% across.
        x0, x1, y = -4.60, 2.60, -0.55
        ruler = Rectangle(width=x1 - x0, height=0.55,
                          color=INK, stroke_width=2.7,
                          fill_color=PAPER, fill_opacity=1)
        ruler.move_to([(x0 + x1) / 2, y, 0])
        ticks = VGroup()
        for i in range(11):
            x = x0 + (x1-x0) * (i / 10)
            ticks.add(Line([x, y + 0.28, 0], [x, y - (0.16 if i % 2 else 0.27), 0],
                           color=INK, stroke_width=2))
        labels = VGroup(tx("0 cm", 21, MID).move_to([x0, y-0.74, 0]),
                        tx("50 cm", 21, MID).move_to([x1, y-0.74, 0]))
        measured_x = x0 + (x1-x0) * 0.92
        length_line = Line([x0, 0.47, 0], [measured_x, 0.47, 0],
                           color=BLUEPRINT, stroke_width=7)
        bracket1 = Line([x0, 0.20, 0], [x0, 0.77, 0], color=BLUEPRINT, stroke_width=3)
        bracket2 = Line([measured_x, 0.20, 0], [measured_x, 0.77, 0],
                        color=BLUEPRINT, stroke_width=3)
        label = tx("46 cm  =  0.46 m", 43, BLUEPRINT, True).move_to([-0.75, 1.46, 0])
        self.play(Create(ruler), Create(ticks), FadeIn(labels), run_time=1.4)
        self.play(Create(length_line), Create(bracket1), Create(bracket2), run_time=1.8)
        self.play(FadeIn(label, shift=UP * 0.1), run_time=0.7)
        self.bottom("Illustrative example: the classroom measurement may be different.")
        self.wait(3.2)
        self.clear_board()

    def clock(self):
        self.titlebar("03", "Measure time: a stopwatch example",
                      "Measure the duration between the start and stop events.")
        clock = Circle(radius=1.22, color=INK, stroke_width=4)
        clock.move_to([-2.80, -0.30, 0])
        center = clock.get_center()
        marks = VGroup(*[
            Line(center + 0.97 * np.array([np.sin(a), np.cos(a), 0]),
                 center + 1.12 * np.array([np.sin(a), np.cos(a), 0]),
                 color=MID, stroke_width=2)
            for a in np.linspace(0, TAU, 13)[:-1]
        ])
        hand = Line(center, center + UP * 0.93, color=BLUEPRINT, stroke_width=5)
        knob = RoundedRectangle(width=0.46, height=0.22, corner_radius=0.06,
                                color=INK, fill_color=LINE, fill_opacity=1)
        knob.move_to(center + UP * 1.37)
        readout = card("ELAPSED TIME", "3.2 s  (example)", width=5.8,
                       height=2.00, accent=BLUEPRINT).move_to([3.10, -0.25, 0])
        self.play(Create(clock), Create(marks), FadeIn(knob), FadeIn(hand), run_time=1.25)
        self.play(Rotate(hand, angle=-0.85*TAU, about_point=center), run_time=2.3,
                  rate_func=linear)
        self.play(FadeIn(readout, shift=RIGHT * 0.2), run_time=0.8)
        self.bottom("Quantity: time   •   Value: 3.2   •   Unit: s   •   Instrument: stopwatch")
        self.wait(3.0)
        self.clear_board()

    def record_table(self):
        self.titlebar("04", "A complete measurement record",
                      "Quantity + numerical value + unit + measuring instrument.")
        rows = [
            ["QUANTITY", "VALUE", "UNIT", "INSTRUMENT"],
            ["Length", "0.46", "m", "Ruler"],
            ["Time", "3.2", "s", "Stopwatch"],
            ["Mass", "0.80", "kg", "Scale"],
        ]
        widths = [3.40, 2.25, 2.15, 4.85]
        left = -sum(widths) / 2
        table = VGroup()
        cells = []
        for ri, row in enumerate(rows):
            y = 0.90 - ri * 0.87
            current_x = left
            pieces = VGroup()
            for ci, cell in enumerate(row):
                r = Rectangle(width=widths[ci], height=0.87, stroke_color=LINE,
                              stroke_width=1.8,
                              fill_color=("#E7F1EC" if ri == 0 else WHITE),
                              fill_opacity=1)
                r.move_to([current_x + widths[ci] / 2, y, 0])
                t = tx(cell, 24 if ri == 0 else 27, FOREST if ri == 0 else INK, ri == 0)
                if t.width > widths[ci] - 0.25:
                    t.scale_to_fit_width(widths[ci] - 0.25)
                t.move_to(r)
                pieces.add(r, t)
                current_x += widths[ci]
            cells.append(pieces)
            table.add(pieces)
        for i, group in enumerate(cells):
            self.play(FadeIn(group, shift=UP * 0.10), run_time=0.57)
        self.bottom("Illustrative data only; students must record their own observed values.")
        self.wait(3.8)
        self.clear_board()

    def compare(self):
        self.titlebar("05", "Compare an estimate with the result",
                      "Different values are useful: discuss why they differ.")
        estimate = card("BEFORE", "Estimated length: 0.50 m",
                        width=6.20, height=2.10, accent=AMBER)
        measured = card("AFTER", "Measured length: 0.46 m",
                        width=6.20, height=2.10, accent=FOREST)
        estimate.move_to([-3.28, 0.12, 0])
        measured.move_to([3.28, 0.12, 0])
        result = tx("Absolute difference:  0.50 − 0.46 = 0.04 m",
                    34, BLUEPRINT, True).move_to([0, -2.05, 0])
        self.play(FadeIn(estimate), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(measured), run_time=0.7)
        self.wait(0.8)
        self.play(Write(result), run_time=1.1)
        self.bottom("A difference is not automatically an error: revisit the estimate and procedure.")
        self.wait(3.0)
        self.clear_board()

    def class_activity(self):
        self.titlebar("06", "Classroom challenge: measure and report",
                      "Carry out the activity in pairs using available instruments.")
        prompts = [
            "1. Estimate the length of a desk.",
            "2. Measure it with a ruler or tape measure.",
            "3. Estimate how long a short walk will take.",
            "4. Time the walk with a stopwatch.",
            "5. Record values, units, instruments; compare.",
        ]
        text_group = VGroup(*[tx(p, 30, INK) for p in prompts])
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        text_group.move_to([0, -0.34, 0])
        for row in text_group:
            self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.45)
        self.wait(4.0)
        self.bottom("Exit ticket: Explain what makes a numerical result a valid measurement.")
        self.wait(3.0)
