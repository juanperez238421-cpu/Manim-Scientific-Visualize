// "Mr. Bones", anatomical edition: a 3-D skeleton in which every bone is its own rigid object.
// Pure module (no DOM): buildModel() declares the bones; evaluate() poses them from controls.
//
// Rig space: x = character's left, y = up, z = character's front; ground at y = 0; unit "u".
// Each bone object has a rigid frame {R, t} and parts (spheres, capsules, discs, ellipsoids,
// plates) in its local coordinates. Long bones run from their proximal joint along local -Y.
// Teeth and costal cartilage are separate objects too, but are not counted as bones.
import {
  add, sub, scl, dot, cross, len, dist, norm, lerp3, I3, mm, mv, tr, col, rx, ry, rz, rotAxis, rotBetween,
  slerpR, fmul, fapp, ftr, frot, finv, frameAlong, twoBone, clamp,
} from '../../core/m3.js';

export const DIM = {
  hip: 26, femur: 62, tibia: 58, ankleH: 13.5, ballZ: 27, heelZ: -11,
  humerus: 60, forearm: 55, radius: 52, clav: 40,
  sacrumTop: [0, 26, -10],
  L: { n: 5, h: 7, rest: -0.025 }, T: { n: 12, h: 6.5, rest: 0.025 }, C: { n: 7, h: 3.4, rest: -0.035 },
  sacralTilt: 0.085, // forward tilt of the lumbar base: puts the skull over the pelvis at rest (tuned, tools/tune_spine.mjs)
  // rib table, rib 1..12: lateral half-width, half-depth, anterior drop
  ribW: [22, 30, 35, 39, 42, 44, 45, 45, 44, 41, 35, 29],
  ribD: [12, 15, 17, 18, 19, 19.5, 19.5, 19, 18, 17, 15, 13],
  ribDrop: [3, 7, 10, 13, 15, 17, 19, 21, 22, 21, 13, 9],
  thoraxCz: 15,
  sternalY: [11, 4.5, -2.5, -9.5, -16.5, -23, -29], // where ribs 1..7 meet the sternum (sternum frame)
};
export const sideName = (s) => (s < 0 ? 'R' : 'L');
export const SIDES = [-1, 1];

// ---------------------------------------------------------------- part constructors
const Sp = (c, r) => ({ t: 'sph', c, r });
const Cp = (a, b, ra, rb = ra) => ({ t: 'cap', a, b, ra, rb });
const Dc = (a, b, r) => ({ t: 'cyl', a, b, r });
const El = (c, r) => ({ t: 'ell', c, r });
const Pl = (pts) => ({ t: 'poly', pts });
const chain = (pts, rs) => pts.slice(1).map((p, i) => Cp(pts[i], p, rs[i], rs[i + 1]));

// point on an axis-aligned ellipsoid in direction d from its centre, and the outward normal there
function onEllipsoid(c, r, d) {
  const lam = 1 / Math.sqrt((d[0] / r[0]) ** 2 + (d[1] / r[1]) ** 2 + (d[2] / r[2]) ** 2);
  const p = add(c, scl(d, lam));
  const n = norm([(p[0] - c[0]) / r[0] ** 2, (p[1] - c[1]) / r[1] ** 2, (p[2] - c[2]) / r[2] ** 2]);
  return { p, n };
}

// rib i (1..12) centre-line in its thoracic vertebra's frame
export function ribCurve(i, s, n = 14) {
  const W = DIM.ribW[i - 1], D = DIM.ribD[i - 1], drop = DIM.ribDrop[i - 1], cz = DIM.thoraxCz;
  const th0 = Math.asin(5 / W);
  let th1;
  if (i <= 7) th1 = Math.PI - Math.asin(Math.min(0.95, 8 / W));
  else if (i <= 10) th1 = Math.PI - Math.asin(Math.min(0.95, 17 / W)) - 0.12;
  else th1 = i === 11 ? 1.95 : 1.6;
  const pts = [];
  for (let k = 0; k < n; k++) {
    const th = th0 + ((th1 - th0) * k) / (n - 1);
    const f = Math.pow((th - th0) / (Math.PI - th0), 1.3);
    pts.push({ th, p: [s * W * Math.sin(th), 3.5 - drop * f, cz - D * Math.cos(th)] });
  }
  return { pts, th0, th1, attach: pts[0].p };
}

