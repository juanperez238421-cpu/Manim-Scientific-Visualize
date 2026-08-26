# Chamfer / Chaflán V2 — Second Visual QA

The V2 render materially improved the V1 score, but two residual composition defects remain and prevent final approval.

## V2 score: 8.7 / 10

### Passes
- Larger body and text hierarchy.
- Opening no longer uses a single clipped workflow sentence.
- Dedicated large `DETAIL A · CORNER` makes 6 mm and 45° readable.
- Progressive red material removal and green planar face are visually distinct.
- Validation cards are large and separated from the model.
- Feature tree and parametric edit are substantially more readable.
- Final workflow is split into two rows.

### Residual defects
1. **HUD subtitle vs phase box** — the long subtitle enters the right-side phase box and is visibly clipped/covered in multiple frames.
2. **Command panel vs 3D part** — during `07 · MODIFY · CHAMFER`, the right edge/front of the solid enters the parameter card region.

## V3 corrective actions
- Shorten the HUD subtitle and add an explicit render-time no-overlap assertion against the phase box.
- Add an additional 1.05-unit left clearance movement before the parameter panel appears.
- Recenter the hidden part after the corner-detail stage so the 3D preview remains centered.
- Preserve all V2 improvements unchanged.

Target approval score after final frame audit: >= 9.4 / 10.
