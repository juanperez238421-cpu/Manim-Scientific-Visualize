#!/usr/bin/env node
// Motion QA for every clip of the library (and the retargeted clips on the second character).
// Samples each clip at 240 Hz and checks:
//   ik          no hard IK clamps (target beyond reach by > 1 u); soft-IK residual reported
//   ground      no foot point below the floor (balls, heels, toe tips)
//   skate       planted feet do not slide (contact points move < 0.05 u per 1/240 s)
//   continuity  max acceleration of pelvis, head, wrists, ankles; spikes only at declared impacts
//   limits      knee and elbow angles inside anatomical ranges
//   physics     the drawn motion against the closed-form physics (flights, releases, circles, L = I w)
//   phases      the action envelope is complete and ordered (prep -> antic -> exec -> follow -> settle)
//   anticipation measured: the body really moves the "wrong way" before the action
// Writes packages/bonemotion/qa/motion_qa.json and prints a table. Exit code 1 on any FAIL.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createMrBones, CM_LOCAL } from '../src/characters/mrbones/index.js';
import { createMannequin } from '../src/characters/mannequin/index.js';
import { CLIPS } from '../src/clips/index.js';
import { gait } from '../src/clips/locomotion.js';
import { fapp, sub, len, dot, norm } from '../src/core/m3.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, '..', 'qa');
fs.mkdirSync(OUT, { recursive: true });
const HZ = 240, dt = 1 / HZ;
const mb = createMrBones(), mq = createMannequin();
const angle = (a, b, c) => Math.acos(Math.max(-1, Math.min(1, dot(norm(sub(a, b)), norm(sub(c, b))))));

function sample(char, inst) {
  const n = Math.floor(inst.duration * HZ);
  const S = [];
  for (let i = 0; i <= n; i++) {
    const t = i * dt;
    const pose = inst.poseAt(t);
    const { ev } = char.evaluatePose(pose);
    S.push({ t, pose, ev });
  }
  return S;
}

function generic(char, inst, S, impactTimes) {
  const r = {};
  // IK
  let hard = 0, softMax = 0;
  for (const s of S) for (const f of s.ev.flags.ik) { if (f.over > 1 || f.under > 1) hard++; softMax = Math.max(softMax, f.err || 0); }
  r.ik = { hardClamps: hard, softResidualMax_u: +softMax.toFixed(2), pass: hard === 0 };
  // ground + skate
  let minY = Infinity, skate = 0;
  const pts = (ev) => ['R', 'L'].flatMap((n) => [ev.J[`ball${n}`], ev.J[`heel${n}`], ...(ev.J[`toeTip0${n}`] ? [ev.J[`toeTip0${n}`]] : [])]).filter(Boolean);
  for (let i = 0; i < S.length; i++) {
    for (const p of pts(S[i].ev)) minY = Math.min(minY, p[1]);
    // planted = on the floor (< 0.02 u) for three consecutive samples; touch-down and lift-off are not slides
    if (i && i < S.length - 1) for (const n of ['R', 'L']) for (const k of ['ball', 'heel']) {
      const a = S[i - 1].ev.J[`${k}${n}`], b = S[i].ev.J[`${k}${n}`], c = S[i + 1].ev.J[`${k}${n}`];
      if (a && b && c && a[1] < 0.02 && b[1] < 0.02 && c[1] < 0.02) skate = Math.max(skate, Math.hypot(a[0] - b[0], a[2] - b[2]));
    }
  }
  r.ground = { minFootY_u: +minY.toFixed(3), pass: minY > -0.5 };
  r.skate = { maxSlidePerSample_u: +skate.toExponential(2), pass: skate < 0.05 };
  // continuity: acceleration of key points, excluding windows around declared impacts
  const keyPts = (ev) => ({ pelvis: ev.fr.pelvis.t, head: ev.fr.head.t, wristR: ev.J.wristR, wristL: ev.J.wristL, ankleR: ev.J.ankleR, ankleL: ev.J.ankleL });
  const near = (t) => impactTimes.some((ti) => Math.abs(t - ti) < 0.06);
  const acc = {};
  for (let i = 1; i < S.length - 1; i++) {
    if (near(S[i].t)) continue;
    const a = keyPts(S[i - 1].ev), b = keyPts(S[i].ev), c = keyPts(S[i + 1].ev);
    for (const k of Object.keys(b)) {
      if (!a[k] || !b[k] || !c[k]) continue;
      const m = len([0, 1, 2].map((d) => (a[k][d] - 2 * b[k][d] + c[k][d]) / (dt * dt))) / 200 / 9.81; // in g
      if (!acc[k] || m > acc[k].g) acc[k] = { g: +m.toFixed(2), t: +S[i].t.toFixed(3) };
    }
  }
  const worst = Math.max(...Object.values(acc).map((x) => x.g));
  r.continuity = { maxAccel_g: acc, worst_g: worst, pass: worst < 60 };
  // joint limits
  let kneeMin = 9, kneeMax = 0, elbowMin = 9, elbowMax = 0;
  for (const s of S) {
    const J = s.ev.J;
    for (const n of ['R', 'L']) {
      if (J[`hip${n}`]) { const k = Math.PI - angle(J[`hip${n}`], J[`knee${n}`], J[`ankle${n}`]); kneeMin = Math.min(kneeMin, k); kneeMax = Math.max(kneeMax, k); }
      if (J[`shoulder${n}`] && J[`elbow${n}`] && !J[`detached${n}`]) { const e = Math.PI - angle(J[`shoulder${n}`], J[`elbow${n}`], J[`wrist${n}`]); elbowMin = Math.min(elbowMin, e); elbowMax = Math.max(elbowMax, e); }
    }
  }
  const lim = char.profile.limits;
  r.limits = { knee_rad: [+kneeMin.toFixed(3), +kneeMax.toFixed(3)], elbow_rad: [+elbowMin.toFixed(3), +elbowMax.toFixed(3)], pass: kneeMax <= lim.knee[1] && kneeMin >= -0.02 && elbowMax <= lim.elbow[1] };
  // phases
  const ph = inst.phases || [];
  const names = ph.map((p) => p.name);
  const ordered = ph.every((p, i) => p.t1 >= p.t0 && (i === 0 || p.t0 >= ph[i - 1].t0 - 1e-6));
  const complete = ['antic', 'exec'].every((n) => names.includes(n)) || names.includes('contact');
  r.phases = { count: ph.length, names: [...new Set(names)], ordered, complete, pass: ordered && complete };
  return r;
}

