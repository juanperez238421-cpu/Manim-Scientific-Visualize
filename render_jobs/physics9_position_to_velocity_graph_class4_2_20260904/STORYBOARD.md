# Physics 9 — Class 4-2 · Position graph → Velocity graph

## Numerical contract
Use the **exact same motion** from Class 4-1:

- `(0 s, 2 m)`
- `(3 s, 8 m)`
- `(5 s, 8 m)`
- `(7 s, 4 m)`

Therefore:

1. `0–3 s`: `Δx = +6 m`, `Δt = 3 s`, `v = +2 m/s`.
2. `3–5 s`: `Δx = 0 m`, `Δt = 2 s`, `v = 0 m/s`.
3. `5–7 s`: `Δx = -4 m`, `Δt = 2 s`, `v = -2 m/s`.

Verification from the velocity graph:

`Δx = (+2)(3) + (0)(2) + (-2)(2) = +2 m`, so `x_f = 2 + 2 = 4 m`, matching the final position in the source graph.

## Scene sequence

### 0. Opening
- Physics 9 / Kinematics.
- Goal: construct the matching `v-t` graph from the already-known `x-t` graph.
- Core bridge: **slope on x-t = height on v-t**.

### 1. Rebuild the original position graph
- Same four ordered pairs.
- Same piecewise line.
- Explicitly identify three straight time intervals.

### 2. Calculate the three slopes
- Persistent `v = slope = Δx/Δt` formula.
- Highlight one position segment at a time.
- Draw visible rise/run geometry.
- Show `+2`, `0`, `-2 m/s` separately.

### 3. Student construction pause
- Blank `v-t` axes.
- Vertical guides at `t = 3 s` and `t = 5 s`.
- Cards list the three already-calculated velocity levels.
- Six-second silent construction window before reveal.

### 4. Build the velocity graph
- Plot each constant level only over its own interval.
- Do not connect the levels with vertical motion lines.
- Explain instantaneous idealized velocity changes at `t=3 s` and `t=5 s`.

### 5. Compare x-t and v-t side by side
- Same time boundaries aligned conceptually.
- Rising x-t ↔ positive v.
- Horizontal x-t ↔ zero v.
- Falling x-t ↔ negative v.

### 6. Physics verification
- Direction / rest / return interpretation.
- Signed area under `v-t` recovers net displacement `+2 m`.
- Final position check recovers `4 m`.

### 7. Reproducible notebook method
1. Split into straight intervals.
2. Calculate slope.
3. Keep the sign.
4. Plot velocity height on the same time interval.
5. Verify with displacement.

## Visual contract
- 1920×1080, 30 fps.
- White background.
- Black / neutral gray hierarchy.
- JP classroom headers and safe margins.
- Large projector-readable labels.
- No external assets.
- ManimCE 0.20.1.

## Render contract
- Python compile.
- Literal `-pql` runtime gate.
- Literal `-pqh` final render.
- H.264 / yuv420p.
- Full FFmpeg decode.
- Every-frame boundary/density scan.
- 72-frame visual audit contact sheet.
- SHA-256.
- Publish final MP4 under `deliveries/physics9_position_to_velocity_graph_class4_2_20260904/`.
