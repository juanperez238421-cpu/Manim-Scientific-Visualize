# Physics 9 Relativity V4 → V5 — Senior Code + Motion QA

## Scope

Input reviewed:
- `Physics9_Relative_Motion_Maxwell_Einstein_V4_FINAL_pqh(1).mp4`
- 1920×1080, 30 fps, H.264/yuv420p
- duration 87.860156 s
- 2,636 video frames

The V4 Python source and every scene/helper function were reviewed before the V5 rewrite. The uploaded V4 render was decoded and sampled across the full timeline to compare code intent against rendered motion. The V5 workflow adds another literal PQL gate, literal PQH render, full FFmpeg decode, all-frame blank/border scan, and a dense distributed visual audit.

## Frame-level visual findings in V4

### Opening / reference frames
- Geometry is readable, but the walker is a fixed pose translated across the screen.
- Human motion reads as sliding rather than walking.
- The building observer is mostly passive; there is no visual sightline or observation cue.
- Train motion is simple translation; the scene lacks relative-motion layering.

### Inside-train scene
- The two-column layout is safe after V4 R2, but the walker still glides rigidly.
- The position formula is correct, but time and position do not update continuously during the motion.
- The student does not visually see `t` and `X'` changing together.

### Building / ground-frame scene
- The train and walker translate independently, but the walker pose is frozen.
- The observer has no active line of sight.
- The difference between train displacement and walker displacement is shown only after the motion, not during it.
- The observer perspective is conceptually correct but visually underdeveloped.

### Comparison / history
- The comparison screen is static.
- Galileo/Newton, Maxwell, and Einstein sections are correct but become text-card sequences.
- Maxwell's wave is drawn once rather than propagated.
- The transition from ordinary relative motion to invariant light speed is primarily verbal.

### Final bridge
- The final scene summarizes the conflict but does not derive a numerical case where elapsed time differs between inertial observers.
- Therefore the student is told that time becomes non-absolute but is not yet forced to calculate it.

## V4 function-by-function audit

| V4 function / block | QA finding | V5 action |
|---|---|---|
| render configuration | Correct and protocol-aligned | Preserved |
| timing wrappers `play`, `wait` | Useful for PQL/PQH protocol | Preserved |
| `txt`, `mtex`, `fit`, `header` | Good safe-layout foundation | Preserved and reused |
| `formula_box`, `result_box` | Good projector-safe design | Generalized into `formula_box` + `text_box` |
| `clear_scene` | Repeated full-scene fades create stop/start rhythm | Replaced by shorter targeted transitions |
| `person(... walking=True)` | **Major motion defect:** walking is a single frozen pose | Replaced by `person_pose(phase)` articulated gait rig |
| `person(... seated=True)` | Readable | Retained as a dedicated seated branch |
| `train` | Geometry mostly good after R2, but not designed as a motion system | Rebuilt as proportional `train_shell`; windows scale with body |
| `building` | Readable but passive | Retained; paired with live observer sightline |
| `velocity_arrow` | Good | Retained |
| `observer_badge` | Useful but static | Replaced where appropriate by `text_box` and active sightline |
| `opening` | Train + person translate, but no gait/parallax observation | Simultaneous train motion + articulated walking + observer sightline |
| `reference_frames` | Correct concept, largely static | Folded into moving inside/outside demonstrations |
| `inside_train` | Formula correct; walker slides rigidly | Articulated gait, live `t'` and `X'` counters, synchronized formula |
| `from_building` | Correct 20+2=22; motion lacks observational cues | Articulated walker + moving train + sightline + live displacement counters |
| `compare_frames` | Static duplicated icons | Both figures walk during comparison |
| `classical_history` | Correct but text-heavy | Reframed using animated velocity vectors first |
| `maxwell` | Static sine wave | Traveling EM wave driven by a phase tracker |
| `tension` | Correct historical conflict | Simplified and merged with Maxwell sequence |
| `einstein` | Correct, static | Kept concise and turned into a question that launches the exercise |
| `final_bridge` | No numerical time-relativity derivation | Replaced by a complete moving light-clock exercise |

## V5 numerical design

### Ordinary relative motion

Train:
\[
V=20\,\mathrm{m/s}
\]

Walker relative to train:
\[
v'=2\,\mathrm{m/s}
\]

Ground observer:
\[
v=v'+V=22\,\mathrm{m/s}
\]

For 3 s:

\[
X_{\rm train}=0+(20)(3)=60\,\mathrm{m}
\]

\[
X_{\rm walker}=0+(22)(3)=66\,\mathrm{m}
\]

The walker remains 6 m ahead of the train reference point, which matches the inside-train result:

\[
X'=0+(2)(3)=6\,\mathrm{m}
\]

### Relativistic light-clock exercise

Use a hypothetical train speed:
\[
v=0.60c
\]

Mirror separation:
\[
H=3.0\,\mathrm{m}
\]

Train frame, one half-trip:
\[
t'_{1/2}=\frac{H}{c}=\frac{3.0}{3.00\times10^8}=10.0\,\mathrm{ns}
\]

Train-frame round trip:
\[
\Delta t'=20.0\,\mathrm{ns}
\]

Ground frame, mirror position uses the same general position equation requested for the lesson:

\[
x_{\rm mirror}=x_0+vt=0+(0.60c)t
\]

The light travels a diagonal distance `ct`, so:

\[
(ct)^2=H^2+(0.60ct)^2
\]

\[
c^2t^2(1-0.36)=9
\]

\[
0.64c^2t^2=9
\]

\[
ct=3.75\,\mathrm{m}
\]

\[
t_{1/2}=12.5\,\mathrm{ns}
\]

Ground-frame round trip:
\[
\Delta t=25.0\,\mathrm{ns}
\]

Verification:
\[
\gamma=\frac{1}{\sqrt{1-0.60^2}}=1.25
\]

\[
\Delta t=\gamma\Delta t'=1.25(20.0\,\mathrm{ns})=25.0\,\mathrm{ns}
\]

This produces a clean classroom conclusion:
- same physical light clock;
- same light speed `c`;
- train clock interval = 20.0 ns;
- ground coordinate interval = 25.0 ns;
- therefore elapsed time is frame-dependent.

## V5 motion architecture

The new motion system uses:
- `ValueTracker` for gait phase;
- articulated arm/thigh/knee/foot geometry from trigonometric joint angles;
- torso/head bob synchronized to the gait cycle;
- continuous live time and distance counters;
- independent train translation and walker-relative translation;
- observer-to-walker dashed sightline;
- moving Maxwell wave phase;
- moving light pulses and mirror geometry;
- diagonal light paths in the ground frame;
- staged equations that enter only after the corresponding visual event.

## Release-blocking visual QA criteria

The V5 render is rejected if any of the following occur:
1. text or equations clip the frame;
2. formula boxes overlap the train, walker, observer, or light clock;
3. walker translates without visible gait cycling;
4. building observer is clipped;
5. train body or windows clip at start/end positions;
6. any Spanish visible text appears;
7. any 3D API appears;
8. the final video fails full FFmpeg decode;
9. the all-frame scan reports excessive blanks or border-heavy frames;
10. the time-dilation values differ from 20.0 ns and 25.0 ns for the selected problem.
