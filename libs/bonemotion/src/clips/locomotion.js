// Procedural gait with exact foot plants (no foot skate by construction).
//
// The walk is built the way an animator breaks it down — contact, down, passing, up — but every
// pose is solved, not guessed:
//   footsteps     planned first (arc length along a straight path, ramped first/last steps)
//   stance        heel strike -> foot flat -> heel off -> toe off: a no-slip roll about the heel and then
//                 the ball (ankle from the pivot), toes kept flat during heel-off
//   swing         C1 Hermite between the toe-off and heel-strike poses, a clearance bump that has zero
//                 value and slope at both ends, a lateral circumduction bulge (Chaplin: wide + flick)
//   pelvis        forward travel, lateral sway over the stance foot, vertical bob (high at mid-stance:
//                 inverted pendulum), twist and roll — keyed on the footstep times with monotone C1 tracks;
//                 the height is then soft-limited (smooth min) so no leg ever over-extends (no knee pop)
//   upper body    counter-twist of the chest, arms swinging opposite the legs with drag, head stabilised
// Everything retargets through profile.dims (leg length, hip width, foot geometry).
import { track, ease, smin, clamp } from '../core/curves.js';
import { SIDE, toWorld, fwdOf, leftOf, ankleFromPivot, reachHeight, hangArm } from '../core/body.js';
import { add, sub, scl, mv, ry } from '../core/m3.js';

export const WALK_STYLES = {
  neutral: { cadence: 1.9, stepLen: 0.5, duty: 0.6, width: 0.55, toeOut: 0.12, lift: 0.1, swingOut: 0.02, kick: 0, heelStrike: 0.28, toeOff: 0.5,
    bob: 2.5, sway: 4, roll: 0.05, yawAmp: 0.09, counter: 0.7, armSwing: 18, armDrag: 0.07, ext: 0.97, kneeOut: 0.2, hipDrop: 2, lean: 0.03 },
  // Chaplin's tramp shuffle: quick short steps, feet turned far out, stiff knees, waddling hips,
  // the swing foot flicks out sideways before it lands, chest up and a slight backward lean
  chaplin: { cadence: 2.6, stepLen: 0.34, duty: 0.6, width: 0.42, toeOut: 0.8, lift: 0.07, swingOut: 0.1, kick: 0.09, heelStrike: 0.34, toeOff: 0.45,
    bob: 3.5, sway: 9, roll: 0.1, yawAmp: 0.06, counter: 0.5, armSwing: 12, armDrag: 0.08, ext: 0.985, kneeOut: 0.65, hipDrop: 0, lean: -0.07 },
};

