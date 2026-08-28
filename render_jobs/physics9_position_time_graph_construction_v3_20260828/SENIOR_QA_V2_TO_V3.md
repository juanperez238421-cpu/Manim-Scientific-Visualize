# Senior QA — Physics 9 Position-Time Graph Construction V2 -> V3

## Source reviewed

`Physics9_Position_Time_Graph_Construction_V2_FINAL_pqh.mp4`

Technical source facts:

- 1920x1080
- 30 fps
- 124.298698 s
- 3,729 frames
- H.264 / yuv420p

## Review method

The V2 upload was decoded and scanned across all 3,729 frames. The QA pass combined:

1. every-frame technical inspection for blank/sparse frames, edge occupancy and transition density;
2. a distributed 60-frame contact sheet;
3. targeted high-resolution inspection of construction, synchronized-motion, slope and summary sections;
4. dense inspection around state transitions where replacement transforms were visually risky;
5. source-code review against the actual rendered defects.

This is stricter than the original technical workflow because the review treats transient animation frames as part of the final classroom experience, not only the stable end states.

## V2 senior score

| Category | Weight | Score |
|---|---:|---:|
| Physics / mathematical correctness | 20 | 19.5 |
| Pedagogical sequence | 20 | 18.0 |
| Graph construction clarity and scale | 18 | 15.0 |
| Layout / hierarchy / projection readability | 18 | 14.5 |
| Animation continuity and transition quality | 14 | 10.0 |
| Technical reproducibility / PQH QA | 10 | 10.0 |
| **TOTAL** | **100** | **87.0 / 100** |

### Overall judgement

**87/100 — strong classroom lesson, but not yet senior-release quality.**

The concept sequence is excellent and the mathematics is correct. The release blockers are visual rather than conceptual.

## Confirmed defects in V2

### 1. Detached blank rectangles in the slope section — release blocker

The source created a `SurroundingRectangle` around the answer and then inserted that rectangle as an independent child into an `arrange(DOWN)` group. `arrange` subsequently moved the rectangle away from the answer, leaving a visibly empty box below the equations.

Observed in the positive, zero and negative slope cases.

**V3 fix:** equations are positioned first, the answer box is created afterward around the final equation, and the box is never independently arranged.

### 2. Axis-scale values were not reliably visible — pedagogical blocker

The graph construction screen explicitly tells students to choose a readable scale, but numeric tick labels were not consistently visible in the rendered graph. That weakens the most important construction step.

**V3 fix:** explicit x-axis labels `0...7` and y-axis labels `0,2,...,10` are generated as independent MathTex objects. The lesson now visibly states `1 s horizontally` and `2 m vertically`.

### 3. Axis callout cards overlap plotted data

In the completed graph-construction view, the `VERTICAL` callout overlaps the plateau point near `(5,8)` and its label; the horizontal callout also competes with the bottom graph area.

**V3 fix:** axis callouts appear only while the axes are introduced, then fade out before data points are plotted.

### 4. Row-highlight morphs produce distorted intermediate frames

`ReplacementTransform` between different `SurroundingRectangle` instances creates stretched/warped intermediate geometry across table rows.

**V3 fix:** row highlights use clean fade-out / create transitions. No geometry morph is used between rows.

### 5. Interval-state cards produce temporary text collisions

The synchronized-motion scene morphs `INTERVAL 1 -> INTERVAL 2 -> INTERVAL 3` using replacement transforms. During the morph, unrelated glyphs overlap and become temporarily unreadable.

**V3 fix:** state cards use cross-fades instead of glyph morphs. The transition is intentionally non-semantic: the card changes state rather than transforming letter-by-letter.

### 6. Slope formula arrives too late and competes with equations

The general formula `v = slope = Δx/Δt` appears only after all three worked cases. In the negative-slope steady state it can compete vertically with the case equations.

**V3 fix:** the formula is established first and persists at the top of the right column. Each worked case occupies a dedicated region below it.

### 7. Slope is calculated algebraically but not geometrically enough

The equations are correct, but students benefit from seeing the rise/run geometry directly on the selected segment.

**V3 improvement:** each case now draws a visible `Δt` horizontal leg and `Δx` vertical leg (or only the horizontal leg when `Δx=0`). This connects graph geometry to the velocity equation.

## V3 acceptance targets

The V3 render is accepted only if all of the following pass:

- Python compile;
- literal PQL runtime gate;
- literal PQH final render;
- 1920x1080, 30 fps, H.264, yuv420p;
- full FFmpeg decode with empty error log;
- every-frame automated scan;
- 96-frame distributed visual audit/contact sheet;
- no detached blank answer rectangles;
- no axis callout/data overlap in completed plotting states;
- explicit numeric axis scale visible;
- clean interval-card transitions;
- reproducible project ZIP and SHA-256.
