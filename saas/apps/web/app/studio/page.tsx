"use client";
import Link from "next/link";
import { useStudio } from "@/components/StudioProvider";
import { JobsList } from "@/components/JobsList";
import { Notice, PageTitle, Skeleton, Stat } from "@/components/ui";

export default function Dashboard() {
  const { me, balance, options, error, loading, refresh } = useStudio();
  return (
    <>
      <PageTitle title="Panel" sub="Resumen de tu cuenta y de lo que el backend permite hoy." right={<Link href="/studio/new" className="btn-primary">Nuevo análisis</Link>} />
      {error && (
        <div className="mb-6"><Notice tone="error" title={error.code === "network_error" ? "No hay conexión con la API" : "La API devolvió un error"}>
          {error.message} <button onClick={() => void refresh()} className="focus-ring ml-1 rounded underline">Reintentar</button>
        </Notice></div>
      )}
      {loading && !me ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4" aria-busy="true"><Skeleton className="h-24" /><Skeleton className="h-24" /><Skeleton className="h-24" /><Skeleton className="h-24" /></div>
      ) : me && balance && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Stat label="Plan" value={<span className="uppercase">{me.plan}</span>} />
          <Stat label="Créditos disponibles" value={balance.available} hint={balance.held ? `${balance.held} retenidos por trabajos activos` : "Sin reservas activas"} />
          <Stat label="PDF máximo" value={`${me.limits.max_pdf_pages} págs.`} hint={`${(me.limits.max_pdf_bytes / 1048576).toFixed(0)} MB`} />
          <Stat label="Video máximo" value={`${me.limits.max_video_seconds} s`} hint={`hasta ${me.limits.max_resolution}`} />
        </div>
      )}
      {me && balance && balance.available === 0 && (
        <div className="mt-6"><Notice tone="warn" title="Sin créditos: no se pueden crear trabajos">
          Puedes subir, analizar y cotizar. Para crear un trabajo se necesita saldo, el flag de creación y un worker; hoy no hay cobros ni pasarela de pago.
        </Notice></div>
      )}
      {options && <p className="mt-6 text-xs text-ink-faint">Opciones de render del backend: idioma {options.languages.join(", ")} · resoluciones {options.resolutions.join(", ")} · {options.target_seconds.min}–{options.target_seconds.max} s.</p>}
      <section className="mt-10">
        <h2 className="mb-4 font-display text-xl font-semibold">Trabajos recientes</h2>
        <JobsList limit={5} />
      </section>
    </>
  );
}
