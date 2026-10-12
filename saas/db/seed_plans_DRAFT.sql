-- BORRADOR, NO APROBADO. No cargar en producción hasta medir costos reales por escena.
-- Restricción de negocio: cada plan debe poder generar >=1 video útil con sus créditos.
-- Con pesos svg 0.5 / manim 1.0 / threejs 2.5 por segundo:
--   Free 30 créditos => p.ej. 45 s de lección sin prólogo (manim 30 s + svg 30 s = 45), o 12 s de prólogo.
--   => Free NO incluye prólogo three.js (un prólogo de 30 s = 75 créditos). Prólogo desde Starter.
INSERT INTO plans (code, name, price_cents, monthly_credits, max_pdf_pages, max_pdf_bytes,
                   max_video_seconds, max_concurrent_jobs, max_resolution, queue_priority, video_retention_days)
VALUES
  ('free',    'Free',    0,     30,  5,  10485760,   60, 1, '720p',  2,  7),
  ('starter', 'Starter', 1900,  300, 20, 31457280,  480, 1, '1080p', 5, 30),
  ('pro',     'Pro',     5900, 1200, 60, 104857600, 900, 3, '1080p', 8, 90);
