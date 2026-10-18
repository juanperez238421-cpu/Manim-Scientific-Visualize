export const OFFER_ES: Record<string, string> = {
  offerable: "Oferta aplicable",
  informational_requires_review: "Informativa · requiere revisión",
  not_offered_exceeds_plan_limits: "No ofrecida · excede límites del plan",
};
export const offerLabel = (s: string) => OFFER_ES[s] ?? (s.startsWith("withheld") ? "Sin cifra (retenida)" : s.startsWith("informational") ? "Informativa" : s);
export const BAND_TITLES = { D: "Dificultad académica", V: "Complejidad visual", E: "Dificultad de extracción", VER: "Nivel de verificación" } as const;
export const experienceLabel = (e: string) => (e === "student_tutor" ? "Solución paso a paso (solution_video)" : "Lección docente (hybrid_lesson)");
export function pickByExperience<T>(v: Record<string, T> | T | undefined, exp: string): T | undefined {
  if (v && typeof v === "object" && !Array.isArray(v) && exp in (v as Record<string, T>)) return (v as Record<string, T>)[exp];
  return typeof v === "number" ? (v as T) : undefined;
}
