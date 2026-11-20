# Physics 9 Acceleration + Galileo — V1 Review and V2 Revision Plan

## Reviewed source

Uploaded final V1 render:
`Physics9_AccelerationGraph_Galileo_V1_FULL_FINAL_pqh.mp4`

Technical inspection of the uploaded file:
- 1920×1080
- 30 fps
- H.264 / yuv420p
- duration: 89.890234 s

The actual video was sampled across the complete timeline and compared with the exact V1 source used to render it.

## What works in V1

- The lesson is visually clean and consistent with the JP Classroom Standard.
- The acceleration graph is physically correct for the 12 velocity intervals.
- The sign convention is clear: positive, zero and negative acceleration are distinguished.
- The constant-acceleration equations are introduced correctly.
- The final Galileo section already establishes the important prediction `x ∝ t²`.

## What needs improvement

### 1. Pacing is too compressed for classroom explanation

The full lesson is under 90 seconds despite containing:
- 12 acceleration intervals,
- sign/magnitude interpretation,
- two motion-equation derivations,
- and the Galileo bridge.

Several conceptual operations happen in the same animation beat, so students see the result before they have enough time to process the intermediate reasoning.

### 2. Each acceleration interval reveals too much at once

In V1, an interval card exposes the time interval, Δv, Δt, numerical acceleration and meaning together, while the graph level is drawn shortly afterward.

V2 will separate each interval into six explicit beats:

1. read the time interval,
2. calculate Δv,
3. calculate Δt,
4. convert units and calculate `a = Δv/Δt`,
5. interpret the sign,
6. draw the corresponding horizontal level on `a(t)`.

A visible pause follows every animation beat.

### 3. The algebraic derivation needs more thinking time

The derivation from

`a = Δv/Δt`

to

`v = v₀ + at`

is correct, but V1 transitions through the algebra quickly.

V2 isolates every algebraic transformation and pauses after each one.

### 4. The position equation should be constructed more explicitly from area

V1 already uses rectangle + triangle under `v(t)`, but the triangle formula appears nearly fully formed.

V2 separates:

- rectangle area,
- generic triangle area,
- substitution of base `t` and height `at`,
- combination into `Δx`,
- final equation `x = x₀ + v₀t + 1/2 at²`.

### 5. Galileo's idea is too brief

The final V1 frames show the ramp, the motion equation and the square-time prediction, but the motivation for the inclined plane is compressed.

V2 adds a dedicated comparison:

- free fall: motion happens very quickly,
- inclined plane: accelerated motion unfolds over a longer, easier-to-measure interval,
- the physical idea remains accelerated motion under gravity.

### 6. The Galileo measurement logic needs to become visible

V1 states the ratio `1:4:9:16`, but does not visually construct it from equal-time measurements.

V2 adds:
- four equal time intervals,
- ramp markers at distances proportional to `1,4,9,16`,
- equal-duration ball motions between time marks,
- the direct test `(x-x₀)/t² ≈ constant`.

## V2 pacing contract

Every explicit animation beat in the custom scene is followed by a visible pause through the new `paced_play(...)` helper.

The JP timing constants are also increased for the final PQH render.

## Acceptance criteria

The V2 delivery is accepted only if:

- English-only scene contract passes.
- JP Classroom style checker passes.
- PQL runtime render passes.
- All runtime safe-layout assertions pass.
- Literal PQH render passes.
- Final video is 1920×1080, 30 fps, H.264, yuv420p.
- Full sequential decode succeeds.
- Every-frame raster-edge scan reports zero violations.
- Audit frames/contact sheet show no overlap or clipping.
- Galileo section visibly includes free-fall motivation, ramp comparison, equal-time markers and the `x/t²` test.
