// The demo reel: one segment per animation of the library. Each segment wraps a clip instance and
// adds staging (camera, follow-spot), the phase bar and a data card.
import { CLIPS } from '../../packages/bonemotion/src/clips/index.js';
import { phaseAt } from '../../packages/bonemotion/src/core/principles.js';
import { fmt } from './fmt.js';
import { gait } from '../../packages/bonemotion/src/clips/locomotion.js';
import { mix } from '../../packages/bonemotion/src/core/pose.js';
import { poseToAbs, unwrapSeq, absToPose } from '../../packages/bonemotion/src/neural/features.js';
import { makeMLP, inbetween } from '../../packages/bonemotion/src/neural/inbetween.js';

const W = 1920, FLOOR_Y = 850;
// camera framing a region [xa, xb] (rig units) with the floor at FLOOR_Y
export function camFor(xc, S = 1.45, pitch = 0.16, y0 = FLOOR_Y) { return { x0: W / 2 - S * xc, y0, S, pitch }; }

function actor(char, pose, sec, opts = {}) {
  const { ev } = char.evaluatePose(pose, sec);
  const P = char.profile;
  const feet = ['R', 'L'].map((n) => ev.J[`ankle${n}`]).filter(Boolean);
  const shadows = feet.map((p) => ({ p, r: 34, k: 0.5 }));
  shadows.push({ p: pose.root.p, r: 90, k: 0.35 });
  return { char, pose, ev, sec, opts, shadows, P };
}

export function clipSegment(char, inst, meta) {
  const sec = char.secondary(inst.poseAt, { t0: 0, t1: inst.duration, impulses: inst.impulses || [] });
  const camAt = meta.cam || (() => camFor(0));
  return {
    ...meta, dur: inst.duration, inst,
    frame(lt) {
      const pose = inst.poseAt(lt);
      const s = sec.at(lt);
      const a = actor(char, pose, s, inst.drawOpts ? inst.drawOpts(lt) : {});
      if (inst.shadowsOff && inst.shadowsOff(lt)) a.shadows = [];
      if (inst.shadows) a.shadows.push(...inst.shadows(lt));
      const cam = camAt(lt, pose);
      const ph = inst.phases ? (inst.phases.find((p) => lt >= p.t0 && lt < p.t1) || null) : null;
      const head = a.ev.fr.head ? a.ev.fr.head.t : pose.root.p;
      const fp = [cam.x0 + cam.S * head[0], cam.y0 - cam.S * head[1] * Math.cos(cam.pitch)];
      return {
        cam, actors: [a], spot: pose.root.p, spotR: meta.spotR || 170, phaseSet: meta.phaseSet || 'action', phase: ph,
        data: meta.data ? meta.data(lt, pose, a.ev, inst) : null, note: meta.note, focus: fp,
        over: inst.over ? (ctx, camv, ink) => inst.over(ctx, camv, ink, lt, a.ev) : null,
        under: inst.under ? (ctx, camv) => inst.under(ctx, camv, lt, a.ev) : null,
      };
    },
  };
}

