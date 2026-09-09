# Sistema Diédrico V12 — Senior QA / delivery correction

## Why V12 exists

V11 completed both its full-timeline PQL render and its literal 1920×1080 / 30 fps PQH render, but the workflow coupled publication to an overly strict frame-distribution heuristic.  That heuristic failed after the valid PQH render, so the artifact, contact sheet, publication and direct-download verification were skipped.

V12 preserves the V11 lesson and fixes the QA architecture.

## Pedagogical content preserved from V11

- post-title composition shifted upward;
- slower classroom cadence and longer holds;
- FRONT / TOP / RIGHT construction split into observation direction, projector rays and contour;
- literal PH 90° fold with safe-area camera reframe;
- clean 2D construction studio;
- ALZADO built segment by segment, then parked at right;
- PLANTA built footprint → middle tier → upper tier, then parked at right;
- PERFIL built segment by segment, then parked at right;
- the same completed cards move from the right-hand archive into the final conventional orthographic layout;
- alignment guides appear only after the views are placed;
- five-step method and closing synthesis retain longer reading pauses.

## V12 QA architecture

1. Generate a standalone V12 source and compile it.
2. Render the complete timeline at PQL as a runtime gate.
3. Render the literal final at PQH, 1920×1080 / 30 fps.
4. Perform a full H.264 decode and hard technical validation.
5. Compute SHA-256 and preserve the exact rendered MP4 in an Actions artifact immediately after hard technical validation.
6. Run whole-timeline spatial diagnostics separately from codec validity; fail only for clear corruption / persistent border clipping rather than normal scene transitions.
7. Generate a 144-frame distributed visual contact sheet.
8. Package source, MP4, render logs, technical report, spatial report, SHA and contact sheet.
9. Publish the exact validated bytes to `published_renders/` under a short filename and a descriptive filename.
10. Download both commit-pinned GitHub files back and require exact byte count + SHA-256 equality.

## Required final files

- `published_renders/Diedrico_3D_to_2D_V12.mp4`
- `published_renders/Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V12_FIXED_FULL_TOTAL_FINAL_pqh.mp4`

A V12 render is not considered delivered until the literal PQH render, full decode, visual audit, artifact preservation, GitHub publication and commit-pinned re-download all pass.
