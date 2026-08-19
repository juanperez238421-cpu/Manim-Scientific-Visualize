# Protocolo ITM para animaciones de croquis, extrusión y modelo CAD 3D

**Versión:** 3.0  
**Fecha:** 18 de agosto de 2026  
**Motor:** Manim Community Edition 0.20.1  
**Formato:** 16:9, 1920×1080, 30 fps, fondo blanco

## 1. Propósito

Este protocolo especializa el protocolo general PQH v8 para escenas que enseñan operaciones CAD. Su objetivo no es mostrar un sólido terminado de inmediato, sino hacer visible la relación causal entre una cara activa, un croquis 2D cerrado, una dirección, una distancia y el volumen resultante.

## 2. Gramática visual obligatoria

Cada operación CAD debe seguir este orden:

```text
CARA ACTIVA → CÁMARA NORMAL → CROQUIS CERRADO → DIRECCIÓN → DISTANCIA → RESULTADO 3D
```

No se inicia una extrusión antes de que el espectador pueda identificar el perfil que la genera.

### 2.1 Operación aditiva

1. Seleccionar una cara o plano.
2. Ubicar la cámara normal a esa cara.
3. Dibujar el perfil cerrado en azul.
4. Pausar para lectura.
5. Abandonar deliberadamente la vista ortogonal.
6. Mostrar crecimiento de profundidad en verde.
7. Conservar el sólido final y retirar el croquis auxiliar.

### 2.2 Operación sustractiva

1. Seleccionar la cara del sólido.
2. Ubicar la cámara normal a esa cara.
3. Dibujar el perfil cerrado en rojo.
4. Pausar para lectura.
5. Mostrar el volumen cortador atravesando la pared.
6. Sustituir la pared por piezas que preserven el vacío real.
7. Retirar perfil y cortador.

Manim no realiza CSG nativo en esta escena. Por eso, el corte se representa pedagógicamente con un volumen cortador y se consolida mediante una geometría de pared segmentada. El resultado debe contener el hueco, no una placa roja sobre la fachada.

## 3. Protocolo del croquis

- Todo perfil que se extruye debe ser cerrado.
- El contorno del croquis debe coincidir con la huella del sólido objetivo.
- Los muros se dibujan como rectángulos cerrados con espesor; no como líneas centrales abiertas.
- Las columnas se dibujan como cuadrados cerrados.
- La losa y la cubierta usan cuatro segmentos con cierre explícito.
- Azul (`#2878B5`) identifica geometría de croquis.
- Un relleno azul de baja opacidad puede reforzar la región sin ocultar la cara base.
- El croquis se dibuja con `Create`; cada explicación textual asociada se escribe con `Write`.

## 4. Protocolo de cámara

### 4.1 Plano horizontal XY

- Estado: `PLAN_2D`.
- `phi = 0°`, `theta = -90°`.
- Uso: losa, muros, columnas y cubierta.
- Debe existir una pausa de estabilización antes de dibujar.

### 4.2 Cara frontal XZ

- Estado: `FRONT_FACE_2D`.
- `phi = 90°`, `theta = -90°`.
- Uso: puerta y ventana.
- El perfil debe aparecer paralelo a la pantalla y sin perspectiva ambigua.

### 4.3 Vista de modelo

- Estado: `MODEL_3D`.
- Ángulos recomendados: `phi = 36°–66°`, `theta = -50°–-58°`.
- Uso: mostrar profundidad, dirección de extrusión y verificación espacial.
- Cada retorno a 3D debe ocurrir antes de que el volumen gane profundidad.

### 4.4 Órbita final

- Iniciar solo cuando el modelo esté completo.
- Velocidad baja (`≈0.085 rad/s`) y duración suficiente para inspección.
- Detener la cámara antes de presentar la síntesis final.

## 5. Portada institucional