// ---------------------------------------------------------------- the model
export function buildModel() {
  const defs = [];
  const def = (d) => { const o = { bias: 0, tone: 'bone', bone: true, small: false, decals: [], side: 0, ...d }; o.uid = defs.length; defs.push(o); return o; };

  // ---- skull (head frame: origin on top of the atlas, y up, z forward)
  const CR_C = [0, 32, -3], CR_R = [35, 35, 38];
  const suture = [];
  for (let k = 0; k <= 26; k++) {
    const ph = -1.35 + (2.7 * k) / 26;
    const z = 0.33 + 0.05 * Math.sin(k * 1.9);
    suture.push(onEllipsoid(CR_C, CR_R, norm([Math.sin(ph), 0.94 * Math.cos(ph), z * Math.cos(ph)])));
  }
  const sagittal = [];
  for (let k = 0; k <= 14; k++) {
    const ph = (1.4 * k) / 14;
    sagittal.push(onEllipsoid(CR_C, CR_R, norm([0.03 * Math.sin(k * 2.3), Math.cos(ph) * 0.94, 0.33 - Math.sin(ph) * 1.2])));
  }
  const crack = [[0.28, 0.84, 0.47], [0.36, 0.76, 0.54], [0.3, 0.69, 0.66], [0.39, 0.6, 0.7], [0.33, 0.53, 0.78], [0.4, 0.47, 0.79]]
    .map((d) => onEllipsoid(CR_C, CR_R, norm(d)));
  const crackBranch = [[0.39, 0.6, 0.7], [0.47, 0.62, 0.62], [0.52, 0.55, 0.65]].map((d) => onEllipsoid(CR_C, CR_R, norm(d)));
  def({
    name: 'cranium', frame: 'head', group: 'skull',
    parts: [El(CR_C, CR_R), Sp([27, 6, -12], 4.6), Sp([-27, 6, -12], 4.6), El([0, 22, -30], [22, 18, 12])],
    decals: [
      { t: 'sline', pts: suture, w: 1.5, dash: [3, 3] },
      { t: 'sline', pts: sagittal, w: 1.5, dash: [3, 3] },
      { t: 'sline', pts: crack, w: 2.2 },
      { t: 'sline', pts: crackBranch, w: 1.8 },
    ],
  });
  const arch = (y, x0, z0, az, n) => Array.from({ length: n }, (_, k) => {
    const ps = (-80 + (160 * k) / (n - 1)) * Math.PI / 180;
    return [x0 * Math.sin(ps), y, z0 + az * Math.cos(ps)];
  });
  def({
    name: 'maxilla', frame: 'head', group: 'skull',
    parts: [El([0, 9, 15], [21, 11, 14]), ...chain(arch(3.5, 16.5, 10, 16, 9), [4.4, 4.4, 4.6, 4.8, 5, 4.8, 4.6, 4.4, 4.4])],
  });
  for (const s of SIDES) {
    def({ name: `zygomatic ${sideName(s)}`, frame: 'head', group: 'skull', side: s,
      parts: [Sp([s * 22, 15, 17], 8.5), Cp([s * 24, 14, 14], [s * 33, 13, -6], 4.2, 3.6)] });
  }
  def({
    name: 'mandible', frame: 'jaw', group: 'skull',
    parts: [
      Sp([25, 0, 0], 3.6), Sp([-25, 0, 0], 3.6),
      Cp([25, 0, 0], [24, -18, 3], 4.6), Cp([-25, 0, 0], [-24, -18, 3], 4.6),
      Cp([21, -4, 5], [19, 3, 8], 2.3), Cp([-21, -4, 5], [-19, 3, 8], 2.3),
      ...chain([[24, -18, 3], [19, -20, 13], [11, -22, 21], [0, -23, 24], [-11, -22, 21], [-19, -20, 13], [-24, -18, 3]], [4.8, 4.8, 4.8, 5, 4.8, 4.8, 4.8]),
      Sp([0, -25, 24], 6.5),
    ],
    decals: [
      { t: 'disc', c: [9, -21, 23.5], n: norm([0.35, 0, 1]), u: [1, 0, 0], r: [1.2, 1.2], fill: '#3a3a3a' },
      { t: 'disc', c: [-9, -21, 23.5], n: norm([-0.35, 0, 1]), u: [1, 0, 0], r: [1.2, 1.2], fill: '#3a3a3a' },
    ],
  });
  // teeth: 10 upper on the maxilla, 10 lower on the mandible
  const toothAngles = [-72, -54, -36, -20, -7, 7, 20, 36, 54, 72];
  toothAngles.forEach((a, k) => {
    const ps = (a * Math.PI) / 180, w = Math.abs(a) < 15 ? 2.5 : Math.abs(a) < 30 ? 2.7 : 3.2;
    const cx = 15.5 * Math.sin(ps), cz = 10 + 16.5 * Math.cos(ps);
    def({ name: `upper tooth ${k + 1}`, frame: 'head', group: 'teeth', tone: 'tooth', bone: false, small: true, bias: 1.5,
      parts: [Cp([cx, 3, cz], [cx, -3.4, cz], w, w * 0.9)] });
  });
  toothAngles.forEach((a, k) => {
    const ps = (a * Math.PI) / 180, w = Math.abs(a) < 15 ? 2.3 : Math.abs(a) < 30 ? 2.6 : 3.1;
    const cx = 14 * Math.sin(ps), cz = 13.5 + 14 * Math.cos(ps);
    def({ name: `lower tooth ${k + 1}`, frame: 'jaw', group: 'teeth', tone: 'tooth', bone: false, small: true, bias: 1.2,
      parts: [Cp([cx, -14, cz], [cx, -7.6, cz], w, w * 0.9)] });
  });
  // eye sockets + nasal aperture: dark openings drawn over the face bones
  for (const s of SIDES) {
    const n = norm([s * 0.32, 0.1, 1]);
    def({ name: `orbit ${sideName(s)}`, frame: 'head', kind: 'socket', bone: false, side: s, bias: 9, parts: [], burstWith: 'cranium',
      socket: { c: [s * 14.5, 24, 31], n, u: norm(cross([0, 1, 0], n)), r: [12, 13.5] } });
  }
  def({ name: 'nasal aperture', frame: 'head', kind: 'decal', bone: false, bias: 9, parts: [], burstWith: 'maxilla',
    decals: [{ t: 'dpoly', n: norm([0, 0.08, 1]), fill: '#0a0a0a',
      pts: [[0, 19, 28.6], [-3.6, 15, 28.3], [-5.6, 9.5, 27.6], [-3, 6.2, 28.2], [0, 7.6, 28.6], [3, 6.2, 28.2], [5.6, 9.5, 27.6], [3.6, 15, 28.3]] }] });
  def({ name: 'hyoid', frame: 'C3', group: 'skull', small: true,
    parts: [Cp([6, 0, 9], [0, 0.5, 12.5], 1.5), Cp([-6, 0, 9], [0, 0.5, 12.5], 1.5), Sp([0, 0.5, 12.5], 2.1)] });

  // ---- vertebral column
  const vparts = {
    L: (h) => [Dc([0, 0.8, 0], [0, h - 0.8, 0], 10), Cp([9, 4.2, -3], [19, 5, -6.5], 2.6, 2.1), Cp([-9, 4.2, -3], [-19, 5, -6.5], 2.6, 2.1),
      Cp([6, 4, -6], [0, 4, -11], 2.4), Cp([-6, 4, -6], [0, 4, -11], 2.4), Cp([0, 4, -11], [0, 2.5, -18.5], 3.2, 2.6)],
    T: (h) => [Dc([0, 0.7, 0], [0, h - 0.7, 0], 7.4), Cp([6.5, 4, -3.5], [12, 5, -7.5], 2.1, 1.8), Cp([-6.5, 4, -3.5], [-12, 5, -7.5], 2.1, 1.8),
      Cp([4.5, 4, -6], [0, 4, -9], 1.9), Cp([-4.5, 4, -6], [0, 4, -9], 1.9), Cp([0, 4, -9], [0, -2.5, -15], 2.2, 1.6)],
    C: (h) => [Dc([0, 0.5, 0], [0, h - 0.5, 0], 5.6), Cp([5, 1.8, -1], [9, 1.8, -2], 1.6, 1.3), Cp([-5, 1.8, -1], [-9, 1.8, -2], 1.6, 1.3),
      Cp([0, 1.8, -5], [0, 1.2, -10], 1.8, 1.4)],
  };
  const spineKeys = [];
  for (const [reg, dim] of [['L', DIM.L], ['T', DIM.T], ['C', DIM.C]]) {
    for (let k = 0; k < dim.n; k++) {
      const num = dim.n - k; // bottom-up: L5..L1, T12..T1, C7..C1
      const key = `${reg}${num}`;
      spineKeys.push({ key, reg, h: dim.h, rest: dim.rest });
      let parts = vparts[reg](dim.h);
      if (key === 'C1') parts = [Dc([0, 0.4, 0], [0, 2.8, 0], 7.2), Cp([7, 1.6, -1], [10.5, 1.6, -2], 1.8)];
      if (key === 'C2') parts = [...parts, Sp([0, 4.2, 0.5], 2.2)];
      def({ name: `vertebra ${key}`, frame: key, group: 'spine', small: reg === 'C', bias: -1, parts });
    }
  }
  def({
    name: 'sacrum', frame: 'pelvis', group: 'pelvis', bias: 1,
    parts: [Pl([[-15, 27, -11], [15, 27, -11], [13, 18, -10], [9, 6, -9], [4, -1, -8], [0, -3, -8], [-4, -1, -8], [-9, 6, -9], [-13, 18, -10]]),
      Cp([0, 25, -13], [0, 0, -11], 4.5, 3)],
    decals: [20, 14, 8.5, 3.5].flatMap((y, k) => [-1, 1].map((sd) => ({ t: 'disc', c: [sd * (5.6 - k * 0.6), y, -8.4], n: [0, 0, 1], u: [1, 0, 0], r: [1.7, 1.4], fill: '#3c3c3c' }))),
  });
  for (let k = 0; k < 3; k++) {
    def({ name: `coccyx ${k + 1}`, frame: `cocc${k}`, group: 'pelvis', small: true, bias: 0.5,
      parts: [Cp([0, 0, 0], [0, -4.2, 0], 2.6 - 0.45 * k, 2.2 - 0.45 * k)] });
  }
  for (const s of SIDES) {
    def({
      name: `os coxae ${sideName(s)}`, frame: 'pelvis', group: 'pelvis', side: s, bias: 4,
      parts: [
        Pl([[s * 12, 25, -10], [s * 24, 34, -6], [s * 34, 37, -1], [s * 42, 33, 4], [s * 43, 24, 8], [s * 38, 16, 10], [s * 34, 12, 9], [s * 28, 8, 6], [s * 22, 7, 2], [s * 15, 12, -6]]),
        ...chain([[s * 24, 34, -6], [s * 34, 37, -1], [s * 42, 33, 4], [s * 43, 24, 8]], [3, 3, 3, 3]),
        Sp([s * 42, 22, 9], 3.5),
        Cp([s * 28, 8, 6], [s * 26, 2, 1], 7),
        Sp([s * 26, 0, 0], 10.5),
        Cp([s * 22, -4, 6], [s * 6, -13, 11], 3.6), Sp([s * 4, -15, 11], 4.5),
        Cp([s * 4, -17, 11], [s * 12, -24, 7], 3), Cp([s * 12, -24, 7], [s * 20, -24, 1], 3.5),
        Sp([s * 22, -22, -2], 5.5), Cp([s * 22, -22, -2], [s * 27, -8, -2], 5),
      ],
    });
  }

  // ---- thorax
  const ribInfo = {};
  for (let i = 1; i <= 12; i++) {
    for (const s of SIDES) {
      const rc = ribCurve(i, s);
      const loc = rc.pts.map((q) => sub(q.p, rc.attach));
      const r = (u) => (i === 1 ? 3.1 : 2.3 + 0.6 * Math.sin(Math.PI * Math.min(1, u * 1.2)));
      const rs = loc.map((_, k) => r(k / (loc.length - 1)));
      const half = Math.max(1, rc.pts.findIndex((q) => q.th >= Math.PI / 2));
      const post = chain(loc.slice(0, half + 1), rs.slice(0, half + 1));
      const ant = chain(loc.slice(half), rs.slice(half));
      const key = `rib${i}${sideName(s)}`;
      ribInfo[key] = { i, s, attach: rc.attach, local: loc, th: rc.pts.map((q) => q.th) };
      def({ name: `rib ${i} ${sideName(s)}`, frame: key, group: 'ribs', side: s, pieces: ant.length ? [post, ant] : [post] });
    }
  }
  // costal cartilage (dynamic: drawn between the rib end and the sternum; flexible, not a bone)
  for (let i = 1; i <= 10; i++) {
    for (const s of SIDES) def({ name: `costal cartilage ${i} ${sideName(s)}`, frame: 'world', dyn: `cart${i}${sideName(s)}`, tone: 'cart', bone: false, side: s, bias: 1.5, parts: [] });
  }
  def({ name: 'manubrium', frame: 'sternum', group: 'sternum', bias: 2.5,
    parts: [Pl([[-8, 15, 0], [-3, 13.5, 0.5], [0, 14.5, 0.5], [3, 13.5, 0.5], [8, 15, 0], [9, 10, 0], [6, 4, 0], [-6, 4, 0], [-9, 10, 0]]), Cp([0, 12, -2], [0, 5, -2], 4)] });
  def({ name: 'sternum body', frame: 'sternum', group: 'sternum', bias: 2.5,
    parts: [Pl([[-6, 3.5, 0], [6, 3.5, 0], [7, -8, 0], [7.5, -20, 0], [6, -31, 0], [-6, -31, 0], [-7.5, -20, 0], [-7, -8, 0]]), Cp([0, 2, -2], [0, -29, -2], 3.5)],
    decals: [-6, -13.5, -21].map((y) => ({ t: 'line', pts: [[-5.5, y, 0.3], [5.5, y, 0.3]], w: 1.3 })) });
  def({ name: 'xiphoid', frame: 'sternum', group: 'sternum', small: true, bias: 2.5, parts: [Cp([0, -31.5, 0], [0, -38, -1], 2.4, 1.5)] });

  // ---- shoulder girdle and arms
  for (const s of SIDES) {
    const n = sideName(s);
    def({ name: `clavicle ${n}`, frame: `clav${n}`, group: 'arm', side: s, bias: 3,
      parts: chain([[0, 0, 0], [0, -10, 1.5], [0, -22, 0.8], [0, -33, -1.5], [0, -40, 0]], [3.8, 3, 2.8, 3, 3.8]) });
    def({ name: `scapula ${n}`, frame: `scap${n}`, group: 'arm', side: s, bias: -3,
      parts: [Pl([[s * -2, -4, -5], [s * -20, 0, -19], [s * -26, -3, -21], [s * -20, -30, -23], [s * -15, -48, -22], [s * -8, -30, -13], [s * -3, -15, -7]]),
        Cp([0, 0, -4], [s * -24, -8, -20], 2.5), Sp([0, 0, 0], 4), Cp([s * -2, -6, 2], [s * -6, -9, 6], 2.2), Sp([s * -1, -9, 0], 5)] });
    def({ name: `humerus ${n}`, frame: `hum${n}`, group: 'arm', side: s,
      parts: [Sp([0, 0, 0], 7), Sp([s * 4.5, -3, 1.5], 4.6), Cp([0, -4, 0], [0, -50, 0], 3.9, 3.3), Sp([s * 2.6, -24, 0.6], 2.6),
        Sp([s * 6, -55.5, -0.5], 4.1), Sp([s * -7.2, -55.5, -0.5], 4.6), Dc([s * -5, -58.5, 0.5], [s * 5, -58.5, 0.5], 4.2)] });
    const xu = s * -3;
    def({ name: `ulna ${n}`, frame: `fore${n}`, group: 'arm', side: s,
      parts: [Sp([xu, 1.5, -3.5], 5), Cp([xu, -2, -1], [xu, -49, 0], 3.0, 2.2), Sp([xu, -51.5, 0], 3.0), Sp([xu, -54, -1], 2.0)] });
    def({ name: `radius ${n}`, frame: `rad${n}`, group: 'arm', side: s, bias: 0.5,
      parts: [Dc([0, 0, 0], [0, -3, 0], 4), Cp([0, -3, 0], [0, -8, 0], 2.5), Sp([s * -1.5, -10, 0.5], 2.5), Cp([0, -8, 0], [0, -45, 0], 2.5, 3.3),
        Dc([0, -46.5, 0], [0, -50.5, 0], 4.4), Sp([s * 3, -51.5, 0], 2.1)] });
    const carpals = [['scaphoid', [4.6, -3.5, 0.5], 3.0], ['lunate', [1.6, -3.5, 0], 2.7], ['triquetrum', [-1.6, -3.8, -0.5], 2.6], ['pisiform', [-3.6, -4.5, 2.6], 1.9],
      ['trapezium', [5.2, -8.2, 1.2], 2.5], ['trapezoid', [2.4, -8.8, 0.5], 2.2], ['capitate', [-0.3, -9, 0], 2.6], ['hamate', [-3.4, -8.6, -0.3], 2.5]];
    for (const [cn, c, r] of carpals) def({ name: `${cn} ${n}`, frame: `hand${n}`, group: 'hand', side: s, small: true, bias: 0.3, parts: [Sp([s * c[0], c[1], c[2]], r)] });
    def({ name: `metacarpal 1 ${n}`, frame: `mc0${n}`, group: 'hand', side: s, small: true, bias: 0.4, parts: [Sp([0, 0, 0], 2.2), Cp([0, 0, 0], [0, -12, 0], 2.3, 1.9), Sp([0, -12, 0], 2.3)] });
    for (let k = 1; k <= 3; k++) def({ name: `metacarpal ${k + 1} ${n}`, frame: `mc${k}${n}`, group: 'hand', side: s, small: true, bias: 0.4, parts: [Sp([0, 0, 0], 2.2), Cp([0, 0, 0], [0, -15, 0], 2.1, 1.7), Sp([0, -15, 0], 2.3)] });
    const FL = { 0: [8, 6], 1: [9.5, 6.5, 5], 2: [10, 7, 5], 3: [9, 6, 4.6] };
    const FR = [1.9, 1.6, 1.4];
    for (let k = 0; k <= 3; k++) {
      FL[k].forEach((L, j) => {
        const r = FR[j] * (k === 0 ? 1.08 : 1);
        def({ name: `phalanx ${k + 1}.${j + 1} ${n}`, frame: `ph${k}${j}${n}`, group: 'hand', side: s, small: true, bias: 0.5,
          parts: [Cp([0, 0, 0], [0, -L, 0], r, r * 0.85), Sp([0, -L, 0], r * (j === FL[k].length - 1 ? 1.05 : 1.15))] });
      });
    }
  }

  // ---- legs and feet
  for (const s of SIDES) {
    const n = sideName(s);
    def({ name: `femur ${n}`, frame: `fem${n}`, group: 'leg', side: s,
      parts: [Sp([0, 0, 0], 8.5), Cp([0, 0, 0], [s * 10, -6, 0], 4.6), Sp([s * 12.5, -5, -1], 6.2), Sp([s * 3, -12, -2.5], 3),
        Cp([s * 8, -10, 0], [s * 0.5, -54, 0], 5.2, 4.6), Sp([s * 5.8, -57.5, -1], 6.6), Sp([s * -5.8, -57.5, -1], 6.6), Sp([0, -56, 3.5], 4.3)] });
    def({ name: `patella ${n}`, frame: `pat${n}`, group: 'leg', side: s, bias: 2, parts: [El([0, 0, 0], [5, 6.5, 2.6])] });
    def({ name: `tibia ${n}`, frame: `tib${n}`, group: 'leg', side: s,
      parts: [Dc([0, -1.5, 0], [0, -5.5, 0], 8.2), Sp([s * 5, -4, -0.5], 5.2), Sp([s * -5, -4, -0.5], 5.2), Sp([0, -10, 4], 3.2),
        Cp([0, -7, 1], [0, -50, 0], 4.5, 3.4), Dc([s * -1, -51.5, 0], [s * -1, -56, 0], 4.6), Sp([s * -5, -57, 0.3], 3.4)] });
    def({ name: `fibula ${n}`, frame: `tib${n}`, group: 'leg', side: s, bias: -0.5,
      parts: [Sp([s * 7.8, -7.5, -2], 3.2), Cp([s * 7.8, -9, -2], [s * 6.3, -55, -0.8], 1.9, 1.6), Sp([s * 6.3, -58.5, -0.5], 3.3)] });
    const foot = (nm, parts, small = true) => def({ name: `${nm} ${n}`, frame: `foot${n}`, group: 'foot', side: s, small, bias: 0.2, parts });
    foot('talus', [El([0, -2.5, 1], [5, 4, 6.5])], false);
    foot('calcaneus', [Cp([0, -5.5, -2], [0, -8.5, -11], 4.8, 5), Sp([s * -3, -7, -3], 2.6)], false);
    foot('navicular', [Sp([s * -2.6, -5.5, 7], 3.2)]);
    foot('cuboid', [Sp([s * 3.4, -8.6, 6.8], 3.4)]);
    foot('medial cuneiform', [Sp([s * -3.6, -7.5, 11.2], 2.6)]);
    foot('intermediate cuneiform', [Sp([s * -0.8, -8, 11.6], 2.3)]);
    foot('lateral cuneiform', [Sp([s * 1.8, -8.5, 11.2], 2.3)]);
    MT.forEach((m, k) => {
      foot(`metatarsal ${k + 1}`, [Sp(sx(m.base, s), m.rb), Cp(sx(m.base, s), sx(m.head, s), m.r0, m.r1), Sp(sx(m.head, s), m.rh)]);
    });
    TOES.forEach((lens, k) => lens.forEach((L, j) => {
      const r = (k === 0 ? [2.5, 2.2] : [1.8, 1.6, 1.4])[j];
      def({ name: `toe phalanx ${k + 1}.${j + 1} ${n}`, frame: `toe${k}${j}${n}`, group: 'foot', side: s, small: true, bias: 0.3,
        parts: [Cp([0, 0, 0], [0, 0, L], r, r * 0.88), Sp([0, 0, L], r * 0.95)] });
    }));
  }

  // ---- props
  // the cane: a long spare bone with a knob, gripped under the knob (frame origin = grip, shaft along -Y)
  def({ name: 'bone cane', frame: 'cane', group: 'prop', bone: false, prop: true, bias: -1.5,
    parts: [Sp([0, 7, 0], 6.2), Sp([2.5, 9, 3], 4.4), Cp([0, 4, 0], [0, -145, 0], 3.3, 2.6), Sp([0, -146, 0], 4.0), Sp([1.6, -147.5, 1], 2.6)] });
  def({ name: 'spare femur (mallet)', frame: 'mallet', group: 'prop', bone: false, prop: true, bias: -1.5, zFrom: 'handL', zEnd: [0, -48, 0],
    parts: [Sp([0, 2, 0], 6.4), Sp([0, 3, 4], 5.6), Cp([0, 0, 0], [0, -46, 0], 3.6, 4.2), Sp([0, -48, 0], 7.2), Cp([0, -48, 0], [3, -53, 0], 4)] });

  return { defs, ribInfo, spineKeys, bones: defs.filter((d) => d.bone).length };
}
// metatarsal table (k = 0 big toe .. 3), x given for the left foot (multiplied by side)
const MT = [
  { base: [-3.8, -8.6, 12.5], head: [-4.8, -10.9, 27], rb: 2.6, r0: 2.9, r1: 2.4, rh: 2.6 },
  { base: [-1, -8.6, 12.5], head: [-1.2, -11.5, 27], rb: 2.1, r0: 2.1, r1: 1.8, rh: 2.0 },
  { base: [1.6, -8.6, 12.3], head: [2.4, -11.5, 26.2], rb: 2.1, r0: 2.1, r1: 1.8, rh: 2.0 },
  { base: [4.2, -8.6, 12], head: [5.8, -11.5, 24.8], rb: 2.0, r0: 2.0, r1: 1.8, rh: 2.0 },
];
const TOES = [[7, 5.5], [4.6, 3, 2.4], [4.4, 2.8, 2.2], [4, 2.6, 2]];
const sx = (p, s) => [s * p[0], p[1], p[2]];
export const FOOT = { MT, TOES, ball: [0, -13.5, 27], heel: [0, -13.5, -11] };
const HAND = {
  mcBase: { 0: [5.3, -9.5, 1.8], 1: [3.0, -10.5, 0], 2: [0, -10.5, 0], 3: [-3.0, -10.5, 0] },
  mcLen: { 0: 12, 1: 15, 2: 15, 3: 15 },
  ph: { 0: [8, 6], 1: [9.5, 6.5, 5], 2: [10, 7, 5], 3: [9, 6, 4.6] },
};

