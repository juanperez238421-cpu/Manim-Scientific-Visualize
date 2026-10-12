-- =====================================================================
-- PDF -> animated educational video SaaS  |  PostgreSQL 15+ schema (v0.1)
-- Propuesta para validación. Convenciones:
--   * PK uuid (gen_random_uuid, built-in desde PG13)
--   * timestamptz siempre en UTC
--   * dinero en centavos (integer), créditos en enteros ("credit" = 1 unidad)
--   * ledger de créditos append-only: el saldo se DERIVA, nunca se edita
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS citext;

-- ---------- helpers ----------------------------------------------------
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END $$ LANGUAGE plpgsql;

-- ---------- enums ------------------------------------------------------
CREATE TYPE job_status AS ENUM (
  'draft',        -- creado por el chatbot/UI, aún no cobrado
  'queued',       -- créditos reservados, en cola
  'running',
  'succeeded',
  'failed',
  'cancelled'
);

CREATE TYPE job_kind AS ENUM (
  'solution_video',   -- flujo pdf-document-to-solution-video
  'hybrid_lesson'     -- HYBRID-SCIANIM-v1: prólogo pop-up + lección Manim + SVG
);

CREATE TYPE render_engine AS ENUM ('manim', 'threejs', 'svg', 'ffmpeg', 'llm', 'pdf');

CREATE TYPE stage_name AS ENUM (
  'extract',        -- PDF -> contenido estructurado + validación contra clave
  'script',         -- guion + lista de escenas (LLM + solver determinista)
  'render_manim',
  'render_prologue',-- three.js headless
  'render_svg',
  'compose',        -- ffmpeg concat + QA
  'upload'
);

CREATE TYPE step_status AS ENUM ('pending','running','succeeded','failed','skipped');

CREATE TYPE ledger_entry_type AS ENUM (
  'grant',      -- créditos mensuales del plan
  'purchase',   -- top-up pagado
  'reserve',    -- al encolar (delta negativo)
  'release',    -- devolución de reserva no usada (delta positivo)
  'consume',    -- ajuste final si el costo real > reserva (delta negativo)
  'refund',     -- reembolso manual / por fallo
  'expire',     -- caducidad de créditos del ciclo
  'adjustment'  -- soporte
);

-- ---------- usuarios ---------------------------------------------------
CREATE TABLE users (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email          citext NOT NULL UNIQUE,
  email_verified boolean NOT NULL DEFAULT false,
  password_hash  text,                       -- NULL si solo OAuth
  display_name   text,
  locale         text NOT NULL DEFAULT 'es',
  role           text NOT NULL DEFAULT 'user' CHECK (role IN ('user','admin','support')),
  status         text NOT NULL DEFAULT 'active' CHECK (status IN ('active','suspended','deleted')),
  stripe_customer_id text UNIQUE,
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now(),
  deleted_at     timestamptz
);
CREATE TRIGGER trg_users_updated BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------- planes y suscripciones ------------------------------------
CREATE TABLE plans (
  id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code                  text NOT NULL UNIQUE,            -- free, starter, pro, ...
  name                  text NOT NULL,
  price_cents           integer NOT NULL CHECK (price_cents >= 0),
  currency              char(3) NOT NULL DEFAULT 'USD',
  monthly_credits       integer NOT NULL CHECK (monthly_credits >= 0),
  max_pdf_pages         integer NOT NULL CHECK (max_pdf_pages > 0),
  max_pdf_bytes         bigint  NOT NULL CHECK (max_pdf_bytes > 0),
  max_video_seconds     integer NOT NULL CHECK (max_video_seconds > 0),
  max_concurrent_jobs   integer NOT NULL DEFAULT 1 CHECK (max_concurrent_jobs > 0),
  max_resolution        text NOT NULL DEFAULT '1080p' CHECK (max_resolution IN ('480p','720p','1080p')),
  queue_priority        smallint NOT NULL DEFAULT 5 CHECK (queue_priority BETWEEN 0 AND 9),
  video_retention_days  integer NOT NULL DEFAULT 30 CHECK (video_retention_days > 0),
  is_active             boolean NOT NULL DEFAULT true,
  created_at            timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE subscriptions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id                 uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan_id                 uuid NOT NULL REFERENCES plans(id),
  status                  text NOT NULL CHECK (status IN ('trialing','active','past_due','cancelled','expired')),
  current_period_start    timestamptz NOT NULL,
  current_period_end      timestamptz NOT NULL,
  cancel_at_period_end    boolean NOT NULL DEFAULT false,
  stripe_subscription_id  text UNIQUE,
  created_at              timestamptz NOT NULL DEFAULT now(),
  updated_at              timestamptz NOT NULL DEFAULT now(),
  CHECK (current_period_end > current_period_start)
);
-- un usuario solo puede tener UNA suscripción vigente
CREATE UNIQUE INDEX uq_subscriptions_one_live ON subscriptions(user_id)
  WHERE status IN ('trialing','active','past_due');
