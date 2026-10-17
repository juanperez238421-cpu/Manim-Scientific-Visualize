// Period lettering for equations: a tiny math typesetter for Canvas 2D in the film's fonts.
// Markup:  x_{0}  subscript   t^{2}  superscript   \sqrt{10}  radical (drawn, not a glyph)
//          \down \up  arrows (drawn)   \cdot  centred dot   \approx  wavy equals (drawn)
// Fonts: Poiret One (text, digits) and Limelight (headings); both latin-subset: anything outside
// it (₀, ², √, ↓, ≈) is drawn with strokes so the lettering never falls back to a system font.
import { G } from '../../packages/bonemotion/src/render/ink.js';

function tokenize(src) {
  const out = [];
  let i = 0;
  const group = () => { // reads {...} at i
    if (src[i] !== '{') { const c = src[i]; i++; return c; }
    let depth = 0, j = i;
    for (; j < src.length; j++) { if (src[j] === '{') depth++; else if (src[j] === '}') { depth--; if (depth === 0) break; } }
    const s = src.slice(i + 1, j); i = j + 1; return s;
  };
  let buf = '';
  const flush = () => { if (buf) out.push({ k: 'txt', s: buf }); buf = ''; };
  while (i < src.length) {
    const c = src[i];
    if (c === '_' || c === '^') { flush(); i++; out.push({ k: c === '_' ? 'sub' : 'sup', s: group() }); continue; }
    if (c === '\\') {
      const m = /^\\([a-z]+)/.exec(src.slice(i));
      if (m) {
        flush(); i += m[0].length;
        if (m[1] === 'sqrt') out.push({ k: 'sqrt', s: group() });
        else out.push({ k: m[1] });
        continue;
      }
    }
    buf += c; i++;
  }
  flush();
  return out;
}

