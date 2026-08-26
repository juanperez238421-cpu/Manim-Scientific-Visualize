# Autodesk Inventor — Miscellaneous Tools · House / Sweep / Loft / Revolve visual grammar

This package rebuilds the eight miscellaneous Inventor operations using the same classroom language established by the approved House Extrusion, Barrido/Sweep, Solevación/Loft and Revolución/Revolve lessons.

## Canonical visual rules

- Full HD 1920×1080, 30 fps, white background.
- Black typography and construction lines with restrained neutral grays.
- Large notebook-friendly text; no dense fake-software UI covering the model.
- Every feature begins from its geometric inputs before the 3D result exists.
- Orthographic camera while drawing sketches/reference geometry.
- 3D camera only after the defining geometry is explicit.
- Continuous feature-formation animation where possible.
- Final slow orbit only after the feature is complete.
- Each operation is one independent Python file and one independent final video.

## Eight dedicated lessons

1. `01_fillet_redondeo.py` — **EDGE → RADIUS → TANGENCY → FILLETED SOLID**
2. `02_chamfer_chaflan.py` — **EDGE → DISTANCE → ANGLE → BEVELED SOLID**
3. `03_mirror_simetria.py` — **SOURCE FEATURE → MIRROR PLANE → REFLECTION → SYMMETRIC MODEL**
4. `04_rib_nervio.py` — **OPEN SKETCH → THICKNESS → EXTENT → STRUCTURAL RIB**
5. `05_emboss_repujado.py` — **FACE → CLOSED SKETCH → DEPTH → EMBOSSED FEATURE**
6. `06_coil_bobina.py` — **PROFILE → AXIS → PITCH → REVOLUTIONS → HELIX**
7. `07_rectangular_pattern_lineal.py` — **SEED → DIRECTION → SPACING → QUANTITY → PATTERN**
8. `08_circular_pattern.py` — **SEED → AXIS → ANGLE → QUANTITY → CIRCULAR PATTERN**

## Pedagogical sequence used in each video

1. Opening: compact geometric mental model.
2. Core idea: what changes geometrically and why.
3. Sketch/reference geometry in orthographic view.
4. Dimensions/parameters before the command.
5. Return to 3D and animate the operation.
6. Engineering check / professional habit.
7. Final orbit and one-line synthesis.

## Render protocol

The GitHub Actions workflow performs, for every lesson:

- Python compile check.
- literal ManimCE 0.20.1 Docker PQL smoke render.
- literal ManimCE 0.20.1 Docker PQH render.
- ffprobe verification: 1920×1080, 30 fps, H.264, yuv420p.
- full FFmpeg decode test.
- QA control sheet.
- SHA-256 checksum.
- individual artifact containing video + source + shared style + QA evidence.

The final package job downloads all eight verified artifacts, concatenates the eight PQH videos into one master class video, and creates one ZIP containing all source code, individual videos, QA evidence and the master compilation.
