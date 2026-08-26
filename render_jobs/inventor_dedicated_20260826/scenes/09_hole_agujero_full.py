from manim import *

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorHoleDetailed(InventorOperationScene):
    """Dedicated Autodesk Inventor Hole lesson using the established CAD UI grammar."""

    OPERATION = "Hole"
    FEATURE_NODE = "Hole1"

    def construct(self):
        self.install_hud(
            [
                ("Placement", "From Sketch"),
                ("Hole Type", "Simple"),
                ("Diameter", "12 mm"),
                ("Termination", "Through All"),
            ],
            [
                "Part1.ipt",
                "Origin",
                "Sketch1",
                "Extrusion1",
                "Sketch2",
                "Hole1",
            ],
        )

        # The consolidated ribbon did not previously contain Hole; overlay the
        # active Inventor-style tool button in the Modify/Create region.
        hole_button = self._tool_button("Hole", -0.90, 3.29, active=True, width=0.86)
        self.add_fixed_in_frame_mobjects(hole_button)

        self.intro(
            "Agujero: parte de un sólido, define una referencia de colocación, configura tipo/diámetro/terminación y elimina material de forma paramétrica."
        )

        plate = animate_rect_sketch_to_extrusion(
            self,
            width=5.8,
            depth=2.85,
            height=0.52,
            shift=DOWN * 0.34,
            dimensions="100 mm x 50 mm",
            extrusion="10 mm",
            step_start=1,
        )

        selected_face = Rectangle(
            width=5.55,
            height=2.60,
            stroke_color=SELECT,
            stroke_width=3.2,
            fill_color=SELECT,
            fill_opacity=0.10,
        ).shift(DOWN * 0.34 + OUT * 0.275)
        self.play(FadeIn(selected_face), run_time=0.45)
        self.step(
            4,
            "Selecciona la cara superior -> Hole",
            "La operación necesita una cara de entrada estable. Inventor usa esa cara para orientar el eje del agujero y calcular la profundidad.",
        )

        placement = Dot3D(
            point=RIGHT * 1.25 + UP * 0.32 + OUT * 0.30,
            radius=0.075,
            color=SELECT,
        )
        guide_x = DashedLine(
            LEFT * 1.60 + UP * 0.32 + OUT * 0.30,
            RIGHT * 1.25 + UP * 0.32 + OUT * 0.30,
            color=UI_MID,
            dash_length=0.10,
        )
        guide_y = DashedLine(
            RIGHT * 1.25 + DOWN * 1.05 + OUT * 0.30,
            RIGHT * 1.25 + UP * 0.32 + OUT * 0.30,
            color=UI_MID,
            dash_length=0.10,
        )
        self.play(FadeIn(placement), Create(guide_x), Create(guide_y), run_time=0.65)
        self.step(
            5,
            "Placement -> From Sketch / punto acotado",
            "Ubica un punto de croquis y acótalo desde referencias funcionales. Si cambia la pieza, esas cotas mantienen la posición del Hole1.",
        )

        hole_profile = Circle(radius=0.35, color=SKETCH, stroke_width=5).move_to(placement.get_center())
        self.play(Create(hole_profile), run_time=0.45)
        self.step(
            6,
            "Hole Type = Simple; Diameter = 12 mm",
            "El diámetro pertenece a Hole1, no a una extrusión negativa improvisada. Para tornillería también puedes elegir Clearance, Tapped, Counterbore o Countersink.",
        )

        drill_axis = Arrow3D(
            start=placement.get_center() + OUT * 0.95,
            end=placement.get_center() + IN * 1.15,
            color=SELECT,
            thickness=0.016,
            height=0.20,
            base_radius=0.075,
        )
        cut_preview = cylinder(0.35, 1.30, PREVIEW, 0.42).move_to(
            [placement.get_center()[0], placement.get_center()[1], 0.0]
        )
        self.play(Create(drill_axis), FadeIn(cut_preview), run_time=0.70)
        self.step(
            7,
            "Termination = Through All",
            "Through All atraviesa todo el espesor aunque la placa cambie después. Distance sirve cuando necesitas una profundidad ciega controlada.",
        )

        # Simulated Boolean cut: a dark internal cylinder is rendered flush with
        # the plate so the viewer reads the feature as removed material.
        hole_void = cylinder(0.35, 0.56, UI_DARK_2, 1.0).move_to(
            [placement.get_center()[0], placement.get_center()[1], 0.0]
        )
        self.play(
            FadeOut(selected_face),
            FadeOut(hole_profile),
            FadeOut(cut_preview),
            FadeOut(guide_x),
            FadeOut(guide_y),
            FadeOut(placement),
            FadeOut(drill_axis),
            FadeIn(hole_void),
            run_time=0.85,
        )
        self.step(
            8,
            "Preview -> verifica orientación, diámetro y profundidad",
            "Antes de OK confirma que la flecha atraviesa la cara correcta, que el diámetro corresponde al diseño y que la terminación no corta geometría no deseada.",
        )

        finish_feature(
            self,
            9,
            "Resultado: Hole1 queda en el árbol del modelo como una operación paramétrica editable, asociada a la cara y al punto de colocación.",
        )
