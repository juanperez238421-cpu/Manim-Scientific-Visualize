# AniMotionPDF web (M4) — landing + Studio inicial

Next.js 15 · TypeScript · Tailwind 3. Rama `m4/frontend-studio` (basada en `claude/saas-video-generator-backend-51xzx1`). No modifica M2 ni M3.

## Ejecutar localmente
1. Backend (ver `../api/README.md`): Postgres + `python scripts/migrate.py --seed-dev-plans`, IdP de desarrollo `python scripts/dev_jwks.py 9100`, y
   `uvicorn app.main:create_app --factory --port 8000` con `DATABASE_URL`, `CLERK_JWKS_URL=http://127.0.0.1:9100/jwks.json`, `CLERK_ISSUER=http://127.0.0.1:9100`, `LOCAL_STORAGE_DIR`, `STORAGE_SIGNING_SECRET`, `CORS_ORIGINS=http://127.0.0.1:3000`.
2. Web: `cp .env.example .env.local` (ajusta `SDI_PREFLIGHT_SCRIPT`), `npm install`, `npm run build && npm start` → http://127.0.0.1:3000
3. Tipos: `npm run gen:api` regenera `lib/api-types.ts` desde `../api/openapi.json`.
4. E2E: `CHROMIUM_PATH=<chromium opcional> M4_TEST_PDF=<ruta a 3.pdf> npx playwright test` (necesita web + backend activos).

## Endpoints reales usados
GET /healthz · GET /v1/me · GET /v1/render-options · GET /v1/credits/balance · POST /v1/uploads/init · PUT URL firmada · POST /v1/uploads/{id}/complete · POST /v1/jobs/estimate · GET /v1/jobs · GET /v1/jobs/{id} · GET /v1/jobs/{id}/assets (solo si `succeeded`). `POST /v1/jobs` está implementado en el cliente pero detrás de flag + saldo + autorización explícita.

## Capacidades
Ver `lib/capabilities.ts` (se muestra en /studio/status). Implementado real: carga/validación, estimación, saldo, historial. Demostración: lista de ejercicios y cotización SDI (analizador local, `/api/preflight`, solo dev). Bloqueado: análisis persistido (M3-D), Clerk, pagos, creación de trabajos, video.
