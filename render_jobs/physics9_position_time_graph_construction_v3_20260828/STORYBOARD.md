# Physics 9 — Position-Time Graph Construction V3 Storyboard

## Pedagogical objective

Students should be able to construct a position-vs-time graph from motion events and then read velocity as the slope of each straight segment.

## Visual continuity strategy

One dataset remains conceptually persistent throughout the lesson:

- `(0 s, 2 m)`
- `(3 s, 8 m)`
- `(5 s, 8 m)`
- `(7 s, 4 m)`

The same motion is shown as:

1. a person moving on a one-dimensional position track;
2. a table of `(t,x)` values;
3. a position-time graph;
4. a synchronized moving point on that graph;
5. three slope / velocity calculations.

## Scene sequence

### Opening

Position vs Time Graph — construct from motion data, then read slope.

### 01 — Start with motion

- physical x-axis from 0 to 10 m;
- four event cards;
- person moves 2 -> 8 -> 8 -> 4 m;
- current event is highlighted with clean cross-fades;
- ordered-pair chain appears only after all events are understood.

### 02 — Construct the graph

- motion table on left;
- horizontal time axis introduced first;
- explicit x-axis numbers `0...7`;
- vertical position axis introduced second;
- explicit y-axis numbers `0,2,...,10`;
- temporary callouts identify axes and units;
- scale card states `1 s horizontally`, `2 m vertically`;
- axis callouts fade out before plotting;
- each table row is highlighted without morph distortion;
- guides project each data pair onto the graph;
- after all points are present, connect in chronological order.

### 03 — Same motion, two representations

- physical track remains above;
- position-time graph remains below;
- one person and one graph point move together;
- a live time readout reinforces synchronization;
- interval cards cross-fade: moving right -> at rest -> moving left;
- traced path progressively reconstructs the graph.

### 04 — Slope is velocity

- general rule `v = slope = Δx/Δt` is established first;
- one graph segment becomes dominant at a time;
- a rise/run triangle is drawn directly on the segment;
- Δx and Δt labels correspond to the algebra at right;
- final velocity answer is boxed in place, never detached;
- cases: `+2 m/s`, `0 m/s`, `-2 m/s`.

### 05 — Read the graph correctly

Four misconception cards:

- height = position;
- slope = velocity;
- graph is not a map of the physical path;
- positive position can coexist with negative velocity.

### 06 — Six-step method

1. record data;
2. time horizontal;
3. position vertical;
4. choose equal readable scale;
5. plot then connect chronologically;
6. read slope with `v = Δx/Δt`.

Exit question remains unsolved for student participation.

## Timing intent

- short pauses during axis construction;
- longer pause after the completed graph;
- deliberate 3 s / 2 s / 2 s synchronized motion to match the time intervals qualitatively;
- long read pauses after each slope calculation;
- final exit question held long enough for classroom response.

## QA risks and mitigations

- **Axis label crowding:** numbers are explicit objects and graph length is slightly reduced from V2.
- **Point/callout overlap:** callout cards are removed before plotting begins.
- **Transform gibberish:** unrelated text cards never morph glyph-to-glyph.
- **Detached answer box:** answer rectangle created after final equation positioning.
- **Slope triangle collisions:** triangle labels use 20 pt MathTex and stay inside graph area.
- **Header clipping:** inherited JP header fit remains active; dense audit will inspect all section transitions.
- **Transient frames:** 96 distributed audit frames plus every-frame automated scan are mandatory.

## Final takeaway

**Position is read from graph height. Velocity is read from graph slope.**
