#!/usr/bin/env node
// Lays out the demo reel exactly as the renderer does and writes:
//   build/bonemotion-demo/cues.json   segment times + every sound event on the final timeline
//   productions/bonemotion-demo/timeline.json   (project.duration updated)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createMrBones } from '../../../packages/bonemotion/src/characters/mrbones/index.js';
import { createMannequin } from '../../../packages/bonemotion/src/characters/mannequin/index.js';
import { buildSegments } from '../segments.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROD = path.resolve(HERE, '..');
const ROOT = path.resolve(PROD, '..', '..');
const tlPath = path.join(PROD, 'timeline.json');
const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
const weights = JSON.parse(fs.readFileSync(path.join(ROOT, 'packages/bonemotion/src/neural/weights/inbetween_v1.json'), 'utf8'));
const segs = buildSegments({ mrbones: createMrBones({ seed: tl.project.seed }), mannequin: createMannequin({ seed: tl.project.seed }) }, tl, { weights });
let acc = 0;
const out = { segments: [], events: [] };
for (const s of segs) {
  out.segments.push({ id: s.id, num: s.num, title: s.title, t0: +acc.toFixed(6), dur: +s.dur.toFixed(6) });
  const ev = (t, kind, extra = {}) => { if (t >= 0 && t <= s.dur) out.events.push({ t: +(acc + t).toFixed(6), kind, seg: s.id, ...extra }); };
  const inst = s.inst;
  if (inst) {
    for (const e of inst.events || []) ev(e.t, e.kind, e.name ? { name: e.name, small: e.small } : {});
    if (inst.gait) for (const st of inst.gait.strikes) ev(st.ts, 'step');
    if (inst.contacts) for (const c of inst.contacts) ev(c.t0 + 0.05, 'cane');
    if (s.id === 'jump') ev(inst.tOff, 'whoosh');
    if (s.id === 'sling') { for (let t = inst.tS + 0.8; t < inst.tRel; t += (2 * Math.PI) / inst.omega) ev(t, 'swish'); }
    if (s.id === 'spin') { for (let t = inst.tFree; t < inst.tStop; t += 0.25) ev(t, 'spinwhoosh', { w: inst.omega(t) }); }
  }
  if (s.id === 'retarget' || s.id === 'neural') ev(0.6, 'sting');
  acc += s.dur;
}
out.total = +acc.toFixed(6);
out.events.sort((a, b) => a.t - b.t);
fs.mkdirSync(path.join(ROOT, 'build/bonemotion-demo'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'build/bonemotion-demo/cues.json'), JSON.stringify(out, null, 1));
tl.project.duration = out.total;
fs.writeFileSync(tlPath, JSON.stringify(tl, null, 1) + '\n');
console.log(`${segs.length} segments, ${out.total.toFixed(2)} s, ${out.events.length} sound events`);
for (const s of out.segments) console.log(`  ${s.num} ${s.id.padEnd(9)} ${s.t0.toFixed(2).padStart(7)}  ${s.dur.toFixed(2)} s`);
