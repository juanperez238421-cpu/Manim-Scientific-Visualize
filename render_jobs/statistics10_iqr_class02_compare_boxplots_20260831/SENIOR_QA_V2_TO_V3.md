# Statistics 10 · IQR Class 02 — Senior QA V2 → V3

## V2 manual senior inspection

The V2 render passed every automated render gate, but a manual 120-frame / full-resolution inspection found two projector-level issues that automated blank/crop detection cannot reliably catch.

### Senior QA score — V2

| Category | Weight | Score | Weighted |
|---|---:|---:|---:|
| Statistical correctness | 25 | 97 | 24.25 |
| Pedagogical sequencing | 20 | 96 | 19.20 |
| Visual hierarchy / projector readability | 15 | 88 | 13.20 |
| Animation / focus guidance | 15 | 93 | 13.95 |
| Pacing / cognitive load | 10 | 90 | 9.00 |
| Classroom usefulness / notebook transfer | 10 | 90 | 9.00 |
| Technical render integrity | 5 | 100 | 5.00 |
| **TOTAL** | **100** |  | **93.60 / 100** |

## Findings requiring V3

1. **Axis-number visibility** — NumberLine tick marks rendered, but the numerical labels were not visibly black on the white classroom background in the audited frames. Quantitative boxplot reading requires a visible scale. V3 forces the entire NumberLine submobject tree to `BLACK_LINE` after construction.
2. **Read-example annotation collision** — `UF = 29.8` and the note `35 is beyond the upper fence` occupied the same visual neighborhood. V3 separates these annotations spatially.
3. **Redundant outlier ring** — V2 drew a second ring around the already-circular outlier mark. V3 highlights the existing outlier with `Circumscribe` instead of creating a duplicate circle.

## V3 acceptance target

- Manual senior QA target: **≥ 97 / 100**.
- Visible numeric labels on every lesson NumberLine.
- No overlap between UF label, outlier note, quartile labels, or boxplot geometry in the read-example scene.
- Literal `-pql` full-timeline validation.
- Literal `-pqh` final render using ManimCE 0.20.1.
- H.264, 1920×1080, 30 fps, yuv420p.
- Complete FFmpeg decode.
- Every-frame blank/sparse/border scan.
- 144 distributed audit frames plus contact sheet.
- Verified 16-page PDF, cover PNG, SHA-256 manifests, and reproducible package.
