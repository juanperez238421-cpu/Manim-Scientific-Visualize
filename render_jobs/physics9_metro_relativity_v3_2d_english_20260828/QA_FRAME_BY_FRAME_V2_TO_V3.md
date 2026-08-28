# Physics 9 Metro Relativity — V2 full-frame QA and V3 redesign

## Scope
The current V2 final MP4 was decoded frame-by-frame before redesign.

- duration: 119.6 s
- frame rate: 30 fps
- decoded frames reviewed by automated scan: 3,588 / 3,588
- blank transition frames: 95
- very sparse frames (<0.5% dark-pixel coverage): 108
- sparse frames (<1.0% dark-pixel coverage): 115
- additional visual review: distributed steady-state frames, animation transition frames, and the existing contact sheet

The automated pass was used to detect blank/sparse states, edge occupation, and abrupt scene changes. Visual QA was then used to judge pedagogy, scale, proportion, pose readability, and scene hierarchy.

## V2 findings by timeline

### 0–13 s — opening
- 3D metro geometry dominates the screen but does not improve the physics argument.
- The train appears small relative to the 16:9 frame.
- The camera angle creates unnecessary perspective and weakens the classroom-diagram style.
- **V3 action:** remove the entire 3D opening. Replace it with a large 2D side-view metro moving along a horizontal track.

### 14–25 s — two observers
- Human pictograms are recognizable, but the train/observer system is still smaller than necessary.
- Too much unused white space separates the station observer from the interior observer.
- The reference-frame idea appears before the most useful equation is established.
- **V3 action:** enlarge both figures and introduce `X = X0 + vt` on this first conceptual screen.

### 26–39 s — walker inside the train
- This is one of the strongest V2 sections.
- The person is legible, but the walking translation and formula development are not tightly synchronized.
- The original values in km/h require extra interpretation for position calculations.
- **V3 action:** use 2 m/s for the walker and a 5 s interval so `Δx = 10 m` follows immediately from `X = X0 + vt`.

### 40–55 s — station view
- The metro and walker become relatively small while formula cards occupy the dominant area.
- Formula placement is detached from the actual motion.
- **V3 action:** use a larger metro, larger station observer, and explicitly track `X_train = 100 m` and `X_walker = 110 m` after 5 s.

### 56–65 s — frame comparison
- Concept is correct and visually simple.
- The two results should be expressed in one unit system before converting to km/h.
- **V3 action:** show 2 m/s vs 22 m/s first, then optionally annotate 7.2 km/h vs 79.2 km/h.

### 66–80 s — lamp section
- Lamp pulse is visually clear.
- The transition to special relativity is too abrupt and the student does not yet calculate anything.
- **V3 action:** retain the 2D lamp idea, then turn it into an explicit light-clock exercise.

### 81–99 s — station light section
- 3D returns and breaks the visual continuity of the lesson.
- Perspective makes the invariant-speed claim harder to read than a 2D diagram would.
- **V3 action:** remove this section completely and replace it with a 2D moving-light-clock triangle.

### 100–119.6 s — final summary
- Summary is too sparse after a relatively dense lesson.
- V2 ends with the invariance of `c`, but it does not make students discover why time cannot remain absolute.
- **V3 action:** end with the same two light events measured in two frames: 8.0 ns in the train frame and 10.0 ns in the station frame.

## V3 numerical redesign

### Ordinary metro motion
Use deliberately simple SI values:

- metro speed: `20 m/s = 72 km/h`
- walking speed relative to metro: `2 m/s = 7.2 km/h`
- walking speed from station: `22 m/s = 79.2 km/h`
- observation interval: `5 s`

With `X = X0 + vt`:

- inside metro: `X'_w = 0 + (2)(5) = 10 m`
- train from station: `X_train = 0 + (20)(5) = 100 m`
- walker from station: `X_w = 0 + (22)(5) = 110 m`

This makes relative displacement visually and numerically transparent: the walker is still 10 m ahead of the train reference point after 5 s.

### Relativistic thought experiment
The ordinary metro remains non-relativistic. A separate clearly labeled **hypothetical relativistic train** is introduced only to make the time effect large enough to calculate by hand.

Use:

- train speed: `v = 0.60c`
- vertical light-clock height: `H = 2.4 m`
- light speed: `c = 3.00 × 10^8 m/s`

Train frame:

`Y_light = 0 + ct'`

`2.4 = ct'  ->  t' = 8.0 ns`

Station frame:

`X_mirror = X0 + vt = 0 + 0.60ct`

The light still moves at `c`, while the ceiling mirror moves horizontally. The geometry gives:

`(ct)^2 = (0.60ct)^2 + (2.4)^2`

`0.64 c^2 t^2 = 5.76`

`ct = 3.0 m`

`t = 10.0 ns`

The horizontal mirror displacement is 1.8 m and the light path is 3.0 m, giving a clean 1.8–2.4–3.0 right triangle.

## Key pedagogical conclusion
The two frames describe the **same emission event and the same mirror-hit event**.

- both measure light speed `c`
- train-frame elapsed coordinate time: `8.0 ns`
- station-frame elapsed coordinate time: `10.0 ns`

Therefore the lesson does not merely state that the speed of light is invariant. Students calculate that if `c` is invariant, elapsed coordinate time cannot be universal/absolute across inertial frames.

## V3 visual contract
- 100% 2D Manim objects
- 100% English visible text
- no `ThreeDScene`, `Prism`, `Sphere`, `Cylinder`, perspective camera, or 3D axes
- large side-view metro with consistent human pictograms
- one dominant result per screen
- fluid gait transforms for walking
- explicit pauses before both student calculations
- `X = X0 + vt` introduced early and reused explicitly
- 1920×1080, 30 fps, H.264/yuv420p
- every rendered frame scanned automatically after PQH render
- distributed visual contact-sheet audit in addition to the full-frame scan
