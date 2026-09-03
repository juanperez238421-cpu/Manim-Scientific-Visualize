# Sistema diédrico / Método de Monge — research brief for V4 faithful scene

## Purpose
Rebuild the dihedral-system explanation so the animation depicts the actual geometric construction instead of a 2D visual metaphor.

## Sources reviewed

1. ISO 5456-2:1996 — *Technical drawings — Projection methods — Part 2: Orthographic representations*  
   https://www.iso.org/standard/11502.html
   - ISO identifies orthographic representation as the standard technical representation method and specifies first-angle and third-angle methods.

2. ISO 128-3:2022 — *Technical product documentation — General principles of representation — Part 3: Views, sections and cuts*  
   https://www.iso.org/standard/83356.html
   - Current general representation standard; view arrangement is based on orthographic projection according to ISO 5456-2.

3. INTEF — *Sistema diédrico: representación espacial en 2D · Fundamentos y planos de proyección*  
   https://descargas.intef.es/recursos_educativos/RED_ES/04_Bachillerato/1/B_1_057_2025_0974/fundamentos_y_planos_de_proyeccin.html
   - Uses two mutually perpendicular projection planes, horizontal (PH) and vertical (PV), whose intersection is the Línea de Tierra (LT).
   - Orthogonal projections onto the two planes yield the principal views.
   - The horizontal plane is unfolded about LT to place the two projections on one drawing plane.

4. Junta de Andalucía / IES Almadraba — José Vicente Araújo, *Sistema diédrico · Fundamentos*  
   https://blogsaverroes.juntadeandalucia.es/jvaraujo/dt1/geometria-descriptiva/diedrico/fundamentos/
   - Explicitly describes cylindrical orthogonal projection onto PV and PH.
   - For a point A: vertical projection a' and horizontal projection a.
   - The two planes are made coplanar by abatimiento.

5. Dibujo Técnico Bachillerato — *Introducción a Sistema Diédrico*  
   https://dibujotecnicobachillerato.com/primero/diedrico/introduccion-a-sistema-diedrico/
   - PH projection = planta; PV projection = alzado.
   - PH is rotated about LT as hinge/charnela until it coincides with PV.
   - Corresponding projections are linked by reference lines perpendicular to LT.

## Geometry contract for the animation

The scene must show the following literally:

1. **PV and PH are perpendicular planes**, not two unrelated screen rectangles.
2. **LT is their common intersection and the real hinge axis**.
3. Place an element in the **first dihedral**: in front of PV and above PH.
4. First demonstrate a single point A:
   - project A orthogonally to PV -> a' (alzado coordinate);
   - project A orthogonally to PH -> a (planta coordinate);
   - projector directions are normal to the receiving plane.
5. Replace the point by one coherent asymmetric stepped solid.
6. Build the FRONT and TOP projections from the same object geometry on the actual receiving planes.
7. Remove the object/projectors before the unfolding so the viewer can track the retained projections.
8. **Rotate PH and its top projection rigidly by -90° about LT**, not by an arbitrary translation or 2D morph.
9. Finish with both projections coplanar:
   - alzado above LT;
   - planta below LT for the first-dihedral / first-angle arrangement;
   - matching x coordinates aligned by reference/projector lines perpendicular to LT.
10. Keep the explanation of Monge/dihedral geometry conceptually separate from the later ISO A / ISO E comparison.

## Visual QA rules

- Use a true `ThreeDScene` for the construction stage.
- White classroom background; black geometry with restrained plane/view accent colors.
- Planes translucent enough to see their perpendicular relationship.
- Never use crossing projector webs; show representative parallel projectors sequentially.
- The solid must remain dimensionally coherent across 3D, alzado and planta.
- The 90° abatimiento must be a rigid rotation around the LT axis.
- Final camera must show a clean sheet-like front view with no perspective ambiguity.
- Safe 16:9 margins; no text or geometry touching the frame border.
