#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Visual-QA refinement for the Physics 9 Galileo masterclass.

This version inherits the complete V1 pedagogical sequence and replaces only
its laboratory-apparatus section with a cleaner, more explicit reconstruction.
The change keeps all equation derivations, graph connections, validation
assertions and student challenge from the validated base scene.
"""

from __future__ import annotations

import numpy as np
from manim import *

from Physics9_Galileo_Inclined_Plane_MUA_FINAL import (
    Physics9GalileoInclinedPlaneFinal,
    BLACK_TEXT,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    RUN,
    RUN_FAST,
    RUN_SLOW,
    PAUSE_READ,
    PAUSE_EXPLAIN,
)


class Physics9GalileoInclinedPlaneFinalV2(Physics9GalileoInclinedPlaneFinal):
    """Final classroom scene with refined Galileo laboratory reconstruction."""

    def galileo_apparatus(self):
        self.set_header(
            3,
            "LAB RECONSTRUCTION: RAMP + BALL + DISTANCE MARKS + WATER CLOCK",
            "Repeat the release from rest and compare the distance traveled after equal intervals of time.",
        )

        # ------------------------------------------------------------------
        # Main inclined-plane apparatus
        # ------------------------------------------------------------------
        start = np.array([-6.05, -2.00, 0.0])
        end = np.array([2.35, 1.50, 0.0])
        ramp = Line(start, end, color=BLACK, stroke_width=5)
        floor = Line(np.array([-6.55, -2.00, 0.0]), np.array([3.00, -2.00, 0.0]), color=BLACK, stroke_width=2)
        support = Line(end, np.array([2.35, -2.00, 0.0]), color=MID_GRAY, stroke_width=2)

        # Horizontal reference and angle marker make the geometry explicit.
        ref = DashedLine(start, start + RIGHT * 2.15, color=LIGHT_GRAY, stroke_width=1.4)
        theta = Angle(ref, ramp, radius=0.52, color=BLACK, stroke_width=1.8)
        theta_label = self.math(r"\theta", 28).next_to(theta, UR, buff=0.05)

        ball = Circle(
            radius=0.19,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(end)
        release = self.txt("release from rest", 19, BOLD).next_to(ball, UP + LEFT, buff=0.16)
        v0 = self.math(r"v_0=0", 28).next_to(release, DOWN, buff=0.08)

        # Measurement scale follows the ramp direction.
        direction = (end - start) / np.linalg.norm(end - start)
        normal = np.array([-direction[1], direction[0], 0.0])
        scale_offset = -0.28 * normal
        ruler = Line(start + scale_offset, end + scale_offset, color=MID_GRAY, stroke_width=1.4)
        marks = VGroup()
        for u in np.linspace(0.0, 1.0, 9):
            p = start + u * (end - start) + scale_offset
            tick = Line(p - normal * 0.08, p + normal * 0.08, color=MID_GRAY, stroke_width=1.4)
            marks.add(tick)
        scale_label = self.txt("distance scale", 17, color=DARK_GRAY).next_to(ruler, DOWN, buff=0.12)

        # ------------------------------------------------------------------
        # Water-clock panel — positioned entirely inside its own safe zone.
        # ------------------------------------------------------------------
        clock_panel = self.panel(3.15, 3.05, fill=WHITE)
        clock_panel.move_to(RIGHT * 5.12 + DOWN * 0.45)

        clock_title = self.txt("WATER CLOCK", 21, BOLD)
        clock_title.next_to(clock_panel.get_top(), DOWN, buff=0.20)

        upper = RoundedRectangle(
            width=1.25,
            height=1.25,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        )
        upper.move_to(clock_panel.get_center() + UP * 0.25)

        # Critical V2 fix: the liquid is centered on the vessel before aligning
        # to its lower edge, so it cannot remain at the scene origin.
        water = Rectangle(
            width=1.08,
            height=0.58,
            stroke_width=0,
            fill_color=LIGHT_GRAY,
            fill_opacity=1,
        )
        water.move_to(upper)
        water.align_to(upper, DOWN).shift(UP * 0.08)

        nozzle = Line(upper.get_bottom(), upper.get_bottom() + DOWN * 0.24, color=BLACK, stroke_width=1.8)
        drops = VGroup(
            Dot(nozzle.get_end() + DOWN * 0.12, radius=0.045, color=BLACK),
            Dot(nozzle.get_end() + DOWN * 0.29, radius=0.035, color=MID_GRAY),
        )
        collector = RoundedRectangle(
            width=1.05,
            height=0.48,
            corner_radius=0.08,
            stroke_color=BLACK,
            stroke_width=1.6,
            fill_color=WHITE,
            fill_opacity=1,
        ).next_to(drops, DOWN, buff=0.10)

        clock_note = self.txt("equal water volume = equal time", 16, BOLD)
        clock_note.next_to(clock_panel.get_bottom(), UP, buff=0.18)

        # ------------------------------------------------------------------
        # Procedure strip: compact enough not to compete with the apparatus.
        # ------------------------------------------------------------------
        procedure = self.note_panel(
            "MEASUREMENT CYCLE",
            [
                "1. Same starting point",
                "2. Release — do not push",
                "3. Mark position at equal times",
                "4. Repeat and compare",
            ],
            width=3.55,
            title_size=20,
            body_size=17,
        )
        procedure.move_to(RIGHT * 4.88 + UP * 2.12)

        lab_question = self.formula_panel(
            r"\text{How does }\Delta x\text{ change when }\Delta t\text{ is fixed?}",
            width=7.2,
            height=0.88,
            size=28,
        )
        lab_question.move_to(LEFT * 2.00 + DOWN * 3.15)

        apparatus = VGroup(ramp, floor, support, ref, theta, theta_label, ruler, marks, scale_label)
        clock = VGroup(clock_panel, clock_title, upper, water, nozzle, drops, collector, clock_note)

        self.play(Create(ramp), Create(floor), Create(support), run_time=RUN)
        self.play(Create(ref), Create(theta), FadeIn(theta_label), run_time=RUN_FAST)
        self.play(FadeIn(ruler), FadeIn(marks), FadeIn(scale_label), run_time=RUN_FAST)
        self.play(FadeIn(ball), FadeIn(release), FadeIn(v0), run_time=RUN_FAST)
        self.play(FadeIn(clock), run_time=RUN)
        self.play(FadeIn(procedure), FadeIn(lab_question), run_time=RUN)
        self.wait(PAUSE_READ)

        # The rolling object accelerates down the ramp. The camera remains fixed
        # so students can compare spatial intervals directly.
        motion_path = Line(end, start + direction * 0.70)
        self.play(
            MoveAlongPath(ball, motion_path),
            run_time=2.7,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()


# Preview:
# manim -pql Physics9_Galileo_Inclined_Plane_MUA_FINAL_V2.py Physics9GalileoInclinedPlaneFinalV2 --disable_caching
# Final:
# manim -pqh Physics9_Galileo_Inclined_Plane_MUA_FINAL_V2.py Physics9GalileoInclinedPlaneFinalV2 --disable_caching
