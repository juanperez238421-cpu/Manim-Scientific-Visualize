# Physics 9 Variable Velocity — V3 Frame-by-Frame Forensic QA → V4

## Source reviewed

Uploaded final V3 render:
`Physics9_VariableVelocity_SENIOR_V3_ENGLISH_FULL_FINAL_pqh(1).mp4`

Technical inspection:
- 1920×1080
- 30 fps
- H.264 / yuv420p
- 91.096419 s

The video was reviewed across the complete timeline using one-second visual sampling, transition checks, and source inspection. The final V4 pipeline also performs a full sequential decode and an automated frame-by-frame border scan.

## Defects found in V3

### 1. Moving cars escape their intended road panels — CRITICAL
Observed around the constant-velocity section (~16–18 s) and the realistic route section (~26–33 s).

Cause:
The car target coordinates were computed before the figure panels were moved/scaled. The road was transformed by the layout, but later car animations still used stale pre-layout coordinates.

V4 correction:
Recompute `road_left`, `road_right`, `car_y`, and all car targets only after the final panel/layout transformation.

### 2. Numbered route strip is too small to function pedagogically
Observed throughout ~20–33 s.

Cause:
Five text-heavy cards were compressed into one horizontal row. Their titles and time labels became too small at 1080p classroom viewing distance.

V4 correction:
Replace the miniature text strip with a clean eight-number progress timeline and one large active event card. The active number is filled black; all text remains monochrome.

### 3. Position-time graph lacks readable numeric coordinates
Observed ~35–46 s.

Cause:
Axes contain ticks but no numbers. Students cannot connect slopes to actual times/distances.

V4 correction:
Add explicit axis-number labels and rebuild the position curve after final layout transformation.

### 4. Position curve was generated before its axes were transformed
Source-level issue affecting graph fidelity/alignment.

Cause:
The curve was created from the original axes coordinates and then the axes were moved/scaled inside a panel without the curve.

V4 correction:
Move/scale the graph panel first, then generate the curve from the transformed axes.

### 5. Smoothed x(t) spline can distort physically meaningful flat transitions
Cause:
`set_points_smoothly` can overshoot near piecewise transitions.

V4 correction:
Use a dense `set_points_as_corners` polyline so stopped and transition regions remain physically faithful.

### 6. Velocity-time construction is still too coarse
Observed ~48–60 s.

Cause:
Five pedagogical cards grouped several distinct velocity regimes together. For example, acceleration, cruise, braking, accident passage, traffic slowdown, and recovery were merged into broad events.

V4 correction:
Construct **all 12 exact intervals** from the defined velocity profile:
1. 0–10: 0→70
2. 10–35: 70 constant
3. 35–40: 70→0
4. 40–55: 0 constant
5. 55–60: 0→65
6. 60–75: 65 constant
7. 75–82: 65→25
8. 82–92: 25 constant
9. 92–100: 25→10
10. 100–108: 10 constant
11. 108–115: 10→55
12. 115–120: 55 constant

Each interval gets its own large step card, exact time range, velocity values, graph-shape description, endpoint dot, and guide.

### 7. v(t) axes lack numeric coordinate labels
Observed ~48–60 s.

V4 correction:
Add explicit time and velocity values around the axes.

### 8. Key-message panel overlaps other content
Observed ~61–64 s.

Cause:
The final key message was placed across the lower middle while the graph panel and active event card were still visible.

V4 correction:
Do not stack the summary. Fade the construction card/rules first, then place the final interpretation panel entirely in the right explanation column.

### 9. Several explanatory blocks are too small for projection
Observed in the MRU panel, graph instruction panels, and final synthesis.

V4 correction:
Reduce wording, increase body sizes, use one large active interpretation card instead of several miniature simultaneous cards, and reorganize the final synthesis into a 2×2 process map.

### 10. Acceleration section is descriptive but not sufficiently constructed
Observed ~65–72 s.

V4 correction:
Add a worked interval:
- 0→70 km/h
- 70 km/h = 19.4 m/s
- 10 min = 600 s
- `a_avg ≈ 0.032 m/s²`

Then distinguish positive, negative, and approximately zero acceleration.

## V4 acceptance criteria

The V4 delivery is accepted only if:
- English-only scene contract passes.
- JP Classroom style checker passes.
- PQL runtime render passes.
- Every runtime safe-layout assertion passes.
- Literal PQH render passes.
- 1920×1080, 30 fps, H.264, yuv420p are verified.
- Full video decodes without errors.
- Automated **every-frame** border scan passes.
- Section-focused audit frames and contact sheets show no escaping cars, clipped text, overlapping panels, or graph misalignment.
- Final MP4 and QA package are published to the branch.


## Secondary post-render V4 QA

After the first successful V4 render, the new video was sampled again at one-second intervals across the full timeline.

Two residual presentation defects were found and corrected before final delivery:

1. **Semantic mismatch during route transitions.**
   The previous event card faded out during the same animation in which the speed readout was already changing. This could briefly show, for example, "Lunch stop" while the speed value was increasing. The fix now removes the previous label first, then animates the speed/car change, and only then reveals the next numbered event.

2. **Final synthesis takeaway overlapped the lower process cards.**
   The `realistic motion ⇒ v = v(t)` formula panel occupied the same vertical band as the bottom process row. The final layout now reserves a dedicated middle band for the takeaway and moves the 2×2 process map lower while remaining inside the safe content zone.

The final accepted render therefore requires a second complete PQH cycle after these fixes.
