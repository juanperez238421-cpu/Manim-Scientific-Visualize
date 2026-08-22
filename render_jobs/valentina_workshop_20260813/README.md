# Valentina - Cálculo III - Taller 1

Paquete ManimCE con **18 videos independientes**, uno por cada pregunta numerada del taller oficial de preparación para el Parcial 1.

- Runtime objetivo: Manim Community Edition 0.20.1
- Formato final: 1920x1080, 30 fps, H.264/yuv420p
- Validación: literal `-pql --fps 30` por escena antes del render final
- Render final: literal `-pqh --fps 30` por escena
- Estilo: `jp_classroom_style.py` (white classroom / black hierarchy)

Escenas: `Q01` ... `Q18`.

Observación pedagógica importante: en la pregunta 12, el inciso a) impreso indica `ln(x-y^2)`, cuyo dominio es `x>y^2`, pero la Figura I representa visualmente una parábola vertical compatible con `y>x^2`. El video documenta esta inconsistencia en lugar de ocultarla.

Render contract FINAL: `py_compile` y 18/18 `-pql --fps 30` ya validados sobre la fuente exacta; entrega final en 18 jobs paralelos con literal `-pqh --fps 30`, FFmpeg/ffprobe instalado explícitamente, decodificación completa, SHA-256 y ZIP consolidado.
