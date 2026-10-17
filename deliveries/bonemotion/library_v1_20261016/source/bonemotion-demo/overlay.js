// Crisp overlays drawn after the film look: the segment title, the live phase bar (which principle of
// animation is happening right now) and a data card (physics read-outs, parameters).
import { mathLine } from './text.js';

const TOK = { BG: '#FFFFFF', INK: '#151515', MUTED: '#6E6E6E', RULE: '#D6D6D6', FILL: '#F3F3F3', ACC: '#B03A2E', VEL: '#B7791F', POS: '#2C6E9B', GAL: '#2F7D5B' };
const SERIF = 'Noto Serif';
export const PHASE_SETS = {
  action: [['prep', 'Preparación'], ['antic', 'Anticipación'], ['exec', 'Ejecución'], ['follow', 'Proyección'], ['settle', 'Asentamiento']],
  walk: [['prep', 'Preparación'], ['contact', 'Contacto'], ['down', 'Bajada'], ['passing', 'Paso'], ['up', 'Subida'], ['settle', 'Asentamiento']],
};

export function makeOverlay(ctx, W, H) {
  const font = (px, w = 400, it = false) => `${it ? 'italic ' : ''}${w} ${px}px "${SERIF}"`;
  const text = (s, x, y, px, col = TOK.INK, { w = 400, align = 'left', it = false } = {}) => { ctx.font = font(px, w, it); ctx.fillStyle = col; ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.fillText(s, x, y); ctx.textAlign = 'left'; };
  const card = (x, y, w, h, border = TOK.RULE) => { ctx.save(); ctx.globalAlpha *= 0.95; ctx.fillStyle = TOK.BG; ctx.fillRect(x, y, w, h); ctx.restore(); ctx.strokeStyle = border; ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h); };
  const measure = (s, px, w = 400) => { ctx.font = font(px, w); return ctx.measureText(s).width; };

  function title(seg) {
    const x = 210, y = 128;
    const w = Math.max(measure(seg.title.toUpperCase(), 30, 700), measure(seg.sub || '', 21)) + 150;
    card(x, y, w, 104);
    ctx.fillStyle = TOK.INK; ctx.fillRect(x + 16, y + 16, 72, 72);
    text(seg.num, x + 52, y + 64, 32, TOK.BG, { w: 700, align: 'center' });
    text(seg.title.toUpperCase(), x + 108, y + 52, 30, TOK.INK, { w: 700 });
    text(seg.sub || '', x + 108, y + 86, 21, TOK.MUTED);
  }
  function phaseBar(set, active, prog) {
    const items = PHASE_SETS[set];
    const px = 22, gap = 14, padX = 22;
    const ws = items.map(([, l]) => measure(l.toUpperCase(), px, 700) + 2 * padX);
    const total = ws.reduce((a, b) => a + b, 0) + gap * (items.length - 1);
    let x = (W - total) / 2;
    const y = H - 112;
    items.forEach(([k, l], i) => {
      const on = k === active;
      ctx.save();
      ctx.fillStyle = on ? TOK.ACC : 'rgba(255,255,255,0.92)';
      ctx.strokeStyle = on ? TOK.ACC : TOK.RULE; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.roundRect(x, y, ws[i], 46, 23); ctx.fill(); ctx.stroke();
      if (on && prog !== null) { ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fillRect(x + 14, y + 38, (ws[i] - 28) * prog, 3); }
      ctx.restore();
      text(l.toUpperCase(), x + ws[i] / 2, y + 31, px, on ? TOK.BG : TOK.MUTED, { w: 700, align: 'center' });
      x += ws[i] + gap;
    });
  }
  function dataCard(lines, x = W - 220 - 520, y = 128) {
    const h = 30 + lines.length * 44;
    const w = 520;
    card(x, y, w, h);
    lines.forEach((l, i) => {
      const yy = y + 50 + i * 44;
      if (l.head) text(l.head, x + 24, yy, 22, TOK.INK, { w: 700 });
      else mathLine(ctx, l.m, x + 24, yy, l.px || 28, { font: SERIF, fill: l.col || TOK.INK, stroke: null });
    });
  }
  function draw(seg, lt, frame, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha;
    title(seg);
    if (frame.phaseSet) {
      const ph = frame.phase;
      phaseBar(frame.phaseSet, ph ? ph.name : null, ph ? Math.min(1, Math.max(0, (lt - ph.t0) / (ph.t1 - ph.t0))) : null);
    }
    if (frame.data && frame.data.length) dataCard(frame.data);
    for (const L of frame.cards || []) {
      ctx.font = font(24, 700);
      const w = Math.max(ctx.measureText(L.text).width, L.sub ? measure(L.sub, 19) : 0) + 36;
      const h = L.sub ? 74 : 46;
      card(L.x - w / 2, L.y, w, h, L.col || TOK.RULE);
      text(L.text, L.x, L.y + 31, 24, L.col || TOK.INK, { w: 700, align: 'center' });
      if (L.sub) text(L.sub, L.x, L.y + 60, 19, TOK.MUTED, { align: 'center' });
    }
    if (frame.note) {
      ctx.font = font(20, 400, true);
      const w = ctx.measureText(frame.note).width + 40;
      card((W - w) / 2, H - 66, w, 38);
      text(frame.note, W / 2, H - 40, 20, TOK.MUTED, { it: true, align: 'center' });
    }
    ctx.restore();
  }
  // a small caption card on the stage (crisp, drawn on the cel before the film look)
  function label({ x, y, text: s, col = TOK.INK, sub }) {
    const c = ctx; void c;
  }
  return { draw, TOK, label };
}
export { TOK };
