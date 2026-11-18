# Instituto Jorge Robledo · Geometría 8° · 2027 P1, Semana 01 · Auditoría V1 → V2

## Veredicto

**PASS** — videos V2 renderizados, verificados y publicados, después de correcciones de contenido, legibilidad, cinemática de animación y colisiones visuales detectadas.

**Ejecución final verificada:** https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/runs/44211121750 (conclusión: success).

## 1. Trazabilidad: el cronograma REAL prevalece sobre una inferencia

Fuente primaria revisada íntegramente: archivo adjunto del usuario **`Geometry_8_2027_P1.docx`** (sección `CLASS PLANNER / 2027 / Grade 8th / Week 1`). Fecha institucional: **19–22 January 2027**, martes a viernes, primer período. Eje: **Foundations of Euclidean Geometry**.

La semana 1 define exactamente dos secuencias:

**Clase 1:** `Course induction and geometric objects`. Establecer convenciones de cuaderno y dibujo; distinguir **point, line, segment, ray, plane**; rotular un diagrama y explicar sus diferencias. Estrategia de acceso: tarjetas de vocabulario, diagramas rotulados, modelado breve, clasificación colaborativa y retroalimentación oral inmediata.

**Clase 2:** `Sets and logical diagrams`. Modelar clasificaciones geométricas mediante conjuntos y **diagramas de dos círculos**; ordenar las representaciones por dimensiones y justificar ubicación/membresía/intersección.

La malla institucional `malla curricular - geometría 8° (2026).docx`, Periodo I, confirma los ejes de conceptos geométricos y conjuntos; aquí **no sustituye** la asignación por clase que sí define el documento 2027.

### Límites de semanas posteriores confirmados en el mismo 2027
- Semana 2 (25–29 enero): rectas y planos, relaciones paralelas, perpendiculares, secantes y coincidentes.
- Semana 3 (1–5 febrero): construcciones con regla y compás, bisectriz perpendicular y precisión.
- Semana 4 (8–12 febrero): elementos, clasificación y medición de ángulos.

No se anticipan estos procedimientos en los videos de semana 1. La planeación enumera **clase 1 y clase 2**, pero **no asigna cada clase a días específicos por grupo**; tales días no se inventan.

## 2. Auditoría V1 vs V2

| Hallazgo V1 | Reparación V2 | Evidencia |
|---|---|---|
| Inducción del curso y convenciones de cuaderno omitidas | Cuaderno animado de fecha, regla, extremos A/B y tarea de copia | Clase 1, fase 01 |
| Punto dibujado de forma estática | Punto matemático de posición nula que se desplaza con un tracker; la marca visible se declara símbolo | Clase 1, fase 02 |
| Recta/rayo/segmento con tamaño reducido | Trazados amplios de hasta 8 unidades Manim, flechas y marcadores A/B geométricamente coherentes | Clase 1, fase 03 |
| Plano insuficiente; representación finita confundible con objeto ideal | Plano extendido con símbolo α, puntos A/B/C no colineales; se explica que el borde es convención gráfica | Clase 1, fase 04 |
| Poca notación formal | Símbolos distintos `AB` con barra, flecha sencilla y flecha doble | Clase 1, fase 05 |
| Clase 2 no iniciaba por clasificación dimensional indicada en 2027 | Secuencia 0D–3D, distinguiendo objeto y representación 2D | Clase 2, fase 01 |
| Venn estático y de escala reducida | Cuatro figuras con relleno de color, animación de desplazamiento a regiones y pausas de observación | Clase 2, fases 02–03 |
| Intersección, unión y justificación mayormente estáticas | Lente de intersección reconstruida por arcos de circunferencia, coloreado de unión e indicación animada | Clase 2, fases 04–06 |
| Texto lateral excedía margen durante preview | `fit_to_safe_area()` con desplazamiento y límite interior verificable | QA: PQL |
| Fórmula de pertenencia interfería con el borde inferior del Venn | Anotación desplazada a la derecha del diagrama y separada de sus regiones | 32 capturas finales |
| Leyendas inferiores pequeñas | Texto de captions CAD a 29 pt y superficie de fondo ampliada | V2 final |
| Pausas cortas | Aumento de esperas y transiciones continuas; respetar el ritmo de lectura del aula | Duración validada |

