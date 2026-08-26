# Case Study 001B — House V4 PQL QA Gate

## Render under review

`House_Extrusion_3D_STEP_BY_STEP_V4_CROQUIS_PROTOCOL_pql.mp4`

Observed PQL duration: approximately 107.66 s. This is intentionally longer than V3 because camera-settling, reading, construction, and observation pauses are now explicit.

## Gate results

### Phase 04 — wall + column croquis

**PASS.** Camera completes transition from oblique model view to PLAN_2D before perimeter construction begins. The slab reads as a rectangle in plan; perimeter, partitions, and column profiles are introduced as separate semantic layers with visible pauses. The completed croquis remains readable before the camera leaves 2D.

### Phase 07 — door negative-extrusion profile

**PASS.** Front facade becomes face-normal before the red door profile is constructed. The profile receives a reading pause. It remains visible during the deliberate return to oblique MODEL_3D, then the red cutter introduces removal depth.

### Phase 08 — window negative-extrusion profile

**PASS.** Same FACE_2D → profile → reading pause → MODEL_3D → cutter grammar is reproduced consistently. The existing door opening remains legible and does not interfere with the window profile.

### Phase 09 — roof outline

**PASS.** The roof outline is correctly classified as croquis even though the phase title is an extrusion phase. Camera returns to PLAN_2D before the blue roof boundary is drawn; after a reading pause, the scene returns to an oblique model view for thickness/extrusion.

## Composition checks

- no new clipping observed in the inspected semantic frames;
- fixed HUD remains stable while 3D camera changes;
- bottom explanatory notes remain separated from active model geometry;
- PLAN_2D framing keeps the active footprint within safe margins;
- FRONT_FACE_2D framing gives door/window profiles substantially better readability than V3.

## Decision

**PQL gate approved. Proceed to literal `-pqh` final rendering and strict technical QA.**

No geometry rewrite is required before PQH. The V4 change is accepted as a camera/timing refinement of the V3 baseline.