export function buildSegments(chars, tl, extra = {}) {
  const mb = chars.mrbones;
  const segs = [];
  const add = (id, num, title, sub, inst, o = {}) => segs.push({ id, ...clipSegment(o.char || mb, inst, { id, num, title, sub, ...o }) });
  const only = (tl.demo && tl.demo.only) || null;
  const want = (id) => !only || only.includes(id);

  if (want('assemble')) {
    const inst = CLIPS.assemble.build(mb, {});
    add('assemble', '01', 'Armado desde el piso', `${inst.count} piezas vuelan en parábolas reales, de los pies al cráneo`, inst, {
      cam: () => camFor(0, 1.5),
      data: (lt) => lt < inst.tAll ? [{ head: 'ARMADO' }, { m: `piezas en su sitio: ${[...inst.plan.values()].filter((q) => q.tLand <= lt).length} / ${inst.count}` }, { m: 'g = 9,81 m/s^{2} para todas', col: '#B03A2E' }] : null,
    });
  }
  if (want('hattip')) {
    const inst = CLIPS.hatTip.build(mb, {});
    add('hattip', '02', 'Saludo con el sombrero', 'la mano guía al sombrero; la cabeza llega un instante después', inst, { cam: () => camFor(0, 1.75, 0.16, 900) });
  }
  if (want('hatflip')) {
    const inst = CLIPS.hatFlip.build(mb, {});
    add('hatflip', '03', 'Sombrero al aire', 'sale de la mano con la velocidad y el giro justos: una vuelta completa y cae en la cabeza', inst, {
      cam: () => camFor(0, 1.6, 0.16, 880),
      data: () => [{ head: 'VUELO LIBRE DEL SOMBRERO' }, { m: `|v| al soltar = ${fmt(Math.hypot(...inst.Vrel) / 200, 2)} m/s`, col: '#B7791F' }, { m: `giro constante ω = ${fmt(inst.omega, 1)} rad/s` }, { m: `tiempo de vuelo ${fmt(inst.T, 2)} s` }],
    });
    segs[segs.length - 1].inst.over = (ctx, cam, ink, lt) => drawTrail(ctx, cam, inst.trail(lt));
  }
  if (want('walk')) {
    const inst = CLIPS.chaplinWalk.build(mb, { x: -560, steps: 12 });
    add('walk', '04', 'Caminata a lo Chaplin', 'pies hacia fuera, rodillas firmes, cadera que se mece, bastón que gira', inst, {
      phaseSet: 'walk', cam: (lt, pose) => camFor(Math.max(-200, Math.min(200, pose.root.p[0]))),
      data: (lt) => [{ head: 'PARÁMETROS DE LA MARCHA' }, { m: `cadencia ${fmt(inst.gait.cadence, 1)} pasos/s` }, { m: `paso ${fmt(inst.gait.stepLen / 200, 2)} m` }, { m: `v = ${fmt(inst.gait.speed / 200, 2)} m/s`, col: '#B7791F' }],
    });
  }
  if (want('hop')) {
    const inst = CLIPS.cornerHop.build(mb, {});
    add('hop', '05', 'Giro en un pie', 'la cabeza gira primero; tres saltos balísticos sobre el pie izquierdo', inst, {
      phaseSet: 'action', cam: (lt, pose) => camFor(Math.max(-150, Math.min(150, pose.root.p[0])), 1.45),
      data: () => [{ head: 'CADA SALTO' }, { m: 'vuelo 0,22 s,  contacto 0,12 s' }, { m: `altura h = gT^{2}/8 = ${fmt(9.81 * 0.22 ** 2 / 8 * 100, 1)} cm`, col: '#2C6E9B' }],
    });
  }
  if (want('bow')) {
    const inst = CLIPS.doffBow.build(mb, {});
    add('bow', '06', 'Reverencia', 'la cadera va atrás para que el peso siga sobre los pies; la cabeza sube al final', inst, { cam: () => camFor(-20, 1.6, 0.16, 880) });
  }
  if (want('jump')) {
    const inst = CLIPS.jump.build(mb, {});
    add('jump', '07', 'Salto vertical', 'agacharse, impulsarse, volar en parábola exacta, amortiguar', inst, {
      cam: () => camFor(0, 1.4, 0.16, 870),
      data: (lt) => [{ head: 'SALTO' }, { m: `v_{despegue} = ${fmt(inst.vOff / 200, 2)} m/s \\up`, col: '#B7791F' }, { m: `h = v^{2}/2g = ${fmt(inst.h / 200, 2)} m`, col: '#2C6E9B' }, { m: `t_{vuelo} = 2v/g = ${fmt(inst.T, 2)} s` }],
    });
    segs[segs.length - 1].inst.over = (ctx, cam, ink, lt) => drawTrail(ctx, cam, inst.trail(lt));
  }
  const throwSeg = (id, num, title, sub, clipId, extra) => {
    if (!want(id)) return;
    const inst = CLIPS[clipId].build(mb, {});
    add(id, num, title, sub, inst, {
      cam: () => camFor(40, 1.42),
      over: true,
      data: (lt) => extra(inst, lt),
    });
    const sg = segs[segs.length - 1];
    sg.inst.over = (ctx, cam, ink, lt) => drawTrail(ctx, cam, inst.trail(lt));
  };
  throwSeg('drop', '08', 'Soltar desde el reposo', 'la mano se abre con el cráneo en reposo y lo vuelve a atrapar más abajo, cediendo', 'skullDrop', (i, lt) => [
    { head: 'CAÍDA LIBRE' }, { m: 'v_{0} = 0', col: '#B7791F' }, { m: `t = ${fmt(Math.max(0, Math.min(lt, i.tCatch) - i.tRel), 2)} s` },
    { m: `v al atrapar = ${fmt(Math.hypot(...i.Vc) / 200, 2)} m/s \\down`, col: '#B7791F' }]);
  throwSeg('toss', '09', 'Lanzamiento hacia arriba', 'cadena cinética: piernas, cadera, tronco y por último el brazo', 'skullToss', (i, lt) => [
    { head: 'AL SOLTAR' }, { m: `v_{0} = ω r = ${fmt(i.v0 / 200, 1)} m/s \\up`, col: '#B7791F' }, { m: `ω = ${fmt(i.omega, 2)} rad/s,  r = ${fmt(i.r / 200, 2)} m` },
    { m: `h_{máx} = v_{0}^{2}/2g = ${fmt((i.v0 / 200) ** 2 / (2 * 9.81), 2)} m`, col: '#2C6E9B' }]);
  throwSeg('slam', '10', 'Lanzamiento hacia abajo', 'brazo por encima: suelta con el radio horizontal, rebota, lo atrapa en el ápice', 'skullSlam', (i, lt) => [
    { head: 'AL SOLTAR Y AL REBOTAR' }, { m: `v_{0} = ${fmt(i.v0 / 200, 1)} m/s \\down`, col: '#B7791F' }, { m: 'coeficiente de restitución e = 0,55' },
    { m: 'se atrapa en el ápice: v = 0', col: '#2F7D5B' }]);
  if (want('sling')) {
    const inst = CLIPS.sling.build(mb, {});
    add('sling', '11', 'Honda con su propio brazo', 'dos tirones, ¡pop!, péndulo, giro y suelta con el radio horizontal', inst, {
      cam: () => camFor(0, 1.32, 0.14, 880),
      data: (lt) => {
        const w = Math.abs(inst.thetaDot(lt));
        return [{ head: 'LA HONDA' }, { m: `R = ${fmt(inst.R / 200, 3)} m` }, { m: `ω = ${fmt(w, 2)} rad/s` }, { m: `v = ω R = ${fmt(w * inst.R / 200, 2)} m/s`, col: '#B7791F' }];
      },
    });
    segs[segs.length - 1].inst.over = (ctx, cam, ink, lt) => { drawSling(ctx, cam, inst, lt); drawTrail(ctx, cam, inst.trail(lt)); };
  }
  if (want('spin')) {
    const inst = CLIPS.pirouette.build(mb, {});
    add('spin', '12', 'Giro: momento angular', 'brazos adentro: menos inercia, más velocidad; L = I ω se conserva', inst, {
      cam: () => camFor(0, 1.6, 0.16, 880),
      data: (lt) => [{ head: 'L = I ω (CONSTANTE)' }, { m: `I = ${fmt(inst.I(lt), 3)} kg m^{2}`, col: '#2C6E9B' }, { m: `ω = ${fmt(inst.omega(lt), 2)} rad/s`, col: '#B7791F' }, { m: `L = ${fmt(lt > inst.tFree && lt < inst.tStop ? inst.I(lt) * inst.omega(lt) : inst.L, 3)} kg m^{2}/s`, col: '#2F7D5B' }],
      note: 'masa de cada hueso proporcional a su volumen (12 kg en total); sin rozamiento en el pivote',
    });
  }
  if (want('retarget')) {
    // the same clips, two very different bodies: a jump, then a walk (the walk is matched to the jump's
    // stance so the hand-off is seamless)
    const mq = chars.mannequin;
    const seq = (char, x, z) => {
      const yaw = 1.25;
      const j = CLIPS.jump.build(char, { x, z, yaw, height: 0.3 });
      const d = char.profile.dims;
      const g = gait(char.profile, { style: 'neutral', yaw, x, z, steps: 8, width: (d.footRestX * 1.1) / (d.hipW * 1.5), toeOut: 0.3, t0: 0.5 });
      const Tj = j.duration - 0.5;
      const poseAt = (t) => (t < Tj ? j.poseAt(t) : t < Tj + 0.35 ? mix(j.poseAt(t), g.poseAt(t - Tj + g.tStart), (t - Tj) / 0.35) : g.poseAt(t - Tj + g.tStart));
      return { char, poseAt, duration: Tj + (g.tStop - g.tStart), j, g };
    };
    const A = seq(mb, -560, -40), B = seq(mq, -250, 70);
    const dur = Math.max(A.duration, B.duration) + 0.3;
    segs.push({ id: 'retarget', ...multiSegment({ num: '13', title: 'Otro personaje, mismo código', sub: 'las proporciones salen del perfil del personaje: el movimiento se adapta solo', dur,
      cam: () => camFor(-120, 1.2, 0.16, 860),
      data: () => [{ head: 'PROPORCIONES' }, { m: `Mr. Bones: pierna ${fmt(mb.profile.dims.legLen / 200, 2)} m` }, { m: `Pino: pierna ${fmt(mq.profile.dims.legLen / 200, 2)} m` }, { m: `salto h = 0,30 m para ambos`, col: '#2C6E9B' }],
      cards: () => [{ x: 560, y: 330, text: 'Mr. Bones', sub: '171 huesos' }, { x: 1080, y: 400, text: 'Pino', sub: 'maniquí, 16 piezas' }],
    }, [A, B]) });
  }
  if (want('neural') && extra.weights) {
    // a held-out walk (parameters never seen in training): 40 frames are removed and re-invented
    const mlp = makeMLP(extra.weights);
    const g = gait(mb.profile, { style: 'neutral', yaw: 1.3, x: 0, z: 0, steps: 7, cadence: 2.05, stepLen: 0.55, toeOut: 0.18, sway: 5.5, bob: 3.2, t0: 0.5 });
    const FPS = 60;
    const nf = Math.floor((g.tStop + 0.2) * FPS);
    const truth = [];
    for (let i = 0; i < nf; i++) truth.push(Array.from(poseToAbs(mb, g.poseAt(i / FPS))));
    unwrapSeq(truth);
    const N = 40, k0 = Math.round(1.9 * FPS);
    const fill = (method) => inbetween(mlp, truth[k0 - 1], truth[k0], truth[k0 + N], truth[k0 + N + 1], N, method);
    const her = fill('hermite'), net = fill('neural');
    const errOf = (seqv) => { let e = 0, n = 0; for (let j = 0; j < seqv.length; j++) for (const o of [0, 19, 26, 33, 39]) { const a = seqv[j], b = truth[k0 + 1 + j]; e += Math.hypot(a[o] - b[o], a[o + 1] - b[o + 1], a[o + 2] - b[o + 2]); n++; } return e / n / 2; };
    const eH = errOf(her), eN = errOf(net);
    const gapT0 = k0 / FPS, gapT1 = (k0 + N) / FPS;
    // timeline: normal speed through the gap, then a slow-motion replay (x0.25) of the gap
    const T1 = gapT1 + 1.2, SLOW = 0.25, rep0 = gapT0 - 0.15, rep1 = gapT1 + 0.15;
    const dur = T1 + (rep1 - rep0) / SLOW + 0.8;
    const walkT = (lt) => (lt < T1 ? lt : lt < T1 + (rep1 - rep0) / SLOW ? rep0 + (lt - T1) * SLOW : rep1 + (lt - T1 - (rep1 - rep0) / SLOW));
    const inGap = (t) => t > gapT0 && t < gapT1;
    const filled = (arr, t) => { const f = t * FPS - k0 - 1, j = Math.floor(f), u = f - j; const a = arr[Math.max(0, Math.min(arr.length - 1, j))], b = arr[Math.max(0, Math.min(arr.length - 1, j + 1))]; return a.map((x, k) => x + (b[k] - x) * u); };
    const shift = (pose, dx) => { const P = JSON.parse(JSON.stringify(pose)); P.root.p[0] += dx; P.legs.forEach((L) => { L.ankle[0] += dx; }); P.arms.forEach((A) => A.specs.forEach((sp) => { if (sp.space === 'world') sp.p[0] += dx; })); return P; };
    const lane = (dx, arr) => ({ char: mb, poseAt: (lt) => { const t = walkT(lt); const tp = g.poseAt(t); return shift(inGap(t) ? absToPose(filled(arr, t), tp) : tp, dx); } });
    const ghostLane = (dx) => ({ char: mb, ghost: 0.3, show: (lt) => inGap(walkT(lt)), poseAt: (lt) => shift(g.poseAt(walkT(lt)), dx) });
    const L = lane(-760, her), R = lane(-90, net);
    segs.push({ id: 'neural', ...multiSegment({ num: '14', title: 'Transiciones aprendidas', sub: 'se borran 40 fotogramas de una caminata nueva; la red los vuelve a inventar', dur,
      cam: () => camFor(-250, 1.15, 0.16, 850),
      data: (lt) => [{ head: inGap(walkT(lt)) ? 'HUECO: 40 FOTOGRAMAS' : lt > T1 ? 'REPETICIÓN x0,25' : 'CAMINATA NUEVA' }, { m: `error Hermite: ${fmt(eH, 1)} cm`, col: '#B03A2E' }, { m: `error red neuronal: ${fmt(eN, 1)} cm`, col: '#2F7D5B' }, { m: 'gris: el movimiento real', col: '#6E6E6E' }],
      cards: () => [{ x: 560, y: 352, text: 'Interpolación cúbica', sub: 'Hermite: suave, pero no sabe caminar', col: '#B03A2E' }, { x: 1330, y: 352, text: 'Red neuronal', sub: 'aprendida de la propia librería', col: '#2F7D5B' }],
      note: 'red de 2 capas ocultas (256), entrenada con movimientos de la librería; corrige la interpolación cúbica entre los dos fotogramas clave',
    }, [ghostLane(-760), ghostLane(-90), L, R]) });
  }
  return segs;
}

