// Exact kinematics used by the clips. Wherever physics decides a motion (a flight, a release, a
// catch, a spin) the clip takes it from here, in closed form whenever one exists, so the QA can
// compare the drawn motion with the formula to round-off.
//
// Units: rig units u and seconds. A character supplies K (u per metre); gravity in u/s^2 is g * K.
import { add, scl, sub, dot, len, norm } from './m3.js';

// ------------------------------------------------------------------ free flight
// p(t) = p0 + v0 t + 1/2 a t^2  (a = [0, -g, 0])
export function projectile(p0, v0, g) {
  const a = [0, -g, 0];
  const at = (t) => add(add(p0, scl(v0, t)), scl(a, 0.5 * t * t));
  const vel = (t) => add(v0, scl(a, t));
  // time at which the height is y on the way down (largest root), null if never reached
  const timeToY = (y) => {
    const A = -0.5 * g, B = v0[1], C = p0[1] - y, D = B * B - 4 * A * C;
    if (D < 0) return null;
    const r1 = (-B - Math.sqrt(D)) / (2 * A), r2 = (-B + Math.sqrt(D)) / (2 * A);
    return Math.max(r1, r2);
  };
  return { at, vel, timeToY, apexT: Math.max(0, v0[1] / g), apexY: p0[1] + Math.max(0, v0[1]) ** 2 / (2 * g), p0, v0, g };
}

// launch velocity that carries p0 to p1 in time T under gravity g (exact)
export const launchVelocity = (p0, p1, T, g) => [(p1[0] - p0[0]) / T, (p1[1] - p0[1] + 0.5 * g * T * T) / T, (p1[2] - p0[2]) / T];

// bouncing on a floor (vertical restitution e, horizontal friction factor mu per bounce)
export function bouncing(p0, v0, g, floorY, e = 0.45, mu = 0.8, maxBounces = 6, vStop = 20) {
  const segs = [];
  let p = p0.slice(), v = v0.slice(), t = 0;
  for (let k = 0; k <= maxBounces; k++) {
    const pr = projectile(p, v, g);
    const tc = pr.timeToY(floorY);
    segs.push({ t0: t, pr, t1: t + tc });
    const vc = pr.vel(tc);
    const vy = -e * vc[1];
    p = pr.at(tc); p[1] = floorY;
    t += tc;
    if (vy < vStop) { segs.push({ t0: t, rest: p, t1: Infinity }); break; }
    v = [vc[0] * mu, vy, vc[2] * mu];
  }
  const find = (t) => segs.find((s) => t < s.t1) || segs[segs.length - 1];
  return {
    at: (t) => { if (t <= 0) return p0.slice(); const s = find(t); return s.rest ? s.rest.slice() : s.pr.at(t - s.t0); },
    vel: (t) => { const s = find(t); return s.rest ? [0, 0, 0] : s.pr.vel(t - s.t0); },
    contacts: segs.filter((s) => !s.rest).map((s) => s.t1),
    segs,
  };
}

// ------------------------------------------------------------------ circular motion
// A swing about a centre with constant angular acceleration from rest at theta0 that reaches
// omegaRel exactly at thetaRel (release), at time tRel. Then constant deceleration over dFollow rad.
// dir = +1 counter-clockwise, -1 clockwise (in the swing plane).
export function swingSchedule({ theta0, thetaRel, omegaRel, tRel, dFollow = 1.2 }) {
  const dir = Math.sign(thetaRel - theta0) || 1;
  const sweep = Math.abs(thetaRel - theta0);
  const alpha = (omegaRel * omegaRel) / (2 * sweep); // rad/s^2
  const T = (2 * sweep) / omegaRel;
  const tStart = tRel - T;
  const beta = (omegaRel * omegaRel) / (2 * dFollow);
  const tStop = tRel + omegaRel / beta;
  const theta = (t) => {
    if (t <= tStart) return theta0;
    if (t <= tRel) { const u = t - tStart; return theta0 + dir * 0.5 * alpha * u * u; }
    const u = Math.min(t, tStop) - tRel;
    return thetaRel + dir * (omegaRel * u - 0.5 * beta * u * u);
  };
  const omega = (t) => {
    if (t <= tStart) return 0;
    if (t <= tRel) return dir * alpha * (t - tStart);
    if (t >= tStop) return 0;
    return dir * (omegaRel - beta * (t - tRel));
  };
  return { theta, omega, tStart, tRel, tStop, alpha, beta, dir, T };
}

