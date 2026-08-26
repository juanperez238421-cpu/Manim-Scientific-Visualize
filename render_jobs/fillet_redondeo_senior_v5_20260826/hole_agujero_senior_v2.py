from __future__ import annotations

from manim import *

from hole_agujero_senior_v1 import (
    InventorHoleAgujeroSeniorV1,
    BLACK_TEXT, DARK, MID, PAPER, WHITE, BOLD, NORMAL,
)


class InventorHoleAgujeroSeniorV2(InventorHoleAgujeroSeniorV1):
    """Hole / Agujero Senior V2.

    Fixes the V1 PQL safe-area failure. The command panel is shifted left and
    slightly narrowed while preserving 22 pt parameter text and the same five
    explicit Hole parameters.
    """

    def parameter_card(self):
        rows = [
            ("Placement", "From Sketch"),
            ("Center", "Point1"),
            ("Hole Type", "Simple"),
            ("Diameter", "Ø 12 mm"),
            ("Termination", "Through All"),
        ]
        head = self.text("HOLE PARAMETERS", 28, BOLD, DARK)
        entries = VGroup()
        for left, right in rows:
            lab = self.text(left, 22, BOLD, DARK)
            val = self.text(right, 22, NORMAL, BLACK_TEXT)
            field = RoundedRectangle(
                width=2.95, height=0.56, corner_radius=0.05,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=MID, stroke_width=1.05,
            )
            val.move_to(field).align_to(field, LEFT).shift(RIGHT*0.15)
            row = VGroup(lab, VGroup(field, val)).arrange(RIGHT, buff=0.18)
            entries.add(row)
        entries.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(head, entries).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel = RoundedRectangle(
            width=5.45, height=content.height+0.58, corner_radius=0.11,
            fill_color=PAPER, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT*0.27)
        group = VGroup(panel, content).move_to([4.92, -0.20, 0])
        self.fixed(group)
        return group
