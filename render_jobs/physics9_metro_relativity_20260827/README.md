# Physics 9 — Metro Relativity · 2D + 3D

Dedicated ManimCE classroom lesson for introducing reference frames, classical relative velocity and the invariance of the speed of light.

## Scene

```text
Physics9MetroRelativity
```

## Source

```text
metro_relativity_lesson.py
```

## Core classroom results

- Metro speed relative to ground: 80 km/h.
- Walker speed relative to metro: 2 km/h in the same direction.
- Walker speed relative to ground: 82 km/h.
- Physical light speed correction: c ≈ 300,000 km/s, not 300,000 km/h.
- Light speed measured in the metro frame: c.
- Light speed measured in the ground frame: c.

## Why the light result is different

For ordinary speeds, the lesson first uses Galilean addition:

```text
u = u' + v
```

For light, the lesson introduces special-relativistic velocity addition:

```text
u = (u' + v) / (1 + u'v/c²)
```

With u' = c, the expression simplifies exactly to u = c.

## Render commands

PQL gate:

```bash
manim -pql metro_relativity_lesson.py Physics9MetroRelativity --format=mp4 --disable_caching
```

Final:

```bash
manim -pqh metro_relativity_lesson.py Physics9MetroRelativity --format=mp4 --disable_caching
```

The GitHub workflow pins ManimCE 0.20.1 and performs the project's standard PQL → PQH → ffprobe → full decode → frame audit → SHA-256 → ZIP pipeline.

## Final delivery name

```text
Physics9_Metro_Relativity_2D3D_FINAL_pqh.mp4
```
