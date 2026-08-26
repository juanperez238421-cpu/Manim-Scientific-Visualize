# Chamfer / Chaflán V1 — Senior Visual QA

Reviewed source: `chamfer_chaflan_senior_v1.py`
Reviewed render: `02_chamfer_chaflan.mp4` (1920×1080, 30 fps, 135.246 s)

## Score: 6.4 / 10 — good technical first pass, not final classroom quality

| Area | Score | Finding |
|---|---:|---|
| Technical render integrity | 10.0 | PQH output is valid H.264/yuv420p, 1920×1080, 30 fps. |
| CAD / chamfer logic | 8.5 | Edge + distance + angle and planar bevel concept are materially correct. |
| Pedagogical sequence | 7.5 | 2D sketch → extrusion → edge → parameters → preview → feature tree is sound. |
| Readability | 4.5 | Too much text is visually small for projected classroom use. |
| Visual hierarchy | 5.0 | Large empty areas coexist with undersized labels/cards/model details. |
| Overlap / safe composition | 4.5 | Several elements crowd each other; the opening route is clipped and corner measurements are cramped. |
| Animation flow | 6.5 | Sequence is understandable but some transitions feel abrupt and information arrives in competing layers. |
| Classroom projection usability | 5.0 | Key parameters, validation text and feature-tree content are too small at normal viewing distance. |

## Frame-audit findings

1. **Opening (~3%)** — the one-line workflow extends beyond the useful visual width and the ending is clipped. Replace with two larger rows/pills.
2. **HUD throughout** — header/subtitle and phase text are smaller than the teaching content requires.
3. **Concept geometry (~13–18%)** — 6 mm / 45° annotations and transition callout are crowded around one corner; main concept occupies too little screen area.
4. **Sketch / constraints (~23–33%)** — rectangle is acceptable, but dimension labels and status information need larger type and stronger spacing.
5. **Selection / parameters (~43–48%)** — parameter panel is too small relative to the available space; values are difficult to read from the back of a classroom.
6. **Cut verification (~58%)** — top-face view leaves most of the frame unused while the actual chamfer geometry is compressed into the upper-right corner. This should become a dedicated enlarged corner-detail view.
7. **Preview (~63–73%)** — model is clearer than previous stages, but explanation text remains too small; material-removal and new-planar-face states should be separated more explicitly.
8. **Validation (~78%)** — cards are readable only at close range and compete with the model. Increase typography and reserve a clean lower band.
9. **Parametric edit (~83–89%)** — feature tree and edit explanation are undersized; split-screen zones should be explicit.
10. **Final summary (~93–97%)** — the workflow line is too long and too small. Use two lines in a dedicated summary panel.

## V2 corrective contract

- Increase primary teaching typography to ~26–31 px equivalents.
- Increase model dimensions and line weights.
- Reserve bottom band for instructional notes; never place notes over the model.
- Split command panel from geometry with dedicated screen zones.
- Replace full-part top view with an enlarged `DETAIL A · CORNER` diagram.
- Separate material removal and planar-face formation into sequential animations.
- Enlarge validation cards and feature tree.
- Split workflow summaries into two rows.
- Keep `fixed()` safe-area assertions active so any layout regression fails at render time.
- Render PQL smoke test, then literal `-pqh`, then full decode + 20 audit frames + contact sheet.
