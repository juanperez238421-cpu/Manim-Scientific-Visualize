# PROTOCOL — ManimCE PQH Senior Render + Direct GitHub Delivery

**Status:** CANONICAL / REQUIRED  
**Protocol ID:** `MANIMCE-PQH-DIRECT-GITHUB-v1`  
**Effective:** 2026-09-01  
**Repository:** `juanperez238421-cpu/Manim-Scientific-Visualize`

## 1. Purpose

This protocol is the mandatory final-delivery standard for every ManimCE video render produced for this project.

The render is **not considered delivered** merely because GitHub Actions rendered successfully or because an Actions artifact ZIP exists. Final delivery is complete only after the validated MP4 binary has been published into the GitHub repository and a direct `raw.githubusercontent.com` URL to the `.mp4` has been verified.

## 2. Non-negotiable final result

For every final ManimCE render intended for download:

1. Render the final scene in **PQH / high quality**.
2. Run technical and visual QA.
3. Compute and record SHA-256.
4. Preserve the workflow artifact for traceability.
5. Publish the **real MP4 binary** to `published_renders/` in GitHub.
6. Verify that GitHub reports the committed file with the expected byte size.
7. Return the direct raw GitHub MP4 URL to the user.

### Required delivery form

```text
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/published_renders/<file>.mp4
```

### Forbidden as the only final delivery

- ChatGPT sandbox-only links.
- GitHub Actions artifact ZIP links.
- A `.zip` containing the MP4 when the user requested the rendered video.
- GitHub blob preview links without a direct raw/download alternative.
- Local/container paths.
- Claims that the render is complete before the direct GitHub MP4 is actually published and verified.

## 3. Canonical pipeline

### Gate A — Source and content QA

Before final rendering:

- Run Python syntax/compile checks.
- Verify ManimCE imports and scene class names.
- Validate equations, labels, numerical examples, dimensions, units and instructional sequence.
- Check geometry/transformation correctness.
- Check text hierarchy, readable font size, safe margins and overlap risks.
- Preserve the approved instructional content unless the requested revision explicitly changes it.

### Gate B — Full-timeline smoke render

Run a complete low/preview-quality timeline render before PQH when practical.

Purpose:

- Detect missing assets.
- Detect LaTeX failures.
- Detect scene exceptions.
- Detect malformed transformations.
- Confirm that the full timeline reaches the final scene.

A short isolated scene test does **not** replace a full-timeline smoke render for a senior/final delivery.

### Gate C — Final PQH render

Default target unless a task explicitly requires another format:

- Container: MP4
- Video codec: H.264
- Pixel format: `yuv420p`
- Resolution: `1920x1080`
- Frame rate: approximately `30 fps`
- ManimCE quality mode: `-pqh`

Use a pinned ManimCE version in GitHub Actions for reproducibility.

### Gate D — Technical video QA

The final MP4 must pass all of the following:

- File exists and is non-empty.
- MP4 container can be opened.
- H.264 video stream is present.
- Resolution matches the target.
- Pixel format is compatible with standard players (`yuv420p` for the default protocol).
- Duration is credible for the scene.
- Full video stream can be decoded without fatal decoder errors.
- Frame count / timeline is plausible and reaches the end.
- Final file size is greater than 1 MB for normal full lessons.
- SHA-256 is generated and stored in QA evidence.

Do not reject an otherwise valid Manim render only because a null muxer produces a timestamp bookkeeping warning. Decoder integrity is the authoritative requirement.

### Gate E — Visual senior QA

Create a distributed contact sheet or equivalent sampled-frame audit across the full duration.

At minimum inspect:

- Opening/title frame.
- Every major concept/figure section.
- Worked-example panels.
- Critical transformation midpoints.
- Formula summary/atlas.
- Final method or conclusion frame.

Check for:

- Cropping at all four frame edges.
- Text outside panels.
- Overlaps.
- Tiny typography.
- Misaligned labels/dimensions.
- Incorrect geometry caused by transforms.
- Low-contrast highlighted regions.
- Empty or broken final frames.

