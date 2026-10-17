// The clip registry: every clip is { id, title, principles, build(character, params) -> instance }.
// An instance exposes { duration, poseAt(t), phases, impulses, events, ... } and works on any character
// whose profile provides the proportions it reads (retargeting).
import { chaplinWalk, hatTip, hatFlip, doffBow, cornerHop } from './chaplin.js';
import { assemble } from './assemble.js';
import { skullThrow } from './throws.js';
import { jump, pirouette } from './actions.js';
import { sling } from './sling.js';

const def = (id, title, build, extra = {}) => ({ id, title, build, ...extra });
export const CLIPS = {
  assemble: def('assemble', 'Armado desde el piso', assemble, { principles: ['anticipación', 'arcos balísticos', 'escalonamiento', 'acción secundaria'] }),
  hatTip: def('hatTip', 'Saludo con el sombrero', hatTip, { principles: ['anticipación', 'acción superpuesta', 'estirar y encoger'] }),
  skullDrop: def('skullDrop', 'Soltar desde el reposo', (c, p) => skullThrow(c, { ...p, mode: 'drop' }), { principles: ['caída libre exacta', 'atrapar amortiguando'] }),
  skullToss: def('skullToss', 'Lanzamiento hacia arriba', (c, p) => skullThrow(c, { ...p, mode: 'under' }), { principles: ['cadena cinética', 'anticipación', 'velocidad exacta al soltar'] }),
  skullSlam: def('skullSlam', 'Lanzamiento hacia abajo', (c, p) => skullThrow(c, { ...p, mode: 'over' }), { principles: ['cadena cinética', 'rebote con restitución', 'atrapar en el ápice'] }),
  jump: def('jump', 'Salto vertical', jump, { principles: ['anticipación', 'vuelo balístico exacto', 'amortiguación', 'acción superpuesta'] }),
  pirouette: def('pirouette', 'Giro: momento angular', pirouette, { principles: ['conservación de L = I ω', 'anticipación', 'equilibrio sobre un pie'] }),
  hatFlip: def('hatFlip', 'Sombrero al aire', hatFlip, { principles: ['anticipación', 'giro libre constante', 'parábola exacta', 'estirar y encoger'] }),
  doffBow: def('doffBow', 'Reverencia', doffBow, { principles: ['anticipación', 'equilibrio', 'acción superpuesta', 'arcos'] }),
  sling: def('sling', 'Honda con su propio brazo', sling, { principles: ['anticipación (tirones)', 'péndulo', 'v = ω R exacta', 'atrapar en un arco'] }),
  cornerHop: def('cornerHop', 'Giro en un pie', cornerHop, { principles: ['la cabeza guía el giro', 'saltos balísticos', 'equilibrio'] }),
  chaplinWalk: def('chaplinWalk', 'Caminata a lo Chaplin', chaplinWalk, { principles: ['arcos', 'acción superpuesta', 'exageración', 'contactos exactos'] }),
};
