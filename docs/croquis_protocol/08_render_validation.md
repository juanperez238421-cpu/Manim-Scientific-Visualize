# 08 — Render Validation

Croquis protocol QA extends, rather than replaces, the project PQH rendering protocol.

## Minimum pipeline

1. `python -m py_compile` exact source.
2. Literal `manim -pql` preview using the target ManimCE version.
3. Extract semantic QA frames around every camera/croquis transition.
4. Correct layout/camera/timing defects.
5. Literal `manim -pqh` final render.
6. Locate exact final MP4; reject empty/missing output.
7. Verify video stream: H.264, 1920×1080, intended FPS, yuv420p.
8. Full FFmpeg decode to null output.
9. Dense or semantic audit frames from final PQH.
10. SHA-256 source/video traceability.

## Croquis-specific acceptance gates

A final PQH render fails protocol QA if any of the following occurs:

- first croquis line appears while camera is moving;
- plan croquis is visibly oblique;
- face croquis is not approximately normal to its active face;
- important profile is too small or occluded to read;
- profile-to-solid/cut relationship is ambiguous;
- there is no perceptible observation pause before leaving a completed croquis;
- a camera transition creates an accidental jump in scale/framing;
- cutter direction does not match the active face normal.

## Evidence package

For a protocol-grade case study retain:

- exact `.py` source;
- PQL log/output or QA frames;
- PQH MP4;
- technical probe report;
- full-decode log;
- semantic audit frames/contact sheet;
- SHA-256 manifest;
- protocol/case-study notes documenting accepted and rejected observations.
