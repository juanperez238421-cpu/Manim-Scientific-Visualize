# Achilles and the Tortoise — V9 Continuous Diagram Storyboard

## Direction goal
Create one continuous mathematical space. The master race diagram never disappears after it is introduced. A single analysis panel remains anchored below the track and changes role from algebra workspace -> interval magnifier -> convergence timeline -> final result. The viewer should always know where the current interval lives in the original race.

## Visual grammar
- 16:9 Full HD, white background, black/neutral gray JP Classroom hierarchy.
- Persistent numbered section header and subtitle.
- Persistent master track from x=0 m to x=12 m.
- Persistent Achilles and tortoise icons on separate vertical lanes.
- Persistent analysis panel below the track.
- Current interval on the master track is highlighted by a neutral translucent selection band.
- Two connector lines visually link that selected interval to the magnified panel.
- No full-screen fade between Zeno stages. Stage changes use Transform / object motion.
- English only.

## Shot 01 — Physical race and exact meeting (0–30 s)
**Header:** THE REAL RACE: WHERE DO THEY MEET?

1. Draw the master track once.
2. Introduce Achilles at 0 m and the tortoise at 10 m.
3. Show compact data chips: v_A = 10 m/s, v_T = 1 m/s, initial lead = 10 m.
4. The analysis panel is already visible below the track.
5. Write the position equations inside the same panel:
   - x_A(t)=10t
   - x_T(t)=10+t
   - 10t=10+t -> t*=10/9 s
   - x*=100/9 m = 11.111... m
6. Animate both racers continuously to the meeting point.
7. Add a persistent dashed meeting marker at x*=100/9 m.

## Shot 02 — Rewind and change the description (30–45 s)
**Header:** ZENO CHANGES THE DESCRIPTION, NOT THE MOTION

1. Keep the same track and same analysis panel.
2. Smoothly rewind the two racers to their initial positions; do not remove them.
3. Replace the algebra content inside the analysis panel with a concise explanation of Zeno's checkpoint rule.
4. Highlight the first travel interval [0,10] m on the master track.
5. Connect the highlighted interval to the analysis panel with two thin guide lines.

## Shot 03 — Persistent interval magnifier (45–105 s)
**Header:** ONE GAP, MAGNIFIED AGAIN AND AGAIN

The outer analysis panel is never redrawn. It becomes a magnifying lens.

### Stage 1
- Master interval: Achilles travels 0 -> 10 m.
- Duration: 1 s.
- Tortoise moves 10 -> 11 m.
- New gap: 1 m.
- In the lens, Achilles moves from left edge to the old tortoise position while the tortoise moves to the right edge.

### Transition to Stage 2
- On the master track, the selection band transforms from [0,10] to [10,11].
- In the lens, the existing Achilles icon slides from the target to the left edge and the tortoise slides from the right edge to the target. This motion means: "we recenter and magnify the remaining gap."
- Numeric metadata morphs; no fade-out of the diagram.

### Stage 2
- 10 -> 11 m, duration 0.1 s, new gap 0.1 m.

### Stage 3
- 11 -> 11.1 m, duration 0.01 s, new gap 0.01 m.

### Stage 4
- 11.1 -> 11.11 m, duration 0.001 s, new gap 0.001 m.

### Pattern reveal
- Keep the master track visible.
- Keep the lens visible.
- Morph the stage metadata into `10 -> 1 -> 0.1 -> 0.01 -> 0.001 -> ...`.
- Add `g_n = 10(1/10)^n` and `lim g_n = 0`.

## Shot 04 — Time convergence without leaving the race (105–135 s)
**Header:** INFINITELY MANY STAGES, FINITE TOTAL TIME

1. Keep the master race above.
2. The same analysis panel morphs from spatial lens into a horizontal time bar.
3. Grow adjacent segments 1 s, 0.1 s, 0.01 s, 0.001 s toward a fixed dashed limit at 10/9 s.
4. Show cumulative time updating.
5. Build the geometric-series equation one line at a time.
6. Visual statement: "Infinite subdivisions do not require infinite time."

## Shot 05 — Convergence becomes the physical catch (135–155 s)
**Header:** THE LIMIT IS THE PHYSICAL MEETING

1. Keep the track; no cut.
2. Racers are already near x=11.111 m from Stage 4.
3. Move them the final tiny amount to x*=100/9 m.
4. Pulse the existing meeting marker.
5. Move Achilles slightly beyond the tortoise.
6. The analysis panel morphs into the final two results: t*=10/9 s and x*=100/9 m.
7. End on the same race diagram with the takeaway: "Zeno creates infinitely many checkpoints; calculus shows their times converge."

## QA acceptance criteria
- English only in visible lesson content.
- Master race track remains continuously visible from introduction through final catch.
- Main Achilles/tortoise objects are transformed/moved, not repeatedly destroyed and recreated during interval analysis.
- The analysis-panel outline remains continuously visible after first appearance.
- No full-scene fade between Stages 1–4.
- Stage 1–4 transitions visually recenter/magnify the previous remaining gap.
- No text overlap, clipping, merged labels, or stale subtitles.
- Mathematical claims validated: t*=10/9 s and x*=100/9 m.
- Literal `-pql` must pass before literal `-pqh`.
- Final: 1920x1080, 30 fps, H.264/yuv420p, full ffmpeg decode, SHA-256, dense audit frames.
