"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, ApiError, type Job } from "@/lib/api";
import { Notice, Skeleton } from "./ui";

export const JOB_STATUS_ES: Record<Job["status"], string> = { draft: "Borrador", queued: "En cola", running: "Procesando", succeeded: "Completado", failed: "Falló", cancelled: "Cancelado" };
const TONE: Record<Job["status"], string> = { draft: "text-ink-dim", queued: "text-mb-blue", running: "text-mb-yellow", succeeded: "text-mb-green", failed: "text-mb-red", cancelled: "text-ink-faint" };

export function JobsList({ limit }: { limit?: number }) {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [err, setErr] = useState<ApiError | null>(null);
  useEffect(() => { api.jobs().then((p) => setJobs(p.items)).catch((e) => setErr(e as ApiError)); }, []);
  if (err) return <Notice tone="error" title="No se pudo cargar el historial">{err.message}{err.requestId && <> · ID {err.requestId}</>}</Notice>;
  if (!jobs) return <div className="space-y-3" aria-busy="true" aria-label="Cargando historial"><Skeleton className="h-16" /><Skeleton className="h-16" /></div>;
  if (jobs.length === 0) return (
    <div className="card p-8 text-center">
      <p className="font-display text-lg">Aún no hay trabajos</p>
      <p className="mx-auto mt-1 max-w-md text-sm text-ink-dim">La creación de trabajos está deshabilitada en este entorno. Puedes analizar un PDF y ver su cotización sin crear ningún trabajo.</p>
      <Link href="/studio/new" className="btn-primary mt-5">Nuevo análisis</Link>
    </div>
  );
  return (
    <ul className="divide-y divide-canvas-line rounded-2xl border border-canvas-line bg-canvas-2/60">
      {jobs.slice(0, limit).map((j) => (
        <li key={j.id}>
          <Link href={`/studio/jobs/${j.id}`} className="focus-ring flex flex-wrap items-center justify-between gap-3 rounded-2xl px-5 py-4 hover:bg-canvas-3">
            <div><p className="font-medium">{j.kind === "solution_video" ? "Video de solución" : "Lección híbrida"}</p><p className="font-mono text-xs text-ink-faint">{j.id.slice(0, 8)} · {new Date(j.created_at).toLocaleString("es-CO")}</p></div>
            <span className={`text-sm font-medium ${TONE[j.status]}`}>{JOB_STATUS_ES[j.status]} · {j.progress_pct}%</span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
