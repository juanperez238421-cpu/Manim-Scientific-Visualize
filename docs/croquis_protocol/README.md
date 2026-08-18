# Croquis Rendering Protocol

A source-backed protocol for technical sketch (`croquis`) animation in ManimCE.

Protocol V1 is derived from reverse-engineering and frame-level QA of the House Step-by-Step V3 reference scene. The goal is to preserve the scene's successful visual identity while turning repeatable behavior into explicit, testable rules.

## Core invariant

**Every important technical croquis must enter a stable 2D camera state before construction geometry begins.**

Normal grammar:

`MODEL_3D → camera transition → CROQUIS_2D → settling pause → construction → reading/observation pause → deliberate return to MODEL_3D → depth/extrusion/cut`

## Proven camera families

- `PLAN_2D`: horizontal XY sketch planes.
- `FRONT_FACE_2D`: front XZ facade profiles.

Additional face states are intentionally deferred until another real case proves the need.

## Protocol documents

1. [`01_visual_grammar.md`](01_visual_grammar.md) — visual causality and hierarchy.
2. [`02_element_taxonomy.md`](02_element_taxonomy.md) — code/Mobject/camera/timing classification.
3. [`03_camera_protocol.md`](03_camera_protocol.md) — deterministic 2D entry/exit rules.
4. [`04_animation_pacing.md`](04_animation_pacing.md) — semantic pause hierarchy.
5. [`05_croquis_scene_states.md`](05_croquis_scene_states.md) — ENTER/BUILD/EXIT state model.
6. [`06_code_patterns.md`](06_code_patterns.md) — minimal reusable helpers.
7. [`07_frame_qa_protocol.md`](07_frame_qa_protocol.md) — code-to-frame visual QA.
8. [`08_render_validation.md`](08_render_validation.md) — PQL/PQH acceptance gates.

## Case studies

- [`case_studies/house_step_v3.md`](case_studies/house_step_v3.md) — foundational V3 diagnosis and V4 protocol extraction.

## Architecture decisions

- [`ADR-001`](decisions/ADR-001-orthographic-entry-before-croquis.md) — enter orthographic 2D before croquis construction.
- [`ADR-002`](decisions/ADR-002-semantic-pause-hierarchy.md) — use semantic pause categories.
- [`ADR-003`](decisions/ADR-003-profile-to-depth-causality.md) — preserve the 2D profile while transitioning to 3D depth when pedagogically useful.

## Reference sources

- Decoded V3 executable source: `render_jobs/house_step_v3/House_Extrusion_3D_STEP_BY_STEP_V3_DECODED.py`
- V4 protocol source: `render_jobs/house_step_v3/House_Extrusion_3D_STEP_BY_STEP_V4_CROQUIS_PROTOCOL.py`
- Reproducible V3→V4 builder: `tools/croquis/build_house_v4.py`

## Review order

For future croquis reviews use:

A. Current-state diagnosis → B. Frame/timeline analysis → C. Code classification → D. Camera-state analysis → E. Pacing analysis → F. Protocol findings → G. Proposed changes → H. Code changes → I. Render QA → J. Protocol update.

The protocol is evidence-driven: a helper becomes stable only after rendered output proves its behavior and another case demonstrates reuse.
