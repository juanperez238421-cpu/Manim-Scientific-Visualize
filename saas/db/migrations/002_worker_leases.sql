-- 002: worker local con lease/heartbeat (el worker NUNCA toca la BD: solo llama a la API interna).
-- Idempotente: se puede reaplicar.
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS lease_owner text;
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS lease_expires_at timestamptz;
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS delivery jsonb;   -- veredictos separados: extracción/verificación/render/QA
CREATE INDEX IF NOT EXISTS idx_jobs_lease ON jobs(lease_expires_at) WHERE status = 'running';

-- Reclama un job: 'queued' o 'running' con lease vencido (worker caído). SKIP LOCKED: varios workers sin pisarse.
-- Tras p_max_attempts reclamos fallidos el job se cierra como fallo de plataforma (reembolso total).
CREATE OR REPLACE FUNCTION claim_job(p_worker text, p_lease_seconds integer DEFAULT 120,
                                     p_max_attempts integer DEFAULT 3) RETURNS uuid AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  LOOP
    SELECT * INTO j FROM jobs
     WHERE status = 'queued' OR (status = 'running' AND lease_expires_at IS NOT NULL AND lease_expires_at < now())
     ORDER BY COALESCE(queued_at, created_at) LIMIT 1 FOR UPDATE SKIP LOCKED;
    IF NOT FOUND THEN RETURN NULL; END IF;
    IF j.status = 'running' AND j.cancel_requested_at IS NOT NULL THEN
      PERFORM confirm_cancel(j.id, 0);                       -- el worker murió tras pedir cancelar: no se cobra
      CONTINUE;
    END IF;
    IF j.attempts >= p_max_attempts THEN
      PERFORM fail_job(j.id, 'worker_lost', 'El worker dejó de responder demasiadas veces.', true, 0);
      CONTINUE;
    END IF;
    IF j.status = 'queued' THEN
      UPDATE jobs SET status = 'running', started_at = now() WHERE id = j.id;
    END IF;
    UPDATE jobs SET attempts = attempts + 1, lease_owner = p_worker,
                    lease_expires_at = now() + make_interval(secs => p_lease_seconds) WHERE id = j.id;
    UPDATE outbox SET status = 'published', published_at = now() WHERE job_id = j.id AND status = 'pending';
    RETURN j.id;
  END LOOP;
END $$ LANGUAGE plpgsql;

-- Latido: extiende el lease. 'ok' | 'cancel_requested'. Lanza lease_lost si otro worker lo tiene.
CREATE OR REPLACE FUNCTION worker_heartbeat(p_job uuid, p_worker text, p_lease_seconds integer DEFAULT 120)
RETURNS text AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status <> 'running' OR j.lease_owner IS DISTINCT FROM p_worker THEN RAISE EXCEPTION 'lease_lost'; END IF;
  UPDATE jobs SET lease_expires_at = now() + make_interval(secs => p_lease_seconds) WHERE id = p_job;
  RETURN CASE WHEN j.cancel_requested_at IS NOT NULL THEN 'cancel_requested' ELSE 'ok' END;
END $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION worker_set_stage(p_job uuid, p_worker text, p_stage stage_name, p_status step_status,
                                            p_progress integer, p_lease_seconds integer DEFAULT 120)
RETURNS text AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status <> 'running' OR j.lease_owner IS DISTINCT FROM p_worker THEN RAISE EXCEPTION 'lease_lost'; END IF;
  UPDATE job_stages SET status = p_status, worker_host = p_worker,
         started_at = CASE WHEN p_status = 'running' THEN COALESCE(started_at, now()) ELSE started_at END,
         finished_at = CASE WHEN p_status IN ('succeeded','failed','skipped') THEN now() ELSE finished_at END
   WHERE job_id = p_job AND stage = p_stage AND attempt = (SELECT max(attempt) FROM job_stages WHERE job_id = p_job AND stage = p_stage);
  UPDATE jobs SET current_stage = p_stage, progress_pct = GREATEST(progress_pct, LEAST(COALESCE(p_progress, 0), 99)),
                  lease_expires_at = now() + make_interval(secs => p_lease_seconds) WHERE id = p_job;
  RETURN CASE WHEN j.cancel_requested_at IS NOT NULL THEN 'cancel_requested' ELSE 'ok' END;
END $$ LANGUAGE plpgsql;

-- Éxito: registra el video, el veredicto y liquida (cobra min(credits, reservado)). Solo el dueño del lease.
CREATE OR REPLACE FUNCTION worker_complete(p_job uuid, p_worker text, p_credits integer, p_delivery jsonb,
                                           p_storage_key text, p_share_key text, p_duration numeric,
                                           p_width integer, p_height integer, p_fps integer,
                                           p_size bigint, p_sha256 text, p_qa jsonb) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'succeeded' THEN RETURN j.final_credits; END IF;
  IF j.status <> 'running' OR j.lease_owner IS DISTINCT FROM p_worker THEN RAISE EXCEPTION 'lease_lost'; END IF;
  IF j.cancel_requested_at IS NOT NULL THEN RAISE EXCEPTION 'cancel_requested'; END IF;
  INSERT INTO videos(job_id, user_id, storage_key, share_key, duration_seconds, width, height, fps, size_bytes,
                     sha256, qa_report)
    VALUES (p_job, j.user_id, p_storage_key, p_share_key, p_duration, p_width, p_height, p_fps, p_size, p_sha256, p_qa)
    ON CONFLICT (job_id) DO NOTHING;
  UPDATE job_stages SET status = 'skipped', finished_at = now() WHERE job_id = p_job AND status = 'pending';
  UPDATE job_stages SET status = 'succeeded', finished_at = COALESCE(finished_at, now())
   WHERE job_id = p_job AND status = 'running';
  UPDATE jobs SET delivery = p_delivery, lease_owner = NULL, lease_expires_at = NULL WHERE id = p_job;
  RETURN complete_job(p_job, p_credits);
END $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION worker_fail(p_job uuid, p_worker text, p_code text, p_message text,
                                       p_platform_fault boolean, p_consumed integer, p_delivery jsonb)
RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'failed' THEN RETURN j.final_credits; END IF;
  IF j.status <> 'running' OR j.lease_owner IS DISTINCT FROM p_worker THEN RAISE EXCEPTION 'lease_lost'; END IF;
  UPDATE job_stages SET status = 'failed', finished_at = now() WHERE job_id = p_job AND status = 'running';
  UPDATE job_stages SET status = 'skipped', finished_at = now() WHERE job_id = p_job AND status = 'pending';
  UPDATE jobs SET delivery = p_delivery, lease_owner = NULL, lease_expires_at = NULL WHERE id = p_job;
  RETURN fail_job(p_job, p_code, p_message, p_platform_fault, p_consumed);
END $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION worker_confirm_cancel(p_job uuid, p_worker text, p_consumed integer) RETURNS integer AS $$
DECLARE j jobs%ROWTYPE;
BEGIN
  SELECT * INTO j FROM jobs WHERE id = p_job FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'job_not_found'; END IF;
  IF j.status = 'cancelled' THEN RETURN j.final_credits; END IF;
  IF j.lease_owner IS DISTINCT FROM p_worker THEN RAISE EXCEPTION 'lease_lost'; END IF;
  UPDATE jobs SET lease_owner = NULL, lease_expires_at = NULL WHERE id = p_job;
  RETURN confirm_cancel(p_job, p_consumed);
END $$ LANGUAGE plpgsql;
