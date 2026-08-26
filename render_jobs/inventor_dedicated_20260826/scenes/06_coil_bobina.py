from manim import *
from library.inventor_pro_ui import *
import math
import numpy as np


class InventorCoilDetailed(InventorOperationScene):
    OPERATION = "Coil"
    FEATURE_NODE = "Coil1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch1 circle"), ("Axis", "Centerline"), ("Pitch", "12 mm"), ("Revolutions", "4")],
            ["Part1.ipt", "Origin", "Sketch1", "Centerline"],
        )
        self.intro("Bobina: combinar giro y avance axial para crear geometría helicoidal controlada por paso y vueltas.")
        axis = DashedLine(start=IN * 2.35, end=OUT * 2.35, color=UI_MID, dash_length=0.18, stroke_width=3)
        profile = Circle(radius=0.20, color=SKETCH, stroke_width=5).rotate(90 * DEGREES, axis=UP).shift(RIGHT * 1.20 + IN * 2.10)
        self.play(Create(axis), FadeIn(profile), run_time=0.8)
        self.step(1, "Croquis: perfil + eje", "La bobina necesita un perfil transversal y un eje/centerline claramente definidos.")
        self.step(2, "3D Model → Create → Coil", "Selecciona el perfil y después el eje. Inventor establece la relación helicoidal entre ambos.")
        pitch = Line3D(start=[1.72, 0, -1.55], end=[1.72, 0, -0.48], color=SELECT, thickness=0.035)
        self.play(Create(pitch), run_time=0.55)
        self.step(3, "Pitch = 12 mm; Revolutions = 4", "El paso es el avance axial por vuelta; las revoluciones controlan la longitud total.")
        preview = ParametricFunction(
            lambda t: np.array([1.20 * math.cos(t), 1.20 * math.sin(t), 0.17 * t - 2.10]),
            t_range=[0, 8 * PI, 0.035], color=PREVIEW, stroke_width=10,
        ).set_opacity(0.60)
        self.play(Create(preview), profile.animate.set_opacity(0.25), run_time=2.2)
        self.step(4, "Inspecciona sentido y longitud", "Invierte la dirección si la hélice avanza al lado incorrecto; verifica pitch × vueltas.")
        helix = ParametricFunction(
            lambda t: np.array([1.20 * math.cos(t), 1.20 * math.sin(t), 0.17 * t - 2.10]),
            t_range=[0, 8 * PI, 0.035], color=STEEL_DARK, stroke_width=12,
        )
        self.play(ReplacementTransform(preview, helix), FadeOut(profile), FadeOut(pitch), run_time=0.9)
        self.step(5, "OK → Coil1", "Coil1 guarda tipo de cálculo, paso, vueltas, perfil y eje para edición posterior.")
        self.finish("Resultado: hélice de cuatro vueltas generada paramétricamente a partir de perfil y centerline.")
