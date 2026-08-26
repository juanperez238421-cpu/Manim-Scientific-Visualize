from manim import *
from library.inventor_pro_ui import *


class InventorRectPatternDetailed(InventorOperationScene):
    OPERATION = "Rectangular Pattern"
    FEATURE_NODE = "RectangularPattern1"

    def construct(self):
        self.install_hud(
            [("Features", "Extrusion2"), ("Direction 1", "X Axis"), ("Quantity", "4"), ("Spacing", "35 mm")],
            ["Part1.ipt", "Origin", "Extrusion1", "Extrusion2"],
        )
        self.intro("Patrón lineal: repetir una operación semilla en una dirección con cantidad y separación paramétricas.")
        plate = rounded_plate(5.8, 2.50, 0.36, 0.26, STEEL).shift(DOWN * 0.36)
        seed = cylinder(0.32, 0.70, STEEL_DARK).shift(LEFT * 2.05 + DOWN * 0.36 + OUT * 0.53)
        self.play(LaggedStart(*[FadeIn(m) for m in plate], lag_ratio=0.05), FadeIn(seed), run_time=0.9)
        self.step(1, "Crea la operación semilla", "Modela una sola protuberancia, corte o agujero. El patrón repetirá ese feature.")
        direction = Arrow3D(start=LEFT * 2.05 + DOWN * 1.48 + OUT * 0.25,
                            end=RIGHT * 2.20 + DOWN * 1.48 + OUT * 0.25,
                            color=SELECT, thickness=0.016, height=0.20, base_radius=0.075)
        self.play(Create(direction), run_time=0.55)
        self.step(2, "3D Model → Pattern → Rectangular", "Selecciona Extrusion2 como Features y una arista/eje para Direction 1.")
        self.step(3, "Quantity = 4; Spacing = 35 mm", "Cantidad incluye la semilla. Spacing controla la distancia centro a centro.")
        copies = VGroup(*[seed.copy().shift(RIGHT * 1.35 * i).set_color(PREVIEW).set_opacity(0.22) for i in range(1, 4)])
        self.add(copies)
        self.play(LaggedStart(*[c.animate.set_opacity(0.60) for c in copies], lag_ratio=0.18), run_time=1.15)
        self.step(4, "Revisa la dirección", "Si las copias crecen hacia el lado equivocado, usa Flip Direction antes de confirmar.")
        final_copies = VGroup(*[seed.copy().shift(RIGHT * 1.35 * i) for i in range(1, 4)])
        self.play(FadeOut(copies), FadeIn(final_copies), FadeOut(direction), run_time=0.75)
        self.step(5, "OK → RectangularPattern1", "Modificar Quantity o Spacing actualiza todas las ocurrencias automáticamente.")
        self.finish("Resultado: cuatro ocurrencias alineadas, gobernadas por una única semilla y dos parámetros.")
