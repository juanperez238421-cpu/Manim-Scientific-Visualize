#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 inclined-plane laboratory V2.

This render-safe revision replaces the opening-mode MathTex badge from V1 with
normal Text inside a classroom panel.  The V1 badge embedded an em dash inside
LaTeX \text{}, which is not portable in the ManimCE TeX pipeline.  All
laboratory content and measurement logic are inherited unchanged.
"""
from manim import *

from Physics9_Inclined_Plane_Lab_Stopwatch_Sensors_FINAL import (
    Physics9InclinedPlaneLabBase,
    DARK_GRAY,
    VERY_LIGHT,
)


class Physics9InclinedPlaneLabV2Base(Physics9InclinedPlaneLabBase):
    def opening(self, mode="BOTH"):
        kicker = self.txt("PHYSICS 9 | EXPERIMENTAL KINEMATICS", 28, BOLD)
        title = self.txt("GALILEO-INSPIRED INCLINED-PLANE LAB", 44, BOLD)
        subtitle = self.txt("Measure position vs time on a real classroom ramp", 27, NORMAL, DARK_GRAY)

        if mode == "STOPWATCH":
            mode_text = "VERSION A  |  STOPWATCH — NO SENSORS REQUIRED"
        elif mode == "SENSORS":
            mode_text = "VERSION B  |  PHOTOGATES / MOTION SENSOR"
        else:
            mode_text = "TWO VERSIONS  |  STOPWATCH + SENSORS"

        # Normal Text is intentional here: this badge is prose, not mathematics.
        mode_box = self.panel(9.7, 0.92, fill=VERY_LIGHT)
        mode_label = self.txt(mode_text, 25, BOLD, DARK_GRAY)
        self.fit(mode_label, 9.15, 0.50)
        mode_label.move_to(mode_box)
        mode_badge = VGroup(mode_box, mode_label)

        question = self.formula_panel(
            r"\boxed{\text{How does position }x\text{ along the ramp change with time }t\text{?}}",
            width=11.1,
            height=1.05,
            size=31,
        )
        group = VGroup(kicker, title, subtitle, mode_badge, question).arrange(DOWN, buff=0.36)
        self.fit(group, 13.6, 6.8)
        group.move_to(ORIGIN)

        self.play_t(FadeIn(kicker), run_time=0.65)
        self.play_t(Write(title), run_time=0.95)
        self.play_t(FadeIn(subtitle), run_time=0.60)
        self.play_t(FadeIn(mode_badge), run_time=0.65)
        self.play_t(FadeIn(question), run_time=0.70)
        self.wait_t(2.0)
        self.play_t(FadeOut(group), run_time=0.60)


class Physics9InclinedPlaneLabMasterV2(Physics9InclinedPlaneLabV2Base):
    def construct(self):
        self.opening("BOTH")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.stopwatch_protocol(3)
        self.stopwatch_trial(4)
        self.stopwatch_analysis(5)
        self.sensor_protocol(6)
        self.sensor_acquisition(7)
        self.sensor_analysis(8)
        self.compare_methods(9)
        self.scientific_conclusion(10, "BOTH")
        self.lab_checklist(11, "BOTH")


class Physics9InclinedPlaneLabStopwatchV2(Physics9InclinedPlaneLabV2Base):
    def construct(self):
        self.opening("STOPWATCH")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.stopwatch_protocol(3)
        self.stopwatch_trial(4)
        self.stopwatch_analysis(5)
        self.scientific_conclusion(6, "STOPWATCH")
        self.lab_checklist(7, "STOPWATCH")


class Physics9InclinedPlaneLabSensorsV2(Physics9InclinedPlaneLabV2Base):
    def construct(self):
        self.opening("SENSORS")
        self.experimental_goal(1)
        self.physical_setup(2)
        self.sensor_protocol(3)
        self.sensor_acquisition(4)
        self.sensor_analysis(5)
        self.scientific_conclusion(6, "SENSORS")
        self.lab_checklist(7, "SENSORS")
