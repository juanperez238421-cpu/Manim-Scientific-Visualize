# Physics 9 — Position vs Time Graph Construction V2

Dedicated classroom animation for constructing and interpreting a position-time (`x-t`) graph.

## Scene

- Source: `position_time_graph_construction_v2.py`
- Class: `Physics9PositionTimeGraphConstructionV2`
- Style dependency: `../physics9_position_time_velocity_workshop_20260824/jp_classroom_style.py`
- ManimCE target: `0.20.1`
- Final format: 1920x1080, 30 fps, H.264/yuv420p MP4

## Content

The lesson begins with a physical one-dimensional motion, converts the motion to `(t,x)` data, constructs the axes, plots points with projection guides, connects them chronologically, synchronizes the physical motion with the graph, calculates the slope of each interval, and finishes with misconception checks and a six-step method.

Data used:

| t (s) | x (m) |
|---:|---:|
| 0 | 2 |
| 3 | 8 |
| 5 | 8 |
| 7 | 4 |

Segment velocities: `+2 m/s`, `0 m/s`, `-2 m/s`.

## Render protocol

The dedicated workflow performs:

1. Python compilation and source assertions.
2. Literal `-pql` runtime gate using ManimCE 0.20.1 Docker.
3. Literal `-pqh` final render.
4. `ffprobe` validation for resolution, frame rate, codec and pixel format.
5. Full FFmpeg decode with zero errors required.
6. Every-frame blank/border scan.
7. 48 distributed visual QA frames and contact sheet.
8. SHA-256 checksums.
9. Reproducible ZIP package containing source, style dependency, storyboard, protocol, workflow, render and QA evidence.
10. Final MP4 publication under `deliveries/physics9_position_time_graph_construction_v2_20260828/`.

The project follows `protocols/PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD.md`.
