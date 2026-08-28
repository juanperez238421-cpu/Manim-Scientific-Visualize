# Physics 9 Position-Time Graph Construction V2 — Storyboard

## Pedagogical objective
Students should be able to construct a position-vs-time graph from a short motion description or table and interpret each straight segment physically.

## Core example
One object follows four events:

- `(0 s, 2 m)` start;
- `(3 s, 8 m)` moves right;
- `(5 s, 8 m)` waits;
- `(7 s, 4 m)` returns left.

The segment velocities are `+2 m/s`, `0 m/s`, and `-2 m/s`.

## Visual continuity
The same four events persist throughout the lesson. The animation first shows physical motion on a one-dimensional track, then converts those events to a table, then to ordered pairs, then to the final graph. A synchronized scene explicitly links the moving object and the moving point on the graph.

## Scene order
1. **Opening** — title, objective, and graph-reading promise.
2. **Motion -> data** — physical track, four event cards, ordered-pair sequence.
3. **Axes + points** — table, horizontal time axis, vertical position axis, units, scale, point-by-point plotting, chronological connection.
4. **Synchronized motion** — object on track and graph point move together through the three intervals.
5. **Slope -> velocity** — calculate `Delta x / Delta t` for positive, zero, and negative segments.
6. **Meaning / misconceptions** — height is position, slope is velocity, graph is not the physical path, positive position can coexist with negative velocity.
7. **Six-step method + exit question** — reproducible notebook recipe.

## Style / format
- ManimCE 0.20.1.
- 1920x1080, 30 fps.
- White background.
- Black text and linework with neutral gray hierarchy.
- Large projector-safe typography.
- Persistent numbered section header.
- No external assets.
- No decorative color coding required; meaning is carried by geometry, weight, labels, and animation.

## Animation rules
- Build axes before points.
- Plot one data row at a time using dashed projection guides.
- Connect points only after all coordinates are visible.
- During synchronized motion, keep the physical track above and the graph below.
- Use linear time interpolation during the synchronized motion so the graph point has the correct physical timing.
- Replace one slope calculation with the next rather than stacking all equations simultaneously.

## QA risks and controls
- **Header clipping:** use the established JP classroom header system.
- **Graph label clipping:** keep labels inside the safe content zone and away from the right frame edge.
- **Table/graph overlap:** maintain a true left-table/right-graph split during construction.
- **Dense equation stacks:** only one segment calculation is emphasized at a time.
- **Updater residue:** all synchronized-motion objects are removed by `clear_stage()` before the next section.
- **Misconception risk:** explicitly state that the line shape is not the physical path.

## Final conceptual takeaway
`position = graph height` and `velocity = graph slope`.