// several actors on one stage; each gets its own secondary motion
function multiSegment(meta, actors) {
  const secs = actors.map((a) => (a.ghost ? null : a.char.secondary(a.poseAt, { t0: 0, t1: meta.dur })));
  return {
    ...meta,
    frame(lt) {
      const list = [];
      actors.forEach((a, k) => {
        if (a.show && !a.show(lt)) return;
        const pose = a.poseAt(lt);
        const s = secs[k] ? secs[k].at(lt) : a.char.ZERO_SEC;
        const act = actor(a.char, pose, s, {});
        if (a.ghost) { act.ghost = a.ghost; act.shadows = []; }
        list.push(act);
      });
      list.sort((p, q) => (p.ghost ? -1 : 0) - (q.ghost ? -1 : 0) || p.pose.root.p[2] - q.pose.root.p[2]);
      const cam = meta.cam(lt);
      return { cam, actors: list, spot: null, phaseSet: null, phase: null, data: meta.data ? meta.data(lt) : null, note: meta.note, cards: meta.cards ? meta.cards(lt) : null, focus: [960, 540] };
    },
  };
}

// the sling circle (dashed), its centre, and the release radius
function drawSling(ctx, cam, inst, lt) {
  if (lt < inst.tS - 0.2 || lt > inst.tCatch + 0.4) return;
  const P = (p) => [cam.x0 + cam.S * p[0], cam.y0 - cam.S * (Math.cos(cam.pitch) * p[1] - Math.sin(cam.pitch) * p[2])];
  const c = P(inst.C), e = P([inst.C[0] + inst.R, inst.C[1], inst.C[2]]);
  const ry = cam.S * inst.R * Math.cos(cam.pitch);
  ctx.save();
  ctx.setLineDash([10, 9]); ctx.strokeStyle = '#2C6E9B'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.ellipse(c[0], c[1], cam.S * inst.R, ry, 0, 0, 2 * Math.PI); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#2C6E9B'; ctx.beginPath(); ctx.arc(c[0], c[1], 6, 0, 2 * Math.PI); ctx.fill();
  ctx.strokeStyle = '#2F7D5B'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(c[0], c[1]); ctx.lineTo(e[0], e[1]); ctx.stroke();
  ctx.restore();
}

// the analytic flight: dashed curve, and a dot every 1/12 s (the spacing chart: slow at the top)
function drawTrail(ctx, cam, tr) {
  if (!tr) return;
  const P = (p) => [cam.x0 + cam.S * p[0], cam.y0 - cam.S * (Math.cos(cam.pitch) * p[1] - Math.sin(cam.pitch) * p[2])];
  ctx.save();
  ctx.setLineDash([9, 8]); ctx.strokeStyle = 'rgba(255,255,255,0.55)'; ctx.lineWidth = 2.5;
  ctx.beginPath(); tr.pts.forEach((p, i) => { const q = P(p); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); }); ctx.stroke();
  ctx.setLineDash([]);
  for (const p of tr.dots) { const q = P(p); ctx.fillStyle = '#ffffff'; ctx.strokeStyle = '#151515'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(q[0], q[1], 5, 0, 2 * Math.PI); ctx.fill(); ctx.stroke(); }
  ctx.restore();
}
void phaseAt;
