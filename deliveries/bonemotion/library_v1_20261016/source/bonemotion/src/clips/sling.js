// The sling, standing: Mr. Bones pops his skull off, holds it out in his left hand, grabs his own left
// arm by the elbow, tugs twice (anticipation), POPs it out of the shoulder (follow-through), lets it
// swing as a pendulum, then spins it in a vertical circle in front of him — constant angular
// acceleration, then constant omega — and lets go with the radius horizontal: the skull leaves straight
// up with v0 = omega R exactly. The arm swings back and waits; the skull falls back into its open hand
// (caught over an arc at constant deceleration), the arm clicks back into the shoulder and the head
// goes back on.
//
// The hand drives the sling the way a real one does: the grip runs on a small circle that leads the
// skull by 90 degrees; with the skull on an exact circle of radius R about a fixed centre, the arm's
// length from grip to skull is constant (R^2 + r_h^2), so the rigid arm never stretches.
import { standPose, SIDE, toWorld } from '../core/body.js';
import { ease, clamp, track, arcPoint, hermite } from '../core/curves.js';
import { slingSchedule, pendulum, projectile } from '../core/physics.js';
import { add, sub, scl, mv, mm, ry, rz, norm, len, cross, rotAxis, slerpR, fapp } from '../core/m3.js';
import { CM_LOCAL } from '../characters/mrbones/index.js';
import { DIM } from '../characters/mrbones/model.js';
import { popHead, headBack } from './throws.js';
import { bothHandsOn, pulse } from './kit.js';

const smooth01 = (t, a, b) => ease.smoother(clamp((t - a) / (b - a), 0, 1));
const GRIP = 8; // the right hand holds the humerus 8 u above the elbow
const ARM = DIM.humerus + DIM.forearm; // 115
const WRIST_CM = 52;

