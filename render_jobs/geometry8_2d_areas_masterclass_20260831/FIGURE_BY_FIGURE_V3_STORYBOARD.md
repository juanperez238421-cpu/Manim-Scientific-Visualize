# Geometry 8 — Area of 2D Figures — Figure-by-Figure V3

## Why V3

The current `Geometry8Areas2DMasterclassFinalQA` is strong as a period-wide area masterclass: it establishes area vs perimeter, square units, transformation arguments, composite/shaded regions, scaling and applications. However, it is not yet a one-to-one animated version of the 10-figure formula guide.

The V3 objective is therefore narrower and more explicit: **every figure receives its own complete micro-lesson** in the same repeated sequence:

> CONSTRUCT → PARTS → DERIVE → EXAMPLE → CHECK SQUARE UNITS

No figure is introduced only as a formula card.

## Formula-guide alignment

| # | Figure | Required parts | Area relation | V3 construction / derivation | Worked example |
|---|---|---|---|---|---|
| 1 | Square | side `s` | `A=s²` | Build four equal perpendicular sides; connect to rectangle `A=bh` with `b=h=s` | `s=5 cm → 25 cm²` |
| 2 | Rectangle | base `b`, height `h` | `A=bh` | Build base, perpendicular height and opposite sides; connect rows × columns to `b×h` | `8×3 → 24 cm²` |
| 3 | Triangle | base `b`, perpendicular height `h` | `A=bh/2` | Draw altitude and 90° mark; duplicate triangle to form a parallelogram | `b=10, h=6 → 30 cm²` |
| 4 | Parallelogram | base `b`, perpendicular height `h` | `A=bh` | Cut a triangular piece and translate it without rotation to form a rectangle | `b=7, h=4 → 28 cm²` |
| 5 | Trapezoid | major base `B`, minor base `b`, height `h` | `A=(B+b)h/2` | Duplicate/rotate a congruent trapezoid to form a parallelogram of base `B+b` | `B=10, b=6, h=4 → 32 cm²` |
| 6 | Rhombus | diagonals `D`, `d` | `A=Dd/2` | Draw perpendicular diagonals; split into four right triangles | `D=12, d=8 → 48 cm²` |
| 7 | Circle | center, radius `r`, diameter `d=2r` | `A=πr²` | Generate circle from rotating radius; sector split → almost-rectangle with base `πr`, height `r` | `r=4 → 16π ≈ 50.27 cm²` |
| 8 | Regular polygon | perimeter `P`, apothem `a` | `A=Pa/2` | Connect center to vertices; sum congruent triangle areas `½sa` and replace `ns` by `P` | `P=30, a=4 → 60 cm²` |
| 9 | Semicircle | radius `r`, diameter `d` | `A=πr²/2` | Cut a full circle through a diameter; retain one of two congruent halves | `r=6 → 18π ≈ 56.55 cm²` |
| 10 | Quarter circle / quadrant | two perpendicular radii `r` | `A=πr²/4` | Draw two perpendicular radii; isolate one of four congruent quarters | `r=8 → 16π ≈ 50.27 cm²` |

## Presentation architecture

1. Opening — explain the repeated four-beat lesson architecture.
2. Area vs perimeter — retain the audited V2 boundary/interior animation.
3. Square units — retain the audited V2 row-aware 1×1 grid animation.
4. Square.
5. Rectangle.
6. Triangle.
7. Parallelogram.
8. Trapezoid.
9. Rhombus.
10. Circle.
11. Regular polygon.
12. Semicircle.
13. Quarter circle.
14. Complete 10-formula atlas.
15. Final six-step solving method.

## Visual rules

- 1920×1080, 30 fps, white background.
- Black / neutral-gray hierarchy; no decorative color dependency.
- Large projector-safe text.
- Native Manim geometry only; no external image assets required.
- Every `h` is shown as a **perpendicular** distance, never as a slanted side.
- Trapezoid notation matches the supplied guide: `B`, `b`, `h`.
- Rhombus notation matches the supplied guide: `D`, `d`.
- Quarter circle is labeled `QUARTER CIRCLE (QUADRANT)` to connect both terms.
- Formula appears only after the geometric relationship has been animated.
- A worked example always shows: given values → formula → substitution → numerical result → square-unit check.

## Senior-QA acceptance gates

- `python -m py_compile` passes.
- Literal accelerated `-pql` full-timeline run passes.
- No clipped text, no header collision, no labels outside safe frame.
- Construction motions preserve geometry (translate rigid pieces; rotate congruent copies; avoid polygon morph artifacts).
- Every numeric result is asserted in `validate_lesson_data()`.
- Literal `-pqh` final render in ManimCE 0.20.1.
- 1920×1080 / 30 fps / H.264 / yuv420p.
- Full FFmpeg decode plus dense distributed frame/contact-sheet audit.

## Render targets

Preview:

```bash
LESSON_TIME_SCALE=0.05 manim -pql Geometry8_2D_Areas_FigureByFigure_V3.py Geometry8Areas2DFigureByFigureV3 --disable_caching
```

Final:

```bash
LESSON_TIME_SCALE=1.0 manim -pqh Geometry8_2D_Areas_FigureByFigure_V3.py Geometry8Areas2DFigureByFigureV3 --disable_caching
```
