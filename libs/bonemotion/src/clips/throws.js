// Standing throws with Mr. Bones' own skull: pop it off, drop it from rest, toss it up underhand,
// slam it down overhand onto the floor (it bounces), catch it with "give", put it back on.
//
// How a throw is built (the kinetic chain, proximal to distal):
//   * the skull's path is primary: before release it rides a circle of radius r about the shoulder,
//     with the angle from swingSchedule (constant angular acceleration from rest, exact omega at release)
//   * the release is where the radius points straight forward, so the velocity is exactly vertical,
//     v0 = omega r (the swing plane leans outward to clear the head and hip, and comes back to vertical
//     with zero slope at release, so the tilt does not tilt the velocity)
//   * hips, legs and trunk run their own action envelopes (anticipation = crouch / coil, execution =
//     drive) that PEAK at the release instant with zero velocity: the shoulder is momentarily still, so
//     the release velocity is exactly the arm's; the body then settles while the arm follows through
//   * after release the skull is a projectile (exact), it keeps the angular velocity it had in the hand
//   * a catch: the hands arrive moving with the skull (C1) and stop it over a distance (constant force)
import { standPose, SIDE, toWorld } from '../core/body.js';
import { action } from '../core/principles.js';
import { ease, clamp, hermite, arcPoint } from '../core/curves.js';
import { projectile, swingSchedule, catchAbsorb, bouncing } from '../core/physics.js';
import { add, sub, scl, mv, mm, ry, rx, rz, norm, len, cross, rotAxis, slerpR, fapp, fmul, ftr, frot, I3 } from '../core/m3.js';
import { CM_LOCAL, HAT_SEAT } from '../characters/mrbones/index.js';
import { bothHandsOn, bothHandsUnder, handUnder, pulse, armTo, armBlend } from './kit.js';

const K = 200;
const smooth01 = (t, a, b) => ease.smoother(clamp((t - a) / (b - a), 0, 1));
const hermV = (a, b, va, vb, u) => [0, 1, 2].map((i) => hermite(a[i], b[i], va[i], vb[i], u));
const numVel = (f, t, h = 1e-4) => scl(sub(f(t + h), f(t - h)), 1 / (2 * h));