const skullCMof = (s) => fapp(s.ev.fr.head, CM_LOCAL);
const results = {};
const add = (id, char, inst, extra = () => ({}), impacts = []) => {
  const t0 = Date.now();
  const S = sample(char, inst);
  const ev = (inst.events || []).map((e) => e.t);
  const r = generic(char, inst, S, [...ev, ...impacts]);
  Object.assign(r, extra(S, inst));
  r.seconds = +((Date.now() - t0) / 1000).toFixed(1);
  r.pass = Object.values(r).every((x) => typeof x !== 'object' || x.pass !== false);
  results[id] = r;
  const flag = (k) => (r[k] && r[k].pass === false ? 'FAIL' : 'ok');
  console.log(`${id.padEnd(22)} ik ${flag('ik')}  ground ${flag('ground')}  skate ${flag('skate')}  cont ${flag('continuity')} (${r.continuity.worst_g} g)  limits ${flag('limits')}  phases ${flag('phases')}${r.physics ? `  physics ${r.physics.pass ? 'ok' : 'FAIL'}` : ''}${r.anticipation ? `  antic ${r.anticipation.pass ? 'ok' : 'FAIL'}` : ''}  -> ${r.pass ? 'PASS' : 'FAIL'}`);
};
const at = (S, t) => S[Math.max(0, Math.min(S.length - 1, Math.round(t * HZ)))];

// ---------------------------------------------------------------- Mr. Bones
add('assemble', mb, CLIPS.assemble.build(mb, {}), (S, i) => {
  // every bone in flight follows the projectile it was given (sampled on a few bones)
  let worst = 0, n = 0;
  for (const q of [...i.plan.values()].filter((_, k) => k % 9 === 0)) {
    for (let tau = 0.02; tau < q.T - 0.02; tau += 0.05) {
      const t = q.tl + tau;
      const objs = i.mapObjects(t)(require0(S, t, i));
      const ob = objs.find((o) => o.def.uid === q.d.uid);
      const V = [(ob.ctr[0] - q.c0[0]), 0, 0]; void V;
      n++;
      // ballistic check: second difference of the centre = -g
      const o2 = i.mapObjects(t + 1e-3)(require0(S, t + 1e-3, i)).find((o) => o.def.uid === q.d.uid);
      const o0 = i.mapObjects(t - 1e-3)(require0(S, t - 1e-3, i)).find((o) => o.def.uid === q.d.uid);
      const ay = (o2.ctr[1] - 2 * ob.ctr[1] + o0.ctr[1]) / 1e-6;
      worst = Math.max(worst, Math.abs(ay + mb.profile.g) / mb.profile.g);
    }
  }
  return { physics: { bonesChecked: n, gravityRelErrMax: +worst.toExponential(2), pass: worst < 1e-3 } };
}, []);
function require0(S, t, i) { const pose = i.poseAt(t); const { ev, c } = mb.evaluatePose(pose); return objectFramesCached(ev, c); }
import { objectFrames } from '../src/characters/mrbones/model.js';
function objectFramesCached(ev, c) { return objectFrames(mb.model, ev, c); }

