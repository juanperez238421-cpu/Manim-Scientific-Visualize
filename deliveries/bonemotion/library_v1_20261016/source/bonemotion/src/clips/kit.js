// Shared building blocks for clips: body layers, two-pass evaluation (body first, then the hands that
// follow props), skull handling and the pop-off / put-back business, catches.
import { standPose, SIDE, toWorld, fwdOf, leftOf } from '../core/body.js';
import { track, ease, clamp } from '../core/curves.js';
import { add, sub, scl, mv, mm, ry, rx, rz, norm, len, cross, fapp, fmul, ftr, frot, finv, rotAxis, slerpR, I3 } from '../core/m3.js';

export { standPose, SIDE, toWorld, fwdOf, leftOf, track, ease, clamp };

// add offsets (a small "layer") to a pose's numeric body channels
export function layer(pose, o) {
  if (o.root) pose.root.p = add(pose.root.p, o.root);
  if (o.yaw) pose.root.yaw += o.yaw;
  if (o.tilt) pose.root.tilt = [pose.root.tilt[0] + o.tilt[0], pose.root.tilt[1] + o.tilt[1]];
  for (const k of ['spine', 'neck', 'head']) if (o[k]) pose[k] = pose[k].map((x, i) => x + o[k][i]);
  if (o.shrug) pose.shrug = pose.shrug.map((x, i) => x + o.shrug[i]);
  if (o.prot) pose.prot = pose.prot.map((x, i) => x + o.prot[i]);
  return pose;
}

// evaluate the body without caring about the arms (head, shoulders and chest do not depend on them)
export function bodyEval(char, pose) { return char.evaluatePose(pose).ev; }

// world velocity of any point function by central difference (QA-grade, h = 1e-4 s)
export const vel = (f, t, h = 1e-4) => scl(sub(f(t + h), f(t - h)), 1 / (2 * h));

// ------------------------------------------------------------------ hands on a skull (Mr. Bones)
// both hands on the sides of the cranium (palms in); `yaw` is the body's facing
export function bothHandsOn(cm, yaw, { spread = 40, lift = 4, back = 6 } = {}) {
  return SIDE.map((s) => ({
    specs: [{ space: 'world', p: add(cm, mv(ry(yaw), [s * spread, lift, -back])) }], pole: [s * 0.7, -0.5, -0.6],
    curl: [0.45, 0.55, 0.6, 0.65], spread: 0.25, pron: 0.55, flex: -0.1, dev: 0,
  }));
}
// both hands cupped beneath the skull, palms up (a catch from below)
export function bothHandsUnder(cm, yaw, { spread = 15, down = 32, back = 8 } = {}) {
  return SIDE.map((s) => ({
    specs: [{ space: 'world', p: add(cm, mv(ry(yaw), [s * spread, -down, -back])) }], pole: [s * 0.8, -0.6, -0.2],
    curl: [0.45, 0.5, 0.55, 0.6], spread: 0.45, pron: 0.9, flex: 0.3, dev: 0,
  }));
}
// one hand cupped beneath the skull (Hamlet's grip); dir = direction from the shoulder to the skull
export function handUnder(cm, dir, s, { off = 34, curl = 0.55 } = {}) {
  return { specs: [{ space: 'world', p: sub(cm, scl(dir, off)) }], pole: [s * 0.8, -0.6, -0.3], curl: [curl, curl + 0.05, curl + 0.1, curl + 0.15], spread: 0.3, pron: 0.9, flex: 0.35, dev: 0 };
}
export const openHand = (A) => ({ ...A, curl: [0, 0, 0.05, 0.05], spread: 1 });

// skull placement records (props.skull): attached, or free with centre of mass cm and orientation R
export const skullFree = (cm, R) => ({ mode: 'free', cm, R });

// a damped "click" pulse (0 -> peak -> 0): used for squash, recoil, ring
export function pulse(tau, f = 7, z = 0.35) {
  if (tau <= 0) return 0;
  const w = 2 * Math.PI * f, wd = w * Math.sqrt(1 - z * z);
  return Math.exp(-z * w * tau) * Math.sin(wd * tau);
}

// interpolate rotation matrices with an ease
export const slerpE = (A, B, u) => slerpR(A, B, clamp(u, 0, 1));
export { add, sub, scl, mv, mm, ry, rx, rz, norm, len, cross, fapp, fmul, ftr, frot, finv, rotAxis, slerpR, I3 };

// Reaching with a hand from where it is (its current specs) to a world target, along a natural path:
// a straight blend would drag the hand past the shoulder (and fold the elbow flat), so the path is pulled
// through a waypoint in front of the chest (weight 4u(1-u)): the hand travels on an arc, like a real reach.
export function armTo(A, target, u, s, { fwd = 62, up = 10, out = 26, k = 0.85 } = {}) {
  const b = k * 4 * u * (1 - u);
  const way = { space: 'chest', p: [s * out, up, fwd] };
  return {
    ...A,
    specs: [
      ...A.specs.map((sp) => ({ ...sp, w: (sp.w ?? 1) * (1 - u) * (1 - b) })),
      { space: 'world', p: target, w: u * (1 - b) },
      { ...way, w: b },
    ],
  };
}

// blend between two arm targets (lists of specs) along the same kind of arc, in either direction
export function armBlend(A, fromSpecs, toSpecs, u, s, { fwd = 62, up = 10, out = 26, k = 0.85 } = {}) {
  const b = k * 4 * u * (1 - u);
  return {
    ...A,
    specs: [
      ...fromSpecs.map((sp) => ({ ...sp, w: (sp.w ?? 1) * (1 - u) * (1 - b) })),
      ...toSpecs.map((sp) => ({ ...sp, w: (sp.w ?? 1) * u * (1 - b) })),
      { space: 'chest', p: [s * out, up, fwd], w: b },
    ],
  };
}
