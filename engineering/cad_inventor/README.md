# Inventor-style 2D Sketch → 3D Volume

A true Manim Community Edition `ThreeDScene` showing how a constrained planar sketch becomes a parametric three-dimensional solid by extrusion.

## Scene

- `InventorSketchToVolume3D`: complete teaching animation.
- `InventorExtrusionSmokeTest`: short 3D CI validation scene.

## Technical features

- ManimCE 0.20.1.
- Real three-dimensional camera transitions and ambient orbit.
- `add_fixed_in_frame_mobjects` for the Inventor-style interface.
- `ValueTracker` + `always_redraw` for continuous extrusion depth.
- Custom arbitrary-polygon prism generation with top, bottom and side faces.
- Parametric holes, dimensions, constraints, feature history and CFD handoff.
- 1920 × 1080, 30 fps, H.264 MP4 delivery target.

## Local render

```bash
python -m py_compile engineering/cad_inventor/inventor_sketch_to_volume_3d.py
manim -pql engineering/cad_inventor/inventor_sketch_to_volume_3d.py InventorExtrusionSmokeTest --disable_caching
manim -pqh engineering/cad_inventor/inventor_sketch_to_volume_3d.py InventorSketchToVolume3D --format=mp4 --disable_caching
```

## Docker render

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" \
  -w /manim \
  manimcommunity/manim:v0.20.1 \
  manim -qh engineering/cad_inventor/inventor_sketch_to_volume_3d.py \
  InventorSketchToVolume3D --format=mp4 --disable_caching
```
