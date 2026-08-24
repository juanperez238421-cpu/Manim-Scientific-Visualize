# Physics 9 — Position, Velocity and Displacement from Graphs

## Project identity

- Course: Grade 9 Physics / Fundamentos de Física
- Planning block: Week 2, 24–28 August 2026
- Lesson link: Achilles/Zeno consolidation → velocity–time graph → area as displacement
- Language: English, matching the course planning and the existing Achilles/position–time materials
- Target: projector-readable 1920×1080 ManimCE presentation with deliberate notebook-copy pauses

## Pedagogical objective

Students should be able to connect the physical meeting of Achilles and the tortoise with the intersection of two position–time lines, read constant velocity from slope, and calculate displacement as signed area under a velocity–time graph.

## Continuity strategy

The same numerical model is preserved across the first half of the lesson:

- Achilles: `x_A(t)=10t`, `v_A=10 m/s`
- Tortoise: `x_T(t)=10+t`, `v_T=1 m/s`
- Meeting: `t*=10/9 s`, `x*=100/9 m`

The intersection in the position–time graph becomes the bridge to the two horizontal lines in the velocity–time graph. Their rectangular areas are then reconciled with the common meeting position.

## Scene sequence

### Opening — FROM MEETING POINT TO DISPLACEMENT

- State the full lesson promise.
- Keep the frame uncluttered and pause long enough to establish the transition from the prior paradox lesson.

### 01 — TODAY'S MAP

Three large cards:

1. locate the meeting on `x–t`;
2. read velocity from slope;
3. calculate displacement from `v–t` area.

### 02 — CONSOLIDATE THE PHYSICAL MEETING

- Show a physical track and the initial 10 m lead.
- Build the two equations progressively.
- Solve `10t=10+t` and box `t*=10/9 s` and `x*=100/9 m`.
- Notebook pause on the boxed result.

### 03 — THE SAME MEETING ON AN x–t GRAPH

- Build axes first.
- Animate Achilles's line from the origin.
- Animate the tortoise's parallel-start-offset line from `x=10 m`.
- Mark the intersection with dashed projections to both axes.
- Explicitly state: same time + same position = physical meeting.

### 04 — WHAT THE SLOPES SAY

- Use two slope triangles tied to the same lines.
- Show `slope=Δx/Δt=v`.
- Evaluate `10/1=10 m/s` and `1/1=1 m/s`.
- Keep the graph visible while the calculation cards appear.

### 05 — FROM x–t SLOPE TO v–t HEIGHT

- Transition to a velocity–time graph.
- Draw horizontal lines at 10 m/s and 1 m/s.
- Explain that constant velocity produces a horizontal line.
- Preserve the same time axis and catch time.

### 06 — AREA UNDER v–t IS DISPLACEMENT

- Shade one rectangle dynamically.
- Build `Δx = area = base × height = Δt × v`.
- Perform the unit check `(s)(m/s)=m`.
- Distinguish graph height (velocity) from shaded area (displacement).

### 07 — RECONCILE THE ACHILLES MEETING

- Shade Achilles's area from `0` to `10/9 s`: `100/9 m`.
- Shade the tortoise's area: `10/9 m`.
- Add the tortoise's initial position: `10 + 10/9 = 100/9 m`.
- Finish with the same meeting coordinate obtained from the `x–t` intersection.

### 08 — GUIDED PIECEWISE EXAMPLE

- Given graph: `4 m/s` for `0–2 s`, then `2 m/s` for `2–5 s`.
- Split into two rectangles.
- Calculate `A1=8 m`, `A2=6 m`, total displacement `14 m`.
- Include a structured pause before the final total.

### 09 — AREA BELOW THE AXIS

- Given graph: `+2 m/s` for `0–3 s`, then `−1 m/s` for `3–5 s`.
- Area above is positive; area below is negative.
- Net displacement: `6−2=4 m`.
- Distance travelled: `6+2=8 m`.
- Keep displacement and distance visually separated.

### 10 — NOTEBOOK RECIPE + EXIT TICKET

Method map:

1. read axes and units;
2. split the region;
3. calculate each area;
4. apply the sign;
5. add and write metres.

Exit ticket: a `3 m/s` horizontal line from `0–4 s`; students determine displacement and explain the units. Reveal `12 m` only after a work pause.

## Camera and animation rules

- Default camera remains stable at 16:9.
- One controlled zoom is allowed for the first shaded area and unit cancellation.
- Headers disappear during the zoom and return atomically afterward.
- Graphs are constructed causally: axes → curve/segments → projection lines → area → equation.
- No graph or equation is replaced before its interpretation has been stated.

## Timing intent

- Short pauses: after labels and single definitions.
- Read pauses: after each completed graph.
- Explain pauses: after each worked calculation.
- Work pause: before guided-example and exit-ticket answers.
- Final pause: on the five-step recipe and closing statement.

## QA risks and controls

- Long headers: fit within the persistent safe header width.
- Tick labels: use restrained font sizes and explicit axis ranges.
- Shaded regions: set low opacity so axes, outlines and labels remain readable.
- Meeting callout: reserve upper-right whitespace and keep it away from the plotted lines.
- Negative area: label it below the axis without clipping the lower frame.
- Piecewise examples: do not show every equation at once; reveal one area at a time.
- Final frame: avoid stacking the recipe and exit ticket simultaneously.

## Final takeaway

An `x–t` graph tells where an object is; its slope tells velocity. A `v–t` graph tells velocity; its signed area tells displacement.
