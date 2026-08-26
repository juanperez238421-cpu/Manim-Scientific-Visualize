from manim import *

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import _fixed_badge, finish_feature

import math
import numpy as np


RADIUS = 1.35
SECTION_RADIUS = 0.22
TURNS = 4
PITCH_WORLD = 1.08
Z0 = -2.12
K = PITCH_WORLD / TAU


def helix_center(t: float) -> np.ndarray:
    return np.array([
        RADIUS * math.cos(t),
        RADIUS * math.sin(t),
        Z0 + K * t,
    ])


def helix_curve(color=PREVIEW, width: float = 9.0, opacity: float = 0.68) -> ParametricFunction:
    return ParametricFunction(
        helix_center,
        t_range=[0, TURNS * TAU, 0.035],
        color=color,
        stroke_width=width,
    ).set_opacity(opacity)


def helix_tube(color=STEEL, opacity: float = 1.0) -> Surface:
    """Tubular spring surface built around the helical centerline."""
    norm = math.sqrt(RADIUS**2 + K**2)

    def surface_point(u: float, v: float) -> np.ndarray:
        c = helix_center(u)
        er = np.array([math.cos(u), math.sin(u), 0.0])
        e2 = np.array([
            -K * math.sin(u) / norm,
            K * math.cos(u) / norm,
            -RADIUS / norm,
        ])
        return c + SECTION_RADIUS * (math.cos(v) * er + math.sin(v) * e2)

    return Surface(
        surface_point,
        u_range=[0, TURNS * TAU],
        v_range=[0, TAU],
        resolution=(64, 10),
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=UI_MID,
        stroke_width=0.45,
    )


