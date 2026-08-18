# 03 — Camera Protocol

## Camera state machine

`MODEL_3D → ENTER_CROQUIS → CROQUIS_2D → EXIT_CROQUIS → MODEL_3D`

A croquis phase is not valid until the camera transition has finished and the settling pause has elapsed.

## PLAN_2D

Reference implementation:

```python
PLAN_2D_PHI = 0 * DEGREES
PLAN_2D_THETA = -90 * DEGREES
PLAN_2D_ZOOM = 0.80
```

Used when the active sketch plane is horizontal (XY):

- slab footprint;
- wall/partition traces;
- column profiles;
- roof outline.

## FRONT_FACE_2D

Reference implementation:

```python
FRONT_2D_PHI = 90 * DEGREES
FRONT_2D_THETA = -90 * DEGREES
FRONT_2D_ZOOM = 0.82
```

Used when the active sketch plane is the front facade (XZ):

- door profile;
- window profile.

The exact sign/orientation is subject to rendered-frame verification; a face-normal state must never be accepted from angles alone without QA.

## Entry contract

`enter_*_croquis()` must:

1. stop unrelated camera motion;
2. move to the deterministic 2D orientation;
3. establish framing/zoom;
4. finish camera motion;
5. wait `CAMERA_SETTLE_PAUSE`;
6. only then permit `Create`/`Write` of important technical geometry.

## Exit contract

`return_model_view()` must occur only after the 2D profile has been readable for a semantic pause. The profile may remain visible during the return to 3D when that continuity explains how depth is introduced.

## Prohibited patterns

```python
self.move_camera(..., run_time=1.6)
self.play(Create(croquis), ...)
```

is prohibited when the target camera is still an oblique model view.

Also prohibited: combining a camera transition and the first important croquis construction in one `self.play(...)` unless a future case proves that simultaneous motion is pedagogically necessary.

## V3 defect that created this rule

Phase 04 moved to `phi=36°`, `theta=-58°` and immediately drew wall/column traces. The geometry was technically correct but visually remained a 3D oblique drawing. V4 replaces that transition with PLAN_2D and adds an explicit settling pause.