export function sling(char, p = {}) {
  const pr = char.profile, g = pr.g, K = pr.K;
  const yaw = p.yaw ?? 1.05, o = [p.x ?? -120, 0, p.z ?? -10];
  const F = [Math.sin(yaw), 0, Math.cos(yaw)];
  const v0 = (p.v0 ?? 4) * K;
  const base = standPose(pr, { x: o[0], z: o[2], yaw, toeOut: 0.5, width: 1.25 });
  base.legs[1].ankle = add(base.legs[1].ankle, scl(F, 14));
  base.props.hat = { mode: 'neck' };
  const hold = toWorld(o, yaw, [0, 192, 80]);
  const pop = popHead(char, 0.4, { hold, yaw });
  const tA = pop.tEnd + 0.1; // the left hand takes the skull out alone
  const tB = tA + 0.8; // right hand on the left elbow
  const tTug1 = tB + 0.12, tTug2 = tTug1 + 0.26, tPop = tTug2 + 0.3;
  // geometry (world plane z = const through the circle centre; the camera sees the circle round)
  const ev0 = char.evaluatePose(base).ev;
  const SH_L = ev0.J.shoulderL, SH_R = ev0.J.shoulderR;
  const dL = norm(add(scl(F, 0.85), [0, 0.18, 0])); // left arm held straight out in front
  const C = add(add(SH_R, scl(F, 70)), [8, 22, 0]); C[2] = SH_L[2] + 34; // spin centre (held by the right hand)
  const rH = 5, Rr = Math.sqrt(ARM * ARM - rH * rH); // grip circle, skull circle radius
  const omega = v0 / Rr;
  const tHang = tPop + 2.0; // pendulum time while the right hand brings the arm to the centre
  const tUpEnd = tHang + 0.35;
  const sch = slingSchedule({ theta0: -Math.PI / 2, thetaRel: 0, omega, tRel: 0, tUp: 0.8, minTurns: 1, dir: 1 });
  const tS = tUpEnd, tRel = tS - sch.tS; // shift the schedule so the spin starts at tS
  const thetaS = (t) => sch.theta(t - tRel), thetaDotS = (t) => sch.thetaDot(t - tRel);
  const P_REL = add(C, [Rr, 0, 0]);
  const fly = projectile(P_REL, [0, v0, 0], g);
  const tCatch = tRel + (2 * v0) / g;
  const dCatch = 70; // arc length over which the open hand slows the skull down
  const aCatch = (v0 * v0) / (2 * dCatch), TCatch = (2 * dCatch) / v0;
  const tStill = tCatch + TCatch;
  // after release the arm keeps turning, slows, swings back to theta = 0 and waits for the skull
  const thAfter = track([{ t: tRel, v: 0, slope: omega }, { t: tRel + 0.32, v: 0.32 * omega / 2, mode: 'flat' }, { t: tCatch - 0.16, v: 0, mode: 'flat' }]);
  const theta = (t) => {
    if (t < tRel) return thetaS(t);
    if (t < tCatch) return thAfter.at(t);
    const tau = Math.min(t, tStill) - tCatch;
    return -(v0 * tau - 0.5 * aCatch * tau * tau) / Rr; // caught: the arm carries it down the circle
  };
  const tPend2 = tStill; // a short damped swing after the catch, then the arm hangs
  const pend2 = pendulum({ theta0: 0, omega0: 0, w0: Math.sqrt(g / 260), damping: 2.5, t0: tPend2, t1: tPend2 + 3 });
  const thetaStill = theta(tStill);
  const tRe0 = tStill + 0.55, tRe1 = tRe0 + 0.7; // back into the socket
  const back = headBack(char, tRe1 + 0.25, { fromCM: hold, fromR: ry(yaw), yaw });
  const duration = back.tEnd + 0.7;
  // pendulum after the pop: the arm swings from straight out (in front) down to hanging
  const psi0 = Math.acos(clamp(-dL[1], -1, 1));
  const pend = pendulum({ theta0: psi0, omega0: 0, w0: Math.sqrt(g / 230), damping: 1.1, t0: tPop + 0.12, t1: tHang + 0.5 });
  const Rskull0 = ry(yaw);
  const planeN = [0, 0, 1];
  const eTh = (th) => [Math.cos(th), Math.sin(th), 0];

  // the detached arm: grip G and direction d (from the humeral head toward the hand)
  function armState(t) {
    if (t < tPop) return null;
    const pullDir = norm(sub(SH_R, SH_L));
    const S0 = SH_L, G0 = add(SH_L, scl(dL, DIM.humerus - GRIP));
    if (t < tPop + 0.12) {
      const u = 1 - (1 - (t - tPop) / 0.12) ** 3;
      const S = add(S0, scl(norm(add(pullDir, scl(F, 0.6))), 26 * u));
      return { S, d: dL, G: add(S, scl(dL, DIM.humerus - GRIP)) };
    }
    if (t < tS) {
      // the pivot (grip) travels to the circle's bottom grip point; the arm hangs from it, swinging in the
      // vertical plane through the pull direction (pendulum, damped, eased to rest for the spin-up)
      const Gp = add(S0, add(scl(norm(add(pullDir, scl(F, 0.6))), 26), scl(dL, DIM.humerus - GRIP)));
      const Gc = add(C, scl(eTh(-Math.PI / 2 + Math.PI / 2), -rH)); // grip at theta = -pi/2 leads by +pi/2 -> e(0) * rH, opposite sign: below
      const u = smooth01(t, tPop + 0.12, tHang);
      const G = arcPoint(Gp, add(C, scl(eTh(0), rH * 0)), [0, 10, 0], u);
      const fade = 1 - smooth01(t, tHang - 0.6, tS);
      const psi = pend.theta(t) * fade; // from straight down, + toward the front
      const swingPlaneFwd = norm([F[0], 0, F[2]]);
      const d = norm(add(scl([0, -1, 0], Math.cos(psi)), scl(swingPlaneFwd, Math.sin(psi))));
      void Gc;
      const S = sub(G, scl(d, DIM.humerus - GRIP));
      return { S, d, G };
    }
    if (t < tRe0 || t < tStill + 0.01) {
      const th = t < tStill ? theta(t) : thetaStill;
      const lead = Math.min(1, smooth01(t, tS, tS + 0.5)) * (1 - smooth01(t, tRel, tRel + 0.3));
      const G = add(C, scl(eTh(th + Math.PI / 2), rH * lead));
      const cm = add(C, scl(eTh(th), Rr));
      const d = norm(sub(cm, G));
      const S = sub(G, scl(d, DIM.humerus - GRIP));
      return { S, d, G, th };
    }
    // the hanging arm after the catch swings a little, then is carried back and clicks into the socket
    const thH = thetaStill + pend2.theta(t);
    const G1 = add(C, [0, 0, 0]);
    const cm1 = add(C, scl(eTh(thH), Rr));
    const d1 = norm(sub(cm1, G1));
    const u = smooth01(t, tRe0, tRe1);
    const dRest = norm(add(scl(F, 0.55), [0, -0.83, 0]));
    const d = norm(add(scl(d1, 1 - u), scl(dRest, u)));
    const S = arcPoint(sub(G1, scl(d1, DIM.humerus - GRIP)), SH_L, [0, 20, 0], u);
    return { S, d, G: add(S, scl(d, DIM.humerus - GRIP)), reattached: t >= tRe1 };
  }
  function poseAt(t) {
    let pose = JSON.parse(JSON.stringify(base));
    // a counter-lean against the pull of the spinning skull (centripetal force on the hand)
    const spinW = smooth01(t, tS, tS + 0.8) * (1 - smooth01(t, tRel + 0.1, tRel + 0.8));
    const th = t >= tS && t < tRel + 0.6 ? theta(t) : 0;
    pose.root.p = add(pose.root.p, add(scl(F, -6 * spinW), [-4 * spinW * Math.cos(th), -5 * spinW, 0]));
    pose.spine = [pose.spine[0] - 0.06 * spinW, pose.spine[1] + 0.05 * spinW * Math.cos(th), pose.spine[2]];
    if (t < tA) { pose.props.hat = { mode: 'head' }; return pop.apply(pose, t); }
    pose = pop.apply(pose, t); // (keeps the hat on the stump)
    if (t >= tRe1 + 0.25) { pose.props.hat = { mode: 'neck' }; return back.apply(pose, t); }
    const A = armState(t);
    // the skull
    let cm, R;
    if (t < tPop) {
      const u = smooth01(t, tA, tB);
      const out = add(SH_L, scl(dL, ARM - 3 + WRIST_CM));
      cm = arcPoint(hold, out, [0, 16, 0], u); R = Rskull0;
    } else if (t < tRel) { cm = add(A.S, scl(A.d, ARM + WRIST_CM)); R = mm(rotAxis(planeN, (A.th ?? -Math.PI / 2) + Math.PI / 2), Rskull0); }
    else if (t < tCatch) { cm = fly.at(t - tRel); R = mm(rotAxis(planeN, omega * (t - tRel)), Rskull0); }
    else if (t < tRe1) { cm = add(A.S, scl(A.d, ARM + WRIST_CM)); R = mm(rotAxis(planeN, omega * (tCatch - tRel) + (theta(Math.min(t, tStill)) - 0)), Rskull0); }
    else { cm = hold; R = Rskull0; }
    if (t >= tRe1 - 0.01 && t < tRe1 + 0.25) { const u = smooth01(t, tRe1, tRe1 + 0.25); cm = arcPoint(add(SH_L, scl(norm(add(scl(F, 0.55), [0, -0.83, 0])), ARM + WRIST_CM)), hold, [0, 10, 20], u); }
    pose.props.skull = { mode: 'free', cm, R };
    // arms
    const ev = char.evaluatePose(pose).ev;
    if (t < tPop) {
      // left arm straight out holding the skull; right hand travels to the left elbow and tugs
      const tug = 3 * Math.max(0, pulse(t - tTug1, 4, 0.5)) + 5 * Math.max(0, pulse(t - tTug2, 4, 0.5));
      const pullDir = norm(sub(SH_R, SH_L));
      const wL = add(sub(cm, scl(dL, WRIST_CM - 2)), scl(pullDir, tug));
      const wA = smooth01(t, tA, tB);
      const both = bothHandsOn(cm, yaw);
      pose.arms[1] = { ...both[1], specs: [{ ...both[1].specs[0], w: 1 - wA }, { space: 'world', p: wL, w: wA }], pole: [0.5, -0.8, -0.2], curl: [0.55, 0.6, 0.65, 0.7], pron: 0.9, flex: 0.3 };
      const elbowGrip = add(add(SH_L, scl(dL, DIM.humerus - GRIP)), [0, 6, 4]);
      const wR = add(elbowGrip, add(scl(pullDir, -12 + tug), [0, 8, 0]));
      const k = smooth01(t, tA + 0.2, tB);
      pose.arms[0] = { ...both[0], specs: [{ ...both[0].specs[0], w: 1 - k }, { space: 'world', p: wR, w: k }], pole: [-0.6, -0.7, -0.4], curl: k > 0.9 ? [0.9, 0.95, 0.95, 0.95] : [0.3, 0.3, 0.3, 0.3], pron: 0.6, flex: 0.1 };
      pose.shrug = [0, 0.06 * (tug / 5)];
    } else if (A && !A.reattached) {
      const holding = t < tRel || t >= tCatch;
      pose.arms[1] = { detached: { S: A.S, d: A.d, n: planeN }, curl: holding ? [0.7, 0.75, 0.8, 0.85] : [0, 0, 0.05, 0.05], spread: holding ? 0.2 : 1, pron: 0.2, flex: 0, dev: 0 };
      // the right fist on the grip; after the pop it flies out a little (follow-through) and comes back
      const over = t < tPop + 0.5 ? scl(norm(sub(SH_R, SH_L)), 14 * Math.max(0, pulse(t - tPop, 1.6, 0.5))) : [0, 0, 0];
      pose.arms[0] = { specs: [{ space: 'world', p: add(add(A.G, [0, 0, -16]), over) }], pole: [-0.5, -0.8, -0.4], curl: [0.85, 0.9, 0.9, 0.9], spread: 0.1, pron: 0.6, flex: 0.2, dev: 0 };
    } else {
      // reattached: the left arm is an arm again (it starts exactly where the detached chain ended),
      // then both hands bring the skull in
      const u = smooth01(t, tRe1, tRe1 + 0.25);
      const both = bothHandsOn(cm, yaw);
      const dRest = norm(add(scl(F, 0.55), [0, -0.83, 0]));
      const wStraight = add(SH_L, scl(dRest, ARM - 9));
      const gripR = add(add(SH_L, scl(dRest, DIM.humerus - GRIP)), [0, 0, -16]);
      pose.arms[1] = { ...both[1], specs: [{ space: 'world', p: wStraight, w: 1 - u }, { ...both[1].specs[0], w: u }] };
      pose.arms[0] = { ...both[0], specs: [{ space: 'world', p: gripR, w: 1 - u }, { ...both[0].specs[0], w: u }] };
    }
    pose.face = { jaw: 0.15, look: [0, 0.2], pupil: 1 };
    return pose;
  }
  const phases = [
    ...pop.phases,
    { name: 'prep', t0: tA, t1: tB }, { name: 'antic', t0: tB, t1: tPop }, { name: 'exec', t0: tPop, t1: tPop + 0.15 }, { name: 'follow', t0: tPop + 0.15, t1: tHang - 0.3 }, { name: 'settle', t0: tHang - 0.3, t1: tS },
    { name: 'prep', t0: tS, t1: tS + 0.8 }, { name: 'exec', t0: tS + 0.8, t1: tRel }, { name: 'follow', t0: tRel, t1: tRel + 0.32 }, { name: 'settle', t0: tCatch, t1: tRe1 },
  ];
  const trail = (t) => {
    if (t < tRel || t > tCatch + 0.6) return null;
    const pts = [], dots = [];
    for (let s = 0; s <= tCatch - tRel + 1e-9; s += 1 / 120) pts.push(fly.at(s));
    for (let s = 0; s <= Math.min(t, tCatch) - tRel + 1e-9; s += 1 / 12) dots.push(fly.at(s));
    return { pts, dots };
  };
  const events = [...pop.events, { t: tTug1, kind: 'tug' }, { t: tTug2, kind: 'tug' }, { t: tPop, kind: 'clack' }, { t: tRel, kind: 'release' }, { t: tCatch, kind: 'catch' }, { t: tRe1, kind: 'click' }, ...back.events];
  return { duration, poseAt, phases, trail, events, C, R: Rr, rH, omega, v0, tS, tRel, tCatch, tPop, P_REL, thetaDot: (t) => (t < tRel ? thetaDotS(t) : 0), theta,
    impulses: [{ t: tPop, ribs: 0.8, jaw: 4 }, { t: tCatch, ribs: 0.5 }, { t: tRe1, ribs: 0.6 }] };
}
void cross; void len; void slerpR; void SIDE; void hermite; void CM_LOCAL; void fapp; void ry; void rz;