class InventorCoilDetailed(InventorOperationScene):
    """Full Autodesk Inventor Coil / Bobina lesson in the consolidated CAD format."""

    OPERATION = "Coil"
    FEATURE_NODE = "Coil1"

    def construct(self):
        self.install_hud(
            [
                ("Profile", "Sketch1 circle"),
                ("Axis", "Centerline"),
                ("Type", "Pitch & Revolution"),
                ("Pitch", "12 mm"),
                ("Revolutions", "4"),
                ("Operation", "New Solid"),
            ],
            [
                "Part1.ipt",
                "Origin",
                "Sketch1",
                "Centerline",
                "Coil1",
            ],
        )

        self.intro(
            "Bobina: combina un perfil 2D y un eje de croquis para generar un sólido helicoidal 3D controlado por paso, revoluciones, dirección y operación."
        )

        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.93, run_time=0.82)
        badge = _fixed_badge(
            self,
            "SKETCH MODE  |  XZ Plane  |  Sketch1",
            "Circle Ø4 mm   |   Mean radius 18 mm   |   Centerline constrained",
        )
        self.step(
            1,
            "Start 2D Sketch -> XZ Plane",
            "Elige un plano que contenga el eje de la bobina. Trabajar normal al plano facilita acotar perfil, radio medio y Centerline sin ambigüedad.",
            2.65,
        )

        axis = DashedLine(
            start=np.array([0.0, 0.0, -2.55]),
            end=np.array([0.0, 0.0, 2.55]),
            color=UI_MID,
            dash_length=0.13,
            stroke_width=3.0,
        )
        axis_end_1 = Dot3D([0, 0, -2.55], radius=0.045, color=UI_MID)
        axis_end_2 = Dot3D([0, 0, 2.55], radius=0.045, color=UI_MID)
        self.play(Create(axis), FadeIn(axis_end_1), FadeIn(axis_end_2), run_time=0.78)
        self.step(
            2,
            "Dibuja una Centerline -> será el Axis",
            "La línea de centro define el eje geométrico de giro y avance. Restringe su posición para que la bobina permanezca estable cuando el croquis sea editado.",
            2.70,
        )

        profile_center = np.array([RADIUS, 0.0, Z0])
        profile = Circle(radius=SECTION_RADIUS, color=SKETCH, stroke_width=5.2)
        profile.rotate(90 * DEGREES, axis=RIGHT)
        profile.move_to(profile_center)
        center_dot = Dot3D(profile_center, radius=0.060, color=SELECT)
        radial_dim = Line3D(
            start=np.array([0.0, 0.0, Z0]),
            end=profile_center,
            color=SELECT,
            thickness=0.018,
        )
        self.play(Create(profile), FadeIn(center_dot), Create(radial_dim), run_time=0.82)
        self.step(
            3,
            "Dibuja el perfil Ø4 mm y acota su distancia al eje",
            "El diámetro del círculo controla el espesor del alambre; la distancia entre su centro y la Centerline controla el diámetro medio de la bobina.",
            2.85,
        )

        self.play(FadeOut(badge), run_time=0.25)
        self.remove_fixed_in_frame_mobjects(badge)
        self.step(
            4,
            "Finish Sketch -> conserva Profile + Centerline",
            "No elimines el croquis: Coil1 dependerá de estas dos referencias. Editar Sketch1 después debe reconstruir diámetro del alambre y diámetro medio.",
            2.65,
        )
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.92)

        self.step(
            5,
            "3D Model -> Create -> Coil",
            "Selecciona el círculo como Profile y la Centerline como Axis. La vista previa debe iniciar exactamente desde la sección circular del croquis.",
            2.75,
        )
        self.play(
            profile.animate.set_color(SELECT),
            axis.animate.set_color(SELECT),
            radial_dim.animate.set_opacity(0.25),
            run_time=0.55,
        )
        self.flash_status("Coil     |     Profile: Sketch1 circle     |     Axis: Centerline")

        self.step(
            6,
            "Coil Size -> Type = Pitch and Revolution",
            "Este modo usa dos parámetros independientes: Pitch controla el avance axial por vuelta y Revolutions controla cuántas vueltas completas se generan.",
            2.90,
        )

        pitch_start = np.array([1.92, 0.0, Z0])
        pitch_end = np.array([1.92, 0.0, Z0 + PITCH_WORLD])
        pitch_line = Line3D(pitch_start, pitch_end, color=SELECT, thickness=0.022)
        pitch_tick_1 = Line3D(
            pitch_start + LEFT * 0.18,
            pitch_start + RIGHT * 0.18,
            color=SELECT,
            thickness=0.016,
        )
        pitch_tick_2 = Line3D(
            pitch_end + LEFT * 0.18,
            pitch_end + RIGHT * 0.18,
            color=SELECT,
            thickness=0.016,
        )
        self.play(Create(pitch_line), Create(pitch_tick_1), Create(pitch_tick_2), run_time=0.62)
        self.step(
            7,
            "Pitch = 12 mm -> separación axial por cada vuelta",
            "Aumentar Pitch separa las espiras; reducirlo las acerca. Verifica siempre que el perfil no se auto-intersecte para el diámetro de alambre elegido.",
            2.90,
        )

        self.step(
            8,
            "Revolutions = 4 -> longitud axial ideal = 48 mm",
            "Cuatro vueltas de 12 mm producen 48 mm de avance axial. Este valor permite anticipar el espacio ocupado antes de aceptar Coil1.",
            2.85,
        )

        preview_path = helix_curve(PREVIEW, width=8.5, opacity=0.60)
        tracer = Dot3D(helix_center(0), radius=0.070, color=SELECT)
        self.step(
            9,
            "Direction / Rotation -> define hacia dónde avanza la hélice",
            "Usa Flip Direction o invierte el sentido de rotación si la bobina crece al lado incorrecto. El croquis inicial permanece fijo como referencia.",
            2.75,
        )
        self.play(
            Create(preview_path),
            MoveAlongPath(tracer, preview_path),
            profile.animate.set_opacity(0.30),
            run_time=2.65,
            rate_func=linear,
        )

        self.step(
            10,
            "Preview -> el perfil recorre una trayectoria helicoidal 3D",
            "La sección circular no se extruye en línea recta: gira alrededor del Axis mientras avanza axialmente. Esa combinación produce la geometría de Coil.",
            3.00,
        )
        self.begin_ambient_camera_rotation(rate=0.065)
        self.wait(1.65)
        self.stop_ambient_camera_rotation()

        preview_tube = helix_tube(PREVIEW, 0.52)
        self.play(
            FadeIn(preview_tube),
            preview_path.animate.set_opacity(0.20),
            FadeOut(tracer),
            run_time=1.15,
        )
        self.step(
            11,
            "Solid Preview -> verifica diámetro, separación y colisiones",
            "Inspecciona la bobina como volumen: confirma que las espiras no se toquen, que el diámetro medio sea correcto y que el resultado ocupe el espacio previsto.",
            3.05,
        )

        final_tube = helix_tube(STEEL, 1.0)
        self.play(
            FadeOut(preview_path),
            FadeOut(preview_tube),
            FadeOut(profile),
            FadeOut(center_dot),
            FadeOut(radial_dim),
            FadeOut(pitch_line),
            FadeOut(pitch_tick_1),
            FadeOut(pitch_tick_2),
            FadeOut(axis_end_1),
            FadeOut(axis_end_2),
            axis.animate.set_color(UI_MID).set_opacity(0.22),
            FadeIn(final_tube),
            run_time=1.10,
        )
        self.step(
            12,
            "OK -> Coil1 aparece en el Model Browser",
            "Coil1 guarda Profile, Axis, Type, Pitch, Revolutions y Operation. Cada parámetro puede editarse después sin reconstruir manualmente la geometría.",
            3.05,
        )

        finish_feature(
            self,
            13,
            "Resultado: un círculo 2D y una Centerline se convirtieron en una bobina tubular 3D de cuatro vueltas, totalmente paramétrica y editable.",
        )