// ---------------------------------------------------------------- posing
export const ZERO_SEC = { jaw: 0, hatLift: 0, hatTilt: 0, ribs: new Array(12).fill(0), ribsL: new Array(12).fill(0), coccyx: 0, fingers: [0, 0], nod: 0 };

// resolve a target spec ({space, p, w}) to world coordinates
function resolveSpec(spec, ctx) {
  const { fr, J } = ctx;
  switch (spec.space) {
    case 'world': return spec.p;
    case 'pelvis': return fapp(fr.pelvis, spec.p);
    case 'chest': return fapp(fr.chest, spec.p);
    case 'head': return fapp(fr.head, spec.p);
    case 'knee': return add(J[`knee${spec.side}`], mv(fr.pelvis.R, spec.p));
    case 'ribStrike': return add(ctx.strike(spec.rib), scl(ctx.strikeNormal(spec.rib), spec.off || 0));
    default: throw new Error(`unknown space ${spec.space}`);
  }
}
function resolveSpecs(list, ctx) {
  let w = 0, p = [0, 0, 0];
  for (const sp of list) { const q = resolveSpec(sp, ctx); p = add(p, scl(q, sp.w ?? 1)); w += sp.w ?? 1; }
  return scl(p, 1 / w);
}

export function evaluate(model, c, sec = ZERO_SEC, opts = {}) {
  const fr = { world: { R: I3, t: [0, 0, 0] } };
  const J = {};
  const flags = { ik: [], notes: [] };
  const dyn = {};

  // pelvis
  const pr = c.pelvisRot || [0, 0, 0];
  fr.pelvis = { R: mm(ry((c.yaw || 0) + pr[1]), mm(rx(pr[0]), rz(pr[2]))), t: c.pelvis };
  J.pelvis = c.pelvis;
  // coccyx (wags with the secondary channel)
  let cf = fmul(fr.pelvis, ftr([0, -3, -8]));
  for (let k = 0; k < 3; k++) {
    cf = fmul(cf, frot(mm(rx(0.32), rz((sec.coccyx || 0) * (0.6 + 0.4 * k)))));
    fr[`cocc${k}`] = cf;
    cf = fmul(cf, ftr([0, -4.2, 0]));
  }
  // spine: bend controls distributed over the vertebrae of each region
  const sp = c.spine || [0, 0, 0], nk = c.neck || [0, 0, 0];
  let F = fmul(fmul(fr.pelvis, ftr(DIM.sacrumTop)), frot(rx(DIM.sacralTilt)));
  for (const v of model.spineKeys) {
    const share = v.reg === 'L' ? 0.4 / DIM.L.n : v.reg === 'T' ? 0.6 / DIM.T.n : 0;
    const nshare = v.reg === 'C' ? 1 / DIM.C.n : 0;
    const nod = v.reg === 'C' ? (sec.nod || 0) / DIM.C.n : 0;
    const fl = v.rest + sp[0] * share + nk[0] * nshare + nod;
    const lat = sp[1] * share + nk[1] * nshare;
    const tw = sp[2] * share + nk[2] * nshare;
    F = fmul(F, frot(mm(ry(tw), mm(rx(fl), rz(-lat)))));
    fr[v.key] = F;
    F = fmul(F, ftr([0, v.h, 0]));
  }
  const hd = c.head || [0, 0, 0];
  fr.headAttach = fmul(F, frot(mm(ry(hd[1]), mm(rx(hd[0]), rz(-hd[2])))));
  fr.head = fr.headAttach;
  if (c.headToss) {
    // free flight: baseline drifts linearly from the launch to the catch frame, plus a gravity parabola
    const { u, T, g, launch, land, turns } = c.headToss;
    const tau = u * T;
    const base = lerp3(launch.t, land.t, u);
    const t = add(base, [0, 0.5 * g * tau * (T - tau), 0]);
    const R = mm(slerpR(launch.R, land.R, u), ry(2 * Math.PI * turns * u));
    fr.head = { R, t };
  }
  // a detached skull: the head frame is given directly (held in a hand, or in free flight)
  if (c.headFrame) fr.head = c.headFrame;
  fr.jaw = fmul(fr.head, fmul(ftr([0, 7, -3]), frot(rx(clamp((c.jaw || 0) + (sec.jaw || 0), 0, 1.1) * 0.55))));
  fr.chest = fmul(fr.T6, ftr([0, 3, 16]));
  fr.sternum = fmul(fr.T4, ftr([0, 2, 34]));

  // ribs: elevation about the rib's own axis (rattle springs + ring after a strike)
  const ribAngle = (i, s) => (c.ribs ? c.ribs[i - 1] : 0) + (s < 0 ? sec.ribs[i - 1] : sec.ribsL[i - 1]) + (c.ring ? c.ring(i, s) : 0);
  for (let i = 1; i <= 12; i++) {
    for (const s of SIDES) {
      const key = `rib${i}${sideName(s)}`;
      const info = model.ribInfo[key];
      const Tf = fr[`T${i}`];
      const axis = norm(sub(info.local[info.local.length - 1], [0, 0, 0]));
      const ax = norm([axis[0], axis[1] * 0.3, Math.abs(axis[2]) + 0.3]);
      fr[key] = fmul(Tf, fmul(ftr(info.attach), frot(rotAxis(ax, s * ribAngle(i, s)))));
    }
  }
  const ribPoint = (key, k) => fapp(fr[key], model.ribInfo[key].local[k]);
  const ribEnd = (key) => { const L = model.ribInfo[key].local; return fapp(fr[key], L[L.length - 1]); };
  // strike point on a (left) rib: on the front-lateral part of the curve; outward normal
  const strikeK = (key) => { const th = model.ribInfo[key].th; let k = 0; while (k < th.length - 1 && th[k] < STRIKE_TH) k++; return k; };
  const strike = (rib) => ribPoint(`rib${rib}L`, strikeK(`rib${rib}L`));
  // outward surface normal at the strike point: perpendicular to the rib's centre-line (the rib is a
  // tube of radius 2.7), aimed out, up and a little toward the camera so the blow reads from the front
  const strikeNormal = (rib) => {
    const key = `rib${rib}L`, k = strikeK(key), L = model.ribInfo[key].local;
    const p = ribPoint(key, k);
    const tg = norm(sub(ribPoint(key, Math.min(L.length - 1, k + 1)), ribPoint(key, Math.max(0, k - 1))));
    const perp = (v) => sub(v, scl(tg, dot(v, tg)));
    const w = STRIKE_N;
    return norm(perp(add(scl(col(fr.chest.R, 0), w[0]), add(scl(col(fr.chest.R, 1), w[1]), scl(col(fr.chest.R, 2), w[2])))));
  };
  J.strike = {};
  for (let r = 1; r <= 12; r++) J.strike[r] = { p: strike(r), n: strikeNormal(r) };

  // shoulder girdle
  const shrug = c.shrug || [0, 0], prot = c.prot || [0, 0];
  for (const s of SIDES) {
    const n = sideName(s), i = s < 0 ? 0 : 1;
    const SC = fapp(fr.sternum, [s * 6, 13, 0]);
    const d0 = norm([s, 0.1, -0.32]);
    const dirL = mv(mm(rz(s * shrug[i]), ry(-s * prot[i])), d0);
    const dir = mv(fr.sternum.R, dirL);
    fr[`clav${n}`] = frameAlong(SC, dir, col(fr.sternum.R, 2));
    const acr = add(SC, scl(dir, DIM.clav));
    J[`acromion${n}`] = acr;
    fr[`scap${n}`] = { R: mm(fr.sternum.R, mm(rz(s * shrug[i] * 0.7), ry(-s * prot[i] * 0.5))), t: acr };
    J[`shoulder${n}`] = add(acr, mv(fr.sternum.R, [s * -1, -9, 1]));
  }

  // legs (before the arms: hands can target knees)
  for (const s of SIDES) {
    const n = sideName(s), L = c.leg[s < 0 ? 0 : 1];
    const hip = fapp(fr.pelvis, [s * DIM.hip, 0, 0]);
    const fwd = mv(ry(L.heading), [0, 0, 1]);
    const pole = L.pole || norm(add(fwd, [s * (L.kneeOut ?? 0.2) * Math.cos(c.yaw || 0), 0, 0]));
    const ik = twoBone(hip, L.a, DIM.femur, DIM.tibia, pole, 0.992);
    flags.ik.push({ limb: `leg ${n}`, reach: ik.reach, over: ik.over, under: ik.under, err: ik.err });
    J[`hip${n}`] = hip; J[`knee${n}`] = ik.mid; J[`ankle${n}`] = ik.end;
    fr[`fem${n}`] = frameAlong(hip, sub(ik.mid, hip), pole);
    fr[`tib${n}`] = frameAlong(ik.mid, sub(ik.end, ik.mid), col(fr[`fem${n}`].R, 2));
    // kneecap rides in front of the knee, halfway between thigh and shin orientation
    const Rm = slerpR(fr[`fem${n}`].R, fr[`tib${n}`].R, 0.5);
    fr[`pat${n}`] = { R: Rm, t: add(add(ik.mid, scl(col(Rm, 2), 8.5)), scl(col(fr[`fem${n}`].R, 1), 3)) };
    const Rf = mm(ry(L.heading), rx(L.pitch || 0));
    fr[`foot${n}`] = { R: Rf, t: ik.end };
    const toe0 = (L.toe || 0) - (L.pitch || 0) * (L.plantW ?? 0);
    TOES.forEach((lens, k) => {
      const m = MT[k];
      let tf = fmul(fr[`foot${n}`], ftr(sx(m.head, s)));
      lens.forEach((Lj, j) => {
        tf = fmul(tf, frot(rx(j === 0 ? toe0 : (L.toe || 0) * 0.6)));
        fr[`toe${k}${j}${n}`] = tf;
        tf = fmul(tf, ftr([0, 0, Lj]));
      });
      J[`toeTip${k}${n}`] = fapp(fr[`toe${k}${lens.length - 1}${n}`], [0, 0, lens[lens.length - 1]]);
    });
    J[`ball${n}`] = fapp(fr[`foot${n}`], FOOT.ball);
    J[`heel${n}`] = fapp(fr[`foot${n}`], FOOT.heel);
  }

  // arms
  const ctx = { fr, J, strike, strikeNormal };
  const armChain = (s, W, A) => {
    const n = sideName(s);
    const S = J[`shoulder${n}`];
    const pole = A.pole ? norm(mv(fr.chest.R, A.pole)) : norm(mv(fr.chest.R, [s * 0.55, -0.15, -1]));
    const ik = twoBone(S, W, DIM.humerus, DIM.forearm, pole, 0.97);
    const hum = frameAlong(S, sub(ik.mid, S), scl(pole, -1));
    const fore = frameAlong(ik.mid, sub(ik.end, ik.mid), col(hum.R, 2));
    const alpha = (A.pron || 0) * 2.6;
    const hand = fmul(fmul(fore, ftr([0, -DIM.forearm, 0])), frot(mm(ry(-s * alpha), mm(rx(-(A.flex || 0)), rz(s * (A.dev || 0))))));
    return { ik, hum, fore, hand, alpha };
  };
  for (const s of SIDES) {
    const n = sideName(s), A = c.arm[s < 0 ? 0 : 1];
    let W, ch, Rhand = null;
    if (A.detached) {
      // the arm pulled off the shoulder: a rigid straight chain (humerus, forearm, hand) placed by its
      // humeral head S and direction d; n is the normal of its swing plane (elbow/hand frames)
      const { S: S0, d, n: nrm = [0, 0, 1] } = A.detached;
      const mid = add(S0, scl(d, DIM.humerus)), end = add(mid, scl(d, DIM.forearm));
      const hum = frameAlong(S0, d, nrm);
      const fore = frameAlong(mid, d, col(hum.R, 2));
      const alpha = (A.pron || 0) * 2.6;
      const hand = fmul(fmul(fore, ftr([0, -DIM.forearm, 0])), frot(mm(ry(-s * alpha), mm(rx(-(A.flex || 0)), rz(s * (A.dev || 0))))));
      ch = { ik: { mid, end, reach: true, over: 0, under: 0 }, hum, fore, hand, alpha };
      J[`detached${n}`] = true;
    } else if (A.mallet) {
      // The mallet (a spare femur gripped in the fist) is posed by key poses solved in joint space:
      //   {strike: rib, lift, w}  head exactly on the rib surface (contact), then lifted off it by
      //                           cocking the wrist back and raising the forearm (lift 0..1)
      //   {target: [specs], w}    head brought to an arbitrary point (inside the ribcage, ...)
      // Each key is solved by Levenberg-Marquardt over x = [wrist W (chest-local, 3), flex, dev, pron],
      // multi-started from a fixed set of anatomical guesses; the keys are blended in joint space
      // (chest-local wrist + wrist angles), so contacts are exact and in-betweens are smooth arcs.
      const chestInv = finv(fr.chest);
      const toW = (xl) => fapp(fr.chest, xl);
      const LIM = { flex: [-1.0, 1.1], dev: [-0.45, 0.5], pron: [0, 1] };
      const x0 = [A.flex || 0, A.dev || 0, A.pron || 0];
      const clampX = (x) => [x[0], x[1], x[2], clamp(x[3], ...LIM.flex), clamp(x[4], ...LIM.dev), clamp(x[5], ...LIM.pron)];
      const chainOf = (x) => armChain(s, toW([x[0], x[1], x[2]]), { ...A, flex: x[3], dev: x[4], pron: x[5] });
      const PRIOR = 0.3; // wrist-angle prior (u of head error per rad)
      // residuals: mallet head on the target (exact), shaft direction toward Dw (soft, WD u per unit),
      // wrist angles toward the natural pose (prior), and a reach penalty
      const WD = 25, WC = 40;
      const shaftOf = (q) => { const F = malletFrame(q.hand, s); return { h: fapp(F, [0, -48, 0]), d: norm(sub(fapp(F, [0, -48, 0]), F.t)) }; };
      const solve = (Pd, Dw) => {
        const resid = (x) => {
          const q = chainOf(x), m = shaftOf(q);
          const r = scl(sub(m.h, Pd), WC); // contact: stiff (a hard constraint in practice)
          if (Dw) r.push(...scl(sub(m.d, Dw), WD));
          for (let a = 3; a < 6; a++) r.push(PRIOR * (x[a] - x0[a - 3]));
          r.push(q.ik.reach ? 0 : 10 * q.ik.over);
          return { r, q, h: m.h };
        };
        // n-dimensional helpers (the m3 vector ops are 3-D only)
        const dotN = (a, b) => { let v = 0; for (let i = 0; i < a.length; i++) v += a[i] * b[i]; return v; };
        const C2 = (r) => dotN(r, r);
        const Pl = fapp(chestInv, Pd);
        let best = null;
        for (const o of MALLET_STARTS) {
          let x = clampX([Pl[0] + s * o[0], Pl[1] + o[1], Pl[2] + o[2], ...x0]);
          let cur = resid(x), C = C2(cur.r), lam = 1e-2, it = 0;
          for (; it < 40 && C > 1e-12; it++) {
            const Jc = [];
            for (let a = 0; a < 6; a++) { const e = a < 3 ? 0.02 : 0.0005; const xp = x.slice(); xp[a] += e; const rp = resid(xp).r; Jc.push(rp.map((v, i) => (v - cur.r[i]) / e)); }
            const Ab = Array.from({ length: 6 }, () => new Array(7).fill(0));
            for (let a = 0; a < 6; a++) {
              for (let b2 = 0; b2 < 6; b2++) Ab[a][b2] = dotN(Jc[a], Jc[b2]) + (a === b2 ? lam * (1 + dotN(Jc[a], Jc[a])) : 0);
              Ab[a][6] = -dotN(Jc[a], cur.r);
            }
            for (let k = 0; k < 6; k++) { // Gauss-Jordan, partial pivoting
              let piv = k; for (let r = k + 1; r < 6; r++) if (Math.abs(Ab[r][k]) > Math.abs(Ab[piv][k])) piv = r;
              [Ab[k], Ab[piv]] = [Ab[piv], Ab[k]];
              const d0 = Ab[k][k] || 1e-12;
              for (let k2 = k; k2 < 7; k2++) Ab[k][k2] /= d0;
              for (let r = 0; r < 6; r++) if (r !== k) { const f_ = Ab[r][k]; for (let k2 = k; k2 < 7; k2++) Ab[r][k2] -= f_ * Ab[k][k2]; }
            }
            const xn = clampX(x.map((v, a) => v + Ab[a][6]));
            const nx = resid(xn), Cn = C2(nx.r);
            if (Cn < C) { x = xn; cur = nx; C = Cn; lam = Math.max(1e-7, lam * 0.3); } else { lam *= 10; if (lam > 1e6) break; }
          }
          if (!best || C < best.C - 1e-9) best = { x, C, it, err: dist(cur.h, Pd) };
        }
        return best;
      };
      let xs = [0, 0, 0, 0, 0, 0], wsum = 0, keyErr = 0, keyIt = 0;
      for (const k of A.mallet) {
        const w = k.w ?? 1;
        if (w < 1e-6) continue;
        let x;
        if (k.strike !== undefined) {
          const Pd = add(strike(k.strike), scl(strikeNormal(k.strike), k.off ?? MALLET_OFF));
          // shaft: from the fist (below, outside) up and in toward the ribs, square to the blow
          const nS = strikeNormal(k.strike);
          const want = mv(fr.chest.R, [s * MALLET_SHAFT[0], MALLET_SHAFT[1], MALLET_SHAFT[2]]);
          const Dw = norm(sub(want, scl(nS, dot(want, nS))));
          const r = solve(Pd, Dw); x = r.x.slice(); keyErr = Math.max(keyErr, r.err); keyIt += r.it;
          // lift: forearm rises and draws back along the rib normal, the wrist cocks back
          const l = k.lift || 0;
          const nL = mv(tr(fr.chest.R), strikeNormal(k.strike));
          x = clampX([x[0] + l * (MALLET_LIFT.up[0] * s + MALLET_LIFT.back * nL[0]), x[1] + l * (MALLET_LIFT.up[1] + MALLET_LIFT.back * nL[1]), x[2] + l * (MALLET_LIFT.up[2] + MALLET_LIFT.back * nL[2]), x[3] + l * MALLET_LIFT.flex, x[4], x[5]]);
        } else {
          const r = solve(resolveSpecs(k.target, ctx)); x = r.x; keyErr = Math.max(keyErr, r.err); keyIt += r.it;
        }
        xs = xs.map((v, a) => v + w * x[a]); wsum += w;
      }
      const xb = xs.map((v) => v / wsum);
      ch = chainOf(xb);
      const contactKey = A.mallet.find((k) => k.strike !== undefined && (k.w ?? 1) / wsum > 0.999 && !((k.lift || 0) > 1e-6) && (k.off ?? MALLET_OFF) === MALLET_OFF);
      if (contactKey) {
        J.malletTarget = add(strike(contactKey.strike), scl(strikeNormal(contactKey.strike), MALLET_OFF));
        J.malletErr = dist(malletHead(ch.hand, s), J.malletTarget);
        J.malletContactRib = contactKey.strike;
      }
      J.malletKeyErr = keyErr; J.malletIters = keyIt;
      J.malletWrist = [xb[3], xb[4], xb[5]];
      J[`wristBend${n}`] = Math.acos(clamp(dot(col(ch.hand.R, 1), col(ch.fore.R, 1)), -1, 1));
    } else {
      W = resolveSpecs(A.specs, ctx);
      ch = armChain(s, W, A);
    }
    flags.ik.push({ limb: `arm ${n}`, reach: ch.ik.reach, over: ch.ik.over, under: ch.ik.under, err: ch.ik.err || 0 });
    J[`elbow${n}`] = ch.ik.mid; J[`wrist${n}`] = ch.ik.end;
    fr[`hum${n}`] = ch.hum; fr[`fore${n}`] = ch.fore; fr[`hand${n}`] = ch.hand;
    // radius: rigid, rotates around the ulna with pronation (crosses over it)
    const P0 = fapp(ch.fore, [s * 3.5, -1, 0]);
    const P1w = fapp(ch.fore, add([s * -3, -53, 0], mv(ry(-s * ch.alpha), [s * 6.5, 0, 0])));
    fr[`rad${n}`] = frameAlong(P0, sub(P1w, P0), col(ch.fore.R, 2));
    // fingers: metacarpals fan from the carpus, phalanges flex toward the palm
    const curl = A.curl || [0.15, 0.15, 0.15, 0.15];
    const spread = A.spread ?? 0.3;
    const lag = (sec.fingers || [0, 0])[s < 0 ? 0 : 1];
    for (let k = 0; k <= 3; k++) {
      const base = sx(HAND.mcBase[k], s);
      const cu = clamp(curl[k] + lag, -0.25, 1.15);
      let R0 = k === 0 ? mm(rz(s * (0.5 + 0.25 * spread)), mm(ry(-s * 0.7), rx(-0.25 * cu))) : mm(rz(s * (2 - k) * 0.09 * (0.4 + spread)), rx(-0.12 * cu));
      let f = fmul(ch.hand, fmul(ftr(base), frot(R0)));
      fr[`mc${k}${n}`] = f;
      f = fmul(f, ftr([0, -HAND.mcLen[k], 0]));
      HAND.ph[k].forEach((Lj, j) => {
        const fl = cu * (k === 0 ? [0.55, 0.75][j] : [0.95, 1.25, 0.8][j]);
        f = fmul(f, frot(rx(-fl)));
        fr[`ph${k}${j}${n}`] = f;
        f = fmul(f, ftr([0, -Lj, 0]));
      });
      J[`fingertip${k}${n}`] = f.t;
    }
    if (A.mallet || A.holdMallet) fr.mallet = malletFrame(ch.hand, s);
  }
  if (!fr.mallet) fr.mallet = null;

  // costal cartilage: flexible curves from rib ends to the sternum (8-10 join the cartilage above)
  for (const s of SIDES) {
    const n = sideName(s);
    let prevMid = null;
    for (let i = 1; i <= 10; i++) {
      const a = ribEnd(`rib${i}${n}`);
      let b;
      if (i <= 7) b = fapp(fr.sternum, [s * 5.5, DIM.sternalY[i - 1], -0.5]);
      else b = prevMid;
      const bulge = scl(norm(add(mv(fr.sternum.R, [s * 0.4, 0, 1]), [0, 0, 0])), 2.2);
      const mid = add(lerp3(a, b, 0.5), bulge);
      const pts = [0, 0.25, 0.5, 0.75, 1].map((u) => add(add(scl(a, (1 - u) ** 2), scl(mid, 2 * u * (1 - u))), scl(b, u * u)));
      dyn[`cart${i}${n}`] = chain(pts, [2.4, 2.2, 2.1, 2.0, 2.0]);
      prevMid = pts[2];
    }
  }
  return { fr, J, flags, dyn };
}

