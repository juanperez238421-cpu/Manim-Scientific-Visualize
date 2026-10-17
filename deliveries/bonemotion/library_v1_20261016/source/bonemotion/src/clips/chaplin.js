// The Chaplin set: the tramp shuffle with a bone cane, the hat tip, the hat flip, the doff-and-bow and
// the one-foot skid around a corner. Mannerisms only (feet out, stiff knees, waddle, cane flourishes,
// hat business); the character is Mr. Bones in his own costume.
//
// Props lead, hands follow: the cane and the hat are animated as objects (exact contacts with the floor
// and the head), and the hand IK targets are taken from their grips.
import { gait } from './locomotion.js';
import { track, ease, clamp, hermite, hermiteD } from '../core/curves.js';
import { add, sub, scl, norm, mv, ry, rx, rz, mm, len, frameAlong, fmul, ftr, frot, fapp, cross } from '../core/m3.js';
import { SIDE, toWorld, fwdOf, leftOf } from '../core/body.js';

export const CANE_LEN = 150; // grip -> floor contact (tip), u

// ------------------------------------------------------------------ the walk with the cane
export function chaplinWalk(char, p = {}) {
  const pr = char.profile || char;
  const g = gait(pr, { style: 'chaplin', yaw: p.yaw ?? 0.95, x: p.x ?? -500, z: p.z ?? 40, steps: p.steps ?? 12, t0: p.t0 ?? 0.9, first: 1 });
  const F = g.F, Lf = g.Lf;
  const rightStrikes = g.strikes.filter((s) => s.i === 0);
  const twirlEvery = p.twirlEvery ?? 2;
  // cane contacts: the tip lands ahead of / outside the right foot at its heel strike, and stays put
  const contacts = rightStrikes.map((s, j) => {
    const T = add(add(g.groundOf(0, s.S), scl(F, 30)), scl(Lf, -26));
    return { t0: s.ts - 0.05, t1: s.ts + 0.13, T, j, last: j === rightStrikes.length - 1 };
  });
  const tipUp = (psi) => norm(add(scl([0, 1, 0], Math.cos(psi)), scl(F, -Math.sin(psi)))); // grip direction from the tip
  const gripIn = (c, t) => {
    const u = clamp((t - c.t0) / (c.t1 - c.t0), 0, 1);
    const psi = 0.1 - 0.16 * u; // the body vaults over the planted cane
    return add(c.T, scl(tipUp(psi), CANE_LEN));
  };
  // the cane while carried (before the first contact / after the last): hanging, swinging with the arm
  const carried = (t) => {
    const pose = g.poseAt(t);
    const base = toWorld(pose.root.p, g.yaw, [-56, 20, 14]);
    const sw = 0.12 * Math.sin(2 * Math.PI * 0.8 * t);
    const dir = norm(add(scl([0, -1, 0], Math.cos(0.18 + sw)), scl(F, Math.sin(0.18 + sw))));
    return { G: base, dir };
  };
  const num = (f, t, e = 1e-3) => scl(sub(f(t + e), f(t - e)), 1 / (2 * e));
  function caneAt(t) {
    // contact
    for (const c of contacts) if (t >= c.t0 && t <= c.t1) { const G = gripIn(c, t); return { G, dir: norm(sub(c.T, G)), contact: c }; }
    // between two contacts: a swing (or a twirl every `twirlEvery` strides)
    for (let k = 0; k < contacts.length - 1; k++) {
      const a = contacts[k], b = contacts[k + 1];
      if (t > a.t1 && t < b.t0) {
        const h = b.t0 - a.t1, u = (t - a.t1) / h;
        const Ga = gripIn(a, a.t1), Gb = gripIn(b, b.t0);
        const va = num((x) => gripIn(a, x), a.t1), vb = num((x) => gripIn(b, x), b.t0);
        const twirl = (k + 1) % twirlEvery === 0;
        const G = [0, 1, 2].map((i) => hermite(Ga[i], Gb[i], va[i] * h, vb[i] * h, u));
        const bump = 16 * u * u * (1 - u) * (1 - u);
        const lift = twirl ? 62 : 8;
        G[1] += lift * bump;
        const out = scl(Lf, -(twirl ? 22 : 6) * bump);
        const Gw = add(G, out);
        // angle of the cane in its swing plane, measured from straight down, + = tip forward
        const ang = (G0, T) => { const d = norm(sub(T, G0)); return Math.atan2(d[0] * F[0] + d[2] * F[2], -d[1]); };
        const pa = ang(Ga, a.T), pb = ang(Gb, b.T);
        let phi;
        if (twirl) {
          // a forward flourish: wind back a touch (anticipation), then a full turn, slowing into the tap
          const e = ease.smoother(u);
          phi = pa + (pb + 2 * Math.PI - pa) * e - 0.35 * Math.sin(Math.PI * Math.min(1, u / 0.25)) * (u < 0.25 ? 1 : 0);
        } else {
          // a plain swing: the tip trails behind the moving hand (drag), then whips forward to the tap
          phi = pa + (pb - pa) * ease.smoother(u) - 0.55 * bump;
        }
        const tilt = twirl ? 0.25 * bump : 0; // the twirl's plane leans outward, clear of the forearm
        const plane = norm(add(scl([0, -1, 0], 1), scl(Lf, Math.tan(tilt))));
        const dir = norm(add(scl(plane, Math.cos(phi)), scl(F, Math.sin(phi))));
        return { G: Gw, dir };
      }
    }
    const first = contacts[0], last = contacts[contacts.length - 1];
    // walking in: blend from carried to the first contact; walking out: lift off and carry
    if (t < first.t0) {
      const k = clamp((t - (first.t0 - 0.5)) / 0.5, 0, 1), e = ease.smoother(k);
      const A = carried(t), B = { G: gripIn(first, first.t0), dir: norm(sub(first.T, gripIn(first, first.t0))) };
      return { G: add(scl(A.G, 1 - e), scl(B.G, e)), dir: norm(add(scl(A.dir, 1 - e), scl(B.dir, e))) };
    }
    const k = clamp((t - last.t1) / 0.5, 0, 1), e = ease.smoother(k);
    const A = { G: gripIn(last, last.t1), dir: norm(sub(last.T, gripIn(last, last.t1))) }, B = carried(t);
    return { G: add(scl(A.G, 1 - e), scl(B.G, e)), dir: norm(add(scl(A.dir, 1 - e), scl(B.dir, e))) };
  }
  const duration = g.tStop + 0.6;
  function poseAt(t) {
    const pose = g.poseAt(t);
    const cn = caneAt(t);
    const F3 = frameAlong(cn.G, cn.dir, F);
    pose.props.cane = { F: F3, tip: add(cn.G, scl(cn.dir, CANE_LEN)), contact: !!cn.contact };
    // right hand on the cane: the wrist continues the cane axis above the fist
    pose.arms[0] = { specs: [{ space: 'world', p: sub(cn.G, scl(cn.dir, 11)) }], pole: [-0.9, -0.1, -0.5], curl: [0.95, 1, 1, 1], spread: 0.1, pron: 0.5, flex: 0.15, dev: 0 };
    // left arm: loose swing, elbow out, a little flourish of the wrist
    pose.arms[1].pole = [0.9, -0.2, -0.4];
    pose.arms[1].specs[0].p = add(pose.arms[1].specs[0].p, [14, 10, 4]);
    pose.arms[1].flex = 0.35; pose.arms[1].curl = [0.15, 0.3, 0.45, 0.6]; pose.arms[1].spread = 0.6;
    // jaunty head: tilts with the hips, chin up
    pose.neck = [pose.neck[0] - 0.08, pose.neck[1] - pose.root.tilt[1] * 1.2, pose.neck[2]];
    pose.face = { jaw: 0.14, look: [0.25, 0.1], pupil: 1 };
    return pose;
  }
  return { duration, poseAt, phases: g.phases, gait: g, contacts, caneAt, impulses: [] };
}

