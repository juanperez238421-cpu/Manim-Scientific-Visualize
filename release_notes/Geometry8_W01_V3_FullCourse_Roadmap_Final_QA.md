# Geometry 8 · Week 01 Class 01 · V3 Full-Course Roadmap · Final QA

## Delivery verdict
**PASS** — Final ManimCE 0.20.1 PQL preview, 1080p PQH, technical decode, source-qualified curriculum and 16 real-frame visual audit. This deliverable **updates only Geometry8 Week01 Class01**; the accepted Week01 Class02 V2 remains unchanged.

### Verified final MP4
`Geometry8_2027_Week01_V3_Class01_FULL_COURSE_ROADMAP_FINAL_pqh.mp4`
- URL: https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-w01-v3-full-course-roadmap/published_renders/Geometry8_2027_Week01_V3_Class01_FULL_COURSE_ROADMAP_FINAL_pqh.mp4
- Duration: **362.630404 seconds** (6 min 02.63 sec)
- Bytes: **15,550,404**
- Video stream: **H.264**, 1920×1080, **30/1 fps**, **yuv420p**
- SHA-256: `52a59ad96edbc9964c226ea3e97600831f48b0da0b9e27d71c857cf15606a559`
- Verified successful workflow: https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/runs/44214922632

## 1 — Authoritative curriculum sources and provenance

**Complete course preview comes from the original Instituto Jorge Robledo _malla curricular - geometría 8° (2026).docx_:**

- Period I — elementary geometric definitions; sets/logical diagrams; lines, planes and their relationships; straightedge/compass constructions; angles (definition, elements, measurement and types), angle-addition postulate, parallel/perpendicular/transversal lines and notable angles from parallel lines.
- Period II — triangle definition, types and notable lines; circle definition, elements and interior angles; congruence and similarity of triangles; proportionality and Thales' theorem; geometric mean and Pythagorean theorem.
- Period III — perimeter and area of plane figures; simple and complex shaded regions; volumes of Pythagorean/Platonic solids; surface area of solids.

**Exact first four weeks of 2027 come from user-supplied `Geometry_8_2027_P1.docx`:**

| Week | Verified dates | Topic |
|---|---|---|
| 01 | 19–22 January 2027 | Foundations of Euclidean Geometry: geometric objects and sets/logical diagrams |
| 02 | 25–29 January 2027 | Lines, planes, spatial relationships; intersecting/parallel/perpendicular/coincident |
| 03 | 1–5 February 2027 | Straightedge, ruler and compass constructions |
| 04 | 8–12 February 2027 | Angle elements, classification, measurement |

**Source limitation:** the original supplied 2027 planner covers only Weeks 1–4. The three-period syllabus displayed at the beginning is **a course preview from the 2026 curriculum**, **not** a claim that later 2027 dates have been fixed. The video visibly distinguishes this. Week 1 Class 01 retains its exact 2027 teaching sequence after the introductory roadmap.

## 2 — Animated structure retained in the institutional CAD format

1. Original institutional cover with genuine IJR PNG, no vector re-illustration.
2. 3-period technical roadmap: continuous path-following timeline graphics.
3. Period I complete topic overview and animated angle/sets/transversal previews.
4. Period II complete topic overview, transforming similar right triangles, animated circle radius and geometrically correct scaled 3:4:5 Pythagorean triangle.
5. Period III complete topic overview, adjustable area model, shaded decomposition and animated axonometric solid faces.
6. Confirmed 2027 Week 1–4 timeline with source-specific dates and topics.
7. All original Class 01 V2 explanations: course induction and notebook conventions, points, line/ray/segment endpoint semantics, plane, notation and counterexamples, partner exercise and summary.

No Week 2–4 procedure is taught early; the illustrations are clearly previews.

## 3 — QA fixes across the two V3 attempts

- Replaced unescaped TeX `&` heading characters, as required by the legacy CAD TeX rendering.
- Updated CI's inherited-method assertions to validate the **new** V3 scene and its original V2 superclass.
- **First successful binary inspection** exposed date/topic collisions in the four-week timeline; the date and text columns were separated.
- Resized and enlarged the Period I set circles so the **entire** blue triangle lies within the common intersection lens.
- **Reran both complete PQL and full PQH** after these visual corrections; second (current) version passed.

## 4 — Final reproducible verification

- Python syntax, curricular section names and authentic school raster PNG: **PASS**.
- Complete ManimCE `-pql` scene: **PASS**.
- Complete ManimCE `-pqh` 1920×1080, 30 fps: **PASS**.
- FFprobe H.264/yuv420p specification: **PASS**.
- Full FFmpeg video-stream decode: **PASS**.
- Automated integrity of 16 full-HD sampled PNG frames: **PASS**.
- **Manual review of 4×4 contact sheet:** authentic crest; period summaries; separated dates and topics; no obvious clipping of sampled figures or captions. Some samples are in the middle of `Write`/construction animations, not final-state content. A sample audit does **not** guarantee zero issues in every video frame.

### Inspectable evidence
- Real contact sheet: https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-w01-v3-full-course-roadmap/published_renders/Geometry8_2027_Week01_V3_Class01_contact.jpg
- Video metadata: https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-w01-v3-full-course-roadmap/published_renders/Geometry8_2027_Week01_V3_QA.tsv
- SHA-256 check: https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-w01-v3-full-course-roadmap/published_renders/Geometry8_2027_Week01_V3_SHA256SUMS.txt
- Source: https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/blob/geometry8-2027-w01-v3-full-course-roadmap/lessons/geometry8_2027/week01/geometry8_week01_cad_v3_roadmap.py
- Original Class02 V2 remains: https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-w01-v3-full-course-roadmap/published_renders/Geometry8_2027_Week01_V2_Class02_Sets_MOTION_FINAL_pqh.mp4