// mallet held in the left hand: handle across the palm, head out of the thumb side
function malletFrame(hand, s) {
  const grip = fapp(hand, [0, -21, 5]);
  const dir = norm(mv(hand.R, [s * 0.95, 0.15, 0.25]));
  const f = frameAlong(add(grip, scl(dir, -10)), dir, col(hand.R, 2));
  return f;
}
// mallet solve constants: multi-start wrist offsets from the head target (chest-local, x mirrored by side),
// contact offset (mallet-head radius 7.2 + rib radius 2.7) and the lift-off motion between strikes
export const MALLET_OFF = 9.9;
const STRIKE_TH = 2.15; // where along each rib the mallet lands (rib-curve angle: lateral side of the cage)
const STRIKE_N = [0.8, 0.25, 0.6]; // blow direction (chest frame, left side): the mallet knocks on the front of the cage
const MALLET_SHAFT = [-0.45, 0.85, 0]; // wanted shaft direction (fist -> head, chest frame, x mirrored): up and inward, square to the blow
const MALLET_STARTS = [[38, -16, -9], [19, 20, -31], [30, 0, -22], [45, -30, 2], [8, 30, -30], [-12, 34, 30]];
const MALLET_LIFT = { up: [4, 5, 0], back: 16, flex: -0.7 };
export function malletHead(hand, s) { return fapp(malletFrame(hand, s), [0, -48, 0]); }

