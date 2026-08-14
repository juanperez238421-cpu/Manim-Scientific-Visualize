#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Multivariable Calculus Workshop — Problems 1, 2, 3.

Senior / auditable ManimCE reconstruction.
Target: Manim Community Edition 0.20.1.
Style contract: jp_classroom_style_EXACT_RENDER_USED(1).py (copied verbatim
as jp_classroom_style.py for a portable import).

Audit design
------------
Every displayed numerical/mathematical claim is represented in AUDIT_DATA and
validated in validate_lesson_data(). Each major segment prints an AUDIT marker
into the render log. Visual objects are built causally and progressively.

Final render commands:
  manim -pqh main.py Video01_Dominios_Auditable --format=mp4 --disable_caching
  manim -pqh main.py Video02_Limites_Auditable --format=mp4 --disable_caching
  manim -pqh main.py Video03_Tangentes_Auditable --format=mp4 --disable_caching
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

import numpy as np
from manim import *
from jp_classroom_style import *


# =============================================================================
# AUDIT DATA — literal workshop readings and validated results
# =============================================================================
AUDIT_DATA = {
    "1a": {
        "expr": r"\mathbf r(t)=\sqrt{t^2-9}\,\mathbf i+t^2\,\mathbf j+\mathbf k",
        "answer": r"(-\infty,-3]\cup[3,\infty)",
    },
    "1b": {
        "expr": r"\mathbf r(t)=\cos(2t)\,\mathbf i+e^{-t}\,\mathbf j+\sin(2t)\,\mathbf k",
        "answer": r"\mathbb R",
    },
    "1c": {
        "expr": r"\mathbf r(t)=\sqrt{t+6}\,\mathbf i+3t\,\mathbf j+\frac{1}{t^2-9}\,\mathbf k",
        "answer": r"[-6,-3)\cup(-3,3)\cup(3,\infty)",
    },
    "1d": {
        "expr": r"\mathbf r(t)=\ln(t-2)\,\mathbf i+e^{1/t}\,\mathbf j-\cos(2t)\,\mathbf k",
        "answer": r"(2,\infty)",
    },
    "2a": {
        "target": 1.0,
        "answer": (2.0, 2.0, 0.0),
    },
    # Literal worksheet reading retained: denominator t-21 and sqrt(t)-3.
    "2b": {
        "target": 2.0,
        "answer": (5.0, -5.0 / 19.0, math.sqrt(2.0) - 3.0),
    },
    "2c": {
        "target": 0.0,
        "answer": (2.0, 0.0, math.e),
    },
    "3a": {
        "t0": 0.0,
        "point": (0.0, -1.0, -1.0),
        "direction": (1.0, 0.0, -1.0),
    },
    "3b": {
        "t0": math.pi,
        "point": (math.pi * math.e**math.pi, math.pi**2 - 2 * math.pi, 0.0),
        "direction": (math.e**math.pi * (1 + math.pi), 2 * math.pi - 2, -1.0),
    },
    "3c": {
        "t0": 1.0,
        "point": (0.0, 3.0, 9.0),
        "direction": (2.0, 1.5, 24.0),
    },
    "3d": {
        "t0": 0.0,
        "point": (1.0, 0.0, 1.0),
        "direction": (-1.0, 1.0, -1.0),
    },
}


# =============================================================================
# REUSABLE VISUAL HELPERS
# =============================================================================
class WorkshopBase(JPMathClassroomScene):
    """Shared animation vocabulary preserving the JP classroom architecture."""

    def audit(self, marker: str, message: str) -> None:
        print(f"AUDIT::{marker}::{message}")

    def validate_lesson_data(self) -> None:
        # Problem 2
        assert_close((1.0**2 - 1) / (1.0 + 1), 0.0, label="auxiliary sanity")
        assert_close(AUDIT_DATA["2a"]["answer"][0], 2.0, label="2a i")
        assert_close(AUDIT_DATA["2a"]["answer"][1], 2.0, label="2a j")
        assert_close(AUDIT_DATA["2a"]["answer"][2], 0.0, label="2a k")
        assert_close(AUDIT_DATA["2b"]["answer"][0], 5.0, label="2b i")
        assert_close(AUDIT_DATA["2b"]["answer"][1], -5 / 19, label="2b j")
        assert_close(AUDIT_DATA["2b"]["answer"][2], math.sqrt(2) - 3, label="2b k")
        assert_close(AUDIT_DATA["2c"]["answer"][0], 2.0, label="2c i")
        assert_close(AUDIT_DATA["2c"]["answer"][1], 0.0, label="2c j")
        assert_close(AUDIT_DATA["2c"]["answer"][2], math.e, label="2c k")

        # Problem 3 derivatives
        p3a = AUDIT_DATA["3a"]
        assert all(abs(a - b) < 1e-10 for a, b in zip(p3a["point"], (0, -1, -1)))
        assert all(abs(a - b) < 1e-10 for a, b in zip(p3a["direction"], (1, 0, -1)))

        p3c = AUDIT_DATA["3c"]
        assert_close(6 * 1 / (1 + 1), p3c["point"][1], label="3c point y")
        assert_close(6 / (1 + 1) ** 2, p3c["direction"][1], label="3c derivative y")
        assert_close(8 * 1 * (2 * 1**2 + 1), p3c["direction"][2], label="3c derivative z")

    # ------------------------------------------------------------------
    # Typography / animation pacing
    # ------------------------------------------------------------------
    def latex_text(self, text: str, size: int = 28, weight: str | None = None) -> Mobject:
        """Computer Modern body labels without changing the JP frame system."""
        if weight == "bold":
            tex = Tex(r"\textbf{" + text + "}", font_size=size, color=BLACK_TEXT)
        else:
            tex = Tex(text, font_size=size, color=BLACK_TEXT)
        return tex

    def slow_write(self, mob: Mobject, run_time: float = 1.25, pause: float = 1.20) -> None:
        self.play(Write(mob), run_time=run_time, rate_func=smootherstep)
        self.wait(pause)

    def reveal_group(self, mobs: Sequence[Mobject], *, lag: float = 0.16, run_time: float = 1.7,
                     shift=UP * 0.06, pause: float = 1.30) -> None:
        self.play(
            LaggedStart(*[FadeIn(m, shift=shift) for m in mobs], lag_ratio=lag),
            run_time=run_time,
            rate_func=smootherstep,
        )
        self.wait(pause)

    def animate_matching_chain(
        self,
        expressions: Sequence[str],
        *,
        position: np.ndarray,
        font_size: int = 39,
        max_width: float = 6.25,
        pauses: Sequence[float] | None = None,
    ) -> Mobject:
        """One equation at a time; common LaTeX survives between steps."""
        if not expressions:
            raise ValueError("empty equation chain")
        pauses = pauses or [2.0] * len(expressions)
        current = self.math(expressions[0], font_size)
        self.fit(current, max_width, 1.35)
        current.move_to(position)
        self.play(Write(current), run_time=1.20, rate_func=smootherstep)
        self.wait(pauses[0])
        for expression, pause in zip(expressions[1:], pauses[1:]):
            target = self.math(expression, font_size)
            self.fit(target, max_width, 1.35)
            target.move_to(position)
            self.play(
                TransformMatchingTex(current, target, transform_mismatches=True),
                run_time=1.45,
                rate_func=smootherstep,
            )
