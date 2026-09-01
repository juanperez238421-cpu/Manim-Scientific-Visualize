# Senior QA — Statistics 10 Module 1

## Mathematical checks
- Single convention only: inclusive linear percentile position r = 1 + (n-1)p.
- Data are ordered before every percentile calculation.
- Linear interpolation appears only when the percentile position is fractional.
- Verified values: P25=64.25, P50=73.5, P75=83.0, P80=85.2, D3=66.5, D7=81.2.
- Q1=P25, Q2=P50, Q3=P75 is the explicit bridge from the prior IQR/boxplot work.
- Percentile value is not presented as identical to percentile rank; that distinction is reserved for Module 2.

## Pedagogical checks
- Sequence follows Meaning -> Visual -> Notation -> Calculation -> Interpretation -> Comparison.
- The lesson does not reteach IQR from zero.
- Every numerical worked example ends with a verbal interpretation.
- Student practice is shown without immediate solutions; the teacher key is separate.
- No z-scores, advanced probability, sampling theory, or unnecessary university-level material appears.

## Visual / render checks
- 1920x1080, 30 fps, white background, projector-scale text.
- Monochrome student-facing content to continue the IQR/boxplot visual language.
- One main idea per screen, persistent numbered headers, separated formula cards and interpretation cards.
- Required pipeline: py_compile -> literal -pql -> literal -pqh -> ffprobe -> full FFmpeg decode -> distributed audit frames -> SHA-256 package.
