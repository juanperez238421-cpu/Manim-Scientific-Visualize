# Geometry 8 • 2027 Week 01 — CAD videos and sampled QA

## Documentary traceability

**Inspected original curriculum:** `malla curricular - geometría 8° (2026).docx`, Instituto Jorge Robledo, Period I. The first two thematic axes explicitly include (1) basic geometric concepts and definitions, and (2) sets and logical diagrams. The source also lists lines and planes, ruler/compass and angles later in the same period.

**Important limit:** the inspected original is a **2026 period-level curriculum**, not an authenticated 2027 Week-1 class-by-class plan. The division into `Geometry8W01_Foundations` and `Geometry8W01_Sets` is a transparent pedagogical adaptation for the previously discussed 2027 opening week (January 19–22). No timetable assigning the exact two lessons to individual days or groups was provided or inferred.

## Educational implementation

- **Class 1:** point as location, not physical disk; different endpoints for mathematical line/ray/segment; A/B are actually marked on the corresponding object; 0D–3D geometric representations; room-plan sketch; three questions with response pauses.
- **Class 2:** explicit finite universe of four figures. `A` = triangles, `B` = blue figures. The green triangle belongs only to A; the blue triangle to both; the blue square only to B; gray square to neither. This is consistently preserved on each Venn-diagram revisit. Thus `|A|=2`, `|B|=2`, `|A∩B|=1`, `|A∪B|=3`.
- No angle arithmetic, protractor/compass constructions, parallel/transversal theorems, area/perimeter or higher-grade content added to the Week 1 introduction.
- English voice-free texts and user-approved institutional CAD House style with authentic IJR PNG school crest, numbered phase HUD and deliberate time to read/respond.

## Build details and audited outputs

**Successful complete run:** https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/runs/44206432379

| Check | Class 1 | Class 2 |
|---|---|---|
| Filename | Geometry8_2027_Week01_V1_Class01_Foundations_FINAL_pqh.mp4 | Geometry8_2027_Week01_V1_Class02_LogicalSets_FINAL_pqh.mp4 |
| Duration | 144.765690 s | 131.899349 s |
| Bytes | 5,843,153 | 5,055,703 |
| Video format | MP4 / H.264 | MP4 / H.264 |
| Resolution, FPS, pixel format | 1920×1080, 30/1, yuv420p | 1920×1080, 30/1, yuv420p |
| ManimCE PQL/PQH | PASS/PASS | PASS/PASS |
| FFprobe, complete decode | PASS/PASS | PASS/PASS |
| SHA-256 | 705ca75f02949da3df199542042d9a5040d5ae078f192f1becbcff252a640d00 | a522eac5a18bbd727d307cf1bbdf54174e8ee47ce7c40f980780950f4aaa4841 |

### Visual contact-sheet inspection

Manually reviewed nine real Full HD sampled frames from each of the two final videos:

- The authentic PNG crest and correct Geometry 8 — Week 01 2027 label appear on both covers.
- The 16:9 CAD upper-left course label, upper-right numbered HUD, bottom semantic legend and teaching content remain legible and within the canvas at sampled moments.
- Class 1: sample at 44% shows line, ray, segment with A/B dots and labels; the sample at 56% captures an unfinished 0D–3D drawing animation; 68% shows floor-plan construction in progress. These are animated steps, not incomplete exported videos.
- Class 2: Venn labels A/TRIANGLES and B/BLUE now appear; the four objects appear in logically appropriate regions; the sample at 68% confirms the union count equation.
- No persistent clipping or substantial overlap was visible at the inspected stills. **This is sampled inspection, not a mathematical guarantee across every animation frame.**

Contact sheets:
- `published_renders/Geometry8_2027_Week01_V1_Class01_contact.jpg`
- `published_renders/Geometry8_2027_Week01_V1_Class02_contact.jpg`
- `published_renders/Geometry8_2027_Week01_V1_FRAME_METRICS.csv`

## Direct download URLs

- [Class 1 MP4](https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-cad-class01-02/published_renders/Geometry8_2027_Week01_V1_Class01_Foundations_FINAL_pqh.mp4)
- [Class 2 MP4](https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-cad-class01-02/published_renders/Geometry8_2027_Week01_V1_Class02_LogicalSets_FINAL_pqh.mp4)

Rendering is reproducible from `lessons/geometry8_2027/week01/geometry8_week01_cad.py` via the branch-specific GitHub Action and pinned ManimCE 0.20.1 Docker image.
