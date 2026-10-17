# bonemotion

Una librería de animación de personajes. Empieza por el esqueleto de Mr. Bones, aplicado a la física, y sirve para cualquier bípedo. Cada personaje después tendrá sus propias animaciones según el concepto o la temática.

Hay tres ideas de fondo:

1. **Los principios de animación se escriben como código.** Un movimiento se construye por fases: preparación, anticipación, ejecución, proyección y asentamiento. La velocidad es continua entre fases.
2. **La física la decide la física.** Vuelos, lanzamientos, honda, atrapadas, saltos y giros salen de fórmulas cerradas. El QA compara lo dibujado con la fórmula hasta el error de redondeo.
3. **El movimiento se adapta al cuerpo.** Ningún clip guarda posiciones fijas: todo se calcula con las proporciones del personaje (`profile.dims`). El mismo código mueve a Mr. Bones (171 huesos, 1,77 m) y a Pino, un maniquí de 16 piezas y 1,33 m.

```
src/
  core/        curvas, principios, física, cuerpo, pose     (sin personaje, sin DOM)
  clips/       locomoción, Chaplin, armado, lanzamientos, honda, salto, giro
  characters/  mrbones/ (rig de 171 huesos)  ·  mannequin/ (Pino)
  neural/      rasgos de pose + red de intercalado aprendida (+ pesos)
  render/      tinta, película, reloj (estilo de los años 30)
tools/         make_dataset.mjs · qa_motion.mjs · qa_neural.mjs
train/         train_inbetween.py (numpy, determinista)
qa/            motion_qa.json · neural_report.json · neural_qa.json
```

## 1. Núcleo

### Curvas (`core/curves.js`)

- **`track(keys)`**: canal con fotogramas clave (escalar o vector), C1.
  - Tangentes Catmull-Rom limitadas: Fritsch-Carlson, sin pasarse de las claves.
  - Modos `flat`, `free`, `linear` y `step`.
  - **Pendiente explícita** (`slope`): así se fija la velocidad exacta de una suelta o de un despegue.
- **`arcPoint(a, b, bulge, u)`**: movimiento en arco. Las líneas rectas se ven mecánicas.
- **`smin`**: mínimo suave. Limita la altura de la cadera sin que la rodilla "salte".

### Principios (`core/principles.js`)

**`action({...})`** es la envolvente canónica de una acción. `u = 0` es el reposo y `u = 1` la meta:

| Fase | Qué hace `u` | Cómo se construye |
|---|---|---|
| Preparación | espera en 0 mientras otros canales se colocan | — |
| Anticipación | va al lado contrario (`u < 0`), entrando lento | curva suave |
| *Moving hold* | el extremo se sostiene pero deriva un poco | sigue vivo |
| Ejecución | acelera hasta el golpe | Hermite monótona; velocidad de golpe explícita (`vHit`) |
| Proyección | la inercia la pasa de la meta (`u > 1`) | desaceleración constante (parábola) |
| Asentamiento | resorte amortiguado de vuelta a 1 | velocidad inicial cero |

Otras herramientas del módulo:

- **Acción superpuesta**: `delayed` (romper articulaciones en sucesión) y `springFollow` (arrastre con resorte integrado a dt fijo).
- **`window`** y **`springStep`**: el resorte amortiguado en forma cerrada.

### Física (`core/physics.js`)

Unidades: `u` (unidades del rig) y segundos. Cada personaje define `K` (u por metro) y `g = 9,81·K`.

- **`projectile`** y **`launchVelocity`**: vuelo libre exacto, y la velocidad que lleva de P0 a P1 en un tiempo T.
- **`bouncing`**: rebotes con restitución.
- **`swingSchedule`**: brazo con aceleración angular constante desde el reposo que llega exactamente a ω en el ángulo de suelta.
- **`slingSchedule`**: honda (α constante, luego ω constante; suelta en un ángulo exacto módulo 2π).
- **`catchAbsorb`**: atrapar cediendo, con fuerza constante sobre una distancia.
- **`pendulum`**: péndulo físico con RK4.
- **`spinConserving`**: momento angular constante, ω(t) = L / I(t).

### Cuerpo y pose (`core/body.js`, `core/pose.js`)

