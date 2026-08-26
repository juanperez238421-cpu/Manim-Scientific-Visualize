from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorRectPatternDetailed(InventorOperationScene):
    OPERATION = "Rectangular Pattern"
    FEATURE_NODE = "RectangularPattern1"

    def construct(self):
        self.install_hud(
            [("Features", "Extrusion2"), ("Direction 1", "X Axis"), ("Quantity", "4"), ("Spacing", "35 mm")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1", "Sketch2", "Extrusion2", "RectangularPattern1"],
        )
        self.intro("Patrón lineal: crear la placa desde un croquis 2D, modelar una sola operación semilla y repetirla paramétricamente en 3D.")

        plate = animate_rect_sketch_to_extrusion(
            self,
            width=5.8,
            depth=2.50,
            height=0.36,
            shift=DOWN * 0.36,
            dimensions="100 mm x 45 mm",
            extrusion="6 mm",
            step_start=1,
        )

        self.step(4, "Sketch2: dibuja la semilla sobre la cara", "Crea un solo círculo cerrado, acótalo y ubícalo respecto a un borde de referencia. El patrón repetirá el feature, no el dibujo manualmente.")
        seed_sketch = Circle(radius=0.32, color=SKETCH, stroke_width=5).shift(LEFT * 2.05 + DOWN * 0.36 + OUT * 0.20)
        self.play(Create(seed_sketch), run_time=0.60)

        self.step(5, "Finish Sketch -> Extrude -> Extrusion2", "Convierte el círculo en una protuberancia de 8 mm. Esta única operación será la semilla asociativa del patrón.")
        seed = cylinder(0.32, 0.70, STEEL_DARK).shift(LEFT * 2.05 + DOWN * 0.36 + OUT * 0.53)
        self.play(FadeOut(seed_sketch), FadeIn(seed), run_time=0.70)

        direction = Arrow3D(
            start=LEFT * 2.05 + DOWN * 1.48 + OUT * 0.25,
            end=RIGHT * 2.20 + DOWN * 1.48 + OUT * 0.25,
            color=SELECT,
            thickness=0.016,
            height=0.20,
            base_radius=0.075,
        )
        self.play(Create(direction), run_time=0.55)
        self.step(6, "3D Model -> Pattern -> Rectangular", "Selecciona Extrusion2 en Features y una arista o X Axis para Direction 1. La flecha naranja muestra el sentido de repetición.")

        self.step(7, "Quantity = 4; Spacing = 35 mm", "Quantity incluye la semilla. Spacing es la distancia centro a centro. Inventor calcula las tres ocurrencias adicionales automáticamente.")
        copies = VGroup(*[
            seed.copy().shift(RIGHT * 1.35 * i).set_color(PREVIEW).set_opacity(0.22)
            for i in range(1, 4)
        ])
        self.add(copies)
        self.play(LaggedStart(*[c.animate.set_opacity(0.60) for c in copies], lag_ratio=0.18), run_time=1.15)

        self.step(8, "Revisa dirección, cantidad y colisiones", "Usa Flip Direction si las copias crecen al lado incorrecto y verifica que ninguna ocurrencia salga de la placa o se solape.")
        final_copies = VGroup(*[seed.copy().shift(RIGHT * 1.35 * i) for i in range(1, 4)])
        self.play(FadeOut(copies), FadeIn(final_copies), FadeOut(direction), run_time=0.75)
        finish_feature(self, 9, "Resultado: cuatro ocurrencias 3D alineadas y gobernadas por una única semilla, Quantity y Spacing.")
