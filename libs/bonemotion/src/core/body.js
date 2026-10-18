// Character-agnostic body helpers: everything here reads the character's proportions (profile.dims),
// so a clip written with them retargets to any biped.
//
// Local body frame: x = the character's LEFT, y = up, z = FORWARD; ry(yaw) turns it into the world.
import { add, sub, scl, mv, ry, rx, mm, norm, len, dot } from './m3.js';

export const SIDE = [-1, 1]; // index 0 = right (x < 0 in the body frame), 1 = left
export const toWorld = (origin, yaw, local) => add(origin, mv(ry(yaw), local));
export const toLocal = (origin, yaw, world) => mv(ry(-yaw), sub(world, origin));
export const fwdOf = (yaw) => [Math.sin(yaw), 0, Math.cos(yaw)];
export const leftOf = (yaw) => [Math.cos(yaw), 0, -Math.sin(yaw)];

// ankle position that keeps a foot pivot (ball, heel, or the point under the ankle) fixed in the world
// while the foot is pitched: the no-slip foot roll. pivotLocal is in the foot frame (profile.foot.*).
export function ankleFromPivot(pivotWorld, pivotLocal, heading, pitch) {
  return sub(pivotWorld, mv(mm(ry(heading), rx(pitch)), pivotLocal));
}

// a planted / free leg record
export function legRec(ankle, heading, { pitch = 0, toe = 0, plantW = 1, kneeOut = 0.25, pole } = {}) {
  return { ankle, heading, pitch, toe, plantW, kneeOut, pole };
}
// foot flat on the ground: `ground` is the point under the ankle
export function flatFoot(pr, ground, heading, o = {}) {
  return legRec([ground[0], pr.dims.ankleH, ground[2]], heading, o);
}

// arms hanging from the shoulders (chest space), relaxed
export function hangArm(pr, s, { out = 4, fwd = -12, bend = 0.95 } = {}) {
  const d = pr.dims;
  const sh = sub(d.shoulder, d.chest);
  return {
    specs: [{ space: 'chest', p: [s * (sh[0] + out), sh[1] - d.armLen * bend, sh[2] + fwd] }],
    curl: [0.25, 0.3, 0.35, 0.4], spread: 0.35, pron: 0.25, flex: 0.1, dev: 0,
  };
}

// the neutral standing pose at ground point (x, z) facing yaw
export function standPose(pr, { x = 0, z = 0, yaw = 0, width = 1, toeOut = 0.15, hipDrop = 0, spine = [0.04, 0, 0] } = {}) {
  const d = pr.dims;
  const o = [x, 0, z];
  const legs = SIDE.map((s) => flatFoot(pr, toWorld(o, yaw, [s * d.footRestX * width, 0, 0]), yaw + s * toeOut));
  return {
    root: { p: add(o, [0, d.standH - hipDrop, 0]), yaw, tilt: [0, 0] },
    spine: spine.slice(), neck: [0, 0, 0], head: [0, 0, 0], shrug: [0, 0], prot: [0, 0],
    legs, arms: SIDE.map((s) => hangArm(pr, s)),
    face: { jaw: 0.1, look: [0, 0], pupil: 1 },
    props: { hat: { mode: 'head' } },
  };
}

// hip joint position for a pelvis pose (for reach limits)
export function hipPos(pr, root, s) {
  const R = mm(ry(root.yaw || 0), mm(rx(root.tilt?.[0] || 0), rz0(root.tilt?.[1] || 0)));
  return add(root.p, mv(R, [s * pr.dims.hipW, 0, 0]));
}
const rz0 = (a) => { const c = Math.cos(a), s = Math.sin(a); return [c, -s, 0, s, c, 0, 0, 0, 1]; };

// highest pelvis height at which the hip can still reach `ankle` with the leg at `ext` of full length
export function reachHeight(pr, rootXZ, yaw, s, ankle, ext = 0.975) {
  const hip = add(rootXZ, mv(ry(yaw), [s * pr.dims.hipW, 0, 0]));
  const dx = hip[0] - ankle[0], dz = hip[2] - ankle[2];
  const L = ext * pr.dims.legLen;
  const h2 = L * L - dx * dx - dz * dz;
  return h2 > 0 ? ankle[1] + Math.sqrt(h2) : ankle[1];
}

export { len, norm, dot, add, sub, scl, mv, ry };
