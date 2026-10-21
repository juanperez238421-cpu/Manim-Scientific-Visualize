# Geometry 8 — Areas sombreadas — Quiz B — Presentacion V2

## Scope
- Only **version B** of the original IJR quiz from 2026-10-19.
- Exactly two problems, each with **20 minutes (1,200 seconds) of solve time**.
- Problem 1: seven non-overlapping gray regions **A, B, C, D, E, F, G**, all added.
- Problem 2: exterior rectangle **R**, with six white cutouts **A, B, C, D, E, F** subtracted.
- Original dimensions, formula names and lettering are preserved; no final area answers shown on student screens.
- Source of truth: original Version B quiz PDF and source TikZ Figura_B1.tex / Figura_B2.tex; not the unrelated Canada presentation V1.

## Protocol
Read docs/PROTOCOL_MANIMCE_PQH_DIRECT_GITHUB_DELIVERY.md. Final MP4 must be 1920×1080, H.264, 30/1 fps, yuv420p, with full decode and sampled-frame visual QA, SHA-256 and direct GitHub MP4 publication. A source branch or an Actions artifact is not final MP4 delivery.

## Build
Use source/quiz_b_v2_manim.py with ManimCE, Noto Serif, LaTeX/dvisvgm and FFmpeg. Generate a still per problem:

    G8_PROBLEM=1 manim -s -qh --fps 30 source/quiz_b_v2_manim.py QuizBCard
    G8_PROBLEM=2 manim -s -qh --fps 30 source/quiz_b_v2_manim.py QuizBCard

Do not infer numbers from image lengths. Encode each exactly 1200-second study window from the validated still, updating the countdown once each second then interpolating static frames to 30 fps. A 1200.000000 s interval is 36,000 frames at 30 fps. Use this clock format inside FFmpeg drawtext (the slashes are escape syntax):

    %{eif\:floor(ceil(1200-t)/60)\:d\:2}\:%{eif\:mod(ceil(1200-t)\,60)\:d\:2}

Sequence: opening → problem 1 prompt → 20-minute problem 1 clock → time-up card → problem 2 prompt → 20-minute problem 2 clock → time-up card. Only the problem intervals, not the entire final video, are exactly 20 minutes each. A fixed video-clock follows media playback (pause/speed/seek). An independent HTML wall-clock timer is a different client and can use Date.now.

## QA gates
- Math: original coefficients/letters A–G and R/A–F; no answer leakage.
- Source: Python syntax check and ManimCE runtime QA.
- Clock: 20:00 at 0 s, 10:00 at 600 s, 00:01 at 1199 s; time-up only after 1200 s.
- FFprobe: 1920×1080, H.264/yuv420p, 30/1 fps, 36,000 frames for each countdown.
- Full decoder: zero fatal errors.
- Contact sheet: opening, both figures, midpoints, and both timer boundary frames.
- SHA-256 of exact final binary and direct raw GitHub publication after validation.
- Existing workflows, source files and published videos remain untouched.

This is an isolated source proposal. Do not claim final GitHub video publication based on this PR alone.
