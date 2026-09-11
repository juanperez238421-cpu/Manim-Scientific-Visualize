#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JP Classroom style wrapper with automatic safe-content placement for audited renders."""

from jp_classroom_style_base import *


def _jp_auto_safe(self, mob: Mobject, label: str) -> None:
    """Fit and reposition a stage inside the official content zone before animation."""
    max_height = CONTENT_TOP_Y - CONTENT_BOTTOM_Y - 0.16
    if mob.width > SAFE_WIDTH - 0.20:
        mob.scale_to_fit_width(SAFE_WIDTH - 0.20)
    if mob.height > max_height:
        mob.scale_to_fit_height(max_height)

    top = mob.get_top()[1]
    if top > CONTENT_TOP_Y - 0.04:
        mob.shift(DOWN * (top - (CONTENT_TOP_Y - 0.04)))

    bottom = mob.get_bottom()[1]
    if bottom < CONTENT_BOTTOM_Y + 0.04:
        mob.shift(UP * ((CONTENT_BOTTOM_Y + 0.04) - bottom))

    self.assert_within_frame(mob, label, margin=0.15)


JPClassroomScene.assert_content_safe = _jp_auto_safe
