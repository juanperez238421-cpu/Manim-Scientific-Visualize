# Physics 9 — Bus Relativity V5 · Consolidated classroom design

Date: 2026-09-07

## Why this version exists

The previous relative-motion sequence had several valid components spread across different versions: reference frames, the 2 m/s walker, the moving vehicle, the road observer, `X = X0 + vt`, Maxwell, Einstein, light invariance and the relativistic velocity-addition formula. V5 consolidates those ideas into one continuous physical situation and removes the separate light-clock / simultaneity detours from this introductory video.

## Pedagogical rule

One bus, two observers, one change of object:

1. Bus speed relative to road: 20 m/s.
2. Walker speed relative to bus: 2 m/s.
3. Road observer measures walker: 22 m/s.
4. After 3 s: bus travels 60 m, walker travels 66 m, relative separation is 6 m.
5. Replace the walker with a light pulse.
6. Passenger measures `c`.
7. Road observer also measures `c`, not `c + 20 m/s`.
8. Introduce the relativistic velocity-addition rule only after the conceptual conflict is visible.
9. Show why low-speed motion still reduces to the ordinary Galilean result.

## Santaolalla-inspired simplification

The narrative borrows the *structure*, not the wording, of Javier Santaolalla's public explanations of relativistic velocity addition: begin from an intuitive everyday addition of speeds, then show that Einstein's rule is the general rule and that ordinary arithmetic is recovered when speeds are tiny relative to `c`.

Public reference used for the redesign:
- Javier Santaolalla / Date un Vlog, **“El movimiento no es lo que parece”** (2023). The video begins with a simple moving-surface velocity-addition question, then progresses through Galileo/Newton, light, Maxwell, Einstein and the relativistic velocity-addition formula.

## Scope intentionally excluded

This introductory video does **not** derive:
- time dilation;
- length contraction;
- relativity of simultaneity;
- Lorentz transformations;
- light-clock geometry.

Those are valid later lessons, but including them here weakens the causal chain from relative motion to invariant light speed.

## Visual rules

- 1920×1080, 30 fps.
- White background.
- Black / gray line work.
- Amber only for light.
- 100% 2D.
- 100% English.
- Large human pictograms.
- One dominant result per screen.
- No external image assets.
- No absolute filesystem paths.

## Numerical claims validated in source

- `20 + 2 = 22 m/s`.
- `(20 m/s)(3 s) = 60 m`.
- `(22 m/s)(3 s) = 66 m`.
- Relative displacement after 3 s: `6 m`.
- `c = 3.00×10^8 m/s`.
- Everyday relativistic correction: `(2×20)/c² ≈ 4.44×10^-16`.
- Relativistic addition with `u' = c` simplifies exactly to `u = c`.

## Render / QA result

GitHub Actions run: `34121000504` — SUCCESS.

- Literal PQL gate: PASS.
- Literal PQH render: PASS.
- 1920×1080, 30 fps.
- H.264 / yuv420p.
- Duration: 92.762109 s.
- Frames: 2,783.
- Full FFmpeg decode: PASS.
- Every-frame scan: 2,783 / 2,783.
- Border-heavy frames: 0.
- 36-frame distributed contact sheet generated.
- SHA-256: `24a20600415d70867e37f7073b3ce120ea1789f5714b7cb1b555ea8372aaf64a`.

Final persistent MP4:
`deliveries/physics9_bus_relativity_v5_20260907/Physics9_Bus_Relativity_V5_SANTAOLALLA_SIMPLE_FINAL_pqh.mp4`
