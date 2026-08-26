from manim import *
import math

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import _fixed_badge, finish_feature


class InventorCircularPatternFull(InventorOperationScene):
    """Full circular pattern lesson using a real Hole-like seed around the Z axis."""

    OPERATION = "Circular Pattern"
    FEATURE_NODE = "CircularPattern1"

    def construct(self):
        self.install_hud(
            [
                ("Features", "Hole1"),
                ("Rotation Axis", "Z Axis"),
                ("Placement", "Full 360 deg"),
                ("Quantity", "8"),
            ],
            [
                "Part1.ipt",
                "Origin",
                "Z Axis",
                "Sketch1",
                "Extrusion1",
                "Sketch2",
                "Hole1",
                "CircularPattern1",
            ],
        )
        self.intro(
            "Patrón circular: crea una sola operación semilla, selecciona un eje estable y distribuye ocurrencias uniformemente alrededor de 360 grados."
        )

        # 2D disk sketch.
        self.move_camera(phi=4 * DEGREES, theta=-90 * DEGREES, zoom=0.90, run_time=0.75)
        badge = _fixed_badge(
            self,
            "SKETCH MODE  |  XY Plane  |  Sketch1",
            "Base circle diameter 90 mm   |   Center coincident with origin",
        )
        base_sketch = Circle(radius=2.25, color=SKETCH, stroke_width=5).shift(DOWN * 0.30)
        center = Dot(base_sketch.get_center(), radius=0.055, color=SELECT)
        self.play(Create(base_sketch), FadeIn(center), run_time=0.85)
        self.step(
            1,
            "Start 2D Sketch -> círculo base centrado",
            "Haz coincidir el centro con el origen y acota el diámetro. El origen estable servirá después como referencia natural del eje del patrón.",
        )

        self.play(FadeOut(badge), run_time=0.25)
        self.remove_fixed_in_frame_mobjects(badge)
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.90)
        disk_preview = cylinder(2.25, 0.05, PREVIEW, 0.48).shift(DOWN * 0.30)
        self.play(FadeIn(disk_preview), base_sketch.animate.set_opacity(0.25), run_time=0.45)
        self.play(disk_preview.animate.stretch_to_fit_depth(0.40), run_time=0.90)
        disk = cylinder(2.25, 0.40, STEEL).shift(DOWN * 0.30)
        self.play(
            ReplacementTransform(disk_preview, disk),
            FadeOut(base_sketch),
            FadeOut(center),
            run_time=0.75,
        )
        self.step(
            2,
            "Finish Sketch -> Extrude -> Extrusion1",
            "Extruye el disco 8 mm. La geometría circular y el origen quedan disponibles como referencias robustas para la siguiente operación.",
        )

        hub = cylinder(0.43, 0.52, STEEL_DARK).shift(DOWN * 0.30 + OUT * 0.26)
        self.play(FadeIn(hub), run_time=0.45)
        self.step(
            3,
            "Crea Hole1 como semilla radial",
            "Coloca un único agujero a una distancia radial acotada. El patrón repetirá Hole1 completo, preservando diámetro, terminación y asociatividad.",
        )

        radial = 1.47
        seed_center = RIGHT * radial + DOWN * 0.30
        seed_sketch = Circle(radius=0.24, color=SKETCH, stroke_width=5).shift(seed_center + OUT * 0.22)
        self.play(Create(seed_sketch), run_time=0.50)
        seed_hole = cylinder(0.24, 0.42, UI_DARK_2, 1.0).shift(seed_center)
        self.play(FadeOut(seed_sketch), FadeIn(seed_hole), run_time=0.65)
        self.step(
            4,
            "Hole1 -> Diameter 8 mm; Through All",
            "Una sola semilla bien definida es suficiente. Evita dibujar ocho círculos: perderías el control paramétrico centralizado del patrón.",
        )

        axis = Arrow3D(
            start=DOWN * 0.30 + IN * 0.70,
            end=DOWN * 0.30 + OUT * 1.45,
            color=SELECT,
            thickness=0.017,
            height=0.21,
            base_radius=0.08,
        )
        self.play(Create(axis), run_time=0.55)
        self.step(
            5,
            "3D Model -> Pattern -> Circular",
            "Selecciona Hole1 en Features y Z Axis como Rotation Axis. El eje define el centro geométrico de toda la distribución.",
        )

        angle_arc = Arc(
            radius=0.86,
            start_angle=0,
            angle=TAU / 8,
            color=SELECT,
            stroke_width=4,
        ).shift(DOWN * 0.30 + OUT * 0.24)
        self.play(Create(angle_arc), run_time=0.45)
        self.step(
            6,
            "Placement = Full; Quantity = 8",
            "Full distribuye las ocho ocurrencias en 360 grados. El incremento uniforme es 360/8 = 45 grados entre centros consecutivos.",
        )

        preview = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            preview.add(
                seed_hole.copy()
                .move_to([
                    radial * math.cos(angle),
                    radial * math.sin(angle) - 0.30,
                    0.0,
                ])
                .set_color(PREVIEW)
                .set_opacity(0.26)
            )
        self.add(preview)
        self.play(
            LaggedStart(*[hole.animate.set_opacity(0.64) for hole in preview], lag_ratio=0.08),
            run_time=1.20,
        )
        self.step(
            7,
            "Preview -> ocho ocurrencias alrededor del eje",
            "La vista previa permite verificar rápidamente separación, cobertura y orientación antes de crear CircularPattern1.",
        )

        self.step(
            8,
            "Comprueba eje y radial de la semilla",
            "Si eliges un eje desplazado, todo el patrón cambia de centro. Si el radio de Hole1 es incorrecto, las ocho ocurrencias heredarán ese error.",
        )

        final = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            final.add(
                seed_hole.copy().move_to([
                    radial * math.cos(angle),
                    radial * math.sin(angle) - 0.30,
                    0.0,
                ])
            )
        self.play(
            FadeOut(preview),
            FadeOut(axis),
            FadeOut(angle_arc),
            FadeIn(final),
            run_time=0.85,
        )
        self.step(
            9,
            "OK -> conserva el patrón como una sola feature",
            "Edita después Quantity, Placement o Rotation Axis desde CircularPattern1; las ocho ocurrencias se recalculan sin redibujar el modelo.",
        )

        finish_feature(
            self,
            10,
            "Resultado: ocho Hole1 uniformes alrededor del eje Z, gobernados por una única operación CircularPattern1 completamente editable.",
        )
