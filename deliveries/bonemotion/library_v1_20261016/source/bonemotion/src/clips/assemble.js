// Assembly from the floor: every bone lies scattered on the stage; they stir (anticipation), then fly
// one by one — feet, shins, thighs, pelvis, a ripple of vertebrae, ribs, sternum, girdles, arms, hands,
// neck and skull, a swarm of teeth — on true ballistic arcs (one gravity for all), spinning into their
// orientation and snapping into place with a damped recoil (velocity continuous at the snap).
// Then he comes alive: a rattle, a look at his own hand, steps on the brim of his hat (the rake gag),
// the hat flips onto his head and he tips it to the audience.
//
// Works on any character that exposes a rigid-object model (Mr. Bones, the mannequin...): bones are
// ranked by anatomy when their names are known, otherwise bottom-up by height.
import { objectFrames } from '../characters/mrbones/model.js';
import { standPose, SIDE, toWorld } from '../core/body.js';
import { action, springStep } from '../core/principles.js';
import { ease, clamp, track } from '../core/curves.js';
import { launchVelocity, projectile } from '../core/physics.js';
import { add, sub, scl, mv, mm, rx, ry, rz, norm, len, cross, rotAxis, slerpR, I3, fmul, ftr, frot, fapp } from '../core/m3.js';
import { hatTipLayer } from './chaplin.js';
import { HAT_SEAT } from '../characters/mrbones/index.js';
import { pulse } from './kit.js';

const hash = (k, i) => { const x = Math.sin((k + 1) * 12.9898 + i * 78.233) * 43758.5453; return x - Math.floor(x); };

// anatomical build order: [tier, order within the tier]
function rankOf(d, spineIndex) {
  const n = d.name;
  const m = (re) => re.test(n);
  if (m(/calcaneus/)) return [0, 0]; if (m(/talus/)) return [0, 1]; if (m(/navicular|cuboid/)) return [0, 2]; if (m(/cuneiform/)) return [0, 3];
  if (m(/^metatarsal/)) return [0, 4 + 0.4 * parseInt(n.split(' ')[1], 10)];
  if (m(/^toe phalanx/)) { const [k, j] = n.split(' ')[2].split('.').map(Number); return [0, 6 + 0.3 * k + 0.6 * j]; }
  if (m(/tibia|fibula/)) return [1, m(/fibula/) ? 0.5 : 0];
  if (m(/patella/)) return [2, 0];
  if (m(/femur/)) return [3, 0];
  if (m(/os coxae/)) return [4, 0]; if (m(/sacrum/)) return [4, 1]; if (m(/coccyx/)) return [4, 1.5 + 0.3 * parseInt(n.split(' ')[1], 10)];
  if (m(/^vertebra/)) return [5, spineIndex[n.split(' ')[1]]];
  if (m(/^rib /)) return [6, 12 - parseInt(n.split(' ')[1], 10)];
  if (m(/manubrium|sternum body|xiphoid/)) return [7, m(/xiphoid/) ? 2 : m(/sternum/) ? 1 : 0];
  if (m(/clavicle/)) return [8, 0]; if (m(/scapula/)) return [8, 1];
  if (m(/humerus/)) return [9, 0];
  if (m(/ulna/)) return [10, 0]; if (m(/radius/)) return [10, 0.5];
  if (m(/scaphoid|lunate|triquetrum|pisiform|trapezium|trapezoid|capitate|hamate/)) return [11, 0];
  if (m(/^metacarpal/)) return [11, 1.5];
  if (m(/^phalanx/)) { const j = parseInt(n.split(' ')[1].split('.')[1], 10); return [11, 2.5 + j]; }
  if (m(/hyoid/)) return [12, 9];
  if (m(/mandible/)) return [13, 0]; if (m(/maxilla/)) return [13, 1]; if (m(/zygomatic/)) return [13, 2]; if (m(/cranium/)) return [13, 3.5];
  if (m(/tooth/)) return [14, parseInt(n.split(' ')[2], 10) * 0.5 + (m(/lower/) ? 0.25 : 0)];
  return null;
}
const TIER_STAGGER = [0.022, 0.12, 0.1, 0.12, 0.1, 0.045, 0.06, 0.08, 0.1, 0.1, 0.08, 0.03, 0.06, 0.16, 0.025];

