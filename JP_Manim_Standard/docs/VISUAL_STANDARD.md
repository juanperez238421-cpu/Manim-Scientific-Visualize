# Visual Standard v1.0

## 1. Canvas and hierarchy

The canonical logical canvas is 16:9 (`frame_width=16`, `frame_height=9`) with white background. Render resolution is deliberately external to the style module so preview quality flags remain effective.

Typography hierarchy:

- section title: 34 pt equivalent, bold;
- subtitle: 20–21;
- panel title: 24–26, bold;
- body: 22–30;
- equations: normally 38–46;
- labels: large enough to remain readable at 1080p delivery.

Use black for primary content and neutral grays for hierarchy. Colored emphasis is opt-in and must be pedagogically justified.

## 2. Safe layout

Use the library's `fit`, `fit_content_zone`, `assert_within_frame` and `assert_content_safe` helpers. Do not rely on visual luck. The default safe width is 14.75 logical units and the usable teaching zone excludes the persistent header.

## 3. Pedagogical sequencing

Preferred scene order:

1. opening and objective;
2. vocabulary / data;
3. visual model;
4. equation development one causal step at a time;
5. worked example;
6. check / interpretation;
7. reproducible method map;
8. closing takeaway.

Do not reveal a complete derivation at once when the learning objective depends on understanding intermediate reasoning.

## 4. Integrated figures and mathematics

When a figure and an equation explain the same idea, keep both visible using `figure_panel`, `formula_panel` and `split_layout`. Highlight only the object currently being discussed. Camera focus may temporarily hide the header but must restore the scene state.

## 5. Tables

Use `build_table` so cells, rows and columns remain independently addressable. Animate rows or relevant cells rather than fading in a monolithic screenshot.

## 6. Assets

Assets must be project-relative and validated before render. Never commit personal absolute paths. Raster assets should be sized close to their display resolution; do not feed unnecessarily large 8K images into a 1080p scene.

## 7. Performance rules

- prefer vector primitives and grouped transforms over hundreds of independent mobjects;
- avoid per-frame Python work when an updater can be simplified or precomputed;
- cache expensive numerical preprocessing outside `construct()` when practical;
- use `ValueTracker`/updaters only while needed and remove them afterward;
- keep preview mode genuinely low resolution;
- keep Manim caching enabled during iteration;
- use `--flush_cache` only for a deliberate clean run.

## 8. Reproducibility

Every displayed numeric claim should be asserted in `validate_lesson_data()`. Randomized scenes must use a fixed seed. Final deliverables include the exact source, render metadata and SHA-256.
