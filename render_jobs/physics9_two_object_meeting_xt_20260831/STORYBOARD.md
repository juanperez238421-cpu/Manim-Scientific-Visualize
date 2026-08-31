# Physics 9 — Two Objects Meeting on a Position-Time Graph

## Learning objective
Students construct two position-time graphs on the same coordinate plane, identify the physical meeting as the graph intersection, and verify the same event using `x = x0 + vt`.

## Numerical model
- Positive direction: right.
- Object A: `x0 = 1 m`, `v = +2 m/s`.
- Object B: `x0 = 13 m`, `v = -1 m/s`.
- `x_A = 1 + 2t`.
- `x_B = 13 - t`.
- Meeting: `1 + 2t = 13 - t -> 3t = 12 -> t = 4 s`.
- Position: `x = 9 m`.

Data used for graph construction:

| t (s) | x_A (m) | x_B (m) |
|---:|---:|---:|
| 0 | 1 | 13 |
| 1 | 3 | 12 |
| 2 | 5 | 11 |
| 3 | 7 | 10 |
| 4 | 9 | 9 |
| 5 | 11 | 8 |

## Scene sequence
1. **Opening** — same JP classroom format as Position-Time Graph Construction V3.
2. **Physical situation** — two walkers on a 0–14 m track, opposite velocity arrows, explicit sign convention.
3. **Data recording** — both walkers move with a shared clock while the corresponding table rows are highlighted.
4. **Object A graph** — construct axes and scale exactly as in V3, plot all A points with projection guides, then connect.
5. **Object B graph** — retain the same axes and scale, plot B with projection guides, then connect using a dashed grayscale line.
6. **Graphical meeting** — student pause, then reveal the intersection `(4 s, 9 m)` with projection lines and a controlled zoom.
7. **Synchronized representation** — physical walkers and both graph points advance under one `ValueTracker`; both coincide at `t = 4 s`.
8. **Equation verification** — establish `x = x0 + vt`, write both equations, impose `x_A = x_B`, solve `t`, then substitute to obtain `x`.
9. **Method comparison** — graph and algebra side by side, same final ordered pair.
10. **Notebook method** — six-step reusable procedure and closing statement.

## Visual contract
- ManimCE 0.20.1.
- 1920×1080, 30 fps.
- White background, black/gray hierarchy only.
- Same `JPClassroomScene` and V3 helper lineage.
- Explicit axis numbers; never rely on automatic `NumberLine` labels for critical graph values.
- Object A: solid black line and filled dots.
- Object B: dark-gray dashed line and hollow dots.
- No overlapping callout cards in the active plotting region.
- Row highlights cross-fade; no geometry morph between unrelated rows.
- Meeting point uses both vertical and horizontal projection guides.
- Algebraic answer must match the graph intersection exactly.
