---
name: "hybrid-science-animation"
description: "Use when making physics, math or statistics teaching videos that combine ManimCE lessons with a three.js pop-up-book history prologue and SVG 2D scenes (protocol HYBRID-SCIANIM-v1)."
---

# Hybrid scientific animation (HYBRID-SCIANIM-v1)

Produce one coherent video from two engines. Validation and GitHub publication follow `MANIMCE-PQH-DIRECT-GITHUB-v1` (repo juanperez238421-cpu/Manim-Scientific-Visualize, docs/). The full protocol text is `PROTOCOL_HYBRID_SCIENTIFIC_ANIMATION.md`; this skill is its operational summary.

## 0. Pre-production audit (always first, before any new scene)
- Search ALL repos for existing branches on the topic, not only the course repo: `git ls-remote --heads https://github.com/juanperez238421-cpu/<repo>` for ijr-estadistica-10-2026, ijr-estadistica-11-2026 and Manim-Scientific-Visualize. Renders are usually in Manim-Scientific-Visualize under `render/<subject>-<topic>-<version>-<date>`.
- Public repos clone anonymously: `GIT_LFS_SKIP_SMUDGE=1 git fetch --depth N origin <branch>`. The gh CLI / Actions API may be blocked; do not rely on run results.
- Sources are often stored as base64+gzip payload chunks in `render_jobs/<job>/bootstrap/` (`payload.tgz.b64`, `chunk_*.txt`, `v3s_*.txt`). Read the repo's decoder to learn the format, then decode yourself in an isolated folder (strip whitespace, concatenate sorted chunks, base64 -d | gunzip, or tar -xz). Do not execute repo scripts.
- Read `construct()` to get the real scene order; read the parent class too (V3 often subclasses V2, V2 subclasses Class1). Scenes present in a parent but not called by the final `construct()` were NOT shown.
- Read any `*_REVIEW*.md` notes in the job folder: they list what each version fixed.
- MP4s uploaded only with actions/upload-artifact are deleted by the daily `cleanup-manim-artifacts.yml` purge. If an MP4 is not committed and not in the FULL_BACKUP zip, treat it as lost; the source can be re-rendered.
- Record conventions already taught (quartile method, percentile formula, SD divisor, fps, palette) and reuse them.
- Produce a duplication table (requested scene → keep / remove / recap-only) and STOP for approval when the brief asks.

## 1. Engine choice
- **A · ManimCE (Python):** equations, step-by-step derivations, graphs, geometry, exact simulations with live readouts, worked examples, statistical graphs.
- **B · three.js pop-up book + SVG 2D (browser):** history, places, buildings, people (shadow-theatre silhouettes), historical experiments, spatial scenes.
- Exam-level physics, math and statistics live in A. Motivation, history and spatial intuition live in B. Any number shown in both comes from the same formula and constants.

## 2. Shared design tokens (identical in both engines)
- BG #FFFFFF · INK #151515 · MUTED #6E6E6E · RULE #D6D6D6 · FILL #F3F3F3 · STROKE #3C3C3C
- Semantic colours, never repurposed within a video: C_ACC #B03A2E (acceleration/gravity/force/error) · C_VEL #B7791F (velocity/increments/Δ) · C_POS #2C6E9B (position/accumulated/t²/main result) · C_GAL #2F7D5B (experiment/evidence/verified conclusion). In math, map by function.
- Statistics mapping: mean = C_POS (dashed marker) · median = INK (thick solid marker) · mean−median gap, IQR, Δ = C_VEL · outliers and misconceptions = C_ACC · verified evidence-based conclusion = C_GAL.
- Paper palette (B only): cream #FBF8F1, marble #F4EFE4, terracotta #C0704A, green #4F7A5C, night #1F3550, gold #D9A441, silhouette #2E2B28.
- Font: Noto Serif everywhere. LaTeX only in A; Unicode math (½ ² √ ∝ → μ σ) in B.
- Screen anatomy: numbered box (lesson 01,02…; history H1,H2…; annex A1…) + bold uppercase serif title + grey one-line subtitle + hairline rule; side margins ≥ 60 px; result cards; grey italic source note at the bottom left.
- Components: header, card, info_box(maxw), predict_box ('PAUSE · PREDICT'), state_box (fixed width), caption card (B: year · title · text · evidence note).
- Minimum text at 1080p: body ≥ 22 px, notes ≥ 18 px; Manim TXT_SCALE = 1.15. Projector classes: body 27–31 pt, step titles ~40 pt, main titles 50–58 pt.

