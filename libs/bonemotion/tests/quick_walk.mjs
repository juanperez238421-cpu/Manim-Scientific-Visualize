import { createMrBones } from '../src/characters/mrbones/index.js';
import { gait } from '../src/clips/locomotion.js';
const mb = createMrBones();
for (const style of ['neutral', 'chaplin']) {
  const g = gait(mb.profile, { style, yaw: 1.2, steps: 8 });
  let clamps = 0, minY = 1e9, skate = 0;
  let prev = null;
  for (let t = g.tStart; t <= g.tStop; t += 1 / 60) {
    const p = g.poseAt(t);
    const { ev } = mb.evaluatePose(p);
    for (const f of ev.flags.ik) if (!f.reach) clamps++;
    for (const n of ['R', 'L']) { minY = Math.min(minY, ev.J[`ball${n}`][1], ev.J[`heel${n}`][1]); }
    if (prev) for (const n of ['R','L']) for (const k of ['ball','heel']) {
      const a = prev.J[`${k}${n}`], b = ev.J[`${k}${n}`];
      if (a[1] < 0.01 && b[1] < 0.01) skate = Math.max(skate, Math.hypot(a[0]-b[0], a[2]-b[2]));
    }
    prev = ev;
  }
  console.log(style, 'dur', (g.tStop-g.tStart).toFixed(2), 'speed m/s', (g.speed/200).toFixed(2), 'clamps', clamps, 'minY', minY.toFixed(4), 'skate', skate.toExponential(2));
}
