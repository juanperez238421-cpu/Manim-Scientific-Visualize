import type { Metadata } from "next";
import { StudioShell } from "@/components/StudioShell";
export const metadata: Metadata = { title: "Studio" };
export default function Layout({ children }: { children: React.ReactNode }) { return <StudioShell>{children}</StudioShell>; }