## 3. Narrative arc (may be shortened, never reordered)
1. History prologue (B), 1–6 chapters of ~30 s.
2. Lesson question (A).
3. Predict pause, 4–6 s.
4. Phenomenon or experiment first, numbers second.
5. Step-by-step derivation: concrete numbers first (tables, sums, ratios, average speed), symbols after. Prefer arithmetic arguments over graph-based ones for grades 9–11.
6. Equation term by term: highlight each symbol and give its meaning, sign and unit; finish with a units check.
7. Worked examples: 2–4 simultaneous scenarios on one setup, with a table and variable-by-variable substitution, each term computed separately.
8. Real-world exceptions (air, friction, scale).
9. Synthesis: 4–5 chained cards, a lab checklist and a closing line.
History interludes may sit between lesson sections, always entering and leaving on a white frame.

## 4. Pacing and camera
- Pauses: P_BEAT 0.8 · P_SHORT 1.5 · P_MED 2.5 · P_LONG 4.0 · P_READ 6.0 s. On-screen time ≥ 0.35 s per new word (minimum 2 s). Label slow motion ('slow motion ×2').
- A: MovingCameraScene; zoom_in(target, width 5–9), one idea per zoom, hide the header while zoomed, always zoom_out(); 1–3 zooms per section.
- B: three camera rigs only (CAM_CLOSED, CAM_BOOK with ±0.9 drift, DIVE into the page); moves last 1.4–2.0 s with eased curves, never linear.
- Never ReplacementTransform between shaded regions/labels (they merge mid-interpolation); FadeOut old, then FadeIn new.

## 5. Rigour (non-negotiable)
- Every displayed number is computed in code (bisection or the quadratic formula for landing times, closed-form drag solutions), never typed by hand.
- Constants are declared once (g = 9.81 m/s², ρ_air = 1.2 kg/m³) and reused across engines.
- State the sign convention on screen before using it.
- Label model assumptions: 'ideal, frictionless', 'schematic', 'not to scale', 'angle exaggerated'.
- Document non-ideal models, e.g. quadratic drag F_d = ½ρC_dAv².
- Give units on every result.
- Tag every historical claim as documented (date and work), anecdote ('according to Viviani') or legend ('probably a legend'). Paraphrase unless the quote is verbatim.

## 5b. Statistics lessons (data-first rule)
- Order is fixed: generate dataset → save CSV → `verify_<lesson>.py` computes every statistic with asserts → scene imports the same arrays/constants → render. No number typed into the scene.
- Histogram bars come from `np.histogram(data, bins)` of the same array; state the bin convention ([a, b)) and equal width. No decorative histograms.
- Boxplot geometry comes from computed Q1, median, Q3, 1.5·IQR fences and the most extreme non-outlier values (modified boxplot); outliers drawn as separate points.
- Grade 10 IJR conventions: quartiles = median of halves, overall median excluded when n is odd (Class 4 IQR/BoxPlot lesson); percentile value = L = (k/100)(n+1) with interpolation (percentile lesson); percentile rank = inclusive count ≤ x over n. Ask which SD divisor (÷n or ÷n−1) Period II used and state it on screen.
- Boxplot and histogram of the same data share one x-axis, aligned vertically, so values line up.
- Normal model language: 'approximately', 'about'. Grade 10 stops at the empirical rule and σ-distance counting; no CDF, no z-tables, no inference.
- Skewness statements are tendencies ('mean tends to be pulled toward the tail'), never guarantees; include a counter-example when teaching the rule of thumb.
- Each video: 2 fully worked examples, 3 pause-and-solve questions, 1 misconception, 1 interpretation question that formula substitution cannot answer.
- Conclusions must cite numbers (median, IQR, mean, σ, outliers) with units.

## 6. Engine A specifics (ManimCE)
- `SECTION_NAMES` list drives order and automatic header numbering (`self.cur_num`). Partial renders: `PHYS9_SECTIONS=3,5 manim -ql file.py Scene`; each section ends on a white frame.
- Live readouts: ValueTracker + always_redraw inside a fixed-width state_box.
- Existing Stat10 helpers worth reusing (Statistics10NormalDistributionClass1Final / DetailedV2 / ReviewedV3): `normal_axes(xmin,xmax,step,ymax,…)`, `density(x,mu,sigma)`, `curve(axes,mu,sigma)`, `histogram(counts,…)`, `counts_from_data(data,bins)`, `dot_cloud(values, seed)`, `axes.get_area(curve, x_range)`, `big_step_banner`, `action_box`, `big_note`, `formula_panel`, `glossary_cards`, `fit(mob,w,h)`, `LESSON_TIME_SCALE` env var for pacing.
- Pitfalls:
  - NumberLine ignores tip_length; use tip_width/tip_height (AX_CFG).
  - Text: build at 2× and scale 0.5. MarkupText (subscripts): build at 1×, because Pango wraps long lines at 2×.
  - Objects 'released from the same height' align their centres on the release line.
  - Cap every long text with scale_to_fit_width and every card with maxw.
