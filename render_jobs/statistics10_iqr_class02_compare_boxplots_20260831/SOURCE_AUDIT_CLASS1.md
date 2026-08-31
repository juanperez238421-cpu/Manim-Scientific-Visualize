# Class 1 forensic source audit - Statistics 10 IQR / Boxplot

## GitHub lineage reviewed

The direct predecessor is the audited Statistics 10 Week 1 rerender branch / PR lineage:

- PR #95: **Rerender Statistics 10 Week 1 IQR with full PQH protocol package**.
- Source: `render_jobs/statistics10_week1_iqr_boxplot_20260824/main.py`.
- Protocol: `render_jobs/statistics10_week1_iqr_boxplot_20260824/RENDER_PROTOCOL.md`.
- Workflow: `.github/workflows/render_statistics10_week1_iqr_boxplot_20260824.yml`.

The Class 1 source visibly establishes the sequence `order -> quartiles -> IQR -> fences -> boxplot -> interpretation -> comparison`, validates the `2,3,4,5,6,7,8,20` example, and renders with a literal PQL gate followed by literal PQH and ffprobe/full-decode verification.

## Current canonical classroom style reviewed

The current `jp_classroom_style.py` API was audited before authoring this continuation. The new lesson reuses `JPMathClassroomScene`, persistent `set_header`, `clear_stage`, formula/note panels, process maps, safe-frame assertions, timing scale, and the 1920x1080/30fps monochrome classroom configuration.

The shared library is vendored unchanged inside this isolated render job rather than overwriting any canonical repository-wide helper.

## Availability note

Files named `T3-1.pdf`, `T3-2.pdf`, `T3 -1(3).mp4`, `T3-2(2).mp4`, `Glossary IQR(1).png`, `StepsIQR(2).png`, and the curriculum DOCX are not present in the active GitHub render branch used for this execution. Their instructional requirements are represented by the supplied Class 2 specification and the verified Class 1 GitHub source lineage above. No unsupported claim is made that those absent binaries were opened in this run.

## Non-negotiable continuity decisions

1. Keep the Class 1 quartile convention.
2. Formalize `1.5*IQR` fences now.
3. Explicitly distinguish fences from whisker endpoints.
4. Use real non-outlier observations as whisker endpoints.
5. Keep outliers as separate points.
6. Compare plots only on the same numerical scale.
7. Finish every numeric calculation with an interpretation sentence.
8. Preview percentiles only at the end; do not turn Class 2 into the percentile lesson.
