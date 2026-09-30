"""Autodesk Inventor — operaciones misceláneas, versión 3D V2.

Render oficial:
    manim -pqh Inventor_Misc_Operations_3D_V2_PQH.py InventorMiscOperations3D

La presentación reproduce el enfoque didáctico usado en las clases de
extrusión, barrido y solevación: croquis/selección -> operación -> sólido 3D.
Los textos se rasterizan con Pillow para conservar portabilidad y tamaño.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont

from manim import *


# ---------------------------------------------------------------------------
# JP Classroom / protocolo PQH
# ---------------------------------------------------------------------------
config.background_color = "#F7F9FC"
config.frame_rate = 30

INK = "#102A43"
MUTED = "#486581"
BLUE = "#1473E6"
CYAN = "#00A6C7"
GREEN = "#1F9D67"
ORANGE = "#F28C28"
RED = "#D64545"
PALE_BLUE = "#AFCBF4"
PALE_CYAN = "#92DDE9"
PALE_GREEN = "#9DDDBF"
PALE_ORANGE = "#F7C98F"
GRID = "#D8E2EC"
WHITE = "#FFFFFF"


def _font_path(bold: bool = False) -> str | None:
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    )
    return next((item for item in candidates if Path(item).exists()), None)


def rtext(
    text: str,
    *,
    size: int = 42,
    color: str = INK,
    bold: bool = False,
    max_width: float | None = None,
    align: str = "center",
) -> ImageMobject:
    """Create crisp transparent text without Pango or LaTeX."""
    font_path = _font_path(bold)
    font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()
    probe = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw_probe = ImageDraw.Draw(probe)
    bbox = draw_probe.multiline_textbbox((0, 0), text, font=font, spacing=10, align=align)
    width = int(max(12, math.ceil(bbox[2] - bbox[0] + 22)))
    height = int(max(12, math.ceil(bbox[3] - bbox[1] + 22)))
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.multiline_text(
        (11 - bbox[0], 11 - bbox[1]),
        text,
        font=font,
        fill=ImageColor.getrgb(color) + (255,),
        spacing=10,
        align=align,
    )
    mob = ImageMobject(np.array(canvas))
    mob.scale_to_fit_height(0.0106 * size * max(1, len(text.splitlines())))
    if max_width and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def pill(text: str, color: str, width: float = 2.45) -> Group:
    box = RoundedRectangle(
        width=width,
        height=0.52,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=1.7,
        fill_color=WHITE,
        fill_opacity=0.96,
    )
    label = rtext(text, size=22, color=color, bold=True, max_width=width - 0.22)
    label.move_to(box)
    return Group(box, label)


def overlay(page: int, kicker: str, title: str, subtitle: str) -> Group:
    kicker_m = rtext(kicker.upper(), size=22, color=BLUE, bold=True, max_width=11.8)
    title_m = rtext(title, size=47, color=INK, bold=True, max_width=12.2)
    subtitle_m = rtext(subtitle, size=26, color=MUTED, max_width=12.0)
    header = Group(kicker_m, title_m, subtitle_m).arrange(DOWN, buff=0.10)
    header.to_edge(UP, buff=0.20)
    footer_line = Line(LEFT * 6.55, RIGHT * 6.55, color=GRID, stroke_width=1.1).shift(DOWN * 3.46)
    footer_left = rtext("Dibujo técnico · Autodesk Inventor", size=18, color=MUTED).to_edge(DL, buff=0.26)
    footer_right = rtext(f"3D V2 · {page:02d}", size=18, color=MUTED, bold=True).to_edge(DR, buff=0.26)
    return Group(header, footer_line, footer_left, footer_right)


def cuboid(
    width: float,
    depth: float,
    height: float,
    *,
    color: str = PALE_BLUE,
    opacity: float = 0.88,
    stroke: str = INK,
) -> Cube:
    solid = Cube(side_length=1.0, fill_opacity=opacity, fill_color=color, stroke_color=stroke, stroke_width=1.3)
    solid.stretch_to_fit_width(width)
    # Inventor convention used here: width=X, depth=Y, height=Z.
    solid.stretch_to_fit_height(depth)
    solid.stretch_to_fit_depth(height)
    return solid


def cylinder(
    radius: float,
    height: float,
    *,
    color: str = PALE_CYAN,
    opacity: float = 0.90,
    stroke: str = INK,
    resolution: tuple[int, int] = (6, 12),
) -> Cylinder:
    return Cylinder(
        radius=radius,
        height=height,
        direction=OUT,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=1.1,
        resolution=resolution,
    )


def rounded_plate(width: float, depth: float, height: float, radius: float, color: str = PALE_GREEN) -> VGroup:
    """Rounded rectangular solid made from two prisms and four cylinders."""
    body_a = cuboid(width - 2 * radius, depth, height, color=color)
    body_b = cuboid(width, depth - 2 * radius, height, color=color)
    corners = VGroup()
    for sx in (-1, 1):
        for sy in (-1, 1):
            cap = cylinder(radius, height, color=color)
            cap.shift([sx * (width / 2 - radius), sy * (depth / 2 - radius), 0])
            corners.add(cap)
    return VGroup(body_a, body_b, corners)


def extruded_polygon(points: list[tuple[float, float]], height: float, color: str) -> VGroup:
    """Closed polygon extruded along Z, useful for chamfers and ribs."""
    z0, z1 = -height / 2, height / 2
    lower = [np.array([x, y, z0]) for x, y in points]
    upper = [np.array([x, y, z1]) for x, y in points]
    faces = VGroup(
        Polygon(*lower, fill_color=color, fill_opacity=0.90, stroke_color=INK, stroke_width=1.3),
        Polygon(*upper, fill_color=color, fill_opacity=0.90, stroke_color=INK, stroke_width=1.3),
    )
    count = len(points)
    for i in range(count):
        j = (i + 1) % count
        faces.add(
            Polygon(
                lower[i], lower[j], upper[j], upper[i],
                fill_color=color,
                fill_opacity=0.88,
                stroke_color=INK,
                stroke_width=1.2,
            )
        )
    return faces


def reference_plane() -> NumberPlane:
    plane = NumberPlane(
        x_range=[-5, 5, 1],
        y_range=[-4, 4, 1],
        background_line_style={"stroke_color": GRID, "stroke_width": 1, "stroke_opacity": 0.48},
        axis_config={"stroke_color": GRID, "stroke_width": 1.2},
    )
    plane.scale(0.78).shift(DOWN * 0.28)
    return plane


def axis_triad() -> VGroup:
    return VGroup(
        Arrow3D(ORIGIN, RIGHT * 1.1, color=RED, thickness=0.012, height=0.16, base_radius=0.07),
        Arrow3D(ORIGIN, UP * 1.1, color=GREEN, thickness=0.012, height=0.16, base_radius=0.07),
        Arrow3D(ORIGIN, OUT * 1.1, color=BLUE, thickness=0.012, height=0.16, base_radius=0.07),
    ).scale(0.55).shift(LEFT * 4.15 + DOWN * 2.28)


class InventorMiscOperations3D(ThreeDScene):
    """3D lesson: every operation is explained as a modelling transformation."""

    def start_page(self, page: int, kicker: str, title: str, subtitle: str, *, zoom: float = 0.78) -> Group:
        self.set_camera_orientation(phi=65 * DEGREES, theta=-48 * DEGREES, zoom=zoom)
        hud = overlay(page, kicker, title, subtitle)
        self.add_fixed_in_frame_mobjects(hud)
        self.add(reference_plane(), axis_triad())
        return hud

    def fixed(self, *mobjects: Mobject) -> None:
        self.add_fixed_in_frame_mobjects(*mobjects)

    def clear_page(self, run_time: float = 0.7) -> None:
        self.stop_ambient_camera_rotation()
        self.clear()

    def construct(self):
        # 01 — Portada 3D
        self.start_page(
            1,
            "Autodesk Inventor",
            "Operaciones misceláneas en 3D",
            "Del croquis y la selección al resultado volumétrico",
            zoom=0.82,
        )
        base = rounded_plate(4.8, 2.8, 0.52, 0.35, PALE_BLUE).shift(DOWN * 0.40)
        boss = cylinder(0.68, 1.08, color=PALE_CYAN).shift(OUT * 0.80 + DOWN * 0.40)
        hole = cylinder(0.25, 1.16, color=WHITE, stroke=ORANGE).shift(OUT * 0.84 + DOWN * 0.40)
        self.play(LaggedStart(*[FadeIn(m, scale=0.88) for m in base], lag_ratio=0.13), run_time=1.5)
        self.play(GrowFromCenter(boss), FadeIn(hole, scale=0.6), run_time=1.0)
        tag = pill("CROQUIS → OPERACIÓN → SÓLIDO", GREEN, 4.25).shift(DOWN * 2.74)
        self.fixed(tag)
        self.play(FadeIn(tag, shift=UP * 0.10))
        self.wait(2.8)
        self.clear_page()

        # 02 — Método común 3D
        self.start_page(
            2,
            "Método común",
            "Leer la geometría antes de elegir el comando",
            "La misma lógica usada en extrusión, barrido y solevación",
        )
        sketch = RoundedRectangle(width=3.9, height=2.2, corner_radius=0.25, color=ORANGE, stroke_width=5)
        sketch.rotate(90 * DEGREES, axis=RIGHT).shift(LEFT * 2.60 + DOWN * 0.35)
        direction = Arrow3D(LEFT * 1.30 + DOWN * 0.35, RIGHT * 0.05 + DOWN * 0.35, color=GREEN, thickness=0.018, height=0.24, base_radius=0.10)
        result = rounded_plate(3.9, 2.2, 0.72, 0.25, PALE_GREEN).shift(RIGHT * 2.15 + DOWN * 0.35)
        labels = Group(
            pill("1 · CROQUIS / SELECCIÓN", ORANGE, 3.05),
            pill("2 · PARÁMETRO", GREEN, 2.35),
            pill("3 · RESULTADO 3D", BLUE, 2.65),
        ).arrange(RIGHT, buff=0.34).shift(DOWN * 2.76)
        self.fixed(labels)
        self.play(Create(sketch), FadeIn(labels[0]), run_time=1.0)
        self.play(GrowFromCenter(direction), FadeIn(labels[1]), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in result], lag_ratio=0.08), FadeIn(labels[2]), run_time=1.4)
        self.set_camera_orientation(theta=-28 * DEGREES, phi=70 * DEGREES)
        self.wait(1.8)
        self.clear_page()

        # 03 — Redondeo
        self.start_page(
            3,
            "Acabado de aristas",
            "Redondeo: sustituir una arista por un radio",
            "Selecciona la arista · define R · verifica continuidad",
        )
        sharp = cuboid(4.6, 2.6, 0.72, color=PALE_BLUE).shift(LEFT * 2.55 + DOWN * 0.36)
        selected = Line3D(
            start=LEFT * 0.25 + UP * 0.94 + OUT * 0.36 + DOWN * 0.36,
            end=LEFT * 0.25 + DOWN * 1.66 + OUT * 0.36 + DOWN * 0.36,
            color=ORANGE,
            thickness=0.045,
        )
        rounded = rounded_plate(4.6, 2.6, 0.72, 0.42, PALE_GREEN).shift(RIGHT * 2.55 + DOWN * 0.36)
        radius_arc = Arc(radius=0.46, start_angle=0, angle=PI / 2, color=ORANGE, stroke_width=6).rotate(90 * DEGREES, RIGHT)
        radius_arc.shift(RIGHT * 4.22 + UP * 0.86 + OUT * 0.38 + DOWN * 0.36)
        bottom = Group(
            pill("ARISTA", ORANGE, 1.65),
            pill("RADIO R", GREEN, 1.85),
            pill("TRANSICIÓN SUAVE", BLUE, 2.65),
        ).arrange(RIGHT, buff=0.42).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(DrawBorderThenFill(sharp), Create(selected), FadeIn(bottom[0]), run_time=1.1)
        self.play(FadeIn(bottom[1]), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in rounded], lag_ratio=0.06), Create(radius_arc), FadeIn(bottom[2]), run_time=1.5)
        self.set_camera_orientation(theta=-25 * DEGREES)
        self.wait(2.0)
        self.clear_page()

        # 04 — Chaflán
        self.start_page(
            4,
            "Acabado de aristas",
            "Chaflán: reemplazar la esquina por una cara plana",
            "Distancia–distancia o distancia–ángulo",
        )
        raw = cuboid(4.6, 2.7, 0.78, color=PALE_BLUE).shift(LEFT * 2.55 + DOWN * 0.35)
        edge = Line3D(
            start=LEFT * 0.25 + UP * 1.00 + OUT * 0.39 + DOWN * 0.35,
            end=LEFT * 0.25 + UP * 1.00 + IN * 0.39 + DOWN * 0.35,
            color=ORANGE,
            thickness=0.05,
        )
        pts = [(-2.3, -1.35), (2.3, -1.35), (2.3, 0.72), (1.67, 1.35), (-2.3, 1.35)]
        chamfer = extruded_polygon(pts, 0.78, PALE_ORANGE).shift(RIGHT * 2.55 + DOWN * 0.35)
        face = Polygon(
            [4.22, 0.37, -0.39], [4.85, 1.00, -0.39], [4.85, 1.00, 0.39], [4.22, 0.37, 0.39],
            fill_color=ORANGE, fill_opacity=0.80, stroke_color=ORANGE, stroke_width=2,
        ).shift(DOWN * 0.35)
        bottom = Group(
            pill("ARISTA", ORANGE, 1.65),
            pill("4 mm × 45°", GREEN, 2.05),
            pill("CARA INCLINADA", BLUE, 2.55),
        ).arrange(RIGHT, buff=0.42).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(DrawBorderThenFill(raw), Create(edge), FadeIn(bottom[0]), run_time=1.0)
        self.play(FadeIn(bottom[1]), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in chamfer], lag_ratio=0.05), FadeIn(face), FadeIn(bottom[2]), run_time=1.5)
        self.set_camera_orientation(theta=-70 * DEGREES, phi=60 * DEGREES)
        self.wait(2.0)
        self.clear_page()

        # 05 — Simetría
        self.start_page(
            5,
            "Reutilización paramétrica",
            "Simetría: modelar media pieza y reflejar",
            "Selecciona operaciones y un plano medio estable",
        )
        plane = Rectangle(width=0.06, height=4.6, color=ORANGE, fill_color=ORANGE, fill_opacity=0.22, stroke_width=2)
        plane.rotate(90 * DEGREES, axis=UP).shift(DOWN * 0.36)
        half = VGroup(
            cuboid(2.2, 2.7, 0.52, color=PALE_BLUE).shift(RIGHT * 1.15 + DOWN * 0.42),
            cuboid(0.44, 2.7, 2.1, color=PALE_CYAN).shift(RIGHT * 0.22 + DOWN * 0.42 + OUT * 0.80),
            cylinder(0.38, 0.62, color=PALE_GREEN).shift(RIGHT * 1.30 + DOWN * 0.42 + OUT * 0.54),
        )
        mirrored = half.copy().flip(RIGHT).set_opacity(0.18)
        bottom = Group(
            pill("MEDIA PIEZA", BLUE, 2.15),
            pill("PLANO MEDIO", ORANGE, 2.20),
            pill("REFLEJAR", GREEN, 1.90),
        ).arrange(RIGHT, buff=0.46).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in half], lag_ratio=0.13), FadeIn(bottom[0]), run_time=1.2)
        self.play(FadeIn(plane), FadeIn(bottom[1]), run_time=0.7)
        self.add(mirrored)
        self.play(mirrored.animate.set_opacity(0.90), FadeIn(bottom[2]), run_time=1.2)
        self.set_camera_orientation(theta=-20 * DEGREES)
        self.wait(2.2)
        self.clear_page()

        # 06 — Nervio
        self.start_page(
            6,
            "Refuerzo estructural",
            "Nervio: convertir una línea en material resistente",
            "Croquis abierto · espesor · dirección",
        )
        base = cuboid(4.8, 2.6, 0.45, color=PALE_BLUE).shift(DOWN * 0.45)
        wall = cuboid(0.48, 2.6, 2.65, color=PALE_CYAN).shift(LEFT * 2.14 + DOWN * 0.45 + OUT * 1.10)
        sketch_line = Line3D(
            start=LEFT * 1.85 + DOWN * 0.45 + OUT * 0.28,
            end=RIGHT * 0.75 + DOWN * 0.45 + OUT * 2.00,
            color=ORANGE,
            thickness=0.045,
        )
        rib_pts = [(-1.90, -0.15), (-1.90, 1.75), (0.85, -0.15)]
        rib = extruded_polygon(rib_pts, 0.34, PALE_GREEN).rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.45)
        bottom = Group(
            pill("LÍNEA ABIERTA", ORANGE, 2.25),
            pill("ESPESOR 6 mm", GREEN, 2.30),
            pill("RIGIDEZ", BLUE, 1.85),
        ).arrange(RIGHT, buff=0.43).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(GrowFromCenter(base), GrowFromCenter(wall), run_time=1.0)
        self.play(Create(sketch_line), FadeIn(bottom[0]), run_time=0.8)
        self.play(FadeIn(bottom[1]), run_time=0.45)
        self.play(LaggedStart(*[GrowFromEdge(face, DOWN) for face in rib], lag_ratio=0.06), FadeIn(bottom[2]), run_time=1.5)
        self.set_camera_orientation(theta=-25 * DEGREES, phi=72 * DEGREES)
        self.wait(2.1)
        self.clear_page()

        # 07 — Repujado
        self.start_page(
            7,
            "Relieve funcional",
            "Repujado: elevar o hundir un perfil sobre una cara",
            "Perfil cerrado · dirección · profundidad",
        )
        plate = rounded_plate(5.0, 3.0, 0.36, 0.30, PALE_BLUE).shift(DOWN * 0.38)
        profile = Circle(radius=0.78, color=ORANGE, stroke_width=6).shift(DOWN * 0.38 + OUT * 0.20)
        embossed = cylinder(0.78, 0.58, color=PALE_CYAN).shift(DOWN * 0.38 + OUT * 0.47)
        inner = cylinder(0.34, 0.64, color=WHITE, stroke=CYAN).shift(DOWN * 0.38 + OUT * 0.50)
        up_arrow = Arrow3D(
            RIGHT * 1.55 + DOWN * 0.38 + OUT * 0.20,
            RIGHT * 1.55 + DOWN * 0.38 + OUT * 1.25,
            color=GREEN,
            thickness=0.018,
            height=0.22,
            base_radius=0.09,
        )
        bottom = Group(
            pill("PERFIL CERRADO", ORANGE, 2.50),
            pill("ALTURA 3 mm", GREEN, 2.10),
            pill("RELIEVE", BLUE, 1.85),
        ).arrange(RIGHT, buff=0.42).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in plate], lag_ratio=0.08), run_time=1.1)
        self.play(Create(profile), FadeIn(bottom[0]), run_time=0.8)
        self.play(GrowFromCenter(up_arrow), FadeIn(bottom[1]), run_time=0.7)
        self.play(ReplacementTransform(profile.copy(), embossed), GrowFromCenter(inner), FadeIn(bottom[2]), run_time=1.2)
        self.set_camera_orientation(theta=-18 * DEGREES)
        self.wait(2.2)
        self.clear_page()

        # 08 — Bobina
        self.start_page(
            8,
            "Geometría helicoidal",
            "Bobina: girar y avanzar alrededor de un eje",
            "Perfil · eje · paso · número de vueltas",
            zoom=0.72,
        )
        axis = DashedLine(IN * 2.35, OUT * 2.35, color=MUTED, dash_length=0.16, stroke_width=3)
        profile = Circle(radius=0.18, color=ORANGE, fill_color=ORANGE, fill_opacity=1).rotate(90 * DEGREES, axis=UP)
        profile.shift(RIGHT * 1.30 + IN * 2.20)
        helix = ParametricFunction(
            lambda t: np.array([1.30 * math.cos(t), 1.30 * math.sin(t), 0.17 * t - 2.15]),
            t_range=[0, 8 * PI, 0.04],
            color=BLUE,
            stroke_width=8,
        )
        pitch_start = RIGHT * 1.75 + IN * 1.60
        pitch_end = RIGHT * 1.75 + IN * 0.54
        pitch = VGroup(
            Arrow3D(pitch_start, pitch_end, color=GREEN, thickness=0.012, height=0.16, base_radius=0.065),
            Arrow3D(pitch_end, pitch_start, color=GREEN, thickness=0.012, height=0.16, base_radius=0.065),
        )
        bottom = Group(
            pill("PERFIL", ORANGE, 1.65),
            pill("EJE", MUTED, 1.45),
            pill("PASO", GREEN, 1.55),
            pill("4 VUELTAS", BLUE, 1.95),
        ).arrange(RIGHT, buff=0.38).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(FadeIn(profile), FadeIn(bottom[0]), run_time=0.6)
        self.play(Create(axis), FadeIn(bottom[1]), run_time=0.7)
        self.play(Create(helix), run_time=2.6)
        self.play(GrowFromCenter(pitch), FadeIn(bottom[2]), FadeIn(bottom[3]), run_time=0.9)
        self.wait(2.8)
        self.clear_page()

        # 09 — Patrón lineal
        self.start_page(
            9,
            "Repetición paramétrica",
            "Patrón lineal: repetir en una dirección",
            "Operación inicial · dirección · separación · cantidad",
        )
        plate = rounded_plate(6.0, 2.6, 0.40, 0.28, PALE_BLUE).shift(DOWN * 0.45)
        seed = cylinder(0.34, 0.72, color=PALE_CYAN).shift(LEFT * 2.10 + DOWN * 0.45 + OUT * 0.55)
        direction = Arrow3D(
            LEFT * 2.10 + DOWN * 1.72 + OUT * 0.25,
            RIGHT * 2.35 + DOWN * 1.72 + OUT * 0.25,
            color=ORANGE,
            thickness=0.018,
            height=0.23,
            base_radius=0.09,
        )
        copies = VGroup(*[
            seed.copy().shift(RIGHT * 1.40 * i).set_opacity(0.18) for i in range(1, 4)
        ])
        bottom = Group(
            pill("SEMILLA", BLUE, 1.70),
            pill("DIRECCIÓN", ORANGE, 1.95),
            pill("140 mm", GREEN, 1.75),
            pill("4 UNIDADES", CYAN, 2.05),
        ).arrange(RIGHT, buff=0.34).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in plate], lag_ratio=0.06), run_time=1.0)
        self.play(GrowFromCenter(seed), FadeIn(bottom[0]), run_time=0.7)
        self.play(GrowFromCenter(direction), FadeIn(bottom[1]), FadeIn(bottom[2]), run_time=0.8)
        self.add(copies)
        self.play(LaggedStart(*[c.animate.set_opacity(0.92) for c in copies], lag_ratio=0.22), FadeIn(bottom[3]), run_time=1.4)
        self.set_camera_orientation(theta=-20 * DEGREES)
        self.wait(2.1)
        self.clear_page()

        # 10 — Patrón circular
        self.start_page(
            10,
            "Repetición paramétrica",
            "Patrón circular: repetir alrededor de un eje",
            "Operación inicial · eje · ángulo total · cantidad",
        )
        disk = cylinder(2.35, 0.42, color=PALE_BLUE).shift(DOWN * 0.40)
        hub = cylinder(0.48, 0.66, color=WHITE, stroke=INK).shift(DOWN * 0.40 + OUT * 0.46)
        seed = cylinder(0.25, 0.68, color=PALE_CYAN).shift(RIGHT * 1.55 + DOWN * 0.40 + OUT * 0.48)
        axis = Arrow3D(
            DOWN * 0.40 + IN * 0.45,
            DOWN * 0.40 + OUT * 1.55,
            color=ORANGE,
            thickness=0.018,
            height=0.23,
            base_radius=0.09,
        )
        copies = VGroup()
        for k in range(1, 8):
            angle = k * TAU / 8
            item = seed.copy().move_to([1.55 * math.cos(angle), 1.55 * math.sin(angle) - 0.40, 0.48]).set_opacity(0.16)
            copies.add(item)
        bottom = Group(
            pill("SEMILLA", BLUE, 1.70),
            pill("EJE", ORANGE, 1.45),
            pill("360°", GREEN, 1.55),
            pill("8 UNIDADES", CYAN, 2.05),
        ).arrange(RIGHT, buff=0.40).shift(DOWN * 2.76)
        self.fixed(bottom)
        self.play(GrowFromCenter(disk), GrowFromCenter(hub), run_time=1.0)
        self.play(GrowFromCenter(seed), FadeIn(bottom[0]), run_time=0.7)
        self.play(GrowFromCenter(axis), FadeIn(bottom[1]), FadeIn(bottom[2]), run_time=0.7)
        self.add(copies)
        self.play(LaggedStart(*[c.animate.set_opacity(0.92) for c in copies], lag_ratio=0.10), FadeIn(bottom[3]), run_time=1.5)
        self.wait(2.6)
        self.clear_page()

        # 11 — Workshop integrador
        self.start_page(
            11,
            "Workshop",
            "Construye un soporte paramétrico completo",
            "Integra acabado, refuerzo, relieve, simetría y patrones",
            zoom=0.70,
        )
        base = rounded_plate(6.4, 3.5, 0.48, 0.38, PALE_BLUE).shift(DOWN * 0.55)
        walls = VGroup(
            cuboid(0.46, 3.1, 2.70, color=PALE_CYAN).shift(LEFT * 2.56 + DOWN * 0.55 + OUT * 1.35),
            cuboid(0.46, 3.1, 2.70, color=PALE_CYAN).shift(RIGHT * 2.56 + DOWN * 0.55 + OUT * 1.35),
        )
        rib_a = extruded_polygon([(-2.32, -0.10), (-2.32, 1.95), (-0.62, -0.10)], 0.32, PALE_GREEN)
        rib_a.rotate(90 * DEGREES, axis=RIGHT).shift(DOWN * 0.55)
        rib_b = rib_a.copy().flip(RIGHT)
        emboss = cylinder(0.70, 0.58, color=PALE_ORANGE).shift(DOWN * 0.55 + OUT * 0.53)
        emboss_hole = cylinder(0.30, 0.66, color=WHITE, stroke=ORANGE).shift(DOWN * 0.55 + OUT * 0.56)
        bosses = VGroup()
        for x in (-2.10, -0.70, 0.70, 2.10):
            bosses.add(cylinder(0.24, 0.64, color=PALE_CYAN).shift([x, -1.05, 0.52]))
        stages = Group(
            pill("1 · BASE", BLUE, 1.70),
            pill("2 · SIMETRÍA", ORANGE, 2.15),
            pill("3 · NERVIOS", GREEN, 2.05),
            pill("4 · DETALLES", CYAN, 2.05),
        ).arrange(RIGHT, buff=0.35).shift(DOWN * 2.76)
        self.fixed(stages)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in base], lag_ratio=0.06), FadeIn(stages[0]), run_time=1.2)
        self.play(LaggedStart(*[GrowFromEdge(w, DOWN) for w in walls], lag_ratio=0.20), FadeIn(stages[1]), run_time=1.2)
        self.play(
            LaggedStart(*[GrowFromCenter(face) for face in rib_a], lag_ratio=0.04),
            LaggedStart(*[GrowFromCenter(face) for face in rib_b], lag_ratio=0.04),
            FadeIn(stages[2]),
            run_time=1.6,
        )
        self.play(
            GrowFromCenter(emboss), GrowFromCenter(emboss_hole),
            LaggedStart(*[GrowFromCenter(b) for b in bosses], lag_ratio=0.12),
            FadeIn(stages[3]), run_time=1.5,
        )
        criterion = pill("CRITERIO: MODELO EDITABLE Y ORDENADO", RED, 4.55).shift(DOWN * 2.12)
        self.fixed(criterion)
        self.play(FadeIn(criterion, shift=UP * 0.10))
        self.wait(3.2)
        self.clear_page()

        # 12 — Cierre
        self.start_page(
            12,
            "Cierre",
            "Primero intención; después comando",
            "Selecciona bien · parametriza · verifica en 3D",
            zoom=0.82,
        )
        final_part = rounded_plate(4.8, 2.9, 0.50, 0.34, PALE_GREEN).shift(DOWN * 0.40)
        center = cylinder(0.70, 0.95, color=PALE_CYAN).shift(DOWN * 0.40 + OUT * 0.70)
        orbit = ParametricFunction(
            lambda t: np.array([2.55 * math.cos(t), 1.55 * math.sin(t) - 0.40, 1.15]),
            t_range=[0, TAU, 0.03],
            color=ORANGE,
            stroke_width=5,
        )
        final_tag = pill("LISTOS PARA MODELAR EN INVENTOR", GREEN, 4.15).shift(DOWN * 2.74)
        self.fixed(final_tag)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in final_part], lag_ratio=0.08), GrowFromCenter(center), run_time=1.4)
        self.play(Create(orbit), FadeIn(final_tag, shift=UP * 0.10), run_time=1.4)
        self.wait(3.5)


if __name__ == "__main__":
    print("manim -pqh Inventor_Misc_Operations_3D_V2_PQH.py InventorMiscOperations3D")
