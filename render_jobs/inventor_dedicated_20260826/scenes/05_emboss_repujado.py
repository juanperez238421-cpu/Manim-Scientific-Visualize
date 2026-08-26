from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorEmbossDetailed(InventorOperationScene):
    OPERATION = "Emboss"
    FEATURE_NODE = "Emboss1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch2"), ("Type", "Emboss from Face"), ("Depth", "3 mm"), ("Direction", "Positive")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1", "Sketch2", "Emboss1"],
        )
        self.intro("Repujado: partir de un croquis 2D base, crear una placa 3D y después elevar o grabar otro perfil sobre una cara.")

        plate = animate_rect_sketch_to_extrusion(
            self,
            width=4.8,
            depth=2.80,
            height=0.34,
            shift=DOWN * 0.34,
            dimensions="80 mm x 50 mm",
            extrusion="6 mm",
            step_start=1,
        )

        self.step(4, "Selecciona la cara superior y crea Sketch2", "El segundo croquis debe quedar asociado a la cara donde se aplicará el relieve; evita planos desconectados del sólido.")
        profile = Circle(radius=0.76, color=SKETCH, stroke_width=5).shift(DOWN * 0.34 + OUT * 0.19)
        inner = Circle(radius=0.34, color=SKETCH, stroke_width=4).shift(DOWN * 0.34 + OUT * 0.20)
        self.play(Create(profile), Create(inner), run_time=0.75)

        self.step(5, "Construye y restringe un perfil cerrado", "Círculos, texto convertido a geometría o contornos cerrados definen exactamente el área que Inventor elevará o grabará.")
        self.step(6, "3D Model -> Create -> Emboss", "Selecciona Sketch2, usa Emboss from Face, define Depth = 3 mm y conserva Positive para generar relieve hacia afuera.")

        preview = cylinder(0.76, 0.58, PREVIEW, 0.55).shift(DOWN * 0.34 + OUT * 0.45)
        preview_inner = cylinder(0.34, 0.63, CANVAS, 0.95).shift(DOWN * 0.34 + OUT * 0.48)
        self.play(FadeIn(preview), FadeIn(preview_inner), profile.animate.set_opacity(0.28), inner.animate.set_opacity(0.28), run_time=0.75)
        self.step(7, "Vista previa: Emboss vs Engrave", "Emboss agrega material y Engrave lo introduce en la cara. Verifica dirección, profundidad y que el contorno permanezca dentro de la superficie.")

        result = cylinder(0.76, 0.58, STEEL_DARK, 1.0).shift(DOWN * 0.34 + OUT * 0.45)
        hole = cylinder(0.34, 0.65, CANVAS, 1.0).shift(DOWN * 0.34 + OUT * 0.48)
        self.play(FadeOut(preview), FadeOut(preview_inner), FadeIn(result), FadeIn(hole), FadeOut(profile), FadeOut(inner), run_time=0.75)
        self.step(8, "OK -> Emboss1", "El Browser registra Sketch2 y Emboss1. La profundidad y el sentido pueden editarse sin rehacer Extrusion1.")
        finish_feature(self, 9, "Resultado: relieve de 3 mm creado desde un segundo croquis y completamente editable como Emboss1.")
