#!/usr/bin/env node
// Neural QA, on the JS side (the code path the renderer uses):
//   1. parity    the JS forward pass reproduces the trainer's evaluation numbers on the held-out test
//                split (same windows definition, independent sampling) within tolerance
//   2. keys      in-betweens keep both key frames exactly (the 4u(1-u) window)
//   3. benefit   on held-out data the network beats the cubic baseline for long gaps (N >= 20)
// Writes packages/bonemotion/qa/neural_qa.json. Exit code 1 on any FAIL.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DIM, POS_BLOCKS } from '../src/neural/features.js';
import { makeMLP, inbetween } from '../src/neural/inbetween.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..');
const DATA = path.join(ROOT, 'build/bonemotion/dataset');
const meta = JSON.parse(fs.readFileSync(path.join(DATA, 'meta.json'), 'utf8'));
const raw = fs.readFileSync(path.join(DATA, 'frames.f32'));
const F = new Float32Array(raw.buffer, raw.byteOffset, raw.byteLength / 4);
const W = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'src/neural/weights/inbetween_v1.json'), 'utf8'));
const report = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'qa/neural_report.json'), 'utf8'));
const mlp = makeMLP(W);
const frame = (i) => Float64Array.from(F.subarray(i * DIM, (i + 1) * DIM));
let off = 0;
const seqs = meta.sequences.map((s) => { const r = { ...s, start: off }; off += s.frames; return r; }).filter((s) => s.split === 'test' && s.frames > 45);
let seed = 4242;
const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
const posErr = (P, Y) => { let e = 0; for (const o of POS_BLOCKS) e += Math.hypot(P[o] - Y[o], P[o + 1] - Y[o + 1], P[o + 2] - Y[o + 2]); return e / POS_BLOCKS.length / 2; };

const out = { windowsPerGap: 400, gaps: {} };
let keysOK = true;
for (const N of [10, 20, 30, 40]) {
  const acc = { linear: 0, hermite: 0, neural: 0 };
  let n = 0;
  for (let w = 0; w < out.windowsPerGap; w++) {
    const s = seqs[Math.floor(rnd() * seqs.length)];
    if (s.frames < N + 4) continue;
    const s0 = s.start + 1 + Math.floor(rnd() * (s.frames - N - 3));
    const ctx = [frame(s0 - 1), frame(s0), frame(s0 + N), frame(s0 + N + 1)];
    const res = {};
    for (const m of ['linear', 'hermite', 'neural']) res[m] = inbetween(mlp, ...ctx, N, m);
    for (let j = 1; j < N; j++) {
      const Y = frame(s0 + j);
      for (const m of ['linear', 'hermite', 'neural']) acc[m] += posErr(res[m][j - 1], Y);
      n++;
    }
    // the keys: the first in-between must sit next to key A (no jump), the last next to key B
    const a = res.neural[0], b = res.neural[N - 2];
    if (posErr(a, ctx[1]) > 3 * (posErr(frame(s0 + 1), ctx[1]) + 0.5) || posErr(b, ctx[2]) > 3 * (posErr(frame(s0 + N - 1), ctx[2]) + 0.5)) keysOK = false;
  }
  const r = { linear: acc.linear / n, hermite: acc.hermite / n, neural: acc.neural / n };
  const py = report.test[`N${N}`];
  r.python = { linear: py.linear.pos_cm, hermite: py.hermite.pos_cm, neural: py.neural.pos_cm };
  // parity: independent samples of the same distribution -> agree within 25 % (sampling noise)
  r.parity = ['linear', 'hermite', 'neural'].every((m) => Math.abs(r[m] - r.python[m]) / r.python[m] < 0.25);
  out.gaps[`N${N}`] = r;
  console.log(`N=${N}: JS  linear ${r.linear.toFixed(2)}  hermite ${r.hermite.toFixed(2)}  neural ${r.neural.toFixed(2)} cm  |  Python ${r.python.linear.toFixed(2)} / ${r.python.hermite.toFixed(2)} / ${r.python.neural.toFixed(2)}  parity ${r.parity ? 'ok' : 'FAIL'}`);
}
// exact parity of the forward pass on fixed vectors (numpy vs JS, float32 weights in JS)
const PV = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'qa/parity_vectors.json'), 'utf8'));
let maxDiff = 0, maxMag = 0;
for (const v of PV) { const y = mlp.forward(v.x); for (let k = 0; k < y.length; k++) { maxDiff = Math.max(maxDiff, Math.abs(y[k] - v.y[k])); maxMag = Math.max(maxMag, Math.abs(v.y[k])); } }
out.forwardParity = { vectors: PV.length, maxAbsDiff: maxDiff, maxAbsOutput: maxMag, relative: maxDiff / maxMag };
console.log(`forward parity: max |JS - numpy| = ${maxDiff.toExponential(2)} (relative ${(maxDiff / maxMag).toExponential(2)})`);
out.checks = {
  forward: maxDiff / maxMag < 1e-4,
  parity: Object.values(out.gaps).every((g) => g.parity),
  keys: keysOK,
  benefit: ['N20', 'N30', 'N40'].every((k) => out.gaps[k].neural < out.gaps[k].hermite),
};
out.pass = Object.values(out.checks).every(Boolean);
fs.writeFileSync(path.join(HERE, '..', 'qa/neural_qa.json'), JSON.stringify(out, null, 1));
console.log(`checks ${JSON.stringify(out.checks)} -> ${out.pass ? 'PASS' : 'FAIL'}`);
process.exit(out.pass ? 0 : 1);
