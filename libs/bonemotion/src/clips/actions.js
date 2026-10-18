// Whole-body physics actions: the vertical jump (exact ballistic flight of the pelvis, landing absorbed
// with constant deceleration) and the pirouette that conserves angular momentum (arms in -> faster).
import { standPose, SIDE, toWorld, ankleFromPivot, flatFoot, hangArm } from '../core/body.js';
import { action } from '../core/principles.js';
import { track, ease, clamp, hermite } from '../core/curves.js';
import { projectile, catchAbsorb, spinConserving } from '../core/physics.js';
import { add, sub, scl, mv, mm, ry, rx, norm, len, fapp } from '../core/m3.js';
import { objectFrames } from '../characters/mrbones/model.js';
import { pulse } from './kit.js';

const smooth01 = (t, a, b) => ease.smoother(clamp((t - a) / (b - a), 0, 1));
const wrapPi = (a) => a - 2 * Math.PI * Math.round(a / (2 * Math.PI));

// ------------------------------------------------------------------ the jump
// prep (arms forward) -> anticipation (deep crouch, arms swing back) -> execution (legs drive, arms
// swing up, heels peel off; the pelvis leaves with exactly v_off) -> flight (pelvis on the exact parabola,
// feet tuck then reach) -> landing (balls first, heels down, pelvis stopped over `absorb` u at constant
// deceleration) -> follow-through (arms keep going down, trunk folds) -> settle (back to standing).
export function jump(char, p = {}) {
  const pr = char.profile, d = pr.dims, g = pr.g, K = pr.K;
  const yaw = p.yaw ?? 0.6, o = [p.x ?? 0, 0, p.z ?? 0];
  const h = (p.height ?? 0.32) * K; // apex rise of the pelvis above take-off
  const vOff = Math.sqrt(2 * g * h);
  const T = (2 * vOff) / g;
  const base = standPose(pr, { x: o[0], z: o[2], yaw, toeOut: 0.3, width: 1.1 });
  const H0 = base.root.p[1];
  const crouch = 0.36 * d.legLen; // pelvis drop at the bottom of the anticipation
  const yOff = H0 + 0.035 * d.legLen; // take-off: legs extended, on the balls of the feet
  const absorb = 0.34 * d.legLen;
  const t0 = 0.5, tPrep = t0 + 0.35, tLow = tPrep + 0.42, tHoldEnd = tLow + 0.07, tOff = tHoldEnd + 0.24;
  const tLand = tOff + T;
  const ab = catchAbsorb({ tCatch: tLand, vIn: [0, -vOff, 0], dist: absorb });
  const tStop = ab.tEnd, tUp = tStop + 0.75, duration = tUp + 0.9;
  // pelvis height: keys with exact take-off slope; flight exact; landing exact; then rise with settle
  const yIn = track([
    { t: t0, v: H0 }, { t: tPrep, v: H0 - 0.05 * d.legLen }, { t: tLow, v: H0 - crouch, mode: 'flat' }, { t: tHoldEnd, v: H0 - crouch * 1.03, mode: 'flat' },
    { t: tOff, v: yOff, slope: vOff },
  ]);
  const rise = action({ start: tStop, antic: { dur: 0, amt: 0 }, exec: { dur: 0.55, snap: 1.4 }, follow: { amt: 0.04 }, settle: { dur: 0.6, f: 1.5, z: 0.55 } });
  const yLanded = yOff - absorb;
  const pelvisY = (t) => {
    if (t < tOff) return yIn.at(t);
    if (t < tLand) return yOff + vOff * (t - tOff) - 0.5 * g * (t - tOff) ** 2;
    if (t < tStop) return yOff + ab.offset(t)[1];
    return yLanded + (H0 - yLanded) * rise.at(t);
  };
  // forward lean of the trunk and arm swing (shoulder angle) as keyed channels
  const lean = track([{ t: t0, v: 0.04 }, { t: tLow, v: 0.55, mode: 'flat' }, { t: tOff, v: -0.02 }, { t: tOff + 0.25 * T, v: 0.05 }, { t: tLand, v: 0.18 }, { t: tStop + 0.08, v: 0.6, mode: 'flat' }, { t: tUp, v: 0.04 }]);
  // arm swing: + forward/up, - back (radians of the arm from hanging)
  const arm = track([{ t: t0, v: 0 }, { t: tPrep, v: 0.5 }, { t: tLow, v: -0.95, mode: 'flat' }, { t: tOff - 0.02, v: 2.4 }, { t: tOff + 0.3 * T, v: 2.6, mode: 'flat' }, { t: tLand - 0.05, v: 1.0 }, { t: tStop + 0.1, v: 0.35 }, { t: tUp + 0.15, v: 0 }]);
  const feet = base.legs.map((L) => ({ ...L }));
  const ballW = feet.map((L) => add([L.ankle[0], 0, L.ankle[2]], mv(ry(L.heading), [pr.foot.ball[0], 0, pr.foot.ball[2]])));
  function legsAt(t, rootY) {
    return feet.map((L, i) => {
      // heel peel before take-off (pivot on the ball), toes pointed in the air, balls first at landing
      if (t < tOff) {
        const pitch = 0.75 * smooth01(t, tOff - 0.16, tOff);
        return { ...L, ankle: pitch > 0 ? ankleFromPivot(ballW[i], pr.foot.ball, L.heading, pitch) : L.ankle, pitch, plantW: 1 };
      }
      if (t >= tLand) {
        const pitch = 0.6 * (1 - smooth01(t, tLand, tLand + 0.09));
        return { ...L, ankle: ankleFromPivot(ballW[i], pr.foot.ball, L.heading, pitch), pitch, plantW: 1 };
      }
      // in the air: the feet hang from the pelvis, tuck up, then reach for the floor
      const u = (t - tOff) / T;
      const a0 = ankleFromPivot(ballW[i], pr.foot.ball, L.heading, 0.75), a1 = ankleFromPivot(ballW[i], pr.foot.ball, L.heading, 0.6);
      const rel0 = sub(a0, [0, yOff, 0]), rel1 = sub(a1, [0, yOff, 0]);
      const tuck = 0.28 * d.legLen * Math.sin(Math.PI * u) ** 1.5;
      const rel = [0, 1, 2].map((k) => rel0[k] + (rel1[k] - rel0[k]) * ease.smoother(u));
      rel[1] += tuck; rel[2] += 0;
      const fwd = mv(ry(yaw), [0, 0, 0.12 * tuck]);
      return { ...L, ankle: add(add([0, rootY, 0], rel), fwd), pitch: 0.75 + (0.6 - 0.75) * u + 0.2 * Math.sin(Math.PI * u), plantW: 1 - ease.smooth(clamp(u / 0.25, 0, 1)) * (1 - ease.smooth(clamp((u - 0.75) / 0.25, 0, 1))), toe: 0.2 * Math.sin(Math.PI * u) };
    });
  }
  function poseAt(t) {
    const pose = JSON.parse(JSON.stringify(base));
    const y = pelvisY(t);
    const ln = lean.at(t);
    // hips move back as the trunk leans (the centre of mass stays over the feet)
    pose.root.p = add([o[0], y, o[2]], mv(ry(yaw), [0, 0, -0.22 * d.legLen * Math.max(0, ln)]));
    pose.spine = [0.04 + ln * 0.75, 0, 0]; pose.neck = [-ln * 0.45, 0, 0];
    pose.root.tilt = [ln * 0.35, 0];
    pose.legs = legsAt(t, y);
    const a = arm.at(t);
    pose.arms = SIDE.map((s) => {
      const A = hangArm(pr, s);
      const sh = sub(d.shoulder, d.chest);
      const L = d.armLen * 0.94;
      // the arm swings in the sagittal plane about the shoulder (chest space), elbows soften mid-swing
      A.specs = [{ space: 'chest', p: [s * (sh[0] + 6), sh[1] - L * Math.cos(a), sh[2] + L * Math.sin(a) * 0.95] }];
      A.flex = 0.1 + 0.25 * Math.max(0, Math.sin(a));
      A.curl = a > 1.5 ? [0.05, 0.1, 0.15, 0.2] : [0.35, 0.4, 0.45, 0.5];
      A.spread = a > 1.5 ? 0.8 : 0.3;
      return A;
    });
    pose.face = { jaw: t > tOff && t < tLand ? 0.5 : 0.12, look: [0, t > tOff && t < tLand ? 0.3 : 0], pupil: 1 };
    pose.props = { hat: { mode: 'head' } };
    return pose;
  }
  const phases = [{ name: 'prep', t0, t1: tPrep }, { name: 'antic', t0: tPrep, t1: tHoldEnd }, { name: 'exec', t0: tHoldEnd, t1: tLand },
    { name: 'follow', t0: tLand, t1: tStop + 0.1 }, { name: 'settle', t0: tStop + 0.1, t1: tUp + 0.6 }];
  const trail = (t) => {
    if (t < tOff) return null;
    const pts = [], dots = [];
    for (let s = 0; s <= T + 1e-9; s += 1 / 120) pts.push([o[0], yOff + vOff * s - 0.5 * g * s * s, o[2]]);
    for (let s = 0; s <= Math.min(t, tLand) - tOff + 1e-9; s += 1 / 12) dots.push([o[0], yOff + vOff * s - 0.5 * g * s * s, o[2]]);
    return { pts, dots };
  };
  return { duration, poseAt, phases, trail, tOff, tLand, vOff, T, h, pelvisY, yOff, impulses: [{ t: tLand, ribs: 1.0, hat: -40, jaw: -5 }], events: [{ t: tOff, kind: 'whoosh' }, { t: tLand, kind: 'land' }] };
}

