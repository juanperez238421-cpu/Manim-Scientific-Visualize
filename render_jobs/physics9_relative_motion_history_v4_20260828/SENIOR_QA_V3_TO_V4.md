# Senior QA Review — V3 to V4

## Source reviewed
`Physics9_Metro_Relativity_V3_2D_ENGLISH_QA_FINAL_pqh(1).mp4`

Technical source properties observed locally:
- 1920×1080
- ~30 fps
- 4,130 frames
- duration ~137.66 s

## Review method
- Automated scan across all 4,130 decoded frames for blank/sparse/border-heavy states.
- 48 evenly distributed visual samples across the complete runtime.
- Targeted inspection around scene transitions and high border-density timestamps.

Automated scan findings on V3:
- blank frames: 68
- very sparse frames: 76
- border-heavy frames: 30
- strongest border-density clusters occur around ~10.5–11.0 s and ~19.6–20.0 s.

## Critical visual issues found in V3

### 1. Title clipping / unsafe horizontal placement
Several section headings are visibly cropped at the left edge. Examples in sampled frames include headings rendered as partial strings such as:
- `H THE OBSERVER AND THE POSITION EQUATION`
- `E METRO: THE TRAIN IS YOUR REFERENCE FRAME`
- `KER, TWO CORRECT VELOCITIES`
- `AMP: LIGHT DOES NOT FOLLOW THE CLASSICAL ADDITION RULE`

This is a release-blocking projector-readability defect.

### 2. Too much information at once
Multiple formulas, labels, long subtitles, diagrams and result boxes are often visible simultaneously. The result is technically rich but pedagogically dense. Students have to decide what to read instead of being guided to one dominant idea.

### 3. Text hierarchy is too small at projector distance
Subtitles and explanatory lines are frequently much smaller than the main geometry. They are readable on a monitor but weak in a classroom projection context.

### 4. The light-clock segment is too advanced for the lesson objective
The V3 narrative moves from simple relative velocity to a full light-clock/time-dilation derivation. That is mathematically valid as a later lesson, but it obscures the simpler conceptual target requested here: understand reference frames first, then understand why constant light speed forced a new kinematics.

### 5. Human and train scale varies too much
The walker and train shrink significantly in the station-frame scenes. This makes the relative-motion comparison less immediate than it should be.

### 6. Historical context is missing
V3 introduces light invariance without first explaining the historical tension:
- Galilean/Newtonian kinematics uses ordinary velocity addition and universal time.
- Maxwell's equations predict electromagnetic waves with a fixed vacuum wave speed.
- Maxwell electromagnetism is not Galilean-invariant.
- Einstein's 1905 resolution preserves the relativity principle and invariant light speed by changing the classical concepts of space and time.

## Senior design decision for V4
V4 is not a patch of V3. It is a conceptual simplification.

### V4 pedagogical spine
1. **Inside the train** — seated observer sees walker at 2 m/s.
2. **From a building** — train moves at 20 m/s, walker is therefore measured at 22 m/s.
3. Use the same equation explicitly in both frames:
   `X = X0 + vt`.
4. Use a short 3 s interval:
   - train position = 60 m
   - walker position = 66 m
   - relative separation = 6 m
5. State the classical-relativity conclusion: same walker, two correct measured velocities because the frames differ.
6. Historical bridge: Galileo/Newton → Maxwell → Einstein.
7. End with a simple conceptual contrast:
   - matter: measured speed depends on frame
   - light: every inertial observer measures the same vacuum speed c
   - therefore classical absolute space/time cannot remain unchanged.

## Numerical redesign
Chosen classroom values:
- train: 20 m/s = 72 km/h
- walker relative to train: 2 m/s = 7.2 km/h
- walker relative to building/ground: 22 m/s = 79.2 km/h
- observation time: 3 s

Reasons:
- arithmetic is mental-math friendly;
- `X = X0 + vt` produces exact integer positions;
- the 10% walker/train speed difference is visible in animation;
- the values remain plausible for a metro-style classroom example.

## Historical accuracy requirement
V4 avoids the misleading phrase that Einstein personally "fought Newton and Maxwell." The historically accurate framing is:

> Einstein confronted a tension between classical Galilean/Newtonian kinematics and Maxwell electromagnetism, and in 1905 proposed special relativity as a consistent kinematic framework compatible with the relativity principle and invariant light speed.

## Visual release criteria for V4
- 100% 2D.
- 100% English visible content.
- White background, black/gray linework, one amber accent for light.
- No section title may exceed safe frame width.
- No text or formula box may touch frame edges.
- One dominant result per stage.
- Large people and train proportions maintained across frames.
- Full `-pql` gate before `-pqh`.
- Full H.264/yuv420p technical QA.
- Full FFmpeg decode.
- Automated every-frame border/blank scan.
- Dense distributed visual contact sheet.
- Final reproducible ZIP and SHA-256 manifest.
