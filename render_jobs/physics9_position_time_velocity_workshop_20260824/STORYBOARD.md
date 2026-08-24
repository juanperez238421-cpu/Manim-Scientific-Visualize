# Physics 9 - Position-Time Velocity Workshop

## Project identity

- Course: Grade 9 Physics / Fundamentos de Fisica
- Unit link: position-time interpretation followed by velocity-time displacement
- Language: English
- Output: projector-readable ManimCE workshop plus two PDF companions
- Visual standard: JP classroom monochrome, 16:9, large graphs, progressive equations and work pauses

## Pedagogical objective

Students calculate constant velocity from the slope of straight position-time segments, interpret the sign and steepness of the slope, and translate a piecewise position-time graph into a piecewise velocity-time graph.

## Persistent conceptual rule

`position-time vertical value -> position`

`position-time slope -> velocity`

`velocity-time vertical value -> velocity`

## Scene sequence

### Opening - READ SLOPE, CALCULATE VELOCITY

- State the lesson promise.
- Link explicitly to the previous displacement presentation.

### 01 - WORKSHOP MAP

1. choose two points;
2. calculate changes;
3. divide and keep the sign;
4. graph one velocity level per time interval.

### 02 - THE SLOPE RECIPE

- Build a straight position-time line.
- Mark `P1=(t1,x1)` and `P2=(t2,x2)`.
- Show a rise/run triangle.
- Build `v_avg=(x2-x1)/(t2-t1)=Dx/Dt`.
- Unit check: metres divided by seconds gives m/s.

### 03 - EXAMPLE A: POSITIVE VELOCITY

- Points `(1 s, 2 m)` and `(5 s, 14 m)`.
- `Dx=12 m`, `Dt=4 s`, `v=+3 m/s`.
- Interpret increasing position.

### 04 - EXAMPLE B: REST

- Horizontal line at `x=6 m` from `0 s` to `4 s`.
- `Dx=0`, therefore `v=0 m/s`.
- Distinguish zero position from zero velocity.

### 05 - EXAMPLE C: NEGATIVE VELOCITY

- Points `(1 s, 12 m)` and `(5 s, 4 m)`.
- `Dx=-8 m`, `Dt=4 s`, `v=-2 m/s`.
- Interpret decreasing position as negative direction.

### 06 - COMPARE SPEEDS BY STEEPNESS

- Object A: 10 m in 2 s -> 5 m/s.
- Object B: 6 m in 2 s -> 3 m/s.
- Keep both lines on the same axes.
- Highlight the steeper line only after both calculations appear.

### 07 - PIECEWISE POSITION GRAPH

- Points `(0,0)`, `(2,8)`, `(5,8)`, `(7,2)`.
- Calculate three slopes: `+4`, `0`, `-3 m/s`.
- Use one table row per segment.

### 08 - BUILD THE MATCHING v-t GRAPH

- Keep a compact copy of the piecewise `x-t` graph.
- Build horizontal velocity levels over `0-2`, `2-5`, and `5-7 s`.
- Use vertical guide lines at each boundary.

### 09 - WORKSHOP PROBLEM 1

- Graph from `(0 s,1 m)` to `(3 s,10 m)`.
- Pause for student work.
- Reveal `v=+3 m/s` step by step.

### 10 - WORKSHOP PROBLEM 2

- Piecewise graph `(0,2)`, `(2,8)`, `(4,8)`, `(6,0)`.
- Pause before answers.
- Reveal `+3`, `0`, `-4 m/s` and the matching `v-t` graph.

### 11 - WHOLE-TRIP AVERAGE VELOCITY

- Reuse `(0,0)`, `(2,8)`, `(5,8)`, `(7,2)`.
- Calculate total displacement divided by total time: `2/7 m/s`.
- State why this differs from an unweighted mean of the three slopes.

### 12 - FINAL RECIPE AND EXIT CHECK

Five-step process:

1. choose points on one segment;
2. calculate `Dx`;
3. calculate `Dt`;
4. divide and keep the sign;
5. draw one horizontal `v-t` level for that interval.

Final sign map: rising -> positive; horizontal -> zero; falling -> negative.

## Timing intent

- Longer pause after each completed calculation.
- Dedicated work pause before both workshop solutions.
- Final render uses `LESSON_TIME_SCALE=1.35` to support classroom reading.

## QA risks

- Coordinate labels must not collide with graph points.
- Negative velocity labels must remain above the safe lower frame.
- Piecewise table and graph must remain large enough for projection.
- Graph transitions must preserve the same time boundaries.
- Do not morph old and new headers separately.
- No answer may appear before the work pause.

## Final takeaway

On a position-time graph, velocity is not the height. Velocity is the slope.
