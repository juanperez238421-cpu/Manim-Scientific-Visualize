# Senior QA — Two-Object Position-Time Meeting V1 -> V2

## V1 render reviewed
`Physics9_Two_Object_Position_Time_Meeting_SENIOR_QA_FINAL_pqh.mp4`

Technical result:
- 1920×1080
- 30 fps
- H.264 / yuv420p
- 164.864714 s
- 4,946 frames
- full FFmpeg decode: PASS
- all-frame scan: 4,946 / 4,946
- blank frames: 30
- very sparse frames: 37
- border-heavy frames: 0

## Visual review method
- 96-frame distributed contact sheet.
- 8 targeted frames around second-graph construction, graphical intersection, synchronized meeting and equation verification.
- Additional full-resolution frames sampled around sections 7–9.

## V1 strengths confirmed
- Clear opposite-direction physical model and velocity signs.
- Two data tables are readable and synchronized to the physical track.
- Explicit graph scale remains visible.
- Object A solid/filled and Object B dashed/hollow remain distinguishable in grayscale.
- Both graphs share exactly one coordinate system and scale.
- Intersection `(4 s, 9 m)` is visually unambiguous.
- Student-check pause occurs before the intersection answer appears.
- Track motion and graph points reach the meeting simultaneously.
- `x = x0 + vt` derivation is mathematically correct and readable.
- Graphical and algebraic results agree.

## Release-blocking transient found
A full-resolution frame during the section 8 -> section 9 transition shows severely overlapped/warped title and subtitle glyphs. The stable frames before and after are correct, but a classroom video is judged on all visible animation frames, not only steady states.

Cause: the shared JP header implementation uses `ReplacementTransform` between unrelated title/subtitle strings. This can create undesirable glyph interpolation even when title and subtitle are changed in the same `play()` call.

## V2 correction
`Physics9TwoObjectMeetingXTV2` subclasses the accepted V1 lesson without changing any lesson content. It overrides only `set_header()` so that:
1. the old header/subtitle fade out;
2. the canonical JP header geometry is rebuilt;
3. the new header/subtitle fade in.

This preserves the exact typography, sizing, spacing and safe-zone logic while removing glyph morphing between semantic section states.

## V2 acceptance
V2 is final only after:
- Python compile;
- literal PQL;
- literal PQH;
- Full-HD technical checks;
- full decode;
- every-frame scan;
- 96-frame distributed audit;
- targeted transition frames around sections 7, 8 and 9;
- no mixed/warped header text;
- SHA-256 and reproducible ZIP.
