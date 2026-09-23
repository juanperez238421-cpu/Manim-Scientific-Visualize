# Physics 9 — Acceleration Graph Construction + Galileo Bridge

## Continuity with the latest variable-velocity lesson

This scene uses the exact same 120-minute velocity profile from the previous V5 lesson. The new objective is to transform the already-constructed velocity-time graph into an acceleration-time graph.

## Physics construction

For every interval:

`a = Δv / Δt`

Velocity is converted from km/h to m/s and time from minutes to seconds before reporting acceleration in m/s².

Expected acceleration levels:

| Step | Interval (min) | Velocity change (km/h) | a (m/s²) | Meaning |
|---|---:|---:|---:|---|
| 01 | 0–10 | 0→70 | +0.0324 | speeding up |
| 02 | 10–35 | 70→70 | 0 | constant velocity |
| 03 | 35–40 | 70→0 | -0.0648 | braking |
| 04 | 40–55 | 0→0 | 0 | stopped |
| 05 | 55–60 | 0→65 | +0.0602 | speeding up |
| 06 | 60–75 | 65→65 | 0 | constant velocity |
| 07 | 75–82 | 65→25 | -0.0265 | slowing down |
| 08 | 82–92 | 25→25 | 0 | constant velocity |
| 09 | 92–100 | 25→10 | -0.00868 | slowing down |
| 10 | 100–108 | 10→10 | 0 | constant velocity |
| 11 | 108–115 | 10→55 | +0.0298 | speeding up |
| 12 | 115–120 | 55→55 | 0 | constant velocity |

The acceleration graph is piecewise constant because every v(t) interval is piecewise linear.

## Constant-acceleration equations introduced

1. `a = Δv / Δt`
2. `v = v₀ + at`
3. `x = x₀ + v₀t + 1/2 at²`

The position equation is derived visually from the area under the velocity-time graph:
- rectangle: `v₀t`
- triangle: `1/2 at²`

## Galileo bridge

For a ball released from rest on an inclined plane:

`v₀ = 0`

therefore

`x - x₀ = 1/2 at²`

so the next experimental prediction is:

`x ∝ t²`

The scene ends by preparing students to test the square-time law with an inclined plane.

## QA contract

- English-only on-screen content.
- JP Classroom Standard.
- ManimCE 0.20.1.
- PQL runtime validation before final PQH.
- Literal `-pqh` final render at 1920×1080, 30 fps.
- Full sequential decode.
- Every-frame outer-border scan.
- 20 audit frames + contact sheet.
- SHA-256 and packaged delivery.