- **La pose** es datos planos: raíz, columna, cuello, cabeza, cintura escapular, piernas (tobillo en el mundo, rumbo, cabeceo, dedos) y brazos (objetivos por espacio: mundo, pecho, pelvis o cabeza).
- Se puede **mezclar** (`mix`), **sumar en capas** (`addLayer`) y **reflejar** (`mirror`).
- **`ankleFromPivot`**: rueda el pie sin deslizar alrededor del talón o de la bola.
- **`reachHeight`**: limita la altura de la cadera según el alcance de la pierna.

## 2. Clips (`clips/`)

Cada clip es `build(personaje, parámetros)` y devuelve `{ duration, poseAt(t), phases, events, impulses }`. Los clips son funciones puras del tiempo: se puede pedir cualquier fotograma, en cualquier orden.

| Clip | Qué muestra |
|---|---|
| `assemble` | 191 piezas (171 huesos y 20 dientes) suben del piso en parábolas reales, de los pies al cráneo. Retroceso al encajar, sin saltos de velocidad. Al final pisa el ala del sombrero, el sombrero voltea a la cabeza y saluda. |
| `hatTip` | La mano guía al sombrero (el objeto manda y la mano lo sigue). La cabeza llega 70 ms después. El sombrero se aplasta en la anticipación. |
| `hatFlip` | El sombrero sale de la mano con la velocidad y el giro exactos, da una vuelta libre y cae en la cabeza. |
| `chaplinWalk` | Marcha procedural (contacto, bajada, paso, subida) con pies hacia fuera, rodillas firmes y cadera que se mece. El talón da un latigazo hacia fuera. El bastón de hueso apoya la punta sin deslizar y hace un molinete cada dos zancadas. |
| `cornerHop` | El giro en un pie de Chaplin: la cabeza gira primero y da tres saltos balísticos sobre la bola del pie, que no se mueve. |
| `doffBow` | Reverencia: la cadera va atrás para mantener el centro de masa sobre los pies. El pie retrocede rodando sobre la bola. La cabeza sube al final. |
| `jump` | Agacharse, impulsarse con los brazos, vuelo exacto de la pelvis y aterrizaje amortiguado con desaceleración constante. |
| `skullDrop` | Suelta con v₀ = 0 y vuelve a atraparlo más abajo, cediendo. Incluye quitarse la cabeza: el sombrero queda colgado en el aire un instante y luego cae al cuello. |
| `skullToss` | Cadena cinética de lo proximal a lo distal. La cadera y el tronco llegan a su pico con velocidad cero justo al soltar, así que v₀ = ωr es exacta. |
| `skullSlam` | Brazo por encima de la cabeza, rebote con restitución, se atrapa en el ápice (v = 0). La cabeza vuelve a su sitio. |
| `sling` | Se quita el brazo izquierdo con dos tirones, cuelga como péndulo y gira como honda. La mano guía con un pequeño círculo adelantado 90°, así el brazo rígido no se estira. Suelta con el radio horizontal (v vertical). El brazo vuelve y atrapa la cabeza; el brazo y la cabeza vuelven a su sitio. |
| `pirouette` | L = I·ω: I se calcula con los volúmenes de los huesos (12 kg en total). Brazos adentro: menos inercia, más velocidad. Termina mirando al frente, porque se ajusta ω₀ para dar vueltas enteras. |
| `gait(profile, {style})` | Marcha `neutral` o `chaplin`, o un estilo propio con unos 20 parámetros (cadencia, paso, ancho, pies hacia fuera, oscilaciones, contrarrotación, braceo...). |

**Los objetos mandan, las manos siguen.** El sombrero, el bastón y el cráneo se animan como objetos con contactos exactos. Los objetivos de la cinemática inversa de las manos salen de sus agarres. Cuando una mano viaja lejos, pasa por un punto delante del pecho (`armTo`/`armBlend`) en lugar de atravesar el hombro.

## 3. Personajes: cómo añadir uno nuevo

Un personaje implementa esta interfaz:

```js
{
  profile: { id, name, K, g, dims: { hipW, thigh, shin, legLen, ankleH, ballZ, heelZ, upper, fore, armLen,
             standH, chest, shoulder, footRestX, ... }, foot: { ball, heel }, limits },
  evaluatePose(pose, sec) -> { c, ev: { fr (marcos), J (articulaciones), flags.ik } },
  draw(ctx, ink, pose, ev, sec, view, drawIndex, opts),
  secondary(poseAt, { t0, t1 }) -> { at(t) },   // movimiento secundario (puede ser nulo)
  hatFrame?, toControls?, model?               // opcionales: accesorios, modelo de objetos rígidos
}
```

