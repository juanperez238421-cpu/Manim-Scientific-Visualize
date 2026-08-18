# 04 — Animation Pacing

The objective is not to make scenes globally slow. Pacing must create time for a specific cognitive action.

## Pause hierarchy

### Micro pause
Typical reference: ~0.4 s.

Use after a note appears or before a new causal action. It separates beats without stopping momentum.

### Construction pause
Typical reference: ~0.7 s.

Use between logically distinct drawing layers such as perimeter → partitions → columns.

### Reading pause
Typical reference: ~1.2 s.

Use after a profile, label, measurement, or completed extrusion result that the viewer must inspect.

### Explanation pause
Typical reference: ~1.5 s.

Use after a complete operation such as a cut, glass insertion, or roof extrusion.

### Camera-settling pause
Typical reference: ~0.75 s.

Mandatory after entering a 2D croquis camera state. The first important technical line must not share temporal attention with camera movement.

### Final observation pause
Typical reference: ~1.9 s.

Use after a complete croquis before leaving drawing mode.

## Pacing anti-patterns found in V3

- Phase 04 had no pause between perimeter, interior traces, and column profiles.
- Exterior walls in phase 06 immediately lost their note after extrusion; the result had little inspection time.
- Door/window profiles were immediately followed by cutter setup without a dedicated profile-reading beat.
- Roof outline was immediately converted into depth from the same oblique camera.

## V4 changes

- separate perimeter / partitions / column-profile construction;
- preserve completed profiles before 3D transition;
- pause after exterior and interior wall extrusion;
- read door/window profile in face-normal 2D before returning to 3D;
- read roof outline in plan 2D before introducing thickness.

## Timing rule

Every `wait()` should be explainable by a semantic category. Anonymous delays are acceptable only during exploratory prototyping; stable scenes should use named timing constants where practical.
