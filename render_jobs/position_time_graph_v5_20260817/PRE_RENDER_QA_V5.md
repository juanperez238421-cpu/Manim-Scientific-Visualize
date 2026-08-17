# Position–Time Graph Senior V5 — Pre-render QA

## Re-score of delivered V4
Overall: **8.2 / 10** under the stricter classroom-visibility standard requested on 2026-08-17.

- Pedagogical sequencing: 9.7/10
- Physics / graph interpretation: 9.7/10
- Graph-construction logic: 9.5/10
- Stable visual hierarchy: 7.9/10
- Element / font size: 7.4/10
- Overlap / merge robustness: 7.5/10
- Camera focus / visual guidance: 6.8/10
- Classroom pacing: 7.9/10

## Confirmed defects in V4 audit frames
1. Some sampled section transitions show merged/interpolated glyphs caused by `ReplacementTransform` between unrelated headers.
2. Several table/graph scenes use excessive white space, making the meaningful geometry too small.
3. Scenes 7–12 rely heavily on static two-column layouts; graph features and formulas compete for attention.
4. Position/velocity labels and point markers are legible but too small for projection from the back of a classroom.
5. The graph-to-motion reconstruction is correct but lacks camera emphasis linking the physical track and graph.
6. Reading holds are shorter than ideal after dense graph/formula transitions.

## V5 design corrections
- Override section-header transitions with full fade-out / clean fade-in. No morphing between unrelated title glyphs.
- Increase axis lengths, graph labels, table fonts, point radius, line thickness, readouts and formula sizes.
- Add stable-layout overlap assertions between major UI blocks.
- Use `MovingCameraScene` zoom/pan for the physical motion, point plotting, chronological graph tracing, slope triangles, graph-to-motion reconstruction, tangent preview and summary rows.
- Recompose scenes 7–12: graph appears large first; only after the key feature is understood does it reduce for side explanation.
- Increase reading pauses and set final `LESSON_TIME_SCALE=1.15`.
- Preserve the exact JP classroom style payload already validated by SHA-256 in the prior run.

## Acceptance target
Final V5 must pass:
`py_compile -> literal -pql -> literal -pqh -> ffprobe -> full ffmpeg decode -> dense frame audit -> SHA-256 -> delivery package`.
