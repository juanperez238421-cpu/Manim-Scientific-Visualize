from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorChamferDetailed(InventorOperationScene):
    OPERATION = "Chamfer"
    FEATURE_NODE = "Chamfer1"

    def construct(self):
        self.install_hud(
            [("Selection", "1 Edge"), ("Type", "Distance + Angle"), ("Distance", "6 mm"), ("Angle", "45 deg")],
            ["Part1.ipt", "Origin", "Sketch1", "Extrusion1", "Chamfer1"],
        )
        self.intro("Chaflán: construir primero el sólido desde un croquis 2D y después sustituir una arista por una cara plana controlada.")

        raw = animate_rect_sketch_to_extrusion(
            self,
            width=4.4,
            depth=2.55,
            height=0.78,
            shift=DOWN * 0.30,
            dimensions="70 mm x 45 mm",
            extrusion="12 mm",
            step_start=1,
        )

        self.step(4, "Selecciona la arista a biselar", "Chamfer trabaja sobre aristas del sólido terminado y genera una cara plana entre las dos caras adyacentes.")
        edge = Line3D(start=[-2.2, 0.975, -0.39], end=[2.2, 0.975, -0.39], color=SELECT, thickness=0.05)
        self.play(Create(edge), run_time=0.55)

        self.step(5, "3D Model -> Modify -> Chamfer", "Escoge el método Distance + Angle. Inventor usa la arista seleccionada y una cara de referencia para orientar el bisel.")
        self.step(6, "Distance = 6 mm; Angle = 45 deg", "La distancia controla el retiro desde la arista y el ángulo gobierna la inclinación de la nueva cara.")

        pts = [(-2.2, -1.275), (2.2, -1.275), (2.2, 0.60), (1.57, 1.275), (-2.2, 1.275)]
        preview = extruded_polygon(pts, 0.78, PREVIEW, 0.58).shift(DOWN * 0.30)
        self.play(FadeOut(raw, run_time=0.25), FadeIn(preview, run_time=0.65), edge.animate.set_opacity(0.35))
        self.step(7, "Comprueba la orientación de la vista previa", "Si la cara inclinada aparece en el lado incorrecto, cambia la referencia o usa Flip Direction antes de aceptar.")

        result = extruded_polygon(pts, 0.78, STEEL, 1.0).shift(DOWN * 0.30)
        self.play(FadeOut(preview), FadeIn(result), FadeOut(edge), run_time=0.75)
        self.step(8, "OK -> Chamfer1", "El Browser registra Chamfer1 como feature dependiente de Extrusion1 y conserva distancia, ángulo y selección.")
        finish_feature(self, 9, "Resultado: cara inclinada de 6 mm a 45 grados, editable sin modificar el croquis base.")
