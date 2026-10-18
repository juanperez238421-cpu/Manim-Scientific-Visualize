"use client";
import { JobsList } from "@/components/JobsList";
import { PageTitle } from "@/components/ui";
export default function History() {
  return (<><PageTitle title="Historial de trabajos" sub="Trabajos reales registrados en el backend para tu cuenta." /><JobsList /></>);
}
