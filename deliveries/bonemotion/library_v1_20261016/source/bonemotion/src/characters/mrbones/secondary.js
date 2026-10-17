// Secondary motion for Mr. Bones: damped springs driven by the accelerations of the primary motion
// (jaw lag and chatter against its stop, a hat that bounces under gravity on the cranium, 24 ribs that
// rattle, head bobble, tail-bone wag, finger lag). Integrated once per clip over [t0, t1] at fixed dt
// (deterministic, seek-safe), then sampled by interpolation at any frame rate.
import { evaluate, ZERO_SEC } from './model.js';
import { col, dot } from '../../core/m3.js';

export const SEC_PARAMS = {
  dt: 1 / 240, sub: 6, maxAcc: 60000,
  jaw: { f: 4.5, z: 0.25, k: 0.047, e: 0.4 },
  hat: { e: 0.3, tiltF: 2.5, tiltZ: 0.2, tiltK: 0.0123 },
  ribs: { f: 3.4, df: 0.07, z: 0.14, ky: 0.0046, kx: 0.0046 },
  nod: { f: 3, z: 0.3, k: 0.0057 },
  coccyx: { f: 3, z: 0.15, k: 0.0355 },
  fingers: { f: 4, z: 0.3, k: 0.026 },
};

// controlsAt(t) -> rig controls; gravity in u/s^2; impulses [{t, hat?, jaw?, ribs?}] kick the springs
export function simulateSecondary(model, controlsAt, { t0 = 0, t1, gravity, impulses = [], hatOnHead = () => true }) {
  const P = SEC_PARAMS, dt = P.dt;
  const N = Math.round((t1 - t0) / dt) + 1;
  const S = { head: [], chest: [], pelvis: [], hand: [[], []], palm: [[], []], jaw0: [] };
  for (let i = 0; i < N; i++) {
    const c = controlsAt(t0 + i * dt);
    const ev = evaluate(model, c, ZERO_SEC);
    S.head.push(ev.fr.head.t); S.chest.push(ev.fr.chest.t); S.pelvis.push(ev.fr.pelvis.t);
    for (const j of [0, 1]) { const h = ev.fr[j ? 'handL' : 'handR']; S.hand[j].push(h.t); S.palm[j].push(col(h.R, 2)); }
    S.jaw0.push(c.jaw || 0);
  }
  const acc = (arr, i) => {
    const a = arr[Math.max(0, i - 1)], b = arr[i], c = arr[Math.min(N - 1, i + 1)];
    const v = [0, 1, 2].map((k) => (a[k] - 2 * b[k] + c[k]) / (dt * dt));
    const m = Math.hypot(...v);
    return m > P.maxAcc ? v.map((x) => (x * P.maxAcc) / m) : v;
  };
  const A = { head: [], chest: [], pelvis: [], hand: [[], []] };
  for (let i = 0; i < N; i++) {
    A.head.push(acc(S.head, i)); A.chest.push(acc(S.chest, i)); A.pelvis.push(acc(S.pelvis, i));
    for (const j of [0, 1]) A.hand[j].push(acc(S.hand[j], i));
  }
  const w = (f) => 2 * Math.PI * f;
  const st = { jaw: [0, 0], hat: [0, 0], tilt: [0, 0], nod: [0, 0], coc: [0, 0], fing: [[0, 0], [0, 0]], ribs: Array.from({ length: 24 }, () => [0, 0]) };
  const spring = (s, om, z, drive, h) => { const a = -om * om * s[0] - 2 * z * om * s[1] + drive; s[1] += a * h; s[0] += s[1] * h; };
  const imp = impulses.map((x) => ({ ...x, i: Math.round((x.t - t0) / dt), done: false }));
  const out = [];
  for (let i = 0; i < N; i++) {
    const t = t0 + i * dt;
    for (const x of imp) if (!x.done && i >= x.i) { x.done = true; if (x.hat) st.hat[1] += x.hat; if (x.jaw) st.jaw[1] += x.jaw; if (x.ribs) st.ribs.forEach((r) => (r[1] += x.ribs)); }
    const onHead = hatOnHead(t);
    if (!onHead) { st.hat = [0, 0]; st.tilt = [0, 0]; }
    out.push({ jaw: st.jaw[0], hatLift: st.hat[0], hatTilt: st.tilt[0], nod: st.nod[0], coccyx: st.coc[0],
      ribs: st.ribs.slice(0, 12).map((r) => r[0]), ribsL: st.ribs.slice(12).map((r) => r[0]), fingers: [st.fing[0][0], st.fing[1][0]] });
    if (i === N - 1) break;
    const h = dt / P.sub;
    for (let k = 0; k < P.sub; k++) {
      const u = k / P.sub;
      const lerpA = (arr) => arr[i].map((x, d) => x + (arr[i + 1][d] - x) * u);
      const ah = lerpA(A.head), ac = lerpA(A.chest), ap = lerpA(A.pelvis);
      spring(st.jaw, w(P.jaw.f), P.jaw.z, -P.jaw.k * ah[1], h);
      const jaw0 = S.jaw0[i];
      if (jaw0 + st.jaw[0] < 0 && st.jaw[1] < 0) { st.jaw[0] = -jaw0; st.jaw[1] = -P.jaw.e * st.jaw[1]; }
      if (onHead) {
        st.hat[1] += -(gravity + ah[1]) * h; st.hat[0] += st.hat[1] * h;
        if (st.hat[0] < 0) { st.hat[0] = 0; if (st.hat[1] < 0) st.hat[1] = -P.hat.e * st.hat[1]; }
        spring(st.tilt, w(P.hat.tiltF), P.hat.tiltZ, P.hat.tiltK * ah[0], h);
      }
      spring(st.nod, w(P.nod.f), P.nod.z, -P.nod.k * ac[1], h);
      spring(st.coc, w(P.coccyx.f), P.coccyx.z, -P.coccyx.k * ap[0], h);
      for (let r = 0; r < 24; r++) {
        const side = r < 12 ? -1 : 1, idx = r % 12;
        spring(st.ribs[r], w(P.ribs.f + P.ribs.df * idx), P.ribs.z, -P.ribs.ky * ac[1] + side * P.ribs.kx * ac[0], h);
      }
      for (const j of [0, 1]) spring(st.fing[j], w(P.fingers.f), P.fingers.z, (P.fingers.k * dot(lerpA(A.hand[j]), S.palm[j][i])) / 1000, h);
    }
  }
  const lerpRec = (a, b, u) => {
    const o = {};
    for (const k of Object.keys(a)) o[k] = Array.isArray(a[k]) ? a[k].map((x, i) => x + (b[k][i] - x) * u) : a[k] + (b[k] - a[k]) * u;
    return o;
  };
  return {
    at(t) {
      const fi = Math.max(0, Math.min(N - 1 - 1e-9, (t - t0) / dt)), i = Math.floor(fi);
      return lerpRec(out[i], out[Math.min(N - 1, i + 1)], fi - i);
    },
    N, dt,
  };
}
export { ZERO_SEC };
