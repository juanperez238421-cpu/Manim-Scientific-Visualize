/** Registro honesto de capacidades. La UI lo muestra tal cual; nada se presenta como real si no lo es. */
export type CapStatus = "real" | "demo" | "pending" | "blocked";
export interface Capability { id: string; name: string; status: CapStatus; detail: string }
export const CAPABILITIES: Capability[] = [
  { id: "api-me", name: "Perfil, plan y límites", status: "real", detail: "GET /v1/me contra FastAPI." },
  { id: "api-upload", name: "Carga y validación de PDF", status: "real", detail: "init → PUT firmado → complete (magic %PDF-, SHA-256, páginas, capa de texto)." },
  { id: "api-estimate", name: "Estimación del backend", status: "real", detail: "POST /v1/jobs/estimate (tarifas draft-0.1, no aprobadas). No admite selección de ejercicios." },
  { id: "api-credits", name: "Saldo y libro mayor", status: "real", detail: "GET /v1/credits/balance y /ledger." },
  { id: "api-jobs", name: "Historial y detalle de trabajos", status: "real", detail: "GET /v1/jobs y /v1/jobs/{id}." },
  { id: "sdi", name: "Preanálisis de ejercicios (SDI)", status: "demo", detail: "Analizador local real (M3-B/C). El backend aún no persiste ni sirve el análisis (falta GET /v1/uploads/{id}/analysis, M3-D)." },
  { id: "sdi-quote", name: "Cotización SDI experimental", status: "demo", detail: "Vista previa NO vinculante calculada por el analizador local; no genera estimate_id del backend." },
  { id: "job-create", name: "Creación de trabajos", status: "blocked", detail: "Requiere flag NEXT_PUBLIC_ENABLE_JOB_CREATION=1, saldo suficiente y worker. Hoy: sin créditos y sin cobros reales." },
  { id: "video", name: "Reproductor y descarga de video", status: "pending", detail: "Se activará con trabajos 'succeeded' y GET /v1/jobs/{id}/assets. No hay videos generados todavía." },
  { id: "auth-clerk", name: "Autenticación Clerk", status: "blocked", detail: "Sin claves de desarrollo. Se usa un IdP de desarrollo local que ejercita la misma verificación JWKS." },
  { id: "payments", name: "Pagos y planes", status: "blocked", detail: "Sin pasarela. Planes y precios son borradores provisionales." },
];
