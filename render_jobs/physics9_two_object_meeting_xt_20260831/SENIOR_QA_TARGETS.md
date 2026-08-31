# Senior QA Targets — Physics 9 Two-Object x-t Meeting

## Source lineage
This lesson is a direct classroom continuation of `Physics9_Position_Time_Graph_Construction_V3_SENIOR_QA_FINAL_pqh` and must preserve its accepted layout, graph-construction logic, explicit numeric scale, transition discipline and technical render protocol.

## Mathematical acceptance gates
- `x_A(t) = 1 + 2t`.
- `x_B(t) = 13 - t`.
- Table values must be exactly A = `[1,3,5,7,9,11]` and B = `[13,12,11,10,9,8]` at t = 0…5 s.
- Graph intersection must be exactly `(4 s, 9 m)`.
- Algebra must solve `1 + 2t = 13 - t` to `t = 4 s`.
- Substitution into both equations must return `x = 9 m`.

## Pedagogical acceptance gates
1. One positive direction is defined before velocity signs are used.
2. Both data sets are recorded before the final meeting is interpreted.
3. Time is horizontal and position is vertical.
4. Both motions use the same axes and the same scale.
5. Students receive a visible pause before the intersection is revealed.
6. The intersection is explained as **same time + same position**.
7. Physical motion and graph-point motion are synchronized under one clock.
8. The equation method is introduced only after the graphical meaning is established.
9. Graphical and algebraic results are compared explicitly.

## Visual acceptance gates
- White background; black/gray hierarchy only.
- Explicit x-axis labels 0…5 and y-axis labels 0,2,…,14.
- Scale card: 1 s horizontally, 2 m vertically.
- Object A = solid black graph with filled dots.
- Object B = dashed dark-gray graph with hollow dots.
- No data points hidden by axis callouts.
- No warped row highlights.
- No semantic text glyph morphs between unrelated states.
- No detached answer rectangles.
- Intersection projection lines remain legible at Full HD.
- Header/title/subtitle remain inside the JP safe frame.

## Technical release gates
- Python compile.
- Literal `-pql` runtime gate in ManimCE 0.20.1 Docker.
- Literal `-pqh` final render.
- 1920×1080, 30 fps, H.264, yuv420p.
- Full FFmpeg decode with empty error log.
- Every-frame blank/sparse/border scan.
- 96 distributed audit frames plus contact sheet.
- Additional targeted frames around the graph-intersection reveal and synchronized meeting.
- SHA-256 for final MP4.
- Reproducible ZIP containing source, storyboard, QA evidence, protocol, workflow and final render.