## 3. Invariantes matemáticos inspeccionados

1. Punto 0D: solo una localización matemática; el disco dibujado representa una ubicación, no un área del punto.
2. Recta: se prolonga en ambas direcciones sin extremos; semirrecta: un origen A; segmento: extremos A y B.
3. Plano ideal: infinito y bidimensional; el polígono es una representación finita, no el límite real del plano.
4. Figura 3D: el cubo mostrado en pantalla es una representación bidimensional de un objeto tridimensional.
5. Conjuntos `A={triángulos}`, `B={figuras azules}`. Verde triángulo solo A; azul triángulo A∩B; azul cuadrado solo B; gris cuadrado afuera de ambos.
6. `|A|=2`, `|B|=2`, `|A∩B|=1`, `|A∪B|=2+2−1=3`. Los símbolos reflejan la misma colección a lo largo de las escenas.

## 4. QA final reproducible

| Parámetro | Clase 1 | Clase 2 |
|---|---:|---:|
| Archivo | `Geometry8_2027_Week01_V2_Class01_Foundations_MOTION_FINAL_pqh.mp4` | `Geometry8_2027_Week01_V2_Class02_Sets_MOTION_FINAL_pqh.mp4` |
| Duración total | 197.632682 s (3:17.63) | 208.499349 s (3:28.50) |
| Tamaño | 7,553,187 bytes | 8,345,340 bytes |
| Códec | H.264 | H.264 |
| Resolución | 1920 × 1080 | 1920 × 1080 |
| Velocidad | 30 fps | 30 fps |
| Formato de píxel | yuv420p | yuv420p |
| Compilación Python | PASS | PASS |
| Render completo ManimCE `-pql` | PASS | PASS |
| Render final ManimCE `-pqh` | PASS | PASS |
| FFprobe y decodificación completa FFmpeg | PASS | PASS |
| Muestreo real completo de imágenes | 16/16 PASS | 16/16 PASS |
| SHA-256 | `2b22b066a01f823981e1584adcedfffd8fe0c376a19079ebdf5a049460de43b7` | `3fe8795fdd48550197a76cdc3221509f043af13592e91916e835de3ce45581cb` |

**Inspección visual manual:** se revisaron las dos hojas de contacto finales 4 × 4, es decir, 32 frames reales del render final. Se confirmó escudo institucional PNG, fecha/título Week 01, HUD, diagramas/figuras ampliadas, distribución de etiquetas y desplazamiento de la fórmula de pertenencia sin colisión. Algunas capturas muestran procesos de `Write` o un inicio de escena de forma incompleta **por estar tomadas durante la animación**; el archivo entero se decodificó correctamente.

La inspección visual es **por muestreo**: no constituye una prueba matemática de cero superposiciones en cada uno de los miles de cuadros.

## 5. Recursos reales (ningún enlace estimado)

- **Clase 1:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_Class01_Foundations_MOTION_FINAL_pqh.mp4
- **Clase 2:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_Class02_Sets_MOTION_FINAL_pqh.mp4
- **16 fotogramas clase 1:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_Class01_contact.jpg
- **16 fotogramas clase 2:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_Class02_contact.jpg
- **FFprobe ledger:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_QA.tsv
- **SHA-256 ledger:** https://raw.githubusercontent.com/juanperez238421-cpu/Manim-Scientific-Visualize/geometry8-2027-week01-v2-curriculum-motion-qa/published_renders/Geometry8_2027_Week01_V2_SHA256SUMS.txt
- **QA full artifact (GitHub Actions):** https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/actions/runs/44211121750
- **Source:** https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/blob/geometry8-2027-week01-v2-curriculum-motion-qa/lessons/geometry8_2027/week01/geometry8_week01_cad_v2.py
- **Pull request:** https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize/pull/183

Original V1 remains published separately for side-by-side comparison. V2 changes are versioned in a separate branch. The captions and original school crest are part of the rendered MP4, not simulated download placeholders.
