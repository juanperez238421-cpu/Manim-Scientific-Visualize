#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 two-object x-t meeting — V2 rendered-pixel QA correction.

The V1 PQH render passed mathematical and technical QA, but dense visual review
found one release-blocking transient defect inherited from the shared header
implementation: glyph interpolation between unrelated section titles can
produce a frame of colliding/warped text.

V2 preserves the complete accepted V1 lesson and replaces section-title glyph
morphs with an intentional fade-out/fade-in state change. No mathematical,
layout, data, timing, graph or equation content is changed.
"""
from __future__ import annotations

from pathlib import Path
import sys
from manim import FadeIn, FadeOut

RENDER_ROOT = Path(__file__).resolve().parents[1]
V1_DIR = RENDER_ROOT / "physics9_two_object_meeting_xt_20260831"
STYLE_DIR = RENDER_ROOT / "physics9_position_time_velocity_workshop_20260824"
for p in (V1_DIR, STYLE_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from two_object_meeting_xt import Physics9TwoObjectMeetingXT  # noqa: E402
from jp_classroom_style import RUN_QUICK  # noqa: E402


class Physics9TwoObjectMeetingXTV2(Physics9TwoObjectMeetingXT):
    """V1 lesson with transition-safe section headers."""

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        """Change semantic section states without glyph-to-glyph morphing.

        The geometry and typography are still created by the canonical JP
        `set_header`; only the transition mechanism is changed. This keeps the
        approved visual contract while eliminating distorted intermediate text.
        """
        old_header = self.header_group
        old_subtitle = self.subtitle_group

        if old_header is None and old_subtitle is None:
            super().set_header(number, title, subtitle)
            return

        old = [mob for mob in (old_header, old_subtitle) if mob is not None]
        if old:
            self.play(*[FadeOut(mob) for mob in old], run_time=RUN_QUICK * 0.55)

        # Force the canonical builder down its clean first-header path.
        self.header_group = None
        self.subtitle_group = None
        super().set_header(number, title, subtitle)

        new_header = self.header_group
        new_subtitle = self.subtitle_group
        new = [mob for mob in (new_header, new_subtitle) if mob is not None]

        # The canonical first-header path adds immediately. Remove and fade in
        # so the state change remains visible and controlled.
        if new:
            self.remove(*new)
            self.play(*[FadeIn(mob) for mob in new], run_time=RUN_QUICK * 0.60)
