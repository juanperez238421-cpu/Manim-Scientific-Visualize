// "Pino", a wooden artist's mannequin: the second character, built to prove that the clips retarget.
// Very different proportions from Mr. Bones (short legs, long torso, big round head, 1.33 m tall),
// a much simpler rig (16 rigid segments with ball joints), same pose schema and the same ink renderer.
import { makeBoneRenderer } from '../mrbones/render.js';
import { mm, mv, rx, ry, rz, add, sub, scl, norm, cross, fmul, ftr, frot, fapp, frameAlong, twoBone, col, I3 } from '../../core/m3.js';

const K = 200;
const D = { hipW: 20, thigh: 50, shin: 46, ankleH: 11, ballZ: 22, heelZ: -9, upper: 52, fore: 50, lumbar: 34, thor: 52, neck: 14, headR: 30, shX: 40, shY: 46 };

function buildModel() {
  const defs = [];
  const def = (d) => { const o = { bias: 0, tone: 'bone', bone: true, small: false, decals: [], side: 0, group: 'body', ...d }; o.uid = defs.length; defs.push(o); return o; };
  const Sp = (c, r) => ({ t: 'sph', c, r });
  const Cp = (a, b, ra, rb = ra) => ({ t: 'cap', a, b, ra, rb });
  const El = (c, r) => ({ t: 'ell', c, r });
  def({ name: 'pelvis block', frame: 'pelvis', parts: [El([0, 2, 0], [27, 13, 15])] });
  def({ name: 'waist ball', frame: 'lumbar', parts: [Sp([0, 2, 0], 10)], bias: 1 });
  def({ name: 'abdomen', frame: 'lumbar', parts: [Cp([0, 8, 0], [0, 30, 0], 15, 19)] });
  def({ name: 'chest block', frame: 'thorax', parts: [El([0, 26, 0], [33, 30, 19]), Cp([-30, 44, 0], [30, 44, 0], 9)] });
  def({ name: 'neck', frame: 'neckF', parts: [Cp([0, 0, 0], [0, 14, 0], 7, 6.5)] });
  def({ name: 'head', frame: 'head', parts: [El([0, 30, 0], [29, 31, 29])] });
  for (const s of [-1, 1]) {
    const n = s < 0 ? 'R' : 'L';
    def({ name: `upper arm ${n}`, frame: `hum${n}`, side: s, parts: [Sp([0, 0, 0], 9), Cp([0, -4, 0], [0, -48, 0], 7.5, 6)] });
    def({ name: `forearm ${n}`, frame: `fore${n}`, side: s, parts: [Sp([0, 0, 0], 6.8), Cp([0, -4, 0], [0, -46, 0], 6, 4.6)] });
    def({ name: `hand ${n}`, frame: `hand${n}`, side: s, small: true, parts: [Sp([0, -2, 0], 5), El([0, -13, 0], [7.5, 10, 3.6]), Cp([s * 6, -6, 2], [s * 10, -14, 4], 2.4)] });
    def({ name: `thigh ${n}`, frame: `fem${n}`, side: s, parts: [Sp([0, 0, 0], 11), Cp([0, -4, 0], [0, -46, 0], 10, 7.5)] });
    def({ name: `shin ${n}`, frame: `tib${n}`, side: s, parts: [Sp([0, 0, 0], 8), Cp([0, -4, 0], [0, -43, 0], 7.4, 5.4)] });
    def({ name: `foot ${n}`, frame: `foot${n}`, side: s, parts: [Sp([0, -1, 0], 6), Cp([0, -6, -5], [0, -8, 18], 6, 5.5)] });
  }
  for (const s of [-1, 1]) {
    const n = norm([s * 0.3, 0.05, 1]);
    def({ name: `eye ${s < 0 ? 'R' : 'L'}`, frame: 'head', kind: 'socket', bone: false, side: s, bias: 9, parts: [],
      socket: { c: [s * 10, 34, 27.5], n, u: norm(cross([0, 1, 0], n)), r: [4.6, 6.2] } });
  }
  return { defs, ribInfo: {}, spineKeys: [], bones: defs.length };
}

