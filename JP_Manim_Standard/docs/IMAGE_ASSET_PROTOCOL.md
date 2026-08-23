# Generated Image Assets → ManimCE Protocol

## Goal
Use an image-generation model (for example, Image 2 / a future image-generation service) to create **visual objects**, then integrate them into JP Manim Standard scenes without baking pedagogy into pixels.

## Asset contract
1. Generate the object with **no text, no equations, no arrows, no labels**.
2. Prefer transparent PNG when the object can be isolated.
3. Use at least 1024 px on the long side; 1536 px is preferred for classroom Full HD scenes.
4. Keep 8–12% transparent safe padding around the object.
5. Use the JP neutral palette unless the lesson explicitly requires semantic color.
6. Store a JSON sidecar with id, purpose, source prompt/model, canvas size and intended Manim usage.
7. Use Manim `Text`, `MathTex`, `Arrow`, `Angle`, `Brace`, etc. for all instructional overlays.
8. Scale down in Manim; do not upscale low-resolution assets.
9. Perform a `-ql` smoke render before final `-pqh` / `-qh`.
10. Final output must pass the existing JP Manim video QA protocol.

## Recommended repository layout

```text
assets/
  generated/
    physics/
    geometry/
    statistics/
    cad/
    generic/
```

Each image should have a matching JSON sidecar:

```text
inclined_plane_block_v1.png
inclined_plane_block_v1.json
```

## Example
See `examples/image_asset_demo.py`.
