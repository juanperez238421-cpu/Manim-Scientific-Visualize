# Physics 9 — Bus Light Clock / Time Dilation V1

## Purpose
Create a full classroom animation from the supplied exercise: a bus moving at `v = 0.60c`, a vertical light clock of height `L = 3.0 m`, Ana inside the bus, and Carlos observing from the road.

## Scientific checks
- `c = 3.0×10^8 m/s`
- Half-trip inside the bus: `t0 = L/c = 1.0×10^-8 s = 10 ns`
- Lorentz factor at `v/c = 0.60`: `γ = 1/sqrt(1-0.60^2) = 1.25`
- Carlos half-trip time: `t = γ t0 = 12.5 ns`
- Carlos horizontal displacement during the half-trip: `vt = 2.25 m`
- Carlos light-path length during the half-trip: `ct = 3.75 m`
- Pythagorean check: `3.75^2 = 3.0^2 + 2.25^2`
- Full light-clock tick: Ana `20 ns`; Carlos `25 ns`.

## Pedagogical sequence
1. Opening challenge with the fast bus and the light clock.
2. Ana's frame: vertical light path and `t0 = L/c`.
3. Carlos's frame: the bus moves while the pulse travels diagonally.
4. Freeze the geometry into the right triangle `ct`, `L`, `vt`.
5. Derive the time-dilation relation one algebraic step at a time.
6. Substitute `v = 0.60c` and obtain `t = 1.25t0 = 12.5 ns`.
7. Interpret the result with side-by-side light-clock timing.
8. Contrast the classical velocity-addition prediction `c + 0.60c = 1.60c` with invariant `c`.
9. Show the low-speed limit using the Lorentz-factor curve.
10. End with the reunion question as an open discussion prompt and a reproducible reasoning map.

## Visual contract
- 1920×1080, 30 fps.
- White background.
- Black / gray classroom hierarchy.
- Amber used only for the light pulse and its path.
- 100% 2D.
- No external assets and no absolute paths.
- Large projector-safe typography.
- One dominant idea per screen.
- Equations revealed progressively instead of appearing as a wall of text.
- Bus and light-clock motion must be genuinely animated, not presented as a static poster.

## Render contract
1. `python -m py_compile` gate.
2. Literal `-pql` ManimCE 0.20.1 Docker render with reduced lesson timing.
3. Literal `-pqh` final render at full timing.
4. `ffprobe` verification: 1920×1080, 30 fps, H.264, yuv420p.
5. Full FFmpeg decode.
6. Every-frame automated scan.
7. 48-frame distributed contact sheet.
8. Publish MP4 + QA files to `deliveries/physics9_bus_light_clock_v1_20260907/`.
