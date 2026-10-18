"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "./Logo";
import { StudioProvider, useStudio } from "./StudioProvider";
import { StatusBadge } from "./StatusBadge";
import { authLabel } from "@/lib/auth";

const NAV = [
  { href: "/studio", label: "Panel", exact: true },
  { href: "/studio/new", label: "Nuevo análisis" },
  { href: "/studio/jobs", label: "Historial" },
  { href: "/studio/status", label: "Estado del sistema" },
];

function Header() {
  const { me, balance, health } = useStudio();
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-canvas-line px-4 py-3 sm:px-6">
      <div className="mr-auto flex flex-wrap items-center gap-2">
        <span className="chip border-mb-yellow/40 bg-mb-yellow/10 text-mb-yellow" title={authLabel()}>Entorno de demostración</span>
        <span className={`chip ${health === "up" ? "border-mb-green/40 text-mb-green" : health === "down" ? "border-mb-red/40 text-mb-red" : "border-canvas-line text-ink-faint"}`}>
          API {health === "up" ? "conectada" : health === "down" ? "sin conexión" : "comprobando…"}
        </span>
      </div>
      <div className="flex items-center gap-4 text-sm">
        <span className="text-ink-dim">Plan <strong className="uppercase text-ink">{me?.plan ?? "—"}</strong></span>
        <span className="text-ink-dim">Créditos <strong className="text-ink">{balance ? balance.available : "—"}</strong>{balance && balance.held > 0 && <span className="text-ink-faint"> (+{balance.held} retenidos)</span>}</span>
      </div>
    </div>
  );
}

function Inner({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[232px_1fr]">
      <aside className="border-b border-canvas-line bg-canvas-2/50 lg:sticky lg:top-0 lg:h-screen lg:border-b-0 lg:border-r">
        <div className="flex items-center justify-between px-4 py-3 lg:block lg:px-5 lg:py-6">
          <Link href="/" className="focus-ring rounded-lg" aria-label="AniMotionPDF, volver al inicio"><Logo /></Link>
        </div>
        <nav aria-label="Studio" className="flex gap-1 overflow-x-auto px-3 pb-3 lg:flex-col lg:px-3">
          {NAV.map((n) => {
            const active = n.exact ? path === n.href : path.startsWith(n.href);
            return (<Link key={n.href} href={n.href} aria-current={active ? "page" : undefined}
              className={`focus-ring whitespace-nowrap rounded-lg px-3 py-2.5 text-sm ${active ? "bg-mb-blue/15 font-semibold text-mb-blue" : "text-ink-dim hover:bg-canvas-3 hover:text-ink"}`}>{n.label}</Link>);
          })}
        </nav>
        <div className="hidden px-5 py-4 text-[11px] leading-relaxed text-ink-faint lg:block">
          <StatusBadge status="demo" label="Auth de desarrollo" />
          <p className="mt-2">Sesión simulada con un IdP local; no es Clerk.</p>
        </div>
      </aside>
      <div className="min-w-0"><Header /><main id="main" className="mx-auto max-w-5xl px-4 py-8 sm:px-6">{children}</main></div>
    </div>
  );
}
export function StudioShell({ children }: { children: React.ReactNode }) {
  return <StudioProvider><Inner>{children}</Inner></StudioProvider>;
}
