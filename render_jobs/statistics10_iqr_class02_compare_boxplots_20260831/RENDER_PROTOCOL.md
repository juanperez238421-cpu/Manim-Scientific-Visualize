# Statistics 10 IQR Class 2 - PQH render and senior QA protocol

Target: Manim Community Edition 0.20.1.

## Acceptance sequence

1. Preserve the exact Class 1 quartile convention.
2. Compile the lesson and vendored classroom style with `python -m py_compile`.
3. Run the static classroom-style checker.
4. Validate the presence of the primary scene and all required section methods.
5. Pull `manimcommunity/manim:v0.20.1`.
6. Run a literal accelerated `-pql` full-timeline validation render.
7. Run the final literal `-pqh` render with `LESSON_TIME_SCALE=1.0`.
8. Verify final media with `ffprobe`: H.264, 1920x1080, 30 fps, yuv420p.
9. Decode the entire final MP4 with FFmpeg; no decode errors are accepted.
10. Scan every frame at reduced resolution for blank frames, sparse frames and border-heavy/cropping risk.
11. Extract 96 distributed full-resolution audit frames and a contact sheet.
12. Build a 16-page presentation PDF from stable audited render frames.
13. Export a representative PNG cover from the audited frame set.
14. Generate SHA-256 checksums.
15. Package MP4, PDF, PNG, exact source, exact style helper, storyboard, source audit, workflow, logs and QA evidence in a ZIP artifact.
16. Persist the final delivery files back to the dedicated render branch when GitHub permissions allow.

## Literal PQL gate

```bash
LESSON_TIME_SCALE=0.07 manim -pql \
  Statistics10_IQR_Class02_Compare_Boxplots_FINAL.py \
  Statistics10IQRClass02CompareBoxplotsFinal \
  --format=mp4 --disable_caching
```

## Literal final PQH

```bash
LESSON_TIME_SCALE=1.0 manim -pqh \
  Statistics10_IQR_Class02_Compare_Boxplots_FINAL.py \
  Statistics10IQRClass02CompareBoxplotsFinal \
  --format=mp4 --disable_caching
```

## Final filenames

- `Statistics10_IQR_Class02_Compare_Boxplots_FINAL_pqh.mp4`
- `Statistics10_IQR_Class02_Compare_Boxplots_PRESENTATION.pdf`
- `Statistics10_IQR_Class02_Compare_Boxplots_COVER.png`
- `Statistics10_IQR_Class02_Compare_Boxplots_FULL_PACKAGE.zip`
