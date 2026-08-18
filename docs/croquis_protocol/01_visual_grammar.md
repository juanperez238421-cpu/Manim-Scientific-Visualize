# 01 — Visual Grammar

## Core causal grammar

Technical construction should read as a causal sequence, not as simultaneous decoration:

`reference → sketch plane → construction geometry → primary profile → reading pause → 3D depth → solid/cut result → observation pause`

## Two visual modes

### MODEL_3D
Purpose: communicate depth, extrusion direction, material addition/removal, and the relationship between faces.

### CROQUIS_2D
Purpose: communicate exact profile topology and construction order without perspective distortion.

The viewer must be able to identify the mode change immediately.

## Croquis families

### PLAN_2D
Camera normal to a horizontal XY sketch plane. Used for slab footprint, wall/column traces, roof footprint, and other plan-view profiles.

### FRONT_FACE_2D
Camera normal to the front XZ facade plane. Used for door/window profiles before negative extrusion.

Future face families may be added only when a real case requires them.

## Visual hierarchy

1. Reference surfaces/grid: light gray, low contrast.
2. Active croquis geometry: blue (`SKETCH`).
3. Positive material operation: green semantic annotation.
4. Negative/cutting profile and cutter: red semantic annotation.
5. Built solids: neutral architectural grays.
6. Fixed HUD: stable screen-space layer; never competes with geometry.

## Closed-profile invariant

Any croquis that directly produces an additive or subtractive solid must be visibly closed before depth is introduced. A wall sketch is therefore not represented by a centerline: its displayed footprint must encode the same width, center and orientation as the 3D wall that follows. Internal walls are drawn one closed profile at a time so closure can be visually verified before extrusion.

## Transparency invariant for architectural interiors

Once exterior walls have been extruded, their fill should remain translucent whenever opaque facades would hide the internal-wall logic. Interior partitions remain substantially more opaque so room topology stays readable. Transparency is a pedagogical viewing aid, not a change in geometry.

## Typography invariant

Technical labels, phase text, notes and summaries use LaTeX (`Tex`/`MathTex`) and are introduced with `self.play(Write(...))`. Boxes, rules and geometric supports may use their own geometric animations, but visible technical text should not simply appear by `FadeIn`.

## Non-negotiable rule

No important 2D technical geometry begins while the camera is still rotating into its croquis state.
