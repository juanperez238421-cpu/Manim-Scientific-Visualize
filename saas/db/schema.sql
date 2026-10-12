-- =====================================================================
-- PDF -> animated educational video SaaS  |  PostgreSQL 15+ schema (v0.3)
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
  email          citext NOT NULL,                  -- NO único: la identidad es (auth_provider, provider_subject)
  email_verified boolean NOT NULL DEFAULT false,
  auth_provider  text NOT NULL DEFAULT 'clerk',
  provider_subject text NOT NULL,            -- 'sub' del JWT verificado (Clerk). Identidad = (provider, sub), NO el email
  display_name   text,
  locale         text NOT NULL DEFAULT 'es',
  role           text NOT NULL DEFAULT 'user' CHECK (role IN ('user','admin','support')),
  status         text NOT NULL DEFAULT 'active' CHECK (status IN ('active','suspended','deleted')),
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now(),
  deleted_at     timestamptz,
  UNIQUE (auth_provider, provider_subject)
);
CREATE INDEX idx_users_email ON users(email);
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
  allows_prologue       boolean NOT NULL DEFAULT false,   -- prólogo three.js permitido en hybrid_lesson
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
  payment_provider        text,                    -- 'mercadopago' | 'wompi' | ... (sin decidir)
  external_subscription_id text,
  UNIQUE (payment_provider, external_subscription_id),
  CHECK ((payment_provider IS NULL) = (external_subscription_id IS NULL)),
  created_at              timestamptz NOT NULL DEFAULT now(),
  updated_at              timestamptz NOT NULL DEFAULT now(),
  CHECK (current_period_end > current_period_start)
);
-- un usuario solo puede tener UNA suscripción vigente
CREATE UNIQUE INDEX uq_subscriptions_one_live ON subscriptions(user_id)
  WHERE status IN ('trialing','active','past_due');
CREATE TRIGGER trg_subs_updated BEFORE UPDATE ON subscriptions
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE payment_customers (
  user_id     uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider    text NOT NULL,
  external_id text NOT NULL,
  PRIMARY KEY (user_id, provider),
  UNIQUE (provider, external_id)
);

-- ---------- PDFs subidos ----------------------------------------------
CREATE TABLE pdf_files (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  original_name text NOT NULL,
  storage_key   text NOT NULL UNIQUE,                 -- clave S3
  content_type  text NOT NULL DEFAULT 'application/pdf' CHECK (content_type = 'application/pdf'),
  size_bytes    bigint NOT NULL CHECK (size_bytes > 0),
  declared_sha256 char(64) NOT NULL CHECK (declared_sha256 ~ '^[0-9a-f]{64}$'),  -- lo declara el cliente en init
  sha256        char(64) CHECK (sha256 ~ '^[0-9a-f]{64}$'),                      -- lo CALCULA el servidor en complete
  upload_expires_at timestamptz,
  page_count    integer CHECK (page_count > 0),       -- NULL hasta analizar
  has_text_layer boolean,                              -- false => requiere OCR (más caro)
  ocr_required  boolean NOT NULL DEFAULT false,
  analysis      jsonb NOT NULL DEFAULT '{}'::jsonb,    -- n problemas, ecuaciones, figuras, complejidad
  status        text NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','uploaded','analyzed','rejected','deleted')),
                -- pending: init hecho; uploaded: bytes verificados; analyzed: listo para estimar
  reject_reason text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  deleted_at    timestamptz,
  CHECK (status IN ('pending','rejected','deleted') OR sha256 IS NOT NULL),
  CHECK (status <> 'analyzed' OR page_count IS NOT NULL),
  UNIQUE (id, user_id)                                  -- habilita FKs compuestas (pertenencia)
);
CREATE INDEX idx_pdf_files_user ON pdf_files(user_id, created_at DESC);
CREATE INDEX idx_pdf_files_sha  ON pdf_files(user_id, sha256);   -- dedupe / caché

