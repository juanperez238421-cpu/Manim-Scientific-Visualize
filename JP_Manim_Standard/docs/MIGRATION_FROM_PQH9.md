# Migration from PQH(9) + EXACT_RENDER_USED(1)

The v1.0 standard preserves the classroom visual contract while separating responsibilities that were previously coupled.

## Preserved

- 16:9 logical classroom canvas.
- White background and black/neutral-gray hierarchy.
- Persistent numbered headers and subtitles.
- Formula, note, figure, table and process-map helpers.
- Safe-layout assertions and controlled camera focus.
- Centralized pedagogical timing through `LESSON_TIME_SCALE`.
- Numeric validation before render.
- MP4 verification, decode check, SHA-256 and QA frames.

## Improved

1. **Render geometry is decoupled from visual geometry.** Pixel width, height and FPS are no longer hard-coded inside the style module, so `-ql` is a true fast preview.
2. **Headless final render uses `-qh`.** `-pqh` remains the desktop command; Docker/CI does not fake an unsupported preview-opening action.
3. **Caching is enabled by default.** `--flush_cache` is explicit and `--disable_caching` is diagnostic-only.
4. **The monolithic style file is modular.** Theme, core behavior, panels, tables, equations, validators and scene classes can evolve independently.
5. **CI cost is split by purpose.** Pull requests run static QA + low-quality smoke render; expensive 1080p renders are manual or release-driven.
6. **Final video properties are executable acceptance gates.** 1920x1080, 30 fps, H.264, yuv420p, positive duration and full FFmpeg decode are checked.
7. **Reproducibility is explicit.** ManimCE is pinned and a default random seed is recorded.
