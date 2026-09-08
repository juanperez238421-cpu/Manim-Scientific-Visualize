# QA V7 → V8 · Sistema diédrico / objeto 3D → vistas 2D

**Input audited:** `Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA_FINAL_pqh.mp4`  
**Audit date:** 2026-09-08  
**Target:** ManimCE 0.20.1 · 1920×1080 · 30 fps · literal `-pqh`

## 1. What was audited

The V7 final was decoded completely and inspected as a real video, not only as source code.

- resolution: **1920×1080**
- codec: **H.264 / yuv420p**
- duration: **77.696 s**
- decoded frames: **2331**
- average frame rate: approximately **30 fps**
- automated spatial metrics were calculated for **every decoded frame**
- a 1-frame-per-second visual contact sequence was reviewed across the full timeline
- extra key frames were inspected around the transitions that produced the smallest or most displaced compositions

## 2. Frame-by-frame findings in V7

### 2.1 Geometry still reads too small

The V7 object is improved over V6, but the actual final render still leaves a large white field around the 3D construction. After the title disappears, the geometry frequently occupies only a modest central region instead of becoming the visual subject of the frame.

Automated evidence:

- `bbox_w < 650 px` at **10.17–10.97 s**
- `bbox_w < 650 px` again at **13.93–15.60 s**
- the principal 3D construction from roughly **15–45 s** has a median detected content width near **913 px**, but that bounding box also includes labels/planes; the solid itself is considerably smaller

Director conclusion: increasing object complexity was not enough; the camera needs a stronger zoom and the graphic hierarchy must use the 16:9 canvas more deliberately.

### 2.2 The main PV/PH construction remains surrounded by unused space

From approximately **18–45 s**, PV, PH, PL, the solid and the projected silhouettes remain readable, but the construction occupies a relatively small island in the middle of the frame. Labels also remain visually small compared with the available resolution.

V8 response:

- increase 3D camera zoom from the V7 range around `0.95–1.22` to a working range around **1.17–1.48** depending on the stage;
- use a fixed top stage header rather than a small bottom chip;
- center the camera on the actual geometric volume through the full construction;
- enlarge directional arrows and give each direction its own pause.

### 2.3 V7 changes too many things simultaneously

The three observation arrows arrive together and the projection sequences are comparatively compressed. The viewer understands the idea, but the motion is still presentation-like rather than explanation-like.

V8 response:

- FRONT appears → pause;
- TOP appears → pause;
- RIGHT appears → pause;
- each direction then dissolves into its corresponding receiving plane;
- projector rays are built in two beats: **anchor rays first**, then the remaining rays;
- each completed outline receives a dedicated hold before the next projection begins.

### 2.4 Critical spatial defect around the Monge transition

The largest remaining V7 directing problem occurs around the source removal / fold / camera transition.

Automated evidence:

- `bbox_w < 650 px` continuously from **46.93–50.63 s**
- detected content center moves left (`cx < 850 px`) from **46.93–50.36 s**
- this is the exact section in which the projection construction collapses into a small left-side object while a large area of the right side is empty

Visual review confirms that the camera move toward the flattened system passes through an edge-on configuration. This temporarily makes the planes and projected outlines look thin, displaced and visually weak.

V8 response:

- keep the literal **90° PH abatimiento**;
- slow it to **4.6 s**;
- hold the completed fold for **2.8 s**;
- **remove the edge-on camera transition entirely**;
- cross-dissolve the finished folded construction into a clean screen-space ALZADO/PLANTA pair;
- construct alignment guides in the stable 2D coordinate system.

### 2.5 Transitional near-empty frames

The V7 render contains several brief stages that visually collapse to a heading or a thin strip of content.

Automated evidence:

- `bbox_h < 220 px` at **57.60–58.40 s**
- `bbox_h < 220 px` at **63.43–64.53 s**
- `bbox_h < 220 px` throughout much of **73.03–77.66 s**

