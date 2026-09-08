# QA V8 → V9 · revisión total de composición vertical

## Hallazgo principal

La geometría de V8 es correcta, pero la composición no lo es. El contenido 3D queda sistemáticamente demasiado abajo después de la portada. En un fotograma representativo alrededor de 20 s, el sistema PV/PH/PL y el sólido ocupan principalmente la mitad inferior de 1920×1080, dejando una franja blanca superior excesiva.

Esto no se corrige moviendo solamente los textos. La causa está en dos capas:

1. **Cámara 3D:** los `frame_center` heredados de V7 mantienen el centro geométrico correcto en coordenadas del mundo, pero visualmente proyectan el sistema demasiado bajo en la pantalla 16:9.
2. **Elementos fixed-in-frame:** los `section_chip()` se ubican con `to_edge(DOWN, buff=0.28)`, por lo que refuerzan aún más el peso visual de la zona inferior.

## Medición de la versión V8 publicada

Archivo revisado: `Diedrico_3D_to_2D_V8.mp4`.

- resolución: 1920×1080
- duración: 77.696 s
- frames: 2331
- auditoría independiente con OpenCV, 2 muestras/s
- umbral de contenido: gris < 235
- ROI principal para diagnóstico vertical: y=0..899 px

Mediana aproximada del centro vertical robusto del contenido principal:

| Ventana | centro y (px) |
|---|---:|
| 10–15 s | 703 |
| 15–20 s | 737 |
| 20–25 s | 738 |
| 25–30 s | 738 |
| 30–35 s | 738 |
| 35–40 s | 738 |
| 40–45 s | 732 |

En una imagen 1080p el centro geométrico de pantalla es y=540. Una mediana de ~738 px confirma el defecto: el núcleo de la explicación está alrededor de **198 px por debajo del centro**.

## Corrección V9

V9 introduce una política explícita de composición superior:

- portada como beat independiente: primero título, luego contenido;
- `CAMERA_Z_UPSHIFT = 1.55`: todos los `frame_center` 3D posteriores reducen su coordenada z en 1.55 unidades. Con phi≈64° esto desplaza el contenido proyectado claramente hacia arriba sin modificar ninguna coordenada física del objeto, de las vistas o de los rayos;
- `CHIP_UPSHIFT = 0.75`: todos los chips fixed-in-frame suben 0.75 unidades Manim;
- `SCREEN_GROUP_UPSHIFT = 0.55`: hoja 2D, método y síntesis final reciben una corrección superior moderada;
- se conservan exactamente el modelo escalonado, las fuentes de proyección, FRONT/TOP/RIGHT, PV/PH/PL y el abatimiento PH de 90°;
- se añaden pequeñas pausas entre cámaras, planos y proyecciones para que la corrección espacial no se sienta abrupta.

## Gates automáticos V9

Además de decodificación completa, H.264/yuv420p, 1920×1080, ~30 fps y auditoría de ocupación, el workflow V9 incorpora un gate específico para este defecto.

Durante la parte 3D (aprox. 5–60 s), excluyendo el strip inferior de captions:

- mediana del centro vertical robusto `median_main_cy < 660 px`;
- percentil 90 `p90_main_cy < 730 px`;
- mediana del borde inferior robusto `median_main_y1 < 900 px`;
- percentil 10 del borde superior `p10_main_y0 > 20 px` para evitar una sobrecorrección/clipping superior.

El objetivo visual no es forzar todo contra la parte superior; es recuperar la zona central/superior y eliminar el gran vacío superior que domina V8.

## Criterios manuales de aceptación

1. Después de desaparecer la portada, el sólido debe aparecer claramente por encima de la posición de V8.
2. Durante PV/PH/PL, el centro perceptual del conjunto debe estar cerca del centro vertical de pantalla y no en el tercio inferior.
3. Ninguna etiqueta FRONT/TOP/RIGHT ni PV/PH/PL debe cortarse por el borde superior.
4. Los chips de etapa deben quedar dentro de safe area y visiblemente separados del borde inferior.
5. El abatimiento de PH debe conservar el eje LT y terminar sin colisión con el borde superior.
6. Hoja 2D, método y síntesis deben mantener lectura completa y una composición ligeramente superior.
7. No se aceptan frames en blanco persistentes, solapes, fills oscuros accidentales o clipping lateral.
