#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the complete V10 scene from validated V9 with surgical director fixes.

The generated file is a normal, standalone ManimCE Python scene and is published
back to the branch by the render workflow together with the validated MP4.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V9_UPSHIFT_FULL_QA.py"
DST = ROOT / "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V10_UPSHIFT_DIRECTOR_QA.py"

s = SRC.read_text(encoding="utf-8")

s = s.replace("V9 UPSHIFT FULL QA", "V10 UPSHIFT DIRECTOR QA")
s = s.replace("V9 preserves", "V10 preserves")
s = s.replace("V9 upper layout", "V10 upper layout")
s = s.replace("V9 upper-screen composition", "V10 upper-screen composition")
s = s.replace(
    "class Projection3Dto2DV9UpShiftFullQA",
    "class Projection3Dto2DV10UpShiftDirectorQA",
)
s = s.replace(
    "Projection3Dto2DV9UpShiftFullQA --disable_caching",
    "Projection3Dto2DV10UpShiftDirectorQA --disable_caching",
)

s = s.replace(
    "SCREEN_GROUP_UPSHIFT = 0.55\n",
    "SCREEN_GROUP_UPSHIFT = 0.55\nFOLD_EXTRA_UPSHIFT = 1.20\nFINAL_UPSHIFT = 1.20\n",
)

old = '''        self.fixed_fade_in(unfold, run_time=T(0.40))\n        self.play(\n            Rotate(\n'''
new = '''        self.fixed_fade_in(unfold, run_time=T(0.40))\n        # Director correction: the folded PH grows downward in the oblique view.\n        # Reframe upward BEFORE the 90° rotation so the whole transformation stays visible.\n        fold_center = self.lifted_center(0.0, 1.62, 1.00) + np.array([0.0, 0.0, -FOLD_EXTRA_UPSHIFT])\n        self.move_camera(zoom=0.94, frame_center=fold_center, run_time=T(0.95))\n        self.wait(T(0.35))\n        self.play(\n            Rotate(\n'''
assert old in s, "fold block not found"
s = s.replace(old, new)

old = '''        sheet_title = Text("UN OBJETO · TRES DESCRIPCIONES 2D", font_size=35, color=INK, weight=BOLD)\n        sheet_title.to_edge(UP, buff=0.28)\n\n        f_panel = self.view_panel(self.front_view_2d(0.90), "FRONT / ALZADO", FRONT_COLOR, 5.35, 3.05)\n        t_panel = self.view_panel(self.top_view_2d(0.82), "TOP / PLANTA", TOP_COLOR, 5.35, 2.70)\n        r_panel = self.view_panel(self.right_view_2d(0.95), "RIGHT / PERFIL", RIGHT_COLOR, 3.25, 3.05)\n\n        f_panel.move_to(np.array([-1.55, -1.35 + SCREEN_GROUP_UPSHIFT, 0]))\n        t_panel.move_to(np.array([-1.55,  2.00 + SCREEN_GROUP_UPSHIFT, 0]))\n        r_panel.move_to(np.array([ 4.10, -1.35 + SCREEN_GROUP_UPSHIFT, 0]))\n\n        vguide = DashedLine(UP * 0.55, DOWN * 0.55, dash_length=0.08, color=GRID, stroke_width=1.6)\n        vguide.move_to(np.array([-1.55, 0.30 + SCREEN_GROUP_UPSHIFT, 0]))\n        hguide = DashedLine(LEFT * 0.70, RIGHT * 0.70, dash_length=0.08, color=GRID, stroke_width=1.6)\n        hguide.move_to(np.array([1.25, -1.35 + SCREEN_GROUP_UPSHIFT, 0]))\n'''
new = '''        sheet_title = Text("UN OBJETO · TRES DESCRIPCIONES 2D", font_size=33, color=INK, weight=BOLD)\n        # Explicit safe-area placement: V9's blanket UP shift made the TOP card collide\n        # with this heading. V10 keeps the sheet elevated but separates every block.\n        sheet_title.move_to(np.array([0.0, 3.72, 0]))\n\n        f_panel = self.view_panel(self.front_view_2d(0.84), "FRONT / ALZADO", FRONT_COLOR, 4.85, 2.55)\n        t_panel = self.view_panel(self.top_view_2d(0.74), "TOP / PLANTA", TOP_COLOR, 4.85, 2.20)\n        r_panel = self.view_panel(self.right_view_2d(0.88), "RIGHT / PERFIL", RIGHT_COLOR, 3.00, 2.55)\n\n        f_panel.move_to(np.array([-1.65, -1.05, 0]))\n        t_panel.move_to(np.array([-1.65,  1.82, 0]))\n        r_panel.move_to(np.array([ 4.00, -1.05, 0]))\n\n        vguide = DashedLine(UP * 0.42, DOWN * 0.42, dash_length=0.08, color=GRID, stroke_width=1.6)\n        vguide.move_to(np.array([-1.65, 0.38, 0]))\n        hguide = DashedLine(LEFT * 0.62, RIGHT * 0.62, dash_length=0.08, color=GRID, stroke_width=1.6)\n        hguide.move_to(np.array([1.18, -1.05, 0]))\n'''
assert old in s, "2D sheet block not found"
s = s.replace(old, new)

s = s.replace(
    "        final = VGroup(synthesis, note).shift(UP * SCREEN_GROUP_UPSHIFT)\n",
    "        final = VGroup(synthesis, note).shift(UP * FINAL_UPSHIFT)\n",
)

s = s.replace(
    "* the final sheet, five-step method and synthesis are shifted upward modestly;",
    "* the folded-plane transition is reframed upward before rotation so PH stays inside frame;\n"
    "* the final sheet uses explicit non-overlapping safe-area coordinates;\n"
    "* the five-step method and final synthesis use separate upper-layout controls;",
)

# Correct generated-file command comments as well.
s = s.replace(
    "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V9_UPSHIFT_FULL_QA.py Projection3Dto2DV10UpShiftDirectorQA",
    "Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V10_UPSHIFT_DIRECTOR_QA.py Projection3Dto2DV10UpShiftDirectorQA",
)

required = [
    "class Projection3Dto2DV10UpShiftDirectorQA",
    "FOLD_EXTRA_UPSHIFT = 1.20",
    "FINAL_UPSHIFT = 1.20",
    "fold_center = self.lifted_center",
    "sheet_title.move_to(np.array([0.0, 3.72, 0]))",
    "f_panel.move_to(np.array([-1.65, -1.05, 0]))",
    "t_panel.move_to(np.array([-1.65,  1.82, 0]))",
    "final = VGroup(synthesis, note).shift(UP * FINAL_UPSHIFT)",
]
missing = [token for token in required if token not in s]
assert not missing, missing

DST.write_text(s, encoding="utf-8")
print(DST)
print(f"generated_chars={len(s)}")
