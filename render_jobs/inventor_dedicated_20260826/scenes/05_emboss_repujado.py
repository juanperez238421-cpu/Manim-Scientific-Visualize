from manim import *
from library.inventor_pro_ui import *


class InventorEmbossDetailed(InventorOperationScene):
    OPERATION = "Emboss"
    FEATURE_NODE = "Emboss1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch2"), ("Type", "Emboss from Face"), ("Depth", "3 mm"), ("Direction", "Positive")],
            ["Part1.ipt", "Origin", "Extrusion1", "Sketch2"],
        )
        self.intro("Repujado: elevar o grabar un perfil de croquis sobre una cara para crear relieve funcional o gráfico.")
        plate = rounded_plate(4.8, 2.80, 0.34, 0.28, STEEL).shift(DOWN * 0.34)
        self.play(LaggedStart(*[FadeIn(m) for m in plate], lag_ratio=0.08), run_time=0.85)
        self.step(1, "Selecciona la cara y crea Sketch2", "El perfil debe estar ubicado sobre la cara donde se aplicará el relieve.")
        profile = Circle(radius=0.76, color=SKETCH, stroke_width=5).shift(DOWN * 0.34 + OUT * 0.19)
        inner = Circle(radius=0.34, color=SKETCH, stroke_width=4).shift(DOWN * 0.34 + OUT * 0.20)
        self.play(Create(profile), Create(inner), run_time=0.75)
        self.step(2, "Construye un perfil cerrado", "Círculos, texto convertido a perfil u otra geometría cerrada pueden formar el área de repujado.")
        self.step(3, "3D Model → Create → Emboss", "Selecciona Emboss from Face y define Depth = 3 mm. Usa dirección positiva para generar relieve.")
        preview = cylinder(0.76, 0.58, PREVIEW, 0.55).shift(DOWN * 0.34 + OUT * 0.45)
        preview_inner = cylinder(0.34, 0.63, CANVAS, 0.95).shift(DOWN * 0.34 + OUT * 0.48)
        self.play(FadeIn(preview), FadeIn(preview_inner), profile.animate.set_opacity(0.28), inner.animate.set_opacity(0.28), run_time=0.75)
        self.step(4, "Vista previa y dirección", "Cambiar Emboss por Engrave invierte el efecto: relieve hacia afuera frente a grabado hacia adentro.")
        result = cylinder(0.76, 0.58, STEEL_DARK, 1.0).shift(DOWN * 0.34 + OUT * 0.45)
        hole = cylinder(0.34, 0.65, CANVAS, 1.0).shift(DOWN * 0.34 + OUT * 0.48)
        self.play(FadeOut(preview), FadeOut(preview_inner), FadeIn(result), FadeIn(hole), FadeOut(profile), FadeOut(inner), run_time=0.75)
        self.step(5, "OK → Emboss1", "El relieve mantiene dependencia con Sketch2 y puede editarse en profundidad o dirección.")
        self.finish("Resultado: relieve de 3 mm creado desde la cara, editable como Emboss1.")
