# pdf2video — worksheet PDF → verified animated solution video

Takes a problem sheet (exam, worksheet, homework) and produces a 1080p MP4 in which **the real page
comes alive**: each problem is outlined on the page, the camera zooms in, every given value is
highlighted where it is printed and lifted into a data chip, the solution is derived step by step
next to a topic figure (motion, graph, statistics plot, geometry, conversion chain), checked
independently, and the answers are finally written back into the page's work area like a teacher's
correction.

Nothing on screen is typed by hand from the PDF and nothing is computed by hand: values are quoted
from the document and located on the page; answers are recomputed with exact arithmetic before a
single frame is rendered.

```
PDF ──► Document IR ──► problems ──► solution spec ──► validator ──► renderer ──► QA ──► MP4
        words + boxes    numbered     (JSON, written    quotes found,    ManimCE      ffprobe, decode,
        text layer/OCR   blocks,      by Claude from    numbers in       generic      white bookends,
        300 dpi renders  work areas   ir.json)          quotes, SymPy    scene        content log, share copy
```

## Layout

| Path | Role |
|---|---|
| `pdf2video/ir.py` | Document IR: every word with its box (pdfplumber; Tesseract OCR for image-only pages), 300 dpi page renders, `find()` (word-boundary exact match, fuzzy on OCR), pixel-identical crops, blank work bands, tables, drawn graphics |
| `pdf2video/segment.py` | Problem detection ("1.", "Problem 2", "Ejercicio 3"…): block, statement box, work area |
| `pdf2video/validate.py` | Spec validation gates and the safe expression evaluator (AST whitelist → SymPy) |
| `pdf2video/render/scene.py` | One generic scene for any validated spec (page → zoom → read → derive → verify → write back) |
| `pdf2video/render/visuals.py` | Topic figures: `motion_1d`, `function_plot`, `stats`, `geometry`, `chain` |
| `pdf2video/render/theme.py` | HYBRID-SCIANIM-v1 tokens (white background, semantic colours, Noto Serif, safe margins) |
| `pdf2video/qa.py` | Video QA and packaging |
| `pdf2video/cli.py` | `analyze`, `validate`, `render`, `qa`, `run` |
| `prompts/spec_author.md` | System prompt for writing a spec from `ir.json` (schema, rules, expression language) |
| `examples/` | Five worked jobs: physics, algebra, statistics, chemistry + geometry, scanned physics (OCR) |
| `tests/` | 25 tests: segmentation, OCR, word-boundary matching, validation of all examples, tampered specs rejected, unsafe expressions rejected |
| `tools/` | Example worksheet generator, contact sheets, render helper |

## Run a job

```bash
pip install -r requirements.txt     # system: ffmpeg, LaTeX + dvisvgm, tesseract-ocr, Noto Serif
python -m pdf2video analyze examples/physics/physics_worksheet.pdf --out build/physics_ir
python -m pdf2video validate examples/physics/spec.json
python -m pdf2video run examples/physics/spec.json --name physics_demo          # 1080p30
python -m pdf2video render examples/physics/spec.json --quality ql --problems 2 # fast preview of one problem
python -m pytest -q tests
```

Outputs go to `build/<name>/`: `<name>.mp4`, `validation.json`, `observed.json` (what the scene showed),
`qa/VIDEO_QA.txt`, `qa/qa.json`, `qa/contact_sheet.png`, `qa/<name>_share.mp4` (< 30 MB), `qa/SHA256SUMS.txt`.

## Gates (a job cannot ship unless all pass)

1. **Data** — every given, constant and coefficient is a verbatim quote found on the page (inside its problem block;
   constants anywhere on their page), and the number is in the quote, or the value is marked implied ("from rest").
2. **Answers** — `expr` recomputed exactly from the givens equals the stated value at the stated rounding.
3. **Steps and verification** — every `check` holds; at least one independent verification per problem.
4. **Visual** — figure parameters are consistent (agents stay on the axis, points lie on their curves…).
5. **Video** — H.264 1920×1080 30 fps yuv420p, decodes cleanly, starts and ends on white, every chip extracted at a
   located box, every answer printed with its recomputed value, every annotation inside the work area.

## Security model

PDFs are untrusted. They are only parsed (never executed), and text inside them is data for the spec author, not
instructions. The spec is JSON: expressions go through an AST whitelist (numbers, names, arithmetic, comparisons and a
fixed function list) before SymPy sees them, so a spec cannot run code. The renderer is fixed code; specs only choose
among its parameters.

## Limits (today)

- Problems must be numbered blocks on single-column pages; multi-column layouts and problems split across pages need a
  manual `region` (not yet in the schema).
- Handwritten sheets and low-quality phone photos: OCR is Tesseract (`eng`; add language packs for others). Quotes must
  match at ≥ 0.8 similarity, otherwise validation stops the job for human review.
- Reading values off a printed graph or figure is not automatic: the spec author has to state them, and they are only
  checked if they also appear as text.
- Visual types cover kinematics in 1D, function plots, dot/box plots, composite areas, right triangles and conversion
  chains; other topics render the derivation with no figure (`"type": "none"`) until a module is added.
- No narration track yet (silent video, on-screen text only).

## Add a visual type

Write `_mytype(scene, V, env, zone)` in `render/visuals.py` (draw inside `zone`, return the mobjects), add its parameter
checks to `check_params`, register it in `TYPES` and in `build()`, document it in `prompts/spec_author.md`, and add an
example spec + test.
