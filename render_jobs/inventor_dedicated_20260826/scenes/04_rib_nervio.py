from manim import *
from library.inventor_pro_ui import *


class InventorRibDetailed(InventorOperationScene):
    OPERATION = "Rib"
    FEATURE_NODE = "Rib1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch2 line"), ("Thickness", "6 mm"), ("Direction", "Symmetric"), ("Extent", "To Next")],
            ["Part1.ipt", "Origin", "Extrusion1", "Sketch2"],
        )
        self.intro("Nervio: convertir una línea de croquis abierta en una pared estructural con espesor y alcance controlados.")
        base = cuboid(4.6, 2.55, 0.42, STEEL).shift(DOWN * 0.38)
        wall = cuboid(0.46, 2.55, 2.35, STEEL_DARK).shift(LEFT * 2.05 + DOWN * 0.38 + OUT * 0.97)
        self.play(FadeIn(base), FadeIn(wall), run_time=0.8)
        self.step(1, "Crea un croquis sobre la cara", "A diferencia de Extrude, Rib puede partir de una línea abierta que representa el eje del refuerzo.")
        sketch = Line3D(start=[-1.82, -0.38, 0.26], end=[0.90, -0.38, 1.88], color=SKETCH, thickness=0.045)
        self.play(Create(sketch), run_time=0.65)
        self.step(2, "Dibuja la línea del nervio", "Acota y restringe la línea; su posición determina dónde crecerá el material.")
        self.step(3, "3D Model → Create → Rib", "Selecciona Sketch2, define Thickness = 6 mm y usa Symmetric para repartir el espesor.")
        pts = [(-1.82, -0.15), (-1.82, 1.68), (0.92, -0.15)]
        preview = extruded_polygon(pts, 0.34, PREVIEW, 0.58).rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.38)
        self.play(FadeIn(preview), sketch.animate.set_opacity(0.30), run_time=0.75)
        self.step(4, "Extent = To Next", "El nervio se prolonga hasta encontrar el sólido. Verifica que conecte base y pared sin atravesar zonas no deseadas.")
        result = extruded_polygon(pts, 0.34, STEEL, 1.0).rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.38)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(sketch), run_time=0.75)
        self.step(5, "OK → Rib1", "El Browser conserva Sketch2 como dependencia de Rib1: editar el croquis reposiciona el refuerzo.")
        self.finish("Resultado: refuerzo estructural delgado generado desde una línea abierta y totalmente editable.")
