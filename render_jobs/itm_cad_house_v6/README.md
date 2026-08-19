# ITM · Dibujo Técnico y CAD · Croquis y extrusión 3D

Paquete ManimCE institucional para explicar, paso a paso, la construcción de una vivienda mediante croquis 2D, extrusión positiva, extrusión negativa y verificación del modelo CAD 3D.

## Escenas entregables

| Escena | Grupo | Salida esperada |
|---|---|---|
| `HouseExtrusionITM_SEDTCAD22` | `SEDTCAD22` | `HouseExtrusionITM_SEDTCAD22.mp4` |
| `HouseExtrusionITM_DTR43` | `DTR43` | `HouseExtrusionITM_DTR43.mp4` |

Las dos escenas heredan de `HouseExtrusion3D`. Solo cambia el código del grupo en la portada y el HUD; la geometría, la cámara, los tiempos y las validaciones son idénticos.

## Secuencia pedagógica

1. Portada institucional ITM.
2. Terreno y retícula de referencia.
3. Croquis cerrado de la losa.
4. Extrusión positiva de la losa.
5. Croquis cerrado de muros y columnas sobre la cara superior.
6. Extrusión positiva de columnas.
7. Extrusión positiva de muros exteriores e interiores.
8. Extrusión negativa de la puerta.
9. Extrusión negativa de la ventana.
10. Croquis y extrusión positiva de la cubierta.
11. Órbita final y síntesis de la gramática CAD.

## Estructura

```text
itm_cad_house_v6/
├── assets/
│   └── itm_logo.png
├── house_extrusion_itm.py
├── CAD_ANIMATION_PROTOCOL.md
├── validate_scene.py
├── manim.cfg
├── requirements.txt
└── README.md
```

## Validación local

```bash
python -m py_compile house_extrusion_itm.py validate_scene.py
python validate_scene.py
```

## Render de prueba

```bash
manim -pql house_extrusion_itm.py HouseExtrusionITM_SEDTCAD22 --format=mp4 --disable_caching
manim -pql house_extrusion_itm.py HouseExtrusionITM_DTR43 --format=mp4 --disable_caching
```

## Render final

```bash
manim -pqh house_extrusion_itm.py HouseExtrusionITM_SEDTCAD22 --format=mp4 --disable_caching
manim -pqh house_extrusion_itm.py HouseExtrusionITM_DTR43 --format=mp4 --disable_caching
```

En ejecución sin escritorio se conserva el indicador literal `-pqh` mediante un `xdg-open` neutro, según el protocolo PQH v8.

## Criterios de aceptación

- Manim Community Edition `0.20.1`.
- Full HD `1920×1080`, `30 fps`.
- MP4 H.264, `yuv420p`.
- Código compilable y activo institucional disponible.
- Todo texto visible creado con `Tex` y animado mediante `Write`.
- Croquis de muros cerrados y congruentes con la huella extruida.
- Transición explícita de cámara ortogonal 2D a vista volumétrica 3D.
- Puerta y ventana terminan como vacíos geométricos, no como rectángulos superpuestos.
- Decodificación completa con FFmpeg, auditoría por fotogramas y suma SHA-256.

## Identidad y trazabilidad

- La identidad visual fue contrastada con la página oficial de formatos institucionales del ITM: <https://www.itm.edu.co/formatos-institucionales/>.
- Los códigos `DTR43` y `SEDTCAD22` corresponden a “Dibujo Técnico y CAD” en documentación pública del ITM: <https://www.itm.edu.co/wp-content/uploads/facultad-ingenierias/2024/Acta-nro.-24.-Reunio%CC%81n-Extraordinaria-del-11-de-junio-de-2025_compressed.pdf>.
- El raster del logotipo se conserva localmente para hacer el render reproducible. Fuente pública de recuperación: <https://keystoneacademic-res.cloudinary.com/image/upload/c_pad,w_3840,h_1280/dpr_auto/f_auto/q_auto/v1/element/15/150420_Metro.png>.

