from manim import *
from library.inventor_pro_ui import *


class InventorMirrorDetailed(InventorOperationScene):
    OPERATION = "Mirror"
    FEATURE_NODE = "Mirror1"

    def construct(self):
        self.install_hud(
            [("Features", "3 selected"), ("Mirror Plane", "YZ Plane"), ("Method", "Identical"), ("Result", "Join")],
            ["Part1.ipt", "Origin", "YZ Plane", "Sketch1", "Extrusion1", "Hole1"],
        )
        self.intro("Simetría: reutilizar operaciones existentes respecto a un plano estable en lugar de modelar dos veces.")
        half = VGroup(
            cuboid(2.10, 2.50, 0.52, STEEL).shift(RIGHT * 1.05 + DOWN * 0.32),
            cuboid(0.40, 2.50, 1.85, STEEL_DARK).shift(RIGHT * 0.20 + DOWN * 0.32 + OUT * 0.67),
            cylinder(0.34, 0.66, STEEL).shift(RIGHT * 1.25 + DOWN * 0.32 + OUT * 0.50),
        )
        self.play(LaggedStart(*[FadeIn(m, scale=0.94) for m in half], lag_ratio=0.10), run_time=0.9)
        self.step(1, "Modela solo la mitad", "La simetría funciona mejor cuando la intención de diseño usa un plano medio claro y estable.")
        plane = Rectangle(width=3.45, height=2.90, stroke_color=SELECT, stroke_width=2,
                          fill_color=SELECT, fill_opacity=0.12)
        plane.rotate(90 * DEGREES, axis=UP).shift(DOWN * 0.32 + OUT * 0.45)
        self.play(FadeIn(plane), run_time=0.55)
        self.step(2, "3D Model → Pattern → Mirror", "En Features selecciona las operaciones que se van a reflejar; evita seleccionar geometría irrelevante.")
        self.step(3, "Selecciona YZ Plane", "El plano de simetría define posición y orientación. Puede ser un Origin Plane o Work Plane.")
        mirrored = half.copy().flip(RIGHT).set_opacity(0.18)
        self.add(mirrored)
        self.play(mirrored.animate.set_opacity(0.58).set_color(PREVIEW), run_time=0.8)
        self.step(4, "Revisa la vista previa", "Confirma orientación, unión y features incluidos antes de crear la copia definitiva.")
        final_mirror = half.copy().flip(RIGHT)
        self.play(FadeOut(mirrored), FadeIn(final_mirror), plane.animate.set_opacity(0.05), run_time=0.75)
        self.step(5, "OK → Mirror1", "Editar Mirror1 cambia el plano o el conjunto de operaciones reflejadas sin duplicar trabajo.")
        self.finish("Resultado: pieza bilateral consistente y paramétrica a partir de una única mitad modelada.")
