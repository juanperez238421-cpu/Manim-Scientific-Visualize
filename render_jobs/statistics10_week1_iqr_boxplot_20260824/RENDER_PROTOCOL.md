# Statistics 10 Week 1 — PQH Render Protocol

Protocol basis: `PROTOCOLO_COMPLETO_RENDER_MANIMCE_PQH` and `protocolo_manimce_docker_render`, using ManimCE 0.20.1.

Acceptance sequence for this rerender:

1. Validate source with `python -m py_compile`.
2. Confirm scene class `Statistics10Week1IQRBoxplot` exists.
3. Run a literal low-quality validation render with `manim -pql`.
4. Run the final literal high-quality render with `manim -pqh` in the official ManimCE Docker image.
5. Verify final MP4 with `ffprobe`: H.264, 1920x1080, 30 fps, yuv420p.
6. Decode the complete MP4 with FFmpeg to detect corruption.
7. Extract 18 evenly distributed audit frames for visual QA.
8. Preserve the exact Python source used to render.
9. Preserve PQL/PQH render logs and decode/ffprobe reports.
10. Generate SHA-256 checksums.
11. Package the final MP4, source, logs, protocol note, checksums and audit frames as one delivery artifact.

Final render command inside Docker:

```bash
manim -pqh render_jobs/statistics10_week1_iqr_boxplot_20260824/main.py Statistics10Week1IQRBoxplot --format=mp4 --disable_caching --media_dir media_pqh
```