// ------------------------------------------------------------------ the hat tip (a layer on any pose)
// The hand rises to the brim (prep), the hat is pressed down a touch (anticipation, the hat squashes),
// snaps up and tips forward while the head nods (the head lags the hand: overlapping action), hangs
// in a moving hold, and comes back down onto the head with a small settle.
import { action } from '../core/principles.js';
import { arcPoint } from '../core/curves.js';
import { HAT_SEAT } from '../characters/mrbones/index.js';

export function hatTipLayer(char, t0, { side = 0, lift = 24, pitch = 0.5, hold = 0.5, nod = 0.22 } = {}) {
  const up = action({ start: t0, prep: 0.36, antic: { dur: 0.16, amt: 0.22 }, hold: 0.05, exec: { dur: 0.2, snap: 2.0 }, follow: { dur: 0.1 }, settle: { dur: 0.45, f: 2, z: 0.55 } });
  const tDown = up.tOver + hold;
  const down = action({ start: tDown, antic: { dur: 0.12, amt: 0.1 }, exec: { dur: 0.2, snap: 1.6 }, follow: { dur: 0.06 }, settle: { dur: 0.5, f: 3, z: 0.4 } });
  const v = (t) => up.at(t) - down.at(t);
  const tGrip = t0 + 0.36, tLet = down.tOver + 0.04, tBack = tLet + 0.45;
  const s = SIDE[side];
  const hatLocal = (vv) => ({ lift: lift * vv, pitch: pitch * Math.max(-0.2, vv), tilt: -0.12 * vv, fwd: 4 * vv });
  function apply(pose, t, ev0) {
    if (t < t0 || t > tBack + 0.01) return pose;
    const ev = ev0 || char.evaluatePose(pose).ev;
    const vv = v(t);
    const vn = v(t - 0.07); // the head follows the hand a beat later
    const hp = hatLocal(vv);
    const held = t >= tGrip && t <= tLet;
    pose.props.hat = { mode: 'head', ...hp, held: t >= tGrip - 0.02 && t <= tLet + 0.02, squash: 1 + 0.35 * Math.min(0, vv) + 0.06 * Math.max(0, Math.min(1, up.vel(t) / 12)) };
    pose.neck = [pose.neck[0] + nod * vn, pose.neck[1], pose.neck[2] - 0.1 * vn];
    pose.spine = [pose.spine[0] + 0.07 * vn, pose.spine[1], pose.spine[2]];
    // grip on the brim (hat frame), world
    const Hf = fmul(ev.fr.head, fmul(ftr([HAT_SEAT[0], HAT_SEAT[1] + hp.lift, HAT_SEAT[2] + hp.fwd]), frot(mm(rz(-0.1 + hp.tilt), rx(hp.pitch)))));
    const grip = fapp(Hf, [s * 20, 5, 33]); // front brim, toward his hand
    const wristAtGrip = add(grip, mv(Hf.R, [s * 5, -9, 13]));
    const rest = ev.J[`wrist${side === 0 ? 'R' : 'L'}`];
    let W;
    if (t < tGrip) W = arcPoint(rest, wristAtGrip, mv(ev.fr.head.R, [s * 18, -10, 58]), ease.smoother((t - t0) / (tGrip - t0)));
    else if (held) W = wristAtGrip;
    else W = arcPoint(wristAtGrip, rest, mv(ev.fr.head.R, [s * 18, -10, 52]), ease.smoother((t - tLet) / (tBack - tLet)));
    const A = pose.arms[side];
    const hk = t < tGrip ? ease.smoother((t - t0) / (tGrip - t0)) : held ? 1 : 1 - ease.smoother((t - tLet) / (tBack - tLet));
    pose.arms[side] = { ...A, specs: [{ space: 'world', p: W }], pole: [s * 0.8, -0.55, 0.25], curl: [0.2 + 0.5 * hk, 0.25 + 0.55 * hk, 0.3 + 0.55 * hk, 0.35 + 0.5 * hk], spread: 0.3, pron: 0.3 + 0.4 * hk, flex: -0.3 * hk + 0.1, dev: 0 };
    pose.face = { ...(pose.face || {}), jaw: 0.12 + 0.18 * Math.max(0, vv) };
    return pose;
  }
  const phases = [...up.phases.map((p) => ({ ...p })), ...down.phases.filter((p) => p.name !== 'antic').map((p) => ({ ...p }))];
  return { apply, up, down, tEnd: tBack, phases, tGrip, tLet };
}

