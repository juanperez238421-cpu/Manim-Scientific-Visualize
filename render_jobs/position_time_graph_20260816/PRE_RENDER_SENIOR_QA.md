# Position–Time Graph — Senior Pre-Render QA

## Previous answer review
The prior answer used pre-rendered matplotlib slides assembled into a video. That was rejected because it did not satisfy the requested ManimCE protocol, did not use the JP classroom architecture, and did not provide concept-driven animation.

## V1 ManimCE reconstruction score before render
**8.9 / 10 (code/design review, before runtime render)**

| Criterion | Score | Review |
|---|---:|---|
| Pedagogical sequence | 9.5 | Physical motion → data → axes → points → graph → reading → slope → story. |
| JP style fidelity | 10.0 | Uses the exact JP style library; SHA-256 verified. |
| Mathematical accuracy | 10.0 | All displayed positions and segment velocities are asserted in `validate_lesson_data()`. |
| Visual hierarchy | 9.0 | Large graph-first layouts, minimal simultaneous content, persistent headers. |
| Animation pedagogy | 9.2 | Data rows, guide lines, moving dots, graph trace, slope triangles, synchronized graph-to-story. |
| Runtime confidence | 7.8 | Static compilation passes; Manim runtime must still be validated by `-pql`. |

## Senior design decisions
1. Begin from physical motion instead of beginning from axes.
2. Use a simple piecewise motion dataset: away at +1 m/s, rest, return at -1 m/s.
3. Build the table before graphing so every plotted point has an observable source.
4. Animate each ordered pair with vertical/horizontal guide lines.
5. Explain slope sign and magnitude in separate scenes to avoid overcrowding.
6. Reconstruct the original motion from the completed graph to close the conceptual loop.
7. Add a curved graph/tangent preview only after the piecewise-linear case is mastered.
8. End with a nine-step process map students can reproduce independently.

## Static QA
- Python `py_compile`: PASS
- Modular section methods: 13 scenes + opening
- Absolute asset paths: none
- External image dependencies: none
- Exact style SHA-256: `3f3f06e94d5cad870ad335502cc1a93e56ce675abb1231ded5f9c71fd3e60e3d`
- Target environment: ManimCE 0.20.1
- Target output: 1920×1080, 30 fps, H.264, yuv420p

## Render acceptance gate
The final video is accepted only if:
- full `-pql` runtime QA passes;
- literal `-pqh` render passes;
- duration is between 4 and 7 minutes;
- `ffprobe` confirms 1920×1080, 30 fps, H.264, yuv420p;
- full FFmpeg decode passes;
- dense audit frames are produced;
- SHA-256 is recorded.
