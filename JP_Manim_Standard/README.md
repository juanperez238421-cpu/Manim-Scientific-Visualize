# JP Manim Classroom Standard

Professional, reusable **Manim Community Edition** standard for classroom and technical animations. The package consolidates the visual language used in the JP classroom series and an auditable render pipeline for previews, final `-pqh`/`-qh` output, technical verification and GitHub Actions delivery.

## Design contract

- 16:9 logical canvas.
- White background.
- Black `Text`, `Tex` and `MathTex` with neutral gray hierarchy.
- Persistent numbered section headers and subtitles.
- Safe content bounds before animation.
- Reusable figure, formula, note, table, split-layout and process-map helpers.
- Controlled camera focus.
- Centralized pedagogical timing.
- Numerical assertions before render.
- Project-relative assets only.

## Why this standard is faster than the legacy workflow

The visual module controls **layout**, not pixel resolution. This means `-ql` can truly render a low-resolution preview. Final resolution/FPS are enforced by the render wrapper. Manim's animation cache is enabled by default and reused; `--disable_caching` is reserved for debugging, while `--flush_cache` is an explicit clean-render operation.

## Quick start

```bash
python -m pip install -e .
cp templates/class_template.py lesson.py
python tools/check_style.py lesson.py
python tools/render_standard.py lesson.py ClassroomTemplate --mode preview
python tools/render_standard.py lesson.py ClassroomTemplate --mode final
```

Local final rendering uses `-pqh`; CI/headless rendering uses `-qh` because preview-opening flags are not supported inside the official Docker environment.

## Repository layout

```text
src/jp_manim_standard/           # modular canonical visual library
  theme.py / core.py / panels.py / tables.py / equations.py / scene.py
templates/class_template.py      # full lesson template
examples/smoke_test.py           # minimal CI render
tools/check_style.py             # static contract checker
tools/render_standard.py         # local render + verify + package pipeline
tools/verify_video.py            # standalone video acceptance gate
docs/VISUAL_STANDARD.md          # visual and pedagogical rules
docs/RENDER_PROTOCOL.md          # reproducible render protocol
.github/workflows/               # CI + manual audited render
manim.cfg                        # final delivery defaults
```

## Version policy

This standard pins **ManimCE 0.20.1** for reproducibility. Upgrade only through a dedicated compatibility PR that renders the smoke test and at least one representative 2D, table-heavy and 3D lesson.

## Delivery acceptance

A final video is accepted only when source validation, style QA, Manim render, MP4 discovery, `ffprobe`, decode test, SHA-256 and QA-frame extraction all succeed. Visual review remains mandatory for pedagogy and overlap/orientation checks.