The final render must not be called `SENIOR_FINAL` until these checks pass.

## 4. Direct GitHub publication gate

After QA passes, publish the exact validated binary to:

```text
published_renders/<FINAL_FILENAME>.mp4
```

The published file must be **byte-identical** to the QA-approved render. Verify this with SHA-256 before publication.

### Publication requirements

- GitHub workflow permissions: `contents: write`, `actions: read`.
- Download the exact validated artifact from the same render workflow/run.
- Verify the expected SHA-256.
- Commit the binary using the GitHub Git Data API or an equivalent binary-safe GitHub mechanism.
- Use a commit message containing `[skip ci]` when publication itself could retrigger the render workflow.
- Render workflows should also ignore `published_renders/**` where appropriate to prevent loops.
- After commit, query GitHub Contents API and verify the file exists, is type `file`, and has the expected byte size.
- Capture the `download_url` supplied by GitHub.

## 5. Repository file-size gate

GitHub rejects normal repository files at or above its hard per-file limit. Therefore:

- **Protocol target maximum:** `< 95 MiB` per published MP4.
- If the final render exceeds 95 MiB, re-encode with high-quality H.264 settings while preserving instructional legibility and the requested resolution/frame rate.
- Re-run technical QA after any re-encode.
- The re-encoded file becomes the canonical validated binary and receives a new SHA-256.

Never silently reduce educational content simply to satisfy the size gate.

## 6. Naming standard

Recommended final naming pattern:

```text
<Subject>_<Topic>_<Version>_SENIOR_FINAL_pqh.mp4
```

Examples:

```text
Geometry8_2D_Areas_FigureByFigure_V5_SENIOR_FINAL_pqh.mp4
Physics9_Position_Time_Graph_V3_SENIOR_FINAL_pqh.mp4
Statistics10_IQR_Class02_V4_SENIOR_FINAL_pqh.mp4
```

Rules:

- No spaces in final published filenames.
- Preserve the version identifier used in source/workflow/QA files.
- `_pqh` is required for the canonical high-quality deliverable when PQH is the requested render mode.

## 7. Required evidence package

The render workflow should preserve, at minimum:

```text
<FINAL>.mp4
<FINAL>_SHA256SUMS.txt
<FINAL>_VIDEO_QA.txt
<FINAL>_contact_sheet.jpg   # or equivalent visual QA evidence
source/                    # relevant scene/style/workflow source where practical
```

The Actions artifact is retained for audit/history, but it is **not** the user-facing download mechanism.

## 8. Required final response to the user

A final ManimCE delivery response must contain the direct GitHub MP4 download link.

Preferred wording pattern:

```text
Final validated PQH render:
[Download <filename>.mp4 directly from GitHub](https://raw.githubusercontent.com/.../<filename>.mp4)

SHA-256: <hash>
```

Do not substitute a sandbox link when a direct GitHub render is available.

## 9. Definition of Done

A ManimCE render request is **DONE** only when all applicable conditions are true:

- [ ] Source/content QA passed.
- [ ] Full timeline smoke render passed.
- [ ] PQH final render passed.
- [ ] Technical decode QA passed.
- [ ] Visual senior QA passed.
- [ ] SHA-256 recorded.
- [ ] Actions artifact preserved.
- [ ] Exact MP4 binary published under `published_renders/`.
- [ ] GitHub file size/path verified after commit.
- [ ] Direct raw GitHub `.mp4` URL generated.
- [ ] User receives that direct GitHub URL.

If the last three items are not complete, the render must be reported as **rendered but not yet delivered**, never as final delivery.

## 10. Reusable GitHub workflow

The repository provides the canonical reusable publication workflow:

```text
.github/workflows/reusable_manimce_pqh_direct_publish.yml
```

All new ManimCE render workflows should call this publication workflow after the final QA/upload job succeeds.

## 11. Governance

This file is the project-level source of truth for final ManimCE video delivery. New render workflows should follow it by default. A task-specific workflow may add stricter QA gates, but it must not weaken the direct GitHub MP4 delivery requirement unless the user explicitly requests a different delivery method.
