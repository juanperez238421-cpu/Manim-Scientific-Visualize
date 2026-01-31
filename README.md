# Manim Scientific Visualizer 🚀

[![Manim](https://img.shields.io/badge/Rendered%20with-Manim-white.svg)](https://docs.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una suite avanzada de visualización computacional diseñada para la comunicación técnica en **Ingeniería Mecánica**, **Investigación de Fluidos** y **Ciencias de la Computación**. Este repositorio contiene una infraestructura modular para transformar datos experimentales y algoritmos complejos en explicaciones visuales de alto impacto.

---

## 🌟 Módulos Destacados

### 1. Investigación de Fluidos (PIV & GWVT)
Visualización de datos reales de la investigación sobre **Turbinas de Vórtice Gravitacional**. 
* **Integración NumPy:** Procesa campos de velocidad experimentales de *Particle Image Velocimetry* (PIV) directamente desde archivos `.npy`.
* **Líneas de Corriente Dinámicas:** Implementación de flujos vectoriales animados para validar perfiles de velocidad y trayectorias de partículas.

### 2. Ingeniería Mecánica & Estática
Soluciones visuales para problemas estructurales y mecánicos.
* **Simulador de Vigas:** Incluye una **GUI interactiva** en Tkinter que permite definir parámetros físicos y generar automáticamente diagramas de cortante ($V$) y momento ($M$).
* **Mecánica 3D:** Renderizado isométrico de máquinas (tambores, soportes) y vectores espaciales utilizando cámaras dinámicas y precisión milimétrica.

### 3. Computer Science & Software
Visualización de la "anatomía" del código y la gestión de memoria.
* **UML Engine:** Generador automático de diagramas de clase que ajustan su tamaño dinámicamente según atributos y métodos.
* **Estructuras de Datos:** Animaciones detalladas de Listas (SLL, DLL, Circulares), Pilas, Colas y Árboles BST con punteros animados.
* **Análisis Algorítmico:** Comparativas de complejidad Big O, Teorema Maestro y ejecución paso a paso con un **Code Cursor** personalizado.

---

## 📂 Estructura del Proyecto

```text
/
├── core/                   # El motor visual (Librerías reutilizables)
│   ├── visual_engine.py    # Estilos de consolas, códigos y badges
│   ├── software_tools.py   # Motores UML y visualizadores de estructuras
│   └── physics_tools.py    # Funciones para PIV, vigas y estática
├── engineering/            # Aplicaciones de Ingeniería Física y Mecánica
├── computer_science/       # Teoría de la Computación y Arquitectura de Software
├── assets/                 # Recursos externos (Imágenes, SVGs, datos .npy)
└── README.md               # Documentación maestra
