from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import _fixed_badge, finish_feature
import math


class InventorCircularPatternDetailed(InventorOperationScene):
    OPERATION = "Circular Pattern"
    FEATURE_NODE = "CircularPattern1"

    def construct(self):
        self.install_hud(
            [("Features", "Hole1"), ("Rotation Axis", "Z Axis"), ("Placement", "Full"), ("Quantity", "8")],
            ["Part1.ipt", "Origin", "Z Axis", "Sketch1", "Extrusion1", "Sketch2", "Hole1", "CircularPattern1"],
        )
        self.intro("Patrón circular: comenzar con un croquis 2D, crear un disco 3D, modelar una sola semilla y distribuirla alrededor de un eje.")

        self.move_camera(phi=4 * DEGREES, theta=-90 * DEGREES, zoom=0.90, run_time=0.75)
        badge = _fixed_badge(
            self,
            "SKETCH MODE  |  XY Plane  |  Sketch1",
            "Base circle diameter 80 mm   |   Center coincident with origin",
        )
        base_sketch = Circle(radius=2.25, color=SKETCH, stroke_width=5).shift(DOWN * 0.34)
        center = Dot(base_sketch.get_center(), radius=0.055, color=SELECT)
        self.play(Create(base_sketch), FadeIn(center), run_time=0.85)
        self.step(1, "Start 2D Sketch -> dibuja el círculo base", "Haz coincidir el centro con el origen y acota el diámetro. Un centro estable será también una referencia natural para el patrón.")

        self.play(FadeOut(badge), run_time=0.25)
        self.remove_fixed_in_frame_mobjects(badge)
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.90)
        disk_preview = cylinder(2.25, 0.04, PREVIEW, 0.50).shift(DOWN * 0.34)
        self.play(FadeIn(disk_preview), base_sketch.animate.set_opacity(0.25), run_time=0.45)
        disk = cylinder(2.25, 0.38, STEEL).shift(DOWN * 0.34)
        self.play(ReplacementTransform(disk_preview, disk), FadeOut(base_sketch), FadeOut(center), run_time=0.85)
        self.step(2, "Finish Sketch -> Extrude -> Extrusion1", "Extruye el círculo 6 mm para crear el disco. La operación conserva Sketch1 como dependencia paramétrica del sólido base.")

        hub = cylinder(0.46, 0.58, CANVAS).shift(DOWN * 0.34 + OUT * 0.42)
        self.play(FadeIn(hub), run_time=0.45)
        self.step(3, "Sketch2: crea una sola semilla radial", "Dibuja un círculo pequeño a la distancia radial correcta. Acota diámetro y distancia al centro para controlar el patrón.")
        seed_sketch = Circle(radius=0.24, color=SKETCH, stroke_width=5).shift(RIGHT * 1.48 + DOWN * 0.34 + OUT * 0.20)
        self.play(Create(seed_sketch), run_time=0.55)

        seed = cylinder(0.24, 0.62, STEEL_DARK).shift(RIGHT * 1.48 + DOWN * 0.34 + OUT * 0.45)
        self.play(FadeOut(seed_sketch), FadeIn(seed), run_time=0.65)
        self.step(4, "Finish Sketch -> crea Hole1 o Extrusion2", "Convierte el perfil en una operación semilla. El patrón debe repetir el feature completo para conservar asociatividad.")

        axis = Arrow3D(
            start=DOWN * 0.34 + IN * 0.55,
            end=DOWN * 0.34 + OUT * 1.45,
            color=SELECT,
            thickness=0.017,
            height=0.21,
            base_radius=0.08,
        )
        self.play(Create(axis), run_time=0.55)
        self.step(5, "3D Model -> Pattern -> Circular", "Selecciona Hole1 en Features y Z Axis como Rotation Axis. El eje controla el centro geométrico de la distribución.")

        self.step(6, "Placement = Full; Quantity = 8", "Full reparte ocho ocurrencias uniformemente en 360 grados. Inventor calcula el incremento angular automáticamente.")
        preview = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            preview.add(
                seed.copy()
                .move_to([1.48 * math.cos(angle), 1.48 * math.sin(angle) - 0.34, 0.45])
                .set_color(PREVIEW)
                .set_opacity(0.22)
            )
        self.add(preview)
        self.play(LaggedStart(*[p.animate.set_opacity(0.60) for p in preview], lag_ratio=0.08), run_time=1.2)

        self.step(7, "Verifica eje, cobertura y separación", "Un eje incorrecto desplaza el centro del patrón. Comprueba que las ocho ocurrencias no se superpongan ni salgan del disco.")
        final = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            final.add(seed.copy().move_to([1.48 * math.cos(angle), 1.48 * math.sin(angle) - 0.34, 0.45]))
        self.play(FadeOut(preview), FadeIn(final), FadeOut(axis), run_time=0.75)
        finish_feature(self, 8, "Resultado: ocho ocurrencias 3D uniformes alrededor del eje Z y controladas por CircularPattern1.")
