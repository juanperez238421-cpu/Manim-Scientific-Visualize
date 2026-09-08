#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Accuracy patch for the dihedral-system lesson.

Keeps the complete ISO A / ISO E animation from diedric_iso_ntc1777.py and
updates the Colombia section after checking the current ICONTEC catalogue.
"""
from pathlib import Path
import sys

# Manim loads scene files by path, so make the sibling base scene importable
# explicitly in Docker/GitHub Actions instead of relying on the repository root
# being installed as a Python package.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from diedric_iso_ntc1777 import *


class DihedralISOProjectionColombia2026(DihedralISOProjectionNTC1777):
    """Full lesson with the 2026 Colombia standards note corrected."""

    def colombia(self):
        h = self.header(
            8,
            "COLOMBIA — NORMATIVE CHECK 2026",
            "NTC means Colombian Technical Standard. It is not, by itself, the same thing as a law or regulation.",
        )
        self.add(h)

        legacy = self.card(
            "NTC 1777:2001 — IMPORTANT REFERENCE",
            [
                "Technical drawing — general principles of presentation.",
                "Equivalent (EQV) to ISO 128 in that edition.",
                "It explicitly accepts BOTH first-angle and third-angle projection.",
                "First-angle = formerly method E; third-angle = formerly method A.",
            ],
            6.85,
            3.55,
        )

        current = self.card(
            "CURRENT ICONTEC CATALOGUE — CHECKED 2026",
            [
                "NTC-ISO 128-3:2022 is listed as VIGENTE.",
                "It covers views, sections and cuts in product documentation.",
                "NTC 1915:1984 is also listed as VIGENTE for building-drawing projection methods.",
                "So: do not describe NTC 1777 as 'ISO A only' or as 'the current legislation'.",
            ],
            6.85,
            3.55,
        )

        VGroup(legacy, current).arrange(RIGHT, buff=0.38).move_to(DOWN * 0.25)
        self.play(FadeIn(legacy), FadeIn(current), run_time=1.0)
        self.wait(4.8)

        conclusion = self.pill(
            "COLOMBIA: READ THE PROJECTION SYMBOL — BOTH METHODS MAY APPEAR",
            21,
        ).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(conclusion), run_time=0.7)
        self.wait(4.0)
        self.clear()


# Preview:
# manim -pql render_jobs/technical_drawing_diedric_iso_20260908/diedric_iso_colombia2026.py DihedralISOProjectionColombia2026 --disable_caching
# Final:
# manim -pqh render_jobs/technical_drawing_diedric_iso_20260908/diedric_iso_colombia2026.py DihedralISOProjectionColombia2026 --disable_caching