// ------------------------------------------------------------------ pop the head off / put it back
// Both hands come up (prep), unscrew the skull a quarter (anticipation), POP (exec, overshoot), carry it
// to the chest. The hat rides up with the skull, hangs in the air a beat when the skull is pulled out
// from under it (the cartoon hang), then free-falls onto the neck stump and squashes.
export function popHead(char, t0, { hold, yaw }) {
  const tGrab = t0 + 0.45, tTwist = tGrab + 0.28, tPop = tTwist + 0.12, tPull = tPop + 0.16, tHeld = tPull + 0.55;
  const tHang = tPull + 0.32;
  let cache = null;
  const prepare = (pose) => {
    if (cache) return cache;
    const ev = char.evaluatePose(pose).ev;
    const cm0 = fapp(ev.fr.headAttach, CM_LOCAL);
    const hatF = char.hatFrame({ ...pose, props: { hat: { mode: 'head' } } }, ev, char.ZERO_SEC).F;
    const neckSeat = fmul(ev.fr.headAttach, fmul(ftr([0, 10, -2]), frot(rz(-0.1))));
    cache = { cm0, R0: ev.fr.headAttach.R, hatF, neckSeat };
    return cache;
  };
  const Rhold = ry(yaw);
  function apply(pose, t) {
    if (t < t0) return pose;
    const C = prepare(pose);
    const twist = 0.4 * smooth01(t, tGrab, tTwist) * (1 - smooth01(t, tPull, tHeld));
    let cm, R;
    if (t < tPop) { cm = C.cm0; R = mm(ry(twist), C.R0); }
    else if (t < tPull) {
      const u = (t - tPop) / (tPull - tPop);
      const up = 24 * (1 - (1 - u) ** 3) + 5 * Math.sin(Math.PI * u); // fast out, slight overshoot
      cm = add(C.cm0, [0, up, 0]); R = mm(ry(twist), C.R0);
    } else {
      const u = smooth01(t, tPull, tHeld);
      const a = add(C.cm0, [0, 24, 0]);
      cm = arcPoint(a, hold, mv(Rhold, [0, 18, 26]), u);
      R = slerpR(mm(ry(twist), C.R0), Rhold, u);
    }
    if (t >= tPop) pose.props.skull = { mode: 'free', cm, R };
    // hands: from the rest pose to the sides of the skull
    const w = smooth01(t, t0, tGrab);
    const grips = bothHandsOn(cm, yaw);
    pose.arms = pose.arms.map((A, i) => (w < 1 ? { ...grips[i], specs: armTo(A, grips[i].specs[0].p, w, SIDE[i], { up: 70, fwd: 72 }).specs } : grips[i]));
    // the hat
    if (t < tPull) pose.props.hat = { mode: 'head', held: true };
    else {
      const Hp = add(C.hatF.t, [0, 24, 0]);
      if (t < tHang) pose.props.hat = { mode: 'world', F: { R: C.hatF.R, t: Hp } };
      else {
        const drop = Hp[1] - C.neckSeat.t[1];
        const tf = Math.sqrt((2 * drop) / char.profile.g);
        const tau = t - tHang;
        if (tau < tf) {
          const u = tau / tf;
          pose.props.hat = { mode: 'world', F: { R: slerpR(C.hatF.R, C.neckSeat.R, u), t: add(Hp, [(C.neckSeat.t[0] - Hp[0]) * u, -0.5 * char.profile.g * tau * tau, (C.neckSeat.t[2] - Hp[2]) * u]) } };
        } else pose.props.hat = { mode: 'neck', squash: 1 - 0.25 * Math.max(0, pulse(tau - tf, 4, 0.35)) };
      }
    }
    pose.face = { ...(pose.face || {}), jaw: t > tPop && t < tPull + 0.3 ? 0.6 : 0.15 };
    return pose;
  }
  const phases = [{ name: 'prep', t0, t1: tGrab }, { name: 'antic', t0: tGrab, t1: tPop }, { name: 'exec', t0: tPop, t1: tPull }, { name: 'follow', t0: tPull, t1: tHang + 0.2 }, { name: 'settle', t0: tHang + 0.2, t1: tHeld + 0.2 }];
  return { apply, tEnd: tHeld, tPop, tHang, phases, events: [{ t: tPop, kind: 'pop' }] };
}

// skull from the hands back onto the neck; the hat hops from the stump onto the skull as it arrives
export function headBack(char, t0, { fromCM, fromR, yaw }) {
  const tSeat = t0 + 0.75, tDone = tSeat + 0.4;
  let C = null;
  const Rhold = ry(yaw);
  function apply(pose, t) {
    if (t < t0) return pose;
    if (!C) {
      const ev = char.evaluatePose(pose).ev;
      const cmN = fapp(ev.fr.headAttach, CM_LOCAL);
      const neckSeat = fmul(ev.fr.headAttach, fmul(ftr([0, 10, -2]), frot(rz(-0.1))));
      const headSeat = fmul(ev.fr.headAttach, fmul(ftr(HAT_SEAT), frot(rz(-0.1))));
      C = { cmN, R0: ev.fr.headAttach.R, neckSeat, headSeat };
    }
    const u = smooth01(t, t0, tSeat);
    if (t < tSeat) {
      const cm = arcPoint(fromCM, C.cmN, mv(Rhold, [0, 30, 30]), u);
      pose.props.skull = { mode: 'free', cm, R: slerpR(fromR, C.R0, u) };
      const grips = bothHandsOn(cm, yaw);
      pose.arms = grips;
    } else {
      pose.props.skull = { mode: 'attached' };
      const w = smooth01(t, tSeat + 0.05, tDone + 0.3);
      const grips = bothHandsOn(fapp(char.evaluatePose(pose).ev.fr.headAttach, CM_LOCAL), yaw);
      pose.arms = pose.arms.map((A, i) => ({ ...armBlend(A, grips[i].specs, A.specs, w, SIDE[i], { up: 70, fwd: 72 }), curl: A.curl }));
    }
    // the hat: a little hop from the stump (launch as the skull comes near) onto the skull
    const tL = tSeat - 0.42, T = 0.42;
    if (t < tL) pose.props.hat = { mode: 'neck' };
    else if (t < tSeat) {
      const tau = t - tL, g = char.profile.g;
      const p0 = C.neckSeat.t, p1 = C.headSeat.t;
      const v = [(p1[0] - p0[0]) / T, (p1[1] - p0[1] + 0.5 * g * T * T) / T, (p1[2] - p0[2]) / T];
      pose.props.hat = { mode: 'world', F: { R: slerpR(C.neckSeat.R, C.headSeat.R, tau / T), t: add(add(p0, scl(v, tau)), [0, -0.5 * g * tau * tau, 0]) } };
    } else pose.props.hat = { mode: 'head', squash: 1 - 0.18 * Math.max(0, pulse(t - tSeat, 4, 0.35)) };
    return pose;
  }
  return { apply, tEnd: tDone + 0.35, tSeat, events: [{ t: tSeat, kind: 'click' }] };
}