CREATE TRIGGER trg_subs_updated BEFORE UPDATE ON subscriptions
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------- PDFs subidos ----------------------------------------------
CREATE TABLE pdf_files (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  original_name text NOT NULL,
  storage_key   text NOT NULL UNIQUE,                 -- clave S3
  size_bytes    bigint NOT NULL CHECK (size_bytes > 0),
  sha256        char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  page_count    integer CHECK (page_count > 0),       -- NULL hasta analizar
  has_text_layer boolean,                              -- false => requiere OCR (más caro)
  analysis      jsonb NOT NULL DEFAULT '{}'::jsonb,    -- n problemas, ecuaciones, figuras, complejidad
  status        text NOT NULL DEFAULT 'uploaded'
                CHECK (status IN ('uploaded','analyzed','rejected','deleted')),
  reject_reason text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  deleted_at    timestamptz
);
CREATE INDEX idx_pdf_files_user ON pdf_files(user_id, created_at DESC);
CREATE INDEX idx_pdf_files_sha  ON pdf_files(user_id, sha256);   -- dedupe / caché

-- ---------- jobs -------------------------------------------------------
CREATE TABLE jobs (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id            uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  pdf_file_id        uuid NOT NULL REFERENCES pdf_files(id),
  kind               job_kind NOT NULL,
  status             job_status NOT NULL DEFAULT 'draft',
  current_stage      stage_name,
  progress_pct       smallint NOT NULL DEFAULT 0 CHECK (progress_pct BETWEEN 0 AND 100),

  -- configuración elegida por el usuario / chatbot
  config             jsonb NOT NULL DEFAULT '{}'::jsonb,
      -- {language, detail_level, target_seconds, include_prologue, resolution,
      --  problems_selected:[...], version:'A'|'B'|...}
  protocol_version   text NOT NULL DEFAULT 'HYBRID-SCIANIM-v1',
  pipeline_version   text NOT NULL,                   -- versión del wrapper de librerías (reproducibilidad)

  -- estimación y cobro
  complexity_score   numeric(6,2) CHECK (complexity_score >= 0),
  estimated_seconds  integer CHECK (estimated_seconds > 0),   -- duración final estimada del video
  estimated_credits  integer CHECK (estimated_credits >= 0),
  reserved_credits   integer NOT NULL DEFAULT 0 CHECK (reserved_credits >= 0),
  final_credits      integer CHECK (final_credits >= 0),

  -- ejecución
  celery_root_id     text,
  attempts           smallint NOT NULL DEFAULT 0,
  error_code         text,
  error_message      text,
  idempotency_key    text,                             -- evita doble cobro en reintentos del cliente

  created_at         timestamptz NOT NULL DEFAULT now(),
  queued_at          timestamptz,
  started_at         timestamptz,
  finished_at        timestamptz,
  updated_at         timestamptz NOT NULL DEFAULT now(),

  CHECK (status <> 'queued'    OR queued_at IS NOT NULL),
  CHECK (status <> 'running'   OR started_at IS NOT NULL),
  CHECK (status NOT IN ('succeeded','failed','cancelled') OR finished_at IS NOT NULL),
  CHECK (status <> 'failed' OR error_code IS NOT NULL)
);
CREATE UNIQUE INDEX uq_jobs_idempotency ON jobs(user_id, idempotency_key)
  WHERE idempotency_key IS NOT NULL;
