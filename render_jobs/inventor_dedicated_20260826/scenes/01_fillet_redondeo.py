from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorFilletDetailed(InventorOperationScene):
    OPERATION = "Fillet"
    FEATURE_NODE = "Fillet1"

    def construct(self):
        self.install_hud(
            [("Selection", "1 Edge"), ("Radius", "8 mm"), ("Continuity", "Tangent"), ("Mode", "Constant")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1", "Fillet1"],
        )
        self.intro("Redondeo de aristas: desde un croquis 2D completamente restringido hasta una transición 3D tangente y paramétrica.")

        raw = animate_rect_sketch_to_extrusion(
            self,
            width=4.4,
            depth=2.55,
            height=0.75,
            shift=DOWN * 0.30,
            dimensions="70 mm x 45 mm",
            extrusion="12 mm",
            step_start=1,
        )

        self.step(4, "Identifica la arista 3D", "Fillet modifica aristas existentes del sólido. Selecciona solo las aristas que deban compartir el mismo radio.")
        selected = Line3D(
            start=[2.2, -1.575, 0.375],
            end=[2.2, 0.975, 0.375],
            color=SELECT,
            thickness=0.045,
        )
        self.play(Create(selected), run_time=0.55)

        self.step(5, "3D Model -> Modify -> Fillet", "Activa Fillet y confirma que la arista aparece en Selection. El feature queda asociado a esa referencia geométrica.")
        radius_arc = Arc(radius=0.55, start_angle=0, angle=PI / 2, color=SELECT, stroke_width=5)
        radius_arc.rotate(90 * DEGREES, RIGHT).shift([1.73, 0.71, 0.42])
        self.play(Create(radius_arc), run_time=0.55)

        self.step(6, "Define Radius = 8 mm", "En Constant Radius, un único valor R gobierna toda la transición. Un radio excesivo puede invadir caras o detalles vecinos.")
        preview = rounded_plate(4.4, 2.55, 0.75, 0.42, PREVIEW).shift(DOWN * 0.30).set_opacity(0.54)
        self.play(FadeOut(raw, run_time=0.25), FadeIn(preview, run_time=0.65), selected.animate.set_opacity(0.35))

        self.step(7, "Inspecciona la vista previa", "Gira la pieza y comprueba tangencia, continuidad y ausencia de autointersecciones antes de aceptar la operación.")
        result = rounded_plate(4.4, 2.55, 0.75, 0.42, STEEL).shift(DOWN * 0.30)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(selected), FadeOut(radius_arc), run_time=0.75)

        self.step(8, "Confirma con OK y revisa el Browser", "Inventor agrega Fillet1 debajo de Extrusion1. Editar Fillet1 cambia el radio sin reconstruir Sketch1 ni Extrusion1.")
        finish_feature(self, 9, "Resultado: arista suave, tangente y completamente paramétrica mediante Fillet1.")
