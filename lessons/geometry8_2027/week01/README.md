# Geometry 8 • 2027 • Quarter 1 • Week 1 (19–22 January)

## Curricular grounding (source versus adaptation)

**Inspected source:** Instituto Jorge Robledo, `malla curricular - geometría 8° (2026).docx`, Period I. Its opening axes are "Conceptos y definiciones básicas de la geometría" and "Conjuntos y diagramas lógicos"; later axes explicitly cover rectas/planos, regla/compás, ángulos and parallel/transversal line relationships.

The current accessible sources **do not provide an individual 2027 weekly Geometry planner assigning exactly these topics to Class 1 and Class 2**. This is a transparent **instructional adaptation**, not a verbatim 2027 class schedule. The Week 1 window of January 19–22, 2027 is inherited from the 2027 school planner discussed in the project; exact group-specific meeting days are not claimed.

### Two proposed video scenes

1. `Geometry8W01_Foundations`: geometry in real life; point as location; difference between line, ray and segment; 0D/1D/2D/3D; geometric floor plan; guided identification exercises. This is an introductory vocabulary lesson, not the later detailed lines/planes unit.
2. `Geometry8W01_Sets`: grouping geometric objects by explicit criteria; logical A/B Venn diagrams; blue triangle in both sets, green triangle in triangles set only, blue square in blue set only, gray square in neither; intersection, union, inclusion-exclusion and discussion questions.

**Not in this week:** compass constructions, angle measurements/addition, parallel and transversal lines, triangle/Pythagoras, surface areas.

## Visual identity and reproducibility

ManimCE 0.20.1, Docker, `-pql` → `-pqh`. Both scenes use the same `Week03Base`/canonical House-CAD technical presentation proven in Physics 9: **authentic IJR PNG**, white background, blue selected geometry, green valid result, fixed numbered HUD, Tex/MathTex, 1920×1080 30 FPS and stepwise pauses. Text presentation is English like the established 2027 class planners.

Source: `lessons/geometry8_2027/week01/geometry8_week01_cad.py`.

If you have a more detailed `Geometry_8_Class_Planner_Weeks_01-04_2027.docx`, it should replace the instructional split where it differs before the videos are used as official lesson-planner evidence.

## QA gate

CI compiles the source and validates the original crest, renders both full scenes at `-pql` and `-pqh`, checks H.264 1920×1080 30 fps yuv420p, performs complete FFmpeg decode, extracts nine real frames per video, builds two contact sheets and records SHA-256. MP4 direct links are published only after these tests succeed.
