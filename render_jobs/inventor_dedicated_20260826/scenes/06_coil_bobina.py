from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import _fixed_badge, finish_feature
import math
import numpy as np


class InventorCoilDetailed(InventorOperationScene):
    OPERATION = "Coil"
    FEATURE_NODE = "Coil1"

    def construct(self):
        self.install_hud(
            [("Profile", "Sketch1 circle"), ("Axis", "Centerline"), ("Pitch", "12 mm"), ("Revolutions", "4")],
            ["Part1.ipt", "Origin", "Sketch1", "Centerline", "Coil1"],
        )
        self.intro("Bobina: transformar un perfil 2D y una línea de centro en una geometría helicoidal 3D controlada por paso y revoluciones.")

        badge = _fixed_badge(
            self,
            "SKETCH MODE  |  XZ Plane  |  Sketch1",
            "Profile diameter 4 mm   |   Centerline constrained   |   Fully Constrained",
        )
        axis = DashedLine(start=IN * 2.35, end=OUT * 2.35, color=UI_MID, dash_length=0.18, stroke_width=3)
        profile = Circle(radius=0.20, color=SKETCH, stroke_width=5).rotate(90 * DEGREES, axis=UP).shift(RIGHT * 1.20 + IN * 2.10)
        self.play(Create(axis), FadeIn(profile), run_time=0.8)
        self.step(1, "Start 2D Sketch -> XZ Plane", "Selecciona un plano que contenga el eje de la bobina. El perfil y la centerline deben pertenecer al mismo croquis o tener referencias estables.")
        self.step(2, "Dibuja el perfil y la Centerline", "Acota el diámetro del perfil, la distancia radial al eje y restringe la línea de centro para definir el diámetro medio de la hélice.")
        self.play(FadeOut(badge), run_time=0.25)
        self.remove_fixed_in_frame_mobjects(badge)

        self.step(3, "Finish Sketch -> 3D Model -> Create -> Coil", "Selecciona primero el perfil cerrado y después la Centerline como Axis. Inventor establece la relación de giro y avance axial.")
        pitch = Line3D(start=[1.72, 0, -1.55], end=[1.72, 0, -0.48], color=SELECT, thickness=0.035)
        self.play(Create(pitch), run_time=0.55)

        self.step(4, "Pitch = 12 mm; Revolutions = 4", "Pitch es el avance axial por vuelta. Con cuatro revoluciones, la longitud axial ideal es pitch multiplicado por el número de vueltas.")
        preview = ParametricFunction(
            lambda t: np.array([1.20 * math.cos(t), 1.20 * math.sin(t), 0.17 * t - 2.10]),
            t_range=[0, 8 * PI, 0.035],
            color=PREVIEW,
            stroke_width=10,
        ).set_opacity(0.60)
        self.play(Create(preview), profile.animate.set_opacity(0.25), run_time=2.2)

        self.step(5, "Observa cómo el croquis se convierte en una hélice 3D", "La sección circular recorre una trayectoria helicoidal alrededor del eje; paso y revoluciones gobiernan la geometría completa.")
        self.step(6, "Verifica sentido, longitud y separación", "Usa Flip Direction si la hélice avanza al lado incorrecto y confirma que las vueltas no se intersecten.")

        helix = ParametricFunction(
            lambda t: np.array([1.20 * math.cos(t), 1.20 * math.sin(t), 0.17 * t - 2.10]),
            t_range=[0, 8 * PI, 0.035],
            color=STEEL_DARK,
            stroke_width=12,
        )
        self.play(ReplacementTransform(preview, helix), FadeOut(profile), FadeOut(pitch), run_time=0.9)
        self.step(7, "OK -> Coil1", "El Browser guarda perfil, eje, tipo de cálculo, pitch y revoluciones. Cualquier parámetro puede editarse después.")
        finish_feature(self, 8, "Resultado: hélice 3D de cuatro vueltas generada paramétricamente a partir de un croquis 2D y una centerline.")
