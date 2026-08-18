# 05 — Croquis Scene States

Croquis behavior is modeled as a small state machine rather than scattered camera calls.

## ENTER_CROQUIS_MODE

Responsibilities:

- identify the active sketch plane;
- select the matching deterministic 2D camera state;
- move camera intentionally;
- establish zoom and safe framing;
- wait for the camera to settle;
- leave existing reference geometry visible only if it helps orientation.

## BUILD_CROQUIS

Recommended internal sequence:

1. reference/construction layer;
2. primary closed profile;
3. secondary/internal geometry;
4. repeated profiles/markers;
5. dimensions/annotations when present;
6. final reading pause.

During this state, perspective motion is normally disabled.

## EXIT_CROQUIS_MODE

Responsibilities:

- complete final observation pause;
- preserve the profile when it must explain the subsequent operation;
- move deliberately to an appropriate model view;
- introduce extrusion/cut depth only after the camera transition;
- clean temporary guides after their causal role is complete.

## Current V4 mapping

| Phase | Enter state | Build | Exit |
|---|---|---|---|
| 02 Slab | PLAN_2D | slab outline | oblique slab extrusion view |
| 04 Walls + columns | PLAN_2D | perimeter → partitions → column profiles | oblique column extrusion view |
| 07 Door | FRONT_FACE_2D | red door profile | oblique cutter/depth view |
| 08 Window | FRONT_FACE_2D | red window profile | oblique cutter/depth view |
| 09 Roof | PLAN_2D | roof outline | oblique roof extrusion view |

## Scope discipline

Protocol V1 intentionally implements only PLAN_2D and FRONT_FACE_2D because they are proven by this case study. Side/rear/local-face camera states should be added only after a real scene requires and validates them.