-- ---------- estimaciones (contrato de precio mostrado al usuario) -----
CREATE TABLE job_estimates (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  pdf_file_id       uuid NOT NULL,
  kind              job_kind NOT NULL,
  config            jsonb NOT NULL,
  estimated_seconds integer NOT NULL CHECK (estimated_seconds > 0),
  estimated_credits integer NOT NULL CHECK (estimated_credits >= 0),
  max_credits       integer NOT NULL CHECK (max_credits >= estimated_credits),  -- tope que el usuario puede autorizar
  breakdown         jsonb NOT NULL,                  -- por motor/escena/OCR, para mostrar y auditar
  pricing_version   text NOT NULL,                   -- tarifas usadas (tarifas aún NO aprobadas)
  config_hash       char(64) NOT NULL,               -- sha256 canónico de (pdf, kind, config, créditos, versión)
  created_at        timestamptz NOT NULL DEFAULT now(),
  expires_at        timestamptz NOT NULL,
  UNIQUE (id, user_id, pdf_file_id),
  FOREIGN KEY (pdf_file_id, user_id) REFERENCES pdf_files(id, user_id)   -- el PDF es del mismo usuario
);
CREATE INDEX idx_job_estimates_user ON job_estimates(user_id, created_at DESC);

-- ---------- jobs -------------------------------------------------------
CREATE TABLE jobs (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id            uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  pdf_file_id        uuid NOT NULL,
  kind               job_kind NOT NULL,
  include_prologue   boolean NOT NULL DEFAULT false,
  estimate_id        uuid,
  max_authorized_credits integer CHECK (max_authorized_credits >= 0),  -- tope aceptado explícitamente
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
  cancel_requested_at timestamptz,                     -- cancelación cooperativa de jobs 'running'

  created_at         timestamptz NOT NULL DEFAULT now(),
  queued_at          timestamptz,
  started_at         timestamptz,
  finished_at        timestamptz,
  updated_at         timestamptz NOT NULL DEFAULT now(),

  CHECK (status <> 'queued'    OR queued_at IS NOT NULL),
  CHECK (status <> 'running'   OR started_at IS NOT NULL),
  CHECK (status NOT IN ('succeeded','failed','cancelled') OR finished_at IS NOT NULL),
  CHECK (status <> 'failed' OR error_code IS NOT NULL),
  -- el prólogo pop-up (H1..) solo existe en hybrid_lesson; solution_video nunca lo lleva
  CHECK (kind = 'hybrid_lesson' OR include_prologue = false),
  -- un job fuera de 'draft' debe tener estimación y tope autorizado
  CHECK (status = 'draft' OR (estimate_id IS NOT NULL AND max_authorized_credits IS NOT NULL)),
  -- se reserva SIEMPRE el máximo autorizado; el costo final nunca lo supera
  CHECK (status IN ('draft','cancelled') OR reserved_credits = max_authorized_credits),
  CHECK (final_credits IS NULL OR final_credits <= reserved_credits),
  -- pertenencia: PDF y estimación son del mismo usuario que el job
  FOREIGN KEY (pdf_file_id, user_id) REFERENCES pdf_files(id, user_id),
  FOREIGN KEY (estimate_id, user_id, pdf_file_id) REFERENCES job_estimates(id, user_id, pdf_file_id)
);
CREATE UNIQUE INDEX uq_jobs_estimate ON jobs(estimate_id) WHERE estimate_id IS NOT NULL;  -- estimación de un solo uso
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

-- =====================================================================
-- FINANZAS v0.3
-- Invariantes:
--   I1  Se reserva SIEMPRE el máximo autorizado; el cobro final <= reserva. La liquidación
--       solo LIBERA (delta > 0): nunca puede dejar el saldo negativo.
--   I2  Orden de bloqueo único: fila del job -> fila del usuario. El bloqueo de usuario es FOR NO KEY UPDATE
--       (serializa por usuario pero NO choca con el KEY SHARE que toman las FKs hijas: con FOR UPDATE
--       dos transacciones que ya insertaron filas hijas se bloqueaban mutuamente al 'subir' el bloqueo).
--   I3  Toda transición y todo movimiento de créditos ocurre en la misma transacción.
--   I4  Idempotencia: reserve/settle usan claves únicas en el ledger y jobs.final_credits.
--   I5  El saldo disponible nunca es negativo (trigger de defensa en el ledger).
--
-- Semántica de saldo (una sola, para no restar dos veces en la UI):
--   available = SUM(delta)   -> ya descuenta lo reservado
--   held      = reservas de jobs aún NO liquidados (final_credits IS NULL)
--   total     = available + held
-- =====================================================================
CREATE VIEW credit_balances AS
  SELECT u.id AS user_id, COALESCE(SUM(l.delta), 0)::integer AS available
  FROM users u LEFT JOIN credit_ledger l ON l.user_id = u.id GROUP BY u.id;

