// Mr. Bones' top hat and bow tie, drawn in the period 2-D style from 3-D frames.
// The hat supports squash & stretch (area kept: sx = 1/sqrt(q), sy = q) and foreshortening when it
// tips toward or away from the camera (fore = projected length of its up axis, 0..1).
import { G } from '../../render/ink.js';

export function drawHat(ink, x, y, s = 1, rot = 0, { squash = 1, fore = 1 } = {}) {
  const ctx = ink.ctx;
  const sy = squash * fore, sx = 1 / Math.sqrt(Math.max(0.3, squash));
  ctx.save();
  ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * sx, s * sy);
  // when strongly foreshortened, show the brim as an ellipse (we look at it from above/below)
  const brimH = 10 + (1 - fore) * 26 / Math.max(0.3, sy);
  ink.shape([[-42, 2], [42, 2], [40, 2 - brimH], [-40, 2 - brimH]], { fill: G.black });
  ink.shape([[-26, -6], [-24, -62], [24, -62], [26, -6]], { fill: G.black });
  ink.shape([[-25, -14], [25, -14], [25, -24], [-25, -24]], { fill: G.mid, lw: 2 });
  ctx.restore();
}

export function drawBowtie(ink, x, y, S, rot, facing) {
  const ctx = ink.ctx;
  ctx.save();
  ctx.translate(x, y); ctx.rotate(rot); ctx.scale(S * 0.62 * Math.max(0.35, facing), S * 0.62);
  ink.shape([[0, 0], [-18, -10], [-18, 10]], { fill: G.black, lw: 2.5 });
  ink.shape([[0, 0], [18, -10], [18, 10]], { fill: G.black, lw: 2.5 });
  ink.shape([[-12, -3], [-6, 0], [-12, 3]], { fill: G.dusk, ink: null, lw: 0 });
  ink.blob(0, 0, 5, 5, 0, { fill: G.black, lw: 2 });
  ctx.restore();
}
