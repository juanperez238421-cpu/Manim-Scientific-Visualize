# STORYBOARD — Physics 9 · Metro, Relative Motion and Light

## Pedagogical objective
Build the idea of reference frame from an everyday metro example, validate classical relative velocity for a walking passenger, then create the conceptual break that motivates special relativity when the passenger turns on a light source.

## Important physics correction
The source statement says 300,000 km/h for light. The lesson explicitly corrects this before using the number:

- c ≈ 300,000 km/s
- c ≈ 1.08 × 10^9 km/h

The original value is shown only as a misconception/unit check and is never treated as the physical speed of light.

## Narrative sequence

1. **3D opening — metro moving south**
   - White background, monochrome train and track.
   - South is defined as +x.
   - Metro glides through a 3D track environment.

2. **3D reference frames**
   - S': seated student inside the metro.
   - S: observer standing on the station platform.
   - Explicit statement: velocity requires an observer/reference frame.

3. **2D inside-train view**
   - Train walls are stationary relative to the student.
   - Walker advances in the same direction at 2 km/h.
   - Result: v_walker/train = 2 km/h.

4. **2D ground/station view**
   - Metro = 80 km/h.
   - Walker adds 2 km/h in the same direction.
   - Galilean addition: 80 + 2 = 82 km/h.
   - Train and walker animate simultaneously with the walker moving 2/80 faster relative to the train motion.

5. **2D split-screen comparison**
   - Same person, two correct answers: 2 km/h and 82 km/h.
   - Emphasis: no contradiction because the reference frames differ.

6. **Unit correction for light**
   - Cross out 300,000 km/h as the light-speed value.
   - Replace with c ≈ 300,000 km/s ≈ 1.08 × 10^9 km/h.

7. **3D light pulse in the metro frame**
   - Walker switches on a lamp.
   - Expanding spherical pulse around the emission event.
   - Seated observer measures c.

8. **3D light pulse from the station frame**
   - Light pulse expands from the emission point while the train moves onward.
   - Ground observer also measures c.
   - Explicit contrast: not c + 80 and not c + 82.

9. **2D Galilean vs Lorentz velocity addition**
   - Ordinary speeds: u = u' + v.
   - Light: u = (u' + v)/(1 + u'v/c²).
   - Substitute u' = c and simplify step by step to u = c.

10. **2D final table and exit question**
    - Metro: 0 km/h inside, 80 km/h ground.
    - Walker: 2 km/h inside, 82 km/h ground.
    - Light: c in both inertial frames.
    - Exit prompt asks why matter and light behave differently in the comparison.

## Visual grammar
- 1920×1080, 30 fps.
- White background.
- Black text and linework, neutral gray hierarchy.
- Single restrained amber accent only for the light pulse.
- Persistent numbered header and subtitle.
- Large projector-safe typography.
- Deliberate pauses for explanation and notebook copying.
- 2D/3D transitions performed by camera orientation changes rather than hard cuts when possible.

## Render protocol
- ManimCE 0.20.1 pinned Docker image.
- py_compile first.
- Literal -pql runtime gate with accelerated lesson time.
- Literal -pqh final render.
- H.264, yuv420p, 1920×1080, 30 fps.
- Full FFmpeg decode.
- 32 distributed audit frames and contact sheet.
- SHA-256 manifest.
- Complete reproducible ZIP.
- Final MP4 copied to the dedicated delivery folder on the render branch.
