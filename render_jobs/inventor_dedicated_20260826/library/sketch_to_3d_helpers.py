from __future__ import annotations

from manim import *

from library.inventor_pro_ui import (
    CANVAS,
    PREVIEW,
    SELECT,
    SKETCH,
    STEEL,
    TEXT,
    TEXT_LIGHT,
    UI_DARK_2,
    UI_LINE,
    UI_MID,
    cuboid,
    fit,
    txt,
)


def _fixed_badge(scene, title: str, detail: str) -> VGroup:
    """Inventor-style fixed overlay used while the model is in 2D sketch mode."""
    box = RoundedRectangle(
        width=7.6,
        height=0.72,
        corner_radius=0.08,
        stroke_color=UI_LINE,
        stroke_width=0.9,
        fill_color=UI_DARK_2,
        fill_opacity=0.96,
    ).move_to([-0.15, 2.18, 0])
    t = txt(title, 17, TEXT_LIGHT, BOLD)
    d = txt(detail, 13, "#D9DDE0")
    fit(t, 7.0)
    fit(d, 7.0)
    t.move_to(box).shift(UP * 0.12)
    d.next_to(t, DOWN, buff=0.045)
    group = VGroup(box, t, d)
    scene.add_fixed_in_frame_mobjects(group)
    return group


def animate_rect_sketch_to_extrusion(
    scene,
    width: float,
    depth: float,
    height: float,
    shift=ORIGIN,
    dimensions: str = "70 mm x 45 mm",
    extrusion: str = "12 mm",
    step_start: int = 1,
    body_color: str = STEEL,
):
    """Show a clear Inventor workflow: XY plane -> constrained 2D sketch -> 3D extrusion.

    The returned Mobject is the finished steel base solid and can be reused by the
    dedicated feature lesson.  HUD objects remain fixed while the camera changes.
    """
    scene.move_camera(phi=4 * DEGREES, theta=-90 * DEGREES, zoom=0.90, run_time=0.75)

    badge = _fixed_badge(
        scene,
        "SKETCH MODE  |  XY Plane  |  Sketch1",
        f"Rectangle {dimensions}   |   Fully Constrained",
    )

    outline = Rectangle(
        width=width,
        height=depth,
        stroke_color=SKETCH,
        stroke_width=5,
        fill_color=CANVAS,
        fill_opacity=0.05,
    ).shift(shift)
    center_h = DashedLine(
        outline.get_left(), outline.get_right(), color=UI_MID, dash_length=0.10, stroke_width=1.6
    )
    center_v = DashedLine(
        outline.get_bottom(), outline.get_top(), color=UI_MID, dash_length=0.10, stroke_width=1.6
    )
    origin = Dot(outline.get_center(), radius=0.055, color=SELECT)

    scene.play(Create(outline), Create(center_h), Create(center_v), FadeIn(origin), run_time=1.05)
    scene.step(
        step_start,
        "Start 2D Sketch -> XY Plane",
        "Selecciona un plano base estable. Inventor entra a Sketch y orienta la camara normal al plano.",
        2.15,
    )
    scene.step(
        step_start + 1,
        f"Dibuja y acota el perfil: {dimensions}",
        "Aplica restricciones horizontal/vertical, fija el origen y deja el croquis completamente restringido antes de crear volumen.",
        2.45,
    )

    scene.play(FadeOut(badge), run_time=0.25)
    scene.remove_fixed_in_frame_mobjects(badge)
    scene.move_camera(phi=64 * DEGREES, theta=-46 * DEGREES, zoom=0.86, run_time=0.90)

    preview = cuboid(width, depth, 0.045, PREVIEW, 0.50).shift(shift)
    scene.play(FadeIn(preview), outline.animate.set_opacity(0.28), run_time=0.45)
    scene.play(preview.animate.stretch_to_fit_depth(height), run_time=1.15)
    scene.step(
        step_start + 2,
        f"Finish Sketch -> Extrude = {extrusion}",
        "El perfil 2D cerrado genera el solido base. Revisa direccion, distancia y operacion Join antes de confirmar Extrusion1.",
        2.55,
    )

    body = cuboid(width, depth, height, body_color, 1.0).shift(shift)
    scene.play(
        FadeOut(outline), FadeOut(center_h), FadeOut(center_v), FadeOut(origin),
        ReplacementTransform(preview, body),
        run_time=0.75,
    )
    scene.flash_status("Extrusion1 created     |     Sketch1 consumed     |     Ready for next 3D feature")
    scene.wait(0.65)
    return body


def finish_feature(scene, number: int, final_message: str):
    """Finish a dedicated lesson with a numbered confirmation and 3D orbit."""
    scene.step(number, "OK -> Feature created", final_message, 2.85)
    scene.flash_status(
        f"Feature created: {scene.FEATURE_NODE}     |     Model updated     |     mm"
    )
    scene.begin_ambient_camera_rotation(rate=0.10)
    scene.wait(3.2)
    scene.stop_ambient_camera_rotation()
    scene.wait(1.0)
