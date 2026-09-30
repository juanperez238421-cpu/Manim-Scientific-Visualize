from __future__ import annotations

import math
import os
import numpy as np
from manim import *

from library.inventor_pro_ui import *
from library.sketch_to_3d_helpers import _fixed_badge

# -----------------------------------------------------------------------------
# LESSON DATA — illustrative thread geometry in millimetres
# -----------------------------------------------------------------------------
PITCH_MM = 2.50
D_MAJOR_MM = 20.000
D_MINOR_MM = 17.294
FLANK_ANGLE_DEG = 60.0

RADIAL_DEPTH_MM = (D_MAJOR_MM - D_MINOR_MM) / 2.0
HALF_ANGLE_DEG = FLANK_ANGLE_DEG / 2.0
PROFILE_WIDTH_MM = 2.0 * RADIAL_DEPTH_MM * math.tan(math.radians(HALF_ANGLE_DEG))
REMAINDER_MM = PITCH_MM - PROFILE_WIDTH_MM

assert RADIAL_DEPTH_MM > 0
assert PROFILE_WIDTH_MM > 0
assert PROFILE_WIDTH_MM < PITCH_MM
assert abs(RADIAL_DEPTH_MM - 1.353) < 1e-9

# World-space mapping used only for visualization.
R_MAJOR = 1.52
R_MINOR = R_MAJOR * (D_MINOR_MM / D_MAJOR_MM)
DEPTH_WORLD = R_MAJOR - R_MINOR
PITCH_WORLD = 1.08
PROFILE_WIDTH_WORLD = PITCH_WORLD * (PROFILE_WIDTH_MM / PITCH_MM)
Z0 = -2.15
TURNS = 4.25
K = PITCH_WORLD / TAU
CUT = "#C95D3A"
VALID = PREVIEW  # established Inventor preview/validation green

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))


def helix_center(t: float, radius: float = (R_MAJOR + R_MINOR) / 2) -> np.ndarray:
    return np.array([
        radius * math.cos(t),
        radius * math.sin(t),
        Z0 + K * t,
    ])


def helix_curve(color=PREVIEW, width: float = 8.0, opacity: float = 0.70) -> ParametricFunction:
    return ParametricFunction(
        lambda t: helix_center(t),
        t_range=[0, TURNS * TAU, 0.035],
        color=color,
        stroke_width=width,
    ).set_opacity(opacity)


def triangular_thread_surface(color=PREVIEW, opacity: float = 0.52) -> Surface:
    """Triangular helical envelope used to visualize the swept profile.

    v=-1..1 spans the axial base of the triangular profile.
    The crest reaches R_MAJOR at v=0; the base lies on R_MINOR.
    This is a pedagogical sharp-V envelope, not a manufacturing-grade ISO root/crest model.
    """

    def surface_point(u: float, v: float) -> np.ndarray:
        r = R_MINOR + DEPTH_WORLD * (1.0 - abs(v))
        z = Z0 + K * u + v * (PROFILE_WIDTH_WORLD / 2.0)
        return np.array([r * math.cos(u), r * math.sin(u), z])

    return Surface(
        surface_point,
        u_range=[0, TURNS * TAU],
        v_range=[-1.0, 1.0],
        resolution=(92, 8),
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=UI_MID,
        stroke_width=0.38,
    )


