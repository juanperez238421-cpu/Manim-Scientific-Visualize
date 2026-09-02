# ManimCE PQH Project Package Standard

**Version:** 1.2  
**Effective date:** 2026-08-24  
**Reference environment:** Manim Community Edition 0.20.1  
**Default final video format:** 1920x1080, 30 fps, H.264, yuv420p, MP4  
**Mandatory companion document:** PDF lesson/document derived from the accepted final PQH render

## 1. Purpose

This protocol extends the existing ManimCE PQH workflow. A final ManimCE delivery is not complete when only an MP4 is produced. Every final project must be delivered as a reproducible `.zip` package containing the rendered video, exact source code, storyboard, project style/dependencies, a PDF document derived from the final accepted render, render/QA evidence, and reproduction instructions.

The PDF is part of the canonical lesson evidence. It must translate the final video into printable, copy-ready classroom documentation without changing the lesson's mathematics, sequence, terminology, or conceptual conclusions.

## 2. Mandatory workflow

For every project, use this order:

1. Review the user request and existing project/style code.
2. Prepare or update a storyboard before implementing a substantial visual/narrative revision.
3. Implement the scene using the established JP classroom style when applicable.
4. Validate Python syntax and lesson data.
5. Run a literal `-pql` QA render.
6. Correct runtime, LaTeX, framing, overlap, continuity, and timing issues.
7. Run a literal `-pqh` final render from the exact accepted source.
8. Verify the MP4 with `ffprobe`.
9. Fully decode the MP4 with FFmpeg and require an empty error log.
10. Export dense audit frames and visually inspect critical transitions.
11. Calculate SHA-256 for the final MP4.
12. Generate the mandatory PDF document from the **accepted final PQH MP4** and its exact storyboard/source.
13. Render the PDF to page images and visually inspect every page for clipping, overlap, broken glyphs, unreadable equations, or unsafe margins.
14. Record SHA-256 for the final PDF.
15. Build the mandatory project ZIP described below.
16. Deliver the ZIP as the canonical project artifact. The MP4 and PDF may also be exposed separately for convenience.

A project that fails any required gate is not final.

## 3. Mandatory ZIP structure

Each final package must follow this logical structure:

```text
<Project_Name>_PQH_PACKAGE/
├── README.md
├── src/
│   ├── <scene_source>.py
│   └── jp_classroom_style.py            # when used by the render
├── storyboard/
│   └── STORYBOARD.md
├── render/
│   └── <Project_Name>_FINAL_pqh.mp4
├── document/
│   └── <Project_Name>_FINAL_VIDEO_NOTES.pdf
├── qa/
│   ├── VIDEO_TECHNICAL.tsv
│   ├── SHA256SUMS.txt                    # MP4 + PDF + critical source hashes
│   ├── full_decode.log
│   ├── render_pql.log
│   ├── render_pqh.log                    # when available
│   ├── audit_frames/
│   └── pdf_pages/                        # rendered PDF page QA images or contact sheet
├── protocol/
│   └── PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD.md
└── workflow/                              # recommended for GitHub-rendered projects
    └── <workflow>.yml
```

Assets required by the scene must be included under `assets/` with project-relative paths. Source used to build the PDF (`.tex`, `.md`, `.html`, `.docx`, or equivalent) is recommended under `document/source/` when practical.

## 4. Storyboard requirement

For explanatory, educational, diagrammatic, or narrative animations, the storyboard is a required project artifact. It must define:

- pedagogical objective;
- visual continuity strategy;
- scene/act order;
- objects that remain persistent;
- camera/zoom behavior;
- equation progression;
- timing intent;
- transition rules;
- final conceptual takeaway;
- known QA risks such as clipping, overlap, crowding, stale labels, or discontinuous diagrams.

The storyboard must correspond to the rendered source; it is not decorative documentation.

## 5. Source traceability

The package must contain the exact `.py` source used for the final PQH render and every local style/helper file required to reproduce it.

For GitHub Actions renders:

- source reconstruction must be deterministic;
- SHA-256 validation must occur before `-pql`;
- the exact reconstructed source/style used by Manim must be copied into the final artifact;
- do not package a different local copy of a style library if its SHA differs from the rendered version.

The PDF must be generated from the same accepted lesson version. Do not generate a PDF from an older video, an older storyboard, or an unaccepted source revision.

## 6. Render gates

### PQL gate

A literal low-quality runtime test is mandatory:

```bash
manim -pql <scene.py> <SceneClass> --format=mp4 --disable_caching
```

PQL must complete without traceback before PQH.

### PQH gate

The final render uses literal high quality:

```bash
manim -pqh <scene.py> <SceneClass> --format=mp4 --disable_caching
```

For headless Docker/GitHub Actions environments, `xdg-open` may be neutralized while preserving the literal `-pqh` invocation.

## 7. Video technical acceptance

Unless the project explicitly requests another target, final PQH must satisfy:

