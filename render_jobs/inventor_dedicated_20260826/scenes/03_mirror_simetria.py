from manim import *
from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorMirrorDetailed(InventorOperationScene):
    OPERATION = "Mirror"
    FEATURE_NODE = "Mirror1"

    def construct(self):
        self.install_hud(
            [("Features", "3 selected"), ("Mirror Plane", "YZ Plane"), ("Method", "Identical"), ("Result", "Join")],
            ["Part1.ipt", "Origin", "YZ Plane", "Sketch1", "Extrusion1", "Hole1", "Mirror1"],
        )
        self.intro("Simetría: construir una sola mitad desde el croquis y reutilizar sus operaciones respecto a un plano medio estable.")

        base_half = animate_rect_sketch_to_extrusion(
            self,
            width=2.10,
            depth=2.50,
            height=0.52,
            shift=RIGHT * 1.05 + DOWN * 0.32,
            dimensions="35 mm x 45 mm",
            extrusion="8 mm",
            step_start=1,
        )

        self.step(4, "Completa solo la mitad funcional", "Agrega únicamente los features necesarios en un lado. La intención de diseño evita modelar dos veces geometría equivalente.")
        wall = cuboid(0.40, 2.50, 1.85, STEEL_DARK).shift(RIGHT * 0.20 + DOWN * 0.32 + OUT * 0.67)
        boss = cylinder(0.34, 0.66, STEEL).shift(RIGHT * 1.25 + DOWN * 0.32 + OUT * 0.50)
        self.play(FadeIn(wall), FadeIn(boss), run_time=0.75)
        half = VGroup(base_half, wall, boss)

        plane = Rectangle(
            width=3.45,
            height=2.90,
            stroke_color=SELECT,
            stroke_width=2,
            fill_color=SELECT,
            fill_opacity=0.12,
        )
        plane.rotate(90 * DEGREES, axis=UP).shift(DOWN * 0.32 + OUT * 0.45)
        self.play(FadeIn(plane), run_time=0.55)
        self.step(5, "Selecciona el plano medio YZ", "El plano de simetría define posición y orientación. Conviene usar un Origin Plane o Work Plane estable y no una cara temporal.")

        self.step(6, "3D Model -> Pattern -> Mirror", "En Features selecciona las operaciones que se reflejarán; no selecciones geometría irrelevante ni dependencias que deban permanecer únicas.")
        mirrored = half.copy().flip(RIGHT).set_opacity(0.18)
        self.add(mirrored)
        self.play(mirrored.animate.set_opacity(0.58).set_color(PREVIEW), run_time=0.8)

        self.step(7, "Revisa la vista previa bilateral", "Comprueba orientación, unión y features incluidos. La copia debe aparecer al lado opuesto del YZ Plane sin solapamientos.")
        final_mirror = half.copy().flip(RIGHT)
        self.play(FadeOut(mirrored), FadeIn(final_mirror), plane.animate.set_opacity(0.05), run_time=0.75)

        self.step(8, "OK -> Mirror1", "El Browser conserva Mirror1 con el plano y el conjunto de features. Editar la mitad original actualiza también la copia.")
        finish_feature(self, 9, "Resultado: pieza bilateral consistente y paramétrica creada a partir de una única mitad modelada.")
