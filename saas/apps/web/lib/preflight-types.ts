/** Subconjunto tipado de la salida REAL de `python -m document_intelligence analyze` (sdi-analysis-0.2.0). */
export type Band = string; // D1..D7 / V0..V6 / E0..E4 / VER*
export interface PreflightExercise {
  id: string; number: number; label: string; excerpt: string; selectable: boolean; subitems: number;
  difficulty: { band: Band; floor_band?: Band; score: number; calibrated: boolean };
  extraction: { level: Band; math_extraction_confidence: number; reasons: string[] };
  animation: { level: Band; reasons: string[] };
  verification: { level: Band; methods: string[]; answer_key_available: boolean; deterministic_possible: boolean };
  topics: { id: string; label: string; confidence: number; calibrated: boolean; engine_support: string }[];
  risks: string[];
}
export interface CreditPreview {
  experience: "student_tutor" | "teacher_studio"; legacy_kind: "solution_video" | "hybrid_lesson"; resolution: string;
  projected_seconds: number; estimated_credits: number; max_credits: number; offer_status: string; offer_reasons: string[];
  pricing_version: string; non_binding: boolean;
}
export interface PreflightReport {
  status: string; estimate_status: string; reject_reason?: string | null;
  tool: { analysis_version: string; backend: string; degraded: boolean; rubric_version: string; workload_version: string; platform: string };
  pages: { page: number; words: number }[];
  warnings: { code: string; message: string }[]; uncertainty: string[];
  difficulty_aggregate: { max: Band; median: Band };
  exercises: PreflightExercise[];
  workload: {
    selected_exercise_ids: string[]; scenes_total: Record<string, number> | number; projected_video_seconds: Record<string, number> | number;
    credit_previews: CreditPreview[]; calibration_status: string;
    cost_chain?: { internal_cost?: { status: string; missing_inputs?: string[] } };
  };
}
export interface PreflightEnvelope { report: PreflightReport; sha256: string; elapsed_ms: number; cached: boolean; source: "local_sdi_analyzer" }