add('hatTip', mb, CLIPS.hatTip.build(mb, {}));
add('hatFlip', mb, CLIPS.hatFlip.build(mb, {}), (S, i) => {
  let worst = 0;
  for (let t = i.tRel + 0.02; t < i.tLand - 0.02; t += 0.02) {
    const H = i.poseAt(t).props.hat.F.t;
    const tau = t - i.tRel;
    const P0 = i.poseAt(i.tRel + 1e-6).props.hat.F.t;
    const exp = [P0[0] + i.Vrel[0] * tau, P0[1] + i.Vrel[1] * tau - 0.5 * mb.profile.g * tau * tau, P0[2] + i.Vrel[2] * tau];
    worst = Math.max(worst, len(sub(H, exp)));
  }
  return { physics: { hatFlightErr_u: +worst.toExponential(2), pass: worst < 0.05 } };
});
add('chaplinWalk', mb, CLIPS.chaplinWalk.build(mb, {}));
add('cornerHop', mb, CLIPS.cornerHop.build(mb, {}), (S, i) => {
  let worst = 0;
  for (const h of i.hops) for (let t = h.tOff + 0.01; t < h.tLand - 0.01; t += 0.01) {
    const y = (k) => i.poseAt(k).root.p[1];
    const ay = (y(t + 1e-3) - 2 * y(t) + y(t - 1e-3)) / 1e-6;
    worst = Math.max(worst, Math.abs(ay + mb.profile.g) / mb.profile.g);
  }
  return { physics: { hopGravityRelErr: +worst.toExponential(2), pass: worst < 1e-3 } };
});
add('doffBow', mb, CLIPS.doffBow.build(mb, {}));
add('jump', mb, CLIPS.jump.build(mb, {}), (S, i) => {
  let worst = 0;
  for (let t = i.tOff + 0.005; t < i.tLand; t += 0.01) { const tau = t - i.tOff; worst = Math.max(worst, Math.abs(i.poseAt(t).root.p[1] - (i.yOff + i.vOff * tau - 0.5 * mb.profile.g * tau * tau))); }
  const vTake = (i.poseAt(i.tOff).root.p[1] - i.poseAt(i.tOff - 1e-4).root.p[1]) / 1e-4;
  const yMin = Math.min(...S.filter((s) => s.t < i.tOff).map((s) => s.pose.root.p[1]));
  const y0 = S[0].pose.root.p[1];
  return { physics: { flightErr_u: +worst.toExponential(2), takeoffVel_ms: +(vTake / 200).toFixed(4), expected_ms: +(i.vOff / 200).toFixed(4), pass: worst < 1e-6 && Math.abs(vTake - i.vOff) < 1 },
    anticipation: { crouch_u: +(y0 - yMin).toFixed(1), pass: y0 - yMin > 20 } };
});
for (const [id, clip] of [['skullDrop', CLIPS.skullDrop], ['skullToss', CLIPS.skullToss], ['skullSlam', CLIPS.skullSlam]]) {
  const inst = clip.build(mb, {});
  add(id, mb, inst, (S, i) => {
    const cm = (t) => i.poseAt(t).props.skull.cm;
    const vL = sub(cm(i.tRel), cm(i.tRel - 1e-5)).map((x) => x / 1e-5), vR = sub(cm(i.tRel + 1e-5), cm(i.tRel)).map((x) => x / 1e-5);
    let worst = 0;
    for (let t = i.tRel + 0.004; t < i.tCatch - 0.004; t += 0.004) {
      const tau = t - i.tRel;
      const exp = i.flight ? i.flight.at(tau) : i.proj.at(tau);
      worst = Math.max(worst, len(sub(cm(t), exp)));
    }
    // anticipation: the skull (or the hand) moves against the release direction before the throw
    const dir = Math.sign(i.V0[1]) || 1;
    let back = 0;
    for (const s of S) if (s.t > i.env.start && s.t < i.tRel) back = Math.max(back, -dir * (cm(s.t)[1] - cm(i.env.start)[1]));
    return {
      physics: { releaseVel_left_ms: vL.map((x) => +(x / 200).toFixed(4)), releaseVel_right_ms: vR.map((x) => +(x / 200).toFixed(4)), expected_ms: i.V0.map((x) => +(x / 200).toFixed(4)),
        flightErrMax_u: +worst.toExponential(2), pass: len(sub(vR, i.V0)) < 2 && len(sub(vL, i.V0)) < 2 && worst < 1e-6 },
      anticipation: id === 'skullDrop' ? { note: 'v0 = 0: no throw, no counter-move', pass: true } : { counterMove_u: +back.toFixed(1), pass: back > 10 },
    };
  });
}
add('sling', mb, CLIPS.sling.build(mb, {}), (S, i) => {
  const cm = (t) => i.poseAt(t).props.skull.cm;
  let rad = 0;
  for (let t = i.tS + 0.85; t < i.tRel; t += 0.01) rad = Math.max(rad, Math.abs(len(sub(cm(t), i.C)) - i.R));
  const vR = sub(cm(i.tRel + 1e-5), cm(i.tRel)).map((x) => x / 1e-5), vL = sub(cm(i.tRel), cm(i.tRel - 1e-5)).map((x) => x / 1e-5);
  let fl = 0;
  for (let t = i.tRel + 0.004; t < i.tCatch - 0.004; t += 0.004) { const tau = t - i.tRel; fl = Math.max(fl, len(sub(cm(t), [i.P_REL[0], i.P_REL[1] + i.v0 * tau - 0.5 * mb.profile.g * tau * tau, i.P_REL[2]]))); }
  return { physics: { circleRadiusErr_u: +rad.toExponential(2), releaseVel_ms: vR.map((x) => +(x / 200).toFixed(4)), beforeRelease_ms: vL.map((x) => +(x / 200).toFixed(4)), expected_ms: [0, +(i.v0 / 200).toFixed(4), 0], flightErr_u: +fl.toExponential(2),
    pass: rad < 1e-6 && Math.abs(vR[1] - i.v0) < 2 && Math.abs(vL[1] - i.v0) < 2 && fl < 1e-6 } };
});
add('pirouette', mb, CLIPS.pirouette.build(mb, {}), (S, i) => {
  let worst = 0;
  for (let t = i.tFree + 0.02; t < i.tStop - 0.02; t += 0.01) worst = Math.max(worst, Math.abs(i.I(t) * i.omega(t) - i.L) / i.L);
  // the drawn rotation rate (from the yaw of the pelvis) agrees with L / I
  let rate = 0;
  for (let t = i.tFree + 0.05; t < i.tStop - 0.05; t += 0.05) { const y = (k) => i.poseAt(k).root.yaw; const w = (y(t + 1e-4) - y(t - 1e-4)) / 2e-4; rate = Math.max(rate, Math.abs(w - i.omega(t)) / i.omega(t)); }
  return { physics: { L: +i.L.toFixed(4), L_relErrMax: +worst.toExponential(2), drawnOmegaRelErr: +rate.toExponential(2), I_open: +i.Igrid[20].toFixed(4), I_closed: +i.Igrid[0].toFixed(4), turns: i.turns, pass: worst < 1e-9 && rate < 2e-3 } };
});

// ---------------------------------------------------------------- retargeting: the same clips on Pino
add('retarget/jump@Pino', mq, CLIPS.jump.build(mq, {}));
const gq = gait(mq.profile, { style: 'neutral', yaw: 1.3, x: -300, steps: 8 });
add('retarget/walk@Pino', mq, { duration: gq.tStop, poseAt: gq.poseAt, phases: gq.phases, events: [] });
const gq2 = gait(mq.profile, { style: 'chaplin', yaw: 1.3, x: -300, steps: 8 });
add('retarget/chaplin@Pino', mq, { duration: gq2.tStop, poseAt: gq2.poseAt, phases: gq2.phases, events: [] });

const all = Object.values(results).every((r) => r.pass);
fs.writeFileSync(path.join(OUT, 'motion_qa.json'), JSON.stringify({ sampledAt_Hz: HZ, clips: results, pass: all }, null, 1));
console.log(`\nOVERALL: ${all ? 'PASS' : 'FAIL'}  -> packages/bonemotion/qa/motion_qa.json`);
process.exit(all ? 0 : 1);
