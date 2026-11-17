# Physics 9 — Quarter 1, Week 1 (2027)

Source: `Physics_9_2027_P1.docx`, IJR Grade 9, week from **19 Jan to 22 Jan 2027**.

## Pedagogical scope

- **Class 1**: physics induction, natural phenomena, evidence-based/testable questions, observation vs explanation, length/mass/time/temperature, base vs derived quantities, physical models.
- **Class 2**: observations to measurements, short length/time activity, estimation, correct quantity/value/unit/instrument records, compare predictions and results.

Both videos are in English and use **animated 2D vector scenes** in the clean white/black technical visual language of the existing House Extrusion 3D ManimCE project. They use the existing IJR physics planner, not copied 2026 kinematics content. Numerical measurements are explicitly labeled as **illustrative examples**, never presented as student results.

## Build

```bash
python -m py_compile lessons/physics9_2027/week01/physics9_2027_week01.py
manim -pql lessons/physics9_2027/week01/physics9_2027_week01.py Physics9Week1Class1
manim -pql lessons/physics9_2027/week01/physics9_2027_week01.py Physics9Week1Class2
manim -pqh lessons/physics9_2027/week01/physics9_2027_week01.py Physics9Week1Class1
manim -pqh lessons/physics9_2027/week01/physics9_2027_week01.py Physics9Week1Class2
```

Official Docker ManimCE image: `manimcommunity/manim:v0.20.1`.

## QA criteria

Source compiles, two `-pql` previews succeed before `-pqh`, MP4s are 1920×1080 / 30 fps / H.264 yuv420p, `ffprobe` and full ffmpeg decode pass. The workflow preserves each source and SHA-256 checksum. Independent classes for maximum reuse and classroom pausing.

## Output

After a successful run, videos are committed under `published_renders/` on this branch and have stable GitHub raw URLs. The workflow creates a ZIP artifact containing code, QA reports, and the two videos.
