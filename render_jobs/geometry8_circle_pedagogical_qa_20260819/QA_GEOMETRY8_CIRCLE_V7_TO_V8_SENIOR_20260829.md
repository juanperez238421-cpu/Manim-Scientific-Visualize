# Geometry 8 Circle V7 → V8 Senior QA Audit

Source reviewed: `Geometry8_Circle_Foundations_HALVES_TWO_ROWS_V7_FINAL_QA_20260829_FINAL_pqh.mp4` (1920×1080, ~155.16 s, ~4655 frames at 30 fps).

## Frame-by-frame visual findings

The audit sampled the entire timeline densely and inspected the critical transition ranges at higher attention. The following defects are visible in the V7 render even though the original runtime bounding-box gate passed.

| Approx. time | V7 finding | Severity | V8 correction |
|---|---|---:|---|
| 8.9–26.6 s | Long Step 01 header is cropped on the left (`...RTS: PERIMETER...`). | Critical | Replaced inherited `move_to(...).align_to(point, LEFT)` header placement with a true `to_edge(LEFT, buff=0.48)` anchor and stricter projector margin. |
| 13–27 s | `CENTER` and `d` visually merge around the circle center; labels are too close to the diameter. | High | Separate coordinates for `CENTER`, `d`, and `r`; larger circle and 50 pt MathTex labels. |
| 31–44 s | Step 02 is readable, but diameter annotation sits inside the figure and competes with the half-arc labels. | Medium | Global larger/slower pacing retained for inherited Step 02; safe header eliminates title clipping. |
| 48.7–53.1 s | Step 03 long header is cropped on the left. | Critical | Global safe header fixes all inherited long-title scenes. |
| 62–75 s | Row labels approach the sector geometry; bottom `P/2 = πr` measurement and checkpoint occupy the same visual region. | High | Rebuilt Step 04. Measurements are shown, held, then removed before the checkpoint appears. Row labels are shortened and moved farther left. |
| 79.7–93 s | Step 05 header is cropped. Motion is correct but slightly fast for classroom copying. | High | Header fixed globally; all animation durations ×1.12 and waits ×1.28 while retaining smooth near-vertical interlock motion. |
| 97–102 s | Step 06 header is cropped. Six ownership arrows cross inside the strip and create unnecessary visual density. | High | Rebuilt Step 06 using only one representative arrow per ownership group, followed by a large height arrow and a larger `height = r, NOT 2r` checkpoint. |
| 106–115 s | Step 07 header is cropped; final base logic is correct but visually small relative to empty space. | High | Rebuilt Step 07 with 36 sectors, larger strip, larger base label, larger one-base formula and longer pauses. |
| 119–133 s | Step 08 header is cropped. 12/24/64-sector strip is small compared with the available frame. | High | Rebuilt Step 08 at radius 2.40 using 8 → 24 → 64 sectors, larger geometry, larger πr/r measurements and 62 pt final equation. |
| 146–155 s | Summary is mathematically correct but can be larger and held longer. | Medium | New 46 pt title, 34 pt summary lines, 62 pt final formula and longer final notebook pause. |

## Code-level root causes and corrections

### Header function
V7 inherits a header implementation that uses:

```python
row.move_to([-0.15, 4.05, 0]).align_to([-7.45, 4.05, 0], LEFT)
```

This is the principal root cause of the rendered left crop. The V8 override instead builds the complete badge/title row, fits only the title when necessary, and then anchors the whole row with:

```python
row.to_edge(UP, buff=0.15).to_edge(LEFT, buff=0.48)
```

The new `projector_safe()` gate uses ±7.70 horizontally and ±4.26 vertically, creating a real visible border rather than merely staying inside the mathematical 16×9 frame.

### Timing
V8 adds two global multipliers on top of the existing `LESSON_TIME_SCALE` protocol:

- `MOTION_SCALE = 1.12`
- `PAUSE_SCALE = 1.28`

This slows the complete inherited and overridden timeline consistently instead of manually lengthening only isolated scenes.

### Step 01
The former stacked formula column is replaced by a progressive large equation panel (`π=P/d → P=πd`) plus separate `d=2r` and `P=π(2r)=2πr` checkpoints. Circumference receives a passing trace before the diameter/radius explanation.

### Step 04
The two-row geometry remains ownership-preserving. The main change is temporal separation: build Row 1, pause; build Row 2, pause; measure Row 1, pause; measure Row 2, pause; remove measurement arrows; only then display the checkpoint. This removes the visible lower-page merge.

### Step 06
The previous six crossing ownership arrows are reduced to two representative arrows. The visual hierarchy becomes: strip → shared band → ownership examples → height arrow → `shared height = r, NOT 2r`.

### Step 07
The strip grows from 32 to 36 sectors and the scene is re-centered. The base equation is 50 pt and the concluding one-base panel is 50 pt.

### Step 08
The limiting argument uses an intentionally coarse 8-sector start so the scalloping is obvious, then morphs to 24 and 64 sectors. The final strip uses radius 2.40, making the limiting rectangle materially larger.

## V8 acceptance gates

The V8 workflow must pass all of the following before delivery:

1. `py_compile` for the complete source stack.
2. Structural checks for V8 class, safe header anchor and timing multipliers.
3. Literal `-pql` full-timeline runtime gate.
4. Literal `-pqh` 1920×1080 / 30 fps render.
5. Full H.264 decode.
6. `yuv420p` assertion.
7. Edge-occupancy check on sampled decoded frames to reject content touching the outer video edge.
8. 60-frame dense contact sheet for final visual review.
9. SHA-256 checksum and artifact upload.
