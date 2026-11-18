# Geometry 8 / 2027 Quarter 1 / Week 01 — V2 deep QA and improved motion

## Authoritative documents

1. **2027 official course planner:** user-uploaded `Geometry_8_2027_P1.docx`, table 1, Grade 8, Quarter 1, **19 January – 22 January 2027**.
2. **Instituto Jorge Robledo malla curricular - geometría 8° (2026).docx**: Period I thematic axes begin with basic definitions and sets/logical diagrams. The 2027 course planner provides the actual **class-by-class day-to-day pedagogical activities**.

### Source-aligned class coverage

| Exact 2027 Week 01 planner requirement | V1 issue | V2 animation or instructional check |
|---|---|---|
| Class 01: course induction and notebook / drawing conventions | Missing | Full diagram modeled on ruled notebook, labels/date and drawing checks |
| Point: definition, naming and visual model | Had dots but little motion | Large, continuously moved named point; dot explicitly a graphic symbol, zero-size mathematical point |
| Line, ray and segment | Three static samples | Large animated strokes with correct direction tips and A/B names, analytical endpoint counts |
| **Plane** | Insufficient / not distinguished | Expanded parallelogram representing a region of an infinite plane, noncollinear points and alpha name |
| Accurate notation, written explanation | Mostly plain English | `AB` overline, ray and double-arrow math notation plus paired construction |
| Class 02: sets and two-circle logical diagrams | V1 circles small and figures appear in place | Two **actual circles**, four comparatively large filled shapes, animated assignment to A-only / both / B-only / neither |
| Class 02: **sort by dimensions** | Only Class 01 showed 0D–3D | Opening physical sort in Class 02 as required by the 2027 planner, with 0D/1D/2D/3D dimensional justification |
| Explain membership, intersection and why objects fall in each region | Too static | Figural emphasis, mathematical membership, analytically constructed intersection lens, highlighted union and no-double-count rule |
| Projected readability and time for discussion | Figures used small portion of 16:9 | Enlarged technical drawings, large TeX and strokewidths, slower transformations, explicit reading/discussion pauses |

### No premature content
- Week 02 (25–29 Jan): intersecting, parallel, perpendicular, coincident line/plane relations.
- Week 03 (1–5 Feb): straightedge/compass constructions.
- Week 04 (8–12 Feb): angles, vertex, degrees, classification, protractor.
These stay out of Week 01 V2.

## Rendering protocol

ManimCE 0.20.1 Docker, source `geometry8_week01_cad_v2.py`, two independent classes:
`Geometry8W01_FoundationsV2`, `Geometry8W01_LogicalSetsV2`.

The validated IJR institutional PNG `assets/ijr_original.png` remains unmodified. The V2 inherits the identical institutional CAD **House Extrusion** cover, fixed HUD and footer semantic legend, with bigger drawing geometry and continuous mathematical motion.

Full pipeline: `python -m py_compile` and PNG header → complete `-pql` renders → full `-pqh` 1920×1080 30fps → FFprobe H264/yuv420p → whole-stream decode → **16 real full-HD sample frames per video**, inspected contact sheets, SHA-256 ledger, direct GitHub-published MP4s on a dedicated V2 branch.

Visual QA is a **sampled visual evaluation**. Full video decodability does not establish universally zero overlapping frames; sampled slides are checked and issues corrected before final signoff. The V1 files remain available for comparison.

## Testable mathematical invariants

- POINT = 0D mathematical location; LINE = extends in two directions with no endpoints; RAY = one endpoint + one direction; SEGMENT = two endpoints; PLANE = ideal flat 2D object extending without bound.
- A/B notation should match drawn points, and visible boundaries should not be mistakenly described as true mathematical line/plane endpoints.
- Sets: A = all triangles, B = all blue figures. Green triangle = A only, blue triangle = A∩B, blue square = B only, gray square = neither.
- `|A|=2`, `|B|=2`, `|A∩B|=1`, `|A∪B|=3`.
- Drawn 3D cube on screen is a 2D drawing **representing** a 3D object.

## Files

- `geometry8_week01_cad_v2.py`
- `qa_geometry8_week01_v2.py`
- `.github/workflows/geometry8_2027_week01_v2_motion.yml`

No dates for specific class-by-group timetable were asserted; the planner gives a week window and two ordered classes only.
