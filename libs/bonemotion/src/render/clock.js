// Musical clock + deterministic randomness. Everything in the cartoon is a pure function of t.

export function makeClock(tl) {
  const spb = 60 / tl.music.bpm; // seconds per beat
  const dps = tl.music.drawingsPerSecond; // drawings per second ("on twos" at 24 fps)
  return {
    spb,
    beat: (t) => t / spb,
    t: (b) => b * spb,
    // time at which the current *drawing* was made: characters move on twos
    drawT: (t) => Math.floor(t * dps + 1e-9) / dps,
    drawIndex: (t) => Math.floor(t * dps + 1e-9),
  };
}

export const clamp01 = (u) => (u < 0 ? 0 : u > 1 ? 1 : u);
export const prog = (x, a, b) => clamp01((x - a) / (b - a));
export const lerp = (a, b, u) => a + (b - a) * u;
export const smooth = (u) => u * u * (3 - 2 * u);
export const easeOut = (u) => 1 - (1 - u) ** 3;
export const easeIn = (u) => u * u * u;
export const easeInOut = (u) => (u < 0.5 ? 4 * u * u * u : 1 - (-2 * u + 2) ** 3 / 2);
// overshoot: settles at 1 after a springy bounce (squash-and-stretch arrivals)
export const backOut = (u, s = 2.2) => 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2;
export const elastic = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : 1 - Math.exp(-6 * u) * Math.cos(u * Math.PI * 4.5));

// beat pulse: 1 on the beat, decays across it — used for "everything bounces on the beat"
export const pulse = (b, sharp = 3) => Math.exp(-sharp * (b - Math.floor(b)));
// hop: 0 on each beat, peaks between beats
export const hop = (b) => Math.sin(Math.PI * (b - Math.floor(b)));

export function hash(...xs) {
  let h = 2166136261 >>> 0;
  for (const x of xs) {
    h ^= (Math.floor(x) | 0) >>> 0;
    h = Math.imul(h, 16777619) >>> 0;
    h ^= h >>> 13;
    h = Math.imul(h, 0x5bd1e995) >>> 0;
    h ^= h >>> 15;
  }
  return h >>> 0;
}
export const rnd = (...xs) => hash(...xs) / 4294967296; // [0, 1)
export const srnd = (...xs) => 2 * rnd(...xs) - 1; // [-1, 1)

// smooth 1-D value noise (for gate weave, flicker drift, swaying)
export function vnoise(seed, x) {
  const i = Math.floor(x), f = x - i;
  const a = srnd(seed, i), b = srnd(seed, i + 1);
  return a + (b - a) * smooth(f);
}
