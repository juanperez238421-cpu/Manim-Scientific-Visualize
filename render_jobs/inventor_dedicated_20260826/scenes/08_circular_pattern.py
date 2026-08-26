from manim import *
from library.inventor_pro_ui import *
import math


class InventorCircularPatternDetailed(InventorOperationScene):
    OPERATION = "Circular Pattern"
    FEATURE_NODE = "CircularPattern1"

    def construct(self):
        self.install_hud(
            [("Features", "Hole1"), ("Rotation Axis", "Z Axis"), ("Placement", "Full"), ("Quantity", "8")],
            ["Part1.ipt", "Origin", "Z Axis", "Extrusion1", "Hole1"],
        )
        self.intro("Patrón circular: distribuir una operación semilla alrededor de un eje mediante cantidad y ángulo total.")
        disk = cylinder(2.25, 0.38, STEEL).shift(DOWN * 0.34)
        hub = cylinder(0.46, 0.58, CANVAS).shift(DOWN * 0.34 + OUT * 0.42)
        seed = cylinder(0.24, 0.62, STEEL_DARK).shift(RIGHT * 1.48 + DOWN * 0.34 + OUT * 0.45)
        self.play(FadeIn(disk), FadeIn(hub), FadeIn(seed), run_time=0.9)
        self.step(1, "Define la semilla", "Crea una sola operación a la distancia radial correcta respecto al eje de giro.")
        axis = Arrow3D(start=DOWN * 0.34 + IN * 0.55, end=DOWN * 0.34 + OUT * 1.45,
                       color=SELECT, thickness=0.017, height=0.21, base_radius=0.08)
        self.play(Create(axis), run_time=0.55)
        self.step(2, "3D Model → Pattern → Circular", "Selecciona Hole1/Extrusion2 como feature y Z Axis como Rotation Axis.")
        self.step(3, "Placement = Full; Quantity = 8", "Full distribuye uniformemente 8 ocurrencias en 360°. También puedes usar un ángulo parcial.")
        preview = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            preview.add(seed.copy().move_to([1.48 * math.cos(angle), 1.48 * math.sin(angle) - 0.34, 0.45])
                        .set_color(PREVIEW).set_opacity(0.22))
        self.add(preview)
        self.play(LaggedStart(*[p.animate.set_opacity(0.60) for p in preview], lag_ratio=0.08), run_time=1.2)
        self.step(4, "Verifica eje, sentido y cobertura", "Un eje incorrecto cambia el centro de distribución. Comprueba que las ocurrencias no se superpongan.")
        final = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            final.add(seed.copy().move_to([1.48 * math.cos(angle), 1.48 * math.sin(angle) - 0.34, 0.45]))
        self.play(FadeOut(preview), FadeIn(final), FadeOut(axis), run_time=0.75)
        self.step(5, "OK → CircularPattern1", "Cantidad, eje y cobertura quedan registrados como parámetros editables del patrón.")
        self.finish("Resultado: ocho ocurrencias uniformes alrededor de Z, controladas por CircularPattern1.")
