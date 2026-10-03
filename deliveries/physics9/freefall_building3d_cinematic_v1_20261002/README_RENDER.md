# Physics 9 — Free Fall Building 3D Cinematic V1

## Pedagogical objective

Explain free fall as a physical phenomenon before introducing equations.

Narrative:

1. Build a 20 m urban building in 3D, floor by floor.
2. Place the sphere on the roof and identify the force model.
3. Release the sphere with one live state controlling position, velocity and HUD.
4. Freeze equal-time positions and expose the quadratic displacement pattern.
5. Apply the established croquis protocol: 3D model → stable facade view → mathematical extraction.
6. Derive \(a_y=-g\), \(v_y=v_0-gt\), \(y=y_0+v_0t-\frac12gt^2\).
7. Re-run the fall synchronized with the live \(v(t)\) graph.
8. Reconstruct Galileo's inclined-plane measurement strategy in 3D.
9. Linearize \(s\) against \(t^2\).
10. Close with one constant-acceleration structure.

## Numerical example

- building height: 20.0 m
- g: 9.81 m/s²
- released from rest
- impact time: 2.02 s
- impact velocity: -19.81 m/s

## Render protocol

ManimCE 0.20.1.

Mandatory pipeline:

\`\`\`text
py_compile
→ PQL full timeline
→ PQM visual gate
→ literal PQH 1920×1080 / 30 fps
→ H.264 yuv420p
→ full FFmpeg decode
→ distributed visual-frame QA
→ SHA-256
\`\`\`

Scene:

\`\`\`text
Physics9FreeFallBuilding3DCinematic
\`\`\`

Local test:

\`\`\`bash
manim -pql physics9_freefall_building3d_cinematic_v1.py Physics9FreeFallBuilding3DCinematic --disable_caching
\`\`\`

Final:

\`\`\`bash
manim -pqh physics9_freefall_building3d_cinematic_v1.py Physics9FreeFallBuilding3DCinematic --disable_caching
\`\`\`
