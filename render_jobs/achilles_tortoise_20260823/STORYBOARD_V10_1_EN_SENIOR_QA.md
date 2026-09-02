# Achilles and the Tortoise — V10.1 Final Senior QA Storyboard

## Goal
Keep the continuous V10 narrative while eliminating the three residual visual defects found in the first V10 PQH audit.

## V10.1 QA corrections
1. Meeting callouts move upward/right into reserved whitespace so they do not cover the Δx₀ data chip or either racer.
2. Stage metadata no longer morphs glyph-to-glyph. The old metadata fades while the same racers, interval band, connectors, baseline, and target remain visible; the new metadata then fades in. This preserves diagram continuity without producing unreadable intermediate text.
3. STEP 1 no longer uses three crowded ×1/10 arrows. The left column now ends with the clean recurrence Δt_{n+1}=(1/10)Δt_n, while the right side shows the general term Δt_n=(1/10)^{n-1}s.

## Story structure

### 01 — THE REAL RACE: WHERE DO THEY MEET?
- Persistent master track.
- v_A=10 m/s, v_T=1 m/s, initial lead 10 m.
- x_A(t)=10t and x_T(t)=10+t.
- Solve t*=10/9 s and x*=100/9 m.
- At the meeting, Achilles and the tortoise share the same x-coordinate but remain on separate vertical lanes.
- The MEETING POSITION formula is shown in an offset callout connected to the x* marker.

### 02 — ZENO CHANGES THE DESCRIPTION, NOT THE MOTION
- Rewind the same racers.
- Explain the checkpoint rule without removing the track or analysis panel.
- Select [0,10] m and connect it to the analysis panel.

### 03 — ONE GAP, MAGNIFIED AGAIN AND AGAIN
- Stage 1: [0,10] m, Δt=1 s, new gap=1 m.
- Stage 2: [10,11] m, Δt=0.1 s, new gap=0.1 m.
- Stage 3: [11,11.1] m, Δt=0.01 s, new gap=0.01 m.
- Stage 4: [11.1,11.11] m, Δt=0.001 s, new gap=0.001 m.
- The same magnifier, racers, baseline, target, master track, and panel persist.
- Only compact metadata changes between stages.
- Reveal g_n=10(1/10)^n and lim g_n=0.

### 04 — INFINITELY MANY STAGES, FINITE TOTAL TIME

#### Step 1 — Time intervals
Δt₁=1 s
Δt₂=0.1 s
Δt₃=0.01 s
Δt₄=0.001 s

Recurrence:
Δt_{n+1}=(1/10)Δt_n

#### Step 2 — Partial sums
S₁=1.000
S₂=1.100
S₃=1.110
S₄=1.111

General term:
Δt_n=(1/10)^{n-1}s

#### Step 3 — Finite geometric sum
S_N=1+1/10+1/10²+...+1/10^{N-1}

S_N=[1-(1/10)^N]/[1-1/10]

Emphasize that this is still a finite sum.

#### Step 4 — Known limit
(1/10)^N → 0 as N→∞

T=lim S_N=(1-0)/(1-1/10)=10/9 s

Numerical bridge:
1.000 → 1.100 → 1.110 → 1.111 → ... → 1.111...

### 05 — THE LIMIT IS THE PHYSICAL MEETING
- Clear derivation content.
- Display only t*=10/9 s and x*=100/9 m.
- Use the offset MEETING POINT callout.
- Replace the synthesis sentence with: “For every t > 10/9 s, Achilles is ahead.”

## Final acceptance gates
- English only.
- No text/icon overlap at either meeting.
- No TARGET/runner collision.
- No metadata glyph collision during stage changes.
- No crowded ×1/10 arrows.
- No formula clipping.
- No stacked closing text.
- Persistent track and panel retained.
- Sequence is mathematically explicit: recurrence → partial sums → finite sum → limit → 10/9.
- Literal -pql PASS before literal -pqh.
- PQH 1920×1080, 30 fps, H.264/yuv420p.
- Full FFmpeg decode PASS.
- Dense audit frames inspected at all critical transitions.
- Final delivery is a reproducible ZIP containing source, builder, storyboard, style, protocol, workflow, MP4, logs, hashes, and audit frames.
