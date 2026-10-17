# bonemotion v1: librería de animación de esqueletos y demo a 60 fps

Esta entrega tiene dos partes:

- una librería profesional de movimiento: `source/bonemotion`, documentada en su `README.md`;
- un demo de cada animación, en `demos/`, más el reel completo.

## Qué cambió respecto de la animación anterior

- **De pie.** Todos los lanzamientos y la honda se hacen de pie. Ya no hay nada acostado.
- **Armado desde el piso.** 191 piezas (171 huesos y 20 dientes) suben una por una, de los pies al cráneo, en parábolas reales con la misma gravedad. Al encajar hay un pequeño retroceso, sin saltos de velocidad.
- **Movimientos a lo Chaplin.**
  - Caminata con pies hacia fuera, rodillas firmes, cadera que se mece y bastón de hueso.
  - Saludo con el sombrero.
  - Sombrero al aire.
  - Reverencia.
  - Giro en un pie.
- **Principios de animación en cada movimiento.** Preparación, anticipación, ejecución, proyección y asentamiento, con velocidad continua entre fases. Una barra en pantalla muestra la fase activa.
- **Fluidez.** 60 fps "en unos": una pose nueva en cada fotograma. Antes eran 15 dibujos por segundo. La tinta "hierve" a 12 por segundo para conservar el dibujo a mano.
- **Lanzamientos orgánicos.** Siguen la cadena cinética: piernas, cadera, tronco y brazo. El cuerpo llega a su pico con velocidad cero al soltar, así que la velocidad de salida es exacta: 3,5 m/s hacia arriba, 5,0 m/s hacia abajo, 4,0 m/s con la honda.
- **Red neuronal.** Un intercalador aprendido, entrenado con los propios movimientos de la librería. En huecos de 40 fotogramas reduce el error unas tres veces respecto de la interpolación cúbica.
- **Se adapta a otros personajes.** Pino, un maniquí con otras proporciones, ejecuta los mismos clips sin tocar su código.

## Archivos

| Archivo | Qué es |
|---|---|
| `bonemotion_demo_reel_1080p60.mp4` | Reel completo, 1920×1080 a 60 fps, CRF 22 (copia para GitHub). |
| `bonemotion_demo_reel_1080p60_share.mp4` | Copia para compartir, codificada en dos pasadas, menos de 30 MB. |
| `demos/01…14_*.mp4` | Un demo por animación, cortado al fotograma exacto, con sonido. |
| `qa/` | Calidad del video, de la animación y de la red neuronal, y hoja de contactos. |
| `source/bonemotion` | Código de la librería, con sus pesos, herramientas, entrenamiento y README. |
| `source/bonemotion-demo` | Código del demo. Las fuentes no van incluidas: son Noto Serif. |

Los 14 demos:

1. Armado desde el piso
2. Saludo con el sombrero
3. Sombrero al aire
4. Caminata a lo Chaplin
5. Giro en un pie
6. Reverencia
7. Salto vertical
8. Soltar desde el reposo
9. Lanzamiento hacia arriba
10. Lanzamiento hacia abajo
11. Honda con su propio brazo
12. Giro con momento angular
13. Otro personaje, mismo código
14. Transiciones aprendidas

## QA

Todo pasa.

- **Animación** (`qa/motion_qa.json`, 12 clips y 3 aplicados a Pino, muestreo a 240 Hz):
  - Cinemática inversa sin topes duros, ningún pie bajo el suelo, sin patinaje.
  - Aceleraciones acotadas; codos y rodillas dentro de rango.
  - Fases completas y anticipación medida.
  - Física: vuelos con error < 1e-6 u, velocidades de suelta exactas por ambos lados, radio de la honda constante, L = I·ω constante.
- **Red neuronal** (`qa/neural_report.json` y `qa/neural_qa.json`):
  - En la prueba: 1,67 cm frente a 4,75 cm de la Hermite y 6,89 cm de la lineal con N = 40; 0,96 cm frente a 2,99 cm con N = 30.
  - El pase hacia delante en JS coincide con numpy con un error relativo de 1,7e-7.
- **Video**:
  - 6051 fotogramas a 60 fps.
  - −16,2 LUFS, pico verdadero −1,9 dBTP.
  - 29 sonidos sincronizados dentro de ±3 ms.
  - 14 demos con conteo de fotogramas exacto.
