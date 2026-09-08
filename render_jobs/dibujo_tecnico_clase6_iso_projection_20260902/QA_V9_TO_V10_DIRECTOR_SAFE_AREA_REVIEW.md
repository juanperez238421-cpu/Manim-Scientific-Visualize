# QA V9 → V10 · composición vertical + safe-area director review

## 1. Qué corrigió V9 correctamente

V8 tenía el núcleo 3D demasiado bajo: en ventanas centrales de la explicación el centro vertical robusto estaba alrededor de y≈738 px en una escena 1080p (centro geométrico y=540). V9 introdujo un desplazamiento real de cámara y superó el gate automático de composición vertical:

- `median_main_cy = 646.5 px`
- `p90_main_cy = 649.5 px`
- `median_main_y1 = 891.47 px`
- `p10_main_y0 = 369 px`

Esto confirmó que el conjunto 3D sí subió respecto de V8.

## 2. Hallazgos de la revisión manual posterior al render V9

La auditoría visual de fotogramas completos detectó tres defectos que la métrica global no podía identificar por sí sola:

1. **Abatimiento alrededor de 60 s:** durante la transición oblicua de PH, el plano abatido crecía hacia el borde inferior y parte de la geometría salía del encuadre antes de que la cámara llegara a la vista ortogonal final.
2. **Hoja 2D alrededor de 75 s:** el título `UN OBJETO · TRES DESCRIPCIONES 2D` y la tarjeta `TOP / PLANTA` se superponían. El origen fue aplicar un `UP` global a las tarjetas sin recalcular el layout vertical del bloque completo.
3. **Síntesis final alrededor de 90 s:** era legible, pero aún tenía demasiado peso visual en la mitad inferior para el criterio solicitado de composición superior después de la portada.

Por tanto V9 no se considera la entrega final, aunque su pipeline automático haya pasado.

## 3. Correcciones V10

V10 conserva el desplazamiento 3D validado de V9 y añade correcciones director-level específicas:

- `FOLD_EXTRA_UPSHIFT = 1.20`: antes del abatimiento de PH se mueve la cámara a un `fold_center` superior y se reduce ligeramente el zoom a 0.94; la rotación completa debe permanecer visible de inicio a fin.
- Hoja 2D con **coordenadas explícitas de safe area**, no un `shift(UP)` ciego:
  - título y=3.72;
  - `TOP / PLANTA` y=1.82 con panel 4.85×2.20;
  - `FRONT / ALZADO` y=−1.05 con panel 4.85×2.55;
  - `RIGHT / PERFIL` y=−1.05 con panel 3.00×2.55.
- `FINAL_UPSHIFT = 1.20`: la síntesis final tiene su propio desplazamiento superior, separado del método y de la hoja 2D.
- Se mantienen `CAMERA_Z_UPSHIFT = 1.55`, `CHIP_UPSHIFT = 0.75` y las pausas/transiciones de V9.

## 4. Gates V10

La nueva ejecución debe validar:

- H.264, yuv420p, 1920×1080, ~30 fps;
- decodificación completa;
- duración > 90 s y > 2700 frames;
- auditoría de ocupación de toda la línea de tiempo;
- auditoría vertical 3D con `median_main_cy < 660`;
- auditoría de borde superior/inferior después de portada, sin contacto persistente con los primeros/últimos píxeles;
- ventana del abatimiento con borde inferior robusto dentro de safe area;
- ventana de hoja 2D sin contenido tocando el borde superior y con suficiente separación vertical;
- síntesis final con centro robusto por encima del centro de V9;
- 120 fotogramas distribuidos uniformemente para revisión visual manual final.

## 5. Criterio de aceptación manual

No se publica V10 como entrega final hasta revisar el contact sheet y fotogramas individuales de: 15 s, 25 s, 45 s, 58–64 s, 74–78 s, método y síntesis final. El gate automático es necesario, pero no reemplaza el QA visual de composición.