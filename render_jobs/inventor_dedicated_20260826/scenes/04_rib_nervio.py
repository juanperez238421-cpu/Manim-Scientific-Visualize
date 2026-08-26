from manim import *

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import animate_rect_sketch_to_extrusion, finish_feature


class InventorRibDetailed(InventorOperationScene):
    """Full Autodesk Inventor Rib / Nervio lesson in the consolidated 2D -> 3D UI format."""

    OPERATION = "Rib"
    FEATURE_NODE = "Rib1"

    def construct(self):
        self.install_hud(
            [
                ("Profile", "Sketch2 line"),
                ("Thickness", "6 mm"),
                ("Direction", "Symmetric"),
                ("Extent", "To Next"),
            ],
            [
                "Part1.ipt",
                "Origin",
                "Sketch1",
                "Extrusion1",
                "Extrusion2",
                "Sketch2",
                "Rib1",
            ],
        )

        self.intro(
            "Nervio: crea primero el sólido anfitrión, dibuja una línea abierta en Sketch2 y conviértela en un refuerzo 3D delgado, conectado y paramétrico."
        )

        # ------------------------------------------------------------------
        # 1-3. Same established grammar as Hole / Extrusion:
        # stable plane -> constrained 2D sketch -> host solid.
        # ------------------------------------------------------------------
        base = animate_rect_sketch_to_extrusion(
            self,
            width=5.55,
            depth=3.00,
            height=0.48,
            shift=DOWN * 0.38,
            dimensions="90 mm x 50 mm",
            extrusion="8 mm",
            step_start=1,
        )

        # ------------------------------------------------------------------
        # 4. Build the second host face. Rib must join existing material.
        # ------------------------------------------------------------------
        self.step(
            4,
            "Crea la pared que recibirá el refuerzo",
            "El nervio trabaja entre caras existentes. Esta pared vertical será la cara límite que encontrará Extent = To Next.",
        )
        wall = cuboid(0.50, 3.00, 2.75, STEEL_DARK, 1.0).shift(
            LEFT * 2.53 + DOWN * 0.38 + OUT * 1.14
        )
        self.play(FadeIn(wall), run_time=0.72)
        self.flash_status("Extrusion2 created     |     Host geometry ready for Rib1")
        self.wait(0.55)

        # ------------------------------------------------------------------
        # 5. Select a stable sketch plane and orient normal to it.
        # ------------------------------------------------------------------
        self.step(
            5,
            "Selecciona la cara lateral -> Start 2D Sketch",
            "Para controlar el perfil del nervio, trabaja normal al plano. La línea quedará definida en una vista 2D antes de generar espesor.",
        )
        face_highlight = cuboid(0.035, 2.78, 2.48, SELECT, 0.18).shift(
            LEFT * 2.25 + DOWN * 0.38 + OUT * 1.13
        )
        self.play(FadeIn(face_highlight), run_time=0.42)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=0.82)

        # ------------------------------------------------------------------
        # 6. Open profile. A Rib is intentionally NOT a closed region.
        # ------------------------------------------------------------------
        p0 = np.array([-2.25, -0.38, 0.28])
        p1 = np.array([0.92, -0.38, 2.16])
        rib_line = Line3D(start=p0, end=p1, color=SKETCH, thickness=0.052)
        start_dot = Dot3D(p0, radius=0.065, color=SELECT)
        end_dot = Dot3D(p1, radius=0.065, color=SELECT)
        self.play(Create(rib_line), FadeIn(start_dot), FadeIn(end_dot), run_time=0.72)
        self.step(
            6,
            "Sketch2 -> dibuja y restringe UNA LÍNEA ABIERTA",
            "Acota los extremos y la inclinación. No cierres un contorno: Rib usa la línea como eje geométrico para construir una pared delgada.",
            2.70,
        )

        # ------------------------------------------------------------------
        # 7. Finish Sketch and recover isometric 3D inspection.
        # ------------------------------------------------------------------
        self.step(
            7,
            "Finish Sketch -> conserva Sketch2 como entrada",
            "Al salir del croquis, la línea sigue asociada al modelo. Si luego editas Sketch2, Inventor puede reconstruir la posición e inclinación del nervio.",
        )
        self.play(FadeOut(face_highlight), FadeOut(start_dot), FadeOut(end_dot), run_time=0.30)
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.82)

        # ------------------------------------------------------------------
        # 8. Activate Rib and confirm profile selection.
        # ------------------------------------------------------------------
        self.step(
            8,
            "3D Model -> Create -> Rib",
            "Activa Rib y confirma Sketch2 line en Profile. La vista previa debe nacer exactamente sobre la línea abierta seleccionada.",
        )
        selected_line = rib_line.copy().set_color(SELECT).set_opacity(1.0)
        self.play(Transform(rib_line, selected_line), run_time=0.45)
        self.flash_status("Rib     |     Profile selected: Sketch2 line")

        # Rib prism lies in the X-Z plane and is thickened symmetrically in Y.
        full_pts = [(-2.25, -0.18), (-2.25, 2.02), (0.92, -0.18)]
        short_pts = [(-2.25, -0.18), (-2.25, 1.27), (0.02, -0.18)]
        preview_short = extruded_polygon(short_pts, 0.38, PREVIEW, 0.48).rotate(
            90 * DEGREES, axis=RIGHT
        ).shift(DOWN * 0.38)
        preview_full = extruded_polygon(full_pts, 0.38, PREVIEW, 0.54).rotate(
            90 * DEGREES, axis=RIGHT
        ).shift(DOWN * 0.38)

        # ------------------------------------------------------------------
        # 9. Thickness: make the material generation explicit.
        # ------------------------------------------------------------------
        self.play(FadeIn(preview_short), rib_line.animate.set_opacity(0.30), run_time=0.66)
        arrow_left = Arrow3D(
            start=[-1.28, -0.38, 1.10],
            end=[-1.28, -0.88, 1.10],
            color=SELECT,
            thickness=0.015,
            height=0.16,
            base_radius=0.055,
        )
        arrow_right = Arrow3D(
            start=[-1.28, -0.38, 1.10],
            end=[-1.28, 0.12, 1.10],
            color=SELECT,
            thickness=0.015,
            height=0.16,
            base_radius=0.055,
        )
        self.play(Create(arrow_left), Create(arrow_right), run_time=0.48)
        self.step(
            9,
            "Thickness = 6 mm -> Direction = Symmetric",
            "El espesor se reparte a ambos lados de Sketch2. La línea permanece como referencia central mientras la operación genera material real.",
            2.75,
        )

        # ------------------------------------------------------------------
        # 10. Extent = To Next: visibly extend until neighboring faces.
        # ------------------------------------------------------------------
        self.step(
            10,
            "Extent = To Next -> extiende hasta las caras vecinas",
            "To Next evita una altura arbitraria: el nervio crece hasta encontrar el sólido siguiente y mantiene contacto con base y pared.",
            2.70,
        )
        self.play(
            ReplacementTransform(preview_short, preview_full),
            FadeOut(arrow_left),
            FadeOut(arrow_right),
            run_time=1.05,
        )

        # ------------------------------------------------------------------
        # 11. Preview validation before OK.
        # ------------------------------------------------------------------
        self.step(
            11,
            "Preview -> verifica unión, orientación y espesor",
            "Antes de aceptar, confirma tres cosas: el nervio toca ambos sólidos, no atraviesa geometría no deseada y mantiene Thickness = 6 mm simétrico.",
            2.85,
        )
        self.begin_ambient_camera_rotation(rate=0.07)
        self.wait(1.75)
        self.stop_ambient_camera_rotation()

        # ------------------------------------------------------------------
        # 12. Commit the parametric feature.
        # ------------------------------------------------------------------
        result = extruded_polygon(full_pts, 0.38, STEEL, 1.0).rotate(
            90 * DEGREES, axis=RIGHT
        ).shift(DOWN * 0.38)
        self.play(
            FadeOut(preview_full),
            FadeOut(rib_line),
            FadeIn(result),
            run_time=0.82,
        )
        self.step(
            12,
            "OK -> Rib1 aparece en el Model Browser",
            "Rib1 queda vinculado a Sketch2 y a las caras anfitrionas. Editar la línea cambia la posición; editar Thickness cambia el espesor del refuerzo.",
            2.90,
        )

        # ------------------------------------------------------------------
        # 13. Final engineering interpretation + orbit.
        # ------------------------------------------------------------------
        finish_feature(
            self,
            13,
            "Resultado: una línea abierta 2D se convirtió en un refuerzo 3D delgado, unido al sólido y completamente editable como operación paramétrica.",
        )
