# Autodesk Inventor — operaciones misceláneas, videos dedicados PQH

Paquete de **8 videos independientes**, uno por operación, derivado de `Inventor_Misc_Operations_3D_V2_PQH.py` y rediseñado como una simulación didáctica **inspirada en Autodesk Inventor Professional 2026**.

## Cambio visual

La versión anterior funcionaba como una presentación 3D con paleta azul/cian/verde. Esta versión cambia la gramática visual para aproximarse al entorno de trabajo de Inventor:

- barra de título oscura;
- Ribbon con pestaña `3D Model`;
- comandos organizados en `Create`, `Modify` y `Pattern`;
- Model Browser a la izquierda;
- Property Panel de la herramienta a la derecha;
- ViewCube y barra de estado;
- sólido principal gris/acero;
- croquis azul;
- selección y comando activo en naranja;
- preview paramétrico en verde sobrio.

No es una copia píxel por píxel de la interfaz propietaria. Reproduce su **arquitectura de interacción** para fines de explicación técnica.

## Videos / códigos

| # | Archivo | Escena | Operación |
|---|---|---|---|
| 01 | `01_fillet_redondeo.py` | `InventorFilletDetailed` | Redondeo / Fillet |
| 02 | `02_chamfer_chaflan.py` | `InventorChamferDetailed` | Chaflán / Chamfer |
| 03 | `03_mirror_simetria.py` | `InventorMirrorDetailed` | Simetría / Mirror |
| 04 | `04_rib_nervio.py` | `InventorRibDetailed` | Nervio / Rib |
| 05 | `05_emboss_repujado.py` | `InventorEmbossDetailed` | Repujado / Emboss |
| 06 | `06_coil_bobina.py` | `InventorCoilDetailed` | Bobina / Coil |
| 07 | `07_rectangular_pattern_lineal.py` | `InventorRectPatternDetailed` | Patrón lineal / Rectangular Pattern |
| 08 | `08_circular_pattern.py` | `InventorCircularPatternDetailed` | Patrón circular / Circular Pattern |

## Secuencia didáctica de cada video

1. Identificar la geometría y la dependencia del feature.
2. Activar la herramienta en `3D Model`.
3. Seleccionar las referencias necesarias.
4. Definir parámetros numéricos explícitos.
5. Revisar la vista previa antes de crear la operación.
6. Confirmar con `OK` y leer el nuevo feature en el Browser.

## QA y render

Cada escena pasa por:

- `python -m py_compile`;
- render de humo literal `-pql`;
- render final literal `-pqh`;
- 1920×1080, 30 fps;
- H.264 / yuv420p;
- `ffprobe` de resolución, fps, codec y duración;
- decodificación completa con FFmpeg;
- seis frames de auditoría distribuidos en el video;
- SHA-256 del MP4 y fuentes.

El workflow usa una **matriz de 8 jobs en paralelo** y luego crea un ZIP maestro con todos los videos, códigos, paquetes individuales y evidencias de QA.
