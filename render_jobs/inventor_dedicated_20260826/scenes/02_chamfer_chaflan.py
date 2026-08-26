from manim import *
from library.inventor_pro_ui import *


class InventorChamferDetailed(InventorOperationScene):
    OPERATION = "Chamfer"
    FEATURE_NODE = "Chamfer1"

    def construct(self):
        self.install_hud(
            [("Selection", "1 Edge"), ("Type", "Distance + Angle"), ("Distance", "6 mm"), ("Angle", "45 deg")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1"],
        )
        self.intro("Chaflán: reemplazar una esquina por una cara plana definida por distancia y/o ángulo.")
        raw = cuboid(4.4, 2.55, 0.78, STEEL).shift(DOWN * 0.30)
        self.play(FadeIn(raw, scale=0.94), run_time=0.8)
        self.step(1, "Selecciona la arista a biselar", "El chaflán trabaja sobre aristas del sólido y crea una nueva cara plana.")
        edge = Line3D(start=[-2.2, 0.975, -0.39], end=[2.2, 0.975, -0.39], color=SELECT, thickness=0.05)
        self.play(Create(edge), run_time=0.55)
        self.step(2, "3D Model → Modify → Chamfer", "Selecciona la arista y escoge el método de definición apropiado.")
        self.step(3, "Distance + Angle", "En este ejemplo: 6 mm y 45°. La cara resultante queda controlada por ambos parámetros.")
        pts = [(-2.2, -1.275), (2.2, -1.275), (2.2, 0.60), (1.57, 1.275), (-2.2, 1.275)]
        preview = extruded_polygon(pts, 0.78, PREVIEW, 0.58).shift(DOWN * 0.30)
        self.play(FadeOut(raw, run_time=0.25), FadeIn(preview, run_time=0.65), edge.animate.set_opacity(0.35))
        self.step(4, "Comprueba la orientación", "Si la cara inclinada aparece hacia el lado incorrecto, invierte la referencia o la dirección.")
        result = extruded_polygon(pts, 0.78, STEEL, 1.0).shift(DOWN * 0.30)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(edge), run_time=0.75)
        self.step(5, "Confirma y revisa Chamfer1", "El Browser conserva la operación y sus parámetros para edición posterior.")
        self.finish("Resultado: cara inclinada controlada por distancia y ángulo, sin modificar el croquis base.")
