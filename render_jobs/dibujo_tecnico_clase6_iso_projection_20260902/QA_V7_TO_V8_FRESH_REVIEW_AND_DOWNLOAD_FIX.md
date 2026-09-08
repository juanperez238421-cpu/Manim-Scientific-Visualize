# QA V7 → V8 · fresh render review + real MP4 download fix

Date: 2026-09-08
Repository: `juanperez238421-cpu/Manim-Scientific-Visualize`

## 1. Fresh V7 technical review

The previously published V7 final was decoded and re-sampled again before V8 was created.

Validated V7 file:
`Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V7_SENIOR_QA_FINAL_pqh.mp4`

Technical results from the fresh pass:

- Resolution: 1920 × 1080
- Average frame rate: 30.001383 fps
- Decoded frames: 2331
- Duration: 77.696419 s
- File size: 4,025,041 bytes
- SHA-256: `74c31b6256161c2ba8c7b7adcb7a075d187230c00efd3776cc5bdc683d5b5236`

Fresh whole-video occupancy sampling at 5 frames/s:

- audited samples: 388
- median content bounding-box width: 913 px
- 10th percentile bounding-box width: 751 px
- median bounding-box height: 473 px
- median non-white fraction: ~0.0910
- near-blank samples: 4

The V7 geometry therefore remains technically valid and materially better framed than V6.

## 2. Fresh visual review

A new 24-frame contact sheet was inspected across the complete 77.7 s timeline.

### Confirmed strengths

- the stepped 3D model is consistently readable;
- the FRONT / TOP / RIGHT projection sequence is spatially coherent;
- projection planes do not crop the model;
- the literal PH 90° fold remains understandable;
- the final top/front/right arrangement uses most of the available width;
- the five-step method has no recurrence of the V6 dark-card `Indicate` bug;
- no persistent text overlap or geometry clipping was found.

### Remaining presentation-level improvements

The review did identify a few safe polish opportunities that do not justify changing the validated geometry:

1. Plane labels become visually weak when they sit over translucent projection planes.
2. Direction labels can use slightly more contrast during the initial orbit.
3. Final 2D silhouettes can use a slightly heavier stroke for classroom projection.
4. Final panels and method bars can use a slightly stronger outline.
5. The delivery path itself must be hardened because a valid raw URL is not sufficient if the user cannot reliably start/download the real MP4.

## 3. V8 scope

V8 intentionally preserves the complete V7 dimensional model and timeline. It is not a geometry rewrite.

Changes introduced in `Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_FULL_TOTAL_DOWNLOAD_SAFE.py`:

- fixed-orientation labels receive a white semi-opaque backing;
- plane-label font size increases to 26;
- direction-label font size increases to 25;
- final FRONT/RIGHT view strokes increase to 5.1;
- final TOP view strokes increase to 4.8;
- final view panel borders increase to 1.8;
- method-bar borders increase to 1.65;
- V7 geometry and all projection coordinates remain untouched.

## 4. V8 render acceptance gates

The V8 workflow must pass all of the following before publication:

- Python compile of V5, V7 and V8 source;
- literal full-timeline PQL smoke render;
- literal 1920×1080 / 30 fps `-pqh` render;
- complete PyAV decode of the final file;
- H.264 + yuv420p verification;
- duration > 60 s and decoded frames > 1800;
- frame occupancy audit across the full timeline;
- 96-frame contact-sheet generation;
- SHA-256 calculation of the exact validated MP4;
- publication to `published_renders/` under two names:
  - descriptive long filename;
  - short ASCII alias `Diedrico_3D_to_2D_V8.mp4`;
- direct GitHub re-download of both published URLs;
- byte-count and SHA-256 equality between the rendered file and both GitHub re-downloads;
- compact workflow artifact containing the real `.mp4`, source, QA logs and contact sheet.

## 5. Download strategy

To avoid ambiguity between a GitHub page and the actual media bytes, V8 publishes the same validated MP4 twice:

1. `published_renders/Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V8_FULL_TOTAL_DOWNLOAD_SAFE_FINAL_pqh.mp4`
2. `published_renders/Diedrico_3D_to_2D_V8.mp4`

The workflow verifies both files by downloading them back from `raw.githubusercontent.com` at the immutable publication commit and comparing SHA-256 hashes with the locally rendered source file.

A V8 render is accepted only if both re-downloads are byte-identical to the validated render.
