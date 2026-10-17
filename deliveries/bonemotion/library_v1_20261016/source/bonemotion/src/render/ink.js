// "Ink and paint" for a 1930s rubber-hose cartoon, in Canvas 2D.
// Every outline boils: vertices wobble by ~1 px per drawing (seeded by the drawing index),
// like hand-inked cels traced anew on every drawing. Colours are greys only (B&W film).
import { srnd } from './clock.js';

export const G = {
  ink: '#121212', black: '#161616', shadow: '#2a2a2a', night: '#3a3a3a', dusk: '#5c5c5c',
  mid: '#8a8a8a', stone: '#b4b4b4', light: '#cfcfcf', paper: '#e6e6e6', white: '#f4f4f4', glow: '#ffffff',
};

export function makeInk(ctx, seed) {
  let boil = 0; // drawing index
  let sid = 0; // shape counter (stable draw order -> stable ids)
  const LW = 4.2; // standard ink line width at 1440 px wide

  const begin = (drawIndex) => { boil = drawIndex; sid = 0; };
  const jit = (amp) => {
    const id = sid++;
    return (i, k) => amp * srnd(seed, boil, id, i, k);
  };

  // closed/open smooth path through points (Catmull-Rom -> cubic Bezier)
  function trace(pts, closed, amp = 1.0) {
    const j = jit(amp);
    const p = pts.map((q, i) => [q[0] + j(i, 0), q[1] + j(i, 1)]);
    const n = p.length;
    ctx.beginPath();
    ctx.moveTo(p[0][0], p[0][1]);
    const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) {
      const p0 = p[(i - 1 + n) % n], p1 = p[i], p2 = p[(i + 1) % n], p3 = p[(i + 2) % n];
      const a = closed || i > 0 ? p0 : p1, d = closed || i < n - 2 ? p3 : p2;
      ctx.bezierCurveTo(p1[0] + (p2[0] - a[0]) / 6, p1[1] + (p2[1] - a[1]) / 6,
        p2[0] - (d[0] - p1[0]) / 6, p2[1] - (d[1] - p1[1]) / 6, p2[0], p2[1]);
    }
    if (closed) ctx.closePath();
  }

  function shape(pts, { fill = null, ink = G.ink, lw = LW, closed = true, amp = 1.0 } = {}) {
    trace(pts, closed, amp);
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (ink && lw > 0) { ctx.strokeStyle = ink; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); }
  }

  function ellipsePts(cx, cy, rx, ry, rot = 0, n = 14) {
    const c = Math.cos(rot), s = Math.sin(rot), out = [];
    for (let i = 0; i < n; i++) {
      const a = (2 * Math.PI * i) / n;
      const x = rx * Math.cos(a), y = ry * Math.sin(a);
      out.push([cx + x * c - y * s, cy + x * s + y * c]);
    }
    return out;
  }
  const blob = (cx, cy, rx, ry, rot, opts) => shape(ellipsePts(cx, cy, rx, ry, rot, Math.max(10, Math.round((rx + ry) / 5))), opts);

  // rubber hose: a limb from p0 to p1 that bends sideways by `bend` (fraction of length)
  function hosePts(p0, p1, bend) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1];
    const L = Math.hypot(dx, dy) || 1;
    const cx = (p0[0] + p1[0]) / 2 - (dy / L) * bend * L, cy = (p0[1] + p1[1]) / 2 + (dx / L) * bend * L;
    const pts = [];
    for (let i = 0; i <= 8; i++) {
      const u = i / 8;
      pts.push([(1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * cx + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * cy + u * u * p1[1]]);
    }
    return pts;
  }
  function hose(p0, p1, bend, w, fill = G.black, lw = LW) {
    const pts = hosePts(p0, p1, bend);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    trace(pts, false, 0.8);
    ctx.strokeStyle = G.ink; ctx.lineWidth = w + 2 * lw; ctx.stroke();
    if (fill && fill !== G.ink && fill !== G.black) {
      trace(pts, false, 0.4);
      ctx.strokeStyle = fill; ctx.lineWidth = w; ctx.stroke();
    }
    return pts;
  }

  // white four-fingered glove (three fingers + thumb), cuff with three stitch lines
  function glove(x, y, ang, s = 1, pose = 'open', flip = 1) {
    ctx.save();
    ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s * flip, s);
    const W = G.white;
    // cuff (flares toward the wrist end)
    shape([[-14, -10], [-2, -16], [-2, 16], [-14, 10]], { fill: W });
    for (const yy of [-6, 0, 6]) shape([[-11, yy], [-4, yy * 1.3]], { closed: false, lw: 2 });
    if (pose === 'fist') {
      blob(14, 0, 17, 15, 0, { fill: W });
      for (const yy of [-7, 0, 7]) shape([[22, yy - 3], [28, yy], [22, yy + 3]], { closed: false, lw: 2.2 });
      blob(10, -14, 7, 5, -0.5, { fill: W });
    } else if (pose === 'point') {
      blob(12, 0, 14, 13, 0, { fill: W });
      shape(ellipsePts(32, -3, 14, 5.5, -0.1, 10), { fill: W });
      blob(12, -14, 6, 5, -0.8, { fill: W });
    } else {
      // open / jazz hand: three fanned fingers
      const spread = pose === 'jazz' ? 0.42 : 0.28;
      for (let k = -1; k <= 1; k++) {
        const a = k * spread;
        shape(ellipsePts(16 + 16 * Math.cos(a), 16 * Math.sin(a) * 1.1, 13, 6, a, 10), { fill: W });
      }
      blob(10, 0, 14, 14, 0, { fill: W });
      shape(ellipsePts(12, -18, 9, 5, -1.1, 10), { fill: W }); // thumb
    }
    ctx.restore();
  }

  function shoe(x, y, s = 1, flip = 1, ang = 0) {
    ctx.save();
    ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s * flip, s);
    shape([[-12, 0], [-10, -14], [8, -16], [30, -10], [36, 0], [26, 6], [-6, 6]], { fill: G.black });
    shape(ellipsePts(20, -8, 6, 3, -0.2, 8), { fill: G.white, ink: null, lw: 0, amp: 0.3 });
    ctx.restore();
  }

  // pie-cut eye: an oval with a wedge cut out (the classic early-30s eye)
  function pieEye(x, y, rx, ry, look = [0, 0], blink = 0, cut = 'white') {
    const h = ry * (1 - 0.9 * blink);
    blob(x, y, rx, h, 0, { fill: G.black, lw: 2 });
    if (blink < 0.6) {
      const px = x + look[0] * rx * 0.25, py = y + look[1] * h * 0.25 - h * 0.25;
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.arc(px, py, Math.min(rx, h) * 0.62, -Math.PI * 0.62, -Math.PI * 0.38);
      ctx.closePath();
      ctx.fillStyle = cut === 'white' ? G.white : G.paper;
      ctx.fill();
    }
  }

  // motion streaks ("speed lines") behind a moving thing
  function speedLines(x, y, dx, dy, n = 4, len = 70) {
    const L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
    ctx.save(); ctx.strokeStyle = G.ink; ctx.lineCap = 'round';
    for (let k = 0; k < n; k++) {
      const o = (k - (n - 1) / 2) * 14;
      ctx.lineWidth = 3;
      shape([[x - ux * 20 - uy * o, y - uy * 20 + ux * o], [x - ux * (20 + len * (0.6 + 0.4 * ((k * 7) % 3) / 2)) - uy * o, y - uy * (20 + len) + ux * o]], { closed: false, lw: 3, amp: 0.6 });
    }
    ctx.restore();
  }

  // little "shock" lines around a surprised head
  function takeLines(x, y, r, amount = 1) {
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * Math.PI * 2 + 0.2;
      const r0 = r * 1.05, r1 = r * (1.05 + 0.35 * amount);
      shape([[x + r0 * Math.cos(a), y + r0 * Math.sin(a)], [x + r1 * Math.cos(a), y + r1 * Math.sin(a)]], { closed: false, lw: 3.4 });
    }
  }

  return { begin, shape, blob, ellipsePts, trace, hose, hosePts, glove, shoe, pieEye, speedLines, takeLines, LW, ctx };
}
