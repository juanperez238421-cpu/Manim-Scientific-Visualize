// Interpolation primitives. Everything is a pure function of time, so any frame can be rendered
// on its own (seek-safe) and every curve can be differentiated analytically for QA.
//
//   ease.*            normalized easing u -> u (0 -> 0, 1 -> 1)
//   hermite / hermiteD cubic Hermite segment value / derivative (tangents already scaled by the span)
//   track(keys)       keyframed scalar or vector channel, C1, with per-key tangent control
//   arcPoint          point on a circular arc through a bulge (motion along arcs, not straight lines)

export const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
export const lerp = (a, b, u) => a + (b - a) * u;
export const prog = (x, a, b) => clamp((x - a) / (b - a), 0, 1);
export const lerpV = (a, b, u) => a.map((x, i) => x + (b[i] - x) * u);

export const ease = {
  linear: (u) => u,
  smooth: (u) => u * u * (3 - 2 * u), // C1 at the ends
  smoother: (u) => u * u * u * (u * (6 * u - 15) + 10), // C2 at the ends
  inQuad: (u) => u * u,
  outQuad: (u) => 1 - (1 - u) * (1 - u),
  inCubic: (u) => u * u * u,
  outCubic: (u) => 1 - (1 - u) ** 3,
  inOutCubic: (u) => (u < 0.5 ? 4 * u * u * u : 1 - (-2 * u + 2) ** 3 / 2),
  inOutSine: (u) => 0.5 - 0.5 * Math.cos(Math.PI * u),
  outBack: (u, s = 1.7) => 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2,
  inBack: (u, s = 1.7) => (s + 1) * u * u * u - s * u * u,
};
// derivative of the normalized eases (per unit u), for velocity bookkeeping
export const easeD = {
  linear: () => 1,
  smooth: (u) => 6 * u * (1 - u),
  smoother: (u) => 30 * u * u * (u - 1) * (u - 1),
  inOutSine: (u) => 0.5 * Math.PI * Math.sin(Math.PI * u),
};

// cubic Hermite on [0,1]: p0 -> p1 with end slopes m0, m1 (d value / d u)
export function hermite(p0, p1, m0, m1, u) {
  const u2 = u * u, u3 = u2 * u;
  return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * m1;
}
export function hermiteD(p0, p1, m0, m1, u) {
  const u2 = u * u;
  return (6 * u2 - 6 * u) * p0 + (3 * u2 - 4 * u + 1) * m0 + (-6 * u2 + 6 * u) * p1 + (3 * u2 - 2 * u) * m1;
}
export function hermiteDD(p0, p1, m0, m1, u) {
  return (12 * u - 6) * p0 + (6 * u - 4) * m0 + (-12 * u + 6) * p1 + (6 * u - 2) * m1;
}

// ------------------------------------------------------------------ keyframe tracks
// keys: [{ t, v, slope?, mode? }]
//   v      number or array (component-wise)
//   slope  explicit velocity (units/s) through the key — e.g. an exact release velocity
//   mode   'auto'   (default) Catmull-Rom tangent, limited so the curve never overshoots its keys
//          'flat'   zero slope: an ease in and out of the key (a hold, an extreme)
//          'free'   Catmull-Rom tangent without limiting (keeps overshoot, for loose follow-through)
//          'linear' straight segment to the next key
//          'step'   jump at the next key
// Values before the first key / after the last are held. Returns { at(t), vel(t), acc(t), keys }.
export function track(keys) {
  const K = keys.slice().sort((a, b) => a.t - b.t);
  const vec = Array.isArray(K[0].v);
  const dim = vec ? K[0].v.length : 1;
  const val = (k, d) => (vec ? k.v[d] : k.v);
  const n = K.length;
  // tangents (units / s) per key and component
  const tan = K.map((k, i) => {
    const out = [];
    for (let d = 0; d < dim; d++) {
      if (k.slope !== undefined) { out.push(vec ? k.slope[d] : k.slope); continue; }
      if (k.mode === 'flat' || n === 1) { out.push(0); continue; }
      const p = K[Math.max(0, i - 1)], q = K[Math.min(n - 1, i + 1)];
      if (i === 0 || i === n - 1) { out.push(0); continue; } // ends ease in/out
      const dl = (val(k, d) - val(p, d)) / (k.t - p.t), dr = (val(q, d) - val(k, d)) / (q.t - k.t);
      if (k.mode === 'free') { out.push((val(q, d) - val(p, d)) / (q.t - p.t)); continue; }
      // monotone (Fritsch-Carlson): no overshoot between keys, zero slope at local extremes
      if (dl * dr <= 0) { out.push(0); continue; }
      const hl = k.t - p.t, hr = q.t - k.t;
      const w1 = 2 * hr + hl, w2 = hr + 2 * hl; // weighted harmonic mean (Brodlie)
      out.push((w1 + w2) / (w1 / dl + w2 / dr));
    }
    return out;
  });
  const seg = (t) => {
    if (t <= K[0].t) return -1;
    if (t >= K[n - 1].t) return n - 1;
    let lo = 0, hi = n - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (K[m].t <= t) lo = m; else hi = m; }
    return lo;
  };
  const evalD = (t, order) => {
    const i = seg(t);
    const res = [];
    for (let d = 0; d < dim; d++) {
      if (i < 0 || i >= n - 1) { res.push(order ? 0 : val(K[i < 0 ? 0 : n - 1], d)); continue; }
      const a = K[i], b = K[i + 1], h = b.t - a.t, u = (t - a.t) / h;
      if (a.mode === 'step') { res.push(order ? 0 : val(a, d)); continue; }
      if (a.mode === 'linear') { res.push(order === 0 ? lerp(val(a, d), val(b, d), u) : order === 1 ? (val(b, d) - val(a, d)) / h : 0); continue; }
      const p0 = val(a, d), p1 = val(b, d), m0 = tan[i][d] * h, m1 = tan[i + 1][d] * h;
      if (order === 0) res.push(hermite(p0, p1, m0, m1, u));
      else if (order === 1) res.push(hermiteD(p0, p1, m0, m1, u) / h);
      else res.push(hermiteDD(p0, p1, m0, m1, u) / (h * h));
    }
    return vec ? res : res[0];
  };
  return { at: (t) => evalD(t, 0), vel: (t) => evalD(t, 1), acc: (t) => evalD(t, 2), keys: K, t0: K[0].t, t1: K[n - 1].t };
}

// a point moving from a to b along a circular arc whose middle is pushed out by `bulge` (vector)
// u in [0,1]; bulge = 0 gives the straight line. Arcs read as natural; straight lines read mechanical.
export function arcPoint(a, b, bulge, u) {
  // quadratic Bezier whose control point (mid + 2 bulge) makes it pass through mid + bulge at u = 1/2
  const ctrl = a.map((x, i) => 0.5 * (x + b[i]) + 2 * bulge[i]);
  return a.map((x, i) => (1 - u) * (1 - u) * x + 2 * u * (1 - u) * ctrl[i] + u * u * b[i]);
}

// smooth minimum (C1): behaves like min(a, b) away from the crossover, rounds it within k
export function smin(a, b, k) {
  const h = clamp(0.5 + (0.5 * (b - a)) / k, 0, 1);
  return lerp(b, a, h) - k * h * (1 - h);
}
