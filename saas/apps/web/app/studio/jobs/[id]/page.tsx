"use client";
import Link from "next/link";
import { use, useEffect, useState } from "react";
import { api, ApiError, type Job } from "@/lib/api";
import { JOB_STATUS_ES } from "@/components/JobsList";
import { Notice, PageTitle, Skeleton } from "@/components/ui";

export default function JobDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [job, setJob] = useState<Job | null>(null);
  const [err, setErr] = useState<ApiError | null>(null);
  const [video, setVideo] = useState<{ url: string } | null>(null);
  useEffect(() => { api.job(id).then(setJob).catch((e) => setErr(e as ApiError)); }, [id]);
  useEffect(() => { if (job?.status === "succeeded") api.assets(id).then((a) => setVideo({ url: a.video_url })).catch(() => setVideo(null)); }, [job, id]);

  if (err) return (<><PageTitle title="Trabajo" /><Notice tone="error" title={err.status === 404 ? "Trabajo no encontrado" : "No se pudo cargar el trabajo"}>{err.message} <Link href="/studio/jobs" className="underline">Volver al historial</Link></Notice></>);
  if (!job) return <div aria-busy="true"><Skeleton className="h-10 w-1/2" /><Skeleton className="mt-6 h-64" /></div>;
  return (
    <>
      <PageTitle title={job.kind === "solution_video" ? "Video de solución" : "Lección híbrida"} sub={`${JOB_STATUS_ES[job.status]} · ${job.progress_pct}% · ${job.id}`} />
      {job.status === "succeeded" && video ? (
        <div className="card overflow-hidden"><video controls preload="metadata" className="aspect-video w-full bg-black" src={video.url} /><div className="flex items-center justify-between p-4 text-sm"><span className="text-ink-dim">Enlace firmado de corta duración.</span><a href={video.url} download className="btn-primary">Descargar MP4</a></div></div>
      ) : (
        <Notice tone="info" title="Video no disponible todavía">El reproductor aparece solo cuando el trabajo termina con éxito y el backend entrega un MP4 real.</Notice>
      )}
      <h2 className="mb-3 mt-8 font-display text-xl font-semibold">Etapas</h2>
      <ol className="grid gap-2 sm:grid-cols-2">
        {job.stages.map((s) => (<li key={s.stage} className="card flex items-center justify-between px-4 py-3 text-sm"><span className="font-mono">{s.stage}</span><span className="text-ink-dim">{s.status}</span></li>))}
      </ol>
      {job.verification && (
        <p className="mt-6 text-sm text-ink-dim">Verificación: <strong className="text-ink">{job.verification.status ?? "sin dato"}</strong>{job.verification.simulated && " · simulada"} · entrega {job.verification.delivery_ready ? "lista" : "no lista"}.</p>
      )}
    </>
  );
}