export function createMannequin({ seed = 7 } = {}) {
  const model = buildModel();
  const legLen = D.thigh + D.shin;
  const dims = {
    K, hipW: D.hipW, thigh: D.thigh, shin: D.shin, legLen, ankleH: D.ankleH, ballZ: D.ballZ, heelZ: D.heelZ,
    upper: D.upper, fore: D.fore, armLen: D.upper + D.fore, hand: 20,
    standH: 101, chest: [0, 74, 16], shoulder: [D.shX, 44 + D.shY, 0], neck: [0, 140, 0], headTop: 216, shoulderW: 2 * D.shX, footRestX: 16,
  };
  const foot = { ball: [0, -D.ankleH, D.ballZ], heel: [0, -D.ankleH, D.heelZ] };
  const profile = { id: 'mannequin', name: 'Pino', K, dims, g: 9.81 * K, foot, skullCM: null, hatSeat: null, canGrip: false, detachable: {},
    limits: { knee: [0, 2.6], elbow: [0, 2.7], spineFlex: [-0.6, 1.2], neck: [-0.9, 0.9] } };

  function evaluatePose(pose) {
    const fr = { world: { R: I3, t: [0, 0, 0] } }, J = {};
    const flags = { ik: [] };
    const tl = pose.root.tilt || [0, 0];
    fr.pelvis = { R: mm(ry(pose.root.yaw || 0), mm(rx(tl[0]), rz(tl[1]))), t: pose.root.p };
    const sp = pose.spine || [0, 0, 0];
    const rot = (v, k) => frot(mm(ry(v[2] * k), mm(rx(v[0] * k), rz(-v[1] * k))));
    fr.lumbar = fmul(fmul(fr.pelvis, ftr([0, 10, 0])), rot(sp, 0.4));
    fr.thorax = fmul(fmul(fr.lumbar, ftr([0, D.lumbar, 0])), rot(sp, 0.6));
    fr.chest = fmul(fr.thorax, ftr([0, 30, 16]));
    fr.neckF = fmul(fmul(fr.thorax, ftr([0, D.thor + 4, 0])), rot(pose.neck || [0, 0, 0], 1));
    fr.head = fmul(fmul(fr.neckF, ftr([0, D.neck, 0])), rot(pose.head || [0, 0, 0], 1));
    const resolve = (specs) => {
      let p = [0, 0, 0], w = 0;
      for (const s of specs) {
        const q = s.space === 'world' ? s.p : fapp(fr[s.space === 'chest' ? 'chest' : s.space === 'pelvis' ? 'pelvis' : 'head'], s.p);
        p = add(p, scl(q, s.w ?? 1)); w += s.w ?? 1;
      }
      return scl(p, 1 / w);
    };
    [-1, 1].forEach((s, i) => {
      const n = s < 0 ? 'R' : 'L';
      // legs
      const L = pose.legs[i];
      const hip = fapp(fr.pelvis, [s * D.hipW, 0, 0]);
      const fwd = mv(ry(L.heading || 0), [0, 0, 1]);
      const pole = L.pole || norm(add(fwd, [s * (L.kneeOut ?? 0.2) * Math.cos(pose.root.yaw || 0), 0, 0]));
      const ik = twoBone(hip, L.ankle, D.thigh, D.shin, pole, 0.992);
      flags.ik.push({ limb: `leg ${n}`, reach: ik.reach, over: ik.over, under: ik.under, err: ik.err });
      fr[`fem${n}`] = frameAlong(hip, sub(ik.mid, hip), pole);
      fr[`tib${n}`] = frameAlong(ik.mid, sub(ik.end, ik.mid), col(fr[`fem${n}`].R, 2));
      fr[`foot${n}`] = { R: mm(ry(L.heading || 0), rx(L.pitch || 0)), t: ik.end };
      J[`hip${n}`] = hip; J[`knee${n}`] = ik.mid; J[`ankle${n}`] = ik.end;
      J[`ball${n}`] = fapp(fr[`foot${n}`], foot.ball); J[`heel${n}`] = fapp(fr[`foot${n}`], foot.heel);
      // arms
      const A = pose.arms[i];
      const S = fapp(fr.thorax, [s * D.shX, D.shY, 0]);
      J[`shoulder${n}`] = S;
      const W = resolve(A.specs);
      const apole = A.pole ? norm(mv(fr.chest.R, A.pole)) : norm(mv(fr.chest.R, [s * 0.55, -0.15, -1]));
      const ai = twoBone(S, W, D.upper, D.fore, apole, 0.97);
      flags.ik.push({ limb: `arm ${n}`, reach: ai.reach, over: ai.over, under: ai.under, err: ai.err });
      fr[`hum${n}`] = frameAlong(S, sub(ai.mid, S), scl(apole, -1));
      fr[`fore${n}`] = frameAlong(ai.mid, sub(ai.end, ai.mid), col(fr[`hum${n}`].R, 2));
      fr[`hand${n}`] = fmul(fmul(fr[`fore${n}`], ftr([0, -D.fore, 0])), frot(rx(-(A.flex || 0))));
      J[`elbow${n}`] = ai.mid; J[`wrist${n}`] = ai.end;
    });
    return { c: { look: pose.face?.look || [0, 0], pupil: pose.face?.pupil ?? 1 }, ev: { fr, J, flags, dyn: {} } };
  }

  const drawBones = makeBoneRenderer(seed ^ 0x77);
  function draw(ctx, ink, pose, ev, sec, view, drawIndex, opts = {}) {
    return drawBones(ctx, model, ev, { look: pose.face?.look || [0, 0], pupil: pose.face?.pupil ?? 1 }, view, drawIndex, { extras: opts.extras || [], filter: opts.filter });
  }
  const ZERO = { jaw: 0, hatLift: 0, hatTilt: 0, ribs: new Array(12).fill(0), ribsL: new Array(12).fill(0), coccyx: 0, fingers: [0, 0], nod: 0 };
  return { profile, model, evaluatePose, draw, secondary: () => ({ at: () => ZERO }), hatFrame: () => null, ZERO_SEC: ZERO, toControls: (p) => p };
}
