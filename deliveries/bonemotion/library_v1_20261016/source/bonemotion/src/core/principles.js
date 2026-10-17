// The principles of animation as code.
//
// action(spec) builds the canonical envelope of one movement, normalized so that
//   u = 0   the rest / starting pose        u = 1   the goal pose
//   u < 0   anticipation (moving AWAY from the goal first)
//   u > 1   follow-through (carried PAST the goal by momentum), then settling back to 1
// Phases, in order (Spanish labels for the on-screen phase bar):
//   prep    Preparación   getting ready (other channels move; this one waits at 0)
//   antic   Anticipación  counter-move to the anticipation extreme, slow in
//   hold    (moving hold) the extreme is held but keeps drifting a little, so it stays alive
//   exec    Ejecución     the action: accelerates from the extreme into the hit (fast, "snappy")
//   follow  Proyección    momentum carries past the goal with constant deceleration
//   settle  Asentamiento  a damped spring returns to the goal: velocity is continuous everywhere
// Every boundary is C1 (no velocity jumps); the hit velocity is explicit, so the moment of contact
// or release can be matched to physics.
import { clamp, hermite, hermiteD, ease } from './curves.js';

export const PHASE_LABEL = {
  prep: 'Preparación', antic: 'Anticipación', hold: 'Anticipación', exec: 'Ejecución', follow: 'Proyección', settle: 'Asentamiento',
};
export const PHASE_ORDER = ['prep', 'antic', 'exec', 'follow', 'settle'];

export function action({ start = 0, prep = 0, antic = { dur: 0.3, amt: 0.15 }, hold = 0, holdDrift = 0.06, exec = { dur: 0.25, snap: 2.2 }, follow = { dur: 0.15 }, settle = { dur: 0.6, f: 2.2, z: 0.45 } } = {}) {
  const A = antic.amt ?? 0, tA0 = start + prep, tA1 = tA0 + (antic.dur || 0);
  const tH1 = tA1 + hold;
  const AH = A * (1 + (hold > 0 ? holdDrift : 0)); // the moving hold drifts a little deeper
  const snap = clamp(exec.snap ?? 2.2, 0, 3); // <= 3 keeps the exec segment monotonic
  const tE1 = tH1 + exec.dur;
  const vp = (snap * (1 + AH)) / exec.dur; // u/s at the hit
  let fdur = follow.dur ?? 0;
  if (follow.amt !== undefined) fdur = (2 * follow.amt) / vp; // overshoot reached with constant deceleration
  const over = (vp * fdur) / 2;
  const tF1 = tE1 + fdur;
  const sd = settle.dur ?? 0.6, w = 2 * Math.PI * (settle.f ?? 2.2), z = clamp(settle.z ?? 0.45, 0.05, 0.999);
  const wd = w * Math.sqrt(1 - z * z);
  const tS1 = tF1 + sd;
  const at = (t) => {
    if (t <= tA0) return 0;
    if (t < tA1) return -A * ease.smooth((t - tA0) / (tA1 - tA0));
    if (t < tH1) return -A - (AH - A) * ease.smooth((t - tA1) / hold);
    if (t < tE1) { const h = exec.dur; return hermite(-AH, 1, 0, vp * h, (t - tH1) / h); }
    if (t < tF1) { const tau = t - tE1; return 1 + vp * tau - (vp / (2 * fdur)) * tau * tau; }
    if (sd <= 0) return 1 + over;
    const tau = Math.min(t, tS1) - tF1;
    const s = Math.exp(-z * w * tau) * (Math.cos(wd * tau) + ((z * w) / wd) * Math.sin(wd * tau));
    return 1 + over * s * (1 - ease.smoother(Math.min(1, tau / sd)));
  };
  const vel = (t) => {
    if (t > tH1 && t < tE1) { const h = exec.dur; return hermiteD(-AH, 1, 0, vp * h, (t - tH1) / h) / h; }
    if (t >= tE1 && t < tF1) return vp - (vp / fdur) * (t - tE1);
    const e = 1e-4; return (at(t + e) - at(t - e)) / (2 * e);
  };
  const phases = [
    prep > 0 && { name: 'prep', t0: start, t1: tA0 },
    { name: 'antic', t0: tA0, t1: tH1 },
    { name: 'exec', t0: tH1, t1: tE1 },
    fdur > 0 && { name: 'follow', t0: tE1, t1: tF1 },
    sd > 0 && { name: 'settle', t0: tF1, t1: tS1 },
  ].filter(Boolean);
  return { at, vel, phases, start, tAntic: tA1, tHit: tE1, tOver: tF1, end: tS1, vHit: vp, over, antic: AH };
}