export function hatTip(char, p = {}) {
  const pr = char.profile;
  const yaw = p.yaw ?? 0.35;
  const base = standPose(pr, { x: p.x ?? 0, z: p.z ?? 20, yaw, toeOut: 0.6 });
  const tip = hatTipLayer(char, 0.8, {});
  const duration = tip.tEnd + 0.9;
  function poseAt(t) {
    const pose = JSON.parse(JSON.stringify(base));
    // a breathing idle underneath
    pose.spine[0] += 0.015 * Math.sin(2 * Math.PI * 0.35 * t);
    pose.root.p[1] -= 1.2 * Math.sin(2 * Math.PI * 0.35 * t);
    pose.face.look = [0.1, 0.05];
    return tip.apply(pose, t);
  }
  return { duration, poseAt, phases: tip.phases, impulses: [{ t: tip.tLet + 0.05, hat: 60 }] };
}
import { standPose } from '../core/body.js';

// ------------------------------------------------------------------ the hat flip
// Off the head, down to the chest, a dip (anticipation), a flick: the hat leaves the hand at exactly
// the velocity and spin that carry it, in free flight (constant spin, parabola), onto the head.
import { track as trackK } from '../core/curves.js';
import { launchVelocity, projectile as projK } from '../core/physics.js';
import { pulse as pulseK } from './kit.js';
import { rotAxis as rotAxisK, slerpR as slerpRK } from '../core/m3.js';

