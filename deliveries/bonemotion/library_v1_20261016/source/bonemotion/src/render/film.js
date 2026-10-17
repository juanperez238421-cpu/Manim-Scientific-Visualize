// Period film look, applied after the cel layer is "photographed":
// gate weave, exposure flicker, grain, dust, scratches, vignette. All seeded by frame index.
import { rnd, srnd, vnoise } from './clock.js';

export function makeFilm(W, H, seed) {
  // grain: four 720x540 luminance tiles, drawn at 2x (grain ~2 px), picked per frame
  const tiles = [];
  for (let k = 0; k < 4; k++) {
    const c = document.createElement('canvas');
    c.width = 720; c.height = 540;
    const g = c.getContext('2d', { willReadFrequently: true });
    const im = g.createImageData(c.width, c.height);
    for (let i = 0; i < c.width * c.height; i++) {
      // sum of 3 uniforms ~ gaussian-ish grain centred on mid-grey
      const v = 128 + 70 * (rnd(seed, k, i, 1) + rnd(seed, k, i, 2) + rnd(seed, k, i, 3) - 1.5);
      im.data[4 * i] = im.data[4 * i + 1] = im.data[4 * i + 2] = v;
      im.data[4 * i + 3] = 255;
    }
    g.putImageData(im, 0, 0);
    tiles.push(c);
  }
  // scratches: a few long-lived vertical lines, scheduled once from the seed
  const scratches = [];
  for (let k = 0; k < 9; k++) {
    const start = Math.floor(rnd(seed, 900, k) * 700);
    scratches.push({ start, len: 10 + Math.floor(rnd(seed, 901, k) * 40), x: 80 + rnd(seed, 902, k) * (W - 160),
      drift: srnd(seed, 903, k) * 1.5, light: rnd(seed, 904, k) < 0.7, w: 1 + rnd(seed, 905, k) * 1.5 });
  }

  function apply(ctx, scene, f, t, opts = {}) {
    const strength = opts.strength ?? 1;
    // gate weave: slow drift + per-frame jitter
    const dx = (1.4 * vnoise(seed + 11, t * 2.2) + 0.5 * srnd(seed, f, 1)) * strength;
    const dy = (2.2 * vnoise(seed + 12, t * 1.7) + 0.7 * srnd(seed, f, 2)) * strength;
    const sc = 1.012;
    ctx.save();
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, W, H);
    ctx.translate(W / 2 + dx, H / 2 + dy);
    ctx.scale(sc, sc);
    ctx.drawImage(scene, -W / 2, -H / 2);
    ctx.restore();
    // exposure flicker
    const fl = (0.032 * srnd(seed, f, 3) + 0.022 * vnoise(seed + 13, t * 6)) * strength;
    ctx.fillStyle = fl > 0 ? `rgba(255,255,255,${fl})` : `rgba(0,0,0,${-fl * 1.4})`;
    ctx.fillRect(0, 0, W, H);
    // grain
    ctx.save();
    ctx.globalCompositeOperation = 'overlay';
    ctx.globalAlpha = 0.2 * strength;
    const tile = tiles[Math.floor(rnd(seed, f, 4) * 4)];
    const ox = -Math.floor(rnd(seed, f, 5) * 720), oy = -Math.floor(rnd(seed, f, 6) * 540);
    ctx.imageSmoothingEnabled = true; // soft 2x grain: period-like and far kinder to the encoder
    for (let x = ox; x < W; x += 1440) for (let y = oy; y < H; y += 1080) ctx.drawImage(tile, x, y, 1440, 1080);
    ctx.restore();
    // dust: specks and the odd hair, one frame each
    const nd = Math.floor(rnd(seed, f, 7) * 5 * strength);
    for (let k = 0; k < nd; k++) {
      const x = rnd(seed, f, 10, k) * W, y = rnd(seed, f, 11, k) * H, light = rnd(seed, f, 12, k) < 0.55;
      ctx.fillStyle = light ? 'rgba(245,245,245,0.85)' : 'rgba(5,5,5,0.85)';
      ctx.strokeStyle = ctx.fillStyle;
      if (rnd(seed, f, 13, k) < 0.25) {
        ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(x, y);
        ctx.bezierCurveTo(x + srnd(seed, f, 14, k) * 40, y + 20, x + srnd(seed, f, 15, k) * 40, y + 40, x + srnd(seed, f, 16, k) * 30, y + 60);
        ctx.stroke();
      } else {
        ctx.beginPath(); ctx.ellipse(x, y, 1.5 + 4 * rnd(seed, f, 17, k), 1.2 + 3 * rnd(seed, f, 18, k), rnd(seed, f, 19, k) * 3, 0, 2 * Math.PI); ctx.fill();
      }
    }
    // scratches
    for (const s of scratches) {
      if (f < s.start || f >= s.start + s.len) continue;
      const x = s.x + s.drift * (f - s.start) + srnd(seed, f, 20, s.start) * 1.2;
      ctx.strokeStyle = s.light ? 'rgba(235,235,235,0.35)' : 'rgba(0,0,0,0.35)';
      ctx.lineWidth = s.w;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x + srnd(seed, f, 21, s.start) * 3, H); ctx.stroke();
    }
    // vignette (projector hot-spot falloff)
    const g = ctx.createRadialGradient(W / 2, H / 2, H * 0.32, W / 2, H / 2, H * 0.9);
    g.addColorStop(0, 'rgba(0,0,0,0)');
    g.addColorStop(1, `rgba(0,0,0,${0.62 * strength})`);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    return { dx, dy, flicker: fl, dust: nd };
  }
  return { apply };
}

// iris wipe: everything outside the circle is black (drawn on the cel layer, before the film look)
export function iris(ctx, W, H, cx, cy, r) {
  if (r > Math.hypot(W, H)) return;
  ctx.save();
  ctx.beginPath();
  ctx.rect(-10, -10, W + 20, H + 20);
  ctx.arc(cx, cy, Math.max(0, r), 0, 2 * Math.PI, true);
  ctx.fillStyle = '#050505';
  ctx.fill('evenodd');
  ctx.restore();
}
