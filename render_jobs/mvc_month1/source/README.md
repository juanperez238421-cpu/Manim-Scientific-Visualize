# Biblioteca ManimCE — Cálculo de varias variables, primer mes

Paquete didáctico modular para **Manim Community Edition 0.20.1**, diseñado para render horizontal 16:9 en `-pqh` (1920×1080, 30 fps).

## Alcance temático asumido

No se suministró una planeación oficial del curso. Por ello, el paquete usa una secuencia estándar de cuatro semanas:

1. **Semana 1:** vectores en R²/R³, componentes, magnitud, producto punto y proyección.
2. **Semana 2:** producto cruz, área orientada, rectas, planos e intersección.
3. **Semana 3:** funciones de dos variables, superficies, curvas de nivel, límites y dependencia del camino.
4. **Semana 4:** derivadas parciales, cortes, gradiente, plano tangente y aproximación lineal.

## Videos y clases

| Video | Archivo | Clase | Tipo visual |
|---|---|---|---|
| 01 | `scenes/week1_vectors.py` | `W1_VectorBridge2D3D` | transición 2D→3D |
| 02 | `scenes/week1_vectors.py` | `W1_DotProductProjection` | 2D |
| 03 | `scenes/week2_geometry3d.py` | `W2_CrossProductArea` | 3D |
| 04 | `scenes/week2_geometry3d.py` | `W2_LinesPlanesIntersection` | 3D |
| 05 | `scenes/week3_functions.py` | `W3_SurfaceToContours` | 3D→vista 2D |
| 06 | `scenes/week3_functions.py` | `W3_PathDependentLimit` | 2D |
| 07 | `scenes/week4_derivatives.py` | `W4_PartialDerivativeSlices` | 3D |
| 08 | `scenes/week4_derivatives.py` | `W4_GradientAndTangentPlane` | 3D combinado |

## Render local

Prueba rápida:

```bash
manim -pql scenes/week1_vectors.py W1_VectorBridge2D3D --disable_caching
```

Render final:

```bash
manim -pqh scenes/week1_vectors.py W1_VectorBridge2D3D --disable_caching
```

El workflow de GitHub Actions renderiza las ocho escenas con el indicador literal `-pqh`, verifica cada MP4 mediante `ffprobe`, genera SHA-256 y crea una compilación final.
