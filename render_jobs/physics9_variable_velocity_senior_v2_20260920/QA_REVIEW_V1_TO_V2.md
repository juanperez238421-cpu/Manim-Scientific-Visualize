# Physics 9 Variable Velocity — QA Review and Senior V2 Remediation

## V1 forensic review

The V1 MP4 is technically valid (1920×1080, 30 fps, H.264), but it does not meet the JP Classroom visual-format contract.

### Critical visual failures

1. **Opening title exceeds the safe frame.** The title is visibly clipped on the left/right because it is created at a fixed large font size without the project \`fit()\` / frame-safety check.
2. **Closing sentence is clipped below the frame.** The final sentence extends beyond the lower safe zone.
3. **Route-story overlays collide.** Speed/status text and event labels occupy the same vertical band above the road, producing unreadable overlaps during transitions.
4. **Graph annotations are overcrowded.** Multiple labels are placed directly on the position-time and velocity-time graphs and compete for the same space.
5. **Section architecture is duplicated instead of using the consolidated style system.** V1 uses bespoke \`section_header()\` and \`clear_all()\` helpers instead of \`standard_opening()\`, \`set_header()\`, \`clear_stage()\`, and safe-layout assertions.
6. **Color system is inconsistent with the default classroom standard.** V1 simultaneously uses blue, red, amber, green, and purple, while the project standard defaults to a monochrome hierarchy unless color is explicitly required.
7. **No runtime layout guards.** V1 has no \`assert_within_frame()\` or \`assert_content_safe()\` checks, so clipped content can pass CI even when ffprobe/decode succeed.
8. **Physics precision can be improved.** The displayed interval formula should be identified as average acceleration: \`a_prom = Δv/Δt\`.

## Senior V2 remediation

- Uses \`JPMathClassroomScene\` and the JP classroom helpers.
- Uses the standard opening, numbered persistent headers, white background, black/gray hierarchy, and reusable panels.
- Adds numerical validation before rendering.
- Adds safe-frame and safe-content assertions to every major section.
- Replaces simultaneous route labels with one event card that transforms as the car advances.
- Uses graph + interpretation-panel layouts instead of placing several text blocks over graph data.
- Uses a single moving marker/guide line to focus attention on one physical event at a time.
- Uses \`a_prom = Δv/Δt\` for the interval-based acceleration bridge.
- Final delivery pipeline requires Python compile, style checker, PQL runtime, literal PQH, ffprobe, full decode, audit frames, contact sheet, SHA-256, and artifact/package publication.