// ------------------------------------------------------------------ the throw clip
// mode: 'drop' (v0 = 0, from the outstretched hand), 'under' (tossed up), 'over' (slammed down)
export function skullThrow(char, p = {}) {
  const pr = char.profile, g = pr.g;
  const mode = p.mode || 'under';
  const yaw = p.yaw ?? 0.95;
  const o = [p.x ?? -40, 0, p.z ?? 0];
  const F = [Math.sin(yaw), 0, Math.cos(yaw)], Lf = [Math.cos(yaw), 0, -Math.sin(yaw)];
  const v0 = (p.v0 ?? (mode === 'under' ? 3.5 : mode === 'over' ? 5 : 0)) * K;
  const r = 128;
  const base = standPose(pr, { x: o[0], z: o[2], yaw, toeOut: 0.45, width: 1.15 });
  // a staggered stance: left foot forward, right back (right-handed throw)
  base.legs[1].ankle = add(base.legs[1].ankle, scl(F, 18)); base.legs[0].ankle = add(base.legs[0].ankle, scl(F, -10));
  base.props.hat = { mode: 'neck' };
  const hold = toWorld(o, yaw, [0, 192, 80]);
  const withPop = mode === 'drop';
  const pop = withPop ? popHead(char, 0.5, { hold, yaw }) : null;
  const tReady = withPop ? pop.tEnd + 0.15 : 0.6;
  // swing geometry
  const theta0 = mode === 'under' ? -(Math.PI / 2 + 1.0) : mode === 'over' ? Math.PI / 2 + 0.95 : 0;
  const omega = v0 / r;
  const tPrep = 0.75;
  const T = mode === 'drop' ? 0 : (2 * Math.abs(theta0)) / omega;
  const tStart = tReady + tPrep;
  const tRel = mode === 'drop' ? tStart + 0.7 : tStart + T;
  const sw = mode === 'drop' ? null : swingSchedule({ theta0, thetaRel: 0, omegaRel: omega, tRel, dFollow: mode === 'under' ? 1.3 : 1.0 });
  const tilt0 = mode === 'over' ? 0.55 : 0.3;
  // body envelope: peaks (zero velocity) exactly at release
  const anticD = 0.45, execD = mode === 'drop' ? 0.3 : 0.4, follD = 0.14;
  const env = action({ start: tRel - (anticD + 0.06 + execD + follD), antic: { dur: anticD, amt: mode === 'drop' ? 0.3 : 1.3 }, hold: 0.06, exec: { dur: execD, snap: 2.2 }, follow: { dur: follD }, settle: { dur: 0.7, f: 1.4, z: 0.6 } });
  const DELTA = mode === 'under' ? { root: [0, 3, 9], spine: [-0.06, 0, -0.16], neck: [-0.2, 0, 0], tilt: [0, 0.04] }
    : mode === 'over' ? { root: [0, 2, 10], spine: [0.26, 0, -0.22], neck: [0.15, 0, 0], tilt: [0, 0.05] }
      : { root: [0, 2, 3], spine: [0.04, 0, 0], neck: [0.05, 0, 0], tilt: [0, 0] };

  let tCatchB = null; // set once the release geometry is known (the lean never changes the release)
  const LEAN = mode === 'drop' ? { down: 22, fwd: 16, flex: 0.48 } : mode === 'under' ? { down: 20, fwd: 20, flex: 0.44 } : { down: 30, fwd: 22, flex: 0.55 };
  function bodyPose(t) {
    const pose = JSON.parse(JSON.stringify(base));
    // the drive peaks at release, then the body lets go of it (back to neutral, C1)
    const u = env.at(t) * (1 - smooth01(t, tRel + 0.12, tRel + 0.95));
    // reaching for the catch: the body leans in to meet the skull, then straightens (anticipation of the catch)
    const lean = tCatchB === null ? 0 : smooth01(t, Math.max(tRel + 0.05, tCatchB - 0.75), tCatchB - 0.1) * (1 - smooth01(t, tCatchB + 0.35, tCatchB + 1.1));
    pose.root.p = add(pose.root.p, mv(ry(yaw), [0, -LEAN.down * lean, LEAN.fwd * lean]));
    pose.spine[0] += LEAN.flex * lean; pose.neck[0] += 0.15 * lean;
    pose.root.p = add(pose.root.p, mv(ry(yaw), scl(DELTA.root, u)));
    pose.spine = pose.spine.map((x, i) => x + DELTA.spine[i] * u);
    pose.neck = pose.neck.map((x, i) => x + DELTA.neck[i] * u);
    pose.root.tilt = [pose.root.tilt[0], pose.root.tilt[1] + DELTA.tilt[1] * u];
    // look at the skull
    pose.face = { jaw: 0.15, look: [0, 0.2], pupil: 1 };
    return pose;
  }
  // shoulder (circle centre) from the body alone
  const shoulderAt = (t) => char.evaluatePose(bodyPose(t)).ev.J.shoulderR;
  const S_REL = shoulderAt(tRel);
  const dirOf = (th) => {
    const tilt = mode === 'drop' ? 0 : tilt0 * (th / theta0) ** 2;
    const up = norm(add(scl([0, 1, 0], Math.cos(tilt)), scl(Lf, -Math.sin(tilt)))); // leans out to his right
    return norm(add(scl(F, Math.cos(th)), scl(up, Math.sin(th))));
  };
  const swingCM = (t) => add(shoulderAt(t), scl(dirOf(sw ? sw.theta(t) : 0), r));
  const P_REL = add(S_REL, scl(F, r));
  const V0 = mode === 'over' ? [0, -v0, 0] : [0, v0, 0];
  const flight = mode === 'over' ? bouncing(P_REL, V0, g, 44, 0.55, 0.6, 3, 60) : null;
  const proj = projectile(P_REL, V0, g);
  const posFlight = (tau) => (flight ? flight.at(tau) : proj.at(tau));
  const velFlight = (tau) => (flight ? flight.vel(tau) : proj.vel(tau));
  // catch: 'under' and 'drop' at chest height on the way down; 'over' at the top of the first rebound
  let tCatch;
  if (mode === 'over') { const s1 = flight.segs[1]; tCatch = tRel + s1.t0 + s1.pr.apexT; }
  else tCatch = tRel + proj.timeToY(mode === 'drop' ? 200 : 238);
  tCatchB = tCatch;
  const Pc = posFlight(tCatch - tRel), Vc = velFlight(tCatch - tRel);
  const absorb = len(Vc) > 1 ? catchAbsorb({ tCatch, vIn: Vc, dist: mode === 'drop' ? 30 : 42 }) : null;
  const tStill = absorb ? absorb.tEnd : tCatch;
  const tBack = tStill + 0.75;
  const back = mode === 'over' ? headBack(char, tBack + 0.2, { fromCM: hold, fromR: ry(yaw), yaw }) : null;
  const duration = back ? back.tEnd + 0.6 : tBack + 1.0;
  const Rhold = ry(yaw);
  const spinRel = sw ? sw.omega(tRel) : 0; // the skull leaves with the hand's angular velocity
  const latAxis = scl(Lf, -1); // rotation axis for a forward/backward tumble
  const Rswing = (th) => mm(rotAxis(latAxis, -th + theta0 * 0), Rhold);
  const prepFrom = hold, prepTo = sw ? swingCM(tStart) : add(S_REL, scl(F, r));

  function skullAt(t) {
    if (t < tReady) return null; // handled by the pop (drop) or the initial hold
    if (t < tStart) { // carried by the right hand to the start of the swing (the left lets go)
      const u = smooth01(t, tReady, tStart);
      return { cm: arcPoint(prepFrom, prepTo, mv(Rhold, mode === 'over' ? [-85, 55, 10] : [-70, -15, 10]), u), R: slerpR(Rhold, sw ? Rswing(theta0) : Rhold, u), hand: 'right', w: u };
    }
    if (t < tRel) return { cm: sw ? swingCM(t) : prepTo, R: sw ? Rswing(sw.theta(t)) : Rhold, hand: 'right' };
    if (t < tCatch) {
      const tau = t - tRel;
      const spin = mode === 'over' && tau > flight.contacts[0] - 1e-9 ? spinRel * flight.contacts[0] - 0.5 * spinRel * (tau - flight.contacts[0]) : spinRel * tau;
      return { cm: posFlight(tau), R: mm(rotAxis(latAxis, -spin), Rhold), free: true };
    }
    const tauC = tCatch - tRel;
    const spinC = mode === 'over' ? spinRel * flight.contacts[0] - 0.5 * spinRel * (tauC - flight.contacts[0]) : spinRel * tauC;
    const Rc = mm(rotAxis(latAxis, -spinC), Rhold);
    const cmC = absorb ? add(Pc, absorb.offset(t)) : Pc;
    const one = mode !== 'over'; // caught in the right hand alone (the left can't reach across); the left joins on the way back
    if (t < tStill) return { cm: cmC, R: Rc, hand: one ? 'rightUnder' : 'both' };
    const u = smooth01(t, tStill, tBack);
    const cmS = absorb ? add(Pc, absorb.offset(tStill)) : Pc;
    return { cm: arcPoint(cmS, hold, mv(Rhold, [0, 14, 10]), u), R: slerpR(Rc, Rhold, u), hand: one && u < 1 ? 'rightUnder' : 'both', join: u };
  }
  let wristsAtA = null;
  // the right hand cupped under the skull (wrist below and a little behind its centre)
  const handUnderAt = (cm) => ({ specs: [{ space: 'world', p: add(cm, mv(ry(yaw), [0, -33, -10])) }], pole: [-0.8, -0.6, -0.2], curl: [0.45, 0.5, 0.55, 0.6], spread: 0.4, pron: 0.95, flex: 0.35, dev: 0 });
  function poseAt(t) {
    let pose = bodyPose(t);
    if (withPop && t < tReady) { pose.props.hat = { mode: 'head' }; pose = pop.apply(pose, t); return pose; }
    if (back && t >= tBack + 0.2) { pose.props.hat = { mode: 'neck' }; return back.apply(pose, t); }
    if (withPop) pose = pop.apply(pose, t); // keeps the hat business (stump)
    pose.props.hat = withPop ? pose.props.hat : { mode: 'neck' };
    const sk = skullAt(t) || { cm: hold, R: Rhold, hand: 'both' };
    pose.props.skull = { mode: 'free', cm: sk.cm, R: sk.R };
    const ev = char.evaluatePose(pose).ev;
    const S = ev.J.shoulderR;
    const both = bothHandsOn(sk.cm, yaw);
    const rest = [JSON.parse(JSON.stringify(base.arms[0])), JSON.parse(JSON.stringify(base.arms[1]))];
    // left hand balance pose while the right throws
    rest[1].specs = [{ space: 'chest', p: [52, -60, 40] }]; rest[1].pole = [0.8, -0.3, -0.4]; rest[1].curl = [0.2, 0.25, 0.3, 0.35]; rest[1].spread = 0.5;
    const blendArm = (A, B, w) => ({ ...(w > 0.5 ? B : A), specs: [...A.specs.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - w) })), ...B.specs.map((s) => ({ ...s, w: (s.w ?? 1) * w }))] });
    if (sk.hand === 'right' && t >= tStart - 1e-9 || (sk.hand === 'right' && sk.w === 1)) {
      const dir = norm(sub(sk.cm, S));
      pose.arms[0] = handUnder(sk.cm, dir, -1, { off: 34 });
      pose.arms[1] = rest[1];
    } else if (sk.hand === 'right') {
      // the hand-over: the right hand slides under, the left hand lets go
      const dir = norm(sub(sk.cm, S));
      pose.arms[0] = blendArm(both[0], handUnder(sk.cm, dir, -1, { off: 34 }), ease.smooth(clamp(sk.w * 2.5, 0, 1)));
      pose.arms[1] = blendArm(both[1], rest[1], ease.smooth(clamp(sk.w * 2.5, 0, 1)));
    } else if (sk.free) {
      // the right hand follows through, then both hands go to meet the skull, moving with it at the catch
      // toss: the hands start riding with the skull at the top of its flight (where it is momentarily still)
      const tA = mode === 'under' ? tRel + proj.apexT : tCatch - 0.42;
      const thetaF = sw ? sw.theta(t) : 0;
      const follow = handUnder(add(S, scl(dirOf(thetaF), r)), dirOf(thetaF), -1, { off: 34, curl: 0.15 });
      if (mode === 'drop') { follow.curl = [0, 0, 0.05, 0.05]; follow.spread = 1; }
      if (t < tA) { pose.arms[0] = follow; pose.arms[1] = rest[1]; }
      else {
        const u = (t - tA) / (tCatch - tA);
        const gc = mode === 'over' ? bothHandsOn(Pc, yaw) : [handUnderAt(Pc), null];
        if (!wristsAtA) { const ev0 = char.evaluatePose(poseAt(tA - 1e-6)).ev; wristsAtA = [ev0.J.wristR, ev0.J.wristL]; }
        // the hands ride along with the falling skull and close in on their grips: hand = skull + offset,
        // the offset eased to the grip offset, so at the catch the hands move exactly with the skull (C1)
        const cmNow = posFlight(t - tRel), cmA = posFlight(tA - tRel), e = ease.smoother(u);
        const grip = mode === 'under'
          ? (i) => { const o0 = sub(wristsAtA[i], cmA), o1 = sub(gc[i].specs[0].p, Pc); return add(cmNow, add(scl(o0, 1 - e), scl(o1, e))); }
          : (i) => hermV(wristsAtA[i], gc[i].specs[0].p, [0, 0, 0], scl(Vc, tCatch - tA), u);
        pose.arms = [0, 1].map((i) => (gc[i] ? { ...gc[i], specs: [{ space: 'world', p: grip(i) }], curl: [0.2, 0.25, 0.3, 0.35], spread: 0.6 } : rest[1]));
      }
    } else if (sk.hand === 'rightUnder') {
      const j = ease.smoother(clamp(((sk.join ?? 0) - 0.3) / 0.7, 0, 1));
      const hu = handUnderAt(sk.cm), side = bothHandsOn(sk.cm, yaw)[0];
      pose.arms[0] = j > 0 ? { ...(j > 0.5 ? side : hu), specs: [{ ...hu.specs[0], w: 1 - j }, { ...side.specs[0], w: j }], pron: hu.pron + (side.pron - hu.pron) * j } : hu;
      pose.arms[1] = j > 0 ? { ...armTo(rest[1], bothHandsOn(sk.cm, yaw)[1].specs[0].p, j, 1), curl: [0.45, 0.55, 0.6, 0.65], pron: 0.55, pole: [0.7, -0.5, -0.6] } : rest[1];
    } else pose.arms = both;
    pose.face.look = [0, sk.free ? clamp((sk.cm[1] - 250) / 200, -0.6, 0.8) : 0.1];
    return pose;
  }
  const phases = [
    ...(pop ? pop.phases : []),
    { name: 'prep', t0: tReady, t1: env.start },
    ...env.phases.map((q) => ({ ...q })),
  ];
  const events = [...(pop ? pop.events : []), { t: tRel, kind: 'release' }, { t: tCatch, kind: 'catch' }];
  if (flight) for (const c of flight.contacts) events.push({ t: tRel + c, kind: 'bounce' });
  if (back) events.push(...back.events);
  // the analytic trajectory, for the overlay (dashed curve + spacing dots every 1/12 s)
  const trail = (t) => {
    if (t < tRel) return null;
    const pts = [];
    for (let s = 0; s <= tCatch - tRel + 1e-9; s += 1 / 120) pts.push(posFlight(s));
    const dots = [];
    for (let s = 0; s <= Math.min(t, tCatch) - tRel + 1e-9; s += 1 / 12) dots.push(posFlight(s));
    return { pts, dots };
  };
  return {
    duration, poseAt, phases, events, trail, tRel, tCatch, v0, omega, r, P_REL, V0, proj, flight, mode, env, sw, shoulderAt, swingCM, S_REL, Vc,
    impulses: [{ t: tRel, jaw: -3 }, { t: tCatch, ribs: 0.6 }],
  };
}
