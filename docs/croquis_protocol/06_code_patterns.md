# 06 — Code Patterns

These patterns are intentionally small. They are extracted from repeated behavior in the House case rather than designed as a general framework in advance.

## Enter plan croquis

```python
def enter_plan_croquis(self, run_time=1.5, zoom=None, settle=None):
    self.move_camera(
        phi=self.PLAN_2D_PHI,
        theta=self.PLAN_2D_THETA,
        zoom=self.PLAN_2D_ZOOM if zoom is None else zoom,
        run_time=run_time,
    )
    self.wait(self.CAMERA_SETTLE_PAUSE if settle is None else settle)
```

## Enter front-face croquis

```python
def enter_front_face_croquis(self, run_time=1.5, zoom=None, settle=None):
    self.move_camera(
        phi=self.FRONT_2D_PHI,
        theta=self.FRONT_2D_THETA,
        zoom=self.FRONT_2D_ZOOM if zoom is None else zoom,
        run_time=run_time,
    )
    self.wait(self.CAMERA_SETTLE_PAUSE if settle is None else settle)
```

## Leave croquis before depth

```python
def return_model_view(self, phi, theta, zoom, run_time=1.5, settle=0.30):
    self.move_camera(phi=phi, theta=theta, zoom=zoom, run_time=run_time)
    if settle > 0:
        self.wait(settle)
```

## Construction sequencing

```python
self.play(Create(primary_profile), run_time=...)
self.wait(self.CONSTRUCTION_PAUSE)
self.play(Create(secondary_geometry), run_time=...)
self.wait(self.READING_PAUSE)
```

## Face-profile → cutter depth

```python
self.enter_front_face_croquis(...)
self.play(Create(profile), ...)
self.wait(self.READING_PAUSE)
self.return_model_view(...)
self.play(FadeIn(cutter), ...)
self.play(cutter.animate.shift(...), ...)
```

This pattern preserves visual continuity: the 2D profile remains the cause of the later 3D cutting volume.

## Boolean simulation note

The House scene does not use a CAD boolean kernel. Door/window removal is represented by replacing the original front wall with segmented post-cut geometry. This is acceptable for explanatory animation when the replacement exactly matches the intended opening and the cutter visually explains the operation.
