# Physics 9 — 2027 Q1 Week 3 (1–5 February)

**Authoritative source:** Physics_9_2027_P1.docx, table 2. Week 3 is **Unit Conversion and Significant Figures**, not kinematics or 2026 Quarter 3 content.

- Class 1 (Conversions and dimensional consistency): length, mass, time, speed; explicit unit factors and correct cancellation; incorrect conversion analysis.
- Class 2 (Significant figures and precision): instrument scale resolution, count significant digits, rounding; compare reported measurements 2 m, 2.0 m and 2.00 m.
- Pedagogy: step-by-step worked examples, guided error analysis, partner review.
- Class dates are not assigned to specific days in the document; they take place during **Monday 1 to Friday 5 February 2027**. No national holiday occurs that week. Local school timetable not supplied, so no day-by-group claims.
- Week 4 (8–12 Feb) is reserved for vernier calipers, micrometers and uncertainty mini-lab. These are explicitly excluded from these Week 3 videos.

## Visual style

Uses **the same CanonicalCADPhysics base** as the fully rendered Physics 9 V5 video: real IJR PNG shield, institutional cover, CAD 2D figures, blue/green/red semantics, numbered HUD, TeX/MathTex, controlled explanation pauses and 16:9 Full HD output.

## Examples that must remain numerically correct

- 1.25 m = 125 cm, 125 cm × (1 m / 100 cm) = 1.25 m.
- 0.75 kg = 750 g; 3 min = 180 s.
- 72 km/h = 20 m/s, using 1000 m/km and h/3600 s.
- 72 km/h × 1000 m/km = 72,000 m/h, **not** 72,000 m/s.
- Exercise: 3.6 km = 3600 m; 90 min = 1.5 h; 54 km/h = 15 m/s.
- 2 m, 2.0 m, 2.00 m imply respectively 1, 2 and 3 significant figures, with reporting places 1 m, 0.1 m, 0.01 m.
- 0.00450 contains 3 significant figures; 1.020 contains 4.
- 4.736 m rounded to 3 significant figures = 4.74 m.
- 0.00520 contains 3 significant figures; 6.284 m rounded to 3 = 6.28 m.

## Build and deliver

Python: `week03_physics9_cad.py`. Scene names: `Physics9W03_Conversions` and `Physics9W03_SignificantFigures`.

CI must run complete `-pql` for both lessons, then `-pqh` for both; validate 1920×1080 30fps H.264 yuv420p, full decode, inspect contact sheets, and commit the verified MP4s in `published_renders/` under the Week 3 branch. The workflow artifact also preserves 18 sampled Full HD frames and SHA-256 hashes.

Instructional examples are illustrative and should not be passed off as measurements collected from pupils.
