# Senior post-render QA — Class 6 ISO V2 -> V3

## Actual V2 render inspected
`Dibujo_Tecnico_Clase6_ISO_Projection_Systems_V2_SENIOR_QA_FINAL_pqh.mp4`

Technical decode of the actual V2 PQH artifact:
- 1920×1080
- H.264 / yuv420p
- 30.004 fps
- 154.145 s
- 4,625 decoded frames
- 7,453,914 bytes

The complete movie was decoded and every frame was scanned for unsafe hard-border contact. A dense distributed timeline review and targeted full-resolution inspection of the 3D/projection scenes were then performed.

## V2 defects found after render

### 1. Dihedral projector web crosses itself
During the FRONT/TOP projection explanation, two projector bundles coexist and cross in the middle of the scene. This creates a dense X-shaped dashed-line web that obscures the geometry instead of clarifying orthographic projection.

**V3:** FRONT projectors are shown, used, and removed before TOP projectors appear.

### 2. Dihedral unfold duplicates and stacks views
V2 uses copied FRONT/TOP objects for the unfold stage while the originals remain visible. Multiple FRONT/TOP silhouettes accumulate in the same plane region.

**V3:** the existing TOP plane and TOP view are transformed in place. No projection view is duplicated during the 90° unfold.

### 3. V2 fails the strict safe-border gate
The every-frame scan found **522 consecutive unsafe frames**, frames 423–944 (approximately 14.10–31.46 s), all within the rebuilt dihedral scene.

**V3:** the border triad is removed from that scene, all teaching geometry is moved inside the classroom safe area, and the same every-frame scan is required to return zero unsafe frames.

### 4. Example projector rays pass through completed view cards
In the ISO A examples, the later TOP/RIGHT projector bundles visually pass through previously completed FRONT/TOP cards because rays connect directly from the 3D solid to final sheet positions.

**V3:** every view is first projected into one temporary clean projection plane near the object. After the rays disappear, that finished card moves to its final ISO A / ISO E sheet location.

### 5. House 3D front gable is visually fragmented
Although V2 corrected the dimensions, its front wall rectangle and triangular gable were separate filled faces, which leaves the model visually fragmented in the isometric view.

**V3:** the front is one coherent pentagonal gable face; roof faces, ridge, eave, TOP view and RIGHT view all share the same 3D coordinates.

## V3 acceptance gate
1. `py_compile` for V1, V2 and V3.
2. Literal complete-timeline `-pql` render.
3. Literal `-pqh` render at 1920×1080, 30 fps.
4. H.264 / yuv420p full decode.
5. Every-frame hard-border scan: **0 unsafe frames** required.
6. 120-frame distributed contact sheet generated from the final PQH.
7. Targeted geometry-frame extraction from dihedral, ISO A and ISO E examples.
8. SHA-256 of the exact validated MP4.
9. Publish the exact validated MP4 to `published_renders/`.
10. Verify publication by the exact publication commit SHA, not by a moving branch ref.
