# Physics 9 — Velocity from Position–Time Graphs

Complete classroom workshop in English for Grade 9 Physics. It consolidates the rule that velocity is the slope of an `x–t` graph and then constructs the corresponding `v–t` graph interval by interval.

## Workshop sequence

1. use two points to calculate `Δx` and `Δt`;
2. interpret positive, zero and negative slopes;
3. compare speeds using line steepness;
4. calculate the velocities of a piecewise `x–t` graph;
5. construct its matching `v–t` graph;
6. pause for two student problems and reveal worked solutions;
7. distinguish segment velocity from whole-trip average velocity;
8. finish with a reusable five-step recipe and exit check.

## Included PDFs

- `Physics9_Position_Time_Velocity_Workshop.pdf`: 11-page student workshop with six problems and answer key.
- `Physics9_Velocity_Time_Displacement_Companion.pdf`: 8-page companion for the previous velocity–time/area-as-displacement lesson, including Achilles and the tortoise.

The PDF builder source is included. The audited workflow reconstructs the exact verified PDF bytes and checks both SHA-256 hashes before packaging.

## Render target

- ManimCE 0.20.1
- Scene: `Physics9PositionTimeVelocityWorkshop`
- Source: `src/position_time_velocity_workshop.py`
- Final: 1920×1080, 30 fps, H.264, yuv420p

## Required commands

```bash
LESSON_TIME_SCALE=0.08 manim -pql position_time_velocity_workshop.py Physics9PositionTimeVelocityWorkshop --format=mp4 --disable_caching
LESSON_TIME_SCALE=1.35 manim -pqh position_time_velocity_workshop.py Physics9PositionTimeVelocityWorkshop --format=mp4 --disable_caching
```

## QA definition

The project is final only after syntax validation, literal PQL, literal PQH, PDF checksum verification, FFprobe verification, full FFmpeg decode, a dense 48-frame audit and SHA-256 generation all pass.

