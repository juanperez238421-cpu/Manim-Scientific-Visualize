# Manim Scientific Visualizer 🚀

[![Manim](https://img.shields.io/badge/Rendered%20with-Manim-white.svg)](https://docs.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced computational visualization suite designed for high-level technical communication in **Mechanical Engineering**, **Fluid Dynamics Research**, and **Computer Science**. This repository provides a modular infrastructure to transform experimental datasets and complex algorithms into high-fidelity visual assets.

---

## 🌟 Core Research & Modules

### 1. Fluid Dynamics (PIV & GWVT)
Visual validation of research on **Gravitational Vortex Turbines (GWVT)**.
* **NumPy Integration:** Native processing of experimental *Particle Image Velocimetry* (PIV) vector fields from `.npy` files.
* **Flow Reconstruction:** Dynamic streamline implementation to validate velocity profiles and vortex core stability.

### 2. Statics & Structural Mechanics

* **Vector Mechanics:** 3D isometric rendering of machine components, spatial vector decomposition, and multi-body equilibrium (Clamps, Drums, and Pins).

<p align="center">
  <img src="TresPlanosCoordenados.gif" alt="Center of Mass" width="1280"/>
</p>

* **Centroid Analysis:** Parametric tracking of composite shapes' centers of mass with real-time coordinate updates.

<p align="center">
  <img src="Centerofmass1.gif" alt="Center of Mass" width="1280"/>
</p>

<p align="center">
  <img src="DynamicCombinedCentroid_1280.gif" alt="Center of Mass" width="1280"/>
</p>

### 3. Computer Science & Software Theory
Visual "white-box" analysis of code execution and memory management.
* **Software Architecture:** Dynamic UML Engine for automated class diagram generation with inheritance/composition mapping.
* **Memory & Pointers:** Low-level visualization of stack/heap allocation, pointer arithmetic, and modern C++ smart pointers (`unique_ptr`, `shared_ptr`).
* **Data Structures:** Animated logic for Lists (SLL, DLL, Circular), FIFO Queues, and BST recursive traversals.
* **Code Debugger:** High-precision **Code Cursor** system for line-by-line algorithm execution tracing.

<p align="center">
  <img src="BSTExplainer.gif" alt="Center of Mass" width="1280"/>
</p>


---


## 📂 Meticulous Project Structure

```text
/
├── 📂 core/                    # Visualization Engine (The Library)
│   ├── visual_engine.py        # Academic themes, Consoles, and Code cursors
│   ├── software_tools.py       # UML generators and Data Structure nodes
│   └── physics_tools.py        # PIV parsers, Beam loads, and 3D Vectors
├── 📂 engineering/             # Physics-Based Applications
│   ├── 📂 fluid_research/      # GWVT Thesis & PIV dataset processing
│   ├── 📂 statics_mechanics/   # Vector systems, Beams, and Equilibrium
│   └── 📂 centroids_geometry/  # Parametric center of mass analysis
├── 📂 computer_science/        # Software & Algorithmic Theory
│   ├── 📂 memory_pointers/     # Memory management and pointer logic
│   ├── 📂 data_structures/     # Linear/Non-linear structures implementation
│   └── 📂 oop_series/          # Inheritance, Polymorphism, and UML design
├── 📂 assets/                  # Scientific datasets (.npy), SVGs, and Images
└── README.md                   # Master Documentation



