# Arquitectura propuesta (v0.1, pendiente de validación)

## 1. Monorepo

```
saas/
├── apps/
│   ├── api/                 # FastAPI: auth, uploads, jobs, créditos, descarga
│   │   ├── app/{routers,services,models,schemas,deps}/
│   │   └── tests/
│   ├── worker/              # Celery: tareas del pipeline (misma imagen base, distintas colas)
│   │   ├── tasks/{extract,script,render_manim,render_prologue,render_svg,compose,upload}.py
│   │   └── tests/
│   └── chatbot/             # Servicio de chat (Claude API + tools contra la API del backend)
├── packages/
│   ├── core/                # Dominio compartido: modelos Pydantic, SceneSpec, estimador de costo/créditos
│   ├── sciviz_adapter/      # Wrapper interno sobre TUS librerías Manim (interfaz estable + versionado)
│   ├── pdf_extract/         # pdfplumber/PyMuPDF/OCR -> Document IR; solver + validate (flujo solution-video)
│   ├── protocol/            # HYBRID-SCIANIM-v1: tokens de diseño, plantilla narrativa, pausas, QA
│   └── storage/             # Cliente S3-compatible (boto3), claves y URLs firmadas
├── engines/
│   ├── threejs_prologue/    # index.html, main.js, art.js, chapters.js, flat.js, render.mjs (Playwright)
│   └── manim_scenes/        # Escenas Manim base parametrizadas (heredan de sciviz_adapter)
├── db/
│   ├── schema.sql           # (incluido en esta propuesta)
│   └── migrations/          # Alembic, a partir del schema aprobado
├── infra/
│   ├── docker/              # api.Dockerfile, worker-manim.Dockerfile (LaTeX+Cairo), worker-web.Dockerfile (Chromium+Node)
│   ├── compose.yaml         # dev: postgres, redis, minio, api, workers
│   └── k8s/ (o terraform/)  # prod: HPA por longitud de cola
└── docs/
```

Las dependencias van en una sola dirección: `apps → packages`. `apps/worker`
nunca importa de `apps/api`.

## 2. Pipeline por job

```
POST /v1/uploads/init → PUT presignado a R2/MinIO → POST /v1/uploads/{id}/complete ─▶ fila pdf_files verificada ─▶ análisis rápido (páginas, texto/OCR, nº problemas) ─▶ estimación de créditos
POST /v1/jobs (estimate_id + Idempotency-Key) ─▶ reserve_credits() atómico ─▶ Celery chain:

 extract ─▶ script ─▶ ┌ render_manim    (cola "manim",   CPU-heavy)  ┐ ─▶ compose ─▶ upload
                      ├ render_prologue (cola "web",     Chromium)   ┤    (ffmpeg)
                      └ render_svg      (cola "web")                 ┘
                         (group/chord: una tarea por ESCENA -> paralelo y reintentable)
```

* **extract**: PDF → `Document IR`. Datos exactos desde el texto del PDF (nada tecleado); para
  `solution_video` se calcula la respuesta en código y se valida contra clave si existe (flujo de
  pdf-document-to-solution-video). Si render y texto discrepan, el job falla con error claro.
* **script**: LLM propone estructura; un validador determinista la fuerza a la plantilla de
  HYBRID-SCIANIM-v1: *prólogo histórico (B, 1–6 cap. de ~30 s) → pregunta → pausa de predicción →
  fenómeno → derivación con números primero → ejemplos → excepciones → síntesis*. El orden nunca se
  altera; solo se acorta. Salida: lista de `SceneSpec` (JSON declarativo, sin código arbitrario).
* **render**: una tarea Celery por escena; `spec_hash` = clave de caché (si existe clip idéntico en
  S3 → no se re-renderiza). 1920×1080, 30 fps, H.264, yuv420p, cada clip empieza/termina en #FFFFFF.
* **compose**: `ffmpeg concat`; QA automático (ffprobe, decodificación completa, juntas blancas,
  SHA-256); copia share <30 MB.