export function assemble(char, p = {}) {
  const pr = char.profile, model = char.model;
  const g = pr.g;
  const yaw = p.yaw ?? 0.3, X = p.x ?? 0, Z = p.z ?? 10;
  const o = [X, 0, Z];
  const base = standPose(pr, { x: X, z: Z, yaw, toeOut: 0.5 });
  const evT = char.evaluatePose(base).ev;
  const objsT = objectFrames(model, evT, char.toControls(base));
  const spineIndex = {};
  (model.spineKeys || []).forEach((v, i) => { spineIndex[v.key] = i; });
  const isMrBones = !!model.ribInfo && Object.keys(model.ribInfo).length > 0;

  // ---- plan
  const plan = new Map();
  let entries = [];
  for (const ob of objsT) {
    const d = ob.def;
    if (d.group === 'prop' || d.dyn || d.kind === 'socket' || d.kind === 'decal') continue;
    let rk = isMrBones ? rankOf(d, spineIndex) : null;
    if (!rk) rk = [0, ob.ctr[1] / 10]; // generic: bottom-up by height
    entries.push({ d, ob, rk });
  }
  if (!isMrBones) { // generic: tiers by height bands
    entries.forEach((e) => { e.rk = [Math.min(13, Math.floor(e.ob.ctr[1] / 30)), e.ob.ctr[0] * 0.002 + 0.5]; });
  }
  const T_START = 1.0;
  const tiers = [...new Set(entries.map((e) => e.rk[0]))].sort((a, b) => a - b);
  let cursor = T_START;
  const pileC = toWorld(o, yaw, [0, 0, 80]);
  for (const tier of tiers) {
    const es = entries.filter((e) => e.rk[0] === tier).sort((a, b) => a.rk[1] - b.rk[1] || a.d.side - b.d.side);
    const st = isMrBones ? TIER_STAGGER[tier] : 0.05;
    const subs = [...new Set(es.map((e) => e.rk[1]))].sort((a, b) => a - b);
    for (const e of es) {
      const k = subs.indexOf(e.rk[1]);
      const sideLag = e.d.side > 0 ? 0.35 * st + 0.02 : 0;
      e.tl = cursor + k * st + sideLag;
    }
    const last = Math.max(...es.map((e) => e.tl));
    cursor = cursor + 0.62 * (last - cursor) + (isMrBones && tier === 13 ? 0.25 : 0.12);
  }
  for (const e of entries) {
    const d = e.d, ob = e.ob, k = d.uid;
    // floor rest: long axis laid flat, random yaw, lowest point on the floor
    const parts = d.pieces ? d.pieces.flat() : d.parts || [];
    let axis = null;
    for (const pt of parts) if ((pt.t === 'cap' || pt.t === 'cyl') && !axis) { const v = sub(pt.b, pt.a); if (len(v) > 8) axis = norm(mv(ob.F.R, v)); }
    let Rflat = I3;
    if (axis) {
      const h = Math.hypot(axis[0], axis[2]);
      if (h > 1e-6 && Math.abs(axis[1]) > 1e-6) Rflat = rotAxis(norm(cross(axis, [axis[0] / h, 0, axis[2] / h])), Math.acos(clamp(h, -1, 1)));
      else if (h <= 1e-6) Rflat = rotAxis([1, 0, 0], Math.PI / 2);
    } else Rflat = rotAxis(norm([hash(k, 7) - 0.5, 0, hash(k, 8) - 0.5]), (0.3 + hash(k, 9)) * Math.PI * 0.5);
    const Qf = mm(ry(hash(k, 3) * 2 * Math.PI), Rflat);
    // lowest point of the object in that orientation, relative to its centre
    const Rw = mm(Qf, ob.F.R);
    const toW = (lp) => add(mv(Rw, lp), mv(Qf, sub(ob.F.t, ob.ctr)));
    let minY = 0;
    for (const pt of parts) {
      if (pt.t === 'sph') minY = Math.min(minY, toW(pt.c)[1] - pt.r);
      else if (pt.t === 'cap') minY = Math.min(minY, toW(pt.a)[1] - pt.ra, toW(pt.b)[1] - pt.rb);
      else if (pt.t === 'cyl') minY = Math.min(minY, toW(pt.a)[1] - pt.r, toW(pt.b)[1] - pt.r);
      else if (pt.t === 'ell') { const c = toW(pt.c); const ext = Math.sqrt((Rw[3] * pt.r[0]) ** 2 + (Rw[4] * pt.r[1]) ** 2 + (Rw[5] * pt.r[2]) ** 2); minY = Math.min(minY, c[1] - ext); }
      else if (pt.t === 'poly') for (const q of pt.pts) minY = Math.min(minY, toW(q)[1] - 1.5);
    }
    const a = hash(k, 1) * 2 * Math.PI, r = Math.sqrt(hash(k, 2));
    const low = ob.ctr[1] < 40; // feet bones lie close to where they belong
    const c0 = low ? add(ob.ctr, [(hash(k, 4) - 0.5) * 60, 0, 40 + hash(k, 5) * 40]) : add(pileC, [Math.cos(a) * 200 * r, 0, Math.sin(a) * 75 * r]);
    c0[1] = -minY + 0.3;
    const dy = ob.ctr[1] - c0[1];
    const T = clamp(0.36 + dy / 900, 0.36, 0.72);
    const spinN = axis && len(sub(parts[0].a || [0, 0, 0], parts[0].b || [0, 0, 0])) > 25 ? 1 : hash(k, 6) < 0.5 ? 1 : 0;
    const spinAx = norm([hash(k, 10) - 0.5, 0.2, hash(k, 11) - 0.5]);
    plan.set(d.uid, { d, tl: e.tl, T, c0, Qf, spinN, spinAx, tLand: e.tl + T });
  }
  const anchors = new Map();
  for (const d of model.defs) {
    if (d.kind === 'socket' || d.kind === 'decal') {
      const anc = d.burstWith ? model.defs.find((q) => q.name === d.burstWith) : model.defs.find((q) => q.frame === d.frame && plan.has(q.uid));
      if (anc) anchors.set(d.uid, anc.uid);
    }
  }
  const lands = [...plan.values()].map((q) => q.tLand);
  const tAll = Math.max(...lands);
  const sternumLand = Math.max(...[...plan.values()].filter((q) => /sternum body|manubrium/.test(q.d.name)).map((q) => q.tLand), T_START);
  const tEyes = tAll + 0.15;
  const W_REC = 2 * Math.PI * 13, Z_REC = 0.45, WD_REC = W_REC * Math.sqrt(1 - Z_REC * Z_REC);

  // rigid state of one planned object at time t: { Q, c } (Q relative to its assembled orientation)
  function stateOf(q, ctr1, t) {
    const tau = t - q.tl;
    if (tau < 0) {
      // waiting on the floor: the pile shivers once at the start, each bone rattles just before it leaves
      let Q = q.Qf, c = q.c0.slice();
      const stir = t > 0.3 && t < 0.75 ? Math.sin(Math.PI * (t - 0.3) / 0.45) : 0;
      const pre = tau > -0.24 ? Math.sin(Math.PI * (tau + 0.24) / 0.24) : 0;
      const wob = 0.05 * stir * Math.sin(2 * Math.PI * 9 * t + q.d.uid) + 0.2 * pre * Math.sin(2 * Math.PI * 12 * tau);
      if (wob) Q = mm(rotAxis([0, 1, 0], wob), Q);
      c[1] += 3 * pre * Math.abs(Math.sin(2 * Math.PI * 12 * tau)) + 1.2 * stir * Math.abs(Math.sin(2 * Math.PI * 9 * t + q.d.uid));
      return { Q, c };
    }
    if (tau < q.T) {
      const V = launchVelocity(q.c0, ctr1, q.T, g);
      const c = projectile(q.c0, V, g).at(tau);
      const u = ease.smoother(tau / q.T);
      let Q = slerpR(q.Qf, I3, u);
      if (q.spinN) Q = mm(rotAxis(q.spinAx, 2 * Math.PI * q.spinN * (1 - u)), Q);
      return { Q, c };
    }
    // snapped in: recoil along the arrival velocity (velocity continuous), damped
    const V = launchVelocity(q.c0, ctr1, q.T, g);
    const Vl = add(V, [0, -g * q.T, 0]);
    const ta = tau - q.T;
    const amp = Math.min(4, len(Vl) / WD_REC);
    const off = scl(norm(Vl), amp * Math.exp(-Z_REC * W_REC * ta) * Math.sin(WD_REC * ta));
    return { Q: I3, c: add(ctr1, off) };
  }
  // ---- the hat: upright on the floor, stepped on (rake gag), flips onto the head
  const hatP = toWorld(o, yaw, [-78, 0, 70]);
  // ---- the "alive" timeline
  const tRattle = tEyes + 0.1;
  const tLook = tRattle + 0.7; // hand up to the face
  const tLookEnd = tLook + 1.7;
  const tStomp0 = tLookEnd + 0.35; // weight to the left leg, right foot rises over the brim
  const tStomp = tStomp0 + 0.62; // the foot lands on the brim edge: launch
  const tFly = 0.95;
  const tLand = tStomp + tFly;
  const tip = hatTipLayer(char, tLand + 0.9, {});
  const duration = tip.tEnd + 1.0;
  const brimEdge = add(hatP, mv(ry(yaw), [36, 0, -8])); // on the side toward his right foot
  const rightPlant = base.legs[0];

  function bodyPose(t) {
    const pose = JSON.parse(JSON.stringify(base));
    pose.face = { jaw: 0.08, look: [0, -0.2], pupil: 0 };
    pose.props = { hat: { mode: 'world' }, bowtie: t > sternumLand };
    // eyes light up: a glint that overshoots and settles
    if (t >= tEyes) pose.face.pupil = Math.max(0, Math.min(1.7, 1 + 0.7 * Math.exp(-4 * (t - tEyes)) * Math.cos(10 * (t - tEyes)) - (1 - Math.min(1, (t - tEyes) / 0.12))));
    // the rattle: a shiver through the spine, shoulders up, then still
    if (t >= tRattle) {
      const r = pulse(t - tRattle, 7, 0.22);
      pose.spine[1] += 0.06 * r; pose.neck[1] -= 0.08 * r; pose.shrug = [0.08 * Math.abs(r), 0.08 * Math.abs(r)];
    }
    // looking at his own right hand: the hand comes up (arc), fingers wiggle one after another
    const lk = Math.min(ease.smoother(clamp((t - tLook) / 0.5, 0, 1)), 1 - ease.smoother(clamp((t - (tLookEnd - 0.45)) / 0.45, 0, 1)));
    if (lk > 0) {
      const A = pose.arms[0];
      const hand = toWorld(o, yaw, [-18, 262, 60]);
      const rest = [A.specs[0]];
      pose.arms[0] = { ...A, specs: [...rest.map((s) => ({ ...s, w: 1 - lk })), { space: 'world', p: hand, w: lk }], pole: [-0.9, -0.4, -0.2], pron: 0.25 + 0.5 * lk, flex: -0.2 * lk + 0.1,
        curl: [0, 1, 2, 3].map((f) => 0.25 + lk * (0.35 + 0.35 * Math.sin(2 * Math.PI * 2.4 * (t - tLook) - f * 0.9))) };
      const lag = Math.min(ease.smoother(clamp((t - tLook - 0.12) / 0.5, 0, 1)), 1 - ease.smoother(clamp((t - (tLookEnd - 0.35)) / 0.45, 0, 1)));
      pose.neck = [pose.neck[0] + 0.12 * lag, pose.neck[1] + 0.05 * lag, pose.neck[2] - 0.32 * lag];
      pose.face.look = [-0.5 * lag, 0.1 * lag];
    }
    // the stomp: weight onto the left leg, right foot lifts over the brim and comes down on its edge
    if (t >= tStomp0 - 0.4) {
      const w = ease.smoother(clamp((t - (tStomp0 - 0.4)) / 0.4, 0, 1)) * (1 - ease.smoother(clamp((t - (tStomp + 0.45)) / 0.4, 0, 1)));
      pose.root.p = add(pose.root.p, mv(ry(yaw), [9 * w, -3 * w, 0]));
      pose.root.tilt[1] += -0.05 * w;
      const L = rightPlant;
      const ballLocal = pr.foot.ball;
      const footOn = (pitch) => sub(add(brimEdge, [0, 5, 0]), mv(mm(ry(L.heading), rx(pitch)), ballLocal)); // ball on top of the brim
      if (t < tStomp0) { /* weight shift only */ }
      else if (t < tStomp + 0.4) {
        // lift (prep), cock the toes up (anticipation), stamp (exec), press (follow)
        const up = add(footOn(-0.35), [0, 34, 0]);
        let a;
        if (t < tStomp - 0.12) a = arcLerp(L.ankle, up, ease.smoother(clamp((t - tStomp0) / (tStomp - 0.12 - tStomp0), 0, 1)));
        else if (t < tStomp) { const u = (t - (tStomp - 0.12)) / 0.12; a = add(scl(up, 1 - u * u), scl(footOn(0.12), u * u)); }
        else a = add(footOn(0.12), [0, -1.5 * Math.sin(Math.PI * Math.min(1, (t - tStomp) / 0.12)), 0]);
        const pitch = t < tStomp - 0.12 ? -0.35 * ease.smoother(clamp((t - tStomp0) / 0.3, 0, 1)) : t < tStomp ? -0.35 + 0.47 * ((t - (tStomp - 0.12)) / 0.12) ** 2 : 0.12;
        pose.legs[0] = { ...L, ankle: a, pitch, plantW: 0, toe: 0.1 };
      } else {
        const u = ease.smoother(clamp((t - (tStomp + 0.4)) / 0.4, 0, 1));
        pose.legs[0] = { ...L, ankle: arcLerp(footOn(0.12), L.ankle, u), pitch: 0.12 * (1 - u), plantW: u, toe: 0 };
      }
      // he watches the hat go up, then straightens to receive it
      if (t > tStomp - 0.3) {
        const ww = ease.smoother(clamp((t - (tStomp - 0.3)) / 0.3, 0, 1)) * (1 - ease.smoother(clamp((t - (tLand - 0.35)) / 0.3, 0, 1)));
        const up = clamp((t - tStomp) / 0.5, 0, 1);
        pose.neck[0] += 0.3 * ww * (1 - up) - 0.35 * ww * up; pose.neck[2] -= 0.4 * ww * (1 - up);
        pose.face.look = [-0.4 * (1 - up) * ww, (0.6 * up - 0.3) * ww];
      }
    }
    // catching the hat with the head: a small give on landing
    if (t >= tLand) { const r = pulse(t - tLand, 3.2, 0.5); pose.neck[0] += 0.07 * r; pose.root.p[1] -= 2.5 * Math.max(0, r); }
    return pose;
  }
  function arcLerp(a, b, u) { const m = add(scl(add(a, b), 0.5), [0, 18, 0]); const q = (1 - u); return add(add(scl(a, q * q), scl(m, 2 * u * q)), scl(b, u * u)); }

  // head seat at the landing instant (the target of the hat's flight)
  const seatAt = (t) => {
    const ev = char.evaluatePose(bodyPose(t)).ev;
    return fmul(ev.fr.head, fmul(ftr(HAT_SEAT), frot(rz(-0.1))));
  };
  const seatLand = seatAt(tLand);
  const R_FLOOR = mm(ry(yaw * 0.3), rz(-0.04));
  const hatF0 = { R: R_FLOOR, t: add(hatP, [0, 2, 0]) };
  const Vh = launchVelocity(hatF0.t, seatLand.t, tFly, g);
  const hatFly = projectile(hatF0.t, Vh, g);

  function poseAt(t) {
    let pose = bodyPose(t);
    // the hat
    if (t < tStomp) pose.props.hat = { mode: 'world', F: hatF0, squash: 1 - (t > tStomp - 0.02 ? 0 : 0) };
    else if (t < tLand) {
      const tau = t - tStomp;
      const u = tau / tFly;
      pose.props.hat = { mode: 'world', F: { R: mm(rz(2 * Math.PI * (1 - u)), slerpR(R_FLOOR, seatLand.R, ease.smooth(u))), t: hatFly.at(tau) }, squash: 1 + 0.1 * Math.min(1, len(hatFly.vel(tau)) / 900) * (1 - u) };
    } else pose.props.hat = { mode: 'head', squash: 1 - 0.16 * Math.max(0, pulse(t - tLand, 4, 0.4)) };
    pose = tip.apply(pose, t);
    return pose;
  }

  // per-object override for the renderer: bones not yet in place are moved rigidly
  function mapObjects(t) {
    if (t > tAll + 0.6) return null;
    return (objs) => {
      const out = [];
      const st = new Map();
      for (const ob of objs) {
        const d = ob.def;
        if (d.dyn) { if (t >= sternumLand) out.push(ob); continue; }
        const q = plan.get(d.uid);
        if (!q) {
          const a = anchors.get(d.uid);
          if (a === undefined) { out.push(ob); continue; }
          const ancOb = objs.find((x) => x.def.uid === a);
          const s = st.get(a) || stateOf(plan.get(a), ancOb.ctr, t);
          out.push({ def: d, F: { R: mm(s.Q, ob.F.R), t: add(s.c, mv(s.Q, sub(ob.F.t, ancOb.ctr))) }, ctr: s.c });
          continue;
        }
        const s = stateOf(q, ob.ctr, t);
        st.set(d.uid, s);
        out.push({ def: d, F: { R: mm(s.Q, ob.F.R), t: add(s.c, mv(s.Q, sub(ob.F.t, ob.ctr))) }, ctr: s.c });
      }
      return out;
    };
  }
  // phases for the phase bar: the whole assembly reads as prep -> antic (the stir) -> exec (the build)
  // -> follow (the rattle) -> settle; the rake gag and the tip carry their own envelopes
  const phases = [
    { name: 'prep', t0: 0.0, t1: 0.3 }, { name: 'antic', t0: 0.3, t1: T_START }, { name: 'exec', t0: T_START, t1: tAll },
    { name: 'follow', t0: tAll, t1: tRattle + 0.5 }, { name: 'settle', t0: tRattle + 0.5, t1: tLook },
    { name: 'prep', t0: tStomp0 - 0.4, t1: tStomp - 0.12 }, { name: 'antic', t0: tStomp - 0.12, t1: tStomp - 0.05 }, { name: 'exec', t0: tStomp - 0.05, t1: tLand },
    { name: 'follow', t0: tLand, t1: tLand + 0.25 }, { name: 'settle', t0: tLand + 0.25, t1: tLand + 0.9 },
    ...tip.phases,
  ];
  const events = [...plan.values()].map((q) => ({ t: q.tLand, kind: 'clack', name: q.d.name, small: !!q.d.small })).sort((a, b) => a.t - b.t);
  events.push({ t: tStomp, kind: 'stomp' }, { t: tLand, kind: 'hatland' }, { t: tEyes, kind: 'eyes' });
  const impulses = [{ t: tRattle, ribs: 1.4, jaw: 4 }, { t: tLand, hat: 40 }];
  const shadowsOff = (t) => t < tAll;
  return { duration, poseAt, phases, events, impulses, mapObjects, tAll, tEyes, tLand, tStomp, plan, hatFly, shadowsOff,
    drawOpts: (t) => ({ mapObjects: mapObjects(t) || undefined }), count: plan.size };
}
