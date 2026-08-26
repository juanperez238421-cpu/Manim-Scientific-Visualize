from __future__ import annotations

import importlib.util
from pathlib import Path
from manim import *

# Load the fully rendered V3 lesson as the audited core.  V4 only overrides the
# visual defects found during manual frame review of the actual V3 PQH video.
BASE_PATH = Path(__file__).with_name("03_mirror_simetria_senior_v3.py")
SPEC = importlib.util.spec_from_file_location("mirror_v3_audited_core", BASE_PATH)
CORE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CORE)

SKETCH = CORE.SKETCH
VALID = CORE.VALID
WARNING = CORE.WARNING
DARK_GRAY = CORE.DARK_GRAY


class InventorMirrorSimetriaSeniorV4Final(CORE.InventorMirrorSimetriaSeniorV3):
    """Final visual-QA correction layer over the rendered V3 core.

    Manual V3 frame review found two remaining presentation defects:
    1) the blue Boss1 selection halo was offset from the actual seed feature;
    2) the parametric edit camera partly hid the seed, weakening the proof that
       both seed and mirrored feature update together.

    V4 fixes those two defects and removes the last mixed-language validation
    phrases while preserving the otherwise approved V3 narrative and layout.
    """

    def choose_feature(self, hud, base, seed):
        self.set_phase(hud, 6, "MIRROR · SELECCIONAR BOSS1", SKETCH)
        self.play(base.animate.shift(LEFT * 0.95), seed.animate.shift(LEFT * 0.95), run_time=0.70)
        card = self.parameter_card()
        self.play(FadeIn(card), run_time=0.60)

        # QA FIX: the selection highlight must occupy exactly Boss1's geometry.
        halo = seed.copy().set_color(SKETCH).set_opacity(0.50)
        self.play(FadeIn(halo), run_time=0.45)
        tag = self.callout("FEATURES = Boss1", [4.95, -2.25, 0], SKETCH, width=4.3)
        self.play(FadeIn(tag), run_time=0.45)
        note = self.bottom_note(
            "Paso 5: 3D Model → Pattern → Mirror. En Features selecciona Boss1.",
            SKETCH,
        )
        self.wait(CORE.READ)
        self.clear_fixed(note)
        self.clear_fixed(tag, 0.25)
        self.play(FadeOut(halo), run_time=0.25)
        return card

    def validate_reference(self, hud):
        self.set_phase(hud, 10, "VALIDAR REFERENCIA", DARK_GRAY)
        robust_h = self.text("ROBUSTA", 28, BOLD, VALID)
        robust_lines = VGroup(
            self.text("Origin YZ Plane", 23, BOLD, DARK_GRAY),
            self.text("referencia estable", 21, NORMAL, DARK_GRAY),
            self.text("recomendada", 21, NORMAL, DARK_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        robust = VGroup(robust_h, robust_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        robust_box = SurroundingRectangle(
            robust, buff=0.28, corner_radius=0.10, color=VALID, stroke_width=1.45
        )
        good = VGroup(robust_box, robust).move_to([-3.35, -0.25, 0])

        fragile_h = self.text("FRÁGIL", 28, BOLD, WARNING)
        fragile_lines = VGroup(
            self.text("cara temporal", 23, BOLD, DARK_GRAY),
            self.text("puede cambiar con ediciones", 21, NORMAL, DARK_GRAY),
            self.text("evitar si no es necesaria", 21, NORMAL, DARK_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        fragile = VGroup(fragile_h, fragile_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fragile_box = SurroundingRectangle(
            fragile, buff=0.28, corner_radius=0.10, color=WARNING, stroke_width=1.45
        )
        bad = VGroup(fragile_box, fragile).move_to([3.35, -0.25, 0])
        cards = VGroup(good, bad)
        self.fixed_safe(cards)
        self.play(FadeIn(robust_box), Write(robust), run_time=0.80)
        self.wait(0.55)
        self.play(FadeIn(fragile_box), Write(fragile), run_time=0.80)
        note = self.bottom_note(
            "Antes de OK: prioriza planos de origen o planos de trabajo estables frente a referencias temporales.",
            DARK_GRAY,
        )
        self.wait(CORE.EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(cards, 0.40)

    def commit_and_edit(self, hud):
        self.set_phase(hud, 11, "OK · MIRROR1", VALID)

        # QA FIX: a more frontal isometric view keeps BOTH bosses visible at once.
        self.move_camera(phi=60 * DEGREES, theta=-90 * DEGREES, zoom=1.00, run_time=0.95)
        model_shift = 1.10
        base = self.base(0.95).shift(RIGHT * model_shift)
        seed = self.boss(-self.OFFSET, opacity=0.97).shift(RIGHT * model_shift)
        mirror = self.boss(self.OFFSET, opacity=0.97).shift(RIGHT * model_shift)
        self.play(FadeIn(base), FadeIn(seed), FadeIn(mirror), run_time=0.85)

        tree = self.feature_tree(False)
        self.play(FadeIn(tree), run_time=0.65)
        note = self.bottom_note(
            "Paso 8: OK crea Mirror1 después de Boss1 en el árbol paramétrico.", VALID
        )
        self.wait(CORE.READ)
        self.clear_fixed(note)

        self.set_phase(hud, 12, "EDITAR BOSS1 · Ø22 mm", SKETCH)
        edit = self.callout("EDIT BOSS1: Ø16 → Ø22", [0.70, -2.48, 0], SKETCH, width=5.0)
        self.play(FadeIn(edit), run_time=0.50)
        seed_big = self.boss(-self.OFFSET, self.BOSS_R_EDIT, 0.97).shift(RIGHT * model_shift)
        mirror_big = self.boss(self.OFFSET, self.BOSS_R_EDIT, 0.97).shift(RIGHT * model_shift)
        self.play(
            Transform(seed, seed_big),
            Transform(mirror, mirror_big),
            run_time=1.80,
            rate_func=smooth,
        )

        tree2 = self.feature_tree(True)
        tree2.set_opacity(0)
        self.play(FadeOut(tree), tree2.animate.set_opacity(1), run_time=0.70)
        self.remove_fixed_in_frame_mobjects(tree)
        self.remove(tree)

        note = self.bottom_note(
            "Prueba paramétrica: Boss1 y su copia crecen simultáneamente de Ø16 mm a Ø22 mm.",
            VALID,
        )
        self.wait(CORE.EXPLAIN)
        self.clear_fixed(note)
        self.clear_fixed(edit, 0.25)
        self.play(
            FadeOut(tree2),
            base.animate.shift(LEFT * model_shift),
            seed.animate.shift(LEFT * model_shift),
            mirror.animate.shift(LEFT * model_shift),
            run_time=0.60,
        )
        self.remove_fixed_in_frame_mobjects(tree2)
        self.remove(tree2)
        return base, seed, mirror