* **Seguridad**: el LLM NUNCA produce Python que se ejecute; produce `SceneSpec` que plantillas
  Manim propias interpretan. Los PDFs son datos no confiables (workers sin red saliente salvo S3).
* **Colas**: `default`, `manim`, `web`, `ffmpeg` → autoescalado independiente. Prioridad por plan.
  `acks_late`, `task_reject_on_worker_lost`, reintentos con backoff, idempotencia por (job, stage, attempt).
* **Recomendación Celery+Redis**: sí para empezar (simple, suficiente). Si luego necesitas flujos
  durables largos, migrar a Temporal; el diseño por etapas ya lo permite.

## 3. Wrapper de librerías propias (sin acoplamiento)

```
packages/sciviz_adapter/
  api.py        # Protocol/ABC estable: draw_axes(), highlight(), step_panel() ...
  v1/           # implementación que delega en tu librería (versión fijada)
  registry.py   # elige implementación según job.pipeline_version
```

Tu repo se instala por commit/tag fijado (`pip install "git+https://...@<tag>"` o submódulo editable
en dev). Solo `sciviz_adapter/vN/` importa tu librería; todo lo demás usa `api.py`. Cambiar de
versión = nuevo `vN` + `pipeline_version` (los jobs viejos siguen reproducibles).
**No toco ningún repo externo hasta que me des el link y lo autorices.**

## 4. Chatbot (resumen)

Servicio aparte con la API de Claude y *tool use* contra el backend. Tools:
`get_pdf_analysis`, `estimate_job(config)`, `create_job(config, confirm=true)`,
`get_job_status(job_id)`, `cancel_job`, `get_credit_balance`, `suggest_script_improvements(job_id)`.
Reglas del prompt: nunca crear/cobrar sin confirmación explícita del usuario con el costo en créditos
mostrado; proponer recortes (menos problemas, sin prólogo, 720p) antes de renderizar; responder
estado solo con datos de `get_job_status`. Prompt y esquemas completos se entregan en la fase 2.

## 5. Costos y modelo de créditos

Costosos, de mayor a menor: **(1) Manim** (LaTeX + Cairo, ~minutos de CPU por minuto de video en 1080p/30fps),
**(2) prólogo three.js** (SwiftShader por software ≈ 0.8 s/frame/proceso a 1080p → ~24 s CPU por segundo
de video; es el más caro por segundo), (3) OCR de PDFs escaneados, (4) LLM (barato en comparación),
(5) ffmpeg y S3 (marginales; el egress de descargas sí cuenta).

Cobro propuesto — **créditos por segundo de video entregado, ponderado por motor**:

```
costo = Σ_escenas ( segundos × peso_motor )  × multiplicador_resolución  + cargo_análisis(OCR/páginas)
peso: svg 0.5 · manim 1.0 · threejs 2.5        (calibrar con usage_events reales)
```

* Se muestra la estimación ANTES de renderizar; se reserva (`reserve`), y al terminar se liquida
  (`release`/`consume`). Si el job falla por error nuestro → reembolso total.
* Límites por plan: páginas, duración máxima, jobs concurrentes, resolución, retención.
* Palancas de margen: caché por `spec_hash`, prólogo opcional (add-on), 480p/720p en borrador,
  render `-ql` de vista previa gratuita limitada, colas con prioridad por plan, workers spot.
* `usage_events.unit_cost_micros` registra el costo real para medir margen por plan y recalibrar pesos.

## 6. Preguntas abiertas para ti
1. ¿Este monorepo vive en este repo (`saas/`) o en un repo nuevo? (propongo repo nuevo en producción;
   aquí lo dejo en `saas/` mientras validamos).
2. Proveedor de pagos (¿Stripe?) y S3 (¿MinIO local/R2/AWS?).
3. ¿Autenticación propia (JWT) o delegada (Clerk/Auth0/Supabase)? El schema soporta ambas.
4. Idioma(s) en pantalla del video (el protocolo pide fijarlo por proyecto).

> v0.2: ver `CONTRACT.md` (protocolo de upload, estados, créditos, auth, pagos) y `db/schema.sql` v0.2.
