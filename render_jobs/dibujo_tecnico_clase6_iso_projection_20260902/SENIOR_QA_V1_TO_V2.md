# Senior QA — Dibujo Tecnico Clase 6 ISO Projection Systems V1 -> V2

## Material reviewed
- User-supplied V1 PQH MP4: `Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V1_SENIOR_FINAL_pqh.mp4`
- Full technical decode: 3,863 frames, 1920x1080, ~30 fps, 128.75 s.
- Full-frame automated boundary/content scan over all decoded frames.
- Distributed 36-frame timeline contact sheet plus targeted full-resolution frames in the 3D/projection sections.
- Exact V1 GitHub source from branch `render/dibujo-tecnico-clase6-iso-projection-v1-20260902`.

## Release-blocking findings

### 1. The V1 “3D” solids are not one coherent geometric model
`make_step_solid()` is assembled from independently specified visible polygons. The low top, front, left, right and tower faces are drawn as separate 2D isometric polygons without a single shared model/topology layer. This creates ambiguous occlusion and edge ownership.

**Visible effect:** the step object reads as a stack of overlapping plates rather than a clean CAD solid, especially during the dihedral and projection-system scenes.

**V2 correction:** one coordinate model is used for all isometric faces and all orthographic views. Critical silhouette edges are re-drawn last and hidden edges are optional dashed lines.

### 2. Orthographic views in V1 are hand-authored and do not exactly match the solid
The V1 step solid uses a 3×2 base and a 1.25×1.10 tower footprint, but `view_front_step()` uses a high section that occupies about 57% of the front width instead of 1.25/3 = 41.7%. The 3D model and front view therefore describe different objects.

**Visible effect:** students can compare the 3D object and the FRONT view and see a different step width.

**V2 correction:** FRONT is generated from the exact model proportions: base 3, tower width 1.25, base height 1, total height 2.10. RIGHT uses 2, 1.10, 1, 2.10. TOP uses 3×2 with the exact 1.25×1.10 tower footprint.

### 3. V1 incorrectly duplicates opposite views
In `projection_panel()` V1 creates:
- BOTTOM as a copy of TOP;
- LEFT as a copy of RIGHT;
- REAR as a copy of FRONT.

For this asymmetric stepped solid those are not all the same drawings. In particular BOTTOM should not show the tower footprint as a visible top feature, and LEFT/REAR should be mirrored relative to RIGHT/FRONT when seen from the opposite observation direction.

**V2 correction:** dedicated `view_bottom_step`, `view_left_step`, and `view_rear_step` are implemented.

### 4. The V1 house-like object is geometrically inconsistent
`make_house_solid()` creates a flat roof plateau between x=0.9 and x=2.1. `view_house_front()` instead shows a roof outline with sloped shoulders and a flat top, while `view_house_right()` is a plain rectangle and `view_house_top()` contains no ridge information.

**Visible effect:** the 3D roof and its FRONT/TOP/RIGHT views cannot all be projections of the same physical solid.

**V2 correction:** the object is rebuilt as a true gable-roof prism: wall block 3×2, eave z=1.2, ridge at x=1.5 and z=2.2. FRONT is a pentagonal gable silhouette, TOP contains the ridge line, and RIGHT shows the full height plus the eave line.

### 5. Dihedral-system scene does not actually explain orthographic projection in 3D
V1 draws a small isometric object on the left, then a vertical rectangle/horizontal parallelogram on the right and a single arrow. The object is not spatially related to the planes and the single arrow does not represent parallel orthographic projectors.

**Visible effect:** the scene looks like “object -> unrelated diagram” rather than “project onto perpendicular planes -> unfold.”

**V2 correction:** object enlarged; vertical FRONT and horizontal TOP planes are explicitly labeled; multiple parallel dashed projector rays are animated; the extracted FRONT and TOP views are created before the 90° unfold step.

### 6. Observation directions are screen directions, not object directions
V1 `projection_systems()` and `types_of_views()` use generic UP/DOWN/LEFT/RIGHT screen arrows around an isometric object. FRONT/REAR/LEFT/RIGHT therefore do not align with the axonometric x/y directions of the solid.

**Visible effect:** the six-view logic is spatially ambiguous.

**V2 correction:** observation arrows are aligned to the isometric model axes and opposite directions are taught as FRONT<->REAR, LEFT<->RIGHT, TOP<->BOTTOM pairs.

### 7. 3D figures are too small relative to the available 16:9 classroom canvas
Across approximately 10.8-28 s, 43-56 s, 62-81 s and 89-109 s, the main solids occupy a small fraction of the screen while large empty white regions remain.

**V2 correction:** 3D solids are scaled up about 25-45% depending on the scene; related view cards are larger and staged sequentially.

### 8. V1 uses `TransformFromCopy(solid, 2D_view)` as if the full 3D object directly morphs into a view
The transformation is visually attractive but pedagogically imprecise: the complete axonometric solid morphs into a 2D silhouette without showing which direction is being projected or which edges survive the projection.

**V2 correction:** projection rays + explicit `PROJECT FRONT/TOP/RIGHT` cues precede creation of each orthographic view. The 3D object remains stable, reinforcing that the object does not change.

## Timeline review summary

| V1 time | Section | Senior QA status | Main issue |
|---:|---|---|---|
| 0-10.8 s | Opening / Roadmap | Acceptable | no release-blocking geometry issue |
| 10.8-28 s | Sistema diedrico | FAIL | pseudo-3D planes, weak projector logic, small object |
| 28-43 s | Standards / symbols | Acceptable | mostly typography / symbol content |
| 43-50 s | Sistemas de proyeccion | FAIL | generic 2D arrows around an isometric solid |
| 50-56 s | Tipos de vista | FAIL | observation directions ambiguous |
| 56-62 s | ISO A rules | FAIL | BOTTOM/LEFT/REAR duplicated from opposite views |
| 62-72 s | ISO A example 1 | FAIL | house solid and orthographic views are inconsistent |
| 72-81 s | ISO A example 2 | FAIL | stepped solid/front view dimensional mismatch |
| 81-89 s | ISO E rules | FAIL | same duplicated-view issue |
| 89-100 s | ISO E example 1 | FAIL | stepped model mismatch persists |
| 100-109 s | ISO E example 2 | FAIL | house model mismatch persists |
| 109-129 s | Comparison / refs / closing | Acceptable | no critical 3D issue |

## V2 acceptance targets
1. Literal PQL complete-timeline gate must pass.
2. Literal `-pqh` render at 1920×1080 and 30 fps.
3. H.264 / yuv420p full decode.
4. Every decoded frame scanned for non-white contact with unsafe outer border.
5. Dense distributed contact sheet plus targeted geometry frames.
6. Source-level assertions for distinct six-view helpers and coherent dimensions.
7. SHA-256 and direct GitHub publication of the exact validated MP4.

Workflow trigger: V2 senior render gate enabled after the workflow definition was committed.
