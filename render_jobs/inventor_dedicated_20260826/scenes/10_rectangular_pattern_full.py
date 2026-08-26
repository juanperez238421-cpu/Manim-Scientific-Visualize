from manim import *

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorRectangularPatternFull(InventorOperationScene):
    """Full rectangular pattern: one seed feature, two orthogonal directions."""

    OPERATION = "Rectangular Pattern"
    FEATURE_NODE = "RectangularPattern1"

    def construct(self):
        self.install_hud(
            [
                ("Features", "Extrusion2"),
                ("Direction 1", "X Axis: 4 x 25 mm"),
                ("Direction 2", "Y Axis: 3 x 18 mm"),
                ("Compute", "Optimized"),
            ],
            [
                "Part1.ipt",
                "Origin",
                "Sketch1",
                "Extrusion1",
                "Sketch2",
                "Extrusion2",
                "RectangularPattern1",
            ],
        )
        self.intro(
            "Patrón rectangular: construye una sola semilla 3D y repítela en una o dos direcciones con cantidades y separaciones paramétricas."
        )

        plate = animate_rect_sketch_to_extrusion(
            self,
            width=5.9,
            depth=3.05,
            height=0.42,
            shift=DOWN * 0.32,
            dimensions="110 mm x 60 mm",
            extrusion="8 mm",
            step_start=1,
        )

        seed_xy = LEFT * 1.95 + DOWN * 1.08
        seed_sketch = Circle(radius=0.27, color=SKETCH, stroke_width=5).shift(seed_xy + OUT * 0.23)
        self.play(Create(seed_sketch), run_time=0.55)
        self.step(
            4,
            "Sketch2 -> crea una única semilla",
            "Dibuja y acota un solo círculo sobre la cara. El patrón debe repetir el feature asociado, no múltiples perfiles dibujados manualmente.",
        )

        seed = cylinder(0.27, 0.64, STEEL_DARK).shift(seed_xy + OUT * 0.48)
        self.play(FadeOut(seed_sketch), FadeIn(seed), run_time=0.65)
        self.step(
            5,
            "Finish Sketch -> Extrude -> Extrusion2",
            "Genera una protuberancia de 10 mm. Extrusion2 será la semilla asociativa que controlará todas las ocurrencias del patrón.",
        )

        arrow_x = Arrow3D(
            start=seed_xy + DOWN * 0.55 + OUT * 0.24,
            end=RIGHT * 2.10 + DOWN * 1.63 + OUT * 0.24,
            color=SELECT,
            thickness=0.015,
            height=0.18,
            base_radius=0.07,
        )
        self.play(Create(arrow_x), run_time=0.50)
        self.step(
            6,
            "3D Model -> Pattern -> Rectangular",
            "Selecciona Extrusion2 como Features y una arista horizontal o X Axis como Direction 1. La flecha naranja define el sentido positivo.",
        )

        # Direction 1: seed + three copies.
        dx = 1.28
        row_preview = VGroup(*[
            seed.copy().shift(RIGHT * dx * i).set_color(PREVIEW).set_opacity(0.24)
            for i in range(1, 4)
        ])
        self.add(row_preview)
        self.play(
            LaggedStart(*[copy.animate.set_opacity(0.62) for copy in row_preview], lag_ratio=0.16),
            run_time=1.05,
        )
        self.step(
            7,
            "Direction 1 -> Quantity = 4; Spacing = 25 mm",
            "Quantity incluye la semilla. Spacing es centro a centro. Inventor calcula las tres ocurrencias nuevas manteniendo dependencia con Extrusion2.",
        )

        arrow_y = Arrow3D(
            start=seed_xy + LEFT * 0.55 + OUT * 0.24,
            end=LEFT * 2.50 + UP * 1.22 + OUT * 0.24,
            color=SELECT,
            thickness=0.015,
            height=0.18,
            base_radius=0.07,
        )
        self.play(Create(arrow_y), run_time=0.50)
        self.step(
            8,
            "Activa Direction 2 -> selecciona Y Axis",
            "La segunda dirección convierte la fila en una matriz rectangular. Cada dirección mantiene su propia cantidad y separación.",
        )

        dy = 0.92
        grid_preview = VGroup()
        # j=0 is already represented by the original seed + row preview.
        for j in range(1, 3):
            for i in range(0, 4):
                grid_preview.add(
                    seed.copy()
                    .shift(RIGHT * dx * i + UP * dy * j)
                    .set_color(PREVIEW)
                    .set_opacity(0.22)
                )
        self.add(grid_preview)
        self.play(
            LaggedStart(*[copy.animate.set_opacity(0.58) for copy in grid_preview], lag_ratio=0.07),
            run_time=1.20,
        )
        self.step(
            9,
            "Direction 2 -> Quantity = 3; Spacing = 18 mm",
            "Resultado previo: 4 x 3 = 12 ocurrencias totales. Ajusta cada separación hasta respetar bordes, zonas libres y restricciones funcionales.",
        )

        final = VGroup()
        for j in range(0, 3):
            for i in range(0, 4):
                if i == 0 and j == 0:
                    continue
                final.add(seed.copy().shift(RIGHT * dx * i + UP * dy * j))

        self.play(
            FadeOut(row_preview),
            FadeOut(grid_preview),
            FadeOut(arrow_x),
            FadeOut(arrow_y),
            FadeIn(final),
            run_time=0.90,
        )
        self.step(
            10,
            "Preview -> revisa dirección, cantidad, spacing y colisiones",
            "Usa Flip Direction si una matriz crece al lado incorrecto y confirma que ninguna ocurrencia exceda la cara o se superponga con otra feature.",
        )

        finish_feature(
            self,
            11,
            "Resultado: RectangularPattern1 controla doce ocurrencias 3D desde una única semilla mediante dos direcciones ortogonales editables.",
        )
