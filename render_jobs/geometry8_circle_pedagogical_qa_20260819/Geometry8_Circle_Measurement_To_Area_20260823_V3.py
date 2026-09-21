#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Geometry 8 — Circle measurement to area, V3 cinematic rebuild.

A full redesign where each concept is constructed through motion: object
measurement, experimental pi, radius/diameter, circumference unwrapping, area
rearrangement, and individually animated exercises.

Target: Manim Community Edition 0.20.1.
"""
from __future__ import annotations

from Geometry8_Circle_Measurement_To_Area_20260823_V2 import Geometry8CircleMeasurementArea20260823V2
from Geometry8_Circle_V3_Primitives import CircleV3PrimitivesMixin
from Geometry8_Circle_V3_Measurement import CircleV3MeasurementMixin
from Geometry8_Circle_V3_Area import CircleV3AreaMixin
from Geometry8_Circle_V3_Exercises import CircleV3ExercisesMixin


class Geometry8CircleMeasurementArea20260823V3(
    CircleV3MeasurementMixin,
    CircleV3AreaMixin,
    CircleV3ExercisesMixin,
    CircleV3PrimitivesMixin,
    Geometry8CircleMeasurementArea20260823V2,
):
    """Dedicated fluid-animation rebuild: measurement -> pi -> C -> A -> practice."""

    def construct(self) -> None:
        self.opening_measurement_bridge_v3()
        self.measure_three_objects_v3()
        self.discover_pi_v3()
        self.elements_radius_diameter_v3()
        self.unwrap_circumference_v3()
        self.boundary_to_surface_v3()
        self.derive_area_sectors_v3()
        self.exercise_diameter_v3()
        self.exercise_radius_area_v3()
        self.exercise_inverse_and_context_v3()
        self.lesson_summary_v3()