// The sling: spin-up with constant alpha from rest at theta0, constant omega until theta = thetaRel
// (mod 2 pi) at tRel, release; then a spin-down that stops exactly `stopTurns` turns later.
export function slingSchedule({ theta0, thetaRel, omega, tRel, tUp = 0.8, minTurns = 1, dir = 1, stopTurns = 1 }) {
  const sweepUp = 0.5 * omega * tUp;
  let total = dir * (thetaRel - theta0);
  total = ((total % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
  while (total < sweepUp + minTurns * 2 * Math.PI) total += 2 * Math.PI;
  const T2 = (total - sweepUp) / omega;
  const tS = tRel - tUp - T2;
  const alpha = omega / tUp;
  const beta = (omega * omega) / (2 * 2 * Math.PI * stopTurns);
  const tStop = tRel + omega / beta;
  const theta = (t) => {
    if (t <= tS) return theta0;
    if (t <= tS + tUp) { const u = t - tS; return theta0 + dir * 0.5 * alpha * u * u; }
    if (t <= tRel) return theta0 + dir * (sweepUp + omega * (t - tS - tUp));
    const u = Math.min(t, tStop) - tRel;
    return theta0 + dir * (total + omega * u - 0.5 * beta * u * u);
  };
  const thetaDot = (t) => {
    if (t <= tS) return 0;
    if (t <= tS + tUp) return dir * alpha * (t - tS);
    if (t <= tRel) return dir * omega;
    if (t >= tStop) return 0;
    return dir * (omega - beta * (t - tRel));
  };
  return { theta, thetaDot, tS, tUp, T2, tRel, tStop, alpha, beta, dir, omega, total };
}

// ------------------------------------------------------------------ catching (impulse absorbed)
// The hand meets the object at tCatch moving with it (vIn) and brings it to rest over a distance d
// with constant deceleration a = v^2 / (2 d), in time T = 2 d / v. offset(t): displacement since catch.
export function catchAbsorb({ tCatch, vIn, dist: d }) {
  const v = len(vIn), dir = norm(vIn);
  const a = (v * v) / (2 * d), T = (2 * d) / v;
  const offset = (t) => { const u = Math.max(0, Math.min(t - tCatch, T)); return scl(dir, v * u - 0.5 * a * u * u); };
  const vel = (t) => { const u = t - tCatch; if (u <= 0) return vIn.slice(); if (u >= T) return [0, 0, 0]; return scl(dir, v - a * u); };
  return { offset, vel, a, T, tEnd: tCatch + T, dir, v };
}

// ------------------------------------------------------------------ pendulum (physical, large amplitude)
// theta'' = -(m g d / I) sin(theta) - c theta'   integrated at fixed dt (RK4), sampled by interpolation
export function pendulum({ theta0 = 0, omega0 = 0, w0, damping = 0.4, t0 = 0, t1 = 10, dt = 1 / 960 }) {
  const n = Math.ceil((t1 - t0) / dt) + 1;
  const TH = new Float64Array(n), OM = new Float64Array(n);
  let th = theta0, om = omega0;
  const f = (x, v) => -w0 * w0 * Math.sin(x) - damping * v;
  for (let i = 0; i < n; i++) {
    TH[i] = th; OM[i] = om;
    const k1x = om, k1v = f(th, om);
    const k2x = om + 0.5 * dt * k1v, k2v = f(th + 0.5 * dt * k1x, om + 0.5 * dt * k1v);
    const k3x = om + 0.5 * dt * k2v, k3v = f(th + 0.5 * dt * k2x, om + 0.5 * dt * k2v);
    const k4x = om + dt * k3v, k4v = f(th + dt * k3x, om + dt * k3v);
    th += (dt / 6) * (k1x + 2 * k2x + 2 * k3x + k4x);
    om += (dt / 6) * (k1v + 2 * k2v + 2 * k3v + k4v);
  }
  const s = (A, t) => { if (t <= t0) return A[0]; const fi = Math.min(n - 1 - 1e-9, (t - t0) / dt), i = Math.floor(fi), u = fi - i; return A[i] * (1 - u) + A[i + 1] * u; };
  return { theta: (t) => s(TH, t), omega: (t) => s(OM, t), period: (2 * Math.PI) / w0 };
}

// ------------------------------------------------------------------ angular momentum
// L = I omega conserved while the moment of inertia changes (arms in / out): omega(t) = L / I(t),
// angle(t) = integral of omega (trapezoid on a fine grid, deterministic)
export function spinConserving({ I, omega0, t0, t1, dt = 1 / 960, angle0 = 0 }) {
  const L = I(t0) * omega0;
  const n = Math.ceil((t1 - t0) / dt) + 1;
  const ANG = new Float64Array(n);
  let a = angle0, wPrev = omega0;
  for (let i = 0; i < n; i++) {
    ANG[i] = a;
    const w = L / I(t0 + (i + 1) * dt);
    a += 0.5 * (wPrev + w) * dt; wPrev = w;
  }
  const angle = (t) => { if (t <= t0) return angle0 + omega0 * (t - t0); const fi = Math.min(n - 1 - 1e-9, (t - t0) / dt), i = Math.floor(fi), u = fi - i; return ANG[i] * (1 - u) + ANG[i + 1] * u; };
  return { L, omega: (t) => L / I(Math.max(t0, Math.min(t1, t))), angle };
}

export const speed = (v) => len(v);
export { dot, sub };
