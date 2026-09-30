# Achilles and the Tortoise — V10 Senior QA Storyboard

## Direction goal
Preserve the successful continuous-diagram language of V9.2 while removing every known overlap and making the time-series argument more pedagogically explicit. The master race remains visible; the analysis panel remains anchored; only its internal role changes.

## Senior QA findings from V9.2
1. At the first physical meeting, character labels and the meeting formula overlap near x*=100/9 m.
2. In magnified Stages 3–4, the TARGET chip can collide with Achilles.
3. The convergence section writes formulas over the time bar and clips the lowest expression.
4. The final MEETING label and closing sentences overlap.
5. The jump from 1 + 0.1 + 0.01 + ... directly to the infinite-series formula is mathematically correct but too abrupt for instruction.

## Visual grammar
- 16:9 Full HD, white background, black/neutral gray JP Classroom hierarchy.
- English visible content only.
- Persistent master track, persistent analysis panel, persistent racers.
- Achilles and tortoise use clearly separated vertical lanes whenever they share the same x-coordinate.
- Meeting information uses an offset callout + arrow; never place formulas on top of the racers.
- No full-screen fade between Zeno stages.
- Each mathematical derivation reserves a clean vertical zone; no formula may cross a diagram, bar, caption, or panel boundary.

## Shot 01 — Solve the ordinary race first
**Header:** THE REAL RACE: WHERE DO THEY MEET?

1. Draw the master track and data chips.
2. Write x_A(t)=10t and x_T(t)=10+t.
3. Set positions equal and solve: 10t = 10 + t, then t*=10/9 s.
4. Substitute into x_A to get x*=100/9 m.
5. Move both racers to the same x-coordinate on separate vertical lanes.
6. Fade moving name labels before the meeting.
7. Show the meeting formula in a callout box offset from the racers and connected to x* by an arrow.

## Shot 02 — Reframe the same motion using Zeno
**Header:** ZENO CHANGES THE DESCRIPTION, NOT THE MOTION

- Smooth rewind; no diagram removal.
- Explain the checkpoint rule.
- Highlight [0,10] m and connect it to the persistent analysis panel.

## Shot 03 — One gap, magnified repeatedly
**Header:** ONE GAP, MAGNIFIED AGAIN AND AGAIN

- The panel becomes one persistent lens.
- Stage metadata is compact: stage number, selected interval, and duration.
- The new gap is labeled only next to its bracket.
- TARGET is offset left so it never collides with Achilles.
- Master racers remain on separate vertical lanes.

Stage sequence:
- Stage 1: [0,10] m, Δt=1 s, new gap=1 m.
- Stage 2: [10,11] m, Δt=0.1 s, new gap=0.1 m.
- Stage 3: [11,11.1] m, Δt=0.01 s, new gap=0.01 m.
- Stage 4: [11.1,11.11] m, Δt=0.001 s, new gap=0.001 m.

Pattern reveal:
g_n = 10(1/10)^n and lim g_n = 0.

## Shot 04 — Build the time result step by step
**Header:** INFINITELY MANY STAGES, FINITE TOTAL TIME

### Step 1 — Identify the time sequence
Δt_1 = 1 s, Δt_2 = 0.1 s, Δt_3 = 0.01 s, Δt_4 = 0.001 s, with ×1/10 between rows.
General term: Δt_n = (1/10)^(n-1) s.

### Step 2 — Make the accumulation intuitive
Show S_1=1.000, S_2=1.100, S_3=1.110, S_4=1.111.
Each checkpoint adds one smaller decimal place.

### Step 3 — Use a finite geometric sum first
S_N = 1 + 1/10 + 1/10^2 + ... + 1/10^(N-1)
S_N = [1-(1/10)^N]/[1-1/10]
Caption: “This is a finite geometric sum, so no infinity has been used yet.”

### Step 4 — Apply the known limit
(1/10)^N -> 0 as N -> infinity.
Then T = lim S_N = (1-0)/(1-1/10) = 10/9 s.
Connect symbolic and decimal views:
1.000 -> 1.100 -> 1.110 -> 1.111 -> ... -> 1.111...
Takeaway: “Infinitely many checkpoints accumulate at a finite time.”

## Shot 05 — Return to the physical race
**Header:** THE LIMIT IS THE PHYSICAL MEETING

1. Clear convergence derivation content.
2. Show only the two boxed final results.
3. Move racers to the same x-coordinate on separate lanes.
4. Show an offset MEETING POINT callout and arrow.
5. Replace the synthesis sentence with the post-meeting statement; never stack both: “For every t > 10/9 s, Achilles is ahead.”

## QA acceptance criteria
- No overlap in the first meeting callout.
- No TARGET/runner collision at any magnified stage.
- No icon merging on the master track.
- No formula/time-diagram overlap.
- No clipping at the bottom of the analysis panel.
- No stacked closing sentences.
- English only.
- Persistent diagram maintained through all Zeno stages.
- Mathematical sequence explicitly progresses: ratio -> partial sums -> finite sum -> limit -> 10/9.
- Literal -pql PASS before -pqh.
- Final PQH: 1920x1080, 30 fps, H.264/yuv420p.
- Full ffmpeg decode PASS.
- Dense audit frames reviewed at all critical transitions.
- Final delivery is a complete reproducible ZIP project package.
