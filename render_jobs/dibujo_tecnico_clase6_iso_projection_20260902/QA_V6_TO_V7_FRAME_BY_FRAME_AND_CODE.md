# QA TOTAL — V6 → V7 · Sistema diédrico / objeto 3D a vistas 2D

Fecha: 2026-09-07  
Fuente auditada: `Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V6_FULL_TOTAL_FINAL_pqh.mp4`  
Código auditado: `Dibujo_Tecnico_3D_to_2D_Orthographic_Projection_V6_FULL_TOTAL.py`

## 1. Auditoría del render V6

Metadatos verificados sobre el MP4 entregado:

- 1920×1080
- 30.0018 fps
- 1632 frames
- 54.397 s

Se recorrieron los 1632 frames y además se revisaron contactos visuales por intervalos de 0.5 s, 1 s y 2 s.

### Hallazgos por intervalo

| Tiempo V6 | Hallazgo | Severidad | Corrección V7 |
|---|---|---:|---|
| 0–7 s | El sólido ocupa una fracción muy pequeña del lienzo. La cámara mira al origen, mientras el objeto vive principalmente en `y>0`, `z>0`. | Alta | `frame_center` se mueve al centro real de la geometría y el zoom aumenta. |
| 0–54 s | Título + subtítulo permanecen fijos todo el video y consumen altura útil durante la construcción. | Alta | El título solo existe en la introducción; se retira antes de proyectar. |
| 7–13 s | PV/PH/PL aparecen alrededor de un objeto demasiado pequeño; los planos dominan el cuadro. | Alta | Planos más compactos y sólido mucho mayor. |
| 13–25 s | Las proyectantes son correctas, pero el movimiento es rápido y el resultado proyectado queda pequeño. | Alta | Rayos más largos, `Create` más lento, resaltado y pausa de 1.45 s tras cada vista. |
| 25–31 s | El abatimiento es geométricamente correcto pero la lectura es pequeña y centrada en exceso. | Media/Alta | Abatimiento a 3.0 s, cámara recentrada y zoom 1.10 para la lectura plana. |
| 31–36 s | Alzado/planta y guías de alineación se ven pequeños frente al área vacía disponible. | Alta | Vistas ampliadas y seis guías verticales asociadas a cambios geométricos reales. |
| 36–41 s | La transición a hoja 2D deja un mini sólido muy pequeño a la izquierda y tres tarjetas pequeñas. | Alta | Se elimina el mini sólido; las tres vistas pasan a paneles grandes que ocupan casi todo el 16:9. |
| 42–49 s | El método está correctamente planteado pero demasiado pequeño. | Alta | Cinco barras de ancho 11.8 unidades, reveladas una por una. |
| 44.5–47.5 s | BUG visual: `Indicate(c[0], color=INK)` convierte temporalmente el relleno blanco de las tarjetas en gris/negro y oculta el texto. | Crítica | Se elimina ese `Indicate`; V7 usa `Circumscribe` sobre el borde sin alterar el relleno. |
| 50–54 s | Síntesis correcta, pero hereda el título persistente y deja sensación de diapositiva. | Media | Cierre independiente, grande y limpio. |

## 2. Auditoría de espacio y proporción

El problema principal de V6 no es la resolución sino el uso del sistema de coordenadas.

### Causas de código

1. `zoom=0.79` en una cámara centrada en el origen.
2. El sólido V5 heredado mide solo `2.90 × 1.40 × 1.55` aproximadamente.
3. El sólido está desplazado a `y≈1.25`, `z≈1.4`, pero el `frame_center` no acompaña ese desplazamiento.
4. Los planos tienen ancho `6.45`, por lo que el encuadre se diseña para los planos, no para el objeto.
5. Las vistas finales se generan con escala `0.72` dentro de tarjetas `3.35 × 2.35`.
6. El recordatorio 3D se reduce adicionalmente con `.scale(0.62)`.

### Corrección geométrica V7

V7 usa un sólido escalonado de tres niveles:

- Base: `x[-2.30,2.30]`, `y[0.75,3.05]`, `z[0.35,1.05]`
- Nivel medio: `x[-1.70,0.85]`, `y[1.00,2.72]`, `z[1.05,1.85]`
- Nivel superior: `x[-1.25,-0.15]`, `y[1.28,2.34]`, `z[1.85,2.75]`

Esto produce tres vistas inequívocamente distintas:

- **Alzado:** perfil escalonado de tres alturas.
- **Planta:** huella exterior + dos huellas interiores desplazadas.
- **Perfil derecho:** escalonado en profundidad y altura.

La cámara inicia con `zoom≈1.06` y `frame_center≈[0,1.85,1.48]`, es decir, enfoca la geometría y no el origen matemático.

## 3. Auditoría línea por línea del V6

### Bloque de cámara
- Correcto técnicamente.
- Incorrecto compositivamente: `zoom=0.79` y ausencia de `frame_center` generan exceso de blanco.

### Bloque de título
- Tipografía legible.
- Persistencia durante toda la escena reduce el área pedagógica.
- V7 lo limita a la introducción.

### `make_solid()` heredado
- Coherente dimensionalmente.
- Demasiado simple para enseñar 3D→2D.
- Dos cajas producen una lectura tipo icono.
- V7 lo reemplaza por tres volúmenes escalonados coherentes.

### `front_outline`, `top_outline`, `right_outline`
- Concepto correcto.
- La geometría es demasiado sencilla y el perfil lateral aporta poca información nueva.
- V7 deriva los tres contornos de un modelo más expresivo.

### Planos PV/PH/PL
- Correctos en orientación.
- Dimensiones excesivas respecto del objeto.
- V7 reduce el dominio y agranda el objeto.

### Proyectantes
- Correctas y ortogonales.
- Demasiado rápidas para clase.
- V7 aumenta duración, cantidad de vértices relevantes y pausa de lectura.

### Abatimiento
- Correcto: PH y planta giran juntos 90° sobre LT.
- V7 conserva exactamente esta lógica y aumenta la duración.

### Hoja final
- Escalas `0.72` + tarjetas pequeñas desperdician el lienzo.
- `mini_solid.scale(0.62)` agrava el problema.
- V7 elimina el thumbnail y usa paneles grandes.

### Método de 5 pasos
- Contenido pedagógico correcto.
- Disposición 3×2 demasiado compacta.
- `Indicate(c[0], color=INK)` es el fallo visual más evidente del render V6.
- V7 usa 5 barras horizontales, una por paso, con `Circumscribe`.

## 4. Criterios de aceptación V7

El render V7 no se considera final hasta superar:

1. `py_compile`.
2. Render completo PQL de toda la línea temporal.
3. Render literal `-pqh` 1920×1080 / 30 fps.
4. Decodificación completa con PyAV.
5. Duración > 60 s.
6. Auditoría automática de ocupación del encuadre.
7. 96 frames distribuidos uniformemente para contacto visual.
8. Verificación de ausencia del patrón V6 `Indicate(c[0], color=INK)`.
9. Publicación del MP4 exacto en `published_renders/`.
10. Re-descarga directa desde GitHub y verificación SHA-256 usando Python, no `curl`.

## 5. Objetivo pedagógico conservado

La secuencia conceptual sigue siendo:

**OBJETO 3D → DIRECCIÓN DE OBSERVACIÓN → PLANO → PROYECTANTES ORTOGONALES → VISTA 2D → ABATIMIENTO → ALINEACIÓN**

La revisión V7 modifica escala, forma, ritmo, composición y QA, pero no reemplaza el concepto de sistema diédrico.
