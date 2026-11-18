# Geometry 8 — 2027 Quarter 1 — first four weeks

The eight-video deliverable follows **the exact uploaded original** `Geometry_8_2027_P1.docx` (dated Week1–4 planner), cross-checked against `malla curricular - geometría 8° (2026)(1).docx`, institutional Period I axes.

## Eight class-by-class videos, in planner order

| Week | Dates | Class 1 | Class 2 |
|---|---|---|---|
| 01 | 19–22 Jan 2027 | Course induction; notebook/drawing conventions; point, line, segment, ray and plane; plus introductory Period I roadmap | Geometric sets and two-circle logical diagrams; sort by dimension and justify membership |
| 02 | 25–29 Jan 2027 | Identify and label intersecting, parallel, perpendicular and coincident arrangements; everyday line/plane models | Draw several spatial configurations; classify and justify; use counterexamples to fix misconceptions |
| 03 | 1–5 Feb 2027 | Marked ruler vs unmarked straightedge; compass setup, given segment and transfer by fixed-radius construction | Perpendicular bisector and parallel/perpendicular configurations, property validation, drawing error |
| 04 | 8–12 Feb 2027 | Angles: vertex, rays, naming and degrees; acute/right/obtuse/straight/reflex by measure | Protractor setup, read degrees, construct specified angle, classify, preview addition as **next** topic |

Specific group-specific class dates are not in the planning source; the week windows are authoritative, the group day is unknown.

**Actual videos already fully verified (reused, not relabelled):**
- Week 01 Class 01 (full Period I animated induction) — `geometry8-2027-w01-v4-period1-curricular-complete/published_renders/Geometry8_2027_Week01_V4_Class01_PERIOD_I_FULL_CURRICULUM_FINAL_pqh.mp4`, original IJR PNG, 493.664 seconds, 1920x1080, 30fps.
- Week 01 Class 02 (sets and logical diagrams) — `geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_Class02_Sets_MOTION_FINAL_pqh.mp4`, 208.499 seconds, Full HD.

**Six NEW real ManimCE scenes** are in `lessons/geometry8_2027/weeks02_04/cad_six_classes.py`. They inherit `Geometry8V2Base`, which loads the genuine PNG and institutional House-Extrusion CAD system, typography, blue sketch/green verification, global HUD, clean 16:9 and pauses. No synthetic logo, placeholders, or slide images.

**Rendering CI**: `.github/workflows/geometry8_2027_w02_w04_six_cad.yml`: Python syntax and logo check, every scene complete PQL→PQH (ManimCE 0.20.1 Docker), H264/1920×1080/30fps/yuv420p FFprobe, whole-video decode, 9 actual 1080p screenshot frames per video (54 total), six real MP4 SHA256s and direct published GitHub links. The pipeline commits the binaries **only on success**.

**Technical caution:** Contact sheets show representative timestamps and are **not** proof that all frames have no transient text collisions.

[Actions workflow](https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/workflows/geometry8_2027_w02_w04_six_cad.yml).
