#!/usr/bin/env node
// Builds the motion corpus the in-betweener learns from: the library's own clips, run many times with
// randomised parameters (tempo, step length, facing, heights, speeds...), sampled at 60 fps and
// converted to feature vectors. Split by sequence: train / val / test (no window crosses a split).
//
//   node packages/bonemotion/tools/make_dataset.mjs [--n 260] [--out build/bonemotion/dataset]
import fs from 'node:fs';
import path from 'node:path';
import { createMrBones } from '../src/characters/mrbones/index.js';
import { CLIPS } from '../src/clips/index.js';
import { gait, WALK_STYLES } from '../src/clips/locomotion.js';
import { poseToAbs, unwrapSeq, DIM, LAYOUT_VERSION } from '../src/neural/features.js';

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(`--${k}`); return i < 0 ? d : argv[i + 1]; };
const N = Number(opt('n', 260));
const OUT = path.resolve(opt('out', 'build/bonemotion/dataset'));
fs.mkdirSync(OUT, { recursive: true });
const FPS = 60;

function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const R = rng(20261016);
const U = (a, b) => a + (b - a) * R();
const char = createMrBones();

// families and their parameter samplers -> { poseAt, duration }
const FAMILIES = {
  walkNeutral: () => { const g = gait(char.profile, { style: 'neutral', yaw: U(-Math.PI, Math.PI), x: U(-200, 200), z: U(-100, 100), steps: 4 + Math.floor(U(0, 6)), cadence: U(1.6, 2.4), stepLen: U(0.36, 0.62), toeOut: U(0.05, 0.3), sway: U(2, 7), bob: U(1.5, 4), first: R() < 0.5 ? 0 : 1, t0: U(0.4, 0.8) }); return { poseAt: g.poseAt, duration: g.tStop + 0.2 }; },
  walkChaplin: () => { const g = gait(char.profile, { style: 'chaplin', yaw: U(-Math.PI, Math.PI), x: U(-200, 200), z: U(-100, 100), steps: 4 + Math.floor(U(0, 7)), cadence: U(2.2, 3.0), stepLen: U(0.26, 0.42), toeOut: U(0.6, 0.95), kick: U(0.03, 0.12), first: R() < 0.5 ? 0 : 1, t0: U(0.4, 0.8) }); return { poseAt: g.poseAt, duration: g.tStop + 0.2 }; },
  caneWalk: () => CLIPS.chaplinWalk.build(char, { yaw: U(-Math.PI, Math.PI), x: U(-300, 0), steps: 6 + Math.floor(U(0, 6)) }),
  jump: () => CLIPS.jump.build(char, { yaw: U(-Math.PI, Math.PI), height: U(0.12, 0.45) }),
  hatTip: () => CLIPS.hatTip.build(char, { yaw: U(-1.2, 1.2) }),
  hatFlip: () => CLIPS.hatFlip.build(char, { yaw: U(-1.2, 1.2) }),
  bow: () => CLIPS.doffBow.build(char, { yaw: U(-1.2, 1.2) }),
  hop: () => CLIPS.cornerHop.build(char, { yaw: U(0.6, 1.8), x: U(-450, -300) }),
  spin: () => CLIPS.pirouette.build(char, { yaw: U(-1, 1), omega0: U(4, 7) }),
  toss: () => CLIPS.skullToss.build(char, { yaw: U(0.3, 1.4), v0: U(2.5, 4.2) }),
  slam: () => CLIPS.skullSlam.build(char, { yaw: U(0.3, 1.4), v0: U(3.5, 6) }),
  drop: () => CLIPS.skullDrop.build(char, { yaw: U(0.3, 1.4) }),
};
const WEIGHTS = { walkNeutral: 5, walkChaplin: 5, caneWalk: 2, jump: 3, hatTip: 1, hatFlip: 1, bow: 1, hop: 2, spin: 1, toss: 1, slam: 1, drop: 1 };
const names = Object.keys(FAMILIES);
const wsum = names.reduce((a, k) => a + WEIGHTS[k], 0);
const pick = () => { let r = R() * wsum; for (const k of names) { r -= WEIGHTS[k]; if (r <= 0) return k; } return names[0]; };

const seqs = [];
let frames = 0;
const t0 = Date.now();
for (let n = 0; n < N; n++) {
  const fam = n < names.length ? names[n] : pick();
  const inst = FAMILIES[fam]();
  const nf = Math.floor(inst.duration * FPS);
  const F = [];
  for (let i = 0; i < nf; i++) F.push(Array.from(poseToAbs(char, inst.poseAt(i / FPS))));
  unwrapSeq(F);
  // split: every 5th sequence to val, every 7th to test (by index; families stay mixed)
  const split = n % 7 === 3 ? 'test' : n % 5 === 1 ? 'val' : 'train';
  seqs.push({ fam, split, frames: F });
  frames += nf;
  if (n % 20 === 0) process.stdout.write(`\r${n}/${N} sequences, ${frames} frames, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
const buf = new Float32Array(frames * DIM);
const meta = { layout: LAYOUT_VERSION, dim: DIM, fps: FPS, sequences: [] };
let off = 0;
for (const s of seqs) {
  for (const f of s.frames) { buf.set(f, off); off += DIM; }
  meta.sequences.push({ fam: s.fam, split: s.split, frames: s.frames.length });
}
fs.writeFileSync(path.join(OUT, 'frames.f32'), Buffer.from(buf.buffer));
fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify(meta, null, 1));
console.log(`\n${seqs.length} sequences, ${frames} frames -> ${path.relative(process.cwd(), OUT)} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
void WALK_STYLES;