// measure or draw; returns the advance width
export function mathLine(ctx, src, x, y, size, { font = 'Noto Serif', fill = G.white, stroke = G.ink, draw = true, weight = 1 } = {}) {
  const toks = tokenize(src);
  let cx = x;
  const setFont = (sz) => { ctx.font = `400 ${sz}px "${font}"`; };
  const text = (s, sz, yy) => {
    setFont(sz);
    const w = ctx.measureText(s).width;
    if (draw) {
      ctx.lineJoin = 'round';
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = Math.max(3, sz * 0.12) * weight; ctx.strokeText(s, cx, yy); }
      ctx.fillStyle = fill; ctx.fillText(s, cx, yy);
    }
    return w;
  };
  const line = (pts, lw) => {
    if (!draw) return;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw + Math.max(3, size * 0.1); ctx.beginPath(); pts.forEach((p, k) => (k ? ctx.lineTo(...p) : ctx.moveTo(...p))); ctx.stroke(); }
    ctx.strokeStyle = fill; ctx.lineWidth = lw; ctx.beginPath(); pts.forEach((p, k) => (k ? ctx.lineTo(...p) : ctx.moveTo(...p))); ctx.stroke();
  };
  ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  const lw = Math.max(2, size * 0.07);
  for (const t of toks) {
    if (t.k === 'txt') cx += text(t.s, size, y);
    else if (t.k === 'sub') cx += mathLine(ctx, t.s, cx + 1, y + size * 0.22, size * 0.6, { font, fill, stroke, draw, weight: 0.8 }) + 2;
    else if (t.k === 'sup') cx += mathLine(ctx, t.s, cx + 1, y - size * 0.42, size * 0.6, { font, fill, stroke, draw, weight: 0.8 }) + 2;
    else if (t.k === 'sqrt') {
      const inner = mathLine(ctx, t.s, 0, 0, size, { font, draw: false });
      const h = size * 0.82, x0 = cx + size * 0.05;
      line([[x0, y - h * 0.38], [x0 + size * 0.12, y - h * 0.48], [x0 + size * 0.26, y + size * 0.06], [x0 + size * 0.44, y - h], [x0 + size * 0.5 + inner + size * 0.08, y - h]], lw);
      cx = x0 + size * 0.5;
      cx += mathLine(ctx, t.s, cx, y, size, { font, fill, stroke, draw }) + size * 0.1;
    } else if (t.k === 'down' || t.k === 'up') {
      const s2 = t.k === 'down' ? 1 : -1, ax = cx + size * 0.28, top = y - size * 0.72, bot = y + size * 0.02;
      const [a, b] = s2 > 0 ? [top, bot] : [bot, top];
      line([[ax, a], [ax, b]], lw);
      line([[ax - size * 0.16, b - s2 * size * 0.2], [ax, b], [ax + size * 0.16, b - s2 * size * 0.2]], lw);
      cx += size * 0.6;
    } else if (t.k === 'to') {
      const yy = y - size * 0.3, x0 = cx + size * 0.15, x1 = cx + size * 0.85;
      line([[x0, yy], [x1, yy]], lw);
      line([[x1 - size * 0.2, yy - size * 0.15], [x1, yy], [x1 - size * 0.2, yy + size * 0.15]], lw);
      cx += size;
    } else if (t.k === 'rew') {
      // ◄◄ rewind mark: two drawn triangles
      if (draw) {
        for (const k of [0, 1]) {
          const x0 = cx + k * size * 0.55;
          ctx.beginPath(); ctx.moveTo(x0, y - size * 0.35); ctx.lineTo(x0 + size * 0.55, y - size * 0.72); ctx.lineTo(x0 + size * 0.55, y + size * 0.02); ctx.closePath();
          if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = Math.max(3, size * 0.08); ctx.stroke(); }
          ctx.fillStyle = fill; ctx.fill();
        }
      }
      cx += size * 1.25;
    } else if (t.k === 'approx') {
      const yy = y - size * 0.3, w = size * 0.55, x0 = cx + size * 0.12;
      for (const dy of [-size * 0.09, size * 0.09]) {
        const pts = []; for (let k = 0; k <= 10; k++) pts.push([x0 + (w * k) / 10, yy + dy + size * 0.06 * Math.sin((k / 10) * 2 * Math.PI)]);
        line(pts, lw * 0.8);
      }
      cx += size * 0.8;
    } else if (t.k === 'cdot') {
      if (draw) { ctx.fillStyle = fill; ctx.beginPath(); ctx.arc(cx + size * 0.2, y - size * 0.3, size * 0.06, 0, 2 * Math.PI); ctx.fill(); }
      cx += size * 0.4;
    } else if (t.k === 'minus') { line([[cx + size * 0.08, y - size * 0.3], [cx + size * 0.46, y - size * 0.3]], lw); cx += size * 0.56; }
  }
  return cx - x;
}
export const mathWidth = (ctx, src, size, font) => mathLine(ctx, src, 0, 0, size, { font, draw: false });

// lettering with a reveal: u in [0, 1] wipes the line on from the left (hand-lettered "write-on")
export function mathReveal(ctx, src, x, y, size, u, opts = {}) {
  if (u <= 0) return;
  const w = mathWidth(ctx, src, size, opts.font);
  ctx.save();
  ctx.beginPath(); ctx.rect(x - 20, y - size * 1.6, (w + 40) * Math.min(1, u), size * 2.4); ctx.clip();
  mathLine(ctx, src, x, y, size, opts);
  ctx.restore();
}

// letter-spaced caption (titles, panel labels)
export function spaced(ctx, text, cx, baseline, size, { font = 'Noto Serif', color = G.paper, track = 0.2, align = 'center', stroke = null } = {}) {
  ctx.font = `400 ${size}px "${font}"`;
  const ws = [...text].map((c) => ctx.measureText(c).width + track * size);
  const total = ws.reduce((a, b) => a + b, 0) - track * size;
  let x = align === 'center' ? cx - total / 2 : align === 'right' ? cx - total : cx;
  ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  [...text].forEach((c, i) => {
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = Math.max(3, size * 0.1); ctx.lineJoin = 'round'; ctx.strokeText(c, x, baseline); }
    ctx.fillStyle = color; ctx.fillText(c, x, baseline); x += ws[i];
  });
  return total;
}
