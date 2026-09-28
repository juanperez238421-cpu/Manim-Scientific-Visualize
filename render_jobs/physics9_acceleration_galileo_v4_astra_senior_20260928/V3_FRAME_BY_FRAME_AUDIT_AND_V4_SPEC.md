# V3 forensic frame-by-frame audit → V4 ASTRA SENIOR redesign

## Baseline
Reviewed render: `Physics9_AccelerationGraph_Galileo_V3_OPUS_VISUAL_FULL_FINAL_pqh.mp4`

- Resolution: 1920×1080
- FPS: 30
- Duration: 246.691 s
- Frames: 7,402
- Existing outer-border QA: PASS
- Additional full-frame raster scan: all 7,402 frames scanned for border contact, global foreground density, and frame-to-frame change.
- Dense visual review: 4-second sampling over the whole movie plus targeted key-frame inspection around section transitions and maximum-content-density windows.

## Findings

### 1. Text is technically inside the frame but often below classroom legibility
The V3 compact axes use 10–18 px-equivalent Manim font sizes for ticks/labels and 15–18 for several reasoning labels. At 1080p on a projected classroom screen these are too small even though they are not clipped.

ASTRA rule for V4:
- body text: >= 25
- state/value readouts: >= 27
- axis labels: >= 22
- tick labels: >= 18
- principal equations: 40–54
- no automatic fit that can silently reduce a teaching-critical formula below the intended hierarchy

### 2. The interval-build scenes have local overlap/crowding
During sections 03–04, the combination of:
- velocity graph,
- acceleration graph,
- six-step vertical rail,
- current-interval card,
- geometric Δv/Δt marks,
- SI formula,

creates dense frames. The Δt brace/axis region and the current-interval calculation become visually crowded. The formula is also compressed inside a small card.

ASTRA rule for V4:
- only one right-side focus card at a time
- never stack a second formula box under a data box
- no teaching text below the x-axis
- geometric guides stay on the graph; numerical explanation stays in the focus card
- every reasoning phase replaces the previous phase instead of accumulating

### 3. Repetition is correct but too mechanically slow
V3 repeats six almost identical visual beats for 12 intervals with a persistent rail. This gives rigor but weakens attention.

ASTRA rule for V4:
- retain all six logical decisions
- animate each as a single focus-state replacement
- accelerate repeated transitions while preserving longer pauses for calculations and conclusions
- target ~3–3.5 min instead of ~4.1 min

### 4. Headers are too long
Several V3 section titles consume most of the top width, forcing smaller typography.

ASTRA rule for V4:
short scientific headers:
- MOTION ↔ v(t)
- SLOPE ↔ ACCELERATION
- BUILD a(t): 0–60 min
- BUILD a(t): 60–120 min
- READ a(t)
- DERIVE v = v0 + at
- AREA → POSITION
- WHY GALILEO USED A RAMP
- TEST x ∝ t²

### 5. Section 05 has unused space but small explanatory text
The replay of a(t) is visually sparse while the right-side physics card is still small.

ASTRA rule for V4:
use a larger graph, large live HUD values, and a single large state word:
ACCELERATING / CRUISING / BRAKING.

### 6. Galileo section is scientifically sound but visually underpowered
The side-by-side free-fall/ramp comparison compresses both physical scenes and forces small captions.

ASTRA rule for V4:
make the comparison sequential:
1. full-size free fall + short timing window,
2. transform into full-size ramp + longer measurable timing window,
3. explicitly state that exact ramp acceleration depends on the rolling/sliding model while constant-acceleration structure is the experimental target.

### 7. The 1:4:9:16 sequence is too small and labels crowd the ramp
Multiple ramp labels remain simultaneously visible.

ASTRA rule for V4:
- one pulse at a time
- one large table row per measurement
- no persistent text attached to the ramp
- then clear the ramp and promote x-versus-t² to a full-size plot

## V4 acceptance criteria

1. No overlap in any static teaching state.
2. No body text below 25 font-size except graph tick labels.
3. No numerical teaching text below an x-axis.
4. One focus panel maximum per graph scene.
5. All 12 acceleration intervals remain mathematically derived from the exact V3/V2 velocity profile.
6. Negative acceleration is never described as backward motion.
7. Vehicle displacement remains the exact integral of the piecewise-linear v(t) profile.
8. Galileo section distinguishes free fall (a=g) from ramp motion whose exact a depends on the mechanical model.
9. Final experimental conclusion: x-x0 ∝ t² for constant acceleration from rest; therefore x versus t² is linear with slope a/2.
10. Literal ManimCE -pqh final render, 1920×1080, 30 fps, H.264/yuv420p, full decode, every-frame border scan, dense contact-sheet QA, and SHA-256.
