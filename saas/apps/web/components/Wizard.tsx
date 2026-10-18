"use client";
import Link from "next/link";
import { useCallback, useMemo, useRef, useState } from "react";
import { api, ApiError, sha256Hex, type JobEstimate, type UploadComplete } from "@/lib/api";
import { JOB_CREATION_FLAG } from "@/lib/config";
import type { PreflightEnvelope, PreflightExercise } from "@/lib/preflight-types";
import { BAND_TITLES, experienceLabel, offerLabel, pickByExperience } from "@/lib/format";
import { useStudio } from "./StudioProvider";
import { Band, Notice, PageTitle } from "./ui";
import { StatusBadge } from "./StatusBadge";

type Op = { id: string; label: string; state: "executed" | "failed" | "skipped" | "blocked"; note: string };
type Phase = "idle" | "working" | "ready" | "error";

async function runPreflight(file: File, select?: string): Promise<PreflightEnvelope> {
  const fd = new FormData(); fd.append("file", file); if (select) fd.append("select", select);
  const r = await fetch("/api/preflight", { method: "POST", body: fd });
  const b = await r.json();
  if (!r.ok) throw new ApiError(r.status, b.code ?? "preflight_failed", b.message ?? "Error del análisis");
  return b as PreflightEnvelope;
}

