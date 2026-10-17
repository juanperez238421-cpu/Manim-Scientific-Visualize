// Learned in-betweening: fill the frames between two key moments.
//
//   baseline  a cubic Hermite per channel between the two keys, with tangents from the neighbouring
//             frames (the classic "computer in-between": smooth, but it knows nothing about motion)
//   network   an MLP that has learned, from the library's own motions, what happens in between
//             (steps, anticipations, overshoots); it predicts a correction to the baseline
//   window    the correction is multiplied by 4u(1-u): zero at both keys, so the keys are kept exactly
//
// Input: 4 context frames (two before the gap, two after) in the window's frame of reference
// (translation and facing removed), the gap length and the in-between position u.
import { DIM, toRel, fromRel } from './features.js';

export function hermiteBaseline(Rm1, R0, R1, R2, N, u) {
  const out = new Float64Array(DIM);
  const h00 = 2 * u ** 3 - 3 * u ** 2 + 1, h10 = u ** 3 - 2 * u ** 2 + u, h01 = -2 * u ** 3 + 3 * u ** 2, h11 = u ** 3 - u ** 2;
  for (let k = 0; k < DIM; k++) {
    const m0 = (R0[k] - Rm1[k]) * N, m1 = (R2[k] - R1[k]) * N;
    out[k] = h00 * R0[k] + h10 * m0 + h01 * R1[k] + h11 * m1;
  }
  return out;
}
export const extraFeats = (N, u) => [N / 40, u, Math.sin(Math.PI * u), Math.cos(Math.PI * u), Math.sin(2 * Math.PI * u)];

// a tiny dense network: layers [{W (out x in, row-major), b}], ELU between layers
export function makeMLP(weights) {
  const layers = weights.layers.map((L) => ({ W: Float32Array.from(L.W), b: Float32Array.from(L.b), nin: L.nin, nout: L.nout }));
  const xm = Float32Array.from(weights.in_mean), xs = Float32Array.from(weights.in_std), rs = Float32Array.from(weights.res_std);
  function forward(x) {
    let h = new Float32Array(x.length);
    for (let i = 0; i < x.length; i++) h[i] = (x[i] - xm[i]) / xs[i];
    layers.forEach((L, li) => {
      const o = new Float32Array(L.nout);
      for (let r = 0; r < L.nout; r++) {
        let acc = L.b[r];
        const off = r * L.nin;
        for (let c = 0; c < L.nin; c++) acc += L.W[off + c] * h[c];
        o[r] = li < layers.length - 1 ? (acc > 0 ? acc : Math.exp(acc) - 1) : acc;
      }
      h = o;
    });
    const res = new Float64Array(DIM);
    for (let k = 0; k < DIM; k++) res[k] = h[k] * rs[k];
    return res;
  }
  return { forward, meta: weights.meta || {} };
}

// fill N-1 in-between frames between absolute frames A0 (key, with Am1 before it) and A1 (key, with
// A2 after it). method: 'linear' | 'hermite' | 'neural'
export function inbetween(mlp, Am1, A0, A1, A2, N, method = 'neural') {
  const p0 = [A0[0], A0[1], A0[2]], y0 = A0[3];
  const R = [Am1, A0, A1, A2].map((A) => toRel(A, p0, y0));
  const ctx = [];
  for (const r of R) for (let k = 0; k < DIM; k++) ctx.push(r[k]);
  const out = [];
  for (let j = 1; j < N; j++) {
    const u = j / N;
    let x;
    if (method === 'linear') { x = new Float64Array(DIM); for (let k = 0; k < DIM; k++) x[k] = R[1][k] + (R[2][k] - R[1][k]) * u; }
    else {
      x = hermiteBaseline(R[0], R[1], R[2], R[3], N, u);
      if (method === 'neural') {
        const res = mlp.forward([...ctx, ...extraFeats(N, u)]);
        const w = 4 * u * (1 - u);
        for (let k = 0; k < DIM; k++) x[k] += w * res[k];
      }
    }
    out.push(fromRel(x, p0, y0));
  }
  return out;
}
