# ADR-001 — Enter orthographic 2D before croquis construction

- Status: Accepted for Protocol V1
- Date: 2026-08-18
- Case: House Step-by-Step V3

## Context

The V3 wall/column croquis was geometrically correct but was drawn from an oblique 3D camera (`phi=36°`, `theta=-58°`). Door/window cut profiles and the roof outline had the same underlying problem: a 2D profile was being explained without a dedicated 2D viewing state.

## Decision

Every important croquis begins only after:

1. selecting the active sketch plane;
2. moving to its deterministic face-normal/plan 2D camera state;
3. completing camera motion;
4. waiting a perceptible settling pause;
5. beginning profile construction.

Protocol V1 defines PLAN_2D and FRONT_FACE_2D because these are the two states proven by the House case.

## Consequences

Positive:
- technical profiles read as drawings rather than perspective decoration;
- profile topology is easier to inspect;
- camera behavior becomes testable;
- future scenes gain consistent visual grammar.

Cost:
- additional camera transitions and runtime;
- every 2D state must be verified in rendered frames, not assumed from angle values alone.
