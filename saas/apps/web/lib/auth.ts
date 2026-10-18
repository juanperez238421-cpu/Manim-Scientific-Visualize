import { AUTH_MODE } from "./config";

/**
 * AUTENTICACIÓN DE DESARROLLO (no es Clerk). La ruta /api/dev-token (servidor) pide un JWT RS256 al IdP local
 * del repositorio (saas/apps/api/scripts/dev_jwks.py). La API lo verifica por el MISMO camino JWKS que usará con Clerk.
 * La integración Clerk real queda BLOQUEADA hasta disponer de claves de desarrollo (ver docs/M4_CAPABILITIES.md).
 */
let cached: { token: string; exp: number } | null = null;

export async function getToken(): Promise<string> {
  if (AUTH_MODE === "clerk") throw new Error("Clerk no está configurado en M4 (BLOCKED).");
  if (cached && cached.exp > Date.now() + 30_000) return cached.token;
  const sub = typeof window !== "undefined" ? (sessionStorage.getItem("m4.sub") ?? "user_m4_demo") : "user_m4_demo";
  const r = await fetch(`/api/dev-token?sub=${encodeURIComponent(sub)}`, { cache: "no-store" });
  if (!r.ok) throw new Error("IdP de desarrollo no disponible");
  const { token } = (await r.json()) as { token: string };
  cached = { token, exp: Date.now() + 50 * 60_000 };
  return token;
}
export const clearToken = () => { cached = null; };
export const authLabel = () => (AUTH_MODE === "dev" ? "Entorno de demostración · IdP de desarrollo (no es Clerk)" : "Clerk");
