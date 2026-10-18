import type { CapStatus } from "@/lib/capabilities";

const MAP: Record<CapStatus, { label: string; cls: string }> = {
  real: { label: "Real", cls: "border-mb-green/40 bg-mb-green/10 text-mb-green" },
  demo: { label: "Entorno de demostración", cls: "border-mb-yellow/40 bg-mb-yellow/10 text-mb-yellow" },
  pending: { label: "Pendiente", cls: "border-mb-blue/40 bg-mb-blue/10 text-mb-blue" },
  blocked: { label: "No disponible", cls: "border-mb-red/40 bg-mb-red/10 text-mb-red" },
};
export function StatusBadge({ status, label }: { status: CapStatus; label?: string }) {
  const m = MAP[status];
  return <span className={`chip ${m.cls}`}><span aria-hidden="true">●</span>{label ?? m.label}</span>;
}