- width: 1920;
- height: 1080;
- frame rate: 30 fps;
- codec: H.264;
- pixel format: yuv420p;
- MP4 readable by `ffprobe`;
- full FFmpeg decode exits with code 0;
- `full_decode.log` is empty;
- final MP4 SHA-256 is recorded.

## 8. Video visual QA acceptance

Technical green status is necessary but not sufficient. Dense audit frames must be reviewed for:

- no text outside the safe frame;
- no object/text overlap that harms readability;
- no stale labels after a state change;
- no character/object merging at important points;
- no sudden diagram disappearance when continuity is pedagogically important;
- no camera zoom that magnifies labels/ticks into unusable sizes;
- equations remain causally ordered and readable;
- transitions preserve the viewer's spatial mental model;
- conclusion is visually consistent with the state shown immediately before it.

If a defect is found, patch the source and rerender. Do not rename an older render as the new version.

## 9. Mandatory PDF derived from the rendered video

Every accepted PQH lesson must include a PDF document derived from the final rendered video.

### 9.1 Content fidelity

The PDF must:

- follow the same pedagogical order as the accepted video;
- preserve the exact lesson data, equations, terminology, and conclusions;
- use selected frames from the accepted MP4 as visual evidence when helpful;
- rewrite animation-dependent information into static, copy-ready mathematical steps;
- not silently add new concepts, examples, values, or corrections that are absent from the accepted lesson unless the user explicitly requests expansion;
- identify the final physical/mathematical result clearly.

### 9.2 Classroom visual standard

Unless another style is explicitly requested, the PDF must use:

- white background;
- black or neutral typography;
- strong title/section hierarchy;
- LaTeX-quality equations for mathematical content;
- safe printable margins;
- no decorative clutter;
- no clipped text or images;
- no overlapping boxes, equations, or captions;
- page numbers and concise lesson identification;
- copy-ready formulas and short explanatory statements suitable for notebook use.

For math-heavy lessons, LaTeX is the preferred authoring path.

### 9.3 Recommended structure

A typical educational video PDF should contain:

1. title / learning goal;
2. setup and given data;
3. step-by-step derivation of the main result;
4. visual explanation pages using selected render frames;
5. formula/sequence development in the same order as the video;
6. limit/series/derivation steps when present;
7. final synthesis connecting the mathematics to the physical/visual result;
8. final notebook summary with key equations.

The page count should follow the lesson, not an arbitrary target.

### 9.4 PDF QA gate

After generation, the PDF must be rendered to page images using a reliable renderer (for example PDFium or Poppler) and every page must be visually checked.

Acceptance requires:

- no clipped text;
- no formula overflow;
- no broken glyphs or black squares;
- no image/text overlap;
- no unreadably small screenshots;
- no content outside printable margins;
- page sequence matches the video lesson;
- all final equations are mathematically legible;
- final PDF SHA-256 is recorded.

The PDF is not accepted until this render-and-inspect gate passes.

## 10. README requirements

The root README inside every package must state:

- project title and version;
- ManimCE version;
- scene class and source file;
- storyboard file;
- final PDF path;
- exact PQL and PQH commands;
- final video technical specifications;
- MP4 SHA-256;
- PDF SHA-256;
- package directory map;
- concise reproduction instructions;
- QA status and notable design decisions.

## 11. Naming convention

Recommended final package name:

```text
<Project_Name>_<VERSION>_FINAL_PQH_PROJECT.zip
```

Recommended final video name:

```text
<Project_Name>_<VERSION>_FINAL_pqh.mp4
```

Recommended final PDF name:

```text
<Project_Name>_<VERSION>_FINAL_VIDEO_NOTES.pdf
```

Avoid ambiguous names such as `final2`, `new`, or `last`.

## 12. GitHub Actions artifact rule

The workflow artifact must include, at minimum:

- final PQH MP4;
- final PDF derived from that MP4;
- exact scene source;
- exact style/helper source used for the render;
- storyboard;
- `VIDEO_TECHNICAL.tsv`;
- `SHA256SUMS.txt` containing MP4 and PDF hashes;
- `full_decode.log`;
- audit frames;
- PDF page QA renders or a complete contact sheet;
- PQL log;
- this package protocol or a versioned equivalent.

Whenever practical, the workflow should construct the final project directory and upload the complete package as one artifact.

## 13. Definition of done

A ManimCE project is DONE only when:

- storyboard and source match;
- PQL passes;
- PQH passes;
- video technical QA passes;
- full decode passes;
- video visual audit passes;
- exact sources are preserved;
- the PDF is generated from the accepted final video;
- the PDF render-and-inspect QA passes;
- MP4 and PDF SHA-256 values are recorded;
- the complete project ZIP exists and is downloadable.

The ZIP is the canonical final project delivery. The MP4 is the canonical motion artifact, and the PDF is the canonical printable lesson/document artifact.