def sharp_profile_triangle(color=SKETCH, fill_opacity: float = 0.14) -> Polygon:
    """Sharp 60-degree triangular profile on the XZ sketch plane (y=0)."""
    apex = np.array([R_MAJOR, 0.0, Z0])
    root_a = np.array([R_MINOR, 0.0, Z0 - PROFILE_WIDTH_WORLD / 2.0])
    root_b = np.array([R_MINOR, 0.0, Z0 + PROFILE_WIDTH_WORLD / 2.0])
    return Polygon(
        root_a,
        apex,
        root_b,
        stroke_color=color,
        stroke_width=5.0,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


class InventorThreadProfileTriangleSenior(InventorOperationScene):
    """Senior 3D CAD lesson: derive a Coil thread profile from P, Dmajor and Dminor.

    Uses the established Autodesk Inventor professional HUD, true ThreeDScene camera
    moves, multiple engineering views, a constrained 2D profile derivation, helical
    path preview, triangular swept surface, and PQL -> PQH QA workflow.
    """

    OPERATION = "Coil"
    FEATURE_NODE = "Coil1"

    # Keep PQL smoke tests fast without changing final pedagogical timing.
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def equation_card(self, title: str, lines: list[str], accent=SELECT,
                      center=(-0.10, 0.75, 0), width=7.7, height=2.45) -> VGroup:
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=accent,
            stroke_width=1.25,
            fill_color="#F8F9FA",
            fill_opacity=0.985,
        )
        head = txt(title, 20, accent, BOLD)
        body = VGroup(*[txt(line, 18, TEXT, BOLD if i == len(lines)-1 else NORMAL)
                        for i, line in enumerate(lines)])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(body, width - 0.55, height - 0.70)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.30)
        card = VGroup(panel, content).move_to(center)
        self.add_fixed_in_frame_mobjects(card)
        return card

    def clear_fixed_card(self, card: Mobject, run_time=0.35):
        self.play(FadeOut(card), run_time=run_time)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)

    def view_badge(self, label: str, detail: str = "") -> VGroup:
        box = RoundedRectangle(
            width=3.90,
            height=0.62 if not detail else 0.82,
            corner_radius=0.08,
            stroke_color=UI_LINE,
            stroke_width=0.9,
            fill_color=UI_DARK_2,
            fill_opacity=0.96,
        ).move_to([2.25, 2.18, 0])
        t = txt(label, 17, TEXT_LIGHT, BOLD)
        if detail:
            d = txt(detail, 12, "#D9DDE0")
            fit(t, 3.45)
            fit(d, 3.45)
            t.move_to(box).shift(UP * 0.13)
            d.next_to(t, DOWN, buff=0.04)
            group = VGroup(box, t, d)
        else:
            t.move_to(box)
            group = VGroup(box, t)
        self.add_fixed_in_frame_mobjects(group)
        return group

    def clear_badge(self, badge: Mobject):
        self.play(FadeOut(badge), run_time=0.25)
        self.remove_fixed_in_frame_mobjects(badge)
        self.remove(badge)

    def profile_derivation_panel(self) -> VGroup:
        """Fixed-frame engineering sketch showing P, Dmajor, Dminor -> triangular profile."""
        panel = RoundedRectangle(
            width=8.35,
            height=4.92,
            corner_radius=0.10,
            stroke_color=UI_LINE,
            stroke_width=0.9,
            fill_color="#F8F9FA",
            fill_opacity=0.985,
        ).move_to([-0.18, 0.22, 0])

        title = txt("SKETCH1 · PERFIL DE ROSCA A PARTIR DE P, ØEXT Y ØINT", 20, TEXT, BOLD)
        title.move_to(panel.get_top() + DOWN * 0.30)
        fit(title, 7.75)

        # Local 2D coordinates inside the panel.
        x0, y_outer = -3.40, 1.15
        x1 = 3.00
        h_vis = 1.46
        y_minor = y_outer - h_vis
        pitch_vis = 2.06
        base_vis = pitch_vis * (PROFILE_WIDTH_MM / PITCH_MM)
        cx = -0.20

        outer = Line([x0, y_outer, 0], [x1, y_outer, 0], color=SKETCH, stroke_width=4.0)
        minor = Line([x0, y_minor, 0], [x1, y_minor, 0], color=CUT, stroke_width=3.2)
        outer_lab = txt(f"Øext = {D_MAJOR_MM:.3f} mm", 16, SKETCH, BOLD).next_to(outer, UP, buff=0.10).align_to(outer, RIGHT)
        minor_lab = txt(f"Øint = {D_MINOR_MM:.3f} mm", 16, CUT, BOLD).next_to(minor, DOWN, buff=0.10).align_to(minor, RIGHT)

        # Two profile stations separated by one pitch.
        c1, c2 = cx - pitch_vis / 2.0, cx + pitch_vis / 2.0
        guides = VGroup(
            DashedLine([c1, y_outer + 0.22, 0], [c1, y_minor - 0.35, 0], color=UI_MID, dash_length=0.08, stroke_width=1.4),
            DashedLine([c2, y_outer + 0.22, 0], [c2, y_minor - 0.35, 0], color=UI_MID, dash_length=0.08, stroke_width=1.4),
        )
        pitch_arrow = DoubleArrow([c1, y_minor - 0.52, 0], [c2, y_minor - 0.52, 0],
                                  buff=0.0, color=SELECT, stroke_width=2.4)
        pitch_label = txt(f"P = {PITCH_MM:.2f} mm", 17, SELECT, BOLD).next_to(pitch_arrow, DOWN, buff=0.05)

        # One sharp-V triangle reconstructed from radial depth and 60-degree flanks.
        tri_left = cx - base_vis / 2.0
        tri_right = cx + base_vis / 2.0
        tri = Polygon(
            [tri_left, y_outer, 0],
            [cx, y_minor, 0],
            [tri_right, y_outer, 0],
            stroke_color=SKETCH,
            stroke_width=4.2,
            fill_color=SKETCH,
            fill_opacity=0.08,
        )
        depth_arrow = DoubleArrow([tri_right + 0.52, y_outer, 0], [tri_right + 0.52, y_minor, 0],
                                  buff=0.0, color=VALID, stroke_width=2.3)
        depth_label = txt(f"h = {RADIAL_DEPTH_MM:.3f} mm", 16, VALID, BOLD).next_to(depth_arrow, RIGHT, buff=0.08)
        base_arrow = DoubleArrow([tri_left, y_outer + 0.34, 0], [tri_right, y_outer + 0.34, 0],
                                 buff=0.0, color=UI_MID, stroke_width=2.0)
        base_label = txt(f"b = {PROFILE_WIDTH_MM:.3f} mm", 15, UI_MID, BOLD).next_to(base_arrow, UP, buff=0.03)
        angle_arc = Arc(radius=0.46, start_angle=60 * DEGREES, angle=60 * DEGREES,
                        arc_center=[cx, y_minor, 0], color=SELECT, stroke_width=2.7)
        angle_label = txt("60°", 16, SELECT, BOLD).move_to([cx, y_minor + 0.58, 0])

        note = txt(
            "P separa repeticiones; h fija la profundidad radial; 60° fija la pendiente de los flancos.",
            15, UI_MID, NORMAL,
        )
        fit(note, 7.6)
        note.move_to(panel.get_bottom() + UP * 0.30)

        return VGroup(panel, title, outer, minor, outer_lab, minor_lab, guides,
                      pitch_arrow, pitch_label, tri, depth_arrow, depth_label,
                      base_arrow, base_label, angle_arc, angle_label, note)

    def construct(self):
        self.install_hud(
            [
                ("Pitch", f"{PITCH_MM:.2f} mm"),
                ("Major Ø", f"{D_MAJOR_MM:.3f} mm"),
                ("Minor Ø", f"{D_MINOR_MM:.3f} mm"),
                ("Flank angle", "60 deg"),
                ("Operation", "Cut / Join"),
            ],
            ["Part1.ipt", "Origin", "Sketch1", "Axis", "Coil1"],
        )

        self.intro(
            "Rosca: usa paso y diámetros para reconstruir el perfil triangular que Coil repetirá helicoidalmente."
        )

        # ------------------------------------------------------------------
        # 1) 3D envelope: establish the two diameters first.
        # ------------------------------------------------------------------
        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.88, run_time=0.88)
        view = self.view_badge("ISOMETRIC VIEW", "Major / minor diameter envelopes")
        outer = cylinder(R_MAJOR, 4.65, STEEL, 0.16)
        minor = cylinder(R_MINOR, 4.65, STEEL_DARK, 0.94)
        axis = DashedLine([0, 0, -2.60], [0, 0, 2.60], color=UI_MID,
                          dash_length=0.12, stroke_width=2.4)
        self.play(FadeIn(outer), FadeIn(minor), Create(axis), run_time=1.10)
        self.step(
            1,
            "Identifica Ø exterior, Ø interior y Pitch",
            "Øext define la cresta/envolvente mayor; Øint define el fondo/envolvente menor; Pitch fija la separación axial entre vueltas consecutivas.",
            2.85,
        )
        self.clear_badge(view)

        # ------------------------------------------------------------------
        # 2) Radial depth from diameters.
        # ------------------------------------------------------------------
        card = self.equation_card(
            "PASO A · PROFUNDIDAD RADIAL DEL PERFIL",
            [
                f"h = (Øext - Øint) / 2",
                f"h = ({D_MAJOR_MM:.3f} - {D_MINOR_MM:.3f}) / 2",
                f"h = {RADIAL_DEPTH_MM:.3f} mm",
            ],
            VALID,
            center=[-0.10, 0.75, 0],
        )
        self.step(
            2,
            "Resta los diámetros y divide entre 2",
            "La diferencia de diámetros está medida de lado a lado. Coil necesita la profundidad radial del triángulo: por eso se divide entre dos.",
            3.15,
        )
        self.clear_fixed_card(card)

        # ------------------------------------------------------------------
        # 3) Professional section/sketch view.
        # ------------------------------------------------------------------
        self.play(FadeOut(outer), FadeOut(minor), FadeOut(axis), run_time=0.55)
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=0.78)
        badge = _fixed_badge(
            self,
            "SKETCH / SECTION VIEW  |  Profile plane normal",
            "Reconstruct the triangular section before invoking Coil",
        )
        sketch = self.profile_derivation_panel()
        self.add_fixed_in_frame_mobjects(sketch)
        self.play(FadeIn(sketch[0]), Write(sketch[1]), run_time=0.72)
        self.play(Create(sketch[2]), Create(sketch[3]), FadeIn(sketch[4]), FadeIn(sketch[5]), run_time=0.70)
        self.step(
            3,
            "Traza las dos envolventes de diámetro",
            "En la vista de sección, Øext y Øint se convierten en dos niveles radiales. La distancia entre ellos es exactamente h.",
            2.80,
        )
        self.play(FadeIn(sketch[6]), GrowArrow(sketch[7]), FadeIn(sketch[8]), run_time=0.72)
        self.step(
            4,
            "Usa Pitch para posicionar la repetición",
            "Pitch NO es automáticamente la base del triángulo. Es la distancia axial entre puntos equivalentes de dos filetes consecutivos.",
            3.00,
        )
        self.play(Create(sketch[9]), GrowArrow(sketch[10]), FadeIn(sketch[11]), run_time=0.75)
        self.play(GrowArrow(sketch[12]), FadeIn(sketch[13]), Create(sketch[14]), FadeIn(sketch[15]), run_time=0.80)
        self.step(
            5,
            "Aplica 60° entre flancos",
            "Con un perfil V simétrico, cada flanco queda a 30° respecto al eje del triángulo. La altura h ya está fijada por los diámetros.",
            3.10,
        )

        card = self.equation_card(
            "PASO B · ANCHO DEL TRIÁNGULO V SIMPLIFICADO",
            [
                "b/2 = h · tan(30°)",
                "b = 2h · tan(30°)",
                f"b = {PROFILE_WIDTH_MM:.3f} mm   <   P = {PITCH_MM:.2f} mm",
            ],
            SELECT,
            center=[-0.10, -0.15, 0],
            width=7.60,
            height=2.25,
        )
        self.step(
            6,
            "Calcula el ancho real del perfil, no lo supongas igual a P",
            f"Aquí b = {PROFILE_WIDTH_MM:.3f} mm. Quedan {REMAINDER_MM:.3f} mm dentro de cada paso para truncamientos/planos según el perfil normalizado elegido.",
            3.35,
        )
        self.clear_fixed_card(card)
        self.play(FadeIn(sketch[16]), run_time=0.40)
        self.wait(0.75)
        self.play(FadeOut(sketch), FadeOut(badge), run_time=0.55)
        self.remove_fixed_in_frame_mobjects(sketch, badge)
        self.remove(sketch, badge)

        # ------------------------------------------------------------------
        # 4) Place the triangular profile in 3D relative to the axis.
        # ------------------------------------------------------------------
        self.move_camera(phi=66 * DEGREES, theta=-50 * DEGREES, zoom=0.89, run_time=0.90)
        outer = cylinder(R_MAJOR, 4.65, STEEL, 0.11)
        minor = cylinder(R_MINOR, 4.65, STEEL_DARK, 0.86)
        axis = DashedLine([0, 0, -2.60], [0, 0, 2.60], color=UI_MID,
                          dash_length=0.12, stroke_width=2.3)
        profile = sharp_profile_triangle(SKETCH, 0.18)
        radial = Line3D([0, 0, Z0], [R_MINOR, 0, Z0], color=SELECT, thickness=0.016)
        self.play(FadeIn(outer), FadeIn(minor), Create(axis), FadeIn(profile), Create(radial), run_time=1.05)
        view = self.view_badge("3D PROFILE PLACEMENT", "Sketch1 + Axis + diameter envelopes")
        self.step(
            7,
            "Ubica el triángulo sobre el plano que contiene el Axis",
            "El vértice y la base deben coincidir con las envolventes Øint/Øext según uses Join o Cut. Mantén el perfil completamente acotado.",
            3.15,
        )
        self.clear_badge(view)
        self.flash_status(
            f"Sketch1 fully constrained   |   h={RADIAL_DEPTH_MM:.3f} mm   |   b={PROFILE_WIDTH_MM:.3f} mm   |   P={PITCH_MM:.2f} mm"
        )

        # ------------------------------------------------------------------
        # 5) Coil preview: helix then swept triangular envelope.
        # ------------------------------------------------------------------
        self.step(
            8,
            "3D Model -> Coil -> Profile: Sketch1 -> Axis: Centerline",
            "En Coil, Pitch controla el avance axial de la hélice. El triángulo solo define la sección transversal que viaja por esa trayectoria.",
            3.10,
        )
        path = helix_curve(PREVIEW, 8.0, 0.72)
        tracer = Dot3D(helix_center(0), radius=0.065, color=SELECT)
        self.play(
            Create(path),
            MoveAlongPath(tracer, path),
            profile.animate.set_opacity(0.32),
            run_time=2.65,
            rate_func=linear,
        )
        self.step(
            9,
            "Preview de trayectoria: una vuelta avanza exactamente P",
            "Después de 360°, el perfil reaparece separado axialmente 2.50 mm. Esa condición es independiente del ancho b del triángulo.",
            2.95,
        )

        swept = triangular_thread_surface(PREVIEW, 0.50)
        self.play(FadeIn(swept), path.animate.set_opacity(0.20), FadeOut(tracer), run_time=1.15)
        self.begin_ambient_camera_rotation(rate=0.075)
        self.wait(1.65)
        self.stop_ambient_camera_rotation()
        self.step(
            10,
            "Solid Preview: inspecciona profundidad, sentido y autointersección",
            "El perfil debe llegar de Øint a Øext sin invadir el siguiente paso. Si b >= P, el perfil o los parámetros son incompatibles con esta simplificación.",
            3.10,
        )

        # ------------------------------------------------------------------
        # 6) Advanced views: section / axial / isometric validation.
        # ------------------------------------------------------------------
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.90, run_time=0.82)
        badge = self.view_badge("SECTION VIEW A-A", "Validate profile depth and flank geometry")
        self.step(
            11,
            "Vista de sección A-A",
            "Comprueba que la sección helicoidal conserva h y el ángulo de 60°. Esta vista detecta perfiles invertidos o referencias de diámetro incorrectas.",
            2.75,
        )
        self.clear_badge(badge)

        self.move_camera(phi=8 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=0.82)
        badge = self.view_badge("AXIAL VIEW", "Concentricity and major/minor envelopes")
        self.step(
            12,
            "Vista axial",
            "Øext y Øint deben permanecer concéntricos con el Axis. Esta vista valida centrado, simetría y orientación del perfil respecto al eje.",
            2.75,
        )
        self.clear_badge(badge)

        self.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.90)
        badge = self.view_badge("FINAL ISOMETRIC", "Wireframe envelope + helical profile")
        final_thread = triangular_thread_surface(STEEL, 0.98)
        self.play(
            FadeOut(path), FadeOut(swept), FadeOut(profile), FadeOut(radial), FadeOut(outer),
            ReplacementTransform(minor, cylinder(R_MINOR, 4.65, STEEL_DARK, 1.0)),
            FadeIn(final_thread),
            axis.animate.set_opacity(0.18),
            run_time=1.15,
        )
        self.step(
            13,
            "Resultado geométrico listo para Coil1",
            "Método reproducible: h desde los diámetros -> flancos de 60° -> b por trigonometría -> P como separación helicoidal -> validar en sección, axial e isométrica.",
            3.30,
        )
        self.clear_badge(badge)

        # Final rigor note: source supports 60°; exact ISO crest/root truncations need the specific standard.
        rigor = self.equation_card(
            "NOTA DE RIGOR",
            [
                "El triángulo mostrado es un perfil V simplificado para explicar la construcción CAD.",
                "Una rosca normalizada real incorpora truncamientos/radios de cresta y raíz.",
                "Para fabricación, aplica las dimensiones exactas de la norma de rosca seleccionada.",
            ],
            CUT,
            center=[-0.10, 0.20, 0],
            width=7.85,
            height=2.55,
        )
        self.wait(2.20)
        self.clear_fixed_card(rigor, 0.40)

        self.flash_status(
            f"Coil1 profile ready   |   P={PITCH_MM:.2f} mm   |   Øext={D_MAJOR_MM:.3f} mm   |   Øint={D_MINOR_MM:.3f} mm   |   60 deg"
        )
        self.begin_ambient_camera_rotation(rate=0.085)
        self.wait(3.10)
        self.stop_ambient_camera_rotation()
        self.wait(0.85)
