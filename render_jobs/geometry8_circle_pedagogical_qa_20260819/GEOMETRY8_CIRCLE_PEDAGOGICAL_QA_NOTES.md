# Geometry 8 Circle — Pedagogical Sequence Senior QA

## Scope

This revision converts the approved 38-page pedagogical PDF sequence into one reproducible ManimCE master scene:

1. Circle Fundamentals
2. Circle Class 2 — Parts, Arcs and Lines
3. Bridge to guided practice
4. Circle Workshop

All mathematical values, terminology, figures and conceptual order remain grounded in the already rendered lesson sources.

## Senior QA finding

The main visual defect in the existing workshop is not mathematical; it is layout compression. Each worked exercise creates six independent cards (`PROBLEM`, `THINK`, `STRATEGY`, `SOLVE`, `CHECK`, `ANSWER`), arranges all six vertically, and then passes the stack through `split_layout(... max_height=5.35)`. The resulting scale reduction makes card text and formulas unnecessarily small at classroom projection distance.

## Fix

The master scene preserves the original workshop objects and data but replaces the display logic for guided solutions. It now:

- restores each existing card to projector width after the compressed layout has been calculated;
- keeps `PROBLEM` large and persistent;
- shows `THINK` and `STRATEGY` sequentially rather than simultaneously;
- transforms to the original `SOLVE` object at large scale;
- finishes with readable `SOLVE + CHECK + FINAL ANSWER` states;
- keeps the original left-side geometry figures, exact numbers, terminology and solution logic;
- increases the formula-choice scenario text and answer scale;
- changes the exit ticket from three small simultaneous question cards to three large sequential question states.

The scene also reproduces the approved PDF module order by postponing the Fundamentals closing bridge until after Class 2.

## Acceptance

- `py_compile` for the reconstructed source stack and master scene.
- Literal `-pql` runtime gate with accelerated lesson timing.
- Literal `-pqh` final render with ManimCE 0.20.1.
- 1920×1080, 30 fps, H.264, yuv420p.
- Full FFmpeg decode.
- 48 dense final-render audit frames.
- SHA-256 of the final MP4.
