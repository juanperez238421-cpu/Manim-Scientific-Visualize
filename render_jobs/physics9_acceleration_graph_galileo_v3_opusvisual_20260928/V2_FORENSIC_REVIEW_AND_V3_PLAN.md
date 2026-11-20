# Physics 9 — V2 forensic visual review and V3 OPUS-visual plan

## Baseline reviewed

Actual rendered baseline:
`Physics9_AccelerationGraph_Galileo_V2_STEP_BY_STEP_FULL_FINAL_pqh.mp4`

Baseline PR: #162.

The review used the real V2 rendered QA contact sheet and the real source/workflow from PR #162, not a reconstructed preview.

## What V2 already does correctly

- Keeps the exact 120-minute velocity profile and computes all 12 acceleration intervals in SI units.
- Uses a consistent six-beat reasoning method per interval.
- Preserves the JP Classroom safe-layout system, 1920x1080/30 fps output, white background, monochrome hierarchy, PQL→PQH render flow, full decode, border scan, audit frames, and SHA-256.
- Connects acceleration to constant-acceleration equations and to Galileo's inclined-plane experiment.
- Provides long enough pauses for classroom use.

## Visual limitations visible in the real rendered contact sheet

1. The animation is technically clean but visually panel-driven. Large portions of the screen are static boxes with text while the graph changes only locally.
2. The physical object is mostly absent during the graph construction. Students see calculations of motion more than motion itself.
3. The velocity and acceleration graphs are usually separated in time, so the causal relation “local slope on v(t) → level on a(t)” is not continuously visible.
4. The 12-interval construction repeats the same right-side card architecture, creating visual monotony even though the reasoning is correct.
5. The equations are presented mainly as stacked cards. Their algebraic causality is weaker than a TransformMatchingTex chain tied to a live graph.
6. The Galileo section is correct in intent but sparse. The real contact sheet shows a ramp, a ball and the 1:4:9:16 idea, but the measurement logic is not embodied strongly enough through synchronized equal-time pulses and a data plot.
7. The graph-to-physics bridge can be stronger: acceleration should be shown simultaneously as (a) slope of v(t), (b) a level on a(t), (c) a vector/state of the moving object, and later (d) the t² signature in displacement.

## V3 visual contract

The V3 keeps the JP classroom format and physics data, but replaces static-card dominance with synchronized visual causality:

- A vector-built vehicle physically replays the same trip while a dot moves on v(t).
- The vehicle position is based on the integral of the velocity profile, not on arbitrary screen-time interpolation.
- Velocity and acceleration graphs remain vertically aligned on the same time axis.
- For every interval, vertical time guides link v(t) and a(t).
- Δv and Δt are shown geometrically on the graph before the SI calculation appears.
- The highlighted velocity segment morphs into the corresponding acceleration level.
- A compact six-step reasoning rail replaces large repeated cards.
- The final acceleration graph is replayed with the moving vehicle, velocity and acceleration readouts.
- The derivation of v=v0+at uses one morphing equation chain beside a visible slope triangle.
- The displacement equation is produced from the rectangle + triangle area under v(t), with the geometry transforming into the algebra.
- Galileo is animated as a measurement problem: fast free fall versus slower ramp motion, followed by equal-time pulses.
- The 1:4:9:16 distance pattern is animated at t=1,2,3,4 and then mapped to an x-versus-t² straight-line test.

## Physics rigor decisions

- Negative acceleration is not presented as backward motion. In this data set v≥0, so a<0 corresponds to decreasing speed.
- The inclined-plane section does not claim that a rolling ball always has a=g sin(theta). The exact magnitude depends on the sliding/rolling model; the constant-acceleration and t² structure is the invariant concept.
- Free fall is introduced as the constant-acceleration case a=g after the general displacement law has been established.
