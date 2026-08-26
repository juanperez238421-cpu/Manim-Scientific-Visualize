from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorRibDetailed(InventorOperationScene):
    OPERATION = "Rib"
    FEATURE_NODE = "Rib1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch2 line"), ("Thickness", "6 mm"), ("Direction", "Symmetric"), ("Extent", "To Next")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1", "Sketch2", "Rib1"],
        )
        self.intro("Nervio: crear primero el sólido base desde un croquis 2D y después convertir una línea abierta en un refuerzo 3D paramétrico.")

        base = animate_rect_sketch_to_extrusion(
            self,
            width=4.6,
            depth=2.55,
            height=0.42,
            shift=DOWN * 0.38,
            dimensions="75 mm x 45 mm",
            extrusion="7 mm",
            step_start=1,
        )

        self.step(4, "Crea la pared que recibirá el refuerzo", "El nervio debe conectar material existente. Aquí una pared vertical representa la siguiente cara que limitará Extent = To Next.")
        wall = cuboid(0.46, 2.55, 2.35, STEEL_DARK).shift(LEFT * 2.05 + DOWN * 0.38 + OUT * 0.97)
        self.play(FadeIn(wall), run_time=0.65)

        self.step(5, "Sketch2 sobre la cara: dibuja una línea abierta", "Rib no requiere un perfil cerrado. Acota la línea y restringe sus extremos para controlar posición, inclinación y dependencia.")
        sketch = Line3D(start=[-1.82, -0.38, 0.26], end=[0.90, -0.38, 1.88], color=SKETCH, thickness=0.045)
        self.play(Create(sketch), run_time=0.65)

        self.step(6, "3D Model -> Create -> Rib", "Selecciona Sketch2, define Thickness = 6 mm y usa Symmetric para repartir el espesor a ambos lados de la línea.")
        pts = [(-1.82, -0.15), (-1.82, 1.68), (0.92, -0.15)]
        preview = extruded_polygon(pts, 0.34, PREVIEW, 0.58).rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.38)
        self.play(FadeIn(preview), sketch.animate.set_opacity(0.30), run_time=0.75)

        self.step(7, "Extent = To Next", "La vista previa debe crecer hasta encontrar el sólido siguiente. Verifica que una base, pared y nervio queden conectados sin atravesar zonas no deseadas.")
        result = extruded_polygon(pts, 0.34, STEEL, 1.0).rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.38)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(sketch), run_time=0.75)

        self.step(8, "OK -> Rib1", "El Browser conserva Sketch2 como dependencia de Rib1. Editar la línea reposiciona el refuerzo y cambiar Thickness modifica su espesor.")
        finish_feature(self, 9, "Resultado: refuerzo estructural delgado creado desde una línea abierta y conectado paramétricamente al sólido.")
