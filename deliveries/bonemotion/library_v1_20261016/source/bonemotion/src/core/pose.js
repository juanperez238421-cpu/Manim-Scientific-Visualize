// The character-agnostic pose: what every clip produces and every character adapter consumes.
//
// Coordinates: rig units of the character, y up, ground at y = 0; index 0 = right limb, 1 = left.
//   root   { p: pelvis position, yaw: facing (0 = toward +z / camera), tilt: [pitch, roll] }
//   spine  [flex, lateral, twist]  distributed over the column      neck, head: same convention
//   shrug, prot  [R, L] shoulder girdle elevation / protraction
//   legs[i] { ankle: world point, heading, pitch (+ = toes down), toe, plantW (0..1 toes kept flat),
//            kneeOut, pole? }
//   arms[i] { specs: [{ space: 'world'|'chest'|'pelvis'|'head', p, w }], pole?, curl[4], spread,
//            pron, flex, dev, detached? }
//   face    { jaw, look: [x, y], pupil }
//   props   character-specific objects (hat, cane, skull, ...): never blended, last writer wins
// A pose is plain data, so it can be mixed, layered, mirrored, stored and learned from.

export function clone(p) { return JSON.parse(JSON.stringify(p)); }

// recursive blend a -> b by u (numbers, numeric arrays, objects). Arm target specs are blended by
// weighting (resolved later in the rig), discrete fields switch at u = 0.5, props are taken from b
// when u >= 0.5 (callers that need a prop hand-off do it explicitly).
export function mix(a, b, u) {
  if (u <= 0) return a;
  if (u >= 1) return b;
  return mixAny(a, b, u, '');
}
function mixAny(a, b, u, key) {
  if (a === undefined) return b;
  if (b === undefined) return a;
  if (typeof a === 'number' && typeof b === 'number') return a + (b - a) * u;
  if (key === 'specs') return [...a.map((s) => ({ ...s, w: (s.w ?? 1) * (1 - u) })), ...b.map((s) => ({ ...s, w: (s.w ?? 1) * u }))];
  if (key === 'props' || key === 'fx') return u < 0.5 ? a : b;
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return u < 0.5 ? a : b;
    return a.map((x, i) => mixAny(x, b[i], u, ''));
  }
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const out = {};
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) out[k] = mixAny(a[k], b[k], u, k);
    return out;
  }
  return u < 0.5 ? a : b;
}

// additive layer: base + w * (layer - ref) on the numeric channels listed (for breathing, sway...)
export function addLayer(base, delta, w = 1) {
  const out = clone(base);
  const walk = (o, d) => {
    for (const k of Object.keys(d)) {
      if (typeof d[k] === 'number') o[k] = (o[k] || 0) + w * d[k];
      else if (Array.isArray(d[k]) && typeof d[k][0] === 'number') o[k] = (o[k] || d[k].map(() => 0)).map((x, i) => x + w * (d[k][i] || 0));
      else if (d[k] && typeof d[k] === 'object') { o[k] = o[k] || {}; walk(o[k], d[k]); }
    }
  };
  walk(out, delta);
  return out;
}

// mirror left <-> right across the character's sagittal plane (x -> -x in root space at yaw 0)
export function mirror(p) {
  const q = clone(p);
  const fx = (v) => [-v[0], v[1], v[2]];
  q.root.p = fx(q.root.p); q.root.yaw = -q.root.yaw; q.root.tilt = [q.root.tilt[0], -q.root.tilt[1]];
  for (const k of ['spine', 'neck', 'head']) q[k] = [q[k][0], -q[k][1], -q[k][2]];
  q.legs = [p.legs[1], p.legs[0]].map((L) => ({ ...clone(L), ankle: fx(L.ankle), heading: -L.heading }));
  q.arms = [p.arms[1], p.arms[0]].map((A) => ({ ...clone(A), specs: A.specs.map((s) => ({ ...s, p: fx(s.p) })) }));
  q.shrug = [p.shrug[1], p.shrug[0]]; q.prot = [p.prot[1], p.prot[0]];
  if (q.face) q.face.look = [-q.face.look[0], q.face.look[1]];
  return q;
}