CREATE INDEX idx_jobs_user_created ON jobs(user_id, created_at DESC);
CREATE INDEX idx_jobs_active       ON jobs(status, queued_at) WHERE status IN ('queued','running');
CREATE INDEX idx_jobs_pdf          ON jobs(pdf_file_id);
CREATE TRIGGER trg_jobs_updated BEFORE UPDATE ON jobs
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- etapas del pipeline (una fila por etapa e intento) -> reintentos, costo y observabilidad
CREATE TABLE job_stages (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id        uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  stage         stage_name NOT NULL,
  attempt       smallint NOT NULL DEFAULT 1,
  status        step_status NOT NULL DEFAULT 'pending',
  worker_host   text,
  started_at    timestamptz,
  finished_at   timestamptz,
  cpu_seconds   numeric(10,2) CHECK (cpu_seconds >= 0),   -- tiempo real consumido
  artifact_key  text,                                      -- salida intermedia en S3
  error_message text,
  UNIQUE (job_id, stage, attempt)
);
CREATE INDEX idx_job_stages_job ON job_stages(job_id);

-- escenas del guion (HYBRID-SCIANIM-v1: H1.., lección 01.., anexos A1..)
CREATE TABLE job_scenes (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id          uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  position        integer NOT NULL CHECK (position >= 0),
  label           text NOT NULL,                       -- 'H1', '01', 'A1'
  engine          render_engine NOT NULL CHECK (engine IN ('manim','threejs','svg')),
  spec            jsonb NOT NULL,                      -- definición declarativa de la escena
  spec_hash       char(64) NOT NULL,                   -- caché de render por contenido
  planned_seconds numeric(7,2) NOT NULL CHECK (planned_seconds > 0),
  status          step_status NOT NULL DEFAULT 'pending',
  render_seconds  numeric(10,2) CHECK (render_seconds >= 0),
  clip_key        text,                                -- clip mp4 en S3
  cache_hit       boolean NOT NULL DEFAULT false,
  UNIQUE (job_id, position)
);
CREATE INDEX idx_job_scenes_hash ON job_scenes(spec_hash);   -- reutilizar clips idénticos

-- ---------- videos generados ------------------------------------------
CREATE TABLE videos (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id           uuid NOT NULL UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
  user_id          uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  storage_key      text NOT NULL UNIQUE,
  share_key        text UNIQUE,                         -- copia <30 MB para compartir
  duration_seconds numeric(8,2) NOT NULL CHECK (duration_seconds > 0),
  width            integer NOT NULL CHECK (width > 0),
  height           integer NOT NULL CHECK (height > 0),
  fps              smallint NOT NULL CHECK (fps > 0),
  size_bytes       bigint NOT NULL CHECK (size_bytes > 0),
  sha256           char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  qa_report        jsonb NOT NULL DEFAULT '{}'::jsonb,  -- ffprobe, juntas blancas, PASS/FAIL por valor
  expires_at       timestamptz,                         -- según plan.video_retention_days
  created_at       timestamptz NOT NULL DEFAULT now(),
  deleted_at       timestamptz
);
CREATE INDEX idx_videos_user    ON videos(user_id, created_at DESC);
CREATE INDEX idx_videos_expires ON videos(expires_at) WHERE deleted_at IS NULL;

-- ---------- créditos (ledger append-only) -----------------------------
CREATE TABLE credit_ledger (
  id              bigserial PRIMARY KEY,
  user_id         uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  job_id          uuid REFERENCES jobs(id),
  subscription_id uuid REFERENCES subscriptions(id),
  entry_type      ledger_entry_type NOT NULL,
  delta           integer NOT NULL CHECK (delta <> 0),
  reason          text,
  idempotency_key text UNIQUE,                          -- webhooks de Stripe / reintentos de Celery
  created_at      timestamptz NOT NULL DEFAULT now(),
  -- signo coherente con el tipo
  CHECK (
    (entry_type IN ('grant','purchase','release','refund') AND delta > 0) OR
    (entry_type IN ('reserve','consume','expire')           AND delta < 0) OR
    (entry_type = 'adjustment')
  ),
  CHECK (entry_type NOT IN ('reserve','release','consume') OR job_id IS NOT NULL)
);
CREATE INDEX idx_ledger_user ON credit_ledger(user_id, id DESC);
CREATE INDEX idx_ledger_job  ON credit_ledger(job_id) WHERE job_id IS NOT NULL;