export function gait(pr, opts = {}) {
  const st = { ...WALK_STYLES[opts.style || 'neutral'], ...opts };
  const d = pr.dims;
  const L = st.stepLen * d.legLen;
  const Ts = 1 / st.cadence; // one step
  const cyc = 2 * Ts;
  const swingT = (1 - st.duty) * cyc;
  const yaw = st.yaw ?? 0;
  const F = fwdOf(yaw), Lf = leftOf(yaw);
  const origin = [st.x ?? 0, 0, st.z ?? 0];
  const nSteps = st.steps ?? 8;
  const first = st.first ?? 0; // index of the leg that steps first (0 = right)
  const tWalk = st.t0 ?? 0.4; // first toe-off (the weight shift happens before it)
  const lat = st.width * d.hipW * 1.5;
  const foot = pr.foot;

  // ---- footstep plan: every plant has an arc-length S and its strike / lift times
  const plants = [[], []];
  for (const i of [0, 1]) plants[i].push({ S: 0, tStrike: -Infinity, tLift: Infinity, initial: true });
  const ramp = (k) => (k === 0 ? 0.55 : k === 1 ? 0.85 : 1);
  let lastS = 0;
  const strikes = [];
  for (let k = 0; k < nSteps; k++) {
    const i = (first + k) % 2;
    const tl = tWalk + k * Ts, ts = tl + swingT;
    const isLast = k === nSteps - 1;
    const S = isLast ? lastS : lastS + ramp(k) * L;
    plants[i][plants[i].length - 1].tLift = tl;
    plants[i].push({ S, tStrike: ts, tLift: Infinity, k, final: isLast });
    strikes.push({ k, i, ts, tl, S });
    lastS = Math.max(lastS, S);
  }
  const tEnd = strikes[strikes.length - 1].ts;
  const groundOf = (i, S) => add(add(origin, scl(F, S)), scl(Lf, SIDE[i] * lat));
  const headingOf = (i) => yaw + SIDE[i] * st.toeOut;

  // stance foot: heel-strike roll (heel pivot), flat, heel-off roll (ball pivot) — exact pivots
  const stanceLeg = (i, p, t) => {
    const g = groundOf(i, p.S), hd = headingOf(i);
    const stanceDur = p.tLift - p.tStrike;
    const rollIn = Math.min(0.16, 0.22 * (Number.isFinite(stanceDur) ? stanceDur : 1));
    const offDur = 0.42 * (Number.isFinite(stanceDur) ? stanceDur : 1);
    const pivotW = (loc) => add(g, mv(ry(hd), [loc[0], 0, loc[2]]));
    if (t < p.tStrike + rollIn) { // heel contact, toes coming down
      const u = ease.smooth(clamp((t - p.tStrike) / rollIn, 0, 1));
      const pitch = -st.heelStrike * (1 - u);
      return { ankle: ankleFromPivot(pivotW(foot.heel), foot.heel, hd, pitch), heading: hd, pitch, toe: 0, plantW: 0, kneeOut: st.kneeOut };
    }
    if (t > p.tLift - offDur) { // heel rising, toes stay planted
      const u = ease.smooth(clamp((t - (p.tLift - offDur)) / offDur, 0, 1));
      const pitch = st.toeOff * u;
      return { ankle: ankleFromPivot(pivotW(foot.ball), foot.ball, hd, pitch), heading: hd, pitch, toe: 0, plantW: 1, kneeOut: st.kneeOut };
    }
    return { ankle: [g[0], d.ankleH, g[2]], heading: hd, pitch: 0, toe: 0, plantW: 1, kneeOut: st.kneeOut };
  };
  // swing foot: from the toe-off pose to the heel-strike pose
  const swingLeg = (i, a, b, t) => {
    const u = clamp((t - a.tLift) / (b.tStrike - a.tLift), 0, 1);
    const A = stanceLeg(i, a, a.tLift), B = stanceLeg(i, b, b.tStrike);
    const e = ease.smoother(u);
    const pos = A.ankle.map((x, k) => x + (B.ankle[k] - x) * e);
    const uu = Math.pow(u, 0.85);
    const bump = 16 * uu * uu * (1 - uu) * (1 - uu); // zero value and slope at both ends
    pos[1] += st.lift * d.legLen * bump;
    // circumduction: the foot swings out around the stance leg; Chaplin flicks it out late in the swing
    const out = st.swingOut * d.legLen * bump + st.kick * d.legLen * Math.sin(Math.PI * u) ** 2 * Math.max(0, Math.sin(Math.PI * (u - 0.35) / 0.65)) * (u > 0.35 ? 1 : 0);
    const side = scl(Lf, SIDE[i] * out);
    const pitch = A.pitch + (B.pitch - A.pitch) * ease.smooth(u) - 0.25 * bump;
    const peel = 1 - ease.smooth(clamp(u / 0.3, 0, 1)); // toes stay flat while the ball leaves the floor
    return { ankle: add(pos, side), heading: A.heading + (B.heading - A.heading) * e, pitch, toe: 0.25 * bump, plantW: peel, kneeOut: st.kneeOut + 0.1 * bump };
  };
  const legAt = (i, t) => {
    const P = plants[i];
    for (let j = 0; j < P.length; j++) {
      const p = P[j];
      if (t < p.tStrike) return swingLeg(i, P[j - 1], p, t);
      if (t <= p.tLift || j === P.length - 1) return stanceLeg(i, p, t);
    }
    return stanceLeg(i, P[P.length - 1], t);
  };

  // ---- pelvis tracks keyed on the footstep times
  const tPrep = tWalk - 0.45; // weight shift onto the stance leg (anticipation of the first step)
  const stanceFirst = 1 - first;
  const sKeys = [{ t: tPrep, v: 0 }, { t: tWalk, v: 0.06 * L }];
  const latKeys = [{ t: tPrep, v: 0 }, { t: tWalk, v: SIDE[stanceFirst] * st.sway * 0.8 }];
  const yKeys = [{ t: tPrep, v: 0 }, { t: tWalk, v: -st.bob * 0.6 }];
  const yawKeys = [{ t: tPrep, v: 0 }];
  const rollKeys = [{ t: tPrep, v: 0 }, { t: tWalk, v: SIDE[stanceFirst] * st.roll * 0.6 }];
  let prevS = 0;
  strikes.forEach((s, n) => {
    const other = n === 0 ? 0 : strikes[n - 1].S;
    sKeys.push({ t: s.ts, v: 0.5 * (s.S + other) });
    yKeys.push({ t: s.ts, v: -st.bob });
    if (n < strikes.length - 1) {
      const nx = strikes[n + 1];
      const tm = 0.5 * (nx.tl + nx.ts); // single support on foot s.i: mid-stance
      sKeys.push({ t: tm, v: s.S });
      latKeys.push({ t: tm, v: SIDE[s.i] * st.sway });
      yKeys.push({ t: tm, v: st.bob });
      rollKeys.push({ t: tm, v: SIDE[s.i] * st.roll });
    }
    yawKeys.push({ t: s.ts, v: n === strikes.length - 1 ? 0 : -SIDE[s.i] * st.yawAmp });
    prevS = s.S;
  });
  void prevS;
  const tStop = tEnd + 0.5;
  sKeys.push({ t: tStop, v: lastS, mode: 'flat' });
  latKeys.push({ t: tEnd, v: 0 }, { t: tStop, v: 0 });
  yKeys.push({ t: tStop, v: 0 });
  yawKeys.push({ t: tStop, v: 0 });
  rollKeys.push({ t: tEnd, v: 0 }, { t: tStop, v: 0 });
  const sT = track(sKeys), latT = track(latKeys), yT = track(yKeys), yawT = track(yawKeys), rollT = track(rollKeys);

  // arms: opposite to the legs, with drag (they lag the pelvis)
  const armKeys = [[{ t: tPrep, v: 0 }], [{ t: tPrep, v: 0 }]];
  strikes.forEach((s, n) => {
    const last = n === strikes.length - 1;
    for (const j of [0, 1]) armKeys[j].push({ t: s.ts + st.armDrag, v: last ? 0 : (j === s.i ? -1 : 1) * st.armSwing });
  });
  for (const j of [0, 1]) armKeys[j].push({ t: tStop + st.armDrag, v: 0 });
  const armT = armKeys.map((k) => track(k));

  const hipH = d.standH - st.hipDrop;
  function poseAt(t) {
    const legs = [legAt(0, t), legAt(1, t)];
    const yawOff = yawT.at(t), roll = rollT.at(t);
    const xz = add(add(origin, scl(F, sT.at(t))), scl(Lf, latT.at(t)));
    let y = hipH + yT.at(t);
    // soft reach limit: never ask a leg for more than ext of its length (no knee pop, no IK clamp)
    for (const i of [0, 1]) y = smin(y, reachHeight(pr, xz, yaw + yawOff, SIDE[i], legs[i].ankle, st.ext), 6);
    const arms = SIDE.map((s, j) => {
      const A = hangArm(pr, s, { out: 6, fwd: -6 });
      const sw = armT[j].at(t);
      A.specs[0].p = add(A.specs[0].p, [0, Math.max(0, sw) * 0.35, sw]);
      A.flex = 0.1 + Math.max(0, sw) * 0.004;
      return A;
    });
    return {
      root: { p: [xz[0], y, xz[2]], yaw: yaw + yawOff, tilt: [0, roll] },
      spine: [0.04 + st.lean, -roll * 0.8, -st.counter * yawOff], neck: [-st.lean * 0.5, -roll * 0.3, -yawOff * 0.4], head: [0, 0, 0],
      shrug: [0, 0], prot: [0, 0], legs, arms,
      face: { jaw: 0.1, look: [0, 0], pupil: 1 }, props: { hat: { mode: 'head' } },
    };
  }
  // the walk breakdown for the phase bar (per step: contact, down, passing, up)
  const phases = [{ name: 'prep', t0: tPrep, t1: tWalk }];
  strikes.forEach((s, n) => {
    if (n === 0) return;
    const prev = strikes[n - 1];
    const a = prev.ts, b = s.ts, h = b - a;
    phases.push({ name: 'contact', t0: a, t1: a + 0.15 * h }, { name: 'down', t0: a + 0.15 * h, t1: a + 0.4 * h }, { name: 'passing', t0: a + 0.4 * h, t1: a + 0.65 * h }, { name: 'up', t0: a + 0.65 * h, t1: b });
  });
  phases.push({ name: 'settle', t0: tEnd, t1: tStop });
  return { poseAt, strikes, plants, phases, tStart: tPrep, tEnd, tStop, speed: L / Ts, stepLen: L, cadence: st.cadence, style: st, groundOf, yaw, F, Lf };
}
