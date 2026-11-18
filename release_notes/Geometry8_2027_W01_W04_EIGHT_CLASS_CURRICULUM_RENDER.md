# Geometry 8 · Quarter 1 · 2027 · Week 01–04 eight-class ManimCE delivery

## Primary source, not an inferred syllabus

**Source:** `Geometry_8_2027_P1.docx`, class planner dated 2027, Instituto Jorge Robledo, Grade 8 (four weekly tables). Reopened and checked every class row from the original. Secondary source: 2026 Instituto Jorge Robledo Geometry 8 malla curricular, Period I, first thematic axes. The dated 2027 weekly planner governs the order; the 2026 malla only provides broader curricular context.

| Week | Exact 2027 school-planner window | Class 1 exact instructional focus | Class 2 exact instructional focus |
|---|---|---|---|
| W01 | 19–22 January | Course induction and geometric objects: notebook and drawing conventions; point, line, segment, ray, plane; diagrams and names | Sets and logical diagrams: two-circle classification by dimensions; justify membership and placement |
| W02 | 25–29 January | Line and plane relationships: intersecting, parallel, perpendicular, coincident, diagrams and classroom objects | Reasoning with spatial diagrams: classifying, explaining and finding counterexamples |
| W03 | 1–5 February | Construction instruments and basic operations: ruler versus straightedge, compass, draw and reproduce segments | Perpendicular and parallel constructions: perpendicular bisector, parallel/perpendicular line, check accuracy |
| W04 | 8–12 February | Angle concept, vertex, rays and degree; acute/right/obtuse/straight/reflex classification, direction vs magnitude | Protractor use: measure and construct angles, short checkpoint; **angle addition is only previewed as the next topic** |

**Important calendar constraint:** original class planner specifies two ordered lessons per week, but does not attribute a specific weekday to each class for each class group. No group-specific meeting dates were invented.

## User-validated visual system

All eight videos use the same authentic school PNG, House Extrusion CAD white technical background, school course HUD, numbered sections, green/blue/black semantic drawings, source-grounded examples, large diagrams, smooth transitions and genuine observation pauses.

- W01 Class01 is the already rendered and verified V4 first-period course overview + Week1 instruction: `published_renders/Geometry8_2027_Week01_V4_Class01_PERIOD_I_FULL_CURRICULUM_FINAL_pqh.mp4`.
- W01 Class02 is the already rendered V2 logical sets lesson: `published_renders/Geometry8_2027_Week01_V2_Class02_Sets_MOTION_FINAL_pqh.mp4`.
- W02–W04, six new independent scenes: `lessons/geometry8_2027/week02_04/geometry8_six_classes_cad.py`.
- QA: `lessons/geometry8_2027/week02_04/qa_six_classes.py`; workflow `.github/workflows/geometry8_2027_weeks02_04_six_classes.yml`.

## Mathematical and pedagogy correctness checks

- Infinite Euclidean lines are symbolically represented by arrows; finite classroom objects and segments are explicitly labeled models.
- Perpendicularity is proven only by exactly 90-degree configurations, not arbitrary visual intersections.
- Coincident lines share all points; lines in planes use a finite parallelogram strictly as schematic ideal-plane model.
- W03 equal-radius compass transfer uses the same constructed displacement to reproduce AB=CD.
- Perpendicular bisector: midpoint M of AB with radius **greater than AB/2**, two arc intersections, perpendicular crossing and equal halves.
- Parallel construction uses two perpendicular relationships; construction precision and potential drawing errors are discussed.
- W04 exact angle values come from explicit parameterized ray rotations (35°, 90°, 125°, 180°, 235°), including reflex.
- Angle `ABC` explicitly has **B as vertex**; the protractor zero line is aligned with one ray.
- Degree examples 65°, 120°, 40°, 90° and 140° are generated mathematically from the specified rotation angle.
- The Week04 Class02 final `25°+35°=60°` example is a **preview**, not a claim that addition has been formally taught in Week04.

## Technical verification protocol

The six new videos render independently in parallel using pinned Docker ManimCE 0.20.1, **literal complete `-pql` first and full `-pqh` second**. Six per-scene GitHub Actions artifacts independently retain source, logs and video. Every new MP4 is tested for H.264, **1920×1080, 30fps, yuv420p**, full FFmpeg decode, 16 full HD sample frames, original cover, 4x4 contact sheet and SHA-256. The publication job commits all six MP4s together only after **all** six render and validation matrix jobs succeed. The frame audit is deliberately sampled; full decodability does not guarantee zero transient text collisions.

## Final video manifest

All six new videos will be committed only after verification:

```
Geometry8_2027_Week02_Class01_LinePlane_FINAL_pqh.mp4
Geometry8_2027_Week02_Class02_SpatialReasoning_FINAL_pqh.mp4
Geometry8_2027_Week03_Class01_Instruments_FINAL_pqh.mp4
Geometry8_2027_Week03_Class02_Constructions_FINAL_pqh.mp4
Geometry8_2027_Week04_Class01_Angles_FINAL_pqh.mp4
Geometry8_2027_Week04_Class02_Protractor_FINAL_pqh.mp4
```

The two existing Week 1 validated videos remain intact. The final artifact manifest must be verified against actual GitHub output rather than claimed from filenames alone.
