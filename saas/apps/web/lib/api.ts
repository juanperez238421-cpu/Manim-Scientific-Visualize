import type { components } from "./api-types";
import { API_URL } from "./config";
import { getToken, clearToken } from "./auth";

type S = components["schemas"];
/** El OpenAPI declara `limits` como objeto abierto; aquí se tipa con los campos que /v1/me devuelve realmente. */
export type Limits = { max_pdf_pages: number; max_pdf_bytes: number; max_video_seconds: number; max_concurrent_jobs: number; max_resolution: string; monthly_credits: number };
export type User = Omit<S["User"], "limits"> & { limits: Limits };
export type RenderOptions = S["RenderOptions"];
export type Balance = S["CreditsBalance"];
export type Job = S["Job"];
export type JobPage = S["JobPage"];
export type JobConfig = S["JobConfig"];
export type JobEstimate = S["JobEstimate"];
export type UploadComplete = S["UploadCompleteResponse"];
export type LedgerPage = S["LedgerPage"];

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string, public requestId?: string) {
    super(message);
  }
}

/** Registro de operaciones reales realizadas contra el backend (evidencia visible en la UI). */
export type CallRecord = { at: string; method: string; path: string; status: number; ms: number };
const listeners = new Set<(r: CallRecord) => void>();
export const onCall = (fn: (r: CallRecord) => void) => { listeners.add(fn); return () => { listeners.delete(fn); }; };
const emit = (r: CallRecord) => listeners.forEach((l) => l(r));

async function req<T>(method: string, path: string, opts: { body?: unknown; headers?: Record<string, string> } = {}): Promise<T> {
  const t0 = performance.now();
  let res: Response;
  try {
    const token = await getToken();
    res = await fetch(`${API_URL}${path}`, {
      method,
      headers: { Authorization: `Bearer ${token}`, ...(opts.body ? { "Content-Type": "application/json" } : {}), ...opts.headers },
      body: opts.body ? JSON.stringify(opts.body) : undefined,
      cache: "no-store",
    });
  } catch (e) {
    emit({ at: new Date().toISOString(), method, path, status: 0, ms: Math.round(performance.now() - t0) });
    throw new ApiError(0, "network_error", "No se pudo conectar con la API. ¿Está en ejecución?");
  }
  emit({ at: new Date().toISOString(), method, path, status: res.status, ms: Math.round(performance.now() - t0) });
  if (res.status === 401) clearToken();
  if (!res.ok) {
    let b: Partial<S["ApiErrorBody"]> = {};
    try { b = await res.json(); } catch { /* cuerpo no JSON */ }
    throw new ApiError(res.status, b.code ?? `http_${res.status}`, b.message ?? res.statusText, b.request_id);
  }
  return (await res.json()) as T;
}

export const api = {
  health: async () => { const r = await fetch(`${API_URL}/healthz`, { cache: "no-store" }); if (!r.ok) throw new ApiError(r.status, "unhealthy", "API no saludable"); return r.json(); },
  me: () => req<User>("GET", "/v1/me"),
  renderOptions: () => req<RenderOptions>("GET", "/v1/render-options"),
  balance: () => req<Balance>("GET", "/v1/credits/balance"),
  ledger: () => req<LedgerPage>("GET", "/v1/credits/ledger"),
  jobs: () => req<JobPage>("GET", "/v1/jobs"),
  job: (id: string) => req<Job>("GET", `/v1/jobs/${id}`),
  cancel: (id: string) => req<Job>("POST", `/v1/jobs/${id}/cancel`),
  assets: (id: string) => req<S["JobAssets"]>("GET", `/v1/jobs/${id}/assets`),
  estimate: (pdf_file_id: string, kind: "solution_video" | "hybrid_lesson", config: JobConfig) =>
    req<JobEstimate>("POST", "/v1/jobs/estimate", { body: { pdf_file_id, kind, config } }),
  /** Solo se invoca si el flag y el saldo lo permiten (ver Studio). Requiere Idempotency-Key. */
  createJob: (estimate_id: string, estimate_hash: string, max_authorized_credits: number, idem: string) =>
    req<Job>("POST", "/v1/jobs", { body: { estimate_id, estimate_hash, max_authorized_credits }, headers: { "Idempotency-Key": idem } }),

  /** Protocolo de carga real: init → PUT firmado → complete. */
  async uploadPdf(file: File, sha256: string): Promise<UploadComplete> {
    const init = await req<S["UploadInitResponse"]>("POST", "/v1/uploads/init", { body: { filename: file.name, size_bytes: file.size, sha256 } });
    const t0 = performance.now();
    const put = await fetch(init.upload_url, { method: "PUT", headers: init.headers, body: file });
    emit({ at: new Date().toISOString(), method: "PUT", path: "(URL firmada de almacenamiento)", status: put.status, ms: Math.round(performance.now() - t0) });
    if (!put.ok) throw new ApiError(put.status, "upload_failed", "El almacenamiento rechazó la carga del PDF.");
    return req<UploadComplete>("POST", `/v1/uploads/${init.file_id}/complete`);
  },
};

export async function sha256Hex(file: File): Promise<string> {
  const buf = await file.arrayBuffer();
  const h = await crypto.subtle.digest("SHA-256", buf);
  return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
