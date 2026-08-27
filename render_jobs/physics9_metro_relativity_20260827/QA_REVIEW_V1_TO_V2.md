# Senior QA Review — Physics 9 Metro Relativity V1 → V2

## V1 visual audit

The rendered V1 was reviewed across the full 162.5 s timeline and through distributed representative frames.

### Main problems detected

1. **Human figures were the weakest visual element.** The 2D people read as thin stick figures and the 3D people were too small to carry the narrative. Their visual weight did not match the metro geometry.
2. **Too much information was shown at once.** Several screens combined train, observer, equations, explanatory cards, arrows and persistent subtitles, reducing projector readability.
3. **The 3D metro was visually useful as an establishing device but too wireframe-like for the human-centered explanation.**
4. **The same person did not feel visually continuous from seated observer → walker → lamp source.** This weakened the story.
5. **Text hierarchy was inconsistent.** Important values such as 2 km/h, 82 km/h and c sometimes competed with smaller explanatory text.
6. **The light-speed correction and relativistic law were conceptually correct but arrived inside a dense sequence.** The student had to process too many transitions before the main contrast became clear.
7. **The light pulse was visually dominant in 3D.** The large wireframe sphere could be interpreted as a geometric object rather than a propagating light front.

## QA rubric for V1

- Physics correctness: **9.2 / 10**
- Narrative simplicity: **5.2 / 10**
- Human figure quality: **4.0 / 10**
- Projector readability: **6.0 / 10**
- 2D/3D integration: **6.2 / 10**
- Overall classroom usability: **6.1 / 10**

## V2 corrective strategy

### Human figures
- Remove all tiny 3D human models.
- Use one consistent large 2D pictogram family with head, filled torso, thick arms/legs, visible joints and natural seated/walking poses.
- Animate walking through alternating poses rather than sliding a static stick figure.
- Keep people large enough to be immediately recognizable from the back of a classroom.

### Visual simplification
- Reserve 3D for only two moments: metro establishing shot and light-propagation scene.
- Keep the core reference-frame explanation in a clean 2D side cutaway.
- Reduce the lesson from ten dense stages to seven conceptual sections plus opening.
- Use one dominant result per screen.

### Pedagogical sequence
1. Establish two observers.
2. Inside view → 2 km/h.
3. Outside view → 80 + 2 = 82 km/h.
4. Freeze and compare the two correct answers.
5. Turn on the lamp and correct the unit of c.
6. Show station view of light and introduce the relativistic rule only after the visual contrast is clear.
7. Finish with a compact comparison table and one exit question.

## Acceptance criteria for V2 final render

- PQL gate passes before PQH.
- 1920×1080, 30 fps, H.264, yuv420p.
- Full FFmpeg decode with no errors.
- No human figure smaller than the intended visual scale in the central teaching scenes.
- No 3D human geometry.
- Major result text remains visually dominant.
- No overlap between people, formulas and persistent header.
- Unit correction clearly reads `c ≈ 300 000 km/s`.
- Final comparison clearly shows Metro: 0/80, Person: 2/82, Light: c/c.
- Distributed frame QA contact sheet produced after final render.
