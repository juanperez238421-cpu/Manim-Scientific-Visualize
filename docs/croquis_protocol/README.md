# Croquis Rendering Protocol

This directory is built from frame-level and source-level analysis of the House Step-by-Step reference implementation and its successive protocol revisions.

## Core invariant

Every technical croquis must enter a stable orthographic 2D camera state before construction geometry begins.

A croquis that drives additive or subtractive geometry must also be visibly closed before depth is introduced. Displayed wall footprints must match the thickness, center and orientation of the actual 3D wall solids.

## Current architectural baseline — House V5

- Stable `PLAN_2D` and `FRONT_FACE_2D` camera states before sketch construction.
- Closed wall profiles derived from the exact wall-solid specifications.
- Internal wall profiles constructed one-by-one with semantic pauses.
- LaTeX (`Tex`/`MathTex`) for technical text and `self.play(Write(...))` for its introduction.
- Transparent exterior walls when opaque facades would obstruct the interior construction logic.
- Named timing classes rather than arbitrary waits.
- Mandatory PQL visual gate before literal PQH delivery.
- Final PQH QA: ffprobe, full FFmpeg decode, semantic audit frames and SHA-256.

See the numbered protocol documents, ADRs and `case_studies/house_step_v5.md` for implementation details.