export function hatFlip(char, p = {}) {
  const pr = char.profile, g = pr.g;
  const yaw = p.yaw ?? 0.45, o = [p.x ?? 0, 0, p.z ?? 20];
  const base = standPose(pr, { x: o[0], z: o[2], yaw, toeOut: 0.55 });
  const Fw = [Math.sin(yaw), 0, Math.cos(yaw)], Lw = [Math.cos(yaw), 0, -Math.sin(yaw)];
  const t0 = 0.6, tLift = t0 + 0.5, tHold = tLift + 0.5, tDip = tHold + 0.28, tRel = tDip + 0.18, T = 0.78, tLand = tRel + T;
  const env = action({ start: tHold - 0.05, antic: { dur: tDip - tHold + 0.05, amt: 0.6 }, exec: { dur: tRel - tDip - 0.06, snap: 2 }, follow: { dur: 0.06 }, settle: { dur: 0.8, f: 1.5, z: 0.6 } });
  function bodyPose(t) {
    const pose = JSON.parse(JSON.stringify(base));
    const u = env.at(t) * (1 - smoothK(t, tRel + 0.1, tRel + 0.8));
    pose.root.p = add(pose.root.p, [0, 2 * u, 0]);
    pose.spine[0] += -0.05 * u;
    // eyes on the hat; the head comes forward to receive it and gives on landing
    const look = smoothK(t, tRel - 0.1, tRel + 0.15) * (1 - smoothK(t, tLand - 0.3, tLand - 0.05));
    pose.neck[0] += -0.25 * look;
    if (t >= tLand) { const r = pulseK(t - tLand, 3, 0.45); pose.neck[0] += 0.1 * r; pose.root.p[1] -= 3 * Math.max(0, r); }
    pose.face = { jaw: 0.12 + 0.25 * look, look: [0, 0.5 * look], pupil: 1 };
    return pose;
  }
  const seatOf = (t) => { const ev = char.evaluatePose(bodyPose(t)).ev; return fmul(ev.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1)))); };
  const S0 = seatOf(t0), SL = seatOf(tLand);
  const lat = scl(Lw, -1); // flip axis: the hat's crown goes toward the audience first
  const hold = toWorld(o, yaw, [-14, 198, 84]), dip = toWorld(o, yaw, [-14, 172, 78]), rel = toWorld(o, yaw, [-10, 238, 82]);
  const Vrel = launchVelocity(rel, SL.t, T, g);
  const fly = projK(rel, Vrel, g);
  const phiHold = -0.5, phiDip = -0.85, phiRel = -0.35;
  const omega = (2 * Math.PI - phiRel) / T; // one full forward turn in flight, landing square
  const pos = trackK([{ t: t0, v: S0.t }, { t: tLift, v: add(S0.t, [0, 13, 4]) }, { t: 0.5 * (tLift + tHold), v: toWorld(o, yaw, [-18, 262, 92]) }, { t: tHold, v: hold, mode: 'flat' }, { t: tDip, v: dip, mode: 'flat' }, { t: tRel, v: rel, slope: Vrel }]);
  const phi = trackK([{ t: t0, v: 0 }, { t: tLift, v: -0.15 }, { t: tHold, v: phiHold, mode: 'flat' }, { t: tDip, v: phiDip, mode: 'flat' }, { t: tRel, v: phiRel, slope: omega }]);
  // the hand after release: follows through up along the throw, stops, comes back down
  const handAfter = trackK([{ t: tRel, v: rel, slope: Vrel }, { t: tRel + 0.22, v: add(rel, scl(norm(Vrel), 30)), mode: 'flat' }, { t: tRel + 0.75, v: toWorld(o, yaw, [-50, 140, 14]) }]);
  const hatAt = (t) => {
    if (t < t0) return null;
    if (t < tRel) return { R: mm(rotAxisK(lat, phi.at(t)), S0.R), t: pos.at(t) };
    if (t < tLand) return { R: mm(rotAxisK(lat, phiRel + omega * (t - tRel)), slerpRK(S0.R, SL.R, (t - tRel) / T)), t: fly.at(t - tRel) };
    return null;
  };
  const tBack = tRel + 0.75, duration = tLand + 1.3;
  function poseAt(t) {
    const pose = bodyPose(t);
    const H = hatAt(t);
    if (H) pose.props.hat = { mode: 'world', F: H, squash: t > tRel ? 1.06 : t > tDip && t < tRel ? 1.08 : 1 };
    else pose.props.hat = { mode: 'head', squash: t >= tLand ? 1 - 0.18 * Math.max(0, pulseK(t - tLand, 4, 0.4)) : 1 };
    // right hand: to the brim (prep), carries the hat, releases, follows through, back to rest
    const ev = char.evaluatePose(pose).ev;
    const rest = ev.J.wristR;
    let W = null, k = 0;
    const gripOf = (F) => add(fapp(F, [-36, 3, 4]), mv(ry(yaw), [-6, -8, -10]));
    if (t >= t0 - 0.4 && t < t0) { k = smoothK(t, t0 - 0.4, t0); W = arcPoint(rest, gripOf(S0), mv(ry(yaw), [-16, -10, 58]), k); }
    else if (t >= t0 && t < tRel) { k = 1; W = gripOf(H); }
    else if (t >= tRel && t < tBack) { k = 1 - smoothK(t, tRel + 0.3, tBack); W = add(handAfter.at(t), mv(ry(yaw), [-6, -8, -10])); }
    if (W) {
      const A = pose.arms[0];
      const direct = t < t0; // the approach arc starts at the rest wrist: follow it as is
      pose.arms[0] = { ...A, specs: direct ? [{ space: 'world', p: W }] : [...A.specs.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - k) })), { space: 'world', p: W, w: k }], pole: [-0.9, -0.4, -0.2], curl: t < tRel ? [0.6, 0.7, 0.7, 0.7] : [0.05, 0.1, 0.15, 0.2], spread: t < tRel ? 0.2 : 0.8, pron: 0.35, flex: 0.2 };
    }
    return pose;
  }
  const phases = [{ name: 'prep', t0: t0 - 0.4, t1: tHold }, { name: 'antic', t0: tHold, t1: tDip }, { name: 'exec', t0: tDip, t1: tLand }, { name: 'follow', t0: tLand, t1: tLand + 0.25 }, { name: 'settle', t0: tLand + 0.25, t1: tLand + 1.0 }];
  const trail = (t) => {
    if (t < tRel) return null;
    const pts = [], dots = [];
    for (let s = 0; s <= T + 1e-9; s += 1 / 120) pts.push(fly.at(s));
    for (let s = 0; s <= Math.min(t, tLand) - tRel + 1e-9; s += 1 / 12) dots.push(fly.at(s));
    return { pts, dots };
  };
  return { duration, poseAt, phases, trail, tRel, tLand, Vrel, omega, T, impulses: [{ t: tLand, hat: 50 }], events: [{ t: tRel, kind: 'flick' }, { t: tLand, kind: 'hatland' }] };
}
const smoothK = (t, a, b) => ease.smoother(clamp((t - a) / (b - a), 0, 1));

