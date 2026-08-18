# Case Study 001 — House Step-by-Step V3

## A. Current-state diagnosis

Reference video: House Step-by-Step V3, approximately 78.46 s, 1920×1080, 30 fps nominal, 2354 decoded frames.

Reference executable source: `render_jobs/house_step_v3/House_Extrusion_3D_STEP_BY_STEP_V3_DECODED.py` (418 lines). The delivered runtime file was a base64+gzip wrapper; the executable source was decoded before line-level analysis.

The scene is structurally strong: terrain → slab croquis → positive extrusion → wall/column croquis → positive extrusion → negative door/window extrusion → roof → orbit. Its main protocol weakness is that several 2D profiles are drawn while the camera remains oblique 3D.

## B. Frame / timeline map

Approximate semantic timeline from source timing and rendered-frame inspection:

| Time | Phase | Camera / visual state | Viewer task | V3 finding |
|---:|---|---|---|---|
| 0–4 s | 01 Terrain | top/plan | establish reference plane | good |
| 4–8.6 s | 02 Slab croquis | top/plan 2D | read closed footprint | good baseline, add formal mode entry |
| 8.6–15.5 s | 03 Slab extrusion | oblique 3D | connect profile to thickness | good |
| 15.5–25.2 s | 04 Walls + columns croquis | **oblique 3D** | read perimeter, partitions, columns | primary defect |
| 25.2–31.4 s | 05 Columns | oblique 3D | see repeated positive extrusion | good, needs more result pause |
| 31.4–42.2 s | 06 Walls | oblique 3D | perimeter then interior walls | good order; exterior result too quickly dismissed |
| 42.2–50.9 s | 07 Door cut | oblique 3D | understand red profile and cutter depth | profile deserves face-normal 2D first |
| 50.9–58.2 s | 08 Window cut | oblique 3D | repeat negative extrusion grammar | same issue as door |
| 58.2–64.6 s | 09 Roof | oblique 3D | read roof outline then thickness | outline is a croquis but camera never returns to plan 2D |
| 64.6–78.5 s | 10 Model complete | oblique orbit | inspect completed model and summary | good |

A mechanical continuity pass was performed across all 2354 decoded frames. Semantic frames and a 4-second contact sheet were inspected visually. These are different QA operations and should not be conflated.

## C. Code classification

Key V3 responsibilities:

| Lines | Code element | Classification | Responsibility |
|---:|---|---|---|
| 42–49 | scene constants | architecture/geometry | dimensional model |
| 51–62 | `box()` | geometry | generic stretched-Cube solid |
| 70–95 | `fixed_hud()` | UI | persistent title/phase/legend |
| 97–104 | `set_phase()` | UI/animation | phase-state transition |
| 109–118 | `slab_outline()` | croquis | slab closed outline |
| 120–140 | `wall_trace()` | croquis | perimeter + interior traces |
| 142–156 | column specs/profiles | croquis/geometry | repeated column positions/profiles |
| 161–185 | wall specs/extrusion | geometry/animation | wall solid construction |
| 187–210 | post-cut wall states | geometry | simulated boolean results |
| 212–220 | `vertical_profile()` | croquis | facade cut profile |
| 222–229 | `cutter_front()` | geometry | 3D removal volume |
| 231–246 | note helpers | UI/timing | transient explanation layer |
| 251–418 | `construct()` | scene architecture | semantic narrative |

### Code-to-frame root cause: phase 04

V3 phase 04 performs:

```python
self.move_camera(phi=36*DEGREES, theta=-58*DEGREES, zoom=0.75, run_time=1.6)
...
self.play(Create(...wall traces...))
```

The geometry is correct, but `phi=36°` is still a 3D oblique state. The visual result around ~16–24 s therefore reads as sketching in perspective rather than entering a technical drawing mode.

### Code-to-frame root cause: phases 07/08

`vertical_profile()` creates a valid red XZ-plane profile, but phase 07 first moves to `phi=66°`, `theta=-55°`, and phase 08 inherits that oblique state. The viewer never gets a dedicated face-normal reading of the cut profile before cutter depth is introduced.

### Code-to-frame root cause: phase 09

The roof outline uses blue sketch lines, therefore it is semantically a croquis even though the phase label is `EXTRUSIÓN + · CUBIERTA`. It is created directly in the oblique model state.

## D. Camera-state analysis

### Valid baseline
- Phase 02: initial `phi=0°`, `theta=-90°` behaves as the project PLAN_2D baseline.

### Invalid/weak croquis entries in V3
- Phase 04: oblique camera used for top-face sketch.
- Phase 07: oblique camera used for door profile.
- Phase 08: no fresh camera state; inherits door's oblique view.
- Phase 09: roof profile drawn from current oblique model view.

## E. Pacing analysis

- Phase 04 reveals perimeter, partitions, and nine column profiles with no semantic pause between layers.
- Phase 06 exterior walls complete and the note is removed immediately; insufficient observation beat.
- Phase 07/08 profile creation flows directly into cutter setup; profile topology does not get dedicated reading time.
- Phase 09 roof outline gets no separate reading beat before thickness.

## F. Protocol findings

1. Croquis validity depends on camera state, not object type alone.
2. A blue sketch line can be a croquis even in a phase named “extrusion”.
3. Top-plane and face-plane croquis need distinct deterministic camera states.
4. The profile should remain visually causal when transitioning back to 3D depth.
5. Pauses should be named by viewer task, not scattered as arbitrary seconds.
6. Mechanical all-frame QA and semantic visual QA are complementary, not interchangeable.

## G. Proposed changes

### KEEP
- white JP-style presentation;
- fixed HUD and semantic color grammar;
- current house dimensions/layout;
- staged slab/columns/walls/cuts/roof narrative;
- red transparent cutter metaphor;
- final orbit and summary.

### REFINE
- all croquis camera entries;
- semantic pauses;
- phase 06 observation time;
- door/window profile reading;
- roof outline reading.

### REFACTOR
- repeated camera angles into PLAN_2D / FRONT_FACE_2D helpers;
- repeated wait values into semantic timing constants.

### REPLACE
- phase 04 oblique croquis camera call;
- direct oblique door/window profile construction;
- oblique roof-profile construction.

## H. V4 implementation

Target source: `House_Extrusion_3D_STEP_BY_STEP_V4_CROQUIS_PROTOCOL.py`.

V4 adds:
- deterministic PLAN_2D and FRONT_FACE_2D states;
- `enter_plan_croquis()`;
- `enter_front_face_croquis()`;
- `return_model_view()`;
- named semantic pause constants;
- PLAN_2D entry for phases 02, 04, 09;
- FRONT_FACE_2D entry for phases 07, 08;
- deliberate return to 3D before depth/cutter motion;
- additional construction/reading/final-observation pauses.

## I. Render QA acceptance targets

V4 is accepted only if rendered frames prove:
- wall/column traces are truly top/plan in phase 04;
- front-face door/window profiles are not oblique;
- camera is stationary before the first profile line appears;
- return to 3D preserves profile-to-depth causality;
- roof outline receives a top/plan reading beat;
- no new crop, overlap, scale, or HUD conflict appears.

## J. Protocol update

This case establishes Protocol V1. New helpers/rules should be promoted only after at least one additional croquis-heavy scene confirms their reuse without special-case distortion.
