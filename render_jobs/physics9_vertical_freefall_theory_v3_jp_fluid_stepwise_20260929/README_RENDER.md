# Physics 9 — Vertical Motion + Free Fall V3 JP Fluid Stepwise

This lesson follows the consolidated **JP Classroom ManimCE Standard** and the project render protocol.

## Scene

`Physics9VerticalFreeFallTheoryV3JPFluid`

Source:

`render_jobs/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise_20260929/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise.py`

## Visual contract

- 1920×1080, 16:9, 30 fps.
- White background.
- Black / neutral gray hierarchy.
- Persistent numbered section header.
- One explicit pedagogical step at a time.
- Motion remains continuous inside a physical process.
- Pauses are intentional: read → explain → work → summarize.
- Camera focus is controlled and temporary.
- Numerical claims are asserted before animation.

## Required render order

1. Static compile and JP style QA.
2. Full-timeline `-pql` gate.
3. Medium-quality review render `-pqm`.
4. Literal final `-pqh` render.
5. Normalize delivery to H.264 / yuv420p.
6. `ffprobe` metadata validation.
7. Full sequential FFmpeg decode.
8. Distributed frame extraction and contact sheet.
9. SHA-256 checksum.
10. Persist the exact source, style library, logs and final MP4.

## Docker commands

From repository root:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -e PYTHONPATH=/manim \
  -e LESSON_TIME_SCALE=0.05 \
  -v "$PWD:/manim" -w /manim \
  manimcommunity/manim:v0.20.1 \
  manim -pql \
  render_jobs/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise_20260929/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise.py \
  Physics9VerticalFreeFallTheoryV3JPFluid \
  --format=mp4 --disable_caching
```

Final:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -e PYTHONPATH=/manim \
  -e LESSON_TIME_SCALE=1.0 \
  -v "$PWD:/manim" -w /manim \
  manimcommunity/manim:v0.20.1 \
  manim -pqh \
  render_jobs/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise_20260929/physics9_vertical_freefall_theory_v3_jp_fluid_stepwise.py \
  Physics9VerticalFreeFallTheoryV3JPFluid \
  --fps 30 --format=mp4 --disable_caching
```

The CI workflow neutralizes `xdg-open` so the literal `-pql/-pqm/-pqh` flags remain usable on a headless GitHub runner.
