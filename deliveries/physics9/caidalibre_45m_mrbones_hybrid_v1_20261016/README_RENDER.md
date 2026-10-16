# Physics 9 — Caída libre desde 45 m con Mr. Bones · HÍBRIDO V1

Un video, dos motores (protocolo HYBRID-SCIANIM-v1):

- **Motor B (cartoon):** Mr. Bones, rig 3D de 171 huesos, estilo años 30.
  - Caso 1: suelta la cabeza.
  - Casos 2 y 3: se arranca el brazo izquierdo y lo usa como **honda**.
  - Física de la honda: centro fijo C, R = 0,575 m, giro con α constante y luego ω constante. Suelta donde el radio es horizontal, así la velocidad sale vertical: v₀ = ωR = 10 m/s exactos, con ω ≈ 17,4 rad/s.
  - Pantalla dividida: vista general a escala con estroboscopio, y cámara que sigue al cráneo con lecturas t, y, v.
- **Motor A (ManimCE):**
  1. Pregunta y convención (+y arriba, a = −g).
  2. PAUSA · PREDICE.
  3. Números primero: tabla 0, 5, 20, 45 m; incrementos 1 : 3 : 5; Δv = −10 m/s cada segundo.
  4. Ecuación término a término, con unidades.
  5. La honda (v = ωR, a_c ≈ 17 g).
  6. Tres casos con sustitución y raíz positiva.
  7. Punto más alto: v = 0 ≠ a; simetría; v² = v₀² + 2gh.
  8. Excepciones: g = 9,81 y arrastre cuadrático estimado (RK4).
  9. Síntesis.

**Datos:** h = 45 m, g = 10 m/s² (las excepciones muestran también 9,81), sin aire.
**Resultados:** T = 3,00 s, −1 + √10 ≈ 2,16 s y 1 + √10 ≈ 4,16 s. |v| = 30,0 m/s, 31,6 m/s y 31,6 m/s.

**De dónde salen los números:** todos se calculan en `verify_caida_libre.py`, con asserts, y se guardan en `shared/derived.json`. Ambos motores leen las mismas constantes de `shared/constants.json`. El QA del cartoon comprueba que la cabeza dibujada coincide con y(t) en cada dibujo (error < 1e-9 m) y compara los resultados contra el JSON de Python.

**Formato:** 1920×1080, 30 fps, H.264 yuv420p, AAC. Cortes en blanco entre motores. Orden de los clips en `qa/EDL.json`. QA en `qa/VIDEO_QA.txt`; todo PASS.

**Archivos:**
- `*_pqh.mp4`: copia para GitHub, CRF 22, menos de 95 MiB.
- `*_SHARE.mp4`: copia para compartir, dos pasadas, menos de 30 MB.
