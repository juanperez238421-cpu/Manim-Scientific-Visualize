# Autodesk Inventor — operaciones misceláneas, videos dedicados 2D -> 3D PQH

Paquete de **8 videos independientes**, uno por operación, derivado de `Inventor_Misc_Operations_3D_V2_PQH.py` y rediseñado como una simulación didáctica **inspirada en Autodesk Inventor Professional 2026**.

## Contrato pedagógico FINAL

Cada video debe comenzar desde la lógica real de modelado paramétrico y no desde una pieza 3D ya terminada:

1. seleccionar el plano de trabajo (`XY`, `XZ`, `YZ` o cara existente);
2. entrar a **Start 2D Sketch**;
3. dibujar el perfil o geometría semilla;
4. aplicar cotas y restricciones geométricas hasta dejar clara la intención de diseño;
5. usar **Finish Sketch**;
6. convertir el croquis en volumen o feature 3D base;
7. seleccionar referencias 3D para la operación dedicada;
8. abrir la herramienta correspondiente desde `3D Model`;
9. definir parámetros numéricos explícitos;
10. inspeccionar la vista previa;
11. confirmar con `OK`;
12. comprobar el feature creado en el **Model Browser**;
13. terminar con una órbita 3D que muestre el resultado desde diferentes ángulos.

## Sistema visual

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

| # | Archivo | Escena | Operación | Flujo 2D -> 3D |
|---|---|---|---|---|
| 01 | `01_fillet_redondeo.py` | `InventorFilletDetailed` | Redondeo / Fillet | Rectángulo acotado -> Extrusion1 -> Edge -> Fillet R=8 mm |
| 02 | `02_chamfer_chaflan.py` | `InventorChamferDetailed` | Chaflán / Chamfer | Rectángulo acotado -> Extrusion1 -> Edge -> 6 mm + 45° |
| 03 | `03_mirror_simetria.py` | `InventorMirrorDetailed` | Simetría / Mirror | Media pieza -> Extrusion1/features -> YZ Plane -> Mirror |
| 04 | `04_rib_nervio.py` | `InventorRibDetailed` | Nervio / Rib | Base -> Extrusion1 -> línea abierta Sketch2 -> Rib 6 mm |
| 05 | `05_emboss_repujado.py` | `InventorEmbossDetailed` | Repujado / Emboss | Placa -> Extrusion1 -> Sketch2 cerrado -> Emboss 3 mm |
| 06 | `06_coil_bobina.py` | `InventorCoilDetailed` | Bobina / Coil | Perfil circular + Centerline -> Coil -> Pitch 12 mm / 4 rev |
| 07 | `07_rectangular_pattern_lineal.py` | `InventorRectPatternDetailed` | Patrón lineal | Placa -> semilla Sketch2/Extrusion2 -> 4 x 35 mm |
| 08 | `08_circular_pattern.py` | `InventorCircularPatternDetailed` | Patrón circular | Disco Ø80 -> semilla radial -> Z Axis -> 8 x 360° |

## QA y render

Cada escena pasa por:

- `python -m py_compile` de escena y librerías compartidas;
- render de humo literal `-pql`;
- render final literal `-pqh`;
- 1920×1080, 30 fps;
- H.264 / yuv420p;
- `ffprobe` de resolución, fps, codec y duración;
- decodificación completa con FFmpeg;
- nueve frames de auditoría distribuidos en el video;
- SHA-256 del MP4 y fuentes.

El renderer FINAL usa una **matriz de 8 operaciones con hasta 4 renders simultáneos** para reducir presión de runners manteniendo ejecución paralela. Después crea un ZIP maestro con los ocho videos PQH, los ocho códigos, las dos librerías compartidas, paquetes individuales y evidencia de QA.

## Salida final esperada

`Inventor_Professional_2D_to_3D_8Tools_FULL_PQH_20260826.zip`

Render generation: 2026-08-26 FINAL 2D-to-3D trigger.