- Usar el logotipo ITM como activo local.
- Mostrar institución, asignatura, grupo, tema y docente.
- Crear todo texto con `Tex` o `MathTex`.
- Animar cada bloque textual mediante `self.play(Write(...))`.
- Mantener el logotipo proporcional y sin deformación.
- No mezclar la portada con el HUD ni con geometría 3D.
- Entregar escenas separadas para `SEDTCAD22` y `DTR43` desde una base común.

## 6. Texto y notación

- Texto técnico: `Tex`.
- Expresiones matemáticas: `MathTex`.
- Animación textual: `self.play(Write(objeto))`.
- No usar `Text` en la escena entregable.
- Reemplazar símbolos Unicode frágiles por comandos LaTeX o equivalentes seguros.
- Título máximo recomendado: 30 pt en HUD y 48 pt en portada.
- Notas: 20 pt mínimo en Full HD.

## 7. Capas y transparencia

- Terreno: gris verdoso claro.
- Losa y cubierta: gris neutro.
- Columnas: gris oscuro.
- Muros exteriores: opacidad aproximada `0.38` para leer el interior.
- Muros interiores: opacidad aproximada `0.94`.
- Vidrio: azul claro, opacidad aproximada `0.42`.
- Extrusión positiva: verde.
- Extrusión negativa: rojo.

La transparencia debe servir a la lectura estructural. Nunca debe convertir los muros en masas visualmente confusas.

## 8. Ritmo pedagógico

- Micropausa: `0.65 s`.
- Pausa de construcción: `1.10 s`.
- Pausa de lectura: `1.75 s`.
- Pausa de explicación: `2.35 s`.
- Observación final de una operación: `2.80 s`.
- Órbita final: mínimo `6.5 s`.

No encadenar croquis y extrusión sin una pausa de lectura. Las operaciones exteriores e interiores deben separarse semánticamente.

## 9. Secuencia de la vivienda

1. Preparar terreno y retícula.
2. Dibujar croquis de losa.
3. Extruir losa.
4. Activar cara superior.
5. Dibujar perfiles cerrados de muros exteriores.
6. Dibujar perfiles cerrados de muros interiores.
7. Dibujar perfiles cerrados de columnas.
8. Extruir columnas.
9. Extruir muros exteriores.
10. Extruir muros interiores.
11. Crear corte de puerta.
12. Crear corte de ventana.
13. Dibujar y extruir cubierta.
14. Verificar con órbita.
15. Resumir la gramática CAD.

## 10. QA visual obligatorio

- Portada centrada, legible y específica del grupo.
- Logotipo dentro del marco seguro.
- Ningún texto superpuesto al HUD.
- Croquis de losa visible antes del espesor.
- Muros y columnas dibujados sobre la losa, no sobre el terreno.
- Perfiles de muro cerrados y con espesor visible.
- Cámara normal durante cada croquis.
- Dirección del cortador coherente con la normal de la fachada.
- Puerta y ventana con vacío final correcto.
- Cubierta creada después de muros y columnas.
- Órbita sin recortes en bordes.
- Resumen final legible durante al menos cinco segundos.

## 11. QA técnico obligatorio

```bash
python -m py_compile house_extrusion_itm.py validate_scene.py
python validate_scene.py
manim -pql house_extrusion_itm.py HouseExtrusionITM_SEDTCAD22 --disable_caching
manim -pql house_extrusion_itm.py HouseExtrusionITM_DTR43 --disable_caching
manim -pqh house_extrusion_itm.py HouseExtrusionITM_SEDTCAD22 --format=mp4 --disable_caching
manim -pqh house_extrusion_itm.py HouseExtrusionITM_DTR43 --format=mp4 --disable_caching
```

Aceptar cada MP4 final solo si `ffprobe` confirma H.264, 1920×1080, 30 fps y `yuv420p`; FFmpeg decodifica el archivo completo; los fotogramas de auditoría no muestran solapes o recortes; y existe una suma SHA-256.

