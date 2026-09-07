# Geometry 8 Circle V8 FINAL3 → FINAL4 — Human Contact-Sheet QA

FINAL3 already passed compile, literal PQL, literal PQH, H.264 full decode, 1920×1080/30 fps validation and outer-edge safety. A 72-frame contact-sheet review was then performed manually before delivery.

## Remaining visual findings

| Scene | Human QA finding | FINAL4 correction |
|---|---|---|
| Step 01 | `CENTER` and the large italic diameter label `d` visually touch around the circle center. | Keep both font sizes; move `CENTER` farther down-left and `d` down-right. Also replace `TransformMatchingTex` with same-object `Transform` so the equation lifecycle remains deterministic. |
| Step 04 | The large `ROW 1 — RIGHT HALF` / `ROW 2 — LEFT HALF` ownership labels have insufficient air before the first sector. | Keep 31 pt labels; translate the complete row + arc + measurement geometry system 0.42 scene units to the right. |
| Step 07 | The right end of the large `base = P/2 = πr` expression comes too close to the `ONE base = P/2 = πr` conclusion panel. | Keep both large; move the conclusion panel from x=3.85 to x=4.45, preserving safe-frame margin while introducing a visible gap. |

## Acceptance rule

FINAL4 is deliverable only after:

1. complete PQL timeline succeeds;
2. literal `-pqh` succeeds at 1920×1080 / 30 fps;
3. H.264 full decode succeeds with yuv420p;
4. outer-edge clipping scan reports zero failures;
5. dense final contact sheet is generated and manually inspected;
6. Step 01, Step 04 and Step 07 corrected frames are individually inspected at full resolution.
