# Physics 9 V4 — Typography + Safe Layout Contract

## Scope

This revision preserves the existing JP Classroom visual identity and the existing ManimCE render protocol. It changes the quality gate for text, formulas, panels, headers and margins.

## 1. Canvas and safe frame

- Final canvas: 1920 × 1080, 16:9, 30 fps.
- Background: white.
- Global JP safe horizontal bounds: x = -7.30 to +7.30.
- Global JP safe vertical bounds: y = -4.10 to +4.10.
- Teaching content must remain below the persistent header content boundary.
- A layout is rejected if it only fits by pushing text against the video edge.

## 2. Typography floors

The following are hard floors for projector-readable classroom material:

| Role | Preferred | Minimum |
|---|---:|---:|
| Opening title | 50 | 44 |
| Section title | 34 | 30 |
| Section subtitle | 22 | 21 |
| Main body text | 26 | 23 |
| Panel title | 27 | 25 |
| Panel body | 24 | 23 |
| Axis labels | 23+ | 22 |
| Graph tick / secondary label | 20–22 | 18 |
| Main formula | 42+ | 29 effective minimum |
| Live numerical HUD | 26 | 24 |

No teaching-critical prose may use graph-tick typography.

## 3. Wrapping instead of shrinking

Long prose uses `text_block()`.

Priority:
1. keep requested font size;
2. wrap to an additional line;
3. reduce only to the role-specific minimum;
4. if it still does not fit, fail the render and redesign the layout.

The library must never silently compress a paragraph until it becomes unreadable.

## 4. Headers

- Section titles are intentionally short.
- Explanatory detail belongs in the subtitle.
- Header titles must fit on one line at >= 30.
- Subtitles may use two lines at >= 21.
- The subtitle cannot intrude into the teaching-content zone.

## 5. Formula panels

- Main formulas should remain 40–54 whenever possible.
- A formula panel can scale only within a controlled range.
- If a formula would fall below the effective minimum, it must be split into a derivation stack or multiple panels.
- No long equation is allowed to be rescued by extreme scaling.

## 6. Cards and explanatory panels

- One dominant focus panel at a time.
- Panel title >= 25.
- Panel body >= 23.
- Statements wrap inside the panel instead of extending beyond it.
- Numerical explanation and graph geometry must not compete in the same small region.

## 7. Dynamic scenes

- Moving objects, vectors, graphs and HUDs share a common physical state.
- Dynamic updater families are frozen before section FadeOut.
- This avoids the ManimCE family-length interpolation failure found in V3 PQH.

## 8. QA

Every final render must pass:

1. Python compile.
2. JP style QA.
3. typography-source QA.
4. full-timeline PQL.
5. PQM visual gate.
6. literal PQH.
7. 1920 × 1080 verification.
8. 30 fps verification.
9. H.264 / yuv420p verification.
10. full sequential decode.
11. distributed QA contact sheet.
12. SHA-256.

## 9. V4 pedagogical typography changes

The long V3 section headers were shortened, while their explanatory meaning remains in the subtitle.

The smallest V3 labels were enlarged:
- 17 px-equivalent ruler labels -> 22;
- 18 time labels -> 22;
- 19 zero / statement labels -> 22–23+;
- 20 graph labels -> 23;
- 20–22 panel titles/bodies -> 23–26;
- live state values -> 26.

The goal is not simply “bigger text”. The goal is a consistent information hierarchy that remains readable from the back of a classroom without violating safe margins.
