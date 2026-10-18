import type { ReactNode } from "react";

export function PageTitle({ title, sub, right }: { title: string; sub?: string; right?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
      <div><h1 className="h-display text-2xl font-semibold sm:text-3xl">{title}</h1>{sub && <p className="mt-1 max-w-2xl text-sm text-ink-dim">{sub}</p>}</div>
      {right}
    </div>
  );
}
export function Stat({ label, value, hint }: { label: string; value: ReactNode; hint?: string }) {
  return (<div className="card p-4"><p className="text-xs uppercase tracking-wide text-ink-faint">{label}</p><p className="mt-1 text-2xl font-semibold">{value}</p>{hint && <p className="mt-1 text-xs text-ink-faint">{hint}</p>}</div>);
}
export function Notice({ tone, title, children }: { tone: "info" | "warn" | "error" | "ok"; title: string; children?: ReactNode }) {
  const c = { info: "border-mb-blue/40 bg-mb-blue/5", warn: "border-mb-yellow/40 bg-mb-yellow/5", error: "border-mb-red/40 bg-mb-red/5", ok: "border-mb-green/40 bg-mb-green/5" }[tone];
  return (<div role={tone === "error" ? "alert" : "status"} className={`rounded-xl border p-4 text-sm ${c}`}><p className="font-semibold">{title}</p>{children && <div className="mt-1 text-ink-dim">{children}</div>}</div>);
}
export function Skeleton({ className = "" }: { className?: string }) {
  return <div aria-hidden="true" className={`animate-pulse rounded-xl bg-canvas-3 ${className}`} />;
}
export function Band({ code, title }: { code: string; title: string }) {
  return <span title={title} className="inline-flex items-center rounded-md border border-canvas-line bg-canvas px-1.5 py-0.5 font-mono text-[11px] text-ink-dim"><span className="sr-only">{title}: </span>{code}</span>;
}