-- el ledger no se edita ni se borra
CREATE OR REPLACE FUNCTION forbid_ledger_mutation() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'credit_ledger is append-only';
END $$ LANGUAGE plpgsql;
CREATE TRIGGER trg_ledger_immutable BEFORE UPDATE OR DELETE ON credit_ledger
  FOR EACH ROW EXECUTE FUNCTION forbid_ledger_mutation();

CREATE VIEW credit_balances AS
  SELECT user_id, COALESCE(SUM(delta), 0)::integer AS balance
  FROM credit_ledger GROUP BY user_id;

-- ---------- logs de renderizado ---------------------------------------
CREATE TABLE render_logs (
  id         bigserial PRIMARY KEY,
  job_id     uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  stage_id   uuid REFERENCES job_stages(id) ON DELETE SET NULL,
  scene_id   uuid REFERENCES job_scenes(id) ON DELETE SET NULL,
  level      text NOT NULL DEFAULT 'info' CHECK (level IN ('debug','info','warning','error')),
  source     render_engine,
  message    text NOT NULL,
  data       jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_render_logs_job   ON render_logs(job_id, id);
CREATE INDEX idx_render_logs_error ON render_logs(job_id) WHERE level = 'error';
-- (a escala: particionar por mes en created_at y retener 30-90 días)

-- ---------- historial de uso / costo real -----------------------------
CREATE TABLE usage_events (
  id               bigserial PRIMARY KEY,
  user_id          uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  job_id           uuid REFERENCES jobs(id) ON DELETE SET NULL,
  metric           text NOT NULL CHECK (metric IN (
                     'manim_render_seconds','threejs_render_seconds','ffmpeg_seconds',
                     'llm_input_tokens','llm_output_tokens','ocr_pages',
                     'storage_bytes','video_seconds_delivered')),
  quantity         numeric(14,2) NOT NULL CHECK (quantity >= 0),
  unit_cost_micros bigint CHECK (unit_cost_micros >= 0),   -- costo interno en 1e-6 USD por unidad
  occurred_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_usage_user_time ON usage_events(user_id, occurred_at DESC);
CREATE INDEX idx_usage_job       ON usage_events(job_id);
CREATE INDEX idx_usage_metric    ON usage_events(metric, occurred_at);

-- ---------- chatbot ----------------------------------------------------
CREATE TABLE chat_sessions (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  pdf_file_id uuid REFERENCES pdf_files(id) ON DELETE SET NULL,
  job_id     uuid REFERENCES jobs(id) ON DELETE SET NULL,      -- job en configuración/seguimiento
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id, updated_at DESC);

CREATE TABLE chat_messages (
  id         bigserial PRIMARY KEY,
  session_id uuid NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role       text NOT NULL CHECK (role IN ('user','assistant','tool')),
  content    jsonb NOT NULL,                  -- bloques de la API de Claude (text/tool_use/tool_result)
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id, id);

-- ---------- datos semilla de planes (ajustables) ----------------------
INSERT INTO plans (code, name, price_cents, monthly_credits, max_pdf_pages, max_pdf_bytes,
                   max_video_seconds, max_concurrent_jobs, max_resolution, queue_priority, video_retention_days)
VALUES
  ('free',    'Free',    0,     30,  5,  10485760,  120, 1, '720p',  2,  7),
  ('starter', 'Starter', 1900,  300, 20, 31457280,  480, 1, '1080p', 5, 30),
  ('pro',     'Pro',     5900, 1200, 60, 104857600, 900, 3, '1080p', 8, 90);
