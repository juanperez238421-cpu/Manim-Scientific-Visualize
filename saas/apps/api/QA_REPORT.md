# QA Report — AniMotionPDF API (etapa 1)

Resultado: **64 PASS / 0 FAIL**, repetido 5 veces consecutivas sin intermitencias (~10 s por corrida).
Entorno: Python 3.13, PostgreSQL 16 real (cluster temporal), FastAPI 0.143, psycopg 3.3, pytest 9. Sin Celery, sin Redis, sin pagos,
sin S3 real (FakeStore), sin Supabase. Clerk simulado con un par RSA de prueba (misma lógica de verificación que producción).

Reproducir: `cd saas/apps/api && pip install -e '.[dev]' pytest-timeout && pytest` (requiere binarios de PostgreSQL 16).

## Defectos reales encontrados por las pruebas (ya corregidos)

| # | Hallazgo | Corrección |
|---|---|---|
| 1 | **Deadlock** entre dos `create_queued_job` concurrentes: el `INSERT` del job toma `KEY SHARE` sobre `users` (FK) y luego se pedía `FOR UPDATE` | Bloqueo de usuario `FOR NO KEY UPDATE` en todas las funciones |
| 2 | **Deadlock** en la ruta HTTP: la fila de `idempotency_keys` (FK a `users`) toma `KEY SHARE` antes del bloqueo | Mismo cambio (`FOR NO KEY UPDATE`); verificado con 6–24 hilos |
| 3 | El trigger diferido `jobs_terminal_settled` evaluaba el `NEW` del evento y no el estado final de la transacción | Relee la fila al hacer COMMIT |
| 4 | `UNIQUE(email)` provocaba **500** al iniciar sesión dos identidades con el mismo email | Email deja de ser único; identidad = (provider, sub) |
| 5 | Mi propio test de estrés usaba una barrera de 30 hilos con 24 tareas (se colgaba) | Corregido en el test |
| 6 | Ejemplo Free (30 s + 30 s = 45 créditos, no 30) | Corregido en `seed_plans_DRAFT.sql` (20 s + 20 s = 30) |

## Cobertura de los criterios de aceptación

| Criterio | Pruebas |
|---|---|
| Idempotencia de creación | `test_idempotent_create_same_body_replays`, `test_409_idempotency_conflict…`, `test_failed_attempt_does_not_cache_error…`, `test_api_concurrent_same_idempotency_key_creates_one_job` |
| Idempotencia de reserva / liquidación | `test_reserve_is_max_authorized_and_settle_only_releases`, `test_concurrent_settle_is_idempotent`, `test_platform_failure_refunds…` |
| Idempotencia de cancelación | `test_cancel_queued_is_immediate…`, `test_api_cancel_endpoint_idempotent_and_refunds`, `test_confirm_cancel…` |
| Concurrencia real sobre el mismo saldo | `test_concurrent_jobs_same_balance_no_overspend` (10 hilos, saldo 100, 2 éxitos), `test_api_concurrent_creates_never_overspend`, `test_no_deadlock_under_mixed_reserve_settle_cancel_stress` (24 hilos) |
| Sin saldos negativos ni cobros duplicados | `test_audit_scenario_settle_cannot_make_balance_negative` (escenario 100/40/60/50 del auditor), `test_ledger_trigger_blocks_negative_balance`, `assert_job_accounting` en cada flujo |
| Aislamiento entre usuarios | `test_isolation_between_users`, `test_other_users_upload_is_404`, `test_ownership_enforced_by_composite_foreign_keys` |
| Estimaciones vencidas / ajenas / alteradas | `test_estimate_expired_is_409`, `test_estimate_tampered_hash_or_credits`, `test_estimate_pricing_version_change_is_409`, `test_estimate_second_use_is_409`, aislamiento (404) |
| Fallos de Celery y reintentos | `test_outbox_written_with_reservation_and_publish_failure_is_recoverable`, `test_concurrent_relays_publish_each_job_once`, `test_cancelled_job_is_never_published`, `test_duplicate_delivery_after_publish_is_harmless`, `test_worker_crash_failure_releases_everything` |
| Respuestas para Next.js | `test_generated_openapi_is_valid_complete_and_committed` (OpenAPI 3.1 válido, 12 operaciones, `Idempotency-Key`, errores tipados, enums = SQL), `test_enums_match_sql` |
| 401 / 402 / 404 / 409 / 422 | `test_auth_errors.py` (401 ×4 variantes), `test_402_insufficient_credits…`, `test_error_shape_404_and_422`, `test_job_not_ready…`, `test_uploads_options.py` |
| UI consume opciones publicadas | `test_render_options_published_by_plan`, `test_estimate_validates_against_published_options` |
| Cancelación segura | `test_cancel_running_is_cooperative_no_early_release`, `test_cancel_vs_worker_start_race_is_always_consistent` (20 iteraciones de carrera), `test_api_cancel_running_then_worker_confirms` |

## Resultados por prueba

### `test_auth_errors.py` — 8 PASS

