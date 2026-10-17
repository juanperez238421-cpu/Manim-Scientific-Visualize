// bonemotion — demo reel renderer (1920x1080, 60 fps on ones: a new pose every frame).
// One segment per animation of the library; each opens and closes with an iris. The ink "boils" at
// 12 drawings/s (hand-drawn life) while the motion itself is sampled at the full frame rate.
import { makeInk, G } from '../../packages/bonemotion/src/render/ink.js';
import { makeFilm, iris } from '../../packages/bonemotion/src/render/film.js';
import { createMrBones } from '../../packages/bonemotion/src/characters/mrbones/index.js';
import { createMannequin } from '../../packages/bonemotion/src/characters/mannequin/index.js';
import { drawStage, drawDrapes, contactShadow, project } from './stage.js';
import { makeOverlay } from './overlay.js';
import { buildSegments } from './segments.js';

async function boot() {
  const tl = await fetch('./timeline.json').then((r) => r.json());
  await Promise.all([document.fonts.load('400 40px "Noto Serif"'), document.fonts.load('700 40px "Noto Serif"'), document.fonts.load('italic 400 40px "Noto Serif"')]);
  await document.fonts.ready;
  const W = tl.project.width, H = tl.project.height, FPS = tl.project.fps, BOIL = tl.project.boilPerSecond || 12;
  const out = document.getElementById('film');
  const octx = out.getContext('2d', { willReadFrequently: true });
  const cel = document.createElement('canvas'); cel.width = W; cel.height = H;
  const cctx = cel.getContext('2d', { willReadFrequently: true });
  const ink = makeInk(cctx, tl.project.seed);
  const ghost = document.createElement('canvas'); ghost.width = W; ghost.height = H;
  const gctx = ghost.getContext('2d');
  const ghostInk = makeInk(gctx, tl.project.seed + 1);
  const film = makeFilm(W, H, tl.project.seed);
  const chars = { mrbones: createMrBones({ seed: tl.project.seed }), mannequin: createMannequin({ seed: tl.project.seed }) };
  const weights = await fetch('../../packages/bonemotion/src/neural/weights/inbetween_v1.json').then((r) => r.json());
  const segs = buildSegments(chars, tl, { weights });
  // lay the segments end to end
  let acc = 0;
  for (const s of segs) { s.t0 = acc; acc += s.dur; }
  const total = acc;
  const OV = makeOverlay(octx, W, H);
  window.SEGMENTS = segs.map((s) => ({ id: s.id, title: s.title, t0: s.t0, dur: s.dur }));

  async function renderAtTime(t, o = {}) {
    const f = Math.round(t * FPS);
    const seg = segs.find((s) => t >= s.t0 && t < s.t0 + s.dur) || segs[segs.length - 1];
    const lt = t - seg.t0;
    const boil = Math.floor(t * BOIL + 1e-9);
    ink.begin(boil); ghostInk.begin(boil);
    const frame = seg.frame(lt);
    const cam = frame.cam;
    cctx.setTransform(1, 0, 0, 1, 0, 0);
    drawStage(ink, W, H, cam, lt, { spot: frame.spot, spotR: frame.spotR || 170 });
    for (const a of frame.actors) {
      for (const sh of a.shadows || []) contactShadow(cctx, cam, sh.p, sh.r || 60, sh.k || 0.45);
    }
    if (frame.under) frame.under(cctx, cam);
    for (const a of frame.actors) {
      if (a.ghost) { // a faint reference skeleton (the ground truth), composited as one layer
        gctx.setTransform(1, 0, 0, 1, 0, 0); gctx.clearRect(0, 0, W, H);
        a.char.draw(gctx, ghostInk, a.pose, a.ev, a.sec, cam, boil, { ...(a.opts || {}), noHat: false });
        cctx.save(); cctx.globalAlpha = a.ghost; cctx.drawImage(ghost, 0, 0); cctx.restore();
      } else a.char.draw(cctx, ink, a.pose, a.ev, a.sec, cam, boil, a.opts || {});
    }
    if (frame.over) frame.over(cctx, cam, ink);
    drawDrapes(ink, W, H, t, 1);
    // iris in / out at the ends of every segment (on the cel, before the film look)
    const io = Math.min(1, lt / 0.5, (seg.dur - lt - 1 / FPS) / 0.5);
    const R = Math.hypot(W, H);
    if (io < 1) iris(cctx, W, H, frame.focus ? frame.focus[0] : W / 2, frame.focus ? frame.focus[1] : H / 2, R * Math.max(0, io) ** 1.6);
    let fx = null;
    if (o.film !== false) fx = film.apply(octx, cel, f, t, { strength: 0.8 }); else { octx.setTransform(1, 0, 0, 1, 0, 0); octx.drawImage(cel, 0, 0); }
    octx.setTransform(1, 0, 0, 1, 0, 0);
    if (io > 0.02) OV.draw(seg, lt, frame, Math.min(1, io * 1.5));
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    return { t, frameIndex: f, drawing: boil, scene: seg.id, layers: [seg.id], film: fx };
  }
  window.STUDIO = { ready: true, duration: total, fps: FPS, renderAtTime, info: { production: tl.project.slug, segments: window.SEGMENTS } };
  void G; void project;
}
boot().catch((e) => { window.STUDIO = { ready: false, error: String(e && e.stack ? e.stack : e) }; console.error(e); });
