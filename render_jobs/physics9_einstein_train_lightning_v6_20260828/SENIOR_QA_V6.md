# Physics 9 — Einstein Train & Lightning V6 Senior QA

## Why V6 exists
V5 focused on a light-clock derivation of time dilation. That is a valid special-relativity thought experiment, but it did not explicitly develop the classic train/embankment lightning scenario requested for relativity of simultaneity.

V6 is a dedicated lesson that uses the general motion equation `X = X0 + vt` as the central mathematical tool before introducing the Lorentz time transformation as a confirmation.

## Exact numerical model
Ground/platform frame at `t=0`:
- rear lightning event: `x_R=-150 m`
- front lightning event: `x_F=+150 m`
- train midpoint observer: `x_T=0`
- platform observer: `x_P=0`
- train speed: `v=0.60c`
- light speed: `c=300 m/us`

Worldlines from the general motion equation:
- `x_T(t)=0+(0.60c)t`
- `x_F(t)=150-ct`
- `x_R(t)=-150+ct`
- `x_P(t)=0`

Platform observer:
- both flashes reach `x=0` at `t=150/c=0.500 us`

Train midpoint observer:
- front reception: `0.60ct=150-ct` -> `t_F=150/(1.60c)=0.3125 us`
- rear reception: `0.60ct=-150+ct` -> `t_R=150/(0.40c)=1.250 us`

Lorentz confirmation of strike-event times in the train frame:
- `gamma=1/sqrt(1-0.60^2)=1.25`
- `t'_F=-0.375 us`
- `t'_R=+0.375 us`
- the front strike occurs `0.750 us` before the rear strike in the train frame

## Pedagogical safeguards
- Reception times and strike-event times are explicitly separated.
- The animation does not claim that different reception times alone are the final mathematical proof of non-simultaneity; the Lorentz transformation confirms the strike-event ordering.
- Light always propagates at `c` in the calculations.
- The train is hypothetical and relativistic; `0.60c` is chosen to make the effect visible numerically.

## Visual design
- 1920x1080, 30 fps, 100% 2D
- white background, black/gray line art, amber only for lightning/light pulses
- large projector-safe equations
- fluid train translation and simultaneous pulse propagation
- exact position equations shown before calculations
- spacetime diagram reuses the same worldlines and intersection events
- one dominant calculation result at a time

## Acceptance gates
1. `python -m py_compile`
2. numerical assertions in source
3. literal `manim -pql`
4. literal `manim -pqh`
5. H.264 / yuv420p / 1920x1080 / 30 fps
6. full FFmpeg decode
7. automated scan of every rendered frame
8. 72-frame distributed contact sheet
9. SHA-256 manifest and reproducible project ZIP
