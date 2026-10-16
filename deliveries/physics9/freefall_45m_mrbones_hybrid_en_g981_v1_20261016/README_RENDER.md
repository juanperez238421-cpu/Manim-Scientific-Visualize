# Physics 9 — Free fall from 45 m with Mr. Bones · HYBRID V1 · English · g = 9.81 m/s²

This is the English edition of the Spanish hybrid film. It uses the same film, timing and rig.
Only two things change:

- the narration and all on-screen text are in English;
- gravity is **g = 9.81 m/s²** everywhere: the physics, the stroboscope, the equations and the tables.

The Spanish original is on branch `render/physics9-caidalibre-45m-mrbones-hybrid-v1-20261016`.

One video, two engines (protocol HYBRID-SCIANIM-v1).

## Engine B (cartoon)

Mr. Bones, a 171-bone 3D rig in 1930s style.

- **Case 1:** he lets go of his head.
- **Cases 2 and 3:** he pulls off his left arm and uses it as a **sling**.

How the sling works:

- The centre C is fixed and the radius is R = 0.575 m.
- The arm spins up with constant α, then holds a constant ω.
- The skull is released when the radius is horizontal, so it leaves vertically.
- That gives exactly v₀ = ωR = 10 m/s, with ω ≈ 17.4 rad/s.

The screen is split:

- an overview at true scale, with a stroboscope;
- a camera that follows the skull, with live t, y and v readouts.

## Engine A (ManimCE)

1. The question and the sign convention (+y up, a = −g).
2. PAUSE · PREDICT.
3. Numbers first:
   - heights 45, 40.1, 25.4 and 0.9 m;
   - drops in the ratio 1 : 3 : 5;
   - Δv = −9.81 m/s every second.
4. The equation term by term, with a units check.
5. The sling: v = ωR and a_c ≈ 17.7 g.
6. The three cases, with substitution, the quadratic formula and the positive root.
7. The highest point:
   - v = 0 there, but a ≠ 0;
   - apex 50.10 m at t = 1.02 s;
   - symmetry;
   - v² = v₀² + 2gh.
8. Exceptions: rounding g to 10, and estimated quadratic drag (RK4).
9. Summary.

## Data

- h = 45 m
- g = 9.81 m/s²
- v₀ = 0, −10 and +10 m/s
- no air

## Results

| Case | T | \|v\| |
|---|---|---|
| 1 | 3.03 s | 29.7 m/s |
| 2 | 2.18 s | 31.4 m/s |
| 3 | 4.22 s | 31.4 m/s |

## Where the numbers come from

- `verify_caida_libre.py` computes every number, checks it with asserts, and saves it to `shared/derived.json`.
- Both engines read the same constants from `shared/constants.json`.
- The cartoon QA checks that the drawn head matches y(t) on every drawing (error < 1e-9 m). It also checks the results against the Python JSON.

## Format

- 1920×1080, 30 fps, H.264 yuv420p, AAC.
- White cuts between the engines.
- The clip order is in `qa/EDL.json`.
- QA is in `qa/VIDEO_QA.txt`. Every check passes.

## Files

- `*_pqh.mp4`: GitHub copy, CRF 22, under 95 MiB.
- `*_SHARE.mp4`: share copy, two-pass encode, under 30 MB.
