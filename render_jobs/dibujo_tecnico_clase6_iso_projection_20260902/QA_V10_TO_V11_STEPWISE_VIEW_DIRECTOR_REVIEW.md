# QA V10 → V11 · Stepwise 2D View Director Review

Date: 2026-09-08

## Actual V10 reviewed

Uploaded render reviewed directly:

`Diedrico_3D_to_2D_V10_UPSHIFT_DIRECTOR_QA_FINAL(1).mp4`

Technical inspection:

- codec: H.264
- pixel format: yuv420p
- frame: 1920 × 1080
- nominal frame rate: 30 fps
- duration: 95.397396 s
- decoded frames: 2862
- file size: 4,677,139 bytes
- SHA-256: `5760e2ba57efb97664be8ec79430a3d9c2c3ff4050cad972b8be42be0ee4ba03`

A 24-frame uniformly distributed contact review was made across the complete timeline, with additional attention to the 3D projection, PH fold, final 2D sheet, method and closing beats.

## What V10 already solved

V10 is materially better than V9 in vertical composition and fold safety. The stepped object remains legible, the three projection planes stay inside the frame, and the PH rotation no longer drops the construction through the lower edge. The final 2D cards are also separated from the title more reliably.

These corrections are preserved in V11.

## Remaining teaching/directing problems in V10

### 1. The lesson still advances too quickly for classroom reading

The current 95.4 s total runtime leaves several important beats visible for only a short period. The object orbit, projection direction labels, projection rays, final sheet and method are understandable when watched as a finished animation, but they still move faster than a teacher-led explanation in which students need to identify the geometry before the next step begins.

### 2. The three 2D views are shown, but not *constructed as three separate ideas*

During approximately the middle half of V10, FRONT, TOP and RIGHT outlines accumulate on the projection planes. Technically correct, but cognitively the student sees more and more geometry in the same 3D frame. The animation does not strongly separate the reasoning:

1. choose one observation direction;
2. project perpendicular to its receiving plane;
3. trace only that resulting 2D contour;
4. stop and read the completed view;
5. store it before starting the next view.

### 3. The clean final sheet appears too quickly

The transition around the final 2D-sheet beat reveals TOP, FRONT and RIGHT cards in a short sequence. The views are visible, but the student does not watch each one being rebuilt line by line in clean 2D and then physically moved to a persistent location.

### 4. There is no persistent “completed views” memory area

A useful classroom device is missing: when ALZADO is completed, it should remain visible while PLANTA is constructed; when PLANTA is completed, both should remain visible while PERFIL is constructed. This makes the one-object/three-descriptions relationship explicit.

### 5. The method and synthesis need a longer reading cadence

The five-step method is correct, but V10 still reads like a summary. V11 should allow each row to appear, highlight, and remain long enough to be read before the next one arrives.

## V11 directing contract

V11 implements the following changes while preserving the validated V10 geometry and fold-safe framing:

1. Global classroom pacing multiplier: `1.25`.
2. FRONT/TOP/RIGHT physical projection rays are split into anchor rays first and remaining rays second.
3. Each physical projection gets an explicit `1 DIRECCIÓN → 2 PROYECTORES → 3 CONTORNO` caption.
4. The PH fold keeps the V10 pre-rotation upward reframe and is slowed to a 4.8 s rotation plus longer holds.
5. A new clean 2D construction studio is added after the fold/alignment explanation.
6. ALZADO is constructed in three numbered steps, traced segment by segment, paused, then reduced and moved to a right-hand “VISTAS TERMINADAS” archive.
7. PLANTA is constructed next, with outer footprint → middle tier → upper tier shown separately, then parked beneath ALZADO on the right.
8. PERFIL is traced segment by segment and parked as the third completed view.
9. The three stored cards then move fluidly from the right archive into a conventional aligned drawing-sheet arrangement using the *same card objects*, not a cut to a new static slide.
10. Alignment guides are drawn only after the cards reach the final arrangement.
11. The five-step method receives longer row-by-row holds.
12. The closing synthesis retains three mini-view silhouettes as a visual memory cue.

## Publication/workflow correction

V10 successfully produced a valid artifact even though its Actions run later failed during GitHub publication. V11 therefore changes delivery order:

1. render and QA the exact PQH MP4;
2. copy the exact validated MP4 into a deterministic package;
3. upload the GitHub Actions artifact **before** publication;
4. publish using the latest branch-head commit instead of assuming the original workflow-trigger SHA is still the branch head;
5. verify the commit-pinned `raw.githubusercontent.com` MP4 byte-for-byte against the validated artifact.

This ensures that even if publication ever fails, the actual rendered MP4 remains downloadable from the workflow artifact.

Workflow registration trigger: V11 renderer is now registered on the branch; this revision starts the full PQL → PQH → QA → artifact → publication pipeline.
