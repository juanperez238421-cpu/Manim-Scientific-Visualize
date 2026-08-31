# Statistics 10 · IQR Class 02 — Senior QA V1 → V2

## Baseline reviewed
- Render: `Statistics10_IQR_Class02_Compare_Boxplots_FINAL_pqh.mp4`
- Duration: 210.6 s
- Resolution: 1920×1080, 30 fps, H.264, yuv420p
- Technical QA from V1: full decode PASS; 6,318 frames scanned; 0 border-heavy frames.
- Review basis: exact V1 source, 96-frame contact sheet, representative full-resolution frames, and the final MP4.

## Senior QA score — V1

| Category | Weight | Score | Weighted |
|---|---:|---:|---:|
| Statistical correctness | 25 | 92 | 23.00 |
| Pedagogical sequencing | 20 | 94 | 18.80 |
| Visual hierarchy / projector readability | 15 | 91 | 13.65 |
| Animation / focus guidance | 15 | 84 | 12.60 |
| Pacing / cognitive load | 10 | 88 | 8.80 |
| Classroom usefulness / notebook transfer | 10 | 94 | 9.40 |
| Technical render integrity | 5 | 100 | 5.00 |
| **TOTAL** | **100** |  | **91.25 / 100** |

## Findings

### Critical accuracy issue fixed in V2
The `READ THE GRAPH` scene used data containing the outlier `35`, but the visible NumberLine ended at `30`. Manim can extrapolate `n2p(35)` beyond the stated axis domain, so the point could still appear, but the graph then visually contradicts its own labeled scale. V2 changes that scene to a visible `0–40` scale and adds a validation guard requiring all plotted values to be inside the axis domain.

### High-priority visual/pedagogical improvements
1. The opening had six small route cards. V2 uses four larger cards: **CLASSIFY → DRAW → READ → COMPARE**.
2. The worked outlier arithmetic was correct but visually flat after the equations appeared. V2 explicitly circumscribes the decisive inequality `20 > 13.5` and the rule that the whisker does not end at the fence.
3. The one-boxplot reading scene now shows the upper fence and visually isolates the outlier, linking formula → graph rather than only graph → text cards.
4. The median-comparison scene now places neutral highlight columns on the two medians while the dashed guides are shown, reducing eye-search time.
5. Whisker labels are enlarged for projector readability.
6. The student challenge prompt is enlarged while preserving the deliberate working pause.

### What was intentionally preserved
- White background / black-first JP classroom visual system.
- Persistent numbered section header.
- Same Class 1 quartile convention.
- Correct modified-boxplot rule: fences classify; whiskers end at real non-outlier observations.
- Same-scale comparison of Groups A and B.
- Deliberate classroom pauses for copying and discussion.
- Final bridge to deciles and percentiles.

## V2 acceptance target
- Overall manual QA target: **≥ 96 / 100**.
- Literal `-pql` complete-timeline validation.
- Literal `-pqh` final render using ManimCE 0.20.1.
- H.264, 1920×1080, 30 fps, yuv420p.
- Full FFmpeg decode with zero decode errors.
- Every-frame blank/sparse/border scan.
- 120 distributed audit frames + contact sheet.
- Verified PDF and representative PNG.
- SHA-256 manifests and reproducible package.
