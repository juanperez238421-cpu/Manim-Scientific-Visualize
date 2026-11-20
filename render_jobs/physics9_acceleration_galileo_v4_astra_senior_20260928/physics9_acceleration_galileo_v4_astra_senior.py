#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Acceleration + Galileo V4 ASTRA SENIOR.

Senior rebuild of the verified V3 render:
- classroom-legible type,
- no persistent micro-panels,
- no teaching text below graph x-axes,
- one focus state at a time,
- all 12 acceleration intervals retained,
- rigorous constant-acceleration and Galileo logic.
"""

from __future__ import annotations

from astra_sections_core import AstraCoreSections
from astra_sections_advanced import AstraAdvancedSections
from astra_visual_mixin import AstraVisualMixin
from physics9_acceleration_graph_galileo_v3_opusvisual import (
    Physics9AccelerationGraphGalileoV3OpusVisual,
    PROFILE,
    ACCEL_INTERVALS,
)


class Physics9AccelerationGalileoV4AstraSenior(
    AstraCoreSections,
    AstraAdvancedSections,
    AstraVisualMixin,
    Physics9AccelerationGraphGalileoV3OpusVisual,
):
    """ASTRA senior classroom scene."""

    def validate_lesson_data(self) -> None:
        Physics9AccelerationGraphGalileoV3OpusVisual.validate_lesson_data(self)
        assert len(PROFILE) == 13
        assert len(ACCEL_INTERVALS) == 12
        assert all(d["t1"] > d["t0"] for d in ACCEL_INTERVALS)
        assert all(v >= 0 for _, v in PROFILE)
        assert abs(self.total_distance_km() - self.distance_km_at(120.0)) < 1e-9

    def construct(self) -> None:
        self.opening()
        self.section_1_recall_velocity_graph()
        self.section_2_meaning_of_acceleration()
        self.section_3_build_acceleration_graph_first_half()
        self.section_4_build_acceleration_graph_second_half()
        self.section_5_read_full_acceleration_graph()
        self.section_6_constant_acceleration_equations()
        self.section_7_position_equation_from_area()
        self.section_8_why_galileo_inclined_plane()
        self.section_9_galileo_measurement_prediction()
        self.standard_closing(
            "Acceleration appears as the slope of v(t), and constant acceleration from rest produces x proportional to t squared."
        )
