"""Physics 9 — City-to-city motion, V4 professional classroom pacing.

Purpose
-------
This scene deliberately reuses the validated V3 physical figures, car geometry,
road model, equations and graph logic, but changes the delivery rhythm so the
video works as a teacher-led classroom explanation rather than a fast slide deck.

Design changes from V3
----------------------
- Preserve the exact V3 figures and numerical physics.
- Increase motion duration without changing physical meaning.
- Increase reading / thinking pauses substantially.
- Add small semantic holds after equation transforms, highlights and reveals.
- Use softer staged exits between sections instead of abrupt full-screen clears.
- Keep the existing modular section architecture and LESSON_TIME_SCALE support.

Render target (ManimCE 0.20.1):
    manim -pqh physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4

Accelerated QA:
    LESSON_TIME_SCALE=0.07 manim -pql physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    Circumscribe,
    FadeOut,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    Transform,
    TransformMatchingShapes,
    TransformMatchingTex,
    Write,
    UP,
)

# V3 remains the single source of truth for the validated geometry, equations,
# road mapping, graphs, constants, and classroom visual language.
from physics9_city_cars_position_velocity_v3 import *  # noqa: F401,F403


# -----------------------------------------------------------------------------
# V4 classroom pacing controls
# -----------------------------------------------------------------------------
# V3 already has good content. V4 intentionally slows the *delivery* rather than
# rewriting the physics or redesigning the validated figures.
MOTION_FACTOR = 1.24
WAIT_FACTOR = 1.80
HEADER_HOLD = 1.10
PRE_CLEAR_HOLD = 1.35
POST_CLEAR_HOLD = 0.45
SEMANTIC_HOLD = 0.42


class Physics9CityCarsV4(Physics9CityCarsV3):
    """V4: V3 visuals + slower, more fluid, teacher-friendly pacing.

    `construct()` remains an orchestration method. Every conceptual block stays in
    its own V3 section method, matching the project's modular classroom code style.
    """

    def validate_data(self):
        """Keep every numerical claim tied to the validated V3 model."""
        super().validate_data()
        assert VA > 0
        assert VB < 0
        assert abs((B0 - A0) - 240.0) < 1e-12
        assert abs((VA - VB) - 120.0) < 1e-12
        assert abs(T_MEET - 2.0) < 1e-12
        assert abs(X_MEET - 160.0) < 1e-12

    def construct(self):
        """Full lesson sequence; content order is intentionally unchanged from V3."""
        self.validate_data()
        self.opening()
        self.problem_model()
        self.sign_convention()
        self.position_equations()
        self.solve_meeting()
        self.live_meeting()
        self.position_graph()
        self.velocity_graph()
        self.cross_checks()
        self.method_summary()
        self.closing()

    # ------------------------------------------------------------------
    # Timing layer
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        """Lengthen visible motion while respecting explicit V3 rate functions.

        We do *not* replace `rate_func`: the live-motion section can still use
        linear motion where constant velocity must remain physically meaningful.
        """
        base = kwargs.get("run_time")
        if base is None:
            base = max(
                [getattr(animation, "run_time", 1.0) for animation in animations]
                or [1.0]
            )
        kwargs["run_time"] = max(0.08, float(base) * MOTION_FACTOR)

        result = super().play(*animations, **kwargs)

        # Tiny pedagogical breath only after semantically dense reveals.
        # It is short enough to preserve flow but long enough for students to read.
        semantic_types = (
            TransformMatchingTex,
            TransformMatchingShapes,
            ReplacementTransform,
            Transform,
            Indicate,
            Circumscribe,
        )
        if any(isinstance(animation, semantic_types) for animation in animations):
            super().wait(SEMANTIC_HOLD)
        return result

    def wait(self, duration=1.0, *args, **kwargs):
        """Convert V3 pauses into deliberate classroom reading/thinking pauses."""
        return super().wait(max(0.12, float(duration) * WAIT_FACTOR), *args, **kwargs)

    # ------------------------------------------------------------------
    # Professional section rhythm
    # ------------------------------------------------------------------
    def header(self, n, title, subtitle=None):
        """Keep the section title on screen long enough to orient the class."""
        group = super().header(n, title, subtitle)
        super().wait(HEADER_HOLD)
        return group

    def clear_scene(self, run_time=0.55):
        """Hold the completed idea, then dissolve it in a soft staged transition."""
        if not self.mobjects:
            return

        # First let the finished reasoning breathe.
        super().wait(PRE_CLEAR_HOLD)

        # Fade the visible stage with a slight upward drift and a small stagger.
        # Using a single LaggedStart keeps the transition fluid and avoids the
        # abrupt 'all objects vanish on one frame' feeling of a slide deck.
        visible = list(self.mobjects)
        transition = LaggedStart(
            *[FadeOut(mob, shift=UP * 0.035) for mob in visible],
            lag_ratio=0.018,
        )
        self.play(transition, run_time=max(0.95, run_time * 1.55))
        super().wait(POST_CLEAR_HOLD)


# Local render commands:
#   python -m py_compile physics9_city_cars_position_velocity_v4.py
#   LESSON_TIME_SCALE=0.07 manim -pql physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4 --disable_caching
#   LESSON_TIME_SCALE=1.0  manim -pqh physics9_city_cars_position_velocity_v4.py Physics9CityCarsV4 --disable_caching