CREATE VIEW credit_holds AS
  SELECT j.user_id, COALESCE(-SUM(l.delta), 0)::integer AS held
  FROM jobs j JOIN credit_ledger l ON l.job_id = j.id
  WHERE j.final_credits IS NULL AND j.reserved_credits > 0
  GROUP BY j.user_id;

-- I5: defensa en profundidad. Serializa por usuario y rechaza saldos negativos.
CREATE OR REPLACE FUNCTION ledger_nonnegative() RETURNS trigger AS $$
DECLARE v_bal integer;
BEGIN
  IF NEW.delta < 0 THEN
    PERFORM 1 FROM users WHERE id = NEW.user_id FOR NO KEY UPDATE;
    SELECT COALESCE(SUM(delta), 0) INTO v_bal FROM credit_ledger WHERE user_id = NEW.user_id;
    IF v_bal + NEW.delta < 0 THEN
      RAISE EXCEPTION 'insufficient_credits';
    END IF;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
CREATE TRIGGER trg_ledger_nonneg BEFORE INSERT ON credit_ledger
  FOR EACH ROW EXECUTE FUNCTION ledger_nonnegative();

-- ---------- transiciones válidas de estado ----------------------------
CREATE OR REPLACE FUNCTION jobs_check_transition() RETURNS trigger AS $$
BEGIN
  IF NEW.status = OLD.status THEN RETURN NEW; END IF;
  IF (OLD.status, NEW.status) IN (
       ('draft','queued'), ('draft','cancelled'),
       ('queued','running'), ('queued','cancelled'), ('queued','failed'),
       ('running','succeeded'), ('running','failed'), ('running','cancelled')) THEN
    RETURN NEW;
  END IF;
  RAISE EXCEPTION 'invalid_transition: % -> %', OLD.status, NEW.status;
END $$ LANGUAGE plpgsql;
CREATE TRIGGER trg_jobs_transition BEFORE UPDATE OF status ON jobs
  FOR EACH ROW EXECUTE FUNCTION jobs_check_transition();

-- Al hacer COMMIT, todo job terminal debe estar liquidado (final_credits fijado).
CREATE OR REPLACE FUNCTION jobs_terminal_settled() RETURNS trigger AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = NEW.id;          -- estado FINAL de la transacción, no el de NEW
  IF FOUND AND j.status IN ('succeeded','failed','cancelled')
     AND j.final_credits IS NULL AND j.reserved_credits > 0 THEN
    RAISE EXCEPTION 'terminal job % not settled', j.id;
  END IF;
  RETURN NULL;
END $$ LANGUAGE plpgsql;
CREATE CONSTRAINT TRIGGER trg_jobs_terminal_settled AFTER INSERT OR UPDATE ON jobs
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION jobs_terminal_settled();

-- ---------- idempotencia HTTP -----------------------------------------
CREATE TABLE idempotency_keys (
  id              bigserial PRIMARY KEY,
  user_id         uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  scope           text NOT NULL,              -- 'job.create', 'job.cancel:<id>'
  key             text NOT NULL,
  request_hash    char(64) NOT NULL,          -- sha256 del cuerpo canónico (+ parámetros de ruta)
  response_status smallint,
  response_body   jsonb,
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (user_id, scope, key)
);
-- (purgar > 24-72 h con un job periódico)

-- ---------- transactional outbox (publicación durable a Celery) -------
CREATE TABLE outbox (
  id           bigserial PRIMARY KEY,
  job_id       uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  topic        text NOT NULL,
  payload      jsonb NOT NULL,
  status       text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','published','cancelled')),
  attempts     integer NOT NULL DEFAULT 0,
  available_at timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz,
  last_error   text,
  created_at   timestamptz NOT NULL DEFAULT now(),
  UNIQUE (job_id, topic)
);
CREATE INDEX idx_outbox_pending ON outbox(available_at) WHERE status = 'pending';

-- ---------- funciones financieras -------------------------------------
-- Los errores de negocio se señalan con RAISE EXCEPTION '<code>' (message = código estable).

-- Liquida un job. PRECONDICIÓN: el llamador ya bloqueó la fila del job (I2).
-- p_charge se acota a la reserva. Solo LIBERA la diferencia. Idempotente.
CREATE OR REPLACE FUNCTION _settle_locked(p_job uuid, p_charge integer) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE; v_charge integer; v_release integer;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job;
  IF j.final_credits IS NOT NULL THEN RETURN j.final_credits; END IF;      -- ya liquidado
  PERFORM 1 FROM users WHERE id = j.user_id FOR NO KEY UPDATE;                     -- job -> usuario
  v_charge  := LEAST(GREATEST(COALESCE(p_charge, 0), 0), j.reserved_credits);
  v_release := j.reserved_credits - v_charge;
  IF v_release > 0 THEN
    INSERT INTO credit_ledger(user_id, job_id, entry_type, delta, reason, idempotency_key)
      VALUES (j.user_id, p_job, 'release', v_release, 'settle: unused reserve', 'settle:' || p_job);
  END IF;
  UPDATE jobs SET final_credits = v_charge WHERE id = p_job;
  RETURN v_charge;
