# House Step V5 — Closed Croquis + LaTeX Typography

## Scope

V5 keeps the approved V4 composition, cameras, color semantics and operation order. It changes only the weak points found in the V4 frame/code review.

## Corrections

1. Internal wall croquis are no longer open centerlines.
2. Every wall profile is a closed rectangle generated from the exact `wall_specs()` dimensions and centers used by the subsequent solid extrusion.
3. Interior wall profiles are written one-by-one in PLAN_2D with a pause after each closure.
4. Technical visible text is generated with `Tex` and introduced through `self.play(Write(...))`.
5. Exterior wall solids use low fill opacity so interior partitions remain readable.
6. Interior partitions remain substantially more opaque than exterior walls.
7. Camera-settle, construction, reading, explanation and observation pauses are increased without changing the overall scene grammar.

## QA gate

Acceptance requires PQL first, dense semantic frame extraction, manual review of the wall-croquis closure sequence and exterior-wall transparency, then literal PQH plus ffprobe/full-decode/SHA-256 validation.

The PQL workflow uses robust final-video discovery because Manim names the preview artifact `HouseExtrusion3D_PQL_PASS.mp4` rather than the scene class name alone.

## PQL result

PASS. The dense 40-frame audit confirms stable PLAN_2D before wall drawing, individually closed internal-wall footprints, readable column profiles, transparent exterior-wall context, opaque-enough internal partitions, and no new HUD clipping. This gate authorizes the V5 literal PQH render.

## Final PQH result

PASS. Literal `-pqh` completed on ManimCE 0.20.1. Final validation passed H.264, 1920×1080, 30 fps, yuv420p, full FFmpeg decode and a 48-frame semantic audit. Duration: 153.292188 s. Video SHA-256: `c6c0843780ef65636dc9ce91ee22dc706d4b976d6bd6878ccb0df0faebe7256f`.
