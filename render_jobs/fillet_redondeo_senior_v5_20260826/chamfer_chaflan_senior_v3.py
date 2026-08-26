from __future__ import annotations

from manim import *

from chamfer_chaflan_senior_v2 import (
    InventorChamferChaflanSeniorV2,
    DARK, MID, LIGHT, SKETCH, VALID, WHITE, BOLD, NORMAL, smooth,
)


class InventorChamferChaflanSeniorV3(InventorChamferChaflanSeniorV2):
    """Final composition QA pass for Chamfer / Chaflán.

    V3 addresses the two residual defects found in the rendered V2 frame audit:
    1) the long HUD subtitle entering the phase box;
    2) the 3D part touching/entering the Chamfer parameter panel.

    All V2 readability, corner-detail, larger typography, sequential preview,
    validation and parametric-edit improvements are preserved.
    """

    EXTRA_PANEL_CLEARANCE = 1.05

    def hud(self):
        title = self.text("AUTODESK INVENTOR PROFESSIONAL", 31, BOLD, DARK)
        # Shortened deliberately so the left HUD has a hard visual boundary
        # before the right-side phase box.
        subtitle = self.text("CHAMFER / CHAFLÁN 3D · herramienta paramétrica", 24, NORMAL, MID)
        title.to_corner(UL, buff=0.32)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.045)
        rule = Line(LEFT*7.52, RIGHT*7.52, color=LIGHT, stroke_width=1.5).to_edge(UP, buff=1.13)

        phase_box = RoundedRectangle(
            width=5.85, height=0.68, corner_radius=0.11,
            fill_color=WHITE, fill_opacity=0.995,
            stroke_color=DARK, stroke_width=1.3,
        ).to_corner(UR, buff=0.32)
        phase = self.text("01 · IDEA DEL CHAFLÁN", 23, BOLD, DARK).move_to(phase_box)

        # Render-time composition assertion: subtitle must not touch phase box.
        if subtitle.get_right()[0] > phase_box.get_left()[0] - 0.28:
            max_w = phase_box.get_left()[0] - 0.28 - subtitle.get_left()[0]
            subtitle.scale_to_fit_width(max_w)
        if subtitle.get_right()[0] > phase_box.get_left()[0] - 0.20:
            raise ValueError("HUD subtitle overlaps phase box")

        group = VGroup(title, subtitle, rule, phase_box, phase)
        self.fixed(group)
        self.play(Write(title), Write(subtitle), Create(rule), Write(phase), run_time=1.45)
        self.wait(1.30)
        return {"group": group, "box": phase_box, "phase": phase}

    def select_edge(self, hud, body):
        # Reuse the complete V2 selection explanation, then add one fluid
        # clearance movement so the subsequent parameter panel has its own zone.
        edge, p0, p1 = super().select_edge(hud, body)
        s = self.EXTRA_PANEL_CLEARANCE
        self.play(
            body.animate.shift(LEFT*s),
            edge.animate.shift(LEFT*s),
            p0.animate.shift(LEFT*s),
            p1.animate.shift(LEFT*s),
            run_time=0.58,
            rate_func=smooth,
        )
        return edge, p0, p1

    def distance_on_face(self, hud, body, edge, p0, p1, card):
        # V2 restores 1.15 units before hiding the part. Because V3 gives the
        # command panel extra clearance, recentre the invisible objects after
        # V2's detail-view transition so the following 3D preview is centered.
        marks = super().distance_on_face(hud, body, edge, p0, p1, card)
        s = self.EXTRA_PANEL_CLEARANCE
        body.shift(RIGHT*s)
        edge.shift(RIGHT*s)
        p0.shift(RIGHT*s)
        p1.shift(RIGHT*s)
        return marks