// ------------------------------------------------------------------ the pirouette
// Wind up (twist the other way), push off with the right foot, spin on the ball of the left foot with
// the arms out, pull them in (moment of inertia drops, omega rises: L = I omega constant), open them
// again (it slows), put the right foot down to stop, a wobble, settle. I(t) is computed from the
// skeleton's own bones (mass proportional to bone volume, 12 kg in all) at each arm position.
export function pirouette(char, p = {}) {
  const pr = char.profile, d = pr.dims, K = pr.K;
  const yaw0 = p.yaw ?? 0.2, o = [p.x ?? 0, 0, p.z ?? 0];
  const base = standPose(pr, { x: o[0], z: o[2], yaw: yaw0, toeOut: 0.2 });
  const tWind = 0.6, tPush = 1.25, tSpin0 = 1.55, tIn0 = 2.6, tIn1 = 3.0, tOut0 = 4.1, tOut1 = 4.5, tStop = 5.4;
  const omega0Req = p.omega0 ?? 2 * Math.PI * 0.9; // rad/s with the arms open (adjusted to land square)
  // arm extension u: 1 = arms out to the sides, 0 = folded on the chest
  const armU = (t) => (t < tSpin0 ? smooth01(t, tWind, tSpin0) : t < tOut0 ? 1 - smooth01(t, tIn0, tIn1) : smooth01(t, tOut0, tOut1));
  const armSpec = (s, u) => {
    const sh = sub(d.shoulder, d.chest);
    const out = [s * (sh[0] + d.armLen * 0.92), sh[1] - 4, sh[2] + 6];
    const fold = [s * -6, sh[1] - 36, sh[2] + 26];
    return [0, 1, 2].map((k) => fold[k] + (out[k] - fold[k]) * u);
  };
  // body on one foot: pivot on the left ball, right foot drawn up to the left knee (retire)
  const leftBall = add([base.legs[1].ankle[0], 0, base.legs[1].ankle[2]], mv(ry(base.legs[1].heading), [pr.foot.ball[0], 0, pr.foot.ball[2]]));
  const pivot = [leftBall[0], 0, leftBall[2]];
  // pose with yaw angle `ang` about the pivot, arm extension u, on-one-foot weight w (0..1)
  function spinPose(ang, u, w, twist = 0) {
    const pose = JSON.parse(JSON.stringify(base));
    // weight over the pivot foot: the pelvis moves above it and rises onto the ball
    const pivLocal = mv(ry(-yaw0), sub(pivot, [o[0], 0, o[2]]));
    const rootLocal = [pivLocal[0] * w * 0.9, base.root.p[1] + 9 * w, pivLocal[2] * w * 0.6];
    const R = ry(ang);
    pose.root.p = add(pivot, mv(R, sub(rootLocal, pivLocal)));
    pose.root.yaw = yaw0 + ang + twist;
    const relaxX = 0;
    void relaxX;
    // left foot on its ball, heel up, turning with the body
    const hd = base.legs[1].heading + ang;
    const pitch = 0.55 * w;
    pose.legs[1] = { ...base.legs[1], ankle: ankleFromPivot(pivot, pr.foot.ball, hd, pitch), heading: hd, pitch, plantW: 1 };
    // right foot: from its plant up to the side of the left knee
    const kneeH = 0.55 * d.legLen;
    const rk = add(pose.root.p, mv(ry(yaw0 + ang), [-14, kneeH - pose.root.p[1] + 8, 14]));
    const rPlant = base.legs[0].ankle;
    const a = w > 0 ? [0, 1, 2].map((k) => rPlant[k] + (rk[k] - rPlant[k]) * w) : rPlant;
    pose.legs[0] = { ...base.legs[0], ankle: a, heading: base.legs[0].heading + wrapPi(ang) * w, pitch: 0.9 * w, plantW: 1 - w, kneeOut: 0.25 + 0.9 * w, toe: 0.3 * w };
    pose.arms = SIDE.map((s) => ({ ...hangArm(pr, s), specs: [{ space: 'chest', p: armSpec(s, u) }], pole: [s * 0.3, -0.9, -0.3], curl: [0.1, 0.15, 0.2, 0.25], spread: 0.7, pron: 0.1 + 0.3 * (1 - u), flex: 0.05 }));
    pose.spine = [0.0, 0, 0]; pose.neck = [-0.05, 0, 0];
    pose.props = { hat: { mode: 'head' } };
    pose.face = { jaw: 0.2, look: [0, 0], pupil: 1 };
    return pose;
  }
  // moment of inertia about the vertical axis through the pivot, as a function of arm extension
  const model = char.model;
  const masses = model.defs.map((dd) => (dd.bone ? partsVolume(dd) : 0));
  const mTot = masses.reduce((a, b) => a + b, 0);
  const KG = 12 / mTot;
  const Igrid = [];
  for (let k = 0; k <= 20; k++) {
    const u = k / 20;
    const pose = spinPose(0, u, 1);
    const { ev, c } = char.evaluatePose(pose);
    const objs = objectFrames(model, ev, c);
    let I = 0;
    for (const ob of objs) { const m = masses[ob.def.uid] * KG; if (!m) continue; const dx = ob.ctr[0] - pivot[0], dz = ob.ctr[2] - pivot[2]; I += m * ((dx * dx + dz * dz) / (K * K)); }
    Igrid.push(I);
  }
  const Iof = (u) => { const f = clamp(u, 0, 1) * 20, i = Math.min(19, Math.floor(f)); return Igrid[i] + (Igrid[i + 1] - Igrid[i]) * (f - i); };
  // spin-up during the push (constant angular acceleration), free spin (L constant), braked stop
  const tFree = tSpin0;
  const windAng = -0.5; // anticipation: twist the other way first
  const BRAKE = 2 * Math.PI * 0.35; // braking angle (constant deceleration)
  // total turn as a function of omega0 is affine (omega(t) = omega0 I0 / I(t)); pick omega0 near the
  // requested value so that he ends facing where he started (a whole number of turns)
  const totalFor = (w0) => { const f = spinConserving({ I: (t) => Iof(armU(t)), omega0: w0, t0: tFree, t1: tStop, angle0: 0.5 * w0 * (tFree - tPush) }); return f.angle(tStop) + BRAKE; };
  const A1 = totalFor(1), A2 = totalFor(2), slope = A2 - A1, icpt = A1 - slope;
  const turns = Math.round((slope * omega0Req + icpt) / (2 * Math.PI));
  const omega0 = (2 * Math.PI * turns - icpt) / slope;
  const alphaUp = omega0 / (tFree - tPush);
  const angAtFree = 0.5 * alphaUp * (tFree - tPush) ** 2;
  const free = spinConserving({ I: (t) => Iof(armU(t)), omega0, t0: tFree, t1: tStop, angle0: angAtFree });
  const wStop = free.omega(tStop);
  const tRest = tStop + (2 * BRAKE) / wStop;
  const beta = wStop / (tRest - tStop);
  // spin angle of the whole body about the pivot (0 until the push); the wind-up is a trunk twist on top
  const angle = (t) => {
    if (t < tPush) return 0;
    if (t < tFree) return 0.5 * alphaUp * (t - tPush) ** 2;
    if (t < tStop) return free.angle(t);
    const u = Math.min(t, tRest) - tStop;
    return free.angle(tStop) + wStop * u - 0.5 * beta * u * u;
  };
  const twistAt = (t) => windAng * smooth01(t, tWind, tPush - 0.05) * (1 - smooth01(t, tPush, tPush + 0.3));
  const duration = tRest + 1.3;
  // the stop must leave him facing the camera-ish: we only report, the spin is physics-first
  function poseAt(t) {
    const w = t < tPush ? smooth01(t, tWind + 0.2, tPush) : t < tRest ? 1 : 1 - smooth01(t, tRest, tRest + 0.45);
    const pose = spinPose(angle(t), armU(t < tStop ? t : tStop) * (t < tRest ? 1 : 1 - 0.5 * smooth01(t, tRest, tRest + 0.6)), w, twistAt(t));
    pose.spine[2] = -0.25 * smooth01(t, tWind, tPush - 0.1) * (1 - smooth01(t, tPush, tPush + 0.3));
    pose.root.p[1] -= 10 * Math.sin(Math.PI * smooth01(t, tWind, tPush));
    if (t > tRest) { const r = pulse(t - tRest, 2.2, 0.3); pose.root.tilt = [0, 0.05 * r]; pose.spine[1] += 0.06 * r; }
    return pose;
  }
  const phases = [{ name: 'prep', t0: 0.3, t1: tWind }, { name: 'antic', t0: tWind, t1: tPush }, { name: 'exec', t0: tPush, t1: tStop }, { name: 'follow', t0: tStop, t1: tRest }, { name: 'settle', t0: tRest, t1: tRest + 1.0 }];
  return { duration, poseAt, phases, Iof, Igrid, turns, omega0, tRest, omega: (t) => (t < tFree ? 0 : t < tStop ? free.omega(t) : Math.max(0, wStop - beta * (t - tStop))), L: free.L, I: (t) => Iof(armU(t)), armU, tIn0, tIn1, tOut0, tStop, tFree, impulses: [{ t: tRest, hat: 30, ribs: 0.6 }] };
}

// volume of a bone's parts (u^3): mass is taken proportional to it
export function partsVolume(d) {
  const parts = d.pieces ? d.pieces.flat() : d.parts || [];
  let v = 0;
  for (const pt of parts) {
    if (pt.t === 'sph') v += (4 / 3) * Math.PI * pt.r ** 3;
    else if (pt.t === 'cap') { const L = len(sub(pt.b, pt.a)); const r = (pt.ra + pt.rb) / 2; v += Math.PI * r * r * L + (2 / 3) * Math.PI * (pt.ra ** 3 + pt.rb ** 3) / 2; }
    else if (pt.t === 'cyl') v += Math.PI * pt.r * pt.r * len(sub(pt.b, pt.a));
    else if (pt.t === 'ell') v += (4 / 3) * Math.PI * pt.r[0] * pt.r[1] * pt.r[2] * 0.25; // the cranium is a shell
    else if (pt.t === 'poly') v += 60;
  }
  return v;
}
void hermite; void projectile; void flatFoot; void toWorld; void rx; void mm; void norm; void fapp;
