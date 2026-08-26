from __future__ import annotations

from manim import *
from fillet_redondeo_senior_v5 import (
    InventorFilletRedondeoSeniorV5,
    DARK,
    MID,
    STEEL,
    STEEL_DARK,
    SKETCH,
    VALID,
    REMOVE,
    WHITE,
    BOLD,
    NORMAL,
    READ,
    EXPLAIN,
    MICRO,
    smooth,
)


class InventorFilletRedondeoSeniorV6(InventorFilletRedondeoSeniorV5):
    """Final senior-QA refinement of the Fillet lesson.

    V6 fixes the two remaining V5 composition defects found by frame audit:
    1. validation cards no longer touch/cover the 3D body and every line is fitted;
    2. parametric-edit labels are shown sequentially below a raised model instead
       of being laid over the part.
    All earlier V5 improvements are inherited unchanged.
    """

    def validation_card(self, title, lines, color, center):
        head = self.text(title, 27, BOLD, color)
        body = VGroup()
        for i, line in enumerate(lines):
            t = self.text(line, 21 if i == 0 else 19, BOLD if i == 0 else NORMAL, DARK)
            if t.width > 4.05:
                t.scale_to_fit_width(4.05)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        if content.width > 4.15:
            content.scale_to_fit_width(4.15)
        panel = RoundedRectangle(
            width=4.75,
            height=max(1.62, content.height + 0.48),
            corner_radius=0.10,
            fill_color=WHITE,
            fill_opacity=0.985,
            stroke_color=color,
            stroke_width=1.4,
        )
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.24)
        return VGroup(panel, content).move_to(center)

    def validate(self, hud, final):
        self.set_phase(hud, 10, "VALIDAR ANTES DE OK", DARK)

        # Reserve a clean lower band for the two cards; the part moves upward.
        self.play(final.animate.shift(UP * 0.82), run_time=0.70, rate_func=smooth)

        ok_card = self.validation_card(
            "VÁLIDO",
            ["R = 8 mm", "cabe entre las caras", "sin autointersección"],
            VALID,
            center=[-3.05, -2.75, 0],
        )
        bad_card = self.validation_card(
            "NO VÁLIDO",
            ["R demasiado grande", "colapsa una cara", "o genera intersección"],
            REMOVE,
            center=[3.05, -2.75, 0],
        )
        cards = VGroup(ok_card, bad_card)
        self.fixed(cards)

        self.play(FadeIn(ok_card[0]), Write(ok_card[1]), run_time=0.95)
        self.wait(0.55)
        self.play(FadeIn(bad_card[0]), Write(bad_card[1]), run_time=0.95)
        self.wait(EXPLAIN)
        self.clear_fixed(cards, 0.45)

        self.play(final.animate.shift(DOWN * 0.82), run_time=0.65, rate_func=smooth)
        return final

    def parametric_edit(self, hud, final):
        self.set_phase(hud, 11, "OK · FILLET1", VALID)

        # Split screen: tree on the left; raised model on the right.
        self.play(final.animate.shift(RIGHT * 1.22 + UP * 0.48), run_time=0.75, rate_func=smooth)
        tree = self.feature_tree()
        self.play(FadeIn(tree), run_time=0.65)

        note = self.note(
            "Paso 7: OK crea Fillet1 después de Extrusion1 en el árbol paramétrico.",
            VALID,
        )
        self.wait(READ)
        self.clear_fixed(note)

        edit = self.small_callout(
            "EDIT FILLET1  ·  R: 8 mm  →  12 mm",
            SKETCH,
            point=[0.35, -2.75, 0],
            width=6.25,
        )
        self.play(FadeIn(edit), run_time=0.55)

        bigger = self.extruded_polygon(
            self.one_corner_points(self.R12),
            self.BASE_H,
            STEEL_DARK,
            0.96,
            DARK,
        ).shift(RIGHT * 1.22 + UP * 0.48)
        self.play(Transform(final, bigger), run_time=1.90, rate_func=smooth)
        self.wait(READ)

        # Remove the edit label before showing the explanatory note: no merges.
        self.clear_fixed(edit, 0.30)
        note = self.note(
            "La pieza se actualiza sin redibujar Sketch1: eso es diseño paramétrico.",
            DARK,
        )
        self.wait(EXPLAIN)
        self.clear_fixed(note)

        back = self.extruded_polygon(
            self.one_corner_points(self.R8),
            self.BASE_H,
            STEEL,
            0.96,
            DARK,
        ).shift(RIGHT * 1.22 + UP * 0.48)
        self.play(Transform(final, back), run_time=1.55, rate_func=smooth)
        self.wait(MICRO)

        self.play(
            FadeOut(tree),
            final.animate.shift(LEFT * 1.22 + DOWN * 0.48),
            run_time=0.65,
            rate_func=smooth,
        )
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)
        return final
