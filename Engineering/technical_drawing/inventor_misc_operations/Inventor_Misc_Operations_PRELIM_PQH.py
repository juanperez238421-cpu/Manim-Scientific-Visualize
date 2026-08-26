"""Autodesk Inventor: operaciones misceláneas — presentación preliminar.

Render objetivo (ManimCE 0.20.1):
    manim -pqh Inventor_Misc_Operations_PRELIM_PQH.py InventorMiscOperations

La escena evita capturas de interfaz para concentrarse en la intención de
diseño: qué selecciona el estudiante, qué parámetro controla y qué resultado
geométrico obtiene.  Los textos se rasterizan con Pillow para que el archivo
sea portable incluso en entornos sin Pango/dvisvgm.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont

from manim import *


# ---------------------------------------------------------------------------
# Configuración visual JP Classroom / PQH
# ---------------------------------------------------------------------------
config.background_color = "#F7F9FC"
config.frame_rate = 60
config.pixel_width = 1920
config.pixel_height = 1080

INK = "#102A43"
MUTED = "#486581"
BLUE = "#1473E6"
CYAN = "#00A6C7"
GREEN = "#1F9D67"
ORANGE = "#F28C28"
RED = "#D64545"
PALE_BLUE = "#E7F1FF"
PALE_CYAN = "#E4F8FB"
PALE_GREEN = "#E6F6EF"
PALE_ORANGE = "#FFF1E2"
GRID = "#DDE6EF"
WHITE = "#FFFFFF"

SAFE_W = 13.1
SAFE_H = 7.15


def _font_path(bold: bool = False) -> str | None:
    """Choose a widely available sans font, with safe fallbacks."""
    names = (
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
    return next((name for name in names if Path(name).exists()), None)


def rtext(
    text: str,
    *,
    size: int = 44,
    color: str = INK,
    bold: bool = False,
    max_width: float | None = None,
    line_spacing: int = 10,
) -> ImageMobject:
    """Return crisp transparent text as an ImageMobject."""
    font_path = _font_path(bold)
    font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()
    lines = text.split("\n")
    probe = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    probe_draw = ImageDraw.Draw(probe)
    bbox = probe_draw.multiline_textbbox(
        (0, 0), text, font=font, spacing=line_spacing, align="center"
    )
    width = int(math.ceil(max(8, bbox[2] - bbox[0] + 18)))
    height = int(math.ceil(max(8, bbox[3] - bbox[1] + 18)))
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.multiline_text(
        (9 - bbox[0], 9 - bbox[1]),
        text,
        font=font,
        fill=ImageColor.getrgb(color) + (255,),
        spacing=line_spacing,
        align="center",
    )
    mob = ImageMobject(np.array(image))
    target_height = 0.0108 * size * max(1, len(lines))
    mob.scale_to_fit_height(target_height)
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def title_block(kicker: str, title: str, subtitle: str | None = None) -> Group:
    kicker_m = rtext(kicker.upper(), size=24, color=BLUE, bold=True, max_width=11.5)
    title_m = rtext(title, size=54, color=INK, bold=True, max_width=12.2)
    parts = [kicker_m, title_m]
    if subtitle:
        parts.append(rtext(subtitle, size=30, color=MUTED, max_width=11.9))
    group = Group(*parts).arrange(DOWN, buff=0.16)
    group.to_edge(UP, buff=0.42)
    return group


def grid_background() -> VGroup:
    lines = VGroup()
    for x in np.arange(-7.2, 7.3, 0.5):
        lines.add(Line([x, -4, 0], [x, 4, 0], color=GRID, stroke_width=0.55))
    for y in np.arange(-4.0, 4.1, 0.5):
        lines.add(Line([-7.2, y, 0], [7.2, y, 0], color=GRID, stroke_width=0.55))
    lines.set_opacity(0.36)
    return lines


def footer(page: int, label: str = "Dibujo técnico · Autodesk Inventor") -> Group:
    line = Line(LEFT * 6.55, RIGHT * 6.55, color=GRID, stroke_width=1.2).shift(DOWN * 3.48)
    left = rtext(label, size=19, color=MUTED).to_edge(DL, buff=0.31)
    right = rtext(f"PRELIMINAR · {page:02d}", size=19, color=MUTED, bold=True).to_edge(DR, buff=0.31)
    return Group(line, left, right)


def pill(text: str, color: str = BLUE, width: float = 2.2) -> Group:
    box = RoundedRectangle(
        width=width,
        height=0.54,
        corner_radius=0.18,
        stroke_width=1.7,
        stroke_color=color,
        fill_color=WHITE,
        fill_opacity=1,
    )
    label = rtext(text, size=23, color=color, bold=True, max_width=width - 0.24)
    label.move_to(box)
    return Group(box, label)


def info_card(
    number: str,
    title: str,
    body: str,
    *,
    color: str = BLUE,
    width: float = 3.65,
    height: float = 2.2,
) -> Group:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_width=1.4,
        stroke_color=color,
        fill_color=WHITE,
        fill_opacity=0.98,
    )
    badge = Circle(radius=0.27, color=color, fill_color=color, fill_opacity=1)
    badge.move_to(box.get_corner(UL) + RIGHT * 0.42 + DOWN * 0.42)
    num = rtext(number, size=22, color=WHITE, bold=True).move_to(badge)
    heading = rtext(title, size=30, color=INK, bold=True, max_width=width - 1.0)
    heading.next_to(badge, RIGHT, buff=0.17).align_to(box, UP).shift(DOWN * 0.23)
    desc = rtext(body, size=23, color=MUTED, max_width=width - 0.48, line_spacing=8)
    desc.move_to(box).shift(DOWN * 0.35)
    return Group(box, badge, num, heading, desc)


def step_strip(items: list[str]) -> Group:
    groups = [pill(item, BLUE, width=2.24) for item in items]
    arrows = [Arrow(LEFT, RIGHT, buff=0, color=MUTED, stroke_width=2.4, max_tip_length_to_length_ratio=0.16).scale(0.27) for _ in range(len(items) - 1)]
    parts = []
    for index, item in enumerate(groups):
        parts.append(item)
        if index < len(arrows):
            parts.append(arrows[index])
    return Group(*parts).arrange(RIGHT, buff=0.15)


def base_plate(width: float = 4.4, height: float = 2.55) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=INK,
        stroke_width=3,
        fill_color=PALE_BLUE,
        fill_opacity=0.95,
    )


def selected_edge(a: np.ndarray, b: np.ndarray) -> Line:
    return Line(a, b, color=ORANGE, stroke_width=9)


def fillet_demo() -> Group:
    before = Polygon(
        [-1.7, -1.05, 0], [1.7, -1.05, 0], [1.7, 1.05, 0], [-1.7, 1.05, 0],
        color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1,
    )
    mark = selected_edge(np.array([1.7, 0.25, 0]), np.array([1.7, 1.05, 0]))
    result = RoundedRectangle(
        width=3.4, height=2.1, corner_radius=0.38,
        color=INK, stroke_width=3, fill_color=PALE_GREEN, fill_opacity=1,
    )
    arc = Arc(radius=0.38, start_angle=0, angle=PI / 2, color=GREEN, stroke_width=8)
    arc.move_arc_center_to(result.get_corner(UR) + LEFT * 0.38 + DOWN * 0.38)
    return Group(Group(before, mark), Group(result, arc))


def chamfer_shapes() -> tuple[Group, Group]:
    before = Polygon(
        [-1.7, -1.05, 0], [1.7, -1.05, 0], [1.7, 1.05, 0], [-1.7, 1.05, 0],
        color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1,
    )
    edges = VGroup(
        selected_edge(np.array([0.95, 1.05, 0]), np.array([1.7, 1.05, 0])),
        selected_edge(np.array([1.7, 0.30, 0]), np.array([1.7, 1.05, 0])),
    )
    after = Polygon(
        [-1.7, -1.05, 0], [1.7, -1.05, 0], [1.7, 0.36, 0], [1.01, 1.05, 0], [-1.7, 1.05, 0],
        color=INK, stroke_width=3, fill_color=PALE_ORANGE, fill_opacity=1,
    )
    cut = Line([1.01, 1.05, 0], [1.7, 0.36, 0], color=ORANGE, stroke_width=8)
    return Group(before, edges), Group(after, cut)


def bracket_half(color: str = PALE_BLUE) -> Polygon:
    return Polygon(
        [0.18, -1.25, 0], [1.75, -1.25, 0], [1.75, -0.72, 0],
        [0.95, -0.72, 0], [0.95, 0.88, 0], [0.18, 1.25, 0],
        color=INK, stroke_width=3, fill_color=color, fill_opacity=1,
    )


def rib_group() -> Group:
    base = Rectangle(width=4.0, height=0.58, color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1).shift(DOWN * 0.95)
    wall = Rectangle(width=0.62, height=2.65, color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1).shift(LEFT * 1.65 + UP * 0.08)
    rib = Polygon([-1.32, -0.67, 0], [-1.32, 0.88, 0], [0.32, -0.67, 0], color=GREEN, stroke_width=3, fill_color=PALE_GREEN, fill_opacity=1)
    arrow = Arrow([0.65, 0.48, 0], [-0.18, -0.19, 0], color=GREEN, stroke_width=4)
    return Group(base, wall, rib, arrow)


def emboss_group() -> Group:
    plate = RoundedRectangle(width=4.1, height=2.35, corner_radius=0.16, color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1)
    crest = Circle(radius=0.63, color=BLUE, stroke_width=5, fill_color=PALE_CYAN, fill_opacity=1)
    inner = RegularPolygon(n=6, radius=0.38, color=CYAN, stroke_width=4, fill_color=WHITE, fill_opacity=1)
    lift = Arrow([1.35, -0.25, 0], [1.35, 0.65, 0], color=ORANGE, stroke_width=4)
    h = rtext("altura", size=21, color=ORANGE, bold=True).next_to(lift, RIGHT, buff=0.1)
    return Group(plate, crest, inner, lift, h)


def coil_group(turns: float = 4.5) -> Group:
    helix = ParametricFunction(
        lambda t: np.array([2.2 * (t / (TAU * turns) - 0.5), 0.9 * math.sin(t), 0]),
        t_range=[0, TAU * turns, 0.04],
        color=BLUE,
        stroke_width=8,
    )
    axis = DashedLine(LEFT * 2.55, RIGHT * 2.55, color=MUTED, stroke_width=2)
    profile = Circle(radius=0.17, color=ORANGE, fill_color=ORANGE, fill_opacity=1).move_to(helix.get_start())
    pitch = DoubleArrow([-1.82, -1.42, 0], [-0.84, -1.42, 0], color=GREEN, stroke_width=3, tip_length=0.13)
    p_label = rtext("paso", size=23, color=GREEN, bold=True).next_to(pitch, DOWN, buff=0.08)
    return Group(axis, helix, profile, pitch, p_label)


def linear_pattern() -> Group:
    plate = RoundedRectangle(width=5.1, height=2.0, corner_radius=0.15, color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1)
    holes = VGroup(*[Circle(radius=0.24, color=BLUE, stroke_width=4, fill_color=WHITE, fill_opacity=1).shift(LEFT * 1.75 + RIGHT * i * 1.15) for i in range(4)])
    direction = Arrow(LEFT * 2.1 + DOWN * 1.38, RIGHT * 2.1 + DOWN * 1.38, color=ORANGE, stroke_width=4)
    label = rtext("cantidad + separación", size=22, color=ORANGE, bold=True).next_to(direction, DOWN, buff=0.08)
    return Group(plate, holes, direction, label)


def circular_pattern() -> Group:
    outer = Circle(radius=1.45, color=INK, stroke_width=3, fill_color=PALE_BLUE, fill_opacity=1)
    center = Circle(radius=0.32, color=INK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
    holes = VGroup(*[
        Circle(radius=0.18, color=CYAN, stroke_width=3, fill_color=WHITE, fill_opacity=1).move_to(1.03 * np.array([math.cos(k * TAU / 8), math.sin(k * TAU / 8), 0]))
        for k in range(8)
    ])
    arc = Arc(radius=1.78, start_angle=0.15, angle=1.45 * PI, color=ORANGE, stroke_width=4)
    arc.add_tip(tip_length=0.18)
    return Group(outer, center, holes, arc)


class InventorMiscOperations(MovingCameraScene):
    """Preliminary class video: one design problem, eight Inventor operations."""

    def setup_slide(self, page: int) -> None:
        self.add(grid_background(), footer(page))

    def clear_slide(self, run_time: float = 0.55) -> None:
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def construct(self):
        self.camera.background_color = "#F7F9FC"

        # 01 — Portada
        self.setup_slide(1)
        ring = Circle(radius=1.42, color=BLUE, stroke_width=8)
        cross = VGroup(
            Line(LEFT * 1.78, RIGHT * 1.78, color=GRID, stroke_width=2),
            Line(DOWN * 1.78, UP * 1.78, color=GRID, stroke_width=2),
        )
        hexagon = RegularPolygon(n=6, radius=0.92, color=INK, stroke_width=5, fill_color=PALE_BLUE, fill_opacity=1)
        hole = Circle(radius=0.36, color=ORANGE, stroke_width=5, fill_color=WHITE, fill_opacity=1)
        icon = Group(cross, ring, hexagon, hole).shift(LEFT * 4.35 + DOWN * 0.25)
        copy = icon.copy().scale(0.82).shift(RIGHT * 0.38 + UP * 0.30).set_opacity(0.22)
        kicker = rtext("AUTODESK INVENTOR", size=27, color=BLUE, bold=True)
        title = rtext("Operaciones\nmisceláneas", size=64, color=INK, bold=True, max_width=7.1)
        subtitle = rtext("Del boceto base a una pieza lista para fabricar", size=31, color=MUTED, max_width=7.1)
        text_group = Group(kicker, title, subtitle).arrange(DOWN, buff=0.22, aligned_edge=LEFT).shift(RIGHT * 2.5 + UP * 0.25)
        tag = pill("VIDEO PRELIMINAR · -pqh", GREEN, width=3.65).next_to(text_group, DOWN, buff=0.42).align_to(text_group, LEFT)
        self.play(Create(cross), Create(ring), DrawBorderThenFill(hexagon), FadeIn(hole, scale=0.6), run_time=1.7)
        self.play(FadeIn(copy), FadeIn(kicker, shift=UP * 0.12), FadeIn(title, shift=UP * 0.12), run_time=1.2)
        self.play(FadeIn(subtitle), FadeIn(tag), run_time=0.8)
        self.wait(2.0)
        self.clear_slide()

        # 02 — Intención de diseño
        self.setup_slide(2)
        heading = title_block("Idea central", "No memorices botones: controla la geometría", "Cada operación responde a una decisión de diseño.")
        self.play(FadeIn(heading, shift=DOWN * 0.12))
        cards = Group(
            info_card("1", "Seleccionar", "Cara, arista, perfil\no eje correcto", color=BLUE),
            info_card("2", "Parametrizar", "Radio, distancia,\nángulo o cantidad", color=ORANGE),
            info_card("3", "Comprobar", "Vista previa, sentido\ny resultado final", color=GREEN),
        ).arrange(RIGHT, buff=0.48).shift(DOWN * 0.70)
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.16), run_time=0.55)
        flow = step_strip(["Entrada", "Operación", "Resultado"]).scale(0.92).shift(DOWN * 2.55)
        self.play(FadeIn(flow), run_time=0.7)
        self.wait(1.7)
        self.clear_slide()

        # 03 — Redondeo y chaflán
        self.setup_slide(3)
        heading = title_block("Familia 1 · Acabado de aristas", "Redondeo y chaflán", "Dos operaciones parecidas, dos intenciones distintas.")
        self.play(FadeIn(heading))
        divider = Line(UP * 1.45, DOWN * 2.72, color=GRID, stroke_width=2)
        left_label = rtext("REDONDEO", size=30, color=GREEN, bold=True).shift(LEFT * 3.55 + UP * 1.23)
        right_label = rtext("CHAFLÁN", size=30, color=ORANGE, bold=True).shift(RIGHT * 3.55 + UP * 1.23)
        self.play(Create(divider), FadeIn(left_label), FadeIn(right_label))
        fillet_before, fillet_after = fillet_demo()
        fillet_before.scale(0.78).shift(LEFT * 3.55 + DOWN * 0.25)
        fillet_after.scale(0.78).move_to(fillet_before)
        chamfer_before, chamfer_after = chamfer_shapes()
        chamfer_before.scale(0.78).shift(RIGHT * 3.55 + DOWN * 0.25)
        chamfer_after.scale(0.78).move_to(chamfer_before)
        self.play(DrawBorderThenFill(fillet_before[0]), FadeIn(fillet_before[1]), DrawBorderThenFill(chamfer_before[0]), FadeIn(chamfer_before[1]), run_time=1.0)
        self.wait(0.6)
        self.play(ReplacementTransform(fillet_before, fillet_after), ReplacementTransform(chamfer_before, chamfer_after), run_time=1.2)
        f_note = rtext("Suaviza transición\nRadio R", size=26, color=MUTED, max_width=3.7).shift(LEFT * 3.55 + DOWN * 1.85)
        c_note = rtext("Corta la esquina\nDistancia / ángulo", size=26, color=MUTED, max_width=3.7).shift(RIGHT * 3.55 + DOWN * 1.85)
        self.play(FadeIn(f_note), FadeIn(c_note))
        self.wait(2.0)
        self.clear_slide()

        # 04 — Simetría
        self.setup_slide(4)
        heading = title_block("Familia 2 · Reutilizar intención", "Simetría", "Modela una vez; refleja respecto a un plano confiable.")
        self.play(FadeIn(heading))
        axis = DashedLine(DOWN * 2.25, UP * 1.25, color=ORANGE, stroke_width=4)
        axis_label = rtext("plano medio", size=24, color=ORANGE, bold=True).next_to(axis, DOWN, buff=0.15)
        left_half = bracket_half().flip(RIGHT).shift(LEFT * 0.16 + DOWN * 0.45)
        right_ghost = bracket_half(PALE_GREEN).shift(RIGHT * 0.16 + DOWN * 0.45).set_opacity(0.18)
        self.play(Create(axis), FadeIn(axis_label), DrawBorderThenFill(left_half), run_time=1.1)
        self.play(FadeIn(right_ghost), run_time=0.5)
        self.play(right_ghost.animate.set_opacity(1), run_time=0.9)
        checks = Group(
            pill("1 · Crear media pieza", BLUE, width=3.0),
            pill("2 · Elegir plano", ORANGE, width=2.7),
            pill("3 · Reflejar", GREEN, width=2.25),
        ).arrange(RIGHT, buff=0.35).shift(DOWN * 2.52)
        self.play(FadeIn(checks, shift=UP * 0.12))
        self.wait(2.0)
        self.clear_slide()

        # 05 — Nervio y repujado
        self.setup_slide(5)
        heading = title_block("Familia 3 · Añadir función", "Nervio y repujado", "Rigidez estructural frente a identidad y relieve.")
        self.play(FadeIn(heading))
        divider = Line(UP * 1.45, DOWN * 2.72, color=GRID, stroke_width=2)
        rib = rib_group().scale(0.92).shift(LEFT * 3.45 + DOWN * 0.30)
        emboss = emboss_group().scale(0.93).shift(RIGHT * 3.45 + DOWN * 0.25)
        rib_title = rtext("NERVIO", size=30, color=GREEN, bold=True).shift(LEFT * 3.45 + UP * 1.20)
        emboss_title = rtext("REPUJADO", size=30, color=BLUE, bold=True).shift(RIGHT * 3.45 + UP * 1.20)
        self.play(Create(divider), FadeIn(rib_title), FadeIn(emboss_title))
        self.play(DrawBorderThenFill(rib[0]), DrawBorderThenFill(rib[1]), run_time=0.7)
        self.play(GrowFromEdge(rib[2], DOWN), GrowArrow(rib[3]), run_time=0.9)
        self.play(DrawBorderThenFill(emboss[0]), Create(emboss[1]), Create(emboss[2]), GrowArrow(emboss[3]), FadeIn(emboss[4]), run_time=1.0)
        notes = Group(
            rtext("Croquis abierto + espesor", size=24, color=MUTED, max_width=4.6),
            rtext("Perfil cerrado + altura", size=24, color=MUTED, max_width=4.6),
        )
        notes[0].shift(LEFT * 3.45 + DOWN * 2.30)
        notes[1].shift(RIGHT * 3.45 + DOWN * 2.30)
        self.play(FadeIn(notes))
        self.wait(2.0)
        self.clear_slide()

        # 06 — Bobina
        self.setup_slide(6)
        heading = title_block("Familia 4 · Geometría helicoidal", "Bobina", "Un perfil gira y avanza alrededor de un eje.")
        self.play(FadeIn(heading))
        coil = coil_group().scale(1.28).shift(UP * 0.03)
        self.play(Create(coil[0]), FadeIn(coil[2]))
        self.play(Create(coil[1]), run_time=2.2)
        self.play(GrowFromCenter(coil[3]), FadeIn(coil[4]))
        controls = Group(
            pill("Perfil", BLUE, width=1.9),
            pill("Eje", ORANGE, width=1.65),
            pill("Paso", GREEN, width=1.75),
            pill("Vueltas", CYAN, width=1.95),
        ).arrange(RIGHT, buff=0.34).shift(DOWN * 2.52)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in controls], lag_ratio=0.14))
        self.wait(2.0)
        self.clear_slide()

        # 07 — Patrones
        self.setup_slide(7)
        heading = title_block("Familia 5 · Repetición paramétrica", "Patrones lineales y circulares", "Copia una operación; controla cantidad, separación y dirección.")
        self.play(FadeIn(heading))
        divider = Line(UP * 1.35, DOWN * 2.72, color=GRID, stroke_width=2)
        linear = linear_pattern().scale(0.92).shift(LEFT * 3.45 + DOWN * 0.20)
        circular = circular_pattern().scale(0.90).shift(RIGHT * 3.45 + DOWN * 0.15)
        l_title = rtext("PATRÓN RECTANGULAR (LINEAL)", size=26, color=BLUE, bold=True, max_width=5.8).shift(LEFT * 3.45 + UP * 1.22)
        c_title = rtext("PATRÓN CIRCULAR", size=28, color=CYAN, bold=True).shift(RIGHT * 3.45 + UP * 1.22)
        self.play(Create(divider), FadeIn(l_title), FadeIn(c_title))
        self.play(DrawBorderThenFill(linear[0]), FadeIn(linear[1][0]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(h, scale=0.6) for h in linear[1][1:]], lag_ratio=0.20), GrowArrow(linear[2]), FadeIn(linear[3]), run_time=1.2)
        self.play(DrawBorderThenFill(circular[0]), FadeIn(circular[1]))
        self.play(LaggedStart(*[FadeIn(h, scale=0.5) for h in circular[2]], lag_ratio=0.10), Create(circular[3]), run_time=1.4)
        warning = pill("Patrona la operación, no todo el sólido", RED, width=5.2).shift(DOWN * 2.62)
        self.play(FadeIn(warning, shift=UP * 0.1))
        self.wait(2.0)
        self.clear_slide()

        # 08 — Mapa de decisión
        self.setup_slide(8)
        heading = title_block("Mapa de decisión", "¿Qué operación necesito?", "Empieza por la intención, luego busca el comando.")
        self.play(FadeIn(heading))
        rows = [
            ("Suavizar una arista", "Redondeo", GREEN),
            ("Crear una cara inclinada", "Chaflán", ORANGE),
            ("Duplicar respecto a un plano", "Simetría", BLUE),
            ("Aumentar rigidez", "Nervio", GREEN),
            ("Crear relieve o marca", "Repujado", CYAN),
            ("Generar hélice", "Bobina", BLUE),
            ("Repetir geometría", "Patrón", ORANGE),
        ]
        table = Group()
        for idx, (need, command, color) in enumerate(rows):
            y = 1.18 - idx * 0.56
            left_box = RoundedRectangle(width=5.55, height=0.45, corner_radius=0.10, color=GRID, stroke_width=1.2, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 2.85 + UP * y)
            right_box = RoundedRectangle(width=3.15, height=0.45, corner_radius=0.10, color=color, stroke_width=1.5, fill_color=WHITE, fill_opacity=1).move_to(RIGHT * 2.20 + UP * y)
            need_t = rtext(need, size=22, color=INK, max_width=5.0).move_to(left_box)
            command_t = rtext(command, size=22, color=color, bold=True, max_width=2.7).move_to(right_box)
            arrow = Arrow(left_box.get_right() + RIGHT * 0.16, right_box.get_left() + LEFT * 0.16, color=MUTED, stroke_width=2.2, buff=0.08, tip_length=0.16)
            row = Group(left_box, right_box, need_t, command_t, arrow)
            table.add(row)
        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.10), run_time=0.32)
        self.wait(1.8)
        self.clear_slide()

        # 09 — Reto de clase
        self.setup_slide(9)
        heading = title_block("Workshop · Reto integrador", "Diseña un soporte paramétrico", "La pieza debe poder modificarse sin rehacer el modelo.")
        self.play(FadeIn(heading))
        part_left = bracket_half(PALE_BLUE).flip(RIGHT).shift(LEFT * 0.16)
        part_right = bracket_half(PALE_GREEN).shift(RIGHT * 0.16)
        part = Group(part_left, part_right).scale(1.12).shift(LEFT * 3.95 + DOWN * 0.35)
        center_hole = Circle(radius=0.38, color=ORANGE, stroke_width=5, fill_color=WHITE, fill_opacity=1).move_to(part).shift(DOWN * 0.47)
        top_holes = VGroup(*[
            Circle(radius=0.16, color=CYAN, stroke_width=3, fill_color=WHITE, fill_opacity=1).shift(LEFT * 4.55 + RIGHT * i * 0.63 + UP * 0.49)
            for i in range(3)
        ])
        self.play(DrawBorderThenFill(part_left), DrawBorderThenFill(part_right), FadeIn(center_hole), LaggedStart(*[FadeIn(h) for h in top_holes], lag_ratio=0.15), run_time=1.3)
        tasks = Group(
            info_card("1", "Base", "Croquis + extrusión", color=BLUE, width=3.0, height=1.23),
            info_card("2", "Acabado", "R6 y chaflán 4 × 45°", color=ORANGE, width=3.0, height=1.23),
            info_card("3", "Función", "Nervio + repujado", color=GREEN, width=3.0, height=1.23),
            info_card("4", "Repetición", "Simetría + patrones", color=CYAN, width=3.0, height=1.23),
        ).arrange(DOWN, buff=0.18).scale(0.95).shift(RIGHT * 3.25 + DOWN * 0.52)
        for card in tasks:
            self.play(FadeIn(card, shift=LEFT * 0.12), run_time=0.42)
        criterion = pill("Criterio: modelo editable y ordenado", RED, width=5.45).shift(DOWN * 2.78 + LEFT * 1.10)
        self.play(FadeIn(criterion, shift=UP * 0.08))
        self.wait(2.3)
        self.clear_slide()

        # 10 — Cierre
        self.setup_slide(10)
        final = title_block("Próxima clase", "Construcción guiada en Inventor", "Boceto → operación base → detalles → verificación")
        final.shift(DOWN * 0.30)
        orbit = Circle(radius=1.55, color=BLUE, stroke_width=5).shift(DOWN * 0.65)
        nodes = VGroup(*[
            Circle(radius=0.16, color=color, fill_color=color, fill_opacity=1).move_to(orbit.point_from_proportion(p))
            for color, p in [(BLUE, 0.03), (ORANGE, 0.28), (GREEN, 0.53), (CYAN, 0.78)]
        ])
        core = RegularPolygon(n=6, radius=0.62, color=INK, stroke_width=5, fill_color=WHITE, fill_opacity=1).shift(DOWN * 0.65)
        self.play(FadeIn(final), Create(orbit), LaggedStart(*[FadeIn(n, scale=0.4) for n in nodes], lag_ratio=0.16), DrawBorderThenFill(core), run_time=1.6)
        close = pill("Diseña con intención", GREEN, width=3.35).shift(DOWN * 2.75)
        self.play(FadeIn(close, shift=UP * 0.1))
        self.wait(2.8)


if __name__ == "__main__":
    print("Render with: manim -pqh Inventor_Misc_Operations_PRELIM_PQH.py InventorMiscOperations")
