# ManimCE PQH Project Package Standard

**Version:** 1.1  
**Effective date:** 2026-08-24  
**Reference environment:** Manim Community Edition 0.20.1  
**Default final format:** 1920x1080, 30 fps, H.264, yuv420p, MP4

## 1. Purpose

This protocol extends the existing ManimCE PQH workflow. A final ManimCE delivery is no longer considered complete when only an MP4 is produced. Every final project must be delivered as a reproducible `.zip` package containing the rendered video, exact source code, storyboard, project style/dependencies, render/QA evidence, and reproduction instructions.

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
12. Build the mandatory project ZIP described below.
13. Deliver the ZIP as the primary artifact. The MP4 may also be exposed separately for convenience.

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
├── qa/
│   ├── VIDEO_TECHNICAL.tsv
│   ├── SHA256SUMS.txt
│   ├── full_decode.log
│   ├── render_pql.log
│   ├── render_pqh.log                    # when available
│   └── audit_frames/
├── protocol/
│   └── PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD.md
└── workflow/                              # recommended for GitHub-rendered projects
    └── <workflow>.yml
```

Assets required by the scene must be included under `assets/` with project-relative paths.

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

## 7. Technical acceptance

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

## 8. Visual QA acceptance

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

## 9. README requirements

The root README inside every package must state:

- project title and version;
- ManimCE version;
- scene class and source file;
- storyboard file;
- exact PQL and PQH commands;
- final technical specifications;
- MP4 SHA-256;
- package directory map;
- concise reproduction instructions;
- QA status and notable design decisions.

## 10. Naming convention

Recommended final package name:

```text
<Project_Name>_<VERSION>_FINAL_PQH_PROJECT.zip
```

Recommended final video name:

```text
<Project_Name>_<VERSION>_FINAL_pqh.mp4
```

Avoid ambiguous names such as `final2`, `new`, or `last`.

## 11. GitHub Actions artifact rule

The workflow artifact must include, at minimum:

- final PQH MP4;
- exact scene source;
- exact style/helper source used for the render;
- storyboard;
- `VIDEO_TECHNICAL.tsv`;
- `SHA256SUMS.txt`;
- `full_decode.log`;
- audit frames;
- PQL log;
- this package protocol or a versioned equivalent.

Whenever practical, the workflow should construct the final project directory and upload the complete package as one artifact.

## 12. Definition of done

A ManimCE project is DONE only when:

- storyboard and source match;
- PQL passes;
- PQH passes;
- technical QA passes;
- full decode passes;
- visual audit passes;
- exact sources are preserved;
- final SHA is recorded;
- the complete project ZIP exists and is downloadable.

The ZIP is the canonical final delivery from this protocol version onward.