// world transform of every object (after the optional burst-apart effect)
export function objectFrames(model, ev, c) {
  const out = [];
  const burst = c.explode || 0;
  const centre = ev.fr.chest ? fapp(ev.fr.chest, [0, 0, 0]) : [0, 0, 0];
  for (const d of model.defs) {
    let F = d.frame === 'world' ? ev.fr.world : ev.fr[d.frame];
    if (!F) continue;
    if (d.dyn && !ev.dyn[d.dyn]) continue;
    const ctrLocal = d.dyn ? [0, 0, 0] : partsCentre(d);
    let ctr = fapp(F, ctrLocal);
    if (d.dyn) ctr = partsCentre({ parts: ev.dyn[d.dyn] });
    if (c.collapse && d.group !== 'prop' && !(c.collapse.skip && c.collapse.skip(d))) {
      // the skeleton falls to pieces: every object free-falls (film gravity) from where it is to the
      // floor, turning its long axis toward horizontal as it drops; time-reversed it reassembles
      const { tau, g, floorY } = c.collapse;
      const h = (k) => { let x = Math.sin((d.uid + 1) * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
      const info = collapseInfo(d);
      const restY = (typeof floorY === 'function' ? floorY(ctr) : floorY) + info.thick;
      const drop = Math.max(0, ctr[1] - restY);
      const tHit = Math.sqrt((2 * drop) / g) + 1e-9;
      const tf = Math.min(tau, tHit), s = tf / tHit;
      const vx = (h(1) - 0.5) * 120, vz = (h(2) - 0.5) * 80;
      const disp = [vx * tf, -(0.5 * g * tf * tf), vz * tf];
      let Rc = I3;
      if (info.axis) {
        const L = norm(mv(F.R, info.axis));
        const horiz = [L[0], 0, L[2]];
        const hl = Math.hypot(L[0], L[2]);
        if (hl > 1e-6 && Math.abs(L[1]) > 1e-6) {
          const ax = norm(cross(L, [L[0] / hl, 0, L[2] / hl]));
          Rc = rotAxis(ax, Math.acos(clamp(hl, -1, 1)) * s);
        } else if (hl <= 1e-6) Rc = rotAxis([1, 0, 0], (Math.PI / 2) * s);
        void horiz;
      }
      Rc = mm(rotAxis([0, 1, 0], (h(3) - 0.5) * 2.5 * s), Rc);
      F = { R: mm(Rc, F.R), t: add(add(mv(Rc, sub(F.t, ctr)), ctr), disp) };
      ctr = add(ctr, disp);
    }
    if (burst > 0 && d.group !== 'prop') {
      const key = d.burstWith ? model.defs.find((q) => q.name === d.burstWith) : d;
      const h = (k) => { let x = Math.sin((key.uid + 1) * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
      if (d.burstWith) ctr = fapp(F, partsCentre(key));
      const out_ = norm(add(sub(ctr, centre), [h(1) * 30 - 15, 20 + h(2) * 30, h(3) * 30 - 15]));
      // leg and foot bones spray sideways rather than down; nothing is driven into the ground
      out_[1] = Math.max(out_[1], -0.2);
      const disp = scl(norm(out_), burst * (34 + 70 * h(4)));
      const floor = Math.min(ctr[1], 4);
      if (ctr[1] + disp[1] < floor) disp[1] = floor - ctr[1];
      const axis = norm([h(5) - 0.5, h(6) - 0.5, h(7) - 0.5]);
      const Rb = rotAxis(axis, burst * (0.8 + 2.4 * h(8)) * (h(9) < 0.5 ? -1 : 1));
      // rotate the object about its own centre, then translate: still a rigid motion
      F = { R: mm(Rb, F.R), t: add(add(mv(Rb, sub(F.t, ctr)), ctr), disp) };
      ctr = add(ctr, disp);
    }
    out.push({ def: d, F, ctr });
  }
  return out;
}
// per-object collapse data: long axis (from its first capsule/cylinder) and resting thickness
const COLLAPSE = new WeakMap();
function collapseInfo(d) {
  if (COLLAPSE.has(d)) return COLLAPSE.get(d);
  const parts = d.pieces ? d.pieces.flat() : d.parts || [];
  let axis = null, rs = [];
  for (const p of parts) {
    if ((p.t === 'cap' || p.t === 'cyl') && !axis) { const v = sub(p.b, p.a); if (Math.hypot(...v) > 8) axis = norm(v); }
    if (p.t === 'sph') rs.push(p.r); else if (p.t === 'cap') rs.push((p.ra + p.rb) / 2); else if (p.t === 'cyl') rs.push(p.r); else if (p.t === 'ell') rs.push(Math.min(...p.r));
  }
  const thick = clamp(rs.length ? rs.reduce((a, b) => a + b, 0) / rs.length : 3, 1.5, 10);
  const info = { axis, thick };
  COLLAPSE.set(d, info);
  return info;
}
export function partsCentre(d) {
  let s = [0, 0, 0], n = 0;
  const parts = d.pieces ? d.pieces.flat() : d.parts;
  for (const p of parts) {
    if (p.t === 'sph' || p.t === 'ell') { s = add(s, p.c); n++; }
    else if (p.t === 'cap' || p.t === 'cyl') { s = add(s, scl(add(p.a, p.b), 0.5)); n++; }
    else if (p.t === 'poly') { for (const q of p.pts) { s = add(s, q); n++; } }
  }
  if (d.socket) return d.socket.c;
  if (d.decals && d.decals[0] && d.decals[0].pts && !n) { const q = d.decals[0].pts; return scl(q.reduce((a, b) => add(a, b), [0, 0, 0]), 1 / q.length); }
  return n ? scl(s, 1 / n) : [0, 0, 0];
}

// joint pairs that must coincide (child frame origin = parent point) — used by the QA
export const CONNECT = (() => {
  const L = [];
  for (const s of SIDES) {
    const n = sideName(s);
    L.push([`tib${n}`, `fem${n}`, [0, -DIM.femur, 0]], [`fore${n}`, `hum${n}`, [0, -DIM.humerus, 0]]);
  }
  return L;
})();
export const LIMBS = {
  femur: DIM.femur, tibia: DIM.tibia, humerus: DIM.humerus, forearm: DIM.forearm, radius: DIM.radius, clavicle: DIM.clav,
};