END $$ LANGUAGE plpgsql;

-- Crea y encola un job validando pertenencia, vigencia e integridad de la estimación,
-- reserva el máximo autorizado y deja la tarea en el outbox: TODO en una transacción.
CREATE OR REPLACE FUNCTION create_queued_job(
  p_user uuid, p_estimate uuid, p_estimate_hash text, p_max_auth integer, p_pipeline_version text,
  p_max_concurrent integer DEFAULT 1000
) RETURNS uuid AS $$
DECLARE e job_estimates%ROWTYPE; p pdf_files%ROWTYPE; v_job uuid; v_bal integer; v_prologue boolean;
BEGIN
  -- Bloqueo del usuario ANTES de insertar el job (el INSERT toma KEY SHARE sobre users por la FK; con
  -- FOR NO KEY UPDATE no hay conflicto). El job nuevo es invisible
  -- para otras transacciones, así que no existe ciclo con el orden job -> usuario del resto de funciones.
  PERFORM 1 FROM users WHERE id = p_user FOR NO KEY UPDATE;
  SELECT * INTO e FROM job_estimates WHERE id = p_estimate AND user_id = p_user;
  IF NOT FOUND THEN RAISE EXCEPTION 'estimate_not_found'; END IF;
  IF e.expires_at <= now() THEN RAISE EXCEPTION 'estimate_expired'; END IF;
  IF e.config_hash <> p_estimate_hash THEN RAISE EXCEPTION 'estimate_mismatch'; END IF;
  IF p_max_auth < e.estimated_credits OR p_max_auth > e.max_credits OR p_max_auth <= 0 THEN
    RAISE EXCEPTION 'invalid_authorization';
  END IF;
  IF EXISTS (SELECT 1 FROM jobs WHERE estimate_id = p_estimate) THEN
    RAISE EXCEPTION 'estimate_already_used';
  END IF;
  SELECT * INTO p FROM pdf_files WHERE id = e.pdf_file_id AND user_id = p_user;
  IF NOT FOUND OR p.status <> 'analyzed' OR p.deleted_at IS NOT NULL THEN
    RAISE EXCEPTION 'pdf_not_ready';
  END IF;
  v_prologue := COALESCE((e.config->>'include_prologue')::boolean, false);

  -- La fila del job nace en esta transacción (nadie más puede bloquearla).
  INSERT INTO jobs(user_id, pdf_file_id, kind, include_prologue, estimate_id, max_authorized_credits,
                   config, pipeline_version, estimated_seconds, estimated_credits)
    VALUES (p_user, e.pdf_file_id, e.kind, v_prologue, e.id, p_max_auth, e.config, p_pipeline_version,
            e.estimated_seconds, e.estimated_credits)
    RETURNING id INTO v_job;

  IF (SELECT count(*) FROM jobs WHERE user_id = p_user AND status IN ('queued','running')) >= p_max_concurrent THEN
    RAISE EXCEPTION 'concurrency_limit';
  END IF;
  SELECT COALESCE(SUM(delta), 0) INTO v_bal FROM credit_ledger WHERE user_id = p_user;
  IF v_bal < p_max_auth THEN RAISE EXCEPTION 'insufficient_credits'; END IF;
  INSERT INTO credit_ledger(user_id, job_id, entry_type, delta, reason, idempotency_key)
    VALUES (p_user, v_job, 'reserve', -p_max_auth, 'job reserve (max authorized)', 'reserve:' || v_job);

  UPDATE jobs SET status = 'queued', queued_at = now(), reserved_credits = p_max_auth WHERE id = v_job;

  INSERT INTO job_stages(job_id, stage, status)
    SELECT v_job, s, CASE WHEN s = 'render_prologue' AND NOT v_prologue THEN 'skipped'::step_status
                          ELSE 'pending'::step_status END
    FROM unnest(enum_range(NULL::stage_name)) AS s;

  INSERT INTO outbox(job_id, topic, payload)
    VALUES (v_job, 'job.run', jsonb_build_object('job_id', v_job));
  RETURN v_job;
