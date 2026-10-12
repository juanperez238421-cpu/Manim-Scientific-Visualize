# Contrato HTTP y decisiones (v0.2) — para validar antes de escribir routers

Estado: **propuesta**. Nada de esto está implementado en FastAPI todavía; `/openapi.json` real
solo existirá cuando existan los endpoints. El borrador del frontend no es fuente de verdad.

## Decisiones adoptadas (de tu handoff)
| Tema | Decisión | Estado |
|---|---|---|
| Repo | `saas/` durante el prototipo; repo comercial aparte en producción | adoptada |
| Objetos | MinIO (dev) / Cloudflare R2 (prod), URLs firmadas, CORS estricto, bucket privado | adoptada |
| Auth | Clerk. FastAPI verifica JWT vía JWKS; identidad = `(auth_provider, provider_subject)`; sin `password_hash`; el email no identifica | adoptada, schema actualizado |
| Pagos | Neutral al proveedor (`payment_provider`, `external_subscription_id`, `payment_customers`). Mercado Pago/Wompi sin decidir. No verifiqué la cobertura de Stripe en Colombia; lo tomo de tu handoff | schema neutral |
| Idioma | `es` inicial; `config.language` publicado en `/v1/render-options` | adoptada |
| Mecanismo de créditos | reserva/liquidación aprobado; **tarifas y planes NO** (`db/seed_plans_DRAFT.sql`) | parcial |

## Contradicciones resueltas
1. **Upload (un solo protocolo)**: `POST /v1/uploads/init {filename,size_bytes,sha256}` → fila `pdf_files(status=pending)` +
   URL PUT presignada (expira); cliente sube a R2; `POST /v1/uploads/{file_id}/complete` → el servidor hace HEAD,
   verifica tamaño, magic `%PDF-`, recalcula SHA-256 (si difiere de `declared_sha256` → `rejected`), cuenta páginas,
   detecta capa de texto/`ocr_required`, aplica límites del plan → `analyzed` o `rejected` (422). `/pdfs` queda descartado.
2. **Estados de job**: exactamente el enum SQL `draft|queued|running|succeeded|failed|cancelled` (UI los traduce).
3. **Etapas**: `GET /v1/jobs/{id}` devuelve `stages[]` (una por `stage_name`, con `status` incl. `skipped`) y
   `scenes: {total, by_status, items[label,engine,status]}`; `current_stage` es solo un atajo y no describe paralelismo.
4. **Tipos**: solo `solution_video` y `hybrid_lesson`. `explain/summarize` son UX y no se mapean solos.
5. **Prólogo**: columna `jobs.include_prologue`. `solution_video` ⇒ siempre `false` (CHECK en BD; su flujo es página→solución→página).
   `hybrid_lesson` ⇒ opcional; si es `false`, la etapa `render_prologue` queda `skipped` y la lección arranca en la pregunta,
   manteniendo el orden del protocolo (solo se acorta, nunca se reordena).
6. **Saldo (definición única)**: `available = SUM(delta)` (ya descuenta reservas); `held` = reservas de jobs queued/running;
   `total = available + held`. La UI muestra `available` y `held` por separado, nunca resta `held` otra vez.
   `GET /v1/credits/balance → {available, held}`.
7. **Reserva sin carreras**: `reserve_credits(job, n)` bloquea la fila del usuario (`FOR UPDATE`), es idempotente por job
   y devuelve `false` → HTTP 402 `insufficient_credits`. Probado: reintento no duplica; saldo insuficiente → false.
   (Pendiente: prueba con conexiones concurrentes reales en los tests de la API.)
8. **Liquidación**: el usuario autoriza `max_credits` (de la estimación) ⇒ `jobs.max_authorized_credits`. `settle_job_credits`
   libera lo no usado, cobra exceso **solo hasta ese tope**, y un fallo técnico (`actual=0`) libera todo. Idempotente.
9. **Free realizable**: con pesos svg 0,5 / manim 1,0 / threejs 2,5, un prólogo de 30 s = 75 > 30 créditos de Free.
   Propuesta (sin aprobar): **Free sin prólogo three.js**, máx. 60 s, 720p; el prólogo desde Starter o como add-on.
   No se anuncia "primer video gratis" hasta medir costos y demostrar un caso completo dentro del presupuesto Free.
10. **Chatbot**: crea jobs por el mismo `POST /v1/jobs` que la UI, con `estimate_id` + `max_credits` aceptado por el usuario
    en un turno de confirmación explícito, y `Idempotency-Key` por acción.

## Endpoints (a confirmar)
| Método | Ruta | Notas |
|---|---|---|
| GET | `/v1/me` | usuario + plan + límites |
| GET | `/v1/render-options` | idiomas, resolución, kinds, prólogo permitido por plan (la UI no hardcodea) |
| POST | `/v1/uploads/init` · `/v1/uploads/{file_id}/complete` | ver (1) |
| POST | `/v1/jobs/estimate` | crea `job_estimates` (con `expires_at`, `breakdown`, `max_credits`) |
| POST | `/v1/jobs` | `Idempotency-Key` obligatorio; body `{estimate_id, max_authorized_credits}`; 201 / 402 / 409 |
| GET | `/v1/jobs`, `/v1/jobs/{id}` | solo del dueño (404 si ajeno) |
| POST | `/v1/jobs/{id}/cancel` | **añadido**: libera la reserva (existe el estado `cancelled`) |
| GET | `/v1/jobs/{id}/assets` | URL firmada corta; 409 si no `succeeded` |
| GET | `/v1/credits/balance`, `/v1/credits/ledger` | paginación por cursor |

Errores: `{code, message, request_id, details?}`. `402 insufficient_credits`, `409 idempotency_conflict | estimate_expired | job_not_ready`,
`422 invalid_pdf`, `404` para recursos ajenos. Idempotency-Key: misma clave+mismo cuerpo ⇒ misma respuesta; misma clave
con cuerpo distinto ⇒ 409.

## Pendiente de ti antes del código FastAPI
- Confirmar o corregir los puntos 1–10 y la lista de endpoints (en especial `/cancel`).
- Tarifas: para calibrar los pesos necesito una medición real de render, o sea el link de tu librería Manim (que tú autorices).