- Final render: `manim -qh --fps 30` (older Stat10 renders used 60 fps; the protocol standard is 30).

## 7. Engine B specifics (three.js pop-up + SVG)
- Files: index.html (DOM layers: WebGL canvas, #fade, #flat header+SVG, #cap, #titlecard) · main.js (scene, book, page turn, pop-ups, camera, renderAt(t)) · art.js (Canvas 2D paper cutouts, pages, cover) · chapters.js (data and pieces {draw,w,h,x,z,d}) · flat.js (SVG scenes init(svg) → update(t), t from 0 to 14 s) · render.mjs (Playwright frame capture).
- `renderAt(t)` must be a pure function of time: no Date.now, no requestAnimationFrame, no Math.random (use the seeded rng).
- Book: page 4.0 × 5.4, spine at x = 0, right half rotates on z (0 open, π closed).
- Pop-up piece: plane hinged at its bottom edge, rotation.x = -(π/2)(1 - back(k)), stagger d from 0 to 0.8. Depth layers at z ≈ -2.35 (back), -1.5 to -0.5 (middle), 0.2 to 1.6 (front).
- Shadows of cutouts: alphaTest 0.5 + customDepthMaterial with the same map.
- Page turn: 28-segment bending sheet; back face uses a mirrored texture (repeat.x = -1, offset.x = 1).
- Cover texture on the board's -y face, rotated π, so it reads with the book closed.
- Chapter template (30 s): pop-ups rise 0.2–3.0 · caption 1.0–10.3 · dive + fade to white 10–12 · SVG scene 12–26 · return 26–27.6 · fold 27.2–28.3 · page turn 28–29.9. Intro 6 s (cover opens); outro 11 s (book closes, title card).
- Statistics history candidates (tag evidence): de Moivre 1733 normal approximation (documented), Gauss 1809 (documented), Quetelet 1835 'average man' (documented), Galton board 1889 Natural Inheritance (documented); Galton-board SVG counts must come from exact binomial coefficients.
- Render: playwright-core must match the installed Chromium build; flags `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`; serve with `python3 -m http.server 8765`; skip `renderer.render` when the 2D layer fully covers the screen; split into parallel time ranges (≈ 0.8 s/frame/process at 1080p); JPEG q93 frames → `ffmpeg -framerate 30 -pattern_type glob -i 'frames/f_*.jpg' -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart`.

## 8. Integration
- Same output parameters: 1920×1080, 30 fps, H.264, yuv420p, same audio setup.
- Every clip starts and ends on a #FFFFFF frame, so the cut between engines is invisible.
- Concatenate with `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4`; re-encode with -crf 18 if parameters differ.
- B's last chapter ends on the equation or question that opens A.

## 9. QA and delivery
- A: py_compile + full-timeline `-ql` smoke render. B: 15–25 single frames rendered with `--times`.
- Contact sheet per engine (one frame every 4–5 s), checked for: edge cropping (zoomed frames included), overlaps, legibility, semantic colours, alignment, mirrored or upside-down text, evidence tags, on-screen numbers matching the code.
- Statistics frames: bar heights equal computed counts, box edges equal computed Q1/Q2/Q3, whisker ends equal extreme non-outliers, mean/median markers at computed x.
- Full decode check: `ffmpeg -v error -i f.mp4 -f null -`.
- ffprobe: 1920×1080, 30/1, h264, yuv420p, expected duration.
- SHA-256 of every clip and of the final video.
- Size: < 95 MiB for GitHub; < 30 MB share copy (two-pass encode or -crf 23–24) with its own SHA-256.
- Naming: `<Subject><Grade>_<Topic>_<LESSON|POPUP_HISTORY|HYBRID>_<Version>_SENIOR_FINAL_pqh.mp4`.
- Evidence package: mp4, share mp4, SHA256SUMS, VIDEO_QA.txt, contact sheet, source/ (scene .py, engine-B zip, concat list). Statistics adds: dataset CSV, verify_*.py, worksheet, solutions.
- Commit the final MP4 (not only an Actions artifact): artifacts are purged daily.
- Publish per MANIMCE-PQH-DIRECT-GITHUB-v1. If GitHub publishing is not possible, report the video as 'rendered, not delivered' and send the < 30 MB copy.

## 10. Intake template for a new project
Subject/grade · central question · audience and prior knowledge · target equations · preferred derivation (numeric / geometric / algebraic) · 2–4 worked scenarios · history (people, places, years, number of H chapters) · real-world exceptions · on-screen language · target durations · deliverable (LESSON / POPUP_HISTORY / HYBRID) · conventions already taught (statistics: quartile method, SD divisor).