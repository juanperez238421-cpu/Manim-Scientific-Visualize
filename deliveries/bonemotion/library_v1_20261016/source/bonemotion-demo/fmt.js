// numbers in Spanish notation (decimal comma), never "-0,00"
export function fmt(x, d = 2) {
  const v = Math.abs(x) < 0.5 * 10 ** -d ? 0 : x;
  return v.toFixed(d).replace('.', ',');
}
