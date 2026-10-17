// The vaudeville stage, drawn in the period ink style: back wall, boards in depth, drapes and valance,
// footlights, a follow-spot and contact shadows. The camera is the rig's orthographic view
// { x0, y0, S (px per u), pitch }: world (x, y, z) -> screen (x0 + S x, y0 - S (cos p y - sin p z)).
import { G } from '../../packages/bonemotion/src/render/ink.js';
import { rnd, vnoise } from '../../packages/bonemotion/src/render/clock.js';

export const project = (cam, p) => {
  const c = Math.cos(cam.pitch || 0), s = Math.sin(cam.pitch || 0);
  return [cam.x0 + cam.S * p[0], cam.y0 - cam.S * (c * p[1] - s * p[2]), s * p[1] + c * p[2]];
};

export function drawStage(ink, W, H, cam, t, { spot = null, spotR = 170, curtain = 1 } = {}) {
  const ctx = ink.ctx;
  const BACK_Z = -260;
  const horizon = project(cam, [0, 0, BACK_Z])[1];
  // back wall
  const g = ctx.createLinearGradient(0, 0, 0, horizon);
  g.addColorStop(0, '#141414'); g.addColorStop(1, '#3b3b3b');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, horizon + 1);
  // wainscot rail and painted panels on the back wall
  ctx.strokeStyle = 'rgba(10,10,10,0.6)'; ctx.lineWidth = 3;
  const rail = horizon - 120 * cam.S;
  ctx.beginPath(); ctx.moveTo(0, rail); ctx.lineTo(W, rail); ctx.stroke();
  for (let x = -40; x < W; x += 240) { ctx.strokeRect(x + 20, rail + 18, 200, horizon - rail - 34); }
  // floor boards
  const fg = ctx.createLinearGradient(0, horizon, 0, H);
  fg.addColorStop(0, '#4a4a4a'); fg.addColorStop(1, '#6b6b6b');
  ctx.fillStyle = fg; ctx.fillRect(0, horizon, W, H - horizon);
  ctx.strokeStyle = 'rgba(20,20,20,0.55)'; ctx.lineWidth = 1.6;
  for (let z = BACK_Z; z < 900; z += 46) { const y = project(cam, [0, 0, z])[1]; if (y > horizon && y < H) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); } }
  ctx.lineWidth = 1.1; ctx.strokeStyle = 'rgba(20,20,20,0.35)';
  for (let k = 0; k < 40; k++) {
    const x = ((k * 197 + 40) % W);
    const z0 = BACK_Z + 46 * Math.floor(rnd(5, k, 1) * 12);
    const y0 = project(cam, [0, 0, z0])[1], y1 = project(cam, [0, 0, z0 + 46])[1];
    ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y1); ctx.stroke();
  }
  ctx.strokeStyle = G.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, horizon); ctx.lineTo(W, horizon); ctx.stroke();
  // follow-spot pool on the floor + a soft beam
  if (spot) {
    const c = project(cam, [spot[0], 0, spot[2]]);
    const ry = spotR * cam.S * Math.sin(cam.pitch || 0.15) * 1.6 + 18;
    const rg = ctx.createRadialGradient(c[0], c[1], 0, c[0], c[1], spotR * cam.S);
    rg.addColorStop(0, 'rgba(255,255,255,0.28)'); rg.addColorStop(0.7, 'rgba(255,255,255,0.12)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.save(); ctx.translate(c[0], c[1]); ctx.scale(1, ry / (spotR * cam.S)); ctx.translate(-c[0], -c[1]);
    ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(c[0], c[1], spotR * cam.S, 0, 2 * Math.PI); ctx.fill(); ctx.restore();
    const beam = ctx.createLinearGradient(0, 0, 0, c[1]);
    beam.addColorStop(0, 'rgba(255,255,255,0.0)'); beam.addColorStop(1, 'rgba(255,255,255,0.07)');
    ctx.fillStyle = beam;
    ctx.beginPath(); ctx.moveTo(c[0] - 40, -10); ctx.lineTo(c[0] + 40, -10); ctx.lineTo(c[0] + spotR * cam.S, c[1]); ctx.lineTo(c[0] - spotR * cam.S, c[1]); ctx.closePath(); ctx.fill();
  }
  return { horizon };
}

