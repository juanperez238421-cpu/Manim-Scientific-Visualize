// 3-D math for the bone rig. Pure functions, no DOM (runs in the browser and in node tests).
// Vectors: [x, y, z]. Matrices: 3x3 row-major arrays of 9 numbers. Rigid frames: { R, t }.
// Rig space: x = the character's left, y = up, z = the character's front, units "u".

export const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
export const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
export const scl = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
export const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const len = (a) => Math.hypot(a[0], a[1], a[2]);
export const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
export const norm = (a) => { const l = len(a); return l > 1e-12 ? [a[0] / l, a[1] / l, a[2] / l] : [0, 0, 0]; };
export const lerp3 = (a, b, u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];

export const I3 = [1, 0, 0, 0, 1, 0, 0, 0, 1];
export function mm(A, B) {
  const C = new Array(9);
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) C[3 * i + j] = A[3 * i] * B[j] + A[3 * i + 1] * B[3 + j] + A[3 * i + 2] * B[6 + j];
  }
  return C;
}
export const mv = (A, v) => [A[0] * v[0] + A[1] * v[1] + A[2] * v[2], A[3] * v[0] + A[4] * v[1] + A[5] * v[2], A[6] * v[0] + A[7] * v[1] + A[8] * v[2]];
export const tr = (A) => [A[0], A[3], A[6], A[1], A[4], A[7], A[2], A[5], A[8]];
export const col = (A, j) => [A[j], A[3 + j], A[6 + j]];
export const cols = (X, Y, Z) => [X[0], Y[0], Z[0], X[1], Y[1], Z[1], X[2], Y[2], Z[2]];
export const det = (A) => A[0] * (A[4] * A[8] - A[5] * A[7]) - A[1] * (A[3] * A[8] - A[5] * A[6]) + A[2] * (A[3] * A[7] - A[4] * A[6]);
export function rx(a) { const c = Math.cos(a), s = Math.sin(a); return [1, 0, 0, 0, c, -s, 0, s, c]; }
export function ry(a) { const c = Math.cos(a), s = Math.sin(a); return [c, 0, s, 0, 1, 0, -s, 0, c]; }
export function rz(a) { const c = Math.cos(a), s = Math.sin(a); return [c, -s, 0, s, c, 0, 0, 0, 1]; }
// Rodrigues rotation about a unit axis k by angle a
export function rotAxis(k, a) {
  const [x, y, z] = k, c = Math.cos(a), s = Math.sin(a), C = 1 - c;
  return [c + x * x * C, x * y * C - z * s, x * z * C + y * s,
    y * x * C + z * s, c + y * y * C, y * z * C - x * s,
    z * x * C - y * s, z * y * C + x * s, c + z * z * C];
}
// rotation taking unit vector a onto unit vector b (shortest arc)
export function rotBetween(a, b) {
  const c = dot(a, b);
  const k = cross(a, b);
  const s = len(k);
  if (s < 1e-12) {
    if (c > 0) return I3;
    const p = Math.abs(a[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
    return rotAxis(norm(cross(a, p)), Math.PI);
  }
  return rotAxis(scl(k, 1 / s), Math.atan2(s, c));
}
export function toAxisAngle(R) {
  const tr_ = R[0] + R[4] + R[8];
  const cosA = Math.max(-1, Math.min(1, (tr_ - 1) / 2));
  const angle = Math.acos(cosA);
  if (angle < 1e-9) return { axis: [1, 0, 0], angle: 0 };
  if (Math.PI - angle < 1e-6) {
    // axis from the diagonal of (R + I) / 2
    const xx = Math.sqrt(Math.max(0, (R[0] + 1) / 2)), yy = Math.sqrt(Math.max(0, (R[4] + 1) / 2)), zz = Math.sqrt(Math.max(0, (R[8] + 1) / 2));
    let ax = [xx, Math.sign(R[1] || 1) * yy, Math.sign(R[2] || 1) * zz];
    return { axis: norm(ax), angle };
  }
  const k = [R[7] - R[5], R[2] - R[6], R[3] - R[1]];
  return { axis: norm(k), angle };
}
// geodesic interpolation between rotations
export function slerpR(A, B, u) {
  const { axis, angle } = toAxisAngle(mm(tr(A), B));
  return mm(A, rotAxis(axis, angle * u));
}

// rigid frames
export const fmul = (A, B) => ({ R: mm(A.R, B.R), t: add(mv(A.R, B.t), A.t) });
export const fapp = (A, p) => add(mv(A.R, p), A.t);
export const ftr = (t) => ({ R: I3, t });
export const frot = (R) => ({ R, t: [0, 0, 0] });
export const finv = (A) => { const Rt = tr(A.R); return { R: Rt, t: scl(mv(Rt, A.t), -1) }; };
// frame whose local -Y axis runs along `down` (unit) and whose local Z is as close as possible to `fwd`.
// Right-handed: X = Y x Z. Long bones are modelled from their proximal joint along local -Y.
export function frameAlong(origin, down, fwd) {
  const Y = scl(norm(down), -1);
  let Z = sub(fwd, scl(Y, dot(fwd, Y)));
  if (len(Z) < 1e-6) {
    const alt = Math.abs(Y[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0];
    Z = sub(alt, scl(Y, dot(alt, Y)));
  }
  Z = norm(Z);
  const X = cross(Y, Z);
  return { R: cols(X, Y, Z), t: origin };
}

// Two-bone IK in 3D. S: root joint, T: target for the end joint, L1/L2 bone lengths, pole: preferred
// direction of the middle joint. Returns the solved middle and end joints and whether T was reachable.
// soft (0..1, optional): beyond soft*(L1+L2) the reach eases exponentially toward full extension instead of
// snapping straight (no knee/elbow "pop"); `err` reports how far the end stays from the target.
export function twoBone(S, T, L1, L2, pole, soft = 0) {
  const v = sub(T, S);
  const d = len(v);
  const dmax = L1 + L2 - 1e-6, dmin = Math.abs(L1 - L2) + 1e-6;
  let ds = d;
  if (soft > 0) { const s0 = soft * dmax; if (d > s0) ds = s0 + (dmax - s0) * (1 - Math.exp(-(d - s0) / (dmax - s0))); }
  const dc = Math.min(dmax, Math.max(dmin, ds));
  const dir = d > 1e-9 ? scl(v, 1 / d) : [0, -1, 0];
  const a = (L1 * L1 - L2 * L2 + dc * dc) / (2 * dc);
  const h = Math.sqrt(Math.max(0, L1 * L1 - a * a));
  let p = sub(pole, scl(dir, dot(pole, dir)));
  if (len(p) < 1e-9) p = Math.abs(dir[2]) < 0.9 ? sub([0, 0, 1], scl(dir, dir[2])) : sub([1, 0, 0], scl(dir, dir[0]));
  p = norm(p);
  const mid = add(add(S, scl(dir, a)), scl(p, h));
  const end = add(S, scl(dir, dc));
  return { mid, end, reach: d <= dmax + 1e-9 && d >= dmin - 1e-9, over: Math.max(0, d - dmax), under: Math.max(0, dmin - d), d, err: Math.abs(d - dc) };
}

export const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
export const angleBetween = (a, b) => Math.acos(clamp(dot(norm(a), norm(b)), -1, 1));
