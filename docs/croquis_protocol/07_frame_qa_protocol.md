# 07 — Frame QA Protocol

A successful Manim render is not sufficient evidence of a successful technical animation.

## Required review windows

For every croquis operation inspect frames at:

1. before camera transition;
2. middle of camera transition;
3. first stable 2D frame;
4. end of camera-settling pause;
5. first technical element;
6. each major construction layer;
7. completed croquis;
8. middle of transition back to 3D;
9. first depth/extrusion frame;
10. completed operation.

## Checks

### Composition
- no crop outside safe frame;
- active profile large enough to read;
- HUD and notes do not cover geometry;
- no unintended empty state.

### Camera
- 2D profile is not oblique;
- horizontal/vertical screen relationships match intended sketch plane;
- no residual camera motion during first construction line;
- transition back to 3D is deliberate.

### Geometry
- closed profiles visually close;
- repeated column profiles align with eventual columns;
- wall traces align with wall solids;
- negative profile aligns with resulting opening;
- cutter moves through the correct wall normal.

### Timing
- labels have reading time;
- geometry layers do not compete simultaneously;
- completed croquis remains visible before exit;
- completed operation remains visible before phase change.

## Mechanical full-frame pass

Use every decoded video frame for continuity checks such as sudden-change metrics, black/blank frames, corruption, and unexpected discontinuities. This is complementary to human visual inspection of semantic frames; it must not be described as human inspection of every frame.

## Code-to-frame traceability template

`timestamp/frame → visual observation → source block → root cause → protocol rule → revision`

Example from V3:

`~16–24 s → wall/column croquis remains oblique → phase 04 camera call → target camera is still 3D → croquis must enter PLAN_2D → replace with enter_plan_croquis() + settle pause.`
