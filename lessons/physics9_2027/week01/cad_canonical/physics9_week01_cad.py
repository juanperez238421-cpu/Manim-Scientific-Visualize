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
    LOGO = Path(__file__).resolve().parent / "assets" / "ijr_original.png"

    CAMERA_SETTLE_PAUSE = 1.50
    MICRO_PAUSE = 1.20
    CONSTRUCTION_PAUSE = 2.20
    READING_PAUSE = 3.40
    EXPLANATION_PAUSE = 4.20
    FINAL_OBSERVATION_PAUSE = 5.00

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
        safe = content.replace("%", r"\%").replace("·", "--").replace("−", "-").replace(
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
        # Original raster crest, not a reillustrated vector: aspect ratio preserved.
        crest = ImageMobject(str(self.LOGO)).scale_to_fit_height(2.25)
        crest.to_edge(UP, buff=0.34)
        uni = self.text(self.INSTITUTION, 27, BOLD, DARK)
        course = self.text(getattr(self, "COURSE_TITLE", "PHYSICS 9"), 52, BOLD, DARK)
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
        self.wait(self.EXPLANATION_PAUSE + 1.5)
        self.play(*[FadeOut(obj) for obj in covers], run_time=0.85)
        for obj in covers:
            self.remove_fixed_in_frame_mobjects(obj)
            self.remove(obj)

    def fixed_hud(self):
        # Near-literal replication of HouseExtrusion3D.fixed_hud().
        title = self.text(getattr(self, "HUD_TITLE", "PHYSICS 9 -- 2027 -- QUARTER 1"), getattr(self, "HUD_TITLE_SIZE", 29), BOLD)
        subtitle = self.text(getattr(self, "HUD_SUBTITLE", "Physical phenomena and measurement -- evidence first"), getattr(self, "HUD_SUB_SIZE", 19), NORMAL, MID)
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
        self.wait(8.0)
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
        self.wait(8.0)
        result = self.label("B is a numerical measurement of length.", (0, -2.16), 28, POSITIVE, True)
        self.play(Write(result), run_time=1.35)
        self.wait(self.READING_PAUSE)
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
        # Fifty 1-cm subdivisions justify reading 46 cm, unlike V2's 5-cm marks.
        ticks = VGroup()
        for i in range(51):
            x = x0 + (x1-x0)*(i/50.0)
            depth = 0.22 if i % 10 == 0 else (0.15 if i % 5 == 0 else 0.09)
            ticks.add(self.rule((x, y + 0.22), (x, y + 0.22-depth), DARK, 1.7))
        self.play(Create(ticks), run_time=2.10)
        self.register(ticks)
        l0 = self.label("0 cm", (x0, -1.34), 25, MID)
        l50 = self.label("50 cm", (x1, -1.34), 25, MID)
        self.play(Write(l0), Write(l50), run_time=0.65)
        x_meas = x0 + (x1-x0)*0.92
        indicator = self.rule((x0, 0.52), (x_meas, 0.52), SKETCH, 5.2)
        lseg = self.rule((x0, 0.20), (x0, 0.85), SKETCH, 2.2)
        rseg = self.rule((x_meas, 0.20), (x_meas, 0.85), SKETCH, 2.2)
        self.play(Create(indicator), Create(lseg), Create(rseg), run_time=2.3)
        self.wait(self.READING_PAUSE)
        self.register(indicator, lseg, rseg)
        value = self.math(r"d=46\,\mathrm{cm}=0.46\,\mathrm{m}",
                          42, POSITIVE).move_to([-1.15, 1.58, 0])
        self.play(Write(value), run_time=1.6)
        self.wait(self.READING_PAUSE)
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
        self.play(Rotate(hand, angle=-TAU*(3.2/10.0), about_point=ctr),
                  run_time=3.2, rate_func=linear)
        elapsed = self.math(r"t=3.2\,\mathrm{s}", 46, POSITIVE).move_to([2.45, 0.94, 0])
        ten_second_scale = self.label("Dial scale: 10 s / revolution", (2.45, -1.72), 24, SKETCH)
        unit = self.label("Quantity: time", (2.45, -0.12), 29, DARK, True)
        instrument = self.label("Instrument: stopwatch", (2.45, -0.95), 28)
        self.play(Write(elapsed), Write(unit), Write(instrument), Write(ten_second_scale), run_time=2.2)
        self.wait(self.READING_PAUSE)
        self.register(elapsed)
        self.caption("Example: 3.2 s corresponds to 32% of a 10 s stopwatch revolution.")
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
                self.play(Create(box), Write(t), run_time=0.56)
                self.register(box,t)
                x += widths[c]
            self.wait(self.READING_PAUSE)
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
        self.wait(self.READING_PAUSE)
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
        self.wait(8.0)
        self.stage_clear()


# ---------------------------------------------------------------------------
# V4: Introductory video that genuinely covers school PHYSICS, not a P3 recap.
# Evidence: 9th-grade 2027 Quarter 1 class plan (intro/measurement), and the
# IJR Physics 10/11 area plans + three-period 2026 curriculum map supplied by
# the user. Grade 10/11 topics are grouped by the exact PERIOD I/II/III maps.
# This is an orientation, not a claim that 2027 Grade 10/11 plans are finalized.
# ---------------------------------------------------------------------------

class Physics9CAD_SchoolRoadmap(CanonicalCADPhysics):
    """Class 1 — visually animated physics journey through Grades 9–11."""
    COURSE_TITLE = "PHYSICS -- GRADES 9 TO 11"
    COVER_TITLE = "THE PHYSICS JOURNEY"
    LESSON_LABEL = "CLASS 01 -- THE WHOLE SCHOOL ROADMAP"
    HUD_TITLE = "PHYSICS -- GRADES 9 TO 11"
    HUD_SUBTITLE = "What physics will teach us -- based on the school's curriculum"
    MICRO_PAUSE = 1.20
    READING_PAUSE = 3.20
    EXPLANATION_PAUSE = 3.90
    FINAL_OBSERVATION_PAUSE = 4.30

    def big(self, text, xy, size=34, color=DARK, weight=NORMAL, width=12.6):
        t = self.label(text, xy, size, color, weight == BOLD)
        if t.width > width:
            t.scale_to_fit_width(width)
        return t

    def start_topic(self, number, phase, title, subtitle):
        self.stage_clear()
        self.set_phase(number, phase, SKETCH if number % 2 else POSITIVE)
        title_obj = self.big(title, (0, 2.03), 39, DARK, BOLD, 13.1)
        sub_obj = self.big(subtitle, (0, 1.34), 27, MID, NORMAL, 13.0)
        self.play(Write(title_obj), run_time=1.05)
        self.play(Write(sub_obj), run_time=0.95)
        self.wait(self.READING_PAUSE)
        return title_obj, sub_obj

    def construct(self):
        self.institutional_cover()
        self.ph = self.fixed_hud()
        self.foundations()
        self.kinematics_dynamics()
        self.energy_circular()
        self.torque_gravity()
        self.oscillations_waves()
        self.electricity_optics()
        self.fluids_thermodynamics()
        self.period_map()
        self.exit_summary(
            "PHYSICS CONNECTS THE ENTIRE NATURAL WORLD",
            "Motion, forces, energy, waves, fields, fluids, heat and space.")
        self.footer_cleanup()

    def foundations(self):
        self.start_topic(1, "GR 9 / FOUNDATIONS", "GRADE 9 -- LEARN TO THINK LIKE A PHYSICIST",
                         "Observation, measurement, units, models and experiments")
        x0, x1 = -5.9, 0.2
        baseline = self.rule((x0, -0.28), (x1, -0.28), DARK, 3.1)
        ticks = VGroup(*[
            self.rule((x0+i*(x1-x0)/12, -0.10),
                      (x0+i*(x1-x0)/12, -0.46 if i % 3 == 0 else -0.30),
                      SKETCH, 2.0)
            for i in range(13)])
        book = Rectangle(width=2.7, height=1.35, color=DARK, stroke_width=2.3,
                         fill_color=MODEL, fill_opacity=0.45).move_to([3.15, -0.15, 0])
        evidence = self.big("MEASURE  -  RECORD  -  COMPARE", (0, -1.73),
                            34, POSITIVE, BOLD)
        self.play(Create(baseline), Create(ticks), run_time=1.5)
        self.play(Create(book), run_time=0.9)
        label = self.big("A scientific model", (3.15, -0.15), 29, SKETCH, BOLD, 2.4)
        self.play(Write(label), Write(evidence), run_time=1.4)
        self.register(baseline, ticks, book)
        self.caption("First learn to collect evidence. Then learn how to explain it.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def kinematics_dynamics(self):
        self.start_topic(2, "GR 10 / PERIOD I", "MOTION AND FORCES",
                         "Kinematics: displacement, velocity, acceleration and projectiles")
        ground = self.rule((-6.2, -0.6), (0.2, -0.6), DARK, 3.3)
        cart = VGroup(
            RoundedRectangle(width=1.05, height=0.50, corner_radius=0.10,
                             color=DARK, stroke_width=2.2, fill_color=MODEL, fill_opacity=1),
            Dot([-0.30,-0.35,0],radius=0.11,color=DARK),
            Dot([0.30,-0.35,0],radius=0.11,color=DARK))
        cart.move_to([-5.35, -0.28, 0])
        self.play(Create(ground), FadeIn(cart), run_time=1.2)
        self.play(cart.animate.shift(RIGHT*4.2), run_time=2.65, rate_func=linear)
        self.register(ground,cart)
        ramp = Polygon([1.2,-1.45,0],[5.95,-1.45,0],[5.95,0.20,0],
                       stroke_color=DARK,stroke_width=3,fill_color=MODEL,fill_opacity=0.55)
        mass = Square(side_length=0.56, color=SKETCH, stroke_width=2.3,
                      fill_color=SKETCH,fill_opacity=0.65).move_to([4.9,-0.77,0])
        force = Arrow([4.9,-0.74,0],[3.55,-0.74,0],
                      color=POSITIVE,buff=0,stroke_width=4)
        self.play(Create(ramp), FadeIn(mass), run_time=1.15)
        self.play(Create(force), run_time=0.90)
        self.register(ramp,mass,force)
        self.big("Newton's laws / friction / inclined planes",
                 (0,-2.27),29,DARK,NORMAL,12.7)
        self.caption("Grade 10 / Period I: How objects move -- and why their motion changes.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def energy_circular(self):
        self.start_topic(3,"GR 10 / PERIOD II","WORK, ENERGY AND CIRCULAR MOTION",
                         "Conservation, momentum, collisions and centripetal motion")
        ramp = ArcBetweenPoints([-6.1,-1.45,0],[-0.45,-1.45,0],angle=-0.66,
                                color=DARK,stroke_width=3.3)
        ball = Dot([-6.1,-1.45,0],radius=0.22,color=SKETCH)
        self.play(Create(ramp),FadeIn(ball),run_time=1.35)
        self.play(MoveAlongPath(ball,ramp),run_time=2.5,rate_func=linear)
        self.register(ramp,ball)
        loop = Circle(radius=1.10,color=DARK,stroke_width=2.8).move_to([3.85,-0.44,0])
        orb = Dot(loop.point_at_angle(PI/2),radius=0.19,color=POSITIVE)
        centripetal = Arrow([3.85,-0.44,0],[4.3,-0.44,0],color=POSITIVE,
                            stroke_width=4,buff=0)
        self.play(Create(loop),FadeIn(orb),run_time=1.2)
        self.play(MoveAlongPath(orb,loop),run_time=2.6,rate_func=linear)
        self.register(loop,orb,centripetal)
        self.big("Energy transforms -- total energy is conserved",
                 (0,-2.30),30,POSITIVE,BOLD,12.5)
        self.caption("Grade 10 / Period II: work, energy, circular motion and momentum.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def torque_gravity(self):
        self.start_topic(4,"GR 10 / PERIOD III","TORQUE, EQUILIBRIUM AND GRAVITY",
                         "Levers, centre of mass, Newtonian gravity and planetary motion")
        fulcrum = Polygon([-3.9,-1.60,0],[-3.15,-0.40,0],[-2.4,-1.60,0],
                          fill_color=SLAB,fill_opacity=0.85,stroke_color=DARK,
                          stroke_width=2.7)
        lever = Rectangle(width=5.2,height=0.16,color=DARK,
                          fill_color=SLAB,fill_opacity=1).move_to([-3.15,-0.42,0])
        mass1 = Square(side_length=0.63,color=SKETCH,fill_color=SKETCH,
                       fill_opacity=0.80).move_to([-5.20,-0.00,0])
        mass2 = Square(side_length=0.63,color=POSITIVE,fill_color=POSITIVE,
                       fill_opacity=0.80).move_to([-1.10,-0.00,0])
        levergroup=VGroup(lever,mass1,mass2)
        self.play(Create(fulcrum),Create(lever),FadeIn(mass1),FadeIn(mass2),
                  run_time=1.7)
        self.play(Rotate(levergroup,angle=0.12,about_point=[-3.15,-0.42,0]),
                  run_time=1.55)
        self.register(fulcrum,levergroup)
        star=Circle(radius=0.40,color="#C58D32",fill_color="#E6B354",
                    fill_opacity=1).move_to([3.72,-0.33,0])
        orbit=Ellipse(width=4.65,height=2.25,color=SKETCH,stroke_width=2.8)
        orbit.move_to([3.72,-0.33,0])
        earth=Dot([6.04,-0.33,0],radius=0.25,color=SKETCH)
        self.play(Create(orbit),FadeIn(star),FadeIn(earth),run_time=1.20)
        self.play(MoveAlongPath(earth,orbit),run_time=2.65,rate_func=linear)
        self.register(orbit,star,earth)
        self.big("Balanced forces  /  planetary attraction",
                 (0,-2.33),30,POSITIVE,BOLD,12.5)
        self.caption("Grade 10 / Period III: machines in equilibrium and the solar system.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def oscillations_waves(self):
        self.start_topic(5,"GR 11 / PERIOD I","OSCILLATIONS, WAVES AND SOUND",
                         "Springs, pendulums, wavelength, frequency and the Doppler effect")
        left_x=-6.0
        spring_points=[]
        for i in range(28):
            x=left_x + (3.5*i/27)
            y= -0.50 + (0.29*(-1)**i if 0<i<27 else 0)
            spring_points.append([x,y,0])
        spring=VMobject(stroke_color=SKETCH,stroke_width=3.4)
        spring.set_points_as_corners(spring_points)
        mass=Square(side_length=0.75,color=DARK,stroke_width=2.2,
                    fill_color=MODEL,fill_opacity=1).move_to([-2.13,-0.50,0])
        wall=self.rule((-6.1,-1.25),(-6.1,0.25),DARK,4)
        self.play(Create(wall),Create(spring),FadeIn(mass),run_time=1.7)
        self.play(mass.animate.shift(RIGHT*0.7),run_time=1.0)
        self.play(mass.animate.shift(LEFT*1.4),run_time=1.9,rate_func=there_and_back)
        self.register(wall,spring,mass)
        wave=FunctionGraph(lambda x: 0.60*np.sin(2.6*x),
                           x_range=[0.0,4.7,0.05],color=POSITIVE,
                           stroke_width=3.7).shift(RIGHT*0.58+DOWN*0.56)
        axis=self.rule((0.3,-0.56),(5.63,-0.56),MID,1.4)
        self.play(Create(axis),Create(wave),run_time=2.1)
        self.register(wave,axis)
        self.big("Oscillation generates waves; waves carry energy",
                 (0,-2.31),29,POSITIVE,BOLD,12.8)
        self.caption("Grade 11 / Period I: oscillators, mechanical waves, sound and Doppler.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def electricity_optics(self):
        self.start_topic(6,"GR 11 / PERIOD II","ELECTRICITY, MAGNETISM AND LIGHT",
                         "Charge, circuits, Coulomb / Ohm, electromagnetic light and lenses")
        # Left: circuit with a battery, resistor and two connecting conductors.
        wire=VGroup(
            self.rule((-5.55,-1.32),(-5.55,0.10),DARK,2.8),
            self.rule((-5.55,0.10),(-1.35,0.10),DARK,2.8),
            self.rule((-1.35,0.10),(-1.35,-1.32),DARK,2.8),
            self.rule((-5.55,-1.32),(-4.60,-1.32),DARK,2.8),
            self.rule((-3.90,-1.32),(-1.35,-1.32),DARK,2.8))
        battery=VGroup(self.rule((-4.55,-1.06),(-4.55,-1.57),SKETCH,3.0),
                       self.rule((-3.94,-1.18),(-3.94,-1.45),SKETCH,3.0))
        resistor=Rectangle(width=1.25,height=0.36,stroke_color=POSITIVE,
                           stroke_width=2.2,fill_color=MODEL,fill_opacity=1)
        resistor.move_to([-3.60,0.10,0])
        label=self.big("CIRCUITS",(-3.5,-2.06),31,DARK,BOLD,5.0)
        self.play(Create(wire),Create(battery),Create(resistor),run_time=2.1)
        self.register(wire,battery,resistor)
        # Right: optical refraction ray with a horizontal interface.
        surface=self.rule((0.58,-0.65),(6.30,-0.65),DARK,2.6)
        normal=DashedLine([3.35,0.91,0],[3.35,-2.10,0],color=MID,
                          dash_length=0.16)
        incident=Arrow([1.45,0.83,0],[3.35,-0.65,0],color=SKETCH,
                       buff=0,stroke_width=3.7)
        refracted=Arrow([3.35,-0.65,0],[4.10,-1.88,0],
                        color=POSITIVE,buff=0,stroke_width=3.7)
        self.play(Create(surface),Create(normal),run_time=1.1)
        self.play(Create(incident),Create(refracted),run_time=1.65)
        self.register(surface,normal,incident,refracted)
        self.caption("Grade 11 / Period II: electricity and magnetism; reflection and refraction.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def fluids_thermodynamics(self):
        self.start_topic(7,"GR 11 / PERIOD III","FLUIDS AND THERMODYNAMICS",
                         "Pressure, buoyancy, Bernoulli, heat transfer and engines")
        tank=Rectangle(width=3.7,height=2.3,stroke_color=DARK,stroke_width=2.6,
                       fill_color=WHITE,fill_opacity=1).move_to([-3.95,-0.37,0])
        water=Rectangle(width=3.59,height=1.45,stroke_width=0,
                        fill_color=GLASS,fill_opacity=0.84).move_to([-3.95,-0.79,0])
        p1=Arrow([-3.95,0.02,0],[-3.95,-0.40,0],color=SKETCH,
                 buff=0,stroke_width=3.8)
        p2=Arrow([-3.95,-0.63,0],[-3.95,-1.28,0],color=SKETCH,
                 buff=0,stroke_width=3.8)
        self.play(Create(tank),FadeIn(water),run_time=1.3)
        self.play(Create(p1),Create(p2),run_time=1.15)
        self.register(tank,water,p1,p2)
        chamber=Rectangle(width=2.6,height=2.05,stroke_color=DARK,stroke_width=3,
                          fill_color=MODEL,fill_opacity=0.65).move_to([3.68,-0.28,0])
        piston=self.rule((2.41,0.17),(4.95,0.17),DARK,7)
        heat=Arrow([3.68,-2.1,0],[3.68,-1.08,0],
                   color=NEGATIVE,stroke_width=5,buff=0)
        self.play(Create(chamber),Create(piston),run_time=1.25)
        self.play(Create(heat),run_time=0.75)
        self.register(chamber,piston,heat)
        self.big("Fluid forces",(-3.95,-2.10),30,SKETCH,BOLD,4.5)
        self.big("Heat and work",(3.68,-2.35),30,NEGATIVE,BOLD,4.3)
        self.caption("Grade 11 / Period III: fluid motion, temperature and heat engines.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)

    def period_map(self):
        self.start_topic(8,"VERIFY / THREE PERIODS","THE SCHOOL PHYSICS ROADMAP",
                         "An orientation using the 2026 Grade 10 and Grade 11 maps")
        left=self.big("GRADE 10",(-3.37,0.65),40,SKETCH,BOLD,5.2)
        right=self.big("GRADE 11",(3.37,0.65),40,POSITIVE,BOLD,5.2)
        centre=self.rule((0.0,-2.28),(0.0,0.93),LIGHT,2.2)
        self.play(Write(left),Write(right),Create(centre),run_time=1.2)
        self.register(centre)
        grade10=["P1   Motion and forces","P2   Energy and circular motion",
                 "P3   Torque and gravitation"]
        grade11=["P1   Oscillations and waves","P2   Electricity, magnetism, light",
                 "P3   Fluids and thermodynamics"]
        for i in range(3):
            y=-0.32-i*0.82
            l=self.big(grade10[i],(-3.43,y),30,DARK,NORMAL,6.25)
            rr=self.big(grade11[i],(3.38,y),30,DARK,NORMAL,6.25)
            self.play(Write(l),Write(rr),run_time=1.07)
            self.wait(0.65)
        self.caption("The Physics 9 measurement course is the foundation for this journey.")
        self.wait(7.0)


# ---------------------------------------------------------------------------
# V4: Grade 9 Class 2 enlarged, with fixed CAD HUD and reserved safe zones.
# Content deliberately remains Week 1's measurement sequence. No new topics
# are added here; this class is a magnified iteration on the accepted V3.
# ---------------------------------------------------------------------------

class Physics9CAD_MeasurementLarge(Physics9CAD_Measurement):
    """Bigger geometry and lettering with explicit margins in each frame."""
    LESSON_LABEL = "CLASS 02 -- FROM OBSERVATION TO MEASUREMENT"
    COVER_TITLE = "MEASUREMENT: ESTIMATE AND VERIFY"
    HUD_TITLE_SIZE = 33
    HUD_SUB_SIZE = 22
    # Diagram stage safe area: x in [-6.55,6.55], y in [-2.40,2.40].
    # Fixed HUD y>2.75; fixed captions y around -3.10; legend y<-3.90.
    SAFE_X = 6.55
    SAFE_Y = 2.40

    def large_text(self, content, xy, size=35, color=DARK, bold=False, width=11.9):
        t = self.label(content, xy, size, color, bold)
        if t.width > width: t.scale_to_fit_width(width)
        if (t.get_left()[0] < -self.SAFE_X - 0.05 or
            t.get_right()[0] > self.SAFE_X + 0.05 or
            t.get_top()[1] > self.SAFE_Y + 0.05 or
            t.get_bottom()[1] < -self.SAFE_Y - 0.05):
            raise ValueError(f"V4 text outside teaching safe area: {content!r}")
        return t

    def caption(self, line, color=DARK):
        # Keep a physical gap between diagrams, explanation caption and legend.
        if self.note is not None:
            self.play(FadeOut(self.note), run_time=0.35)
            self.note = None
        back = RoundedRectangle(
            width=13.52, height=0.78, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.97,
            stroke_color=LIGHT, stroke_width=1.2,
        ).move_to([0,-3.16,0])
        t = self.text(line, 30, NORMAL, color).move_to(back)
        if t.width > 12.90: t.scale_to_fit_width(12.90)
        self.note=VGroup(back,t)
        self.add_fixed_in_frame_mobjects(self.note)
        self.play(FadeIn(back),Write(t),run_time=1.15)
        return self.note

    def workflow(self):
        self.set_phase(1, "FIVE MEASUREMENT STEPS", SKETCH)
        names=["OBSERVE","ESTIMATE","MEASURE","RECORD","COMPARE"]
        x_positions=[-5.23,-2.61,0.01,2.63,5.25]
        for i,name in enumerate(names):
            x=x_positions[i]
            circ=Circle(radius=0.50,stroke_color=SKETCH,stroke_width=3.0)
            circ.move_to([x,0.65,0])
            n=self.large_text(str(i+1),(x,0.65),39,SKETCH,True,0.65)
            label=self.large_text(name,(x,-0.43),30,DARK,True,2.30)
            self.play(Create(circ),Write(n),Write(label),run_time=0.94)
            self.register(circ)
            if i<4:
                arr=Arrow([x+0.58,0.65,0],[x_positions[i+1]-0.60,0.65,0],
                          stroke_width=3.2,color=POSITIVE,buff=0,
                          max_tip_length_to_length_ratio=0.22)
                self.play(Create(arr),run_time=0.42)
                self.register(arr)
            self.wait(self.MICRO_PAUSE)
        self.caption("Estimate first. Measure using an instrument. Report value AND unit.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def ruler(self):
        self.set_phase(2, "LENGTH -- LARGE RULER", SKETCH)
        x0,x1,y=-5.85,5.85,-0.64
        ruler=Rectangle(width=x1-x0,height=0.66,color=DARK,
                        stroke_width=2.5,fill_color=MODEL,fill_opacity=1)
        ruler.move_to([(x0+x1)/2,y,0])
        ticks=VGroup()
        for i in range(51):
            x=x0+(x1-x0)*i/50.0
            depth=0.42 if i%10==0 else (0.32 if i%5==0 else 0.20)
            ticks.add(self.rule((x,y+0.32),(x,y+0.32-depth),DARK,1.65))
        self.play(Create(ruler),Create(ticks),run_time=2.45)
        self.register(ruler,ticks)
        start=self.large_text("0 cm",(x0,-1.63),32,MID,False,1.15)
        end=self.large_text("50 cm",(x1,-1.63),32,MID,False,1.40)
        measured_x=x0+(x1-x0)*(46/50.0)
        measure=self.rule((x0,0.58),(measured_x,0.58),SKETCH,7.0)
        bracket_l=self.rule((x0,0.21),(x0,0.90),SKETCH,3.1)
        bracket_r=self.rule((measured_x,0.21),(measured_x,0.90),SKETCH,3.1)
        self.play(Write(start),Write(end),run_time=0.85)
        self.play(Create(measure),Create(bracket_l),Create(bracket_r),
                  run_time=2.25)
        self.register(measure,bracket_l,bracket_r)
        value=self.math(r"d=46\,\mathrm{cm}=0.46\,\mathrm{m}",
                        56,POSITIVE).move_to([0,1.70,0])
        if value.width > 11.9:value.scale_to_fit_width(11.9)
        self.play(Write(value),run_time=1.80)
        self.register(value)
        self.wait(self.READING_PAUSE)
        self.caption("The 46 cm endpoint is marked with 1 cm subdivisions.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def stopwatch(self):
        self.set_phase(3, "TIME -- LARGE STOPWATCH", SKETCH)
        centre=np.array([-3.33,-0.28,0])
        radius=1.79
        dial=Circle(radius=radius,color=DARK,stroke_width=4.5).move_to(centre)
        markers=VGroup()
        for angle in np.linspace(0,TAU,13)[:-1]:
            p=centre+radius*0.77*np.array([np.sin(angle),np.cos(angle),0])
            q=centre+radius*0.94*np.array([np.sin(angle),np.cos(angle),0])
            markers.add(Line(p,q,color=DARK,stroke_width=3.0))
        hand=Line(centre,centre+1.45*UP,color=SKETCH,stroke_width=5.2)
        knob=RoundedRectangle(width=0.70,height=0.24,corner_radius=0.09,
                              color=DARK,fill_color=SLAB,fill_opacity=1)
        knob.move_to(centre+UP*1.98)
        self.play(Create(dial),Create(markers),FadeIn(knob),Create(hand),
                  run_time=1.70)
        self.play(Rotate(hand,angle=-TAU*0.32,about_point=centre),
                  run_time=3.20,rate_func=linear)
        self.register(dial,markers,knob,hand)
        t=self.math(r"t=3.2\,\mathrm{s}",62,POSITIVE).move_to([3.12,1.16,0])
        self.play(Write(t),run_time=1.15);self.register(t)
        self.large_text("Quantity: time",(3.20,0.05),35,DARK,True,5.25)
        self.large_text("Tool: stopwatch",(3.20,-0.83),35,DARK,False,5.35)
        self.large_text("10 s / revolution",(3.20,-1.67),31,SKETCH,False,5.45)
        self.wait(self.READING_PAUSE)
        self.caption("This example represents 3.2 seconds of elapsed time.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def record(self):
        self.set_phase(4, "WRITE THE DATA -- CLEARLY", POSITIVE)
        headers=["QUANTITY","VALUE","UNIT","INSTRUMENT"]
        examples=[
            ["Length","0.46","m","Ruler"],
            ["Time","3.2","s","Stopwatch"],
            ["Mass","0.80","kg","Balance"],
        ]
        widths=[3.10,2.12,1.75,4.28]
        startx=-sum(widths)/2
        for row_id,words in enumerate([headers]+examples):
            x=startx
            for col_id,word in enumerate(words):
                wid=widths[col_id]
                center=[x+wid/2,1.65-row_id*1.02,0]
                box=Rectangle(width=wid,height=1.02,stroke_color=LIGHT,
                              stroke_width=1.8,
                              fill_color=TERRAIN if row_id==0 else WHITE,
                              fill_opacity=1).move_to(center)
                t=self.text(word,33 if row_id==0 else 37,
                            BOLD if row_id==0 else NORMAL,
                            SKETCH if row_id==0 else DARK).move_to(center)
                if t.width>wid-0.28:t.scale_to_fit_width(wid-0.28)
                self.play(Create(box),Write(t),run_time=0.58)
                self.register(box,t)
                x+=wid
            self.wait(1.85)
        self.caption("These numbers are illustrative: record your own measurements.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def compare(self):
        self.set_phase(5, "ESTIMATE VS MEASUREMENT", NEGATIVE)
        est=self.rule((-5.5,0.75),(5.2,0.75),SKETCH,8)
        mes=self.rule((-5.5,-0.72),(4.33,-0.72),POSITIVE,8)
        label1=self.large_text("ESTIMATE: 0.50 m",(0,1.53),39,SKETCH,True,12)
        self.play(Write(label1),Create(est),run_time=1.55)
        self.register(est)
        self.wait(self.READING_PAUSE)
        label2=self.large_text("MEASURED: 0.46 m",(0,-0.20),39,POSITIVE,True,12)
        self.play(Write(label2),Create(mes),run_time=1.55)
        self.register(mes)
        equation=self.math(r"|0.50-0.46|=0.04\,\mathrm{m}",
                           54,NEGATIVE).move_to([0,-1.95,0])
        if equation.width>11.85:equation.scale_to_fit_width(11.85)
        self.play(Write(equation),run_time=1.60)
        self.register(equation)
        self.caption("The difference is 0.04 m. Discuss what caused it.")
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.stage_clear()

    def activity(self):
        self.set_phase(6, "PAIRED MEASUREMENT TASK", POSITIVE)
        steps=[
            "1. Estimate the desk length.",
            "2. Use a ruler or measuring tape.",
            "3. Estimate the duration of a short walk.",
            "4. Measure it with a stopwatch.",
            "5. Record quantity, value, unit and tool.",
            "6. Compare your prediction and result.",
        ]
        lines=VGroup(*[self.text(line,36,NORMAL,DARK) for line in steps])
        lines.arrange(DOWN,aligned_edge=LEFT,buff=0.28).move_to([0,-0.10,0])
        if lines.width>12.65:lines.scale_to_fit_width(12.65)
        if lines.get_top()[1] > self.SAFE_Y or lines.get_bottom()[1]<-self.SAFE_Y:
            raise ValueError("V4 workshop text would intrude into HUD/caption")
        for row in lines:
            self.play(Write(row),run_time=1.08)
            self.wait(1.05)
        self.register(lines)
        self.caption("Exit ticket: What makes a measurement scientifically useful?")
        self.wait(8.0)
        self.stage_clear()
