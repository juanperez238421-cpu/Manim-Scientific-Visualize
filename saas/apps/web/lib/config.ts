/** Configuración pública. Nada secreto vive aquí. */
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
/** "dev": IdP de desarrollo del repo (NO es Clerk). "clerk": integración real, aún sin implementar en M4. */
export const AUTH_MODE = (process.env.NEXT_PUBLIC_AUTH_MODE ?? "dev") as "dev" | "clerk";
/** El botón «Crear trabajo» solo se habilita si este flag lo permite Y el backend/saldo lo permiten. */
export const JOB_CREATION_FLAG = process.env.NEXT_PUBLIC_ENABLE_JOB_CREATION === "1";
