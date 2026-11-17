#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 / Q1 Week 01 (19–22 January 2027), CAD-HOUSE CANONICAL STYLE.

This is NOT the previous simplified "card" design. It is a literal adaptation
of the institutional visual grammar found in:
render_jobs/itm_cad_house_v6/house_extrusion_itm.py
render_jobs/itm_cad_house_v6/CAD_ANIMATION_PROTOCOL.md
at branch house-step-v3-render-20260818.

ManimCE 0.20.1. Two separate scenes: Physics9CAD_Induction, Physics9CAD_Measurement.
Institutional cover, original local IJR crest, Tex/MathTex/Write typography,
numbered top-right fixed HUD, persistent bottom semantic legend, construction
colors and cad-like 2D drafting diagrams. 2D allowed by lesson plan; the
sequence is observation -> selected variable -> construction -> quantitative
result -> verification. Every numerical result in lessons is an example.
"""
from __future__ import annotations

from pathlib import Path
from manim import *
import numpy as np
import math
import os

PHYSICS_CAD_PREVIEW = os.getenv("PHYSICS_CAD_PREVIEW", "0") == "1"
config.pixel_width = 854 if PHYSICS_CAD_PREVIEW else 1920
config.pixel_height = 480 if PHYSICS_CAD_PREVIEW else 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 15 if PHYSICS_CAD_PREVIEW else 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D7D7D7"
TERRAIN = "#E8EEE5"
SLAB = "#B8BEC5"
SKETCH = "#2878B5"      # sketch, selected physical variable
POSITIVE = "#2E8B57"    # observation supported by measurement
NEGATIVE = "#C0392B"    # unsupported claim or discrepancy
MODEL = "#E5E7E9"
GLASS = "#BFD7EA"


class CanonicalCADPhysics(ThreeDScene):
    INSTITUTION = "INSTITUTO JORGE ROBLEDO"
    TEACHER = "Juan Diego Pérez Álvarez"
    TITLE = "PHYSICS 9 -- QUARTER 1 -- WEEK 01"
    COVER_TITLE = "PHYSICAL PHENOMENA AND MEASUREMENT"
    LESSON_LABEL = "CLASS 01"
    LOGO = Path(__file__).resolve().parent / "assets" / "ijr_crest.svg"

    CAMERA_SETTLE_PAUSE = 1.00
    MICRO_PAUSE = 0.65
    CONSTRUCTION_PAUSE = 1.10
    READING_PAUSE = 1.75
    EXPLANATION_PAUSE = 2.35
    FINAL_OBSERVATION_PAUSE = 2.80

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        # CAD PLAN_2D: camera normal to the XY sketch plane.
        self.set_camera_orientation(phi=0 * DEGREES,
                                    theta=-90 * DEGREES, zoom=1)
        self.stage = []
        self.note = None

    def text(self, content, size=28, weight=NORMAL, color=BLACK_TEXT):
        # Matching house V6: all technical lettering uses TeX and Write.
        safe = content.replace("·", "--").replace("−", "-").replace(
            "→", r"$\rightarrow$"
        )
        if weight == BOLD and "$" not in safe:
            safe = r"\textbf{" + safe + "}"
        return Tex(safe, font_size=size, color=color)

    def math(self, expression, size=38, color=BLACK_TEXT):
        return MathTex(expression, font_size=size, color=color)

    def register(self, *objects):
        self.stage.extend(objects)
        return objects

    def stage_clear(self):
        if self.note is not None:
            self.register(self.note)
            self.note = None
        objects = [m for m in self.stage if m in self.mobjects]
        if objects:
            self.play(*[FadeOut(m) for m in objects], run_time=0.72)
        self.stage = []

    def institutional_cover(self):
        if not self.LOGO.exists():
            raise FileNotFoundError(f"Missing exact local crest: {self.LOGO}")
        crest = SVGMobject(str(self.LOGO)).scale_to_fit_height(2.02)
        crest.to_edge(UP, buff=0.34)
        uni = self.text(self.INSTITUTION, 27, BOLD, DARK)
        course = self.text("PHYSICS 9", 52, BOLD, DARK)
        group = self.text("2027 -- QUARTER 1 -- WEEK 01", 26, BOLD, SKETCH)
        main = self.text(self.COVER_TITLE, 31, BOLD, DARK)
        lesson = self.text(self.LESSON_LABEL, 27, BOLD, POSITIVE)
        teacher = self.text(f"Teacher: {self.TEACHER}", 23, NORMAL, MID)
        rule_top = Line(LEFT * 5.5, RIGHT * 5.5,
                        color=SKETCH, stroke_width=2.4)
        rule_bottom = Line(LEFT * 4.1, RIGHT * 4.1,
                           color=LIGHT, stroke_width=1.4)
        stack = VGroup(uni, course, group, rule_top, main, lesson, rule_bottom, teacher)
        stack.arrange(DOWN, buff=0.18)
        stack.next_to(crest, DOWN, buff=0.12)
        # Exact CAD cover motif: closed sketch -> material/result.
        motifs = VGroup(
            Square(0.50, color=SKETCH, stroke_width=2.4),
            Arrow(LEFT * 0.18, RIGHT * 0.26,
                  color=DARK, stroke_width=2, buff=0).shift(RIGHT * 0.25),
            Square(0.50, color=POSITIVE, stroke_width=2.4).shift(RIGHT * 0.77),
        ).scale(0.83).next_to(stack, DOWN, buff=0.32)
        covers = [crest, *stack, motifs]
        for obj in covers:
            self.add_fixed_in_frame_mobjects(obj)
        self.play(FadeIn(crest, shift=DOWN * 0.08), run_time=0.85)
        self.play(Write(uni), run_time=0.8)
        self.play(Write(course), run_time=1.25)
        self.play(Write(group), Create(rule_top), run_time=0.95)
        self.play(Write(main), run_time=1.05)
        self.play(Write(lesson), run_time=0.8)
        self.play(Create(rule_bottom), Write(teacher), run_time=0.9)
        self.play(Create(motifs), run_time=0.75)
        self.wait(self.EXPLANATION_PAUSE)
        self.play(*[FadeOut(obj) for obj in covers], run_time=0.85)
        for obj in covers:
            self.remove_fixed_in_frame_mobjects(obj)
            self.remove(obj)

    def fixed_hud(self):
        # Near-literal replication of HouseExtrusion3D.fixed_hud().
        title = self.text("PHYSICS 9 -- 2027 -- QUARTER 1", 29, BOLD)
        subtitle = self.text(
            "Physical phenomena and measurement -- evidence first",
            19, NORMAL, MID,
        )
        title.to_corner(UL, buff=0.38)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)
        rule = Line(LEFT * 7.55, RIGHT * 7.55,
                    color=LIGHT, stroke_width=1.3).to_edge(UP, buff=1.08)
        phase_box = RoundedRectangle(
            width=5.75, height=0.52, corner_radius=0.10,
            fill_color=WHITE, fill_opacity=0.97,
            stroke_color=DARK, stroke_width=1.1,
        ).to_corner(UR, buff=0.40)
        phase = self.text("01 -- OBSERVE", 19, BOLD).move_to(phase_box)
        skdot = Circle(radius=0.07, fill_color=SKETCH, fill_opacity=1,
                       stroke_width=0)
        sktxt = self.text("SELECT / MODEL", 17, BOLD, SKETCH)
        medot = Circle(radius=0.07, fill_color=POSITIVE, fill_opacity=1,
                       stroke_width=0)
        metxt = self.text("EVIDENCE / MEASURED", 17, BOLD, POSITIVE)
        nodot = Circle(radius=0.07, fill_color=NEGATIVE, fill_opacity=1,
                       stroke_width=0)
        notxt = self.text("UNSUPPORTED / DIFFERENCE", 17, BOLD, NEGATIVE)
        legend = VGroup(skdot, sktxt, medot, metxt, nodot, notxt)
        legend.arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.25)
        self.hud = [title, subtitle, rule, phase_box, phase, legend]
        for obj in self.hud:
            self.add_fixed_in_frame_mobjects(obj)
        self.play(Write(title), Write(subtitle), Write(phase),
                  Write(sktxt), Write(metxt), Write(notxt), run_time=1.85)
        self.wait(self.READING_PAUSE)
        return {"box": phase_box, "text": phase}

    def set_phase(self, number, label, color=DARK):
        old = self.ph["text"]
        new = self.text(f"{number:02d} -- {label}", 19, BOLD, color)
        new.move_to(self.ph["box"])
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), Write(new), run_time=0.72)
        self.wait(self.MICRO_PAUSE)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        self.ph["text"] = new

    def caption(self, line, color=DARK):
        if self.note is not None:
            self.play(FadeOut(self.note), run_time=0.35)
            self.note = None
        back = RoundedRectangle(
            width=13.4, height=0.70, corner_radius=0.12,
            fill_color=WHITE, fill_opacity=0.96,
            stroke_color=LIGHT, stroke_width=1.1,
        ).move_to([0, -3.14, 0])
        t = self.text(line, 24, NORMAL, color).move_to(back)
        if t.width > 12.8:
            t.scale_to_fit_width(12.8)
        self.note = VGroup(back, t)
        self.add_fixed_in_frame_mobjects(self.note)
        self.play(FadeIn(back), Write(t), run_time=1.0)
        return self.note

    def label(self, s, pos, size=30, color=DARK, bold=False):
        obj = self.text(s, size, BOLD if bold else NORMAL, color)
        obj.move_to(np.array([pos[0], pos[1], 0]))
        self.register(obj)
        return obj

    def rule(self, a, b, color=SKETCH, width=3):
        return Line(np.array([a[0], a[1], 0]),
                    np.array([b[0], b[1], 0]),
                    color=color, stroke_width=width)

    def exit_summary(self, first, second):
        self.stage_clear()
        self.set_phase(99, "VERIFY / SUMMARY", POSITIVE)
        title = self.label(first, (0, 0.93), 44, POSITIVE, True)
        sub = self.label(second, (0, -0.45), 30)
        if sub.width > 13.4:
            sub.scale_to_fit_width(13.4)
        self.play(Write(title), Write(sub), run_time=1.7)
        self.caption("Observe, select a quantity, measure, and check the evidence.", POSITIVE)
        self.wait(5.2)
        self.stage_clear()

    def footer_cleanup(self):
        # All HUD elements are fixed; clear them at end only.
        all_hud = [*self.hud]
        if self.ph["text"] not in all_hud:
            all_hud.append(self.ph["text"])
        self.play(*[FadeOut(obj) for obj in all_hud], run_time=0.6)
        for obj in all_hud:
            self.remove_fixed_in_frame_mobjects(obj)
            self.remove(obj)


class Physics9CAD_Induction(CanonicalCADPhysics):
    LESSON_LABEL = "CLASS 01 -- PHYSICS INDUCTION"
    COVER_TITLE = "WHAT DOES PHYSICS STUDY?"

    def construct(self):
        self.institutional_cover()
        self.ph = self.fixed_hud()
        self.phenomenon()
        self.evidence()
        self.quantities()
        self.model()
        self.class_check()
        self.exit_summary("PHYSICS IS A SCIENCE OF EVIDENCE",
                          "Describe. Ask. Identify a measurable quantity.")
        self.footer_cleanup()

    def phenomenon(self):
        self.set_phase(1, "PHYSICAL PHENOMENON", SKETCH)
        # Functional CAD-style geometry, not pictorial slide/cards.
        plane = Rectangle(width=6.9, height=0.16, color=DARK,
                          fill_color=SLAB, fill_opacity=1)
        plane.move_to([-3.1, -1.75, 0])
        x = -3.4
        p0 = np.array([x, 1.7, 0])
        p1 = np.array([x, -1.41, 0])
        route = DashedLine(p0, p1, color=SKETCH, stroke_width=2,
                           dash_length=0.14)
        marker = ValueTracker(0.0)
        ball = always_redraw(lambda:
            Circle(radius=0.29, stroke_color=DARK, stroke_width=1.6,
                   fill_color=SKETCH, fill_opacity=0.97)
            .move_to(p0 + (p1-p0) * marker.get_value()))
        observer = self.label("WHAT CHANGED?", (3.20, 1.28), 33, DARK, True)
        q1 = self.label("Position", (3.25, 0.32), 32, SKETCH)
        q2 = self.label("Time", (3.25, -0.33), 32, SKETCH)
        p = self.label("A falling object", (-3.3, 2.15), 26, DARK)
        self.play(Create(plane), Create(route), Write(p), run_time=1.6)
        self.play(FadeIn(ball), run_time=0.55)
        self.wait(self.READING_PAUSE)
        self.play(marker.animate.set_value(1.0), run_time=3.0,
                  rate_func=rate_functions.ease_in_quad)
        self.play(Write(observer), Write(q1), Write(q2), run_time=1.4)
        self.caption("Observation: the ball moves downward. Explanation requires evidence.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        # Clear live tracker before FadeOut: never leave a drifting object.
        ball.clear_updaters()
        self.register(plane, route, ball)
        self.stage_clear()

    def evidence(self):
        self.set_phase(2, "QUESTION / EVIDENCE", POSITIVE)
        src = self.label("A ball falls", (-3.4, 1.6), 38, DARK, True)
        select = self.label("Can we measure how long it takes?", (1.55, 1.6), 29, SKETCH)
        meter = self.label("YES: use a stopwatch", (1.65, 0.25), 30, POSITIVE, True)
        claim = self.label("NO TEST: the ball wants to fall", (1.20, -1.18), 29, NEGATIVE)
        connector = Arrow([-4.25, 1.17, 0], [-0.60, 1.17, 0],
                          buff=0, color=SKETCH, stroke_width=3)
        sep = Line([-5.3, -0.48, 0], [5.3, -0.48, 0],
                   color=LIGHT, stroke_width=1.5)
        self.play(Write(src), Create(connector), run_time=1.25)
        self.play(Write(select), run_time=1.0)
        self.wait(self.READING_PAUSE)
        self.play(Write(meter), Create(sep), run_time=0.9)
        self.wait(self.EXPLANATION_PAUSE)
        self.play(Write(claim), run_time=1.05)
        self.caption("A scientific question should be answerable using observations or measurements.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.register(connector, sep)
        self.stage_clear()

    def quantities(self):
        self.set_phase(3, "SELECT THE QUANTITY", SKETCH)
        # Four independent technical diagrams; no infographic "cards".
        guides = VGroup(
            self.rule((-6.6, 0.1), (6.6, 0.1), LIGHT, 1.4),
            self.rule((0, 2.1), (0, -2.5), LIGHT, 1.4),
        )
        self.play(Create(guides), run_time=0.65)
        self.register(guides)
        # LENGTH: dimensional annotation
        dim = DoubleArrow([-5.55, 1.03, 0], [-1.35, 1.03, 0],
                          color=SKETCH, stroke_width=3,
                          buff=0, max_tip_length_to_length_ratio=0.12)
        ltxt = self.label("LENGTH -- metre (m)", (-3.45, 1.75), 27, DARK, True)
        self.play(Create(dim), Write(ltxt), run_time=1.2)
        self.register(dim)
        # MASS: weight on a balance platform -- do NOT equate mass and weight.
        weight = Rectangle(width=1.3, height=0.87, stroke_color=DARK,
                           stroke_width=2.5, fill_color=SLAB,
                           fill_opacity=0.95).move_to([3.1, 1.06, 0])
        balance = self.rule((1.90, 0.50), (4.35, 0.50), DARK, 3.2)
        mass = self.label("MASS -- kilogram (kg)", (3.12, 1.85), 27, DARK, True)
        self.play(Create(weight), Create(balance), Write(mass), run_time=1.3)
        self.register(weight, balance)
        # TIME: clock schematic, with moving hand
        ctr = np.array([-3.55, -1.32, 0])
        dial = Circle(radius=0.86, color=DARK, stroke_width=2.7).move_to(ctr)
        hand = Line(ctr, ctr + 0.7*UP, color=SKETCH, stroke_width=4)
        time = self.label("TIME -- second (s)", (-3.50, -2.32), 27, DARK, True)
        self.play(Create(dial), Create(hand), Write(time), run_time=1.3)
        self.play(Rotate(hand, -PI * 0.75, about_point=ctr), run_time=1.6)
        self.register(dial, hand)
        # TEMPERATURE: schematic thermometer
        stem = RoundedRectangle(width=0.26, height=1.15, corner_radius=0.10,
                                color=DARK, fill_color=WHITE, fill_opacity=1)
        stem.move_to([3.20, -1.10, 0])
        bulb = Circle(radius=0.34, color=DARK, stroke_width=2,
                      fill_color=NEGATIVE, fill_opacity=0.9).move_to([3.20, -1.70, 0])
        fluid = self.rule((3.2, -1.72), (3.2, -0.97), NEGATIVE, 5)
        temp = self.label("TEMPERATURE -- kelvin (K)", (3.25, -2.32), 26, DARK, True)
        self.play(Create(stem), Create(bulb), Create(fluid), Write(temp), run_time=1.3)
        self.register(stem, bulb, fluid)
        self.caption("Length, mass, time and temperature are SI base quantities.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def model(self):
        self.set_phase(4, "BUILD A SIMPLE MODEL", SKETCH)
        # 2D drafting chain: physical movement -> selected measurements -> model.
        baseline = self.rule((-6.65, -0.35), (-1.95, -0.35), DARK, 3)
        p_start = Dot(point=[-6.15, -0.35, 0], radius=0.22, color=SKETCH)
        p_end = Dot(point=[-2.60, -0.35, 0], radius=0.22, color=POSITIVE)
        track = DashedLine([-6.15, -0.35, 0], [-2.60, -0.35, 0],
                           color=SKETCH, stroke_width=2)
        title1 = self.label("MOVEMENT", (-4.5, 1.24), 29, DARK, True)
        distance = self.math(r"d=4\,\mathrm{m}", 36, SKETCH).move_to([2.70, 1.22, 0])
        time = self.math(r"t=2\,\mathrm{s}", 36, SKETCH).move_to([2.70, 0.40, 0])
        bar = self.rule((0.28, -0.17), (5.08, -0.17), LIGHT, 2)
        model = self.math(r"\overline{v}=\frac{d}{t}=2\,\mathrm{m/s}",
                          43, POSITIVE).move_to([2.82, -1.27, 0])
        self.play(Create(baseline), FadeIn(p_start), Write(title1), run_time=1.2)
        self.play(Create(track), TransformFromCopy(p_start, p_end), run_time=1.8)
        self.play(Write(distance), Write(time), run_time=1.5)
        self.wait(self.READING_PAUSE)
        self.play(Create(bar), Write(model), run_time=1.7)
        self.caption("Illustrative example: average speed is a derived quantity.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.register(baseline, track, p_start, p_end, distance, time, bar, model)
        self.stage_clear()

    def class_check(self):
        self.set_phase(5, "CLASSROOM CHECK", POSITIVE)
        title = self.label("Observation, quantity or unsupported claim?", (0, 1.67), 32, DARK, True)
        a = self.label("A: The door is beautiful.", (-0.25, 0.66), 30)
        b = self.label("B: The door is 2 m tall.", (-0.25, -0.25), 30)
        wait = self.label("THINK -- DISCUSS -- JUSTIFY", (0, -1.35), 24, SKETCH, True)
        self.play(Write(title), Write(a), Write(b), run_time=1.6)
        self.play(Write(wait), run_time=0.65)
        self.wait(4.2)
        result = self.label("B is a numerical measurement of length.", (0, -2.16), 28, POSITIVE, True)
        self.play(Write(result), run_time=1.0)
        self.caption("What instrument and unit would you record?")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()


class Physics9CAD_Measurement(CanonicalCADPhysics):
    LESSON_LABEL = "CLASS 02 -- MEASURING THE WORLD"
    COVER_TITLE = "FROM OBSERVATION TO MEASUREMENT"

    def validate_examples(self):
        assert abs(0.50 - 0.46 - 0.04) < 1e-12
        assert 46 / 100 == 0.46

    def construct(self):
        self.validate_examples()
        self.institutional_cover()
        self.ph = self.fixed_hud()
        self.workflow()
        self.ruler()
        self.stopwatch()
        self.record()
        self.compare()
        self.activity()
        self.exit_summary("A MEASUREMENT NEEDS A UNIT",
                          "Quantity + numerical value + unit + instrument")
        self.footer_cleanup()

    def workflow(self):
        self.set_phase(1, "MEASUREMENT PROCEDURE", SKETCH)
        words = ("OBSERVE", "ESTIMATE", "MEASURE", "RECORD", "COMPARE")
        # CAD process pipeline, numbered steps plus actual arrows, not cards.
        for index, name in enumerate(words):
            x = -5.42 + index * 2.70
            circ = Circle(radius=0.37, color=SKETCH, stroke_width=2.4)
            circ.move_to([x, 0.72, 0])
            number = self.label(str(index+1), (x, 0.72), 29, SKETCH, True)
            text = self.label(name, (x, -0.35), 22, DARK, True)
            self.play(Create(circ), Write(number), Write(text), run_time=0.77)
            self.register(circ)
            if index < 4:
                arr = Arrow([x+0.57, 0.72, 0], [x+2.15, 0.72, 0],
                            color=POSITIVE, stroke_width=2.3,
                            buff=0, max_tip_length_to_length_ratio=0.20)
                self.play(Create(arr), run_time=0.55)
                self.register(arr)
            self.wait(self.MICRO_PAUSE)
        self.caption("An estimate is a prediction; a measurement uses a calibrated instrument.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def ruler(self):
        self.set_phase(2, "LENGTH / RULER", SKETCH)
        # Exactly 0–50 cm technical scale. Sample 46 cm is at 92% of the axis.
        x0, x1, y = -6.00, 3.10, -0.55
        scale = Rectangle(width=x1-x0, height=0.47, stroke_color=DARK,
                          stroke_width=2.2, fill_color=MODEL,
                          fill_opacity=1).move_to([(x0+x1)/2, y, 0])
        self.play(Create(scale), run_time=1.0)
        self.register(scale)
        for i in range(11):
            x = x0 + (x1-x0)*(i/10.0)
            tick = self.rule((x, y + 0.22), (x, y - 0.16 if i % 2 else y-0.22), DARK, 1.5)
            self.play(Create(tick), run_time=0.12)
            self.register(tick)
        l0 = self.label("0 cm", (x0, -1.34), 25, MID)
        l50 = self.label("50 cm", (x1, -1.34), 25, MID)
        self.play(Write(l0), Write(l50), run_time=0.65)
        x_meas = x0 + (x1-x0)*0.92
        indicator = self.rule((x0, 0.52), (x_meas, 0.52), SKETCH, 5.2)
        lseg = self.rule((x0, 0.20), (x0, 0.85), SKETCH, 2.2)
        rseg = self.rule((x_meas, 0.20), (x_meas, 0.85), SKETCH, 2.2)
        self.play(Create(indicator), Create(lseg), Create(rseg), run_time=1.9)
        self.register(indicator, lseg, rseg)
        value = self.math(r"d=46\,\mathrm{cm}=0.46\,\mathrm{m}",
                          42, POSITIVE).move_to([-1.15, 1.58, 0])
        self.play(Write(value), run_time=1.6)
        self.register(value)
        self.caption("Illustrative measurement: length, 0.46 m, ruler.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def stopwatch(self):
        self.set_phase(3, "TIME / STOPWATCH", SKETCH)
        ctr = np.array([-3.50, 0.00, 0])
        clock = Circle(radius=1.45, color=DARK, stroke_width=3)
        clock.move_to(ctr)
        self.play(Create(clock), run_time=1.1)
        self.register(clock)
        marks = VGroup()
        for a in np.linspace(0, TAU, 13)[:-1]:
            p0 = ctr + 1.17*np.array([math.sin(a), math.cos(a), 0])
            p1 = ctr + 1.36*np.array([math.sin(a), math.cos(a), 0])
            marks.add(Line(p0, p1, color=DARK, stroke_width=2))
        hand = Line(ctr, ctr + UP*1.08, color=SKETCH, stroke_width=5)
        self.play(Create(marks), Create(hand), run_time=1.3)
        self.register(marks, hand)
        self.play(Rotate(hand, angle=-1.20*PI, about_point=ctr),
                  run_time=3.2, rate_func=linear)
        elapsed = self.math(r"t=3.2\,\mathrm{s}", 46, POSITIVE).move_to([2.45, 0.8, 0])
        unit = self.label("Quantity: time", (2.45, -0.12), 29, DARK, True)
        instrument = self.label("Instrument: stopwatch", (2.45, -0.95), 28)
        self.play(Write(elapsed), Write(unit), Write(instrument), run_time=1.8)
        self.register(elapsed)
        self.caption("Illustrative example. Start and stop events define the elapsed time.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def record(self):
        self.set_phase(4, "RECORD YOUR DATA", POSITIVE)
        # Technical table with four independent columns and draft lines.
        widths = [3.35, 2.20, 1.85, 4.85]
        headers = ["Quantity", "Value", "Unit", "Instrument"]
        rows = [
            ["Length", "0.46", "m", "ruler"],
            ["Time", "3.2", "s", "stopwatch"],
            ["Mass", "0.80", "kg", "balance"],
        ]
        start_x = -sum(widths)/2
        top_y = 1.68
        for row_n, line in enumerate([headers]+rows):
            x = start_x
            for c, word in enumerate(line):
                center = [x + widths[c]/2, top_y-0.91*row_n, 0]
                box = Rectangle(width=widths[c], height=0.91, color=LIGHT,
                                stroke_width=1.4,
                                fill_color=TERRAIN if row_n == 0 else WHITE,
                                fill_opacity=1).move_to(center)
                t = self.text(word, 24 if row_n==0 else 28,
                              BOLD if row_n==0 else NORMAL,
                              DARK if row_n else SKETCH).move_to(center)
                if t.width > widths[c]-0.28:
                    t.scale_to_fit_width(widths[c]-0.28)
                self.play(Create(box), Write(t), run_time=0.20)
                self.register(box,t)
                x += widths[c]
            self.wait(self.MICRO_PAUSE)
        self.caption("Illustrative values only: record the quantity, number, unit, and instrument.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def compare(self):
        self.set_phase(5, "COMPARE ESTIMATE AND RESULT", NEGATIVE)
        x0, length = -5.85, 10.3
        estimate = self.rule((x0, 1.03), (x0 + length, 1.03), SKETCH, 6)
        real = self.rule((x0, -0.32), (x0 + length*0.92, -0.32), POSITIVE, 6)
        label1 = self.label("Estimate: 0.50 m", (-3.1, 1.67), 30, SKETCH, True)
        label2 = self.label("Measured: 0.46 m", (-3.1, -0.95), 30, POSITIVE, True)
        self.play(Create(estimate), Write(label1), run_time=1.5)
        self.wait(self.READING_PAUSE)
        self.play(Create(real), Write(label2), run_time=1.5)
        self.wait(self.READING_PAUSE)
        eq = self.math(r"|0.50-0.46|=0.04\,\mathrm{m}", 43, NEGATIVE)
        eq.move_to([1.8, -2.0, 0])
        self.play(Write(eq), run_time=1.6)
        self.register(estimate, real, eq)
        self.caption("Difference between estimate and measured value: 0.04 m.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def activity(self):
        self.set_phase(6, "MEASUREMENT STATIONS", POSITIVE)
        steps = [
            "1. Estimate the length of a desk.",
            "2. Measure length using a ruler or tape.",
            "3. Estimate the duration of a short walk.",
            "4. Measure elapsed time with a stopwatch.",
            "5. Record your values, units, and instruments.",
            "6. Compare estimates with measurements.",
        ]
        group = VGroup()
        for line in steps:
            g = self.text(line, 28)
            group.add(g)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([0, -0.15, 0])
        if group.width > 13.4: group.scale_to_fit_width(13.4)
        for g in group:
            self.play(Write(g), run_time=0.95)
            self.wait(self.MICRO_PAUSE)
        self.register(group)
        self.caption("Exit ticket: what distinguishes an estimate from a measurement?")
        self.wait(4.5)
        self.stage_clear()
