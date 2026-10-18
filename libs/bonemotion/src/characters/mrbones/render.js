// Ink-and-paint renderer for the 3-D bone rig (browser only).
// Orthographic projection with a slight downward camera pitch. Every part is convex (sphere,
// tapered capsule, disc, ellipsoid) so its silhouette is the convex hull of its projected
// samples — exact for spheres, capsules and discs. A bone is the union of its parts: stroke the
// union with 2x the line width, then fill it, so only the outer outline survives.
import { mm, mv, rx, add, sub, scl, cross, norm, dot, fapp } from '../../core/m3.js';
import { objectFrames } from './model.js';
import { rnd } from '../../render/clock.js';

const TONES = {
  bone: { light: [240, 239, 234], dark: [183, 182, 176] },
  cart: { light: [198, 198, 194], dark: [146, 146, 142] },
  tooth: { light: [247, 247, 244], dark: [202, 202, 198] },
};
const BACK = [62, 62, 62];
const INK = '#141414';
const mixc = (a, b, u) => `rgb(${a.map((x, i) => Math.round(x + (b[i] - x) * u)).join(',')})`;

function hull(P) {
  if (P.length < 3) return P;
  P.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [];
  for (const p of P) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
  const up = [];
  for (let i = P.length - 1; i >= 0; i--) { const p = P[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
  up.pop(); lo.pop();
  return lo.concat(up);
}
const area = (P) => { let a = 0; for (let i = 0; i < P.length; i++) { const p = P[i], q = P[(i + 1) % P.length]; a += p[0] * q[1] - q[0] * p[1]; } return a / 2; };
function perp(v) { const a = Math.abs(v[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0]; const u = norm(cross(v, a)); return [u, cross(v, u)]; }

export function makeBoneRenderer(seed) {
  return function drawSkeleton(ctx, model, ev, c, view, drawIndex, opts = {}) {
    const { x0, y0, S } = view;
    const Rp = rx(view.pitch || 0);
    const k = S / 1.17;
    const proj = (p) => { const q = mv(Rp, p); return [x0 + S * q[0], y0 - S * q[1], q[2]]; };
    // opts.mapObjects lets a caller move whole bones rigidly (assembly, bursts) before drawing
    let objs = objectFrames(model, ev, c);
    if (opts.mapObjects) objs = opts.mapObjects(objs);
    const chestZ = mv(Rp, ev.fr.chest.t)[2];
    const items = [];

    for (const o of objs) {
      const d = o.def;
      if (opts.filter && !opts.filter(d)) continue;
      const W = { R: mm(Rp, o.F.R), t: mv(Rp, o.F.t) };
      const P = (p) => { const q = add(mv(W.R, p), W.t); return [x0 + S * q[0], y0 - S * q[1], q[2]]; };
      const facing = (n) => mv(W.R, n)[2];
      if (d.kind === 'socket') {
        const z = P(d.socket.c)[2] + d.bias;
        items.push({ z, draw: () => drawSocket(d, P, facing, W, c) });
        continue;
      }
      if (d.kind === 'decal') {
        items.push({ z: P(partsCentreOfDecals(d))[2] + d.bias, draw: () => drawDecals(d, P, facing, k) });
        continue;
      }
      const pieces = d.dyn ? [ev.dyn[d.dyn]] : d.pieces || [d.parts];
      pieces.forEach((parts, pi) => {
        const outlines = [];
        let zs = 0, zn = 0;
        parts.forEach((pt, pj) => {
          const ol = outline(pt, P, S);
          if (ol.pts.length >= 3) outlines.push(ol.pts);
          zs += ol.z; zn++;
        });
        if (!outlines.length) return;
        // a held prop sorts with the fist that holds it (just under the fingers), not by its own centre
        // a held prop sorts with the fist that holds it (just under the fingers), and never behind what
        // its working end touches (the mallet head sits on the rib's front surface at a strike)
        let z = zs / zn + d.bias;
        if (d.zFrom && ev.fr[d.zFrom]) z = Math.max(mv(Rp, ev.fr[d.zFrom].t)[2] + d.bias, mv(Rp, fapp(o.F, d.zEnd))[2] + 3);
        items.push({ z, draw: () => paintUnion(d, outlines, pi, z) });
      });
    }
    for (const ex of opts.extras || []) items.push(ex);
    items.sort((a, b) => a.z - b.z);
    for (const it of items) it.draw();

    // ---------------------------------------------------------------- painters
    function outline(pt, P, S) {
      const circ = (cs, r, n) => { const out = []; for (let i = 0; i < n; i++) { const a = (2 * Math.PI * i) / n; out.push([cs[0] + r * Math.cos(a), cs[1] + r * Math.sin(a)]); } return out; };
      const nOf = (rpx) => Math.max(10, Math.min(28, Math.round(rpx * 1.1)));
      if (pt.t === 'sph') { const cs = P(pt.c); return { pts: circ(cs, pt.r * S, nOf(pt.r * S)), z: cs[2] }; }
      if (pt.t === 'cap') {
        const a = P(pt.a), b = P(pt.b);
        return { pts: hull([...circ(a, pt.ra * S, nOf(pt.ra * S)), ...circ(b, pt.rb * S, nOf(pt.rb * S))]), z: (a[2] + b[2]) / 2 };
      }
      if (pt.t === 'cyl') {
        const ax = norm(sub(pt.b, pt.a)); const [u, v] = perp(ax); const pts = [];
        let z = 0;
        for (const e of [pt.a, pt.b]) for (let i = 0; i < 16; i++) { const t = (2 * Math.PI * i) / 16; const q = P(add(e, add(scl(u, pt.r * Math.cos(t)), scl(v, pt.r * Math.sin(t))))); pts.push(q); z += q[2]; }
        return { pts: hull(pts.map((q) => [q[0], q[1]])), z: z / pts.length };
      }
      if (pt.t === 'ell') {
        const pts = []; let z = 0;
        for (let i = 1; i < 8; i++) for (let j = 0; j < 14; j++) {
          const th = (Math.PI * i) / 8, ph = (2 * Math.PI * j) / 14;
          const q = P(add(pt.c, [pt.r[0] * Math.sin(th) * Math.cos(ph), pt.r[1] * Math.cos(th), pt.r[2] * Math.sin(th) * Math.sin(ph)]));
          pts.push(q); z += q[2];
        }
        pts.push(P(add(pt.c, [0, pt.r[1], 0])), P(add(pt.c, [0, -pt.r[1], 0])));
        return { pts: hull(pts.map((q) => [q[0], q[1]])), z: z / (pts.length - 2) };
      }
      if (pt.t === 'poly') {
        const qs = pt.pts.map(P);
        return { pts: qs.map((q) => [q[0], q[1]]), z: qs.reduce((a, q) => a + q[2], 0) / qs.length };
      }
      return { pts: [], z: 0 };
    }

    function paintUnion(d, outlines, pi, z) {
      const amp = 0.45 * k;
      const path = new Path2D();
      outlines.forEach((ol, oi) => {
        let pts = ol;
        if (area(pts) > 0) pts = pts.slice().reverse(); // one winding for every part (non-zero union)
        pts.forEach((p, vi) => {
          const jx = (rnd(seed, drawIndex, d.uid, pi * 64 + oi, vi * 2) - 0.5) * 2 * amp;
          const jy = (rnd(seed, drawIndex, d.uid, pi * 64 + oi, vi * 2 + 1) - 0.5) * 2 * amp;
          if (vi === 0) path.moveTo(p[0] + jx, p[1] + jy); else path.lineTo(p[0] + jx, p[1] + jy);
        });
        path.closePath();
      });
      const tone = TONES[d.tone] || TONES.bone;
      const tint = d.prop ? 0 : Math.max(0, Math.min(0.55, (chestZ - z - 14) / 40));
      const lw = (d.small ? 1.25 : 2.0) * k;
      ctx.save();
      ctx.lineJoin = 'round';
      ctx.strokeStyle = INK;
      ctx.lineWidth = 2 * lw;
      ctx.stroke(path);
      ctx.fillStyle = mixc(tone.dark, BACK, tint);
      ctx.fill(path);
      ctx.clip(path);
      ctx.translate(1.5 * k, -1.7 * k); // moonlight from the upper right: shadow crescent lower left
      ctx.fillStyle = mixc(tone.light, BACK, tint);
      ctx.fill(path);
      ctx.restore();
      if (pi === 0 && d.decals.length) drawDecalsOf(d);
    }
    function drawDecalsOf(d) {
      const o = objs.find((q) => q.def === d);
      const W = { R: mm(Rp, o.F.R), t: mv(Rp, o.F.t) };
      const P = (p) => { const q = add(mv(W.R, p), W.t); return [x0 + S * q[0], y0 - S * q[1], q[2]]; };
      drawDecals(d, P, (n) => mv(W.R, n)[2], k);
    }
    function drawDecals(d, P, facing, k) {
      for (const dc of d.decals) {
        ctx.save();
        ctx.strokeStyle = INK; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        if (dc.t === 'sline') {
          ctx.lineWidth = dc.w * k;
          if (dc.dash) ctx.setLineDash(dc.dash.map((x) => x * k));
          ctx.beginPath();
          let pen = false;
          for (const q of dc.pts) {
            const f = facing(q.n);
            const s = P(q.p);
            if (f > 0.12) { if (pen) ctx.lineTo(s[0], s[1]); else ctx.moveTo(s[0], s[1]); pen = true; } else pen = false;
          }
          ctx.stroke();
        } else if (dc.t === 'line') {
          ctx.lineWidth = dc.w * k;
          ctx.beginPath();
          dc.pts.forEach((p, i) => { const s = P(p); if (i) ctx.lineTo(s[0], s[1]); else ctx.moveTo(s[0], s[1]); });
          ctx.stroke();
        } else if (dc.t === 'disc') {
          const f = facing(dc.n);
          if (f > 0.05) {
            const v = cross(dc.n, dc.u);
            ctx.beginPath();
            for (let i = 0; i < 16; i++) {
              const a = (2 * Math.PI * i) / 16;
              const s = P(add(dc.c, add(scl(dc.u, dc.r[0] * Math.cos(a)), scl(v, dc.r[1] * Math.sin(a)))));
              if (i) ctx.lineTo(s[0], s[1]); else ctx.moveTo(s[0], s[1]);
            }
            ctx.closePath(); ctx.fillStyle = dc.fill; ctx.fill();
          }
        } else if (dc.t === 'dpoly') {
          const f = facing(dc.n);
          if (f > 0.05) {
            ctx.beginPath();
            dc.pts.forEach((p, i) => { const s = P(p); if (i) ctx.lineTo(s[0], s[1]); else ctx.moveTo(s[0], s[1]); });
            ctx.closePath(); ctx.fillStyle = dc.fill; ctx.fill();
            ctx.lineWidth = 1.4 * k; ctx.stroke();
          }
        }
        ctx.restore();
      }
    }
    function drawSocket(d, P, facing, W, c) {
      const so = d.socket;
      const f = facing(so.n);
      if (f <= 0.02) return;
      const v = cross(so.n, so.u);
      ctx.save();
      ctx.beginPath();
      for (let i = 0; i < 24; i++) {
        const a = (2 * Math.PI * i) / 24;
        const r = [so.r[0] * (1 + 0.06 * Math.sin(3 * a + d.side)), so.r[1]];
        const s = P(add(so.c, add(scl(so.u, r[0] * Math.cos(a)), scl(v, r[1] * Math.sin(a)))));
        if (i) ctx.lineTo(s[0], s[1]); else ctx.moveTo(s[0], s[1]);
      }
      ctx.closePath();
      ctx.fillStyle = '#060606'; ctx.fill();
      ctx.strokeStyle = INK; ctx.lineWidth = 1.8 * k; ctx.stroke();
      // glowing pin-point pupil (with a pie-cut glint) floating in the dark socket
      if (f > 0.25 && (c.pupil ?? 1) > 0.04) {
        const look = c.look || [0, 0];
        const pu = c.pupil ?? 1;
        const cpt = add(so.c, add(scl(so.u, d.side * 0 + look[0] * 3.6), scl(v, look[1] * 3.6 - 1.5)));
        const s = P(add(cpt, scl(so.n, 0.5)));
        const r = Math.max(0.2, 1.5 + 1.3 * (pu - 1)) * S * Math.min(1, pu * 2);
        const g = ctx.createRadialGradient(s[0], s[1], 0, s[0], s[1], r * 4.5);
        g.addColorStop(0, 'rgba(255,255,255,0.55)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(s[0], s[1], r * 4.5, 0, 2 * Math.PI); ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.arc(s[0], s[1], r, 0, 2 * Math.PI); ctx.fill();
        if (r > 2.2) { ctx.fillStyle = '#060606'; ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.arc(s[0], s[1], r * 1.05, -2.1, -1.2); ctx.closePath(); ctx.fill(); }
      }
      ctx.restore();
    }
    return { project: proj };
  };
}
function partsCentreOfDecals(d) {
  const q = d.decals[0].pts;
  return scl(q.reduce((a, b) => add(a, b), [0, 0, 0]), 1 / q.length);
}
