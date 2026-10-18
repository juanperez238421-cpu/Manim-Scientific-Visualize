-- BORRADOR, NO APROBADO. No cargar en producción hasta medir costos reales por escena.
-- Restricción de negocio: cada plan debe poder generar >=1 video útil con sus créditos.
-- Pesos borrador por segundo: svg 0.5 / manim 1.0 / threejs 2.5 (multiplicador de resolución aparte).
--   Free (30 créditos): p.ej. 20 s Manim + 20 s SVG = 20(1.0)+20(0.5) = 30 créditos => 40 s.
--   (El ejemplo anterior "30 s + 30 s" costaba 45: era un error.)
--   Un prólogo de 30 s three.js cuesta 75 => Free NO incluye prólogo.
-- NOTA: con max_video_seconds=60 el límite vinculante del Free son los créditos, no la duración.
INSERT INTO plans (code, name, price_cents, monthly_credits, max_pdf_pages, max_pdf_bytes,
                   max_video_seconds, max_concurrent_jobs, max_resolution, queue_priority,
                   video_retention_days, allows_prologue)
VALUES
  ('free',    'Free',    0,     30,  5,  10485760,   60, 1, '720p',  2,  7, false),
  ('starter', 'Starter', 1900,  300, 20, 31457280,  480, 1, '1080p', 5, 30, true),
  ('pro',     'Pro',     5900, 1200, 60, 104857600, 900, 3, '1080p', 8, 90, true);
