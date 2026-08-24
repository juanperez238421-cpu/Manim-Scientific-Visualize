# Physics 9 — Velocity–Time Graph and Area as Displacement

Complete English ManimCE lesson aligned with Week 2 of the Grade 9 third-period plan (24–28 August 2026).

## Lesson sequence

1. consolidate the Achilles–tortoise physical meeting;
2. represent the meeting as an intersection on an `x–t` graph;
3. read velocity from slope;
4. transfer constant velocities to a `v–t` graph;
5. calculate displacement as signed area;
6. reconcile both racers at the same meeting position;
7. solve a piecewise example;
8. distinguish displacement from distance;
9. complete a notebook recipe and exit ticket.

## Render target

- ManimCE 0.20.1
- Scene: `Physics9VelocityTimeDisplacement`
- Source: `src/velocity_time_displacement_lesson.py`
- Final: 1920×1080, 30 fps, H.264, yuv420p

## Required commands

```bash
LESSON_TIME_SCALE=0.08 manim -pql velocity_time_displacement_lesson.py Physics9VelocityTimeDisplacement --format=mp4 --disable_caching
LESSON_TIME_SCALE=1.0 manim -pqh velocity_time_displacement_lesson.py Physics9VelocityTimeDisplacement --format=mp4 --disable_caching
```

## QA definition

The project is final only after syntax validation, literal PQL, literal PQH, ffprobe verification, full FFmpeg decode, dense frame audit and SHA-256 generation all pass.

Technical evidence and the final MP4 are populated in `qa/` and `render/` by the audited workflow.