// map an envelope onto a channel: value = a + (b - a) * u   (numbers or arrays)
export function along(env, a, b) {
  const f = (u) => (Array.isArray(a) ? a.map((x, i) => x + (b[i] - x) * u) : a + (b - a) * u);
  return (t) => f(env.at(t));
}

// overlapping action / successive breaking of joints: the same motion, delayed along a chain
export const delayed = (fn, dt) => (t) => fn(t - dt);

// drag + follow-through on any signal: a damped spring chasing the signal (critically or under-damped).
// Integrated once at fixed dt over [t0, t1] (deterministic), then sampled with linear interpolation.
export function springFollow(signal, { t0, t1, f = 3, z = 0.5, dt = 1 / 480 }) {
  const w = 2 * Math.PI * f;
  const n = Math.ceil((t1 - t0) / dt) + 1;
  const s0 = signal(t0);
  const vec = Array.isArray(s0);
  const dim = vec ? s0.length : 1;
  const get = (t) => (vec ? signal(t) : [signal(t)]);
  let x = get(t0).slice(), v = new Array(dim).fill(0);
  const X = new Float64Array(n * dim);
  for (let i = 0; i < n; i++) {
    for (let d = 0; d < dim; d++) X[i * dim + d] = x[d];
    // semi-implicit Euler with 4 sub-steps
    for (let k = 0; k < 4; k++) {
      const tt = t0 + (i + k / 4) * dt, target = get(tt), h = dt / 4;
      for (let d = 0; d < dim; d++) { v[d] += (w * w * (target[d] - x[d]) - 2 * z * w * v[d]) * h; x[d] += v[d] * h; }
    }
  }
  return (t) => {
    if (t <= t0) return signal(t);
    const fi = Math.min(n - 1 - 1e-9, (t - t0) / dt), i = Math.floor(fi), u = fi - i;
    if (t >= t1) { const out = []; for (let d = 0; d < dim; d++) out.push(X[(n - 1) * dim + d] + (get(t)[d] - get(t1)[d])); return vec ? out : out[0]; }
    const out = [];
    for (let d = 0; d < dim; d++) out.push(X[i * dim + d] * (1 - u) + X[(i + 1) * dim + d] * u);
    return vec ? out : out[0];
  };
}

// analytic step response of a damped spring (0 -> 1), velocity zero at the start
export function springStep(tau, f = 2, z = 0.4) {
  if (tau <= 0) return 0;
  const w = 2 * Math.PI * f;
  if (z >= 1) return 1 - Math.exp(-w * tau) * (1 + w * tau);
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * tau) * (Math.cos(wd * tau) + ((z * w) / wd) * Math.sin(wd * tau));
}

// a blend weight that comes in and goes out with C1 continuity
export function window(t, a, b, c, d) {
  if (t <= a || t >= d) return 0;
  if (t < b) return ease.smooth((t - a) / (b - a));
  if (t <= c) return 1;
  return 1 - ease.smooth((t - c) / (d - c));
}

// which phase of a list is active at t (for the phase bar); null between phases
export function phaseAt(phases, t) {
  for (const p of phases) if (t >= p.t0 && t < p.t1) return p.name;
  return null;
}
