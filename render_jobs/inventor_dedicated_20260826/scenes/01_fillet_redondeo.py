from manim import *
from library.inventor_pro_ui import *


class InventorFilletDetailed(InventorOperationScene):
    OPERATION = "Fillet"
    FEATURE_NODE = "Fillet1"

    def construct(self):
        self.install_hud(
            [("Selection", "1 Edge"), ("Radius", "8 mm"), ("Continuity", "Tangent"), ("Mode", "Constant")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1"],
        )
        self.intro("Redondeo de aristas: sustituir una arista viva por una transición tangente de radio controlado.")

        raw = cuboid(4.4, 2.55, 0.75, STEEL).shift(DOWN * 0.30)
        self.play(FadeIn(raw, scale=0.94), run_time=0.8)
        self.step(1, "Identifica la arista", "El redondeo modifica aristas existentes; no necesita un croquis nuevo.")

        selected = Line3D(start=[2.2, -1.575, 0.375], end=[2.2, 0.975, 0.375],
                          color=SELECT, thickness=0.045)
        self.play(Create(selected), run_time=0.55)
        self.step(2, "3D Model → Modify → Fillet", "Activa Fillet y selecciona la arista. Inventor la resalta como referencia del feature.")

        radius_arc = Arc(radius=0.55, start_angle=0, angle=PI / 2, color=SELECT, stroke_width=5)
        radius_arc.rotate(90 * DEGREES, RIGHT).shift([1.73, 0.71, 0.42])
        self.play(Create(radius_arc), run_time=0.55)
        self.step(3, "Define Radius = 8 mm", "Para Constant Radius, un único valor R gobierna toda la transición seleccionada.")

        preview = rounded_plate(4.4, 2.55, 0.75, 0.42, PREVIEW).shift(DOWN * 0.30).set_opacity(0.54)
        self.play(FadeOut(raw, run_time=0.25), FadeIn(preview, run_time=0.65), selected.animate.set_opacity(0.35))
        self.step(4, "Inspecciona la vista previa", "Comprueba que el radio no invada agujeros, paredes delgadas o aristas vecinas.")

        result = rounded_plate(4.4, 2.55, 0.75, 0.42, STEEL).shift(DOWN * 0.30)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(selected), FadeOut(radius_arc), run_time=0.75)
        self.step(5, "Confirma con OK", "El Browser agrega Fillet1. Editar ese nodo permite cambiar el radio sin rehacer el sólido.")
        self.finish("Resultado: arista suave, tangente y completamente paramétrica mediante Fillet1.")