// drapes and valance in front of everything (screen space), with slow breathing folds
export function drawDrapes(ink, W, H, t, open = 1) {
  const ctx = ink.ctx;
  const side = (dir) => {
    const w = 170 + (1 - open) * (W / 2 - 170);
    const x0 = dir < 0 ? 0 : W - w;
    const folds = 7;
    const pts = [];
    for (let k = 0; k <= 40; k++) {
      const y = (k / 40) * (H + 20) - 10;
      const sway = 6 * vnoise(31 + dir, t * 0.4 + k * 0.05);
      pts.push([dir < 0 ? w + sway + 14 * Math.sin(k * 0.5) : W - w + sway + 14 * Math.sin(k * 0.5), y]);
    }
    ctx.save();
    ctx.beginPath();
    if (dir < 0) { ctx.moveTo(-10, -10); pts.forEach((p) => ctx.lineTo(p[0], p[1])); ctx.lineTo(-10, H + 10); }
    else { ctx.moveTo(W + 10, -10); pts.forEach((p) => ctx.lineTo(p[0], p[1])); ctx.lineTo(W + 10, H + 10); }
    ctx.closePath();
    const lg = ctx.createLinearGradient(x0, 0, x0 + w, 0);
    for (let f = 0; f <= folds; f++) { const u = f / folds; lg.addColorStop(u, f % 2 ? '#2b2b2b' : '#151515'); }
    ctx.fillStyle = lg; ctx.fill();
    ctx.strokeStyle = G.ink; ctx.lineWidth = 4; ctx.stroke();
    // fold lines
    ctx.strokeStyle = 'rgba(0,0,0,0.6)'; ctx.lineWidth = 2;
    for (let f = 1; f < folds; f++) { const x = x0 + (w * f) / folds; ctx.beginPath(); ctx.moveTo(x, 0); ctx.bezierCurveTo(x + 8, H * 0.3, x - 8, H * 0.7, x + 4, H); ctx.stroke(); }
    // tie-back
    ctx.fillStyle = '#8a8a8a';
    const ty = H * 0.56, tx = dir < 0 ? w - 30 : W - w + 30;
    ctx.beginPath(); ctx.ellipse(tx, ty, 34, 9, dir * 0.3, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
    ctx.restore();
  };
  side(-1); side(1);
  // valance with scallops
  ctx.fillStyle = '#1b1b1b';
  ctx.beginPath(); ctx.moveTo(-10, -10); ctx.lineTo(W + 10, -10); ctx.lineTo(W + 10, 70);
  for (let x = W; x >= 0; x -= 96) ctx.quadraticCurveTo(x - 48, 118, x - 96, 70);
  ctx.closePath(); ctx.fill(); ctx.strokeStyle = G.ink; ctx.lineWidth = 4; ctx.stroke();
  ctx.strokeStyle = '#7a7a7a'; ctx.lineWidth = 3;
  ctx.beginPath(); for (let x = W; x >= 0; x -= 96) { ctx.moveTo(x, 64); ctx.quadraticCurveTo(x - 48, 108, x - 96, 64); } ctx.stroke();
  // footlights
  for (let k = 0; k < 14; k++) {
    const x = 120 + k * ((W - 240) / 13), y = H - 18;
    const rg = ctx.createRadialGradient(x, y, 0, x, y, 70);
    rg.addColorStop(0, 'rgba(255,255,255,0.35)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(x, y, 70, 0, 2 * Math.PI); ctx.fill();
    ctx.fillStyle = '#d8d8d8'; ctx.beginPath(); ctx.ellipse(x, y + 6, 16, 9, 0, Math.PI, 0); ctx.fill();
    ctx.strokeStyle = G.ink; ctx.lineWidth = 2.5; ctx.stroke();
  }
}

// soft contact shadow under a point on the floor (feet, a landing skull)
export function contactShadow(ctx, cam, p, r = 60, k = 0.45) {
  const c = project(cam, [p[0], 0, p[2]]);
  const h = Math.max(0, p[1]);
  const a = k * Math.max(0, 1 - h / 400);
  const rr = r * cam.S * (1 + h / 500);
  ctx.save();
  ctx.translate(c[0], c[1]); ctx.scale(1, 0.26);
  const rg = ctx.createRadialGradient(0, 0, 0, 0, 0, rr);
  rg.addColorStop(0, `rgba(0,0,0,${a})`); rg.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(0, 0, rr, 0, 2 * Math.PI); ctx.fill();
  ctx.restore();
}
