#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle Measurement to Area V4 Senior Projector QA.

V4 is a readability/camera redesign of the audited V3 lesson. It keeps the same
mathematics and evidence sequence while making every construction large enough
for classroom projection and adding explicit think/read pauses and zooms.
"""
from __future__ import annotations

from Geometry8_Circle_Measurement_To_Area_20260823_V3 import Geometry8CircleMeasurementArea20260823V3
from Geometry8_Circle_V4_Senior_QA import CircleV4SeniorQAMixin
from Geometry8_Circle_V4_Senior_QA_Fixes import CircleV4SeniorQAFixesMixin


class Geometry8CircleMeasurementArea20260823V4(
    CircleV4SeniorQAFixesMixin,
    CircleV4SeniorQAMixin,
    Geometry8CircleMeasurementArea20260823V3,
):
    """Senior QA projector edition: large type, large figures, pauses, camera focus."""

    def construct(self) -> None:
        self.opening_measurement_bridge_v4()
        self.measure_three_objects_v4()
        self.discover_pi_v4()
        self.elements_radius_diameter_v4()
        self.unwrap_circumference_v4()
        self.boundary_to_surface_v4()
        self.derive_area_sectors_v4()
        self.exercise_diameter_v4()
        self.exercise_radius_area_v4()
        self.exercise_inverse_and_context_v4()
        self.lesson_summary_v4()