export function Wizard() {
  const { me, options, refresh } = useStudio();
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [phase, setPhase] = useState<Phase>("idle");
  const [error, setError] = useState<string | null>(null);
  const [drag, setDrag] = useState(false);
  const [upload, setUpload] = useState<UploadComplete | null>(null);
  const [pre, setPre] = useState<PreflightEnvelope | null>(null);
  const [preMsg, setPreMsg] = useState<string | null>(null);
  const [ops, setOps] = useState<Op[]>([]);
  const [sel, setSel] = useState<Set<string>>(new Set());
  const [kind, setKind] = useState<"solution_video" | "hybrid_lesson">("solution_video");
  const [detail, setDetail] = useState("standard");
  const [res, setRes] = useState("720p");
  const [secs, setSecs] = useState(60);
  const [estimate, setEstimate] = useState<JobEstimate | null>(null);
  const [quote, setQuote] = useState<PreflightEnvelope | null>(null);
  const [quoting, setQuoting] = useState(false);
  const [authorized, setAuthorized] = useState(false);

  const addOp = (o: Op) => setOps((p) => [...p.filter((x) => x.id !== o.id), o]);
  const invalidateQuotes = () => { setEstimate(null); setQuote(null); setAuthorized(false); };

  const analyze = useCallback(async (f: File) => {
    setError(null); setPhase("working"); setUpload(null); setPre(null); setPreMsg(null); setOps([]); setSel(new Set()); invalidateQuotes();
    // 1) Validación local (no sustituye la del servidor)
    const head = new Uint8Array(await f.slice(0, 5).arrayBuffer());
    const magic = String.fromCharCode(...head);
    if (!/\.pdf$/i.test(f.name) || magic !== "%PDF-") { setError("El archivo no parece un PDF válido (cabecera %PDF- ausente)."); addOp({ id: "local", label: "Validación local", state: "failed", note: "Cabecera inválida" }); setPhase("error"); return; }
    if (me && f.size > me.limits.max_pdf_bytes) { setError(`El PDF pesa ${(f.size / 1048576).toFixed(1)} MB y tu plan permite ${(me.limits.max_pdf_bytes / 1048576).toFixed(0)} MB.`); addOp({ id: "local", label: "Validación local", state: "failed", note: "Excede el tamaño del plan" }); setPhase("error"); return; }
    addOp({ id: "local", label: "Validación local (tipo, cabecera, tamaño)", state: "executed", note: `${f.name} · ${(f.size / 1024).toFixed(1)} KB` });

    // 2) Carga real al backend (init → PUT → complete)
    try {
      const sha = await sha256Hex(f);
      addOp({ id: "sha", label: "SHA-256 en el navegador", state: "executed", note: sha.slice(0, 16) + "…" });
      const up = await api.uploadPdf(f, sha);
      setUpload(up);
      addOp({ id: "upload", label: "Carga y validación en el backend", state: "executed", note: `status=${up.status} · ${up.page_count} pág.` });
    } catch (e) {
      const m = e instanceof ApiError ? `${e.message}${e.requestId ? ` (ID ${e.requestId})` : ""}` : String(e);
      setError(m); addOp({ id: "upload", label: "Carga y validación en el backend", state: "failed", note: m }); setPhase("error"); return;
    }

    // 3) Preanálisis SDI. El backend NO lo expone todavía: se usa el analizador local real (si está habilitado).
    addOp({ id: "analysis-endpoint", label: "Consulta del análisis persistido (GET /v1/uploads/{id}/analysis)", state: "blocked", note: "El endpoint no existe aún (M3-D). No se inventa." });
    try {
      const p = await runPreflight(f);
      setPre(p);
      addOp({ id: "sdi", label: "Preanálisis con el analizador SDI local", state: "executed", note: `${p.report.exercises.length} ejercicios · estado ${p.report.status}${p.cached ? " · desde caché" : ""}` });
    } catch (e) {
      const m = e instanceof ApiError ? e.message : String(e);
      setPreMsg(m); addOp({ id: "sdi", label: "Preanálisis con el analizador SDI local", state: e instanceof ApiError && e.status === 501 ? "skipped" : "failed", note: m });
    }
    setPhase("ready"); void refresh();
  }, [me, refresh]);

  const pick = (f: File | undefined | null) => { if (f) { setFile(f); void analyze(f); } };
  const toggle = (id: string) => { setSel((p) => { const n = new Set(p); n.has(id) ? n.delete(id) : n.add(id); return n; }); invalidateQuotes(); };

  const selected = useMemo(() => (pre?.report.exercises ?? []).filter((e) => sel.has(e.id)), [pre, sel]);
  const planAllowsPrologue = options?.kinds.find((k) => k.kind === kind)?.prologue_allowed ?? false;

  async function computeQuote() {
    if (!upload || !file) return;
    setQuoting(true); setError(null); setAuthorized(false);
    try {
      const est = await api.estimate(upload.file_id, kind, { language: "es", detail_level: detail, target_seconds: secs, resolution: res, include_prologue: false });
      setEstimate(est); addOp({ id: "estimate", label: "Estimación del backend (POST /v1/jobs/estimate)", state: "executed", note: `${est.estimated_credits} créditos (máx. ${est.max_credits}) · sin cobro` });
    } catch (e) {
      const m = e instanceof ApiError ? `${e.message}${e.requestId ? ` (ID ${e.requestId})` : ""}` : String(e);
      setError(m); addOp({ id: "estimate", label: "Estimación del backend", state: "failed", note: m });
    }
    if (pre && sel.size > 0) {
      try {
        const q = await runPreflight(file, [...sel].join(","));
        setQuote(q); addOp({ id: "sdi-quote", label: "Cotización SDI de la selección (no vinculante)", state: "executed", note: `${sel.size} ejercicio(s)` });
      } catch (e) { addOp({ id: "sdi-quote", label: "Cotización SDI de la selección", state: "failed", note: e instanceof Error ? e.message : String(e) }); }
    }
    setQuoting(false);
  }

  async function createJob() {
    if (!estimate) return;
    try {
      const j = await api.createJob(estimate.estimate_id, estimate.estimate_hash, estimate.max_credits, crypto.randomUUID());
      addOp({ id: "job", label: "Creación de trabajo", state: "executed", note: `job ${j.id.slice(0, 8)} · ${j.status}` });
      window.location.href = `/studio/jobs/${j.id}`;
    } catch (e) { const m = e instanceof ApiError ? `${e.code}: ${e.message}` : String(e); setError(m); addOp({ id: "job", label: "Creación de trabajo", state: "failed", note: m }); }
  }

  const blockers: string[] = [];
  if (!JOB_CREATION_FLAG) blockers.push("El flag NEXT_PUBLIC_ENABLE_JOB_CREATION no está activo en este entorno.");
  if (!estimate) blockers.push("Calcula primero la cotización del backend.");
  else if (!estimate.sufficient_credits) blockers.push(`Saldo insuficiente: necesitas hasta ${estimate.max_credits} créditos y tienes ${estimate.available_credits}.`);
  blockers.push("No hay un worker de render verificado desde esta interfaz (M2 se prueba por separado).");
  const canCreate = JOB_CREATION_FLAG && !!estimate?.sufficient_credits && authorized;

  return (
    <>
      <PageTitle title="Nuevo análisis" sub="Sube un PDF, revisa los ejercicios detectados y obtén una cotización antes de autorizar nada. Subir y analizar no consume créditos." />

      <section aria-labelledby="s-upload" className="mb-10">
        <h2 id="s-upload" className="mb-3 font-display text-xl font-semibold">1 · Carga del PDF</h2>
        <label onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)} onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]); }}
          className={`focus-within:ring-2 focus-within:ring-mb-blue flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-10 text-center transition ${drag ? "border-mb-blue bg-mb-blue/10" : "border-canvas-line bg-canvas-2/60 hover:border-mb-blue/50"}`}>
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#58C4DD" strokeWidth="1.5" aria-hidden="true"><path d="M12 16V4m0 0L7 9m5-5l5 5M4 16v3a1 1 0 001 1h14a1 1 0 001-1v-3" strokeLinecap="round" strokeLinejoin="round" /></svg>
          <span className="mt-3 font-medium">{file ? file.name : "Arrastra un PDF o haz clic para elegirlo"}</span>
          <span className="mt-1 text-xs text-ink-faint">Solo PDF{me ? ` · hasta ${(me.limits.max_pdf_bytes / 1048576).toFixed(0)} MB y ${me.limits.max_pdf_pages} páginas en tu plan` : ""}</span>
          <input ref={inputRef} data-testid="pdf-input" type="file" accept="application/pdf,.pdf" className="sr-only" onChange={(e) => pick(e.target.files?.[0])} />
        </label>
        {phase === "working" && <p role="status" className="mt-3 text-sm text-mb-blue" aria-live="polite">Validando, subiendo y analizando…</p>}
        {error && <div className="mt-3"><Notice tone="error" title="No se pudo completar el paso">{error}</Notice></div>}
      </section>

      {ops.length > 0 && (
        <section aria-labelledby="s-ops" className="mb-10">
          <h2 id="s-ops" className="mb-3 font-display text-xl font-semibold">Evidencia: qué ejecutó realmente cada capa</h2>
          <ul className="space-y-2">
            {ops.map((o) => (
              <li key={o.id} className="card flex flex-wrap items-center justify-between gap-2 px-4 py-3 text-sm">
                <span>{o.label}<span className="block text-xs text-ink-faint">{o.note}</span></span>
                <StatusBadge status={o.state === "executed" ? "real" : o.state === "blocked" ? "blocked" : o.state === "skipped" ? "pending" : "blocked"} label={{ executed: "Ejecutado", failed: "Falló", skipped: "No ejecutado", blocked: "Bloqueado" }[o.state]} />
              </li>
            ))}
          </ul>
        </section>
      )}

      {upload && (
        <section aria-labelledby="s-sum" className="mb-10">
          <h2 id="s-sum" className="mb-3 font-display text-xl font-semibold">2 · Resumen del documento</h2>
          <dl className="grid gap-3 sm:grid-cols-4">
            {[["Estado (backend)", upload.status], ["Páginas", String(upload.page_count)], ["Capa de texto", upload.has_text_layer ? "Sí" : "No"], ["OCR requerido", upload.ocr_required ? "Sí" : "No"]].map(([k, v]) => (
              <div key={k} className="card p-4"><dt className="text-xs uppercase tracking-wide text-ink-faint">{k}</dt><dd className="mt-1 text-lg font-semibold">{v}</dd></div>
            ))}
          </dl>
          <p className="mt-2 break-all font-mono text-[11px] text-ink-faint">SHA-256 {upload.sha256}</p>
          {pre && (
            <div className="mt-4 space-y-3">
              <Notice tone={pre.report.status === "ready" ? "ok" : "warn"} title={`Preanálisis SDI: ${pre.report.status} · ${pre.report.estimate_status}`}>
                Analizador local <span className="font-mono text-xs">{pre.report.tool.analysis_version}</span> · backend <span className="font-mono text-xs">{pre.report.tool.backend}</span>{pre.report.tool.degraded && " (degradado, sin geometría)"} · dificultad máx. {pre.report.difficulty_aggregate.max}, mediana {pre.report.difficulty_aggregate.median}.
                {pre.report.warnings.map((w) => (<span key={w.code} className="mt-1 block text-xs">⚠ {w.message}</span>))}
              </Notice>
              <details className="text-xs text-ink-faint"><summary className="focus-ring cursor-pointer rounded underline">Incertidumbres declaradas por el analizador</summary><ul className="mt-2 list-disc space-y-1 pl-5">{pre.report.uncertainty.map((u) => <li key={u}>{u}</li>)}</ul></details>
              <p className="text-xs text-ink-faint">Origen: analizador local (no persistido en el backend). Esta vista es un <strong>entorno de demostración</strong> hasta que exista GET /v1/uploads/{"{id}"}/analysis.</p>
            </div>
          )}
          {!pre && preMsg && <div className="mt-4"><Notice tone="warn" title="Lista de ejercicios no disponible">El análisis de ejercicios no está habilitado en este entorno ({preMsg}). La carga y validación del backend sí funcionaron.</Notice></div>}
        </section>
      )}

      {pre && (
        <section aria-labelledby="s-ex" className="mb-10">
          <h2 id="s-ex" className="mb-1 font-display text-xl font-semibold">3 · Ejercicios detectados ({pre.report.exercises.length})</h2>
          <p className="mb-4 text-sm text-ink-dim">Elige los ejercicios que quieres convertir en video. Las bandas son heurísticas provisionales, no calibradas.</p>
          <fieldset>
            <legend className="sr-only">Ejercicios disponibles</legend>
            <ul className="space-y-2">
              {pre.report.exercises.map((e: PreflightExercise) => (
                <li key={e.id}>
                  <label className={`card flex cursor-pointer gap-3 p-4 transition focus-within:ring-2 focus-within:ring-mb-blue ${sel.has(e.id) ? "border-mb-blue bg-mb-blue/5" : "hover:border-mb-blue/40"}`}>
                    <input type="checkbox" className="mt-1 h-5 w-5 accent-[#58C4DD]" checked={sel.has(e.id)} onChange={() => toggle(e.id)} data-testid={`ex-${e.number}`} disabled={!e.selectable} />
                    <span className="min-w-0 flex-1">
                      <span className="flex flex-wrap items-center gap-2"><strong>Ejercicio {e.number}</strong>
                        <Band code={e.difficulty.band} title={BAND_TITLES.D} /><Band code={e.animation.level} title={BAND_TITLES.V} /><Band code={e.extraction.level} title={BAND_TITLES.E} /><Band code={e.verification.level} title={BAND_TITLES.VER} />
                        {e.subitems > 0 && <span className="text-xs text-ink-faint">{e.subitems} sub-ítems</span>}</span>
                      <span className="mt-1 block text-sm text-ink-dim">{e.excerpt.replace(/Answer:.*$/i, "").trim()}</span>
                      {e.risks.length > 0 && <span className="mt-1 block text-xs text-mb-yellow">⚠ {e.risks[0]}</span>}
                    </span>
                  </label>
                </li>
              ))}
            </ul>
          </fieldset>
          <p className="mt-3 text-xs text-ink-faint" aria-live="polite">{sel.size} seleccionado(s). D = dificultad académica · V = complejidad visual · E = extracción · VER = verificación.</p>
        </section>
      )}

      {upload && (
        <section aria-labelledby="s-cfg" className="mb-10">
          <h2 id="s-cfg" className="mb-3 font-display text-xl font-semibold">4 · Configuración del video</h2>
          <div className="card grid gap-4 p-5 sm:grid-cols-2">
            <div><label htmlFor="kind" className="mb-1 block text-sm font-medium">Modo</label>
              <select id="kind" value={kind} onChange={(e) => { setKind(e.target.value as typeof kind); invalidateQuotes(); }} className="focus-ring w-full rounded-lg border border-canvas-line bg-canvas px-3 py-3 text-sm">
                <option value="solution_video">Solución paso a paso (solution_video)</option><option value="hybrid_lesson">Lección híbrida (hybrid_lesson)</option></select></div>
            <div><label htmlFor="detail" className="mb-1 block text-sm font-medium">Nivel de detalle</label>
              <select id="detail" value={detail} onChange={(e) => { setDetail(e.target.value); invalidateQuotes(); }} className="focus-ring w-full rounded-lg border border-canvas-line bg-canvas px-3 py-3 text-sm">{(options?.detail_levels ?? ["standard"]).map((d) => <option key={d}>{d}</option>)}</select></div>
            <div><label htmlFor="res" className="mb-1 block text-sm font-medium">Resolución</label>
              <select id="res" value={res} onChange={(e) => { setRes(e.target.value); invalidateQuotes(); }} className="focus-ring w-full rounded-lg border border-canvas-line bg-canvas px-3 py-3 text-sm">{(options?.resolutions ?? ["720p"]).map((r) => <option key={r}>{r}</option>)}</select></div>
            <div><label htmlFor="secs" className="mb-1 block text-sm font-medium">Duración objetivo: {secs} s</label>
              <input id="secs" type="range" min={options?.target_seconds.min ?? 10} max={options?.target_seconds.max ?? 60} step={5} value={secs} onChange={(e) => { setSecs(Number(e.target.value)); invalidateQuotes(); }} className="focus-ring w-full accent-[#58C4DD]" /></div>
            <div className="sm:col-span-2 text-xs text-ink-faint">Idioma: {options?.languages.join(", ") ?? "es"} · Prólogo three.js: {planAllowsPrologue ? "permitido por tu plan" : "no permitido por tu plan (se omite)"}.</div>
          </div>
        </section>
      )}

      {upload && (
        <section aria-labelledby="s-quote" className="mb-10">
          <h2 id="s-quote" className="mb-1 font-display text-xl font-semibold">5 · Vista previa de créditos</h2>
          <p className="mb-4 text-sm text-ink-dim">No se cobra nada. La estimación del backend crea un registro de cotización (vence en minutos); la cotización SDI es informativa.</p>
          <button className="btn-primary" onClick={() => void computeQuote()} disabled={quoting} data-testid="quote-btn">{quoting ? "Calculando…" : "Calcular cotización"}</button>
          {pre && sel.size === 0 && <p className="mt-2 text-xs text-mb-yellow">Sin ejercicios seleccionados solo se calculará la estimación del backend.</p>}

          {(estimate || quote) && (
            <div className="mt-5 grid gap-4 lg:grid-cols-2">
              {estimate && (
                <article className="card p-5" data-testid="backend-estimate"><div className="flex items-start justify-between gap-2"><h3 className="font-display text-lg font-semibold">Estimación del backend</h3><StatusBadge status="real" label="Backend real" /></div>
                  <p className="mt-3 text-3xl font-semibold">{estimate.estimated_credits} <span className="text-sm font-normal text-ink-faint">créditos · máx. autorizable {estimate.max_credits}</span></p>
                  <dl className="mt-3 space-y-1 text-sm text-ink-dim">
                    <div className="flex justify-between"><dt>Duración estimada</dt><dd>{estimate.estimated_seconds} s</dd></div>
                    {Object.entries((estimate.breakdown as { credits_by_engine?: Record<string, number> }).credits_by_engine ?? {}).map(([k, v]) => (<div key={k} className="flex justify-between"><dt>Créditos · motor {k}</dt><dd>{v}</dd></div>))}
                    <div className="flex justify-between"><dt>Multiplicador de resolución</dt><dd>×{String((estimate.breakdown as { resolution_multiplier?: number }).resolution_multiplier ?? "—")}</dd></div>
                    <div className="flex justify-between"><dt>Tu saldo</dt><dd className={estimate.sufficient_credits ? "text-mb-green" : "text-mb-red"}>{estimate.available_credits} {estimate.sufficient_credits ? "(suficiente)" : "(insuficiente)"}</dd></div>
                  </dl>
                  <p className="mt-3 text-xs text-ink-faint">Tarifas {estimate.pricing_version} · borrador no aprobado · vence {new Date(estimate.expires_at).toLocaleTimeString("es-CO")}. No distingue ejercicios seleccionados.</p></article>
              )}
              {quote && (
                <article className="card p-5" data-testid="sdi-quote"><div className="flex items-start justify-between gap-2"><h3 className="font-display text-lg font-semibold">Cotización SDI experimental</h3><StatusBadge status="demo" /></div>
                  <p className="mt-1 text-xs text-ink-faint">Para {selected.map((s) => `#${s.number}`).join(", ")} · analizador local, no vinculante.</p>
                  <ul className="mt-3 space-y-3">
                    {quote.report.workload.credit_previews.map((c) => {
                      const sc = pickByExperience(quote.report.workload.scenes_total as Record<string, number>, c.experience);
                      return (<li key={c.experience} className="rounded-xl border border-canvas-line bg-canvas p-3 text-sm">
                        <p className="font-medium">{experienceLabel(c.experience)}</p>
                        <p className="mt-1 text-2xl font-semibold">{c.estimated_credits} <span className="text-xs font-normal text-ink-faint">créditos · máx. {c.max_credits}</span></p>
                        <p className="text-xs text-ink-dim">{sc ?? "—"} escenas · ≈{c.projected_seconds} s · {c.resolution}</p>
                        <p className="mt-1 text-xs text-mb-yellow">{offerLabel(c.offer_status)}{c.offer_reasons.length ? ` — ${c.offer_reasons.join("; ")}` : ""}</p></li>);
                    })}
                  </ul>
                  <p className="mt-3 text-xs text-ink-faint">Calibración: {quote.report.workload.calibration_status}. Costo interno: {quote.report.workload.cost_chain?.internal_cost?.status ?? "NOT_COMPUTABLE"}. Las cifras son supuestos sin medir.</p></article>
              )}
            </div>
          )}
        </section>
      )}

      {upload && (
        <section aria-labelledby="s-job" className="mb-16">
          <h2 id="s-job" className="mb-3 font-display text-xl font-semibold">6 · Crear trabajo</h2>
          <div className="card p-5">
            {!canCreate && (<div className="mb-4"><Notice tone="warn" title="Creación de trabajos deshabilitada">
              <ul className="mt-1 list-disc space-y-1 pl-5">{blockers.map((b) => <li key={b}>{b}</li>)}</ul></Notice></div>)}
            {JOB_CREATION_FLAG && estimate?.sufficient_credits && (
              <label className="mb-4 flex items-start gap-2 text-sm"><input type="checkbox" className="mt-1 h-5 w-5 accent-[#58C4DD]" checked={authorized} onChange={(e) => setAuthorized(e.target.checked)} />Autorizo reservar hasta {estimate.max_credits} créditos para este trabajo.</label>)}
            <button className="btn-primary" disabled={!canCreate} onClick={() => void createJob()} data-testid="create-job">Crear trabajo</button>
            <p className="mt-3 text-xs text-ink-faint">Hoy no hay cobros reales ni videos generados desde esta interfaz. <Link href="/studio/status" className="underline">Ver estado de capacidades</Link>.</p>
          </div>
        </section>
      )}
    </>
  );
}