- PASS `test_401_missing_token`
- PASS `test_401_bad_scheme_and_garbage`
- PASS `test_401_wrong_signature`
- PASS `test_401_expired_wrong_issuer_wrong_azp`
- PASS `test_identity_is_sub_not_email`
- PASS `test_me_returns_plan_and_creates_user_once`
- PASS `test_error_shape_404_and_422`
- PASS `test_request_id_is_propagated`

### `test_finance_sql.py` — 25 PASS

- PASS `test_audit_scenario_settle_cannot_make_balance_negative`
- PASS `test_reserve_is_max_authorized_and_settle_only_releases`
- PASS `test_concurrent_jobs_same_balance_no_overspend`
- PASS `test_same_estimate_concurrently_creates_exactly_one_job`
- PASS `test_concurrent_settle_is_idempotent`
- PASS `test_no_deadlock_under_mixed_reserve_settle_cancel_stress`
- PASS `test_ledger_trigger_blocks_negative_balance`
- PASS `test_ledger_is_append_only`
- PASS `test_holds_exclude_settled_jobs`
- PASS `test_platform_failure_refunds_everything_non_platform_charges_consumed`
- PASS `test_invalid_transitions_rejected`
- PASS `test_terminal_job_without_settlement_cannot_commit`
- PASS `test_ownership_enforced_by_composite_foreign_keys`
- PASS `test_solution_video_cannot_have_prologue`
- PASS `test_cancel_queued_is_immediate_full_refund_and_idempotent`
- PASS `test_cancel_running_is_cooperative_no_early_release`
- PASS `test_confirm_cancel_requires_request_and_caps_to_reserve`
- PASS `test_cancel_finished_job_is_rejected`
- PASS `test_cancel_vs_worker_start_race_is_always_consistent`
- PASS `test_api_cancel_endpoint_idempotent_and_refunds`
- PASS `test_api_cancel_running_then_worker_confirms`
- PASS `test_api_cancel_finished_is_409`
- PASS `test_api_concurrent_same_idempotency_key_creates_one_job`
- PASS `test_api_concurrent_creates_never_overspend`
- PASS `test_api_concurrency_limit_race_never_exceeds_plan`

### `test_jobs_api.py` — 16 PASS

- PASS `test_create_job_reserves_max_authorized`
- PASS `test_hybrid_with_prologue_has_active_prologue_stage`
- PASS `test_402_insufficient_credits_and_nothing_persists`
- PASS `test_idempotent_create_same_body_replays`
- PASS `test_409_idempotency_conflict_same_key_different_body`
- PASS `test_idempotency_key_required_and_scoped_per_user`
- PASS `test_failed_attempt_does_not_cache_error_retry_works`
- PASS `test_estimate_second_use_is_409`
- PASS `test_estimate_expired_is_409`
- PASS `test_estimate_tampered_hash_or_credits`
- PASS `test_estimate_pricing_version_change_is_409`
- PASS `test_isolation_between_users`
- PASS `test_job_not_ready_assets_then_ready`
- PASS `test_stage_and_scene_progress_in_job`
- PASS `test_concurrent_job_limit_per_plan`
- PASS `test_pagination_cursor`

### `test_outbox_openapi.py` — 7 PASS

- PASS `test_outbox_written_with_reservation_and_publish_failure_is_recoverable`
- PASS `test_concurrent_relays_publish_each_job_once`
- PASS `test_cancelled_job_is_never_published`
- PASS `test_duplicate_delivery_after_publish_is_harmless`
- PASS `test_worker_crash_failure_releases_everything`
- PASS `test_generated_openapi_is_valid_complete_and_committed`
- PASS `test_enums_match_sql`

### `test_uploads_options.py` — 8 PASS

- PASS `test_upload_happy_path`
- PASS `test_init_returns_signed_put_without_secrets`
- PASS `test_422_invalid_pdfs`
- PASS `test_complete_before_upload_is_409`
- PASS `test_other_users_upload_is_404`
- PASS `test_render_options_published_by_plan`
- PASS `test_estimate_validates_against_published_options`
- PASS `test_free_plan_can_afford_one_useful_video`

## No cubierto en esta etapa (declarado, no probado)

- Celery/Redis reales, workers, pipeline de render, ffmpeg, S3/MinIO/R2 reales (se usa `FakeStore`; `S3Store` sin ejecutar).
- Verificación JWT contra el JWKS real de Clerk (la lógica de emisor/exp/azp está probada con claves locales).
- Webhooks de pago, suscripciones reales, `GET /v1/plans`, expiración física de URLs firmadas (se verifica que se generan con TTL, no que S3 las rechace).
- Recuperación de jobs `running` huérfanos por caída de worker (requiere un reaper; hoy solo existe `mark_running` → `resumed`).
- Carga/rendimiento; purga de `idempotency_keys` y migraciones Alembic (el esquema se aplica como un único `schema.sql`).
- Tarifas: son BORRADOR; el Free solo está validado contra los pesos draft (`test_free_plan_can_afford_one_useful_video`).
- Con pesos draft, 60 s de `solution_video` a 720p cuestan 39 créditos > 30: el límite vinculante del Free son los créditos (~47 s), no `max_video_seconds=60`.

