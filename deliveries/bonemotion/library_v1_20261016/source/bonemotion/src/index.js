// bonemotion — public API
export * as curves from './core/curves.js';
export * as principles from './core/principles.js';
export * as physics from './core/physics.js';
export * as body from './core/body.js';
export * as pose from './core/pose.js';
export { CLIPS } from './clips/index.js';
export { gait, WALK_STYLES } from './clips/locomotion.js';
export { createMrBones } from './characters/mrbones/index.js';
export { createMannequin } from './characters/mannequin/index.js';
export { makeMLP, inbetween, hermiteBaseline } from './neural/inbetween.js';
export { poseToAbs, absToPose, unwrapSeq } from './neural/features.js';
