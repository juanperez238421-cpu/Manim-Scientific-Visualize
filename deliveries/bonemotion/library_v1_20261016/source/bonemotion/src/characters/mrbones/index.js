// Mr. Bones as a bonemotion character: profile (proportions for retargeting), pose -> rig controls,
// props (top hat, bone cane, detachable skull and arm) and drawing.
import { buildModel, evaluate, ZERO_SEC, DIM, FOOT } from './model.js';
import { makeBoneRenderer } from './render.js';
import { simulateSecondary } from './secondary.js';
import { drawHat, drawBowtie } from './costume.js';
import { fmul, ftr, frot, fapp, rz, ry, rx, mm, mv, sub, add, scl, len, norm, col, I3 } from '../../core/m3.js';

export const K = 200; // u per metre: Mr. Bones is 1.77 m to the top of the skull
export const CM_LOCAL = [0, 26, -4]; // skull centre of mass in the head frame
export const HAT_SEAT = [2, 53.5, -3]; // hat brim centre in the head frame

export function createMrBones({ seed = 7 } = {}) {
  const model = buildModel();
  const dims = {
    K, hipW: DIM.hip, thigh: DIM.femur, shin: DIM.tibia, legLen: DIM.femur + DIM.tibia, ankleH: 13.5, ballZ: 27, heelZ: -11,
    upper: DIM.humerus, fore: DIM.forearm, armLen: DIM.humerus + DIM.forearm, hand: 24,
    standH: 126, shoulder: [42.9, 117, 20.6], chest: [0, 100, 10], neck: [0, 161, 7], headTop: 228, shoulderW: 86,
    footRestX: 20, // ankle half-spacing at rest
  };
  const profile = {
    id: 'mrbones', name: 'Mr. Bones', K, dims, g: 9.81 * K,
    foot: { ball: FOOT.ball, heel: FOOT.heel },
    skullCM: CM_LOCAL, hatSeat: HAT_SEAT, canGrip: true, detachable: { skull: true, arm: true },
    // generous anatomical ranges for QA (radians)
    limits: { knee: [0.0, 2.6], elbow: [0.0, 2.7], spineFlex: [-0.6, 1.2], neck: [-0.9, 0.9] },
  };

  // ---------------------------------------------------------------- pose -> rig controls
  function toControls(pose) {
    const P = pose.props || {};
    const c = {
      visible: true, yaw: pose.root.yaw || 0, pelvis: pose.root.p, pelvisRot: [pose.root.tilt?.[0] || 0, 0, pose.root.tilt?.[1] || 0],
      spine: pose.spine || [0, 0, 0], neck: pose.neck || [0, 0, 0], head: pose.head || [0, 0, 0],
      jaw: pose.face?.jaw ?? 0.1, look: pose.face?.look || [0, 0], pupil: pose.face?.pupil ?? 1,
      shrug: pose.shrug || [0, 0], prot: pose.prot || [0, 0],
      leg: pose.legs.map((L) => ({ a: L.ankle, heading: L.heading || 0, pitch: L.pitch || 0, toe: L.toe || 0, plantW: L.plantW ?? 1, kneeOut: L.kneeOut ?? 0.25, pole: L.pole })),
      arm: pose.arms.map((A) => ({
        specs: A.specs, pole: A.pole, curl: A.curl || [0.2, 0.2, 0.2, 0.2], spread: A.spread ?? 0.3, pron: A.pron ?? 0.25, flex: A.flex ?? 0.1, dev: A.dev ?? 0,
        detached: A.detached || undefined,
      })),
      explode: P.explode || 0, collapse: null, headToss: null, bowtie: P.bowtie !== false,
      headFrame: P.skull && P.skull.mode !== 'attached' ? skullHeadFrame(P.skull) : null,
    };
    return c;
  }
  // a detached skull is placed by its centre of mass (cm) and orientation R
  const skullHeadFrame = (sk) => ({ R: sk.R, t: sub(sk.cm, mv(sk.R, CM_LOCAL)) });

  function evaluatePose(pose, sec = ZERO_SEC) {
    const c = toControls(pose);
    const ev = evaluate(model, c, sec);
    const P = pose.props || {};
    // the cane: authored in the world (prop leads, the hand follows its grip)
    ev.fr.cane = P.cane && P.cane.F ? P.cane.F : null;
    ev.fr.mallet = null;
    return { c, ev };
  }

  // hat frame: on the head (with its bounce), or anywhere in the world (clip-authored), with squash
  function hatFrame(pose, ev, sec) {
    const h = (pose.props && pose.props.hat) || { mode: 'head' };
    if (h.mode === 'none') return null;
    if (h.mode === 'world') return { F: h.F, squash: h.squash ?? 1 };
    // on the neck stump (the skull is away): sits on the atlas, a little lower
    if (h.mode === 'neck') return { F: fmul(ev.fr.headAttach, fmul(ftr([0, 10 + (h.lift || 0), -2]), frot(rz(-0.1 + (sec.hatTilt || 0))))), squash: h.squash ?? 1 };
    const sl = h.held ? 0 : Math.max(0, sec.hatLift || 0), st = h.held ? 0 : sec.hatTilt || 0;
    const F = fmul(ev.fr.head, fmul(ftr([HAT_SEAT[0], HAT_SEAT[1] + sl + (h.lift || 0), HAT_SEAT[2] + (h.fwd || 0)]), frot(mm(rz(-0.1 + st + (h.tilt || 0)), rx(h.pitch || 0)))));
    return { F, squash: h.squash ?? 1 };
  }

  // ---------------------------------------------------------------- drawing
  const drawBones = makeBoneRenderer(seed ^ 0x5b0e);
  function draw(ctx, ink, pose, ev, sec, view, drawIndex, opts = {}) {
    const Rp = rx(view.pitch || 0);
    const proj = (q) => { const r = mv(Rp, q); return [view.x0 + view.S * r[0], view.y0 - view.S * r[1], r[2]]; };
    const extras = [...(opts.extras || [])];
    const H = opts.noHat ? null : hatFrame(pose, ev, sec);
    if (H) {
      const o = proj(H.F.t), up = proj(fapp(H.F, [0, 10, 0])), fwd = proj(fapp(H.F, [0, 0, 10]));
      const rot = Math.atan2(up[0] - o[0], -(up[1] - o[1]));
      const fore = Math.max(0.22, Math.min(1, Math.hypot(up[0] - o[0], up[1] - o[1]) / (10 * view.S)));
      // the hat sorts with the head it sits on (or by its own depth when free)
      const z = o[2] + 4;
      extras.push({ z, draw: () => drawHat(ink, o[0], o[1], view.S * 0.92, rot, { squash: H.squash, fore, flip: fwd[2] < o[2] - 1e9 }) });
    }
    if (pose.props?.bowtie !== false && ev.fr.C7 && !opts.noBowtie) {
      const p = fapp(ev.fr.C7, [0, 3, 12.5]);
      const o = proj(p), xr = proj(fapp(ev.fr.C7, [10, 3, 12.5]));
      const facing = mv(mm(Rp, ev.fr.C7.R), [0, 0, 1])[2];
      if (facing > -0.2) extras.push({ z: o[2] + 8, draw: () => drawBowtie(ink, o[0], o[1], view.S, Math.atan2(xr[1] - o[1], xr[0] - o[0]), facing) });
    }
    const c = toControls(pose);
    return drawBones(ctx, model, ev, c, view, drawIndex, { extras, filter: opts.filter, mapObjects: opts.mapObjects });
  }

  // secondary motion for a clip: poseAt(t) over [t0, t1]
  function secondary(poseAt, { t0, t1, impulses = [], hatOnHead } = {}) {
    return simulateSecondary(model, (t) => toControls(poseAt(t)), { t0, t1, gravity: profile.g, impulses,
      hatOnHead: hatOnHead || ((t) => { const h = poseAt(t).props?.hat; return !h || (h.mode === 'head' && !h.held); }) });
  }

  return { profile, model, toControls, evaluatePose, hatFrame, draw, secondary, ZERO_SEC, skullHeadFrame };
}

// helpers shared by clips that handle Mr. Bones' skull
export const skullCM = (ev) => fapp(ev.fr.head, CM_LOCAL);
export { I3, len, norm, col, add, scl, ry };