// ------------------------------------------------------------------ doff and bow
// The hat sweeps off in a wide arc and out to the side; a lift of the chest first (anticipation), then
// the deep bow from the hips — the hips go back so the weight stays over the feet — the right foot
// slides back, the left hand to the waist; on the way up the head comes last (overlapping action).
export function doffBow(char, p = {}) {
  const pr = char.profile, d = pr.dims;
  const yaw = p.yaw ?? 0.25, o = [p.x ?? 0, 0, p.z ?? 20];
  const base = standPose(pr, { x: o[0], z: o[2], yaw, toeOut: 0.5 });
  const t0 = 0.5;
  const bow = action({ start: t0 + 0.5, antic: { dur: 0.35, amt: 0.12 }, hold: 0.08, exec: { dur: 0.45, snap: 1.7 }, follow: { dur: 0.1 }, settle: { dur: 0.5, f: 1.4, z: 0.6 } });
  const tUp = bow.end + 0.3; // moving hold at the bottom
  const up = action({ start: tUp, antic: { dur: 0.15, amt: 0.05 }, exec: { dur: 0.5, snap: 1.5 }, follow: { dur: 0.08 }, settle: { dur: 0.6, f: 1.6, z: 0.55 } });
  const flexOf = (t) => bow.at(t) - up.at(t);
  const BOW = 0.85;
  const stepBack = (t) => smoothK(t, bow.start + 0.1, bow.tHit) * (1 - smoothK(t, up.tHit - 0.1, up.tHit + 0.3));
  function bodyPose(t) {
    const pose = JSON.parse(JSON.stringify(base));
    const f = flexOf(t), fn = flexOf(t - 0.12); // the neck lags on the way down and on the way up
    pose.spine[0] += BOW * f;
    pose.neck[0] += 0.35 * fn - 0.1 * f;
    pose.root.p = add(pose.root.p, mv(ry(yaw), [0, -10 * Math.max(0, f), -0.3 * d.legLen * Math.max(0, f)]));
    pose.root.tilt = [0.32 * Math.max(0, f), 0];
    // right foot slides back on an arc and comes back
    const sb = stepBack(t);
    if (sb > 0) {
      const L = base.legs[0];
      const ballStart = add([L.ankle[0], 0, L.ankle[2]], mv(ry(L.heading), [pr.foot.ball[0], 0, pr.foot.ball[2]]));
      const ballBack = add(ballStart, mv(ry(yaw), [-4, 0, -40]));
      const off = ankleFromPivot(ballStart, pr.foot.ball, L.heading, 0.45); // heel peeled off, toes still down
      const endA = ankleFromPivot(ballBack, pr.foot.ball, L.heading, 0.35);
      if (sb < 0.22) { const pp = 0.45 * ease.smoother(sb / 0.22); pose.legs[0] = { ...L, ankle: ankleFromPivot(ballStart, pr.foot.ball, L.heading, pp), pitch: pp, plantW: 1, toe: 0 }; }
      else {
        const u = (sb - 0.22) / 0.78, e = ease.smoother(u), bump = 16 * u * u * (1 - u) * (1 - u);
        const a = add([0, 1, 2].map((k) => off[k] + (endA[k] - off[k]) * e), [0, 10 * bump, 0]);
        pose.legs[0] = { ...L, ankle: a, pitch: 0.45 + (0.35 - 0.45) * e, plantW: 1, toe: 0 };
      }
    }
    // left hand to the waist
    const w = smoothK(t, bow.start, bow.tHit) * (1 - smoothK(t, up.tHit, up.end));
    const A = pose.arms[1];
    pose.arms[1] = { ...A, specs: [...A.specs.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - w) })), { space: 'chest', p: [10, -72, 26], w }], pole: [0.9, -0.2, -0.2], curl: [0.1, 0.1, 0.15, 0.2], spread: 0.2, pron: 0.6 };
    pose.face = { jaw: 0.1 + 0.25 * Math.max(0, f), look: [0, -0.3 * Math.max(0, f)], pupil: 1 };
    return pose;
  }
  // the hat: lifted off, swept out to the side (brim held, crown to the audience), and back on
  const tOff0 = t0, tOff1 = t0 + 0.45, tSw = bow.tHit, tRet0 = up.start + 0.1, tRet1 = up.tHit + 0.25;
  let S0 = null;
  const hatPath = (t, ev) => {
    if (!S0) { const e0 = char.evaluatePose(bodyPose(tOff0)).ev; S0 = fmul(e0.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1)))); }
    const seatNow = fmul(ev.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1))));
    const out = { R: mm(ev.fr.chest.R, mm(rz(-1.3), rx(-0.4))), t: fapp(ev.fr.chest, [-112, -34, 34]) };
    const lifted = { R: S0.R, t: add(S0.t, [0, 12, 8]) };
    if (t < tOff1) { const u = smoothK(t, tOff0, tOff1); return { R: S0.R, t: arcPoint(S0.t, lifted.t, [0, 0, 0], u) }; }
    if (t < tSw) { const u = smoothK(t, tOff1, tSw); return { R: slerpRK(lifted.R, out.R, u), t: arcPoint(lifted.t, out.t, mv(ry(yaw), [-22, 16, 26]), u) }; }
    if (t < tRet0) return out;
    if (t < tRet1) { const u = smoothK(t, tRet0, tRet1); return { R: slerpRK(out.R, seatNow.R, u), t: arcPoint(out.t, seatNow.t, mv(ry(yaw), [-24, 18, 26]), u) }; }
    return null;
  };
  const duration = up.end + 0.6;
  function poseAt(t) {
    const pose = bodyPose(t);
    const ev = char.evaluatePose(pose).ev;
    const H = t >= tOff0 ? hatPath(t, ev) : null;
    const rest = ev.J.wristR;
    let k = 0, W = null;
    const gripOf = (F) => add(fapp(F, [-34, 3, 8]), mv(F.R, [-4, -6, 6]));
    if (H) { pose.props.hat = { mode: 'world', F: H }; k = 1; W = gripOf(H); }
    else pose.props.hat = { mode: 'head', squash: t > tRet1 ? 1 - 0.12 * Math.max(0, pulseK(t - tRet1, 4, 0.4)) : 1 };
    if (t >= tOff0 - 0.4 && t < tOff0) { const e0 = char.evaluatePose(bodyPose(tOff0)).ev; const S = fmul(e0.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1)))); k = smoothK(t, tOff0 - 0.4, tOff0); W = arcPoint(rest, gripOf(S), mv(ry(yaw), [-16, -10, 58]), k); }
    if (t >= tRet1 && t < tRet1 + 0.45) { k = 1 - smoothK(t, tRet1, tRet1 + 0.45); const e1 = char.evaluatePose(bodyPose(tRet1)).ev; const S = fmul(e1.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1)))); W = gripOf(S); }
    if (W) {
      const A = pose.arms[0];
      const direct = t < tOff0 || t >= tRet1; // approach and return arcs start/end at the rest wrist
      pose.arms[0] = { ...A, specs: direct ? [{ space: 'world', p: t < tOff0 ? W : arcPoint(W, rest, mv(ry(yaw), [-16, -10, 52]), 1 - k) }] : [...A.specs.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - k) })), { space: 'world', p: W, w: k }], pole: [-0.9, -0.4, -0.1], curl: [0.55, 0.65, 0.7, 0.7], spread: 0.25, pron: 0.4, flex: 0.1 };
    }
    return pose;
  }
  const phases = [{ name: 'prep', t0: t0 - 0.4, t1: bow.start }, ...bow.phases, ...up.phases.filter((q) => q.name !== 'antic')];
  return { duration, poseAt, phases, impulses: [{ t: tRet1, hat: 40 }, { t: bow.tHit, ribs: 0.5 }], events: [{ t: tRet1, kind: 'hatland' }] };
}
import { ankleFromPivot } from '../core/body.js';