These are not rendering errors, but they are weak uses of a 1920×1080 instructional frame.

V8 response:

- preserve visible geometric context during transitions;
- use three large 2D cards instead of a sparse asymmetric sheet;
- expand the five-step method vertically;
- keep the three projected views visible above the final synthesis.

### 2.6 Final drawing sheet balance

V7 places TOP above FRONT and RIGHT at far right with different card sizes. The result is technically understandable but visually unbalanced: the right side and upper/lower negative spaces do not form a stable grid.

V8 response:

- three equal-size cards across the width;
- identical visual hierarchy for FRONT / TOP / RIGHT;
- large view geometry inside every card;
- sequential card emphasis with pauses;
- no tiny 3D thumbnail.

### 2.7 Five-step method is still too fast for classroom use

V7 reveals each method row quickly and waits only about `0.38 s` after the highlight. For a teacher-led explanation, students do not have enough time to read, point, or copy.

V8 response:

- bars enlarged to **13.25 units wide × 0.93 high**;
- larger title/detail typography;
- each row: fade in → circumscribe → **1.45 s reading pause**;
- full five-step method remains visible for another **3.2 s** after completion.

### 2.8 Closing screen is too thin

From roughly **73 s onward**, the final message becomes a thin horizontal band. The automated audit reports very low bounding-box height because the rest of the screen is empty.

V8 response:

- preserve FRONT / TOP / RIGHT mini-views above the synthesis;
- place the 3D → orthographic projection → 2D relationship in the middle;
- add the explanatory sentence below;
- hold the complete final composition for **5.4 s**.

## 3. Source-level V7 findings

The V7 source is structurally sound: one exact dimensional model generates FRONT, TOP and RIGHT, and the literal PH rotation is correct. The problem is now mostly **directing**, not geometry.

Specific source items changed in V8:

1. `zoom=1.06` opening composition is replaced by a larger **1.42** starting zoom.
2. plane-stage zoom around `0.98` is replaced by a larger working framing around **1.22**.
3. simultaneous direction-arrow entrance becomes sequential.
4. `section_chip()` is replaced in the main timeline by a larger fixed stage header.
5. ray creation is split into anchor and completion passes.
6. V7 camera move to the flattened system is removed because it creates the edge-on visual defect.
7. final sheet panels are replaced by equal-width full-height cards.
8. method bars are enlarged and substantially slowed.
9. closing synthesis retains geometric views to avoid a nearly empty last frame.

## 4. V8 acceptance criteria

The final V8 PQH render should be accepted only if all of the following are true:

- 1920×1080, H.264, yuv420p, approximately 30 fps;
- full-frame decode succeeds;
- duration is intentionally longer than V7 (target **>110 s**);
- no near-blank transition caused by edge-on camera motion;
- 3D construction occupies a substantially larger portion of the frame;
- no title, card, view, plane label or method row is clipped;
- no overlap between fixed stage headers and 3D geometry;
- FRONT / TOP / RIGHT are visibly derived from the same solid;
- PH still performs a literal −90° rotation about the line of ground;
- final three-card sheet is balanced across the frame;
- every major conceptual stage contains an intentional pause;
- the final frame contains both the three views and the conceptual synthesis.

## 5. Pedagogical structure preserved

V8 deliberately preserves the same conceptual sequence:

1. recognize the 3D volume;
2. select observation directions;
3. place projection planes;
4. construct FRONT / ALZADO;
5. construct TOP / PLANTA;
6. construct RIGHT / PERFIL;
7. retain the views after removing the object;
8. unfold PH around LT;
9. align corresponding dimensions;
10. present the three clean 2D descriptions;
11. summarize the five-step method;
12. close with `OBJETO 3D → PROYECCIÓN ORTOGONAL → VISTAS 2D`.

The content is therefore not replaced. V8 is a full directing, spacing, pacing and transition pass over V7.
