# Mirror / Simetría — Total QA Review (V2 → V3)

## Basis reviewed

- Actual delivered V2 PQH video: `Inventor_Mirror_Simetria_Senior_V2_FINAL_PQH.mp4`.
- Actual V2 source: `scenes/03_mirror_simetria_senior.py`.
- Dedicated Inventor senior lesson core already used in the recent Hole/Fillet family: persistent Autodesk-style HUD, explicit phase labels, stronger model contrast, bottom instructional note, browser/tree validation, parametric edit proof.

## V2 QA score

| Area | Score | Finding |
|---|---:|---|
| Technical render | 10/10 | 1920×1080, 30 fps, H.264/yuv420p, full decode PASS. |
| Narrative logic | 8.5/10 | Correct concept → sketch → seed → plane → preview → validation → edit sequence. |
| Classroom legibility | 6.5/10 | Several explanatory cards, section subtitles and browser text are too small relative to a projected 1080p classroom frame. |
| 3D readability | 6.0/10 | Base and seed use low opacity; Boss1 becomes visually weak against the white background. |
| Inventor interface continuity | 6.5/10 | V2 uses large transient section headers instead of the stronger persistent HUD/phase pattern used by the current dedicated core. |
| Step-by-step explicitness | 7.0/10 | The geometry is correct but the operational clicks/selections are not separated enough for a student reproducing the command. |
| Terminology consistency | 7.0/10 | Spanish opening + English instructional body creates unnecessary language switching. |
| Parametric teaching value | 9.0/10 | Editing Boss1 and updating both sides is a strong closing proof. |
| Overall | **7.6/10** | Technically valid render, but not yet at the visual/teaching standard of the strongest recent dedicated Inventor lessons. |

## V3 mandatory corrections

1. Preserve the minimal white Autodesk Inventor aesthetic but use the persistent senior HUD and a top-right numbered phase label.
2. Increase model opacity from the washed-out V2 appearance to a solid steel-gray CAD body.
3. Increase critical label sizes and use a single bottom instructional note rather than multiple small competing cards.
4. Separate the command into explicit reproducible phases: Sketch1 → Extrusion1 → Sketch2 → Boss1 → Mirror/Features → YZ Plane → Preview → verify equal distance → OK/Mirror1 → parametric edit.
5. Keep only limited functional accents: blue for sketch/selection, green for validated result, red only for warnings/reference fragility.
6. Remove the ambiguous `Operation = Join` row from the Mirror parameter card; the lesson mirrors `Boss1` as a feature using the YZ plane.
7. Keep the 28 mm / 28 mm top-view proof and the stable-origin-plane vs fragile-reference comparison.
8. Keep the browser dependency `Mirror1 = Boss1 / YZ Plane` and explicitly show `Boss1 Ø16 → Ø22` propagating to the mirrored copy.
9. Add a final browser/process summary and slow orbit for inspection.
10. Run literal `-pql` smoke, literal `-pqh` final, FFmpeg full decode, 1920×1080/30 fps/H.264/yuv420p assertions, and a denser frame contact sheet before accepting delivery.

## Acceptance gate

V3 is accepted only after the rendered PQH artifact is manually reviewed from its generated contact sheet and representative full-resolution frames. A successful workflow alone is not considered sufficient visual QA.