`characters/mannequin` es el ejemplo mínimo, de unas 120 líneas. Con eso, el salto, las dos marchas y el armado desde el piso funcionan sin tocar los clips. Las animaciones propias de cada personaje (su temática) se escriben como clips nuevos con las mismas piezas: `action`, `track`, la física, `gait` y la pose.

## 4. Red neuronal: intercalado aprendido (`neural/`)

**El problema.** Dados dos fotogramas clave separados por N fotogramas (entre 6 y 40, a 60 fps), inventar los fotogramas intermedios.

**Cómo funciona.**

- **Base**: una Hermite cúbica por canal, con tangentes tomadas de los fotogramas vecinos.
- **Red**: un MLP de 189 entradas, dos capas ocultas de 256 con ELU y 46 salidas (126.254 parámetros). Predice una corrección a esa base.
- **Ventana**: la corrección se multiplica por 4u(1−u), así que las dos claves se respetan siempre.
- **Entradas**: los cuatro fotogramas de contexto en el marco de la ventana (sin traslación ni rumbo), N y u.

**Datos.**

- 900 secuencias generadas con la propia librería y parámetros al azar: 263.173 poses.
- Separadas por secuencia: 616 de entrenamiento, 155 de validación y 129 de prueba.
- Entrenamiento con numpy, Adam y coseno, 60 épocas, con semilla fija.

**Resultados en la prueba (secuencias nunca vistas).** Error medio de posición sobre pelvis, tobillos y muñecas, en cm:

| Hueco | Lineal | Hermite | Red |
|---|---|---|---|
| N = 10 (0,17 s) | 1,07 | 0,30 | **0,30** |
| N = 20 (0,33 s) | 3,05 | 1,43 | **0,65** |
| N = 30 (0,50 s) | 4,96 | 2,99 | **0,96** |
| N = 40 (0,67 s) | 6,89 | 4,75 | **1,67** |

Con huecos largos la red reduce el error unas tres veces respecto de la Hermite. Con huecos cortos (N = 10) las dos empatan, porque ahí la cúbica ya acierta. En JS, la salida de la red coincide con la de numpy con un error relativo de 1,7e-7.

**Dónde se usa.** Sirve para transiciones y para rellenar huecos: el demo borra 40 fotogramas de una caminata nueva y la red los reinventa. La física nunca pasa por la red: vuelos, sueltas y contactos siguen siendo analíticos.

**Verificación** (`tools/qa_neural.mjs`):

- El pase hacia delante en JS (el que usa el renderizador) reproduce las métricas del entrenador.
- Las claves se mantienen.
- Para N ≥ 20 la red gana a la Hermite.

## 5. QA riguroso (`tools/qa_motion.mjs`, muestreo a 240 Hz)

Para cada clip, y para los clips reaplicados a Pino, se revisa:

- **Cinemática inversa**: cero "clamps" duros, con IK suave en brazos y piernas.
- **Suelo**: ningún punto del pie por debajo.
- **Patinaje**: los puntos apoyados no se deslizan; menos de 0,05 u por muestra.
- **Continuidad**: aceleraciones de pelvis, cabeza, muñecas y tobillos acotadas, salvo en impactos declarados.
- **Límites**: rodilla y codo dentro de rangos anatómicos.
- **Fases**: completas y en orden.
- **Anticipación medida**: el cuerpo de verdad va al revés antes de la acción.
- **Física**: vuelos exactos (error < 1e-6 u), velocidades de suelta exactas por ambos lados, radio de la honda constante, L = I·ω constante, gravedad de cada hueso del armado y de cada salto.

```bash
node packages/bonemotion/tools/qa_motion.mjs     # -> qa/motion_qa.json
node packages/bonemotion/tools/make_dataset.mjs  # corpus
.venv/bin/python packages/bonemotion/train/train_inbetween.py --epochs 60
node packages/bonemotion/tools/qa_neural.mjs     # -> qa/neural_qa.json
```

## 6. Fluidez

- Los clips se muestrean en tiempo continuo. El demo se renderiza a **60 fps "en unos"**: una pose nueva en cada fotograma.
- El trazo de tinta "hierve" a 12 dibujos por segundo, independiente del movimiento. Así se conserva la vida del dibujo a mano sin el tartamudeo de animar en dos.
- El movimiento secundario (mandíbula, sombrero, 24 costillas, coxis, dedos) se integra una vez por clip a 240 Hz y se interpola.
