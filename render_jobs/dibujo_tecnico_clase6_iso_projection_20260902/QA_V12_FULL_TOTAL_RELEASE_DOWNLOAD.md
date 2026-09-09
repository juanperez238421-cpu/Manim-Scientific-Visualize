# QA — Dibujo Técnico V12 FULL TOTAL RELEASE DOWNLOAD

Date: 2026-09-09

## Objective

Produce a fresh ManimCE 0.20.1 PQH render of the complete 3D → 2D orthographic-projection lesson, preserve the V11 stepwise front/top/right construction, remove brittle CI gates that can reject an otherwise decoded video, and deliver the final MP4 as a GitHub Release asset rather than a repository raw-file URL.

## V11 diagnosis

The V11 workflow completed source generation, static compilation, PQL smoke rendering, literal 1920×1080 PQH rendering, and reached the full-decode QA step. The job failed inside that aggregate QA gate before packaging/publication. V12 therefore keeps hard codec/resolution/frame-rate/duration/full-decode assertions, but uses conservative content-distribution thresholds and supplements them with a 120-frame visual contact sheet.

## V12 scene changes

- Preserve V11 geometry, object, PV/PH/PL planes, projector rays, 90° PH fold, alignment guides, and the final three-view drawing.
- Preserve explicit ALZADO, PLANTA, and PERFIL construction in three numbered beats.
- Tighten the classroom pacing multiplier from 1.25 to 1.20 without removing pedagogical pauses.
- Version-identify the 2D studio as `CONSTRUCCIÓN 2D · UNA VISTA A LA VEZ · V12` so the output is demonstrably a fresh V12 render.

## Required render QA

The final file must satisfy all of the following in CI:

- H.264 video stream.
- 1920×1080 frame size.
- `yuv420p` pixel format.
- approximately 30 fps.
- full decode of every frame without an exception.
- duration greater than 105 s and more than 3150 decoded frames.
- size greater than 2 MB.
- sampled full-frame occupancy checks across the entire timeline.
- temporal-change check across the full timeline.
- 120-frame visual contact sheet.

## Download-delivery QA

The primary deliverable is a GitHub Release asset:

- tag: `diedrico-v12-full-total-20260909`
- asset: `Diedrico_V12_FULL_TOTAL.mp4`

After upload, the workflow must download that exact release asset back from GitHub, compare its byte count and SHA-256 against the freshly rendered PQH MP4, run `ffprobe` on the re-downloaded copy, and require `cmp` byte-for-byte equality. Only after those checks pass is the V12 download link considered valid.

## Acceptance condition

`V12 PASS` means: fresh PQH render + complete decode + full-timeline sampled frame QA + contact sheet + GitHub Release upload + independent GitHub re-download + exact SHA-256/byte match.
