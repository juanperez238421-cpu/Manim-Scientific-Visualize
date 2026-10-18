# Propuesta de benchmark de render (NO ejecutado — solo lectura de la librería)

Objetivo: reemplazar los pesos BORRADOR de créditos (svg 0,5 / manim 1,0 / threejs 2,5 por segundo) por
costos medidos. No se modificó ni se ejecutó nada de `Core/`. Esto es solo el diseño.

## Interfaz observada (lectura de `Core/`, 322 líneas en total)
* `visual_engine.py`: `make_paragraph`, `make_badge`, `make_code_window`, `make_console_box`, `AcademicScene(MovingCameraScene)`.
* `physics_tools.py`: `create_piv_streamlines(npy_path, …)`, `draw_point_load`, `make_beam_support`,
  `create_3d_force_vector`, `make_dimension_line`.
* `software_tools.py`: `make_uml_class`, `make_node_box`, `make_pointer_arrow`, `make_memory_cell`.

Implicaciones para `sciviz_adapter` (v1): son **funciones factoría de mobjects + una escena base**, sin estado
ni versión propia; `from manim import *` (importación con comodín) y `create_piv_streamlines` lee un `.npy` desde
disco (ruta controlada por el sistema, nunca por el usuario). El adaptador debe exponer solo operaciones
nombradas y validadas (`draw_dimension`, `draw_uml`, …), nunca reenviar `**kwargs` arbitrarios.
La librería no cubre aún lo que HYBRID-SCIANIM-v1 exige (tokens de diseño C_ACC/C_VEL/C_POS/C_GAL, `state_box`,
`predict_box`, pausas P_*): esos vivirán en `packages/protocol`, no en la librería.

## Qué medir
Por escena y por motor: tiempo de pared, segundos de CPU (usuario+sistema), memoria máxima (RSS), resolución, fps,
duración del clip, tamaño del mp4, segundos de render por segundo de video (RTF). 5 repeticiones, mediana y p95.

| Caso | Contenido | Por qué |
|---|---|---|
| M1 | Texto + `make_badge` + `make_paragraph`, 10 s | línea base de Manim sin LaTeX |
| M2 | `MathTex` con 6 fórmulas, 15 s | costo de LaTeX (cuello de botella típico) |
| M3 | Ejes + gráfica + `ValueTracker` con lectura en vivo, 15 s | animación continua |
| M4 | Escena científica: `make_dimension_line` + `draw_point_load` + `make_beam_support`, 20 s | uso real de `Core/` |
| M5 | `create_piv_streamlines` con un `.npy` sintético fijo, 20 s | el caso más pesado de la librería |
| S1 | SVG (`flat.js`) 14 s con Playwright | costo de motor B-2D |
| T1 | Prólogo three.js (capítulo de 30 s) con SwiftShader | el más caro según el protocolo (~0,8 s/frame/proceso) |
| C1 | `ffmpeg concat` de 3 clips + copia <30 MB | composición |

Cada caso en 480p15, 720p30 y 1080p30 para calibrar `RESOLUTION_MULT`.

## Condiciones reproducibles (fijar y registrar en `benchmark_env.json`)
Commit exacto de `Manim-Scientific-Visualize`; Python, ManimCE, ffmpeg, LaTeX (texlive), Chromium/Playwright y
Node con versión; CPU (modelo, nº de núcleos), RAM, SO; contenedor Docker con límites fijos de CPU/RAM
(`--cpus`, `--memory`); sin otras cargas; caché de Manim limpia en la primera pasada y caliente en las siguientes
(medir ambas: la caché por `spec_hash` cambia el costo real).

## Salida y uso
`benchmark_results.csv` + `benchmark_env.json`. De ahí: costo en CPU-segundos por segundo de video por motor →
× precio de cómputo (spot/on-demand) = costo en USD → créditos = costo / precio objetivo por crédito con el margen
deseado. Los resultados alimentan `pricing.py` (`PRICING_VERSION` nuevo) y `usage_events.unit_cost_micros`.
Criterio de aceptación del plan Free: un video completo (extract + script + render + compose) dentro de 30 créditos.

## Autorización pendiente
Ejecutar el benchmark consume CPU y requiere instalar ManimCE/LaTeX/Chromium en el entorno de medición.
No lo ejecuto sin tu autorización explícita (y sin definir dónde: este contenedor no refleja el hardware de producción).
