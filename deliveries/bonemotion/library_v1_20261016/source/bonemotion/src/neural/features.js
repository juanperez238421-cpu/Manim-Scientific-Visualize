// Pose <-> feature vector for the learned in-betweener, and the window-relative transform.
// The SAME definitions are mirrored in train/train_inbetween.py (keep them in sync; the dataset tool
// writes the layout into its meta file and the trainer checks it).
//
// Absolute frame vector (46): world positions in u, angles in rad (yaw/headings unwrapped per sequence)
//   0-2 root p | 3 yaw | 4-5 tilt | 6-8 spine | 9-11 neck | 12-14 head | 15-16 shrug | 17-18 prot
//   19-21 ankle R | 22 heading R | 23 pitch R | 24 toe R | 25 plantW R
//   26-28 ankle L | 29 heading L | 30 pitch L | 31 toe L | 32 plantW L
//   33-35 wrist R | 36 curl R | 37 pron R | 38 flex R
//   39-41 wrist L | 42 curl L | 43 pron L | 44 flex L | 45 jaw
export const DIM = 46;
export const POS_BLOCKS = [0, 19, 26, 33, 39]; // 3-vectors expressed relative to the window's start root
export const ANG_IDX = [3, 22, 29]; // angles measured from the window's start yaw
export const LAYOUT_VERSION = 'bm-feat-v1';

export function poseToAbs(char, pose) {
  const { ev } = char.evaluatePose(pose);
  const A = new Float64Array(DIM);
  A.set(pose.root.p, 0); A[3] = pose.root.yaw || 0; A[4] = pose.root.tilt?.[0] || 0; A[5] = pose.root.tilt?.[1] || 0;
  A.set(pose.spine, 6); A.set(pose.neck, 9); A.set(pose.head, 12); A.set(pose.shrug || [0, 0], 15); A.set(pose.prot || [0, 0], 17);
  [0, 1].forEach((i) => {
    const L = pose.legs[i], o = 19 + 7 * i;
    A.set(L.ankle, o); A[o + 3] = L.heading || 0; A[o + 4] = L.pitch || 0; A[o + 5] = L.toe || 0; A[o + 6] = L.plantW ?? 1;
    const Ar = pose.arms[i], q = 33 + 6 * i;
    A.set(ev.J[`wrist${i ? 'L' : 'R'}`], q);
    const cu = Ar.curl || [0.2, 0.2, 0.2, 0.2];
    A[q + 3] = (cu[0] + cu[1] + cu[2] + cu[3]) / 4; A[q + 4] = Ar.pron ?? 0.25; A[q + 5] = Ar.flex ?? 0.1;
  });
  A[45] = pose.face?.jaw ?? 0.1;
  return A;
}

// keep yaw-like angles continuous along a sequence
export function unwrapSeq(frames) {
  for (const k of ANG_IDX) for (let i = 1; i < frames.length; i++) {
    let d = frames[i][k] - frames[i - 1][k];
    while (d > Math.PI) { frames[i][k] -= 2 * Math.PI; d -= 2 * Math.PI; }
    while (d < -Math.PI) { frames[i][k] += 2 * Math.PI; d += 2 * Math.PI; }
  }
  return frames;
}

// to / from the frame of reference (p0, y0) of a window
export function toRel(A, p0, y0) {
  const c = Math.cos(y0), s = Math.sin(y0);
  const R = Float64Array.from(A);
  for (const o of POS_BLOCKS) {
    const x = A[o] - p0[0], y = A[o + 1] - p0[1], z = A[o + 2] - p0[2];
    R[o] = c * x - s * z; R[o + 1] = y; R[o + 2] = s * x + c * z;
  }
  for (const k of ANG_IDX) R[k] = A[k] - y0;
  return R;
}
export function fromRel(R, p0, y0) {
  const c = Math.cos(y0), s = Math.sin(y0);
  const A = Float64Array.from(R);
  for (const o of POS_BLOCKS) {
    const x = R[o], y = R[o + 1], z = R[o + 2];
    A[o] = p0[0] + c * x + s * z; A[o + 1] = p0[1] + y; A[o + 2] = p0[2] - s * x + c * z;
  }
  for (const k of ANG_IDX) A[k] = R[k] + y0;
  return A;
}

// back to a pose (props and fine finger detail come from a template pose)
export function absToPose(A, template) {
  const P = JSON.parse(JSON.stringify(template));
  P.root.p = [A[0], A[1], A[2]]; P.root.yaw = A[3]; P.root.tilt = [A[4], A[5]];
  P.spine = [A[6], A[7], A[8]]; P.neck = [A[9], A[10], A[11]]; P.head = [A[12], A[13], A[14]];
  P.shrug = [A[15], A[16]]; P.prot = [A[17], A[18]];
  [0, 1].forEach((i) => {
    const o = 19 + 7 * i, q = 33 + 6 * i;
    P.legs[i] = { ...P.legs[i], ankle: [A[o], A[o + 1], A[o + 2]], heading: A[o + 3], pitch: A[o + 4], toe: A[o + 5], plantW: Math.max(0, Math.min(1, A[o + 6])) };
    const cu = A[q + 3];
    P.arms[i] = { ...P.arms[i], specs: [{ space: 'world', p: [A[q], A[q + 1], A[q + 2]] }], curl: [cu, cu, cu, cu], pron: A[q + 4], flex: A[q + 5] };
    delete P.arms[i].detached;
  });
  P.face = { ...(P.face || {}), jaw: A[45] };
  return P;
}
