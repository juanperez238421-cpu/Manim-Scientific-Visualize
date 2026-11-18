# Physics 9 — 2027, Week 1 — V3 Deep QA Report

## Source and identity
- Week 1 of the uploaded Physics_9_2027_P1.docx (19–22 Jan 2027), Grade 9: Class 1 physics induction, testable questions and physical quantities; Class 2 length/time measurement activity, estimation, and recorded units/instruments.
- Canonical style from House Extrusion 3D V6 source and its CAD Animation Protocol in Manim-Scientific-Visualize.
- The asset is an authentic original PNG, copied byte-identically from the existing IJR Physics 9 repository's laboratorio-planeaciones/assets/logo-ijr.png. Its Git blob SHA is c1ac2d32cb57a1ecab9a18708076ae8e215d42a4. It is an ImageMobject, not a simplified SVG approximation.

## Specific V2 problems and V3 repairs

1. HIGH / Logo identity: V2 used a vector approximation of the school emblem. V3 embeds a valid institutional PNG; Pillow opens/verifies it during CI and the actual render cover was visually inspected.
2. HIGH / Inadequate reading time: V2 micro 0.65 s, reading 1.75 s, explanation 2.35 s, observation 2.80 s. V3 uses 1.20, 3.40, 4.20, and 5.00 seconds, respectively, plus 8-second final wrap-up and classroom-thought holds.
3. MEDIUM / Measurement-table rapid build: V2 showed cells in only 0.20 s. V3 slows each cell to 0.56 s and extends row reading pauses.
4. MEDIUM / Stopwatch physics: V2's rotation was not synchronized with its numerical 3.2 s example. V3 explicitly calibrates a 10 s per-revolution dial and rotates by 3.2/10 of a turn (115.2 degrees).
5. MEDIUM / Ruler fidelity: V2 showed only coarse ticks yet reported 46 cm. V3 draws 51 ticks (0–50 cm with 1-cm steps) and differentiates major 5/10-cm ticks.
6. HIGH / Visual QA completeness: V2 checked technical properties and extracted frames, but did not provide contact sheets. V3 preserves 18 original Full HD PNG frames in its Actions artifact, creates two shareable 3x3 contact sheets and records frame statistics.
7. PQL regression found and repaired during V3: a literal percent symbol in a Tex caption caused DVI-to-SVG compilation failure. The shared LaTeX sanitizer now escapes percent characters and both PQL tests passed.

## Verified video results

| Metric | Class 01 | Class 02 |
|---|---|---|
| V2 duration | 93.698698 s | 108.794141 s |
| V3 duration | 130.366016 s | 176.631706 s |
| Extra presentation time | +36.67 s / +39.1% | +67.84 s / +62.4% |
| Video | MP4 H.264 | MP4 H.264 |
| Video format | 1920x1080; 30 fps; yuv420p | 1920x1080; 30 fps; yuv420p |
| File size | 3,423,967 B | 5,096,454 B |
| Source syntax / PQL / PQH / FFprobe / full decode | PASS | PASS |
| SHA-256 | a65cb5f1529ebb46c558d9b705e647d8d7ed994820637684892e8ddf246447e7 | 6a8ff773fa6afba21cdba6750029d427f035d783f94745c6e9fbe4d0aa6ca51c |

Workflow: https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/runs/44150150458

## Manual storyboard review based on actual rendered frames

Both rendered contact sheets were opened and inspected. In the nine sampled frames per class, the original PNG shield is recognizable, aligned and proportional on the institutional cover. The top-left course identification, numbered top-right HUD, lower semantic legend and caption region are consistently separated. Technical illustrations appear fully on screen, without conspicuous label overlap, crop or collision at the sampled positions. The Class 2 sample at 8% falls inside an intentional incremental-Write transition, accounting for partial header text in that one snapshot. The ruler, stopwatch, measurement-table rows and class exercises are visibly present. The palette remains faithful to the CAD house technical protocol (blue for selected geometry, green for verification, red for unsupported claims and comparison).

Contact sheets:
- published_renders/Physics9_2027_Week01_V3_Class01_contact.jpg
- published_renders/Physics9_2027_Week01_V3_Class02_contact.jpg

Raw video properties: published_renders/Physics9_2027_Week01_V3_QA.tsv
Frame statistics: published_renders/Physics9_2027_Week01_V3_FRAME_METRICS.csv
Checksum file: published_renders/Physics9_2027_Week01_V3_SHA256SUMS.txt

## Acceptance and limits

ACCEPTED FOR CLASSROOM USE. The full files pass technical validation and 18 sampled frames were visually reviewed. This is a sampled visual audit, not a frame-by-frame proof that no overlap can occur anywhere in both videos. No narration or music was added. All numerical measurements are explicitly illustrative examples, not classroom measurements.

Final render files:
- published_renders/Physics9_2027_Week01_V3_Class01_CAD_PNG_FINAL_PQH.mp4
- published_renders/Physics9_2027_Week01_V3_Class02_CAD_PNG_FINAL_PQH.mp4