// ------------------------------------------------------------------ the corner hop (Chaplin's skid turn)
// He shuffles in, plants, kicks the right leg out, holds his hat on and hops round on the left foot —
// three hops, the head turning first (it leads the turn), the left arm out for balance — then lands
// on both feet and shuffles off the other way. Each hop is an exact ballistic flight of the pelvis;
// each contact reverses its vertical velocity with constant acceleration (no velocity jumps).
import { mix as mixPose } from '../core/pose.js';
import { armTo } from './kit.js';
export function cornerHop(char, p = {}) {
  const pr = char.profile, g = pr.g, d = pr.dims;
  const yaw1 = p.yaw ?? 1.2;
  const g1 = gait(pr, { style: 'chaplin', yaw: yaw1, x: p.x ?? -420, z: p.z ?? -30, steps: 6, t0: 0.6, first: 1 });
  const end1 = g1.poseAt(g1.tStop);
  const spot = [end1.legs[1].ankle[0], 0, end1.legs[1].ankle[2]]; // the left foot: the hop spot
  // the left foot pivots on its ball (fixed on the floor) while the body turns round
  const ballFixed = add(spot, mv(ry(end1.legs[1].heading), [pr.foot.ball[0], 0, pr.foot.ball[2]]));
  const hdOf = (yw) => end1.legs[1].heading + (yw - yaw1);
  const finalAnkle = ankleFromPivot(ballFixed, pr.foot.ball, hdOf(yaw1 - Math.PI), 0);
  const tH0 = g1.tStop - 0.15; // take over from the walk as it settles
  const tPrep = tH0 + 0.35; // right leg out, weight onto the left foot, crouch (anticipation)
  const nHop = 3, Th = 0.22, Tc = 0.12;
  const vH = (g * Th) / 2; // take-off speed of each hop
  const hops = [];
  for (let k = 0; k < nHop; k++) { const tOff = tPrep + Tc / 2 + k * (Th + Tc); hops.push({ tOff, tLand: tOff + Th }); }
  const tLast = hops[nHop - 1].tLand;
  const tH1 = tLast + 0.45; // both feet down, upright
  const yaw2 = yaw1 - Math.PI;
  const L2 = [Math.cos(yaw2), 0, -Math.sin(yaw2)];
  const lat2 = 0.42 * d.hipW * 1.5;
  const origin2 = sub([finalAnkle[0], 0, finalAnkle[2]], scl(L2, lat2));
  const g2 = gait(pr, { style: 'chaplin', yaw: yaw2, x: origin2[0], z: origin2[2], steps: 6, t0: 0.6, first: 0 });
  const t2 = tH1 - g2.tStart; // gait 2 runs on its own clock shifted by t2
  const start2 = g2.poseAt(g2.tStart);
  // pelvis height during the hops: crouch -> (flight, contact)* -> land
  const yBase = end1.root.p[1] - 6;
  const yT = yBase + (vH * Tc) / 4; // take-off / landing height of the pelvis
  const aC = (2 * vH) / Tc; // contact acceleration: reverses -vH -> +vH in Tc
  const yHop = (t) => {
    if (t < tPrep) return end1.root.p[1] - 6 * ease.smoother(clamp((t - tH0) / (tPrep - tH0), 0, 1));
    for (let k = 0; k < nHop; k++) {
      const h = hops[k];
      if (t < h.tOff) {
        if (k === 0) { const tau = t - tPrep; return yBase + 0.5 * aC * tau * tau; } // from rest
        const tau = t - hops[k - 1].tLand; return yT - vH * tau + 0.5 * aC * tau * tau;
      }
      if (t < h.tLand) { const tau = t - h.tOff; return yT + vH * tau - 0.5 * g * tau * tau; }
    }
    const tau = t - tLast;
    const a = (vH * vH) / (2 * 10); // the last landing absorbed over 10 u
    const T = vH / a;
    if (tau < T) return yT - (vH * tau - 0.5 * a * tau * tau);
    return yT - 10 + (end1.root.p[1] - (yT - 10)) * ease.smoother(clamp((tau - T) / (tH1 - tLast - T), 0, 1));
  };
  // body yaw: turns during the flights, the head leads
  const yawK = [{ t: tH0, v: yaw1 }, { t: tPrep, v: yaw1 + 0.12 }];
  hops.forEach((h, k) => yawK.push({ t: h.tLand, v: yaw1 - (Math.PI * (k + 1)) / nHop, mode: 'free' }));
  yawK[yawK.length - 1].mode = 'flat';
  const yawT = track(yawK);
  const yawAt = (t) => (t < tH0 ? yaw1 : t > tLast ? yaw2 : yawT.at(t));
  function hopPose(t) {
    const pose = JSON.parse(JSON.stringify(end1));
    const yw = yawAt(t);
    const y = yHop(t);
    // pelvis over the left foot
    const w = ease.smoother(clamp((t - tH0) / (tPrep - tH0), 0, 1)) * (1 - ease.smoother(clamp((t - tLast) / (tH1 - tLast), 0, 1)));
    const over = add(spot, mv(ry(yw), [-d.hipW * 0.9, 0, -6]));
    const restXZ = [end1.root.p[0] + (start2.root.p[0] - end1.root.p[0]) * ease.smoother(clamp((t - tPrep) / (tH1 - tPrep), 0, 1)), 0, end1.root.p[2] + (start2.root.p[2] - end1.root.p[2]) * ease.smoother(clamp((t - tPrep) / (tH1 - tPrep), 0, 1))];
    pose.root.p = [restXZ[0] + (over[0] - restXZ[0]) * w, y, restXZ[2] + (over[2] - restXZ[2]) * w];
    pose.root.yaw = yw;
    pose.root.tilt = [0, 0.08 * w];
    // left foot: on the ball through the contacts; in the air it rises with the pelvis
    const hd = hdOf(yw);
    let air = 0;
    for (const h of hops) if (t > h.tOff && t < h.tLand) air = Math.sin(Math.PI * (t - h.tOff) / Th);
    const ballP = ballFixed;
    const pitch = 0.3 * w;
    pose.legs[1] = { ...pose.legs[1], ankle: add(ankleFromPivot(ballP, pr.foot.ball, hd, pitch), [0, 13 * air, 0]), heading: hd, pitch: pitch + 0.2 * air, plantW: 1 - 0.6 * air };
    // right leg kicked out in front, toe up
    const out = add(pose.root.p, mv(ry(yw), [-46, -92, 52]));
    const R0 = end1.legs[0], R1 = start2.legs[0];
    const kick = w;
    const plant = t < tPrep ? R0 : R1;
    const a = [0, 1, 2].map((k) => plant.ankle[k] + (out[k] - plant.ankle[k]) * kick + (k === 1 ? 26 * kick * (1 - kick) * (1 - kick) : 0));
    pose.legs[0] = { ...plant, ankle: a, heading: (t < tPrep ? R0.heading : R1.heading) * (1 - kick) + (yw - 0.9) * kick, pitch: -0.35 * kick, plantW: 1 - kick, kneeOut: 0.6 };
    // hands: right on the crown of the hat, left out for balance (flapping with the hops)
    const ev = char.evaluatePose(pose).ev;
    const brim = fapp(ev.fr.head, [-18, 58, 30]), wr = add(brim, mv(ev.fr.head.R, [-5, -9, 13]));
    pose.arms[0] = { ...armTo(pose.arms[0], wr, w, -1), pole: [-0.8, -0.55, 0.25], curl: [0.55, 0.65, 0.7, 0.7], spread: 0.25, pron: 0.6, flex: -0.2 * w };
    const flap = 0.5 + 0.5 * Math.sin(2 * Math.PI * (t - tPrep) / (Th + Tc));
    pose.arms[1] = { ...pose.arms[1], specs: [...pose.arms[1].specs.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - w) })), { space: 'chest', p: [92, -20 + 22 * flap, 10], w }], pole: [0.2, -0.9, -0.3], curl: [0.05, 0.1, 0.15, 0.2], spread: 0.9 };
    // lean into the turn; the head turns first
    pose.spine = [pose.spine[0], pose.spine[1] + 0.1 * w, pose.spine[2]];
    pose.neck = [pose.neck[0], pose.neck[1], (yawAt(t + 0.22) - yw) * 1.3];
    pose.props.hat = { mode: 'head' };
    pose.face = { jaw: 0.35 * w + 0.1, look: [-0.3 * w, 0], pupil: 1 };
    return pose;
  }
  const duration = t2 + g2.tStop + 0.5;
  function poseAt(t) {
    if (t < tH0) return g1.poseAt(t);
    if (t < tH0 + 0.2) return mixPose(g1.poseAt(t), hopPose(t), ease.smoother((t - tH0) / 0.2));
    if (t < tH1) return hopPose(t);
    if (t < tH1 + 0.2) return mixPose(hopPose(t), g2.poseAt(t - t2), ease.smoother((t - tH1) / 0.2));
    return g2.poseAt(t - t2);
  }
  const phases = [...g1.phases.filter((q) => q.t1 <= tH0), { name: 'prep', t0: tH0, t1: tPrep - 0.1 }, { name: 'antic', t0: tPrep - 0.1, t1: tPrep + Tc / 2 }, { name: 'exec', t0: tPrep + Tc / 2, t1: tLast },
    { name: 'follow', t0: tLast, t1: tLast + 0.2 }, { name: 'settle', t0: tLast + 0.2, t1: tH1 }, ...g2.phases.map((q) => ({ ...q, t0: q.t0 + t2, t1: q.t1 + t2 }))];
  return { duration, poseAt, phases, hops, tH0, tH1, impulses: hops.map((h) => ({ t: h.tLand, ribs: 0.3 })), events: hops.map((h) => ({ t: h.tLand, kind: 'hop' })) };
}
