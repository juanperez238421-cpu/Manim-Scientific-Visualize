# 02 — Element Taxonomy

The taxonomy is derived from `House_Extrusion_3D_STEP_BY_STEP_V3_DECODED.py` rather than the base64/gzip wrapper.

## Scene architecture

- `HouseExtrusion3D(ThreeDScene)`: narrative scene and 3D camera owner.
- `construct()`: ten semantic phases from reference terrain to final model inspection.
- `fixed_hud()` / `set_phase()`: persistent instructional UI and phase state.
- `phase_note()` / `remove_note()`: transient explanation layer.

## Geometry factories

- `box()`: generic neutral 3D solid primitive implemented with a stretched `Cube`.
- `slab_outline()`: closed PLAN_2D slab profile.
- `wall_trace()`: exterior + interior PLAN_2D construction traces.
- `column_specs()`: 3×3 position specification for column profiles.
- `column_profiles()`: PLAN_2D square profiles.
- `wall_specs()`: dimensional specification for wall solids.
- `make_wall_extrusion()`: thin seed geometry → target wall geometry.
- `front_after_door()`: post-cut front wall representation after door removal.
- `front_final()`: post-cut front wall representation after door + window removal.
- `vertical_profile()`: FRONT_FACE_2D negative-extrusion profile.
- `cutter_front()`: transparent red cutting volume used to explain removal depth.

## Croquis elements

| Element | Current representation | Semantic role |
|---|---|---|
| Primary outline | Blue `Line`/`Rectangle` | Closed profile to operate on |
| Interior trace | Blue `Line` | Partition/reference construction |
| Column profile | Blue `Square` | Repeated closed profile |
| Negative profile | Red `Rectangle` | Material-removal boundary |
| Cutter | Red transparent `Cube` | 3D depth of negative extrusion |
| Grid | Light `Line` group | Reference plane, not active geometry |

## Camera elements

- Initial top camera: current implicit PLAN_2D state.
- Oblique model views: depth/extrusion explanation.
- V3 problem: phase 04 draws plan geometry from an oblique camera.
- V4 protocol helpers: `enter_plan_croquis()`, `enter_front_face_croquis()`, `return_model_view()`.

## Animation elements

- `Create`: technical drawing/construction.
- `LaggedStart(Create...)`: ordered multi-element drawing.
- `Transform(seed, target)`: positive extrusion growth.
- `FadeIn/FadeOut`: state replacement, notes, cutter visibility, and boolean-result simulation.
- `.animate.shift(...)`: explicit cutter penetration or profile displacement.
- `move_camera`: mode change; must be semantically isolated from croquis creation.

## Timing elements

Protocol V1 introduces named timing semantics instead of scattered anonymous waits:

- `CAMERA_SETTLE_PAUSE`
- `MICRO_PAUSE`
- `CONSTRUCTION_PAUSE`
- `READING_PAUSE`
- `EXPLANATION_PAUSE`
- `FINAL_OBSERVATION_PAUSE`