END $$ LANGUAGE plpgsql;

-- Cancelación. queued/draft: inmediata + reembolso total. running: solo SOLICITA (cooperativa);
-- los créditos siguen retenidos hasta confirm_cancel(). Idempotente. Devuelve el estado resultante.
CREATE OR REPLACE FUNCTION request_cancel(p_job uuid, p_user uuid) RETURNS text AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job AND user_id = p_user FOR UPDATE;      -- job primero
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'cancelled' THEN RETURN 'cancelled'; END IF;
  IF j.status IN ('succeeded','failed') THEN RAISE EXCEPTION 'job_not_cancellable'; END IF;
  IF j.status = 'running' THEN
    UPDATE jobs SET cancel_requested_at = COALESCE(cancel_requested_at, now()) WHERE id = p_job;
    RETURN 'cancelling';
  END IF;
  -- draft | queued
  UPDATE jobs SET status = 'cancelled', finished_at = now() WHERE id = p_job;
  UPDATE outbox SET status = 'cancelled' WHERE job_id = p_job AND status = 'pending';
  UPDATE job_stages SET status = 'skipped' WHERE job_id = p_job AND status = 'pending';
  PERFORM _settle_locked(p_job, 0);
  RETURN 'cancelled';
END $$ LANGUAGE plpgsql;

-- Worker: inicia. 'started' | 'resumed' (re-entrega tras caída) | 'cancelled' | 'terminal'.
CREATE OR REPLACE FUNCTION mark_running(p_job uuid) RETURNS text AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'cancelled' THEN RETURN 'cancelled'; END IF;
  IF j.status IN ('succeeded','failed') THEN RETURN 'terminal'; END IF;
  IF j.status = 'running' THEN
    UPDATE jobs SET attempts = attempts + 1 WHERE id = p_job;
    RETURN 'resumed';
  END IF;
  UPDATE jobs SET status = 'running', started_at = now(), attempts = attempts + 1 WHERE id = p_job;
  RETURN 'started';
END $$ LANGUAGE plpgsql;

-- Worker: éxito. Cobra min(p_actual, reservado) y libera el resto. Idempotente.
CREATE OR REPLACE FUNCTION complete_job(p_job uuid, p_actual integer) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'succeeded' THEN RETURN j.final_credits; END IF;
  IF j.status <> 'running' THEN RAISE EXCEPTION 'invalid_transition: % -> succeeded', j.status; END IF;
  UPDATE jobs SET status = 'succeeded', finished_at = now(), progress_pct = 100 WHERE id = p_job;
  RETURN _settle_locked(p_job, p_actual);
END $$ LANGUAGE plpgsql;

-- Worker: fallo. Si es atribuible a la plataforma se devuelve TODO; si no, se cobra lo consumido.
CREATE OR REPLACE FUNCTION fail_job(p_job uuid, p_code text, p_message text,
                                    p_platform_fault boolean, p_consumed integer) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'failed' THEN RETURN j.final_credits; END IF;
  IF j.status NOT IN ('queued','running') THEN RAISE EXCEPTION 'invalid_transition: % -> failed', j.status; END IF;
  UPDATE jobs SET status = 'failed', finished_at = now(), error_code = p_code, error_message = p_message
   WHERE id = p_job;
  UPDATE outbox SET status = 'cancelled' WHERE job_id = p_job AND status = 'pending';
  RETURN _settle_locked(p_job, CASE WHEN p_platform_fault THEN 0 ELSE p_consumed END);
END $$ LANGUAGE plpgsql;

-- Worker: confirma que DEJÓ de procesar tras una solicitud de cancelación. Cobra solo lo consumido.
CREATE OR REPLACE FUNCTION confirm_cancel(p_job uuid, p_consumed integer) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'cancelled' THEN RETURN j.final_credits; END IF;
  IF j.status <> 'running' OR j.cancel_requested_at IS NULL THEN RAISE EXCEPTION 'cancel_not_requested'; END IF;
  UPDATE jobs SET status = 'cancelled', finished_at = now() WHERE id = p_job;
  UPDATE job_stages SET status = 'skipped' WHERE job_id = p_job AND status = 'pending';
  RETURN _settle_locked(p_job, p_consumed);
END $$ LANGUAGE plpgsql;

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
-- NOTA: los planes semilla viven en db/seed_plans_DRAFT.sql (tarifas NO aprobadas).
