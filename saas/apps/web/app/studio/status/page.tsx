"use client";
import { useStudio } from "@/components/StudioProvider";
import { StatusBadge } from "@/components/StatusBadge";
import { PageTitle } from "@/components/ui";
import { CAPABILITIES } from "@/lib/capabilities";

export default function Status() {
  const { calls, health } = useStudio();
  return (
    <>
      <PageTitle title="Estado del sistema" sub="Registro honesto de lo implementado, simulado y bloqueado, más las llamadas reales que ha hecho esta sesión del navegador." />
      <ul className="grid gap-3 md:grid-cols-2">
        {CAPABILITIES.map((c) => (
          <li key={c.id} className="card p-4"><div className="flex items-start justify-between gap-3"><h2 className="font-medium">{c.name}</h2><StatusBadge status={c.status} /></div><p className="mt-2 text-sm text-ink-dim">{c.detail}</p></li>
        ))}
      </ul>
      <h2 className="mb-3 mt-10 font-display text-xl font-semibold">Llamadas reales de esta sesión <span className="text-sm font-normal text-ink-faint">(API {health})</span></h2>
      <div className="overflow-x-auto rounded-2xl border border-canvas-line">
        <table className="w-full text-left text-xs">
          <caption className="sr-only">Llamadas HTTP realizadas por el navegador</caption>
          <thead className="bg-canvas-2 text-ink-faint"><tr><th scope="col" className="px-3 py-2">Hora</th><th scope="col" className="px-3 py-2">Método</th><th scope="col" className="px-3 py-2">Ruta</th><th scope="col" className="px-3 py-2">HTTP</th><th scope="col" className="px-3 py-2">ms</th></tr></thead>
          <tbody className="font-mono">
            {calls.length === 0 && <tr><td colSpan={5} className="px-3 py-4 text-ink-faint">Sin llamadas todavía.</td></tr>}
            {calls.map((c, i) => (<tr key={i} className="border-t border-canvas-line"><td className="px-3 py-2">{new Date(c.at).toLocaleTimeString("es-CO")}</td><td className="px-3 py-2">{c.method}</td><td className="max-w-[18rem] truncate px-3 py-2">{c.path}</td><td className={`px-3 py-2 ${c.status >= 400 || c.status === 0 ? "text-mb-red" : "text-mb-green"}`}>{c.status || "ERR"}</td><td className="px-3 py-2">{c.ms}</td></tr>))}
          </tbody>
        </table>
      </div>
    </>
  );
}
